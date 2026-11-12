# -*- coding: utf-8 -*-
"""Testes da Lambda de contas (sem AWS). Rodar: python -X utf8 -m unittest test_lambda_auth -v"""

import base64
import json
import os
import unittest
from decimal import Decimal

os.environ["TOKEN_SECRET"] = "t" * 40
os.environ["BOOTSTRAP_SECRET"] = "b" * 20
os.environ["PBKDF2_ITER"] = "1000"  # rápido nos testes

import aws_lambda_dynamodb as L  # noqa: E402

L.PBKDF2_ITER = 1000


class MemStore:
    def __init__(self):
        self.items = {}

    def _copy(self, item):
        return json.loads(json.dumps(item, cls=L.DecimalEncoder), parse_float=Decimal) if item else item

    def get(self, key):
        return self._copy(self.items.get(key))

    def put(self, item):
        self.items[item["user_id"]] = self._copy(item)

    def put_new(self, item):
        if item["user_id"] in self.items:
            return False
        self.put(item)
        return True

    def delete(self, key):
        self.items.pop(key, None)

    def scan_prefix(self, prefix):
        return [self._copy(v) for k, v in self.items.items() if k.startswith(prefix)]


class Base(unittest.TestCase):
    ADMIN = ("chefe@exemplo.com", "SenhaAdmin#1")

    def setUp(self):
        self.store = MemStore()
        L.STORE = self.store
        self.mail = []
        L.SEND_EMAIL = lambda to, subject, text, html: self.mail.append((to, text))
        self.clock = 1_800_000_000
        L.now = lambda: self.clock
        r = self.call("bootstrap_admin", secret="b" * 20, email=self.ADMIN[0], name="Chefe", password=self.ADMIN[1])
        self.assertEqual(r["status"], 200, r)
        self.admin = self.call("login", email=self.ADMIN[0], password=self.ADMIN[1], aud="admin")["body"]["token"]

    def call(self, action, headers=None, **payload):
        payload["action"] = action
        event = {"requestContext": {"http": {"method": "POST"}}, "body": json.dumps(payload), "headers": headers or {}}
        res = L.lambda_handler(event, None)
        return {"status": res["statusCode"], "body": json.loads(res["body"])}

    def last_code(self, email):
        for to, text in reversed(self.mail):
            if to == email:
                return text.split("Código: ")[1][:6]
        raise AssertionError("nenhum e-mail para " + email)

    def make_student(self, email="ana@exemplo.com", pwd="SenhaAna#123", name="Ana"):
        r = self.call("admin_invite", token=self.admin, email=email, name=name)
        self.assertEqual(r["status"], 200, r)
        r = self.call("accept_invite", email=email, code=self.last_code(email), password=pwd)
        self.assertEqual(r["status"], 200, r)
        return r["body"]["token"]


