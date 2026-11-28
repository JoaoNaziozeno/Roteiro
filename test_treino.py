# -*- coding: utf-8 -*-
"""
Treino (questões de marcar). Confere:
  - os bancos de questões: cada questão de código roda no Python e o gabarito é o que aparece na tela;
  - os geradores de conta: sorteados muitas vezes no Node e refeitos aqui com o NumPy (outro caminho até a resposta);
  - o motor (sorteio, alternativas, gravação do resultado) e a revisão ativa com questões do treino;
  - as páginas GERADAS (cartão na aula, menu "⋯ Mais", treino misto na página Revisões, arquivos de deploy).

    python -X utf8 build_ecosystem.py
    python -X utf8 -m unittest test_treino
"""
import json
import re
import unittest
import zipfile
from pathlib import Path

import treino
from revisoes_page import RA_JS
from test_contadores import PAGINAS, funcao_js, json_apos, ler, node
from treino_checagem import CHECK, ORDEM_LIVRE, distinta, perto
from treino_js import TR_JS
from validate_lessons import check_latex

BASE = Path(__file__).resolve().parent
SEMENTES = 120


def fora_do_latex(s):
    return re.sub(r"\$[^$]*\$", "", s)


class Bancos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bancos = treino.carregar()

    def test_questoes_de_codigo_conferidas_no_python(self):
        probs = [p for banco in self.bancos.values() for titulo, qs in banco.items() for p in treino.conferir(qs, titulo)]
        self.assertEqual(probs, [])

    def test_toda_aula_do_piloto_tem_treino_variado(self):
        for tr, banco in self.bancos.items():
            for titulo, qs in banco.items():
                tipos = [q["k"] for q in qs]
                self.assertGreaterEqual(len(qs), 10, titulo)
                if tr == "ia":   # código: saída, completar e achar o erro em toda aula
                    for k in ("saida", "lacuna", "erro"):
                        self.assertIn(k, tipos, (titulo, k))
                else:            # contas com números novos em toda aula de Matemática
                    self.assertGreaterEqual(tipos.count("conta"), 3, titulo)
                    for q in qs:
                        if q["k"] == "conta":
                            self.assertIn(q["g"], CHECK, titulo)

    def test_latex_das_questoes_de_matematica(self):
        for titulo, qs in self.bancos["mat"].items():
            for q in qs:
                for s in treino.textos(q):
                    self.assertEqual(check_latex(s), [], (titulo, s[:60]))


