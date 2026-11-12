# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 2 (parte C): dados na prática e boas práticas."""
from lesson_factory import *

AULAS = {}

AULAS["Web scraping e APIs"] = aula(
    35,
    "O dataset perfeito para a sua ideia quase nunca existe pronto. Juntar uma API aqui, uma página raspada ali e transformar tudo numa tabela limpa é como nascem os projetos de dados mais originais de um portfólio.",
    ["planejar a coleta: API primeiro, scraping depois;", "paginar resultados e respeitar limites;", "transformar respostas em DataFrame."],
    ["Consumir APIs, web scraping (Fase 1) e Pandas."],
    [
        chute("Uma API devolve 100 resultados por página e você precisa de 2.000. O que fazer?", ["Pedir 2.000 de uma vez e torcer.", "Percorrer as páginas num laço, com uma pequena pausa entre os pedidos.", "Raspar a página do site em vez da API."], 1,
              ["A API vai ignorar ou recusar o pedido acima do limite.", "Isso! Paginação em laço, respeitando o limite de pedidos por minuto, é o padrão.", "Se há API, ela é sempre a melhor opção: mais estável e permitida."],
              "API &gt; scraping. E sempre devagar."),
        concreto("A colheita", "<p>Coletar dados é colher: você passa pelo pomar (as páginas), enche cestos pequenos (cada pedido) e junta tudo no galpão (o DataFrame). Colher rápido demais derruba a árvore, e o dono do pomar fecha a porteira.</p>"),
        nota("O roteiro de coleta", [
            ("Procure a API oficial", "primeiro", "Documentada, estável e dentro das regras."),
            ("<code>params={\"page\": n, \"per_page\": 100}</code>", "paginação", "Peça pedaço por pedaço até acabar."),
            ("<code>time.sleep(1)</code>", "pausa", "Respeita o limite de pedidos e evita bloqueio."),
            ("<code>pd.json_normalize(lista)</code>", "achatar JSON", "Transforma JSON aninhado em colunas."),
            ("Salve o bruto antes de limpar", "cache", "Se a limpeza tiver bug, você não precisa coletar de novo."),
        ], rot="Agora sim, o método"),
        cod("Paginação simulada", "A função <code>buscar_pagina(n)</code> imita uma API: devolve uma lista de itens e uma lista vazia quando as páginas acabam. Colete <b>todos</b> os itens num laço.",
            '''
def buscar_pagina(n):
    dados = list(range(1, 24))
    return dados[(n - 1) * 10:n * 10]

itens = []
# percorra as páginas até receber uma lista vazia

print(len(itens), itens[-1] if itens else None)
''',
            [("Coleta os 23 itens", "assert itens == list(range(1, 24)), f'coletou {len(itens)} itens'")],
            '''
def buscar_pagina(n):
    dados = list(range(1, 24))
    return dados[(n - 1) * 10:n * 10]

itens = []
pagina = 1
while True:
    lote = buscar_pagina(pagina)
    if not lote:
        break
    itens.extend(lote)
    pagina += 1

print(len(itens), itens[-1] if itens else None)
''', ["Um <code>while True</code> com <code>break</code> quando o lote vier vazio.", "<code>itens.extend(lote)</code> acrescenta todos de uma vez."]),
        cod("JSON aninhado para tabela", "Transforme a resposta em DataFrame com <code>pd.json_normalize</code> e calcule a média de estrelas por linguagem.",
            '''
import pandas as pd

resposta = [
    {"nome": "a", "info": {"linguagem": "Python", "estrelas": 120}},
    {"nome": "b", "info": {"linguagem": "Python", "estrelas": 80}},
    {"nome": "c", "info": {"linguagem": "Rust", "estrelas": 50}},
]

media = None
print(media)
''',
            [("Médias corretas", "assert media.to_dict() == {'Python': 100.0, 'Rust': 50.0}, f'media = {media.to_dict()}'")],
            '''
import pandas as pd

resposta = [
    {"nome": "a", "info": {"linguagem": "Python", "estrelas": 120}},
    {"nome": "b", "info": {"linguagem": "Python", "estrelas": 80}},
    {"nome": "c", "info": {"linguagem": "Rust", "estrelas": 50}},
]

df = pd.json_normalize(resposta)
media = df.groupby("info.linguagem")["info.estrelas"].mean()
print(media)
''', ["<code>pd.json_normalize</code> cria colunas como <code>info.linguagem</code>."], rot="Mão no código · nível 2"),
        erros([
            ("Coletar dados pessoais sem base legal.", "A LGPD vale para dados raspados. Colete só o necessário e anonimize."),
            ("Coletar tudo de novo a cada teste.", "Salve a resposta bruta em disco e trabalhe a partir dela."),
            ("Ignorar o código 429.", "É “muitos pedidos”. Espere (o cabeçalho <code>Retry-After</code> diz quanto) e tente de novo."),
        ]),
        ponte("Datasets próprios para IA",
              "<p>Um classificador de avaliações de produtos brasileiros, um RAG com as leis do seu estado, um painel de vagas de IA: todos começam com uma coleta bem feita. É o tipo de projeto que mostra iniciativa num portfólio.</p>"),
        quiz([
            ("Antes de raspar um site, o que procurar?", ["Uma API oficial.", "O código-fonte do servidor.", "O e-mail do dono."], 0, "Mais estável e permitido."),
            ("Para que serve a pausa entre pedidos?", ["Deixar o código mais bonito.", "Respeitar limites e não sobrecarregar o servidor.", "Economizar memória."], 1, "Evita bloqueios."),
            ("O que <code>pd.json_normalize</code> faz?", ["Valida o JSON.", "Achata JSON aninhado em colunas.", "Ordena chaves."], 1, "Chaves internas viram colunas com ponto."),
        ]),
    ],
    ["API primeiro; scraping só quando não houver alternativa.", "Pagine com pausas e salve o bruto.", "<code>json_normalize</code> transforma a resposta em tabela."],
    "SQLite e SQLAlchemy: bancos de dados direto do Python.",
    livro=("ATBS:12", "Capítulo 12, “Web Scraping”", "Como o livro baixa páginas e lida com erros de download?"))

