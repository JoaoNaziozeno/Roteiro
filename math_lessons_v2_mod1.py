# -*- coding: utf-8 -*-
"""
Aulas Visuais v2 - Módulo 1: Álgebra Linear para IA & Tensores (Tópicos 1 a 11)
Didática profunda, blocos flexíveis, referências a Gilbert Strang, Deisenroth, 3Blue1Brown, Goodfellow.
Exemplos com números conferidos, código exploratório e conexões diretas com IA e o Classificador da Cafeteria.
"""

from math_lessons_v2_samples import LESSONS_V2_SAMPLES, _defs, SVG_PROJECAO, SVG_EMBEDDINGS

SVG_PARALELOGRAMO = r"""<svg viewBox="0 0 320 220" class="lv2-svg" role="img" aria-label="Soma de dois vetores pela regra do paralelogramo">""" + _defs("pg") + r"""
<line x1="20" y1="180" x2="300" y2="180" class="sv-ax"/><line x1="40" y1="200" x2="40" y2="20" class="sv-ax"/>
<line x1="40" y1="180" x2="180" y2="180" class="sv-a" marker-end="url(#pgt)"/>
<line x1="40" y1="180" x2="100" y2="80" class="sv-b" marker-end="url(#pgm)"/>
<line x1="180" y1="180" x2="240" y2="80" class="sv-thin sv-dash"/>
<line x1="100" y1="80" x2="240" y2="80" class="sv-thin sv-dash"/>
<line x1="40" y1="180" x2="240" y2="80" class="sv-a" style="stroke-width:3" marker-end="url(#pgt)"/>
<text x="110" y="196" class="sv-t">u = [3, 0]</text>
<text x="54" y="125" class="sv-tm">v = [1, 2]</text>
<text x="246" y="74" class="sv-t">u + v = [4, 2]</text>
</svg>"""

SVG_TRANSF_LINEAR = r"""<svg viewBox="0 0 360 210" class="lv2-svg" role="img" aria-label="Transformação linear deformando a grade">""" + _defs("tl") + r"""
<g transform="translate(10, 10)">
  <text x="75" y="20" text-anchor="middle" class="sv-tm">Espaço Original (i, j)</text>
  <line x1="20" y1="160" x2="150" y2="160" class="sv-ax"/><line x1="40" y1="180" x2="40" y2="40" class="sv-ax"/>
  <line x1="40" y1="180" x2="40" y2="40" class="sv-ax"/>
  <line x1="40" y1="160" x2="100" y2="160" class="sv-a" marker-end="url(#tlt)"/>
  <line x1="40" y1="160" x2="40" y2="100" class="sv-b" marker-end="url(#tlm)"/>
  <text x="105" y="174" class="sv-t">î = [1, 0]</text>
  <text x="46" y="96" class="sv-tm">ĵ = [0, 1]</text>
</g>
<g transform="translate(180, 10)">
  <text x="85" y="20" text-anchor="middle" class="sv-tm">Após Matriz A = [[2, 1], [0, 1.5]]</text>
  <line x1="20" y1="160" x2="160" y2="160" class="sv-ax"/><line x1="30" y1="180" x2="30" y2="40" class="sv-ax"/>
  <line x1="30" y1="160" x2="130" y2="160" class="sv-a" marker-end="url(#tlt)"/>
  <line x1="30" y1="160" x2="80" y2="85" class="sv-b" marker-end="url(#tlm)"/>
  <text x="134" y="174" class="sv-t">A î = [2, 0]</text>
  <text x="84" y="80" class="sv-tm">A ĵ = [1, 1.5]</text>
</g>
</svg>"""

