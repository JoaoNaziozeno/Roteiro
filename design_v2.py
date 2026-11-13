# -*- coding: utf-8 -*-
"""
Design v2 do Roteiro IA: "Rota" — a jornada do zero à IA como um mapa vivo.

Camada aplicada no FIM de todas as páginas geradas (depois de todo o CSS/JS existente),
então só refina o visual e acrescenta interações, sem alterar a lógica de estudo,
login, progresso ou sincronização.

O que ela traz:
  - Tokens novos (tipografia Space Grotesk + Inter, cores por trilha, superfícies de vidro)
    nos temas claro e escuro, mantendo os nomes de variáveis já usados (--bg, --card, --tx...).
  - Fundo "aurora" sutil e animado (só CSS).
  - Hub: herói com o MAPA DA SUA TRILHA (SVG): estações por trilha com anel de progresso,
    caminho aceso até onde você está e um marcador "você está aqui". Clicar leva à trilha.
  - Cartões com holofote que segue o cursor e borda na cor da trilha.
  - Entrada das seções ao rolar (CSS scroll-driven animations, com fallback estático).
  - Transições entre páginas (View Transitions entre documentos, onde o navegador suporta).
  - Paleta de comandos (Ctrl/⌘ + K): busca páginas e tópicos e abre a aula direto.
  - Respeita prefers-reduced-motion e funciona no celular.
"""

