# -*- coding: utf-8 -*-
"""
Página "Revisões" (revisoes.html): a agenda única de revisões.

Junta as revisões que o quiz de cada aula agenda e as que você marca com "↻ Revisar" (agenda em
review_js.RV). Mostra atrasadas, hoje, próximos 7 dias e mais adiante, um calendário de 14 dias,
"Revisei" (como foi? e o site agenda a próxima), mudar data, tirar, agendar qualquer aula pela busca
e os números da semana. A situação das aulas e os pontos da Jornada não mudam aqui.
"""
import json

from favicon import FAVICON_LINK
from auth_aws_sync import AUTH_GUARD_HEAD_SCRIPT, AUTH_AWS_SYNC_CSS, CHANGE_CREDENTIALS_MODAL_HTML, AUTH_AWS_SYNC_JS

REVIEW_PAGE_CSS = r"""
.rvp-main{max-width:1200px;margin:0 auto;padding:28px 22px 100px}
.rvp-head{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:14px;margin-bottom:16px}
.rvp-head h1{margin:0;font-size:1.9rem;font-weight:800;letter-spacing:-.02em}
.rvp-head p{margin:6px 0 0;color:var(--mu);font-size:.95rem;max-width:640px;line-height:1.5}
.rvp-btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:36px;padding:6px 14px;border-radius:99px;
  border:1px solid var(--bd);background:transparent;color:var(--tx);font:inherit;font-size:.82rem;font-weight:600;text-decoration:none;cursor:pointer;white-space:nowrap}
.rvp-btn:hover{border-color:var(--t-hub)}
.rvp-btn.pri{background:var(--t-hub);border-color:var(--t-hub);color:#04201d}
.rvp-today{display:flex;align-items:center;gap:16px;padding:16px 18px;margin-bottom:14px;border-radius:16px;
  border:1px solid color-mix(in srgb,var(--t-hub) 30%,var(--bd));background:linear-gradient(135deg,color-mix(in srgb,var(--t-hub) 12%,var(--card)),var(--card))}
.rvp-today[hidden]{display:none}
.rvp-today .ico{font-size:2rem;line-height:1}
.rvp-today div>b{display:block;font-size:1.15rem}
.rvp-today div>span{display:block;margin-top:3px;font-size:.85rem;color:var(--mu);line-height:1.45}
.rvp-today div>span b{color:var(--tx)}
.rvp-search{margin-bottom:14px;padding:14px;border:1px solid var(--bd);border-radius:14px;background:var(--card)}
.rvp-search[hidden]{display:none}
.rvp-search input{width:100%;min-height:40px;padding:8px 14px;border-radius:10px;border:1px solid var(--bd);background:var(--bg);color:var(--tx);font:inherit;font-size:.9rem}
.rvp-res{list-style:none;margin:8px 0 0;padding:0}
.rvp-res li button{width:100%;display:flex;align-items:center;gap:10px;padding:8px 10px;border:0;border-radius:10px;background:transparent;color:var(--tx);font:inherit;font-size:.86rem;text-align:left;cursor:pointer}
.rvp-res li button:hover{background:var(--bg)}
.rvp-res small{margin-left:auto;color:var(--mu);font-size:.74rem;white-space:nowrap}
.rvp-cal{display:grid;grid-template-columns:repeat(14,minmax(52px,1fr));gap:6px;margin-bottom:16px;overflow-x:auto;scrollbar-width:none}
.rvp-cal::-webkit-scrollbar{display:none}
.rvp-day{display:flex;flex-direction:column;align-items:center;gap:2px;padding:7px 2px;border-radius:10px;border:1px solid var(--bd);
  background:var(--card);color:var(--mu);font:inherit;font-size:.7rem;cursor:pointer}
.rvp-day b{font-size:.98rem;color:var(--tx)}
.rvp-day.hj{border-color:var(--t-hub)}
.rvp-day.hj b{color:var(--t-hub)}
.rvp-day.sel{background:color-mix(in srgb,var(--t-hub) 16%,var(--card));border-color:var(--t-hub)}
.rvp-dots{display:flex;gap:3px;min-height:7px;align-items:center;font-size:.62rem}
.rvp-dots i{width:6px;height:6px;border-radius:50%;background:var(--c)}
.rvp-dots i.late{background:#ef6b5b}
.rvp-grid{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:18px;align-items:start}
@media (max-width:980px){.rvp-grid{grid-template-columns:minmax(0,1fr)}}
.rvp-sec{margin-bottom:12px;border:1px solid var(--bd);border-radius:14px;background:var(--card);overflow:hidden}
.rvp-sec h2{display:flex;justify-content:space-between;margin:0;padding:10px 14px;border-bottom:1px solid var(--bd);
  font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--mu)}
.rvp-sec.late h2{color:#ef6b5b}
.rvp-sec.now h2{color:var(--t-hub)}
.rvp-sec ul{list-style:none;margin:0;padding:0}
.rvp-item{display:flex;align-items:center;gap:12px;padding:10px 14px;border-top:1px solid var(--bd)}
.rvp-item:first-child{border-top:0}
.rvp-dot{flex:none;width:9px;height:9px;border-radius:50%;background:var(--c)}
.rvp-t{flex:1;min-width:0}
.rvp-t a{color:var(--tx);text-decoration:none;font-size:.92rem;font-weight:600;line-height:1.3}
.rvp-t a:hover{text-decoration:underline}
.rvp-t small{display:block;margin-top:2px;font-size:.76rem;color:var(--mu)}
.rvp-acts{display:flex;gap:6px;flex:none}
@media (max-width:640px){.rvp-item{flex-wrap:wrap}.rvp-acts{width:100%;padding-left:21px}.rvp-acts .rvp-btn{flex:1}}
.rvp-empty{padding:26px 22px;border:1px dashed var(--bd);border-radius:14px;color:var(--mu);font-size:.92rem;line-height:1.6;text-align:center}
.rvp-empty b{color:var(--tx)}
.rvp-filter{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:0 0 10px;font-size:.85rem;color:var(--mu)}
.rvp-box{margin-bottom:12px;padding:14px;border:1px solid var(--bd);border-radius:14px;background:var(--card)}
.rvp-box h3{margin:0 0 8px;font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--mu)}
.rvp-kv{display:flex;justify-content:space-between;gap:10px;padding:4px 0;font-size:.86rem}
.rvp-kv b{font-variant-numeric:tabular-nums}
.rvp-kv a{color:var(--tx);text-decoration:none}
.rvp-kv a:hover{text-decoration:underline}
.rvp-rule{display:flex;gap:10px;padding:5px 0;font-size:.84rem;line-height:1.45}
.rvp-rule span:first-child{flex:none;width:20px;text-align:center}
.rvp-muted{color:var(--mu)}
"""

