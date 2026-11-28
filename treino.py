# -*- coding: utf-8 -*-
"""
Treino: junta os bancos de questões, liga cada aula ao seu id e grava treino_<trilha>.json (baixado pela página
só quando você começa um treino). Também confere as questões de código rodando o Python de verdade.

    python -X utf8 treino.py          -> confere todas as questões e mostra quantas há por aula

Formato das questões: ver treino_js.py. Bancos (título da aula -> lista de questões):
    IA, Fase 1 ("Base da linguagem" e "Estruturas de dados")   treino_ia_f1.py
    Matemática, Módulo 1 do site (Fundamentos)                 treino_mat_fund.py
    Matemática, Álgebra Linear (Módulo 2 do site)              treino_mat_m1.py
    Matemática, Cálculo (Módulo 3)                             treino_mat_calc.py
    Matemática, Probabilidade, Estatística e Informação (4)    treino_mat_prob.py
    Matemática, Transformers (Módulo 5)                        treino_mat_transf.py
Geradores de conta: treino_contas.py (Álgebra Linear e ferramentas), treino_contas_calc.py (Fundamentos e Cálculo),
treino_contas_prob.py (Probabilidade, Estatística e Informação) e treino_contas_transf.py (Transformers).
"""
import contextlib
import importlib
import io
import json
import os
import sys
import warnings

BASE = os.path.dirname(os.path.abspath(__file__))
BANCOS = {"ia": ["treino_ia_f1"],
          "mat": ["treino_mat_fund", "treino_mat_m1", "treino_mat_calc", "treino_mat_prob", "treino_mat_transf"]}
# Geradores de conta: cada arquivo registra os seus em TR.GEN (o 1º também define as ferramentas TR.H)
GERADORES = ["treino_contas", "treino_contas_calc", "treino_contas_prob", "treino_contas_transf"]
TIPOS = ("saida", "lacuna", "erro", "conceito", "conta")

INDEX = {}   # id da aula -> nº de questões (preenchido por montar(); vai para as páginas como TR_INDEX)
MODS = []    # fases/módulos com treino, para o treino misto da página Revisões (TR_MODS)


def carregar():
    """{trilha: {título da aula: [questões]}}"""
    out = {}
    for tr, mods in BANCOS.items():
        out[tr] = {}
        for nome in mods:
            for titulo, qs in importlib.import_module(nome).TREINO.items():
                out[tr].setdefault(titulo, []).extend(qs)
    return out


def montar(tracks):
    """tracks = {"ia": phases, "mat": ..., "ing": ...}, já com o currículo aplicado (ids fixos).
    Preenche INDEX e MODS e devolve ({trilha: {id: [questões]}}, [(trilha, título) sem aula correspondente])."""
    import curriculo
    bancos = carregar()
    por_id, achados = {tr: {} for tr in bancos}, set()
    INDEX.clear()
    MODS.clear()
    for tr, phases in tracks.items():
        banco = bancos.get(tr) or {}
        for p_idx, p in enumerate(phases):
            ids = []
            for g_idx, g in enumerate(p["g"]):
                for t_idx, raw in enumerate(g[1]):
                    titulo = raw.get("title", "") if isinstance(raw, dict) else str(raw).split("||")[0]
                    if titulo in banco:
                        tid = curriculo.topic_id(raw, tr, p_idx, g_idx, t_idx)
                        por_id[tr][tid] = banco[titulo]
                        INDEX[tid] = len(banco[titulo])
                        ids.append(tid)
                        achados.add((tr, titulo))
            if ids:
                MODS.append({"k": f"{tr}-{p_idx}", "tr": tr, "nome": p["t"], "ids": ids})
    soltos = [(tr, t) for tr, b in bancos.items() for t in b if (tr, t) not in achados]
    return por_id, soltos


def gravar(por_id, pasta):
    """Grava treino_<trilha>.json; devolve [(caminho, nome publicado)]."""
    saidas = []
    for tr, banco in por_id.items():
        if not banco:
            continue
        nome = f"treino_{tr}.json"
        caminho = os.path.join(pasta, nome)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(banco, f, ensure_ascii=False, separators=(",", ":"))
        saidas.append((caminho, nome))
    return saidas