GUIDES_MOD1_V2 = {
    # Reutiliza o piloto 3
    "Produto escalar (Dot Product) e projeções": LESSONS_V2_SAMPLES["Produto escalar (Dot Product) e projeções"],

    # 1. Vetores e espaços vetoriais
    "Vetores e espaços vetoriais: intuição geométrica": {
        "v": 2,
        "duracao": 25,
        "gancho": r"""Como um computador consegue representar uma frase, o preço de uma casa ou o estado de uma conta de banco em uma única entidade matemática? A resposta é o <b>vetor</b>, a estrutura atômica sobre a qual toda a Inteligência Artificial é construída.""",
        "prerequisitos": ["Nenhum pré-requisito avançado: apenas familiaridade com números reais e o plano cartesiano."],
        "objetivos": [
            "compreender as três faces de um vetor: a geométrica (seta), a computacional (lista de floats) e a algébrica (ponto em um espaço vetorial);",
            "somar e multiplicar vetores por escalares geometricamente e por coordenadas;",
            "entender o que significa o espaço $\\mathbb{R}^n$ e como embeddings de LLMs habitam $\\mathbb{R}^{1536}$;",
            "manipular vetores em Python com NumPy.",
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "As Três Perspectivas",
                "titulo": "O que é um vetor, afinal?",
                "corpo": r"""<p>Gilbert Strang costuma abrir suas aulas no MIT com uma frase direta: <i>“O coração da Álgebra Linear são duas operações com vetores: somar e multiplicar por um número”</i>. Mas dependendo de com quem você fala, a palavra 'vetor' tem nuances diferentes:</p>
<ul>
<li><b>Para a Física (visão geométrica):</b> É uma seta com <b>tamanho</b> (magnitude) e <b>direção</b>. Não importa onde ela começa no espaço; se tem o mesmo tamanho e aponta para o mesmo lado, é o mesmo vetor.</li>
<li><b>Para a Ciência da Computação:</b> É simplesmente um <b>arranjo ordenado de números</b> (uma lista ou <code>array</code>). Por exemplo, as features de uma avaliação da nossa cafeteria: <code>[número_estrelas, contagem_palavras, pontuação_sentimento]</code>.</li>
<li><b>Para a Matemática (visão abstrata):</b> É qualquer elemento que pertence a um <b>espaço vetorial</b>, isto é, que pode ser somado e multiplicado por escalares respeitando 8 propriedades básicas de consistência (comutatividade, associatividade, elemento neutro, etc.).</li>
</ul>
<p>Em Inteligência Artificial, nós <b>fundimos essas três visões</b> o tempo todo: pensamos na lista de números do computador como uma coordenada geométrica que aponta em uma direção do espaço semântico!</p>""",
            },
            {
                "tipo": "notacao",
                "titulo": "Notação formal dos livros",
                "corpo": r"""<p>Veja como os livros de IA e Álgebra Linear representam vetores:</p>
$$\vec{v} = \begin{bmatrix} v_1 \\ v_2 \\ \vdots \\ v_n \end{bmatrix} \in \mathbb{R}^n$$""",
                "itens": [
                    {"simbolo": r"$\vec{v}$ ou $\mathbf{v}$", "leitura": "vetor v", "significado": "A seta ou negrito distingue o vetor de um número comum (escalar $v$). Em papers de IA, usa-se quase sempre negrito minúsculo $\mathbf{x}$."},
                    {"simbolo": r"$\begin{bmatrix} v_1 \\ v_2 \end{bmatrix}$", "leitura": "vetor coluna v", "significado": "Por convenção matemática universal, vetores padrão são tratados como <b>colunas verticais</b>. Uma linha horizontal é representada com a transposta $\mathbf{v}^\top = [v_1, v_2]$."},
                    {"simbolo": r"$v_i$", "leitura": "v índice i", "significado": "O elemento individual na posição $i$ do vetor (ex.: $v_1$ é a primeira feature, $v_2$ é a segunda)."},
                    {"simbolo": r"$\mathbb{R}^n$", "leitura": "R elevado a n (ou espaço real de dimensão n)", "significado": "Conjunto de todas as listas com $n$ números reais contínuos. O plano cartesiano 2D é $\mathbb{R}^2$. Um embedding do modelo da OpenAI é $\mathbb{R}^{1536}$ (1.536 dimensões)."},
                ],
            },
            {
                "tipo": "visual",
                "titulo": "As duas operações sagradas: Soma e Multiplicação por Escalar",
                "corpo": r"""<p>Quando somamos dois vetores $\vec{u} + \vec{v}$, somamos elemento por elemento. Geometricamente, colocamos a ponta de um no início do outro (a famosa <b>Regra do Paralelogramo</b>):</p>""",
                "svg": SVG_PARALELOGRAMO,
                "legenda": "Soma de u = [3, 0] com v = [1, 2] resulta em u + v = [4, 2].",
                "depois": r"""<p>A segunda operação é a multiplicação por um número comum (chamado <b>escalar</b> porque ele <i>escala</i>, isto é, encolhe ou estica a seta sem mudar sua reta de suporte):</p>
$$2 \cdot \begin{bmatrix} 1 \\ 2 \end{bmatrix} = \begin{bmatrix} 2 \\ 4 \end{bmatrix}, \qquad -1 \cdot \begin{bmatrix} 1 \\ 2 \end{bmatrix} = \begin{bmatrix} -1 \\ -2 \end{bmatrix} \text{ (inverte o sentido)}$$""",
            },
            {
                "tipo": "ponte",
                "titulo": "Onde isso vive na IA moderna?",
                "corpo": r"""<p>Nos modelos de linguagem contemporâneos (ChatGPT, Claude, Llama), palavras e conceitos são representados como vetores densos em $\mathbb{R}^d$, chamados <b>embeddings</b>.</p>
<p>No artigo clássico de Mikolov et al. (2013), descobriu-se que somas e subtrações nesses espaços vetoriais refletem relações semânticas do mundo real:</p>
$$\vec{v}_{\text{Rei}} - \vec{v}_{\text{Homem}} + \vec{v}_{\text{Mulher}} \approx \vec{v}_{\text{Rainha}}$$
<p>Se você subtrai a 'direção masculina' de Rei e adiciona a 'direção feminina', o ponto resultante no espaço de alta dimensão cai exatamente vizinho ao vetor de Rainha! Isso só é possível porque o modelo aprendeu um espaço vetorial consistente.</p>""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Experimentando com vetores em NumPy",
                "codigo": r'''import numpy as np

# Definindo vetores no plano 2D
u = np.array([3.0, 0.0])
v = np.array([1.0, 2.0])

# 1. Soma vetorial componente a componente
soma = u + v
print("u + v =", soma)  # [4. 2.]

# 2. Multiplicação por escalar
duplo = 2.0 * v
print("2 * v =", duplo)  # [2. 4.]

# 3. Embedding de 1536 dimensões (simulação)
embedding_fake = np.random.randn(1536)
print("Dimensão do embedding:", embedding_fake.shape)
print("Primeiros 3 valores:", embedding_fake[:3].round(3))''',
                "experimentos": [
                    r"O que acontece se você multiplicar <code>v</code> por <code>-1.0</code>? Verifique as coordenadas.",
                    r"Tente somar um vetor de 2 elementos com um de 3 elementos. Qual erro o NumPy devolve? Esse erro de shape é o mais comum em deep learning.",
                ],
            },
            {
                "tipo": "desafio",
                "exercicios": [
                    {
                        "enunciado": r"Dados $\vec{a} = [2, -1, 4]$ e $\vec{b} = [-3, 5, 0]$, calcule o vetor $\vec{c} = 2\vec{a} - 3\vec{b}$.",
                        "dicas": ["Multiplique cada componente de a por 2 e de b por -3, depois some."],
                        "resposta": r"$2\vec{a} = [4, -2, 8]$ e $-3\vec{b} = [9, -15, 0]$. Somando componente a componente: $\vec{c} = [4+9, -2-15, 8+0] = [13, -17, 8]$.",
                    },
                ],
            },
            {
                "tipo": "armadilhas",
                "itens": [
                    {"erro": "Achar que um vetor precisa começar na origem (0, 0).", "correcao": "Um vetor representa um deslocamento relativo. Desenhamos a partir da origem por conveniência para ler as coordenadas da ponta."},
                    {"erro": "Confundir lista comum de Python [1, 2] com array do NumPy.", "correcao": "Em Python nativo, [1, 2] + [3, 4] gera [1, 2, 3, 4] (concatenação). Em NumPy, gera [4, 6] (soma vetorial matemática)."},
                ],
            },
        ],
        "resumo": [
            "Um vetor é uma lista de números que pode ser visualizada como uma seta com direção e tamanho.",
            "As duas operações fundamentais são soma elemento a elemento e multiplicação por escalar.",
            "O espaço onde moram listas de n números reais é chamado de R^n.",
            "Embeddings em IA são vetores densos em espaços de centenas ou milhares de dimensões.",
        ],
        "proxima": r"""Agora que sabemos somar e esticar vetores, o que acontece quando misturamos vários deles ao mesmo tempo? Na <b>aula 2</b> vamos explorar as <b>combinações lineares</b>, o <b>espaço gerado (span)</b> e as <b>bases</b>.""",
        "referencias": [
            {"obra": "Gilbert Strang, <i>Introduction to Linear Algebra</i> (5ª ed.)", "trecho": "§1.1 Vectors and Linear Combinations", "uso": "Fundação geométrica e algébrica dos vetores"},
            {"obra": "Deisenroth, Faisal & Ong, <i>Mathematics for Machine Learning</i>", "trecho": "§2.1–2.2 Vector Spaces and Subspaces", "uso": "Definição formal de espaços vetoriais"},
            {"obra": "3Blue1Brown", "trecho": "Essence of Linear Algebra, cap. 1", "uso": "As 3 perspectivas sobre vetores"},
        ],
    },

    # 2. Combinações lineares, span e bases
    "Combinações lineares, espaço gerado (span) e bases": {
        "v": 2,
        "duracao": 25,
        "gancho": r"""Como dois vetores simples como $[1, 0]$ e $[0, 1]$ conseguem construir qualquer imagem na tela do seu computador? E quando adicionamos um terceiro vetor, ele ajuda a alcançar novos pontos ou é apenas redundante? Essa é a diferença entre um espaço rico e um modelo com parâmetros inúteis.""",
        "prerequisitos": ["Aula 1: soma e multiplicação de vetores por escalares."],
        "objetivos": [
            "entender e calcular combinações lineares $c_1 \vec{v}_1 + c_2 \vec{v}_2$;",
            "visualizar o conceito de Espaço Gerado (Span) e identificar quando ele é uma reta, um plano ou um volume 3D;",
            "distinguir independência linear de dependência linear;",
            "compreender o conceito de Base como o conjunto mínimo gerador de um espaço.",
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Mistura Fundamental",
                "titulo": "Combinação Linear: o botão giratório do neurônio",
                "corpo": r"""<p>Se você tem dois vetores $\vec{v}_1$ e $\vec{v}_2$, uma <b>combinação linear</b> nada mais é do que esticar ou encolher cada um deles por um peso escalar ($c_1, c_2$) e somar o resultado:</p>
$$\vec{w} = c_1 \vec{v}_1 + c_2 \vec{v}_2 + \dots + c_k \vec{v}_k$$
<p>Pense nos escalares $c_1, c_2$ como botões de volume em uma mesa de som. Cada vetor $\vec{v}_i$ é um canal de áudio (baixo, bateria, voz). A música final que sai nas caixas de som é a combinação linear desses canais ponderados pelos volumes!</p>
<p>Em um neurônio artificial, cada entrada $x_i$ é multiplicada por um peso sináptico $w_i$. A operação pré-ativação $\sum w_i x_i$ é exatamente uma combinação linear.</p>""",
            },
            {
                "tipo": "texto",
                "titulo": "O que é o Span (Espaço Gerado)?",
                "corpo": r"""<p>O <b>Span</b> de um conjunto de vetores é a coleção de <b>TODOS os pontos possíveis que você consegue atingir</b> variando livremente os botões $c_1, c_2, \dots$ em todos os números reais possíveis de $-\infty$ a $+\infty$:</p>
<ul>
<li><b>Com 1 vetor não nulo:</b> O span é uma <b>linha reta infinita</b> passando pela origem.</li>
<li><b>Com 2 vetores que não apontam na mesma linha:</b> O span é um <b>plano 2D infinito</b>.</li>
<li><b>Com 3 vetores que não vivem no mesmo plano:</b> O span cobre todo o <b>espaço 3D ($\mathbb{R}^3$)</b>.</li>
</ul>
<p>Mas e se tivermos dois vetores na mesma linha reta, como $\vec{v}_1 = [1, 2]$ e $\vec{v}_2 = [2, 4]$? Como o segundo é apenas o dobro do primeiro, girar os botões de ambos ainda mantém você preso na mesma linha! Dizemos que eles são <b>linearmente dependentes</b>.</p>""",
            },
            {
                "tipo": "tabela",
                "titulo": "Independência Linear vs Dependência Linear",
                "cabecalho": ["Conceito", "Definição Geométrica", "Na Prática em IA"],
                "linhas": [
                    ["Linearmente Independentes (LI)", "Nenhum vetor pode ser escrito como combinação dos outros. Cada um adiciona uma dimensão nova.", "Features não redundantes. Cada atributo traz informação inédita."],
                    ["Linearmente Dependentes (LD)", "Pelo menos um vetor é supérfluo: ele já vive no span dos outros.", "Multicolinearidade: colunas duplicadas que aumentam o custo sem trazer novidade."],
                ],
            },
            {
                "tipo": "passos",
                "titulo": "Descobrindo as coordenadas em uma nova Base",
                "corpo": r"""<p>Uma <b>Base</b> de um espaço vetorial é um conjunto de vetores que cumpre duas regras de ouro: (1) são linearmente independentes e (2) seu span cobre todo o espaço.</p>
<p>A base padrão do plano 2D é $\hat{i} = [1, 0]$ e $\hat{j} = [0, 1]$. Vamos expressar o ponto do nosso cliente $\vec{p} = [5, 7]$ nessa base:</p>""",
                "passos": [
                    {"faca": r"Escrever a equação de combinação linear: $c_1 \begin{bmatrix} 1 \\ 0 \end{bmatrix} + c_2 \begin{bmatrix} 0 \\ 1 \end{bmatrix} = \begin{bmatrix} 5 \\ 7 \end{bmatrix}$.", "porque": "Queremos encontrar os escalares c1 e c2."},
                    {"faca": r"Linha 1: $c_1(1) + c_2(0) = 5 \implies c_1 = 5$.", "porque": "A coordenada X é determinada puramente pelo vetor unitário horizontal."},
                    {"faca": r"Linha 2: $c_1(0) + c_2(1) = 7 \implies c_2 = 7$.", "porque": "A coordenada Y é determinada pelo vetor unitário vertical."},
                ],
                "conclusao": r"""As coordenadas de um ponto nada mais são do que <b>os coeficientes da combinação linear</b> necessária para chegar até ele a partir dos vetores de base!""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Testando independência linear com posto (Rank)",
                "codigo": r'''import numpy as np

# Matriz cujas colunas são os vetores v1 e v2
# Caso 1: Independentes
A_li = np.array([[1.0, 0.0],
                 [0.0, 1.0]])
print("Posto (Rank) LI:", np.linalg.matrix_rank(A_li))  # 2 (cobre 2D)

# Caso 2: Dependentes (v2 = 2 * v1)
A_ld = np.array([[1.0, 2.0],
                 [2.0, 4.0]])
print("Posto (Rank) LD:", np.linalg.matrix_rank(A_ld))  # 1 (preso em 1D)''',
                "experimentos": [
                    r"Adicione uma terceira coluna à matriz A_li que seja a soma da primeira com a segunda: <code>[1.0, 1.0]</code>. O posto aumenta para 3 ou continua 2? Por quê?",
                ],
            },
        ],
        "resumo": [
            "Combinação linear é multiplicar vetores por escalares e somar tudo.",
            "Span é o conjunto de todos os pontos acessíveis por combinações lineares de um grupo de vetores.",
            "Vetores são linearmente independentes se nenhum deles puder ser montado a partir dos outros.",
            "Uma base é o conjunto mínimo de vetores independentes capaz de gerar todo o espaço.",
        ],
        "proxima": r"""Na <b>aula 3</b> vamos aprender a operação mais importante de toda a inteligência artificial: o <b>produto escalar</b>, que mede a sombra e a afinidade entre dois vetores.""",
        "referencias": [
            {"obra": "Gilbert Strang, <i>Introduction to Linear Algebra</i> (5ª ed.)", "trecho": "§2.1 Linear Independence, Basis and Dimension", "uso": "Definição de bases e independência"},
            {"obra": "Deisenroth, Faisal & Ong, <i>Mathematics for Machine Learning</i>", "trecho": "§2.3–2.4 Linear Independence and Basis", "uso": "Rigor formal de span e postos"},
            {"obra": "3Blue1Brown", "trecho": "Essence of Linear Algebra, cap. 2", "uso": "Visualização dinâmica do span"},
        ],
    },

    # 4. Norma de vetores (L1, L2) e distâncias
    "Norma de vetores (L1, L2 Euclidiana) e distâncias": {
        "v": 2,
        "duracao": 25,
        "gancho": r"""Quando uma rede neural aprende, como o algoritmo sabe se os pesos estão ficando grandes demais e decorando o ruído? E por que a escolha entre duas formas de medir distância matemática faz um modelo zerar variáveis inúteis ou apenas mantê-las pequeninas?""",
        "prerequisitos": ["Aula 1: vetores e coordenadas no plano cartesiano."],
        "objetivos": [
            "calcular a Norma L2 (Euclidiana) e a Norma L1 (Manhattan);",
            "compreender geometricamente como as curvas de nível de L1 (losango) e L2 (círculo) influenciam a regularização;",
            "entender por que a regularização Lasso (L1) gera esparsidade enquanto a Ridge (L2 / Weight Decay) apenas encolhe pesos;",
            "calcular normas e distâncias com NumPy e PyTorch.",
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "Medindo o Comprimento",
                "titulo": "O que é uma Norma?",
                "corpo": r"""<p>No dia a dia, medimos distâncias com uma régua direta. Mas na matemática e na IA, uma <b>Norma</b> $\|\vec{v}\|$ é uma função que atribui a cada vetor um comprimento estritamente positivo (ou zero para o vetor nulo). Existem duas normas que dominam todo o ecossistema de aprendizado de máquina:</p>
<ul>
<li><b>Norma $L_2$ (Euclidiana):</b> É a distância geométrica em linha reta direta, calculada pelo Teorema de Pitágoras estendido: $\|\vec{v}\|_2 = \sqrt{\sum v_i^2}$.</li>
<li><b>Norma $L_1$ (Manhattan / Cityblock):</b> É a soma dos valores absolutos dos passos em cada eixo: $\|\vec{v}\|_1 = \sum |v_i|$. Como um táxi nas ruas de Nova York, que não pode atravessar quarteirões na diagonal e precisa andar pelas avenidas ortogonais.</li>
</ul>""",
            },
            {
                "tipo": "passos",
                "titulo": "Cálculo Comparativo Passo a Passo com $\vec{v} = [3, -4]$",
                "passos": [
                    {"faca": r"Norma L1: somar os módulos $|3| + |-4| = 3 + 4 = \mathbf{7}$.", "porque": "A norma L1 ignora sinais negativos e mede o percurso em quarteirões."},
                    {"faca": r"Norma L2: elevar ao quadrado $3^2 + (-4)^2 = 9 + 16 = 25$.", "porque": "O quadrado penaliza distâncias maiores e elimina sinais."},
                    {"faca": r"Extrair a raiz quadrada: $\sqrt{25} = \mathbf{5}$.", "porque": "A raiz devolve a unidade de medida para a escala original (triângulo 3-4-5)."},
                ],
                "conclusao": r"""Note que $\|\vec{v}\|_2 \le \|\vec{v}\|_1$ sempre! A linha reta diagonal ($5$) é sempre o caminho mais curto que a rota em quarteirões ($7$).""",
            },
            {
                "tipo": "ponte",
                "titulo": "O Segredo da Regularização: Por que L1 zera pesos?",
                "corpo": r"""<p>Para evitar que redes neurais decorem os dados (overfitting), adicionamos à função de perda um termo que penaliza o tamanho dos pesos:</p>
$$\text{Perda Total} = \text{Erro de Previsão} + \lambda \|\vec{w}\|$$
<p>Se usamos a <b>Norma $L_1$ (Lasso)</b>, as curvas de nível da penalidade são <b>losangos com pontas afiadas sobre os eixos</b>. Quando as curvas elípticas do erro encostam no losango, quase sempre tocam em um dos vértices — onde uma das coordenadas é <b>exatamente zero</b>! Por isso L1 faz <i>seleção automática de features</i>, eliminando variáveis inúteis.</p>
<p>Se usamos a <b>Norma $L_2$ (Ridge / Weight Decay)</b>, as curvas de nível são <b>círculos perfeitamente suaves</b>. O ponto de contato raramente cai no eixo; ele apenas encolhe todos os pesos uniformemente para valores pequenos, sem zerá-los. Essa é a técnica usada para treinar Transformers como Llama e GPT!</p>""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Calculando normas com numpy.linalg",
                "codigo": r'''import numpy as np

v = np.array([3.0, -4.0])

l1 = np.linalg.norm(v, ord=1)
l2 = np.linalg.norm(v, ord=2)
linf = np.linalg.norm(v, ord=np.inf) # Norma máxima (valor absoluto do maior termo)

print(f"Vetor: {v}")
print(f"Norma L1 (Manhattan) : {l1:.1f}")  # 7.0
print(f"Norma L2 (Euclidiana): {l2:.1f}")  # 5.0
print(f"Norma L-infinito     : {linf:.1f}") # 4.0''',
                "experimentos": [
                    r"O que acontece com as normas de um vetor unitário como <code>[0.6, 0.8]</code>? Teste no código.",
                ],
            },
        ],
        "resumo": [
            "Norma L2 mede linha reta direta (Pitágoras). Norma L1 mede percurso em eixos perpendiculares (Manhattan).",
            "Norma L1 induz esparsidade (pesos viram exatamente zero), excelente para descartar atributos redundantes.",
            "Norma L2 (Weight Decay) impede explosão de parâmetros sem zerá-los, mantendo a estabilidade de redes neurais profundas.",
        ],
        "proxima": r"""Sabendo calcular comprimentos de vetores, como medimos o ângulo e o alinhamento de direção entre dois conceitos independentemente de seu tamanho? Na <b>aula 5</b> veremos a <b>Similaridade de Cosseno</b>.""",
        "referencias": [
            {"obra": "Goodfellow, Bengio & Courville, <i>Deep Learning</i>", "trecho": "§2.5 Norms e §7.1 Parameter Norm Penalties", "uso": "Regularização L1 vs L2 em aprendizado profundo"},
            {"obra": "Deisenroth, Faisal & Ong, <i>Mathematics for Machine Learning</i>", "trecho": "§3.1 Norms", "uso": "Propriedades formais das p-normas"},
        ],
    },

    # 5. Ângulo entre vetores e Similaridade de Cosseno
    "Ângulo entre vetores e Similaridade de Cosseno": {
        "v": 2,
        "duracao": 25,
        "gancho": r"""Um documento curto de um parágrafo diz: “Excelente café, atendimento impecável!”. Um artigo longo de três páginas elogia o mesmo café com as mesmas palavras repetidas dezenas de vezes. Seus vetores têm tamanhos completamente diferentes, mas como o sistema de busca sabe que o assunto é rigorosamente o mesmo?""",
        "prerequisitos": ["Aula 3: Produto Escalar.", "Aula 4: Normas Euclidiana L2."],
        "objetivos": [
            "calcular a similaridade de cosseno a partir do produto escalar e das normas L2;",
            "compreender por que a métrica independe do comprimento do texto ou magnitude dos vetores;",
            "interpretar a escala entre -1 (opostos), 0 (ortogonais) e +1 (idênticos em significado);",
            "aplicar a similaridade em embeddings reais de cafeteria.",
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "Isolando a Direção",
                "titulo": "A Fórmula do Cosseno",
                "corpo": r"""<p>Na aula 3 vimos que $\vec{u} \cdot \vec{v} = \|\vec{u}\| \|\vec{v}\| \cos\theta$. Se isolarmos o termo $\cos\theta$, obtemos a <b>Similaridade de Cosseno</b>:</p>
$$\cos\theta = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\|_2 \cdot \|\vec{v}\|_2} = \left(\frac{\vec{u}}{\|\vec{u}\|}\right) \cdot \left(\frac{\vec{v}}{\|\vec{v}\|}\right)$$
<p>Repare na elegância da segunda forma: <b>a similaridade de cosseno nada mais é do que o produto escalar entre os vetores após terem sido normalizados para tamanho 1!</b></p>""",
            },
            {
                "tipo": "passos",
                "titulo": "Calculando a Similaridade entre as avaliações da Cafeteria",
                "corpo": r"""<p>Vamos usar os embeddings 2D da nossa cafeteria: 'ótimo' $= [3, 2]$ e 'bom' $= [2, 1]$.</p>""",
                "passos": [
                    {"faca": r"Produto escalar: $3\times2 + 2\times1 = 6 + 2 = 8$.", "porque": "Mede a concordância bruta das coordenadas."},
                    {"faca": r"Norma L2 de 'ótimo': $\sqrt{3^2 + 2^2} = \sqrt{9 + 4} = \sqrt{13} \approx 3{,}6056$.", "porque": "Comprimento da primeira seta."},
                    {"faca": r"Norma L2 de 'bom': $\sqrt{2^2 + 1^2} = \sqrt{4 + 1} = \sqrt{5} \approx 2{,}2361$.", "porque": "Comprimento da segunda seta."},
                    {"faca": r"Divisão: $\dfrac{8}{\sqrt{13} \times \sqrt{5}} = \dfrac{8}{\sqrt{65}} = \dfrac{8}{8{,}0623} \approx \mathbf{0{,}9923}$.", "porque": "Normaliza pelo produto dos comprimentos."},
                ],
                "conclusao": r"""O cosseno é $0{,}9923$, o que corresponde a um ângulo de apenas $7{,}1^\circ$! O sistema de busca conclui com quase 100% de confiança que 'ótimo' e 'bom' apontam para o mesmo conceito semântico.""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Matriz de similaridade semântica com NumPy",
                "codigo": r'''import numpy as np

palavras = {
    "ótimo": np.array([3.0, 2.0]),
    "bom": np.array([2.0, 1.0]),
    "ruim": np.array([-2.0, 1.0]),
    "péssimo": np.array([-3.0, 2.0])
}

def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("ótimo vs bom    :", round(cos_sim(palavras["ótimo"], palavras["bom"]), 4))       # 0.9923
print("ótimo vs péssimo:", round(cos_sim(palavras["ótimo"], palavras["péssimo"]), 4))   # -0.3846
print("bom vs ruim     :", round(cos_sim(palavras["bom"], palavras["ruim"]), 4))         # -0.6000''',
                "experimentos": [
                    r"O que acontece se você multiplicar o vetor 'bom' por 1.000? A similaridade com 'ótimo' muda? Por que isso é vital para RAG?",
                ],
            },
        ],
        "resumo": [
            "Similaridade de cosseno mede o ângulo entre vetores, ignorando suas grandezas individuais.",
            "Varia de -1 (opostos polares) a +1 (idênticos em significado).",
            "É o padrão de fato para busca semântica, RAG e comparação de embeddings em IA.",
        ],
        "proxima": r"""Até aqui operamos em vetores isolados. Mas como transformamos o espaço todo de uma vez só? Na <b>aula 6</b> entenderemos <b>matrizes como transformações lineares no espaço</b>.""",
        "referencias": [
            {"obra": "Deisenroth, Faisal & Ong, <i>Mathematics for Machine Learning</i>", "trecho": "§3.3 Lengths and Distances", "uso": "Definição do ângulo em espaços euclidianos"},
            {"obra": "Goodfellow, Bengio & Courville, <i>Deep Learning</i>", "trecho": "§2.4 Cosine Similarity", "uso": "Uso em sistemas neurais e embeddings"},
        ],
    },

    # 6. Matrizes como transformações lineares no espaço
    "Matrizes como transformações lineares no espaço": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""O que acontece quando você olha para uma matriz cheia de números como $\begin{bmatrix} 2 & 1 \\ 0 & 1.5 \end{bmatrix}$? Se você só enxerga uma tabela estática, está perdendo a mágica: matrizes são máquinas dinâmicas que esticam, giram e deformam o próprio tecido do espaço!""",
        "prerequisitos": ["Aula 1: vetores e bases unitárias î e ĵ."],
        "objetivos": [
            "visualizar uma matriz como uma transformação linear do espaço;",
            "entender o segredo das colunas: a primeira coluna diz onde vai parar î, a segunda diz onde vai parar ĵ;",
            "prever onde qualquer ponto [x, y] vai parar através da combinação linear das colunas;",
            "reconhecer rotação, escala e cisalhamento (shear).",
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Revelação Visual",
                "titulo": "O Segredo das Colunas de uma Matriz",
                "corpo": r"""<p>3Blue1Brown popularizou a melhor intuição já concebida para matrizes: <b>as colunas de uma matriz dizem exatamente onde os vetores de base padrão foram parar após a transformação</b>!</p>
