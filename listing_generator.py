# -*- coding: utf-8 -*-
"""
Gerador de Páginas de Listagem com Estúdio Unificado de Estudo,
Auto-Progresso, KaTeX, Estúdio 3D de Vetores e Lousa de Desenho 2D.
"""

import json
from studio_js import STUDIO_JS

def generate_listing_page(track_id, page_title, page_sub, track_icon, phases, out_path, shared_css="", is_english=False):
    total_topics = 0
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
                topic_id = f"{track_id}-{p_idx}-{g_idx}-{t_idx}"
                total_topics += 1

                topic_title = ""
                yt_url = ""
                yt_label = "▶ Vídeo" if not is_english else "▶ EnglishBay"
                doc_url = ""
                doc_label = "📖 Material"

                if isinstance(raw_t, dict):
                    topic_title = raw_t.get("title", "")
                    yt_url = raw_t.get("video_url") or raw_t.get("url") or ""
                    yt_label = raw_t.get("video_label") or ("▶ YouTube" if is_english else "▶ Vídeo")
                    doc_url = raw_t.get("doc_url") or ""
                    doc_label = raw_t.get("doc_label") or "📖 Material"
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
                    "doc_url": doc_url,
                    "doc_label": doc_label
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
        p_count = sum(len(g["topics"]) for g in p["groups"])
        sub_btns = []
        for g in p["groups"]:
            sub_btns.append(f"""
            <button class="sb-sub-btn" onclick="jumpToSub('{g['id']}')">
              <span>{g['name']}</span>
              <span class="sb-badge-count">{len(g['topics'])}</span>
            </button>
            """)

        sidebar_tree_html.append(f"""
        <details class="sb-phase" open>
          <summary>
            <span class="sb-phase-title">📁 {p['title'].split('·')[0].strip()}</span>
            <span class="sb-badge-count">{p_count}</span>
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
                yt_btn_html = ""
                if t.get("url"):
                    t_lbl = t.get("label", "▶ Vídeo")
                    yt_btn_html = f'<button class="yt-btn" onclick="openStudyModal(\'{t_id}\')" title="Assistir no Estúdio Integrado">{t_lbl}</button>'

                doc_btn_html = ""
                if t.get("doc_url"):
                    doc_btn_html = f'<a href="{t["doc_url"]}" target="_blank" rel="noopener" class="doc-btn" title="Acessar material de estudo / documentação">{t.get("doc_label", "📖 Material")}</a>'

                topics_rows.append(f"""
                <div class="topic-row" data-id="{t['id']}" id="top-{t['id']}">
                  <div class="topic-left" onclick="openStudyModal('{t['id']}')" style="cursor:pointer" title="Clique para abrir Estúdio de Estudo & Anotações">
                    <span class="topic-title-text">{t['title']}</span>
                  </div>
                  <div class="topic-actions">
                    {yt_btn_html}
                    {doc_btn_html}
                    <button class="status-btn status-btn-z" onclick="cycleStatus('{t['id']}')" title="Clique para alternar: Do zero ➔ Falta terminar ➔ Concluído">🔴 Do zero</button>
                    <button class="note-btn" onclick="openStudyModal('{t['id']}')" title="Abrir Estúdio de Estudo & Anotações">📝 Anotações & Estudo</button>
                  </div>
                </div>
                """)

            groups_html.append(f"""
            <div class="group-section" id="{g['id']}">
              <div class="group-title">📌 {g['name']} ({len(g['topics'])})</div>
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
            <div class="phase-callout callout-tip">{p['tip']}</div>
            <div class="phase-callout callout-proj">🎯 <b>Projeto Prático:</b> {p['proj']}</div>
            <div class="phase-callout callout-res">📚 <b>Recursos Sugeridos:</b> {p['res']}</div>
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
<!-- KaTeX Math Typesetting -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
<style>
__SHARED_CSS__
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
    </nav>
    <div class="nav-right">
      <button class="player-ext-btn" onclick="openFlashcardsReviewModal()" title="Revisar Flashcards de Estudo">🗂️ Flashcards</button>
      <button class="player-ext-btn" onclick="openExportModal()" title="Exportar Caderno em Markdown/PDF">📥 Exportar Caderno</button>
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
        <p class="sub">__PAGE_SUB__ · <b>__TOTAL_TOPICS__ tópicos</b> organizados para domínio completo.</p>
      </div>

      <!-- RASTREADOR ITERATIVO E DINÂMICO DE METAS -->
      <section class="tracker-box" id="tracker-box">
        <div class="tracker-head">
          <div class="tracker-title">⏱️ Metas & Ritmo de Estudo</div>
          <div class="tracker-presets">
            <button class="trk-btn active" id="btn-pace-std" onclick="setPace('std')">Equilibrado (8-10h/sem)</button>
            <button class="trk-btn" id="btn-pace-acc" onclick="setPace('acc')">Acelerado (20-25h/sem)</button>
          </div>
        </div>

        <div class="level-banner">
          <div class="level-info">
            <div class="level-icon" id="lvl-icon">🌱</div>
            <div>
              <div class="level-name" id="lvl-name">Iniciante Curioso</div>
              <div class="level-desc" id="lvl-desc">Iniciando os primeiros passos da jornada.</div>
            </div>
          </div>
          <div class="level-xp-wrap">
            <div class="level-xp-text" id="lvl-xp-txt">0 / __TOTAL_TOPICS__ concluídos (0%)</div>
            <div class="level-xp-bar"><div class="level-xp-fill" id="lvl-xp-fill" style="width:0%"></div></div>
          </div>
        </div>

        <div class="pace-status-card pace-ontrack" id="pace-status-card">
          <span id="pace-status-text">🎯 Cronograma pronto: selecione seus tópicos e registre o progresso</span>
          <span id="pace-status-tag">Ritmo Ativo</span>
        </div>

        <div class="next-step-box" id="next-step-box">
          <div class="next-step-info">
            <span class="next-step-tag">Próximo Passo Recomendado:</span>
            <span class="next-step-title" id="next-step-title">Começar pelo primeiro tópico da trilha</span>
          </div>
          <button class="next-step-btn" id="next-step-btn" onclick="scrollToNextStep()">▶ Ir para este Tópico</button>
        </div>

        <div class="pace-stat-row">
          <div class="pace-stat-card">
            <span class="pace-stat-num" id="stat-done">0</span>
            <span class="pace-stat-sub">Tópicos Concluídos (🟢)</span>
          </div>
          <div class="pace-stat-card">
            <span class="pace-stat-num" id="stat-prog">0</span>
            <span class="pace-stat-sub">Falta Terminar (🟡)</span>
          </div>
          <div class="pace-stat-card">
            <span class="pace-stat-num" id="stat-zero">__TOTAL_TOPICS__</span>
            <span class="pace-stat-sub">Do Zero (🔴 Default)</span>
          </div>
          <div class="pace-stat-card">
            <span class="pace-stat-num" id="stat-notes">0</span>
            <span class="pace-stat-sub">Anotações Criadas (📝)</span>
          </div>
        </div>
      </section>

      <!-- BARRA DE PROGRESSO & FILTROS -->
      <section class="progress-card">
        <div class="progress-top">
          <span>Progresso da Trilha</span>
          <span id="prog-pct-label">0%</span>
        </div>
        <div class="prog-bar">
          <div class="p-e" id="bar-e" style="width:0%"></div>
          <div class="p-r" id="bar-r" style="width:0%"></div>
          <div class="p-z" id="bar-z" style="width:100%"></div>
        </div>
      </section>

      <section class="filter-row">
        <div class="filters">
          <button class="fil-btn active" data-f="all" onclick="setFilter('all')">Todos (__TOTAL_TOPICS__)</button>
          <button class="fil-btn" data-f="z" onclick="setFilter('z')">🔴 Do zero</button>
          <button class="fil-btn" data-f="r" onclick="setFilter('r')">🟡 Falta terminar</button>
          <button class="fil-btn" data-f="e" onclick="setFilter('e')">🟢 Concluído</button>
          <button class="fil-btn" data-f="n" onclick="setFilter('n')">📝 Anotações</button>
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
        <div class="note-breadcrumb" id="modal-breadcrumb">__PAGE_TITLE__</div>
        <h2 class="note-topic-title" id="modal-topic-title">Título do Tópico</h2>
      </div>
      <div class="note-header-right">
        <!-- TOGGLE DE PROGRESSO AUTOMÁTICO -->
        <div class="auto-prog-wrap" title="Quando ativado, atualiza o progresso para 'Falta terminar' e 'Concluído' conforme seu tempo de estudo no vídeo/leitura">
          <label class="switch">
            <input type="checkbox" id="modal-auto-prog-check" onchange="toggleAutoProgress(this.checked)">
            <span class="slider"></span>
          </label>
          <span style="display:flex;align-items:center;gap:4px">⚡ Progresso Auto</span>
        </div>

        <!-- STATUS MANUAL -->
        <div class="note-status-wrap">
          <button class="note-status-pill" id="modal-status-btn" onclick="toggleModalTopicStatus()" title="Clique para alternar manualmente: Do zero ➔ Falta terminar ➔ Concluído">🔴 Do zero</button>
        </div>

        <!-- META DE DATA -->
        <div class="note-date-wrap">
          <label>🎯 Meta:</label>
          <input type="date" id="modal-date-input" onchange="onModalDateChange()">
        </div>

        <!-- POMODORO TIMER INTEGRADO -->
        <div class="pomodoro-wrap" id="pomodoro-wrap">
          <button class="pomo-toggle-btn" id="pomo-btn" onclick="togglePomodoro()" title="Iniciar ciclo Pomodoro de 25 min">🍅 25:00</button>
          <button class="pomo-reset-btn" onclick="resetPomodoro()" title="Resetar Pomodoro">↺</button>
          <span class="pomo-count-badge" id="pomo-count-badge" title="Pomodoros concluídos hoje">0 🍅</span>
        </div>

        <button class="note-close-btn" onclick="closeNoteModal()" title="Fechar estúdio">✕</button>
      </div>
    </div>

    <!-- 2. CORPO DO ESTÚDIO: DIVIDIDO LADO A LADO (VÍDEO À ESQUERDA | ANOTAÇÕES À DIREITA) -->
    <div class="study-columns-layout" id="study-columns-layout">

      <!-- COLUNA DA ESQUERDA: VÍDEO, MATERIAIS & SESSÃO DE ESTUDO -->
      <div class="study-player-col" id="study-player-sect">
        <div class="study-player-topbar">
          <div class="player-topbar-info">
            <span class="player-source-tag" id="modal-player-tag">▶ Vídeo Aula</span>
            <span class="player-source-title" id="modal-player-title">Material de Estudo</span>
          </div>
          <div class="player-topbar-actions">
            <a href="#" target="_blank" rel="noopener" id="modal-external-link" class="player-ext-btn" title="Abrir vídeo no YouTube em nova aba">↗ YouTube Externo</a>
            <a href="#" target="_blank" rel="noopener" id="modal-doc-link" class="player-ext-btn doc-ext" style="display:none" title="Abrir documentação ou material oficial">📖 Documentação</a>
            <button class="player-collapse-btn" id="modal-collapse-btn" onclick="toggleVideoCollapse()" title="Recolher / Ocultar player de vídeo">▲ Ocultar Vídeo</button>
          </div>
        </div>

        <!-- CONTAINER DO IFRAME DO VÍDEO -->
        <div class="video-responsive-wrap" id="video-wrapper">
          <iframe id="modal-video-iframe" src="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
        </div>

        <!-- BARRA DE PROGRESSO DA SESSÃO / AUTO PROGRESSO -->
        <div class="session-progress-bar-wrap" id="session-progress-wrap">
          <div class="session-progress-info">
            <span id="session-progress-text">⏱️ Sessão Ativa: 00:00 · Status: Estudando</span>
            <div style="display:flex;align-items:center;gap:10px">
              <span id="session-progress-pct" style="font-weight:750;color:var(--ac)">0%</span>
              <button class="session-finish-btn" onclick="markTopicCompleteNow()" title="Marcar este tópico como Concluído imediatamente">✅ Concluir Tópico</button>
            </div>
          </div>
          <div class="session-bar-track">
            <div class="session-bar-fill" id="session-bar-fill" style="width:0%"></div>
          </div>
        </div>

        <!-- PAINEL EXTRA DE CONTEXTO E DICAS DO TÓPICO -->
        <div class="study-left-extra-info">
          <div class="study-left-card">
            <div class="study-left-card-title">💡 Aprendizado Ativo & Imersivo:</div>
            <p>Assista aos conceitos no vídeo à esquerda, pause nos momentos-chave e registre seus códigos e insights no caderno à direita. Use a <b>Paleta Matemática</b> para fórmulas e o <b>Estúdio 3D</b> para visualizar tensores e vetores geometricamente.</p>
          </div>
        </div>
      </div>

      <!-- BARRA DIVISÓRIA ARRASTÁVEL ENTRE VÍDEO E ANOTAÇÕES -->
      <div class="study-split-resizer" id="study-split-resizer" title="Arraste para redimensionar vídeo e caderno (Duplo clique para 50% / 50%)">
        <div class="resizer-handle"></div>
      </div>

      <!-- COLUNA DA DIREITA: CADERNO DE ANOTAÇÕES & ESQUEMAS -->
      <div class="study-notes-col" id="study-notes-col">
        <div class="notes-section-head">
          <div class="notes-head-title">
            <span>📝 Caderno de Anotações & Esquemas</span>
          </div>
          <div class="toolbar-modes">
            <button class="tb-mode-btn" data-mode="split" onclick="setNoteViewMode('split')">◫ Lado a Lado</button>
            <button class="tb-mode-btn active" data-mode="editor" onclick="setNoteViewMode('editor')">✍️ Editor</button>
            <button class="tb-mode-btn" data-mode="preview" onclick="setNoteViewMode('preview')">👁️ Prévia</button>
          </div>
        </div>

        <div class="note-toolbar">
          <div class="toolbar-group">
            <!-- UNDO / REDO COM CTRL+Z / CTRL+Y -->
            <button class="tb-btn tb-btn-undo" id="tb-btn-undo" onclick="undoNote()" title="Desfazer (Ctrl + Z)">↩</button>
            <button class="tb-btn tb-btn-redo" id="tb-btn-redo" onclick="redoNote()" title="Refazer (Ctrl + Y ou Ctrl + Shift + Z)">↪</button>
            <span class="tb-sep"></span>

            <button class="tb-btn" onclick="insertNoteFormat('bold') title="Negrito"><b>B</b></button>
            <button class="tb-btn" onclick="insertNoteFormat('italic')" title="Itálico"><i>I</i></button>
            <button class="tb-btn" onclick="insertNoteFormat('heading')" title="Título"><b>H</b></button>
            <button class="tb-btn" onclick="insertNoteFormat('quote')" title="Dica">💡 Dica</button>
            <span class="tb-sep"></span>
            <button class="tb-btn" onclick="insertNoteFormat('list')" title="Lista">📋 Lista</button>
            <button class="tb-btn" onclick="insertNoteFormat('checklist')" title="Checklist">☑️ Check</button>
            <button class="tb-btn" onclick="insertNoteFormat('table')" title="Tabela">📊 Tabela</button>
            <button class="tb-btn" onclick="insertNoteFormat('code')" title="Código Python">💻 Código</button>
            <span class="tb-sep"></span>
            
            <!-- MARCADOR DE VÍDEO & PRONÚNCIA EM INGLÊS -->
            <button class="tb-btn" onclick="insertTimestampToNotes()" title="Inserir marcador de tempo atual do vídeo [mm:ss]">⏱️ Minuto</button>
            <button class="tb-btn tb-audio-btn" onclick="speakSelectedText()" title="Ouvir pronúncia em inglês nativo do texto selecionado">🔊 Pronúncia</button>
            <span class="tb-sep"></span>

            <!-- FERRAMENTAS CIENTÍFICAS: MATEMÁTICA, 3D, DESENHO, MATRIZES, FLASHCARDS E EXPORTAÇÃO -->
            <button class="tb-btn tb-highlight-math" onclick="toggleMathPalette()" title="Inserir Fórmulas e Símbolos Matemáticos">∑ Matemática</button>
            <button class="tb-btn tb-highlight-3d" onclick="open3DVectorStudio()" title="Abrir Estúdio de Vetores e Gráfico 3D (Eixos X, Y, Z)">🌐 Vetores & 3D</button>
            <button class="tb-btn tb-highlight-draw" onclick="openWhiteboardDrawer()" title="Abrir Lousa para Desenhar Formas Geométricas 2D">✏️ Desenhar</button>
            <button class="tb-btn" onclick="openMatrixCalculator()" title="Abrir Calculadora de Matrizes e Vetores">🧮 Matrizes</button>
            <button class="tb-btn" onclick="openFlashcardsReviewModal()" title="Revisar Flashcards das suas anotações">🗂️ Flashcards</button>
            <button class="tb-btn" onclick="openExportModal()" title="Exportar Caderno em Markdown, PDF ou JSON">📥 Exportar</button>
          </div>

          <div class="toolbar-templates">
            <select class="tb-select" onchange="insertNoteTemplate(this.value); this.value='';">
              <option value="" disabled selected>+ Inserir Modelo...</option>
              <option value="summary">📝 Resumo de Aula</option>
              <option value="table">📊 Tabela de Comparação</option>
              <option value="code">💻 Exemplo Prático Python</option>
              <option value="math_vectors">📐 Vetores & Álgebra Linear</option>
              <option value="schema">📐 Esquema de Fluxo</option>
              <option value="flashcard">🗂️ Novo Flashcard (Pergunta / Resposta)</option>
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
Assista ao vídeo na esquerda e faça suas anotações diretamente aqui na direita!" oninput="onNoteEditorInput()"></textarea>
          </div>
          <div class="note-preview-pane">
            <div class="preview-header">👁️ Pré-visualização Formatada (Markdown / KaTeX / Tabelas / Imagens)</div>
            <div class="preview-body" id="modal-preview-body"></div>
          </div>
        </div>

        <!-- RODAPÉ -->
        <div class="note-modal-footer">
          <div class="footer-stats" id="modal-footer-stats">0 palavras · 0 caracteres</div>
          <div class="footer-sync" id="modal-sync-indicator">💾 Salvo automaticamente</div>
          <div class="footer-actions">
            <button class="note-clear-btn" onclick="clearModalNote()">Limpar</button>
            <button class="note-save-btn" onclick="closeNoteModal()">💾 Salvar & Fechar</button>
          </div>
        </div>
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
<!-- SUBMODAL 1: REVISÃO DE FLASHCARDS & REPETIÇÃO ESPAÇADA (ANKI LITE)      -->
<!-- ======================================================================= -->
<div id="modal-flashcards" class="modal-sub-overlay" hidden>
  <div class="modal-sub-box modal-fc-box">
    <div class="modal-sub-header">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:1.3rem">🗂️</span>
        <h3 style="margin:0;font-size:1.15rem;color:var(--tx)">Revisão de Flashcards & Repetição Espaçada</h3>
      </div>
      <div style="display:flex;align-items:center;gap:10px">
        <span id="fc-counter" style="font-size:.84rem;font-weight:750;color:var(--mu)">1/1</span>
        <button class="note-close-btn" onclick="closeFlashcardsModal()">✕</button>
      </div>
    </div>

    <div class="fc-card-viewport">
      <div class="fc-card-inner">
        <div>
          <span class="fc-card-tag" id="fc-card-tag">CARD 1 · Tópico</span>
          <div class="fc-card-content" id="fc-card-content">Pergunta do flashcard</div>
        </div>

        <div class="fc-card-answer-wrap" id="fc-card-answer-wrap">
          <div style="font-size:.76rem;text-transform:uppercase;color:var(--mu);margin-bottom:6px">Resposta Correta:</div>
          <div id="fc-card-answer-text">Texto da resposta</div>
        </div>
      </div>
    </div>

    <div class="fc-actions-bar">
      <button class="fc-reveal-btn" id="fc-reveal-btn" onclick="flipFlashcard()">👁️ Revelar Resposta</button>
      <div class="fc-rating-btns" id="fc-rating-btns">
        <button class="fc-rate-btn rate-hard" onclick="rateFlashcard('hard')">
          <span>🔴 Difícil</span>
          <span style="font-size:.7rem;opacity:.85">1 dia</span>
        </button>
        <button class="fc-rate-btn rate-good" onclick="rateFlashcard('good')">
          <span>🟡 Bom</span>
          <span style="font-size:.7rem;opacity:.85">3 dias</span>
        </button>
        <button class="fc-rate-btn rate-easy" onclick="rateFlashcard('easy')">
          <span>🟢 Fácil</span>
          <span style="font-size:.7rem;opacity:.85">7 dias</span>
        </button>
      </div>
    </div>
  </div>
</div>

<!-- ======================================================================= -->
<!-- SUBMODAL 2: CALCULADORA DE MATRIZES E ÁLGEBRA LINEAR                    -->
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

<script>
const TRACK_ID = "__TRACK_ID__";
const TOTAL_TRACK_TOPICS = __TOTAL_TOPICS__;
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

function saveLocal() {
  try {
    localStorage.setItem(KEY, JSON.stringify(PR));
  } catch(e) {}
}

// 2. Sincronizar com Banco de Dados / API
async function initSync() {
  loadLocal();
  paint();

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
  let doneCount = 0, progCount = 0, zeroCount = 0, noteCount = 0;

  for (let i = 0; i < TOTAL_TRACK_TOPICS; i++) {
    const row = document.querySelector(`.topic-row[data-id^="${TRACK_ID}-"]`);
  }

  const allRows = document.querySelectorAll(`.topic-row`);
  let firstUncompletedRow = null;

  allRows.forEach(row => {
    const tid = row.getAttribute("data-id");
    const item = PR[tid] || { s: "z", n: "", d: "" };
    const status = item.s || "z";

    if (status === "e") doneCount++;
    else if (status === "r") progCount++;
    else zeroCount++;

    if (item.n && item.n.trim()) noteCount++;

    // Botão de status do tópico
    const sBtn = row.querySelector(".status-btn");
    if (sBtn) {
      sBtn.className = `status-btn status-btn-${status}`;
      if (status === "e") sBtn.textContent = "🟢 Concluído";
      else if (status === "r") sBtn.textContent = "🟡 Falta terminar";
      else sBtn.textContent = "🔴 Do zero";
    }

    // Botão de anotações
    const nBtn = row.querySelector(".note-btn");
    if (nBtn) {
      const hasNote = item.n && item.n.trim().length > 0;
      nBtn.className = `note-btn ${hasNote ? 'has-note' : ''}`;
      nBtn.textContent = hasNote ? "📝 Anotações *" : "📝 Anotações & Estudo";
    }

    // Identificar primeiro não concluído para recomendação
    if (!firstUncompletedRow && status !== "e") {
      firstUncompletedRow = row;
    }

    // Aplicar Filtro e Busca
    applyRowVisibility(row, status, item.n || "");
  });

  // Atualizar Contadores
  const elDone = document.getElementById("stat-done");
  const elProg = document.getElementById("stat-prog");
  const elZero = document.getElementById("stat-zero");
  const elNotes = document.getElementById("stat-notes");

  if (elDone) elDone.textContent = doneCount;
  if (elProg) elProg.textContent = progCount;
  if (elZero) elZero.textContent = zeroCount;
  if (elNotes) elNotes.textContent = noteCount;

  // Barra de Progresso
  const total = TOTAL_TRACK_TOPICS || 1;
  const pctE = Math.round((doneCount / total) * 100);
  const pctR = Math.round((progCount / total) * 100);
  const pctZ = Math.max(0, 100 - pctE - pctR);

  const barE = document.getElementById("bar-e");
  const barR = document.getElementById("bar-r");
  const barZ = document.getElementById("bar-z");
  const pctLabel = document.getElementById("prog-pct-label");

  if (barE) barE.style.width = `${pctE}%`;
  if (barR) barR.style.width = `${pctR}%`;
  if (barZ) barZ.style.width = `${pctZ}%`;
  if (pctLabel) pctLabel.textContent = `${pctE}% Concluído (${doneCount}/${total})`;

  // Gamificação / Patente de XP
  const lvlIcon = document.getElementById("lvl-icon");
  const lvlName = document.getElementById("lvl-name");
  const lvlDesc = document.getElementById("lvl-desc");
  const lvlXpTxt = document.getElementById("lvl-xp-txt");
  const lvlXpFill = document.getElementById("lvl-xp-fill");

  if (lvlXpTxt) lvlXpTxt.textContent = `${doneCount} / ${total} concluídos (${pctE}%)`;
  if (lvlXpFill) lvlXpFill.style.width = `${pctE}%`;

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

  // Próximo Passo Recomendado
  const nextTitle = document.getElementById("next-step-title");
  if (nextTitle) {
    if (firstUncompletedRow) {
      const tName = firstUncompletedRow.querySelector(".topic-title-text")?.textContent || "";
      nextTitle.textContent = tName;
    } else {
      nextTitle.textContent = "🎉 Todos os tópicos desta trilha foram concluídos com sucesso!";
    }
  }

  // Diagnóstico de Ritmo
  const statusCard = document.getElementById("pace-status-card");
  const statusText = document.getElementById("pace-status-text");
  const statusTag = document.getElementById("pace-status-tag");
  if (statusCard && statusText && statusTag) {
    if (pctE > 0) {
      statusCard.className = "pace-status-card pace-ahead";
      statusTag.textContent = "🟢 Em Progresso";
      statusText.innerHTML = `Ritmo Ativo! <b>${doneCount} de ${total} tópicos concluídos</b> (${pctE}%). Continue registrando seu progresso diariamente!`;
    } else {
      statusCard.className = "pace-status-card pace-ontrack";
      statusTag.textContent = "🚀 Ponto de Partida";
      statusText.innerHTML = `Pronto para começar! Clique em <b>▶ Vídeo</b> ou <b>📝 Anotações & Estudo</b> em qualquer tópico para abrir o estúdio de estudo integrado.`;
    }
  }
}

// 4. Alternância de Status
function cycleStatus(topicId) {
  if (!PR[topicId]) PR[topicId] = { s: "z", n: "", d: "" };
  const cur = PR[topicId].s || "z";
  let next = "z";
  if (cur === "z") next = "r";
  else if (cur === "r") next = "e";
  else next = "z";

  PR[topicId].s = next;
  saveLocal();
  paint();
  syncTopicToServer(topicId);
}

function updateModalStatusBtn(status) {
  const btn = document.getElementById("modal-status-btn");
  if (!btn) return;
  if (status === "e") {
    btn.textContent = "🟢 Concluído";
    btn.style.color = "var(--e)";
  } else if (status === "r") {
    btn.textContent = "🟡 Falta terminar";
    btn.style.color = "var(--r)";
  } else {
    btn.textContent = "🔴 Do zero";
    btn.style.color = "var(--z)";
  }
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

function applyRowVisibility(row, status, noteText) {
  let matchFilter = true;
  if (FILTER === "z") matchFilter = status === "z";
  else if (FILTER === "r") matchFilter = status === "r";
  else if (FILTER === "e") matchFilter = status === "e";
  else if (FILTER === "n") matchFilter = noteText.trim().length > 0;

  let matchSearch = true;
  if (SEARCH_QUERY) {
    const text = row.textContent.toLowerCase();
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
    if (item.s !== "e") {
      row.scrollIntoView({ behavior: "smooth", block: "center" });
      row.style.boxShadow = "0 0 0 4px var(--ac)";
      setTimeout(() => { row.style.boxShadow = ""; }, 1800);
      break;
    }
  }
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
  const savedTheme = localStorage.getItem("roteiro-theme");
  if (savedTheme) document.documentElement.setAttribute("data-theme", savedTheme);
} catch(e) {}

window.addEventListener("DOMContentLoaded", () => {
  initSync();
  if (typeof initSplitResizer === "function") initSplitResizer();
  if (typeof updatePomodoroUI === "function") updatePomodoroUI();
});
</script>
</body>
</html>
"""

    rendered = (template
        .replace("__PAGE_TITLE__", page_title)
        .replace("__PAGE_SUB__", page_sub)
        .replace("__TRACK_ICON__", track_icon)
        .replace("__TRACK_ID__", track_id)
        .replace("__TOTAL_TOPICS__", str(total_topics))
        .replace("__SHARED_CSS__", shared_css)
        .replace("__ACTIVE_HUB__", active_hub)
        .replace("__ACTIVE_IA__", active_ia)
        .replace("__ACTIVE_MAT__", active_mat)
        .replace("__ACTIVE_ING__", active_ing)
        .replace("__SIDEBAR_TREE__", sb_tree_str)
        .replace("__PHASES_CONTENT__", phases_str)
        .replace("__TOPICS_MAP_JSON__", topics_map_json)
        .replace("__STUDIO_JS__", STUDIO_JS)
    )

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Gerado: {out_path} ({total_topics} tópicos enriquecidos)")
