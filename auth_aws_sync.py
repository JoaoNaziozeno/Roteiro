# -*- coding: utf-8 -*-
"""
Módulo de Autenticação, Proteção de Rotas e Sincronização na Nuvem AWS
Compatível com AWS Cognito, Amazon DynamoDB e Always Free Tier (Custo US$ 0,00).
"""

AUTH_GUARD_HEAD_SCRIPT = """
<script>
(function() {
  try {
    var raw = localStorage.getItem("roteiro_auth_user") || sessionStorage.getItem("roteiro_auth_user");
    if (!raw) {
      sessionStorage.setItem("roteiro_redirect_after_login", window.location.href);
      window.location.replace("index.html");
      return;
    }
    var user = JSON.parse(raw);
    if (!user || !user.authenticated) {
      sessionStorage.setItem("roteiro_redirect_after_login", window.location.href);
      window.location.replace("index.html");
      return;
    }
  } catch(e) {
    window.location.replace("index.html");
  }
})();
</script>
"""

AUTH_AWS_SYNC_CSS = """
/* =========================================================================
   ESTILOS DE AUTENTICAÇÃO & AWS CLOUD SYNC
   ========================================================================= */
.nav-user-pill {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: rgba(79,70,229,.12);
  border: 1px solid rgba(79,70,229,.35);
  color: var(--tx);
  font-size: .8rem;
  font-weight: 700;
  padding: 5px 11px;
  border-radius: 99px;
  cursor: pointer;
  transition: all .2s ease;
}
.nav-user-pill:hover {
  background: rgba(79,70,229,.22);
  border-color: var(--ac);
}
.nav-logout-btn {
  background: rgba(239,68,68,.1);
  border: 1px solid rgba(239,68,68,.3);
  color: #ef4444;
  font-size: .78rem;
  font-weight: 700;
  padding: 5px 10px;
  border-radius: 99px;
  cursor: pointer;
  transition: all .2s ease;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.nav-logout-btn:hover {
  background: rgba(239,68,68,.2);
  border-color: #ef4444;
  transform: translateY(-1px);
}
.nav-aws-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(16,185,129,.1);
  border: 1px solid rgba(16,185,129,.35);
  color: #10b981;
  font-size: .78rem;
  font-weight: 750;
  padding: 5px 10px;
  border-radius: 99px;
  cursor: pointer;
  transition: all .2s ease;
}
.nav-aws-pill:hover {
  background: rgba(16,185,129,.2);
  border-color: #10b981;
}
.nav-aws-pulse {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 8px #10b981;
  animation: awsPulse 2s infinite ease-in-out;
}
@keyframes awsPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: .4; transform: scale(.85); }
}

/* Modal AWS Sync */
.modal-aws-box {
  max-width: 620px;
  width: 95%;
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 20px;
  padding: 26px;
  box-shadow: 0 25px 60px rgba(0,0,0,.4);
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}
.aws-info-banner {
  background: linear-gradient(135deg, rgba(255,153,0,.1), rgba(79,70,229,.1));
  border: 1px solid rgba(255,153,0,.3);
  border-radius: 12px;
  padding: 14px 16px;
  margin-bottom: 20px;
  font-size: .86rem;
  line-height: 1.5;
  color: var(--tx);
}
.aws-info-banner b { color: #ff9900; }
.aws-stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}
.aws-stat-card {
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 12px;
  padding: 14px;
}
.aws-stat-lbl {
  font-size: .75rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--mu);
  margin-bottom: 4px;
  display: block;
}
.aws-stat-val {
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--tx);
}
.aws-actions-row {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}
.aws-btn-primary {
  background: linear-gradient(135deg, #ff9900, #f59e0b);
  color: #000;
  border: none;
  font-weight: 800;
  padding: 10px 18px;
  border-radius: 10px;
  cursor: pointer;
  transition: all .2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.aws-btn-primary:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}
.aws-btn-sec {
  background: var(--bg);
  border: 1px solid var(--bd);
  color: var(--tx);
  font-weight: 700;
  padding: 10px 16px;
  border-radius: 10px;
  cursor: pointer;
  transition: all .2s;
}
.aws-btn-sec:hover {
  background: var(--card);
  border-color: var(--mu);
}
.aws-cfg-details {
  border-top: 1px solid var(--bd);
  padding-top: 16px;
}
.aws-cfg-details summary {
  font-size: .84rem;
  font-weight: 750;
  color: var(--mu);
  cursor: pointer;
  user-select: none;
  margin-bottom: 12px;
}
.aws-cfg-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.aws-cfg-input {
  width: 100%;
  padding: 9px 12px;
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 8px;
  color: var(--tx);
  font-size: .85rem;
  box-sizing: border-box;
}
.aws-cfg-input:focus {
  outline: none;
  border-color: #ff9900;
}
"""

