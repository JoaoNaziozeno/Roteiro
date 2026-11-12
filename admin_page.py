# -*- coding: utf-8 -*-
"""
Gera admin.html: painel do administrador (login próprio, alunos, progresso e histórico).

Fala só com a Lambda (aws_lambda_dynamodb.py) usando um token de admin, que fica no
sessionStorage e vale 1 hora. Nada de estudo do aluno é guardado neste navegador.
"""

import json

from favicon import FAVICON_LINK

TRAIL_NAMES = {"ia": "IA & Código", "mat": "Matemática", "ing": "Inglês"}


def _topic_title(raw):
    if isinstance(raw, dict):
        return raw.get("title", "")
    if isinstance(raw, str) and "||" in raw:
        return raw.split("||", 1)[0]
    return str(raw)


def build_topics(tracks):
    """{"ia": [{"t": título da fase, "items": [[id, título], ...]}, ...], ...} com os ids do progresso."""
    out = {}
    for tr, phases in tracks.items():
        out[tr] = []
        for p_idx, p in enumerate(phases):
            items = []
            for g_idx, g in enumerate(p["g"]):
                for t_idx, raw in enumerate(g[1]):
                    items.append([f"{tr}-{p_idx}-{g_idx}-{t_idx}", _topic_title(raw)])
            out[tr].append({"t": p.get("t", f"Fase {p_idx + 1}"), "items": items})
    return out


