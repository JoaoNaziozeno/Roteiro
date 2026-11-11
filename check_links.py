# -*- coding: utf-8 -*-
"""
Verifica se os vídeos do YouTube usados nas trilhas de IA, Matemática e Inglês ainda existem
e se podem ser tocados dentro do site (incorporação permitida).

Uso (na pasta do projeto):
    python check_links.py              -> lista os vídeos fora do ar (código de saída 1 se houver algum)
    python check_links.py --todos      -> mostra também canal e título de cada vídeo válido

Usa o endpoint público oEmbed do YouTube (não precisa de chave de API).
Rode antes de publicar: um vídeo apagado ou com ID corrompido aparece aqui.
"""
import concurrent.futures as cf
import json
import re
import sys
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCES = ["build_ia_data.py", "build_math_data.py", "math_lessons_pilot.py", "english_playlist.json"]
ID_RE = re.compile(r"(?:youtube\.com/watch\?v=|youtu\.be/|\"id\":\s*\"|'id':\s*'|\"videoId\":\s*\")([\w-]{11})")
PILOT_ID_RE = re.compile(r"\"id\":\s*\"([\w-]{11})\"")


def collect():
    found = {}
    for name in SOURCES:
        p = BASE / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for rx in (ID_RE, PILOT_ID_RE):
            for m in rx.finditer(text):
                found.setdefault(m.group(1), set()).add(name)
    return found


def check(vid):
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (roteiro-link-check)"})
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.load(r)
        return vid, True, f"{d.get('author_name', '')} | {d.get('title', '')}"
    except urllib.error.HTTPError as e:
        # 401/403 = existe mas o dono desativou a incorporação: no site aparece "Vídeo indisponível".
        # 404/400 = não existe (apagado, privado ou ID corrompido).
        return vid, False, f"HTTP {e.code}" + (" (incorporação desativada: não toca no site)" if e.code in (401, 403) else " (removido ou privado)")
    except Exception as e:  # rede fora, timeout...
        return vid, None, f"não verificado: {e}"


def main():
    show_all = "--todos" in sys.argv
    ids = collect()
    print(f"Verificando {len(ids)} vídeos únicos...")
    with cf.ThreadPoolExecutor(6) as ex:
        results = list(ex.map(check, ids))
    # Falhas de rede (sem resposta) ganham uma segunda tentativa, em sequência
    results = [check(r[0]) if r[1] is None else r for r in results]
    bad = [r for r in results if r[1] is False]
    unknown = [r for r in results if r[1] is None]
    for vid, ok, info in sorted(results, key=lambda r: (r[1] is not False, r[0])):
        if ok is False or ok is None or show_all:
            mark = "OK " if ok else ("?? " if ok is None else "XX ")
            print(f"  {mark}{vid}  {info}  [{', '.join(sorted(ids[vid]))}]")
    print(f"\nResultado: {len(results) - len(bad) - len(unknown)} ok, {len(bad)} fora do ar, {len(unknown)} sem verificação.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
