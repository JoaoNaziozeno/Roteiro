# -*- coding: utf-8 -*-
"""
Blocos da Aula Visual para as trilhas de IA e Inglês.

Programação
  - "codigo"  : editor de Python que roda no próprio navegador (Pyodide, num Web Worker),
                com testes automáticos, dicas e solução. Laço infinito? O worker é encerrado
                depois de alguns segundos e a aula explica o que aconteceu.
  - "parsons" : montar o código (ou a frase) colocando as linhas na ordem certa.
  - "palpite" com "codigo": "preveja a saída" (tratado no renderizador principal).

Idiomas
  - "dialogo" : conversa com áudio por fala (voz do próprio navegador) e tradução sob demanda.
  - "ouvir"   : escute e escolha / ditado.
  - "falar"   : fale a frase e o navegador transcreve e compara (Chrome e Edge).
  - "vocab"   : cartões de vocabulário que viram e marcam o que você já domina.

Laboratórios novos: "logistica" (regressão logística) e "atencao" (mapa de atenção).
Tudo que o aluno faz é salvo com lv2SaveAnswer (vai para a nuvem junto com o progresso).
"""

EXTRA_JS = r"""
// =========================================================================
// BLOCOS NOVOS: IA (código executável) e Inglês (ouvir, falar, vocabulário)
// =========================================================================
Object.assign(LV2_META, {
  codigo:  { icon: "", label: "Mão no código" },
  parsons: { icon: "", label: "Monte na ordem certa" },
  dialogo: { icon: "", label: "Situação real" },
  ouvir:   { icon: "", label: "Ouça e responda" },
  falar:   { icon: "", label: "Fale e compare" },
  vocab:   { icon: "", label: "Vocabulário da aula" }
});

const lv2Attr = s => lv2Esc(s).replace(/"/g, "&quot;");
const LV2_SPECS = {};      // dados de cada bloco interativo, por id (evita JSON em atributos)

// ---------------------------------------------------------------- voz (TTS)
let lv2Voice = null;
function lv2PickVoice() {
  if (!("speechSynthesis" in window)) return null;
  const vs = speechSynthesis.getVoices();
  return vs.find(v => /^en[-_]US/i.test(v.lang) && /Google|Natural|Aria|Jenny|Samantha|Guy/i.test(v.name)) ||
         vs.find(v => /^en[-_]US/i.test(v.lang)) || vs.find(v => /^en/i.test(v.lang)) || null;
}
if ("speechSynthesis" in window) { lv2Voice = lv2PickVoice(); speechSynthesis.onvoiceschanged = () => { lv2Voice = lv2PickVoice(); }; }
function lv2Speak(texts, rate) {
  if (!("speechSynthesis" in window)) { if (typeof showToast === "function") showToast("Seu navegador não tem voz sintetizada."); return; }
  speechSynthesis.cancel();
  if (!lv2Voice) lv2Voice = lv2PickVoice();
  // Sem voz em inglês instalada, o navegador leria com sotaque de português: avisa o aluno uma vez
  if (!lv2Voice && speechSynthesis.getVoices().length && !lv2Speak.warned) {
    lv2Speak.warned = true;
    if (typeof showToast === "function") showToast("Seu navegador não tem voz em inglês. Use o Chrome ou o Edge, ou instale a fala em inglês no Windows (Configurações › Hora e idioma › Fala).");
  }
  (Array.isArray(texts) ? texts : [texts]).forEach(t => {
    const u = new SpeechSynthesisUtterance(String(t).replace(/<[^>]+>/g, ""));
    u.lang = "en-US"; u.rate = rate || 0.95;
    if (lv2Voice) u.voice = lv2Voice;
    speechSynthesis.speak(u);
  });
}
const lv2SayBtn = (text, label) => `<button type="button" class="lv2-say" data-lv2x="say" data-text="${lv2Attr(text)}" aria-label="Ouvir em inglês" title="Ouvir">${label || "🔊"}</button>`;
// apóstrofo é ignorado: "what's" e "whats" contam como a mesma palavra
const lv2Norm = s => String(s).toLowerCase().replace(/[’']/g, "").replace(/[^a-z0-9 ]+/g, " ").replace(/\s+/g, " ").trim();

// Compara palavras: quais da frase esperada apareceram no que foi dito/escrito
function lv2WordDiff(expected, got) {
  const exp = lv2Norm(expected).split(" ").filter(Boolean), have = lv2Norm(got).split(" ").filter(Boolean);
  const pool = have.slice();
  let hits = 0;
  const html = exp.map(w => { const k = pool.indexOf(w); if (k >= 0) { pool.splice(k, 1); hits++; return `<span class="lv2-w-ok">${w}</span>`; } return `<span class="lv2-w-miss">${w}</span>`; }).join(" ");
  return { pct: exp.length ? Math.round(100 * hits / exp.length) : 0, html, exact: lv2Norm(expected) === lv2Norm(got) };
}

// ---------------------------------------------------------------- Python no navegador (Pyodide em Web Worker)
const LV2_PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js";
const LV2_PY_WORKER = [
  'importScripts("' + LV2_PYODIDE + '");',
  "let py = null;",
  "const last = e => { const t = String(e && e.message || e).trim().split('\\n').filter(Boolean); return t.slice(-1)[0] || 'Erro'; };",
  "const tb = e => { const t = String(e && e.message || e).trim().split('\\n').filter(Boolean); const k = t.findIndex(l => l.includes('File \"<exec>\"')); return (k >= 0 ? t.slice(k) : t.slice(-3)).join('\\n'); };",
  "self.onmessage = async (ev) => {",
  "  const m = ev.data;",
  "  try {",
  "    if (!py) py = await loadPyodide();",
  "    if (m.boot) { self.postMessage({ id: m.id, ok: true }); return; }",
  "    let out = '';",
  "    py.setStdout({ batched: s => { out += s + '\\n'; } });",
  "    py.setStderr({ batched: s => { out += s + '\\n'; } });",
  "    try { await py.loadPackagesFromImports(m.code); } catch (_) {}",
  "    const ns = py.globals.get('dict')();",
  "    let err = null;",
  "    try { await py.runPythonAsync(m.code, { globals: ns, filename: '<exec>' }); } catch (e) { err = tb(e); }",
  "    const results = [];",
  "    if (!err) for (const t of (m.tests || [])) {",
  "      try { ns.set('saida', out); await py.runPythonAsync(t.codigo, { globals: ns }); results.push({ nome: t.nome, ok: true }); }",
  "      catch (e) { results.push({ nome: t.nome, ok: false, msg: last(e).replace(/^AssertionError:?\\s*/, '') }); }",
  "    }",
  "    ns.destroy();",
  "    self.postMessage({ id: m.id, ok: true, out, err, results });",
  "  } catch (e) { self.postMessage({ id: m.id, ok: false, err: String(e && e.message || e) }); }",
  "};"
].join("\n");
let lv2PyW = null, lv2PyReady = false, lv2PySeq = 0;
const lv2PyPend = {};
function lv2PyWorker() {
  if (lv2PyW) return lv2PyW;
  lv2PyW = new Worker(URL.createObjectURL(new Blob([LV2_PY_WORKER], { type: "text/javascript" })));
  lv2PyW.onmessage = e => { const cb = lv2PyPend[e.data.id]; if (cb) { delete lv2PyPend[e.data.id]; cb(e.data); } };
  lv2PyW.onerror = e => { Object.keys(lv2PyPend).forEach(k => { lv2PyPend[k]({ ok: false, err: "Não foi possível carregar o Python (" + (e.message || "sem internet?") + ")." }); delete lv2PyPend[k]; }); lv2PyW = null; lv2PyReady = false; };
  return lv2PyW;
}
function lv2PyCall(msg, timeoutMs) {
  return new Promise(res => {
    const id = ++lv2PySeq, w = lv2PyWorker();
    let done = false;
    const t = setTimeout(() => {
      if (done) return; done = true; delete lv2PyPend[id];
      try { w.terminate(); } catch (_) {}
      lv2PyW = null; lv2PyReady = false;
      res({ ok: false, timeout: true });
    }, timeoutMs);
    lv2PyPend[id] = d => { if (done) return; done = true; clearTimeout(t); res(d); };
    w.postMessage(Object.assign({ id }, msg));
  });
}
async function lv2PyRun(code, tests, status) {
  if (!lv2PyReady) {
    status("Carregando o Python no navegador (só na primeira vez, ~10 MB)...");
    const b = await lv2PyCall({ boot: true }, 120000);
    if (!b.ok) return b.timeout ? { ok: false, err: "O Python demorou demais para carregar. Verifique a internet e tente de novo." } : b;
    lv2PyReady = true;
  }
  status("Rodando...");
  return lv2PyCall({ code, tests }, 8000);
}

// ---------------------------------------------------------------- renderizadores
const LV2_EXTRA = {
  codigo(b, i) {
    const id = `py-${i}`;
    LV2_SPECS[id] = { inicial: b.inicial || "", testes: b.testes || [] };
    const rows = Math.min(18, Math.max(5, (b.inicial || "").split("\n").length + 2));
    let h = b.enunciado ? `<div class="lv2-q">${b.enunciado}</div>` : "";
    h += `<div class="lv2-py" data-py="${id}">` +
      `<div class="lv2-py-bar"><span class="lv2-py-lang">Python</span><span class="lv2-py-status"></span></div>` +
      `<textarea class="lv2-py-ed" spellcheck="false" autocapitalize="off" autocomplete="off" rows="${rows}" aria-label="Editor de código Python">${lv2Esc(b.inicial || "")}</textarea>` +
      `<div class="lv2-py-actions"><button type="button" class="lv2-btn" data-lv2x="py-run">▶ Rodar</button>` +
      ((b.testes || []).length ? `<button type="button" class="lv2-btn lv2-btn-main" data-lv2x="py-check">✓ Verificar</button>` : "") +
      `<button type="button" class="lv2-btn lv2-btn-ghost" data-lv2x="py-reset" title="Voltar ao código inicial">↺ Recomeçar</button></div>` +
      `<pre class="lv2-py-out" hidden></pre><div class="lv2-py-tests"></div></div>`;
    (b.dicas || []).forEach((d, j) => { h += `<details><summary>Dica ${j + 1}</summary><div>${d}</div></details>`; });
    if (b.solucao) h += `<details><summary>Ver uma solução</summary><div><pre class="lv2-code"><code>${lv2HighlightPy(b.solucao)}</code></pre>${b.explicacao || ""}</div></details>`;
    return h;
  },

  parsons(b, i) {
    const id = `ps-${i}`, lines = b.linhas || [];
    LV2_SPECS[id] = { linhas: lines };
    // embaralha de forma estável (sempre na mesma ordem para a mesma aula), nunca na ordem certa
    let order = lines.map((_, k) => k), seed = 7 + i * 13;
    for (let k = order.length - 1; k > 0; k--) { seed = (seed * 9301 + 49297) % 233280; const j = Math.floor(seed / 233280 * (k + 1)); [order[k], order[j]] = [order[j], order[k]]; }
    if (order.every((v, k) => v === k) && order.length > 1) order.push(order.shift());
    const isCode = b.modo !== "frase";
    return `<ol class="lv2-ps ${isCode ? "is-code" : "is-words"}" data-ps="${id}">` + order.map(k =>
      `<li class="lv2-ps-line" data-k="${k}"><span class="lv2-ps-txt">${isCode ? lv2HighlightPy(lines[k]) : lv2Esc(lines[k])}</span>` +
      `<span class="lv2-ps-btns"><button type="button" data-lv2x="ps-up" aria-label="Subir">↑</button><button type="button" data-lv2x="ps-down" aria-label="Descer">↓</button></span></li>`).join("") +
      `</ol><div class="lv2-wbtns"><button type="button" class="lv2-btn lv2-btn-main" data-lv2x="ps-check">Conferir a ordem</button></div><div class="lv2-ps-msg"></div>` +
      (b.explicacao ? `<details><summary>Ver a explicação</summary><div>${b.explicacao}</div></details>` : "");
  },

  dialogo(b, i) {
    const falas = b.falas || [], a = falas.length ? falas[0].quem : "";
    LV2_SPECS[`dl-${i}`] = falas.map(f => f.en);
    return `<div class="lv2-dlg" data-dl="dl-${i}">` + falas.map(f =>
      `<div class="lv2-dlg-row" data-side="${f.quem === a ? "a" : "b"}"><div class="lv2-dlg-who">${f.quem}</div>` +
      `<div class="lv2-dlg-bubble">${lv2SayBtn(f.en)}<div><div class="lv2-dlg-en">${f.en}</div><div class="lv2-dlg-pt" hidden>${f.pt || ""}</div></div></div></div>`).join("") +
      `</div><div class="lv2-wbtns"><button type="button" class="lv2-btn lv2-btn-main" data-lv2x="dlg-all">▶ Ouvir a conversa</button>` +
      `<button type="button" class="lv2-btn" data-lv2x="dlg-slow">🐢 Mais devagar</button><button type="button" class="lv2-btn" data-lv2x="dlg-pt">Mostrar tradução</button></div>`;
  },

  ouvir(b, i) {
    return `<div class="lv2-listen">` + (b.itens || []).map((it, k) => {
      const head = `<div class="lv2-lis-head"><span class="lv2-ex-n">${k + 1}</span>${lv2SayBtn(it.frase, "🔊 Ouvir")}${lv2SayBtn(it.frase, "🐢")}` +
        (it.dica ? `<span class="lv2-lis-hint">${it.dica}</span>` : "") + `</div>`;
      if (it.opcoes) {
        return `<div class="lv2-lis" data-lis="${k}">${head}<div class="lv2-opts">` + it.opcoes.map((o, j) =>
          `<button type="button" class="lv2-opt" data-lv2x="lis-opt" data-j="${j}" data-ok="${j === it.correta ? 1 : 0}">${o}</button>`).join("") +
          `</div><div class="lv2-lis-reveal" hidden>Áudio: <b>${it.frase}</b>${it.pt ? ` <span class="lv2-muted">(${it.pt})</span>` : ""}</div></div>`;
      }
      return `<div class="lv2-lis" data-lis="${k}" data-frase="${lv2Attr(it.frase)}">${head}<div class="lv2-dictbox"><input type="text" class="lv2-dict" aria-label="Escreva o que ouviu" placeholder="escreva o que ouviu" autocapitalize="off" spellcheck="false">` +
        `<button type="button" class="lv2-btn" data-lv2x="lis-dict">Conferir</button></div><div class="lv2-lis-res"></div></div>`;
    }).join("") + `</div>`;
  },

  falar(b, i) {
    const ok = "webkitSpeechRecognition" in window || "SpeechRecognition" in window;
    return (ok ? "" : `<div class="lv2-note">Seu navegador não reconhece fala (funciona no Chrome e no Edge). Você ainda pode ouvir o modelo e repetir em voz alta.</div>`) +
      `<div class="lv2-speak">` + (b.frases || []).map((f, k) =>
        `<div class="lv2-spk" data-spk="${k}" data-frase="${lv2Attr(f.en)}"><div class="lv2-spk-en">${f.en}</div>` +
        (f.pt ? `<div class="lv2-spk-pt">${f.pt}</div>` : "") +
        `<div class="lv2-spk-btns">${lv2SayBtn(f.en, "🔊 Modelo")}${lv2SayBtn(f.en, "🐢")}` +
        (ok ? `<button type="button" class="lv2-btn lv2-btn-main" data-lv2x="spk">🎙 Falar</button>` : "") +
        `</div><div class="lv2-spk-res"></div></div>`).join("") + `</div>`;
  },

  vocab(b, i) {
    const cards = b.cartoes || [];
    return `<div class="lv2-vocab" data-vc="${i}">` + cards.map((c, k) =>
      `<div class="lv2-card" data-k="${k}"><button type="button" class="lv2-card-face" data-lv2x="vc-flip" aria-label="Virar cartão">` +
      `<span class="lv2-card-en">${c.en}</span><span class="lv2-card-back" hidden><span class="lv2-card-pt">${c.pt}</span>${c.ex ? `<span class="lv2-card-ex">${c.ex}</span>` : ""}</span></button>` +
      `<div class="lv2-card-foot">${lv2SayBtn(c.ex || c.en)}<button type="button" class="lv2-card-mark" data-lv2x="vc-know" data-v="1">Já sei</button><button type="button" class="lv2-card-mark" data-lv2x="vc-know" data-v="0">Rever</button></div></div>`).join("") +
      `</div><div class="lv2-vc-sum"></div>`;
  }
};

// ---------------------------------------------------------------- laboratórios novos
Object.assign(LV2_WIDGETS, {
  // Regressão logística: horas de estudo -> chance de passar. Ajuste w e b ou deixe o gradiente ajustar.
  logistica(el) {
    const D = [[0.5,0],[1,0],[1.5,0],[2,0],[2.5,1],[3,0],[3.5,0],[4,1],[4.5,0],[5,1],[5.5,1],[6,0],[6.5,1],[7,1],[8,1],[9,1]];
    const W = 340, H = 220, P = 26, X = x => P + x / 10 * (W - 2 * P), Y = y => H - P - y * (H - 2 * P);
    const sig = z => 1 / (1 + Math.exp(-z));
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" class="lv2-wsvg" role="img" aria-label="Curva logística sobre os dados"></svg>` +
      `<div class="lv2-wctl">${lv2Slider("w", "w (inclinação)", -3, 3, 0.5, 0.1)}${lv2Slider("b", "b (deslocamento)", -10, 10, -1, 0.1)}${lv2Slider("t", "limiar de decisão", 0.1, 0.9, 0.5, 0.05)}</div>` +
      `<div class="lv2-wbtns"><button type="button" class="lv2-btn" data-lg="fit">Deixar o gradiente ajustar</button></div><div class="lv2-wout"></div>`;
    const svg = el.querySelector("svg"), out = el.querySelector(".lv2-wout");
    let cur = null;
    const draw = o => {
      cur = o;
      let g = "";
      for (let y = 0; y <= 1.0001; y += 0.25) g += `<line x1="${P}" y1="${Y(y)}" x2="${W - P}" y2="${Y(y)}" class="sv-ax"/><text x="4" y="${Y(y) + 4}" class="sv-tm">${Math.round(y * 100)}%</text>`;
      for (let x = 0; x <= 10; x += 2) g += `<text x="${X(x) - 4}" y="${H - 8}" class="sv-tm">${x}h</text>`;
      g += `<line x1="${P}" y1="${Y(o.t)}" x2="${W - P}" y2="${Y(o.t)}" stroke="#e8a100" stroke-dasharray="5 4" stroke-width="1.3"/>`;
      let path = "";
      for (let k = 0; k <= 100; k++) { const x = k / 10; path += (k ? "L" : "M") + X(x).toFixed(1) + " " + Y(sig(o.w * x + o.b)).toFixed(1); }
      g += `<path d="${path}" fill="none" stroke="#10b981" stroke-width="2.6"/>`;
      let hit = 0, loss = 0;
      D.forEach(([x, y]) => {
        const p = sig(o.w * x + o.b), pred = p >= o.t ? 1 : 0, ok = pred === y;
        hit += ok; loss += -(y ? Math.log(Math.max(p, 1e-9)) : Math.log(Math.max(1 - p, 1e-9)));
        g += `<circle cx="${X(x)}" cy="${Y(y)}" r="5" fill="${y ? "var(--tx)" : "none"}" stroke="${ok ? "var(--tx)" : "#ef4444"}" stroke-width="${ok ? 1.5 : 2.5}"/>`;
      });
      if (Math.abs(o.w) > 1e-6) {
        const xb = (Math.log(o.t / (1 - o.t)) - o.b) / o.w;
        if (xb > 0 && xb < 10) g += `<line x1="${X(xb)}" y1="${P}" x2="${X(xb)}" y2="${H - P}" stroke="#e8a100" stroke-width="1"/><text x="${X(xb) + 4}" y="${Y(0.62)}" class="sv-tm">fronteira ≈ ${lv2Num(xb)}h</text>`;
      }
      svg.innerHTML = g;
      out.innerHTML = `Acertos: <b>${hit}/${D.length}</b> (${Math.round(100 * hit / D.length)}%) · perda logarítmica média: <b>${lv2Num(loss / D.length)}</b>` +
        `<div style="font-size:.76rem;color:var(--mu);margin-top:4px">Bolinha cheia = passou, vazia = não passou. Contorno vermelho = o modelo errou essa pessoa. p = σ(w·horas + b)</div>`;
    };
    lv2Bind(el, draw);
    el.addEventListener("click", ev => {
      if (!ev.target.closest("[data-lg]")) return;
      let w = cur.w, b = cur.b;
      for (let s = 0; s < 4000; s++) {
        let gw = 0, gb = 0;
        D.forEach(([x, y]) => { const e = sig(w * x + b) - y; gw += e * x; gb += e; });
        w -= 0.05 * gw / D.length; b -= 0.05 * gb / D.length;
      }
      const set = (k, v) => { const inp = el.querySelector(`input[data-in="${k}"]`); if (inp) { inp.value = Math.max(+inp.min, Math.min(+inp.max, v)); inp.dispatchEvent(new Event("input", { bubbles: true })); } };
      set("w", Math.round(w * 10) / 10); set("b", Math.round(b * 10) / 10);
    });
  },

  // Atenção: cada palavra (consulta) distribui 100% da atenção pelas palavras anteriores (chaves).
  atencao(el) {
    const T = ["a", "fluffy", "blue", "creature", "roamed", "the", "verdant", "forest"];
    // pontuações q·k ilustrativas (linha = quem pergunta, coluna = quem responde)
    const S = [
      [2, 0, 0, 0, 0, 0, 0, 0],
      [1, 2, 0, 0, 0, 0, 0, 0],
      [0.5, 1, 2, 0, 0, 0, 0, 0],
      [0.5, 3.2, 3, 1.5, 0, 0, 0, 0],
      [0, 0.5, 0.3, 3.5, 1.5, 0, 0, 0],
      [0.5, 0, 0, 0.3, 0.5, 1.5, 0, 0],
      [0, 0, 0.3, 0, 0, 0.5, 1.5, 0],
      [0, 0, 0, 0.5, 1.2, 0.8, 3.4, 1.4]
    ];
    el.innerHTML = `<div class="lv2-att-toks"></div><div class="lv2-wctl">${lv2Slider("tau", "temperatura (divide as pontuações antes do softmax)", 0.3, 3, 1, 0.1)}</div>` +
      `<label class="lv2-att-mask"><input type="checkbox" data-mask checked> máscara causal (não olhar para palavras futuras)</label>` +
      `<div class="lv2-att-bars"></div><div class="lv2-wout"></div>`;
    const toks = el.querySelector(".lv2-att-toks"), bars = el.querySelector(".lv2-att-bars"), out = el.querySelector(".lv2-wout");
    let q = 3, tau = 1;
    const draw = () => {
      const mask = el.querySelector("[data-mask]").checked;
      const row = S[q].map((s, k) => (mask && k > q) ? -Infinity : (k > q ? 1.2 : s) / tau);
      const m = Math.max(...row), ex = row.map(v => v === -Infinity ? 0 : Math.exp(v - m)), z = ex.reduce((a, b) => a + b, 0), w = ex.map(v => v / z);
      toks.innerHTML = T.map((t, k) => `<button type="button" class="lv2-att-tok${k === q ? " is-q" : ""}" data-q="${k}" style="--a:${k === q ? 0 : w[k]}">${t}</button>`).join("");
      bars.innerHTML = T.map((t, k) => `<div class="lv2-att-row${mask && k > q ? " is-off" : ""}"><span>${t}</span><i style="width:${(w[k] * 100).toFixed(1)}%"></i><b>${Math.round(w[k] * 100)}%</b></div>`).join("");
      const top = w.map((v, k) => [v, k]).filter(([, k]) => k !== q).sort((a, b) => b[0] - a[0])[0];
      out.innerHTML = `Consulta: <b>“${T[q]}”</b>. Os pesos somam 100%. Quem mais recebe atenção (fora ela mesma): <b>“${T[top[1]]}”</b> com ${Math.round(top[0] * 100)}%.` +
        (tau < 0.7 ? ` <span class="lv2-tag-warn">Temperatura baixa: o softmax fica “decidido” e quase toda a atenção vai para uma palavra só.</span>` : tau > 2 ? ` <span class="lv2-tag-warn">Temperatura alta: a atenção se espalha por igual e o contexto perde foco.</span>` : "");
    };
    el.addEventListener("click", ev => { const b = ev.target.closest("[data-q]"); if (b) { q = +b.dataset.q; draw(); } });
    el.addEventListener("change", ev => { if (ev.target.matches("[data-mask]")) draw(); });
    lv2Bind(el, o => { tau = o.tau; draw(); });
  }
});

// ---------------------------------------------------------------- interações + salvar/restaurar
function lv2InitExtra(root, topicId) {
  const saved = (topicId && lv2ReadAnswers()[topicId]) || {};
  const X = saved.x || {};
  const saveX = (key, val) => lv2SaveAnswer(topicId, a => { a.x = a.x || {}; a.x[key] = val; });

  // --- Python: restaura o código salvo e o resultado dos testes
  root.querySelectorAll(".lv2-py").forEach(box => {
    const id = box.dataset.py, st = X[id], ed = box.querySelector(".lv2-py-ed");
    if (st && typeof st.c === "string") ed.value = st.c;
    if (st && +st.ok) box.querySelector(".lv2-py-tests").innerHTML = `<div class="lv2-tag-ok">✓ Você já passou em todos os testes deste exercício.</div>`;
    // Tab = 4 espaços; Enter mantém o recuo (e aumenta depois de ":")
    ed.addEventListener("keydown", ev => {
      if (ev.key === "Tab") { ev.preventDefault(); const s = ed.selectionStart; ed.setRangeText("    ", s, ed.selectionEnd, "end"); }
      else if (ev.key === "Enter") {
        const s = ed.selectionStart, line = ed.value.slice(0, s).split("\n").pop(), ind = (line.match(/^\s*/) || [""])[0];
        ev.preventDefault(); ed.setRangeText("\n" + ind + (/:\s*$/.test(line) ? "    " : ""), s, ed.selectionEnd, "end");
      }
    });
    let typing;
    ed.addEventListener("input", () => { clearTimeout(typing); typing = setTimeout(() => saveX(id, { c: ed.value, ok: (X[id] && X[id].ok && X[id].c === ed.value) ? 1 : 0 }), 600); });
  });

  // --- Montar na ordem: restaura a ordem
  root.querySelectorAll(".lv2-ps").forEach(ol => {
    const st = X[ol.dataset.ps];
    if (st && Array.isArray(st.o)) st.o.forEach(k => { const li = ol.querySelector(`[data-k="${k}"]`); if (li) ol.appendChild(li); });
    if (st && +st.ok) ol.parentElement.querySelector(".lv2-ps-msg").innerHTML = `<span class="lv2-tag-ok">✓ Ordem certa!</span>`;
  });

  // --- Escuta: restaura respostas
  root.querySelectorAll(".lv2-listen").forEach((wrap, w) => {
    wrap.querySelectorAll(".lv2-lis").forEach(it => {
      const key = `ls-${lv2BlockIdx(wrap)}-${it.dataset.lis}`, st = X[key];
      if (!st) return;
      if (st.j != null) { const btn = it.querySelector(`[data-j="${st.j}"]`); if (btn) lv2ListenPick(it, btn); }
      if (st.t != null) { it.querySelector(".lv2-dict").value = st.t; lv2ListenDict(it); }
    });
  });

  // --- Fala: melhor pontuação de cada frase
  root.querySelectorAll(".lv2-spk").forEach(it => {
    const st = X[`sp-${lv2BlockIdx(it)}-${it.dataset.spk}`];
    if (st && st.best != null) it.querySelector(".lv2-spk-res").innerHTML = `<span class="lv2-muted">Sua melhor tentativa: ${st.best}% das palavras reconhecidas.</span>`;
  });

  // --- Vocabulário: o que já sabe
  root.querySelectorAll(".lv2-vocab").forEach(v => {
    const st = X[`vc-${lv2BlockIdx(v)}`] || {};
    v.querySelectorAll(".lv2-card").forEach(c => { if (st[c.dataset.k] != null) c.dataset.know = st[c.dataset.k]; });
    lv2VocabSum(v);
  });

  root.addEventListener("click", async ev => {
    const t = ev.target.closest("[data-lv2x]"); if (!t) return;
    const kind = t.dataset.lv2x;
    if (kind === "say") { lv2Speak(t.dataset.text, t.textContent.includes("🐢") ? 0.65 : 0.95); return; }

    if (kind === "py-run" || kind === "py-check" || kind === "py-reset") {
      const box = t.closest(".lv2-py"), id = box.dataset.py, spec = LV2_SPECS[id] || {}, ed = box.querySelector(".lv2-py-ed");
      const out = box.querySelector(".lv2-py-out"), res = box.querySelector(".lv2-py-tests"), status = box.querySelector(".lv2-py-status");
      if (kind === "py-reset") { ed.value = spec.inicial || ""; out.hidden = true; res.innerHTML = ""; saveX(id, { c: ed.value, ok: 0 }); return; }
      box.querySelectorAll("button").forEach(b => b.disabled = true);
      const r = await lv2PyRun(ed.value, kind === "py-check" ? spec.testes : [], s => { status.textContent = s; });
      box.querySelectorAll("button").forEach(b => b.disabled = false);
      status.textContent = "";
      out.hidden = false;
      if (r.timeout) {
        out.className = "lv2-py-out is-err";
        out.textContent = "⏱ O código rodou por mais de 8 segundos e foi interrompido.\nQuase sempre isso é um laço infinito: a condição do while nunca fica falsa.\nConfira se a variável da condição muda dentro do laço.";
        res.innerHTML = "";
        return;
      }
      out.className = "lv2-py-out" + (r.err ? " is-err" : "");
      out.textContent = (r.out || "") + (r.err ? (r.out ? "\n" : "") + r.err : "") || "(o código rodou e não imprimiu nada)";
      if (kind === "py-check") {
        const list = r.results || [], pass = !r.err && list.length && list.every(x => x.ok);
        res.innerHTML = r.err ? `<div class="lv2-tag-bad">O código deu erro antes dos testes. Leia a última linha da mensagem acima.</div>` :
          list.map(x => `<div class="lv2-py-test ${x.ok ? "ok" : "bad"}">${x.ok ? "✓" : "✗"} ${x.nome}${!x.ok && x.msg ? ` <span class="lv2-muted">— ${lv2Esc(x.msg)}</span>` : ""}</div>`).join("") +
          (pass ? `<div class="lv2-tag-ok" style="margin-top:6px">Todos os testes passaram!</div>` : "");
        saveX(id, { c: ed.value, ok: pass ? 1 : 0 });
      } else {
        saveX(id, { c: ed.value, ok: (X[id] && X[id].ok && X[id].c === ed.value) ? 1 : 0 });
      }
      return;
    }

    if (kind === "ps-up" || kind === "ps-down") {
      const li = t.closest("li"), ol = li.parentElement;
      if (kind === "ps-up" && li.previousElementSibling) ol.insertBefore(li, li.previousElementSibling);
      if (kind === "ps-down" && li.nextElementSibling) ol.insertBefore(li.nextElementSibling, li);
      ol.parentElement.querySelector(".lv2-ps-msg").innerHTML = "";
      saveX(ol.dataset.ps, { o: [...ol.children].map(x => +x.dataset.k), ok: 0 });
      return;
    }
    if (kind === "ps-check") {
      const blk = t.closest(".lv2-block"), ol = blk.querySelector(".lv2-ps"), spec = LV2_SPECS[ol.dataset.ps];
      const got = [...ol.children].map(x => spec.linhas[+x.dataset.k]);
      const right = got.every((l, k) => l === spec.linhas[k]);
      const firstBad = got.findIndex((l, k) => l !== spec.linhas[k]);
      [...ol.children].forEach((li, k) => li.classList.toggle("is-bad", !right && k === firstBad));
      blk.querySelector(".lv2-ps-msg").innerHTML = right ? `<span class="lv2-tag-ok">✓ Ordem certa!</span>` : `<span class="lv2-tag-bad">Ainda não. A linha ${firstBad + 1} (marcada) está fora do lugar.</span>`;
      saveX(ol.dataset.ps, { o: [...ol.children].map(x => +x.dataset.k), ok: right ? 1 : 0 });
      return;
    }

    if (kind === "dlg-all" || kind === "dlg-slow") { const d = t.closest(".lv2-block").querySelector(".lv2-dlg"); lv2Speak(LV2_SPECS[d.dataset.dl] || [], kind === "dlg-slow" ? 0.7 : 0.95); return; }
    if (kind === "dlg-pt") {
      const blk = t.closest(".lv2-block"), show = blk.querySelector(".lv2-dlg-pt").hidden;
      blk.querySelectorAll(".lv2-dlg-pt").forEach(p => p.hidden = !show);
      t.textContent = show ? "Esconder tradução" : "Mostrar tradução";
      return;
    }

    if (kind === "lis-opt") {
      const it = t.closest(".lv2-lis"); lv2ListenPick(it, t);
      saveX(`ls-${lv2BlockIdx(it)}-${it.dataset.lis}`, { j: +t.dataset.j });
      return;
    }
    if (kind === "lis-dict") {
      const it = t.closest(".lv2-lis"); lv2ListenDict(it);
      saveX(`ls-${lv2BlockIdx(it)}-${it.dataset.lis}`, { t: it.querySelector(".lv2-dict").value });
      return;
    }

    if (kind === "spk") {
      const it = t.closest(".lv2-spk"), resEl = it.querySelector(".lv2-spk-res");
      const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SR) return;
      const rec = new SR();
      rec.lang = "en-US"; rec.interimResults = false; rec.maxAlternatives = 3;
      t.disabled = true; t.textContent = "🎙 Ouvindo...";
      resEl.innerHTML = `<span class="lv2-muted">Fale agora...</span>`;
      const end = () => { t.disabled = false; t.textContent = "🎙 Falar"; };
      rec.onresult = e => {
        const alts = [...e.results[0]].map(a => a.transcript);
        const best = alts.map(a => ({ a, d: lv2WordDiff(it.dataset.frase, a) })).sort((x, y) => y.d.pct - x.d.pct)[0];
        const key = `sp-${lv2BlockIdx(it)}-${it.dataset.spk}`, prev = (X[key] && X[key].best) || 0;
        const msg = best.d.pct === 100 ? `<span class="lv2-tag-ok">Perfeito! Todas as palavras foram reconhecidas.</span>` :
          best.d.pct >= 70 ? `<span class="lv2-tag-warn">Quase! Treine as palavras em cinza e tente de novo.</span>` :
          `<span class="lv2-tag-bad">Ouça o modelo devagar (🐢), repita e tente de novo.</span>`;
        resEl.innerHTML = `${msg}<div class="lv2-spk-diff">${best.d.html}</div><div class="lv2-muted">O navegador entendeu: “${lv2Esc(best.a)}” · ${best.d.pct}%</div>`;
        if (best.d.pct > prev) { X[key] = { best: best.d.pct }; saveX(key, { best: best.d.pct }); }
      };
      rec.onerror = e => { resEl.innerHTML = `<span class="lv2-tag-bad">${e.error === "not-allowed" ? "O microfone foi bloqueado. Libere o acesso no ícone de cadeado da barra de endereço." : e.error === "no-speech" ? "Não ouvi nada. Tente de novo, mais perto do microfone." : "Não deu para reconhecer agora (" + e.error + ")."}</span>`; end(); };
      rec.onend = end;
      try { rec.start(); } catch (_) { end(); }
      return;
    }

    if (kind === "vc-flip") { const c = t.closest(".lv2-card"), back = c.querySelector(".lv2-card-back"); back.hidden = !back.hidden; c.classList.toggle("is-flipped", !back.hidden); return; }
    if (kind === "vc-know") {
      const c = t.closest(".lv2-card"), v = c.closest(".lv2-vocab");
      c.dataset.know = t.dataset.v;
      const key = `vc-${lv2BlockIdx(v)}`, st = {};
      v.querySelectorAll(".lv2-card").forEach(x => { if (x.dataset.know != null) st[x.dataset.k] = +x.dataset.know; });
      saveX(key, st); lv2VocabSum(v);
    }
  });
}

function lv2ListenPick(it, btn) {
  it.querySelectorAll(".lv2-opt").forEach(o => { o.disabled = true; if (o.dataset.ok === "1") o.classList.add("is-right"); });
  if (btn.dataset.ok !== "1") btn.classList.add("is-wrong");
  it.querySelector(".lv2-lis-reveal").hidden = false;
}
function lv2ListenDict(it) {
  const d = lv2WordDiff(it.dataset.frase, it.querySelector(".lv2-dict").value), res = it.querySelector(".lv2-lis-res");
  res.innerHTML = d.exact ? `<span class="lv2-tag-ok">✓ Exatamente!</span>` :
    `<span class="${d.pct >= 70 ? "lv2-tag-warn" : "lv2-tag-bad"}">${d.pct}% das palavras.</span> <span class="lv2-spk-diff">${d.html}</span>`;
}
function lv2VocabSum(v) {
  const all = v.querySelectorAll(".lv2-card"), know = [...all].filter(c => c.dataset.know === "1").length;
  const sum = v.parentElement.querySelector(".lv2-vc-sum");
  if (sum) sum.innerHTML = `Você marcou <b>${know} de ${all.length}</b> como “já sei”.` + (know === all.length ? ` <span class="lv2-tag-ok">Vocabulário da aula dominado!</span>` : " Volte nas marcadas como “Rever” amanhã.");
}
"""

