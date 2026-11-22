# -*- coding: utf-8 -*-
"""
Organização do currículo com ids FIXOS.

O progresso de cada aluno é guardado pelo id do tópico ("mat-3-0-0" = trilha-fase-grupo-posição).
Antes, esse id era calculado pela posição na hora de gerar as páginas: mover ou remover um tópico
mudava o id de outros e embaralhava o progresso de todo mundo.

Aqui cada tópico recebe primeiro o seu id atual ("sid") e só DEPOIS o currículo é reorganizado:
reordenar módulos, marcar tópicos como opcionais ou acrescentar tópicos novos (com id próprio) não
muda o id de nenhum tópico existente. Os geradores usam topic_id() para ler o id.
"""

import re

# Tópicos de aprofundamento: continuam no roteiro, mas não contam na meta nem nos percentuais.
# (id, trecho que o título precisa conter, motivo exibido ao aluno)
OPTIONAL = [
    ("ia-1-4-0", "Web scraping", "Já visto na Fase 1 (Web scraping com BeautifulSoup)."),
    ("ia-1-5-2", "Streamlit", "Streamlit é visto na Fase 6, em Interfaces com Gradio e Streamlit."),
    ("ia-3-3-1", "GANs", "Aprofundamento: raramente cobrado de quem começa como engenheiro de IA."),
    ("ia-3-3-2", "difusão", "Aprofundamento: raramente cobrado de quem começa como engenheiro de IA."),
    ("ia-3-3-3", "grafos", "Aprofundamento: raramente cobrado de quem começa como engenheiro de IA."),
    ("ia-3-3-4", "YOLO", "Aprofundamento em visão computacional."),
    ("ia-3-3-5", "Segmentação", "Aprofundamento em visão computacional."),
    ("ia-3-4-5", "Mixed precision", "Otimização avançada de treino."),
    ("ia-3-5-0", "TensorFlow", "O roteiro usa PyTorch; TensorFlow fica como alternativa."),
    ("ia-3-5-2", "ONNX", "Aprofundamento de deploy de modelos."),
    ("ia-3-5-3", "Lightning", "Aprofundamento: atalho sobre o PyTorch puro."),
    ("mat-0-1-3", "pseudoinversa", "Aprofundamento de álgebra linear."),
    ("mat-1-1-1", "Hessiana", "Aprofundamento de cálculo."),
    ("mat-2-1-1", "Limite Central", "Aprofundamento de estatística."),
]


def _as_dict(raw):
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and "||" in raw:
        title, url = raw.split("||", 1)
        return {"title": title, "video_url": url}
    return {"title": str(raw)}


def title_of(raw):
    return _as_dict(raw).get("title", "") if isinstance(raw, (dict, str)) else str(raw)


def topic_id(raw, tr, p_idx, g_idx, t_idx):
    """Id fixo do tópico (sid) ou, se não houver, o id pela posição."""
    if isinstance(raw, dict) and raw.get("sid"):
        return raw["sid"]
    return f"{tr}-{p_idx}-{g_idx}-{t_idx}"


def is_optional(raw):
    return isinstance(raw, dict) and bool(raw.get("opt"))


def stabilize(tracks):
    """Carimba em cada tópico o id que ele tem HOJE (antes de qualquer reorganização)."""
    for tr, phases in tracks.items():
        for p_idx, p in enumerate(phases):
            for g_idx, g in enumerate(p["g"]):
                items = g[1]
                for t_idx, raw in enumerate(items):
                    d = _as_dict(raw)
                    if d is not raw:
                        items[t_idx] = d
                    d.setdefault("sid", f"{tr}-{p_idx}-{g_idx}-{t_idx}")


def _renumber(phases):
    for i, p in enumerate(phases):
        p["t"] = re.sub(r"^Módulo \d+", f"Módulo {i + 1}", p["t"])


def reorganize_math(phases):
    """Fundamentos (funções, logaritmos, notação) passam para o início; Teoria da Informação vai
    para depois de Probabilidade. Os ids dos tópicos não mudam."""
    old4 = next(p for p in phases if p["t"].startswith("Módulo 4"))
    prob = next(p for p in phases if p["t"].startswith("Módulo 3"))
    fund_group = next(g for g in old4["g"] if g[0].startswith("Álgebra e Geometria"))
    info_group = next(g for g in old4["g"] if g[0].startswith("Teoria da Informação"))
    fundamentos = {
        "t": "Módulo 0 · Fundamentos: Funções, Logaritmos & Notação Matemática",
        "d": "1 a 2 semanas",
        "tip": old4["tip"],
        "p": "Desenhar em Python (matplotlib) uma reta, uma parábola, uma exponencial e um logaritmo, "
             "e calcular à mão e em código um somatório escrito na notação usada nos artigos de IA.",
        "r": old4["r"],
        "g": [["Fundamentos para Ler a Matemática da IA", fund_group[1]]],
    }
    prob["t"] = "Módulo 3 · Probabilidade, Estatística & Teoria da Informação"
    prob["d"] = "4 a 5 semanas"
    prob["p"] = prob["p"].rstrip(".") + ". Depois, implementar do zero a Softmax e a Cross-Entropy Loss."
    prob["g"].append(info_group)
    phases.remove(old4)
    phases.insert(0, fundamentos)
    _renumber(phases)


def mark_optional(tracks):
    index = {}
    for tr, phases in tracks.items():
        for p in phases:
            for g in p["g"]:
                for raw in g[1]:
                    index[raw["sid"]] = raw
    for sid, must_contain, why in OPTIONAL:
        raw = index.get(sid)
        if raw is None or must_contain.lower() not in raw.get("title", "").lower():
            raise ValueError(f"Tópico opcional não confere: {sid} deveria conter '{must_contain}' "
                             f"(título atual: {raw and raw.get('title')!r})")
        raw["opt"] = True
        raw["opt_note"] = why


def apply(tracks):
    """Aplica tudo, em ordem. Altera as listas no lugar."""
    stabilize(tracks)
    reorganize_math(tracks["mat"])
    mark_optional(tracks)
    return tracks


def counts(tracks):
    """{trilha: {"req": obrigatórios, "opt": opcionais, "phases": nº de fases/módulos}}"""
    out = {}
    for tr, phases in tracks.items():
        req = opt = 0
        for p in phases:
            for g in p["g"]:
                for raw in g[1]:
                    if is_optional(raw):
                        opt += 1
                    else:
                        req += 1
        out[tr] = {"req": req, "opt": opt, "phases": len(phases)}
    return out


def split_count(topics):
    """(obrigatórios, opcionais) de uma lista de tópicos: a regra única de todos os contadores."""
    opt = sum(1 for t in topics if is_optional(t))
    return len(topics) - opt, opt


def required_ids(tracks):
    return sorted(raw["sid"] for phases in tracks.values() for p in phases for g in p["g"]
                  for raw in g[1] if not is_optional(raw))


def optional_ids(tracks):
    return sorted(raw["sid"] for phases in tracks.values() for p in phases for g in p["g"]
                  for raw in g[1] if is_optional(raw))
