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
  tabela:      { icon: "📊", label: "Compare" }
};

function isPtGuideV2(g) { return Boolean(g && g.v === 2 && Array.isArray(g.blocos)); }
function ptGuideCardCount(g) { return isPtGuideV2(g) ? g.blocos.length : 4; }

function lv2Esc(s) {
  return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
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
      inner += `<pre class="lv2-code"><code>${lv2Esc(b.codigo)}</code></pre>`;
      if (b.experimentos && b.experimentos.length) {
        inner += `<div class="lv2-exp-title">🔬 Experimente e observe</div><ul>${b.experimentos.map(e => `<li>${e}</li>`).join("")}</ul>`;
      }
      break;
    case "desafio":
      inner += (b.exercicios || []).map((ex, k) =>
        `<div class="lv2-ex"><div><span class="lv2-ex-n">${k + 1}</span>${ex.enunciado}</div>` +
        (ex.dicas || []).map((d, j) => `<details><summary>💡 Dica ${j + 1}</summary><div>${d}</div></details>`).join("") +
        `<details><summary>✅ Resposta comentada</summary><div>${ex.resposta || ""}</div></details></div>`).join("");
      break;
    case "armadilhas":
      inner += `<div class="lv2-pitfalls">` + (b.itens || []).map(it =>
        `<div class="lv2-pit"><div class="lv2-pit-wrong">✗ ${it.erro}</div><div class="lv2-pit-right">✓ ${it.correcao}</div></div>`).join("") + `</div>`;
      break;
    case "tabela":
      inner += `<div class="lv2-table-wrap"><table class="lv2-table"><thead><tr>${(b.cabecalho || []).map(h => `<th>${h}</th>`).join("")}</tr></thead>` +
               `<tbody>${(b.linhas || []).map(r => `<tr>${r.map(c => `<td>${c}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
      break;
  }
  if (b.depois) inner += `<div class="lv2-prose" style="margin-top:10px">${b.depois}</div>`;
  return `<section class="lv2-block lv2-${tipo}" id="pt-step-card-${i}">` +
         `<header class="lv2-head"><div class="lv2-kicker">${meta.icon} ${b.rotulo || meta.label}</div>` +
         `<span class="lv2-badge" id="pt-step-badge-${i}">${i}/${n}</span></header>` +
         (b.titulo ? `<h4 class="lv2-title">${b.titulo}</h4>` : "") + inner + `</section>`;
}

function renderPtGuideV2Body(g) {
  const blocos = g.blocos || [];
  const n = blocos.length;
  const chips = [];
  if (g.duracao) chips.push(`⏱️ ~${g.duracao} min`);
  chips.push(`🧩 ${n} etapas`);
  const exCount = blocos.filter(b => b.tipo === "desafio").reduce((s, b) => s + (b.exercicios || []).length, 0);
  if (exCount) chips.push(`🎯 ${exCount} exercícios`);
  if (blocos.some(b => b.tipo === "laboratorio")) chips.push("🧪 laboratório");

  let html = `<div class="lv2"><div class="lv2-hero">` +
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
    html += `<div class="lv2-meta-title">🧠 Para levar desta aula</div><ul>${g.resumo.map(r => `<li>${r}</li>`).join("")}</ul>`;
  }
  if (g.proxima) html += `<div class="lv2-meta-title" style="margin-top:10px">➡️ Próximo passo da jornada</div><div>${g.proxima}</div>`;
  if (g.referencias && g.referencias.length) {
    html += `<div class="lv2-refs"><div class="lv2-meta-title">📚 Referências usadas nesta aula</div><ul>` +
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
    } else if (b.tipo === "desafio") {
      out.push(`### 🎯 ${lv2Strip(b.titulo) || "Exercícios"}`);
      (b.exercicios || []).forEach((ex, k) => out.push(`${k + 1}. ${lv2Strip(ex.enunciado)}`));
      out.push("");
    }
  });
  return out.join("\n");
}
"""
