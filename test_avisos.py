# -*- coding: utf-8 -*-
"""
Avisos (fase 3): o cálculo (AV) roda no Node com datas fixas e um localStorage falso; as verificações das
páginas leem as páginas GERADAS:

    python -X utf8 build_ecosystem.py
    python -X utf8 -m unittest test_avisos
"""
import json
import re
import unittest

from alerts_js import AV_JS
from review_js import REVIEW_JS
from test_contadores import PAGINAS, json_apos, ler, node

# 27/11/2026, 10h (horário local)
BASE_JS = r"""
const store = {};
const localStorage = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); } };
const NOW = new Date(2026, 10, 27, 10).getTime(), DAY = 86400000;
const put = (k, v) => { store[k] = JSON.stringify(v); };
""" + REVIEW_JS + "\n" + AV_JS + "\nconst out = {};\n"
TOPICOS = [["ia-0-0-0", "ia", "Aula A", 1], ["ia-0-0-1", "ia", "Aula B", 1], ["mat-0-0-0", "mat", "Aula C", 0],
           ["ia-0-0-2", "ia", "Aula D", 1], ["ia-0-0-3", "ia", "Aula E", 1], ["ing-0-0-0", "ing", "Aula F", 1]]


def rodar(js):
    return node(BASE_JS + "const T = " + json.dumps(TOPICOS) + ";\n" + js + "\nconsole.log(JSON.stringify(out));")


def resumo(itens):
    return [(a["k"], a["grupo"], a["urg"], a.get("id") or a.get("pid") or "", a.get("n", "")) for a in itens]


class CalculoDosAvisos(unittest.TestCase):
    def test_sem_nada_nao_ha_aviso(self):
        r = rodar("out.l = AV.list(NOW, T); out.u = AV.urgentCount(NOW);")
        self.assertEqual((r["l"], r["u"]), ([], 0))

    def test_prazos_das_aulas_e_dos_projetos(self):
        r = rodar(r"""
put("roteiro-ia-v1", {
  "ia-0-0-0": { s: "r", d: "2026-11-26" },   // venceu ontem
  "ia-0-0-1": { s: "z", d: "2026-11-27" },   // vence hoje
  "mat-0-0-0": { s: "z", d: "2026-11-29" },  // em 2 dias
  "ia-0-0-2": { s: "e", d: "2026-11-20" },   // concluída: prazo não importa mais
  "ia-0-0-3": { s: "z", d: "2026-12-05" }    // longe demais
});
put("roteiro_portfolio_projects", [
  { id: "p1", title: "CLI", status: "wip", prazo: "2026-11-27" },
  { id: "p2", title: "ETL", status: "done", prazo: "2026-11-20" },
  { id: "p3", title: "Bot", status: "wip" },
  { id: "p4", title: "RAG", status: "planned", prazo: "2026-11-28" }
]);
out.l = AV.list(NOW, T); out.u = AV.urgentCount(NOW);
""")
        self.assertEqual(resumo([a for a in r["l"] if a["k"] in ("prazo", "proj")]), [
            ("prazo", "hoje", 1, "ia-0-0-0", -1), ("prazo", "hoje", 1, "ia-0-0-1", 0), ("prazo", "breve", 0, "mat-0-0-0", 2),
            ("proj", "hoje", 1, "p1", 0), ("proj", "breve", 0, "p4", 1)])
        sem = [a for a in r["l"] if a["k"] == "semprazo"]
        self.assertEqual([p["pid"] for p in sem[0]["projs"]], ["p3"])
        self.assertEqual(r["u"], 3)   # 2 prazos de aula + 1 de projeto (vencidos ou de hoje)

    def test_revisoes_contam_no_urgente(self):
        r = rodar(r"""
put("roteiro-review-v1", { "ia-0-0-0": { due: "2026-11-25", step: 0, src: "quiz" }, "ing-0-0-0": { due: "2026-11-27", step: 1, src: "quiz" },
                            "ia-0-0-1": { due: "2026-11-30", step: 1, src: "manual" } });
out.l = AV.list(NOW, T); out.u = AV.urgentCount(NOW);
""")
        rev = [a for a in r["l"] if a["k"] == "rev"][0]
        self.assertEqual((rev["n"], rev["late"], rev["urg"], rev["ids"]), (2, 1, 2, ["ia-0-0-0", "ing-0-0-0"]))
        self.assertEqual(r["u"], 2)

    def test_pendentes_quiz_e_aula_parada(self):
        r = rodar(r"""
put("roteiro-ia-v1", {
  "ia-0-0-0": { s: "e" },                    // concluída, tem quiz, sem aprovação: pendente
  "ia-0-0-1": { s: "e" },                    // concluída e aprovada no quiz
  "mat-0-0-0": { s: "e" },                   // concluída, mas a aula não tem quiz
  "ia-0-0-2": { s: "r" },                    // em andamento, última atividade há 10 dias: parada
  "ia-0-0-3": { s: "r" },                    // em andamento, ativa há 2 dias
  "ing-0-0-0": { s: "r" }                    // em andamento, sem nenhum registro: não dá para saber
});
put("roteiro-review-v1", { "ia-0-0-1": { passedAt: NOW - 5 * DAY, score: 3, total: 3 } });
put("roteiro-sessions-v1", [{ t: NOW - 10 * DAY, id: "ia-0-0-2", sec: 600 }, { t: NOW - 2 * DAY, id: "ia-0-0-3", sec: 300 }]);
out.l = AV.list(NOW, T);
""")
        quiz = [a for a in r["l"] if a["k"] == "quiz"][0]
        self.assertEqual(quiz["ids"], ["ia-0-0-0"])
        parada = [a for a in r["l"] if a["k"] == "parada"][0]
        self.assertEqual(parada["itens"], [{"id": "ia-0-0-2", "dias": 10}])
        self.assertTrue(all(a["urg"] == 0 for a in r["l"] if a["grupo"] == "pend"))

    def test_sequencia_em_risco_e_dias_sem_estudar(self):
        r = rodar(r"""
put("roteiro-sessions-v1", [{ t: NOW - DAY, id: "ia-0-0-0", sec: 300 }, { t: NOW - 3 * DAY, id: "ia-0-0-0", sec: 300 }]);
put("roteiro-review-v1", { "ia-0-0-1": { due: "2026-12-30", step: 2, hist: [[NOW - 2 * DAY, "f"]] } });   // revisão também conta
out.risco = AV.list(NOW, T).filter(a => a.grupo === "ritmo");
put("roteiro-sessions-v1", [{ t: NOW - DAY, id: "ia-0-0-0", sec: 300 }, { t: NOW - 3 * DAY, id: "ia-0-0-0", sec: 300 }, { t: NOW - 3600e3, id: "ia-0-0-0", sec: 60 }]);
out.hoje = AV.list(NOW, T).filter(a => a.grupo === "ritmo");
put("roteiro-sessions-v1", [{ t: NOW - 5 * DAY, id: "ia-0-0-0", sec: 300 }]); put("roteiro-review-v1", {});
out.parado = AV.list(NOW, T).filter(a => a.grupo === "ritmo");
""")
        self.assertEqual([(a["k"], a["n"]) for a in r["risco"]], [("seq", 3)])   # ontem + anteontem (revisão) + 3 dias atrás
        self.assertEqual(r["hoje"], [])                                         # já estudou hoje: sem aviso
        self.assertEqual([(a["k"], a["dias"]) for a in r["parado"]], [("parado", 5)])

    def test_ocultar_so_vale_para_o_que_nao_e_urgente(self):
        r = rodar(r"""
put("roteiro-ia-v1", { "ia-0-0-0": { s: "e" }, "ia-0-0-1": { s: "z", d: "2026-11-27" } });
const antes = AV.list(NOW, T);
antes.forEach(a => AV.hide(a.key, NOW));
out.depois = AV.list(NOW, T).map(a => a.k);
put("roteiro-ia-v1", { "ia-0-0-0": { s: "e" }, "ia-0-0-1": { s: "z", d: "2026-11-27" }, "ia-0-0-3": { s: "e" } });
out.novo = AV.list(NOW, T).map(a => a.k);    // mais uma aula sem quiz: o aviso volta
""")
        self.assertEqual(r["depois"], ["prazo"])
        self.assertEqual(sorted(r["novo"]), ["prazo", "quiz"])