ADMIN_HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Painel do Administrador · Roteiro</title>
__FAVICON__
<style>
:root{--bg:#f6f7f9;--card:#fff;--tx:#18202a;--mu:#5d6876;--bd:#dfe3e8;--ac:#2f6fed;--ac-tx:#fff;--ok:#12805c;--ok-bg:#e3f5ee;--warn:#9a6200;--warn-bg:#fdf1dc;--bad:#b42318;--bad-bg:#fde8e7;--bar:#e8ebef}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0f1318;--card:#171c23;--tx:#e6e9ee;--mu:#9aa4b1;--bd:#2a313b;--ac:#6d9bff;--ac-tx:#0f1318;--ok:#4fd1a1;--ok-bg:#12302a;--warn:#f0b75a;--warn-bg:#33270f;--bad:#ff8a80;--bad-bg:#3a1714;--bar:#252c35}}
:root[data-theme="dark"]{--bg:#0f1318;--card:#171c23;--tx:#e6e9ee;--mu:#9aa4b1;--bd:#2a313b;--ac:#6d9bff;--ac-tx:#0f1318;--ok:#4fd1a1;--ok-bg:#12302a;--warn:#f0b75a;--warn-bg:#33270f;--bad:#ff8a80;--bad-bg:#3a1714;--bar:#252c35}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
button,input,select{font:inherit;color:inherit}
.wrap{max-width:1100px;margin:0 auto;padding:20px 16px 60px}
.card{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:18px}
h1{font-size:1.35rem;margin:0}
h2{font-size:1.05rem;margin:0 0 12px}
.mu{color:var(--mu)}
.small{font-size:.82rem}
label{display:block;font-size:.8rem;font-weight:600;color:var(--mu);margin:0 0 4px}
input[type=text],input[type=email],input[type=password],input[type=search],select{width:100%;padding:9px 11px;border:1px solid var(--bd);border-radius:8px;background:var(--bg)}
input:focus,select:focus,button:focus-visible{outline:2px solid var(--ac);outline-offset:1px}
.btn{border:1px solid var(--bd);background:var(--card);border-radius:8px;padding:8px 14px;cursor:pointer;font-weight:600;white-space:nowrap}
.btn:hover{border-color:var(--ac)}
.btn.primary{background:var(--ac);border-color:var(--ac);color:var(--ac-tx)}
.btn.danger{color:var(--bad);border-color:var(--bad)}
.btn.link{border:0;background:none;color:var(--ac);padding:4px 6px}
.btn:disabled{opacity:.55;cursor:default}
.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.grow{flex:1;min-width:0}
.msg{padding:9px 12px;border-radius:8px;font-size:.87rem;margin-top:12px}
.msg.ok{background:var(--ok-bg);color:var(--ok)}
.msg.err{background:var(--bad-bg);color:var(--bad)}
.msg.warn{background:var(--warn-bg);color:var(--warn)}
#login-view{max-width:400px;margin:8vh auto 0}
#login-view .card>*+*{margin-top:12px}
header.top{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:18px}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--bd);margin-bottom:16px}
.tab{border:0;background:none;padding:9px 14px;cursor:pointer;font-weight:600;color:var(--mu);border-bottom:2px solid transparent;margin-bottom:-1px}
.tab[aria-selected=true]{color:var(--tx);border-bottom-color:var(--ac)}
.invite{display:grid;grid-template-columns:1fr 1fr auto;gap:10px;align-items:end}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:16px 0}
.stat{background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:10px 12px}
.stat b{display:block;font-size:1.3rem}
table{width:100%;border-collapse:collapse}
th,td{text-align:left;padding:9px 8px;border-bottom:1px solid var(--bd);vertical-align:middle}
th{font-size:.76rem;text-transform:uppercase;letter-spacing:.04em;color:var(--mu);font-weight:600}
tr.click{cursor:pointer}
tr.click:hover td{background:var(--bg)}
.badge{display:inline-block;padding:2px 8px;border-radius:99px;font-size:.75rem;font-weight:700}
.b-active{background:var(--ok-bg);color:var(--ok)}
.b-invited{background:var(--warn-bg);color:var(--warn)}
.b-blocked{background:var(--bad-bg);color:var(--bad)}
.bar{height:6px;border-radius:99px;background:var(--bar);overflow:hidden;min-width:60px}
.bar i{display:block;height:100%;background:var(--ac)}
.pct{font-size:.78rem;color:var(--mu);font-variant-numeric:tabular-nums}
.empty{text-align:center;padding:30px 10px;color:var(--mu)}
dialog{border:1px solid var(--bd);border-radius:14px;background:var(--card);color:var(--tx);padding:0;width:min(860px,96vw);max-height:92vh}
dialog::backdrop{background:rgba(0,0,0,.45)}
.dlg-head{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;padding:16px 18px;border-bottom:1px solid var(--bd);position:sticky;top:0;background:var(--card);z-index:1}
.dlg-body{padding:16px 18px}
.actions{display:flex;gap:8px;flex-wrap:wrap;margin:4px 0 18px}
details.trail{border:1px solid var(--bd);border-radius:10px;margin-bottom:10px}
details.trail>summary{padding:10px 12px;cursor:pointer;display:flex;gap:10px;align-items:center;font-weight:600}
.phase{padding:4px 12px 10px}
.phase h4{font-size:.82rem;color:var(--mu);margin:10px 0 4px}
.topic{display:flex;gap:10px;align-items:center;padding:4px 0;border-bottom:1px dashed var(--bd)}
.topic span{flex:1;font-size:.88rem}
.topic select{width:150px;padding:4px 6px;font-size:.82rem}
.topic.changed span{font-weight:700;color:var(--ac)}
.savebar{position:sticky;bottom:0;background:var(--card);border-top:1px solid var(--bd);padding:10px 18px;display:none;justify-content:space-between;align-items:center;gap:10px}
.savebar.on{display:flex}
@media (max-width:760px){
  .invite{grid-template-columns:1fr}
  .stats{grid-template-columns:repeat(2,1fr)}
  .hide-sm{display:none}
  th,td{padding:8px 4px}
  .topic select{width:120px}
}
</style>
<script>
try{var th=localStorage.getItem("roteiro-theme");if(th)document.documentElement.setAttribute("data-theme",th);}catch(e){}
</script>
</head>
<body>
<div class="wrap">

