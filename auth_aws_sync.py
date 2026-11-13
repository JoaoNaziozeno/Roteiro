# -*- coding: utf-8 -*-
"""
Login, sessão e sincronização na nuvem (AWS Lambda + DynamoDB) usados por todas as páginas.

A senha é conferida na Lambda (aws_lambda_dynamodb.py). O navegador guarda só um token
assinado com validade; os dados de estudo ficam marcados com o dono (roteiro_data_owner)
e são apagados do navegador quando outra pessoa entra ou quando o aluno sai da conta.
"""

AUTH_GUARD_HEAD_SCRIPT = """
<script>
(function() {
  try {
    var raw = localStorage.getItem("roteiro_auth_user") || sessionStorage.getItem("roteiro_auth_user");
    var u = raw ? JSON.parse(raw) : null;
    var dev = location.hostname === "localhost" || location.hostname === "127.0.0.1" || location.protocol === "file:";
    var ok = u && u.authenticated && ((u.token && u.exp * 1000 > Date.now()) || (dev && u.email === "joao@roteiro.ia"));
    if (!ok) {
      sessionStorage.setItem("roteiro_redirect_after_login", location.pathname + location.search + location.hash);
      location.replace("index.html");
    }
  } catch (e) {
    location.replace("index.html");
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

_LBL = 'style="font-size:.78rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px"'
_ERR = 'class="forgot-error-box" style="display:none"'

CHANGE_CREDENTIALS_MODAL_HTML = f"""
<!-- MODAL: MEU PERFIL E SENHA -->
<div id="modal-change-credentials" class="modal-sub-overlay" hidden>
  <div class="modal-sub-box" style="max-width:480px;width:95%">
    <div class="modal-sub-header">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:1.3rem">🔑</span>
        <h3 class="modal-sub-title">Meu perfil e senha</h3>
      </div>
      <button class="modal-close-icon" onclick="closeChangeCredentialsModal()" aria-label="Fechar">✕</button>
    </div>

    <form id="form-change-credentials" onsubmit="handleSaveNewCredentials(event)">
      <div style="display:flex;flex-direction:column;gap:12px">
        <div>
          <label {_LBL} for="change-user-name">Nome</label>
          <input type="text" id="change-user-name" class="aws-cfg-input" required maxlength="80" autocomplete="name">
        </div>
        <div>
          <label {_LBL} for="change-user-email">E-mail da conta</label>
          <input type="email" id="change-user-email" class="aws-cfg-input" readonly disabled>
          <span style="font-size:.72rem;color:var(--mu);margin-top:3px;display:block">Para trocar o e-mail, fale com o administrador.</span>
        </div>
        <div class="dropdown-divider"></div>
        <p style="font-size:.78rem;color:var(--mu);margin:0">Deixe os campos de senha em branco para mudar só o nome.</p>
        <div>
          <label {_LBL} for="change-current-pass">Senha atual</label>
          <input type="password" id="change-current-pass" class="aws-cfg-input" autocomplete="current-password">
        </div>
        <div>
          <label {_LBL} for="change-new-pass">Nova senha (mínimo 8 caracteres)</label>
          <input type="password" id="change-new-pass" class="aws-cfg-input" minlength="8" autocomplete="new-password">
        </div>
        <div>
          <label {_LBL} for="change-confirm-pass">Confirmar nova senha</label>
          <input type="password" id="change-confirm-pass" class="aws-cfg-input" minlength="8" autocomplete="new-password">
        </div>
      </div>

      <div id="change-cred-error" {_ERR}></div>

      <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:18px">
        <button type="button" class="aws-btn-sec" onclick="closeChangeCredentialsModal()">Cancelar</button>
        <button type="submit" id="btn-save-credentials" class="aws-btn-primary">Salvar</button>
      </div>
    </form>
  </div>