AULAS["SQLite e SQLAlchemy"] = aula(
    35,
    "Um banco de dados inteiro num único arquivo, sem instalar servidor: é o SQLite, que já vem com o Python. E o SQLAlchemy é a camada que deixa o mesmo código conversar com SQLite hoje e Postgres amanhã.",
    ["criar e consultar um banco SQLite com <code>sqlite3</code>;", "usar parâmetros e transações;", "ligar Pandas e banco com <code>to_sql</code> e <code>read_sql</code>."],
    ["SQL e Pandas."],
    [
        chute("Você inseriu linhas com <code>con.execute(\"INSERT ...\")</code> e fechou o programa. Ao abrir de novo, as linhas sumiram. Por quê?", ["O SQLite apaga tudo ao fechar.", "Faltou <code>con.commit()</code>.", "O arquivo era muito grande."], 1,
              ["O SQLite guarda tudo em disco, desde que a transação seja confirmada.", "Isso! Mudanças ficam pendentes numa transação até o <code>commit</code>.", "O tamanho não tem relação."],
              "Escreveu? Confirme com <code>commit</code> (ou use <code>with con:</code>, que confirma sozinho)."),
        concreto("O caderno com cadeado", "<p>O SQLite é um caderno organizado em tabelas, guardado num arquivo só. A <b>transação</b> é escrever a lápis: só quando você passa a caneta (<code>commit</code>) aquilo fica valendo. Se algo dá errado no meio, apaga-se o lápis (<code>rollback</code>).</p>"),
        nota("Python ↔ banco", [
            ("<code>con = sqlite3.connect(\"dados.db\")</code>", "conectar", "Cria o arquivo se não existir. <code>\":memory:\"</code> fica só na memória."),
            ("<code>con.execute(sql, (valor,))</code>", "executar com parâmetros", "Os <code>?</code> no SQL são preenchidos com segurança."),
            ("<code>with con:</code>", "transação", "Confirma ao final; desfaz se houver erro."),
            ("<code>df.to_sql(\"tabela\", con, index=False)</code>", "DataFrame → tabela", "Grava o DataFrame inteiro."),
            ("<code>pd.read_sql(\"SELECT ...\", con)</code>", "consulta → DataFrame", "O resultado já chega como tabela."),
            ("<code>create_engine(\"sqlite:///dados.db\")</code>", "SQLAlchemy", "Troque a URL por <code>postgresql://...</code> e o resto continua igual."),
        ]),
        cod("Cadastro com parâmetros", "Crie a tabela <code>alunos</code> (nome, nota), insira os alunos da lista <b>usando parâmetros</b> (<code>?</code>) dentro de uma transação e consulte a média das notas.",
            '''
import sqlite3

con = sqlite3.connect(":memory:")
alunos = [("Ana", 8.0), ("Bia", 6.5), ("Caio", 9.5)]

media = None
print(media)
''',
            [("Média 8.0", "assert media == 8.0, f'media = {media}'"), ("Três linhas gravadas", "assert con.execute('SELECT COUNT(*) FROM alunos').fetchone()[0] == 3")],
            '''
import sqlite3

con = sqlite3.connect(":memory:")
alunos = [("Ana", 8.0), ("Bia", 6.5), ("Caio", 9.5)]

with con:
    con.execute("CREATE TABLE alunos (nome TEXT, nota REAL)")
    con.executemany("INSERT INTO alunos VALUES (?, ?)", alunos)

media = con.execute("SELECT AVG(nota) FROM alunos").fetchone()[0]
print(media)
''', ["<code>con.executemany(\"INSERT INTO alunos VALUES (?, ?)\", alunos)</code>", "<code>fetchone()[0]</code> pega o único valor do resultado."]),
        cod("Pandas e banco", "Grave o DataFrame no banco com <code>to_sql</code> e leia de volta, com <code>pd.read_sql</code>, só as linhas com valor acima de 50.",
            '''
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
df = pd.DataFrame({"produto": ["a", "b", "c"], "valor": [30, 80, 120]})

caros = None
print(caros)
''',
            [("Dois produtos caros", "assert caros['produto'].tolist() == ['b', 'c'], f'caros = {caros}'")],
            '''
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
df = pd.DataFrame({"produto": ["a", "b", "c"], "valor": [30, 80, 120]})

df.to_sql("vendas", con, index=False)
caros = pd.read_sql("SELECT * FROM vendas WHERE valor > 50", con)
print(caros)
''', ["<code>df.to_sql(\"vendas\", con, index=False)</code>", "<code>pd.read_sql(\"SELECT ...\", con)</code>"], rot="Mão no código · nível 2"),
        erros([
            ("Esquecer o <code>commit</code>.", "Use <code>with con:</code>: confirma sozinho."),
            ("Formatar SQL com f-string usando dado do usuário.", "SQL injection. Sempre parâmetros <code>?</code>."),
            ("Usar SQLite para muitos usuários escrevendo ao mesmo tempo.", "Ele brilha em leitura e aplicações locais. Para muitos escritores, use Postgres."),
        ]),
        ponte("Bancos em aplicações de IA",
              "<p>Histórico de conversas de um chatbot, cache de respostas de LLM (para não pagar duas vezes pela mesma pergunta), registro de previsões para monitoramento: tudo isso vai para um banco. O SQLite é perfeito para protótipos; o mesmo código com SQLAlchemy migra para produção.</p>"),
        quiz([
            ("O que o <code>commit</code> faz?", ["Fecha o banco.", "Confirma as alterações pendentes.", "Cria uma tabela."], 1, "Sem ele, as escritas se perdem."),
            ("Como passar valores com segurança?", ["Com f-strings.", "Com parâmetros <code>?</code>.", "Com <code>+</code>."], 1, "Previne SQL injection."),
            ("Qual a vantagem do SQLAlchemy?", ["É mais rápido que SQL.", "O mesmo código funciona com bancos diferentes.", "Não precisa de SQL nunca."], 1, "Troca-se só a URL de conexão."),
        ]),
    ],
    ["SQLite: banco completo num arquivo, já incluso no Python.", "Escreva com parâmetros e confirme com <code>commit</code> (ou <code>with con:</code>).", "<code>to_sql</code> e <code>read_sql</code> ligam Pandas e banco."],
    "SQL avançado: subconsultas e window functions.",
    livro=("PYDOC:", "Tutorial oficial do Python (biblioteca padrão, módulo sqlite3)", "Que exemplo de uso de parâmetros a documentação do sqlite3 mostra?"))

