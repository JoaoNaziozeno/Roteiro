# -*- coding: utf-8 -*-
"""
Confere as Aulas Visuais de IA e Inglês antes de publicar.

    python -X utf8 validate_lessons.py            -> estrutura + exercícios de código
    python -X utf8 validate_lessons.py --links    -> também testa os links de livros e documentação
    python -X utf8 validate_lessons.py ia_f1a     -> só as aulas de um arquivo

O que é verificado:
  - cobertura: quais tópicos de IA e aulas de Inglês ainda não têm Aula Visual;
  - estrutura de cada bloco (alternativa correta dentro do intervalo, um "porquê" por alternativa etc.);
  - HTML básico (tags abertas e fechadas) e cifrões soltos, que o KaTeX leria como fórmula;
  - exercícios de código: a solução oficial passa em todos os testes e o código inicial NÃO passa.
    Exercícios com numpy/pandas não rodam aqui (são conferidos no navegador, com o Pyodide).
"""
import importlib
import json
import os
import re
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

RUNNER = r'''
import sys, json, io, contextlib
spec = json.load(open(sys.argv[1], encoding="utf-8"))
if spec.get("libs"): sys.path.insert(0, spec["libs"])
fila = list(spec.get("stdin") or [])
def _input(prompt=""):
    if not fila: raise EOFError("input() sem entrada")
    v = str(fila.pop(0)); print(str(prompt) + v); return v
ns = {"input": _input, "__name__": "__main__"}
buf = io.StringIO()
res = {"err": None, "tests": []}
try:
    with contextlib.redirect_stdout(buf):
        exec(compile(spec["code"], "<exec>", "exec"), ns)
except BaseException as e:
    res["err"] = type(e).__name__ + ": " + str(e)
if not res["err"]:
    for t in spec["tests"]:
        ns["saida"] = buf.getvalue()
        try:
            exec(t["codigo"], ns); res["tests"].append([t["nome"], True, ""])
        except BaseException as e:
            res["tests"].append([t["nome"], False, type(e).__name__ + ": " + str(e)])
print("@@" + json.dumps(res))
'''
# Bibliotecas pesadas (numpy, pandas): defina LV_PYLIBS com uma pasta onde elas estejam instaladas
# (pip install --target PASTA numpy pandas) para conferir também esses exercícios.
LIBS = os.environ.get("LV_PYLIBS", "")
HEAVY = re.compile(r"^\s*(import|from)\s+(numpy|pandas|scipy|matplotlib|sklearn|sympy)\b", re.M)


def run_code(code, tests, stdin):
    with tempfile.TemporaryDirectory() as d:
        sp, rp = os.path.join(d, "s.json"), os.path.join(d, "r.py")
        json.dump({"code": code, "tests": tests, "stdin": stdin, "libs": LIBS}, open(sp, "w", encoding="utf-8"))
        open(rp, "w", encoding="utf-8").write(RUNNER)
        try:
            p = subprocess.run([sys.executable, "-I", "-X", "utf8", rp, sp], capture_output=True, text=True, encoding="utf-8", timeout=60 if LIBS else 6, cwd=d)
        except subprocess.TimeoutExpired:
            return {"timeout": True}
        m = re.search(r"@@(\{.*\})\s*$", p.stdout, re.S)
        return json.loads(m.group(1)) if m else {"err": "runner: " + (p.stderr or p.stdout)[-200:]}


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ("codigo", "inicial", "solucao", "testes", "url", "linhas", "entradas"):
                yield from strings(v)
    elif isinstance(o, (list, tuple)):
        for v in o:
            yield from strings(v)


def check_html(s):
    probs = []
    for tag in ("b", "i", "code", "pre", "p", "ul", "ol", "li"):
        a, b = len(re.findall(rf"<{tag}(\s[^>]*)?>", s)), s.count(f"</{tag}>")
        if a != b:
            probs.append(f"<{tag}> {a} abre / {b} fecha")
    plain = re.sub(r"<pre.*?</pre>|<code>.*?</code>", "", s, flags=re.S)
    if plain.count("$") % 2:
        probs.append("cifrão solto ($)")
    return probs


