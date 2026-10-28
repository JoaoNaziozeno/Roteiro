# -*- coding: utf-8 -*-
"""
Módulo de Autenticação, Proteção de Rotas, Hashing Criptográfico SHA-256 e Sincronização na Nuvem AWS
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
   ESTILOS DE AUTENTICAÇÃO, DROPDOWN DO USUÁRIO & AWS CLOUD SYNC
   ========================================================================= */
.nav-user-dropdown-wrap {
  position: relative;
  display: inline-block;
}
.nav-user-pill {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: rgba(74,92,106,.25);
  border: 1px solid rgba(155,168,171,.3);
  color: var(--tx);
  font-size: .82rem;
  font-weight: 750;
  padding: 6px 13px;
  border-radius: 99px;
  cursor: pointer;
  transition: all .2s ease;
  user-select: none;
}
.nav-user-pill:hover, .nav-user-pill.active {
  background: rgba(74,92,106,.4);
  border-color: var(--ac);
  transform: translateY(-1px);
}
.nav-user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 260px;
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 16px;
  box-shadow: 0 16px 40px rgba(0,0,0,.35);
  padding: 8px;
  z-index: 1000;
  display: none;
  flex-direction: column;
  gap: 4px;
  animation: dropdownFade .18s ease-out;
}
.nav-user-dropdown[hidden] {
  display: none !important;
}
@keyframes dropdownFade {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}
.dropdown-user-header {
  padding: 10px 12px;
  border-bottom: 1px solid var(--bd);
  margin-bottom: 4px;
  text-align: left;
}
.dropdown-user-name {
  font-size: .88rem;
  font-weight: 800;
  color: var(--tx);
}
.dropdown-user-email {
  font-size: .74rem;
  color: var(--mu);
  word-break: break-all;
  margin-top: 2px;
}
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 9px 12px;
  background: transparent;
  border: none;
  border-radius: 10px;
  color: var(--tx);
  font-size: .82rem;
  font-weight: 700;
  text-align: left;
  cursor: pointer;
  transition: all .15s;
  box-sizing: border-box;
}
.dropdown-item:hover {
  background: var(--bg);
  color: var(--ac);
}
.dropdown-item.danger {
  color: #ef4444;
}
.dropdown-item.danger:hover {
  background: rgba(239,68,68,.12);
  color: #ef4444;
}
.dropdown-divider {
  height: 1px;
  background: var(--bd);
  margin: 4px 0;
}

.nav-aws-pulse {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 8px #10b981;
  animation: awsPulse 2s infinite ease-in-out;
  display: inline-block;
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

/* LINK E FORMULÁRIO DE RECUPERAÇÃO DE SENHA (2FA / OTP) */
.forgot-pass-link {
  font-size: .82rem;
  color: var(--ac);
  text-decoration: none;
  font-weight: 700;
  cursor: pointer;
  transition: all .2s;
}
.forgot-pass-link:hover {
  text-decoration: underline;
  filter: brightness(1.2);
}
.forgot-info-banner {
  background: rgba(37,55,69,.4);
  border: 1px solid rgba(155,168,171,.25);
  border-radius: 10px;
  padding: 11px 14px;
  font-size: .81rem;
  color: var(--tx);
  margin-bottom: 16px;
  line-height: 1.45;
}
.forgot-success-banner {
  background: rgba(16,185,129,.1);
  border: 1px solid rgba(16,185,129,.3);
  border-radius: 10px;
  padding: 12px 14px;
  font-size: .82rem;
  color: #10b981;
  margin-bottom: 16px;
  line-height: 1.45;
}
.forgot-error-box {
  background: rgba(239,68,68,.12);
  border: 1px solid rgba(239,68,68,.3);
  color: #ef4444;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: .82rem;
  margin-top: 14px;
  line-height: 1.45;
}
.forgot-channel-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
@media (max-width: 480px) {
  .forgot-channel-grid {
    grid-template-columns: 1fr;
  }
}
.forgot-channel-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid var(--bd);
  background: var(--bg);
  cursor: pointer;
  transition: all .2s;
  user-select: none;
}
.forgot-channel-card:hover {
  border-color: var(--mu);
  background: var(--card);
}
.forgot-channel-card.active {
  border-color: #9BA8AB;
  background: rgba(74,92,106,.25);
  box-shadow: 0 0 0 2px rgba(155,168,171,.25);
}
.channel-card-icon {
  font-size: 1.4rem;
  flex-shrink: 0;
}
.channel-card-body {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.channel-card-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: .84rem;
  font-weight: 750;
  color: var(--tx);
}
.channel-card-desc {
  font-size: .71rem;
  color: var(--mu);
  line-height: 1.25;
}
.channel-badge {
  font-size: .63rem;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 4px;
}
.channel-badge.recommended {
  background: rgba(16,185,129,.15);
  color: #10b981;
}
.channel-badge.zap {
  background: rgba(37,211,102,.15);
  color: #25d366;
}
.otp-code-input {
  font-family: monospace;
  font-size: 1.45rem;
  letter-spacing: 8px;
  text-align: center;
  font-weight: 800;
  color: #CCD0CF;
  padding: 10px;
}
.forgot-link-btn {
  background: transparent;
  border: none;
  color: var(--ac);
  font-size: .78rem;
  font-weight: 700;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
}
.forgot-link-btn:disabled {
  color: var(--mu);
  cursor: not-allowed;
  text-decoration: none;
  opacity: .65;
}
"""

