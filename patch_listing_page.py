# -*- coding: utf-8 -*-
"""
Atualiza generate_listing_page em build_ecosystem.py com o gerador moderno e robusto.
"""
from listing_generator import build_listing_page_code

def main():
    target = "/mnt/c/Users/joao1/Desktop/Roteiro/build_ecosystem.py"
    with open(target, "r", encoding="utf-8") as f:
        content = f.read()

    pos1 = content.find("def generate_listing_page(")
    pos2 = content.find('print("Listing page generator pronto.")')
    assert pos1 != -1 and pos2 != -1, "Markers for generate_listing_page not found"

    new_code = build_listing_page_code().strip() + "\n\n"
    new_content = content[:pos1] + new_code + content[pos2:]

    with open(target, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("build_ecosystem.py atualizado com generate_listing_page com sucesso!")

if __name__ == "__main__":
    main()
