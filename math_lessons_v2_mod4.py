# -*- coding: utf-8 -*-
"""
Aulas Visuais de Matemática v2 — Módulo 4: Funções, Geometria Analítica & Teoria da Informação.
Baseado em James Stewart (Precalculus/Calculus),
Claude Shannon (A Mathematical Theory of Communication),
Cover & Thomas (Elements of Information Theory),
Deisenroth, Faisal & Ong (Mathematics for Machine Learning, Cap. 2, 3 e 9) e
Goodfellow, Bengio & Courville (Deep Learning, Cap. 3, 5 e 6).
"""

# SVG: Hiperplano separador e margem de classificação
SVG_HIPERPLANO = r'''<svg viewBox="0 0 520 230" class="lv2-svg" role="img" aria-label="Hiperplano de decisão e margem de classificação">
  <!-- Eixos -->
  <line x1="30" y1="200" x2="490" y2="200" class="sv-ax"/>
  <line x1="40" y1="210" x2="40" y2="20" class="sv-ax"/>
  <text x="495" y="204" class="sv-tm">x₁ (estrelas)</text>
  <text x="35" y="15" class="sv-tm">x₂ (tamanho texto)</text>

  <!-- Pontos Classe Positiva (+) -->
  <circle cx="360" cy="60" r="5" class="sv-fill"/>
  <circle cx="410" cy="80" r="5" class="sv-fill"/>
  <circle cx="340" cy="110" r="5" class="sv-fill"/>
  <circle cx="440" cy="50" r="5" class="sv-fill"/>
  <text x="400" y="40" class="sv-t" style="font-weight:700">Classe +1 (Ótimo)</text>

  <!-- Pontos Classe Negativa (-) -->
  <circle cx="100" cy="170" r="5" class="sv-fillm"/>
  <circle cx="150" cy="150" r="5" class="sv-fillm"/>
  <circle cx="120" cy="120" r="5" class="sv-fillm"/>
  <circle cx="190" cy="180" r="5" class="sv-fillm"/>
  <text x="80" y="105" class="sv-tm" style="font-weight:700">Classe -1 (Ruim)</text>

  <!-- Hiperplano de Decisão Central w·x + b = 0 -->
  <line x1="160" y1="210" x2="350" y2="30" class="sv-a" style="stroke-width:2.6"/>
  <text x="290" y="30" class="sv-t" style="font-weight:700">wᵀx + b = 0</text>

  <!-- Margens paralelas w·x + b = ±1 -->
  <line x1="200" y1="210" x2="390" y2="30" class="sv-b sv-dash" style="stroke-width:1.5"/>
  <line x1="120" y1="210" x2="310" y2="30" class="sv-b sv-dash" style="stroke-width:1.5"/>

  <!-- Vetor normal w ortogonal à reta -->
  <line x1="255" y1="120" x2="295" y2="80" class="sv-a" style="stroke-width:2.2" marker-end="url(#m2-garr)"/>
  <text x="300" y="80" class="sv-t" style="font-weight:700">w (vetor normal)</text>
</svg>'''

# SVG: Distância Euclidiana L2 vs Manhattan L1
SVG_L1_VS_L2 = r'''<svg viewBox="0 0 500 220" class="lv2-svg" role="img" aria-label="Distância Euclidiana L2 vs Manhattan L1">
  <!-- Grid de fundo simulando quarteirões -->
  <g class="sv-thin" style="stroke:#253745;stroke-dasharray:2 2">
    <line x1="60" y1="50" x2="440" y2="50"/><line x1="60" y1="100" x2="440" y2="100"/>
    <line x1="60" y1="150" x2="440" y2="150"/><line x1="60" y1="200" x2="440" y2="200"/>
    <line x1="60" y1="50" x2="60" y2="200"/><line x1="140" y1="50" x2="140" y2="200"/>
    <line x1="220" y1="50" x2="220" y2="200"/><line x1="300" y1="50" x2="300" y2="200"/>
    <line x1="380" y1="50" x2="380" y2="200"/><line x1="440" y1="50" x2="440" y2="200"/>
  </g>

  <!-- Ponto A (140, 150) e Ponto B (380, 50) -->
  <circle cx="140" cy="150" r="6" class="sv-fill"/>
  <circle cx="380" cy="50" r="6" class="sv-fillm"/>
  <text x="120" y="165" class="sv-t" style="font-weight:700">Ponto A (x₁)</text>
  <text x="385" y="45" class="sv-tm" style="font-weight:700">Ponto B (x₂)</text>

  <!-- Distância Euclidiana L2 (hipotenusa direta em linha reta) -->
  <line x1="140" y1="150" x2="380" y2="50" class="sv-a" style="stroke-width:3"/>
  <text x="220" y="85" class="sv-t" style="font-weight:700">L₂: Euclidiana (linha reta)</text>

  <!-- Distância Manhattan L1 (quarteirões em ângulo reto) -->
  <polyline points="140,150 380,150 380,50" class="sv-b sv-dash" style="stroke-width:2.4;fill:none"/>
  <text x="240" y="170" class="sv-tm" style="font-weight:700">L₁: Manhattan (|Δx| + |Δy|)</text>
</svg>'''

# SVG: Perdas de Regressão MSE, MAE, Huber
SVG_LOSS_REG = r'''<svg viewBox="0 0 520 220" class="lv2-svg" role="img" aria-label="Comparativo de funções de perda: MSE vs MAE vs Huber">
  <!-- Eixos centrais -->
  <line x1="30" y1="180" x2="490" y2="180" class="sv-ax"/>
  <line x1="260" y1="20" x2="260" y2="190" class="sv-ax"/>
  <text x="495" y="184" class="sv-tm">Erro (y - ŷ)</text>
  <text x="265" y="20" class="sv-tm">Perda L</text>

  <!-- MSE: Parábola e^2 (cresce muito rápido) -->
  <path d="M 120 40 Q 260 210 400 40" class="sv-a" style="stroke-width:2.8"/>
  <text x="390" y="35" class="sv-t" style="font-weight:700">MSE: (y - ŷ)²</text>

  <!-- MAE: V em formato afiado |e| -->
  <path d="M 100 50 L 260 180 L 420 50" class="sv-b sv-dash" style="stroke-width:2.2"/>
  <text x="425" y="65" class="sv-tm">MAE: |y - ŷ|</text>

  <!-- Huber: suave no centro, linear nas pontas -->
  <path d="M 70 30 L 190 145 Q 260 190 330 145 L 450 30" class="sv-thin" style="stroke:#CCD0CF;stroke-width:2"/>
  <text x="75" y="20" class="sv-tm" style="font-size:11px">Huber (suave + robusta)</text>
</svg>'''

