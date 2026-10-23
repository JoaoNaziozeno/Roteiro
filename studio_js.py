# -*- coding: utf-8 -*-
"""
JavaScript para o Estúdio Unificado de Estudo, Auto-Progresso,
Estúdio de Vetores 3D (X, Y, Z) e Lousa de Desenho 2D.
"""

STUDIO_JS = r"""
// =========================================================================
// VARIÁVEIS E ESTADO DO ESTÚDIO UNIFICADO
// =========================================================================
let studySessionTimer = null;
let sessionSeconds = 0;
const SESSION_TARGET_SECONDS = 60; // 60 segundos de estudo ativo para autoconclusão
let autoProgressEnabled = true;

try {
  const savedAuto = localStorage.getItem("roteiro-auto-progress");
  if (savedAuto !== null) autoProgressEnabled = savedAuto === "true";
} catch(e) {}

function getYoutubeEmbedUrl(url) {
  if (!url) return "";
  if (url.includes("youtube.com/embed/")) return url;
  const matchV = url.match(/[?&]v=([^&#]+)/);
  if (matchV) return "https://www.youtube.com/embed/" + matchV[1] + "?enablejsapi=1&rel=0&cc_load_policy=1&cc_lang_pref=pt&hl=pt";
  const matchShort = url.match(/youtu\.be\/([^?&#]+)/);
  if (matchShort) return "https://www.youtube.com/embed/" + matchShort[1] + "?enablejsapi=1&rel=0&cc_load_policy=1&cc_lang_pref=pt&hl=pt";
  const matchL = url.match(/[?&]list=([^&#]+)/);
  if (matchL) return "https://www.youtube.com/embed/videoseries?list=" + matchL[1] + "&enablejsapi=1&rel=0&cc_load_policy=1&cc_lang_pref=pt&hl=pt";
  return url;
}

function copyPtGuideToNotebook(topicId) {
  const topicInfo = (typeof TOPICS_MAP !== "undefined" && TOPICS_MAP[topicId]) || {};
  const g = topicInfo.pt_guide;
  if (!g) return;
  const editor = document.getElementById("modal-note-editor");
  if (!editor) return;

  const cleanIntuicao = (g.intuicao || "").replace(/<\/?[^>]+(>|$)/g, "");
  const cleanExemplo = (g.exemplo || "").replace(/<\/?[^>]+(>|$)/g, "");
  const mdBlock = [
    `## 📘 Resumo em Português: ${topicInfo.title || ""}`,
    "",
    `### 🎯 1. Intuição & Conceito`,
    cleanIntuicao,
    "",
    `### 📐 2. Fórmula Matemática`,
    g.formula || "",
    "",
    `### 🔢 3. Exemplo Prático Passo a Passo`,
    cleanExemplo,
    "",
    `### 🐍 4. Aplicação em Python (IA)`,
    "```python",
    g.codigo || "",
    "```",
    ""
  ].join("\n");

  const cur = editor.value.trim();
  editor.value = cur ? (cur + "\n\n" + mdBlock) : mdBlock;
  onNoteEditorInput();
  setNoteViewMode("split");
  showToast("📘 Apostila em Português + Código copiados para o seu Caderno!");
}

function showToast(msg) {
  let toast = document.getElementById("app-toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "app-toast";
    toast.className = "toast-notice";
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add("show");
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove("show"), 3200);
}

// =========================================================================
// ABRIR E FECHAR O ESTÚDIO UNIFICADO DE ESTUDO & ANOTAÇÕES
// =========================================================================
function openStudyModal(topicId, focusGuide = false) {
  CURRENT_MODAL_TOPIC_ID = topicId;
  const modal = document.getElementById("note-modal");
  if (!modal) return;

  const topicInfo = (typeof TOPICS_MAP !== "undefined" && TOPICS_MAP[topicId]) || {};
  const row = document.getElementById("top-" + topicId);
  const title = topicInfo.title || (row ? row.querySelector(".topic-title-text").textContent : "Tópico de Estudo");
  
  document.getElementById("modal-topic-title").textContent = title;

  const v = PR[topicId] || {};
  const s = v.s || "z";
  updateModalStatusBtn(s);

  const dateInput = document.getElementById("modal-date-input");
  if (dateInput) dateInput.value = v.d || "";

  // Auto-progresso checkbox
  const autoCheck = document.getElementById("modal-auto-prog-check");
  if (autoCheck) autoCheck.checked = autoProgressEnabled;

  // Player de Vídeo e Material
  const playerSect = document.getElementById("study-player-sect");
  const iframe = document.getElementById("modal-video-iframe");
  const extLink = document.getElementById("modal-external-link");
  const docLink = document.getElementById("modal-doc-link");
  const playerTag = document.getElementById("modal-player-tag");
  const playerTitle = document.getElementById("modal-player-title");

  const videoUrl = topicInfo.url || "";
  const docUrl = topicInfo.doc_url || "";
  const videoLabel = topicInfo.label || "▶ Vídeo Aula";
  const docLabel = topicInfo.doc_label || "📖 Material Oficial";
  const ytPtUrl = topicInfo.yt_pt_url || "";
  const ptGuide = topicInfo.pt_guide || null;

  if (videoUrl) {
    if (playerSect) playerSect.style.display = "flex";
    if (iframe) iframe.src = getYoutubeEmbedUrl(videoUrl);
    if (extLink) {
      extLink.href = videoUrl;
      extLink.style.display = "inline-flex";
    }
    if (playerTag) playerTag.textContent = videoLabel;
    if (playerTitle) playerTitle.textContent = title;
  } else {
    if (iframe) iframe.src = "";
    if (extLink) extLink.style.display = "none";
    if (playerTitle) playerTitle.textContent = "Material Teórico e Prático";
  }

  if (docUrl && docLink) {
    docLink.href = docUrl;
    docLink.textContent = ptGuide ? "🌐 Artigo Externo PT-BR ↗" : docLabel;
    docLink.style.display = "inline-flex";
  } else if (docLink) {
    docLink.style.display = "none";
  }

  // Renderizar Apostila Interativa em Português (quando disponível no tópico)
  const guideContainer = document.getElementById("modal-pt-guide-container");
  const defaultTipCard = document.getElementById("modal-default-tip-card");
  if (guideContainer) {
    if (ptGuide) {
      if (defaultTipCard) defaultTipCard.style.display = "none";
      const fmtExemplo = (ptGuide.exemplo || "").replace(/\n/g, "<br>");
      const fmtFormula = (ptGuide.formula || "").replace(/\n/g, "<br>");
      guideContainer.innerHTML = `
        <div class="study-left-card" id="pt-guide-box" style="border:1px solid rgba(99,102,241,.45);background:linear-gradient(160deg,rgba(79,70,229,.09),rgba(16,185,129,.05));padding:16px 18px;border-radius:14px;margin-bottom:10px">
          <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px;margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid var(--bd)">
            <div style="font-size:.95rem;font-weight:850;color:var(--tx);display:flex;align-items:center;gap:7px">
              <span>📘 Apostila Descomplicada em Português (PT-BR)</span>
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:6px">
              <button type="button" onclick="copyPtGuideToNotebook('${topicId}')" style="font:inherit;font-size:.74rem;font-weight:800;padding:5px 11px;border-radius:8px;border:1px solid var(--ac);background:var(--ac);color:#fff;cursor:pointer">
                📥 Copiar para Meu Caderno
              </button>
              ${ytPtUrl ? `<a href="${ytPtUrl}" target="_blank" rel="noopener" style="font-size:.74rem;font-weight:800;padding:5px 11px;border-radius:8px;border:1px solid rgba(239,68,68,.4);background:rgba(239,68,68,.12);color:#ef4444;text-decoration:none;display:inline-flex;align-items:center;gap:4px">🇧🇷 Aulas Brasileiras no YouTube ↗</a>` : ""}
              ${docUrl ? `<a href="${docUrl}" target="_blank" rel="noopener" style="font-size:.74rem;font-weight:800;padding:5px 11px;border-radius:8px;border:1px solid rgba(16,185,129,.4);background:rgba(16,185,129,.12);color:#10b981;text-decoration:none;display:inline-flex;align-items:center;gap:4px">🌐 Fonte Complementar PT-BR ↗</a>` : ""}
            </div>
          </div>

          <div style="display:flex;flex-direction:column;gap:12px;font-size:.86rem;line-height:1.6;color:var(--tx)">
            <div style="background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:11px 14px">
              <div style="font-size:.76rem;font-weight:800;text-transform:uppercase;color:var(--ac);margin-bottom:4px">🎯 1. O que é & Intuição Geométrica (Em Português)</div>
              <div>${ptGuide.intuicao || ""}</div>
            </div>

            <div style="background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:11px 14px">
              <div style="font-size:.76rem;font-weight:800;text-transform:uppercase;color:#f59e0b;margin-bottom:4px">📐 2. Fórmula Matemática & Significado</div>
              <div id="pt-guide-formula-render">${fmtFormula}</div>
            </div>

            <div style="background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:11px 14px">
              <div style="font-size:.76rem;font-weight:800;text-transform:uppercase;color:#10b981;margin-bottom:4px">🔢 3. Exemplo Prático Passo a Passo</div>
              <div id="pt-guide-example-render">${fmtExemplo}</div>
            </div>

            <div style="background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:11px 14px">
              <div style="font-size:.76rem;font-weight:800;text-transform:uppercase;color:#06b6d4;margin-bottom:4px">🐍 4. Como a IA calcula isso em Python / NumPy</div>
              <pre style="margin:6px 0 0;padding:10px 12px;background:#0d1017;color:#e5e7eb;border-radius:8px;overflow-x:auto;font-family:monospace;font-size:.8rem;line-height:1.45"><code>${(ptGuide.codigo || "").replace(/</g, "&lt;").replace(/>/g, "&gt;")}</code></pre>
            </div>
          </div>
        </div>
      `;
      if (typeof renderMathInElement === "function") {
        try {
          renderMathInElement(guideContainer, {
            delimiters: [
              {left: "$$", right: "$$", display: true},
              {left: "$", right: "$", display: false}
            ],
            throwOnError: false
          });
        } catch(e) {}
      }
    } else {
      guideContainer.innerHTML = "";
      if (defaultTipCard) defaultTipCard.style.display = "block";
    }
  }

  // Iniciar Cronômetro da Sessão
  initStudySessionTimer(topicId);

  // Caderno de Anotações (abaixo do vídeo)
  const editor = document.getElementById("modal-note-editor");
  if (editor) {
    editor.value = v.n || "";
    initNoteHistory(editor.value);
    updatePomodoroUI();
    renderModalPreview(editor.value);
    updateNoteStats(editor.value);
  }

  setNoteViewMode(window.innerWidth < 768 ? "editor" : NOTE_VIEW_MODE);
  modal.hidden = false;
  modal.removeAttribute("hidden");
  modal.classList.add("active");
  modal.style.display = "flex";
  document.body.style.overflow = "hidden";

  if (focusGuide) {
    setTimeout(() => {
      const gBox = document.getElementById("pt-guide-box");
      if (gBox) {
        gBox.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }, 120);
  }
}

function openNoteModal(topicId) {
  openStudyModal(topicId);
}

function closeNoteModal() {
  const modal = document.getElementById("note-modal");
  if (!modal) return;

  // Parar vídeo para não tocar áudio em background
  const iframe = document.getElementById("modal-video-iframe");
  if (iframe) iframe.src = "";

  // Parar timer de sessão
  clearInterval(studySessionTimer);
  studySessionTimer = null;

  if (CURRENT_MODAL_TOPIC_ID) {
    const editor = document.getElementById("modal-note-editor");
    const dateInput = document.getElementById("modal-date-input");
    const text = editor ? editor.value : "";
    const date = dateInput ? dateInput.value : "";
    if (!PR[CURRENT_MODAL_TOPIC_ID]) PR[CURRENT_MODAL_TOPIC_ID] = { s: "z", n: "", d: "" };
    PR[CURRENT_MODAL_TOPIC_ID].n = text;
    PR[CURRENT_MODAL_TOPIC_ID].d = date;
    saveLocal();
    paint();
    syncTopicToServer(CURRENT_MODAL_TOPIC_ID);
  }

  modal.hidden = true;
  modal.setAttribute("hidden", "");
  modal.classList.remove("active");
  modal.style.display = "none";
  document.body.style.overflow = "";
  CURRENT_MODAL_TOPIC_ID = null;
}

// Recolher / Expandir Vídeo no Modal
function toggleVideoCollapse() {
  const wrapper = document.getElementById("video-wrapper");
  const btn = document.getElementById("modal-collapse-btn");
  if (!wrapper || !btn) return;

  const isCollapsed = wrapper.classList.toggle("collapsed");
  btn.textContent = isCollapsed ? "▼ Expandir Vídeo" : "▲ Recolher Vídeo";
  btn.title = isCollapsed ? "Expandir vídeo player" : "Recolher vídeo para focar nas anotações";
}

// Alternar Progresso Automático ON/OFF
function toggleAutoProgress(enabled) {
  autoProgressEnabled = enabled;
  try { localStorage.setItem("roteiro-auto-progress", enabled ? "true" : "false"); } catch(e) {}
  showToast(enabled ? "⚡ Progresso Automático ATIVADO: avança conforme seu estudo!" : "⚡ Progresso Automático DESATIVADO: controle 100% manual!");
}

// Timer de Sessão & Auto-Progresso
function initStudySessionTimer(topicId) {
  clearInterval(studySessionTimer);
  sessionSeconds = 0;

  const timerTxt = document.getElementById("session-progress-text");
  const barFill = document.getElementById("session-bar-fill");
  const pctTxt = document.getElementById("session-progress-pct");

  if (barFill) barFill.style.width = "0%";
  if (pctTxt) pctTxt.textContent = "0%";

  studySessionTimer = setInterval(() => {
    sessionSeconds++;
    const mins = String(Math.floor(sessionSeconds / 60)).padStart(2, "0");
    const secs = String(sessionSeconds % 60).padStart(2, "0");

    const pct = Math.min(100, Math.round((sessionSeconds / SESSION_TARGET_SECONDS) * 100));
    if (timerTxt) timerTxt.textContent = `⏱️ Sessão Ativa: ${mins}:${secs} · Status: Estudando`;
    if (barFill) barFill.style.width = `${pct}%`;
    if (pctTxt) pctTxt.textContent = `${pct}%`;

    // Se o progresso automático estiver ativado:
    if (autoProgressEnabled && CURRENT_MODAL_TOPIC_ID === topicId) {
      const curStatus = (PR[topicId] && PR[topicId].s) ? PR[topicId].s : "z";

      // Aos 10 segundos de estudo ativo: marca como "Falta terminar"
      if (sessionSeconds === 10 && curStatus === "z") {
        if (!PR[topicId]) PR[topicId] = { s: "z", n: "", d: "" };
        PR[topicId].s = "r";
        updateModalStatusBtn("r");
        saveLocal();
        paint();
        syncTopicToServer(topicId);
        showToast("🟡 Estudo iniciado! Status atualizado para: Falta terminar");
      }

      // Ao atingir a meta da sessão (60s): marca como "Concluído"
      if (sessionSeconds === SESSION_TARGET_SECONDS && curStatus !== "e") {
        if (!PR[topicId]) PR[topicId] = { s: "z", n: "", d: "" };
        PR[topicId].s = "e";
        updateModalStatusBtn("e");
        saveLocal();
        paint();
        syncTopicToServer(topicId);
        showToast("🟢 Tópico concluído automaticamente! Parabéns pelo foco!");
      }
    }
  }, 1000);
}

// Botão rápido de concluir tópico agora
function markTopicCompleteNow() {
  if (!CURRENT_MODAL_TOPIC_ID) return;
  if (!PR[CURRENT_MODAL_TOPIC_ID]) PR[CURRENT_MODAL_TOPIC_ID] = { s: "z", n: "", d: "" };
  PR[CURRENT_MODAL_TOPIC_ID].s = "e";
  updateModalStatusBtn("e");
  saveLocal();
  paint();
  syncTopicToServer(CURRENT_MODAL_TOPIC_ID);
  showToast("🟢 Tópico registrado como Concluído!");
}

// =========================================================================
// PALETA DE SÍMBOLOS MATEMÁTICOS & FÓRMULAS LATEX
// =========================================================================
function toggleMathPalette(force) {
  const p = document.getElementById("math-symbols-palette");
  if (!p) return;
  const isHidden = p.style.display === "none";
  p.style.display = (force !== undefined) ? (force ? "block" : "none") : (isHidden ? "block" : "none");
}

function insertSymbol(sym) {
  const editor = document.getElementById("modal-note-editor");
  if (!editor) return;
  editor.focus();
  const start = editor.selectionStart;
  const end = editor.selectionEnd;
  const val = editor.value;
  editor.value = val.substring(0, start) + sym + val.substring(end);
  editor.selectionStart = editor.selectionEnd = start + sym.length;
  pushNoteHistory(editor.value, true);
  onNoteEditorInput();
}

function insertLatexTemplate(name) {
  let tmpl = "";
  switch(name) {
    case "vec3d":
      tmpl = "\n$$\\vec{v} = \\begin{bmatrix} x \\\\ y \\\\ z \\end{bmatrix}$$\n";
      break;
    case "matrix2x2":
      tmpl = "\n$$A = \\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}$$\n";
      break;
    case "dotprod":
      tmpl = "\n$$\\vec{u} \\cdot \\vec{v} = u_1 v_1 + u_2 v_2 + u_3 v_3 = \\|\\vec{u}\\| \\|\\vec{v}\\| \\cos(\\theta)$$\n";
      break;
    case "norm":
      tmpl = "\n$$\\|\\vec{v}\\| = \\sqrt{x^2 + y^2 + z^2}$$\n";
      break;
    case "gradient":
      tmpl = "\n$$\\nabla f = \\begin{bmatrix} \\frac{\\partial f}{\\partial x} \\\\ \\frac{\\partial f}{\\partial y} \\\\ \\frac{\\partial f}{\\partial z} \\end{bmatrix}$$\n";
      break;
    case "softmax":
      tmpl = "\n$$\\text{Softmax}(z_i) = \\frac{e^{z_i}}{\\sum_{j=1}^{K} e^{z_j}}$$\n";
      break;
    case "attention":
      tmpl = "\n$$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V$$\n";
      break;
  }
  if (!tmpl) return;
  const editor = document.getElementById("modal-note-editor");
  if (editor) {
    editor.focus();
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    const val = editor.value;
    editor.value = val.substring(0, start) + tmpl + val.substring(end);
    editor.selectionStart = editor.selectionEnd = start + tmpl.length;
    onNoteEditorInput();
  }
  toggleMathPalette(false);
}

// =========================================================================
// ESTÚDIO DE VETORES & GEOMETRIA 3D (EIXOS X, Y, Z INTERATIVO)
// =========================================================================
let rotX = 0.35, rotY = 0.55;
let zoom3D = 28;
let isDragging3D = false;
let lastMouseX = 0, lastMouseY = 0;
let scene3DInitialized = false;

function open3DVectorStudio() {
  const modal = document.getElementById("modal-3d-studio");
  if (!modal) return;
  modal.hidden = false;
  modal.removeAttribute("hidden");
  modal.classList.add("active");
  modal.style.display = "flex";

  if (!scene3DInitialized) {
    init3DCanvasEvents();
    scene3DInitialized = true;
  }
  update3DScene();
}

function close3DVectorStudio() {
  const modal = document.getElementById("modal-3d-studio");
  if (!modal) return;
  modal.hidden = true;
  modal.setAttribute("hidden", "");
  modal.classList.remove("active");
  modal.style.display = "none";
}

function reset3DCamera() {
  rotX = 0.35;
  rotY = 0.55;
  zoom3D = 28;
  update3DScene();
}

function project3D(x, y, z, cx, cy) {
  const cosY = Math.cos(rotY), sinY = Math.sin(rotY);
  const x1 = x * cosY + z * sinY;
  const z1 = -x * sinY + z * cosY;

  const cosX = Math.cos(rotX), sinX = Math.sin(rotX);
  const y2 = y * cosX - z1 * sinX;
  const z2 = y * sinX + z1 * cosX;

  const dist = 500;
  const fov = dist / (dist + z2 * zoom3D * 0.4);
  const px = cx + x1 * zoom3D * fov;
  const py = cy - y2 * zoom3D * fov;
  return { x: px, y: py, z: z2 };
}

function draw3DArrowHead(ctx, from, to, color, size = 6) {
  const dx = to.x - from.x;
  const dy = to.y - from.y;
  const angle = Math.atan2(dy, dx);
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(to.x, to.y);
  ctx.lineTo(to.x - size * 2 * Math.cos(angle - Math.PI / 6), to.y - size * 2 * Math.sin(angle - Math.PI / 6));
  ctx.lineTo(to.x - size * 2 * Math.cos(angle + Math.PI / 6), to.y - size * 2 * Math.sin(angle + Math.PI / 6));
  ctx.closePath();
  ctx.fill();
}

function draw3DCube(ctx, cx, cy, s) {
  const v = [
    [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],
    [-s, -s, s],  [s, -s, s],  [s, s, s],  [-s, s, s]
  ].map(pt => project3D(pt[0], pt[1], pt[2], cx, cy));

  ctx.strokeStyle = "rgba(139, 92, 246, 0.45)";
  ctx.lineWidth = 1.5;
  const edges = [
    [0,1],[1,2],[2,3],[3,0],
    [4,5],[5,6],[6,7],[7,4],
    [0,4],[1,5],[2,6],[3,7]
  ];
  edges.forEach(([i, j]) => {
    ctx.beginPath();
    ctx.moveTo(v[i].x, v[i].y);
    ctx.lineTo(v[j].x, v[j].y);
    ctx.stroke();
  });
}

function draw3DPlane(ctx, cx, cy, s) {
  const corners = [
    [-s, 0, -s], [s, 0, -s], [s, 0, s], [-s, 0, s]
  ].map(pt => project3D(pt[0], pt[1], pt[2], cx, cy));

  ctx.fillStyle = "rgba(6, 182, 212, 0.15)";
  ctx.strokeStyle = "rgba(6, 182, 212, 0.6)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(corners[0].x, corners[0].y);
  corners.forEach(pt => ctx.lineTo(pt.x, pt.y));
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
}

function draw3DPyramid(ctx, cx, cy, s) {
  const base = [
    [-s, 0, -s], [s, 0, -s], [s, 0, s], [-s, 0, s]
  ].map(pt => project3D(pt[0], pt[1], pt[2], cx, cy));
  const apex = project3D(0, s * 1.5, 0, cx, cy);

  ctx.strokeStyle = "rgba(232, 161, 0, 0.6)";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(base[0].x, base[0].y);
  base.forEach(pt => ctx.lineTo(pt.x, pt.y));
  ctx.closePath();
  ctx.stroke();

  base.forEach(pt => {
    ctx.beginPath();
    ctx.moveTo(pt.x, pt.y);
    ctx.lineTo(apex.x, apex.y);
    ctx.stroke();
  });
}

function draw3DSphere(ctx, cx, cy, r) {
  const p0 = project3D(0, 0, 0, cx, cy);
  ctx.strokeStyle = "rgba(47, 163, 107, 0.5)";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.arc(p0.x, p0.y, r * zoom3D, 0, Math.PI * 2);
  ctx.stroke();
}

function update3DScene() {
  const canvas = document.getElementById("canvas-3d");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = canvas.width, h = canvas.height;
  const cx = w / 2, cy = h / 2;

  // Limpar fundo escuro
  ctx.fillStyle = "#0f1218";
  ctx.fillRect(0, 0, w, h);

  // Grade no plano XZ
  const showGrid = document.getElementById("v3d-show-grid")?.checked ?? true;
  if (showGrid) {
    ctx.strokeStyle = "rgba(255,255,255,0.08)";
    ctx.lineWidth = 1;
    const gridRange = 6;
    for (let i = -gridRange; i <= gridRange; i++) {
      const p1 = project3D(i, 0, -gridRange, cx, cy);
      const p2 = project3D(i, 0, gridRange, cx, cy);
      ctx.beginPath();
      ctx.moveTo(p1.x, p1.y);
      ctx.lineTo(p2.x, p2.y);
      ctx.stroke();

      const p3 = project3D(-gridRange, 0, i, cx, cy);
      const p4 = project3D(gridRange, 0, i, cx, cy);
      ctx.beginPath();
      ctx.moveTo(p3.x, p3.y);
      ctx.lineTo(p4.x, p4.y);
      ctx.stroke();
    }
  }

  // Eixos X, Y, Z
  const axisLen = 6.5;
  const p0 = project3D(0, 0, 0, cx, cy);

  // Eixo X (Vermelho)
  const px = project3D(axisLen, 0, 0, cx, cy);
  const pnx = project3D(-axisLen, 0, 0, cx, cy);
  ctx.strokeStyle = "#ef4444";
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(pnx.x, pnx.y);
  ctx.lineTo(px.x, px.y);
  ctx.stroke();
  draw3DArrowHead(ctx, p0, px, "#ef4444");
  ctx.fillStyle = "#ef4444";
  ctx.font = "bold 13px system-ui";
  ctx.fillText("+X", px.x + 8, px.y);

  // Eixo Y (Verde)
  const py = project3D(0, axisLen, 0, cx, cy);
  const pny = project3D(0, -axisLen, 0, cx, cy);
  ctx.strokeStyle = "#10b981";
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(pny.x, pny.y);
  ctx.lineTo(py.x, py.y);
  ctx.stroke();
  draw3DArrowHead(ctx, p0, py, "#10b981");
  ctx.fillStyle = "#10b981";
  ctx.fillText("+Y", py.x + 8, py.y);

  // Eixo Z (Azul)
  const pz = project3D(0, 0, axisLen, cx, cy);
  const pnz = project3D(0, 0, -axisLen, cx, cy);
  ctx.strokeStyle = "#3b82f6";
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(pnz.x, pnz.y);
  ctx.lineTo(pz.x, pz.y);
  ctx.stroke();
  draw3DArrowHead(ctx, p0, pz, "#3b82f6");
  ctx.fillStyle = "#3b82f6";
  ctx.fillText("+Z", pz.x + 8, pz.y);

  // Formas Geométricas 3D Opcionais
  const shape = document.getElementById("v3d-shape-select")?.value || "cube";
  if (shape === "cube") draw3DCube(ctx, cx, cy, 3);
  else if (shape === "plane") draw3DPlane(ctx, cx, cy, 4);
  else if (shape === "pyramid") draw3DPyramid(ctx, cx, cy, 3);
  else if (shape === "sphere") draw3DSphere(ctx, cx, cy, 2.5);

  // Vetor 1 (Roxo)
  const x1 = parseFloat(document.getElementById("v3d-x1")?.value || 3);
  const y1 = parseFloat(document.getElementById("v3d-y1")?.value || 4);
  const z1 = parseFloat(document.getElementById("v3d-z1")?.value || 2);
  const pv1 = project3D(x1, y1, z1, cx, cy);

  ctx.strokeStyle = "#a855f7";
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(p0.x, p0.y);
  ctx.lineTo(pv1.x, pv1.y);
  ctx.stroke();
  draw3DArrowHead(ctx, p0, pv1, "#a855f7", 8);
  ctx.fillStyle = "#c084fc";
  ctx.font = "bold 13px system-ui";
  ctx.fillText(`v1 [${x1}, ${y1}, ${z1}]`, pv1.x + 10, pv1.y - 6);

  // Vetor 2 (Ciano)
  const x2 = parseFloat(document.getElementById("v3d-x2")?.value || 1);
  const y2 = parseFloat(document.getElementById("v3d-y2")?.value || 0);
  const z2 = parseFloat(document.getElementById("v3d-z2")?.value || 3);
  const pv2 = project3D(x2, y2, z2, cx, cy);

  ctx.strokeStyle = "#06b6d4";
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(p0.x, p0.y);
  ctx.lineTo(pv2.x, pv2.y);
  ctx.stroke();
  draw3DArrowHead(ctx, p0, pv2, "#06b6d4", 8);
  ctx.fillStyle = "#22d3ee";
  ctx.fillText(`v2 [${x2}, ${y2}, ${z2}]`, pv2.x + 10, pv2.y - 6);

  // Cálculos Vetoriais
  const norm1 = Math.sqrt(x1*x1 + y1*y1 + z1*z1);
  const norm2 = Math.sqrt(x2*x2 + y2*y2 + z2*z2);
  const dot = x1*x2 + y1*y2 + z1*z2;
  const cosTheta = Math.max(-1, Math.min(1, dot / ((norm1 * norm2) || 1)));
  const angleDeg = (Math.acos(cosTheta) * 180 / Math.PI).toFixed(1);

  const elNorm1 = document.getElementById("v3d-norm-1");
  if (elNorm1) elNorm1.textContent = `||v1|| = ${norm1.toFixed(2)}`;
  const elNorm2 = document.getElementById("v3d-norm-2");
  if (elNorm2) elNorm2.textContent = `||v2|| = ${norm2.toFixed(2)}`;
  const elDot = document.getElementById("v3d-dot-prod");
  if (elDot) elDot.textContent = dot.toFixed(2);
  const elAngle = document.getElementById("v3d-angle");
  if (elAngle) elAngle.textContent = `${angleDeg}° (${(dot > 0 ? "Ângulo Agudo" : dot < 0 ? "Ângulo Obtuso" : "Ortogonais / Perpendiculares")})`;
}

function init3DCanvasEvents() {
  const canvas = document.getElementById("canvas-3d");
  if (!canvas) return;

  canvas.addEventListener("mousedown", e => {
    isDragging3D = true;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
  });

  window.addEventListener("mousemove", e => {
    if (!isDragging3D) return;
    const dx = e.clientX - lastMouseX;
    const dy = e.clientY - lastMouseY;
    rotY += dx * 0.01;
    rotX += dy * 0.01;
    rotX = Math.max(-Math.PI / 2 + 0.1, Math.min(Math.PI / 2 - 0.1, rotX));
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
    update3DScene();
  });

  window.addEventListener("mouseup", () => { isDragging3D = false; });

  canvas.addEventListener("wheel", e => {
    zoom3D = Math.max(12, Math.min(55, zoom3D - e.deltaY * 0.03));
    update3DScene();
    e.preventDefault();
  }, { passive: false });

  // Touch para dispositivos móveis
  canvas.addEventListener("touchstart", e => {
    if (e.touches.length === 1) {
      isDragging3D = true;
      lastMouseX = e.touches[0].clientX;
      lastMouseY = e.touches[0].clientY;
    }
  });

  canvas.addEventListener("touchmove", e => {
    if (!isDragging3D || e.touches.length !== 1) return;
    const dx = e.touches[0].clientX - lastMouseX;
    const dy = e.touches[0].clientY - lastMouseY;
    rotY += dx * 0.012;
    rotX += dy * 0.012;
    lastMouseX = e.touches[0].clientX;
    lastMouseY = e.touches[0].clientY;
    update3DScene();
    e.preventDefault();
  }, { passive: false });

  canvas.addEventListener("touchend", () => { isDragging3D = false; });
}

function insert3DSnapshotToNotes() {
  const canvas = document.getElementById("canvas-3d");
  if (!canvas) return;
  const dataUrl = canvas.toDataURL("image/png");

  const x1 = document.getElementById("v3d-x1")?.value || 3;
  const y1 = document.getElementById("v3d-y1")?.value || 4;
  const z1 = document.getElementById("v3d-z1")?.value || 2;
  const x2 = document.getElementById("v3d-x2")?.value || 1;
  const y2 = document.getElementById("v3d-y2")?.value || 0;
  const z2 = document.getElementById("v3d-z2")?.value || 3;
  const dot = document.getElementById("v3d-dot-prod")?.textContent || "";
  const angle = document.getElementById("v3d-angle")?.textContent || "";

  const snippet = `\n\n![Gráfico Vetorial 3D (Eixos X, Y, Z)](${dataUrl})\n\n> 📐 **Análise Geométrica 3D:**\n> - $\\vec{v}_1 = \\begin{bmatrix} ${x1} \\\\ ${y1} \\\\ ${z1} \\end{bmatrix}$, $\\vec{v}_2 = \\begin{bmatrix} ${x2} \\\\ ${y2} \\\\ ${z2} \\end{bmatrix}$\n> - **Produto Escalar $\\vec{v}_1 \\cdot \\vec{v}_2$:** ${dot} | **Ângulo $\\theta$:** ${angle}\n\n`;

  const editor = document.getElementById("modal-note-editor");
  if (editor) {
    editor.value += snippet;
    pushNoteHistory(editor.value, true);
    onNoteEditorInput();
  }
  close3DVectorStudio();
  showToast("📸 Gráfico 3D inserido nas suas anotações com sucesso!");
}

// =========================================================================
// LOUSA DE DESENHO GEOMÉTRICO 2D (WHITEBOARD CANVAS)
// =========================================================================
let currentDrawTool = "pen";
let currentDrawColor = "#8b5cf6";
let isDrawingWhiteboard = false;
let drawStartX = 0, drawStartY = 0;
let whiteboardSnapshot = null;
let whiteboardInitialized = false;

function openWhiteboardDrawer() {
  const modal = document.getElementById("modal-draw-studio");
  if (!modal) return;
  modal.hidden = false;
  modal.removeAttribute("hidden");
  modal.classList.add("active");
  modal.style.display = "flex";

  if (!whiteboardInitialized) {
    initWhiteboardEvents();
    clearWhiteboard();
    whiteboardInitialized = true;
  }
}

function closeWhiteboardDrawer() {
  const modal = document.getElementById("modal-draw-studio");
  if (!modal) return;
  modal.hidden = true;
  modal.setAttribute("hidden", "");
  modal.classList.remove("active");
  modal.style.display = "none";
}

function setDrawTool(tool) {
  currentDrawTool = tool;
  document.querySelectorAll(".draw-tool-btn").forEach(b => {
    b.classList.toggle("active", b.dataset.tool === tool);
  });
}

function setDrawColor(color) {
  currentDrawColor = color;
  document.querySelectorAll(".color-dot").forEach(d => {
    d.classList.toggle("active", d.style.background === color);
  });
}

function clearWhiteboard() {
  const canvas = document.getElementById("whiteboard-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = "#11141c";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function initWhiteboardEvents() {
  const canvas = document.getElementById("whiteboard-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  function getPos(e) {
    const rect = canvas.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    return {
      x: (clientX - rect.left) * (canvas.width / rect.width),
      y: (clientY - rect.top) * (canvas.height / rect.height)
    };
  }

  function start(e) {
    isDrawingWhiteboard = true;
    const pos = getPos(e);
    drawStartX = pos.x;
    drawStartY = pos.y;
    whiteboardSnapshot = ctx.getImageData(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = currentDrawColor;
    ctx.lineWidth = 3;
    ctx.lineCap = "round";

    if (currentDrawTool === "pen") {
      ctx.beginPath();
      ctx.moveTo(pos.x, pos.y);
    }
  }

  function move(e) {
    if (!isDrawingWhiteboard) return;
    const pos = getPos(e);

    if (currentDrawTool === "pen") {
      ctx.lineTo(pos.x, pos.y);
      ctx.stroke();
    } else {
      ctx.putImageData(whiteboardSnapshot, 0, 0);
      ctx.beginPath();
      ctx.strokeStyle = currentDrawColor;
      ctx.lineWidth = 3;

      if (currentDrawTool === "line") {
        ctx.moveTo(drawStartX, drawStartY);
        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();
      } else if (currentDrawTool === "arrow") {
        ctx.moveTo(drawStartX, drawStartY);
        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();
        draw3DArrowHead(ctx, { x: drawStartX, y: drawStartY }, { x: pos.x, y: pos.y }, currentDrawColor, 7);
      } else if (currentDrawTool === "rect") {
        ctx.strokeRect(drawStartX, drawStartY, pos.x - drawStartX, pos.y - drawStartY);
      } else if (currentDrawTool === "circle") {
        const rad = Math.hypot(pos.x - drawStartX, pos.y - drawStartY);
        ctx.arc(drawStartX, drawStartY, rad, 0, Math.PI * 2);
        ctx.stroke();
      } else if (currentDrawTool === "axes") {
        // Desenha eixos cartesianos X e Y a partir do ponto inicial
        ctx.moveTo(drawStartX - 100, drawStartY);
        ctx.lineTo(drawStartX + 100, drawStartY);
        ctx.stroke();
        draw3DArrowHead(ctx, {x: drawStartX, y: drawStartY}, {x: drawStartX + 100, y: drawStartY}, currentDrawColor, 6);

        ctx.moveTo(drawStartX, drawStartY + 100);
        ctx.lineTo(drawStartX, drawStartY - 100);
        ctx.stroke();
        draw3DArrowHead(ctx, {x: drawStartX, y: drawStartY}, {x: drawStartX, y: drawStartY - 100}, currentDrawColor, 6);
      }
    }
    if (e.cancelable) e.preventDefault();
  }

  function end() {
    isDrawingWhiteboard = false;
  }

  canvas.addEventListener("mousedown", start);
  canvas.addEventListener("mousemove", move);
  canvas.addEventListener("mouseup", end);
  canvas.addEventListener("mouseleave", end);

  canvas.addEventListener("touchstart", start, { passive: false });
  canvas.addEventListener("touchmove", move, { passive: false });
  canvas.addEventListener("touchend", end);
}

function insertWhiteboardToNotes() {
  const canvas = document.getElementById("whiteboard-canvas");
  if (!canvas) return;
  const dataUrl = canvas.toDataURL("image/png");
  const snippet = `\n\n![Esquema / Desenho Geométrico](${dataUrl})\n\n`;

  const editor = document.getElementById("modal-note-editor");
  if (editor) {
    editor.value += snippet;
    pushNoteHistory(editor.value, true);
    onNoteEditorInput();
  }
  closeWhiteboardDrawer();
  showToast("📥 Desenho inserido nas suas anotações com sucesso!");
}


// =========================================================================
// 1. GERENCIADOR DE HISTÓRICO UNDO / REDO (CTRL + Z / CTRL + Y)
// =========================================================================
let noteHistoryStack = [];
let noteHistoryIndex = -1;
let noteHistoryDebounce = null;
const MAX_HISTORY = 100;

function initNoteHistory(initialVal) {
  noteHistoryStack = [initialVal || ""];
  noteHistoryIndex = 0;
  updateUndoRedoButtons();

  const editor = document.getElementById("modal-note-editor");
  if (editor && !editor._hasHistoryListener) {
    editor._hasHistoryListener = true;
    editor.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z") {
        e.preventDefault();
        if (e.shiftKey) {
          redoNote();
        } else {
          undoNote();
        }
      } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "y") {
        e.preventDefault();
        redoNote();
      }
    });
  }
}

function pushNoteHistory(val, immediate) {
  if (noteHistoryIndex >= 0 && noteHistoryStack[noteHistoryIndex] === val) return;

  if (immediate) {
    clearTimeout(noteHistoryDebounce);
    _recordHistory(val);
  } else {
    clearTimeout(noteHistoryDebounce);
    noteHistoryDebounce = setTimeout(() => {
      _recordHistory(val);
    }, 350);
  }
}

function _recordHistory(val) {
  noteHistoryStack = noteHistoryStack.slice(0, noteHistoryIndex + 1);
  noteHistoryStack.push(val);
  if (noteHistoryStack.length > MAX_HISTORY) {
    noteHistoryStack.shift();
  }
  noteHistoryIndex = noteHistoryStack.length - 1;
  updateUndoRedoButtons();
}

function undoNote() {
  if (noteHistoryIndex > 0) {
    noteHistoryIndex--;
    applyHistoryToEditor(noteHistoryStack[noteHistoryIndex]);
    showToast("↩ Desfeito");
  }
}

function redoNote() {
  if (noteHistoryIndex < noteHistoryStack.length - 1) {
    noteHistoryIndex++;
    applyHistoryToEditor(noteHistoryStack[noteHistoryIndex]);
    showToast("↪ Refeito");
  }
}

function applyHistoryToEditor(val) {
  const editor = document.getElementById("modal-note-editor");
  if (!editor) return;
  editor.value = val;
  updateUndoRedoButtons();
  if (typeof renderModalPreview === "function") renderModalPreview(val);
  if (typeof updateNoteStats === "function") updateNoteStats(val);

  if (CURRENT_MODAL_TOPIC_ID) {
    if (!PR[CURRENT_MODAL_TOPIC_ID]) PR[CURRENT_MODAL_TOPIC_ID] = { s: "z", n: "", d: "" };
    PR[CURRENT_MODAL_TOPIC_ID].n = val;
    saveLocal();
    if (typeof syncTopicToServer === "function") syncTopicToServer(CURRENT_MODAL_TOPIC_ID);
  }
}

function updateUndoRedoButtons() {
  const uBtn = document.getElementById("tb-btn-undo");
  const rBtn = document.getElementById("tb-btn-redo");
  if (uBtn) {
    const canUndo = noteHistoryIndex > 0;
    uBtn.disabled = !canUndo;
    uBtn.style.opacity = canUndo ? "1" : "0.35";
  }
  if (rBtn) {
    const canRedo = noteHistoryIndex < noteHistoryStack.length - 1;
    rBtn.disabled = !canRedo;
    rBtn.style.opacity = canRedo ? "1" : "0.35";
  }
}

// =========================================================================
// 2. DIVISÓRIA ARRASTÁVEL ENTRE VÍDEO E ANOTAÇÕES (SPLIT RESIZER)
// =========================================================================
function initSplitResizer() {
  const resizer = document.getElementById("study-split-resizer");
  const container = document.getElementById("study-columns-layout");
  const leftCol = document.getElementById("study-player-sect");
  const rightCol = document.getElementById("study-notes-col");
  if (!resizer || !container || !leftCol || !rightCol) return;

  try {
    const savedRatio = localStorage.getItem("roteiro-split-ratio");
    if (savedRatio && window.innerWidth > 1040) {
      const r = parseFloat(savedRatio);
      if (r >= 20 && r <= 80) {
        leftCol.style.flex = `0 0 ${r}%`;
        leftCol.style.width = `${r}%`;
        leftCol.style.maxWidth = `${r}%`;
        rightCol.style.flex = `1 1 ${100 - r}%`;
        rightCol.style.width = `${100 - r}%`;
      }
    }
  } catch(e) {}

  let isDragging = false;

  resizer.addEventListener("mousedown", (e) => {
    if (window.innerWidth <= 1040) return;
    isDragging = true;
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";
    resizer.classList.add("dragging");
    const iframe = document.getElementById("modal-video-iframe");
    if (iframe) iframe.style.pointerEvents = "none";
  });

  document.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    const rect = container.getBoundingClientRect();
    const offsetX = e.clientX - rect.left;
    let pct = (offsetX / rect.width) * 100;
    pct = Math.max(22, Math.min(78, pct));

    leftCol.style.flex = `0 0 ${pct}%`;
    leftCol.style.width = `${pct}%`;
    leftCol.style.maxWidth = `${pct}%`;
    rightCol.style.flex = `1 1 ${100 - pct}%`;
    rightCol.style.width = `${100 - pct}%`;
  });

  document.addEventListener("mouseup", () => {
    if (isDragging) {
      isDragging = false;
      document.body.style.cursor = "";
      document.body.style.userSelect = "";
      resizer.classList.remove("dragging");
      const iframe = document.getElementById("modal-video-iframe");
      if (iframe) iframe.style.pointerEvents = "auto";

      const rect = container.getBoundingClientRect();
      const leftRect = leftCol.getBoundingClientRect();
      const pct = Math.round((leftRect.width / rect.width) * 100);
      try { localStorage.setItem("roteiro-split-ratio", pct); } catch(e) {}
    }
  });

  resizer.addEventListener("dblclick", () => {
    leftCol.style.flex = "0 0 50%";
    leftCol.style.width = "50%";
    leftCol.style.maxWidth = "50%";
    rightCol.style.flex = "1 1 50%";
    rightCol.style.width = "50%";
    try { localStorage.setItem("roteiro-split-ratio", "50"); } catch(e) {}
    showToast("Divisão resetada para 50% / 50%");
  });
}

// =========================================================================
// 3. MARCADORES DE TEMPO INTERATIVOS NO VÍDEO (TIMESTAMPS & SEEK)
// =========================================================================
function formatSeconds(sec) {
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

function seekVideoToSeconds(sec) {
  const iframe = document.getElementById("modal-video-iframe");
  if (!iframe) return;

  let s = 0;
  if (typeof sec === "number") {
    s = sec;
  } else if (typeof sec === "string") {
    const parts = sec.trim().split(":").map(Number);
    if (parts.length === 2) s = parts[0] * 60 + parts[1];
    else if (parts.length === 3) s = parts[0] * 3600 + parts[1] * 60 + parts[2];
    else s = Number(sec) || 0;
  }

  try {
    iframe.contentWindow.postMessage(JSON.stringify({
      event: "command",
      func: "seekTo",
      args: [s, true]
    }), "*");
  } catch(e) {}

  showToast(`⏩ Vídeo avançado para ${formatSeconds(s)}`);
}

function insertTimestampToNotes() {
  const editor = document.getElementById("modal-note-editor");
  if (!editor) return;
  editor.focus();

  const cur = sessionSeconds || 0;
  const stamp = `⏱️ [${formatSeconds(cur)}] `;

  const start = editor.selectionStart;
  const end = editor.selectionEnd;
  const text = editor.value;
  editor.value = text.substring(0, start) + stamp + text.substring(end);
  editor.selectionStart = editor.selectionEnd = start + stamp.length;
  pushNoteHistory(editor.value, true);
  onNoteEditorInput();
  showToast(`Marcador ${stamp.trim()} inserido!`);
}

// =========================================================================
// 4. PRONÚNCIA EM INGLÊS NATIVO (TEXT-TO-SPEECH)
// =========================================================================
function speakSelectedText(lang = "en-US") {
  if (!window.speechSynthesis) {
    showToast("⚠️ Navegador sem suporte a síntese de voz");
    return;
  }

  const editor = document.getElementById("modal-note-editor");
  let selected = "";
  if (editor && editor.selectionStart !== editor.selectionEnd) {
    selected = editor.value.substring(editor.selectionStart, editor.selectionEnd).trim();
  }
  if (!selected && window.getSelection) {
    selected = window.getSelection().toString().trim();
  }
  if (!selected) {
    const titleEl = document.getElementById("modal-topic-title");
    selected = titleEl ? titleEl.textContent : "";
  }

  if (!selected) {
    showToast("Selecione um texto para ouvir a pronúncia");
    return;
  }

  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(selected);
  u.lang = lang;
  u.rate = 0.95;
  window.speechSynthesis.speak(u);
  showToast(`🔊 Ouvindo pronúncia: "${selected.slice(0, 32)}${selected.length > 32 ? '...' : ''}"`);
}

// =========================================================================
// 5. TEMPORIZADOR POMODORO INTEGRADO (COM ALERTA SONORO WEB AUDIO)
// =========================================================================
let pomodoroTimer = null;
let pomodoroRemaining = 25 * 60;
let pomodoroRunning = false;
let pomodoroTodayCount = 0;

try {
  const todayKey = "roteiro-pomo-" + new Date().toISOString().slice(0, 10);
  const savedPomo = localStorage.getItem(todayKey);
  if (savedPomo) pomodoroTodayCount = parseInt(savedPomo, 10) || 0;
} catch(e) {}

function updatePomodoroUI() {
  const btn = document.getElementById("pomo-btn");
  const badge = document.getElementById("pomo-count-badge");
  if (btn) {
    const mins = String(Math.floor(pomodoroRemaining / 60)).padStart(2, "0");
    const secs = String(pomodoroRemaining % 60).padStart(2, "0");
    btn.textContent = `🍅 ${mins}:${secs}`;
    btn.classList.toggle("running", pomodoroRunning);
    btn.title = pomodoroRunning ? "Pausar Pomodoro" : "Iniciar Pomodoro (25 min de foco)";
  }
  if (badge) {
    badge.textContent = `${pomodoroTodayCount} 🍅`;
  }
}

function togglePomodoro() {
  if (pomodoroRunning) {
    clearInterval(pomodoroTimer);
    pomodoroRunning = false;
    updatePomodoroUI();
    showToast("⏸️ Pomodoro pausado");
  } else {
    pomodoroRunning = true;
    updatePomodoroUI();
    showToast("▶️ Pomodoro iniciado! 25 min de foco total");
    pomodoroTimer = setInterval(() => {
      pomodoroRemaining--;
      if (pomodoroRemaining <= 0) {
        clearInterval(pomodoroTimer);
        pomodoroRunning = false;
        pomodoroRemaining = 25 * 60;
        pomodoroTodayCount++;
        try {
          const todayKey = "roteiro-pomo-" + new Date().toISOString().slice(0, 10);
          localStorage.setItem(todayKey, String(pomodoroTodayCount));
        } catch(e) {}
        playZenBell();
        updatePomodoroUI();
        alert("🎉 Ciclo Pomodoro Concluído!\nVocê completou 25 minutos de estudo de alta intensidade. Faça uma pausa de 5 minutos!");
      } else {
        updatePomodoroUI();
      }
    }, 1000);
  }
}

function resetPomodoro() {
  clearInterval(pomodoroTimer);
  pomodoroRunning = false;
  pomodoroRemaining = 25 * 60;
  updatePomodoroUI();
  showToast("↺ Pomodoro resetado para 25:00");
}

function playZenBell() {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(587.33, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.35);
    gain.gain.setValueAtTime(0.3, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 2.5);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 2.6);
  } catch(e) {}
}

// =========================================================================
// 6. SISTEMA DE FLASHCARDS & REVISÃO ESPAÇADA (ANKI LITE)
// =========================================================================
let currentFlashcards = [];
let fcCurrentIndex = 0;

function collectTrackFlashcards() {
  const cards = [];
  for (const tid in PR) {
    const note = (PR[tid] && PR[tid].n) ? PR[tid].n : "";
    if (!note) continue;

    const lines = note.split("\n");
    let pendingQ = "";

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].replace(/^[>\s*-]+/, "").trim();

      const qMatch = line.match(/^\*?\*?(?:P|Q|Pergunta|Question)\s*:\*?\*?\s*(.+)$/i);
      if (qMatch) {
        pendingQ = qMatch[1].trim();
        continue;
      }

      const aMatch = line.match(/^\*?\*?(?:R|A|Resposta|Answer)\s*:\*?\*?\s*(.+)$/i);
      if (aMatch && pendingQ) {
        const topicTitle = (TOPICS_MAP[tid] && TOPICS_MAP[tid].title) || tid;
        cards.push({
          id: `${tid}-${i}`,
          topicId: tid,
          topicTitle: topicTitle,
          q: pendingQ,
          a: aMatch[1].trim()
        });
        pendingQ = "";
      }
    }
  }
  return cards;
}

function openFlashcardsReviewModal() {
  currentFlashcards = collectTrackFlashcards();
  const modal = document.getElementById("modal-flashcards");
  if (!modal) return;

  if (currentFlashcards.length === 0) {
    alert("Nenhum flashcard encontrado nas suas anotações ainda!\n\nPara criar um flashcard, basta usar o botão '🗂️ Flashcard' na barra de ferramentas das anotações de qualquer tópico!");
    return;
  }

  fcCurrentIndex = 0;
  renderCurrentFlashcard();
  modal.hidden = false;
  modal.removeAttribute("hidden");
  modal.style.display = "flex";
}

function closeFlashcardsModal() {
  const modal = document.getElementById("modal-flashcards");
  if (modal) modal.style.display = "none";
}

function renderCurrentFlashcard() {
  const tagEl = document.getElementById("fc-card-tag");
  const contentEl = document.getElementById("fc-card-content");
  const ansTextEl = document.getElementById("fc-card-answer-text");
  const ansEl = document.getElementById("fc-card-answer-wrap");
  const revBtn = document.getElementById("fc-reveal-btn");
  const rateBtns = document.getElementById("fc-rating-btns");
  const counterEl = document.getElementById("fc-counter");

  if (fcCurrentIndex >= currentFlashcards.length) {
    if (tagEl) tagEl.textContent = "🎉 SESSÃO CONCLUÍDA";
    if (contentEl) contentEl.innerHTML = `Excelente! Você revisou todos os <b>${currentFlashcards.length} flashcards</b> desta trilha!`;
    if (ansEl) ansEl.className = "fc-card-answer-wrap";
    if (revBtn) revBtn.style.display = "none";
    if (rateBtns) rateBtns.className = "fc-rating-btns";
    if (counterEl) counterEl.textContent = `${currentFlashcards.length}/${currentFlashcards.length}`;
    return;
  }

  const card = currentFlashcards[fcCurrentIndex];

  if (tagEl) tagEl.textContent = `CARD ${fcCurrentIndex + 1} DE ${currentFlashcards.length} · ${card.topicTitle}`;
  if (contentEl) contentEl.textContent = card.q;
  if (ansTextEl) ansTextEl.textContent = card.a;
  if (ansEl) ansEl.className = "fc-card-answer-wrap";
  if (revBtn) {
    revBtn.style.display = "inline-flex";
    revBtn.textContent = "👁️ Revelar Resposta";
  }
  if (rateBtns) rateBtns.className = "fc-rating-btns";
  if (counterEl) counterEl.textContent = `${fcCurrentIndex + 1}/${currentFlashcards.length}`;
}

function flipFlashcard() {
  const ansEl = document.getElementById("fc-card-answer-wrap");
  const revBtn = document.getElementById("fc-reveal-btn");
  const rateBtns = document.getElementById("fc-rating-btns");

  if (ansEl) ansEl.className = "fc-card-answer-wrap show";
  if (revBtn) revBtn.style.display = "none";
  if (rateBtns) rateBtns.className = "fc-rating-btns show";
}

function rateFlashcard(level) {
  fcCurrentIndex++;
  renderCurrentFlashcard();
}

// =========================================================================
// 7. CALCULADORA DE MATRIZES E VETORES (ÁLGEBRA LINEAR)
// =========================================================================
let lastCalculatedLatex = "";
let lastCalculatedVectorLatex = "";

function openMatrixCalculator() {
  const modal = document.getElementById("modal-matrix-calc");
  if (modal) {
    modal.hidden = false;
    modal.removeAttribute("hidden");
    modal.style.display = "flex";
  }
}

function closeMatrixCalculator() {
  const modal = document.getElementById("modal-matrix-calc");
  if (modal) modal.style.display = "none";
}

function setCalcTab(tab) {
  document.querySelectorAll(".calc-tab-btn").forEach(b => b.classList.toggle("active", b.dataset.tab === tab));
  document.querySelectorAll(".calc-tab-pane").forEach(p => p.classList.toggle("active", p.id === `calc-pane-${tab}`));
}

function calculateMatrix(op) {
  const a00 = parseFloat(document.getElementById("m-a00")?.value || 0);
  const a01 = parseFloat(document.getElementById("m-a01")?.value || 0);
  const a10 = parseFloat(document.getElementById("m-a10")?.value || 0);
  const a11 = parseFloat(document.getElementById("m-a11")?.value || 0);

  const b00 = parseFloat(document.getElementById("m-b00")?.value || 0);
  const b01 = parseFloat(document.getElementById("m-b01")?.value || 0);
  const b10 = parseFloat(document.getElementById("m-b10")?.value || 0);
  const b11 = parseFloat(document.getElementById("m-b11")?.value || 0);

  let resLatex = "";

  if (op === "detA") {
    const det = (a00 * a11) - (a01 * a10);
    resLatex = `\\det(A) = (${a00} \\times ${a11}) - (${a01} \\times ${a10}) = ${det.toFixed(2)}`;
  } else if (op === "add") {
    const r00 = a00 + b00, r01 = a01 + b01, r10 = a10 + b10, r11 = a11 + b11;
    resLatex = `A + B = \\begin{bmatrix} ${r00} & ${r01} \\\\ ${r10} & ${r11} \\end{bmatrix}`;
  } else if (op === "mul") {
    const r00 = (a00 * b00) + (a01 * b10);
    const r01 = (a00 * b01) + (a01 * b11);
    const r10 = (a10 * b00) + (a11 * b10);
    const r11 = (a10 * b01) + (a11 * b11);
    resLatex = `A \\times B = \\begin{bmatrix} ${r00} & ${r01} \\\\ ${r10} & ${r11} \\end{bmatrix}`;
  } else if (op === "invA") {
    const det = (a00 * a11) - (a01 * a10);
    if (Math.abs(det) < 1e-9) {
      resLatex = `\\text{Matriz A não possui inversa } (\\det(A) = 0)`;
    } else {
      const invDet = 1 / det;
      const i00 = (a11 * invDet).toFixed(2);
      const i01 = (-a01 * invDet).toFixed(2);
      const i10 = (-a10 * invDet).toFixed(2);
      const i11 = (a00 * invDet).toFixed(2);
      resLatex = `A^{-1} = \\frac{1}{${det.toFixed(2)}} \\begin{bmatrix} ${a11} & ${-a01} \\\\ ${-a10} & ${a00} \\end{bmatrix} = \\begin{bmatrix} ${i00} & ${i01} \\\\ ${i10} & ${i11} \\end{bmatrix}`;
    }
  } else if (op === "transA") {
    resLatex = `A^T = \\begin{bmatrix} ${a00} & ${a10} \\\\ ${a01} & ${a11} \\end{bmatrix}`;
  }

  lastCalculatedLatex = resLatex;
  const resBox = document.getElementById("calc-matrix-result");
  if (resBox) {
    resBox.innerHTML = `$$${resLatex}$$`;
    if (window.renderMathInElement) {
      window.renderMathInElement(resBox, { delimiters: [{ left: "$$", right: "$$", display: true }] });
    }
  }
}

function calculateVectorOp(op) {
  const u1 = parseFloat(document.getElementById("v-u1")?.value || 0);
  const u2 = parseFloat(document.getElementById("v-u2")?.value || 0);
  const u3 = parseFloat(document.getElementById("v-u3")?.value || 0);

  const v1 = parseFloat(document.getElementById("v-v1")?.value || 0);
  const v2 = parseFloat(document.getElementById("v-v2")?.value || 0);
  const v3 = parseFloat(document.getElementById("v-v3")?.value || 0);

  let resLatex = "";

  if (op === "dot") {
    const dot = (u1 * v1) + (u2 * v2) + (u3 * v3);
    resLatex = `\\vec{u} \\cdot \\vec{v} = (${u1} \\times ${v1}) + (${u2} \\times ${v2}) + (${u3} \\times ${v3}) = ${dot.toFixed(2)}`;
  } else if (op === "cross") {
    const c1 = (u2 * v3) - (u3 * v2);
    const c2 = (u3 * v1) - (u1 * v3);
    const c3 = (u1 * v2) - (u2 * v1);
    resLatex = `\\vec{u} \\times \\vec{v} = \\begin{bmatrix} ${c1.toFixed(2)} \\\\ ${c2.toFixed(2)} \\\\ ${c3.toFixed(2)} \\end{bmatrix}`;
  } else if (op === "angle") {
    const dot = (u1 * v1) + (u2 * v2) + (u3 * v3);
    const normU = Math.sqrt(u1*u1 + u2*u2 + u3*u3);
    const normV = Math.sqrt(v1*v1 + v2*v2 + v3*v3);
    if (normU === 0 || normV === 0) {
      resLatex = `\\text{Vetor nulo não possui ângulo definido}`;
    } else {
      const cosTheta = Math.max(-1, Math.min(1, dot / (normU * normV)));
      const deg = (Math.acos(cosTheta) * 180 / Math.PI).toFixed(1);
      resLatex = `\\cos(\\theta) = \\frac{${dot.toFixed(2)}}{${normU.toFixed(2)} \\times ${normV.toFixed(2)}} \\implies \\theta = ${deg}^\\circ`;
    }
  }

  lastCalculatedVectorLatex = resLatex;
  const resBox = document.getElementById("calc-vector-result");
  if (resBox) {
    resBox.innerHTML = `$$${resLatex}$$`;
    if (window.renderMathInElement) {
      window.renderMathInElement(resBox, { delimiters: [{ left: "$$", right: "$$", display: true }] });
    }
  }
}

function insertMatrixResultToNotes() {
  if (!lastCalculatedLatex) {
    showToast("Faça uma operação com matrizes primeiro!");
    return;
  }
  const editor = document.getElementById("modal-note-editor");
  if (!editor) return;
  editor.focus();
  const md = `\n$$${lastCalculatedLatex}$$\n`;
  const start = editor.selectionStart;
  editor.value = editor.value.substring(0, start) + md + editor.value.substring(start);
  editor.selectionStart = editor.selectionEnd = start + md.length;
  pushNoteHistory(editor.value, true);
  onNoteEditorInput();
  closeMatrixCalculator();
  showToast("📥 Solução LaTeX inserida na anotação!");
}

function insertVectorResultToNotes() {
  if (!lastCalculatedVectorLatex) {
    showToast("Faça uma operação com vetores primeiro!");
    return;
  }
  const editor = document.getElementById("modal-note-editor");
  if (!editor) return;
  editor.focus();
  const md = `\n$$${lastCalculatedVectorLatex}$$\n`;
  const start = editor.selectionStart;
  editor.value = editor.value.substring(0, start) + md + editor.value.substring(start);
  editor.selectionStart = editor.selectionEnd = start + md.length;
  pushNoteHistory(editor.value, true);
  onNoteEditorInput();
  closeMatrixCalculator();
  showToast("📥 Solução vetorial inserida na anotação!");
}

// =========================================================================
// 8. EXPORTAÇÃO DO CADERNO (MARKDOWN, PDF IMPRIMÍVEL E BACKUP JSON)
// =========================================================================
function openExportModal() {
  const modal = document.getElementById("modal-export-notebook");
  if (modal) {
    modal.hidden = false;
    modal.removeAttribute("hidden");
    modal.style.display = "flex";
  }
}

function closeExportModal() {
  const modal = document.getElementById("modal-export-notebook");
  if (modal) modal.style.display = "none";
}

function exportNotebookMarkdown() {
  let md = `# 📚 Caderno Completo de Estudos - ${document.title}\n`;
  md += `> Gerado em: ${new Date().toLocaleDateString("pt-BR")} | Ecossistema Roteiro de IA\n\n---\n\n`;

  let count = 0;
  for (const tid in PR) {
    const item = PR[tid];
    if (item && item.n && item.n.trim()) {
      count++;
      const info = (typeof TOPICS_MAP !== "undefined" && TOPICS_MAP[tid]) || {};
      const statusLabel = item.s === "e" ? "🟢 Concluído" : item.s === "r" ? "🟡 Falta terminar" : "🔴 Do zero";
      md += `## 📌 ${info.title || tid}\n`;
      md += `**Status:** ${statusLabel} | **ID:** \`${tid}\`\n\n`;
      if (info.url) md += `* **Vídeo Aula:** ${info.url}\n`;
      if (info.doc_url) md += `* **Material / Docs:** ${info.doc_url}\n`;
      md += `\n### 📝 Anotações & Exercícios:\n\n${item.n.trim()}\n\n---\n\n`;
    }
  }

  if (count === 0) {
    alert("Você ainda não tem anotações registradas para exportar!");
    return;
  }

  const blob = new Blob([md], { type: "text/markdown;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `caderno-estudos-${TRACK_ID || 'roteiro'}.md`;
  a.click();
  showToast(`📥 Caderno com ${count} tópicos exportado em Markdown!`);
  closeExportModal();
}

function exportNotebookPrint() {
  let html = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>Caderno de Estudos - ${document.title}</title>`;
  html += `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">`;
  html += `<style>body{font-family:system-ui,-apple-system,sans-serif;line-height:1.6;padding:40px;max-width:850px;margin:auto;color:#111}h1{border-bottom:2px solid #333;padding-bottom:10px}h2{color:#4f46e5;margin-top:30px}pre{background:#f3f4f6;padding:12px;border-radius:6px;overflow-x:auto}table{border-collapse:collapse;width:100%}th,td{border:1px solid #ddd;padding:8px}@media print{body{padding:0}}</style></head><body>`;
  html += `<h1>📚 Caderno de Estudos - ${document.title}</h1>`;

  let count = 0;
  for (const tid in PR) {
    const item = PR[tid];
    if (item && item.n && item.n.trim()) {
      count++;
      const info = (typeof TOPICS_MAP !== "undefined" && TOPICS_MAP[tid]) || {};
      html += `<h2>${count}. ${info.title || tid}</h2>`;
      html += `<div>${parseMarkdown(item.n)}</div><hr>`;
    }
  }

  if (count === 0) {
    alert("Você ainda não tem anotações registradas para exportar!");
    return;
  }

  html += "<scr" + "ipt src=\"https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js\"></scr" + "ipt>";
  html += "<scr" + "ipt src=\"https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js\"></scr" + "ipt>";
  html += "<scr" + "ipt>renderMathInElement(document.body); setTimeout(()=>window.print(), 600);</scr" + "ipt></body></html>";

  const w = window.open("", "_blank");
  if (w) {
    w.document.write(html);
    w.document.close();
  }
  closeExportModal();
}

function exportBackupJson() {
  const data = {
    exportDate: new Date().toISOString(),
    track: TRACK_ID,
    progress: PR
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `backup-${TRACK_ID}-roteiro.json`;
  a.click();
  showToast("💾 Backup JSON baixado com sucesso!");
  closeExportModal();
}

"""
