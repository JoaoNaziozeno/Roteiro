# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 2 (parte B): SQL, formatos, NumPy/Pandas avançado e boas práticas."""
from lesson_factory import *

AULAS = {}

AULAS["SQL: SELECT, WHERE, JOIN, GROUP BY"] = aula(
    45,
    "Os dados das empresas não moram em CSVs: moram em bancos de dados. E a língua para conversar com eles, há 50 anos, é o SQL. Em quase toda vaga de dados e IA, SQL aparece na lista de requisitos.",
    ["escrever consultas com <code>SELECT</code>, <code>WHERE</code> e <code>ORDER BY</code>;", "agrupar com <code>GROUP BY</code>;", "juntar tabelas com <code>JOIN</code>."],
    ["Pandas: filtrar, agrupar e juntar (as ideias são as mesmas)."],
    [
        chute("O que essa consulta devolve?", ["Todos os clientes.", "O nome dos clientes de Recife.", "Quantos clientes há em Recife."], 1,
              ["O <code>WHERE</code> filtra.", "Isso! <code>SELECT</code> escolhe as colunas, <code>FROM</code> a tabela e <code>WHERE</code> as linhas.", "Para contar seria <code>SELECT COUNT(*)</code>."],
              "SQL se lê quase como uma frase em inglês: selecione isto, da tabela tal, onde tal condição.",
              cod="SELECT nome FROM clientes WHERE cidade = 'Recife';", rot="Chute antes de ver"),
        concreto("O bibliotecário", "<p>Você não procura entre as estantes: pede ao bibliotecário “os livros de ficção publicados depois de 2010, do mais recente para o mais antigo”. O SQL é esse pedido escrito, e o banco de dados é o bibliotecário que sabe onde tudo está.</p>"),
        nota("A anatomia de uma consulta", [
            ("<code>SELECT col1, col2</code>", "selecione", "Quais colunas. <code>*</code> traz todas."),
            ("<code>FROM tabela</code>", "de", "De qual tabela."),
            ("<code>WHERE condição</code>", "onde", "Filtra linhas: <code>=</code>, <code>&gt;</code>, <code>AND</code>, <code>OR</code>, <code>LIKE 'Re%'</code>, <code>IN (...)</code>."),
            ("<code>GROUP BY col</code> + <code>COUNT</code>, <code>SUM</code>, <code>AVG</code>", "agrupe", "Uma linha por grupo. <code>HAVING</code> filtra os grupos."),
            ("<code>JOIN outra ON a.id = b.id</code>", "junte", "<code>LEFT JOIN</code> mantém todas as linhas da esquerda."),
            ("<code>ORDER BY col DESC LIMIT 10</code>", "ordene e limite", "Os 10 maiores."),
        ], rot="Agora sim, a sintaxe"),
        passos("Total por cidade, só as grandes", [
            ("<code>SELECT cidade, SUM(valor) AS total</code>", "As colunas do resultado."),
            ("<code>FROM vendas</code>", "A tabela."),
            ("<code>WHERE data &gt;= '2025-01-01'</code>", "Filtra as linhas antes de agrupar."),
            ("<code>GROUP BY cidade</code>", "Uma linha por cidade."),
            ("<code>HAVING SUM(valor) &gt; 1000 ORDER BY total DESC</code>", "Filtra os grupos e ordena."),
        ], fim="O banco executa em outra ordem: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY. Por isso o <code>WHERE</code> não enxerga apelidos criados no <code>SELECT</code>."),
        cod("Sua primeira consulta", "O banco SQLite em memória já tem a tabela <code>vendas</code>. Escreva em <code>consulta</code> o SQL que devolve <b>cidade e total vendido</b>, ordenado do maior total para o menor.",
            '''
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE vendas (cidade TEXT, valor REAL);
INSERT INTO vendas VALUES ('Recife', 100), ('Natal', 40), ('Recife', 60), ('Natal', 80), ('Salvador', 30);
""")

consulta = "SELECT * FROM vendas"

resultado = con.execute(consulta).fetchall()
print(resultado)
''',
            [("Resultado correto", "assert resultado == [('Recife', 160.0), ('Natal', 120.0), ('Salvador', 30.0)], f'resultado = {resultado}'")],
            '''
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE vendas (cidade TEXT, valor REAL);
INSERT INTO vendas VALUES ('Recife', 100), ('Natal', 40), ('Recife', 60), ('Natal', 80), ('Salvador', 30);
""")

consulta = "SELECT cidade, SUM(valor) AS total FROM vendas GROUP BY cidade ORDER BY total DESC"

resultado = con.execute(consulta).fetchall()
print(resultado)
''', ["<code>SELECT cidade, SUM(valor) AS total FROM vendas GROUP BY cidade</code>", "No final: <code>ORDER BY total DESC</code>."]),
        cod("JOIN", "Escreva a consulta que devolve o <b>nome do cliente</b> e o <b>número de pedidos</b> de cada cliente que fez pelo menos um pedido, em ordem alfabética.",
            '''
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE clientes (id INTEGER, nome TEXT);
CREATE TABLE pedidos (id INTEGER, id_cliente INTEGER);
INSERT INTO clientes VALUES (1, 'Bia'), (2, 'Ana'), (3, 'Caio');
INSERT INTO pedidos VALUES (10, 1), (11, 2), (12, 1), (13, 1);
""")

consulta = ""

print(con.execute(consulta).fetchall() if consulta else "escreva a consulta")
''',
            [("Resultado correto", "assert con.execute(consulta).fetchall() == [('Ana', 1), ('Bia', 3)], f'deu {con.execute(consulta).fetchall()}'")],
            '''
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE clientes (id INTEGER, nome TEXT);
CREATE TABLE pedidos (id INTEGER, id_cliente INTEGER);
INSERT INTO clientes VALUES (1, 'Bia'), (2, 'Ana'), (3, 'Caio');
INSERT INTO pedidos VALUES (10, 1), (11, 2), (12, 1), (13, 1);
""")

consulta = """
SELECT c.nome, COUNT(p.id) AS n
FROM clientes c
JOIN pedidos p ON p.id_cliente = c.id
GROUP BY c.nome
ORDER BY c.nome
"""

print(con.execute(consulta).fetchall() if consulta else "escreva a consulta")
''', ["<code>FROM clientes c JOIN pedidos p ON p.id_cliente = c.id</code>", "Agrupe por nome e conte os pedidos."], rot="Mão no código · nível 2"),
        erros([
            ("Usar <code>WHERE</code> para filtrar o resultado de um <code>SUM</code>.", "Filtro sobre grupos é <code>HAVING</code>."),
            ("Esquecer a condição do <code>JOIN</code>.", "Cada linha casa com todas as outras (produto cartesiano): milhões de linhas por engano."),
            ("Montar SQL juntando texto com o que o usuário digitou.", "Abre caminho para <b>SQL injection</b>. Use parâmetros: <code>con.execute(\"... WHERE id = ?\", (id,))</code>."),
        ]),
        ponte("SQL na vida de quem faz IA",
              "<p>Antes de treinar, alguém precisa extrair os dados do banco com SQL. Depois, previsões são gravadas de volta em tabelas. E com a extensão <b>pgvector</b>, o próprio Postgres faz busca por similaridade para RAG (Fase 6). Até agentes de IA geram SQL para responder perguntas sobre dados.</p>"),
        quiz([
            ("Qual cláusula filtra grupos depois do <code>GROUP BY</code>?", ["<code>WHERE</code>", "<code>HAVING</code>", "<code>ORDER BY</code>"], 1, "<code>WHERE</code> filtra linhas antes; <code>HAVING</code>, grupos depois."),
            ("O que um <code>LEFT JOIN</code> garante?", ["Só as linhas que casam.", "Todas as linhas da tabela da esquerda.", "Ordem alfabética."], 1, "As sem par recebem nulos."),
            ("Como evitar SQL injection?", ["Usando letras maiúsculas.", "Usando consultas com parâmetros (<code>?</code>).", "Usando <code>LIMIT</code>."], 1, "Nunca concatene texto do usuário."),
        ]),
    ],
    ["<code>SELECT</code> colunas <code>FROM</code> tabela <code>WHERE</code> condição.", "<code>GROUP BY</code> com agregações; <code>HAVING</code> filtra grupos.", "<code>JOIN ... ON</code> junta tabelas; use parâmetros, nunca concatenação."],
    "Ler CSV, Excel e JSON com Pandas.",
    livro=("MLCC:", "Google Machine Learning Crash Course, módulo “Working with data”", "Que cuidados com a qualidade dos dados o curso destaca?"))