AULAS["SQL avançado: subconsultas e window functions"] = aula(
    40,
    "“O ranking de vendedores dentro de cada loja.” “O crescimento de cada mês em relação ao anterior.” “Clientes que gastaram acima da média.” Perguntas assim derrubam o SQL básico, e são exatamente as perguntas de uma entrevista para vaga de dados.",
    ["usar subconsultas e CTEs (<code>WITH</code>);", "calcular rankings com <code>ROW_NUMBER</code> e <code>RANK</code>;", "comparar com a linha anterior usando <code>LAG</code>."],
    ["SQL: SELECT, WHERE, JOIN, GROUP BY."],
    [
        chute("Qual a diferença entre <code>GROUP BY</code> e uma window function com <code>OVER (PARTITION BY ...)</code>?", ["Nenhuma.", "<code>GROUP BY</code> reduz a uma linha por grupo; a window function mantém todas as linhas e acrescenta o cálculo do grupo.", "Window functions só funcionam com datas."], 1,
              ["A diferença é grande: uma resume, a outra anota.", "Isso! Com a window function, cada venda continua lá, com o total da loja ao lado.", "Funcionam com qualquer coluna."],
              "Window = “olhar para o grupo sem perder a linha”."),
        concreto("O boletim com a média da turma", "<p>No boletim, cada aluno vê a <b>própria</b> nota e, ao lado, a <b>média da turma</b> e a sua <b>posição</b>. Ninguém sumiu da lista: ganhou informação do grupo. É o que uma window function faz.</p>"),
        nota("Ferramentas avançadas", [
            ("<code>WITH t AS (SELECT ...) SELECT ... FROM t</code>", "CTE", "Dá nome a uma consulta intermediária. Legível como passos."),
            ("<code>WHERE valor &gt; (SELECT AVG(valor) FROM v)</code>", "subconsulta", "Uma consulta dentro da outra."),
            ("<code>SUM(valor) OVER (PARTITION BY loja)</code>", "window", "Total da loja em cada linha."),
            ("<code>ROW_NUMBER() OVER (PARTITION BY loja ORDER BY valor DESC)</code>", "ranking", "1, 2, 3... dentro de cada loja. <code>RANK</code> repete em empates."),
            ("<code>LAG(valor) OVER (ORDER BY mes)</code>", "linha anterior", "O valor do mês passado, ao lado do atual."),
        ], rot="Agora sim, a sintaxe"),
        cod("O melhor vendedor de cada loja", "Escreva a consulta que devolve <b>loja e vendedor</b> com a maior venda de cada loja, usando <code>ROW_NUMBER</code> numa CTE. Ordene por loja.",
            '''
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE vendas (loja TEXT, vendedor TEXT, valor REAL);
INSERT INTO vendas VALUES
 ('A', 'Ana', 500), ('A', 'Bia', 700), ('A', 'Caio', 300),
 ('B', 'Davi', 900), ('B', 'Eva', 400);
""")

consulta = ""

print(con.execute(consulta).fetchall() if consulta else "escreva a consulta")
''',
            [("Resultado correto", "assert con.execute(consulta).fetchall() == [('A', 'Bia'), ('B', 'Davi')], f'deu {con.execute(consulta).fetchall()}'")],
            '''
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE vendas (loja TEXT, vendedor TEXT, valor REAL);
INSERT INTO vendas VALUES
 ('A', 'Ana', 500), ('A', 'Bia', 700), ('A', 'Caio', 300),
 ('B', 'Davi', 900), ('B', 'Eva', 400);
""")

consulta = """
WITH ranking AS (
  SELECT loja, vendedor,
         ROW_NUMBER() OVER (PARTITION BY loja ORDER BY valor DESC) AS pos
  FROM vendas
)
SELECT loja, vendedor FROM ranking WHERE pos = 1 ORDER BY loja
"""

print(con.execute(consulta).fetchall() if consulta else "escreva a consulta")
''', ["Na CTE: <code>ROW_NUMBER() OVER (PARTITION BY loja ORDER BY valor DESC) AS pos</code>.", "Fora dela: <code>WHERE pos = 1</code>."]),
        cod("Crescimento mês a mês", "Escreva a consulta que devolve, para cada mês, o valor e a <b>diferença em relação ao mês anterior</b> (use <code>LAG</code>). O primeiro mês fica com diferença nula.",
            '''
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE mensal (mes TEXT, valor REAL);
INSERT INTO mensal VALUES ('2025-01', 100), ('2025-02', 130), ('2025-03', 120);
""")

consulta = ""

print(con.execute(consulta).fetchall() if consulta else "escreva a consulta")
''',
            [("Resultado correto", "assert con.execute(consulta).fetchall() == [('2025-01', 100.0, None), ('2025-02', 130.0, 30.0), ('2025-03', 120.0, -10.0)], f'deu {con.execute(consulta).fetchall()}'")],
            '''
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE mensal (mes TEXT, valor REAL);
INSERT INTO mensal VALUES ('2025-01', 100), ('2025-02', 130), ('2025-03', 120);
""")

consulta = """
SELECT mes, valor, valor - LAG(valor) OVER (ORDER BY mes) AS dif
FROM mensal
ORDER BY mes
"""

print(con.execute(consulta).fetchall() if consulta else "escreva a consulta")
''', ["<code>valor - LAG(valor) OVER (ORDER BY mes)</code>"], rot="Mão no código · nível 2"),
        erros([
            ("Usar a coluna de uma window function no <code>WHERE</code> da mesma consulta.", "O <code>WHERE</code> roda antes. Calcule numa CTE e filtre fora dela."),
            ("Subconsultas aninhadas em três níveis.", "Reescreva com CTEs: cada passo com um nome."),
            ("Esquecer o <code>ORDER BY</code> dentro do <code>OVER</code> em <code>LAG</code> e rankings.", "Sem ordem, “anterior” e “primeiro” não fazem sentido."),
        ]),
        ponte("Atributos de comportamento",
              "<p>“Quantas compras o cliente fez nos últimos 30 dias?”, “quanto mudou desde o mês passado?”: esses atributos, os melhores para prever cancelamento e fraude, são calculados com window functions direto no banco, antes de o dado chegar ao modelo.</p>"),
        quiz([
            ("O que <code>PARTITION BY</code> define?", ["A ordem do resultado.", "Os grupos dentro dos quais a window function calcula.", "O nome da tabela."], 1, "Como um GROUP BY que não reduz linhas."),
            ("Para comparar com o mês anterior, use:", ["<code>LAG</code>", "<code>COUNT</code>", "<code>HAVING</code>"], 0, "Traz a linha anterior."),
            ("Para que serve uma CTE?", ["Acelerar o banco.", "Dar nome a uma etapa intermediária da consulta.", "Criar tabelas permanentes."], 1, "<code>WITH nome AS (...)</code>."),
        ]),
    ],
    ["CTEs (<code>WITH</code>) organizam a consulta em passos.", "Window functions calculam sobre grupos sem perder as linhas.", "<code>ROW_NUMBER</code>, <code>RANK</code> e <code>LAG</code> resolvem rankings e comparações."],
    "Parquet: o formato colunar dos dados grandes.",
    livro=("MLCC:", "Google Machine Learning Crash Course, módulo sobre dados numéricos", "Como o curso sugere transformar dados brutos em atributos?"))