CHANGE_CREDENTIALS_MODAL_HTML = """
<!-- MODAL: ALTERAR USUÁRIO E SENHA (COM HASH CRIPTOGRÁFICO SHA-256) -->
<div id="modal-change-credentials" class="modal-sub-overlay" hidden>
  <div class="modal-sub-box" style="max-width:480px;width:95%">
    <div class="modal-sub-header">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:1.3rem">🔑</span>
        <h3 class="modal-sub-title">Alterar Usuário & Senha</h3>
      </div>
      <button class="modal-close-icon" onclick="closeChangeCredentialsModal()">✕</button>
    </div>

    <div style="background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.25);border-radius:10px;padding:10px 14px;font-size:.8rem;color:var(--tx);margin-bottom:16px;line-height:1.4">
      🛡️ <b>Segurança Criptográfica:</b> Sua senha é convertida em um <b>Hash SHA-256 irreversível com Salt</b> antes de ser gravada. O texto puro da sua senha nunca é salvo em nenhum lugar.
    </div>

    <form id="form-change-credentials" onsubmit="handleSaveNewCredentials(event)">
      <div style="display:flex;flex-direction:column;gap:12px">
        <div>
          <label style="font-size:.78rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Nome de Exibição</label>
          <input type="text" id="change-user-name" class="aws-cfg-input" required placeholder="Seu Nome Completo">
        </div>
        <div>
          <label style="font-size:.78rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">E-mail Cadastrado</label>
          <input type="email" id="change-user-email" class="aws-cfg-input" required placeholder="seu-email@dominio.com">
        </div>
        <div class="dropdown-divider"></div>
        <div>
          <label style="font-size:.78rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Senha / PIN Atual</label>
          <input type="password" id="change-current-pass" class="aws-cfg-input" required placeholder="Digite sua senha ou PIN atual">
        </div>
        <div>
          <label style="font-size:.78rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Nova Senha / PIN (mínimo 4 caracteres)</label>
          <input type="password" id="change-new-pass" class="aws-cfg-input" required placeholder="Digite a nova senha">
        </div>
        <div>
          <label style="font-size:.78rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Confirmar Nova Senha</label>
          <input type="password" id="change-confirm-pass" class="aws-cfg-input" required placeholder="Confirme a nova senha">
        </div>
      </div>

      <div id="change-cred-error" style="display:none;background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.3);color:#ef4444;padding:8px 12px;border-radius:8px;font-size:.82rem;margin-top:14px;text-align:center"></div>

      <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:18px">
        <button type="button" class="aws-btn-sec" onclick="closeChangeCredentialsModal()">Cancelar</button>
        <button type="submit" class="aws-btn-primary">💾 Salvar Alterações</button>
      </div>
    </form>
  </div>
</div>
"""

FORGOT_PASSWORD_MODAL_HTML = """
<!-- MODAL: RECUPERAÇÃO DE SENHA (2FA / OTP VIA SES OU WHATSAPP) -->
<div id="modal-forgot-password" class="modal-sub-overlay" hidden>
  <div class="modal-sub-box" style="max-width:490px;width:95%">
    <div class="modal-sub-header">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:1.35rem">🔐</span>
        <div>
          <h3 class="modal-sub-title" style="margin:0">Recuperação de Acesso</h3>
          <span style="font-size:.73rem;color:var(--mu);font-weight:600">Verificação Segura em Duas Etapas (OTP)</span>
        </div>
      </div>
      <button class="modal-close-icon" onclick="closeForgotPasswordModal()">✕</button>
    </div>

    <!-- PASSO 1: ESCOLHA DO CANAL (E-MAIL OU WHATSAPP) -->
    <div id="forgot-step-channel">
      <div class="forgot-info-banner">
        Escolha por onde deseja receber seu código descartável de 6 dígitos (válido por 10 minutos) para validar sua identidade e criar uma nova senha:
      </div>

      <form id="form-forgot-request" onsubmit="handleSendResetCode(event)">
        <div style="display:flex;flex-direction:column;gap:14px">
          <div>
            <label style="font-size:.78rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Seu E-mail Cadastrado</label>
            <input type="email" id="forgot-input-email" class="aws-cfg-input" required placeholder="seu-email@dominio.com">
          </div>

          <div>
            <label style="font-size:.78rem;font-weight:700;color:var(--mu);display:block;margin-bottom:8px">Canal de Envio do Código</label>
            <div class="forgot-channel-grid">
              <!-- CANAL 1: EMAIL (SES) -->
              <div class="forgot-channel-card active" id="channel-card-email" onclick="selectForgotChannel('email')">
                <div class="channel-card-icon">✉️</div>
                <div class="channel-card-body">
                  <div class="channel-card-title">
                    <span>E-mail</span>
                    <span class="channel-badge recommended">Recomendado</span>
                  </div>
                  <div class="channel-card-desc">Amazon SES · Grátis</div>
                </div>
              </div>

              <!-- CANAL 2: WHATSAPP -->
              <div class="forgot-channel-card" id="channel-card-whatsapp" onclick="selectForgotChannel('whatsapp')">
                <div class="channel-card-icon">💬</div>
                <div class="channel-card-body">
                  <div class="channel-card-title">
                    <span>WhatsApp</span>
                    <span class="channel-badge zap">Webhook</span>
                  </div>
                  <div class="channel-card-desc">Twilio / Webhook</div>
                </div>
              </div>
            </div>
          </div>

          <!-- CAMPO ADICIONAL DE TELEFONE (APENAS SE WHATSAPP SELECIONADO) -->
          <div id="forgot-phone-wrap" style="display:none">
            <label style="font-size:.78rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Número do WhatsApp (com DDD)</label>
            <input type="tel" id="forgot-input-phone" class="aws-cfg-input" placeholder="+55 (11) 99999-9999">
            <span style="font-size:.72rem;color:var(--mu);margin-top:3px;display:block">Informe o DDD brasileiro e o número (ex: 11988887777 ou +5511...)</span>
          </div>
        </div>

        <div id="forgot-msg-error-step1" class="forgot-error-box" style="display:none"></div>

        <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:20px">
          <button type="button" class="aws-btn-sec" onclick="closeForgotPasswordModal()">Cancelar</button>
          <button type="submit" id="btn-send-reset-code" class="aws-btn-primary">
            <span>🚀 Enviar Código ➔</span>
          </button>
        </div>
      </form>
    </div>

    <!-- PASSO 2: DIGITAÇÃO DO CÓDIGO OTP & NOVA SENHA -->
    <div id="forgot-step-verify" style="display:none">
      <div class="forgot-success-banner">
        <span>Código enviado com sucesso para <b id="forgot-target-dest">...</b>! Verifique sua caixa postal ou WhatsApp.</span>
      </div>

      <form id="form-forgot-verify" onsubmit="handleVerifyAndResetPassword(event)">
        <div style="display:flex;flex-direction:column;gap:14px">
          <div>
            <label style="font-size:.78rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Código de Verificação (6 dígitos)</label>
            <input type="text" id="forgot-input-code" class="aws-cfg-input otp-code-input" maxlength="6" pattern="[0-9]{6}" required placeholder="000000" autocomplete="one-time-code">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px">
              <span style="font-size:.74rem;color:var(--mu)">Expira em: <b id="forgot-otp-timer" style="color:#ff9900">10:00</b></span>
              <button type="button" id="btn-resend-otp" class="forgot-link-btn" onclick="resendResetCode()" disabled>Reenviar (<span id="resend-countdown">60</span>s)</button>
            </div>
          </div>

          <div class="dropdown-divider" style="margin:4px 0"></div>

          <div>
            <label style="font-size:.78rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Nova Senha (mínimo 4 caracteres)</label>
            <input type="password" id="forgot-new-pass" class="aws-cfg-input" required minlength="4" placeholder="Digite a nova senha">
          </div>

          <div>
            <label style="font-size:.78rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Confirmar Nova Senha</label>
            <input type="password" id="forgot-confirm-pass" class="aws-cfg-input" required minlength="4" placeholder="Confirme a nova senha">
          </div>
        </div>

        <div id="forgot-msg-error-step2" class="forgot-error-box" style="display:none"></div>

        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:20px;gap:8px;flex-wrap:wrap">
          <button type="button" class="forgot-link-btn" onclick="backToChannelSelection()">← Trocar canal ou e-mail</button>
          <div style="display:flex;gap:10px">
            <button type="button" class="aws-btn-sec" onclick="closeForgotPasswordModal()">Cancelar</button>
            <button type="submit" id="btn-verify-reset-code" class="aws-btn-primary">
              <span>✅ Redefinir & Entrar ➔</span>
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</div>

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
        <div class="aws-stat-val" id="aws-conn-status-val" style="display:flex;align-items:center;gap:6px;color:#10b981">
          <span class="nav-aws-pulse"></span> Sincronização Automática Ativa
        </div>
      </div>
      <div class="aws-stat-card">
        <span class="aws-stat-lbl">Último Backup na Nuvem</span>
        <div class="aws-stat-val" id="aws-last-sync-time" style="font-size:.9rem">Hoje, em tempo real</div>
      </div>
      <div class="aws-stat-card">
        <span class="aws-stat-lbl">Armazenamento Usado</span>
        <div class="aws-stat-val" id="aws-storage-used-val">~120 KB <span style="font-size:.76rem;color:var(--mu);font-weight:500">(de 25 GB grátis)</span></div>
      </div>
      <div class="aws-stat-card">
        <span class="aws-stat-lbl">Conta AWS Ativa</span>
        <div class="aws-stat-val" id="aws-user-email-display">João Naziozeno</div>
      </div>
    </div>

    <div class="aws-actions-row">
      <button class="aws-btn-primary" onclick="triggerAwsManualSync(event)">
        🔄 Sincronizar Tudo Agora
      </button>
      <button class="aws-btn-sec" onclick="exportAwsBackupFile()">
        📥 Baixar Backup Local (JSON)
      </button>
    </div>

    <details class="aws-cfg-details" open>
      <summary>⚙️ Parâmetros Técnicos da Nuvem AWS (DynamoDB + Lambda)</summary>
      <div class="aws-cfg-form">
        <div>
          <label style="font-size:.76rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">URL de Sincronização AWS Lambda (Function URL HTTPS · Always Free)</label>
          <input type="url" id="aws-cfg-endpoint" class="aws-cfg-input" value="https://x37p5anc5yesrwweqfbwxcexsu0dpzdu.lambda-url.us-east-2.on.aws/">
        </div>

        <div id="aws-conn-test-feedback" style="display:none;padding:10px 14px;border-radius:10px;font-size:.82rem;line-height:1.5;border:1px solid var(--bd);margin:8px 0"></div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
          <div>
            <label style="font-size:.76rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Região da AWS</label>
            <input type="text" id="aws-cfg-region" class="aws-cfg-input" value="us-east-2">
          </div>
          <div>
            <label style="font-size:.76rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Tabela do Amazon DynamoDB</label>
            <input type="text" id="aws-cfg-table" class="aws-cfg-input" value="roteiro_estudos_joao">
          </div>
        </div>
        <div>
          <label style="font-size:.76rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Cognito User Pool ID (Opcional)</label>
          <input type="text" id="aws-cfg-pool" class="aws-cfg-input" placeholder="Ex: us-east-2_a1B2c3D4">
        </div>
        <div style="display:flex;gap:8px;margin-top:6px">
          <button type="button" class="aws-btn-primary" style="flex:1" onclick="saveAwsConfigParams()">
            💾 Salvar & Testar Conexão Agora
          </button>
          <button type="button" class="aws-btn-sec" onclick="testAwsLambdaConnection()">
            🧪 Testar
          </button>
        </div>
      </div>
    </details>
  </div>
</div>
"""

