// Uso: python metrics_js.py && node test_metrics.js
const assert = require("assert");
const RM = require("./metrics.js");
const DAY = 86400000, WEEK = 7 * DAY, now = Date.now();
const eff = { tracks: { ia: 1, mat: 1, ing: 1 }, topics: {} };

// totais e pesos
assert.deepStrictEqual(RM.totals(eff), { topics: 289, points: 289 });
assert.strictEqual(RM.totals({ tracks: { ia: 3, mat: 3, ing: 1 }, topics: {} }).points, 173 * 3 + 43 * 3 + 73);

// ponderado: concluído = peso; "falta terminar" = crédito parcial por vp/gp
const PR = { "ia-1": { s: "e" }, "mat-1": { s: "r", vp: 100, gp: 0 }, "ing-1": { s: "z" } };
const P = RM.progress(PR, { tracks: { ia: 3, mat: 2, ing: 1 }, topics: {} });
assert.strictEqual(P.structDone, 1);
assert.strictEqual(P.pts, 3 + 2 * 0.5);

// 5 tópicos simples != 5 complexos
const simples = RM.progress({ "ing-1": { s: "e" }, "ing-2": { s: "e" } }, { tracks: { ia: 1, mat: 1, ing: 1 }, topics: {} }).pts;
const complexos = RM.progress({ "ia-1": { s: "e" }, "ia-2": { s: "e" } }, { tracks: { ia: 4, mat: 1, ing: 1 }, topics: {} }).pts;
assert.ok(complexos > simples);

// previsão: poucos dados NÃO geram data
assert.strictEqual(RM.forecast(100, []).level, "insufficient");
assert.strictEqual(RM.forecast(100, [5]).level, "insufficient");
const f = RM.forecast(100, [10, 10, 10]);
assert.strictEqual(f.level, "preliminary");
assert.strictEqual(f.dMed, 70); // 100 / (10/7)
assert.strictEqual(RM.forecast(100, [10, 10, 10, 10]).level, "ok");
assert.strictEqual(RM.forecast(0, [10, 10]).level, "done");

// série semanal ignora bulk e semanas antes do início do registro
const ev = [
  { t: now - 2 * DAY, id: "ia-1", f: "z", to: "e", src: "ui" },
  { t: now - 3 * DAY, id: "ia-2", f: "z", to: "e", src: "bulk" },
  { t: now - 9 * DAY, id: "ia-3", f: "z", to: "e", src: "ui" },
];
const ser = RM.weeklySeries(ev, now, now - 15 * DAY, eff);
assert.deepStrictEqual(ser, [1, 1]); // 2 semanas completas; o bulk não conta
assert.deepStrictEqual(RM.weeklySeries(ev, now, now - 5 * DAY, eff), []); // 5 dias: nenhuma semana completa

// situação vs plano
const total = 289, dl = now + 180 * DAY, st0 = now;
assert.strictEqual(RM.status(50, 8, total, 5).k, "nodata");            // < 7 dias
assert.strictEqual(RM.status(50, null, total, 30).k, "neutral");       // sem meta nunca é "atrasado"
assert.strictEqual(RM.status(100, 50, total, 30).k, "ahead");
assert.strictEqual(RM.status(52, 50, total, 30).k, "ontrack");
assert.strictEqual(RM.status(40, 50, total, 30).k, "ontrack");         // -10 pts = -3,5% (dentro de 5%)
assert.strictEqual(RM.status(30, 50, total, 30).k, "attention");       // -20 pts
assert.strictEqual(RM.status(10, 50, total, 30).k, "late");            // -40 pts

// marcos só a partir do log
const cv = RM.curve([{ t: now - DAY, id: "ia-1", f: "z", to: "e" }], eff, now - 10 * DAY, now, 30);
assert.ok(RM.milestones(cv, 289).some(m => m.th === 10));
console.log("✅ todos os testes passaram");