<section id="login-view" hidden>
  <div class="card">
    <h1>Painel do administrador</h1>
    <p class="mu small">Área restrita. Entre com a conta de administrador (é diferente da conta de aluno).</p>
    <form id="login-form">
      <div><label for="lg-email">E-mail</label><input type="email" id="lg-email" required autocomplete="username"></div>
      <div style="margin-top:10px"><label for="lg-pass">Senha</label><input type="password" id="lg-pass" required autocomplete="current-password"></div>
      <div id="lg-msg"></div>
      <button class="btn primary" type="submit" style="width:100%;margin-top:14px">Entrar</button>
    </form>
    <p class="small mu"><a href="index.html">← Voltar para o site</a></p>
  </div>
</section>

<section id="app-view" hidden>
  <header class="top">
    <div>
      <h1>Painel do administrador</h1>
      <div class="small mu">Conectado como <b id="who"></b> · sessão até <span id="exp"></span></div>
    </div>
    <div class="row">
      <button class="btn" id="btn-pass">Trocar minha senha</button>
      <button class="btn" id="btn-logout">Sair</button>
    </div>
  </header>

  <div class="tabs" role="tablist">
    <button class="tab" role="tab" aria-selected="true" data-tab="users">Alunos</button>
    <button class="tab" role="tab" aria-selected="false" data-tab="audit">Histórico</button>
  </div>

  <div id="tab-users">
    <div class="card">
      <h2>Convidar aluno</h2>
      <form id="invite-form" class="invite">
        <div><label for="inv-name">Nome</label><input type="text" id="inv-name" required maxlength="80" autocomplete="off"></div>
        <div><label for="inv-email">E-mail</label><input type="email" id="inv-email" required autocomplete="off"></div>
        <button class="btn primary" type="submit">Enviar convite</button>
      </form>
      <div id="inv-msg"></div>
    </div>

    <div class="stats" id="stats"></div>

    <div class="card">
      <div class="row" style="margin-bottom:10px">
        <h2 class="grow" style="margin:0">Alunos</h2>
        <input type="search" id="filter" placeholder="Buscar por nome ou e-mail" style="max-width:260px">
        <button class="btn" id="btn-reload">Atualizar</button>
      </div>
      <div style="overflow-x:auto">
        <table>
          <thead><tr><th>Aluno</th><th>Situação</th><th>IA</th><th>Matemática</th><th>Inglês</th><th class="hide-sm">Último acesso</th></tr></thead>
          <tbody id="users-body"></tbody>
        </table>
      </div>
    </div>
  </div>

  <div id="tab-audit" hidden>
    <div class="card">
      <div class="row" style="margin-bottom:10px"><h2 class="grow" style="margin:0">Histórico de ações</h2><button class="btn" id="btn-audit">Atualizar</button></div>
      <div style="overflow-x:auto">
        <table>
          <thead><tr><th>Quando</th><th>Ação</th><th>Aluno</th><th class="hide-sm">Detalhes</th></tr></thead>
          <tbody id="audit-body"></tbody>
        </table>
      </div>
    </div>
  </div>
</section>
</div>

<dialog id="dlg-user">
  <div class="dlg-head">
    <div><h2 id="du-name" style="margin:0"></h2><div class="small mu" id="du-sub"></div></div>
    <button class="btn link" data-close aria-label="Fechar">✕</button>
  </div>
  <div class="dlg-body">
    <div class="actions" id="du-actions"></div>
    <div id="du-msg"></div>
    <h2 style="margin-top:6px">Progresso</h2>
    <p class="small mu" style="margin-top:-6px">Altere a situação dos tópicos e clique em "Salvar alterações". Tudo fica registrado no histórico.</p>
    <div id="du-trails"></div>
  </div>
  <div class="savebar" id="du-savebar">
    <span class="small"><b id="du-count">0</b> alteração(ões) pendente(s)</span>
    <div class="row"><button class="btn" id="du-discard">Descartar</button><button class="btn primary" id="du-save">Salvar alterações</button></div>
  </div>
</dialog>

