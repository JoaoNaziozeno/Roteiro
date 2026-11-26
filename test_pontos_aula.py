# -*- coding: utf-8 -*-
"""
Pontos de cada aula (topo do estúdio): o valor mostrado na aula é o mesmo que a Jornada do hub soma.
Lê as páginas GERADAS:

    python -X utf8 build_ecosystem.py
    python -X utf8 -m unittest test_pontos_aula

Roda o código real da página no Node (cálculo RM + funções do aviso), com um localStorage falso.
"""
import json
import re
import unittest

from metrics_js import TRACK_WEIGHTS
from test_contadores import PAGINAS, funcao_js, json_apos, ler, node


def trecho(texto, inicio, fim_regex):
    """Do começo de `inicio` (na coluna 0) até a primeira linha que casa com `fim_regex`."""
    i = texto.index("\n" + inicio) + 1
    m = re.compile(fim_regex, re.M).search(texto, i)
    return texto[i:m.end()]


class PontosDaAula(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pag = {tr: ler(nome) for tr, nome in PAGINAS.items()}
        cls.hub = ler("index.html")

    def test_trilhas_usam_a_configuracao_e_os_pesos_do_hub(self):
        do_hub = json_apos(self.hub, "RM.configure(")
        for tr, s in self.pag.items():
            self.assertEqual(json_apos(s, "RM.configure("), do_hub, tr)
            self.assertIn("const TRACK_WEIGHTS = Object.freeze(" + json.dumps(TRACK_WEIGHTS) + ")", s, tr)
            self.assertIn('id="modal-points"', s, tr)
        self.assertIn("const TRACK_WEIGHTS = Object.freeze(" + json.dumps(TRACK_WEIGHTS) + ")", self.hub)
        self.assertIn("const JR_TRACK_WEIGHTS = RM.TRACK_WEIGHTS;", self.hub)

    def test_aula_soma_o_mesmo_que_a_jornada(self):
        s = self.pag["mat"]
        mapa = json_apos(s, "const TOPICS_MAP = ")
        obrig = [k for k, t in mapa.items() if not t["opt"]]
        opcional = next(k for k, t in mapa.items() if t["opt"])
        a, b, c, d = obrig[:4]
        rm = trecho(s, "const RM = (() => {", r"^RM\.configure\(.*\);$")
        js = ("const store = {}; const localStorage = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); } };\n"
              + rm + "\nlet PR = {};\n"
              + trecho(s, "const lessonPtsRound", r"^const lessonPtsRound.*$") + "\n"
              + funcao_js(s, "lessonPointsInfo") + "\n"
              + f"""
const ids = {json.dumps([a, b, c, d, opcional])};
PR = {{ "ia-0-0-0": {{ s: "e" }}, "ing-0-0-0": {{ s: "e" }} }};
PR[ids[1]] = {{ s: "r", vp: 100, gp: 50 }};
PR[ids[2]] = {{ s: "r", vp: 100, gp: 100 }};
PR[ids[3]] = {{ s: "e" }};
const eff = {{ tracks: Object.assign({{}}, RM.TRACK_WEIGHTS), topics: {{}} }};
const out = {{}};
for (const id of ids) {{
  const x = lessonPointsInfo(id);
  // o que a Jornada soma se esta aula for concluída agora
  const antes = RM.progress(PR, eff).pts, guard = PR[id];
  PR[id] = Object.assign({{}}, guard, {{ s: "e" }});
  const depois = RM.progress(PR, eff).pts;
  PR[id] = guard;
  out[id] = Object.assign(x, {{ hubSoma: depois - antes }});
}}
out.totalPontos = RM.totals(eff).points;
console.log(JSON.stringify(out));
""")
        r = node(js)
        w = TRACK_WEIGHTS["mat"]
        self.assertEqual((r[a]["group"], r[a]["w"], r[a]["rest"]), ("todo", w, w))
        self.assertEqual((r[b]["group"], r[b]["got"], r[b]["rest"]), ("doing", w * 0.75, w * 0.25))
        self.assertEqual((r[c]["group"], r[c]["rest"]), ("full", 0))
        self.assertEqual((r[d]["group"], r[d]["rest"]), ("done", 0))
        self.assertEqual(r[opcional], {"group": "opt", "hubSoma": 0})
        for k in (a, b, c, d):
            self.assertAlmostEqual(r[k]["rest"], r[k]["hubSoma"], places=9, msg=k)   # aula e hub contam igual
            # o % da Jornada sobe exatamente o que falta na aula, sobre o total de pontos do roteiro
            self.assertAlmostEqual(r[k]["jAfter"] - r[k]["jNow"], r[k]["rest"] / r["totalPontos"] * 100, places=9, msg=k)

    def test_todas_as_frases_saem_certas(self):
        s = self.pag["ing"]
        js = (trecho(s, "const LESSON_PTS_PHRASES = {", r"^\};$") + "\n"
              + trecho(s, "const lessonPtsRound", r"^const lessonPtsRound.*$") + "\n"
              + funcao_js(s, "lessonPointsUsable") + "\n" + funcao_js(s, "lessonPointsFill") + "\n"
              + r"""
const casos = {
  todo:  [{ w: 1, got: 0, rest: 1, jNow: 7.04, jAfter: 7.14 }, { w: 6, got: 0, rest: 6, jNow: 10, jAfter: 10.6 }],
  doing: [{ w: 6, got: 4.5, rest: 1.5, jNow: 10, jAfter: 10.15 }, { w: 4, got: 0.1, rest: 3.9, jNow: 3, jAfter: 3.4 }],
  full:  [{ w: 1, got: 1, rest: 0, jNow: 5, jAfter: 5 }, { w: 4, got: 4, rest: 0, jNow: 5, jAfter: 5 }],
  won:   [{ w: 6, got: 6, rest: 0, ganhou: 1.5, jNow: 12.3, jAfter: 12.3 }, { w: 1, got: 1, rest: 0, ganhou: 0, jNow: 5, jAfter: 5 }],
  done:  [{ w: 1, got: 1, rest: 0, jNow: 5, jAfter: 5 }, { w: 6, got: 6, rest: 0, jNow: 12.3, jAfter: 12.3 }],
  opt:   [{}]
};
const out = [], usaveis = {};
for (const g in LESSON_PTS_PHRASES) {
  usaveis[g] = 0;
  for (const x of casos[g]) for (const t of LESSON_PTS_PHRASES[g]) {
    if (!lessonPointsUsable(t, x)) continue;
    usaveis[g]++;
    out.push(lessonPointsFill(t, x).replace(/<\/?b>/g, ""));
  }
}
console.log(JSON.stringify({ out, usaveis, total: Object.values(LESSON_PTS_PHRASES).reduce((a, p) => a + p.length, 0) }));
""")
        r = node(js)
        self.assertGreaterEqual(r["total"], 35)                 # variedade de verdade
        for g, n in r["usaveis"].items():
            self.assertGreater(n, 0, g)
        for frase in r["out"]:
            self.assertNotRegex(frase, r"[{}]", frase)          # nenhum marcador sobrando
            self.assertNotIn("+0 ", frase)                      # nunca "some +0 pontos"
            self.assertNotRegex(frase, r"(?<![\d,])1 pontos\b", frase)  # "1 ponto", no singular
            self.assertNotRegex(frase, r"\bde ([\d,]+%) para \1", frase)   # nunca "sobe de 7% para 7%"
        self.assertTrue(any("+1 ponto" in f for f in r["out"]))
        self.assertTrue(any("+1,5 pontos" in f for f in r["out"]))
        self.assertTrue(any("Acabou de entrar na Jornada: +1,5 pontos" in f for f in r["out"]))   # o que acabou de somar
        self.assertFalse(any("Acabou de entrar na Jornada: +0" in f for f in r["out"]))


if __name__ == "__main__":
    unittest.main()
