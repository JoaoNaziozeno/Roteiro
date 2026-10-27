# -*- coding: utf-8 -*-
"""
Aulas Visuais de Matemática v2 — Módulo 3: Probabilidade & Estatística para IA.
Baseado em Allen Downey (Think Stats / Think Bayes),
Deisenroth, Faisal & Ong (Mathematics for Machine Learning, Cap. 6) e
Goodfellow, Bengio & Courville (Deep Learning, Cap. 3 e 5).
"""

from math_lessons_v2_samples import LESSONS_V2_SAMPLES

# SVG: Discreto (PMF) vs Contínuo (PDF)
SVG_DISCRETO_CONTINUO = r'''<svg viewBox="0 0 540 220" class="lv2-svg" role="img" aria-label="Comparativo: Variável Discreta PMF vs Contínua PDF">
  <!-- Painel Esquerdo: Discreto PMF -->
  <line x1="30" y1="180" x2="240" y2="180" class="sv-ax"/>
  <line x1="40" y1="190" x2="40" y2="30" class="sv-ax"/>
  <text x="75" y="25" class="sv-t" style="font-weight:700">Discreta (PMF) - P(X = x)</text>
  <!-- Barras discretas -->
  <rect x="65" y="120" width="16" height="60" fill="#4A5C6A" rx="2"/>
  <rect x="95" y="70" width="16" height="110" fill="#CCD0CF" rx="2"/>
  <rect x="125" y="90" width="16" height="90" fill="#4A5C6A" rx="2"/>
  <rect x="155" y="140" width="16" height="40" fill="#4A5C6A" rx="2"/>
  <rect x="185" y="160" width="16" height="20" fill="#4A5C6A" rx="2"/>
  <text x="96" y="60" class="sv-tm" style="font-size:10px">0.35</text>
  <text x="70" y="200" class="sv-tm">1</text>
  <text x="100" y="200" class="sv-tm">2</text>
  <text x="130" y="200" class="sv-tm">3</text>
  <text x="160" y="200" class="sv-tm">4</text>
  <text x="190" y="200" class="sv-tm">5</text>
  <text x="50" y="215" class="sv-tm" style="font-size:10px">Soma das barras = 1.0 (100%)</text>

  <!-- Divisor -->
  <line x1="260" y1="20" x2="260" y2="200" class="sv-thin sv-dash"/>

  <!-- Painel Direito: Contínuo PDF -->
  <line x1="290" y1="180" x2="510" y2="180" class="sv-ax"/>
  <line x1="300" y1="190" x2="300" y2="30" class="sv-ax"/>
  <text x="330" y="25" class="sv-t" style="font-weight:700">Contínua (PDF) - Densidade p(x)</text>
  <!-- Curva Gaussiana -->
  <path d="M 305 178 Q 360 178 390 120 T 410 40 T 430 120 Q 460 178 505 178" class="sv-a" style="stroke-width:2.5"/>
  <!-- Área sombreada entre a e b -->
  <path d="M 390 120 T 410 40 T 430 120 L 430 180 L 390 180 Z" fill="rgba(74,92,106,0.25)"/>
  <line x1="390" y1="120" x2="390" y2="180" class="sv-thin sv-dash"/>
  <line x1="430" y1="120" x2="430" y2="180" class="sv-thin sv-dash"/>
  <text x="385" y="195" class="sv-tm">a</text>
  <text x="425" y="195" class="sv-tm">b</text>
  <text x="382" y="150" class="sv-t" style="font-size:11px;font-weight:700">Área = P(a ≤ X ≤ b)</text>
  <text x="315" y="215" class="sv-tm" style="font-size:10px">P(X = a) pontual é ZERO; probabilidade é ÁREA!</text>
</svg>'''

# SVG: Curva Normal Gaussiana e Regra 68-95-99.7
SVG_NORMAL_GAUSS = r'''<svg viewBox="0 0 540 220" class="lv2-svg" role="img" aria-label="Distribuição Normal Gaussiana com desvios padrão">
  <!-- Eixo X -->
  <line x1="30" y1="170" x2="510" y2="170" class="sv-ax"/>
  <!-- Centro média mu -->
  <line x1="270" y1="175" x2="270" y2="35" class="sv-thin sv-dash"/>
  <text x="265" y="190" class="sv-t" style="font-weight:700">μ (média)</text>

  <!-- Curva Normal -->
  <path d="M 50 169 Q 150 168 200 130 T 270 40 T 340 130 Q 390 168 490 169" class="sv-a" style="stroke-width:2.8"/>

  <!-- Faixa de 1 sigma (68.2%) -->
  <rect x="210" y="45" width="120" height="125" fill="rgba(204,208,207,0.12)" rx="3"/>
  <line x1="210" y1="170" x2="210" y2="120" class="sv-thin"/>
  <line x1="330" y1="170" x2="330" y2="120" class="sv-thin"/>
  <text x="195" y="190" class="sv-tm">μ - 1σ</text>
  <text x="315" y="190" class="sv-tm">μ + 1σ</text>
  <text x="245" y="105" class="sv-t" style="font-weight:700">68.2%</text>

  <!-- Faixa de 2 sigma (95.4%) -->
  <line x1="150" y1="170" x2="150" y2="155" class="sv-thin sv-dash"/>
  <line x1="390" y1="170" x2="390" y2="155" class="sv-thin sv-dash"/>
  <text x="135" y="190" class="sv-tm">μ - 2σ</text>
  <text x="375" y="190" class="sv-tm">μ + 2σ</text>

  <!-- Indicador de 95% -->
  <line x1="150" y1="25" x2="390" y2="25" class="sv-b"/>
  <text x="250" y="20" class="sv-tm" style="font-weight:700">95.4% dos dados</text>
</svg>'''

# SVG: Trade-off Viés vs Variância
SVG_BIAS_VARIANCE = r'''<svg viewBox="0 0 520 220" class="lv2-svg" role="img" aria-label="Curvas do Trade-off Viés vs Variância">
  <!-- Eixos -->
  <line x1="40" y1="190" x2="490" y2="190" class="sv-ax"/>
  <line x1="50" y1="200" x2="50" y2="25" class="sv-ax"/>
  <text x="390" y="206" class="sv-tm">Complexidade do Modelo →</text>
  <text x="15" y="25" class="sv-tm">Erro</text>

  <!-- Curva do Viés ao quadrado (cai com a complexidade) -->
  <path d="M 60 40 Q 180 140 480 175" class="sv-b" style="stroke-width:2.2"/>
  <text x="400" y="165" class="sv-tm">Viés² (Underfitting)</text>

  <!-- Curva da Variância (sobe com a complexidade) -->
  <path d="M 60 180 Q 280 170 480 40" class="sv-b sv-dash" style="stroke-width:2.2"/>
  <text x="390" y="55" class="sv-tm">Variância (Overfitting)</text>

  <!-- Curva do Erro Total (U-shape) -->
  <path d="M 60 70 Q 240 160 480 85" class="sv-a" style="stroke-width:3"/>
  <text x="270" y="150" class="sv-t" style="font-weight:700">Erro Total (Teste)</text>

  <!-- Ponto Ótimo -->
  <circle cx="240" cy="120" r="5" class="sv-fill"/>
  <line x1="240" y1="120" x2="240" y2="190" class="sv-thin sv-dash"/>
  <text x="205" y="205" class="sv-t" style="font-size:11px;font-weight:700">Ponto Ideal (Sweet Spot)</text>
</svg>'''