AULAS["Formato Parquet"] = aula(
    25,
    "Um CSV de 2 GB pode virar um Parquet de 300 MB que carrega dez vezes mais rápido, com os tipos das colunas preservados. Não é compressão mágica: é guardar os dados <b>por coluna</b> em vez de por linha.",
    ["entender armazenamento por linha e por coluna;", "gravar e ler Parquet com Pandas;", "ler só as colunas necessárias."],
    ["Ler CSV, Excel e JSON."],
    [
        chute("Você só precisa de 2 das 80 colunas de um arquivo enorme. Em qual formato a leitura é muito mais rápida?", ["CSV.", "Parquet.", "Os dois iguais."], 1,
              ["No CSV, cada linha tem todas as colunas misturadas: é preciso ler tudo.", "Isso! O Parquet guarda cada coluna separada: dá para ler só as 2 que importam.", "A diferença pode passar de 10 vezes."],
              "Formato colunar combina com análise, que quase sempre usa poucas colunas."),
        concreto("O armário por tipo de roupa", "<p>Guardar <b>por linha</b> é ter uma gaveta por dia da semana, com camisa, calça e meia misturadas. Guardar <b>por coluna</b> é uma gaveta só de camisas, outra só de calças. Se você quer todas as camisas, o segundo jeito é imediato, e roupas parecidas juntas ocupam menos espaço.</p>"),
        tabela("CSV × Parquet", ["", "CSV", "Parquet"], [
            ["Organização", "por linha, texto", "por coluna, binário"],
            ["Tipos das colunas", "perdidos (tudo vira texto)", "preservados (datas, inteiros, categorias)"],
            ["Tamanho", "grande", "pequeno (compressão por coluna)"],
            ["Ler só algumas colunas", "lê tudo", "lê só o necessário"],
            ["Abrir no Excel / editor", "sim", "não diretamente"],
        ], rot="Comparando"),
        nota("No Pandas", [
            ("<code>df.to_parquet(\"dados.parquet\")</code>", "gravar", "Requer <code>pyarrow</code> (ou <code>fastparquet</code>)."),
            ("<code>pd.read_parquet(\"dados.parquet\", columns=[\"a\", \"b\"])</code>", "ler colunas", "Só o que você precisa."),
            ("<code>df[\"cidade\"].astype(\"category\")</code>", "tipo categoria", "Textos repetidos ocupam muito menos memória e disco."),
        ]),
        cod("Economizando memória", "Converta a coluna <code>cidade</code> (com valores muito repetidos) para o tipo <code>category</code> e confira que o uso de memória caiu para menos da metade.",
            '''
import pandas as pd

df = pd.DataFrame({"cidade": ["Recife", "Natal", "Salvador"] * 20000})
antes = df.memory_usage(deep=True).sum()

# converta aqui

depois = df.memory_usage(deep=True).sum()
print(antes, depois)
''',
            [("Tipo categoria", "assert str(df['cidade'].dtype) == 'category'"), ("Memória caiu mais da metade", "assert depois < antes / 2, f'antes={antes}, depois={depois}'")],
            '''
import pandas as pd

df = pd.DataFrame({"cidade": ["Recife", "Natal", "Salvador"] * 20000})
antes = df.memory_usage(deep=True).sum()

df["cidade"] = df["cidade"].astype("category")

depois = df.memory_usage(deep=True).sum()
print(antes, depois)
''', ["<code>df[\"cidade\"] = df[\"cidade\"].astype(\"category\")</code>"]),
        lab("CSV × Parquet na sua máquina", '''
import numpy as np, pandas as pd, time, os

df = pd.DataFrame({"a": np.random.rand(2_000_000), "b": np.random.randint(0, 100, 2_000_000),
                   "c": np.random.choice(["x", "y", "z"], 2_000_000)})
df.to_csv("teste.csv", index=False)
df.to_parquet("teste.parquet")
print("CSV:", os.path.getsize("teste.csv") // 1_000_000, "MB · Parquet:", os.path.getsize("teste.parquet") // 1_000_000, "MB")

t = time.time(); pd.read_csv("teste.csv", usecols=["a"]); print("CSV:", round(time.time() - t, 2), "s")
t = time.time(); pd.read_parquet("teste.parquet", columns=["a"]); print("Parquet:", round(time.time() - t, 2), "s")
''', corpo="<p>Rode no Colab (ou com <code>pip install pyarrow</code>):</p>", exps=["Compare tamanhos e tempos. Quanto o Parquet ganhou?"]),
        erros([
            ("Usar Parquet para arquivos que pessoas vão abrir no Excel.", "Para troca com humanos, CSV ou Excel. Para pipelines, Parquet."),
            ("Achar que Parquet resolve dados que não cabem na memória.", "Ajuda muito, mas para isso existem Polars, DuckDB e leitura em partes."),
        ]),
        ponte("Datasets grandes de IA",
              "<p>O Hugging Face converte datasets para Parquet automaticamente, e a biblioteca <code>datasets</code> lê esses arquivos sem carregar tudo na memória. Bilhões de tokens de treino de LLMs circulam nesse formato.</p>"),
        quiz([
            ("Por que o Parquet é menor que o CSV?", ["Apaga linhas repetidas.", "Guarda por coluna, em binário, com compressão.", "Usa menos casas decimais."], 1, "Valores parecidos juntos comprimem bem."),
            ("Qual vantagem o Parquet tem sobre o CSV quanto aos tipos?", ["Nenhuma.", "Preserva os tipos de cada coluna.", "Converte tudo para texto."], 1, "Datas continuam datas."),
            ("Quando o CSV ainda é a melhor escolha?", ["Para compartilhar com pessoas e planilhas.", "Para datasets de bilhões de linhas.", "Nunca."], 0, "Legível por qualquer programa."),
        ]),
    ],
    ["Parquet guarda por coluna: menor, mais rápido e com tipos preservados.", "Leia só as colunas necessárias.", "Tipo <code>category</code> economiza memória em textos repetidos."],
    "Plotly: gráficos interativos.",
    livro=("PDA:chapter-6-data-loading-storage-and-file-formats", "Capítulo 6, seção sobre formatos binários", "Que formatos binários o livro compara?"))