DESIGN_HEAD = r"""
<!-- Segura a primeira pintura até o fim da página (#ds-end): a transição já mostra a página pronta,
     sem montar menu, tema e listas na frente do usuário. Navegadores sem suporte ignoram. -->
<link rel="expect" href="#ds-end" blocking="render">
<script>try{var t=localStorage.getItem("roteiro-theme");if(t)document.documentElement.setAttribute("data-theme",t)}catch(e){}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<!-- Fontes: pré-carregadas para estarem prontas na primeira pintura, e "optional" para nunca trocarem
     depois que a página aparece (a troca da fonte do sistema para a Inter fazia o menu "pular"). -->
<link rel="preload" as="font" type="font/woff2" crossorigin href="https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2">
<link rel="preload" as="font" type="font/woff2" crossorigin href="https://fonts.gstatic.com/s/spacegrotesk/v22/V8mDoQDjQSkFtoMM3T6r8E7mPbF4Cw.woff2">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=optional">
<style id="design-v2">
/* ============================ TOKENS ============================ */
:root{
  --ds-font:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --ds-display:"Space Grotesk","Inter",system-ui,sans-serif;
  --ds-radius:18px;
  --ds-ease:cubic-bezier(.2,.8,.2,1);
  --t-ia:#38bdf8; --t-mat:#f5a524; --t-ing:#34d399; --t-proj:#a78bfa; --t-hub:#5eead4;
  --ds-glow:rgba(94,234,212,.35);
}
:root:not([data-theme="light"]){
  --bg:#060b10; --card:#0c171f; --tx:#e6edf0; --mu:#95a6af; --bd:#1c2c37;
  --ds-surface:rgba(13,24,32,.72); --ds-surface-2:rgba(18,32,42,.6); --ds-line:rgba(148,178,190,.14);
  --ds-shadow:0 18px 50px -18px rgba(0,0,0,.75);
}
:root[data-theme="light"]{
  --bg:#f2f5f6; --card:#ffffff; --tx:#0b1a22; --mu:#4c616c; --bd:#d6dfe3;
  --t-ia:#0284c7; --t-mat:#b45309; --t-ing:#047857; --t-proj:#6d28d9; --t-hub:#0f766e;
  --ds-glow:rgba(15,118,110,.22);
  --ds-surface:rgba(255,255,255,.78); --ds-surface-2:rgba(255,255,255,.6); --ds-line:rgba(11,26,34,.08);
  --ds-shadow:0 18px 40px -22px rgba(11,26,34,.35);
}
body[data-track="ia"]{--t:var(--t-ia)} body[data-track="mat"]{--t:var(--t-mat)}
body[data-track="ing"]{--t:var(--t-ing)} body[data-track="proj"]{--t:var(--t-proj)}
body[data-track="hub"]{--t:var(--t-hub)}

/* ============================ BASE ============================ */
body{font-family:var(--ds-font);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;background:var(--bg)}
h1,h2,h3,.hero-head h1,.track-card-title,.phase-title-text,.speed-title,.tracker-title,.lv2-title,.note-topic-title{font-family:var(--ds-display);letter-spacing:-.02em}
::selection{background:color-mix(in srgb,var(--t,var(--t-hub)) 35%,transparent)}
:focus-visible{outline:2px solid var(--t,var(--t-hub));outline-offset:2px;border-radius:6px}

/* Fundo aurora: três luzes lentas atrás de tudo */
body::before{
  content:"";position:fixed;inset:-20vmax;z-index:-1;pointer-events:none;
  background:
    radial-gradient(38vmax 30vmax at 18% 12%,color-mix(in srgb,var(--t,var(--t-hub)) 16%,transparent),transparent 70%),
    radial-gradient(34vmax 28vmax at 85% 18%,color-mix(in srgb,var(--t-proj) 11%,transparent),transparent 70%),
    radial-gradient(40vmax 30vmax at 60% 95%,color-mix(in srgb,var(--t-ia) 10%,transparent),transparent 70%);
  animation:ds-aurora 28s ease-in-out infinite alternate;
}
:root[data-theme="light"] body::before{opacity:.75}
@keyframes ds-aurora{to{transform:translate3d(3vmax,-2vmax,0) rotate(6deg) scale(1.06)}}
/* grão fino por cima, dá textura sem custo */
body::after{
  content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.05;
  background-image:radial-gradient(currentColor 1px,transparent 1px);background-size:3px 3px;color:var(--tx);
  mask-image:linear-gradient(to bottom,#000,transparent 70%);
}
.layout,.content-wrapper,main,.hub-main{background:transparent}

/* ============================ NAV ============================ */
.top-nav{background:color-mix(in srgb,var(--bg) 72%,transparent)!important;backdrop-filter:blur(16px) saturate(1.4);-webkit-backdrop-filter:blur(16px) saturate(1.4);border-bottom:1px solid var(--ds-line)!important;view-transition-name:ds-nav}
.nav-brand{font-family:var(--ds-display);font-weight:700}
.nav-link{position:relative;border-radius:10px;transition:color .2s,background .2s}
.nav-link.active{background:color-mix(in srgb,var(--t,var(--t-hub)) 14%,transparent)!important;border:1px solid color-mix(in srgb,var(--t,var(--t-hub)) 35%,transparent)!important;color:var(--tx)!important}
.nav-link.active::after{content:"";position:absolute;left:12px;right:12px;bottom:-1px;height:2px;border-radius:2px;background:var(--t,var(--t-hub));box-shadow:0 0 12px var(--t,var(--t-hub))}
.ds-k-btn{font:inherit;font-size:.78rem;font-weight:600;display:inline-flex;align-items:center;gap:8px;padding:6px 8px 6px 12px;border-radius:10px;border:1px solid var(--ds-line);background:var(--ds-surface-2);color:var(--mu);cursor:pointer;transition:.2s}
.ds-k-btn:hover{color:var(--tx);border-color:color-mix(in srgb,var(--t,var(--t-hub)) 45%,transparent)}
kbd,.ds-kbd{font:600 .68rem/1 var(--ds-font);padding:3px 6px;border-radius:6px;border:1px solid var(--ds-line);background:var(--bg);color:var(--mu)}

/* ============================ SUPERFÍCIES ============================ */
.track-card,.jr-sect,.tracker-box,.progress-card,.phase-card,.market-box,.proj-card,.jr-card,.filter-row .search-input{
  background:var(--ds-surface)!important;border:1px solid var(--ds-line)!important;
  backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);box-shadow:var(--ds-shadow)!important;
}
.jr-card{background:var(--ds-surface-2)!important;box-shadow:none!important}
.jr-sect,.track-card,.tracker-box,.progress-card,.phase-card{border-radius:var(--ds-radius)!important}

/* Holofote que segue o cursor (variáveis --mx/--my atualizadas via JS) */
.ds-spot{position:relative;isolation:isolate}
.ds-spot::before{
  content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;z-index:0;opacity:0;transition:opacity .3s;
  background:radial-gradient(420px circle at var(--mx,50%) var(--my,50%),color-mix(in srgb,var(--c,var(--t,var(--t-hub))) 13%,transparent),transparent 60%);
}
.ds-spot:hover::before{opacity:1}
.ds-spot>*{position:relative;z-index:1}

/* ============================ HUB: HERÓI + MAPA ============================ */
.hub-hero.ds-hero{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:36px;align-items:center;text-align:left;margin:8px 0 40px;min-height:380px}
.ds-eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:.74rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--t-hub);padding:5px 12px;border-radius:99px;border:1px solid color-mix(in srgb,var(--t-hub) 35%,transparent);background:color-mix(in srgb,var(--t-hub) 8%,transparent)}
.ds-eyebrow i{width:7px;height:7px;border-radius:50%;background:var(--t-hub);box-shadow:0 0 10px var(--t-hub);animation:ds-pulse 2.4s infinite}
.hub-hero.ds-hero h1{font-size:clamp(2.2rem,4.6vw,3.6rem)!important;line-height:1.04!important;font-weight:700!important;margin:18px 0 16px!important;background:none!important;-webkit-text-fill-color:var(--tx)!important;color:var(--tx)!important;text-wrap:balance}
.ds-grad{background:linear-gradient(100deg,var(--t-ia),var(--t-hub) 40%,var(--t-ing) 70%,var(--t-mat));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;background-size:200% 100%;animation:ds-shine 9s ease-in-out infinite alternate}
@keyframes ds-shine{to{background-position:100% 0}}
.hub-hero.ds-hero p{font-size:1.06rem!important;color:var(--mu)!important;max-width:34em;margin:0 0 26px!important;text-wrap:pretty}
.ds-hero-actions{display:flex;flex-wrap:wrap;gap:10px}
.ds-btn{font:600 .92rem/1 var(--ds-font);display:inline-flex;align-items:center;gap:10px;padding:13px 18px;border-radius:12px;text-decoration:none;cursor:pointer;border:1px solid transparent;transition:transform .2s var(--ds-ease),box-shadow .2s,background .2s,border-color .2s}
.ds-btn-primary{background:var(--tx);color:var(--bg);box-shadow:0 10px 30px -10px var(--ds-glow)}
.ds-btn-primary:hover{transform:translateY(-2px);box-shadow:0 16px 36px -12px var(--ds-glow)}
.ds-btn-primary .ds-arrow{transition:transform .2s var(--ds-ease)}
.ds-btn-primary:hover .ds-arrow{transform:translateX(4px)}
.ds-btn-ghost{background:var(--ds-surface-2);color:var(--tx);border-color:var(--ds-line)}
.ds-btn-ghost:hover{border-color:color-mix(in srgb,var(--t-hub) 45%,transparent)}

.ds-route{position:relative;display:flex;flex-direction:column;width:100%;border-radius:24px;border:1px solid var(--ds-line);background:
  radial-gradient(circle at 1px 1px,var(--ds-line) 1px,transparent 0) 0 0/22px 22px,var(--ds-surface);box-shadow:var(--ds-shadow);overflow:hidden}
.ds-route svg{width:100%;height:auto;aspect-ratio:31/20;display:block;flex:none}
.ds-route .r-base{fill:none;stroke:var(--ds-line);stroke-width:10;stroke-linecap:round}
.ds-route .r-lit{fill:none;stroke:url(#dsRouteGrad);stroke-width:5;stroke-linecap:round;filter:drop-shadow(0 0 6px var(--ds-glow));transition:stroke-dashoffset 1.6s var(--ds-ease)}
.ds-route .r-dash{fill:none;stroke:var(--mu);stroke-width:1.2;stroke-dasharray:2 9;opacity:.5}
.ds-route .st{cursor:pointer;outline:none}
.ds-route .st-ring-bg{fill:var(--card);stroke:var(--ds-line);stroke-width:6}
.ds-route .st-ring{fill:none;stroke-width:6;stroke-linecap:round;transform:rotate(-90deg);transform-box:fill-box;transform-origin:center;transition:stroke-dashoffset 1.4s var(--ds-ease)}
.ds-route .st-ico{font-size:20px;text-anchor:middle;dominant-baseline:central}
.ds-route .st-name{font:700 12.5px var(--ds-display);fill:var(--tx);text-anchor:middle}
.ds-route .st-pct{font:600 11px var(--ds-font);fill:var(--mu);text-anchor:middle}
.ds-route .st:hover .st-ring-bg,.ds-route .st:focus-visible .st-ring-bg{stroke:currentColor}
.ds-route .st:hover,.ds-route .st:focus-visible{filter:drop-shadow(0 0 10px currentColor)}
.ds-route .goal{font:700 11px var(--ds-display);fill:var(--mu);letter-spacing:.08em}
.ds-route .you{fill:var(--tx)}
.ds-route .you-halo{fill:var(--t-hub);opacity:.35;transform-box:fill-box;transform-origin:center;animation:ds-halo 2.2s ease-out infinite}
@keyframes ds-halo{from{transform:scale(.6);opacity:.55}to{transform:scale(2.4);opacity:0}}
@keyframes ds-pulse{50%{opacity:.35}}
.ds-route-legend{padding:0 18px 16px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;font-size:.74rem;color:var(--mu);pointer-events:none}
.ds-route-legend b{color:var(--tx);font-family:var(--ds-display)}

/* Título da seção de trilhas */
.ds-section-title{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin:8px 0 18px}
.ds-section-title h2{font-size:1.5rem;margin:0}
.ds-section-title span{color:var(--mu);font-size:.88rem}

/* Cartões das trilhas */
.track-card{--c:var(--t-hub);overflow:hidden;transition:transform .35s var(--ds-ease),border-color .3s,box-shadow .35s!important}
.track-card[data-track="ia"]{--c:var(--t-ia)} .track-card[data-track="mat"]{--c:var(--t-mat)}
.track-card[data-track="ing"]{--c:var(--t-ing)} .track-card[data-track="proj"]{--c:var(--t-proj)}
.track-card::after{content:"";position:absolute;inset:0 0 auto 0;height:3px;background:linear-gradient(90deg,var(--c),transparent);opacity:.9}
.track-card:hover{transform:translateY(-6px)!important;border-color:color-mix(in srgb,var(--c) 45%,transparent)!important;box-shadow:0 28px 60px -28px color-mix(in srgb,var(--c) 60%,transparent)!important}
.track-card-icon{width:52px;height:52px;display:grid;place-items:center;border-radius:14px;font-size:1.6rem!important;background:color-mix(in srgb,var(--c) 14%,transparent);border:1px solid color-mix(in srgb,var(--c) 30%,transparent)}
.track-badge-count{background:transparent!important;color:var(--mu)!important;border-color:var(--ds-line)!important}
.track-card-title{font-size:1.32rem!important}
.track-progress-wrap{border-top-color:var(--ds-line)!important}
.track-progress-bar{height:8px!important;background:color-mix(in srgb,var(--c) 12%,var(--bd))!important}
.track-progress-fill{background:linear-gradient(90deg,color-mix(in srgb,var(--c) 70%,#fff 0%),var(--c))!important;box-shadow:0 0 14px color-mix(in srgb,var(--c) 70%,transparent);transition:width 1.2s var(--ds-ease)!important}
.track-access-btn{background:transparent!important;color:var(--tx)!important;border:1px solid color-mix(in srgb,var(--c) 45%,transparent)!important;box-shadow:none!important;font-weight:650!important}
.track-access-btn:hover{background:var(--c)!important;color:#061016!important;transform:none!important}

/* Jornada */
.jr-sect{padding:28px!important}
.speed-title{font-size:1.25rem}
.speed-preset-btn.active{background:var(--tx)!important;color:var(--bg)!important;border-color:var(--tx)!important;box-shadow:none!important}
.jr-bar>i.w{background:linear-gradient(90deg,var(--t-ia),var(--t-hub))!important}

/* ============================ TRILHAS ============================ */
.hero-head{position:relative;padding:28px 0 8px}
.hero-head h1{font-size:clamp(1.7rem,3.6vw,2.6rem)!important;line-height:1.1;font-weight:700!important}
.hero-head::before{content:"";display:block;width:64px;height:4px;border-radius:4px;background:var(--t,var(--t-hub));box-shadow:0 0 16px var(--t,var(--t-hub));margin-bottom:18px}
.hero-head .sub{max-width:60em;color:var(--mu)}
.prog-bar .p-e{background:linear-gradient(90deg,color-mix(in srgb,var(--t) 70%,#fff 0%),var(--t))!important}
.prog-bar{background:var(--bd)!important}
.prog-bar .p-z{background:transparent!important}
.prog-bar .p-r{background:#e8a100!important}
.phase-head{background:transparent!important;border-bottom-color:var(--ds-line)!important;transition:background .2s}
.phase-head:hover{background:color-mix(in srgb,var(--t,var(--t-hub)) 6%,transparent)!important}
.phase-title-text{font-size:1.08rem!important}
.group-title{color:var(--t,var(--ac))!important;border-bottom-color:var(--ds-line)!important}
.topic-row{position:relative;background:color-mix(in srgb,var(--card) 55%,transparent)!important;border:1px solid var(--ds-line)!important;transition:transform .25s var(--ds-ease),border-color .2s,background .2s!important}
.topic-row::before{content:"";position:absolute;left:0;top:10px;bottom:10px;width:3px;border-radius:3px;background:var(--bd);transition:background .3s,box-shadow .3s}
.topic-row.status-r::before{background:#e8a100}
.topic-row.status-e::before{background:#2fa36b;box-shadow:0 0 10px #2fa36b}
.topic-row:hover{transform:translateX(3px);border-color:color-mix(in srgb,var(--t,var(--t-hub)) 40%,transparent)!important;background:color-mix(in srgb,var(--t,var(--t-hub)) 6%,var(--card))!important}
.fil-btn.active,.trk-btn.active{background:var(--tx)!important;color:var(--bg)!important;border-color:var(--tx)!important}
.sidebar{background:color-mix(in srgb,var(--bg) 80%,transparent)!important;backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-right:1px solid var(--ds-line)!important}

/* Estúdio */
.note-modal-overlay{background:color-mix(in srgb,#020608 70%,transparent)!important;backdrop-filter:blur(10px)!important}
.unified-study-box{border:1px solid var(--ds-line)!important;animation:ds-modal-in .45s var(--ds-ease)}
@keyframes ds-modal-in{from{opacity:0;transform:translateY(14px) scale(.985);filter:blur(4px)}to{opacity:1;transform:none;filter:none}}
.note-next-btn{background:var(--tx)!important;color:var(--bg)!important;border-color:var(--tx)!important}
.note-next-btn:hover:not(:disabled){filter:brightness(1.1)}

/* ============================ ROLAGEM: SEÇÕES SURGEM ============================ */
@supports (animation-timeline: view()){
  .phase-card,.track-card,.jr-card,.proj-card,.ds-section-title{
    animation:ds-rise linear both;animation-timeline:view();animation-range:entry 0% entry 35%;
  }
}
@keyframes ds-rise{from{opacity:0;transform:translateY(26px) scale(.985)}to{opacity:1;transform:none}}

/* ============================ TRANSIÇÃO ENTRE PÁGINAS ============================ */
@view-transition{navigation:auto}
/* Espaço da barra de rolagem sempre reservado: o menu não desliza ~8 px quando ela aparece */
html{scrollbar-gutter:stable}
/* Fundo da transição igual ao do site (evita clarão entre a saída e a entrada) */
html::view-transition{background:var(--bg)}
/* Menu do topo: fica parado e troca na hora (mesma largura em todas as páginas) */
::view-transition-group(ds-nav){animation:none}
::view-transition-old(ds-nav){display:none}
::view-transition-new(ds-nav){animation:none}
/* Conteúdo (a tela inteira, camada "root"): a página antiga sobe um pouco enquanto some e a nova entra
   de baixo enquanto aparece. Como é a tela inteira que se move, nada é esticado entre layouts diferentes
   (roteiros têm barra lateral e o Hub não). As duas nunca ficam sobrepostas. */
::view-transition-old(root){animation:ds-page-out .18s cubic-bezier(.4,0,1,1) both}
::view-transition-new(root){animation:ds-page-in .46s var(--ds-ease) .12s both}
@keyframes ds-page-out{to{opacity:0;transform:translateY(-10px)}}
@keyframes ds-page-in{from{opacity:0;transform:translateY(16px)}}
@keyframes ds-fade-out{to{opacity:0}}
@keyframes ds-fade-in{from{opacity:0}}
/* Barra lateral dos roteiros (só em telas largas, onde ela fica fixa ao lado do conteúdo) */
@media (min-width:1040px){
  .sidebar{view-transition-name:ds-side}
  /* Entre dois roteiros ela fica no lugar e só troca o conteúdo, sem sobrepor os textos */
  ::view-transition-group(ds-side){animation:none}
  ::view-transition-old(ds-side){animation:ds-fade-out .14s ease-in both}
  ::view-transition-new(ds-side){animation:ds-fade-in .3s ease-out .1s both}
  /* Do Hub/Projetos para um roteiro ela desliza da esquerda; na volta, desliza para a esquerda */
  ::view-transition-new(ds-side):only-child{animation:ds-side-in .5s var(--ds-ease) .06s both}
  ::view-transition-old(ds-side):only-child{animation:ds-side-out .24s cubic-bezier(.4,0,1,1) both}
}
@keyframes ds-side-in{from{opacity:0;transform:translateX(-28px)}}
@keyframes ds-side-out{to{opacity:0;transform:translateX(-28px)}}

/* ============================ PALETA DE COMANDOS ============================ */
.ds-pal{position:fixed;inset:0;z-index:2000;display:none;align-items:flex-start;justify-content:center;padding:12vh 16px 16px;background:color-mix(in srgb,#020608 55%,transparent);backdrop-filter:blur(6px)}
.ds-pal.open{display:flex}
.ds-pal-box{width:min(640px,100%);border-radius:18px;border:1px solid var(--ds-line);background:var(--card);box-shadow:0 40px 90px -30px rgba(0,0,0,.7);overflow:hidden;animation:ds-modal-in .3s var(--ds-ease)}
.ds-pal-in{display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid var(--ds-line)}
.ds-pal-in input{flex:1;font:500 1rem var(--ds-font);background:transparent;border:0;outline:0;color:var(--tx)}
.ds-pal-list{max-height:min(56vh,440px);overflow:auto;padding:6px}
.ds-pal-grp{font-size:.68rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--mu);padding:10px 12px 4px}
.ds-pal-it{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:10px;cursor:pointer;color:var(--tx);font-size:.9rem}
.ds-pal-it small{margin-left:auto;color:var(--mu);font-size:.74rem;white-space:nowrap}
.ds-pal-it .dot{width:8px;height:8px;border-radius:50%;flex:none;background:var(--bd)}
.ds-pal-it .dot.e{background:#2fa36b}.ds-pal-it .dot.r{background:#e8a100}
.ds-pal-it[aria-selected="true"]{background:color-mix(in srgb,var(--t,var(--t-hub)) 14%,transparent)}
.ds-pal-empty{padding:28px;text-align:center;color:var(--mu);font-size:.9rem}
.ds-pal-foot{display:flex;gap:14px;padding:10px 16px;border-top:1px solid var(--ds-line);font-size:.72rem;color:var(--mu)}

/* ============================ RESPONSIVO ============================ */
@media (max-width:980px){
  .hub-hero.ds-hero{grid-template-columns:1fr;gap:26px;min-height:0}
}
@media (max-width:760px){
  .hub-hero.ds-hero{margin-top:0}
  .hub-hero.ds-hero p{font-size:.96rem!important}
  .ds-btn{padding:12px 15px;font-size:.88rem}
  .ds-k-btn .ds-k-label,.ds-k-btn kbd{display:none}
  .ds-k-btn{padding:7px 9px}
  .ds-route .st-name{font-size:22px}
  .ds-route .st-pct{font-size:18px;transform:translateY(12px)}
  .ds-route .st-name{transform:translateY(4px)}
  .ds-route .goal{font-size:17px}
  .ds-route-legend{font-size:.78rem}
  #nav-db-status{display:none!important}
  .jr-sect{padding:18px 14px!important}
  .topic-row:hover{transform:none}
  .ds-pal{padding-top:8vh}
}

/* ============================ MOVIMENTO REDUZIDO ============================ */
@media (prefers-reduced-motion:reduce){
  @view-transition{navigation:none}
  body::before,.ds-grad,.ds-eyebrow i,.ds-route .you-halo{animation:none!important}
  .phase-card,.track-card,.jr-card,.proj-card,.ds-section-title{animation:none!important}
  .unified-study-box,.ds-pal-box{animation:none!important}
  .ds-route .r-lit,.ds-route .st-ring,.track-progress-fill{transition:none!important}
  .track-card:hover,.topic-row:hover,.ds-btn-primary:hover{transform:none!important}
}
</style>
"""