REVIEW_PAGE_JS = r"""
// =================== PÁGINA REVISÕES ===================
const RV_TOPICS = __RV_TOPICS__;   // {id: [trilha, título]}
const RV_TRK = { ia: { nome: "IA & Código", pagina: "ia.html", cor: "--t-ia" },
                 mat: { nome: "Matemática", pagina: "matematica.html", cor: "--t-mat" },
                 ing: { nome: "Inglês", pagina: "ingles.html", cor: "--t-ing" } };
const RV_WD = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
let RV_DIA = null;   // dia escolhido no calendário (filtro)

function rvpTrack(id) { const tp = RV_TOPICS[id]; return RV_TRK[tp ? tp[0] : "ia"] || RV_TRK.ia; }
function rvpLink(id) { return rvpTrack(id).pagina + "?aula=" + encodeURIComponent(id); }
function rvpWeekday(ds) { const p = ds.split("-").map(Number); return RV_WD[new Date(p[0], p[1] - 1, p[2], 12).getDay()]; }

function rvpItem(it) {
  const tp = RV_TOPICS[it.id], t = rvpTrack(it.id);
  const meta = [t.nome, RV.when(it.due), it.src === "quiz" ? "agendada pelo quiz" : "agendada por você", it.n + "ª revisão"];
  return '<li class="rvp-item" style="--c:var(' + t.cor + ')"><i class="rvp-dot" aria-hidden="true"></i>' +
    '<div class="rvp-t"><a href="' + rvpLink(it.id) + '">' + rvEsc(tp[1]) + "</a><small>" + meta.map(rvEsc).join(" · ") + "</small></div>" +
    '<div class="rvp-acts"><a class="rvp-btn" href="' + rvpLink(it.id) + '">Abrir aula</a>' +
    '<button type="button" class="rvp-btn pri" onclick="openReviewMenu(\'' + it.id + '\', this, \'grade\')">Revisei</button>' +
    '<button type="button" class="rvp-btn" aria-label="Mudar a data ou tirar da agenda" title="Mudar a data ou tirar da agenda" ' +
    'onclick="openReviewMenu(\'' + it.id + '\', this, \'date\')">⋯</button></div></li>';
}

function rvpSection(titulo, itens, cls) {
  if (!itens.length) return "";
  return '<section class="rvp-sec ' + (cls || "") + '"><h2><span>' + titulo + "</span><span>" + itens.length + "</span></h2><ul>" +
    itens.map(rvpItem).join("") + "</ul></section>";
}

function renderRevisoes() {
  const hoje = RV.today(), semana = RV.addDays(hoje, 7);
  const ag = RV.agenda().filter(it => RV_TOPICS[it.id]);
  const atrasadas = ag.filter(it => it.due < hoje), deHoje = ag.filter(it => it.due === hoje);

  // Resumo de hoje
  const box = document.getElementById("rv-hoje"), n = atrasadas.length + deHoje.length, prox = ag.find(it => it.due > hoje);
  box.hidden = !ag.length;
  if (n) {
    box.innerHTML = '<span class="ico" aria-hidden="true">🧠</span><div><b>Hoje: ' + n + (n === 1 ? " revisão" : " revisões") +
      (atrasadas.length ? " · " + atrasadas.length + (atrasadas.length === 1 ? " atrasada" : " atrasadas") : "") + "</b>" +
      "<span>Abra a aula, refaça o quiz e um exercício de cabeça, e toque em <b>Revisei</b> para dizer como foi. O site agenda a próxima.</span></div>";
  } else if (prox) {
    box.innerHTML = '<span class="ico" aria-hidden="true">🎉</span><div><b>Nada para revisar hoje</b><span>Próxima: ' +
      rvEsc(RV_TOPICS[prox.id][1]) + " · " + RV.when(prox.due) + ".</span></div>";
  }

  // Calendário: 14 dias a partir de hoje (hoje inclui as atrasadas, em vermelho)
  let cal = "";
  for (let i = 0; i < 14; i++) {
    const d = RV.addDays(hoje, i), doDia = ag.filter(it => it.due === d), late = i === 0 ? atrasadas : [];
    const dots = late.map(() => '<i class="late"></i>').concat(doDia.map(it => '<i style="--c:var(' + rvpTrack(it.id).cor + ')"></i>'));
    const tot = dots.length;
    cal += '<button type="button" class="rvp-day' + (i === 0 ? " hj" : "") + (RV_DIA === d ? " sel" : "") + '" data-d="' + d + '" ' +
      'aria-pressed="' + (RV_DIA === d) + '" title="' + (tot ? tot + (tot === 1 ? " revisão" : " revisões") : "Sem revisões") + '">' +
      (i === 0 ? "Hoje" : rvpWeekday(d)) + "<b>" + Number(d.slice(8)) + '</b><span class="rvp-dots">' + dots.slice(0, 5).join("") +
      (tot > 5 ? "+" + (tot - 5) : "") + "</span></button>";
  }
  const calEl = document.getElementById("rv-cal");
  calEl.innerHTML = cal;
  calEl.querySelectorAll(".rvp-day").forEach(b => b.onclick = () => { RV_DIA = RV_DIA === b.dataset.d ? null : b.dataset.d; renderRevisoes(); });

  // Lista
  const lista = document.getElementById("rv-lista");
  if (!ag.length) {
    lista.innerHTML = '<div class="rvp-empty"><b>Nenhuma revisão agendada ainda.</b><br>Quando você passa no quiz de uma aula, a primeira revisão entra aqui sozinha. ' +
      "Você também pode agendar qualquer aula pelo <b>📅 Agendar revisão</b>, aqui em cima, ou pelo <b>↻ Revisar</b> de cada aula.</div>";
  } else if (RV_DIA) {
    const doDia = ag.filter(it => it.due === RV_DIA || (RV_DIA === hoje && it.due < hoje));
    lista.innerHTML = '<div class="rvp-filter"><span>Mostrando ' + (RV_DIA === hoje ? "hoje" : rvpWeekday(RV_DIA).toLowerCase() + ", " + RV.fmt(RV_DIA)) + "</span>" +
      '<button type="button" class="rvp-btn" onclick="RV_DIA = null; renderRevisoes()">Ver tudo</button></div>' +
      (rvpSection(RV_DIA === hoje ? "Hoje" : "Dia " + RV.fmt(RV_DIA), doDia, RV_DIA === hoje ? "now" : "") ||
       '<div class="rvp-empty">Nenhuma revisão neste dia.</div>');
  } else {
    lista.innerHTML = rvpSection("Atrasadas", atrasadas, "late") + rvpSection("Hoje", deHoje, "now") +
      rvpSection("Próximos 7 dias", ag.filter(it => it.due > hoje && it.due <= semana)) +
      rvpSection("Mais adiante", ag.filter(it => it.due > semana));
  }

  // Lateral: números da semana
  const s = RV.stats();
  document.getElementById("rv-semana").innerHTML = "<h3>Sua semana de revisões</h3>" +
    [["Revisões feitas (7 dias)", s.feitas], ["😌 Lembrou fácil", s.f], ["🙂 Com esforço", s.m], ["😵 Não lembrou", s.z],
     ["🔥 Dias seguidos revisando", s.streak], ["🏆 Aulas dominadas", s.dominadas]]
      .map(([k, v]) => '<div class="rvp-kv"><span>' + k + "</span><b>" + v + "</b></div>").join("");
  const dif = s.hard.filter(h => RV_TOPICS[h[0]]);
  const custo = document.getElementById("rv-custo");
  custo.hidden = !dif.length;
  custo.innerHTML = "<h3>Aulas que mais custaram</h3>" + dif.map(([id, z]) =>
    '<div class="rvp-kv"><a href="' + rvpLink(id) + '">' + rvEsc(RV_TOPICS[id][1]) + '</a><span class="rvp-muted">' + z + (z === 1 ? " vez" : " vezes") + "</span></div>").join("");
}

// Agendar qualquer aula pela busca
function rvpToggleSearch() {
  const p = document.getElementById("rv-busca");
  p.hidden = !p.hidden;
  if (!p.hidden) { const i = p.querySelector("input"); i.value = ""; rvpSearch(""); i.focus(); }
}
function rvpSearch(q) {
  const norm = s => String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  const nq = norm(q).trim(), out = document.getElementById("rv-busca-res");
  if (!nq) { out.innerHTML = '<li class="rvp-muted" style="padding:8px 10px;font-size:.82rem">Digite parte do nome da aula.</li>'; return; }
  const hits = Object.keys(RV_TOPICS).filter(id => norm(RV_TOPICS[id][1]).includes(nq)).slice(0, 8);
  out.innerHTML = hits.length ? hits.map(id => '<li><button type="button" onclick="openReviewMenu(\'' + id + '\', this, \'date\')">' +
    '<i class="rvp-dot" style="--c:var(' + rvpTrack(id).cor + ')" aria-hidden="true"></i>' + rvEsc(RV_TOPICS[id][1]) +
    "<small>" + rvpTrack(id).nome + "</small></button></li>").join("")
    : '<li class="rvp-muted" style="padding:8px 10px;font-size:.82rem">Nenhuma aula com esse nome.</li>';
}

window.addEventListener("rv:change", () => { try { renderRevisoes(); } catch (e) { console.error(e); } });

function toggleTheme() {
  const html = document.documentElement;
  const isDark = html.getAttribute("data-theme") === "dark" || (!html.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
  const next = isDark ? "light" : "dark";
  html.setAttribute("data-theme", next);
  try { localStorage.setItem("roteiro-theme", next); } catch (e) {}
}

// Monta a agenda antes da primeira pintura (o script está no fim do <body>)
renderRevisoes();
"""