AULAS["Plotly e gráficos interativos"] = aula(
    25,
    "Num gráfico estático, o leitor vê o que você escolheu mostrar. Num gráfico interativo, ele passa o mouse, dá zoom, liga e desliga séries e descobre sozinho. O Plotly faz isso com uma linha, e o resultado vai direto para dashboards.",
    ["criar gráficos interativos com <code>plotly.express</code>;", "usar cor, tamanho e animação como dimensões extras;", "exportar para HTML."],
    ["Matplotlib, Seaborn e Pandas."],
    [
        chute("Qual a principal vantagem de um gráfico interativo num relatório?", ["Fica mais colorido.", "O leitor explora detalhes (valores exatos, zoom, filtros) sem você precisar fazer dez gráficos.", "Ocupa menos espaço no disco."], 1,
              ["Cor não é a questão.", "Isso! Passar o mouse mostra o valor exato; clicar na legenda isola uma série.", "Geralmente ocupa mais."],
              "Estático para documento impresso e artigo; interativo para exploração e dashboard."),
        concreto("O mapa de papel e o mapa do celular", "<p>O mapa de papel mostra uma escala fixa. O do celular dá zoom na sua rua e mostra o nome do restaurante quando você toca. Plotly é o mapa do celular dos gráficos.</p>"),
        nota("Plotly Express", [
            ("<code>px.scatter(df, x=\"a\", y=\"b\", color=\"c\", size=\"d\")</code>", "dispersão", "Cor e tamanho viram dimensões extras."),
            ("<code>px.line(df, x=\"data\", y=\"valor\", color=\"loja\")</code>", "linha", "Uma linha por loja."),
            ("<code>hover_data=[\"nome\"]</code>", "detalhes no mouse", "Informações extras ao passar o mouse."),
            ("<code>animation_frame=\"ano\"</code>", "animação", "Um quadro por ano, com botão de play."),
            ("<code>fig.write_html(\"grafico.html\")</code>", "exportar", "Abre em qualquer navegador, sem Python."),
        ]),
        lab("Riqueza e expectativa de vida", '''
import plotly.express as px

df = px.data.gapminder()
fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                 hover_name="country", log_x=True, animation_frame="year", size_max=55)
fig.show()
''', corpo="<p>Rode no Colab: é um dos gráficos mais famosos da visualização de dados.</p>",
            exps=["Dê play. O que acontece com a Ásia entre 1952 e 2007?", "Passe o mouse sobre o Brasil em anos diferentes."]),
        cod("Preparando os dados do gráfico", "Gráficos interativos com linha por grupo precisam do formato longo. Prepare <code>df_longo</code> com as colunas <code>mes</code>, <code>loja</code> e <code>vendas</code> a partir da tabela larga.",
            '''
import pandas as pd

largo = pd.DataFrame({"mes": ["jan", "fev"], "loja_A": [10, 15], "loja_B": [7, 12]})

df_longo = None
print(df_longo)
''',
            [("Colunas certas", "assert list(df_longo.columns) == ['mes', 'loja', 'vendas']"), ("4 linhas", "assert len(df_longo) == 4 and df_longo['vendas'].sum() == 44")],
            '''
import pandas as pd

largo = pd.DataFrame({"mes": ["jan", "fev"], "loja_A": [10, 15], "loja_B": [7, 12]})

df_longo = largo.melt(id_vars="mes", var_name="loja", value_name="vendas")
print(df_longo)
''', ["<code>largo.melt(id_vars=\"mes\", var_name=\"loja\", value_name=\"vendas\")</code>"], exp="<p>Com isso: <code>px.line(df_longo, x=\"mes\", y=\"vendas\", color=\"loja\")</code>.</p>"),
        erros([
            ("Interatividade como enfeite.", "Se o leitor não precisa explorar, um gráfico estático claro comunica melhor."),
            ("Arquivo HTML enorme com milhões de pontos.", "Agregue ou amostre antes de plotar."),
        ]),
        ponte("Explorando embeddings",
              "<p>Um uso clássico em IA: reduzir embeddings de textos para 2 dimensões (PCA, Fase 3) e plotar com Plotly, com o texto de cada ponto no <code>hover</code>. Você vê, literalmente, frases parecidas formando grupos.</p>"),
        quiz([
            ("O que <code>color=\"continente\"</code> faz num <code>px.scatter</code>?", ["Muda o fundo.", "Pinta os pontos conforme a coluna continente.", "Ordena os pontos."], 1, "Uma dimensão extra."),
            ("Como compartilhar um gráfico Plotly com quem não tem Python?", ["Mandar o notebook.", "Exportar com <code>write_html</code>.", "Copiar o código."], 1, "Abre no navegador."),
            ("Quando preferir o gráfico estático?", ["Em artigos e documentos impressos.", "Em dashboards.", "Nunca."], 0, "Papel não tem mouse."),
        ]),
    ],
    ["<code>plotly.express</code> cria gráficos interativos em uma linha.", "Cor, tamanho e animação adicionam dimensões.", "Exporte para HTML ou use em dashboards."],
    "Notebooks reprodutíveis: experimentos que outras pessoas conseguem refazer.",
    livro=("PDSH:04.00-introduction-to-matplotlib", "Capítulo 4, para comparar com a abordagem estática", "Que limitações do Matplotlib o livro aponta?"))

