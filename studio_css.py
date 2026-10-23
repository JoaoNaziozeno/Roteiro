# -*- coding: utf-8 -*-
"""
CSS Adicional para o Estúdio Unificado de Estudo (Vídeo à Esquerda + Anotações à Direita),
Progresso Automático, Estúdio 3D de Vetores & Geometria e Lousa de Desenho 2D.
"""

STUDIO_CSS = """
/* =========================================================================
   ESTÚDIO UNIFICADO DE ESTUDO & ANOTAÇÕES (VÍDEO À ESQUERDA | NOTAS À DIREITA)
   ========================================================================= */
.unified-study-box {
  max-width: 1560px !important;
  width: 96vw !important;
  height: 94vh !important;
  max-height: 980px !important;
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important;
  border-radius: 16px;
  box-shadow: 0 28px 70px rgba(0,0,0,.55);
}

/* Switch de Progresso Automático */
.auto-prog-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: .78rem;
  font-weight: 700;
  color: var(--tx);
  background: var(--bg);
  padding: 4px 12px;
  border-radius: 99px;
  border: 1px solid var(--bd);
  user-select: none;
}
.switch {
  position: relative;
  display: inline-block;
  width: 32px;
  height: 18px;
}
.switch input { opacity: 0; width: 0; height: 0; }
.slider {
  position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
  background-color: var(--bd); transition: .2s; border-radius: 99px;
}
.slider:before {
  position: absolute; content: ""; height: 12px; width: 12px; left: 3px; bottom: 3px;
  background-color: white; transition: .2s; border-radius: 50%;
}
input:checked + .slider { background-color: var(--e); }
input:checked + .slider:before { transform: translateX(14px); }

/* Layout Dividido em Duas Colunas: Vídeo à Esquerda e Anotações à Direita */
.study-columns-layout {
  display: flex;
  flex-direction: row;
  flex: 1;
  min-height: 0;
  overflow: hidden;
  background: var(--card);
}

/* Coluna da Esquerda: Vídeo & Sessão de Estudo */
.study-player-col {
  flex: 0 0 50%;
  width: 50%;
  max-width: 50%;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--bd);
  background: var(--card);
  overflow-y: auto;
  overflow-x: hidden;
  transition: all .25s ease;
}

.study-player-topbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 10px 16px;
  background: var(--bg);
  border-bottom: 1px solid var(--bd);
}

.player-topbar-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: .84rem;
  min-width: 0;
}

.player-source-tag {
  font-size: .72rem;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 6px;
  background: var(--ac);
  color: #fff;
  letter-spacing: .02em;
  white-space: nowrap;
}

.player-source-title {
  font-weight: 700;
  color: var(--tx);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 240px;
}

.player-topbar-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.player-ext-btn {
  font-size: .76rem;
  font-weight: 650;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid var(--bd);
  background: var(--card);
  color: var(--tx);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: .15s;
  white-space: nowrap;
}
.player-ext-btn:hover { border-color: var(--ac); color: var(--ac); }
.player-ext-btn.doc-ext { background: rgba(79,70,229,.1); border-color: rgba(79,70,229,.3); color: var(--ac); }

.player-collapse-btn {
  font: inherit;
  font-size: .76rem;
  font-weight: 650;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid var(--bd);
  background: var(--card);
  color: var(--tx);
  cursor: pointer;
  transition: .15s;
  white-space: nowrap;
}
.player-collapse-btn:hover { background: var(--bd); }

/* Responsive Video Wrapper em 16:9 */
.video-responsive-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #000;
  overflow: hidden;
  transition: all .3s cubic-bezier(.4,0,.2,1);
}
.video-responsive-wrap.collapsed {
  display: none !important;
}
.video-responsive-wrap iframe {
  width: 100%;
  height: 100%;
  border: none;
  display: block;
}

/* Barra de Progresso da Sessão / Auto-Progresso */
.session-progress-bar-wrap {
  padding: 8px 16px;
  background: var(--card);
  border-top: 1px solid var(--bd);
  border-bottom: 1px solid var(--bd);
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.session-progress-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: .76rem;
  color: var(--mu);
}

.session-finish-btn {
  font: inherit;
  font-size: .74rem;
  font-weight: 750;
  padding: 3px 10px;
  border-radius: 6px;
  border: none;
  background: var(--e);
  color: #fff;
  cursor: pointer;
  transition: .15s;
  white-space: nowrap;
}
.session-finish-btn:hover { opacity: .9; transform: scale(1.02); }

.session-bar-track {
  height: 5px;
  background: var(--bd);
  border-radius: 99px;
  overflow: hidden;
}
.session-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--ac), var(--e));
  border-radius: 99px;
  transition: width .5s linear;
}

/* Card de contexto e dicas no painel esquerdo */
.study-left-extra-info {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
  background: var(--bg);
}
.study-left-card {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 10px;
  padding: 14px 16px;
  box-shadow: 0 2px 6px rgba(0,0,0,.03);
}
.study-left-card-title {
  font-size: .84rem;
  font-weight: 750;
  color: var(--tx);
  margin-bottom: 6px;
}
.study-left-card p {
  font-size: .8rem;
  line-height: 1.55;
  color: var(--mu);
  margin: 0;
}

/* Coluna da Direita: Caderno de Anotações & Esquemas */
.study-notes-col {
  flex: 1 1 50%;
  width: 50%;
  display: flex;
  flex-direction: column;
  min-height: 0;
  min-width: 0;
  background: var(--card);
  overflow: hidden;
}

.notes-section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  background: var(--card);
  border-bottom: 1px solid var(--bd);
}

.notes-head-title {
  font-size: .88rem;
  font-weight: 750;
  color: var(--tx);
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Botões especiais na Toolbar */
.tb-btn.tb-highlight-math {
  background: rgba(79,70,229,.1);
  border-color: rgba(79,70,229,.35);
  color: var(--ac);
  font-weight: 750;
}
.tb-btn.tb-highlight-math:hover { background: var(--ac); color: #fff; }

.tb-btn.tb-highlight-3d {
  background: rgba(139,92,246,.12);
  border-color: rgba(139,92,246,.35);
  color: #8b5cf6;
  font-weight: 750;
}
.tb-btn.tb-highlight-3d:hover { background: #8b5cf6; color: #fff; }

.tb-btn.tb-highlight-draw {
  background: rgba(6,182,212,.12);
  border-color: rgba(6,182,212,.35);
  color: #06b6d4;
  font-weight: 750;
}
.tb-btn.tb-highlight-draw:hover { background: #06b6d4; color: #fff; }

/* Paleta de Símbolos Matemáticos */
.math-palette-wrap {
  background: var(--bg);
  border-bottom: 1px solid var(--bd);
  padding: 10px 16px;
  animation: noteFadeIn .18s ease;
}
.math-palette-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: .8rem;
  font-weight: 750;
  color: var(--tx);
}
.math-palette-close {
  background: transparent;
  border: none;
  font-size: .95rem;
  color: var(--mu);
  cursor: pointer;
}
.math-symbols-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 8px;
}
.sym-btn {
  font: inherit;
  font-size: .78rem;
  font-weight: 650;
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid var(--bd);
  background: var(--card);
  color: var(--tx);
  cursor: pointer;
  transition: .12s;
}
.sym-btn:hover {
  border-color: var(--ac);
  color: var(--ac);
  transform: translateY(-1px);
}
.math-templates-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  padding-top: 6px;
  border-top: 1px dashed var(--bd);
}
.sym-tmpl-btn {
  font: inherit;
  font-size: .74rem;
  font-weight: 650;
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid rgba(79,70,229,.25);
  background: rgba(79,70,229,.07);
  color: var(--ac);
  cursor: pointer;
  transition: .15s;
}
.sym-tmpl-btn:hover { background: var(--ac); color: #fff; }

/* Modos de visualização do Workspace de Anotações */
.note-workspace {
  display: flex;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.note-workspace.mode-editor .note-editor-pane {
  flex: 1;
  border-right: none;
}
.note-workspace.mode-editor .note-preview-pane {
  display: none !important;
}

.note-workspace.mode-preview .note-editor-pane {
  display: none !important;
}
.note-workspace.mode-preview .note-preview-pane {
  flex: 1;
}

.note-workspace.mode-split {
  flex-direction: column;
}
.note-workspace.mode-split .note-editor-pane {
  flex: 1 1 50%;
  border-right: none;
  border-bottom: 1px solid var(--bd);
  min-height: 140px;
}
.note-workspace.mode-split .note-preview-pane {
  flex: 1 1 50%;
  min-height: 140px;
}

@media (min-width: 1440px) {
  .note-workspace.mode-split {
    flex-direction: row;
  }
  .note-workspace.mode-split .note-editor-pane {
    border-right: 1px solid var(--bd);
    border-bottom: none;
  }
}

/* Responsividade em Telas Pequenas e Tablets */
@media (max-width: 1040px) {
  .study-columns-layout {
    flex-direction: column !important;
    overflow-y: auto !important;
  }
  .study-player-col {
    flex: 0 0 auto !important;
    width: 100% !important;
    max-width: 100% !important;
    border-right: none !important;
    border-bottom: 1px solid var(--bd) !important;
  }
  .study-notes-col {
    flex: 1 0 auto !important;
    width: 100% !important;
    min-height: 580px !important;
  }
}

/* Submodais: Estúdio 3D e Lousa de Desenho */
.modal-sub-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.78);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 1050;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 16px;
  animation: noteFadeIn .2s ease;
}
.modal-sub-overlay.active {
  display: flex !important;
}
.modal-sub-overlay[hidden] {
  display: none !important;
}

.modal-sub-box {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 16px;
  box-shadow: 0 24px 60px rgba(0,0,0,.5);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-3d-box {
  max-width: 1050px;
  width: 95vw;
  max-height: 90vh;
}

.modal-sub-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  background: var(--card);
  border-bottom: 1px solid var(--bd);
}

.modal-3d-body {
  display: flex;
  flex-wrap: wrap;
  overflow-y: auto;
  max-height: calc(90vh - 65px);
}

.canvas-3d-wrap {
  flex: 1 1 500px;
  background: #0f1218;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 1px solid var(--bd);
  user-select: none;
}
#canvas-3d {
  width: 100%;
  max-width: 650px;
  height: 440px;
  cursor: grab;
}
#canvas-3d:active { cursor: grabbing; }

.canvas-3d-overlay-hint {
  position: absolute;
  top: 12px;
  left: 14px;
  font-size: .74rem;
  font-weight: 650;
  color: rgba(255,255,255,.7);
  background: rgba(0,0,0,.6);
  padding: 4px 10px;
  border-radius: 6px;
  pointer-events: none;
}

.canvas-3d-axes-legend {
  position: absolute;
  bottom: 12px;
  left: 14px;
  display: flex;
  gap: 10px;
  font-size: .76rem;
  font-weight: 750;
  background: rgba(0,0,0,.6);
  padding: 4px 10px;
  border-radius: 6px;
  pointer-events: none;
}

.controls-3d-wrap {
  flex: 1 1 340px;
  padding: 18px 20px;
  background: var(--card);
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.v3d-panel-title {
  font-size: .95rem;
  font-weight: 800;
  color: var(--tx);
}

.v3d-vector-card {
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 10px;
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.v3d-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: .84rem;
}
.v3d-norm-tag {
  font-size: .76rem;
  font-weight: 750;
  color: var(--mu);
}
.v3d-inputs-row {
  display: flex;
  gap: 10px;
}
.v3d-inputs-row label {
  font-size: .8rem;
  font-weight: 700;
  color: var(--tx);
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
}
.v3d-inputs-row input[type="number"] {
  font: inherit;
  font-size: .82rem;
  padding: 4px 6px;
  border-radius: 6px;
  border: 1px solid var(--bd);
  background: var(--card);
  color: var(--tx);
  width: 100%;
}

.v3d-options-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 8px 12px;
  background: var(--bg);
  border-radius: 8px;
  border: 1px solid var(--bd);
}
.v3d-opt-label {
  font-size: .8rem;
  font-weight: 700;
  color: var(--tx);
  display: flex;
  align-items: center;
  gap: 6px;
}
.v3d-select {
  font: inherit;
  font-size: .78rem;
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid var(--bd);
  background: var(--card);
  color: var(--tx);
}

.v3d-math-results {
  background: rgba(79,70,229,.07);
  border: 1px solid rgba(79,70,229,.25);
  border-radius: 10px;
  padding: 10px 14px;
  font-size: .82rem;
  line-height: 1.6;
  color: var(--tx);
}
.v3d-math-results b { color: var(--ac); }

.v3d-actions-row {
  display: flex;
  gap: 10px;
  margin-top: 6px;
}
.v3d-snapshot-btn {
  flex: 1;
  font: inherit;
  font-size: .84rem;
  font-weight: 750;
  padding: 10px 14px;
  border-radius: 8px;
  border: none;
  background: #8b5cf6;
  color: #fff;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(139,92,246,.35);
  transition: .18s;
}
.v3d-snapshot-btn:hover { background: #7c3aed; transform: translateY(-1px); }

.v3d-reset-btn {
  font: inherit;
  font-size: .8rem;
  font-weight: 650;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid var(--bd);
  background: var(--bg);
  color: var(--tx);
  cursor: pointer;
}
.v3d-reset-btn:hover { background: var(--bd); }

/* Lousa de Desenho 2D */
.modal-draw-box {
  max-width: 900px;
  width: 95vw;
}
.draw-toolbar {
  padding: 10px 16px;
  background: var(--bg);
  border-bottom: 1px solid var(--bd);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}
.draw-tool-group {
  display: flex;
  gap: 4px;
}
.draw-tool-btn {
  font: inherit;
  font-size: .78rem;
  padding: 5px 10px;
  border-radius: 6px;
  border: 1px solid var(--bd);
  background: var(--card);
  color: var(--tx);
  cursor: pointer;
  transition: .15s;
}
.draw-tool-btn.active {
  background: var(--ac);
  border-color: var(--ac);
  color: #fff;
  font-weight: 700;
}

.draw-color-group {
  display: flex;
  align-items: center;
  gap: 6px;
}
.color-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  cursor: pointer;
  transition: transform .15s;
}
.color-dot.active {
  transform: scale(1.25);
  box-shadow: 0 0 0 2px var(--card), 0 0 0 4px var(--ac);
}

.draw-action-group {
  display: flex;
  gap: 8px;
}
.draw-act-btn {
  font: inherit;
  font-size: .78rem;
  padding: 5px 12px;
  border-radius: 6px;
  border: 1px solid var(--bd);
  background: var(--card);
  color: var(--tx);
  cursor: pointer;
}
.draw-insert-btn {
  background: var(--ac);
  border-color: var(--ac);
  color: #fff;
  font-weight: 700;
}
.draw-insert-btn:hover { background: var(--ac-hover); }

.draw-canvas-wrap {
  background: #11141c;
  display: flex;
  justify-content: center;
  overflow: hidden;
}
#whiteboard-canvas {
  max-width: 100%;
  height: 450px;
  cursor: crosshair;
}

/* Toast de Notificação */
.toast-notice {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%) translateY(20px);
  background: var(--card);
  color: var(--tx);
  border: 1px solid var(--ac);
  border-radius: 99px;
  padding: 10px 20px;
  font-size: .86rem;
  font-weight: 700;
  box-shadow: 0 10px 30px rgba(0,0,0,.3);
  z-index: 2000;
  opacity: 0;
  transition: all .25s ease;
  pointer-events: none;
}
.toast-notice.show {
  transform: translateX(-50%) translateY(0);
  opacity: 1;
}

/* =========================================================================
   BARRA DIVISÓRIA ARRASTÁVEL (SPLIT RESIZER)
   ========================================================================= */
.study-split-resizer {
  width: 8px;
  background: var(--bg);
  border-left: 1px solid var(--bd);
  border-right: 1px solid var(--bd);
  cursor: col-resize;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;
  transition: background .15s ease;
  z-index: 5;
}
.study-split-resizer:hover, .study-split-resizer.dragging {
  background: var(--ac);
  border-color: var(--ac);
}
.resizer-handle {
  width: 2px;
  height: 28px;
  background: var(--mu);
  border-radius: 2px;
  transition: all .15s ease;
}
.study-split-resizer:hover .resizer-handle, .study-split-resizer.dragging .resizer-handle {
  background: #fff;
  height: 40px;
}

/* =========================================================================
   MARCADORES DE TEMPO INTERATIVOS NO VÍDEO (TIMESTAMPS)
   ========================================================================= */
.note-timestamp-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 7px;
  font-family: inherit;
  font-size: .76rem;
  font-weight: 750;
  border-radius: 6px;
  background: rgba(79,70,229,.12);
  border: 1px solid rgba(79,70,229,.35);
  color: var(--ac);
  cursor: pointer;
  text-decoration: none;
  transition: all .15s ease;
  margin: 0 2px;
}
.note-timestamp-pill:hover {
  background: var(--ac);
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(79,70,229,.3);
}

/* =========================================================================
   TEMPORIZADOR POMODORO INTEGRADO
   ========================================================================= */
.pomodoro-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--bg);
  padding: 3px 10px;
  border-radius: 99px;
  border: 1px solid var(--bd);
  user-select: none;
}
.pomo-toggle-btn {
  font: inherit;
  font-size: .78rem;
  font-weight: 750;
  padding: 2px 6px;
  border: none;
  background: transparent;
  color: var(--tx);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: .15s;
}
.pomo-toggle-btn.running {
  color: #ef4444;
  animation: pomoPulse 1.5s infinite;
}
@keyframes pomoPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: .65; }
}
.pomo-reset-btn {
  font: inherit;
  font-size: .78rem;
  padding: 1px 4px;
  border: none;
  background: transparent;
  color: var(--mu);
  cursor: pointer;
}
.pomo-reset-btn:hover { color: var(--tx); }
.pomo-count-badge {
  font-size: .72rem;
  font-weight: 800;
  color: var(--mu);
  padding-left: 4px;
  border-left: 1px solid var(--bd);
}

/* =========================================================================
   BOTÕES DE UNDO / REDO & ÁUDIO
   ========================================================================= */
.tb-btn-undo, .tb-btn-redo {
  font-size: .84rem !important;
  font-weight: 800 !important;
}
.tb-audio-btn {
  background: rgba(16,185,129,.1) !important;
  border-color: rgba(16,185,129,.35) !important;
  color: #10b981 !important;
  font-weight: 750 !important;
}
.tb-audio-btn:hover {
  background: #10b981 !important;
  color: #fff !important;
}

/* =========================================================================
   FLASHCARDS NAS ANOTAÇÕES & MODAL DE REVISÃO (ANKI LITE)
   ========================================================================= */
.note-flashcard-box {
  background: var(--bg);
  border-left: 4px solid #f59e0b;
  border-radius: 0 8px 8px 0;
  padding: 12px 16px;
  margin: 12px 0;
}
.note-flashcard-title {
  font-size: .78rem;
  font-weight: 800;
  color: #f59e0b;
  text-transform: uppercase;
  letter-spacing: .04em;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.note-flashcard-q {
  font-weight: 700;
  color: var(--tx);
  margin-bottom: 4px;
}
.note-flashcard-a {
  color: var(--mu);
  font-size: .92rem;
}

.modal-fc-box {
  max-width: 680px;
  width: 95vw;
}
.fc-card-viewport {
  perspective: 1000px;
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: var(--bg);
}
.fc-card-inner {
  width: 100%;
  min-height: 220px;
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,.08);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 24px;
  text-align: center;
  position: relative;
  transition: all .25s ease;
}
.fc-card-tag {
  font-size: .72rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--mu);
  letter-spacing: .05em;
}
.fc-card-content {
  font-size: 1.15rem;
  font-weight: 650;
  color: var(--tx);
  line-height: 1.6;
  margin: 18px 0;
}
.fc-card-answer-wrap {
  display: none;
  animation: noteFadeIn .2s ease;
  padding-top: 14px;
  border-top: 1px dashed var(--bd);
  font-size: 1.05rem;
  color: var(--ac);
  font-weight: 600;
}
.fc-card-answer-wrap.show {
  display: block;
}
.fc-actions-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 20px;
  background: var(--card);
  border-top: 1px solid var(--bd);
}
.fc-reveal-btn {
  font: inherit;
  font-size: .88rem;
  font-weight: 750;
  padding: 10px 24px;
  border-radius: 8px;
  border: none;
  background: var(--ac);
  color: #fff;
  cursor: pointer;
  transition: .15s;
}
.fc-reveal-btn:hover { background: var(--ac-hover); }
.fc-rating-btns {
  display: none;
  align-items: center;
  gap: 10px;
  width: 100%;
}
.fc-rating-btns.show {
  display: flex;
}
.fc-rate-btn {
  flex: 1;
  font: inherit;
  font-size: .82rem;
  font-weight: 750;
  padding: 10px 12px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: .15s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}
.fc-rate-btn.rate-hard { background: rgba(239,68,68,.12); color: #ef4444; border: 1px solid rgba(239,68,68,.3); }
.fc-rate-btn.rate-good { background: rgba(245,158,11,.12); color: #f59e0b; border: 1px solid rgba(245,158,11,.3); }
.fc-rate-btn.rate-easy { background: rgba(16,185,129,.12); color: #10b981; border: 1px solid rgba(16,185,129,.3); }
.fc-rate-btn:hover { transform: translateY(-2px); filter: brightness(1.08); }

/* =========================================================================
   CALCULADORA DE MATRIZES & VETORES
   ========================================================================= */
.modal-calc-box {
  max-width: 880px;
  width: 95vw;
}
.calc-tabs {
  display: flex;
  border-bottom: 1px solid var(--bd);
  background: var(--bg);
}
.calc-tab-btn {
  font: inherit;
  font-size: .84rem;
  font-weight: 700;
  padding: 12px 20px;
  border: none;
  background: transparent;
  color: var(--mu);
  cursor: pointer;
  border-bottom: 2px solid transparent;
}
.calc-tab-btn.active {
  color: var(--ac);
  border-bottom-color: var(--ac);
  background: var(--card);
}
.calc-tab-pane {
  display: none;
  padding: 20px;
  flex-direction: column;
  gap: 16px;
}
.calc-tab-pane.active {
  display: flex;
}
.calc-matrices-row {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}
.calc-matrix-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.calc-matrix-title {
  font-size: .84rem;
  font-weight: 750;
  color: var(--tx);
}
.calc-matrix-grid {
  display: grid;
  grid-template-columns: repeat(2, 60px);
  gap: 6px;
}
.calc-matrix-grid.dim-3 {
  grid-template-columns: repeat(3, 50px);
}
.calc-matrix-grid input {
  font: inherit;
  font-size: .86rem;
  padding: 8px 4px;
  text-align: center;
  border-radius: 6px;
  border: 1px solid var(--bd);
  background: var(--bg);
  color: var(--tx);
}
.calc-actions-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.calc-op-btn {
  font: inherit;
  font-size: .8rem;
  font-weight: 700;
  padding: 8px 14px;
  border-radius: 6px;
  border: 1px solid var(--bd);
  background: var(--card);
  color: var(--tx);
  cursor: pointer;
  transition: .15s;
}
.calc-op-btn:hover {
  border-color: var(--ac);
  color: var(--ac);
}
.calc-result-box {
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 10px;
  padding: 16px;
  font-family: inherit;
  font-size: .95rem;
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* =========================================================================
   MODAL DE EXPORTAÇÃO DO CADERNO
   ========================================================================= */
.modal-export-box {
  max-width: 720px;
  width: 95vw;
}
.export-options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 14px;
  padding: 24px;
  background: var(--bg);
}
.export-card-btn {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 12px;
  padding: 20px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
  cursor: pointer;
  transition: all .2s ease;
  font: inherit;
}
.export-card-btn:hover {
  border-color: var(--ac);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,.08);
}
.export-card-icon {
  font-size: 2rem;
}
.export-card-title {
  font-size: .92rem;
  font-weight: 750;
  color: var(--tx);
}
.export-card-desc {
  font-size: .78rem;
  color: var(--mu);
  line-height: 1.45;
}

"""
