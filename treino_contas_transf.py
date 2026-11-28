# -*- coding: utf-8 -*-
"""
Geradores de conta do Treino: Matemática, Módulo 5 do site (Matemática dos Transformers & Geometria de Embeddings).

Mesmo formato de treino_contas.py (que define as ferramentas TR.H usadas aqui). As respostas são refeitas com o
NumPy em treino_checagem.py.
"""

TR_GEN_JS = r"""
// =================== TREINO: geradores de conta (Transformers e embeddings) ===================
(() => {
  const G = TR.GEN;
  const { n, V, M, P, nt, $, dot, sum, add, mul, mv, r2, nrm, prods, signed, milhar } = TR.H;
  const V3 = x => V(x, 3);
  const sh = a => "<code>(" + a.join(", ") + ")</code>";
  const shStr = v => sh(String(v).split("x"));

  // ---------------- Alta dimensão ----------------
  G.quaseort = { t: "Quase-ortogonalidade em alta dimensão", f: (R, p) => {
    const d = R.pick([16, 64, 100, 256, 1024, 4096, 10000]), v = 1 / Math.sqrt(d);
    return { q: "Dois vetores aleatórios em " + $("\\mathbb{R}^{" + d + "}") + " têm cosseno com média 0 e desvio padrão de cerca de " + $("1/\\sqrt{d}") + ". Quanto dá esse desvio?",
      v, casas: 4, fmt: x => $("\\approx " + n(x, 4)), d: { d },
      ops: [{ v: 1 / d, why: "dividiu por d, sem a raiz" }, { v: Math.sqrt(d), why: "esqueceu de inverter" }, { v: 0.5, why: "" }],
      x: $("1/\\sqrt{" + d + "} = 1/" + n(Math.sqrt(d), 2) + " \\approx " + n(v, 4)) + ". Em dimensão alta, quase todo par de vetores aleatórios é quase perpendicular: cabem muitas direções praticamente independentes." };
  } };

  G.normsq = { t: "Comprimento típico de um vetor aleatório", f: (R, p) => {
    const d = R.pick([16, 64, 100, 256, 1024, 4096]), v = Math.sqrt(d);
    return { q: "Um vetor tem " + d + " coordenadas, cada uma com média 0 e variância 1. Qual é o comprimento (norma L2) típico dele?", v, d: { d },
      ops: [{ v: d, why: "esqueceu a raiz (isso é a norma ao quadrado)" }, { v: 1, why: "achou que ele já é unitário" }, { v: d / 2, why: "" }],
      x: "A norma ao quadrado é a soma de " + d + " quadrados com média 1: cerca de " + d + ". A norma fica perto de " + $("\\sqrt{" + d + "} = " + n(v)) + ". Por isso os embeddings costumam ser normalizados." };
  } };

  G.paramsffn = { t: "Pesos da camada feed-forward", f: (R, p) => {
    const dm = R.pick([256, 512, 768, 1024, 4096]), dff = 4 * dm, v = 2 * dm * dff;
    return { q: "Uma camada feed-forward de Transformer tem " + $("d_{model} = " + dm) + " e " + $("d_{ff} = 4\\,d_{model} = " + dff) +
             " (uma matriz sobe para " + dff + " e outra desce de volta). Quantos pesos ela tem, sem contar os vieses?", v, fmt: x => milhar(x) + " pesos", d: { dm },
      ops: [{ v: dm * dff, why: "contou uma matriz só" }, { v: dm * dm, why: "usou d × d" }, { v: 2 * dm + 2 * dff, why: "somou as dimensões em vez de multiplicar" }],
      x: "Duas matrizes de " + $(dm + " \\times " + dff) + ": " + $("2 \\cdot " + dm + " \\cdot " + dff + " = " + milhar(v)) + ". Boa parte dos parâmetros de um LLM mora nessas camadas, que funcionam como memória." };
  } };

  // ---------------- Normalização de embeddings ----------------
  G.normaliza = { t: "Normalizar um embedding", f: (R, p) => {
    const [base, L] = R.pick([[[3, 4], 5], [[6, 8], 10], [[5, 12], 13], [[1, 2, 2], 3], [[2, 3, 6], 7], [[8, 15], 17]]);
    const v = signed(R, R.shuffle(base)), u = v.map(x => x / L), s1 = sum(v.map(Math.abs)), mx = Math.max(...v.map(Math.abs));
    return { q: "Normalize " + $("v = " + V(v)) + " para comprimento 1, como se faz com embeddings.", v: u, casas: 3, fmt: x => $(V3(x)), d: { v },
      ops: [{ v: v.map(x => x / s1), why: "dividiu pela soma dos módulos (norma L1)" }, { v: v.map(x => x / (L * L)), why: "dividiu por ‖v‖²" }, { v: v.map(x => x / mx), why: "dividiu pelo maior valor" }],
      x: $("\\lVert v \\rVert = " + n(L)) + ", então " + $("v / \\lVert v \\rVert = " + V3(u)) + ". Confira: a soma dos quadrados dá 1." };
  } };

  G.dist2cos = { t: "Distância e cosseno na esfera unitária", f: (R, p) => {
    const c = R.pick([0.9, 0.8, 0.6, 0.5, 0.2, 0, -0.5]), D = 2 - 2 * c, tipo = R.pick(["d", "c"]);
    if (tipo === "d") return { q: "Dois embeddings normalizados (comprimento 1) têm cosseno " + $(n(c)) + ". Quanto vale " + $("\\lVert u - v \\rVert^2") + "?", v: D, d: { c, tipo },
      ops: [{ v: 1 - c, why: "esqueceu o fator 2" }, { v: 2 + 2 * c, why: "trocou o sinal" }, { v: Math.sqrt(D), why: "deu a distância, sem elevar ao quadrado" }],
      x: "Na esfera unitária, " + $("\\lVert u - v \\rVert^2 = 2 - 2\\cos\\theta = 2 - 2\\cdot " + P(c) + " = " + n(D)) + ". Por isso, com vetores normalizados, cosseno e distância ordenam os vizinhos do mesmo jeito." };
    return { q: "Dois embeddings normalizados estão a uma distância ao quadrado " + $("\\lVert u - v \\rVert^2 = " + n(D)) + ". Quanto vale o cosseno entre eles?", v: c, d: { c, tipo },
      ops: [{ v: r2(1 - D), why: "esqueceu de dividir por 2" }, { v: r2(D / 2), why: "" }, { v: r2(2 - D), why: "" }],
      x: "De " + $("\\lVert u - v \\rVert^2 = 2 - 2\\cos\\theta") + ": " + $("\\cos\\theta = 1 - " + n(D) + "/2 = " + n(c)) + "." };
  } };

  G.rmsnorm = { t: "RMSNorm", f: (R, p) => {
    const [b, rms] = R.pick([[[1, 1, 3, 5], 3], [[1, 5, 5, 7], 5], [[1, 1, 7, 7], 5], [[2, 2, 2, 2], 2], [[1, 7], 5], [[7, 17], 13], [[3, 3, 3, 3], 3]]);
    const x = signed(R, R.shuffle(b)), k = x.length, v = x.map(t => t / rms), mu = sum(x) / k, sd = Math.sqrt(sum(x.map(t => (t - mu) * (t - mu))) / k);
    return { q: "Aplique a RMSNorm (sem o ganho aprendido) em " + $("x = " + V(x)) + ": divida cada coordenada pela raiz da média dos quadrados.", v, casas: 3, fmt: t => $(V3(t)), d: { x },
      ops: [{ v: x.map(t => t / (sum(x.map(Math.abs)) / k)), why: "dividiu pela média dos módulos" }, { v: x.map(t => t / Math.sqrt(sum(x.map(q => q * q)))), why: "dividiu pela norma L2 (faltou a média)" },
            { v: sd ? x.map(t => (t - mu) / sd) : x.map(() => 0), why: "subtraiu a média: isso é a LayerNorm" }],
      x: "Média dos quadrados: " + $("(" + x.map(t => P(t) + "^2").join(" + ") + ")/" + k + " = " + n(rms * rms)) + ", e a raiz é " + $(n(rms)) + ". Dividindo: " + $(V3(v)) +
         ". A RMSNorm não subtrai a média: é mais barata que a LayerNorm e é a usada no Llama." };
  } };

  // ---------------- Query, Key, Value ----------------
  G.qkvshape = { t: "Shapes de Q, de QKᵀ e da saída da atenção", f: (R, p) => {
    const nt0 = R.pick([5, 10, 128, 512]), dm = R.pick([64, 512, 768]), dk = R.pick([16, 32, 48]), what = R.pick(["Q", "S", "O"]);
    const ans = what === "S" ? [nt0, nt0] : [nt0, dk];
    const pool = [...new Set([[nt0, dk], [nt0, nt0], [dm, dk], [dk, dk], [nt0, dm], [dk, nt0], [dm, dm]].map(a => a.join("x")))].filter(t => t !== ans.join("x"));
    const qual = { Q: "de " + $("Q = X W_Q"), S: "das pontuações " + $("Q K^\\top"), O: "da saída " + $("\\text{softmax}(QK^\\top/\\sqrt{d_k})\\,V") }[what];
    return { q: "Uma frase tem " + nt0 + " tokens: " + $("X") + " tem shape " + sh([nt0, dm]) + " e " + $("W_Q, W_K, W_V") + " têm shape " + sh([dm, dk]) + ". Qual é o shape " + qual + "?",
      v: ans.join("x"), fmt: shStr, d: { n: nt0, dm, dk, what },
      ops: R.shuffle(pool).slice(0, 3).map(t => ({ v: t, why: "" })),
      x: "Q, K e V ficam com shape " + sh([nt0, dk]) + " (um vetor de " + dk + " números por token). " + $("QK^\\top") + " compara todos com todos: " + sh([nt0, nt0]) +
         ". Multiplicando os pesos por V, volta a " + sh([nt0, dk]) + "." };
  } };

  G.qproj = { t: "Projetar um embedding na query", f: (R, p) => {
    const x = R.vec(2, -2, 3), W = [R.vec(2, -2, 3), R.vec(2, -2, 3)], q = [x[0] * W[0][0] + x[1] * W[1][0], x[0] * W[0][1] + x[1] * W[1][1]];
    return { q: "Um token tem embedding " + $("x = " + V(x)) + " (vetor-linha). Calcule a query " + $("q = x\\,W_Q") + " com " + $("W_Q = " + M(W)) + ".", v: q, d: { x, W },
      ops: [{ v: mv(W, x), why: "usou as linhas de W (fez W x)" }, { v: [x[0] * W[0][0], x[1] * W[1][1]], why: "usou só a diagonal" }, { v: [x[0] + W[0][0] + W[1][0], x[1] + W[0][1] + W[1][1]], why: "somou em vez de multiplicar" }],
      x: "Vetor-linha vezes matriz: cada coordenada de q é x com uma <b>coluna</b> de W. " + $("q_1 = " + prods(x, [W[0][0], W[1][0]]) + " = " + n(q[0])) + " e " +
         $("q_2 = " + prods(x, [W[0][1], W[1][1]]) + " = " + n(q[1])) + "." };
  } };

  G.paramsqkv = { t: "Pesos de W_Q, W_K e W_V", f: (R, p) => {
    const dm = R.pick([512, 768, 1024]), v = 3 * dm * dm;
    return { q: "Num bloco de atenção com " + $("d_{model} = " + dm) + ", quantos pesos têm " + $("W_Q") + ", " + $("W_K") + " e " + $("W_V") + " juntas (cada uma " + $(dm + " \\times " + dm) + ", sem vieses)?",
      v, fmt: x => milhar(x) + " pesos", d: { dm },
      ops: [{ v: dm * dm, why: "contou uma matriz só" }, { v: 3 * dm * (dm / 8), why: "contou só uma cabeça (d_k = d/8)" }, { v: 4 * dm * dm, why: "incluiu a W_O" }],
      x: $("3 \\cdot " + dm + "^2 = 3 \\cdot " + milhar(dm * dm) + " = " + milhar(v)) + ". Repare que o número de pesos não depende do tamanho da frase." };
  } };

  // ---------------- Scaled dot-product attention ----------------
  G.attscore = { t: "Pontuação de atenção com escala", f: (R, p) => {
    const tipo = R.pick(["vet", "num"]);
    if (tipo === "vet") {
      const q = R.vec(4, -2, 3), k = R.vec(4, -2, 3), s = dot(q, k), v = s / 2;
      return { q: "Com " + $("d_k = 4") + ", calcule " + $("\\dfrac{q \\cdot k}{\\sqrt{d_k}}") + " para " + $("q = " + V(q)) + " e " + $("k = " + V(k)) + ".", v, d: { s, dk: 4 },
        ops: [{ v: s, why: "esqueceu de dividir por √d_k" }, { v: s / 4, why: "dividiu por d_k, sem a raiz" }, { v: s * 2, why: "multiplicou em vez de dividir" }],
        x: $("q \\cdot k = " + prods(q, k) + " = " + n(s)) + " e " + $("\\sqrt{4} = 2") + ": " + $(n(s) + "/2 = " + n(v)) + "." };
    }
    const dk = R.pick([16, 64, 100, 256]), rt = Math.sqrt(dk), s = rt * R.pick([1, 1.5, 2, 3, -1, -2]), v = s / rt;
    return { q: "O produto escalar " + $("q \\cdot k") + " deu " + $(n(s)) + " e " + $("d_k = " + dk) + ". Quanto vale a pontuação " + $("\\dfrac{q \\cdot k}{\\sqrt{d_k}}") + "?", v, d: { s, dk },
      ops: [{ v: s, why: "esqueceu de dividir por √d_k" }, { v: s / dk, why: "dividiu por d_k, sem a raiz" }, { v: s * rt, why: "multiplicou em vez de dividir" }],
      x: $("\\sqrt{" + dk + "} = " + n(rt)) + ", então " + $(n(s) + "/" + n(rt) + " = " + n(v)) + "." };
  } };

  G.attpesos = { t: "Pesos de atenção (softmax das pontuações)", f: (R, p) => {
    let s; do { s = [R.int(0, 3), R.int(0, 3)]; } while (s[0] === s[1]);
    const e = s.map(Math.exp), v = e[0] / (e[0] + e[1]);
    return { q: "Um token tem pontuações " + $(n(s[0])) + " e " + $(n(s[1])) + " para duas keys. Depois da softmax, quanto peso vai para a primeira?", v, d: { s },
      ops: [{ v: s[0] / (s[0] + s[1]), why: "dividiu as pontuações sem exponenciar" }, { v: 0.5, why: "achou que fica meio a meio" }, { v: r2(e[0]), why: "não dividiu pela soma" }],
      x: $("\\dfrac{e^{" + s[0] + "}}{e^{" + s[0] + "} + e^{" + s[1] + "}} = \\dfrac{" + n(e[0]) + "}{" + n(e[0]) + " + " + n(e[1]) + "} \\approx " + n(v)) + "." };
  } };

  G.attout = { t: "Saída da atenção (média ponderada dos values)", f: (R, p) => {
    const w = R.pick([[0.75, 0.25], [0.5, 0.5], [0.9, 0.1], [0.2, 0.8], [0.6, 0.4]]), v1 = R.vec(2, -4, 8), v2 = R.vec(2, -4, 8);
    const out = add(mul(w[0], v1), mul(w[1], v2));
    return { q: "Os pesos de atenção são " + $(n(w[0]) + " \\text{ e } " + n(w[1])) + ", e os values são " + $("v_1 = " + V(v1)) + " e " + $("v_2 = " + V(v2)) + ". Qual é a saída?",
      v: out, d: { w, v1, v2 },
      ops: [{ v: mul(0.5, add(v1, v2)), why: "fez a média simples, ignorando os pesos" }, { v: add(mul(w[1], v1), mul(w[0], v2)), why: "trocou os pesos" }, { v: add(v1, v2), why: "somou sem ponderar" }],
      x: $(n(w[0]) + "\\cdot " + V(v1) + " + " + n(w[1]) + "\\cdot " + V(v2) + " = " + V(out)) + ". A saída de cada token é uma mistura dos values, na proporção da atenção." };
  } };

  G.varscale = { t: "Por que dividir por √d_k", f: (R, p) => {
    const dk = R.pick([16, 64, 128, 256]), v = Math.sqrt(dk);
    return { q: "Com componentes de média 0 e variância 1, o produto escalar " + $("q \\cdot k") + " (com " + $("d_k = " + dk) + ") tem variância " + $(String(dk)) + ". Para voltar à variância 1, divide-se por…",
      v, d: { dk },
      ops: [{ v: dk, why: "dividiu pela variância, não pelo desvio padrão" }, { v: dk / 2, why: "" }, { v: r2(Math.log(dk)), why: "" }],
      x: "Dividir por c divide a variância por c². Para cortar " + dk + " para 1, " + $("c = \\sqrt{" + dk + "} = " + n(v)) + ". Sem isso, a softmax satura e o gradiente some." };
  } };

  // ---------------- Multi-head ----------------
  G.dk = { t: "Dimensão de cada cabeça", f: (R, p) => {
    const [dm, h] = R.pick([[512, 8], [768, 12], [1024, 16], [4096, 32], [2048, 16]]), v = dm / h;
    return { q: "Com " + $("d_{model} = " + dm) + " e " + h + " cabeças de atenção, qual é a dimensão " + $("d_k") + " de cada cabeça?", v, d: { dm, h },
      ops: [{ v: dm * h, why: "multiplicou" }, { v: h, why: "deu o número de cabeças" }, { v: dm, why: "achou que cada cabeça usa a dimensão inteira" }],
      x: $("d_k = " + dm + "/" + h + " = " + v) + ". As cabeças dividem o espaço entre si, então o custo total é o mesmo de uma cabeça só com " + $("d_k = " + dm) + "." };
  } };

  G.mhashape = { t: "Shapes dentro da multi-head attention", f: (R, p) => {
    const [dm, h] = R.pick([[512, 8], [768, 12], [256, 4]]), nt0 = R.pick([10, 20, 128]), dk = dm / h, what = R.pick(["cabeca", "concat", "atencao"]);
    const ans = what === "cabeca" ? [nt0, dk] : what === "concat" ? [nt0, dm] : [nt0, nt0];
    const pool = [...new Set([[nt0, dk], [nt0, dm], [nt0, nt0], [h, dk], [nt0, h], [dk, dk]].map(a => a.join("x")))].filter(t => t !== ans.join("x"));
    const qual = { cabeca: "da query de <b>uma</b> cabeça", concat: "da concatenação das " + h + " cabeças", atencao: "da matriz de pesos de atenção de uma cabeça" }[what];
    return { q: "Uma frase de " + nt0 + " tokens passa por uma multi-head attention com " + $("d_{model} = " + dm) + " e " + h + " cabeças. Qual é o shape " + qual + "?",
      v: ans.join("x"), fmt: shStr, d: { n: nt0, dm, h, what },
      ops: R.shuffle(pool).slice(0, 3).map(t => ({ v: t, why: "" })),
      x: "Cada cabeça trabalha com " + $("d_k = " + dm + "/" + h + " = " + dk) + ": query " + sh([nt0, dk]) + " e pesos de atenção " + sh([nt0, nt0]) + ". Juntando as " + h + " saídas lado a lado, volta a " + sh([nt0, dm]) + "." };
  } };

  G.mhaparams = { t: "Pesos de um bloco de atenção completo", f: (R, p) => {
    const dm = R.pick([512, 768, 1024]), h = R.pick([8, 12, 16]), v = 4 * dm * dm;
    return { q: "Num bloco de multi-head attention com " + $("d_{model} = " + dm) + " e " + h + " cabeças, quantos pesos têm " + $("W_Q, W_K, W_V") + " e " + $("W_O") + " juntas (sem vieses)?",
      v, fmt: x => milhar(x) + " pesos", d: { dm, h },
      ops: [{ v: 3 * dm * dm, why: "esqueceu a W_O" }, { v: 4 * dm * (dm / h), why: "contou uma cabeça só" }, { v: 4 * dm * dm * h, why: "multiplicou pelo número de cabeças" }],
      x: "Quatro matrizes " + $(dm + " \\times " + dm) + ": " + $("4 \\cdot " + milhar(dm * dm) + " = " + milhar(v)) + ". Dividir em cabeças não muda o total: cada uma usa uma fatia de " + $(String(dm / h)) + " colunas." };
  } };

  // ---------------- Posição ----------------
  const ROT = { 90: v => [-v[1], v[0]], 180: v => [-v[0], -v[1]], 270: v => [v[1], -v[0]] };
  G.rope = { t: "Rotação do RoPE", f: (R, p) => {
    const x = [R.nz(-4, 4), R.nz(-4, 4)], ang = R.pick([90, 180, 270]), out = ROT[ang](x), volta = ROT[360 - ang] ? ROT[360 - ang](x) : x;
    return { q: "No RoPE, cada par de coordenadas gira um ângulo que depende da posição do token. Girando " + $(V(x)) + " em " + $(ang + "^\\circ") + " no sentido anti-horário, o que sai?",
      v: out, d: { x, ang },
      ops: [{ v: volta, why: "girou no sentido horário" }, { v: x.slice(), why: "não girou" }, { v: [x[1], x[0]], why: "só trocou as coordenadas, sem os sinais" }],
      x: "Girar " + ang + "° leva " + $("(x, y)") + " em " + (ang === 90 ? $("(-y,\\ x)") : ang === 180 ? $("(-x,\\ -y)") : $("(y,\\ -x)")) + ": " + $(V(x) + " \\to " + V(out)) + ". O comprimento não muda, só a direção." };
  } };

  G.roperel = { t: "RoPE e a distância entre posições", f: (R, p) => {
    const m = R.int(3, 12), k = R.int(0, m - 1);
    return { q: "No RoPE, a query na posição " + m + " gira " + $(m + "\\theta") + " e a key na posição " + k + " gira " + $(k + "\\theta") + ". O produto escalar entre elas depende de qual ângulo?",
      v: m - k, fmt: x => $(x + "\\theta"), d: { m, k },
      ops: [{ v: m + k, why: "somou as posições" }, { v: m * k, why: "multiplicou as posições" }, { v: m, why: "usou só a posição da query" }],
      x: "Girar as duas e fazer o produto escalar dá o mesmo que girar uma pela diferença: " + $("(" + m + " - " + k + ")\\theta = " + (m - k) + "\\theta") + ". Só a distância relativa entre os tokens importa." };
  } };

  G.pefreq = { t: "Frequências do positional encoding", f: (R, p) => {
    const d = R.pick([64, 128, 256, 512, 768]);
    return { q: "No positional encoding senoidal com " + $("d = " + d) + ", cada frequência é usada num par (seno, cosseno). Quantas frequências diferentes existem?", v: d / 2, d: { d },
      ops: [{ v: d, why: "contou uma frequência por coordenada" }, { v: 10000, why: "confundiu com a base 10000 da fórmula" }, { v: 2 * d, why: "" }],
      x: "As " + d + " coordenadas formam " + (d / 2) + " pares, e cada par usa uma frequência. Elas vão das bem rápidas às bem lentas, como os ponteiros de um relógio." };
  } };
})();
"""
