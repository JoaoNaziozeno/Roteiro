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
const GUIDE_READ_TARGET_SECONDS = 45; // 45s de leitura ativa na Aula Visual + rolagem pelos 4 cards
let autoProgressEnabled = true;

// Estado em tempo real do Vídeo (YouTube IFrame API) e da Aula Visual PT-BR
let ytCurrentTime = 0;
let ytMaxTime = 0;
let ytDuration = 0;
let ytPlayerState = -1; // 1 = playing, 2 = paused, 0 = ended
let ytVideoCompleted = false;
let guideReadSeconds = 0;
let guideCardsSeen = { 1: false, 2: false, 3: false, 4: false };
let guideCompleted = false;
let notifiedVideoHalf = false;
let notifiedGuideHalf = false;

try {
  const savedAuto = localStorage.getItem("roteiro-auto-progress");
  if (savedAuto !== null) autoProgressEnabled = savedAuto === "true";
} catch(e) {}

function getYoutubeEmbedUrl(url) {
  if (!url) return "";
  const originParam = (typeof window !== "undefined" && window.location && window.location.origin && window.location.origin.startsWith("http"))
    ? "&origin=" + encodeURIComponent(window.location.origin)
    : "";
  if (url.includes("youtube.com/embed/")) return url;
  const matchV = url.match(/[?&]v=([^&#]+)/);
  if (matchV) return "https://www.youtube.com/embed/" + matchV[1] + "?enablejsapi=1&rel=0&cc_load_policy=1&cc_lang_pref=pt&hl=pt" + originParam;
  const matchShort = url.match(/youtu\.be\/([^?&#]+)/);
  if (matchShort) return "https://www.youtube.com/embed/" + matchShort[1] + "?enablejsapi=1&rel=0&cc_load_policy=1&cc_lang_pref=pt&hl=pt" + originParam;
  const matchL = url.match(/[?&]list=([^&#]+)/);
  if (matchL) return "https://www.youtube.com/embed/videoseries?list=" + matchL[1] + "&enablejsapi=1&rel=0&cc_load_policy=1&cc_lang_pref=pt&hl=pt" + originParam;
  return url;
}

function sendYoutubeListeningHandshake() {
  const iframe = document.getElementById("modal-video-iframe");
  if (!iframe || !iframe.contentWindow || !iframe.src) return;
  try {
    iframe.contentWindow.postMessage(JSON.stringify({ event: "listening", id: 1, channel: "widget" }), "*");
    iframe.contentWindow.postMessage(JSON.stringify({ event: "command", func: "addEventListener", args: ["onStateChange"] }), "*");
  } catch(e) {}
}

if (typeof window !== "undefined" && !window._roteiroYtListenerBound) {
  window._roteiroYtListenerBound = true;
  window.addEventListener("message", (event) => {
    if (!event.origin || (!event.origin.includes("youtube.com") && !event.origin.includes("youtu.be"))) return;
    let data = event.data;
    if (typeof data === "string") {
      try { data = JSON.parse(data); } catch(e) { return; }
    }
    if (!data || typeof data !== "object") return;

    if (data.event === "infoDelivery" && data.info) {
      if (typeof data.info.duration === "number" && data.info.duration > 0) {
        ytDuration = data.info.duration;
      }
      if (typeof data.info.currentTime === "number" && data.info.currentTime >= 0) {
        ytCurrentTime = data.info.currentTime;
        if (ytCurrentTime > ytMaxTime) ytMaxTime = ytCurrentTime;
      }
      if (typeof data.info.playerState === "number") {
        ytPlayerState = data.info.playerState;
        if (ytPlayerState === 0) {
          ytVideoCompleted = true;
        }
      }
      if (ytDuration > 0 && Math.max(ytCurrentTime, ytMaxTime) >= ytDuration * 0.90) {
        ytVideoCompleted = true;
      }
      syncSessionStudyProgressUI();
    } else if (data.event === "onStateChange") {
      if (typeof data.info === "number") {
        ytPlayerState = data.info;
        if (ytPlayerState === 0) {
          ytVideoCompleted = true;
          syncSessionStudyProgressUI();
        }
      }
    }
  });
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
  markPtGuideReadNow(true);
  showToast("📘 Apostila em Português copiada para o Caderno e Aula Visual validada (100%)!");
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
let CURRENT_MODAL_VIDEO_OPT = 1;

function switchModalVideoOption(optNum, resetPlayerTimer = false) {
  const topicId = CURRENT_MODAL_TOPIC_ID;
  if (!topicId) return;
  const topicInfo = (typeof TOPICS_MAP !== "undefined" && TOPICS_MAP[topicId]) || {};
  const video1Url = topicInfo.url || "";
  const video1Label = topicInfo.label || "▶ Aula 1: Khan Academy (PT-BR)";
  const video2Url = topicInfo.url2 || "";
  const video2Label = topicInfo.label2 || "🎬 Opção 2: 3B1B / StatQuest";

  CURRENT_MODAL_VIDEO_OPT = (optNum === 2 && video2Url) ? 2 : 1;
  const activeUrl = CURRENT_MODAL_VIDEO_OPT === 2 ? video2Url : video1Url;
  const activeLabel = CURRENT_MODAL_VIDEO_OPT === 2 ? video2Label : video1Label;

  const iframe = document.getElementById("modal-video-iframe");
  const extLink = document.getElementById("modal-external-link");
  const playerTag = document.getElementById("modal-player-tag");
  const switcherWrap = document.getElementById("modal-video-switcher-wrap");
  const btnOpt1 = document.getElementById("modal-video-opt1-btn");
  const btnOpt2 = document.getElementById("modal-video-opt2-btn");

  if (switcherWrap) {
    if (video1Url && video2Url) {
      switcherWrap.style.display = "inline-flex";
      if (btnOpt1) {
        btnOpt1.textContent = video1Label;
        btnOpt1.style.background = CURRENT_MODAL_VIDEO_OPT === 1 ? "var(--ac)" : "var(--card)";
        btnOpt1.style.color = CURRENT_MODAL_VIDEO_OPT === 1 ? "#fff" : "var(--tx)";
        btnOpt1.style.borderColor = CURRENT_MODAL_VIDEO_OPT === 1 ? "var(--ac)" : "var(--bd)";
      }
      if (btnOpt2) {
        btnOpt2.textContent = video2Label;
        btnOpt2.style.background = CURRENT_MODAL_VIDEO_OPT === 2 ? "#f59e0b" : "var(--card)";
        btnOpt2.style.color = CURRENT_MODAL_VIDEO_OPT === 2 ? "#fff" : "var(--tx)";
        btnOpt2.style.borderColor = CURRENT_MODAL_VIDEO_OPT === 2 ? "#f59e0b" : "var(--bd)";
      }
    } else {
      switcherWrap.style.display = "none";
    }
  }

  if (activeUrl) {
    if (iframe) {
      ytCurrentTime = 0;
      ytDuration = 0;
      iframe.onload = () => {
        sendYoutubeListeningHandshake();
        setTimeout(sendYoutubeListeningHandshake, 700);
        setTimeout(sendYoutubeListeningHandshake, 1800);
      };
      iframe.src = getYoutubeEmbedUrl(activeUrl);
    }
    if (extLink) {
      extLink.href = activeUrl;
      extLink.style.display = "inline-flex";
    }
    if (playerTag) playerTag.textContent = activeLabel;
  }

  const vWrap = document.getElementById("video-wrapper");
  const cBtn = document.getElementById("modal-collapse-btn");
  if (vWrap && vWrap.classList.contains("collapsed")) {
    vWrap.classList.remove("collapsed");
    if (cBtn) cBtn.textContent = "▲ Ocultar Vídeo";
  }

  if (!resetPlayerTimer) {
    const p = document.getElementById("study-player-sect");
    if (p) p.scrollTo({ top: 0, behavior: "smooth" });
    showToast(`🎬 Reproduzindo: ${activeLabel}`);
  }
}

function openStudyModal(topicId, focusGuide = false, videoOpt = 1) {
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
  const video2Url = topicInfo.url2 || "";
  const docUrl = topicInfo.doc_url || "";
  const videoLabel = topicInfo.label || "▶ Vídeo Aula";
  const video2Label = topicInfo.label2 || "🎬 2ª Opção";
  const docLabel = topicInfo.doc_label || "📖 Material Oficial";
  const ytPtUrl = topicInfo.yt_pt_url || "";
  const ptGuide = topicInfo.pt_guide || null;

  if (videoUrl || video2Url) {
    if (playerSect) playerSect.style.display = "flex";
    if (playerTitle) playerTitle.textContent = title;
    switchModalVideoOption(videoOpt, true);
  } else {
    if (iframe) iframe.src = "";
    if (extLink) extLink.style.display = "none";
    if (playerTitle) playerTitle.textContent = "Material Teórico e Prático";
  }

  if (docUrl && docLink) {
    docLink.href = docUrl;
    docLink.textContent = ptGuide ? "🌐 Khan Academy / Fonte PT-BR ↗" : docLabel;
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
        <div class="study-left-card" id="pt-guide-box" style="border:1px solid rgba(155,168,171,.3);background:linear-gradient(160deg,rgba(37,55,69,.5),rgba(74,92,106,.2));padding:16px 18px;border-radius:14px;margin-bottom:10px">
          <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px;margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid var(--bd)">
            <div style="font-size:.95rem;font-weight:850;color:var(--tx);display:flex;align-items:center;gap:7px">
              <span>📘 Aula Visual Passo a Passo — Método Khan Academy (PT-BR)</span>
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:6px">
              <button type="button" onclick="switchModalVideoOption(1)" style="font:inherit;font-size:.74rem;font-weight:800;padding:5px 11px;border-radius:8px;border:1px solid rgba(204,0,0,.45);background:rgba(204,0,0,.14);color:#ef4444;cursor:pointer">
                ${videoLabel} ↑
              </button>
              ${video2Url ? `<button type="button" onclick="switchModalVideoOption(2)" style="font:inherit;font-size:.74rem;font-weight:800;padding:5px 11px;border-radius:8px;border:1px solid rgba(245,158,11,.45);background:rgba(245,158,11,.14);color:#f59e0b;cursor:pointer">${video2Label} ↑</button>` : ""}
              <button type="button" onclick="copyPtGuideToNotebook('${topicId}')" style="font:inherit;font-size:.74rem;font-weight:800;padding:5px 11px;border-radius:8px;border:1px solid var(--ac);background:var(--ac);color:#fff;cursor:pointer">
                📥 Copiar para Meu Caderno
              </button>
              ${ytPtUrl ? `<a href="${ytPtUrl}" target="_blank" rel="noopener" style="font-size:.74rem;font-weight:800;padding:5px 11px;border-radius:8px;border:1px solid rgba(16,185,129,.4);background:rgba(16,185,129,.12);color:#10b981;text-decoration:none;display:inline-flex;align-items:center;gap:4px">🎓 Canal @khanacademyportugues ↗</a>` : ""}
            </div>
          </div>

          <div style="display:flex;flex-direction:column;gap:12px;font-size:.86rem;line-height:1.6;color:var(--tx)">
            <div id="pt-step-card-1" style="background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:11px 14px;transition:border-color .2s">
              <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:4px">
                <div style="font-size:.76rem;font-weight:800;text-transform:uppercase;color:var(--ac)">🎯 1. O que é & Intuição Geométrica (Em Português)</div>
                <span id="pt-step-badge-1" style="font-size:.68rem;font-weight:750;padding:1px 7px;border-radius:99px;background:var(--bg);color:var(--mu);border:1px solid var(--bd)">1/4</span>
              </div>
              <div>${ptGuide.intuicao || ""}</div>
            </div>

            <div id="pt-step-card-2" style="background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:11px 14px;transition:border-color .2s">
              <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:4px">
                <div style="font-size:.76rem;font-weight:800;text-transform:uppercase;color:#f59e0b">📐 2. Fórmula Matemática & Significado</div>
                <span id="pt-step-badge-2" style="font-size:.68rem;font-weight:750;padding:1px 7px;border-radius:99px;background:var(--bg);color:var(--mu);border:1px solid var(--bd)">2/4</span>
              </div>
              <div id="pt-guide-formula-render">${fmtFormula}</div>
            </div>

            <div id="pt-step-card-3" style="background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:11px 14px;transition:border-color .2s">
              <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:4px">
                <div style="font-size:.76rem;font-weight:800;text-transform:uppercase;color:#10b981">🔢 3. Exemplo Prático Passo a Passo</div>
                <span id="pt-step-badge-3" style="font-size:.68rem;font-weight:750;padding:1px 7px;border-radius:99px;background:var(--bg);color:var(--mu);border:1px solid var(--bd)">3/4</span>
              </div>
              <div id="pt-guide-example-render">${fmtExemplo}</div>
            </div>

            <div id="pt-step-card-4" style="background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:11px 14px;transition:border-color .2s">
              <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:4px">
                <div style="font-size:.76rem;font-weight:800;text-transform:uppercase;color:#06b6d4">🐍 4. Como a IA calcula isso em Python / NumPy</div>
                <span id="pt-step-badge-4" style="font-size:.68rem;font-weight:750;padding:1px 7px;border-radius:99px;background:var(--bg);color:var(--mu);border:1px solid var(--bd)">4/4</span>
              </div>
              <pre style="margin:6px 0 0;padding:10px 12px;background:#0d1017;color:#e5e7eb;border-radius:8px;overflow-x:auto;font-family:monospace;font-size:.8rem;line-height:1.45"><code>${(ptGuide.codigo || "").replace(/</g, "&lt;").replace(/>/g, "&gt;")}</code></pre>
            </div>
          </div>

          <div id="pt-guide-validation-bar" style="margin-top:14px;padding:12px 14px;border-radius:10px;border:1px dashed rgba(16,185,129,.45);background:rgba(16,185,129,.07);display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px">
            <div style="display:flex;flex-direction:column;gap:2px">
              <span id="pt-guide-val-title" style="font-size:.82rem;font-weight:800;color:#10b981">📖 Validação de Leitura da Aula Visual (Vale 50% da Conclusão)</span>
              <span id="pt-guide-val-sub" style="font-size:.75rem;color:var(--mu)">Role pelos 4 cards + ~45s de leitura na tela, ou clique ao lado para confirmar leitura imediata.</span>
            </div>
            <button type="button" id="pt-guide-complete-btn" onclick="markPtGuideReadNow()" style="font:inherit;font-size:.78rem;font-weight:800;padding:7px 14px;border-radius:8px;border:1px solid #10b981;background:#10b981;color:#fff;cursor:pointer;transition:.15s;white-space:nowrap">
              ☑️ Marcar Aula Visual como Lida
            </button>
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

  // Vincular evento de rolagem da coluna esquerda para rastrear leitura dos 4 cards
  if (playerSect) {
    playerSect.onscroll = () => {
      checkPtGuideScrollAndVisibility(false);
      syncSessionStudyProgressUI();
    };
  }

  // Iniciar Cronômetro da Sessão e Validador Duplo
  initStudySessionTimer(topicId);

  // Caderno de Anotações (abaixo do vídeo)
  const editor = document.getElementById("modal-note-editor");
  if (editor) {
    editor.value = v.n || "";
    initNoteHistory(editor.value);
    renderModalPreview(editor.value);
    updateNoteStats(editor.value);
  }

  setNoteViewMode(window.innerWidth < 768 ? "editor" : NOTE_VIEW_MODE);
  modal.hidden = false;
  modal.removeAttribute("hidden");
  modal.classList.add("active");
  modal.style.display = "flex";
  document.body.style.overflow = "hidden";

  const vWrap = document.getElementById("video-wrapper");
  const cBtn = document.getElementById("modal-collapse-btn");
  if (vWrap && vWrap.classList.contains("collapsed")) {
    vWrap.classList.remove("collapsed");
    if (cBtn) cBtn.textContent = "▲ Ocultar Vídeo";
  }

  if (focusGuide) {
    setTimeout(() => {
      const gBox = document.getElementById("pt-guide-box");
      if (gBox) {
        gBox.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }, 120);
  } else {
    if (playerSect) playerSect.scrollTop = 0;
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

  // Registrar tempo da sessão de estudo
  try {
    if (CURRENT_MODAL_TOPIC_ID && sessionSeconds >= 20) {
      const l = JSON.parse(localStorage.getItem("roteiro-sessions-v1") || "[]");
      l.push({ t: Date.now(), id: CURRENT_MODAL_TOPIC_ID, sec: sessionSeconds });
      localStorage.setItem("roteiro-sessions-v1", JSON.stringify(l.slice(-2000)));
    }
  } catch(e) {}

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

// =========================================================================
// MOTOR DE VALIDAÇÃO REAL DE ESTUDO (50% VÍDEO YOUTUBE + 50% AULA VISUAL PT-BR)
// =========================================================================
function resetSessionStudyProgress() {
  ytCurrentTime = 0;
  ytMaxTime = 0;
  ytVideoCompleted = false;
  guideReadSeconds = 0;
  guideCardsSeen = { 1: false, 2: false, 3: false, 4: false };
  guideCompleted = false;
  notifiedVideoHalf = false;
  notifiedGuideHalf = false;
  for (let i = 1; i <= 4; i++) {
    const b = document.getElementById(`pt-step-badge-${i}`);
    const c = document.getElementById(`pt-step-card-${i}`);
    if (b) {
      b.textContent = `${i}/4`;
      b.style.background = "var(--bg)";
      b.style.color = "var(--mu)";
      b.style.borderColor = "var(--bd)";
    }
    if (c) c.style.borderColor = "var(--bd)";
  }
  syncSessionStudyProgressUI();
}

function checkPtGuideScrollAndVisibility(incrementReadSeconds = false) {
  const topicId = CURRENT_MODAL_TOPIC_ID;
  if (!topicId) return;
  const topicInfo = (typeof TOPICS_MAP !== "undefined" && TOPICS_MAP[topicId]) || {};
  if (!topicInfo.pt_guide) return;

  const container = document.getElementById("study-player-sect");
  const gBox = document.getElementById("pt-guide-box");
  if (!container || !gBox) return;

  const cRect = container.getBoundingClientRect();
  const gRect = gBox.getBoundingClientRect();

  // Verifica se a Aula Visual está visível na tela da coluna esquerda
  const isGuideVisible = (gRect.top < cRect.bottom - 35) && (gRect.bottom > cRect.top + 35);
  if (incrementReadSeconds && isGuideVisible && document.visibilityState !== "hidden") {
    guideReadSeconds++;
  }

  // Verifica quais dos 4 cards já entraram no campo de visão
  for (let i = 1; i <= 4; i++) {
    const card = document.getElementById(`pt-step-card-${i}`);
    if (!card) continue;
    const r = card.getBoundingClientRect();
    if (r.top < cRect.bottom - 25 && r.bottom > cRect.top + 15) {
      if (!guideCardsSeen[i]) {
        guideCardsSeen[i] = true;
        const badge = document.getElementById(`pt-step-badge-${i}`);
        if (badge) {
          badge.textContent = `✓ ${i}/4 Lido`;
          badge.style.background = "rgba(16,185,129,.15)";
          badge.style.color = "#10b981";
          badge.style.borderColor = "rgba(16,185,129,.4)";
        }
        card.style.borderColor = "rgba(16,185,129,.45)";
      }
    }
  }
}

function getComputedVideoAndGuideProgress(topicId) {
  const topicInfo = (typeof TOPICS_MAP !== "undefined" && TOPICS_MAP[topicId]) || {};
  const hasVideo = Boolean(topicInfo.url);
  const hasGuide = Boolean(topicInfo.pt_guide);
  const saved = PR[topicId] || { s: "z", n: "", d: "" };

  // 1. Cálculo do Progresso do Vídeo (0 a 100%)
  let videoPct = saved.vp || 0;
  if (saved.s === "e") videoPct = 100;
  if (ytVideoCompleted) {
    videoPct = 100;
  } else if (ytDuration > 0) {
    const effectiveTarget = ytDuration * 0.90; // 90% da duração real do vídeo (desconta créditos finais)
    const curPct = Math.min(100, Math.round((Math.max(ytCurrentTime, ytMaxTime) / effectiveTarget) * 100));
    if (curPct > videoPct) videoPct = curPct;
    if (videoPct >= 100) ytVideoCompleted = true;
  }

  // 2. Cálculo do Progresso da Aula Visual PT-BR (0 a 100%)
  let guidePct = saved.gp || 0;
  if (saved.s === "e") guidePct = 100;
  let seenCount = 0;
  for (let i = 1; i <= 4; i++) {
    if (guideCardsSeen[i]) seenCount++;
  }
  if (guideCompleted) {
    guidePct = 100;
  } else if (hasGuide) {
    // 50% pela visualização dos 4 cards na rolagem + 50% pelos 45s de leitura ativa na tela
    const cardsScore = (seenCount / 4) * 50;
    const timeScore = Math.min(50, (guideReadSeconds / GUIDE_READ_TARGET_SECONDS) * 50);
    const calcGuide = Math.min(100, Math.round(cardsScore + timeScore));
    if (calcGuide > guidePct) guidePct = calcGuide;
    if (seenCount === 4 && guideReadSeconds >= GUIDE_READ_TARGET_SECONDS) {
      guidePct = 100;
      guideCompleted = true;
    }
  }

  // Salvar subprogresso no objeto PR
  if (!PR[topicId]) PR[topicId] = { s: "z", n: "", d: "" };
  if (videoPct > (PR[topicId].vp || 0)) PR[topicId].vp = videoPct;
  if (guidePct > (PR[topicId].gp || 0)) PR[topicId].gp = guidePct;

  // 3. Regra A — Estudo Completo (50% Vídeo + 50% Aula Visual quando ambos existem)
  let totalPct = 0;
  if (hasVideo && hasGuide) {
    totalPct = Math.round((videoPct * 0.5) + (guidePct * 0.5));
  } else if (hasVideo) {
    totalPct = videoPct;
  } else if (hasGuide) {
    totalPct = guidePct;
  }

  return { hasVideo, hasGuide, videoPct, guidePct, seenCount, totalPct };
}

function syncSessionStudyProgressUI() {
  const topicId = CURRENT_MODAL_TOPIC_ID;
  if (!topicId) return;

  const { hasVideo, hasGuide, videoPct, guidePct, seenCount, totalPct } = getComputedVideoAndGuideProgress(topicId);

  const timerTxt = document.getElementById("session-progress-text");
  const videoPill = document.getElementById("session-video-pill");
  const guidePill = document.getElementById("session-guide-pill");
  const barFill = document.getElementById("session-bar-fill");
  const pctTxt = document.getElementById("session-progress-pct");

  const mins = String(Math.floor(sessionSeconds / 60)).padStart(2, "0");
  const secs = String(sessionSeconds % 60).padStart(2, "0");
  if (timerTxt) {
    timerTxt.textContent = `⏱️ Sessão: ${mins}:${secs}`;
  }

  if (videoPill) {
    videoPill.style.display = hasVideo ? "inline-flex" : "none";
    if (videoPct >= 100) {
      videoPill.textContent = hasGuide ? `🎬 Vídeo: 100% ✓ (50/50%)` : `🎬 Vídeo: 100% ✓`;
      videoPill.style.background = "rgba(16,185,129,.15)";
      videoPill.style.borderColor = "rgba(16,185,129,.45)";
      videoPill.style.color = "#10b981";
    } else if (ytDuration > 0) {
      videoPill.textContent = `🎬 Vídeo: ${videoPct}% (${formatSeconds(ytCurrentTime)}/${formatSeconds(ytDuration)})`;
      videoPill.style.background = "rgba(74,92,106,.2)";
      videoPill.style.borderColor = "rgba(155,168,171,.35)";
      videoPill.style.color = "var(--ac)";
    } else {
      videoPill.textContent = `🎬 Vídeo: ${videoPct}% (Assista ao vídeo)`;
      videoPill.style.background = "rgba(74,92,106,.2)";
      videoPill.style.borderColor = "rgba(155,168,171,.35)";
      videoPill.style.color = "var(--ac)";
    }
  }

  if (guidePill) {
    guidePill.style.display = hasGuide ? "inline-flex" : "none";
    if (guidePct >= 100) {
      guidePill.textContent = `📘 Aula Visual: 100% ✓ (50/50%)`;
      guidePill.style.background = "rgba(16,185,129,.18)";
      guidePill.style.borderColor = "rgba(16,185,129,.5)";
      guidePill.style.color = "#10b981";
    } else {
      const readSecCap = Math.min(GUIDE_READ_TARGET_SECONDS, guideReadSeconds);
      guidePill.textContent = `📘 Aula Visual: ${guidePct}% (${seenCount}/4 cards · ${readSecCap}s/${GUIDE_READ_TARGET_SECONDS}s)`;
      guidePill.style.background = "rgba(16,185,129,.08)";
      guidePill.style.borderColor = "rgba(16,185,129,.32)";
      guidePill.style.color = "#10b981";
    }
  }

  // Atualizar barra de validação no rodapé da Aula Visual PT-BR
  const valBtn = document.getElementById("pt-guide-complete-btn");
  const valTitle = document.getElementById("pt-guide-val-title");
  const valSub = document.getElementById("pt-guide-val-sub");
  if (valBtn && hasGuide) {
    if (guidePct >= 100) {
      valBtn.textContent = "✅ Aula Visual Lida (100%)";
      valBtn.style.background = "rgba(16,185,129,.2)";
      valBtn.style.color = "#10b981";
      if (valTitle) valTitle.textContent = "✅ Leitura da Aula Visual Concluída! (+50% garantidos)";
      if (valSub) valSub.textContent = videoPct >= 100
        ? "🎉 Você completou tanto a Aula Visual quanto o Vídeo (100% do Tópico)!"
        : "Agora conclua o vídeo acima para atingir 100% do estudo completo.";
    } else {
      const readSecCap = Math.min(GUIDE_READ_TARGET_SECONDS, guideReadSeconds);
      valBtn.textContent = `☑️ Marcar Aula Visual como Lida (${guidePct}%)`;
      valBtn.style.background = "#10b981";
      valBtn.style.color = "#fff";
      if (valTitle) valTitle.textContent = `📖 Leitura da Aula Visual: ${guidePct}% (${seenCount}/4 cards vistos · ${readSecCap}s/${GUIDE_READ_TARGET_SECONDS}s)`;
    }
  }

  if (barFill) barFill.style.width = `${totalPct}%`;
  if (pctTxt) pctTxt.textContent = `${totalPct}%`;

  // Regras de Auto-Progresso (Regra A: 50% Vídeo + 50% Aula Visual)
  if (autoProgressEnabled) {
    const curStatus = (PR[topicId] && PR[topicId].s) ? PR[topicId].s : "z";

    // Mudar de "Do zero" para "Falta terminar" ao iniciar estudo real
    if (curStatus === "z" && (totalPct >= 5 || ytPlayerState === 1 || guideReadSeconds >= 8)) {
      PR[topicId].s = "r";
      updateModalStatusBtn("r");
      saveLocal();
      paint();
      syncTopicToServer(topicId);
      showToast("🟡 Estudo iniciado! Status atualizado para: Falta terminar");
    }

    // Avisos intermediários quando completa uma das metades (50%)
    if (hasVideo && hasGuide) {
      if (videoPct >= 100 && guidePct < 100 && !notifiedVideoHalf) {
        notifiedVideoHalf = true;
        saveLocal();
        showToast("🎬 Vídeo concluído (50%)! Agora leia a 📘 Aula Visual PT-BR abaixo para completar 100%!");
      }
      if (guidePct >= 100 && videoPct < 100 && !notifiedGuideHalf) {
        notifiedGuideHalf = true;
        saveLocal();
        showToast("📘 Aula Visual concluída (50%)! Assista ao 🎬 Vídeo para completar os 100% do tópico!");
      }
    }

    // Só conclui o tópico automaticamente quando totalPct chega a 100%
    if (totalPct >= 100 && curStatus !== "e") {
      window.__evSrc = "auto";
      PR[topicId].s = "e";
      updateModalStatusBtn("e");
      saveLocal();
      paint();
      syncTopicToServer(topicId);
      showToast(hasGuide
        ? "🟢 Estudo Completo (Vídeo 50% + Aula Visual 50% = 100%)! Tópico Concluído!"
        : "🟢 Vídeo finalizado (100%)! Tópico concluído automaticamente!");
    }
  }
}

function markPtGuideReadNow(silent = false) {
  const topicId = CURRENT_MODAL_TOPIC_ID;
  if (!topicId) return;
  guideCompleted = true;
  guideReadSeconds = GUIDE_READ_TARGET_SECONDS;
  for (let i = 1; i <= 4; i++) {
    guideCardsSeen[i] = true;
    const badge = document.getElementById(`pt-step-badge-${i}`);
    if (badge) {
      badge.textContent = `✓ ${i}/4 Lido`;
      badge.style.background = "rgba(16,185,129,.15)";
      badge.style.color = "#10b981";
      badge.style.borderColor = "rgba(16,185,129,.4)";
    }
  }
  if (!PR[topicId]) PR[topicId] = { s: "z", n: "", d: "" };
  PR[topicId].gp = 100;
  saveLocal();
  syncSessionStudyProgressUI();
  if (!silent) {
    showToast("📘 Aula Visual PT-BR marcada como 100% Lida!");
  }
}

function scrollOrValidatePtGuide() {
  const gBox = document.getElementById("pt-guide-box");
  if (gBox) {
    gBox.scrollIntoView({ behavior: "smooth", block: "start" });
    showToast("📘 Role pelos 4 cards da Aula Visual ou clique no botão verde ao final para validar!");
  }
}

function toggleManualVideoValidated() {
  const topicId = CURRENT_MODAL_TOPIC_ID;
  if (!topicId) return;
  if (!PR[topicId]) PR[topicId] = { s: "z", n: "", d: "" };
  if (ytVideoCompleted || (PR[topicId].vp || 0) >= 100) {
    ytVideoCompleted = false;
    PR[topicId].vp = 0;
    showToast("🔄 Progresso do vídeo resetado para acompanhar o player.");
  } else {
    ytVideoCompleted = true;
    PR[topicId].vp = 100;
    showToast("🎬 Vídeo validado como 100% assistido!");
  }
  saveLocal();
  syncSessionStudyProgressUI();
}

function initStudySessionTimer(topicId) {
  clearInterval(studySessionTimer);
  sessionSeconds = 0;
  ytCurrentTime = 0;
  ytMaxTime = 0;
  ytDuration = 0;
  ytPlayerState = -1;

  const saved = PR[topicId] || { s: "z", n: "", d: "" };
  ytVideoCompleted = (saved.s === "e" || (saved.vp || 0) >= 100);
  guideCompleted = (saved.s === "e" || (saved.gp || 0) >= 100);
  guideReadSeconds = guideCompleted ? GUIDE_READ_TARGET_SECONDS : 0;
  guideCardsSeen = {
    1: guideCompleted,
    2: guideCompleted,
    3: guideCompleted,
    4: guideCompleted
  };
  notifiedVideoHalf = ytVideoCompleted;
  notifiedGuideHalf = guideCompleted;

  checkPtGuideScrollAndVisibility(false);
  syncSessionStudyProgressUI();

  studySessionTimer = setInterval(() => {
    if (document.visibilityState === "visible") sessionSeconds++;
    if (ytDuration === 0) {
      sendYoutubeListeningHandshake();
    }
    checkPtGuideScrollAndVisibility(true);
    syncSessionStudyProgressUI();
  }, 1000);
}

// Botão rápido de concluir tópico agora (100% manual)
function markTopicCompleteNow() {
  if (!CURRENT_MODAL_TOPIC_ID) return;
  window.__evSrc = "manual";
  if (!PR[CURRENT_MODAL_TOPIC_ID]) PR[CURRENT_MODAL_TOPIC_ID] = { s: "z", n: "", d: "" };
  PR[CURRENT_MODAL_TOPIC_ID].s = "e";
  PR[CURRENT_MODAL_TOPIC_ID].vp = 100;
  PR[CURRENT_MODAL_TOPIC_ID].gp = 100;
  ytVideoCompleted = true;
  guideCompleted = true;
  updateModalStatusBtn("e");
  syncSessionStudyProgressUI();
  saveLocal();
  paint();
  syncTopicToServer(CURRENT_MODAL_TOPIC_ID);
  showToast("🟢 Tópico registrado manualmente como Concluído!");
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
  ctx.fillStyle = "#06141B";
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
  ctx.fillStyle = "#11212D";
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

  const cur = (typeof ytCurrentTime === "number" && ytCurrentTime > 0) ? ytCurrentTime : (sessionSeconds || 0);
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
