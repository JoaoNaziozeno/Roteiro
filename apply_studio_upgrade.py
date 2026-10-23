# -*- coding: utf-8 -*-
"""
Script de atualização do ecossistema:
1. Conecta ia_phases ao build_ia_data enriquecido com todas as aulas do Guanabara (173 tópicos);
2. Adiciona os estilos STUDIO_CSS em SHARED_CSS;
3. Atualiza generate_listing_page com:
   - Suporte a KaTeX e Markdown com Imagens/Gráficos;
   - Modal Unificado de Estudo (Player de Vídeo no topo + Anotações logo abaixo);
   - Progresso Automático com Toggle [ON/OFF] e avanço em tempo real de estudo;
   - Paleta de Símbolos Matemáticos e Templates LaTeX;
   - Estúdio Interativo de Vetores & Geometria 3D (Eixos X, Y, Z com rotação 360°, formas geométricas e cálculos em tempo real);
   - Lousa de Desenho de Formas Geométricas 2D com inserção em 1 clique na anotação;
   - Serialização de TOPICS_MAP para busca instantânea de metadados.
"""

import re
from build_ia_data import get_enriched_ia_phases
from studio_css import STUDIO_CSS
from studio_js import STUDIO_JS

def main():
    target_path = "/mnt/c/Users/joao1/Desktop/Roteiro/build_ecosystem.py"
    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Atualizar ia_phases import
    pos_ia = content.find("ia_phases = [")
    pos_mat = content.find("# 2. Dados de Matemática", pos_ia)
    assert pos_ia != -1 and pos_mat != -1, "ia_phases markers not found"

    new_ia_import = "from build_ia_data import get_enriched_ia_phases\nia_phases = get_enriched_ia_phases()\n\n# ---------------------------------------------------------------------------\n"
    content = content[:pos_ia] + new_ia_import + content[pos_mat:]

    # 2. Adicionar STUDIO_CSS no SHARED_CSS
    pos_shared = content.find('SHARED_CSS = """')
    assert pos_shared != -1, "SHARED_CSS not found"
    pos_shared_end = content.find('print("SHARED_CSS pronto.")', pos_shared)
    assert pos_shared_end != -1, "SHARED_CSS end not found"

    # Injetar STUDIO_CSS antes do fechamento das aspas de SHARED_CSS
    last_quotes = content.rfind('"""', pos_shared, pos_shared_end)
    content = content[:last_quotes] + "\n" + STUDIO_CSS + "\n" + content[last_quotes:]

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Passo 1 & 2 concluídos: ia_phases e SHARED_CSS atualizados!")

if __name__ == "__main__":
    main()
