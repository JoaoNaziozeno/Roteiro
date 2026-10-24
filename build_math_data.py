# -*- coding: utf-8 -*-
"""
Gerador de dados 100% em Português (PT-BR) para a Trilha de Matemática Essencial para IA (43 tópicos).
Inclui:
- 1ª Opção de Videoaula Principal: Canal Oficial Khan Academy Português (https://www.youtube.com/@khanacademyportugues/videos) - Didática passo a passo no quadro.
- 2ª Opção de Videoaula: Animações Visuais 3Blue1Brown & StatQuest preservadas como segunda opção.
- Apostila Interativa Completa em Português (Intuição, Fórmula Explicada, Exemplo Passo a Passo e Código Python) para cada um dos 43 tópicos.
- Links de unidades e exercícios 100% em Português na Khan Academy Brasil (pt.khanacademy.org).
"""

def get_enriched_mat_phases():
    return [{'t': 'Módulo 1 · Álgebra Linear para IA & Tensores',
  'd': '3 a 4 semanas',
  'tip': '💡 <b>Como Estudar sem Travar:</b> Comece clicando no botão vermelho <b>▶ Khan Academy PT-BR</b> (1ª Opção) '
         'para assistir à explicação calma, passo a passo e em português no quadro. Depois, leia os 4 passos da <b>📘 '
         'Aula Visual PT-BR</b> logo abaixo do vídeo. Quando quiser ver a intuição geométrica animada, alterne para a '
         '<b>🎬 2ª Opção (3B1B / StatQuest)</b>!',
  'p': 'Implementar multiplicação de matrizes pura em Python e comparar o tempo de execução com `numpy.dot` e '
       '`torch.matmul`.',
  'r': '1ª Opção: Canal Oficial Khan Academy Português (@khanacademyportugues) · 2ª Opção: 3Blue1Brown & StatQuest · '
       'Aula Visual & Apostila Interativa em Português',
  'g': [['Vetores e Operações',
         [{'title': 'Vetores e espaços vetoriais: intuição geométrica',
           'video_url': 'https://www.youtube.com/watch?v=Y0ZyUhi0khY',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=vetores+algebra+linear',
           'doc_url': 'https://pt.khanacademy.org/math/linear-algebra/vectors-and-spaces/vectors/v/vector-introduction-linear-algebra',
           'doc_label': '📘 Aula Visual PT-BR: Vetores',
           'pt_guide': {'intuicao': 'Na Física, um vetor é uma seta no espaço com tamanho e direção. Na Computação e '
                                    'na IA, um <b>vetor é simplesmente uma lista ordenada de números</b> (por exemplo, '
                                    'as características de um imóvel: `[área, quartos, idade]`). Geométrica e '
                                    'algebricamente são a mesma coisa: cada número da lista é uma coordenada que diz o '
                                    'quanto andar nos eixos X, Y, Z...',
                        'formula': '$$\\vec{v} = \\begin{bmatrix} x_1 \\\\ x_2 \\\\ \\vdots \\\\ x_n \\end{bmatrix} '
                                   '\\in \\mathbb{R}^n$$\n'
                                   'Onde $\\mathbb{R}^n$ significa um espaço com $n$ dimensões reais (ex.: um '
                                   'embedding da OpenAI vive em $\\mathbb{R}^{1536}$, ou seja, uma lista de 1.536 '
                                   'números).',
                        'exemplo': 'Imagine representar dois clientes de um banco como vetores 2D: `[renda_mensal_mil, '
                                   'score_credito_cem]`.\n'
                                   '• Cliente A: $\\vec{a} = [5, 8]$\n'
                                   '• Cliente B: $\\vec{b} = [3, 6]$\n'
                                   'Somar os dois vetores é somar posição por posição: $\\vec{a} + \\vec{b} = [5+3, '
                                   '8+6] = [8, 14]$. Multiplicar por um número (escalar $2$) estica o vetor: $2 \\cdot '
                                   '\\vec{a} = [10, 16]$.',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  '# Criando dois vetores em Python (NumPy)\n'
                                  'a = np.array([5, 8])\n'
                                  'b = np.array([3, 6])\n'
                                  '\n'
                                  "print('Soma vetorial:', a + b)         # [ 8 14]\n"
                                  "print('Multiplicação por escalar:', 2 * a) # [10 16]"},
           'video2_url': 'https://www.youtube.com/watch?v=fNk_zzaMoSs',
           'video2_label': '🎬 2ª Opção: 3B1B Vetores'},
          {'title': 'Combinações lineares, espaço gerado (span) e bases',
           'video_url': 'https://www.youtube.com/watch?v=pWGCka7DLWE',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=combinacoes+lineares+espaco+gerado',
           'doc_url': 'https://pt.khanacademy.org/math/linear-algebra/vectors-and-spaces/linear-combinations/v/linear-combinations-and-span',
           'doc_label': '📘 Aula Visual PT-BR: Span & Bases',
           'pt_guide': {'intuicao': '<b>Combinação Linear</b> é misturar vetores multiplicando cada um por um peso '
                                    '($c_1, c_2...$) e somando tudo — exatamente o que um neurônio artificial faz com '
                                    'os dados de entrada! O <b>Espaço Gerado (Span)</b> é o conjunto de todos os '
                                    'pontos que você consegue alcançar fazendo essas misturas. Já uma <b>Base</b> é o '
                                    'conjunto mínimo de vetores independentes (que não são redundantes) capazes de '
                                    'gerar todo o espaço.',
                        'formula': '$$\\vec{w} = c_1 \\vec{v}_1 + c_2 \\vec{v}_2 + \\dots + c_k \\vec{v}_k$$\n'
                                   '• $\\vec{v}_1, \\vec{v}_2$: Vetores de base (direções fundamentais)\n'
                                   '• $c_1, c_2$: Pesos escalares (quanto usamos de cada vetor)',
                        'exemplo': 'No plano 2D, os vetores padrão são $\\hat{i} = [1, 0]$ (passo para a direita) e '
                                   '$\\hat{j} = [0, 1]$ (passo para cima).\n'
                                   'Para chegar ao ponto $[4, 7]$, fazemos a combinação linear:\n'
                                   '$$4 \\cdot [1, 0] + 7 \\cdot [0, 1] = [4, 0] + [0, 7] = [4, 7]$$\n'
                                   'Como $\\hat{i}$ e $\\hat{j}$ apontam em direções diferentes, o <b>Span</b> deles '
                                   'cobre todo o plano 2D! Mas se tivéssemos $[1, 2]$ e $[2, 4]$ (um é o dobro do '
                                   'outro), eles estariam presos na mesma linha reta (são linearmente dependentes).',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'v1 = np.array([1, 0])\n'
                                  'v2 = np.array([0, 1])\n'
                                  '\n'
                                  '# Combinação linear com pesos c1 = 4 e c2 = 7\n'
                                  'c1, c2 = 4, 7\n'
                                  'resultado = c1 * v1 + c2 * v2\n'
                                  "print('Ponto alcançado no espaço:', resultado) # [4 7]"},
           'video2_url': 'https://www.youtube.com/watch?v=k7RM-ot2NWY',
           'video2_label': '🎬 2ª Opção: 3B1B Span & Bases'},
          {'title': 'Produto escalar (Dot Product) e projeções',
           'video_url': 'https://www.youtube.com/watch?v=OtGMHiOmMGE',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=produto+escalar+vetores',
           'doc_url': 'https://pt.khanacademy.org/math/linear-algebra/vectors-and-spaces/dot-cross-products/v/vector-dot-product-and-vector-length',
           'doc_label': '📘 Aula Visual PT-BR: Produto Escalar',
           'pt_guide': {'intuicao': 'O <b>Produto Escalar (Dot Product)</b> é a operação mais importante de toda a '
                                    'Inteligência Artificial! Você pega dois vetores do mesmo tamanho, multiplica os '
                                    'elementos de mesma posição e soma tudo, gerando um único número. Geometricamente, '
                                    'ele mede <b>o quanto dois vetores apontam para a mesma direção</b> (a '
                                    'sombra/projeção de um sobre o outro).',
                        'formula': '$$\\vec{u} \\cdot \\vec{v} = \\sum_{i=1}^{n} u_i v_i = u_1 v_1 + u_2 v_2 + \\dots '
                                   '+ u_n v_n$$\n'
                                   'interpretação do resultado:\n'
                                   '• <b>Positivo ($> 0$):</b> Apontam para direções parecidas.\n'
                                   '• <b>Zero ($= 0$):</b> São perpendiculares (90°, ortogonais / sem relação).\n'
                                   '• <b>Negativo ($< 0$):</b> Apontam em sentidos opostos.',
                        'exemplo': 'Dados $\\vec{u} = [2, 3, 1]$ e $\\vec{v} = [4, 0, -2]$:\n'
                                   '$$\\vec{u} \\cdot \\vec{v} = (2 \\times 4) + (3 \\times 0) + (1 \\times -2) = 8 + '
                                   '0 - 2 = 6$$\n'
                                   'Em uma rede neural, a saída de um neurônio antes da ativação é exatamente o '
                                   'produto escalar entre o vetor de entradas $\\vec{x}$ e o vetor de pesos '
                                   '$\\vec{w}$!',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'u = np.array([2, 3, 1])\n'
                                  'v = np.array([4, 0, -2])\n'
                                  '\n'
                                  '# Três formas equivalentes em Python:\n'
                                  'dot1 = np.dot(u, v)\n'
                                  'dot2 = u @ v\n'
                                  "print('Produto Escalar:', dot2) # 6"},
           'video2_url': 'https://www.youtube.com/watch?v=LyGKycYT2v0',
           'video2_label': '🎬 2ª Opção: 3B1B Dot Product'},
          {'title': 'Norma de vetores (L1, L2 Euclidiana) e distâncias',
           'video_url': 'https://www.youtube.com/watch?v=jnwlDOrLD_M',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=modulo+norma+vetor+comprimento',
           'doc_url': 'https://pt.khanacademy.org/math/precalculus/x9e81a4f98389efdf:vectors/x9e81a4f98389efdf:vector-magnitude/v/finding-vector-magnitude-from-components',
           'doc_label': '📘 Aula Visual PT-BR: Normas L1 e L2',
           'pt_guide': {'intuicao': 'A <b>Norma</b> de um vetor mede o seu <b>tamanho (comprimento)</b> desde a origem '
                                    '$[0,0]$ até a ponta da seta. Em Machine Learning usamos principalmente duas '
                                    'normas para medir erros e regularizar pesos (evitar overfitting):\n'
                                    '• <b>Norma L1 (Manhattan / Lasso):</b> Soma dos valores absolutos (como andar em '
                                    'quarteirões).\n'
                                    '• <b>Norma L2 (Euclidiana / Ridge):</b> Teorema de Pitágoras (linha reta direta).',
                        'formula': '$$\\|\\vec{v}\\|_1 = |v_1| + |v_2| + \\dots + |v_n|$$\n'
                                   '$$\\|\\vec{v}\\|_2 = \\sqrt{v_1^2 + v_2^2 + \\dots + v_n^2}$$',
                        'exemplo': 'Para o vetor $\\vec{v} = [3, -4]$:\n'
                                   '• <b>Norma L1:</b> $|3| + |-4| = 3 + 4 = 7$\n'
                                   '• <b>Norma L2 (Euclidiana):</b> $\\sqrt{3^2 + (-4)^2} = \\sqrt{9 + 16} = '
                                   '\\sqrt{25} = 5$',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'v = np.array([3, -4])\n'
                                  '\n'
                                  'norma_l1 = np.linalg.norm(v, ord=1)\n'
                                  'norma_l2 = np.linalg.norm(v, ord=2)\n'
                                  "print(f'Norma L1: {norma_l1} | Norma L2 (Euclidiana): {norma_l2}')"},
           'video2_url': 'https://www.youtube.com/watch?v=LyGKycYT2v0',
           'video2_label': '🎬 2ª Opção: 3B1B Normas'},
          {'title': 'Ângulo entre vetores e Similaridade de Cosseno',
           'video_url': 'https://www.youtube.com/watch?v=0HOoTNrRDU4',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=angulo+entre+vetores+produto+escalar',
           'doc_url': 'https://pt.khanacademy.org/math/linear-algebra/vectors-and-spaces/dot-cross-products/v/defining-the-angle-between-vectors',
           'doc_label': '📘 Aula Visual PT-BR: Cosseno',
           'pt_guide': {'intuicao': "Como sistemas de busca semântica, RAG e ChatGPT sabem que a frase <i>'cachorro "
                                    "feliz'</i> é parecida com <i>'cão alegre'</i>? Usando a <b>Similaridade de "
                                    'Cosseno</b>! Em vez de olhar para o tamanho dos vetores, ela mede apenas o '
                                    '<b>cosseno do ângulo $\\theta$</b> entre eles. Se apontam para a mesma direção '
                                    '($\\theta = 0^\\circ$), a similaridade é $1.0$ (100% idênticos em significado)!',
                        'formula': '$$\\text{similaridade}(\\vec{u}, \\vec{v}) = \\cos(\\theta) = \\frac{\\vec{u} '
                                   '\\cdot \\vec{v}}{\\|\\vec{u}\\|_2 \\cdot \\|\\vec{v}\\|_2}$$\n'
                                   'O valor sempre fica entre $-1$ (opostos), $0$ (sem relação) e $+1$ (mesma '
                                   'direção).',
                        'exemplo': 'Sejam $\\vec{u} = [1, 2]$ e $\\vec{v} = [2, 4]$ (mesma direção, tamanhos '
                                   'diferentes):\n'
                                   '• Produto escalar: $1(2) + 2(4) = 10$\n'
                                   '• Normas: $\\|\\vec{u}\\| = \\sqrt{5}$ e $\\|\\vec{v}\\| = \\sqrt{20} = '
                                   '2\\sqrt{5}$\n'
                                   '• Cosseno: $\\frac{10}{\\sqrt{5} \\cdot 2\\sqrt{5}} = \\frac{10}{10} = 1.0$ '
                                   '(Similaridade máxima!).',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'u = np.array([1, 2])\n'
                                  'v = np.array([2, 4])\n'
                                  '\n'
                                  'cos_sim = (u @ v) / (np.linalg.norm(u) * np.linalg.norm(v))\n'
                                  "print(f'Similaridade de Cosseno: {cos_sim:.4f}') # 1.0000"},
           'video2_url': 'https://www.youtube.com/watch?v=e9U0QAFbfLI',
           'video2_label': '🎬 2ª Opção: StatQuest Cosseno'}]],
        ['Matrizes e Tensores',
         [{'title': 'Matrizes como transformações lineares no espaço',
           'video_url': 'https://www.youtube.com/watch?v=4PCktDZJH8E',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=transformacoes+lineares+matrizes',
           'doc_url': 'https://pt.khanacademy.org/math/linear-algebra/matrix-transformations/linear-transformations/v/linear-transformations',
           'doc_label': '📘 Aula Visual PT-BR: Transformações',
           'pt_guide': {'intuicao': 'Uma <b>Matriz</b> não é apenas uma tabela morta de números: ela é uma <b>máquina '
                                    'que move, gira, estica ou achata o espaço</b>! Quando você multiplica uma matriz '
                                    '$A$ por um vetor $\\vec{x}$, a matriz transforma esse vetor em um novo vetor. '
                                    'Cada camada de uma Rede Neural (*Linear Layer*) é literalmente uma matriz que '
                                    'deforma os dados para separar classes!',
                        'formula': '$$\\vec{y} = A \\vec{x} = \\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix} '
                                   '\\begin{bmatrix} x \\\\ y \\end{bmatrix} = \\begin{bmatrix} ax + by \\\\ cx + dy '
                                   '\\end{bmatrix}$$\n'
                                   'Dica visual: A 1ª coluna da matriz diz onde o eixo X ($[1,0]$) vai parar; a 2ª '
                                   'coluna diz onde o eixo Y ($[0,1]$) vai parar!',
                        'exemplo': 'A matriz $A = \\begin{bmatrix} 2 & 0 \\\\ 0 & 3 \\end{bmatrix}$ duplica a largura '
                                   '(X) e triplica a altura (Y) de qualquer vetor.\n'
                                   'Se aplicarmos no vetor $\\vec{x} = [4, 5]$:\n'
                                   '$$A\\vec{x} = [2 \\times 4, 3 \\times 5] = [8, 15]$$',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  '# Matriz que gira qualquer vetor 2D em 90 graus para a esquerda\n'
                                  'R_90 = np.array([[0, -1],\n'
                                  '                 [1,  0]])\n'
                                  'v = np.array([3, 0]) # Aponta para a direita\n'
                                  "print('Vetor após rotação de 90°:', R_90 @ v) # [0, 3] (Aponta para cima!)"},
           'video2_url': 'https://www.youtube.com/watch?v=kYB8IZa5AuE',
           'video2_label': '🎬 2ª Opção: 3B1B Matrizes'},
          {'title': 'Multiplicação de matrizes (Dot product vs. Hadamard elemento a elemento)',
           'video_url': 'https://www.youtube.com/watch?v=0ziYp9N-zGE',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=multiplicacao+de+matrizes',
           'doc_url': 'https://pt.khanacademy.org/math/precalculus/x9e81a4f98389efdf:matrices/x9e81a4f98389efdf:multiplying-matrices-by-matrices/v/matrix-multiplication-intro',
           'doc_label': '📘 Aula Visual PT-BR: Mult. Matrizes',
           'pt_guide': {'intuicao': 'Existem duas multiplicações muito diferentes em IA e confundi-las é o erro nº 1 '
                                    'em PyTorch/NumPy:\n'
                                    '1. <b>Multiplicação Matricial (`A @ B`):</b> Linha da primeira $\\times$ Coluna '
                                    'da segunda. Só funciona se o nº de colunas de $A$ for igual ao nº de linhas de '
                                    '$B$ ($m \\times k$ com $k \\times n \\rightarrow m \\times n$).\n'
                                    '2. <b>Produto de Hadamard (`A * B`):</b> Multiplica posição por posição (exige '
                                    'matrizes de mesmo tamanho).',
                        'formula': '$$\\text{Matricial: } (AB)_{ij} = \\sum_{k} A_{ik} B_{kj} \\quad | \\quad '
                                   '\\text{Hadamard: } (A \\odot B)_{ij} = A_{ij} \\cdot B_{ij}$$',
                        'exemplo': 'Sejam $A = \\begin{bmatrix} 1 & 2 \\\\ 3 & 4 \\end{bmatrix}$ e $B = '
                                   '\\begin{bmatrix} 2 & 0 \\\\ 1 & 3 \\end{bmatrix}$:\n'
                                   '• <b>Hadamard (`A * B`):</b> $\\begin{bmatrix} 1\\times 2 & 2\\times 0 \\\\ '
                                   '3\\times 1 & 4\\times 3 \\end{bmatrix} = \\begin{bmatrix} 2 & 0 \\\\ 3 & 12 '
                                   '\\end{bmatrix}$\n'
                                   '• <b>Matricial (`A @ B`):</b> 1ª linha com 1ª coluna $= 1(2)+2(1)=4$; 1ª linha com '
                                   '2ª coluna $= 1(0)+2(3)=6 \\rightarrow \\begin{bmatrix} 4 & 6 \\\\ 10 & 12 '
                                   '\\end{bmatrix}$.',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'A = np.array([[1, 2], [3, 4]])\n'
                                  'B = np.array([[2, 0], [1, 3]])\n'
                                  '\n'
                                  "print('Matricial (A @ B):\\n', A @ B)\n"
                                  "print('Elemento a elemento / Hadamard (A * B):\\n', A * B)"},
           'video2_url': 'https://www.youtube.com/watch?v=XkY2DOUCWMU',
           'video2_label': '🎬 2ª Opção: 3B1B Mult. Matrizes'},
          {'title': 'Sistemas de equações lineares e determinantes',
           'video_url': 'https://www.youtube.com/watch?v=OU9sWHk_dlw',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=determinante+matriz+sistemas+lineares',
           'doc_url': 'https://pt.khanacademy.org/math/precalculus/x9e81a4f98389efdf:matrices/x9e81a4f98389efdf:determinant-of-a-2x2-matrix/v/finding-the-determinant-of-a-2x2-matrix',
           'doc_label': '📘 Aula Visual PT-BR: Determinantes',
           'pt_guide': {'intuicao': 'Um sistema de várias equações pode ser escrito de forma compacta como $A\\vec{x} '
                                    '= \\vec{b}$. O <b>Determinante ($\\det(A)$)</b> mede <b>como a matriz altera a '
                                    'área ou volume</b> do espaço! Se $\\det(A) = 0$, significa que a matriz esmagou o '
                                    'espaço (por exemplo, achatou um quadrado 2D em uma linha 1D), perdendo informação '
                                    'de forma irreversível!',
                        'formula': '$$\\det\\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix} = a\\cdot d - b\\cdot c$$\n'
                                   '• Se $\\det(A) \\neq 0$: O sistema tem solução única e a matriz pode ser '
                                   'invertida.\n'
                                   '• Se $\\det(A) = 0$: Matriz singular (colunas redundantes / sem inversa).',
                        'exemplo': 'Para $A = \\begin{bmatrix} 3 & 2 \\\\ 1 & 4 \\end{bmatrix}$:\n'
                                   '$$\\det(A) = (3 \\times 4) - (2 \\times 1) = 12 - 2 = 10$$\n'
                                   'A matriz multiplica a área de qualquer figura por $10$!',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'A = np.array([[3, 2], [1, 4]])\n'
                                  'b = np.array([16, 13])\n'
                                  '\n'
                                  "print('Determinante:', round(np.linalg.det(A), 2)) # 10.0\n"
                                  '# Resolvendo o sistema A * x = b:\n'
                                  'x = np.linalg.solve(A, b)\n'
                                  "print('Solução x:', x) # [3.8, 2.3]"},
           'video2_url': 'https://www.youtube.com/watch?v=Ip3X9LOh2dk',
           'video2_label': '🎬 2ª Opção: 3B1B Determinante'},
          {'title': 'Inversa de matriz e pseudoinversa de Moore-Penrose',
           'video_url': 'https://www.youtube.com/watch?v=LSVLRg70DhA',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=matriz+inversa+introducao',
           'doc_url': 'https://pt.khanacademy.org/math/precalculus/x9e81a4f98389efdf:matrices/x9e81a4f98389efdf:intro-to-matrix-inverses/v/inverse-matrix-part-1',
           'doc_label': '📘 Aula Visual PT-BR: Matriz Inversa',
           'pt_guide': {'intuicao': "A <b>Matriz Inversa ($A^{-1}$)</b> é o 'Ctrl+Z' (desfazer) de uma transformação "
                                    'linear: se a matriz $A$ gira o espaço em $+30^\\circ$, a matriz $A^{-1}$ gira em '
                                    '$-30^\\circ$, voltando tudo ao original ($A \\cdot A^{-1} = I$, onde $I$ é a '
                                    'matriz identidade). E quando a matriz não é quadrada (ex.: 1.000 linhas de '
                                    'clientes e 5 colunas na Regressão Linear)? Usamos a <b>Pseudoinversa de '
                                    'Moore-Penrose ($A^+$)</b>, que encontra a melhor solução aproximada!',
                        'formula': '$$A \\cdot A^{-1} = I = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix} \\quad | '
                                   '\\quad \\text{Pseudoinversa: } A^+ = (A^T A)^{-1} A^T$$',
                        'exemplo': 'Se $A\\vec{x} = \\vec{b}$ e $A$ tem inversa, isolamos $\\vec{x}$ multiplicando '
                                   'pela inversa: $\\vec{x} = A^{-1}\\vec{b}$.\n'
                                   'Em Machine Learning, os pesos ótimos de uma Regressão Linear são calculados '
                                   'diretamente com a pseudoinversa: $\\vec{w} = X^+ \\vec{y}$!',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'A = np.array([[4, 7], [2, 6]])\n'
                                  'A_inv = np.linalg.inv(A)\n'
                                  "print('A @ A_inv (Identidade):\\n', np.round(A @ A_inv))\n"
                                  '\n'
                                  '# Pseudoinversa para matriz retangular (3x2):\n'
                                  'X = np.array([[1, 2], [3, 4], [5, 6]])\n'
                                  'X_pinv = np.linalg.pinv(X)\n'
                                  "print('Shape da Pseudoinversa:', X_pinv.shape) # (2, 3)"},
           'video2_url': 'https://www.youtube.com/watch?v=uQhTuRlWM3E',
           'video2_label': '🎬 2ª Opção: 3B1B Inversa & Colunas'},
          {'title': 'Autovalores e Autovetores (Eigenvalues & Eigenvectors)',
           'video_url': 'https://www.youtube.com/watch?v=hJhtsfeBLok',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=autovalores+e+autovetores',
           'doc_url': 'https://pt.khanacademy.org/math/linear-algebra/alternate-bases/eigen-everything/v/linear-algebra-introduction-to-eigenvalues-and-eigenvectors',
           'doc_label': '📘 Aula Visual PT-BR: Autovetores',
           'pt_guide': {'intuicao': 'Quando uma matriz transforma o espaço, quase todos os vetores mudam de direção. '
                                    'Mas existem alguns vetores especiais que <b>não mudam de direção</b> — eles '
                                    'apenas são esticados ou encolhidos! Esses vetores especiais são os <b>Autovetores '
                                    '(Eigenvectors)</b>, e o fator pelo qual eles são esticados é o <b>Autovalor '
                                    "(Eigenvalue $\\lambda$)</b>. Eles revelam os 'eixos principais' dos dados!",
                        'formula': '$$A \\vec{v} = \\lambda \\vec{v}$$\n'
                                   'Onde $A$ é a matriz, $\\vec{v}$ é o autovetor (direção preservada) e $\\lambda$ '
                                   '(lambda) é o autovalor (fator de escala).',
                        'exemplo': 'Na matriz $A = \\begin{bmatrix} 3 & 0 \\\\ 0 & 1 \\end{bmatrix}$, o vetor '
                                   '$\\vec{v}_1 = [1, 0]$ vira $[3, 0] = 3 \\cdot \\vec{v}_1$.\n'
                                   'Logo, $[1, 0]$ é um autovetor com autovalor $\\lambda = 3$ (a direção principal '
                                   'onde os dados mais crescem!).',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'A = np.array([[4, 2],\n'
                                  '              [1, 3]])\n'
                                  '\n'
                                  'autovalores, autovetores = np.linalg.eig(A)\n'
                                  "print('Autovalores (lambdas):', autovalores) # [5., 2.]"},
           'video2_url': 'https://www.youtube.com/watch?v=PFDu9oVAE-g',
           'video2_label': '🎬 2ª Opção: 3B1B Autovalores'},
          {'title': 'Decomposição em Valores Singulares (SVD) e PCA',
           'video_url': 'https://www.youtube.com/watch?v=pZ6mMVEE89g',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=autovalores+autovetores+matriz+2x2',
           'doc_url': 'https://pt.khanacademy.org/math/linear-algebra/alternate-bases/eigen-everything/v/linear-algebra-eigenvalues-of-a-2x2-matrix',
           'doc_label': '📘 Aula Visual PT-BR: SVD & PCA',
           'pt_guide': {'intuicao': 'Imagine uma tabela com 100 colunas correlacionadas. Como resumir essas 100 '
                                    'colunas em apenas 2 ou 3 colunas sem perder a informação essencial? Usando <b>PCA '
                                    '(Análise de Componentes Principais)</b> e <b>SVD (Decomposição em Valores '
                                    'Singulares)</b>! Eles encontram as direções de maior variância (maior '
                                    'espalhamento da informação) e descartam o ruído. O <b>LoRA</b> (usado para fazer '
                                    'fine-tuning de LLMs) usa exatamente decomposição de matrizes de baixo posto '
                                    'inspirada no SVD!',
                        'formula': '$$A = U \\Sigma V^T$$\n'
                                   'Qualquer matriz $A$ pode ser fatorada em uma rotação ($V^T$), um esticamento nos '
                                   'eixos principais ($\\Sigma$, matriz diagonal de valores singulares) e outra '
                                   'rotação ($U$).',
                        'exemplo': 'Se você tem fotos 1000x1000 pixels, o SVD permite manter apenas os 50 maiores '
                                   'valores singulares de $\\Sigma$, comprimindo a imagem em 90% mantendo quase toda a '
                                   'nitidez!',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  '# Criando dados 2D correlacionados\n'
                                  'X = np.array([[1, 2], [2, 4.1], [3, 5.9], [4, 8.2]])\n'
                                  'X_centrado = X - X.mean(axis=0)\n'
                                  '\n'
                                  '# Decomposição SVD\n'
                                  'U, S, Vt = np.linalg.svd(X_centrado)\n'
                                  "print('Valores Singulares (importância de cada eixo):', np.round(S, 2))"},
           'video2_url': 'https://www.youtube.com/watch?v=FgakZw6K1QQ',
           'video2_label': '🎬 2ª Opção: StatQuest PCA'}]]]},
 {'t': 'Módulo 2 · Cálculo Diferencial, Gradientes & Otimização',
  'd': '3 a 4 semanas',
  'tip': '💡 <b>Como Estudar sem Travar:</b> Comece clicando no botão vermelho <b>▶ Khan Academy PT-BR</b> (1ª Opção) '
         'para assistir à explicação calma, passo a passo e em português no quadro. Depois, leia os 4 passos da <b>📘 '
         'Aula Visual PT-BR</b> logo abaixo do vídeo. Quando quiser ver a intuição geométrica animada, alterne para a '
         '<b>🎬 2ª Opção (3B1B / StatQuest)</b>!',
  'p': 'Construir do zero em Python uma descida de gradiente que aprende sozinha os parâmetros de uma reta para prever '
       'preços.',
  'r': '1ª Opção: Canal Oficial Khan Academy Português (@khanacademyportugues) · 2ª Opção: 3Blue1Brown & StatQuest · '
       'Aula Visual & Apostila Interativa em Português',
  'g': [['Cálculo Diferencial',
         [{'title': 'Limites e taxa de variação instantânea (ideia geral)',
           'video_url': 'https://www.youtube.com/watch?v=fitJZb1KI44',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=introducao+aos+limites+derivadas',
           'doc_url': 'https://pt.khanacademy.org/math/AP-calculus-ab/ab-limits-new/ab-1-2/v/introduction-to-limits-hd',
           'doc_label': '📘 Aula Visual PT-BR: Limites & Taxa',
           'pt_guide': {'intuicao': "O <b>Limite</b> responde à pergunta: <i>'Para qual valor uma função está se "
                                    "aproximando quando chegamos infinitamente perto de um ponto?'</i>. A partir disso "
                                    'nasce a <b>Taxa de Variação Instantânea (Derivada)</b>: é como o velocímetro do '
                                    "carro num instante exato. Em IA, ela responde: <i>'Se eu mexer um milímetro neste "
                                    "peso $w$ da rede neural, o erro sobe ou desce?'</i>",
                        'formula': "$$f'(x) = \\lim_{h \\to 0} \\frac{f(x + h) - f(x)}{h}$$\n"
                                   'O numerador $f(x+h) - f(x)$ é a mudança na saída; o denominador $h$ é o pequeno '
                                   'passo dado na entrada.',
                        'exemplo': 'Seja $f(x) = x^2$. No ponto $x = 3$, temos $f(3) = 9$.\n'
                                   'Se dermos um micro-passo $h = 0.001$ para $x = 3.001$, temos $f(3.001) = '
                                   '9.006001$.\n'
                                   'Dividindo a variação pelo passo: $\\frac{9.006001 - 9}{0.001} \\approx 6$. Ou '
                                   'seja, a taxa de variação em $x=3$ é $6$!',
                        'codigo': '# Calculando a derivada numérica com um micro-passo h\n'
                                  'def f(x):\n'
                                  '    return x ** 2\n'
                                  '\n'
                                  'x = 3.0\n'
                                  'h = 0.0001\n'
                                  'derivada_aprox = (f(x + h) - f(x)) / h\n'
                                  "print(f'Taxa de variação em x=3: {derivada_aprox:.4f}') # ~6.0001"},
           'video2_url': 'https://www.youtube.com/watch?v=WUvTyaaNkzM',
           'video2_label': '🎬 2ª Opção: 3B1B Essência do Cálculo'},
          {'title': 'Derivadas fundamentais e regras básicas (potência, produto, soma)',
           'video_url': 'https://www.youtube.com/watch?v=W8QdwWyP0jY',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=regra+da+potencia+derivadas',
           'doc_url': 'https://pt.khanacademy.org/math/ap-calculus-ab/ab-differentiation-1-new/ab-2-5/v/power-rule',
           'doc_label': '📘 Aula Visual PT-BR: Regras Derivação',
           'pt_guide': {'intuicao': 'Em vez de calcular limites toda vez, usamos atalhos diretos chamados <b>Regras de '
                                    'Derivação</b>:\n'
                                    '• <b>Constante:</b> A derivada de um número fixo é $0$ (não varia).\n'
                                    "• <b>Regra do Tombo (Potência):</b> O expoente $n$ 'cai' multiplicando na frente "
                                    'e perde $1$ no topo ($x^n \\rightarrow n \\cdot x^{n-1}$).\n'
                                    '• <b>Soma:</b> A derivada da soma é a soma das derivadas.',
                        'formula': '$$\\frac{d}{dx}(x^n) = n \\cdot x^{n-1} \\quad | \\quad \\frac{d}{dx}(e^x) = e^x '
                                   '\\quad | \\quad \\frac{d}{dx}(\\ln x) = \\frac{1}{x}$$',
                        'exemplo': 'Qual a derivada da função de perda quadrática $L(w) = 3w^2 - 12w + 5$?\n'
                                   '• Derivada de $3w^2$: o $2$ tomba multiplicando o $3 \\rightarrow 6w$\n'
                                   '• Derivada de $-12w$: fica $-12$\n'
                                   '• Derivada de $+5$: é $0$\n'
                                   "Resultado: $L'(w) = 6w - 12$. (Para achar o ponto onde o erro é mínimo, igualamos "
                                   'a zero: $6w - 12 = 0 \\Rightarrow w = 2$!).',
                        'codigo': '# Verificando a derivada de L(w) = 3w^2 - 12w + 5\n'
                                  'def L_derivada(w):\n'
                                  '    return 6 * w - 12\n'
                                  '\n'
                                  "print('Inclinação em w=0:', L_derivada(0)) # -12 (erro descendo)\n"
                                  "print('Inclinação em w=2:', L_derivada(2)) # 0 (fundo do vale / erro mínimo!)"},
           'video2_url': 'https://www.youtube.com/watch?v=S0_qX4VFYMQ',
           'video2_label': '🎬 2ª Opção: 3B1B Derivadas Geométricas'},
          {'title': 'Regra da Cadeia (Chain Rule) - o motor do Backpropagation',
           'video_url': 'https://www.youtube.com/watch?v=sgYtbgQWcKw',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=regra+da+cadeia+derivadas',
           'doc_url': 'https://pt.khanacademy.org/math/ap-calculus-ab/ab-differentiation-2-new/ab-3-1a/v/chain-rule-introduction',
           'doc_label': '📘 Aula Visual PT-BR: Regra da Cadeia',
           'pt_guide': {'intuicao': 'Uma Rede Neural Profunda nada mais é do que uma <b>função dentro de outra função, '
                                    'dentro de outra função</b> (camada 1 $\\rightarrow$ camada 2 $\\rightarrow$ '
                                    'camada 3 $\\rightarrow$ erro). Como descobrir a culpa de um peso lá da 1ª camada '
                                    'pelo erro final lá na última camada? Usando a <b>Regra da Cadeia</b>! Ela diz que '
                                    'basta <b>multiplicar as derivadas locais de trás para frente</b>. Isso é 100% o '
                                    'algoritmo de <b>Backpropagation</b>!',
                        'formula': '$$\\frac{dL}{dw} = \\frac{dL}{dy} \\cdot \\frac{dy}{dz} \\cdot \\frac{dz}{dw}$$\n'
                                   '<i>Derivada da função de fora $\\times$ Derivada da função de dentro!</i>',
                        'exemplo': 'Se $z = 3w$ e $L = z^2$:\n'
                                   '• $\\frac{dL}{dz} = 2z$\n'
                                   '• $\\frac{dz}{dw} = 3$\n'
                                   'Pela Regra da Cadeia: $\\frac{dL}{dw} = 2z \\cdot 3 = 6z = 18w$.',
                        'codigo': '# Simulando um mini Backpropagation com Regra da Cadeia\n'
                                  'w = 2.0\n'
                                  'z = 3 * w      # Camada 1 (z = 6)\n'
                                  'L = z ** 2     # Loss final (L = 36)\n'
                                  '\n'
                                  '# Backpropagation (de trás para frente):\n'
                                  'dL_dz = 2 * z  # 12\n'
                                  'dz_dw = 3.0    # 3\n'
                                  'dL_dw = dL_dz * dz_dw\n'
                                  "print('Gradiente dL/dw via Regra da Cadeia:', dL_dw) # 36.0"},
           'video2_url': 'https://www.youtube.com/watch?v=YG15m2VwSjA',
           'video2_label': '🎬 2ª Opção: 3B1B Regra da Cadeia'},
          {'title': 'Derivadas de funções de ativação (Sigmoide, Tanh, ReLU, GeLU)',
           'video_url': 'https://www.youtube.com/watch?v=R0phEcQlHAg',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=derivada+como+inclinacao+da+curva',
           'doc_url': 'https://pt.khanacademy.org/math/ap-calculus-ab/ab-differentiation-1-new/ab-2-1/v/derivative-as-a-concept',
           'doc_label': '📘 Aula Visual PT-BR: Ativações',
           'pt_guide': {'intuicao': 'Sem <b>Funções de Ativação</b>, uma rede neural de 100 camadas seria '
                                    'matematicamente igual a uma única camada linear! As ativações dobram o espaço '
                                    'para aprender padrões complexos:\n'
                                    '• <b>Sigmoide:</b> Espreme números entre $0$ e $1$ (usada em probabilidades '
                                    'binárias).\n'
                                    '• <b>ReLU:</b> Se for negativo vira $0$; se for positivo passa direto! Sua '
                                    'derivada é simplesmente $0$ ou $1$, evitando o sumiço do gradiente (*vanishing '
                                    'gradient*).',
                        'formula': "$$\\text{ReLU}(x) = \\max(0, x) \\implies \\text{ReLU}'(x) = \\begin{cases} 1 & "
                                   '\\text{se } x > 0 \\\\ 0 & \\text{se } x < 0 \\end{cases}$$\n'
                                   "$$\\sigma(x) = \\frac{1}{1 + e^{-x}} \\implies \\sigma'(x) = \\sigma(x) \\cdot (1 "
                                   '- \\sigma(x))$$',
                        'exemplo': 'Se $x = 0$, a Sigmoide vale $\\sigma(0) = 0.5$. Sua derivada máxima ocorre aí: '
                                   "$\\sigma'(0) = 0.5 \\times (1 - 0.5) = 0.25$. Já para valores muito grandes "
                                   "($x=10$), $\\sigma'(10) \\approx 0$ (o neurônio satura e para de aprender!). Por "
                                   'isso a <b>ReLU</b> e a <b>GeLU</b> dominam os LLMs modernos.',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'def sigmoid(x):\n'
                                  '    return 1 / (1 + np.exp(-x))\n'
                                  '\n'
                                  'def sigmoid_derivada(x):\n'
                                  '    s = sigmoid(x)\n'
                                  '    return s * (1 - s)\n'
                                  '\n'
                                  'def relu_derivada(x):\n'
                                  '    return np.where(x > 0, 1.0, 0.0)\n'
                                  '\n'
                                  "print('Derivada ReLU em [-2, 5]:', relu_derivada(np.array([-2, 5]))) # [0., 1.]"},
           'video2_url': 'https://www.youtube.com/watch?v=aircAruvnKk',
           'video2_label': '🎬 2ª Opção: 3B1B Redes Neurais'}]],
        ['Gradientes e Otimizadores',
         [{'title': 'Derivadas parciais e o vetor Gradiente (nabla f)',
           'video_url': 'https://www.youtube.com/watch?v=EWcBlzlvdW8',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=derivadas+parciais+gradiente',
           'doc_url': 'https://pt.khanacademy.org/math/multivariable-calculus/multivariable-derivatives/partial-derivative-and-gradient-articles/a/the-gradient',
           'doc_label': '📘 Aula Visual PT-BR: Vetor Gradiente',
           'pt_guide': {'intuicao': 'Quando uma função depende de várias variáveis ao mesmo tempo (ex.: erro $L(w_1, '
                                    'w_2)$), calculamos a <b>Derivada Parcial ($\\partial$)</b> derivando uma variável '
                                    'de cada vez e fingindo que as outras são números fixos. Juntando todas as '
                                    'derivadas parciais dentro de um vetor, formamos o <b>Vetor Gradiente ($\\nabla '
                                    'L$)</b>, que aponta na direção de <b>maior subida</b> da montanha de erro!',
                        'formula': '$$\\nabla f(w_1, w_2) = \\begin{bmatrix} \\frac{\\partial f}{\\partial w_1} \\\\ '
                                   '\\frac{\\partial f}{\\partial w_2} \\end{bmatrix}$$',
                        'exemplo': 'Seja $f(w_1, w_2) = w_1^2 + 3w_2^2$.\n'
                                   '• Derivada parcial em relação a $w_1$: $\\frac{\\partial f}{\\partial w_1} = '
                                   '2w_1$\n'
                                   '• Derivada parcial em relação a $w_2$: $\\frac{\\partial f}{\\partial w_2} = '
                                   '6w_2$\n'
                                   'No ponto $(1, 2)$, o vetor gradiente é $\\nabla f = [2, 12]$. Para descer a '
                                   'montanha (reduzir o erro), andamos no sentido oposto: $[-2, -12]$!',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  '# Calculando o vetor gradiente de f(w1, w2) = w1^2 + 3*w2^2\n'
                                  'def gradiente(w):\n'
                                  '    w1, w2 = w[0], w[1]\n'
                                  '    return np.array([2 * w1, 6 * w2])\n'
                                  '\n'
                                  'ponto = np.array([1.0, 2.0])\n'
                                  "print('Vetor Gradiente no ponto (1,2):', gradiente(ponto)) # [ 2. 12.]"},
           'video2_url': 'https://www.youtube.com/watch?v=IHZwWFHWa-w',
           'video2_label': '🎬 2ª Opção: 3B1B Gradiente Descendente'},
          {'title': 'Matriz Jacobiana e Matriz Hessiana (curvatura da loss)',
           'video_url': 'https://www.youtube.com/watch?v=VmfTXVG9S0U',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=matriz+jacobiana+hessiana',
           'doc_url': 'https://pt.khanacademy.org/math/multivariable-calculus/multivariable-derivatives/jacobian/v/computing-a-jacobian-matrix',
           'doc_label': '📘 Aula Visual PT-BR: Jacobiana & Hessiana',
           'pt_guide': {'intuicao': '• <b>Matriz Jacobiana ($J$):</b> Guarda todas as derivadas de <b>1ª ordem</b> '
                                    'quando uma camada tem múltiplas entradas e múltiplas saídas.\n'
                                    '• <b>Matriz Hessiana ($H$):</b> Guarda as derivadas de <b>2ª ordem</b> (a '
                                    'derivada da derivada). Ela mede a <b>curvatura</b> do terreno de erro: diz se '
                                    'estamos num vale fundo (mínimo local), num topo de morro (máximo) ou num ponto de '
                                    'sela!',
                        'formula': '$$J_{ij} = \\frac{\\partial f_i}{\\partial x_j} \\quad | \\quad H_{ij} = '
                                   '\\frac{\\partial^2 L}{\\partial w_i \\partial w_j}$$',
                        'exemplo': 'Se a derivada primeira diz a inclinação da pista, a 2ª derivada (Hessiana) diz se '
                                   'a pista está curvando para cima (como uma tigela $\\cup$, ótimo para convergir!) '
                                   'ou para baixo ($\\cap$).',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  '# Para f(x, y) = x^2 + 3*y^2, a Hessiana é constante:\n'
                                  'H = np.array([[2.0, 0.0],\n'
                                  '              [0.0, 6.0]])\n'
                                  "print('Autovalores da Hessiana (>0 indica vale convexo):', np.linalg.eigvals(H))"},
           'video2_url': 'https://www.youtube.com/watch?v=Ilg3gGewQ5U',
           'video2_label': '🎬 2ª Opção: 3B1B O que é Backprop?'},
          {'title': 'Algoritmo de Descida do Gradiente (Vanilla Gradient Descent)',
           'video_url': 'https://www.youtube.com/watch?v=kY6Vq0NfY_8',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=gradiente+calculo+multivariavel',
           'doc_url': 'https://pt.khanacademy.org/math/multivariable-calculus/multivariable-derivatives/gradient-and-directional-derivatives/v/gradient',
           'doc_label': '📘 Aula Visual PT-BR: Gradiente Descendente',
           'pt_guide': {'intuicao': 'Imagine estar no topo de uma montanha no meio de uma neblina densa e querer '
                                    'chegar ao fundo do vale. Você sente a inclinação do chão sob seus pés (o '
                                    'Gradiente $\\nabla L$) e dá um passo na direção que desce ($-\\nabla L$). Repita '
                                    'isso milhares de vezes e sua rede neural aprenderá os pesos perfeitos! Esse é o '
                                    '<b>Gradiente Descendente</b>.',
                        'formula': '$$w_{\\text{novo}} = w_{\\text{atual}} - \\alpha \\cdot \\nabla '
                                   'L(w_{\\text{atual}})$$\n'
                                   '• $w$: Peso do modelo\n'
                                   '• $\\alpha$ (alpha): Taxa de aprendizado (*Learning Rate* — tamanho do passo)\n'
                                   '• $\\nabla L$: Gradiente do erro',
                        'exemplo': 'Queremos minimizar $L(w) = (w - 5)^2$, cujo mínimo é $w = 5$.\n'
                                   'Começando em $w = 1$ com taxa $\\alpha = 0.2$:\n'
                                   "• Derivada: $L'(1) = 2(1 - 5) = -8$\n"
                                   '• Atualização: $w_{\\text{novo}} = 1 - 0.2 \\times (-8) = 1 + 1.6 = 2.6$ (Já '
                                   'chegou mais perto do $5$!).',
                        'codigo': 'w = 1.0\n'
                                  'lr = 0.2 # Taxa de aprendizado (learning rate)\n'
                                  '\n'
                                  'for passo in range(10):\n'
                                  '    grad = 2 * (w - 5) # Derivada de (w - 5)^2\n'
                                  '    w = w - lr * grad\n'
                                  "print(f'Peso aprendido após 10 passos: {w:.4f} (Alvo ideal: 5.0)')"},
           'video2_url': 'https://www.youtube.com/watch?v=tIeHLnjs5U8',
           'video2_label': '🎬 2ª Opção: 3B1B Backprop Calculus'},
          {'title': 'Otimizadores modernos: Momentum, RMSprop e Adam',
           'video_url': 'https://www.youtube.com/watch?v=gvgv7lNcBfs',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=regra+da+cadeia+multivariavel+gradiente',
           'doc_url': 'https://pt.khanacademy.org/math/multivariable-calculus/multivariable-derivatives/multivariable-chain-rule/v/multivariable-chain-rule',
           'doc_label': '📘 Aula Visual PT-BR: Otimizador Adam',
           'pt_guide': {'intuicao': 'O Gradiente Descendente puro é lento e pode ficar ziguezagueando em barrancos. '
                                    'Por isso criaram otimizadores inteligentes:\n'
                                    '• <b>Momentum:</b> Simula uma bola pesada ganhando embalo (inércia) ladeira '
                                    'abaixo.\n'
                                    '• <b>RMSprop:</b> Adapta o tamanho do passo para cada peso individualmente.\n'
                                    '• <b>Adam (Adaptive Moment Estimation):</b> Junta o embalo do Momentum + o passo '
                                    'adaptativo do RMSprop! É o otimizador padrão de 99% dos modelos modernos.',
                        'formula': '$$m_t = \\beta_1 m_{t-1} + (1 - \\beta_1) g_t \\quad (\\text{Média / Momentum})$$\n'
                                   '$$v_t = \\beta_2 v_{t-1} + (1 - \\beta_2) g_t^2 \\quad (\\text{Velocidade '
                                   'adaptativa})$$\n'
                                   '$$w_{t+1} = w_t - \\alpha \\frac{\\hat{m}_t}{\\sqrt{\\hat{v}_t} + \\epsilon}$$',
                        'exemplo': 'Se um peso recebe gradientes gigantescos toda hora, o Adam diminui o passo dele '
                                   'para não explodir; se outro peso recebe gradientes tímidos, o Adam aumenta o passo '
                                   'dele para acelerar o aprendizado!',
                        'codigo': '# Exemplo conceitual de Momentum em Python\n'
                                  'w, v_inercia = 1.0, 0.0\n'
                                  'lr, beta = 0.1, 0.9\n'
                                  'for _ in range(15):\n'
                                  '    grad = 2 * (w - 5)\n'
                                  '    v_inercia = beta * v_inercia + (1 - beta) * grad\n'
                                  '    w = w - lr * v_inercia\n'
                                  "print(f'Peso otimizado com Momentum: {w:.4f}')"},
           'video2_url': 'https://www.youtube.com/watch?v=vMh0zPT0tLI',
           'video2_label': '🎬 2ª Opção: StatQuest SGD'},
          {'title': 'Taxa de aprendizado (Learning Rate), convergência e pontos de sela',
           'video_url': 'https://www.youtube.com/watch?v=4rCTNjeTUwM',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=pontos+de+sela+maximos+e+minimos',
           'doc_url': 'https://pt.khanacademy.org/math/multivariable-calculus/applications-of-multivariable-derivatives/optimizing-multivariable-functions/a/maximums-minimums-and-saddle-points',
           'doc_label': '📘 Aula Visual PT-BR: Learning Rate',
           'pt_guide': {'intuicao': 'A <b>Taxa de Aprendizado ($\\alpha$ ou Learning Rate)</b> é o hiperparâmetro mais '
                                    'crítico do treinamento:\n'
                                    '• <b>Muito pequena (ex.: $10^{-7}$):</b> O treinamento demora uma eternidade e '
                                    'pode parar em buracos rasos.\n'
                                    '• <b>Muito grande (ex.: $10.0$):</b> O passo é tão largo que pula de um lado para '
                                    'o outro do vale e o erro explode (`NaN`)!\n'
                                    '• <b>Ponto de Sela:</b> Um platô onde uma direção desce e outra sobe (como uma '
                                    'sela de cavalo), onde o gradiente zera sem ser o fundo do vale.',
                        'formula': '$$\\text{Cosine Annealing / Warmup: } \\alpha_t = \\alpha_{\\min} + '
                                   '\\frac{1}{2}(\\alpha_{\\max} - \\alpha_{\\min})\\left(1 + '
                                   '\\cos\\left(\\frac{t}{T}\\pi\\right)\\right)$$',
                        'exemplo': 'No treinamento de LLMs (como GPT e Llama), usamos um <b>Learning Rate '
                                   'Scheduler</b>: começamos aquecendo devagar (*Warmup*) até $3\\times 10^{-4}$ e '
                                   'depois vamos reduzindo suavemente para refinar os pesos finais.',
                        'codigo': '# Comparando Learning Rate ideal vs Learning Rate alto demais\n'
                                  'for lr in [0.1, 1.05]:\n'
                                  '    w = 0.0\n'
                                  '    for _ in range(5):\n'
                                  '        w = w - lr * (2 * (w - 3))\n'
                                  "    print(f'LR={lr} -> w final = {w:.2f} (Alvo: 3.00)')"},
           'video2_url': 'https://www.youtube.com/watch?v=sDv4f4s2SB8',
           'video2_label': '🎬 2ª Opção: StatQuest Learning Rate'}]]]},
 {'t': 'Módulo 3 · Probabilidade & Estatística para IA',
  'd': '3 a 4 semanas',
  'tip': '💡 <b>Como Estudar sem Travar:</b> Comece clicando no botão vermelho <b>▶ Khan Academy PT-BR</b> (1ª Opção) '
         'para assistir à explicação calma, passo a passo e em português no quadro. Depois, leia os 4 passos da <b>📘 '
         'Aula Visual PT-BR</b> logo abaixo do vídeo. Quando quiser ver a intuição geométrica animada, alterne para a '
         '<b>🎬 2ª Opção (3B1B / StatQuest)</b>!',
  'p': 'Construir um classificador Naive Bayes em Python para detectar mensagens de spam usando o Teorema de Bayes.',
  'r': '1ª Opção: Canal Oficial Khan Academy Português (@khanacademyportugues) · 2ª Opção: 3Blue1Brown & StatQuest · '
       'Aula Visual & Apostila Interativa em Português',
  'g': [['Estatística Descritiva & Probabilidade',
         [{'title': 'Variáveis aleatórias discretas e contínuas',
           'video_url': 'https://www.youtube.com/watch?v=IYdiKeQ9xEI',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=variaveis+aleatorias+discretas+e+continuas',
           'doc_url': 'https://pt.khanacademy.org/math/statistics-probability/random-variables-stats-library/random-variables-discrete/v/random-variables',
           'doc_label': '📘 Aula Visual PT-BR: Var. Aleatórias',
           'pt_guide': {'intuicao': 'Uma <b>Variável Aleatória ($X$)</b> traduz eventos incertos do mundo real em '
                                    'números:\n'
                                    '• <b>Discreta:</b> Assume valores contáveis/inteiros (ex.: número de cliques num '
                                    'anúncio, qual palavra do vocabulário o LLM vai escolher). Usa Função Massa de '
                                    'Probabilidade ($P(X=x)$).\n'
                                    '• <b>Contínua:</b> Assume qualquer valor com casas decimais num intervalo (ex.: '
                                    'temperatura amanhã, preço de uma ação). Usa Função Densidade de Probabilidade '
                                    '($f(x)$).',
                        'formula': '$$\\text{Discreta: } \\sum_{x} P(X = x) = 1 \\quad | \\quad \\text{Contínua: } '
                                   '\\int_{-\\infty}^{+\\infty} f(x)\\,dx = 1$$',
                        'exemplo': 'Em IA: prever <b>Classificação</b> (Gato, Cachorro ou Pássaro) modela uma variável '
                                   '<b>discreta</b>; prever <b>Regressão</b> (valor de venda de uma casa em R$) modela '
                                   'uma variável <b>contínua</b>.',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  '# Variável discreta: sorteando próximo token com probabilidades [0.7, 0.2, 0.1]\n'
                                  "tokens = ['Inteligência', 'Artificial', 'Futuro']\n"
                                  'probs = [0.7, 0.2, 0.1]\n'
                                  'escolha = np.random.choice(tokens, p=probs)\n'
                                  "print('Token amostrado:', escolha)"},
           'video2_url': 'https://www.youtube.com/watch?v=HZGCoVF3YvM',
           'video2_label': '🎬 2ª Opção: 3B1B Probabilidade'},
          {'title': 'Média, mediana, variância e desvio padrão',
           'video_url': 'https://www.youtube.com/watch?v=UdrtnBGSeSw',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=media+variancia+e+desvio+padrao',
           'doc_url': 'https://pt.khanacademy.org/math/statistics-probability/summarizing-quantitative-data/variance-standard-deviation-population/v/range-variance-and-standard-deviation-as-measures-of-dispersion',
           'doc_label': '📘 Aula Visual PT-BR: Variância & Desvio',
           'pt_guide': {'intuicao': '• <b>Média ($\\mu$):</b> O centro de gravidade dos dados (sensível a valores '
                                    'extremos/outliers).\n'
                                    '• <b>Mediana:</b> O valor exatamente no meio quando ordenamos os dados (robusta '
                                    'contra outliers!).\n'
                                    '• <b>Variância ($\\sigma^2$) e Desvio Padrão ($\\sigma$):</b> Medem o quanto os '
                                    'dados estão espalhados longe da média. Toda camada de <b>BatchNorm / '
                                    'LayerNorm</b> em redes neurais usa média e desvio padrão para estabilizar os '
                                    'neurônios!',
                        'formula': '$$\\mu = \\frac{1}{n}\\sum_{i=1}^n x_i \\quad | \\quad \\sigma^2 = '
                                   '\\frac{1}{n}\\sum_{i=1}^n (x_i - \\mu)^2 \\quad | \\quad \\sigma = '
                                   '\\sqrt{\\sigma^2}$$',
                        'exemplo': 'Salários em mil reais: `[3, 4, 5, 4, 100]`.\n'
                                   '• A <b>Média</b> é $23.2$ mil (distorcida pelo $100$).\n'
                                   '• A <b>Mediana</b> é $4$ mil (retrata muito melhor o grupo!).',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'dados = np.array([10, 12, 15, 18, 20])\n'
                                  "print('Média:', np.mean(dados))\n"
                                  "print('Mediana:', np.median(dados))\n"
                                  "print('Desvio Padrão:', round(np.std(dados), 2))"},
           'video2_url': 'https://www.youtube.com/watch?v=SzZ6G436HKM',
           'video2_label': '🎬 2ª Opção: StatQuest Variância'},
          {'title': 'Esperança matemática, covariância e correlação',
           'video_url': 'https://www.youtube.com/watch?v=VMVwGJiD2EA',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=valor+esperado+esperanca+matematica',
           'doc_url': 'https://pt.khanacademy.org/math/statistics-probability/random-variables-stats-library/random-variables-discrete/v/expected-value-of-a-discrete-random-variable',
           'doc_label': '📘 Aula Visual PT-BR: Correlação',
           'pt_guide': {'intuicao': '• <b>Esperança Matemática ($E[X]$):</b> É a média ponderada pelas probabilidades '
                                    '(o retorno médio esperado no longo prazo).\n'
                                    '• <b>Covariância e Correlação ($r$ de Pearson):</b> Medem se duas variáveis '
                                    'caminham juntas! A correlação sempre vai de $-1$ (quando uma sobe, a outra cai) '
                                    'até $+1$ (sobem juntas), passando por $0$ (sem relação linear).',
                        'formula': '$$E[X] = \\sum x_i P(x_i) \\quad | \\quad r_{xy} = \\frac{\\text{Cov}(X, '
                                   'Y)}{\\sigma_X \\cdot \\sigma_Y} \\in [-1, +1]$$',
                        'exemplo': "Se 'Horas de Estudo' e 'Nota na Prova' têm correlação $r = +0.88$, existe forte "
                                   'relação positiva! Lembrete de ouro em Ciência de Dados: <b>Correlação não implica '
                                   'causalidade</b>.',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'horas_estudo = np.array([1, 2, 4, 6, 8])\n'
                                  'notas = np.array([40, 52, 70, 85, 96])\n'
                                  '\n'
                                  'corr = np.corrcoef(horas_estudo, notas)[0, 1]\n'
                                  "print(f'Correlação de Pearson: {corr:.4f}') # ~0.996"},
           'video2_url': 'https://www.youtube.com/watch?v=qtaqvPAeEJY',
           'video2_label': '🎬 2ª Opção: StatQuest Covariância'},
          {'title': 'Probabilidade condicional e Teorema de Bayes',
           'video_url': 'https://www.youtube.com/watch?v=885a44XKDqM',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=probabilidade+condicional+bayes',
           'doc_url': 'https://pt.khanacademy.org/math/statistics-probability/probability-library/conditional-probability-independence/v/calculating-conditional-probability',
           'doc_label': '📘 Aula Visual PT-BR: Teorema de Bayes',
           'pt_guide': {'intuicao': 'A <b>Probabilidade Condicional $P(A|B)$</b> é a chance de $A$ acontecer '
                                    '<i>sabendo que $B$ já aconteceu</i>. O <b>Teorema de Bayes</b> é a fórmula '
                                    'matemática para <b>atualizar nossas crenças diante de novas evidências</b>! Você '
                                    'começa com uma estimativa inicial (*Priori*), observa os dados reais '
                                    '(*Verossimilhança*) e calcula a probabilidade atualizada (*Posteriori*).',
                        'formula': '$$P(A \\mid B) = \\frac{P(B \\mid A) \\cdot P(A)}{P(B)}$$\n'
                                   '• $P(A)$: Probabilidade a priori (antes da evidência)\n'
                                   '• $P(B|A)$: Verossimilhança (chance da evidência aparecer se $A$ for verdade)\n'
                                   '• $P(A|B)$: Probabilidade a posteriori (atualizada!)',
                        'exemplo': "Filtro de Spam: $20\\%$ dos e-mails são Spam ($P(S)=0.2$). A palavra 'Prêmio' "
                                   'aparece em $80\\%$ dos Spams ($P(P|S)=0.8$), mas só em $5\\%$ dos e-mails '
                                   'normais.\n'
                                   "Se chegou um e-mail com 'Prêmio', a chance de ser Spam salta de $20\\%$ para:\n"
                                   '$$P(S|P) = \\frac{0.8 \\times 0.2}{(0.8 \\times 0.2) + (0.05 \\times 0.8)} = '
                                   '\\frac{0.16}{0.20} = 80\\%!$$',
                        'codigo': 'p_spam = 0.20\n'
                                  'p_normal = 0.80\n'
                                  'p_premio_dado_spam = 0.80\n'
                                  'p_premio_dado_normal = 0.05\n'
                                  '\n'
                                  'p_premio_total = (p_premio_dado_spam * p_spam) + (p_premio_dado_normal * p_normal)\n'
                                  'p_spam_dado_premio = (p_premio_dado_spam * p_spam) / p_premio_total\n'
                                  "print(f'Chance de ser Spam dado a palavra Prêmio: {p_spam_dado_premio*100:.1f}%') # "
                                  '80.0%'},
           'video2_url': 'https://www.youtube.com/watch?v=HZGCoVF3YvM',
           'video2_label': '🎬 2ª Opção: 3B1B Teorema de Bayes'}]],
        ['Distribuições & Inferência',
         [{'title': 'Distribuição Normal (Gaussiana) e probabilidade vs verossimilhança',
           'video_url': 'https://www.youtube.com/watch?v=hgtMWR3TFnY',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=distribuicao+normal+gaussiana',
           'doc_url': 'https://pt.khanacademy.org/math/statistics-probability/modeling-distributions-of-data/normal-distributions-library/v/introduction-to-the-normal-distribution',
           'doc_label': '📘 Aula Visual PT-BR: Curva Normal',
           'pt_guide': {'intuicao': 'A <b>Distribuição Normal (Curva em Sino de Gauss)</b> aparece em toda a natureza '
                                    'e na inicialização de pesos de redes neurais! Nela, a maioria dos valores se '
                                    'concentra perto da média $\\mu$, e valores extremos são raros:\n'
                                    '• <b>68%</b> dos dados ficam a até $1$ desvio padrão ($\\mu \\pm 1\\sigma$).\n'
                                    '• <b>95%</b> ficam a até $2$ desvios padrões ($\\mu \\pm 2\\sigma$).',
                        'formula': '$$f(x) = \\frac{1}{\\sigma \\sqrt{2\\pi}} e^{-\\frac{1}{2}\\left(\\frac{x - '
                                   '\\mu}{\\sigma}\\right)^2}$$',
                        'exemplo': '• <b>Probabilidade:</b> Conhecemos a curva ($\\mu, \\sigma$) e perguntamos a '
                                   'chance de sair um dado $x$.\n'
                                   '• <b>Verossimilhança (Likelihood):</b> Já temos os dados observados e perguntamos '
                                   'quais parâmetros ($\\mu, \\sigma$) melhor explicam esses dados!',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  '# Inicializando pesos de uma camada neural com Distribuição Normal Padrão (média 0, '
                                  'desvio 1)\n'
                                  'pesos = np.random.normal(loc=0.0, scale=1.0, size=1000)\n'
                                  "print(f'Média gerada: {pesos.mean():.2f} | Desvio: {pesos.std():.2f}')"},
           'video2_url': 'https://www.youtube.com/watch?v=rzFX5NWojp0',
           'video2_label': '🎬 2ª Opção: StatQuest Dist. Normal'},
          {'title': 'Teorema do Limite Central e amostragem',
           'video_url': 'https://www.youtube.com/watch?v=JNm3M9cqWyc',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=teorema+do+limite+central',
           'doc_url': 'https://pt.khanacademy.org/math/statistics-probability/sampling-distributions-library/sample-means/v/central-limit-theorem',
           'doc_label': '📘 Aula Visual PT-BR: Limite Central',
           'pt_guide': {'intuicao': 'O <b>Teorema do Limite Central (TLC)</b> é quase mágica matemática: mesmo que os '
                                    'seus dados originais tenham um formato totalmente torto ou estranho, se você '
                                    'tirar várias amostras e calcular a <b>média de cada amostra</b>, a distribuição '
                                    'dessas médias sempre formará uma <b>Curva Normal perfeita</b>! É por isso que '
                                    'treinar redes neurais em pequenos lotes (<b>Mini-Batch SGD</b> de 32 ou 64 '
                                    'exemplos) funciona tão bem!',
                        'formula': '$$\\bar{X} \\sim \\mathcal{N}\\left(\\mu, \\frac{\\sigma^2}{n}\\right) \\implies '
                                   '\\text{Erro Padrão} = \\frac{\\sigma}{\\sqrt{n}}$$\n'
                                   'Quanto maior o tamanho da amostra $n$, menor a incerteza da média!',
                        'exemplo': 'Jogar 1 dado tem distribuição reta (uniforme de 1 a 6). Mas se você jogar 30 dados '
                                   'e tirar a média deles repetidas vezes, o gráfico das médias forma um sino '
                                   'Gaussiano centrado em $3.5$!',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  '# Tirando 1000 médias de 30 lançamentos de dados (1 a 6)\n'
                                  'medias = [np.random.randint(1, 7, size=30).mean() for _ in range(1000)]\n'
                                  "print(f'Média global das amostras: {np.mean(medias):.2f} (Teórico: 3.50)')"},
           'video2_url': 'https://www.youtube.com/watch?v=JNm3M9IJihQ',
           'video2_label': '🎬 2ª Opção: StatQuest Limite Central'},
          {'title': 'Intervalos de confiança e teste de hipóteses (noção)',
           'video_url': 'https://www.youtube.com/watch?v=bekNKJoxYbQ',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=intervalo+de+confianca+estatistica',
           'doc_url': 'https://pt.khanacademy.org/math/statistics-probability/confidence-intervals-one-sample/introduction-to-confidence-intervals/v/confidence-intervals-and-margin-of-error',
           'doc_label': '📘 Aula Visual PT-BR: Confiança & p-valor',
           'pt_guide': {'intuicao': 'Quando você cria um novo modelo de IA e ele acerta $85\\%$ no teste contra '
                                    '$83\\%$ do modelo antigo, será que ele é realmente melhor ou foi pura sorte da '
                                    'amostra? O <b>Intervalo de Confiança</b> dá a margem de erro (ex.: $85\\% \\pm '
                                    '1.2\\%$), e o <b>Teste de Hipóteses ($p$-valor)</b> mede a probabilidade de essa '
                                    'diferença ter ocorrido por puro acaso!',
                        'formula': '$$IC_{95\\%} = \\bar{x} \\pm 1.96 \\cdot \\frac{s}{\\sqrt{n}}$$\n'
                                   'Regra prática: Se o <b>$p$-valor $< 0.05$ (5%)</b>, rejeitamos a hipótese de sorte '
                                   'e confirmamos que a melhoria é estatisticamente significativa!',
                        'exemplo': 'Em um Teste A/B de recomendação com $n=100$ usuários, média $\\bar{x}=50$ e desvio '
                                   '$s=10$:\n'
                                   'Margem de erro $= 1.96 \\times \\frac{10}{\\sqrt{100}} = 1.96$. Intervalo de 95%: '
                                   '$[48.04, 51.96]$.',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'media, desvio, n = 85.0, 6.0, 100\n'
                                  'margem_95 = 1.96 * (desvio / np.sqrt(n))\n'
                                  "print(f'Acurácia com 95% de confiança: {media:.1f}% ± {margem_95:.2f}%')"},
           'video2_url': 'https://www.youtube.com/watch?v=TqOeMYtOc1w',
           'video2_label': '🎬 2ª Opção: StatQuest Confiança'},
          {'title': 'Máxima Verossimilhança (Maximum Likelihood Estimation - MLE)',
           'video_url': 'https://www.youtube.com/watch?v=BFu8smEp-Cc',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=densidade+de+probabilidade+verossimilhanca',
           'doc_url': 'https://pt.khanacademy.org/math/statistics-probability/random-variables-stats-library/random-variables-continuous/v/probability-density-functions',
           'doc_label': '📘 Aula Visual PT-BR: MLE',
           'pt_guide': {'intuicao': '<b>Máxima Verossimilhança (MLE)</b> é o princípio filosófico por trás do '
                                    "treinamento de quase todos os modelos de Machine Learning e LLMs: <i>'Quais são "
                                    'os pesos $\\theta$ do modelo que tornam os dados reais que observamos no '
                                    "treinamento o mais prováveis possível?'</i>. Minimizar a função de perda "
                                    '<b>Cross-Entropy</b> é matematicamente idêntico a maximizar a '
                                    'log-verossimilhança!',
                        'formula': '$$\\hat{\\theta}_{\\text{MLE}} = \\arg\\max_{\\theta} \\sum_{i=1}^n \\log P(y_i '
                                   '\\mid x_i; \\theta)$$\n'
                                   'Usamos a soma dos logaritmos ($\\log$) porque multiplicar milhares de '
                                   'probabilidades pequenas ($0.01 \\times 0.01...$) zeraria a memória do computador '
                                   '(*underflow*)!',
                        'exemplo': 'Se você jogou uma moeda 10 vezes e deu 7 Caras, qual o valor de $p$ (chance de '
                                   'Cara) que maximiza a verossimilhança desse resultado? Pela derivada da função '
                                   'log-verossimilhança, encontramos exatamente $\\hat{p} = 7/10 = 0.70$!',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  '# Testando qual parâmetro p maximiza a log-verossimilhança de 7 caras em 10 '
                                  'jogadas\n'
                                  'ps = np.linspace(0.1, 0.9, 9)\n'
                                  'log_lik = 7 * np.log(ps) + 3 * np.log(1 - ps)\n'
                                  'melhor_p = ps[np.argmax(log_lik)]\n'
                                  "print('Estimativa de Máxima Verossimilhança (p):', round(melhor_p, 2)) # 0.7"},
           'video2_url': 'https://www.youtube.com/watch?v=XepXtl9YKwc',
           'video2_label': '🎬 2ª Opção: StatQuest MLE'},
          {'title': 'Trade-off Viés vs. Variância (Bias-Variance Dilemma)',
           'video_url': 'https://www.youtube.com/watch?v=X-Bkr_UHuHI',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=regressao+linear+ajuste+residuos',
           'doc_url': 'https://pt.khanacademy.org/math/statistics-probability/describing-relationships-quantitative-data/introduction-to-trend-lines/v/fitting-a-line-to-data',
           'doc_label': '📘 Aula Visual PT-BR: Viés vs Variância',
           'pt_guide': {'intuicao': 'Todo erro de um modelo de IA vem do equilíbrio entre dois extremos:\n'
                                    '• <b>Alto Viés (Underfitting):</b> O modelo é simples demais (ex.: tentar ajustar '
                                    'uma linha reta num gráfico em curva). Ele erra tanto no treino quanto no teste.\n'
                                    '• <b>Alta Variância (Overfitting):</b> O modelo decorou até o ruído dos dados de '
                                    'treino! Ele tira nota 100% no treino, mas falha miseravelmente em dados novos.',
                        'formula': '$$\\text{Erro Total} = \\text{Viés}^2 + \\text{Variância} + \\text{Ruído '
                                   'Irredutível}$$',
                        'exemplo': '• Modelo A: Treino = 65% | Teste = 64% $\\rightarrow$ Sofre de <b>Alto Viés '
                                   '(Underfitting)</b>.\n'
                                   '• Modelo B: Treino = 99% | Teste = 71% $\\rightarrow$ Sofre de <b>Alta Variância '
                                   '(Overfitting)</b>.\n'
                                   '• Modelo C: Treino = 92% | Teste = 90% $\\rightarrow$ <b>Equilíbrio Ideal '
                                   '(Generalização)</b>!',
                        'codigo': '# Diagnóstico automático de Viés vs Variância\n'
                                  'def diagnosticar_modelo(acc_treino, acc_teste):\n'
                                  '    if acc_treino < 0.75:\n'
                                  "        return 'Alto Viés (Underfitting): aumente a capacidade do modelo!'\n"
                                  '    elif (acc_treino - acc_teste) > 0.10:\n'
                                  "        return 'Alta Variância (Overfitting): use Regularização/Dropout e mais "
                                  "dados!'\n"
                                  "    return 'Equilíbrio saudável (Boa generalização)!'\n"
                                  '\n'
                                  'print(diagnosticar_modelo(0.99, 0.72))'},
           'video2_url': 'https://www.youtube.com/watch?v=EuBBz3bI-aA',
           'video2_label': '🎬 2ª Opção: StatQuest Viés vs Variância'}]]]},
 {'t': 'Módulo 4 · Funções Matemáticas, Geometria & Teoria da Informação',
  'd': '2 semanas',
  'tip': '💡 <b>Como Estudar sem Travar:</b> Comece clicando no botão vermelho <b>▶ Khan Academy PT-BR</b> (1ª Opção) '
         'para assistir à explicação calma, passo a passo e em português no quadro. Depois, leia os 4 passos da <b>📘 '
         'Aula Visual PT-BR</b> logo abaixo do vídeo. Quando quiser ver a intuição geométrica animada, alterne para a '
         '<b>🎬 2ª Opção (3B1B / StatQuest)</b>!',
  'p': 'Implementar em Python as funções Softmax e Cross-Entropy Loss do zero e testar com previsões de um modelo.',
  'r': '1ª Opção: Canal Oficial Khan Academy Português (@khanacademyportugues) · 2ª Opção: 3Blue1Brown & StatQuest · '
       'Aula Visual & Apostila Interativa em Português',
  'g': [['Álgebra e Geometria Analítica',
         [{'title': 'Equações, inequações e gráficos de funções aplicadas',
           'video_url': 'https://www.youtube.com/watch?v=h4Kf1w4LBVQ',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=equacoes+lineares+e+graficos+funcoes',
           'doc_url': 'https://pt.khanacademy.org/math/algebra/x2f8bb11595b61c86:forms-of-linear-equations/x2f8bb11595b61c86:intro-to-slope-intercept-form/v/slope-intercept-form',
           'doc_label': '📘 Aula Visual PT-BR: Funções & Reta',
           'pt_guide': {'intuicao': 'A equação da reta $y = wx + b$ é a semente de toda a Inteligência Artificial! '
                                    'Nela, $w$ (*weight* / peso) é a <b>inclinação da reta</b> (o quanto $y$ muda para '
                                    'cada unidade de $x$), e $b$ (*bias* / viés) é o ponto onde a reta corta o eixo '
                                    'vertical (o valor base quando $x=0$). Uma inequação como $w_1 x_1 + w_2 x_2 + b > '
                                    '0$ divide o plano em duas regiões (classificador linear!).',
                        'formula': '$$f(x) = w \\cdot x + b \\quad | \\quad \\text{Fronteira de decisão: } \\vec{w} '
                                   '\\cdot \\vec{x} + b = 0$$',
                        'exemplo': 'Previsão de preço de imóvel: $\\text{Preço} = 8 \\cdot (\\text{m}^2) + 50$.\n'
                                   '• O peso $w = 8$ diz que cada metro quadrado adiciona R$ 8 mil.\n'
                                   '• O viés $b = 50$ é o valor base do terreno (R$ 50 mil).',
                        'codigo': '# Um neurônio linear simples\n'
                                  'def neuronio_linear(x, w=8.0, b=50.0):\n'
                                  '    return w * x + b\n'
                                  '\n'
                                  "print('Preço estimado para 70 m²:', neuronio_linear(70), 'mil reais') # 610.0"},
           'video2_url': 'https://www.youtube.com/watch?v=WUvTyaaNkzM',
           'video2_label': '🎬 2ª Opção: 3B1B Gráficos & Funções'},
          {'title': 'Exponenciais e logaritmos na modelagem de IA',
           'video_url': 'https://www.youtube.com/watch?v=LV81nqJWwdk',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=introducao+aos+logaritmos+exponenciais',
           'doc_url': 'https://pt.khanacademy.org/math/algebra2/x2ec2f6f830c9fb89:logs/x2ec2f6f830c9fb89:log-intro/v/logarithms',
           'doc_label': '📘 Aula Visual PT-BR: Exp & Log',
           'pt_guide': {'intuicao': 'A função exponencial ($e^x$, onde $e \\approx 2.718$) transforma qualquer número '
                                    '(mesmo negativo!) em um número estritamente <b>positivo</b> e amplifica os '
                                    'maiores valores (base do Softmax!). Já o <b>Logaritmo Natural ($\\ln(x)$)</b> é a '
                                    'operação inversa: ele transforma multiplicações difíceis em somas simples '
                                    '($\\ln(a \\cdot b) = \\ln a + \\ln b$) e penaliza severamente previsões erradas '
                                    'perto de zero!',
                        'formula': '$$e^0 = 1 \\quad | \\quad \\ln(e^x) = x \\quad | \\quad \\ln(a \\cdot b) = \\ln(a) '
                                   '+ \\ln(b)$$',
                        'exemplo': 'Na função de perda <i>Log-Loss</i> ($-\\ln(p)$):\n'
                                   '• Se o modelo prevê $p = 0.99$ para a classe certa, o erro é $-\\ln(0.99) \\approx '
                                   '0.01$ (quase zero!).\n'
                                   '• Se o modelo prevê $p = 0.01$ para a classe certa, o erro explode para '
                                   '$-\\ln(0.01) \\approx 4.60$!',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'for p in [0.99, 0.50, 0.01]:\n'
                                  '    penalidade = -np.log(p)\n'
                                  "    print(f'Probabilidade prevista={p:.2f} -> Penalidade "
                                  "Log-Loss={penalidade:.3f}')"},
           'video2_url': 'https://www.youtube.com/watch?v=m2MIpDrF7Es',
           'video2_label': '🎬 2ª Opção: 3B1B Número de Euler e'},
          {'title': 'Somatório, produtório e notação matemática em papers',
           'video_url': 'https://www.youtube.com/watch?v=kCbfPGFQlOY',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=notacao+de+somatorio+sigma',
           'doc_url': 'https://pt.khanacademy.org/math/ap-calculus-ab/ab-integration-new/ab-6-3/v/sigma-notation-for-sums',
           'doc_label': '📘 Aula Visual PT-BR: Notação Sigma',
           'pt_guide': {'intuicao': 'Sempre que você vir a letra grega <b>Sigma maiúscula ($\\sum$)</b> num artigo de '
                                    'IA, traduza mentalmente na hora para um <b>laço `for` somando elementos '
                                    '(`sum()`)</b> em Python! E quando vir o <b>Pi maiúsculo ($\\prod$)</b>, traduza '
                                    'para um laço multiplicando elementos (`np.prod()`). Só isso destrava 90% da '
                                    'leitura de papers!',
                        'formula': '$$\\sum_{i=1}^{n} x_i = x_1 + x_2 + \\dots + x_n \\quad | \\quad \\prod_{i=1}^{n} '
                                   'x_i = x_1 \\times x_2 \\times \\dots \\times x_n$$',
                        'exemplo': 'Calcular $\\sum_{i=1}^{4} i^2$:\n'
                                   'Para $i=1, 2, 3, 4$, elevamos ao quadrado e somamos:\n'
                                   '$$1^2 + 2^2 + 3^2 + 4^2 = 1 + 4 + 9 + 16 = 30$$',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'x = np.array([1, 2, 3, 4])\n'
                                  'somatorio = np.sum(x ** 2)   # Sigma (Σ)\n'
                                  'produtorio = np.prod(x)      # Pi (Π)\n'
                                  "print(f'Somatório Σ(x²): {somatorio} | Produtório Π(x): {produtorio}')"},
           'video2_url': 'https://www.youtube.com/watch?v=TgKwz5hkrvw',
           'video2_label': '🎬 2ª Opção: 3B1B Notação Matemática'},
          {'title': 'Geometria analítica e distância Euclidiana vs Manhattan',
           'video_url': 'https://www.youtube.com/watch?v=WM-_zN5priE',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=formula+da+distancia+entre+dois+pontos',
           'doc_url': 'https://pt.khanacademy.org/math/geometry/hs-geo-analytic-geometry/hs-geo-distance-and-midpoints/v/distance-formula',
           'doc_label': '📘 Aula Visual PT-BR: Distâncias',
           'pt_guide': {'intuicao': 'Algoritmos como <b>KNN (Vizinhos Mais Próximos)</b>, <b>K-Means '
                                    '(Clusterização)</b> e bancos vetoriais agrupam pontos medindo a distância entre '
                                    'eles:\n'
                                    '• <b>Distância Euclidiana (L2):</b> A régua em linha reta (voo de pássaro) entre '
                                    'dois pontos.\n'
                                    '• <b>Distância de Manhattan (L1):</b> A soma das diferenças absolutas nos eixos '
                                    '(caminho de táxi em ruas quadriculadas).',
                        'formula': '$$d_{\\text{Euclidiana}}(\\vec{p}, \\vec{q}) = \\sqrt{\\sum_{i=1}^n (p_i - q_i)^2} '
                                   '\\quad | \\quad d_{\\text{Manhattan}}(\\vec{p}, \\vec{q}) = \\sum_{i=1}^n |p_i - '
                                   'q_i|$$',
                        'exemplo': 'Entre os pontos $P = (1, 2)$ e $Q = (4, 6)$:\n'
                                   '• Diferenças nos eixos: $\\Delta x = |1-4| = 3$ e $\\Delta y = |2-6| = 4$.\n'
                                   '• <b>Manhattan:</b> $3 + 4 = 7$.\n'
                                   '• <b>Euclidiana:</b> $\\sqrt{3^2 + 4^2} = \\sqrt{25} = 5$.',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'p = np.array([1, 2])\n'
                                  'q = np.array([4, 6])\n'
                                  '\n'
                                  'd_euclid = np.linalg.norm(p - q, ord=2)\n'
                                  'd_manhat = np.linalg.norm(p - q, ord=1)\n'
                                  "print(f'Euclidiana: {d_euclid} | Manhattan: {d_manhat}')"},
           'video2_url': 'https://www.youtube.com/watch?v=hl3bQySs8sM',
           'video2_label': '🎬 2ª Opção: StatQuest Métricas de Distância'}]],
        ['Teoria da Informação & Perda',
         [{'title': 'Entropia de Shannon (medida de incerteza da informação)',
           'video_url': 'https://www.youtube.com/watch?v=H3eh00i2v-A',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=entropia+da+informacao+shannon',
           'doc_url': 'https://pt.khanacademy.org/computing/computer-science/informationtheory/moderninfotheory/v/information-entropy',
           'doc_label': '📘 Aula Visual PT-BR: Entropia Shannon',
           'pt_guide': {'intuicao': 'Criada por Claude Shannon, a <b>Entropia ($H$)</b> mede o <b>grau de surpresa, '
                                    'bagunça ou incerteza</b> de uma distribuição de probabilidade:\n'
                                    '• Se uma moeda tem 100% de chance de dar Cara ($p=1.0$), não há surpresa nenhuma: '
                                    '<b>Entropia = 0</b>.\n'
                                    '• Se a moeda é honesta ($50\\%$ Cara / $50\\%$ Coroa), a incerteza é máxima: '
                                    '<b>Entropia = 1 bit</b>!\n'
                                    'Árvores de Decisão (*Random Forest / XGBoost*) escolhem perguntas que reduzem a '
                                    'entropia!',
                        'formula': '$$H(P) = -\\sum_{i} P(x_i) \\log_2 P(x_i)$$',
                        'exemplo': 'Para uma moeda justa $P = [0.5, 0.5]$:\n'
                                   '$$H = -(0.5 \\log_2 0.5 + 0.5 \\log_2 0.5) = -(0.5(-1) + 0.5(-1)) = 1.0 \\text{ '
                                   'bit}$$',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'def entropia_shannon(probs):\n'
                                  '    p = np.array(probs)\n'
                                  '    p = p[p > 0] # Evita log(0)\n'
                                  '    return -np.sum(p * np.log2(p))\n'
                                  '\n'
                                  "print('Moeda viciada [0.99, 0.01]:', round(entropia_shannon([0.99, 0.01]), 3))\n"
                                  "print('Moeda justa   [0.50, 0.50]:', round(entropia_shannon([0.50, 0.50]), 3))"},
           'video2_url': 'https://www.youtube.com/watch?v=l6DKRf-fAAM',
           'video2_label': '🎬 2ª Opção: 3B1B Entropia de Shannon'},
          {'title': 'Entropia Cruzada (Cross-Entropy Loss) e função Softmax',
           'video_url': 'https://www.youtube.com/watch?v=MUfVNqHkq-c',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=teoria+da+informacao+probabilidade',
           'doc_url': 'https://pt.khanacademy.org/computing/computer-science/informationtheory',
           'doc_label': '📘 Aula Visual PT-BR: Softmax & Cross-Entropy',
           'pt_guide': {'intuicao': 'Esta é a dupla mais famosa do Deep Learning e dos LLMs:\n'
                                    '1. <b>Softmax:</b> Pega as notas brutas (*logits*) da última camada da rede (ex.: '
                                    '`[2.0, 1.0, 0.1]`) e aplica $e^x$ dividido pela soma, transformando tudo em '
                                    '<b>probabilidades que somam 100%</b> (`[0.66, 0.24, 0.10]`).\n'
                                    '2. <b>Cross-Entropy Loss (Entropia Cruzada):</b> Mede a distância entre a '
                                    'probabilidade que o modelo previu e o gabarito real!',
                        'formula': '$$\\text{Softmax}(z_i) = \\frac{e^{z_i}}{\\sum_{j} e^{z_j}} \\quad | \\quad '
                                   'L_{\\text{CE}} = -\\sum_{i} y_i \\ln(\\hat{p}_i) = -\\ln(\\hat{p}_{\\text{classe '
                                   'correta}})$$',
                        'exemplo': 'Se o gabarito real é a classe 0 (`Gato`) e o Softmax do modelo deu $\\hat{p}_0 = '
                                   '0.66$ (66% de confiança em Gato):\n'
                                   'O erro Cross-Entropy é simplesmente $-\\ln(0.66) \\approx 0.415$. Se o modelo '
                                   'melhorar para $99\\%$, o erro cai para $-\\ln(0.99) \\approx 0.01$!',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'logits = np.array([2.0, 1.0, 0.1])\n'
                                  '# 1. Softmax\n'
                                  'exps = np.exp(logits)\n'
                                  'probs = exps / np.sum(exps)\n'
                                  "print('Probabilidades Softmax:', np.round(probs, 3)) # [0.659, 0.242, 0.099]\n"
                                  '\n'
                                  '# 2. Cross-Entropy para classe correta = índice 0\n'
                                  'loss = -np.log(probs[0])\n'
                                  "print('Cross-Entropy Loss:', round(loss, 4))"},
           'video2_url': 'https://www.youtube.com/watch?v=6ArSys5qHAU',
           'video2_label': '🎬 2ª Opção: StatQuest Cross-Entropy'},
          {'title': 'Divergência de Kullback-Leibler (KL Divergence)',
           'video_url': 'https://www.youtube.com/watch?v=2fzYE-Emar0',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=comparacao+de+distribuicoes+z+score',
           'doc_url': 'https://pt.khanacademy.org/math/statistics-probability/modeling-distributions-of-data/z-scores/v/ck12-org-normal-distribution-problems-z-score',
           'doc_label': '📘 Aula Visual PT-BR: Divergência KL',
           'pt_guide': {'intuicao': 'A <b>Divergência KL ($D_{KL}(P \\parallel Q)$)</b> mede o quanto uma distribuição '
                                    'de probabilidade $Q$ (do seu modelo) se afastou de uma distribuição de referência '
                                    '$P$. Ela é fundamental no <b>RLHF / PPO / DPO</b> (alinhamento de LLMs como o '
                                    'ChatGPT): usamos a Divergência KL para garantir que o modelo alinhado não se '
                                    'afaste demais do modelo base original e não desaprendas a falar!',
                        'formula': '$$D_{KL}(P \\parallel Q) = \\sum_{i} P(i) \\ln\\left(\\frac{P(i)}{Q(i)}\\right)$$\n'
                                   'Se $P$ e $Q$ forem idênticas, $D_{KL} = 0$. Caso contrário, é sempre positiva ($> '
                                   '0$).',
                        'exemplo': 'Se o modelo base dá $P = [0.8, 0.2]$ e o novo modelo dá $Q = [0.5, 0.5]$:\n'
                                   '$$D_{KL} = 0.8 \\ln(0.8/0.5) + 0.2 \\ln(0.2/0.5) \\approx 0.376 - 0.183 = 0.193$$',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'P = np.array([0.8, 0.2])\n'
                                  'Q = np.array([0.5, 0.5])\n'
                                  '\n'
                                  'kl_div = np.sum(P * np.log(P / Q))\n'
                                  "print('Divergência KL(P || Q):', round(kl_div, 4)) # 0.1927"},
           'video2_url': 'https://www.youtube.com/watch?v=SxGYPqCgJWM',
           'video2_label': '🎬 2ª Opção: StatQuest KL Divergence'},
          {'title': 'Funções de perda de regressão (MSE, MAE, Huber) e classificação',
           'video_url': 'https://www.youtube.com/watch?v=YqjrJQchKV0',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=residuos+erro+quadratico+regressao',
           'doc_url': 'https://pt.khanacademy.org/math/statistics-probability/describing-relationships-quantitative-data/more-on-regression/v/residual-plots',
           'doc_label': '📘 Aula Visual PT-BR: MSE, MAE & Huber',
           'pt_guide': {'intuicao': 'Quando prevemos números contínuos (preços, vendas, temperatura), como medimos o '
                                    'erro?\n'
                                    '• <b>MSE (Erro Quadrático Médio):</b> Eleva o erro ao quadrado $(y - '
                                    '\\hat{y})^2$. Penaliza severamente erros grandes!\n'
                                    '• <b>MAE (Erro Absoluto Médio):</b> Usa o módulo $|y - \\hat{y}|$. É mais '
                                    'resistente a outliers.\n'
                                    '• <b>Huber Loss:</b> Combina o melhor dos dois (quadrática para erros pequenos e '
                                    'linear para erros gigantes).',
                        'formula': '$$\\text{MSE} = \\frac{1}{n}\\sum_{i=1}^n (y_i - \\hat{y}_i)^2 \\quad | \\quad '
                                   '\\text{MAE} = \\frac{1}{n}\\sum_{i=1}^n |y_i - \\hat{y}_i|$$',
                        'exemplo': 'Erros em 3 previsões: `[1, 2, 10]`.\n'
                                   '• <b>MAE:</b> $(1 + 2 + 10) / 3 = 4.33$\n'
                                   '• <b>MSE:</b> $(1^2 + 2^2 + 10^2) / 3 = 105 / 3 = 35.0$ (Veja como o erro $10$ '
                                   'dominou o MSE!).',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'y_real = np.array([100, 200, 300])\n'
                                  'y_prev = np.array([102, 195, 320])\n'
                                  '\n'
                                  'mse = np.mean((y_real - y_prev) ** 2)\n'
                                  'mae = np.mean(np.abs(y_real - y_prev))\n'
                                  "print(f'MAE: {mae:.2f} | MSE: {mse:.2f} | RMSE: {np.sqrt(mse):.2f}')"},
           'video2_url': 'https://www.youtube.com/watch?v=Ilg3gGewQ5U',
           'video2_label': '🎬 2ª Opção: 3B1B Funções de Perda'}]]]},
 {'t': 'Módulo 5 · Matemática dos Transformers & Geometria de Embeddings',
  'd': '2 semanas',
  'tip': '💡 <b>Como Estudar sem Travar:</b> Comece clicando no botão vermelho <b>▶ Khan Academy PT-BR</b> (1ª Opção) '
         'para assistir à explicação calma, passo a passo e em português no quadro. Depois, leia os 4 passos da <b>📘 '
         'Aula Visual PT-BR</b> logo abaixo do vídeo. Quando quiser ver a intuição geométrica animada, alterne para a '
         '<b>🎬 2ª Opção (3B1B / StatQuest)</b>!',
  'p': 'Implementar em Python/NumPy a função exata de Scaled Dot-Product Attention e inspecionar a matriz de pesos de '
       'atenção.',
  'r': '1ª Opção: Canal Oficial Khan Academy Português (@khanacademyportugues) · 2ª Opção: 3Blue1Brown & StatQuest · '
       'Aula Visual & Apostila Interativa em Português',
  'g': [['Geometria Vetorial em IA Moderna',
         [{'title': 'Espaços vetoriais de alta dimensão e armazenamento de fatos em LLMs',
           'video_url': 'https://www.youtube.com/watch?v=wEUj7cZtHYo',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=espacos+e+subespacos+vetoriais',
           'doc_url': 'https://pt.khanacademy.org/math/linear-algebra/vectors-and-spaces/subspaces-and-the-basis-for-a-subspace/v/linear-subspaces',
           'doc_label': '📘 Aula Visual PT-BR: Alta Dimensão',
           'pt_guide': {'intuicao': 'Nós humanos só conseguimos enxergar até 3 dimensões (largura, altura e '
                                    'profundidade). Mas os LLMs operam em espaços de <b>768, 1.536 ou 4.096 '
                                    'dimensões</b>! Nesses espaços gigantescos, cada direção pode codificar um '
                                    'conceito semântico independente (gênero, tempo verbal, capital de país, '
                                    'sentimento, idioma), permitindo que a rede armazene milhões de conceitos como '
                                    'direções quase perpendiculares!',
                        'formula': '$$\\vec{e}_{\\text{Rei}} - \\vec{e}_{\\text{Homem}} + \\vec{e}_{\\text{Mulher}} '
                                   '\\approx \\vec{e}_{\\text{Rainha}}$$',
                        'exemplo': "A aritmética vetorial funciona em conceitos! Se você subtrair o vetor de 'França' "
                                   "do vetor de 'Paris' e somar o vetor de 'Brasil', você aterrissa muito perto do "
                                   "vetor de 'Brasília'!",
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  '# Simulando vetores semânticos [Realeza, Feminino, Idade]\n'
                                  'rei    = np.array([0.95, 0.05, 0.70])\n'
                                  'homem  = np.array([0.05, 0.05, 0.70])\n'
                                  'mulher = np.array([0.05, 0.95, 0.70])\n'
                                  '\n'
                                  'resultado = rei - homem + mulher\n'
                                  "print('Vetor resultante (Rainha):', np.round(resultado, 2)) # [0.95, 0.95, 0.70]"},
           'video2_url': 'https://www.youtube.com/watch?v=9-Jl0dxWQs8',
           'video2_label': '🎬 2ª Opção: 3B1B Fatos em LLMs'},
          {'title': 'Normalização de embeddings e geometria do espaço semântico',
           'video_url': 'https://www.youtube.com/watch?v=u7xJkFbf9qw',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=vetor+unitario+normalizacao',
           'doc_url': 'https://pt.khanacademy.org/math/precalculus/x9e81a4f98389efdf:vectors/x9e81a4f98389efdf:unit-vectors/v/intro-unit-vector-notation',
           'doc_label': '📘 Aula Visual PT-BR: Norm. Embeddings',
           'pt_guide': {'intuicao': 'Em bancos de dados vetoriais (como Pinecone, Qdrant, Chroma e FAISS usados em '
                                    'sistemas RAG), costumamos <b>normalizar todos os embeddings para que tenham '
                                    'tamanho (norma L2) igual a $1.0$</b>. Por quê? Porque quando dois vetores têm '
                                    'tamanho $1$, a <b>Similaridade de Cosseno vira um simples Produto Escalar (`u @ '
                                    'v`)</b>, tornando a busca em milhões de documentos muito mais rápida!',
                        'formula': '$$\\hat{u} = \\frac{\\vec{u}}{\\|\\vec{u}\\|_2} \\implies \\|\\hat{u}\\|_2 = 1 '
                                   '\\implies \\cos(\\theta) = \\hat{u} \\cdot \\hat{v}$$',
                        'exemplo': 'O vetor $\\vec{u} = [3, 4]$ tem tamanho $\\sqrt{3^2+4^2} = 5$.\n'
                                   'Dividindo por $5$, obtemos o vetor unitário normalizado $\\hat{u} = [0.6, 0.8]$, '
                                   'pois $0.6^2 + 0.8^2 = 0.36 + 0.64 = 1.0$!',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'u = np.array([3.0, 4.0])\n'
                                  'u_norm = u / np.linalg.norm(u)\n'
                                  "print('Embedding normalizado:', u_norm)             # [0.6, 0.8]\n"
                                  "print('Nova norma (sempre 1.0):', np.linalg.norm(u_norm)) # 1.0"},
           'video2_url': 'https://www.youtube.com/watch?v=wjZofJX0v4M',
           'video2_label': '🎬 2ª Opção: 3B1B O que é GPT / Embeddings'},
          {'title': 'Projeções lineares e matrizes de pesos Query, Key e Value (W_q, W_k, W_v)',
           'video_url': 'https://www.youtube.com/watch?v=we829K4NOq8',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=projecoes+lineares+em+subespacos+matrizes',
           'doc_url': 'https://pt.khanacademy.org/math/linear-algebra/alternate-bases/orthogonal-projections/v/linear-algebra-projections-onto-subspaces',
           'doc_label': '📘 Aula Visual PT-BR: Matrizes Q, K, V',
           'pt_guide': {'intuicao': 'Para que cada palavra de uma frase converse com as outras no Transformer, '
                                    'multiplicamos o embedding de cada palavra $X$ por 3 matrizes aprendidas ($W_Q, '
                                    'W_K, W_V$), gerando 3 papéis:\n'
                                    '• <b>Query ($Q$ - Pergunta):</b> O que esta palavra está procurando no contexto? '
                                    '(ex.: um adjetivo procurando a qual substantivo se refere).\n'
                                    '• <b>Key ($K$ - Etiqueta/Chave):</b> O que esta palavra oferece de '
                                    'identificação?\n'
                                    '• <b>Value ($V$ - Conteúdo/Valor):</b> A informação semântica que será '
                                    'transferida se der *match*!',
                        'formula': '$$Q = X W_Q \\quad | \\quad K = X W_K \\quad | \\quad V = X W_V$$',
                        'exemplo': "Na frase <i>'O banco estava fechado porque ele faliu'</i>, a palavra <b>'ele'</b> "
                                   "gera uma <b>Query ($Q$)</b> procurando *'quem é o sujeito financeiro?'*. A palavra "
                                   "<b>'banco'</b> tem uma <b>Key ($K$)</b> compatível! O match entre $Q$ e $K$ "
                                   "transfere o <b>Value ($V$)</b> de 'banco' para 'ele'.",
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  '# 3 palavras com embeddings de dimensão 4\n'
                                  'X = np.random.randn(3, 4)\n'
                                  '# Matrizes de projeção (4 -> 2)\n'
                                  'Wq, Wk, Wv = np.random.randn(4, 2), np.random.randn(4, 2), np.random.randn(4, 2)\n'
                                  '\n'
                                  'Q, K, V = X @ Wq, X @ Wk, X @ Wv\n'
                                  "print('Shapes Q, K, V:', Q.shape, K.shape, V.shape) # (3, 2)"},
           'video2_url': 'https://www.youtube.com/watch?v=eMlx5fFNoYc',
           'video2_label': '🎬 2ª Opção: 3B1B Atenção em Transformers'}]],
        ['Matemática da Atenção',
         [{'title': 'Fórmula de Scaled Dot-Product Attention: softmax((Q @ K^T) / sqrt(d_k)) * V',
           'video_url': 'https://www.youtube.com/watch?v=aKhhYguY0DQ',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=multiplicacao+de+matrizes+produto+escalar',
           'doc_url': 'https://pt.khanacademy.org/math/precalculus/x9e81a4f98389efdf:matrices/x9e81a4f98389efdf:multiplying-matrices-by-matrices/a/multiplying-matrices',
           'doc_label': '📘 Aula Visual PT-BR: Fórmula da Atenção',
           'pt_guide': {'intuicao': 'Esta é a equação mais importante da IA moderna (do artigo *Attention Is All You '
                                    'Need*), explicada passo a passo:\n'
                                    '1. <b>`Q @ K.T`</b>: Calcula o produto escalar entre todas as Perguntas ($Q$) e '
                                    'todas as Chaves ($K$), medindo a afinidade entre cada par de palavras.\n'
                                    '2. <b>`/ sqrt(d_k)`</b>: Divide pela raiz da dimensão para que os números não '
                                    'fiquem gigantescos e não saturem o Softmax.\n'
                                    '3. <b>`softmax(...)`</b>: Transforma as afinidades em pesos percentuais que somam '
                                    '$100\\%$.\n'
                                    '4. <b>`@ V`</b>: Faz a média ponderada dos Valores ($V$) com base na atenção!',
                        'formula': '$$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{Q '
                                   'K^T}{\\sqrt{d_k}}\\right) V$$',
                        'exemplo': "Se uma palavra dá $80\\%$ de atenção para 'banco' e $20\\%$ para 'fechado', seu "
                                   'novo vetor será $0.80 \\cdot V_{\\text{banco}} + 0.20 \\cdot V_{\\text{fechado}}$!',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  'def self_attention(Q, K, V):\n'
                                  '    d_k = Q.shape[-1]\n'
                                  '    scores = (Q @ K.T) / np.sqrt(d_k)\n'
                                  '    exps = np.exp(scores - np.max(scores, axis=-1, keepdims=True))\n'
                                  '    pesos_atencao = exps / np.sum(exps, axis=-1, keepdims=True)\n'
                                  '    return pesos_atencao @ V, pesos_atencao\n'
                                  '\n'
                                  'Q = K = V = np.array([[1.0, 0.0], [0.9, 0.2], [0.0, 1.0]])\n'
                                  'saida, pesos = self_attention(Q, K, V)\n'
                                  "print('Matriz de Pesos de Atenção:\\n', np.round(pesos, 2))"},
           'video2_url': 'https://www.youtube.com/watch?v=eMlx5fFNoYc',
           'video2_label': '🎬 2ª Opção: 3B1B Fórmula da Atenção'},
          {'title': 'Mecanismo Multi-Head Attention: divisão de dimensões e concatenação',
           'video_url': 'https://www.youtube.com/watch?v=HWw_9l1oQYE',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=composicao+de+transformacoes+lineares',
           'doc_url': 'https://pt.khanacademy.org/math/linear-algebra/matrix-transformations/composition-of-transformations/v/linear-algebra-compositions-of-linear-transformations-1',
           'doc_label': '📘 Aula Visual PT-BR: Multi-Head Attention',
           'pt_guide': {'intuicao': 'Por que ter apenas 1 cabeça de atenção se podemos ter várias em paralelo '
                                    '(<b>Multi-Head Attention</b>)? Dividindo um embedding de $512$ dimensões em $8$ '
                                    'cabeças de $64$ dimensões cada:\n'
                                    '• A <b>Cabeça 1</b> pode focar na relação gramatical (sujeito $\\leftrightarrow$ '
                                    'verbo).\n'
                                    "• A <b>Cabeça 2</b> pode focar em pronomes ('ele' $\\leftrightarrow$ 'João').\n"
                                    '• A <b>Cabeça 3</b> pode focar em rimas ou código!\n'
                                    'No final, concatenamos todas as cabeças lado a lado e multiplicamos por $W_O$.',
                        'formula': '$$\\text{MultiHead}(Q, K, V) = \\text{Concat}(\\text{head}_1, \\dots, '
                                   '\\text{head}_h) W_O$$',
                        'exemplo': 'Se `d_model = 768` e usamos `num_heads = 12`, cada cabeça trabalha com vetores '
                                   'menores de tamanho `d_k = 768 / 12 = 64`. Quando juntamos as 12 saídas de tamanho '
                                   '64 (`12 * 64`), voltamos exatamente para `768`!',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  '# Simulando Concatenação de 2 cabeças de atenção (cada uma com dimensão 2 -> total '
                                  '4)\n'
                                  'head_1 = np.array([[0.1, 0.2], [0.3, 0.4]]) # Foco sintático\n'
                                  'head_2 = np.array([[0.8, 0.9], [0.5, 0.6]]) # Foco semântico\n'
                                  '\n'
                                  'concat = np.concatenate([head_1, head_2], axis=-1)\n'
                                  "print('Saída concatenada (2 tokens x 4 dims):\\n', concat)"},
           'video2_url': 'https://www.youtube.com/watch?v=wjZofJX0v4M',
           'video2_label': '🎬 2ª Opção: 3B1B Multi-Head Attention'},
          {'title': 'Positional Encodings: funções sinusoidais e rotação vetorial (RoPE)',
           'video_url': 'https://www.youtube.com/watch?v=l5M24T20FZ8',
           'video_label': '▶ Khan Academy PT-BR',
           'yt_pt_url': 'https://www.youtube.com/@khanacademyportugues/search?query=rotacao+de+vetores+matriz+de+rotacao',
           'doc_url': 'https://pt.khanacademy.org/math/linear-algebra/matrix-transformations/lin-trans-examples/v/linear-transformation-examples-rotations-in-r2',
           'doc_label': '📘 Aula Visual PT-BR: Positional & RoPE',
           'pt_guide': {'intuicao': 'Diferente dos humanos, o Transformer processa todas as palavras da frase ao mesmo '
                                    "tempo (em paralelo). Sem uma marcação de posição, para ele <i>'O cachorro mordeu "
                                    "o homem'</i> seria idêntico a <i>'O homem mordeu o cachorro'</i>! O <b>Positional "
                                    'Encoding</b> injeta a ordem das palavras usando ondas de seno e cosseno. Nos LLMs '
                                    'atuais (Llama 3, Qwen, DeepSeek), usamos o <b>RoPE (Rotary Position '
                                    'Embedding)</b>, que gira os vetores $Q$ e $K$ em um ângulo proporcional à posição '
                                    'da palavra!',
                        'formula': '$$PE_{(pos, 2i)} = \\sin\\left(\\frac{pos}{10000^{2i/d}}\\right) \\quad | \\quad '
                                   'R_\\theta = \\begin{bmatrix} \\cos(m\\theta) & -\\sin(m\\theta) \\\\ '
                                   '\\sin(m\\theta) & \\cos(m\\theta) \\end{bmatrix}$$',
                        'exemplo': 'Com o <b>RoPE</b>, se a palavra A está na posição $2$ e a palavra B está na '
                                   'posição $5$, o produto escalar entre elas depende apenas da <b>distância relativa '
                                   '($5 - 2 = 3$)</b> entre os seus ângulos de rotação!',
                        'codigo': 'import numpy as np\n'
                                  '\n'
                                  '# Aplicando Rotação Posicional 2D (RoPE) em um vetor na posição m\n'
                                  'def aplicar_rope_2d(vetor, pos, theta=0.1):\n'
                                  '    ang = pos * theta\n'
                                  '    R = np.array([[np.cos(ang), -np.sin(ang)],\n'
                                  '                  [np.sin(ang),  np.cos(ang)]])\n'
                                  '    return R @ vetor\n'
                                  '\n'
                                  'v = np.array([1.0, 0.0])\n'
                                  "print('Posição 0:', np.round(aplicar_rope_2d(v, 0), 3))\n"
                                  "print('Posição 5:', np.round(aplicar_rope_2d(v, 5), 3))"},
           'video2_url': 'https://www.youtube.com/watch?v=eMlx5fFNoYc',
           'video2_label': '🎬 2ª Opção: 3B1B Positional Embeddings'}]]]}]
