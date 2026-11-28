# -*- coding: utf-8 -*-
"""
Treino: questões de marcar para fixar cada aula, principalmente de código e de contas.

Tipos de questão ("k"):
  saida     "Qual é a saída?": codigo, opcoes (texto da tela), correta, porques (opcional), x
  lacuna    "Complete o código": codigo com "____", pergunta, opcoes (pedaços de código), correta, saida, x
  erro      "Ache o erro": codigo, linha (1 = primeira), correcao (a linha certa), saida (opcional), pergunta (opcional), x
  conceito  múltipla escolha: pergunta (HTML, aceita $LaTeX$), opcoes, correta, porques (opcional), codigo (opcional), x
  conta     "Faça a conta": g (id do gerador em treino_contas.py) e p (parâmetros, opcional). Os números mudam a cada vez.
Todos aceitam "tema" (rótulo curto para a lista de erros) e "fixa": true (não embaralhar as alternativas).

As questões de código são conferidas rodando o Python (treino.py / test_treino.py): o gabarito é o que o
Python imprime de verdade. Os geradores de conta são sorteados centenas de vezes nos testes e conferidos com o NumPy.

TR_JS     cálculo, sem tela (sorteio, alternativas, gravação do resultado); roda no Node nos testes
TR_UI_JS  a sessão na tela (uma aula, ou misto por módulo na página Revisões) e o cartão "Treinar esta aula"
TR_CSS    estilos
"""

