# -*- coding: utf-8 -*-
"""Novo cockpit do Hub: 'A Jornada'. Substitui tacômetro/anéis/patentes por indicadores baseados em esforço real."""
from metrics_js import METRICS_JS

JOURNEY_CSS = r"""
.jr-sect{background:var(--card);border:1px solid var(--bd);border-radius:22px;padding:24px 26px;margin-bottom:36px;box-shadow:0 14px 40px rgba(6,20,27,.4)}
.jr-toolbar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;margin:14px 0}
.jr-grid{display:grid;grid-template-columns:1.6fr 1fr;gap:16px;margin-bottom:16px}
.jr-grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
@media(max-width:980px){.jr-grid{grid-template-columns:1fr}}
.jr-col{display:flex;flex-direction:column;gap:16px}
.jr-card{background:var(--bg);border:1px solid var(--bd);border-radius:16px;padding:16px 18px}
.jr-h{font-size:.74rem;font-weight:800;text-transform:uppercase;letter-spacing:.05em;color:var(--mu);margin:0 0 10px;display:flex;justify-content:space-between;gap:8px;align-items:center}
.jr-big{font-size:1.5rem;font-weight:850;color:var(--tx);line-height:1.15}
.jr-sub{font-size:.78rem;color:var(--mu);line-height:1.45;margin-top:4px}
.jr-bar{height:9px;background:var(--bd);border-radius:99px;overflow:hidden;position:relative}
.jr-bar>i{display:block;height:100%;border-radius:99px;transition:width .4s}
.jr-bar>i.s{background:#253745;position:absolute;left:0;top:0}
.jr-bar>i.w{background:linear-gradient(90deg,#4A5C6A,#9BA8AB);position:absolute;left:0;top:0}
.jr-row{display:flex;justify-content:space-between;gap:8px;font-size:.78rem;font-weight:700;color:var(--tx);margin:10px 0 4px}
.jr-svg{width:100%;height:auto;display:block}
.jr-leg{display:flex;flex-wrap:wrap;gap:12px;font-size:.72rem;font-weight:700;color:var(--mu);margin-top:6px}
.jr-chip{font-size:.7rem;font-weight:800;padding:2px 9px;border-radius:99px;border:1px solid var(--bd);background:var(--card);color:var(--mu)}
.jr-list{margin:0;padding:0;list-style:none;font-size:.8rem;display:flex;flex-direction:column;gap:6px}
.jr-list li{display:flex;justify-content:space-between;gap:8px;color:var(--tx)}
.jr-list li span:last-child{color:var(--mu);font-weight:700}
.speed-diagnosis-card.pace-attn{background:rgba(232,161,0,.12);border:1px solid rgba(232,161,0,.4);color:#b77f00}
.speed-diagnosis-card.pace-late{background:rgba(234,88,12,.1);border:1px solid rgba(234,88,12,.35);color:#c2410c}
.speed-diagnosis-card.pace-nodata{background:var(--bg);border:1px solid var(--bd);color:var(--mu)}
#jr-banner-text{flex:1 1 260px!important;min-width:0}
#jr-banner-text b{font-weight:750}
#jr-banner-text>b:first-child{display:block;font-size:.95rem}
.jr-banner-sub{display:block;margin-top:4px;font-size:.84rem;font-weight:500;line-height:1.55;color:var(--tx)}
.jr-banner-sub+.jr-banner-sub{margin-top:6px;font-size:.76rem;color:var(--mu)}
"""

