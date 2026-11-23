# -*- coding: utf-8 -*-
"""
Gerador de Páginas de Listagem com Estúdio Unificado de Estudo,
Auto-Progresso, KaTeX, Estúdio 3D de Vetores e Lousa de Desenho 2D.
"""

import html as html_lib
import json
import re
import curriculo
from listing_css import LISTING_CSS
from studio_js import STUDIO_JS
from favicon import FAVICON_LINK
from auth_aws_sync import AUTH_GUARD_HEAD_SCRIPT, AUTH_AWS_SYNC_CSS, CHANGE_CREDENTIALS_MODAL_HTML, AUTH_AWS_SYNC_JS

def _list_title(title):
    """Nome na lista. Na playlist de Inglês, "Curso de Inglês - Módulo 01" se repete em 73 linhas e o módulo já é
    o título da seção: fica "Aula 01 · assunto". O nome completo continua no estúdio e na busca."""
    title = title.replace("\\u0026", "&amp;")   # a playlist traz esse escape como texto
    m = re.match(r"Curso de Inglês - Módulo \d+ Aula (\d+)\s*[:\-]?\s*(.+)$", title)
    if m:
        return f"Aula {int(m.group(1)):02d} · {m.group(2)}"
    return "Aula Zero" if re.fullmatch(r"Curso de Inglês GRÁTIS - Aula Zero", title) else title


def _count_badge(topics):
    req, opt = curriculo.split_count(topics)
    if not opt:
        return f'<span class="sb-badge-count">{req}</span>'
    return (f'<span class="sb-badge-count" title="{req} obrigatórios + {opt} opcionais">'
            f'{req} <span class="cnt-opt">+{opt}</span></span>')


def _count_title(topics):
    req, opt = curriculo.split_count(topics)
    if not opt:
        return str(req)
    return f"{req} + {opt} {'opcional' if opt == 1 else 'opcionais'}"


def generate_listing_page(track_id, page_title, page_sub, track_icon, phases, out_path, shared_css="", is_english=False):
    total_topics = 0      # só obrigatórios (meta e percentuais)
    all_topics = 0        # todos, inclusive opcionais (filtro "Todos")
    phase_items = []
    topics_map = {}

    for p_idx, p in enumerate(phases):
        p_title = p["t"]
        p_dur = p["d"]
        p_tip = p["tip"]
        p_proj = p["p"]
        p_res = p["r"]
        groups_data = []

        for g_idx, g in enumerate(p["g"]):
            g_name = g[0]
            topics_list = []

            for t_idx, raw_t in enumerate(g[1]):
                topic_id = curriculo.topic_id(raw_t, track_id, p_idx, g_idx, t_idx)
                is_opt = curriculo.is_optional(raw_t)
                all_topics += 1
                if not is_opt:
                    total_topics += 1

                topic_title = ""
                yt_url = ""
                yt_label = "▶ Vídeo" if not is_english else "▶ EnglishBay"
                doc_url = ""
                doc_label = "📖 Material"

                pt_guide = None
                yt_pt_url = ""
                yt2_url = ""
                yt2_label = ""

                if isinstance(raw_t, dict):
                    topic_title = raw_t.get("title", "")
                    yt_url = raw_t.get("video_url") or raw_t.get("url") or ""
                    yt_label = raw_t.get("video_label") or ("▶ YouTube" if is_english else "▶ Vídeo")
                    yt2_url = raw_t.get("video2_url") or ""
                    yt2_label = raw_t.get("video2_label") or "🎬 2ª Opção de Vídeo"
                    doc_url = raw_t.get("doc_url") or ""
                    doc_label = raw_t.get("doc_label") or "📖 Material"
                    pt_guide = raw_t.get("pt_guide")
                    yt_pt_url = raw_t.get("yt_pt_url") or ""
                elif isinstance(raw_t, str) and "||" in raw_t:
                    parts = raw_t.split("||", 1)
                    topic_title = parts[0]
                    yt_url = parts[1]
                else:
                    topic_title = str(raw_t)

                t_dict = {
                    "id": topic_id,
                    "title": topic_title,
                    "url": yt_url,
                    "label": yt_label,
                    "url2": yt2_url,
                    "label2": yt2_label,
                    "doc_url": doc_url,
                    "doc_label": doc_label,
                    "pt_guide": pt_guide,
                    "yt_pt_url": yt_pt_url,
                    "opt": is_opt,
                    "opt_note": raw_t.get("opt_note", "") if isinstance(raw_t, dict) else ""
                }
                topics_list.append(t_dict)
                topics_map[topic_id] = t_dict

            groups_data.append({
                "name": g_name,
                "id": f"sec-{p_idx}-{g_idx}",
                "topics": topics_list
            })

        phase_items.append({
            "idx": p_idx,
            "title": p_title,
            "dur": p_dur,
            "tip": p_tip,
            "proj": p_proj,
            "res": p_res,
            "groups": groups_data
        })

    # Sidebar Tree HTML
    sidebar_tree_html = []
    for p in phase_items:
        p_topics = [t for g in p["groups"] for t in g["topics"]]
        sub_btns = []
        for g in p["groups"]:
            sub_btns.append(f"""
            <button class="sb-sub-btn" onclick="jumpToSub('{g['id']}')">
              <span>{g['name']}</span>
              {_count_badge(g['topics'])}
            </button>
            """)

        sidebar_tree_html.append(f"""
        <details class="sb-phase" open>
          <summary>
            <span class="sb-phase-title">📁 {p['title'].split('·')[0].strip()}</span>
            {_count_badge(p_topics)}
          </summary>
          <div class="sb-sub-list">
            {''.join(sub_btns)}
          </div>
        </details>
        """)
    sb_tree_str = "\n".join(sidebar_tree_html)

    # Conteúdo das Fases HTML
    phases_content_html = []
    for p in phase_items:
        groups_html = []
        for g in p["groups"]:
            topics_rows = []
            for t in g["topics"]:
                t_id = t["id"]
                t_short = _list_title(t["title"])
                t_name = html_lib.escape(html_lib.unescape(t_short))
                doc_lbl = (t.get("doc_label") or "").replace("📘 Aula Visual PT-BR:", "📖 Artigo:").replace("📘 Aula Visual:", "📖 Artigo:").replace(" PT-BR", "")

                options = []
                if t.get("url2"):
                    t2_lbl = html_lib.escape(t.get("label2") or "2º vídeo")
                    options.append(f'<button class="row-opt" data-act="video2" title="{t2_lbl}" onclick="openStudyModal(\'{t_id}\', false, 2)">2º vídeo</button>')
                if t.get("pt_guide"):
                    options.append(f'<button class="row-opt" data-act="guide" onclick="openStudyModal(\'{t_id}\', true, 1)">Aula Visual</button>')
                if t.get("doc_url"):
                    doc_name = "Documentação" if track_id == "ia" else "Material de apoio"
                    options.append(f'<a class="row-opt" data-act="doc" href="{t["doc_url"]}" target="_blank" rel="noopener" title="{html_lib.escape(doc_lbl)}">{doc_name} ↗</a>')
                options.append(f'<button class="row-opt" data-act="notes" onclick="openTopicNotes(\'{t_id}\')">Anotações</button>')
                # Revisão é uma marca à parte: não muda a situação da aula nem os contadores
                options.append(f'<button class="row-opt" data-act="review" aria-pressed="false" onclick="toggleTopicReview(\'{t_id}\')">↻ Revisar</button>')

                # A bolinha não gira o status sozinha: voltar a "Do zero" apaga o % de vídeo e de aula, então é escolha explícita
                status_options = "".join(
                    f'<button class="row-opt" data-status="{code}" aria-pressed="false" onclick="chooseTopicStatus(\'{t_id}\', \'{code}\')">{name}</button>'
                    for code, name in (("z", "Do zero"), ("r", "Em andamento"), ("e", "Concluído")))

                # A busca continua achando pelo nome do vídeo e do material, que saíram da vista
                search_text = html_lib.escape(" ".join(x for x in (t["title"] if t_short != t["title"] else "", t.get("label"), t.get("label2") if t.get("url2") else "", doc_lbl) if x))
                play_title = html_lib.escape(t.get("label") or "Abrir a aula")
                opt_attr = ' data-opt="1"' if t.get("opt") else ""
                opt_class = " topic-optional" if t.get("opt") else ""
                opt_badge = f'<span class="opt-badge" title="{html_lib.escape(t.get("opt_note", ""))}">Opcional</span>' if t.get("opt") else ""

                topics_rows.append(f"""
                <div class="topic-row status-z{opt_class}" data-id="{t_id}" id="top-{t_id}"{opt_attr} data-search="{search_text}">
                  <button class="row-st" onclick="toggleRowPanel('{t_id}', 'status')" aria-expanded="false" aria-controls="status-{t_id}" aria-label="Situação de {t_name}: Do zero" title="Mudar a situação"><i aria-hidden="true"></i></button>
                  <div class="topic-left" onclick="openStudyModal('{t_id}', false, 1)">
                    <span class="topic-title-text">{t_short}</span>{opt_badge}<span class="row-meta"></span>
                  </div>
                  <button class="row-play" onclick="openStudyModal('{t_id}', false, 1)" aria-label="Abrir a aula {t_name}" title="{play_title}">▶</button>
                  <button class="row-more" onclick="toggleRowPanel('{t_id}', 'more')" aria-expanded="false" aria-controls="more-{t_id}" aria-label="Mais opções de {t_name}" title="Mais opções">⋯</button>
                  <div class="topic-panel" id="status-{t_id}" hidden>{status_options}</div>
                  <div class="topic-panel" id="more-{t_id}" hidden>{''.join(options)}</div>
                </div>
                """)

            groups_html.append(f"""
            <div class="group-section" id="{g['id']}">
              <div class="group-title">📌 {g['name']} ({_count_title(g['topics'])})</div>
              <div class="group-topics">
                {''.join(topics_rows)}
              </div>
            </div>
            """)

        phases_content_html.append(f"""
        <div class="phase-card" id="phase-{p['idx']}">
          <div class="phase-head" onclick="togglePhaseCollapse({p['idx']})">
            <span class="phase-title-text">⚡ {p['title']}</span>
            <span class="phase-dur">⏱️ {p['dur']}</span>
          </div>
          <div class="phase-body" id="phase-body-{p['idx']}">
            <details class="phase-about">
              <summary>Sobre {'esta fase' if track_id == 'ia' else 'este módulo'}: dica, projeto e recursos</summary>
              <div class="phase-callout callout-tip">{p['tip']}</div>
              <div class="phase-callout callout-proj">🎯 <b>Projeto Prático:</b> {p['proj']}</div>
              <div class="phase-callout callout-res">📚 <b>Recursos Sugeridos:</b> {p['res']}</div>
            </details>
            {''.join(groups_html)}
          </div>
        </div>
        """)
    phases_str = "\n".join(phases_content_html)

    active_hub = ""
    active_ia = "active" if track_id == "ia" else ""
    active_mat = "active" if track_id == "mat" else ""
    active_ing = "active" if track_id == "ing" else ""

    topics_map_json = json.dumps(topics_map, ensure_ascii=False)

    template = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>__PAGE_TITLE__ - Roteiro de IA</title>