<dialog id="dlg-pass">
  <div class="dlg-head"><h2 style="margin:0">Trocar minha senha</h2><button class="btn link" data-close aria-label="Fechar">✕</button></div>
  <form class="dlg-body" id="pass-form">
    <div><label for="pw-cur">Senha atual</label><input type="password" id="pw-cur" required autocomplete="current-password"></div>
    <div style="margin-top:10px"><label for="pw-new">Nova senha (mínimo 8 caracteres)</label><input type="password" id="pw-new" required minlength="8" autocomplete="new-password"></div>
    <div style="margin-top:10px"><label for="pw-new2">Confirmar nova senha</label><input type="password" id="pw-new2" required minlength="8" autocomplete="new-password"></div>
    <div id="pw-msg"></div>
    <div class="row" style="justify-content:flex-end;margin-top:14px"><button class="btn primary" type="submit">Salvar</button></div>
  </form>
</dialog>

<script>
"use strict";
const TOPICS = __TOPICS__;
const TRAIL_NAMES = __TRAIL_NAMES__;
const TOTALS = Object.fromEntries(Object.entries(TOPICS).map(([k, ph]) => [k, ph.reduce((n, p) => n + p.items.length, 0)]));
const OFFICIAL_LAMBDA_URL = "https://x37p5anc5yesrwweqfbwxcexsu0dpzdu.lambda-url.us-east-2.on.aws/";
const SESSION_KEY = "roteiro_admin_session";
const STATUS_LABEL = { z: "Não iniciado", r: "Em andamento", e: "Concluído" };
const ACTION_LABEL = {
  bootstrap_admin: "Conta admin criada", bootstrap_reset_admin: "Senha do admin redefinida", invite: "Convite enviado",
  resend_invite: "Convite reenviado", set_status: "Situação alterada", delete_user: "Aluno excluído",
  force_reset: "Troca de senha forçada", edit_progress: "Progresso editado"
};

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const fmtDate = (sec) => sec ? new Date(Number(sec) * 1000).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" }) : "—";
let USERS = [];
let CURRENT = null;      // { user, progress }
let PENDING = {};        // tópico -> nova situação

function isLocalDev() { const h = location.hostname; return h === "localhost" || h === "127.0.0.1" || location.protocol === "file:"; }
function endpoint() {
  try {
    const ep = (JSON.parse(localStorage.getItem("roteiro_aws_config") || "{}") || {}).endpoint || "";
    if (/^https:\/\/[a-z0-9]+\.lambda-url\.[a-z0-9-]+\.on\.aws\/?$/.test(ep) || (isLocalDev() && /^http:\/\/(localhost|127\.0\.0\.1):\d+\/?$/.test(ep))) return ep;
  } catch (e) {}
  return OFFICIAL_LAMBDA_URL;
}

function getSession() {
  try {
    const s = JSON.parse(sessionStorage.getItem(SESSION_KEY) || "null");
    if (s && s.token && s.exp * 1000 > Date.now()) return s;
  } catch (e) {}
  sessionStorage.removeItem(SESSION_KEY);
  return null;
}

async function api(action, payload = {}, auth = true) {
  const body = Object.assign({}, payload, { action, aud: "admin" });
  if (auth) {
    const s = getSession();
    if (!s) { showLogin("Sua sessão expirou. Entre novamente."); throw new Error("Sessão expirada."); }
    body.token = s.token;
  }
  let res, json = null;
  try {
    res = await fetch(endpoint(), { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body), cache: "no-store" });
  } catch (e) { throw new Error("Sem conexão com o servidor."); }
  try { json = await res.json(); } catch (e) {}
  if (res.ok && json && json.ok) return json;
  if (auth && res.status === 401 && json && json.relogin) { sessionStorage.removeItem(SESSION_KEY); showLogin("Sua sessão expirou. Entre novamente."); }
  throw new Error((json && json.error) || `Erro no servidor (HTTP ${res.status}).`);
}

function msg(el, kind, text) { el.innerHTML = text ? `<div class="msg ${kind}">${esc(text)}</div>` : ""; }

function busy(btn, on) { if (btn) btn.disabled = on; }

// ---------------------------------------------------------------- login
function showLogin(text) {
  $("app-view").hidden = true;
  $("login-view").hidden = false;
  document.querySelectorAll("dialog[open]").forEach(d => d.close());
  msg($("lg-msg"), "warn", text || "");
  $("lg-pass").value = "";
}