AULAS["Ler CSV, Excel e JSON"] = aula(
    30,
    "Com o módulo <code>csv</code> você leu arquivo linha por linha. Com o Pandas, uma linha de código carrega o arquivo inteiro numa tabela, já com tipos, datas e ausentes tratados, venha ele de CSV, Excel, JSON ou de uma URL.",
    ["usar <code>read_csv</code>, <code>read_excel</code> e <code>read_json</code>;", "ajustar separador, decimal, codificação e datas;", "gravar resultados com <code>to_csv</code>."],
    ["Pandas: DataFrames e Series; json e csv."],
    [
        chute("Um CSV brasileiro usa <code>;</code> como separador e vírgula como decimal. O que acontece com <code>pd.read_csv(\"vendas.csv\")</code> sem ajustes?", ["Funciona perfeitamente.", "Tudo vira uma coluna só, com o texto inteiro.", "Dá erro de codificação sempre."], 1,
              ["O padrão do Pandas é vírgula como separador.", "Isso! Sem <code>sep=\";\"</code>, o Pandas não acha separadores e põe cada linha numa coluna só.", "Codificação é outro problema possível, mas não é o principal aqui."],
              "<code>pd.read_csv(\"vendas.csv\", sep=\";\", decimal=\",\")</code> resolve."),
        concreto("O tradutor de formatos", "<p>Cada formato fala uma língua: CSV é texto com separadores, Excel é planilha com abas, JSON é árvore. O Pandas é o tradutor que transforma todos eles na mesma coisa: um DataFrame.</p>"),
        nota("Os leitores", [
            ("<code>pd.read_csv(caminho, sep=\";\", decimal=\",\", encoding=\"latin-1\")</code>", "CSV", "Também lê direto de URL."),
            ("<code>parse_dates=[\"data\"]</code>", "datas", "Converte a coluna em datas na leitura."),
            ("<code>usecols=[...]</code>, <code>nrows=1000</code>", "ler só parte", "Ótimo para arquivos grandes."),
            ("<code>pd.read_excel(caminho, sheet_name=\"Vendas\")</code>", "Excel", "Precisa do pacote <code>openpyxl</code>."),
            ("<code>pd.read_json(caminho, lines=True)</code>", "JSON / JSONL", "<code>lines=True</code> para um objeto por linha."),
            ("<code>df.to_csv(\"saida.csv\", index=False)</code>", "gravar", "<code>index=False</code> evita uma coluna extra de índice."),
        ]),
        cod("Lendo um CSV brasileiro", "O texto <code>dados</code> imita um CSV exportado de um sistema brasileiro. Leia com <code>pd.read_csv</code> (use <code>io.StringIO(dados)</code>) acertando separador, decimal e datas, e imprima o valor total.",
            '''
import io
import pandas as pd

dados = """data;produto;valor
05/01/2025;caneta;2,50
12/01/2025;caderno;18,00
03/02/2025;mochila;120,00
"""

df = pd.read_csv(io.StringIO(dados))

print(df)
''',
            [("Três colunas", "assert list(df.columns) == ['data', 'produto', 'valor'], f'colunas = {list(df.columns)}'"),
             ("Valor numérico, total 140.5", "assert df['valor'].sum() == 140.5, f'soma = {df[\"valor\"].sum()}'"),
             ("Data como data (dia primeiro)", "assert str(df['data'].dtype).startswith('datetime') and df['data'].iloc[0].month == 1 and df['data'].iloc[2].month == 2, 'use parse_dates e dayfirst=True'")],
            '''
import io
import pandas as pd

dados = """data;produto;valor
05/01/2025;caneta;2,50
12/01/2025;caderno;18,00
03/02/2025;mochila;120,00
"""

df = pd.read_csv(io.StringIO(dados), sep=";", decimal=",", parse_dates=["data"], dayfirst=True)

print(df)
''', ["<code>sep=\";\"</code> e <code>decimal=\",\"</code>.", "<code>parse_dates=[\"data\"], dayfirst=True</code> lê dia/mês/ano."]),
        cod("JSONL para tabela", "Datasets de LLM costumam vir em JSONL (um JSON por linha). Leia o texto com <code>pd.read_json(..., lines=True)</code> e calcule a média de tokens por exemplo.",
            '''
import io
import pandas as pd

jsonl = """{"pergunta": "O que é IA?", "tokens": 12}
{"pergunta": "Explique RAG.", "tokens": 30}
{"pergunta": "O que é um token?", "tokens": 18}
"""

media = None
print(media)
''',
            [("Média 20", "assert media == 20, f'media = {media}'")],
            '''
import io
import pandas as pd

jsonl = """{"pergunta": "O que é IA?", "tokens": 12}
{"pergunta": "Explique RAG.", "tokens": 30}
{"pergunta": "O que é um token?", "tokens": 18}
"""

df = pd.read_json(io.StringIO(jsonl), lines=True)
media = df["tokens"].mean()
print(media)
''', ["<code>pd.read_json(io.StringIO(jsonl), lines=True)</code>"], rot="Mão no código · nível 2"),
        erros([
            ("Acentos estranhos (<code>SÃ£o Paulo</code>).", "O arquivo não é UTF-8. Tente <code>encoding=\"latin-1\"</code>."),
            ("Datas lidas como texto ou com dia e mês trocados.", "<code>parse_dates</code> e <code>dayfirst=True</code> para o formato brasileiro."),
            ("Coluna <code>Unnamed: 0</code> aparecendo.", "O arquivo foi salvo com o índice. Grave com <code>index=False</code>."),
        ]),
        ponte("Os formatos dos datasets de IA",
              "<p>No Hugging Face, datasets aparecem em CSV, JSONL e Parquet. Conjuntos de avaliação de LLMs costumam ser JSONL com pergunta e resposta esperada. Saber carregar qualquer um deles numa tabela é o primeiro passo de qualquer experimento.</p>"),
        quiz([
            ("Qual parâmetro lê arquivos com ponto e vírgula?", ["<code>delimiter_br=True</code>", "<code>sep=\";\"</code>", "<code>decimal=\";\"</code>"], 1, "Separador de colunas."),
            ("Para JSON com um objeto por linha, use:", ["<code>lines=True</code>", "<code>orient=\"index\"</code>", "<code>header=None</code>"], 0, "É o JSONL."),
            ("Por que usar <code>index=False</code> no <code>to_csv</code>?", ["Para gravar mais rápido.", "Para não gravar o índice como coluna extra.", "Para ordenar."], 1, "Evita o <code>Unnamed: 0</code>."),
        ]),
    ],
    ["<code>read_csv</code>, <code>read_excel</code> e <code>read_json</code> transformam arquivos em DataFrames.", "Ajuste <code>sep</code>, <code>decimal</code>, <code>encoding</code> e datas para arquivos brasileiros.", "JSONL é o formato comum de datasets de LLM."],
    "Broadcasting: operações entre arrays de formatos diferentes.",
    livro=("PDA:chapter-6-data-loading-storage-and-file-formats", "Capítulo 6, “Data Loading, Storage, and File Formats”", "Que opções de read_csv o livro lista como as mais usadas?"))