__FAVICON__
__AUTH_GUARD__
<!-- KaTeX Math Typesetting -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
<style>
__SHARED_CSS__
__AUTH_AWS_CSS__
__LISTING_CSS__
</style>
</head>
<body>

<!-- TOPBAR FIXA -->
<header class="top-nav">
  <div class="top-nav-inner">
    <a href="index.html" class="nav-brand">🚀 <span>Roteiro IA</span></a>
    <nav class="nav-links">
      <a href="index.html" class="nav-link __ACTIVE_HUB__">🏠 Hub Central</a>
      <a href="ia.html" class="nav-link __ACTIVE_IA__">🤖 IA & Código</a>
      <a href="matematica.html" class="nav-link __ACTIVE_MAT__">📐 Matemática</a>
      <a href="ingles.html" class="nav-link __ACTIVE_ING__">🇺🇸 Inglês EnglishBay</a>
      <a href="projetos.html" class="nav-link">🛠️ Projetos & Portfólio</a>
    </nav>
    <div class="nav-right">
      <div class="nav-user-dropdown-wrap" id="nav-user-wrap">
        <button class="nav-user-pill" onclick="toggleUserDropdown(event)" id="nav-auth-user" title="Menu da Conta">
          👤 <span>Minha conta</span> <span style="font-size:.7rem;margin-left:2px">▾</span>
        </button>
        <div class="nav-user-dropdown" id="nav-user-dropdown" hidden style="display:none">
          <div class="dropdown-user-header">
            <div class="dropdown-user-name" id="dropdown-user-name">Minha conta</div>
            <div class="dropdown-user-email" id="dropdown-user-email"></div>
          </div>
          <button class="dropdown-item" onclick="openChangeCredentialsModal()">
            <span>🔑</span>
            <span>Meu perfil e senha</span>
          </button>
          <div class="dropdown-divider"></div>
          <button class="dropdown-item danger" onclick="handleUserLogout()">
            <span>🔒</span>
            <span>Sair da Conta</span>
          </button>
        </div>
      </div>
      <span id="nav-db-status" class="nav-status-pill">💾 Local</span>
      <button class="nav-theme-btn" onclick="toggleTheme()" title="Alternar tema claro/escuro">🌓</button>
    </div>
  </div>
</header>

<div class="layout">
  <!-- SIDEBAR DE NAVEGAÇÃO RÁPIDA -->
  <aside class="sidebar" id="sidebar">
    <div class="sb-header">
      <span class="sb-header-title">__TRACK_ICON__ __PAGE_TITLE__</span>
      <button class="sb-icon-btn" onclick="toggleSidebar()" title="Fechar menu">✕</button>
    </div>

    <div class="sb-shortcuts">
      <button class="sb-quick-btn" onclick="window.scrollTo({top:0,behavior:'smooth'})">⬆ Ir ao Topo</button>
      <button class="sb-quick-btn" onclick="scrollToNextStep()">🎯 Pular para Próximo Passo</button>
      <button class="sb-quick-btn" onclick="setFilter('all')">👁️ Mostrar Todos</button>
      <button class="sb-quick-btn" id="sb-export" onclick="openExportFromMenu()" title="Exportar Caderno em Markdown, PDF ou JSON">📥 Exportar Caderno</button>
    </div>

    <div style="font-size:.76rem;font-weight:750;text-transform:uppercase;color:var(--mu);margin-top:6px;letter-spacing:.04em">
      Índice & Navegação Rápida
    </div>

    <div class="sb-tree">
      __SIDEBAR_TREE__
    </div>
  </aside>

  <div class="sb-backdrop" id="sb-backdrop" onclick="toggleSidebar()"></div>

  <!-- CONTEÚDO PRINCIPAL -->
  <div class="content-wrapper">
    <main>
      <div class="hero-head">
        <h1>__TRACK_ICON__ __PAGE_TITLE__</h1>
      </div>

      <!-- RESUMO DA TRILHA: um card só -->
      <section class="trail-summary" id="trail-summary">
        <div class="sum-line">
          <b id="stat-done">0</b>
          <span>de __TOTAL_TOPICS__ concluídos<span id="stat-extra"></span></span>
          <span id="prog-pct-label">0%</span>
        </div>
        <div class="prog-bar" aria-hidden="true">
          <div class="p-e" id="bar-e" style="width:0%"></div>
          <div class="p-r" id="bar-r" style="width:0%"></div>
        </div>
        <div class="sum-next">
          <div class="sum-next-info">
            <span class="next-step-tag" id="next-step-tag">Próxima aula</span>
            <span class="next-step-title" id="next-step-title">Começar pelo primeiro tópico da trilha</span>
          </div>
          <button class="next-step-btn" id="next-step-btn" onclick="continueStudy()">Continuar</button>
        </div>
        <details class="sum-more">
          <summary>Nível e ritmo de estudo</summary>
          <div class="level-info">
            <div class="level-icon" id="lvl-icon">🌱</div>
            <div>
              <div class="level-name" id="lvl-name">Iniciante Curioso</div>
              <div class="level-desc" id="lvl-desc">Iniciando os primeiros passos da jornada.</div>
            </div>
          </div>
          <div class="tracker-presets">
            <button class="trk-btn active" id="btn-pace-std" onclick="setPace('std')">Equilibrado (8-10h/sem)</button>
            <button class="trk-btn" id="btn-pace-acc" onclick="setPace('acc')">Acelerado (20-25h/sem)</button>
          </div>
          <p class="sub">__PAGE_SUB__ · <b>__TOTAL_TOPICS__ tópicos</b>__EXTRA_TOPICS__ organizados para domínio completo.</p>
        </details>
      </section>

      <section class="filter-row">
        <div class="filters">
          <button class="fil-btn active" data-f="all" onclick="setFilter('all')" title="Todos: __ALL_LABEL__">Todos</button>
          <button class="fil-btn" data-f="z" onclick="setFilter('z')"><span class="fil-long">Do zero</span><span class="fil-short">A fazer</span></button>
          <button class="fil-btn" data-f="r" onclick="setFilter('r')"><span class="fil-long">Em andamento</span><span class="fil-short">Fazendo</span></button>
          <button class="fil-btn" data-f="e" onclick="setFilter('e')"><span class="fil-long">Concluídos</span><span class="fil-short">Feitos</span></button>
          <button class="fil-btn" data-f="n" onclick="setFilter('n')"><span class="fil-long">Anotações</span><span class="fil-short">Notas</span></button>
          <button class="fil-btn" data-f="v" onclick="setFilter('v')"><span class="fil-long">↻ Revisar</span><span class="fil-short">Revisar</span></button>
        </div>
        <input type="search" class="search-input" id="search-box" placeholder="🔍 Filtrar tópicos..." oninput="onSearchInput(this.value)">
      </section>

      <!-- LISTAGEM DE FASES -->
      <div id="phases-container">
        __PHASES_CONTENT__
      </div>
    </main>
  </div>
</div>

<button class="sb-toggle-btn" onclick="toggleSidebar()">☰ Menu & Tópicos</button>