function showApp() {
  const s = getSession();
  if (!s) return showLogin();
  $("login-view").hidden = true;
  $("app-view").hidden = false;
  $("who").textContent = s.name ? `${s.name} (${s.email})` : s.email;
  $("exp").textContent = new Date(s.exp * 1000).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
  loadUsers();
}

$("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = e.submitter;
  busy(btn, true);
  msg($("lg-msg"), "", "");
  try {
    const r = await api("login", { email: $("lg-email").value.trim().toLowerCase(), password: $("lg-pass").value }, false);
    sessionStorage.setItem(SESSION_KEY, JSON.stringify({ token: r.token, exp: r.expires_at, email: r.user.email, name: r.user.name }));
    $("lg-pass").value = "";
    showApp();
  } catch (err) {
    msg($("lg-msg"), "err", err.message);
  } finally { busy(btn, false); }
});

$("btn-logout").addEventListener("click", () => { sessionStorage.removeItem(SESSION_KEY); showLogin("Você saiu do painel."); });

// Encerra a tela quando a sessão vence, mesmo sem cliques.
setInterval(() => { if (!$("app-view").hidden && !getSession()) showLogin("Sua sessão expirou. Entre novamente."); }, 30000);

// ---------------------------------------------------------------- abas
document.querySelectorAll(".tab").forEach(t => t.addEventListener("click", () => {
  document.querySelectorAll(".tab").forEach(x => x.setAttribute("aria-selected", String(x === t)));
  $("tab-users").hidden = t.dataset.tab !== "users";
  $("tab-audit").hidden = t.dataset.tab !== "audit";
  if (t.dataset.tab === "audit") loadAudit();
}));

// ---------------------------------------------------------------- alunos
function statusBadge(u) {
  const map = { active: ["b-active", "Ativo"], invited: ["b-invited", "Convite pendente"], blocked: ["b-blocked", "Bloqueado"] };
  const [cls, label] = map[u.status] || ["", u.status];
  return `<span class="badge ${cls}">${label}</span>`;
}

function progressCell(u, trail) {
  const done = ((u.progress_summary || {})[trail] || {}).done || 0;
  const pct = TOTALS[trail] ? Math.round(done * 100 / TOTALS[trail]) : 0;
  return `<div class="bar" title="${done} de ${TOTALS[trail]} concluídos"><i style="width:${pct}%"></i></div><span class="pct">${done}/${TOTALS[trail]}</span>`;
}

function renderUsers() {
  const q = $("filter").value.trim().toLowerCase();
  const list = USERS.filter(u => !q || (u.name || "").toLowerCase().includes(q) || u.email.includes(q));
  $("users-body").innerHTML = list.length ? list.map(u => `
    <tr class="click" data-email="${esc(u.email)}" tabindex="0">
      <td><b>${esc(u.name || "—")}</b><div class="small mu">${esc(u.email)}</div></td>
      <td>${statusBadge(u)}</td>
      <td>${progressCell(u, "ia")}</td><td>${progressCell(u, "mat")}</td><td>${progressCell(u, "ing")}</td>
      <td class="hide-sm small">${fmtDate(u.last_login)}</td>
    </tr>`).join("") : `<tr><td colspan="6" class="empty">${USERS.length ? "Nenhum aluno encontrado." : "Nenhum aluno ainda. Use o formulário acima para convidar o primeiro."}</td></tr>`;
  const count = (st) => USERS.filter(u => u.status === st).length;
  const week = USERS.filter(u => u.last_login && Date.now() / 1000 - u.last_login < 7 * 86400).length;
  $("stats").innerHTML = [["Alunos", USERS.length], ["Ativos", count("active")], ["Convites pendentes", count("invited")], ["Entraram nos últimos 7 dias", week]]
    .map(([l, v]) => `<div class="stat"><span class="small mu">${l}</span><b>${v}</b></div>`).join("");
}

