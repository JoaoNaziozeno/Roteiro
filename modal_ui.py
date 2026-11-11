# -*- coding: utf-8 -*-
"""
Sistema visual dos modais ("Foco").

Uma única camada de estilo, carregada por último em todas as páginas, que padroniza:
  - o estúdio de estudo (#note-modal): cabeçalho, player, progresso da sessão, caderno e aula visual;
  - os submodais (.modal-sub-*): Estúdio 3D, Lousa, Matrizes, Exportar, login/credenciais, projetos;
  - a leitura dos blocos da Aula Visual (.lv2), que deixam de ser cartões e viram texto corrido.

Nada aqui muda conteúdo, ids ou funções: só tokens, tipografia, espaçamento e superfícies.
"""

MODAL_UI_CSS = r"""
<style id="modal-ui">
/* ============================ TOKENS ============================ */
.note-modal-overlay,.modal-sub-overlay{
  --m-bg:var(--card);
  --m-sunk:color-mix(in srgb,var(--tx) 4%,var(--card));
  --m-hover:color-mix(in srgb,var(--tx) 7%,transparent);
  --m-line:color-mix(in srgb,var(--tx) 10%,transparent);
  --m-line-2:color-mix(in srgb,var(--tx) 17%,transparent);
  --m-tx:var(--tx);--m-mu:var(--mu);
  --m-acc:var(--t,var(--t-hub,#5eead4));
  --m-ok:#2fa36b;--m-warn:#d99a00;--m-bad:#e5484d;
  --m-r1:6px;--m-r2:10px;--m-r3:14px;
  --m-fs-xs:.75rem;--m-fs-sm:.8125rem;--m-fs:.875rem;
  --m-ease:cubic-bezier(.2,.8,.2,1);
  font-family:var(--ds-font,system-ui,sans-serif);
}
.note-modal-overlay,.modal-sub-overlay{background:color-mix(in srgb,#020608 62%,transparent)!important;backdrop-filter:blur(6px)!important;-webkit-backdrop-filter:blur(6px)!important}

/* Rolagem discreta em tudo que está dentro de um modal */
.note-modal-overlay *,.modal-sub-overlay *{scrollbar-width:thin;scrollbar-color:color-mix(in srgb,var(--tx) 16%,transparent) transparent}
.note-modal-overlay ::-webkit-scrollbar,.modal-sub-overlay ::-webkit-scrollbar{width:8px;height:8px}
.note-modal-overlay ::-webkit-scrollbar-thumb,.modal-sub-overlay ::-webkit-scrollbar-thumb{background:color-mix(in srgb,var(--tx) 14%,transparent);border-radius:8px;border:2px solid transparent;background-clip:padding-box}
.note-modal-overlay ::-webkit-scrollbar-track,.modal-sub-overlay ::-webkit-scrollbar-track{background:transparent}

/* Botões base reutilizados */
.m-icon-btn{display:inline-grid;place-items:center;width:32px;height:32px;padding:0!important;border:0!important;border-radius:8px!important;background:transparent!important;color:var(--m-mu)!important;cursor:pointer;list-style:none;transition:background .15s,color .15s;font-size:0!important}
.m-icon-btn svg{fill:currentColor}
.m-icon-btn:hover{background:var(--m-hover)!important;color:var(--m-tx)!important}
.m-text-btn{font:500 var(--m-fs-sm)/1 var(--ds-font,inherit);padding:7px 10px;border:0;border-radius:8px;background:transparent;color:var(--m-mu);cursor:pointer;transition:background .15s,color .15s}
.m-text-btn:hover{background:var(--m-hover);color:var(--m-tx)}

/* ============================ ESTÚDIO: CAIXA ============================ */
#note-modal{padding:16px}
#note-modal .unified-study-box{
  width:min(1680px,100%)!important;max-width:none!important;height:100%!important;max-height:none!important;
  border-radius:16px!important;border:1px solid var(--m-line)!important;background:var(--m-bg)!important;
  box-shadow:0 40px 100px -30px rgba(0,0,0,.65)!important;animation:m-in .35s var(--m-ease)!important;
}
@keyframes m-in{from{opacity:0;transform:translateY(10px) scale(.99)}to{opacity:1;transform:none}}

/* Cabeçalho: uma linha, título à esquerda, ações à direita */
#note-modal .note-modal-header{
  display:flex;flex-wrap:nowrap;align-items:center;gap:16px;min-height:60px;padding:10px 14px 10px 22px;
  background:var(--m-bg);border-bottom:1px solid var(--m-line);
}
#note-modal .note-header-left{flex:1 1 auto;min-width:0;gap:3px}
#note-modal .note-breadcrumb{display:flex;align-items:center;gap:7px;font-size:.6875rem;font-weight:600;letter-spacing:.09em;color:var(--m-mu)}
#note-modal .note-breadcrumb::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--m-acc);flex:none}
#note-modal .note-topic-title{font-size:1.0625rem;font-weight:600;line-height:1.3;color:var(--m-tx);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#note-modal .note-header-right{flex:none;flex-wrap:nowrap;gap:6px;align-items:center}

/* Status: pílula neutra com ponto colorido */
#note-modal .note-status-pill{
  display:inline-flex;align-items:center;gap:8px;height:32px;padding:0 12px;border-radius:99px;
  border:1px solid var(--m-line)!important;background:transparent!important;color:var(--m-tx)!important;
  font:500 var(--m-fs-sm)/1 var(--ds-font,inherit);cursor:pointer;transition:background .15s,border-color .15s;
}
#note-modal .note-status-pill:hover{background:var(--m-hover)!important;border-color:var(--m-line-2)!important}
#note-modal .note-status-pill::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--m-bad)}
#note-modal .note-status-pill[data-s="r"]::before{background:var(--m-warn)}
#note-modal .note-status-pill[data-s="e"]::before{background:var(--m-ok)}

/* Opções da aula (progresso automático + meta) num menu */
.m-opts{position:relative}
.m-opts>summary::-webkit-details-marker{display:none}
.m-opts[open]>summary{background:var(--m-hover)!important;color:var(--m-tx)!important}
.m-opts-menu{
  position:absolute;top:calc(100% + 8px);right:0;z-index:20;width:300px;padding:6px;
  background:var(--m-bg);border:1px solid var(--m-line-2);border-radius:12px;box-shadow:0 24px 48px -16px rgba(0,0,0,.55);
  animation:m-in .18s var(--m-ease);
}
.m-opts-menu>*{display:flex!important;align-items:center;justify-content:space-between;gap:14px;padding:10px 12px!important;border-radius:8px;margin:0!important;border:0!important;background:transparent!important;font-size:var(--m-fs-sm)!important;color:var(--m-tx)!important;cursor:pointer}
.m-opts-menu>*:hover{background:var(--m-hover)!important}
.m-opts-text{display:flex;flex-direction:column;gap:3px;cursor:inherit}
.m-opts-text b{font-weight:600;color:var(--m-tx)}
.m-opts-text small{font-size:var(--m-fs-xs);color:var(--m-mu);font-weight:400}
.m-opts-menu input[type=date]{font:inherit;font-size:var(--m-fs-xs)!important;padding:6px 8px!important;border-radius:8px!important;border:1px solid var(--m-line-2)!important;background:var(--m-sunk)!important;color:var(--m-tx)!important;color-scheme:dark;max-width:132px}
:root[data-theme="light"] .m-opts-menu input[type=date]{color-scheme:light}
.m-opts-menu .switch{flex:none}
.m-opts-menu .slider{background:var(--m-line-2)}
.m-opts-menu input:checked+.slider{background:var(--m-ok)}

/* Próxima aula: a única ação primária do cabeçalho */
#note-modal .note-next-btn{
  height:32px;padding:0 14px!important;border-radius:8px!important;font:600 var(--m-fs-sm)/1 var(--ds-font,inherit)!important;
  background:var(--m-tx)!important;color:var(--m-bg)!important;border:0!important;display:inline-flex;align-items:center;gap:6px;margin-left:4px;
}
#note-modal .note-next-btn span{transition:transform .2s var(--m-ease)}
#note-modal .note-next-btn:hover:not(:disabled) span{transform:translateX(3px)}
#note-modal .note-close-btn{margin-left:2px}

/* ============================ ESTÚDIO: COLUNAS ============================ */
#note-modal .study-columns-layout{background:var(--m-bg)}
#note-modal .study-player-col{background:var(--m-bg);border-right:1px solid var(--m-line)}
#note-modal .study-notes-col{background:var(--m-bg)}
#note-modal .study-split-resizer{width:7px;margin:0 -3px;background:transparent;border:0;z-index:6}
#note-modal .study-split-resizer .resizer-handle{opacity:0;transition:opacity .15s}
#note-modal .study-split-resizer:hover .resizer-handle,#note-modal .study-split-resizer.dragging .resizer-handle{opacity:1}
#note-modal .study-split-resizer:hover,#note-modal .study-split-resizer.dragging{background:color-mix(in srgb,var(--m-acc) 35%,transparent)}

/* Barra do player: abas discretas, fonte como link */
#note-modal .study-player-topbar{min-height:44px;padding:6px 12px 6px 16px;background:var(--m-bg);border-bottom:1px solid var(--m-line);gap:12px}
#note-modal .player-source-tag{padding:0;background:transparent!important;color:var(--m-mu)!important;font-size:var(--m-fs-xs);font-weight:600;letter-spacing:.06em;text-transform:uppercase}
#note-modal .player-source-title{display:none}
#note-modal .video-segmented-switcher{background:transparent!important;border:0!important;padding:0!important;gap:2px;box-shadow:none!important}
#note-modal .video-seg-btn{height:30px;padding:0 10px!important;border-radius:8px!important;border:0!important;background:transparent!important;color:var(--m-mu)!important;font:500 var(--m-fs-sm)/1 var(--ds-font,inherit)!important;box-shadow:none!important}
#note-modal .video-seg-btn:hover{color:var(--m-tx)!important;background:var(--m-hover)!important}
#note-modal .video-seg-btn.active{color:var(--m-tx)!important;background:var(--m-hover)!important;font-weight:600!important}
#note-modal .player-ext-btn,#note-modal .player-ext-btn.doc-ext{height:30px;padding:0 10px;border:0!important;border-radius:8px;background:transparent!important;color:var(--m-mu)!important;font:500 var(--m-fs-sm)/1 var(--ds-font,inherit)}
#note-modal .player-ext-btn:hover{background:var(--m-hover)!important;color:var(--m-tx)!important}
#note-modal .video-responsive-wrap{background:#000;min-height:0}

/* Progresso da sessão: uma linha de metadados + barra fina */
#note-modal .session-progress-bar-wrap{padding:10px 16px 12px;gap:9px;background:var(--m-bg);border:0;border-bottom:1px solid var(--m-line)}
#note-modal .session-progress-info{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:var(--m-fs-xs);color:var(--m-mu)}
.session-meta,.session-end{display:flex;align-items:center;gap:4px;flex-wrap:wrap;min-width:0}
.session-end{gap:12px}
.session-time{font-variant-numeric:tabular-nums;margin-right:6px}
.session-chip{font:500 var(--m-fs-xs)/1 var(--ds-font,inherit);display:inline-flex;align-items:center;gap:6px;padding:6px 8px;border:0;border-radius:6px;background:transparent;color:var(--m-mu);cursor:pointer;font-variant-numeric:tabular-nums;transition:background .15s,color .15s}
.session-chip::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--m-line-2)}
.session-chip:hover{background:var(--m-hover);color:var(--m-tx)}
.session-chip.is-done{color:var(--m-tx)}
.session-chip.is-done::before{background:var(--m-ok)}
.session-pct{font-weight:600;color:var(--m-tx);font-variant-numeric:tabular-nums}
#note-modal .session-finish-btn{height:28px;padding:0 12px;border-radius:8px;border:1px solid var(--m-line-2);background:transparent;color:var(--m-tx);font:500 var(--m-fs-xs)/1 var(--ds-font,inherit);transform:none!important}
#note-modal .session-finish-btn:hover{background:var(--m-ok);border-color:var(--m-ok);color:#fff;opacity:1}
#note-modal .session-bar-track{height:3px;background:var(--m-line)}
#note-modal .session-bar-fill{background:var(--m-acc)}

/* Dica padrão (aulas sem Aula Visual) */
#note-modal .study-left-extra-info{background:var(--m-bg);padding:20px}
#note-modal .study-left-card{background:var(--m-sunk);border:0;border-radius:12px;padding:16px 18px;box-shadow:none}
#note-modal .study-left-card-title{font-size:var(--m-fs-sm);font-weight:600;margin-bottom:6px}
#note-modal .study-left-card p{font-size:var(--m-fs-sm);line-height:1.6}

/* ============================ ESTÚDIO: CADERNO ============================ */
#note-modal .notes-section-head{min-height:44px;padding:6px 12px 6px 16px;background:var(--m-bg);border-bottom:1px solid var(--m-line);gap:10px}
#note-modal .notes-head-title{font-size:var(--m-fs-sm);font-weight:600}
#note-modal .toolbar-modes{background:var(--m-sunk);padding:3px;border-radius:9px;gap:2px}
#note-modal .tb-mode-btn{height:26px;padding:0 10px;border:0;border-radius:7px;background:transparent;color:var(--m-mu);font:500 var(--m-fs-xs)/1 var(--ds-font,inherit)}
#note-modal .tb-mode-btn:hover{color:var(--m-tx)}
#note-modal .tb-mode-btn.active{background:var(--m-bg);color:var(--m-tx);box-shadow:0 1px 2px rgba(0,0,0,.25),0 0 0 1px var(--m-line)}

/* Ferramentas: uma linha só, rolável, sem moldura em cada botão */
#note-modal .note-toolbar{flex-wrap:nowrap;gap:8px;padding:6px 12px;background:var(--m-bg);border-bottom:1px solid var(--m-line);overflow-x:auto}
#note-modal .toolbar-group{flex-wrap:nowrap;gap:2px}
#note-modal .tb-btn,#note-modal .tb-btn.tb-highlight-math,#note-modal .tb-btn.tb-highlight-3d,#note-modal .tb-btn.tb-highlight-draw,#note-modal .tb-audio-btn{
  height:28px;padding:0 8px;border:0!important;border-radius:6px;background:transparent!important;color:var(--m-mu)!important;
  font:500 var(--m-fs-xs)/1 var(--ds-font,inherit);white-space:nowrap;box-shadow:none!important;transform:none!important;
}
#note-modal .tb-btn:hover{background:var(--m-hover)!important;color:var(--m-tx)!important}
#note-modal .tb-btn:disabled{opacity:.35}
#note-modal .tb-sep{height:16px;margin:0 6px;background:var(--m-line);flex:none}
#note-modal .toolbar-templates{flex:none}
#note-modal .tb-select{height:28px;padding:0 8px;border:1px solid var(--m-line);border-radius:6px;background:transparent;color:var(--m-mu);font:500 var(--m-fs-xs)/1 var(--ds-font,inherit);cursor:pointer}
#note-modal .math-palette-wrap{background:var(--m-sunk);border-bottom:1px solid var(--m-line)}
#note-modal .sym-btn,#note-modal .sym-tmpl-btn{border:1px solid var(--m-line);background:var(--m-bg);border-radius:6px}
#note-modal .sym-btn:hover,#note-modal .sym-tmpl-btn:hover{border-color:var(--m-line-2);background:var(--m-hover)}

#note-modal .note-editor-pane{border-color:var(--m-line)!important}
#note-modal .note-editor-pane textarea{padding:20px 24px;font-size:.84rem;line-height:1.75;color:var(--m-tx)}
#note-modal .note-editor-pane textarea::placeholder{color:color-mix(in srgb,var(--m-mu) 70%,transparent)}
#note-modal .note-preview-pane{background:var(--m-bg);padding:20px 24px}
#note-modal .preview-header{font-size:.6875rem;font-weight:600;letter-spacing:.08em;border-bottom:0;margin-bottom:10px;padding:0}
#note-modal .preview-body{font-size:.9375rem;line-height:1.7}
#note-modal .note-modal-footer{padding:8px 12px 8px 16px;background:var(--m-bg);border-top:1px solid var(--m-line)}
#note-modal .footer-stats{font-size:var(--m-fs-xs);font-variant-numeric:tabular-nums}
#note-modal .note-clear-btn{height:30px;padding:0 12px;border:0;border-radius:8px;background:transparent;color:var(--m-mu);font:500 var(--m-fs-xs)/1 var(--ds-font,inherit)}
#note-modal .note-clear-btn:hover{background:var(--m-hover);color:var(--m-bad)}
#note-modal .note-save-btn{height:30px;padding:0 14px;border:1px solid var(--m-line-2);border-radius:8px;background:transparent;color:var(--m-tx);font:500 var(--m-fs-xs)/1 var(--ds-font,inherit)}
#note-modal .note-save-btn:hover{background:var(--m-hover)}
#note-modal .layout-guide-right .study-player-col .study-notes-panel{border-top:0}

/* ============================ AULA VISUAL: LEITURA ============================ */
#note-modal .layout-guide-right .study-notes-col .study-left-extra-info{padding:0;background:var(--m-bg)}
.guide-shell{max-width:760px;margin:0 auto;padding:0 40px 64px}
.guide-shell-head{position:sticky;top:0;z-index:4;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 0;margin-bottom:8px;background:color-mix(in srgb,var(--m-bg,var(--card)) 88%,transparent);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--m-line)}
.guide-shell-title{font-size:.6875rem;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--m-mu)}

#note-modal .lv2{gap:0;font-size:1rem;line-height:1.72;color:var(--m-tx);text-wrap:pretty}
#note-modal .lv2 p{margin:0 0 .85em}
#note-modal .lv2 ul,#note-modal .lv2 ol{padding-left:1.25em}
#note-modal .lv2 li{margin:.3em 0}
#note-modal .lv2 li::marker{color:var(--m-mu)}
#note-modal .lv2 code{background:var(--m-sunk);border:1px solid var(--m-line);padding:1px 6px;border-radius:5px;font-size:.86em}
#note-modal .lv2 .katex-display{margin:1.1em 0;overflow-x:auto;overflow-y:hidden;padding:4px 0}

/* Abertura da aula */
#note-modal .lv2-hero{border:0;border-radius:0;background:none;padding:28px 0 32px}
#note-modal .lv2-chips{gap:0;margin-bottom:14px}
#note-modal .lv2-chip{border:0;background:none;padding:0;font-size:var(--m-fs-xs);font-weight:500;color:var(--m-mu)}
#note-modal .lv2-chip+.lv2-chip::before{content:"·";margin:0 8px;color:var(--m-line-2)}
#note-modal .lv2-hook{font-family:var(--ds-display,inherit);font-size:1.375rem;font-weight:600;line-height:1.4;letter-spacing:-.015em;text-wrap:balance}
#note-modal .lv2-meta{gap:18px;margin-top:22px}
#note-modal .lv2-meta-title{font-size:.6875rem;font-weight:600;letter-spacing:.09em;color:var(--m-mu);margin-bottom:4px}
#note-modal .lv2-meta ul{margin:0}

/* Cada etapa é uma seção de texto, separada por uma linha fina, não um cartão */
#note-modal .lv2-block{border:0!important;border-top:1px solid var(--m-line)!important;border-radius:0;background:none!important;padding:36px 0;transition:none}
#note-modal .lv2-head{margin-bottom:6px}
#note-modal .lv2-kicker{font-size:.6875rem;font-weight:600;letter-spacing:.09em;color:var(--m-acc)}
#note-modal .lv2-badge{border:0;background:none;padding:0;font-size:var(--m-fs-xs);font-weight:500;color:color-mix(in srgb,var(--m-mu) 75%,transparent);font-variant-numeric:tabular-nums}
#note-modal .lv2-badge.is-seen{color:var(--m-ok)}
#note-modal .lv2-title{font-size:1.25rem;font-weight:600;line-height:1.35;margin:4px 0 14px;letter-spacing:-.015em}
#note-modal .lv2-concreto,#note-modal .lv2-palpite,#note-modal .lv2-quiz{border-left:0!important}
#note-modal .lv2-crianca{background:none!important}

/* Notação, passos, conclusões */
#note-modal .lv2-notation{gap:0;margin:14px 0 4px;border-top:1px solid var(--m-line)}
#note-modal .lv2-not-row{background:none;border-radius:0;padding:12px 0;border-bottom:1px solid var(--m-line);grid-template-columns:minmax(96px,auto) 1fr;gap:18px}
#note-modal .lv2-not-read{font-size:var(--m-fs-sm)}
#note-modal .lv2-steps{gap:14px;margin-top:14px}
#note-modal .lv2-steps li{background:none;border-radius:0;padding:2px 0 2px 40px}
#note-modal .lv2-steps li::before{left:0;top:3px;width:24px;height:24px;background:transparent;border:1px solid var(--m-line-2);color:var(--m-mu);font-size:.72rem;font-weight:600}
#note-modal .lv2-step-why{font-size:.9rem}
#note-modal .lv2-conclusion,#note-modal .lv2-mission{margin:16px 0;padding:2px 0 2px 16px;border:0;border-left:2px solid var(--m-acc);border-radius:0;background:none}
#note-modal .lv2-mission ol{margin-top:6px}
#note-modal .lv2-exp-title,#note-modal .lv2-layer-tag{font-size:.6875rem;font-weight:600;letter-spacing:.09em;color:var(--m-mu);margin:22px 0 6px}
#note-modal .lv2-mission .lv2-exp-title{margin-top:0}

/* Respostas recolhidas */
#note-modal .lv2 details{margin-top:14px;border:1px solid var(--m-line);border-radius:10px;padding:0;background:none}
#note-modal .lv2 summary{padding:11px 14px;font-size:var(--m-fs-sm);font-weight:500;color:var(--m-mu);list-style:none;display:flex;align-items:center;gap:8px}
#note-modal .lv2 summary::-webkit-details-marker{display:none}
#note-modal .lv2 summary::before{content:"";width:6px;height:6px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:rotate(-45deg);transition:transform .2s}
#note-modal .lv2 details[open]>summary::before{transform:rotate(45deg)}
#note-modal .lv2 summary:hover{color:var(--m-tx)}
#note-modal .lv2 details>*:not(summary){padding:0 16px 14px}
#note-modal .lv2 details[open]>summary{margin-bottom:0}

/* Código: paleta própria para cada tema; o realce vem de lv2HighlightPy (.tk-*) */
.note-modal-overlay{
  --code-bg:#0b1218;--code-line:rgba(148,178,190,.14);--code-tx:#d6dee1;--code-mu:#6f8590;
  --code-c:#6f8590;--code-s:#9fdcae;--code-n:#f2b872;--code-k:#c8a8ff;--code-f:#7fc8f8;
}
:root[data-theme="light"] .note-modal-overlay{
  --code-bg:#f6f8fa;--code-line:#e1e7eb;--code-tx:#1f2b31;--code-mu:#6a7a83;
  --code-c:#6e7f88;--code-s:#116329;--code-n:#a04f00;--code-k:#7c3aed;--code-f:#0550ae;
}
#note-modal .lv2-code,#note-modal .lv2 pre{margin:14px 0 0;padding:16px 18px;background:var(--code-bg);color:var(--code-tx);border:1px solid var(--code-line);border-radius:10px;font-family:ui-monospace,"JetBrains Mono","Cascadia Code",SFMono-Regular,Consolas,monospace;font-size:.8125rem;line-height:1.7;tab-size:4;overflow-x:auto}
#note-modal .lv2 pre code,#note-modal .lv2-code code{background:none!important;border:0!important;padding:0!important;border-radius:0!important;font-size:inherit!important;color:inherit;white-space:pre}
#note-modal .tk-c{color:var(--code-c);font-style:italic}
#note-modal .tk-s{color:var(--code-s)}
#note-modal .tk-n{color:var(--code-n)}
#note-modal .tk-k{color:var(--code-k);font-weight:500}
#note-modal .tk-f{color:var(--code-f)}
#note-modal .lv2 pre::selection,#note-modal .lv2 pre *::selection{background:color-mix(in srgb,var(--code-f) 28%,transparent)}

/* Armadilhas e tabelas */
#note-modal .lv2-pitfalls{gap:0;margin-top:10px}
#note-modal .lv2-pit{background:none;border-radius:0;padding:12px 0;border-bottom:1px solid var(--m-line)}
#note-modal .lv2-pit:last-child{border-bottom:0}
#note-modal .lv2-pit-wrong{color:var(--m-mu);font-weight:500}
#note-modal .lv2-table{font-size:.875rem}
#note-modal .lv2-table th{font-size:.6875rem;letter-spacing:.06em;font-weight:600;border-bottom:1px solid var(--m-line-2)}
#note-modal .lv2-table td{border-bottom:1px solid var(--m-line);padding:9px 8px}

/* Interações: opções, retornos, botões */
#note-modal .lv2-opts{gap:8px;margin-top:14px}
#note-modal .lv2-opt{padding:12px 16px;border-radius:10px;border:1px solid var(--m-line-2);background:transparent;font-size:.9375rem;line-height:1.45;transition:border-color .15s,background .15s}
#note-modal .lv2-opt:hover:not(:disabled){border-color:color-mix(in srgb,var(--m-tx) 35%,transparent);background:var(--m-hover)}
#note-modal .lv2-opt.is-right{border-color:var(--m-ok);background:color-mix(in srgb,var(--m-ok) 10%,transparent)}
#note-modal .lv2-opt.is-wrong{border-color:var(--m-bad);background:color-mix(in srgb,var(--m-bad) 8%,transparent)}
#note-modal .lv2-fb,#note-modal .lv2-qz-exp{margin-top:12px;padding:14px 16px;border:0;border-radius:10px;background:var(--m-sunk);font-size:.9375rem}
#note-modal .lv2-fb-msg{font-weight:600}
#note-modal .lv2-btn{height:32px;padding:0 14px;border-radius:8px;border:1px solid var(--m-line-2);background:transparent;font-weight:500;font-size:var(--m-fs-sm)}
#note-modal .lv2-btn:hover{background:var(--m-hover)}
#note-modal .lv2-btn-main{background:var(--m-tx);color:var(--m-bg);border-color:var(--m-tx)}
#note-modal .lv2-btn-main:hover{background:var(--m-tx);filter:brightness(1.12)}

/* Vídeo guiado */
#note-modal .lv2-video-meta{font-size:var(--m-fs-sm);margin:8px 0 10px}
#note-modal .lv2-video-meta b{color:var(--m-tx);font-weight:600}
#note-modal .lv2-video-wrap{border-radius:12px;background:#05090c;border:1px solid var(--m-line)}
#note-modal .lv2-video-play{height:40px;padding:0 18px;border-radius:99px;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.08);color:#fff;font-weight:600;font-size:var(--m-fs-sm);backdrop-filter:blur(6px);transition:background .15s}
#note-modal .lv2-video-play:hover{background:rgba(255,255,255,.16)}
#note-modal .lv2-ext{font-size:var(--m-fs-xs);margin-top:8px;text-decoration:none}
#note-modal .lv2-ext:hover{color:var(--m-tx);text-decoration:underline}
#note-modal .lv2-clip-note{border:0;background:var(--m-sunk);font-weight:500;font-size:var(--m-fs-sm);border-radius:10px;padding:8px 8px 8px 14px;justify-content:space-between}
#note-modal .lv2-clip-replay{height:28px;padding:0 12px;border-radius:8px;border:1px solid var(--m-line-2);background:transparent;color:var(--m-tx);font-weight:500;font-size:var(--m-fs-xs)}

/* Blocos de IA e Inglês no mesmo ritmo visual */
#note-modal .lv2-py{border:1px solid var(--code-line);border-radius:12px;background:var(--code-bg);margin-top:16px}
#note-modal .lv2-py-bar,#note-modal .lv2-py-actions,#note-modal .lv2-py-out,#note-modal .lv2-py-tests:not(:empty){border-color:var(--code-line)}
#note-modal .lv2-py-ed{color:var(--code-tx);font-size:.8125rem;line-height:1.7;padding:14px 18px}
#note-modal .lv2-py-out{color:var(--code-tx)}
#note-modal .lv2-py-actions .lv2-btn:not(.lv2-btn-main){background:transparent}
#note-modal .lv2-ps-line{border-color:var(--m-line-2);background:transparent;border-radius:10px;padding:8px 8px 8px 14px}
#note-modal .lv2-ps.is-code .lv2-ps-line{background:var(--code-bg);border-color:var(--code-line);color:var(--code-tx)}
#note-modal .lv2-ps-btns button{border-color:var(--m-line);border-radius:8px}
#note-modal .lv2-dlg-bubble{background:var(--m-sunk);border:0;border-radius:14px}
#note-modal .lv2-dlg-row[data-side="b"] .lv2-dlg-bubble{background:color-mix(in srgb,var(--m-acc) 12%,var(--m-bg))}
#note-modal .lv2-say{border-color:var(--m-line-2);background:transparent;border-radius:8px}
#note-modal .lv2-say:hover{background:var(--m-hover)}
#note-modal .lv2-spk{border-color:var(--m-line);border-radius:12px;padding:14px 16px}
#note-modal .lv2-card{border-color:var(--m-line);background:var(--m-bg);border-radius:12px}
#note-modal .lv2-card-foot{border-color:var(--m-line)}
#note-modal .lv2-dict{border-color:var(--m-line-2);background:transparent;height:34px}
#note-modal .lv2-note{border-radius:10px}

/* Laboratórios interativos: aqui o contêiner se justifica (é uma área de manipulação) */
#note-modal .lv2-wbox{margin-top:16px;border:1px solid var(--m-line);border-radius:14px;padding:18px;background:var(--m-sunk)}
#note-modal .lv2-wctl{gap:10px 18px;margin-top:14px}
#note-modal .lv2-wctl label{font-size:var(--m-fs-xs);font-weight:500;gap:4px}
#note-modal .lv2-wout{border:1px solid var(--m-line);background:var(--m-bg);border-radius:10px;padding:10px 12px;font-size:var(--m-fs-sm);margin-top:12px}

/* Prática e quiz */
#note-modal .lv2-ex{padding:20px 0 6px;border-top:1px solid var(--m-line)}
#note-modal .lv2-ex:first-of-type{border-top:0;padding-top:8px}
#note-modal .lv2-lvl-tag{font-size:.6875rem;font-weight:600;letter-spacing:.09em;margin-bottom:6px}
#note-modal .lv2-check{gap:8px;margin-top:12px}
#note-modal .lv2-check input{height:34px;padding:0 12px;border-radius:8px;border:1px solid var(--m-line-2);background:transparent;font-size:var(--m-fs-sm)}
#note-modal .lv2-check input:focus{outline:none;border-color:var(--m-acc);box-shadow:0 0 0 3px color-mix(in srgb,var(--m-acc) 20%,transparent)}
#note-modal .lv2-check-msg{font-weight:500;font-size:var(--m-fs-sm)}
#note-modal .lv2-qz{padding:16px 0;border-top:1px solid var(--m-line)}
#note-modal .lv2-qopt{padding:8px 10px;border-radius:8px;font-size:.9375rem}
#note-modal .lv2-qopt:hover{background:var(--m-hover)}

/* Camadas e revisão */
#note-modal .lv2-lock{border:1px dashed var(--m-line-2);border-radius:10px;padding:12px 14px;font-size:var(--m-fs-sm)}
#note-modal .lv2-src{background:none;border-radius:0;padding:12px 0;margin:0;border-bottom:1px solid var(--m-line)}
#note-modal .lv2-src a{font-weight:600;text-decoration:none}
#note-modal .lv2-src a:hover{text-decoration:underline}
#note-modal .lv2-src-meta{font-size:var(--m-fs-xs)}
#note-modal .lv2-review{border:0;background:color-mix(in srgb,var(--m-warn) 12%,transparent);border-radius:8px;padding:8px 12px;font-size:var(--m-fs-sm)}

/* Fecho da aula */
#note-modal .lv2-footer{border:0;border-top:1px solid var(--m-line);border-radius:0;background:none;padding:36px 0 0}
#note-modal .lv2-refs{font-size:var(--m-fs-sm);margin-top:20px}

/* Aulas no formato antigo (4 etapas com estilo embutido): mesmo ritmo de leitura */
#pt-guide-box [id^="pt-step-card-"]{background:none!important;border:0!important;border-top:1px solid var(--m-line)!important;border-radius:0!important;padding:28px 0!important;box-shadow:none!important}
#pt-guide-box [id^="pt-step-badge-"]{border:0!important;background:none!important;padding:0!important;color:var(--m-mu)}
#pt-guide-box [id^="pt-step-badge-"].is-seen{color:var(--m-ok)!important}

/* ============================ SUBMODAIS ============================ */
.modal-sub-box{border:1px solid var(--m-line)!important;border-radius:16px!important;background:var(--m-bg)!important;box-shadow:0 40px 100px -30px rgba(0,0,0,.65)!important;animation:m-in .3s var(--m-ease)}
.modal-sub-header{min-height:56px;padding:10px 12px 10px 20px!important;background:var(--m-bg)!important;border-bottom:1px solid var(--m-line)!important}
.modal-sub-header h3,.modal-sub-title{font-family:var(--ds-display,inherit)!important;font-size:1rem!important;font-weight:600!important;letter-spacing:-.01em;color:var(--m-tx)!important;margin:0!important}
.modal-sub-header span[style*="font-size:1.3rem"]{display:none}
.modal-sub-header .note-close-btn,.modal-sub-header .modal-close-icon{width:32px;height:32px;display:inline-grid;place-items:center;padding:0;border:0;border-radius:8px;background:transparent;color:var(--m-mu);font-size:1rem;cursor:pointer}
.modal-sub-header .note-close-btn:hover,.modal-sub-header .modal-close-icon:hover{background:var(--m-hover);color:var(--m-tx)}
.modal-sub-overlay input:not([type=range]):not([type=checkbox]):not([type=radio]):not([type=color]),.modal-sub-overlay select,.modal-sub-overlay textarea{border-radius:8px;border:1px solid var(--m-line-2);background:var(--m-sunk);color:var(--m-tx)}
.modal-sub-overlay input:focus,.modal-sub-overlay select:focus,.modal-sub-overlay textarea:focus{outline:none;border-color:var(--m-acc);box-shadow:0 0 0 3px color-mix(in srgb,var(--m-acc) 20%,transparent)}

/* Ferramentas dos submodais: mesmo botão fantasma do caderno */
.modal-sub-overlay .draw-toolbar,.modal-sub-overlay .calc-tabs{background:var(--m-bg)!important;border-bottom:1px solid var(--m-line)!important}
.modal-sub-overlay .draw-tool-btn,.modal-sub-overlay .draw-act-btn,.modal-sub-overlay .calc-tab-btn,.modal-sub-overlay .v3d-reset-btn,.modal-sub-overlay .calc-op-btn{
  border:1px solid transparent!important;border-radius:8px!important;background:transparent!important;color:var(--m-mu)!important;font-weight:500!important;box-shadow:none!important;transform:none!important}
.modal-sub-overlay .draw-tool-btn:hover,.modal-sub-overlay .draw-act-btn:hover,.modal-sub-overlay .calc-tab-btn:hover,.modal-sub-overlay .v3d-reset-btn:hover,.modal-sub-overlay .calc-op-btn:hover{background:var(--m-hover)!important;color:var(--m-tx)!important}
.modal-sub-overlay .draw-tool-btn.active,.modal-sub-overlay .calc-tab-btn.active{background:var(--m-hover)!important;color:var(--m-tx)!important;border-color:var(--m-line)!important}
.modal-sub-overlay .calc-op-btn{border-color:var(--m-line)!important}
.modal-sub-overlay .draw-insert-btn,.modal-sub-overlay .v3d-snapshot-btn{border:0!important;border-radius:8px!important;background:var(--m-tx)!important;color:var(--m-bg)!important;font-weight:600!important;box-shadow:none!important;transform:none!important}
.modal-sub-overlay .v3d-vector-card,.modal-sub-overlay .calc-matrix-card,.modal-sub-overlay .calc-result-box,.modal-sub-overlay .v3d-math-results{border:1px solid var(--m-line)!important;background:var(--m-sunk)!important;border-radius:12px!important;box-shadow:none!important}
.modal-sub-overlay .export-card-btn{border:1px solid var(--m-line)!important;border-radius:12px!important;background:transparent!important;box-shadow:none!important;transform:none!important;transition:background .15s,border-color .15s}
.modal-sub-overlay .export-card-btn:hover{background:var(--m-hover)!important;border-color:var(--m-line-2)!important}
.modal-sub-overlay .export-card-title{font-weight:600}
.modal-sub-overlay .export-card-desc{color:var(--m-mu)}

/* ============================ RESPONSIVO ============================ */
@media (max-width:1280px){
  .guide-shell{padding:0 28px 56px}
}
@media (max-width:1040px){
  #note-modal{padding:10px}
  #note-modal .study-player-col{border-right:0!important;border-bottom:1px solid var(--m-line)!important}
  .guide-shell{max-width:720px}
  #note-modal .layout-guide-right #study-notes-panel{border-top:1px solid var(--m-line)}
}
@media (max-width:760px){
  #note-modal{padding:0}
  #note-modal .unified-study-box{border-radius:0!important;border:0!important}
  #note-modal .note-modal-header{flex-wrap:wrap;gap:8px 10px;padding:10px 10px 10px 16px;min-height:0}
  #note-modal .note-header-left{flex:1 1 100%;padding-right:44px}
  #note-modal .note-topic-title{font-size:1rem;white-space:normal;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
  #note-modal .note-header-right{width:100%;justify-content:flex-start;gap:6px}
  #note-modal .note-header-right .note-close-btn{position:absolute;top:10px;right:8px}
  #note-modal .note-next-btn{margin-left:auto}
  .m-opts-menu{position:fixed;left:10px;right:10px;top:auto;bottom:10px;width:auto}
  #note-modal .study-player-topbar{padding:6px 10px}
  #note-modal .session-progress-bar-wrap{padding:8px 12px 10px}
  #note-modal .notes-section-head{padding:6px 10px}
  #note-modal .note-toolbar{padding:6px 8px}
  #note-modal .note-editor-pane textarea{padding:16px}
  .guide-shell{padding:0 18px 48px}
  .guide-shell-head{padding:10px 0}
  #note-modal .lv2{font-size:.96875rem}
  #note-modal .lv2-hero{padding:20px 0 24px}
  #note-modal .lv2-hook{font-size:1.15rem}
  #note-modal .lv2-block{padding:28px 0}
  #note-modal .lv2-title{font-size:1.125rem}
  #note-modal .lv2-not-row{grid-template-columns:1fr;gap:4px}
  #note-modal .lv2-not-sym{text-align:left}
  #note-modal .lv2-wbox{padding:12px;margin-left:-4px;margin-right:-4px}
  .modal-sub-overlay{padding:0!important;align-items:flex-end!important}
  .modal-sub-box{width:100%!important;max-width:none!important;max-height:94dvh!important;border-radius:16px 16px 0 0!important}
}
@media (prefers-reduced-motion:reduce){
  #note-modal .unified-study-box,.modal-sub-box,.m-opts-menu{animation:none!important}
}
</style>
"""

MODAL_UI_JS = r"""
<script>
/* Menu de opções da aula: fecha ao clicar fora ou com Esc */
(function () {
  document.addEventListener("click", function (e) {
    document.querySelectorAll("details.m-opts[open]").forEach(function (d) { if (!d.contains(e.target)) d.open = false; });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var open = document.querySelector("details.m-opts[open]");
    if (open) { open.open = false; e.stopPropagation(); }
  }, true);
})();
</script>
"""