TR_JS = r"""
// =================== TREINO: questões de marcar (sem tela; testado no Node) ===================
const TR = (() => {
  const KIND = { saida: "🐍 Qual é a saída?", lacuna: "🧩 Complete o código", erro: "🐞 Ache o erro",
                 conta: "🔢 Faça a conta", conceito: "🧠 Conceito" };
  const SHORT = { saida: "saída", lacuna: "completar", erro: "erro", conta: "conta", conceito: "conceito" };
  const ICON = { saida: "🐍", lacuna: "🧩", erro: "🐞", conta: "🔢", conceito: "🧠" };
  const ASK = { saida: "O que aparece na tela?", erro: "Este programa tem um erro. Em qual linha ele está?" };
  const ANS_KEY = "roteiro-answers-v1";   // o resultado fica junto das respostas da aula (vai para a nuvem com elas)
  const PER_SESSION = 10;

  // Números pseudoaleatórios com semente (os testes repetem o mesmo sorteio); na página, Math.random
  function rng(seed) {
    let a = seed >>> 0;
    return () => {
      a = (a + 0x6D2B79F5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function shuffle(arr, rnd) {
    rnd = rnd || Math.random;
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); const t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }

  // ---- números em LaTeX (vírgula decimal, nunca "-0") ----
  function n(x, casas) {
    if (typeof x !== "number") return String(x);
    const c = casas == null ? 2 : casas, p = Math.pow(10, c);
    let v = Math.round(x * p) / p;
    if (v === 0) v = 0;
    let s = String(v);
    if (s.indexOf("e") >= 0) s = v.toFixed(c);
    return s.replace(".", "{,}");
  }
  const vec = (v, c) => "(" + v.map(x => n(x, c)).join(",\\ ") + ")";
  const mat = (M, c) => "\\begin{bmatrix}" + M.map(r => r.map(x => n(x, c)).join(" & ")).join(" \\\\ ") + "\\end{bmatrix}";
  const isMat = v => Array.isArray(v) && v.length > 0 && Array.isArray(v[0]);
  function fmtVal(v, c) {   // valor -> HTML da alternativa
    if (typeof v === "number") return "$" + n(v, c) + "$";
    if (isMat(v)) return "$" + mat(v, c) + "$";
    if (Array.isArray(v)) return "$" + vec(v, c) + "$";
    return String(v);
  }

  // Ferramentas dos geradores de conta
  function tools(rnd) {
    const R = {
      rnd,
      int: (a, b) => a + Math.floor(rnd() * (b - a + 1)),            // inteiro de a até b
      nz: (a, b) => { let x; do { x = R.int(a, b); } while (x === 0); return x; },   // idem, sem o zero
      pick: arr => arr[Math.floor(rnd() * arr.length)],
      sign: () => (rnd() < 0.5 ? -1 : 1),
      vec: (k, a, b) => Array.from({ length: k }, () => R.int(a, b)),
      shuffle: arr => shuffle(arr, rnd),
      n, v: vec, m: mat, fmtVal                                        // formatação em LaTeX
    };
    return R;
  }

  // Alternativa "vizinha" quando o gerador não trouxe erradas suficientes
  function near(v, R) {
    if (typeof v === "number") {
      if (Number.isInteger(v)) return v + R.pick([-3, -2, -1, 1, 2, 3]);
      const d = Math.max(0.01, Math.abs(v) * R.pick([0.1, 0.2, 0.3]));
      return Math.round((v + R.pick([-1, 1]) * d) * 100) / 100;
    }
    if (isMat(v)) { const M = v.map(r => r.slice()), i = R.int(0, M.length - 1), j = R.int(0, M[0].length - 1); M[i][j] = near(M[i][j], R); return M; }
    if (Array.isArray(v)) { const w = v.slice(), i = R.int(0, w.length - 1); w[i] = near(w[i], R); return w; }
    return null;
  }

  const GEN = {};   // geradores de conta: GEN[id] = { t: "título curto", f: (R, p) => ({ q, v, ops, x, d, casas, h }) }

  function conta(q, rnd) {
    const G = GEN[q.g];
    if (!G) return null;
    const R = tools(rnd), r = G.f(R, q.p || {}), c = r.casas;
    const fmt = r.fmt || (v => fmtVal(v, c));          // o gerador pode escrever as alternativas do seu jeito
    const hOf = o => o.h || fmt(o.v);
    const right = { h: hOf(r), v: r.v, why: "", ok: true };
    const seen = new Set([right.h]), wrong = [];      // alternativas com o mesmo texto na tela não se repetem
    (r.ops || []).forEach(o => { const h = hOf(o); if (!seen.has(h)) { seen.add(h); wrong.push({ h, v: o.v, why: o.why || "" }); } });
    for (let t = 0; wrong.length < 3 && t < 80; t++) {
      const v = near(r.v, R); if (v == null) break;
      const h = hOf({ v }); if (!seen.has(h)) { seen.add(h); wrong.push({ h, v, why: "" }); }
    }
    const opts = shuffle([right].concat(wrong.slice(0, 3)), rnd);
    return { k: "conta", g: q.g, t: G.t, q: r.q, opts, c: opts.findIndex(o => o.ok), x: r.x || "", d: r.d, src: q };
  }

  // Uma questão pronta para a tela: alternativas embaralhadas (ou números sorteados, nas contas)
  function inst(q, rnd) {
    rnd = rnd || Math.random;
    if (!q) return null;
    if (q.k === "conta") return conta(q, rnd);
    const base = { k: q.k, q: q.pergunta || ASK[q.k] || "", x: q.x || "", src: q,
                   out: q.saida == null ? null : String(q.saida) };
    if (q.k === "erro") {
      return Object.assign(base, { lines: String(q.codigo || "").split("\n"), c: q.linha - 1, fix: q.correcao || "" });
    }
    const mono = q.k === "saida" || q.k === "lacuna" || !!q.mono;
    const idx = (q.opcoes || []).map((_, i) => i), order = q.fixa ? idx : shuffle(idx, rnd);
    const opts = order.map(i => ({ h: q.opcoes[i], why: (q.porques || [])[i] || "", mono, ok: i === q.correta }));
    return Object.assign(base, { code: q.codigo || null, opts, c: opts.findIndex(o => o.ok) });
  }

  // Sessão de uma aula: até 10 questões, revezando os tipos (nada de 4 contas seguidas)
  function pick(qs, max, rnd) {
    rnd = rnd || Math.random; max = max || PER_SESSION;
    const by = {};
    shuffle(qs || [], rnd).forEach(q => { (by[q.k] = by[q.k] || []).push(q); });
    const kinds = shuffle(Object.keys(by), rnd), out = [];
    for (let r = 0; out.length < max; r++) {
      let any = false;
      for (const k of kinds) if (out.length < max && by[k][r]) { out.push(by[k][r]); any = true; }
      if (!any) break;
    }
    return out;
  }
  // Treino misto: as aulas se revezam (misturar matérias fixa mais) e, de cada aula, vem a questão do tipo
  // menos usado até ali (para não cair, por acaso, 5 "Qual é a saída?" num treino de 10) -> [{id, q}]
  function pickMixed(lessons, max, rnd) {
    rnd = rnd || Math.random; max = max || PER_SESSION;
    const L = shuffle(lessons || [], rnd).map(l => ({ id: l.id, qs: pick(l.qs, max, rnd) })).filter(l => l.qs.length);
    const out = [], usados = {};
    for (let r = 0; out.length < max; r++) {
      let any = false;
      for (const l of L) {
        if (out.length >= max || !l.qs.length) continue;
        let best = 0;
        l.qs.forEach((q, i) => { if ((usados[q.k] || 0) < (usados[l.qs[best].k] || 0)) best = i; });
        const q = l.qs.splice(best, 1)[0];
        usados[q.k] = (usados[q.k] || 0) + 1;
        out.push({ id: l.id, q });
        any = true;
      }
      if (!any) break;
    }
    return out;
  }
  function byKind(items, res) {
    const o = {};
    items.forEach((it, i) => { const k = (it.q || it).k; o[k] = o[k] || [0, 0]; o[k][1]++; if (res[i]) o[k][0]++; });
    return o;
  }

  // ---- resultado por aula, dentro das respostas da aula: a.tr = {b: melhor %, s: "8/10", n: vezes, l: quando} ----
  function readAns() { try { return JSON.parse(localStorage.getItem(ANS_KEY) || "{}") || {}; } catch (e) { return {}; } }
  function stats(id) { const a = readAns()[id]; return (a && a.tr) || null; }
  function record(id, ok, total, now) {
    now = now || Date.now();
    const all = readAns(), a = all[id] || {}, prev = a.tr || null, pct = total ? Math.round(ok / total * 100) : 0;
    a.p = a.p || {}; a.c = a.c || {}; a.q = a.q || {};
    a.tr = { b: Math.max(prev ? prev.b || 0 : 0, pct), s: ok + "/" + total, n: (prev ? prev.n || 0 : 0) + 1, l: now };
    a.t = now;
    all[id] = a;
    try { localStorage.setItem(ANS_KEY, JSON.stringify(all)); } catch (e) {}
    return { prev, cur: a.tr };
  }

  // Rótulos curtos (lista de erros, caderno da aula e revisão ativa)
  const strip = h => String(h == null ? "" : h).replace(/<[^>]+>/g, "").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"').replace(/&amp;/g, "&").replace(/\$/g, "").replace(/\s+/g, " ").trim();
  const short = (s, k) => { s = strip(s); return s.length > k ? s.slice(0, k - 1).trimEnd() + "…" : s; };
  // 1ª linha que diz algo (pula linhas em branco e os imports, iguais em todas as questões de NumPy)
  const firstLine = code => {
    const ls = String(code || "").split("\n").map(l => l.trim()).filter(Boolean);
    return ls.find(l => !/^(import|from)\s/.test(l)) || ls[0] || "";
  };
  function labelOf(q) {
    if (!q) return "";
    if (q.tema) return q.tema;
    if (q.k === "conta") return (GEN[q.g] && GEN[q.g].t) || "Conta";
    if (q.k === "saida") return "Saída de " + short(firstLine(q.codigo), 50);
    if (q.k === "erro") return "Erro em " + short(firstLine(q.codigo), 50);
    return short(q.pergunta, 90);
  }
  function answerOf(q) {
    if (!q || q.k === "conta") return "";
    if (q.k === "erro") return "linha " + q.linha + ": " + String(q.correcao || "").trim();
    return short((q.opcoes || [])[q.correta], 120);
  }

  return { KIND, SHORT, ICON, PER_SESSION, GEN, rng, shuffle, tools, n, vec, mat, fmtVal, near, inst, pick, pickMixed, byKind,
           stats, record, strip, labelOf, answerOf };
})();
if (typeof module !== "undefined") module.exports = TR;
"""