GUIDES_MOD3_V2 = {
    # =========================================================================
    # TÓPICO 21: Variáveis aleatórias discretas e contínuas
    # =========================================================================
    "Variáveis aleatórias discretas e contínuas": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Se você sortear uma palavra de um vocabulário, há uma probabilidade exata (ex.: 3%) de sair a palavra <i>"inteligência"</i>. Mas se você medir a altura exata de uma pessoa com precisão atômica ($1.75239481\dots\text{ m}$), a probabilidade matemática de encontrar alguém com essa altura exata é <b>rigorosamente zero</b> ($P(X = x) = 0$). Como a IA lida com essa aparente contradição matemática?""",
        "prerequisitos": [
            "Conceito de limite e área sob a curva (Tópico 12)",
            "Somatórios ($\sum$) e conjuntos finitos"
        ],
        "objetivos": [
            "compreender o que é uma variável aleatória como função que mapeia eventos em números reais;",
            "diferenciar Função Massa de Probabilidade (PMF, discreta) de Função Densidade de Probabilidade (PDF, contínua);",
            "entender por que a probabilidade em variáveis contínuas é dada pela área sob a curva (integral) e não pela altura do gráfico."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Definição Desmistificada",
                "titulo": "O que é uma Variável Aleatória?",
                "corpo": r"""<p>Apesar do nome enganoso, uma <b>variável aleatória $X$</b> não é uma variável comum e nem é caótica: ela é uma <b>regra matemática (função)</b> que atribui um número real numérico a cada resultado de um processo estocástico do mundo real.</p>
<p>Allen Downey, no célebre <i>Think Stats</i>, divide essas variáveis em dois grandes reinos com regras completamente distintas:</p>
<ul>
<li><b>Discretas:</b> O conjunto de resultados possíveis é enumerável (como uma lista de inteiros). Exemplo: o próximo token predito por um LLM entre as 32.000 opções do vocabulário, ou o número de estrelas de uma avaliação da nossa cafeteria $\{1, 2, 3, 4, 5\}$.</li>
<li><b>Contínuas:</b> A variável pode assumir qualquer valor real em uma escala contínua $\mathbb{R}$. Exemplo: o tempo de resposta da inferência em milissegundos ($142.384\dots\text{ ms}$) ou o peso de uma sinapse neural.</li>
</ul>""",
            },
            {
                "tipo": "visual",
                "titulo": "O Grande Contraste: Altura de Barras vs. Área Contínua",
                "corpo": r"""<p>Veja como o conceito de probabilidade muda radicalmente entre os dois mundos:</p>""",
                "svg": SVG_DISCRETO_CONTINUO,
                "legenda": "No mundo discreto, cada barra tem sua probabilidade direta e a soma é 1. No mundo contínuo, a probabilidade é a ÁREA sob a curva em um intervalo [a, b].",
            },
            {
                "tipo": "notacao",
                "titulo": "Como ler a notação formal dos livros",
                "corpo": r"""<p>Veja as fórmulas que regem os dois domínios:</p>""",
                "itens": [
                    {"simbolo": r"$\text{PMF}: P(X = x)$", "leitura": "função massa de probabilidade", "significado": "Para discretas. A soma de todos os estados possíveis é sempre 100%: $\sum_{i} P(X = x_i) = 1$."},
                    {"simbolo": r"$\text{PDF}: p(x)$", "leitura": "função densidade de probabilidade", "significado": "Para contínuas. $p(x)$ não é uma probabilidade, é uma <b>densidade</b>! Pode inclusive ser maior que 1. A probabilidade só existe no intervalo: $P(a \le X \le b) = \int_a^b p(x) dx$."},
                    {"simbolo": r"$P(X = a) = 0$", "leitura": "probabilidade pontual contínua é zero", "significado": "Como a largura de um único ponto geométrico é zero ($dx \to 0$), a área sob a curva naquele ponto específico é rigorosamente zero."},
                ],
            },
            {
                "tipo": "ponte",
                "titulo": "Onde isso vive na IA: Sampling e Geração de Texto em LLMs",
                "corpo": r"""<p>Quando o ChatGPT gera texto, a última camada emite um vetor de <b>probabilidades discretas (uma PMF)</b> sobre todo o vocabulário através da função Softmax:</p>
$$P(\text{token} = w_i) = \frac{e^{z_i / T}}{\sum_{j} e^{z_j / T}}$$
<p>O hiperparâmetro de <b>Temperatura ($T$)</b> achata ou afia essa PMF discreta:</p>
<ul>
<li>$T \to 0$ (Argmax ganancioso): Pega sempre o token de probabilidade máxima (determinístico).</li>
<li>$T = 0.7$ (Criativo equilibrado): Amostra da PMF, permitindo que tokens plausíveis com 15% de chance sejam escolhidos às vezes, gerando respostas variadas.</li>
</ul>""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Amostragem Discreta com Temperatura",
                "codigo": r'''import numpy as np

# Logits de 4 palavras candidatas após o processamento da cafeteria:
# ["excelente", "bom", "regular", "horrível"]
palavras = ["excelente", "bom", "regular", "horrível"]
logits = np.array([3.0, 2.0, 0.5, -1.0])

def softmax_com_temperatura(z, T=1.0):
    # Subtrai o máximo para estabilidade numérica
    exp_z = np.exp((z - np.max(z)) / T)
    return exp_z / np.sum(exp_z)

# Testando duas temperaturas: T=1.0 (natural) e T=0.2 (focado)
p_natural = softmax_com_temperatura(logits, T=1.0)
p_focado = softmax_com_temperatura(logits, T=0.2)

print("Distribuição discreta PMF (T = 1.0):")
for w, p in zip(palavras, p_natural):
    print(f"  {w:10s}: {p*100:5.1f}%")

print("\nDistribuição discreta afiada (T = 0.2):")
for w, p in zip(palavras, p_focado):
    print(f"  {w:10s}: {p*100:5.1f}%")

# Amostrando 5 vezes da PMF natural
np.random.seed(42)
sorteios = np.random.choice(palavras, size=5, p=p_natural)
print("\n5 sorteios da distribuição com T=1.0:", list(sorteios))''',
                "experimentos": [
                    "Aumente a temperatura para <code>T = 5.0</code> e observe como as probabilidades se aproximam de um sorteio perfeitamente uniforme de 25% para cada palavra.",
                    "Verifique que a soma das probabilidades em qualquer temperatura continua dando exatamente 1.0 (propriedade sagrada de uma PMF)."
                ]
            }
        ],
        "resumo": [
            "Uma variável aleatória mapeia eventos do mundo em números reais matematicamente tratáveis.",
            "Variáveis discretas utilizam PMF com somatórios diretos de probabilidades que totalizam 1.",
            "Variáveis contínuas utilizam PDF onde a probabilidade é calculada pela área de uma integral sob a curva."
        ],
        "proxima": r"Agora que conhecemos distribuições de probabilidade, como resumir seu comportamento em números simples? Vamos investigar a Média, a Mediana e a Variância.",
        "referencias": [
            {"obra": "Downey, A. Think Stats: Exploratory Data Analysis in Python", "trecho": "Capítulos 1 e 3: Probability Mass Functions and Cumulative Distribution Functions", "uso": "Abordagem computacional e empírica de variáveis discretas e contínuas"},
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Capítulo 6.1: Discrete and Continuous Probabilities", "uso": "Formalização matemática de espaços amostrais e medidas de probabilidade"}
        ]
    },

    # =========================================================================
    # TÓPICO 22: Média, mediana, variância e desvio padrão
    # =========================================================================
    "Média, mediana, variância e desvio padrão": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Se Bill Gates entrar em um restaurante com 99 pessoas comuns, a <i>renda média</i> do local salta instantaneamente para mais de 10 milhões de reais por pessoa. Mas ninguém ali ficou um centavo mais rico! Por que a <b>média</b> é tão vulnerável a outliers, por que a <b>mediana</b> resiste e por que a fórmula da variância divide por $n-1$ em vez de $n$?""",
        "prerequisitos": [
            "Somatórios ($\sum$) e álgebra fundamental (Tópico 12)",
            "Variáveis aleatórias (Tópico 21)"
        ],
        "objetivos": [
            "compreender a média como centro de gravidade e a mediana como ponto de corte de 50%;",
            "deduzir a intuição da Variância e do Desvio Padrão como dispersão quadrática em torno do centro;",
            "entender a Correção de Bessel ($n-1$) na variância amostral;",
            "conectar essa padronização à LayerNorm usada no treinamento de LLMs."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "Média vs. Mediana",
                "titulo": "O Centro de Gravidade contra o Meio da Fila",
                "corpo": r"""<p>Para resumir um conjunto de dados com um único número representativo de <i>tendência central</i>, a Estatística oferece dois grandes campeões:</p>
