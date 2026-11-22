# -*- coding: utf-8 -*-
"""
Todos os contadores de tópicos contam igual. Lê as páginas GERADAS, então rode depois do build:

    python -X utf8 build_ecosystem.py
    python -X utf8 -m unittest test_contadores

Regra única: o número principal é o de obrigatórios; os opcionais aparecem à parte.
Precisa do Node (já usado por test_metrics.js) para executar as funções das páginas.
"""
import json
import re
import subprocess
import unittest
from pathlib import Path

import curriculo

BASE = Path(__file__).resolve().parent
PAGINAS = {"ia": "ia.html", "mat": "matematica.html", "ing": "ingles.html"}


def ler(nome):
    return (BASE / nome).read_text(encoding="utf-8")


def json_apos(texto, marca):
    return json.JSONDecoder().raw_decode(texto[texto.index(marca) + len(marca):])[0]


def node(codigo):
    r = subprocess.run(["node", "-"], input=codigo, capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise AssertionError(r.stderr)
    return json.loads(r.stdout)


def funcao_js(texto, nome):
    """Código de uma função declarada na coluna 0 (termina no primeiro "}" também na coluna 0)."""
    return re.search(rf"^(?:async )?function {nome}\(.*?^\}}", texto, re.S | re.M).group(0)


class Contadores(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pag = {tr: ler(nome) for tr, nome in PAGINAS.items()}
        cls.hub = ler("index.html")
        cls.admin = ler("admin.html")
        cls.mapa = {tr: list(json_apos(s, "const TOPICS_MAP = ").values()) for tr, s in cls.pag.items()}
        cls.req = {tr: [t["id"] for t in ts if not t["opt"]] for tr, ts in cls.mapa.items()}
        cls.opt = {tr: [t["id"] for t in ts if t["opt"]] for tr, ts in cls.mapa.items()}

    def test_opcionais_sao_os_do_curriculo(self):
        self.assertEqual(sorted(i for ids in self.opt.values() for i in ids), sorted(o[0] for o in curriculo.OPTIONAL))

    def test_lateral_e_titulos_de_grupo(self):
        for tr, s in self.pag.items():
            grupos = {}
            for bloco in re.split(r'<div class="group-section" id="', s)[1:]:
                gid = bloco[:bloco.index('"')]
                linhas = re.findall(r'<div class="topic-row[^>]*>', bloco)
                opt = sum('data-opt="1"' in x for x in linhas)
                grupos[gid] = (len(linhas) - opt, opt)
                req_txt = re.search(r'class="group-title">[^<]*\((\d+)(?: \+ (\d+) opciona(?:l|is))?\)</div>', bloco)
                self.assertEqual((int(req_txt[1]), int(req_txt[2] or 0)), grupos[gid], f"{tr}: título de {gid}")
            soma = [0, 0]
            selo = r'<span class="sb-badge-count"[^>]*>(\d+)(?: <span class="cnt-opt">\+(\d+)</span>)?</span>'
            for fase in re.findall(r'<details class="sb-phase".*?</details>', s, re.S):
                numeros = [(int(a), int(b or 0)) for a, b in re.findall(selo, fase)]
                gids = re.findall(r"jumpToSub\('([^']+)'\)", fase)
                self.assertEqual(numeros[1:], [grupos[g] for g in gids], f"{tr}: subgrupos da lateral")
                esperado = (sum(grupos[g][0] for g in gids), sum(grupos[g][1] for g in gids))
                self.assertEqual(numeros[0], esperado, f"{tr}: fase na lateral")
                soma = [soma[0] + esperado[0], soma[1] + esperado[1]]
            self.assertEqual(soma, [len(self.req[tr]), len(self.opt[tr])], f"{tr}: soma das fases")

    def test_topo_e_filtro_todos(self):
        for tr, s in self.pag.items():
            r, o = len(self.req[tr]), len(self.opt[tr])
            extra = f" (+{o} opcionais)" if o else ""
            self.assertIn(f"<b>{r} tópicos</b>{extra} organizados", s)
            self.assertIn(f'title="Todos: {r + o}' + (f" ({r} + {o} opcionais)" if o else "") + '">Todos</button>', s)
            self.assertIn(f"const TOTAL_TRACK_TOPICS = {r};", s)

    def test_cartoes_do_hub(self):
        for tr, unidade in (("ia", "Tópicos"), ("mat", "Tópicos"), ("ing", "Aulas")):
            r, o = len(self.req[tr]), len(self.opt[tr])
            self.assertIn(f"{r} {unidade}" + (f" (+{o} opcionais)" if o else "") + " · ", self.hub)
        self.assertIn(f">{sum(map(len, self.mapa.values()))} Tópicos</span>", self.hub)

    def test_painel_de_ritmo_ignora_opcionais_e_ids_inexistentes(self):
        config = json_apos(self.hub, "RM.configure(")
        self.assertEqual(config["totals"], {tr: len(ids) for tr, ids in self.req.items()})
        self.assertEqual(sorted(config["required"]), sorted(i for ids in self.req.values() for i in ids))
        from metrics_js import METRICS_JS
        feitos = [i for t in self.mapa.values() for i in (x["id"] for x in t)] + ["ia-9-9-9", "mat-9-9-9"]
        r = node(METRICS_JS + f"RM.configure({json.dumps(config)});"
                 f"const p = Object.fromEntries({json.dumps(feitos)}.map(i => [i, {{s: 'e'}}]));"
                 "const x = RM.progress(p, {tracks: {}, topics: {}});"
                 "console.log(JSON.stringify(Object.fromEntries(Object.entries(x.per).map(([t, v]) => [t, v.done]))));")
        self.assertEqual(r, {tr: len(ids) for tr, ids in self.req.items()})

    def test_admin_conta_como_a_pagina_do_aluno(self):
        topicos = json_apos(self.admin, "const TOPICS = ")
        totais = re.search(r"^const TOTALS = .*$", self.admin, re.M).group(0)
        casos = {
            "tudo": [i for t in self.mapa.values() for i in (x["id"] for x in t)] + ["ia-9-9-9"],
            "obrigatorios": [i for ids in self.req.values() for i in ids],
            "opcionais": [i for ids in self.opt.values() for i in ids],
        }
        js = (f"const TOPICS = {json.dumps(topicos)};\n{totais}\n"
              + funcao_js(self.admin, "countTrail") + "\n" + funcao_js(self.admin, "countAll") + "\n"
              + f"const casos = {json.dumps(casos)}, out = {{TOTALS}};"
              "for (const c in casos) out[c] = countAll(Object.fromEntries(casos[c].map(i => [i, {s: 'e'}])));"
              "console.log(JSON.stringify(out));")
        r = node(js)
        self.assertEqual(r["TOTALS"], {tr: len(ids) for tr, ids in self.req.items()})
        for tr in self.mapa:
            n, o = len(self.req[tr]), len(self.opt[tr])
            self.assertEqual(r["tudo"][tr], {"done": n, "started": 0, "extra": o})
            self.assertEqual(r["obrigatorios"][tr], {"done": n, "started": 0, "extra": 0})
            self.assertEqual(r["opcionais"][tr], {"done": 0, "started": 0, "extra": o})

    def test_indice_das_conquistas(self):
        indice = json_apos(self.hub, "const CQ_INDEX = ")
        for tr, ids in self.req.items():
            blocos = {m: v for m, v in indice["modules"].items() if m.startswith(tr + "-")}
            self.assertEqual(sum(v[1] for v in blocos.values()), len(ids))
            fases = {m.rsplit("-", 1)[0] for m in blocos}
            self.assertEqual(len(fases), len(re.findall(r'<div class="phase-card"', self.pag[tr])))

    def test_mapa_da_jornada_recebe_o_primeiro_calculo(self):
        guarda = self.hub.index("window.__dsRouteData =")
        define = self.hub.index("window.dsRoute = function")
        rele = self.hub.index("if (window.__dsRouteData) window.dsRoute(")
        self.assertLess(guarda, define)
        self.assertLess(define, rele)

    def test_textos_sem_totais_velhos(self):
        n_playlist = len(json.loads(ler("english_playlist.json")))
        self.assertIn(f"As {n_playlist} vídeo-aulas da playlist oficial + {len(self.req['ing']) - n_playlist} de inglês",
                      self.pag["ing"])
        self.assertNotIn("6 módulos, 12 aulas", self.pag["ing"])
        for n in re.findall(r"\b(\d+) Aulas Visuais de Matemática", self.pag["mat"]):
            self.assertEqual(int(n), len(self.mapa["mat"]))


if __name__ == "__main__":
    unittest.main()