class TestFluxoNormal(Base):
    def test_convite_login_e_dados(self):
        tok = self.make_student()
        r = self.call("save_data", token=tok, progress={"ia-0-0-0": {"s": "e", "n": "", "d": ""}}, pace="std")
        self.assertEqual(r["status"], 200, r)
        r = self.call("login", email="ana@exemplo.com", password="SenhaAna#123")
        self.assertEqual(r["status"], 200)
        r = self.call("get_data", token=r["body"]["token"])
        self.assertEqual(r["body"]["data"]["progress"]["ia-0-0-0"]["s"], "e")

    def test_token_no_header(self):
        tok = self.make_student()
        r = self.call("me", headers={"authorization": "Bearer " + tok})
        self.assertEqual(r["body"]["user"]["email"], "ana@exemplo.com")

    def test_dados_separados_por_aluno(self):
        ana = self.make_student()
        bia = self.make_student("bia@exemplo.com", "SenhaBia#123", "Bia")
        self.call("save_data", token=ana, progress={"ia-1-0-0": {"s": "e"}})
        self.call("save_data", token=bia, progress={"mat-0-0-0": {"s": "r"}})
        self.assertEqual(list(self.call("get_data", token=ana)["body"]["data"]["progress"]), ["ia-1-0-0"])
        self.assertEqual(list(self.call("get_data", token=bia)["body"]["data"]["progress"]), ["mat-0-0-0"])

    def test_save_sem_extra_preserva_extra(self):
        tok = self.make_student()
        self.call("save_data", token=tok, progress={}, extra={"review": {"a": 1}})
        self.call("save_data", token=tok, progress={"ia-0-0-1": {"s": "e"}})
        self.assertEqual(self.call("get_data", token=tok)["body"]["data"]["extra"], {"review": {"a": 1}})

    def test_recuperar_senha(self):
        self.make_student()
        self.clock += 120
        self.call("request_reset", email="ana@exemplo.com")
        r = self.call("confirm_reset", email="ana@exemplo.com", code=self.last_code("ana@exemplo.com"),
                      password="NovaSenha#99")
        self.assertEqual(r["status"], 200, r)
        self.assertEqual(self.call("login", email="ana@exemplo.com", password="SenhaAna#123")["status"], 401)
        self.assertEqual(self.call("login", email="ana@exemplo.com", password="NovaSenha#99")["status"], 200)

    def test_convite_importa_progresso_antigo(self):
        self.store.put({"user_id": "velho@exemplo.com", "pwd_hash": "abc", "progress": {"ia-0-0-0": {"s": "e"}},
                        "pace": "fast"})
        r = self.call("admin_invite", token=self.admin, email="velho@exemplo.com", name="Velho")
        self.assertTrue(r["body"]["imported_legacy"])
        tok = self.call("accept_invite", email="velho@exemplo.com", code=self.last_code("velho@exemplo.com"),
                        password="SenhaVelho#1")["body"]["token"]
        data = self.call("get_data", token=tok)["body"]["data"]
        self.assertEqual(data["pace"], "fast")
        self.assertNotIn("pwd_hash", data)

    def test_trocar_senha_derruba_outras_sessoes(self):
        tok1 = self.make_student()
        tok2 = self.call("login", email="ana@exemplo.com", password="SenhaAna#123")["body"]["token"]
        r = self.call("change_password", token=tok1, current="SenhaAna#123", new="OutraSenha#1")
        self.assertEqual(r["status"], 200)
        self.assertEqual(self.call("me", token=tok2)["status"], 401)
        self.assertEqual(self.call("me", token=r["body"]["token"])["status"], 200)