DESIGN_JS = r"""
<script id="design-v2-js">
window.DS_TOPICS = __DS_TOPICS__;
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var norm = function (s) { return String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };

  var PAGES = [
    { t: "Hub Central", d: "Sua jornada e o mapa da trilha", href: "index.html", ico: "🧭", k: "hub" },
    { t: "IA & Código", d: "Python, dados, Machine Learning, Deep Learning e LLMs", href: "ia.html", ico: "🤖", k: "ia" },
    { t: "Matemática para IA", d: "Álgebra linear, cálculo, probabilidade e atenção", href: "matematica.html", ico: "📐", k: "mat" },
    { t: "Inglês", d: "Do básico aos tempos verbais avançados", href: "ingles.html", ico: "🗣️", k: "ing" },
    { t: "Projetos & Portfólio", d: "Projetos práticos para o seu GitHub", href: "projetos.html", ico: "🛠️", k: "proj" }
  ];

  /* ---------- Holofote que segue o cursor ---------- */
  function initSpotlight() {
    var sel = ".track-card,.jr-card,.phase-card,.proj-card,.tracker-box,.progress-card";
    $$(sel).forEach(function (el) { el.classList.add("ds-spot"); });
    document.addEventListener("pointermove", function (e) {
      var el = e.target && e.target.closest && e.target.closest(".ds-spot");
      if (!el) return;
      var r = el.getBoundingClientRect();
      el.style.setProperty("--mx", (e.clientX - r.left) + "px");
      el.style.setProperty("--my", (e.clientY - r.top) + "px");
    }, { passive: true });
  }

  /* ---------- Cartões das trilhas ganham a cor da trilha ---------- */
  function tagTrackCards() {
    $$(".track-card").forEach(function (c) {
      var a = c.querySelector("a[href]"); if (!a) return;
      var h = a.getAttribute("href");
      c.dataset.track = /ia\.html/.test(h) ? "ia" : /matematica/.test(h) ? "mat" : /ingles/.test(h) ? "ing" : /projetos/.test(h) ? "proj" : "hub";
    });
  }

  /* ---------- Mapa da trilha (Hub) ---------- */
  var ROUTE_D = "M60 330 C 150 330, 150 250, 215 236 S 330 250, 350 180 S 300 92, 390 78 S 500 70, 560 50";
  var STATIONS = [
    { k: "ia", at: 0.20, name: "IA & Código", ico: "🤖", href: "ia.html" },
    { k: "mat", at: 0.43, name: "Matemática", ico: "📐", href: "matematica.html" },
    { k: "ing", at: 0.65, name: "Inglês", ico: "🗣️", href: "ingles.html" },
    { k: "proj", at: 0.86, name: "Projetos", ico: "🛠️", href: "projetos.html" }
  ];
  var routeState = null;
  function buildRoute() {
    var host = $("#ds-route"); if (!host || host.dataset.built) return;
    host.dataset.built = "1";
    var NS = "http://www.w3.org/2000/svg";
    var svg = '<svg viewBox="0 0 620 400" role="img" aria-labelledby="ds-route-t"><title id="ds-route-t">Mapa da sua trilha de estudos</title>' +
      '<defs><linearGradient id="dsRouteGrad" x1="0" y1="1" x2="1" y2="0"><stop offset="0" style="stop-color:var(--t-ia)"/><stop offset=".45" style="stop-color:var(--t-hub)"/><stop offset=".75" style="stop-color:var(--t-ing)"/><stop offset="1" style="stop-color:var(--t-mat)"/></linearGradient></defs>' +
      '<path class="r-base" d="' + ROUTE_D + '"/><path class="r-dash" d="' + ROUTE_D + '"/><path class="r-lit" d="' + ROUTE_D + '"/>' +
      '<g class="stations"></g><g class="youg"><circle class="you-halo" r="9"/><circle class="you" r="6"/></g>' +
      '<text class="goal" x="566" y="30" text-anchor="end">IA ✦</text><text class="goal" x="60" y="306" text-anchor="middle">ZERO</text></svg>' +
      '<div class="ds-route-legend"><span>Você está em <b id="ds-route-pct">0%</b> da jornada</span><span id="ds-route-next"></span></div>';
    host.innerHTML = svg;
    var path = host.querySelector(".r-lit"), L = path.getTotalLength();
    path.style.strokeDasharray = L; path.style.strokeDashoffset = L;
    var g = host.querySelector(".stations"), C = 2 * Math.PI * 24;
    STATIONS.forEach(function (s) {
      var p = path.getPointAtLength(L * s.at);
      var a = document.createElementNS(NS, "a");
      a.setAttribute("href", s.href); a.setAttribute("class", "st"); a.setAttribute("tabindex", "0");
      a.style.color = "var(--t-" + s.k + ")";
      a.innerHTML = '<title>' + s.name + '</title><circle class="st-ring-bg" cx="' + p.x + '" cy="' + p.y + '" r="24"/>' +
        '<circle class="st-ring" cx="' + p.x + '" cy="' + p.y + '" r="24" data-k="' + s.k + '" style="stroke:var(--t-' + s.k + ')" stroke-dasharray="' + C + '" stroke-dashoffset="' + C + '"/>' +
        '<text class="st-ico" x="' + p.x + '" y="' + p.y + '">' + s.ico + '</text>' +
        '<text class="st-name" x="' + p.x + '" y="' + (p.y + 44) + '">' + s.name + '</text>' +
        '<text class="st-pct" x="' + p.x + '" y="' + (p.y + 59) + '" data-pct="' + s.k + '">0%</text>';
      g.appendChild(a);
    });
    routeState = { path: path, L: L, C: C, host: host };
    var start = path.getPointAtLength(0);
    moveYou(start.x, start.y);
  }
  function moveYou(x, y) {
    var g = routeState && routeState.host.querySelector(".youg"); if (!g) return;
    g.setAttribute("transform", "translate(" + x + " " + y + ")");
  }
  var youAnim = null;
  // Chamado pelo cálculo do Hub com os números reais de progresso
  window.dsRoute = function (d) {
    buildRoute(); if (!routeState) return;
    var f = Math.max(0, Math.min(1, (d.overall || 0) / 100));
    // o ponto aceso nunca fica "atrás" da primeira estação quando há progresso
    var vis = f > 0 ? Math.max(0.03, f) : 0;
    routeState.path.style.strokeDashoffset = routeState.L * (1 - vis);
    STATIONS.forEach(function (s) {
      var v = Math.max(0, Math.min(100, (d.per && d.per[s.k]) || 0));
      var ring = routeState.host.querySelector('.st-ring[data-k="' + s.k + '"]');
      if (ring) ring.style.strokeDashoffset = routeState.C * (1 - v / 100);
      var t = routeState.host.querySelector('[data-pct="' + s.k + '"]');
      if (t) t.textContent = Math.round(v) + "%";
    });
    var pctEl = $("#ds-route-pct"); if (pctEl) pctEl.textContent = (Math.round((d.overall || 0) * 10) / 10).toLocaleString("pt-BR") + "%";
    var nx = $("#ds-route-next"); if (nx && d.nextLabel) nx.textContent = "Próxima parada: " + d.nextLabel;
    var cont = $("#ds-continue"); if (cont && d.nextHref) cont.setAttribute("href", d.nextHref);
    // "você está aqui" desliza pelo caminho até o progresso atual
    var target = routeState.L * vis;
    if (youAnim) cancelAnimationFrame(youAnim);
    if (reduce) { var p = routeState.path.getPointAtLength(target); moveYou(p.x, p.y); return; }
    var t0 = null, from = routeState.cur || 0, dur = 1600;
    var step = function (ts) {
      if (!t0) t0 = ts;
      var k = Math.min(1, (ts - t0) / dur), e = 1 - Math.pow(1 - k, 3), len = from + (target - from) * e;
      var p = routeState.path.getPointAtLength(len); moveYou(p.x, p.y); routeState.cur = len;
      if (k < 1) youAnim = requestAnimationFrame(step);
    };
    youAnim = requestAnimationFrame(step);
  };

  /* ---------- Paleta de comandos (Ctrl/⌘ + K) ---------- */
  var pal = null, items = [], sel = 0;
  function readPR() { try { return JSON.parse(localStorage.getItem("roteiro-ia-v1") || "{}") || {}; } catch (e) { return {}; } }
  function collect() {
    var out = [];
    PAGES.forEach(function (p) { out.push({ grp: "Páginas", t: p.t, d: p.d, ico: p.ico, run: function () { location.href = p.href; } }); });
    out.push({ grp: "Ações", t: "Alternar tema claro/escuro", d: "", ico: "🌓", run: function () { if (typeof toggleTheme === "function") toggleTheme(); } });
    var pr = readPR(), here = document.body.getAttribute("data-track");
    var NAMES = { ia: "IA & Código", mat: "Matemática", ing: "Inglês" }, PAGE = { ia: "ia.html", mat: "matematica.html", ing: "ingles.html" };
    var idx = window.DS_TOPICS || [];
    // tópicos da trilha atual primeiro
    idx.slice().sort(function (a, b) { return (a[1] === here ? 0 : 1) - (b[1] === here ? 0 : 1); }).forEach(function (row) {
      var id = row[0], tr = row[1], title = row[2], st = (pr[id] || {}).s || "z";
      out.push({ grp: "Tópicos", t: title, d: NAMES[tr] || "", st: st, ico: "", topic: true,
        run: function () {
          if (tr === here && typeof openStudyModal === "function" && typeof TOPICS_MAP !== "undefined" && TOPICS_MAP[id]) openStudyModal(id, Boolean(TOPICS_MAP[id].pt_guide), 1);
          else location.href = PAGE[tr] + "?aula=" + encodeURIComponent(id);
        } });
    });
    return out;
  }
  function render(q) {
    var list = $(".ds-pal-list", pal), all = collect(), toks = norm(q).split(/\s+/).filter(Boolean);
    items = !toks.length ? all.filter(function (x) { return !x.topic; }).concat(all.filter(function (x) { return x.topic && x.st === "r"; }).slice(0, 6))
      : all.filter(function (x) { var h = norm(x.t + " " + x.d); return toks.every(function (t) { return h.indexOf(t) >= 0; }); }).slice(0, 60);
    sel = 0;
    if (!items.length) { list.innerHTML = '<div class="ds-pal-empty">Nada encontrado para “' + esc(q) + '”.</div>'; return; }
    var html = "", last = "";
    items.forEach(function (x, i) {
      var gl = x.topic && !toks.length ? "Em andamento" : x.grp;
      if (gl !== last) { html += '<div class="ds-pal-grp">' + gl + "</div>"; last = gl; }
      html += '<div class="ds-pal-it" role="option" id="ds-pal-' + i + '" data-i="' + i + '" aria-selected="' + (i === 0) + '">' +
        (x.ico ? "<span>" + x.ico + "</span>" : '<span class="dot ' + (x.st || "") + '"></span>') + "<span>" + esc(x.t) + "</span>" +
        (x.d ? "<small>" + esc(x.d) + "</small>" : "") + "</div>";
    });
    list.innerHTML = html;
  }
  function move(d) {
    if (!items.length) return;
    var prev = $('#ds-pal-' + sel, pal); if (prev) prev.setAttribute("aria-selected", "false");
    sel = (sel + d + items.length) % items.length;
    var cur = $('#ds-pal-' + sel, pal); if (cur) { cur.setAttribute("aria-selected", "true"); cur.scrollIntoView({ block: "nearest" }); }
    $("input", pal).setAttribute("aria-activedescendant", "ds-pal-" + sel);
  }
  function choose(i) { var x = items[i]; if (!x) return; closePal(); setTimeout(x.run, 10); }
  function buildPal() {
    pal = document.createElement("div");
    pal.className = "ds-pal"; pal.setAttribute("role", "dialog"); pal.setAttribute("aria-modal", "true"); pal.setAttribute("aria-label", "Buscar páginas e tópicos");
    pal.innerHTML = '<div class="ds-pal-box"><div class="ds-pal-in"><span aria-hidden="true">🔎</span>' +
      '<input type="text" placeholder="Buscar páginas, tópicos e ações…" aria-label="Buscar" role="combobox" aria-expanded="true" aria-controls="ds-pal-list" autocomplete="off">' +
      '<span class="ds-kbd">Esc</span></div><div class="ds-pal-list" id="ds-pal-list" role="listbox"></div>' +
      '<div class="ds-pal-foot"><span><span class="ds-kbd">↑↓</span> navegar</span><span><span class="ds-kbd">Enter</span> abrir</span><span><span class="ds-kbd">Esc</span> fechar</span></div></div>';
    document.body.appendChild(pal);
    var inp = $("input", pal);
    inp.addEventListener("input", function () { render(inp.value); });
    inp.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Enter") { e.preventDefault(); choose(sel); }
      else if (e.key === "Escape") { e.preventDefault(); closePal(); }
    });
    pal.addEventListener("click", function (e) {
      var it = e.target.closest(".ds-pal-it"); if (it) { choose(+it.dataset.i); return; }
      if (e.target === pal) closePal();
    });
  }
  var lastFocus = null;
  function openPal() {
    if (!pal) buildPal();
    lastFocus = document.activeElement;
    pal.classList.add("open"); var inp = $("input", pal); inp.value = ""; render(""); inp.focus();
  }
  function closePal() { if (!pal) return; pal.classList.remove("open"); if (lastFocus && lastFocus.focus) lastFocus.focus(); }
  window.dsOpenPalette = openPal;
  document.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && (e.key === "k" || e.key === "K")) { e.preventDefault(); pal && pal.classList.contains("open") ? closePal() : openPal(); }
  });
  function addNavButton() {
    // O botão já vem no HTML (apply_design), para o menu não mudar de largura depois de desenhado.
    var right = $(".nav-right"); if (!right) return;
    var mac = /Mac|iPhone|iPad/.test(navigator.platform || "");
    var b = $(".ds-k-btn", right);
    if (!b) {
      b = document.createElement("button");
      b.type = "button"; b.className = "ds-k-btn";
      b.innerHTML = '<span aria-hidden="true">🔎</span><span class="ds-k-label">Buscar</span><kbd>Ctrl K</kbd>';
      right.insertBefore(b, right.firstChild);
    }
    if (mac) { var k = $("kbd", b); if (k) k.textContent = "⌘ K"; b.title = "Buscar páginas e tópicos (⌘ + K)"; }
    b.addEventListener("click", openPal);
  }

  function init() {
    var tr = document.body.getAttribute("data-track");
    if (!tr) document.body.setAttribute("data-track", /ia\.html/.test(location.pathname) ? "ia" : "hub");
    tagTrackCards(); initSpotlight(); addNavButton(); buildRoute();
    // Link direto para uma aula (vindo da busca em outra página): pagina.html?aula=<id>
    try {
      var aula = new URLSearchParams(location.search).get("aula");
      if (aula && typeof TOPICS_MAP !== "undefined" && TOPICS_MAP[aula] && typeof openStudyModal === "function") {
        setTimeout(function () { openStudyModal(aula, Boolean(TOPICS_MAP[aula].pt_guide), 1); }, 350);
        history.replaceState(null, "", location.pathname);
      }
    } catch (e) {}
  }
  // Este script fica no fim do <body>: o conteúdo já existe, então monta na hora (antes da primeira pintura).
  init();
})();
</script>
"""