def check_guide(key, g, problems, code_jobs):
    def bad(msg):
        problems.append(f"[{key}] {msg}")
    for f in ("gancho", "objetivos", "blocos", "resumo"):
        if not g.get(f):
            bad(f"falta {f}")
    tipos = [b.get("tipo") for b in g.get("blocos", [])]
    if "quiz" not in tipos:
        bad("sem quiz")
    for i, b in enumerate(g.get("blocos", []), 1):
        t = b.get("tipo")
        where = f"bloco {i} ({t})"
        if t == "palpite":
            n = len(b.get("opcoes", []))
            if not 0 <= b.get("correta", -1) < n:
                bad(f"{where}: correta fora do intervalo")
            if b.get("porques") and len(b["porques"]) != n:
                bad(f"{where}: {len(b['porques'])} porquês para {n} opções")
        elif t == "quiz":
            for q in b.get("perguntas", []):
                if not 0 <= q.get("correta", -1) < len(q.get("opcoes", [])):
                    bad(f"{where}: correta fora do intervalo em “{q.get('pergunta', '')[:40]}”")
            if len(b.get("perguntas", [])) < 3:
                bad(f"{where}: menos de 3 perguntas")
        elif t == "codigo":
            if not b.get("testes") or not b.get("solucao"):
                bad(f"{where}: sem testes ou sem solução")
            else:
                code_jobs.append((key, b))
            if re.search(r"^saida\s*=", b.get("solucao", "") + "\n" + b.get("inicial", ""), re.M):
                bad(f"{where}: o código usa a variável 'saida', reservada para a saída do programa nos testes")
        elif t == "parsons":
            if len(b.get("linhas", [])) < 3:
                bad(f"{where}: menos de 3 linhas")
            if len(set(b["linhas"])) != len(b["linhas"]):
                bad(f"{where}: linhas repetidas")
        elif t == "ouvir":
            for it in b.get("itens", []):
                if "opcoes" in it and not 0 <= it.get("correta", -1) < len(it["opcoes"]):
                    bad(f"{where}: correta fora do intervalo em “{it['frase']}”")
        elif t in ("dialogo", "vocab", "falar"):
            if not (b.get("falas") or b.get("cartoes") or b.get("frases")):
                bad(f"{where}: vazio")
    for s in strings(g):
        for p in check_html(s):
            bad(f"{p} em “{s[:50]}”")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    only = None
    if args:
        only = set(importlib.import_module(args[0]).AULAS)
    from lessons_all import ia_guides, en_guides
    from build_ia_data import get_enriched_ia_phases
    ia, en = ia_guides(), en_guides()
    titles = [t["title"] for p in get_enriched_ia_phases() for g in p["g"] for t in g[1]]
    vids = [e["videoId"] for e in json.load(open(os.path.join(BASE, "english_playlist.json"), encoding="utf-8"))]
    miss_ia, miss_en = [t for t in titles if t not in ia], [v for v in vids if v not in en]
    extra = [k for k in ia if k not in titles] + [k for k in en if k not in vids]
    print(f"IA: {len(titles) - len(miss_ia)}/{len(titles)} aulas · Inglês: {len(vids) - len(miss_en)}/{len(vids)} aulas")
    if extra:
        print("  CHAVES QUE NÃO CASAM COM NENHUM TÓPICO:", extra)
    if "--faltam" in sys.argv:
        for t in miss_ia:
            print("   falta IA:", t)
        for v in miss_en:
            print("   falta EN:", v)

    problems, code_jobs = [], []
    for key, g in list(ia.items()) + list(en.items()):
        if only is None or key in only:
            check_guide(key, g, problems, code_jobs)

    ran = skipped = 0
    for key, b in code_jobs:
        if HEAVY.search(b["solucao"]) and not LIBS:
            skipped += 1
            continue
        ran += 1
        r = run_code(b["solucao"], b["testes"], b.get("entradas"))
        if r.get("timeout") or r.get("err"):
            problems.append(f"[{key}] código “{b.get('titulo')}”: solução falha: {r.get('err') or 'tempo esgotado'}")
        else:
            for nome, ok, msg in r["tests"]:
                if not ok:
                    problems.append(f"[{key}] código “{b.get('titulo')}”: solução não passa em “{nome}”: {msg}")
        r0 = run_code(b["inicial"], b["testes"], b.get("entradas"))
        if not (r0.get("timeout") or r0.get("err")) and all(ok for _, ok, _ in r0["tests"]):
            problems.append(f"[{key}] código “{b.get('titulo')}”: o código inicial já passa em todos os testes")
    print(f"Exercícios de código: {ran} conferidos aqui, {skipped} com numpy/pandas (conferir no navegador)")

    if "--links" in sys.argv:
        import concurrent.futures as cf
        import urllib.request
        urls = {}
        for key, g in list(ia.items()) + list(en.items()):
            for b in g.get("blocos", []):
                if b.get("tipo") == "camadas":
                    for it in b.get("ponte", []) + b.get("profundidade", []) + b.get("revisao", []):
                        if "youtube.com" not in it["url"] and "youglish.com" not in it["url"]:
                            urls.setdefault(it["url"], key)

        def chk(u):
            try:
                req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
                return u, urllib.request.urlopen(req, timeout=25).status
            except Exception as e:
                return u, str(e)[:60]
        with cf.ThreadPoolExecutor(10) as ex:
            res = list(ex.map(chk, urls))
        badl = [(u, s) for u, s in res if s != 200]
        print(f"Links: {len(res) - len(badl)}/{len(res)} ok")
        for u, s in badl:
            print(f"   {s} | {u} | ex.: {urls[u]}")

    print(f"\n{len(problems)} problema(s)")
    for p in problems:
        print("  -", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
