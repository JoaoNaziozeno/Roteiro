import json, os, re

# Carregar playlist de inglês limpa
with open('/mnt/c/Users/joao1/Desktop/Roteiro/english_playlist.json', 'r', encoding='utf-8') as f:
    english_playlist = json.load(f)

# ---------------------------------------------------------------------------
# 1. Dados de IA (6 Fases Técnicas - 173 Tópicos)
# ---------------------------------------------------------------------------
from build_ia_data import get_enriched_ia_phases
ia_phases = get_enriched_ia_phases()

# ---------------------------------------------------------------------------
# 2. Dados de Matemática (5 Módulos - 43 Tópicos com Vídeos 3B1B/StatQuest e PDFs)
# ---------------------------------------------------------------------------
mat_phases = [
    {
        "t": "Módulo 1 · Álgebra Linear para IA & Tensores",
        "d": "3 a 4 semanas",
        "tip": "💡 <b>Dica de Ouro:</b> A intuição geométrica importa mais que decorar regras. Assista aos vídeos do 3Blue1Brown para visualizar transformações espaciais e consulte o livro MML (Mathematics for Machine Learning) para a notação formal.",
        "p": "Implementar multiplicação de matrizes pura (sem NumPy) e comparar o tempo de execução com `torch.matmul` em GPU.",
        "r": "Canal 3Blue1Brown (Essence of Linear Algebra) · Livro Cambridge Mathematics for Machine Learning (PDF gratuito) · Immersive Linear Algebra",
        "g": [
            [
                "Vetores e Operações",
                [
                    {
                        "title": "Vetores e espaços vetoriais: intuição geométrica",
                        "video_url": "https://www.youtube.com/watch?v=fNk_zzaMoSs",
                        "video_label": "▶ 3B1B Vetores",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=42",
                        "doc_label": "📖 PDF MML Cap 2.1"
                    },
                    {
                        "title": "Combinações lineares, espaço gerado (span) e bases",
                        "video_url": "https://www.youtube.com/watch?v=k7RM-ot2NWY",
                        "video_label": "▶ 3B1B Span & Bases",
                        "doc_url": "https://immersivemath.com/ila/ch03_vectors/ch03.html",
                        "doc_label": "📖 Immersive Math Cap 3"
                    },
                    {
                        "title": "Produto escalar (Dot Product) e projeções",
                        "video_url": "https://www.youtube.com/watch?v=LyGKycYT2v0",
                        "video_label": "▶ 3B1B Dot Product",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=75",
                        "doc_label": "📖 PDF MML Cap 3.1"
                    },
                    {
                        "title": "Norma de vetores (L1, L2 Euclidiana) e distâncias",
                        "video_url": "https://www.youtube.com/watch?v=LyGKycYT2v0",
                        "video_label": "▶ 3B1B Normas",
                        "doc_url": "https://www.deeplearningbook.org/contents/linear_algebra.html",
                        "doc_label": "📖 Deep Learning Cap 2.5"
                    },
                    {
                        "title": "Ângulo entre vetores e Similaridade de Cosseno",
                        "video_url": "https://www.youtube.com/watch?v=e9U0QAFbfLI",
                        "video_label": "▶ StatQuest Cosseno",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=78",
                        "doc_label": "📖 PDF MML Cap 3.2"
                    }
                ]
            ],
            [
                "Matrizes e Tensores",
                [
                    {
                        "title": "Matrizes como transformações lineares no espaço",
                        "video_url": "https://www.youtube.com/watch?v=kYB8IZa5AuE",
                        "video_label": "▶ 3B1B Matrizes",
                        "doc_url": "https://immersivemath.com/ila/ch04_matrices/ch04.html",
                        "doc_label": "📖 Immersive Math Cap 4"
                    },
                    {
                        "title": "Multiplicação de matrizes (Dot product vs. Hadamard elemento a elemento)",
                        "video_url": "https://www.youtube.com/watch?v=XkY2DOUCWMU",
                        "video_label": "▶ 3B1B Mult. Matrizes",
                        "doc_url": "https://www.deeplearningbook.org/contents/linear_algebra.html",
                        "doc_label": "📖 Deep Learning Cap 2.2"
                    },
                    {
                        "title": "Sistemas de equações lineares e determinantes",
                        "video_url": "https://www.youtube.com/watch?v=Ip3X9LOh2dk",
                        "video_label": "▶ 3B1B Determinante",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=55",
                        "doc_label": "📖 PDF MML Cap 2.3"
                    },
                    {
                        "title": "Inversa de matriz e pseudoinversa de Moore-Penrose",
                        "video_url": "https://www.youtube.com/watch?v=uQhTuRlWM3E",
                        "video_label": "▶ 3B1B Inversa & Colunas",
                        "doc_url": "https://www.deeplearningbook.org/contents/linear_algebra.html",
                        "doc_label": "📖 Deep Learning Cap 2.9"
                    },
                    {
                        "title": "Autovalores e Autovetores (Eigenvalues & Eigenvectors)",
                        "video_url": "https://www.youtube.com/watch?v=PFDu9oVAE-g",
                        "video_label": "▶ 3B1B Autovalores",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=105",
                        "doc_label": "📖 PDF MML Cap 4.2"
                    },
                    {
                        "title": "Decomposição em Valores Singulares (SVD) e PCA",
                        "video_url": "https://www.youtube.com/watch?v=FgakZw6K1QQ",
                        "video_label": "▶ StatQuest PCA",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=320",
                        "doc_label": "📖 PDF MML Cap 10 PCA"
                    }
                ]
            ]
        ]
    },
    {
        "t": "Módulo 2 · Cálculo Diferencial, Gradientes & Otimização",
        "d": "3 a 4 semanas",
        "tip": "💡 <b>Dica de Ouro:</b> O conceito de derivada como taxa instantânea de variação e a Regra da Cadeia são a chave para dominar todo o Backpropagation das redes neurais.",
        "p": "Construir do zero em Python uma descida de gradiente com cálculo manual de derivada para minimizar uma função de perda quadrática.",
        "r": "Canal 3Blue1Brown (Essence of Calculus) · Andrej Karpathy (Micrograd) · Livro Cambridge MML Cap 5",
        "g": [
            [
                "Cálculo Diferencial",
                [
                    {
                        "title": "Limites e taxa de variação instantânea (ideia geral)",
                        "video_url": "https://www.youtube.com/watch?v=WUvTyaaNkzM",
                        "video_label": "▶ 3B1B Essência do Cálculo",
                        "doc_url": "https://www.3blue1brown.com/lessons/essence-of-calculus",
                        "doc_label": "📖 3B1B Artigo Cap 1"
                    },
                    {
                        "title": "Derivadas fundamentais e regras básicas (potência, produto, soma)",
                        "video_url": "https://www.youtube.com/watch?v=S0_qX4VFYMQ",
                        "video_label": "▶ 3B1B Derivadas Geométricas",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=145",
                        "doc_label": "📖 PDF MML Cap 5.2"
                    },
                    {
                        "title": "Regra da Cadeia (Chain Rule) - o motor do Backpropagation",
                        "video_url": "https://www.youtube.com/watch?v=YG15m2VwSjA",
                        "video_label": "▶ 3B1B Regra da Cadeia",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=153",
                        "doc_label": "📖 PDF MML Cap 5.4"
                    },
                    {
                        "title": "Derivadas de funções de ativação (Sigmoide, Tanh, ReLU, GeLU)",
                        "video_url": "https://www.youtube.com/watch?v=aircAruvnKk",
                        "video_label": "▶ 3B1B Redes Neurais",
                        "doc_url": "https://github.com/karpathy/micrograd",
                        "doc_label": "💻 Micrograd Karpathy"
                    }
                ]
            ],
            [
                "Gradientes e Otimizadores",
                [
                    {
                        "title": "Derivadas parciais e o vetor Gradiente (nabla f)",
                        "video_url": "https://www.youtube.com/watch?v=IHZwWFHWa-w",
                        "video_label": "▶ 3B1B Gradiente Descendente",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=148",
                        "doc_label": "📖 PDF MML Cap 5.1"
                    },
                    {
                        "title": "Matriz Jacobiana e Matriz Hessiana (curvatura da loss)",
                        "video_url": "https://www.youtube.com/watch?v=Ilg3gGewQ5U",
                        "video_label": "▶ 3B1B O que é Backprop?",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=150",
                        "doc_label": "📖 PDF MML Cap 5.3"
                    },
                    {
                        "title": "Algoritmo de Descida do Gradiente (Vanilla Gradient Descent)",
                        "video_url": "https://www.youtube.com/watch?v=tIeHLnjs5U8",
                        "video_label": "▶ 3B1B Backprop Calculus",
                        "doc_url": "https://www.deeplearningbook.org/contents/numerical.html",
                        "doc_label": "📖 Deep Learning Cap 4.3"
                    },
                    {
                        "title": "Otimizadores modernos: Momentum, RMSprop e Adam",
                        "video_url": "https://www.youtube.com/watch?v=vMh0zPT0tLI",
                        "video_label": "▶ StatQuest SGD",
                        "doc_url": "https://www.deeplearningbook.org/contents/optimization.html",
                        "doc_label": "📖 Deep Learning Cap 8.5"
                    },
                    {
                        "title": "Taxa de aprendizado (Learning Rate), convergência e pontos de sela",
                        "video_url": "https://www.youtube.com/watch?v=sDv4f4s2SB8",
                        "video_label": "▶ StatQuest Learning Rate",
                        "doc_url": "https://www.deeplearningbook.org/contents/numerical.html",
                        "doc_label": "📖 Deep Learning Cap 4.3"
                    }
                ]
            ]
        ]
    },
    {
        "t": "Módulo 3 · Probabilidade & Estatística para IA",
        "d": "3 a 4 semanas",
        "tip": "💡 <b>Dica de Ouro:</b> Todo modelo de IA toma decisões sob incerteza. Entender o Teorema de Bayes e as distribuições permite mensurar a confiança das previsões.",
        "p": "Criar um notebook calculando a probabilidade a posteriori de um diagnóstico ou classificação de spam usando o Teorema de Bayes.",
        "r": "Canal 3Blue1Brown · StatQuest com Josh Starmer · Livro Cambridge MML Cap 6",
        "g": [
            [
                "Estatística Descritiva & Probabilidade",
                [
                    {
                        "title": "Variáveis aleatórias discretas e contínuas",
                        "video_url": "https://www.youtube.com/watch?v=HZGCoVF3YvM",
                        "video_label": "▶ 3B1B Probabilidade",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=175",
                        "doc_label": "📖 PDF MML Cap 6.1"
                    },
                    {
                        "title": "Média, mediana, variância e desvio padrão",
                        "video_url": "https://www.youtube.com/watch?v=SzZ6G436HKM",
                        "video_label": "▶ StatQuest Variância",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=182",
                        "doc_label": "📖 PDF MML Cap 6.4"
                    },
                    {
                        "title": "Esperança matemática, covariância e correlação",
                        "video_url": "https://www.youtube.com/watch?v=qtaqvPAeEJY",
                        "video_label": "▶ StatQuest Covariância",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=183",
                        "doc_label": "📖 PDF MML Cap 6.4"
                    },
                    {
                        "title": "Probabilidade condicional e Teorema de Bayes",
                        "video_url": "https://www.youtube.com/watch?v=HZGCoVF3YvM",
                        "video_label": "▶ 3B1B Teorema de Bayes",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=178",
                        "doc_label": "📖 PDF MML Cap 6.3"
                    }
                ]
            ],
            [
                "Distribuições & Inferência",
                [
                    {
                        "title": "Distribuição Normal (Gaussiana) e probabilidade vs verossimilhança",
                        "video_url": "https://www.youtube.com/watch?v=rzFX5NWojp0",
                        "video_label": "▶ StatQuest Dist. Normal",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=190",
                        "doc_label": "📖 PDF MML Cap 6.5"
                    },
                    {
                        "title": "Teorema do Limite Central e amostragem",
                        "video_url": "https://www.youtube.com/watch?v=JNm3M9IJihQ",
                        "video_label": "▶ StatQuest Limite Central",
                        "doc_url": "https://www.khanacademy.org/math/statistics-probability",
                        "doc_label": "📖 Khan Academy Estatística"
                    },
                    {
                        "title": "Intervalos de confiança e teste de hipóteses (noção)",
                        "video_url": "https://www.youtube.com/watch?v=TqOeMYtOc1w",
                        "video_label": "▶ StatQuest Confiança",
                        "doc_url": "https://www.deeplearningbook.org/contents/prob.html",
                        "doc_label": "📖 Deep Learning Cap 3.9"
                    },
                    {
                        "title": "Máxima Verossimilhança (Maximum Likelihood Estimation - MLE)",
                        "video_url": "https://www.youtube.com/watch?v=XepXtl9YKwc",
                        "video_label": "▶ StatQuest MLE",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=278",
                        "doc_label": "📖 PDF MML Cap 9.1"
                    },
                    {
                        "title": "Trade-off Viés vs. Variância (Bias-Variance Dilemma)",
                        "video_url": "https://www.youtube.com/watch?v=EuBBz3bI-aA",
                        "video_label": "▶ StatQuest Viés vs Variância",
                        "doc_url": "https://www.deeplearningbook.org/contents/ml.html",
                        "doc_label": "📖 Deep Learning Cap 5.4"
                    }
                ]
            ]
        ]
    },
    {
        "t": "Módulo 4 · Funções Matemáticas, Geometria & Teoria da Informação",
        "d": "2 semanas",
        "tip": "💡 <b>Dica de Ouro:</b> Entropia mede o grau de incerteza da informação. A Cross-Entropy Loss é simplesmente a penalidade aplicada quando a previsão do modelo discorda da distribuição real.",
        "p": "Calcular manualmente e plotar o gráfico da Cross-Entropy Loss comparada com MSE para um problema de classificação binária.",
        "r": "Canal 3Blue1Brown (Entropia & Teoria da Informação) · StatQuest · Deep Learning Book Cap 3",
        "g": [
            [
                "Álgebra e Geometria Analítica",
                [
                    {
                        "title": "Equações, inequações e gráficos de funções aplicadas",
                        "video_url": "https://www.youtube.com/watch?v=WUvTyaaNkzM",
                        "video_label": "▶ 3B1B Gráficos & Funções",
                        "doc_url": "https://www.khanacademy.org/math/algebra",
                        "doc_label": "📖 Khan Academy Álgebra"
                    },
                    {
                        "title": "Exponenciais e logaritmos na modelagem de IA",
                        "video_url": "https://www.youtube.com/watch?v=m2MIpDrF7Es",
                        "video_label": "▶ 3B1B Número de Euler e",
                        "doc_url": "https://www.deeplearningbook.org/contents/prob.html",
                        "doc_label": "📖 Deep Learning Cap 3.10"
                    },
                    {
                        "title": "Somatório, produtório e notação matemática em papers",
                        "video_url": "https://www.youtube.com/watch?v=TgKwz5hkrvw",
                        "video_label": "▶ 3B1B Notação Matemática",
                        "doc_url": "https://mml-book.github.io/",
                        "doc_label": "📖 Guia Notação MML"
                    },
                    {
                        "title": "Geometria analítica e distância Euclidiana vs Manhattan",
                        "video_url": "https://www.youtube.com/watch?v=hl3bQySs8sM",
                        "video_label": "▶ StatQuest Métricas de Distância",
                        "doc_url": "https://mml-book.github.io/book/mml-book.pdf#page=76",
                        "doc_label": "📖 PDF MML Cap 3.2"
                    }
                ]
            ],
            [
                "Teoria da Informação & Perda",
                [
                    {
                        "title": "Entropia de Shannon (medida de incerteza da informação)",
                        "video_url": "https://www.youtube.com/watch?v=l6DKRf-fAAM",
                        "video_label": "▶ 3B1B Entropia de Shannon",
                        "doc_url": "https://www.3blue1brown.com/lessons/entropy",
                        "doc_label": "📖 3B1B Artigo Entropia"
                    },
                    {
                        "title": "Entropia Cruzada (Cross-Entropy Loss) e função Softmax",
                        "video_url": "https://www.youtube.com/watch?v=6ArSys5qHAU",
                        "video_label": "▶ StatQuest Cross-Entropy",
                        "doc_url": "https://www.deeplearningbook.org/contents/prob.html",
                        "doc_label": "📖 Deep Learning Cap 3.13"
                    },
                    {
                        "title": "Divergência de Kullback-Leibler (KL Divergence)",
                        "video_url": "https://www.youtube.com/watch?v=SxGYPqCgJWM",
                        "video_label": "▶ StatQuest KL Divergence",
                        "doc_url": "https://www.deeplearningbook.org/contents/prob.html",
                        "doc_label": "📖 Deep Learning Cap 3.13"
                    },
                    {
                        "title": "Funções de perda de regressão (MSE, MAE, Huber) e classificação",
                        "video_url": "https://www.youtube.com/watch?v=Ilg3gGewQ5U",
                        "video_label": "▶ 3B1B Funções de Perda",
                        "doc_url": "https://www.deeplearningbook.org/contents/mlp.html",
                        "doc_label": "📖 Deep Learning Cap 6.2"
                    }
                ]
            ]
        ]
    },
    {
        "t": "Módulo 5 · Matemática dos Transformers & Geometria de Embeddings",
        "d": "2 semanas",
        "tip": "💡 <b>Dica de Ouro:</b> A atenção dos Transformers é pura multiplicação de matrizes com normalização softmax. Dominar a fórmula de Scaled Dot-Product Attention te coloca no top 5% dos desenvolvedores de IA.",
        "p": "Implementar em Python com NumPy ou PyTorch a fórmula exata de Atenção: softmax((Q @ K.T) / sqrt(d_k)) @ V.",
        "r": "Canal 3Blue1Brown (Visualizing Attention & GPTs) · Paper Attention Is All You Need (arXiv:1706.03762) · Illustrated Transformer",
        "g": [
            [
                "Geometria Vetorial em IA Moderna",
                [
                    {
                        "title": "Espaços vetoriais de alta dimensão e armazenamento de fatos em LLMs",
                        "video_url": "https://www.youtube.com/watch?v=9-Jl0dxWQs8",
                        "video_label": "▶ 3B1B Fatos em LLMs",
                        "doc_url": "https://transformer-circuits.pub/2023/monosemantic-features/index.html",
                        "doc_label": "📄 Anthropic Paper Monosemantic"
                    },
                    {
                        "title": "Normalização de embeddings e geometria do espaço semântico",
                        "video_url": "https://www.youtube.com/watch?v=wjZofJX0v4M",
                        "video_label": "▶ 3B1B O que é GPT / Embeddings",
                        "doc_url": "https://jalammar.github.io/illustrated-word2vec/",
                        "doc_label": "📖 Illustrated Embeddings"
                    },
                    {
                        "title": "Projeções lineares e matrizes de pesos Query, Key e Value (W_q, W_k, W_v)",
                        "video_url": "https://www.youtube.com/watch?v=eMlx5fFNoYc",
                        "video_label": "▶ 3B1B Atenção em Transformers",
                        "doc_url": "https://jalammar.github.io/illustrated-transformer/",
                        "doc_label": "📖 Illustrated Transformer"
                    }
                ]
            ],
            [
                "Matemática da Atenção",
                [
                    {
                        "title": "Fórmula de Scaled Dot-Product Attention: softmax((Q @ K^T) / sqrt(d_k)) * V",
                        "video_url": "https://www.youtube.com/watch?v=eMlx5fFNoYc",
                        "video_label": "▶ 3B1B Fórmula da Atenção",
                        "doc_url": "https://arxiv.org/pdf/1706.03762",
                        "doc_label": "📄 Paper Attention Is All You Need"
                    },
                    {
                        "title": "Mecanismo Multi-Head Attention: divisão de dimensões e concatenação",
                        "video_url": "https://www.youtube.com/watch?v=wjZofJX0v4M",
                        "video_label": "▶ 3B1B Multi-Head Attention",
                        "doc_url": "https://arxiv.org/pdf/1706.03762#page=4",
                        "doc_label": "📄 Paper Seção 3.2"
                    },
                    {
                        "title": "Positional Encodings: funções sinusoidais e rotação vetorial (RoPE)",
                        "video_url": "https://www.youtube.com/watch?v=eMlx5fFNoYc",
                        "video_label": "▶ 3B1B Positional Embeddings",
                        "doc_url": "https://arxiv.org/pdf/2104.09864",
                        "doc_label": "📄 Paper RoFormer RoPE"
                    }
                ]
            ]
        ]
    }
]