JOURNEY_HTML = r"""<section class="jr-sect" id="hub-tracker-sect">
    <div class="speed-head" style="margin-bottom:0">
      <div class="speed-title-wrap">
        <div class="speed-title-icon" id="global-icon">🧭</div>
        <div>
          <div class="speed-title">A Jornada <span class="nav-status-pill" id="global-badge">Do primeiro tópico ao último projeto</span></div>
          <div class="speed-subtitle">Quanto você já avançou, em que ritmo e quando deve chegar à meta.</div>
        </div>
      </div>
      <div class="speed-presets-wrap">
        <span style="font-size:.74rem;font-weight:800;color:var(--mu);padding:0 6px">Meta:</span>
        <button class="speed-preset-btn" id="btn-pace-none" onclick="setHubPace('none')">Sem meta</button>
        <button class="speed-preset-btn" id="btn-pace-sprint" onclick="setHubPace('sprint')">⚡ 4 meses</button>
        <button class="speed-preset-btn active" id="btn-pace-optimistic" onclick="setHubPace('optimistic')">🚀 6 meses</button>
        <button class="speed-preset-btn" id="btn-pace-standard" onclick="setHubPace('standard')">🎯 14 meses</button>
      </div>
    </div>

    <div class="jr-toolbar">
      <div class="speed-date-inputs">
        <label for="hub-start-date">📅 Início:</label>
        <input type="date" id="hub-start-date" class="speed-date-input" onchange="onStartDateChange(this.value)">
        <button class="speed-reset-btn" onclick="resetStartDateToday()">Hoje</button>
      </div>
    </div>

    <div class="speed-diagnosis-card pace-nodata" id="jr-banner">
      <div id="jr-banner-text" style="flex:1">Carregando seus dados…</div>
      <span class="speed-diag-badge" id="jr-banner-badge">…</span>
    </div>

    <div class="jr-grid">
      <div class="jr-card">
        <div class="jr-h"><span>📈 Sua evolução acumulada</span><span class="jr-chip" id="jr-chart-chip">esforço (pontos)</span></div>
        <div id="jr-chart"></div>
        <div class="jr-leg">
          <span style="color:#9BA8AB">┄ Plano da meta</span><span style="color:#10b981">━ Realizado</span>
          <span style="color:#CCD0CF">▨ Faixa de previsão</span><span>· trecho claro = antes do início do registro</span>
        </div>
      </div>
      <div class="jr-col">
        <div class="jr-card">
          <div class="jr-h"><span>🎯 Progresso</span></div>
          <div class="jr-row"><span>Considerando a dificuldade</span><span id="jr-wpct">0%</span></div>
          <div class="jr-bar"><i class="w" id="jr-wbar" style="width:0%"></i></div>
          <div class="jr-row"><span>Tópicos concluídos</span><span id="jr-spct">0%</span></div>
          <div class="jr-bar"><i class="s" id="jr-sbar" style="width:0%"></i></div>
          <div class="jr-sub" id="jr-explain"></div>
        </div>
        <div class="jr-card">
          <div class="jr-h"><span>🏁 Previsão de conclusão</span><span class="jr-chip" id="jr-conf">–</span></div>
          <div class="jr-big" id="jr-fc-main">–</div>
          <div class="jr-sub" id="jr-fc-sub"></div>
        </div>
      </div>
    </div>

    <div class="jr-grid3">
      <div class="jr-card">
        <div class="jr-h"><span>⚡ Ritmo e tempo</span></div>
        <div class="jr-big" id="jr-pace">–</div>
        <div class="jr-sub" id="jr-pace-sub"></div>
        <div class="jr-sub" id="jr-time" style="margin-top:8px"></div>
      </div>
      <div class="jr-card">
        <div class="jr-h"><span>🗺️ Onde está o esforço</span></div>
        <div id="jr-tracks"></div>
      </div>
      <div class="jr-card">
        <div class="jr-h"><span>👉 Próximo passo</span></div>
        <div class="jr-big" style="font-size:1rem" id="hub-next-step-title">–</div>
        <a href="ia.html" id="hub-next-step-btn" class="hub-next-action-btn" style="margin-top:10px">Continuar ➔</a>
        <div class="jr-sub" id="jr-next-ms" style="margin-top:10px"></div>
      </div>
      <div class="jr-card">
        <div class="jr-h"><span>🧪 E se eu acelerar?</span></div>
        <div style="display:flex;justify-content:space-between;font-size:.8rem;font-weight:800"><span style="color:var(--mu)">Ritmo</span><span id="whatif-lbl" style="color:#06b6d4">+25%</span></div>
        <input type="range" id="hub-whatif-slider" min="0" max="100" step="5" value="25" oninput="updateWhatIf()" style="width:100%;accent-color:#06b6d4">
        <div class="jr-big" style="font-size:1.05rem" id="whatif-res">–</div>
        <div class="jr-sub" id="whatif-sub"></div>
      </div>
      <div class="jr-card">
        <div class="jr-h"><span>🏅 Marcos reais</span></div>
        <ul class="jr-list" id="jr-ms"></ul>
      </div>
    </div>
  </section>"""