<!-- ========================================================================= -->
<!-- MODAL DO ESTÚDIO UNIFICADO DE ESTUDO & CADERNO DE ANOTAÇÕES               -->
<!-- ========================================================================= -->
<div id="note-modal" class="note-modal-overlay" hidden>
  <div class="note-modal-box unified-study-box">
    
    <!-- 1. CABEÇALHO DO ESTÚDIO DE ESTUDO -->
    <div class="note-modal-header">
      <div class="note-header-left">
        <div class="note-breadcrumb" id="modal-breadcrumb">__MODAL_TRACK_NAME__</div>
        <h2 class="note-topic-title" id="modal-topic-title">Título do Tópico</h2>
      </div>
      <div class="note-header-right">
        <!-- STATUS MANUAL -->
        <div class="note-status-wrap">
          <button class="note-status-pill" id="modal-status-btn" data-s="z" onclick="toggleModalTopicStatus()" title="Clique para alternar: Do zero → Em andamento → Concluído">Do zero</button>
          <button type="button" class="note-review-pill" id="modal-review-btn" aria-pressed="false" onclick="toggleTopicReview(CURRENT_MODAL_TOPIC_ID)" title="Colocar esta aula na lista de revisão (a situação não muda)"><span aria-hidden="true">↻</span><span class="rv-txt">Revisar</span></button>
        </div>

        <!-- OPÇÕES DA AULA: progresso automático e meta de data -->
        <details class="m-opts" id="modal-opts">
          <summary class="m-icon-btn" title="Opções da aula" aria-label="Opções da aula">
            <svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="3" cy="8" r="1.4"/><circle cx="8" cy="8" r="1.4"/><circle cx="13" cy="8" r="1.4"/></svg>
          </summary>
          <div class="m-opts-menu">
            <label class="auto-prog-wrap" title="Atualiza o status para 'Em andamento' e 'Concluído' conforme seu tempo de estudo no vídeo e na leitura">
              <span class="m-opts-text"><b>Progresso automático</b><small>Atualiza o status pelo tempo de estudo</small></span>
              <span class="switch">
                <input type="checkbox" id="modal-auto-prog-check" onchange="toggleAutoProgress(this.checked)">
                <span class="slider"></span>
              </span>
            </label>
            <div class="note-date-wrap">
              <label for="modal-date-input" class="m-opts-text"><b>Meta de conclusão</b><small>Data em que quer terminar esta aula</small></label>
              <input type="date" id="modal-date-input" onchange="onModalDateChange()">
            </div>
          </div>
        </details>

        <!-- PRÓXIMA AULA -->
        <button type="button" class="note-next-btn" id="modal-next-btn" onclick="goToNextLesson()" title="Salvar e abrir a próxima aula da trilha">Próxima aula <span aria-hidden="true">→</span></button>

        <button class="note-close-btn m-icon-btn" onclick="closeNoteModal()" title="Fechar (Esc)" aria-label="Fechar estúdio">
          <svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" fill="none"/></svg>
        </button>
      </div>
    </div>

    <!-- 2. CORPO DO ESTÚDIO: DIVIDIDO LADO A LADO (VÍDEO À ESQUERDA | ANOTAÇÕES À DIREITA) -->
    <div class="study-columns-layout" id="study-columns-layout">

      <!-- COLUNA DA ESQUERDA: VÍDEO, MATERIAIS & SESSÃO DE ESTUDO -->
      <div class="study-player-col" id="study-player-sect">
        <div class="study-player-topbar">
          <div class="player-topbar-info">
            <span class="player-source-tag" id="modal-player-tag">Vídeo</span>
            <div id="modal-video-switcher-wrap" class="video-segmented-switcher" style="display:none">
              <button type="button" id="modal-video-opt1-btn" class="video-seg-btn active" onclick="switchModalVideoOption(1)" title="Opção 1: Aula Principal">1. Principal</button>
              <button type="button" id="modal-video-opt2-btn" class="video-seg-btn" onclick="switchModalVideoOption(2)" title="Opção 2: Vídeo Complementar">2. Complementar</button>
            </div>
            <span class="player-source-title" id="modal-player-title">Material de Estudo</span>
          </div>
          <div class="player-topbar-actions">
            <a href="#" target="_blank" rel="noopener" id="modal-doc-link" class="player-ext-btn doc-ext" style="display:none" title="Abrir artigo ou material oficial da aula">Fonte Oficial ↗</a>
          </div>
        </div>

        <!-- CONTAINER DO IFRAME DO VÍDEO -->
        <div class="video-responsive-wrap" id="video-wrapper">
          <iframe id="modal-video-iframe" src="" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
        </div>

        <!-- BARRA DE PROGRESSO DA SESSÃO / VALIDAÇÃO REAL DE ESTUDO -->
        <div class="session-progress-bar-wrap" id="session-progress-wrap">
          <div class="session-progress-info">
            <div class="session-meta">
              <span id="session-progress-text" class="session-time">Sessão 00:00</span>
              <button type="button" id="session-video-pill" class="session-chip" onclick="toggleManualVideoValidated()" title="Progresso do vídeo. Assistiu pelo YouTube? Clique para validar.">Vídeo 0%</button>
              <button type="button" id="session-guide-pill" class="session-chip" onclick="scrollOrValidatePtGuide()" style="display:none" title="Progresso da aula visual: etapas que você marcou como lidas e tempo de leitura">Aula 0%</button>
            </div>
            <div class="session-end">
              <span id="session-progress-pct" class="session-pct">0%</span>
              <button class="session-finish-btn" onclick="markTopicCompleteNow()" title="Marcar este tópico como concluído agora">Concluir</button>
            </div>
          </div>
          <div class="session-bar-track">
            <div class="session-bar-fill" id="session-bar-fill" style="width:0%"></div>
          </div>
        </div>

        <!-- PAINEL EXTRA DE CONTEXTO E APOSTILA INTERATIVA -->
        <div class="study-left-extra-info" id="study-left-extra-info">
          <div id="modal-pt-guide-container"></div>
          <div class="study-left-card" id="modal-default-tip-card">
            <div class="study-left-card-title">Como estudar esta aula</div>
            <p>Assista ao vídeo, pause nos momentos-chave e registre no caderno o que entendeu com suas palavras. Use <b>Fórmulas</b> para escrever matemática e <b>3D</b> para enxergar vetores no espaço.</p>
          </div>
        </div>
      </div>

      <!-- BARRA DIVISÓRIA ARRASTÁVEL ENTRE VÍDEO E ANOTAÇÕES -->
      <div class="study-split-resizer" id="study-split-resizer" title="Arraste para redimensionar vídeo e caderno (Duplo clique para 50% / 50%)">
        <div class="resizer-handle"></div>
      </div>

      <!-- COLUNA DA DIREITA: AULA VISUAL (quando o tópico tem) ou CADERNO DE ANOTAÇÕES.
           arrangeStudyColumns() move os painéis: com Aula Visual, o caderno desce para baixo do vídeo. -->
      <div class="study-notes-col" id="study-notes-col">
       <div class="study-notes-panel" id="study-notes-panel">
        <div class="notes-section-head">
          <div class="notes-head-title">
            <span>Caderno</span>
          </div>
          <div class="toolbar-modes">
            <button class="tb-mode-btn" data-mode="split" onclick="setNoteViewMode('split')">Lado a lado</button>
            <button class="tb-mode-btn active" data-mode="editor" onclick="setNoteViewMode('editor')">Editor</button>
            <button class="tb-mode-btn" data-mode="preview" onclick="setNoteViewMode('preview')">Prévia</button>
          </div>
        </div>

        <div class="note-toolbar">
          <div class="toolbar-group">
            <!-- UNDO / REDO COM CTRL+Z / CTRL+Y -->
            <button class="tb-btn tb-btn-undo" id="tb-btn-undo" onclick="undoNote()" title="Desfazer (Ctrl + Z)">↩</button>
            <button class="tb-btn tb-btn-redo" id="tb-btn-redo" onclick="redoNote()" title="Refazer (Ctrl + Y ou Ctrl + Shift + Z)">↪</button>
            <span class="tb-sep"></span>

            <button class="tb-btn" onclick="insertNoteFormat('bold')" title="Negrito"><b>B</b></button>
            <button class="tb-btn" onclick="insertNoteFormat('italic')" title="Itálico"><i>I</i></button>
            <button class="tb-btn" onclick="insertNoteFormat('heading')" title="Título"><b>H</b></button>
            <button class="tb-btn" onclick="insertNoteFormat('quote')" title="Dica">Dica</button>
            <span class="tb-sep"></span>
            <button class="tb-btn" onclick="insertNoteFormat('list')" title="Lista">Lista</button>
            <button class="tb-btn" onclick="insertNoteFormat('checklist')" title="Checklist">Check</button>
            <button class="tb-btn" onclick="insertNoteFormat('table')" title="Tabela">Tabela</button>
            <button class="tb-btn" onclick="insertNoteFormat('code')" title="Código Python">Código</button>
            <span class="tb-sep"></span>
            
            <!-- MARCADOR DE VÍDEO & PRONÚNCIA EM INGLÊS -->
            <button class="tb-btn" onclick="insertTimestampToNotes()" title="Inserir marcador de tempo atual do vídeo [mm:ss]">Minuto</button>
            <button class="tb-btn tb-audio-btn" onclick="speakSelectedText()" title="Ouvir pronúncia em inglês nativo do texto selecionado">Pronúncia</button>
            <span class="tb-sep"></span>

            <!-- FERRAMENTAS CIENTÍFICAS: MATEMÁTICA, 3D, DESENHO, MATRIZES E EXPORTAÇÃO -->
            <button class="tb-btn tb-highlight-math" onclick="toggleMathPalette()" title="Inserir Fórmulas e Símbolos Matemáticos">∑ Fórmulas</button>
            <button class="tb-btn tb-highlight-3d" onclick="open3DVectorStudio()" title="Abrir Estúdio de Vetores e Gráfico 3D (Eixos X, Y, Z)">3D</button>
            <button class="tb-btn tb-highlight-draw" onclick="openWhiteboardDrawer()" title="Abrir Lousa para Desenhar Formas Geométricas 2D">Desenhar</button>
            <button class="tb-btn" onclick="openMatrixCalculator()" title="Abrir Calculadora de Matrizes e Vetores">Matrizes</button>
            <button class="tb-btn" onclick="openExportModal()" title="Exportar Caderno em Markdown, PDF ou JSON">Exportar</button>
          </div>

          <div class="toolbar-templates">
            <select class="tb-select" onchange="insertNoteTemplate(this.value); this.value='';">
              <option value="" disabled selected>Modelos</option>
              <option value="summary">📝 Resumo de Aula</option>
              <option value="table">📊 Tabela de Comparação</option>
              <option value="code">💻 Exemplo Prático Python</option>
              <option value="math_vectors">📐 Vetores & Álgebra Linear</option>
              <option value="schema">📐 Esquema de Fluxo</option>
              <option value="vocab_en">🇺🇸 Tabela Vocabulário & Pronúncia</option>
            </select>
          </div>
        </div>

        <!-- PALETA DE SÍMBOLOS MATEMÁTICOS & FÓRMULAS LATEX (EXPANSÍVEL) -->
        <div id="math-symbols-palette" class="math-palette-wrap" style="display:none">
          <div class="math-palette-head">
            <span>∑ Símbolos & Fórmulas Matemáticas para IA</span>
            <button class="math-palette-close" onclick="toggleMathPalette(false)">✕</button>
          </div>
          <div class="math-symbols-grid">
            <button class="sym-btn" onclick="insertSymbol('∑')">∑ (somatório)</button>
            <button class="sym-btn" onclick="insertSymbol('∏')">∏ (produtório)</button>
            <button class="sym-btn" onclick="insertSymbol('∫')">∫ (integral)</button>
            <button class="sym-btn" onclick="insertSymbol('∂')">∂ (derivada parcial)</button>
            <button class="sym-btn" onclick="insertSymbol('∇')">∇ (gradiente / nabla)</button>
            <button class="sym-btn" onclick="insertSymbol('√')">√ (raiz)</button>
            <button class="sym-btn" onclick="insertSymbol('θ')">θ (teta / parâmetros)</button>
            <button class="sym-btn" onclick="insertSymbol('λ')">λ (lambda / regularização)</button>
            <button class="sym-btn" onclick="insertSymbol('α')">α (alpha / learning rate)</button>
            <button class="sym-btn" onclick="insertSymbol('β')">β (beta)</button>
            <button class="sym-btn" onclick="insertSymbol('π')">π (pi)</button>
            <button class="sym-btn" onclick="insertSymbol('∈')">∈ (pertence)</button>
            <button class="sym-btn" onclick="insertSymbol('ℝ')">ℝ (reais)</button>
            <button class="sym-btn" onclick="insertSymbol('ℝⁿ')">ℝⁿ (espaço n-dimensional)</button>
            <button class="sym-btn" onclick="insertSymbol('·')">· (produto escalar)</button>
            <button class="sym-btn" onclick="insertSymbol('×')">× (produto vetorial)</button>
            <button class="sym-btn" onclick="insertSymbol('∥v∥')">∥v∥ (norma do vetor)</button>
            <button class="sym-btn" onclick="insertSymbol('Wᵀ')">Wᵀ (transposta)</button>
            <button class="sym-btn" onclick="insertSymbol('≠')">≠</button>
            <button class="sym-btn" onclick="insertSymbol('≈')">≈</button>
            <button class="sym-btn" onclick="insertSymbol('≤')">≤</button>
            <button class="sym-btn" onclick="insertSymbol('≥')">≥</button>
          </div>
          <div class="math-templates-row">
            <span style="font-size:.76rem;font-weight:700;color:var(--mu)">Templates LaTeX:</span>
            <button class="sym-tmpl-btn" onclick="insertLatexTemplate('vec3d')">Vetor Coluna 3D [x, y, z]</button>
            <button class="sym-tmpl-btn" onclick="insertLatexTemplate('matrix2x2')">Matriz 2x2</button>
            <button class="sym-tmpl-btn" onclick="insertLatexTemplate('dotprod')">Produto Escalar u · v</button>
            <button class="sym-tmpl-btn" onclick="insertLatexTemplate('norm')">Norma Euclidiana ||v||</button>
            <button class="sym-tmpl-btn" onclick="insertLatexTemplate('gradient')">Gradiente ∇f</button>
            <button class="sym-tmpl-btn" onclick="insertLatexTemplate('softmax')">Softmax</button>
            <button class="sym-tmpl-btn" onclick="insertLatexTemplate('attention')">Atenção Transformer</button>
          </div>
        </div>

        <!-- WORKSPACE DE ANOTAÇÕES -->
        <div class="note-workspace mode-editor" id="note-workspace">
          <div class="note-editor-pane">
            <textarea id="modal-note-editor" placeholder="Digite suas anotações, fórmulas matemáticas ($...$ ou $$...$$), códigos e insights da aula aqui...