TR_UI_JS = r"""
// =================== TREINO: a sessão na tela ===================
const TR_INDEX = __TR_INDEX__;   // {id da aula: nº de questões}
const TR_MODS = __TR_MODS__;     // módulos com treino, para o treino misto: [{k, tr, nome, ids}]
const TR_BANKS = {};             // trilha -> {id: [questões]} (baixado na primeira vez: treino_<trilha>.json)
const TR_COLOR = { ia: "--t-ia", mat: "--t-mat", ing: "--t-ing" };
const TR_OK = ["Isso!", "Certo!", "Mandou bem!", "Exato!"], TR_NO = ["Quase!", "Não foi dessa vez.", "Ainda não."];
let TR_S = null;

function trEsc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
function trTrack(id) { return String(id || "").split("-")[0]; }
function trTitle(id) {
  if (typeof TOPICS_MAP !== "undefined" && TOPICS_MAP[id]) return TOPICS_MAP[id].title;
  if (typeof RV_TOPICS !== "undefined" && RV_TOPICS[id]) return RV_TOPICS[id][1];
  const row = (window.DS_TOPICS || []).find(r => r[0] === id);
  return row ? row[2] : id;
}
async function trLoadBank(track) {
  if (TR_BANKS[track]) return TR_BANKS[track];
  const r = await fetch("treino_" + track + ".json", { cache: "no-cache" });
  if (!r.ok) throw new Error("erro " + r.status);
  return (TR_BANKS[track] = await r.json());
}
// Aulas que você já começou ou concluiu (para o treino misto)
function trStudied() {
  let pr = {};
  try { pr = JSON.parse(localStorage.getItem("roteiro-ia-v1") || "{}") || {}; } catch (e) {}
  return new Set(Object.keys(pr).filter(id => pr[id] && (pr[id].s === "e" || pr[id].s === "r")));
}

// Realce do Python (o mesmo da Aula Visual; aqui também na página Revisões)
const TR_PY_RE = /(#[^\n]*)|("{3}[\s\S]*?"{3}|'{3}[\s\S]*?'{3}|[fFrRbB]?"(?:\\.|[^"\\\n])*"|[fFrRbB]?'(?:\\.|[^'\\\n])*')|\b(\d+(?:\.\d+)?(?:e-?\d+)?)\b|\b(import|from|as|def|return|for|in|if|elif|else|while|class|with|lambda|and|or|not|is|None|True|False|try|except|finally|raise|yield|pass|break|continue|global|assert|async|await)\b|([A-Za-z_]\w*)(?=\()/g;
function trHL(src) {
  const s = String(src == null ? "" : src);
  let out = "", last = 0, m;
  TR_PY_RE.lastIndex = 0;
  while ((m = TR_PY_RE.exec(s))) {
    out += trEsc(s.slice(last, m.index));
    const cls = m[1] ? "c" : m[2] ? "s" : m[3] ? "n" : m[4] ? "k" : "f";
    out += '<span class="tk-' + cls + '">' + trEsc(m[0]) + "</span>";
    last = TR_PY_RE.lastIndex;
  }
  return out + trEsc(s.slice(last));
}
function trMath(el) {
  if (!window.renderMathInElement) return;
  try {
    window.renderMathInElement(el, { delimiters: [{ left: "$$", right: "$$", display: true }, { left: "$", right: "$", display: false }],
      throwOnError: false, ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "option"] });
  } catch (e) {}
}

// Questão pronta (inst) -> HTML. a = alternativa marcada (null = ainda não respondeu). Também usada na revisão ativa.
function trQHTML(inst, a) {
  const done = a != null, right = done && a === inst.c;
  let h = '<div class="tr-kind">' + TR.KIND[inst.k] + (inst.k === "conta" ? "<small>🎲 números novos a cada vez</small>" : "") + "</div>";
  h += '<div class="tr-q">' + inst.q + "</div>";
  if (inst.k === "erro") {
    h += '<div class="tr-lines">' + inst.lines.map((ln, i) => {
      const cls = done ? (i === inst.c ? " ok" : i === a ? " no" : "") : "";
      return '<button type="button" class="tr-ln' + cls + '" data-o="' + i + '"' + (done || !ln.trim() ? " disabled" : "") + ">" +
             '<span class="tr-n">' + (i + 1) + "</span><code>" + (trHL(ln) || " ") + "</code></button>";
    }).join("") + "</div>";
  } else {
    if (inst.code) {
      let code = trHL(inst.code);
      if (inst.k === "lacuna") {
        const fill = done ? '<span class="tr-gap ok">' + trEsc(inst.opts[inst.c].h) + "</span>" : '<span class="tr-gap">____</span>';
        code = code.replace("____", fill);
      }
      h += '<pre class="tr-code"><code>' + code + "</code></pre>";
    }
    h += '<div class="tr-opts">' + inst.opts.map((o, i) => {
      const cls = done ? (i === inst.c ? " ok" : i === a ? " no" : "") : "";
      const mark = done ? (i === inst.c ? "✓" : i === a ? "✗" : "") : String(i + 1);
      const why = done && o.why && inst.k === "conta" ? '<small class="tr-why">' + o.why + "</small>" : "";
      return '<button type="button" class="tr-opt' + (o.mono ? " mono" : "") + cls + '" data-o="' + i + '"' + (done ? " disabled" : "") + ">" +
             '<span class="tr-r" aria-hidden="true">' + mark + '</span><span class="tr-ot">' + (o.mono ? trEsc(o.h) : o.h) + "</span>" + why + "</button>";
    }).join("") + "</div>";
  }
  if (done) {
    if (inst.m == null) inst.m = Math.floor(Math.random() * 4);
    const head = inst.k === "erro" ? (right ? "Achou! Linha " + (inst.c + 1) + "." : "O erro está na linha " + (inst.c + 1) + ".")
                                   : (right ? TR_OK[inst.m % TR_OK.length] : TR_NO[inst.m % TR_NO.length]);
    h += '<div class="tr-fb ' + (right ? "ok" : "no") + '"><b class="tr-fb-h">' + head + "</b>";
    if (!right && inst.k !== "erro" && inst.k !== "conta" && inst.opts[a] && inst.opts[a].why) h += '<div class="tr-fb-why">' + inst.opts[a].why + "</div>";
    h += "<div>" + inst.x + "</div>";
    if (inst.k === "erro") h += '<code class="tr-fix">✓ ' + trEsc(String(inst.fix).trim()) + "</code>";
    if ((inst.k === "erro" || inst.k === "lacuna") && inst.out != null && inst.out !== "") {
      h += '<div class="tr-out"><span>Saída do programa certo:</span><pre>' + trEsc(inst.out) + "</pre></div>";
    }
    h += "</div>";
  }
  return h;
}

// ---- a janela do treino (criada na primeira vez) ----
function trBox() {
  let el = document.getElementById("tr");
  if (el) return el;
  el = document.createElement("div");
  el.className = "tr"; el.id = "tr"; el.hidden = true;
  el.setAttribute("role", "dialog"); el.setAttribute("aria-modal", "true"); el.setAttribute("aria-labelledby", "tr-title");
  el.innerHTML = '<div class="tr-box"><div class="tr-top"><button type="button" class="tr-x" aria-label="Sair do treino" title="Sair (Esc)">✕</button>' +
    '<b id="tr-title">🏋️ Treino</b><span id="tr-count"></span></div><div class="tr-prog"><i id="tr-bar"></i></div><div class="tr-body" id="tr-body"></div></div>';
  el.querySelector(".tr-x").onclick = () => trClose(true);
  document.body.appendChild(el);
  return el;
}
function trSet(id, v) { const e = document.getElementById(id); if (e) e.textContent = v; }
function trShow(track, title) {
  const el = trBox();
  el.style.setProperty("--tc", "var(" + (TR_COLOR[track] || "--t-hub") + ")");
  el.hidden = false; document.body.classList.add("tr-on");
  trSet("tr-title", title); trSet("tr-count", "");
  document.getElementById("tr-bar").style.width = "0%";
  document.getElementById("tr-body").innerHTML = '<div class="tr-wait">Preparando as questões…</div>';
}
function trClose(ask) {
  const S = TR_S;
  if (ask && S && S.i > 0 && S.i < S.items.length && !confirm("Sair do treino? As questões que você já respondeu não serão contadas.")) return;
  const el = document.getElementById("tr");
  if (el) el.hidden = true;
  document.body.classList.remove("tr-on");
  TR_S = null;
  trPaintEntries();
}

// Treino de uma aula (fim da Aula Visual, menu "⋯ Mais" e página Revisões)
async function trOpenLesson(id) {
  trShow(trTrack(id), "🏋️ Treino");
  let bank;
  try { bank = await trLoadBank(trTrack(id)); }
  catch (e) { document.getElementById("tr-body").innerHTML = '<div class="tr-wait">Não consegui carregar as questões (' + trEsc(e.message) + "). Confira a conexão e tente de novo.</div>"; return; }
  const qs = bank[id] || [];
  if (!qs.length) { document.getElementById("tr-body").innerHTML = '<div class="tr-wait">Esta aula ainda não tem treino.</div>'; return; }
  trBegin({ mode: "one", ids: [id], items: TR.pick(qs).map(q => ({ id, q })) });
}
// Treino misto de um módulo: questões das aulas que você já começou ou concluiu
async function trOpenMixed(key) {
  const m = TR_MODS.find(x => x.k === key);
  if (!m) return;
  trShow(m.tr, "🔀 Treino misto");
  let bank;
  try { bank = await trLoadBank(m.tr); }
  catch (e) { document.getElementById("tr-body").innerHTML = '<div class="tr-wait">Não consegui carregar as questões (' + trEsc(e.message) + ").</div>"; return; }
  const st = trStudied();
  let ids = m.ids.filter(id => st.has(id) && bank[id]), note = "";
  if (!ids.length) { ids = m.ids.filter(id => bank[id]); note = "Você ainda não estudou aulas deste módulo, então o treino usa todas."; }
  trBegin({ mode: "mix", key, ids, note, items: TR.pickMixed(ids.map(id => ({ id, qs: bank[id] }))) });
}
function trBegin(o) {
  const items = o.items.map(it => ({ id: it.id, q: it.q, inst: TR.inst(it.q) })).filter(it => it.inst);
  if (!items.length) { document.getElementById("tr-body").innerHTML = '<div class="tr-wait">Nenhuma questão disponível.</div>'; return; }
  TR_S = Object.assign({}, o, { items, i: 0, answered: null, res: [] });
  trRender();
}

function trRender() {
  const S = TR_S;
  if (!S) return;
  if (S.i >= S.items.length) return trResult();
  const it = S.items[S.i], ok = S.res.filter(Boolean).length;
  trSet("tr-count", (S.i + 1) + " de " + S.items.length + (ok ? " · ✔ " + ok : ""));
  document.getElementById("tr-bar").style.width = (S.i / S.items.length * 100) + "%";
  let h = "";
  if (S.note && S.i === 0) h += '<p class="tr-note">' + trEsc(S.note) + "</p>";
  h += '<div class="tr-chip" style="--c:var(' + (TR_COLOR[trTrack(it.id)] || "--t-hub") + ')"><i></i><span>' + trEsc(trTitle(it.id)) + "</span>" +
       (S.mode === "redo" ? "<small>refazendo as que errou</small>" : "") + "</div>";
  h += '<div class="tr-card">' + trQHTML(it.inst, S.answered) + "</div>";
  h += S.answered == null ? '<p class="tr-tip">' + (it.inst.k === "erro" ? "Toque na linha com o erro (ou tecle o número dela)." : "Toque na resposta (ou tecle o número).") + "</p>"
    : '<div class="tr-actions"><button type="button" class="tr-btn pri" data-next>' + (S.i + 1 < S.items.length ? "Próxima →" : "Ver resultado") + "</button></div>";
  const body = document.getElementById("tr-body");
  body.innerHTML = h; body.scrollTop = 0; trMath(body);
  body.querySelectorAll("[data-o]").forEach(b => { b.onclick = () => trAnswer(+b.dataset.o); });
  const nx = body.querySelector("[data-next]");
  if (nx) { nx.onclick = trNext; try { nx.focus({ preventScroll: true }); } catch (e) {} }
}
// A alternativa i existe? (no "Ache o erro", linha em branco não conta)
function trCanAnswer(inst, i) { return inst.k === "erro" ? !!String(inst.lines[i] || "").trim() : !!inst.opts[i]; }
function trAnswer(i) {
  const S = TR_S;
  if (!S || S.answered != null) return;
  const inst = S.items[S.i].inst;
  if (!trCanAnswer(inst, i)) return;
  S.answered = i; S.res[S.i] = i === inst.c;
  trRender();
}
function trNext() { if (!TR_S) return; TR_S.i++; TR_S.answered = null; trRender(); }

function trResult() {
  const S = TR_S, body = document.getElementById("tr-body");
  const ok = S.res.filter(Boolean).length, n = S.items.length, pct = n ? Math.round(ok / n * 100) : 0;
  trSet("tr-count", "Resultado");
  document.getElementById("tr-bar").style.width = "100%";
  // Só o treino completo de uma aula grava o resultado dela: refazer as erradas ou o misto (1 ou 2 questões por aula)
  // não são comparáveis com o treino de 10 questões e mudariam o "seu melhor" à toa
  if (!S.saved && S.mode === "one") {
    S.saved = true; S.prev = {};
    S.ids.forEach(id => {
      const idx = S.items.map((it, i) => (it.id === id ? i : -1)).filter(i => i >= 0);
      if (idx.length) S.prev[id] = TR.record(id, idx.filter(i => S.res[i]).length, idx.length).prev;
    });
    if (typeof scheduleAwsRealtimeSync === "function") { try { scheduleAwsRealtimeSync(); } catch (e) {} }
    try { window.dispatchEvent(new CustomEvent("tr:change")); } catch (e) {}
  }
  const miss = S.items.filter((_, i) => !S.res[i]);
  const msg = pct === 100 ? "Gabaritou! 🏆" : pct >= 80 ? "Mandou bem!" : pct >= 60 ? "Bom treino! Vale rever os erros abaixo." : "Esse custou, e tudo bem: é errando aqui que você acerta depois.";
  let h = '<div class="tr-end"><div class="tr-score">' + ok + "/" + n + '</div><p class="tr-msg">' + msg + "</p>";
  if (S.mode === "one" && S.prev && S.prev[S.ids[0]]) h += '<p class="tr-sub">Antes, seu melhor nesta aula era ' + S.prev[S.ids[0]].b + "%.</p>";
  const bk = TR.byKind(S.items, S.res);
  h += '<div class="tr-chips">' + Object.keys(bk).map(k => '<span class="tr-chip2">' + TR.ICON[k] + " " + TR.SHORT[k] + " " + bk[k][0] + "/" + bk[k][1] + "</span>").join("") + "</div>";
  if (S.mode === "mix") {
    h += '<div class="tr-rows">' + S.ids.filter(id => S.items.some(it => it.id === id)).map(id => {
      const idx = S.items.map((it, i) => (it.id === id ? i : -1)).filter(i => i >= 0), a = idx.filter(i => S.res[i]).length;
      return '<div class="tr-row"><span>' + trEsc(trTitle(id)) + "</span><b>" + a + "/" + idx.length + "</b></div>";
    }).join("") + "</div>";
  }
  if (miss.length) {
    h += '<div class="tr-miss"><b>Para rever (' + miss.length + "):</b><ul>" + miss.map(it => "<li>" + trEsc(TR.labelOf(it.q)) +
         (S.mode === "mix" ? ' <small>· ' + trEsc(trTitle(it.id)) + "</small>" : "") + "</li>").join("") + "</ul></div>";
  }
  h += '<div class="tr-actions wrap">';
  if (miss.length) h += '<button type="button" class="tr-btn pri" data-redo>Refazer só as ' + miss.length + (miss.length === 1 ? " que errei" : " que errei") + "</button>";
  h += '<button type="button" class="tr-btn' + (miss.length ? "" : " pri") + '" data-again>Treinar de novo</button>';
  const id1 = S.ids.length === 1 ? S.ids[0] : null, ag = id1 && typeof RV !== "undefined" ? RV.byId()[id1] : null;
  if (id1 && typeof RV !== "undefined" && pct < 80 && !ag) h += '<button type="button" class="tr-btn" data-rev>↻ Pôr na revisão</button>';
  h += '<button type="button" class="tr-btn" data-close>Fechar</button></div>';
  if (id1 && ag) h += '<p class="tr-sub">↻ Esta aula já está na sua agenda de revisões: ' + trEsc(RV.when(ag.due)) + ".</p>";
  h += "</div>";
  body.innerHTML = h; body.scrollTop = 0; trMath(body);
  const on = (sel, fn) => { const b = body.querySelector(sel); if (b) b.onclick = fn; };
  const base = S.from || S.mode;   // de onde veio (uma aula ou misto), também ao refazer as erradas
  on("[data-redo]", () => trBegin({ mode: "redo", from: base, key: S.key, ids: S.ids, items: miss.map(it => ({ id: it.id, q: it.q })) }));
  on("[data-again]", () => (base === "mix" ? trOpenMixed(S.key) : trOpenLesson(S.ids[0])));
  on("[data-rev]", () => {
    RV.schedule(id1, RV.addDays(RV.today(), 1));
    if (typeof rvToast === "function") rvToast("Revisão marcada para amanhã.");
    if (typeof rvNavBadge === "function") rvNavBadge();
    const b = body.querySelector("[data-rev]"); if (b) { b.disabled = true; b.textContent = "✓ Na revisão de amanhã"; }
  });
  on("[data-close]", () => trClose(false));
}

// Cartão "Treinar esta aula" (fim da Aula Visual)
function trEntryHTML(id) {
  const n = TR_INDEX[id];
  if (!n) return "";
  const st = TR.stats(id), k = Math.min(n, TR.PER_SESSION);
  const sub = st ? "Seu melhor: " + st.b + "% · última vez " + trEsc(st.s) + " · treinou " + st.n + (st.n === 1 ? " vez" : " vezes")
                 : "Questões de marcar, com a explicação na hora. Não mexe no seu progresso nem nos pontos.";
  return '<div class="tr-entry" data-tr="' + id + '"><span class="tr-entry-ico" aria-hidden="true">🏋️</span><div class="tr-entry-t"><b>Treinar esta aula · ' + k +
         " questões</b><span>" + sub + '</span></div><button type="button" class="tr-entry-go" onclick="trOpenLesson(\'' + id + '\')">' +
         (st ? "Treinar de novo" : "Começar") + "</button></div>";
}
function trPaintEntries() {
  document.querySelectorAll(".tr-entry[data-tr]").forEach(el => {
    const html = trEntryHTML(el.dataset.tr);
    if (html) el.outerHTML = html;
  });
}

// Teclado: na fase de captura, para o Esc do treino não fechar também a aula que está por baixo
window.addEventListener("keydown", e => {
  const el = document.getElementById("tr"), S = TR_S;
  if (!el || el.hidden) return;
  if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); trClose(true); return; }
  if (!S || S.i >= S.items.length || (e.target.closest && e.target.closest("input,textarea"))) return;
  if (S.answered == null && /^[1-9]$/.test(e.key)) { e.preventDefault(); e.stopPropagation(); trAnswer(+e.key - 1); }
  else if (S.answered != null && (e.key === "Enter" || e.key === " ")) {
    e.stopPropagation();
    if (!(e.target.closest && e.target.closest("button"))) { e.preventDefault(); trNext(); }   // num botão, o próprio clique resolve
  }
}, true);
"""

