# -*- coding: utf-8 -*-
"""
Agenda de revisões: uma fonte só para todas as páginas.

Junta as revisões que o quiz da aula agenda e as que você marca com "↻ Revisar" numa agenda única,
guardada em "roteiro-review-v1" (o mesmo registro que o quiz já usava). Ele vai para a nuvem no campo
"extra" do DynamoDB, e na junção a nuvem fica, para cada aula, com o registro de "last" mais recente.

Registro de uma aula (formato novo; os campos antigos do quiz continuam):
  due    "AAAA-MM-DD" da próxima revisão, no dia local (null = fora da agenda)
  step   posição em STEPS (intervalo atual, em dias)
  src    "quiz" (agendada pelo quiz) ou "manual" (agendada por você)
  hist   [[instante, nota], ...] das últimas revisões ("z" não lembrei, "m" com esforço, "f" fácil)
  done   instante da última revisão feita · mastered: instante em que a aula ficou dominada
  last   instante da última alteração (decide a junção com a nuvem)
  score, total, passedAt: dados do quiz (como antes)

Compatível com o que já existe:
  - registros antigos do quiz (next: [4 datas], done) viram agenda sem migração: a próxima data não feita
    é a revisão marcada; ao mexer, o registro passa para o formato novo;
  - a marca antiga "↻ Revisar" (progresso[id].rv, sem data) entra como revisão de hoje até você agendar,
    revisar ou tirar.

REVIEW_JS é puro o bastante para rodar no Node (testes), com um localStorage falso.
REVIEW_UI_JS / REVIEW_UI_CSS: o menu "Quando revisar?", o aviso com "desfazer" e o contador do menu.
"""

