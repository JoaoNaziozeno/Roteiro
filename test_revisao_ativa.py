# -*- coding: utf-8 -*-
"""
Revisão ativa (fase 2): cartões montados das aulas, sessão (escolha, nota, mistura, caderno) e páginas.
Lê as páginas GERADAS e o revisao_cartoes.json:

    python -X utf8 build_ecosystem.py
    python -X utf8 -m unittest test_revisao_ativa
"""
import json
import re
import unittest
import zipfile
from pathlib import Path

from review_cards import build_decks
from review_js import REVIEW_JS, REVIEW_UI_JS
from revisoes_page import RA_JS
from test_contadores import PAGINAS, json_apos, ler, node

BASE = Path(__file__).resolve().parent
FLASH = ("arm", "not", "pen", "pas", "exp", "pon", "obj")


class CartoesDasAulas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapas = {tr: json_apos(ler(nome), "const TOPICS_MAP = ") for tr, nome in PAGINAS.items()}
        cls.decks = json.loads((BASE / "revisao_cartoes.json").read_text(encoding="utf-8"))
        # questões do Treino (treino_<trilha>.json): também entram nos cartões das aulas que têm treino
        cls.treino = {}
        for arq in BASE.glob("treino_*.json"):
            cls.treino.update(json.loads(arq.read_text(encoding="utf-8")))

    def test_arquivo_e_o_que_as_aulas_geram_e_vai_para_o_deploy(self):
        self.assertEqual(self.decks, build_decks(self.mapas, self.treino))
        self.assertTrue((BASE / "dist_deploy" / "revisao_cartoes.json").exists())
        self.assertIn("revisao_cartoes.json", zipfile.ZipFile(BASE / "roteiro_aws_deploy.zip").namelist())

    def test_toda_aula_obrigatoria_tem_sessao_de_pelo_menos_4_cartoes(self):
        for tr, mapa in self.mapas.items():
            for tid, t in mapa.items():
                if t["opt"]:
                    continue
                self.assertIn(tid, self.decks, tid)
                ks = [c["k"] for c in self.decks[tid]["c"]]
                sessao = min(ks.count("mem"), 1) + min(sum(ks.count(k) for k in FLASH), 3) + min(ks.count("quiz"), 3)
                self.assertGreaterEqual(sessao, 4, tid)
                self.assertEqual(ks[0], "mem", tid)   # o "puxe da memória" sempre existe e vem primeiro

    def test_cartoes_completos(self):
        for tid, d in self.decks.items():
            for c in d["c"]:
                if c["k"] == "mem":
                    self.assertTrue(c["a"] and all(x.strip() for x in c["a"]), tid)
                elif c["k"] == "quiz":
                    self.assertTrue(c["q"] and len(c["o"]) >= 2 and 0 <= c["c"] < len(c["o"]), tid)
                elif c["k"] == "obj":
                    self.assertTrue(c["q"], tid)
                elif c["k"] == "tr":     # questão do Treino, inteira (formato em treino_js.py)
                    self.assertIn(c["q"]["k"], ("saida", "lacuna", "erro", "conceito", "conta"), tid)
                    self.assertIn(c["q"], self.treino[tid], tid)
                else:
                    self.assertTrue(c["q"] and (c.get("a") or c.get("l")), (tid, c["k"]))

    def test_reforco_da_matematica_tem_o_2o_video(self):
        for tid, t in self.mapas["mat"].items():
            if t.get("url2"):
                self.assertTrue(self.decks[tid]["r"].get("v2"), tid)