</div>
"""

FORGOT_PASSWORD_MODAL_HTML = f"""
<!-- MODAL: ESQUECI A SENHA -->
<div id="modal-forgot-password" class="modal-sub-overlay" hidden>
  <div class="modal-sub-box" style="max-width:490px;width:95%">
    <div class="modal-sub-header">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:1.35rem">🔐</span>
        <h3 class="modal-sub-title" style="margin:0">Esqueci a senha</h3>
      </div>
      <button class="modal-close-icon" onclick="closeForgotPasswordModal()" aria-label="Fechar">✕</button>
    </div>

    <div id="forgot-step-channel">
      <div class="forgot-info-banner">Informe o e-mail da sua conta. Se ele estiver cadastrado, você recebe um código de 6 dígitos, válido por 15 minutos.</div>
      <form id="form-forgot-request" onsubmit="handleSendResetCode(event)">
        <label {_LBL} for="forgot-input-email">E-mail</label>
        <input type="email" id="forgot-input-email" class="aws-cfg-input" required autocomplete="email" placeholder="seu-email@dominio.com">
        <div id="forgot-msg-error-step1" {_ERR}></div>
        <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:20px">
          <button type="button" class="aws-btn-sec" onclick="closeForgotPasswordModal()">Cancelar</button>
          <button type="submit" id="btn-send-reset-code" class="aws-btn-primary">Enviar código</button>
        </div>
      </form>
    </div>

    <div id="forgot-step-verify" style="display:none">
      <div class="forgot-success-banner"><span>Se <b id="forgot-target-dest">...</b> estiver cadastrado, o código já foi enviado. Confira também a caixa de spam.</span></div>
      <form id="form-forgot-verify" onsubmit="handleVerifyAndResetPassword(event)">
        <div style="display:flex;flex-direction:column;gap:14px">
          <div>
            <label {_LBL} for="forgot-input-code">Código (6 dígitos)</label>
            <input type="text" id="forgot-input-code" class="aws-cfg-input otp-code-input" maxlength="6" pattern="[0-9]{{6}}" inputmode="numeric" required placeholder="000000" autocomplete="one-time-code">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px">
              <span style="font-size:.74rem;color:var(--mu)">Expira em: <b id="forgot-otp-timer">15:00</b></span>
              <button type="button" id="btn-resend-otp" class="forgot-link-btn" onclick="resendResetCode()" disabled>Reenviar (<span id="resend-countdown">60</span>s)</button>
            </div>
          </div>
          <div>
            <label {_LBL} for="forgot-new-pass">Nova senha (mínimo 8 caracteres)</label>
            <input type="password" id="forgot-new-pass" class="aws-cfg-input" required minlength="8" autocomplete="new-password">
          </div>
          <div>
            <label {_LBL} for="forgot-confirm-pass">Confirmar nova senha</label>
            <input type="password" id="forgot-confirm-pass" class="aws-cfg-input" required minlength="8" autocomplete="new-password">
          </div>
        </div>
        <div id="forgot-msg-error-step2" {_ERR}></div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:20px;gap:8px;flex-wrap:wrap">
          <button type="button" class="forgot-link-btn" onclick="backToChannelSelection()">← Trocar e-mail</button>
          <div style="display:flex;gap:10px">
            <button type="button" class="aws-btn-sec" onclick="closeForgotPasswordModal()">Cancelar</button>
            <button type="submit" id="btn-verify-reset-code" class="aws-btn-primary">Redefinir e entrar</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- MODAL: TENHO UM CONVITE -->
<div id="modal-accept-invite" class="modal-sub-overlay" hidden>
  <div class="modal-sub-box" style="max-width:490px;width:95%">
    <div class="modal-sub-header">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:1.35rem">✉️</span>
        <h3 class="modal-sub-title" style="margin:0">Tenho um convite</h3>
      </div>
      <button class="modal-close-icon" onclick="closeInviteModal()" aria-label="Fechar">✕</button>
    </div>
    <div class="forgot-info-banner">Use o e-mail em que você recebeu o convite e o código de 6 dígitos que veio nele (se não achar a mensagem, procure no spam). Aqui você cria a sua senha.</div>
    <form id="form-accept-invite" onsubmit="handleAcceptInvite(event)">
      <div style="display:flex;flex-direction:column;gap:12px">
        <div>
          <label {_LBL} for="invite-email">E-mail</label>
          <input type="email" id="invite-email" class="aws-cfg-input" required autocomplete="email">
        </div>
        <div>
          <label {_LBL} for="invite-code">Código do convite</label>
          <input type="text" id="invite-code" class="aws-cfg-input otp-code-input" maxlength="6" pattern="[0-9]{{6}}" inputmode="numeric" required placeholder="000000" autocomplete="one-time-code">
        </div>
        <div>
          <label {_LBL} for="invite-name">Como quer ser chamado (opcional)</label>
          <input type="text" id="invite-name" class="aws-cfg-input" maxlength="80" autocomplete="name">
        </div>
        <div>
          <label {_LBL} for="invite-pass">Crie uma senha (mínimo 8 caracteres)</label>
          <input type="password" id="invite-pass" class="aws-cfg-input" required minlength="8" autocomplete="new-password">
        </div>
        <div>
          <label {_LBL} for="invite-pass2">Confirme a senha</label>
          <input type="password" id="invite-pass2" class="aws-cfg-input" required minlength="8" autocomplete="new-password">
        </div>
      </div>
      <div id="invite-error" {_ERR}></div>
      <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:18px">
        <button type="button" class="aws-btn-sec" onclick="closeInviteModal()">Cancelar</button>
        <button type="submit" id="btn-accept-invite" class="aws-btn-primary">Criar senha e entrar</button>
      </div>
    </form>
  </div>
</div>
"""

AUTH_AWS_SYNC_JS = r"""
// =========================================================================
// LOGIN, SESSÃO E SINCRONIZAÇÃO NA NUVEM
// A senha é conferida na Lambda; aqui fica só o token assinado e a validade.
// =========================================================================
const AUTH_USER_KEY = "roteiro_auth_user";
const AWS_CONFIG_KEY = "roteiro_aws_config";
const DATA_OWNER_KEY = "roteiro_data_owner";      // e-mail do dono dos dados de estudo deste navegador
const SAVED_EMAIL_KEY = "roteiro_saved_email";    // e-mail lembrado na tela de login
const REDIRECT_KEY = "roteiro_redirect_after_login";
const TEST_USER_EMAIL = "joao@roteiro.ia";        // usuário de teste: só funciona em localhost e não sincroniza
const OFFICIAL_LAMBDA_URL = "https://x37p5anc5yesrwweqfbwxcexsu0dpzdu.lambda-url.us-east-2.on.aws/";