REVIEW_JS = r"""
const RV = (() => {
  const KEY = "roteiro-review-v1", PKEY = "roteiro-ia-v1", DAY = 86400000;
  const STEPS = [1, 3, 7, 21, 60];   // dias até a próxima revisão: sobe quando você lembra fácil
  const pad = n => String(n).padStart(2, "0");
  const dateOf = t => { const d = new Date(t); return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); };
  const today = now => dateOf(now == null ? Date.now() : now);
  const parse = ds => { const p = String(ds).split("-").map(Number); return new Date(p[0], p[1] - 1, p[2], 12); };
  const addDays = (ds, n) => { const d = parse(ds); d.setDate(d.getDate() + n); return dateOf(d.getTime()); };
  const between = (a, b) => Math.round((parse(b) - parse(a)) / DAY);   // dias de a até b (meio-dia evita o horário de verão)
  const fmt = ds => { const p = String(ds).split("-"); return p[2] + "/" + p[1]; };
  const read = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k) || "null"); return v && typeof v === "object" ? v : d; } catch (e) { return d; } };
  const readAll = () => read(KEY, {});
  const clampStep = s => Math.max(0, Math.min(STEPS.length - 1, s | 0));

  // Revisão marcada de uma aula: {due, step, src} ou null (fora da agenda)
  function stateOf(rec) {
    if (!rec || typeof rec !== "object") return null;
    if ("due" in rec) return rec.due ? { due: String(rec.due), step: clampStep(rec.step), src: rec.src === "manual" ? "manual" : "quiz" } : null;
    // formato antigo do quiz: revisões 1, 3, 7 e 21 dias depois de passar; "done" = última revisão feita
    const nx = Array.isArray(rec.next) ? rec.next.map(Number).filter(t => t > 0).sort((a, b) => a - b) : [];
    const i = nx.findIndex(t => t > (Number(rec.done) || 0));
    return i < 0 ? null : { due: dateOf(nx[i]), step: clampStep(i), src: "quiz" };
  }

  // Todas as revisões marcadas, da mais antiga para a mais nova: [{id, due, step, src, n, since?}]
  function agenda(now) {
    const recs = readAll(), prog = read(PKEY, {}), t = today(now), out = [];
    for (const id in recs) {
      const st = stateOf(recs[id]);
      if (st) out.push({ id, due: st.due, step: st.step, src: st.src, n: (Array.isArray(recs[id].hist) ? recs[id].hist.length : 0) + 1 });
    }
    // marca "↻ Revisar" do formato anterior (sem data): fica para hoje até você agendar, revisar ou tirar
    for (const id in prog) {
      const p = prog[id], r = recs[id];
      if (!p || !p.rv || (r && ("due" in r || stateOf(r)))) continue;
      out.push({ id, due: t, step: 0, src: "manual", n: 1, since: Number(p.rv) || null });
    }
    return out.sort((a, b) => (a.due < b.due ? -1 : a.due > b.due ? 1 : a.id < b.id ? -1 : 1));
  }

  function byId(now) { const m = {}; agenda(now).forEach(it => { m[it.id] = it; }); return m; }

  function counts(now) {
    const t = today(now), week = addDays(t, 7);
    let late = 0, hoje = 0, soon = 0, total = 0;
    agenda(now).forEach(it => { total++; if (it.due < t) late++; else if (it.due === t) hoje++; else if (it.due <= week) soon++; });
    return { late, hoje, due: late + hoje, soon, total };
  }

  // "hoje", "amanhã", "em 3 dias", "atrasada desde 25/11", "30/12"
  function when(due, now) {
    const n = between(today(now), due);
    if (n < 0) return n === -1 ? "atrasada desde ontem" : "atrasada desde " + fmt(due);
    return n === 0 ? "hoje" : n === 1 ? "amanhã" : n < 7 ? "em " + n + " dias" : fmt(due);
  }

  // Data da próxima revisão se você disser que foi fácil / com esforço / não lembrei (sem gravar)
  function preview(id, grade, now) {
    const rec = readAll()[id] || {}, st = stateOf(rec);
    let step = st ? st.step : clampStep(rec.step);
    step = grade === "f" ? step + 1 : grade === "z" ? 0 : step;
    return step >= STEPS.length ? null : addDays(today(now), STEPS[step]);   // null = aula dominada
  }

  function write(all) {
    try { localStorage.setItem(KEY, JSON.stringify(all)); } catch (e) {}
    if (typeof scheduleAwsRealtimeSync === "function") scheduleAwsRealtimeSync();
  }

  // A marca antiga sai do progresso quando a aula passa a ter agenda de verdade. Devolve se havia marca.
  function dropFlag(id) {
    const prog = read(PKEY, null);
    let had = false;
    if (prog && prog[id] && prog[id].rv) {
      had = true;
      delete prog[id].rv;
      try { localStorage.setItem(PKEY, JSON.stringify(prog)); } catch (e) {}
    }
    try { if (typeof PR !== "undefined" && PR && PR[id] && PR[id].rv) { had = true; delete PR[id].rv; } } catch (e) {}
    return had;
  }

  function changed(id) {
    try { if (typeof window !== "undefined" && window.dispatchEvent) window.dispatchEvent(new CustomEvent("rv:change", { detail: { id } })); } catch (e) {}
  }

  // Grava uma alteração (sempre com "last" novo) e devolve como era antes, para "desfazer":
  // {rec: registro anterior (ou null), flag: se a aula tinha a marca antiga "↻ Revisar"}
  function save(id, mutate, now) {
    now = now == null ? Date.now() : now;
    const all = readAll(), before = all[id] ? JSON.parse(JSON.stringify(all[id])) : null;
    const rec = Object.assign({}, all[id] || {}), st = stateOf(rec);
    if (!("due" in rec)) { rec.due = st ? st.due : null; rec.step = st ? st.step : 0; if (st) rec.src = st.src; }
    rec.next = [];   // formato antigo convertido: a agenda passa a valer só por "due"
    mutate(rec, st, today(now), now);
    rec.last = now;
    all[id] = rec;
    write(all);
    const flag = dropFlag(id);
    changed(id);
    return { rec: before, flag };
  }

  // Agenda (ou muda) a data da revisão. Uma aula nova na agenda conta como "marcada por você".
  const schedule = (id, due, now) => save(id, (r, st) => { r.due = String(due); if (!st) { r.src = "manual"; r.step = clampStep(r.step); } delete r.mastered; }, now);
  const remove = (id, now) => save(id, r => { r.due = null; }, now);

  // Desfaz uma alteração com o que save() devolveu: volta o registro de antes, com "last" novo
  // (senão a nuvem traria de volta a versão desfeita)
  function restore(id, token, now) {
    now = now == null ? Date.now() : now;
    const tk = token || {};
    if (tk.flag && !(tk.rec && stateOf(tk.rec))) return schedule(id, today(now), now);   // era a marca antiga: volta para hoje
    const all = readAll();
    all[id] = tk.rec ? Object.assign({}, tk.rec, { last: now }) : { due: null, step: 0, next: [], last: now };
    write(all);
    changed(id);
    return null;
  }

  // Revisão feita. Nota: "z" não lembrei (volta amanhã), "m" com esforço (mesmo intervalo), "f" fácil (intervalo maior).
  // Fácil no último intervalo (60 dias) = aula dominada: sai da agenda.
  function complete(id, grade, now) {
    return save(id, (r, st, t, ts) => {
      let step = st ? st.step : clampStep(r.step);
      step = grade === "f" ? step + 1 : grade === "z" ? 0 : step;
      r.hist = (Array.isArray(r.hist) ? r.hist : []).concat([[ts, grade]]).slice(-12);
      r.done = ts;
      if (step >= STEPS.length) { r.due = null; r.step = STEPS.length - 1; r.mastered = ts; }
      else { r.step = step; r.due = addDays(t, STEPS[step]); delete r.mastered; }
    }, now);
  }

  // Quiz da aula aprovado. 1ª aprovação: primeira revisão amanhã (se você ainda não tinha marcado uma data).
  // Refazer o quiz no dia da revisão (ou depois) conta como revisão feita: tudo certo = fácil, senão = com esforço.
  function quizPassed(id, score, total, now) {
    now = now == null ? Date.now() : now;
    const rec0 = readAll()[id] || {}, st0 = stateOf(rec0);
    if (rec0.passedAt && st0 && st0.due <= today(now)) complete(id, score >= total ? "f" : "m", now);
    save(id, (r, st, t) => {
      r.score = score; r.total = total;
      if (!r.passedAt) {
        r.passedAt = now;
        if (!st) { r.due = addDays(t, STEPS[0]); r.step = 0; r.src = "quiz"; }
      }
    }, now);
    return readAll()[id];
  }

  // Números da página Revisões: últimos 7 dias, dias seguidos revisando, aulas que mais custaram, dominadas
  function stats(now) {
    now = now == null ? Date.now() : now;
    const recs = readAll(), week = now - 7 * DAY, days = new Set(), hard = [];
    let feitas = 0, f = 0, m = 0, z = 0, dominadas = 0;
    for (const id in recs) {
      const r = recs[id] || {}, h = Array.isArray(r.hist) ? r.hist : [];
      if (r.mastered) dominadas++;
      let zz = 0;
      h.forEach(e => {
        const ts = Number(e && e[0]), g = e && e[1];
        if (!ts) return;
        days.add(today(ts));
        if (g === "z") zz++;
        if (ts >= week) { feitas++; if (g === "f") f++; else if (g === "m") m++; else if (g === "z") z++; }
      });
      if (zz) hard.push([id, zz]);
    }
    let streak = 0, d = today(now);
    if (!days.has(d)) d = addDays(d, -1);   // ainda não revisou hoje: a sequência de ontem continua valendo
    while (days.has(d)) { streak++; d = addDays(d, -1); }
    hard.sort((a, b) => b[1] - a[1] || (a[0] < b[0] ? -1 : 1));
    return { feitas, f, m, z, streak, dominadas, hard: hard.slice(0, 3) };
  }

  return { KEY, STEPS, today, addDays, between, fmt, when, stateOf, agenda, byId, counts, preview,
           schedule, remove, restore, complete, quizPassed, stats };
})();
if (typeof module !== "undefined") module.exports = RV;
"""