<ul>
<li><b>Média ($\bar{x}$ ou $\mu$):</b> É o centro de gravidade físico dos dados: $\bar{x} = \frac{1}{n} \sum_{i=1}^n x_i$. Se você colocasse cada ponto de dado como um peso sobre uma régua de madeira, a média seria o ponto exato de apoio onde a régua se equilibraria perfeitamente. Por isso, um único valor extremo muito distante (outlier) puxa a régua com uma alavanca brutal!</li>
<li><b>Mediana:</b> É o valor central após ordenar todos os números. Exatamente 50% dos dados estão abaixo dela e 50% acima. Se Bill Gates entrar no restaurante, a mediana salta apenas para a pessoa vizinha na fila, permanecendo praticamente inalterada.</li>
</ul>""",
            },
            {
                "tipo": "notacao",
                "titulo": "Medidas de Dispersão: Variância e Desvio Padrão",
                "corpo": r"""<p>Saber o centro não basta: precisamos saber o quão <b>espalhados</b> os dados estão em torno desse centro:</p>""",
                "itens": [
                    {"simbolo": r"$\sigma^2 = \frac{1}{n}\sum (x_i - \mu)^2$", "leitura": "variância populacional", "significado": "Média dos desvios quadráticos em relação ao centro. Eleva-se ao quadrado para evitar que desvios positivos e negativos se anulem e para penalizar erros grandes."},
                    {"simbolo": r"$s^2 = \frac{1}{n-1}\sum (x_i - \bar{x})^2$", "leitura": "variância amostral (com Bessel)", "significado": "A famosa <b>Correção de Bessel</b>: divide por $n-1$ para corrigir o viés intrínseco de estimar a variância a partir de uma amostra finita."},
                    {"simbolo": r"$\sigma = \sqrt{\sigma^2}$", "leitura": "desvio padrão", "significado": "Raiz quadrada da variância. Traz a unidade de medida de volta à mesma escala original dos dados (ex.: metros em vez de metros quadrados)."},
                ],
            },
            {
                "tipo": "pense",
                "titulo": "Por que dividir por n - 1 e não por n?",
                "pergunta": r"""Por que a fórmula da variância de uma amostra divide pelo total menos um ($n-1$) e não pelo tamanho total da amostra ($n$)?""",
                "resposta": r"""<p>Quando calculamos a média amostral $\bar{x}$ a partir de nossos dados, essa média calculada já está, por definição matemática, no ponto que <b>minimiza a soma dos quadrados das distâncias</b> daqueles dados específicos!</p>
<p>Isso significa que a distância dos dados até a média amostral $\bar{x}$ é sempre sistematicamente <i>menor</i> do que a distância real até a verdadeira média populacional $\mu$ (que nós não conhecemos). Portanto, dividir por $n$ geraria uma estimativa <b>viesada para baixo (otimista demais)</b>.</p>
<p>Dividir por $n-1$ infla ligeiramente o resultado final, compensando exatamente o grau de liberdade perdido ao fixar a média amostral, produzindo um estimador matematicamente não-viesado!</p>"""
            },
            {
                "tipo": "ponte",
                "titulo": "Onde isso vive na IA: Layer Normalization (LayerNorm)",
                "corpo": r"""<p>Todo bloco Transformer (GPT, Claude, LLaMA) aplica a <b>LayerNorm</b> nas ativações de cada token antes dos blocos de atenção e feed-forward:</p>
$$\mu = \frac{1}{d} \sum_{i=1}^d x_i, \quad \sigma = \sqrt{\frac{1}{d}\sum_{i=1}^d (x_i - \mu)^2 + \epsilon}, \quad \hat{x}_i = \frac{x_i - \mu}{\sigma} \cdot \gamma + \beta$$
<p>Isso força o vetor de ativação de cada token a ter rigorosamente <b>média 0 e desvio padrão 1</b>. Sem essa normalização contínua de média e desvio padrão, as ativações em redes de 96 camadas explodiriam ou colapsariam numericamente!</p>""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: O Impacto dos Outliers e a LayerNorm",
                "codigo": r'''import numpy as np

# 1. Demonstração da fragilidade da média com Outlier
salarios = np.array([2500, 3200, 2800, 4100, 3000, 2900, 3500])
print(f"Salários normais: {salarios}")
print(f"Média  : R$ {np.mean(salarios):,.2f}")
print(f"Mediana: R$ {np.median(salarios):,.2f}")

# Entra Bill Gates no restaurante:
salarios_com_bilionario = np.append(salarios, 100_000_000)
print(f"\nApós entrada de 1 bilionário:")
print(f"Nova Média  : R$ {np.mean(salarios_com_bilionario):,.2f} (Distorcida!)")
print(f"Nova Mediana: R$ {np.median(salarios_com_bilionario):,.2f} (Robusta!)")

# 2. Implementando LayerNorm de um vetor de ativação de IA
x_token = np.array([12.5, -4.2, 0.8, 8.4, -2.1])
media = np.mean(x_token)
desvio = np.std(x_token) # ddof=0 padrão da engenharia
x_norm = (x_token - media) / (desvio + 1e-5)

print(f"\nVetor de ativação original: {x_token}")
print(f"Vetor normalizado (LayerNorm): {x_norm.round(3)}")
print(f"Média pós-norm : {np.mean(x_norm):.6f} (efetivamente 0.0)")
print(f"Desvio pós-norm: {np.std(x_norm):.6f} (efetivamente 1.0)")''',
                "experimentos": [
                    "Compare <code>np.var(salarios, ddof=0)</code> (divisão por n) com <code>np.var(salarios, ddof=1)</code> (divisão por n-1 de Bessel). Note a pequena correção na amostra de tamanho 7.",
                    "Altere os valores do vetor <code>x_token</code> multiplicando tudo por 1.000. Veja como a LayerNorm neutraliza totalmente essa escala, produzindo a mesma saída normalizada."
                ]
            }
        ],
        "resumo": [
            "A média é o centro de gravidade (sensível a extremos) e a mediana é o ponto divisório de 50% (resistente a ruído).",
            "A variância quantifica a dispersão quadrática em torno da média, corrigida por $n-1$ em amostras finitas.",
            "A Layer Normalization de LLMs padroniza média zero e desvio unitário em cada camada para estabilizar o aprendizado."
        ],
        "proxima": r"Agora que sabemos medir a dispersão de uma variável, como medimos se duas variáveis andam juntas ou em direções opostas? Entram a Covariância e a Correlação.",
        "referencias": [
            {"obra": "Downey, A. Think Stats", "trecho": "Capítulo 2: Descriptive Statistics", "uso": "Análise da sensibilidade da média a caudas pesadas e outliers"},
            {"obra": "Ba, Kiros & Hinton (2016). Layer Normalization", "trecho": "Paper original", "uso": "Aplicação prática de média e desvio padrão em tensores de redes profundas"}
        ]
    },

    # =========================================================================
    # TÓPICO 23: Esperança matemática, covariância e correlação
    # =========================================================================
    "Esperança matemática, covariância e correlação": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Se um jogo de apostas cobra R$ 10 de entrada e paga R$ 1.000 com probabilidade de 1%, vale a pena jogar a longo prazo? E quando analisamos avaliações da nossa cafeteria, como saber se <i>tempo de espera</i> e <i>nota de satisfação</i> têm uma relação real ou se variam de forma independente? A resposta está na <b>Esperança Matemática ($\mathbb{E}$)</b> e na <b>Correlação de Pearson</b>.""",
        "prerequisitos": [
            "Variáveis aleatórias e média (Tópicos 21 e 22)",
            "Produto escalar e cosseno de vetores (Tópicos 3 e 5)"
        ],
        "objetivos": [
            "compreender a Esperança Matemática ($\mathbb{E}[X]$) como o retorno médio ponderado no longo prazo;",
            "entender a Covariância como o produto cruzado de desvios simultâneos;",
            "dominar a Correlação de Pearson $\rho \in [-1, 1]$ e sua profunda equivalência geométrica com a Similaridade de Cosseno."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "O Retorno Ponderado",
                "titulo": "O que é Esperança Matemática?",
                "corpo": r"""<p>A <b>Esperança Matemática $\mathbb{E}[X]$</b> (também chamada de valor esperado) é a média ponderada de todos os valores possíveis que uma variável aleatória pode assumir, onde os pesos são suas respectivas probabilidades:</p>