GUIDES_MOD4_V2 = {
    # =========================================================================
    # TÓPICO 30: Equações, inequações e gráficos de funções aplicadas
    # =========================================================================
    "Equações, inequações e gráficos de funções aplicadas": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""O que é, no fundo, a decisão de uma IA que aprova ou reprova um empréstimo bancário? É uma <b>inequação geométrica</b>: se $w_1 x_1 + w_2 x_2 + b > 0$, aprovado; se for $< 0$, recusado. Como retas, planos e hiperplanos se tornam fronteiras de decisão em modelos lineares, SVMs e no neurônio artificial de McCulloch-Pitts?""",
        "prerequisitos": [
            "Vetores e produto escalar (Tópicos 1 e 3)",
            "Geometria analítica do plano cartesiano ($y = mx + b$)"
        ],
        "objetivos": [
            "compreender equações lineares como hiperplanos separadores em $\mathbb{R}^d$;",
            "entender o significado geométrico do vetor normal de pesos $\mathbf{w}$ e do viés (bias) $b$;",
            "calcular a distância de um ponto até o hiperplano de decisão e entender a margem de separação."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Fronteira que Divide o Mundo",
                "titulo": "Hiperplanos de Separação em IA",
                "corpo": r"""<p>No colégio, aprendemos que $y = mx + b$ descreve uma reta em 2D. Em Machine Learning, reescrevemos essa mesma equação em forma vetorial canônica:</p>
$$\mathbf{w}^\top \mathbf{x} + b = 0 \iff w_1 x_1 + w_2 x_2 + \dots + w_d x_d + b = 0$$
<p>Essa equação define uma <b>fronteira de decisão (hiperplano)</b> de dimensão $d-1$:</p>
<ul>
<li>Em 2D ($x_1, x_2$), o hiperplano é uma <b>linha reta</b> que divide o plano em dois semi-planos.</li>
<li>Em 3D ($x_1, x_2, x_3$), é uma <b>folha plana infinita</b> que divide o espaço em dois hemisférios.</li>
<li>Em 1.536D (embeddings de LLMs), é um <b>hiperplano de 1.535 dimensões</b> que separa conceitos semânticos!</li>
</ul>
<p>O vetor de pesos $\mathbf{w}$ é sempre <b>rigorosamente ortogonal (perpendicular)</b> à reta de decisão, apontando para o lado da classe positiva!</p>""",
            },
            {
                "tipo": "visual",
                "titulo": "Geometria do Hiperplano Separador",
                "corpo": r"""<p>Veja como o vetor de pesos $\mathbf{w}$ e o viés $b$ organizam a classificação das avaliações da nossa cafeteria:</p>""",
                "svg": SVG_HIPERPLANO,
                "legenda": "O hiperplano w·x + b = 0 separa as avaliações positivas das negativas. O vetor w aponta perpendicularmente na direção da classe positiva.",
            },
            {
                "tipo": "notacao",
                "titulo": "Anatomia da Regra de Decisão",
                "corpo": r"""<p>Veja os elementos que compõem o classificador linear:</p>""",
                "itens": [
                    {"simbolo": r"$\hat{y} = \text{sinal}(\mathbf{w}^\top \mathbf{x} + b)$", "leitura": "predição é o sinal do produto escalar mais o viés", "significado": "Se a pontuação for positiva ($>0$), prediz $+1$. Se for negativa ($<0$), prediz $-1$."},
                    {"simbolo": r"$d = \frac{|\mathbf{w}^\top \mathbf{x} + b|}{\|\mathbf{w}\|}$", "leitura": "distância ortogonal do ponto ao hiperplano", "significado": "Mede quão profundamente um exemplo está dentro do território da sua classe. É a base da margem do SVM (Support Vector Machine)."},
                    {"simbolo": r"$b$ (Bias / Viés)", "leitura": "termo de viés", "significado": "Desloca o hiperplano para longe da origem. Se $b = 0$, o hiperplano é obrigado a passar exatamente por $(0, 0)$."},
                ],
            },
            {
                "tipo": "passos",
                "titulo": "Cálculo Passo a Passo: Classificando uma Avaliação",
                "corpo": r"""<p>Considere nosso classificador da cafeteria com vetor de pesos $\mathbf{w} = [2.0, 1.5]^\top$ e viés $b = -5.0$. Vamos classificar dois clientes:</p>""",
                "passos": [
                    {
                        "faca": r"Cliente 1: deu 4 estrelas e escreveu 2 frases positivas. Vetor $\mathbf{x}_1 = [4, 2]^\top$. Calcule a pontuação: $$z_1 = \mathbf{w}^\top \mathbf{x}_1 + b = (2.0 \times 4) + (1.5 \times 2) - 5.0 = 8.0 + 3.0 - 5.0 = +6.0$$",
                        "porque": "Multiplicamos cada feature pelo seu respectivo peso e somamos o viés."
                    },
                    {
                        "faca": r"Decisão do Cliente 1: Como $z_1 = +6.0 > 0$, a predição é $\hat{y}_1 = +1$ (Avaliação Satisfeita).",
                        "porque": "O ponto está do lado positivo do hiperplano com margem alta."
                    },
                    {
                        "faca": r"Cliente 2: deu 1 estrela e escreveu 1 frase curta. Vetor $\mathbf{x}_2 = [1, 1]^\top$. Calcule a pontuação: $$z_2 = \mathbf{w}^\top \mathbf{x}_2 + b = (2.0 \times 1) + (1.5 \times 1) - 5.0 = 2.0 + 1.5 - 5.0 = -1.5$$",
                        "porque": "A pontuação resultou em um valor negativo."
                    },
                    {
                        "faca": r"Decisão do Cliente 2: Como $z_2 = -1.5 < 0$, a predição é $\hat{y}_2 = -1$ (Avaliação Insatisfeita).",
                        "porque": "O ponto está do lado negativo do hiperplano separador."
                    }
                ],
                "conclusao": r"A fronteira de decisão $2.0 x_1 + 1.5 x_2 - 5.0 = 0$ traça uma linha clara no espaço de features que separa com perfeição o comportamento dos dois clientes."
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: O Perceptron Linear em Ação",
                "codigo": r'''import numpy as np

# Hiperplano: w1*x1 + w2*x2 + b = 0
w = np.array([2.0, 1.5])
b = -5.0

# 4 clientes: [estrelas, frases]
X = np.array([
    [4.0, 2.0],  # Cliente A (claramente satisfeito)
    [1.0, 1.0],  # Cliente B (claramente insatisfeito)
    [2.0, 1.0],  # Cliente C (nota baixa)
    [3.0, 0.0]   # Cliente D (quase em cima da linha!)
])

logits = X @ w + b
predicoes = np.where(logits > 0, "+1 (Satisfeito)", "-1 (Insatisfeito)")

print("Classificação Linear dos Clientes:")
for x, logit, pred in zip(X, logits, predicoes):
    distancia = abs(logit) / np.linalg.norm(w)
    print(f"Features: {x} -> Logit: {logit:5.2f} | Distância à margem: {distancia:.2f} | Classe: {pred}")''',
                "experimentos": [
                    "Observe o Cliente D com features [3, 0]: seu logit é $2(3) + 1.5(0) - 5 = +1.0$, bem próximo da fronteira de dúvida.",
                    "Altere o viés para <code>b = -10.0</code> e veja como o classificador fica muito mais 'exigente', exigindo muito mais estrelas para aprovar."
                ]
            }
        ],
        "resumo": [
            "Classificadores lineares tomam decisões avaliando de qual lado de um hiperplano $\mathbf{w}^\top \mathbf{x} + b = 0$ o dado se encontra.",
            "O vetor de pesos $\mathbf{w}$ dita a inclinação e orientação ortogonal da fronteira e o viés $b$ controla o deslocamento.",
            "A distância geométrica até a fronteira quantifica o grau de confiança da previsão do modelo."
        ],
        "proxima": r"Por que quase todas as funções de custo e ativações da IA utilizam exponenciais e logaritmos? No próximo tópico, vamos entender o papel de $e^x$ e $\ln(x)$.",
        "referencias": [
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Capítulo 2.7: Linear Independence and Affine Spaces", "uso": "Definição geométrica e vetorial de hiperplanos afins"},
            {"obra": "Goodfellow, Bengio & Courville. Deep Learning", "trecho": "Capítulo 5.7: Supervised Learning Algorithms and Perceptrons", "uso": "História dos classificadores lineares e superfícies de decisão"}
        ]
    },

    # =========================================================================
    # TÓPICO 31: Exponenciais e logaritmos na modelagem de IA
    # =========================================================================
    "Exponenciais e logaritmos na modelagem de IA": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Por que a base natural de Euler ($e = 2.71828\dots$) e o logaritmo natural ($\ln$) aparecem em <b>praticamente todas as páginas</b> de qualquer livro ou artigo de Inteligência Artificial? Por que sem o logaritmo os computadores mais potentes do mundo sofreriam de <i>overflow</i> e <i>underflow</i> imediato ao calcular probabilidades?""",
        "prerequisitos": [
            "Álgebra fundamental e potências",
            "Derivadas básicas (Tópico 13)"
        ],
        "objetivos": [
            "compreender por que $e^x$ é a ferramenta perfeita para garantir positividade estrita em IA;",
            "dominar as propriedades de $\ln(x)$ que transformam produtos de probabilidade em somas dóceis;",
            "entender o truque do LogSumExp para impedir instabilidade numérica em GPUs."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "O Número Mágico de Euler",
                "titulo": "Por que a base 'e' é tão especial?",
                "corpo": r"""<p>O número $e \approx 2.71828$ não foi escolhido por capricho. Ele é a única base no universo que satisfaz a propriedade mágica:</p>
$$\frac{d}{dx}[e^x] = e^x$$
<p>A taxa instantânea de variação de $e^x$ é rigorosamente igual ao seu próprio valor atual. Em Inteligência Artificial, a função exponencial desempenha uma função insubstituível: ela é um <b>conversor universal de números reais para grandezas estritamente positivas</b>:</p>
<p>Não importa se o neurônio calculou um número extremamente negativo (ex.: $z = -50$): $e^{-50} = 1.9 \times 10^{-22} > 0$. É por isso que ela alimenta o numerador e denominador da função Softmax!</p>""",
            },
            {
                "tipo": "texto",
                "rotulo": "A Salvação Numérica",
                "titulo": "As Três Propriedades Sagradas do Logaritmo",
                "corpo": r"""<p>O logaritmo natural $\ln(x)$ é o espelho inverso de $e^x$ ($\ln(e^x) = x$). Ele é uma função <b>estritamente crescente</b> (se $a > b$, então $\ln(a) > \ln(b)$). Isso significa que encontrar o ponto de máximo de uma probabilidade é exatamente o mesmo que encontrar o ponto de máximo do seu logaritmo!</p>
<p>Suas três identidades fundamentais salvam os cálculos de IA:</p>
<ol>
<li><b>Produto vira Soma:</b> $\ln(a \cdot b) = \ln(a) + \ln(b)$. Transforma produtos de probabilidades minúsculas em somas de log-probabilidades, eliminando o underflow numérico!</li>
<li><b>Divisão vira Subtração:</b> $\ln(a / b) = \ln(a) - \ln(b)$.</li>
<li><b>Potência vira Multiplicação:</b> $\ln(a^k) = k \cdot \ln(a)$. Permite 'descer' expoentes complicados para frente da expressão.</li>
</ol>""",
            },
            {
                "tipo": "passos",
                "titulo": "O Truque do LogSumExp (LSE) nas GPUs",
                "corpo": r"""<p>Ao calcular o denominador da Softmax $\ln \left( \sum_{i} e^{z_i} \right)$, se um dos logits for grande (ex.: $z_1 = 1000$), a exponencial $e^{1000}$ transborda imediatamente para o infinito positivo (`inf / overflow`). Veja o truque matemático que toda biblioteca de Deep Learning aplica internamente:</p>""",
                "passos": [
                    {
                        "faca": r"Encontre o valor máximo dos logits: $$m = \max(z_1, z_2, \dots, z_n)$$",
                        "porque": "Subtrair o máximo garantirá que o maior expoente seja exatamente zero ($z_i - m \le 0$)."
                    },
                    {
                        "faca": r"Coloque $e^m$ em evidência dentro da soma: $$\sum_{i=1}^n e^{z_i} = \sum_{i=1}^n e^{(z_i - m) + m} = e^m \cdot \sum_{i=1}^n e^{z_i - m}$$",
                        "porque": "Propriedade das potências: $e^{a+b} = e^a \cdot e^b$."
                    },
                    {
                        "faca": r"Aplique o logaritmo na expressão fatorada: $$\ln\left( \sum_{i=1}^n e^{z_i} \right) = \ln\left( e^m \cdot \sum_{i=1}^n e^{z_i - m} \right) = \ln(e^m) + \ln\left( \sum_{i=1}^n e^{z_i - m} \right)$$",
                        "porque": "O logaritmo do produto vira a soma dos logaritmos."
                    },
                    {
                        "faca": r"Simplifique $\ln(e^m) = m$: $$\text{LogSumExp}(\mathbf{z}) = m + \ln\left( \sum_{i=1}^n e^{z_i - m} \right)$$",
                        "porque": "O termo $e^{z_i - m}$ agora fica sempre no intervalo seguro $(0, 1]$, tornando o cálculo 100% à prova de overflow!"
                    }
                ],
                "conclusao": r"Esse truque aparentemente simples é executado bilhões de vezes por segundo nos clusters de GPUs da OpenAI, Anthropic e Google para garantir estabilidade numérica contínua."
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: O Desastre do Overflow vs. LogSumExp",
                "codigo": r'''import numpy as np

# Logits com valores altos (comuns na saída de modelos de linguagem)
logits = np.array([1000.0, 1001.0, 999.0])

# 1. Tentativa Ingênua (sem estabilização)
try:
    soma_exp = np.sum(np.exp(logits))
    lse_ingenuo = np.log(soma_exp)
    print("Tentativa ingênua:", lse_ingenuo)
except Exception as e:
    print("Erro na ingênua:", e)

print(f"np.exp(1000.0) resulta em: {np.exp(logits[0])} (OVERFLOW CATASTRÓFICO!)")

# 2. Implementação do Truque LogSumExp Estável
def logsumexp_estavel(z):
    m = np.max(z)
    return m + np.log(np.sum(np.exp(z - m)))

lse_correto = logsumexp_estavel(logits)
print(f"LogSumExp Estável: {lse_correto:.6f} (Cálculo perfeito sem NaN ou Inf!)")

# Verificação com a biblioteca oficial do SciPy
from scipy.special import logsumexp
print(f"SciPy logsumexp  : {logsumexp(logits):.6f}")
assert np.isclose(lse_correto, logsumexp(logits)), "O cálculo deve bater com o SciPy!"''',
                "experimentos": [
                    "Experimente com logits extremamente negativos (ex.: <code>[-1000.0, -1002.0]</code>) e verifique como a implementação ingênua sofre de underflow (resultando em $\log(0) = -\infty$), enquanto o LogSumExp permanece exato.",
                    "Entenda por que PyTorch tem a função nativa <code>torch.nn.functional.log_softmax</code> para fundir o cálculo em um único kernel de GPU ultrarrápido."
                ]
            }
        ],
        "resumo": [
            "A função exponencial $e^x$ mapeia números reais em valores estritamente positivos, sendo a espinha dorsal de probabilidades.",
            "O logaritmo natural converte produtos de probabilidades em somas e impede sobredimensionamento numérico.",
            "O truque LogSumExp protege o cálculo do denominador da Softmax contra overflow e underflow computacional."
        ],
        "proxima": r"Com as funções transcendentais dominadas, como ler e decodificar a rica notação de somatórios, produtórios e operadores em artigos científicos de IA? Esse é o foco do Tópico 32.",
        "referencias": [
            {"obra": "Stewart, J. Calculus", "trecho": "Capítulo 1.5 e 1.6: Exponential Functions and Logarithms", "uso": "Propriedades analíticas e deduções da base natural euleriana"},
            {"obra": "Goodfellow, Bengio & Courville. Deep Learning", "trecho": "Capítulo 4.1: Overflow and Underflow", "uso": "Motivação computacional detalhada do algoritmo LogSumExp"}
        ]
    },

    # =========================================================================
    # TÓPICO 32: Somatório, produtório e notação matemática em papers
    # =========================================================================
    "Somatório, produtório e notação matemática em papers": {
        "v": 2,
        "duracao": 25,
        "gancho": r"""Você abre um paper seminal de Machine Learning da DeepMind ou Meta e se depara com fórmulas cheias de $\sum_{i=1}^N$, $\prod_{t}$, $\arg\max$, $\mathbb{E}_{x \sim p}$ e $\odot$. Como decodificar essa taquigrafia matemática sem medo e enxergar cada símbolo como uma linha límpida de código Python/NumPy?""",
        "prerequisitos": [
            "Noções de laços de repetição (`for loops`) em programação",
            "Vetores e matrizes (Tópicos 1 e 7)"
        ],
        "objetivos": [
            "aprender a ler e traduzir somatórios ($\sum$) e produtórios ($\prod$) com múltiplos índices e condições;",
            "compreender os operadores $\arg\max$, $\arg\min$ e a função indicadora $\mathbb{I}[\cdot]$;",
            "traduzir expressões complexas de papers diretamente em operações vetorizadas de NumPy."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Pedra de Roseta da IA",
                "titulo": "A Taquigrafia Matemática Decodificada",
                "corpo": r"""<p>Cientistas escrevem equações matemáticas com operadores condensados porque seria cansativo escrever loops repetitivos. Mas todo operador tem um equivalente exato e direto na programação:</p>
<p>Entender essa correspondência remove 90% do medo de ler artigos originais no ArXiv!</p>""",
            },
            {
                "tipo": "tabela",
                "titulo": "Dicionário Visual de Notação Matemática em Papers",
                "cabecalho": ["Símbolo Matemático", "Como se Lê", "O que faz?", "Equivalente em Python / NumPy"],
                "linhas": [
                    [r"$\sum_{i=1}^n x_i$", "Somatório de x_i de 1 a n", "Acumula a soma de todos os elementos", "<code>np.sum(x)</code> ou <code>sum(x)</code>"],
                    [r"$\prod_{j=1}^m p_j$", "Produtório de p_j de 1 a m", "Acumula a multiplicação de todos os elementos", "<code>np.prod(p)</code>"],
                    [r"$\arg\max_x f(x)$", "Argumento do máximo de f(x)", "Retorna o <b>índice / argumento</b> x que gerou a maior saída, não o valor em si", "<code>np.argmax(f)</code>"],
                    [r"$\arg\min_w L(w)$", "Argumento do mínimo da perda", "Retorna o peso w que minimiza o erro", "O resultado da otimização final"],
                    [r"$\mathbb{I}[\text{condição}]$", "Função indicadora", "Retorna 1 se a condição for verdadeira, e 0 se for falsa", "<code>int(condicao)</code> ou <code>(y == pred).astype(int)</code>"],
                    [r"$\mathbf{A} \odot \mathbf{B}$ ou $\circ$", "Produto de Hadamard", "Multiplicação elemento a elemento entre duas matrizes de mesmo tamanho", "<code>A * B</code> (não use <code>A @ B</code>!)"],
                    [r"$\|\mathbf{x}\|_2$", "Norma L2 Euclidiana", "Comprimento do vetor $\sqrt{\sum x_i^2}$", "<code>np.linalg.norm(x)</code>"],
                    [r"$\mathbb{E}_{x \sim p}[f(x)]$", "Esperança de f sob a distribuição p", "Média ponderada pela probabilidade", "<code>np.mean(f(x_amostrado))</code>"]
                ]
            },
            {
                "tipo": "passos",
                "titulo": "Decodificando uma Equação Real de Paper",
                "corpo": r"""<p>Veja esta equação clássica de acurácia balanceada de um paper: $$\text{Acc} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}[y_i = \arg\max_c (\hat{y}_{i, c})]$$ Vamos traduzi-la passo a passo para código:</p>""",
                "passos": [
                    {
                        "faca": r"Identifique a parte interna: $\arg\max_c (\hat{y}_{i, c})$.",
                        "porque": "Para o exemplo $i$, pega a classe $c$ que tem a maior probabilidade predita pelo modelo: <code>pred = np.argmax(probs, axis=1)</code>."
                    },
                    {
                        "faca": r"Avalie a função indicadora: $\mathbb{I}[y_i = \text{pred}_i]$.",
                        "porque": "Compara se a classe verdadeira $y_i$ é igual à predição. Dá 1 se acertou e 0 se errou: <code>acertos = (y == pred)</code>."
                    },
                    {
                        "faca": r"Execute o somatório com média: $\frac{1}{N} \sum_{i=1}^N (\dots)$.",
                        "porque": "Soma todos os acertos e divide pelo total de exemplos $N$: <code>np.mean(acertos)</code>."
                    }
                ],
                "conclusao": r"Uma fórmula que parecia ameaçadora e complexa se resumiu a uma única linha de código elegante: <code>acuracia = np.mean(y == np.argmax(probs, axis=1))</code>!"
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Da Notação de Paper ao Código",
                "codigo": r'''import numpy as np

# Simulando probabilidades preditas de 4 avaliações da cafeteria para 3 classes:
# [P(Péssimo), P(Neutro), P(Ótimo)]
probs = np.array([
    [0.10, 0.20, 0.70],  # Exemplo 1: prediz classe 2 (Ótimo)
    [0.85, 0.10, 0.05],  # Exemplo 2: prediz classe 0 (Péssimo)
    [0.15, 0.75, 0.10],  # Exemplo 3: prediz classe 1 (Neutro)
    [0.40, 0.50, 0.10]   # Exemplo 4: prediz classe 1 (Neutro)
])

# Rótulos verdadeiros (classes reais)
y_real = np.array([2, 0, 1, 2]) # O 4º cliente era Ótimo, mas o modelo previu Neutro!

# 1. argmax_c (classe predita)
predicoes = np.argmax(probs, axis=1)
print(f"Predições argmax : {predicoes}")
print(f"Rótulos reais    : {y_real}")

# 2. Indicadora I[y == pred]
indicadora = (y_real == predicoes).astype(int)
print(f"Função Indicadora: {indicadora} (1 = acerto, 0 = erro)")

# 3. Média do somatório (1/N * sum)
acuracia = np.mean(indicadora)
print(f"Acurácia calculada: {acuracia * 100:.1f}% (3 acertos em 4)")''',
                "experimentos": [
                    "Traduza a fórmula da entropia de Shannon $-\sum p \log p$ usando <code>-np.sum(p * np.log2(p))</code>.",
                    "Experimente com matrizes e o operador de Hadamard ($\odot$) multiplicando duas matrizes com <code>A * B</code>."
                ]
            }
        ],
        "resumo": [
            "A notação matemática de papers é uma linguagem compacta com correspondência direta para loops e operações vetorizadas.",
            "$\arg\max$ recupera o índice do maior elemento e $\mathbb{I}[\cdot]$ converte condições booleanas em 1 ou 0.",
            "Dominar essa sintaxe destrava a capacidade de ler e implementar os artigos mais recentes de inteligência artificial."
        ],
        "proxima": r"Como medir o quão distantes dois pontos ou embeddings estão no espaço multidimensional? Vamos explorar a Geometria Analítica das distâncias Euclidiana e Manhattan.",
        "referencias": [
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Mathematical Notation Reference", "uso": "Convenções universais de vetores, matrizes, somas e operadores indexados"},
            {"obra": "Goodfellow, Bengio & Courville. Deep Learning", "trecho": "Notation Guide (pp. xi-xvi)", "uso": "Notações contemporâneas de tensores e conjuntos de dados"}
        ]
    },

    # =========================================================================
    # TÓPICO 33: Geometria analítica e distância Euclidiana vs Manhattan
    # =========================================================================
    "Geometria analítica e distância Euclidiana vs Manhattan": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Se um pássaro voa entre dois pontos em linha reta, ele percorre a <b>Distância Euclidiana ($L_2$)</b>. Mas se um táxi de Nova York anda pelas ruas quadriculadas, ele é obrigado a percorrer quarteirões em ângulo reto: essa é a <b>Distância Manhattan ($L_1$)</b>. Por que a escolha entre $L_1$ e $L_2$ afeta drasticamente a busca vetorial em RAG, o clustering k-Means e a indução de esparsidade em pesos?""",
        "prerequisitos": [
            "Normas L1 e L2 de vetores (Tópico 4)",
            "Teorema de Pitágoras e geometria do plano"
        ],
        "objetivos": [
            "diferenciar geometricamente e algebricamente a distância Euclidiana ($L_2$) da distância Manhattan ($L_1$);",
            "compreender como a distância em alta dimensionalidade sofre o fenômeno da 'Maldição da Dimensionalidade';",
            "aplicar essas distâncias no algoritmo k-Nearest Neighbors (k-NN) de recomendação."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "O Voo do Pássaro contra a Rota do Táxi",
                "titulo": "As Duas Métricas de Proximidade",
                "corpo": r"""<p>Para medir a distância entre dois pontos $\mathbf{u}, \mathbf{v} \in \mathbb{R}^d$, a Geometria Analítica define uma família de métricas (chamadas <b>distâncias de Minkowski</b>):</p>
