# -*- coding: utf-8 -*-
"""
Histórico de conclusões (roteiro-events-v1): a primeira mudança depois de abrir a página num navegador
limpo ganha data, e o progresso que vem da nuvem nunca vira "concluído agora". Lê as páginas GERADAS:

    python -X utf8 build_ecosystem.py
    python -X utf8 -m unittest test_eventos

Roda as funções reais da página no Node, com um localStorage falso.
"""
import json
import unittest

from test_contadores import funcao_js, ler, node

CENARIO = r"""
const store = {};
const localStorage = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = String(v); },
  removeItem: k => { delete store[k]; }
};
const window = {};
const KEY = "roteiro-ia-v1";
let PR = {};
%(funcs)s
const read = k => JSON.parse(localStorage.getItem(k) || "null");
const out = {};

// 1) Navegador limpo, sem nada: a primeira conclusão já vira evento com data
loadLocal();
PR["ia-0-0-0"] = { s: "e", n: "", d: "" };
diffAndLogEvents();
out.limpo = { eventos: read("roteiro-events-v1"), logStart: Boolean(localStorage.getItem("roteiro-log-start")) };

// 2) Página abriu vazia e a nuvem chegou depois (10 concluídos): só a mudança nova vira evento
for (const k in store) delete store[k];
PR = {};
loadLocal();
const nuvem = {};
for (let i = 0; i < 10; i++) nuvem["ia-1-0-" + i] = { s: "e", n: "", d: "" };
awsSetStatusSnapshot(nuvem);
PR = JSON.parse(JSON.stringify(nuvem));
PR["ia-0-0-1"] = { s: "e", n: "", d: "" };
diffAndLogEvents();
out.nuvemDepois = read("roteiro-events-v1");

// 3) A nuvem gravou antes de a página abrir (sem foto ainda): só a mudança nova vira evento
for (const k in store) delete store[k];
localStorage.setItem(KEY, JSON.stringify(nuvem));
PR = {};
loadLocal();
PR["ia-0-0-2"] = { s: "r", n: "", d: "" };
diffAndLogEvents();
out.nuvemAntes = read("roteiro-events-v1");

// 4) Já havia foto e histórico: nada muda no comportamento antigo
for (const k in store) delete store[k];
localStorage.setItem("roteiro-snap-v1", JSON.stringify({ "ia-0-0-0": "r" }));
localStorage.setItem("roteiro-events-v1", JSON.stringify([{ t: 1, id: "x", f: "z", to: "r", src: "ui" }]));
localStorage.setItem("roteiro-log-start", "123");
PR = { "ia-0-0-0": { s: "r", n: "", d: "" } };
loadLocal();
PR["ia-0-0-0"].s = "e";
diffAndLogEvents();
out.antigo = { eventos: read("roteiro-events-v1"), logStart: localStorage.getItem("roteiro-log-start") };

console.log(JSON.stringify(out));
"""


class PrimeiraConclusao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        s = ler("ia.html")
        funcs = "\n".join(funcao_js(s, n) for n in ("loadLocal", "statusSnapshot", "diffAndLogEvents", "awsSetStatusSnapshot"))
        cls.r = node(CENARIO % {"funcs": funcs})

    def eventos(self, lista):
        return [(e["id"], e["f"], e["to"]) for e in lista or []]

    def test_navegador_limpo_registra_a_primeira(self):
        self.assertEqual(self.eventos(self.r["limpo"]["eventos"]), [("ia-0-0-0", "z", "e")])
        self.assertTrue(self.r["limpo"]["logStart"])

    def test_nuvem_depois_de_abrir_nao_vira_conclusao(self):
        self.assertEqual(self.eventos(self.r["nuvemDepois"]), [("ia-0-0-1", "z", "e")])

    def test_nuvem_antes_de_abrir_nao_vira_conclusao(self):
        self.assertEqual(self.eventos(self.r["nuvemAntes"]), [("ia-0-0-2", "z", "r")])

    def test_quem_ja_tinha_historico_segue_igual(self):
        self.assertEqual(self.eventos(self.r["antigo"]["eventos"]), [("x", "z", "r"), ("ia-0-0-0", "r", "e")])
        self.assertEqual(self.r["antigo"]["logStart"], "123")

    def test_toda_gravacao_da_nuvem_atualiza_a_foto(self):
        s = ler("ia.html")
        pull = funcao_js(s, "awsRealtimePullFromDynamoDB")
        self.assertIn("awsSetStatusSnapshot(fresh)", pull)
        self.assertIn("awsSetStatusSnapshot(merged)", pull)
        self.assertIn("awsSetStatusSnapshot(cur)", funcao_js(s, "awsRealtimePushToDynamoDB"))
        for pagina in ("index.html", "matematica.html", "ingles.html", "projetos.html"):
            self.assertIn("function awsSetStatusSnapshot(", ler(pagina), pagina)


if __name__ == "__main__":
    unittest.main()