$$\mathbb{E}[X] = \sum_{i=1}^k x_i \cdot P(X = x_i)$$
<p>No caso do jogo que cobra R$ 10:</p>
$$\mathbb{E}[\text{Lucro}] = (1000 - 10) \times 0.01 + (-10) \times 0.99 = 9.90 - 9.90 = 0.00$$
<p>O retorno esperado é zero: no longo prazo de milhares de partidas, nem o jogador nem a banca lucram. Em IA, a função de perda total que minimizamos é rigorosamente a <b>esperança matemática do erro</b> sobre a distribuição de dados: $\min_w \mathbb{E}_{(x, y) \sim \mathcal{D}} [L(f(x; w), y)]$!</p>""",
            },
            {
                "tipo": "texto",
                "rotulo": "Caminhando Juntas",
                "titulo": "Covariância e Correlação de Pearson",
                "corpo": r"""<p>Para medir se duas variáveis $X$ e $Y$ co-variam (aumentam ou diminuem juntas), usamos a <b>Covariância</b>:</p>
$$\text{Cov}(X, Y) = \mathbb{E}[(X - \mathbb{E}[X])(Y - \mathbb{E}[Y])] = \frac{1}{n-1}\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})$$
<ul>
<li>Se quando $x$ está acima da média, $y$ também tende a estar acima da média, o produto é $(+) \times (+) = (+)$. Covariância positiva!</li>
<li>Se quando $x$ sobe, $y$ desce, o produto é $(+) \times (-) = (-)$. Covariância negativa!</li>
<li>Se não houver padrão, produtos positivos e negativos se cancelam para aproximadamente zero.</li>
</ul>
<p>O problema da covariância é que seu valor numérico depende da unidade (ex.: se medir em centímetros em vez de metros, o número multiplica por 100). Para torná-la universal, dividimos pelos desvios padrões, obtendo o <b>Coeficiente de Correlação de Pearson ($\rho$)</b>:</p>
$$\rho_{X, Y} = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y} \in [-1, +1]$$""",
            },
            {
                "tipo": "notacao",
                "titulo": "A Conexão Sagrada: Pearson é Cosseno!",
                "corpo": r"""<p>Lembra da fórmula da Similaridade de Cosseno do Módulo 1 (Tópico 5)? Veja esta revelação matemática profunda:</p>
