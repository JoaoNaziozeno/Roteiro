# -*- coding: utf-8 -*-
"""
Fábrica de Aulas Visuais: funções curtas que montam os blocos do formato v2
(lesson_v2_assets.py + lesson_blocks_v3.py). Os arquivos de conteúdo (ia_f*.py, en_m*.py)
só chamam estas funções, o que mantém cada aula enxuta e com a mesma estrutura.

Uso típico (IA):
    AULAS["Título exato do tópico"] = aula(35, "gancho", [objetivos], [pré-requisitos], [
        chute("pergunta", ["a", "b", "c"], 1, ["porquê a", "porquê b", "porquê c"], "fecho", cod="print(1)"),
        concreto("Título", "<p>html</p>"), crianca("<p>html</p>"), ver("o que anotar do vídeo"),
        nota("Título", [("símbolo", "leitura", "significado")]),
        passos("Título", [("faça", "por quê")], corpo="...", fim="..."),
        cod("Título", "enunciado", INICIAL, [("teste", "assert ...")], SOLUCAO, ["dica"]),
        ordem("Título", ["linha 1", "linha 2"]), lab("Título", CODIGO, exps=["experimento"]),
        erros([("erro", "correção")]), ponte("Título", "<p>html</p>"),
        quiz([("pergunta", ["a", "b", "c"], 0, "explicação")]),
    ], ["resumo"], "próxima aula", livro=("ATBS", "cap. 2", "pergunta guia"))

Inglês usa também: dialogo, vocab, ouvir, falar, tabela, pense, e yg("frase") para a camada extra.
A camada "Vá mais fundo" é montada sozinha: documentação do tópico (IA) ou YouGlish (Inglês) + livro.
Dentro dos textos, use py("código") para um bloco de código Python com realce e sh("...") para terminal/SQL.
"""
import html as _html

# Livros e cursos gratuitos usados na camada de profundidade (todos conferidos por check_links/validate)
LIVROS = {
    "ATBS": ("Al Sweigart, <i>Automate the Boring Stuff with Python</i> (grátis online)", "https://automatetheboringstuff.com/2e/chapter{n}/"),
    "PYDOC": ("Tutorial oficial do Python (em português)", "https://docs.python.org/pt-br/3/tutorial/{n}.html"),
    "PROGIT": ("Scott Chacon, <i>Pro Git</i> (grátis, em português)", "https://git-scm.com/book/pt-br/v2"),
    "PDA": ("Wes McKinney, <i>Python for Data Analysis</i>, 3ª ed. (grátis online)", "https://wesmckinney.com/book/{n}"),
    "PDSH": ("Jake VanderPlas, <i>Python Data Science Handbook</i> (grátis online)", "https://jakevdp.github.io/PythonDataScienceHandbook/{n}.html"),
    "ISLP": ("James et al., <i>An Introduction to Statistical Learning</i> (PDF gratuito)", "https://www.statlearning.com/"),
    "MLCC": ("Google, <i>Machine Learning Crash Course</i> (grátis)", "https://developers.google.com/machine-learning/crash-course/{n}"),
    "D2L": ("Zhang et al., <i>Dive into Deep Learning</i> (grátis online)", "https://d2l.ai/{n}.html"),
    "NNDL": ("Michael Nielsen, <i>Neural Networks and Deep Learning</i> (grátis online)", "http://neuralnetworksanddeeplearning.com/{n}.html"),
    "UDL": ("Simon Prince, <i>Understanding Deep Learning</i> (PDF gratuito)", "https://udlbook.github.io/udlbook/"),
    "HF": ("Hugging Face, <i>LLM Course</i> (grátis)", "https://huggingface.co/learn/llm-course/{n}"),
    "PROMPT": ("DAIR.AI, <i>Prompt Engineering Guide</i> (em português)", "https://www.promptingguide.ai/pt/{n}"),
    "MISSING": ("MIT, <i>The Missing Semester of Your CS Education</i> (grátis)", "https://missing.csail.mit.edu/2020/{n}/"),
    "MADEML": ("Goku Mohandas, <i>Made With ML</i> (MLOps, grátis)", "https://madewithml.com/"),
    "FASTAPI": ("Documentação do FastAPI (em português)", "https://fastapi.tiangolo.com/pt/{n}/"),
}


