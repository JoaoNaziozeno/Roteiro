# -*- coding: utf-8 -*-
"""
Gerador de dados completos e enriquecidos para as 6 fases da trilha de IA & Código (173 tópicos).
Inclui vídeo aulas do Gustavo Guanabara (Curso em Vídeo) na Fase 1 e materiais de ponta nas Fases 2 a 6.
"""

def get_enriched_ia_phases():
    return [
        {
            "t": "Fase 1 · Fundamentos de programação com Python",
            "d": "2 a 3 meses",
            "tip": "💡 <b>Dica de Ouro:</b> Não pule a Fase 1! Quem tenta ir direto para IA sem uma base sólida em Python costuma travar mais tarde. O professor Gustavo Guanabara (Curso em Vídeo) possui a melhor didática em português para criar intimidade real com código, terminal e estruturas.",
            "p": "Um programa em Python que consome uma API pública (previsão do tempo, filmes, cotações) via requests/JSON e exibe os dados tratados e organizados no terminal.",
            "r": "Curso em Vídeo (Gustavo Guanabara, Python 3 Mundos 1, 2 e 3 + Git/GitHub) · CS50P Harvard · Livro Automate the Boring Stuff with Python",
            "g": [
                [
                    "Base da linguagem",
                    [
                        {
                            "title": "Instalar Python e usar o terminal",
                            "video_url": "https://www.youtube.com/watch?v=S9uPNppGsGo",
                            "video_label": "▶ Guanabara Python #01/03",
                            "doc_url": "https://docs.python.org/pt-br/3/using/index.html",
                            "doc_label": "📖 Docs Instalação Python"
                        },
                        {
                            "title": "Variáveis e tipos (int, float, str, bool)",
                            "video_url": "https://www.youtube.com/watch?v=hdDHg1p3YVc",
                            "video_label": "▶ Guanabara Python #06",
                            "doc_url": "https://docs.python.org/pt-br/3/library/stdtypes.html",
                            "doc_label": "📖 Docs Tipos Python"
                        },
                        {
                            "title": "Entrada e saída de dados",
                            "video_url": "https://www.youtube.com/watch?v=nIHq1MtJaKs",
                            "video_label": "▶ Guanabara Python #04 - Entrada & Saída",
                            "doc_url": "https://docs.python.org/pt-br/3/tutorial/inputoutput.html",
                            "doc_label": "📖 Docs Entrada/Saída"
                        },
                        {
                            "title": "Condicionais (if, elif, else)",
                            "video_url": "https://www.youtube.com/watch?v=K10u3XIf1-Q",
                            "video_label": "▶ Guanabara Python #10/12",
                            "doc_url": "https://docs.python.org/pt-br/3/tutorial/controlflow.html#if-statements",
                            "doc_label": "📖 Docs Condicionais"
                        },
                        {
                            "title": "Laços (for, while)",
                            "video_url": "https://www.youtube.com/watch?v=cL4YDtFnCt4",
                            "video_label": "▶ Guanabara Python #13 · for",
                            "doc_url": "https://docs.python.org/pt-br/3/tutorial/controlflow.html#for-statements",
                            "doc_label": "📖 Docs Laços for/while"
                        },
                        {
                            "title": "Funções, parâmetros e retorno",
                            "video_url": "https://www.youtube.com/watch?v=ezfr9d7wd_k",
                            "video_label": "▶ Guanabara Python #20/21",
                            "doc_url": "https://docs.python.org/pt-br/3/tutorial/controlflow.html#defining-functions",
                            "doc_label": "📖 Docs Funções"
                        }
                    ]
                ],
                [
                    "Estruturas de dados",
                    [
                        {
                            "title": "Listas e fatiamento",
                            "video_url": "https://www.youtube.com/watch?v=N1hTsbW50eM",
                            "video_label": "▶ Guanabara Python #17 · Listas",
                            "doc_url": "https://docs.python.org/pt-br/3/tutorial/datastructures.html#more-on-lists",
                            "doc_label": "📖 Docs Listas e Métodos"
                        },
                        {
                            "title": "Dicionários",
                            "video_url": "https://www.youtube.com/watch?v=ZWj8o692qGY",
                            "video_label": "▶ Guanabara Python #19",
                            "doc_url": "https://docs.python.org/pt-br/3/tutorial/datastructures.html#dictionaries",
                            "doc_label": "📖 Docs Dicionários"
                        },
                        {
                            "title": "Tuplas e conjuntos",
                            "video_url": "https://www.youtube.com/watch?v=0LB3FSfjvao",
                            "video_label": "▶ Guanabara Python #16",
                            "doc_url": "https://docs.python.org/pt-br/3/tutorial/datastructures.html#tuples-and-sequences",
                            "doc_label": "📖 Docs Tuplas & Sets"
                        },
                        {
                            "title": "List comprehension",
                            "video_url": "https://www.youtube.com/watch?v=M2zL6LnQwkw",
                            "video_label": "▶ Hashtag · List Comprehension",
                            "doc_url": "https://docs.python.org/pt-br/3/tutorial/datastructures.html#list-comprehensions",
                            "doc_label": "📖 Docs List Comprehensions"
                        }
                    ]
                ],
                [
                    "Programação intermediária",
                    [
                        {
                            "title": "Orientação a objetos (classes, métodos, herança)",
                            "video_url": "https://www.youtube.com/playlist?list=PLHz_AreHm4dkqe2aR0tQK74m8SFe-aGsY",
                            "video_label": "▶ Guanabara POO #01-#05",
                            "doc_url": "https://docs.python.org/pt-br/3/tutorial/classes.html",
                            "doc_label": "📖 Docs POO Python"
                        },
                        {
                            "title": "Módulos e pacotes",
                            "video_url": "https://www.youtube.com/watch?v=s3r8_Aug4y8",
                            "video_label": "▶ Guanabara Python #22 · Módulos e Pacotes",
                            "doc_url": "https://docs.python.org/pt-br/3/tutorial/modules.html",
                            "doc_label": "📖 Docs Módulos & Pacotes"
                        },
                        {
                            "title": "Arquivos (ler e escrever)",
                            "video_url": "https://www.youtube.com/watch?v=bfTFe6bKLXk",
                            "video_label": "▶ Guanabara Exercício #115b · Arquivos",
                            "doc_url": "https://docs.python.org/pt-br/3/tutorial/inputoutput.html#reading-and-writing-files",
                            "doc_label": "📖 Docs Arquivos I/O"
                        },
                        {
                            "title": "Tratamento de erros (try/except)",
                            "video_url": "https://www.youtube.com/watch?v=xz2B3bfNjEk",
                            "video_label": "▶ Guanabara Python #23 · Erros e Exceções",
                            "doc_url": "https://docs.python.org/pt-br/3/tutorial/errors.html",
                            "doc_label": "📖 Docs Try/Except"
                        },
                        {
                            "title": "Ambientes virtuais e pip",
                            "video_url": "https://www.youtube.com/watch?v=m1TYpvIYm74",
                            "video_label": "▶ Otávio Miranda · venv e pip",
                            "doc_url": "https://docs.python.org/pt-br/3/tutorial/venv.html",
                            "doc_label": "📖 Docs Ambientes Virtuais"
                        }
                    ]
                ],
                [
                    "Ferramentas",
                    [
                        {
                            "title": "Git: commit, branch, merge",
                            "video_url": "https://www.youtube.com/watch?v=6Czd1Yetaac",
                            "video_label": "▶ Guanabara Git #01-#06",
                            "doc_url": "https://git-scm.com/book/pt-br/v2",
                            "doc_label": "📖 Pro Git Livro Oficial"
                        },
                        {
                            "title": "GitHub: repositórios e README",
                            "video_url": "https://www.youtube.com/watch?v=5BYm7UdCrX0",
                            "video_label": "▶ Guanabara Git · Primeiro repositório",
                            "doc_url": "https://docs.github.com/pt/get-started",
                            "doc_label": "📖 Docs GitHub Começando"
                        },
                        {
                            "title": "Consumir APIs com requests e JSON",
                            "video_url": "https://www.youtube.com/watch?v=IdviYZIQLlA",
                            "video_label": "▶ Hashtag · Biblioteca Requests",
                            "doc_url": "https://requests.readthedocs.io/en/latest/",
                            "doc_label": "📖 Docs Requests Oficial"
                        }
                    ]
                ],
                [
                    "Boas práticas",
                    [
                        {
                            "title": "Estilo de código PEP 8",
                            "video_url": "https://www.youtube.com/watch?v=wDl1f4uLlHo",
                            "video_label": "▶ Hashtag · PEP 8",
                            "doc_url": "https://peps.python.org/pep-0008/",
                            "doc_label": "📖 Guia Oficial PEP 8"
                        },
                        {
                            "title": "Docstrings e comentários",
                            "video_url": "https://www.youtube.com/watch?v=XgPLNNy3qgI",
                            "video_label": "▶ Universo Discreto · Comentários e Docstrings",
                            "doc_url": "https://peps.python.org/pep-0257/",
                            "doc_label": "📖 Docs PEP 257 Docstrings"
                        },
                        {
                            "title": "Depuração (debug) e leitura de erros",
                            "video_url": "https://www.youtube.com/watch?v=ElRd0cbXIv4",
                            "video_label": "▶ Debugging no VS Code",
                            "doc_url": "https://docs.python.org/pt-br/3/library/pdb.html",
                            "doc_label": "📖 Docs Python Debugger"
                        },
                        {
                            "title": "Testes simples com pytest",
                            "video_url": "https://www.youtube.com/watch?v=pZvhZ-Lr-PE",
                            "video_label": "▶ Eduardo Mendes · Testes unitários",
                            "doc_url": "https://docs.pytest.org/en/latest/",
                            "doc_label": "📖 Docs Pytest Oficial"
                        },
                        {
                            "title": "Lambda, map e filter",
                            "video_url": "https://www.youtube.com/watch?v=xmMXULd0dxc",
                            "video_label": "▶ Hashtag · Funções Lambda",
                            "doc_url": "https://docs.python.org/pt-br/3/tutorial/controlflow.html#lambda-expressions",
                            "doc_label": "📖 Docs Expressões Lambda"
                        },
                        {
                            "title": "Geradores e iteradores",
                            "video_url": "https://www.youtube.com/watch?v=tmeKsb2Fras",
                            "video_label": "▶ Generators & Yield",
                            "doc_url": "https://docs.python.org/pt-br/3/howto/functional.html#generators",
                            "doc_label": "📖 Docs Generators Howto"
                        },
                        {
                            "title": "Decoradores (noção)",
                            "video_url": "https://www.youtube.com/watch?v=FsAPt_9Bf3U",
                            "video_label": "▶ Decorators Desmistificados",
                            "doc_url": "https://peps.python.org/pep-0318/",
                            "doc_label": "📖 Docs PEP 318 Decorators"
                        }
                    ]
                ],
                [
                    "Bibliotecas úteis",
                    [
                        {
                            "title": "datetime",
                            "video_url": "https://www.youtube.com/watch?v=A7S_RwWcrK0",
                            "video_label": "▶ Hashtag · Biblioteca datetime",
                            "doc_url": "https://docs.python.org/pt-br/3/library/datetime.html",
                            "doc_label": "📖 Docs datetime Oficial"
                        },
                        {
                            "title": "os e pathlib",
                            "video_url": "https://www.youtube.com/watch?v=T17BTNKBeJY",
                            "video_label": "▶ Otávio Miranda · pathlib",
                            "doc_url": "https://docs.python.org/pt-br/3/library/pathlib.html",
                            "doc_label": "📖 Docs pathlib Oficial"
                        },
                        {
                            "title": "json e csv",
                            "video_url": "https://www.youtube.com/watch?v=9N6a-VLBa2I",
                            "video_label": "▶ Arquivos JSON e CSV",
                            "doc_url": "https://docs.python.org/pt-br/3/library/json.html",
                            "doc_label": "📖 Docs json & csv"
                        },
                        {
                            "title": "Expressões regulares (re)",
                            "video_url": "https://www.youtube.com/watch?v=K8L6KVGG-7o",
                            "video_label": "▶ Regex em Python do Zero",
                            "doc_url": "https://docs.python.org/pt-br/3/library/re.html",
                            "doc_label": "📖 Docs Regex Oficial"
                        },
                        {
                            "title": "Web scraping com BeautifulSoup",
                            "video_url": "https://www.youtube.com/watch?v=WzUPnQwSQyk",
                            "video_label": "▶ Hashtag · BeautifulSoup",
                            "doc_url": "https://crummy.com/software/BeautifulSoup/bs4/doc/",
                            "doc_label": "📖 Docs BeautifulSoup4"
                        }
                    ]
                ],
                [
                    "Prática",
                    [
                        {
                            "title": "30 exercícios (Beecrowd, HackerRank, Exercism)",
                            "video_url": "https://www.youtube.com/playlist?list=PLHz_AreHm4dm6wYOIW20NgkL20I47-10X",
                            "video_label": "▶ Guanabara 100 Exercícios",
                            "doc_url": "https://exercism.org/tracks/python",
                            "doc_label": "💻 Exercism Trilha Python"
                        },
                        {
                            "title": "Algoritmos de busca e ordenação",
                            "video_url": "https://www.youtube.com/watch?v=EgLE5HwRy_M",
                            "video_label": "▶ Programação Dinâmica · Busca Binária",
                            "doc_url": "https://runestone.academy/ns/books/published/pythonds/SortSearch/sorting.html",
                            "doc_label": "📖 Guia Busca e Ordenação"
                        },
                        {
                            "title": "Noções de complexidade (Big O)",
                            "video_url": "https://www.youtube.com/watch?v=v4cd1O4zkGw",
                            "video_label": "▶ Big O Notation Explicada",
                            "doc_url": "https://www.bigocheatsheet.com/",
                            "doc_label": "📊 Big-O Cheat Sheet"
                        },
                        {
                            "title": "Projeto de linha de comando completo",
                            "video_url": "https://www.youtube.com/watch?v=pog8YmHkGMs",
                            "video_label": "▶ Guanabara Exercício #115a · Projeto com menu",
                            "doc_url": "https://click.palletsprojects.com/",
                            "doc_label": "📖 Click CLI Python"
                        }
                    ]
                ]
            ]
        },
        {
            "t": "Fase 2 · Python para dados & SQL",
            "d": "1,5 a 2 meses",
            "tip": "💡 <b>Dica de Ouro:</b> NumPy e Pandas são o arroz com feijão diário de qualquer profissional de dados e IA. Crie o hábito de documentar suas análises com gráficos claros e storytelling.",
            "p": "Escolha um dataset real do Kaggle, limpe os dados ausentes, filtre, faça análises e gráficos explicativos e publique o Jupyter Notebook completo no GitHub.",
            "r": "Kaggle Learn (Python, Pandas e Data Visualization) · Documentação oficial do Pandas (10 minutes to pandas)",
            "g": [
                [
                    "Bibliotecas",
                    [
                        {
                            "title": "NumPy: arrays e operações vetorizadas",
                            "video_url": "https://www.youtube.com/watch?v=LZDZ0AZmWHI",
                            "video_label": "▶ Hashtag · NumPy do zero",
                            "doc_url": "https://numpy.org/doc/stable/user/quickstart.html",
                            "doc_label": "📖 NumPy Quickstart"
                        },
                        {
                            "title": "Pandas: DataFrames e Series",
                            "video_url": "https://www.youtube.com/watch?v=vmEHCJofslg",
                            "video_label": "▶ Pandas DataFrames Crash Course",
                            "doc_url": "https://pandas.pydata.org/docs/user_guide/10min.html",
                            "doc_label": "📖 10 Minutes to Pandas"
                        },
                        {
                            "title": "Pandas: filtrar, agrupar e juntar (merge)",
                            "video_url": "https://www.youtube.com/watch?v=ZyhVh-qRZPA",
                            "video_label": "▶ Pandas Filter, GroupBy & Merge",
                            "doc_url": "https://pandas.pydata.org/docs/user_guide/merging.html",
                            "doc_label": "📖 Pandas Merge & GroupBy"
                        },
                        {
                            "title": "Limpeza de dados e valores ausentes",
                            "video_url": "https://www.youtube.com/watch?v=bDhvCp3_lYw",
                            "video_label": "▶ Data Cleaning com Pandas",
                            "doc_url": "https://pandas.pydata.org/docs/user_guide/missing_data.html",
                            "doc_label": "📖 Pandas Missing Data Guide"
                        }
                    ]
                ],
                [
                    "Visualização",
                    [
                        {
                            "title": "Matplotlib",
                            "video_url": "https://www.youtube.com/watch?v=UO98lJQ3QGI",
                            "video_label": "▶ Matplotlib Tutorial Completo",
                            "doc_url": "https://matplotlib.org/stable/tutorials/introductory/quick_start.html",
                            "doc_label": "📖 Matplotlib Quick Start"
                        },
                        {
                            "title": "Seaborn",
                            "video_url": "https://www.youtube.com/watch?v=6GUZXDef2U0",
                            "video_label": "▶ Seaborn Visualização Elegante",
                            "doc_url": "https://seaborn.pydata.org/tutorial.html",
                            "doc_label": "📖 Seaborn Tutorial Oficial"
                        },
                        {
                            "title": "Análise exploratória de dados (EDA)",
                            "video_url": "https://www.youtube.com/watch?v=qBigTkBLU6g",
                            "video_label": "▶ EDA Passo a Passo na Prática",
                            "doc_url": "https://www.kaggle.com/learn/data-visualization",
                            "doc_label": "💻 Kaggle Data Visualization"
                        }
                    ]
                ],
                [
                    "Ambiente e dados",
                    [
                        {
                            "title": "Jupyter Notebook e Google Colab",
                            "video_url": "https://www.youtube.com/watch?v=HW29067qVWk",
                            "video_label": "▶ Jupyter & Colab para Dados",
                            "doc_url": "https://colab.research.google.com/notebooks/intro.ipynb",
                            "doc_label": "📖 Colab Welcome Guide"
                        },
                        {
                            "title": "SQL: SELECT, WHERE, JOIN, GROUP BY",
                            "video_url": "https://www.youtube.com/watch?v=G7bMwefn8RQ",
                            "video_label": "▶ Dev Aprender · Curso SQL Completo",
                            "doc_url": "https://www.w3schools.com/sql/",
                            "doc_label": "📖 W3Schools SQL Tutorial"
                        },
                        {
                            "title": "Ler CSV, Excel e JSON",
                            "video_url": "https://www.youtube.com/watch?v=AnJPtKLtc7o",
                            "video_label": "▶ Hashtag · Arquivos CSV no Python",
                            "doc_url": "https://pandas.pydata.org/docs/user_guide/io.html",
                            "doc_label": "📖 Pandas IO Tools Guide"
                        }
                    ]
                ],
                [
                    "NumPy e Pandas avançado",
                    [
                        {
                            "title": "Broadcasting",
                            "video_url": "https://www.youtube.com/watch?v=oG1t3qlzq14",
                            "video_label": "▶ mCoding · NumPy Broadcasting",
                            "doc_url": "https://numpy.org/doc/stable/user/basics.broadcasting.html",
                            "doc_label": "📖 NumPy Broadcasting Guide"
                        },
                        {
                            "title": "Máscaras booleanas e indexação",
                            "video_url": "https://www.youtube.com/watch?v=_d_Ka-ks2a0",
                            "video_label": "▶ codebasics · Indexação booleana no NumPy",
                            "doc_url": "https://numpy.org/doc/stable/user/basics.indexing.html",
                            "doc_label": "📖 NumPy Indexing Guide"
                        },
                        {
                            "title": "Séries temporais",
                            "video_url": "https://www.youtube.com/watch?v=UFuo7EHI8zc",
                            "video_label": "▶ Time Series com Pandas",
                            "doc_url": "https://pandas.pydata.org/docs/user_guide/timeseries.html",
                            "doc_label": "📖 Pandas Time Series"
                        },
                        {
                            "title": "Pivot tables e melt",
                            "video_url": "https://www.youtube.com/watch?v=xPPs59pn6qU",
                            "video_label": "▶ Pivot Table e Melt no Pandas",
                            "doc_url": "https://pandas.pydata.org/docs/user_guide/reshaping.html",
                            "doc_label": "📖 Pandas Reshaping"
                        },
                        {
                            "title": "Apply e funções vetorizadas",
                            "video_url": "https://www.youtube.com/watch?v=P_q0tkYqvSk",
                            "video_label": "▶ Apply vs Operações Vetorizadas",
                            "doc_url": "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html",
                            "doc_label": "📖 Pandas Apply Reference"
                        },
                        {
                            "title": "Outliers e duplicados",
                            "video_url": "https://www.youtube.com/watch?v=EdlUaBMlEzE",
                            "video_label": "▶ Asimov · Limpeza de dados com Pandas",
                            "doc_url": "https://scikit-learn.org/stable/modules/outlier_detection.html",
                            "doc_label": "📖 Scikit-learn Outliers"
                        },
                        {
                            "title": "Encoding de variáveis categóricas",
                            "video_url": "https://www.youtube.com/watch?v=RWaMw02_MQQ",
                            "video_label": "▶ LabelEncoder vs One-Hot",
                            "doc_url": "https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features",
                            "doc_label": "📖 Sklearn Categorical Encoding"
                        }
                    ]
                ],
                [
                    "Dados na prática",
                    [
                        {
                            "title": "Web scraping e APIs",
                            "video_url": "https://www.youtube.com/watch?v=kqvWOcPog4s",
                            "video_label": "▶ Programação Dinâmica · Raspagem de dados",
                            "doc_url": "https://realpython.com/beautiful-soup-web-scraper-python/",
                            "doc_label": "📖 RealPython Scraping Guide"
                        },
                        {
                            "title": "SQLite e SQLAlchemy",
                            "video_url": "https://www.youtube.com/watch?v=AKQ3XEDI9Mw",
                            "video_label": "▶ SQLite & SQLAlchemy em Python",
                            "doc_url": "https://docs.sqlalchemy.org/en/20/intro.html",
                            "doc_label": "📖 SQLAlchemy 2.0 Tutorial"
                        },
                        {
                            "title": "SQL avançado: subconsultas e window functions",
                            "video_url": "https://www.youtube.com/watch?v=Ww71knvhQ-s",
                            "video_label": "▶ Window Functions e Subqueries",
                            "doc_url": "https://mode.com/sql-tutorial/sql-window-functions/",
                            "doc_label": "📖 Mode SQL Window Functions"
                        },
                        {
                            "title": "Formato Parquet",
                            "video_url": "https://www.youtube.com/watch?v=pTwDOKfB9QA",
                            "video_label": "▶ Hashtag · CSV x Parquet x Feather",
                            "doc_url": "https://parquet.apache.org/docs/",
                            "doc_label": "📖 Apache Parquet Docs"
                        },
                        {
                            "title": "Plotly e gráficos interativos",
                            "video_url": "https://www.youtube.com/watch?v=GGL6U0k8WYA",
                            "video_label": "▶ Plotly Gráficos Interativos 2D/3D",
                            "doc_url": "https://plotly.com/python/",
                            "doc_label": "📖 Plotly Python Open Source"
                        }
                    ]
                ],
                [
                    "Boas práticas",
                    [
                        {
                            "title": "Notebooks reprodutíveis",
                            "video_url": "https://www.youtube.com/watch?v=szP9IRbwO9o",
                            "video_label": "▶ Let's Data · Dominando o Jupyter",
                            "doc_url": "https://docs.jupyter.org/en/latest/",
                            "doc_label": "📖 Jupyter Documentation"
                        },
                        {
                            "title": "Storytelling com dados",
                            "video_url": "https://www.youtube.com/watch?v=qBigTkBLU6g",
                            "video_label": "▶ Data Storytelling e Insights",
                            "doc_url": "https://www.storytellingwithdata.com/",
                            "doc_label": "📖 Storytelling With Data"
                        },
                        {
                            "title": "Dashboards com Streamlit",
                            "video_url": "https://www.youtube.com/watch?v=zxA97KcUm1Q",
                            "video_label": "▶ Asimov · Streamlit em 10 minutos",
                            "doc_url": "https://docs.streamlit.io/",
                            "doc_label": "📖 Streamlit Docs Oficial"
                        }
                    ]
                ]
            ]
        },
        {
            "t": "Fase 3 · Machine Learning clássico",
            "d": "2 a 3 meses",
            "tip": "💡 <b>Marco Importante:</b> Já na Fase 3 você consegue construir soluções de alto valor de mercado! Foque em dominar validação cruzada e métricas adequadas (evitar overfitting) antes de pensar em redes profundas.",
            "p": "Prever preços de imóveis com regressão, classificar cancelamento de clientes (churn) ou competir em uma competição 'Getting Started' do Kaggle com Scikit-Learn.",
            "r": "Machine Learning Specialization (Andrew Ng, Coursera) · Livro Hands-On Machine Learning (Aurélien Géron) · Kaggle Learn (Intro to Machine Learning)",
            "g": [
                [
                    "Conceitos",
                    [
                        {
                            "title": "Aprendizado supervisionado vs. não supervisionado",
                            "video_url": "https://www.youtube.com/watch?v=1FZ0A1QCMWc",
                            "video_label": "▶ Andrew Ng Supervised vs Unsupervised",
                            "doc_url": "https://scikit-learn.org/stable/getting_started.html",
                            "doc_label": "📖 Sklearn Intro Tutorial"
                        },
                        {
                            "title": "Treino, validação e teste",
                            "video_url": "https://www.youtube.com/watch?v=fSytzGwwBVw",
                            "video_label": "▶ StatQuest Train, Test & Cross-Validation",
                            "doc_url": "https://scikit-learn.org/stable/modules/cross_validation.html",
                            "doc_label": "📖 Sklearn Train-Test Split"
                        },
                        {
                            "title": "Overfitting e underfitting",
                            "video_url": "https://www.youtube.com/watch?v=EuBBz3bI-aA",
                            "video_label": "▶ StatQuest Bias and Variance Tradeoff",
                            "doc_url": "https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html",
                            "doc_label": "📖 Sklearn Bias-Variance Example"
                        },
                        {
                            "title": "Validação cruzada",
                            "video_url": "https://www.youtube.com/watch?v=fSytzGwwBVw",
                            "video_label": "▶ K-Fold Cross Validation Explicado",
                            "doc_url": "https://scikit-learn.org/stable/modules/cross_validation.html#k-fold",
                            "doc_label": "📖 Sklearn K-Fold Guide"
                        },
                        {
                            "title": "Engenharia de atributos (feature engineering)",
                            "video_url": "https://www.youtube.com/watch?v=pYVScuY-GPk",
                            "video_label": "▶ codebasics · Feature Engineering",
                            "doc_url": "https://www.kaggle.com/learn/feature-engineering",
                            "doc_label": "💻 Kaggle Feature Engineering"
                        }
                    ]
                ],
                [
                    "Algoritmos",
                    [
                        {
                            "title": "Regressão linear",
                            "video_url": "https://www.youtube.com/watch?v=7ArmBVF2dCs",
                            "video_label": "▶ StatQuest Linear Regression",
                            "doc_url": "https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares",
                            "doc_label": "📖 Sklearn Linear Regression"
                        },
                        {
                            "title": "Regressão logística",
                            "video_url": "https://www.youtube.com/watch?v=yIYKR4sgzI8",
                            "video_label": "▶ StatQuest · Logistic Regression",
                            "doc_url": "https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression",
                            "doc_label": "📖 Sklearn Logistic Regression"
                        },
                        {
                            "title": "Árvores de decisão",
                            "video_url": "https://www.youtube.com/watch?v=7VeUPuFGJHk",
                            "video_label": "▶ StatQuest Decision Trees",
                            "doc_url": "https://scikit-learn.org/stable/modules/tree.html",
                            "doc_label": "📖 Sklearn Decision Trees"
                        },
                        {
                            "title": "Random Forest",
                            "video_url": "https://www.youtube.com/watch?v=J4Wdy0Wc_xQ",
                            "video_label": "▶ StatQuest Random Forests",
                            "doc_url": "https://scikit-learn.org/stable/modules/ensemble.html#forests-of-randomized-trees",
                            "doc_label": "📖 Sklearn Random Forests"
                        },
                        {
                            "title": "Gradient Boosting (XGBoost, LightGBM)",
                            "video_url": "https://www.youtube.com/watch?v=3CC4N4z3GJc",
                            "video_label": "▶ StatQuest Gradient Boost & XGBoost",
                            "doc_url": "https://xgboost.readthedocs.io/en/stable/",
                            "doc_label": "📖 XGBoost Documentation"
                        },
                        {
                            "title": "K-Means e clusterização",
                            "video_url": "https://www.youtube.com/watch?v=4b5d3muPQmA",
                            "video_label": "▶ StatQuest K-Means Clustering",
                            "doc_url": "https://scikit-learn.org/stable/modules/clustering.html#k-means",
                            "doc_label": "📖 Sklearn K-Means"
                        },
                        {
                            "title": "PCA",
                            "video_url": "https://www.youtube.com/watch?v=FgakZw6K1QQ",
                            "video_label": "▶ StatQuest Principal Component Analysis",
                            "doc_url": "https://scikit-learn.org/stable/modules/decomposition.html#pca",
                            "doc_label": "📖 Sklearn PCA Guide"
                        }
                    ]
                ],
                [
                    "Avaliação e prática",
                    [
                        {
                            "title": "Métricas: acurácia, precisão, recall, F1",
                            "video_url": "https://www.youtube.com/watch?v=qWfzIYCvBqo",
                            "video_label": "▶ Kimberly Fessel · Precision vs Recall",
                            "doc_url": "https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics",
                            "doc_label": "📖 Sklearn Classification Metrics"
                        },
                        {
                            "title": "Matriz de confusão e curva ROC",
                            "video_url": "https://www.youtube.com/watch?v=4jRBRDbJemM",
                            "video_label": "▶ StatQuest ROC and AUC Curves",
                            "doc_url": "https://scikit-learn.org/stable/modules/model_evaluation.html#roc-metrics",
                            "doc_label": "📖 Sklearn ROC AUC"
                        },
                        {
                            "title": "Scikit-learn e pipelines",
                            "video_url": "https://www.youtube.com/watch?v=xIqX1dqcNbY",
                            "video_label": "▶ Greg Hogg · Scikit-Learn Pipelines",
                            "doc_url": "https://scikit-learn.org/stable/modules/compose.html#pipeline",
                            "doc_label": "📖 Sklearn Pipeline Guide"
                        },
                        {
                            "title": "Ajuste de hiperparâmetros",
                            "video_url": "https://www.youtube.com/watch?v=HdlDYng8g9s",
                            "video_label": "▶ codebasics · GridSearchCV",
                            "doc_url": "https://scikit-learn.org/stable/modules/grid_search.html",
                            "doc_label": "📖 Sklearn Hyperparameter Tuning"
                        }
                    ]
                ],
                [
                    "Mais algoritmos",
                    [
                        {
                            "title": "KNN",
                            "video_url": "https://www.youtube.com/watch?v=HVXime0nQeI",
                            "video_label": "▶ StatQuest K-Nearest Neighbors",
                            "doc_url": "https://scikit-learn.org/stable/modules/neighbors.html",
                            "doc_label": "📖 Sklearn Nearest Neighbors"
                        },
                        {
                            "title": "Naive Bayes",
                            "video_url": "https://www.youtube.com/watch?v=O2L2Uv9pdDA",
                            "video_label": "▶ StatQuest Naive Bayes",
                            "doc_url": "https://scikit-learn.org/stable/modules/naive_bayes.html",
                            "doc_label": "📖 Sklearn Naive Bayes"
                        },
                        {
                            "title": "SVM",
                            "video_url": "https://www.youtube.com/watch?v=efR1C6CvhmE",
                            "video_label": "▶ StatQuest Support Vector Machines",
                            "doc_url": "https://scikit-learn.org/stable/modules/svm.html",
                            "doc_label": "📖 Sklearn Support Vector Machines"
                        },
                        {
                            "title": "DBSCAN e clusterização hierárquica",
                            "video_url": "https://www.youtube.com/watch?v=RDZUdRSDOok",
                            "video_label": "▶ StatQuest DBSCAN Clustering",
                            "doc_url": "https://scikit-learn.org/stable/modules/clustering.html#dbscan",
                            "doc_label": "📖 Sklearn DBSCAN Guide"
                        },
                        {
                            "title": "Regularização Lasso e Ridge",
                            "video_url": "https://www.youtube.com/watch?v=Q81RR3yKn30",
                            "video_label": "▶ StatQuest Ridge and Lasso Regression",
                            "doc_url": "https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression-and-classification",
                            "doc_label": "📖 Sklearn Regularization"
                        },
                        {
                            "title": "Detecção de anomalias",
                            "video_url": "https://www.youtube.com/watch?v=Y1x51i1936M",
                            "video_label": "▶ Isolation Forest",
                            "doc_url": "https://scikit-learn.org/stable/modules/outlier_detection.html",
                            "doc_label": "📖 Sklearn Anomaly Detection"
                        }
                    ]
                ],
                [
                    "Pré-processamento",
                    [
                        {
                            "title": "Normalização e padronização",
                            "video_url": "https://www.youtube.com/watch?v=sxEqtjLC0aM",
                            "video_label": "▶ StandardScaler vs MinMaxScaler",
                            "doc_url": "https://scikit-learn.org/stable/modules/preprocessing.html#standardization-or-mean-removal-and-variance-scaling",
                            "doc_label": "📖 Sklearn Preprocessing"
                        },
                        {
                            "title": "Dados desbalanceados (SMOTE)",
                            "video_url": "https://www.youtube.com/watch?v=JnlM4yLFNuo",
                            "video_label": "▶ codebasics · Dados desbalanceados",
                            "doc_url": "https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html",
                            "doc_label": "📖 Imbalanced-Learn SMOTE"
                        },
                        {
                            "title": "Seleção de atributos",
                            "video_url": "https://www.youtube.com/watch?v=bDhvCp3_lYw",
                            "video_label": "▶ Feature Selection Techniques",
                            "doc_url": "https://scikit-learn.org/stable/modules/feature_selection.html",
                            "doc_label": "📖 Sklearn Feature Selection"
                        },
                        {
                            "title": "Vazamento de dados (data leakage)",
                            "video_url": "https://www.youtube.com/watch?v=fSytzGwwBVw",
                            "video_label": "▶ Como Evitar Data Leakage",
                            "doc_url": "https://www.kaggle.com/learn/data-leakage",
                            "doc_label": "💻 Kaggle Data Leakage"
                        },
                        {
                            "title": "Séries temporais com ML",
                            "video_url": "https://www.youtube.com/watch?v=UFuo7EHI8zc",
                            "video_label": "▶ Forecasting com Machine Learning",
                            "doc_url": "https://scikit-learn.org/stable/auto_examples/applications/plot_cyclical_feature_engineering.html",
                            "doc_label": "📖 Sklearn: atributos de tempo"
                        }
                    ]
                ],
                [
                    "Interpretação e ética",
                    [
                        {
                            "title": "Importância de atributos",
                            "video_url": "https://www.youtube.com/watch?v=J4Wdy0Wc_xQ",
                            "video_label": "▶ Feature Importance no Random Forest",
                            "doc_url": "https://scikit-learn.org/stable/modules/permutation_importance.html",
                            "doc_label": "📖 Sklearn Permutation Importance"
                        },
                        {
                            "title": "SHAP e LIME",
                            "video_url": "https://www.youtube.com/watch?v=MQ6fFDwjuco",
                            "video_label": "▶ A Data Odyssey · SHAP",
                            "doc_url": "https://shap.readthedocs.io/en/latest/",
                            "doc_label": "📖 SHAP Documentation"
                        },
                        {
                            "title": "Viés e ética em ML",
                            "video_url": "https://www.youtube.com/watch?v=gV0_raKR2UQ",
                            "video_label": "▶ CrashCourse AI · Viés algorítmico",
                            "doc_url": "https://fairlearn.org/",
                            "doc_label": "📖 Fairlearn Project"
                        },
                        {
                            "title": "Sistemas de recomendação",
                            "video_url": "https://www.youtube.com/watch?v=n3RKsY2H-NE",
                            "video_label": "▶ Collaborative Filtering & Recommenders",
                            "doc_url": "https://developers.google.com/machine-learning/recommendation",
                            "doc_label": "📖 Google Recommendation Systems"
                        }
                    ]
                ]
            ]
        },
        {
            "t": "Fase 4 · Deep Learning & Redes Neurais",
            "d": "2 a 3 meses",
            "tip": "💡 <b>Dica de Ouro:</b> Não tente aprender TensorFlow e PyTorch ao mesmo tempo. Escolha <b>PyTorch</b>: é a ferramenta padrão em 90% da pesquisa mundial e nas Big Techs de IA generativa.",
            "p": "Construir e treinar uma rede neural convolucional (CNN) em PyTorch para classificar imagens (como CIFAR-10 ou raio-x médico), atingindo mais de 85% de acurácia.",
            "r": "Canal 3Blue1Brown (Série Redes Neurais) · Deep Learning Specialization (Andrew Ng) · Andrej Karpathy (Neural Networks: Zero to Hero)",
            "g": [
                [
                    "Fundamentos de redes neurais",
                    [
                        {
                            "title": "Neurônio, camadas e pesos",
                            "video_url": "https://www.youtube.com/watch?v=aircAruvnKk",
                            "video_label": "▶ 3B1B O que é uma Rede Neural?",
                            "doc_url": "https://www.deeplearningbook.org/contents/mlp.html",
                            "doc_label": "📖 Deep Learning Book Cap 6"
                        },
                        {
                            "title": "Funções de ativação",
                            "video_url": "https://www.youtube.com/watch?v=68BZ5f7P94E",
                            "video_label": "▶ StatQuest Activation Functions",
                            "doc_url": "https://pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-non-linearity",
                            "doc_label": "📖 PyTorch Activation Functions"
                        },
                        {
                            "title": "Função de perda",
                            "video_url": "https://www.youtube.com/watch?v=IHZwWFHWa-w",
                            "video_label": "▶ 3B1B Gradient Descent & Loss",
                            "doc_url": "https://pytorch.org/docs/stable/nn.html#loss-functions",
                            "doc_label": "📖 PyTorch Loss Functions"
                        },
                        {
                            "title": "Backpropagation",
                            "video_url": "https://www.youtube.com/watch?v=Ilg3gGewQ5U",
                            "video_label": "▶ 3B1B O que o Backpropagation faz?",
                            "doc_url": "https://colah.github.io/posts/2015-08-Backprop/",
                            "doc_label": "📖 Colah's Blog Calculus on Graphs"
                        },
                        {
                            "title": "Gradiente descendente e otimizadores (SGD, Adam)",
                            "video_url": "https://www.youtube.com/watch?v=MD2fYip6QsQ",
                            "video_label": "▶ Otimizadores: SGD, Momentum e Adam",
                            "doc_url": "https://pytorch.org/docs/stable/optim.html",
                            "doc_label": "📖 PyTorch Optimizers Guide"
                        },
                        {
                            "title": "Regularização (dropout, weight decay)",
                            "video_url": "https://www.youtube.com/watch?v=D8PJAL-MZv8",
                            "video_label": "▶ Andrew Ng · Dropout",
                            "doc_url": "https://pytorch.org/docs/stable/generated/torch.nn.Dropout.html",
                            "doc_label": "📖 PyTorch Dropout Docs"
                        }
                    ]
                ],
                [
                    "Arquiteturas",
                    [
                        {
                            "title": "CNNs para imagens",
                            "video_url": "https://www.youtube.com/watch?v=HGwBXDKFk9I",
                            "video_label": "▶ StatQuest Convolutional Neural Networks",
                            "doc_url": "https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html",
                            "doc_label": "📖 PyTorch Training a Classifier"
                        },
                        {
                            "title": "Transfer learning",
                            "video_url": "https://www.youtube.com/watch?v=BqqfQnyjmgg",
                            "video_label": "▶ Transfer Learning com ResNet/VGG",
                            "doc_url": "https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html",
                            "doc_label": "📖 PyTorch Transfer Learning"
                        },
                        {
                            "title": "RNNs e LSTMs para sequências",
                            "video_url": "https://www.youtube.com/watch?v=AsNTP8Kwu80",
                            "video_label": "▶ StatQuest Recurrent Neural Networks",
                            "doc_url": "https://colah.github.io/posts/2015-08-Understanding-LSTMs/",
                            "doc_label": "📖 Understanding LSTM Networks"
                        }
                    ]
                ],
                [
                    "Prática com PyTorch",
                    [
                        {
                            "title": "Tensores e autograd",
                            "video_url": "https://www.youtube.com/watch?v=IC0_FRiX-sw",
                            "video_label": "▶ PyTorch Tensors & Autograd Blitz",
                            "doc_url": "https://pytorch.org/tutorials/beginner/blitz/tensor_tutorial.html",
                            "doc_label": "📖 PyTorch Tensor Basics"
                        },
                        {
                            "title": "Datasets e DataLoaders",
                            "video_url": "https://www.youtube.com/watch?v=VVDHU_TWwUg",
                            "video_label": "▶ Custom Datasets em PyTorch",
                            "doc_url": "https://pytorch.org/tutorials/beginner/basics/data_tutorial.html",
                            "doc_label": "📖 PyTorch Datasets & DataLoaders"
                        },
                        {
                            "title": "Loop de treino e avaliação",
                            "video_url": "https://www.youtube.com/watch?v=c36lUUr864M",
                            "video_label": "▶ PyTorch Full Training Loop",
                            "doc_url": "https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html",
                            "doc_label": "📖 PyTorch Model Optimization"
                        },
                        {
                            "title": "Treinar em GPU (Colab)",
                            "video_url": "https://www.youtube.com/watch?v=r7Am-ZGMef8",
                            "video_label": "▶ Acelerando PyTorch com CUDA na GPU",
                            "doc_url": "https://pytorch.org/docs/stable/cuda.html",
                            "doc_label": "📖 PyTorch CUDA Semantics"
                        }
                    ]
                ],
                [
                    "Mais arquiteturas",
                    [
                        {
                            "title": "Autoencoders",
                            "video_url": "https://www.youtube.com/watch?v=9zKuYvjFFS8",
                            "video_label": "▶ Autoencoders e Compressão Latente",
                            "doc_url": "https://www.deeplearningbook.org/contents/autoencoders.html",
                            "doc_label": "📖 Deep Learning Book Cap 14"
                        },
                        {
                            "title": "GANs",
                            "video_url": "https://www.youtube.com/watch?v=8L11aMN5KY8",
                            "video_label": "▶ Generative Adversarial Networks",
                            "doc_url": "https://pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html",
                            "doc_label": "📖 PyTorch DCGAN Tutorial"
                        },
                        {
                            "title": "Modelos de difusão (noção)",
                            "video_url": "https://www.youtube.com/watch?v=1CIpzeNxIhU",
                            "video_label": "▶ Como Funcionam Diffusion Models",
                            "doc_url": "https://huggingface.co/blog/annotated-diffusion",
                            "doc_label": "📖 Annotated Diffusion Model"
                        },
                        {
                            "title": "Redes de grafos (noção)",
                            "video_url": "https://www.youtube.com/watch?v=GXhBEj1ZtE8",
                            "video_label": "▶ Alex Foo · Redes Neurais em Grafos",
                            "doc_url": "https://distill.pub/2021/gnn-intro/",
                            "doc_label": "📖 Distill GNN Gentle Introduction"
                        },
                        {
                            "title": "Detecção de objetos (YOLO)",
                            "video_url": "https://www.youtube.com/watch?v=ag3DLKsl2vk",
                            "video_label": "▶ YOLO Object Detection",
                            "doc_url": "https://docs.ultralytics.com/",
                            "doc_label": "📖 Ultralytics YOLO Docs"
                        },
                        {
                            "title": "Segmentação de imagens",
                            "video_url": "https://www.youtube.com/watch?v=NhdzGfB1q74",
                            "video_label": "▶ U-Net explicada",
                            "doc_url": "https://pytorch.org/hub/mateuszbuda_brain-segmentation-pytorch_unet/",
                            "doc_label": "📖 PyTorch U-Net Hub"
                        }
                    ]
                ],
                [
                    "Treino na prática",
                    [
                        {
                            "title": "Batch normalization",
                            "video_url": "https://www.youtube.com/watch?v=DtEq44FTPM4",
                            "video_label": "▶ CodeEmporium · Batch Normalization",
                            "doc_url": "https://pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html",
                            "doc_label": "📖 PyTorch BatchNorm2d"
                        },
                        {
                            "title": "Learning rate schedulers",
                            "video_url": "https://www.youtube.com/watch?v=QzulmoOg2JE",
                            "video_label": "▶ Andrew Ng · Learning Rate Decay",
                            "doc_url": "https://pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate",
                            "doc_label": "📖 PyTorch LR Schedulers"
                        },
                        {
                            "title": "Data augmentation",
                            "video_url": "https://www.youtube.com/watch?v=mTVf7BN7S8w",
                            "video_label": "▶ Data Augmentation com Torchvision",
                            "doc_url": "https://pytorch.org/vision/stable/transforms.html",
                            "doc_label": "📖 Torchvision Transforms"
                        },
                        {
                            "title": "Early stopping e checkpoints",
                            "video_url": "https://www.youtube.com/watch?v=Ygvskt5HadI",
                            "video_label": "▶ CampusX · Early Stopping",
                            "doc_url": "https://pytorch.org/tutorials/beginner/saving_loading_models.html",
                            "doc_label": "📖 PyTorch Saving & Loading"
                        },
                        {
                            "title": "Depurar rede que não aprende",
                            "video_url": "https://www.youtube.com/watch?v=P6sfmUTpUmc",
                            "video_label": "▶ Andrej Karpathy · Ativações, gradientes e BatchNorm",
                            "doc_url": "http://karpathy.github.io/2019/04/25/recipe/",
                            "doc_label": "📖 Karpathy NN Training Recipe"
                        },
                        {
                            "title": "Mixed precision",
                            "video_url": "https://www.youtube.com/watch?v=r7Am-ZGMef8",
                            "video_label": "▶ Automatic Mixed Precision (AMP)",
                            "doc_url": "https://pytorch.org/docs/stable/amp.html",
                            "doc_label": "📖 PyTorch AMP Tutorial"
                        }
                    ]
                ],
                [
                    "Outras ferramentas",
                    [
                        {
                            "title": "TensorFlow e Keras (noção)",
                            "video_url": "https://www.youtube.com/watch?v=tPYj3fFJGjk",
                            "video_label": "▶ TensorFlow 2.0 / Keras Crash Course",
                            "doc_url": "https://www.tensorflow.org/tutorials",
                            "doc_label": "📖 TensorFlow Tutorials"
                        },
                        {
                            "title": "TensorBoard e logs",
                            "video_url": "https://www.youtube.com/watch?v=VJW9wU-1n18",
                            "video_label": "▶ Patrick Loeber · TensorBoard no PyTorch",
                            "doc_url": "https://pytorch.org/tutorials/intermediate/tensorboard_tutorial.html",
                            "doc_label": "📖 PyTorch with TensorBoard"
                        },
                        {
                            "title": "Exportar modelos com ONNX",
                            "video_url": "https://www.youtube.com/watch?v=0t2jOBZSd6s",
                            "video_label": "▶ DigitalSreeni · ONNX",
                            "doc_url": "https://pytorch.org/tutorials/advanced/super_resolution_with_onnxruntime.html",
                            "doc_label": "📖 PyTorch ONNX Export"
                        },
                        {
                            "title": "PyTorch Lightning",
                            "video_url": "https://www.youtube.com/watch?v=DbESHcCoWbM",
                            "video_label": "▶ PyTorch Lightning em 15 Minutos",
                            "doc_url": "https://lightning.ai/docs/pytorch/stable/",
                            "doc_label": "📖 Lightning AI Documentation"
                        }
                    ]
                ]
            ]
        },
        {
            "t": "Fase 5 · IA moderna, LLMs e Transformers",
            "d": "2 a 3 meses",
            "tip": "💡 <b>Dica de Portfólio:</b> Construir um sistema RAG (busca semântica em documentos próprios + LLM) e integrar agentes com ferramentas é uma das habilidades com maior demanda e contratação imediata no mercado atual.",
            "p": "Um chatbot que responde perguntas sobre seus próprios documentos (RAG com banco vetorial e embeddings), capaz de chamar funções externas (Agente).",
            "r": "Hugging Face NLP / LLM Course (gratuito) · Andrej Karpathy (Let’s build GPT do zero) · Documentação oficial das APIs de LLMs (OpenAI, Anthropic, Google Gemini)",
            "g": [
                [
                    "Teoria",
                    [
                        {
                            "title": "Tokenização e embeddings",
                            "video_url": "https://www.youtube.com/watch?v=zduSFxRajkE",
                            "video_label": "▶ Karpathy Tokenização BPE",
                            "doc_url": "https://huggingface.co/learn/nlp-course/chapter2/4",
                            "doc_label": "📖 Hugging Face Tokenizers"
                        },
                        {
                            "title": "Mecanismo de atenção",
                            "video_url": "https://www.youtube.com/watch?v=eMlx5fFNoYc",
                            "video_label": "▶ 3B1B Visualizando Mecanismo de Atenção",
                            "doc_url": "https://jalammar.github.io/illustrated-transformer/",
                            "doc_label": "📖 The Illustrated Transformer"
                        },
                        {
                            "title": "Arquitetura Transformer",
                            "video_url": "https://www.youtube.com/watch?v=kCc8FmEb1nY",
                            "video_label": "▶ Karpathy Let's build GPT do zero",
                            "doc_url": "https://arxiv.org/abs/1706.03762",
                            "doc_label": "📄 Paper Attention Is All You Need"
                        },
                        {
                            "title": "Pré-treino, fine-tuning e RLHF (visão geral)",
                            "video_url": "https://www.youtube.com/watch?v=bZQun8Y4L2A",
                            "video_label": "▶ Karpathy State of GPT / RLHF",
                            "doc_url": "https://huggingface.co/blog/rlhf",
                            "doc_label": "📖 Hugging Face RLHF Guide"
                        }
                    ]
                ],
                [
                    "Ferramentas",
                    [
                        {
                            "title": "Hugging Face: modelos, datasets e transformers",
                            "video_url": "https://www.youtube.com/watch?v=tiZFewofSLM",
                            "video_label": "▶ Hugging Face Transformers Course",
                            "doc_url": "https://huggingface.co/docs/transformers/index",
                            "doc_label": "📖 Hugging Face Docs"
                        },
                        {
                            "title": "Fine-tuning com LoRA",
                            "video_url": "https://www.youtube.com/watch?v=dA-NhCtrrVE",
                            "video_label": "▶ LoRA & QLoRA Fine-Tuning de LLMs",
                            "doc_url": "https://huggingface.co/docs/peft/index",
                            "doc_label": "📖 Hugging Face PEFT Guide"
                        },
                        {
                            "title": "Engenharia de prompts",
                            "video_url": "https://www.youtube.com/watch?v=jC4v5AS4RIM",
                            "video_label": "▶ Andrew Ng Prompt Engineering",
                            "doc_url": "https://www.promptingguide.ai/pt",
                            "doc_label": "📖 Prompt Engineering Guide"
                        },
                        {
                            "title": "Usar APIs de LLMs (chamadas, streaming, tool use)",
                            "video_url": "https://www.youtube.com/watch?v=gMeTK6zzaO4",
                            "video_label": "▶ Adam Lucek · Function Calling",
                            "doc_url": "https://platform.openai.com/docs/api-reference",
                            "doc_label": "📖 OpenAI / Gemini API Docs"
                        }
                    ]
                ],
                [
                    "Aplicações",
                    [
                        {
                            "title": "RAG: busca em documentos + LLM",
                            "video_url": "https://www.youtube.com/watch?v=tcqEUSNCn8I",
                            "video_label": "▶ RAG Completo do Zero",
                            "doc_url": "https://python.langchain.com/docs/tutorials/rag/",
                            "doc_label": "📖 LangChain RAG Tutorial"
                        },
                        {
                            "title": "Bancos vetoriais e busca semântica",
                            "video_url": "https://www.youtube.com/watch?v=klTvEwg3oJ4",
                            "video_label": "▶ ChromaDB, Pinecone & Vetores",
                            "doc_url": "https://docs.trychroma.com/",
                            "doc_label": "📖 ChromaDB Getting Started"
                        },
                        {
                            "title": "Agentes e uso de ferramentas",
                            "video_url": "https://www.youtube.com/watch?v=HzGOWq5UyjY",
                            "video_label": "▶ Tech With Tim · Como agentes funcionam",
                            "doc_url": "https://python.langchain.com/docs/tutorials/agents/",
                            "doc_label": "📖 LangChain Agents Guide"
                        },
                        {
                            "title": "Avaliação e segurança de sistemas com LLM",
                            "video_url": "https://www.youtube.com/watch?v=MltkRz94SWA",
                            "video_label": "▶ Evals para engenheiros de IA",
                            "doc_url": "https://docs.ragas.io/",
                            "doc_label": "📖 Ragas Evaluation Framework"
                        }
                    ]
                ],
                [
                    "Teoria avançada",
                    [
                        {
                            "title": "Self-attention e multi-head",
                            "video_url": "https://www.youtube.com/watch?v=eMlx5fFNoYc",
                            "video_label": "▶ 3B1B Multi-Head Attention",
                            "doc_url": "https://arxiv.org/abs/1706.03762",
                            "doc_label": "📄 Paper Transformer Seção 3.2"
                        },
                        {
                            "title": "Positional encoding",
                            "video_url": "https://www.youtube.com/watch?v=1biZfFLPRSY",
                            "video_label": "▶ AI Coffee Break · Positional Embeddings",
                            "doc_url": "https://kazemnejad.com/blog/transformer_architecture_positional_encoding/",
                            "doc_label": "📖 Kazemnejad Positional Encoding"
                        },
                        {
                            "title": "Encoder vs. decoder (BERT vs. GPT)",
                            "video_url": "https://www.youtube.com/watch?v=FKlPCK1uFrc",
                            "video_label": "▶ BERT vs GPT vs T5 Arquiteturas",
                            "doc_url": "https://jalammar.github.io/illustrated-bert/",
                            "doc_label": "📖 The Illustrated BERT"
                        },
                        {
                            "title": "Janela de contexto e KV cache",
                            "video_url": "https://www.youtube.com/watch?v=80bIUggRJf4",
                            "video_label": "▶ Efficient NLP · KV Cache",
                            "doc_url": "https://huggingface.co/docs/transformers/kv_cache",
                            "doc_label": "📖 KV Cache Optimization Guide"
                        },
                        {
                            "title": "Quantização (4-bit, 8-bit)",
                            "video_url": "https://www.youtube.com/watch?v=mNE_d-C82lI",
                            "video_label": "▶ Maarten Grootendorst · GPTQ vs GGUF vs AWQ",
                            "doc_url": "https://huggingface.co/blog/hf-bitsandbytes-integration",
                            "doc_label": "📖 Hugging Face Bitsandbytes"
                        },
                        {
                            "title": "Scaling laws",
                            "video_url": "https://www.youtube.com/watch?v=PZXN7jm9IC0",
                            "video_label": "▶ Edan Meyer · Chinchilla",
                            "doc_url": "https://arxiv.org/abs/2001.08361",
                            "doc_label": "📄 OpenAI Scaling Laws Paper"
                        }
                    ]
                ],
                [
                    "Aplicações avançadas",
                    [
                        {
                            "title": "Chunking e estratégias de recuperação no RAG",
                            "video_url": "https://www.youtube.com/watch?v=tcqEUSNCn8I",
                            "video_label": "▶ Advanced RAG: Chunking & Hybrid Search",
                            "doc_url": "https://www.pinecone.io/learn/chunking-strategies/",
                            "doc_label": "📖 Pinecone Chunking Strategies"
                        },
                        {
                            "title": "Reranking",
                            "video_url": "https://www.youtube.com/watch?v=aVgZE746OXw",
                            "video_label": "▶ Bi-Encoder vs Cross-Encoder",
                            "doc_url": "https://docs.cohere.com/docs/reranking",
                            "doc_label": "📖 Cohere Rerank Documentation"
                        },
                        {
                            "title": "Saída estruturada (JSON)",
                            "video_url": "https://www.youtube.com/watch?v=xpvFinvqRCA",
                            "video_label": "▶ Efficient NLP · Saída estruturada",
                            "doc_url": "https://platform.openai.com/docs/guides/structured-outputs",
                            "doc_label": "📖 OpenAI Structured Outputs"
                        },
                        {
                            "title": "Memória e orquestração de agentes",
                            "video_url": "https://www.youtube.com/watch?v=3Yp-hIEcWXk",
                            "video_label": "▶ LangChain · Memória de agentes",
                            "doc_url": "https://langchain-ai.github.io/langgraph/",
                            "doc_label": "📖 LangGraph Documentation"
                        },
                        {
                            "title": "Protocolo MCP",
                            "video_url": "https://www.youtube.com/watch?v=deprLB_y6Ho",
                            "video_label": "▶ Código Fonte TV · MCP",
                            "doc_url": "https://modelcontextprotocol.io/",
                            "doc_label": "📖 Model Context Protocol Docs"
                        },
                        {
                            "title": "Multimodalidade: visão e áudio",
                            "video_url": "https://www.youtube.com/watch?v=lOD_EE96jhM",
                            "video_label": "▶ IBM · Vision Language Models",
                            "doc_url": "https://platform.openai.com/docs/guides/vision",
                            "doc_label": "📖 OpenAI Vision Guide"
                        }
                    ]
                ],
                [
                    "Qualidade e segurança",
                    [
                        {
                            "title": "Avaliação de LLMs (evals e benchmarks)",
                            "video_url": "https://www.youtube.com/watch?v=EN8jVkv0kiw",
                            "video_label": "▶ ByteByteGo · Fundamentos de evals",
                            "doc_url": "https://github.com/openai/evals",
                            "doc_label": "📖 OpenAI Evals Framework"
                        },
                        {
                            "title": "Alucinações e mitigação",
                            "video_url": "https://www.youtube.com/watch?v=bZQun8Y4L2A",
                            "video_label": "▶ Como Prevenir Alucinações de LLM",
                            "doc_url": "https://arxiv.org/abs/2309.01219",
                            "doc_label": "📄 Survey on Hallucination in LLMs"
                        },
                        {
                            "title": "Prompt injection",
                            "video_url": "https://www.youtube.com/watch?v=jrHRe9lSqqA",
                            "video_label": "▶ IBM · Prompt Injection",
                            "doc_url": "https://genai.owasp.org/llm-top-10/",
                            "doc_label": "📖 OWASP GenAI Top 10"
                        },
                        {
                            "title": "Custo e latência",
                            "video_url": "https://www.youtube.com/watch?v=u57EnkQaUTY",
                            "video_label": "▶ IBM · Prompt Caching",
                            "doc_url": "https://platform.openai.com/docs/guides/production-best-practices",
                            "doc_label": "📖 Production Best Practices"
                        },
                        {
                            "title": "Modelos locais (Ollama, llama.cpp)",
                            "video_url": "https://www.youtube.com/watch?v=UtSSMs6ObqY",
                            "video_label": "▶ Tech With Tim · Ollama em 15 min",
                            "doc_url": "https://ollama.com/",
                            "doc_label": "📖 Ollama Official Website"
                        }
                    ]
                ]
            ]
        },
        {
            "t": "Fase 6 · Engenharia de IA, MLOps e Produção",
            "d": "contínuo",
            "tip": "💡 <b>Dica de Carreira:</b> Código sem deploy não gera valor perceptível. Ter de 3 a 5 projetos no GitHub com README impecável, explicação do problema, solução, resultados e demo online vale mais do que dezenas de certificados.",
            "p": "Publique de 3 a 5 dos seus melhores projetos com demo online funcional (Gradio, Streamlit ou FastAPI em Docker) e documentação exemplar no GitHub e LinkedIn.",
            "r": "Documentações oficiais (Docker, FastAPI, MLflow) · Projetos Open Source · Comunidades e repositórios de referência",
            "g": [
                [
                    "Engenharia",
                    [
                        {
                            "title": "Docker",
                            "video_url": "https://www.youtube.com/watch?v=fqMOX6JJhGo",
                            "video_label": "▶ Docker para Iniciantes Completo",
                            "doc_url": "https://docs.docker.com/get-started/",
                            "doc_label": "📖 Docker Get Started"
                        },
                        {
                            "title": "FastAPI e criação de APIs",
                            "video_url": "https://www.youtube.com/watch?v=R26iojTwUv8",
                            "video_label": "▶ Hashtag · API com FastAPI",
                            "doc_url": "https://fastapi.tiangolo.com/tutorial/",
                            "doc_label": "📖 FastAPI Tutorial Oficial"
                        },
                        {
                            "title": "Deploy em nuvem (AWS, GCP ou Azure)",
                            "video_url": "https://www.youtube.com/watch?v=pJ_nCklQ65w",
                            "video_label": "▶ Shaw Talebi · FastAPI, Docker e AWS",
                            "doc_url": "https://aws.amazon.com/sagemaker/",
                            "doc_label": "📖 AWS SageMaker Overview"
                        },
                        {
                            "title": "Testes e boas práticas de código",
                            "video_url": "https://www.youtube.com/watch?v=FW-mYXr2M8w",
                            "video_label": "▶ Hashtag · PyTest",
                            "doc_url": "https://docs.pytest.org/",
                            "doc_label": "📖 Pytest Documentation"
                        }
                    ]
                ],
                [
                    "MLOps",
                    [
                        {
                            "title": "Versionamento de dados e modelos",
                            "video_url": "https://www.youtube.com/watch?v=kLKBcPonMYw",
                            "video_label": "▶ DVC · Versionando dados",
                            "doc_url": "https://dvc.org/doc/start",
                            "doc_label": "📖 DVC Get Started"
                        },
                        {
                            "title": "MLflow ou Weights & Biases",
                            "video_url": "https://www.youtube.com/watch?v=6ngxBkx05Fs",
                            "video_label": "▶ codebasics · MLflow",
                            "doc_url": "https://mlflow.org/docs/latest/index.html",
                            "doc_label": "📖 MLflow Documentation"
                        },
                        {
                            "title": "Monitoramento de modelos",
                            "video_url": "https://www.youtube.com/watch?v=uOG685WFO00",
                            "video_label": "▶ Fiddler AI · ML Drift",
                            "doc_url": "https://docs.evidentlyai.com/",
                            "doc_label": "📖 Evidently AI Model Monitoring"
                        }
                    ]
                ],
                [
                    "Carreira",
                    [
                        {
                            "title": "3 a 5 projetos documentados no GitHub",
                            "video_url": "https://www.youtube.com/watch?v=fCXBaEnPzgo",
                            "video_label": "▶ Data Professor · Portfólio no GitHub",
                            "doc_url": "https://github.com/topics/machine-learning",
                            "doc_label": "💻 GitHub ML Topics"
                        },
                        {
                            "title": "READMEs com problema, solução e resultados",
                            "video_url": "https://www.youtube.com/watch?v=6Czd1Yetaac",
                            "video_label": "▶ README Incrível para Projetos",
                            "doc_url": "https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes",
                            "doc_label": "📖 Guia README GitHub"
                        },
                        {
                            "title": "Perfil ativo no LinkedIn e Kaggle",
                            "video_url": "https://www.youtube.com/watch?v=cBbYhhH399c",
                            "video_label": "▶ Kaggle CareerCon · Análise de portfólio e currículo",
                            "doc_url": "https://www.kaggle.com/",
                            "doc_label": "💻 Kaggle Official"
                        },
                        {
                            "title": "Inglês técnico",
                            "video_url": "https://www.youtube.com/watch?v=0HHnezXSKnI",
                            "video_label": "▶ Playlist Inglês EnglishBay",
                            "doc_url": "https://arxiv.org/archive/cs",
                            "doc_label": "📄 arXiv Computer Science"
                        }
                    ]
                ],
                [
                    "Infraestrutura",
                    [
                        {
                            "title": "Linux e shell avançado",
                            "video_url": "https://www.youtube.com/watch?v=oxuRxtrO2Ag",
                            "video_label": "▶ Linux Terminal do Básico ao Avançado",
                            "doc_url": "https://ubuntu.com/tutorials/command-line-for-beginners",
                            "doc_label": "📖 Ubuntu Command Line"
                        },
                        {
                            "title": "CI/CD com GitHub Actions",
                            "video_url": "https://www.youtube.com/watch?v=R8_veQiYBjI",
                            "video_label": "▶ GitHub Actions CI/CD Pipeline",
                            "doc_url": "https://docs.github.com/pt/actions",
                            "doc_label": "📖 GitHub Actions Docs"
                        },
                        {
                            "title": "Kubernetes (noção)",
                            "video_url": "https://www.youtube.com/watch?v=X48VuDVv0do",
                            "video_label": "▶ Kubernetes Explicado em 15 Minutos",
                            "doc_url": "https://kubernetes.io/docs/home/",
                            "doc_label": "📖 Kubernetes Documentation"
                        },
                        {
                            "title": "Filas e processamento assíncrono",
                            "video_url": "https://www.youtube.com/watch?v=VRHVEporra0",
                            "video_label": "▶ Pretty Printed · Celery",
                            "doc_url": "https://docs.celeryq.dev/en/stable/",
                            "doc_label": "📖 Celery Documentation"
                        },
                        {
                            "title": "Redis, Postgres e pgvector",
                            "video_url": "https://www.youtube.com/watch?v=AKQ3XEDI9Mw",
                            "video_label": "▶ PostgreSQL com pgvector para IA",
                            "doc_url": "https://github.com/pgvector/pgvector",
                            "doc_label": "📖 pgvector Open Source"
                        }
                    ]
                ],
                [
                    "Produto",
                    [
                        {
                            "title": "Interfaces com Gradio e Streamlit",
                            "video_url": "https://www.youtube.com/watch?v=eE7CamOE-PA",
                            "video_label": "▶ AssemblyAI · Gradio Crash Course",
                            "doc_url": "https://www.gradio.app/docs",
                            "doc_label": "📖 Gradio Documentation"
                        },
                        {
                            "title": "Front-end básico (HTML e JS)",
                            "video_url": "https://www.youtube.com/watch?v=Ejkb_YpuHWs",
                            "video_label": "▶ Guanabara HTML5 e CSS3",
                            "doc_url": "https://developer.mozilla.org/pt-BR/docs/Learn",
                            "doc_label": "📖 MDN Web Docs"
                        },
                        {
                            "title": "Autenticação e limites de uso",
                            "video_url": "https://www.youtube.com/watch?v=qqGkshRzw_g",
                            "video_label": "▶ Hashtag · FastAPI: OAuth2 e JWT",
                            "doc_url": "https://fastapi.tiangolo.com/tutorial/security/",
                            "doc_label": "📖 FastAPI Security Guide"
                        },
                        {
                            "title": "Observabilidade de LLMs",
                            "video_url": "https://www.youtube.com/watch?v=THfB4p2xCFY",
                            "video_label": "▶ Langfuse · Tracing de agentes",
                            "doc_url": "https://docs.smith.langchain.com/",
                            "doc_label": "📖 LangSmith Docs"
                        }
                    ]
                ],
                [
                    "Crescimento profissional",
                    [
                        {
                            "title": "Currículo e entrevistas técnicas",
                            "video_url": "https://www.youtube.com/watch?v=s-MaQ6S9_DA",
                            "video_label": "▶ Entrevistas de ML Engineer",
                            "doc_url": "https://www.deeplearning.ai/the-batch/",
                            "doc_label": "📖 The Batch by Andrew Ng"
                        },
                        {
                            "title": "Contribuir com open source",
                            "video_url": "https://www.youtube.com/watch?v=WldXhauP024",
                            "video_label": "▶ GitHub · Primeiras contribuições",
                            "doc_url": "https://opensource.guide/pt/",
                            "doc_label": "📖 Guia de Open Source"
                        },
                        {
                            "title": "Escrever artigos e posts",
                            "video_url": "https://www.youtube.com/watch?v=qBigTkBLU6g",
                            "video_label": "▶ Criando Conteúdo Técnico e Artigos",
                            "doc_url": "https://developers.google.com/tech-writing",
                            "doc_label": "📖 Google Technical Writing"
                        },
                        {
                            "title": "Comunidades e eventos",
                            "video_url": "https://www.youtube.com/watch?v=tiZFewofSLM",
                            "video_label": "▶ Redes e Comunidades de IA",
                            "doc_url": "https://huggingface.co/community",
                            "doc_label": "💬 Hugging Face Community"
                        },
                        {
                            "title": "Certificações (opcional)",
                            "video_url": "https://www.youtube.com/watch?v=TGjq6u8VqK8",
                            "video_label": "▶ AWS · ML Engineer Associate",
                            "doc_url": "https://aws.amazon.com/certification/certified-machine-learning-specialty/",
                            "doc_label": "📖 AWS ML Specialty"
                        }
                    ]
                ]
            ]
        }
    ]
