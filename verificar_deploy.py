# -*- coding: utf-8 -*-
"""
Confere se a Lambda (e, com --site, o GitHub Pages) está pronta para o login multiusuário.

    python verificar_deploy.py           só a Lambda
    python verificar_deploy.py --site    Lambda + site publicado

Não usa nenhuma senha nem cria nada: só faz pedidos que devem ser recusados.
"""

import json
import sys
import urllib.error
import urllib.request

LAMBDA_URL = "https://x37p5anc5yesrwweqfbwxcexsu0dpzdu.lambda-url.us-east-2.on.aws/"
SITE_URL = "https://joaonaziozeno.github.io/Roteiro/"
SITE_ORIGIN = "https://joaonaziozeno.github.io"
UA = {"User-Agent": "roteiro-verificar-deploy"}

results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(("  OK   " if ok else "  FALHA") + f"  {name}" + (f"  ({detail})" if detail and not ok else ""))


def request(method, url, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    h = dict(UA, **(headers or {}))
    if data is not None:
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, dict(r.headers), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode("utf-8", "replace")


def as_json(text):
    try:
        return json.loads(text)
    except Exception:
        return {}


def lower_headers(h):
    return {k.lower(): v for k, v in h.items()}


def main():
    global LAMBDA_URL
    if "--url" in sys.argv:
        LAMBDA_URL = sys.argv[sys.argv.index("--url") + 1]
    print("Lambda:", LAMBDA_URL)
    st, _, body = request("GET", LAMBDA_URL)
    j = as_json(body)
    is_new = j.get("service") == "roteiro-auth" and j.get("version") == 2
    check("versão nova no ar (service roteiro-auth v2)", is_new, body[:120])
    if not is_new:
        # A Lambda antiga grava qualquer POST na tabela: não envia os testes abaixo.
        print()
        print("A Lambda ainda está na versão antiga. Publique o código (passo 6 do guia) e rode de novo.")
        sys.exit(1)
    check("GET não devolve dados de usuário", "progress" not in body and "pwd" not in body)

    st, _, body = request("POST", LAMBDA_URL, {"action": "get_data"})
    check("ler dados sem login é recusado (401)", st == 401, f"HTTP {st}")

    st, _, body = request("POST", LAMBDA_URL, {"action": "save_data", "user_id": "x@x.com", "progress": {}})
    check("gravar sem login é recusado (401)", st == 401, f"HTTP {st}")

    st, _, body = request("POST", LAMBDA_URL, {"action": "login", "email": "naoexiste@exemplo.com", "password": "1234"})
    check("login com senha antiga '1234' é recusado (401)", st == 401, f"HTTP {st} {body[:120]}")
    check("Lambda tem TOKEN_SECRET configurado", st != 503, as_json(body).get("error", ""))

    st, h, _ = request("OPTIONS", LAMBDA_URL, headers={"Origin": SITE_ORIGIN, "Access-Control-Request-Method": "POST",
                                                      "Access-Control-Request-Headers": "content-type"})
    h = lower_headers(h)
    allow = h.get("access-control-allow-origin", "")
    check("CORS libera o site", allow in (SITE_ORIGIN, "*"), f"Allow-Origin={allow!r}")
    st, h, _ = request("OPTIONS", LAMBDA_URL, headers={"Origin": "https://site-estranho.example",
                                                      "Access-Control-Request-Method": "POST"})
    allow = lower_headers(h).get("access-control-allow-origin", "")
    check("CORS não libera outros sites", allow not in ("*", "https://site-estranho.example"),
          f"Allow-Origin={allow!r} (restrinja no passo 5 do guia)")

    if "--site" in sys.argv:
        print("Site:", SITE_URL)
        st, _, body = request("GET", SITE_URL + "index.html")
        check("index.html publicado com o login novo", st == 200 and "claimLocalDataFor" in body and "computeSha256" not in body,
              f"HTTP {st}")
        st, _, body = request("GET", SITE_URL + "admin.html")
        check("admin.html publicado", st == 200 and "Painel do administrador" in body, f"HTTP {st}")

    print()
    if all(results):
        print("Tudo certo.")
    else:
        print(f"{results.count(False)} item(ns) com falha. Veja docs/DEPLOY_LOGIN.md.")
        sys.exit(1)


if __name__ == "__main__":
    main()
