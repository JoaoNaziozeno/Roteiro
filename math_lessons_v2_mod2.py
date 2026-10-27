# -*- coding: utf-8 -*-
"""
Aulas Visuais de Matemática v2 — Módulo 2: Cálculo Diferencial & Otimização.
Baseado em James Stewart (Cálculo), Gilbert Strang (Calculus),
Deisenroth, Faisal & Ong (Mathematics for Machine Learning, Cap. 5 e 7) e
Goodfellow, Bengio & Courville (Deep Learning, Cap. 4, 6 e 8).
"""

from math_lessons_v2_samples import LESSONS_V2_SAMPLES

# SVG: Tangente e Secante aproximando o limite
SVG_SECANTE_TANGENTE = r'''<svg viewBox="0 0 520 260" class="lv2-svg" role="img" aria-label="Reta secante aproximando a tangente">
  <defs>
    <marker id="m2-arr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" class="sv-fillm"/>
    </marker>
  </defs>
  <!-- Eixos -->
  <line x1="40" y1="230" x2="480" y2="230" class="sv-ax" marker-end="url(#m2-arr)"/>
  <line x1="60" y1="245" x2="60" y2="25" class="sv-ax" marker-end="url(#m2-arr)"/>
  <text x="490" y="234" class="sv-tm">x</text>
  <text x="54" y="20" class="sv-tm">f(x)</text>

  <!-- Curva f(x) = x^2 / 400 + 40 -->
  <path d="M 70 215 Q 220 200 450 45" class="sv-a" style="stroke-width:2.8"/>
  <text x="440" y="35" class="sv-t" style="font-weight:700">f(x)</text>

  <!-- Pontos: P(x, f(x)) e Q(x+h, f(x+h)) -->
  <!-- Ponto P (x=160, y=190) -->
  <circle cx="160" cy="190" r="5" class="sv-fill"/>
  <line x1="160" y1="190" x2="160" y2="230" class="sv-thin sv-dash"/>
  <text x="156" y="246" class="sv-tm">x</text>
  <text x="135" y="185" class="sv-t" style="font-weight:700">P</text>

  <!-- Ponto Q (x+h=320, y=130) -->
  <circle cx="320" cy="130" r="5" class="sv-fillm"/>
  <line x1="320" y1="130" x2="320" y2="230" class="sv-thin sv-dash"/>
  <text x="310" y="246" class="sv-tm">x + h</text>
  <text x="330" y="130" class="sv-tm" style="font-weight:700">Q</text>

  <!-- Reta Secante passando por P e Q -->
  <line x1="80" y1="220" x2="400" y2="100" class="sv-b sv-dash" style="stroke-width:1.8"/>
  <text x="385" y="92" class="sv-tm">Secante (inclinação Δf/Δx)</text>

  <!-- Reta Tangente no ponto P -->
  <line x1="80" y1="230" x2="320" y2="110" class="sv-a" style="stroke-width:2.2"/>
  <text x="240" y="105" class="sv-t" style="font-weight:700">Tangente exata (h → 0)</text>

  <!-- Indicação do delta x (h) -->
  <line x1="160" y1="210" x2="320" y2="210" class="sv-thin" marker-end="url(#m2-arr)"/>
  <text x="235" y="204" class="sv-tm" style="font-weight:700">h = Δx</text>
</svg>'''

# SVG: Funções de ativação (Sigmoide, Tanh, ReLU, GeLU)
SVG_ATIVACAO = r'''<svg viewBox="0 0 540 220" class="lv2-svg" role="img" aria-label="Curvas de ativação: Sigmoide, Tanh, ReLU, GeLU">
  <!-- Eixos centrais -->
  <line x1="30" y1="120" x2="510" y2="120" class="sv-ax"/>
  <line x1="270" y1="20" x2="270" y2="210" class="sv-ax"/>
  <text x="515" y="124" class="sv-tm">x</text>
  <text x="274" y="22" class="sv-tm">y</text>

  <!-- Sigmoide: varia de 0 a 1 (y=120 é 0, y=50 é 1) -->
  <path d="M 40 119 Q 200 119 250 85 T 300 55 Q 380 50 500 50" class="sv-a" style="stroke:#9BA8AB;stroke-width:2"/>
  <text x="440" y="44" class="sv-tm" style="font-weight:700">Sigmoide σ(x)</text>

  <!-- ReLU: 0 para x<=0, x para x>0 -->
  <path d="M 40 120 L 270 120 L 460 25" class="sv-b" style="stroke-width:2.5"/>
  <text x="440" y="20" class="sv-t" style="font-weight:700">ReLU (max(0, x))</text>

  <!-- GeLU: curva suave que mergulha levemente abaixo de 0 antes de subir -->
  <path d="M 40 120 Q 200 120 240 126 Q 260 128 280 115 L 430 35" class="sv-a" style="stroke-dasharray:4 4;stroke-width:2"/>
  <text x="360" y="65" class="sv-t">GeLU (Transformers)</text>

  <!-- Destaque saturação -->
  <rect x="40" y="30" width="80" height="100" fill="rgba(74,92,106,0.15)" rx="4"/>
  <text x="45" y="70" class="sv-tm" style="font-size:10px">Saturação σ'≈ 0</text>
  <rect x="420" y="35" width="80" height="95" fill="rgba(74,92,106,0.15)" rx="4"/>
  <text x="425" y="90" class="sv-tm" style="font-size:10px">Saturação σ'≈ 0</text>
</svg>'''

# SVG: Contorno de Loss e Vetor Gradiente Ortogonal
SVG_GRADIENTE_2D = r'''<svg viewBox="0 0 500 240" class="lv2-svg" role="img" aria-label="Curvas de nível e direção do vetor gradiente">
  <defs>
    <marker id="m2-garr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#CCD0CF"/>
    </marker>
    <marker id="m2-narr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#9BA8AB"/>
    </marker>
  </defs>
  <!-- Elipses concêntricas (Curvas de nível da função quadrática) -->
  <ellipse cx="250" cy="120" rx="200" ry="90" class="sv-thin" style="stroke:#253745"/>
  <ellipse cx="250" cy="120" rx="140" ry="60" class="sv-thin" style="stroke:#4A5C6A"/>
  <ellipse cx="250" cy="120" rx="80" ry="35" class="sv-thin" style="stroke:#4A5C6A"/>
  <ellipse cx="250" cy="120" rx="25" ry="12" class="sv-thin" style="stroke:#9BA8AB"/>
  <circle cx="250" cy="120" r="4" class="sv-fill"/>
  <text x="256" y="124" class="sv-t" style="font-size:11px;font-weight:700">Mínimo w* (Loss mínima)</text>

  <!-- Ponto atual de treino w_t -->
  <circle cx="390" cy="75" r="5" class="sv-fill"/>
  <text x="400" y="70" class="sv-t" style="font-weight:700">w_t (ponto atual)</text>

  <!-- Vetor Gradiente ∇L (máxima subida) -->
  <line x1="390" y1="75" x2="450" y2="45" class="sv-b" style="stroke-width:2.4" marker-end="url(#m2-narr)"/>
  <text x="420" y="38" class="sv-tm" style="font-weight:700">∇L (subida máxima)</text>

  <!-- Vetor Oposto -η∇L (descida para o centro) -->
  <line x1="390" y1="75" x2="310" y2="105" class="sv-a" style="stroke-width:2.8" marker-end="url(#m2-garr)"/>
  <text x="315" y="85" class="sv-t" style="font-weight:700">-η ∇L (passo do GD)</text>

  <!-- Linha tangente à curva de nível mostrando ortogonalidade -->
  <line x1="365" y1="40" x2="415" y2="110" class="sv-thin sv-dash"/>
  <text x="420" y="115" class="sv-tm" style="font-size:10px">Tangente à curva de nível</text>
</svg>'''

# SVG: Comparação de Otimizadores (GD, SGD, Adam)
SVG_OTIMIZADORES = r'''<svg viewBox="0 0 520 220" class="lv2-svg" role="img" aria-label="Trajetória de SGD vs Momentum vs Adam">
  <!-- Ravina elíptica -->
  <ellipse cx="260" cy="110" rx="230" ry="90" class="sv-thin" style="stroke:#253745"/>
  <ellipse cx="260" cy="110" rx="150" ry="50" class="sv-thin" style="stroke:#4A5C6A"/>
  <ellipse cx="260" cy="110" rx="60" ry="18" class="sv-thin" style="stroke:#9BA8AB"/>
  <circle cx="260" cy="110" r="4" class="sv-fill"/>

  <!-- SGD puro (oscila violentamente nas paredes) -->
  <path d="M 70 40 L 90 180 L 120 45 L 145 175 L 175 60 L 205 150 L 230 90 L 255 110" class="sv-b sv-dash" style="stroke:#9BA8AB;stroke-width:1.6"/>
  <text x="65" y="30" class="sv-tm">SGD (oscilações perpendiculares)</text>

  <!-- Momentum / Adam (amortecimento suave direto ao centro) -->
  <path d="M 70 40 Q 110 90 150 102 T 220 108 L 260 110" class="sv-a" style="stroke-width:2.8"/>
  <text x="140" y="125" class="sv-t" style="font-weight:700">Adam / Momentum (amortecido e rápido)</text>
</svg>'''