class Geradores(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # cada gerador sem parâmetros e com cada parâmetro usado nos bancos de questões
        var = {}
        for banco in treino.carregar().values():
            for qs in banco.values():
                for q in qs:
                    if q["k"] == "conta" and q.get("p") and q["p"] not in var.setdefault(q["g"], []):
                        var[q["g"]].append(q["p"])
        cls.amostras = node(TR_JS + "\n" + treino.gen_js() + r"""
const VAR = __VAR__, out = [];
for (const g of Object.keys(TR.GEN)) for (let s = 0; s < __N__; s++) {
  for (const p of [{}].concat(VAR[g] || [])) {
    const it = TR.inst({ k: "conta", g, p }, TR.rng(s * 7919 + 13));
    out.push({ g, s, d: it.d, c: it.c, q: it.q, x: it.x, t: it.t, casas: it.casas == null ? 2 : it.casas,
               opts: it.opts.map(o => ({ v: o.v, h: o.h, ok: o.ok, why: o.why })) });
  }
}
console.log(JSON.stringify(out));
""".replace("__N__", str(SEMENTES)).replace("__VAR__", json.dumps(var)))

    def test_todo_gerador_tem_conferencia(self):
        self.assertEqual(sorted({a["g"] for a in self.amostras}), sorted(CHECK))

    def test_a_certa_bate_com_o_numpy_e_as_erradas_nao(self):
        for a in self.amostras:
            onde = (a["g"], a["s"])
            esperado = CHECK[a["g"]](a["d"])
            ops = a["opts"]
            self.assertEqual(len(ops), 4, onde)
            self.assertEqual(len({o["h"] for o in ops}), 4, onde)                 # nada repetido na tela
            self.assertEqual([i for i, o in enumerate(ops) if o.get("ok")], [a["c"]], onde)
            norm = (lambda v: sorted(v) if isinstance(v, list) else v) if a["g"] in ORDEM_LIVRE else (lambda v: v)
            self.assertTrue(perto(norm(ops[a["c"]]["v"]), esperado, a["casas"]), (onde, ops[a["c"]]["v"], esperado))
            for i, o in enumerate(ops):
                if i != a["c"] and o["v"] is not None:
                    self.assertTrue(distinta(norm(o["v"]), esperado, a["casas"]), (onde, "errada igual à certa", o["h"]))

    def test_textos_sem_lixo_e_latex_valido(self):
        for a in self.amostras:
            onde = (a["g"], a["s"])
            textos = [a["q"], a["x"]] + [o["h"] for o in a["opts"]] + [o["why"] for o in a["opts"]]
            for s in textos:
                self.assertNotRegex(s, r"undefined|NaN|Infinity|\[object", onde)
                self.assertEqual(s.count("$") % 2, 0, (onde, s))
                self.assertNotIn("{,}", fora_do_latex(s), (onde, s))     # vírgula decimal do LaTeX fora da fórmula
                self.assertEqual(check_latex(s), [], (onde, s))
            self.assertTrue(a["q"] and a["x"] and a["t"], onde)


MOTOR = r"""
const store = {};
const localStorage = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); } };
""" + TR_JS + "\n" + treino.gen_js() + "\nconst out = {};\n"


class Motor(unittest.TestCase):
    def test_sorteio_reveza_tipos_e_aulas(self):
        r = node(MOTOR + r"""
const qs = [];
["saida", "saida", "saida", "saida", "lacuna", "lacuna", "erro", "erro", "conceito", "conta"].forEach((k, i) => qs.push({ k, n: i }));
out.um = TR.pick(qs, 10, TR.rng(5)).map(q => q.k);
out.tres = TR.pick(qs, 3, TR.rng(9)).map(q => q.k);
const L = ["a", "b", "c"].map(id => ({ id, qs: qs.slice(0, 4).map(q => Object.assign({ id }, q)) }));
out.misto = TR.pickMixed(L, 6, TR.rng(2)).map(it => it.id);
// 10 aulas com saída, conta e conceito: o misto reveza os tipos também
const M = Array.from({ length: 10 }, (_, i) => ({ id: "m" + i, qs: [{ k: "saida" }, { k: "conta" }, { k: "conceito" }] }));
out.tipos = []; for (let s = 1; s <= 20; s++) { const c = {}; TR.pickMixed(M, 10, TR.rng(s)).forEach(it => { c[it.q.k] = (c[it.q.k] || 0) + 1; }); out.tipos.push(c); }
console.log(JSON.stringify(out));
""")
        self.assertEqual(sorted(r["um"]), sorted(["saida"] * 4 + ["lacuna"] * 2 + ["erro"] * 2 + ["conceito", "conta"]))
        self.assertEqual(len(set(r["um"][:5])), 5)               # a 1ª rodada passa por todos os tipos
        self.assertEqual(len(set(r["tres"])), 3)
        self.assertEqual(len(set(r["misto"][:3])), 3)             # as aulas se revezam
        self.assertEqual(sorted(r["misto"]), ["a", "a", "b", "b", "c", "c"])
        for c in r["tipos"]:
            self.assertEqual(sorted(c.values()), [3, 3, 4], c)

    def test_alternativas_embaralhadas_sem_perder_a_certa(self):
        r = node(MOTOR + r"""
const q = { k: "conceito", pergunta: "p", opcoes: ["A", "B", "C", "D"], correta: 2, porques: ["pa", "pb", "", "pd"], x: "x" };
out.v = []; for (let s = 1; s <= 30; s++) { const it = TR.inst(q, TR.rng(s)); out.v.push([it.opts.map(o => o.h).join(""), it.opts[it.c].h, it.opts.map(o => o.why).join("|")]); }
const e = TR.inst({ k: "erro", codigo: "a = 1\n\nprint(a +)", linha: 3, correcao: "print(a + 1)", x: "x" });
out.e = [e.lines.length, e.c, e.q];
out.fixa = TR.inst(Object.assign({}, q, { fixa: true }), TR.rng(3)).opts.map(o => o.h).join("");
console.log(JSON.stringify(out));
""")
        ordens = {v[0] for v in r["v"]}
        self.assertGreater(len(ordens), 5)                        # a ordem muda de um treino para outro
        for ordem, certa, porques in r["v"]:
            self.assertEqual(certa, "C")
            self.assertEqual(porques, "|".join({"A": "pa", "B": "pb", "C": "", "D": "pd"}[ch] for ch in ordem))
        self.assertEqual(r["e"][:2], [3, 2])
        self.assertIn("Em qual linha", r["e"][2])
        self.assertEqual(r["fixa"], "ABCD")

    def test_resultado_fica_nas_respostas_da_aula(self):
        r = node(MOTOR + r"""
store["roteiro-answers-v1"] = JSON.stringify({ "ia-0-0-1": { p: { "1": 2 }, c: {}, q: { "7": { s: [0, 1, 2], d: 1 } }, t: 5 } });
out.antes = TR.stats("ia-0-0-1");
out.r1 = TR.record("ia-0-0-1", 8, 10, 1000);
out.r2 = TR.record("ia-0-0-1", 6, 10, 2000);
out.a = JSON.parse(store["roteiro-answers-v1"])["ia-0-0-1"];
out.novo = TR.record("mat-0-0-0", 3, 4, 3000);
console.log(JSON.stringify(out));
""")
        self.assertIsNone(r["antes"])
        self.assertIsNone(r["r1"]["prev"])
        self.assertEqual(r["r2"]["prev"], {"b": 80, "s": "8/10", "n": 1, "l": 1000})
        self.assertEqual(r["a"]["tr"], {"b": 80, "s": "6/10", "n": 2, "l": 2000})   # o melhor continua 80%
        self.assertEqual((r["a"]["p"], r["a"]["q"], r["a"]["t"]), ({"1": 2}, {"7": {"s": [0, 1, 2], "d": 1}}, 2000))
        self.assertEqual(r["novo"]["cur"]["b"], 75)

    def test_rotulos_para_a_lista_de_erros(self):
        r = node(MOTOR + r"""
out.l = [TR.labelOf({ k: "saida", codigo: "\nimport numpy as np\nv = [1, 2]\nprint(v)" }), TR.labelOf({ k: "conta", g: "dot" }),
         TR.labelOf({ k: "erro", codigo: "x = 1\nprint(x" }), TR.labelOf({ k: "conceito", pergunta: "O que é <code>x</code>?", tema: "" }),
         TR.labelOf({ k: "lacuna", pergunta: "p", tema: "fatiamento" })];
out.a = [TR.answerOf({ k: "conceito", opcoes: ["a", "<b>b</b>"], correta: 1 }), TR.answerOf({ k: "erro", linha: 2, correcao: "  print(x)" }),
         TR.answerOf({ k: "conta", g: "dot" })];
console.log(JSON.stringify(out));
""")
        self.assertEqual(r["l"], ["Saída de v = [1, 2]", "Produto escalar", "Erro em x = 1", "O que é x?", "fatiamento"])
        self.assertEqual(r["a"], ["b", "linha 2: print(x)", ""])

    def test_revisao_ativa_usa_ate_2_questoes_do_treino(self):
        base = r"""
let seed = 3; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const deck = { c: [{ k: "mem", a: ["i"] }, { k: "arm", q: "e", a: "c" }, { k: "pen", q: "p", a: "r" },
  { k: "quiz", q: "q1", o: ["a", "b"], c: 0 }, { k: "quiz", q: "q2", o: ["a", "b"], c: 1 }, { k: "quiz", q: "q3", o: ["a", "b"], c: 0 },
  { k: "tr", q: { k: "conta", g: "dot" } }, { k: "tr", q: { k: "conta", g: "l2" } }, { k: "tr", q: { k: "conta", g: "det2" } }] };
const ks = []; for (let i = 0; i < 40; i++) ks.push(RA.pick(deck, rnd).map(c => c.k).join(","));
console.log(JSON.stringify({ ks, lab: RA.labelOf({ k: "tr", q: { k: "conta", g: "dot" } }) }));
"""
        com = node(MOTOR + RA_JS + base)
        for ks in com["ks"]:
            k = ks.split(",")
            self.assertEqual(k[0], "mem")
            self.assertEqual(k.count("tr"), 2)
            self.assertEqual(k.count("quiz") + k.count("tr"), 3)
        self.assertEqual(com["lab"], "Treino: Produto escalar")
        sem = node(RA_JS + base.replace("RA.labelOf({ k: \"tr\", q: { k: \"conta\", g: \"dot\" } })", "\"\""))
        for ks in sem["ks"]:                                       # sem o Treino na página, só o quiz
            self.assertEqual(ks.split(",").count("tr"), 0)
            self.assertEqual(ks.split(",").count("quiz"), 3)


class Paginas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bancos = treino.carregar()
        cls.mapas = {tr: json_apos(ler(nome), "const TOPICS_MAP = ") for tr, nome in PAGINAS.items()}
        cls.arquivos = {tr: json.loads((BASE / f"treino_{tr}.json").read_text(encoding="utf-8")) for tr in ("ia", "mat")}

    def test_arquivos_de_treino_sao_os_bancos_e_vao_para_o_deploy(self):
        nomes = zipfile.ZipFile(BASE / "roteiro_aws_deploy.zip").namelist()
        for tr, arq in self.arquivos.items():
            por_titulo = {self.mapas[tr][tid]["title"]: qs for tid, qs in arq.items()}
            self.assertEqual(por_titulo, self.bancos[tr])
            self.assertTrue((BASE / "dist_deploy" / f"treino_{tr}.json").exists())
            self.assertIn(f"treino_{tr}.json", nomes)

    def test_trilhas_sabem_quais_aulas_tem_treino(self):
        todas = {tid: len(qs) for arq in self.arquivos.values() for tid, qs in arq.items()}
        hub = json_apos(ler("index.html"), "RM.configure(")
        self.assertEqual(hub["treino"], sorted(todas))           # a Jornada sabe quais aulas têm treino (parte dos pontos)
        for tr in ("ia", "mat"):
            s = ler(PAGINAS[tr])
            indice = json_apos(s, "const TR_INDEX = ")
            self.assertEqual(indice, todas)        # o mesmo índice em todas as páginas com treino
            self.assertEqual(json_apos(s, "RM.configure(")["treino"], sorted(todas), tr)
            for tid in self.mapas[tr]:
                linha = s[s.index(f'id="more-{tid}"'):]
                linha = linha[:linha.index("</div>")]
                # "🏋️ Treinar" da lista abre a Aula Visual no treino (não há mais janela por cima da aula)
                self.assertEqual(f"trGoLesson('{tid}')" in linha, tid in indice, tid)
                if tid in indice:                  # o treino fica no fim da Aula Visual: toda aula com treino tem uma
                    self.assertIn("blocos", self.mapas[tr][tid]["pt_guide"] or {}, tid)
            ini = s.index("function renderPtGuideV2Body(")
            self.assertIn("trAulaHTML(topicId)", s[ini:s.index("\nfunction ", ini + 10)])
            ini = s.index("function lv2Init(")
            self.assertIn("trAulaInit(root)", s[ini:s.index("\nfunction ", ini + 10)])
            for nome in ("function trAulaHTML(", "function trAulaInit(", "function trGoLesson(", "function trQHTML(", 'const TR_PY_RE'):
                self.assertIn(nome, s, (tr, nome))
            for velho in ("trOpenLesson", "trEntryHTML", "tr-entry"):
                self.assertNotIn(velho, s, (tr, velho))
        self.assertNotIn("const TR_INDEX", ler("ingles.html"))   # Inglês ainda não tem banco de questões

    def test_rotulos_em_texto_puro(self):
        # O rótulo vai, em texto puro, para a lista "Para rever", a revisão ativa e o caderno: sem LaTeX cru
        # (só a Matemática usa LaTeX; na IA uma barra invertida é de verdade, como em C:\Users)
        qs = [q for arq in self.arquivos.values() for lista in arq.values() for q in lista]
        r = node(MOTOR + "const qs = " + json.dumps(qs) + ";\nconsole.log(JSON.stringify(qs.map(q => TR.labelOf(q))));")
        self.assertEqual(len(r), len(qs))
        mat = {json.dumps(q, sort_keys=True) for lista in self.arquivos["mat"].values() for q in lista}
        for q, rot in zip(qs, r):
            self.assertTrue(rot.strip(), q)
            if json.dumps(q, sort_keys=True) in mat:
                self.assertNotRegex(rot, r"\\[A-Za-z]|[{}]", rot)

    def test_bloco_do_treino_na_aula(self):
        s = ler(PAGINAS["mat"])
        tid = next(k for k in json_apos(s, "const TR_INDEX = ") if k.startswith("mat-"))
        js = (MOTOR + "const TR_INDEX = " + json.dumps({tid: 10, "x-1": 3}) + ";\n"
              + "const TR_COLOR = { ia: '--t-ia', mat: '--t-mat', ing: '--t-ing' };\n"
              + "function trTrack(id) { return String(id || '').split('-')[0]; }\n" + funcao_js(s, "trAulaHTML") + "\n"
              + f"console.log(JSON.stringify({{ a: trAulaHTML({json.dumps(tid)}), b: trAulaHTML('x-1'), c: trAulaHTML('nada') }}));")
        r = node(js)
        self.assertIn(f'class="tr-aula" data-tr="{tid}"', r["a"])
        self.assertIn("--tc:var(--t-mat)", r["a"])
        self.assertIn("10 questões de marcar, uma por vez", r["a"])
        for parte in ('class="tr-a-count"', 'class="tr-prog"', 'class="tr-a-pts" hidden', 'class="tr-a-body"'):
            self.assertIn(parte, r["a"])
        self.assertNotIn('role="dialog"', r["a"])                 # dentro da aula, sem janela
        self.assertIn("3 questões", r["b"])                       # banco menor que uma sessão
        self.assertEqual(r["c"], "")                              # aula sem treino: nada

    def test_revisoes_tem_treino_misto_e_revisao_ativa_com_treino(self):
        s = ler("revisoes.html")
        self.assertIn('id="rv-treino"', s)
        mods = json_apos(s, "const TR_MODS = ")
        # IA: a Fase 1 (16 aulas com treino); Matemática: os 5 módulos inteiros (44 aulas), na ordem do site
        self.assertEqual([(m["tr"], len(m["ids"])) for m in mods], [("ia", 16), ("mat", 4), ("mat", 11), ("mat", 9), ("mat", 14), ("mat", 6)])
        self.assertEqual(len({m["k"] for m in mods}), len(mods))
        for m, nome in zip(mods, ("Fundamentos de programação", "Fundamentos", "Álgebra Linear", "Cálculo", "Probabilidade", "Transformers")):
            self.assertIn(nome, m["nome"])
        for trecho in ("function rvpTreino(", "trOpenMixed(", "function raRenderTreino(", 'window.addEventListener("tr:change"'):
            self.assertIn(trecho, s, trecho)
        decks = json.loads((BASE / "revisao_cartoes.json").read_text(encoding="utf-8"))
        for tr, arq in self.arquivos.items():
            for tid, qs in arq.items():
                self.assertEqual([c["q"] for c in decks[tid]["c"] if c["k"] == "tr"], qs[:10], tid)


if __name__ == "__main__":
    unittest.main()
