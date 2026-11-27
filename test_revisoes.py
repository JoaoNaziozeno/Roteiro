# -*- coding: utf-8 -*-
"""
Agenda de revisões (review_js.RV): o cálculo roda no Node com um localStorage falso e datas fixas.
As verificações das páginas leem as páginas GERADAS:

    python -X utf8 build_ecosystem.py
    python -X utf8 -m unittest test_revisoes
"""
import json
import re
import unittest
from pathlib import Path

from review_js import REVIEW_JS
from test_contadores import node

BASE = Path(__file__).resolve().parent

# 27/11/2026, 10h no horário local: "hoje" = 2026-11-27
PREAMBULO = r"""
const store = {};
const localStorage = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); }, removeItem: k => { delete store[k]; } };
const NOW = new Date(2026, 10, 27, 10).getTime(), DAY = 86400000;
const R = () => JSON.parse(store["roteiro-review-v1"] || "{}");
const P = () => JSON.parse(store["roteiro-ia-v1"] || "{}");
const limpa = () => { for (const k in store) delete store[k]; };
""" + REVIEW_JS + "\nconst out = {};\n"


def rodar(cenario):
    return node(PREAMBULO + cenario + "\nconsole.log(JSON.stringify(out));")


class AgendaDeRevisoes(unittest.TestCase):
    def test_datas(self):
        r = rodar("""
out.hoje = RV.today(NOW);
out.virada = [RV.addDays("2026-11-30", 1), RV.addDays("2026-12-31", 1), RV.addDays("2026-03-01", -1)];
out.entre = [RV.between("2026-12-31", "2027-01-02"), RV.between("2026-11-27", "2026-11-20")];
out.quando = ["2026-11-26", "2026-11-20", "2026-11-27", "2026-11-28", "2026-11-30", "2026-12-10"].map(d => RV.when(d, NOW));
""")
        self.assertEqual(r["hoje"], "2026-11-27")
        self.assertEqual(r["virada"], ["2026-12-01", "2027-01-01", "2026-02-28"])
        self.assertEqual(r["entre"], [2, -7])
        self.assertEqual(r["quando"], ["atrasada desde ontem", "atrasada desde 20/11", "hoje", "amanhã", "em 3 dias", "10/12"])

    def test_formato_antigo_do_quiz_entra_na_agenda(self):
        r = rodar("""
store["roteiro-review-v1"] = JSON.stringify({
  "ia-0-0-0": { score: 3, total: 3, passedAt: NOW - 2 * DAY, last: NOW - 2 * DAY, next: [NOW - DAY, NOW + DAY, NOW + 5 * DAY, NOW + 19 * DAY] },
  "ia-0-0-1": { score: 3, total: 3, passedAt: NOW - 3 * DAY, done: NOW - DAY, last: NOW - DAY, next: [NOW - 2 * DAY, NOW + DAY, NOW + 4 * DAY, NOW + 18 * DAY] },
  "ia-0-0-2": { score: 3, total: 3, passedAt: NOW - 40 * DAY, done: NOW - DAY, last: NOW - DAY, next: [NOW - 39 * DAY, NOW - 37 * DAY, NOW - 33 * DAY, NOW - 19 * DAY] }
});
out.agenda = RV.agenda(NOW);
out.contagem = RV.counts(NOW);
""")
        self.assertEqual([(i["id"], i["due"], i["step"], i["src"]) for i in r["agenda"]],
                         [("ia-0-0-0", "2026-11-26", 0, "quiz"), ("ia-0-0-1", "2026-11-28", 1, "quiz")])   # a 3ª já fez tudo
        self.assertEqual(r["contagem"], {"late": 1, "hoje": 0, "due": 1, "soon": 1, "total": 2})

    def test_marca_antiga_entra_como_hoje_e_sai_ao_agendar(self):
        r = rodar("""
store["roteiro-ia-v1"] = JSON.stringify({ "mat-3-0-1": { s: "e", n: "", d: "", rv: NOW - 5 * DAY }, "ia-0-0-0": { s: "e" } });
out.antes = RV.agenda(NOW);
const token = RV.schedule("mat-3-0-1", "2026-11-30", NOW);
out.depois = RV.agenda(NOW);
out.flag = P()["mat-3-0-1"].rv === undefined;
out.status = P()["mat-3-0-1"].s;
RV.restore("mat-3-0-1", token, NOW + 1000);
out.desfeito = RV.agenda(NOW);
limpa();
store["roteiro-ia-v1"] = JSON.stringify({ "mat-3-0-2": { s: "e", rv: NOW - DAY } });
RV.complete("mat-3-0-2", "m", NOW);                         // revisou direto a aula da marca antiga
out.origem = RV.stateOf(R()["mat-3-0-2"]).src;
""")
        self.assertEqual([(i["id"], i["due"], i["src"]) for i in r["antes"]], [("mat-3-0-1", "2026-11-27", "manual")])
        self.assertEqual([(i["id"], i["due"], i["src"]) for i in r["depois"]], [("mat-3-0-1", "2026-11-30", "manual")])
        self.assertTrue(r["flag"])
        self.assertEqual(r["status"], "e")   # a situação da aula não muda
        self.assertEqual([(i["id"], i["due"]) for i in r["desfeito"]], [("mat-3-0-1", "2026-11-27")])
        self.assertEqual(r["origem"], "manual")   # continua "agendada por você", não "pelo quiz"

    def test_intervalos_crescem_e_a_aula_fica_dominada(self):
        r = rodar("""
RV.schedule("ia-0-1-0", "2026-11-27", NOW);
out.passos = [];
let t = NOW;
for (let i = 0; i < 5; i++) { RV.complete("ia-0-1-0", "f", t); const st = RV.stateOf(R()["ia-0-1-0"]); out.passos.push(st ? [st.step, st.due] : null); }
out.dominada = Boolean(R()["ia-0-1-0"].mastered);
limpa();
RV.schedule("ia-0-1-1", "2026-11-27", NOW);
RV.complete("ia-0-1-1", "f", NOW); RV.complete("ia-0-1-1", "f", NOW);   // passo 2 (7 dias)
RV.complete("ia-0-1-1", "m", NOW); out.esforco = RV.stateOf(R()["ia-0-1-1"]);
RV.complete("ia-0-1-1", "z", NOW); out.esqueci = RV.stateOf(R()["ia-0-1-1"]);
for (let i = 0; i < 20; i++) RV.complete("ia-0-1-1", "m", NOW + i);
out.hist = R()["ia-0-1-1"].hist.length;
out.previa = ["z", "m", "f"].map(g => RV.preview("ia-0-1-1", g, NOW));
""")
        self.assertEqual(r["passos"], [[1, "2026-11-30"], [2, "2026-12-04"], [3, "2026-12-18"], [4, "2027-01-26"], None])
        self.assertTrue(r["dominada"])
        self.assertEqual((r["esforco"]["step"], r["esforco"]["due"]), (2, "2026-12-04"))   # com esforço: mesmo intervalo
        self.assertEqual((r["esqueci"]["step"], r["esqueci"]["due"]), (0, "2026-11-28"))   # não lembrei: amanhã
        self.assertEqual(r["hist"], 12)
        self.assertEqual(r["previa"], ["2026-11-28", "2026-11-28", "2026-11-30"])

    def test_quiz_agenda_a_primeira_e_refazer_no_dia_conta_como_revisao(self):
        r = rodar("""
RV.quizPassed("ing-0-0-0", 2, 3, NOW);
out.primeira = R()["ing-0-0-0"];
RV.quizPassed("ing-0-0-0", 3, 3, NOW + 3600e3);              // antes do dia: só atualiza a nota
out.antesDoDia = RV.stateOf(R()["ing-0-0-0"]);
RV.quizPassed("ing-0-0-0", 3, 3, NOW + DAY);                 // no dia da revisão, tudo certo = fácil
out.noDia = RV.stateOf(R()["ing-0-0-0"]);
out.notas = R()["ing-0-0-0"].hist.map(h => h[1]);
limpa();
RV.schedule("ing-0-0-1", "2026-12-05", NOW);                 // você já tinha marcado uma data
RV.quizPassed("ing-0-0-1", 3, 3, NOW);
out.manual = RV.stateOf(R()["ing-0-0-1"]);
""")
        p = r["primeira"]
        self.assertEqual((p["due"], p["step"], p["src"], p["score"], p["total"]), ("2026-11-28", 0, "quiz", 2, 3))
        self.assertTrue(p["passedAt"])
        self.assertEqual(r["antesDoDia"]["due"], "2026-11-28")
        self.assertEqual((r["noDia"]["step"], r["noDia"]["due"]), (1, "2026-12-01"))
        self.assertEqual(r["notas"], ["f"])
        self.assertEqual((r["manual"]["due"], r["manual"]["src"]), ("2026-12-05", "manual"))

    def test_tirar_e_desfazer(self):
        r = rodar("""
RV.quizPassed("ia-0-2-0", 3, 3, NOW);
const tk = RV.remove("ia-0-2-0", NOW);
out.semAgenda = RV.agenda(NOW).length;
RV.restore("ia-0-2-0", tk, NOW + 5);
out.volta = RV.stateOf(R()["ia-0-2-0"]);
const tk2 = RV.schedule("ia-0-2-9", "2026-12-01", NOW);      // aula que não estava na agenda
RV.restore("ia-0-2-9", tk2, NOW + 5);
out.someDeNovo = RV.stateOf(R()["ia-0-2-9"]);
out.last = R()["ia-0-2-9"].last;
""")
        self.assertEqual(r["semAgenda"], 0)
        self.assertEqual(r["volta"]["due"], "2026-11-28")
        self.assertIsNone(r["someDeNovo"])
        self.assertGreater(r["last"], 0)

    def test_numeros_da_semana(self):
        r = rodar("""
store["roteiro-review-v1"] = JSON.stringify({
  "ia-0-0-0": { due: "2026-11-30", step: 1, hist: [[NOW - 2 * DAY, "z"], [NOW - DAY, "m"], [NOW - 20 * DAY, "z"]] },
  "mat-0-0-0": { due: null, step: 4, mastered: NOW - DAY, hist: [[NOW, "f"]] }
});
out.s = RV.stats(NOW);
""")
        s = r["s"]
        self.assertEqual((s["feitas"], s["f"], s["m"], s["z"], s["dominadas"], s["streak"]), (3, 1, 1, 1, 1, 3))
        self.assertEqual(s["hard"], [["ia-0-0-0", 2]])