// Dados de estudo de quem está logado (apagados ao sair ou quando outra pessoa entra)
const STUDY_KEYS = [
  "roteiro-ia-v1", "roteiro-answers-v1", "roteiro-review-v1", "roteiro-events-v1", "roteiro-sessions-v1",
  "roteiro-log-start", "roteiro-start-date", "roteiro-hub-pace", "roteiro_portfolio_projects", "roteiro-snap-v1",
  "roteiro-effort-v1", "roteiro-auto-progress", "roteiro_aws_last_sync", "roteiro_password_hash", "roteiro-admin-rev", "roteiro-sync-base"
];
const STUDY_PREFIXES = ["roteiro-note-"];

let _awsRealtimeTimer = null;

function escapeHtml(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function isLocalDev() {
  const h = window.location.hostname;
  return h === "localhost" || h === "127.0.0.1" || window.location.protocol === "file:";
}

function isTestUser(u) {
  return !!u && u.email === TEST_USER_EMAIL && isLocalDev();
}

function clearAuthSession() {
  try { localStorage.removeItem(AUTH_USER_KEY); sessionStorage.removeItem(AUTH_USER_KEY); } catch (e) {}
}

// Retorna o usuário logado, ou null se não houver sessão válida.
function getLoggedInUser() {
  let u = null;
  try {
    const raw = localStorage.getItem(AUTH_USER_KEY) || sessionStorage.getItem(AUTH_USER_KEY);
    u = raw ? JSON.parse(raw) : null;
  } catch (e) { return null; }
  if (!u || !u.authenticated) return null;
  if (isTestUser(u)) return u;
  if (!u.token || !u.exp || u.exp * 1000 < Date.now()) { clearAuthSession(); return null; }
  return u;
}

function saveAuthSession(resp, remember) {
  const u = {
    authenticated: true, name: resp.user.name || "", email: resp.user.email,
    token: resp.token, exp: resp.expires_at, remember: !!remember
  };
  clearAuthSession();
  try { (remember ? localStorage : sessionStorage).setItem(AUTH_USER_KEY, JSON.stringify(u)); } catch (e) {}
  try {
    if (remember) localStorage.setItem(SAVED_EMAIL_KEY, u.email);
    else localStorage.removeItem(SAVED_EMAIL_KEY);
  } catch (e) {}
  return u;
}

function updateStoredUser(fields) {
  const u = getLoggedInUser();
  if (!u) return;
  Object.assign(u, fields);
  try { (localStorage.getItem(AUTH_USER_KEY) ? localStorage : sessionStorage).setItem(AUTH_USER_KEY, JSON.stringify(u)); } catch (e) {}
}

function wipeStudyData() {
  try {
    STUDY_KEYS.forEach(k => localStorage.removeItem(k));
    const extra = [];
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k && STUDY_PREFIXES.some(p => k.startsWith(p))) extra.push(k);
    }
    extra.forEach(k => localStorage.removeItem(k));
    localStorage.removeItem(DATA_OWNER_KEY);
  } catch (e) {}
}

// Garante que os dados de estudo deste navegador são de quem acabou de entrar.
// Dados de outra pessoa (ou sem dono conhecido) são apagados antes de baixar os da nuvem.
function claimLocalDataFor(email) {
  try {
    const owner = localStorage.getItem(DATA_OWNER_KEY);
    if (owner === email) return;
    // Navegadores do formato antigo não têm dono: os dados só são mantidos se o e-mail lembrado era o mesmo.
    const legacyEmail = (localStorage.getItem(SAVED_EMAIL_KEY) || "").toLowerCase();
    if (owner || legacyEmail !== email) wipeStudyData();
    localStorage.setItem(DATA_OWNER_KEY, email);
  } catch (e) {}
}

// Aceita só uma Function URL da AWS ou, com o site rodando em localhost, um servidor local de testes.
function isValidEndpoint(url) {
  return /^https:\/\/[a-z0-9]+\.lambda-url\.[a-z0-9-]+\.on\.aws\/?$/.test(url || "")
    || (isLocalDev() && /^http:\/\/(localhost|127\.0\.0\.1):\d+\/?$/.test(url || ""));
}

function getAwsConfig() {
  try {
    const cfg = JSON.parse(localStorage.getItem(AWS_CONFIG_KEY) || "{}") || {};
    if (!isValidEndpoint(cfg.endpoint)) cfg.endpoint = OFFICIAL_LAMBDA_URL;
    return cfg;
  } catch (e) {
    return { endpoint: OFFICIAL_LAMBDA_URL };
  }
}

function getAwsEndpointUrl() {
  return getAwsConfig().endpoint || OFFICIAL_LAMBDA_URL;
}

// Chamada à Lambda. Com auth=true envia o token; se a sessão expirou, leva para o login.
async function apiCall(action, payload = {}, auth = false) {
  const body = Object.assign({}, payload, { action });
  if (auth) {
    const u = getLoggedInUser();
    if (!u || !u.token) { handleSessionExpired(); throw new Error("Sessão expirada. Entre novamente."); }
    body.token = u.token;
  }
  let res, json = null;
  try {
    res = await fetch(getAwsEndpointUrl(), {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body), cache: "no-store"
    });
  } catch (e) {
    throw new Error("Sem conexão com o servidor. Verifique a internet e tente de novo.");
  }
  try { json = await res.json(); } catch (e) {}
  if (res.ok && json && json.ok) return json;
  if (auth && res.status === 401 && json && json.relogin) handleSessionExpired();
  const err = new Error((json && json.error) || `Erro no servidor (HTTP ${res.status}).`);
  err.status = res.status;
  throw err;
}