$$D_p(\mathbf{u}, \mathbf{v}) = \left( \sum_{i=1}^d |u_i - v_i|^p \right)^{1/p}$$
<ul>
<li><b>Distância Euclidiana ($p = 2$):</b> É a distância física em linha reta (hipotenusa de Pitágoras):
$$d_2(\mathbf{u}, \mathbf{v}) = \sqrt{\sum_{i=1}^d (u_i - v_i)^2}$$</li>
<li><b>Distância Manhattan ($p = 1$, City Block):</b> É a soma dos deslocamentos absolutos ao longo dos eixos perpendiculares:
$$d_1(\mathbf{u}, \mathbf{v}) = \sum_{i=1}^d |u_i - v_i|$$</li>
</ul>
<p>Pela desigualdade triangular, a distância Euclidiana é <b>sempre menor ou igual</b> à distância Manhattan ($d_2 \le d_1$), sendo iguais apenas se todos os deslocamentos ocorrerem em um único eixo!</p>""",
            },
            {
                "tipo": "visual",
                "titulo": "Comparação Visual: Hipotenusa vs. Quarteirões",
                "corpo": r"""<p>Veja o caminho percorrido pelas duas métricas para conectar o ponto A ao ponto B:</p>""",
                "svg": SVG_L1_VS_L2,
                "legenda": "A distância Euclidiana corta o caminho em linha reta (L2), enquanto a Manhattan soma os catetos horizontais e verticais (L1).",
            },
            {
                "tipo": "ponte",
                "titulo": "A Maldição da Dimensionalidade em Espaços de Alta Dimensão",
                "corpo": r"""<p>Em 2D ou 3D, a intuição geométrica funciona perfeitamente. Mas o que acontece quando calculamos distâncias Euclidianas em embeddings de 1.536 dimensões?</p>