class TestAtaques(Base):
    def test_sem_token_nao_le_nem_grava(self):
        self.make_student()
        self.assertEqual(self.call("get_data")["status"], 401)
        self.assertEqual(self.call("save_data", user_id="ana@exemplo.com", progress={})["status"], 401)

    def test_get_nao_devolve_dados(self):
        self.make_student()
        res = L.lambda_handler({"requestContext": {"http": {"method": "GET"}},
                                "queryStringParameters": {"user_id": "ana@exemplo.com"}}, None)
        self.assertNotIn("ana", res["body"])

    def test_nao_grava_na_conta_de_outro(self):
        ana = self.make_student()
        self.make_student("bia@exemplo.com", "SenhaBia#123", "Bia")
        self.call("save_data", token=ana, user_id="bia@exemplo.com", progress={"ia-9": {"s": "e"}})
        self.assertNotIn("progress", self.store.items.get("data#bia@exemplo.com", {}))

    def test_token_adulterado(self):
        tok = self.make_student()
        body, sig = tok.split(".")
        data = json.loads(base64.urlsafe_b64decode(body + "=="))
        data["sub"] = self.ADMIN[0]
        data["role"] = "admin"
        data["aud"] = "admin"
        fake = base64.urlsafe_b64encode(json.dumps(data).encode()).rstrip(b"=").decode() + "." + sig
        self.assertEqual(self.call("admin_list_users", token=fake)["status"], 401)
        self.assertEqual(self.call("me", token=fake)["status"], 401)

    def test_token_expirado(self):
        tok = self.make_student()
        self.clock += 13 * 3600
        self.assertEqual(self.call("me", token=tok)["status"], 401)

    def test_aluno_nao_usa_painel_admin(self):
        tok = self.make_student()
        self.assertEqual(self.call("admin_list_users", token=tok)["status"], 401)
        self.assertEqual(self.call("login", email="ana@exemplo.com", password="SenhaAna#123", aud="admin")["status"], 401)

    def test_admin_nao_entra_nas_trilhas_e_token_admin_nao_serve_no_app(self):
        self.assertEqual(self.call("login", email=self.ADMIN[0], password=self.ADMIN[1])["status"], 401)
        self.assertEqual(self.call("get_data", token=self.admin)["status"], 401)

    def test_bloqueio_por_tentativas(self):
        self.make_student()
        for _ in range(5):
            self.assertEqual(self.call("login", email="ana@exemplo.com", password="errada123")["status"], 401)
        self.assertEqual(self.call("login", email="ana@exemplo.com", password="SenhaAna#123")["status"], 429)
        self.clock += 16 * 60
        self.assertEqual(self.call("login", email="ana@exemplo.com", password="SenhaAna#123")["status"], 200)

    def test_erro_igual_para_email_inexistente(self):
        self.make_student()
        a = self.call("login", email="ninguem@exemplo.com", password="qualquer1")
        b = self.call("login", email="ana@exemplo.com", password="qualquer1")
        self.assertEqual((a["status"], a["body"]["error"]), (b["status"], b["body"]["error"]))
        r = self.call("request_reset", email="ninguem@exemplo.com")
        self.assertEqual(r["status"], 200)
        self.assertNotIn("acct#ninguem@exemplo.com", self.store.items)

    def test_senhas_antigas_nao_funcionam(self):
        self.make_student()
        for pwd in ("1234", "admin"):
            self.assertEqual(self.call("login", email="ana@exemplo.com", password=pwd)["status"], 401)
        self.assertEqual(self.call("login", email="novo@exemplo.com", password="qualquercoisa")["status"], 401)

    def test_codigo_limite_de_tentativas(self):
        self.make_student()
        self.clock += 120
        self.call("request_reset", email="ana@exemplo.com")
        code = self.last_code("ana@exemplo.com")
        wrong = "000000" if code != "000000" else "111111"
        for _ in range(5):
            self.call("confirm_reset", email="ana@exemplo.com", code=wrong, password="NovaSenha#99")
        r = self.call("confirm_reset", email="ana@exemplo.com", code=code, password="NovaSenha#99")
        self.assertEqual(r["status"], 400)

    def test_convite_nao_reutilizavel_e_expira(self):
        self.call("admin_invite", token=self.admin, email="c@exemplo.com", name="C")
        code = self.last_code("c@exemplo.com")
        self.clock += 8 * 24 * 3600
        self.assertEqual(self.call("accept_invite", email="c@exemplo.com", code=code, password="SenhaC#1234")["status"], 400)

    def test_bloquear_derruba_sessao(self):
        tok = self.make_student()
        r = self.call("admin_set_status", token=self.admin, email="ana@exemplo.com", status="blocked")
        self.assertEqual(r["status"], 200)
        self.assertEqual(self.call("me", token=tok)["status"], 401)
        r = self.call("login", email="ana@exemplo.com", password="SenhaAna#123")
        self.assertEqual(r["status"], 403)
        self.call("admin_set_status", token=self.admin, email="ana@exemplo.com", status="active")
        self.assertEqual(self.call("login", email="ana@exemplo.com", password="SenhaAna#123")["status"], 200)

    def test_bootstrap_nao_cria_segundo_admin(self):
        r = self.call("bootstrap_admin", secret="b" * 20, email="outro@exemplo.com", password="SenhaOutro#1")
        self.assertEqual(r["status"], 409)
        r = self.call("bootstrap_admin", secret="errado", email=self.ADMIN[0], password="NovaAdmin#12")
        self.assertEqual(r["status"], 403)

    def test_bootstrap_recupera_senha_do_admin(self):
        r = self.call("bootstrap_admin", secret="b" * 20, email=self.ADMIN[0], password="NovaAdmin#12")
        self.assertEqual(r["status"], 200)
        self.assertEqual(self.call("admin_list_users", token=self.admin)["status"], 401)
        self.assertEqual(self.call("login", email=self.ADMIN[0], password="NovaAdmin#12", aud="admin")["status"], 200)

    def test_sem_token_secret_falha_fechado(self):
        old = os.environ.pop("TOKEN_SECRET")
        try:
            self.assertEqual(self.call("login", email=self.ADMIN[0], password=self.ADMIN[1], aud="admin")["status"], 503)
        finally:
            os.environ["TOKEN_SECRET"] = old

    def test_respostas_nunca_trazem_hash(self):
        tok = self.make_student()
        for r in (self.call("me", token=tok), self.call("admin_list_users", token=self.admin),
                  self.call("admin_get_user", token=self.admin, email="ana@exemplo.com")):
            text = json.dumps(r["body"])
            self.assertNotIn("pwd", text)
            self.assertNotIn("code_hash", text)


