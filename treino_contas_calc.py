# -*- coding: utf-8 -*-
"""
Geradores de conta do Treino: Matemática, Módulo 1 do site (Fundamentos: funções, logaritmos, notação e distâncias)
e Módulo 3 (Cálculo: limites, derivadas, regra da cadeia, gradiente, descida do gradiente e otimizadores).

Mesmo formato de treino_contas.py (que define as ferramentas TR.H usadas aqui). As respostas são refeitas com o
NumPy em treino_checagem.py.
"""

TR_GEN_JS = r"""
// =================== TREINO: geradores de conta (Fundamentos e Cálculo) ===================
(() => {
  const G = TR.GEN;
  const { n, V, M, N1, P, nt, $, dot, sum, sub, mul, r2, nrm, prods, li, signed, lin } = TR.H;
  const P3 = x => (x < 0 ? "(" + n(x, 3) + ")" : n(x, 3));
  const sg = k => (k < 0 ? "- " + n(-k) : "+ " + n(k));                 // "+ 3" / "- 2"
  const aff = (a, b, v) => lin([a], [v || "x"]) + (b ? " " + sg(b) : "");   // "2x - 3"
  // polinômio em LaTeX a partir dos coeficientes (do maior grau para o menor)
  const poly = (cs, v) => {
    v = v || "x"; const g = cs.length - 1; let s = "";
    cs.forEach((c, i) => {
      if (!c) return;
      const e = g - i, ab = Math.abs(c), coef = ab === 1 && e > 0 ? "" : n(ab);
      const t = coef + (e === 0 ? "" : e === 1 ? v : v + "^{" + e + "}");
      s += s ? (c < 0 ? " - " : " + ") + t : (c < 0 ? "-" : "") + t;
    });
    return s || "0";
  };
  const pval = (cs, x) => cs.reduce((a, c) => a * x + c, 0);
  const pder = cs => cs.slice(0, -1).map((c, i) => c * (cs.length - 1 - i));
  const termo = (c, e) => (e === 0 ? n(c) : (c === 1 ? "" : c === -1 ? "-" : n(c)) + (e === 1 ? "x" : "x^{" + e + "}"));
  const sci = x => { if (x === 0) return "0"; const e = Math.floor(Math.log10(Math.abs(x))), m = x / Math.pow(10, e);
    return n(Math.round(m * 10) / 10, 1) + " \\times 10^{" + e + "}"; };
  const pick2 = (R, arr) => { const a = R.shuffle(arr); return [a[0], a[1]]; };

  // ================= Módulo 1 · Fundamentos =================
  G.linz = { t: "Pontuação de um classificador linear", f: (R, p) => {
    const w = [R.pick([-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 3]), R.pick([-2, -1, -0.5, 0.5, 1, 2, 2.5])], x = R.vec(2, -3, 5), b = R.nz(-6, 6);
    const wx = dot(w, x), z = wx + b;
    return { q: "Um classificador linear tem pesos " + $("w = " + V(w)) + " e viés " + $("b = " + n(b)) + ". Qual é a pontuação " +
             $("z = w \\cdot x + b") + " do ponto " + $("x = " + V(x)) + "?", v: z, d: { w, x, b },
      ops: [{ v: wx, why: "esqueceu de somar o viés" }, { v: wx - b, why: "subtraiu o viés" }, { v: sum(w) + sum(x) + b, why: "somou tudo em vez de multiplicar" }],
      x: $("z = " + prods(w, x) + " + " + P(b) + " = " + n(wx) + " + " + P(b) + " = " + n(z)) + "." };
  } };

  G.linlado = { t: "De que lado da fronteira fica o ponto", f: (R, p) => {
    let w, x, b, z;
    do { w = [R.nz(-3, 3), R.nz(-3, 3)]; x = R.vec(2, -4, 4); b = R.nz(-5, 5); z = dot(w, x) + b; } while (Math.abs(z) > 12 || dot(w, x) === 0);
    const fmt = v => (v > 0 ? "Classe positiva: " + $("z = " + n(v) + " > 0") : v < 0 ? "Classe negativa: " + $("z = " + n(v) + " < 0") : "Em cima da fronteira: " + $("z = 0"));
    return { q: "A fronteira de decisão é " + $(lin(w, ["x_1", "x_2"]) + " " + sg(b) + " = 0") + ". Onde fica o ponto " + $("x = " + V(x)) + "?", v: z, fmt, d: { w, x, b },
      ops: [{ v: dot(w, x), why: "esqueceu o viés" }, { v: -z, why: "errou o sinal na conta" }, { v: dot(w, x) - b, why: "subtraiu o viés" }],
      x: $("z = " + prods(w, x) + " + " + P(b) + " = " + n(z)) + ". " + (z > 0 ? "Positivo: o ponto fica do lado para onde w aponta."
         : z < 0 ? "Negativo: o ponto fica do lado oposto ao de w." : "Zero: o ponto está exatamente na fronteira.") };
  } };

  G.distplano = { t: "Distância até a fronteira", f: (R, p) => {
    const w = signed(R, R.pick([[3, 4], [4, 3], [6, 8], [8, 6], [5, 12], [12, 5]])), L = nrm(w);
    let x, b, z; do { x = R.vec(2, -3, 4); b = R.int(-10, 10); z = dot(w, x) + b; } while (z === 0);
    const d = Math.abs(z) / L;
    return { q: "Qual é a distância do ponto " + $("x = " + V(x)) + " até a reta " + $(lin(w, ["x_1", "x_2"]) + (b ? " " + sg(b) : "") + " = 0") +
             "? Use " + $("d = \\dfrac{|w \\cdot x + b|}{\\lVert w \\rVert}") + ".", v: d, d: { w, x, b },
      ops: [{ v: Math.abs(z), why: "esqueceu de dividir por ‖w‖" }, { v: Math.abs(z) / (L * L), why: "dividiu por ‖w‖²" }, { v: Math.abs(dot(w, x)) / L, why: "esqueceu o viés" }],
      x: $("w \\cdot x + b = " + prods(w, x) + " + " + P(b) + " = " + n(z)) + " e " + $("\\lVert w \\rVert = " + n(L)) + ", então " +
         $("d = \\dfrac{" + n(Math.abs(z)) + "}{" + n(L) + "} \\approx " + n(d)) + "." };
  } };

  G.inequa = { t: "Inequação do 1º grau", f: (R, p) => {
    const a = R.pick([-4, -3, -2, 2, 3, 4]), k = R.nz(-5, 5), b = R.nz(-9, 9), op = R.pick([">", "<", "\\geq", "\\leq"]), c = a * k + b;
    const flip = { ">": "<", "<": ">", "\\geq": "\\leq", "\\leq": "\\geq" }, res = a > 0 ? op : flip[op];
    const fmt = v => { const [o, kk] = String(v).split("|"); return $("x " + o + " " + n(+kk)); };
    return { q: "Resolva " + $(n(a) + "x " + sg(b) + " " + op + " " + n(c)) + ".", v: res + "|" + k, fmt, d: { a, b, c, op },
      ops: [{ v: (a > 0 ? flip[op] : op) + "|" + k, why: a < 0 ? "esqueceu de inverter a desigualdade ao dividir por negativo" : "inverteu sem precisar" },
            { v: res + "|" + (-k), why: "errou o sinal ao isolar x" }, { v: res + "|" + r2((c + b) / a), why: "somou o " + nt(b) + " em vez de subtrair" },
            { v: (a > 0 ? flip[op] : op) + "|" + (-k), why: "errou o sinal e o sentido da desigualdade" }, { v: res + "|" + (c - b), why: "esqueceu de dividir por " + nt(a) }],
      x: "Passe o " + $(n(b)) + " para o outro lado: " + $(n(a) + "x " + op + " " + n(c - b)) + ". Divida por " + $(n(a)) +
         (a < 0 ? " e, como é negativo, <b>inverta</b> a desigualdade" : "") + ": " + $("x " + res + " " + n(k)) + "." };
  } };

  G.logprop = { t: "Propriedades do logaritmo", f: (R, p) => {
    const m = R.int(1, 6), k = R.int(1, 5), tipo = R.pick(["prod", "div", "pot"]), a = Math.pow(2, m), b = Math.pow(2, k);
    if (tipo === "prod") return { q: "Quanto vale " + $("\\log_2(" + a + " \\cdot " + b + ")") + "?", v: m + k, d: { tipo, a, b, k },
      ops: [{ v: m * k, why: "multiplicou os logaritmos" }, { v: r2(Math.log2(a + b)), why: "somou os números antes do log" }, { v: a * b, why: "esqueceu o logaritmo" }],
      x: "Log de produto vira soma: " + $("\\log_2 " + a + " + \\log_2 " + b + " = " + m + " + " + k + " = " + (m + k)) + "." };
    if (tipo === "div") return { q: "Quanto vale " + $("\\log_2\\left(\\dfrac{" + a + "}{" + b + "}\\right)") + "?", v: m - k, d: { tipo, a, b, k },
      ops: [{ v: r2(m / k), why: "dividiu os logaritmos" }, { v: m + k, why: "somou em vez de subtrair" }, { v: k - m, why: "subtraiu na ordem errada" }],
      x: "Log de divisão vira subtração: " + $("\\log_2 " + a + " - \\log_2 " + b + " = " + m + " - " + k + " = " + (m - k)) + "." };
    return { q: "Quanto vale " + $("\\log_2(" + a + "^{" + k + "})") + "?", v: m * k, d: { tipo, a, b, k },
      ops: [{ v: m + k, why: "somou o expoente em vez de multiplicar" }, { v: Math.pow(m, k), why: "elevou o log ao expoente" }, { v: m, why: "ignorou o expoente" }],
      x: "O expoente sai multiplicando: " + $(k + "\\cdot \\log_2 " + a + " = " + k + "\\cdot " + m + " = " + (m * k)) + "." };
  } };

  G.logeq = { t: "Equação exponencial", f: (R, p) => {
    const c = R.pick([1, 2, 3, 5]), k = R.int(2, 7), rhs = c * Math.pow(2, k);
    return { q: "Resolva " + $((c === 1 ? "" : n(c) + "\\cdot ") + "2^x = " + n(rhs)) + ".", v: k, d: { c, rhs },
      ops: [{ v: rhs / c / 2, why: "dividiu por 2 em vez de usar o log" }, { v: r2(Math.log2(rhs)), why: "esqueceu de dividir por " + c + " antes" },
            { v: Math.pow(2, k), why: "achou o valor de 2ˣ, não o x" }],
      x: (c === 1 ? "" : "Divida por " + c + ": " + $("2^x = " + n(rhs / c)) + ". ") + "Aplique " + $("\\log_2") + ": " + $("x = \\log_2 " + n(rhs / c) + " = " + k) + "." };
  } };

  G.lse = { t: "LogSumExp sem estourar", f: (R, p) => {
    const a = R.pick([100, 500, 1000, 2000]), k = R.pick([2, 4, 8, 10]), val = a + Math.log(k);
    return { q: "Os " + k + " logits valem todos " + $(n(a)) + ". Quanto dá " + $("\\ln \\sum_i e^{z_i}") + "? (Calcular " + $("e^{" + a + "}") +
             " direto estoura o float.)", v: val, d: { a, k },
      ops: [{ v: k * a, why: "somou os expoentes" }, { v: a, why: "ignorou a soma" }, { v: a * Math.log(k), why: "multiplicou por ln k em vez de somar" }],
      x: "Tire o máximo " + $("m = " + a) + " de dentro da soma: " + $("\\ln \\sum e^{z_i} = m + \\ln \\sum e^{z_i - m} = " + a + " + \\ln " + k + " \\approx " + n(val)) + "." };
  } };

  G.expdecay = { t: "Decaimento exponencial", f: (R, p) => {
    const L0 = R.pick([4, 8, 16, 32, 64]), t = R.int(2, 4), Lt = L0 * Math.pow(0.5, t);
    return { q: "A cada época, a perda cai pela metade: " + $("L_t = L_0 \\cdot 0{,}5^t") + ". Com " + $("L_0 = " + L0) + ", quanto vale " + $("L_" + t) + "?",
      v: Lt, casas: 3, d: { L0, t },
      ops: [{ v: L0 - 0.5 * t, why: "subtraiu 0,5 por época (queda linear)" }, { v: L0 * 0.5 * t, why: "multiplicou 0,5 por t em vez de elevar" }, { v: L0 / Math.pow(2, t - 1), why: "contou uma época a menos" }],
      x: $("L_" + t + " = " + L0 + " \\cdot 0{,}5^{" + t + "} = " + L0 + " \\cdot " + n(Math.pow(0.5, t), 4) + " = " + n(Lt, 3)) + "." };
  } };

  G.soma = { t: "Somatório", f: (R, p) => {
    const a = R.nz(-3, 4), b = R.nz(-5, 5), N = R.int(3, 6), termos = [];
    for (let i = 1; i <= N; i++) termos.push(a * i + b);
    const s = sum(termos);
    return { q: "Calcule " + $("\\sum_{i=1}^{" + N + "} (" + aff(a, b, "i") + ")") + ".", v: s, d: { a, b, N },
      ops: [{ v: s - termos[N - 1], why: "parou em i = " + (N - 1) + ", mas o último índice entra" }, { v: a * N * (N + 1) / 2 + b, why: "somou o " + nt(b) + " uma vez só" },
            { v: s + b, why: "começou em i = 0" }],
      x: "Some os termos de " + $("i = 1") + " até " + $(String(N)) + ": " + $(termos.map(P).join(" + ") + " = " + n(s)) + "." };
  } };

  G.prod = { t: "Produtório", f: (R, p) => {
    const k = R.int(3, 4), x = Array.from({ length: k }, () => R.pick([-3, -2, -1, 2, 3, 4, 0.5])), pr = x.reduce((a, b) => a * b, 1);
    return { q: "Calcule " + $("\\prod_{i=1}^{" + k + "} x_i") + " para " + $("x = " + V(x)) + ".", v: pr, casas: 3, d: { x },
      ops: [{ v: sum(x), why: "somou em vez de multiplicar" }, { v: pr / x[k - 1], why: "esqueceu o último termo" }, { v: Math.abs(pr), why: "ignorou os sinais" }],
      x: "Multiplique todos: " + $(x.map(P).join(" \\cdot ") + " = " + n(pr, 3)) + "." };
  } };

  G.argmax = { t: "arg max", f: (R, p) => {
    let x; do { x = R.vec(R.int(4, 6), -5, 12); } while (x.filter(v => v === Math.max(...x)).length > 1 || x.filter(v => v === Math.min(...x)).length > 1);
    const mx = Math.max(...x), i = x.indexOf(mx) + 1, imin = x.indexOf(Math.min(...x)) + 1;
    const fmt = v => (String(v).startsWith("val:") ? $(n(+String(v).slice(4))) + " (o valor)" : $("i = " + v));
    return { q: "Para " + $("x = " + V(x)) + ", quanto vale " + $("\\arg\\max_i\\, x_i") + " (posições contadas a partir de 1)?", v: i, fmt, d: { x },
      ops: [{ v: "val:" + mx, why: "deu o maior valor, não a posição" }, { v: i - 1, why: "contou a partir do zero" }, { v: imin, why: "pegou a posição do menor (arg min)" }],
      x: "O maior valor é " + $(n(mx)) + ", na posição " + $(String(i)) + ". O " + $("\\arg\\max") + " devolve a posição, não o valor (no NumPy, " +
         "<code>np.argmax</code> daria " + (i - 1) + ", porque conta do zero)." };
  } };

  G.indic = { t: "Acurácia com a função indicadora", f: (R, p) => {
    const N = R.pick([4, 5, 8, 10]), y = R.vec(N, 0, 2);
    let yh, hits; do { yh = y.map(v => (R.rnd() < 0.65 ? v : (v + R.int(1, 2)) % 3)); hits = y.filter((v, i) => v === yh[i]).length; } while (hits === 0 || hits === N);
    const acc = hits / N;
    return { q: "Rótulos " + $("y = " + V(y)) + " e previsões " + $("\\hat y = " + V(yh)) + ". Quanto vale " + $("\\frac{1}{N}\\sum_{i=1}^{N} \\mathbb{I}[y_i = \\hat y_i]") + "?",
      v: acc, casas: 3, d: { y, yh },
      ops: [{ v: hits, why: "contou os acertos e não dividiu por N" }, { v: 1 - acc, why: "calculou a taxa de erro" }, { v: hits / (N - 1), why: "dividiu por N − 1" }],
      x: "A indicadora vale 1 onde acertou: " + $(y.map((v, i) => (v === yh[i] ? "1" : "0")).join(" + ") + " = " + hits) + ". Dividindo por " +
         $("N = " + N) + ": " + $(n(acc, 3)) + " (é a acurácia)." };
  } };

  G.knn = { t: "Vizinho mais próximo", f: (R, p) => {
    const metr = R.pick(["euclidiana", "Manhattan"]), dE = (a, b) => nrm(sub(a, b)), dM = (a, b) => sum(sub(a, b).map(Math.abs));
    const dist = metr === "euclidiana" ? dE : dM, outra = metr === "euclidiana" ? dM : dE, nomes = ["A", "B", "C"];
    let q, Pt, ds; do { q = R.vec(2, 0, 6); Pt = [R.vec(2, 0, 8), R.vec(2, 0, 8), R.vec(2, 0, 8)]; ds = Pt.map(x => dist(q, x)); }
    while (new Set(ds.map(r2)).size < 3 || Pt.some(x => x[0] === q[0] && x[1] === q[1]));
    const best = ds.indexOf(Math.min(...ds)), dsO = Pt.map(x => outra(q, x)), bestO = dsO.indexOf(Math.min(...dsO));
    const fmt = v => (v === "empate" ? "Há empate entre dois pontos" : "Ponto " + v);
    return { q: "Pela distância " + metr + ", qual é o vizinho mais próximo de " + $("q = " + V(q)) + "? " + nomes.map((nm, i) => $(nm + " = " + V(Pt[i]))).join(", ") + ".",
      v: nomes[best], fmt, d: { q, P: Pt, metr },
      ops: nomes.filter((_, i) => i !== best).map(nm => ({ v: nm, why: nomes.indexOf(nm) === bestO ? "é o mais perto pela outra distância" : "" })).concat([{ v: "empate", why: "" }]),
      x: "Distâncias " + metr + " até q: " + nomes.map((nm, i) => nm + " = " + $(n(ds[i]))).join(", ") + ". O menor é " + nomes[best] + "." +
         (bestO !== best ? " Pela outra distância, o mais perto seria " + nomes[bestO] + ": a escolha da métrica muda o vizinho." : "") };
  } };

  // ================= Módulo 3 · Cálculo =================
  G.secante = { t: "Inclinação da secante", f: (R, p) => {
    const a = R.pick([1, 2, 3, -1, 0.5]), x0 = R.int(-2, 3), h = R.pick([1, 0.5, 0.1]), f = x => a * x * x, m = (f(x0 + h) - f(x0)) / h;
    return { q: "Para " + $("f(x) = " + termo(a, 2)) + ", qual é a inclinação da secante entre " + $("x = " + n(x0)) + " e " + $("x = " + n(x0 + h)) + "? Use " +
             $("\\dfrac{f(x+h) - f(x)}{h}") + ".", v: m, casas: 3, d: { a, x0, h },
      ops: [{ v: 2 * a * x0, why: "calculou a derivada (a tangente), não a secante" }, { v: f(x0 + h) - f(x0), why: "esqueceu de dividir por h" },
            { v: (f(x0 + h) + f(x0)) / h, why: "somou em vez de subtrair" }],
      x: $("f(" + n(x0 + h) + ") = " + n(f(x0 + h), 3)) + " e " + $("f(" + n(x0) + ") = " + n(f(x0), 3)) + ", então " +
         $("\\dfrac{" + n(f(x0 + h), 3) + " - " + P3(f(x0)) + "}{" + n(h) + "} = " + n(m, 3)) + ". Com h cada vez menor, a secante vira a tangente: " +
         $("f'(" + n(x0) + ") = " + n(2 * a * x0)) + "." };
  } };

  G.derivlim = { t: "Derivada como limite", f: (R, p) => {
    const a = R.nz(-3, 3), b = R.nz(-5, 5), x0 = R.int(-3, 3), d = 2 * a * x0 + b;
    return { q: "Usando " + $("f'(x) = \\lim_{h \\to 0} \\dfrac{f(x+h) - f(x)}{h}") + ", quanto vale " + $("f'(" + n(x0) + ")") + " para " + $("f(x) = " + poly([a, b, 0])) + "?",
      v: d, d: { a, b, x0 },
      ops: [{ v: a * x0 * x0 + b * x0, why: "calculou f(x₀), não a derivada" }, { v: 2 * a * x0, why: "esqueceu o termo " + nt(b) + "x" }, { v: a * x0 + b, why: "esqueceu o 2 que vem do quadrado" }],
      x: "O quociente vira " + $("\\dfrac{a(x+h)^2 + b(x+h) - ax^2 - bx}{h} = 2ax + b + ah") + ", que tende a " + $("2ax + b") + " quando " + $("h \\to 0") + ". Em " +
         $("x = " + n(x0)) + ": " + $("2\\cdot " + P(a) + "\\cdot " + P(x0) + " + " + P(b) + " = " + n(d)) + "." };
  } };

  G.limfrac = { t: "Limite do tipo 0/0", f: (R, p) => {
    const c = R.nz(-5, 6), k = R.pick([1, 2, 3]), v = 2 * k * c;
    const den = c > 0 ? "x - " + n(c) : "x + " + n(-c);
    const fmt = x => (x === "nao" ? "Não existe, porque dá 0/0" : $(n(x)));
    return { q: "Quanto vale " + $("\\lim_{x \\to " + n(c) + "} \\dfrac{" + (k === 1 ? "" : k) + "x^2 - " + n(k * c * c) + "}{" + den + "}") + "?", v, fmt, d: { c, k },
      ops: [{ v: 0, why: "trocou 0/0 por 0" }, { v: "nao", why: "0/0 pede para simplificar antes" }, { v: k * c, why: "esqueceu um dos fatores c" }, { v: k * c * c, why: "" }],
      x: "Fatore: " + $((k === 1 ? "" : k) + "(x^2 - " + n(c * c) + ") = " + (k === 1 ? "" : k) + "(" + den + ")(" + (c > 0 ? "x + " + n(c) : "x - " + n(-c)) + ")") +
         " e cancele " + $("(" + den + ")") + ". Sobra " + $((k === 1 ? "" : k) + "(" + (c > 0 ? "x + " + n(c) : "x - " + n(-c)) + ")") + ", que em " + $("x = " + n(c)) + " vale " + $(n(v)) + "." };
  } };

  G.diffnum = { t: "Derivada numérica (diferença central)", f: (R, p) => {
    const x0 = R.pick([1, 2, 3, -1, -2]), h = 0.1, f = x => x * x * x, cen = (f(x0 + h) - f(x0 - h)) / (2 * h), fw = (f(x0 + h) - f(x0)) / h;
    return { q: "Para conferir um gradiente, calcule " + $("\\dfrac{f(x+h) - f(x-h)}{2h}") + " para " + $("f(x) = x^3") + ", " + $("x = " + n(x0)) + " e " + $("h = 0{,}1") + ".",
      v: cen, d: { x0, h },
      ops: [{ v: fw, why: "usou a diferença para a frente, (f(x+h) − f(x))/h" }, { v: 2 * cen, why: "dividiu por h em vez de 2h" }, { v: 3 * x0 * x0, why: "deu a derivada exata, sem fazer a conta numérica" }],
      x: $("f(" + n(x0 + h) + ") = " + n(f(x0 + h), 3)) + " e " + $("f(" + n(x0 - h) + ") = " + n(f(x0 - h), 3)) + ", então " +
         $("\\dfrac{" + n(f(x0 + h), 3) + " - " + P3(f(x0 - h)) + "}{0{,}2} = " + n(cen)) + ". Bem perto da derivada exata " + $("3x^2 = " + n(3 * x0 * x0)) +
         ": é assim que se confere um backpropagation." };
  } };

  G.dpoly = { t: "Derivada de um polinômio", f: (R, p) => {
    const cs = [R.nz(-3, 3), R.int(-4, 4), R.nz(-5, 5), R.int(-5, 5)], x0 = R.int(-2, 3), df = pder(cs), d = pval(df, x0);
    return { q: "Quanto vale " + $("f'(" + n(x0) + ")") + " para " + $("f(x) = " + poly(cs)) + "?", v: d, d: { cs, x0 },
      ops: [{ v: pval(cs, x0), why: "calculou f(x₀), não f'(x₀)" }, { v: pval(cs.slice(0, 3), x0), why: "baixou o grau sem multiplicar pelo expoente" },
            { v: d - cs[2], why: "derivou o termo em x como se fosse constante" }],
      x: "Pela regra da potência, " + $("f'(x) = " + poly(df)) + ". Em " + $("x = " + n(x0)) + ": " + $("f'(" + n(x0) + ") = " + n(d)) + "." };
  } };

  G.dpot = { t: "Regra da potência", f: (R, p) => {
    const a = R.pick([2, 3, 4, 5, -2, -3, 0.5]), k = R.pick([2, 3, 4, 5, -1, -2]);
    return { q: "Derive " + $("f(x) = " + termo(a, k)) + ".", v: [a * k, k - 1], fmt: v => $("f'(x) = " + termo(v[0], v[1])), d: { a, k },
      ops: [{ v: [a * k, k], why: "não diminuiu o expoente" }, { v: [a, k - 1], why: "esqueceu de multiplicar pelo expoente" }, { v: [a * k, k + 1], why: "aumentou o expoente em vez de diminuir" }],
      x: "Regra da potência: " + $("\\dfrac{d}{dx}\\,a x^n = n\\,a\\,x^{n-1}") + ". Aqui: " + $(P(k) + "\\cdot " + P(a) + "\\, x^{" + k + " - 1} = " + termo(a * k, k - 1)) + "." };
  } };

  G.dprod = { t: "Regra do produto", f: (R, p) => {
    const a = R.nz(-4, 4), b = R.nz(-5, 5), x0 = R.int(-2, 3), u = x0 + a, v = x0 * x0 + b, dv = 2 * x0, d = v + u * dv;
    return { q: "Use a regra do produto para calcular " + $("f'(" + n(x0) + ")") + " com " + $("f(x) = (x " + sg(a) + ")(x^2 " + sg(b) + ")") + ".", v: d, d: { a, b, x0 },
      ops: [{ v: dv, why: "multiplicou as derivadas (u'·v')" }, { v: v, why: "fez só u'v" }, { v: u * dv, why: "fez só uv'" }],
      x: "Com " + $("u = x " + sg(a)) + " e " + $("v = x^2 " + sg(b)) + ": " + $("f' = u'v + uv' = 1\\cdot " + P(v) + " + " + P(u) + "\\cdot " + P(dv) + " = " + n(d)) + "." };
  } };

  G.dmse = { t: "Derivada do erro quadrático", f: (R, p) => {
    const w = R.pick([-1, 0.5, 1, 1.5, 2, 3]), x = R.nz(-3, 4), y = R.int(-5, 8), r = w * x - y, d = 2 * r * x;
    return { q: "Para " + $("L(w) = (w x - y)^2") + " com " + $("x = " + n(x)) + " e " + $("y = " + n(y)) + ", quanto vale " + $("\\dfrac{dL}{dw}") + " em " + $("w = " + n(w)) + "?",
      v: d, d: { w, x, y },
      ops: [{ v: 2 * r, why: "esqueceu a derivada de dentro (o x)" }, { v: r * r, why: "calculou a perda, não a derivada" }, { v: -d, why: "errou o sinal do resíduo" }],
      x: "Regra da cadeia: " + $("\\dfrac{dL}{dw} = 2(wx - y)\\cdot x") + ". O resíduo é " + $(n(w) + "\\cdot " + P(x) + " - " + P(y) + " = " + n(r)) + ", então " +
         $("2\\cdot " + P(r) + "\\cdot " + P(x) + " = " + n(d)) + "." };
  } };

  G.cadeia = { t: "Regra da cadeia", f: (R, p) => {
    const a = R.nz(-3, 3), b = R.int(-3, 4), k = R.pick([2, 3]), x0 = R.int(-2, 2), u = a * x0 + b, fora = k * Math.pow(u, k - 1), d = fora * a;
    return { q: "Calcule " + $("\\dfrac{dy}{dx}") + " em " + $("x = " + n(x0)) + " para " + $("y = (" + aff(a, b) + ")^{" + k + "}") + ".", v: d, d: { a, b, k, x0 },
      ops: [{ v: fora, why: "esqueceu de multiplicar pela derivada de dentro (" + nt(a) + ")" }, { v: k * Math.pow(x0, k - 1) * a, why: "avaliou a de fora em x, não em u" },
            { v: Math.pow(u, k), why: "calculou y, não a derivada" }],
      x: "De dentro: " + $("u = " + aff(a, b) + " = " + n(u)) + " e " + $("u' = " + n(a)) + ". De fora: " + $("\\dfrac{dy}{du} = " + k + "u" + (k === 2 ? "" : "^{" + (k - 1) + "}") + " = " + n(fora)) +
         ". Multiplique: " + $(n(fora) + "\\cdot " + P(a) + " = " + n(d)) + "." };
  } };

  G.cadeialn = { t: "Regra da cadeia com logaritmo", f: (R, p) => {
    let a, b, x0, u; do { a = R.pick([1, 2, 3, 4, -1, -2]); b = R.int(-3, 6); x0 = R.int(-2, 3); u = a * x0 + b; } while (u <= 0);
    return { q: "Calcule " + $("\\dfrac{dy}{dx}") + " em " + $("x = " + n(x0)) + " para " + $("y = \\ln(" + aff(a, b) + ")") + ".", v: a / u, casas: 3, d: { a, b, x0 },
      ops: [{ v: 1 / u, why: "esqueceu a derivada de dentro (" + nt(a) + ")" }, { v: Math.log(u), why: "calculou y, não a derivada" }, { v: u / a, why: "inverteu a fração" }],
      x: $("\\dfrac{d}{dx}\\ln u = \\dfrac{u'}{u}") + ". Aqui " + $("u = " + n(u)) + " e " + $("u' = " + n(a)) + ", então " + $("\\dfrac{" + n(a) + "}{" + n(u) + "} \\approx " + n(a / u, 3)) + "." };
  } };

  G.cadeia3 = { t: "Regra da cadeia com três elos", f: (R, p) => {
    const m = R.pick([2, 3, -1, -2]), pp = R.pick([2, 3, -2]), qq = R.int(-3, 3), x0 = R.int(-2, 2), v = m * x0, u = pp * v + qq, d = 2 * u * pp * m;
    return { q: "Com " + $("y = u^2") + ", " + $("u = " + aff(pp, qq, "v")) + " e " + $("v = " + n(m) + "x") + ", quanto vale " + $("\\dfrac{dy}{dx}") + " em " + $("x = " + n(x0)) + "?",
      v: d, d: { m, pp, qq, x0 },
      ops: [{ v: 2 * u * pp, why: "esqueceu o último elo (dv/dx)" }, { v: 2 * u + pp + m, why: "somou os elos em vez de multiplicar" }, { v: 2 * x0 * pp * m, why: "avaliou o 2u em x, não em u" }],
      x: "Ida: " + $("v = " + n(v)) + " e " + $("u = " + n(u)) + ". Volta: " + $("\\dfrac{dy}{du} = 2u = " + n(2 * u)) + ", " + $("\\dfrac{du}{dv} = " + n(pp)) + " e " +
         $("\\dfrac{dv}{dx} = " + n(m)) + ". Multiplique: " + $(n(2 * u) + "\\cdot " + P(pp) + "\\cdot " + P(m) + " = " + n(d)) + "." };
  } };

  G.passo1 = { t: "Um passo de treino de um neurônio", f: (R, p) => {
    const w = R.pick([0, 0.5, 1, 2, -1]), b = R.pick([0, 1, -1]), x = R.pick([1, 2, 3, -1]), y = R.int(-2, 6), eta = R.pick([0.1, 0.05, 0.01]);
    const yh = w * x + b, r = yh - y, g = 2 * r * x, wn = w - eta * g;
    return { q: "Um neurônio linear faz " + $("\\hat y = wx + b") + " com perda " + $("L = (\\hat y - y)^2") + ". Com " + $("w = " + n(w)) + ", " + $("b = " + n(b)) + ", " +
             $("x = " + n(x)) + ", " + $("y = " + n(y)) + " e " + $("\\eta = " + n(eta)) + ", quanto vale w depois de um passo de descida do gradiente?", v: wn, casas: 3, d: { w, b, x, y, eta },
      ops: [{ v: w + eta * g, why: "somou o gradiente (subiu a ladeira)" }, { v: w - g, why: "esqueceu a taxa de aprendizado" }, { v: w - eta * 2 * r, why: "esqueceu o x no gradiente" }],
      x: $("\\hat y = " + n(yh)) + ", então " + $("\\dfrac{\\partial L}{\\partial w} = 2(\\hat y - y)\\,x = 2\\cdot " + P(r) + "\\cdot " + P(x) + " = " + n(g)) + ". Passo: " +
         $("w \\leftarrow " + n(w) + " - " + n(eta) + "\\cdot " + P(g) + " = " + n(wn, 3)) + "." };
  } };

  G.sigd = { t: "Derivada da sigmoide", f: (R, p) => {
    const s = R.pick([0.5, 0.1, 0.2, 0.25, 0.4, 0.6, 0.75, 0.8, 0.9]);
    return { q: "Se " + $("\\sigma(z) = " + n(s)) + ", quanto vale a derivada " + $("\\sigma'(z)") + "?", v: s * (1 - s), casas: 4, d: { s },
      ops: [{ v: s, why: "repetiu o σ(z)" }, { v: 1 - s, why: "fez só 1 − σ" }, { v: s * s, why: "elevou σ ao quadrado" }],
      x: $("\\sigma'(z) = \\sigma(z)\\,(1 - \\sigma(z)) = " + n(s) + "\\cdot " + n(1 - s) + " = " + n(s * (1 - s), 4)) +
         ". O máximo é 0,25 (em z = 0): por isso a sigmoide enfraquece o gradiente em redes fundas." };
  } };

  G.relud = { t: "Derivada da ReLU", f: (R, p) => {
    let z; do { z = R.vec(4, -3, 3).map(v => (v === 0 ? 1 : v) + R.pick([0, 0.5])); } while (!z.some(v => v < 0) || !z.some(v => v > 0));
    const d = z.map(v => (v > 0 ? 1 : 0));
    return { q: "Para " + $("z = " + V(z)) + ", qual é a derivada da ReLU em cada posição?", v: d, d: { z },
      ops: [{ v: z.map(v => Math.max(0, v)), why: "calculou a ReLU, não a derivada" }, { v: z.map(v => Math.sign(v)), why: "pôs −1 onde z é negativo" }, { v: z.map(() => 1), why: "achou que a derivada é sempre 1" }],
      x: "A ReLU é " + $("\\max(0, z)") + ": inclinação 1 onde " + $("z > 0") + " e 0 onde " + $("z < 0") + ". Resultado: " + $(V(d)) + "." };
  } };

  G.tanhd = { t: "Derivada da tangente hiperbólica", f: (R, p) => {
    const t = R.pick([0, 0.2, 0.5, 0.6, 0.8, 0.9, -0.5, -0.8]);
    return { q: "Se " + $("\\tanh(z) = " + n(t)) + ", quanto vale " + $("\\tanh'(z)") + "?", v: 1 - t * t, d: { t },
      ops: [{ v: 1 - t, why: "esqueceu de elevar ao quadrado" }, { v: t * (1 - t), why: "usou a fórmula da sigmoide" }, { v: t * t, why: "fez só tanh²" }],
      x: $("\\tanh'(z) = 1 - \\tanh^2(z) = 1 - " + P(t) + "^2 = " + n(1 - t * t)) + ". O máximo é 1, em z = 0." };
  } };

  G.vanish = { t: "Gradiente que some (vanishing gradient)", f: (R, p) => {
    const k = R.pick([2, 3, 4, 5, 6]), v = Math.pow(0.25, k);
    return { q: "A derivada da sigmoide é no máximo 0,25. Numa rede com " + k + " camadas sigmoide, por quanto o gradiente que chega à 1ª camada fica multiplicado, no melhor caso?",
      v, casas: 6, fmt: x => $(x < 0.01 ? sci(x) : n(x, 4)), d: { k },
      ops: [{ v: 0.25 * k, why: "somou em vez de multiplicar" }, { v: 0.25, why: "considerou só uma camada" }, { v: Math.pow(0.25, k - 1), why: "contou uma camada a menos" }],
      x: "Cada camada multiplica por no máximo 0,25: " + $("0{,}25^{" + k + "} = " + (v < 0.01 ? sci(v) : n(v, 4))) + ". Com muitas camadas o sinal praticamente some, e é por isso que redes fundas usam ReLU." };
  } };

  G.parcial = { t: "Derivada parcial", f: (R, p) => {
    const a = R.nz(-3, 3), b = R.nz(-4, 4), c = R.nz(-3, 3), x0 = R.int(-2, 3), y0 = R.int(-2, 3), qual = R.pick(["x", "y"]);
    const fx = 2 * a * x0 + b * y0, fy = b * x0 + 2 * c * y0, v = qual === "x" ? fx : fy;
    return { q: "Para " + $("f(x, y) = " + lin([a, b, c], ["x^2", "xy", "y^2"])) + ", quanto vale " + $("\\dfrac{\\partial f}{\\partial " + qual + "}") + " no ponto " + $("(" + n(x0) + ",\\ " + n(y0) + ")") + "?",
      v, d: { a, b, c, x0, y0, qual },
      ops: [{ v: qual === "x" ? fy : fx, why: "derivou em relação à outra variável" }, { v: qual === "x" ? 2 * a * x0 : 2 * c * y0, why: "esqueceu o termo cruzado" }, { v: fx + fy, why: "derivou nas duas variáveis" }],
      x: "Congele a outra variável e derive: " + (qual === "x" ? $("\\dfrac{\\partial f}{\\partial x} = 2\\cdot " + P(a) + "x + " + P(b) + "y")
                                                                 : $("\\dfrac{\\partial f}{\\partial y} = " + P(b) + "x + 2\\cdot " + P(c) + "y")) + ". No ponto: " + $(n(v)) + "." };
  } };

  G.grad = { t: "Vetor gradiente", f: (R, p) => {
    const a = R.nz(-3, 3), b = R.nz(-3, 3), c = R.int(-3, 3), x0 = R.int(-2, 3), y0 = R.int(-2, 3);
    const g = [2 * a * x0 + c * y0, 2 * b * y0 + c * x0];
    return { q: "Calcule " + $("\\nabla f") + " no ponto " + $("(" + n(x0) + ",\\ " + n(y0) + ")") + " para " + $("f(x, y) = " + lin([a, b, c], ["x^2", "y^2", "xy"])) + ".", v: g, d: { a, b, c, x0, y0 },
      ops: [{ v: [g[1], g[0]], why: "trocou as componentes" }, { v: [a * x0 + c * y0, b * y0 + c * x0], why: "esqueceu o 2 dos quadrados" }, { v: [2 * a * x0, 2 * b * y0], why: "esqueceu o termo cruzado xy" }],
      x: $("\\nabla f = \\left(\\dfrac{\\partial f}{\\partial x},\\ \\dfrac{\\partial f}{\\partial y}\\right) = (2\\cdot " + P(a) + "x + " + P(c) + "y,\\ 2\\cdot " + P(b) + "y + " + P(c) + "x)") +
         ". No ponto: " + $(V(g)) + "." };
  } };

  G.graddir = { t: "Direção da descida mais rápida", f: (R, p) => {
    const g = [R.nz(-6, 6), R.nz(-6, 6)], v = g.map(x => -x);
    return { q: "Num ponto, " + $("\\nabla L = " + V(g)) + ". Em que direção andar para a perda <b>cair</b> o mais rápido possível?", v, d: { g },
      ops: [{ v: g.slice(), why: "esse é o sentido da subida mais rápida" }, { v: [-g[1], g[0]], why: "perpendicular: anda pela curva de nível, sem descer" }, { v: [g[1], g[0]], why: "trocou as componentes" }],
      x: "O gradiente aponta para a subida mais íngreme. A descida mais rápida é o oposto: " + $("-\\nabla L = " + V(v)) + ". É o que a descida do gradiente faz a cada passo." };
  } };

  G.hess = { t: "Matriz Hessiana", f: (R, p) => {
    const a = R.nz(-3, 3), b = R.nz(-4, 4), c = R.nz(-3, 3);
    return { q: "Qual é a Hessiana de " + $("f(x, y) = " + lin([a, b, c], ["x^2", "xy", "y^2"])) + "?", v: [[2 * a, b], [b, 2 * c]], d: { a, b, c },
      ops: [{ v: [[a, b], [b, c]], why: "esqueceu o 2 das derivadas segundas" }, { v: [[2 * a, 2 * b], [2 * b, 2 * c]], why: "dobrou o termo cruzado" }, { v: [[2 * a, 0], [0, 2 * c]], why: "ignorou o termo cruzado" }],
      x: "Derivadas segundas: " + $("f_{xx} = " + n(2 * a)) + ", " + $("f_{yy} = " + n(2 * c)) + " e " + $("f_{xy} = f_{yx} = " + n(b)) + "." };
  } };

  const SELA = { min: "Mínimo local: curva para cima em todas as direções", max: "Máximo local: curva para baixo em todas as direções",
                 sela: "Ponto de sela: sobe numa direção e desce em outra", nd: "Não dá para saber sem derivadas de ordem maior" };
  G.sela = { t: "Mínimo, máximo ou ponto de sela", f: (R, p) => {
    let H, det; do { const q = R.int(-3, 3); H = [[R.nz(-5, 5), q], [q, R.nz(-5, 5)]]; det = H[0][0] * H[1][1] - q * q; } while (det === 0);
    const cat = det < 0 ? "sela" : H[0][0] > 0 ? "min" : "max";
    return { q: "Num ponto crítico (gradiente zero), a Hessiana é " + $("H = " + M(H)) + ". Que tipo de ponto é?", v: cat, fmt: c => SELA[c], d: { H },
      ops: ["min", "max", "sela", "nd"].filter(c => c !== cat).map(c => ({ v: c, why: "" })),
      x: $("\\det H = " + P(H[0][0]) + "\\cdot " + P(H[1][1]) + " - " + P(H[0][1]) + "^2 = " + n(det)) +
         (det < 0 ? ". Negativo: os autovalores têm sinais opostos, então é ponto de sela."
                  : ". Positivo, e " + $("H_{11} = " + n(H[0][0])) + (H[0][0] > 0 ? " é positivo: os dois autovalores são positivos, mínimo." : " é negativo: os dois autovalores são negativos, máximo.")) };
  } };

  G.jacob = { t: "Matriz Jacobiana", f: (R, p) => {
    const a = R.nz(-3, 3), b = R.nz(-3, 3), x0 = R.int(-2, 3), y0 = R.int(-2, 3);
    const J = [[2 * x0, a], [b * y0, b * x0]];
    return { q: "Para " + $("F(x, y) = (x^2 " + sg(a) + "y,\\ " + n(b) + "xy)") + ", qual é a Jacobiana no ponto " + $("(" + n(x0) + ",\\ " + n(y0) + ")") + "?", v: J, d: { a, b, x0, y0 },
      ops: [{ v: [[J[0][0], J[1][0]], [J[0][1], J[1][1]]], why: "montou a transposta (colunas no lugar das linhas)" }, { v: [[2 * x0, a], [b * x0, b * y0]], why: "trocou as derivadas de xy" },
            { v: [[x0 * x0, a * y0], [b * x0 * y0, b * x0 * y0]], why: "calculou os valores, não as derivadas" }],
      x: "Cada linha é o gradiente de uma saída: " + $("\\left(\\dfrac{\\partial F_1}{\\partial x}, \\dfrac{\\partial F_1}{\\partial y}\\right) = (2x,\\ " + n(a) + ")") + " e " +
         $("\\left(\\dfrac{\\partial F_2}{\\partial x}, \\dfrac{\\partial F_2}{\\partial y}\\right) = (" + n(b) + "y,\\ " + n(b) + "x)") + ". No ponto: " + $(M(J)) + "." };
  } };

  G.gdpasso = { t: "Um passo de descida do gradiente", f: (R, p) => {
    const c = R.nz(-3, 6), w0 = R.int(-4, 6), eta = R.pick([0.1, 0.2, 0.25, 0.5, 0.05]), g = 2 * (w0 - c), w1 = w0 - eta * g;
    return { q: "Para " + $("L(w) = (w " + sg(-c) + ")^2") + ", com " + $("w_0 = " + n(w0)) + " e " + $("\\eta = " + n(eta)) + ", quanto vale " + $("w_1") + "?", v: w1, casas: 3, d: { c, w0, eta },
      ops: [{ v: w0 + eta * g, why: "somou o gradiente (subiu)" }, { v: w0 - g, why: "esqueceu a taxa de aprendizado" }, { v: w0 - eta * (w0 - c), why: "esqueceu o 2 da derivada" }],
      x: $("L'(w) = 2(w " + sg(-c) + ")") + ", então " + $("L'(" + n(w0) + ") = " + n(g)) + ". Passo: " + $("w_1 = " + n(w0) + " - " + n(eta) + "\\cdot " + P(g) + " = " + n(w1, 3)) + "." };
  } };

  G.gd2 = { t: "Dois passos de descida do gradiente", f: (R, p) => {
    const c = R.nz(-2, 5), w0 = R.int(-3, 6), eta = R.pick([0.1, 0.25, 0.5]), g = w => 2 * (w - c);
    const w1 = w0 - eta * g(w0), w2 = w1 - eta * g(w1);
    return { q: "Para " + $("L(w) = (w " + sg(-c) + ")^2") + ", " + $("w_0 = " + n(w0)) + " e " + $("\\eta = " + n(eta)) + ", quanto vale " + $("w_2") + " (dois passos)?", v: w2, casas: 3, d: { c, w0, eta },
      ops: [{ v: w1, why: "deu um passo só" }, { v: w0 - 2 * eta * g(w0), why: "repetiu o gradiente do 1º passo" }, { v: w1 + eta * g(w1), why: "no 2º passo, subiu em vez de descer" }],
      x: "1º passo: " + $("w_1 = " + n(w0) + " - " + n(eta) + "\\cdot " + P(g(w0)) + " = " + n(w1, 3)) + ". 2º passo, com o gradiente novo " + $("L'(w_1) = " + n(g(w1), 3)) + ": " +
         $("w_2 = " + n(w1, 3) + " - " + n(eta) + "\\cdot " + P3(g(w1)) + " = " + n(w2, 3)) + ". Repare que o passo encolhe perto do mínimo." };
  } };

  const REGIME = { suave: "Converge para o mínimo, sem passar dele", oscila: "Converge, mas passa do mínimo e volta (oscila)",
                   diverge: "Diverge: cada passo fica pior", parado: "Fica parado no lugar" };
  G.gdlr = { t: "Taxa de aprendizado grande ou pequena", f: (R, p) => {
    const a = R.pick([0.5, 1, 2]), fat = R.pick([0.4, 0.8, 1.5, 1.8, 2.5, 3]), eta = fat / (2 * a), r = 1 - fat;
    const cat = Math.abs(r) > 1 ? "diverge" : r < 0 ? "oscila" : "suave";
    return { q: "Para " + $("L(w) = " + n(a) + "w^2") + " (mínimo em w = 0) e " + $("\\eta = " + n(eta, 3)) + ", o que a descida do gradiente faz a partir de w = 1?", v: cat, fmt: c => REGIME[c], d: { a, eta },
      ops: ["suave", "oscila", "diverge", "parado"].filter(c => c !== cat).map(c => ({ v: c, why: "" })),
      x: "Cada passo faz " + $("w \\leftarrow w - \\eta\\cdot " + n(2 * a) + "w = (1 - " + n(fat) + ")\\,w = " + n(r) + "\\,w") + ". " +
         (cat === "suave" ? "O fator está entre 0 e 1: w encolhe a cada passo, sempre do mesmo lado."
          : cat === "oscila" ? "O fator está entre −1 e 0: w troca de sinal a cada passo, mas encolhe."
          : "O fator tem módulo maior que 1: w cresce a cada passo, a taxa está grande demais.") };
  } };

  G.minibatch = { t: "Passos por época com mini-batch", f: (R, p) => {
    const N = R.pick([1000, 1200, 2500, 5000, 50000, 60000]), B = R.pick([32, 64, 100, 128, 256]), v = Math.ceil(N / B);
    return { q: "Com " + $(String(N)) + " exemplos de treino e lotes de " + $(String(B)) + ", quantas atualizações de peso acontecem numa época?", v, fmt: x => $(String(x)), d: { N, B },
      ops: [{ v: Math.floor(N / B), why: "esqueceu o último lote, que vem incompleto" }, { v: r2(N / B), why: "deixou a divisão quebrada" }, { v: N, why: "contou uma atualização por exemplo (SGD puro)" }],
      x: "Uma atualização por lote: " + $("\\lceil " + N + " / " + B + " \\rceil = " + v) + (N % B ? " (o último lote vem com " + (N % B) + " exemplos)." : ".") };
  } };

  G.momentum = { t: "Momentum", f: (R, p) => {
    const beta = 0.9, vp = R.pick([0, 1, 2, -1, 0.5]), g = R.pick([1, 2, 3, 4, -2, 5]), v = beta * vp + (1 - beta) * g;
    return { q: "No Momentum, " + $("v_t = \\beta\\,v_{t-1} + (1 - \\beta)\\,g_t") + ". Com " + $("\\beta = 0{,}9") + ", " + $("v_{t-1} = " + n(vp)) + " e " + $("g_t = " + n(g)) + ", quanto vale " + $("v_t") + "?",
      v, casas: 3, d: { vp, g },
      ops: [{ v: beta * vp + g, why: "esqueceu o (1 − β) no gradiente" }, { v: (1 - beta) * vp + beta * g, why: "trocou os pesos" }, { v: beta * (vp + g), why: "multiplicou tudo por β" }],
      x: $("v_t = 0{,}9\\cdot " + P(vp) + " + 0{,}1\\cdot " + P(g) + " = " + n(beta * vp, 3) + " + " + P(0.1 * g) + " = " + n(v, 3)) + ". É uma média que lembra os passos anteriores (a inércia)." };
  } };

  G.rmsprop = { t: "RMSprop", f: (R, p) => {
    const beta = 0.9, s = R.pick([0, 1, 2, 4, 0.5]), g = R.pick([1, 2, 3, -2, 4]), v = beta * s + (1 - beta) * g * g;
    return { q: "No RMSprop, " + $("s_t = \\beta\\,s_{t-1} + (1 - \\beta)\\,g_t^2") + ". Com " + $("\\beta = 0{,}9") + ", " + $("s_{t-1} = " + n(s)) + " e " + $("g_t = " + n(g)) + ", quanto vale " + $("s_t") + "?",
      v, casas: 3, d: { s, g },
      ops: [{ v: beta * s + (1 - beta) * g, why: "esqueceu de elevar g ao quadrado" }, { v: beta * s + g * g, why: "esqueceu o (1 − β)" }, { v: (1 - beta) * s + beta * g * g, why: "trocou os pesos" }],
      x: $("s_t = 0{,}9\\cdot " + P(s) + " + 0{,}1\\cdot " + P(g) + "^2 = " + n(beta * s, 3) + " + " + n(0.1 * g * g, 3) + " = " + n(v, 3)) +
         ". Depois o passo é dividido por " + $("\\sqrt{s_t}") + ": direções com gradiente grande andam menos." };
  } };

  G.adambias = { t: "Adam: correção de viés", f: (R, p) => {
    const b1 = 0.9, g = R.pick([1, 2, 4, 5, -3, 10]), m1 = (1 - b1) * g, mh = m1 / (1 - b1);
    return { q: "No 1º passo do Adam (" + $("m_0 = 0") + ", " + $("\\beta_1 = 0{,}9") + "), o gradiente é " + $("g_1 = " + n(g)) + ". Quanto valem " + $("m_1 = \\beta_1 m_0 + (1 - \\beta_1) g_1") +
             " e a versão corrigida " + $("\\hat m_1 = m_1 / (1 - \\beta_1^1)") + "?", v: [m1, mh], fmt: v => $("m_1 = " + n(v[0], 2) + ",\\ \\hat m_1 = " + n(v[1], 2)), d: { g },
      ops: [{ v: [m1, m1], why: "esqueceu a correção de viés" }, { v: [b1 * g, b1 * g / (1 - b1)], why: "trocou β e 1 − β" }, { v: [g, g / (1 - b1)], why: "não multiplicou g por (1 − β)" }],
      x: $("m_1 = 0{,}1\\cdot " + P(g) + " = " + n(m1, 2)) + ", pequeno demais porque a média começou do zero. A correção divide por " + $("1 - 0{,}9 = 0{,}1") + ": " +
         $("\\hat m_1 = " + n(mh, 2)) + ", que é o próprio gradiente." };
  } };

  G.warmup = { t: "Aquecimento (warmup) da taxa", f: (R, p) => {
    const em = R.pick([0.001, 0.003, 0.0006, 0.002]), Tw = R.pick([1000, 2000, 500]), t = R.pick([0.1, 0.25, 0.5, 0.75]) * Tw, v = em * t / Tw;
    return { q: "No warmup linear, " + $("\\eta_t = \\eta_{\\max} \\cdot t / T_w") + ". Com " + $("\\eta_{\\max} = " + n(em, 4)) + " e " + $("T_w = " + Tw) + ", quanto vale a taxa no passo " + $("t = " + t) + "?",
      v, casas: 7, fmt: x => $(n(x, 7)), d: { em, Tw, t },
      ops: [{ v: em, why: "usou a taxa cheia, sem aquecimento" }, { v: em * Tw / t, why: "inverteu a fração" }, { v: em * t, why: "não dividiu por T_w" }],
      x: $("\\eta_{" + t + "} = " + n(em, 4) + " \\cdot " + t + " / " + Tw + " = " + n(v, 7)) + ". A taxa sobe aos poucos até o máximo, o que evita passos enormes no início do treino." };
  } };

  G.cosdecay = { t: "Decaimento por cosseno", f: (R, p) => {
    const em = R.pick([0.008, 0.004, 0.0012]), T = R.pick([1200, 3000, 6000]), fr = R.pick([0, 1 / 3, 0.5, 2 / 3, 1]), t = Math.round(fr * T);
    const v = 0.5 * em * (1 + Math.cos(Math.PI * fr));
    return { q: "No cosine decay, " + $("\\eta_t = \\tfrac{1}{2}\\,\\eta_{\\max}\\,(1 + \\cos(\\pi t / T))") + ". Com " + $("\\eta_{\\max} = " + n(em, 4)) + " e " + $("T = " + T) + ", quanto vale " + $("\\eta_{" + t + "}") + "?",
      v, casas: 7, fmt: x => $(n(x, 7)), d: { em, T, t },
      ops: [{ v: em * (1 - fr), why: "fez a queda em linha reta" }, { v: 0.5 * em * (1 - Math.cos(Math.PI * fr)), why: "trocou o sinal do cosseno" }, { v: em, why: "não aplicou o decaimento" },
            { v: em / 4, why: "dividiu o máximo por 4" }, { v: 0, why: "achou que a taxa zera" }],
      x: $("\\cos(\\pi \\cdot " + t + " / " + T + ") = " + n(Math.cos(Math.PI * fr), 2)) + ", então " + $("\\eta = \\tfrac{1}{2}\\cdot " + n(em, 4) + "\\cdot (1 " + sg(r2(Math.cos(Math.PI * fr))) + ") = " + n(v, 7)) + "." };
  } };
})();
"""