REVIEW_UI_CSS = r"""
/* ===== Agenda de revisões: menu "Quando revisar?", aviso e contador do menu ===== */
.nav-rv-badge{display:inline-grid;place-items:center;min-width:18px;height:18px;margin-left:6px;padding:0 5px;border-radius:9px;
  background:var(--t-hub);color:#04201d;font-size:.68rem;font-weight:800;line-height:1;vertical-align:1px}
.nav-rv-badge.late{background:#ef6b5b;color:#fff}
.nav-rv-badge[hidden]{display:none}
.rv-menu{position:fixed;z-index:100000;width:320px;max-width:calc(100vw - 20px);padding:12px;border-radius:14px;
  border:1px solid var(--bd);background:var(--card);color:var(--tx);box-shadow:0 24px 60px rgba(0,0,0,.45);font-size:.85rem}
.rv-menu h6{margin:0 0 2px;font-size:.9rem;font-weight:700}
.rv-menu .rv-sub{margin:0 0 10px;font-size:.76rem;color:var(--mu);line-height:1.4}
.rv-menu .rv-lbl{margin:10px 0 6px;font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--mu)}
.rv-menu .rv-grades{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.rv-menu .rv-grade{display:flex;flex-direction:column;align-items:center;gap:2px;padding:8px 4px;border-radius:12px;border:1px solid var(--bd);
  background:transparent;color:var(--tx);font:inherit;font-size:.76rem;cursor:pointer;line-height:1.25}
.rv-menu .rv-grade span{font-size:1.15rem}
.rv-menu .rv-grade small{color:var(--mu);font-size:.68rem}
.rv-menu .rv-grade:hover,.rv-menu .rv-chip:hover{border-color:var(--t-hub)}
.rv-menu .rv-chips{display:flex;flex-wrap:wrap;gap:6px}
.rv-menu .rv-chip{min-height:32px;padding:5px 11px;border-radius:99px;border:1px solid var(--bd);background:transparent;color:var(--tx);font:inherit;font-size:.78rem;cursor:pointer}
.rv-menu .rv-chip.on{border-color:var(--t-hub);color:var(--t-hub);font-weight:700}
.rv-menu input[type=date]{min-height:32px;padding:4px 8px;border-radius:99px;border:1px solid var(--bd);background:transparent;color:var(--tx);font:inherit;font-size:.78rem;color-scheme:dark light}
.rv-menu .rv-foot{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:10px;padding-top:8px;border-top:1px solid var(--bd);font-size:.72rem;color:var(--mu)}
.rv-menu .rv-off{border:0;background:none;color:#ef6b5b;font:inherit;font-size:.76rem;cursor:pointer;padding:4px 0}
@media (max-width:600px){.rv-menu{left:10px!important;right:10px;top:auto!important;bottom:10px;width:auto}}
.rv-toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);z-index:100001;display:flex;align-items:center;gap:12px;
  max-width:calc(100vw - 24px);padding:10px 16px;border-radius:12px;background:#0f1d27;color:#e8eef1;border:1px solid #2c4350;
  box-shadow:0 16px 40px rgba(0,0,0,.4);font-size:.85rem}
.rv-toast button{border:0;background:none;color:var(--t-hub,#5eead4);font:inherit;font-weight:700;cursor:pointer;padding:2px 4px}
"""