AULAS["Broadcasting"] = aula(
    30,
    "Como somar um vetor de 3 números a cada uma das mil linhas de uma matriz, sem laço e sem copiar o vetor mil vezes? O NumPy “estica” o menor array para caber no maior. Essa regra se chama broadcasting, e está em toda camada de rede neural.",
    ["entender a regra de compatibilidade de formatos;", "combinar escalar, vetor e matriz;", "usar <code>np.newaxis</code> e <code>reshape</code> para alinhar dimensões."],
    ["NumPy: arrays e operações vetorizadas."],
    [
        chute("Qual o <code>shape</code> do resultado?", ["(3,)", "(2, 3)", "Dá erro"], 1,
              ["O resultado tem o tamanho do maior.", "Isso! O vetor <code>(3,)</code> é “esticado” para cada uma das 2 linhas.", "As últimas dimensões casam (3 com 3), então funciona."],
              "Compare os formatos <b>da direita para a esquerda</b>: cada par deve ser igual ou um deles ser 1.",
              cod='import numpy as np\nM = np.zeros((2, 3))\nv = np.array([1, 2, 3])\nprint((M + v).shape)'),
        concreto("O carimbo", "<p>Para pôr a mesma marca em cada linha de uma folha, você não fotocopia o carimbo: carimba linha por linha. O broadcasting faz isso com o array menor, sem gastar memória com cópias.</p>"),
        nota("A regra", [
            ("Alinhe os formatos pela direita", "passo 1", "<code>(2, 3)</code> e <code>(3,)</code> → compare 3 com 3, depois 2 com nada."),
            ("Cada par deve ser igual ou 1", "passo 2", "Dimensão ausente conta como 1."),
            ("A dimensão 1 é esticada", "passo 3", "Sem copiar dados na memória."),
            ("<code>v[:, np.newaxis]</code> ou <code>v.reshape(-1, 1)</code>", "virar coluna", "Transforma <code>(3,)</code> em <code>(3, 1)</code> para operar por linha."),
        ], rot="Agora sim, a regra"),
        passos("Padronizando colunas de uma matriz", [
            ("<code>X</code> tem formato <code>(100, 4)</code>: 100 exemplos, 4 atributos.", "Uma linha por exemplo."),
            ("<code>media = X.mean(axis=0)</code> tem formato <code>(4,)</code>.", "Uma média por coluna."),
            ("<code>X - media</code>: <code>(100, 4)</code> com <code>(4,)</code>.", "A média de cada coluna é subtraída de todas as linhas."),
            ("<code>(X - media) / X.std(axis=0)</code>", "Padronização completa, sem um único laço."),
        ]),
        cod("Distâncias de uma vez", "Calcule a distância euclidiana de <b>cada ponto</b> de <code>P</code> até o ponto <code>q</code>, sem laços, usando broadcasting.",
            '''
import numpy as np

P = np.array([[0, 0], [3, 4], [6, 8]])
q = np.array([0, 0])

dist = None
print(dist)
''',
            [("Distâncias corretas", "import numpy as np\nassert np.allclose(dist, [0, 5, 10]), f'dist = {dist}'")],
            '''
import numpy as np

P = np.array([[0, 0], [3, 4], [6, 8]])
q = np.array([0, 0])

dist = np.sqrt(((P - q) ** 2).sum(axis=1))
print(dist)
''', ["<code>P - q</code> subtrai <code>q</code> de cada linha.", "Eleve ao quadrado, some por linha (<code>axis=1</code>) e tire a raiz."]),
        cod("Tabela de multiplicação", "Crie a tabuada de 1 a 5 (matriz 5×5) usando broadcasting entre um vetor linha e um vetor coluna.",
            '''
import numpy as np

v = np.arange(1, 6)
tabuada = None
print(tabuada)
''',
            [("Formato 5x5", "assert tabuada.shape == (5, 5)"), ("Valores corretos", "import numpy as np\nassert tabuada[2, 3] == 12 and tabuada[4, 4] == 25 and tabuada[0].tolist() == [1, 2, 3, 4, 5]")],
            '''
import numpy as np

v = np.arange(1, 6)
tabuada = v[:, np.newaxis] * v
print(tabuada)
''', ["<code>v[:, np.newaxis]</code> tem formato (5, 1); <code>v</code> tem (5,).", "Multiplicando, o resultado é (5, 5)."], rot="Mão no código · nível 2"),
        erros([
            ("<code>ValueError: operands could not be broadcast together</code>.", "Imprima os <code>.shape</code> e alinhe pela direita: algum par não é igual nem 1."),
            ("Broadcasting silencioso no lugar errado.", "Somar <code>(3,)</code> com <code>(3, 1)</code> dá <code>(3, 3)</code>, não erro. Confira o formato do resultado."),
            ("Usar <code>np.tile</code> para copiar antes de operar.", "Desperdiça memória. O broadcasting faz o mesmo sem copiar."),
        ]),
        ponte("O viés de uma camada",
              "<p>Uma camada linear calcula <code>X @ W + b</code>: <code>X @ W</code> tem formato <code>(lote, saídas)</code> e o viés <code>b</code>, <code>(saídas,)</code>. É o broadcasting que soma o mesmo viés a cada exemplo do lote. Em atenção, a máscara causal também é aplicada por broadcasting.</p>"),
        quiz([
            ("<code>(4, 1)</code> com <code>(3,)</code> resulta em:", ["(4, 3)", "(4, 1)", "Erro"], 0, "1 estica para 3; a dimensão ausente estica para 4."),
            ("<code>(2, 3)</code> com <code>(2,)</code> resulta em:", ["(2, 3)", "(2, 2)", "Erro"], 2, "Pela direita: 3 com 2, nem iguais nem 1."),
            ("Para que serve <code>np.newaxis</code>?", ["Criar um array vazio.", "Acrescentar uma dimensão de tamanho 1.", "Somar eixos."], 1, "Alinha formatos para o broadcasting."),
        ]),
    ],
    ["Broadcasting estica dimensões de tamanho 1 sem copiar dados.", "Compare os formatos da direita para a esquerda.", "É o que soma o viés a cada exemplo numa camada."],
    "Máscaras booleanas: filtrar arrays sem laço.",
    livro=("PDSH:02.05-computation-on-arrays-broadcasting", "Seção 2.5, “Computation on Arrays: Broadcasting”", "Quais são as três regras de broadcasting do livro?"))

