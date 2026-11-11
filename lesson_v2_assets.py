# -*- coding: utf-8 -*-
"""
Aula Visual v2 — renderizador de blocos pedagógicos flexíveis.

Cada aula deixa de ter 4 cards fixos (intuicao/formula/exemplo/codigo) e passa a ser
uma sequência livre de blocos, escolhidos conforme a melhor forma de ensinar o assunto.

Formato de dados (pt_guide v2):
{
  "v": 2,
  "duracao": 25,                        # minutos estimados
  "gancho": "html",                     # pergunta/situação que abre a aula
  "prerequisitos": ["..."],             # o que o aluno vai reutilizar
  "objetivos": ["..."],                 # ao final da aula você vai saber...
  "blocos": [ {"tipo": ..., "titulo": ..., "corpo": "html", ...campos do tipo} ],
  "resumo": ["..."],
  "proxima": "html",                    # ponte para a próxima aula
  "referencias": [{"obra": "...", "trecho": "...", "uso": "..."}]
}

Tipos de bloco e campos extras:
  texto        -> corpo
  notacao      -> itens: [{simbolo, leitura, significado}]
  visual       -> svg, legenda
  icones       -> total, colunas, grupos: [{n, estilo: s1|s2|s3, rotulo}], resto, legenda
  passos       -> passos: [{faca, porque}], conclusao
  pense        -> pergunta, resposta
  laboratorio  -> codigo, experimentos: [...]
  desafio      -> exercicios: [{enunciado, dicas: [...], resposta}]
  armadilhas   -> itens: [{erro, correcao}]
  ponte        -> corpo (aplicação concreta em IA e conexões com outras aulas)
  tabela       -> cabecalho: [...], linhas: [[...]]

Blocos do piloto (Concreto -> Desenho -> Fórmula, prática ativa e revisão espaçada):
  concreto     -> corpo (situação do dia a dia que já É o conceito, antes de qualquer símbolo)
  crianca      -> corpo ("explica como se eu tivesse 10 anos")
  palpite      -> pergunta, opcoes: [...], correta: idx, explicacao, porques: [... por opção, opcional]
  video        -> id (YouTube), inicio, fim (segundos), canal, titulo_video, missao: [...], respostas (html)
  widget       -> widget: vetores | produto_escalar | descida, missoes: [...]
  pratica      -> exercicios: [{nivel: 1|2|3, enunciado, valor (número ou lista, opcional), tol, dicas, resposta}]
  quiz         -> perguntas: [{pergunta, opcoes, correta, explicacao}], minimo
                  (aprovado -> agenda revisões em 1, 3, 7 e 21 dias e libera o bloco "camadas";
                  as revisões são sincronizadas com o DynamoDB junto com o progresso)
  camadas      -> ponte: [{nome, url, trecho, tempo, foco}], profundidade: [{obra, url, secao, perguntas}],
                  revisao: [{nome, url, trecho, tempo, foco}]
Todos aceitam "corpo" (antes do conteúdo específico) e "depois" (após o conteúdo).

Aulas no formato antigo (sem "v": 2) continuam sendo renderizadas pelo código atual.
"""

