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
.rvp-today>div{flex:1;min-width:0}
.rvp-go{flex-direction:column;gap:0;min-height:44px;padding:7px 18px;font-size:.88rem}
.rvp-go small{font-weight:600;font-size:.7rem;opacity:.75}
@media (max-width:640px){.rvp-today{flex-wrap:wrap}.rvp-go{width:100%}}
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
.rvp-tr-sub{margin:0 0 6px;font-size:.78rem;line-height:1.45;color:var(--mu)}
.rvp-tr{display:flex;align-items:center;gap:10px;padding:9px 0;border-top:1px solid var(--bd)}
.rvp-tr>div{flex:1;min-width:0}
.rvp-tr b{display:block;font-size:.86rem;line-height:1.35}
.rvp-tr small{display:block;margin-top:2px;font-size:.74rem;color:var(--mu)}
.rvp-tr .rvp-btn{flex:none}
.rvp-rule{display:flex;gap:10px;padding:5px 0;font-size:.84rem;line-height:1.45}
.rvp-rule span:first-child{flex:none;width:20px;text-align:center}
.rvp-muted{color:var(--mu)}
"""

RA_JS = r"""
// =================== REVISÃO ATIVA: escolha dos cartões, nota e caderno (sem tela; testado no Node) ===================
const RA = (() => {
  const LABEL = { mem: "Puxe da memória", arm: "Armadilha comum", not: "Notação", pen: "Pense", pas: "Por que este passo?",
                  exp: "Explique com suas palavras", pon: "Onde isso aparece na IA?", obj: "Consegue explicar isto?", quiz: "Quiz relâmpago",
                  tr: "Treino relâmpago" };
  const hasTR = () => typeof TR !== "undefined";   // o Treino carrega depois deste script: confere na hora do uso
  const PTS = { f: 1, m: 0.5, z: 0 };
  function shuffle(arr, rnd) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); const t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  // Cartões de uma sessão: o "puxe da memória" primeiro, até 3 rápidos (um de cada tipo antes de repetir) e até 3 de marcar:
  // com treino na aula, até 2 vêm do treino (contas com números novos, código) e o resto do quiz de saída
  function pick(deck, rnd) {
    rnd = rnd || Math.random;
    const c = (deck && deck.c) || [];
    const mem = c.filter(x => x.k === "mem").slice(0, 1);
    const trn = hasTR() ? shuffle(c.filter(x => x.k === "tr"), rnd).slice(0, 2) : [];
    const quiz = shuffle(c.filter(x => x.k === "quiz"), rnd).slice(0, 3 - trn.length).concat(trn);
    const tipos = {};
    shuffle(c.filter(x => x.k !== "mem" && x.k !== "quiz" && x.k !== "tr"), rnd).forEach(x => { (tipos[x.k] = tipos[x.k] || []).push(x); });
    const flash = [];
    for (let r = 0; flash.length < 3; r++) {
      let pegou = false;
      for (const k in tipos) if (flash.length < 3 && tipos[k][r]) { flash.push(tipos[k][r]); pegou = true; }
      if (!pegou) break;
    }
    return mem.concat(shuffle(flash, rnd), shuffle(quiz, rnd));
  }
  function score(res) { const n = res.length, s = res.reduce((a, r) => a + (PTS[r] || 0), 0); return { n, s, pct: n ? s / n : 0 }; }
  // Nota sugerida para a agenda: 85% ou mais = fácil; 50% ou mais = com esforço; abaixo = não lembrei
  function suggest(res) { const p = score(res).pct; return p >= 0.85 ? "f" : p >= 0.5 ? "m" : "z"; }
  // Revisão do dia: rodadas alternando as aulas (misturar matérias fixa mais); cada aula começa pela memória
  function interleave(lessons, max) {
    const out = [];
    for (let r = 0; out.length < max; r++) {
      let any = false;
      for (const L of lessons) if (r < L.cards.length && out.length < max) { out.push({ id: L.id, card: L.cards[r] }); any = true; }
      if (!any) break;
    }
    return out;
  }
  // Tira o HTML: quebras de linha e itens viram espaço; marcações no meio do texto (<code>, <b>) só somem
  const strip = h => String(h == null ? "" : h).replace(/<(br|\/p|\/li|\/div|\/h\d)\b[^>]*>/gi, " ").replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/g, " ").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/\s+/g, " ").trim();
  const short = (s, n) => { s = strip(s); return s.length > n ? s.slice(0, n - 1).trimEnd() + "…" : s; };
  function labelOf(c) {
    if (c.k === "tr") return hasTR() ? "Treino: " + TR.labelOf(c.q) : "Treino";
    if (c.k === "mem") return "Ideias-chave da aula";
    if (c.k === "not") return "O que significa " + strip(c.q);
    if (c.k === "exp") return "Explicar: " + short(c.q, 80);
    if (c.k === "pon") return "Onde isso aparece na IA" + (c.q ? " (" + short(c.q, 60) + ")" : "");
    return short(c.q, 90);
  }
  function answerOf(c) {
    if (c.k === "tr") return hasTR() ? short(TR.answerOf(c.q), 160) : "";
    if (c.k === "quiz") return short(c.o[c.c], 160);
    if (c.k === "not") return short((c.l ? c.l + ": " : "") + (c.a || ""), 160);
    if (c.k === "mem" || c.k === "obj") return "";
    return short(c.a, 160);
  }
  // Texto para o caderno da aula (Markdown), com os cartões que você não lembrou
  function noteText(weak, dia) {
    if (!weak || !weak.length) return "";
    return "\n\n## 🔁 Revisão ativa de " + dia + ": pontos para reforçar\n" +
      weak.map(c => { const a = answerOf(c); return "- " + labelOf(c) + (a ? " → " + a : ""); }).join("\n") + "\n";
  }
  return { LABEL, shuffle, pick, score, suggest, interleave, strip, labelOf, answerOf, noteText };
})();
if (typeof module !== "undefined") module.exports = RA;
"""

RA_UI_JS = r"""
// =================== REVISÃO ATIVA: a sessão em cartões ===================
let RA_DECKS = null, RA_S = null;
async function raLoadDecks() {
  if (RA_DECKS) return RA_DECKS;
  const r = await fetch("revisao_cartoes.json", { cache: "no-cache" });
  if (!r.ok) throw new Error("erro " + r.status);
  RA_DECKS = await r.json();
  return RA_DECKS;
}
function raMath(el) {
  if (!window.renderMathInElement) return;
  try {
    window.renderMathInElement(el, { delimiters: [{ left: "$$", right: "$$", display: true }, { left: "$", right: "$", display: false },
      { left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }], throwOnError: false });
  } catch (e) {}
}
function raSet(id, v) { const e = document.getElementById(id); if (e) e.textContent = v; }
function raClose(ask) {
  if (ask && RA_S && RA_S.i > 0 && RA_S.i < RA_S.items.length && !confirm("Sair da revisão? Os cartões que você já respondeu não serão salvos.")) return;
  document.getElementById("ra").hidden = true;
  document.body.classList.remove("ra-on");
  RA_S = null;
}