async function loadUsers() {
  try {
    USERS = (await api("admin_list_users")).users || [];
    renderUsers();
  } catch (err) {
    $("users-body").innerHTML = `<tr><td colspan="6" class="empty">${esc(err.message)}</td></tr>`;
  }
}

$("filter").addEventListener("input", renderUsers);
$("btn-reload").addEventListener("click", loadUsers);
$("users-body").addEventListener("click", (e) => { const tr = e.target.closest("tr[data-email]"); if (tr) openUser(tr.dataset.email); });
$("users-body").addEventListener("keydown", (e) => { const tr = e.target.closest("tr[data-email]"); if (tr && e.key === "Enter") openUser(tr.dataset.email); });

$("invite-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = e.submitter;
  busy(btn, true);
  try {
    const r = await api("admin_invite", { name: $("inv-name").value.trim(), email: $("inv-email").value.trim().toLowerCase() });
    let text = r.message;
    if (r.imported_legacy) text += " O progresso que já existia para esse e-mail foi importado.";
    msg($("inv-msg"), r.email_sent ? "ok" : "warn", text);
    $("invite-form").reset();
    loadUsers();
  } catch (err) {
    msg($("inv-msg"), "err", err.message);
  } finally { busy(btn, false); }
});

// ---------------------------------------------------------------- detalhe do aluno
async function openUser(email) {
  const dlg = $("dlg-user");
  $("du-name").textContent = "Carregando...";
  $("du-sub").textContent = "";
  $("du-actions").innerHTML = "";
  $("du-trails").innerHTML = "";
  msg($("du-msg"), "", "");
  PENDING = {};
  updateSavebar();
  if (!dlg.open) dlg.showModal();
  try {
    const r = await api("admin_get_user", { email });
    CURRENT = { user: r.user, progress: (r.data && r.data.progress) || {} };
    renderUser();
  } catch (err) {
    $("du-name").textContent = "Erro";
    msg($("du-msg"), "err", err.message);
  }
}

function renderUser() {
  const u = CURRENT.user;
  $("du-name").textContent = u.name || u.email;
  $("du-sub").innerHTML = `${esc(u.email)} · ${statusBadge(u)} · último acesso: ${fmtDate(u.last_login)} · última sincronização: ${u.last_sync ? new Date(Number(u.last_sync)).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" }) : "—"}`;
  const a = [];
  if (u.status === "invited") a.push(`<button class="btn" data-act="resend">Reenviar convite</button>`);
  if (u.status === "active") a.push(`<button class="btn" data-act="block">Bloquear</button>`, `<button class="btn" data-act="reset">Forçar troca de senha</button>`);
  if (u.status === "blocked") a.push(`<button class="btn" data-act="unblock">Desbloquear</button>`);
  a.push(`<button class="btn danger" data-act="delete">Excluir aluno</button>`);
  $("du-actions").innerHTML = a.join("");
  renderTrails();
}

function topicStatus(id) {
  if (id in PENDING) return PENDING[id];
  const v = CURRENT.progress[id];
  return v && (v.s === "e" || v.s === "r") ? v.s : "z";
}

function renderTrails() {
  const openNow = new Set([...document.querySelectorAll("details.trail[open]")].map(d => d.dataset.trail));
  $("du-trails").innerHTML = Object.entries(TOPICS).map(([tr, phases]) => {
    const ids = phases.flatMap(p => p.items.map(i => i[0]));
    const done = ids.filter(id => topicStatus(id) === "e").length;
    const started = ids.filter(id => topicStatus(id) === "r").length;
    const body = phases.map(p => `<div class="phase"><h4>${esc(p.t)}</h4>${p.items.map(([id, title]) => {
      const s = topicStatus(id);
      const opts = ["z", "r", "e"].map(v => `<option value="${v}"${v === s ? " selected" : ""}>${STATUS_LABEL[v]}</option>`).join("");
      return `<div class="topic${id in PENDING ? " changed" : ""}"><span>${esc(title)}</span><select data-topic="${id}" aria-label="Situação de ${esc(title)}">${opts}</select></div>`;
    }).join("")}</div>`).join("");
    return `<details class="trail" data-trail="${tr}"${openNow.has(tr) ? " open" : ""}>
      <summary><span class="grow">${esc(TRAIL_NAMES[tr])}</span><span class="pct">${done}/${ids.length} concluídos · ${started} em andamento</span></summary>
      <div class="phase"><button class="btn danger" data-reset-trail="${tr}">Zerar ${esc(TRAIL_NAMES[tr])}</button></div>${body}</details>`;
  }).join("");
}