GUIDES_MOD2_V2 = {
    # =========================================================================
    # TÓPICO 12: Limites e taxa de variação instantânea (ideia geral)
    # =========================================================================
    "Limites e taxa de variação instantânea (ideia geral)": {
        "v": 2,
        "duracao": 25,
        "gancho": r"""Como medir a velocidade exata de um carro de corrida em um <b>único milésimo de segundo</b> se, no instante exato, o tempo parou e a distância percorrida é zero ($\frac{0}{0}$)? Toda a matemática do aprendizado de máquina nasce da solução elegante para essa divisão impossível: a <b>taxa de variação instantânea</b>.""",
        "prerequisitos": [
            "Álgebra básica (fatoração de polinômios)",
            "Coordenadas cartesianas e inclinação de retas ($m = \frac{\Delta y}{\Delta x}$)"
        ],
        "objetivos": [
            "compreender a intuição do limite como uma aproximação contínua sem necessidade de tocar o infinito;",
            "derivar algebricamente a taxa instantânea de variação usando o limite da reta secante quando $h \to 0$;",
            "entender por que em IA usamos derivadas numéricas como verificação de gradiente (Gradient Checking)."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "O Paradoxo da Velocidade",
                "titulo": "A inclinação da secante que vira tangente",
                "corpo": r"""<p>James Stewart, em seu clássico manual de <i>Cálculo</i>, explica que a derivada nasceu da união de dois problemas históricos: o <b>problema da velocidade instantânea</b> na Física e o <b>problema da reta tangente</b> na Geometria.</p>
<p>Se você viaja de São Paulo a Campinas (100 km) em 1 hora, sua velocidade média foi de $100\text{ km/h}$. Mas em vários momentos seu velocímetro marcou $120\text{ km/h}$, e em outros você esteve parado no pedágio a $0\text{ km/h}$.</p>
<p>Para calcular a velocidade em um instante exato $t$, calculamos a velocidade média em um intervalo cada vez menor $h$:</p>
$$v_{\text{média}} = \frac{f(t + h) - f(t)}{h}$$
<p>Se fizermos $h = 0$ diretamente, caímos na indefinição $\frac{0}{0}$. Mas se investigarmos o valor para o qual a fração <b>tende</b> quando $h$ se aproxima infinitesimalmente de zero ($h \to 0$), encontramos a <b>velocidade instantânea</b>!</p>""",
            },
            {
                "tipo": "visual",
                "titulo": "A Geometria do Limite: Da Secante à Tangente",
                "corpo": r"""<p>Geometricamente, a fração $\frac{f(x+h)-f(x)}{h}$ é a inclinação de uma <b>reta secante</b> que corta a curva em dois pontos distintos $P$ e $Q$. Quando encolhemos $h$ em direção a zero, o ponto $Q$ desliza sobre a curva rumo a $P$, e a secante se transforma na <b>reta tangente</b>:</p>""",
                "svg": SVG_SECANTE_TANGENTE,
                "legenda": "Quando h encolhe para zero, a inclinação da secante converge exatamente para a inclinação da reta tangente.",
            },
            {
                "tipo": "notacao",
                "titulo": "Como ler a notação dos limites",
                "corpo": r"""<p>A notação formal introduzida por Cauchy e Weierstrass é o alicerce do Cálculo Moderno:</p>
$$f'(x) = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h}$$""",
                "itens": [
                    {"simbolo": r"$\lim_{h \to 0}$", "leitura": "limite quando h tende a zero", "significado": "Significa investigar o comportamento da expressão à medida que a distância $h$ fica arbitrariamente próxima de zero, sem precisar ser exatamente zero."},
                    {"simbolo": r"$f'(x)$ ou $\frac{df}{dx}$", "leitura": "f linha de x (ou derivada de f em relação a x)", "significado": "A taxa instantânea com que $f(x)$ varia a cada minúscula unidade que você perturba $x$."},
                    {"simbolo": r"$\Delta x, \Delta y$", "leitura": "delta x, delta y", "significado": "Variações macroscópicas finitas. A derivada é a razão entre variações infinitesimais $dy / dx$."},
                ],
            },
            {
                "tipo": "passos",
                "titulo": "Calculando a derivada de f(x) = x² à mão pelo limite",
                "corpo": r"""<p>Vamos encontrar a taxa de variação da função de perda quadrática $f(x) = x^2$ em um ponto qualquer $x$, aplicando a definição formal passo a passo:</p>""",
                "passos": [
                    {
                        "faca": r"Escreva a definição formal do quociente de Newton: $$\frac{f(x+h) - f(x)}{h}$$",
                        "porque": "Precisamos calcular a diferença vertical dividida pela diferença horizontal."
                    },
                    {
                        "faca": r"Substitua $f(x+h) = (x+h)^2$ e $f(x) = x^2$: $$\frac{(x+h)^2 - x^2}{h} = \frac{x^2 + 2xh + h^2 - x^2}{h}$$",
                        "porque": "Expandimos o produto notável $(x+h)^2 = x^2 + 2xh + h^2$."
                    },
                    {
                        "faca": r"Cancele $x^2 - x^2 = 0$: $$\frac{2xh + h^2}{h}$$",
                        "porque": "Os termos constantes em relação a $h$ se anulam perfeitamente."
                    },
                    {
                        "faca": r"Coloque $h$ em evidência e divida pelo denominador: $$\frac{h(2x + h)}{h} = 2x + h \quad (\text{para } h \neq 0)$$",
                        "porque": "Eliminamos a divisão por zero que causava a indeterminação 0/0!"
                    },
                    {
                        "faca": r"Agora aplique o limite $h \to 0$: $$\lim_{h \to 0} (2x + h) = 2x$$",
                        "porque": "Quando $h$ desaparece, sobra apenas $2x$. Conclusão: a derivada de $x^2$ é exatamente $2x$!"
                    }
                ],
                "conclusao": r"Se estivermos no ponto $x = 3$, a inclinação da curva é $f'(3) = 2(3) = 6$. Se aumentarmos $x$ em $0.001$, a função subirá aproximadamente $6 \times 0.001 = 0.006$."
            },
            {
                "tipo": "ponte",
                "titulo": "Onde isso vive na IA: Gradient Checking",
                "corpo": r"""<p>Em frameworks modernos (PyTorch, TensorFlow, JAX), os gradientes são calculados via diferenciação automática exata (autograd). Mas como engenheiros de IA testam se a implementação customizada de uma nova camada não tem bugs matemáticos?</p>
<p>Eles usam a <b>aproximação numérica por diferenças finitas centradas</b> com $h = 10^{-5}$:</p>
$$\frac{\partial L}{\partial w} \approx \frac{L(w + h) - L(w - h)}{2h}$$
<p>Se o gradiente analítico do autograd bater com a aproximação numérica em até 5 casas decimais, temos certeza de que a rede está aprendendo na direção correta!</p>""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Derivada Analítica vs. Numérica",
                "codigo": r'''import numpy as np

# Função de perda quadrática simples L(w) = w^2
def L(w):
    return w ** 2

# Derivada analítica exata deduzida pelo limite: L'(w) = 2w
def grad_analitico(w):
    return 2.0 * w

# Derivada numérica por diferenças finitas centradas
def grad_numerico(f, w, h=1e-5):
    return (f(w + h) - f(w - h)) / (2.0 * h)

# Testando no ponto w = 3.0
w_teste = 3.0
exato = grad_analitico(w_teste)
numerico = grad_numerico(L, w_teste)
erro_relativo = abs(exato - numerico) / (abs(exato) + 1e-12)

print(f"Ponto w = {w_teste}")
print(f"Gradiente Analítico Exato : {exato:.8f}")
print(f"Gradiente Numérico (h=1e-5): {numerico:.8f}")
print(f"Erro Relativo (tolerância < 1e-7): {erro_relativo:.2e}")
assert erro_relativo < 1e-7, "Gradiente incorreto!"
print("Gradient check passou com sucesso!")''',
                "experimentos": [
                    "Altere a função para <code>L(w) = w**3</code>. Deduza a derivada analítica ($3w^2$) e verifique se o gradient check continua batendo.",
                    "Experimente mudar <code>h = 1.0</code> (muito grande) ou <code>h = 1e-15</code> (muito pequeno). Observe como erros de truncamento e erros de ponto flutuante afetam a precisão."
                ]
            },
            {
                "tipo": "armadilhas",
                "titulo": "Armadilhas comuns com limites e derivadas",
                "itens": [
                    {"erro": "Achar que a derivada é a divisão de zero por zero.", "correcao": "O limite analisa a razão de grandezas infinitesimais antes que atinjam zero. A razão converge para um número finito perfeitamente determinado."},
                    {"erro": "Usar h = 1e-20 na diferenciação numérica achando que fica mais preciso.", "correcao": "Em computadores de 64 bits, números menores que 1e-16 sofrem de 'cancelamento catastrófico' na subtração de ponto flutuante. O valor ideal é tipicamente $h \approx 10^{-5}$ a $10^{-7}$."}
                ]
            }
        ],
        "resumo": [
            "A derivada mede a sensibilidade instantânea de uma função: quanto $f(x)$ muda quando $x$ recebe uma leve perturbação.",
            "O limite $\lim_{h \to 0} \frac{f(x+h)-f(x)}{h}$ transforma a inclinação de uma secante na inclinação exata da reta tangente.",
            "Em IA, a taxa de variação diz se devemos aumentar ou diminuir um peso para reduzir o erro da rede."
        ],
        "proxima": r"Agora que entendemos como limites geram derivadas, vamos aprender as regras fundamentais de derivação para não precisarmos calcular limites longos a cada função.",
        "referencias": [
            {"obra": "Stewart, J. Calculus: Early Transcendentals", "trecho": "Capítulo 2: Limits and Derivatives", "uso": "Definição formal de limite e interpretação física da velocidade instantânea"},
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Capítulo 5.1: Slope and Derivative", "uso": "Conexão entre derivadas unidimensionais e otimização de funções de perda"}
        ]
    },

    # =========================================================================
    # TÓPICO 13: Derivadas fundamentais e regras básicas (potência, produto, soma)
    # =========================================================================
    "Derivadas fundamentais e regras básicas (potência, produto, soma)": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Um modelo como o GPT-4 tem mais de 1 trilhão de parâmetros. Se tivéssemos que calcular o limite $\lim_{h \to 0}$ para cada peso, o universo acabaria antes do treino do primeiro lote. Como as <b>regras de derivação</b> transformam cálculos infinitos em simples operações de multiplicação e soma instantâneas?""",
        "prerequisitos": [
            "Conceito de limite e derivada instantânea (Tópico 12)",
            "Polinômios e propriedades distributivas"
        ],
        "objetivos": [
            "dominar as quatro regras fundamentais: constante, potência, soma e produto;",
            "compreender a intuição geométrica da Regra do Produto via área de um retângulo que se expande;",
            "aplicar essas regras na derivação da função de custo do Erro Quadrático Médio (MSE)."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "O Kit de Ferramentas do Engenheiro",
                "titulo": "As quatro regras mestras",
                "corpo": r"""<p>Graças a séculos de desenvolvimento do Cálculo, não precisamos reabrir limites toda vez que derivamos uma função. Qualquer arquitetura de rede neural profunda é composta por blocos elementares combinados por quatro regras universais:</p>
<ul>
<li><b>Regra da Constante:</b> $\frac{d}{dx}[c] = 0$. Um número fixo não varia quando $x$ varia; sua taxa de variação é nula.</li>
<li><b>Regra da Potência:</b> $\frac{d}{dx}[x^n] = n x^{n-1}$. O expoente 'desce' multiplicando e subtraímos 1 do expoente.</li>
<li><b>Regra da Soma:</b> $\frac{d}{dx}[f(x) + g(x)] = f'(x) + g'(x)$. A derivada da soma é a soma das derivadas (linearidade do operador).</li>
<li><b>Regra da Multiplicação por Escalar:</b> $\frac{d}{dx}[c \cdot f(x)] = c \cdot f'(x)$. Uma constante multiplicativa simplesmente acompanha a derivada.</li>
</ul>""",
            },
            {
                "tipo": "texto",
                "rotulo": "Intuição Geométrica",
                "titulo": "Por que a Regra do Produto NÃO é simplesmente u' · v'?",
                "corpo": r"""<p>Um dos erros mais comuns de iniciantes é pensar que $(u \cdot v)' = u' \cdot v'$. James Stewart demonstra isso imaginando um retângulo de lados $u$ e $v$, cuja área é $A = u \cdot v$:</p>
<p>Se aumentamos a largura de $u$ para $u + \Delta u$ e a altura de $v$ para $v + \Delta v$, a nova área expandida é:</p>
$$A_{\text{nova}} = (u + \Delta u)(v + \Delta v) = u v + v \Delta u + u \Delta v + \Delta u \Delta v$$
<p>A variação total da área é $\Delta A = A_{\text{nova}} - u v = v \Delta u + u \Delta v + \Delta u \Delta v$.</p>
<p>Dividindo tudo por $\Delta x$ e fazendo as variações irem a zero, o termo pequenino $\Delta u \Delta v$ vira uma poeira de 2ª ordem e desaparece. Restam exatamente duas faixas de expansão:</p>
$$\frac{d}{dx}[u(x) \cdot v(x)] = u'(x) \cdot v(x) + u(x) \cdot v'(x)$$
<p><i>“Derivada do primeiro vezes o segundo, mais o primeiro vezes a derivada do segundo!”</i></p>""",
            },
            {
                "tipo": "notacao",
                "titulo": "Resumo das Regras Essenciais",
                "corpo": r"""<p>Mantenha essa tabela sempre em mente ao inspecionar papers de Machine Learning:</p>""",
                "itens": [
                    {"simbolo": r"$\frac{d}{dx}[x^3] = 3x^2$", "leitura": "derivada de x ao cubo", "significado": "Regra da potência com $n=3$. Em $x=2$, a inclinação é $3(2^2) = 12$."},
                    {"simbolo": r"$\frac{d}{dx}[e^x] = e^x$", "leitura": "derivada da exponencial natural", "significado": "A única função cuja taxa de variação instantânea é rigorosamente idêntica ao seu próprio valor em qualquer ponto."},
                    {"simbolo": r"$\frac{d}{dx}[\ln(x)] = \frac{1}{x}$", "leitura": "derivada do logaritmo natural", "significado": "Fundamental na função de perda de Cross-Entropy (Entropia Cruzada) usada em LLMs."},
                ],
            },
            {
                "tipo": "passos",
                "titulo": "Exemplo Prático: Derivando a Loss de Regressão Linear",
                "corpo": r"""<p>Vamos derivar a perda de um único exemplo em relação ao peso $w$, onde a predição é $\hat{y} = w x$ e a perda quadrática é $L = (\hat{y} - y)^2 = (w x - y)^2$:</p>""",
                "passos": [
                    {
                        "faca": r"Expanda o quadrado da diferença: $$L(w) = w^2 x^2 - 2 w x y + y^2$$",
                        "porque": "Permite aplicar as regras da soma, constante e potência diretamente."
                    },
                    {
                        "faca": r"Aplique a regra da soma termo a termo: $$\frac{dL}{dw} = \frac{d}{dw}[w^2 x^2] - \frac{d}{dw}[2 w x y] + \frac{d}{dw}[y^2]$$",
                        "porque": "A derivada da soma é a soma das derivadas."
                    },
                    {
                        "faca": r"Trate $x$ e $y$ como constantes em relação a $w$: $$\frac{d}{dw}[w^2 x^2] = x^2 (2w) = 2 w x^2$$ $$\frac{d}{dw}[2 w x y] = 2 x y (1) = 2 x y$$ $$\frac{d}{dw}[y^2] = 0$$",
                        "porque": "$y^2$ não depende de $w$, logo sua derivada é zero."
                    },
                    {
                        "faca": r"Agrupe e coloque $2x$ em evidência: $$\frac{dL}{dw} = 2 x (w x - y) = 2 x (\hat{y} - y)$$",
                        "porque": "Chegamos à famosa fórmula do gradiente: <b>2 vezes o erro de predição vezes a entrada x</b>!"
                    }
                ],
                "conclusao": r"Se a rede previu $\hat{y} = 8$ mas o real era $y = 5$, o erro é $+3$. Se $x = 2$, o gradiente é $2(2)(3) = 12$. O peso $w$ deve diminuir para reduzir esse erro."
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Regras de Derivação em Ação",
                "codigo": r'''import numpy as np

# Entrada x e rótulo real y
x = 2.0
y = 5.0
w = 4.0  # peso atual

# Forward pass (predição e loss)
y_hat = w * x          # 4.0 * 2.0 = 8.0
loss = (y_hat - y)**2  # (8.0 - 5.0)^2 = 9.0

# Backward pass analítico usando a regra deduzida
erro = y_hat - y       # 3.0
dL_dw = 2.0 * x * erro # 2 * 2.0 * 3.0 = 12.0

# Passo de atualização com taxa de aprendizado eta = 0.05
eta = 0.05
w_novo = w - eta * dL_dw  # 4.0 - 0.05 * 12.0 = 3.4

# Nova perda após o passo
y_hat_novo = w_novo * x
loss_nova = (y_hat_novo - y)**2

print(f"Loss inicial: {loss:.4f} (com w = {w})")
print(f"Gradiente dL/dw: {dL_dw:.4f}")
print(f"Novo peso w: {w_novo:.4f}")
print(f"Nova loss: {loss_nova:.4f} (redução de {(1 - loss_nova/loss)*100:.1f}%)")
assert loss_nova < loss, "A loss deveria ter diminuído!"''',
                "experimentos": [
                    "Altere <code>w = 1.0</code> (fazendo a predição subestimar o valor real, com $\hat{y} = 2.0$). Observe o sinal negativo do gradiente e veja como o peso é aumentado.",
                    "Experimente com uma taxa de aprendizado muito alta (ex.: <code>eta = 0.6</code>) e observe a loss explodir devido a passos descalibrados."
                ]
            },
            {
                "tipo": "desafio",
                "titulo": "Sua vez de praticar",
                "exercicios": [
                    {
                        "enunciado": r"Calcule a derivada de $f(x) = 5 x^3 - 4 x^2 + 7 x - 12$ no ponto $x = 1$.",
                        "dicas": [
                            "Derive termo a termo usando a regra da potência: $\\frac{d}{dx}[x^n] = n x^{n-1}$.",
                            "Lembre-se de que a derivada de uma constante $-12$ é zero.",
                            "Depois de achar a expressão $f'(x)$, substitua $x = 1$."
                        ],
                        "resposta": r"Aplicando a regra da potência: $f'(x) = 5(3x^2) - 4(2x) + 7(1) - 0 = 15x^2 - 8x + 7$. No ponto $x=1$: $f'(1) = 15(1) - 8(1) + 7 = 14$."
                    }
                ]
            }
        ],
        "resumo": [
            "Regras de derivação decompõem funções complexas em combinações de regras triviais (potência, soma, produto).",
            "A regra do produto $(uv)' = u'v + uv'$ surge da expansão de duas faces de uma área geométrica retangular.",
            "O gradiente do erro quadrático é proporcional ao resíduo $(\hat{y} - y)$ multiplicado pela entrada $x$."
        ],
        "proxima": r"Agora que sabemos derivar funções isoladas, como derivamos funções aninhadas uma dentro da outra? Esse é o papel da Regra da Cadeia, o coração do Backpropagation.",
        "referencias": [
            {"obra": "Stewart, J. Calculus: Early Transcendentals", "trecho": "Capítulo 3: Differentiation Rules", "uso": "Dedução geométrica da regra do produto e tabela fundamental de derivadas"},
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Capítulo 5.2: Taylor Series and Derivative Rules", "uso": "Aplicação das regras em funções de custo de aprendizado estatístico"}
        ]
    },

    # =========================================================================
    # TÓPICO 14: Regra da Cadeia (Chain Rule) - o motor do Backpropagation
    # =========================================================================
    "Regra da Cadeia (Chain Rule) - o motor do Backpropagation": LESSONS_V2_SAMPLES["Regra da Cadeia (Chain Rule) - o motor do Backpropagation"],

    # =========================================================================
    # TÓPICO 15: Derivadas de funções de ativação (Sigmoide, Tanh, ReLU, GeLU)
    # =========================================================================
    "Derivadas de funções de ativação (Sigmoide, Tanh, ReLU, GeLU)": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Por mais de 20 anos, o treinamento de redes neurais profundas falhava porque o sinal de aprendizado desaparecia misteriosamente após poucas camadas. A culpa era de uma propriedade insidiosa da derivada da função <b>Sigmoide</b>. Como a substituição por <b>ReLU</b> e depois <b>GeLU</b> permitiu que os Transformers do ChatGPT treinassem centenas de camadas sem congelar?""",
        "prerequisitos": [
            "Regra da Cadeia e derivadas elementares (Tópicos 13 e 14)",
            "Função exponencial $e^x$"
        ],
        "objetivos": [
            "derivar analiticamente a função Sigmoide e compreender sua propriedade elegante $\sigma'(z) = \sigma(z)(1 - \sigma(z))$;",
            "entender geometricamente o problema do Vanishing Gradient (gradiente evanescente);",
            "comparar as vantagens e limitações de Sigmoide, Tanh, ReLU, Leaky ReLU e GeLU na arquitetura de LLMs."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "O Papel da Não-Linearidade",
                "titulo": "Por que redes neurais precisam de ativações?",
                "corpo": r"""<p>Em Álgebra Linear, aprendemos que o produto de matrizes é sempre linear: $W_2 (W_1 \mathbf{x}) = (W_2 W_1) \mathbf{x} = W_{\text{total}} \mathbf{x}$. Se uma rede neural de 100 camadas tivesse apenas multiplicações lineares, ela seria matematicamente idêntica a uma rede de <b>uma única camada</b>!</p>
<p>As <b>funções de ativação não lineares</b> $\sigma(z)$ são as dobradiças que curvam o espaço de decisão, permitindo que a rede aprenda fronteiras altamente complexas. Mas toda função de ativação precisa ser diferenciável para que o gradiente possa fluir de volta no Backpropagation.</p>""",
            },
            {
                "tipo": "visual",
                "titulo": "As Quatro Grandes Ativações",
                "corpo": r"""<p>Veja como o formato de cada curva dita o comportamento de sua respectiva derivada:</p>""",
                "svg": SVG_ATIVACAO,
                "legenda": "Sigmoide satura nas extremidades (derivada vai a zero). ReLU tem gradiente constante 1 para valores positivos. GeLU suaviza a transição perto de zero.",
            },
            {
                "tipo": "passos",
                "titulo": "Dedução Elegante: A Derivada da Sigmoide",
                "corpo": r"""<p>A função Sigmoide é definida como $\sigma(z) = \frac{1}{1 + e^{-z}} = (1 + e^{-z})^{-1}$. Vamos calcular sua derivada usando a Regra da Cadeia:</p>""",
                "passos": [
                    {
                        "faca": r"Aplique a regra da potência com expoente $-1$: $$\frac{d\sigma}{dz} = -1(1 + e^{-z})^{-2} \cdot \frac{d}{dz}[1 + e^{-z}]$$",
                        "porque": "Regra da cadeia: derivada da função de fora vezes a derivada de dentro."
                    },
                    {
                        "faca": r"Calcule a derivada interna: $\frac{d}{dz}[1 + e^{-z}] = -e^{-z}$. Substitua na expressão: $$\frac{d\sigma}{dz} = -(1 + e^{-z})^{-2} (-e^{-z}) = \frac{e^{-z}}{(1 + e^{-z})^2}$$",
                        "porque": "Menos com menos resulta em sinal positivo."
                    },
                    {
                        "faca": r"Separe a fração em dois fatores inteligentes: $$\frac{e^{-z}}{(1 + e^{-z})^2} = \left(\frac{1}{1 + e^{-z}}\right) \left(\frac{e^{-z}}{1 + e^{-z}}\right)$$",
                        "porque": "O primeiro fator é exatamente a própria definição de $\sigma(z)$!"
                    },
                    {
                        "faca": r"Some e subtraia 1 no numerador do segundo fator: $$\frac{e^{-z}}{1 + e^{-z}} = \frac{1 + e^{-z} - 1}{1 + e^{-z}} = 1 - \frac{1}{1 + e^{-z}} = 1 - \sigma(z)$$",
                        "porque": "Reescrevemos o segundo fator totalmente em termos de $\sigma(z)$."
                    },
                    {
                        "faca": r"Junte os dois fatores: $$\sigma'(z) = \sigma(z) \cdot (1 - \sigma(z))$$",
                        "porque": "Uma das fórmulas mais bonitas de toda a matemática: a derivada da sigmoide pode ser calculada reusando sua própria saída!"
                    }
                ],
                "conclusao": r"Em $z = 0$, $\sigma(0) = 0.5$. Portanto, a derivada máxima é $\sigma'(0) = 0.5 \times 0.5 = 0.25$. Em qualquer outro ponto, a derivada é <b>menor que 0.25</b>!"
            },
            {
                "tipo": "armadilhas",
                "titulo": "A armadilha mortal: Vanishing Gradient",
                "corpo": r"""<p>Por que a derivada máxima da Sigmoide ser $0.25$ quase matou o Deep Learning?</p>
<p>Imagine uma rede com 10 camadas em série usando Sigmoide. Na Regra da Cadeia, os gradientes são multiplicados camada por camada:</p>
$$\frac{\partial L}{\partial w_1} \propto \sigma'_1 \cdot \sigma'_2 \cdot \sigma'_3 \dots \sigma'_{10} \le (0.25)^{10} \approx 0.00000095$$
<p>O sinal que chega na primeira camada é atenuado por um fator de <b>um milhão</b>! Os primeiros pesos simplesmente param de atualizar: a rede 'congela'.</p>""",
                "itens": [
                    {"erro": "Usar Sigmoide em camadas intermediárias (ocultas) de redes profundas.", "correcao": "Use ReLU, Leaky ReLU ou GeLU nas camadas ocultas. Reserve a Sigmoide apenas para a última camada em classificação binária."},
                    {"erro": "Achar que a ReLU é perfeita porque tem derivada 1.", "correcao": "Se a entrada da ReLU for negativa ($z < 0$), sua derivada é rigorosamente 0. Se um neurônio ficar preso na região negativa para todos os dados, ele 'morre' para sempre (Dying ReLU)."}
                ]
            },
            {
                "tipo": "tabela",
                "titulo": "Comparativo das Funções de Ativação em IA",
                "cabecalho": ["Ativação", "Fórmula", "Derivada", "Vantagem Principal", "Onde é usada?"],
                "linhas": [
                    ["Sigmoide", r"$\sigma(z) = \frac{1}{1 + e^{-z}}$", r"$\sigma(1 - \sigma) \le 0.25$", "Mapeia para probabilidade $[0, 1]$", "Classificação binária final, gates de LSTM"],
                    ["Tanh", r"$\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$", r"$1 - \tanh^2(z) \le 1.0$", "Centrada em zero (saídas $[-1, 1]$)", "Células de RNN clássica"],
                    ["ReLU", r"$\max(0, z)$", r"$1 \text{ se } z>0 \text{ senão } 0$", "Custo computacional mínimo, sem saturação positiva", "Redes convolucionais (CNNs), MLPs"],
                    ["GeLU", r"$z \cdot \Phi(z)$", r"Suave, probabilística", "Não tem ponta afiada em zero, excelente fluxo de gradiente", "Padrão moderno em BERT, GPT-2/3/4, LLaMA"]
                ]
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Multiplicação em Cadeia e Vanishing Gradient",
                "codigo": r'''import numpy as np

# Função sigmoide e sua derivada elegante
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

def d_sigmoid(z):
    s = sigmoid(z)
    return s * (1.0 - s)

# Derivada da ReLU
def d_relu(z):
    return np.where(z > 0, 1.0, 0.0)

# Simulando uma rede com 10 camadas lineares em sequência
np.random.seed(42)
camadas = 10
z_valores = np.random.uniform(-2, 2, size=camadas)

# Multiplicando as derivadas ao longo das 10 camadas (Regra da Cadeia)
grad_sigmoide = np.prod([d_sigmoid(z) for z in z_valores])
grad_relu = np.prod([d_relu(np.maximum(0.1, z)) for z in z_valores])

print("Simulação do fluxo de gradiente ao longo de 10 camadas:")
print(f"Sinal residual com Sigmoide: {grad_sigmoide:.2e}")
print(f"Sinal residual com ReLU    : {grad_relu:.2f}")
print(f"Atenuação da Sigmoide: o sinal é {grad_relu / (grad_sigmoide + 1e-12):,.0f}x mais fraco!")''',
                "experimentos": [
                    "Aumente o número de camadas para <code>camadas = 30</code> e veja como o gradiente da Sigmoide desaparece para exatamente 0.0 na precisão do computador.",
                    "Experimente com valores extremos de $z$, como $z = 8.0$. Observe como a derivada da Sigmoide cai para ordens de $10^{-4}$ mesmo em uma única camada."
                ]
            }
        ],
        "resumo": [
            "Não-linearidades são essenciais para que redes neurais empilhem capacidade de representação além de matrizes lineares.",
            "A derivada da sigmoide $\sigma(1-\sigma)$ tem teto em 0.25, gerando o colapso por gradiente evanescente em redes profundas.",
            "GeLU e ReLU resolveram esse estrangulamento e formam a base das arquiteturas modernas de Transformers."
        ],
        "proxima": r"Agora que dominamos derivadas de uma variável, como lidamos com funções de múltiplos parâmetros? Entra em cena o vetor Gradiente.",
        "referencias": [
            {"obra": "Goodfellow, Bengio & Courville. Deep Learning", "trecho": "Capítulo 6.3: Hidden Units", "uso": "Análise comparativa de Sigmoide, Tanh, ReLU e variantes"},
            {"obra": "Hendrycks & Gimpel (2016). Gaussian Error Linear Units (GELUs)", "trecho": "Paper original", "uso": "Motivação teórica para o uso de GeLU nos Transformers modernos"}
        ]
    },

    # =========================================================================
    # TÓPICO 16: Derivadas parciais e o vetor Gradiente (nabla f)
    # =========================================================================
    "Derivadas parciais e o vetor Gradiente (nabla f)": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Imagine estar vendado em uma montanha nebulosa cheia de vales e colinas em 360 graus. Como seus pés podem sentir, em uma fração de segundo, a <b>direção exata</b> que desce o morro mais rápido? O <b>vetor Gradiente ($\nabla f$)</b> é a bússola geométrica que guia todo algoritmo de Machine Learning.""",
        "prerequisitos": [
            "Vetores em $\mathbb{R}^n$ (Tópico 1)",
            "Derivadas fundamentais e regra da potência (Tópico 13)"
        ],
        "objetivos": [
            "compreender derivadas parciais como a inclinação obtida ao congelar todas as outras variáveis exceto uma;",
            "montar o vetor gradiente $\nabla f$ e provar geometricamente por que ele aponta na direção de máxima subida;",
            "visualizar o gradiente como um vetor perpendicular às curvas de nível de uma superfície de erro."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Arte de Congelar Variáveis",
                "titulo": "O que é uma derivada parcial?",
                "corpo": r"""<p>No mundo real e em IA, funções de perda nunca dependem de uma única variável. Elas dependem de milhões de pesos simultaneamente: $L(w_1, w_2, \dots, w_d)$.</p>
<p>Para calcular o efeito de um único peso $w_1$ sobre o erro total, usamos a <b>derivada parcial</b> $\frac{\partial L}{\partial w_1}$. O símbolo $\partial$ (chamado <i>del</i> ou <i>d arredondado</i>) avisa:</p>
<p><b>“Finja que todos os outros pesos ($w_2, w_3, \dots$) são números fixos congelados na pedra, e derive a expressão considerando apenas $w_1$ como variável livre!”</b></p>""",
            },
            {
                "tipo": "notacao",
                "titulo": "A Notação do Gradiente",
                "corpo": r"""<p>Quando agrupamos todas as derivadas parciais individuais em uma única lista vertical, formamos o <b>vetor Gradiente</b>:</p>
$$\nabla f(\mathbf{x}) = \begin{bmatrix} \frac{\partial f}{\partial x_1} \\ \frac{\partial f}{\partial x_2} \\ \vdots \\ \frac{\partial f}{\partial x_d} \end{bmatrix} \in \mathbb{R}^d$$""",
                "itens": [
                    {"simbolo": r"$\nabla$ (Nabla)", "leitura": "nabla f (ou gradiente de f)", "significado": "O operador vetorial diferencial. Transforma uma função escalar (que cospe um único número de erro) em um vetor completo de direção em $\mathbb{R}^d$."},
                    {"simbolo": r"$\frac{\partial f}{\partial x_i}$", "leitura": "derivada parcial de f em relação a x índice i", "significado": "A taxa de variação da função ao andar exclusivamente na direção do eixo $x_i$."},
                    {"simbolo": r"$-\nabla f$", "leitura": "menos gradiente", "significado": "O vetor que aponta para a <b>direção de máxima descida</b>. É o passo que damos para minimizar o erro!"},
                ],
            },
            {
                "tipo": "visual",
                "titulo": "Ortogonalidade às Curvas de Nível",
                "corpo": r"""<p>Em um mapa topográfico, as linhas de contorno (curvas de nível) conectam pontos de mesma altitude. O vetor gradiente tem uma propriedade matemática extraordinária: ele é sempre <b>perpendicular (ortogonal)</b> à curva de nível que passa pelo ponto atual!</p>""",
                "svg": SVG_GRADIENTE_2D,
                "legenda": "O gradiente aponta perpendicularmente à elipse de contorno na direção de maior subida. O algoritmo dá um passo na direção oposta (-∇L).",
            },
            {
                "tipo": "passos",
                "titulo": "Cálculo Passo a Passo: O Gradiente de uma Bacia 2D",
                "corpo": r"""<p>Considere uma função de perda com dois parâmetros $w_1$ e $w_2$: $$L(w_1, w_2) = 2 w_1^2 + 3 w_2^2$$ Vamos calcular o gradiente no ponto inicial $(w_1, w_2) = (2, 1)$:</p>""",
                "passos": [
                    {
                        "faca": r"Calcule a derivada parcial em relação a $w_1$: trate $w_2$ como constante. $$\frac{\partial L}{\partial w_1} = \frac{\partial}{\partial w_1}[2 w_1^2] + 0 = 4 w_1$$",
                        "porque": "Como $3 w_2^2$ não tem $w_1$, sua derivada é zero."
                    },
                    {
                        "faca": r"Calcule a derivada parcial em relação a $w_2$: trate $w_1$ como constante. $$\frac{\partial L}{\partial w_2} = 0 + \frac{\partial}{\partial w_2}[3 w_2^2] = 6 w_2$$",
                        "porque": "Como $2 w_1^2$ não tem $w_2$, sua derivada é zero."
                    },
                    {
                        "faca": r"Monte o vetor gradiente simbólico: $$\nabla L(w_1, w_2) = \begin{bmatrix} 4 w_1 \\ 6 w_2 \end{bmatrix}$$",
                        "porque": "Agrupamos as parciais em um vetor coluna."
                    },
                    {
                        "faca": r"Avalie no ponto $(2, 1)$: $$\nabla L(2, 1) = \begin{bmatrix} 4(2) \\ 6(1) \end{bmatrix} = \begin{bmatrix} 8 \\ 6 \end{bmatrix}$$",
                        "porque": "Substituímos as coordenadas numéricas atuais."
                    },
                    {
                        "faca": r"Calcule a magnitude e o vetor de descida: $$\|-\nabla L\| = \sqrt{(-8)^2 + (-6)^2} = \sqrt{64 + 36} = 10$$",
                        "porque": "A direção ótima de descida é o vetor $[-8, -6]^\top$."
                    }
                ],
                "conclusao": r"Se dermos um passo com taxa de aprendizado $\eta = 0.1$, o novo ponto será $(w_1, w_2) = (2, 1) - 0.1 \times [8, 6] = (2 - 0.8, 1 - 0.6) = (1.2, 0.4)$. A perda cairá de $2(2^2) + 3(1^2) = 11.0$ para $2(1.2^2) + 3(0.4^2) = 2.88 + 0.48 = 3.36$ (uma queda colossal de 70% em um único passo!)."
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Calculando e Visualizando o Gradiente 2D",
                "codigo": r'''import numpy as np

# Função de perda bivariada
def L(w1, w2):
    return 2.0 * w1**2 + 3.0 * w2**2

# Gradiente analítico exato
def grad_L(w1, w2):
    dw1 = 4.0 * w1
    dw2 = 6.0 * w2
    return np.array([dw1, dw2])

# Ponto de partida
w = np.array([2.0, 1.0])
eta = 0.1

print(f"Ponto inicial: w = {w}, Loss = {L(w[0], w[1]):.2f}")

# 5 passos de Descida do Gradiente
for passo in range(1, 6):
    g = grad_L(w[0], w[1])
    w = w - eta * g
    loss = L(w[0], w[1])
    print(f"Passo {passo}: w = [{w[0]:.3f}, {w[1]:.3f}], ||g|| = {np.linalg.norm(g):.2f}, Loss = {loss:.4f}")

assert loss < 0.5, "Deveria ter convergido próximo ao mínimo (0,0)!"''',
                "experimentos": [
                    "Observe como a componente $w_2$ converge mais rápido que $w_1$ porque sua curvatura é mais íngreme ($6w_2$ vs $4w_1$).",
                    "Adicione um termo cruzado como $w_1 w_2$ à função e calcule as novas derivadas parciais com o produto."
                ]
            }
        ],
        "resumo": [
            "Derivadas parciais medem a sensibilidade de uma função multidimensional ao mover um parâmetro de cada vez mantendo os outros fixos.",
            "O vetor gradiente $\nabla f$ agrupa todas as derivadas parciais e aponta geometricamente para a direção de maior subida.",
            "O algoritmo de otimização move os pesos na direção do oposto do gradiente ($-\nabla f$) para descer o relevo do erro."
        ],
        "proxima": r"O gradiente resume a primeira derivada de uma função vetorial. Mas o que acontece se tivermos funções que recebem vetores e cospem vetores? Entram a matriz Jacobiana e a curvatura da Hessiana.",
        "referencias": [
            {"obra": "Stewart, J. Multivariable Calculus", "trecho": "Capítulo 14.6: Directional Derivatives and the Gradient Vector", "uso": "Prova de que o gradiente aponta na direção de máxima taxa de crescimento"},
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Capítulo 5.3: Gradients of Vector-Valued Functions", "uso": "Formalização do vetor gradiente em espaços multidimensionais"}
        ]
    },

    # =========================================================================
    # TÓPICO 17: Matriz Jacobiana e Matriz Hessiana (curvatura da loss)
    # =========================================================================
    "Matriz Jacobiana e Matriz Hessiana (curvatura da loss)": {
        "v": 2,
        "duracao": 35,
        "gancho": r"""O gradiente informa para onde ir, mas ele é cego em relação a um detalhe crucial: o relevo à sua frente é um vale aberto e plano ou uma ravina traiçoeira em formato de sela de cavalo? Como a <b>Matriz Jacobiana</b> generaliza derivadas para camadas inteiras e a <b>Matriz Hessiana</b> mede a curvatura de 2ª ordem da perda?""",
        "prerequisitos": [
            "Derivadas parciais e vetor gradiente (Tópico 16)",
            "Matrizes e transformações lineares (Tópicos 6 e 7)",
            "Autovalores e autovetores (Tópico 10)"
        ],
        "objetivos": [
            "compreender a Matriz Jacobiana como a tabela de derivadas de 1ª ordem para funções de vetor-para-vetor;",
            "construir a Matriz Hessiana de derivadas parciais de 2ª ordem;",
            "usar os autovalores da Hessiana para classificar mínimos locais, máximos locais e pontos de sela (Saddle Points);",
            "entender por que métodos de 2ª ordem puros (Newton-Raphson) são inviáveis em LLMs."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "Jacobiana: De Vetores para Vetores",
                "titulo": "A Matriz das Derivadas Cruzadas de 1ª Ordem",
                "corpo": r"""<p>Em uma camada de rede neural, a entrada é um vetor $\mathbf{x} \in \mathbb{R}^n$ e a saída é outro vetor $\mathbf{y} = \mathbf{f}(\mathbf{x}) \in \mathbb{R}^m$. Como representar todas as taxas de variação possíveis?</p>
<p>Precisamos saber como cada componente de saída $y_i$ responde a cada componente de entrada $x_j$. Essa coleção organizada forma a <b>Matriz Jacobiana</b> $J \in \mathbb{R}^{m \times n}$:</p>
$$J = \begin{bmatrix} \frac{\partial f_1}{\partial x_1} & \frac{\partial f_1}{\partial x_2} & \cdots & \frac{\partial f_1}{\partial x_n} \\ \frac{\partial f_2}{\partial x_1} & \frac{\partial f_2}{\partial x_2} & \cdots & \frac{\partial f_2}{\partial x_n} \\ \vdots & \vdots & \ddots & \vdots \\ \frac{\partial f_m}{\partial x_1} & \frac{\partial f_m}{\partial x_2} & \cdots & \frac{\partial f_m}{\partial x_n} \end{bmatrix}$$
<p>Cada linha de $J$ é simplesmente o gradiente transposto de uma das saídas: $J_{i, :} = (\nabla f_i)^\top$.</p>""",
            },
            {
                "tipo": "texto",
                "rotulo": "Hessiana: A Curvatura de 2ª Ordem",
                "titulo": "Como saber se o chão é uma tigela ou uma sela?",
                "corpo": r"""<p>Se a perda é uma função escalar $L(\mathbf{w})$, o gradiente $\nabla L$ dá a inclinação de 1ª ordem. Mas qual é a <i>aceleração</i> ou <i>curvatura</i> do relevo?</p>
<p>A <b>Matriz Hessiana</b> $H \in \mathbb{R}^{d \times d}$ agrupa todas as derivadas parciais de 2ª ordem:</p>
$$H_{ij} = \frac{\partial^2 L}{\partial w_i \partial w_j}$$
<p>Pelo Teorema de Clairaut-Schwarz, se as derivadas forem contínuas, $\frac{\partial^2 L}{\partial w_i \partial w_j} = \frac{\partial^2 L}{\partial w_j \partial w_i}$. Logo, a matriz Hessiana é <b>sempre simétrica</b> ($H = H^\top$)!</p>""",
            },
            {
                "tipo": "notacao",
                "titulo": "Classificação via Autovalores da Hessiana",
                "corpo": r"""<p>Os autovalores $\lambda_i$ da matriz Hessiana revelam a geometria local do espaço onde o gradiente se anula ($\nabla L = \mathbf{0}$):</p>""",
                "itens": [
                    {"simbolo": r"$\lambda_i > 0 \quad (\forall i)$", "leitura": "todos autovalores positivos (Hessiana positiva-definida)", "significado": "O relevo curva para cima em todas as direções: estamos em um <b>Mínimo Local</b> (fundo de uma tigela)."},
                    {"simbolo": r"$\lambda_i < 0 \quad (\forall i)$", "leitura": "todos autovalores negativos (Hessiana negativa-definida)", "significado": "O relevo curva para baixo em todas as direções: estamos em um <b>Máximo Local</b> (topo de um morro)."},
                    {"simbolo": r"$\lambda \text{ com sinais mistos}$", "leitura": "autovalores positivos e negativos", "significado": "Em algumas direções curva para cima, em outras para baixo: estamos em um <b>Ponto de Sela (Saddle Point)</b>!"},
                ],
            },
            {
                "tipo": "passos",
                "titulo": "Cálculo Passo a Passo: Hessiana e Ponto de Sela",
                "corpo": r"""<p>Vamos analisar a função clássica de sela $f(x, y) = x^2 - y^2$ no ponto crítico $(0, 0)$:</p>""",
                "passos": [
                    {
                        "faca": r"Calcule o vetor gradiente de 1ª ordem: $$\nabla f = \begin{bmatrix} \frac{\partial f}{\partial x} \\ \frac{\partial f}{\partial y} \end{bmatrix} = \begin{bmatrix} 2x \\ -2y \end{bmatrix}$$",
                        "porque": "No ponto $(0, 0)$, $\nabla f = [0, 0]^\top$. É um ponto estacionário."
                    },
                    {
                        "faca": r"Calcule as segundas derivadas parciais: $$\frac{\partial^2 f}{\partial x^2} = 2, \quad \frac{\partial^2 f}{\partial y^2} = -2, \quad \frac{\partial^2 f}{\partial x \partial y} = 0$$",
                        "porque": "Derivamos cada componente de 1ª ordem novamente."
                    },
                    {
                        "faca": r"Monte a matriz Hessiana: $$H = \begin{bmatrix} 2 & 0 \\ 0 & -2 \end{bmatrix}$$",
                        "porque": "Organizamos os termos na matriz simétrica $2 \times 2$."
                    },
                    {
                        "faca": r"Extraia os autovalores de $H$: Como $H$ é diagonal, seus autovalores são os próprios elementos diagonais: $$\lambda_1 = +2, \quad \lambda_2 = -2$$",
                        "porque": "Temos um autovalor estritamente positivo e outro estritamente negativo."
                    }
                ],
                "conclusao": r"Como os autovalores têm sinais opostos, $(0,0)$ é categoricamente um <b>ponto de sela</b>! Ao longo do eixo x a função sobe como uma parábola $x^2$, e ao longo do eixo y a função despenca como $-y^2$."
            },
            {
                "tipo": "ponte",
                "titulo": "Por que o Método de Newton não é usado em LLMs?",
                "corpo": r"""<p>O método de Newton usa a Hessiana para dar o salto perfeito até o mínimo em um único passo: $\mathbf{w}_{t+1} = \mathbf{w}_t - H^{-1} \nabla L$. Por que não usamos isso em redes neurais modernas?</p>
<ol>
<li><b>Custo de Memória Impossível:</b> Um modelo com $d = 100\text{ bilhões}$ de parâmetros exigiria uma Hessiana de tamanho $10^{11} \times 10^{11} = 10^{22}$ números em ponto flutuante! Isso exigiria bilhões de petabytes de memória RAM.</li>
<li><b>Custo de Inversão Cúbico:</b> Inverter uma matriz $d \times d$ custa $\mathcal{O}(d^3)$ operações.</li>
<li><b>Atração por Pontos de Sela:</b> O método de Newton puro é atraído cega e agressivamente para pontos de sela onde $\nabla L = \mathbf{0}$, em vez de fugir deles.</li>
</ol>
<p>Por isso, o aprendizado profundo moderno usa <b>métodos de 1ª ordem com estimativas diagonais inteligentes</b>, como o otimizador Adam!</p>""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Hessiana e Autovalores",
                "codigo": r'''import numpy as np

# Função com ponto de sela f(x, y) = x^2 - y^2
def f(x, y):
    return x**2 - y**2

# Hessiana analítica
H = np.array([
    [2.0,  0.0],
    [0.0, -2.0]
])

# Cálculo de autovalores e autovetores
autovalores, autovetores = np.linalg.eigh(H)

print("Matriz Hessiana:")
print(H)
print("\nAutovalores da Hessiana:", autovalores)

if np.all(autovalores > 0):
    print("Classificação: Mínimo Local estrito (tigela)")
elif np.all(autovalores < 0):
    print("Classificação: Máximo Local estrito (morro)")
else:
    print("Classificação: PONTO DE SELA (Saddle Point)! Sinais mistos detectados.")''',
                "experimentos": [
                    "Modifique a Hessiana para uma tigela com $H = [[4.0, 1.0], [1.0, 3.0]]$. Verifique se ambos os autovalores ficam positivos.",
                    "Experimente calcular o determinante de $H$ ($\det(H) = \lambda_1 \lambda_2$). Em 2D, $\det(H) < 0$ é a assinatura garantida de um ponto de sela!"
                ]
            }
        ],
        "resumo": [
            "A Matriz Jacobiana agrupa as derivadas de 1ª ordem de transformações de vetor para vetor (camadas de redes neurais).",
            "A Matriz Hessiana contém as derivadas parciais de 2ª ordem e mede a curvatura multidimensional da função de perda.",
            "Autovalores de sinais mistos na Hessiana denunciam pontos de sela, que são onipresentes em relevos de alta dimensionalidade."
        ],
        "proxima": r"Armados com o gradiente, vamos entender a dinâmica completa do algoritmo mais importante da história da computação moderna: a Descida do Gradiente.",
        "referencias": [
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Capítulo 5.4: Higher-Order Derivatives and Hessian", "uso": "Definição formal da matriz Hessiana e aproximações de Taylor de 2ª ordem"},
            {"obra": "Goodfellow, Bengio & Courville. Deep Learning", "trecho": "Capítulo 4.3: Beyond the Gradient: Jacobians and Hessians", "uso": "Análise da inviabilidade de métodos de Newton e proliferação de pontos de sela"}
        ]
    },

    # =========================================================================
    # TÓPICO 18: Algoritmo de Descida do Gradiente (Vanilla Gradient Descent)
    # =========================================================================
    "Algoritmo de Descida do Gradiente (Vanilla Gradient Descent)": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Toda a inteligência do ChatGPT, do Gemini e dos carros autônomos se resume a uma única equação matemática repetida bilhões de vezes: $\mathbf{w} \leftarrow \mathbf{w} - \eta \nabla L$. Como essa linha de código aparentemente singela consegue ajustar bilhões de conexões sinápticas artificiais para aprender conceitos humanos complexos?""",
        "prerequisitos": [
            "Vetor gradiente $\nabla f$ (Tópico 16)",
            "Multiplicação de vetor por escalar (Tópico 1)"
        ],
        "objetivos": [
            "compreender o algoritmo de Descida do Gradiente passo a passo e seu hiperparâmetro $\eta$ (learning rate);",
            "comparar as três variantes práticas: Batch GD, Stochastic GD (SGD) e Mini-batch GD;",
            "entender por que GPUs e Tensor Cores tornaram o Mini-batch GD o padrão da indústria de IA."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Equação que Move a IA",
                "titulo": "A Anatomia da Atualização de Pesos",
                "corpo": r"""<p>A Descida do Gradiente é um algoritmo iterativo de otimização de primeira ordem. Sua regra de atualização é:</p>
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \eta \nabla L(\mathbf{w}_t)$$
<p>Cada símbolo desempenha um papel cirúrgico:</p>
<ul>
<li>$\mathbf{w}_t$: O vetor de pesos atual no instante $t$.</li>
<li>$\nabla L(\mathbf{w}_t)$: O vetor gradiente, indicando para onde a perda sobe mais rápido.</li>
<li>O sinal de menos ($-$): Garante que andamos no sentido oposto ao gradiente, descendo a montanha de erro.</li>
<li>$\eta$ (eta): A <b>taxa de aprendizado (learning rate)</b>, um número escalar positivo que controla o tamanho do passo que damos a cada iteração.</li>
</ul>""",
            },
            {
                "tipo": "tabela",
                "titulo": "As Três Variantes de Descida do Gradiente",
                "cabecalho": ["Modalidade", "Quantos dados por passo?", "Prós", "Contras"],
                "linhas": [
                    ["Batch GD (Full)", "Todo o dataset de treino", "Gradiente matematicamente exato e trajetória estável", "Impossível colocar terabytes de dados na GPU; cada passo demora horas"],
                    ["Stochastic GD (SGD)", "1 único exemplo aleatório", "Cálculo instantâneo, baixo uso de memória, ruído ajuda a pular vales rasos", "Trajetória caótica em zigue-zague, não aproveita o paralelismo de matrizes da GPU"],
                    ["Mini-batch GD (Padrão)", "Um lote pequeno (32 a 4.096 exemplos)", "Trajetória suave e satura o paralelismo maciço dos Tensor Cores das GPUs", "Exige calibrar o hiperparâmetro do tamanho de lote (batch size)"]
                ]
            },
            {
                "tipo": "passos",
                "titulo": "Calculando 3 Passos de Descida do Gradiente à Mão",
                "corpo": r"""<p>Vamos minimizar a perda quadrática simples $L(w) = (w - 3)^2$, cujo mínimo evidente é $w^* = 3$. Começamos em $w_0 = 0.0$ com taxa $\eta = 0.2$:</p>""",
                "passos": [
                    {
                        "faca": r"Obtenha a fórmula do gradiente: $$\frac{dL}{dw} = 2(w - 3)$$",
                        "porque": "Aplicamos a regra da potência e cadeia em $(w-3)^2$."
                    },
                    {
                        "faca": r"Passo 1: Em $w_0 = 0.0$, o gradiente é $2(0 - 3) = -6.0$. $$w_1 = 0.0 - 0.2(-6.0) = 0.0 + 1.2 = 1.2$$ Perda inicial $L(0) = 9.0 \implies L(1.2) = (1.2 - 3)^2 = (-1.8)^2 = 3.24$.",
                        "porque": "O gradiente negativo indicou que deveríamos andar para a direita (+)."
                    },
                    {
                        "faca": r"Passo 2: Em $w_1 = 1.2$, o gradiente é $2(1.2 - 3) = 2(-1.8) = -3.6$. $$w_2 = 1.2 - 0.2(-3.6) = 1.2 + 0.72 = 1.92$$ Nova perda $L(1.92) = (1.92 - 3)^2 = (-1.08)^2 = 1.1664$.",
                        "porque": "O gradiente encolheu espontaneamente de $-6.0$ para $-3.6$ conforme nos aproximamos do vale!"
                    },
                    {
                        "faca": r"Passo 3: Em $w_2 = 1.92$, o gradiente é $2(1.92 - 3) = -2.16$. $$w_3 = 1.92 - 0.2(-2.16) = 1.92 + 0.432 = 2.352$$ Nova perda $L(2.352) = (2.352 - 3)^2 = (-0.648)^2 = 0.4199$.",
                        "porque": "A cada passo o erro cai dramaticamente: $9.0 \to 3.24 \to 1.17 \to 0.42$!"
                    }
                ],
                "conclusao": r"Em apenas 3 passos simples, o peso saltou de $0.0$ para $2.352$, aproximando-se velozmente do alvo perfeito $3.0$ sem nenhum raciocínio mágico: pura aritmética vetorial!"
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Mini-batch Gradient Descent Completo",
                "codigo": r'''import numpy as np

# Criando dados sintéticos: y = 3*x + 2 + ruído
np.random.seed(42)
N = 100
X = np.random.uniform(-3, 3, size=(N, 1))
y = 3.0 * X + 2.0 + np.random.normal(0, 0.2, size=(N, 1))

# Inicializando parâmetros: peso w e viés b
w = np.random.randn(1, 1)
b = 0.0

eta = 0.05
batch_size = 20
epocas = 15

print(f"Pesos iniciais: w = {w.item():.3f}, b = {b:.3f}")

# Loop de treino com Mini-batch GD
for epoca in range(epocas):
    indices = np.random.permutation(N)
    X_shuffled = X[indices]
    y_shuffled = y[indices]
    
    for i in range(0, N, batch_size):
        xb = X_shuffled[i:i+batch_size]
        yb = y_shuffled[i:i+batch_size]
        
        # Forward pass
        pred = xb @ w + b
        erro = pred - yb
        
        # Gradientes médios do mini-batch
        grad_w = (2.0 / len(xb)) * (xb.T @ erro)
        grad_b = (2.0 / len(xb)) * np.sum(erro)
        
        # Atualização
        w -= eta * grad_w
        b -= eta * grad_b

loss_final = np.mean((X @ w + b - y)**2)
print(f"Treino concluído! w = {w.item():.3f} (alvo: 3.0), b = {b:.3f} (alvo: 2.0)")
print(f"MSE final: {loss_final:.4f}")
assert abs(w.item() - 3.0) < 0.1, "O peso w deveria ter convergido próximo de 3.0"''',
                "experimentos": [
                    "Modifique o tamanho do batch para <code>batch_size = 1</code> (SGD puro) e observe como a trajetória oscila mais, exigindo diminuir o eta.",
                    "Experimente colocar <code>eta = 0.8</code> e veja o cálculo transbordar para NaN por ultrapassagem violenta do mínimo (overshooting)."
                ]
            }
        ],
        "resumo": [
            "A Descida do Gradiente atualiza pesos na direção oposta ao gradiente multiplicada pela taxa de aprendizado.",
            "O Mini-batch GD equilibra a fidelidade estocástica com a máxima eficiência de processamento paralelo em GPUs modernas.",
            "Conforme os pesos se aproximam do mínimo, a inclinação diminui e os passos desaceleram organicamente."
        ],
        "proxima": r"Embora o Vanilla GD seja elegante, ele patina em ravinas e vales estreitos. Para superar isso, a IA inventou otimizadores com memória: Momentum, RMSprop e Adam.",
        "referencias": [
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Capítulo 7.1: Gradient Descent", "uso": "Análise matemática de convergência e taxas de contração"},
            {"obra": "Goodfellow, Bengio & Courville. Deep Learning", "trecho": "Capítulo 8.1: How Learning Differs from Pure Optimization", "uso": "Diferença entre otimização teórica e generalização via Mini-batch SGD"}
        ]
    },

    # =========================================================================
    # TÓPICO 19: Otimizadores modernos: Momentum, RMSprop e Adam
    # =========================================================================
    "Otimizadores modernos: Momentum, RMSprop e Adam": {
        "v": 2,
        "duracao": 35,
        "gancho": r"""Se você soltar uma bola de boliche no alto de um desfiladeiro íngreme, ela não para a cada centímetro para recalcular a direção: ela ganha <b>inércia (momentum)</b>, atravessa lombadas e desce direto para o fundo do vale. Por que o <b>Adam</b>, ao misturar a inércia da Física com a calibragem individual de cada coordenada do RMSprop, tornou-se o otimizador soberano no treino de todos os grandes modelos de linguagem?""",
        "prerequisitos": [
            "Descida do Gradiente e vetor gradiente (Tópicos 16 e 18)",
            "Médias ponderadas móveis"
        ],
        "objetivos": [
            "entender a analogia física do Momentum e como ele cancela oscilações em ravinas;",
            "compreender o RMSprop e sua adaptação de escala por coordenada;",
            "dominar as equações completas do Adam, incluindo a correção de viés dos momentos de 1ª e 2ª ordem."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "O Problema das Ravinas",
                "titulo": "Por que o gradiente simples patina?",
                "corpo": r"""<p>Em superfícies reais de perda, a curvatura raramente é uma tigela perfeitamente redonda. Quase sempre ela se parece com um <b>desfiladeiro estreito (ravina)</b>: as paredes laterais são extremamente íngremes, mas o fundo do vale tem uma inclinação quase plana que leva ao objetivo.</p>
<p>O gradiente simples comete um erro primário: ele é dominado pela parede íngreme, fazendo os pesos quicarem desesperadamente de um lado para o outro do desfiladeiro, avançando quase nada ao longo do leito do vale!</p>""",
            },
            {
                "tipo": "visual",
                "titulo": "Trajetória: SGD vs. Otimizadores com Inércia",
                "corpo": r"""<p>Veja o contraste entre a oscilação ineficiente do SGD e a descida focada de algoritmos com memória:</p>""",
                "svg": SVG_OTIMIZADORES,
                "legenda": "O SGD gasta energia quicando entre as paredes íngremes. Momentum e Adam amortecem as oscilações transversais e aceleram ao longo do leito do vale.",
            },
            {
                "tipo": "passos",
                "titulo": "A Evolução Matemática em Três Etapas",
                "corpo": r"""<p>Acompanhe como a comunidade de IA construiu o Adam resolvendo uma limitação por vez:</p>""",
                "passos": [
                    {
                        "faca": r"Etapa 1: Adicionar Inércia Física (Momentum) $$\mathbf{v}_t = \beta_1 \mathbf{v}_{t-1} + (1 - \beta_1) \mathbf{g}_t, \quad \mathbf{w}_{t+1} = \mathbf{w}_t - \eta \mathbf{v}_t$$",
                        "porque": "Como os gradientes perpendiculares alternam de sinal (+ e -), sua média móvel $\mathbf{v}_t$ se cancela para zero! Já os gradientes ao longo do vale têm sempre o mesmo sinal e se somam com força."
                    },
                    {
                        "faca": r"Etapa 2: Escalonamento Adaptativo por Coordenada (RMSprop) $$\mathbf{s}_t = \beta_2 \mathbf{s}_{t-1} + (1 - \beta_2) \mathbf{g}_t^2, \quad \mathbf{w}_{t+1} = \mathbf{w}_t - \frac{\eta}{\sqrt{\mathbf{s}_t} + \epsilon} \mathbf{g}_t$$",
                        "porque": "Se uma coordenada tem gradientes gigantescos, dividimos por $\sqrt{\mathbf{s}_t}$ para acalmar o passo. Se tem gradientes tímidos, dividimos por um número minúsculo para amplificar o passo!"
                    },
                    {
                        "faca": r"Etapa 3: A Fusão Suprema (Adam - Adaptive Moment Estimation) $$\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1 - \beta_1) \mathbf{g}_t \quad (\text{1º momento: direção com inércia})$$ $$\mathbf{v}_t = \beta_2 \mathbf{v}_{t-1} + (1 - \beta_2) \mathbf{g}_t^2 \quad (\text{2º momento: escala de curvatura})$$",
                        "porque": "O Adam combina o melhor dos dois mundos: direção suave do Momentum + passos calibrados por coordenada do RMSprop."
                    },
                    {
                        "faca": r"Etapa 4: Correção de Viés Inicial (Bias Correction) $$\hat{\mathbf{m}}_t = \frac{\mathbf{m}_t}{1 - \beta_1^t}, \quad \hat{\mathbf{v}}_t = \frac{\mathbf{v}_t}{1 - \beta_2^t}$$ $$\mathbf{w}_{t+1} = \mathbf{w}_t - \frac{\eta}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon} \hat{\mathbf{m}}_t$$",
                        "porque": "Como $\mathbf{m}_0$ e $\mathbf{v}_0$ começam em zero, nos primeiros passos eles são artificialmente puxados para zero. Dividir por $(1 - \beta^t)$ corrige perfeitamente esse viés nas primeiras iterações!"
                    }
                ],
                "conclusao": r"Os hiperparâmetros padrão propostos por Kingma & Ba (2014) são usados até hoje no treinamento dos maiores LLMs do mundo: $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$."
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Otimizador Adam Implementado do Zero",
                "codigo": r'''import numpy as np

# Função de ravina íngreme: f(x, y) = 0.1*x^2 + 2.0*y^2
def loss_ravina(w):
    return 0.1 * w[0]**2 + 2.0 * w[1]**2

def grad_ravina(w):
    return np.array([0.2 * w[0], 4.0 * w[1]])

# Algoritmo Adam do zero
def treinar_adam(passos=30, eta=0.3, beta1=0.9, beta2=0.999, eps=1e-8):
    w = np.array([5.0, 5.0]) # Ponto inicial distante
    m = np.zeros_like(w)
    v = np.zeros_like(w)
    
    trajetoria = [w.copy()]
    for t in range(1, passos + 1):
        g = grad_ravina(w)
        
        # Atualização dos momentos
        m = beta1 * m + (1.0 - beta1) * g
        v = beta2 * v + (1.0 - beta2) * (g ** 2)
        
        # Correção de viés
        m_hat = m / (1.0 - beta1 ** t)
        v_hat = v / (1.0 - beta2 ** t)
        
        # Passo de atualização
        w -= (eta / (np.sqrt(v_hat) + eps)) * m_hat
        trajetoria.append(w.copy())
        
    return w, loss_ravina(w)

w_final, perda_final = treinar_adam()
print(f"Ponto final após 30 passos de Adam: w = [{w_final[0]:.4f}, {w_final[1]:.4f}]")
print(f"Perda final: {perda_final:.6f} (quase zero absoluto!)")
assert perda_final < 0.05, "Adam deveria ter descido a ravina com facilidade!"''',
                "experimentos": [
                    "Compare o resultado desativando a inércia (fazendo <code>beta1 = 0.0</code>) e veja como a coordenada $x$ plana demora muito mais para convergir.",
                    "Experimente remover o termo $\epsilon = 10^{-8}$ e observe o perigo iminente de divisão por zero quando o gradiente é estritamente nulo."
                ]
            }
        ],
        "resumo": [
            "Momentum introduz inércia física que cancela zigue-zagues em direções ortogonais e acelera ao longo de vales de baixa inclinação.",
            "RMSprop normaliza o tamanho do passo dividindo pela raiz da média dos gradientes ao quadrado de cada coordenada.",
            "O Adam unifica Momentum e RMSprop com correção matemática de viés, sendo o padrão absoluto para treinar redes profundas e LLMs."
        ],
        "proxima": r"Mesmo com um otimizador poderoso como o Adam, como escolher a velocidade ideal do treino? No próximo tópico, desvendaremos o mistério do Learning Rate Scheduling e dos Pontos de Sela.",
        "referencias": [
            {"obra": "Kingma & Ba (2014). Adam: A Method for Stochastic Optimization", "trecho": "Paper seminal (ICLR)", "uso": "Dedução da correção de viés e formulação original do algoritmo"},
            {"obra": "Goodfellow, Bengio & Courville. Deep Learning", "trecho": "Capítulo 8.5: Algorithms with Adaptive Learning Rates", "uso": "Comparativo conceitual de AdaGrad, RMSprop e Adam"}
        ]
    },

    # =========================================================================
    # TÓPICO 20: Taxa de aprendizado, convergência e pontos de sela
    # =========================================================================
    "Taxa de aprendizado (Learning Rate), convergência e pontos de sela": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Se a taxa de aprendizado for $10^{-6}$, seu modelo levará 1.000 anos e milhões de dólares de GPU para aprender. Se for $1.0$, a perda explodirá para `NaN` no primeiro segundo. Além disso, em espaços de 1 bilhão de dimensões, por que o maior medo de um cientista de dados não são os mínimos locais, mas a proliferação avassaladora de <b>pontos de sela</b>?""",
        "prerequisitos": [
            "Descida do Gradiente e otimizador Adam (Tópicos 18 e 19)",
            "Matriz Hessiana e autovalores (Tópicos 10 e 17)"
        ],
        "objetivos": [
            "compreender o impacto crítico do hiperparâmetro de Taxa de Aprendizado (Learning Rate);",
            "dominar estratégias de escalonamento: Warmup linear e Cosine Decay Schedule;",
            "provar por que pontos de sela dominam exponencialmente sobre mínimos locais em alta dimensionalidade (Dauphin et al., 2014)."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "O Dilema da Velocidade",
                "titulo": "Os Quatro Comportamentos do Learning Rate",
                "corpo": r"""<p>A taxa de aprendizado $\eta$ dita a magnitude de cada passo no espaço de parâmetros. Andrew Ng costuma descrevê-la como o hiperparâmetro mais importante de toda a rede neural:</p>