JOURNEY_JS_A = METRICS_JS + r"""
RM.configure(__RM_CONFIG__);   // totais só com os tópicos obrigatórios (opcionais ficam fora da meta)
HUB_PRESETS.none = { name: "Sem meta", days: null, label: "Sem data-alvo definida" };
const EVENTS_KEY = "roteiro-events-v1", SESS_KEY = "roteiro-sessions-v1",
      LOGSTART_KEY = "roteiro-log-start", EFFORT_KEY = "roteiro-effort-v1";
const jrEl = id => document.getElementById(id);
const jrSet = (id, h) => { const e = jrEl(id); if (e) e.innerHTML = h; };
const jrRead = (k, d) => { try { const r = localStorage.getItem(k); return r ? JSON.parse(r) : d; } catch (e) { return d; } };
const jrF = n => (Math.round(n * 10) / 10).toLocaleString("pt-BR");
const jrPct = n => (Math.round(n * 10) / 10).toLocaleString("pt-BR") + "%";
window.__jr = { remaining: 0, fc: null, hpp: null, now: Date.now() };

function formatDateBR(d) {
  if (!d || isNaN(d.getTime())) return "--/--/----";
  return String(d.getDate()).padStart(2, "0") + "/" + String(d.getMonth() + 1).padStart(2, "0") + "/" + d.getFullYear();
}
function triggerPulse() {
  const c = jrEl("hub-tracker-sect"); if (!c) return;
  c.classList.remove("pulse-update"); void c.offsetWidth; c.classList.add("pulse-update");
  setTimeout(() => c.classList.remove("pulse-update"), 700);
}
function loadPaceSettings() {
  try {
    const sp = localStorage.getItem(PACE_KEY);
    if (sp && HUB_PRESETS[sp]) currentPace = sp;
    const ss = localStorage.getItem(START_KEY);
    if (ss && /^\d{4}-\d{2}-\d{2}$/.test(ss)) currentStartDate = ss;
    else { currentStartDate = new Date().toISOString().slice(0, 10); localStorage.setItem(START_KEY, currentStartDate); }
  } catch (e) { currentPace = "optimistic"; currentStartDate = new Date().toISOString().slice(0, 10); }
}
function setHubPace(k) {
  if (!HUB_PRESETS[k]) return;
  currentPace = k; try { localStorage.setItem(PACE_KEY, k); } catch (e) {}
  triggerPulse(); calcAndPaint();
}
function onStartDateChange(v) { if (!v) return; currentStartDate = v; try { localStorage.setItem(START_KEY, v); } catch (e) {} triggerPulse(); calcAndPaint(); }
function resetStartDateToday() { onStartDateChange(new Date().toISOString().slice(0, 10)); const i = jrEl("hub-start-date"); if (i) i.value = currentStartDate; }
// Pesos de esforço de cada trilha: vêm de TRACK_WEIGHTS (metrics_js.py, com a calibração explicada lá),
// os mesmos que o aviso de pontos de cada aula usa.
// Não há UI para alterar: valores antigos salvos no navegador (EFFORT_KEY.tracks) são ignorados.
const JR_TRACK_WEIGHTS = RM.TRACK_WEIGHTS;
function updateWhatIf() {
  const sl = jrEl("hub-whatif-slider"); if (!sl) return;
  const boost = parseInt(sl.value, 10) || 0, { remaining, fc, hpp } = window.__jr, now = window.__jr.now;
  jrSet("whatif-lbl", "+" + boost + "%");
  if (!fc || (fc.level !== "ok" && fc.level !== "preliminary") || !fc.dMed) {
    jrSet("whatif-res", "Disponível após 2 semanas de registro");
    jrSet("whatif-sub", "A simulação usa o seu ritmo das últimas semanas. Continue estudando e ela fica disponível.");
    return;
  }
  const newPace = fc.med * (1 + boost / 100), nd = Math.ceil(remaining / (newPace / 7)), saved = fc.dMed - nd;
  jrSet("whatif-res", formatDateBR(new Date(now + nd * 86400000)));
  let sub = boost === 0 ? "Mantendo o ritmo mediano atual." : "Antecipa ~" + saved + " dia(s) vs. ritmo atual.";
  if (hpp && boost > 0) sub += " Equivale a ~" + Math.round(fc.med * boost / 100 * hpp * 60 / 7) + " min/dia a mais (seu tempo médio por ponto).";
  else if (boost > 0) sub += " Registre suas sessões para ver isso em minutos por dia.";
  jrSet("whatif-sub", sub);
}
"""