// ids: aulas da sessão · mode: "one" (uma aula) ou "day" (revisão do dia, aulas misturadas)
async function raStart(ids, mode) {
  const box = document.getElementById("ra"), body = document.getElementById("ra-body");
  box.hidden = false; document.body.classList.add("ra-on");
  raSet("ra-title", mode === "day" ? "Revisão do dia" : "Revisão ativa"); raSet("ra-count", "");
  document.getElementById("ra-bar").style.width = "0%";
  body.innerHTML = '<div class="ra-wait">Preparando os cartões…</div>';
  let decks;
  try { decks = await raLoadDecks(); }
  catch (e) { body.innerHTML = '<div class="ra-wait">Não consegui carregar os cartões (' + rvEsc(e.message) + "). Confira a conexão e tente de novo.</div>"; return; }
  const lessons = ids.filter(id => decks[id] && RV_TOPICS[id]).map(id => ({ id, cards: RA.pick(decks[id]) })).filter(L => L.cards.length);
  if (!lessons.length) {
    body.innerHTML = '<div class="ra-wait">Esta aula ainda não tem cartões de revisão. Revise pela própria aula e use o <b>⋯ → Já revisou?</b> para registrar.</div>';
    return;
  }
  const items = mode === "day" ? RA.interleave(lessons, 24) : lessons[0].cards.map(card => ({ id: lessons[0].id, card }));
  RA_S = { mode, items, i: 0, shown: false, answered: null, res: {}, weak: {}, grade: {},
           ids: lessons.map(L => L.id).filter(id => items.some(x => x.id === id)) };
  raRender();
}
function rvStartActive(id) { raStart([id], "one"); }   // o "▶ Fazer a revisão ativa" do menu, já nesta página
function raStartDay() {
  const hoje = RV.today();
  raStart(RV.agenda().filter(it => it.due <= hoje && RV_TOPICS[it.id]).slice(0, 5).map(it => it.id), "day");
}