$$\cos(\theta) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$$
<p>Se você pegar duas listas de dados $X$ e $Y$, subtrair a média de cada uma para centrá-las em zero ($\mathbf{u} = X - \bar{X}$ e $\mathbf{v} = Y - \bar{Y}$), o coeficiente de Pearson é <b>exatamente o cosseno do ângulo entre os dois vetores de dados</b>!</p>""",
                "itens": [
                    {"simbolo": r"$\rho = +1$", "leitura": "correlação linear positiva perfeita", "significado": "Cosseno = 1 ($\theta = 0^\circ$). Os dois vetores apontam exatamente na mesma direção semântica."},
                    {"simbolo": r"$\rho = 0$", "leitura": "correlação linear nula", "significado": "Cosseno = 0 ($\theta = 90^\circ$). Os dois vetores de dados são estritamente <b>ortogonais</b> (não compartilham informação linear)."},
                    {"simbolo": r"$\rho = -1$", "leitura": "correlação linear negativa perfeita", "significado": "Cosseno = -1 ($\theta = 180^\circ$). Um vetor aponta exatamente no sentido oposto do outro."},
                ],
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Calculando a Matriz de Covariância e Pearson",
                "codigo": r'''import numpy as np

# Dados da Cafeteria: 5 clientes
# X = tempo de espera em minutos
# Y = nota de avaliação de satisfação (1 a 5)
tempo_espera = np.array([2.0, 5.0, 8.0, 12.0, 15.0])
nota_cliente = np.array([5.0, 4.0, 3.0,  2.0,  1.0])

# 1. Centrando os dados (subtraindo a média)
u = tempo_espera - np.mean(tempo_espera)
v = nota_cliente - np.mean(nota_cliente)

# 2. Covariância manual
cov_manual = np.sum(u * v) / (len(tempo_espera) - 1)

# 3. Correlação de Pearson manual
rho_manual = cov_manual / (np.std(tempo_espera, ddof=1) * np.std(nota_cliente, ddof=1))

# 4. Cosseno geométrico dos vetores centrados
cos_vetores = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

print(f"Covariância manual: {cov_manual:.4f} (negativa: mais espera = menor nota)")
print(f"Pearson manual    : {rho_manual:.4f}")
print(f"Cosseno geométrico: {cos_vetores:.4f}")
print(f"NumPy corrcoef    : {np.corrcoef(tempo_espera, nota_cliente)[0, 1]:.4f}")

assert np.isclose(rho_manual, cos_vetores), "Pearson deve ser rigorosamente igual ao Cosseno!"
print("Identidade comprovada com sucesso!")''',
                "experimentos": [
                    "Experimente mudar a nota para uma relação não linear, como $Y = X^2$ com $X \in [-5, 5]$. Observe como o Pearson pode dar 0.0 mesmo havendo uma dependência perfeita (pois Pearson mede apenas alinhamento linear!).",
                    "Gere uma matriz de covariância de dados de alta dimensão com <code>np.cov</code> e observe como ela é a base do PCA (Análise de Componentes Principais)."
                ]
            }
        ],
        "resumo": [
            "Esperança matemática é a média ponderada por probabilidades que guia o cálculo do risco e da perda esperada.",
            "Covariância indica o sentido conjunto da variação e a Correlação de Pearson padroniza esse valor entre -1 e +1.",
            "A Correlação de Pearson é rigorosamente idêntica ao cosseno do ângulo entre vetores de dados centrados na média."
        ],
        "proxima": r"Com a base da incerteza pronta, vamos entender o motor supremo da inferência: o Teorema de Bayes e a Probabilidade Condicional.",
        "referencias": [
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Capítulo 6.4 e 6.5: Summary Statistics and Independence", "uso": "Formalização de esperança matemática e operadores de covariância"},
            {"obra": "Downey, A. Think Stats", "trecho": "Capítulo 7: Relationships between Variables", "uso": "Interpretação prática da correlação de Pearson e limitações com dados não lineares"}
        ]
    },

    # =========================================================================
    # TÓPICO 24: Probabilidade condicional e Teorema de Bayes
    # =========================================================================
    "Probabilidade condicional e Teorema de Bayes": LESSONS_V2_SAMPLES["Probabilidade condicional e Teorema de Bayes"],

    # =========================================================================
    # TÓPICO 25: Distribuição Normal (Gaussiana) e probabilidade vs verossimilhança
    # =========================================================================
    "Distribuição Normal (Gaussiana) e probabilidade vs verossimilhança": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Por que alturas humanas, notas de exames nacionais e o ruído térmico em processadores assumem exatamente a mesma curva em forma de sino? E quando ajustamos uma IA aos dados, qual é a sutil, mas profunda, diferença entre <b>Probabilidade</b> (dados variam, parâmetros fixos) e <b>Verossimilhança / Likelihood</b> (dados fixos, parâmetros variam)?""",
        "prerequisitos": [
            "Função densidade de probabilidade PDF (Tópico 21)",
            "Média e desvio padrão (Tópico 22)"
        ],
        "objetivos": [
            "compreender a anatomia matemática da equação da Distribuição Normal $\mathcal{N}(\mu, \sigma^2)$;",
            "dominar a Regra Empírica 68-95-99.7 dos desvios padrão;",
            "distinguir categoricamente Probabilidade de Verossimilhança (Likelihood), o pilar da calibração de modelos."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Curva Soberana",
                "titulo": "A Anatomia da Equação Gaussiana",
                "corpo": r"""<p>Carl Friedrich Gauss deduziu a distribuição que hoje leva seu nome investigando os erros cometidos por astrônomos ao apontar telescópios para planetas. Sua fórmula matemática é:</p>
$$p(x; \mu, \sigma) = \frac{1}{\sigma \sqrt{2\pi}} \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)$$
<p>Observe a beleza simétrica dessa equação:</p>
<ul>
<li>$(x - \mu)^2$: A distância ao quadrado do ponto $x$ até o centro $\mu$. Como é ao quadrado, estar 2 unidades à direita ou à esquerda produz rigorosamente o mesmo valor (simetria perfeita).</li>
<li>$\exp(-\dots)$: O expoente negativo faz o valor decair vertiginosamente quanto mais nos afastamos do centro, gerando as caudas suaves da curva.</li>
<li>$\frac{1}{\sigma \sqrt{2\pi}}$: A constante normalizadora que garante que a área total sob a curva seja rigorosamente igual a $1.0$ (100% de probabilidade).</li>
</ul>""",
            },
            {
                "tipo": "visual",
                "titulo": "A Regra Sagrada: 68 - 95 - 99.7",
                "corpo": r"""<p>Em qualquer distribuição normal perfeita no universo, não importa se $\mu=0$ ou $\mu=1.000.000$, a proporção de dados contida nos desvios padrão é universal:</p>""",
                "svg": SVG_NORMAL_GAUSS,
                "legenda": "68.2% dos dados caem dentro de ±1σ, 95.4% dentro de ±2σ e 99.7% dentro de ±3σ da média.",
            },
            {
                "tipo": "notacao",
                "titulo": "Probabilidade vs. Verossimilhança (Likelihood)",
                "corpo": r"""<p>Essa é a distinção conceitual mais importante de toda a inferência estatística moderna:</p>""",
                "itens": [
                    {"simbolo": r"$\text{Probabilidade}: P(\text{Dados} \mid \theta)$", "leitura": "probabilidade dos dados dado o parâmetro theta", "significado": "Os parâmetros do modelo $\theta = (\mu, \sigma)$ são <b>conhecidos e fixos</b>. Calculamos a chance de novos dados futuros caírem em certa faixa."},
                    {"simbolo": r"$\text{Verossimilhança}: L(\theta \mid \text{Dados})$", "leitura": "verossimilhança de theta dados os dados coletados", "significado": "Os dados já foram coletados no mundo real e são <b>fixos e imutáveis</b>. Variamos os parâmetros $\theta$ para descobrir quais parâmetros tornam os dados observados o mais plausíveis possível!"},
                ],
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Calculando a Likelihood de uma Amostra",
                "codigo": r'''import numpy as np

# Função de densidade da Gaussiana
def pdf_normal(x, mu, sigma):
    constante = 1.0 / (sigma * np.sqrt(2.0 * np.pi))
    expoente = -0.5 * ((x - mu) / sigma) ** 2
    return constante * np.exp(expoente)

# Dados coletados da cafeteria: tempo de atendimento de 3 clientes (em minutos)
dados_reais = np.array([4.8, 5.2, 5.0])

# Hipótese 1: Modelo A com mu = 5.0, sigma = 1.0
densidades_A = pdf_normal(dados_reais, mu=5.0, sigma=1.0)
likelihood_A = np.prod(densidades_A)

# Hipótese 2: Modelo B com mu = 10.0, sigma = 1.0 (parâmetro ruim!)
densidades_B = pdf_normal(dados_reais, mu=10.0, sigma=1.0)
likelihood_B = np.prod(densidades_B)

print(f"Dados observados: {dados_reais}")
print(f"Likelihood do Modelo A (mu=5.0) : {likelihood_A:.6f}")
print(f"Likelihood do Modelo B (mu=10.0): {likelihood_B:.2e}")
print(f"O Modelo A é {likelihood_A / (likelihood_B + 1e-15):,.0f}x mais verossímil que o Modelo B!")''',
                "experimentos": [
                    "Varie o parâmetro $\mu$ de 3.0 até 7.0 em passos de 0.1 e plote a curva de Likelihood. Veja como ela atinge o pico exatamente na média dos dados ($5.0$).",
                    "Entenda por que multiplicamos as densidades: sob a premissa de dados independentes (i.i.d.), a probabilidade conjunta é o produto das densidades individuais."
                ]
            }
        ],
        "resumo": [
            "A curva Gaussiana descreve fenômenos naturais agregados com simetria perfeita em torno da média $\mu$.",
            "A regra 68-95-99.7 oferece limites rápidos para detecção de anomalias e intervalos empíricos.",
            "Probabilidade projeta dados a partir de parâmetros fixos; Verossimilhança (Likelihood) busca os melhores parâmetros para dados observados fixos."
        ],
        "proxima": r"Por que a curva normal surge com tanta frequência na natureza e no aprendizado de máquina? A resposta está no Teorema do Limite Central.",
        "referencias": [
            {"obra": "Goodfellow, Bengio & Courville. Deep Learning", "trecho": "Capítulo 3.9: Common Probability Distributions", "uso": "Propriedades da distribuição Gaussiana e máxima entropia para variância fixa"},
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Capítulo 6.5: Gaussian Distribution", "uso": "Manipulação analítica de variáveis aleatórias Gaussianas multivariadas"}
        ]
    },

    # =========================================================================
    # TÓPICO 26: Teorema do Limite Central e amostragem
    # =========================================================================
    "Teorema do Limite Central e amostragem": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Role um dado de 6 faces: a probabilidade de cada face é 1/6 (um gráfico reto, plano e nada parecido com um sino). Agora jogue 50 dados e calcule a média das faces. Repita isso 1.000 vezes. Como por encanto, a média das médias se organiza em uma curva Gaussiana perfeita! Por que o <b>Teorema do Limite Central</b> é considerado a espinha dorsal de toda a inferência estatística e do Mini-batch GD?""",
        "prerequisitos": [
            "Variáveis aleatórias e média (Tópicos 21 e 22)",
            "Distribuição Normal (Tópico 25)"
        ],
        "objetivos": [
            "compreender o enunciado do Teorema do Limite Central (TLC);",
            "dominar a fórmula do Erro Padrão da Média ($\text{SE} = \frac{\sigma}{\sqrt{n}}$);",
            "entender por que o Mini-batch SGD converge para o gradiente real graças ao TLC."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Mágica da Soma de Variáveis",
                "titulo": "O Enunciado Universal do TLC",
                "corpo": r"""<p>O <b>Teorema do Limite Central (TLC)</b> afirma que se você coletar amostras aleatórias independentes de tamanho $n$ de <b>qualquer distribuição de probabilidade</b> (não importa quão esquisita, assimétrica ou pontiaguda ela seja, desde que tenha média $\mu$ e variância finita $\sigma^2$):</p>
<p>A distribuição das <b>médias amostrais $\bar{X}_n$</b> se aproximará cada vez mais de uma <b>Distribuição Normal</b> conforme $n$ cresce:</p>
$$\bar{X}_n \sim \mathcal{N}\left(\mu, \frac{\sigma^2}{n}\right)$$
<p>Veja que a variância da média é dividida por $n$! Conforme o tamanho da amostra aumenta, a incerteza da média encolhe na proporção de $\frac{1}{\sqrt{n}}$.</p>""",
            },
            {
                "tipo": "notacao",
                "titulo": "Erro Padrão da Média (Standard Error)",
                "corpo": r"""<p>Não confunda Desvio Padrão com Erro Padrão:</p>""",
                "itens": [
                    {"simbolo": r"$\sigma$ (Desvio Padrão)", "leitura": "sigma", "significado": "Mede a dispersão individual e natural entre os indivíduos da população (não diminui se você coletar mais dados)."},
                    {"simbolo": r"$\text{SE} = \frac{\sigma}{\sqrt{n}}$ (Erro Padrão)", "leitura": "erro padrão da média", "significado": "Mede a incerteza estatística sobre a nossa estimativa da média. Diminui na taxa de $\sqrt{n}$ conforme aumentamos a amostra!"},
                ],
            },
            {
                "tipo": "ponte",
                "titulo": "Por que o Mini-batch GD funciona na prática?",
                "corpo": r"""<p>No treinamento de redes neurais, calcular o gradiente exato exigiria processar bilhões de exemplos de treino a cada passo. Em vez disso, sorteamos um mini-batch de tamanho $n = 128$ ou $n = 512$.</p>