JOURNEY_JS_B = r"""
function drawJourney(o) {
  const W = 640, H = 230, L = 46, R = 14, T = 14, B = 30, iw = W - L - R, ih = H - T - B, DAY = 86400000;
  const X = t => L + (t - o.start) / (o.end - o.start) * iw;
  const Y = v => T + ih - Math.min(v, o.total) / o.total * ih;
  let s = '<svg viewBox="0 0 ' + W + " " + H + '" class="jr-svg" role="img" aria-label="Evolução acumulada do esforço">';
  [0, 0.5, 1].forEach(f => {
    s += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + Y(o.total * f) + '" y2="' + Y(o.total * f) + '" stroke="var(--bd)" stroke-dasharray="3 3"/>';
    s += '<text x="4" y="' + (Y(o.total * f) + 4) + '" fill="var(--mu)" font-size="10" font-weight="700">' + Math.round(o.total * f) + "</text>";
  });
  if (o.deadline) s += '<line x1="' + X(o.start) + '" y1="' + Y(0) + '" x2="' + X(o.deadline) + '" y2="' + Y(o.total) + '" stroke="#9BA8AB" stroke-width="2" stroke-dasharray="5 4" stroke-opacity=".7"/>';
  const fc = o.fc;
  if (fc && (fc.level === "ok" || fc.level === "preliminary") && fc.med > 0) {
    const dd = (o.end - o.now) / DAY, yv = p => o.pts + p / 7 * dd;
    s += '<polygon points="' + X(o.now) + "," + Y(o.pts) + " " + X(o.end) + "," + Y(yv(fc.fast)) + " " + X(o.end) + "," + Y(yv(fc.slow)) + '" fill="#4A5C6A" fill-opacity=".22"/>';
    s += '<line x1="' + X(o.now) + '" y1="' + Y(o.pts) + '" x2="' + X(o.end) + '" y2="' + Y(yv(fc.med)) + '" stroke="#CCD0CF" stroke-width="2" stroke-dasharray="5 4"/>';
  }
  const cv = o.curve;
  if (cv.length) {
    if (cv[0].t > o.start) s += '<line x1="' + X(o.start) + '" y1="' + Y(0) + '" x2="' + X(cv[0].t) + '" y2="' + Y(cv[0].v) + '" stroke="#10b981" stroke-opacity=".35" stroke-width="3"/>';
    s += '<polyline fill="none" stroke="#10b981" stroke-width="3.5" stroke-linejoin="round" points="' + cv.map(p => X(p.t) + "," + Y(p.v)).join(" ") + '"/>';
  }
  s += '<circle cx="' + X(o.now) + '" cy="' + Y(o.pts) + '" r="5.5" fill="#10b981" stroke="var(--card)" stroke-width="2"/>';
  s += '<text x="' + L + '" y="' + (H - 8) + '" fill="var(--mu)" font-size="10" font-weight="700">' + formatDateBR(new Date(o.start)) + "</text>";
  s += '<text x="' + (W - R) + '" y="' + (H - 8) + '" text-anchor="end" fill="var(--mu)" font-size="10" font-weight="700">' + formatDateBR(new Date(o.end)) + "</text></svg>";
  return s;
}

function calcAndPaint() {
  const DAY = 86400000, now = Date.now();
  const raw = jrRead(EFFORT_KEY, {});
  const eff = { tracks: Object.assign({}, JR_TRACK_WEIGHTS), topics: raw.topics || {} };
  const ev = jrRead(EVENTS_KEY, []), ses = jrRead(SESS_KEY, []);
  const logStart = parseInt(localStorage.getItem(LOGSTART_KEY) || "", 10) || null;

  // o treino aprovado de cada aula também soma (parte dos pontos das aulas com treino, ver RM.credit)
  const P = RM.progress(PR, eff, RM.trBest(jrRead("roteiro-answers-v1", {}))), T = RM.totals(eff);
  const sPct = P.structDone / T.topics * 100, wPct = P.pts / T.points * 100, remaining = Math.max(0, T.points - P.pts);

  // cards das trilhas (mantém os 4 cards grandes do hub)
  let projDone = 0; const totalProj = 6;
  try { const pl = JSON.parse(localStorage.getItem("roteiro_portfolio_projects") || "[]"); projDone = pl.filter(x => x.status === "done").length; } catch (e) {}
  const trackUI = { ia: "ia", mat: "mat", ing: "ing" };
  for (const t in trackUI) {
    const p = P.per[t], pc = Math.round(p.done / p.total * 100);
    jrSet("card-" + t + "-pct", pc + "% (" + p.done + "/" + p.total + ")");
    const f = jrEl("card-" + t + "-fill"); if (f) f.style.width = pc + "%";
  }
  jrSet("card-proj-pct", Math.round(projDone / totalProj * 100) + "% (" + projDone + "/" + totalProj + ")");
  const pf = jrEl("card-proj-fill"); if (pf) pf.style.width = Math.round(projDone / totalProj * 100) + "%";

  // meta e plano
  const preset = HUB_PRESETS[currentPace] || HUB_PRESETS.optimistic;
  const start = new Date(currentStartDate + "T00:00:00").getTime();
  const elapsed = Math.max(0, Math.floor((now - start) / DAY));
  const deadline = preset.days ? start + preset.days * DAY : null;
  const planned = RM.planned(T.points, start, deadline, now);
  const st = RM.status(P.pts, planned, T.points, elapsed);
  const series = RM.weeklySeries(ev, now, logStart, eff);
  const fc = RM.forecast(remaining, series);
  const req = deadline ? RM.requiredPace(remaining, now, deadline) : null;
  const curPace = series.length ? series.slice(0, 4).reduce((a, b) => a + b, 0) / Math.min(4, series.length) : null;
  const hpp = RM.hoursPerPoint(ses, ev, eff, logStart);
  window.__jr = { remaining, fc, hpp, now };

  const sInput = jrEl("hub-start-date"); if (sInput && !sInput.value) sInput.value = currentStartDate;
  document.querySelectorAll(".speed-preset-btn").forEach(b => b.classList.remove("active"));
  const cb = jrEl("btn-pace-" + currentPace); if (cb) cb.classList.add("active");

  // faixa de situação (5 estados)
  const B = { ahead: ["pace-ahead", "🟢 ADIANTADO"], ontrack: ["pace-ontrack", "🔵 NO RITMO"], attention: ["pace-attn", "🟡 ATENÇÃO"],
              late: ["pace-late", "🟠 ABAIXO DA META"], nodata: ["pace-nodata", "⚪ SEM DADOS SUFICIENTES"], neutral: ["pace-nodata", "⚪ SEM META DEFINIDA"] }[st.k];
  // Texto em duas partes: a frase principal (em destaque) e a explicação com os números, em linguagem simples.
  // "Pontos" = esforço: cada aula vale conforme a dificuldade (JR_TRACK_WEIGHTS, de metrics_js.TRACK_WEIGHTS).
  let msg;
  const perDay = deadline ? T.points / ((deadline - start) / DAY) : 0;
  const n0 = x => Math.round(x).toLocaleString("pt-BR");
  const plural = (n, um, varios) => n + " " + (n === 1 ? um : varios);
  const metaNome = "meta de " + preset.months + " meses";
  const fim = deadline ? formatDateBR(new Date(deadline)) : "";
  const PONTOS = '<span class="jr-banner-sub">Os pontos medem o esforço: cada aula vale conforme a dificuldade (Inglês ' +
    JR_TRACK_WEIGHTS.ing + ", IA " + JR_TRACK_WEIGHTS.ia + ", Matemática " + JR_TRACK_WEIGHTS.mat + "). Nas aulas com treino, " +
    Math.round(RM.TR_SHARE * 100) + "% dos pontos vêm dele, com pelo menos " + RM.TR_MIN + "% de acertos.</span>";
  const ritmoHoje = curPace != null
    ? "Nas últimas " + plural(Math.min(4, series.length), "semana", "semanas") + ", você fez em média <b>" + jrF(curPace) + " pontos por semana</b>. "
    : "";
  // Ritmo necessário traduzido em aulas: é o que dá para planejar na semana
  const emAulas = r => " (por exemplo, " + plural(Math.ceil(r / JR_TRACK_WEIGHTS.ia), "aula", "aulas") + " de IA ou " +
    plural(Math.ceil(r / JR_TRACK_WEIGHTS.mat), "aula", "aulas") + " de Matemática por semana)";
  if (st.k === "neutral") msg = "<b>Você está sem meta de prazo.</b>" +
    '<span class="jr-banner-sub">O painel mostra seu ritmo, mas não compara com um plano. Se quiser uma data para mirar, escolha 4, 6 ou 14 meses acima.</span>';
  else if (st.k === "nodata") msg = "<b>" + (elapsed === 0 ? "Hoje começa a sua jornada." : "Você está no dia " + elapsed + " da jornada.") + "</b>" +
    '<span class="jr-banner-sub">A comparação com o plano começa no 7º dia. Antes disso, uns poucos dias bons ou ruins mudariam muito o resultado.</span>';
  else {
    const d = Math.abs(st.delta), dd = perDay ? Math.max(1, Math.round(d / perDay)) : 0;
    const pelo = "Pela " + metaNome + ", hoje você já deveria ter uns <b>" + n0(planned) + " pontos</b>, e você tem <b>" + jrF(P.pts) + "</b>. ";
    if (st.k === "ahead") msg = "<b>Você está uns " + plural(dd, "dia", "dias") + " adiantado em relação à " + metaNome + ". 🎉</b>" +
      '<span class="jr-banner-sub">' + pelo + ritmoHoje + "A meta termina em " + fim + ". Continue assim!</span>" + PONTOS;
    else if (st.k === "ontrack") msg = "<b>Você está no ritmo da " + metaNome + ".</b>" +
      '<span class="jr-banner-sub">' + pelo +
      (st.delta < 0 ? "A diferença de " + n0(d) + " pontos ainda está dentro da folga do plano (até " + n0(0.05 * T.points) + " pontos, 5% do total). "
                    : d >= 1 ? "Você está " + n0(d) + " pontos à frente. " : "") +
      ritmoHoje + "A meta termina em " + fim + ".</span>" + PONTOS;
    else msg = "<b>Você está uns " + plural(dd, "dia", "dias") + " atrasado em relação à " + metaNome + ".</b>" +
      '<span class="jr-banner-sub">' + pelo + "Faltam " + n0(d) + " pontos para alcançar o plano. " + ritmoHoje +
      (req ? "Para terminar tudo até " + fim + ", o ritmo precisa subir para uns <b>" + n0(req) + " pontos por semana</b>" + emAulas(req) + "." : "") +
      "</span>" + PONTOS;
  }
  const bn = jrEl("jr-banner"); if (bn) bn.className = "speed-diagnosis-card " + B[0];
  jrSet("jr-banner-text", msg); jrSet("jr-banner-badge", B[1]);

  // progresso
  jrSet("jr-wpct", jrPct(wPct)); jrSet("jr-spct", jrPct(sPct));
  jrEl("jr-wbar").style.width = wPct + "%"; jrEl("jr-sbar").style.width = sPct + "%";
  jrSet("jr-explain", "Você concluiu " + P.structDone + " de " + T.topics + " tópicos. Considerando a dificuldade de cada trilha (um tópico de Matemática exige mais estudo que uma aula de Inglês), já percorreu " + jrF(P.pts) + " de " + jrF(T.points) + " pontos, contando o que está em andamento e os treinos.");

  // previsão
  const fmt = d => formatDateBR(new Date(now + d * DAY));
  jrSet("jr-conf", fc.level === "ok" || fc.level === "preliminary" ? "confiança " + fc.conf : fc.level === "done" ? "concluído" : "preliminar");
  if (fc.level === "done") { jrSet("jr-fc-main", "Roteiro concluído 🎓"); jrSet("jr-fc-sub", ""); }
  else if (fc.level === "insufficient") {
    jrSet("jr-fc-main", "Ainda sem data");
    jrSet("jr-fc-sub", "A previsão aparece depois de " + fc.need + " semanas completas de estudo registradas (até agora: " + fc.n + ")." +
      (logStart ? " Registro iniciado em " + formatDateBR(new Date(logStart)) + "." : " O registro começa quando você marcar o próximo tópico.") +
      (req ? " Para a meta, o ritmo necessário é ~" + jrF(req) + " pontos/semana." : ""));
  } else if (!fc.dMed) { jrSet("jr-fc-main", "Sem ritmo recente"); jrSet("jr-fc-sub", "Nas últimas semanas não houve conclusões, então não há projeção."); }
  else {
    jrSet("jr-fc-main", fmt(fc.dMed));
    jrSet("jr-fc-sub", "Faixa: " + (fc.dFast ? fmt(fc.dFast) : "–") + " a " + (fc.dSlow ? fmt(fc.dSlow) : "mais de 4 anos") + " (otimista a conservador)." +
      (fc.level === "preliminary" ? " Prévia: baseada em " + fc.n + " semanas; estreita com mais histórico." : " Baseada em " + fc.n + " semanas de registro.") +
      (deadline ? (fc.dMed * DAY + now <= deadline ? " Provável antes da meta." : " Provável depois da meta.") : ""));
  }

  // ritmo e tempo
  jrSet("jr-pace", curPace != null ? jrF(curPace) + " pts/sem" : "–");
  let ps = series.length ? "Média das últimas " + Math.min(4, series.length) + " semanas completas." : "Ainda sem semana completa de registro.";
  if (series.length >= 8) { const a = series.slice(0, 4).reduce((x, y) => x + y, 0), b = series.slice(4, 8).reduce((x, y) => x + y, 0); ps += b > 0 ? " Vs. 4 semanas anteriores: " + (a >= b ? "+" : "") + Math.round((a - b) / b * 100) + "%." : ""; }
  jrSet("jr-pace-sub", ps);
  const secAll = ses.reduce((a, s) => a + (s.sec || 0), 0), sec7 = ses.filter(s => s.t >= now - 7 * DAY).reduce((a, s) => a + (s.sec || 0), 0);
  jrSet("jr-time", ses.length ? "⏱️ " + jrF(secAll / 3600) + " h registradas (" + jrF(sec7 / 3600) + " h nos últimos 7 dias)." : "⏱️ Seu tempo de estudo aparece aqui depois da primeira sessão no estúdio de aulas.");

  // trilhas
  const nm = { ia: ["🤖 IA & Código", "ia.html"], mat: ["📐 Matemática", "matematica.html"], ing: ["🇺🇸 Inglês", "ingles.html"] };
  jrSet("jr-tracks", Object.keys(nm).map(t => {
    const p = P.per[t], w = p.pts / p.ptsTotal * 100, s2 = p.done / p.total * 100;
    return '<div class="jr-row"><a href="' + nm[t][1] + '" style="color:inherit;text-decoration:none">' + nm[t][0] + "</a><span>" + p.done + "/" + p.total + " · esforço " + jrPct(w) + '</span></div><div class="jr-bar"><i class="s" style="width:' + s2 + '%"></i><i class="w" style="width:' + w + '%"></i></div>';
  }).join(""));

  // próximo passo (regras simples e transparentes)
  const lastAct = Math.max(0, ...ev.map(e => e.t), ...ses.map(s => s.t));
  const idle = lastAct ? Math.floor((now - lastAct) / DAY) : null;
  const least = Object.keys(nm).sort((a, b) => P.per[a].pts / P.per[a].ptsTotal - P.per[b].pts / P.per[b].ptsTotal)[0];
  let nt;
  if (idle !== null && idle >= 3) nt = "Última atividade registrada há " + idle + " dias. Uma sessão curta em " + nm[least][0] + " retoma o fio sem pressão.";
  else if ((st.k === "attention" || st.k === "late") && req) nt = "Para voltar ao plano: ~" + jrF(req) + " pontos/semana. Comece por " + nm[least][0] + ", a trilha com menos esforço concluído.";
  else nt = "Continue em " + nm[least][0] + ", a trilha com menor esforço concluído (" + jrPct(P.per[least].pts / P.per[least].ptsTotal * 100) + ").";
  jrSet("hub-next-step-title", nt);
  const nb = jrEl("hub-next-step-btn"); if (nb) { nb.href = nm[least][1]; nb.textContent = "Ir para " + nm[least][0] + " ➔"; }

  // Mapa da trilha no topo do Hub (design v2): mesmos números do painel, sem cálculo próprio
  // O primeiro cálculo roda antes de o script do mapa existir: os números ficam guardados e o mapa os lê ao nascer.
  window.__dsRouteData = {
    overall: wPct,
    per: { ia: P.per.ia.pts / P.per.ia.ptsTotal * 100, mat: P.per.mat.pts / P.per.mat.ptsTotal * 100,
           ing: P.per.ing.pts / P.per.ing.ptsTotal * 100, proj: projDone / totalProj * 100 },
    nextHref: nm[least][1], nextLabel: nm[least][0].replace(/^\S+\s/, "")
  };
  if (typeof window.dsRoute === "function") window.dsRoute(window.__dsRouteData);

  // marcos reais (derivados do log de eventos, nunca inventados)
  const cv = RM.curve(ev, eff, logStart, now, P.pts);
  const ms = RM.milestones(cv, T.points), nx = RM.nextStep(wPct);
  jrSet("jr-ms", ms.length ? ms.map(m => "<li><span>✔ " + m.th + "% do esforço</span><span>" + (m.t ? formatDateBR(new Date(m.t)) : "antes do registro") + "</span></li>").join("")
                           : "<li><span>Nenhum marco registrado ainda</span><span></span></li>");
  jrSet("jr-next-ms", nx ? "Próximo marco: " + nx + "% do esforço (faltam " + jrF(T.points * nx / 100 - P.pts) + " pontos)." : "Todos os marcos alcançados.");

  // gráfico
  let end = Math.max(now + 14 * DAY, deadline || 0);
  if (fc.dSlow) end = Math.max(end, now + Math.min(fc.dSlow, 730) * DAY);
  else if (!deadline) end = now + 90 * DAY;
  jrSet("jr-chart", drawJourney({ start, end, now, deadline, total: T.points, pts: P.pts, curve: cv, fc }));
  updateWhatIf();
  if (typeof renderConquistas === "function") { try { renderConquistas(); } catch (e) { console.error(e); } }
}
"""