AULAS["Notebooks reprodutíveis"] = aula(
    25,
    "“Funcionava ontem.” “No meu computador dá 0,92.” Um resultado que só você consegue reproduzir não é um resultado. Reprodutibilidade é o que separa um experimento científico de um palpite com gráficos.",
    ["fixar sementes aleatórias;", "registrar versões e dependências;", "organizar o notebook para rodar de cima a baixo."],
    ["Jupyter e Colab, ambientes virtuais."],
    [
        chute("Você treinou o mesmo modelo duas vezes, sem mudar nada, e obteve 0,91 e 0,87. A causa mais provável?", ["Bug no Python.", "Aleatoriedade sem semente fixa (separação dos dados, inicialização).", "O computador esquentou."], 1,
              ["O Python é determinístico quando você controla a aleatoriedade.", "Isso! Separação treino/teste, embaralhamento e pesos iniciais são sorteados. Sem semente, cada execução é diferente.", "Temperatura não muda resultados."],
              "Fixe a semente em <b>todas</b> as fontes de aleatoriedade."),
        concreto("A receita de bolo", "<p>“Um pouco de farinha, forno quente” não é receita. Receita boa tem quantidades, marcas, temperatura e tempo. Um notebook reproduzível é uma receita completa: versões, sementes, dados e a ordem dos passos.</p>"),
        passos("O checklist da reprodutibilidade", [
            ("Fixe sementes: <code>random.seed(42)</code>, <code>np.random.seed(42)</code>, <code>random_state=42</code>.", "Todo sorteio passa a ser repetível."),
            ("Registre as versões: <code>requirements.txt</code> com versões fixas.", "Outra versão de uma biblioteca pode mudar o resultado."),
            ("Dados com origem clara: URL, data da coleta, ou uma cópia versionada.", "Ninguém deve depender do “arquivo que estava no meu desktop”."),
            ("Notebook linear: reinicie e execute tudo.", "Sem estados escondidos."),
            ("Funções reutilizadas vão para arquivos <code>.py</code>.", "O notebook conta a história; o código pesado mora em módulos."),
        ]),
        cod("Sementes fixas", "A função <code>experimento</code> embaralha os dados e devolve os 3 primeiros. Faça-a ser reproduzível: com a mesma semente, o resultado deve ser sempre o mesmo.",
            '''
import random

def experimento(dados, semente=42):
    dados = dados[:]
    random.shuffle(dados)
    return dados[:3]

print(experimento(list(range(10))), experimento(list(range(10))))
''',
            [("Mesma semente, mesmo resultado", "assert experimento(list(range(10))) == experimento(list(range(10)))"),
             ("Semente diferente, resultado diferente", "assert experimento(list(range(50)), 1) != experimento(list(range(50)), 2)")],
            '''
import random

def experimento(dados, semente=42):
    rng = random.Random(semente)
    dados = dados[:]
    rng.shuffle(dados)
    return dados[:3]

print(experimento(list(range(10))), experimento(list(range(10))))
''', ["Crie um gerador próprio: <code>rng = random.Random(semente)</code> e use <code>rng.shuffle</code>."], exp="<p>Um gerador próprio (<code>random.Random</code> ou <code>np.random.default_rng</code>) é melhor que a semente global: nada fora da função interfere.</p>"),
        erros([
            ("Fixar a semente só no começo e depois chamar bibliotecas que têm a própria aleatoriedade.", "Passe <code>random_state</code> a cada função do scikit-learn e fixe a semente do PyTorch."),
            ("<code>pip install pandas</code> sem versão.", "Daqui a um ano é outra versão. Fixe: <code>pandas==2.2.3</code>."),
            ("Resultado reportado de uma execução sortuda.", "Rode com várias sementes e reporte média e desvio."),
        ]),
        ponte("Reprodutibilidade em IA",
              "<p>Em deep learning, mesmo com sementes fixas, algumas operações na GPU não são determinísticas. Por isso artigos sérios reportam a média de várias execuções. E ferramentas como MLflow (Fase 6) registram automaticamente parâmetros, versões e resultados de cada experimento.</p>"),
        quiz([
            ("Por que fixar sementes?", ["Para o código rodar mais rápido.", "Para os sorteios serem repetíveis.", "Para usar menos memória."], 1, "Mesmo experimento, mesmo resultado."),
            ("O que deve ir no <code>requirements.txt</code>?", ["Só os nomes das bibliotecas.", "Nomes com versões fixas.", "O código do notebook."], 1, "Versões mudam comportamentos."),
            ("Como reportar um resultado de forma honesta?", ["A melhor execução.", "Média e variação de várias execuções.", "A primeira execução."], 1, "Evita resultados de sorte."),
        ]),
    ],
    ["Fixe sementes em todas as fontes de aleatoriedade.", "Versões fixas e dados com origem clara.", "Notebook linear, que roda de cima a baixo."],
    "Storytelling com dados: transformar análise em decisão.",
    livro=("PDSH:01.00-ipython-beyond-normal-python", "Capítulo 1, seções sobre histórico e comandos mágicos", "Que ferramentas o IPython oferece para registrar o que foi executado?"))

