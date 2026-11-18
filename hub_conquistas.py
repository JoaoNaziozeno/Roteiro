# -*- coding: utf-8 -*-
"""
Painel "Suas conquistas" do Hub: mostra o que JÁ foi feito, para motivar.

Usa só dados reais do navegador (nada inventado):
  roteiro-ia-v1        progresso de cada tópico (s: "e" concluído, "r" em andamento)
  roteiro-events-v1    histórico de mudanças de status, com data
  roteiro-sessions-v1  sessões de estudo cronometradas (segundos)
  roteiro_portfolio_projects  projetos do portfólio
"""

import json

TRACKS = [
    ("ia", "IA & Código", "🤖", "ia.html", "--t-ia"),
    ("mat", "Matemática", "📐", "matematica.html", "--t-mat"),
    ("ing", "Inglês", "🇺🇸", "ingles.html", "--t-ing"),
]


def _title(raw):
    if isinstance(raw, dict):
        return raw.get("title", "")
    if isinstance(raw, str) and "||" in raw:
        return raw.split("||", 1)[0]
    return str(raw)


def build_index(tracks):
    """Índice compacto: tópicos {id: [título, módulo]} e módulos {módulo: [nome, total]}."""
    topics, modules = {}, {}
    for tr, phases in tracks.items():
        for p_idx, p in enumerate(phases):
            for g_idx, g in enumerate(p["g"]):
                mod = f"{tr}-{p_idx}-{g_idx}"
                items = g[1]
                modules[mod] = [str(g[0]), len(items)]
                for t_idx, raw in enumerate(items):
                    topics[f"{mod}-{t_idx}"] = [_title(raw), mod]
    data = {"topics": topics, "modules": modules}
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


CONQ_CSS = r"""
.cq-sect{background:var(--card);border:1px solid var(--bd);border-radius:22px;padding:24px 26px;margin-bottom:28px;box-shadow:0 14px 40px rgba(6,20,27,.4)}
.cq-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:12px;margin-bottom:18px}
.cq-title{font-size:1.25rem;font-weight:850;color:var(--tx);margin:0}
.cq-lead{font-size:.92rem;color:var(--mu);margin:6px 0 0;line-height:1.5;max-width:720px}
.cq-lead b{color:var(--tx)}
.cq-stats{display:flex;gap:10px;flex-wrap:wrap}
.cq-stat{background:var(--bg);border:1px solid var(--bd);border-radius:14px;padding:10px 14px;min-width:110px}
.cq-stat b{display:block;font-size:1.45rem;font-weight:850;color:var(--tx);line-height:1.1}
.cq-stat span{font-size:.72rem;font-weight:700;color:var(--mu);text-transform:uppercase;letter-spacing:.04em}
.cq-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-bottom:16px}
@media(max-width:1100px){.cq-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:560px){.cq-grid{grid-template-columns:1fr}.cq-sect{padding:18px 14px}.cq-stats{display:grid;grid-template-columns:1fr 1fr;width:100%}.cq-stat{min-width:0}}
.cq-card{background:var(--bg);border:1px solid var(--bd);border-radius:16px;padding:16px;display:flex;flex-direction:column;gap:10px;text-decoration:none;color:inherit;transition:border-color .2s,transform .2s}
.cq-card:hover{border-color:color-mix(in srgb,var(--c) 55%,transparent);transform:translateY(-2px)}
.cq-card-top{display:flex;align-items:center;gap:14px}
.cq-ring{width:86px;height:86px;flex:none}
.cq-ring .bg{stroke:var(--bd)}
.cq-ring .fg{stroke:var(--c);transition:stroke-dashoffset 1s cubic-bezier(.2,.8,.2,1)}
.cq-ring text{fill:var(--tx);font-weight:850;font-size:19px}
.cq-name{font-weight:800;color:var(--tx);font-size:.98rem}
.cq-count{font-size:.8rem;color:var(--mu);margin-top:2px;line-height:1.4}
.cq-count b{color:var(--c)}
.cq-line{font-size:.78rem;color:var(--mu);line-height:1.45}
.cq-line b{color:var(--tx);font-weight:700}
.cq-est{font-size:.76rem;font-weight:700;color:var(--tx);background:color-mix(in srgb,var(--c) 12%,transparent);border:1px solid color-mix(in srgb,var(--c) 30%,transparent);border-radius:10px;padding:7px 10px;line-height:1.4}
.cq-row2{display:grid;grid-template-columns:1.25fr 1fr;gap:14px}
@media(max-width:980px){.cq-row2{grid-template-columns:1fr}}
.cq-box{background:var(--bg);border:1px solid var(--bd);border-radius:16px;padding:16px}
.cq-h{font-size:.74rem;font-weight:800;text-transform:uppercase;letter-spacing:.05em;color:var(--mu);margin:0 0 12px;display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap}
.cq-heat{display:grid;grid-template-rows:repeat(7,auto);grid-auto-flow:column;grid-auto-columns:minmax(10px,20px);gap:4px;justify-content:start}
.cq-heat i{display:block;aspect-ratio:1;border-radius:4px;background:var(--bd);opacity:.55}
.cq-heat i.l1{background:var(--t-hub);opacity:.35}.cq-heat i.l2{background:var(--t-hub);opacity:.6}
.cq-heat i.l3{background:var(--t-hub);opacity:.85}.cq-heat i.l4{background:var(--t-hub);opacity:1}
.cq-heat i.today{outline:2px solid var(--tx);outline-offset:1px}
.cq-heat i.future{visibility:hidden}
.cq-legend{display:flex;align-items:center;gap:4px;font-size:.7rem;color:var(--mu);margin-top:8px;justify-content:flex-end}
.cq-legend i{width:11px;height:11px;border-radius:3px;display:inline-block;background:var(--t-hub)}
.cq-badges{display:flex;flex-wrap:wrap;gap:8px}
.cq-badge{display:inline-flex;align-items:center;gap:6px;font-size:.76rem;font-weight:700;padding:6px 10px;border-radius:99px;border:1px solid var(--bd);background:var(--card);color:var(--tx)}
.cq-badge.new{border-color:var(--t-hub);box-shadow:0 0 0 3px color-mix(in srgb,var(--t-hub) 18%,transparent)}
.cq-next{margin-top:12px;font-size:.8rem;color:var(--mu);line-height:1.5}
.cq-next b{color:var(--tx)}
.cq-nextbar{height:7px;background:var(--bd);border-radius:99px;overflow:hidden;margin-top:6px}
.cq-nextbar i{display:block;height:100%;background:var(--t-hub);border-radius:99px}
@media (prefers-reduced-motion:reduce){.cq-ring .fg{transition:none}.cq-card:hover{transform:none}}
"""

