# -*- coding: utf-8 -*-
"""
Lambda do Roteiro: contas, login e sincronização do progresso (DynamoDB).

Tudo numa única tabela (DYNAMODB_TABLE), com a chave "user_id" prefixada:
  acct#<email>   conta: nome, papel (aluno/admin), situação, senha (PBKDF2), códigos
  data#<email>   dados de estudo do aluno: progresso, projetos, extra...
  audit#<ts>#<id> registro das ações do admin
Itens antigos (chave = e-mail puro) são do formato anterior: só são lidos ao convidar
esse e-mail, para importar o progresso que já existia.

Variáveis de ambiente:
  TOKEN_SECRET       obrigatório, 32+ caracteres aleatórios (assina os tokens)
  BOOTSTRAP_SECRET   opcional; permite criar a PRIMEIRA conta admin (depois pode apagar)
  SES_SENDER_EMAIL   remetente verificado no Amazon SES (convites e recuperação)
  APP_URL            endereço do site, usado no texto dos e-mails
  DYNAMODB_TABLE     padrão: roteiro_estudos_joao
  PBKDF2_ITER        padrão: 600000 (se o login ficar lento, aumente a memória da Lambda)

Todas as chamadas são POST com JSON {"action": ..., "token": ...}. O token também
pode vir no header "Authorization: Bearer <token>".
"""

import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import time
from decimal import Decimal

TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "roteiro_estudos_joao")
REGIONS_TO_TRY = ["us-east-2", "us-east-1", "sa-east-1"]
PBKDF2_ITER = int(os.environ.get("PBKDF2_ITER") or 600000)  # recomendação OWASP para PBKDF2-SHA256

TOKEN_TTL = {"app": 12 * 3600, "app_long": 7 * 24 * 3600, "admin": 3600}
CODE_TTL = {"invite": 7 * 24 * 3600, "reset": 15 * 60}
CODE_MAX_TRIES = 5
LOGIN_MAX_FAILS = 5
LOGIN_LOCK_SECONDS = 15 * 60
MAX_DATA_BYTES = 350_000
MIN_PASSWORD = 8

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TRAIL_PREFIX = {"ia": "ia-", "mat": "mat-", "ing": "ing-"}
DATA_FIELDS = ("progress", "projects", "start_date", "pace", "extra")

GENERIC_LOGIN_ERROR = "E-mail ou senha incorretos."
GENERIC_CODE_ERROR = "Código inválido ou expirado."


# ---------------------------------------------------------------------------
# Erros e respostas
# ---------------------------------------------------------------------------
class ApiError(Exception):
    def __init__(self, status, message, **extra):
        super().__init__(message)
        self.status = status
        self.message = message
        self.extra = extra


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super().default(obj)


def _response(status, body):
    # O CORS (origens permitidas) é configurado na Function URL; não duplicar headers aqui.
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store"},
        "body": json.dumps(body, cls=DecimalEncoder, ensure_ascii=False),
    }


def now():
    return int(time.time())


# ---------------------------------------------------------------------------
# Armazenamento (DynamoDB). Os testes trocam por um armazenamento em memória.
# ---------------------------------------------------------------------------
class DynamoStore:
    def __init__(self):
        self._table = None

    def _tbl(self):
        if self._table is not None:
            return self._table
        import boto3
        env_region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        regions = [env_region] if env_region else []
        regions += [r for r in REGIONS_TO_TRY if r not in regions]
        last = None
        for reg in regions:
            try:
                table = boto3.resource("dynamodb", region_name=reg).Table(TABLE_NAME)
                table.load()
                self._table = table
                return table
            except Exception as exc:
                if "ResourceNotFoundException" in str(exc):  # tabela não existe nessa região
                    last = exc
                    continue
                if "AccessDenied" in str(exc):  # sem permissão de DescribeTable: usa a região mesmo assim
                    self._table = table
                    return table
                raise
        raise last or RuntimeError("Tabela não encontrada")

    def get(self, key):
        return self._tbl().get_item(Key={"user_id": key}, ConsistentRead=True).get("Item")

    def put(self, item):
        self._tbl().put_item(Item=item)

    def put_new(self, item):
        """Grava só se a chave ainda não existe. Retorna False se já existia."""
        try:
            self._tbl().put_item(Item=item, ConditionExpression="attribute_not_exists(user_id)")
            return True
        except Exception as exc:
            if "ConditionalCheckFailed" in str(exc):
                return False
            raise

    def delete(self, key):
        self._tbl().delete_item(Key={"user_id": key})

    def scan_prefix(self, prefix):
        from boto3.dynamodb.conditions import Attr
        kwargs = {"FilterExpression": Attr("user_id").begins_with(prefix)}
        items = []
        while True:
            resp = self._tbl().scan(**kwargs)
            items += resp.get("Items", [])
            if "LastEvaluatedKey" not in resp:
                return items
            kwargs["ExclusiveStartKey"] = resp["LastEvaluatedKey"]