AULAS["Storytelling com dados"] = aula(
    25,
    "Uma análise brilhante que ninguém entende não muda nada. A última etapa do trabalho com dados é a mais subestimada: contar o que você descobriu de forma que alguém <b>tome uma decisão</b> por causa disso.",
    ["estruturar uma apresentação em contexto, descoberta e ação;", "escrever títulos que dizem a conclusão;", "tirar do gráfico tudo que não ajuda."],
    ["Visualização (Matplotlib, Seaborn, Plotly) e EDA."],
    [
        chute("Qual título de gráfico é melhor para uma reunião?", ["“Vendas por mês (2025)”", "“As vendas caíram 18% desde que o frete subiu em março”", "“Gráfico 3”"], 1,
              ["Descreve o gráfico, mas obriga o leitor a descobrir a conclusão sozinho.", "Isso! O título já diz a mensagem. O gráfico vira a prova.", "Não diz nada."],
              "Título descritivo diz <b>o que é</b>; título de conclusão diz <b>o que importa</b>."),
        concreto("O advogado no tribunal", "<p>O advogado não despeja todas as provas na mesa. Ele conta uma história (o que aconteceu), mostra as provas certas, na ordem certa, e termina com um pedido claro. Apresentar dados é igual: contexto, evidência e <b>pedido</b>.</p>"),
        passos("A estrutura em três atos", [
            ("<b>Contexto</b>: qual era a pergunta e por que ela importa.", "Uma ou duas frases. Sem jargão."),
            ("<b>Descoberta</b>: a resposta, com um ou dois gráficos.", "Só o que sustenta a mensagem. O resto vai para o anexo."),
            ("<b>Ação</b>: o que você recomenda e qual o impacto esperado.", "“Sugiro X; esperamos Y.”"),
        ], fim="Teste: se alguém ler só os títulos dos slides, entende a história inteira?"),
        tabela("Limpando um gráfico", ["Tire", "Mantenha"], [
            ["Grades pesadas e bordas", "Os dados e a comparação principal"],
            ["Cores para tudo", "Uma cor de destaque para o que importa; cinza no resto"],
            ["Legenda distante", "Rótulos diretamente nas linhas"],
            ["3D, sombras e pizza", "Barras e linhas simples"],
        ], rot="Menos é mais"),
        cod("Título de conclusão", "Escreva a função que gera um título de conclusão a partir de dois valores: <b>As vendas caíram 18% em março</b> ou <b>As vendas subiram 5% em março</b> (porcentagem arredondada, sem casas decimais).",
            '''
def titulo(antes, depois, mes):
    return ""

print(titulo(1000, 820, "março"))
''',
            [("Queda", "assert titulo(1000, 820, 'março') == 'As vendas caíram 18% em março', f'deu {titulo(1000, 820, \"março\")!r}'"), ("Alta", "assert titulo(200, 210, 'abril') == 'As vendas subiram 5% em abril'")],
            '''
def titulo(antes, depois, mes):
    variacao = (depois - antes) / antes * 100
    verbo = "subiram" if variacao >= 0 else "caíram"
    return f"As vendas {verbo} {abs(round(variacao))}% em {mes}"

print(titulo(1000, 820, "março"))
''', ["Variação percentual: <code>(depois - antes) / antes * 100</code>.", "Escolha o verbo pelo sinal e use <code>abs</code>."]),
        erros([
            ("Mostrar o processo em vez do resultado.", "A audiência quer a conclusão. O passo a passo vai para o apêndice."),
            ("Vinte gráficos numa apresentação de dez minutos.", "Três gráficos bem escolhidos convencem mais."),
            ("Esconder a incerteza.", "Diga o tamanho da amostra e as limitações. Credibilidade vale mais que certeza falsa."),
        ]),
        ponte("Contar a história de um modelo",
              "<p>“Nosso modelo tem F1 de 0,87” não convence ninguém de negócio. “O modelo identifica 9 em cada 10 fraudes, e cada fraude evitada economiza 400 reais” convence. Traduzir métricas em impacto é uma das habilidades mais valorizadas em quem trabalha com IA.</p>"),
        quiz([
            ("O que deve dizer o título de um gráfico numa apresentação?", ["O nome das variáveis.", "A conclusão principal.", "A fonte dos dados."], 1, "O gráfico é a prova da frase."),
            ("Qual é o último ato de uma boa apresentação de dados?", ["Os detalhes técnicos.", "A recomendação de ação.", "O agradecimento."], 1, "Dados existem para decisões."),
            ("Como destacar a informação principal num gráfico?", ["Usar muitas cores.", "Uma cor de destaque e o resto em cinza.", "Fazer em 3D."], 1, "Contraste guia o olhar."),
        ]),
    ],
    ["Contexto, descoberta e ação.", "Títulos que dizem a conclusão.", "Tire do gráfico o que não sustenta a mensagem."],
    "Dashboards com Streamlit: análises que as pessoas usam.",
    livro=("MLCC:", "Google Machine Learning Crash Course, introdução", "Como o curso apresenta resultados de modelos de forma visual?"))