CONQ_HTML = r"""<section class="cq-sect" id="hub-conquistas" aria-labelledby="cq-title">
    <div class="cq-head">
      <div>
        <h2 class="cq-title" id="cq-title">🏆 Suas conquistas</h2>
        <p class="cq-lead" id="cq-lead">Carregando o que você já fez…</p>
      </div>
      <div class="cq-stats" id="cq-stats"></div>
    </div>
    <div class="cq-grid" id="cq-cards"></div>
    <div class="cq-row2">
      <div class="cq-box">
        <div class="cq-h"><span>📅 Seus dias de estudo (últimas 12 semanas)</span><span id="cq-streak"></span></div>
        <div class="cq-heat" id="cq-heat" role="img" aria-label="Calendário dos dias com estudo"></div>
        <div class="cq-legend">menos <i style="opacity:.35"></i><i style="opacity:.6"></i><i style="opacity:.85"></i><i></i> mais</div>
      </div>
      <div class="cq-box">
        <div class="cq-h"><span>🎖️ Selos conquistados</span><span id="cq-badge-count"></span></div>
        <div class="cq-badges" id="cq-badges"></div>
        <div class="cq-next" id="cq-next"></div>
      </div>
    </div>
  </section>"""

CONQ_JS = r"""
// =================== SUAS CONQUISTAS (só dados reais deste navegador/da nuvem) ===================
const CQ_INDEX = __CONQ_INDEX__;
const CQ_TRACKS = __CONQ_TRACKS__;
const CQ_DAY = 86400000;

function cqRead(k, d) { try { const r = localStorage.getItem(k); return r ? JSON.parse(r) : d; } catch (e) { return d; } }
function cqEsc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
function cqDayKey(t) { const d = new Date(t); return d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate(); }
function cqNum(n) { return Math.round(n).toLocaleString("pt-BR"); }
function cqHours(sec) { const h = sec / 3600; return h < 1 ? Math.round(sec / 60) + " min" : (Math.round(h * 10) / 10).toLocaleString("pt-BR") + " h"; }
function cqDate(t) { const d = new Date(t); return String(d.getDate()).padStart(2, "0") + "/" + String(d.getMonth() + 1).padStart(2, "0"); }

function cqRing(pct, label) {
  const r = 36, c = 2 * Math.PI * r, off = c * (1 - Math.max(0, Math.min(100, pct)) / 100);
  return '<svg class="cq-ring" viewBox="0 0 86 86" aria-hidden="true"><circle class="bg" cx="43" cy="43" r="' + r + '" fill="none" stroke-width="8"/>' +
    '<circle class="fg" cx="43" cy="43" r="' + r + '" fill="none" stroke-width="8" stroke-linecap="round" transform="rotate(-90 43 43)" ' +
    'stroke-dasharray="' + c.toFixed(2) + '" stroke-dashoffset="' + off.toFixed(2) + '"/>' +
    '<text x="43" y="49" text-anchor="middle">' + label + "</text></svg>";
}

function renderConquistas() {
  const root = document.getElementById("hub-conquistas");
  if (!root) return;
  const now = Date.now();
  const prog = (typeof PR !== "undefined" && PR) ? PR : cqRead("roteiro-ia-v1", {});
  const events = cqRead("roteiro-events-v1", []);
  const sessions = cqRead("roteiro-sessions-v1", []);
  const projects = cqRead("roteiro_portfolio_projects", []);
  const topics = CQ_INDEX.topics, modules = CQ_INDEX.modules;

  // Situação atual de cada tópico conhecido
  const done = {}, started = {};
  for (const id in topics) {
    const s = prog[id] && prog[id].s;
    if (s === "e") done[id] = true; else if (s === "r") started[id] = true;
  }
  // Data em que cada tópico foi concluído (último evento "-> e" de um tópico que continua concluído)
  const doneAt = {};
  events.forEach(e => { if (e && e.to === "e" && done[e.id] && (!doneAt[e.id] || e.t > doneAt[e.id])) doneAt[e.id] = e.t; });

  // Dias com estudo: sessões cronometradas + conclusões/avanços
  const dayMin = {};
  sessions.forEach(s => { if (s && s.t) dayMin[cqDayKey(s.t)] = (dayMin[cqDayKey(s.t)] || 0) + (s.sec || 0) / 60; });
  events.forEach(e => { if (e && e.t && (e.to === "e" || e.to === "r")) { const k = cqDayKey(e.t); dayMin[k] = (dayMin[k] || 0) + (e.to === "e" ? 15 : 5); } });
  const studied = k => (dayMin[k] || 0) > 0;
  let streak = 0;
  for (let d = 0; d < 400; d++) {
    const k = cqDayKey(now - d * CQ_DAY);
    if (studied(k)) streak++; else if (d === 0) continue; else break;
  }
  let best = 0, run = 0;
  const keys = Object.keys(dayMin).filter(studied).map(k => { const [y, m, d] = k.split("-").map(Number); return new Date(y, m - 1, d).getTime(); }).sort((a, b) => a - b);
  keys.forEach((t, i) => { run = i && Math.round((t - keys[i - 1]) / CQ_DAY) === 1 ? run + 1 : 1; best = Math.max(best, run); });
  const daysStudied = keys.length;
  const totalSec = sessions.reduce((a, s) => a + ((s && s.sec) || 0), 0);
  const totalDone = Object.keys(done).length;
  const last30 = Object.values(doneAt).filter(t => t >= now - 30 * CQ_DAY).length;

  // Módulos completos
  const modDone = {};
  for (const id in done) { const m = topics[id][1]; modDone[m] = (modDone[m] || 0) + 1; }
  const fullMods = Object.keys(modDone).filter(m => modDone[m] >= modules[m][1]);

  // Cabeçalho
  const projDone = projects.filter(p => p && p.status === "done").length;
  let lead;
  if (!totalDone && !daysStudied) lead = "Aqui vão aparecer os tópicos que você concluir, os dias em que estudou e os selos que conquistar. Conclua sua primeira aula e veja este painel ganhar vida.";
  else {
    lead = "Você já concluiu <b>" + cqNum(totalDone) + " tópico" + (totalDone === 1 ? "" : "s") + "</b>";
    if (fullMods.length) lead += " e fechou <b>" + fullMods.length + " módulo" + (fullMods.length === 1 ? "" : "s") + " inteiro" + (fullMods.length === 1 ? "" : "s") + "</b>";
    lead += ". ";
    if (streak >= 2) lead += "🔥 São <b>" + streak + " dias seguidos</b> de estudo. Não deixe a sequência quebrar hoje!";
    else if (last30) lead += "Só nos últimos 30 dias foram <b>" + last30 + "</b>. Cada aula concluída é um passo que ninguém tira de você.";
    else lead += "Cada aula concluída é um passo que ninguém tira de você.";
  }
  document.getElementById("cq-lead").innerHTML = lead;
  const stats = [[cqNum(totalDone), "tópicos concluídos"], [daysStudied, "dias de estudo"], [totalSec ? cqHours(totalSec) : "–", "estudadas"], [best ? best + (best === 1 ? " dia" : " dias") : "–", "maior sequência"]];
  document.getElementById("cq-stats").innerHTML = stats.map(s => '<div class="cq-stat"><b>' + s[0] + "</b><span>" + s[1] + "</span></div>").join("");

  // Cartões por disciplina
  const cards = CQ_TRACKS.map(([tr, name, icon, href, color]) => {
    const ids = Object.keys(topics).filter(id => id.startsWith(tr + "-"));
    const total = ids.length, d = ids.filter(id => done[id]).length, r = ids.filter(id => started[id]).length;
    const pct = total ? d / total * 100 : 0;
    const mods = Object.keys(modules).filter(m => m.startsWith(tr + "-"));
    const fm = mods.filter(m => (modDone[m] || 0) >= modules[m][1]).length;
    const lastId = ids.filter(id => doneAt[id]).sort((a, b) => doneAt[b] - doneAt[a])[0];
    // Meta próxima: o módulo mais perto de terminar (a previsão do roteiro inteiro fica na Jornada)
    const recent = ids.filter(id => doneAt[id] && doneAt[id] >= now - 28 * CQ_DAY).length;
    const open = mods.filter(m => (modDone[m] || 0) < modules[m][1])
      .sort((a, b) => ((modDone[b] || 0) / modules[b][1]) - ((modDone[a] || 0) / modules[a][1]) || (a < b ? -1 : 1));
    let est;
    if (d >= total) est = "🎓 Disciplina concluída. Que orgulho!";
    else if (open.length) {
      const m = open[0], left = modules[m][1] - (modDone[m] || 0);
      est = "🎯 Próximo módulo: <b>" + cqEsc(modules[m][0]) + "</b> · falta" + (left > 1 ? "m " + left + " tópicos" : " 1 tópico");
      if (recent > 0) {
        const days = Math.max(1, Math.ceil(left / (recent / 28)));
        est += ". No seu ritmo, você fecha em ~" + days + (days === 1 ? " dia." : " dias.");
      } else est += ".";
    }
    const pctLabel = (pct > 0 && pct < 1 ? "<1" : Math.round(pct)) + "%";
    return '<a class="cq-card" href="' + href + '" style="--c:var(' + color + ')">' +
      '<div class="cq-card-top">' + cqRing(pct, pctLabel) + '<div><div class="cq-name">' + icon + " " + name + "</div>" +
      '<div class="cq-count"><b>' + d + "</b> de " + total + " concluídos" + (r ? " · " + r + " em andamento" : "") + "</div></div></div>" +
      '<div class="cq-line">Módulos completos: <b>' + fm + " de " + mods.length + "</b></div>" +
      (lastId ? '<div class="cq-line">Última conquista: <b>' + cqEsc(topics[lastId][0]) + "</b> (" + cqDate(doneAt[lastId]) + ")</div>" : "") +
      '<div class="cq-est">' + est + "</div></a>";
  });
  const pPct = projects.length ? projDone / projects.length * 100 : 0;
  cards.push('<a class="cq-card" href="projetos.html" style="--c:var(--t-proj)"><div class="cq-card-top">' + cqRing(pPct, Math.round(pPct) + "%") +
    '<div><div class="cq-name">🛠️ Projetos</div><div class="cq-count"><b>' + projDone + "</b> de " + (projects.length || 6) + " concluídos" +
    (projects.filter(p => p && p.status === "wip").length ? " · " + projects.filter(p => p && p.status === "wip").length + " em desenvolvimento" : "") + "</div></div></div>" +
    '<div class="cq-line">Projetos são o que mais pesa num currículo de IA: cada um vira uma prova do que você sabe fazer.</div></a>');
  document.getElementById("cq-cards").innerHTML = cards.join("");

  // Calendário (12 semanas, colunas = semanas, linhas = dom..sáb)
  const today = new Date(now); today.setHours(0, 0, 0, 0);
  const startDay = new Date(today.getTime() - (7 * 11 + today.getDay()) * CQ_DAY);
  let cells = "";
  for (let i = 0; i < 84; i++) {
    const t = startDay.getTime() + i * CQ_DAY, k = cqDayKey(t), m = dayMin[k] || 0;
    const lvl = m <= 0 ? 0 : m < 15 ? 1 : m < 40 ? 2 : m < 90 ? 3 : 4;
    const fut = t > today.getTime();
    cells += '<i class="' + (lvl ? "l" + lvl : "") + (t === today.getTime() ? " today" : "") + (fut ? " future" : "") + '" title="' +
      new Date(t).toLocaleDateString("pt-BR", { weekday: "short", day: "2-digit", month: "2-digit" }) + (m ? " · estudou" : " · sem registro") + '"></i>';
  }
  document.getElementById("cq-heat").innerHTML = cells;
  document.getElementById("cq-streak").textContent = streak ? "🔥 " + streak + (streak === 1 ? " dia seguido" : " dias seguidos") : (daysStudied ? "estude hoje para começar uma sequência" : "");

  // Selos
  const tracksThisWeek = new Set(Object.keys(doneAt).filter(id => doneAt[id] >= now - 7 * CQ_DAY).map(id => id.split("-")[0]));
  const tiers = [
    ["📘", "tópico", "tópicos", totalDone, [1, 5, 10, 25, 50, 100, 150, 200, 289]],
    ["⏱️", "hora estudada", "horas estudadas", totalSec / 3600, [1, 5, 10, 25, 50, 100]],
    ["🔥", "dia seguido", "dias seguidos", best, [3, 7, 14, 30, 60]],
    ["🧩", "módulo completo", "módulos completos", fullMods.length, [1, 3, 5, 10, 20]],
  ];
  const earned = [], upcoming = [];
  tiers.forEach(([ic, one, many, val, steps]) => {
    steps.forEach(s => { if (val >= s) earned.push({ ic, label: s + " " + (s === 1 ? one : many) }); });
    const nx = steps.find(s => val < s);
    if (nx) upcoming.push({ ic, label: nx + " " + (nx === 1 ? one : many), val, nx, frac: val / nx });
  });
  if (tracksThisWeek.size >= 3) earned.push({ ic: "🎯", label: "As 3 disciplinas na mesma semana" });
  document.getElementById("cq-badge-count").textContent = earned.length ? earned.length + " no total" : "";
  document.getElementById("cq-badges").innerHTML = earned.length
    ? earned.map(b => '<span class="cq-badge">' + b.ic + " " + cqEsc(b.label) + "</span>").join("")
    : '<span class="cq-line">Seu primeiro selo chega ao concluir o primeiro tópico.</span>';
  const next = upcoming.sort((a, b) => b.frac - a.frac)[0];
  if (next) {
    const falta = next.nx - next.val;
    const faltaTxt = next.ic === "⏱️" ? cqHours(falta * 3600) : Math.ceil(falta);
    document.getElementById("cq-next").innerHTML = "Próximo selo: <b>" + next.ic + " " + cqEsc(next.label) + "</b> · falta" + (falta > 1 ? "m " : " ") + faltaTxt +
      '<div class="cq-nextbar"><i style="width:' + Math.round(next.frac * 100) + '%"></i></div>';
  } else document.getElementById("cq-next").textContent = "Você conquistou todos os selos. Lenda!";
}
"""
