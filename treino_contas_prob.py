# -*- coding: utf-8 -*-
"""
Geradores de conta do Treino: Matemática, Módulo 4 do site (Probabilidade, Estatística & Teoria da Informação).

Mesmo formato de treino_contas.py (que define as ferramentas TR.H usadas aqui). As respostas são refeitas em
treino_checagem.py por outro caminho (contagens, NumPy, math.erf).
"""

TR_GEN_JS = r"""
// =================== TREINO: geradores de conta (Probabilidade, Estatística e Informação) ===================
(() => {
  const G = TR.GEN;
  const { n, V, M, N1, P, nt, $, dot, sum, sub, r2, pctF, milhar } = TR.H;
  const lista = arr => arr.map(x => n(x, 3)).join(",\\ ");
  const media = a => sum(a) / a.length;
  const mediana = a => { const s = a.slice().sort((x, y) => x - y), k = s.length; return k % 2 ? s[(k - 1) / 2] : (s[k / 2 - 1] + s[k / 2]) / 2; };
  const lg2 = Math.log2, ln = Math.log;
  // partes inteiras positivas que somam 'total' (para probabilidades em décimos)
  const partes = (R, k, total) => {
    const cuts = R.shuffle(Array.from({ length: total - 1 }, (_, i) => i + 1)).slice(0, k - 1).sort((a, b) => a - b);
    return cuts.concat([total]).map((c, i) => c - (i ? cuts[i - 1] : 0));
  };
  const pct2 = x => $(n(x, 2) + "\\%");
  // valor em reais por extenso: o cifrão do símbolo do real abriria uma fórmula no KaTeX
  const reais = x => (x < 0 ? "perde " : "ganha ") + nt(Math.abs(x), 2) + " reais por aposta, em média";

  // ---------------- Variáveis aleatórias ----------------
  G.pmffalta = { t: "Probabilidade que falta na tabela", f: (R, p) => {
    const k = R.int(3, 4), dez = partes(R, k, 10), ps = dez.map(x => x / 10), i = R.int(0, k - 1), falta = ps[i];
    const mostra = ps.map((x, j) => (j === i ? "?" : n(x)));
    return { q: "A variável X vale " + Array.from({ length: k }, (_, j) => j + 1).join(", ") + " com probabilidades " + $(mostra.join(",\\ ")) + ". Quanto vale o ponto de interrogação?",
      v: falta, d: { ps, i },
      ops: [{ v: r2(1 - falta), why: "deu a soma das outras" }, { v: r2(1 / k), why: "achou que todas são iguais" }, { v: 0, why: "achou que não sobra nada" }],
      x: "As probabilidades somam 1: " + $("1 - (" + ps.filter((_, j) => j !== i).map(x => n(x)).join(" + ") + ") = " + n(falta)) + "." };
  } };

  G.pmfcum = { t: "Probabilidade acumulada", f: (R, p) => {
    const ps = partes(R, 4, 10).map(x => x / 10), k = R.int(0, 2), tipo = R.pick(["le", "gt"]);
    const v = r2(tipo === "le" ? sum(ps.slice(0, k + 1)) : sum(ps.slice(k + 1)));
    return { q: "X vale 0, 1, 2 ou 3 com probabilidades " + $(lista(ps)) + ", nessa ordem. Quanto vale " + $("P(X " + (tipo === "le" ? "\\leq" : ">") + " " + k + ")") + "?",
      v, d: { ps, k, tipo },
      ops: [{ v: ps[k], why: "pegou só P(X = " + k + ")" }, { v: r2(1 - v), why: "calculou o complemento" },
            { v: r2(tipo === "le" ? sum(ps.slice(0, k)) : sum(ps.slice(k))), why: tipo === "le" ? "deixou o " + k + " de fora (fez <)" : "incluiu o " + k + " (fez ≥)" }],
      x: "Some as probabilidades dos valores " + (tipo === "le" ? "de 0 até " + k : "maiores que " + k) + ": " + $(n(v)) + "." };
  } };

  G.unifarea = { t: "Probabilidade numa distribuição uniforme", f: (R, p) => {
    const b = R.pick([4, 5, 8, 10, 20]); let lo, hi; do { lo = R.int(0, b - 1); hi = R.int(1, b); } while (hi <= lo || (lo === 0 && hi === b));
    const v = (hi - lo) / b;
    return { q: "X é uniforme entre 0 e " + b + ". Quanto vale " + $("P(" + lo + " \\leq X \\leq " + hi + ")") + "?", v, casas: 3, d: { b, lo, hi },
      ops: [{ v: hi - lo, why: "esqueceu de dividir pelo tamanho do intervalo" }, { v: 1 / b, why: "deu a altura da densidade, não a área" }, { v: hi / b, why: "calculou P(X ≤ " + hi + ")" }],
      x: "A densidade é " + $("1/" + b) + " no intervalo todo. A probabilidade é a área: " + $("(" + hi + " - " + lo + ") \\cdot \\tfrac{1}{" + b + "} = " + n(v, 3)) + "." };
  } };

  // ---------------- Média, mediana, variância ----------------
  G.media = { t: "Média", f: (R, p) => {
    const k = R.pick([4, 5]), xs = R.vec(k, 1, 20), m = media(xs);
    return { q: "Qual é a média de " + $(lista(xs)) + "?", v: m, d: { xs },
      ops: [{ v: mediana(xs), why: "calculou a mediana" }, { v: sum(xs) / (k - 1), why: "dividiu por n − 1" }, { v: sum(xs), why: "esqueceu de dividir" }],
      x: $("\\dfrac{" + xs.join(" + ") + "}{" + k + "} = \\dfrac{" + sum(xs) + "}{" + k + "} = " + n(m)) + "." };
  } };

  G.mediana = { t: "Mediana", f: (R, p) => {
    const k = R.pick([5, 6, 7]), xs = R.vec(k, 1, 30), s = xs.slice().sort((a, b) => a - b), md = mediana(xs), mid = Math.floor(k / 2);
    return { q: "Qual é a mediana de " + $(lista(xs)) + "?", v: md, d: { xs },
      ops: [{ v: r2(media(xs)), why: "calculou a média" }, { v: xs[mid], why: "pegou o do meio sem ordenar" },
            { v: k % 2 ? s[mid + 1] : s[mid], why: k % 2 ? "contou a posição errada" : "com quantidade par, faltou tirar a média dos dois do meio" }],
      x: "Ordene: " + $(lista(s)) + ". " + (k % 2 ? "O do meio é " + $(n(md)) : "Com " + k + " valores, a mediana é a média dos dois do meio: " + $("(" + s[mid - 1] + " + " + s[mid] + ")/2 = " + n(md))) + "." };
  } };

  G.variancia = { t: "Variância e desvio padrão", f: (R, p) => {
    const dv = R.pick([[-3, -1, 0, 1, 3], [-2, -2, 0, 2, 2], [-4, 0, 0, 0, 4], [-1, -1, 1, 1], [-3, -1, 1, 3], [-2, 0, 0, 2], [-6, -2, 2, 6], [-5, -1, 1, 5]]);
    const mu = R.int(3, 20), xs = R.shuffle(dv.map(x => x + mu)), k = xs.length, sq = sum(dv.map(x => x * x)), vr = sq / k, sd = Math.sqrt(vr), tipo = R.pick(["var", "dp"]);
    const v = tipo === "var" ? vr : sd;
    return { q: "Calcule " + (tipo === "var" ? "a variância" : "o desvio padrão") + " populacional (dividindo por n) de " + $(lista(xs)) + ".", v, d: { xs, tipo },
      ops: [{ v: tipo === "var" ? sd : vr, why: tipo === "var" ? "deu o desvio padrão (a raiz)" : "esqueceu a raiz (isso é a variância)" },
            { v: tipo === "var" ? sq / (k - 1) : Math.sqrt(sq / (k - 1)), why: "dividiu por n − 1 (a amostral)" }, { v: sum(dv.map(Math.abs)) / k, why: "usou o módulo em vez do quadrado" }],
      x: "A média é " + $(String(mu)) + ". Desvios: " + $(lista(xs.map(x => x - mu))) + ". " + $("\\sigma^2 = \\dfrac{" + sq + "}{" + k + "} = " + n(vr)) +
         (tipo === "dp" ? " e " + $("\\sigma = \\sqrt{" + n(vr) + "} \\approx " + n(sd)) : "") + "." };
  } };

  G.zscore = { t: "Escore z (padronização)", f: (R, p) => {
    const mu = R.pick([50, 60, 70, 100, 500]), sd = R.pick([2, 4, 5, 10, 15, 20]), z = R.pick([-2, -1.5, -1, 0.5, 1, 1.5, 2, 2.5, 3]), x = mu + z * sd;
    return { q: "Com média " + $(String(mu)) + " e desvio padrão " + $(String(sd)) + ", qual é o escore " + $("z = \\dfrac{x - \\mu}{\\sigma}") + " de " + $("x = " + n(x)) + "?", v: z, d: { mu, sd, x },
      ops: [{ v: x - mu, why: "não dividiu pelo desvio padrão" }, { v: r2(x / sd), why: "esqueceu de subtrair a média" }, { v: r2((x - mu) / (sd * sd)), why: "dividiu pela variância" }],
      x: $("z = \\dfrac{" + n(x) + " - " + mu + "}{" + sd + "} = " + n(z)) + ": o valor está a " + nt(Math.abs(z)) + " desvio" + (Math.abs(z) === 1 ? "" : "s") + " padrão " + (z > 0 ? "acima" : "abaixo") + " da média. A LayerNorm faz essa conta em cada vetor." };
  } };

  // ---------------- Esperança, covariância e correlação ----------------
  G.esper = { t: "Esperança (valor esperado)", f: (R, p) => {
    const k = R.int(3, 4), xs = R.shuffle([0, 1, 2, 3, 5, 10]).slice(0, k).sort((a, b) => a - b), ps = partes(R, k, 10).map(x => x / 10), E = r2(dot(xs, ps));
    return { q: "X vale " + $(lista(xs)) + " com probabilidades " + $(lista(ps)) + ". Quanto vale " + $("\\mathbb{E}[X]") + "?", v: E, d: { xs, ps },
      ops: [{ v: r2(media(xs)), why: "fez a média simples, ignorando as probabilidades" }, { v: 1, why: "somou as probabilidades" }, { v: xs[ps.indexOf(Math.max(...ps))], why: "pegou o valor mais provável" }],
      x: "Valor vezes probabilidade, tudo somado: " + $(xs.map((x, i) => n(x) + "\\cdot " + n(ps[i])).join(" + ") + " = " + n(E)) + "." };
  } };

  G.esperjogo = { t: "Ganho esperado de uma aposta", f: (R, p) => {
    const pw = R.pick([0.1, 0.2, 0.25, 0.4, 0.5]), W = R.pick([10, 20, 50, 100]), Lo = R.pick([5, 10, 20]), v = r2(pw * W - (1 - pw) * Lo);
    return { q: "Uma aposta paga " + W + " reais com probabilidade " + nt(pw) + "; senão, você perde " + Lo + " reais. Qual é o ganho esperado por aposta?", v, fmt: reais, d: { pw, W, Lo },
      ops: [{ v: pw * W, why: "esqueceu as perdas" }, { v: r2(pw * W + (1 - pw) * Lo), why: "somou a perda em vez de subtrair" }, { v: W - Lo, why: "ignorou as probabilidades" }],
      x: $(n(pw) + "\\cdot " + W + " - " + n(r2(1 - pw)) + "\\cdot " + Lo + " = " + n(pw * W) + " - " + n(r2((1 - pw) * Lo)) + " = " + n(v)) + (v < 0 ? ": em média, você perde." : ": em média, você ganha.") };
  } };

  G.cov = { t: "Covariância", f: (R, p) => {
    const k = R.pick([4, 5]), pats = k === 4 ? [[-3, -1, 1, 3], [-2, -1, 1, 2], [-1, -1, 1, 1]] : [[-2, -1, 0, 1, 2], [-3, -1, 0, 1, 3], [-2, -2, 0, 2, 2]];
    const dx = R.shuffle(R.pick(pats)), dy = R.shuffle(R.pick(pats)).map(x => x * R.pick([1, 1, -1, 2]));
    const mx = R.int(2, 9), my = R.int(2, 9), xs = dx.map(x => x + mx), ys = dy.map(y => y + my), s = dot(dx, dy), cv = s / k;
    const corr = s / Math.sqrt(dot(dx, dx) * dot(dy, dy));
    return { q: "Calcule a covariância populacional de " + $("x = " + V(xs)) + " e " + $("y = " + V(ys)) + ".", v: cv, d: { xs, ys },
      ops: [{ v: s / (k - 1), why: "dividiu por n − 1" }, { v: r2(dot(xs, ys) / k), why: "esqueceu de subtrair as médias" }, { v: r2(corr), why: "calculou a correlação" }],
      x: "Médias: " + $("\\bar x = " + mx) + " e " + $("\\bar y = " + my) + ". Produtos dos desvios: " + $(dx.map((a, i) => P(a) + "\\cdot " + P(dy[i])).join(" + ") + " = " + n(s)) +
         ". Dividindo por " + k + ": " + $(n(cv)) + "." };
  } };

  G.corrsinal = { t: "Correlação de Pearson", f: (R, p) => {
    const sh = R.int(0, 3), xs = [-2, -1, 0, 1, 2].map(x => x + sh), curva = R.rnd() < 0.3;
    const a = R.pick([-3, -2, -0.5, 0.5, 2, 3, -1, 1]), b = R.int(-3, 5), mx = media(xs);
    const ys = curva ? xs.map(x => (x - mx) * (x - mx)) : xs.map(x => a * x + b), r = curva ? 0 : Math.sign(a);
    return { q: "Os pontos têm " + $("x = " + V(xs)) + " e " + $("y = " + V(ys)) + ". Quanto vale a correlação de Pearson entre x e y?", v: r, fmt: v => $(n(v)), d: { xs, ys },
      ops: (curva ? [{ v: 1, why: "existe relação, mas ela não é linear" }, { v: -1, why: "" }, { v: 0.5, why: "" }]
                  : [{ v: -r, why: "errou o sentido da relação" }, { v: 0, why: "achou que não há relação" }, { v: a, why: "confundiu correlação com inclinação" }]),
      x: curva ? "y é o quadrado da distância até o centro: sobe dos dois lados. A relação existe, mas não é linear, e os efeitos se cancelam: r = 0."
               : "Os pontos estão exatamente numa reta " + (a > 0 ? "subindo" : "descendo") + " (" + $("y = " + n(a) + "x " + (b < 0 ? "- " + n(-b) : "+ " + n(b))) + "), então " + $("r = " + n(r)) +
                 ". A inclinação não importa: só a direção e o quanto os pontos se afastam da reta." };
  } };

  // ---------------- Probabilidade condicional e Bayes ----------------
  G.bayes = { t: "Teorema de Bayes (teste médico)", f: (R, p) => {
    const prev = R.pick([0.01, 0.02, 0.05, 0.1]), sens = R.pick([0.9, 0.95, 0.99]), fp = R.pick([0.05, 0.1, 0.02]);
    const N = 10000, doentes = N * prev, vp = sens * doentes, falsos = fp * (N - doentes), post = vp / (vp + falsos);
    return { q: "Uma doença atinge " + nt(prev * 100) + "% das pessoas. O teste detecta " + nt(sens * 100) + "% dos doentes e dá falso positivo em " + nt(fp * 100) +
             "% dos saudáveis. Se o teste deu positivo, qual a chance de a pessoa estar doente?", v: 100 * post, fmt: pctF, casas: 1, d: { prev, sens, fp },
      ops: [{ v: 100 * sens, why: "confundiu P(+ | doente) com P(doente | +)" }, { v: 100 * sens * prev, why: "esqueceu de dividir por P(+)" }, { v: 100 * (1 - fp), why: "usou a especificidade" }],
      x: "Em " + milhar(N) + " pessoas: " + milhar(doentes) + " doentes, dos quais " + milhar(vp) + " dão positivo; e " + milhar(N - doentes) + " saudáveis, com " + milhar(falsos) +
         " falsos positivos. Entre os positivos: " + $("\\dfrac{" + milhar(vp) + "}{" + milhar(vp) + " + " + milhar(falsos) + "} \\approx " + n(100 * post, 1) + "\\%") + "." };
  } };

  G.condtab = { t: "Probabilidade condicional numa tabela", f: (R, p) => {
    const a = R.int(10, 60), b = R.int(5, 40), c = R.int(5, 40), d0 = R.int(40, 200), N = a + b + c + d0;
    // tabela em bloco ($$), numa linha só dela; ``…'' são as aspas do LaTeX
    const tab = "\\begin{array}{l|cc} & \\text{tem ``grátis''} & \\text{não tem} \\\\ \\hline \\text{spam} & " + a + " & " + b + " \\\\ \\text{normal} & " + c + " & " + d0 + " \\end{array}";
    return { q: "Contagem de e-mails: $$" + tab + "$$ Qual é " + $("P(\\text{spam} \\mid \\text{tem ``grátis''})") + "?", v: 100 * a / (a + c), fmt: pctF, casas: 1, d: { a, b, c, d0 },
      ops: [{ v: 100 * a / N, why: "calculou P(spam e grátis), a conjunta" }, { v: 100 * a / (a + b), why: "calculou P(grátis | spam), a inversa" }, { v: 100 * (a + c) / N, why: "calculou P(grátis)" }],
      x: "A barra manda olhar só a coluna \"tem grátis\": " + $(String(a + c)) + " e-mails, dos quais " + $(String(a)) + " são spam. " + $("\\dfrac{" + a + "}{" + (a + c) + "} \\approx " + n(100 * a / (a + c), 1) + "\\%") + "." };
  } };

  G.odds = { t: "Bayes na forma de chances", f: (R, p) => {
    const k = R.pick([1, 3, 4, 9, 19]), LR = R.pick([2, 3, 4, 9]), post = LR / (LR + k);
    return { q: "A priori, as chances de um e-mail ser spam são de 1 para " + k + ". A palavra \"grátis\" aparece " + LR + " vezes mais em spam do que em e-mail normal. Vendo a palavra, qual a probabilidade de ser spam?",
      v: 100 * post, fmt: pctF, casas: 1, d: { k, LR },
      ops: [{ v: 100 * LR / k, why: "leu as chances como se fossem a probabilidade" }, { v: 100 * Math.min(1, LR / (1 + k)), why: "multiplicou a probabilidade a priori pela razão" }, { v: 100 / (1 + k), why: "ficou com a probabilidade a priori" }],
      x: "Chances a posteriori = chances a priori × razão: " + $("1 : " + k + " \\times " + LR + " = " + LR + " : " + k) + ". Em probabilidade: " + $("\\dfrac{" + LR + "}{" + LR + " + " + k + "} \\approx " + n(100 * post, 1) + "\\%") + "." };
  } };

  G.pelomenos = { t: "Pelo menos um sucesso", f: (R, p) => {
    const pr = R.pick([0.5, 0.1, 0.2, 0.3]), m = R.int(2, 4), v = 1 - Math.pow(1 - pr, m);
    return { q: "Cada tentativa dá certo com probabilidade " + nt(pr) + ", de forma independente. Em " + m + " tentativas, qual a chance de pelo menos uma dar certo?", v: 100 * v, fmt: pct2, d: { pr, m },
      ops: [{ v: 100 * m * pr, why: "somou as probabilidades" }, { v: 100 * Math.pow(pr, m), why: "calculou a chance de todas darem certo" }, { v: 100 * Math.pow(1 - pr, m), why: "calculou a chance de nenhuma dar certo" }],
      x: "Pelo menos uma = 1 − nenhuma: " + $("1 - " + n(1 - pr) + "^{" + m + "} = 1 - " + n(Math.pow(1 - pr, m), 4) + " = " + n(100 * v, 2) + "\\%") + "." };
  } };

  // ---------------- Normal, amostragem e testes ----------------
  const REGRA = { 1: 68, 2: 95, 3: 99.7 };
  G.regra689 = { t: "Regra 68-95-99,7", f: (R, p) => {
    const mu = R.pick([100, 70, 50, 170]), sd = R.pick([5, 10, 15, 2]), k = R.int(1, 3), v = REGRA[k];
    const outras = [v / 2, 68, 95, 99.7, 50].filter(x => x !== v);
    return { q: "Uma grandeza segue uma normal com média " + mu + " e desvio padrão " + sd + ". Que porcentagem fica entre " + (mu - k * sd) + " e " + (mu + k * sd) + "?", v, fmt: pctF, casas: 1, d: { k },
      ops: outras.map(x => ({ v: x, why: x === v / 2 ? "contou só um lado da média" : "" })),
      x: "O intervalo é a média ± " + k + " desvio" + (k > 1 ? "s" : "") + " padrão: pela regra 68-95-99,7, ali ficam cerca de " + $(n(v, 1) + "\\%") + " dos valores." };
  } };

  G.normtail = { t: "Cauda da distribuição normal", f: (R, p) => {
    const k = R.int(1, 2), mu = R.pick([100, 50, 70]), sd = R.pick([5, 10, 15]), cima = R.rnd() < 0.5, v = (100 - REGRA[k]) / 2;
    return { q: "Numa normal com média " + mu + " e desvio padrão " + sd + ", que porcentagem fica " + (cima ? "acima de " + (mu + k * sd) : "abaixo de " + (mu - k * sd)) + "?", v, fmt: pctF, casas: 1, d: { k },
      ops: [{ v: 100 - REGRA[k], why: "somou as duas caudas" }, { v: REGRA[k] / 2, why: "pegou o pedaço entre a média e o corte" }, { v: (100 + REGRA[k]) / 2, why: "pegou o lado de dentro" }],
      x: "Entre ± " + k + " desvio" + (k > 1 ? "s" : "") + " ficam " + REGRA[k] + "%. Sobram " + (100 - REGRA[k]) + "%, divididos igualmente entre as duas caudas: " + $(n(v, 1) + "\\%") + " de cada lado." };
  } };

  G.bernoulliL = { t: "Verossimilhança de uma sequência", f: (R, p) => {
    const m = R.int(2, 4), h = R.int(0, m), pr = R.pick([0.5, 0.2, 0.8, 0.6, 0.4]), seq = R.shuffle(Array(h).fill("cara").concat(Array(m - h).fill("coroa")));
    const v = Math.pow(pr, h) * Math.pow(1 - pr, m - h);
    return { q: "Numa moeda com " + $("P(\\text{cara}) = " + n(pr)) + ", qual é a verossimilhança da sequência " + seq.join(", ") + "?", v, casas: 4, fmt: x => $(n(x, 4)), d: { m, h, pr },
      ops: [{ v: Math.pow(pr, h), why: "esqueceu as coroas" }, { v: h / m, why: "deu a proporção de caras" }, { v: Math.pow(1 - pr, h) * Math.pow(pr, m - h), why: "trocou cara e coroa" }],
      x: "Multiplique a probabilidade de cada lançamento: " + $(seq.map(s => (s === "cara" ? n(pr) : n(r2(1 - pr)))).join(" \\cdot ") + " = " + n(v, 4)) + "." };
  } };

  G.erropadrao = { t: "Erro padrão da média", f: (R, p) => {
    const sd = R.pick([2, 5, 10, 12, 20]), m = R.pick([4, 16, 25, 100, 400]), v = sd / Math.sqrt(m);
    return { q: "Uma medida tem desvio padrão " + sd + ". Qual é o erro padrão da média de " + m + " medidas?", v, casas: 3, d: { sd, m },
      ops: [{ v: sd / m, why: "dividiu por n, não por √n" }, { v: sd * Math.sqrt(m), why: "multiplicou pela raiz" }, { v: sd * sd / m, why: "usou a variância" }],
      x: $("SE = \\dfrac{\\sigma}{\\sqrt{n}} = \\dfrac{" + sd + "}{\\sqrt{" + m + "}} = \\dfrac{" + sd + "}{" + Math.sqrt(m) + "} = " + n(v, 3)) + "." };
  } };

  G.amostra4x = { t: "Quanto aumentar a amostra", f: (R, p) => {
    const k = R.pick([2, 3, 4, 10]), v = k * k;
    return { q: "Para o erro padrão da média cair para 1/" + k + " do atual, por quanto é preciso multiplicar o tamanho da amostra?", v, d: { k },
      ops: [{ v: k, why: "achou que o erro cai na mesma proporção que n cresce" }, { v: 2 * k, why: "" }, { v: r2(Math.sqrt(k)), why: "inverteu a relação da raiz" }],
      x: "O erro padrão é " + $("\\sigma/\\sqrt{n}") + ". Para dividi-lo por " + k + ", " + $("\\sqrt{n}") + " precisa ficar " + k + " vezes maior, ou seja, n fica " + $(k + "^2 = " + v) + " vezes maior." };
  } };

  G.ic95 = { t: "Intervalo de confiança de 95%", f: (R, p) => {
    const [sd, m] = R.pick([[10, 100], [20, 100], [15, 25], [8, 16], [12, 36], [30, 225]]), xb = R.int(20, 120), se = sd / Math.sqrt(m), mg = 1.96 * se;
    const fmt = v => $("[" + n(v[0]) + ";\\ " + n(v[1]) + "]");
    return { q: "Uma amostra de " + m + " medidas tem média " + xb + ", e o desvio padrão é " + sd + ". Qual é o intervalo de 95% para a média (use 1,96)?", v: [xb - mg, xb + mg], fmt, d: { xb, sd, m },
      ops: [{ v: [xb - 1.96 * sd, xb + 1.96 * sd], why: "esqueceu de dividir por √n" }, { v: [xb - se, xb + se], why: "esqueceu o 1,96" }, { v: [xb - 1.96 * sd / m, xb + 1.96 * sd / m], why: "dividiu por n" }],
      x: $("SE = " + sd + "/\\sqrt{" + m + "} = " + n(se)) + " e a margem é " + $("1{,}96 \\cdot " + n(se) + " = " + n(mg)) + ". Intervalo: " + fmt([xb - mg, xb + mg]) + "." };
  } };

  const PV = { rej: "Rejeita H₀: a diferença é estatisticamente significativa", nrej: "Não rejeita H₀: os dados são compatíveis com nenhum efeito",
               prova: "Prova que H₀ é verdadeira", certeza: "Mostra a chance de H₀ ser verdadeira" };
  G.pvalor = { t: "Decisão com o p-valor", f: (R, p) => {
    const pv = R.pick([0.001, 0.01, 0.03, 0.04, 0.06, 0.2, 0.5]), alpha = R.pick([0.05, 0.01]), cat = pv < alpha ? "rej" : "nrej";
    return { q: "Num teste com nível de significância " + $("\\alpha = " + n(alpha)) + ", o p-valor deu " + $(n(pv, 3)) + ". O que se conclui?", v: cat, fmt: c => PV[c], d: { pv, alpha },
      ops: ["rej", "nrej", "prova", "certeza"].filter(c => c !== cat).map(c => ({ v: c, why: c === "prova" ? "um teste nunca prova H₀" : c === "certeza" ? "o p-valor não é a chance de H₀ ser verdadeira" : "" })),
      x: (pv < alpha ? "p = " + nt(pv, 3) + " é menor que α = " + nt(alpha) + ": rejeita-se H₀." : "p = " + nt(pv, 3) + " não é menor que α = " + nt(alpha) + ": não se rejeita H₀.") +
         " O p-valor é a chance de ver dados tão extremos <b>se</b> H₀ fosse verdadeira, e não a chance de H₀ ser verdadeira." };
  } };

  G.zteste = { t: "Estatística z de um teste", f: (R, p) => {
    const mu0 = R.pick([100, 50, 70]), sd = R.pick([10, 15, 20]), m = R.pick([25, 100, 16, 36]), se = sd / Math.sqrt(m), z = R.pick([-2.5, -1.5, -1, 0.5, 1, 1.5, 2, 2.5, 3]), xb = mu0 + z * se;
    return { q: "H₀ diz que a média é " + mu0 + ". Uma amostra de " + m + " medidas (desvio padrão " + sd + ") deu média " + nt(xb) + ". Quanto vale " + $("z = \\dfrac{\\bar x - \\mu_0}{\\sigma/\\sqrt{n}}") + "?",
      v: z, d: { mu0, sd, m, xb },
      ops: [{ v: r2((xb - mu0) / sd), why: "esqueceu o √n" }, { v: r2((xb - mu0) / (sd / m)), why: "dividiu por n" }, { v: r2(xb - mu0), why: "não dividiu pelo erro padrão" }],
      x: $("\\sigma/\\sqrt{n} = " + sd + "/" + Math.sqrt(m) + " = " + n(se)) + " e " + $("z = \\dfrac{" + n(xb) + " - " + mu0 + "}{" + n(se) + "} = " + n(z)) + (Math.abs(z) > 1.96 ? ". Passa de 1,96: significativo a 5%." : ". Não passa de 1,96: não é significativo a 5%.") };
  } };

  // ---------------- Máxima verossimilhança, viés e variância, comparar modelos ----------------
  G.mlebern = { t: "Máxima verossimilhança de uma moeda", f: (R, p) => {
    const m = R.pick([8, 10, 20, 25, 50]), h = R.int(1, m - 1);
    return { q: "Em " + m + " lançamentos saíram " + h + " caras. Qual é a estimativa de máxima verossimilhança de " + $("P(\\text{cara})") + "?", v: h / m, casas: 3, d: { m, h },
      ops: [{ v: (h + 1) / (m + 2), why: "usou a correção de Laplace, que não é a máxima verossimilhança" }, { v: (m - h) / m, why: "pegou a proporção de coroas" }, { v: 0.5, why: "supôs a moeda honesta" }],
      x: "A verossimilhança " + $("p^{" + h + "}(1-p)^{" + (m - h) + "}") + " é máxima na proporção observada: " + $("\\hat p = " + h + "/" + m + " = " + n(h / m, 3)) + "." };
  } };

  G.nll = { t: "Log-verossimilhança negativa (NLL)", f: (R, p) => {
    const ps = Array.from({ length: 3 }, () => R.pick([1, 0.5, 0.25, 0.8, 0.9, 0.1])), v = -sum(ps.map(ln));
    return { q: "O modelo deu às respostas certas de 3 exemplos as probabilidades " + $(lista(ps)) + ". Quanto vale a NLL, " + $("-\\sum \\ln p_i") + "?", v, d: { ps },
      ops: [{ v: sum(ps.map(ln)), why: "esqueceu o sinal de menos" }, { v: ps.reduce((a, b) => a * b, 1), why: "calculou a verossimilhança, sem log" }, { v: 3 - sum(ps), why: "somou 1 − p em vez de usar o log" }],
      x: $("-(" + ps.map(x => "\\ln " + n(x)).join(" + ") + ") = -(" + ps.map(x => P(r2(ln(x)))).join(" + ") + ") \\approx " + n(v)) + ". Probabilidade 1 não custa nada; quanto menor a probabilidade, maior a perda." };
  } };

  G.mlemu = { t: "Máxima verossimilhança da média", f: (R, p) => {
    const k = R.pick([4, 5]), xs = R.vec(k, 0, 12), m = media(xs), s = xs.slice().sort((a, b) => a - b);
    return { q: "Os dados " + $(lista(xs)) + " vieram de uma normal com desvio padrão conhecido. Qual " + $("\\mu") + " maximiza a verossimilhança?", v: m, d: { xs },
      ops: [{ v: mediana(xs), why: "pegou a mediana (ela minimiza o erro absoluto, não o quadrático)" }, { v: (s[0] + s[k - 1]) / 2, why: "pegou o meio entre o menor e o maior" }, { v: sum(xs) / (k - 1), why: "dividiu por n − 1" }],
      x: "Maximizar a verossimilhança da normal é minimizar a soma dos quadrados dos desvios, e quem faz isso é a média: " + $(n(m)) + "." };
  } };

  G.biasvar = { t: "Erro = viés² + variância + ruído", f: (R, p) => {
    const b = R.pick([0.5, 1, 1.5, 2]), va = R.pick([0.5, 1, 2, 3]), ru = R.pick([0.25, 0.5, 1]), v = b * b + va + ru;
    return { q: "Um modelo tem viés " + nt(b) + ", variância " + nt(va) + " e ruído irredutível " + nt(ru) + ". Qual é o erro quadrático esperado?", v, d: { b, va, ru },
      ops: [{ v: b + va + ru, why: "esqueceu de elevar o viés ao quadrado" }, { v: b * b + va, why: "esqueceu o ruído" }, { v: (b + va) * (b + va), why: "elevou a soma ao quadrado" }],
      x: $(n(b) + "^2 + " + n(va) + " + " + n(ru) + " = " + n(b * b) + " + " + n(va) + " + " + n(ru) + " = " + n(v)) + ". O ruído não some com modelo nenhum." };
  } };

  const DIAG = { under: "Underfitting (viés alto): o modelo é simples demais", over: "Overfitting (variância alta): o modelo decorou o treino",
                 bom: "Bom ajuste: erros baixos e parecidos", dados: "Os dados de validação estão errados" };
  G.diagfit = { t: "Diagnóstico pelo erro de treino e validação", f: (R, p) => {
    const cat = R.pick(["under", "over", "bom"]);
    const tr = cat === "under" ? R.int(28, 40) : cat === "over" ? R.int(1, 5) : R.int(3, 8);
    const va = cat === "over" ? tr + R.int(15, 30) : tr + R.int(1, 3);
    return { q: "Erro no treino: " + tr + "%. Erro na validação: " + va + "%. Qual é o diagnóstico mais provável?", v: cat, fmt: c => DIAG[c], d: { tr, va },
      ops: ["under", "over", "bom", "dados"].filter(c => c !== cat).map(c => ({ v: c, why: "" })),
      x: cat === "under" ? "Erra muito até no treino: falta capacidade. Use um modelo maior ou mais atributos."
         : cat === "over" ? "Vai muito bem no treino e mal na validação: decorou. Use regularização, mais dados ou early stopping."
         : "Os dois erros são baixos e próximos: o modelo generaliza bem." };
  } };

  G.amostrasn = { t: "Quantas perguntas de teste são necessárias", f: (R, p) => {
    const pr = R.pick([0.5, 0.8, 0.9, 0.7]), d = R.pick([0.02, 0.05, 0.1]), v = 16 * pr * (1 - pr) / (d * d);
    return { q: "Para detectar uma diferença de " + nt(d * 100) + " pontos percentuais entre dois modelos com acurácia perto de " + nt(pr * 100) + "%, use " + $("n \\approx 16\\,p(1-p)/d^2") + ". Quantas perguntas são necessárias?",
      v, fmt: x => milhar(x) + " perguntas", d: { pr, d },
      ops: [{ v: 16 * pr * (1 - pr) / d, why: "esqueceu de elevar d ao quadrado" }, { v: 16 * pr / (d * d), why: "usou p em vez de p(1 − p)" }, { v: 16 / (d * d), why: "esqueceu o p(1 − p)" }],
      x: $("16 \\cdot " + n(pr) + " \\cdot " + n(r2(1 - pr)) + " / " + n(d) + "^2 = " + n(16 * pr * (1 - pr), 2) + " / " + n(d * d, 4) + " = " + milhar(v)) + ". Diferenças pequenas exigem muitos testes." };
  } };

  const ICD = { pos: "A diferença é real: o modelo B é melhor", neg: "A diferença é real: o modelo A é melhor", acaso: "Pode ser acaso: o intervalo contém o zero",
                media: "B é melhor, porque o centro do intervalo é positivo" };
  G.icdiff = { t: "Bootstrap: a diferença é real?", f: (R, p) => {
    const tipo = R.pick(["pos", "neg", "acaso", "acaso"]);
    let lo, hi; if (tipo === "pos") { lo = R.int(1, 15) / 10; hi = lo + R.int(5, 40) / 10; } else if (tipo === "neg") { hi = -R.int(1, 15) / 10; lo = hi - R.int(5, 40) / 10; }
    else { lo = -R.int(2, 20) / 10; hi = R.int(5, 30) / 10; }
    return { q: "No bootstrap pareado, o intervalo de 95% para (acurácia de B − acurácia de A) deu " + $("[" + n(lo) + ";\\ " + n(hi) + "]") + " pontos percentuais. O que concluir?",
      v: tipo, fmt: c => ICD[c], d: { lo, hi },
      ops: ["pos", "neg", "acaso", "media"].filter(c => c !== tipo).map(c => ({ v: c, why: "" })),
      x: tipo === "acaso" ? "O intervalo vai do negativo ao positivo: o zero está dentro, então não dá para descartar que os modelos sejam iguais."
         : "O intervalo inteiro está " + (tipo === "pos" ? "acima" : "abaixo") + " de zero: a diferença se mantém em quase todos os sorteios." };
  } };

  G.acuraciase = { t: "Margem de erro de uma acurácia", f: (R, p) => {
    const [pr, m] = R.pick([[0.9, 100], [0.8, 400], [0.5, 100], [0.9, 400], [0.5, 400], [0.8, 100], [0.5, 2500]]), se = Math.sqrt(pr * (1 - pr) / m), v = 200 * se;
    return { q: "Um modelo acertou " + nt(pr * 100) + "% de " + m + " perguntas. Qual é a margem de erro de 95% (≈ 2 erros padrão), em pontos percentuais?", v, fmt: x => "± " + nt(x, 2) + " pontos percentuais", d: { pr, m },
      ops: [{ v: 100 * se, why: "esqueceu o fator 2 (≈ 1,96)" }, { v: 200 * pr * (1 - pr) / m, why: "esqueceu a raiz" }, { v: 200 * Math.sqrt(pr / m), why: "usou p em vez de p(1 − p)" }],
      x: $("2\\sqrt{\\dfrac{" + n(pr) + "\\cdot " + n(r2(1 - pr)) + "}{" + m + "}} = 2 \\cdot " + n(se, 3) + " = " + n(v / 100, 3)) + ", ou seja, ± " + nt(v, 2) + " pontos percentuais." };
  } };

  // ---------------- Teoria da informação ----------------
  const DIST = [[0.5, 0.5], [0.5, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.5, 0.25, 0.125, 0.125], [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125], [0.5, 0.125, 0.125, 0.125, 0.125], [0.25, 0.25, 0.5]];
  G.entropia = { t: "Entropia de Shannon", f: (R, p) => {
    const ps = R.shuffle(R.pick(DIST)), H = -sum(ps.map(x => x * lg2(x))), k = ps.length;
    return { q: "Qual é a entropia, em bits, da distribuição " + $(lista(ps)) + "?", v: H, casas: 3, d: { ps },
      ops: [{ v: -H, why: "esqueceu o sinal de menos" }, { v: lg2(k), why: "usou o máximo, como se fosse uniforme" }, { v: k, why: "contou os resultados" }],
      x: $("H = -\\sum p_i \\log_2 p_i = " + ps.map(x => n(x, 3) + "\\cdot " + n(-lg2(x))).join(" + ") + " = " + n(H, 3)) + " bits." };
  } };

  G.surpresa = { t: "Surpresa (autoinformação)", f: (R, p) => {
    const k = R.int(1, 10), den = Math.pow(2, k);
    return { q: "Um evento tem probabilidade " + $("\\tfrac{1}{" + den + "}") + ". Quanto vale a surpresa " + $("I = -\\log_2 p") + ", em bits?", v: k, d: { den },
      ops: [{ v: -k, why: "esqueceu o sinal de menos" }, { v: den, why: "deu 1/p, sem o log" }, { v: r2(k * Math.log(2)), why: "usou log natural (nats)" }],
      x: $("-\\log_2 \\tfrac{1}{" + den + "} = \\log_2 " + den + " = " + k) + ". Cada vez que a probabilidade cai pela metade, a surpresa sobe 1 bit." };
  } };

  G.entmax = { t: "Entropia máxima", f: (R, p) => {
    const k = R.pick([2, 4, 8, 16, 32, 64, 256, 1024]);
    return { q: "Há " + k + " resultados igualmente prováveis. Qual é a entropia, em bits?", v: lg2(k), d: { k },
      ops: [{ v: k, why: "deu o número de resultados" }, { v: k / 2, why: "" }, { v: r2(Math.log(k)), why: "usou log natural (nats), não bits" }],
      x: "Na distribuição uniforme, cada resultado tem " + $("p = 1/" + k) + ", e " + $("H = \\log_2 " + k + " = " + lg2(k)) + " bits: o máximo possível com " + k + " resultados." };
  } };

  G.softmax = { t: "Softmax", f: (R, p) => {
    let z; do { z = [R.int(0, 4), R.int(0, 4), R.int(0, 4)]; } while (z.filter(x => x === Math.max(...z)).length > 1 || sum(z) === 0);
    const i = z.indexOf(Math.max(...z)), ex = z.map(Math.exp), v = ex[i] / sum(ex);
    return { q: "Os logits de 3 classes são " + $("z = " + V(z)) + ". Qual é a probabilidade da classe " + (i + 1) + " depois da softmax?", v, d: { z, i },
      ops: [{ v: z[i] / sum(z), why: "dividiu os logits sem exponenciar" }, { v: 1 / 3, why: "achou que fica uniforme" }, { v: r2(ex[i]), why: "não dividiu pela soma" }],
      x: $("e^{" + z.join("} ,\\ e^{") + "}") + " valem " + $(lista(ex.map(r2))) + ", que somam " + $(n(sum(ex))) + ". Então " + $("\\dfrac{" + n(ex[i]) + "}{" + n(sum(ex)) + "} \\approx " + n(v)) + "." };
  } };

  G.ce = { t: "Entropia cruzada de um exemplo", f: (R, p) => {
    const pr = R.pick([0.5, 0.25, 0.1, 0.9, 0.8, 0.6, 0.05]);
    return { q: "O modelo deu probabilidade " + nt(pr) + " à classe certa. Quanto vale a perda de entropia cruzada " + $("-\\ln p") + " desse exemplo?", v: -ln(pr), d: { pr },
      ops: [{ v: 1 - pr, why: "usou 1 − p, sem o log" }, { v: r2(-lg2(pr)), why: "usou log na base 2 (o PyTorch usa ln)" }, { v: r2(ln(pr)), why: "esqueceu o sinal de menos" }],
      x: $("-\\ln " + n(pr) + " \\approx " + n(-ln(pr))) + ". Acertar com confiança custa pouco; dar probabilidade baixa à classe certa custa muito." };
  } };

  G.cegrad = { t: "Gradiente de softmax + entropia cruzada", f: (R, p) => {
    const ps = partes(R, 3, 10).map(x => x / 10), c = R.int(0, 2), y = [0, 1, 2].map(j => (j === c ? 1 : 0)), g = ps.map((x, j) => r2(x - y[j]));
    return { q: "Depois da softmax, as probabilidades são " + $("p = " + V(ps)) + " e a classe certa é a " + (c + 1) + "ª. Qual é o gradiente da perda em relação aos logits?", v: g, d: { ps, c },
      ops: [{ v: g.map(x => -x), why: "fez y − p" }, { v: ps.slice(), why: "esqueceu de subtrair y" }, { v: ps.map((x, j) => (j === c ? r2(x - 1) : 0)), why: "mexeu só na classe certa" }],
      x: "Com softmax e entropia cruzada juntas, o gradiente é " + $("p - y = " + V(ps) + " - " + V(y) + " = " + V(g)) + ": empurra a classe certa para cima e as outras para baixo." };
  } };

  G.kl = { t: "Divergência KL", f: (R, p) => {
    const k = R.int(2, 3); let Pd, Qd;
    do { Pd = partes(R, k, 10).map(x => x / 10); Qd = partes(R, k, 10).map(x => x / 10); } while (Pd.every((x, i) => x === Qd[i]));
    const kl = (a, b) => sum(a.map((x, i) => x * lg2(x / b[i]))), v = kl(Pd, Qd);
    return { q: "Calcule " + $("D_{KL}(P \\parallel Q) = \\sum p_i \\log_2 \\dfrac{p_i}{q_i}") + " para " + $("P = " + V(Pd)) + " e " + $("Q = " + V(Qd)) + ".", v, casas: 3, d: { P: Pd, Q: Qd },
      ops: [{ v: kl(Qd, Pd), why: "inverteu P e Q (a KL não é simétrica)" }, { v: -sum(Pd.map((x, i) => x * lg2(Qd[i]))), why: "calculou a entropia cruzada H(P, Q)" }, { v: 0, why: "achou que dá zero" }],
      x: $(Pd.map((x, i) => n(x) + "\\log_2 \\tfrac{" + n(x) + "}{" + n(Qd[i]) + "}").join(" + ") + " \\approx " + n(v, 3)) + " bits. Só dá zero quando P = Q." };
  } };

  G.ceent = { t: "Entropia cruzada = entropia + KL", f: (R, p) => {
    const HP = R.pick([0.8, 1, 1.5, 2]), KL = R.pick([0.1, 0.2, 0.3, 0.5]), HPQ = HP + KL;
    return { q: "A entropia de P é " + nt(HP) + " bits e a entropia cruzada " + $("H(P, Q)") + " é " + nt(HPQ) + " bits. Quanto vale " + $("D_{KL}(P \\parallel Q)") + "?", v: KL, d: { HP, HPQ },
      ops: [{ v: HP + HPQ, why: "somou" }, { v: r2(HPQ / HP), why: "dividiu" }, { v: -KL, why: "subtraiu na ordem errada" }],
      x: $("H(P, Q) = H(P) + D_{KL}(P \\parallel Q)") + ", então " + $("D_{KL} = " + n(HPQ) + " - " + n(HP) + " = " + n(KL)) + ". Minimizar a entropia cruzada é minimizar a KL, porque H(P) dos dados é fixa." };
  } };

  // ---------------- Funções de perda ----------------
  const erros = R => { const y = R.vec(4, 0, 10); let e; do { e = R.vec(4, -3, 3); } while (e.every(x => x === 0)); return { y, yh: y.map((v, i) => v + e[i]), e }; };
  G.mse = { t: "Erro quadrático médio (MSE)", f: (R, p) => {
    const { y, yh, e } = erros(R), mse = media(e.map(x => x * x));
    return { q: "Alvos " + $("y = " + V(y)) + " e previsões " + $("\\hat y = " + V(yh)) + ". Quanto vale o MSE?", v: mse, d: { y, yh },
      ops: [{ v: media(e.map(Math.abs)), why: "calculou o MAE" }, { v: sum(e.map(x => x * x)), why: "esqueceu de dividir por n" }, { v: r2(Math.sqrt(mse)), why: "tirou a raiz (isso é o RMSE)" }],
      x: "Erros: " + $(V(e)) + ". Quadrados: " + $(V(e.map(x => x * x))) + ". Média: " + $(n(mse)) + "." };
  } };

  G.mae = { t: "Erro absoluto médio (MAE)", f: (R, p) => {
    const { y, yh, e } = erros(R), mae = media(e.map(Math.abs));
    return { q: "Alvos " + $("y = " + V(y)) + " e previsões " + $("\\hat y = " + V(yh)) + ". Quanto vale o MAE?", v: mae, d: { y, yh },
      ops: [{ v: media(e.map(x => x * x)), why: "elevou ao quadrado (MSE)" }, { v: Math.abs(media(e)), why: "fez a média com sinal: os erros se cancelam" }, { v: sum(e.map(Math.abs)), why: "esqueceu de dividir por n" }],
      x: "Erros: " + $(V(e)) + ". Módulos: " + $(V(e.map(Math.abs))) + ". Média: " + $(n(mae)) + "." };
  } };

  G.huber = { t: "Perda de Huber", f: (R, p) => {
    const r = R.pick([0.5, -0.5, 0.2, 2, -3, 4, 1.5, -2.5]), a = Math.abs(r), v = a <= 1 ? 0.5 * r * r : a - 0.5;
    return { q: "Com " + $("\\delta = 1") + ", quanto vale a perda de Huber para um erro de " + $(n(r)) + "?", v, casas: 3, d: { r },
      ops: [{ v: 0.5 * r * r, why: "usou a parte quadrática mesmo com erro grande" }, { v: a - 0.5, why: "usou a parte linear mesmo com erro pequeno" }, { v: a, why: "usou o erro absoluto puro" }, { v: r * r, why: "usou o quadrado sem o ½" }],
      x: (a <= 1 ? "Erro pequeno (|r| ≤ δ): parte quadrática, " + $("\\tfrac{1}{2} r^2 = " + n(v, 3))
                 : "Erro grande (|r| > δ): parte linear, " + $("\\delta(|r| - \\tfrac{1}{2}\\delta) = " + n(a) + " - 0{,}5 = " + n(v, 3))) + ". Assim um outlier não domina o gradiente." };
  } };
})();
"""