function raFaces(it) {
  const c = it.card, deck = RA_DECKS[it.id] || {}, li = a => "<ul>" + a.map(x => "<li>" + x + "</li>").join("") + "</ul>";
  switch (c.k) {
    case "mem": return { f: "Sem olhar: quais são as ideias-chave desta aula? Tente lembrar pelo menos duas antes de virar." +
                           (c.h && c.h.length ? '<details class="ra-hint"><summary>Dica: o que a aula prometia ensinar</summary>' + li(c.h) + "</details>" : ""),
                         b: li(c.a) };
    case "arm": return { f: "Erro comum: " + c.q + '<span class="ra-sub">O que está errado e qual é o jeito certo?</span>', b: c.a };
    case "not": return { f: 'O que significa <span class="ra-sym">' + c.q + "</span>?", b: (c.l ? "<b>" + c.l + "</b><br>" : "") + (c.a || "") };
    case "pas": return { f: (c.t ? '<span class="ra-sub ra-top-sub">' + c.t + "</span>" : "") + "Por que este passo? " + c.q, b: c.a };
    case "exp": return { f: "Explique com suas palavras: <b>" + c.q + "</b>", b: c.a };
    case "pon": return { f: "Onde isso aparece na IA?" + (c.q ? '<span class="ra-sub">' + c.q + "</span>" : ""), b: c.a };
    case "obj": { const mem = (deck.c || []).find(x => x.k === "mem");
                  return { f: "Consegue explicar isto de cabeça? " + c.q, b: "Compare com as ideias-chave:" + (mem ? li(mem.a) : "") }; }
    default: return { f: c.q, b: c.a || "" };
  }
}

function raRender() {
  const S = RA_S; if (!S) return;
  if (S.i >= S.items.length) return raResult();
  const it = S.items[S.i], c = it.card, t = rvpTrack(it.id);
  raSet("ra-count", (S.i + 1) + " / " + S.items.length);
  document.getElementById("ra-bar").style.width = (S.i / S.items.length * 100) + "%";
  const chip = '<div class="ra-chip" style="--c:var(' + t.cor + ')"><i></i><span>' + rvEsc(RV_TOPICS[it.id][1]) + "</span><small>" + t.nome + "</small></div>";
  if (c.k === "tr") return raRenderTreino(it, chip);   // questão do Treino (contas com números novos, código)
  const faces = raFaces(it);
  let h = chip + '<div class="ra-card"><div class="ra-kick">' + RA.LABEL[c.k] + '</div><div class="ra-q">' + faces.f + "</div>";
  if (c.k === "quiz") {
    const a = S.answered;
    h += '<div class="ra-opts">' + c.o.map((o, i) => '<button type="button" class="ra-opt' +
         (a != null ? (i === c.c ? " ok" : i === a ? " no" : "") : "") + '" data-o="' + i + '"' + (a != null ? " disabled" : "") +
         "><kbd>" + (i + 1) + "</kbd>" + o + "</button>").join("") + "</div>";
    if (a != null) h += '<div class="ra-a ' + (a === c.c ? "ok" : "no") + '"><b>' + (a === c.c ? "✓ Isso!" : "✗ Não foi dessa vez.") + "</b> " + (c.e || "") + "</div>";
    h += "</div>" + (a != null ? '<div class="ra-actions"><button type="button" class="ra-btn pri" data-next>Continuar →</button></div>'
                                : '<p class="ra-tip">Escolha uma opção (ou tecle o número).</p>');
  } else {
    if (S.shown) h += '<div class="ra-a">' + faces.b + "</div>";
    h += "</div>";
    h += S.shown
      ? '<p class="ra-tip">Como foi para lembrar?</p><div class="ra-grades">' +
        '<button type="button" class="ra-grade" data-g="z"><span>😵</span>Não lembrei<kbd>1</kbd></button>' +
        '<button type="button" class="ra-grade" data-g="m"><span>🙂</span>Com esforço<kbd>2</kbd></button>' +
        '<button type="button" class="ra-grade" data-g="f"><span>😌</span>Lembrei fácil<kbd>3</kbd></button></div>'
      : '<div class="ra-actions"><button type="button" class="ra-btn pri" data-show>Mostrar resposta<kbd>espaço</kbd></button></div>' +
        '<p class="ra-tip">Tente responder de cabeça (ou em voz alta) antes de virar.</p>';
  }
  const body = document.getElementById("ra-body");
  body.innerHTML = h; body.scrollTop = 0; raMath(body);
  const show = body.querySelector("[data-show]"); if (show) show.onclick = () => { S.shown = true; raRender(); };
  body.querySelectorAll("[data-g]").forEach(b => b.onclick = () => raGrade(b.dataset.g));
  body.querySelectorAll("[data-o]").forEach(b => b.onclick = () => raAnswer(+b.dataset.o));
  const nx = body.querySelector("[data-next]"); if (nx) nx.onclick = raAdvance;
}
// Cartão com uma questão do Treino: a mesma tela do treino (trQHTML), dentro do cartão da revisão
function raRenderTreino(it, chip) {
  const S = RA_S, body = document.getElementById("ra-body");
  if (!it.inst) it.inst = TR.inst(it.card.q);
  if (!it.inst) { S.i++; return raRender(); }          // gerador desconhecido: pula o cartão
  const a = S.answered;
  body.innerHTML = chip + '<div class="ra-card tr-in"><div class="ra-kick">' + RA.LABEL.tr + "</div>" + trQHTML(it.inst, a) + "</div>" +
    (a != null ? '<div class="ra-actions"><button type="button" class="ra-btn pri" data-next>Continuar →</button></div>'
               : '<p class="ra-tip">' + (it.inst.k === "erro" ? "Toque na linha com o erro (ou tecle o número dela)." : "Escolha uma opção (ou tecle o número).") + "</p>");
  body.scrollTop = 0; raMath(body);
  body.querySelectorAll("[data-o]").forEach(b => b.onclick = () => raAnswer(+b.dataset.o));
  const nx = body.querySelector("[data-next]"); if (nx) nx.onclick = raAdvance;
}
function raRecord(id, g, card) {
  (RA_S.res[id] = RA_S.res[id] || []).push(g);
  if (g === "z") (RA_S.weak[id] = RA_S.weak[id] || []).push(card);
}
function raGrade(g) { const it = RA_S.items[RA_S.i]; raRecord(it.id, g, it.card); raAdvance(); }
function raAnswer(i) {
  const S = RA_S, it = S.items[S.i], tr = it.card.k === "tr";
  if (S.answered != null || (tr && !(it.inst && trCanAnswer(it.inst, i)))) return;
  S.answered = i;
  raRecord(it.id, i === (tr ? it.inst.c : it.card.c) ? "f" : "z", it.card);
  raRender();
}
function raAdvance() { RA_S.i++; RA_S.shown = false; RA_S.answered = null; raRender(); }

