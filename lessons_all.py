# -*- coding: utf-8 -*-
"""
Junta todas as Aulas Visuais de IA e Inglês:
  - IA: arquivos ia_f*.py (um dicionário AULAS por arquivo, chaveado pelo título do tópico) + pilotos;
  - Inglês: arquivos en_m*.py (AULAS chaveado pelo videoId da playlist) + pilotos.
Os pilotos, feitos à mão com trechos de vídeo, têm prioridade sobre as aulas geradas em lote.
"""
import glob
import importlib
import os

BASE = os.path.dirname(os.path.abspath(__file__))


def _load(pattern):
    out = {}
    for path in sorted(glob.glob(os.path.join(BASE, pattern))):
        mod = importlib.import_module(os.path.splitext(os.path.basename(path))[0])
        dup = set(out) & set(mod.AULAS)
        if dup:
            raise ValueError(f"Aula repetida em {os.path.basename(path)}: {sorted(dup)}")
        out.update(mod.AULAS)
    return out


def ia_guides():
    """Aulas de IA prontas para a página, já com a camada 'Vá mais fundo' (documentação do tópico + livro)."""
    from ia_lessons_pilot import IA_PILOT_GUIDES
    from build_ia_data import get_enriched_ia_phases
    from lesson_factory import finalizar
    g = _load("ia_f*.py")
    g.update(IA_PILOT_GUIDES)
    docs = {t["title"]: {"url": t.get("doc_url"), "nome": (t.get("doc_label") or "").replace("📖", "").strip()}
            for p in get_enriched_ia_phases() for grp in p["g"] for t in grp[1]}
    return {k: finalizar(v, docs.get(k)) for k, v in g.items()}


def en_guides():
    """Aulas de Inglês prontas para a página (camada extra: YouGlish da frase-chave)."""
    from english_lessons_pilot import ENGLISH_PILOT_GUIDES
    from lesson_factory import finalizar
    g = _load("en_m*.py")
    g.update(ENGLISH_PILOT_GUIDES)
    return {k: finalizar(v) for k, v in g.items()}