<p>Pelo Teorema do Limite Central, o gradiente médio desse lote:</p>
$$\mathbf{g}_{\text{batch}} = \frac{1}{n} \sum_{i=1}^n \nabla L_i$$
<p>É uma variável aleatória normalmente distribuída centrada exatamente no <b>verdadeiro gradiente populacional</b>, com o ruído diminuindo com $\frac{1}{\sqrt{n}}$! É por isso que podemos confiar cegamente nos passos de uma GPU sem processar todo o dataset a cada iteração.</p>""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: O Milagre da Emergência Gaussiana",
                "codigo": r'''import numpy as np

# População altamente bizarra e uniforme (nada normal!): números entre 0 e 10
np.random.seed(42)
num_experimentos = 2000
tamanho_amostra = 40

medias_amostrais = []
for _ in range(num_experimentos):
    # Sorteia 40 números de uma distribuição uniforme
    amostra = np.random.uniform(0.0, 10.0, size=tamanho_amostra)
    medias_amostrais.append(np.mean(amostra))

medias_amostrais = np.array(medias_amostrais)

print("Distribuição original: Uniforme em [0, 10] (média teórica = 5.0)")
print(f"Média das 2.000 médias amostrais : {np.mean(medias_amostrais):.4f}")
print(f"Desvio padrão observado das médias: {np.std(medias_amostrais):.4f}")

# Erro padrão teórico: sigma / sqrt(n) = (10 / sqrt(12)) / sqrt(40) = 2.8867 / 6.3245 ≈ 0.4564
se_teorico = (10.0 / np.sqrt(12)) / np.sqrt(tamanho_amostra)
print(f"Erro Padrão Teórico (SE)          : {se_teorico:.4f}")
assert abs(np.std(medias_amostrais) - se_teorico) < 0.03, "O TLC comprovou a convergência!"''',
                "experimentos": [
                    "Aumente <code>tamanho_amostra = 200</code> e observe o erro padrão encolher para menos de metade do valor.",
                    "Substitua a distribuição uniforme por uma exponencial com <code>np.random.exponential(scale=2.0)</code> e veja o TLC continuar produzindo uma normal simétrica para as médias."
                ]
            }
        ],
        "resumo": [
            "O Teorema do Limite Central garante que médias de amostras independentes convergem para a distribuição normal.",
            "O erro da média cai com a raiz quadrada da amostra ($\text{SE} = \sigma / \sqrt{n}$).",
            "O gradiente estimado de mini-batches em IA herda a estabilidade do TLC para permitir otimização rápida e confiável."
        ],
        "proxima": r"Com o erro padrão em mãos, como saber se a diferença de performance entre dois modelos de IA é real ou mera sorte? Vamos estudar Intervalos de Confiança e Testes de Hipótese.",
        "referencias": [
            {"obra": "Downey, A. Think Stats", "trecho": "Capítulo 9: Hypothesis Testing and Sampling Distributions", "uso": "Simulação computacional de distribuições amostrais"},
            {"obra": "Stewart, J. Calculus", "trecho": "Apêndice de Probabilidade: Central Limit Theorem", "uso": "Prova do comportamento assintótico de somas de variáveis aleatórias"}
        ]
    },

    # =========================================================================
    # TÓPICO 27: Intervalos de confiança e teste de hipóteses (noção)
    # =========================================================================
    "Intervalos de confiança e teste de hipóteses (noção)": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Você treinou uma nova versão do seu modelo de NLP e avaliou em 100 perguntas: a acurácia saltou de 75% para 79%. Esse ganho de 4% é uma <b>melhoria real da inteligência</b> ou foi mera sorte estatística de uma amostra pequena? Como os <b>Intervalos de Confiança</b> e o <b>p-valor</b> impedem cientistas de dados de comemorar ilusões estatísticas?""",
        "prerequisitos": [
            "Teorema do Limite Central e Erro Padrão (Tópico 26)",
            "Distribuição Normal (Tópico 25)"
        ],
        "objetivos": [
            "construir intervalos de confiança de 95% usando o multiplicador crítico $1.96$;",
            "formular testes de hipótese ($H_0$ nula vs $H_1$ alternativa);",
            "interpretar corretamente o $p$-valor sem cometer a falácia da probabilidade reversa."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "Margem de Incerteza",
                "titulo": "O Intervalo de Confiança de 95%",
                "corpo": r"""<p>Na ciência do mundo real, estimativas pontuais isoladas (ex.: <i>“a acurácia é 79%”</i>) são incompletas porque toda amostra finita carrega incerteza. O <b>Intervalo de Confiança (IC)</b> expressa essa margem de tolerância:</p>
$$IC_{95\%} = \left[ \bar{x} - 1.96 \cdot \text{SE}, \quad \bar{x} + 1.96 \cdot \text{SE} \right]$$
<p>O número mágico $1.96$ vem da curva Gaussiana: exatamente 95% da área sob a normal padrão está entre $-1.96$ e $+1.96$ desvios padrão da média!</p>
<p><b>Significado correto:</b> Se repetíssemos esse experimento 100 vezes coletando novas amostras, em 95 delas o intervalo construído conteria o verdadeiro valor real da população.</p>""",
            },
            {
                "tipo": "texto",
                "rotulo": "O Julgamento Estatístico",
                "titulo": "Hipótese Nula ($H_0$) e o p-valor",
                "corpo": r"""<p>Um <b>teste de hipótese</b> funciona como um tribunal criminal com a premissa de presunção de inocência:</p>