<ul>
<li><b>Muito Baixa ($\eta = 10^{-6}$):</b> A convergência é linearmente desesperadora. A perda parece não se mover e o modelo pode ficar preso em regiões quase planas.</li>
<li><b>Baixa Adequada:</b> Convergência lenta, porém garantida e sem oscilações bruscas.</li>
<li><b>Ótima:</b> Queda rápida e estável em direção ao fundo do vale, estabilizando na solução ótima.</li>
<li><b>Muito Alta ($\eta = 1.0$):</b> Ultrapassagem catastrófica (overshooting). O passo é tão grande que salta por cima do vale e aterrissa na parede oposta em uma altura ainda maior, divergindo para o infinito (`NaN`).</li>
</ul>""",
            },
            {
                "tipo": "texto",
                "rotulo": "Agendamento Moderno",
                "titulo": "Warmup e Decaimento Cosseno (Cosine Decay)",
                "corpo": r"""<p>Em modelos modernos como LLaMA e GPT, a taxa de aprendizado <b>nunca é mantida fixa</b> durante o treino. Ela segue uma curva cuidadosamente coreografada:</p>
<ol>
<li><b>Learning Rate Warmup (Aquecimento):</b> Nos primeiros milhares de passos, a taxa começa em quase zero e sobe linearmente até o valor máximo. <i>Por quê?</i> No início do treino, com pesos aleatórios, os gradientes são caóticos e instáveis. O warmup impede que passos gigantescos destruam a inicialização do modelo antes que a atenção se estabilize.</li>
<li><b>Cosine Annealing (Decaimento Cosseno):</b> Após o pico, a taxa diminui suavemente seguindo uma curva de cosseno até $10\%$ ou $1\%$ do valor máximo, permitindo que os pesos se acomodem com extrema precisão no fundo dos vales mais profundos.</li>
</ol>""",
            },
            {
                "tipo": "pense",
                "titulo": "O Mistério dos Mínimos Locais em 1.000 Dimensões",
                "pergunta": r"""Em 1 dimensão, uma função pode facilmente ter vários mínimos locais onde uma bolinha fica presa. Por que em um espaço de 1.000 dimensões (ou 1 bilhão) é virtualmente impossível ficar preso em um mínimo local ruim?""",
                "resposta": r"""<p>Para um ponto ser um <b>mínimo local</b>, todas as direções precisam curvar para cima simultaneamente. Se supusermos que cada direção tem 50% de chance de curvar para cima e 50% de curvar para baixo:</p>