def send_email_ses(to, subject, text, html):
    import boto3
    sender = os.environ.get("SES_SENDER_EMAIL")
    if not sender:
        raise ApiError(503, "Envio de e-mail não configurado (SES_SENDER_EMAIL).")
    region = os.environ.get("SES_REGION") or os.environ.get("AWS_REGION") or "us-east-2"
    boto3.client("ses", region_name=region).send_email(
        Source=sender,
        Destination={"ToAddresses": [to]},
        Message={
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body": {"Text": {"Data": text, "Charset": "UTF-8"}, "Html": {"Data": html, "Charset": "UTF-8"}},
        },
    )


STORE = DynamoStore()
SEND_EMAIL = send_email_ses


# ---------------------------------------------------------------------------
# Senhas, códigos e tokens
# ---------------------------------------------------------------------------
def hash_password(password, salt=None, iterations=None):
    salt = salt or secrets.token_hex(16)
    iterations = int(iterations or PBKDF2_ITER)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), iterations).hex()
    return {"alg": "pbkdf2_sha256", "iter": iterations, "salt": salt, "hash": digest}


def check_password(password, record):
    if not record or not record.get("hash"):
        # Gasta o mesmo tempo para não revelar se a conta existe.
        hash_password(password or "x")
        return False
    test = hash_password(password, record["salt"], int(record["iter"]))
    return hmac.compare_digest(test["hash"], record["hash"])


def hash_code(code, email):
    return hmac.new(_secret(), f"{email}:{code}".encode(), hashlib.sha256).hexdigest()


def new_code():
    return f"{secrets.randbelow(1_000_000):06d}"


def _secret():
    s = os.environ.get("TOKEN_SECRET") or ""
    if len(s) < 32:
        raise ApiError(503, "Servidor sem TOKEN_SECRET configurado (mínimo 32 caracteres).")
    return s.encode()


def _b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _unb64(text):
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def make_token(acct, aud, long_session=False):
    ttl = TOKEN_TTL["app_long" if (aud == "app" and long_session) else aud]
    payload = {"sub": acct["email"], "role": acct["role"], "aud": aud, "tv": int(acct.get("tv", 0)),
               "iat": now(), "exp": now() + ttl}
    body = _b64(json.dumps(payload, separators=(",", ":")).encode())
    sig = _b64(hmac.new(_secret(), body.encode(), hashlib.sha256).digest())
    return f"{body}.{sig}", payload["exp"]


