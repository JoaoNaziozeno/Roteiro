# -*- coding: utf-8 -*-
"""
Cartões da "Revisão ativa", montados do conteúdo que cada Aula Visual já tem.

Gera revisao_cartoes.json: {id: {"c": [cartões candidatos], "r": {reforço}}}. A página Revisões só baixa
esse arquivo quando você começa uma revisão, e sorteia quais cartões entram em cada sessão (cada revisão
sai um pouco diferente). Nada de conteúdo novo é escrito à mão: tudo vem das aulas.

Tipos de cartão ("k"):
  mem   puxe da memória: as ideias-chave da aula (resumo "Para levar desta aula")
  arm   armadilha comum: o erro (frente) e a correção (verso)
  not   notação: o símbolo (frente) e a leitura + o significado (verso)
  pen   pense: a pergunta e a resposta
  pas   passo: o que se faz (frente) e o porquê (verso)
  exp   explique com suas palavras: o título de um texto da aula (frente) e o texto (verso)
  pon   onde isso aparece na IA: a conexão da aula com IA (verso)
        (exp e pon só entram em aulas com menos de 3 cartões rápidos)
  obj   consegue explicar isto?: um objetivo da aula (o verso mostra as ideias-chave do cartão "mem");
        só entra em aulas que ainda ficaram com menos de 4 cartões
  quiz  pergunta de múltipla escolha do quiz de saída (ou do "chute antes de ver"), com a explicação

Reforço ("r"), usado quando a revisão custou:
  v2    nome do 2º vídeo da aula (outra explicação)
  kid   texto do bloco "Explica como se eu tivesse 10 anos"
  src   fontes "Para o dia da revisão" [{nome, url, tempo}]
"""
import json

MAX_FLASH = 6      # candidatos por tipo de cartão rápido (a sessão sorteia até 3 no total)
MAX_QUIZ = 4       # perguntas candidatas (a sessão usa até 3)


def _txt(v):
    return v.strip() if isinstance(v, str) else ""


def build_deck(t):
    """Cartões e reforço de uma aula (t = item do TOPICS_MAP). None se a aula não tem Aula Visual v2."""
    g = t.get("pt_guide")
    if not isinstance(g, dict) or g.get("v") != 2:
        return None
    blocos = g.get("blocos") or []
    cards = []
    resumo = [_txt(r) for r in (g.get("resumo") or []) if _txt(r)]
    objetivos = [_txt(o) for o in (g.get("objetivos") or []) if _txt(o)]
    if resumo:
        mem = {"k": "mem", "a": resumo}
        if objetivos:
            mem["h"] = objetivos   # dica: o que a aula prometia ensinar
        cards.append(mem)
    for b in blocos:
        tipo = b.get("tipo")
        if tipo == "armadilhas":
            for it in (b.get("itens") or [])[:MAX_FLASH]:
                if _txt(it.get("erro")) and _txt(it.get("correcao")):
                    cards.append({"k": "arm", "q": _txt(it["erro"]), "a": _txt(it["correcao"])})
        elif tipo == "notacao":
            for it in (b.get("itens") or [])[:MAX_FLASH]:
                if _txt(it.get("simbolo")) and (_txt(it.get("significado")) or _txt(it.get("leitura"))):
                    cards.append({"k": "not", "q": _txt(it["simbolo"]), "l": _txt(it.get("leitura")), "a": _txt(it.get("significado"))})
        elif tipo == "pense":
            if _txt(b.get("pergunta")) and _txt(b.get("resposta")):
                cards.append({"k": "pen", "q": _txt(b["pergunta"]), "a": _txt(b["resposta"])})
        elif tipo == "passos":
            for p in (b.get("passos") or [])[:MAX_FLASH]:
                if _txt(p.get("faca")) and _txt(p.get("porque")):
                    cards.append({"k": "pas", "q": _txt(p["faca"]), "a": _txt(p["porque"]), "t": _txt(b.get("titulo"))})
    # Poucos cartões rápidos (algumas aulas de Matemática): os textos da aula viram "explique com suas palavras"
    # e o bloco "onde isso aparece na IA" vira pergunta de conexão
    if sum(1 for c in cards if c["k"] in ("arm", "not", "pen", "pas")) < 3:
        for b in blocos:
            tipo, titulo, corpo = b.get("tipo"), _txt(b.get("titulo")), _txt(b.get("corpo"))
            if tipo == "texto" and titulo and corpo:
                cards.append({"k": "exp", "q": titulo, "a": corpo})
            elif tipo == "ponte" and corpo:
                cards.append({"k": "pon", "q": titulo, "a": corpo})
    # Ainda poucos cartões: cada objetivo da aula vira "consegue explicar isto?" (o verso mostra as ideias-chave)
    if len(cards) < 4 and resumo:
        for o in objetivos[:3]:
            cards.append({"k": "obj", "q": o})
    quiz = []
    for b in blocos:
        if b.get("tipo") == "quiz":
            for q in b.get("perguntas") or []:
                if _txt(q.get("pergunta")) and len(q.get("opcoes") or []) >= 2 and isinstance(q.get("correta"), int):
                    quiz.append({"k": "quiz", "q": _txt(q["pergunta"]), "o": [_txt(o) for o in q["opcoes"]],
                                 "c": q["correta"], "e": _txt(q.get("explicacao"))})
    if len(quiz) < 2:   # pouco quiz: o "chute antes de ver" também vira pergunta
        for b in blocos:
            if b.get("tipo") == "palpite" and _txt(b.get("pergunta")) and len(b.get("opcoes") or []) >= 2 and isinstance(b.get("correta"), int):
                quiz.append({"k": "quiz", "q": _txt(b["pergunta"]), "o": [_txt(o) for o in b["opcoes"]],
                             "c": b["correta"], "e": _txt(b.get("explicacao"))})
    cards += quiz[:MAX_QUIZ]

    reforco = {}
    if t.get("url2"):
        reforco["v2"] = _txt(t.get("label2")).replace("🎬 2ª Opção:", "").strip() or "2º vídeo da aula"
    kid = next((b for b in blocos if b.get("tipo") == "crianca" and _txt(b.get("corpo"))), None)
    if kid:
        reforco["kid"] = _txt(kid["corpo"])
    fontes = [{"nome": _txt(s.get("nome")), "url": _txt(s.get("url")), "tempo": _txt(s.get("tempo"))}
              for b in blocos if b.get("tipo") == "camadas" for s in (b.get("revisao") or [])
              if _txt(s.get("nome")) and _txt(s.get("url"))]
    if fontes:
        reforco["src"] = fontes
    return {"c": cards, "r": reforco}


def build_decks(topic_maps):
    """topic_maps = {"ia": TOPICS_MAP, "mat": ..., "ing": ...} -> {id: deck}"""
    decks = {}
    for tm in topic_maps.values():
        for tid, t in tm.items():
            d = build_deck(t)
            if d and d["c"]:
                decks[tid] = d
    return decks


def write_decks(topic_maps, out_path):
    decks = build_decks(topic_maps)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(decks, f, ensure_ascii=False, separators=(",", ":"))
    return decks