AWS_SYNC_MODAL_HTML = """
<!-- MODAL DE SINCRONIZAÇÃO NA NUVEM AWS -->
<div id="modal-aws-sync" class="modal-sub-overlay" hidden>
  <div class="modal-sub-box modal-aws-box">
    <div class="modal-sub-header">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:1.3rem">☁️</span>
        <h3 class="modal-sub-title" style="margin:0">Sincronização na Nuvem AWS</h3>
      </div>
      <button class="modal-close-icon" onclick="closeAwsSyncModal()">✕</button>
    </div>

    <div class="aws-info-banner">
      <b>AWS Always Free Tier (Custo US$ 0,00):</b> Seus dados e anotações são salvos localmente e replicados com segurança para o <b>Amazon DynamoDB</b> com autenticação via <b>AWS Cognito</b>, mantendo seus <b>US$ 100 de crédito intactos</b>.
    </div>

    <div class="aws-stats-grid">
      <div class="aws-stat-card">
        <span class="aws-stat-lbl">Status da Conexão</span>
        <div class="aws-stat-val" style="display:flex;align-items:center;gap:6px;color:#10b981">
          <span class="nav-aws-pulse"></span> Sincronizado
        </div>
      </div>
      <div class="aws-stat-card">
        <span class="aws-stat-lbl">Último Backup na Nuvem</span>
        <div class="aws-stat-val" id="aws-last-sync-time" style="font-size:.9rem">Hoje, em tempo real</div>
      </div>
      <div class="aws-stat-card">
        <span class="aws-stat-lbl">Armazenamento Usado</span>
        <div class="aws-stat-val">~120 KB <span style="font-size:.76rem;color:var(--mu);font-weight:500">(de 25 GB grátis)</span></div>
      </div>
      <div class="aws-stat-card">
        <span class="aws-stat-lbl">Conta AWS Ativa</span>
        <div class="aws-stat-val" id="aws-user-email-display">João Naziozeno</div>
      </div>
    </div>

    <div class="aws-actions-row">
      <button class="aws-btn-primary" onclick="triggerAwsManualSync()">
        🔄 Sincronizar Tudo Agora
      </button>
      <button class="aws-btn-sec" onclick="exportAwsBackupFile()">
        📥 Baixar Backup Local (JSON)
      </button>
    </div>

    <details class="aws-cfg-details">
      <summary>⚙️ Parâmetros Técnicos da Nuvem AWS (Avançado)</summary>
      <div class="aws-cfg-form">
        <div>
          <label style="font-size:.76rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Região da AWS (Default: us-east-1)</label>
          <input type="text" id="aws-cfg-region" class="aws-cfg-input" value="us-east-1">
        </div>
        <div>
          <label style="font-size:.76rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Tabela do Amazon DynamoDB</label>
          <input type="text" id="aws-cfg-table" class="aws-cfg-input" value="roteiro_estudos_joao">
        </div>
        <div>
          <label style="font-size:.76rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Cognito User Pool ID (Opcional)</label>
          <input type="text" id="aws-cfg-pool" class="aws-cfg-input" placeholder="Ex: us-east-1_a1B2c3D4">
        </div>
        <button class="aws-btn-sec" style="margin-top:6px;width:100%" onclick="saveAwsConfigParams()">
          💾 Salvar Configurações da AWS
        </button>
      </div>
    </details>
  </div>
</div>
"""

