# -*- coding: utf-8 -*-
"""
Aplica o cockpit 'A Jornada' no build_ecosystem.py. Rode na pasta do projeto:
    python apply_journey.py
Faz backup em build_ecosystem.py.bak. Depois rode `python build_ecosystem.py` para regenerar os HTMLs.
"""
import shutil, sys
from pathlib import Path

SRC = Path("build_ecosystem.py")
s = SRC.read_text(encoding="utf-8")

if "hub_journey" in s:
    sys.exit("Já aplicado (hub_journey encontrado). Nada a fazer.")

def cut(text, start_marker, end_marker, replacement):
    a = text.index(start_marker)
    b = text.index(end_marker, a)
    return text[:a] + replacement + text[b:]

shutil.copy(SRC, "build_ecosystem.py.bak")

# 1) import
s = s.replace("from projects_generator import generate_projects_page",
              "from projects_generator import generate_projects_page\n"
              "from hub_journey import JOURNEY_CSS, JOURNEY_HTML, JOURNEY_JS_A, JOURNEY_JS_B", 1)

# 2) HTML: troca o cockpit inteiro (da <section speedometer> até o comentário dos 4 cards)
s = cut(s, '<section class="speedometer-sect"', "<!-- OS 4 CARDS GRANDES DE REDIRECIONAMENTO -->",
        "__JOURNEY_HTML__\n\n  ")

# 3) JS: troca o bloco do cockpit (setCockpitView ... updateHubWhatIf ... setHubPace ...) e o calcAndPaint
s = cut(s, "function setCockpitView(viewKey)", "function loadData(){", "__JOURNEY_JS_A__\n\n")
s = cut(s, "function calcAndPaint(){", "function toggleTheme(){", "__JOURNEY_JS_B__\n\n")

# 4) substituições finais do template
old = '.replace("__HUB_CSS__", hub_css)'
assert old in s, "Não achei a cadeia .replace('__HUB_CSS__', hub_css)"
s = s.replace(old, '.replace("__HUB_CSS__", hub_css + JOURNEY_CSS)\n'
                   '        .replace("__JOURNEY_HTML__", JOURNEY_HTML)\n'
                   '        .replace("__JOURNEY_JS_A__", JOURNEY_JS_A)\n'
                   '        .replace("__JOURNEY_JS_B__", JOURNEY_JS_B)', 1)

SRC.write_text(s, encoding="utf-8")
print("OK. Backup: build_ecosystem.py.bak. Agora rode: python build_ecosystem.py")
