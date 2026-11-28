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
// chaves antigas (números do formato anterior) não contam como tópicos
const legado = RM.progress({ "35": { s: "e" }, "211": { s: "e" }, "ia-1": { s: "e" } }, eff);
assert.strictEqual(legado.structDone, 1);
assert.strictEqual(legado.per.ia.done, 1);
assert.strictEqual(RM.evNet({ id: "35", f: "z", to: "e" }, eff), 0);
assert.strictEqual(RM.evNet({ id: "ia-1", f: "z", to: "e" }, eff), 1);
// com catálogo: id que não existe no roteiro e opcional não contam (nem em progresso, nem em eventos, nem no total)
RM.configure({ totals: { ia: 2, mat: 1, ing: 1 }, optional: ["ia-op"], required: ["ia-a", "ia-b", "mat-a", "ing-a"] });
const cat = RM.progress({ "ia-a": { s: "e" }, "ia-op": { s: "e" }, "ia-9-9-9": { s: "e" } }, eff);
assert.strictEqual(cat.structDone, 1);
assert.strictEqual(RM.evNet({ id: "ia-9-9-9", f: "z", to: "e" }, eff), 0);
assert.strictEqual(RM.totals({ tracks: eff.tracks, topics: { "ia-9-9-9": 7 } }).points, 4);

// treino: nas aulas com treino, 25% do peso vem dele, e só com pelo menos 70% de acertos (o melhor resultado)
RM.configure({ treino: ["ia-a", "mat-a"] });
const w6 = { tracks: { ia: 4, mat: 6, ing: 1 }, topics: {} };
const melhor = RM.trBest({ "mat-a": { tr: { b: 70 } }, "ia-a": { tr: { b: 60 } }, "ia-b": { tr: { b: 100 } }, "ing-a": { p: {} } });
assert.deepStrictEqual(melhor, { "mat-a": 70, "ia-a": 60, "ia-b": 100 });
const so = id => ({ [id]: melhor[id] });                                                // o melhor de uma aula só
assert.strictEqual(RM.progress({ "ia-a": { s: "e" } }, w6).pts, 3);                    // concluída sem treino: só o estudo
assert.strictEqual(RM.progress({ "ia-a": { s: "e" } }, w6, so("ia-a")).pts, 3);        // 60% não basta
assert.strictEqual(RM.progress({ "mat-a": { s: "e" } }, w6, so("mat-a")).pts, 6);      // 70% fecha a aula
assert.strictEqual(RM.progress({ "mat-a": { s: "r", vp: 100, gp: 0 } }, w6, so("mat-a")).pts, 4.5 * 0.5 + 1.5);
assert.strictEqual(RM.progress({}, w6, melhor).pts, 1.5);                               // treino antes do estudo também conta
assert.strictEqual(RM.progress({}, w6, melhor).structDone, 0);
assert.strictEqual(RM.progress({ "ia-b": { s: "e" } }, w6, so("ia-b")).pts, 4);        // aula sem treino: tudo pelo estudo
assert.strictEqual(RM.progress({ "ia-a": { s: "e" }, "mat-a": { s: "e" } }, w6, melhor).pts, 3 + 6);
assert.strictEqual(RM.totals(w6).points, 2 * 4 + 6 + 1);                                // o peso total não muda
assert.strictEqual(RM.evNet({ id: "mat-a", f: "r", to: "e" }, w6), 4.5);               // concluir soma só o estudo
assert.strictEqual(RM.evNet({ id: "ia-b", f: "r", to: "e" }, w6), 4);
// a curva acumulada termina nos pontos de agora sem descer (aula concluída, treino por fazer)
const cvT = RM.curve([{ t: now - DAY, id: "mat-a", f: "z", to: "e" }], w6, now - 10 * DAY, now, RM.progress({ "mat-a": { s: "e" } }, w6).pts);
assert.ok(cvT.every((p, i) => i === 0 || p.v >= cvT[i - 1].v), JSON.stringify(cvT));
console.log("✅ todos os testes passaram");