def _b(tipo, **kw):
    d = {"tipo": tipo}
    d.update({k: v for k, v in kw.items() if v not in (None, "", [], ())})
    return d


def py(code):
    """Bloco de código Python para usar dentro de textos (ganha realce de sintaxe na página)."""
    return '<pre class="lv2-code" data-lang="py"><code>' + _html.escape(code.strip("\n"), quote=False) + "</code></pre>"


def sh(code):
    """Bloco de terminal, SQL ou outro texto de código (sem realce de Python)."""
    return '<pre class="lv2-code"><code>' + _html.escape(code.strip("\n"), quote=False) + "</code></pre>"


def chute(q, ops, ok, pq, exp="", cod=None, rot=None):
    return _b("palpite", rotulo=rot or ("Preveja a saída" if cod else "Chute antes de ver"), codigo=cod,
              pergunta=q, opcoes=list(ops), correta=ok, porques=list(pq), explicacao=exp)


def concreto(t, corpo): return _b("concreto", titulo=t, corpo=corpo)
def crianca(corpo): return _b("crianca", corpo=corpo)
def texto(t, corpo, rot=None): return _b("texto", titulo=t, corpo=corpo, rotulo=rot)
def ponte(t, corpo): return _b("ponte", titulo=t, corpo=corpo)


def ver(foco, ingles=False):
    """Tarefa para fazer enquanto assiste ao vídeo do tópico (que fica ao lado da aula)."""
    if ingles:
        corpo = ("<ul><li>Repita em voz alta toda vez que o professor disser <i>repeat</i>.</li>"
                 f"<li>Anote 3 frases que ele usar com <b>{foco}</b>.</li>"
                 "<li>Nas práticas, pause e responda antes dele.</li></ul>")
    else:
        corpo = (f"<p>Anote, com as suas palavras, <b>{foco}</b>. Depois compare com a explicação desta aula: "
                 "explicar de novo, do seu jeito, é o que fixa.</p>")
    return _b("texto", rotulo="Enquanto assiste ao vídeo ao lado", corpo=corpo)


def nota(t, itens, corpo=None, rot="Agora sim, a sintaxe"):
    return _b("notacao", rotulo=rot, titulo=t, corpo=corpo,
              itens=[{"simbolo": a, "leitura": b, "significado": c} for a, b, c in itens])


def passos(t, ps, corpo=None, fim=None):
    return _b("passos", rotulo="Resolvido passo a passo", titulo=t, corpo=corpo,
              passos=[{"faca": a, "porque": b} for a, b in ps], conclusao=fim)


def cod(t, q, ini, tests, sol, dicas=(), exp=None, rot=None, entradas=None):
    return _b("codigo", rotulo=rot or "Mão no código", titulo=t, enunciado=q, inicial=ini.lstrip("\n"),
              testes=[{"nome": a, "codigo": b} for a, b in tests], solucao=sol.strip("\n"),
              dicas=list(dicas), explicacao=exp, entradas=list(entradas) if entradas else None)


def ordem(t, linhas, corpo=None, exp=None, frase=False):
    return _b("parsons", titulo=t, corpo=corpo, linhas=list(linhas), explicacao=exp, modo="frase" if frase else None)


def lab(t, codigo, corpo=None, exps=()):
    return _b("laboratorio", titulo=t, corpo=corpo, codigo=codigo.strip("\n"), experimentos=list(exps))


def erros(itens): return _b("armadilhas", itens=[{"erro": a, "correcao": b} for a, b in itens])
def pense(t, q, r, corpo=None, rot=None): return _b("pense", rotulo=rot, titulo=t, corpo=corpo, pergunta=q, resposta=r)
def tabela(t, cab, linhas, rot="Organize na cabeça", corpo=None): return _b("tabela", rotulo=rot, titulo=t, corpo=corpo, cabecalho=list(cab), linhas=[list(l) for l in linhas])
def widget(nome, t, corpo, missoes): return _b("widget", widget=nome, titulo=t, corpo=corpo, missoes=list(missoes))


def pratica(exs, t="Treino em 3 níveis", corpo=None):
    """exs: (nível, enunciado, valor, [dicas], resposta)"""
    return _b("pratica", titulo=t, corpo=corpo,
              exercicios=[{"nivel": n, "enunciado": e, "valor": v, "dicas": list(d), "resposta": r} for n, e, v, d, r in exs])