SESSAO = REVIEW_JS + "\n" + RA_JS + r"""
let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const deck = { c: [
  { k: "mem", a: ["ideia 1", "ideia 2"] },
  { k: "arm", q: "erro A", a: "certo A" }, { k: "arm", q: "erro B", a: "certo B" }, { k: "arm", q: "erro C", a: "certo C" },
  { k: "not", q: "$\\sum$", l: "somatório", a: "soma tudo" },
  { k: "pen", q: "por quê?", a: "porque <b>sim</b>" },
  { k: "quiz", q: "Q1", o: ["a", "b"], c: 0, e: "" }, { k: "quiz", q: "Q2", o: ["a", "b"], c: 1, e: "" },
  { k: "quiz", q: "Q3", o: ["a", "b"], c: 0, e: "" }, { k: "quiz", q: "Q4", o: ["a", "b"], c: 1, e: "" }
] };
const out = {};
out.escolha = RA.pick(deck, rnd).map(c => c.k);
out.notas = [["f", "f", "f", "f", "f", "f", "m"], ["f", "m", "z", "f"], ["z", "z", "m", "f"], []].map(RA.suggest);
out.mistura = RA.interleave([{ id: "a", cards: [1, 2, 3] }, { id: "b", cards: [1] }, { id: "c", cards: [1, 2] }], 5).map(x => x.id + x.card);
out.caderno = RA.noteText([deck.c[1], deck.c[4], deck.c[5], deck.c[6], deck.c[0]], "27/11");
out.texto = [RA.strip("Rodar <code>app.py</code>?"), RA.strip("<ul><li>um</li><li>dois</li></ul>"), RA.strip("a<br>b &lt;3")];
out.vazio = RA.noteText([], "27/11");
"""


class Sessao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = node(SESSAO + "\nconsole.log(JSON.stringify(out));")

    def test_escolha_varia_os_tipos_e_respeita_os_limites(self):
        e = self.r["escolha"]
        self.assertEqual(e[0], "mem")
        rapidos = [k for k in e if k in FLASH]
        self.assertEqual(len(rapidos), 3)
        self.assertEqual(sorted(set(rapidos)), ["arm", "not", "pen"])   # um de cada tipo antes de repetir
        self.assertEqual(e.count("quiz"), 3)

    def test_nota_sugerida(self):
        self.assertEqual(self.r["notas"], ["f", "m", "z", "z"])

    def test_revisao_do_dia_mistura_as_aulas(self):
        self.assertEqual(self.r["mistura"], ["a1", "b1", "c1", "a2", "c2"])

    def test_texto_do_caderno(self):
        c = self.r["caderno"]
        self.assertTrue(c.startswith("\n\n## 🔁 Revisão ativa de 27/11: pontos para reforçar\n"))
        self.assertIn("- erro A → certo A", c)
        self.assertIn("- O que significa $\\sum$ → somatório: soma tudo", c)
        self.assertIn("- por quê? → porque sim", c)            # sem HTML no caderno
        self.assertIn("- Q1 → a", c)                            # quiz: a resposta certa
        self.assertIn("- Ideias-chave da aula\n", c)
        self.assertEqual(self.r["vazio"], "")
        self.assertEqual(self.r["texto"], ["Rodar app.py?", "um dois", "a b <3"])   # sem espaço antes do "?"


class Caderno(unittest.TestCase):
    def test_anota_no_caderno_sem_mexer_no_resto(self):
        r = node(r"""
const store = {}; const localStorage = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); } };
""" + REVIEW_JS + r"""
store["roteiro-ia-v1"] = JSON.stringify({ "ia-0-0-0": { s: "e", n: "minha nota", d: "2026-12-01", vp: 100 } });
RV.appendNote("ia-0-0-0", "\n\n## extra");
RV.appendNote("ia-0-0-9", "nova");
console.log(store["roteiro-ia-v1"]);
""")
        self.assertEqual(r["ia-0-0-0"], {"s": "e", "n": "minha nota\n\n## extra", "d": "2026-12-01", "vp": 100})
        self.assertEqual(r["ia-0-0-9"], {"s": "z", "n": "nova", "d": ""})


class PaginasDaRevisaoAtiva(unittest.TestCase):
    def test_pagina_revisoes_tem_a_sessao(self):
        s = ler("revisoes.html")
        for trecho in ('id="ra"', "async function raStart(", "function raStartDay(", "katex.min.js", 'fetch("revisao_cartoes.json"',
                       'get("ativa")', "▶ Começar revisão do dia"):
            self.assertIn(trecho, s, trecho)
        # a sessão é carregada antes de a página usá-la (o ?ativa= abre a sessão ao carregar)
        self.assertLess(s.index("let RA_DECKS = null"), s.index("\nrenderRevisoes();"))

    def test_atalho_no_menu_e_segundo_video(self):
        self.assertIn('href="revisoes.html?ativa=', REVIEW_UI_JS)
        for nome in PAGINAS.values():
            self.assertIn('qs.get("video") === "2"', ler(nome), nome)


if __name__ == "__main__":
    unittest.main()