def _js(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def ui_js():
    """O script do Treino com o índice desta build (precisa de montar() antes)."""
    from treino_js import TR_JS, TR_UI_JS
    return TR_JS + "\n" + gen_js() + "\n" + TR_UI_JS.replace("__TR_INDEX__", _js(INDEX)).replace("__TR_MODS__", _js(MODS))


def gen_js():
    """Todos os geradores de conta, na ordem de GERADORES (o 1º define as ferramentas TR.H)."""
    return "\n".join(importlib.import_module(m).TR_GEN_JS for m in GERADORES)


def contar(tid):
    return INDEX.get(tid, 0)


# ---------------------------------------------------------------- conferência das questões de código
class _Limite(Exception):
    pass


def rodar(codigo, entradas=None, max_linhas=200_000):
    """Roda um trecho de Python e devolve (o que aparece na tela, nome do erro ou None).
    input() lê de 'entradas' e, como num terminal, a tela mostra a pergunta e o que foi digitado.
    Laço infinito vira o erro "LacoInfinito" (para depois de max_linhas linhas executadas)."""
    tela = io.StringIO()
    fila = [str(e) for e in (entradas or [])]

    def _input(prompt=""):
        if not fila:
            raise EOFError("input() sem entrada")
        v = fila.pop(0)
        tela.write(str(prompt) + v + "\n")
        return v

    passos = [0]

    def _trace(frame, event, arg):
        if frame.f_code.co_filename != "<treino>":
            return None              # só o trecho da questão conta (o import do NumPy executa milhares de linhas)
        if event == "line":
            passos[0] += 1
            if passos[0] > max_linhas:
                raise _Limite()
        return _trace

    ns = {"__name__": "__main__", "input": _input}
    erro, antigo = None, sys.gettrace()
    try:
        with contextlib.redirect_stdout(tela), warnings.catch_warnings():
            warnings.simplefilter("ignore")      # ex.: o aviso de overflow de np.exp(1000), que faz parte da questão
            sys.settrace(_trace)
            try:
                exec(compile(codigo, "<treino>", "exec"), ns)
            finally:
                sys.settrace(antigo)
    except _Limite:
        erro = "LacoInfinito"
    except BaseException as e:      # noqa: BLE001 (o erro faz parte da resposta)
        erro = type(e).__name__
    return tela.getvalue(), erro


def _norm(s):
    return "\n".join(l.rstrip() for l in str(s).replace("\r\n", "\n").strip("\n").split("\n"))


NADA = "(nada aparece)"   # alternativa para quando o programa não imprime nada


def na_tela(out, erro):
    """O que a pessoa vê: o que foi impresso e, se quebrou, o nome do erro na última linha."""
    t = _norm(out)
    if erro:
        return t + "\n" + erro if t else erro
    return t or NADA


def textos(q):
    """Textos em HTML da questão (para conferir tags e cifrões); código e saídas ficam de fora."""
    campos = ["pergunta", "x", "tema"] + (["opcoes"] if q.get("k") == "conceito" else []) + ["porques"]
    for c in campos:
        v = q.get(c)
        for s in (v if isinstance(v, list) else [v]):
            if isinstance(s, str) and s:
                yield s


def conferir(qs, titulo=""):
    """Problemas de um banco de questões (lista vazia = tudo certo)."""
    from validate_lessons import check_html
    probs = []
    for i, q in enumerate(qs, 1):
        k, onde = q.get("k"), f"[{titulo}] questão {i} ({q.get('k')})"
        bad = probs.append
        if k not in TIPOS:
            bad(f"{onde}: tipo desconhecido")
            continue
        for s in textos(q):
            for p in check_html(s):
                bad(f"{onde}: {p} em {s[:50]!r}")
        if k == "conta":
            if not q.get("g"):
                bad(f"{onde}: sem gerador (g)")
            continue
        if not q.get("x"):
            bad(f"{onde}: sem explicação (x)")
        if k in ("saida", "lacuna", "conceito"):
            ops, c = q.get("opcoes") or [], q.get("correta")
            if len(ops) < 3:
                bad(f"{onde}: menos de 3 alternativas")
            if len(set(map(_norm, ops))) != len(ops):
                bad(f"{onde}: alternativas repetidas")
            if not isinstance(c, int) or not 0 <= c < len(ops):
                bad(f"{onde}: correta fora do intervalo")
                continue
            if q.get("porques") and len(q["porques"]) != len(ops):
                bad(f"{onde}: {len(q['porques'])} porquês para {len(ops)} alternativas")
            if k == "conceito" and not q.get("pergunta"):
                bad(f"{onde}: sem pergunta")
        if k == "saida":
            got = na_tela(*rodar(q["codigo"], q.get("entradas")))
            if _norm(ops[c]) != got:
                bad(f"{onde}: o Python mostra {got!r}, mas a alternativa certa é {ops[c]!r}")
            for j, o in enumerate(ops):
                if j != c and _norm(o) == got:
                    bad(f"{onde}: a alternativa {o!r} também está certa")
        elif k == "lacuna":
            if q.get("codigo", "").count("____") != 1 or not q.get("pergunta") or q.get("saida") is None:
                bad(f"{onde}: precisa de pergunta, saída e exatamente uma lacuna ____")
                continue
            alvo = _norm(q["saida"])
            for j, o in enumerate(ops):
                out, err = rodar(q["codigo"].replace("____", o), q.get("entradas"))
                ok = err is None and _norm(out) == alvo
                if j == c and not ok:
                    bad(f"{onde}: com a certa ({o!r}) o programa mostra {na_tela(out, err)!r}, e não {alvo!r}")
                if j != c and ok:
                    bad(f"{onde}: a alternativa {o!r} também funciona")
        elif k == "erro":
            linhas, L, fix = q.get("codigo", "").split("\n"), q.get("linha"), q.get("correcao", "")
            if not (isinstance(L, int) and 1 <= L <= len(linhas)) or not linhas[L - 1].strip():
                bad(f"{onde}: linha do erro inválida")
                continue
            ind = lambda s: len(s) - len(s.lstrip())
            if q.get("indentacao"):      # o erro é a própria indentação
                if fix.strip() != linhas[L - 1].strip() or ind(fix) == ind(linhas[L - 1]):
                    bad(f"{onde}: erro de indentação: a correção deve mudar só o recuo")
            elif fix.strip() == linhas[L - 1].strip() or ind(fix) != ind(linhas[L - 1]):
                bad(f"{onde}: a correção precisa mudar a linha e manter a indentação")
            out, err = rodar("\n".join(linhas[:L - 1] + [fix] + linhas[L:]), q.get("entradas"))
            esperado = None if q.get("saida") is None else _norm(q["saida"])
            if err:
                bad(f"{onde}: o programa corrigido dá {err}")
            elif esperado is not None and _norm(out) != esperado:
                bad(f"{onde}: o corrigido mostra {_norm(out)!r}, e não {esperado!r}")
            out0, err0 = rodar(q["codigo"], q.get("entradas"))
            if err0 is None and (esperado is None or _norm(out0) == esperado):
                bad(f"{onde}: o código com erro funciona igual ao corrigido")
    return probs


def main():
    from build_ia_data import get_enriched_ia_phases
    from build_math_data import get_enriched_mat_phases
    import curriculo
    tracks = {"ia": get_enriched_ia_phases(), "mat": get_enriched_mat_phases()}
    curriculo.apply(tracks)
    por_id, soltos = montar(tracks)
    probs = [f"título sem aula: {tr} · {t}" for tr, t in soltos]
    bancos = carregar()
    for tr, banco in bancos.items():
        for titulo, qs in banco.items():
            probs += conferir(qs, titulo)
    for tr, banco in bancos.items():
        print(f"{tr}: {len(banco)} aulas, {sum(len(q) for q in banco.values())} questões")
        for titulo, qs in banco.items():
            tipos = {}
            for q in qs:
                tipos[q["k"]] = tipos.get(q["k"], 0) + 1
            print(f"   {len(qs):>2}  {titulo[:60]:<60} " + " ".join(f"{k}={v}" for k, v in sorted(tipos.items())))
    print(f"\n{len(probs)} problema(s)")
    for p in probs:
        print("  -", p)
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