class PaginasComAgenda(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ler = lambda self, n: (BASE / n).read_text(encoding="utf-8")

    def test_pagina_revisoes_existe_e_vai_para_o_deploy(self):
        s = self.ler("revisoes.html")
        self.assertIn('<body data-track="rev">', s)
        self.assertIn("const RV = (() => {", s)
        self.assertIn("awsRealtimePullFromDynamoDB", s)          # sincroniza com a nuvem como as outras
        self.assertIn('id="rv-lista"', s)
        self.assertTrue((BASE / "dist_deploy" / "revisoes.html").exists())
        import zipfile
        self.assertIn("revisoes.html", zipfile.ZipFile(BASE / "roteiro_aws_deploy.zip").namelist())

    def test_menu_tem_revisoes_com_contador_em_todas_as_paginas(self):
        for nome in ("index.html", "ia.html", "matematica.html", "ingles.html", "projetos.html", "revisoes.html",
                     "Roteiro de Estudo_ do zero à IA.html"):
            s = self.ler(nome)
            nav = s[s.index('<nav class="nav-links"'):s.index("</nav>")]
            self.assertEqual(nav.count('href="revisoes.html"'), 1, nome)
            self.assertIn('id="nav-rv-badge"', nav, nome)
            self.assertLess(s.index("const RV = (() => {"), s.index('<nav class="nav-links"'), nome)   # contador antes da 1ª pintura
            self.assertIn("rvNavBadge()", s[s.index("</nav>"):s.index("</nav>") + 4000], nome)
        self.assertIn('href="revisoes.html" class="nav-link active"', self.ler("revisoes.html"))

    def test_trilhas_hub_e_quiz_usam_a_agenda(self):
        for nome in ("ia.html", "matematica.html", "ingles.html"):
            s = self.ler(nome)
            self.assertNotIn("toggleTopicReview", s, nome)
            self.assertIn("openReviewMenu(CURRENT_MODAL_TOPIC_ID, this)", s, nome)
            self.assertIn("RV.byId()", s, nome)
            self.assertIn("RV.quizPassed(", s, nome)
            self.assertNotIn("LV2_REVIEW_DAYS", s, nome)
        hub = self.ler("index.html")
        self.assertIn('id="av-hoje"', hub)              # as revisões de hoje aparecem no cartão "Hoje" (avisos)
        self.assertNotIn("function cqReviewDone", hub)

    def test_sincronizacao_avisa_as_paginas(self):
        s = self.ler("ia.html")
        pull = s[s.index("async function awsRealtimePullFromDynamoDB"):]
        pull = pull[:pull.index("\n}\n")]
        self.assertIn('new CustomEvent("rv:change")', pull)


if __name__ == "__main__":
    unittest.main()
