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
        config = json_apos(s, "RM.configure(")
        com_treino = set(config["treino"])
        obrig = [k for k, t in mapa.items() if not t["opt"]]
        opcional = next(k for k, t in mapa.items() if t["opt"])
        a, b, c, d, e, f = obrig[:6]
        self.assertLessEqual({a, b, c, d, e, f}, com_treino)                  # toda a Matemática tem treino
        sem = next(k for k in config["required"] if k.startswith("ia-") and k not in com_treino)
        rm = trecho(s, "const RM = (() => {", r"^RM\.configure\(.*\);$")
        js = ("const store = {}; const localStorage = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); } };\n"
              + rm + "\nlet PR = {};\n"
              + trecho(s, "const lessonPtsRound", r"^const lessonPtsRound.*$") + "\n"
              + funcao_js(s, "lessonPointsInfo") + "\n"
              + f"""
const ids = {json.dumps([a, b, c, d, e, f, sem, opcional])};
PR = {{ "ia-0-0-0": {{ s: "e" }}, "ing-0-0-0": {{ s: "e" }} }};
PR[ids[1]] = {{ s: "r", vp: 100, gp: 50 }};
PR[ids[2]] = {{ s: "r", vp: 100, gp: 100 }};     // estudo completo, treino por fazer
PR[ids[3]] = {{ s: "e" }};                       // concluída, treino abaixo de 70%
PR[ids[4]] = {{ s: "e" }};                       // concluída e com o treino aprovado
PR[ids[5]] = {{ s: "r", vp: 100, gp: 50 }};      // em andamento, treino aprovado
PR[ids[6]] = {{ s: "e" }};                       // aula sem treino
store["roteiro-answers-v1"] = JSON.stringify({{ [ids[3]]: {{ tr: {{ b: 60 }} }}, [ids[4]]: {{ tr: {{ b: 80 }} }}, [ids[5]]: {{ tr: {{ b: 70 }} }} }});
const eff = {{ tracks: Object.assign({{}}, RM.TRACK_WEIGHTS), topics: {{}} }};
const melhor = () => RM.trBest(JSON.parse(store["roteiro-answers-v1"]));
const out = {{}};
for (const id of ids) {{
  const x = lessonPointsInfo(id);
  // o que a Jornada soma se esta aula ficar completa agora (concluída e com o treino aprovado)
  const antes = RM.progress(PR, eff, melhor()).pts, guard = PR[id], salvo = store["roteiro-answers-v1"];
  const ans = JSON.parse(salvo); ans[id] = {{ tr: {{ b: 100 }} }}; store["roteiro-answers-v1"] = JSON.stringify(ans);
  PR[id] = Object.assign({{}}, guard, {{ s: "e" }});
  const depois = RM.progress(PR, eff, melhor()).pts;
  PR[id] = guard; store["roteiro-answers-v1"] = salvo;
  out[id] = Object.assign(x, {{ hubSoma: depois - antes }});
}}
out.totalPontos = RM.totals(eff).points;
console.log(JSON.stringify(out));
""")
        r = node(js)
        w, sh = TRACK_WEIGHTS["mat"], 0.25
        tr = w * sh
        self.assertEqual((r[a]["group"], r[a]["w"], r[a]["rest"], r[a]["tr"], r[a]["trOk"], r[a]["trPts"]), ("todo", w, w, True, False, tr))
        self.assertEqual((r[b]["group"], r[b]["got"], r[b]["rest"]), ("doing", (w - tr) * 0.75, w - (w - tr) * 0.75))
        self.assertEqual((r[c]["group"], r[c]["got"], r[c]["rest"]), ("treino", w - tr, tr))    # o resto é do treino
        self.assertEqual((r[d]["group"], r[d]["got"], r[d]["rest"]), ("treino", w - tr, tr))    # 60% não basta
        self.assertEqual((r[e]["group"], r[e]["rest"], r[e]["trOk"]), ("done", 0, True))
        self.assertEqual((r[f]["group"], r[f]["got"]), ("doing", (w - tr) * 0.75 + tr))
        self.assertEqual((r[sem]["group"], r[sem]["w"], r[sem]["rest"], r[sem]["tr"]), ("done", TRACK_WEIGHTS["ia"], 0, False))
        self.assertEqual(r[opcional], {"group": "opt", "hubSoma": 0})
        for k in (a, b, c, d, e, f, sem):
            self.assertAlmostEqual(r[k]["rest"], r[k]["hubSoma"], places=9, msg=k)   # aula e hub contam igual
            # o % da Jornada sobe exatamente o que falta na aula, sobre o total de pontos do roteiro
            self.assertAlmostEqual(r[k]["jAfter"] - r[k]["jNow"], r[k]["rest"] / r["totalPontos"] * 100, places=9, msg=k)
            self.assertEqual(r[k]["min"], 70, k)

    def test_todas_as_frases_saem_certas(self):
        s = self.pag["ing"]
        js = (trecho(s, "const LESSON_PTS_PHRASES = {", r"^\};$") + "\n"
              + trecho(s, "const lessonPtsRound", r"^const lessonPtsRound.*$") + "\n"
              + funcao_js(s, "lessonPointsUsable") + "\n" + funcao_js(s, "lessonPointsFill") + "\n"
              + r"""
const T6 = { tr: true, trOk: false, trPts: 1.5, estudo: 4.5, min: 70 }, T4 = { tr: true, trOk: false, trPts: 1, estudo: 3, min: 70 };
const casos = {
  todo:  [{ group: "todo", w: 1, got: 0, rest: 1, jNow: 7.04, jAfter: 7.14 }, { group: "todo", w: 6, got: 0, rest: 6, jNow: 10, jAfter: 10.6 },
          Object.assign({ group: "todo", w: 6, got: 0, rest: 6, jNow: 10, jAfter: 10.6 }, T6),
          Object.assign({ group: "todo", w: 4, got: 0, rest: 4, jNow: 3, jAfter: 3.4 }, T4)],
  doing: [{ group: "doing", w: 6, got: 4.5, rest: 1.5, jNow: 10, jAfter: 10.15 }, { group: "doing", w: 4, got: 0.1, rest: 3.9, jNow: 3, jAfter: 3.4 },
          Object.assign({ group: "doing", w: 6, got: 2.25, rest: 3.75, jNow: 10, jAfter: 10.4 }, T6),
          Object.assign({ group: "doing", w: 4, got: 2, rest: 2, jNow: 3, jAfter: 3.2 }, T4, { trOk: true })],   // treino feito, estudo pela metade
  full:  [{ group: "full", w: 1, got: 1, rest: 0, jNow: 5, jAfter: 5 }, { group: "full", w: 4, got: 4, rest: 0, jNow: 5, jAfter: 5 }],
  treino: [Object.assign({ group: "treino", w: 6, got: 4.5, rest: 1.5, jNow: 12, jAfter: 12.2 }, T6),
           Object.assign({ group: "treino", w: 4, got: 3, rest: 1, jNow: 5, jAfter: 5.1 }, T4)],
  won:   [{ group: "done", w: 6, got: 6, rest: 0, ganhou: 1.5, jNow: 12.3, jAfter: 12.3 }, { group: "done", w: 1, got: 1, rest: 0, ganhou: 0, jNow: 5, jAfter: 5 }],
  wonTr: [Object.assign({ group: "treino", w: 6, got: 4.5, rest: 1.5, ganhou: 1.1, jNow: 12, jAfter: 12.2 }, T6),
          Object.assign({ group: "treino", w: 4, got: 3, rest: 1, ganhou: 0, jNow: 5, jAfter: 5.1 }, T4)],
  trWon: [Object.assign({ group: "done", w: 6, got: 6, rest: 0, ganhou: 1.5, jNow: 12.2, jAfter: 12.2 }, T6, { trOk: true }),
          Object.assign({ group: "doing", w: 4, got: 1, rest: 3, ganhou: 1, jNow: 3, jAfter: 3.4 }, T4, { trOk: true })],
  done:  [{ group: "done", w: 1, got: 1, rest: 0, jNow: 5, jAfter: 5 }, { group: "done", w: 6, got: 6, rest: 0, jNow: 12.3, jAfter: 12.3 }],
  opt:   [{}]
};
const out = [], usaveis = {}, erros = [];
for (const g in LESSON_PTS_PHRASES) {
  usaveis[g] = 0;
  for (const x of casos[g]) for (const t of LESSON_PTS_PHRASES[g]) {
    if (!lessonPointsUsable(t, x)) continue;
    usaveis[g]++;
    const f = lessonPointsFill(t, x).replace(/<\/?b>/g, "");
    out.push(f);
    // antes de completar o estudo: treino só nas aulas com treino por fazer, e nelas nada de "conclua e leve tudo"
    if (g === "todo" || g === "doing") {
      const pend = Boolean(x.tr && !x.trOk);
      if (/treino/.test(f) && !pend) erros.push(["treino sem treino por fazer", f]);
      if (pend && /conclu/i.test(f)) erros.push(["concluir não dá o treino", f]);
    }
  }
}
console.log(JSON.stringify({ out, usaveis, erros, total: Object.values(LESSON_PTS_PHRASES).reduce((a, p) => a + p.length, 0) }));
""")
        r = node(js)
        self.assertGreaterEqual(r["total"], 35)                 # variedade de verdade
        for g, n in r["usaveis"].items():
            self.assertGreater(n, 0, g)
        self.assertEqual(r["erros"], [])
        for frase in r["out"]:
            self.assertNotRegex(frase, r"[{}]", frase)          # nenhum marcador sobrando
            self.assertNotIn("undefined", frase)
            self.assertNotIn("NaN", frase)
            self.assertNotIn("+0 ", frase)                      # nunca "some +0 pontos"
            self.assertNotRegex(frase, r"(?<![\d,])1 pontos\b", frase)  # "1 ponto", no singular
            self.assertNotRegex(frase, r"\bde ([\d,]+%) para \1", frase)   # nunca "sobe de 7% para 7%"
        self.assertTrue(any("+1 ponto" in f for f in r["out"]))
        self.assertTrue(any("+1,5 pontos" in f for f in r["out"]))
        self.assertTrue(any("Acabou de entrar na Jornada: +1,5 pontos" in f for f in r["out"]))   # o que acabou de somar
        self.assertFalse(any("Acabou de entrar na Jornada: +0" in f for f in r["out"]))
        # treino: a parte dele, o mínimo de acertos e o que ele acabou de somar
        self.assertTrue(any("4,5 pontos pelo estudo e 1,5 pontos pelo treino" in f for f in r["out"]))
        self.assertTrue(any("3 pontos pelo estudo e 1 ponto pelo treino" in f for f in r["out"]))
        self.assertTrue(any("70%" in f for f in r["out"]))
        self.assertTrue(any(f.startswith("Treino aprovado! +1,5 pontos") for f in r["out"]))


if __name__ == "__main__":
    unittest.main()