LESSON_V2_CSS = r"""
/* ===== Aula Visual v2 ===== */
.lv2{display:flex;flex-direction:column;gap:12px;font-size:.88rem;line-height:1.65;color:var(--tx)}
.lv2 p{margin:0 0 .7em}.lv2 p:last-child{margin-bottom:0}
.lv2 code{background:rgba(74,92,106,.22);padding:1px 5px;border-radius:4px;font-size:.84em}
.lv2 ul{margin:.3em 0 .6em;padding-left:1.2em}.lv2 li{margin:.15em 0}
.lv2-hero{border:1px solid var(--bd);border-radius:12px;padding:14px 16px;background:linear-gradient(135deg,rgba(74,92,106,.20),rgba(37,55,69,.06))}
.lv2-chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.lv2-chip{font-size:.7rem;font-weight:700;padding:2px 9px;border-radius:99px;border:1px solid var(--bd);color:var(--mu);background:var(--card)}
.lv2-hook{font-size:.97rem;font-weight:600;line-height:1.55}
.lv2-meta{display:grid;gap:10px;margin-top:12px}
.lv2-meta-title{font-size:.7rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:var(--mu);margin-bottom:2px}
.lv2-block{border:1px solid var(--bd);border-radius:12px;padding:12px 15px;background:var(--card);transition:border-color .2s}
.lv2-head{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:2px}
.lv2-kicker{font-size:.7rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:var(--mu)}
.lv2-badge{font-size:.66rem;font-weight:750;padding:1px 7px;border-radius:99px;background:var(--bg);color:var(--mu);border:1px solid var(--bd);white-space:nowrap}
.lv2-title{margin:2px 0 8px;font-size:.98rem;font-weight:800;line-height:1.35}
.lv2-notation{display:grid;gap:7px;margin:8px 0 4px}
.lv2-not-row{display:grid;grid-template-columns:minmax(92px,auto) 1fr;gap:12px;align-items:center;padding:8px 10px;border-radius:8px;background:rgba(74,92,106,.13)}
.lv2-not-sym{font-size:1.02rem;text-align:center}
.lv2-not-read{font-size:.78rem;color:var(--mu)}
.lv2-steps{list-style:none;counter-reset:lv2s;padding:0;margin:8px 0 0;display:flex;flex-direction:column;gap:8px}
.lv2-steps li{counter-increment:lv2s;position:relative;padding:8px 10px 8px 42px;border-radius:8px;background:rgba(74,92,106,.10)}
.lv2-steps li::before{content:counter(lv2s);position:absolute;left:11px;top:9px;width:21px;height:21px;border-radius:50%;background:var(--bd);color:var(--tx);font-size:.72rem;font-weight:800;display:flex;align-items:center;justify-content:center}
.lv2-step-why{font-size:.82rem;color:var(--mu);margin-top:4px}
.lv2-conclusion{margin-top:10px;padding:9px 12px;border-radius:8px;border:1px dashed var(--mu)}
.lv2-q{font-weight:650}
.lv2 details{margin-top:8px;border:1px solid var(--bd);border-radius:8px;padding:6px 10px;background:var(--bg)}
.lv2 summary{cursor:pointer;font-weight:700;font-size:.8rem;color:var(--mu);user-select:none}
.lv2 details[open]>summary{margin-bottom:6px}
.lv2-code,.lv2 pre{margin:8px 0 0;padding:10px 12px;background:#06141B;color:#CCD0CF;border:1px solid #253745;border-radius:8px;overflow-x:auto;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:.79rem;line-height:1.5}
.lv2 pre code{background:none;padding:0;font-size:inherit}
.lv2-exp-title{font-size:.72rem;font-weight:800;text-transform:uppercase;color:var(--mu);margin-top:10px}
.lv2-ex{padding:10px 0 4px;border-top:1px solid var(--bd)}.lv2-ex:first-of-type{border-top:none;padding-top:4px}
.lv2-ex-n{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border-radius:50%;background:var(--bd);font-size:.72rem;font-weight:800;margin-right:8px}
.lv2-pitfalls{display:grid;gap:8px;margin-top:6px}
.lv2-pit{padding:8px 11px;border-radius:8px;background:rgba(74,92,106,.11)}
.lv2-pit-wrong{color:var(--mu);font-weight:650}
.lv2-pit-right{margin-top:3px}
.lv2-table-wrap{overflow-x:auto;margin-top:8px}
.lv2-table{width:100%;border-collapse:collapse;font-size:.82rem}
.lv2-table th{font-size:.72rem;text-transform:uppercase;color:var(--mu);text-align:left;padding:6px 8px;border-bottom:1.5px solid var(--bd)}
.lv2-table td{padding:6px 8px;border-bottom:1px solid var(--bd);vertical-align:top}
.lv2-fig{margin:10px 0 2px}
.lv2-svg{width:100%;height:auto;display:block;max-width:560px;margin:0 auto}
.lv2-fig figcaption{font-size:.78rem;color:var(--mu);text-align:center;margin-top:6px}
.lv2-legend{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;font-size:.76rem;color:var(--mu);margin-top:6px}
.lv2-leg{display:inline-flex;align-items:center;gap:5px}
.lv2-dot-s0{fill:var(--bd)}.lv2-dot-s1{fill:var(--tx)}.lv2-dot-s2{fill:var(--mu)}.lv2-dot-s3{fill:none;stroke:var(--tx);stroke-width:1.5}
.sv-ax{stroke:var(--mu);stroke-width:1;opacity:.55}
.sv-a{stroke:var(--tx);stroke-width:2.6;fill:none}
.sv-b{stroke:var(--mu);stroke-width:2.6;fill:none}
.sv-thin{stroke:var(--mu);stroke-width:1.4;fill:none}
.sv-dash{stroke-dasharray:4 4}
.sv-t{fill:var(--tx);font-size:12px;font-family:inherit}
.sv-tm{fill:var(--mu);font-size:11px;font-family:inherit}
.sv-it{font-style:italic}
.sv-fill{fill:var(--tx)}.sv-fillm{fill:var(--mu)}
.sv-node{fill:var(--card);stroke:var(--mu);stroke-width:1.5}
.lv2-footer{border:1px solid var(--bd);border-radius:12px;padding:12px 15px;background:linear-gradient(135deg,rgba(37,55,69,.06),rgba(74,92,106,.18))}
.lv2-refs{font-size:.78rem;color:var(--mu);margin-top:10px}
.lv2-refs li{margin:.25em 0}
/* ===== Piloto: blocos ativos ===== */
.lv2{--lv2-ok:#10b981;--lv2-warn:#e8a100;--lv2-bad:#ef4444}
.lv2-concreto{border-left:4px solid var(--lv2-warn)}
.lv2-crianca{background:linear-gradient(135deg,rgba(232,161,0,.10),rgba(16,185,129,.06))}
.lv2-palpite,.lv2-quiz{border-left:4px solid var(--mu)}
.lv2-opts{display:flex;flex-direction:column;gap:6px;margin-top:8px}
.lv2-opt{font:inherit;font-size:.85rem;text-align:left;padding:8px 12px;border-radius:9px;border:1px solid var(--bd);background:var(--bg);color:var(--tx);cursor:pointer;transition:.15s}
.lv2-opt:hover:not(:disabled){border-color:var(--mu)}
.lv2-opt:disabled{cursor:default}
.lv2-opt.is-right{border-color:var(--lv2-ok);background:rgba(16,185,129,.12)}
.lv2-opt.is-wrong{border-color:var(--lv2-bad);background:rgba(239,68,68,.10)}
.lv2-fb{margin-top:10px;padding:10px 12px;border-radius:9px;background:var(--bg);border:1px dashed var(--mu)}
.lv2-fb-msg{font-weight:800;margin-bottom:4px}
.lv2-btn{font:inherit;font-size:.8rem;font-weight:700;padding:6px 13px;border-radius:99px;border:1px solid var(--bd);background:var(--bg);color:var(--tx);cursor:pointer}
.lv2-btn:hover{border-color:var(--mu)}
.lv2-btn-main{background:var(--tx);color:var(--bg);border-color:var(--tx)}
.lv2-video-meta{font-size:.78rem;color:var(--mu);margin-bottom:6px}
.lv2-mission{padding:8px 12px;border-radius:9px;background:rgba(74,92,106,.12);margin-bottom:8px}
.lv2-mission ol{margin:.3em 0 0;padding-left:1.3em}
.lv2-video-wrap{position:relative;width:100%;aspect-ratio:16/9;border-radius:10px;overflow:hidden;background:#06141B;display:flex;align-items:center;justify-content:center}
.lv2-video-wrap iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.lv2-video-play{font:inherit;font-weight:800;font-size:.9rem;padding:10px 18px;border-radius:99px;border:1px solid #4A5C6A;background:#253745;color:#CCD0CF;cursor:pointer}
.lv2-ext{display:inline-block;margin-top:6px;font-size:.76rem;color:var(--mu)}
.lv2-clip-note{margin-top:8px;padding:8px 12px;border-radius:9px;background:rgba(16,185,129,.12);border:1px solid rgba(16,185,129,.35);font-size:.82rem;font-weight:700;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.lv2-clip-note[hidden]{display:none}
.lv2-clip-replay{font:inherit;font-size:.78rem;font-weight:800;padding:4px 12px;border-radius:99px;border:1px solid #4A5C6A;background:#253745;color:#CCD0CF;cursor:pointer}
.lv2-wbox{margin-top:8px;border:1px solid var(--bd);border-radius:10px;padding:10px;background:var(--bg)}
.lv2-wsvg{width:100%;height:auto;display:block;max-width:420px;margin:0 auto;touch-action:manipulation}
.lv2-wctl{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:6px 14px;margin-top:8px}
.lv2-wctl label{display:flex;flex-direction:column;font-size:.74rem;font-weight:700;color:var(--mu)}
.lv2-wctl input[type=range]{width:100%;accent-color:var(--lv2-ok)}
.lv2-wout{margin-top:8px;font-size:.84rem;padding:8px 10px;border-radius:8px;background:var(--card);border:1px solid var(--bd)}
.lv2-wbtns{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.lv2-wtable{width:100%;border-collapse:collapse;font-size:.76rem;margin-top:6px;font-variant-numeric:tabular-nums}
.lv2-wtable td,.lv2-wtable th{padding:3px 6px;border-bottom:1px solid var(--bd);text-align:right}
.lv2-tag-ok{color:var(--lv2-ok);font-weight:800}.lv2-tag-warn{color:var(--lv2-warn);font-weight:800}.lv2-tag-bad{color:var(--lv2-bad);font-weight:800}
.lv2-lvl-tag{font-size:.7rem;font-weight:800;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px}
.lv2-lvl-1 .lv2-lvl-tag{color:var(--lv2-ok)}.lv2-lvl-2 .lv2-lvl-tag{color:var(--lv2-warn)}.lv2-lvl-3 .lv2-lvl-tag{color:var(--lv2-bad)}
.lv2-check{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-top:8px}
.lv2-check input{font:inherit;font-size:.82rem;padding:5px 9px;border-radius:8px;border:1px solid var(--bd);background:var(--bg);color:var(--tx);width:170px;max-width:100%}
.lv2-check-msg{font-size:.8rem;font-weight:700}
.lv2-qz{padding:8px 0;border-top:1px solid var(--bd)}.lv2-qz:first-child{border-top:none}
.lv2-qopt{display:flex;gap:8px;align-items:flex-start;padding:5px 8px;border-radius:8px;cursor:pointer;font-size:.84rem}
.lv2-qopt:hover{background:rgba(74,92,106,.12)}
.lv2-qz.is-right .lv2-q::after{content:" ✓";color:var(--lv2-ok)}
.lv2-qz.is-wrong .lv2-q::after{content:" ✗";color:var(--lv2-bad)}
.lv2-qz-exp{margin-top:6px;font-size:.82rem;padding:7px 10px;border-radius:8px;background:var(--bg)}
.lv2-quiz-res{margin-top:10px;font-size:.85rem}
.lv2-layers[data-locked="1"] .lv2-layer-body{display:none}
.lv2-layers[data-locked="0"] .lv2-lock{display:none}
.lv2-lock{padding:10px 12px;border-radius:9px;border:1px dashed var(--mu);font-size:.84rem;display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between}
.lv2-layer{margin-top:10px}
.lv2-layer-tag{font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.04em;color:var(--mu);margin-bottom:6px}
.lv2-src{padding:8px 11px;border-radius:9px;background:rgba(74,92,106,.11);margin-bottom:6px}
.lv2-src a{font-weight:750;color:var(--tx)}
.lv2-src-meta{font-size:.74rem;color:var(--mu);margin:2px 0 4px}
.lv2-review{font-size:.8rem;padding:6px 10px;border-radius:8px;background:rgba(232,161,0,.12);border:1px solid rgba(232,161,0,.4);margin-top:8px}
"""