function raReforco(id) {
  const r = (RA_DECKS[id] || {}).r || {}, link = rvpLink(id);
  let h = '<div class="ra-ref"><b>🎯 Reforço sugerido</b><ul>';
  if (r.v2) h += '<li>🎬 Outra explicação: <a href="' + link + '&video=2">' + rvEsc(r.v2) + "</a></li>";
  if (r.kid) h += '<li><details><summary>🧒 Explicação bem simples</summary><div class="ra-kid">' + r.kid + "</div></details></li>";
  (r.src || []).forEach(s => { h += '<li>📚 <a href="' + rvEsc(s.url) + '" target="_blank" rel="noopener">' + rvEsc(s.nome) + "</a>" + (s.tempo ? " · " + rvEsc(s.tempo) : "") + "</li>"; });
  return h + '<li>📘 <a href="' + link + '">Rever na aula</a> os pontos marcados com ✗</li></ul></div>';
}
function raPicker(id) {
  return '<div class="ra-pick" data-id="' + id + '">' + [["z", "😵", "Não lembrei"], ["m", "🙂", "Com esforço"], ["f", "😌", "Fácil"]].map(([g, e, n]) => {
    const d = RV.preview(id, g);
    return '<button type="button" class="ra-pg' + (RA_S.grade[id] === g ? " on" : "") + '" data-g="' + g + '"><span>' + e + "</span>" + n +
           "<small>" + (d ? "próxima " + rvDueText(d) : "aula dominada") + "</small></button>";
  }).join("") + "</div>";
}