<ul>
<li>Em 1 dimensão: probabilidade de ser mínimo local = $\frac{1}{2} = 50\%$.</li>
<li>Em 10 dimensões: $(\frac{1}{2})^{10} = \frac{1}{1024} \approx 0.09\%$.</li>
<li>Em 1.000 dimensões: $(\frac{1}{2})^{1000} \approx 10^{-301}$ (um zero seguido de 300 zeros antes do 1!).</li>
</ul>
<p>Em alta dimensão, quase todo ponto estacionário com gradiente zero tem várias direções que curvam para cima e várias que curvam para baixo: ele é obrigatoriamente um <b>Ponto de Sela</b>! O otimizador quase sempre encontra uma rota de escape para continuar descendo.</p>"""
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Implementando Cosine Annealing com Warmup",
                "codigo": r'''import numpy as np

def get_lr(passo, total_passos, warmup_passos, lr_max=1e-3, lr_min=1e-5):
    # 1. Fase de Warmup Linear
    if passo < warmup_passos:
        return lr_max * (passo / warmup_passos)
    
    # 2. Fase de Decaimento Cosseno
    progresso = (passo - warmup_passos) / (total_passos - warmup_passos)
    fator_cosseno = 0.5 * (1.0 + np.cos(np.pi * progresso))
    return lr_min + (lr_max - lr_min) * fator_cosseno

# Simulando um treino de 1000 passos com 100 passos de warmup
passos_teste = [0, 50, 100, 300, 550, 800, 1000]
print("Curva de Learning Rate no estilo Transformer:")
for p in passos_teste:
    lr = get_lr(p, total_passos=1000, warmup_passos=100, lr_max=3e-4)
    print(f"Passo {p:4d}: LR = {lr:.6f}")''',
                "experimentos": [
                    "Observe como no passo 0 a taxa começa em 0.0, atinge exatamente o pico de 0.000300 no passo 100, e desacelera suavemente até o final.",
                    "Plote mentalmente a curva: ela evita os choques violentos de gradiente da inicialização aleatória."
                ]
            },
            {
                "tipo": "armadilhas",
                "titulo": "Armadilhas de Treinamento",
                "itens": [
                    {"erro": "Usar uma taxa de aprendizado fixa durante todo o ciclo de treino de um Transformer.", "correcao": "Sempre utilize um scheduler com Warmup e Cosine Decay. Sem warmup, as primeiras camadas de atenção frequentemente divergem."},
                    {"erro": "Achar que a perda precisa diminuir monotonicamente a cada lote.", "correcao": "No Mini-batch SGD e no Adam, a perda estocástica flutua naturalmente entre lotes. O que deve diminuir de forma consistente é a média móvel da perda ao longo das épocas."}
                ]
            }
        ],
        "resumo": [
            "A taxa de aprendizado calibra a velocidade e a estabilidade da convergência em direção à perda mínima.",
            "Estratégias de Warmup + Cosine Decay são obrigatórias em LLMs para estabilizar a inicialização e refinar a convergência.",
            "Em alta dimensionalidade, a probabilidade matemática de mínimos locais ruins cai para zero, enquanto pontos de sela predominam."
        ],
        "proxima": r"Concluímos a jornada do Cálculo e Otimização! No próximo módulo, adentraremos o universo da Probabilidade e Estatística, a linguagem da incerteza que fundamenta os modelos generativos.",
        "referencias": [
            {"obra": "Dauphin et al. (2014). Identifying and attacking the saddle point problem in high-dimensional non-convex optimization", "trecho": "Paper NIPS", "uso": "Prova empírica e teórica da dominância de pontos de sela em redes profundas"},
            {"obra": "Loshchilov & Hutter (2017). SGDR: Stochastic Gradient Descent with Warm Restarts", "trecho": "Paper ICLR", "uso": "Fundamentação do decaimento cosseno da taxa de aprendizado"}
        ]
    }
}