def quiz(qs):
    return _b("quiz", corpo="<p>3 perguntas. Acertando 2, a camada “Vá mais fundo” é liberada e as revisões são agendadas.</p>",
              perguntas=[{"pergunta": p, "opcoes": list(o), "correta": c, "explicacao": e} for p, o, c, e in qs])


# ---- Inglês
def dialogo(t, falas, corpo=None):
    return _b("dialogo", titulo=t, corpo=corpo or "<p>Ouça a conversa inteira, depois frase por frase (🔊). Tente entender antes de mostrar a tradução.</p>",
              falas=[{"quem": q, "en": e, "pt": p} for q, e, p in falas])


def vocab(cartoes, t="Vocabulário da aula"):
    return _b("vocab", titulo=t, corpo="<p>Clique no cartão para ver a tradução. Marque <b>Já sei</b> ou <b>Rever</b>: fica salvo.</p>",
              cartoes=[{"en": e, "pt": p, "ex": x} for e, p, x in cartoes])


def ouvir(itens):
    """itens: ("frase", ["op1","op2","op3"], correta, "tradução") para escolha, ou ("frase", "dica") para ditado."""
    out = []
    for it in itens:
        if len(it) == 2:
            out.append({"frase": it[0], "dica": it[1]})
        else:
            out.append({"frase": it[0], "opcoes": list(it[1]), "correta": it[2], "pt": it[3]})
    return _b("ouvir", titulo="Escute e responda",
              corpo="<p>Clique em 🔊 (ou 🐢 para ouvir devagar). Onde houver alternativas, escolha; onde houver campo, escreva exatamente o que ouviu.</p>", itens=out)


def falar(frases):
    return _b("falar", titulo="Agora é a sua vez de falar",
              corpo="<p>Ouça o modelo, clique em 🎙 <b>Falar</b> e diga a frase. As palavras reconhecidas ficam verdes.</p>",
              frases=[{"en": e, "pt": p} for e, p in frases])


def _camadas(livro=None, doc=None, yg=None):
    pt, prof = [], []
    if doc and doc.get("url"):
        pt.append({"nome": doc.get("nome") or "Documentação oficial", "url": doc["url"], "trecho": "leitura de referência",
                   "foco": "Leia procurando os mesmos conceitos desta aula; documentação se lê como dicionário, não como romance."})
    for frase in ([yg] if isinstance(yg, str) else (yg or [])):
        pt.append({"nome": f"YouGlish: “{frase}” na boca de nativos", "url": "https://youglish.com/pronounce/" + frase.replace(" ", "%20") + "/english",
                   "trecho": "ouça 5 exemplos", "tempo": 5, "foco": "Frases reais, com sotaques diferentes, treinam o ouvido melhor do que repetir um só modelo."})
    if livro:
        key, secao, pergunta = (list(livro) + ["", ""])[:3]
        obra, url = LIVROS[key.split(":")[0]]
        n = key.split(":", 1)[1] if ":" in key else ""
        prof.append({"obra": obra, "url": url.replace("{n}", n), "secao": secao, "perguntas": [pergunta] if pergunta else []})
    if not pt and not prof:
        return None
    return _b("camadas", ponte=pt, profundidade=prof)


def aula(dur, gancho, obj, pre, blocos, resumo, prox, livro=None, yg=None):
    """livro=("CHAVE:parte-da-url", "seção", "pergunta guia"); yg="frase" (Inglês)."""
    return {"v": 2, "duracao": dur, "gancho": gancho, "objetivos": list(obj), "prerequisitos": list(pre),
            "blocos": [b for b in blocos if b], "resumo": list(resumo), "proxima": prox, "_livro": livro, "_yg": yg}


def finalizar(guia, doc=None):
    """Acrescenta a camada 'Vá mais fundo' (documentação/YouGlish + livro) se a aula ainda não tiver uma."""
    if not guia or guia.get("v") != 2:
        return guia
    livro, yg = guia.pop("_livro", None), guia.pop("_yg", None)
    if not any(b.get("tipo") == "camadas" for b in guia["blocos"]):
        c = _camadas(livro, doc, yg)
        if c:
            guia["blocos"].append(c)
    return guia