function updateSavebar() {
  const n = Object.keys(PENDING).length;
  $("du-count").textContent = n;
  $("du-savebar").classList.toggle("on", n > 0);
}

$("du-trails").addEventListener("change", (e) => {
  const sel = e.target.closest("select[data-topic]");
  if (!sel) return;
  const id = sel.dataset.topic;
  const v = CURRENT.progress[id];
  const orig = v && (v.s === "e" || v.s === "r") ? v.s : "z";
  if (sel.value === orig) delete PENDING[id]; else PENDING[id] = sel.value;
  sel.closest(".topic").classList.toggle("changed", id in PENDING);
  updateSavebar();
});

$("du-discard").addEventListener("click", () => { PENDING = {}; updateSavebar(); renderTrails(); });

$("du-save").addEventListener("click", async (e) => {
  const btn = e.currentTarget;
  busy(btn, true);
  try {
    await api("admin_edit_progress", { email: CURRENT.user.email, op: "set_topics", changes: PENDING });
    const n = Object.keys(PENDING).length;
    await openUser(CURRENT.user.email);
    msg($("du-msg"), "ok", `${n} tópico(s) atualizado(s). O aluno vê a mudança na próxima vez que abrir o site.`);
    loadUsers();
  } catch (err) {
    msg($("du-msg"), "err", err.message);
  } finally { busy(btn, false); }
});

$("du-trails").addEventListener("click", async (e) => {
  const b = e.target.closest("[data-reset-trail]");
  if (!b) return;
  const tr = b.dataset.resetTrail;
  if (!confirm(`Zerar todo o progresso de ${TRAIL_NAMES[tr]} de ${CURRENT.user.name || CURRENT.user.email}? Isso não pode ser desfeito.`)) return;
  busy(b, true);
  try {
    await api("admin_edit_progress", { email: CURRENT.user.email, op: "reset_trail", trail: tr });
    await openUser(CURRENT.user.email);
    msg($("du-msg"), "ok", `Progresso de ${TRAIL_NAMES[tr]} zerado.`);
    loadUsers();
  } catch (err) {
    msg($("du-msg"), "err", err.message);
    busy(b, false);
  }
});

$("du-actions").addEventListener("click", async (e) => {
  const b = e.target.closest("[data-act]");
  if (!b) return;
  const u = CURRENT.user, act = b.dataset.act;
  const who = u.name || u.email;
  let call, ok;
  if (act === "resend") { call = ["admin_resend_invite", {}]; ok = "Convite reenviado."; }
  if (act === "block") {
    if (!confirm(`Bloquear ${who}? A pessoa sai na hora de todos os aparelhos e não consegue entrar até ser desbloqueada.`)) return;
    call = ["admin_set_status", { status: "blocked" }]; ok = "Aluno bloqueado.";
  }
  if (act === "unblock") { call = ["admin_set_status", { status: "active" }]; ok = "Aluno desbloqueado."; }
  if (act === "reset") {
    if (!confirm(`Forçar ${who} a criar uma senha nova? A senha atual deixa de valer e a pessoa recebe um código por e-mail.`)) return;
    call = ["admin_force_reset", {}]; ok = "Senha anulada e código enviado.";
  }
  if (act === "delete") {
    const typed = prompt(`Excluir ${who} apaga a conta e TODO o progresso, sem volta.\n\nPara confirmar, digite o e-mail do aluno:`);
    if (typed === null) return;
    call = ["admin_delete_user", { confirm: typed.trim().toLowerCase() }]; ok = "Aluno excluído.";
  }
  busy(b, true);
  try {
    const r = await api(call[0], Object.assign({ email: u.email }, call[1]));
    if (act === "delete") { $("dlg-user").close(); msg($("inv-msg"), "ok", `${who}: ${ok}`); }
    else {
      await openUser(u.email);
      const warn = r.email_sent === false;
      msg($("du-msg"), warn ? "warn" : "ok", warn ? "Feito, mas o e-mail não foi enviado. Confira o Amazon SES." : ok);
    }
    loadUsers();
  } catch (err) {
    msg($("du-msg"), "err", err.message);
    busy(b, false);
  }
});

