# -*- coding: utf-8 -*-
"""
Avisos (fase 3): o que pede atenção, num sino 🔔 em todas as páginas e num cartão "Hoje" no hub.

Fontes (tudo o que o site já guarda; nada novo para preencher):
  revisões     agenda única (RV): de hoje e atrasadas
  prazos       "Meta de conclusão" de cada aula (progresso[id].d), só de aulas não concluídas;
               prazo de cada projeto (projetos[].prazo, campo novo na página Projetos)
  pendentes    aula concluída sem o quiz de saída; aula em andamento parada há 7 dias ou mais;
               projeto em andamento sem prazo
  ritmo        sequência de dias de estudo em risco (estudou ontem, ainda não hoje); dias sem estudar

O número vermelho do sino conta só o urgente: revisões de hoje/atrasadas e prazos vencidos ou de hoje.
Pendentes e ritmo aparecem no painel, sem número, e podem ser ocultados (fica só neste aparelho).

AV_JS é puro o bastante para rodar no Node (testes), com RV e um localStorage falso.
"""

AV_JS = r"""
// =================== AVISOS: o que pede atenção (sem tela; testado no Node) ===================
const AV = (() => {
  const DAY = 86400000, HIDE_KEY = "roteiro-avisos-ocultos";
  const read = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k) || "null"); return v == null ? d : v; } catch (e) { return d; } };
  const isDate = d => typeof d === "string" && /^\d{4}-\d{2}-\d{2}/.test(d);

  // Dias com estudo (o mesmo critério das Conquistas): sessões no estúdio, conclusões/avanços e revisões feitas.
  // last[id] = última atividade em cada aula (sessão ou mudança de situação).
  function studyDays() {
    const days = new Set(), last = {};
    read("roteiro-sessions-v1", []).forEach(s => {
      if (!s || !s.t) return;
      if ((s.sec || 0) > 0) days.add(RV.today(s.t));
      if (s.id) last[s.id] = Math.max(last[s.id] || 0, s.t);
    });
    read("roteiro-events-v1", []).forEach(e => {
      if (!e || !e.t) return;
      if (e.to === "e" || e.to === "r") days.add(RV.today(e.t));
      if (e.id) last[e.id] = Math.max(last[e.id] || 0, e.t);
    });
    const recs = read(RV.KEY, {});
    for (const id in recs) (recs[id] && Array.isArray(recs[id].hist) ? recs[id].hist : []).forEach(h => { const t = Number(h && h[0]); if (t) days.add(RV.today(t)); });
    return { days, last };
  }

  // Sequência: dias seguidos estudando até hoje (ou até ontem, se ainda não estudou hoje)
  function streakInfo(now) {
    const { days } = studyDays(), hoje = RV.today(now);
    let n = 0, d = days.has(hoje) ? hoje : RV.addDays(hoje, -1);
    while (days.has(d)) { n++; d = RV.addDays(d, -1); }
    let lastDay = null;
    days.forEach(k => { if (!lastDay || k > lastDay) lastDay = k; });
    return { streak: n, today: days.has(hoje), lastDay };
  }

  // Só o urgente (número vermelho do sino): revisões de hoje/atrasadas + prazos vencidos ou de hoje
  function urgentCount(now) {
    const hoje = RV.today(now);
    let n = RV.counts(now).due;
    const prog = read("roteiro-ia-v1", {});
    for (const id in prog) { const p = prog[id]; if (p && p.s !== "e" && isDate(p.d) && String(p.d).slice(0, 10) <= hoje) n++; }
    const projs = read("roteiro_portfolio_projects", []);
    (Array.isArray(projs) ? projs : []).forEach(pj => { if (pj && pj.status !== "done" && isDate(pj.prazo) && pj.prazo.slice(0, 10) <= hoje) n++; });
    return n;
  }

  // Lista completa. topics = [[id, trilha, título, tem_quiz], ...] (o índice da busca)
  function list(now, topics) {
    now = now == null ? Date.now() : now;
    const hoje = RV.today(now), T = {}, out = [];
    (topics || []).forEach(r => { T[r[0]] = r; });
    const prog = read("roteiro-ia-v1", {}), rev = read(RV.KEY, {}), projs = read("roteiro_portfolio_projects", []);
    const P = Array.isArray(projs) ? projs : [];
    // 1) revisões de hoje e atrasadas
    const c = RV.counts(now);
    if (c.due) out.push({ k: "rev", grupo: "hoje", urg: c.due, n: c.due, late: c.late, ids: RV.agenda(now).filter(it => it.due <= hoje && T[it.id]).map(it => it.id), key: "rev" });
    // 2) prazos das aulas ainda não concluídas: vencidos, de hoje e dos próximos 3 dias
    Object.keys(prog).sort().forEach(id => {
      const p = prog[id];
      if (!p || p.s === "e" || !isDate(p.d) || !T[id]) return;
      const d = String(p.d).slice(0, 10), n = RV.between(hoje, d);
      if (n <= 3) out.push({ k: "prazo", grupo: n <= 0 ? "hoje" : "breve", urg: n <= 0 ? 1 : 0, id, d, n, key: "prazo:" + id + ":" + d });
    });
    // 3) prazos dos projetos
    P.forEach(pj => {
      if (!pj || pj.status === "done" || !isDate(pj.prazo)) return;
      const d = pj.prazo.slice(0, 10), n = RV.between(hoje, d);
      if (n <= 3) out.push({ k: "proj", grupo: n <= 0 ? "hoje" : "breve", urg: n <= 0 ? 1 : 0, pid: pj.id, titulo: pj.title || "Projeto", d, n, key: "proj:" + pj.id + ":" + d });
    });
    // 4) aulas concluídas que têm quiz de saída, sem a aprovação registrada
    const semQuiz = Object.keys(prog).filter(id => prog[id] && prog[id].s === "e" && T[id] && T[id][3] && !(rev[id] && rev[id].passedAt)).sort();
    if (semQuiz.length) out.push({ k: "quiz", grupo: "pend", urg: 0, ids: semQuiz, key: "quiz:" + semQuiz.length });
    // 5) aulas em andamento sem atividade há 7 dias ou mais (sem registro de atividade, não dá para saber: fica de fora)
    const { last } = studyDays();
    const paradas = Object.keys(prog).filter(id => prog[id] && prog[id].s === "r" && T[id] && last[id] && now - last[id] >= 7 * DAY)
      .sort((a, b) => last[a] - last[b]).map(id => ({ id, dias: Math.floor((now - last[id]) / DAY) }));
    if (paradas.length) out.push({ k: "parada", grupo: "pend", urg: 0, itens: paradas, key: "parada:" + paradas.map(x => x.id + "@" + last[x.id]).join(",") });
    // 6) projetos em andamento sem prazo
    const semPrazo = P.filter(pj => pj && pj.status === "wip" && !isDate(pj.prazo));
    if (semPrazo.length) out.push({ k: "semprazo", grupo: "pend", urg: 0, projs: semPrazo.map(pj => ({ pid: pj.id, titulo: pj.title || "Projeto" })),
                                    key: "semprazo:" + semPrazo.map(pj => pj.id).join(",") });
    // 7) ritmo: sequência em risco, ou dias sem estudar
    const s = streakInfo(now);
    if (!s.today && s.streak >= 2) out.push({ k: "seq", grupo: "ritmo", urg: 0, n: s.streak, key: "seq:" + hoje });
    else if (!s.today && !s.streak && s.lastDay) {
      const dias = RV.between(s.lastDay, hoje);
      if (dias >= 3) out.push({ k: "parado", grupo: "ritmo", urg: 0, dias, key: "parado:" + s.lastDay });
    }
    const oc = read(HIDE_KEY, {});
    return out.filter(a => a.urg || !oc[a.key]);   // o urgente nunca some por ter sido ocultado
  }

  function hide(key, now) {
    const oc = read(HIDE_KEY, {});
    oc[key] = now == null ? Date.now() : now;
    try { localStorage.setItem(HIDE_KEY, JSON.stringify(oc)); } catch (e) {}
  }

  return { list, urgentCount, hide, streakInfo, studyDays, HIDE_KEY };
})();
if (typeof module !== "undefined") module.exports = AV;
"""