<p>Considere os vetores unitários de partida: $\hat{i} = [1, 0]$ (1 passo para a direita) e $\hat{j} = [0, 1]$ (1 passo para cima). Se aplicamos uma matriz $A$ sobre eles:</p>
$$A \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} a \\ c \end{bmatrix} \quad (\text{1ª coluna!})$$
$$A \begin{bmatrix} 0 \\ 1 \end{bmatrix} = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \begin{bmatrix} 0 \\ 1 \end{bmatrix} = \begin{bmatrix} b \\ d \end{bmatrix} \quad (\text{2ª coluna!})$$
<p>Isso é libertador! Para saber o que qualquer matriz faz com o universo, basta olhar para onde ela levou $\hat{i}$ e $\hat{j}$.</p>""",
            },
            {
                "tipo": "visual",
                "titulo": "A Deformação Linear da Grade",
                "svg": SVG_TRANSF_LINEAR,
                "legenda": "A matriz A levou î=[1,0] para [2,0] e levou ĵ=[0,1] para [1, 1.5]. Todo o resto da grade acompanha proporcionalmente!",
            },
            {
                "tipo": "passos",
                "titulo": "Prevendo onde o ponto [3, 2] vai parar",
                "passos": [
                    {"faca": r"Decompor o ponto inicial na base: $[3, 2] = 3\hat{i} + 2\hat{j}$.", "porque": "Três passos na direção de î e dois na de ĵ."},
                    {"faca": r"Como a transformação é linear, ela respeita a mesma proporção: $A [3, 2] = 3 (A\hat{i}) + 2 (A\hat{j})$.", "porque": "A linearidade garante que retas continuam retas e a origem permanece fixa."},
                    {"faca": r"Substituir as colunas transformadas: $3 \begin{bmatrix} 2 \\ 0 \end{bmatrix} + 2 \begin{bmatrix} 1 \\ 1{,}5 \end{bmatrix} = \begin{bmatrix} 6 \\ 0 \end{bmatrix} + \begin{bmatrix} 2 \\ 3 \end{bmatrix} = \begin{bmatrix} 8 \\ 3 \end{bmatrix}$.", "porque": "Basta somar as contribuições."},
                ],
                "conclusao": r"""O ponto $[3, 2]$ foi transformado em $[8, 3]$! Em uma rede neural, cada camada densa faz exatamente isso: deforma o espaço de atributos para tornar classes separáveis.""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Transformando vetores com matrizes em NumPy",
                "codigo": r'''import numpy as np

# Matriz que cisalha e estica
A = np.array([[2.0, 1.0],
              [0.0, 1.5]])

# Ponto original
x = np.array([3.0, 2.0])

# Transformacao linear via operador @
y = A @ x
print(f"Ponto original : {x}")
print(f"Ponto projetado: {y}") # [8. 3.]''',
                "experimentos": [
                    r"O que faz a matriz de rotação 90°: <code>A = np.array([[0, -1], [1, 0]])</code>? Teste com o vetor <code>[1, 0]</code>.",
                ],
            },
        ],
        "resumo": [
            "Matrizes são transformações lineares que movem o espaço mantendo a origem fixa e linhas retas como retas.",
            "As colunas de uma matriz representam onde foram parar os vetores de base unitários.",
            "Multiplicar uma matriz por um vetor é computar a combinação linear de suas colunas ponderadas pelas coordenadas do vetor.",
        ],
        "proxima": r"""Agora que entendemos a ação de uma matriz sobre um vetor, o que acontece quando multiplicamos duas matrizes seguidas? Na <b>aula 7</b> veremos a <b>Multiplicação de Matrizes</b>.""",
        "referencias": [
            {"obra": "Gilbert Strang, <i>Introduction to Linear Algebra</i> (5ª ed.)", "trecho": "§7.1 The Idea of a Linear Transformation", "uso": "Conceito de transformações lineares"},
            {"obra": "3Blue1Brown", "trecho": "Essence of Linear Algebra, cap. 3", "uso": "Intuição das colunas como novos vetores de base"},
        ],
    },

    # 7. Multiplicação de matrizes
    "Multiplicação de matrizes (Dot product vs. Hadamard elemento a elemento)": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Por que a NVIDIA se tornou uma das empresas mais valiosas do planeta construindo GPUs e Tensor Cores? Porque o treino de redes neurais e Transformers se resume a uma única operação repetida trilhões de vezes: a multiplicação de matrizes.""",
        "prerequisitos": ["Aula 3: Produto Escalar.", "Aula 6: Matrizes como transformações."],
        "objetivos": [
            "distinguir a multiplicação matricial real ($A B$) do produto de Hadamard elemento a elemento ($A \\odot B$);",
            "dominar a regra de compatibilidade de dimensões $(m \\times k) \\times (k \\times n) = (m \\times n)$;",
            "enxergar a multiplicação sob duas perspectivas: produtos escalares de linhas por colunas ou composição de transformações;",
            "entender por que a ordem importa: $A B \\neq B A$.",
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "Diferença Vital",
                "titulo": "Produto Matricial vs Produto de Hadamard",
                "corpo": r"""<p>Em programação e em matemática, existem duas formas completamente distintas de 'multiplicar' duas tabelas de números:</p>