AULAS["Máscaras booleanas e indexação"] = aula(
    30,
    "“Todos os preços acima de 100”, “zere os valores negativos”, “pegue as linhas 3, 7 e 9”. No NumPy, nada disso precisa de laço: você escreve a condição e ela vira um filtro.",
    ["criar máscaras com comparações;", "filtrar e alterar valores com máscaras;", "usar indexação avançada e <code>np.where</code>."],
    ["NumPy e broadcasting."],
    [
        chute("O que esse código imprime?", ["[False True True]", "[5 9]", "2"], 1,
              ["Isso é a máscara <code>v &gt; 3</code> sozinha.", "Isso! A máscara, usada como índice, devolve só os elementos onde ela é <code>True</code>.", "Para contar seria <code>(v &gt; 3).sum()</code>."],
              "Comparação → máscara de True/False → filtro.",
              cod='import numpy as np\nv = np.array([2, 5, 9])\nprint(v[v > 3])'),
        concreto("A peneira", "<p>A máscara é uma peneira com o formato da condição: o que passa pelos furos fica, o resto é descartado. E dá para usar a mesma peneira para <b>trocar</b> só os grãos que passaram.</p>"),
        nota("Indexação poderosa", [
            ("<code>m = v &gt; 0</code>", "máscara", "Array de True/False do mesmo formato."),
            ("<code>v[m]</code>", "filtrar", "Só os elementos onde a máscara é True."),
            ("<code>v[v &lt; 0] = 0</code>", "alterar com máscara", "Zera só os negativos."),
            ("<code>(v &gt; 0) &amp; (v &lt; 10)</code>", "combinar", "<code>&amp;</code>, <code>|</code> e <code>~</code> (não), com parênteses."),
            ("<code>v[[0, 2, 5]]</code>", "indexação por lista", "Pega posições específicas."),
            ("<code>np.where(cond, a, b)</code>", "se/senão vetorizado", "Onde a condição vale, <code>a</code>; senão, <code>b</code>."),
        ]),
        passos("A ativação ReLU", [
            ("<code>z = np.array([-2, 0.5, -1, 3])</code>", "Saídas de uma camada antes da ativação."),
            ("<code>np.where(z &gt; 0, z, 0)</code>", "Mantém os positivos, zera o resto."),
            ("Resultado: <code>[0, 0.5, 0, 3]</code>", "É a ReLU, a ativação mais usada em redes neurais (Fase 4)."),
        ]),
        cod("Limpando leituras de sensor", "Leituras negativas são erros do sensor. Substitua-as pela <b>média das leituras válidas</b> (as não negativas), sem laços.",
            '''
import numpy as np

leituras = np.array([20.0, -1.0, 22.0, 24.0, -1.0, 26.0])

# corrija aqui

print(leituras)
''',
            [("Negativos viram 23.0", "assert leituras.tolist() == [20.0, 23.0, 22.0, 24.0, 23.0, 26.0], f'leituras = {leituras.tolist()}'")],
            '''
import numpy as np

leituras = np.array([20.0, -1.0, 22.0, 24.0, -1.0, 26.0])

validas = leituras >= 0
leituras[~validas] = leituras[validas].mean()

print(leituras)
''', ["<code>validas = leituras &gt;= 0</code>", "<code>leituras[~validas] = leituras[validas].mean()</code>"]),
        cod("Acurácia por máscara", "Compare as previsões com os rótulos usando uma máscara e calcule a acurácia (fração de acertos).",
            '''
import numpy as np

previsto = np.array([1, 0, 1, 1, 0, 1])
real = np.array([1, 0, 0, 1, 0, 0])

acuracia = None
print(acuracia)
''',
            [("Acurácia 4/6", "assert abs(acuracia - 4 / 6) < 1e-9, f'acuracia = {acuracia}'")],
            '''
import numpy as np

previsto = np.array([1, 0, 1, 1, 0, 1])
real = np.array([1, 0, 0, 1, 0, 0])

acuracia = (previsto == real).mean()
print(acuracia)
''', ["<code>previsto == real</code> é uma máscara; a média de True/False é a fração de True."], rot="Mão no código · nível 2"),
        erros([
            ("<code>v[v &gt; 0 and v &lt; 5]</code>", "Use <code>&amp;</code> com parênteses: <code>v[(v &gt; 0) &amp; (v &lt; 5)]</code>."),
            ("Achar que a fatia <code>v[1:3]</code> é cópia.", "Fatias são <b>visões</b>: alterar a fatia altera o original. Use <code>.copy()</code>."),
            ("Máscara de formato diferente do array.", "Ela precisa ter o mesmo formato (ou ser compatível por broadcasting)."),
        ]),
        ponte("Máscaras em IA",
              "<p>A <b>máscara de atenção</b> esconde tokens futuros ou de preenchimento. A <b>máscara de perda</b> ignora posições sem rótulo. Métricas como acurácia, precisão e recall são somas de máscaras. É a mesma ferramenta, em todo lugar.</p>"),
        quiz([
            ("O que <code>(v &gt; 0).sum()</code> calcula?", ["A soma dos positivos.", "Quantos elementos são positivos.", "O maior positivo."], 1, "Cada True vale 1."),
            ("O que <code>~m</code> faz numa máscara?", ["Inverte True e False.", "Soma 1.", "Ordena."], 0, "É o “não”."),
            ("<code>np.where(v &gt; 0, 1, -1)</code> devolve:", ["Os índices positivos.", "1 onde é positivo e -1 no resto.", "Só os positivos."], 1, "Se/senão vetorizado."),
        ]),
    ],
    ["Comparações criam máscaras; máscaras filtram e alteram.", "Combine com <code>&amp;</code>, <code>|</code> e <code>~</code>, entre parênteses.", "<code>np.where</code> é o se/senão vetorizado."],
    "Séries temporais: dados que dependem da data.",
    livro=("PDSH:02.06-boolean-arrays-and-masks", "Seção 2.6, “Comparisons, Masks, and Boolean Logic”", "Que exemplo com dados de chuva o livro usa?"))

