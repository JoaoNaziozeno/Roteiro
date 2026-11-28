# -*- coding: utf-8 -*-
"""
Cálculos do dashboard (progresso ponderado, ritmo, previsão, situação vs meta).
Funções PURAS: sem DOM, sem localStorage. Rodam no navegador e em Node (testes).

Uso:  python metrics_js.py   ->  gera metrics.js para testar com `node test_metrics.js`
"""

METRICS_JS = r"""
const RM = (() => {
  const DAY = 86400000, WEEK = 7 * DAY;
  const TRACK_TOTAL = { ia: 173, mat: 43, ing: 73 };   // substituído por configure() com os obrigatórios
  const OPTIONAL = new Set();                            // tópicos opcionais: fora da meta e dos percentuais
  const REQUIRED = new Set();                            // ids obrigatórios do roteiro atual (vazio = sem catálogo)
  const TREINO = new Set();                              // aulas com Treino no fim da Aula Visual (treino.py)
  // Nas aulas com treino, TR_SHARE do peso vem dele, e só com pelo menos TR_MIN% de acertos (o melhor resultado).
  // O resto vem do estudo (vídeo e Aula Visual, ou o ✓ de Concluído). O peso total da aula não muda.
  const TR_SHARE = 0.25, TR_MIN = 70;
  const trackOf = k => k.startsWith("mat-") ? "mat" : k.startsWith("ing-") ? "ing" : "ia";
  // Só conta tópicos do roteiro atual (ia-/mat-/ing-). Chaves antigas (números como "35", do formato
  // anterior) ficam de fora: antes eram somadas como IA e inflavam o total.
  const isTopic = k => typeof k === "string" && /^(ia|mat|ing)-/.test(k) && !OPTIONAL.has(k) && (!REQUIRED.size || REQUIRED.has(k));
  function configure(c) {
    if (c && c.totals) for (const t in c.totals) TRACK_TOTAL[t] = c.totals[t];
    if (c && Array.isArray(c.optional)) { OPTIONAL.clear(); c.optional.forEach(k => OPTIONAL.add(k)); }
    if (c && Array.isArray(c.required)) { REQUIRED.clear(); c.required.forEach(k => REQUIRED.add(k)); }
    if (c && Array.isArray(c.treino)) { TREINO.clear(); c.treino.forEach(k => TREINO.add(k)); }
  }
  const trackW = (eff, t) => (eff.tracks && eff.tracks[t] > 0) ? eff.tracks[t] : 1;
  const weightOf = (k, eff) => (eff.topics && eff.topics[k] > 0) ? eff.topics[k] : trackW(eff, trackOf(k));
  const trShare = k => (TREINO.has(k) ? TR_SHARE : 0);   // parte do peso que vem do treino (0 = aula sem treino)
  // Melhor % no treino de cada aula, das respostas salvas (roteiro-answers-v1: {aula: {tr: {b: melhor %}}})
  function trBest(answers) {
    const o = {};
    for (const k in (answers || {})) { const a = answers[k]; if (a && a.tr && a.tr.b > 0) o[k] = a.tr.b; }
    return o;
  }
  const trPassed = (k, best) => trShare(k) > 0 && Boolean(best) && (best[k] || 0) >= TR_MIN;
  // Crédito de uma aula: o estudo (concluída = inteiro; em andamento = média do % de vídeo e de aula) vale
  // (1 - TR_SHARE) do peso nas aulas com treino, e o treino aprovado vale o resto. Sem treino, o estudo vale tudo.
  function credit(k, it, w, best) {
    it = it || {};
    const sh = trShare(k);
    const study = it.s === "e" ? 1 : it.s === "r" ? Math.min(1, ((it.vp || 0) + (it.gp || 0)) / 200) : 0;
    return w * ((1 - sh) * study + (trPassed(k, best) ? sh : 0));
  }

  // Esforço total do roteiro, em "pontos" (1 ponto = tópico de peso 1)
  function totals(eff) {
    let topics = 0, points = 0;
    for (const t in TRACK_TOTAL) { topics += TRACK_TOTAL[t]; points += TRACK_TOTAL[t] * trackW(eff, t); }
    for (const k in (eff.topics || {})) if (isTopic(k) && eff.topics[k] > 0) points += eff.topics[k] - trackW(eff, trackOf(k));
    return { topics, points };
  }

  // Estrutural = tópicos concluídos. Ponderado = crédito de cada aula (credit): peso dos concluídos + crédito
  // parcial dos "falta terminar" (média do % de vídeo (vp) e % de aula visual (gp)) + o treino aprovado.
  // best = melhor % no treino de cada aula (trBest); sem ele, nenhum treino conta.
  function progress(PR, eff, best) {
    const per = {};
    for (const t in TRACK_TOTAL) per[t] = { done: 0, pts: 0, total: TRACK_TOTAL[t], ptsTotal: TRACK_TOTAL[t] * trackW(eff, t) };
    let structDone = 0, pts = 0;
    // o treino conta mesmo numa aula que ainda não aparece no progresso
    const keys = new Set(Object.keys(PR || {}).concat(Object.keys(best || {}).filter(k => trPassed(k, best))));
    for (const k of keys) {
      if (!isTopic(k)) continue;
      const it = (PR && PR[k]) || {}, t = trackOf(k), c = credit(k, it, weightOf(k, eff), best);
      if (it.s === "e") { structDone++; per[t].done++; }
      per[t].pts += c; pts += c;
    }
    return { structDone, pts, per };
  }

  // Variação líquida de esforço concluído causada por um evento {t,id,f,to,src}. Concluir uma aula com treino
  // soma só a parte do estudo: o treino aprovado entra nos pontos sem evento, como o crédito parcial.
  const evNet = (e, eff) => {
    if (!isTopic(e.id)) return 0;
    const w = weightOf(e.id, eff) * (1 - trShare(e.id));
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

  // Peso de cada trilha em pontos de esforço (ver TRACK_WEIGHTS no Python): o hub e as aulas usam este mesmo valor
  const TRACK_WEIGHTS = Object.freeze(__TRACK_WEIGHTS__);

  return { TRACK_TOTAL, TRACK_WEIGHTS, TR_SHARE, TR_MIN, configure, trackOf, isTopic, trackW, weightOf, trShare, trBest, trPassed,
           credit, totals, progress, evNet, weeklySeries, forecast, planned, status, requiredPace, curve, milestones, nextStep, hoursPerPoint };
})();
if (typeof module !== "undefined") module.exports = RM;
"""