<ul>
<li><b>Multiplicação Matricial Clássica ($A B$):</b> Cada célula $(i, j)$ da matriz resultante é o <b>produto escalar da linha $i$ de $A$ com a coluna $j$ de $B$</b>. Representa a composição de transformações lineares. Em Python/NumPy, usa-se o operador <code>@</code> ou <code>np.matmul</code>.</li>
<li><b>Produto de Hadamard ($A \odot B$):</b> Multiplica simplesmente os números que estão na mesma posição: $C_{ij} = A_{ij} \times B_{ij}$. As matrizes precisam ter exatamente o mesmo tamanho. Em Python, usa-se o operador asterisco <code>*</code>.</li>
</ul>
<p>Confundir <code>*</code> com <code>@</code> é a causa de 90% dos bugs de dimensões de quem está começando a programar PyTorch!</p>""",
            },
            {
                "tipo": "passos",
                "titulo": "Regra dos Shapes e Cálculo Linha x Coluna",
                "corpo": r"""<p>Para poder multiplicar $A \times B$, o número de colunas da primeira deve ser rigorosamente igual ao número de linhas da segunda:</p>
$$(2 \times \mathbf{3}) \times (\mathbf{3} \times 2) \implies (2 \times 2)$$""",
                "passos": [
                    {"faca": r"Sejam $A = \begin{bmatrix} 1 & 2 & 0 \\ 0 & 1 & 1 \end{bmatrix}$ e $B = \begin{bmatrix} 1 & 0 \\ 2 & 1 \\ 0 & 3 \end{bmatrix}$.", "porque": "Shape de A é (2, 3) e de B é (3, 2)."},
                    {"faca": r"Célula (1, 1): linha 1 de A com coluna 1 de B: $1(1) + 2(2) + 0(0) = 1 + 4 + 0 = \mathbf{5}$.", "porque": "Produto escalar da 1ª linha com 1ª coluna."},
                    {"faca": r"Célula (1, 2): linha 1 de A com coluna 2 de B: $1(0) + 2(1) + 0(3) = 0 + 2 + 0 = \mathbf{2}$.", "porque": "Produto escalar da 1ª linha com 2ª coluna."},
                    {"faca": r"Célula (2, 1): linha 2 de A com coluna 1 de B: $0(1) + 1(2) + 1(0) = 0 + 2 + 0 = \mathbf{2}$.", "porque": "Produto escalar da 2ª linha com 1ª coluna."},
                    {"faca": r"Célula (2, 2): linha 2 de A com coluna 2 de B: $0(0) + 1(1) + 1(3) = 0 + 1 + 3 = \mathbf{4}$.", "porque": "Produto escalar da 2ª linha com 2ª coluna."},
                ],
                "conclusao": r"""O resultado é a matriz $\begin{bmatrix} 5 & 2 \\ 2 & 4 \end{bmatrix}$. Ela condensa quatro produtos escalares simultâneos!""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Comparando @ com * em NumPy",
                "codigo": r'''import numpy as np

A = np.array([[1, 2],
              [3, 4]])
B = np.array([[2, 0],
              [1, 2]])

# 1. Produto matricial real (composição)
real = A @ B
print("Produto Matricial (A @ B):\n", real)

# 2. Produto de Hadamard (elemento a elemento)
hadamard = A * B
print("Produto de Hadamard (A * B):\n", hadamard)''',
                "experimentos": [
                    r"Calcule <code>B @ A</code> no terminal. O resultado é igual a <code>A @ B</code>? A multiplicação de matrizes é comutativa?",
                ],
            },
        ],
        "resumo": [
            "Multiplicação matricial A @ B compõe transformações e calcula produtos escalares entre linhas de A e colunas de B.",
            "Produto de Hadamard A * B multiplica valores nas mesmas posições e não é a mesma coisa.",
            "Compatibilidade de shapes: (M x K) @ (K x N) resulta em (M x N).",
            "A ordem importa: quase sempre A @ B != B @ A.",
        ],
        "proxima": r"""Na <b>aula 8</b> veremos como sistemas de equações lineares se expressam como $A x = b$ e o que o <b>determinante</b> nos revela sobre a preservação de volume.""",
        "referencias": [
            {"obra": "Gilbert Strang, <i>Introduction to Linear Algebra</i> (5ª ed.)", "trecho": "§1.3 Matrices and §2.4 Rules for Matrix Operations", "uso": "Multiplicação por blocos, linhas e colunas"},
            {"obra": "Goodfellow, Bengio & Courville, <i>Deep Learning</i>", "trecho": "§2.2 Multiplying Matrices and Vectors", "uso": "Diferenciação entre produto matricial e Hadamard"},
        ],
    },

    # 8. Sistemas lineares e determinantes
    "Sistemas de equações lineares e determinantes": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""O que o número do Determinante mede na geometria real? E por que se o determinante de uma matriz for zero, é impossível recuperar a informação original de uma imagem ou vetor?""",
        "prerequisitos": ["Aula 6: matrizes como transformações do espaço."],
        "objetivos": [
            "escrever qualquer sistema de equações na forma matricial compacta $A \vec{x} = \vec{b}$;",
            "compreender o Determinante como o fator de escala de área (2D) ou volume (3D);",
            "identificar quando um sistema tem solução única ($\det(A) \neq 0$) ou infinitas/nenhuma solução ($\det(A) = 0$).",
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Geometria do Determinante",
                "titulo": "O que o Determinante mede de verdade?",
                "corpo": r"""<p>3Blue1Brown e Strang apresentam a forma mais intuitiva de entender o <b>Determinante ($\det(A)$)</b>: ele mede <b>o quanto a transformação linear multiplica a área (em 2D) ou o volume (em 3D) de qualquer figura</b>!</p>