AULAS["Séries temporais"] = aula(
    35,
    "Vendas por dia, temperatura por hora, acessos por minuto. Quando os dados têm data, a ordem importa: o ontem explica o hoje. O Pandas tem ferramentas próprias para isso, e elas são a base de qualquer previsão.",
    ["usar datas como índice;", "reamostrar com <code>resample</code>;", "calcular médias móveis e defasagens com <code>rolling</code> e <code>shift</code>."],
    ["Pandas e datetime."],
    [
        chute("Para ver a <b>tendência</b> de vendas diárias muito barulhentas, o que ajuda mais?", ["Ordenar as vendas do maior para o menor.", "Uma média móvel de 7 dias.", "Apagar os fins de semana."], 1,
              ["Ordenar destrói a ordem no tempo, que é justamente a informação.", "Isso! A média móvel suaviza o barulho do dia a dia e deixa a tendência aparecer.", "Apagar dados esconde o padrão semanal, não o barulho."],
              "Em série temporal, nunca embaralhe nem ordene por valor."),
        concreto("O termômetro do quarto", "<p>A temperatura de um minuto para o outro oscila à toa. Mas a média da última hora conta uma história clara: está esquentando. Séries temporais são isso: separar a <b>tendência</b> do <b>barulho</b> e reconhecer os <b>ciclos</b> (dia, semana, ano).</p>"),
        nota("Ferramentas de tempo", [
            ("<code>df.set_index(\"data\")</code>", "data como índice", "Com <code>DatetimeIndex</code>, dá para fatiar por data: <code>df[\"2025-03\"]</code>."),
            ("<code>df.resample(\"W\").sum()</code>", "reamostrar", "De diário para semanal (<code>\"W\"</code>), mensal (<code>\"ME\"</code>)..."),
            ("<code>s.rolling(7).mean()</code>", "média móvel", "Média dos últimos 7 pontos, em cada ponto."),
            ("<code>s.shift(1)</code>", "defasagem", "O valor de ontem, alinhado com hoje."),
            ("<code>s.pct_change()</code>", "variação", "Crescimento percentual em relação ao ponto anterior."),
        ]),
        passos("Atributos para prever as vendas de amanhã", [
            ("<code>df[\"ontem\"] = df[\"vendas\"].shift(1)</code>", "O valor de ontem."),
            ("<code>df[\"media_7\"] = df[\"vendas\"].shift(1).rolling(7).mean()</code>", "Média da semana anterior (o <code>shift</code> evita usar o próprio dia)."),
            ("<code>df[\"dia_semana\"] = df.index.dayofweek</code>", "O ciclo semanal."),
            ("<code>df.dropna()</code>", "As primeiras linhas não têm histórico suficiente."),
        ], fim="Separe treino e teste <b>pelo tempo</b>: treine no passado e teste no futuro, nunca ao acaso."),
        cod("Média móvel e defasagem", "Crie a coluna <code>media_3</code> (média móvel de 3 dias) e a coluna <code>ontem</code> (vendas do dia anterior).",
            '''
import pandas as pd

datas = pd.date_range("2025-01-01", periods=6, freq="D")
df = pd.DataFrame({"vendas": [10, 20, 30, 40, 50, 60]}, index=datas)

# crie as colunas aqui

print(df)
''',
            [("Média móvel correta", "import math\nv = df['media_3'].tolist()\nassert math.isnan(v[0]) and math.isnan(v[1]) and v[2:] == [20.0, 30.0, 40.0, 50.0], f'media_3 = {v}'"),
             ("Defasagem correta", "import math\nv = df['ontem'].tolist()\nassert math.isnan(v[0]) and v[1:] == [10.0, 20.0, 30.0, 40.0, 50.0], f'ontem = {v}'")],
            '''
import pandas as pd

datas = pd.date_range("2025-01-01", periods=6, freq="D")
df = pd.DataFrame({"vendas": [10, 20, 30, 40, 50, 60]}, index=datas)

df["media_3"] = df["vendas"].rolling(3).mean()
df["ontem"] = df["vendas"].shift(1)

print(df)
''', ["<code>df[\"vendas\"].rolling(3).mean()</code>", "<code>df[\"vendas\"].shift(1)</code>"]),
        cod("De diário para semanal", "Reamostre as vendas diárias para totais <b>semanais</b> (semanas terminando no domingo).",
            '''
import pandas as pd

datas = pd.date_range("2025-01-06", periods=14, freq="D")  # começa numa segunda-feira
s = pd.Series(range(1, 15), index=datas)

semanal = None
print(semanal)
''',
            [("Duas semanas", "assert semanal.tolist() == [28, 77], f'semanal = {semanal.tolist()}'")],
            '''
import pandas as pd

datas = pd.date_range("2025-01-06", periods=14, freq="D")
s = pd.Series(range(1, 15), index=datas)

semanal = s.resample("W").sum()
print(semanal)
''', ["<code>s.resample(\"W\").sum()</code>"], rot="Mão no código · nível 2"),
        erros([
            ("Separar treino e teste ao acaso.", "O modelo “vê o futuro” e parece ótimo, mas falha em produção. Corte por data."),
            ("Média móvel que inclui o próprio dia como atributo para prevê-lo.", "Vazamento. Aplique <code>shift(1)</code> antes."),
            ("Datas como texto.", "Converta com <code>pd.to_datetime</code> antes de qualquer operação de tempo."),
        ]),
        ponte("Tempo em IA",
              "<p>Previsão de demanda, detecção de anomalias em servidores e monitoramento de modelos (a acurácia está caindo com o tempo?) são problemas de séries temporais. E a ideia de “usar o passado para prever o próximo” é exatamente o que um LLM faz, token a token.</p>"),
        quiz([
            ("O que <code>s.shift(1)</code> faz?", ["Soma 1 aos valores.", "Desloca a série: cada ponto recebe o valor anterior.", "Remove a primeira linha."], 1, "É o “valor de ontem”."),
            ("Como separar treino e teste numa série temporal?", ["Ao acaso.", "Pelo tempo: passado no treino, futuro no teste.", "Pelos valores maiores."], 1, "Simula o uso real."),
            ("<code>resample(\"ME\")</code> agrupa por:", ["Minuto.", "Mês.", "Média."], 1, "<i>Month End</i>."),
        ]),
    ],
    ["Use datas como índice para fatiar e reamostrar.", "<code>rolling</code> suaviza; <code>shift</code> traz o passado para o presente.", "Treino e teste se separam pelo tempo."],
    "Pivot e melt: mudar o formato da tabela.",
    livro=("PDA:chapter-11-time-series", "Capítulo 11, “Time Series”", "Como o livro explica a diferença entre resample e rolling?"))