# ---------------------------------------------------------------------------
# 3. Dados de Inglês EnglishBay (6 Módulos - 73 Vídeo-Aulas)
# ---------------------------------------------------------------------------
ing_phases = [
    {
        "t": "Módulo 1 · Fundamentos Básicos & Apresentação",
        "d": "2 a 3 semanas (1 aula/dia)",
        "tip": "💡 <b>Dica de Estudo:</b> Repita as frases em voz alta junto com o professor. Anote no seu Caderno de Anotações (📝) o vocabulário novo e as estruturas essenciais de cada aula!",
        "p": "Gravar um áudio de 1 minuto em inglês apresentando seu nome, idade, ocupação e o que você gosta de fazer.",
        "r": "Canal EnglishBay no YouTube · Caderno de Anotações integrado · Prática diária de 25-30 min",
        "g": [
            ["Apresentação & Primeiro Contato", english_playlist[:4]],
            ["Estrutura, Números & Adjetivos", english_playlist[4:7]],
            ["Gostos, Hobbies & Conversação Inicial", english_playlist[7:10]],
            ["Família, Gramática & 25 Verbos Essenciais", english_playlist[10:13]]
        ]
    },
    {
        "t": "Módulo 2 · Rotina Diária, Horas & Preposições",
        "d": "2 a 3 semanas",
        "tip": "💡 <b>Dica de Estudo:</b> Domine as preposições IN, ON, AT praticando com os horários e locais da sua rotina real de desenvolvedor.",
        "p": "Escrever um parágrafo descrevendo sua rotina matinal e noturna em inglês usando preposições e horários.",
        "r": "Canal EnglishBay no YouTube · Tabela de preposições no Caderno de Anotações",
        "g": [
            ["Família, Artigos & Rotina", english_playlist[13:16]],
            ["Pronomes & Preposições (IN, ON, AT)", english_playlist[16:19]],
            ["Frequência, Datas & Ações em Andamento", english_playlist[19:22]],
            ["Horas, Verbo Haver & 25 Adjetivos", english_playlist[22:25]]
        ]
    },
    {
        "t": "Módulo 3 · Verbos Modais, Futuro & Pronomes",
        "d": "2 semanas",
        "tip": "💡 <b>Dica de Estudo:</b> Modais como Can, Should e Must aparecem em quase todas as documentações técnicas e reuniões de trabalho.",
        "p": "Listar 5 coisas que você DEVE (must) fazer na sua transição de carreira e 5 coisas que você PODE (can) construir com IA.",
        "r": "Canal EnglishBay no YouTube · Exercícios práticos com textos e áudios",
        "g": [
            ["Capacidade (Can) & Pronomes Oblíquos", english_playlist[25:27]],
            ["Conselhos (Should), Pronomes Reflexivos & Dever (Must)", english_playlist[27:30]],
            ["Perguntas Confusas, Futuro (Will) & Advérbios", english_playlist[30:33]],
            ["Futuro (Going to), Do vs Make & Possibilidades", english_playlist[33:37]]
        ]
    },
    {
        "t": "Módulo 4 · Passado, Hábitos & Comparativos",
        "d": "2 semanas",
        "tip": "💡 <b>Dica de Estudo:</b> Memorize os 25 verbos irregulares mais comuns criando frases sobre seu dia anterior de trabalho e código.",
        "p": "Escrever sobre como era sua vida profissional há 5 anos (usando Used To e Simple Past).",
        "r": "Canal EnglishBay no YouTube · Tabela de verbos irregulares no Caderno de Anotações",
        "g": [
            ["Cortesia (Would like), Comparativos & Desejos", english_playlist[37:40]],
            ["Superlativos, Passado do To Be & Igualdade", english_playlist[40:43]],
            ["Passado Simples & 25 Verbos Irregulares", english_playlist[43:46]],
            ["Poder no Passado (Could), Pronomes & Hábitos (Used to)", english_playlist[46:49]]
        ]
    },
    {
        "t": "Módulo 5 · Estruturas Intermediárias & Conversação",
        "d": "2 semanas",
        "tip": "💡 <b>Dica de Estudo:</b> Pratique criar hipóteses com Second Conditional (\"If I had more time, I would study more IA\").",
        "p": "Simular uma entrevista técnica respondendo perguntas indiretas e falando sobre hábitos passados vs atuais.",
        "r": "Canal EnglishBay no YouTube · Roteiro de conversação no Caderno de Anotações",
        "g": [
            ["Duração de Tempo & Perguntas sem Auxiliares", english_playlist[49:51]],
            ["Hipóteses (E se...), Auxiliares & Condicionais", english_playlist[51:54]],
            ["Prefixos, Past Continuous & Sufixos", english_playlist[54:57]],
            ["Ofertas, Perguntas Indiretas, Hábitos & Quantificadores", english_playlist[57:61]]
        ]
    },
    {
        "t": "Módulo 6 · Fluência Avançada, Tempos Perfeitos & Voz Passiva",
        "d": "2 semanas",
        "tip": "💡 <b>Dica de Estudo:</b> O Present Perfect é essencial para artigos científicos e documentações (\"We have trained the model on 1B tokens\").",
        "p": "Ler a introdução do paper 'Attention is All You Need' e identificar verbos na voz passiva e no present perfect.",
        "r": "Canal EnglishBay no YouTube · Leituras de documentações técnicas em inglês",
        "g": [
            ["Present Perfect & Infinitivo vs Gerúndio", english_playlist[61:63]],
            ["Ever/Never, Verbos com Infinitivo & Present Perfect Continuous", english_playlist[63:66]],
            ["Verbos com Gerúndio, Past Perfect & Voz Passiva", english_playlist[66:69]],
            ["Third Conditional, Reported Speech, Desejos & Tag Questions", english_playlist[69:73]]
        ]
    }
]

print("Datasets prontos. Gerando páginas...")