EXTRA_CSS = r"""
/* ===== Blocos novos: código, ordem, diálogo, escuta, fala, vocabulário ===== */
.lv2-muted{color:var(--mu);font-size:.85em}
.lv2-note{padding:8px 12px;border-radius:8px;background:rgba(232,161,0,.12);font-size:.82rem;margin-bottom:8px}
.lv2-btn-ghost{background:transparent;border-color:transparent;color:var(--mu)}
.lv2-say{font:inherit;font-size:.8rem;padding:3px 8px;border-radius:8px;border:1px solid var(--bd);background:var(--bg);color:var(--tx);cursor:pointer;white-space:nowrap}
.lv2-say:hover{border-color:var(--mu)}

/* Python */
/* Sem ligaduras: "<=" e "!=" aparecem como o aluno digita, não como ≤ e ≠ */
.lv2-py-ed,.lv2-py-out,.lv2-ps-txt,.lv2-code,.lv2 pre,.lv2 code{font-variant-ligatures:none;font-feature-settings:"liga" 0,"calt" 0}
.lv2-py{margin-top:10px;border:1px solid var(--bd);border-radius:10px;overflow:hidden;background:var(--bg)}
.lv2-py-bar{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:6px 12px;font-size:.72rem;color:var(--mu);border-bottom:1px solid var(--bd)}
.lv2-py-lang{font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.lv2-py-status{font-style:italic}
.lv2-py-ed{display:block;width:100%;box-sizing:border-box;resize:vertical;border:0;outline:none;padding:12px 14px;font:13px/1.65 ui-monospace,"JetBrains Mono","Cascadia Code",Consolas,monospace;background:transparent;color:var(--tx);tab-size:4;white-space:pre;overflow:auto}
.lv2-py-actions{display:flex;flex-wrap:wrap;gap:6px;padding:8px 10px;border-top:1px solid var(--bd)}
.lv2-py-out{margin:0;padding:10px 14px;border-top:1px solid var(--bd);font:12.5px/1.6 ui-monospace,Consolas,monospace;white-space:pre-wrap;max-height:260px;overflow:auto;background:transparent;color:var(--tx)}
.lv2-py-out.is-err{color:#ef4444}
.lv2-py-tests{padding:0 14px}
.lv2-py-tests:not(:empty){padding:8px 14px 10px;border-top:1px solid var(--bd)}
.lv2-py-test{font-size:.84rem;padding:2px 0}
.lv2-py-test.ok{color:#10b981}.lv2-py-test.bad{color:#ef4444}

/* Montar na ordem */
.lv2-ps{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-direction:column;gap:6px}
.lv2-ps-line{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:6px 8px 6px 12px;border:1px solid var(--bd);border-radius:8px;background:var(--bg)}
.lv2-ps.is-code .lv2-ps-txt{font:13px/1.5 ui-monospace,Consolas,monospace;white-space:pre}
.lv2-ps-line.is-bad{border-color:#ef4444}
.lv2-ps-btns{display:flex;gap:4px;flex:none}
.lv2-ps-btns button{font:inherit;width:28px;height:28px;border-radius:6px;border:1px solid var(--bd);background:transparent;color:var(--mu);cursor:pointer}
.lv2-ps-btns button:hover{color:var(--tx);border-color:var(--mu)}
.lv2-ps-msg{margin-top:8px;font-size:.85rem}

/* Diálogo */
.lv2-dlg{display:flex;flex-direction:column;gap:10px;margin-top:10px}
.lv2-dlg-row{display:flex;flex-direction:column;gap:3px;max-width:88%}
.lv2-dlg-row[data-side="b"]{align-self:flex-end;align-items:flex-end}
.lv2-dlg-who{font-size:.7rem;font-weight:700;color:var(--mu);text-transform:uppercase;letter-spacing:.06em}
.lv2-dlg-bubble{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border-radius:12px;background:var(--bg);border:1px solid var(--bd)}
.lv2-dlg-en{font-weight:600}
.lv2-dlg-pt{font-size:.84rem;color:var(--mu);margin-top:2px}

/* Escuta */
.lv2-listen{display:flex;flex-direction:column;gap:16px;margin-top:10px}
.lv2-lis-head{display:flex;align-items:center;flex-wrap:wrap;gap:8px}
.lv2-lis-hint{font-size:.82rem;color:var(--mu)}
.lv2-lis-reveal{margin-top:8px;font-size:.88rem}
.lv2-lis-res{margin-top:6px;font-size:.88rem}
.lv2-dictbox{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-top:8px}
.lv2-dict{font:inherit;font-size:.9rem;padding:6px 10px;border-radius:8px;border:1px solid var(--bd);background:var(--bg);color:var(--tx);width:min(420px,100%)}
.lv2-w-ok{color:#10b981;font-weight:600}
.lv2-w-miss{color:var(--mu);text-decoration:underline dotted}

/* Fala */
.lv2-speak{display:flex;flex-direction:column;gap:14px;margin-top:10px}
.lv2-spk{padding:12px 14px;border:1px solid var(--bd);border-radius:10px}
.lv2-spk-en{font-size:1.05rem;font-weight:600}
.lv2-spk-pt{font-size:.84rem;color:var(--mu)}
.lv2-spk-btns{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.lv2-spk-res{margin-top:8px;font-size:.88rem}
.lv2-spk-diff{display:block;margin:4px 0}

/* Vocabulário */
.lv2-vocab{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(200px,100%),1fr));gap:10px;margin-top:10px}
.lv2-card{display:flex;flex-direction:column;border:1px solid var(--bd);border-radius:12px;overflow:hidden;background:var(--bg)}
.lv2-card[data-know="1"]{border-color:rgba(16,185,129,.55)}
.lv2-card[data-know="0"]{border-color:rgba(232,161,0,.55)}
.lv2-card-face{font:inherit;flex:1;display:flex;flex-direction:column;gap:6px;align-items:flex-start;text-align:left;padding:14px;border:0;background:transparent;color:var(--tx);cursor:pointer;min-height:84px}
.lv2-card-en{font-weight:700;font-size:1rem}
.lv2-card-back{display:flex;flex-direction:column;gap:4px}
.lv2-card-back[hidden]{display:none}
.lv2-card-pt{color:var(--mu)}
.lv2-card-ex{font-size:.84rem;font-style:italic}
.lv2-card-foot{display:flex;gap:6px;align-items:center;padding:8px 10px;border-top:1px solid var(--bd)}
.lv2-card-mark{font:inherit;font-size:.74rem;padding:3px 8px;border-radius:6px;border:1px solid var(--bd);background:transparent;color:var(--mu);cursor:pointer}
.lv2-card[data-know="1"] .lv2-card-mark[data-v="1"]{color:#10b981;border-color:#10b981}
.lv2-card[data-know="0"] .lv2-card-mark[data-v="0"]{color:#e8a100;border-color:#e8a100}
.lv2-vc-sum{margin-top:10px;font-size:.86rem}

/* Atenção */
.lv2-att-toks{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.lv2-att-tok{font:inherit;font-size:.9rem;padding:5px 10px;border-radius:8px;border:1px solid var(--bd);cursor:pointer;color:var(--tx);background:color-mix(in srgb,#10b981 calc(var(--a,0)*100%),transparent)}
.lv2-att-tok.is-q{border-color:#e8a100;box-shadow:0 0 0 2px rgba(232,161,0,.35)}
.lv2-att-mask{display:flex;align-items:center;gap:8px;font-size:.8rem;color:var(--mu);margin-top:8px}
.lv2-att-bars{display:flex;flex-direction:column;gap:4px;margin-top:10px}
.lv2-att-row{display:grid;grid-template-columns:76px 1fr 44px;align-items:center;gap:8px;font-size:.8rem}
.lv2-att-row i{display:block;height:10px;border-radius:5px;background:#10b981;min-width:1px;transition:width .25s}
.lv2-att-row b{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}
.lv2-att-row.is-off{opacity:.35}
"""