Assista ao vídeo e registre aqui seus insights, fórmulas e códigos!" oninput="onNoteEditorInput()"></textarea>
          </div>
          <div class="note-preview-pane">
            <div class="preview-header">Prévia</div>
            <div class="preview-body" id="modal-preview-body"></div>
          </div>
        </div>

        <!-- RODAPÉ -->
        <div class="note-modal-footer">
          <div class="footer-stats" id="modal-footer-stats">0 palavras · 0 caracteres</div>
          <div class="footer-sync" id="modal-sync-indicator" style="display:none"></div>
          <div class="footer-actions">
            <button class="note-clear-btn" onclick="clearModalNote()">Limpar</button>
            <button class="note-save-btn" onclick="closeNoteModal()">Salvar e fechar</button>
          </div>
        </div>
       </div><!-- /study-notes-panel -->
      </div>

    </div><!-- /study-columns-layout -->
  </div>
</div>

<!-- ======================================================================= -->
<!-- ESTÚDIO DE VETORES & GEOMETRIA 3D (EIXOS X, Y, Z INTERATIVO)             -->
<!-- ======================================================================= -->
<div id="modal-3d-studio" class="modal-sub-overlay" hidden>
  <div class="modal-sub-box modal-3d-box">
    <div class="modal-sub-header">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:1.3rem">🌐</span>
        <h3 style="margin:0;font-size:1.15rem;color:var(--tx)">Estúdio de Vetores & Geometria 3D</h3>
      </div>
      <button class="note-close-btn" onclick="close3DVectorStudio()">✕</button>
    </div>

    <div class="modal-3d-body">
      <!-- CANVAS 3D INTERATIVO -->
      <div class="canvas-3d-wrap">
        <canvas id="canvas-3d" width="600" height="420"></canvas>
        <div class="canvas-3d-overlay-hint">
          <span>🔄 Arraste com o mouse para girar em 360° · Scroll para zoom</span>
        </div>
        <div class="canvas-3d-axes-legend">
          <span style="color:#ef4444">🔴 Eixo X</span>
          <span style="color:#10b981">🟢 Eixo Y</span>
          <span style="color:#3b82f6">🔵 Eixo Z</span>
        </div>
      </div>

      <!-- PAINEL DE CONTROLES E CÁLCULOS 3D -->
      <div class="controls-3d-wrap">
        <div class="v3d-panel-title">📐 Coordenadas dos Vetores</div>

        <!-- Vetor 1 -->
        <div class="v3d-vector-card" style="border-left:4px solid #8b5cf6">
          <div class="v3d-card-head">
            <span style="font-weight:750;color:#8b5cf6">Vetor v1 (Roxo)</span>
            <span class="v3d-norm-tag" id="v3d-norm-1">||v1|| = 5.39</span>
          </div>
          <div class="v3d-inputs-row">
            <label>X: <input type="number" id="v3d-x1" value="3" step="0.5" oninput="update3DScene()"></label>
            <label>Y: <input type="number" id="v3d-y1" value="4" step="0.5" oninput="update3DScene()"></label>
            <label>Z: <input type="number" id="v3d-z1" value="2" step="0.5" oninput="update3DScene()"></label>
          </div>
        </div>

        <!-- Vetor 2 -->
        <div class="v3d-vector-card" style="border-left:4px solid #06b6d4">
          <div class="v3d-card-head">
            <span style="font-weight:750;color:#06b6d4">Vetor v2 (Ciano)</span>
            <span class="v3d-norm-tag" id="v3d-norm-2">||v2|| = 3.16</span>
          </div>
          <div class="v3d-inputs-row">
            <label>X: <input type="number" id="v3d-x2" value="1" step="0.5" oninput="update3DScene()"></label>
            <label>Y: <input type="number" id="v3d-y2" value="0" step="0.5" oninput="update3DScene()"></label>
            <label>Z: <input type="number" id="v3d-z2" value="3" step="0.5" oninput="update3DScene()"></label>
          </div>
        </div>

        <!-- Opções de Formas Geométricas 3D -->
        <div class="v3d-options-row">
          <label class="v3d-opt-label">Forma 3D:
            <select id="v3d-shape-select" class="v3d-select" onchange="update3DScene()">
              <option value="none">Nenhuma (Apenas Vetores)</option>
              <option value="cube" selected>Cubo 3D Wireframe</option>
              <option value="plane">Plano / Hiperplano</option>
              <option value="pyramid">Pirâmide / Tetraedro</option>
              <option value="sphere">Esfera Unitária</option>
            </select>
          </label>
          <label style="display:flex;align-items:center;gap:6px;font-size:.82rem;cursor:pointer">
            <input type="checkbox" id="v3d-show-grid" checked onchange="update3DScene()"> Grade de Fundo
          </label>
        </div>

        <!-- Cálculos Matemáticos em Tempo Real -->
        <div class="v3d-math-results" id="v3d-math-results">
          <div><b>Produto Escalar (v1 · v2):</b> <span id="v3d-dot-prod">9.00</span></div>
          <div><b>Ângulo entre os vetores (θ):</b> <span id="v3d-angle">58.1°</span></div>
        </div>

        <!-- Botões de Ação -->
        <div class="v3d-actions-row">
          <button class="v3d-snapshot-btn" onclick="insert3DSnapshotToNotes()">📸 Inserir Gráfico 3D na Anotação</button>
          <button class="v3d-reset-btn" onclick="reset3DCamera()">🔄 Resetar Visão</button>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ======================================================================= -->
<!-- LOUSA DE DESENHO GEOMÉTRICO 2D (WHITEBOARD CANVAS)                       -->
<!-- ======================================================================= -->
<div id="modal-draw-studio" class="modal-sub-overlay" hidden>
  <div class="modal-sub-box modal-draw-box">
    <div class="modal-sub-header">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:1.3rem">✏️</span>
        <h3 style="margin:0;font-size:1.15rem;color:var(--tx)">Lousa de Desenho & Formas Geométricas 2D</h3>
      </div>
      <button class="note-close-btn" onclick="closeWhiteboardDrawer()">✕</button>
    </div>

    <!-- Barra de Ferramentas de Desenho -->
    <div class="draw-toolbar">
      <div class="draw-tool-group">
        <button class="draw-tool-btn active" data-tool="pen" onclick="setDrawTool('pen')" title="Caneta livre">✏️ Caneta</button>
        <button class="draw-tool-btn" data-tool="line" onclick="setDrawTool('line')" title="Linha reta">📏 Linha</button>
        <button class="draw-tool-btn" data-tool="arrow" onclick="setDrawTool('arrow')" title="Seta de vetor">➔ Vetor</button>
        <button class="draw-tool-btn" data-tool="rect" onclick="setDrawTool('rect')" title="Retângulo">◻️ Retângulo</button>
        <button class="draw-tool-btn" data-tool="circle" onclick="setDrawTool('circle')" title="Círculo">⭕ Círculo</button>
        <button class="draw-tool-btn" data-tool="axes" onclick="setDrawTool('axes')" title="Eixos Cartesianos X e Y">➕ Eixos X,Y</button>
      </div>

      <div class="draw-color-group">
        <span class="color-dot active" style="background:#8b5cf6" onclick="setDrawColor('#8b5cf6')"></span>
        <span class="color-dot" style="background:#06b6d4" onclick="setDrawColor('#06b6d4')"></span>
        <span class="color-dot" style="background:#10b981" onclick="setDrawColor('#10b981')"></span>
        <span class="color-dot" style="background:#ef4444" onclick="setDrawColor('#ef4444')"></span>
        <span class="color-dot" style="background:#f59e0b" onclick="setDrawColor('#f59e0b')"></span>
        <span class="color-dot" style="background:#ffffff;border:1px solid #ccc" onclick="setDrawColor('#ffffff')"></span>
      </div>

      <div class="draw-action-group">
        <button class="draw-act-btn" onclick="clearWhiteboard()">🗑️ Limpar</button>
        <button class="draw-act-btn draw-insert-btn" onclick="insertWhiteboardToNotes()">📥 Inserir Desenho na Anotação</button>
      </div>
    </div>

    <!-- Canvas de Desenho -->
    <div class="draw-canvas-wrap">
      <canvas id="whiteboard-canvas" width="750" height="450"></canvas>
    </div>
  </div>