<p>Surge o fenômeno da <b>concentração de medidas</b>: em alta dimensão, a razão entre a distância para o vizinho mais distante e para o vizinho mais próximo converge para $1.0$:</p>
$$\lim_{d \to \infty} \frac{d_{\max} - d_{\min}}{d_{\min}} \to 0$$
<p>Todos os pontos parecem estar <i>quase à mesma distância</i> uns dos outros! É exatamente por essa razão que em Retrieval-Augmented Generation (RAG) e LLMs prefere-se a <b>Similaridade de Cosseno com vetores normalizados</b> em vez da distância Euclidiana pura.</p>""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: k-NN com Distâncias L1 e L2",
                "codigo": r'''import numpy as np

# Base de embeddings simplificada de 4 avaliações da cafeteria [sentimento, tamanho]:
# Classes: 0 = Ruim, 1 = Excelente
banco_avaliacoes = np.array([
    [-2.0, 1.0],  # 0: Ruim
    [-3.0, 2.0],  # 0: Ruim
    [ 2.0, 1.0],  # 1: Excelente
    [ 3.0, 2.0]   # 1: Excelente
])
classes = np.array([0, 0, 1, 1])

# Nova avaliação misteriosa que acabou de chegar
nova_avaliacao = np.array([1.5, 1.2])

# 1. Distâncias Euclidianas L2
dist_L2 = np.linalg.norm(banco_avaliacoes - nova_avaliacao, axis=1)

# 2. Distâncias Manhattan L1
dist_L1 = np.sum(np.abs(banco_avaliacoes - nova_avaliacao), axis=1)

print(f"Nova avaliação: {nova_avaliacao}")
print("\nComparativo de Distâncias aos pontos da base:")
for idx, (l2, l1, c) in enumerate(zip(dist_L2, dist_L1, classes)):
    print(f"Ponto {idx} (Classe {c}): L2 = {l2:.3f} | L1 = {l1:.3f}")

vizinho_L2 = np.argmin(dist_L2)
vizinho_L1 = np.argmin(dist_L1)

print(f"\nVizinho mais próximo por L2: Ponto {vizinho_L2} (Classe {classes[vizinho_L2]})")
print(f"Vizinho mais próximo por L1: Ponto {vizinho_L1} (Classe {classes[vizinho_L1]})")
assert classes[vizinho_L2] == 1, "Deveria classificar como Excelente!"''',
                "experimentos": [
                    "Experimente com um ponto onde a escolha de L1 vs L2 mude a ordem de classificação dos vizinhos mais próximos.",
                    "Simule a maldição da dimensionalidade gerando 100 pontos aleatórios em 10 dimensões e em 10.000 dimensões com <code>np.random.randn</code>. Meça a diferença relativa entre a maior e a menor distância."
                ]
            }
        ],
        "resumo": [
            "A distância Euclidiana mede a menor distância linear direta e é sensível a desvios grandes ao quadrado.",
            "A distância Manhattan soma desvios absolutos por eixo e é mais robusta a outliers em dados tabulares esparsos.",
            "Em alta dimensionalidade, a métrica de cosseno é frequentemente superior à distância euclidiana devido à concentração de medidas."
        ],
        "proxima": r"Como medir o volume de 'informação' e 'surpresa' contido em uma mensagem? Entra em cena uma das maiores mentes do século XX: Claude Shannon e a Entropia.",
        "referencias": [
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Capítulo 3.1: Norms and Inner Products", "uso": "Definição formal de distâncias métricas e espaços de Hilbert"},
            {"obra": "Aggarwal et al. (2001). On the Surprising Behavior of Distance Metrics in High Dimensional Space", "trecho": "Paper seminal", "uso": "Demonstração matemática da degradação das normas L1 e L2 com o aumento da dimensão"}
        ]
    },

    # =========================================================================
    # TÓPICO 34: Entropia de Shannon (medida de incerteza da informação)
    # =========================================================================
    "Entropia de Shannon (medida de incerteza da informação)": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Se uma manchete diz: <i>“O Sol nasceu no leste esta manhã”</i>, quanta informação nova você recebeu? Rigorosamente <b>zero bits</b>, pois a probabilidade era de 100% e a surpresa foi nula. Mas se a notícia diz: <i>“Nevou no meio do Saara”</i>, a surpresa é colossal! Como Claude Shannon conseguiu transformar a intuição humana de <b>surpresa e incerteza</b> em uma equação matemática precisa que hoje mede o aprendizado de LLMs?""",
        "prerequisitos": [
            "Variáveis aleatórias e probabilidade (Tópicos 21 e 24)",
            "Logaritmos e propriedades da base 2 (Tópico 31)"
        ],
        "objetivos": [
            "compreender a fórmula da Auto-Informação (Surpresa) $I(x) = -\log_2 P(x)$;",
            "deduzir a Entropia de Shannon $H(X) = -\sum p_i \log_2 p_i$ como a incerteza média de um sistema;",
            "entender por que a distribuição uniforme maximiza a entropia e como isso se relaciona com a inteligência de LLMs."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Matemática da Surpresa",
                "titulo": "Quanta Informação tem um Evento?",
                "corpo": r"""<p>Em 1948, nos laboratórios Bell, Claude Shannon fundou a <b>Teoria da Informação</b> ao formalizar uma ideia revolucionária: <b>a informação de um evento é inversamente proporcional à sua probabilidade de ocorrência</b>.</p>