REVIEW_UI_JS = r"""
// =================== MENU "QUANDO REVISAR?" (aula, lista da trilha, hub e página Revisões) ===================
const RV_TRACKS = { ia: { nome: "IA & Código", pagina: "ia.html" }, mat: { nome: "Matemática", pagina: "matematica.html" },
                    ing: { nome: "Inglês", pagina: "ingles.html" } };
function rvTrackOf(id) { return String(id).startsWith("mat-") ? "mat" : String(id).startsWith("ing-") ? "ing" : "ia"; }
// Data para frases: "hoje", "amanhã", "30/11 (em 3 dias)", "04/12"
function rvDueText(ds) {
  const n = RV.between(RV.today(), ds);
  return n <= 1 ? RV.when(ds) : n < 7 ? RV.fmt(ds) + " (" + RV.when(ds) + ")" : RV.fmt(ds);
}
function rvEsc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }

let RV_MENU = null;
function closeReviewMenu() {
  if (!RV_MENU) return;
  RV_MENU.el.remove();
  document.removeEventListener("pointerdown", RV_MENU.out, true);
  document.removeEventListener("keydown", RV_MENU.key, true);
  RV_MENU = null;
}

function rvToast(msg, undo) {
  let t = document.getElementById("rv-toast");
  if (t) t.remove();
  t = document.createElement("div");
  t.id = "rv-toast"; t.className = "rv-toast"; t.setAttribute("role", "status");
  t.innerHTML = "<span>" + msg + "</span>" + (undo ? '<button type="button">Desfazer</button>' : "");
  if (undo) t.querySelector("button").onclick = () => { undo(); t.remove(); };
  document.body.appendChild(t);
  clearTimeout(rvToast.timer);
  rvToast.timer = setTimeout(() => t.remove(), undo ? 6000 : 3500);
}

// mode: "all" (datas + "já revisei") · "grade" (só "como foi?") · "date" (só datas)
function openReviewMenu(id, anchor, mode) {
  if (!id || typeof RV === "undefined") return;
  if (RV_MENU && RV_MENU.id === id && RV_MENU.anchor === anchor) { closeReviewMenu(); return; }
  closeReviewMenu();
  mode = mode || "all";
  const st = RV.byId()[id], t = RV.today();
  const el = document.createElement("div");
  el.className = "rv-menu"; el.setAttribute("role", "dialog"); el.setAttribute("aria-label", "Revisão da aula");
  const n0 = st ? RV.between(t, st.due) : 0;
  let h = st ? "<h6>Revisão " + rvEsc(n0 < 0 ? RV.when(st.due) : rvDueText(st.due)) + "</h6>"
             : "<h6>Quando revisar esta aula?</h6>";
  h += '<p class="rv-sub">' + (st ? (st.src === "quiz" ? "Agendada pelo quiz da aula" : "Agendada por você") + " · " + st.n + "ª revisão"
                                 : "Entra na página Revisões. A situação da aula e os pontos não mudam.") + "</p>";
  if (mode !== "date") {
    const nx = g => { const d = RV.preview(id, g); return d ? "próxima " + RV.when(d) : "aula dominada"; };
    h += '<div class="rv-lbl">' + (st ? "Já revisou? Como foi para lembrar" : "Revisei agora. Como foi") + "</div>" +
      '<div class="rv-grades">' +
      '<button type="button" class="rv-grade" data-g="z"><span>😵</span>Não lembrei<small>' + nx("z") + "</small></button>" +
      '<button type="button" class="rv-grade" data-g="m"><span>🙂</span>Com esforço<small>' + nx("m") + "</small></button>" +
      '<button type="button" class="rv-grade" data-g="f"><span>😌</span>Fácil<small>' + nx("f") + "</small></button></div>";
  }
  if (mode !== "grade") {
    const ch = [["Hoje", 0], ["Amanhã", 1], ["Em 3 dias", 3], ["Em 1 semana", 7]];
    h += '<div class="rv-lbl">' + (st ? "Mudar a data" : "Agendar para") + "</div><div class=\"rv-chips\">" +
      ch.map(([n, d]) => { const ds = RV.addDays(t, d); return '<button type="button" class="rv-chip' + (st && st.due === ds ? " on" : "") + '" data-d="' + ds + '">' + n + "</button>"; }).join("") +
      '<input type="date" aria-label="Escolher data" min="' + t + '" value="' + (st ? st.due : "") + '"></div>';
  }
  h += '<div class="rv-foot"><span>' + (st ? "" : "Dica: o quiz da aula também agenda sozinho.") + "</span>" +
       (st ? '<button type="button" class="rv-off">Tirar da agenda</button>' : "") + "</div>";
  el.innerHTML = h;
  document.body.appendChild(el);

  const done = (msg, undoFrom) => { closeReviewMenu(); rvToast(msg, undoFrom === undefined ? null : () => RV.restore(id, undoFrom)); };
  el.querySelectorAll(".rv-grade").forEach(b => b.onclick = () => {
    const g = b.dataset.g, before = RV.complete(id, g), it = RV.byId()[id];
    done(it ? "Revisão registrada. Próxima: " + rvDueText(it.due) + "." : "🏆 Aula dominada! Ela sai da agenda.", before);
  });
  el.querySelectorAll(".rv-chip").forEach(b => b.onclick = () => {
    const before = RV.schedule(id, b.dataset.d);
    done("Revisão marcada para " + rvDueText(b.dataset.d) + ".", before);
  });
  const inp = el.querySelector("input[type=date]");
  if (inp) inp.onchange = () => { if (!inp.value) return; const before = RV.schedule(id, inp.value); done("Revisão marcada para " + rvDueText(inp.value) + ".", before); };
  const off = el.querySelector(".rv-off");
  if (off) off.onclick = () => { const before = RV.remove(id); done("Aula tirada da agenda.", before); };

  // posição: embaixo do botão (ou em cima, se não couber); no celular o CSS vira uma folha no rodapé
  const r = anchor && anchor.getBoundingClientRect ? anchor.getBoundingClientRect() : { left: 20, right: 20, top: 80, bottom: 80 };
  const w = el.offsetWidth, hh = el.offsetHeight;
  let left = Math.min(Math.max(10, r.right - w), innerWidth - w - 10);
  let top = r.bottom + 8;
  if (top + hh > innerHeight - 10) top = Math.max(10, r.top - hh - 8);
  el.style.left = left + "px"; el.style.top = top + "px";

  const out = e => { if (!el.contains(e.target) && !(anchor && anchor.contains && anchor.contains(e.target))) closeReviewMenu(); };
  const key = e => { if (e.key === "Escape") { e.stopPropagation(); closeReviewMenu(); } };
  document.addEventListener("pointerdown", out, true);
  document.addEventListener("keydown", key, true);
  RV_MENU = { id, anchor, el, out, key };
  const first = el.querySelector("button,input"); if (first) first.focus({ preventScroll: true });
}

// Contador do item "Revisões" no menu: revisões de hoje + atrasadas (vermelho se houver atrasada)
function rvNavBadge() {
  const b = document.getElementById("nav-rv-badge");
  if (!b || typeof RV === "undefined") return;
  const c = RV.counts();
  b.textContent = c.due;
  b.hidden = !c.due;
  b.classList.toggle("late", c.late > 0);
  b.title = c.late ? c.late + " atrasada(s) e " + c.hoje + " para hoje" : c.hoje + " para hoje";
}
if (typeof window !== "undefined") window.addEventListener("rv:change", () => { try { rvNavBadge(); } catch (e) {} });
"""