# ---------------------------------------------------------------------------
# Estilos CSS Compartilhados
# ---------------------------------------------------------------------------
BASE_SHARED_CSS = """
:root{--bg:#f6f7f9;--card:#fff;--tx:#1b1f27;--mu:#667085;--bd:#e3e6ec;--ac:#4f46e5;--ac-hover:#4338ca;--z:#e5484d;--r:#e8a100;--e:#2fa36b;
box-sizing:border-box}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0f1218;--card:#181c25;--tx:#e8eaf0;--mu:#9aa3b2;--bd:#2a303c;--ac:#8b85ff;--ac-hover:#9d98ff;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0f1218;--card:#181c25;--tx:#e8eaf0;--mu:#9aa3b2;--bd:#2a303c;--ac:#8b85ff;--ac-hover:#9d98ff;color-scheme:dark}
html{scroll-padding-top:70px;scroll-behavior:smooth}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}

/* Topbar Sticky de Navegação */
.top-nav{
  position:sticky;
  top:0;
  z-index:100;
  background:rgba(255,255,255,.88);
  backdrop-filter:blur(10px);
  -webkit-backdrop-filter:blur(10px);
  border-bottom:1px solid var(--bd);
  transition:background .2s;
}
:root[data-theme="dark"] .top-nav, @media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .top-nav{background:rgba(24,28,37,.88)}}

.top-nav-inner{
  max-width:1440px;
  margin:0 auto;
  padding:0 22px;
  height:58px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
}
.nav-brand{
  display:flex;
  align-items:center;
  gap:8px;
  font-weight:800;
  font-size:1.05rem;
  color:var(--tx);
  text-decoration:none;
}
.nav-brand span{
  background:linear-gradient(135deg,var(--ac),#ec4899);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}
.nav-links{
  display:flex;
  align-items:center;
  gap:6px;
  overflow-x:auto;
}
.nav-links::-webkit-scrollbar{display:none}
.nav-link{
  font-size:.84rem;
  font-weight:600;
  padding:7px 12px;
  border-radius:8px;
  color:var(--mu);
  text-decoration:none;
  display:inline-flex;
  align-items:center;
  gap:6px;
  white-space:nowrap;
  transition:.15s;
}
.nav-link:hover{color:var(--tx);background:var(--bg)}
.nav-link.active{color:var(--ac);background:rgba(79,70,229,.1);font-weight:700}

.nav-right{display:flex;align-items:center;gap:8px}
.nav-status-pill{
  font-size:.72rem;
  font-weight:600;
  padding:3px 8px;
  border-radius:99px;
  background:var(--bd);
  color:var(--mu);
}
.badge-pg{background:#0064a5;color:#fff}
.badge-sq{background:#003b57;color:#fff}
.nav-theme-btn{
  font:inherit;
  border:1px solid var(--bd);
  background:var(--card);
  color:var(--tx);
  padding:5px 9px;
  border-radius:8px;
  cursor:pointer;
  font-size:.9rem;
}

/* Layout com Sidebar */
.layout{display:flex;min-height:calc(100vh - 58px)}
.sidebar{
  width:320px;
  flex-shrink:0;
  background:var(--card);
  border-right:1px solid var(--bd);
  position:sticky;
  top:58px;
  height:calc(100vh - 58px);
  overflow-y:auto;
  padding:16px 14px;
  display:flex;
  flex-direction:column;
  gap:12px;
  z-index:90;
  transition:transform .25s cubic-bezier(0.16, 1, 0.3, 1),width .25s ease;
}
.sidebar::-webkit-scrollbar{width:5px}
.sidebar::-webkit-scrollbar-thumb{background:var(--bd);border-radius:10px}

.sb-header{display:flex;align-items:center;justify-content:space-between;padding-bottom:10px;border-bottom:1px solid var(--bd)}
.sb-header-title{font-weight:750;font-size:.92rem;color:var(--tx);display:flex;align-items:center;gap:6px}
.sb-shortcuts{display:grid;grid-template-columns:1fr;gap:4px}
.sb-quick-btn{font:inherit;font-size:.78rem;padding:6px 10px;border-radius:8px;border:1px solid transparent;background:var(--bg);color:var(--tx);cursor:pointer;text-align:left;display:flex;align-items:center;gap:6px;transition:.15s}
.sb-quick-btn:hover{border-color:var(--ac);color:var(--ac)}

.sb-tree{display:flex;flex-direction:column;gap:6px;margin-top:6px}
details.sb-phase{border-radius:8px;background:transparent}
details.sb-phase summary{list-style:none;cursor:pointer;padding:7px 9px;border-radius:8px;display:flex;align-items:center;justify-content:space-between;gap:6px;font-size:.82rem;font-weight:650;color:var(--tx);transition:.15s}
details.sb-phase summary::-webkit-details-marker{display:none}
details.sb-phase summary:hover{background:var(--bg)}
details.sb-phase.active-phase summary{background:rgba(79,70,229,.1);color:var(--ac)}
.sb-phase-title{display:flex;align-items:center;gap:6px;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sb-badge-count{font-size:.7rem;padding:1px 6px;border-radius:99px;background:var(--bd);color:var(--mu);font-weight:600;flex-shrink:0}

.sb-sub-list{display:flex;flex-direction:column;gap:2px;padding:4px 0 6px 14px;margin-left:8px;border-left:1px solid var(--bd)}
.sb-sub-btn{
  font:inherit;
  font-size:.76rem;
  padding:5px 8px;
  border-radius:6px;
  border:none;
  background:transparent;
  color:var(--mu);
  text-align:left;
  cursor:pointer;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:6px;
  transition:.15s;
}
.sb-sub-btn:hover{background:var(--bg);color:var(--tx)}
.sb-sub-btn.active-group{color:var(--ac);font-weight:600;background:rgba(79,70,229,.08)}

/* Botão Mobile da Sidebar */
.sb-toggle-btn{
  position:fixed;
  bottom:20px;
  right:20px;
  z-index:95;
  background:var(--ac);
  color:#fff;
  border:none;
  border-radius:99px;
  padding:10px 18px;
  font:inherit;
  font-size:.85rem;
  font-weight:650;
  display:none;
  align-items:center;
  gap:8px;
  cursor:pointer;
  box-shadow:0 4px 18px rgba(79,70,229,.35);
}
.sb-backdrop{display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);backdrop-filter:blur(3px);z-index:85}
.sb-backdrop.active{display:block}

@media(max-width:1040px){
  .sidebar{position:fixed;left:0;top:58px;bottom:0;transform:translateX(-100%);box-shadow:6px 0 28px rgba(0,0,0,.25)}
  .sidebar.open{transform:translateX(0)}
  .sb-toggle-btn{display:flex}
}

/* Área de Conteúdo */
.content-wrapper{flex:1;min-width:0;display:flex;flex-direction:column}
main{max-width:1260px;width:100%;margin:0 auto;padding:26px 24px 90px}
.hero-head{margin-bottom:20px}
.hero-head h1{font-size:1.75rem;margin:0 0 6px;font-weight:800;letter-spacing:-.02em}
.hero-head .sub{color:var(--mu);margin:0;font-size:.95rem}

/* Animação de Scroll */
@keyframes highlightHeading {
  0% { background: transparent; }
  25% { background: rgba(79, 70, 229, 0.22); color: var(--ac); padding-left: 8px; border-radius: 6px; }
  75% { background: rgba(79, 70, 229, 0.22); color: var(--ac); padding-left: 8px; border-radius: 6px; }
  100% { background: transparent; padding-left: 0; }
}
.target-highlight {
  animation: highlightHeading 1.8s ease-in-out;
  transition: all .2s ease;
}

/* Rastreador de Metas / Gamificação */
.tracker-box{
  background:var(--card);
  border:1px solid var(--bd);
  border-radius:16px;
  padding:20px 22px;
  margin-bottom:22px;
  box-shadow:0 6px 20px rgba(0,0,0,.03);
}
.tracker-head{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px}
.tracker-title{font-size:1.02rem;font-weight:750;color:var(--tx);display:flex;align-items:center;gap:8px}
.tracker-presets{display:flex;flex-wrap:wrap;gap:6px}
.trk-btn{font:inherit;font-size:.78rem;padding:5px 12px;border-radius:99px;border:1px solid var(--bd);background:var(--bg);color:var(--tx);cursor:pointer;transition:.15s}
.trk-btn:hover{border-color:var(--ac);color:var(--ac)}
.trk-btn.active{background:var(--ac);color:#fff;border-color:var(--ac);font-weight:600}

.level-banner{background:var(--bg);border:1px solid var(--bd);border-radius:12px;padding:12px 16px;margin-bottom:14px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px}
.level-info{display:flex;align-items:center;gap:10px}
.level-icon{font-size:1.6rem}
.level-name{font-weight:750;font-size:.92rem;color:var(--tx)}
.level-desc{font-size:.78rem;color:var(--mu);margin-top:1px}
.level-xp-wrap{display:flex;flex-direction:column;align-items:flex-end;gap:4px;flex:1 1 200px}
.level-xp-text{font-size:.78rem;font-weight:600;color:var(--ac)}
.level-xp-bar{width:100%;max-width:220px;height:6px;background:var(--bd);border-radius:99px;overflow:hidden}
.level-xp-fill{height:100%;background:linear-gradient(90deg,var(--ac),#ec4899);border-radius:99px;transition:width .4s ease}

.pace-status-card{padding:12px 16px;border-radius:10px;margin-bottom:14px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;font-size:.88rem;font-weight:600}
.pace-ahead{background:rgba(47,163,107,.12);border:1px solid rgba(47,163,107,.3);color:var(--e)}
.pace-ontrack{background:rgba(79,70,229,.1);border:1px solid rgba(79,70,229,.28);color:var(--ac)}
.pace-behind{background:rgba(229,72,77,.12);border:1px solid rgba(229,72,77,.3);color:var(--z)}

.next-step-box{background:rgba(79,70,229,.06);border:1px dashed var(--ac);border-radius:12px;padding:12px 16px;margin-bottom:14px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px}
.next-step-info{display:flex;flex-direction:column;gap:2px}
.next-step-tag{font-size:.72rem;font-weight:700;letter-spacing:.05em;color:var(--ac);text-transform:uppercase}
.next-step-title{font-size:.88rem;font-weight:650;color:var(--tx)}
.next-step-btn{font:inherit;font-size:.82rem;font-weight:650;padding:8px 16px;border-radius:99px;border:none;background:var(--ac);color:#fff;cursor:pointer;display:flex;align-items:center;gap:6px;box-shadow:0 3px 12px rgba(79,70,229,.3);transition:.2s}
.next-step-btn:hover{transform:translateY(-1px);box-shadow:0 5px 16px rgba(79,70,229,.4)}

.pace-stat-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin-bottom:14px}
.pace-stat-card{background:var(--bg);border:1px solid var(--bd);border-radius:10px;padding:10px 14px;display:flex;flex-direction:column;gap:3px}
.pace-stat-num{font-size:1.15rem;font-weight:750;color:var(--tx)}
.pace-stat-sub{font-size:.74rem;color:var(--mu)}

/* Barra Global de Progresso */
.progress-card{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:14px 18px;margin-bottom:18px}
.progress-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;font-size:.86rem;font-weight:650}
.prog-bar{width:100%;height:8px;background:var(--bd);border-radius:99px;overflow:hidden;display:flex}
.p-z{background:var(--z);transition:width .3s}
.p-r{background:var(--r);transition:width .3s}
.p-e{background:var(--e);transition:width .3s}

/* Filtros e Busca */
.filter-row{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;margin-bottom:18px}
.filters{display:flex;flex-wrap:wrap;gap:6px}
.fil-btn{font:inherit;font-size:.78rem;padding:5px 12px;border-radius:99px;border:1px solid var(--bd);background:var(--card);color:var(--tx);cursor:pointer;transition:.15s}
.fil-btn:hover{border-color:var(--ac)}
.fil-btn.active{background:var(--ac);color:#fff;border-color:var(--ac);font-weight:600}
.search-input{font:inherit;font-size:.82rem;padding:6px 12px;border-radius:99px;border:1px solid var(--bd);background:var(--card);color:var(--tx);min-width:220px}
.search-input:focus{outline:none;border-color:var(--ac)}

/* Cards das Fases */
.phase-card{background:var(--card);border:1px solid var(--bd);border-radius:14px;margin-bottom:16px;overflow:hidden}
.phase-head{padding:14px 18px;background:var(--bg);border-bottom:1px solid var(--bd);display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;cursor:pointer}
.phase-title-text{font-size:1.02rem;font-weight:750;color:var(--tx);display:flex;align-items:center;gap:8px}
.phase-dur{font-size:.74rem;padding:3px 10px;border-radius:99px;background:var(--bd);color:var(--mu);font-weight:600}
.phase-body{padding:18px}
.phase-callout{padding:10px 14px;border-radius:8px;font-size:.82rem;margin-bottom:12px}
.callout-tip{background:rgba(79,70,229,.07);border-left:3px solid var(--ac);color:var(--tx)}
.callout-proj{background:rgba(47,163,107,.08);border-left:3px solid var(--e);color:var(--tx)}
.callout-res{background:var(--bg);border:1px solid var(--bd);color:var(--mu);font-size:.8rem}

.group-section{margin-top:16px}
.group-title{font-size:.88rem;font-weight:750;color:var(--ac);text-transform:uppercase;letter-spacing:.04em;margin:0 0 8px;padding-bottom:4px;border-bottom:1px solid var(--bd);display:flex;align-items:center;gap:6px}

/* Linha de Tópico / Aula */
.topic-row{
  display:flex;
  flex-wrap:wrap;
  align-items:center;
  justify-content:space-between;
  gap:8px 14px;
  padding:10px 14px;
  border-radius:10px;
  margin-bottom:6px;
  background:var(--bg);
  border:1px solid transparent;
  transition:.15s;
}
.topic-row:hover{border-color:var(--bd)}
.topic-row.status-e{background:rgba(47,163,107,.06);border-color:rgba(47,163,107,.2)}
.topic-row.status-r{background:rgba(232,161,0,.06);border-color:rgba(232,161,0,.25)}
.topic-row.status-z{background:var(--bg)}

.topic-left{
  display:flex;
  align-items:center;
  gap:10px;
  flex:1 1 280px;
  min-width:0;
}
.topic-title-text{
  font-size:.88rem;
  font-weight:550;
  color:var(--tx);
  line-height:1.45;
}
.topic-actions{
  display:flex;
  align-items:center;
  justify-content:flex-end;
  gap:6px;
  flex-shrink:0;
  flex-wrap:wrap;
  margin-left:auto;
}

/* Botões de Ação do Tópico */
.status-btn{
  font:inherit;
  font-size:.76rem;
  font-weight:650;
  padding:4px 10px;
  border-radius:99px;
  border:1px solid transparent;
  cursor:pointer;
  transition:.15s;
  display:inline-flex;
  align-items:center;
  gap:4px;
  white-space:nowrap;
}
.status-btn-z{background:rgba(229,72,77,.1);color:var(--z);border-color:rgba(229,72,77,.25)}
.status-btn-r{background:rgba(232,161,0,.12);color:var(--r);border-color:rgba(232,161,0,.35)}
.status-btn-e{background:rgba(47,163,107,.12);color:var(--e);border-color:rgba(47,163,107,.3)}

.note-btn{
  font:inherit;
  font-size:.76rem;
  padding:4px 8px;
  border-radius:6px;
  border:1px solid var(--bd);
  background:var(--card);
  color:var(--mu);
  cursor:pointer;
  display:inline-flex;
  align-items:center;
  gap:4px;
  transition:.15s;
  white-space:nowrap;
}
.note-btn:hover{color:var(--tx);border-color:var(--ac)}
.note-btn.has-notes{color:var(--ac);border-color:var(--ac);background:rgba(79,70,229,.08);font-weight:600}

.yt-btn{
  font:inherit;
  font-size:.74rem;
  font-weight:650;
  padding:4px 9px;
  border-radius:6px;
  border:none;
  background:#cc0000;
  color:#fff;
  text-decoration:none;
  display:inline-flex;
  align-items:center;
  gap:4px;
  box-shadow:0 2px 6px rgba(204,0,0,.25);
  transition:.15s;
}
.yt-btn:hover{background:#e60000;transform:translateY(-1px)}

.doc-btn{
  font:inherit;
  font-size:.74rem;
  font-weight:650;
  padding:4px 9px;
  border-radius:6px;
  border:1px solid rgba(79,70,229,.3);
  background:rgba(79,70,229,.08);
  color:var(--ac);
  text-decoration:none;
  display:inline-flex;
  align-items:center;
  gap:4px;
  transition:.15s;
  white-space:nowrap;
}
.doc-btn:hover{background:var(--ac);color:#fff;transform:translateY(-1px)}

/* =========================================================================
   MODAL DE ANOTAÇÕES (MARKDOWN, TABELAS, CÓDIGO)
   ========================================================================= */
.note-modal-overlay{
  position:fixed;
  inset:0;
  background:rgba(0,0,0,.72);
  backdrop-filter:blur(6px);
  -webkit-backdrop-filter:blur(6px);
  z-index:999;
  display:none; /* Invisível por padrão */
  align-items:center;
  justify-content:center;
  padding:16px;
  animation:noteFadeIn .2s ease;
}
.note-modal-overlay.active{
  display:flex !important;
}
.note-modal-overlay[hidden]{
  display:none !important;
}
@keyframes noteFadeIn{from{opacity:0;transform:scale(.98)}to{opacity:1;transform:scale(1)}}
.note-modal-box{
  background:var(--card);
  border:1px solid var(--bd);
  border-radius:16px;
  width:100%;
  max-width:1080px;
  height:90vh;
  max-height:860px;
  display:flex;
  flex-direction:column;
  box-shadow:0 24px 60px rgba(0,0,0,.45);
  overflow:hidden;
}
.note-modal-header{
  padding:14px 20px;
  border-bottom:1px solid var(--bd);
  display:flex;
  flex-wrap:wrap;
  align-items:center;
  justify-content:space-between;
  gap:10px;
  background:var(--card);
}
.note-header-left{display:flex;flex-direction:column;gap:2px}
.note-breadcrumb{font-size:.72rem;font-weight:600;color:var(--mu);text-transform:uppercase;letter-spacing:.04em}
.note-topic-title{font-size:1.05rem;font-weight:750;color:var(--tx);margin:0}
.note-header-right{display:flex;align-items:center;gap:10px}
.note-status-wrap{display:flex;align-items:center;gap:6px;font-size:.78rem;color:var(--mu)}
.note-status-pill{font:inherit;font-size:.76rem;font-weight:650;padding:4px 10px;border-radius:99px;border:1px solid var(--bd);background:var(--bg);color:var(--tx);cursor:pointer}
.note-date-wrap{display:flex;align-items:center;gap:6px;font-size:.78rem;color:var(--mu)}
.note-date-wrap input{font:inherit;font-size:.76rem;padding:3px 8px;border-radius:6px;border:1px solid var(--bd);background:var(--bg);color:var(--tx)}
.note-close-btn{font:inherit;font-size:1.1rem;border:none;background:transparent;color:var(--mu);cursor:pointer;padding:4px 8px;border-radius:6px}
.note-close-btn:hover{background:var(--bg);color:var(--tx)}

.note-toolbar{
  padding:8px 16px;
  background:var(--bg);
  border-bottom:1px solid var(--bd);
  display:flex;
  flex-wrap:wrap;
  align-items:center;
  justify-content:space-between;
  gap:8px;
}
.toolbar-group{display:flex;align-items:center;gap:4px;flex-wrap:wrap}
.tb-btn{font:inherit;font-size:.76rem;padding:5px 8px;border-radius:6px;border:1px solid var(--bd);background:var(--card);color:var(--tx);cursor:pointer;display:inline-flex;align-items:center;gap:4px}
.tb-btn:hover{border-color:var(--ac);color:var(--ac)}
.tb-sep{width:1px;height:18px;background:var(--bd);margin:0 2px}
.tb-select{font:inherit;font-size:.76rem;padding:4px 8px;border-radius:6px;border:1px solid var(--bd);background:var(--card);color:var(--tx)}
.toolbar-modes{display:flex;align-items:center;gap:3px}
.tb-mode-btn{font:inherit;font-size:.74rem;padding:4px 8px;border-radius:6px;border:1px solid transparent;background:transparent;color:var(--mu);cursor:pointer}
.tb-mode-btn.active{background:var(--card);border-color:var(--bd);color:var(--tx);font-weight:600}

.note-workspace{display:flex;flex:1;min-height:0;overflow:hidden}
.note-editor-pane{flex:1;display:flex;flex-direction:column;border-right:1px solid var(--bd)}
.note-editor-pane textarea{width:100%;height:100%;resize:none;border:none;outline:none;padding:16px 20px;font:14px/1.65 ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;background:transparent;color:var(--tx)}
.note-preview-pane{flex:1;overflow-y:auto;padding:18px 22px;background:var(--card)}
.preview-header{font-size:.74rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--mu);margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid var(--bd)}
.preview-body{font-size:.92rem;line-height:1.65;color:var(--tx)}

.mode-editor .note-preview-pane{display:none}
.mode-editor .note-editor-pane{border-right:none}
.mode-preview .note-editor-pane{display:none}

.note-modal-footer{
  padding:10px 18px;
  background:var(--card);
  border-top:1px solid var(--bd);
  display:flex;
  flex-wrap:wrap;
  align-items:center;
  justify-content:space-between;
  gap:10px;
}
.footer-stats{font-size:.76rem;color:var(--mu)}
.footer-sync{font-size:.76rem;color:var(--e);font-weight:600}
.footer-actions{display:flex;align-items:center;gap:8px}
.note-clear-btn{font:inherit;font-size:.78rem;padding:5px 10px;border-radius:6px;border:1px solid var(--bd);background:var(--bg);color:var(--mu);cursor:pointer}
.note-save-btn{font:inherit;font-size:.8rem;font-weight:650;padding:6px 14px;border-radius:8px;border:none;background:var(--ac);color:#fff;cursor:pointer}

/* Formatação do Preview Markdown */
.note-table-wrap{overflow-x:auto;margin:12px 0}
.note-table{width:100%;border-collapse:collapse;font-size:.85rem}
.note-table th,.note-table td{border:1px solid var(--bd);padding:8px 12px;text-align:left}
.note-table th{background:var(--bg);font-weight:700}
.note-code-block{background:var(--bg);border:1px solid var(--bd);border-radius:8px;margin:12px 0;overflow:hidden}
.code-header{display:flex;justify-content:space-between;align-items:center;padding:5px 12px;border-bottom:1px solid var(--bd);background:rgba(0,0,0,.03);font-size:.72rem;color:var(--mu)}
.copy-code-btn{font:inherit;font-size:.7rem;border:none;background:transparent;color:var(--ac);cursor:pointer}
.note-code-block pre{margin:0;padding:12px 14px;font:13px/1.55 ui-monospace,SFMono-Regular,monospace;overflow-x:auto}
.note-checklist{list-style:none;padding-left:0;margin:10px 0}
.note-todo{display:flex;align-items:center;gap:8px;margin:4px 0}
.note-todo.done{text-decoration:line-through;color:var(--mu)}
.note-quote{border-left:4px solid var(--ac);background:rgba(79,70,229,.07);padding:8px 12px;margin:10px 0;border-radius:0 6px 6px 0}
.empty-notes-hint{color:var(--mu);font-style:italic;padding:30px 10px;text-align:center}


"""

