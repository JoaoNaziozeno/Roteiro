# -*- coding: utf-8 -*-
"""
CSS das páginas de trilha (IA, Matemática e Inglês), em dois arranjos:
  - celular (até 899 px): título quebra, opções quebram, filtros com nome curto;
  - computador (900 px ou mais): linha única, opções lado a lado, filtros com nome completo.

A lista serve para escolher a aula: status, título e ▶. O resto fica no ⋯ ou dentro do estúdio.
"""

LISTING_CSS = r"""
main .hero-head h1{font-size:1.45rem!important;line-height:1.2!important}
main [hidden],main .topic-panel[hidden]{display:none!important}

/* Resumo da trilha */
.trail-summary{border:1px solid var(--bd);border-radius:16px;padding:14px 16px;margin:14px 0 12px;background:var(--card)}
.sum-line{display:flex;align-items:baseline;flex-wrap:wrap;gap:2px 8px;font-size:.84rem;color:var(--mu)}
.sum-line b{font-size:1.35rem;color:var(--tx);font-variant-numeric:tabular-nums}
.sum-line #prog-pct-label{margin-left:auto;font-variant-numeric:tabular-nums}
.prog-bar{width:100%;height:6px;margin:9px 0 12px;background:var(--bd);border-radius:99px;overflow:hidden;display:flex}
.prog-bar>div{height:100%;transition:width .3s}
.prog-bar>div.has{min-width:5px}
.p-e{background:var(--e)}
.p-r{background:var(--r)}
.sum-next{display:flex;align-items:center;gap:10px}
.sum-next-info{flex:1;min-width:0}
.next-step-tag{display:block;font-size:.74rem;color:var(--mu)}
.next-step-title{font-size:.9rem;font-weight:650;color:var(--tx)}
.next-step-btn{font:inherit;font-size:.85rem;font-weight:700;min-height:40px;padding:8px 18px;border:0;border-radius:99px;background:var(--t,var(--ac));color:#06141B;cursor:pointer}
.sum-more{margin-top:10px;padding-top:4px;border-top:1px solid var(--bd)}
.sum-more>summary,.phase-about>summary{padding:8px 0;font-size:.8rem;color:var(--mu);cursor:pointer}
.sum-more>summary:hover,.phase-about>summary:hover{color:var(--tx)}
.sum-more .sub{margin:8px 0 0;font-size:.8rem;line-height:1.5;color:var(--mu)}
.level-info{display:flex;align-items:center;gap:10px;padding:6px 0 10px}
.level-icon{font-size:1.5rem}
.level-name{font-weight:750;font-size:.9rem;color:var(--tx)}
.level-desc{font-size:.78rem;color:var(--mu)}
.tracker-presets{display:flex;flex-wrap:wrap;gap:6px}
.trk-btn{font:inherit;font-size:.78rem;padding:6px 12px;border-radius:99px;border:1px solid var(--bd);background:var(--bg);color:var(--tx);cursor:pointer}

/* Filtros e busca */
.filter-row{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px;margin-bottom:14px}
.filters{display:flex;flex-wrap:nowrap;gap:3px;max-width:100%;overflow-x:auto;scrollbar-width:none}
.filters::-webkit-scrollbar{display:none}
.filters .fil-btn{flex:0 0 auto;white-space:nowrap;min-height:34px;padding:5px 7px;font-size:.75rem;transition:color .15s,background .15s,border-color .15s}
.fil-long{display:none}

/* Sobre a fase */
.phase-about{margin:-8px 0 0}
.phase-about[open]{margin-bottom:4px}
.group-section{margin-top:12px}

/* Linha da aula */
.topic-row{
  display:flex;flex-wrap:wrap;align-items:center;
  gap:0 4px;min-height:56px;padding:5px 6px;
  border-radius:10px;margin-bottom:6px;
}
.topic-left{flex:1 1 0;min-width:0;padding:4px 4px;cursor:pointer}
.topic-title-text{font-size:.9rem;font-weight:600;line-height:1.3;color:var(--tx);overflow-wrap:anywhere}
.row-meta{display:block;margin-top:2px;font-size:.74rem;color:var(--mu)}
.row-meta:empty{display:none}
.row-st,.row-more{flex:0 0 36px;height:44px;padding:0;border:0;background:transparent;color:var(--mu);display:grid;place-items:center;cursor:pointer;font:inherit}
.row-st i{box-sizing:border-box;width:21px;height:21px;border:2px solid var(--mu);border-radius:50%;display:grid;place-items:center;font:800 12px/1 system-ui}
.status-r .row-st i{border-color:#e8a100;background:linear-gradient(90deg,#e8a100 50%,transparent 50%)}
.status-e .row-st i{border-color:#2fa36b;background:#2fa36b;color:#fff}
.status-e .row-st i::after{content:"✓"}
.row-more{font-size:1.15rem;border-radius:8px}
.row-more:hover,.row-more[aria-expanded="true"]{color:var(--tx)}
.row-play{flex:0 0 40px;height:40px;padding:0 0 0 2px;border-radius:50%;border:1px solid var(--t,var(--ac));background:transparent;color:var(--t,var(--ac));cursor:pointer;font:inherit;font-size:.85rem}
.row-play:hover{background:var(--t,var(--ac));color:#06141B}
.topic-panel{flex:1 1 100%;min-width:0;display:flex;flex-wrap:wrap;gap:6px;padding:6px 0 8px 40px}
.row-opt{font:inherit;font-size:.8rem;line-height:1.2;display:inline-flex;align-items:center;min-height:36px;padding:6px 10px;border:1px solid var(--bd);border-radius:8px;background:transparent;color:var(--tx);text-decoration:none;white-space:nowrap;cursor:pointer}
.row-opt:hover{border-color:var(--t,var(--ac))}
.row-opt[aria-pressed="true"]{border-color:var(--t,var(--ac));font-weight:700}

@media (min-width:900px){
  .filters{gap:6px}
  .filters .fil-btn{padding:6px 14px;font-size:.8rem}
  .fil-long{display:inline}
  .fil-short{display:none}
  .topic-row{min-height:48px;padding:1px 10px}
  .topic-left{padding:3px 6px}
  .row-st,.row-more{height:40px}
  .row-play{flex-basis:36px;height:36px}
  .row-meta{display:inline;margin:0 0 0 10px}
  .topic-panel{flex-wrap:nowrap;padding:4px 0 8px 46px}
}
@media (max-width:899px){
  /* menos moldura, mais título */
  main{padding-left:12px;padding-right:12px}
  .phase-body{padding:14px 8px}
  .topic-row{gap:0 2px;padding:4px 2px 4px 5px}
  .row-st,.row-more{flex-basis:36px;min-width:36px}
  .topic-left{padding:4px 2px}
  .filter-row .search-input{width:100%;min-width:0;min-height:38px}
}
"""