function raResult() {
  const S = RA_S, body = document.getElementById("ra-body");
  raSet("ra-count", "Resultado");
  document.getElementById("ra-bar").style.width = "100%";
  S.ids.forEach(id => { if (!S.grade[id]) S.grade[id] = RA.suggest(S.res[id] || []); });
  const anyWeak = S.ids.some(id => (S.weak[id] || []).length);
  let h = "";
  if (S.ids.length === 1) {
    const id = S.ids[0], sc = RA.score(S.res[id] || []), pct = Math.round(sc.pct * 100), weak = S.weak[id] || [];
    const firmes = S.items.filter(x => x.id === id && weak.indexOf(x.card) < 0);
    h += '<div class="ra-res-head"><div class="ra-ring" style="--p:' + pct + '"><b>' + pct + "%</b></div><div><h3>" +
         (sc.pct >= 0.85 ? "Mandou bem! Ficou firme." : sc.pct >= 0.5 ? "Boa revisão! Alguns pontos pedem reforço." : "Essa custou, e tudo bem: é assim que fixa.") +
         "</h3><p>" + rvEsc(RV_TOPICS[id][1]) + "</p></div></div>";
    h += '<ul class="ra-list">' + firmes.map(x => '<li class="ok">✓ ' + rvEsc(RA.labelOf(x.card)) + "</li>").join("") +
         weak.map(c => '<li class="no">✗ ' + rvEsc(RA.labelOf(c)) + "</li>").join("") + "</ul>";
    if (weak.length || S.grade[id] === "z") h += raReforco(id);
    h += '<div class="ra-h4">Como foi, no geral? (sugerimos pela sua nota)</div>' + raPicker(id);
  } else {
    h += '<div class="ra-res-head"><div><h3>Revisão do dia concluída 🎉</h3><p>' + S.items.length + " cartões de " + S.ids.length + " aulas</p></div></div>";
    S.ids.forEach(id => {
      const sc = RA.score(S.res[id] || []), weak = S.weak[id] || [];
      h += '<div class="ra-row"><div class="ra-row-h"><b>' + rvEsc(RV_TOPICS[id][1]) + "</b><span>" + Math.round(sc.pct * 100) + "%</span></div>" +
           (weak.length ? '<p class="ra-weak">✗ ' + weak.map(c => rvEsc(RA.labelOf(c))).join(" · ") +
                          ' · <a href="' + rvpLink(id) + '">rever na aula</a></p>' : "") + raPicker(id) + "</div>";
    });
  }
  if (anyWeak) h += '<label class="ra-check"><input type="checkbox" id="ra-anotar" checked> Anotar no caderno da aula os pontos para reforçar</label>';
  h += '<div class="ra-actions"><button type="button" class="ra-btn pri" data-fim>Concluir e agendar</button></div>';
  body.innerHTML = h; body.scrollTop = 0; raMath(body);
  body.querySelectorAll(".ra-pick").forEach(p => p.querySelectorAll(".ra-pg").forEach(b => b.onclick = () => {
    S.grade[p.dataset.id] = b.dataset.g;
    p.querySelectorAll(".ra-pg").forEach(x => x.classList.toggle("on", x === b));
  }));
  body.querySelector("[data-fim]").onclick = raFinish;
}

function raFinish() {
  const S = RA_S, anotar = document.getElementById("ra-anotar"), dia = RV.fmt(RV.today());
  const prox = S.ids.map(id => {
    RV.complete(id, S.grade[id]);
    if (anotar && anotar.checked) { const md = RA.noteText(S.weak[id] || [], dia); if (md) RV.appendNote(id, md); }
    const it = RV.byId()[id];
    return it ? it.due : null;
  });
  const n = S.ids.length;
  raClose(false);
  rvToast(n === 1 ? (prox[0] ? "Revisão registrada. Próxima: " + rvDueText(prox[0]) + "." : "🏆 Aula dominada! Ela sai da agenda.")
                  : n + " revisões registradas. Bom trabalho!");
}

