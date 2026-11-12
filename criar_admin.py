# -*- coding: utf-8 -*-
"""
Cria a conta de administrador do Roteiro (ou redefine a senha dela).

Uso, no seu terminal:
    python criar_admin.py

O script pede a URL da Lambda, o BOOTSTRAP_SECRET (o mesmo configurado na Lambda),
o e-mail, o nome e a senha do admin. A senha é digitada sem aparecer na tela e vai
direto para a Lambda por HTTPS; ela não é gravada em nenhum arquivo.
Depois de criar o admin, apague a variável BOOTSTRAP_SECRET da Lambda.
"""

import getpass
import json
import urllib.error
import urllib.request

DEFAULT_URL = "https://x37p5anc5yesrwweqfbwxcexsu0dpzdu.lambda-url.us-east-2.on.aws/"


def main():
    url = input(f"URL da Lambda [{DEFAULT_URL}]: ").strip() or DEFAULT_URL
    secret = getpass.getpass("BOOTSTRAP_SECRET: ").strip()
    email = input("E-mail do admin (diferente do seu e-mail de aluno): ").strip()
    name = input("Nome do admin [Administrador]: ").strip() or "Administrador"
    pwd = getpass.getpass("Senha do admin (mínimo 8 caracteres): ")
    if pwd != getpass.getpass("Repita a senha: "):
        print("As senhas não conferem.")
        return
    body = json.dumps({"action": "bootstrap_admin", "secret": secret, "email": email,
                       "name": name, "password": pwd}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(json.loads(resp.read()).get("message"))
    except urllib.error.HTTPError as err:
        print("Erro:", json.loads(err.read() or b"{}").get("error", err.reason))


if __name__ == "__main__":
    main()