</div>

<!-- ======================================================================= -->
<!-- SUBMODAL: CALCULADORA DE MATRIZES E ÁLGEBRA LINEAR                      -->
<!-- ======================================================================= -->
<div id="modal-matrix-calc" class="modal-sub-overlay" hidden>
  <div class="modal-sub-box modal-calc-box">
    <div class="modal-sub-header">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:1.3rem">🧮</span>
        <h3 style="margin:0;font-size:1.15rem;color:var(--tx)">Calculadora de Matrizes & Álgebra Linear</h3>
      </div>
      <button class="note-close-btn" onclick="closeMatrixCalculator()">✕</button>
    </div>

    <div class="calc-tabs">
      <button class="calc-tab-btn active" data-tab="matrices" onclick="setCalcTab('matrices')">Matrizes 2×2</button>
      <button class="calc-tab-btn" data-tab="vectors" onclick="setCalcTab('vectors')">Vetores & Ângulo</button>
    </div>

    <div class="calc-tab-pane active" id="calc-pane-matrices">
      <div class="calc-matrices-row">
        <!-- Matriz A -->
        <div class="calc-matrix-card">
          <div class="calc-matrix-title">Matriz A</div>
          <div class="calc-matrix-grid">
            <input type="number" id="m-a00" value="2" step="any">
            <input type="number" id="m-a01" value="1" step="any">
            <input type="number" id="m-a10" value="1" step="any">
            <input type="number" id="m-a11" value="3" step="any">
          </div>
        </div>

        <div style="font-size:1.4rem;font-weight:700;color:var(--mu)">operar com</div>

        <!-- Matriz B -->
        <div class="calc-matrix-card">
          <div class="calc-matrix-title">Matriz B</div>
          <div class="calc-matrix-grid">
            <input type="number" id="m-b00" value="1" step="any">
            <input type="number" id="m-b01" value="0" step="any">
            <input type="number" id="m-b10" value="2" step="any">
            <input type="number" id="m-b11" value="1" step="any">
          </div>
        </div>
      </div>

      <div class="calc-actions-row">
        <button class="calc-op-btn" onclick="calculateMatrix('detA')">det(A)</button>
        <button class="calc-op-btn" onclick="calculateMatrix('invA')">Inversa A⁻¹</button>
        <button class="calc-op-btn" onclick="calculateMatrix('transA')">Transposta Aᵀ</button>
        <button class="calc-op-btn" onclick="calculateMatrix('add')">A + B</button>
        <button class="calc-op-btn" onclick="calculateMatrix('mul')">A × B</button>
      </div>

      <div class="calc-result-box" id="calc-matrix-result">
        <span>Clique em uma das operações acima para calcular a solução detalhada em KaTeX.</span>
      </div>

      <div style="display:flex;justify-content:flex-end">
        <button class="note-save-btn" onclick="insertMatrixResultToNotes()">📥 Inserir Solução LaTeX na Anotação</button>
      </div>
    </div>

    <div class="calc-tab-pane" id="calc-pane-vectors">
      <div style="display:flex;gap:20px;flex-wrap:wrap">
        <div class="calc-matrix-card">
          <div class="calc-matrix-title">Vetor u = [x, y, z]</div>
          <div style="display:flex;gap:6px">
            <input type="number" id="v-u1" value="3" style="width:55px;padding:6px;border-radius:6px;border:1px solid var(--bd);background:var(--bg);color:var(--tx)">
            <input type="number" id="v-u2" value="4" style="width:55px;padding:6px;border-radius:6px;border:1px solid var(--bd);background:var(--bg);color:var(--tx)">
            <input type="number" id="v-u3" value="0" style="width:55px;padding:6px;border-radius:6px;border:1px solid var(--bd);background:var(--bg);color:var(--tx)">
          </div>
        </div>
        <div class="calc-matrix-card">
          <div class="calc-matrix-title">Vetor v = [x, y, z]</div>
          <div style="display:flex;gap:6px">
            <input type="number" id="v-v1" value="1" style="width:55px;padding:6px;border-radius:6px;border:1px solid var(--bd);background:var(--bg);color:var(--tx)">
            <input type="number" id="v-v2" value="2" style="width:55px;padding:6px;border-radius:6px;border:1px solid var(--bd);background:var(--bg);color:var(--tx)">
            <input type="number" id="v-v3" value="2" style="width:55px;padding:6px;border-radius:6px;border:1px solid var(--bd);background:var(--bg);color:var(--tx)">
          </div>
        </div>
      </div>
      <div class="calc-actions-row">
        <button class="calc-op-btn" onclick="calculateVectorOp('dot')">Produto Escalar u · v</button>
        <button class="calc-op-btn" onclick="calculateVectorOp('cross')">Produto Vetorial u × v</button>
        <button class="calc-op-btn" onclick="calculateVectorOp('angle')">Ângulo θ entre u e v</button>
      </div>
      <div class="calc-result-box" id="calc-vector-result">
        <span>Selecione uma operação vetorial para calcular.</span>
      </div>
      <div style="display:flex;justify-content:flex-end">
        <button class="note-save-btn" onclick="insertVectorResultToNotes()">📥 Inserir Vetores na Anotação</button>
      </div>
    </div>
  </div>
</div>

<!-- ======================================================================= -->
<!-- SUBMODAL 3: EXPORTADOR DE CADERNO COMPLETO & PORTFÓLIO                  -->
<!-- ======================================================================= -->
<div id="modal-export-notebook" class="modal-sub-overlay" hidden>
  <div class="modal-sub-box modal-export-box">
    <div class="modal-sub-header">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:1.3rem">📥</span>
        <h3 style="margin:0;font-size:1.15rem;color:var(--tx)">Exportador de Caderno & Portfólio de Estudos</h3>
      </div>
      <button class="note-close-btn" onclick="closeExportModal()">✕</button>
    </div>

    <div class="export-options-grid">
      <button class="export-card-btn" onclick="exportNotebookMarkdown()">
        <span class="export-card-icon">📄</span>
        <span class="export-card-title">Baixar em Markdown (.md)</span>
        <span class="export-card-desc">Compila todas as suas notas, tabelas e links em um arquivo único formatado, pronto para subir no GitHub.</span>
      </button>

      <button class="export-card-btn" onclick="exportNotebookPrint()">
        <span class="export-card-icon">🖨️</span>
        <span class="export-card-title">Imprimir / Salvar em PDF</span>
        <span class="export-card-desc">Abre uma visualização limpa com todas as fórmulas matemáticas renderizadas para imprimir ou salvar em PDF.</span>
      </button>

      <button class="export-card-btn" onclick="exportBackupJson()">
        <span class="export-card-icon">💾</span>
        <span class="export-card-title">Backup Completo (JSON)</span>
        <span class="export-card-desc">Exporta todos os dados de progresso, anotações e metas para restaurar a qualquer momento.</span>
      </button>
    </div>
  </div>
</div>

__CHANGE_CREDENTIALS_MODAL__

<script>
__AUTH_AWS_SYNC_JS__

const TRACK_ID = "__TRACK_ID__";
const TOTAL_TRACK_TOPICS = __TOTAL_TOPICS__;
let NEXT_TOPIC_ID = null;   // o "Continuar" abre esta aula (definida no paint)
const TOPICS_MAP = __TOPICS_MAP_JSON__;
const KEY = "roteiro-ia-v1";
let PR = {};
let FILTER = "all";
let SEARCH_QUERY = "";
let PACE_MODE = "std";
let CURRENT_MODAL_TOPIC_ID = null;
let NOTE_VIEW_MODE = "split";
let API_BASE = "http://localhost:8000";
let API_CONNECTED = false;
let noteDebounceTimer = null;

// 1. Carregar do LocalStorage
function loadLocal() {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) PR = JSON.parse(raw);
  } catch(e) {}
}

function diffAndLogEvents(){
  try{
    const cur = {}; for (const k in PR) cur[k] = PR[k].s || "z";
    const raw = localStorage.getItem("roteiro-snap-v1");
    if (!raw){
      localStorage.setItem("roteiro-snap-v1", JSON.stringify(cur));
      localStorage.setItem("roteiro-log-start", String(Date.now()));
      return;
    }
    const snap = JSON.parse(raw), now = Date.now(), ev = [];
    for (const k in cur){ const f = snap[k] || "z"; if (f !== cur[k]) ev.push({t:now, id:k, f, to:cur[k]}); }
    if (!ev.length) return;
    const src = window.__evSrc || (ev.length > 5 ? "bulk" : "ui"); window.__evSrc = null;
    ev.forEach(e => e.src = src);
    const log = JSON.parse(localStorage.getItem("roteiro-events-v1") || "[]").concat(ev).slice(-5000);
    localStorage.setItem("roteiro-events-v1", JSON.stringify(log));
    localStorage.setItem("roteiro-snap-v1", JSON.stringify(cur));
  }catch(e){}
}

function saveLocal() {
  try {
    localStorage.setItem(KEY, JSON.stringify(PR));
    diffAndLogEvents();
    if (typeof scheduleAwsRealtimeSync === "function") scheduleAwsRealtimeSync();
  } catch(e) {}
}