from studio_css import STUDIO_CSS
SHARED_CSS = BASE_SHARED_CSS + "\n" + STUDIO_CSS

from auth_aws_sync import AUTH_AWS_SYNC_CSS, AWS_SYNC_MODAL_HTML, CHANGE_CREDENTIALS_MODAL_HTML, AUTH_AWS_SYNC_JS
from projects_generator import generate_projects_page

print("SHARED_CSS pronto.")

from listing_generator import generate_listing_page as _gen_listing_page

def generate_listing_page(track_id, page_title, page_sub, track_icon, phases, out_path, is_english=False, shared_css=None):
    if shared_css is None:
        shared_css = SHARED_CSS
    return _gen_listing_page(
        track_id=track_id,
        page_title=page_title,
        page_sub=page_sub,
        track_icon=track_icon,
        phases=phases,
        out_path=out_path,
        shared_css=shared_css,
        is_english=is_english
    )

print("Listing page generator pronto (conectado ao listing_generator modular).")

def generate_hub_page(out_path):
    hub_css = SHARED_CSS + "\n" + AUTH_AWS_SYNC_CSS + """
/* =========================================================================
   PORTAL DE LOGIN & ACESSO RESTRITO
   ========================================================================= */
.portal-login-wrap {
  max-width: 920px;
  margin: 30px auto 80px;
  padding: 0 16px;
}
.portal-card {
  background: var(--card);
  border: 1px solid rgba(79,70,229,.35);
  border-radius: 24px;
  padding: 38px 42px;
  box-shadow: 0 20px 60px rgba(0,0,0,.15), 0 0 40px rgba(79,70,229,.08);
  text-align: center;
  position: relative;
  overflow: hidden;
}
.portal-badge {
  display: inline-block;
  background: rgba(79,70,229,.15);
  border: 1px solid rgba(79,70,229,.35);
  color: var(--ac);
  font-size: .8rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .05em;
  padding: 6px 14px;
  border-radius: 99px;
  margin-bottom: 14px;
}
.portal-title {
  font-size: 2.1rem;
  font-weight: 850;
  margin: 0 0 10px;
  color: var(--tx);
  letter-spacing: -.02em;
}
.portal-subtitle {
  font-size: 1rem;
  color: var(--mu);
  max-width: 560px;
  margin: 0 auto 28px;
  line-height: 1.55;
}
.portal-form {
  max-width: 440px;
  margin: 0 auto;
  text-align: left;
}
.portal-input-group {
  margin-bottom: 18px;
}
.portal-label {
  display: block;
  font-size: .82rem;
  font-weight: 750;
  color: var(--tx);
  margin-bottom: 6px;
}
.portal-input {
  width: 100%;
  padding: 13px 16px;
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 12px;
  color: var(--tx);
  font-size: .95rem;
  box-sizing: border-box;
  transition: all .2s;
}
.portal-input:focus {
  outline: none;
  border-color: var(--ac);
  box-shadow: 0 0 0 3px rgba(79,70,229,.18);
}
.portal-remember-row {
  margin-bottom: 22px;
}
.portal-submit-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, var(--ac), #8b5cf6);
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 1.05rem;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(79,70,229,.3);
  transition: all .2s;
}
.portal-submit-btn:hover {
  filter: brightness(1.1);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(79,70,229,.4);
}
.portal-error-msg {
  background: rgba(239,68,68,.12);
  border: 1px solid rgba(239,68,68,.3);
  color: #ef4444;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: .84rem;
  margin-bottom: 16px;
  text-align: center;
}
.portal-card-footer {
  margin-top: 32px;
  padding-top: 22px;
  border-top: 1px solid var(--bd);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
  text-align: left;
}
.portal-footer-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: .82rem;
  color: var(--mu);
  line-height: 1.45;
}
.portal-footer-item b {
  color: var(--tx);
}
.portal-preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
  margin-top: 26px;
}
.portal-preview-card {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 14px;
  padding: 16px;
  text-align: center;
}
.portal-preview-icon {
  font-size: 1.6rem;
  display: block;
  margin-bottom: 6px;
}
.portal-preview-card h4 {
  margin: 0 0 4px;
  font-size: .9rem;
  color: var(--tx);
}
.portal-preview-card p {
  margin: 0;
  font-size: .76rem;
  color: var(--mu);
  line-height: 1.4;
}

/* Banner de Nuvem Ativa no Hub */
.hub-aws-banner {
  background: linear-gradient(135deg, rgba(16,185,129,.08), rgba(255,153,0,.08));
  border: 1px solid rgba(16,185,129,.3);
  border-radius: 14px;
  padding: 14px 18px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.hub-aws-banner-left {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: .88rem;
  color: var(--tx);
}
.hub-aws-banner-left b {
  color: #10b981;
}

/* Hub Cards e Seções Específicas */
.hub-main{max-width:1260px;margin:0 auto;padding:32px 24px 100px}
.hub-hero{text-align:center;margin-bottom:34px}
.hub-hero h1{font-size:2.2rem;font-weight:850;letter-spacing:-.03em;margin:0 0 10px;background:linear-gradient(135deg,var(--tx) 30%,var(--ac));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hub-hero p{font-size:1.08rem;color:var(--mu);max-width:760px;margin:0 auto}

/* Card de Esclarecimento sobre Metas & Inglês */
.clarification-card{
  background:linear-gradient(135deg,rgba(79,70,229,.08),rgba(236,72,153,.05));
  border:1px solid rgba(79,70,229,.25);
  border-radius:18px;
  padding:24px 28px;
  margin-bottom:32px;
  box-shadow:0 8px 24px rgba(79,70,229,.06);
}
.clarification-head{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.clarification-badge{background:var(--ac);color:#fff;font-size:.76rem;font-weight:750;padding:4px 10px;border-radius:99px;text-transform:uppercase;letter-spacing:.04em}
.clarification-title{font-size:1.25rem;font-weight:800;color:var(--tx)}
.clarification-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:16px}
.clarification-col{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:16px 18px}
.clarification-col h4{margin:0 0 8px;font-size:.95rem;font-weight:750;color:var(--tx);display:flex;align-items:center;gap:6px}
.clarification-col p{margin:0;font-size:.86rem;line-height:1.55;color:var(--mu)}
.clarification-col b{color:var(--tx)}

/* =========================================================================
   VELOCÍMETRO GLOBAL E PAINEL DE METAS & RITMO
   ========================================================================= */
.speedometer-sect {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 18px;
  padding: 24px 26px;
  margin-bottom: 34px;
  box-shadow: 0 8px 30px rgba(0,0,0,.04);
  position: relative;
  overflow: hidden;
}

.speed-head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 18px;
}

.speed-title {
  font-size: 1.18rem;
  font-weight: 800;
  color: var(--tx);
  display: flex;
  align-items: center;
  gap: 8px;
}

.speed-presets-wrap {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
}

.speed-preset-btn {
  font: inherit;
  font-size: .8rem;
  font-weight: 650;
  padding: 6px 14px;
  border-radius: 99px;
  border: 1px solid var(--bd);
  background: var(--bg);
  color: var(--tx);
  cursor: pointer;
  transition: all .18s ease;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.speed-preset-btn:hover {
  border-color: var(--ac);
  color: var(--ac);
  transform: translateY(-1px);
}

.speed-preset-btn.active {
  background: var(--ac);
  border-color: var(--ac);
  color: #fff;
  box-shadow: 0 3px 12px rgba(79,70,229,.35);
}

.speed-date-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 10px 14px;
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 12px;
  margin-bottom: 16px;
  font-size: .84rem;
}

.speed-date-inputs {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
}

.speed-date-inputs label {
  color: var(--mu);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.speed-date-input {
  font: inherit;
  font-size: .82rem;
  padding: 5px 10px;
  border-radius: 8px;
  border: 1px solid var(--bd);
  background: var(--card);
  color: var(--tx);
  outline: none;
}

.speed-date-input:focus {
  border-color: var(--ac);
}

.speed-reset-btn {
  font: inherit;
  font-size: .78rem;
  font-weight: 650;
  padding: 5px 12px;
  border-radius: 8px;
  border: 1px solid var(--bd);
  background: var(--card);
  color: var(--tx);
  cursor: pointer;
  transition: .15s;
}

.speed-reset-btn:hover {
  background: var(--bd);
}

/* Card de Diagnóstico Dinâmico ao Vivo */
.speed-diagnosis-card {
  padding: 14px 18px;
  border-radius: 12px;
  margin-bottom: 18px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  font-size: .9rem;
  font-weight: 600;
  line-height: 1.5;
  transition: all .25s ease;
}

.speed-diagnosis-card.pace-ahead {
  background: rgba(47,163,107,.12);
  border: 1px solid rgba(47,163,107,.35);
  color: var(--e);
}

.speed-diagnosis-card.pace-ontrack {
  background: rgba(79,70,229,.1);
  border: 1px solid rgba(79,70,229,.3);
  color: var(--ac);
}

.speed-diagnosis-card.pace-behind {
  background: rgba(229,72,77,.12);
  border: 1px solid rgba(229,72,77,.35);
  color: var(--z);
}

.speed-diag-badge {
  font-size: .8rem;
  font-weight: 800;
  padding: 5px 12px;
  border-radius: 99px;
  background: var(--card);
  border: 1px solid currentColor;
  white-space: nowrap;
  letter-spacing: .02em;
}

/* O Medidor / Velocímetro Visual (Speedometer Gauge) */
.speed-gauge-card {
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 14px;
  padding: 18px 20px;
  margin-bottom: 18px;
}

.speed-gauge-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
}

.speed-gauge-head-title {
  font-size: .95rem;
  font-weight: 750;
  color: var(--tx);
  display: flex;
  align-items: center;
  gap: 7px;
}

.speed-gauge-multiplier {
  font-size: .86rem;
  font-weight: 850;
  padding: 4px 12px;
  border-radius: 99px;
  background: linear-gradient(135deg,rgba(79,70,229,.15),rgba(236,72,153,.15));
  color: var(--ac);
  border: 1px solid rgba(79,70,229,.3);
  letter-spacing: .02em;
}

.speed-gauge-track-wrap {
  position: relative;
  margin: 22px 0 14px;
}

.speed-gauge-bar {
  height: 16px;
  border-radius: 99px;
  background: linear-gradient(90deg, #f59e0b 0%, #10b981 38%, #06b6d4 72%, #8b5cf6 100%);
  position: relative;
  box-shadow: inset 0 2px 4px rgba(0,0,0,.22);
}

.speed-gauge-marker {
  position: absolute;
  top: -6px;
  bottom: -6px;
  width: 6px;
  background: #fff;
  border: 2px solid var(--tx);
  border-radius: 99px;
  transform: translateX(-50%);
  transition: left .5s cubic-bezier(.34,1.56,.64,1);
  box-shadow: 0 0 12px rgba(0,0,0,.35), 0 0 0 3px rgba(79,70,229,.35);
  z-index: 2;
}

.speed-gauge-marker-pin {
  position: absolute;
  top: -26px;
  left: 50%;
  transform: translateX(-50%);
  font-size: .72rem;
  font-weight: 850;
  color: var(--tx);
  background: var(--card);
  padding: 2px 8px;
  border-radius: 6px;
  border: 1px solid var(--bd);
  white-space: nowrap;
  box-shadow: 0 3px 8px rgba(0,0,0,.18);
}

.speed-gauge-scale {
  display: flex;
  justify-content: space-between;
  font-size: .72rem;
  color: var(--mu);
  font-weight: 650;
  padding: 0 4px;
}

/* Grade de Métricas de Velocidade e Cronograma */
.speed-metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}

.speed-metric-box {
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 12px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.speed-metric-lbl {
  font-size: .76rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .04em;
  color: var(--mu);
  display: flex;
  align-items: center;
  gap: 5px;
}

.speed-metric-val {
  font-size: 1.35rem;
  font-weight: 850;
  color: var(--tx);
  line-height: 1.2;
}

.speed-metric-sub {
  font-size: .76rem;
  font-weight: 600;
  color: var(--mu);
}

/* Barras Comparativas: Real vs Meta Esperada */
.comp-bars-card {
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 14px;
  padding: 16px 18px;
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comp-bar-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: .84rem;
  font-weight: 700;
  color: var(--tx);
}

.comp-bar-track {
  height: 9px;
  background: var(--bd);
  border-radius: 99px;
  overflow: hidden;
  margin-top: 5px;
}

.comp-bar-fill-real {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #06b6d4);
  border-radius: 99px;
  transition: width .4s ease;
}

.comp-bar-fill-target {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  border-radius: 99px;
  transition: width .4s ease;
}

/* Mini Radar das 3 Trilhas no Hub */
.hub-radar-card {
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 14px;
  padding: 16px 18px;
  margin-bottom: 18px;
}

.hub-radar-title {
  font-size: .92rem;
  font-weight: 750;
  color: var(--tx);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.hub-radar-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 12px;
}

.hub-radar-item {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 12px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: border-color .2s, transform .2s;
}

.hub-radar-item:hover {
  border-color: var(--ac);
  transform: translateY(-2px);
}

.hub-radar-item-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.hub-radar-name {
  font-size: .86rem;
  font-weight: 750;
  color: var(--tx);
  display: flex;
  align-items: center;
  gap: 6px;
}

.hub-radar-count {
  font-size: .78rem;
  font-weight: 700;
  color: var(--mu);
}

.hub-radar-bar {
  height: 6px;
  background: var(--bd);
  border-radius: 99px;
  overflow: hidden;
}

.hub-radar-fill {
  height: 100%;
  border-radius: 99px;
  transition: width .4s ease;
}

.hub-radar-link {
  align-self: flex-end;
  font-size: .76rem;
  font-weight: 700;
  color: var(--ac);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.hub-radar-link:hover {
  text-decoration: underline;
}

/* Próximo Passo Sugerido */
.hub-next-box {
  background: linear-gradient(135deg,rgba(79,70,229,.07),rgba(236,72,153,.05));
  border: 1px dashed var(--ac);
  border-radius: 12px;
  padding: 12px 18px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.hub-next-tag {
  font-size: .7rem;
  font-weight: 750;
  letter-spacing: .05em;
  color: var(--ac);
  text-transform: uppercase;
}

.hub-next-title {
  font-size: .88rem;
  font-weight: 700;
  color: var(--tx);
  margin-top: 2px;
}

.hub-next-action-btn {
  font: inherit;
  font-size: .82rem;
  font-weight: 750;
  padding: 8px 18px;
  border-radius: 99px;
  border: none;
  background: var(--ac);
  color: #fff;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 3px 12px rgba(79,70,229,.3);
  transition: .2s;
}

.hub-next-action-btn:hover {
  background: var(--ac-hover);
  transform: translateY(-1px);
  box-shadow: 0 5px 16px rgba(79,70,229,.4);
}

@keyframes hubPulseAnim {
  0% { box-shadow: 0 0 0 0 rgba(79,70,229,.4); }
  70% { box-shadow: 0 0 0 14px rgba(79,70,229,0); }
  100% { box-shadow: 0 0 0 0 rgba(79,70,229,0); }
}
.pulse-update {
  animation: hubPulseAnim .7s ease-out;
}

/* Grade dos 3 Cards Principais de Trilha */
.track-cards-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:22px;margin-bottom:40px}
.track-card{
  background:var(--card);
  border:1px solid var(--bd);
  border-radius:18px;
  padding:26px 24px;
  display:flex;
  flex-direction:column;
  justify-content:space-between;
  box-shadow:0 6px 22px rgba(0,0,0,.03);
  transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease;
  position:relative;
  overflow:hidden;
}
.track-card:hover{
  transform:translateY(-4px);
  box-shadow:0 12px 32px rgba(79,70,229,.12);
  border-color:var(--ac);
}
.track-card-top{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:14px}
.track-card-icon{font-size:2.2rem}
.track-badge-count{font-size:.76rem;font-weight:700;padding:4px 10px;border-radius:99px;background:var(--bg);color:var(--ac);border:1px solid var(--bd)}
.track-card-title{font-size:1.25rem;font-weight:800;color:var(--tx);margin:0 0 8px}
.track-card-desc{font-size:.88rem;color:var(--mu);line-height:1.55;margin:0 0 18px;flex:1}

.track-progress-wrap{margin-bottom:20px;padding-top:14px;border-top:1px solid var(--bd)}
.track-progress-info{display:flex;justify-content:space-between;font-size:.82rem;font-weight:650;color:var(--tx);margin-bottom:6px}
.track-progress-bar{height:7px;background:var(--bd);border-radius:99px;overflow:hidden}
.track-progress-fill{height:100%;border-radius:99px;transition:width .4s}

.track-access-btn{
  font:inherit;
  font-size:.92rem;
  font-weight:750;
  padding:12px 20px;
  border-radius:12px;
  border:none;
  background:var(--ac);
  color:#fff;
  text-decoration:none;
  text-align:center;
  display:flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  box-shadow:0 4px 14px rgba(79,70,229,.28);
  transition:.2s;
}
.track-access-btn:hover{background:var(--ac-hover);transform:scale(1.01)}

/* Contexto Global de Mercado */
.market-box{
  background:var(--card);
  border:1px solid var(--bd);
  border-radius:18px;
  padding:26px 28px;
  box-shadow:0 4px 18px rgba(0,0,0,.02);
}
.market-title{font-size:1.2rem;font-weight:800;color:var(--tx);margin:0 0 10px;display:flex;align-items:center;gap:8px}
.market-desc{font-size:.92rem;line-height:1.65;color:var(--mu);margin-bottom:18px}
.market-stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px}
.market-stat{background:var(--bg);border:1px solid var(--bd);border-radius:12px;padding:14px 16px}
.market-stat-num{font-size:1.4rem;font-weight:850;color:var(--ac);display:block;margin-bottom:3px}
.market-stat-lbl{font-size:.82rem;color:var(--tx);font-weight:600}
"""

    html_template = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Hub Central - Roteiro de Estudo do zero à IA</title>
