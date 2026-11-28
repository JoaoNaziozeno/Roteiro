# -*- coding: utf-8 -*-
"""
Geradores de conta do Treino (Matemática: Álgebra Linear para IA & Tensores).

Cada gerador sorteia números que dão resultado "redondo" (inteiro ou com até 2 casas), monta as alternativas
erradas a partir dos erros mais comuns (com o porquê de cada uma) e escreve a resolução com os mesmos números.
A cada treino os números mudam.

Formato: TR.GEN[id] = { t: "título curto", f: (R, p) => ({ q, v, ops: [{v, why}], x, d, casas?, h?, fmt? }) }
  q     enunciado (HTML com $LaTeX$)       v     resposta certa (número, vetor, matriz ou texto)
  ops   erradas, cada uma com o erro que leva a ela    x     resolução com os números sorteados
  d     dados sorteados: test_treino.py refaz a conta com o NumPy a partir deles e confere v
  fmt   como escrever uma alternativa (padrão: número, vetor ou matriz em LaTeX)
"""

TR_GEN_JS = r"""
// =================== TREINO: geradores de conta (Álgebra Linear) ===================
(() => {
  const G = TR.GEN, n = TR.n, V = TR.vec, M = TR.mat;
  const N1 = x => n(x);
  const P = x => (typeof x === "number" && x < 0 ? "(" + n(x) + ")" : n(x));   // negativo entre parênteses nos produtos
  const nt = (x, c) => n(x, c).replace("{,}", ",");                             // número fora do LaTeX
  const $ = s => "$" + s + "$";
  const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
  const sum = a => a.reduce((s, x) => s + x, 0);
  const add = (a, b) => a.map((x, i) => x + b[i]);
  const sub = (a, b) => a.map((x, i) => x - b[i]);
  const mul = (k, a) => a.map(x => k * x);
  const mv = (A, x) => A.map(r => dot(r, x));
  const mm = (A, B) => A.map(r => B[0].map((_, j) => r.reduce((s, x, k) => s + x * B[k][j], 0)));
  const tr = A => A[0].map((_, j) => A.map(r => r[j]));
  const had = (A, B) => A.map((r, i) => r.map((x, j) => x * B[i][j]));
  const r2 = x => Math.round(x * 100) / 100;
  const nrm = v => Math.sqrt(dot(v, v));
  const prods = (a, b) => a.map((x, i) => P(x) + "\\cdot " + P(b[i])).join(" + ");
  const li = arr => "<ol>" + arr.map(s => "<li>" + s + "</li>").join("") + "</ol>";
  const signed = (R, v) => v.map(x => (x === 0 ? 0 : x * R.sign()));
  const dimOf = (R, p) => p.dim || R.pick([2, 3]);
  // "2x - y", "a + 3b": coeficientes 1 e 0 somem
  const lin = (cs, vs) => {
    let s = "";
    cs.forEach((c, i) => {
      if (!c) return;
      const t = (Math.abs(c) === 1 ? "" : n(Math.abs(c))) + vs[i];
      s += s ? (c < 0 ? " - " : " + ") + t : (c < 0 ? "-" : "") + t;
    });
    return s || "0";
  };
  const par = (x, y, a, b) => $(a + " = " + n(x) + ",\\ " + b + " = " + n(y));
  const lamPair = v => { const s = v.slice().sort((p, q) => p - q); return $("\\lambda = " + n(s[0]) + " \\text{ e } " + n(s[1])); };
  const PIT2 = [[[3, 4], 5], [[6, 8], 10], [[5, 12], 13], [[8, 15], 17], [[9, 12], 15]];
  const PIT3 = [[[1, 2, 2], 3], [[2, 3, 6], 7], [[1, 4, 8], 9], [[4, 4, 7], 9], [[2, 6, 9], 11], [[6, 6, 7], 11], [[2, 10, 11], 15]];
  const PIT5 = [[3, 4], [4, 3], [0, 5], [5, 0], [6, 8], [8, 6], [0, 10], [10, 0]];   // normas 5 e 10: divisões exatas

  // ---------------- Vetores ----------------
  G.vsoma = { t: "Soma de vetores", f: (R, p) => {
    const k = dimOf(R, p), u = R.vec(k, -6, 6), v = R.vec(k, -6, 6), s = add(u, v);
    return { q: "Calcule " + $("u + v") + " para " + $("u = " + V(u)) + " e " + $("v = " + V(v)) + ".", v: s, d: { u, v },
      ops: [{ v: sub(u, v), why: "fez u − v" }, { v: u.map((x, i) => x * v[i]), why: "multiplicou as coordenadas" },
            { v: sum(u) + sum(v), why: "somou tudo num número só" }],
      x: "Some coordenada por coordenada: " + $("(" + u.map((x, i) => n(x) + " + " + P(v[i])).join(",\\ ") + ") = " + V(s)) + "." };
  } };

  G.vescala = { t: "Número vezes vetor", f: (R, p) => {
    const k = dimOf(R, p), a = R.pick([-3, -2, 2, 3, 4, 5]), u = R.vec(k, -5, 5), s = mul(a, u);
    return { q: "Calcule " + $(n(a) + "\\,u") + " para " + $("u = " + V(u)) + ".", v: s, d: { a, u },
      ops: [{ v: u.map(x => x + a), why: "somou o número em cada coordenada" }, { v: [a * u[0]].concat(u.slice(1)), why: "multiplicou só a 1ª coordenada" },
            { v: mul(-a, u), why: "errou o sinal" }],
      x: "Multiplique cada coordenada por " + $(n(a)) + ": " + $("(" + u.map(x => n(a) + "\\cdot " + P(x)).join(",\\ ") + ") = " + V(s)) + "." };
  } };

  G.vcomb = { t: "Combinação linear", f: (R, p) => {
    const a = R.nz(-3, 3), b = R.nz(-3, 3), u = R.vec(2, -4, 4), v = R.vec(2, -4, 4), s = add(mul(a, u), mul(b, v));
    return { q: "Calcule " + $("w = " + lin([a, b], ["u", "v"])) + " para " + $("u = " + V(u)) + " e " + $("v = " + V(v)) + ".", v: s, d: { a, b, u, v },
      ops: [{ v: add(mul(a, u), v), why: "esqueceu o número que multiplica v" }, { v: add(mul(b, u), mul(a, v)), why: "trocou os números de u e v" },
            { v: sub(mul(a, u), mul(b, v)), why: "errou o sinal do 2º termo" }],
      x: "Primeiro multiplique, depois some: " + $(n(a) + "\\,u = " + V(mul(a, u))) + " e " + $(n(b) + "\\,v = " + V(mul(b, v))) + ", então " + $("w = " + V(s)) + "." };
  } };

  G.vdesloc = { t: "Vetor de A até B", f: (R, p) => {
    const k = dimOf(R, p), A = R.vec(k, -5, 6), B = R.vec(k, -5, 6), s = sub(B, A);
    return { q: "Qual é o vetor que leva o ponto " + $("A = " + V(A)) + " até o ponto " + $("B = " + V(B)) + "?", v: s, d: { A, B },
      ops: [{ v: sub(A, B), why: "fez A − B (o vetor ao contrário)" }, { v: add(A, B), why: "somou os pontos" }, { v: B.slice(), why: "usou só o ponto B" }],
      x: "Chegada menos saída: " + $("\\overrightarrow{AB} = B - A = " + V(s)) + "." };
  } };

  // ---------------- Combinações, span e bases ----------------
  G.combcoef = { t: "Coeficientes de uma combinação linear", f: (R, p) => {
    const bases = [[[1, 0], [1, 1]], [[1, 1], [0, 1]], [[2, 1], [1, 1]], [[1, 2], [0, 1]], [[1, 1], [1, -1]], [[1, 0], [2, 1]], [[3, 1], [1, 0]], [[1, -1], [0, 1]]];
    const [b1, b2] = R.pick(bases);
    let a, b; do { a = R.nz(-4, 4); b = R.nz(-4, 4); } while (a === b);
    const w = add(mul(a, b1), mul(b, b2));
    return { q: "Escreva " + $("w = " + V(w)) + " como " + $("w = a\\,b_1 + b\\,b_2") + ", com " + $("b_1 = " + V(b1)) + " e " + $("b_2 = " + V(b2)) +
             ". Quanto valem " + $("a") + " e " + $("b") + "?",
      v: [a, b], fmt: v => par(v[0], v[1], "a", "b"), d: { b1, b2, w },
      ops: [{ v: [b, a], why: "trocou a e b" }, { v: w.slice(), why: "usou as coordenadas de w" }, { v: [a, -b], why: "errou o sinal de b" }],
      x: "Coordenada por coordenada: " + $(lin([b1[0], b2[0]], ["a", "b"]) + " = " + n(w[0])) + " e " + $(lin([b1[1], b2[1]], ["a", "b"]) + " = " + n(w[1])) +
         ". Resolvendo, " + par(a, b, "a", "b") + ". Confira: " + $(n(a) + "\\cdot " + V(b1) + " + " + P(b) + "\\cdot " + V(b2) + " = " + V(w)) + "." };
  } };

  G.base2 = { t: "Base do R² pelo determinante", f: (R, p) => {
    const u = [R.nz(-5, 5), R.int(-5, 5)];
    let v;
    if (R.rnd() < 0.45) v = mul(R.pick([-3, -2, -1, 2, 3]), u);              // paralelos: não formam base
    else do { v = [R.int(-5, 5), R.nz(-5, 5)]; } while (u[0] * v[1] - u[1] * v[0] === 0);
    const det = u[0] * v[1] - u[1] * v[0];
    const fmt = d => (d !== 0 ? "Sim: " + $("\\det = " + n(d) + " \\neq 0") : "Não: " + $("\\det = 0") + ", um é múltiplo do outro");
    return { q: "Monte a matriz com " + $("u = " + V(u)) + " e " + $("v = " + V(v)) + " nas colunas. Quanto vale o determinante, e os dois formam uma base do " + $("\\mathbb{R}^2") + "?",
      v: det, fmt, d: { u, v },
      ops: [{ v: u[0] * v[1] + u[1] * v[0], why: "somou os produtos em vez de subtrair" }, { v: u[0] * u[1] - v[0] * v[1], why: "multiplicou dentro de cada vetor" },
            { v: -det, why: "subtraiu na ordem errada" }],
      x: $("\\det " + M([[u[0], v[0]], [u[1], v[1]]]) + " = " + P(u[0]) + "\\cdot " + P(v[1]) + " - " + P(v[0]) + "\\cdot " + P(u[1]) + " = " + n(det)) + ". " +
         (det !== 0 ? "Diferente de zero: os vetores não são paralelos e geram o plano inteiro, então formam uma base."
                    : "Zero: um vetor é múltiplo do outro, os dois ficam na mesma reta e não formam base.") };
  } };

  // ---------------- Produto escalar e projeções ----------------
  G.dot = { t: "Produto escalar", f: (R, p) => {
    const k = p.dim || R.pick([2, 3, 3, 4]), u = R.vec(k, -5, 5), v = R.vec(k, -5, 5), s = dot(u, v), pr = u.map((x, i) => x * v[i]);
    return { q: "Calcule " + $("u \\cdot v") + " para " + $("u = " + V(u)) + " e " + $("v = " + V(v)) + ".", v: s, d: { u, v },
      ops: [{ v: pr, why: "multiplicou e não somou" }, { v: sum(u) + sum(v), why: "somou todos os números" }, { v: sum(pr.map(Math.abs)), why: "ignorou os sinais" }],
      x: "Multiplique posição por posição e some: " + $(prods(u, v) + " = " + pr.map(P).join(" + ") + " = " + n(s)) + "." };
  } };

  G.dotang = { t: "Sinal do produto escalar e o ângulo", f: (R, p) => {
    const u = [R.nz(-5, 5), R.nz(-5, 5)];
    let v;
    if (R.rnd() < 0.34) v = mul(R.pick([-2, -1, 1, 2]), [-u[1], u[0]]);      // perpendicular
    else do { v = R.vec(2, -5, 5); } while (dot(u, v) === 0);
    const s = dot(u, v), cat = s > 0 ? "agudo" : s < 0 ? "obtuso" : "reto";
    const H = { agudo: "Agudo (menor que 90°)", reto: "Reto (exatamente 90°)", obtuso: "Obtuso (maior que 90°)", nd: "Não dá para saber sem medir com transferidor" };
    return { q: "Sem calcular o ângulo: o ângulo entre " + $("u = " + V(u)) + " e " + $("v = " + V(v)) + " é…", v: cat, fmt: c => H[c], d: { u, v },
      ops: ["agudo", "reto", "obtuso", "nd"].filter(c => c !== cat).map(c => ({ v: c, why: "" })),
      x: $("u \\cdot v = " + prods(u, v) + " = " + n(s)) + ". " + (s > 0 ? "Positivo: os vetores apontam para o mesmo lado, ângulo agudo."
         : s < 0 ? "Negativo: apontam para lados opostos, ângulo obtuso." : "Zero: os vetores são perpendiculares (90°).") };
  } };

  G.projesc = { t: "Projeção escalar", f: (R, p) => {
    const v = signed(R, R.pick(PIT5)), u = R.vec(2, -6, 6), L = nrm(v), s = dot(u, v), c = s / L;
    return { q: "Qual é a projeção escalar de " + $("u = " + V(u)) + " sobre " + $("v = " + V(v)) + "? Use " + $("\\text{comp}_v\\,u = \\dfrac{u \\cdot v}{\\lVert v \\rVert}") + ".",
      v: c, d: { u, v },
      ops: [{ v: s, why: "esqueceu de dividir por ‖v‖" }, { v: s / (L * L), why: "dividiu por ‖v‖² (o fator do vetor projeção)" }, { v: s * L, why: "multiplicou em vez de dividir" }],
      x: $("u \\cdot v = " + prods(u, v) + " = " + n(s)) + " e " + $("\\lVert v \\rVert = \\sqrt{" + P(v[0]) + "^2 + " + P(v[1]) + "^2} = " + n(L)) +
         ", então " + $("\\dfrac{" + n(s) + "}{" + n(L) + "} = " + n(c)) + "." };
  } };

  G.ortok = { t: "Valor que deixa dois vetores perpendiculares", f: (R, p) => {
    const k0 = R.nz(-5, 5), c = R.nz(-4, 4), m = R.pick([1, 1, -1, 2]), u = [m * c, -m * k0];
    return { q: "Para qual valor de " + $("k") + " os vetores " + $("u = " + V(u)) + " e " + $("w = (k,\\ " + n(c) + ")") + " são perpendiculares?",
      v: k0, d: { u, c },
      ops: [{ v: -k0, why: "errou o sinal ao isolar k" }, { v: c, why: "copiou a outra coordenada de w" }, { v: 0, why: "achou que k = 0 sempre resolve" }],
      x: "Perpendiculares têm produto escalar zero: " + $(n(u[0]) + "k + " + P(u[1]) + "\\cdot " + P(c) + " = 0") + ", ou seja, " +
         $(n(u[0]) + "k = " + n(-u[1] * c)) + " e " + $("k = " + n(k0)) + "." };
  } };

  // ---------------- Normas e distâncias ----------------
  G.l2 = { t: "Norma L2 (comprimento)", f: (R, p) => {
    const [base, L] = R.pick(R.rnd() < 0.5 ? PIT2 : PIT3), v = signed(R, R.shuffle(base));
    return { q: "Calcule a norma L2 (o comprimento) de " + $("v = " + V(v)) + ".", v: L, d: { v },
      ops: [{ v: sum(v.map(Math.abs)), why: "calculou a norma L1 (soma dos módulos)" }, { v: L * L, why: "esqueceu a raiz quadrada" }, { v: sum(v), why: "somou as coordenadas com sinal" }],
      x: $("\\lVert v \\rVert_2 = \\sqrt{" + v.map(x => P(x) + "^2").join(" + ") + "} = \\sqrt{" + n(L * L) + "} = " + n(L)) + "." };
  } };

  G.l1 = { t: "Norma L1", f: (R, p) => {
    let v; do { v = R.vec(R.int(3, 5), -9, 9); } while (!v.some(x => x < 0) || !v.some(x => x > 0));
    const s = sum(v.map(Math.abs));
    return { q: "Calcule a norma L1 de " + $("v = " + V(v)) + ".", v: s, d: { v },
      ops: [{ v: sum(v), why: "esqueceu o módulo (os negativos descontaram)" }, { v: Math.max(...v.map(Math.abs)), why: "calculou a norma L∞ (o maior módulo)" },
            { v: sum(v.map(x => x * x)), why: "somou os quadrados" }],
      x: "Some os módulos: " + $("\\lVert v \\rVert_1 = " + v.map(x => "|" + n(x) + "|").join(" + ") + " = " + n(s)) + "." };
  } };

  G.dist2 = { t: "Distância euclidiana", f: (R, p) => {
    const [base, L] = R.pick(R.rnd() < 0.6 ? PIT2 : PIT3.slice(0, 4)), dl = signed(R, R.shuffle(base)), A = R.vec(dl.length, -4, 6), B = add(A, dl);
    return { q: "Qual é a distância euclidiana entre " + $("A = " + V(A)) + " e " + $("B = " + V(B)) + "?", v: L, d: { A, B },
      ops: [{ v: sum(dl.map(Math.abs)), why: "calculou a distância Manhattan" }, { v: L * L, why: "esqueceu a raiz quadrada" }, { v: Math.abs(sum(dl)), why: "somou as diferenças com sinal" }],
      x: "Diferenças: " + $("B - A = " + V(dl)) + ". Então " + $("d = \\sqrt{" + dl.map(x => P(x) + "^2").join(" + ") + "} = \\sqrt{" + n(L * L) + "} = " + n(L)) + "." };
  } };

  G.manh = { t: "Distância Manhattan", f: (R, p) => {
    const k = R.pick([2, 3]);
    let A, B, dl; do { A = R.vec(k, -5, 6); B = R.vec(k, -5, 6); dl = sub(B, A); } while (!dl.some(x => x < 0) || !dl.some(x => x > 0));
    const s = sum(dl.map(Math.abs));
    return { q: "Qual é a distância Manhattan (L1) entre " + $("A = " + V(A)) + " e " + $("B = " + V(B)) + "?", v: s, d: { A, B },
      ops: [{ v: r2(nrm(dl)), why: "calculou a distância euclidiana" }, { v: Math.abs(sum(dl)), why: "somou as diferenças com sinal" }, { v: Math.max(...dl.map(Math.abs)), why: "pegou só a maior diferença" }],
      x: "Some quanto se anda em cada eixo: " + $(dl.map((x, i) => "|" + n(B[i]) + " - " + P(A[i]) + "|").join(" + ") + " = " + dl.map(x => n(Math.abs(x))).join(" + ") + " = " + n(s)) + "." };
  } };

  // ---------------- Ângulo e cosseno ----------------
  G.cos = { t: "Similaridade de cosseno", f: (R, p) => {
    let u, v, c; do { u = signed(R, R.pick(PIT5)); v = signed(R, R.pick(PIT5)); c = dot(u, v) / (nrm(u) * nrm(v)); } while (Math.abs(c) > 0.999);
    const s = dot(u, v), Lu = nrm(u), Lv = nrm(v);
    return { q: "Calcule a similaridade de cosseno entre " + $("u = " + V(u)) + " e " + $("v = " + V(v)) + ".", v: c, d: { u, v },
      ops: [{ v: s, why: "esqueceu de dividir pelas normas" }, { v: r2(s / Lu), why: "dividiu só por ‖u‖" }, { v: r2(1 - c), why: "calculou a distância de cosseno (1 − cos)" }],
      x: $("u \\cdot v = " + prods(u, v) + " = " + n(s)) + ", " + $("\\lVert u \\rVert = " + n(Lu)) + " e " + $("\\lVert v \\rVert = " + n(Lv)) +
         ". Então " + $("\\cos\\theta = \\dfrac{" + n(s) + "}{" + n(Lu) + "\\cdot " + n(Lv) + "} = " + n(c)) + "." };
  } };

  G.cosesp = { t: "Cosseno em casos especiais", f: (R, p) => {
    const u = [R.nz(-4, 4), R.nz(-4, 4)], t = R.pick(["mesmo", "oposto", "perp"]), k = R.pick([2, 3, 4]);
    const v = t === "mesmo" ? mul(k, u) : t === "oposto" ? mul(-k, u) : mul(R.pick([1, 2, -1]), [-u[1], u[0]]);
    const c = t === "mesmo" ? 1 : t === "oposto" ? -1 : 0;
    const fmt = x => (x === "dep" ? "Depende do tamanho dos vetores" : $(n(x)));
    return { q: "Sem fazer a conta inteira: qual é a similaridade de cosseno entre " + $("u = " + V(u)) + " e " + $("v = " + V(v)) + "?",
      v: c, fmt, d: { u, v },
      ops: [1, -1, 0].filter(x => x !== c).map(x => ({ v: x, why: "" })).concat([{ v: "dep", why: "o tamanho não muda o cosseno" }]),
      x: t === "perp" ? "Aqui " + $("u \\cdot v = " + n(dot(u, v))) + ": os vetores são perpendiculares, então o cosseno é 0."
        : $("v = " + n(t === "mesmo" ? k : -k) + "\\,u") + ": mesma direção" + (t === "mesmo" ? " e mesmo sentido, cosseno 1." : ", sentido oposto, cosseno −1.") +
          " Esticar o vetor (o " + $(n(k)) + ") não muda o cosseno: ele só olha a direção." };
  } };

  G.angesp = { t: "Ângulo entre vetores", f: (R, p) => {
    const T = [[[1, 0], [1, 1], 45], [[1, 0], [0, 1], 90], [[1, 1], [-1, 1], 90], [[1, 0], [-1, 1], 135], [[1, 0], [-1, 0], 180],
               [[1, 1], [2, 2], 0], [[1, 0], [1, -1], 45], [[1, 1], [0, 1], 45], [[1, 1], [-1, 0], 135], [[0, 1], [1, -1], 135]];
    const [a, b, ang] = R.pick(T), op = R.int(0, 3);
    const f = w => (op === 1 ? [w[1], w[0]] : op === 2 ? [-w[0], w[1]] : op === 3 ? [w[0], -w[1]] : w);   // o mesmo espelho nos dois: ângulo igual
    const u = f(mul(R.pick([1, 2, 3]), a)).map(x => x || 0), v = f(mul(R.pick([1, 2, 3]), b)).map(x => x || 0);
    const s = dot(u, v), c = s / (nrm(u) * nrm(v));
    return { q: "Qual é o ângulo entre " + $("u = " + V(u)) + " e " + $("v = " + V(v)) + "?", v: ang, fmt: x => $(n(x) + "^\\circ"), d: { u, v },
      ops: R.shuffle([0, 45, 60, 90, 135, 180].filter(x => x !== ang)).slice(0, 3).map(x => ({ v: x, why: "" })),
      x: $("\\cos\\theta = \\dfrac{u \\cdot v}{\\lVert u \\rVert\\,\\lVert v \\rVert} = \\dfrac{" + n(s) + "}{\\sqrt{" + n(dot(u, u)) + "}\\cdot\\sqrt{" + n(dot(v, v)) + "}} \\approx " + n(c, 3)) +
         ". Como " + $("\\cos " + n(ang) + "^\\circ \\approx " + n(Math.cos(ang * Math.PI / 180), 3)) + ", o ângulo é " + $(n(ang) + "^\\circ") + "." };
  } };

  // ---------------- Matrizes como transformações ----------------
  G.matvec = { t: "Matriz vezes vetor", f: (R, p) => {
    const k = p.dim || 2, A = Array.from({ length: k }, () => R.vec(k, -3, 4)), x = R.vec(k, -3, 4), y = mv(A, x);
    return { q: "Calcule " + $("A\\,x") + " para " + $("A = " + M(A)) + " e " + $("x = " + V(x)) + ".", v: y, d: { A, x },
      ops: [{ v: mv(tr(A), x), why: "usou as colunas como se fossem linhas (Aᵀx)" }, { v: A.map((r, i) => r[i] * x[i]), why: "usou só a diagonal" },
            { v: A.map(r => sum(r) * x[0]), why: "multiplicou a soma de cada linha só por x₁" }],
      x: "Cada linha de A faz um produto escalar com x:" + li(A.map((r, i) => $("y_" + (i + 1) + " = " + prods(r, x) + " = " + n(y[i])))) + "Resultado: " + $(V(y)) + "." };
  } };

  G.matcol = { t: "Para onde vai um vetor da base", f: (R, p) => {
    const A = [R.vec(2, -4, 5), R.vec(2, -4, 5)], j = R.int(0, 1), e = j === 0 ? [1, 0] : [0, 1], y = mv(A, e);
    return { q: "A matriz " + $("A = " + M(A)) + " transforma o plano. Para onde ela leva " + $(j === 0 ? "e_1 = (1,\\ 0)" : "e_2 = (0,\\ 1)") + "?", v: y, d: { A, e },
      ops: [{ v: A[j].slice(), why: "pegou a linha em vez da coluna" }, { v: mv(A, j === 0 ? [0, 1] : [1, 0]), why: "pegou a outra coluna" }, { v: e.slice(), why: "achou que o vetor não muda" }],
      x: $("A\\,e_" + (j + 1)) + " é exatamente a " + (j + 1) + "ª coluna de A: " + $(V(y)) + ". É por isso que as colunas de uma matriz mostram para onde vão os eixos." };
  } };

  G.transf = { t: "Matriz de uma transformação", f: (R, p) => {
    const k = R.pick([2, 3]);
    const L = [["rot90", "gira o plano 90° no sentido anti-horário", [[0, -1], [1, 0]]], ["rot-90", "gira o plano 90° no sentido horário", [[0, 1], [-1, 0]]],
               ["refx", "espelha no eixo x: (x, y) vira (x, −y)", [[1, 0], [0, -1]]], ["refy", "espelha no eixo y: (x, y) vira (−x, y)", [[-1, 0], [0, 1]]],
               ["esc", "aumenta tudo " + k + " vezes", [[k, 0], [0, k]]], ["estx", "estica só o eixo x, " + k + " vezes", [[k, 0], [0, 1]]],
               ["rot180", "gira o plano 180°", [[-1, 0], [0, -1]]]];
    const i = R.int(0, L.length - 1), [nome, desc, A] = L[i], cols = tr(A);
    return { q: "Qual matriz " + desc + "?", v: A, d: { nome, k },
      ops: R.shuffle(L.filter((_, j) => j !== i)).map(o => ({ v: o[2], why: "esta " + o[1] })),
      x: "Veja para onde vão " + $("e_1 = (1,\\ 0)") + " e " + $("e_2 = (0,\\ 1)") + ": eles viram as colunas da matriz. Aqui " + $("e_1 \\to " + V(cols[0])) + " e " + $("e_2 \\to " + V(cols[1])) + "." };
  } };

  // ---------------- Multiplicação de matrizes ----------------
  G.matmulij = { t: "Um elemento do produto AB", f: (R, p) => {
    const k = p.dim || R.pick([2, 3]), A = Array.from({ length: k }, () => R.vec(k, -3, 4)), B = Array.from({ length: k }, () => R.vec(k, -3, 4));
    const i = R.int(0, k - 1), j = R.int(0, k - 1), C = mm(A, B), col = B.map(r => r[j]);
    return { q: "Com " + $("A = " + M(A)) + " e " + $("B = " + M(B)) + ", quanto vale o elemento da linha " + (i + 1) + ", coluna " + (j + 1) + " de " + $("AB") + "?",
      v: C[i][j], d: { A, B, i, j },
      ops: [{ v: A[i][j] * B[i][j], why: "multiplicou elemento a elemento (Hadamard)" }, { v: dot(A[i], B[j]), why: "fez linha de A com linha de B" },
            { v: mm(B, A)[i][j], why: "calculou BA (a ordem importa)" }],
      x: "Linha " + (i + 1) + " de A com a coluna " + (j + 1) + " de B: " + $(prods(A[i], col) + " = " + n(C[i][j])) + "." };
  } };

  G.matmul2 = { t: "Produto de matrizes 2×2", f: (R, p) => {
    const A = [R.vec(2, -3, 4), R.vec(2, -3, 4)], B = [R.vec(2, -3, 4), R.vec(2, -3, 4)], C = mm(A, B);
    return { q: "Calcule " + $("AB") + " para " + $("A = " + M(A)) + " e " + $("B = " + M(B)) + ".", v: C, d: { A, B },
      ops: [{ v: had(A, B), why: "multiplicou elemento a elemento" }, { v: mm(B, A), why: "calculou BA" }, { v: mm(A, tr(B)), why: "fez linha com linha" }],
      x: "Cada elemento é linha de A com coluna de B:" + li([0, 1].flatMap(i => [0, 1].map(j => $("c_{" + (i + 1) + (j + 1) + "} = " + prods(A[i], [B[0][j], B[1][j]]) + " = " + n(C[i][j]))))) };
  } };

  G.hada = { t: "Produto elemento a elemento (Hadamard)", f: (R, p) => {
    const A = [R.vec(2, -3, 4), R.vec(2, -3, 4)], B = [R.vec(2, -3, 4), R.vec(2, -3, 4)], H = had(A, B);
    return { q: "Calcule " + $("A \\odot B") + " (o <code>A * B</code> do NumPy) para " + $("A = " + M(A)) + " e " + $("B = " + M(B)) + ".", v: H, d: { A, B },
      ops: [{ v: mm(A, B), why: "fez o produto de matrizes (A @ B)" }, { v: A.map((r, i) => r.map((x, j) => x + B[i][j])), why: "somou" },
            { v: had(A, tr(B)), why: "transpôs B sem querer" }],
      x: "Cada posição vezes a mesma posição: " + $(M(A.map((r, i) => r.map((x, j) => P(x) + "\\cdot " + P(B[i][j])))) + " = " + M(H)) + "." };
  } };

  G.forma = { t: "Shape de um produto (A @ W)", f: (R, p) => {
    const DIMS = [3, 10, 16, 64, 128], m = R.pick([2, 8, 32, 64, 100]), k1 = R.pick(DIMS), c = R.pick([1, 2, 5, 10, 256]);
    const bate = R.rnd() < 0.75, k2 = bate ? k1 : R.pick(DIMS.filter(x => x !== k1));
    const sh = (a, b) => "<code>(" + a + ", " + b + ")</code>";
    const fmt = v => (v === "erro" ? "Dá erro: as dimensões não batem" : sh(...String(v).split("x")));
    const mais = [{ v: k1 + "x" + k2, why: "juntou as dimensões de dentro" }, { v: m + "x" + k1, why: "copiou o shape de A" },
                  { v: k2 + "x" + c, why: "copiou o shape de W" }, { v: c + "x" + m, why: "inverteu a ordem" }, { v: m + "x" + m, why: "repetiu as linhas de A" }];
    const ops = (bate ? [{ v: "erro", why: "as dimensões de dentro (" + k1 + " e " + k2 + ") batem" }]
                      : [{ v: m + "x" + c, why: "só olhou as pontas: as de dentro (" + k1 + " e " + k2 + ") não batem" }]).concat(mais);
    return { q: "No NumPy, <code>A</code> tem shape " + sh(m, k1) + " e <code>W</code> tem shape " + sh(k2, c) + ". Qual é o shape de <code>A @ W</code>?",
      v: bate ? m + "x" + c : "erro", fmt, d: { a: [m, k1], w: [k2, c] }, ops,
      x: bate ? "As dimensões de dentro batem (" + k1 + " com " + k2 + ") e somem; ficam as de fora: " + sh(m, c) + "."
              : "Para multiplicar, o nº de colunas de A (" + k1 + ") tem que ser igual ao nº de linhas de W (" + k2 + "). Não é, então o NumPy dá <code>ValueError</code>." };
  } };

  // ---------------- Sistemas e determinantes ----------------
  G.det2 = { t: "Determinante 2×2", f: (R, p) => {
    const A = [R.vec(2, -6, 6), R.vec(2, -6, 6)], [[a, b], [c, d]] = A, det = a * d - b * c;
    return { q: "Calcule " + $("\\det A") + " para " + $("A = " + M(A)) + ".", v: det, d: { A },
      ops: [{ v: a * d + b * c, why: "somou os produtos das diagonais" }, { v: b * c - a * d, why: "subtraiu na ordem errada" }, { v: a * b - c * d, why: "multiplicou as linhas, não as diagonais" }],
      x: $("\\det A = ad - bc = " + P(a) + "\\cdot " + P(d) + " - " + P(b) + "\\cdot " + P(c) + " = " + n(a * d) + " - " + P(b * c) + " = " + n(det)) + "." };
  } };

  G.det3 = { t: "Determinante 3×3 (Sarrus)", f: (R, p) => {
    const A = Array.from({ length: 3 }, () => R.vec(3, -2, 3)), [[a, b, c], [d, e, f], [g, h, i]] = A;
    const pos = [a * e * i, b * f * g, c * d * h], neg = [c * e * g, a * f * h, b * d * i], det = sum(pos) - sum(neg);
    return { q: "Calcule " + $("\\det A") + " para " + $("A = " + M(A)) + " (regra de Sarrus).", v: det, d: { A },
      ops: [{ v: a * e * i, why: "multiplicou só a diagonal principal" }, { v: sum(pos), why: "esqueceu os três termos que subtraem" }, { v: sum(pos) + sum(neg), why: "somou os termos que deviam subtrair" }],
      x: "Sarrus: as três diagonais que descem menos as três que sobem. " + $("(" + pos.map(P).join(" + ") + ") - (" + neg.map(P).join(" + ") + ") = " + n(sum(pos)) + " - " + P(sum(neg)) + " = " + n(det)) + "." };
  } };

  G.sist2 = { t: "Sistema 2×2", f: (R, p) => {
    let a, b, c, d; do { a = R.int(-4, 4); b = R.int(-4, 4); c = R.int(-4, 4); d = R.int(-4, 4); } while (a * d - b * c === 0 || !a || !b || (!c && !d));
    const x = R.int(-5, 5), y = R.int(-5, 5), e = a * x + b * y, f = c * x + d * y;
    const eq = (p1, p2, rhs) => lin([p1, p2], ["x", "y"]) + " = " + n(rhs);
    const subst = (p1, p2) => P(p1) + "\\cdot " + P(x) + " + " + P(p2) + "\\cdot " + P(y);
    return { q: "Resolva o sistema " + $("\\begin{cases} " + eq(a, b, e) + " \\\\ " + eq(c, d, f) + " \\end{cases}"),
      v: [x, y], fmt: v => par(v[0], v[1], "x", "y"), d: { A: [[a, b], [c, d]], b: [e, f] },
      ops: [{ v: [y, x], why: "trocou x e y" }, { v: [-x, y], why: "errou o sinal de x" }, { v: [x + b, y - a], why: "serve só na 1ª equação" }],
      x: "Um caminho: isole uma variável numa equação e substitua na outra. Confira " + par(x, y, "x", "y") + " nas duas: " +
         $(subst(a, b) + " = " + n(e)) + " ✓ e " + $(subst(c, d) + " = " + n(f)) + " ✓." };
  } };

  G.detarea = { t: "Determinante e área", f: (R, p) => {
    let A; do { A = [R.vec(2, -4, 5), R.vec(2, -4, 5)]; } while (A[0][0] * A[1][1] - A[0][1] * A[1][0] === 0);
    const [[a, b], [c, d]] = A, det = a * d - b * c;
    return { q: "Um quadrado de área 1 passa pela transformação " + $("A = " + M(A)) + ". Qual é a área da figura que sai?", v: Math.abs(det), d: { A },
      ops: [{ v: det, why: "área não é negativa: use o módulo do det" }, { v: a + d, why: "somou a diagonal (isso é o traço)" }, { v: Math.abs(a * d + b * c), why: "somou os produtos das diagonais" }],
      x: $("\\det A = " + P(a) + "\\cdot " + P(d) + " - " + P(b) + "\\cdot " + P(c) + " = " + n(det)) + ". A área é multiplicada por " + $("|\\det A| = " + n(Math.abs(det))) +
         (det < 0 ? " (o sinal negativo só diz que a figura foi espelhada)." : ".") };
  } };

  G.detsing = { t: "Quando a matriz não tem inversa", f: (R, p) => {
    const a = R.pick([1, 2, 3, -1, -2]), k = R.nz(-4, 4), c = R.nz(-4, 4), b = a * k, sol = k * c;
    return { q: "Para qual valor de " + $("t") + " a matriz " + $(M([[a, b], [c, "t"]])) + " não tem inversa?", v: sol, d: { a, b, c },
      ops: [{ v: -sol, why: "errou o sinal" }, { v: b * c, why: "esqueceu de dividir por " + nt(a) }, { v: 0, why: "achou que t = 0 zera o determinante" }],
      x: "Não tem inversa quando " + $("\\det = 0") + ": " + $(n(a) + "t - " + P(b) + "\\cdot " + P(c) + " = 0") + ", então " + $("t = \\dfrac{" + n(b * c) + "}{" + n(a) + "} = " + n(sol)) + "." };
  } };

  // ---------------- Inversa ----------------
  G.inv2 = { t: "Inversa 2×2", f: (R, p) => {
    let A = mm(mm([[1, R.int(-2, 2)], [0, 1]], [[R.pick([1, 1, -1, 2]), 0], [0, 1]]), [[1, 0], [R.int(-2, 2), 1]]);   // det 1, -1 ou 2
    if (R.rnd() < 0.4) A = A.map(r => [r[1], r[0]]);
    const [[a, b], [c, d]] = A, det = a * d - b * c, inv = [[d / det, -b / det], [-c / det, a / det]];
    return { q: "Calcule " + $("A^{-1}") + " para " + $("A = " + M(A)) + ".", v: inv, d: { A },
      ops: [{ v: [[d, -b], [-c, a]], why: "esqueceu de dividir pelo det" }, { v: [[d / det, b / det], [c / det, a / det]], why: "trocou a diagonal, mas esqueceu os sinais" },
            { v: [[a / det, -b / det], [-c / det, d / det]], why: "trocou os sinais, mas não a diagonal" }, { v: [[-d / det, b / det], [c / det, -a / det]], why: "errou o sinal de tudo" }],
      x: "Na 2×2: troque " + $("a") + " e " + $("d") + " de lugar, troque o sinal de " + $("b") + " e " + $("c") + " e divida pelo det. " +
         $("\\det A = " + n(det)) + ", então " + $("A^{-1} = \\dfrac{1}{" + n(det) + "}" + M([[d, -b], [-c, a]]) + " = " + M(inv)) + "." };
  } };

  G.invdiag = { t: "Inversa de matriz diagonal", f: (R, p) => {
    const vals = R.shuffle([2, 4, 5, 10, -2, -4, -5]).slice(0, R.pick([2, 3]));
    const D = vals.map((x, i) => vals.map((_, j) => (i === j ? x : 0))), inv = D.map((r, i) => r.map((x, j) => (i === j ? 1 / x : 0)));
    return { q: "Calcule a inversa de " + $("D = " + M(D)) + ".", v: inv, d: { D },
      ops: [{ v: D.map(r => r.map(x => -x)), why: "só trocou os sinais" }, { v: inv.map(r => r.map(x => -x)), why: "inverteu e também trocou os sinais" }, { v: D, why: "achou que a diagonal não muda" }],
      x: "Na diagonal, a inversa só inverte cada número: " + vals.map(x => $("\\tfrac{1}{" + n(x) + "} = " + n(1 / x))).join(", ") + ". Confira: " + $("D\\,D^{-1} = I") + "." };
  } };

  G.axb = { t: "Resolver Ax = b com a inversa", f: (R, p) => {
    let A = mm([[1, R.int(-2, 2)], [0, 1]], [[1, 0], [R.int(-2, 2), 1]]);   // det 1: inversa inteira
    if (R.rnd() < 0.5) A = A.map(r => [r[1], r[0]]);
    const x = R.vec(2, -4, 4), b = mv(A, x), [[a, bb], [c, d]] = A, det = a * d - bb * c, inv = [[d / det, -bb / det], [-c / det, a / det]];
    return { q: "Resolva " + $("A\\,x = b") + " para " + $("A = " + M(A)) + " e " + $("b = " + V(b)) + ".", v: x, d: { A, b },
      ops: [{ v: mv(A, b), why: "multiplicou b por A em vez de A⁻¹" }, { v: b.slice(), why: "achou que x = b" }, { v: [x[1], x[0]], why: "trocou as coordenadas" }],
      x: $("A^{-1} = " + M(inv)) + " e " + $("x = A^{-1} b = " + V(x)) + ". Confira: " + $("A\\,x = " + V(mv(A, x))) + "." };
  } };

  // ---------------- Autovalores e autovetores ----------------
  G.eigtri = { t: "Autovalores de matriz triangular", f: (R, p) => {
    let a, d; do { a = R.int(-5, 6); d = R.int(-5, 6); } while (a === d);
    const b = R.nz(-5, 5), A = R.rnd() < 0.6 ? [[a, b], [0, d]] : [[a, 0], [b, d]];
    return { q: "Quais são os autovalores de " + $("A = " + M(A)) + "?", v: [Math.min(a, d), Math.max(a, d)], fmt: lamPair, d: { A },
      ops: [{ v: [a, b], why: "pegou números fora da diagonal" }, { v: [a + d, a * d], why: "calculou o traço e o det" }, { v: [-a, -d], why: "errou o sinal" }],
      x: "Em matriz triangular, os autovalores são os números da diagonal: " + lamPair([a, d]) + ". Confira: " + $("\\det(A - \\lambda I) = (" + n(a) + " - \\lambda)(" + n(d) + " - \\lambda)") + ", que zera nesses dois valores." };
  } };

  G.eigtd = { t: "Autovalores pelo traço e o determinante", f: (R, p) => {
    let l1, l2; do { l1 = R.int(-4, 7); l2 = R.int(-4, 7); } while (l1 === l2);
    const T = l1 + l2, D = l1 * l2;
    const poly = "\\lambda^2" + (T ? (T > 0 ? " - " : " + ") + (Math.abs(T) === 1 ? "" : n(Math.abs(T))) + "\\lambda" : "") + (D ? (D > 0 ? " + " : " - ") + n(Math.abs(D)) : "") + " = 0";
    return { q: "Uma matriz 2×2 tem traço " + $(n(T)) + " e determinante " + $(n(D)) + ". Quais são os autovalores?", v: [Math.min(l1, l2), Math.max(l1, l2)], fmt: lamPair, d: { T, D },
      ops: [{ v: [T, D], why: "usou o traço e o det como se fossem os autovalores" }, { v: [-l1, -l2], why: "errou o sinal" }, { v: [l1 + 1, l2 - 1], why: "a soma bate, mas o produto não" }],
      x: "Os autovalores somam o traço e multiplicam o det, então são as raízes de " + $(poly) + ": " + lamPair([l1, l2]) + ". Confira: " +
         $(n(l1) + " + " + P(l2) + " = " + n(T)) + " e " + $(n(l1) + "\\cdot " + P(l2) + " = " + n(D)) + "." };
  } };

  G.eigvec = { t: "É autovetor? Qual o autovalor?", f: (R, p) => {
    const v = R.pick([[1, 1], [1, -1], [1, 2], [2, 1]]), lam = R.nz(-4, 5), eig = R.rnd() < 0.7;
    const row = t => { for (let k = 0; k < 200; k++) { const r0 = R.int(-4, 5), rest = t - r0 * v[0]; if (rest % v[1] === 0 && Math.abs(rest / v[1]) <= 9) return [r0, rest / v[1]]; } return null; };
    const paralelo = w => w[0] * v[1] === w[1] * v[0];
    let A = null;
    if (eig) { const l1 = row(lam * v[0]), l2 = row(lam * v[1]); if (l1 && l2) A = [l1, l2]; }   // linhas com A·v = λ·v
    if (!A) do { A = [R.vec(2, -4, 5), R.vec(2, -4, 5)]; } while (paralelo(mv(A, v)));             // ou uma A qualquer em que v não é autovetor
    const w = mv(A, v), par1 = paralelo(w), L = par1 ? w[0] / v[0] : null;
    const fmt = x => (x === "nao" ? "Não é autovetor" : "Sim, com " + $("\\lambda = " + n(x)));
    const ops = par1
      ? [{ v: "nao", why: "Av ficou na mesma direção de v" }, { v: A[0][0], why: "pegou o 1º número de A" }, { v: -L, why: "errou o sinal" }, { v: w[0], why: "não dividiu pela coordenada de v" }]
      : [{ v: r2(w[0] / v[0]), why: "dividiu só a 1ª coordenada" }, { v: A[0][0], why: "pegou o 1º número de A" }, { v: A[0][0] + A[1][1], why: "usou o traço" },
         { v: r2(w[1] / v[1]), why: "dividiu só a 2ª coordenada" }, { v: A[1][1], why: "pegou o último número de A" }, { v: 1, why: "chutou λ = 1" }, { v: -1, why: "chutou λ = −1" }];
    return { q: "Seja " + $("A = " + M(A)) + ". O vetor " + $("v = " + V(v)) + " é autovetor de A? Se for, com qual autovalor?", v: par1 ? L : "nao", fmt, d: { A, v },
      ops, x: "Calcule " + $("A\\,v = " + V(w)) + ". " + (par1 ? "Isso é " + $(n(L) + "\\cdot " + V(v)) + ": mesma direção de v, então é autovetor com " + $("\\lambda = " + n(L)) + "."
        : "Não existe um número que vezes " + $(V(v)) + " dê " + $(V(w)) + ", então v não é autovetor.") };
  } };

  G.eigpot = { t: "Potência de matriz num autovetor", f: (R, p) => {
    const lam = R.pick([-3, -2, 2, 3, 4]), v = R.vec(2, -3, 3).map(x => x || 1), k = R.pick([2, 2, 3]), lk = Math.pow(lam, k);
    return { q: "Sabendo que " + $("A\\,v = " + n(lam) + "\\,v") + " para " + $("v = " + V(v)) + ", quanto vale " + $("A^{" + k + "}\\,v") + "?", v: mul(lk, v), d: { lam, v, k },
      ops: [{ v: mul(lam, v), why: "aplicou A uma vez só" }, { v: mul(k * lam, v), why: "multiplicou λ por " + k + " em vez de elevar" }, { v: lk, why: "esqueceu o vetor (ficou só o número)" }],
      x: "Cada vez que A age em v, ele é multiplicado por " + $(n(lam)) + ": " + $("A^{" + k + "} v = " + P(lam) + "^{" + k + "}\\,v = " + n(lk) + "\\cdot " + V(v) + " = " + V(mul(lk, v))) + "." };
  } };

  // ---------------- SVD e PCA ----------------
  const pctF = x => $(n(x, 1) + "\\%");
  G.varexp = { t: "Variância explicada pelos autovalores", f: (R, p) => {
    const S = R.pick([10, 20, 25, 40, 50]);
    let l; do { const a = R.int(Math.ceil(S * 0.35), Math.floor(S * 0.8)), b = R.int(1, Math.max(1, S - a - 1)); l = [a, b, S - a - b].sort((x, y) => y - x); } while (l[2] <= 0 || l[0] === l[1] || l[1] === l[2]);
    const pct = 100 * l[0] / S;
    return { q: "A PCA achou os autovalores da covariância " + $("\\lambda = " + l.map(N1).join(",\\ ")) + ". Que porcentagem da variância a 1ª componente explica?",
      v: pct, fmt: pctF, d: { l },
      ops: [{ v: 100 * l[0] / l[1], why: "dividiu pelo 2º autovalor" }, { v: 100 * l[0] / (l[0] + l[1]), why: "esqueceu a 3ª componente" }, { v: l[0], why: "usou o autovalor direto como porcentagem" }],
      x: "1º autovalor dividido pela soma de todos: " + $("\\dfrac{" + n(l[0]) + "}{" + l.map(N1).join(" + ") + "} = \\dfrac{" + n(l[0]) + "}{" + n(S) + "} = " + n(pct, 1) + "\\%") + "." };
  } };

  const SV = [[4, 3], [5, 4, 3], [7, 1], [6, 3, 2, 1], [5, 4, 2, 2, 1], [9, 4, 1, 1, 1], [7, 5, 4, 3, 1], [8, 4, 4, 2], [6, 6, 4, 2, 2, 2]];
  G.varsing = { t: "Variância explicada pelos valores singulares", f: (R, p) => {
    const s = R.pick(SV), sq = s.map(x => x * x), S2 = sum(sq), pct = 100 * sq[0] / S2;
    return { q: "A SVD dos dados (já centralizados) deu os valores singulares " + $("\\sigma = " + s.map(N1).join(",\\ ")) + ". Que porcentagem da variância a 1ª componente explica?",
      v: pct, fmt: pctF, d: { s },
      ops: [{ v: 100 * s[0] / sum(s), why: "usou σ sem elevar ao quadrado" }, { v: 100 * sq[0] / (sum(s) * sum(s)), why: "elevou a soma ao quadrado" }, { v: 100 * s[0] / S2, why: "esqueceu de elevar o σ₁" }],
      x: "A variância de cada componente é proporcional a " + $("\\sigma^2") + ": " + $("\\dfrac{" + n(s[0]) + "^2}{" + s.map(x => n(x) + "^2").join(" + ") + "} = \\dfrac{" + n(sq[0]) + "}{" + n(S2) + "} = " + n(pct, 1) + "\\%") + "." };
  } };

  G.ncomp = { t: "Quantas componentes manter", f: (R, p) => {
    const meta = R.pick([80, 90, 95]);
    let l, k, cum;
    do {
      l = Array.from({ length: R.int(4, 6) }, () => R.int(1, 12)).sort((a, b) => b - a);
      const S = sum(l); let acc = 0; cum = l.map(x => (acc += x, 100 * acc / S));
      k = cum.findIndex(c => c >= meta - 1e-9) + 1;
    } while (k < 2 || cum.some(c => Math.abs(c - meta) < 0.05));   // nada de empate na meta
    const cand = [...new Set([k - 1, k + 1, k + 2, l.length, 1, 2])].filter(x => x >= 1 && x <= l.length && x !== k);
    return { q: "Os autovalores da covariância são " + $(l.map(N1).join(",\\ ")) + ". Qual é o menor número de componentes que explica pelo menos " + meta + "% da variância?",
      v: k, fmt: x => x + (x === 1 ? " componente" : " componentes"), d: { l, meta },
      ops: cand.slice(0, 3).map(x => ({ v: x, why: x < k ? "ainda não chega a " + meta + "%" : "passa do necessário" })),
      x: "Some do maior para o menor e veja o acumulado: " + cum.map((c, i) => (i + 1) + " → " + nt(c, 1) + "%").join(" · ") + ". A meta de " + meta + "% chega com " + k + "." };
  } };

  G.svdshape = { t: "Shapes da SVD no NumPy", f: (R, p) => {
    const m = R.pick([30, 50, 100, 200]), k = R.pick([5, 10, 20]), full = R.rnd() < 0.5, what = R.pick(["U", "S", "Vt"]);
    const sh = a => "<code>(" + a.join(", ") + (a.length === 1 ? "," : "") + ")</code>";
    const ans = what === "U" ? (full ? [m, m] : [m, k]) : what === "S" ? [k] : [k, k];
    const pool = [[m, m], [m, k], [k, k], [k], [m], [k, m]].filter(a => a.join("x") !== ans.join("x"));
    return { q: "<code>A</code> tem shape " + sh([m, k]) + " e você roda <code>U, S, Vt = np.linalg.svd(A, full_matrices=" + (full ? "True" : "False") + ")</code>. Qual é o shape de <code>" + what + "</code>?",
      v: ans.join("x"), fmt: v => sh(String(v).split("x").map(Number)), d: { m, k, full, what },
      ops: R.shuffle(pool).slice(0, 3).map(a => ({ v: a.join("x"), why: "" })),
      x: (full ? "Com <code>full_matrices=True</code>, <code>U</code> é quadrada, " + sh([m, m]) : "Com <code>full_matrices=False</code> (SVD reduzida), <code>U</code> fica " + sh([m, k])) +
         "; <code>S</code> vem como um vetor com os " + k + " valores singulares, " + sh([k]) + ", e <code>Vt</code> é " + sh([k, k]) + "." };
  } };

  G.pcaproj = { t: "Coordenada na 1ª componente (PCA)", f: (R, p) => {
    const w = R.pick([[0.6, 0.8], [0.8, 0.6], [-0.6, 0.8], [0.8, -0.6], [1, 0], [0, 1]]), mu = R.vec(2, -3, 5), x = R.vec(2, -3, 8), c = sub(x, mu), s = r2(dot(c, w));
    return { q: "Na PCA, a 1ª componente é " + $("w = " + V(w, 1)) + " e a média dos dados é " + $("\\mu = " + V(mu)) + ". Qual é a coordenada do ponto " + $("x = " + V(x)) + " nessa componente?",
      v: s, d: { w, mu, x },
      ops: [{ v: r2(dot(x, w)), why: "esqueceu de centralizar (subtrair a média)" }, { v: r2(dot(c, [w[1], w[0]])), why: "trocou as coordenadas de w" }, { v: r2(nrm(c)), why: "calculou a distância até a média" }],
      x: "Centralize e projete: " + $("x - \\mu = " + V(c)) + " e " + $("(x - \\mu)\\cdot w = " + prods(c, w) + " = " + n(s)) + "." };
  } };
  // Ferramentas compartilhadas com os outros arquivos de geradores (treino_contas_*.py)
  const milhar = x => String(Math.round(x)).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  TR.H = { n, V, M, N1, P, nt, $, dot, sum, add, sub, mul, mv, mm, tr, had, r2, nrm, prods, li, signed, dimOf, lin, par, lamPair, pctF, milhar };
})();
"""