AULAS["Pivot tables e melt"] = aula(
    30,
    "A mesma informação pode estar “larga” (um mês por coluna) ou “longa” (uma linha por mês). Gráficos e modelos preferem um formato; relatórios, o outro. Pivot e melt são as duas direções dessa transformação.",
    ["transformar formato longo em largo com <code>pivot_table</code>;", "transformar largo em longo com <code>melt</code>;", "reconhecer o formato “tidy”."],
    ["Pandas: filtrar, agrupar e juntar."],
    [
        chute("Uma planilha tem as colunas <code>aluno, jan, fev, mar</code>. Para fazer um gráfico de linha com o Seaborn, qual formato você precisa?", ["Esse mesmo.", "Longo: <code>aluno, mes, nota</code>.", "Uma coluna por aluno."], 1,
              ["Com um mês por coluna, o Seaborn não sabe que “jan, fev, mar” são valores de uma mesma variável.", "Isso! No formato longo, cada linha é uma observação e “mês” vira uma coluna: é o formato <i>tidy</i>.", "Isso só troca um formato largo por outro."],
              "<code>melt</code> transforma largo em longo."),
        concreto("A tabela dinâmica do Excel", "<p>A tabela dinâmica pega uma lista longa de vendas e monta um quadro com produtos nas linhas, meses nas colunas e o total no cruzamento. <code>pivot_table</code> é exatamente isso. O <code>melt</code> desfaz o quadro e volta à lista.</p>"),
        nota("As duas direções", [
            ("<code>df.pivot_table(index=\"produto\", columns=\"mes\", values=\"valor\", aggfunc=\"sum\")</code>", "longo → largo", "Linhas, colunas, valores e como agregar."),
            ("<code>df.melt(id_vars=[\"aluno\"], var_name=\"mes\", value_name=\"nota\")</code>", "largo → longo", "As colunas que não estão em <code>id_vars</code> viram linhas."),
            ("Formato <i>tidy</i>", "arrumado", "Cada variável numa coluna, cada observação numa linha."),
            ("<code>pd.crosstab(df.a, df.b)</code>", "tabela de contagem", "Quantas vezes cada combinação aparece."),
        ]),
        cod("Tabela dinâmica", "Monte a tabela com <b>produtos nas linhas</b>, <b>meses nas colunas</b> e o <b>total vendido</b> no cruzamento.",
            '''
import pandas as pd

vendas = pd.DataFrame({
    "produto": ["caneta", "caneta", "caderno", "caderno", "caneta"],
    "mes": ["jan", "fev", "jan", "fev", "jan"],
    "valor": [10, 20, 30, 40, 5],
})

tabela = None
print(tabela)
''',
            [("Totais corretos", "assert tabela.loc['caneta', 'jan'] == 15 and tabela.loc['caderno', 'fev'] == 40 and tabela.shape == (2, 2), f'tabela =\\n{tabela}'")],
            '''
import pandas as pd

vendas = pd.DataFrame({
    "produto": ["caneta", "caneta", "caderno", "caderno", "caneta"],
    "mes": ["jan", "fev", "jan", "fev", "jan"],
    "valor": [10, 20, 30, 40, 5],
})

tabela = vendas.pivot_table(index="produto", columns="mes", values="valor", aggfunc="sum")
print(tabela)
''', ["<code>index=\"produto\", columns=\"mes\", values=\"valor\", aggfunc=\"sum\"</code>"]),
        cod("Melt", "Transforme a planilha larga de notas em formato longo, com as colunas <code>aluno</code>, <code>mes</code> e <code>nota</code>.",
            '''
import pandas as pd

notas = pd.DataFrame({"aluno": ["Ana", "Bia"], "jan": [7, 9], "fev": [8, 6]})

longo = None
print(longo)
''',
            [("Colunas certas", "assert list(longo.columns) == ['aluno', 'mes', 'nota']"), ("4 linhas", "assert len(longo) == 4"),
             ("Valores certos", "assert set(map(tuple, longo.values.tolist())) == {('Ana', 'jan', 7), ('Bia', 'jan', 9), ('Ana', 'fev', 8), ('Bia', 'fev', 6)}")],
            '''
import pandas as pd

notas = pd.DataFrame({"aluno": ["Ana", "Bia"], "jan": [7, 9], "fev": [8, 6]})

longo = notas.melt(id_vars=["aluno"], var_name="mes", value_name="nota")
print(longo)
''', ["<code>notas.melt(id_vars=[\"aluno\"], var_name=\"mes\", value_name=\"nota\")</code>"], rot="Mão no código · nível 2"),
        erros([
            ("<code>pivot</code> com combinações repetidas.", "<code>pivot</code> não sabe agregar e dá erro. Use <code>pivot_table</code> com <code>aggfunc</code>."),
            ("Guardar dados no formato largo “porque fica bonito”.", "Para analisar, prefira o longo; monte o largo só na hora de mostrar."),
        ]),
        ponte("Formatos em ML",
              "<p>Modelos clássicos querem o formato largo: uma linha por exemplo, uma coluna por atributo. Logs de experimentos costumam chegar longos (uma linha por métrica por época) e viram largos para comparar modelos lado a lado. Pivot e melt fazem a ponte.</p>"),
        quiz([
            ("Qual operação transforma colunas em linhas?", ["<code>pivot_table</code>", "<code>melt</code>", "<code>merge</code>"], 1, "Largo → longo."),
            ("No formato <i>tidy</i>:", ["Cada observação é uma linha e cada variável, uma coluna.", "Cada mês é uma coluna.", "Não há valores repetidos."], 0, "Arrumado para análise."),
            ("Quando usar <code>pivot_table</code> em vez de <code>pivot</code>?", ["Quando há combinações repetidas que precisam ser agregadas.", "Nunca.", "Para dados de texto."], 0, "Ela agrega com <code>aggfunc</code>."),
        ]),
    ],
    ["<code>pivot_table</code>: longo → largo, agregando.", "<code>melt</code>: largo → longo.", "Analise no formato <i>tidy</i>; mostre no formato que o leitor preferir."],
    "Apply e operações vetorizadas: transformar colunas.",
    livro=("PDA:chapter-8-data-wrangling-join-combine-and-reshape", "Capítulo 8, seção “Reshaping and Pivoting”", "Como o livro explica stack e unstack?"))

AULAS["Apply e funções vetorizadas"] = aula(
    30,
    "Às vezes a transformação de uma coluna é complicada demais para uma conta simples. O <code>apply</code> aplica qualquer função Python a cada valor. Mas ele cobra caro em velocidade, e saber quando <b>não</b> usá-lo é metade da lição.",
    ["usar <code>apply</code>, <code>map</code> e os métodos <code>.str</code> e <code>.dt</code>;", "trocar <code>apply</code> por operações vetorizadas;", "usar <code>np.where</code> e <code>pd.cut</code> para regras."],
    ["Pandas e máscaras booleanas."],
    [
        chute("Para calcular <code>preco * 1.1</code> numa coluna de 1 milhão de linhas, o que é mais rápido?", ["<code>df[\"preco\"].apply(lambda p: p * 1.1)</code>", "<code>df[\"preco\"] * 1.1</code>", "Tanto faz."], 1,
              ["Funciona, mas chama uma função Python um milhão de vezes.", "Isso! A operação vetorizada roda em código compilado, dezenas de vezes mais rápido.", "A diferença chega a 50 ou 100 vezes."],
              "Regra: vetorizado primeiro; <code>apply</code> só quando não há alternativa."),
        concreto("O carimbo e a caneta", "<p>Para pôr a data em mil envelopes, você usa um <b>carimbo</b> (vetorizado). Para escrever uma dedicatória diferente em cada um, precisa da <b>caneta</b> (apply). A caneta faz qualquer coisa, mas é lenta.</p>"),
        nota("Ferramentas", [
            ("<code>s.apply(f)</code>", "aplicar", "Chama <code>f</code> em cada valor. Flexível e lento."),
            ("<code>s.map({\"a\": 1, \"b\": 2})</code>", "mapear", "Troca valores usando um dicionário."),
            ("<code>s.str.lower()</code>, <code>.str.contains(\"x\")</code>", "texto vetorizado", "Métodos de texto para a coluna inteira."),
            ("<code>s.dt.year</code>, <code>.dt.dayofweek</code>", "datas vetorizadas", "Partes de datas."),
            ("<code>np.where(cond, a, b)</code>", "regra simples", "Se/senão para a coluna inteira."),
            ("<code>pd.cut(s, bins=[0, 18, 60, 120], labels=[...])</code>", "faixas", "Transforma números em categorias."),
        ]),
        cod("Faixa etária sem apply", "Crie a coluna <code>faixa</code> com <b>jovem</b> (até 17), <b>adulto</b> (18 a 59) e <b>idoso</b> (60 ou mais), usando <code>pd.cut</code>.",
            '''
import pandas as pd

df = pd.DataFrame({"idade": [5, 17, 18, 45, 59, 60, 90]})

# crie a coluna faixa

print(df)
''',
            [("Faixas corretas", "assert df['faixa'].astype(str).tolist() == ['jovem', 'jovem', 'adulto', 'adulto', 'adulto', 'idoso', 'idoso'], f'faixa = {df[\"faixa\"].astype(str).tolist()}'")],
            '''
import pandas as pd

df = pd.DataFrame({"idade": [5, 17, 18, 45, 59, 60, 90]})

df["faixa"] = pd.cut(df["idade"], bins=[-1, 17, 59, 200], labels=["jovem", "adulto", "idoso"])

print(df)
''', ["<code>pd.cut(df[\"idade\"], bins=[-1, 17, 59, 200], labels=[...])</code>", "Os intervalos incluem o limite da direita: (-1, 17], (17, 59], (59, 200]."]),
        cod("Mapear e extrair", "Crie <code>codigo</code> (mapeie <b>sim</b> para 1 e <b>não</b> para 0) e <code>dominio</code> (o que vem depois do @ no e-mail), sem <code>apply</code>.",
            '''
import pandas as pd

df = pd.DataFrame({"resposta": ["sim", "não", "sim"], "email": ["ana@gmail.com", "bia@ufpe.br", "caio@empresa.com"]})

# crie as colunas

print(df)
''',
            [("codigo correto", "assert df['codigo'].tolist() == [1, 0, 1]"), ("dominio correto", "assert df['dominio'].tolist() == ['gmail.com', 'ufpe.br', 'empresa.com'], f'dominio = {df[\"dominio\"].tolist()}'")],
            '''
import pandas as pd

df = pd.DataFrame({"resposta": ["sim", "não", "sim"], "email": ["ana@gmail.com", "bia@ufpe.br", "caio@empresa.com"]})

df["codigo"] = df["resposta"].map({"sim": 1, "não": 0})
df["dominio"] = df["email"].str.split("@").str[1]

print(df)
''', ["<code>.map({\"sim\": 1, \"não\": 0})</code>", "<code>.str.split(\"@\").str[1]</code>"], rot="Mão no código · nível 2"),
        erros([
            ("<code>apply</code> com <code>axis=1</code> em milhões de linhas.", "É praticamente um laço Python. Procure a versão vetorizada."),
            ("<code>map</code> com dicionário incompleto.", "Valores que não estão no dicionário viram ausentes (NaN)."),
            ("<code>for</code> com <code>iterrows</code> para criar colunas.", "O jeito mais lento possível. Opere na coluna inteira."),
        ]),
        ponte("Pré-processamento em escala",
              "<p>No Hugging Face, <code>dataset.map(f, batched=True)</code> aplica uma função a <b>lotes</b>, e não a cada exemplo: é a mesma lição de vetorização, para tokenizar milhões de textos. Quando o código de dados é lento, o treino inteiro espera.</p>"),
        quiz([
            ("Quando o <code>apply</code> se justifica?", ["Sempre.", "Quando não existe operação vetorizada equivalente.", "Para somar colunas."], 1, "Último recurso."),
            ("O que <code>s.map(dicionario)</code> faz com valores ausentes do dicionário?", ["Mantém o valor original.", "Vira NaN.", "Dá erro."], 1, "Confira com <code>isna</code>."),
            ("Qual transforma números em faixas?", ["<code>pd.cut</code>", "<code>pd.melt</code>", "<code>pd.merge</code>"], 0, "Com <code>bins</code> e <code>labels</code>."),
        ]),
    ],
    ["Vetorizado primeiro: contas, <code>.str</code>, <code>.dt</code>, <code>np.where</code>, <code>pd.cut</code>.", "<code>map</code> troca valores por dicionário.", "<code>apply</code> é flexível, mas lento: último recurso."],
    "Outliers e duplicados: o que destoa e o que se repete.",
    livro=("PDA:chapter-7-data-cleaning-and-preparation", "Capítulo 7, seções de transformação de dados e manipulação de strings", "Como o livro usa map e replace na limpeza?"))