<style>
__HUB_CSS__
</style>
</head>
<body>

<!-- TOPBAR FIXA -->
<header class="top-nav">
  <div class="top-nav-inner">
    <a href="index.html" class="nav-brand">🚀 <span>Roteiro IA</span></a>
    <nav class="nav-links" id="hub-nav-links">
      <a href="index.html" class="nav-link active">🏠 Hub Central</a>
      <a href="ia.html" class="nav-link">🤖 IA & Código</a>
      <a href="matematica.html" class="nav-link">📐 Matemática</a>
      <a href="ingles.html" class="nav-link">🇺🇸 Inglês EnglishBay</a>
      <a href="projetos.html" class="nav-link">🛠️ Projetos & Portfólio</a>
    </nav>
    <div class="nav-right">
      <div class="nav-user-dropdown-wrap" id="nav-user-wrap">
        <button class="nav-user-pill" onclick="toggleUserDropdown(event)" id="nav-auth-user" title="Menu da Conta">
          👤 <span>João Naziozeno</span> <span style="font-size:.7rem;margin-left:2px">▾</span>
        </button>
        <div class="nav-user-dropdown" id="nav-user-dropdown" hidden>
          <div class="dropdown-user-header">
            <div class="dropdown-user-name" id="dropdown-user-name">João Naziozeno</div>
            <div class="dropdown-user-email" id="dropdown-user-email">joao@roteiro.ia</div>
          </div>
          <button class="dropdown-item" onclick="openAwsSyncModal()">
            <span>☁️</span>
            <span>Sincronização AWS</span>
          </button>
          <button class="dropdown-item" onclick="openChangeCredentialsModal()">
            <span>🔑</span>
            <span>Alterar Usuário & Senha</span>
          </button>
          <div class="dropdown-divider"></div>
          <button class="dropdown-item danger" onclick="handleUserLogout()">
            <span>🔒</span>
            <span>Sair da Conta</span>
          </button>
        </div>
      </div>
      <span id="nav-db-status" class="nav-status-pill">💾 Local</span>
      <button class="nav-theme-btn" onclick="toggleTheme()" title="Alternar tema claro/escuro">🌓</button>
    </div>
  </div>
</header>