<ul>
<li>Se $\det(A) = 3$: Qualquer quadrado de área $1$ vira um paralelogramo de área $3$. A transformação triplicou as áreas.</li>
<li>Se $\det(A) = 1$: As figuras mudam de formato, mas a área se conserva (como em uma rotação pura).</li>
<li>Se $\det(A) < 0$: O espaço foi invertido como em um espelho (mudança de orientação, como virar a mão esquerda na direita).</li>
<li><b>Se $\det(A) = 0$:</b> O espaço foi <b>completamente esmagado</b> em uma dimensão menor (um plano 2D virou uma linha reta, ou um volume 3D virou uma folha plana). Informação foi destruída para sempre!</li>
</ul>""",
            },
            {
                "tipo": "passos",
                "titulo": "Cálculo Passo a Passo em Matriz 2x2",
                "corpo": r"""$$\det\begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc$$""",
                "passos": [
                    {"faca": r"Seja $A = \begin{bmatrix} 3 & 1 \\ 2 & 4 \end{bmatrix}$.", "porque": "Matriz com colunas [3, 2] e [1, 4]."},
                    {"faca": r"Diagonal principal: $3 \times 4 = 12$.", "porque": "Multiplicação ad."},
                    {"faca": r"Diagonal secundária: $1 \times 2 = 2$.", "porque": "Multiplicação bc."},
                    {"faca": r"Subtração: $12 - 2 = \mathbf{10}$.", "porque": "O determinante vale 10."},
                ],
                "conclusao": r"""O determinante é $10 \neq 0$. Isso garante que o sistema linear correspondente tem solução única e que o espaço não foi colapsado!""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Resolvendo sistemas Ax = b em NumPy",
                "codigo": r'''import numpy as np

# Sistema:
# 3x + 1y = 9
# 2x + 4y = 16
A = np.array([[3.0, 1.0],
              [2.0, 4.0]])
b = np.array([9.0, 16.0])

# Determinante
det = np.linalg.det(A)
print(f"Determinante: {det:.2f}")

# Solucao exata x = [2, 3]
x = np.linalg.solve(A, b)
print(f"Solução [x, y]: {x}")''',
                "experimentos": [
                    r"Crie uma matriz com linhas duplicadas: <code>A = np.array([[2, 4], [1, 2]])</code>. Quanto dá o determinante? O que acontece se tentar rodar <code>np.linalg.solve</code>?",
                ],
            },
        ],
        "resumo": [
            "Sistemas lineares se escrevem na forma compacta A x = b.",
            "O determinante mede o fator de multiplicação de área ou volume.",
            "Determinante zero indica perda irrecuperável de dimensão (matriz singular).",
        ],
        "proxima": r"""Se uma matriz não esmagou o espaço ($\det \neq 0$), nós podemos 'desfazer' sua transformação? Na <b>aula 9</b> veremos a <b>Matriz Inversa e a Pseudoinversa de Moore-Penrose</b>.""",
        "referencias": [
            {"obra": "Gilbert Strang, <i>Introduction to Linear Algebra</i> (5ª ed.)", "trecho": "§5.1 The Properties of Determinants", "uso": "Propriedades geométricas dos determinantes"},
            {"obra": "3Blue1Brown", "trecho": "Essence of Linear Algebra, cap. 6", "uso": "Determinante como expansão de área"},
        ],
    },

    # 9. Inversa e pseudoinversa
    "Inversa de matriz e pseudoinversa de Moore-Penrose": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Como desfazer o que uma matriz fez? E o que fazer quando temos 1.000 dados de treino e apenas 2 parâmetros, gerando um sistema com mais equações do que incógnitas onde é matematicamente impossível achar uma inversa exata?""",
        "prerequisitos": ["Aula 8: Sistemas lineares e Determinantes."],
        "objetivos": [
            "compreender a Matriz Inversa $A^{-1}$ como a operação que desfaz a transformação linear ($A^{-1} A = I$);",
            "entender por que sistemas retangulares (mais amostras que variáveis) exigem a Pseudoinversa de Moore-Penrose $A^+$;",
            "deduzir a solução exata dos Mínimos Quadrados da Regressão Linear: $\vec{w} = (X^\top X)^{-1} X^\top \vec{y}$.",
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "Desfazendo o Filme",
                "titulo": "A Matriz Inversa",
                "corpo": r"""<p>Se uma matriz $A$ girou e esticou um vetor, a <b>Matriz Inversa $A^{-1}$</b> é a transformação que roda o filme ao contrário, devolvendo cada ponto à sua posição original:</p>
