# -*- coding: utf-8 -*-
"""
Gerador de dados 100% em Português (PT-BR) para a Trilha de Matemática Essencial para IA (43 tópicos).
Inclui:
- Apostila Interativa Completa em Português (Intuição, Fórmula Explicada, Exemplo Passo a Passo e Código Python) para cada um dos 43 tópicos.
- Links de leitura e livros abertos 100% em Português (UFRGS REAMAT, Khan Academy PT-BR, Deep Learning Book Brasil e Wikipédia Matemática PT).
- Links de videoaulas em Português (professores brasileiros + animações 3B1B com legendas/áudio PT-BR forçados).
"""

def get_enriched_mat_phases():
    return [
        {
            "t": "Módulo 1 · Álgebra Linear para IA & Tensores",
            "d": "3 a 4 semanas",
            "tip": "💡 <b>Dica de Ouro:</b> Não decore fórmulas secas! Clique no botão azul <b>📘 Apostila PT-BR</b> de cada tópico para ler a explicação passo a passo em português, ver o exemplo resolvido na mão e testar o código em Python.",
            "p": "Implementar multiplicação de matrizes pura em Python e comparar o tempo de execução com `numpy.dot` e `torch.matmul`.",
            "r": "Apostila Interativa Integrada em Português · Livro Aberto Álgebra Linear UFRGS (REAMAT) · Khan Academy Brasil · Canal Prof. Grings & Matemática Rapidola",
            "g": [
                [
                    "Vetores e Operações",
                    [
                        {
                            "title": "Vetores e espaços vetoriais: intuição geométrica",
                            "video_url": "https://www.youtube.com/watch?v=fNk_zzaMoSs",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=vetores+algebra+linear+aula+portugues+grings",
                            "doc_url": "https://pt.khanacademy.org/math/linear-algebra/vectors-and-spaces/vectors/v/vector-introduction-linear-algebra",
                            "doc_label": "📘 Apostila PT-BR: Vetores",
                            "pt_guide": {
                                "intuicao": "Na Física, um vetor é uma seta no espaço com tamanho e direção. Na Computação e na IA, um <b>vetor é simplesmente uma lista ordenada de números</b> (por exemplo, as características de um imóvel: `[área, quartos, idade]`). Geométrica e algebricamente são a mesma coisa: cada número da lista é uma coordenada que diz o quanto andar nos eixos X, Y, Z...",
                                "formula": "$$\\vec{v} = \\begin{bmatrix} x_1 \\\\ x_2 \\\\ \\vdots \\\\ x_n \\end{bmatrix} \\in \\mathbb{R}^n$$\nOnde $\\mathbb{R}^n$ significa um espaço com $n$ dimensões reais (ex.: um embedding da OpenAI vive em $\\mathbb{R}^{1536}$, ou seja, uma lista de 1.536 números).",
                                "exemplo": "Imagine representar dois clientes de um banco como vetores 2D: `[renda_mensal_mil, score_credito_cem]`.\n• Cliente A: $\\vec{a} = [5, 8]$\n• Cliente B: $\\vec{b} = [3, 6]$\nSomar os dois vetores é somar posição por posição: $\\vec{a} + \\vec{b} = [5+3, 8+6] = [8, 14]$. Multiplicar por um número (escalar $2$) estica o vetor: $2 \\cdot \\vec{a} = [10, 16]$.",
                                "codigo": "import numpy as np\n\n# Criando dois vetores em Python (NumPy)\na = np.array([5, 8])\nb = np.array([3, 6])\n\nprint('Soma vetorial:', a + b)         # [ 8 14]\nprint('Multiplicação por escalar:', 2 * a) # [10 16]"
                            }
                        },
                        {
                            "title": "Combinações lineares, espaço gerado (span) e bases",
                            "video_url": "https://www.youtube.com/watch?v=k7RM-ot2NWY",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=combinacao+linear+espaco+gerado+base+algebra+linear+portugues",
                            "doc_url": "https://www.ufrgs.br/reamat/AlgebraLinear/livro/s5-combinacao_linear.html",
                            "doc_label": "📘 Apostila PT-BR: Span & Bases",
                            "pt_guide": {
                                "intuicao": "<b>Combinação Linear</b> é misturar vetores multiplicando cada um por um peso ($c_1, c_2...$) e somando tudo — exatamente o que um neurônio artificial faz com os dados de entrada! O <b>Espaço Gerado (Span)</b> é o conjunto de todos os pontos que você consegue alcançar fazendo essas misturas. Já uma <b>Base</b> é o conjunto mínimo de vetores independentes (que não são redundantes) capazes de gerar todo o espaço.",
                                "formula": "$$\\vec{w} = c_1 \\vec{v}_1 + c_2 \\vec{v}_2 + \\dots + c_k \\vec{v}_k$$\n• $\\vec{v}_1, \\vec{v}_2$: Vetores de base (direções fundamentais)\n• $c_1, c_2$: Pesos escalares (quanto usamos de cada vetor)",
                                "exemplo": "No plano 2D, os vetores padrão são $\\hat{i} = [1, 0]$ (passo para a direita) e $\\hat{j} = [0, 1]$ (passo para cima).\nPara chegar ao ponto $[4, 7]$, fazemos a combinação linear:\n$$4 \\cdot [1, 0] + 7 \\cdot [0, 1] = [4, 0] + [0, 7] = [4, 7]$$\nComo $\\hat{i}$ e $\\hat{j}$ apontam em direções diferentes, o <b>Span</b> deles cobre todo o plano 2D! Mas se tivéssemos $[1, 2]$ e $[2, 4]$ (um é o dobro do outro), eles estariam presos na mesma linha reta (são linearmente dependentes).",
                                "codigo": "import numpy as np\n\nv1 = np.array([1, 0])\nv2 = np.array([0, 1])\n\n# Combinação linear com pesos c1 = 4 e c2 = 7\nc1, c2 = 4, 7\nresultado = c1 * v1 + c2 * v2\nprint('Ponto alcançado no espaço:', resultado) # [4 7]"
                            }
                        },
                        {
                            "title": "Produto escalar (Dot Product) e projeções",
                            "video_url": "https://www.youtube.com/watch?v=LyGKycYT2v0",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=produto+escalar+projecao+vetores+aula+portugues",
                            "doc_url": "https://pt.khanacademy.org/math/linear-algebra/vectors-and-spaces/dot-cross-products/v/vector-dot-product-and-vector-length",
                            "doc_label": "📘 Apostila PT-BR: Produto Escalar",
                            "pt_guide": {
                                "intuicao": "O <b>Produto Escalar (Dot Product)</b> é a operação mais importante de toda a Inteligência Artificial! Você pega dois vetores do mesmo tamanho, multiplica os elementos de mesma posição e soma tudo, gerando um único número. Geometricamente, ele mede <b>o quanto dois vetores apontam para a mesma direção</b> (a sombra/projeção de um sobre o outro).",
                                "formula": "$$\\vec{u} \\cdot \\vec{v} = \\sum_{i=1}^{n} u_i v_i = u_1 v_1 + u_2 v_2 + \\dots + u_n v_n$$\ninterpretação do resultado:\n• <b>Positivo ($> 0$):</b> Apontam para direções parecidas.\n• <b>Zero ($= 0$):</b> São perpendiculares (90°, ortogonais / sem relação).\n• <b>Negativo ($< 0$):</b> Apontam em sentidos opostos.",
                                "exemplo": "Dados $\\vec{u} = [2, 3, 1]$ e $\\vec{v} = [4, 0, -2]$:\n$$\\vec{u} \\cdot \\vec{v} = (2 \\times 4) + (3 \\times 0) + (1 \\times -2) = 8 + 0 - 2 = 6$$\nEm uma rede neural, a saída de um neurônio antes da ativação é exatamente o produto escalar entre o vetor de entradas $\\vec{x}$ e o vetor de pesos $\\vec{w}$!",
                                "codigo": "import numpy as np\n\nu = np.array([2, 3, 1])\nv = np.array([4, 0, -2])\n\n# Três formas equivalentes em Python:\ndot1 = np.dot(u, v)\ndot2 = u @ v\nprint('Produto Escalar:', dot2) # 6"
                            }
                        },
                        {
                            "title": "Norma de vetores (L1, L2 Euclidiana) e distâncias",
                            "video_url": "https://www.youtube.com/watch?v=LyGKycYT2v0",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=norma+de+um+vetor+modulo+distancia+euclidiana+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Norma_(matem%C3%A1tica)",
                            "doc_label": "📘 Apostila PT-BR: Normas L1 e L2",
                            "pt_guide": {
                                "intuicao": "A <b>Norma</b> de um vetor mede o seu <b>tamanho (comprimento)</b> desde a origem $[0,0]$ até a ponta da seta. Em Machine Learning usamos principalmente duas normas para medir erros e regularizar pesos (evitar overfitting):\n• <b>Norma L1 (Manhattan / Lasso):</b> Soma dos valores absolutos (como andar em quarteirões).\n• <b>Norma L2 (Euclidiana / Ridge):</b> Teorema de Pitágoras (linha reta direta).",
                                "formula": "$$\\|\\vec{v}\\|_1 = |v_1| + |v_2| + \\dots + |v_n|$$\n$$\\|\\vec{v}\\|_2 = \\sqrt{v_1^2 + v_2^2 + \\dots + v_n^2}$$",
                                "exemplo": "Para o vetor $\\vec{v} = [3, -4]$:\n• <b>Norma L1:</b> $|3| + |-4| = 3 + 4 = 7$\n• <b>Norma L2 (Euclidiana):</b> $\\sqrt{3^2 + (-4)^2} = \\sqrt{9 + 16} = \\sqrt{25} = 5$",
                                "codigo": "import numpy as np\n\nv = np.array([3, -4])\n\nnorma_l1 = np.linalg.norm(v, ord=1)\nnorma_l2 = np.linalg.norm(v, ord=2)\nprint(f'Norma L1: {norma_l1} | Norma L2 (Euclidiana): {norma_l2}')"
                            }
                        },
                        {
                            "title": "Ângulo entre vetores e Similaridade de Cosseno",
                            "video_url": "https://www.youtube.com/watch?v=e9U0QAFbfLI",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=angulo+entre+dois+vetores+similaridade+de+cosseno+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Similaridade_por_cosseno",
                            "doc_label": "📘 Apostila PT-BR: Cosseno",
                            "pt_guide": {
                                "intuicao": "Como sistemas de busca semântica, RAG e ChatGPT sabem que a frase <i>'cachorro feliz'</i> é parecida com <i>'cão alegre'</i>? Usando a <b>Similaridade de Cosseno</b>! Em vez de olhar para o tamanho dos vetores, ela mede apenas o <b>cosseno do ângulo $\\theta$</b> entre eles. Se apontam para a mesma direção ($\\theta = 0^\\circ$), a similaridade é $1.0$ (100% idênticos em significado)!",
                                "formula": "$$\\text{similaridade}(\\vec{u}, \\vec{v}) = \\cos(\\theta) = \\frac{\\vec{u} \\cdot \\vec{v}}{\\|\\vec{u}\\|_2 \\cdot \\|\\vec{v}\\|_2}$$\nO valor sempre fica entre $-1$ (opostos), $0$ (sem relação) e $+1$ (mesma direção).",
                                "exemplo": "Sejam $\\vec{u} = [1, 2]$ e $\\vec{v} = [2, 4]$ (mesma direção, tamanhos diferentes):\n• Produto escalar: $1(2) + 2(4) = 10$\n• Normas: $\\|\\vec{u}\\| = \\sqrt{5}$ e $\\|\\vec{v}\\| = \\sqrt{20} = 2\\sqrt{5}$\n• Cosseno: $\\frac{10}{\\sqrt{5} \\cdot 2\\sqrt{5}} = \\frac{10}{10} = 1.0$ (Similaridade máxima!).",
                                "codigo": "import numpy as np\n\nu = np.array([1, 2])\nv = np.array([2, 4])\n\ncos_sim = (u @ v) / (np.linalg.norm(u) * np.linalg.norm(v))\nprint(f'Similaridade de Cosseno: {cos_sim:.4f}') # 1.0000"
                            }
                        }
                    ]
                ],
                [
                    "Matrizes e Tensores",
                    [
                        {
                            "title": "Matrizes como transformações lineares no espaço",
                            "video_url": "https://www.youtube.com/watch?v=kYB8IZa5AuE",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=transformacoes+lineares+matrizes+algebra+linear+portugues",
                            "doc_url": "https://www.ufrgs.br/reamat/AlgebraLinear/livro/s9-transformacoes_lineares.html",
                            "doc_label": "📘 Apostila PT-BR: Transformações",
                            "pt_guide": {
                                "intuicao": "Uma <b>Matriz</b> não é apenas uma tabela morta de números: ela é uma <b>máquina que move, gira, estica ou achata o espaço</b>! Quando você multiplica uma matriz $A$ por um vetor $\\vec{x}$, a matriz transforma esse vetor em um novo vetor. Cada camada de uma Rede Neural (*Linear Layer*) é literalmente uma matriz que deforma os dados para separar classes!",
                                "formula": "$$\\vec{y} = A \\vec{x} = \\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\end{bmatrix} = \\begin{bmatrix} ax + by \\\\ cx + dy \\end{bmatrix}$$\nDica visual: A 1ª coluna da matriz diz onde o eixo X ($[1,0]$) vai parar; a 2ª coluna diz onde o eixo Y ($[0,1]$) vai parar!",
                                "exemplo": "A matriz $A = \\begin{bmatrix} 2 & 0 \\\\ 0 & 3 \\end{bmatrix}$ duplica a largura (X) e triplica a altura (Y) de qualquer vetor.\nSe aplicarmos no vetor $\\vec{x} = [4, 5]$:\n$$A\\vec{x} = [2 \\times 4, 3 \\times 5] = [8, 15]$$",
                                "codigo": "import numpy as np\n\n# Matriz que gira qualquer vetor 2D em 90 graus para a esquerda\nR_90 = np.array([[0, -1],\n                 [1,  0]])\nv = np.array([3, 0]) # Aponta para a direita\nprint('Vetor após rotação de 90°:', R_90 @ v) # [0, 3] (Aponta para cima!)"
                            }
                        },
                        {
                            "title": "Multiplicação de matrizes (Dot product vs. Hadamard elemento a elemento)",
                            "video_url": "https://www.youtube.com/watch?v=XkY2DOUCWMU",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=multiplicacao+de+matrizes+aula+portugues+ferretto+grings",
                            "doc_url": "https://pt.khanacademy.org/math/precalculus/x9e81a4f98389efdf:matrices/x9e81a4f98389efdf:multiplying-matrices-by-matrices/a/multiplying-matrices",
                            "doc_label": "📘 Apostila PT-BR: Mult. Matrizes",
                            "pt_guide": {
                                "intuicao": "Existem duas multiplicações muito diferentes em IA e confundi-las é o erro nº 1 em PyTorch/NumPy:\n1. <b>Multiplicação Matricial (`A @ B`):</b> Linha da primeira $\\times$ Coluna da segunda. Só funciona se o nº de colunas de $A$ for igual ao nº de linhas de $B$ ($m \\times k$ com $k \\times n \\rightarrow m \\times n$).\n2. <b>Produto de Hadamard (`A * B`):</b> Multiplica posição por posição (exige matrizes de mesmo tamanho).",
                                "formula": "$$\\text{Matricial: } (AB)_{ij} = \\sum_{k} A_{ik} B_{kj} \\quad | \\quad \\text{Hadamard: } (A \\odot B)_{ij} = A_{ij} \\cdot B_{ij}$$",
                                "exemplo": "Sejam $A = \\begin{bmatrix} 1 & 2 \\\\ 3 & 4 \\end{bmatrix}$ e $B = \\begin{bmatrix} 2 & 0 \\\\ 1 & 3 \\end{bmatrix}$:\n• <b>Hadamard (`A * B`):</b> $\\begin{bmatrix} 1\\times 2 & 2\\times 0 \\\\ 3\\times 1 & 4\\times 3 \\end{bmatrix} = \\begin{bmatrix} 2 & 0 \\\\ 3 & 12 \\end{bmatrix}$\n• <b>Matricial (`A @ B`):</b> 1ª linha com 1ª coluna $= 1(2)+2(1)=4$; 1ª linha com 2ª coluna $= 1(0)+2(3)=6 \\rightarrow \\begin{bmatrix} 4 & 6 \\\\ 10 & 12 \\end{bmatrix}$.",
                                "codigo": "import numpy as np\n\nA = np.array([[1, 2], [3, 4]])\nB = np.array([[2, 0], [1, 3]])\n\nprint('Matricial (A @ B):\\n', A @ B)\nprint('Elemento a elemento / Hadamard (A * B):\\n', A * B)"
                            }
                        },
                        {
                            "title": "Sistemas de equações lineares e determinantes",
                            "video_url": "https://www.youtube.com/watch?v=Ip3X9LOh2dk",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=determinantes+e+sistemas+lineares+portugues+grings",
                            "doc_url": "https://www.ufrgs.br/reamat/AlgebraLinear/livro/s1-sistemas_lineares.html",
                            "doc_label": "📘 Apostila PT-BR: Determinantes",
                            "pt_guide": {
                                "intuicao": "Um sistema de várias equações pode ser escrito de forma compacta como $A\\vec{x} = \\vec{b}$. O <b>Determinante ($\\det(A)$)</b> mede <b>como a matriz altera a área ou volume</b> do espaço! Se $\\det(A) = 0$, significa que a matriz esmagou o espaço (por exemplo, achatou um quadrado 2D em uma linha 1D), perdendo informação de forma irreversível!",
                                "formula": "$$\\det\\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix} = a\\cdot d - b\\cdot c$$\n• Se $\\det(A) \\neq 0$: O sistema tem solução única e a matriz pode ser invertida.\n• Se $\\det(A) = 0$: Matriz singular (colunas redundantes / sem inversa).",
                                "exemplo": "Para $A = \\begin{bmatrix} 3 & 2 \\\\ 1 & 4 \\end{bmatrix}$:\n$$\\det(A) = (3 \\times 4) - (2 \\times 1) = 12 - 2 = 10$$\nA matriz multiplica a área de qualquer figura por $10$!",
                                "codigo": "import numpy as np\n\nA = np.array([[3, 2], [1, 4]])\nb = np.array([16, 13])\n\nprint('Determinante:', round(np.linalg.det(A), 2)) # 10.0\n# Resolvendo o sistema A * x = b:\nx = np.linalg.solve(A, b)\nprint('Solução x:', x) # [3.8, 2.3]"
                            }
                        },
                        {
                            "title": "Inversa de matriz e pseudoinversa de Moore-Penrose",
                            "video_url": "https://www.youtube.com/watch?v=uQhTuRlWM3E",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=matriz+inversa+algebra+linear+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Matriz_inversa",
                            "doc_label": "📘 Apostila PT-BR: Matriz Inversa",
                            "pt_guide": {
                                "intuicao": "A <b>Matriz Inversa ($A^{-1}$)</b> é o 'Ctrl+Z' (desfazer) de uma transformação linear: se a matriz $A$ gira o espaço em $+30^\\circ$, a matriz $A^{-1}$ gira em $-30^\\circ$, voltando tudo ao original ($A \\cdot A^{-1} = I$, onde $I$ é a matriz identidade). E quando a matriz não é quadrada (ex.: 1.000 linhas de clientes e 5 colunas na Regressão Linear)? Usamos a <b>Pseudoinversa de Moore-Penrose ($A^+$)</b>, que encontra a melhor solução aproximada!",
                                "formula": "$$A \\cdot A^{-1} = I = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix} \\quad | \\quad \\text{Pseudoinversa: } A^+ = (A^T A)^{-1} A^T$$",
                                "exemplo": "Se $A\\vec{x} = \\vec{b}$ e $A$ tem inversa, isolamos $\\vec{x}$ multiplicando pela inversa: $\\vec{x} = A^{-1}\\vec{b}$.\nEm Machine Learning, os pesos ótimos de uma Regressão Linear são calculados diretamente com a pseudoinversa: $\\vec{w} = X^+ \\vec{y}$!",
                                "codigo": "import numpy as np\n\nA = np.array([[4, 7], [2, 6]])\nA_inv = np.linalg.inv(A)\nprint('A @ A_inv (Identidade):\\n', np.round(A @ A_inv))\n\n# Pseudoinversa para matriz retangular (3x2):\nX = np.array([[1, 2], [3, 4], [5, 6]])\nX_pinv = np.linalg.pinv(X)\nprint('Shape da Pseudoinversa:', X_pinv.shape) # (2, 3)"
                            }
                        },
                        {
                            "title": "Autovalores e Autovetores (Eigenvalues & Eigenvectors)",
                            "video_url": "https://www.youtube.com/watch?v=PFDu9oVAE-g",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=autovalores+e+autovetores+algebra+linear+portugues",
                            "doc_url": "https://www.ufrgs.br/reamat/AlgebraLinear/livro/s11-autovalores_e_autovetores.html",
                            "doc_label": "📘 Apostila PT-BR: Autovetores",
                            "pt_guide": {
                                "intuicao": "Quando uma matriz transforma o espaço, quase todos os vetores mudam de direção. Mas existem alguns vetores especiais que <b>não mudam de direção</b> — eles apenas são esticados ou encolhidos! Esses vetores especiais são os <b>Autovetores (Eigenvectors)</b>, e o fator pelo qual eles são esticados é o <b>Autovalor (Eigenvalue $\\lambda$)</b>. Eles revelam os 'eixos principais' dos dados!",
                                "formula": "$$A \\vec{v} = \\lambda \\vec{v}$$\nOnde $A$ é a matriz, $\\vec{v}$ é o autovetor (direção preservada) e $\\lambda$ (lambda) é o autovalor (fator de escala).",
                                "exemplo": "Na matriz $A = \\begin{bmatrix} 3 & 0 \\\\ 0 & 1 \\end{bmatrix}$, o vetor $\\vec{v}_1 = [1, 0]$ vira $[3, 0] = 3 \\cdot \\vec{v}_1$.\nLogo, $[1, 0]$ é um autovetor com autovalor $\\lambda = 3$ (a direção principal onde os dados mais crescem!).",
                                "codigo": "import numpy as np\n\nA = np.array([[4, 2],\n              [1, 3]])\n\nautovalores, autovetores = np.linalg.eig(A)\nprint('Autovalores (lambdas):', autovalores) # [5., 2.]"
                            }
                        },
                        {
                            "title": "Decomposição em Valores Singulares (SVD) e PCA",
                            "video_url": "https://www.youtube.com/watch?v=FgakZw6K1QQ",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=pca+analise+de+componentes+principais+svd+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/An%C3%A1lise_de_componentes_principais",
                            "doc_label": "📘 Apostila PT-BR: SVD & PCA",
                            "pt_guide": {
                                "intuicao": "Imagine uma tabela com 100 colunas correlacionadas. Como resumir essas 100 colunas em apenas 2 ou 3 colunas sem perder a informação essencial? Usando <b>PCA (Análise de Componentes Principais)</b> e <b>SVD (Decomposição em Valores Singulares)</b>! Eles encontram as direções de maior variância (maior espalhamento da informação) e descartam o ruído. O <b>LoRA</b> (usado para fazer fine-tuning de LLMs) usa exatamente decomposição de matrizes de baixo posto inspirada no SVD!",
                                "formula": "$$A = U \\Sigma V^T$$\nQualquer matriz $A$ pode ser fatorada em uma rotação ($V^T$), um esticamento nos eixos principais ($\\Sigma$, matriz diagonal de valores singulares) e outra rotação ($U$).",
                                "exemplo": "Se você tem fotos 1000x1000 pixels, o SVD permite manter apenas os 50 maiores valores singulares de $\\Sigma$, comprimindo a imagem em 90% mantendo quase toda a nitidez!",
                                "codigo": "import numpy as np\n\n# Criando dados 2D correlacionados\nX = np.array([[1, 2], [2, 4.1], [3, 5.9], [4, 8.2]])\nX_centrado = X - X.mean(axis=0)\n\n# Decomposição SVD\nU, S, Vt = np.linalg.svd(X_centrado)\nprint('Valores Singulares (importância de cada eixo):', np.round(S, 2))"
                            }
                        }
                    ]
                ]
            ]
        },
        {
            "t": "Módulo 2 · Cálculo Diferencial, Gradientes & Otimização",
            "d": "3 a 4 semanas",
            "tip": "💡 <b>Dica de Ouro:</b> Você não precisa resolver integrais cabeludas de faculdade para criar IA! Tudo o que você precisa do Cálculo é entender que a <b>Derivada é uma bússola</b> que aponta para onde o erro da rede neural diminui.",
            "p": "Construir do zero em Python uma descida de gradiente que aprende sozinha os parâmetros de uma reta para prever preços.",
            "r": "Apostila Interativa Integrada em Português · Livro Aberto Cálculo UFRGS (REAMAT) · Canal Prof. Ferretto & Prof. Grings",
            "g": [
                [
                    "Cálculo Diferencial",
                    [
                        {
                            "title": "Limites e taxa de variação instantânea (ideia geral)",
                            "video_url": "https://www.youtube.com/watch?v=WUvTyaaNkzM",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=limites+e+derivadas+introducao+calculo+portugues+ferretto+grings",
                            "doc_url": "https://pt.khanacademy.org/math/differential-calculus/dc-diff-intro",
                            "doc_label": "📘 Apostila PT-BR: Limites & Taxa",
                            "pt_guide": {
                                "intuicao": "O <b>Limite</b> responde à pergunta: <i>'Para qual valor uma função está se aproximando quando chegamos infinitamente perto de um ponto?'</i>. A partir disso nasce a <b>Taxa de Variação Instantânea (Derivada)</b>: é como o velocímetro do carro num instante exato. Em IA, ela responde: <i>'Se eu mexer um milímetro neste peso $w$ da rede neural, o erro sobe ou desce?'</i>",
                                "formula": "$$f'(x) = \\lim_{h \\to 0} \\frac{f(x + h) - f(x)}{h}$$\nO numerador $f(x+h) - f(x)$ é a mudança na saída; o denominador $h$ é o pequeno passo dado na entrada.",
                                "exemplo": "Seja $f(x) = x^2$. No ponto $x = 3$, temos $f(3) = 9$.\nSe dermos um micro-passo $h = 0.001$ para $x = 3.001$, temos $f(3.001) = 9.006001$.\nDividindo a variação pelo passo: $\\frac{9.006001 - 9}{0.001} \\approx 6$. Ou seja, a taxa de variação em $x=3$ é $6$!",
                                "codigo": "# Calculando a derivada numérica com um micro-passo h\ndef f(x):\n    return x ** 2\n\nx = 3.0\nh = 0.0001\nderivada_aprox = (f(x + h) - f(x)) / h\nprint(f'Taxa de variação em x=3: {derivada_aprox:.4f}') # ~6.0001"
                            }
                        },
                        {
                            "title": "Derivadas fundamentais e regras básicas (potência, produto, soma)",
                            "video_url": "https://www.youtube.com/watch?v=S0_qX4VFYMQ",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=regras+de+derivacao+calculo+1+aula+portugues+grings",
                            "doc_url": "https://www.ufrgs.br/reamat/Calculo/livro-cfuv/derivada-regras_de_derivacao.html",
                            "doc_label": "📘 Apostila PT-BR: Regras Derivação",
                            "pt_guide": {
                                "intuicao": "Em vez de calcular limites toda vez, usamos atalhos diretos chamados <b>Regras de Derivação</b>:\n• <b>Constante:</b> A derivada de um número fixo é $0$ (não varia).\n• <b>Regra do Tombo (Potência):</b> O expoente $n$ 'cai' multiplicando na frente e perde $1$ no topo ($x^n \\rightarrow n \\cdot x^{n-1}$).\n• <b>Soma:</b> A derivada da soma é a soma das derivadas.",
                                "formula": "$$\\frac{d}{dx}(x^n) = n \\cdot x^{n-1} \\quad | \\quad \\frac{d}{dx}(e^x) = e^x \\quad | \\quad \\frac{d}{dx}(\\ln x) = \\frac{1}{x}$$",
                                "exemplo": "Qual a derivada da função de perda quadrática $L(w) = 3w^2 - 12w + 5$?\n• Derivada de $3w^2$: o $2$ tomba multiplicando o $3 \\rightarrow 6w$\n• Derivada de $-12w$: fica $-12$\n• Derivada de $+5$: é $0$\nResultado: $L'(w) = 6w - 12$. (Para achar o ponto onde o erro é mínimo, igualamos a zero: $6w - 12 = 0 \\Rightarrow w = 2$!).",
                                "codigo": "# Verificando a derivada de L(w) = 3w^2 - 12w + 5\ndef L_derivada(w):\n    return 6 * w - 12\n\nprint('Inclinação em w=0:', L_derivada(0)) # -12 (erro descendo)\nprint('Inclinação em w=2:', L_derivada(2)) # 0 (fundo do vale / erro mínimo!)"
                            }
                        },
                        {
                            "title": "Regra da Cadeia (Chain Rule) - o motor do Backpropagation",
                            "video_url": "https://www.youtube.com/watch?v=YG15m2VwSjA",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=regra+da+cadeia+derivada+portugues+grings+ferretto",
                            "doc_url": "https://pt.khanacademy.org/math/ap-calculus-ab/ab-differentiation-2-new/ab-3-1a/a/chain-rule-review",
                            "doc_label": "📘 Apostila PT-BR: Regra da Cadeia",
                            "pt_guide": {
                                "intuicao": "Uma Rede Neural Profunda nada mais é do que uma <b>função dentro de outra função, dentro de outra função</b> (camada 1 $\\rightarrow$ camada 2 $\\rightarrow$ camada 3 $\\rightarrow$ erro). Como descobrir a culpa de um peso lá da 1ª camada pelo erro final lá na última camada? Usando a <b>Regra da Cadeia</b>! Ela diz que basta <b>multiplicar as derivadas locais de trás para frente</b>. Isso é 100% o algoritmo de <b>Backpropagation</b>!",
                                "formula": "$$\\frac{dL}{dw} = \\frac{dL}{dy} \\cdot \\frac{dy}{dz} \\cdot \\frac{dz}{dw}$$\n<i>Derivada da função de fora $\\times$ Derivada da função de dentro!</i>",
                                "exemplo": "Se $z = 3w$ e $L = z^2$:\n• $\\frac{dL}{dz} = 2z$\n• $\\frac{dz}{dw} = 3$\nPela Regra da Cadeia: $\\frac{dL}{dw} = 2z \\cdot 3 = 6z = 18w$.",
                                "codigo": "# Simulando um mini Backpropagation com Regra da Cadeia\nw = 2.0\nz = 3 * w      # Camada 1 (z = 6)\nL = z ** 2     # Loss final (L = 36)\n\n# Backpropagation (de trás para frente):\ndL_dz = 2 * z  # 12\ndz_dw = 3.0    # 3\ndL_dw = dL_dz * dz_dw\nprint('Gradiente dL/dw via Regra da Cadeia:', dL_dw) # 36.0"
                            }
                        },
                        {
                            "title": "Derivadas de funções de ativação (Sigmoide, Tanh, ReLU, GeLU)",
                            "video_url": "https://www.youtube.com/watch?v=aircAruvnKk",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=funcoes+de+ativacao+redes+neurais+relu+sigmoid+portugues",
                            "doc_url": "https://www.deeplearningbook.com.br/funcao-de-ativacao/",
                            "doc_label": "📘 Apostila PT-BR: Ativações",
                            "pt_guide": {
                                "intuicao": "Sem <b>Funções de Ativação</b>, uma rede neural de 100 camadas seria matematicamente igual a uma única camada linear! As ativações dobram o espaço para aprender padrões complexos:\n• <b>Sigmoide:</b> Espreme números entre $0$ e $1$ (usada em probabilidades binárias).\n• <b>ReLU:</b> Se for negativo vira $0$; se for positivo passa direto! Sua derivada é simplesmente $0$ ou $1$, evitando o sumiço do gradiente (*vanishing gradient*).",
                                "formula": "$$\\text{ReLU}(x) = \\max(0, x) \\implies \\text{ReLU}'(x) = \\begin{cases} 1 & \\text{se } x > 0 \\\\ 0 & \\text{se } x < 0 \\end{cases}$$\n$$\\sigma(x) = \\frac{1}{1 + e^{-x}} \\implies \\sigma'(x) = \\sigma(x) \\cdot (1 - \\sigma(x))$$",
                                "exemplo": "Se $x = 0$, a Sigmoide vale $\\sigma(0) = 0.5$. Sua derivada máxima ocorre aí: $\\sigma'(0) = 0.5 \\times (1 - 0.5) = 0.25$. Já para valores muito grandes ($x=10$), $\\sigma'(10) \\approx 0$ (o neurônio satura e para de aprender!). Por isso a <b>ReLU</b> e a <b>GeLU</b> dominam os LLMs modernos.",
                                "codigo": "import numpy as np\n\ndef sigmoid(x):\n    return 1 / (1 + np.exp(-x))\n\ndef sigmoid_derivada(x):\n    s = sigmoid(x)\n    return s * (1 - s)\n\ndef relu_derivada(x):\n    return np.where(x > 0, 1.0, 0.0)\n\nprint('Derivada ReLU em [-2, 5]:', relu_derivada(np.array([-2, 5]))) # [0., 1.]"
                            }
                        }
                    ]
                ],
                [
                    "Gradientes e Otimizadores",
                    [
                        {
                            "title": "Derivadas parciais e o vetor Gradiente (nabla f)",
                            "video_url": "https://www.youtube.com/watch?v=IHZwWFHWa-w",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=derivadas+parciais+e+vetor+gradiente+portugues",
                            "doc_url": "https://pt.khanacademy.org/math/multivariable-calculus/multivariable-derivatives/partial-derivative-and-gradient-articles/a/the-gradient",
                            "doc_label": "📘 Apostila PT-BR: Vetor Gradiente",
                            "pt_guide": {
                                "intuicao": "Quando uma função depende de várias variáveis ao mesmo tempo (ex.: erro $L(w_1, w_2)$), calculamos a <b>Derivada Parcial ($\\partial$)</b> derivando uma variável de cada vez e fingindo que as outras são números fixos. Juntando todas as derivadas parciais dentro de um vetor, formamos o <b>Vetor Gradiente ($\\nabla L$)</b>, que aponta na direção de <b>maior subida</b> da montanha de erro!",
                                "formula": "$$\\nabla f(w_1, w_2) = \\begin{bmatrix} \\frac{\\partial f}{\\partial w_1} \\\\ \\frac{\\partial f}{\\partial w_2} \\end{bmatrix}$$",
                                "exemplo": "Seja $f(w_1, w_2) = w_1^2 + 3w_2^2$.\n• Derivada parcial em relação a $w_1$: $\\frac{\\partial f}{\\partial w_1} = 2w_1$\n• Derivada parcial em relação a $w_2$: $\\frac{\\partial f}{\\partial w_2} = 6w_2$\nNo ponto $(1, 2)$, o vetor gradiente é $\\nabla f = [2, 12]$. Para descer a montanha (reduzir o erro), andamos no sentido oposto: $[-2, -12]$!",
                                "codigo": "import numpy as np\n\n# Calculando o vetor gradiente de f(w1, w2) = w1^2 + 3*w2^2\ndef gradiente(w):\n    w1, w2 = w[0], w[1]\n    return np.array([2 * w1, 6 * w2])\n\nponto = np.array([1.0, 2.0])\nprint('Vetor Gradiente no ponto (1,2):', gradiente(ponto)) # [ 2. 12.]"
                            }
                        },
                        {
                            "title": "Matriz Jacobiana e Matriz Hessiana (curvatura da loss)",
                            "video_url": "https://www.youtube.com/watch?v=Ilg3gGewQ5U",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=matriz+jacobiana+e+hessiana+calculo+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Matriz_hessiana",
                            "doc_label": "📘 Apostila PT-BR: Jacobiana & Hessiana",
                            "pt_guide": {
                                "intuicao": "• <b>Matriz Jacobiana ($J$):</b> Guarda todas as derivadas de <b>1ª ordem</b> quando uma camada tem múltiplas entradas e múltiplas saídas.\n• <b>Matriz Hessiana ($H$):</b> Guarda as derivadas de <b>2ª ordem</b> (a derivada da derivada). Ela mede a <b>curvatura</b> do terreno de erro: diz se estamos num vale fundo (mínimo local), num topo de morro (máximo) ou num ponto de sela!",
                                "formula": "$$J_{ij} = \\frac{\\partial f_i}{\\partial x_j} \\quad | \\quad H_{ij} = \\frac{\\partial^2 L}{\\partial w_i \\partial w_j}$$",
                                "exemplo": "Se a derivada primeira diz a inclinação da pista, a 2ª derivada (Hessiana) diz se a pista está curvando para cima (como uma tigela $\\cup$, ótimo para convergir!) ou para baixo ($\\cap$).",
                                "codigo": "import numpy as np\n\n# Para f(x, y) = x^2 + 3*y^2, a Hessiana é constante:\nH = np.array([[2.0, 0.0],\n              [0.0, 6.0]])\nprint('Autovalores da Hessiana (>0 indica vale convexo):', np.linalg.eigvals(H))"
                            }
                        },
                        {
                            "title": "Algoritmo de Descida do Gradiente (Vanilla Gradient Descent)",
                            "video_url": "https://www.youtube.com/watch?v=tIeHLnjs5U8",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=gradiente+descendente+machine+learning+portugues",
                            "doc_url": "https://www.deeplearningbook.com.br/algoritmo-gradient-descent/",
                            "doc_label": "📘 Apostila PT-BR: Gradiente Descendente",
                            "pt_guide": {
                                "intuicao": "Imagine estar no topo de uma montanha no meio de uma neblina densa e querer chegar ao fundo do vale. Você sente a inclinação do chão sob seus pés (o Gradiente $\\nabla L$) e dá um passo na direção que desce ($-\\nabla L$). Repita isso milhares de vezes e sua rede neural aprenderá os pesos perfeitos! Esse é o <b>Gradiente Descendente</b>.",
                                "formula": "$$w_{\\text{novo}} = w_{\\text{atual}} - \\alpha \\cdot \\nabla L(w_{\\text{atual}})$$\n• $w$: Peso do modelo\n• $\\alpha$ (alpha): Taxa de aprendizado (*Learning Rate* — tamanho do passo)\n• $\\nabla L$: Gradiente do erro",
                                "exemplo": "Queremos minimizar $L(w) = (w - 5)^2$, cujo mínimo é $w = 5$.\nComeçando em $w = 1$ com taxa $\\alpha = 0.2$:\n• Derivada: $L'(1) = 2(1 - 5) = -8$\n• Atualização: $w_{\\text{novo}} = 1 - 0.2 \\times (-8) = 1 + 1.6 = 2.6$ (Já chegou mais perto do $5$!).",
                                "codigo": "w = 1.0\nlr = 0.2 # Taxa de aprendizado (learning rate)\n\nfor passo in range(10):\n    grad = 2 * (w - 5) # Derivada de (w - 5)^2\n    w = w - lr * grad\nprint(f'Peso aprendido após 10 passos: {w:.4f} (Alvo ideal: 5.0)')"
                            }
                        },
                        {
                            "title": "Otimizadores modernos: Momentum, RMSprop e Adam",
                            "video_url": "https://www.youtube.com/watch?v=vMh0zPT0tLI",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=otimizadores+adam+rmsprop+momentum+redes+neurais+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Descida_de_gradiente_estoc%C3%A1stico#Adam",
                            "doc_label": "📘 Apostila PT-BR: Otimizador Adam",
                            "pt_guide": {
                                "intuicao": "O Gradiente Descendente puro é lento e pode ficar ziguezagueando em barrancos. Por isso criaram otimizadores inteligentes:\n• <b>Momentum:</b> Simula uma bola pesada ganhando embalo (inércia) ladeira abaixo.\n• <b>RMSprop:</b> Adapta o tamanho do passo para cada peso individualmente.\n• <b>Adam (Adaptive Moment Estimation):</b> Junta o embalo do Momentum + o passo adaptativo do RMSprop! É o otimizador padrão de 99% dos modelos modernos.",
                                "formula": "$$m_t = \\beta_1 m_{t-1} + (1 - \\beta_1) g_t \\quad (\\text{Média / Momentum})$$\n$$v_t = \\beta_2 v_{t-1} + (1 - \\beta_2) g_t^2 \\quad (\\text{Velocidade adaptativa})$$\n$$w_{t+1} = w_t - \\alpha \\frac{\\hat{m}_t}{\\sqrt{\\hat{v}_t} + \\epsilon}$$",
                                "exemplo": "Se um peso recebe gradientes gigantescos toda hora, o Adam diminui o passo dele para não explodir; se outro peso recebe gradientes tímidos, o Adam aumenta o passo dele para acelerar o aprendizado!",
                                "codigo": "# Exemplo conceitual de Momentum em Python\nw, v_inercia = 1.0, 0.0\nlr, beta = 0.1, 0.9\nfor _ in range(15):\n    grad = 2 * (w - 5)\n    v_inercia = beta * v_inercia + (1 - beta) * grad\n    w = w - lr * v_inercia\nprint(f'Peso otimizado com Momentum: {w:.4f}')"
                            }
                        },
                        {
                            "title": "Taxa de aprendizado (Learning Rate), convergência e pontos de sela",
                            "video_url": "https://www.youtube.com/watch?v=sDv4f4s2SB8",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=learning+rate+taxa+de+aprendizado+machine+learning+portugues",
                            "doc_url": "https://www.deeplearningbook.com.br/algoritmo-gradient-descent/",
                            "doc_label": "📘 Apostila PT-BR: Learning Rate",
                            "pt_guide": {
                                "intuicao": "A <b>Taxa de Aprendizado ($\\alpha$ ou Learning Rate)</b> é o hiperparâmetro mais crítico do treinamento:\n• <b>Muito pequena (ex.: $10^{-7}$):</b> O treinamento demora uma eternidade e pode parar em buracos rasos.\n• <b>Muito grande (ex.: $10.0$):</b> O passo é tão largo que pula de um lado para o outro do vale e o erro explode (`NaN`)!\n• <b>Ponto de Sela:</b> Um platô onde uma direção desce e outra sobe (como uma sela de cavalo), onde o gradiente zera sem ser o fundo do vale.",
                                "formula": "$$\\text{Cosine Annealing / Warmup: } \\alpha_t = \\alpha_{\\min} + \\frac{1}{2}(\\alpha_{\\max} - \\alpha_{\\min})\\left(1 + \\cos\\left(\\frac{t}{T}\\pi\\right)\\right)$$",
                                "exemplo": "No treinamento de LLMs (como GPT e Llama), usamos um <b>Learning Rate Scheduler</b>: começamos aquecendo devagar (*Warmup*) até $3\\times 10^{-4}$ e depois vamos reduzindo suavemente para refinar os pesos finais.",
                                "codigo": "# Comparando Learning Rate ideal vs Learning Rate alto demais\nfor lr in [0.1, 1.05]:\n    w = 0.0\n    for _ in range(5):\n        w = w - lr * (2 * (w - 3))\n    print(f'LR={lr} -> w final = {w:.2f} (Alvo: 3.00)')"
                            }
                        }
                    ]
                ]
            ]
        },
        {
            "t": "Módulo 3 · Probabilidade & Estatística para IA",
            "d": "3 a 4 semanas",
            "tip": "💡 <b>Dica de Ouro:</b> A Inteligência Artificial não trabalha com certezas absolutas, mas com <b>probabilidades</b>. Quando um LLM escreve uma frase, ele está sorteando a próxima palavra a partir de uma distribuição de probabilidade condicional!",
            "p": "Construir um classificador Naive Bayes em Python para detectar mensagens de spam usando o Teorema de Bayes.",
            "r": "Apostila Interativa Integrada em Português · Livro Aberto Probabilidade e Estatística UFRGS (REAMAT) · Khan Academy Estatística PT-BR",
            "g": [
                [
                    "Estatística Descritiva & Probabilidade",
                    [
                        {
                            "title": "Variáveis aleatórias discretas e contínuas",
                            "video_url": "https://www.youtube.com/watch?v=HZGCoVF3YvM",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=variaveis+aleatorias+discretas+e+continuas+portugues",
                            "doc_url": "https://pt.khanacademy.org/math/statistics-probability/random-variables-stats-library",
                            "doc_label": "📘 Apostila PT-BR: Var. Aleatórias",
                            "pt_guide": {
                                "intuicao": "Uma <b>Variável Aleatória ($X$)</b> traduz eventos incertos do mundo real em números:\n• <b>Discreta:</b> Assume valores contáveis/inteiros (ex.: número de cliques num anúncio, qual palavra do vocabulário o LLM vai escolher). Usa Função Massa de Probabilidade ($P(X=x)$).\n• <b>Contínua:</b> Assume qualquer valor com casas decimais num intervalo (ex.: temperatura amanhã, preço de uma ação). Usa Função Densidade de Probabilidade ($f(x)$).",
                                "formula": "$$\\text{Discreta: } \\sum_{x} P(X = x) = 1 \\quad | \\quad \\text{Contínua: } \\int_{-\\infty}^{+\\infty} f(x)\\,dx = 1$$",
                                "exemplo": "Em IA: prever <b>Classificação</b> (Gato, Cachorro ou Pássaro) modela uma variável <b>discreta</b>; prever <b>Regressão</b> (valor de venda de uma casa em R$) modela uma variável <b>contínua</b>.",
                                "codigo": "import numpy as np\n\n# Variável discreta: sorteando próximo token com probabilidades [0.7, 0.2, 0.1]\ntokens = ['Inteligência', 'Artificial', 'Futuro']\nprobs = [0.7, 0.2, 0.1]\nescolha = np.random.choice(tokens, p=probs)\nprint('Token amostrado:', escolha)"
                            }
                        },
                        {
                            "title": "Média, mediana, variância e desvio padrão",
                            "video_url": "https://www.youtube.com/watch?v=SzZ6G436HKM",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=media+mediana+variancia+e+desvio+padrao+portugues",
                            "doc_url": "https://pt.khanacademy.org/math/statistics-probability/summarizing-quantitative-data",
                            "doc_label": "📘 Apostila PT-BR: Variância & Desvio",
                            "pt_guide": {
                                "intuicao": "• <b>Média ($\\mu$):</b> O centro de gravidade dos dados (sensível a valores extremos/outliers).\n• <b>Mediana:</b> O valor exatamente no meio quando ordenamos os dados (robusta contra outliers!).\n• <b>Variância ($\\sigma^2$) e Desvio Padrão ($\\sigma$):</b> Medem o quanto os dados estão espalhados longe da média. Toda camada de <b>BatchNorm / LayerNorm</b> em redes neurais usa média e desvio padrão para estabilizar os neurônios!",
                                "formula": "$$\\mu = \\frac{1}{n}\\sum_{i=1}^n x_i \\quad | \\quad \\sigma^2 = \\frac{1}{n}\\sum_{i=1}^n (x_i - \\mu)^2 \\quad | \\quad \\sigma = \\sqrt{\\sigma^2}$$",
                                "exemplo": "Salários em mil reais: `[3, 4, 5, 4, 100]`.\n• A <b>Média</b> é $23.2$ mil (distorcida pelo $100$).\n• A <b>Mediana</b> é $4$ mil (retrata muito melhor o grupo!).",
                                "codigo": "import numpy as np\n\ndados = np.array([10, 12, 15, 18, 20])\nprint('Média:', np.mean(dados))\nprint('Mediana:', np.median(dados))\nprint('Desvio Padrão:', round(np.std(dados), 2))"
                            }
                        },
                        {
                            "title": "Esperança matemática, covariância e correlação",
                            "video_url": "https://www.youtube.com/watch?v=qtaqvPAeEJY",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=covariancia+e+correlacao+estatistica+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Coeficiente_de_correla%C3%A7%C3%A3o_de_Pearson",
                            "doc_label": "📘 Apostila PT-BR: Correlação",
                            "pt_guide": {
                                "intuicao": "• <b>Esperança Matemática ($E[X]$):</b> É a média ponderada pelas probabilidades (o retorno médio esperado no longo prazo).\n• <b>Covariância e Correlação ($r$ de Pearson):</b> Medem se duas variáveis caminham juntas! A correlação sempre vai de $-1$ (quando uma sobe, a outra cai) até $+1$ (sobem juntas), passando por $0$ (sem relação linear).",
                                "formula": "$$E[X] = \\sum x_i P(x_i) \\quad | \\quad r_{xy} = \\frac{\\text{Cov}(X, Y)}{\\sigma_X \\cdot \\sigma_Y} \\in [-1, +1]$$",
                                "exemplo": "Se 'Horas de Estudo' e 'Nota na Prova' têm correlação $r = +0.88$, existe forte relação positiva! Lembrete de ouro em Ciência de Dados: <b>Correlação não implica causalidade</b>.",
                                "codigo": "import numpy as np\n\nhoras_estudo = np.array([1, 2, 4, 6, 8])\nnotas = np.array([40, 52, 70, 85, 96])\n\ncorr = np.corrcoef(horas_estudo, notas)[0, 1]\nprint(f'Correlação de Pearson: {corr:.4f}') # ~0.996"
                            }
                        },
                        {
                            "title": "Probabilidade condicional e Teorema de Bayes",
                            "video_url": "https://www.youtube.com/watch?v=HZGCoVF3YvM",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=teorema+de+bayes+probabilidade+condicional+portugues",
                            "doc_url": "https://pt.khanacademy.org/math/ap-statistics/probability-ap/stats-conditional-probability/a/check-independence-conditional-probability",
                            "doc_label": "📘 Apostila PT-BR: Teorema de Bayes",
                            "pt_guide": {
                                "intuicao": "A <b>Probabilidade Condicional $P(A|B)$</b> é a chance de $A$ acontecer <i>sabendo que $B$ já aconteceu</i>. O <b>Teorema de Bayes</b> é a fórmula matemática para <b>atualizar nossas crenças diante de novas evidências</b>! Você começa com uma estimativa inicial (*Priori*), observa os dados reais (*Verossimilhança*) e calcula a probabilidade atualizada (*Posteriori*).",
                                "formula": "$$P(A \\mid B) = \\frac{P(B \\mid A) \\cdot P(A)}{P(B)}$$\n• $P(A)$: Probabilidade a priori (antes da evidência)\n• $P(B|A)$: Verossimilhança (chance da evidência aparecer se $A$ for verdade)\n• $P(A|B)$: Probabilidade a posteriori (atualizada!)",
                                "exemplo": "Filtro de Spam: $20\\%$ dos e-mails são Spam ($P(S)=0.2$). A palavra 'Prêmio' aparece em $80\\%$ dos Spams ($P(P|S)=0.8$), mas só em $5\\%$ dos e-mails normais.\nSe chegou um e-mail com 'Prêmio', a chance de ser Spam salta de $20\\%$ para:\n$$P(S|P) = \\frac{0.8 \\times 0.2}{(0.8 \\times 0.2) + (0.05 \\times 0.8)} = \\frac{0.16}{0.20} = 80\\%!$$",
                                "codigo": "p_spam = 0.20\np_normal = 0.80\np_premio_dado_spam = 0.80\np_premio_dado_normal = 0.05\n\np_premio_total = (p_premio_dado_spam * p_spam) + (p_premio_dado_normal * p_normal)\np_spam_dado_premio = (p_premio_dado_spam * p_spam) / p_premio_total\nprint(f'Chance de ser Spam dado a palavra Prêmio: {p_spam_dado_premio*100:.1f}%') # 80.0%"
                            }
                        }
                    ]
                ],
                [
                    "Distribuições & Inferência",
                    [
                        {
                            "title": "Distribuição Normal (Gaussiana) e probabilidade vs verossimilhança",
                            "video_url": "https://www.youtube.com/watch?v=rzFX5NWojp0",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=distribuicao+normal+gaussiana+estatistica+portugues",
                            "doc_url": "https://pt.khanacademy.org/math/statistics-probability/modeling-distributions-of-data/normal-distributions-library/a/normal-distributions-review",
                            "doc_label": "📘 Apostila PT-BR: Curva Normal",
                            "pt_guide": {
                                "intuicao": "A <b>Distribuição Normal (Curva em Sino de Gauss)</b> aparece em toda a natureza e na inicialização de pesos de redes neurais! Nela, a maioria dos valores se concentra perto da média $\\mu$, e valores extremos são raros:\n• <b>68%</b> dos dados ficam a até $1$ desvio padrão ($\\mu \\pm 1\\sigma$).\n• <b>95%</b> ficam a até $2$ desvios padrões ($\\mu \\pm 2\\sigma$).",
                                "formula": "$$f(x) = \\frac{1}{\\sigma \\sqrt{2\\pi}} e^{-\\frac{1}{2}\\left(\\frac{x - \\mu}{\\sigma}\\right)^2}$$",
                                "exemplo": "• <b>Probabilidade:</b> Conhecemos a curva ($\\mu, \\sigma$) e perguntamos a chance de sair um dado $x$.\n• <b>Verossimilhança (Likelihood):</b> Já temos os dados observados e perguntamos quais parâmetros ($\\mu, \\sigma$) melhor explicam esses dados!",
                                "codigo": "import numpy as np\n\n# Inicializando pesos de uma camada neural com Distribuição Normal Padrão (média 0, desvio 1)\npesos = np.random.normal(loc=0.0, scale=1.0, size=1000)\nprint(f'Média gerada: {pesos.mean():.2f} | Desvio: {pesos.std():.2f}')"
                            }
                        },
                        {
                            "title": "Teorema do Limite Central e amostragem",
                            "video_url": "https://www.youtube.com/watch?v=JNm3M9IJihQ",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=teorema+do+limite+central+estatistica+portugues",
                            "doc_url": "https://pt.khanacademy.org/math/statistics-probability/sampling-distributions-library/sample-means/v/central-limit-theorem",
                            "doc_label": "📘 Apostila PT-BR: Limite Central",
                            "pt_guide": {
                                "intuicao": "O <b>Teorema do Limite Central (TLC)</b> é quase mágica matemática: mesmo que os seus dados originais tenham um formato totalmente torto ou estranho, se você tirar várias amostras e calcular a <b>média de cada amostra</b>, a distribuição dessas médias sempre formará uma <b>Curva Normal perfeita</b>! É por isso que treinar redes neurais em pequenos lotes (<b>Mini-Batch SGD</b> de 32 ou 64 exemplos) funciona tão bem!",
                                "formula": "$$\\bar{X} \\sim \\mathcal{N}\\left(\\mu, \\frac{\\sigma^2}{n}\\right) \\implies \\text{Erro Padrão} = \\frac{\\sigma}{\\sqrt{n}}$$\nQuanto maior o tamanho da amostra $n$, menor a incerteza da média!",
                                "exemplo": "Jogar 1 dado tem distribuição reta (uniforme de 1 a 6). Mas se você jogar 30 dados e tirar a média deles repetidas vezes, o gráfico das médias forma um sino Gaussiano centrado em $3.5$!",
                                "codigo": "import numpy as np\n\n# Tirando 1000 médias de 30 lançamentos de dados (1 a 6)\nmedias = [np.random.randint(1, 7, size=30).mean() for _ in range(1000)]\nprint(f'Média global das amostras: {np.mean(medias):.2f} (Teórico: 3.50)')"
                            }
                        },
                        {
                            "title": "Intervalos de confiança e teste de hipóteses (noção)",
                            "video_url": "https://www.youtube.com/watch?v=TqOeMYtOc1w",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=intervalo+de+confianca+e+teste+de+hipoteses+portugues",
                            "doc_url": "https://pt.khanacademy.org/math/statistics-probability/confidence-intervals-one-sample",
                            "doc_label": "📘 Apostila PT-BR: Confiança & p-valor",
                            "pt_guide": {
                                "intuicao": "Quando você cria um novo modelo de IA e ele acerta $85\\%$ no teste contra $83\\%$ do modelo antigo, será que ele é realmente melhor ou foi pura sorte da amostra? O <b>Intervalo de Confiança</b> dá a margem de erro (ex.: $85\\% \\pm 1.2\\%$), e o <b>Teste de Hipóteses ($p$-valor)</b> mede a probabilidade de essa diferença ter ocorrido por puro acaso!",
                                "formula": "$$IC_{95\\%} = \\bar{x} \\pm 1.96 \\cdot \\frac{s}{\\sqrt{n}}$$\nRegra prática: Se o <b>$p$-valor $< 0.05$ (5%)</b>, rejeitamos a hipótese de sorte e confirmamos que a melhoria é estatisticamente significativa!",
                                "exemplo": "Em um Teste A/B de recomendação com $n=100$ usuários, média $\\bar{x}=50$ e desvio $s=10$:\nMargem de erro $= 1.96 \\times \\frac{10}{\\sqrt{100}} = 1.96$. Intervalo de 95%: $[48.04, 51.96]$.",
                                "codigo": "import numpy as np\n\nmedia, desvio, n = 85.0, 6.0, 100\nmargem_95 = 1.96 * (desvio / np.sqrt(n))\nprint(f'Acurácia com 95% de confiança: {media:.1f}% ± {margem_95:.2f}%')"
                            }
                        },
                        {
                            "title": "Máxima Verossimilhança (Maximum Likelihood Estimation - MLE)",
                            "video_url": "https://www.youtube.com/watch?v=XepXtl9YKwc",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=estimacao+de+maxima+verossimilhanca+estatistica+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/M%C3%A1xima_verossimilhan%C3%A7a",
                            "doc_label": "📘 Apostila PT-BR: MLE",
                            "pt_guide": {
                                "intuicao": "<b>Máxima Verossimilhança (MLE)</b> é o princípio filosófico por trás do treinamento de quase todos os modelos de Machine Learning e LLMs: <i>'Quais são os pesos $\\theta$ do modelo que tornam os dados reais que observamos no treinamento o mais prováveis possível?'</i>. Minimizar a função de perda <b>Cross-Entropy</b> é matematicamente idêntico a maximizar a log-verossimilhança!",
                                "formula": "$$\\hat{\\theta}_{\\text{MLE}} = \\arg\\max_{\\theta} \\sum_{i=1}^n \\log P(y_i \\mid x_i; \\theta)$$\nUsamos a soma dos logaritmos ($\\log$) porque multiplicar milhares de probabilidades pequenas ($0.01 \\times 0.01...$) zeraria a memória do computador (*underflow*)!",
                                "exemplo": "Se você jogou uma moeda 10 vezes e deu 7 Caras, qual o valor de $p$ (chance de Cara) que maximiza a verossimilhança desse resultado? Pela derivada da função log-verossimilhança, encontramos exatamente $\\hat{p} = 7/10 = 0.70$!",
                                "codigo": "import numpy as np\n\n# Testando qual parâmetro p maximiza a log-verossimilhança de 7 caras em 10 jogadas\nps = np.linspace(0.1, 0.9, 9)\nlog_lik = 7 * np.log(ps) + 3 * np.log(1 - ps)\nmelhor_p = ps[np.argmax(log_lik)]\nprint('Estimativa de Máxima Verossimilhança (p):', round(melhor_p, 2)) # 0.7"
                            }
                        },
                        {
                            "title": "Trade-off Viés vs. Variância (Bias-Variance Dilemma)",
                            "video_url": "https://www.youtube.com/watch?v=EuBBz3bI-aA",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=vies+e+variancia+machine+learning+overfitting+underfitting+portugues",
                            "doc_url": "https://www.deeplearningbook.com.br/underfitting-e-overfitting/",
                            "doc_label": "📘 Apostila PT-BR: Viés vs Variância",
                            "pt_guide": {
                                "intuicao": "Todo erro de um modelo de IA vem do equilíbrio entre dois extremos:\n• <b>Alto Viés (Underfitting):</b> O modelo é simples demais (ex.: tentar ajustar uma linha reta num gráfico em curva). Ele erra tanto no treino quanto no teste.\n• <b>Alta Variância (Overfitting):</b> O modelo decorou até o ruído dos dados de treino! Ele tira nota 100% no treino, mas falha miseravelmente em dados novos.",
                                "formula": "$$\\text{Erro Total} = \\text{Viés}^2 + \\text{Variância} + \\text{Ruído Irredutível}$$",
                                "exemplo": "• Modelo A: Treino = 65% | Teste = 64% $\\rightarrow$ Sofre de <b>Alto Viés (Underfitting)</b>.\n• Modelo B: Treino = 99% | Teste = 71% $\\rightarrow$ Sofre de <b>Alta Variância (Overfitting)</b>.\n• Modelo C: Treino = 92% | Teste = 90% $\\rightarrow$ <b>Equilíbrio Ideal (Generalização)</b>!",
                                "codigo": "# Diagnóstico automático de Viés vs Variância\ndef diagnosticar_modelo(acc_treino, acc_teste):\n    if acc_treino < 0.75:\n        return 'Alto Viés (Underfitting): aumente a capacidade do modelo!'\n    elif (acc_treino - acc_teste) > 0.10:\n        return 'Alta Variância (Overfitting): use Regularização/Dropout e mais dados!'\n    return 'Equilíbrio saudável (Boa generalização)!'\n\nprint(diagnosticar_modelo(0.99, 0.72))"
                            }
                        }
                    ]
                ]
            ]
        },
        {
            "t": "Módulo 4 · Funções Matemáticas, Geometria & Teoria da Informação",
            "d": "2 semanas",
            "tip": "💡 <b>Dica de Ouro:</b> Aqui você domina como as redes neurais medem seus próprios erros! Entender <b>Softmax</b> e <b>Cross-Entropy (Entropia Cruzada)</b> vai fazer você ler qualquer código de PyTorch ou artigo de IA com total naturalidade.",
            "p": "Implementar em Python as funções Softmax e Cross-Entropy Loss do zero e testar com previsões de um modelo.",
            "r": "Apostila Interativa Integrada em Português · Deep Learning Book Brasil · Khan Academy Álgebra PT-BR",
            "g": [
                [
                    "Álgebra e Geometria Analítica",
                    [
                        {
                            "title": "Equações, inequações e gráficos de funções aplicadas",
                            "video_url": "https://www.youtube.com/watch?v=WUvTyaaNkzM",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=funcoes+e+graficos+matematica+aula+portugues+ferretto",
                            "doc_url": "https://pt.khanacademy.org/math/algebra/x2f8bb11595b61c86:functions",
                            "doc_label": "📘 Apostila PT-BR: Funções & Reta",
                            "pt_guide": {
                                "intuicao": "A equação da reta $y = wx + b$ é a semente de toda a Inteligência Artificial! Nela, $w$ (*weight* / peso) é a <b>inclinação da reta</b> (o quanto $y$ muda para cada unidade de $x$), e $b$ (*bias* / viés) é o ponto onde a reta corta o eixo vertical (o valor base quando $x=0$). Uma inequação como $w_1 x_1 + w_2 x_2 + b > 0$ divide o plano em duas regiões (classificador linear!).",
                                "formula": "$$f(x) = w \\cdot x + b \\quad | \\quad \\text{Fronteira de decisão: } \\vec{w} \\cdot \\vec{x} + b = 0$$",
                                "exemplo": "Previsão de preço de imóvel: $\\text{Preço} = 8 \\cdot (\\text{m}^2) + 50$.\n• O peso $w = 8$ diz que cada metro quadrado adiciona R$ 8 mil.\n• O viés $b = 50$ é o valor base do terreno (R$ 50 mil).",
                                "codigo": "# Um neurônio linear simples\ndef neuronio_linear(x, w=8.0, b=50.0):\n    return w * x + b\n\nprint('Preço estimado para 70 m²:', neuronio_linear(70), 'mil reais') # 610.0"
                            }
                        },
                        {
                            "title": "Exponenciais e logaritmos na modelagem de IA",
                            "video_url": "https://www.youtube.com/watch?v=m2MIpDrF7Es",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=funcao+exponencial+e+logaritmo+numero+de+euler+portugues",
                            "doc_url": "https://pt.khanacademy.org/math/algebra2/x2ec2f6f830c9fb89:logs",
                            "doc_label": "📘 Apostila PT-BR: Exp & Log",
                            "pt_guide": {
                                "intuicao": "A função exponencial ($e^x$, onde $e \\approx 2.718$) transforma qualquer número (mesmo negativo!) em um número estritamente <b>positivo</b> e amplifica os maiores valores (base do Softmax!). Já o <b>Logaritmo Natural ($\\ln(x)$)</b> é a operação inversa: ele transforma multiplicações difíceis em somas simples ($\\ln(a \\cdot b) = \\ln a + \\ln b$) e penaliza severamente previsões erradas perto de zero!",
                                "formula": "$$e^0 = 1 \\quad | \\quad \\ln(e^x) = x \\quad | \\quad \\ln(a \\cdot b) = \\ln(a) + \\ln(b)$$",
                                "exemplo": "Na função de perda <i>Log-Loss</i> ($-\\ln(p)$):\n• Se o modelo prevê $p = 0.99$ para a classe certa, o erro é $-\\ln(0.99) \\approx 0.01$ (quase zero!).\n• Se o modelo prevê $p = 0.01$ para a classe certa, o erro explode para $-\\ln(0.01) \\approx 4.60$!",
                                "codigo": "import numpy as np\n\nfor p in [0.99, 0.50, 0.01]:\n    penalidade = -np.log(p)\n    print(f'Probabilidade prevista={p:.2f} -> Penalidade Log-Loss={penalidade:.3f}')"
                            }
                        },
                        {
                            "title": "Somatório, produtório e notação matemática em papers",
                            "video_url": "https://www.youtube.com/watch?v=TgKwz5hkrvw",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=somatorio+e+produtorio+notacao+sigma+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Somat%C3%B3rio",
                            "doc_label": "📘 Apostila PT-BR: Notação Sigma",
                            "pt_guide": {
                                "intuicao": "Sempre que você vir a letra grega <b>Sigma maiúscula ($\\sum$)</b> num artigo de IA, traduza mentalmente na hora para um <b>laço `for` somando elementos (`sum()`)</b> em Python! E quando vir o <b>Pi maiúsculo ($\\prod$)</b>, traduza para um laço multiplicando elementos (`np.prod()`). Só isso destrava 90% da leitura de papers!",
                                "formula": "$$\\sum_{i=1}^{n} x_i = x_1 + x_2 + \\dots + x_n \\quad | \\quad \\prod_{i=1}^{n} x_i = x_1 \\times x_2 \\times \\dots \\times x_n$$",
                                "exemplo": "Calcular $\\sum_{i=1}^{4} i^2$:\nPara $i=1, 2, 3, 4$, elevamos ao quadrado e somamos:\n$$1^2 + 2^2 + 3^2 + 4^2 = 1 + 4 + 9 + 16 = 30$$",
                                "codigo": "import numpy as np\n\nx = np.array([1, 2, 3, 4])\nsomatorio = np.sum(x ** 2)   # Sigma (Σ)\nprodutorio = np.prod(x)      # Pi (Π)\nprint(f'Somatório Σ(x²): {somatorio} | Produtório Π(x): {produtorio}')"
                            }
                        },
                        {
                            "title": "Geometria analítica e distância Euclidiana vs Manhattan",
                            "video_url": "https://www.youtube.com/watch?v=hl3bQySs8sM",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=distancia+euclidiana+e+manhattan+machine+learning+knn+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Dist%C3%A2ncia_euclidiana",
                            "doc_label": "📘 Apostila PT-BR: Distâncias",
                            "pt_guide": {
                                "intuicao": "Algoritmos como <b>KNN (Vizinhos Mais Próximos)</b>, <b>K-Means (Clusterização)</b> e bancos vetoriais agrupam pontos medindo a distância entre eles:\n• <b>Distância Euclidiana (L2):</b> A régua em linha reta (voo de pássaro) entre dois pontos.\n• <b>Distância de Manhattan (L1):</b> A soma das diferenças absolutas nos eixos (caminho de táxi em ruas quadriculadas).",
                                "formula": "$$d_{\\text{Euclidiana}}(\\vec{p}, \\vec{q}) = \\sqrt{\\sum_{i=1}^n (p_i - q_i)^2} \\quad | \\quad d_{\\text{Manhattan}}(\\vec{p}, \\vec{q}) = \\sum_{i=1}^n |p_i - q_i|$$",
                                "exemplo": "Entre os pontos $P = (1, 2)$ e $Q = (4, 6)$:\n• Diferenças nos eixos: $\\Delta x = |1-4| = 3$ e $\\Delta y = |2-6| = 4$.\n• <b>Manhattan:</b> $3 + 4 = 7$.\n• <b>Euclidiana:</b> $\\sqrt{3^2 + 4^2} = \\sqrt{25} = 5$.",
                                "codigo": "import numpy as np\n\np = np.array([1, 2])\nq = np.array([4, 6])\n\nd_euclid = np.linalg.norm(p - q, ord=2)\nd_manhat = np.linalg.norm(p - q, ord=1)\nprint(f'Euclidiana: {d_euclid} | Manhattan: {d_manhat}')"
                            }
                        }
                    ]
                ],
                [
                    "Teoria da Informação & Perda",
                    [
                        {
                            "title": "Entropia de Shannon (medida de incerteza da informação)",
                            "video_url": "https://www.youtube.com/watch?v=l6DKRf-fAAM",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=entropia+de+shannon+teoria+da+informacao+arvore+de+decisao+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Entropia_(teoria_da_informa%C3%A7%C3%A3o)",
                            "doc_label": "📘 Apostila PT-BR: Entropia Shannon",
                            "pt_guide": {
                                "intuicao": "Criada por Claude Shannon, a <b>Entropia ($H$)</b> mede o <b>grau de surpresa, bagunça ou incerteza</b> de uma distribuição de probabilidade:\n• Se uma moeda tem 100% de chance de dar Cara ($p=1.0$), não há surpresa nenhuma: <b>Entropia = 0</b>.\n• Se a moeda é honesta ($50\\%$ Cara / $50\\%$ Coroa), a incerteza é máxima: <b>Entropia = 1 bit</b>!\nÁrvores de Decisão (*Random Forest / XGBoost*) escolhem perguntas que reduzem a entropia!",
                                "formula": "$$H(P) = -\\sum_{i} P(x_i) \\log_2 P(x_i)$$",
                                "exemplo": "Para uma moeda justa $P = [0.5, 0.5]$:\n$$H = -(0.5 \\log_2 0.5 + 0.5 \\log_2 0.5) = -(0.5(-1) + 0.5(-1)) = 1.0 \\text{ bit}$$",
                                "codigo": "import numpy as np\n\ndef entropia_shannon(probs):\n    p = np.array(probs)\n    p = p[p > 0] # Evita log(0)\n    return -np.sum(p * np.log2(p))\n\nprint('Moeda viciada [0.99, 0.01]:', round(entropia_shannon([0.99, 0.01]), 3))\nprint('Moeda justa   [0.50, 0.50]:', round(entropia_shannon([0.50, 0.50]), 3))"
                            }
                        },
                        {
                            "title": "Entropia Cruzada (Cross-Entropy Loss) e função Softmax",
                            "video_url": "https://www.youtube.com/watch?v=6ArSys5qHAU",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=softmax+e+cross+entropy+entropia+cruzada+redes+neurais+portugues",
                            "doc_url": "https://www.deeplearningbook.com.br/funcao-softmax/",
                            "doc_label": "📘 Apostila PT-BR: Softmax & Cross-Entropy",
                            "pt_guide": {
                                "intuicao": "Esta é a dupla mais famosa do Deep Learning e dos LLMs:\n1. <b>Softmax:</b> Pega as notas brutas (*logits*) da última camada da rede (ex.: `[2.0, 1.0, 0.1]`) e aplica $e^x$ dividido pela soma, transformando tudo em <b>probabilidades que somam 100%</b> (`[0.66, 0.24, 0.10]`).\n2. <b>Cross-Entropy Loss (Entropia Cruzada):</b> Mede a distância entre a probabilidade que o modelo previu e o gabarito real!",
                                "formula": "$$\\text{Softmax}(z_i) = \\frac{e^{z_i}}{\\sum_{j} e^{z_j}} \\quad | \\quad L_{\\text{CE}} = -\\sum_{i} y_i \\ln(\\hat{p}_i) = -\\ln(\\hat{p}_{\\text{classe correta}})$$",
                                "exemplo": "Se o gabarito real é a classe 0 (`Gato`) e o Softmax do modelo deu $\\hat{p}_0 = 0.66$ (66% de confiança em Gato):\nO erro Cross-Entropy é simplesmente $-\\ln(0.66) \\approx 0.415$. Se o modelo melhorar para $99\\%$, o erro cai para $-\\ln(0.99) \\approx 0.01$!",
                                "codigo": "import numpy as np\n\nlogits = np.array([2.0, 1.0, 0.1])\n# 1. Softmax\nexps = np.exp(logits)\nprobs = exps / np.sum(exps)\nprint('Probabilidades Softmax:', np.round(probs, 3)) # [0.659, 0.242, 0.099]\n\n# 2. Cross-Entropy para classe correta = índice 0\nloss = -np.log(probs[0])\nprint('Cross-Entropy Loss:', round(loss, 4))"
                            }
                        },
                        {
                            "title": "Divergência de Kullback-Leibler (KL Divergence)",
                            "video_url": "https://www.youtube.com/watch?v=SxGYPqCgJWM",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=divergencia+kl+kullback+leibler+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Diverg%C3%AAncia_de_Kullback-Leibler",
                            "doc_label": "📘 Apostila PT-BR: Divergência KL",
                            "pt_guide": {
                                "intuicao": "A <b>Divergência KL ($D_{KL}(P \\parallel Q)$)</b> mede o quanto uma distribuição de probabilidade $Q$ (do seu modelo) se afastou de uma distribuição de referência $P$. Ela é fundamental no <b>RLHF / PPO / DPO</b> (alinhamento de LLMs como o ChatGPT): usamos a Divergência KL para garantir que o modelo alinhado não se afaste demais do modelo base original e não desaprendas a falar!",
                                "formula": "$$D_{KL}(P \\parallel Q) = \\sum_{i} P(i) \\ln\\left(\\frac{P(i)}{Q(i)}\\right)$$\nSe $P$ e $Q$ forem idênticas, $D_{KL} = 0$. Caso contrário, é sempre positiva ($> 0$).",
                                "exemplo": "Se o modelo base dá $P = [0.8, 0.2]$ e o novo modelo dá $Q = [0.5, 0.5]$:\n$$D_{KL} = 0.8 \\ln(0.8/0.5) + 0.2 \\ln(0.2/0.5) \\approx 0.376 - 0.183 = 0.193$$",
                                "codigo": "import numpy as np\n\nP = np.array([0.8, 0.2])\nQ = np.array([0.5, 0.5])\n\nkl_div = np.sum(P * np.log(P / Q))\nprint('Divergência KL(P || Q):', round(kl_div, 4)) # 0.1927"
                            }
                        },
                        {
                            "title": "Funções de perda de regressão (MSE, MAE, Huber) e classificação",
                            "video_url": "https://www.youtube.com/watch?v=Ilg3gGewQ5U",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=mse+mae+rmse+funcoes+de+perda+regressao+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Erro_quadr%C3%A1tico_m%C3%A9dio",
                            "doc_label": "📘 Apostila PT-BR: MSE, MAE & Huber",
                            "pt_guide": {
                                "intuicao": "Quando prevemos números contínuos (preços, vendas, temperatura), como medimos o erro?\n• <b>MSE (Erro Quadrático Médio):</b> Eleva o erro ao quadrado $(y - \\hat{y})^2$. Penaliza severamente erros grandes!\n• <b>MAE (Erro Absoluto Médio):</b> Usa o módulo $|y - \\hat{y}|$. É mais resistente a outliers.\n• <b>Huber Loss:</b> Combina o melhor dos dois (quadrática para erros pequenos e linear para erros gigantes).",
                                "formula": "$$\\text{MSE} = \\frac{1}{n}\\sum_{i=1}^n (y_i - \\hat{y}_i)^2 \\quad | \\quad \\text{MAE} = \\frac{1}{n}\\sum_{i=1}^n |y_i - \\hat{y}_i|$$",
                                "exemplo": "Erros em 3 previsões: `[1, 2, 10]`.\n• <b>MAE:</b> $(1 + 2 + 10) / 3 = 4.33$\n• <b>MSE:</b> $(1^2 + 2^2 + 10^2) / 3 = 105 / 3 = 35.0$ (Veja como o erro $10$ dominou o MSE!).",
                                "codigo": "import numpy as np\n\ny_real = np.array([100, 200, 300])\ny_prev = np.array([102, 195, 320])\n\nmse = np.mean((y_real - y_prev) ** 2)\nmae = np.mean(np.abs(y_real - y_prev))\nprint(f'MAE: {mae:.2f} | MSE: {mse:.2f} | RMSE: {np.sqrt(mse):.2f}')"
                            }
                        }
                    ]
                ]
            ]
        },
        {
            "t": "Módulo 5 · Matemática dos Transformers & Geometria de Embeddings",
            "d": "2 semanas",
            "tip": "💡 <b>Dica de Ouro:</b> Bem-vindo ao coração matemático do ChatGPT, Claude e Gemini! O mecanismo de <b>Atenção (Self-Attention)</b> nada mais é do que usar os conceitos dos Módulos 1 e 4 (Produto Escalar de Matrizes + Softmax) para fazer as palavras conversarem entre si!",
            "p": "Implementar em Python/NumPy a função exata de Scaled Dot-Product Attention e inspecionar a matriz de pesos de atenção.",
            "r": "Apostila Interativa Integrada em Português · Aulas UNIVESP Deep Learning & Transformers · Guia Visual de Atenção em Português",
            "g": [
                [
                    "Geometria Vetorial em IA Moderna",
                    [
                        {
                            "title": "Espaços vetoriais de alta dimensão e armazenamento de fatos em LLMs",
                            "video_url": "https://www.youtube.com/watch?v=9-Jl0dxWQs8",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=embeddings+espaco+vetorial+llms+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Word_embedding",
                            "doc_label": "📘 Apostila PT-BR: Alta Dimensão",
                            "pt_guide": {
                                "intuicao": "Nós humanos só conseguimos enxergar até 3 dimensões (largura, altura e profundidade). Mas os LLMs operam em espaços de <b>768, 1.536 ou 4.096 dimensões</b>! Nesses espaços gigantescos, cada direção pode codificar um conceito semântico independente (gênero, tempo verbal, capital de país, sentimento, idioma), permitindo que a rede armazene milhões de conceitos como direções quase perpendiculares!",
                                "formula": "$$\\vec{e}_{\\text{Rei}} - \\vec{e}_{\\text{Homem}} + \\vec{e}_{\\text{Mulher}} \\approx \\vec{e}_{\\text{Rainha}}$$",
                                "exemplo": "A aritmética vetorial funciona em conceitos! Se você subtrair o vetor de 'França' do vetor de 'Paris' e somar o vetor de 'Brasil', você aterrissa muito perto do vetor de 'Brasília'!",
                                "codigo": "import numpy as np\n\n# Simulando vetores semânticos [Realeza, Feminino, Idade]\nrei    = np.array([0.95, 0.05, 0.70])\nhomem  = np.array([0.05, 0.05, 0.70])\nmulher = np.array([0.05, 0.95, 0.70])\n\nresultado = rei - homem + mulher\nprint('Vetor resultante (Rainha):', np.round(resultado, 2)) # [0.95, 0.95, 0.70]"
                            }
                        },
                        {
                            "title": "Normalização de embeddings e geometria do espaço semântico",
                            "video_url": "https://www.youtube.com/watch?v=wjZofJX0v4M",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=word2vec+embeddings+busca+semantica+rag+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Vetor_unit%C3%A1rio",
                            "doc_label": "📘 Apostila PT-BR: Norm. Embeddings",
                            "pt_guide": {
                                "intuicao": "Em bancos de dados vetoriais (como Pinecone, Qdrant, Chroma e FAISS usados em sistemas RAG), costumamos <b>normalizar todos os embeddings para que tenham tamanho (norma L2) igual a $1.0$</b>. Por quê? Porque quando dois vetores têm tamanho $1$, a <b>Similaridade de Cosseno vira um simples Produto Escalar (`u @ v`)</b>, tornando a busca em milhões de documentos muito mais rápida!",
                                "formula": "$$\\hat{u} = \\frac{\\vec{u}}{\\|\\vec{u}\\|_2} \\implies \\|\\hat{u}\\|_2 = 1 \\implies \\cos(\\theta) = \\hat{u} \\cdot \\hat{v}$$",
                                "exemplo": "O vetor $\\vec{u} = [3, 4]$ tem tamanho $\\sqrt{3^2+4^2} = 5$.\nDividindo por $5$, obtemos o vetor unitário normalizado $\\hat{u} = [0.6, 0.8]$, pois $0.6^2 + 0.8^2 = 0.36 + 0.64 = 1.0$!",
                                "codigo": "import numpy as np\n\nu = np.array([3.0, 4.0])\nu_norm = u / np.linalg.norm(u)\nprint('Embedding normalizado:', u_norm)             # [0.6, 0.8]\nprint('Nova norma (sempre 1.0):', np.linalg.norm(u_norm)) # 1.0"
                            }
                        },
                        {
                            "title": "Projeções lineares e matrizes de pesos Query, Key e Value (W_q, W_k, W_v)",
                            "video_url": "https://www.youtube.com/watch?v=eMlx5fFNoYc",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=query+key+value+transformers+mecanismo+de+atencao+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Transformador_(modelo_de_aprendizado_de_m%C3%A1quina)",
                            "doc_label": "📘 Apostila PT-BR: Matrizes Q, K, V",
                            "pt_guide": {
                                "intuicao": "Para que cada palavra de uma frase converse com as outras no Transformer, multiplicamos o embedding de cada palavra $X$ por 3 matrizes aprendidas ($W_Q, W_K, W_V$), gerando 3 papéis:\n• <b>Query ($Q$ - Pergunta):</b> O que esta palavra está procurando no contexto? (ex.: um adjetivo procurando a qual substantivo se refere).\n• <b>Key ($K$ - Etiqueta/Chave):</b> O que esta palavra oferece de identificação?\n• <b>Value ($V$ - Conteúdo/Valor):</b> A informação semântica que será transferida se der *match*!",
                                "formula": "$$Q = X W_Q \\quad | \\quad K = X W_K \\quad | \\quad V = X W_V$$",
                                "exemplo": "Na frase <i>'O banco estava fechado porque ele faliu'</i>, a palavra <b>'ele'</b> gera uma <b>Query ($Q$)</b> procurando *'quem é o sujeito financeiro?'*. A palavra <b>'banco'</b> tem uma <b>Key ($K$)</b> compatível! O match entre $Q$ e $K$ transfere o <b>Value ($V$)</b> de 'banco' para 'ele'.",
                                "codigo": "import numpy as np\n\n# 3 palavras com embeddings de dimensão 4\nX = np.random.randn(3, 4)\n# Matrizes de projeção (4 -> 2)\nWq, Wk, Wv = np.random.randn(4, 2), np.random.randn(4, 2), np.random.randn(4, 2)\n\nQ, K, V = X @ Wq, X @ Wk, X @ Wv\nprint('Shapes Q, K, V:', Q.shape, K.shape, V.shape) # (3, 2)"
                            }
                        }
                    ]
                ],
                [
                    "Matemática da Atenção",
                    [
                        {
                            "title": "Fórmula de Scaled Dot-Product Attention: softmax((Q @ K^T) / sqrt(d_k)) * V",
                            "video_url": "https://www.youtube.com/watch?v=eMlx5fFNoYc",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=scaled+dot+product+attention+transformer+portugues+univesp",
                            "doc_url": "https://pt.wikipedia.org/wiki/Aten%C3%A7%C3%A3o_(aprendizado_de_m%C3%A1quina)",
                            "doc_label": "📘 Apostila PT-BR: Fórmula da Atenção",
                            "pt_guide": {
                                "intuicao": "Esta é a equação mais importante da IA moderna (do artigo *Attention Is All You Need*), explicada passo a passo:\n1. <b>`Q @ K.T`</b>: Calcula o produto escalar entre todas as Perguntas ($Q$) e todas as Chaves ($K$), medindo a afinidade entre cada par de palavras.\n2. <b>`/ sqrt(d_k)`</b>: Divide pela raiz da dimensão para que os números não fiquem gigantescos e não saturem o Softmax.\n3. <b>`softmax(...)`</b>: Transforma as afinidades em pesos percentuais que somam $100\\%$.\n4. <b>`@ V`</b>: Faz a média ponderada dos Valores ($V$) com base na atenção!",
                                "formula": "$$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{Q K^T}{\\sqrt{d_k}}\\right) V$$",
                                "exemplo": "Se uma palavra dá $80\\%$ de atenção para 'banco' e $20\\%$ para 'fechado', seu novo vetor será $0.80 \\cdot V_{\\text{banco}} + 0.20 \\cdot V_{\\text{fechado}}$!",
                                "codigo": "import numpy as np\n\ndef self_attention(Q, K, V):\n    d_k = Q.shape[-1]\n    scores = (Q @ K.T) / np.sqrt(d_k)\n    exps = np.exp(scores - np.max(scores, axis=-1, keepdims=True))\n    pesos_atencao = exps / np.sum(exps, axis=-1, keepdims=True)\n    return pesos_atencao @ V, pesos_atencao\n\nQ = K = V = np.array([[1.0, 0.0], [0.9, 0.2], [0.0, 1.0]])\nsaida, pesos = self_attention(Q, K, V)\nprint('Matriz de Pesos de Atenção:\\n', np.round(pesos, 2))"
                            }
                        },
                        {
                            "title": "Mecanismo Multi-Head Attention: divisão de dimensões e concatenação",
                            "video_url": "https://www.youtube.com/watch?v=wjZofJX0v4M",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=multi+head+attention+transformers+explicacao+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Transformador_(modelo_de_aprendizado_de_m%C3%A1quina)",
                            "doc_label": "📘 Apostila PT-BR: Multi-Head Attention",
                            "pt_guide": {
                                "intuicao": "Por que ter apenas 1 cabeça de atenção se podemos ter várias em paralelo (<b>Multi-Head Attention</b>)? Dividindo um embedding de $512$ dimensões em $8$ cabeças de $64$ dimensões cada:\n• A <b>Cabeça 1</b> pode focar na relação gramatical (sujeito $\\leftrightarrow$ verbo).\n• A <b>Cabeça 2</b> pode focar em pronomes ('ele' $\\leftrightarrow$ 'João').\n• A <b>Cabeça 3</b> pode focar em rimas ou código!\nNo final, concatenamos todas as cabeças lado a lado e multiplicamos por $W_O$.",
                                "formula": "$$\\text{MultiHead}(Q, K, V) = \\text{Concat}(\\text{head}_1, \\dots, \\text{head}_h) W_O$$",
                                "exemplo": "Se `d_model = 768` e usamos `num_heads = 12`, cada cabeça trabalha com vetores menores de tamanho `d_k = 768 / 12 = 64`. Quando juntamos as 12 saídas de tamanho 64 (`12 * 64`), voltamos exatamente para `768`!",
                                "codigo": "import numpy as np\n\n# Simulando Concatenação de 2 cabeças de atenção (cada uma com dimensão 2 -> total 4)\nhead_1 = np.array([[0.1, 0.2], [0.3, 0.4]]) # Foco sintático\nhead_2 = np.array([[0.8, 0.9], [0.5, 0.6]]) # Foco semântico\n\nconcat = np.concatenate([head_1, head_2], axis=-1)\nprint('Saída concatenada (2 tokens x 4 dims):\\n', concat)"
                            }
                        },
                        {
                            "title": "Positional Encodings: funções sinusoidais e rotação vetorial (RoPE)",
                            "video_url": "https://www.youtube.com/watch?v=eMlx5fFNoYc",
                            "video_label": "▶ Aula Visual (Leg. PT-BR)",
                            "yt_pt_url": "https://www.youtube.com/results?search_query=positional+encoding+rope+transformers+portugues",
                            "doc_url": "https://pt.wikipedia.org/wiki/Transformador_(modelo_de_aprendizado_de_m%C3%A1quina)",
                            "doc_label": "📘 Apostila PT-BR: Positional & RoPE",
                            "pt_guide": {
                                "intuicao": "Diferente dos humanos, o Transformer processa todas as palavras da frase ao mesmo tempo (em paralelo). Sem uma marcação de posição, para ele <i>'O cachorro mordeu o homem'</i> seria idêntico a <i>'O homem mordeu o cachorro'</i>! O <b>Positional Encoding</b> injeta a ordem das palavras usando ondas de seno e cosseno. Nos LLMs atuais (Llama 3, Qwen, DeepSeek), usamos o <b>RoPE (Rotary Position Embedding)</b>, que gira os vetores $Q$ e $K$ em um ângulo proporcional à posição da palavra!",
                                "formula": "$$PE_{(pos, 2i)} = \\sin\\left(\\frac{pos}{10000^{2i/d}}\\right) \\quad | \\quad R_\\theta = \\begin{bmatrix} \\cos(m\\theta) & -\\sin(m\\theta) \\\\ \\sin(m\\theta) & \\cos(m\\theta) \\end{bmatrix}$$",
                                "exemplo": "Com o <b>RoPE</b>, se a palavra A está na posição $2$ e a palavra B está na posição $5$, o produto escalar entre elas depende apenas da <b>distância relativa ($5 - 2 = 3$)</b> entre os seus ângulos de rotação!",
                                "codigo": "import numpy as np\n\n# Aplicando Rotação Posicional 2D (RoPE) em um vetor na posição m\ndef aplicar_rope_2d(vetor, pos, theta=0.1):\n    ang = pos * theta\n    R = np.array([[np.cos(ang), -np.sin(ang)],\n                  [np.sin(ang),  np.cos(ang)]])\n    return R @ vetor\n\nv = np.array([1.0, 0.0])\nprint('Posição 0:', np.round(aplicar_rope_2d(v, 0), 3))\nprint('Posição 5:', np.round(aplicar_rope_2d(v, 5), 3))"
                            }
                        }
                    ]
                ]
            ]
        }
    ]