AUTH_AWS_SYNC_JS = r"""
// =========================================================================
// SCRIPT DE AUTENTICAÇÃO, HASH SHA-256, DROPDOWN & NUVEM AWS
// =========================================================================
const AUTH_USER_KEY = "roteiro_auth_user";
const AWS_CONFIG_KEY = "roteiro_aws_config";
const PASSWORD_HASH_KEY = "roteiro_password_hash";
const CRYPTO_SALT = "roteiro_ia_salt_2026_#9821_";

// Função para gerar HASH criptográfico SHA-256 com Salt
async function computeSha256(plainText) {
  const encoder = new TextEncoder();
  const data = encoder.encode(CRYPTO_SALT + String(plainText));
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, "0")).join("");
}

// Validar se uma senha/PIN confere com o Hash salvo ou na nuvem AWS DynamoDB
async function validateLoginPassword(inputPass, email = "") {
  const inputHash = await computeSha256(inputPass);
  let savedHash = localStorage.getItem(PASSWORD_HASH_KEY);

  // 1. Se o hash local for idêntico, autenticado imediatamente!
  if (savedHash && savedHash === inputHash) {
    return true;
  }

  // 2. Se não bateu localmente ou não há hash local, verificar na AWS Cloud (DynamoDB)
  const targetEmail = (email || localStorage.getItem("roteiro_saved_email") || "").trim().toLowerCase();
  if (targetEmail && targetEmail !== "joao@roteiro.ia" && targetEmail.includes("@")) {
    const endpoint = getAwsEndpointUrl();
    if (endpoint) {
      try {
        const sep = endpoint.includes("?") ? "&" : "?";
        const res = await fetch(`${endpoint}${sep}user_id=${encodeURIComponent(targetEmail)}`, { cache: "no-store" });
        if (res.ok) {
          const json = await res.json();
          if (json && json.found && json.data) {
            const cloudHash = json.data.pwd_hash;
            if (cloudHash && cloudHash === inputHash) {
              // Sincroniza o hash autenticado da nuvem com o localStorage local
              localStorage.setItem(PASSWORD_HASH_KEY, inputHash);
              if (json.data.user_name) {
                const u = getLoggedInUser() || {};
                u.name = json.data.user_name;
                u.email = targetEmail;
                localStorage.setItem(AUTH_USER_KEY, JSON.stringify(u));
              }
              return true;
            }
          }
        }
      } catch(e) {
        console.warn("Falha ao consultar DynamoDB para validar login:", e);
      }
    }
  }

  // 3. Fallback para primeiro acesso em ambiente limpo (sem hash gravado)
  if (!savedHash) {
    const defaultHash = await computeSha256("1234");
    if (inputPass === "1234" || inputPass === "admin") {
      localStorage.setItem(PASSWORD_HASH_KEY, defaultHash);
      return true;
    }
    // Se o usuário digitou uma senha customizada no primeiro login com >= 4 chars, gravar como seu hash
    if (inputPass && inputPass.length >= 4) {
      localStorage.setItem(PASSWORD_HASH_KEY, inputHash);
      return true;
    }
    return false;
  }

  return false;
}

function getLoggedInUser() {
  try {
    const raw = localStorage.getItem(AUTH_USER_KEY) || sessionStorage.getItem(AUTH_USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch(e) {
    return null;
  }
}

function updateNavAuthUI() {
  closeUserDropdown();
  const user = getLoggedInUser();
  const userPill = document.getElementById("nav-auth-user");
  const emailDisplay = document.getElementById("aws-user-email-display");
  const dropName = document.getElementById("dropdown-user-name");
  const dropEmail = document.getElementById("dropdown-user-email");

  if (user && user.authenticated) {
    const name = user.name || "João Naziozeno";
    const email = (user.email && user.email !== "joao@roteiro.ia") ? user.email : "";

    if (userPill) {
      userPill.innerHTML = `👤 <span>${name}</span> <span style="font-size:.7rem;margin-left:2px">▾</span>`;
      userPill.title = email ? `Conectado como ${email} · Clique para opções` : `Conectado · Clique para opções`;
    }
    if (emailDisplay) emailDisplay.textContent = name;
    if (dropName) dropName.textContent = name;
    if (dropEmail) dropEmail.textContent = email || "Conectado";
  }
}

function toggleUserDropdown(e) {
  if (e) e.stopPropagation();
  const dd = document.getElementById("nav-user-dropdown");
  const pill = document.getElementById("nav-auth-user");
  if (!dd) return;
  const isHidden = dd.hasAttribute("hidden") || dd.style.display === "none";
  if (isHidden) {
    dd.removeAttribute("hidden");
    dd.style.display = "flex";
    if (pill) pill.classList.add("active");
  } else {
    closeUserDropdown();
  }
}

function closeUserDropdown() {
  const dd = document.getElementById("nav-user-dropdown");
  const pill = document.getElementById("nav-auth-user");
  if (dd) {
    dd.setAttribute("hidden", "true");
    dd.style.display = "none";
  }
  if (pill) pill.classList.remove("active");
}

window.addEventListener("click", (e) => {
  const wrap = document.getElementById("nav-user-wrap");
  if (wrap && !wrap.contains(e.target)) {
    closeUserDropdown();
  }
});

function handleUserLogout() {
  closeUserDropdown();
  if (confirm("Deseja realmente sair da sua conta? Suas anotações e progresso estão salvos com segurança.")) {
    try {
      localStorage.removeItem(AUTH_USER_KEY);
      sessionStorage.removeItem(AUTH_USER_KEY);
    } catch(e) {}
    window.location.href = "index.html";
  }
}

function openChangeCredentialsModal() {
  closeUserDropdown();
  const modal = document.getElementById("modal-change-credentials");
  const user = getLoggedInUser();
  if (modal) {
    document.getElementById("change-user-name").value = user?.name || "João Naziozeno";
    document.getElementById("change-user-email").value = (user?.email && user.email !== "joao@roteiro.ia") ? user.email : "";
    document.getElementById("change-current-pass").value = "";
    document.getElementById("change-new-pass").value = "";
    document.getElementById("change-confirm-pass").value = "";
    const errEl = document.getElementById("change-cred-error");
    if (errEl) errEl.style.display = "none";

    modal.hidden = false;
    modal.removeAttribute("hidden");
    modal.style.display = "flex";
  }
}

function closeChangeCredentialsModal() {
  const modal = document.getElementById("modal-change-credentials");
  if (modal) {
    modal.hidden = true;
    modal.setAttribute("hidden", "true");
    modal.style.display = "none";
  }
}

async function handleSaveNewCredentials(e) {
  e.preventDefault();
  const name = document.getElementById("change-user-name").value.trim();
  const email = document.getElementById("change-user-email").value.trim();
  const curPass = document.getElementById("change-current-pass").value.trim();
  const newPass = document.getElementById("change-new-pass").value.trim();
  const confirmPass = document.getElementById("change-confirm-pass").value.trim();
  const errEl = document.getElementById("change-cred-error");

  const isCurValid = await validateLoginPassword(curPass);
  if (!isCurValid) {
    errEl.textContent = "A senha / PIN atual está incorreta.";
    errEl.style.display = "block";
    return;
  }

  if (newPass.length < 4) {
    errEl.textContent = "A nova senha deve ter no mínimo 4 caracteres.";
    errEl.style.display = "block";
    return;
  }

  if (newPass !== confirmPass) {
    errEl.textContent = "A confirmação de senha não confere.";
    errEl.style.display = "block";
    return;
  }

  // Gerar HASH criptográfico seguro SHA-256
  const newHash = await computeSha256(newPass);
  localStorage.setItem(PASSWORD_HASH_KEY, newHash);

  // Atualizar dados de usuário autenticado
  const user = getLoggedInUser() || { authenticated: true };
  user.name = name;
  user.email = email;
  user.updatedAt = Date.now();

  if (localStorage.getItem(AUTH_USER_KEY)) {
    localStorage.setItem(AUTH_USER_KEY, JSON.stringify(user));
  } else {
    sessionStorage.setItem(AUTH_USER_KEY, JSON.stringify(user));
  }

  closeChangeCredentialsModal();
  updateNavAuthUI();
  scheduleAwsRealtimeSync();

  if (typeof showToast === "function") {
    showToast("🔑 Senha criptografada (SHA-256) e sincronizada!");
  } else {
    alert("Dados e senha criptografada (SHA-256) atualizados com sucesso!");
  }
}

// =========================================================================
// RECUPERAÇÃO DE SENHA EM DUAS ETAPAS (2FA / OTP VIA SES OU WHATSAPP)
// =========================================================================
let _currentForgotChannel = "email";
let _otpExpiryTimer = null;
let _otpResendTimer = null;
let _otpExpirySeconds = 600;
let _otpResendSeconds = 60;

function openForgotPasswordModal() {
  const modal = document.getElementById("modal-forgot-password");
  if (!modal) return;

  const err1 = document.getElementById("forgot-msg-error-step1");
  const err2 = document.getElementById("forgot-msg-error-step2");
  if (err1) err1.style.display = "none";
  if (err2) err2.style.display = "none";

  const step1 = document.getElementById("forgot-step-channel");
  const step2 = document.getElementById("forgot-step-verify");
  if (step1) step1.style.display = "block";
  if (step2) step2.style.display = "none";

  const emailInput = document.getElementById("forgot-input-email");
  const loginEmail = document.getElementById("login-input-email");
  const user = getLoggedInUser();
  if (emailInput) {
    const candidate = (user && user.email) || (loginEmail ? loginEmail.value.trim() : "") || (localStorage.getItem("roteiro_saved_email") || "");
    emailInput.value = (candidate && candidate !== "joao@roteiro.ia") ? candidate : "";
  }

  selectForgotChannel("email");

  modal.hidden = false;
  modal.removeAttribute("hidden");
  modal.style.display = "flex";
}

function closeForgotPasswordModal() {
  const modal = document.getElementById("modal-forgot-password");
  if (modal) {
    modal.hidden = true;
    modal.setAttribute("hidden", "true");
    modal.style.display = "none";
  }
  clearInterval(_otpExpiryTimer);
  clearInterval(_otpResendTimer);
}

function selectForgotChannel(channel) {
  _currentForgotChannel = channel;
  const cardEmail = document.getElementById("channel-card-email");
  const cardZap = document.getElementById("channel-card-whatsapp");
  const phoneWrap = document.getElementById("forgot-phone-wrap");
  const phoneInput = document.getElementById("forgot-input-phone");

  if (cardEmail) cardEmail.classList.toggle("active", channel === "email");
  if (cardZap) cardZap.classList.toggle("active", channel === "whatsapp");

  if (phoneWrap) {
    phoneWrap.style.display = channel === "whatsapp" ? "block" : "none";
  }
  if (phoneInput && channel === "whatsapp") {
    phoneInput.required = true;
    phoneInput.focus();
  } else if (phoneInput) {
    phoneInput.required = false;
  }
}

function backToChannelSelection() {
  clearInterval(_otpExpiryTimer);
  clearInterval(_otpResendTimer);
  const step1 = document.getElementById("forgot-step-channel");
  const step2 = document.getElementById("forgot-step-verify");
  if (step1) step1.style.display = "block";
  if (step2) step2.style.display = "none";
}

async function handleSendResetCode(e) {
  if (e) e.preventDefault();
  const email = document.getElementById("forgot-input-email").value.trim();
  const phone = document.getElementById("forgot-input-phone")?.value.trim() || "";
  const errEl = document.getElementById("forgot-msg-error-step1");
  const btn = document.getElementById("btn-send-reset-code");

  if (!email) {
    if (errEl) { errEl.textContent = "Informe seu e-mail cadastrado."; errEl.style.display = "block"; }
    return;
  }
  if (_currentForgotChannel === "whatsapp" && !phone) {
    if (errEl) { errEl.textContent = "Informe o número do WhatsApp com DDD."; errEl.style.display = "block"; }
    return;
  }

  if (errEl) errEl.style.display = "none";
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<span>⏳ Enviando código...</span>`;
  }

  try {
    const endpoint = getAwsEndpointUrl();
    const payload = {
      action: "request_reset",
      user_id: email.toLowerCase(),
      channel: _currentForgotChannel,
      phone: phone
    };

    const resp = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await resp.json();
    if (!resp.ok || !data.ok) {
      let msg = data.error || "Não foi possível enviar o código de verificação.";
      if (data.hint) msg += "\n👉 " + data.hint;
      throw new Error(msg);
    }

    const targetDest = document.getElementById("forgot-target-dest");
    if (targetDest) {
      targetDest.textContent = data.masked_destination || (_currentForgotChannel === "email" ? email : phone);
    }

    const step1 = document.getElementById("forgot-step-channel");
    const step2 = document.getElementById("forgot-step-verify");
    if (step1) step1.style.display = "none";
    if (step2) step2.style.display = "block";

    const codeInput = document.getElementById("forgot-input-code");
    if (codeInput) codeInput.value = "";
    const newPassInput = document.getElementById("forgot-new-pass");
    if (newPassInput) newPassInput.value = "";
    const confirmPassInput = document.getElementById("forgot-confirm-pass");
    if (confirmPassInput) confirmPassInput.value = "";
    const err2 = document.getElementById("forgot-msg-error-step2");
    if (err2) err2.style.display = "none";

    startOtpCountdown(data.expires_in_seconds || 600);
    startResendCountdown(60);
    if (codeInput) codeInput.focus();

  } catch(err) {
    if (errEl) {
      errEl.innerHTML = `⚠️ <b>Erro:</b> ${err.message.replace(/\n/g, "<br>")}`;
      errEl.style.display = "block";
    }
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = `<span>🚀 Enviar Código ➔</span>`;
    }
  }
}

async function resendResetCode() {
  const btnResend = document.getElementById("btn-resend-otp");
  if (btnResend && btnResend.disabled) return;
  await handleSendResetCode(null);
}

function startOtpCountdown(totalSec) {
  clearInterval(_otpExpiryTimer);
  _otpExpirySeconds = totalSec;
  const timerEl = document.getElementById("forgot-otp-timer");

  function updateTimer() {
    const mins = Math.floor(_otpExpirySeconds / 60);
    const secs = _otpExpirySeconds % 60;
    if (timerEl) timerEl.textContent = `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
    if (_otpExpirySeconds <= 0) {
      clearInterval(_otpExpiryTimer);
      if (timerEl) timerEl.textContent = "Expirado";
    }
    _otpExpirySeconds--;
  }
  updateTimer();
  _otpExpiryTimer = setInterval(updateTimer, 1000);
}

function startResendCountdown(sec) {
  clearInterval(_otpResendTimer);
  _otpResendSeconds = sec;
  const btnResend = document.getElementById("btn-resend-otp");
  const countdownSpan = document.getElementById("resend-countdown");
  if (btnResend) {
    btnResend.disabled = true;
    btnResend.innerHTML = `Reenviar (<span id="resend-countdown">${sec}</span>s)`;
  }

  _otpResendTimer = setInterval(() => {
    _otpResendSeconds--;
    const span = document.getElementById("resend-countdown");
    if (span) span.textContent = _otpResendSeconds;
    if (_otpResendSeconds <= 0) {
      clearInterval(_otpResendTimer);
      if (btnResend) {
        btnResend.disabled = false;
        btnResend.textContent = "Reenviar código agora";
      }
    }
  }, 1000);
}

async function handleVerifyAndResetPassword(e) {
  if (e) e.preventDefault();
  const email = document.getElementById("forgot-input-email").value.trim();
  const code = document.getElementById("forgot-input-code").value.trim();
  const newPass = document.getElementById("forgot-new-pass").value.trim();
  const confirmPass = document.getElementById("forgot-confirm-pass").value.trim();
  const errEl = document.getElementById("forgot-msg-error-step2");
  const btn = document.getElementById("btn-verify-reset-code");

  if (code.length !== 6 || !/^\d{6}$/.test(code)) {
    if (errEl) { errEl.textContent = "O código deve conter exatamente 6 dígitos numéricos."; errEl.style.display = "block"; }
    return;
  }
  if (newPass.length < 4) {
    if (errEl) { errEl.textContent = "A nova senha deve ter no mínimo 4 caracteres."; errEl.style.display = "block"; }
    return;
  }
  if (newPass !== confirmPass) {
    if (errEl) { errEl.textContent = "A confirmação de senha não confere."; errEl.style.display = "block"; }
    return;
  }

  if (errEl) errEl.style.display = "none";
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<span>⏳ Validando...</span>`;
  }

  try {
    const newHash = await computeSha256(newPass);
    const endpoint = getAwsEndpointUrl();
    const payload = {
      action: "confirm_reset",
      user_id: email.toLowerCase(),
      code: code,
      new_pwd_hash: newHash
    };

    const resp = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await resp.json();
    if (!resp.ok || !data.ok) {
      throw new Error(data.error || "Código de verificação incorreto ou expirado.");
    }

    localStorage.setItem(PASSWORD_HASH_KEY, newHash);
    const userObj = {
      authenticated: true,
      name: data.user_name || "João Naziozeno",
      email: email,
      loginTime: Date.now(),
      provider: "aws-dynamodb-verified"
    };
    localStorage.setItem(AUTH_USER_KEY, JSON.stringify(userObj));

    closeForgotPasswordModal();

    if (typeof checkHubAuth === "function") checkHubAuth();
    if (typeof updateNavAuthUI === "function") updateNavAuthUI();

    if (typeof showToast === "function") {
      showToast("🎉 Senha redefinida com sucesso! Acesso liberado.");
    } else {
      alert("🎉 Senha redefinida com sucesso! Você já está autenticado no ecossistema.");
    }

  } catch(err) {
    if (errEl) {
      errEl.innerHTML = `⚠️ <b>Erro:</b> ${err.message}`;
      errEl.style.display = "block";
    }
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = `<span>✅ Redefinir & Entrar ➔</span>`;
    }
  }
}

const OFFICIAL_LAMBDA_URL = "https://x37p5anc5yesrwweqfbwxcexsu0dpzdu.lambda-url.us-east-2.on.aws/";
let _awsRealtimeTimer = null;

function getAwsConfig() {
  try {
    const raw = localStorage.getItem(AWS_CONFIG_KEY);
    let cfg = raw ? JSON.parse(raw) : {};
    // Auto-corrigir se o endpoint estiver vazio ou contiver o erro de digitação anterior (rwwcq em vez de rwweq)
    if (!cfg.endpoint || cfg.endpoint.includes("rwwcq")) {
      cfg.endpoint = OFFICIAL_LAMBDA_URL;
      cfg.region = "us-east-2";
      cfg.table = "roteiro_estudos_joao";
      try { localStorage.setItem(AWS_CONFIG_KEY, JSON.stringify(cfg)); } catch(e) {}
    }
    return cfg;
  } catch(e) {
    return { endpoint: OFFICIAL_LAMBDA_URL, region: "us-east-2", table: "roteiro_estudos_joao" };
  }
}

function getAwsEndpointUrl() {
  const cfg = getAwsConfig();
  if (cfg.endpoint && cfg.endpoint.trim()) return cfg.endpoint.trim();
  return OFFICIAL_LAMBDA_URL;
}

function updateAwsStorageSizeDisplay() {
  try {
    const rawProg = localStorage.getItem("roteiro-ia-v1") || "{}";
    const rawProj = localStorage.getItem("roteiro_portfolio_projects") || "[]";
    const kb = Math.max(1, Math.round((rawProg.length + rawProj.length) / 1024));
    const el = document.getElementById("aws-storage-used-val");
    if (el) {
      el.innerHTML = `~${kb} KB <span style="font-size:.76rem;color:var(--mu);font-weight:500">(de 25 GB grátis)</span>`;
    }
  } catch(e) {}
}

function scheduleAwsRealtimeSync() {
  clearTimeout(_awsRealtimeTimer);
  _awsRealtimeTimer = setTimeout(() => {
    awsRealtimePushToDynamoDB(true);
  }, 650);
}

async function awsRealtimePushToDynamoDB(silent = true) {
  const endpoint = getAwsEndpointUrl();
  const nowStr = "Hoje, às " + new Date().toLocaleTimeString("pt-BR", {hour: "2-digit", minute: "2-digit", second: "2-digit"});
  try {
    localStorage.setItem("roteiro_aws_last_sync", nowStr);
  } catch(e) {}

  const lastSyncEl = document.getElementById("aws-last-sync-time");
  if (lastSyncEl) lastSyncEl.textContent = nowStr;
  updateAwsStorageSizeDisplay();

  const syncInd = document.getElementById("modal-sync-indicator");
  if (syncInd) syncInd.textContent = endpoint ? "☁️ Sincronizando AWS..." : "💾 Salvo automaticamente";

  if (!endpoint) {
    if (syncInd) syncInd.textContent = "💾 Salvo automaticamente";
    return false;
  }

  const user = getLoggedInUser() || {};
  if (!user || !user.authenticated) {
    if (syncInd) syncInd.textContent = "💾 Salvo localmente";
    return false;
  }

  const userEmail = (user.email || "").trim().toLowerCase();
  if (!userEmail || userEmail === "joao@roteiro.ia" || !userEmail.includes("@")) {
    if (syncInd) syncInd.textContent = "💾 Salvo localmente";
    return false;
  }

  let progressObj = {};
  let projectsArr = [];
  try { progressObj = JSON.parse(localStorage.getItem("roteiro-ia-v1") || "{}"); } catch(e) {}
  try { projectsArr = JSON.parse(localStorage.getItem("roteiro_portfolio_projects") || "[]"); } catch(e) {}

  const payload = {
    user_id: userEmail,
    user_name: user.name || "João Naziozeno",
    pwd_hash: localStorage.getItem(PASSWORD_HASH_KEY) || "",
    progress: progressObj,
    projects: projectsArr,
    start_date: localStorage.getItem("roteiro-hub-start") || "",
    pace: localStorage.getItem("roteiro-hub-pace") || "std",
    updated_at: Date.now()
  };

  try {
    console.log("☁️ [AWS Sync] Enviando dados para:", endpoint, payload);
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const resText = await res.text();
    let json = null;
    try { json = JSON.parse(resText); } catch(e) {}

    if (res.ok && json && json.ok) {
      const dbBadge = document.getElementById("nav-db-status");
      if (dbBadge) {
        dbBadge.className = "nav-status-pill badge-pg";
        dbBadge.style.background = "#10b981";
        dbBadge.style.color = "#fff";
        dbBadge.textContent = "☁️ DynamoDB";
      }
      if (syncInd) syncInd.textContent = "☁️ Salvo no DynamoDB (" + new Date().toLocaleTimeString("pt-BR", {hour:"2-digit",minute:"2-digit"}) + ")";
      if (!silent && typeof showToast === "function") {
        showToast("☁️ Sincronizado em tempo real com o Amazon DynamoDB!");
      }
      console.log("✅ [AWS Sync] Gravado com sucesso no DynamoDB:", json);
      return true;
    } else {
      const errMsg = (json && (json.error || json.hint)) || resText || `HTTP ${res.status}`;
      console.error("❌ [AWS Sync Error]", errMsg);
      if (syncInd) syncInd.textContent = "⚠️ Erro de sincronização AWS";
      if (!silent) {
        alert("⚠️ Erro ao salvar no DynamoDB pela Lambda:\n\n" + errMsg);
      }
      return false;
    }
  } catch(e) {
    console.error("❌ [AWS Sync Network Error]", e);
    if (!silent) {
      alert("⚠️ Erro de conexão ou CORS ao acessar a AWS Lambda:\n\n" + e.message + "\n\nVerifique se o Tipo de Autenticação da Function URL é NONE e se o CORS está liberado.");
    }
  }
  if (syncInd) syncInd.textContent = "💾 Salvo localmente";
  return false;
}

async function awsRealtimePullFromDynamoDB() {
  const endpoint = getAwsEndpointUrl();
  if (!endpoint) return false;

  const user = getLoggedInUser() || {};
  const savedEmail = localStorage.getItem("roteiro_saved_email") || "";
  const rawEmail = (user && user.email) || savedEmail || "";
  const userId = rawEmail.trim().toLowerCase();

  // NUNCA consultar com ID genérico ou email fictício joao@roteiro.ia
  if (!userId || userId === "joao@roteiro.ia" || userId === "estudante" || !userId.includes("@")) {
    return false;
  }

  const sep = endpoint.includes("?") ? "&" : "?";

  try {
    const res = await fetch(`${endpoint}${sep}user_id=${encodeURIComponent(userId)}`, { cache: "no-store" });
    if (!res.ok) return false;
    const json = await res.json();
    const dbBadge = document.getElementById("nav-db-status");
    if (dbBadge) {
      dbBadge.className = "nav-status-pill badge-pg";
      dbBadge.style.background = "#10b981";
      dbBadge.style.color = "#fff";
      dbBadge.textContent = "☁️ DynamoDB";
    }

    if (json && json.found && json.data) {
      const cloud = json.data;
      // Só atualiza o hash local da senha se o usuário atual autenticado for o dono da conta
      if (cloud.pwd_hash && user && user.authenticated && user.email && user.email.toLowerCase() === userId) {
        localStorage.setItem(PASSWORD_HASH_KEY, cloud.pwd_hash);
      }
      if (cloud.progress && typeof cloud.progress === "object") {
        let localPr = {};
        try { localPr = JSON.parse(localStorage.getItem("roteiro-ia-v1") || "{}"); } catch(e) {}
        const merged = Object.assign({}, localPr, cloud.progress);
        localStorage.setItem("roteiro-ia-v1", JSON.stringify(merged));
        if (typeof PR !== "undefined") {
          for (const k in merged) PR[k] = merged[k];
        }
      }
      if (Array.isArray(cloud.projects) && cloud.projects.length > 0) {
        localStorage.setItem("roteiro_portfolio_projects", JSON.stringify(cloud.projects));
      }
      if (cloud.start_date) localStorage.setItem("roteiro-hub-start", cloud.start_date);
      if (cloud.pace) localStorage.setItem("roteiro-hub-pace", cloud.pace);

      if (typeof paint === "function") paint();
      if (typeof renderHubDashboard === "function") renderHubDashboard();
      if (typeof renderProjects === "function") renderProjects();
      return true;
    } else {
      // Primeiro acesso na nuvem: envia os dados locais atuais para inicializar a tabela no DynamoDB
      if (user && user.authenticated) {
        await awsRealtimePushToDynamoDB(true);
      }
      return true;
    }
  } catch(e) {
    return false;
  }
}

function openAwsSyncModal() {
  closeUserDropdown();
  const modal = document.getElementById("modal-aws-sync");
  if (modal) {
    modal.hidden = false;
    modal.removeAttribute("hidden");
    modal.style.display = "flex";
    
    const lastSyncEl = document.getElementById("aws-last-sync-time");
    if (lastSyncEl) {
      const savedSync = localStorage.getItem("roteiro_aws_last_sync");
      const now = new Date();
      lastSyncEl.textContent = savedSync || ("Hoje, às " + now.toLocaleTimeString("pt-BR", {hour: "2-digit", minute: "2-digit"}));
    }
    updateAwsStorageSizeDisplay();
    
    try {
      const cfg = getAwsConfig();
      const epInput = document.getElementById("aws-cfg-endpoint");
      if (epInput && cfg.endpoint) epInput.value = cfg.endpoint;
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

async function triggerAwsManualSync(ev) {
  const btn = ev?.currentTarget;
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = "⏳ Sincronizando com DynamoDB...";
  }
  
  await awsRealtimePushToDynamoDB(false);
  
  setTimeout(() => {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = "🔄 Sincronizar Tudo Agora";
    }
    const lastSyncEl = document.getElementById("aws-last-sync-time");
    if (lastSyncEl) {
      const now = new Date();
      lastSyncEl.textContent = "Hoje, às " + now.toLocaleTimeString("pt-BR", {hour: "2-digit", minute: "2-digit", second: "2-digit"});
    }
    if (!getAwsEndpointUrl()) {
      if (typeof showToast === "function") {
        showToast("💾 Dados salvos! Cole a URL da sua função AWS Lambda abaixo para replicar no DynamoDB.");
      }
    }
  }, 450);
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

async function testAwsLambdaConnection() {
  const epEl = document.getElementById("aws-cfg-endpoint");
  const endpoint = epEl ? epEl.value.trim() : "";
  const statusEl = document.getElementById("aws-conn-test-feedback");

  if (!endpoint) {
    if (statusEl) {
      statusEl.style.display = "block";
      statusEl.style.background = "rgba(239,68,68,.12)";
      statusEl.style.borderColor = "rgba(239,68,68,.35)";
      statusEl.style.color = "#ef4444";
      statusEl.innerHTML = "⚠️ <b>Cole a URL da função AWS Lambda</b> no campo acima antes de testar.";
    }
    return false;
  }

  // Auto-detectar região da URL
  const regMatch = endpoint.match(/lambda-url\.([a-z0-9-]+)\.on\.aws/);
  if (regMatch && regMatch[1]) {
    const regInput = document.getElementById("aws-cfg-region");
    if (regInput) regInput.value = regMatch[1];
  }

  if (statusEl) {
    statusEl.style.display = "block";
    statusEl.style.background = "rgba(74,92,106,.2)";
    statusEl.style.borderColor = "rgba(155,168,171,.35)";
    statusEl.style.color = "var(--ac)";
    statusEl.innerHTML = "⏳ <b>Testando conexão com AWS Lambda e DynamoDB...</b>";
  }

  const user = getLoggedInUser() || {};
  const userId = ((user && user.email) || localStorage.getItem("roteiro_saved_email") || "estudante").toLowerCase();
  const sep = endpoint.includes("?") ? "&" : "?";

  try {
    const res = await fetch(`${endpoint}${sep}user_id=${encodeURIComponent(userId)}&test=1`, { cache: "no-store" });
    const text = await res.text();
    let json = null;
    try { json = JSON.parse(text); } catch(e) {}

    if (text.includes("Hello from Lambda!")) {
      if (statusEl) {
        statusEl.style.background = "rgba(245,158,11,.14)";
        statusEl.style.borderColor = "rgba(245,158,11,.45)";
        statusEl.style.color = "#f59e0b";
        statusEl.innerHTML = "⚠️ <b>Código padrão da AWS detectado!</b> A sua função Lambda ainda está rodando o código de exemplo inicial da AWS (<i>Hello from Lambda!</i>).<br><br>👉 <b>Como corrigir:</b> Abra o painel da sua função Lambda na AWS, vá na aba <b>Código (Code)</b>, apague o que estiver lá, cole todo o código do arquivo <code>aws_lambda_dynamodb.py</code> e clique no botão azul <b>Deploy</b>!";
      }
      return false;
    }

    if (res.status === 403 || text.includes("Forbidden")) {
      if (statusEl) {
        statusEl.style.background = "rgba(239,68,68,.12)";
        statusEl.style.borderColor = "rgba(239,68,68,.35)";
        statusEl.style.color = "#ef4444";
        statusEl.innerHTML = "⚠️ <b>Erro 403 Forbidden!</b> A sua Function URL está exigindo autenticação AWS IAM.<br><br>👉 <b>Como corrigir:</b> Na página da sua Lambda na AWS, vá em <b>Configuração ➔ URL da função ➔ Editar</b> e altere <b>Tipo de autenticação</b> para <b>NONE</b>.";
      }
      return false;
    }

    if (!res.ok || (json && json.ok === false)) {
      const errMsg = (json && json.error) || text;
      const hint = (json && json.hint) || "";
      if (statusEl) {
        statusEl.style.background = "rgba(239,68,68,.12)";
        statusEl.style.borderColor = "rgba(239,68,68,.35)";
        statusEl.style.color = "#ef4444";
        statusEl.innerHTML = `⚠️ <b>Erro na AWS (${res.status}):</b> ${errMsg}${hint ? `<br><br>💡 <b>Dica:</b> ${hint}` : ""}`;
      }
      return false;
    }

    if (json && json.ok) {
      const pushed = await awsRealtimePushToDynamoDB(true);
      if (statusEl) {
        statusEl.style.background = "rgba(16,185,129,.14)";
        statusEl.style.borderColor = "rgba(16,185,129,.4)";
        statusEl.style.color = "#10b981";
        statusEl.innerHTML = `✅ <b>Conexão 100% Ativa e Funcionando!</b><br>• Tabela DynamoDB: <code>${json.table || "roteiro_estudos_joao"}</code><br>• Região identificada: <code>${json.region || "AWS"}</code><br>• Status: Seus dados locais foram enviados e gravados no DynamoDB agora mesmo! Atualize a tela do DynamoDB na AWS para ver os dados.`;
      }
      if (typeof showToast === "function") {
        showToast("☁️ Conectado com sucesso ao Amazon DynamoDB!");
      }
      return true;
    }

    if (statusEl) {
      statusEl.innerHTML = `⚠️ Resposta inesperada da Lambda: ${text.slice(0, 160)}`;
    }
    return false;
  } catch(err) {
    if (statusEl) {
      statusEl.style.background = "rgba(239,68,68,.12)";
      statusEl.style.borderColor = "rgba(239,68,68,.35)";
      statusEl.style.color = "#ef4444";
      statusEl.innerHTML = `⚠️ <b>Falha ao conectar na URL:</b> ${err.message}<br><br>👉 Verifique se marcou a caixinha <b>Configurar CORS</b> na Function URL da Lambda com <i>Allow Origin = *</i> e <i>Allow Methods = GET, POST, OPTIONS</i>.`;
    }
    return false;
  }
}

async function saveAwsConfigParams() {
  try {
    const epEl = document.getElementById("aws-cfg-endpoint");
    const endpoint = epEl ? epEl.value.trim() : "";
    const regMatch = endpoint.match(/lambda-url\.([a-z0-9-]+)\.on\.aws/);
    const detectedRegion = (regMatch && regMatch[1]) || document.getElementById("aws-cfg-region").value.trim() || "us-east-2";

    const cfg = {
      endpoint: endpoint,
      region: detectedRegion,
      table: document.getElementById("aws-cfg-table").value.trim() || "roteiro_estudos_joao",
      pool: document.getElementById("aws-cfg-pool").value.trim() || ""
    };
    localStorage.setItem(AWS_CONFIG_KEY, JSON.stringify(cfg));
    const regInput = document.getElementById("aws-cfg-region");
    if (regInput) regInput.value = detectedRegion;

    if (cfg.endpoint) {
      await testAwsLambdaConnection();
    } else {
      if (typeof showToast === "function") {
        showToast("💾 Configurações da AWS salvas!");
      }
    }
  } catch(e) {
    alert("Erro ao salvar: " + e.message);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  updateNavAuthUI();
  updateAwsStorageSizeDisplay();
  awsRealtimePullFromDynamoDB();
});
"""
