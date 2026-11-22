# -*- coding: utf-8 -*-
"""
Visual enxuto das trilhas e do hub: o que saiu da vista continua a um toque. Lê as páginas GERADAS:

    python -X utf8 build_ecosystem.py
    python -X utf8 -m unittest test_visual
"""
import json
import re
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parent
PAGINAS = {"ia": "ia.html", "mat": "matematica.html", "ing": "ingles.html"}


class Visual(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pag = {tr: (BASE / nome).read_text(encoding="utf-8") for tr, nome in PAGINAS.items()}
        cls.hub = (BASE / "index.html").read_text(encoding="utf-8")
        cls.mapa, cls.linhas = {}, {}
        for tr, s in cls.pag.items():
            k = "const TOPICS_MAP = "
            cls.mapa[tr] = json.JSONDecoder().raw_decode(s[s.index(k) + len(k):])[0]
            corpo = s[:s.index("const TOPICS_MAP = ")]
            partes = re.split(r'(?=<div class="topic-row )', corpo)[1:]
            cls.linhas[tr] = {re.search(r'data-id="([^"]+)"', p).group(1): p for p in partes}

    def test_toda_aula_tem_linha(self):
        for tr in self.pag:
            self.assertEqual(list(self.linhas[tr]), list(self.mapa[tr]))

    def test_linha_tem_so_status_titulo_abrir_e_mais(self):
        for tr, linhas in self.linhas.items():
            for tid, linha in linhas.items():
                visivel = linha[:linha.index('<div class="topic-panel"')]
                self.assertEqual(re.findall(r'<button class="([^"]+)"', visivel), ["row-st", "row-play", "row-more"], tid)
                self.assertNotIn("<a ", visivel, tid)

    def test_tudo_que_saiu_da_vista_esta_no_mais(self):
        for tr, linhas in self.linhas.items():
            for tid, linha in linhas.items():
                t = self.mapa[tr][tid]
                painel = linha[linha.index(f'id="more-{tid}"'):]
                painel = painel[:painel.index("</div>")]
                esperado = [nome for nome, tem in (("video2", t["url2"]), ("guide", t["pt_guide"]),
                                                   ("doc", t["doc_url"]), ("notes", True)) if tem]
                self.assertEqual(re.findall(r'data-act="(\w+)"', painel), esperado, tid)
                if t["doc_url"]:
                    self.assertIn(f'href="{t["doc_url"]}"', painel, tid)
                if t["url2"]:
                    self.assertIn(f"openStudyModal('{tid}', false, 2)", painel, tid)

    def test_situacao_e_escolha_explicita(self):
        for tr, linhas in self.linhas.items():
            self.assertNotIn("cycleStatus", self.pag[tr])
            for tid, linha in linhas.items():
                self.assertEqual(re.findall(r'data-status="(\w)"', linha), ["z", "r", "e"], tid)

    def test_um_card_de_progresso_e_exportar_no_menu(self):
        for tr, s in self.pag.items():
            self.assertEqual(s.count('<section class="trail-summary"'), 1)
            for velho in ('class="pace-stat-card"', 'class="progress-card"', 'id="lvl-xp-txt"', 'class="pace-status-card'):
                self.assertNotIn(velho, s, tr)
            menu = s[s.index('<aside class="sidebar"'):s.index("</aside>")]
            self.assertIn("openExportFromMenu()", menu)

    def test_filtros_tem_nome_de_celular_e_de_computador(self):
        for tr, s in self.pag.items():
            for longo, curto in (("Do zero", "A fazer"), ("Em andamento", "Fazendo"), ("Concluídos", "Feitos"), ("Anotações", "Notas")):
                self.assertIn(f'<span class="fil-long">{longo}</span><span class="fil-short">{curto}</span>', s, tr)

    def test_fases_comecam_recolhidas(self):
        for tr, s in self.pag.items():
            n = len(re.findall(r'<div class="phase-card"', s))
            self.assertEqual(s.count('<details class="phase-about">'), n, tr)

    def test_etapa_da_aula_so_e_marcada_pelo_aluno(self):
        for tr, s in self.pag.items():
            ini = s.index("function checkPtGuideScrollAndVisibility(")
            corpo = s[ini:s.index("\nfunction ", ini + 10)]
            self.assertNotIn("guideCardsSeen[i] = true", corpo, tr)
            self.assertIn("togglePtStepRead(i)", corpo, tr)
            self.assertIn("function togglePtStepRead(", s, tr)
            self.assertIn("saved.gc", s, tr)

    def test_hub_sem_anel(self):
        self.assertNotIn("function cqRing", self.hub)
        self.assertIn("function cqCard", self.hub)


if __name__ == "__main__":
    unittest.main()