def read_token(token):
    try:
        body, sig = token.split(".")
        good = _b64(hmac.new(_secret(), body.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(sig, good):
            return None
        payload = json.loads(_unb64(body))
        if payload.get("exp", 0) < now():
            return None
        return payload
    except ApiError:
        raise
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Contas
# ---------------------------------------------------------------------------
def norm_email(value):
    email = str(value or "").strip().lower()
    if not EMAIL_RE.match(email) or len(email) > 254:
        raise ApiError(400, "Informe um e-mail válido.")
    return email


def check_new_password(pwd):
    pwd = str(pwd or "")
    if len(pwd) < MIN_PASSWORD:
        raise ApiError(400, f"A senha precisa ter pelo menos {MIN_PASSWORD} caracteres.")
    if len(pwd) > 200:
        raise ApiError(400, "Senha longa demais.")
    return pwd


def get_acct(email):
    return STORE.get(f"acct#{email}")


def public_user(acct, data=None):
    out = {
        "email": acct["email"], "name": acct.get("name", ""), "role": acct["role"], "status": acct["status"],
        "created_at": acct.get("created_at"), "last_login": acct.get("last_login"),
        "invite_pending": acct.get("code_kind") == "invite",
    }
    if data is not None:
        prog = data.get("progress") or {}
        out["progress_summary"] = progress_summary(prog)
        out["last_sync"] = data.get("updated_at")
    return out


def progress_summary(progress):
    summary = {}
    for trail, prefix in TRAIL_PREFIX.items():
        done = started = 0
        for key, val in progress.items():
            if key.startswith(prefix) and isinstance(val, dict):
                if val.get("s") == "e":
                    done += 1
                elif val.get("s") not in (None, "", "z"):
                    started += 1
        summary[trail] = {"done": done, "started": started}
    return summary


def issue_code(acct, kind):
    code = new_code()
    acct.update({"code_kind": kind, "code_hash": hash_code(code, acct["email"]),
                 "code_exp": now() + CODE_TTL[kind], "code_tries": 0})
    return code


def consume_code(acct, kind, code):
    """Confere o código; conta as tentativas erradas. Lança ApiError se não servir."""
    if not acct or acct.get("code_kind") != kind or acct.get("status") == "blocked":
        raise ApiError(400, GENERIC_CODE_ERROR)
    if int(acct.get("code_exp", 0)) < now() or int(acct.get("code_tries", 0)) >= CODE_MAX_TRIES:
        raise ApiError(400, GENERIC_CODE_ERROR)
    if not hmac.compare_digest(hash_code(str(code or "").strip(), acct["email"]), acct.get("code_hash", "")):
        acct["code_tries"] = int(acct.get("code_tries", 0)) + 1
        STORE.put(acct)
        raise ApiError(400, GENERIC_CODE_ERROR)
    for k in ("code_kind", "code_hash", "code_exp", "code_tries"):
        acct.pop(k, None)


def send_code_email(acct, code, kind):
    app_url = os.environ.get("APP_URL", "")
    if kind == "invite":
        subject = "Seu convite para o Roteiro de Estudos"
        intro = f"Olá, {acct.get('name') or 'estudante'}! Você foi convidado para o Roteiro de Estudos."
        action = "Abra o site, escolha \"Tenho um convite\" e use este código para criar sua senha. Ele vale por 7 dias."
    else:
        subject = "Código para redefinir sua senha · Roteiro de Estudos"
        intro = "Recebemos um pedido para redefinir a senha da sua conta."
        action = "Use este código na tela \"Esqueci a senha\". Ele vale por 15 minutos. Se não foi você, ignore este e-mail."
    text = f"{intro}\n\nCódigo: {code}\n\n{action}\n\n{app_url}"
    html = (f"<div style=\"font-family:Arial,sans-serif;max-width:480px\"><p>{intro}</p>"
            f"<p style=\"font-size:30px;font-weight:700;letter-spacing:6px\">{code}</p>"
            f"<p>{action}</p><p><a href=\"{app_url}\">{app_url}</a></p></div>")
    SEND_EMAIL(acct["email"], subject, text, html)


def audit(admin_email, action, target="", details=None):
    STORE.put({"user_id": f"audit#{now():010d}#{secrets.token_hex(4)}", "at": now(), "admin": admin_email,
               "action": action, "target": target, "details": details or {}})


# ---------------------------------------------------------------------------
# Ações públicas
# ---------------------------------------------------------------------------
def act_login(p, _ctx):
    email = str(p.get("email") or "").strip().lower()
    password = str(p.get("password") or "")
    aud = "admin" if p.get("aud") == "admin" else "app"
    acct = get_acct(email) if EMAIL_RE.match(email) else None

    if acct and int(acct.get("locked_until", 0)) > now():
        hash_password(password or "x")
        raise ApiError(429, "Muitas tentativas. Tente de novo em alguns minutos.")

    ok = check_password(password, acct.get("pwd") if acct else None)
    role_ok = acct is not None and ((aud == "admin") == (acct.get("role") == "admin"))
    if not (ok and role_ok and acct.get("status") == "active"):
        if acct:
            fails = int(acct.get("failed", 0)) + 1
            acct["failed"] = 0 if fails >= LOGIN_MAX_FAILS else fails
            if fails >= LOGIN_MAX_FAILS:
                acct["locked_until"] = now() + LOGIN_LOCK_SECONDS
            STORE.put(acct)
        if ok and role_ok and acct.get("status") == "blocked":
            raise ApiError(403, "Esta conta está bloqueada. Fale com o administrador.")
        raise ApiError(401, GENERIC_LOGIN_ERROR)

    acct.update({"failed": 0, "locked_until": 0, "last_login": now()})
    STORE.put(acct)
    token, exp = make_token(acct, aud, bool(p.get("remember")))
    return {"token": token, "expires_at": exp, "user": public_user(acct)}


def act_accept_invite(p, _ctx):
    email = norm_email(p.get("email"))
    password = check_new_password(p.get("password"))
    acct = get_acct(email)
    consume_code(acct, "invite", p.get("code"))
    acct.pop("code_sent_at", None)  # o envio do convite não deve atrasar uma recuperação de senha
    acct.update({"pwd": hash_password(password), "status": "active", "tv": int(acct.get("tv", 0)) + 1,
                 "failed": 0, "locked_until": 0, "last_login": now()})
    if str(p.get("name") or "").strip():
        acct["name"] = str(p["name"]).strip()[:80]
    STORE.put(acct)
    token, exp = make_token(acct, "app", bool(p.get("remember")))
    return {"token": token, "expires_at": exp, "user": public_user(acct)}


def act_request_reset(p, _ctx):
    email = str(p.get("email") or "").strip().lower()
    acct = get_acct(email) if EMAIL_RE.match(email) else None
    # Resposta igual exista ou não a conta (não revela quem está cadastrado).
    if acct and acct.get("status") == "active" and acct.get("role") == "student":
        last = int(acct.get("code_sent_at", 0))
        if now() - last >= 60:
            code = issue_code(acct, "reset")
            acct["code_sent_at"] = now()
            STORE.put(acct)
            send_code_email(acct, code, "reset")
    return {"message": "Se o e-mail estiver cadastrado, enviamos um código para ele."}


def act_confirm_reset(p, _ctx):
    email = norm_email(p.get("email"))
    password = check_new_password(p.get("password"))
    acct = get_acct(email)
    consume_code(acct, "reset", p.get("code"))
    acct.update({"pwd": hash_password(password), "tv": int(acct.get("tv", 0)) + 1,
                 "failed": 0, "locked_until": 0})
    STORE.put(acct)
    return {"message": "Senha redefinida. Entre com a nova senha."}


def act_bootstrap_admin(p, _ctx):
    """Cria a primeira conta admin, ou redefine a senha do admin existente (recuperação).
    Só funciona enquanto BOOTSTRAP_SECRET estiver configurado na Lambda."""
    expected = os.environ.get("BOOTSTRAP_SECRET") or ""
    if len(expected) < 16 or not hmac.compare_digest(str(p.get("secret") or ""), expected):
        raise ApiError(403, "Não autorizado.")
    email = norm_email(p.get("email"))
    password = check_new_password(p.get("password"))
    admins = [a for a in STORE.scan_prefix("acct#") if a.get("role") == "admin"]
    if admins:
        acct = next((a for a in admins if a["email"] == email), None)
        if not acct:
            raise ApiError(409, "Já existe uma conta admin com outro e-mail.")
        acct.update({"pwd": hash_password(password), "tv": int(acct.get("tv", 0)) + 1, "status": "active",
                     "failed": 0, "locked_until": 0})
        STORE.put(acct)
        audit(email, "bootstrap_reset_admin", email)
        return {"message": "Senha do admin redefinida. Agora remova BOOTSTRAP_SECRET da Lambda."}
    acct = {"user_id": f"acct#{email}", "email": email, "name": str(p.get("name") or "Administrador")[:80],
            "role": "admin", "status": "active", "pwd": hash_password(password), "tv": 1,
            "created_at": now(), "failed": 0, "locked_until": 0}
    if not STORE.put_new(acct):
        raise ApiError(409, "Esse e-mail já tem conta. Use outro e-mail para o admin.")
    audit(email, "bootstrap_admin", email)
    return {"message": "Conta admin criada. Agora remova BOOTSTRAP_SECRET da Lambda."}


# ---------------------------------------------------------------------------
# Ações do aluno (token "app")
# ---------------------------------------------------------------------------
def act_me(_p, ctx):
    return {"user": public_user(ctx["acct"])}


def act_get_data(_p, ctx):
    data = STORE.get(f"data#{ctx['acct']['email']}") or {}
    return {"data": {k: data.get(k) for k in DATA_FIELDS + ("updated_at",) if k in data}}


def act_save_data(p, ctx):
    email = ctx["acct"]["email"]
    incoming = {k: p[k] for k in DATA_FIELDS if k in p}
    if not isinstance(incoming.get("progress", {}), dict) or not isinstance(incoming.get("projects", []), list):
        raise ApiError(400, "Formato de dados inválido.")
    prev = STORE.get(f"data#{email}") or {}
    item = {"user_id": f"data#{email}"}
    for k in DATA_FIELDS:
        item[k] = incoming[k] if k in incoming else prev.get(k)
        if item[k] is None:
            item.pop(k)
    item["updated_at"] = int(p.get("updated_at") or now() * 1000)
    if len(json.dumps(item, cls=DecimalEncoder)) > MAX_DATA_BYTES:
        raise ApiError(413, "Dados grandes demais para sincronizar.")
    STORE.put(item)
    return {"synced": True, "updated_at": item["updated_at"]}


def act_change_password(p, ctx):
    acct = ctx["acct"]
    if not check_password(str(p.get("current") or ""), acct.get("pwd")):
        raise ApiError(401, "A senha atual está incorreta.")
    acct["pwd"] = hash_password(check_new_password(p.get("new")))
    acct["tv"] = int(acct.get("tv", 0)) + 1  # derruba as outras sessões
    STORE.put(acct)
    token, exp = make_token(acct, ctx["aud"], bool(p.get("remember")))
    return {"token": token, "expires_at": exp, "message": "Senha alterada."}


def act_update_profile(p, ctx):
    acct = ctx["acct"]
    name = str(p.get("name") or "").strip()[:80]
    if not name:
        raise ApiError(400, "Informe um nome.")
    acct["name"] = name
    STORE.put(acct)
    return {"user": public_user(acct)}


# ---------------------------------------------------------------------------
# Ações do admin (token "admin")
# ---------------------------------------------------------------------------
def _student(email):
    acct = get_acct(norm_email(email))
    if not acct or acct.get("role") != "student":
        raise ApiError(404, "Aluno não encontrado.")
    return acct


def act_admin_list_users(_p, _ctx):
    accts = [a for a in STORE.scan_prefix("acct#") if a.get("role") == "student"]
    datas = {d["user_id"][5:]: d for d in STORE.scan_prefix("data#")}
    users = [public_user(a, datas.get(a["email"], {})) for a in accts]
    users.sort(key=lambda u: (u["name"] or u["email"]).lower())
    return {"users": users}


def act_admin_get_user(p, _ctx):
    acct = _student(p.get("email"))
    data = STORE.get(f"data#{acct['email']}") or {}
    return {"user": public_user(acct, data),
            "data": {k: data.get(k) for k in DATA_FIELDS + ("updated_at",) if k in data}}


def act_admin_invite(p, ctx):
    email = norm_email(p.get("email"))
    name = str(p.get("name") or "").strip()[:80]
    if not name:
        raise ApiError(400, "Informe o nome do aluno.")
    acct = {"user_id": f"acct#{email}", "email": email, "name": name, "role": "student", "status": "invited",
            "tv": 0, "created_at": now(), "failed": 0, "locked_until": 0}
    code = issue_code(acct, "invite")
    acct["code_sent_at"] = now()
    if not STORE.put_new(acct):
        raise ApiError(409, "Esse e-mail já tem conta.")
    imported = False
    legacy = STORE.get(email)  # item do formato antigo (chave = e-mail)
    if legacy and not STORE.get(f"data#{email}"):
        item = {"user_id": f"data#{email}", "updated_at": int(legacy.get("updated_at") or now() * 1000)}
        for k in DATA_FIELDS:
            if legacy.get(k) is not None:
                item[k] = legacy[k]
        STORE.put(item)
        imported = True
    try:
        send_code_email(acct, code, "invite")
        sent = True
    except Exception:
        sent = False
    audit(ctx["acct"]["email"], "invite", email, {"name": name, "imported_legacy": imported, "email_sent": sent})
    msg = "Convite enviado." if sent else "Conta criada, mas o e-mail não foi enviado. Use \"Reenviar convite\"."
    return {"user": public_user(acct), "email_sent": sent, "imported_legacy": imported, "message": msg}


def act_admin_resend_invite(p, ctx):
    acct = _student(p.get("email"))
    if acct.get("status") != "invited":
        raise ApiError(400, "Esse aluno já aceitou o convite.")
    code = issue_code(acct, "invite")
    acct["code_sent_at"] = now()
    STORE.put(acct)
    send_code_email(acct, code, "invite")
    audit(ctx["acct"]["email"], "resend_invite", acct["email"])
    return {"message": "Convite reenviado."}


def act_admin_set_status(p, ctx):
    acct = _student(p.get("email"))
    status = p.get("status")
    if status not in ("active", "blocked"):
        raise ApiError(400, "Situação inválida.")
    if status == "active" and not (acct.get("pwd") or {}).get("hash"):
        raise ApiError(400, "Esse aluno ainda não criou senha. Reenvie o convite.")
    acct["status"] = status
    acct["tv"] = int(acct.get("tv", 0)) + 1  # bloquear derruba os tokens já emitidos
    STORE.put(acct)
    audit(ctx["acct"]["email"], "set_status", acct["email"], {"status": status})
    return {"user": public_user(acct)}


def act_admin_delete_user(p, ctx):
    acct = _student(p.get("email"))
    if str(p.get("confirm") or "").strip().lower() != acct["email"]:
        raise ApiError(400, "Para excluir, confirme digitando o e-mail do aluno.")
    STORE.delete(f"acct#{acct['email']}")
    STORE.delete(f"data#{acct['email']}")
    audit(ctx["acct"]["email"], "delete_user", acct["email"])
    return {"message": "Aluno excluído."}


def act_admin_force_reset(p, ctx):
    acct = _student(p.get("email"))
    if acct.get("status") != "active":
        raise ApiError(400, "Só dá para forçar a troca de senha de um aluno ativo.")
    acct.pop("pwd", None)
    acct["tv"] = int(acct.get("tv", 0)) + 1
    code = issue_code(acct, "reset")
    acct["code_sent_at"] = now()
    STORE.put(acct)
    try:
        send_code_email(acct, code, "reset")
        sent = True
    except Exception:
        sent = False
    audit(ctx["acct"]["email"], "force_reset", acct["email"], {"email_sent": sent})
    return {"email_sent": sent, "message": "Senha anulada. O aluno precisa usar \"Esqueci a senha\"."}


def act_admin_edit_progress(p, ctx):
    acct = _student(p.get("email"))
    key = f"data#{acct['email']}"
    data = STORE.get(key) or {"user_id": key}
    progress = dict(data.get("progress") or {})
    op = p.get("op")
    if op == "reset_trail":
        prefix = TRAIL_PREFIX.get(p.get("trail"))
        if not prefix:
            raise ApiError(400, "Trilha inválida.")
        removed = [k for k in progress if k.startswith(prefix)]
        for k in removed:
            progress.pop(k)
        details = {"op": op, "trail": p.get("trail"), "removed": len(removed)}
    elif op == "set_topics":
        changes = p.get("changes") or {}
        if not isinstance(changes, dict) or not changes or len(changes) > 500:
            raise ApiError(400, "Informe os tópicos a alterar.")
        for topic, status in changes.items():
            if not any(str(topic).startswith(pre) for pre in TRAIL_PREFIX.values()) or status not in ("z", "r", "e"):
                raise ApiError(400, f"Alteração inválida: {topic}")
            entry = dict(progress.get(topic) or {"s": "z", "n": "", "d": ""})
            entry["s"] = status
            if status == "z":
                progress.pop(topic, None)
            else:
                progress[topic] = entry
        details = {"op": op, "changes": changes}
    else:
        raise ApiError(400, "Operação inválida.")
    data["progress"] = progress
    data["updated_at"] = now() * 1000
    STORE.put(data)
    audit(ctx["acct"]["email"], "edit_progress", acct["email"], details)
    return {"progress_summary": progress_summary(progress), "updated_at": data["updated_at"]}


def act_admin_audit(p, _ctx):
    items = STORE.scan_prefix("audit#")
    items.sort(key=lambda i: i["user_id"], reverse=True)
    limit = max(1, min(int(p.get("limit") or 100), 500))
    return {"entries": [{k: i.get(k) for k in ("at", "admin", "action", "target", "details")} for i in items[:limit]]}


# ---------------------------------------------------------------------------
# Roteamento
# ---------------------------------------------------------------------------
PUBLIC = {
    "login": act_login, "accept_invite": act_accept_invite, "request_reset": act_request_reset,
    "confirm_reset": act_confirm_reset, "bootstrap_admin": act_bootstrap_admin,
}
STUDENT = {
    "me": act_me, "get_data": act_get_data, "save_data": act_save_data,
    "change_password": act_change_password, "update_profile": act_update_profile,
}
ADMIN = {
    "admin_list_users": act_admin_list_users, "admin_get_user": act_admin_get_user,
    "admin_invite": act_admin_invite, "admin_resend_invite": act_admin_resend_invite,
    "admin_set_status": act_admin_set_status, "admin_delete_user": act_admin_delete_user,
    "admin_force_reset": act_admin_force_reset, "admin_edit_progress": act_admin_edit_progress,
    "admin_audit": act_admin_audit, "me": act_me, "change_password": act_change_password,
}


def authenticate(token, aud):
    payload = read_token(str(token or ""))
    if not payload or payload.get("aud") != aud:
        raise ApiError(401, "Sessão expirada. Entre novamente.", relogin=True)
    acct = get_acct(payload["sub"])
    if (not acct or acct.get("status") != "active" or int(acct.get("tv", 0)) != int(payload.get("tv", -1))
            or acct.get("role") != payload.get("role")):
        raise ApiError(401, "Sessão expirada. Entre novamente.", relogin=True)
    if aud == "admin" and acct.get("role") != "admin":
        raise ApiError(403, "Acesso restrito ao administrador.")
    return {"acct": acct, "aud": aud}


def handle(payload, headers):
    action = str(payload.get("action") or "")
    token = payload.get("token")
    auth = headers.get("authorization") or headers.get("Authorization") or ""
    if not token and auth.lower().startswith("bearer "):
        token = auth[7:].strip()

    if action in PUBLIC:
        return PUBLIC[action](payload, None)
    if action.startswith("admin_") or payload.get("aud") == "admin":
        if action not in ADMIN:
            raise ApiError(400, "Ação desconhecida.")
        return ADMIN[action](payload, authenticate(token, "admin"))
    if action in STUDENT:
        return STUDENT[action](payload, authenticate(token, "app"))
    raise ApiError(400, "Ação desconhecida.")


def lambda_handler(event, context):
    method = (event.get("requestContext", {}).get("http", {}).get("method") or event.get("httpMethod") or "GET").upper()
    if method == "OPTIONS":
        return _response(200, {"ok": True})
    if method == "GET":
        return _response(200, {"ok": True, "service": "roteiro-auth", "version": 2})
    if method != "POST":
        return _response(405, {"ok": False, "error": "Método não suportado."})
    try:
        raw = event.get("body") or "{}"
        if event.get("isBase64Encoded"):
            raw = base64.b64decode(raw).decode("utf-8")
        if len(raw) > MAX_DATA_BYTES + 20_000:
            raise ApiError(413, "Requisição grande demais.")
        payload = json.loads(raw, parse_float=Decimal)
        if not isinstance(payload, dict):
            raise ApiError(400, "Requisição inválida.")
        result = handle(payload, event.get("headers") or {})
        return _response(200, {"ok": True, **result})
    except ApiError as err:
        return _response(err.status, {"ok": False, "error": err.message, **err.extra})
    except json.JSONDecodeError:
        return _response(400, {"ok": False, "error": "JSON inválido."})
    except Exception as exc:  # não vaza detalhes internos para o navegador
        print("ERRO INTERNO:", repr(exc))
        return _response(500, {"ok": False, "error": "Erro interno no servidor. Tente de novo."})