<ul>
<li><b>Hipótese Nula ($H_0$):</b> O modelo novo <i>não tem nenhuma vantagem real</i> em relação ao antigo. A diferença de 4% foi mero ruído de sorte.</li>
<li><b>Hipótese Alternativa ($H_1$):</b> O modelo novo é genuinamente superior.</li>
<li><b>p-valor:</b> A probabilidade de obter uma diferença de 4% (ou maior) <b>supondo que a hipótese nula fosse estritamente verdadeira</b>.</li>
</ul>
<p>Se o $p$-valor for muito pequeno (por convenção, $p < 0.05$ ou $5\%$), o tribunal conclui: <i>“Seria improvável demais esse resultado ter acontecido por pura sorte; portanto, rejeitamos $H_0$ e declaramos a melhoria estatisticamente significativa!”</i></p>""",
            },
            {
                "tipo": "armadilhas",
                "titulo": "A Falácia Universal do p-valor",
                "itens": [
                    {"erro": "Achar que p = 0.03 significa que há 97% de chance de o modelo ser melhor.", "correcao": "O p-valor NÃO é $P(H_1 \mid \text{Dados})$. O p-valor é $P(\text{Dados extremos} \mid H_0)$. Ele mede quão bizarros seriam os dados se não houvesse efeito nenhum."},
                    {"erro": "Confundir significância estatística com significância prática.", "correcao": "Com 10 milhões de dados, um ganho minúsculo de 0.001% pode ter $p < 0.0001$, mas na prática não traz nenhum benefício perceptível ao usuário."}
                ]
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Teste A/B de Modelos de Linguagem",
                "codigo": r'''import numpy as np

# Avaliação de 100 perguntas: Modelo A acertou 75, Modelo B acertou 79
n = 100
pA = 0.75
pB = 0.79

diff = pB - pA  # +0.04 (4% de ganho aparente)

# Erro padrão da diferença de duas proporções
se_diff = np.sqrt((pA*(1-pA)/n) + (pB*(1-pB)/n))
z_score = diff / se_diff

print(f"Diferença observada : +{diff*100:.1f}%")
print(f"Erro Padrão da dif  : {se_diff*100:.2f}%")
print(f"Escore Z            : {z_score:.2f}")

# Intervalo de 95% para a diferença
ic_inferior = diff - 1.96 * se_diff
ic_superior = diff + 1.96 * se_diff
print(f"Intervalo de 95%    : [{ic_inferior*100:.1f}%, {ic_superior*100:.1f}%]")

if ic_inferior < 0:
    print("Conclusão: O intervalo CONTÉM ZERO! Não há evidência estatística sólida de que o modelo B seja superior (pode ter sido sorte na amostra de 100 testes).")
else:
    print("Conclusão: O modelo B é estatisticamente superior!")''',
                "experimentos": [
                    "Aumente o teste para <code>n = 2000</code> perguntas mantendo as mesmas taxas de 75% e 79%. Observe como o erro padrão despenca e a diferença passa a ser altamente significativa.",
                    "Entenda por que benchmarks sérios de IA (como MMLU e LMSYS Chatbot Arena) avaliam milhares de prompts antes de declarar um modelo campeão."
                ]
            }
        ],
        "resumo": [
            "Intervalos de confiança contextualizam a margem de erro inerente a amostras estatísticas finitas.",
            "O p-valor mede a compatibilidade dos dados com a hipótese nula de ausência de efeito.",
            "Significância estatística depende fundamentalmente do tamanho da amostra testada."
        ],
        "proxima": r"Agora que compreendemos como quantificar a probabilidade dos dados, como escolher os parâmetros ótimos de uma rede neural? Conheça a Máxima Verossimilhança (MLE).",
        "referencias": [
            {"obra": "Downey, A. Think Stats", "trecho": "Capítulo 9: Testing Hypotheses", "uso": "Metodologia de testes de hipótese por permutação e métodos analíticos"},
            {"obra": "Wasserman, L. All of Statistics", "trecho": "Capítulo 10: Hypothesis Testing and p-values", "uso": "Fundamentação teórica de testes z e limites de confiança"}
        ]
    },

    # =========================================================================
    # TÓPICO 28: Máxima Verossimilhança (Maximum Likelihood Estimation - MLE)
    # =========================================================================
    "Máxima Verossimilhança (Maximum Likelihood Estimation - MLE)": {
        "v": 2,
        "duracao": 35,
        "gancho": r"""Como um modelo de inteligência artificial define o que são 'pesos perfeitos'? A resposta é um dos princípios mais brilhantes de toda a história da Estatística: a <b>Máxima Verossimilhança (MLE)</b>. Por que minimizar a função de perda de <b>Cross-Entropy</b> em redes neurais e LLMs é rigorosamente idêntico a maximizar a probabilidade de o modelo gerar o mundo real?""",
        "prerequisitos": [
            "Funções de verossimilhança (Tópico 25)",
            "Logaritmo natural $\ln(x)$ e derivadas (Tópicos 12 e 13)"
        ],
        "objetivos": [
            "compreender o princípio da Máxima Verossimilhança (MLE);",
            "dominar o truque do Log-Likelihood para contornar o underflow numérico de probabilidades;",
            "provar analiticamente que minimizar a Negative Log-Likelihood (NLL) equivale à Cross-Entropy Loss dos LLMs."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "O Princípio Fundamental",
                "titulo": "O que é Máxima Verossimilhança?",
                "corpo": r"""<p>Imagine que você tem uma moeda viciada e joga 10 vezes, obtendo 8 Caras e 2 Coroas. Qual é a probabilidade $p$ de dar Cara dessa moeda?</p>
<p>Intuitivamente você diria $p = 80\% = 0.8$. A Máxima Verossimilhança (MLE) é a formalização matemática desse raciocínio: <b>escolha os parâmetros $\theta$ que tornam os dados observados o mais prováveis de terem ocorrido</b>:</p>
$$\theta_{\text{MLE}} = \arg\max_\theta \prod_{i=1}^n P(x_i \mid \theta)$$
<p>Se as amostras são independentes, a probabilidade conjunta de observar todo o conjunto de dados é o produtório ($\prod$) de todas as probabilidades individuais.</p>""",
            },
            {
                "tipo": "passos",
                "titulo": "O Truque do Logaritmo (Log-Likelihood)",
                "corpo": r"""<p>Por que nunca maximizamos o produto de probabilidades diretamente em um computador?</p>""",
                "passos": [
                    {
                        "faca": r"Identifique o perigo do Underflow Numérico: Se multiplicarmos 1.000 probabilidades típicas como $0.05 \times 0.02 \times \dots$, o resultado é da ordem de $10^{-500}$.",
                        "porque": "Processadores de 64 bits não conseguem representar números menores que $\approx 10^{-308}$ e arredondam tudo para zero absoluto (`underflow`)."
                    },
                    {
                        "faca": r"Aplique o logaritmo natural $\ln$ em ambos os lados: $$\ln \left( \prod_{i=1}^n P(x_i \mid \theta) \right) = \sum_{i=1}^n \ln P(x_i \mid \theta)$$",
                        "porque": "Pela propriedade sagrada dos logaritmos, o logaritmo de um produto vira a <b>soma dos logaritmos</b>!"
                    },
                    {
                        "faca": r"Multiplique por $-1$ para transformar em função de perda: $$\text{NLL}(\theta) = -\sum_{i=1}^n \ln P(x_i \mid \theta)$$",
                        "porque": "Algoritmos de otimização (como Adam e SGD) são projetados para <b>minimizar perdas</b>. Minimizar a <i>Negative Log-Likelihood</i> (NLL) é exatamente o mesmo que maximizar a verossimilhança!"
                    }
                ],
                "conclusao": r"Em classificação e em LLMs, a perda média $\frac{1}{n} \text{NLL}$ é a famosa <b>Cross-Entropy Loss</b>! Quando treinamos o ChatGPT, estamos simplesmente aplicando MLE para maximizar a probabilidade de ele acertar o próximo token."
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Estimando a Moeda Viciada por MLE",
                "codigo": r'''import numpy as np

# 10 lançamentos: 8 sucessos (1) e 2 fracassos (0)
dados = np.array([1, 1, 1, 0, 1, 1, 0, 1, 1, 1])
k = np.sum(dados) # 8
n = len(dados)    # 10

# Função de Negative Log-Likelihood para uma Bernoulli
def nll_bernoulli(p, k, n):
    p = np.clip(p, 1e-12, 1.0 - 1e-12)
    return -(k * np.log(p) + (n - k) * np.log(1.0 - p))

# Testando vários candidatos a probabilidade p de 0.1 a 0.99
candidatos_p = np.linspace(0.1, 0.99, 100)
perdas = [nll_bernoulli(p, k, n) for p in candidatos_p]

p_otimo = candidatos_p[np.argmin(perdas)]
print(f"Sucessos observados: {k} em {n} tentativas")
print(f"Parâmetro analítico k/n       : {k/n:.4f}")
print(f"Parâmetro ótimo encontrado MLE: {p_otimo:.4f}")
assert abs(p_otimo - 0.8) < 0.02, "MLE deveria convergir para 0.8!"''',
                "experimentos": [
                    "Verifique que o ponto onde a perda NLL é mínima corresponde ao ponto onde a derivada $-\frac{k}{p} + \frac{n-k}{1-p} = 0$, cuja solução é $p = k/n$.",
                    "Entenda como a MLE justifica teoricamente por que a média amostral é a melhor estimativa sob a hipótese gaussiana."
                ]
            }
        ],
        "resumo": [
            "A Máxima Verossimilhança seleciona parâmetros que maximizam a chance de observar o dataset real.",
            "O truque do logaritmo transforma produtos instáveis em somas numericamente seguras.",
            "A minimização da Negative Log-Likelihood é a fundação matemática direta da Cross-Entropy usada em LLMs."
        ],
        "proxima": r"Com o critério de ajuste pronto, surge a grande pergunta: um modelo muito ajustado aos dados de treino é sempre melhor? Vamos desvendar o dilema Viés vs. Variância.",
        "referencias": [
            {"obra": "Goodfellow, Bengio & Courville. Deep Learning", "trecho": "Capítulo 5.5: Maximum Likelihood Estimation", "uso": "Dedução da equivalência entre MLE, divergência KL e entropia cruzada"},
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Capítulo 9.1: Maximum Likelihood Estimation", "uso": "Formulações analíticas para modelos lineares e gaussianos"}
        ]
    },

    # =========================================================================
    # TÓPICO 29: Trade-off Viés vs. Variância (Bias-Variance Dilemma)
    # =========================================================================
    "Trade-off Viés vs. Variância (Bias-Variance Dilemma)": {
        "v": 2,
        "duracao": 35,
        "gancho": r"""Um aluno estuda para o vestibular decorando todas as respostas das provas dos últimos 10 anos vírgula por vírgula. No dia da prova inédita, ele tira zero porque a pergunta mudou ligeiramente. Outro aluno estuda apenas um resumo de duas linhas e também tira nota baixa por ignorar os detalhes. Como a <b>decomposição matemática do erro</b> explica a fronteira entre <b>Underfitting</b> e <b>Overfitting</b>?""",
        "prerequisitos": [
            "Esperança matemática e variância (Tópicos 22 e 23)",
            "Descida do Gradiente e funções de perda (Tópicos 18 e 28)"
        ],
        "objetivos": [
            "deduzir a decomposição matemática do erro em $\text{Viés}^2 + \text{Variância} + \text{Ruído Irredutível}$;",
            "identificar os sintomas clássicos de Underfitting (alto viés) e Overfitting (alta variância);",
            "conhecer as armas modernas de regularização: Weight Decay, Dropout e Early Stopping."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Equação Mestra do Erro",
                "titulo": "A Decomposição Matemática do Erro Quadrático",
                "corpo": r"""<p>Suponha que os dados reais sejam gerados por $y = f(x) + \epsilon$, onde $\epsilon$ é um ruído gaussiano com média zero e variância $\sigma^2$. Ao treinarmos um modelo $\hat{f}(x)$, o erro quadrático esperado em dados inéditos se decompõe rigorosamente em três componentes:</p>