AULAS["Outliers e duplicados"] = aula(
    30,
    "Uma idade de 230 anos, um salário de 1 milhão numa pesquisa de estagiários, o mesmo pedido gravado três vezes. Valores extremos e repetidos distorcem médias e confundem modelos, mas apagar sem pensar também destrói informação.",
    ["detectar outliers com a regra do IQR e com o z-score;", "decidir entre corrigir, limitar ou manter;", "encontrar e remover duplicados."],
    ["Limpeza de dados, NumPy e Pandas."],
    [
        chute("Numa base de transações, há valores enormes e raríssimos. Você está construindo um <b>detector de fraudes</b>. O que fazer com eles?", ["Apagar todos.", "Investigar: podem ser exatamente as fraudes.", "Trocar pela média."], 1,
              ["Você apagaria justamente o que procura.", "Isso! Outlier nem sempre é erro. Às vezes é o sinal mais importante.", "Trocar pela média também apaga o sinal."],
              "Pergunta-chave: o valor é <b>impossível</b> (erro) ou só <b>raro</b> (informação)?"),
        concreto("A foto da turma", "<p>Na foto da turma, alguém de 2,10 m chama a atenção. Ele é real: removê-lo da foto não deixaria a turma mais verdadeira. Mas se a ficha diz “altura: 21 m”, isso é erro de digitação. Distinguir os dois casos é o trabalho.</p>"),
        nota("Detectar e decidir", [
            ("IQR = Q3 − Q1", "intervalo interquartil", "A faixa onde está a metade central dos dados."),
            ("Fora de [Q1 − 1,5·IQR, Q3 + 1,5·IQR]", "regra do boxplot", "É o que o boxplot desenha como pontinhos."),
            ("z = (x − média) / desvio", "z-score", "Quantos desvios padrão o valor está da média. |z| &gt; 3 é suspeito."),
            ("<code>s.clip(inf, sup)</code>", "limitar", "Mantém o dado mas corta o exagero (<i>winsorizar</i>)."),
            ("<code>df.duplicated()</code> / <code>drop_duplicates(subset=[...])</code>", "duplicados", "Marca e remove linhas repetidas, inteiras ou por algumas colunas."),
        ]),
        passos("A regra do IQR em [10, 12, 12, 13, 14, 15, 90]", [
            ("Q1 = 12 e Q3 = 14,5.", "Quartis: 25% e 75% dos dados."),
            ("IQR = 2,5; limites: 12 − 3,75 = 8,25 e 14,5 + 3,75 = 18,25.", "1,5 vezes o IQR para cada lado."),
            ("90 está acima de 18,25: outlier.", "Agora investigue: erro ou caso real?"),
        ]),
        cod("Detector por IQR", "Complete a função que devolve uma <b>máscara</b> (Series de True/False) marcando os outliers pela regra do IQR.",
            '''
import pandas as pd

def outliers_iqr(s):
    return s != s

s = pd.Series([10, 12, 12, 13, 14, 15, 90])
print(s[outliers_iqr(s)])
''',
            [("Marca só o 90", "import pandas as pd\ns = pd.Series([10, 12, 12, 13, 14, 15, 90])\nassert outliers_iqr(s).tolist() == [False] * 6 + [True]"),
             ("Pega os dois extremos", "import pandas as pd\ns = pd.Series([-50, 10, 11, 12, 13, 14, 80])\nassert outliers_iqr(s).tolist() == [True, False, False, False, False, False, True]")],
            '''
import pandas as pd

def outliers_iqr(s):
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    return (s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)

s = pd.Series([10, 12, 12, 13, 14, 15, 90])
print(s[outliers_iqr(s)])
''', ["<code>s.quantile(0.25)</code> e <code>s.quantile(0.75)</code>.", "Combine as duas condições com <code>|</code>."]),
        cod("Pedidos duplicados", "O sistema gravou alguns pedidos duas vezes. Remova as linhas com o mesmo <code>id_pedido</code>, mantendo a <b>primeira</b> ocorrência.",
            '''
import pandas as pd

pedidos = pd.DataFrame({"id_pedido": [1, 2, 2, 3, 3, 3], "valor": [10, 20, 20, 30, 31, 30]})

limpos = pedidos
print(limpos)
''',
            [("Três pedidos", "assert limpos['id_pedido'].tolist() == [1, 2, 3]"), ("Mantém a primeira ocorrência", "assert limpos['valor'].tolist() == [10, 20, 30]")],
            '''
import pandas as pd

pedidos = pd.DataFrame({"id_pedido": [1, 2, 2, 3, 3, 3], "valor": [10, 20, 20, 30, 31, 30]})

limpos = pedidos.drop_duplicates(subset=["id_pedido"], keep="first")
print(limpos)
''', ["<code>drop_duplicates(subset=[\"id_pedido\"], keep=\"first\")</code>"], rot="Mão no código · nível 2"),
        erros([
            ("Remover outliers automaticamente, sempre.", "Pode apagar o fenômeno mais importante. Investigue antes."),
            ("Usar z-score em dados muito assimétricos.", "Média e desvio são puxados pelos próprios extremos. Prefira o IQR ou a mediana."),
            ("Duplicados entre treino e teste.", "O modelo “decora” o exemplo e o teste fica otimista demais. Remova duplicados <b>antes</b> de separar."),
        ]),
        ponte("Duplicados e outliers em IA",
              "<p>Em dados de treino de LLMs, deduplicação é etapa obrigatória: textos repetidos são decorados e reproduzidos. Em detecção de anomalias (Fase 3), os outliers deixam de ser problema e viram o <b>objetivo</b>.</p>"),
        quiz([
            ("Pela regra do IQR, um valor é outlier se:", ["Está acima da média.", "Está mais de 1,5·IQR além dos quartis.", "Aparece só uma vez."], 1, "É o critério do boxplot."),
            ("Um outlier deve ser:", ["Sempre removido.", "Investigado: pode ser erro ou informação valiosa.", "Sempre mantido."], 1, "Depende da causa."),
            ("Por que remover duplicados antes de separar treino e teste?", ["Para economizar memória.", "Para o mesmo exemplo não aparecer nos dois lados.", "Para ordenar os dados."], 1, "Evita uma avaliação otimista."),
        ]),
    ],
    ["Detecte com IQR (robusto) ou z-score (dados simétricos).", "Outlier impossível é erro; outlier raro pode ser o sinal.", "Remova duplicados antes de separar treino e teste."],
    "Encoding: transformar categorias em números.",
    livro=("PDSH:03.07-merge-and-join", "Capítulo 3, seções sobre agregação e dados ausentes", "Que funções de agregação o livro usa para resumir grupos?"))