_TOPIC_INDEX_JSON = "[]"


def set_topic_index(tracks):
    """tracks = {"ia": phases, "mat": phases, "ing": phases}. Gera [[id, trilha, título], ...] com os
    mesmos ids das páginas (trilha-fase-grupo-tópico), para a busca achar qualquer aula."""
    import json
    rows = []
    for tr, phases in tracks.items():
        for p_idx, p in enumerate(phases):
            for g_idx, g in enumerate(p["g"]):
                for t_idx, raw in enumerate(g[1]):
                    if isinstance(raw, dict):
                        title = raw.get("title", "")
                    elif isinstance(raw, str) and "||" in raw:
                        title = raw.split("||", 1)[0]
                    else:
                        title = str(raw)
                    rows.append([f"{tr}-{p_idx}-{g_idx}-{t_idx}", tr, title])
    global _TOPIC_INDEX_JSON
    _TOPIC_INDEX_JSON = json.dumps(rows, ensure_ascii=False, separators=(",", ":")).replace("</", "<\/")


# Roda logo depois do menu, antes da primeira pintura: o selo já nasce "Nuvem" para quem está logado
# (antes ele aparecia como "Local" e trocava ~1 s depois, fazendo o menu pular a cada troca de página).
NAV_EARLY_SCRIPT = """<script>
(function () {
  try {
    var raw = localStorage.getItem("roteiro_auth_user") || sessionStorage.getItem("roteiro_auth_user");
    var u = raw ? JSON.parse(raw) : null;
    var b = document.getElementById("nav-db-status");
    if (!b || !u || !u.token || !(u.exp * 1000 > Date.now())) return;
    if (localStorage.getItem("roteiro_data_owner") !== u.email) return;
    b.className = "nav-status-pill badge-pg";
    b.style.background = "#10b981";
    b.style.color = "#fff";
    b.style.display = "inline-flex";
    b.textContent = "\\u2601\\ufe0f Nuvem";
  } catch (e) {}
})();
</script>"""