# Pesos de esforço calibrados internamente (1 ponto ≈ 1h de estudo efetivo de um tópico "padrão").
#  - Inglês (1): cada tópico é uma videoaula de ~15-25 min de gramática/vocabulário básico-intermediário
#    + prática curta ≈ 1h. É a referência.
#  - IA & Código (4): tópicos muito heterogêneos (de "docstrings" a "Transformer", "RAG", "deploy",
#    projetos completos). Mediana realista para quem parte do zero ≈ 4h por tópico (ler + codar + depurar).
#  - Matemática (6): tópicos densos e abstratos (SVD, Jacobiana/Hessiana, MLE, KL, atenção), cada um com
#    derivação, exemplo resolvido e código. Exige reler, praticar exercícios e consolidar ≈ 6h por tópico.
# Resultado: IA ≈ 68% do esforço total, Matemática ≈ 25%, Inglês ≈ 7%.
# Fonte única: a Jornada do hub e o aviso de pontos de cada aula leem RM.TRACK_WEIGHTS.
TRACK_WEIGHTS = {"ia": 4, "mat": 6, "ing": 1}

import json as _json
METRICS_JS = METRICS_JS.replace("__TRACK_WEIGHTS__", _json.dumps(TRACK_WEIGHTS))

if __name__ == "__main__":
    with open("metrics.js", "w", encoding="utf-8") as f:
        f.write(METRICS_JS)
    print("metrics.js gerado. Teste: node test_metrics.js")