const confirmDiscard = () => !Object.keys(PENDING).length || confirm("Descartar as alterações de progresso que não foram salvas?");
document.querySelectorAll("dialog [data-close]").forEach(b => b.addEventListener("click", () => {
  const d = b.closest("dialog");
  if (d.id !== "dlg-user" || confirmDiscard()) d.close();
}));
$("dlg-user").addEventListener("cancel", (e) => { if (!confirmDiscard()) e.preventDefault(); });

// ---------------------------------------------------------------- histórico
function auditDetails(e) {
  const d = e.details || {};
  if (e.action === "set_status") return d.status === "blocked" ? "Bloqueado" : "Desbloqueado";
  if (e.action === "edit_progress") {
    if (d.op === "reset_trail") return `Zerou ${TRAIL_NAMES[d.trail] || d.trail} (${d.removed || 0} tópicos)`;
    return Object.entries(d.changes || {}).map(([id, s]) => `${id}: ${STATUS_LABEL[s] || s}`).join(", ");
  }
  if (e.action === "invite") return [d.name, d.imported_legacy ? "progresso antigo importado" : "", d.email_sent === false ? "e-mail não enviado" : ""].filter(Boolean).join(" · ");
  if (e.action === "force_reset") return d.email_sent === false ? "e-mail não enviado" : "código enviado";
  return "";
}

async function loadAudit() {
  $("audit-body").innerHTML = `<tr><td colspan="4" class="empty">Carregando...</td></tr>`;
  try {
    const rows = (await api("admin_audit", { limit: 200 })).entries || [];
    $("audit-body").innerHTML = rows.length ? rows.map(e => `<tr>
      <td class="small">${fmtDate(e.at)}</td><td>${esc(ACTION_LABEL[e.action] || e.action)}</td>
      <td class="small">${esc(e.target || "")}</td><td class="hide-sm small mu">${esc(auditDetails(e))}</td></tr>`).join("")
      : `<tr><td colspan="4" class="empty">Nenhuma ação registrada.</td></tr>`;
  } catch (err) {
    $("audit-body").innerHTML = `<tr><td colspan="4" class="empty">${esc(err.message)}</td></tr>`;
  }
}
$("btn-audit").addEventListener("click", loadAudit);

// ---------------------------------------------------------------- minha senha
$("btn-pass").addEventListener("click", () => { $("pass-form").reset(); msg($("pw-msg"), "", ""); $("dlg-pass").showModal(); });
$("pass-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  if ($("pw-new").value !== $("pw-new2").value) return msg($("pw-msg"), "err", "A confirmação não confere.");
  const btn = e.submitter;
  busy(btn, true);
  try {
    const r = await api("change_password", { current: $("pw-cur").value, new: $("pw-new").value });
    const s = getSession();
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(Object.assign(s, { token: r.token, exp: r.expires_at })));
    $("dlg-pass").close();
    showApp();
  } catch (err) {
    msg($("pw-msg"), "err", err.message);
  } finally { busy(btn, false); }
});

if (getSession()) showApp(); else showLogin();
</script>
</body>
</html>
"""


def generate_admin_page(out_path, tracks):
    topics = json.dumps(build_topics(tracks), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = (ADMIN_HTML
            .replace("__FAVICON__", FAVICON_LINK)
            .replace("__TOPICS__", topics)
            .replace("__TRAIL_NAMES__", json.dumps(TRAIL_NAMES, ensure_ascii=False)))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Gerado: {out_path} (Painel do administrador)")