<p>A quantidade de informação (ou <i>surprisal</i>) de observar um evento $x$ com probabilidade $P(x)$ é:</p>
$$I(x) = -\log_2 P(x) = \log_2\left(\frac{1}{P(x)}\right) \text{ (medida em bits)}$$
<ul>
<li>Se um evento tem certeza absoluta ($P = 1$): $I(x) = -\log_2(1) = 0\text{ bits}$. Zero surpresa, zero informação!</li>
<li>Se uma moeda honesta dá cara ($P = 0.5$): $I(x) = -\log_2(0.5) = \log_2(2) = 1\text{ bit}$ exato de informação.</li>
<li>Se um evento raríssimo acontece ($P = \frac{1}{1024} \approx 0.001$): $I(x) = \log_2(1024) = 10\text{ bits}$ de informação pura!</li>
</ul>""",
            },
            {
                "tipo": "notacao",
                "titulo": "A Equação da Entropia de Shannon",
                "corpo": r"""<p>A <b>Entropia $H(X)$</b> é a média ponderada (esperança matemática) de toda a surpresa contida em uma distribuição de probabilidade:</p>
$$H(X) = \mathbb{E}[I(X)] = -\sum_{i=1}^n P(x_i) \log_2 P(x_i)$$""",
                "itens": [
                    {"simbolo": r"$H(X)$", "leitura": "entropia de X", "significado": "Mede o grau médio de incerteza ou desordem da fonte de dados. Quanto mais imprevisível for o sorteio, maior é a entropia."},
                    {"simbolo": r"$\log_2$", "leitura": "logaritmo na base 2", "significado": "Unidade em <b>bits</b> (dígitos binários de sim/não necessários para codificar a mensagem sem perdas). Se usar logaritmo natural $\ln$, a unidade chama-se <i>nats</i>."},
                    {"simbolo": r"0 \log 0 = 0", "leitura": "convenção de continuidade", "significado": "Por limite matemático, $\lim_{p \to 0^+} p \log p = 0$. Eventos impossíveis não contribuem para a entropia."},
                ],
            },
            {
                "tipo": "passos",
                "titulo": "Calculando a Entropia de Duas Moedas",
                "corpo": r"""<p>Vamos comparar a incerteza de uma moeda honesta contra uma moeda viciada:</p>""",
                "passos": [
                    {
                        "faca": r"Moeda Honesta: $P(\text{Cara}) = 0.5$, $P(\text{Coroa}) = 0.5$. Calcule termo a termo: $$H = - (0.5 \log_2 0.5 + 0.5 \log_2 0.5) = - (0.5(-1) + 0.5(-1)) = -(-1) = 1.0\text{ bit}$$",
                        "porque": "Incerteza máxima: precisamos de exatamente 1 pergunta binária (1 bit) para descobrir o resultado."
                    },
                    {
                        "faca": r"Moeda Viciada: $P(\text{Cara}) = 0.9$, $P(\text{Coroa}) = 0.1$. Calcule: $$H = - (0.9 \log_2 0.9 + 0.1 \log_2 0.1) = - (0.9(-0.152) + 0.1(-3.322)) = - (-0.137 - 0.332) = 0.469\text{ bits}$$",
                        "porque": "A incerteza despencou para menos da metade: quase sempre dará Cara!"
                    },
                    {
                        "faca": r"Moeda de Dois Lados Iguais: $P(\text{Cara}) = 1.0$, $P(\text{Coroa}) = 0.0$. $$H = - (1.0 \log_2 1.0 + 0) = 0.0\text{ bits}$$",
                        "porque": "Certeza absoluta: zero incerteza, zero entropia."
                    }
                ],
                "conclusao": r"A entropia atinge seu pico máximo exatamente quando todas as opções são <b>equiprováveis (distribuição uniforme)</b>, e cai para zero quando o resultado é 100% determinístico."
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Calculando a Entropia de uma Distribuição de Tokens",
                "codigo": r'''import numpy as np

def entropia_shannon(probabilidades, base=2):
    # Filtra probabilidades estritamente positivas para evitar log(0)
    p = np.array(probabilidades)
    p = p[p > 0]
    if base == 2:
        return -np.sum(p * np.log2(p))
    else:
        return -np.sum(p * np.log(p)) # em nats

# Cenário 1: Modelo hesitante e confuso sobre o próximo token (4 opções com 25% cada)
p_confuso = [0.25, 0.25, 0.25, 0.25]

# Cenário 2: Modelo confiante e assertivo (94% em um token, 2% nos outros)
p_confiante = [0.94, 0.02, 0.02, 0.02]

h_confuso = entropia_shannon(p_confuso)
h_confiante = entropia_shannon(p_confiante)

print(f"Entropia do modelo confuso  : {h_confuso:.3f} bits (máxima incerteza: log2(4) = 2.0)")
print(f"Entropia do modelo confiante: {h_confiante:.3f} bits (alta assertividade!)")
assert h_confuso > h_confiante * 4, "O modelo confuso deve ter entropia muito maior!"''',
                "experimentos": [
                    "Varie a probabilidade $p$ de uma Bernoulli de 0.01 a 0.99 e plote a curva de Shannon. Observe o topo da curva em $p = 0.5$.",
                    "Entenda por que a Perplexidade (PPL) usada para avaliar LLMs é simplesmente $2^{H(X)}$ (o número equivalente de escolhas difíceis que o modelo tem pela frente)."
                ]
            }
        ],
        "resumo": [
            "A auto-informação mede a surpresa de um evento individual ($-\log_2 P(x)$).",
            "A Entropia de Shannon quantifica a incerteza média global de uma distribuição de probabilidade.",
            "Distribuições uniformes têm entropia máxima e modelos determinísticos têm entropia zero."
        ],
        "proxima": r"O que acontece quando comparamos a distribuição real dos dados com a distribuição predita pela nossa IA? Entra em cena a Entropia Cruzada (Cross-Entropy).",
        "referencias": [
            {"obra": "Shannon, C. (1948). A Mathematical Theory of Communication", "trecho": "Bell System Technical Journal", "uso": "Definição fundacional da medida de informação e entropia"},
            {"obra": "Cover & Thomas. Elements of Information Theory", "trecho": "Capítulo 2: Entropy, Relative Entropy, and Mutual Information", "uso": "Tratamento matemático rigoroso de medidas de informação"}
        ]
    },

    # =========================================================================
    # TÓPICO 35: Entropia Cruzada (Cross-Entropy Loss) e função Softmax
    # =========================================================================
    "Entropia Cruzada (Cross-Entropy Loss) e função Softmax": {
        "v": 2,
        "duracao": 35,
        "gancho": r"""Como penalizar um modelo que jura com 99% de certeza que um gato é um cachorro? A função <b>Softmax</b> converte números brutos arbitrários em uma distribuição de probabilidades genuína, e a <b>Entropia Cruzada (Cross-Entropy)</b> aplica uma punição exponencial e impiedosa para erros confiantes. Por que essa dupla é a função de perda mais utilizada em toda a inteligência artificial moderna?""",
        "prerequisitos": [
            "Entropia de Shannon (Tópico 34)",
            "Logaritmos e exponenciais (Tópico 31)",
            "Derivadas parciais (Tópico 16)"
        ],
        "objetivos": [
            "compreender a função Softmax como a generalização multidimensional da Sigmoide;",
            "deduzir a fórmula da Entropia Cruzada $H(y, \hat{y}) = -\sum y_i \ln \hat{y}_i$;",
            "provar a dedução do gradiente da Softmax + Cross-Entropy: $\frac{\partial L}{\partial z_i} = p_i - y_i$."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "Transformando Logits em Probabilidades",
                "titulo": "A Função Softmax",
                "corpo": r"""<p>A última camada de uma rede neural classifica entre $K$ classes emitindo um vetor de pontuações brutas não restritas $\mathbf{z} \in \mathbb{R}^K$ (chamados <b>logits</b>). Esses números podem ser negativos, zero ou muito grandes.</p>
