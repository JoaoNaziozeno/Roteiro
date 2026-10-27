# -*- coding: utf-8 -*-
"""
Aulas-piloto no formato Aula Visual v2 (proposta para aprovação).

Personagem recorrente da trilha: o "Classificador de Avaliações" de uma cafeteria.
Ele aparece em várias aulas com os MESMOS números, para o aluno ver a mesma
peça de IA ganhando camadas de matemática ao longo da jornada:
  embeddings 2D de brinquedo  ->  eixo 1 = positividade, eixo 2 = intensidade
  ótimo = [3, 2]   bom = [2, 1]   ruim = [-2, 1]   péssimo = [-3, 2]

Todos os números destas aulas foram conferidos por script.
Strings em r'''...''' (raw) para escrever LaTeX com uma única barra.
"""

# -------------------------------------------------------------------------
# SVGs (usam apenas classes do LESSON_V2_CSS, então seguem o tema claro/escuro)
# -------------------------------------------------------------------------
_ARROW_DEFS = r"""<defs>
<marker id="{id}t" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="sv-fill"/></marker>
<marker id="{id}m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="sv-fillm"/></marker>
</defs>"""


def _defs(prefix):
    return _ARROW_DEFS.replace("{id}", prefix)


SVG_PROJECAO = r"""<svg viewBox="0 0 320 232" class="lv2-svg" role="img" aria-label="Projeção do vetor w sobre o vetor v">""" + _defs("pj") + r"""
<line x1="20" y1="190" x2="300" y2="190" class="sv-ax"/><line x1="40" y1="212" x2="40" y2="22" class="sv-ax"/>
<line x1="160" y1="70" x2="160" y2="190" class="sv-thin sv-dash"/>
<polyline points="150,190 150,180 160,180" class="sv-thin"/>
<line x1="40" y1="190" x2="200" y2="190" class="sv-b" marker-end="url(#pjm)"/>
<line x1="40" y1="190" x2="160" y2="70" class="sv-a" marker-end="url(#pjt)"/>
<path d="M68,190 A28,28 0 0,0 59.8,170.2" class="sv-thin"/>
<text x="72" y="180" class="sv-tm">θ = 45°</text>
<text x="166" y="66" class="sv-t">w = [3, 3]</text>
<text x="206" y="186" class="sv-tm">v = [4, 0]</text>
<line x1="40" y1="204" x2="160" y2="204" class="sv-a"/><line x1="40" y1="199" x2="40" y2="209" class="sv-a"/><line x1="160" y1="199" x2="160" y2="209" class="sv-a"/>
<text x="100" y="224" text-anchor="middle" class="sv-t">sombra de w sobre v = 3</text>
<text x="166" y="134" class="sv-tm sv-it">luz vinda de cima ↓</text>
</svg>"""

SVG_EMBEDDINGS = r"""<svg viewBox="0 0 340 222" class="lv2-svg" role="img" aria-label="Embeddings de brinquedo de quatro palavras no plano">""" + _defs("em") + r"""
<line x1="10" y1="190" x2="330" y2="190" class="sv-ax"/><line x1="170" y1="205" x2="170" y2="40" class="sv-ax"/>
<text x="330" y="208" text-anchor="end" class="sv-tm">positividade →</text>
<text x="176" y="48" class="sv-tm">intensidade ↑</text>
<line x1="170" y1="190" x2="290" y2="110" class="sv-a" marker-end="url(#emt)"/>
<line x1="170" y1="190" x2="250" y2="150" class="sv-a" marker-end="url(#emt)"/>
<line x1="170" y1="190" x2="90" y2="150" class="sv-b sv-dash" marker-end="url(#emm)"/>
<line x1="170" y1="190" x2="50" y2="110" class="sv-b sv-dash" marker-end="url(#emm)"/>
<text x="294" y="104" class="sv-t">ótimo [3, 2]</text>
<text x="256" y="152" class="sv-t">bom [2, 1]</text>
<text x="86" y="144" text-anchor="end" class="sv-tm">ruim [−2, 1]</text>
<text x="46" y="102" text-anchor="start" class="sv-tm">péssimo [−3, 2]</text>
</svg>"""

SVG_GRAFO = r"""<svg viewBox="0 0 640 214" class="lv2-svg" role="img" aria-label="Grafo computacional de um neurônio com valores e gradientes">""" + _defs("gc") + r"""
<rect x="16" y="30" width="64" height="28" rx="7" class="sv-node"/><text x="48" y="49" text-anchor="middle" class="sv-t">x = 2</text>
<rect x="16" y="100" width="64" height="28" rx="7" class="sv-node"/><text x="48" y="119" text-anchor="middle" class="sv-t">w = 0,5</text>
<circle cx="150" cy="80" r="20" class="sv-node"/><text x="150" y="85" text-anchor="middle" class="sv-t">×</text>
<line x1="80" y1="44" x2="132" y2="71" class="sv-thin" marker-end="url(#gcm)"/>
<line x1="80" y1="114" x2="132" y2="89" class="sv-thin" marker-end="url(#gcm)"/>
<circle cx="270" cy="80" r="20" class="sv-node"/><text x="270" y="85" text-anchor="middle" class="sv-t">+</text>
<rect x="238" y="150" width="64" height="28" rx="7" class="sv-node"/><text x="270" y="169" text-anchor="middle" class="sv-t">b = −0,5</text>
<line x1="270" y1="150" x2="270" y2="102" class="sv-thin" marker-end="url(#gcm)"/>
<line x1="170" y1="80" x2="248" y2="80" class="sv-thin" marker-end="url(#gcm)"/>
<text x="209" y="70" text-anchor="middle" class="sv-t">wx = 1</text>
<circle cx="390" cy="80" r="20" class="sv-node"/><text x="390" y="85" text-anchor="middle" class="sv-t">σ</text>
<line x1="290" y1="80" x2="368" y2="80" class="sv-thin" marker-end="url(#gcm)"/>
<text x="329" y="70" text-anchor="middle" class="sv-t">z = 0,5</text>
<rect x="490" y="62" width="112" height="36" rx="8" class="sv-node"/><text x="546" y="85" text-anchor="middle" class="sv-t">½(a − y)²</text>
<rect x="514" y="150" width="64" height="28" rx="7" class="sv-node"/><text x="546" y="169" text-anchor="middle" class="sv-t">y = 1</text>
<line x1="546" y1="150" x2="546" y2="100" class="sv-thin" marker-end="url(#gcm)"/>
<line x1="410" y1="80" x2="488" y2="80" class="sv-thin" marker-end="url(#gcm)"/>
<text x="449" y="70" text-anchor="middle" class="sv-t">a = 0,622</text>
<text x="546" y="52" text-anchor="middle" class="sv-t">L = 0,0713</text>
<text x="449" y="104" text-anchor="middle" class="sv-tm sv-it">∂L/∂a = −0,378</text>
<text x="329" y="104" text-anchor="middle" class="sv-tm sv-it">∂L/∂z = −0,0887</text>
<text x="209" y="104" text-anchor="middle" class="sv-tm sv-it">∂L/∂(wx) = −0,0887</text>
<text x="88" y="146" class="sv-tm sv-it">∂L/∂w = −0,177</text>
<text x="280" y="136" class="sv-tm sv-it">∂L/∂b = −0,0887</text>
<text x="320" y="206" text-anchor="middle" class="sv-tm">em cima: valores calculados na ida (forward) · em itálico, embaixo: gradientes calculados na volta (backward)</text>
</svg>"""