function handleSessionExpired() {
  clearAuthSession();
  try { sessionStorage.setItem(REDIRECT_KEY, location.pathname + location.search + location.hash); } catch (e) {}
  if (!/(^|\/)(index\.html)?$/.test(location.pathname)) location.replace("index.html");
  else if (typeof checkHubAuth === "function") checkHubAuth();
}

// Para onde ir depois do login: só caminhos deste mesmo site.
function takeRedirectAfterLogin() {
  let target = "";
  try { target = sessionStorage.getItem(REDIRECT_KEY) || ""; sessionStorage.removeItem(REDIRECT_KEY); } catch (e) {}
  if (!target || !target.startsWith("/") || target.startsWith("//")) return "index.html";
  return target;
}

function finishLogin(resp, remember) {
  // Primeiro confere de quem são os dados deste navegador (usa o e-mail lembrado ANTES de atualizá-lo).
  claimLocalDataFor(String(resp.user.email || "").toLowerCase());
  saveAuthSession(resp, remember);
  // Recarrega a página para que nada do usuário anterior fique na memória.
  window.location.href = takeRedirectAfterLogin();
}

function showFormError(el, msg) {
  if (!el) return;
  el.textContent = "⚠️ " + msg;
  el.style.display = "block";
}

function setBusy(btn, busy, label) {
  if (!btn) return;
  if (busy) { btn.dataset.label = btn.textContent; btn.textContent = label || "Aguarde..."; btn.disabled = true; }
  else { btn.textContent = btn.dataset.label || btn.textContent; btn.disabled = false; }
}

// ---------------------------------------------------------------- LOGIN
async function handlePortalLogin(e) {
  if (e) e.preventDefault();
  const email = document.getElementById("login-input-email").value.trim().toLowerCase();
  const pass = document.getElementById("login-input-pass").value;
  const remember = document.getElementById("login-remember-me").checked;
  const errorEl = document.getElementById("login-error-msg");
  const btn = document.querySelector("#portal-login-form button[type='submit']");
  if (errorEl) errorEl.style.display = "none";

  if (email === TEST_USER_EMAIL && isLocalDev()) {
    showFormError(errorEl, "O usuário de teste é criado direto no navegador, sem senha.");
    return;
  }
  setBusy(btn, true, "Entrando...");
  try {
    const resp = await apiCall("login", { email, password: pass, remember });
    finishLogin(resp, remember);
  } catch (err) {
    showFormError(errorEl, err.message);
    setBusy(btn, false);
  }
}

function updateNavAuthUI() {
  closeUserDropdown();
  const user = getLoggedInUser();
  if (!user) return;
  const name = user.name || user.email || "Estudante";
  const email = isTestUser(user) ? "Usuário de teste (local)" : (user.email || "");
  const userPill = document.getElementById("nav-auth-user");
  if (userPill) {
    userPill.innerHTML = `👤 <span>${escapeHtml(name)}</span> <span style="font-size:.7rem;margin-left:2px">▾</span>`;
    userPill.title = `Conectado como ${email} · Clique para opções`;
  }
  const dropName = document.getElementById("dropdown-user-name");
  const dropEmail = document.getElementById("dropdown-user-email");
  if (dropName) dropName.textContent = name;
  if (dropEmail) dropEmail.textContent = email;
}