// 2. Sincronizar com Banco de Dados / API
async function initSync() {
  loadLocal();
  paint();

  // O banco local do server.py (usuário 1) é só para desenvolvimento: vale apenas para o usuário de teste,
  // nunca para uma conta real (senão o progresso local se misturaria com o dela). Em produção, a nuvem é o backend.
  if (!isTestUser(getLoggedInUser())) {
    return;
  }

  try {
    let res = await fetch(API_BASE + "/api/status", { cache: "no-store" }).catch(()=>null);
    if (!res && !window.location.origin.startsWith("http")) {
      res = await fetch("http://localhost:8080/api/status", { cache: "no-store" }).catch(()=>null);
      if (res) API_BASE = "http://localhost:8080";
    }

    if (res && res.ok) {
      const data = await res.json();
      API_CONNECTED = true;
      const dbBadge = document.getElementById("nav-db-status");
      if (dbBadge) {
        if (data.db_type === "postgres") {
          dbBadge.className = "nav-status-pill badge-pg";
          dbBadge.textContent = "🐘 PostgreSQL";
        } else {
          dbBadge.className = "nav-status-pill badge-sq";
          dbBadge.textContent = "💾 SQLite";
        }
      }

      const progRes = await fetch(API_BASE + "/api/progress?user_id=1");
      if (progRes.ok) {
        const dbData = await progRes.json();
        for (const k in dbData) {
          PR[k] = Object.assign({ s: "z", n: "", d: "" }, dbData[k]);
        }
        saveLocal();
        paint();
      }
    }
  } catch(e) {}
}

async function syncTopicToServer(topicId) {
  if (!API_CONNECTED) return;
  const item = PR[topicId] || { s: "z", n: "", d: "" };
  try {
    await fetch(API_BASE + "/api/progress", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: 1,
        topic_id: topicId,
        status: item.s,
        notes: item.n,
        target_date: item.d
      })
    });
  } catch(e) {}
}

// 3. Renderização e Atualização Visual da Tela
function paint() {
  let doneCount = 0, progCount = 0, zeroCount = 0, noteCount = 0, reviewCount = 0;
  const optCount = { e: 0, r: 0, z: 0 };

  const allRows = document.querySelectorAll(`.topic-row`);
  let firstUncompletedRow = null;
  const STATUS_NAME = { z: "Do zero", r: "Em andamento", e: "Concluído" };

  allRows.forEach(row => {
    const tid = row.getAttribute("data-id");
    const item = PR[tid] || { s: "z", n: "", d: "" };
    const status = item.s || "z";
    const isOpt = row.hasAttribute("data-opt");   // opcionais: fora dos contadores e da meta

    if (isOpt) optCount[status === "e" || status === "r" ? status : "z"]++;
    else if (status === "e") doneCount++;
    else if (status === "r") progCount++;
    else zeroCount++;

    if (item.n && item.n.trim()) noteCount++;
    if (item.rv) reviewCount++;
    const rvBtn = row.querySelector('[data-act="review"]');
    if (rvBtn) {
      rvBtn.setAttribute("aria-pressed", String(Boolean(item.rv)));
      rvBtn.textContent = item.rv ? "✓ Na revisão" : "↻ Revisar";
    }

    // Situação: bolinha, faixa lateral e a opção marcada no painel
    const st = status === "e" || status === "r" ? status : "z";
    row.classList.toggle("status-z", st === "z");
    row.classList.toggle("status-r", st === "r");
    row.classList.toggle("status-e", st === "e");
    const sBtn = row.querySelector(".row-st");
    if (sBtn) {
      const label = sBtn.getAttribute("aria-label");
      sBtn.setAttribute("aria-label", label.slice(0, label.lastIndexOf(":") + 2) + STATUS_NAME[st]);
    }
    row.querySelectorAll("[data-status]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.status === st)));

    const meta = row.querySelector(".row-meta");
    if (meta) {
      const bits = [];
      if (st === "r") bits.push("Em andamento");
      if (item.n && item.n.trim()) bits.push("com anotação");
      if (item.rv) bits.push("↻ para revisar");
      meta.textContent = bits.join(" · ");
    }

    // Identificar primeiro não concluído para recomendação
    if (!firstUncompletedRow && status !== "e" && !isOpt) {
      firstUncompletedRow = row;
    }

    // Aplicar Filtro e Busca
    applyRowVisibility(row, status, item.n || "", Boolean(item.rv));
  });

  // Resumo da trilha
  const total = TOTAL_TRACK_TOPICS || 1;
  const pctE = Math.round((doneCount / total) * 100);
  const setText = (id, text) => { const el = document.getElementById(id); if (el) el.textContent = text; };
  setText("stat-done", doneCount);
  setText("stat-extra", (progCount ? ` · ${progCount} em andamento` : "") + (optCount.e ? ` · +${optCount.e} opc.` : ""));
  setText("prog-pct-label", `${pctE}%`);

  [["bar-e", doneCount], ["bar-r", progCount]].forEach(([id, n]) => {
    const bar = document.getElementById(id);
    if (!bar) return;
    bar.style.width = `${(n / total) * 100}%`;
    bar.classList.toggle("has", n > 0);
  });

  // Os números saíram dos filtros: ficam na dica de cada botão (obrigatórios + opcionais)
  const reqCount = { e: doneCount, r: progCount, z: zeroCount };
  for (const s in reqCount) {
    const el = document.querySelector(`.fil-btn[data-f="${s}"]`);
    if (el) el.title = STATUS_NAME[s] + ": " + reqCount[s] + (optCount[s] ? ` + ${optCount[s]} opc.` : "");
  }
  const notesBtn = document.querySelector('.fil-btn[data-f="n"]');
  if (notesBtn) notesBtn.title = "Anotações: " + noteCount;
  const reviewBtn = document.querySelector('.fil-btn[data-f="v"]');
  if (reviewBtn) reviewBtn.title = "Para revisar: " + reviewCount;

  // Nível
  const lvlIcon = document.getElementById("lvl-icon");
  const lvlName = document.getElementById("lvl-name");
  const lvlDesc = document.getElementById("lvl-desc");

  if (pctE >= 100) {
    if (lvlIcon) lvlIcon.textContent = "👑";
    if (lvlName) lvlName.textContent = "Mestre Supremo em IA";
    if (lvlDesc) lvlDesc.textContent = "Trilha 100% dominada com código, projetos e prática!";
  } else if (pctE >= 70) {
    if (lvlIcon) lvlIcon.textContent = "🏆";
    if (lvlName) lvlName.textContent = "Engenheiro Avançado";
    if (lvlDesc) lvlDesc.textContent = "Domínio sólido e pronto para posições de destaque.";
  } else if (pctE >= 40) {
    if (lvlIcon) lvlIcon.textContent = "⚡";
    if (lvlName) lvlName.textContent = "Desenvolvedor em Evolução";
    if (lvlDesc) lvlDesc.textContent = "Construindo soluções reais e conectando ferramentas.";
  } else if (pctE >= 15) {
    if (lvlIcon) lvlIcon.textContent = "🔥";
    if (lvlName) lvlName.textContent = "Estudante Focado";
    if (lvlDesc) lvlDesc.textContent = "Ganhando tração consistente dia após dia.";
  } else {
    if (lvlIcon) lvlIcon.textContent = "🌱";
    if (lvlName) lvlName.textContent = "Iniciante Curioso";
    if (lvlDesc) lvlDesc.textContent = "Construindo alicerces de ferro do zero absoluto.";
  }

  // Próxima aula
  NEXT_TOPIC_ID = firstUncompletedRow ? firstUncompletedRow.getAttribute("data-id") : null;
  setText("next-step-title", firstUncompletedRow
    ? firstUncompletedRow.querySelector(".topic-title-text").textContent
    : "🎉 Todos os tópicos obrigatórios desta trilha foram concluídos!");
  const nextBtn = document.getElementById("next-step-btn");
  if (nextBtn) nextBtn.hidden = !NEXT_TOPIC_ID;
  const nextTag = document.getElementById("next-step-tag");
  if (nextTag) nextTag.hidden = !NEXT_TOPIC_ID;
}

// 4. Situação do tópico
function chooseTopicStatus(topicId, next) {
  if (!PR[topicId]) PR[topicId] = { s: "z", n: "", d: "" };
  closeRowPanels();
  if ((PR[topicId].s || "z") === next) return;

  PR[topicId].s = next;
  if (next === "z") {
    PR[topicId].vp = 0;
    PR[topicId].gp = 0;
    delete PR[topicId].gc;
  } else if (next === "e") {
    PR[topicId].vp = 100;
    PR[topicId].gp = 100;
  }
  saveLocal();
  paint();
  syncTopicToServer(topicId);
}

// Lista de revisão: marca à parte (campo rv = quando entrou na lista). A situação, os contadores,
// as conquistas e o ritmo não mudam. Vai para a nuvem junto com o resto do progresso.
function toggleTopicReview(topicId) {
  if (!topicId) return;
  if (!PR[topicId]) PR[topicId] = { s: "z", n: "", d: "" };
  const add = !PR[topicId].rv;
  if (add) PR[topicId].rv = Date.now();
  else delete PR[topicId].rv;
  saveLocal();
  paint();
  updateModalReviewBtn();
  if (typeof showToast === "function") showToast(add ? "↻ Aula na lista de revisão. A situação dela não muda." : "Aula retirada da lista de revisão.");
}

function updateModalReviewBtn() {
  const btn = document.getElementById("modal-review-btn");
  if (!btn) return;
  const on = Boolean(CURRENT_MODAL_TOPIC_ID && PR[CURRENT_MODAL_TOPIC_ID] && PR[CURRENT_MODAL_TOPIC_ID].rv);
  btn.setAttribute("aria-pressed", String(on));
  btn.querySelector(".rv-txt").textContent = on ? "Na revisão" : "Revisar";
  btn.title = on ? "Esta aula está na lista de revisão. Toque para tirar." : "Colocar esta aula na lista de revisão (a situação não muda)";
}

function updateModalStatusBtn(status) {
  const btn = document.getElementById("modal-status-btn");
  if (!btn) return;
  const s = status === "e" || status === "r" ? status : "z";
  btn.dataset.s = s;
  btn.textContent = s === "e" ? "Concluído" : s === "r" ? "Em andamento" : "Do zero";
}

function toggleModalTopicStatus() {
  if (!CURRENT_MODAL_TOPIC_ID) return;
  const cur = (PR[CURRENT_MODAL_TOPIC_ID] && PR[CURRENT_MODAL_TOPIC_ID].s) ? PR[CURRENT_MODAL_TOPIC_ID].s : "z";
  let next = "z";
  if (cur === "z") next = "r";
  else if (cur === "r") next = "e";
  else next = "z";

  if (!PR[CURRENT_MODAL_TOPIC_ID]) PR[CURRENT_MODAL_TOPIC_ID] = { s: "z", n: "", d: "" };
  PR[CURRENT_MODAL_TOPIC_ID].s = next;
  if (next === "z") {
    PR[CURRENT_MODAL_TOPIC_ID].vp = 0;
    PR[CURRENT_MODAL_TOPIC_ID].gp = 0;
    if (typeof resetSessionStudyProgress === "function") resetSessionStudyProgress();
  } else if (next === "e") {
    PR[CURRENT_MODAL_TOPIC_ID].vp = 100;
    PR[CURRENT_MODAL_TOPIC_ID].gp = 100;
    if (typeof syncSessionStudyProgressUI === "function") syncSessionStudyProgressUI();
  }
  updateModalStatusBtn(next);
  saveLocal();
  paint();
  syncTopicToServer(CURRENT_MODAL_TOPIC_ID);
}

function onModalDateChange() {
  if (!CURRENT_MODAL_TOPIC_ID) return;
  const dateInput = document.getElementById("modal-date-input");
  if (!PR[CURRENT_MODAL_TOPIC_ID]) PR[CURRENT_MODAL_TOPIC_ID] = { s: "z", n: "", d: "" };
  PR[CURRENT_MODAL_TOPIC_ID].d = dateInput ? dateInput.value : "";
  saveLocal();
  syncTopicToServer(CURRENT_MODAL_TOPIC_ID);
}

// 5. Filtros e Pesquisa
function setFilter(f) {
  FILTER = f;
  document.querySelectorAll(".fil-btn").forEach(b => {
    b.classList.toggle("active", b.getAttribute("data-f") === f);
  });
  paint();
}

function onSearchInput(val) {
  SEARCH_QUERY = (val || "").trim().toLowerCase();
  paint();
}

function applyRowVisibility(row, status, noteText, inReview) {
  let matchFilter = true;
  if (FILTER === "z") matchFilter = status === "z";
  else if (FILTER === "r") matchFilter = status === "r";
  else if (FILTER === "e") matchFilter = status === "e";
  else if (FILTER === "n") matchFilter = noteText.trim().length > 0;
  else if (FILTER === "v") matchFilter = Boolean(inReview);

  let matchSearch = true;
  if (SEARCH_QUERY) {
    const text = (row.querySelector(".topic-left").textContent + " " + (row.dataset.search || "")).toLowerCase();
    matchSearch = text.includes(SEARCH_QUERY);
  }

  row.style.display = (matchFilter && matchSearch) ? "flex" : "none";
}

// 6. Navegação e Atalhos
function toggleSidebar() {
  const sb = document.getElementById("sidebar");
  const bd = document.getElementById("sb-backdrop");
  if (!sb) return;
  sb.classList.toggle("open");
  if (bd) bd.classList.toggle("active");
}

function jumpToSub(subId) {
  const el = document.getElementById(subId);
  if (el) {
    el.scrollIntoView({ behavior: "smooth", block: "start" });
    if (window.innerWidth < 1040) toggleSidebar();
  }
}

function scrollToNextStep() {
  const allRows = document.querySelectorAll(".topic-row");
  for (const row of allRows) {
    const tid = row.getAttribute("data-id");
    const item = PR[tid] || { s: "z" };
    if (item.s !== "e" && !row.hasAttribute("data-opt")) {   // o mesmo tópico do "Próximo passo recomendado"
      row.scrollIntoView({ behavior: "smooth", block: "center" });
      row.style.boxShadow = "0 0 0 4px var(--ac)";
      setTimeout(() => { row.style.boxShadow = ""; }, 1800);
      break;
    }
  }
}

// Linha da aula: um painel aberto por vez (situação ou mais opções)
function closeRowPanels() {
  document.querySelectorAll(".topic-panel:not([hidden])").forEach(p => {
    p.hidden = true;
    const btn = document.querySelector(`[aria-controls="${p.id}"]`);
    if (btn) btn.setAttribute("aria-expanded", "false");
  });
}

function toggleRowPanel(topicId, kind) {
  const panel = document.getElementById(`${kind}-${topicId}`);
  if (!panel) return;
  const open = panel.hidden;
  closeRowPanels();
  panel.hidden = !open;
  const btn = document.querySelector(`[aria-controls="${panel.id}"]`);
  if (btn) btn.setAttribute("aria-expanded", String(open));
}

function openTopicNotes(topicId) {
  openStudyModal(topicId, false, 1);
  setTimeout(() => {
    const ed = document.getElementById("modal-note-editor");
    if (!ed || CURRENT_MODAL_TOPIC_ID !== topicId) return;
    if (!ed.offsetParent) setNoteViewMode("editor");   // estava em "Prévia"
    ed.scrollIntoView({ block: "center" });
    ed.focus({ preventScroll: true });
  }, 450);
}

function continueStudy() {
  if (NEXT_TOPIC_ID) openStudyModal(NEXT_TOPIC_ID, false, 1);
}

function openExportFromMenu() {
  const sb = document.getElementById("sidebar");
  if (window.innerWidth < 1040 && sb && sb.classList.contains("open")) toggleSidebar();
  openExportModal();
}

function togglePhaseCollapse(idx) {
  const body = document.getElementById(`phase-body-${idx}`);
  if (body) {
    const isHidden = body.style.display === "none";
    body.style.display = isHidden ? "block" : "none";
  }
}

function setPace(mode) {
  PACE_MODE = mode;
  document.querySelectorAll(".trk-btn").forEach(b => {
    b.classList.toggle("active", b.id === `btn-pace-${mode}`);
  });
}

// 7. Editor de Anotações & Markdown
function onNoteEditorInput() {
  const editor = document.getElementById("modal-note-editor");
  if (!editor || !CURRENT_MODAL_TOPIC_ID) return;
  const val = editor.value;
  if (typeof pushNoteHistory === "function") pushNoteHistory(val, false);
  renderModalPreview(val);
  updateNoteStats(val);

  const sync = document.getElementById("modal-sync-indicator");
  if (sync) sync.textContent = "⏳ Salvando...";

  clearTimeout(noteDebounceTimer);
  noteDebounceTimer = setTimeout(() => {
    if (!PR[CURRENT_MODAL_TOPIC_ID]) PR[CURRENT_MODAL_TOPIC_ID] = { s: "z", n: "", d: "" };
    PR[CURRENT_MODAL_TOPIC_ID].n = val;
    saveLocal();
    paint();
    syncTopicToServer(CURRENT_MODAL_TOPIC_ID);
    if (sync) sync.textContent = "💾 Salvo automaticamente";
  }, 400);
}

function renderModalPreview(md) {
  const preview = document.getElementById("modal-preview-body");
  if (!preview) return;
  preview.innerHTML = parseMarkdown(md);

  // Renderizar Fórmulas KaTeX se disponível
  if (window.renderMathInElement) {
    try {
      window.renderMathInElement(preview, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "$", right: "$", display: false },
          { left: "\\[", right: "\\]", display: true },
          { left: "\\(", right: "\\)", display: false }
        ],
        throwOnError: false
      });
    } catch(e) {}
  }
}