AULAS["Dashboards com Streamlit"] = aula(
    35,
    "Seu notebook tem a análise perfeita, mas o gerente não vai abrir um notebook. Com Streamlit, o mesmo código Python vira um site interativo, com filtros e gráficos, em poucas dezenas de linhas e sem HTML.",
    ["montar uma página com <code>st.title</code>, <code>st.write</code> e gráficos;", "criar filtros com <code>st.selectbox</code> e <code>st.slider</code>;", "usar cache e publicar o app."],
    ["Pandas, Plotly e funções."],
    [
        chute("Num app Streamlit, o usuário mexe num slider. O que acontece?", ["Só o gráfico ligado ao slider é atualizado.", "O script inteiro roda de novo, de cima a baixo, com o novo valor.", "Nada, até apertar um botão."], 1,
              ["Essa é a intuição natural, mas não é o modelo do Streamlit.", "Isso! A cada interação o script roda de novo. Por isso o cache (<code>@st.cache_data</code>) é essencial para não recarregar os dados toda vez.", "Widgets disparam a reexecução imediatamente."],
              "Modelo mental: o script é a página; cada interação redesenha tudo."),
        concreto("O painel do carro", "<p>Você não abre o motor para saber a velocidade: olha o painel. O dashboard é o painel da análise: mostra os números que importam e deixa a pessoa ajustar o que quer ver, sem tocar no motor (o código).</p>"),
        nota("Peças do Streamlit", [
            ("<code>st.title</code>, <code>st.write</code>, <code>st.metric</code>", "conteúdo", "Título, texto/tabelas e cartões de indicador."),
            ("<code>st.selectbox</code>, <code>st.slider</code>, <code>st.multiselect</code>", "filtros", "Cada um devolve o valor escolhido."),
            ("<code>st.plotly_chart(fig)</code>, <code>st.dataframe(df)</code>", "gráficos e tabelas", "Interativos por padrão."),
            ("<code>@st.cache_data</code>", "cache", "Guarda o resultado da função; não recarrega os dados a cada clique."),
            ("<code>streamlit run app.py</code>", "rodar", "Abre no navegador. Para publicar: Streamlit Community Cloud."),
        ]),
        lab("Seu primeiro dashboard", '''
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def carregar():
    return px.data.gapminder()

df = carregar()
st.title("Expectativa de vida no mundo")

continente = st.selectbox("Continente", sorted(df["continent"].unique()))
ano = st.slider("Ano", int(df.year.min()), int(df.year.max()), 2007, step=5)

filtro = df[(df.continent == continente) & (df.year == ano)]
st.metric("Expectativa média", f"{filtro.lifeExp.mean():.1f} anos")
st.plotly_chart(px.bar(filtro.sort_values("lifeExp"), x="lifeExp", y="country", orientation="h"))
''', corpo="<p>Salve como <code>app.py</code> e rode <code>streamlit run app.py</code> (depois de <code>pip install streamlit plotly</code>):</p>",
            exps=["Troque o <code>selectbox</code> por um <code>multiselect</code> de países.", "Publique no Streamlit Community Cloud a partir de um repositório no GitHub."]),
        cod("A lógica por trás do filtro", "Separe a lógica da interface: escreva <code>filtrar(df, continente, ano)</code> e <code>indicador(df)</code> (média de <code>vida</code> com 1 casa). O app só chamaria essas funções.",
            '''
import pandas as pd

df = pd.DataFrame({
    "pais": ["Brasil", "Chile", "Japão", "Índia"],
    "continente": ["América", "América", "Ásia", "Ásia"],
    "ano": [2007, 2007, 2007, 2002],
    "vida": [72.4, 78.6, 82.6, 62.9],
})

def filtrar(df, continente, ano):
    return df

def indicador(df):
    return 0

print(indicador(filtrar(df, "América", 2007)))
''',
            [("Filtra continente e ano", "assert filtrar(df, 'Ásia', 2007)['pais'].tolist() == ['Japão']"), ("Indicador com 1 casa", "assert indicador(filtrar(df, 'América', 2007)) == 75.5, f'deu {indicador(filtrar(df, \"América\", 2007))}'")],
            '''
import pandas as pd

df = pd.DataFrame({
    "pais": ["Brasil", "Chile", "Japão", "Índia"],
    "continente": ["América", "América", "Ásia", "Ásia"],
    "ano": [2007, 2007, 2007, 2002],
    "vida": [72.4, 78.6, 82.6, 62.9],
})

def filtrar(df, continente, ano):
    return df[(df["continente"] == continente) & (df["ano"] == ano)]

def indicador(df):
    return round(df["vida"].mean(), 1)

print(indicador(filtrar(df, "América", 2007)))
''', ["Combine as condições com <code>&amp;</code>.", "<code>round(df[\"vida\"].mean(), 1)</code>"], exp="<p>Funções puras assim podem ser testadas sem abrir o navegador.</p>"),
        erros([
            ("Carregar o dataset sem cache.", "Cada clique relê o arquivo. Use <code>@st.cache_data</code>."),
            ("Toda a lógica misturada com <code>st.</code>.", "Separe funções de dados (testáveis) da interface."),
            ("Publicar com a chave de API no código.", "Use <code>st.secrets</code>."),
        ]),
        ponte("Demos de IA",
              "<p>Streamlit (e o Gradio, Fase 6) é a forma mais rápida de transformar um modelo em algo que outras pessoas experimentam: um campo de texto, um botão “Classificar” e o resultado. Para portfólio, um link de demo vale mais do que mil linhas de README.</p>"),
        quiz([
            ("O que acontece num app Streamlit quando o usuário mexe num filtro?", ["Nada.", "O script roda de novo inteiro.", "Só aquela linha roda."], 1, "Por isso o cache é importante."),
            ("Para que serve <code>@st.cache_data</code>?", ["Salvar o app.", "Evitar recalcular funções caras a cada interação.", "Esconder dados."], 1, "Guarda resultados."),
            ("Qual comando roda o app?", ["<code>python app.py</code>", "<code>streamlit run app.py</code>", "<code>pip run app.py</code>"], 1, "Abre no navegador."),
        ]),
    ],
    ["Streamlit transforma um script Python num app web interativo.", "Cada interação reexecuta o script: use cache.", "Separe a lógica (testável) da interface."],
    "Fase 3: Machine Learning clássico, começando por supervisionado e não supervisionado.",
    livro=("MLCC:", "Google Machine Learning Crash Course, visão geral", "Que problemas o curso usa como exemplos práticos?"))