function toggleUserDropdown(e) {
  if (e) e.stopPropagation();
  const dd = document.getElementById("nav-user-dropdown");
  const pill = document.getElementById("nav-auth-user");
  if (!dd) return;
  if (dd.hasAttribute("hidden") || dd.style.display === "none") {
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
  if (dd) { dd.setAttribute("hidden", "true"); dd.style.display = "none"; }
  if (pill) pill.classList.remove("active");
}

window.addEventListener("click", (e) => {
  const wrap = document.getElementById("nav-user-wrap");
  if (wrap && !wrap.contains(e.target)) closeUserDropdown();
});

async function handleUserLogout() {
  closeUserDropdown();
  if (!confirm("Deseja sair da sua conta? Seu progresso fica salvo na nuvem e é apagado deste navegador.")) return;
  const user = getLoggedInUser();
  if (user && !isTestUser(user)) {
    clearTimeout(_awsRealtimeTimer);
    const ok = await Promise.race([awsRealtimePushToDynamoDB(true), new Promise(r => setTimeout(() => r(false), 5000))]);
    if (!ok && !confirm("Não consegui enviar as últimas alterações para a nuvem. Sair mesmo assim? O que não foi enviado será perdido.")) return;
  }
  wipeStudyData();
  clearAuthSession();
  window.location.href = "index.html";
}

// ---------------------------------------------------------------- MODAIS
function showModal(id) {
  const m = document.getElementById(id);
  if (m) { m.hidden = false; m.removeAttribute("hidden"); m.style.display = "flex"; }
  return m;
}

function hideModal(id) {
  const m = document.getElementById(id);
  if (m) { m.hidden = true; m.setAttribute("hidden", "true"); m.style.display = "none"; }
}

function openChangeCredentialsModal() {
  closeUserDropdown();
  const user = getLoggedInUser();
  if (!user) return;
  document.getElementById("change-user-name").value = user.name || "";
  document.getElementById("change-user-email").value = user.email || "";
  ["change-current-pass", "change-new-pass", "change-confirm-pass"].forEach(id => document.getElementById(id).value = "");
  document.getElementById("change-cred-error").style.display = "none";
  showModal("modal-change-credentials");
}

function closeChangeCredentialsModal() { hideModal("modal-change-credentials"); }

async function handleSaveNewCredentials(e) {
  e.preventDefault();
  const user = getLoggedInUser();
  const errEl = document.getElementById("change-cred-error");
  const btn = document.getElementById("btn-save-credentials");
  const name = document.getElementById("change-user-name").value.trim();
  const cur = document.getElementById("change-current-pass").value;
  const nova = document.getElementById("change-new-pass").value;
  const conf = document.getElementById("change-confirm-pass").value;
  errEl.style.display = "none";
  if (!user) return;
  if (isTestUser(user)) { showFormError(errEl, "O usuário de teste não tem conta na nuvem."); return; }
  if ((cur || nova || conf) && (!cur || nova.length < 8)) { showFormError(errEl, "Para trocar a senha, informe a atual e uma nova com 8 caracteres ou mais."); return; }
  if (nova !== conf) { showFormError(errEl, "A confirmação da nova senha não confere."); return; }

  setBusy(btn, true, "Salvando...");
  try {
    if (name && name !== user.name) {
      const r = await apiCall("update_profile", { name }, true);
      updateStoredUser({ name: r.user.name });
    }
    if (nova) {
      const r = await apiCall("change_password", { current: cur, new: nova, remember: !!user.remember }, true);
      updateStoredUser({ token: r.token, exp: r.expires_at });
    }
    closeChangeCredentialsModal();
    updateNavAuthUI();
    if (typeof showToast === "function") showToast(nova ? "🔑 Senha alterada. As outras sessões foram encerradas." : "✅ Nome atualizado.");
  } catch (err) {
    showFormError(errEl, err.message);
  } finally {
    setBusy(btn, false);
  }
}

// ------------------------------------------------- ESQUECI A SENHA
let _otpExpiryTimer = null, _otpResendTimer = null;

function openForgotPasswordModal() {
  ["forgot-msg-error-step1", "forgot-msg-error-step2"].forEach(id => { const el = document.getElementById(id); if (el) el.style.display = "none"; });
  document.getElementById("forgot-step-channel").style.display = "block";
  document.getElementById("forgot-step-verify").style.display = "none";
  const loginEmail = document.getElementById("login-input-email");
  document.getElementById("forgot-input-email").value = loginEmail ? loginEmail.value.trim() : "";
  showModal("modal-forgot-password");
}

function closeForgotPasswordModal() {
  hideModal("modal-forgot-password");
  clearInterval(_otpExpiryTimer);
  clearInterval(_otpResendTimer);
}

function backToChannelSelection() {
  clearInterval(_otpExpiryTimer);
  clearInterval(_otpResendTimer);
  document.getElementById("forgot-step-channel").style.display = "block";
  document.getElementById("forgot-step-verify").style.display = "none";
}

async function handleSendResetCode(e) {
  if (e) e.preventDefault();
  const email = document.getElementById("forgot-input-email").value.trim().toLowerCase();
  const errEl = document.getElementById("forgot-msg-error-step1");
  const btn = document.getElementById("btn-send-reset-code");
  errEl.style.display = "none";
  setBusy(btn, true, "Enviando...");
  try {
    await apiCall("request_reset", { email });
    document.getElementById("forgot-target-dest").textContent = email;
    document.getElementById("forgot-step-channel").style.display = "none";
    document.getElementById("forgot-step-verify").style.display = "block";
    ["forgot-input-code", "forgot-new-pass", "forgot-confirm-pass"].forEach(id => document.getElementById(id).value = "");
    document.getElementById("forgot-msg-error-step2").style.display = "none";
    startOtpCountdown(15 * 60);
    startResendCountdown(60);
    document.getElementById("forgot-input-code").focus();
  } catch (err) {
    showFormError(errEl, err.message);
  } finally {
    setBusy(btn, false);
  }
}

async function resendResetCode() {
  const b = document.getElementById("btn-resend-otp");
  if (b && b.disabled) return;
  backToChannelSelection();
  await handleSendResetCode(null);
}

function startOtpCountdown(totalSec) {
  clearInterval(_otpExpiryTimer);
  let left = totalSec;
  const el = document.getElementById("forgot-otp-timer");
  const tick = () => {
    if (el) el.textContent = left > 0 ? `${String(Math.floor(left / 60)).padStart(2, "0")}:${String(left % 60).padStart(2, "0")}` : "Expirado";
    if (left-- <= 0) clearInterval(_otpExpiryTimer);
  };
  tick();
  _otpExpiryTimer = setInterval(tick, 1000);
}

function startResendCountdown(sec) {
  clearInterval(_otpResendTimer);
  let left = sec;
  const b = document.getElementById("btn-resend-otp");
  if (b) { b.disabled = true; b.innerHTML = `Reenviar (<span id="resend-countdown">${sec}</span>s)`; }
  _otpResendTimer = setInterval(() => {
    left--;
    const span = document.getElementById("resend-countdown");
    if (span) span.textContent = left;
    if (left <= 0) {
      clearInterval(_otpResendTimer);
      if (b) { b.disabled = false; b.textContent = "Reenviar código"; }
    }
  }, 1000);
}

async function handleVerifyAndResetPassword(e) {
  if (e) e.preventDefault();
  const email = document.getElementById("forgot-input-email").value.trim().toLowerCase();
  const code = document.getElementById("forgot-input-code").value.trim();
  const nova = document.getElementById("forgot-new-pass").value;
  const conf = document.getElementById("forgot-confirm-pass").value;
  const errEl = document.getElementById("forgot-msg-error-step2");
  const btn = document.getElementById("btn-verify-reset-code");
  errEl.style.display = "none";
  if (!/^\d{6}$/.test(code)) { showFormError(errEl, "O código tem 6 dígitos."); return; }
  if (nova.length < 8) { showFormError(errEl, "A nova senha precisa ter pelo menos 8 caracteres."); return; }
  if (nova !== conf) { showFormError(errEl, "A confirmação da senha não confere."); return; }
  setBusy(btn, true, "Validando...");
  try {
    await apiCall("confirm_reset", { email, code, password: nova });
    const remember = !!(document.getElementById("login-remember-me") || {}).checked;
    const resp = await apiCall("login", { email, password: nova, remember });
    closeForgotPasswordModal();
    finishLogin(resp, remember);
  } catch (err) {
    showFormError(errEl, err.message);
    setBusy(btn, false);
  }
}

// ------------------------------------------------- CONVITE
function openInviteModal() {
  ["invite-email", "invite-code", "invite-name", "invite-pass", "invite-pass2"].forEach(id => document.getElementById(id).value = "");
  document.getElementById("invite-error").style.display = "none";
  const loginEmail = document.getElementById("login-input-email");
  if (loginEmail) document.getElementById("invite-email").value = loginEmail.value.trim();
  showModal("modal-accept-invite");
}

function closeInviteModal() { hideModal("modal-accept-invite"); }

async function handleAcceptInvite(e) {
  e.preventDefault();
  const email = document.getElementById("invite-email").value.trim().toLowerCase();
  const code = document.getElementById("invite-code").value.trim();
  const name = document.getElementById("invite-name").value.trim();
  const pass = document.getElementById("invite-pass").value;
  const pass2 = document.getElementById("invite-pass2").value;
  const errEl = document.getElementById("invite-error");
  const btn = document.getElementById("btn-accept-invite");
  errEl.style.display = "none";
  if (!/^\d{6}$/.test(code)) { showFormError(errEl, "O código do convite tem 6 dígitos."); return; }
  if (pass.length < 8) { showFormError(errEl, "A senha precisa ter pelo menos 8 caracteres."); return; }
  if (pass !== pass2) { showFormError(errEl, "A confirmação da senha não confere."); return; }
  setBusy(btn, true, "Criando...");
  try {
    const remember = !!(document.getElementById("login-remember-me") || {}).checked;
    const resp = await apiCall("accept_invite", { email, code, name, password: pass, remember });
    closeInviteModal();
    finishLogin(resp, remember);
  } catch (err) {
    showFormError(errEl, err.message);
    setBusy(btn, false);
  }
}

// ------------------------------------------------- SINCRONIZAÇÃO

// -------------------------------------------------------------------------
// Dados de estudo além do progresso: revisões espaçadas, histórico de eventos
// (ritmo/previsão), sessões cronometradas e início do registro.
// Vão no campo "extra" do item do DynamoDB (limite do item: 400 KB), por isso
// eventos e sessões são compactados em arrays e limitados aos mais recentes.
// -------------------------------------------------------------------------
const AWS_EXTRA_MAX_EVENTS = 2500, AWS_EXTRA_MAX_SESSIONS = 1500;
function awsReadJson(k, d) { try { const r = localStorage.getItem(k); return r ? JSON.parse(r) : d; } catch (e) { return d; } }

function awsCollectExtra() {
  const ev = awsReadJson("roteiro-events-v1", []).slice(-AWS_EXTRA_MAX_EVENTS);
  const ses = awsReadJson("roteiro-sessions-v1", []).slice(-AWS_EXTRA_MAX_SESSIONS);
  const ls = parseInt(localStorage.getItem("roteiro-log-start") || "", 10);
  return {
    v: 1,
    reviews: awsReadJson("roteiro-review-v1", {}),
    answers: awsReadJson("roteiro-answers-v1", {}),
    events: ev.map(e => [e.t, e.id, e.f, e.to, e.src || "ui"]),
    sessions: ses.map(s => [s.t, s.id || "", s.sec || 0]),
    log_start: ls > 0 ? ls : null
  };
}

// Junta o que veio da nuvem com o que está neste dispositivo, sem perder nada de nenhum lado.
// Retorna true se este dispositivo tinha algo que a nuvem ainda não tinha.
function awsMergeExtra(x) {
  if (!x || typeof x !== "object") return false;
  let localHasMore = false;
  const num = v => (typeof v === "number" ? v : parseFloat(v)) || 0;

  // revisões: por tópico, fica o registro mais recente
  const locR = awsReadJson("roteiro-review-v1", {}), cloudR = x.reviews || {};
  const mergedR = Object.assign({}, locR);
  for (const k in cloudR) {
    const c = cloudR[k] || {}, l = locR[k];
    if (!l || num(c.last) >= num(l.last)) {
      mergedR[k] = Object.assign({}, c, {
        score: num(c.score), total: num(c.total), last: num(c.last),
        passedAt: c.passedAt ? num(c.passedAt) : undefined, done: c.done ? num(c.done) : undefined,
        next: Array.isArray(c.next) ? c.next.map(num) : undefined
      });
    }
  }
  for (const k in locR) if (!cloudR[k] || num(locR[k].last) > num(cloudR[k].last)) localHasMore = true;
  try { localStorage.setItem("roteiro-review-v1", JSON.stringify(mergedR)); } catch (e) {}

  // respostas das atividades das aulas: por tópico, fica a versão mais recente
  const locA = awsReadJson("roteiro-answers-v1", {}), cloudA = x.answers || {};
  const mergedA = Object.assign({}, locA);
  for (const k in cloudA) {
    const c = cloudA[k], l = locA[k];
    if (c && typeof c === "object" && (!l || num(c.t) >= num(l.t))) mergedA[k] = c;
  }
  for (const k in locA) if (!cloudA[k] || num(locA[k].t) > num(cloudA[k].t)) localHasMore = true;
  try { localStorage.setItem("roteiro-answers-v1", JSON.stringify(mergedA)); } catch (e) {}

  // eventos: união sem duplicar (mesmo instante + tópico + novo estado)
  const locE = awsReadJson("roteiro-events-v1", []);
  const seen = new Set(locE.map(e => e.t + "|" + e.id + "|" + e.to));
  const cloudE = (x.events || []).map(a => ({ t: num(a[0]), id: a[1], f: a[2], to: a[3], src: a[4] || "ui" }));
  const cloudSeen = new Set(cloudE.map(e => e.t + "|" + e.id + "|" + e.to));
  const evAll = locE.concat(cloudE.filter(e => !seen.has(e.t + "|" + e.id + "|" + e.to))).sort((a, b) => a.t - b.t).slice(-5000);
  if (locE.some(e => !cloudSeen.has(e.t + "|" + e.id + "|" + e.to))) localHasMore = true;
  try { localStorage.setItem("roteiro-events-v1", JSON.stringify(evAll)); } catch (e) {}

  // sessões de estudo: união por instante + tópico
  const locS = awsReadJson("roteiro-sessions-v1", []);
  const sSeen = new Set(locS.map(s => s.t + "|" + (s.id || "")));
  const cloudS = (x.sessions || []).map(a => ({ t: num(a[0]), id: a[1] || undefined, sec: num(a[2]) }));
  const cSeen = new Set(cloudS.map(s => s.t + "|" + (s.id || "")));
  const sAll = locS.concat(cloudS.filter(s => !sSeen.has(s.t + "|" + (s.id || "")))).sort((a, b) => a.t - b.t).slice(-2000);
  if (locS.some(s => !cSeen.has(s.t + "|" + (s.id || "")))) localHasMore = true;
  try { localStorage.setItem("roteiro-sessions-v1", JSON.stringify(sAll)); } catch (e) {}

  // início do registro: o mais antigo dos dois
  const lLs = parseInt(localStorage.getItem("roteiro-log-start") || "", 10) || 0, cLs = num(x.log_start);
  const ls = lLs && cLs ? Math.min(lLs, cLs) : (lLs || cLs);
  if (ls) try { localStorage.setItem("roteiro-log-start", String(ls)); } catch (e) {}
  if (lLs && (!cLs || lLs < cLs)) localHasMore = true;
  return localHasMore;
}

function canSync() {
  const u = getLoggedInUser();
  return !!u && !isTestUser(u) && localStorage.getItem(DATA_OWNER_KEY) === u.email;
}

function setSyncIndicator(text) {
  const el = document.getElementById("modal-sync-indicator");
  if (el) el.textContent = text;
}

function markCloudBadge() {
  const b = document.getElementById("nav-db-status");
  if (b) { b.className = "nav-status-pill badge-pg"; b.style.background = "#10b981"; b.style.color = "#fff"; b.textContent = "☁️ Nuvem"; }
}

function scheduleAwsRealtimeSync() {
  clearTimeout(_awsRealtimeTimer);
  _awsRealtimeTimer = setTimeout(() => awsRealtimePushToDynamoDB(true), 650);
}

// Versão da última edição de progresso feita pelo admin que este aparelho já baixou.
function getAdminRev() { return parseInt(localStorage.getItem("roteiro-admin-rev") || "0", 10) || 0; }

// Progresso como estava na última sincronização: serve para saber o que o aluno mudou desde então.
function setSyncBase(progress) { try { localStorage.setItem("roteiro-sync-base", JSON.stringify(progress || {})); } catch (e) {} }

function localChangesSinceSync() {
  const base = awsReadJson("roteiro-sync-base", {}), cur = awsReadJson("roteiro-ia-v1", {}), out = {};
  for (const k in cur) if (JSON.stringify(cur[k]) !== JSON.stringify(base[k])) out[k] = cur[k];
  return out;
}

async function awsRealtimePushToDynamoDB(silent = true, retry = true) {
  if (!canSync()) { setSyncIndicator("💾 Salvo neste navegador"); return false; }
  setSyncIndicator("☁️ Sincronizando...");
  const payload = {
    progress: awsReadJson("roteiro-ia-v1", {}),
    projects: awsReadJson("roteiro_portfolio_projects", []),
    start_date: localStorage.getItem("roteiro-start-date") || "",
    pace: localStorage.getItem("roteiro-hub-pace") || "std",
    extra: awsCollectExtra(),
    admin_rev: getAdminRev(),
    updated_at: Date.now()
  };
  try {
    await apiCall("save_data", payload, true);
    setSyncBase(payload.progress);
    const t = new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
    try { localStorage.setItem("roteiro_aws_last_sync", "Hoje, às " + t); } catch (e) {}
    markCloudBadge();
    setSyncIndicator("☁️ Salvo na nuvem (" + t + ")");
    if (!silent && typeof showToast === "function") showToast("☁️ Progresso salvo na nuvem!");
    return true;
  } catch (err) {
    if (err.status === 409 && retry) {
      // O admin editou o progresso: baixa a versão dele, reaplica o que o aluno mudou
      // desde a última sincronização e envia de novo.
      const mine = localChangesSinceSync();
      await awsRealtimePullFromDynamoDB();
      if (Object.keys(mine).length) {
        const cur = Object.assign(awsReadJson("roteiro-ia-v1", {}), mine);
        try { localStorage.setItem("roteiro-ia-v1", JSON.stringify(cur)); } catch (e) {}
        if (typeof PR !== "undefined") Object.assign(PR, mine);
        if (typeof paint === "function") paint();
      }
      return awsRealtimePushToDynamoDB(silent, false);
    }
    console.warn("[Sync] Falha ao enviar:", err.message);
    setSyncIndicator("⚠️ Não sincronizou (salvo neste navegador)");
    if (!silent) alert("⚠️ Não foi possível salvar na nuvem:\n\n" + err.message);
    return false;
  }
}

async function awsRealtimePullFromDynamoDB() {
  if (!canSync()) return false;
  const user = getLoggedInUser();
  let cloud;
  try {
    cloud = (await apiCall("get_data", {}, true)).data || {};
  } catch (err) {
    console.warn("[Sync] Falha ao baixar:", err.message);
    return false;
  }
  markCloudBadge();
  if (!Object.keys(cloud).length) {
    // Conta nova na nuvem: envia o que já existe neste navegador (dele mesmo).
    await awsRealtimePushToDynamoDB(true);
    return true;
  }
  const cloudRev = parseInt(cloud.admin_rev || 0, 10) || 0;
  if (cloudRev > getAdminRev()) {
    // O admin editou o progresso deste aluno: a versão da nuvem substitui a local (não junta),
    // senão tópicos zerados pelo admin voltariam deste aparelho.
    const fresh = (cloud.progress && typeof cloud.progress === "object") ? cloud.progress : {};
    try { localStorage.setItem("roteiro-ia-v1", JSON.stringify(fresh)); } catch (e) {}
    if (typeof PR !== "undefined") { for (const k in PR) delete PR[k]; Object.assign(PR, fresh); }
    try { localStorage.setItem("roteiro-admin-rev", String(cloudRev)); } catch (e) {}
  } else if (cloud.progress && typeof cloud.progress === "object") {
    const merged = Object.assign({}, awsReadJson("roteiro-ia-v1", {}), cloud.progress);
    try { localStorage.setItem("roteiro-ia-v1", JSON.stringify(merged)); } catch (e) {}
    if (typeof PR !== "undefined") for (const k in merged) PR[k] = merged[k];
  }
  if (Array.isArray(cloud.projects) && cloud.projects.length > 0) {
    try { localStorage.setItem("roteiro_portfolio_projects", JSON.stringify(cloud.projects)); } catch (e) {}
  }
  if (cloud.start_date && /^\d{4}-\d{2}-\d{2}$/.test(cloud.start_date)) {
    try { localStorage.setItem("roteiro-start-date", cloud.start_date); } catch (e) {}
    if (typeof currentStartDate !== "undefined") currentStartDate = cloud.start_date;
  }
  if (cloud.pace) {
    try { localStorage.setItem("roteiro-hub-pace", cloud.pace); } catch (e) {}
    if (typeof currentPace !== "undefined" && typeof HUB_PRESETS !== "undefined" && HUB_PRESETS[cloud.pace]) currentPace = cloud.pace;
  }
  setSyncBase(cloud.progress || {});
  const extraChanged = awsMergeExtra(cloud.extra);
  if (typeof paint === "function") paint();
  if (typeof calcAndPaint === "function") calcAndPaint();
  if (typeof renderHubDashboard === "function") renderHubDashboard();
  if (typeof renderProjects === "function") renderProjects();
  if (extraChanged && user) scheduleAwsRealtimeSync();
  return true;
}

window.addEventListener("DOMContentLoaded", () => {
  updateNavAuthUI();
  awsRealtimePullFromDynamoDB();
});
"""