$$A^{-1} A = A A^{-1} = I \quad (\text{Matriz Identidade})$$
<p>Para $A^{-1}$ existir, a matriz precisa ser quadrada e seu determinante não pode ser zero ($\det(A) \neq 0$). Se o espaço foi esmagado para uma linha ($\det = 0$), múltiplos pontos caíram no mesmo lugar e não há como saber de onde cada um veio!</p>""",
            },
            {
                "tipo": "ponte",
                "titulo": "O Mundo Real da IA: Mais dados do que incógnitas",
                "corpo": r"""<p>Na ciência de dados e machine learning, quase nunca temos matrizes quadradas. Temos $N = 100.000$ linhas (exemplos) e apenas $d = 10$ colunas (features). A matriz de dados $X$ tem formato $(100.000 \times 10)$.</p>
<p>O sistema $X \vec{w} = \vec{y}$ não tem solução exata (é impossível uma única reta passar exatamente por 100 mil pontos ruidosos). A solução é encontrar o vetor de pesos $\vec{w}$ que <b>minimiza o erro quadrático</b>.</p>
<p>Isso é feito pela <b>Pseudoinversa de Moore-Penrose ($X^+$)</b>:</p>
$$X^+ = (X^\top X)^{-1} X^\top \implies \vec{w}^* = X^+ \vec{y} = (X^\top X)^{-1} X^\top \vec{y}$$
<p>Essa fórmula histórica (a solução analítica dos Mínimos Quadrados Ordinários - OLS) é a base de toda a regressão linear clássica!</p>""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Calculando a Pseudoinversa com NumPy",
                "codigo": r'''import numpy as np

# Matriz retangular (3 exemplos, 2 features)
X = np.array([[1.0, 1.0],
              [1.0, 2.0],
              [1.0, 3.0]])
y = np.array([2.0, 2.5, 3.5])

# Calculo analitico da pseudoinversa via pinv
X_pinv = np.linalg.pinv(X)
w_otimo = X_pinv @ y

print("Pesos ótimos [intercepto, inclinação]:", w_otimo.round(3))
# Formula manual de Moore-Penrose: (X.T @ X)^-1 @ X.T
manual_pinv = np.linalg.inv(X.T @ X) @ X.T
print("Diferença da fórmula manual:", np.max(np.abs(X_pinv - manual_pinv)))''',
                "experimentos": [
                    r"Verifique que <code>X_pinv @ X</code> resulta na matriz identidade 2x2 <code>[[1, 0], [0, 1]]</code>.",
                ],
            },
        ],
        "resumo": [
            "A inversa A^-1 desfaz a transformação linear, existindo apenas para matrizes quadradas não singulares.",
            "Para matrizes retangulares com mais dados que atributos, a Pseudoinversa de Moore-Penrose encontra a solução de mínimos quadrados.",
            "w = (X^T X)^-1 X^T y é a fórmula fechada da regressão linear.",
        ],
        "proxima": r"""Existem direções especiais em uma matriz que não giram quando ela atua, apenas esticam? Na <b>aula 10</b> estudaremos <b>Autovalores e Autovetores</b>.""",
        "referencias": [
            {"obra": "Gilbert Strang, <i>Introduction to Linear Algebra</i> (5ª ed.)", "trecho": "§4.3 Projections and §4.4 Least Squares Approximations", "uso": "Dedução dos mínimos quadrados e Moore-Penrose"},
            {"obra": "Goodfellow, Bengio & Courville, <i>Deep Learning</i>", "trecho": "§2.9 The Moore-Penrose Pseudoinverse", "uso": "Aplicações em aprendizado de máquina"},
        ],
    },

    # 10. Autovalores e Autovetores
    "Autovalores e Autovetores (Eigenvalues & Eigenvectors)": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""A maioria dos vetores muda de direção quando uma matriz atua sobre eles: uma seta que apontava para o nordeste passa a apontar para o leste. Mas em quase toda matriz, existem eixos privilegiados que permanecem rigorosamente na mesma reta, apenas esticando ou encolhendo. Descobrir esses eixos é o segredo do PageRank do Google e da compressão de imagens.""",
        "prerequisitos": ["Aula 6: Matrizes como transformações.", "Aula 8: Determinantes."],
        "objetivos": [
            "compreender a equação fundamental $A \vec{v} = \lambda \vec{v}$;",
            "interpretar autovetores como eixos de rotação/estiramento invariantes e autovalores como o fator de escala;",
            "calcular autovalores através da equação característica $\det(A - \lambda I) = 0$;",
            "reconhecer o papel de autovetores em estabilidade, PageRank e PCA.",
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Equação dos Eixos Sagrados",
                "titulo": "O que significa A v = λ v?",
                "corpo": r"""<p>Normalmente, multiplicar uma matriz $A$ por um vetor $\vec{v}$ muda o tamanho E a direção da seta. Mas para alguns vetores especiais $\vec{v}$, o resultado é matematicamente equivalente a simplesmente multiplicar o vetor por um número escalar $\lambda$ (a letra grega <i>lambda</i>):</p>