<p>A função <b>Softmax</b> transforma esses logits em um vetor de probabilidades válidas $\mathbf{p}$ (onde cada $p_i \in (0, 1)$ e $\sum_{i=1}^K p_i = 1$):</p>
$$p_i = \text{softmax}(\mathbf{z})_i = \frac{e^{z_i}}{\sum_{j=1}^K e^{z_j}}$$
<p>O exponencial $e^{z_i}$ amplifica os contrastes: a classe com o maior logit recebe a maior fatia da pizza de probabilidade, mas as outras classes continuam recebendo frações menores não-nulas, permitindo que o gradiente flua de volta por todas elas!</p>""",
            },
            {
                "tipo": "texto",
                "rotulo": "A Punição pela Falsa Certeza",
                "titulo": "A Fórmula da Entropia Cruzada (Cross-Entropy)",
                "corpo": r"""<p>A Entropia Cruzada mede o número médio de bits necessários para codificar dados vindos da verdadeira distribuição $y$ usando o modelo imperfeito $\hat{y}$:</p>
$$L_{\text{CE}} = H(y, \hat{y}) = -\sum_{i=1}^K y_i \ln(\hat{y}_i)$$
<p>Em tarefas de classificação exclusiva (como prever o próximo token ou classificar a avaliação), o vetor real $y$ é um <b>one-hot vector</b> (tem $1$ na classe correta $c$ e $0$ em todas as outras). Assim, a fórmula colapsa de forma espetacular para um único termo:</p>
$$L_{\text{CE}} = -\ln(\hat{y}_c)$$
<p>Onde $\hat{y}_c$ é a probabilidade atribuída pelo modelo à <b>classe correta</b>!</p>
<ul>
<li>Se o modelo previu com 99% de certeza a classe correta ($\hat{y}_c = 0.99$): $L = -\ln(0.99) = 0.010$ (perda quase zero).</li>
<li>Se previu com 50% de incerteza ($\hat{y}_c = 0.50$): $L = -\ln(0.50) = 0.693$.</li>
<li>Se previu com 1% de chance para a classe correta ($\hat{y}_c = 0.01$): $L = -\ln(0.01) = 4.605$ (punição exponencial!).</li>
</ul>""",
            },
            {
                "tipo": "passos",
                "titulo": "A Derivada Mais Bonita da IA: p_i - y_i",
                "corpo": r"""<p>Quando combinamos a Softmax com a Cross-Entropy, as derivadas complexas de frações e exponenciais se cancelam perfeitamente na Regra da Cadeia:</p>""",
                "passos": [
                    {
                        "faca": r"Calcule a derivada da perda $L = -\sum_k y_k \ln(p_k)$ em relação ao logit bruto $z_i$: $$\frac{\partial L}{\partial z_i} = \sum_k \frac{\partial L}{\partial p_k} \frac{\partial p_k}{\partial z_i}$$",
                        "porque": "Regra da cadeia para derivadas de múltiplas variáveis."
                    },
                    {
                        "faca": r"Substitua $\frac{\partial L}{\partial p_k} = -\frac{y_k}{p_k}$ e a derivada da Softmax $\frac{\partial p_k}{\partial z_i} = p_k(\delta_{ki} - p_i)$ (onde $\delta_{ki}=1$ se $k=i$ e $0$ se $k \neq i$): $$\frac{\partial L}{\partial z_i} = -\sum_k \frac{y_k}{p_k} \left[ p_k(\delta_{ki} - p_i) \right] = -\sum_k y_k (\delta_{ki} - p_i)$$",
                        "porque": "O termo $p_k$ no numerador cancela rigorosamente com $p_k$ no denominador!"
                    },
                    {
                        "faca": r"Distribua o somatório: $$-\sum_k y_k \delta_{ki} + \sum_k y_k p_i = -y_i + p_i \sum_k y_k$$",
                        "porque": "O único termo sobrevivente com $\delta_{ki}$ é quando $k=i$."
                    },
                    {
                        "faca": r"Como $y$ é uma distribuição de probabilidade, a soma de suas componentes é $\sum y_k = 1$: $$\frac{\partial L}{\partial z_i} = p_i - y_i$$",
                        "porque": "Chegamos ao resultado de elegância suprema!"
                    }
                ],
                "conclusao": r"O gradiente que a GPU precisa retropropagar para a rede inteira é simplesmente: <b>a probabilidade que o modelo chutou MENOS o rótulo real (predição - alvo)</b>! Se o modelo previu $0.8$ e o real era $1.0$, o gradiente é $-0.2$."
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Softmax, Cross-Entropy e Gradiente Manual",
                "codigo": r'''import numpy as np

# Logits de saída de um modelo para 3 classes: [Ruim, Regular, Ótimo]
logits = np.array([2.0, 1.0, 0.1])
# Rótulo real: a avaliação era 'Ruim' (classe 0)
y_real = np.array([1.0, 0.0, 0.0])

# 1. Softmax numericamente estável
exp_z = np.exp(logits - np.max(logits))
probs = exp_z / np.sum(exp_z)

# 2. Cross-Entropy Loss
loss_ce = -np.sum(y_real * np.log(probs + 1e-12))

# 3. Gradiente exato em relação aos logits: (p - y)
grad_logits = probs - y_real

print("Análise de Cross-Entropy Loss:")
print(f"Logits de entrada  : {logits}")
print(f"Probabilidades (p) : {probs.round(4)} -> Classe mais provável: {np.argmax(probs)}")
print(f"Rótulo Real (y)    : {y_real}")
print(f"Perda Cross-Entropy: {loss_ce:.4f}")
print(f"Gradiente (p - y)  : {grad_logits.round(4)}")

# Verificação: a soma dos gradientes em relação a todos os logits é sempre zero!
print(f"Soma dos gradientes: {np.sum(grad_logits):.8f} (equilíbrio dinâmico preservado)")
assert np.isclose(np.sum(grad_logits), 0.0), "A soma dos gradientes da Softmax deve ser zero!"''',
                "experimentos": [
                    "Modifique o rótulo real para a classe 2 (Ótimo, que teve probabilidade baixa de apenas 10%). Observe a perda explodir para mais de 2.0 e o gradiente da classe 2 ficar em $-0.90$ para forçar o peso a subir com agressividade.",
                    "Entenda por que modelos generativos auto-regressivos como GPT treinam minimizando exatamente essa Cross-Entropy token a token."
                ]
            }
        ],
        "resumo": [
            "Softmax mapeia logits contínuos em distribuições estocásticas normalizadas.",
            "Cross-Entropy penaliza exponencialmente desvios onde o modelo expressa certeza errônea.",
            "A união analítica de Softmax e Cross-Entropy resulta no gradiente linear mais limpo do cálculo: $\mathbf{p} - \mathbf{y}$."
        ],
        "proxima": r"Como medir a diferença entre duas distribuições contínuas de probabilidade sem usar a entropia direta? Vamos conhecer a Divergência de Kullback-Leibler (KL).",
        "referencias": [
            {"obra": "Goodfellow, Bengio & Courville. Deep Learning", "trecho": "Capítulo 6.2.2.3: Softmax Units for Multinoulli Output Distributions", "uso": "Dedução do gradiente de Softmax com Cross-Entropy e saturação"},
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Capítulo 9.1: Maximum Likelihood and Cross-Entropy Equivalence", "uso": "Prova da equivalência entre MLE e minimização de entropia cruzada"}
        ]
    },

    # =========================================================================
    # TÓPICO 36: Divergência de Kullback-Leibler (KL Divergence)
    # =========================================================================
    "Divergência de Kullback-Leibler (KL Divergence)": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""No alinhamento do ChatGPT com seres humanos (RLHF), como instruir o modelo a se tornar prestativo e seguro sem que ele <i>'enlouqueça'</i> e esqueça toda a fluência e vocabulário do modelo base pré-treinado original? A resposta é a <b>Penalidade KL ($D_{\text{KL}}$)</b>. Por que a Divergência KL mede a distância entre distribuições e por que ela é <b>fundamentalmente assimétrica</b> ($D_{\text{KL}}(P \parallel Q) \neq D_{\text{KL}}(Q \parallel P)$)?""",
        "prerequisitos": [
            "Entropia de Shannon e Cross-Entropy (Tópicos 34 e 35)",
            "Esperança matemática (Tópico 23)"
        ],
        "objetivos": [
            "compreender a definição da Divergência KL como perda de informação por usar a distribuição $Q$ para aproximar $P$;",
            "provar que $D_{\text{KL}}(P \parallel Q) \ge 0$ (Desigualdade de Gibbs) com igualdade se e somente se $P = Q$;",
            "entender o impacto da assimetria da KL (Mode-seeking vs. Mean-seeking) e seu papel no RLHF e VAEs."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Distância Informacional",
                "titulo": "O que é a Divergência KL?",
                "corpo": r"""<p>A <b>Divergência de Kullback-Leibler</b> (também chamada de <i>entropia relativa</i>) mede a ineficiência de codificar eventos que seguem a verdadeira distribuição $P$ usando um código otimizado para uma distribuição aproximada $Q$:</p>
$$D_{\text{KL}}(P \parallel Q) = \sum_{x} P(x) \ln\left( \frac{P(x)}{Q(x)} \right) = \sum_x P(x) \ln P(x) - \sum_x P(x) \ln Q(x)$$
<p>Reescrevendo em termos das entropias que já conhecemos:</p>
$$D_{\text{KL}}(P \parallel Q) = H(P, Q) - H(P) = \text{Cross-Entropy} - \text{Entropia Real}$$
<p>Como a entropia real $H(P)$ de um dataset fixo é constante, <b>minimizar a Cross-Entropy é rigorosamente idêntico a minimizar a Divergência KL entre o modelo e a realidade</b>!</p>""",
            },
            {
                "tipo": "pense",
                "titulo": "Por que a Divergência KL NÃO é uma distância geométrica comum?",
                "pergunta": r"""A distância entre São Paulo e Rio de Janeiro é a mesma que entre Rio de Janeiro e São Paulo ($d(A, B) = d(B, A)$). Por que a Divergência KL não respeita essa simetria ($D_{\text{KL}}(P \parallel Q) \neq D_{\text{KL}}(Q \parallel P)$)?""",
                "resposta": r"""<p>A KL não é simétrica porque o peso da média ponderada é dado pela <b>primeira distribuição ($P$)</b>!</p>
<ul>
<li><b>Forward KL $D_{\text{KL}}(P \parallel Q)$ (Mean-seeking):</b> A média é tomada sob $P$. Se $P(x) > 0$, $Q(x)$ é proibida de ser zero (senão $\ln(P/0) \to \infty$). Isso força $Q$ a se espalhar para cobrir todos os modos de $P$.</li>
<li><b>Reverse KL $D_{\text{KL}}(Q \parallel P)$ (Mode-seeking):</b> A média é tomada sob $Q$. Se $P(x) = 0$, $Q(x)$ precisa ser rigorosamente zero para evitar punição. Isso faz $Q$ focar com precisão em um único modo, ignorando o resto. É exatamente o comportamento buscado no RLHF!</li>
</ul>"""
            },
            {
                "tipo": "ponte",
                "titulo": "Onde isso vive na IA: A Rédea Curta do RLHF",
                "corpo": r"""<p>Nos algoritmos de alinhamento como PPO (Proximal Policy Optimization) e DPO (Direct Preference Optimization), a função de recompensa otimizada pelo LLM inclui uma penalidade KL explícita:</p>
$$\max_\theta \mathbb{E}\left[ R(x, y) \right] - \beta \cdot D_{\text{KL}}\left(\pi_\theta(y \mid x) \parallel \pi_{\text{base}}(y \mid x)\right)$$
<p>O termo $R(x, y)$ premia respostas úteis, mas a penalidade $-\beta D_{\text{KL}}$ puxa o modelo de volta se ele tentar 'hackear' o sistema ou se afastar demais do modelo base $\pi_{\text{base}}$. É o cinto de segurança que impede alucinações e colapso de linguagem!</p>""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Calculando a Assimetria da Divergência KL",
                "codigo": r'''import numpy as np

# Duas distribuições de probabilidade discretas sobre 3 categorias:
P = np.array([0.70, 0.20, 0.10]) # Distribuição alvo (real)
Q = np.array([0.40, 0.40, 0.20]) # Distribuição do modelo (aproximada)

def kl_divergence(p, q):
    # D_KL(P || Q) = sum( p * log(p / q) )
    p = np.clip(p, 1e-12, 1.0)
    q = np.clip(q, 1e-12, 1.0)
    return np.sum(p * np.log(p / q))

kl_PQ = kl_divergence(P, Q)
kl_QP = kl_divergence(Q, P)

print(f"Distribuição P: {P}")
print(f"Distribuição Q: {Q}")
print(f"D_KL(P || Q)  : {kl_PQ:.6f} nats")
print(f"D_KL(Q || P)  : {kl_QP:.6f} nats")
print(f"Diferença     : {abs(kl_PQ - kl_QP):.6f} (Assimetria Comprovada!)")

assert not np.isclose(kl_PQ, kl_QP), "A Divergência KL deve ser fundamentalmente assimétrica!"
assert kl_divergence(P, P) == 0.0, "D_KL de uma distribuição com ela mesma deve ser zero!"
print("Propriedades de Kullback-Leibler verificadas com perfeição!")''',
                "experimentos": [
                    "Faça $Q$ ter probabilidade zero onde $P$ é positivo (ex.: <code>Q = [0.0, 0.8, 0.2]</code>) e veja como a divergência explode para o infinito.",
                    "Implemente a Divergência de Jensen-Shannon (JSD), que é a versão simétrica da KL: $JSD(P, Q) = \frac{1}{2} D_{KL}(P \parallel M) + \frac{1}{2} D_{KL}(Q \parallel M)$, onde $M = \frac{P+Q}{2}$."
                ]
            }
        ],
        "resumo": [
            "A Divergência KL quantifica a perda de informação ao modelar a distribuição real $P$ através de $Q$.",
            "É sempre maior ou igual a zero, anulando-se exclusivamente quando as distribuições são idênticas.",
            "Sua assimetria matemática é explorada no alinhamento de LLMs (RLHF) para ancorar modelos afinados ao modelo base."
        ],
        "proxima": r"Para fechar o módulo, vamos analisar as funções de perda de regressão contínua: MSE, MAE e a elegante perda de Huber.",
        "referencias": [
            {"obra": "Cover & Thomas. Elements of Information Theory", "trecho": "Capítulo 2.3: Relative Entropy (Kullback-Leibler Distance)", "uso": "Prova formal da desigualdade de Gibbs via convexidade da função logaritmo"},
            {"obra": "Goodfellow, Bengio & Courville. Deep Learning", "trecho": "Capítulo 3.13: Information Theory", "uso": "Aplicações em VAEs e aprendizado de representações"}
        ]
    },

    # =========================================================================
    # TÓPICO 37: Funções de perda de regressão (MSE, MAE, Huber) e classificação
    # =========================================================================
    "Funções de perda de regressão (MSE, MAE, Huber) e classificação": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Se um cliente da nossa cafeteria diz que esperou 1.000 minutos por um café (um erro grosseiro de digitação no aplicativo), como seu modelo de previsão deve reagir? O <b>MSE</b> tentará desesperadamente ajustar a curva para agradar esse outlier, destruindo as previsões de todos os outros clientes. O <b>MAE</b> ignorará o erro, mas oscilará perto do ponto ótimo. Como a <b>perda de Huber</b> combina a suavidade do cálculo com a imunidade contra ruído extremo?""",
        "prerequisitos": [
            "Derivadas básicas e módulos (Tópicos 12 e 13)",
            "Média vs. Mediana e outliers (Tópico 22)"
        ],
        "objetivos": [
            "comparar analiticamente MSE (L2), MAE (L1) e a perda de Huber;",
            "compreender por que o MSE prevê a média condicional e o MAE prevê a mediana condicional;",
            "identificar qual função de perda escolher conforme a presença de ruído e as exigências da aplicação de IA."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "O Triângulo das Perdas de Regressão",
                "titulo": "As Três Grandes Métricas Contínuas",
                "corpo": r"""<p>Quando a IA precisa prever um número contínuo (tempo de entrega, temperatura, preço de casa), a escolha da função de perda define a 'personalidade' do modelo:</p>
<ul>
<li><b>MSE (Mean Squared Error / Perda L2):</b>
$$L_{\text{MSE}} = \frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2$$
Penaliza erros grandes de forma quadrática. Se o erro dobra, a penalidade quadruplica! Sua derivada é suave ($2(y - \hat{y})$), facilitando a convergência via gradiente, mas é extremamente frágil a outliers.</li>
<li><b>MAE (Mean Absolute Error / Perda L1):</b>
$$L_{\text{MAE}} = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i|$$
Penaliza proporcionalmente ao tamanho do erro linear. É muito robusta a ruídos extremos. No entanto, sua derivada não é suave na origem: ela salta descontinuamente de $-1$ para $+1$, fazendo o otimizador quicar em torno do mínimo.</li>
<li><b>Perda de Huber (O Melhor dos Dois Mundos):</b>
$$L_\delta(e) = \begin{cases} \frac{1}{2} e^2 & \text{se } |e| \le \delta \\ \delta |e| - \frac{1}{2}\delta^2 & \text{se } |e| > \delta \end{cases}$$
Para erros pequenos ($|e| \le \delta$), ela se comporta como MSE (derivada suave e estável). Para erros gigantes ($|e| > \delta$), ela vira MAE linear, impedindo que outliers explodam o gradiente!</li>
</ul>""",
            },
            {
                "tipo": "visual",
                "titulo": "Formatos Geométricos: Parábola, V e Huber",
                "corpo": r"""<p>Veja a curvatura das três funções em relação ao resíduo de erro $(y - \hat{y})$:</p>""",
                "svg": SVG_LOSS_REG,
                "legenda": "MSE é uma parábola de rápida subida. MAE é um V de ponta afiada. Huber suaviza a ponta com uma parábola e estende os braços linearmente.",
            },
            {
                "tipo": "tabela",
                "titulo": "Guia de Decisão de Funções de Perda",
                "cabecalho": ["Função de Perda", "Alvo Estatístico", "Comportamento do Gradiente", "Quando usar?"],
                "linhas": [
                    ["MSE (L2)", "Média $\mathbb{E}[y \mid x]$", "Proporcional ao erro ($2e$); encolhe suavemente até zero", "Dados limpos com ruído puramente gaussiano, regressão padrão"],
                    ["MAE (L1)", "Mediana", "Constante ($\pm 1$); não diminui perto do zero", "Dados com muitos outliers e caudas pesadas"],
                    ["Huber", "Média perto do centro, Mediana nas caudas", "Linear suave no centro e saturado em $\pm \delta$ nas pontas", "Detecção de objetos (YOLO, Faster R-CNN), redes neurais profundas com ruído"]
                ]
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Comparando Gradientes com um Outlier Extremo",
                "codigo": r'''import numpy as np

# Resíduos de erro: 4 exemplos normais e 1 outlier gigantesco
erros = np.array([0.2, -0.4, 0.1, -0.3, 50.0]) # 50.0 é o erro do outlier

# 1. Gradiente MSE: 2 * e
grad_mse = 2.0 * erros

# 2. Gradiente MAE: sign(e)
grad_mae = np.sign(erros)

# 3. Gradiente Huber com delta = 1.0
delta = 1.0
grad_huber = np.where(np.abs(erros) <= delta, erros, delta * np.sign(erros))

print(f"Resíduos de erro: {erros}\n")
print(f"Gradiente MSE  : {grad_mse.round(2)}")
print(f"  -> O outlier gerou gradiente de {grad_mse[-1]:.1f}! (Vai destruir o modelo)")
print(f"Gradiente MAE  : {grad_mae.round(2)}")
print(f"  -> O outlier gerou gradiente de {grad_mae[-1]:.1f} (mesmo peso de qualquer erro)")
print(f"Gradiente Huber: {grad_huber.round(2)}")
print(f"  -> O outlier foi perfeitamente contido no teto de delta = {grad_huber[-1]:.1f}!")''',
                "experimentos": [
                    "Observe como no MSE o exemplo outlier representa mais de 98% de todo o gradiente acumulado do batch.",
                    "Altere o hiperparâmetro <code>delta = 2.0</code> e observe como o raio de suavidade quadrática se expande."
                ]
            }
        ],
        "resumo": [
            "O MSE otimiza para a média e tem derivadas suaves, mas é hipervulnerável a anomalias.",
            "O MAE otimiza para a mediana e é robusto a ruídos, mas tem derivada descontínua na origem.",
            "A perda de Huber combina convergência suave perto do alvo com imunidade total contra gradientes explosivos de outliers."
        ],
        "proxima": r"Completamos o Módulo 4! Entramos agora na fronteira final: a Geometria Vetorial e a Matemática da Atenção dos Transformers.",
        "referencias": [
            {"obra": "Huber, P. J. (1964). Robust Estimation of a Location Parameter", "trecho": "Annals of Mathematical Statistics", "uso": "Artigo original propondo a função de perda robusta"},
            {"obra": "Goodfellow, Bengio & Courville. Deep Learning", "trecho": "Capítulo 5.5: Estimators, Bias and Variance", "uso": "Conexão entre funções de perda, penalidades e normas L1 e L2"}
        ]
    }
}