TEMPLATE = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Revisões · Roteiro IA</title>
__FAVICON__
__AUTH_GUARD__
<style>
__CSS__
</style>
</head>
<body>

<header class="top-nav">
  <div class="top-nav-inner">
    <a href="index.html" class="nav-brand">🚀 <span>Roteiro IA</span></a>
    <nav class="nav-links">
      <a href="index.html" class="nav-link">🏠 Hub Central</a>
      <a href="ia.html" class="nav-link">🤖 IA & Código</a>
      <a href="matematica.html" class="nav-link">📐 Matemática</a>
      <a href="ingles.html" class="nav-link">🇺🇸 Inglês EnglishBay</a>
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

<main class="rvp-main">
  <div class="rvp-head">
    <div>
      <h1>↻ Revisões</h1>
      <p>Revisar no dia certo é o que faz o conteúdo ficar. O quiz de cada aula agenda as revisões sozinho, e você pode agendar qualquer aula. Depois de revisar, diga como foi: o site agenda a próxima.</p>
    </div>
    <button type="button" class="rvp-btn" onclick="rvpToggleSearch()">📅 Agendar revisão</button>
  </div>

  <div class="rvp-search" id="rv-busca" hidden>
    <input type="search" placeholder="Buscar aula para agendar (ex.: logaritmos, listas, present simple)" aria-label="Buscar aula para agendar" oninput="rvpSearch(this.value)">
    <ul class="rvp-res" id="rv-busca-res"></ul>
  </div>

  <div class="rvp-today" id="rv-hoje" hidden></div>
  <div class="rvp-cal" id="rv-cal" aria-label="Próximos 14 dias"></div>

  <div class="rvp-grid">
    <div id="rv-lista"></div>
    <aside>
      <div class="rvp-box" id="rv-semana"></div>
      <div class="rvp-box">
        <h3>Como o site agenda</h3>
        <div class="rvp-rule"><span>😌</span><span><b>Fácil:</b> a próxima fica mais longe (1 → 3 → 7 → 21 → 60 dias). Fácil nos 60 dias: aula dominada, sai da agenda.</span></div>
        <div class="rvp-rule"><span>🙂</span><span><b>Com esforço:</b> repete o mesmo intervalo.</span></div>
        <div class="rvp-rule"><span>😵</span><span><b>Não lembrei:</b> volta amanhã, e o intervalo recomeça.</span></div>
        <div class="rvp-rule rvp-muted"><span>✅</span><span>Passou no quiz de uma aula? A 1ª revisão fica para o dia seguinte. Refazer o quiz no dia da revisão também conta.</span></div>
        <div class="rvp-rule rvp-muted"><span>↻</span><span>A situação das aulas e os pontos da Jornada não mudam com as revisões.</span></div>
      </div>
      <div class="rvp-box" id="rv-custo" hidden></div>
    </aside>
  </div>
</main>

__CHANGE_CRED__

<script>
__AUTH_JS__

__PAGE_JS__
</script>
</body>
</html>"""


def generate_review_page(out_path, shared_css, topic_index_json):
    """topic_index_json: [[id, trilha, título], ...] (o mesmo índice da busca do design v2)."""
    topics = {row[0]: [row[1], row[2]] for row in json.loads(topic_index_json)}
    page_js = REVIEW_PAGE_JS.replace("__RV_TOPICS__", json.dumps(topics, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
    html = (TEMPLATE
            .replace("__FAVICON__", FAVICON_LINK)
            .replace("__AUTH_GUARD__", AUTH_GUARD_HEAD_SCRIPT)
            .replace("__CSS__", shared_css + "\n" + AUTH_AWS_SYNC_CSS + "\n" + REVIEW_PAGE_CSS)
            .replace("__CHANGE_CRED__", CHANGE_CREDENTIALS_MODAL_HTML)
            .replace("__AUTH_JS__", AUTH_AWS_SYNC_JS)
            .replace("__PAGE_JS__", page_js))
    from design_v2 import apply_design
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(apply_design(html, "rev"))
    print(f"Gerado: {out_path} (Revisões)")