AULAS["Encoding de variáveis categóricas"] = aula(
    30,
    "Modelos só entendem números. Mas “cidade”, “plano” e “cor” são categorias. Transformar texto em número parece trivial, e é exatamente aí que muitos modelos aprendem relações que não existem.",
    ["usar one-hot encoding;", "saber quando o label/ordinal encoding faz sentido;", "lidar com categorias raras e novas."],
    ["Pandas e apply/map."],
    [
        chute("Você codifica cidades como Recife = 1, Natal = 2, Salvador = 3. Para um modelo linear, qual o problema?", ["Nenhum.", "O modelo entende que Salvador é “3 vezes” Recife e que Natal fica “entre” as duas.", "Os números são pequenos demais."], 1,
              ["Há um problema sério, mesmo sem erro de execução.", "Isso! Números carregam ordem e distância. Cidades não têm ordem. Por isso existe o one-hot.", "O tamanho dos números não é a questão."],
              "Categoria sem ordem → one-hot. Categoria com ordem (P, M, G) → ordinal."),
        concreto("As caixinhas de marcar", "<p>Num formulário, “cidade” não vira um número: vira uma lista de caixinhas, e só uma fica marcada. One-hot é isso: uma coluna 0/1 para cada categoria.</p>"),
        nota("As formas de codificar", [
            ("<code>pd.get_dummies(df, columns=[\"cidade\"])</code>", "one-hot", "Uma coluna 0/1 por categoria. Seguro para categorias sem ordem."),
            ("<code>s.map({\"P\": 0, \"M\": 1, \"G\": 2})</code>", "ordinal", "Só quando a ordem é real."),
            ("<code>OneHotEncoder(handle_unknown=\"ignore\")</code>", "no scikit-learn", "Aprende as categorias no treino e ignora categorias novas na produção."),
            ("Categorias raras → “outros”", "agrupar", "Evita centenas de colunas quase vazias."),
            ("Target encoding", "média do alvo por categoria", "Poderoso para muitas categorias, mas vaza fácil: calcule só com o treino."),
        ]),
        cod("One-hot com Pandas", "Aplique one-hot na coluna <code>plano</code> (as colunas novas devem ter o prefixo <code>plano_</code>) e mantenha a coluna <code>idade</code>.",
            '''
import pandas as pd

df = pd.DataFrame({"idade": [30, 25, 41], "plano": ["básico", "premium", "básico"]})

codificado = df
print(codificado)
''',
            [("Colunas certas", "assert sorted(codificado.columns) == ['idade', 'plano_básico', 'plano_premium'], f'colunas = {list(codificado.columns)}'"),
             ("Valores 0/1 certos", "assert codificado['plano_premium'].astype(int).tolist() == [0, 1, 0]")],
            '''
import pandas as pd

df = pd.DataFrame({"idade": [30, 25, 41], "plano": ["básico", "premium", "básico"]})

codificado = pd.get_dummies(df, columns=["plano"])
print(codificado)
''', ["<code>pd.get_dummies(df, columns=[\"plano\"])</code>: o prefixo vem do nome da coluna."]),
        cod("Ordinal com sentido", "Os tamanhos têm ordem real. Codifique <code>tamanho</code> como P = 0, M = 1, G = 2 e GG = 3.",
            '''
import pandas as pd

df = pd.DataFrame({"tamanho": ["M", "GG", "P", "G", "M"]})

# crie a coluna tamanho_cod

print(df)
''',
            [("Códigos corretos", "assert df['tamanho_cod'].tolist() == [1, 3, 0, 2, 1]")],
            '''
import pandas as pd

df = pd.DataFrame({"tamanho": ["M", "GG", "P", "G", "M"]})

df["tamanho_cod"] = df["tamanho"].map({"P": 0, "M": 1, "G": 2, "GG": 3})

print(df)
''', ["<code>.map({\"P\": 0, \"M\": 1, \"G\": 2, \"GG\": 3})</code>"], rot="Mão no código · nível 2"),
        erros([
            ("One-hot em colunas com milhares de categorias (como CEP).", "A tabela explode. Agrupe as raras, use target encoding ou embeddings."),
            ("Codificar treino e teste separadamente com <code>get_dummies</code>.", "As colunas podem não bater. Use o <code>OneHotEncoder</code> treinado no treino."),
            ("Esquecer categorias novas em produção.", "Um cliente de uma cidade nova não pode derrubar o modelo: <code>handle_unknown=\"ignore\"</code>."),
        ]),
        ponte("De one-hot a embeddings",
              "<p>Um LLM com vocabulário de 100 mil tokens não usa one-hot de 100 mil colunas: usa <b>embeddings</b>, vetores densos aprendidos em que categorias parecidas ficam próximas. É a evolução natural da ideia desta aula (Fase 5).</p>"),
        quiz([
            ("Para a coluna “cor” (azul, verde, vermelho), use:", ["Ordinal.", "One-hot.", "Nenhum."], 1, "Cores não têm ordem."),
            ("Para “escolaridade” (fundamental, médio, superior), um ordinal é:", ["Errado sempre.", "Aceitável, porque há ordem real.", "Obrigatório."], 1, "A ordem tem significado."),
            ("Para que serve <code>handle_unknown=\"ignore\"</code>?", ["Ignorar ausentes.", "Não quebrar com categorias que não apareceram no treino.", "Remover colunas."], 1, "Robustez em produção."),
        ]),
    ],
    ["One-hot para categorias sem ordem; ordinal só com ordem real.", "Aprenda as categorias no treino e trate as novas.", "Embeddings são a versão densa e aprendida dessa ideia."],
    "Web scraping e APIs: montar seu próprio dataset.",
    livro=("MLCC:", "Google Machine Learning Crash Course, “Categorical data”", "Que problemas de vocabulário grande o curso discute?"))