# Botão de busca já no HTML do menu (antes era criado por JavaScript depois da primeira pintura e
# empurrava os links do menu ~86 px para os lados em IA, Matemática e Inglês).
NAV_SEARCH_BUTTON = ('<button type="button" class="ds-k-btn" title="Buscar páginas e tópicos (Ctrl + K)">'
                     '<span aria-hidden="true">🔎</span><span class="ds-k-label">Buscar</span><kbd>Ctrl K</kbd></button>')


def apply_design(html: str, track: str) -> str:
    """Injeta a camada de design no fim do <head> e do <body> e marca a trilha da página."""
    from modal_ui import MODAL_UI_CSS, MODAL_UI_JS
    html = html.replace("</head>", DESIGN_HEAD + "\n" + MODAL_UI_CSS + "\n</head>", 1)
    html = html.replace("<body>", f'<body data-track="{track}">', 1)
    html = html.replace("</header>", "</header>\n" + NAV_EARLY_SCRIPT, 1)
    html = html.replace('<div class="nav-right">', '<div class="nav-right">\n' + NAV_SEARCH_BUTTON, 1)
    idx = html.rfind("</body>")
    if idx != -1:
        html = (html[:idx] + DESIGN_JS.replace("__DS_TOPICS__", _TOPIC_INDEX_JSON) + "\n" + MODAL_UI_JS
                + '\n<div id="ds-end" hidden></div>\n' + html[idx:])
    return html
