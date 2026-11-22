# -*- coding: utf-8 -*-
"""
Fase 1 de IA na ordem do curso de Python do Gustavo Guanabara, sem mudar o id de nenhum tópico.

1. cada tópico da lista-base recebe o id que sempre teve (pela posição);
2. as aulas que faltavam entram com id próprio ("g" + número da aula do curso), que nunca colide com os de posição;
3. só então os três primeiros grupos são ordenados por ORDEM.

Tópico novo na lista-base continua entrando no FIM do grupo dele (e precisa entrar em ORDEM se for desses grupos).
Ficam de fora de propósito: #02 (história do Python), #05 (instalar o PyCharm) e #11 (cores no terminal).
"""

_YT = "https://www.youtube.com/watch?v="
_DOC = "https://docs.python.org/pt-br/3/"

# (id, nº da aula, título do tópico, vídeo, assunto, caminho na documentação, nome da documentação)
NOVAS = [
    ("ia-0-0-g07", 7, "Operadores aritméticos", "Vw6gLypRKmY", "Operadores", "tutorial/introduction.html#numbers", "Números"),
    ("ia-0-0-g08", 8, "Usar módulos prontos (import)", "oOUyhGNib2Q", "Módulos", "library/math.html", "Módulo math"),
    ("ia-0-0-g09", 9, "Manipular textos (strings)", "a7DH88vk2Sk", "Textos", "library/stdtypes.html#string-methods", "Métodos de string"),
    ("ia-0-0-g12", 12, "Condições aninhadas e elif", "j9bYDjaAYzw", "elif", "tutorial/controlflow.html#if-statements", "if e elif"),
    ("ia-0-0-g14", 14, "Repetir enquanto (while)", "LH6OIn2lBaI", "while", "reference/compound_stmts.html#the-while-statement", "while"),
    ("ia-0-0-g15", 15, "Interromper laços (break) e f-strings", "1OFp_-R2B2A", "break", "tutorial/controlflow.html#break-and-continue-statements", "break e continue"),
    ("ia-0-1-g18", 18, "Listas compostas (listas dentro de listas)", "YV_JQmZNFsk", "Listas 2", "tutorial/datastructures.html#nested-list-comprehensions", "Listas aninhadas"),
    ("ia-0-1-g21", 21, "Funções: escopo, opcionais e docstrings", "etjJ_4Eqrk8", "Funções 2", "tutorial/controlflow.html#more-on-defining-functions", "Mais sobre funções"),
]

ORDEM = [
    # Base da linguagem: #01/03, 04, 06, 07, 08, 09, 10, 12, 13, 14, 15
    ["ia-0-0-0", "ia-0-0-2", "ia-0-0-1", "ia-0-0-g07", "ia-0-0-g08", "ia-0-0-g09",
     "ia-0-0-3", "ia-0-0-g12", "ia-0-0-4", "ia-0-0-g14", "ia-0-0-g15"],
    # Estruturas de dados: #16, 17, 18, 19 e list comprehension
    ["ia-0-1-2", "ia-0-1-0", "ia-0-1-g18", "ia-0-1-1", "ia-0-1-3"],
    # Programação intermediária: #20, 21, 22, 23 e o que vem depois do curso
    ["ia-0-0-5", "ia-0-1-g21", "ia-0-2-1", "ia-0-2-3", "ia-0-2-2", "ia-0-2-0", "ia-0-2-4", "ia-0-2-5"],
]


def organizar(phases):
    """Recebe a lista-base (recém-criada) e devolve as fases já com sid, aulas novas e ordem do curso."""
    for p_idx, p in enumerate(phases):
        for g_idx, g in enumerate(p["g"]):
            for t_idx, t in enumerate(g[1]):
                t["sid"] = f"ia-{p_idx}-{g_idx}-{t_idx}"

    grupos = phases[0]["g"][:len(ORDEM)]
    por_id = {t["sid"]: t for g in grupos for t in g[1]}
    for sid, n, titulo, vid, assunto, doc, doc_nome in NOVAS:
        por_id[sid] = {
            "sid": sid,
            "title": titulo,
            "video_url": _YT + vid,
            "video_label": f"▶ Guanabara #{n:02d} · {assunto}",
            "doc_url": _DOC + doc,
            "doc_label": f"📖 Docs {doc_nome}",
        }

    pedidos = [sid for ids in ORDEM for sid in ids]
    if sorted(pedidos) != sorted(por_id):
        raise ValueError("ORDEM da Fase 1 não confere com os tópicos: "
                         f"{sorted(set(pedidos) ^ set(por_id))}")
    for g, ids in zip(grupos, ORDEM):
        g[1][:] = [por_id[sid] for sid in ids]
    return phases