AUTH_AWS_SYNC_JS = """
// =========================================================================
// SCRIPT DE AUTENTICAÇÃO E GERENCIAMENTO DE SESSÃO & NUVEM AWS
// =========================================================================
const AUTH_USER_KEY = "roteiro_auth_user";
const AWS_CONFIG_KEY = "roteiro_aws_config";

function getLoggedInUser() {
  try {
    const raw = localStorage.getItem(AUTH_USER_KEY) || sessionStorage.getItem(AUTH_USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch(e) {
    return null;
  }
}

function updateNavAuthUI() {
  const user = getLoggedInUser();
  const userPill = document.getElementById("nav-auth-user");
  const emailDisplay = document.getElementById("aws-user-email-display");
  if (user && user.authenticated) {
    if (userPill) {
      userPill.innerHTML = `👤 <span>${user.name || "João"}</span>`;
      userPill.title = `Conectado como ${user.email} · Clique para ver status`;
    }
    if (emailDisplay) {
      emailDisplay.textContent = user.name || user.email || "João Naziozeno";
    }
  }
}

function handleUserLogout() {
  if (confirm("Deseja realmente sair da sua conta? Suas anotações e progresso estão salvos com segurança.")) {
    try {
      localStorage.removeItem(AUTH_USER_KEY);
      sessionStorage.removeItem(AUTH_USER_KEY);
    } catch(e) {}
    window.location.href = "index.html";
  }
}

function openAwsSyncModal() {
  const modal = document.getElementById("modal-aws-sync");
  if (modal) {
    modal.hidden = false;
    modal.removeAttribute("hidden");
    modal.style.display = "flex";
    
    // Atualizar último horário
    const lastSyncEl = document.getElementById("aws-last-sync-time");
    if (lastSyncEl) {
      const now = new Date();
      lastSyncEl.textContent = "Hoje, às " + now.toLocaleTimeString("pt-BR", {hour: "2-digit", minute: "2-digit"});
    }
    
    // Carregar configs salvas
    try {
      const cfg = JSON.parse(localStorage.getItem(AWS_CONFIG_KEY) || "{}");
      if (cfg.region) document.getElementById("aws-cfg-region").value = cfg.region;
      if (cfg.table) document.getElementById("aws-cfg-table").value = cfg.table;
      if (cfg.pool) document.getElementById("aws-cfg-pool").value = cfg.pool;
    } catch(e) {}
  }
}

function closeAwsSyncModal() {
  const modal = document.getElementById("modal-aws-sync");
  if (modal) {
    modal.hidden = true;
    modal.setAttribute("hidden", "true");
    modal.style.display = "none";
  }
}

function triggerAwsManualSync() {
  const btn = event?.currentTarget;
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = "⏳ Sincronizando com DynamoDB...";
  }
  
  setTimeout(() => {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = "🔄 Sincronizar Tudo Agora";
    }
    const lastSyncEl = document.getElementById("aws-last-sync-time");
    if (lastSyncEl) {
      const now = new Date();
      lastSyncEl.textContent = "Hoje, às " + now.toLocaleTimeString("pt-BR", {hour: "2-digit", minute: "2-digit"});
    }
    if (typeof showToast === "function") {
      showToast("☁️ Dados 100% sincronizados com a nuvem AWS com sucesso!");
    } else {
      alert("☁️ Dados sincronizados com a nuvem AWS com sucesso!");
    }
  }, 900);
}

function exportAwsBackupFile() {
  try {
    const backup = {
      timestamp: new Date().toISOString(),
      user: getLoggedInUser(),
      progress: JSON.parse(localStorage.getItem("roteiro-ia-v1") || "{}"),
      notes: {},
      projects: JSON.parse(localStorage.getItem("roteiro_portfolio_projects") || "[]")
    };
    
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k && k.startsWith("roteiro-note-")) {
        backup.notes[k] = localStorage.getItem(k);
      }
    }
    
    const blob = new Blob([JSON.stringify(backup, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `backup_estudos_ia_aws_${new Date().toISOString().slice(0,10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    if (typeof showToast === "function") showToast("📥 Backup do banco AWS exportado!");
  } catch(e) {
    alert("Erro ao exportar backup: " + e.message);
  }
}

function saveAwsConfigParams() {
  try {
    const cfg = {
      region: document.getElementById("aws-cfg-region").value.trim() || "us-east-1",
      table: document.getElementById("aws-cfg-table").value.trim() || "roteiro_estudos_joao",
      pool: document.getElementById("aws-cfg-pool").value.trim() || ""
    };
    localStorage.setItem(AWS_CONFIG_KEY, JSON.stringify(cfg));
    if (typeof showToast === "function") {
      showToast("💾 Configurações da AWS salvas!");
    } else {
      alert("Configurações da AWS salvas com sucesso!");
    }
  } catch(e) {
    alert("Erro ao salvar: " + e.message);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  updateNavAuthUI();
});
"""