AV_UI_JS = r"""
// =================== SINO DE AVISOS E CARTÃO "HOJE" DO HUB ===================
let AV_MAP = null;
function avTopic(id) { if (!AV_MAP) { AV_MAP = {}; (window.DS_TOPICS || []).forEach(r => { AV_MAP[r[0]] = r; }); } return AV_MAP[id]; }
// Nome curto, como na lista da trilha (listing_generator._list_title): "Aula 04 · assunto" no Inglês
function avTitle(id) {
  const r = avTopic(id); if (!r) return id;
  const t = String(r[2]).replace(/\\u0026/g, "&");
  const m = t.match(/^Curso de Inglês - Módulo \d+ Aula (\d+)\s*[:\-]?\s*(.+)$/);
  if (m) return "Aula " + String(+m[1]).padStart(2, "0") + " · " + m[2];
  return /^Curso de Inglês GRÁTIS - Aula Zero$/.test(t) ? "Aula Zero" : t;
}
function avLink(id) { return RV_TRACKS[rvTrackOf(id)].pagina + "?aula=" + encodeURIComponent(id); }
function avPrazo(n, d) {
  return n < 0 ? (n === -1 ? "venceu ontem" : "venceu há " + (-n) + " dias") : n === 0 ? "vence hoje" : n === 1 ? "vence amanhã" : "vence " + RV.fmt(d);
}
function avPlural(n, um, varios) { return n + " " + (n === 1 ? um : varios); }
function avLinks(ids, max) {
  const mais = ids.length - max;
  return ids.slice(0, max).map(id => '<a href="' + avLink(id) + '">' + rvEsc(avTitle(id)) + "</a>").join(" · ") + (mais > 0 ? " · e mais " + mais : "");
}
const AV_GRUPOS = [["hoje", "Hoje"], ["breve", "Nos próximos dias"], ["pend", "Pendentes"], ["ritmo", "Ritmo"]];

// Um aviso: ícone, texto e ação
function avItem(a) {
  const naRevisoes = typeof raStartDay === "function";
  let ico = "", txt = "", sub = "", act = "";
  switch (a.k) {
    case "rev":
      ico = "↻"; txt = "<b>" + avPlural(a.n, "revisão", "revisões") + " para hoje</b>" + (a.late ? " · " + avPlural(a.late, "atrasada", "atrasadas") : "");
      sub = a.ids.length ? avLinks(a.ids, 3) : "";
      act = naRevisoes ? '<button type="button" class="av-act pri" onclick="avClose(); raStartDay()">Começar</button>'
                       : '<a class="av-act pri" href="revisoes.html?dia=1">Começar</a>';
      break;
    case "prazo":
      ico = "⏰"; txt = "<b>Prazo " + avPrazo(a.n, a.d) + ":</b> " + rvEsc(avTitle(a.id)); sub = "Meta de conclusão que você definiu para esta aula";
      act = '<a class="av-act" href="' + avLink(a.id) + '">Abrir aula</a>';
      break;
    case "proj":
      ico = "🛠️"; txt = "<b>Projeto " + avPrazo(a.n, a.d) + ":</b> " + rvEsc(a.titulo);
      act = '<a class="av-act" href="projetos.html#' + encodeURIComponent(a.pid) + '">Ver projeto</a>';
      break;
    case "quiz":
      ico = "📝"; txt = "<b>" + avPlural(a.ids.length, "aula concluída", "aulas concluídas") + " sem o quiz de saída</b>";
      sub = avLinks(a.ids, 3) + "<br>O quiz agenda as revisões e libera o “Vá mais fundo”.";
      act = '<a class="av-act" href="' + avLink(a.ids[0]) + '">Fazer o quiz</a>';
      break;
    case "parada":
      ico = "💤";
      txt = a.itens.length === 1 ? "<b>Parada há " + a.itens[0].dias + " dias:</b> " + rvEsc(avTitle(a.itens[0].id))
                                 : "<b>" + a.itens.length + " aulas em andamento paradas há 7 dias ou mais</b>";
      sub = a.itens.length === 1 ? "Em andamento, sem estudo desde então" : avLinks(a.itens.map(x => x.id), 3);
      act = '<a class="av-act" href="' + avLink(a.itens[0].id) + '">Continuar</a>';
      break;
    case "semprazo":
      ico = "🛠️"; txt = "<b>" + (a.projs.length === 1 ? "Projeto em andamento sem prazo:</b> " + rvEsc(a.projs[0].titulo) : a.projs.length + " projetos em andamento sem prazo</b>");
      sub = "Defina uma data e ele entra nos avisos";
      act = '<a class="av-act" href="projetos.html#' + encodeURIComponent(a.projs[0].pid) + '">Definir prazo</a>';
      break;
    case "seq":
      ico = "🔥"; txt = "<b>Sequência de " + a.n + " dias:</b> estude hoje para não quebrar"; sub = "Uma revisão de 5 minutos já conta.";
      act = naRevisoes ? '<button type="button" class="av-act" onclick="avClose(); raStartDay()">Revisar</button>' : '<a class="av-act" href="revisoes.html">Revisar</a>';
      break;
    case "parado":
      ico = "😴"; txt = "<b>Faz " + a.dias + " dias sem estudar</b>"; sub = "5 minutos de revisão já retomam o ritmo.";
      act = '<a class="av-act" href="revisoes.html">Retomar</a>';
      break;
  }
  const ocultar = a.urg ? "" : '<button type="button" class="av-hide" data-key="' + rvEsc(a.key) + '" title="Ocultar este aviso (neste aparelho)" aria-label="Ocultar este aviso">✕</button>';
  return '<li class="av-item' + (a.urg ? " urg" : "") + '"><span class="av-ico" aria-hidden="true">' + ico + '</span><div class="av-t">' + txt +
         (sub ? "<small>" + sub + "</small>" : "") + '</div><div class="av-acts">' + act + ocultar + "</div></li>";
}

function avGroupsHTML(items, max) {
  let h = "", n = 0;
  AV_GRUPOS.forEach(([g, nome]) => {
    const its = items.filter(a => a.grupo === g).slice(0, max ? Math.max(0, max - n) : 99);
    n += its.length;
    if (its.length) h += '<div class="av-g">' + nome + '</div><ul class="av-list">' + its.map(avItem).join("") + "</ul>";
  });
  return h;
}

function avBindHide(root) {
  root.querySelectorAll(".av-hide").forEach(b => b.onclick = e => { e.stopPropagation(); AV.hide(b.dataset.key); avRefresh(); });
}

// Painel do sino
let AV_PANEL = null;
function avClose() {
  if (!AV_PANEL) return;
  AV_PANEL.el.remove();
  document.removeEventListener("pointerdown", AV_PANEL.out, true);
  document.removeEventListener("keydown", AV_PANEL.key, true);
  const b = document.getElementById("av-bell"); if (b) b.setAttribute("aria-expanded", "false");
  AV_PANEL = null;
}
function avToggle(btn) {
  if (AV_PANEL) { avClose(); return; }
  const el = document.createElement("div");
  el.className = "av-panel"; el.setAttribute("role", "dialog"); el.setAttribute("aria-label", "Avisos");
  document.body.appendChild(el);
  const out = e => { if (!el.contains(e.target) && !(btn && btn.contains(e.target))) avClose(); };
  const key = e => { if (e.key === "Escape") { e.stopPropagation(); avClose(); } };
  document.addEventListener("pointerdown", out, true);
  document.addEventListener("keydown", key, true);
  AV_PANEL = { el, btn, out, key };
  if (btn) btn.setAttribute("aria-expanded", "true");
  avRenderPanel();
}
function avRenderPanel() {
  if (!AV_PANEL) return;
  const items = AV.list(Date.now(), window.DS_TOPICS || []), el = AV_PANEL.el, urg = AV.urgentCount();
  el.innerHTML = '<div class="av-head"><b>🔔 Avisos</b><span>' + (urg ? avPlural(urg, "urgente", "urgentes") : "nada urgente") + "</span></div>" +
    (items.length ? avGroupsHTML(items) : '<p class="av-empty">✨ Tudo em dia. Nenhuma revisão, prazo ou pendência agora.</p>') +
    '<p class="av-foot">Prazos: “Meta de conclusão” no ⋯ de cada aula e o campo Prazo de cada projeto.</p>';
  avBindHide(el);
  const r = AV_PANEL.btn ? AV_PANEL.btn.getBoundingClientRect() : { right: innerWidth - 10, bottom: 60 };
  el.style.top = Math.round(r.bottom + 8) + "px";
  el.style.left = Math.round(Math.max(10, Math.min(r.right - el.offsetWidth, innerWidth - el.offsetWidth - 10))) + "px";
}

// Número vermelho do sino (só o urgente)
function avBellBadge() {
  const b = document.getElementById("av-bell-badge");
  if (!b) return;
  const n = AV.urgentCount();
  b.textContent = n > 99 ? "99+" : n;
  b.hidden = !n;
  const bell = document.getElementById("av-bell");
  if (bell) bell.title = n ? "Avisos: " + avPlural(n, "urgente", "urgentes") : "Avisos";
}

// Cartão "Hoje" no topo do hub: os avisos mais importantes, com ação direta
function avRenderHoje() {
  const box = document.getElementById("av-hoje");
  if (!box) return;
  const items = AV.list(Date.now(), window.DS_TOPICS || []);
  box.hidden = false;
  box.innerHTML = '<div class="av-hoje-h"><h2>📋 Hoje</h2>' +
    (items.length > 4 ? '<button type="button" class="av-more" onclick="avToggle(document.getElementById(\'av-bell\'))">Ver todos os ' + items.length + " avisos</button>" : "") + "</div>" +
    (items.length ? avGroupsHTML(items, 4) : '<p class="av-empty">✨ Tudo em dia: nenhuma revisão, prazo ou pendência para hoje. Que tal adiantar a próxima aula?</p>');
  avBindHide(box);
}

function avRefresh() { try { avBellBadge(); avRenderHoje(); avRenderPanel(); } catch (e) {} }
// Depois que a página inteira existe (o índice das aulas, DS_TOPICS, vem no fim do <body>)
function avBoot() {
  avRefresh();
  window.addEventListener("rv:change", avRefresh);
  window.addEventListener("av:change", avRefresh);
}
"""