LESSON_V2_JS = r"""
// =========================================================================
// AULA VISUAL v2 — renderizador de blocos pedagógicos flexíveis
// =========================================================================
const LV2_META = {
  texto:       { icon: "📖", label: "Explicação" },
  notacao:     { icon: "🔤", label: "Como ler a notação" },
  visual:      { icon: "👁️", label: "Visualize" },
  icones:      { icon: "👥", label: "Visualize" },
  passos:      { icon: "🧮", label: "Resolvido passo a passo" },
  pense:       { icon: "🤔", label: "Pare e pense" },
  laboratorio: { icon: "🧪", label: "Laboratório" },
  desafio:     { icon: "🎯", label: "Sua vez" },
  armadilhas:  { icon: "⚠️", label: "Armadilhas comuns" },
  ponte:       { icon: "🔗", label: "Onde isso aparece na IA" },
  tabela:      { icon: "📊", label: "Compare" },
  concreto:    { icon: "🍎", label: "Começando pelo concreto" },
  crianca:     { icon: "🧒", label: "Explica como se eu tivesse 10 anos" },
  palpite:     { icon: "🎲", label: "Chute antes de ver" },
  video:       { icon: "🎬", label: "Assista com uma missão" },
  widget:      { icon: "🕹️", label: "Mexa e descubra" },
  pratica:     { icon: "🏋️", label: "Prática em 3 níveis" },
  quiz:        { icon: "✅", label: "Quiz de saída" },
  camadas:     { icon: "📚", label: "Vá mais fundo" }
};
const LV2_REVIEW_KEY = "roteiro-review-v1";
const LV2_REVIEW_DAYS = [1, 3, 7, 21];
const lv2Fmt = s => Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0");

/* Trechos de vídeo: o parâmetro end= do YouTube só para a reprodução uma vez e
   deixa a barra livre para o vídeo inteiro. Aqui o player fala com a página
   (enablejsapi) e a página mantém a reprodução dentro de [início, fim]. */
const LV2_CLIPS = new Map(); // contentWindow do iframe -> {s, e, iframe, note, ended}
function lv2YtCmd(clip, func, args) {
  try { clip.iframe.contentWindow.postMessage(JSON.stringify({ event: "command", func, args: args || [] }), "*"); } catch (_) {}
}
function lv2PlayClip(wrap) {
  const s = +wrap.dataset.s || 0, e = +wrap.dataset.e || 0;
  let src = wrap.dataset.src + "&enablejsapi=1";
  if (/^https?:/.test(location.origin)) src += "&origin=" + encodeURIComponent(location.origin);
  wrap.innerHTML = `<iframe src="${src}" title="Trecho do vídeo" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>`;
  const iframe = wrap.querySelector("iframe");
  const note = wrap.parentElement.querySelector(".lv2-clip-note");
  const clip = { s, e, iframe, note, ended: false };
  const hello = () => { try { iframe.contentWindow.postMessage(JSON.stringify({ event: "listening", id: Math.random().toString(36).slice(2) }), "*"); } catch (_) {} };
  iframe.addEventListener("load", () => { LV2_CLIPS.set(iframe.contentWindow, clip); hello(); setTimeout(hello, 800); });
  if (note) {
    note.hidden = true;
    const replay = note.querySelector(".lv2-clip-replay");
    if (replay) replay.onclick = () => { clip.ended = false; note.hidden = true; lv2YtCmd(clip, "seekTo", [s, true]); lv2YtCmd(clip, "playVideo"); };
  }
}
window.addEventListener("message", ev => {
  if (!/youtube(-nocookie)?\.com$/.test((ev.origin || "").replace(/^https?:\/\/(www\.)?/, ""))) return;
  const clip = LV2_CLIPS.get(ev.source);
  if (!clip) return;
  let d; try { d = typeof ev.data === "string" ? JSON.parse(ev.data) : ev.data; } catch (_) { return; }
  const info = d && d.info;
  if (!info || typeof info.currentTime !== "number") return;
  const t = info.currentTime;
  if (clip.e && t >= clip.e - 0.25) {
    clip.ended = true;
    lv2YtCmd(clip, "pauseVideo");
    lv2YtCmd(clip, "seekTo", [clip.e - 0.5, true]);
    if (clip.note) clip.note.hidden = false;
  } else if (clip.s && t < clip.s - 1.5) {
    lv2YtCmd(clip, "seekTo", [clip.s, true]);
  } else if (clip.ended && t < clip.e - 2) {
    clip.ended = false;
    if (clip.note) clip.note.hidden = true;
  }
});
const lv2Date = t => { const d = new Date(t); return String(d.getDate()).padStart(2, "0") + "/" + String(d.getMonth() + 1).padStart(2, "0"); };
function lv2ReadReview() { try { return JSON.parse(localStorage.getItem(LV2_REVIEW_KEY) || "{}") || {}; } catch (e) { return {}; } }
function lv2WriteReview(o) {
  try { localStorage.setItem(LV2_REVIEW_KEY, JSON.stringify(o)); } catch (e) {}
  // Revisões fazem parte do progresso: vão para a nuvem junto com o resto (campo "extra" no DynamoDB)
  if (typeof scheduleAwsRealtimeSync === "function") scheduleAwsRealtimeSync();
}

function isPtGuideV2(g) { return Boolean(g && g.v === 2 && Array.isArray(g.blocos)); }
function ptGuideCardCount(g) { return isPtGuideV2(g) ? g.blocos.length : 4; }

function lv2Esc(s) {
  return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/* Realce de sintaxe Python, leve e sem dependências: comentários, textos, números,
   palavras-chave e chamadas de função ganham classes .tk-* coloridas pelo tema. */
const LV2_PY_RE = /(#[^\n]*)|("{3}[\s\S]*?"{3}|'{3}[\s\S]*?'{3}|[fFrRbB]?"(?:\\.|[^"\\\n])*"|[fFrRbB]?'(?:\\.|[^'\\\n])*')|\b(\d+(?:\.\d+)?(?:e-?\d+)?)\b|\b(import|from|as|def|return|for|in|if|elif|else|while|class|with|lambda|and|or|not|is|None|True|False|try|except|finally|raise|yield|pass|break|continue|global|assert)\b|([A-Za-z_]\w*)(?=\()/g;
function lv2HighlightPy(src) {
  const s = String(src == null ? "" : src);
  let out = "", last = 0, m;
  LV2_PY_RE.lastIndex = 0;
  while ((m = LV2_PY_RE.exec(s))) {
    out += lv2Esc(s.slice(last, m.index));
    const cls = m[1] ? "c" : m[2] ? "s" : m[3] ? "n" : m[4] ? "k" : "f";
    out += `<span class="tk-${cls}">${lv2Esc(m[0])}</span>`;
    last = LV2_PY_RE.lastIndex;
  }
  return out + lv2Esc(s.slice(last));
}

function lv2IconArray(b) {
  const cols = b.colunas || 40, total = b.total || 1000, gap = 11, r = 4;
  const rows = Math.ceil(total / cols);
  const cls = [];
  (b.grupos || []).forEach(g => { for (let k = 0; k < g.n; k++) cls.push(g.estilo || "s1"); });
  while (cls.length < total) cls.push("s0");
  let dots = "";
  for (let k = 0; k < total; k++) {
    const cx = 8 + (k % cols) * gap, cy = 8 + Math.floor(k / cols) * gap;
    dots += `<circle cx="${cx}" cy="${cy}" r="${r}" class="lv2-dot-${cls[k]}"/>`;
  }
  const W = 16 + (cols - 1) * gap, H = 16 + (rows - 1) * gap;
  const sw = st => `<svg width="12" height="12" aria-hidden="true"><circle cx="6" cy="6" r="4.5" class="lv2-dot-${st}"/></svg>`;
  let legend = (b.grupos || []).map(g => `<span class="lv2-leg">${sw(g.estilo || "s1")}${g.rotulo}</span>`).join("");
  if (b.resto) legend += `<span class="lv2-leg">${sw("s0")}${b.resto}</span>`;
  return `<figure class="lv2-fig"><svg viewBox="0 0 ${W} ${H}" class="lv2-svg" role="img">${dots}</svg>` +
         `<div class="lv2-legend">${legend}</div>${b.legenda ? `<figcaption>${b.legenda}</figcaption>` : ""}</figure>`;
}

function lv2Block(b, i, n) {
  const tipo = b.tipo || "texto";
  const meta = LV2_META[tipo] || LV2_META.texto;
  let inner = b.corpo ? `<div class="lv2-prose">${b.corpo}</div>` : "";
  switch (tipo) {
    case "notacao":
      inner += `<div class="lv2-notation">` + (b.itens || []).map(it =>
        `<div class="lv2-not-row"><div class="lv2-not-sym">${it.simbolo}</div><div>` +
        `<div class="lv2-not-read">lê-se: <i>${it.leitura}</i></div><div>${it.significado}</div></div></div>`).join("") + `</div>`;
      break;
    case "visual":
      inner += `<figure class="lv2-fig">${b.svg || ""}${b.legenda ? `<figcaption>${b.legenda}</figcaption>` : ""}</figure>`;
      break;
    case "icones":
      inner += lv2IconArray(b);
      break;
    case "passos":
      inner += `<ol class="lv2-steps">` + (b.passos || []).map(p =>
        `<li><div>${p.faca}</div>${p.porque ? `<div class="lv2-step-why"><b>Por quê?</b> ${p.porque}</div>` : ""}</li>`).join("") + `</ol>` +
        (b.conclusao ? `<div class="lv2-conclusion">${b.conclusao}</div>` : "");
      break;
    case "pense":
      inner += `<div class="lv2-q">${b.pergunta || ""}</div>` +
               `<details><summary>Pensou? Ver a resposta</summary><div>${b.resposta || ""}</div></details>`;
      break;
    case "laboratorio":
      inner += `<pre class="lv2-code"><code>${lv2HighlightPy(b.codigo)}</code></pre>`;
      if (b.experimentos && b.experimentos.length) {
        inner += `<div class="lv2-exp-title">Experimente e observe</div><ul>${b.experimentos.map(e => `<li>${e}</li>`).join("")}</ul>`;
      }
      break;
    case "desafio":
      inner += (b.exercicios || []).map((ex, k) =>
        `<div class="lv2-ex"><div><span class="lv2-ex-n">${k + 1}</span>${ex.enunciado}</div>` +
        (ex.dicas || []).map((d, j) => `<details><summary>Dica ${j + 1}</summary><div>${d}</div></details>`).join("") +
        `<details><summary>Resposta comentada</summary><div>${ex.resposta || ""}</div></details></div>`).join("");
      break;
    case "armadilhas":
      inner += `<div class="lv2-pitfalls">` + (b.itens || []).map(it =>
        `<div class="lv2-pit"><div class="lv2-pit-wrong">✗ ${it.erro}</div><div class="lv2-pit-right">✓ ${it.correcao}</div></div>`).join("") + `</div>`;
      break;
    case "tabela":
      inner += `<div class="lv2-table-wrap"><table class="lv2-table"><thead><tr>${(b.cabecalho || []).map(h => `<th>${h}</th>`).join("")}</tr></thead>` +
               `<tbody>${(b.linhas || []).map(r => `<tr>${r.map(c => `<td>${c}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
      break;
    case "palpite":
      inner += `<div class="lv2-q">${b.pergunta || ""}</div><div class="lv2-opts">` +
        (b.opcoes || []).map((o, k) => `<button type="button" class="lv2-opt" data-lv2="palpite" data-k="${k}" data-ok="${k === b.correta ? 1 : 0}">${o}</button>`).join("") +
        `</div><div class="lv2-fb" hidden><div class="lv2-fb-msg"></div>` +
        (b.porques || []).map((p, k) => `<div class="lv2-fb-why" data-k="${k}" hidden>${p}</div>`).join("") +
        `<div>${b.explicacao || ""}</div></div>`;
      break;
    case "video": {
      const s = b.inicio || 0, e = b.fim || 0;
      const src = `https://www.youtube-nocookie.com/embed/${b.id}?start=${s}${e ? `&end=${e}` : ""}&rel=0&autoplay=1`;
      inner += `<div class="lv2-video-meta"><b>${b.canal || "YouTube"}</b>${b.titulo_video ? ` · ${b.titulo_video}` : ""} · ` +
        (e ? `trecho ${lv2Fmt(s)} → ${lv2Fmt(e)} (~${Math.max(1, Math.round((e - s) / 60))} min)` : (s ? `a partir de ${lv2Fmt(s)}` : "vídeo completo")) + `</div>`;
      if (b.missao && b.missao.length) {
        inner += `<div class="lv2-mission"><div class="lv2-exp-title" style="margin-top:0">Sua missão enquanto assiste</div><ol>${b.missao.map(m => `<li>${m}</li>`).join("")}</ol></div>`;
      }
      inner += `<div class="lv2-video-wrap" data-src="${src}" data-s="${s}" data-e="${e}"><button type="button" class="lv2-video-play" data-lv2="play">▶ ${e || s ? "Assistir o trecho aqui" : "Assistir aqui"}</button></div>` +
        (e ? `<div class="lv2-clip-note" hidden>⏹ Fim do trecho. <button type="button" class="lv2-clip-replay">↺ Rever o trecho</button></div>` : "") +
        `<a class="lv2-ext" href="https://www.youtube.com/watch?v=${b.id}&t=${s}s" target="_blank" rel="noopener">Abrir no YouTube ↗</a>`;
      if (b.respostas) inner += `<details><summary>Assistiu? Conferir a missão</summary><div>${b.respostas}</div></details>`;
      break;
    }
    case "widget":
      inner += `<div class="lv2-wbox" data-widget="${b.widget}"></div>`;
      if (b.missoes && b.missoes.length) {
        inner += `<div class="lv2-exp-title">Missões</div><ol>${b.missoes.map(m => `<li>${m}</li>`).join("")}</ol>`;
      }
      break;
    case "pratica": {
      const N = { 1: ["🟢", "Aquecimento"], 2: ["🟡", "Aplicação"], 3: ["🔴", "Desafio de IA"] };
      inner += (b.exercicios || []).map((ex, k) => {
        const lv = ex.nivel || 1, nm = N[lv] || N[1];
        const isArr = Array.isArray(ex.valor);
        return `<div class="lv2-ex lv2-lvl-${lv}"><div class="lv2-lvl-tag">Nível ${lv} · ${nm[1]}</div>` +
          `<div><span class="lv2-ex-n">${k + 1}</span>${ex.enunciado}</div>` +
          (ex.valor != null ? `<div class="lv2-check"><input type="text" inputmode="decimal" aria-label="Sua resposta" placeholder="${isArr ? "ex.: 3; -1; 2" : "sua resposta"}">` +
            `<button type="button" class="lv2-btn" data-lv2="check" data-v='${JSON.stringify(ex.valor)}' data-tol="${ex.tol == null ? 0.01 : ex.tol}">Conferir</button><span class="lv2-check-msg"></span></div>` : "") +
          (ex.dicas || []).map((d, j) => `<details><summary>Dica ${j + 1}</summary><div>${d}</div></details>`).join("") +
          `<details><summary>Resolução comentada</summary><div>${ex.resposta || ""}</div></details></div>`;
      }).join("");
      break;
    }
    case "quiz": {
      const qs = b.perguntas || [], min = b.minimo || Math.ceil(qs.length * 2 / 3);
      inner += `<div class="lv2-quiz-box" data-min="${min}" data-n="${qs.length}">` + qs.map((q, k) =>
        `<div class="lv2-qz" data-c="${q.correta}"><div class="lv2-q">${k + 1}. ${q.pergunta}</div><div class="lv2-opts">` +
        (q.opcoes || []).map((o, j) => `<label class="lv2-qopt"><input type="radio" name="lv2qz-${i}-${k}" value="${j}"><span>${o}</span></label>`).join("") +
        `</div><div class="lv2-qz-exp" hidden>${q.explicacao || ""}</div></div>`).join("") +
        `<div class="lv2-wbtns"><button type="button" class="lv2-btn lv2-btn-main" data-lv2="quiz">Corrigir</button></div><div class="lv2-quiz-res"></div></div>`;
      break;
    }
    case "camadas": {
      const src = it => `<div class="lv2-src"><a href="${it.url}" target="_blank" rel="noopener">${it.nome} ↗</a>` +
        `<div class="lv2-src-meta">${[it.trecho, it.tempo ? `~${it.tempo} min` : ""].filter(Boolean).join(" · ")}</div>${it.foco ? `<div>${it.foco}</div>` : ""}</div>`;
      inner += `<div class="lv2-layers" data-locked="1"><div class="lv2-lock"><span>🔒 Libera quando você passar no quiz de saída. Primeiro a base, depois a profundidade.</span>` +
        `<button type="button" class="lv2-btn" data-lv2="unlock">Ver mesmo assim</button></div><div class="lv2-layer-body">`;
      if (b.ponte && b.ponte.length) inner += `<div class="lv2-layer"><div class="lv2-layer-tag">Ponte · acessível e visual</div>${b.ponte.map(src).join("")}</div>`;
      if (b.profundidade && b.profundidade.length) {
        inner += `<div class="lv2-layer"><div class="lv2-layer-tag">Profundidade · leitura guiada (opcional)</div>` + b.profundidade.map(it =>
          `<div class="lv2-src"><a href="${it.url}" target="_blank" rel="noopener">${it.obra} ↗</a><div class="lv2-src-meta">${it.secao || ""}</div>` +
          (it.perguntas && it.perguntas.length ? `<div>Leia procurando responder:</div><ol>${it.perguntas.map(p => `<li>${p}</li>`).join("")}</ol>` : "") +
          `<div style="font-size:.8rem;color:var(--mu)">✍️ Depois, escreva no caderno 3 frases traduzindo o que leu para a linguagem desta aula. Se não conseguir, marque o tópico como “Revisar”.</div></div>`).join("") + `</div>`;
      }
      if (b.revisao && b.revisao.length) inner += `<div class="lv2-layer"><div class="lv2-layer-tag">Para o dia da revisão · outra explicação</div>${b.revisao.map(src).join("")}</div>`;
      inner += `</div></div>`;
      break;
    }
  }
  if (b.depois) inner += `<div class="lv2-prose" style="margin-top:10px">${b.depois}</div>`;
  return `<section class="lv2-block lv2-${tipo}" id="pt-step-card-${i}">` +
         `<header class="lv2-head"><div class="lv2-kicker">${b.rotulo || meta.label}</div>` +
         `<span class="lv2-badge" id="pt-step-badge-${i}">${i}/${n}</span></header>` +
         (b.titulo ? `<h4 class="lv2-title">${b.titulo}</h4>` : "") + inner + `</section>`;
}

function renderPtGuideV2Body(g, topicId) {
  const blocos = g.blocos || [];
  const n = blocos.length;
  const chips = [];
  if (g.duracao) chips.push(`~${g.duracao} min`);
  chips.push(`${n} etapas`);
  const exCount = blocos.filter(b => b.tipo === "desafio" || b.tipo === "pratica").reduce((s, b) => s + (b.exercicios || []).length, 0);
  if (exCount) chips.push(`${exCount} exercícios`);
  if (blocos.some(b => b.tipo === "widget")) chips.push("interativo");
  if (blocos.some(b => b.tipo === "video")) chips.push("vídeo guiado");
  if (blocos.some(b => b.tipo === "laboratorio")) chips.push("laboratório");
  const rv = topicId ? lv2ReadReview()[topicId] : null;
  if (rv && rv.next && rv.next.length) {
    const due = rv.next.find(t => t > (rv.done || 0));
    if (due && due <= Date.now()) chips.push("revisão de hoje");
  }

  let html = `<div class="lv2" data-topic="${topicId || ""}"><div class="lv2-hero">` +
    `<div class="lv2-chips">${chips.map(c => `<span class="lv2-chip">${c}</span>`).join("")}</div>` +
    `<div class="lv2-hook">${g.gancho || ""}</div><div class="lv2-meta">`;
  if (g.objetivos && g.objetivos.length) {
    html += `<div><div class="lv2-meta-title">Ao final desta aula você vai</div><ul>${g.objetivos.map(o => `<li>${o}</li>`).join("")}</ul></div>`;
  }
  if (g.prerequisitos && g.prerequisitos.length) {
    html += `<div><div class="lv2-meta-title">Você vai reutilizar</div><ul>${g.prerequisitos.map(o => `<li>${o}</li>`).join("")}</ul></div>`;
  }
  html += `</div></div>`;
  blocos.forEach((b, k) => { html += lv2Block(b, k + 1, n); });

  html += `<div class="lv2-footer">`;
  if (g.resumo && g.resumo.length) {
    html += `<div class="lv2-meta-title">Para levar desta aula</div><ul>${g.resumo.map(r => `<li>${r}</li>`).join("")}</ul>`;
  }
  if (g.proxima) html += `<div class="lv2-meta-title" style="margin-top:14px">Próximo passo</div><div>${g.proxima}</div>`;
  if (g.referencias && g.referencias.length) {
    html += `<div class="lv2-refs"><div class="lv2-meta-title">Referências desta aula</div><ul>` +
      g.referencias.map(r => `<li><b>${r.obra}</b>${r.trecho ? ` — ${r.trecho}` : ""}${r.uso ? `. <i>${r.uso}</i>` : ""}</li>`).join("") + `</ul></div>`;
  }
  html += `</div></div>`;
  return html;
}

function lv2Strip(html) {
  return String(html || "")
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<\/(p|li|div|h4|tr)>/gi, "\n")
    .replace(/<li>/gi, "- ")
    .replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/g, " ").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&")
    .replace(/\n{3,}/g, "\n\n").trim();
}

function lv2ToMarkdown(g, title) {
  const out = [`## 📘 ${title || ""}`, ""];
  if (g.gancho) out.push(`> ${lv2Strip(g.gancho)}`, "");
  if (g.resumo && g.resumo.length) { out.push("### 🧠 Ideias-chave"); g.resumo.forEach(r => out.push(`- ${lv2Strip(r)}`)); out.push(""); }
  (g.blocos || []).forEach(b => {
    if (b.tipo === "notacao") {
      out.push(`### 🔤 ${lv2Strip(b.titulo) || "Notação"}`);
      (b.itens || []).forEach(it => out.push(`- ${it.simbolo} — *${lv2Strip(it.leitura)}*: ${lv2Strip(it.significado)}`));
      out.push("");
    } else if (b.tipo === "laboratorio" && b.codigo) {
      out.push(`### 🧪 ${lv2Strip(b.titulo) || "Laboratório"}`, "```python", b.codigo, "```", "");
    } else if (b.tipo === "desafio" || b.tipo === "pratica") {
      out.push(`### 🎯 ${lv2Strip(b.titulo) || "Exercícios"}`);
      (b.exercicios || []).forEach((ex, k) => out.push(`${k + 1}. ${lv2Strip(ex.enunciado)}`));
      out.push("");
    }
  });
  return out.join("\n");
}

// =========================================================================
// Interatividade do piloto: palpites, vídeos sob demanda, correção, quiz,
// revisão espaçada e widgets manipuláveis (SVG puro, sem bibliotecas).
// =========================================================================
const LV2_NS = "http://www.w3.org/2000/svg";
const lv2Num = x => (Math.round(x * 100) / 100).toLocaleString("pt-BR");
const lv2Vec = a => "[" + a.map(lv2Num).join("; ") + "]";

function lv2Arrow(x1, y1, x2, y2, color, w, dash) {
  const a = Math.atan2(y2 - y1, x2 - x1), L = Math.hypot(x2 - x1, y2 - y1);
  if (L < 1) return "";
  const h = Math.min(10, L * 0.45), bx = x2 - h * Math.cos(a), by = y2 - h * Math.sin(a);
  const p1 = [bx + h * 0.45 * Math.sin(a), by - h * 0.45 * Math.cos(a)], p2 = [bx - h * 0.45 * Math.sin(a), by + h * 0.45 * Math.cos(a)];
  return `<line x1="${x1}" y1="${y1}" x2="${bx}" y2="${by}" stroke="${color}" stroke-width="${w || 2.6}" ${dash ? 'stroke-dasharray="5 4"' : ""} stroke-linecap="round"/>` +
         `<polygon points="${x2},${y2} ${p1[0]},${p1[1]} ${p2[0]},${p2[1]}" fill="${color}"/>`;
}
function lv2Grid(W, H, X, Y, xr, yr) {
  let s = "";
  for (let x = Math.ceil(xr[0]); x <= xr[1]; x++) s += `<line x1="${X(x)}" y1="0" x2="${X(x)}" y2="${H}" stroke="var(--bd)" stroke-width="${x === 0 ? 1.6 : 0.6}"/>`;
  for (let y = Math.ceil(yr[0]); y <= yr[1]; y++) s += `<line x1="0" y1="${Y(y)}" x2="${W}" y2="${Y(y)}" stroke="var(--bd)" stroke-width="${y === 0 ? 1.6 : 0.6}"/>`;
  return s;
}
function lv2Slider(id, label, min, max, val, step) {
  return `<label>${label}: <b data-out="${id}">${lv2Num(val)}</b><input type="range" data-in="${id}" min="${min}" max="${max}" step="${step || 1}" value="${val}"></label>`;
}
function lv2Bind(el, draw) {
  const get = () => { const o = {}; el.querySelectorAll("[data-in]").forEach(i => { o[i.dataset.in] = parseFloat(i.value); const b = el.querySelector(`[data-out="${i.dataset.in}"]`); if (b) b.textContent = lv2Num(o[i.dataset.in]); }); return o; };
  el.addEventListener("input", () => draw(get()));
  draw(get());
}

const LV2_WIDGETS = {
  // Soma de vetores (regra do paralelogramo) e multiplicação por escalar
  vetores(el) {
    const W = 300, H = 300, R = 8, X = x => W / 2 + x * W / (2 * R), Y = y => H / 2 - y * H / (2 * R);
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" class="lv2-wsvg" role="img" aria-label="Plano com os vetores u, v, u+v e k·v"></svg>` +
      `<div class="lv2-wctl">${lv2Slider("ux", "u₁ (passos para o lado)", -4, 4, 3)}${lv2Slider("uy", "u₂ (passos para cima)", -4, 4, 1)}` +
      `${lv2Slider("vx", "v₁", -4, 4, 1)}${lv2Slider("vy", "v₂", -4, 4, 2)}${lv2Slider("k", "k (escalar que multiplica v)", -2, 2, 1, 0.5)}</div><div class="lv2-wout"></div>`;
    const svg = el.querySelector("svg"), out = el.querySelector(".lv2-wout");
    lv2Bind(el, o => {
      const u = [o.ux, o.uy], v = [o.vx, o.vy], s = [u[0] + v[0], u[1] + v[1]], kv = [o.k * v[0], o.k * v[1]];
      let g = lv2Grid(W, H, X, Y, [-R, R], [-R, R]);
      g += `<line x1="${X(u[0])}" y1="${Y(u[1])}" x2="${X(s[0])}" y2="${Y(s[1])}" stroke="var(--mu)" stroke-width="1.3" stroke-dasharray="4 4"/>`;
      g += `<line x1="${X(v[0])}" y1="${Y(v[1])}" x2="${X(s[0])}" y2="${Y(s[1])}" stroke="var(--mu)" stroke-width="1.3" stroke-dasharray="4 4"/>`;
      g += lv2Arrow(X(0), Y(0), X(kv[0]), Y(kv[1]), "#e8a100", 7) .replace(/stroke-width="7"/, 'stroke-width="7" stroke-opacity=".45"').replace(/fill="#e8a100"/, 'fill="#e8a100" fill-opacity=".55"');
      g += lv2Arrow(X(0), Y(0), X(u[0]), Y(u[1]), "var(--tx)");
      g += lv2Arrow(X(0), Y(0), X(v[0]), Y(v[1]), "var(--mu)");
      g += lv2Arrow(X(0), Y(0), X(s[0]), Y(s[1]), "#10b981", 3.2);
      g += `<text x="6" y="16" font-size="11" fill="var(--tx)" font-weight="700">u</text><text x="20" y="16" font-size="11" fill="var(--mu)" font-weight="700">v</text>` +
           `<text x="34" y="16" font-size="11" fill="#10b981" font-weight="700">u+v</text><text x="64" y="16" font-size="11" fill="#e8a100" font-weight="700">k·v</text>`;
      svg.innerHTML = g;
      let note = "";
      if (s[0] === 0 && s[1] === 0) note = ` <span class="lv2-tag-ok">u + v voltou à origem: v é o “caminho de volta” de u, ou seja, v = −u.</span>`;
      else if (o.k < 0) note = ` <span class="lv2-tag-warn">k negativo inverte o sentido da seta.</span>`;
      else if (o.k === 0) note = ` <span class="lv2-tag-warn">k = 0 encolhe a seta até virar um ponto (o vetor nulo).</span>`;
      out.innerHTML = `u + v = ${lv2Vec(u)} + ${lv2Vec(v)} = <b style="color:#10b981">${lv2Vec(s)}</b> &nbsp;·&nbsp; ${lv2Num(o.k)} · v = <b style="color:#e8a100">${lv2Vec(kv)}</b>.${note}`;
    });
  },

  // Produto escalar como "sombra × comprimento" e o sinal como concordância
  produto_escalar(el) {
    const W = 320, H = 200, S = 32, X = x => W / 2 + x * S, Y = y => H - 36 - y * S;
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" class="lv2-wsvg" role="img" aria-label="Vetores v e w, a sombra de w sobre v e o produto escalar"></svg>` +
      `<div class="lv2-wctl">${lv2Slider("th", "ângulo entre v e w (graus)", 0, 180, 45, 5)}${lv2Slider("lw", "comprimento de w", 0.5, 4.5, 3, 0.5)}${lv2Slider("lv", "comprimento de v", 1, 4.5, 3, 0.5)}</div><div class="lv2-wout"></div>`;
    const svg = el.querySelector("svg"), out = el.querySelector(".lv2-wout");
    lv2Bind(el, o => {
      const t = o.th * Math.PI / 180, v = [o.lv, 0], w = [o.lw * Math.cos(t), o.lw * Math.sin(t)];
      const dot = v[0] * w[0] + v[1] * w[1], cos = Math.cos(t), sh = w[0];
      let g = lv2Grid(W, H, X, Y, [-5, 5], [-1, 5]);
      g += `<line x1="${X(0)}" y1="${Y(0)}" x2="${X(sh)}" y2="${Y(0)}" stroke="#e8a100" stroke-width="7" stroke-opacity=".6" stroke-linecap="round"/>`;
      g += `<line x1="${X(w[0])}" y1="${Y(w[1])}" x2="${X(sh)}" y2="${Y(0)}" stroke="var(--mu)" stroke-width="1.3" stroke-dasharray="4 4"/>`;
      g += lv2Arrow(X(0), Y(0), X(v[0]), Y(v[1]), "var(--mu)");
      g += lv2Arrow(X(0), Y(0), X(w[0]), Y(w[1]), "var(--tx)");
      g += `<text x="${X(v[0]) + 4}" y="${Y(0) + 16}" font-size="12" fill="var(--mu)" font-weight="700">v</text>` +
           `<text x="${X(w[0]) + 5}" y="${Y(w[1]) - 4}" font-size="12" fill="var(--tx)" font-weight="700">w</text>` +
           `<text x="6" y="14" font-size="11" fill="#e8a100" font-weight="700">sombra de w sobre v = ${lv2Num(sh)}</text>`;
      svg.innerHTML = g;
      const eps = 1e-9;
      const verdict = Math.abs(dot) < 1e-6 ? `<span class="lv2-tag-warn">ZERO: perpendiculares, não concordam nem discordam</span>`
        : dot > eps ? `<span class="lv2-tag-ok">POSITIVO: apontam para o mesmo lado (concordam)</span>`
        : `<span class="lv2-tag-bad">NEGATIVO: apontam para lados opostos (discordam)</span>`;
      out.innerHTML = `v = ${lv2Vec(v)}, w = ${lv2Vec(w)}<br>` +
        `Pela regra: v₁w₁ + v₂w₂ = ${lv2Num(v[0])}×${lv2Num(w[0])} + 0×${lv2Num(w[1])} = <b>${lv2Num(dot)}</b><br>` +
        `Pela geometria: sombra × |v| = ${lv2Num(sh)} × ${lv2Num(o.lv)} = <b>${lv2Num(sh * o.lv)}</b> &nbsp;·&nbsp; cos θ = ${lv2Num(cos)}<br>${verdict}`;
    });
  },

  // Descida do gradiente em L(w) = (w − 3)², com taxa de aprendizado ajustável
  descida(el) {
    const W = 320, H = 200, xr = [-3, 9], yMax = 36;
    const X = w => (w - xr[0]) / (xr[1] - xr[0]) * W, Y = l => H - 14 - Math.min(l, yMax) / yMax * (H - 24);
    const L = w => (w - 3) ** 2, dL = w => 2 * (w - 3);
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" class="lv2-wsvg" role="img" aria-label="Curva de perda e os passos da descida do gradiente"></svg>` +
      `<div class="lv2-wctl">${lv2Slider("eta", "η (taxa de aprendizado)", 0.05, 1.1, 0.2, 0.05)}${lv2Slider("w0", "w₀ (chute inicial)", -2, 8, 0, 0.5)}</div>` +
      `<div class="lv2-wbtns"><button type="button" class="lv2-btn lv2-btn-main" data-gd="1">Dar 1 passo</button><button type="button" class="lv2-btn" data-gd="10">+10 passos</button><button type="button" class="lv2-btn" data-gd="0">Recomeçar</button></div>` +
      `<div class="lv2-wout"></div>`;
    const svg = el.querySelector("svg"), out = el.querySelector(".lv2-wout");
    let path = [], cfg = null;
    const paint = () => {
      let g = "";
      let d = "";
      for (let k = 0; k <= 120; k++) { const w = xr[0] + (xr[1] - xr[0]) * k / 120; d += (k ? "L" : "M") + X(w).toFixed(1) + "," + Y(L(w)).toFixed(1); }
      g += `<line x1="0" y1="${H - 14}" x2="${W}" y2="${H - 14}" stroke="var(--bd)"/>`;
      for (let x = xr[0]; x <= xr[1]; x += 3) g += `<text x="${X(x)}" y="${H - 2}" font-size="9" fill="var(--mu)" text-anchor="middle">${x}</text>`;
      g += `<path d="${d}" fill="none" stroke="var(--mu)" stroke-width="2"/>`;
      g += `<line x1="${X(3)}" y1="${Y(0)}" x2="${X(3)}" y2="${Y(0) - 8}" stroke="#10b981" stroke-width="2"/><text x="${X(3) + 4}" y="${Y(0) - 10}" font-size="9" fill="#10b981">mínimo w* = 3</text>`;
      for (let k = 1; k < path.length; k++) {
        const a = path[k - 1], b = path[k];
        if (Math.abs(b) > 60) break;
        g += `<line x1="${X(a)}" y1="${Y(L(a))}" x2="${X(b)}" y2="${Y(L(b))}" stroke="#e8a100" stroke-width="1.6" stroke-dasharray="3 3"/>`;
      }
      path.forEach((w, k) => { if (Math.abs(w) <= 60 && w >= xr[0] && w <= xr[1]) g += `<circle cx="${X(w)}" cy="${Y(L(w))}" r="${k === path.length - 1 ? 5.5 : 3.5}" fill="${k === path.length - 1 ? "#e8a100" : "var(--tx)"}"/>`; });
      svg.innerHTML = g;
      const last = path[path.length - 1], n = path.length - 1;
      let st;
      if (!isFinite(last) || Math.abs(last) > 1e6) st = `<span class="lv2-tag-bad">Explodiu! Com η = ${lv2Num(cfg.eta)} cada passo pula para mais longe do que o anterior. É o famoso “loss virou NaN”.</span>`;
      else if (Math.abs(last - 3) < 0.01) st = `<span class="lv2-tag-ok">Convergiu no passo ${path.findIndex(w => Math.abs(w - 3) < 0.01)}: |w − 3| &lt; 0,01.</span>`;
      else if (n >= 2 && Math.abs(path[n] - path[n - 2]) < 1e-9 && Math.abs(last - 3) > 0.01) st = `<span class="lv2-tag-warn">Ping-pong eterno: com η = 1 o passo pula exatamente para o lado oposto, à mesma distância do mínimo.</span>`;
      else if (n >= 2 && Math.abs(path[n] - 3) > Math.abs(path[n - 1] - 3)) st = `<span class="lv2-tag-bad">Divergindo: a distância até o mínimo está crescendo.</span>`;
      else if (n >= 2 && Math.sign(path[n] - 3) !== Math.sign(path[n - 1] - 3)) st = `<span class="lv2-tag-warn">Zigue-zague: passou do mínimo e voltou. Converge, mas oscilando.</span>`;
      else st = n ? "Descendo..." : "Clique em “Dar 1 passo”.";
      const rows = path.slice(-6).map((w, j) => { const k = path.length - Math.min(6, path.length) + j; return isFinite(w) && Math.abs(w) < 1e6 ? `<tr><td>${k}</td><td>${lv2Num(w)}</td><td>${lv2Num(dL(w))}</td><td>${lv2Num(L(w))}</td></tr>` : ""; }).join("");
      out.innerHTML = `${st}<table class="lv2-wtable"><thead><tr><th>passo t</th><th>w</th><th>gradiente 2(w−3)</th><th>perda L(w)</th></tr></thead><tbody>${rows}</tbody></table>` +
        `<div style="font-size:.76rem;color:var(--mu);margin-top:4px">Regra: w ← w − η · 2(w − 3)</div>`;
    };
    const reset = o => { cfg = o; path = [o.w0]; paint(); };
    lv2Bind(el, reset);
    el.addEventListener("click", ev => {
      const b = ev.target.closest("[data-gd]"); if (!b) return;
      const k = +b.dataset.gd;
      if (k === 0) { reset(cfg); return; }
      for (let j = 0; j < k; j++) { const w = path[path.length - 1]; if (!isFinite(w) || Math.abs(w) > 1e6) break; path.push(w - cfg.eta * dL(w)); }
      paint();
    });
  }
};

function lv2ParseNums(s) {
  return String(s).replace(/[\[\]()]/g, " ").split(/[;\s]+/).filter(Boolean).map(x => parseFloat(x.replace(",", ".")));
}

function lv2ScheduleReview(topicId, score, total) {
  if (!topicId) return null;
  const all = lv2ReadReview(), now = Date.now(), DAY = 86400000;
  const prev = all[topicId] || {};
  const firstPass = !prev.passedAt;
  const rec = Object.assign({}, prev, { score, total, last: now });
  if (firstPass) { rec.passedAt = now; rec.next = LV2_REVIEW_DAYS.map(d => now + d * DAY); }
  else rec.done = now; // refazer o quiz conta como uma revisão concluída
  all[topicId] = rec; lv2WriteReview(all);
  return rec;
}

function lv2ShowReview(root, rec) {
  const box = root.querySelector(".lv2-quiz-res"); if (!box || !rec || !rec.next) return;
  const pend = rec.next.filter(t => t > (rec.done || 0));
  box.insertAdjacentHTML("beforeend", `<div class="lv2-review">🔁 Revisões agendadas: ${rec.next.map(t => (pend.includes(t) ? "" : "✓ ") + lv2Date(t)).join(" · ")}. ` +
    `Nesses dias, refaça este quiz e um exercício 🟡 de cabeça. Se errar, volte o tópico para “Revisar”.</div>`);
}

function lv2Unlock(root) { root.querySelectorAll(".lv2-layers").forEach(l => l.dataset.locked = "0"); }

/* Respostas das atividades (chute, prática e quiz), por aula. Ficam no navegador e vão
   para a nuvem junto com o resto do progresso (campo "extra" -> answers), então ao reabrir
   a aula, em qualquer dispositivo, o que você já respondeu continua lá. */
const LV2_ANS_KEY = "roteiro-answers-v1";
function lv2ReadAnswers() { try { return JSON.parse(localStorage.getItem(LV2_ANS_KEY) || "{}") || {}; } catch (e) { return {}; } }
function lv2SaveAnswer(topicId, mutate) {
  if (!topicId) return;
  const all = lv2ReadAnswers();
  const a = all[topicId] || {};
  a.p = a.p || {}; a.c = a.c || {}; a.q = a.q || {};
  mutate(a);
  a.t = Date.now();
  all[topicId] = a;
  try { localStorage.setItem(LV2_ANS_KEY, JSON.stringify(all)); } catch (e) {}
  if (typeof scheduleAwsRealtimeSync === "function") scheduleAwsRealtimeSync();
}
const lv2BlockIdx = el => { const sec = el.closest(".lv2-block"); return sec ? sec.id.replace("pt-step-card-", "") : "0"; };

function lv2ApplyPalpite(blk, t) {
  const opts = blk.querySelectorAll(".lv2-opt"), ok = t.dataset.ok === "1";
  opts.forEach(o => { o.disabled = true; if (o.dataset.ok === "1") o.classList.add("is-right"); });
  if (!ok) t.classList.add("is-wrong");
  const fb = blk.querySelector(".lv2-fb"); fb.hidden = false;
  fb.querySelector(".lv2-fb-msg").textContent = ok ? "🎯 Acertou o chute!" : "Boa tentativa! Errar o palpite e depois entender o porquê fixa mais do que acertar de primeira.";
  const why = fb.querySelector(`.lv2-fb-why[data-k="${t.dataset.k}"]`); if (why) why.hidden = false;
}

function lv2RunCheck(box) {
  const btn = box.querySelector("[data-lv2=check]"), msg = box.querySelector(".lv2-check-msg");
  const want = JSON.parse(btn.dataset.v), tol = parseFloat(btn.dataset.tol), got = lv2ParseNums(box.querySelector("input").value);
  const W = Array.isArray(want) ? want : [want];
  if (!got.length || got.some(isNaN)) { msg.innerHTML = `<span class="lv2-tag-warn">Digite um número${W.length > 1 ? " para cada componente, separados por ponto e vírgula" : ""}.</span>`; return null; }
  const right = got.length === W.length && W.every((x, k) => Math.abs(x - got[k]) <= tol + 1e-9);
  msg.innerHTML = right ? `<span class="lv2-tag-ok">✓ Correto!</span>` : `<span class="lv2-tag-bad">✗ Ainda não. Abra a dica 1 e tente de novo.</span>`;
  return right;
}

function lv2RunQuiz(root, q, topicId, restoring) {
  const items = q.querySelectorAll(".lv2-qz");
  let score = 0, answered = 0;
  items.forEach(it => {
    const sel = it.querySelector("input:checked");
    it.classList.remove("is-right", "is-wrong");
    if (sel) answered++;
    const right = sel && +sel.value === +it.dataset.c;
    if (right) score++;
    it.classList.add(right ? "is-right" : "is-wrong");
    it.querySelector(".lv2-qz-exp").hidden = false;
  });
  const res = q.querySelector(".lv2-quiz-res"), n = items.length, min = +q.dataset.min;
  if (answered < n) { res.innerHTML = `<span class="lv2-tag-warn">Responda todas as ${n} perguntas antes de corrigir.</span>`; items.forEach(it => { it.classList.remove("is-right", "is-wrong"); it.querySelector(".lv2-qz-exp").hidden = true; }); return false; }
  if (score >= min) {
    res.innerHTML = `<span class="lv2-tag-ok">${score}/${n}: aprovado! A camada “Vá mais fundo” foi liberada.</span>`;
    lv2Unlock(root);
    // Ao restaurar não reagenda as revisões: elas já foram marcadas quando você corrigiu de verdade.
    const rec = restoring ? (lv2ReadReview()[topicId] || null) : lv2ScheduleReview(topicId, score, n);
    if (rec) lv2ShowReview(root, rec);
  } else {
    res.innerHTML = `<span class="lv2-tag-bad">${score}/${n}. Leia as explicações, reveja os blocos marcados com ✗ e tente de novo.</span>`;
  }
  return true;
}

// Reaplica na tela o que já foi respondido nesta aula
function lv2RestoreAnswers(root, topicId) {
  const a = topicId ? lv2ReadAnswers()[topicId] : null;
  if (!a) return;
  Object.keys(a.p || {}).forEach(i => {
    const blk = root.querySelector(`#pt-step-card-${i}`), t = blk && blk.querySelector(`.lv2-opt[data-k="${a.p[i]}"]`);
    if (t) lv2ApplyPalpite(blk, t);
  });
  const checks = root.querySelectorAll(".lv2-check");
  Object.keys(a.c || {}).forEach(k => {
    const box = checks[+k], v = a.c[k];
    if (!box || !v) return;
    box.querySelector("input").value = v[0] || "";
    if (+v[1]) lv2RunCheck(box);
  });
  Object.keys(a.q || {}).forEach(i => {
    const blk = root.querySelector(`#pt-step-card-${i}`), q = blk && blk.querySelector(".lv2-quiz-box"), st = a.q[i];
    if (!q || !st) return;
    q.querySelectorAll(".lv2-qz").forEach((it, k) => {
      const j = (st.s || [])[k];
      const r = j != null && +j >= 0 ? it.querySelector(`input[value="${+j}"]`) : null;
      if (r) r.checked = true;
    });
    if (+st.d) lv2RunQuiz(root, q, topicId, true);
  });
  if (+a.u) lv2Unlock(root);
}

function lv2Init(container) {
  const root = container && container.querySelector(".lv2");
  if (!root || root.__lv2) return;
  root.__lv2 = true;
  const topicId = root.dataset.topic || "";
  root.querySelectorAll(".lv2-wbox").forEach(el => { try { (LV2_WIDGETS[el.dataset.widget] || (() => {}))(el); } catch (e) { console.warn("widget", e); } });
  const rec = topicId ? lv2ReadReview()[topicId] : null;
  if (rec && rec.passedAt) {
    lv2Unlock(root);
    const res = root.querySelector(".lv2-quiz-res");
    if (res) { res.innerHTML = `Você já passou neste quiz (${rec.score}/${rec.total}). Refaça quando chegar o dia da revisão.`; lv2ShowReview(root, rec); }
  }
  lv2RestoreAnswers(root, topicId);

  const checks = [...root.querySelectorAll(".lv2-check")];
  const checkKey = box => String(checks.indexOf(box));
  const quizState = q => [...q.querySelectorAll(".lv2-qz")].map(it => { const sel = it.querySelector("input:checked"); return sel ? +sel.value : -1; });

  // O que você digita fica salvo mesmo antes de clicar em "Conferir"
  let typing;
  root.addEventListener("input", ev => {
    const box = ev.target.closest(".lv2-check");
    if (!box) return;
    clearTimeout(typing);
    typing = setTimeout(() => lv2SaveAnswer(topicId, a => {
      const prev = a.c[checkKey(box)];
      a.c[checkKey(box)] = [ev.target.value, prev && prev[0] === ev.target.value ? prev[1] : 0];
    }), 500);
  });
  // Marcar uma alternativa do quiz já fica salvo
  root.addEventListener("change", ev => {
    const q = ev.target.closest(".lv2-quiz-box");
    if (!q) return;
    lv2SaveAnswer(topicId, a => { a.q[lv2BlockIdx(q)] = { s: quizState(q), d: 0 }; });
  });

  root.addEventListener("click", ev => {
    const t = ev.target.closest("[data-lv2]"); if (!t) return;
    const kind = t.dataset.lv2, blk = t.closest(".lv2-block");
    if (kind === "palpite") {
      lv2ApplyPalpite(blk, t);
      lv2SaveAnswer(topicId, a => { a.p[lv2BlockIdx(blk)] = +t.dataset.k; });
    } else if (kind === "play") {
      const wrap = t.closest(".lv2-video-wrap");
      lv2PlayClip(wrap);
    } else if (kind === "check") {
      const box = t.closest(".lv2-check"), right = lv2RunCheck(box);
      if (right === null) return;
      lv2SaveAnswer(topicId, a => { a.c[checkKey(box)] = [box.querySelector("input").value, 1]; });
    } else if (kind === "quiz") {
      const q = t.closest(".lv2-quiz-box");
      const graded = lv2RunQuiz(root, q, topicId, false);
      lv2SaveAnswer(topicId, a => { a.q[lv2BlockIdx(q)] = { s: quizState(q), d: graded ? 1 : 0 }; });
    } else if (kind === "unlock") {
      lv2Unlock(root);
      lv2SaveAnswer(topicId, a => { a.u = 1; });
    }
  });
}
"""