<main class="hub-main">
  <!-- ESTADO 1: TELA DE LOGIN / PORTAL DE ACESSO (QUANDO DESCONECTADO) -->
  <div id="hub-login-view" style="display:none">
    <div class="portal-login-wrap">
      <div class="portal-card">
        <div class="portal-badge">🔒 Área Restrita do Estudante</div>
        <h2 class="portal-title">Portal de Acesso · Roteiro de IA</h2>
        <p class="portal-subtitle">Faça login para desbloquear suas trilhas de estudo, anotações de código e sincronização com a nuvem AWS.</p>
        
        <form id="portal-login-form" onsubmit="handlePortalLogin(event)" class="portal-form">
          <div class="portal-input-group">
            <label class="portal-label">E-mail Cadastrado</label>
            <input type="email" id="login-input-email" class="portal-input" value="joao@roteiro.ia" required placeholder="seu-email@dominio.com">
          </div>

          <div class="portal-input-group">
            <div style="display:flex;justify-content:space-between;align-items:center">
              <label class="portal-label">Senha / PIN Master</label>
              <span style="font-size:.74rem;color:var(--mu)">PIN Inicial: <b>1234</b></span>
            </div>
            <input type="password" id="login-input-pass" class="portal-input" required placeholder="Digite sua senha ou PIN (1234)">
          </div>

          <div class="portal-remember-row">
            <label style="display:flex;align-items:center;gap:7px;cursor:pointer;font-size:.82rem;color:var(--mu);user-select:none">
              <input type="checkbox" id="login-remember-me" checked>
              <span>Lembrar meu acesso neste dispositivo (30 dias)</span>
            </label>
          </div>

          <div id="login-error-msg" class="portal-error-msg" style="display:none"></div>

          <button type="submit" class="portal-submit-btn">
            🚀 Entrar no Ecossistema de IA ➔
          </button>
        </form>

        <div class="portal-card-footer">
          <div class="portal-footer-item">
            <span>☁️</span>
            <span><b>AWS Cloud Ready:</b> Compatível com Amazon DynamoDB & Cognito Always Free Tier.</span>
          </div>
          <div class="portal-footer-item">
            <span>🛡️</span>
            <span><b>Privacidade Total:</b> Seu progresso e suas anotações ficam 100% isolados no seu perfil.</span>
          </div>
        </div>
      </div>

      <!-- PREVIEW DAS 4 TRILHAS PROTEGIDAS -->
      <div class="portal-preview-grid">
        <div class="portal-preview-card">
          <span class="portal-preview-icon">🤖</span>
          <h4>IA & Código</h4>
          <p>173 tópicos práticos em 6 fases de Python a LLMs</p>
        </div>
        <div class="portal-preview-card">
          <span class="portal-preview-icon">📐</span>
          <h4>Matemática para IA</h4>
          <p>43 tópicos aplicados de Álgebra Linear e Cálculo</p>
        </div>
        <div class="portal-preview-card">
          <span class="portal-preview-icon">🇺🇸</span>
          <h4>Inglês EnglishBay</h4>
          <p>73 vídeo-aulas da playlist oficial</p>
        </div>
        <div class="portal-preview-card">
          <span class="portal-preview-icon">🛠️</span>
          <h4>Laboratório de Projetos</h4>
          <p>6 projetos para impressionar recrutadores</p>
        </div>
      </div>
    </div>
  </div>

  <!-- ESTADO 2: CONTEÚDO AUTENTICADO DO HUB (QUANDO CONECTADO) -->
  <div id="hub-authenticated-view" style="display:none">
    <!-- HERO HEAD -->
    <section class="hub-hero">
      <h1>Hub Central de Aprendizado</h1>
      <p>Do zero absoluto até o desenvolvimento e engenharia de Inteligência Artificial moderna. Escolha uma das 4 páginas estruturadas abaixo para gerenciar seus estudos, anotações e progresso.</p>
    </section>

  <!-- =======================================================================
       PROGRESSO GLOBAL, VELOCÍMETRO & MEDIDOR DE RITMO EM TEMPO REAL
       ======================================================================= -->
  <section class="speedometer-sect" id="hub-tracker-sect">
    <!-- CABEÇALHO DO RASTREADOR & SELEÇÃO DE METAS -->
    <div class="speed-head">
      <div class="speed-title">
        <span>⚡ Velocímetro & Medidor de Ritmo Global (289 Itens no Total)</span>
      </div>
      <div class="speed-presets-wrap">
        <span style="font-size:.78rem;font-weight:700;color:var(--mu);margin-right:2px">Meta de Prazo:</span>
        <button class="speed-preset-btn" id="btn-pace-sprint" onclick="setHubPace('sprint')" title="Sprint intensivo de 4 meses">⚡ Ultra (4 meses)</button>
        <button class="speed-preset-btn active" id="btn-pace-optimistic" onclick="setHubPace('optimistic')" title="Ritmo acelerado focado de 6 meses">🚀 Otimista (6 meses)</button>
        <button class="speed-preset-btn" id="btn-pace-standard" onclick="setHubPace('standard')" title="Ritmo equilibrado sustentável de 14 meses">🎯 Equilibrado (14 meses)</button>
      </div>
    </div>

    <!-- SELETOR DE DATA DE INÍCIO & STATUS -->
    <div class="speed-date-row">
      <div class="speed-date-inputs">
        <label for="hub-start-date">📅 Data de Início da Jornada:</label>
        <input type="date" id="hub-start-date" class="speed-date-input" onchange="onStartDateChange(this.value)">
        <button class="speed-reset-btn" onclick="resetStartDateToday()" title="Redefinir data de início para hoje">Redefinir Hoje</button>
      </div>
      <div style="display:flex;align-items:center;gap:8px">
        <span class="nav-status-pill" id="global-badge" style="font-size:.78rem;padding:3px 10px">Sincronizado</span>
      </div>
    </div>

    <!-- BANNER DE PATENTE & XP GLOBAL -->
    <div class="level-banner">
      <div class="level-info">
        <div class="level-icon" id="global-icon">🚀</div>
        <div>
          <div class="level-name" id="global-rank">Iniciante Curioso</div>
          <div class="level-desc" id="global-desc">Acompanhe seu avanço em todas as 3 trilhas integradas</div>
        </div>
      </div>
      <div class="level-xp-wrap">
        <div class="level-xp-text" id="global-xp-text">0 de 289 concluídos (0%)</div>
        <div class="level-xp-bar"><div class="level-xp-fill" id="global-xp-fill" style="width:0%"></div></div>
      </div>
    </div>

    <!-- CARD DE DIAGNÓSTICO DINÂMICO AO VIVO -->
    <div class="speed-diagnosis-card pace-ontrack" id="hub-diagnosis-card">
      <div id="hub-diagnosis-text" style="flex:1">Calculando ritmo de estudo...</div>
      <span class="speed-diag-badge" id="hub-diagnosis-badge">⏱️ Calculando</span>
    </div>

    <!-- MEDIDOR VISUAL DE VELOCIDADE (SPEEDOMETER GAUGE) -->
    <div class="speed-gauge-card">
      <div class="speed-gauge-header">
        <div class="speed-gauge-head-title">
          <span>⚡ Medidor de Velocidade em Tempo Real</span>
          <span style="font-size:.78rem;color:var(--mu);font-weight:normal">(Comparação com o ritmo alvo necessário)</span>
        </div>
        <span class="speed-gauge-multiplier" id="hub-speed-multiplier">1.0x Ritmo Alvo</span>
      </div>

      <div class="speed-gauge-track-wrap">
        <div class="speed-gauge-bar">
          <div class="speed-gauge-marker" id="hub-speed-marker" style="left:40%">
            <div class="speed-gauge-marker-pin" id="hub-speed-pin">1.0x</div>
          </div>
        </div>
      </div>

      <div class="speed-gauge-scale">
        <span>0.0x (Partida)</span>
        <span>0.5x (Lento)</span>
        <span>1.0x (Meta Ideal)</span>
        <span>1.5x (Acelerado)</span>
        <span>2.0x+ (Turbo Sprint ⚡)</span>
      </div>
    </div>

    <!-- GRADE DE 4 CARDS DE MÉTRICAS -->
    <div class="speed-metrics-grid">
      <div class="speed-metric-box">
        <span class="speed-metric-lbl">⚡ Velocidade Real</span>
        <span class="speed-metric-val" id="hub-val-speed">0.0 /sem</span>
        <span class="speed-metric-sub" id="hub-sub-speed">0.0 tópicos/dia</span>
      </div>

      <div class="speed-metric-box">
        <span class="speed-metric-lbl">🎯 Velocidade Alvo</span>
        <span class="speed-metric-val" id="hub-val-target-speed">11.2 /sem</span>
        <span class="speed-metric-sub" id="hub-sub-target-speed">Meta de 6 meses (180 dias)</span>
      </div>

      <div class="speed-metric-box">
        <span class="speed-metric-lbl">📅 Previsão de Formatura</span>
        <span class="speed-metric-val" id="hub-val-forecast">--/--/----</span>
        <span class="speed-metric-sub" id="hub-sub-forecast">no seu ritmo atual</span>
      </div>

      <div class="speed-metric-box">
        <span class="speed-metric-lbl">⏳ Prazo da Meta</span>
        <span class="speed-metric-val" id="hub-val-deadline">--/--/----</span>
        <span class="speed-metric-sub" id="hub-sub-daysleft">0 dias restantes</span>
      </div>
    </div>

    <!-- BARRAS COMPARATIVAS: REAL VS ESPERADO -->
    <div class="comp-bars-card">
      <div class="comp-bar-item">
        <div class="comp-bar-head">
          <span>🟢 Seu Progresso Real Concluído:</span>
          <span id="hub-comp-txt-real">0 de 289 tópicos (0%)</span>
        </div>
        <div class="comp-bar-track">
          <div class="comp-bar-fill-real" id="hub-comp-fill-real" style="width:0%"></div>
        </div>
      </div>

      <div class="comp-bar-item">
        <div class="comp-bar-head">
          <span>🎯 Meta Esperada para Hoje (no prazo):</span>
          <span id="hub-comp-txt-target">0 de 289 tópicos (0%)</span>
        </div>
        <div class="comp-bar-track">
          <div class="comp-bar-fill-target" id="hub-comp-fill-target" style="width:0%"></div>
        </div>
      </div>
    </div>

    <!-- MINI-RADAR DAS 3 TRILHAS INTEGRADAS -->
    <div class="hub-radar-card">
      <div class="hub-radar-title">
        <span>🗺️ Radar de Conclusão por Trilha Integrada</span>
      </div>
      <div class="hub-radar-grid">
        <div class="hub-radar-item">
          <div class="hub-radar-item-top">
            <span class="hub-radar-name">🤖 IA & Código</span>
            <span class="hub-radar-count" id="radar-ia-count">0 / 173 (0%)</span>
          </div>
          <div class="hub-radar-bar">
            <div class="hub-radar-fill" id="radar-ia-fill" style="width:0%;background:var(--ac)"></div>
          </div>
          <a href="ia.html" class="hub-radar-link">Abrir Trilha de IA ➔</a>
        </div>

        <div class="hub-radar-item">
          <div class="hub-radar-item-top">
            <span class="hub-radar-name">📐 Matemática</span>
            <span class="hub-radar-count" id="radar-mat-count">0 / 43 (0%)</span>
          </div>
          <div class="hub-radar-bar">
            <div class="hub-radar-fill" id="radar-mat-fill" style="width:0%;background:#e8a100"></div>
          </div>
          <a href="matematica.html" class="hub-radar-link" style="color:#e8a100">Abrir Trilha de Matemática ➔</a>
        </div>

        <div class="hub-radar-item">
          <div class="hub-radar-item-top">
            <span class="hub-radar-name">🇺🇸 Inglês EnglishBay</span>
            <span class="hub-radar-count" id="radar-ing-count">0 / 73 (0%)</span>
          </div>
          <div class="hub-radar-bar">
            <div class="hub-radar-fill" id="radar-ing-fill" style="width:0%;background:#2fa36b"></div>
          </div>
          <a href="ingles.html" class="hub-radar-link" style="color:#2fa36b">Abrir Trilha de Inglês ➔</a>
        </div>

        <div class="hub-radar-item">
          <div class="hub-radar-item-top">
            <span class="hub-radar-name">🛠️ Projetos & Portfólio</span>
            <span class="hub-radar-count" id="radar-proj-count">0 / 6 (0%)</span>
          </div>
          <div class="hub-radar-bar">
            <div class="hub-radar-fill" id="radar-proj-fill" style="width:0%;background:#ec4899"></div>
          </div>
          <a href="projetos.html" class="hub-radar-link" style="color:#ec4899">Abrir Projetos ➔</a>
        </div>
      </div>
    </div>

    <!-- PRÓXIMO PASSO SUGERIDO -->
    <div class="hub-next-box">
      <div>
        <div class="hub-next-tag">🎯 Próximo Passo Sugerido</div>
        <div class="hub-next-title" id="hub-next-step-title">Acessar a Trilha de IA & Programação para iniciar seus estudos</div>
      </div>
      <a href="ia.html" id="hub-next-step-btn" class="hub-next-action-btn">Ir para o Tópico ➔</a>
    </div>
  </section>

  <!-- OS 4 CARDS GRANDES DE REDIRECIONAMENTO -->
  <div style="font-size:1.15rem;font-weight:800;color:var(--tx);margin-bottom:16px;display:flex;align-items:center;gap:8px">
    🎯 Suas 4 Páginas de Aprendizado & Portfólio:
  </div>

  <section class="track-cards-grid">
    <!-- CARD 1: IA & PROGRAMAÇÃO -->
    <div class="track-card">
      <div>
        <div class="track-card-top">
          <div class="track-card-icon">🤖</div>
          <span class="track-badge-count">173 Tópicos · 6 Fases</span>
        </div>
        <h3 class="track-card-title">Inteligência Artificial & Código</h3>
        <p class="track-card-desc">
          Do zero ao domínio técnico completo: Python essencial, Git, consumo de APIs, Pandas, Scikit-learn, PyTorch, Redes Neurais, Transformers, LLMs, Agentes e MLOps.
        </p>
      </div>

      <div>
        <div class="track-progress-wrap">
          <div class="track-progress-info">
            <span>Progresso em IA:</span>
            <span id="card-ia-pct">0%</span>
          </div>
          <div class="track-progress-bar">
            <div class="track-progress-fill" id="card-ia-fill" style="width:0%;background:var(--ac)"></div>
          </div>
        </div>
        <a href="ia.html" class="track-access-btn">Acessar Trilha de IA & Programação ➔</a>
      </div>
    </div>

    <!-- CARD 2: MATEMÁTICA PARA IA -->
    <div class="track-card">
      <div>
        <div class="track-card-top">
          <div class="track-card-icon">📐</div>
          <span class="track-badge-count">43 Tópicos · 5 Módulos</span>
        </div>
        <h3 class="track-card-title">Matemática Essencial para IA</h3>
        <p class="track-card-desc">
          Apenas a matemática que você realmente usa: Álgebra Linear com tensores, Cálculo com gradientes e Backpropagation, Probabilidade Bayesiana e Geometria de Embeddings.
        </p>
      </div>

      <div>
        <div class="track-progress-wrap">
          <div class="track-progress-info">
            <span>Progresso em Matemática:</span>
            <span id="card-mat-pct">0%</span>
          </div>
          <div class="track-progress-bar">
            <div class="track-progress-fill" id="card-mat-fill" style="width:0%;background:#e8a100"></div>
          </div>
        </div>
        <a href="matematica.html" class="track-access-btn" style="background:#e8a100">Acessar Trilha de Matemática ➔</a>
      </div>
    </div>

    <!-- CARD 3: INGLÊS ENGLISHBAY -->
    <div class="track-card">
      <div>
        <div class="track-card-top">
          <div class="track-card-icon">🇺🇸</div>
          <span class="track-badge-count">73 Aulas · 6 Módulos</span>
        </div>
        <h3 class="track-card-title">Curso de Inglês EnglishBay</h3>
        <p class="track-card-desc">
          Sequência completa e organizada da playlist oficial do YouTube: da apresentação pessoal e estruturas básicas até tempos perfeitos, verbos modais e voz passiva.
        </p>
      </div>

      <div>
        <div class="track-progress-wrap">
          <div class="track-progress-info">
            <span>Progresso em Inglês:</span>
            <span id="card-ing-pct">0%</span>
          </div>
          <div class="track-progress-bar">
            <div class="track-progress-fill" id="card-ing-fill" style="width:0%;background:#2fa36b"></div>
          </div>
        </div>
        <a href="ingles.html" class="track-access-btn" style="background:#2fa36b">Acessar Trilha de Inglês ➔</a>
      </div>
    </div>

    <!-- CARD 4: LABORATÓRIO DE PROJETOS & PORTFÓLIO -->
    <div class="track-card">
      <div>
        <div class="track-card-top">
          <div class="track-card-icon">🛠️</div>
          <span class="track-badge-count">6 Projetos · Práticos</span>
        </div>
        <h3 class="track-card-title">Laboratório de Projetos & Portfólio</h3>
        <p class="track-card-desc">
          Construa aplicações reais de IA para o seu currículo: CLI com APIs, Pipeline ETL com PostgreSQL, API de Machine Learning com FastAPI, Classificador CNN com PyTorch, Chatbot RAG com LangChain e Deploy em nuvem com Docker e AWS.
        </p>
      </div>

      <div>
        <div class="track-progress-wrap">
          <div class="track-progress-info">
            <span>Progresso em Projetos:</span>
            <span id="card-proj-pct">0%</span>
          </div>
          <div class="track-progress-bar">
            <div class="track-progress-fill" id="card-proj-fill" style="width:0%;background:#ec4899"></div>
          </div>
        </div>
        <a href="projetos.html" class="track-access-btn" style="background:linear-gradient(135deg,#ec4899,#8b5cf6)">Acessar Laboratório de Projetos ➔</a>
      </div>
    </div>
  </section>

  <!-- CONTEXTO GLOBAL DE MERCADO -->
  <section class="market-box">
    <div class="market-title">🗺️ O Cenário Global do Talento em IA</div>
    <div class="market-desc">
      Dados do <b>Stanford AI Index</b> e do <b>Global AI Talent Tracker</b> (Carnegie/Paulson Institute) mostram que existem hoje cerca de 150.000 a 200.000 pessoas no mundo trabalhando diretamente no desenvolvimento de ponta em IA. Quando incluímos quem cria integrações e aplicações com APIs e modelos abertos, o número salta para a casa dos milhões (mais de 5,6 milhões de repositórios ativos no GitHub e Hugging Face).
      <br><br>
      Quem domina a tríade <b>Código Python + Matemática Aplicada + Inglês Técnico</b> se posiciona imediatamente no percentil mais valorizado do mercado mundial de tecnologia.
    </div>

    <div class="market-stats-grid">
      <div class="market-stat">
        <span class="market-stat-num">34,2% a 59%</span>
        <span class="market-stat-lbl">Talentos de elite empregados nos EUA (OpenAI, Google, Anthropic, Meta)</span>
      </div>
      <div class="market-stat">
        <span class="market-stat-num">40,6%</span>
        <span class="market-stat-lbl">Origem de pesquisadores seniores na China (formação matemática de ponta)</span>
      </div>
      <div class="market-stat">
        <span class="market-stat-num">5,6 Milhões</span>
        <span class="market-stat-lbl">Projetos de IA ativos no ecossistema global do GitHub & Hugging Face</span>
      </div>
      <div class="market-stat">
        <span class="market-stat-num">289 Tópicos</span>
        <span class="market-stat-lbl">Currículo completo deste roteiro cobrindo as 3 habilidades essenciais</span>
      </div>
    </div>
  </section>
  </div> <!-- /#hub-authenticated-view -->