LESSONS_V2_SAMPLES = {

# =========================================================================
# AULA 3 — PRODUTO ESCALAR
# Formato: do concreto (supermercado) -> geometria (sombra) -> IA (embeddings, neurônio)
# =========================================================================
"Produto escalar (Dot Product) e projeções": {
    "v": 2,
    "duracao": 25,
    "gancho": r"""Como um computador decide que <b>“ótimo”</b> está mais perto de <b>“bom”</b> do que de <b>“péssimo”</b>, se tudo o que ele enxerga são listas de números? A resposta cabe em uma única operação, a mesma que cada neurônio de uma rede executa bilhões de vezes por segundo.""",
    "prerequisitos": [
        "Aula 1: um vetor é uma lista de números e também uma seta.",
        "Aula 2: combinação linear, ou seja, multiplicar cada parte por um peso e somar tudo.",
    ],
    "objetivos": [
        "calcular um produto escalar e dizer o que o número obtido significa;",
        "interpretar o sinal do resultado (positivo, zero ou negativo) como concordância de direção;",
        "calcular a projeção, a “sombra” de um vetor sobre outro;",
        "reconhecer o produto escalar dentro de um neurônio, de uma busca semântica e da atenção dos Transformers.",
    ],
    "blocos": [
        {
            "tipo": "texto",
            "rotulo": "Começando pelo concreto",
            "titulo": "Você já faz produto escalar no supermercado",
            "corpo": r"""<p>Você comprou 2 pães, 3 litros de leite e 1 pacote de café. Os preços são 1,50, 4,00 e 12,00 reais. Quanto deu a conta?</p>
<p>Você multiplica <b>cada quantidade pelo preço correspondente</b> e soma tudo:</p>
$$2 \times 1{,}5 \;+\; 3 \times 4 \;+\; 1 \times 12 \;=\; 3 + 12 + 12 \;=\; 27$$
<p>Agora repare na estrutura. Existem duas listas, as quantidades $[2,\,3,\,1]$ e os preços $[1{,}5,\;4,\;12]$, e uma regra: <b>multiplique par a par e some</b>. Isso é exatamente o <b>produto escalar</b>. O resultado é um único número, um <i>escalar</i>, e daí vem o nome. Em inglês ele se chama <i>dot product</i> por causa do ponto ($\cdot$) usado para escrevê-lo.</p>
<p>Guarde esta leitura, porque ela vai voltar no fim da aula: <b>o produto escalar é um total ponderado</b>. Uma lista diz “quanto tem de cada coisa”, e a outra diz “quanto vale cada coisa”.</p>""",
        },
        {
            "tipo": "notacao",
            "titulo": "A mesma conta, na língua dos livros",
            "corpo": r"""<p>Agora que você já fez a conta, veja como os livros escrevem exatamente a mesma coisa:</p>
$$\vec{u} \cdot \vec{v} \;=\; \sum_{i=1}^{n} u_i\, v_i \;=\; u_1 v_1 + u_2 v_2 + \dots + u_n v_n$$
<p>Parece assustador, mas cada pedaço é uma instrução simples:</p>""",
            "itens": [
                {"simbolo": r"$\vec{u}\cdot\vec{v}$", "leitura": "u escalar v (ou “u ponto v”)",
                 "significado": "O produto escalar entre os vetores $\\vec u$ e $\\vec v$. A setinha em cima indica que a letra representa um vetor, e não um número."},
                {"simbolo": r"$u_i$", "leitura": "u índice i", "significado": "O componente que está na posição $i$ do vetor $\\vec u$. No supermercado, $u_2 = 3$ (litros de leite)."},
                {"simbolo": r"$\sum_{i=1}^{n}$", "leitura": "somatório de i igual a 1 até n",
                 "significado": "Uma instrução de repetição: faça a conta da direita para $i = 1, 2, \\dots, n$ e some os resultados. É um laço <code>for</code> escrito em uma linha."},
                {"simbolo": r"$n$", "leitura": "ene", "significado": "Quantos componentes cada vetor tem. Os dois vetores precisam ter o mesmo $n$, senão sobra alguém sem par."},
                {"simbolo": r"$\mathbf{u}^{\top}\mathbf{v}$", "leitura": "u transposto vezes v",
                 "significado": "Outra forma de escrever o mesmo produto, comum em Strang, Goodfellow e nos artigos de IA. Você vai entender o “transposto” ($^{\\top}$) na aula de matrizes. Por enquanto, saiba que é sinônimo de $\\vec u \\cdot \\vec v$."},
            ],
        },
        {
            "tipo": "visual",
            "rotulo": "A ideia geométrica",
            "titulo": "Quanto um vetor “anda” na direção do outro?",
            "corpo": r"""<p>A conta algébrica é fácil, mas o que ela <i>significa</i> geometricamente? Imagine o sol a pino sobre a reta do vetor $\vec v$. O vetor $\vec w$ projeta uma <b>sombra</b> sobre essa reta:</p>""",
            "svg": SVG_PROJECAO,
            "legenda": "A sombra de w = [3, 3] sobre a direção de v = [4, 0] mede 3 unidades.",
            "depois": r"""<p>O produto escalar responde: <b>(comprimento da sombra) × (comprimento de $\vec v$)</b>. Aqui a sombra mede 3 e $\vec v$ mede 4, então o resultado é $3 \times 4 = 12$.</p>
<p>Agora faça a conta algébrica: $\vec v \cdot \vec w = 4 \times 3 + 0 \times 3 = 12$. <b>As duas contas dão o mesmo resultado.</b> Essa coincidência, que Strang destaca logo no primeiro capítulo do livro, é o que torna o produto escalar tão poderoso: uma regra mecânica de multiplicar e somar carrega uma informação geométrica sobre ângulos.</p>
<p>A forma geral dessa ligação é:</p>
$$\vec u \cdot \vec v \;=\; \|\vec u\|\;\|\vec v\|\;\cos\theta$$
<p>Leia $\|\vec u\|$ como “norma de u”, ou seja, o <b>comprimento</b> da seta, calculado por Pitágoras (a aula 4 trata disso com calma). $\theta$ é a letra grega <i>teta</i>, usada para o ângulo entre os vetores. O $\cos\theta$ funciona como um medidor de alinhamento: vale $1$ quando os vetores apontam para o mesmo lado, $0$ quando são perpendiculares e $-1$ quando apontam para lados opostos.</p>
<p>Conferindo: $\|\vec v\| = 4$, $\|\vec w\| = \sqrt{3^2+3^2} = \sqrt{18} \approx 4{,}243$ e $\cos 45^\circ \approx 0{,}7071$. Multiplicando, $4 \times 4{,}243 \times 0{,}7071 \approx 12{,}0$. ✓</p>""",
        },
        {
            "tipo": "tabela",
            "titulo": "O sinal conta uma história",
            "corpo": r"""<p>Na prática, quase nunca calculamos o ângulo. Olhamos direto para o <b>sinal</b> do produto escalar:</p>""",
            "cabecalho": ["Ângulo θ", "cos θ", "Produto escalar", "Exemplo", "Leitura"],
            "linhas": [
                [r"menor que 90°", "positivo", r"$> 0$", r"$[4,0]\cdot[3,3] = 12$", "apontam para o mesmo lado e concordam"],
                [r"exatamente 90°", "zero", r"$= 0$", r"$[1,2]\cdot[2,-1] = 2 - 2 = 0$", "perpendiculares (ortogonais): não compartilham nenhuma direção"],
                [r"maior que 90°", "negativo", r"$< 0$", r"$[4,0]\cdot[-3,3] = -12$", "apontam para lados opostos e discordam"],
            ],
        },
        {
            "tipo": "pense",
            "pergunta": r"""Se você dobrar o tamanho de $\vec w$, passando de $[3,3]$ para $[6,6]$, o que acontece com o produto escalar $\vec v \cdot \vec w$? E com o ângulo entre eles?""",
            "resposta": r"""<p>O produto escalar <b>dobra</b>: $4 \times 6 + 0 \times 6 = 24$, porque cada termo da soma dobrou. O ângulo <b>não muda</b> e continua em 45°, porque a direção da seta é a mesma.</p>
<p>Essa é uma descoberta importante. O produto escalar mistura duas informações, <b>alinhamento</b> e <b>tamanho</b>. Se quisermos medir só o alinhamento, temos de dividir pelos comprimentos, e é isso que faz a <b>similaridade de cosseno</b> (aula 5). Os Transformers enfrentam o mesmo problema: em dimensões altas os produtos escalares crescem demais, e por isso a fórmula da atenção divide tudo por $\sqrt{d_k}$ (aula 41).</p>""",
        },
        {
            "tipo": "passos",
            "titulo": "Calculando a sombra exatamente: a projeção",
            "corpo": r"""<p>Às vezes queremos a própria sombra, como um <b>vetor</b> deitado sobre $\vec v$, e não só o número. A fórmula é:</p>
$$\operatorname{proj}_{\vec v}\,\vec w \;=\; \frac{\vec w \cdot \vec v}{\vec v \cdot \vec v}\;\vec v$$
<p>Leia como “projeção de w sobre v”. Vamos aplicá-la a $\vec w = [3,3]$ e $\vec v = [4,0]$, entendendo cada peça:</p>""",
            "passos": [
                {"faca": r"Numerador: $\vec w \cdot \vec v = 3\times4 + 3\times0 = 12$.",
                 "porque": "Mede o quanto w concorda com a direção de v, ou seja, a sombra multiplicada pelo comprimento de v."},
                {"faca": r"Denominador: $\vec v \cdot \vec v = 4\times4 + 0\times0 = 16$.",
                 "porque": r"O produto de um vetor com ele mesmo é o comprimento ao quadrado ($\|\vec v\|^2 = 4^2$). Dividir por ele retira o “excesso” de tamanho de v que entrou no numerador."},
                {"faca": r"Fração: $\dfrac{12}{16} = 0{,}75$.",
                 "porque": "Responde quantas cópias de v cabem na sombra: três quartos de v."},
                {"faca": r"Resultado: $0{,}75 \times [4,0] = [3,\,0]$.",
                 "porque": "A sombra precisa estar deitada sobre a reta de v, então ela é um múltiplo de v."},
                {"faca": r"Verificação: o “resto” $\vec w - \operatorname{proj} = [3,3]-[3,0] = [0,3]$ satisfaz $[0,3]\cdot[4,0] = 0$.",
                 "porque": "O que sobra é perpendicular a v, exatamente o tracejado vertical da figura. Isso confirma que a sombra foi bem calculada."},
            ],
            "conclusao": r"""Todo vetor pode ser quebrado em <b>uma parte ao longo de v</b> mais <b>uma parte perpendicular a v</b>. Essa decomposição está por trás do método dos mínimos quadrados (a regressão linear clássica, Strang cap. 4) e do PCA (aula 11).""",
        },
        {
            "tipo": "visual",
            "rotulo": "O salto para a IA",
            "titulo": "Palavras como setas: embeddings",
            "corpo": r"""<p>Modelos de linguagem transformam cada palavra em um vetor chamado <b>embedding</b>. Vamos usar uma versão de brinquedo com só 2 dimensões, que vai nos acompanhar ao longo da trilha no nosso <b>classificador de avaliações de uma cafeteria</b>. O eixo 1 mede positividade e o eixo 2 mede intensidade:</p>""",
            "svg": SVG_EMBEDDINGS,
            "legenda": "Embeddings de brinquedo. Em modelos reais são centenas ou milhares de dimensões, e os eixos não têm nomes interpretáveis.",
        },
        {
            "tipo": "tabela",
            "titulo": "O produto escalar como votação",
            "cabecalho": ["Par de palavras", "Conta", "Resultado"],
            "linhas": [
                ["ótimo · bom", r"$3\times2 + 2\times1 = 6 + 2$", r"$\mathbf{8}$"],
                ["ótimo · ruim", r"$3\times(-2) + 2\times1 = -6 + 2$", r"$\mathbf{-4}$"],
                ["ótimo · péssimo", r"$3\times(-3) + 2\times2 = -9 + 4$", r"$\mathbf{-5}$"],
                ["bom · ruim", r"$2\times(-2) + 1\times1 = -4 + 1$", r"$\mathbf{-3}$"],
            ],
            "depois": r"""<p>Olhe para “ótimo · péssimo”. A dimensão positividade vota fortemente <b>contra</b> a semelhança ($-9$), mas a dimensão intensidade vota <b>a favor</b> ($+4$), porque as duas são palavras fortes. O resultado, $-5$, é a soma dos votos.</p>
<p>Essa é a melhor forma de pensar o produto escalar em IA: <b>cada dimensão vota a favor (+) ou contra (−) a semelhança, com força proporcional aos valores</b>. Em um embedding real com 1.536 dimensões, são 1.536 votos.</p>""",
        },
        {
            "tipo": "ponte",
            "titulo": "Três lugares onde você vai reencontrar esta operação",
            "corpo": r"""<p><b>1. Dentro de cada neurônio.</b> Um neurônio recebe características $\vec x$, tem pesos $\vec w$ e calcula $z = \vec w \cdot \vec x + b$, ou seja, um total ponderado como o do supermercado. No nosso classificador, se $\vec x = [2,\,0,\,1]$ (2 palavras positivas, 0 negativas, 1 ponto de exclamação), $\vec w = [1{,}5,\;-2,\;0{,}3]$ e $b = -1$:</p>
$$z = 1{,}5\times2 + (-2)\times0 + 0{,}3\times1 + (-1) = 3 + 0 + 0{,}3 - 1 = 2{,}3$$
<p>Como $z > 0$, o neurônio aposta em “avaliação positiva”. Os <b>pesos</b> fazem o papel dos preços: dizem quanto vale cada característica.</p>
<p><b>2. Na busca semântica e no RAG.</b> Quando um sistema procura os trechos de documento mais relevantes para sua pergunta, ele calcula o produto escalar (ou o cosseno) entre o embedding da pergunta e o de cada trecho, e fica com os maiores.</p>
<p><b>3. No coração dos Transformers.</b> A atenção decide quanto cada palavra deve “prestar atenção” em cada outra calculando $\vec q \cdot \vec k$ entre um vetor de consulta (<i>query</i>) e um vetor de chave (<i>key</i>). É o mesmo produto escalar, aplicado milhões de vezes (aulas 40 e 41). E a multiplicação de matrizes, a operação que as GPUs aceleram, é simplesmente <b>muitos produtos escalares organizados em tabela</b> (aula 7).</p>""",
        },
        {
            "tipo": "laboratorio",
            "titulo": "Investigue com NumPy",
            "corpo": r"""<p>Use o código como bancada de experimentos: rode, mude um número e preveja o resultado <i>antes</i> de executar.</p>""",
            "codigo": r'''import numpy as np

v = np.array([4.0, 0.0])
w = np.array([3.0, 3.0])

# 1) Três formas de calcular o MESMO número
print("laço manual:", sum(v[i] * w[i] for i in range(len(v))))
print("np.dot     :", np.dot(v, w))
print("operador @ :", v @ w)

# 2) A versão geométrica concorda?
cos_theta = (v @ w) / (np.linalg.norm(v) * np.linalg.norm(w))
print("ângulo (graus):", np.degrees(np.arccos(cos_theta)))   # ~45

# 3) Projeção de w sobre v e o resto perpendicular
proj = (w @ v) / (v @ v) * v
resto = w - proj
print("projeção:", proj, "| resto:", resto, "| resto·v =", resto @ v)

# 4) Cuidado: * NÃO é produto escalar
print("v * w (elemento a elemento):", v * w)   # [12. 0.] -> um vetor!
print("soma de v * w             :", (v * w).sum())''',
            "experimentos": [
                r"Troque <code>w</code> por <code>[-3, 3]</code>. Antes de rodar, preveja o sinal do produto e o ângulo. (Resposta esperada: $-12$ e 135°.)",
                r"Use <code>w = [0, 5]</code>. Por que o produto dá zero mesmo com um vetor longo?",
                r"Multiplique <code>w</code> por 10. O que muda no produto escalar e o que fica igual no ângulo?",
                r"Sorteie dois vetores de 1.000 dimensões com <code>a = np.random.randn(1000)</code> e <code>b = np.random.randn(1000)</code>, e calcule o cosseno entre eles. Repita várias vezes. Os valores ficam perto de zero, e a aula 38 explica por que isso é fundamental para os LLMs.",
            ],
        },
        {
            "tipo": "desafio",
            "titulo": "Exercícios com dicas graduais",
            "exercicios": [
                {
                    "enunciado": r"Calcule $\vec a \cdot \vec b$ para $\vec a = [1,\,-2,\,3]$ e $\vec b = [4,\,0,\,-1]$. Os vetores estão perto de ser perpendiculares?",
                    "dicas": ["Multiplique posição por posição e some os três resultados.",
                              r"Para julgar se estão “perto” de perpendiculares, compare o produto com o tamanho dos vetores: $\|\vec a\| = \sqrt{14}$ e $\|\vec b\| = \sqrt{17}$."],
                    "resposta": r"""$\vec a\cdot\vec b = 4 + 0 - 3 = 1$. O cosseno vale $\dfrac{1}{\sqrt{14}\,\sqrt{17}} \approx \dfrac{1}{15{,}43} \approx 0{,}065$, o que dá $\theta \approx 86{,}3^\circ$. <b>Sim, estão quase perpendiculares.</b> O produto escalar não deu exatamente zero, mas ficou minúsculo comparado ao tamanho dos vetores. Lição: “pequeno” só tem sentido em relação às normas.""",
                },
                {
                    "enunciado": r"Encontre o valor de $k$ que torna $[2,\,k]$ perpendicular a $[3,\,6]$.",
                    "dicas": ["Perpendicular significa produto escalar igual a zero.",
                              r"Monte a equação $2\times3 + k\times6 = 0$."],
                    "resposta": r"""$6 + 6k = 0 \Rightarrow k = -1$. Conferindo: $[2,-1]\cdot[3,6] = 6 - 6 = 0$ ✓. Repare que “ser perpendicular” virou uma <b>equação</b>. É assim que muitas restrições geométricas entram nos algoritmos.""",
                },
                {
                    "enunciado": r"Calcule a projeção de $\vec w = [2,\,3]$ sobre $\vec v = [1,\,1]$ e verifique que o resto é perpendicular a $\vec v$.",
                    "dicas": [r"Calcule $\vec w\cdot\vec v$ e $\vec v\cdot\vec v$ separadamente.",
                              r"A fração é $5/2$. Multiplique-a pelo vetor $\vec v$."],
                    "resposta": r"""$\vec w\cdot\vec v = 5$ e $\vec v\cdot\vec v = 2$, então a projeção é $2{,}5\times[1,1] = [2{,}5,\;2{,}5]$. O resto é $[2,3]-[2{,}5,\,2{,}5] = [-0{,}5,\;0{,}5]$, e $[-0{,}5,\,0{,}5]\cdot[1,1] = 0$ ✓.""",
                },
                {
                    "enunciado": r"Usando os embeddings da aula, qual palavra tem o maior produto escalar com “bom”? Agora invente a palavra “excelente” $= [6,\,4]$, que tem a mesma direção de “ótimo” e o dobro do tamanho. O que acontece com o ranking? Isso é desejável?",
                    "dicas": [r"Calcule bom·ótimo, bom·ruim e bom·péssimo.",
                              r"bom·excelente $= 2\times6 + 1\times4$. Compare com bom·ótimo."],
                    "resposta": r"""bom·ótimo $= 8$, bom·ruim $= -3$ e bom·péssimo $= -6+2 = -4$, então “ótimo” vence. Mas bom·excelente $= 16$, o dobro de bom·ótimo, <b>só porque o vetor é mais longo</b>, já que a direção é a mesma. Se o objetivo é comparar <i>significado</i>, isso é um defeito: o produto escalar puro favorece vetores grandes. A correção é normalizar os vetores ou usar o cosseno, o assunto da aula 5.""",
                },
            ],
        },
        {
            "tipo": "armadilhas",
            "itens": [
                {"erro": "“O resultado do produto escalar é um vetor.”",
                 "correcao": "É um único número. Você obtém um vetor ao multiplicar um vetor por um escalar ou na projeção, que reaproveita o produto escalar dentro da fórmula."},
                {"erro": "“Em NumPy, a * b calcula o produto escalar.”",
                 "correcao": "<code>a * b</code> multiplica elemento a elemento (produto de Hadamard) e devolve um vetor. O produto escalar é <code>a @ b</code> ou <code>np.dot(a, b)</code>, que equivale a <code>(a * b).sum()</code>."},
                {"erro": "“Produto escalar grande quer dizer vetores parecidos.”",
                 "correcao": "Ele também cresce com o tamanho dos vetores. Para comparar só a direção, use a similaridade de cosseno (aula 5)."},
                {"erro": "“Produto escalar zero quer dizer que um dos vetores é nulo.”",
                 "correcao": "Pode ser, mas o caso interessante é outro: vetores não nulos e perpendiculares, como $[1,2]$ e $[2,-1]$."},
                {"erro": "“Dá para calcular com vetores de tamanhos diferentes.”",
                 "correcao": "Não dá: sobrariam componentes sem par. O NumPy avisa com um erro do tipo <code>shapes (3,) and (2,) not aligned</code>, e esse é um dos erros mais comuns ao montar redes neurais."},
            ],
        },
    ],
    "resumo": [
        r"Produto escalar: multiplicar par a par e somar, $\vec u\cdot\vec v = \sum_i u_i v_i$. O resultado é um número.",
        r"Geometricamente, $\vec u\cdot\vec v = \|\vec u\|\|\vec v\|\cos\theta$, que é a sombra de um vetor vezes o comprimento do outro.",
        "O sinal indica a concordância: positivo quando os vetores concordam, zero quando são perpendiculares e negativo quando discordam.",
        r"A projeção $\frac{\vec w\cdot\vec v}{\vec v\cdot\vec v}\vec v$ divide um vetor em uma parte paralela e outra perpendicular.",
        "Em IA, o produto escalar é o total ponderado do neurônio, a medida de semelhança entre embeddings e o placar da atenção.",
    ],
    "proxima": r"""Usamos o comprimento $\|\vec v\|$ de passagem. Na <b>aula 4</b> ele ganha vida própria: existe mais de uma forma de medir “tamanho” (as normas L1 e L2), e essa escolha muda o comportamento de modelos reais por meio da regularização.""",
    "referencias": [
        {"obra": "Gilbert Strang, <i>Introduction to Linear Algebra</i> (5ª ed.)", "trecho": "§1.2 Lengths and Dot Products",
         "uso": "Equivalência entre a regra algébrica e o ângulo; vetores perpendiculares"},
        {"obra": "Deisenroth, Faisal & Ong, <i>Mathematics for Machine Learning</i>", "trecho": "§3.2–3.4 e §3.8",
         "uso": "Produto interno, ângulos, ortogonalidade e projeções ortogonais"},
        {"obra": "Goodfellow, Bengio & Courville, <i>Deep Learning</i>", "trecho": "§2.2 Multiplying Matrices and Vectors",
         "uso": "Notação xᵀy usada nos artigos"},
        {"obra": "3Blue1Brown, <i>Essence of Linear Algebra</i>", "trecho": "cap. 9, “Dot products and duality”",
         "uso": "Intuição visual da projeção"},
        {"obra": "Mikolov et al. (2013), <i>Efficient Estimation of Word Representations in Vector Space</i>", "trecho": "",
         "uso": "Origem dos embeddings de palavras (word2vec)"},
    ],
},

# =========================================================================
# AULA 14 — REGRA DA CADEIA
# Formato: analogia física -> função composta -> grafo computacional -> treinar um neurônio à mão
# =========================================================================
"Regra da Cadeia (Chain Rule) - o motor do Backpropagation": {
    "v": 2,
    "duracao": 30,
    "gancho": r"""Uma rede neural é uma fila de funções: a saída de uma vira a entrada da próxima. Quando o erro no final da fila está alto, <b>de quem é a culpa</b>? Da última camada? Da primeira? De cada um dos milhões de pesos? A regra da cadeia distribui essa culpa com precisão matemática, e o algoritmo que faz isso tem nome: <b>backpropagation</b>.""",
    "prerequisitos": [
        "Aula 12: a derivada como taxa de variação, ou seja, “quanto a saída muda quando a entrada muda um pouquinho”.",
        r"Aula 13: as regras básicas, como $(x^n)' = n\,x^{n-1}$.",
        r"Aula 3: o neurônio calcula $z = w x + b$.",
    ],
    "objetivos": [
        "reconhecer uma função composta e separá-la em “de dentro” e “de fora”;",
        "aplicar a regra da cadeia com dois e com três elos;",
        "calcular à mão o gradiente de um neurônio (ida e volta) e executar um passo real de treinamento;",
        "conferir gradientes numericamente, uma técnica usada por quem implementa redes.",
    ],
    "blocos": [
        {
            "tipo": "texto",
            "rotulo": "Começando pela intuição",
            "titulo": "Taxas que se multiplicam",
            "corpo": r"""<p>Um balão sobe <b>5 metros por segundo</b>. Na atmosfera, a temperatura cai cerca de <b>0,0065 °C a cada metro</b> de altitude. Quanto a temperatura muda <b>por segundo</b>, para quem está no balão?</p>
$$\underbrace{-0{,}0065\ \tfrac{^\circ\text{C}}{\text{m}}}_{\text{temperatura por metro}} \times \underbrace{5\ \tfrac{\text{m}}{\text{s}}}_{\text{metros por segundo}} = -0{,}0325\ \tfrac{^\circ\text{C}}{\text{s}}$$
<p>Sem perceber, você usou a regra da cadeia. A temperatura depende da altitude, a altitude depende do tempo, e <b>as taxas de variação de cada elo se multiplicam</b>. Repare como as unidades “se cancelam” (metros com metros), o que é uma boa pista de que a conta está certa.</p>
<p>Stewart usa uma imagem parecida, com engrenagens: se a engrenagem $u$ gira 3 vezes mais rápido que $x$ e $y$ gira 2 vezes mais rápido que $u$, então $y$ gira $2\times3 = 6$ vezes mais rápido que $x$. Toda a aula é uma formalização dessa ideia.</p>""",
        },
        {
            "tipo": "texto",
            "titulo": "Função composta: uma linha de montagem",
            "corpo": r"""<p>Considere $y = (3x+1)^2$. Para calcular $y$ a partir de $x$, você faz duas etapas, como em uma linha de montagem:</p>
<ul><li><b>Máquina de dentro:</b> recebe $x$ e devolve $u = 3x + 1$.</li>
<li><b>Máquina de fora:</b> recebe $u$ e devolve $y = u^2$.</li></ul>
<p>Com $x = 1$, a primeira máquina entrega $u = 4$ e a segunda entrega $y = 16$. Quando uma função está “dentro” de outra assim, dizemos que é uma <b>função composta</b>. Uma rede neural é uma composição com dezenas de máquinas: camada 1, ativação, camada 2, ativação, …, perda.</p>""",
        },
        {
            "tipo": "notacao",
            "titulo": "Os símbolos da regra",
            "corpo": r"""<p>A regra da cadeia diz que a taxa total é o produto das taxas de cada elo:</p>
$$\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx} \qquad\text{ou, equivalentemente,}\qquad (f\circ g)'(x) = f'\big(g(x)\big)\cdot g'(x)$$""",
            "itens": [
                {"simbolo": r"$\dfrac{dy}{dx}$", "leitura": "dê y dê x",
                 "significado": "A taxa de variação de $y$ por unidade de $x$. É notação de Leibniz: parece uma fração e às vezes se comporta como uma, mas na verdade é um limite (aula 12)."},
                {"simbolo": r"$\dfrac{dy}{du}$", "leitura": "dê y dê u", "significado": "A taxa da máquina de fora, que mede quanto $y$ muda quando $u$ muda."},
                {"simbolo": r"$f\circ g$", "leitura": "f composta com g (ou “f bola g”)", "significado": "Primeiro aplica $g$, depois $f$. Lê-se da direita para a esquerda: $(f\\circ g)(x) = f(g(x))$."},
                {"simbolo": r"$f'\big(g(x)\big)$", "leitura": "f linha calculada em g de x",
                 "significado": "A derivada da máquina de fora <b>avaliada no valor que sai da máquina de dentro</b>. Esse detalhe é onde mais se erra."},
                {"simbolo": r"$\dfrac{\partial L}{\partial w}$", "leitura": "derivada parcial de L em relação a w (o ∂ lê-se “del” ou “d curvo”)",
                 "significado": "Usada quando a função depende de várias variáveis e variamos só uma, mantendo as outras fixas. A perda de uma rede depende de muitos pesos, por isso o ∂ aparece em todo artigo de IA (aula 16)."},
            ],
        },
        {
            "tipo": "passos",
            "titulo": r"Exemplo resolvido: a derivada de $(3x+1)^2$ em $x = 1$",
            "passos": [
                {"faca": r"Derivada de dentro: $u = 3x+1 \;\Rightarrow\; \dfrac{du}{dx} = 3$.",
                 "porque": "Cada unidade a mais de x empurra u 3 unidades para cima."},
                {"faca": r"Derivada de fora: $y = u^2 \;\Rightarrow\; \dfrac{dy}{du} = 2u$.",
                 "porque": "É a regra da potência, aplicada como se u fosse a variável."},
                {"faca": r"Avalie a de fora no ponto certo: com $x = 1$, temos $u = 4$, então $\dfrac{dy}{du} = 2\times4 = 8$.",
                 "porque": "A máquina de fora está recebendo u = 4, e não x = 1."},
                {"faca": r"Multiplique os elos: $\dfrac{dy}{dx} = 8 \times 3 = 24$.",
                 "porque": "As taxas se encadeiam, como no balão e nas engrenagens."},
                {"faca": r"Confira numericamente: em $x = 1{,}001$, temos $y = (4{,}003)^2 = 16{,}024009$, então $\dfrac{\Delta y}{\Delta x} = \dfrac{0{,}024009}{0{,}001} = 24{,}009 \approx 24$ ✓",
                 "porque": "Nunca confie cegamente em uma derivada: um pequeno empurrão em x confirma a conta."},
            ],
            "conclusao": r"""Fórmula geral: $\dfrac{dy}{dx} = 2(3x+1)\cdot 3 = 6(3x+1)$. Para conferir por outro caminho, expanda $(3x+1)^2 = 9x^2+6x+1$ e derive: $18x + 6 = 6(3x+1)$. Os dois caminhos dão o mesmo resultado, mas em uma rede neural expandir é impossível. A regra da cadeia é o único caminho viável.""",
        },
        {
            "tipo": "pense",
            "pergunta": r"""Por que não basta derivar $u^2$ como $2u = 8$ e parar por aí?""",
            "resposta": r"""Porque $2u$ é a taxa de $y$ <b>em relação a $u$</b>, e a pergunta é sobre a taxa em relação a $x$. Cada unidade de $x$ move $u$ três unidades, e esquecer esse fator subestima a resposta em 3 vezes. Esquecer a “derivada de dentro” é o erro número 1 do cálculo. Em uma rede neural, o mesmo erro faria os pesos das primeiras camadas receberem gradientes errados.""",
        },
        {
            "tipo": "visual",
            "rotulo": "Agora, um neurônio de verdade",
            "titulo": "O grafo computacional do nosso classificador",
            "corpo": r"""<p>Voltemos ao classificador de avaliações da aula 3, agora reduzido a um neurônio com uma entrada. A entrada é $x = 2$ (duas palavras positivas na avaliação), o peso é $w = 0{,}5$ e o viés é $b = -0{,}5$. A ativação é a sigmoide $\sigma(z) = \dfrac{1}{1+e^{-z}}$, que espreme qualquer número no intervalo entre 0 e 1. O rótulo verdadeiro é $y = 1$ (a avaliação é positiva), e a perda é $L = \tfrac12(a-y)^2$. Tudo isso é uma composição de quatro máquinas:</p>
$$L = \tfrac12\Big(\sigma(w\,x + b) - y\Big)^2$$
<p>Os frameworks representam essa composição como um <b>grafo computacional</b>:</p>""",
            "svg": SVG_GRAFO,
            "legenda": "Cada nó só precisa conhecer a própria derivada local. A regra da cadeia junta todas elas.",
        },
        {
            "tipo": "passos",
            "rotulo": "Passo 1 de 3",
            "titulo": "A ida (forward pass): calcular o erro",
            "passos": [
                {"faca": r"$z = w\,x + b = 0{,}5\times2 - 0{,}5 = 0{,}5$", "porque": "É o total ponderado da aula 3."},
                {"faca": r"$a = \sigma(0{,}5) = \dfrac{1}{1+e^{-0{,}5}} = \dfrac{1}{1{,}6065} \approx 0{,}6225$",
                 "porque": "A sigmoide converte o placar em uma “probabilidade” de a avaliação ser positiva: 62%."},
                {"faca": r"$L = \tfrac12(0{,}6225 - 1)^2 = \tfrac12(0{,}1425) \approx 0{,}0713$",
                 "porque": "A perda mede o quão longe estamos do alvo. Queremos diminuí-la."},
            ],
        },
        {
            "tipo": "passos",
            "rotulo": "Passo 2 de 3",
            "titulo": "A volta (backward pass): distribuir a culpa",
            "corpo": r"""<p>Queremos $\dfrac{\partial L}{\partial w}$, isto é, quanto a perda muda se mexermos no peso. Pela regra da cadeia, percorremos o grafo <b>de trás para frente</b>, multiplicando as derivadas locais:</p>
$$\frac{\partial L}{\partial w} = \frac{\partial L}{\partial a}\cdot\frac{\partial a}{\partial z}\cdot\frac{\partial z}{\partial w}$$""",
            "passos": [
                {"faca": r"$\dfrac{\partial L}{\partial a} = a - y = 0{,}6225 - 1 = -0{,}3775$",
                 "porque": r"A derivada de $\tfrac12(a-y)^2$ é $(a-y)$; o ½ foi colocado justamente para cancelar o 2. O sinal negativo diz que aumentar a diminui a perda."},
                {"faca": r"$\dfrac{\partial a}{\partial z} = \sigma(z)\,\big(1-\sigma(z)\big) = 0{,}6225\times0{,}3775 \approx 0{,}2350$",
                 "porque": "É uma propriedade elegante da sigmoide (a aula 15 demonstra). A derivada se calcula com o próprio valor de a, que já temos da ida."},
                {"faca": r"$\dfrac{\partial L}{\partial z} = -0{,}3775\times0{,}2350 \approx -0{,}0887$",
                 "porque": "Dois elos multiplicados. Este número será reaproveitado no passo seguinte."},
                {"faca": r"$\dfrac{\partial z}{\partial w} = x = 2 \;\Rightarrow\; \dfrac{\partial L}{\partial w} = -0{,}0887\times2 \approx -0{,}1774$",
                 "porque": "Se z = wx + b, cada unidade a mais em w aumenta z em x unidades."},
                {"faca": r"$\dfrac{\partial z}{\partial b} = 1 \;\Rightarrow\; \dfrac{\partial L}{\partial b} = -0{,}0887$",
                 "porque": "Reaproveitamos ∂L/∂z sem recalcular nada. Em uma rede com milhões de pesos, esse reaproveitamento é o que torna o backpropagation viável."},
            ],
            "conclusao": r"""Os dois gradientes são negativos, então <b>aumentar</b> $w$ e $b$ faz a perda <b>diminuir</b>. Agora sabemos para onde mexer.""",
        },
        {
            "tipo": "passos",
            "rotulo": "Passo 3 de 3",
            "titulo": "Um passo de treinamento: a rede aprende",
            "corpo": r"""<p>A regra de atualização da descida do gradiente (aula 18) é <b>andar contra o gradiente</b>, com um tamanho de passo $\eta$ (a letra grega <i>eta</i>, chamada taxa de aprendizado). Vamos usar $\eta = 0{,}5$:</p>""",
            "passos": [
                {"faca": r"$w \leftarrow w - \eta\,\dfrac{\partial L}{\partial w} = 0{,}5 - 0{,}5\times(-0{,}1774) = 0{,}5887$",
                 "porque": "Gradiente negativo com sinal de menos na frente faz w aumentar."},
                {"faca": r"$b \leftarrow b - \eta\,\dfrac{\partial L}{\partial b} = -0{,}5 - 0{,}5\times(-0{,}0887) = -0{,}4556$",
                 "porque": "Mesma lógica."},
                {"faca": r"Nova ida: $z = 0{,}5887\times2 - 0{,}4556 = 0{,}7218$; $a = \sigma(0{,}7218) \approx 0{,}6730$; $L \approx 0{,}0535$",
                 "porque": "Recalculamos tudo com os pesos novos."},
            ],
            "conclusao": r"""A perda caiu de <b>0,0713</b> para <b>0,0535</b>, uma redução de 25% em um único passo, e a “probabilidade” de avaliação positiva subiu de 62% para 67%. <b>Você acabou de treinar uma rede neural à mão.</b> O GPT faz exatamente isso, com bilhões de pesos e trilhões de exemplos.""",
        },
        {
            "tipo": "texto",
            "titulo": "Por que de trás para frente?",
            "corpo": r"""<p>Daria para estimar cada derivada “empurrando” um peso de cada vez e medindo a perda, como fizemos na conferência numérica. O problema é o custo: são <b>duas passadas pela rede para cada peso</b>. Um modelo com 7 bilhões de pesos exigiria 14 bilhões de passadas para dar <i>um único</i> passo de treino.</p>
<p>O backpropagation calcula <b>todos</b> os gradientes de uma vez, com uma passada de ida e uma de volta. A volta custa aproximadamente o dobro da ida. O segredo é o que vimos no passo 2: cada $\partial L/\partial(\text{nó})$ é calculado uma vez e reaproveitado por todos os nós anteriores. Em computação, isso se chama <b>programação dinâmica</b> (Goodfellow, §6.5).</p>""",
        },
        {
            "tipo": "laboratorio",
            "titulo": "Confira os gradientes e treine por 20 passos",
            "corpo": r"""<p>Este código usa só Python puro, sem bibliotecas. A conferência numérica (<i>gradient checking</i>) é uma técnica real, usada para encontrar bugs em implementações de redes.</p>""",
            "codigo": r'''import math

def sigmoide(z):
    return 1 / (1 + math.exp(-z))

def perda(w, b, x=2.0, y=1.0):
    return 0.5 * (sigmoide(w * x + b) - y) ** 2

w, b, x, y = 0.5, -0.5, 2.0, 1.0

# ---- ida (forward) ----
z = w * x + b
a = sigmoide(z)

# ---- volta (backward): regra da cadeia, elo por elo ----
dL_da = a - y
da_dz = a * (1 - a)
dL_dz = dL_da * da_dz          # calculado UMA vez...
dL_dw = dL_dz * x              # ...reaproveitado aqui
dL_db = dL_dz * 1              # ...e aqui

# ---- conferência numérica (diferença central) ----
h = 1e-5
num_dw = (perda(w + h, b) - perda(w - h, b)) / (2 * h)
print(f"dL/dw pela regra da cadeia: {dL_dw:.6f}")   # -0.177447
print(f"dL/dw numérico            : {num_dw:.6f}")  # -0.177447

# ---- treinamento: 20 passos de descida do gradiente ----
eta = 0.5
for passo in range(1, 21):
    a = sigmoide(w * x + b)
    dL_dz = (a - y) * a * (1 - a)
    w -= eta * dL_dz * x
    b -= eta * dL_dz
    if passo in (1, 5, 10, 20):
        print(f"passo {passo:2d} | w={w:.3f} b={b:.3f} | perda={perda(w, b):.4f}")''',
            "experimentos": [
                r"Mude o alvo para <code>y = 0</code> e a entrada para <code>x = 10</code>. A perda começa alta, mas o gradiente sai minúsculo. Por quê? Calcule <code>a * (1 - a)</code> nesse caso. Esse é o problema do <b>gradiente que desaparece</b>, assunto da aula 15.",
                r"Teste <code>eta = 5</code> e <code>eta = 0.01</code>. Com qual valor o treino oscila, e com qual ele quase não sai do lugar? (Aula 20.)",
                r"Troque a perda por $(a-y)^2$, sem o ½. O que acontece com o gradiente? E com o treino, se você ajustar <code>eta</code>?",
                r"Altere <code>h</code> na conferência para <code>1e-1</code> e depois para <code>1e-12</code>. Por que valores muito grandes <i>e</i> muito pequenos pioram a estimativa? (Dica: aproximação versus arredondamento do computador.)",
            ],
        },
        {
            "tipo": "desafio",
            "exercicios": [
                {
                    "enunciado": r"Calcule a derivada de $f(x) = (x^2+1)^3$ em $x = 2$.",
                    "dicas": [r"De dentro: $u = x^2 + 1$. De fora: $u^3$.",
                              r"Derivada de fora: $3u^2$. Derivada de dentro: $2x$. Quanto vale $u$ quando $x = 2$?"],
                    "resposta": r"""$u(2) = 5$, então $f'(2) = 3\times5^2\times(2\times2) = 3\times25\times4 = 300$. O erro mais comum é usar $3x^2$ (avaliar em $x$ em vez de $u$), o que daria $3\times4\times4 = 48$.""",
                },
                {
                    "enunciado": r"Derive $g(x) = e^{-x^2}$ e calcule $g'(1)$. Você vai reencontrar essa função na aula 25: ela é a forma do sino da distribuição normal.",
                    "dicas": [r"A derivada de $e^u$ é $e^u$, e a de dentro é a derivada de $-x^2$."],
                    "resposta": r"""$g'(x) = e^{-x^2}\cdot(-2x)$, então $g'(1) = -2e^{-1} \approx -0{,}7358$. O sinal negativo faz sentido: à direita do pico o sino está descendo.""",
                },
                {
                    "enunciado": r"Um neurônio usa ReLU, $a = \max(0, z)$, com $z = wx + b$, e perda $L = (a-y)^2$. Com $w = 1$, $b = 0{,}5$, $x = 1$ e $y = 3$, calcule $\dfrac{\partial L}{\partial w}$. Depois repita com $b = -2$. O que acontece?",
                    "dicas": [r"A derivada da ReLU é 1 quando $z > 0$ e 0 quando $z < 0$.",
                              r"Monte a cadeia $\dfrac{\partial L}{\partial a}\cdot\dfrac{\partial a}{\partial z}\cdot\dfrac{\partial z}{\partial w}$, com $\dfrac{\partial L}{\partial a} = 2(a-y)$."],
                    "resposta": r"""Com $b = 0{,}5$: $z = 1{,}5$, $a = 1{,}5$ e $L = 2{,}25$. Os elos valem $2(1{,}5-3) = -3$, depois $1$, depois $x = 1$, então $\dfrac{\partial L}{\partial w} = -3$. Com $b = -2$: $z = -1$, $a = 0$, e o elo da ReLU vale <b>0</b>. O gradiente inteiro vira zero e o peso não aprende, por maior que seja o erro. Esse é o “neurônio morto” (<i>dying ReLU</i>): um único elo nulo bloqueia a cadeia toda.""",
                },
            ],
        },
        {
            "tipo": "armadilhas",
            "itens": [
                {"erro": "Esquecer a derivada de dentro.", "correcao": r"Sempre pergunte: “isso é uma função de $x$ ou de algo que depende de $x$?”. Se depender, multiplique pela derivada desse algo."},
                {"erro": r"Avaliar a derivada de fora em $x$ em vez de $u$.", "correcao": r"Em $(3x+1)^2$ com $x=1$, o certo é $2\cdot\mathbf{4}\cdot3 = 24$, e não $2\cdot\mathbf{1}\cdot3 = 6$."},
                {"erro": "“dy/dx é uma fração, então sempre posso cancelar os du.”",
                 "correcao": "Esse cancelamento é um bom mnemônico para cadeias simples. Com várias variáveis e vários caminhos entre a entrada e a saída, as contribuições de cada caminho precisam ser <b>somadas</b> (regra da cadeia multivariável, aulas 16 e 17)."},
                {"erro": "“Backpropagation é o algoritmo que faz a rede aprender.”",
                 "correcao": "O backpropagation só <b>calcula</b> os gradientes. Quem usa esses gradientes para mudar os pesos é o otimizador: descida do gradiente, Adam etc. (aulas 18 e 19)."},
            ],
        },
        {
            "tipo": "ponte",
            "titulo": "Do papel ao PyTorch, e o problema das redes profundas",
            "corpo": r"""<p>No PyTorch, o mesmo neurônio fica assim. O <code>backward()</code> executa exatamente o passo 2:</p>
<pre><code>import torch
w = torch.tensor(0.5, requires_grad=True)
b = torch.tensor(-0.5, requires_grad=True)
a = torch.sigmoid(w * 2.0 + b)
L = 0.5 * (a - 1.0) ** 2
L.backward()
print(w.grad, b.grad)   # tensor(-0.1774) tensor(-0.0887)</code></pre>
<p>Cada operação registra a própria derivada local durante a ida, e o <code>backward()</code> multiplica tudo na volta. Esse mecanismo se chama <b>diferenciação automática</b> (<i>autograd</i>).</p>
<p>Agora imagine um Transformer com 96 camadas. O gradiente que chega à primeira camada é um <b>produto de dezenas de derivadas locais</b>. Se cada uma for um pouco menor que 1, o produto some (<i>vanishing gradient</i>); se for um pouco maior, explode. Por isso os Transformers usam <b>conexões residuais</b>, $y = x + F(x)$: pela regra da cadeia, $\frac{dy}{dx} = 1 + F'(x)$, e esse “1” cria uma via expressa por onde o gradiente passa intacto. Junto com a normalização (aula 39), é isso que permite treinar redes com dezenas de camadas.</p>""",
        },
    ],
    "resumo": [
        r"Em uma composição, as taxas de variação se multiplicam: $\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}$.",
        "A derivada de fora é avaliada no valor de dentro, e esquecer o fator de dentro é o erro clássico.",
        "Uma rede neural é um grafo de funções simples, e cada nó só precisa conhecer a própria derivada local.",
        "O backpropagation aplica a regra da cadeia de trás para frente, reaproveitando resultados, e obtém todos os gradientes por cerca de 3 vezes o custo de uma ida.",
        "A conferência numérica com diferenças finitas valida qualquer gradiente calculado à mão ou por código.",
    ],
    "proxima": r"""O fator $\sigma'(z) = 0{,}235$ que usamos está perto do máximo possível da sigmoide, que é 0,25. Na <b>aula 15</b> você vai ver por que isso condena redes profundas com sigmoide, e como ReLU e GeLU resolveram o problema.""",
    "referencias": [
        {"obra": "James Stewart, <i>Calculus</i> (8ª ed.)", "trecho": "§3.4 The Chain Rule",
         "uso": "Analogia das engrenagens e a notação de Leibniz"},
        {"obra": "Goodfellow, Bengio & Courville, <i>Deep Learning</i>", "trecho": "§6.5 Back-Propagation and Other Differentiation Algorithms",
         "uso": "Grafos computacionais e o reaproveitamento por programação dinâmica"},
        {"obra": "Deisenroth, Faisal & Ong, <i>Mathematics for Machine Learning</i>", "trecho": "§5.2 e §5.6",
         "uso": "Derivadas parciais, backpropagation e diferenciação automática"},
        {"obra": "Andrej Karpathy, <i>The spelled-out intro to neural networks and backpropagation (micrograd)</i>", "trecho": "",
         "uso": "Construção de um autograd do zero, uma ótima continuação desta aula"},
        {"obra": "Rumelhart, Hinton & Williams (1986), <i>Learning representations by back-propagating errors</i>", "trecho": "Nature 323",
         "uso": "O artigo que popularizou o backpropagation"},
    ],
},

# =========================================================================
# AULA 24 — TEOREMA DE BAYES
# Formato: aposta -> contagem de pessoas -> fórmula derivada da tabela -> chances/logits -> spam
# =========================================================================
"Probabilidade condicional e Teorema de Bayes": {
    "v": 2,
    "duracao": 30,
    "gancho": r"""Um exame com 90% de acerto deu positivo. Qual a chance de você estar doente? Se você pensou em algo perto de 90%, está em boa companhia: em estudos clássicos, a maioria dos médicos superestimou essa resposta drasticamente. Nesta aula você vai descobrir a resposta certa, entender por que a intuição falha e perceber que o mesmo raciocínio move filtros de spam, classificadores e a forma como uma IA expressa incerteza.""",
    "prerequisitos": [
        "Aula 21: probabilidade como proporção de casos.",
        "Aula 14: o neurônio com sigmoide. Ele vai ganhar uma interpretação nova no fim desta aula.",
    ],
    "objetivos": [
        r"distinguir $P(A\mid B)$ de $P(B\mid A)$, a confusão mais cara da estatística;",
        "resolver problemas de Bayes contando pessoas (frequências naturais) e, depois, pela fórmula;",
        "atualizar uma crença em sequência, quando chegam novas evidências;",
        "usar a forma de chances (odds) e entender por que redes neurais trabalham com logits;",
        "explicar como funciona um filtro de spam Naive Bayes.",
    ],
    "blocos": [
        {
            "tipo": "pense",
            "rotulo": "Faça sua aposta",
            "pergunta": r"""<p>Uma doença atinge <b>1%</b> da população. O exame detecta <b>90%</b> dos doentes, mas também dá positivo, por engano, em <b>9%</b> das pessoas saudáveis. Uma pessoa escolhida ao acaso fez o exame e o resultado deu <b>positivo</b>.</p>
<p>Qual é a chance de ela estar doente? Escreva um número antes de continuar.</p>""",
            "resposta": r"""Guarde o seu palpite. A resposta aparece no próximo bloco, sem fórmula nenhuma, só contando pessoas. Compare depois e veja o tamanho da diferença.""",
        },
        {
            "tipo": "icones",
            "rotulo": "Contando em vez de calcular",
            "titulo": "1.000 pessoas fazem o exame",
            "corpo": r"""<p>Em vez de lidar com porcentagens abstratas, imagine <b>1.000 pessoas reais</b>:</p>
<ul><li>1% está doente, ou seja, <b>10 pessoas</b>. O exame detecta 90% delas: <b>9 positivos</b> e 1 negativo.</li>
<li>99% estão saudáveis, ou seja, <b>990 pessoas</b>. O exame erra em 9% delas: cerca de <b>89 falsos positivos</b>.</li></ul>""",
            "total": 1000, "colunas": 40,
            "grupos": [
                {"n": 9, "estilo": "s1", "rotulo": "doentes com positivo (9)"},
                {"n": 1, "estilo": "s3", "rotulo": "doente com negativo (1)"},
                {"n": 89, "estilo": "s2", "rotulo": "saudáveis com positivo (89)"},
            ],
            "resto": "saudáveis com negativo (901)",
            "legenda": "Cada ponto é uma pessoa. Os positivos são os pontos cheios, claros e médios: 9 + 89 = 98.",
            "depois": r"""<p>No total, <b>98 pessoas</b> receberam resultado positivo, e só <b>9</b> delas estão doentes:</p>
$$\frac{9}{98} \approx 0{,}092 \;=\; \mathbf{9{,}2\%}$$
<p>Bem longe de 90%. O que aconteceu? A doença é <b>rara</b>, então mesmo uma taxa pequena de erro (9%) aplicada a uma multidão de saudáveis (990) produz muito mais alarmes falsos (89) do que casos verdadeiros (9). A raridade inicial, chamada de <b>taxa-base</b>, domina o resultado.</p>
<p>Esse método de trocar porcentagens por contagens se chama <b>frequências naturais</b>. Gigerenzer e Hoffrage (1995) mostraram que ele multiplica a taxa de acerto das pessoas nesse tipo de problema.</p>""",
        },
        {
            "tipo": "tabela",
            "titulo": "Os mesmos números, organizados",
            "cabecalho": ["", "Positivo", "Negativo", "Total"],
            "linhas": [
                ["<b>Doente</b>", "9", "1", "10"],
                ["<b>Saudável</b>", "89", "901", "990"],
                ["<b>Total</b>", "98", "902", "1.000"],
            ],
            "depois": r"""<p>Agora leia a tabela de dois jeitos. Esse é o coração da aula:</p>
<ul><li><b>Pela linha “Doente”:</b> dos 10 doentes, 9 deram positivo, ou seja, $9/10 = 90\%$. Esse número é o que o laboratório informa.</li>
<li><b>Pela coluna “Positivo”:</b> dos 98 positivos, 9 estão doentes, ou seja, $9/98 = 9{,}2\%$. Esse número é o que o paciente quer saber.</li></ul>
<p>O numerador é o mesmo (9) e os denominadores são diferentes. <b>Toda a confusão vem de trocar o denominador</b>, isto é, de trocar o universo de pessoas que estamos olhando.</p>""",
        },
        {
            "tipo": "notacao",
            "titulo": "Dando nome ao que acabamos de fazer",
            "corpo": r"""<p>A barra vertical “|” é a notação que registra <b>qual é o universo</b>, ou seja, o denominador:</p>""",
            "itens": [
                {"simbolo": r"$P(D)$", "leitura": "probabilidade de D",
                 "significado": "A chance de estar doente antes de qualquer exame: $10/1000 = 1\\%$."},
                {"simbolo": r"$P(+\mid D)$", "leitura": "probabilidade de positivo <b>dado</b> doente",
                 "significado": "Olhando <b>só para os doentes</b> (a linha), a fração com resultado positivo: $9/10$. Também é chamada de <i>sensibilidade</i> ou <i>recall</i>."},
                {"simbolo": r"$P(D\mid +)$", "leitura": "probabilidade de doente dado positivo",
                 "significado": "Olhando <b>só para os positivos</b> (a coluna), a fração de doentes: $9/98$. Em classificação, é a <i>precisão</i>."},
                {"simbolo": r"$\neg D$ ou $D^c$", "leitura": "não D (complemento de D)", "significado": "Estar saudável. $P(\\neg D) = 1 - P(D) = 0{,}99$."},
                {"simbolo": r"$P(D \cap +)$", "leitura": "probabilidade de D <b>e</b> positivo",
                 "significado": "A chance de as duas coisas acontecerem juntas: a célula $9/1000$ da tabela. O símbolo ∩ significa interseção."},
            ],
            "depois": r"""<p>A definição de probabilidade condicional formaliza o “olhar só para a coluna”:</p>
$$P(D\mid +) = \frac{P(D\cap +)}{P(+)} = \frac{9/1000}{98/1000} = \frac{9}{98}$$""",
        },
        {
            "tipo": "passos",
            "titulo": "Da tabela para a fórmula de Bayes",
            "corpo": r"""<p>Nem sempre teremos uma tabela pronta. Normalmente sabemos as taxas do exame ($P(+\mid D)$ e $P(+\mid\neg D)$) e a frequência da doença ($P(D)$). Vamos reconstruir cada número da tabela só com essas três informações:</p>""",
            "passos": [
                {"faca": r"Doentes com positivo: $P(D\cap +) = P(+\mid D)\,P(D) = 0{,}90\times0{,}01 = 0{,}009$",
                 "porque": "90% dos doentes, que são 1% da população. É o “9 em 1.000”."},
                {"faca": r"Todos os positivos: $P(+) = P(+\mid D)P(D) + P(+\mid\neg D)P(\neg D) = 0{,}009 + 0{,}09\times0{,}99 = 0{,}009 + 0{,}0891 = 0{,}0981$",
                 "porque": "Os positivos vêm de duas fontes, doentes e saudáveis, e somamos as duas. Isso é a lei da probabilidade total."},
                {"faca": r"Divida: $P(D\mid +) = \dfrac{0{,}009}{0{,}0981} \approx 0{,}0917$",
                 "porque": "É a fração de positivos que são doentes. (Com 89,1 falsos positivos exatos dá 9,17%; arredondando para 89 pessoas, dá 9/98 ≈ 9,18%.)"},
            ],
            "conclusao": r"""<p>Juntando os passos, você acabou de deduzir o <b>Teorema de Bayes</b>:</p>
$$\underbrace{P(D\mid +)}_{\text{posterior}} = \frac{\overbrace{P(+\mid D)}^{\text{verossimilhança}}\;\cdot\;\overbrace{P(D)}^{\text{prior}}}{\underbrace{P(+)}_{\text{evidência}}}$$
<p>Os nomes fazem sentido agora. O <b>prior</b> é a crença <i>antes</i> da evidência (1%). A <b>verossimilhança</b> mede o quanto a evidência é compatível com a hipótese (90%). O <b>posterior</b> é a crença <i>depois</i> da evidência (9,2%).</p>""",
        },
        {
            "tipo": "tabela",
            "rotulo": "Bayes como aprendizado",
            "titulo": "E se a pessoa repetir o exame?",
            "corpo": r"""<p>Downey, em <i>Think Bayes</i>, destaca a leitura <b>diacrônica</b> (ao longo do tempo) de Bayes: é uma regra para <b>atualizar crenças conforme chegam dados</b>. O posterior de hoje vira o prior de amanhã. Supondo que os erros de exames repetidos sejam independentes:</p>""",
            "cabecalho": ["Exame", "Crença antes (prior)", "Resultado", "Crença depois (posterior)"],
            "linhas": [
                ["1º", "1,0%", "positivo", "9,2%"],
                ["2º", "9,2%", "positivo", "50,3%"],
                ["3º", "50,3%", "positivo", "91,0%"],
            ],
            "depois": r"""<p>Cada evidência empurra a crença, e a mesma evidência tem efeito diferente dependendo de onde se parte. É assim que uma IA bayesiana aprende: começa com uma suposição e a ajusta a cada dado.</p>""",
        },
        {
            "tipo": "passos",
            "titulo": "O atalho das chances (odds)",
            "corpo": r"""<p>Existe uma forma de Bayes que faz essas contas de cabeça. Em vez de probabilidade, usamos <b>chances</b>: $\text{chances} = \dfrac{p}{1-p}$. Probabilidade de 1% equivale a chances de 1 para 99. Nessa forma, a regra vira uma multiplicação:</p>
$$\underbrace{\frac{P(D\mid +)}{P(\neg D\mid +)}}_{\text{chances depois}} \;=\; \underbrace{\frac{P(+\mid D)}{P(+\mid \neg D)}}_{\text{razão de verossimilhança}} \;\times\; \underbrace{\frac{P(D)}{P(\neg D)}}_{\text{chances antes}}$$
<p>O denominador $P(+)$, o mais trabalhoso de calcular, simplesmente se cancela.</p>""",
            "passos": [
                {"faca": r"Razão de verossimilhança do exame: $\dfrac{0{,}90}{0{,}09} = 10$.",
                 "porque": "Um positivo é 10 vezes mais provável em um doente do que em um saudável. Esse número resume a força da evidência."},
                {"faca": r"1º positivo: $\dfrac{1}{99}\times10 = \dfrac{10}{99}$, ou seja, $p = \dfrac{10}{109} \approx 9{,}2\%$ ✓",
                 "porque": "Para voltar das chances a:b para a probabilidade, calcule a/(a+b)."},
                {"faca": r"2º positivo: $\dfrac{100}{99}$, ou seja, $p = \dfrac{100}{199} \approx 50{,}3\%$ ✓",
                 "porque": "Basta multiplicar por 10 de novo."},
                {"faca": r"3º positivo: $\dfrac{1000}{99}$, ou seja, $p \approx 91{,}0\%$ ✓",
                 "porque": "Os mesmos números da tabela anterior, em três multiplicações."},
            ],
            "conclusao": r"""Tomando o logaritmo, as multiplicações viram <b>somas</b>: cada positivo <b>soma</b> $\ln 10 \approx 2{,}303$ às log-chances. Guarde esta ideia: em IA, <b>evidências se somam no espaço das log-chances</b>.""",
        },
        {
            "tipo": "ponte",
            "titulo": "Logits são log-chances: o neurônio da aula 14 era bayesiano",
            "corpo": r"""<p>Lembra da sigmoide, $\sigma(z) = \dfrac{1}{1+e^{-z}}$? Se $z$ for a log-chance, $z = \ln\dfrac{p}{1-p}$, então $\sigma(z) = p$. A sigmoide é exatamente a função que <b>converte log-chances em probabilidade</b>.</p>
<p>Conferindo com o exame: a log-chance inicial é $\ln(1/99) \approx -4{,}595$. Somando a evidência $\ln 10 \approx 2{,}303$, chegamos a $-2{,}292$, e $\sigma(-2{,}292) = \dfrac{1}{1+e^{2{,}292}} = \dfrac{1}{1+9{,}9} \approx 0{,}092$ ✓.</p>
<p>Agora releia o neurônio: $z = \vec w\cdot\vec x + b$, seguido de $\sigma(z)$. O <b>viés $b$ faz o papel do prior</b>, e cada termo $w_i x_i$ <b>soma uma evidência</b> nas log-chances. O número $z$ antes da sigmoide (ou da softmax) se chama <b>logit</b>, nome que você vai ver em todo código de PyTorch. Quando um classificador devolve “87% de chance de spam”, ele está estimando um posterior $P(\text{classe}\mid\text{entrada})$.</p>""",
        },
        {
            "tipo": "passos",
            "rotulo": "Aplicação clássica",
            "titulo": "Um filtro de spam Naive Bayes",
            "corpo": r"""<p>Em 2002, Paul Graham publicou “A Plan for Spam”, e filtros bayesianos se espalharam pelos e-mails do mundo. Vejamos a ideia com números simples. Suponha que 40% dos e-mails sejam spam e que, olhando e-mails antigos, tenhamos medido:</p>
<ul><li>a palavra “grátis” aparece em 30% dos spams e em 2% dos e-mails normais;</li>
<li>a palavra “reunião” aparece em 1% dos spams e em 10% dos e-mails normais.</li></ul>""",
            "passos": [
                {"faca": r"Chances iniciais de spam: $\dfrac{0{,}4}{0{,}6} = \dfrac{2}{3}$.", "porque": "É o prior, antes de ler o e-mail."},
                {"faca": r"Chega um e-mail com “grátis”: a razão é $\dfrac{0{,}30}{0{,}02} = 15$, então as chances passam a $\dfrac23\times15 = 10$, ou seja, $p = \dfrac{10}{11} \approx 90{,}9\%$.",
                 "porque": "“grátis” é 15 vezes mais comum em spam: é uma evidência forte."},
                {"faca": r"O mesmo e-mail também contém “reunião”: a razão é $\dfrac{0{,}01}{0{,}10} = 0{,}1$, então as chances passam a $10\times0{,}1 = 1$, ou seja, $p = 50\%$.",
                 "porque": "Uma razão menor que 1 é evidência <b>contra</b> o spam. As evidências se combinam por multiplicação."},
            ],
            "conclusao": r"""Por que o nome <b>“ingênuo”</b> (<i>naive</i>)? Porque o método supõe que as palavras são independentes entre si, dada a classe. Na prática isso é falso (“Rio” e “Janeiro” aparecem juntas), mas o método funciona surpreendentemente bem para <i>ordenar</i> e-mails do mais ao menos suspeito.""",
        },
        {
            "tipo": "laboratorio",
            "titulo": "Simule um milhão de pessoas",
            "corpo": r"""<p>Quando estiver em dúvida sobre uma conta de probabilidade, <b>simule</b>. Repare em um detalhe bonito do código: <code>positivo[doente].mean()</code> e <code>doente[positivo].mean()</code> são a mesma expressão com os papéis trocados, exatamente como $P(+\mid D)$ e $P(D\mid +)$.</p>""",
            "codigo": r'''import numpy as np

rng = np.random.default_rng(seed=42)
N = 1_000_000                     # pessoas simuladas

prevalencia    = 0.01             # P(D)
sensibilidade  = 0.90             # P(+ | D)
falso_positivo = 0.09             # P(+ | não D)

doente = rng.random(N) < prevalencia
chance_positivo = np.where(doente, sensibilidade, falso_positivo)
positivo = rng.random(N) < chance_positivo

# Olhar só para os doentes  -> P(+ | D)
print("P(+ | D) simulada:", positivo[doente].mean())    # ~0.90
# Olhar só para os positivos -> P(D | +)
print("P(D | +) simulada:", doente[positivo].mean())    # ~0.092

# A fórmula de Bayes, para comparar
p_pos = sensibilidade * prevalencia + falso_positivo * (1 - prevalencia)
print("P(D | +) por Bayes:", sensibilidade * prevalencia / p_pos)  # 0.0917''',
            "experimentos": [
                r"Mude <code>prevalencia</code> para 0.10 e depois para 0.50. Preveja antes de rodar. (Respostas: cerca de 52,6% e 90,9%.) O mesmo exame tem valores muito diferentes em populações diferentes.",
                r"Reduza <code>falso_positivo</code> para 0.01, mantendo a prevalência em 1%. Quanto melhora? (Cerca de 47,6%.) O que pesa mais, a sensibilidade ou o falso positivo?",
                r"Escreva um laço que aplica 3 exames seguidos e confira os valores 9,2%, 50,3% e 91,0% da tabela.",
                r"Faça um gráfico (<code>matplotlib</code>) de $P(D\mid +)$ em função da prevalência, de 0,001 a 0,5. Onde a curva é mais íngreme?",
            ],
        },
        {
            "tipo": "desafio",
            "exercicios": [
                {
                    "enunciado": r"<b>O problema dos biscoitos</b> (Downey, <i>Think Bayes</i>). O pote 1 tem 30 biscoitos de baunilha e 10 de chocolate. O pote 2 tem 20 de cada. Você escolhe um pote ao acaso, tira um biscoito sem olhar, e ele é de baunilha. Qual a probabilidade de ter vindo do pote 1?",
                    "dicas": ["Os dois potes têm 40 biscoitos e a mesma chance de serem escolhidos. Pense em todos os biscoitos de baunilha juntos.",
                              r"Há 30 + 20 = 50 biscoitos de baunilha no total. Quantos vêm do pote 1?"],
                    "resposta": r"""Pela contagem: $30/50 = 0{,}6$. Pela fórmula: $\dfrac{0{,}75\times0{,}5}{0{,}75\times0{,}5 + 0{,}5\times0{,}5} = \dfrac{0{,}375}{0{,}625} = 0{,}6$. A evidência “baunilha” elevou a crença no pote 1 de 50% para 60%.""",
                },
                {
                    "enunciado": r"<b>Detector de texto gerado por IA.</b> Em uma turma, 5% dos trabalhos foram escritos por IA. Um detector acusa 95% dos textos de IA, mas também acusa 10% dos textos humanos. Um trabalho foi acusado. Qual a chance de ele ter sido escrito por IA?",
                    "dicas": ["Imagine 1.000 trabalhos: quantos são de IA e quantos são humanos?",
                              "Textos de IA acusados: 95% de 50. Textos humanos acusados: 10% de 950."],
                    "resposta": r"""De IA e acusados: $47{,}5$. Humanos e acusados: $95$. Então $\dfrac{47{,}5}{142{,}5} = \dfrac13 \approx 33\%$. <b>Dois em cada três trabalhos acusados são humanos.</b> Esse é um argumento matemático real contra punir alunos com base apenas em detectores.""",
                },
                {
                    "enunciado": r"Com prior de 1% (chances de 1:99) e um exame com razão de verossimilhança 10, quantos positivos seguidos são necessários para passar de 99% de certeza?",
                    "dicas": [r"99% de probabilidade equivale a chances de 99:1, ou seja, 99.",
                              r"Depois de $k$ positivos, as chances valem $10^k/99$. Resolva $10^k/99 \ge 99$."],
                    "resposta": r"""É preciso $10^k \ge 9801$, então $k = 4$. Com 4 positivos, as chances são $10000/99 \approx 101$, o que dá $p = 101/102 \approx 99{,}0\%$. Na forma de log-chances: são 4 “parcelas” de $2{,}303$ somadas ao ponto de partida $-4{,}595$.""",
                },
            ],
        },
        {
            "tipo": "armadilhas",
            "itens": [
                {"erro": r"Confundir $P(A\mid B)$ com $P(B\mid A)$.",
                 "correcao": "Essa confusão tem até nome: <b>falácia do promotor</b>. “Só 1 em 1 milhão de inocentes teria esse DNA” <i>não</i> significa “a chance de o réu ser inocente é 1 em 1 milhão”. Em uma cidade de 10 milhões, cerca de 10 inocentes teriam o mesmo DNA."},
                {"erro": "Ignorar a taxa-base (o prior).", "correcao": "Um exame excelente aplicado a um evento raro ainda gera mais falsos alarmes do que acertos. Sempre pergunte: “quão comum é isso antes da evidência?”."},
                {"erro": "“Meu modelo tem 99% de acurácia, então é ótimo.”",
                 "correcao": r"Se só 1% dos casos é positivo, um modelo que <i>sempre</i> responde “negativo” também tem 99% de acurácia e não serve para nada. Por isso usamos <b>precisão</b> ($P(\text{real}\mid\text{previsto})$, que é Bayes) e <b>recall</b> ($P(\text{previsto}\mid\text{real})$)."},
                {"erro": "Multiplicar evidências sem verificar a independência.",
                 "correcao": "Dois exames do mesmo laboratório, com a mesma falha, não são evidências independentes. A tabela de exames repetidos só vale se os erros forem independentes, e essa é a mesma suposição “ingênua” do Naive Bayes."},
            ],
        },
        {
            "tipo": "ponte",
            "titulo": "O que vem pela frente na trilha",
            "corpo": r"""<p><b>Treinar uma rede é fazer Bayes ao contrário.</b> Na aula 28 (Máxima Verossimilhança) vamos escolher os pesos $\theta$ que tornam os dados mais prováveis, maximizando $P(\text{dados}\mid\theta)$, que é a verossimilhança desta aula. Se também multiplicarmos por um prior sobre os pesos, $P(\theta)$, obtemos a estimativa MAP. Com um prior gaussiano, esse termo extra é exatamente a <b>regularização L2</b> (<i>weight decay</i>) usada no treino de LLMs (Goodfellow, §5.6).</p>
<p>E a <b>entropia cruzada</b> (aula 35), a perda usada para treinar o GPT, mede o quão bem as probabilidades que o modelo atribui (posteriores sobre o próximo token) explicam o que realmente aconteceu.</p>""",
        },
    ],
    "resumo": [
        r"$P(A\mid B)$ significa “entre os casos em que B aconteceu, a fração em que A também aconteceu”. A barra define o denominador.",
        r"Bayes: $P(H\mid E) = \dfrac{P(E\mid H)\,P(H)}{P(E)}$, ou posterior = verossimilhança × prior ÷ evidência.",
        "Quando travar, troque porcentagens por contagens (frequências naturais) e monte a tabela.",
        "Na forma de chances, cada evidência multiplica pela razão de verossimilhança. Nas log-chances, ela soma.",
        "Logits são log-chances: a sigmoide e a softmax convertem a soma de evidências de um neurônio em probabilidades.",
    ],
    "proxima": r"""Até aqui, os eventos eram “sim ou não”. Na <b>aula 25</b> entram as grandezas contínuas, como altura, ruído e pesos de uma rede, com a distribuição normal. Também vamos separar com cuidado <b>probabilidade</b> de <b>verossimilhança</b>, duas palavras que já apareceram aqui.""",
    "referencias": [
        {"obra": "Allen B. Downey, <i>Think Bayes</i> (2ª ed.)", "trecho": "cap. “Bayes's Theorem”",
         "uso": "O problema dos biscoitos e a interpretação diacrônica (atualização de crenças)"},
        {"obra": "Gigerenzer & Hoffrage (1995), <i>How to improve Bayesian reasoning without instruction: frequency formats</i>", "trecho": "Psychological Review 102",
         "uso": "Frequências naturais e o exemplo clássico de diagnóstico"},
        {"obra": "Deisenroth, Faisal & Ong, <i>Mathematics for Machine Learning</i>", "trecho": "§6.3 Sum Rule, Product Rule, and Bayes' Theorem", "uso": ""},
        {"obra": "Goodfellow, Bengio & Courville, <i>Deep Learning</i>", "trecho": "§3.11 Bayes' Rule e §5.6 Bayesian Statistics",
         "uso": "Ligação entre o prior e a regularização (MAP)"},
        {"obra": "Paul Graham (2002), <i>A Plan for Spam</i>", "trecho": "", "uso": "Filtros de spam bayesianos"},
        {"obra": "3Blue1Brown, <i>Bayes theorem, the geometry of changing beliefs</i>", "trecho": "", "uso": "Visualização do teorema como áreas"},
    ],
},
}