class TestAdmin(Base):
    def test_lista_e_resumo(self):
        tok = self.make_student()
        self.call("save_data", token=tok, progress={"ia-0-0-0": {"s": "e"}, "ia-0-0-1": {"s": "r"}, "mat-0-0-0": {"s": "e"}})
        users = self.call("admin_list_users", token=self.admin)["body"]["users"]
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["progress_summary"]["ia"], {"done": 1, "started": 1})
        self.assertEqual(users[0]["progress_summary"]["mat"]["done"], 1)

    def test_editar_progresso_e_auditoria(self):
        tok = self.make_student()
        self.call("save_data", token=tok, progress={"ia-0-0-0": {"s": "e"}, "mat-0-0-0": {"s": "e"}})
        r = self.call("admin_edit_progress", token=self.admin, email="ana@exemplo.com", op="reset_trail", trail="ia")
        self.assertEqual(r["body"]["progress_summary"]["ia"]["done"], 0)
        r = self.call("admin_edit_progress", token=self.admin, email="ana@exemplo.com", op="set_topics",
                      changes={"ing-0-0-0": "e"})
        self.assertEqual(r["body"]["progress_summary"]["ing"]["done"], 1)
        bad = self.call("admin_edit_progress", token=self.admin, email="ana@exemplo.com", op="set_topics",
                        changes={"pwd": "e"})
        self.assertEqual(bad["status"], 400)
        actions = [e["action"] for e in self.call("admin_audit", token=self.admin)["body"]["entries"]]
        self.assertEqual(actions.count("edit_progress"), 2)

    def test_excluir_exige_confirmacao(self):
        self.make_student()
        self.assertEqual(self.call("admin_delete_user", token=self.admin, email="ana@exemplo.com")["status"], 400)
        r = self.call("admin_delete_user", token=self.admin, email="ana@exemplo.com", confirm="ana@exemplo.com")
        self.assertEqual(r["status"], 200)
        self.assertNotIn("acct#ana@exemplo.com", self.store.items)

    def test_admin_nao_mexe_em_admin(self):
        for action in ("admin_set_status", "admin_delete_user", "admin_force_reset"):
            r = self.call(action, token=self.admin, email=self.ADMIN[0], status="blocked", confirm=self.ADMIN[0])
            self.assertEqual(r["status"], 404, action)

    def test_forcar_troca_de_senha(self):
        tok = self.make_student()
        r = self.call("admin_force_reset", token=self.admin, email="ana@exemplo.com")
        self.assertEqual(r["status"], 200)
        self.assertEqual(self.call("me", token=tok)["status"], 401)
        self.assertEqual(self.call("login", email="ana@exemplo.com", password="SenhaAna#123")["status"], 401)
        r = self.call("confirm_reset", email="ana@exemplo.com", code=self.last_code("ana@exemplo.com"), password="Nova#Senha1")
        self.assertEqual(r["status"], 200)

    def test_convite_duplicado(self):
        self.make_student()
        r = self.call("admin_invite", token=self.admin, email="ANA@exemplo.com", name="Ana 2")
        self.assertEqual(r["status"], 409)


if __name__ == "__main__":
    unittest.main()
