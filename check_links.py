# -*- coding: utf-8 -*-
"""
Verifica os vídeos do YouTube usados nas trilhas de IA, Matemática e Inglês:
  1. se ainda existem e podem ser tocados dentro do site (incorporação permitida);
  2. se cada par TÓPICO + VÍDEO já teve o título real conferido (videos_conferidos.json).
     Existir não basta: um vídeo no ar pode ser de outro assunto.

Uso (na pasta do projeto):
    python check_links.py                    -> problemas (código de saída 1 se houver algum)
    python check_links.py --todos            -> mostra também canal e título de cada vídeo válido
    python check_links.py --offline          -> só o item 2, sem internet
    python check_links.py --aprovar "trecho" -> depois de trocar um vídeo: mostra o título real dos vídeos ainda
                                                não conferidos dos tópicos com esse trecho e pede confirmação

Usa o endpoint público oEmbed do YouTube (não precisa de chave de API).
Rode antes de publicar: um vídeo apagado, com ID corrompido ou fora de conferência aparece aqui.
"""
import concurrent.futures as cf
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
MANIFESTO = BASE / "videos_conferidos.json"
SOURCES = ["build_ia_data.py", "build_math_data.py", "math_lessons_pilot.py", "ia_lessons_pilot.py",
           "english_lessons_pilot.py", "english_playlist.json"]
ID_RE = re.compile(r"(?:youtube\.com/watch\?v=|youtu\.be/|\"id\":\s*\"|'id':\s*'|\"videoId\":\s*\")([\w-]{11})")
PILOT_ID_RE = re.compile(r"\"id\":\s*\"([\w-]{11})\"")
URL_RE = re.compile(r"[?&](?:v|list)=([\w-]+)")


def pares():
    """{"trilha | título do tópico": [ids]} exatamente como as páginas são montadas (inclui playlists)."""
    from build_ia_data import get_enriched_ia_phases
    from build_math_data import get_enriched_mat_phases
    from en_m7_trabalho import MODULO_7
    ingles = json.loads((BASE / "english_playlist.json").read_text(encoding="utf-8"))
    trilhas = {"ia": get_enriched_ia_phases(), "mat": get_enriched_mat_phases(),
               "ing": [{"g": [["", ingles]]}, MODULO_7]}
    out = {}
    for tr, fases in trilhas.items():
        for fase in fases:
            for grupo in fase["g"]:
                for t in grupo[1]:
                    for campo in ("video_url", "video2_url", "url"):
                        m = URL_RE.search(t.get(campo) or "")
                        if m:
                            ids = out.setdefault(f"{tr} | {t['title']}", [])
                            if m.group(1) not in ids:
                                ids.append(m.group(1))
    return out


def conferidos():
    return json.loads(MANIFESTO.read_text(encoding="utf-8")) if MANIFESTO.exists() else {}


def sem_conferencia(atual, ok):
    return [(topico, vid) for topico, ids in atual.items() for vid in ids if vid not in ok.get(topico, {})]


def collect():
    found = {}
    extra = sorted(p.name for pat in ("ia_f*.py", "en_m*.py") for p in BASE.glob(pat))
    for name in SOURCES + extra:
        p = BASE / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for rx in (ID_RE, PILOT_ID_RE):
            for m in rx.finditer(text):
                found.setdefault(m.group(1), set()).add(name)
    return found


def check(vid):
    alvo = ("https://www.youtube.com/playlist?list=" if vid.startswith("PL") and len(vid) > 11
            else "https://www.youtube.com/watch?v=") + vid
    url = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(alvo, safe="")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (roteiro-link-check)"})
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.load(r)
        return vid, True, f"{d.get('author_name', '')} | {d.get('title', '')}"
    except urllib.error.HTTPError as e:
        # 401/403 = existe mas o dono desativou a incorporação: no site aparece "Vídeo indisponível".
        # 404/400 = não existe (apagado, privado ou ID corrompido).
        # 429/5xx = o YouTube não respondeu agora: não prova nada sobre o vídeo.
        if e.code == 429 or e.code >= 500:
            return vid, None, f"não verificado: HTTP {e.code}"
        return vid, False, f"HTTP {e.code}" + (" (incorporação desativada: não toca no site)" if e.code in (401, 403) else " (removido ou privado)")
    except Exception as e:  # rede fora, timeout...
        return vid, None, f"não verificado: {e}"


def aprovar(trecho):
    ok = conferidos()
    fila = [(t, v) for t, v in sem_conferencia(pares(), ok) if trecho.lower() in t.lower()]
    for topico, vid in fila:
        _, existe, info = check(vid)
        print(f"\nTópico: {topico}\nVídeo : {info}")
        if not existe:
            print("  não registrado.")
        elif input("O vídeo é desse assunto? (s/N) ").strip().lower() == "s":
            ok.setdefault(topico, {})[vid] = info
            MANIFESTO.write_text(json.dumps(ok, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
            print("  registrado.")
    if not fila:
        print("Nada pendente com esse trecho.")


def main():
    if "--aprovar" in sys.argv:
        i = sys.argv.index("--aprovar")
        return aprovar(sys.argv[i + 1] if len(sys.argv) > i + 1 else "")

    atual, ok = pares(), conferidos()
    pendentes = sem_conferencia(atual, ok)
    for topico, vid in pendentes:
        print(f"  XX {vid}  título não conferido para “{topico}” (use --aprovar)")
    print(f"Conferência de assunto: {sum(map(len, atual.values())) - len(pendentes)} ok, {len(pendentes)} sem conferência.")
    if "--offline" in sys.argv:
        sys.exit(1 if pendentes else 0)

    show_all = "--todos" in sys.argv
    ids = collect()
    for topico, vids in atual.items():
        for vid in vids:
            ids.setdefault(vid, set()).add(topico)
    print(f"Verificando {len(ids)} vídeos únicos...")
    with cf.ThreadPoolExecutor(4) as ex:
        results = list(ex.map(check, ids))
    # Falhas de rede (sem resposta) ganham uma segunda tentativa, em sequência; limite do YouTube (429) não
    results = [check(r[0]) if r[1] is None and "429" not in r[2] else r for r in results]
    bad = [r for r in results if r[1] is False]
    unknown = [r for r in results if r[1] is None]
    registrado = {v: info for d in ok.values() for v, info in d.items()}
    for vid, good, info in sorted(results, key=lambda r: (r[1] is not False, r[0])):
        if good is False or good is None or show_all:
            mark = "OK " if good else ("?? " if good is None else "XX ")
            print(f"  {mark}{vid}  {info}  [{', '.join(sorted(ids[vid]))}]")
        elif vid in registrado and registrado[vid].split(" | ", 1)[-1].strip() != info.split(" | ", 1)[-1].strip():
            print(f"  !!  {vid}  o título mudou desde a conferência: “{info}” (antes “{registrado[vid]}”)")
    print(f"\nResultado: {len(results) - len(bad) - len(unknown)} ok, {len(bad)} fora do ar, {len(unknown)} sem verificação.")
    sys.exit(1 if bad or pendentes else 0)


if __name__ == "__main__":
    main()
