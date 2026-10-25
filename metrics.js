
const RM = (() => {
  const DAY = 86400000, WEEK = 7 * DAY;
  const TRACK_TOTAL = { ia: 173, mat: 43, ing: 73 };
  const trackOf = k => k.startsWith("mat-") ? "mat" : k.startsWith("ing-") ? "ing" : "ia";
  const trackW = (eff, t) => (eff.tracks && eff.tracks[t] > 0) ? eff.tracks[t] : 1;
  const weightOf = (k, eff) => (eff.topics && eff.topics[k] > 0) ? eff.topics[k] : trackW(eff, trackOf(k));

  // Esforço total do roteiro, em "pontos" (1 ponto = tópico de peso 1)
  function totals(eff) {
    let topics = 0, points = 0;
    for (const t in TRACK_TOTAL) { topics += TRACK_TOTAL[t]; points += TRACK_TOTAL[t] * trackW(eff, t); }
    for (const k in (eff.topics || {})) if (eff.topics[k] > 0) points += eff.topics[k] - trackW(eff, trackOf(k));
    return { topics, points };
  }

  // Estrutural = tópicos concluídos. Ponderado = peso dos concluídos + crédito parcial dos "falta terminar"
  // (crédito parcial = média do % de vídeo (vp) e % de aula visual (gp) já registrados no tópico).
  function progress(PR, eff) {
    const per = {};
    for (const t in TRACK_TOTAL) per[t] = { done: 0, pts: 0, total: TRACK_TOTAL[t], ptsTotal: TRACK_TOTAL[t] * trackW(eff, t) };
    let structDone = 0, pts = 0;
    for (const k in PR) {
      const it = PR[k] || {}, t = trackOf(k), w = weightOf(k, eff);
      let c = 0;
      if (it.s === "e") { c = w; structDone++; per[t].done++; }
      else if (it.s === "r") c = w * Math.min(1, ((it.vp || 0) + (it.gp || 0)) / 200);
      per[t].pts += c; pts += c;
    }
    return { structDone, pts, per };
  }

  // Variação líquida de esforço concluído causada por um evento {t,id,f,to,src}
  const evNet = (e, eff) => {
    const w = weightOf(e.id, eff);
    return (e.to === "e" && e.f !== "e") ? w : (e.f === "e" && e.to !== "e") ? -w : 0;
  };

  // Esforço concluído por semana (janelas de 7 dias terminando agora; só semanas COMPLETAS após o início do registro).
  // Eventos "bulk" (importação em lote) não entram: não representam ritmo real.
  function weeklySeries(ev, now, logStart, eff, maxWeeks) {
    const out = [], n = maxWeeks || 8;
    for (let k = 0; k < n; k++) {
      const a = now - (k + 1) * WEEK, b = now - k * WEEK;
      if (!logStart || a < logStart) break;
      let s = 0;
      for (const e of ev) if (e.src !== "bulk" && e.t >= a && e.t < b) s += evNet(e, eff);
      out.push(Math.max(0, s));
    }
    return out; // índice 0 = semana mais recente
  }

  // Previsão em faixa. Com poucos dados NÃO devolve data.
  function forecast(remaining, series) {
    const n = series.length;
    if (remaining <= 0) return { level: "done" };
    if (n < 2) return { level: "insufficient", n, need: 2 };
    const s = series.slice().sort((a, b) => a - b);
    const q = p => { const i = (s.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i); return s[lo] + (s[hi] - s[lo]) * (i - lo); };
    const mean = series.reduce((a, b) => a + b, 0) / n;
    const sd = Math.sqrt(series.reduce((a, b) => a + (b - mean) ** 2, 0) / n);
    const cv = mean > 0 ? sd / mean : 9;
    const med = q(0.5), slow = n < 4 ? s[0] : q(0.25), fast = n < 4 ? s[n - 1] : q(0.75);
    let conf = n >= 6 ? "alta" : n >= 4 ? "média" : "baixa";
    if (cv > 0.8 && conf !== "baixa") conf = conf === "alta" ? "média" : "baixa";
    const days = p => (p > 0 && remaining / (p / 7) < 1500) ? Math.ceil(remaining / (p / 7)) : null;
    return { level: n >= 4 ? "ok" : "preliminary", conf, n, med, slow, fast, cv,
             dMed: days(med), dSlow: days(slow), dFast: days(fast) };
  }

  const planned = (total, start, deadline, now) =>
    deadline ? total * Math.min(1, Math.max(0, (now - start) / (deadline - start))) : null;

  // Situação vs plano (esforço, não contagem de tópicos). Tolerância: 5% do esforço total.
  function status(done, plannedNow, total, elapsedDays) {
    if (plannedNow == null) return { k: "neutral" };
    if (elapsedDays < 7) return { k: "nodata" };
    const d = done - plannedNow, tol = 0.05 * total;
    const k = d > tol ? "ahead" : d >= -tol ? "ontrack" : d >= -2 * tol ? "attention" : "late";
    return { k, delta: d };
  }

  function requiredPace(remaining, now, deadline) {
    const weeks = (deadline - now) / WEEK;
    return weeks > 0 ? remaining / weeks : null;
  }

  // Curva acumulada real. Antes do início do registro só há o "baseline" (não inventamos histórico).
  function curve(ev, eff, logStart, now, pts) {
    if (!logStart) return [];
    const sorted = ev.slice().sort((a, b) => a.t - b.t);
    const net = sorted.reduce((a, e) => a + evNet(e, eff), 0);
    let run = Math.max(0, pts - net);
    const out = [{ t: logStart, v: run }];
    for (const e of sorted) { const d = evNet(e, eff); if (d !== 0) { run += d; out.push({ t: e.t, v: Math.max(0, run) }); } }
    out.push({ t: now, v: pts });
    return out;
  }

  const STEPS = [10, 25, 50, 75, 100];
  function milestones(cv, total) {
    const done = [];
    for (const th of STEPS) {
      const i = cv.findIndex(p => p.v / total * 100 >= th);
      if (i >= 0) done.push({ th, t: i === 0 ? null : cv[i].t });
    }
    return done;
  }
  const nextStep = pct => STEPS.find(s => s > pct) || null;

  // Horas por ponto de esforço, só com dados suficientes (>=3h registradas e >=3 pontos concluídos no período)
  function hoursPerPoint(sessions, ev, eff, logStart) {
    if (!logStart) return null;
    const sec = sessions.filter(s => s.t >= logStart).reduce((a, s) => a + (s.sec || 0), 0);
    const pts = ev.filter(e => e.src !== "bulk").reduce((a, e) => a + evNet(e, eff), 0);
    return (sec >= 3 * 3600 && pts >= 3) ? (sec / 3600) / pts : null;
  }

  return { TRACK_TOTAL, trackOf, trackW, weightOf, totals, progress, evNet, weeklySeries, forecast,
           planned, status, requiredPace, curve, milestones, nextStep, hoursPerPoint };
})();
if (typeof module !== "undefined") module.exports = RM;