function updateNoteStats(text) {
  const stats = document.getElementById("modal-footer-stats");
  if (!stats) return;
  const charCount = (text || "").length;
  const wordCount = (text || "").trim() ? text.trim().split(/\s+/).length : 0;
  stats.textContent = `${wordCount} palavra${wordCount !== 1 ? 's' : ''} · ${charCount} caractere${charCount !== 1 ? 's' : ''}`;
}

function setNoteViewMode(mode) {
  NOTE_VIEW_MODE = mode;
  const ws = document.getElementById("note-workspace");
  if (ws) ws.className = `note-workspace mode-${mode}`;
  document.querySelectorAll(".tb-mode-btn").forEach(b => {
    b.classList.toggle("active", b.dataset.mode === mode);
  });
}

function insertNoteFormat(type) {
  const editor = document.getElementById("modal-note-editor");
  if (!editor) return;
  editor.focus();
  const start = editor.selectionStart;
  const end = editor.selectionEnd;
  const sel = editor.value.substring(start, end);
  let rep = "";

  switch(type) {
    case "bold": rep = `**${sel || 'texto em negrito'}**`; break;
    case "italic": rep = `*${sel || 'texto em itálico'}*`; break;
    case "heading": rep = `\n### ${sel || 'Título da Seção'}\n`; break;
    case "quote": rep = `\n> 💡 **Dica de Ouro:** ${sel || 'Insira uma dica importante aqui'}\n`; break;
    case "list":
      rep = sel ? sel.split('\n').map(l => `- ${l}`).join('\n') : `\n- Item 1\n- Item 2\n- Item 3\n`;
      break;
    case "checklist":
      rep = sel ? sel.split('\n').map(l => `- [ ] ${l}`).join('\n') : `\n- [ ] Tarefa a realizar\n- [x] Tarefa concluída\n`;
      break;
    case "table":
      rep = `\n| Conceito | Explicação Prática | Aplicação em IA |\n|---|---|---|\n| Termo 1 | Definição clara | Como é usado |\n| Termo 2 | Definição clara | Como é usado |\n`;
      break;
    case "code":
      rep = `\n\`\`\`python\n# Código prático:\ndef exemplo():\n    pass\n\`\`\`\n`;
      break;
    case "schema":
      rep = `\n\`\`\`diagram\n[Entrada / Dados] ───▶ [Processamento / Modelo] ───▶ [Predição / Saída]\n\`\`\`\n`;
      break;
  }

  if (rep) {
    editor.value = editor.value.substring(0, start) + rep + editor.value.substring(end);
    editor.selectionStart = editor.selectionEnd = start + rep.length;
    if (typeof pushNoteHistory === "function") pushNoteHistory(editor.value, true);
    onNoteEditorInput();
  }
}