AV_CSS = r"""
/* ===== Avisos: sino, painel e cartão "Hoje" ===== */
.av-bell{position:relative;display:inline-grid;place-items:center;width:36px;height:36px;border-radius:50%;border:1px solid var(--bd);
  background:transparent;color:var(--tx);font-size:.95rem;cursor:pointer;flex:none}
.av-bell:hover,.av-bell[aria-expanded="true"]{border-color:var(--t-hub)}
.av-bell-badge{position:absolute;top:-5px;right:-5px;display:grid;place-items:center;min-width:18px;height:18px;padding:0 4px;border-radius:9px;
  background:#ef6b5b;color:#fff;font:800 .64rem/1 Inter,system-ui,sans-serif}
.av-bell-badge[hidden]{display:none}
.av-panel{position:fixed;z-index:100000;width:400px;max-width:calc(100vw - 20px);max-height:min(70vh,620px);overflow:auto;padding:12px 14px;
  border-radius:16px;border:1px solid var(--bd);background:var(--card);color:var(--tx);box-shadow:0 24px 60px rgba(0,0,0,.45);font-size:.85rem}
@media (max-width:600px){.av-panel{left:8px!important;right:8px;top:auto!important;bottom:8px;width:auto;max-height:80vh}}
.av-head{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:4px}
.av-head b{font-size:1rem}
.av-head span{font-size:.75rem;color:var(--mu)}
.av-g{margin:12px 0 6px;font-size:.68rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--mu)}
.av-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:7px}
.av-item{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border-radius:12px;border:1px solid var(--bd);background:var(--bg)}
.av-item.urg{border-color:color-mix(in srgb,#ef6b5b 45%,var(--bd))}
.av-ico{flex:none;width:20px;text-align:center;font-size:1rem;line-height:1.35}
.av-t{flex:1;min-width:0;line-height:1.4}
.av-t small{display:block;margin-top:3px;font-size:.74rem;color:var(--mu);line-height:1.45}
.av-t small a{color:var(--t-hub);text-decoration:none}
.av-t small a:hover{text-decoration:underline}
.av-acts{display:flex;align-items:center;gap:4px;flex:none}
.av-act{display:inline-flex;align-items:center;min-height:30px;padding:4px 11px;border-radius:99px;border:1px solid var(--bd);background:transparent;
  color:var(--tx);font:inherit;font-size:.76rem;font-weight:600;text-decoration:none;cursor:pointer;white-space:nowrap}
.av-act:hover{border-color:var(--t-hub)}
.av-act.pri{background:var(--t-hub);border-color:var(--t-hub);color:#04201d}
.av-hide{width:26px;height:26px;border:0;border-radius:50%;background:transparent;color:var(--mu);font:inherit;font-size:.75rem;cursor:pointer}
.av-hide:hover{background:var(--bd);color:var(--tx)}
.av-empty{margin:10px 0 4px;color:var(--mu);line-height:1.5}
.av-foot{margin:12px 0 0;padding-top:8px;border-top:1px solid var(--bd);font-size:.72rem;color:var(--mu)}
.av-hoje{margin:0 0 26px;padding:16px 18px;border-radius:18px;border:1px solid var(--bd);background:var(--card)}
.av-hoje[hidden]{display:none}
.av-hoje-h{display:flex;justify-content:space-between;align-items:center;gap:10px}
.av-hoje-h h2{margin:0;font-size:1.05rem}
.av-more{border:0;background:none;color:var(--t-hub);font:inherit;font-size:.8rem;font-weight:600;cursor:pointer}
.av-hoje .av-item{background:var(--bg)}
@media (max-width:640px){.av-item{flex-wrap:wrap}.av-acts{width:100%;justify-content:flex-end}}
"""

NAV_BELL = ('<button type="button" class="av-bell" id="av-bell" aria-haspopup="dialog" aria-expanded="false" title="Avisos" '
            'onclick="avToggle(this)"><span aria-hidden="true">🔔</span><span class="av-bell-badge" id="av-bell-badge" hidden></span></button>')