</main>

__AWS_SYNC_MODAL__
__CHANGE_CREDENTIALS_MODAL__

<script>
__AUTH_AWS_SYNC_JS__

function checkHubAuth() {
  const user = getLoggedInUser();
  const loginView = document.getElementById("hub-login-view");
  const authView = document.getElementById("hub-authenticated-view");
  const navUserWrap = document.getElementById("nav-user-wrap");
  const navLinks = document.getElementById("hub-nav-links");

  if (user && user.authenticated) {
    if (loginView) loginView.style.display = "none";
    if (authView) authView.style.display = "block";
    if (navUserWrap) navUserWrap.style.display = "inline-block";
    if (navLinks) navLinks.style.display = "flex";
    
    const heroH1 = document.querySelector(".hub-hero h1");
    if (heroH1) heroH1.innerHTML = `Painel do Estudante: Rumo à IA 🚀`;
    const heroP = document.querySelector(".hub-hero p");
    if (heroP) heroP.innerHTML = `Bem-vindo de volta, <b>${user.name || "João"}</b>! Suas anotações estão sincronizadas e protegidas na nuvem AWS. Escolha uma das 4 páginas abaixo:`;

    calcAndPaint();
  } else {
    if (loginView) loginView.style.display = "block";
    if (authView) authView.style.display = "none";
    if (navUserWrap) navUserWrap.style.display = "none";
    if (navLinks) navLinks.style.display = "none";
  }
}

async function handlePortalLogin(e) {
  e.preventDefault();
  const email = document.getElementById("login-input-email").value.trim();
  const pass = document.getElementById("login-input-pass").value.trim();
  const remember = document.getElementById("login-remember-me").checked;
  const errorEl = document.getElementById("login-error-msg");

  // Validação criptográfica com HASH SHA-256 e Salt
  const isValid = await validateLoginPassword(pass);

  if (isValid) {
    let userName = "João Naziozeno";
    const existing = getLoggedInUser();
    if (existing && existing.name) userName = existing.name;

    const userObj = {
      authenticated: true,
      name: userName,
      email: email || "joao@roteiro.ia",
      loginTime: Date.now(),
      provider: "aws-cognito-ready"
    };

    if (remember) {
      localStorage.setItem("roteiro_auth_user", JSON.stringify(userObj));
    } else {
      sessionStorage.setItem("roteiro_auth_user", JSON.stringify(userObj));
    }

    if (errorEl) errorEl.style.display = "none";

    const redirectUrl = sessionStorage.getItem("roteiro_redirect_after_login");
    if (redirectUrl) {
      sessionStorage.removeItem("roteiro_redirect_after_login");
      window.location.href = redirectUrl;
      return;
    }

    checkHubAuth();
    updateNavAuthUI();
  } else {
    if (errorEl) {
      errorEl.textContent = "Senha ou PIN incorreto. Use o PIN inicial: 1234 (ou sua senha configurada no perfil).";
      errorEl.style.display = "block";
    }
  }
}

const KEY = "roteiro-ia-v1";
const PACE_KEY = "roteiro-hub-pace";
const START_KEY = "roteiro-start-date";

let PR = {};
let API_BASE = "http://localhost:8000";

const HUB_PRESETS = {
  sprint: { name: "⚡ Ultra Otimista", months: 4, days: 120, label: "Meta de 4 meses (Sprint intensivo)" },
  optimistic: { name: "🚀 Otimista Acelerado", months: 6, days: 180, label: "Meta de 6 meses (Ritmo acelerado)" },
  standard: { name: "🎯 Equilibrado Sustentável", months: 14, days: 420, label: "Meta de 14 meses (Sustentável)" }
};

let currentPace = "optimistic";
let currentStartDate = "";

function loadPaceSettings() {
  try {
    const savedPace = localStorage.getItem(PACE_KEY);
    if(savedPace && HUB_PRESETS[savedPace]) currentPace = savedPace;
    
    const savedStart = localStorage.getItem(START_KEY);
    if(savedStart && /^\d{4}-\d{2}-\d{2}$/.test(savedStart)) {
      currentStartDate = savedStart;
    } else {
      currentStartDate = new Date().toISOString().slice(0, 10);
      try { localStorage.setItem(START_KEY, currentStartDate); } catch(e){}
    }
  } catch(e) {
    currentPace = "optimistic";
    currentStartDate = new Date().toISOString().slice(0, 10);
  }
}

function setHubPace(presetKey) {
  if(!HUB_PRESETS[presetKey]) return;
  currentPace = presetKey;
  try { localStorage.setItem(PACE_KEY, presetKey); } catch(e){}
  
  document.querySelectorAll(".speed-preset-btn").forEach(b => b.classList.remove("active"));
  const activeBtn = document.getElementById("btn-pace-" + presetKey);
  if(activeBtn) activeBtn.classList.add("active");
  
  triggerPulse();
  calcAndPaint();
}

function onStartDateChange(val) {
  if(!val) return;
  currentStartDate = val;
  try { localStorage.setItem(START_KEY, val); } catch(e){}
  triggerPulse();
  calcAndPaint();
}

function resetStartDateToday() {
  currentStartDate = new Date().toISOString().slice(0, 10);
  const inputEl = document.getElementById("hub-start-date");
  if(inputEl) inputEl.value = currentStartDate;
  try { localStorage.setItem(START_KEY, currentStartDate); } catch(e){}
  triggerPulse();
  calcAndPaint();
}

function triggerPulse() {
  const card = document.getElementById("hub-tracker-sect");
  if(card) {
    card.classList.remove("pulse-update");
    void card.offsetWidth;
    card.classList.add("pulse-update");
    setTimeout(() => card.classList.remove("pulse-update"), 700);
  }
}

function formatDateBR(d) {
  if(!d || isNaN(d.getTime())) return "--/--/----";
  const day = String(d.getDate()).padStart(2, "0");
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const year = d.getFullYear();
  return `${day}/${month}/${year}`;
}

function loadData(){
  try{
    const raw = localStorage.getItem(KEY);
    if(raw) PR = JSON.parse(raw);
  }catch(e){}
}

async function initSync(){
  loadData();
  loadPaceSettings();
  calcAndPaint();

  try{
    let res = await fetch(API_BASE + "/api/status", { cache: "no-store" }).catch(()=>null);
    if(!res && !window.location.origin.startsWith("http")){
      res = await fetch("http://localhost:8080/api/status", { cache: "no-store" }).catch(()=>null);
      if(res) API_BASE = "http://localhost:8080";
    }

    if(res && res.ok){
      const data = await res.json();
      const dbBadge = document.getElementById("nav-db-status");
      if(dbBadge){
        if(data.db_type === "postgres"){
          dbBadge.className = "nav-status-pill badge-pg";
          dbBadge.textContent = "🐘 PostgreSQL";
        } else {
          dbBadge.className = "nav-status-pill badge-sq";
          dbBadge.textContent = "💾 SQLite";
        }
      }

      const progRes = await fetch(API_BASE + "/api/progress?user_id=1");
      if(progRes.ok){
        const dbData = await progRes.json();
        for(const k in dbData){
          PR[k] = Object.assign({s:"z", n:"", d:""}, dbData[k]);
        }
        try{ localStorage.setItem(KEY, JSON.stringify(PR)); }catch(e){}
        calcAndPaint();
      }
    }
  }catch(e){}
}