function insertNoteTemplate(tpl) {
  const editor = document.getElementById("modal-note-editor");
  if (!editor) return;
  editor.focus();

  const templates = {
    summary: `\n## 📝 Resumo da Aula\n\n### 🎯 O que aprendi:\n- Ponto chave 1\n- Ponto chave 2\n\n### 💡 Dúvidas / Aprofundamento:\n- O que preciso revisar depois\n`,
    table: `\n### 📊 Comparação de Conceitos\n\n| Item | Vantagens | Desvantagens | Quando Usar |\n|---|---|---|---|\n| Opção A | Rápido | Menos preciso | Prototipagem |\n| Opção B | Robusto | Mais lento | Produção |\n`,
    code: `\n### 💻 Exemplo Prático em Python\n\n\`\`\`python\nimport numpy as np\n\n# Exemplo de código do tópico:\ndef main():\n    print("Executando aprendizado!")\n\nif __name__ == '__main__':\n    main()\n\`\`\`\n`,
    math_vectors: `\n### 📐 Vetores & Geometria Linear\n\n$$\\vec{v}_1 = \\begin{bmatrix} x_1 \\\\ y_1 \\\\ z_1 \\end{bmatrix}, \\quad \\vec{v}_2 = \\begin{bmatrix} x_2 \\\\ y_2 \\\\ z_2 \\end{bmatrix}$$\n\n> **Produto Escalar:** $\\vec{v}_1 \\cdot \\vec{v}_2 = x_1 x_2 + y_1 y_2 + z_1 z_2$\n> **Norma Euclidiana:** $\\|\\vec{v}_1\\| = \\sqrt{x_1^2 + y_1^2 + z_1^2}$\n`,
    schema: `\n### 📐 Esquema de Fluxo de Dados\n\n\`\`\`diagram\n┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐\n│  Ingestão/Input │ ────▶ │  Transformação  │ ────▶ │  Resultado/Pred │\n└─────────────────┘       └─────────────────┘       └─────────────────┘\n\`\`\`\n`
  };

  if (templates[tpl]) {
    editor.value += templates[tpl];
    if (typeof pushNoteHistory === "function") pushNoteHistory(editor.value, true);
    onNoteEditorInput();
  }
}

function clearModalNote() {
  if (confirm("Tem certeza que deseja apagar todas as anotações deste tópico?")) {
    const editor = document.getElementById("modal-note-editor");
    if (editor) {
      editor.value = "";
      onNoteEditorInput();
    }
  }
}

function escHtml(str) {
  return String(str || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function parseMarkdown(md) {
  if (!md || !md.trim()) {
    return '<div class="empty-notes-hint">📝 Nenhuma anotação ainda.<br>Assista ao vídeo acima e faça suas anotações, desenhos geométricos e cálculos aqui!</div>';
  }
  const lines = md.split(/\r?\n/);
  let html = [];
  let inCode = false;
  let codeLang = '';
  let codeLines = [];
  let inTable = false;
  let tableRows = [];
  let inUl = false;

  function flushList() {
    if (inUl) { html.push('</ul>'); inUl = false; }
  }
  function flushTable() {
    if (!inTable) return;
    if (tableRows.length > 0) {
      let tHtml = '<div class="note-table-wrap"><table class="note-table">';
      tableRows.forEach((row, idx) => {
        const isHeader = idx === 0;
        const tag = isHeader ? 'th' : 'td';
        const cols = row.split('|').slice(1, -1);
        tHtml += '<tr>' + cols.map(c => '<' + tag + '>' + parseInline(c.trim()) + '</' + tag + '>').join('') + '</tr>';
      });
      tHtml += '</table></div>';
      html.push(tHtml);
    }
    inTable = false;
    tableRows = [];
  }

  function parseInline(text) {
    let t = escHtml(text);
    t = t.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
    t = t.replace(/\*(.*?)\*/g, '<i>$1</i>');
    t = t.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
    // Timestamps clicáveis no vídeo: [04:25] ou ⏱️ [04:25]
    t = t.replace(/(?:⏱️\s*)?\[(\d{1,2}:\d{2}(?::\d{2})?)\]/g, '<button class="note-timestamp-pill" onclick="seekVideoToSeconds(\'$1\')" title="Pular vídeo para $1">⏱️ $1</button>');
    // Suporte a imagens (incluindo Data URLs de snapshots 3D e desenhos!)
    t = t.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" style="max-width:100%;border-radius:8px;border:1px solid var(--bd);margin:10px 0;box-shadow:0 4px 12px rgba(0,0,0,.15);display:block;">');
    t = t.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    return t;
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    if (line.startsWith('```')) {
      flushList();
      flushTable();
      if (!inCode) {
        inCode = true;
        codeLang = line.slice(3).trim() || 'python';
        codeLines = [];
      } else {
        inCode = false;
        const safeCode = escHtml(codeLines.join('\n'));
        html.push(`<div class="note-code-block"><div class="code-header"><span>${codeLang}</span><button class="copy-code-btn" onclick="navigator.clipboard.writeText(this.closest('.note-code-block').querySelector('code').innerText);showToast('Copiado!')">Copiar</button></div><pre><code>${safeCode}</code></pre></div>`);
      }
      continue;
    }

    if (inCode) {
      codeLines.push(line);
      continue;
    }

    if (line.trim().startsWith('|') && line.trim().endsWith('|')) {
      flushList();
      if (line.includes('---')) continue;
      inTable = true;
      tableRows.push(line.trim());
      continue;
    } else {
      flushTable();
    }

    if (line.startsWith('### ')) {
      flushList();
      html.push(`<h3>${parseInline(line.slice(4))}</h3>`);
      continue;
    }
    if (line.startsWith('## ')) {
      flushList();
      html.push(`<h2>${parseInline(line.slice(3))}</h2>`);
      continue;
    }
    if (line.startsWith('# ')) {
      flushList();
      html.push(`<h1>${parseInline(line.slice(2))}</h1>`);
      continue;
    }
    if (line.startsWith('> ')) {
      flushList();
      html.push(`<blockquote class="note-quote">${parseInline(line.slice(2))}</blockquote>`);
      continue;
    }
    if (line.startsWith('- [ ] ') || line.startsWith('- [x] ')) {
      flushList();
      const done = line.startsWith('- [x] ');
      const content = parseInline(line.slice(6));
      html.push(`<div class="note-todo ${done ? 'done' : ''}"><input type="checkbox" ${done ? 'checked' : ''} disabled> <span>${content}</span></div>`);
      continue;
    }
    if (line.startsWith('- ') || line.startsWith('* ')) {
      if (!inUl) { html.push('<ul class="note-list">'); inUl = true; }
      html.push(`<li>${parseInline(line.slice(2))}</li>`);
      continue;
    } else {
      flushList();
    }

    if (!line.trim()) {
      continue;
    }

    html.push(`<p>${parseInline(line)}</p>`);
  }

  flushList();
  flushTable();
  return html.join('\n');
}

__STUDIO_JS__

function toggleTheme() {
  const html = document.documentElement;
  const isDark = html.getAttribute("data-theme") === "dark" || (!html.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
  const next = isDark ? "light" : "dark";
  html.setAttribute("data-theme", next);
  try { localStorage.setItem("roteiro-theme", next); } catch(e) {}
}

try {
  const savedTheme = localStorage.getItem("roteiro-theme") || "dark";
  document.documentElement.setAttribute("data-theme", savedTheme);
} catch(e) {}

// Monta a lista antes da primeira pintura (o script está no fim do <body>)
initSync();
if (typeof initSplitResizer === "function") initSplitResizer();
</script>
</body>
</html>
"""

    modal_track_names = {
        "ia": "Inteligência Artificial",
        "mat": "Matemática",
        "ing": "Inglês"
    }
    modal_track_name = modal_track_names.get(track_id, page_title)

    n_opt = all_topics - total_topics
    all_label = f"{all_topics} ({total_topics} + {n_opt} opcionais)" if n_opt else str(all_topics)
    extra_topics = f" (+{n_opt} opcionais)" if n_opt else ""
    rendered = (template
        .replace("__AUTH_GUARD__", AUTH_GUARD_HEAD_SCRIPT)
        .replace("__AUTH_AWS_CSS__", AUTH_AWS_SYNC_CSS)
        .replace("__CHANGE_CREDENTIALS_MODAL__", CHANGE_CREDENTIALS_MODAL_HTML)
        .replace("__AUTH_AWS_SYNC_JS__", AUTH_AWS_SYNC_JS)
        .replace("__PAGE_TITLE__", page_title)
        .replace("__MODAL_TRACK_NAME__", modal_track_name)
        .replace("__PAGE_SUB__", page_sub)
        .replace("__TRACK_ICON__", track_icon)
        .replace("__TRACK_ID__", track_id)
        .replace("__TOTAL_TOPICS__", str(total_topics))
        .replace("__ALL_LABEL__", all_label)
        .replace("__EXTRA_TOPICS__", extra_topics)
        .replace("__SHARED_CSS__", shared_css)
        .replace("__LISTING_CSS__", LISTING_CSS)
        .replace("__FAVICON__", FAVICON_LINK)
        .replace("__ACTIVE_HUB__", active_hub)
        .replace("__ACTIVE_IA__", active_ia)
        .replace("__ACTIVE_MAT__", active_mat)
        .replace("__ACTIVE_ING__", active_ing)
        .replace("__SIDEBAR_TREE__", sb_tree_str)
        .replace("__PHASES_CONTENT__", phases_str)
        .replace("__TOPICS_MAP_JSON__", topics_map_json)
        .replace("__STUDIO_JS__", STUDIO_JS)
    )

    from design_v2 import apply_design
    rendered = apply_design(rendered, track_id)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Gerado: {out_path} ({total_topics} tópicos enriquecidos)")