$$\mathbb{E}\left[ (y - \hat{f}(x))^2 \right] = \underbrace{\left( \mathbb{E}[\hat{f}(x)] - f(x) \right)^2}_{\text{Viés}^2\ (\text{Bias})} + \underbrace{\mathbb{E}\left[ (\hat{f}(x) - \mathbb{E}[\hat{f}(x)])^2 \right]}_{\text{Variância}\ (\text{Variance})} + \underbrace{\sigma^2}_{\text{Ruído Irredutível}}$$""",
            },
            {
                "tipo": "visual",
                "titulo": "O Cabo-de-Guerra da Complexidade",
                "corpo": r"""<p>Conforme aumentamos a capacidade do modelo (número de parâmetros e camadas), o comportamento do erro segue a clássica curva em U:</p>""",
                "svg": SVG_BIAS_VARIANCE,
                "legenda": "Modelos simples sofrem de alto viés (underfitting). Modelos complexos sofrem de alta variância (overfitting). O objetivo é encontrar o ponto de mínimo no erro de teste.",
            },
            {
                "tipo": "tabela",
                "titulo": "Sintomas e Remédios de Viés e Variância",
                "cabecalho": ["Dimensão", "O que significa?", "Sintoma no Treino/Validação", "Como corrigir?"],
                "linhas": [
                    ["Alto Viés (Underfitting)", "Modelo rígido demais; não consegue aprender a complexidade dos dados", "Erro de treino alto e erro de validação igualmente alto", "Aumentar tamanho do modelo, adicionar mais camadas, usar features mais ricas"],
                    ["Alta Variância (Overfitting)", "Modelo memorizou o ruído e particularidades específicas do treino", "Erro de treino quase zero, mas erro de validação alto (gap enorme)", "Mais dados de treino, Regularização L2 (Weight Decay), Dropout, Early Stopping"],
                    ["Ruído Irredutível ($\sigma^2$)", "Limitação física e ruído dos próprios sensores/dados", "Erro mínimo teórico inultrapassável (Bayes Error)", "Coletar sensores melhores ou dados com maior resolução"]
                ]
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Ajuste Polinomial e Overfitting Visível",
                "codigo": r'''import numpy as np

# Gerando dados reais de uma senoide com ruído
np.random.seed(42)
N = 15
X = np.sort(np.random.uniform(0, 1, size=N))
y_real = np.sin(2 * np.pi * X)
y = y_real + np.random.normal(0, 0.2, size=N)

# Ajustando 3 modelos polinomiais:
# Grau 1: Reta simples (Alto Viés / Underfitting)
# Grau 3: Cúbico equilibrado (Ponto Ideal)
# Grau 12: Polinômio de grau 12 (Alta Variância / Overfitting extremo)
p1 = np.poly1d(np.polyfit(X, y, deg=1))
p3 = np.poly1d(np.polyfit(X, y, deg=3))
p12 = np.poly1d(np.polyfit(X, y, deg=12))

# Erro no treino
mse1_treino = np.mean((p1(X) - y)**2)
mse3_treino = np.mean((p3(X) - y)**2)
mse12_treino = np.mean((p12(X) - y)**2)

# Erro em 100 pontos de teste inéditos
X_teste = np.linspace(0, 1, 100)
y_teste = np.sin(2 * np.pi * X_teste) + np.random.normal(0, 0.2, size=100)
mse1_teste = np.mean((p1(X_teste) - y_teste)**2)
mse3_teste = np.mean((p3(X_teste) - y_teste)**2)
mse12_teste = np.mean((p12(X_teste) - y_teste)**2)

print("Comparativo de Desempenho (Treino vs Teste):")
print(f"Grau 1  (Reta)      -> MSE Treino: {mse1_treino:.4f} | MSE Teste: {mse1_teste:.4f} (Underfitting)")
print(f"Grau 3  (Cúbico)    -> MSE Treino: {mse3_treino:.4f} | MSE Teste: {mse3_teste:.4f} (SWEET SPOT!)")
print(f"Grau 12 (Polinômio) -> MSE Treino: {mse12_treino:.4f} | MSE Teste: {mse12_teste:.4f} (OVERFITTING EXPLOSIVO!)")
assert mse12_teste > mse3_teste * 3, "O polinômio grau 12 deve falhar catastroficamente no teste!"''',
                "experimentos": [
                    "Observe como o polinômio de grau 12 tem erro de treino quase zero, mas seu erro no teste explode para ordens de grandeza maiores devido a oscilações extremas.",
                    "Adicione uma regularização Ridge (penalidade sobre os coeficientes ao quadrado) e veja como ela doma o modelo de grau 12."
                ]
            }
        ],
        "resumo": [
            "O erro total esperado é a soma de Viés ao quadrado, Variância do modelo e Ruído irredutível.",
            "Underfitting ocorre por falta de capacidade expressiva e Overfitting por memorização de ruído amostral.",
            "Técnicas de regularização como Weight Decay reduzem a variância ao custo de um aumento controlado de viés."
        ],
        "proxima": r"Completamos os fundamentos de Probabilidade e Estatística! No Módulo 4, estudaremos a Geometria Analítica e a Teoria da Informação de Shannon que balizam a função de perda das IAs generativas.",
        "referencias": [
            {"obra": "Bishop, C. Pattern Recognition and Machine Learning", "trecho": "Capítulo 3.2: The Bias-Variance Decomposition", "uso": "Dedução analítica clássica da decomposição do erro quadrático"},
            {"obra": "Goodfellow, Bengio & Courville. Deep Learning", "trecho": "Capítulo 5.4: Estimators, Bias and Variance", "uso": "Discussão moderna sobre trade-off de viés e capacidade em redes profundas"}
        ]
    }
}