document.addEventListener("keydown", e => {
  const S = RA_S;
  if (document.getElementById("ra").hidden) return;
  if (e.key === "Escape") { e.preventDefault(); raClose(true); return; }
  if (!S || S.i >= S.items.length || e.target.closest && e.target.closest("input,textarea,summary")) return;
  const c = S.items[S.i].card, inst = S.items[S.i].inst;
  if (c.k === "quiz" || c.k === "tr") {
    const n = c.k === "tr" ? (inst ? (inst.lines || inst.opts).length : 0) : c.o.length;
    if (S.answered == null && /^[1-9]$/.test(e.key) && +e.key <= n) { e.preventDefault(); raAnswer(+e.key - 1); }
    else if (S.answered != null && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); raAdvance(); }
  } else if (!S.shown && (e.key === " " || e.key === "Enter")) { e.preventDefault(); S.shown = true; raRender(); }
  else if (S.shown && ["1", "2", "3"].includes(e.key)) { e.preventDefault(); raGrade({ 1: "z", 2: "m", 3: "f" }[e.key]); }
});
"""

RA_CSS = r"""
/* ===== Revisão ativa (sessão em cartões) ===== */
.ra{position:fixed;inset:0;z-index:99990;display:flex;align-items:center;justify-content:center;padding:18px;
  background:color-mix(in srgb,var(--bg) 84%,transparent);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.ra[hidden]{display:none}
body.ra-on{overflow:hidden}
.ra-box{width:min(680px,100%);max-height:100%;display:flex;flex-direction:column;border:1px solid var(--bd);border-radius:22px;
  background:var(--card);box-shadow:0 40px 100px rgba(0,0,0,.5);overflow:hidden}
.ra-top{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:12px 16px}
.ra-x{width:36px;height:36px;border-radius:50%;border:1px solid var(--bd);background:transparent;color:var(--tx);cursor:pointer;font:inherit}
.ra-top span{min-width:36px;text-align:right;color:var(--mu);font-size:.85rem;font-variant-numeric:tabular-nums}
.ra-prog{height:4px;background:var(--bd)}
.ra-prog i{display:block;height:100%;width:0;background:var(--t-hub);transition:width .25s}
.ra-body{padding:18px 20px 22px;overflow:auto}
.ra-wait{padding:40px 10px;text-align:center;color:var(--mu);line-height:1.6}
.ra-chip{display:flex;align-items:center;gap:8px;margin-bottom:12px;font-size:.82rem;color:var(--mu)}
.ra-chip i{flex:none;width:8px;height:8px;border-radius:50%;background:var(--c)}
.ra-chip span{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ra-chip small{margin-left:auto;flex:none;font-size:.74rem}
.ra-card{padding:18px;border-radius:18px;border:1px solid color-mix(in srgb,var(--t-hub) 28%,var(--bd));
  background:linear-gradient(180deg,color-mix(in srgb,var(--t-hub) 7%,var(--card)),var(--card))}
.ra-kick{font-size:.7rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#f5a524}
.ra-q{margin-top:8px;font-size:1.12rem;font-weight:650;line-height:1.45}
.ra-sub{display:block;margin-top:6px;font-size:.86rem;font-weight:500;color:var(--mu)}
.ra-top-sub{margin:0 0 6px}
.ra-sym{font-size:1.2em}
.ra-hint{margin-top:10px;font-size:.84rem;font-weight:500;color:var(--mu)}
.ra-hint summary{cursor:pointer}
.ra-a{margin-top:14px;padding-top:12px;border-top:1px dashed var(--bd);font-size:.95rem;line-height:1.6}
.ra-a ul{margin:.3em 0 0;padding-left:1.2em}
.ra-a.ok b{color:#2fa36b}.ra-a.no b{color:#ef6b5b}
.ra code,.ra-a code{background:rgba(74,92,106,.22);padding:1px 5px;border-radius:4px;font-size:.88em}
.ra-opts{display:flex;flex-direction:column;gap:8px;margin-top:14px}
.ra-opt{display:flex;gap:10px;align-items:flex-start;padding:10px 14px;border-radius:12px;border:1px solid var(--bd);background:var(--bg);
  color:var(--tx);font:inherit;font-size:.92rem;text-align:left;cursor:pointer}
.ra-opt kbd{flex:none;font:700 .7rem Inter,system-ui;opacity:.55;margin-top:3px}
.ra-opt:hover:not([disabled]){border-color:var(--t-hub)}
.ra-opt[disabled]{cursor:default}
.ra-opt.ok{border-color:#2fa36b;background:color-mix(in srgb,#2fa36b 14%,var(--bg))}
.ra-opt.no{border-color:#ef6b5b;background:color-mix(in srgb,#ef6b5b 12%,var(--bg))}
.ra-actions{display:flex;justify-content:center;margin-top:16px}
.ra-btn{display:inline-flex;align-items:center;gap:8px;min-height:42px;padding:9px 20px;border-radius:99px;border:1px solid var(--bd);
  background:transparent;color:var(--tx);font:inherit;font-weight:700;cursor:pointer}
.ra-btn.pri{background:var(--t-hub);border-color:var(--t-hub);color:#04201d}
.ra-btn kbd,.ra-grade kbd{font:600 .66rem Inter,system-ui;opacity:.6}
.ra-tip{margin:12px 0 0;text-align:center;font-size:.8rem;color:var(--mu)}
.ra-grades{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:10px}
.ra-grade{display:flex;flex-direction:column;align-items:center;gap:3px;padding:12px 6px;border-radius:14px;border:1px solid var(--bd);
  background:var(--bg);color:var(--tx);font:inherit;font-size:.84rem;cursor:pointer}
.ra-grade span{font-size:1.4rem}
.ra-grade:hover{border-color:var(--t-hub)}
.ra-res-head{display:flex;align-items:center;gap:16px;margin-bottom:10px}
.ra-res-head h3{margin:0;font-size:1.15rem;line-height:1.35}
.ra-res-head p{margin:4px 0 0;color:var(--mu);font-size:.88rem}
.ra-ring{--p:0;flex:none;width:88px;height:88px;border-radius:50%;display:grid;place-items:center;
  background:conic-gradient(var(--t-hub) calc(var(--p) * 1%),var(--bd) 0)}
.ra-ring b{width:68px;height:68px;border-radius:50%;display:grid;place-items:center;background:var(--card);font-size:1.15rem}
.ra-list{list-style:none;margin:8px 0;padding:0;font-size:.88rem;line-height:1.6}
.ra-list .ok{color:#2fa36b}.ra-list .no{color:#ef6b5b}
.ra-ref{margin-top:12px;padding:12px 14px;border-radius:14px;border:1px solid color-mix(in srgb,#e8a100 40%,var(--bd));
  background:color-mix(in srgb,#e8a100 8%,var(--card));font-size:.88rem}
.ra-ref ul{margin:6px 0 0;padding-left:1.1em}
.ra-ref li{margin:5px 0}
.ra-ref a{color:var(--t-hub)}
.ra-ref summary{cursor:pointer}
.ra-kid{margin-top:6px;font-size:.86rem;line-height:1.55}
.ra-h4{margin:16px 0 6px;font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--mu)}
.ra-pick{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.ra-pg{display:flex;flex-direction:column;align-items:center;gap:2px;padding:9px 4px;border-radius:12px;border:1px solid var(--bd);
  background:var(--bg);color:var(--tx);font:inherit;font-size:.8rem;cursor:pointer;line-height:1.25}
.ra-pg span{font-size:1.15rem}
.ra-pg small{font-size:.68rem;color:var(--mu)}
.ra-pg.on{border-color:var(--t-hub);box-shadow:inset 0 0 0 1px var(--t-hub)}
.ra-row{padding:12px 0;border-top:1px solid var(--bd)}
.ra-row-h{display:flex;justify-content:space-between;gap:10px;margin-bottom:6px;font-size:.9rem}
.ra-weak{margin:0 0 8px;font-size:.8rem;color:#ef6b5b}
.ra-weak a{color:var(--t-hub)}
.ra-check{display:flex;gap:8px;align-items:flex-start;margin-top:14px;font-size:.86rem;color:var(--mu)}
@media (max-width:600px){.ra{padding:0}.ra-box{height:100%;max-height:none;border-radius:0;border:0}.ra-q{font-size:1.02rem}.ra-body{padding:14px 14px 20px}}
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
    '<div class="rvp-acts"><button type="button" class="rvp-btn pri" onclick="raStart([\'' + it.id + '\'], \'one\')" title="Revisão ativa em cartões (5 a 10 min)">▶ Revisar</button>' +
    '<a class="rvp-btn" href="' + rvpLink(it.id) + '">Abrir aula</a>' +
    '<button type="button" class="rvp-btn" aria-label="Já revisou, mudar a data ou tirar da agenda" title="Já revisou, mudar a data ou tirar da agenda" ' +
    'onclick="openReviewMenu(\'' + it.id + '\', this, \'all\')">⋯</button></div></li>';
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
    const aulas = Math.min(n, 5), min = Math.max(5, Math.min(24, aulas * 6));
    box.innerHTML = '<span class="ico" aria-hidden="true">🧠</span><div><b>Hoje: ' + n + (n === 1 ? " revisão" : " revisões") +
      (atrasadas.length ? " · " + atrasadas.length + (atrasadas.length === 1 ? " atrasada" : " atrasadas") : "") + "</b>" +
      "<span>Cartões das aulas" + (aulas > 1 ? ", misturados (misturar matérias fixa mais)" : "") + ". No fim, você diz como foi e o site agenda a próxima." +
      (n > 5 ? " Começa pelas 5 mais urgentes." : "") + '</span></div><button type="button" class="rvp-btn pri rvp-go" onclick="raStartDay()">▶ Começar revisão do dia<small>≈ ' + min + " min</small></button>";
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

// Treino misto: um botão por fase/módulo que tem treino (questões de várias aulas, misturadas)
function rvpTreino() {
  const el = document.getElementById("rv-treino");
  if (!el || typeof TR_MODS === "undefined" || !TR_MODS.length) return;
  const st = trStudied();
  el.hidden = false;
  el.innerHTML = "<h3>🏋️ Treino misto</h3><p class=\"rvp-tr-sub\">Questões de marcar de várias aulas do módulo, misturadas. Não muda a agenda nem os pontos.</p>" +
    TR_MODS.map(m => {
      const feitas = m.ids.filter(id => st.has(id)).length, treinadas = m.ids.filter(id => TR.stats(id)).length;
      const meta = [m.ids.length + " aulas com treino", feitas ? feitas + (feitas === 1 ? " já estudada" : " já estudadas") : "nenhuma estudada ainda"];
      if (treinadas) meta.push(treinadas + (treinadas === 1 ? " já treinada" : " já treinadas"));
      return '<div class="rvp-tr"><i class="rvp-dot" style="--c:var(' + (RV_TRK[m.tr] || RV_TRK.ia).cor + ')" aria-hidden="true"></i><div><b>' + rvEsc(m.nome) + "</b><small>" +
        meta.join(" · ") + '</small></div><button type="button" class="rvp-btn pri" onclick="trOpenMixed(\'' + m.k + '\')">Treinar</button></div>';
    }).join("");
}

window.addEventListener("rv:change", () => { try { renderRevisoes(); } catch (e) { console.error(e); } });
window.addEventListener("tr:change", () => { try { rvpTreino(); } catch (e) { console.error(e); } });

function toggleTheme() {
  const html = document.documentElement;
  const isDark = html.getAttribute("data-theme") === "dark" || (!html.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
  const next = isDark ? "light" : "dark";
  html.setAttribute("data-theme", next);
  try { localStorage.setItem("roteiro-theme", next); } catch (e) {}
}

// Monta a agenda antes da primeira pintura (o script está no fim do <body>); o treino misto, quando o Treino carregar
renderRevisoes();
window.addEventListener("DOMContentLoaded", () => { try { rvpTreino(); } catch (e) {} });

// revisoes.html?ativa=<aula>: vem do "▶ Fazer a revisão ativa" de uma aula ou do hub
// revisoes.html?dia=1: vem do "Começar" do aviso de revisões (sino ou cartão "Hoje"): abre a revisão do dia
(function () {
  try {
    const qs = new URLSearchParams(location.search), id = qs.get("ativa");
    if (id && RV_TOPICS[id]) { history.replaceState(null, "", location.pathname); raStart([id], "one"); }
    else if (qs.get("dia")) { history.replaceState(null, "", location.pathname); if (RV.counts().due) raStartDay(); }
  } catch (e) {}
})();
"""

TEMPLATE = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Revisões · Roteiro IA</title>
__FAVICON__
__AUTH_GUARD__
<!-- KaTeX: fórmulas dos cartões de Matemática -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
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
      <div class="rvp-box" id="rv-treino" hidden></div>
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

<!-- REVISÃO ATIVA: a sessão em cartões (uma aula ou a revisão do dia) -->
<div class="ra" id="ra" hidden role="dialog" aria-modal="true" aria-labelledby="ra-title">
  <div class="ra-box">
    <div class="ra-top">
      <button type="button" class="ra-x" onclick="raClose(true)" aria-label="Sair da revisão" title="Sair (Esc)">✕</button>
      <b id="ra-title">Revisão ativa</b>
      <span id="ra-count"></span>
    </div>
    <div class="ra-prog"><i id="ra-bar"></i></div>
    <div class="ra-body" id="ra-body"></div>
  </div>
</div>

<script>
__AUTH_JS__

__RA_JS__

__RA_UI_JS__

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
            .replace("__CSS__", shared_css + "\n" + AUTH_AWS_SYNC_CSS + "\n" + REVIEW_PAGE_CSS + "\n" + RA_CSS)
            .replace("__CHANGE_CRED__", CHANGE_CREDENTIALS_MODAL_HTML)
            .replace("__AUTH_JS__", AUTH_AWS_SYNC_JS)
            .replace("__RA_JS__", RA_JS)
            .replace("__PAGE_JS__", page_js)
            .replace("__RA_UI_JS__", RA_UI_JS))
    from design_v2 import apply_design
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(apply_design(html, "rev"))
    print(f"Gerado: {out_path} (Revisões)")