class PaginasComAvisos(unittest.TestCase):
    def test_sino_em_todas_as_paginas(self):
        for nome in ("index.html", "ia.html", "matematica.html", "ingles.html", "projetos.html", "revisoes.html",
                     "Roteiro de Estudo_ do zero à IA.html"):
            s = ler(nome)
            direita = s[s.index('<div class="nav-right">'):s.index("</header>")]
            self.assertIn('id="av-bell"', direita, nome)
            self.assertIn('id="av-bell-badge"', direita, nome)
            fim_header = s.index("</header>")
            self.assertIn("avBellBadge()", s[fim_header:fim_header + 1500], nome)          # número certo antes da 1ª pintura
            self.assertLess(s.index("window.DS_TOPICS ="), s.index("try { avBoot(); }"), nome)   # avisos com os títulos
            self.assertLess(s.index("try { avBoot(); }"), s.index('<div id="ds-end"'), nome)

    def test_indice_sabe_quais_aulas_tem_quiz(self):
        idx = json_apos(ler("index.html"), "window.DS_TOPICS = ")
        tem = {r[0]: r[3] for r in idx}
        for tr, nome in PAGINAS.items():
            for tid, t in json_apos(ler(nome), "const TOPICS_MAP = ").items():
                g = t.get("pt_guide") or {}
                esperado = 1 if any(b.get("tipo") == "quiz" and b.get("perguntas") for b in g.get("blocos", [])) else 0
                self.assertEqual(tem[tid], esperado, tid)

    def test_hub_projetos_revisoes_e_trilhas(self):
        hub = ler("index.html")
        self.assertLess(hub.index('class="hub-hero'), hub.index('id="av-hoje"'))
        self.assertIn('cqRead("roteiro-review-v1", {})', hub)    # revisões contam como dia de estudo nas Conquistas
        proj = ler("projetos.html")
        for trecho in ("function onProjectDeadlineChange(", 'onchange="onProjectDeadlineChange(', 'class="proj-card" id="${p.id}"',
                       'new CustomEvent("av:change")'):
            self.assertIn(trecho, proj, trecho)
        self.assertIn('qs.get("dia")', ler("revisoes.html"))
        for nome in PAGINAS.values():
            self.assertIn('"⏰ prazo vencido"', ler(nome), nome)


if __name__ == "__main__":
    unittest.main()