$$A \vec{v} = \lambda \vec{v}$$
<ul>
<li>$\vec{v}$ é o <b>Autovetor</b> (<i>eigenvector</i>): ele define o <b>eixo invariante</b>. Ele não sai da reta sobre a qual está apoiado.</li>
<li>$\lambda$ é o <b>Autovalor</b> (<i>eigenvalue</i>): é o <b>fator de esticamento</b>. Se $\lambda = 2$, o vetor dobra de tamanho. Se $\lambda = 0.5$, encolhe pela metade. Se $\lambda < 0$, inverte o sentido.</li>
</ul>""",
            },
            {
                "tipo": "passos",
                "titulo": "Como encontrar os Autovalores: a Equação Característica",
                "corpo": r"""<p>Reescrevendo $A \vec{v} = \lambda \vec{v}$:</p>
$$(A - \lambda I) \vec{v} = \vec{0}$$
<p>Para que exista uma solução $\vec{v}$ diferente de zero, a matriz $(A - \lambda I)$ precisa obrigatoriamente ter determinante igual a zero:</p>
$$\det(A - \lambda I) = 0$$""",
                "passos": [
                    {"faca": r"Seja $A = \begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$. Subtrair $\lambda$ na diagonal: $\begin{bmatrix} 4 - \lambda & 1 \\ 2 & 3 - \lambda \end{bmatrix}$.", "porque": "Construir a matriz A - lambda I."},
                    {"faca": r"Calcular o determinante: $(4 - \lambda)(3 - \lambda) - (1)(2) = 12 - 7\lambda + \lambda^2 - 2 = \lambda^2 - 7\lambda + 10$.", "porque": "Equação quadrática característica."},
                    {"faca": r"Igualar a zero: $\lambda^2 - 7\lambda + 10 = 0 \implies (\lambda - 5)(\lambda - 2) = 0$.", "porque": "Fatorar o polinômio."},
                    {"faca": r"Autovalores encontrados: $\lambda_1 = 5$ e $\lambda_2 = 2$.", "porque": "As raízes da equação."},
                ],
                "conclusao": r"""A matriz tem dois autovalores reais: um eixo principal que estica 5 vezes ($\lambda_1 = 5$) e um eixo secundário que estica 2 vezes ($\lambda_2 = 2$).""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Calculando eigendecomposition com NumPy",
                "codigo": r'''import numpy as np

A = np.array([[4.0, 1.0],
              [2.0, 3.0]])

# Funcao especializada de autovalores e autovetores
autovalores, autovetores = np.linalg.eig(A)

print("Autovalores encontrados:", autovalores) # [5. 2.]
print("Autovetores (colunas):\n", autovetores.round(3))

# Verificando A @ v = lambda * v para o primeiro autovetor
v1 = autovetores[:, 0]
l1 = autovalores[0]

print("A @ v1     :", (A @ v1).round(3))
print("lambda1 * v1:", (l1 * v1).round(3))''',
                "experimentos": [
                    r"Observe que <code>A @ v1</code> e <code>l1 * v1</code> são rigorosamente idênticos! O autovetor não mudou de direção.",
                ],
            },
        ],
        "resumo": [
            "A v = lambda v: autovetores são direções que não rotacionam sob a matriz; autovalores são os fatores de esticamento.",
            "Encontrados através da equação característica det(A - lambda I) = 0.",
            "Estruturam o PCA, decomposições espectrais e algoritmos como o PageRank.",
        ],
        "proxima": r"""Na <b>aula 11</b> encerraremos o Módulo 1 com a jóia da coroa da álgebra linear moderna: a <b>Decomposição em Valores Singulares (SVD) e o PCA</b>.""",
        "referencias": [
            {"obra": "Gilbert Strang, <i>Introduction to Linear Algebra</i> (5ª ed.)", "trecho": "§6.1 Introduction to Eigenvalues", "uso": "Intuição de autovetores como eixos estáveis"},
            {"obra": "Deisenroth, Faisal & Ong, <i>Mathematics for Machine Learning</i>", "trecho": "§4.1–4.2 Eigenvalues and Eigenvectors", "uso": "Propriedades espectrais"},
        ],
    },

    # 11. SVD e PCA
    "Decomposição em Valores Singulares (SVD) e PCA": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Como comprimir uma imagem de 10 Megabytes para apenas 500 Kilobytes preservando todas as feições principais? E como reduzir uma tabela com 500 características de clientes para apenas 2 eixos para plotar em um gráfico 2D sem perder a variabilidade dos dados? A resposta é o PCA e o SVD.""",
        "prerequisitos": ["Aula 10: Autovalores e Autovetores.", "Aula 4: Normas e Distâncias."],
        "objetivos": [
            "compreender o teorema do SVD: qualquer matriz pode ser decomposta em $A = U \Sigma V^\top$;",
            "interpretar a tríade geométrica: Rotação $\to$ Escala $\to$ Rotação;",
            "entender o PCA (Principal Component Analysis) como a busca pelas direções de máxima variância;",
            "usar PCA para comprimir e descompactar dados com NumPy.",
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "O Teorema Fundamental",
                "titulo": "SVD: A Fatoração Suprema da Álgebra Linear",
                "corpo": r"""<p>Strang descreve a <b>Decomposição em Valores Singulares (SVD)</b> como o ápice de todo o curso de Álgebra Linear. Enquanto autovalores só funcionam em matrizes quadradas, o SVD funciona para <b>QUALQUER matriz retangular</b> de qualquer tamanho $(m \times n)$:</p>