function calcAndPaint(){
  let iaDone = 0, matDone = 0, ingDone = 0;
  let totalNotes = 0;

  for(const k in PR){
    const item = PR[k];
    if(item.s === "e"){
      if(k.startsWith("ia-")) iaDone++;
      else if(k.startsWith("mat-")) matDone++;
      else if(k.startsWith("ing-")) ingDone++;
      else iaDone++; // fallback para IDs antigos da trilha de IA
    }
    if(item.n && item.n.trim()) totalNotes++;
  }

  // Porcentagens dos Cards Individuais
  const iaPct = Math.round((iaDone / 173) * 100);
  const matPct = Math.round((matDone / 43) * 100);
  const ingPct = Math.round((ingDone / 73) * 100);

  const elIaPct = document.getElementById("card-ia-pct");
  if(elIaPct) elIaPct.textContent = `${iaPct}% (${iaDone}/173)`;
  const elIaFill = document.getElementById("card-ia-fill");
  if(elIaFill) elIaFill.style.width = `${iaPct}%`;

  const elMatPct = document.getElementById("card-mat-pct");
  if(elMatPct) elMatPct.textContent = `${matPct}% (${matDone}/43)`;
  const elMatFill = document.getElementById("card-mat-fill");
  if(elMatFill) elMatFill.style.width = `${matPct}%`;

  const elIngPct = document.getElementById("card-ing-pct");
  if(elIngPct) elIngPct.textContent = `${ingPct}% (${ingDone}/73)`;
  const elIngFill = document.getElementById("card-ing-fill");
  if(elIngFill) elIngFill.style.width = `${ingPct}%`;

  // Mini Radar das Trilhas
  const rIaCount = document.getElementById("radar-ia-count");
  if(rIaCount) rIaCount.textContent = `${iaDone} / 173 (${iaPct}%)`;
  const rIaFill = document.getElementById("radar-ia-fill");
  if(rIaFill) rIaFill.style.width = `${iaPct}%`;

  const rMatCount = document.getElementById("radar-mat-count");
  if(rMatCount) rMatCount.textContent = `${matDone} / 43 (${matPct}%)`;
  const rMatFill = document.getElementById("radar-mat-fill");
  if(rMatFill) rMatFill.style.width = `${matPct}%`;

  const rIngCount = document.getElementById("radar-ing-count");
  if(rIngCount) rIngCount.textContent = `${ingDone} / 73 (${ingPct}%)`;
  const rIngFill = document.getElementById("radar-ing-fill");
  if(rIngFill) rIngFill.style.width = `${ingPct}%`;

  // Projetos do Laboratório
  let projDone = 0;
  const totalProj = 6;
  try {
    const pList = JSON.parse(localStorage.getItem("roteiro_portfolio_projects") || "[]");
    if (pList && pList.length > 0) {
      projDone = pList.filter(x => x.status === "done").length;
    }
  } catch(e) {}
  const projPct = Math.round((projDone / totalProj) * 100);

  const elProjPct = document.getElementById("card-proj-pct");
  if(elProjPct) elProjPct.textContent = `${projPct}% (${projDone}/${totalProj})`;
  const elProjFill = document.getElementById("card-proj-fill");
  if(elProjFill) elProjFill.style.width = `${projPct}%`;

  const rProjCount = document.getElementById("radar-proj-count");
  if(rProjCount) rProjCount.textContent = `${projDone} / ${totalProj} (${projPct}%)`;
  const rProjFill = document.getElementById("radar-proj-fill");
  if(rProjFill) rProjFill.style.width = `${projPct}%`;

  // Total Global (289 tópicos)
  const totalDone = iaDone + matDone + ingDone;
  const globalPct = Math.round((totalDone / 289) * 100);

  const elGlobalXpText = document.getElementById("global-xp-text");
  if(elGlobalXpText) elGlobalXpText.textContent = `${totalDone} de 289 concluídos (${globalPct}%)`;
  const elGlobalXpFill = document.getElementById("global-xp-fill");
  if(elGlobalXpFill) elGlobalXpFill.style.width = `${globalPct}%`;

  const rankEl = document.getElementById("global-rank");
  const descEl = document.getElementById("global-desc");
  const iconEl = document.getElementById("global-icon");

  if(globalPct >= 100){
    if(iconEl) iconEl.textContent = "👑";
    if(rankEl) rankEl.textContent = "Mestre Supremo em IA";
    if(descEl) descEl.textContent = "Currículo 100% concluído em Código, Matemática e Inglês!";
  } else if(globalPct >= 70){
    if(iconEl) iconEl.textContent = "🏆";
    if(rankEl) rankEl.textContent = "Engenheiro de IA Avançado";
    if(descEl) descEl.textContent = "Grande domínio prático e pronto para posições sênior.";
  } else if(globalPct >= 40){
    if(iconEl) iconEl.textContent = "⚡";
    if(rankEl) rankEl.textContent = "Desenvolvedor & Praticante";
    if(descEl) descEl.textContent = "Construindo modelos e conectando componentes reais.";
  } else if(globalPct >= 15){
    if(iconEl) iconEl.textContent = "🔥";
    if(rankEl) rankEl.textContent = "Estudante Focado";
    if(descEl) descEl.textContent = "Ganhando tração consistente nas 3 trilhas.";
  } else {
    if(iconEl) iconEl.textContent = "🌱";
    if(rankEl) rankEl.textContent = "Iniciante Curioso";
    if(descEl) descEl.textContent = "Dando os primeiros passos do zero absoluto.";
  }

  // Sincronizar input de data
  const sInput = document.getElementById("hub-start-date");
  if(sInput && !sInput.value) sInput.value = currentStartDate;

  // Botões de Preset
  document.querySelectorAll(".speed-preset-btn").forEach(b => b.classList.remove("active"));
  const curBtn = document.getElementById("btn-pace-" + currentPace);
  if(curBtn) curBtn.classList.add("active");

  // =========================================================================
  // CÁLCULO MATEMÁTICO DO VELOCÍMETRO E CRONOGRAMA
  // =========================================================================
  const preset = HUB_PRESETS[currentPace] || HUB_PRESETS.optimistic;
  const startMs = new Date(currentStartDate + "T00:00:00").getTime();
  const nowMs = Date.now();
  const elapsedDays = Math.max(1, Math.round((nowMs - startMs) / 86400000));
  const elapsedWeeks = Math.max(0.14, elapsedDays / 7);

  // Meta de velocidade
  const targetDays = preset.days;
  const targetWeeks = targetDays / 7;
  const targetSpeedPerWeek = 289 / targetWeeks;
  const targetSpeedPerDay = 289 / targetDays;

  // Velocidade real atual
  const realSpeedPerWeek = totalDone / elapsedWeeks;
  const realSpeedPerDay = totalDone / elapsedDays;

  // Tópicos esperados para hoje
  const expectedDoneToday = Math.min(289, Math.round(targetSpeedPerDay * elapsedDays));
  const diffTopics = totalDone - expectedDoneToday;
  const diffDays = Math.round(diffTopics / targetSpeedPerDay);

  // Data limite da meta selecionada
  const targetDeadlineDate = new Date(startMs + targetDays * 86400000);
  const daysRemaining = Math.max(0, Math.round((targetDeadlineDate.getTime() - nowMs) / 86400000));

  // Previsão de conclusão no ritmo atual
  let forecastDate = null;
  let forecastSub = "";
  if(totalDone === 0){
    forecastDate = targetDeadlineDate;
    forecastSub = "Aguardando primeiro tópico concluído";
  } else {
    const remainingTopics = 289 - totalDone;
    const daysToFinish = Math.round(remainingTopics / Math.max(0.05, realSpeedPerDay));
    forecastDate = new Date(nowMs + daysToFinish * 86400000);
    const diffForecastDays = Math.round((targetDeadlineDate.getTime() - forecastDate.getTime()) / 86400000);
    if(diffForecastDays >= 0){
      forecastSub = `🚀 ${diffForecastDays} dias antes do prazo!`;
    } else {
      forecastSub = `⚠️ ${Math.abs(diffForecastDays)} dias além do prazo`;
    }
  }

  // Preencher os 4 Cards de Métricas
  const elValSpeed = document.getElementById("hub-val-speed");
  const elSubSpeed = document.getElementById("hub-sub-speed");
  if(elValSpeed) elValSpeed.textContent = `${realSpeedPerWeek.toFixed(1)} /sem`;
  if(elSubSpeed) elSubSpeed.textContent = `${realSpeedPerDay.toFixed(1)} tópicos/dia (Dia ${elapsedDays})`;

  const elValTargetSpeed = document.getElementById("hub-val-target-speed");
  const elSubTargetSpeed = document.getElementById("hub-sub-target-speed");
  if(elValTargetSpeed) elValTargetSpeed.textContent = `${targetSpeedPerWeek.toFixed(1)} /sem`;
  if(elSubTargetSpeed) elSubTargetSpeed.textContent = preset.label;

  const elValForecast = document.getElementById("hub-val-forecast");
  const elSubForecast = document.getElementById("hub-sub-forecast");
  if(elValForecast) elValForecast.textContent = formatDateBR(forecastDate);
  if(elSubForecast) elSubForecast.textContent = forecastSub;

  const elValDeadline = document.getElementById("hub-val-deadline");
  const elSubDaysLeft = document.getElementById("hub-sub-daysleft");
  if(elValDeadline) elValDeadline.textContent = formatDateBR(targetDeadlineDate);
  if(elSubDaysLeft) elSubDaysLeft.textContent = `${daysRemaining} dias restantes`;

  // Velocímetro Visual (Speedometer Gauge)
  let speedRatio = 0;
  if(totalDone > 0 && targetSpeedPerWeek > 0){
    speedRatio = realSpeedPerWeek / targetSpeedPerWeek;
  }
  
  // Marker position: escala de 0.0x a 2.5x (1.0x fica em 40%)
  const markerPct = Math.min(97, Math.max(3, Math.round((speedRatio / 2.5) * 100)));
  const markerEl = document.getElementById("hub-speed-marker");
  const pinEl = document.getElementById("hub-speed-pin");
  const multiplierEl = document.getElementById("hub-speed-multiplier");

  if(markerEl) markerEl.style.left = `${markerPct}%`;
  if(pinEl) pinEl.textContent = `${speedRatio.toFixed(1)}x`;

  if(multiplierEl){
    if(totalDone === 0){
      multiplierEl.textContent = "0.0x · Ponto de Partida";
    } else if(speedRatio >= 1.3){
      multiplierEl.textContent = `⚡ ${speedRatio.toFixed(1)}x do Ritmo Alvo · TURBO SPRINT!`;
    } else if(speedRatio >= 0.9){
      multiplierEl.textContent = `🎯 ${speedRatio.toFixed(1)}x do Ritmo Alvo · NA META IDEAL`;
    } else {
      multiplierEl.textContent = `🟡 ${speedRatio.toFixed(1)}x do Ritmo Alvo · RITMO MODERADO`;
    }
  }

  // Diagnóstico Dinâmico ao Vivo (Card & Badge)
  const diagCard = document.getElementById("hub-diagnosis-card");
  const diagText = document.getElementById("hub-diagnosis-text");
  const diagBadge = document.getElementById("hub-diagnosis-badge");

  if(diagCard && diagText && diagBadge){
    if(totalDone === 0){
      diagCard.className = "speed-diagnosis-card pace-ontrack";
      diagBadge.textContent = "🚀 Pronto para a Largada";
      diagText.innerHTML = `Você está no <b>Dia ${elapsedDays}</b>! Marque seus tópicos estudados em uma das 3 trilhas abaixo para começar a calibrar seu velocímetro em tempo real.`;
    } else if(diffTopics >= 2){
      diagCard.className = "speed-diagnosis-card pace-ahead";
      diagBadge.textContent = `🟢 ADIANTADO (+${diffTopics} TÓPICOS · +${diffDays} DIAS)`;
      diagText.innerHTML = `Ritmo Espetacular! Você está <b>${diffTopics} tópicos à frente</b> da sua meta para a data de hoje (+${diffDays} dias adiantado). No ritmo de <b>${realSpeedPerWeek.toFixed(1)} tópicos/semana</b>, você alcançará o domínio de IA antes do planejado!`;
    } else if(diffTopics >= -2){
      diagCard.className = "speed-diagnosis-card pace-ontrack";
      diagBadge.textContent = "🔵 NO PRAZO IDEAL (Ritmo Perfeito)";
      diagText.innerHTML = `Excelente consistência! Seu estudo está <b>rigorosamente no cronograma</b> da sua meta (${preset.name}). Mantenha esse ritmo para se formar em <b>${formatDateBR(targetDeadlineDate)}</b>.`;
    } else {
      const behind = Math.abs(diffTopics);
      diagCard.className = "speed-diagnosis-card pace-behind";
      diagBadge.textContent = `🟡 RITMO MODERADO (-${behind} TÓPICOS)`;
      diagText.innerHTML = `Atenção à meta: Você está <b>${behind} tópicos atrás</b> do planejado para hoje. Aumente um pouco a carga de estudo nesta semana para recolocar o velocímetro na zona verde!`;
    }
  }

  // Barras Comparativas: Real vs Esperado
  const compTxtReal = document.getElementById("hub-comp-txt-real");
  const compFillReal = document.getElementById("hub-comp-fill-real");
  const compTxtTarget = document.getElementById("hub-comp-txt-target");
  const compFillTarget = document.getElementById("hub-comp-fill-target");

  const expectedPct = Math.min(100, Math.round((expectedDoneToday / 289) * 100));

  if(compTxtReal) compTxtReal.textContent = `${totalDone} de 289 tópicos (${globalPct}%)`;
  if(compFillReal) compFillReal.style.width = `${globalPct}%`;

  if(compTxtTarget) compTxtTarget.textContent = `${expectedDoneToday} de 289 tópicos (${expectedPct}%)`;
  if(compFillTarget) compFillTarget.style.width = `${expectedPct}%`;

  // Próximo Passo Sugerido
  const nextTitle = document.getElementById("hub-next-step-title");
  const nextBtn = document.getElementById("hub-next-step-btn");
  if(nextTitle && nextBtn){
    if(iaDone === 0){
      nextTitle.textContent = "Iniciar os Fundamentos na Trilha de IA & Código (Python essencial e lógica)";
      nextBtn.href = "ia.html";
      nextBtn.textContent = "Acessar IA & Código ➔";
    } else if(matDone === 0){
      nextTitle.textContent = "Iniciar a Trilha de Matemática Essencial para IA (Módulo 1: Álgebra Linear)";
      nextBtn.href = "matematica.html";
      nextBtn.textContent = "Acessar Matemática ➔";
    } else if(ingDone === 0){
      nextTitle.textContent = "Iniciar a Trilha de Inglês EnglishBay (Aula 1 da Playlist Oficial)";
      nextBtn.href = "ingles.html";
      nextBtn.textContent = "Acessar Inglês ➔";
    } else {
      if(iaPct <= matPct && iaPct <= ingPct){
        nextTitle.textContent = `Continuar Trilha de IA & Programação (${iaDone}/173 concluídos · ${iaPct}%)`;
        nextBtn.href = "ia.html";
        nextBtn.textContent = "Ir para Trilha de IA ➔";
      } else if(matPct <= ingPct){
        nextTitle.textContent = `Continuar Trilha de Matemática para IA (${matDone}/43 concluídos · ${matPct}%)`;
        nextBtn.href = "matematica.html";
        nextBtn.textContent = "Ir para Matemática ➔";
      } else {
        nextTitle.textContent = `Continuar Curso de Inglês EnglishBay (${ingDone}/73 concluídos · ${ingPct}%)`;
        nextBtn.href = "ingles.html";
        nextBtn.textContent = "Ir para Inglês ➔";
      }
    }
  }
}

function toggleTheme(){
  const html = document.documentElement;
  const isDark = html.getAttribute("data-theme") === "dark" || (!html.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
  const next = isDark ? "light" : "dark";
  html.setAttribute("data-theme", next);
  try{ localStorage.setItem("roteiro-theme", next); }catch(e){}
}

try{
  const savedTheme = localStorage.getItem("roteiro-theme");
  if(savedTheme) document.documentElement.setAttribute("data-theme", savedTheme);
}catch(e){}

window.addEventListener("DOMContentLoaded", () => {
  initSync();
  checkHubAuth();
});
</script>
</body>
</html>
"""

    html = (html_template
        .replace("__HUB_CSS__", hub_css)
        .replace("__AWS_SYNC_MODAL__", AWS_SYNC_MODAL_HTML)
        .replace("__CHANGE_CREDENTIALS_MODAL__", CHANGE_CREDENTIALS_MODAL_HTML)
        .replace("__AUTH_AWS_SYNC_JS__", AUTH_AWS_SYNC_JS)
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Gerado: {out_path} (Hub Central)")

# ---------------------------------------------------------------------------
# Executar a Geração de Todos os Arquivos do Ecossistema
# ---------------------------------------------------------------------------
out_ia = "/mnt/c/Users/joao1/Desktop/Roteiro/ia.html"
out_mat = "/mnt/c/Users/joao1/Desktop/Roteiro/matematica.html"
out_ing = "/mnt/c/Users/joao1/Desktop/Roteiro/ingles.html"
out_proj = "/mnt/c/Users/joao1/Desktop/Roteiro/projetos.html"
out_hub = "/mnt/c/Users/joao1/Desktop/Roteiro/index.html"
out_mirror = "/mnt/c/Users/joao1/Desktop/Roteiro/Roteiro de Estudo_ do zero à IA.html"

generate_listing_page(
    track_id="ia",
    page_title="Inteligência Artificial & Programação Python",
    page_sub="Do zero aos fundamentos de Python, Engenharia de Dados, Scikit-learn, PyTorch, Transformers, LLMs, Agentes e MLOps",
    track_icon="🤖",
    phases=ia_phases,
    out_path=out_ia,
    is_english=False
)

generate_listing_page(
    track_id="mat",
    page_title="Matemática Essencial para IA",
    page_sub="Álgebra Linear, Tensores, Cálculo Diferencial, Gradientes, Backpropagation, Probabilidade Bayesiana e Matemática dos Transformers",
    track_icon="📐",
    phases=mat_phases,
    out_path=out_mat,
    is_english=False
)

generate_listing_page(
    track_id="ing",
    page_title="Curso de Inglês EnglishBay (Playlist Oficial)",
    page_sub="Sequência completa de 73 vídeo-aulas da playlist oficial com links diretos para o YouTube, anotações de vocabulário e exercícios",
    track_icon="🇺🇸",
    phases=ing_phases,
    out_path=out_ing,
    is_english=True
)

generate_projects_page(out_proj, SHARED_CSS)

generate_hub_page(out_hub)
generate_hub_page(out_mirror)

print("\n🚀 Todos os arquivos do ecossistema gerados com sucesso!")