TR_CSS = r"""
/* ===== Treino (questões de marcar) ===== */
/* .tr = a janela do treino; .tr-in = uma questão do treino dentro de outra tela (cartão da revisão ativa) */
.tr,.tr-in{--tc:var(--t-hub);--code-bg:#0b1218;--code-line:rgba(148,178,190,.14);--code-tx:#d6dee1;
  --code-c:#6f8590;--code-s:#9fdcae;--code-n:#f2b872;--code-k:#c8a8ff;--code-f:#7fc8f8}
:root[data-theme="light"] .tr,:root[data-theme="light"] .tr-in{--code-bg:#f6f8fa;--code-line:#e1e7eb;--code-tx:#1f2b31;--code-c:#6e7f88;--code-s:#116329;--code-n:#a04f00;--code-k:#7c3aed;--code-f:#0550ae}
.tr{position:fixed;inset:0;z-index:99995;display:flex;align-items:center;justify-content:center;padding:18px;
  background:color-mix(in srgb,var(--bg) 84%,transparent);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.tr[hidden]{display:none}
body.tr-on{overflow:hidden}
.tr-box{width:min(680px,100%);max-height:100%;display:flex;flex-direction:column;border:1px solid var(--bd);border-radius:22px;
  background:var(--card);color:var(--tx);box-shadow:0 40px 100px rgba(0,0,0,.5);overflow:hidden;font-size:15px;line-height:1.55}
.tr-top{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:12px 16px}
.tr-top b{font-size:.95rem}
.tr-x{width:36px;height:36px;border-radius:50%;border:1px solid var(--bd);background:transparent;color:var(--tx);cursor:pointer;font:inherit}
.tr-top span{min-width:36px;text-align:right;color:var(--mu);font-size:.82rem;font-variant-numeric:tabular-nums;white-space:nowrap}
.tr-prog{height:4px;background:var(--bd)}
.tr-prog i{display:block;height:100%;width:0;background:var(--tc);box-shadow:0 0 10px var(--tc);transition:width .25s}
.tr-body{padding:16px 20px 22px;overflow:auto}
.tr-wait{padding:40px 10px;text-align:center;color:var(--mu);line-height:1.6}
.tr-note{margin:0 0 10px;padding:8px 12px;border-radius:10px;background:color-mix(in srgb,var(--tc) 10%,transparent);font-size:.84rem;color:var(--mu)}
.tr-chip{display:flex;align-items:center;gap:8px;margin-bottom:10px;font-size:.8rem;color:var(--mu)}
.tr-chip i{flex:none;width:8px;height:8px;border-radius:50%;background:var(--c)}
.tr-chip span{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tr-chip small{margin-left:auto;flex:none;font-size:.72rem}
.tr-card{padding:16px;border-radius:18px;border:1px solid color-mix(in srgb,var(--tc) 28%,var(--bd));
  background:linear-gradient(180deg,color-mix(in srgb,var(--tc) 7%,var(--card)),var(--card))}
.tr-kind{display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;font-size:.74rem;font-weight:800;letter-spacing:.04em;color:var(--tc)}
.tr-kind small{font-weight:600;letter-spacing:0;color:var(--mu)}
.tr-q{margin-top:8px;font-size:1.02rem;font-weight:650;line-height:1.5}
.tr-q code,.tr-fb code:not(.tr-fix),.tr-opt:not(.mono) code{background:rgba(74,92,106,.25);padding:1px 5px;border-radius:4px;font-size:.88em}
.tr-code{margin:12px 0 0;padding:12px 14px;background:var(--code-bg);color:var(--code-tx);border:1px solid var(--code-line);border-radius:10px;
  font:13.5px/1.6 ui-monospace,"JetBrains Mono","Cascadia Code",SFMono-Regular,Consolas,monospace;overflow-x:auto;tab-size:4}
.tr-code code{background:none;padding:0;white-space:pre;font:inherit;color:inherit}
:is(.tr,.tr-in) .tk-c{color:var(--code-c);font-style:italic}:is(.tr,.tr-in) .tk-s{color:var(--code-s)}:is(.tr,.tr-in) .tk-n{color:var(--code-n)}
:is(.tr,.tr-in) .tk-k{color:var(--code-k);font-weight:500}:is(.tr,.tr-in) .tk-f{color:var(--code-f)}
.tr-gap{display:inline-block;min-width:4.5ch;padding:0 4px;border-bottom:2px dashed var(--tc);color:var(--tc);text-align:center}
.tr-gap.ok{border-bottom-style:solid;border-color:#2fa36b;color:#2fa36b;font-weight:700}
.tr-opts{display:flex;flex-direction:column;gap:8px;margin-top:14px}
.tr-opt{display:flex;align-items:center;gap:10px;width:100%;padding:10px 12px;border-radius:12px;border:1px solid var(--bd);background:var(--bg);
  color:var(--tx);font:inherit;font-size:.93rem;text-align:left;cursor:pointer;line-height:1.45}
.tr-opt.mono .tr-ot{font:13.5px/1.5 ui-monospace,"JetBrains Mono",Consolas,monospace;white-space:pre-wrap}
.tr-opt:hover:not([disabled]){border-color:var(--tc)}
.tr-opt[disabled]{cursor:default}
.tr-r{flex:none;width:22px;height:22px;border-radius:50%;border:2px solid var(--bd);display:grid;place-items:center;font:700 .7rem/1 Inter,system-ui;color:var(--mu)}
.tr-ot{min-width:0;overflow-wrap:anywhere}
.tr-why{margin-left:auto;padding-left:8px;font-size:.74rem;color:var(--mu);text-align:right}
.tr-opt.ok{border-color:#2fa36b;background:color-mix(in srgb,#2fa36b 14%,var(--bg))}
.tr-opt.ok .tr-r{border-color:#2fa36b;background:#2fa36b;color:#06221a}
.tr-opt.no{border-color:#ef6b5b;background:color-mix(in srgb,#ef6b5b 12%,var(--bg))}
.tr-opt.no .tr-r{border-color:#ef6b5b;background:#ef6b5b;color:#2a0808}
.tr-lines{margin-top:12px;border:1px solid var(--code-line);border-radius:10px;overflow:hidden;background:var(--code-bg)}
.tr-ln{display:flex;align-items:baseline;gap:10px;width:100%;padding:6px 12px;border:0;border-top:1px solid var(--code-line);background:transparent;
  color:var(--code-tx);font:13.5px/1.55 ui-monospace,"JetBrains Mono",Consolas,monospace;text-align:left;cursor:pointer}
.tr-ln:first-child{border-top:0}
.tr-ln code{background:none;padding:0;white-space:pre;font:inherit;color:inherit;overflow-x:auto}
.tr-ln:hover:not([disabled]){background:color-mix(in srgb,var(--tc) 12%,transparent)}
.tr-ln[disabled]{cursor:default}
.tr-n{flex:none;width:18px;text-align:right;color:var(--code-c);font-size:.78rem}
.tr-ln.ok{background:color-mix(in srgb,#2fa36b 18%,transparent);box-shadow:inset 3px 0 0 #2fa36b}
.tr-ln.no{background:color-mix(in srgb,#ef6b5b 16%,transparent);box-shadow:inset 3px 0 0 #ef6b5b}
.tr-fb{margin-top:14px;padding:11px 13px;border-radius:12px;border:1px solid var(--bd);background:var(--bg);font-size:.9rem;line-height:1.6}
.tr-fb.ok{border-color:color-mix(in srgb,#2fa36b 50%,var(--bd))}.tr-fb.no{border-color:color-mix(in srgb,#ef6b5b 50%,var(--bd))}
.tr-fb-h{display:block;margin-bottom:3px}.tr-fb.ok .tr-fb-h{color:#2fa36b}.tr-fb.no .tr-fb-h{color:#ef6b5b}
.tr-fb-why{margin-bottom:6px;color:var(--mu)}
.tr-fb ol,.tr-fb ul{margin:.3em 0 0;padding-left:1.3em}
.tr-fix{display:block;margin-top:8px;padding:6px 10px;border-radius:8px;background:color-mix(in srgb,#2fa36b 12%,transparent);color:#2fa36b;
  font:13px/1.5 ui-monospace,Consolas,monospace;white-space:pre-wrap}
.tr-out{margin-top:8px;font-size:.8rem;color:var(--mu)}
.tr-out pre{margin:4px 0 0;padding:6px 10px;border-radius:8px;background:var(--code-bg);color:var(--code-tx);font:12.5px/1.5 ui-monospace,Consolas,monospace;white-space:pre-wrap}
.tr-tip{margin:12px 0 0;text-align:center;font-size:.8rem;color:var(--mu)}
.tr-actions{display:flex;justify-content:center;gap:8px;margin-top:16px}
.tr-actions.wrap{flex-wrap:wrap}
.tr-btn{display:inline-flex;align-items:center;gap:8px;min-height:42px;padding:9px 18px;border-radius:99px;border:1px solid var(--bd);
  background:transparent;color:var(--tx);font:inherit;font-weight:700;cursor:pointer}
.tr-btn.pri{background:var(--tc);border-color:var(--tc);color:#04121a}
.tr-btn[disabled]{opacity:.7;cursor:default}
.tr-end{text-align:center}
.tr-score{font-size:2.6rem;font-weight:800;letter-spacing:-.03em;line-height:1.1;margin-top:6px}
.tr-msg{margin:6px 0 0;font-weight:650}
.tr-sub{margin:6px 0 0;font-size:.84rem;color:var(--mu)}
.tr-chips{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin:12px 0 4px}
.tr-chip2{font-size:.74rem;font-weight:700;padding:3px 10px;border-radius:99px;border:1px solid var(--bd);color:var(--mu)}
.tr-rows{margin:10px 0 0;text-align:left;font-size:.86rem}
.tr-row{display:flex;justify-content:space-between;gap:10px;padding:6px 0;border-top:1px solid var(--bd)}
.tr-miss{margin-top:12px;padding-top:10px;border-top:1px solid var(--bd);text-align:left;font-size:.86rem}
.tr-miss ul{margin:4px 0 0;padding-left:1.2em;color:var(--mu)}
.tr-miss small{color:var(--mu)}
/* Cartão "Treinar esta aula" (fim da Aula Visual) e treino misto (página Revisões) */
.tr-entry{display:flex;align-items:center;gap:12px;margin:2px 0;padding:12px 14px;border-radius:14px;border:1px dashed color-mix(in srgb,var(--t,var(--t-hub)) 55%,transparent);
  background:color-mix(in srgb,var(--t,var(--t-hub)) 7%,transparent)}
.tr-entry-ico{font-size:1.5rem;flex:none}
.tr-entry-t{min-width:0;flex:1}
.tr-entry-t b{display:block;font-size:.93rem}
.tr-entry-t span{display:block;font-size:.8rem;color:var(--mu);line-height:1.45}
.tr-entry-go{flex:none;padding:8px 14px;border-radius:99px;border:1px solid var(--t,var(--t-hub));background:var(--t,var(--t-hub));color:#04121a;font:inherit;font-weight:700;font-size:.84rem;cursor:pointer}
@media (max-width:600px){.tr{padding:0}.tr-box{height:100%;max-height:none;border-radius:0;border:0}.tr-body{padding:12px 12px 20px}
  .tr-card{padding:13px}.tr-q{font-size:.97rem}.tr-entry{flex-wrap:wrap}.tr-entry-go{width:100%}}
"""
