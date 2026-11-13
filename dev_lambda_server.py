# -*- coding: utf-8 -*-
"""
Servidor local para testar o login sem AWS: roda aws_lambda_dynamodb.py com um banco em memória.

    python -X utf8 dev_lambda_server.py          (porta 8787)

- Na primeira execução cria contas de teste (admin e dois alunos) com senhas aleatórias
  e grava em dev_accounts.json (fora do git).
- E-mails (convites e códigos) não são enviados: vão para dev_outbox.log (fora do git).
- No site rodando em localhost, aponte a sincronização para http://localhost:8787/
  (menu da conta → Sincronização na nuvem → Endereço do servidor).
Nada aqui é usado em produção.
"""

import json
import os
import secrets
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("TOKEN_SECRET", secrets.token_hex(32))
os.environ.setdefault("BOOTSTRAP_SECRET", secrets.token_hex(16))
os.environ.setdefault("PBKDF2_ITER", "50000")
os.environ.setdefault("APP_URL", "http://localhost:8000/index.html")

import aws_lambda_dynamodb as L  # noqa: E402
from test_lambda_auth import MemStore  # noqa: E402

PORT = int(os.environ.get("DEV_LAMBDA_PORT") or 8787)
ACCOUNTS_FILE = os.path.join(HERE, "dev_accounts.json")
OUTBOX_FILE = os.path.join(HERE, "dev_outbox.log")


def fake_email(to, subject, text, html):
    with open(OUTBOX_FILE, "a", encoding="utf-8") as f:
        f.write(f"--- {time.strftime('%H:%M:%S')} para {to}: {subject}\n{text}\n\n")
    print(f"[e-mail] {to}: {subject}")


def call(action, **payload):
    payload["action"] = action
    res = L.lambda_handler({"requestContext": {"http": {"method": "POST"}}, "body": json.dumps(payload)}, None)
    body = json.loads(res["body"])
    if res["statusCode"] != 200:
        raise RuntimeError(f"{action}: {body}")
    return body


def last_code(email):
    text = open(OUTBOX_FILE, encoding="utf-8").read()
    block = text.rsplit(f"para {email}:", 1)[1]
    return block.split("Código: ")[1][:6]


def seed():
    accounts = {
        "admin": {"email": "admin@roteiro.test", "name": "Admin de Teste", "password": secrets.token_urlsafe(12)},
        "students": [
            {"email": "ana@roteiro.test", "name": "Ana Teste", "password": secrets.token_urlsafe(12)},
            {"email": "bruno@roteiro.test", "name": "Bruno Teste", "password": secrets.token_urlsafe(12)},
        ],
    }
    if os.path.exists(ACCOUNTS_FILE):
        accounts = json.load(open(ACCOUNTS_FILE, encoding="utf-8"))
    else:
        json.dump(accounts, open(ACCOUNTS_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    a = accounts["admin"]
    call("bootstrap_admin", secret=os.environ["BOOTSTRAP_SECRET"], **a)
    admin = call("login", email=a["email"], password=a["password"], aud="admin")["token"]
    for s in accounts["students"]:
        call("admin_invite", token=admin, email=s["email"], name=s["name"])
        call("accept_invite", email=s["email"], code=last_code(s["email"]), password=s["password"])
    print(f"Contas de teste prontas (senhas em {os.path.basename(ACCOUNTS_FILE)}).")


class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        origin = self.headers.get("Origin") or ""
        if origin.startswith("http://localhost:") or origin.startswith("http://127.0.0.1:") or origin == "null":
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "content-type, authorization")

    def _run(self, method):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length).decode("utf-8") if length else ""
        event = {"requestContext": {"http": {"method": method}}, "body": body,
                 "headers": {k.lower(): v for k, v in self.headers.items()}}
        res = L.lambda_handler(event, None)
        data = res["body"].encode("utf-8")
        self.send_response(res["statusCode"])
        self._cors()
        for k, v in res["headers"].items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self._run("OPTIONS")

    def do_GET(self):
        self._run("GET")

    def do_POST(self):
        self._run("POST")

    def log_message(self, fmt, *args):
        sys.stdout.write("[lambda] " + (fmt % args) + "\n")


if __name__ == "__main__":
    L.STORE = MemStore()
    L.SEND_EMAIL = fake_email
    open(OUTBOX_FILE, "w", encoding="utf-8").close()
    seed()
    print(f"Lambda local em http://localhost:{PORT}/")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