$$A = U \Sigma V^\top$$
<ul>
<li>$U$ (matriz ortogonal $m \times m$): Rotação no espaço de saída. Suas colunas são os autovetores de $A A^\top$.</li>
<li>$\Sigma$ (matriz diagonal $m \times n$): Valores singulares ($\sigma_1 \ge \sigma_2 \ge \dots \ge 0$). Fatores de escala ordenados por relevância.</li>
<li>$V^\top$ (matriz ortogonal $n \times n$): Rotação no espaço de entrada. Suas linhas são os autovetores de $A^\top A$.</li>
</ul>
<p>Geometricamente, <b>qualquer matriz retangular do universo pode ser entendida como uma rotação, seguida de um esticamento nos eixos principais, seguido de outra rotação</b>!</p>""",
            },
            {
                "tipo": "ponte",
                "titulo": "PCA: Redução de Dimensionalidade sem Mistério",
                "corpo": r"""<p>O <b>PCA (Análise de Componentes Principais)</b> usa exatamente o SVD na matriz de dados centrada na média:</p>
<ol>
<li>O <b>1º Componente Principal</b> é a reta que passa pela nuvem de dados capturando a <b>maior variância possível</b> (espalhamento dos dados).</li>
<li>O <b>2º Componente Principal</b> é perpendicular ao primeiro e captura a maior variância restante.</li>
</ol>
<p>Se mantivermos apenas os $k$ primeiros componentes e descartarmos o restante, comprimimos os dados preservando a esmagadora maioria da informação original. Isso é fundamental para visualizar clusters de embeddings em 2D com ferramentas como t-SNE e UMAP!</p>""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Comprimindo dados com SVD em NumPy",
                "codigo": r'''import numpy as np

# Matriz 4x3 simulando dados
A = np.array([[2.0, 4.0, 1.0],
              [3.0, 6.0, 2.0],
              [1.0, 2.0, 0.5],
              [4.0, 8.0, 1.5]])

# Decomposicao SVD completa
U, S, Vt = np.linalg.svd(A)

print("Valores singulares (S):", S.round(2))
# Observe que o 1o valor singular domina a variancia:
print(f"Energia do 1o componente: {(S[0]**2 / np.sum(S**2))*100:.1f}%")

# Reconstrucao de rank 1 (comprimida)
A_comprimida = U[:, :1] * S[0] @ Vt[:1, :]
print("Matriz reconstruída com 1 único componente:\n", A_comprimida.round(2))''',
                "experimentos": [
                    r"Compare a matriz original <code>A</code> com <code>A_comprimida</code>. Como o segundo atributo é praticamente o dobro do primeiro, 1 componente sozinho preserva mais de 98% da informação!",
                ],
            },
        ],
        "resumo": [
            "SVD fatora qualquer matriz em A = U Sigma V^T (rotação, escala, rotação).",
            "PCA encontra as direções de máxima variância nos dados, permitindo descartar ruídos e comprimir dados.",
            "Fundamenta sistemas de recomendação (filtragem colaborativa), compressão de imagens e visualização de embeddings.",
        ],
        "proxima": r"""Com a Álgebra Linear dominada, completamos o Módulo 1! No <b>Módulo 2 (aula 12)</b> iniciaremos o <b>Cálculo Diferencial</b>, a linguagem que permite às redes neurais aprender através de taxas de variação instantânea.""",
        "referencias": [
            {"obra": "Gilbert Strang, <i>Introduction to Linear Algebra</i> (5ª ed.)", "trecho": "§7.2 Bases and Matrices in the SVD", "uso": "Geometria do SVD"},
            {"obra": "Goodfellow, Bengio & Courville, <i>Deep Learning</i>", "trecho": "§2.8 Singular Value Decomposition e §2.12 Principal Components Analysis", "uso": "SVD e PCA aplicados ao aprendizado de máquina"},
            {"obra": "Deisenroth, Faisal & Ong, <i>Mathematics for Machine Learning</i>", "trecho": "§10.1–10.4 Principal Component Analysis", "uso": "Derivação passo a passo do PCA"},
        ],
    },
}
