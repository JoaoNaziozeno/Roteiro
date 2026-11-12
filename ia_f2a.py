# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 2 (parte A): NumPy, Pandas, visualização e ambiente."""
from lesson_factory import *

AULAS = {}

AULAS["NumPy: arrays e operações vetorizadas"] = aula(
    40,
    "Somar um milhão de números com um laço Python leva segundos. Com NumPy, milissegundos. Não é truque: o NumPy faz a conta inteira em código compilado, de uma vez. Toda a IA em Python, de pandas a PyTorch, está construída sobre essa ideia.",
    ["criar arrays e entender <code>shape</code> e <code>dtype</code>;", "fazer operações vetorizadas sem laço;", "usar agregações como <code>sum</code>, <code>mean</code> e <code>argmax</code>."],
    ["Listas e laços (Fase 1)."],
    [
        chute("O que esse código imprime?", ["[1, 2, 3, 1, 2, 3]", "[2 4 6]", "Dá erro"], 1,
              ["Isso aconteceria com uma <b>lista</b> Python: <code>lista * 2</code> repete a lista.", "Isso! Num array, a operação vale para <b>cada elemento</b>: é a vetorização.", "Multiplicar array por número é a operação mais comum do NumPy."],
              "Array não é lista: as operações agem elemento a elemento.",
              cod='import numpy as np\nv = np.array([1, 2, 3])\nprint(v * 2)'),
        concreto("A planilha que calcula a coluna inteira", "<p>No Excel você escreve a fórmula uma vez e arrasta para a coluna toda. Você não faz célula por célula. O NumPy é isso para Python: <code>precos * 1.1</code> reajusta um milhão de preços de uma vez.</p>"),
        crianca("<p>Uma lista é uma <b>fila de pessoas</b>, cada uma diferente. Um array é um <b>pelotão</b>: todos do mesmo tipo, em formação, obedecendo à mesma ordem ao mesmo tempo. Por isso ele é tão rápido.</p>"),
        ver("as diferenças que o professor mostra entre lista e array"),
        nota("O essencial do NumPy", [
            ("<code>np.array([1, 2, 3])</code>", "criar", "Também <code>np.zeros(5)</code>, <code>np.ones((2, 3))</code>, <code>np.arange(0, 10, 2)</code>, <code>np.linspace(0, 1, 5)</code>."),
            ("<code>a.shape</code>", "formato", "Tupla com o tamanho de cada dimensão: <code>(3,)</code>, <code>(2, 3)</code>."),
            ("<code>a.dtype</code>", "tipo", "Todos os elementos têm o mesmo tipo: <code>int64</code>, <code>float32</code>..."),
            ("<code>a + b</code>, <code>a * 2</code>, <code>np.sqrt(a)</code>", "vetorização", "Contas elemento a elemento, sem laço."),
            ("<code>a.sum()</code>, <code>a.mean()</code>, <code>a.max()</code>, <code>a.argmax()</code>", "agregações", "Resumem o array. <code>argmax</code> devolve a <b>posição</b> do maior."),
            ("<code>a.reshape(2, 3)</code>", "remodelar", "Mesmos dados, outro formato."),
        ]),
        passos("Média ponderada sem laço", [
            ("<code>notas = np.array([7, 8, 10])</code> e <code>pesos = np.array([2, 3, 5])</code>", "Dois arrays do mesmo tamanho."),
            ("<code>notas * pesos</code> → <code>[14 24 50]</code>", "Multiplica posição a posição."),
            ("<code>(notas * pesos).sum()</code> → 88", "Soma tudo."),
            ("Dividido por <code>pesos.sum()</code> (10) → 8.8", "Uma linha, nenhum laço."),
        ], fim="Isso é, literalmente, o <b>produto escalar</b> da aula de Matemática: <code>notas @ pesos</code> dá 88."),
        cod("Normalizando dados", "Complete a função para devolver o array <b>padronizado</b>: subtraia a média e divida pelo desvio padrão. Sem laços.",
            '''
import numpy as np

def padronizar(x):
    return x

v = np.array([2.0, 4.0, 6.0, 8.0])
print(padronizar(v).round(3))
''',
            [("Média vira 0", "import numpy as np\nr = padronizar(np.array([2.0, 4.0, 6.0, 8.0]))\nassert abs(r.mean()) < 1e-9, f'média = {r.mean()}'"),
             ("Desvio vira 1", "import numpy as np\nr = padronizar(np.array([2.0, 4.0, 6.0, 8.0]))\nassert abs(r.std() - 1) < 1e-9, f'desvio = {r.std()}'"),
             ("Devolve um array", "import numpy as np\nassert isinstance(padronizar(np.array([1.0, 3.0])), np.ndarray)")],
            '''
import numpy as np

def padronizar(x):
    return (x - x.mean()) / x.std()

v = np.array([2.0, 4.0, 6.0, 8.0])
print(padronizar(v).round(3))
''', ["<code>x.mean()</code> e <code>x.std()</code> dão média e desvio.", "<code>(x - x.mean()) / x.std()</code> faz tudo de uma vez."]),
        cod("A classe mais provável", "Um classificador devolveu as probabilidades de 3 classes para 4 imagens (uma linha por imagem). Devolva um array com o <b>índice da classe mais provável</b> de cada imagem.",
            '''
import numpy as np

probs = np.array([
    [0.1, 0.7, 0.2],
    [0.8, 0.1, 0.1],
    [0.3, 0.3, 0.4],
    [0.2, 0.5, 0.3],
])

previsao = None
print(previsao)
''',
            [("Previsões corretas", "assert list(previsao) == [1, 0, 2, 1], f'previsao = {previsao}'")],
            '''
import numpy as np

probs = np.array([
    [0.1, 0.7, 0.2],
    [0.8, 0.1, 0.1],
    [0.3, 0.3, 0.4],
    [0.2, 0.5, 0.3],
])

previsao = probs.argmax(axis=1)
print(previsao)
''', ["<code>argmax</code> devolve a posição do maior.", "<code>axis=1</code> faz a conta ao longo de cada linha."], rot="Mão no código · nível 2 · ponte para IA"),
        erros([
            ("Percorrer um array com <code>for</code> para fazer contas.", "Funciona, mas joga fora a velocidade. Procure a operação vetorizada."),
            ("Misturar tipos: <code>np.array([1, \"a\"])</code>.", "Tudo vira texto e as contas param de funcionar."),
            ("Confundir <code>axis=0</code> e <code>axis=1</code>.", "<code>axis=0</code> percorre as linhas (resultado por coluna); <code>axis=1</code>, as colunas (resultado por linha)."),
        ]),
        ponte("Tudo é array",
              "<p>Uma imagem é um array <code>(altura, largura, 3)</code>. Um lote de frases tokenizadas, <code>(lote, tokens)</code>. Os pesos de uma camada, <code>(entradas, saídas)</code>. Tensores do PyTorch funcionam exatamente como arrays do NumPy, com a vantagem de rodar na GPU e calcular gradientes.</p>"),
        quiz([
            ("Qual o <code>shape</code> de <code>np.zeros((3, 4))</code>?", ["(4, 3)", "(3, 4)", "12"], 1, "3 linhas e 4 colunas."),
            ("O que <code>np.array([1, 2]) + np.array([10, 20])</code> dá?", ["[1, 2, 10, 20]", "[11 22]", "33"], 1, "Soma elemento a elemento."),
            ("Por que o NumPy é mais rápido que laços Python?", ["Usa a GPU sempre.", "Faz as contas em código compilado, sobre blocos de dados do mesmo tipo.", "Pula elementos."], 1, "Vetorização."),
        ]),
    ],
    ["Array é um bloco de dados do mesmo tipo, com <code>shape</code> e <code>dtype</code>.", "Operações são vetorizadas: valem para todos os elementos, sem laço.", "Agregações com <code>axis</code> resumem por linha ou por coluna."],
    "Pandas: tabelas com nome de coluna.",
    livro=("PDSH:02.00-introduction-to-numpy", "Capítulo 2, “Introduction to NumPy”", "Por que o livro diz que arrays são mais eficientes que listas?"))

AULAS["Pandas: DataFrames e Series"] = aula(
    40,
    "O NumPy entende números em formação. O Pandas entende <b>tabelas</b>: colunas com nome, tipos diferentes por coluna, linhas com rótulo. É o Excel do cientista de dados, com a vantagem de cada passo ficar registrado em código.",
    ["criar e ler um DataFrame;", "selecionar colunas e linhas com <code>loc</code> e <code>iloc</code>;", "inspecionar dados com <code>head</code>, <code>info</code> e <code>describe</code>."],
    ["NumPy: arrays e operações vetorizadas."],
    [
        chute("Num DataFrame <code>df</code>, o que <code>df[\"idade\"]</code> devolve?", ["Uma linha.", "Uma coluna (uma Series).", "O número de colunas."], 1,
              ["Linhas são selecionadas com <code>loc</code> ou <code>iloc</code>.", "Isso! Colchetes com o nome pegam a coluna, que é uma <b>Series</b>.", "Isso seria <code>df.shape[1]</code>."],
              "DataFrame = várias Series lado a lado, compartilhando o mesmo índice."),
        concreto("A planilha com superpoderes", "<p>Um DataFrame é uma planilha: colunas com nome, uma linha por registro. A diferença é que, em vez de clicar, você <b>escreve</b> o que quer: “filtre quem tem mais de 30, agrupe por cidade, tire a média”. E pode repetir isso amanhã com dados novos.</p>"),
        nota("Peças do Pandas", [
            ("<code>pd.DataFrame({\"col\": [...]})</code>", "criar", "A partir de um dicionário de listas. Ou <code>pd.read_csv(\"arquivo.csv\")</code>."),
            ("<code>df.head()</code>, <code>df.info()</code>, <code>df.describe()</code>", "inspecionar", "Primeiras linhas; tipos e nulos; estatísticas das colunas numéricas."),
            ("<code>df[\"col\"]</code> / <code>df[[\"a\", \"b\"]]</code>", "colunas", "Uma coluna (Series) ou várias (DataFrame)."),
            ("<code>df.loc[rótulo, \"col\"]</code>", "por rótulo", "Seleciona pelo nome do índice e da coluna."),
            ("<code>df.iloc[0, 2]</code>", "por posição", "Seleciona pela posição numérica, como em listas."),
            ("<code>df[\"nova\"] = df[\"a\"] * 2</code>", "nova coluna", "Operações em colunas são vetorizadas."),
        ]),
        passos("Primeiro contato com um dataset", [
            ("<code>df = pd.read_csv(\"vendas.csv\")</code>", "Carrega a tabela."),
            ("<code>df.shape</code>", "Quantas linhas e colunas."),
            ("<code>df.head()</code>", "Dá uma olhada nas primeiras linhas."),
            ("<code>df.info()</code>", "Tipos e valores ausentes por coluna."),
            ("<code>df.describe()</code>", "Média, mínimo, máximo e quartis."),
        ], fim="Esses cinco comandos são o “bom dia” de qualquer análise."),
        cod("Seu primeiro DataFrame", "Crie o DataFrame <code>df</code> com as colunas <code>produto</code>, <code>preco</code> e <code>qtd</code> a partir do dicionário, e acrescente a coluna <code>total</code> (preço × quantidade).",
            '''
import pandas as pd

dados = {"produto": ["caneta", "caderno", "mochila"], "preco": [2.5, 18.0, 120.0], "qtd": [10, 3, 1]}

df = None

print(df)
''',
            [("É um DataFrame com 3 linhas", "import pandas as pd\nassert isinstance(df, pd.DataFrame) and len(df) == 3"),
             ("Coluna total correta", "assert list(df['total']) == [25.0, 54.0, 120.0], f'total = {list(df[\"total\"])}'")],
            '''
import pandas as pd

dados = {"produto": ["caneta", "caderno", "mochila"], "preco": [2.5, 18.0, 120.0], "qtd": [10, 3, 1]}

df = pd.DataFrame(dados)
df["total"] = df["preco"] * df["qtd"]

print(df)
''', ["<code>df = pd.DataFrame(dados)</code>", "<code>df[\"total\"] = df[\"preco\"] * df[\"qtd\"]</code>"]),
        cod("loc e iloc", "Use <code>loc</code> para pegar o preço do <b>caderno</b> (o índice é o nome do produto) e <code>iloc</code> para pegar a quantidade da <b>última</b> linha.",
            '''
import pandas as pd

df = pd.DataFrame({"preco": [2.5, 18.0, 120.0], "qtd": [10, 3, 1]}, index=["caneta", "caderno", "mochila"])

preco_caderno = None
qtd_ultima = None

print(preco_caderno, qtd_ultima)
''',
            [("Preço do caderno", "assert preco_caderno == 18.0, f'deu {preco_caderno}'"), ("Quantidade da última linha", "assert qtd_ultima == 1, f'deu {qtd_ultima}'")],
            '''
import pandas as pd

df = pd.DataFrame({"preco": [2.5, 18.0, 120.0], "qtd": [10, 3, 1]}, index=["caneta", "caderno", "mochila"])

preco_caderno = df.loc["caderno", "preco"]
qtd_ultima = df.iloc[-1, 1]

print(preco_caderno, qtd_ultima)
''', ["<code>df.loc[\"caderno\", \"preco\"]</code>", "<code>df.iloc[-1, 1]</code>: última linha, segunda coluna."], rot="Mão no código · nível 2"),
        erros([
            ("<code>df[\"col\"][0] = valor</code> (atribuição encadeada).", "Pode alterar uma cópia e não o DataFrame. Use <code>df.loc[0, \"col\"] = valor</code>."),
            ("Confundir <code>loc</code> e <code>iloc</code>.", "<code>loc</code> usa rótulos; <code>iloc</code>, posições. Com índice numérico, eles parecem iguais até deixarem de ser."),
            ("Percorrer linhas com <code>for</code> para fazer contas.", "Opere nas colunas inteiras: é mais rápido e mais claro."),
        ]),
        ponte("O DataFrame no caminho até o modelo",
              "<p>Quase todo projeto de ML clássico passa por um DataFrame: carregar, limpar, criar atributos, separar <code>X = df[colunas]</code> e <code>y = df[\"alvo\"]</code>. O scikit-learn aceita DataFrames diretamente. Para LLMs, datasets de avaliação também costumam viver em tabelas.</p>"),
        quiz([
            ("Qual comando mostra tipos e valores ausentes?", ["<code>df.head()</code>", "<code>df.info()</code>", "<code>df.describe()</code>"], 1, "<code>info</code> lista colunas, tipos e não nulos."),
            ("<code>df.iloc[0]</code> devolve:", ["A primeira coluna.", "A primeira linha.", "O primeiro valor."], 1, "Posição 0 nas linhas."),
            ("Como selecionar as colunas a e b?", ["<code>df[\"a\", \"b\"]</code>", "<code>df[[\"a\", \"b\"]]</code>", "<code>df.a.b</code>"], 1, "Uma lista de nomes dentro dos colchetes."),
        ]),
    ],
    ["DataFrame é uma tabela de Series com o mesmo índice.", "<code>loc</code> seleciona por rótulo; <code>iloc</code>, por posição.", "<code>head</code>, <code>info</code> e <code>describe</code> são o primeiro passo de toda análise."],
    "Filtrar, agrupar e juntar tabelas.",
    livro=("PDA:chapter-5-pandas-basics", "Capítulo 5, “Getting Started with pandas”", "Como o livro explica o alinhamento automático pelo índice?"))

AULAS["Pandas: filtrar, agrupar e juntar (merge)"] = aula(
    45,
    "“Qual cidade vendeu mais no último trimestre, e quais clientes de lá compraram mais de uma vez?” Três operações respondem a quase qualquer pergunta de negócio: <b>filtrar</b>, <b>agrupar</b> e <b>juntar</b>.",
    ["filtrar linhas com condições;", "agrupar e agregar com <code>groupby</code>;", "juntar tabelas com <code>merge</code>."],
    ["Pandas: DataFrames e Series."],
    [
        chute("O que <code>df[df[\"idade\"] &gt; 30]</code> devolve?", ["Uma coluna de True e False.", "Só as linhas em que a idade é maior que 30.", "O número de pessoas com mais de 30."], 1,
              ["Isso é só a parte de dentro: <code>df[\"idade\"] &gt; 30</code>, a máscara.", "Isso! A máscara de True/False, colocada dentro de <code>df[...]</code>, filtra as linhas.", "Para contar, some a máscara: <code>(df[\"idade\"] &gt; 30).sum()</code>."],
              "Filtrar = criar uma máscara booleana e usá-la como índice."),
        concreto("O relatório do gerente", "<p>O gerente pede: “só as vendas de março” (<b>filtrar</b>), “total por vendedor” (<b>agrupar</b>), “com o nome da loja de cada um” (<b>juntar</b> com a tabela de lojas). É o mesmo que um SQL com <code>WHERE</code>, <code>GROUP BY</code> e <code>JOIN</code>.</p>"),
        nota("As três operações", [
            ("<code>df[(df.a &gt; 1) &amp; (df.b == \"x\")]</code>", "filtrar", "Combine condições com <code>&amp;</code> (e) e <code>|</code> (ou), cada uma entre parênteses."),
            ("<code>df.query(\"a &gt; 1 and b == 'x'\")</code>", "filtrar em texto", "Mais legível para filtros longos."),
            ("<code>df.groupby(\"cidade\")[\"valor\"].sum()</code>", "agrupar", "Separa por cidade, aplica a soma em cada grupo, junta os resultados."),
            ("<code>.agg(total=(\"valor\", \"sum\"), n=(\"valor\", \"count\"))</code>", "várias agregações", "Nomeia cada resultado."),
            ("<code>pd.merge(a, b, on=\"id\", how=\"left\")</code>", "juntar", "<code>how</code>: <code>inner</code> (só os que casam), <code>left</code> (todos da esquerda), <code>outer</code> (todos)."),
        ]),
        passos("Separar, aplicar, combinar", [
            ("<code>groupby(\"cidade\")</code> separa as linhas em grupos.", "Um grupo por cidade."),
            ("<code>[\"valor\"].sum()</code> aplica a soma dentro de cada grupo.", "Uma conta por grupo."),
            ("O resultado combina tudo numa Series indexada pela cidade.", "Use <code>.reset_index()</code> para voltar a ser tabela."),
        ], fim="Esse padrão tem nome: <i>split-apply-combine</i>."),
        cod("Filtrar e agrupar", "Calcule o <b>total vendido por cidade</b>, considerando só as vendas acima de 50. O resultado deve ser uma Series <code>total</code>, indexada pela cidade.",
            '''
import pandas as pd

vendas = pd.DataFrame({
    "cidade": ["Recife", "Natal", "Recife", "Natal", "Recife"],
    "valor": [100, 40, 60, 80, 30],
})

total = None
print(total)
''',
            [("Recife 160, Natal 80", "assert total.to_dict() == {'Natal': 80, 'Recife': 160}, f'total = {total.to_dict()}'")],
            '''
import pandas as pd

vendas = pd.DataFrame({
    "cidade": ["Recife", "Natal", "Recife", "Natal", "Recife"],
    "valor": [100, 40, 60, 80, 30],
})

total = vendas[vendas["valor"] > 50].groupby("cidade")["valor"].sum()
print(total)
''', ["Primeiro filtre: <code>vendas[vendas[\"valor\"] &gt; 50]</code>.", "Depois <code>.groupby(\"cidade\")[\"valor\"].sum()</code>."]),
        cod("Juntando tabelas", "Junte <code>pedidos</code> e <code>clientes</code> pela coluna <code>id_cliente</code>, mantendo <b>todos os pedidos</b> (mesmo sem cliente cadastrado). Depois conte quantos pedidos ficaram sem nome.",
            '''
import pandas as pd

pedidos = pd.DataFrame({"id_pedido": [1, 2, 3, 4], "id_cliente": [10, 20, 10, 99]})
clientes = pd.DataFrame({"id_cliente": [10, 20], "nome": ["Ana", "Bia"]})

juntos = None
sem_nome = None
print(juntos, sem_nome)
''',
            [("Mantém os 4 pedidos", "assert len(juntos) == 4, f'{len(juntos)} linhas'"), ("Um pedido sem nome", "assert sem_nome == 1, f'sem_nome = {sem_nome}'")],
            '''
import pandas as pd

pedidos = pd.DataFrame({"id_pedido": [1, 2, 3, 4], "id_cliente": [10, 20, 10, 99]})
clientes = pd.DataFrame({"id_cliente": [10, 20], "nome": ["Ana", "Bia"]})

juntos = pd.merge(pedidos, clientes, on="id_cliente", how="left")
sem_nome = juntos["nome"].isna().sum()
print(juntos, sem_nome)
''', ["<code>how=\"left\"</code> mantém todos os pedidos.", "<code>juntos[\"nome\"].isna().sum()</code> conta os vazios."], rot="Mão no código · nível 2"),
        erros([
            ("<code>df[df.a &gt; 1 and df.b &lt; 5]</code>", "Com Series, use <code>&amp;</code> e <code>|</code>, e parênteses em cada condição."),
            ("Merge que multiplica linhas.", "Se a chave se repete nas duas tabelas, cada combinação vira uma linha. Confira o tamanho antes e depois."),
            ("Esquecer o <code>how</code> no merge.", "O padrão é <code>inner</code>: linhas sem par somem em silêncio."),
        ]),
        ponte("Agrupar para entender o modelo",
              "<p>Depois de treinar, a pergunta mais importante é: <b>onde o modelo erra?</b> Um <code>groupby</code> por região, faixa etária ou categoria mostra a acurácia de cada grupo, e revela vieses que a média geral esconde.</p>"),
        quiz([
            ("Como combinar duas condições num filtro?", ["<code>and</code>", "<code>&amp;</code>, com parênteses em cada condição", "<code>+</code>"], 1, "Operadores elemento a elemento."),
            ("O que <code>how=\"left\"</code> faz num merge?", ["Mantém só as linhas que casam.", "Mantém todas as linhas da tabela da esquerda.", "Ordena pela esquerda."], 1, "As sem par ficam com valores ausentes."),
            ("<code>df.groupby(\"loja\")[\"valor\"].mean()</code> calcula:", ["A média geral.", "A média de valor por loja.", "Quantas lojas existem."], 1, "Uma média para cada grupo."),
        ]),
    ],
    ["Filtrar é usar uma máscara booleana dentro de <code>df[...]</code>.", "<code>groupby</code> separa, aplica e combina.", "<code>merge</code> junta tabelas por uma chave; escolha o <code>how</code> com cuidado."],
    "Limpeza de dados: lidar com o que falta.",
    livro=("PDA:chapter-10-data-aggregation-and-group-operations", "Capítulo 10, “Data Aggregation and Group Operations”", "Que exemplos de agg com várias funções o livro mostra?"))

AULAS["Limpeza de dados e valores ausentes"] = aula(
    40,
    "Dados reais vêm sujos: campos vazios, “N/A”, idade 999, “São Paulo” e “sao paulo” como cidades diferentes. Cientistas de dados passam boa parte do tempo limpando, e um modelo treinado em dados sujos aprende a sujeira.",
    ["encontrar valores ausentes com <code>isna</code>;", "decidir entre remover e preencher;", "padronizar textos e tipos."],
    ["Pandas: filtrar, agrupar e juntar."],
    [
        chute("Uma coluna <code>salario</code> tem 3% de valores ausentes. Qual a escolha mais segura para começar?", ["Preencher com zero.", "Preencher com a mediana e registrar quais eram ausentes.", "Apagar a coluna."], 1,
              ["Zero é um salário falso: puxa a média para baixo e engana o modelo.", "Isso! A mediana resiste a valores extremos, e a coluna indicadora preserva a informação de que o dado faltava.", "Com só 3% de ausentes, a coluna ainda é valiosa."],
              "Ausência também é informação: às vezes, “não informou” diz muito."),
        concreto("A ficha de cadastro", "<p>Num cadastro em papel, há campos em branco, letra ilegível e gente que escreveu a cidade de três jeitos. Antes de tirar qualquer conclusão, alguém precisa <b>conferir e padronizar</b> as fichas. Limpeza de dados é esse trabalho, feito em código para ser repetível.</p>"),
        nota("Ferramentas de limpeza", [
            ("<code>df.isna().sum()</code>", "ausentes por coluna", "Primeira coisa a olhar."),
            ("<code>df.dropna(subset=[\"col\"])</code>", "remover", "Tira as linhas com ausente naquela coluna."),
            ("<code>df[\"col\"].fillna(valor)</code>", "preencher", "Com média, mediana, moda ou um valor fixo."),
            ("<code>df[\"col\"].str.strip().str.lower()</code>", "padronizar texto", "Tira espaços e unifica maiúsculas."),
            ("<code>pd.to_numeric(df[\"col\"], errors=\"coerce\")</code>", "converter tipo", "O que não for número vira ausente, em vez de dar erro."),
            ("<code>df.replace({\"N/A\": np.nan})</code>", "marcadores falsos", "Transforma “N/A”, “-” e afins em ausentes de verdade."),
        ]),
        passos("Um roteiro de limpeza", [
            ("Olhe: <code>info()</code>, <code>isna().sum()</code>, <code>value_counts()</code> nas colunas de texto.", "Descubra os problemas antes de mexer."),
            ("Converta tipos: números que chegaram como texto.", "Use <code>errors=\"coerce\"</code> e conte quantos viraram ausentes."),
            ("Padronize textos: espaços, maiúsculas, acentos.", "“Recife ” e “recife” viram a mesma cidade."),
            ("Trate ausentes: remova ou preencha, coluna por coluna.", "A decisão depende do significado do dado."),
            ("Confira de novo.", "Limpeza também tem bugs."),
        ]),
        cod("Limpando um cadastro", "Limpe o DataFrame: padronize a cidade (sem espaços nas pontas, em minúsculas), converta <code>idade</code> para número (o que não for número vira ausente) e preencha as idades ausentes com a <b>mediana</b>.",
            '''
import pandas as pd

df = pd.DataFrame({
    "cidade": [" Recife", "recife", "NATAL ", "Natal"],
    "idade": ["30", "N/A", "25", "40"],
})

# limpe aqui

print(df)
''',
            [("Cidades padronizadas", "assert list(df['cidade']) == ['recife', 'recife', 'natal', 'natal'], f'cidades = {list(df[\"cidade\"])}'"),
             ("Idade numérica e sem ausentes", "assert df['idade'].isna().sum() == 0 and df['idade'].dtype.kind in 'if'"),
             ("Ausente virou a mediana (30)", "assert df['idade'].tolist() == [30.0, 30.0, 25.0, 40.0], f'idades = {df[\"idade\"].tolist()}'")],
            '''
import pandas as pd

df = pd.DataFrame({
    "cidade": [" Recife", "recife", "NATAL ", "Natal"],
    "idade": ["30", "N/A", "25", "40"],
})

df["cidade"] = df["cidade"].str.strip().str.lower()
df["idade"] = pd.to_numeric(df["idade"], errors="coerce")
df["idade"] = df["idade"].fillna(df["idade"].median())

print(df)
''', ["Texto: <code>.str.strip().str.lower()</code>.", "Número: <code>pd.to_numeric(..., errors=\"coerce\")</code>, depois <code>.fillna(df[\"idade\"].median())</code>."]),
        erros([
            ("<code>dropna()</code> sem pensar.", "Pode apagar metade dos dados. Veja quantas linhas sobram e se os removidos são parecidos com os que ficam."),
            ("Preencher com a média antes de separar treino e teste.", "A média “vaza” informação do teste para o treino. Calcule-a só no treino (aula de vazamento de dados)."),
            ("Limpar no Excel à mão.", "Não é reproduzível. No próximo arquivo, tudo de novo."),
        ]),
        ponte("Lixo entra, lixo sai",
              "<p>Para LLMs, a limpeza dos dados de treino (remover duplicados, textos tóxicos, lixo de páginas web) é parte central do que faz um modelo ser bom. Em RAG, documentos mal extraídos geram respostas ruins. Qualidade de dados é, muitas vezes, o maior ganho disponível.</p>"),
        quiz([
            ("Como contar os ausentes de cada coluna?", ["<code>df.count()</code>", "<code>df.isna().sum()</code>", "<code>df.missing()</code>"], 1, "<code>isna</code> marca; <code>sum</code> conta."),
            ("Por que preferir a mediana à média para preencher salários?", ["É mais rápida.", "Não é distorcida por poucos valores muito altos.", "É sempre maior."], 1, "A mediana é robusta a extremos."),
            ("O que <code>errors=\"coerce\"</code> faz em <code>to_numeric</code>?", ["Ignora a coluna.", "Transforma o que não é número em ausente.", "Arredonda os números."], 1, "Em vez de dar erro."),
        ]),
    ],
    ["Olhe antes de limpar: tipos, ausentes e contagens de valores.", "Remover ou preencher é uma decisão por coluna, com base no significado.", "Padronize textos e converta tipos de forma reproduzível."],
    "Matplotlib: transformar dados em gráficos.",
    livro=("PDA:chapter-7-data-cleaning-and-preparation", "Capítulo 7, “Data Cleaning and Preparation”", "Que estratégias de preenchimento o livro apresenta?"))

AULAS["Matplotlib"] = aula(
    35,
    "Uma tabela com mil números não diz nada. Um gráfico mostra, em um segundo, a tendência, o pico e o ponto estranho. O Matplotlib é a base sobre a qual quase toda visualização em Python é construída.",
    ["criar gráficos de linha, barras, dispersão e histograma;", "usar figura e eixos (<code>fig, ax</code>);", "rotular eixos e título para o gráfico se explicar sozinho."],
    ["NumPy e Pandas."],
    [
        chute("Você quer ver a <b>distribuição</b> das idades dos clientes. Qual gráfico?", ["Linha.", "Histograma.", "Pizza."], 1,
              ["Linha mostra evolução no tempo.", "Isso! O histograma conta quantos valores caem em cada faixa.", "Pizza compara partes de um todo, e mal."],
              "Primeiro decida a <b>pergunta</b>; o tipo de gráfico vem dela."),
        concreto("A pergunta escolhe o gráfico", "<p>Evolução no tempo: <b>linha</b>. Comparar categorias: <b>barras</b>. Relação entre duas variáveis: <b>dispersão</b>. Como os valores se espalham: <b>histograma</b>. Errar o tipo é como responder a outra pergunta.</p>"),
        tabela("Qual gráfico para qual pergunta", ["Pergunta", "Gráfico", "Matplotlib"], [
            ["Como mudou ao longo do tempo?", "Linha", "<code>ax.plot(x, y)</code>"],
            ["Qual categoria é maior?", "Barras", "<code>ax.bar(categorias, valores)</code>"],
            ["Duas variáveis andam juntas?", "Dispersão", "<code>ax.scatter(x, y)</code>"],
            ["Como os valores se distribuem?", "Histograma", "<code>ax.hist(valores, bins=20)</code>"],
        ]),
        nota("Figura e eixos", [
            ("<code>fig, ax = plt.subplots()</code>", "criar", "<code>fig</code> é a folha; <code>ax</code> é a área do gráfico."),
            ("<code>ax.set_title</code>, <code>set_xlabel</code>, <code>set_ylabel</code>", "rotular", "Gráfico sem rótulo não se explica."),
            ("<code>fig, axs = plt.subplots(1, 2)</code>", "vários gráficos", "Uma figura com dois eixos lado a lado."),
            ("<code>fig.savefig(\"g.png\", dpi=150)</code>", "salvar", "Para o README ou o relatório."),
        ]),
        lab("Curva de aprendizado", '''
import matplotlib.pyplot as plt

epocas = list(range(1, 11))
perda_treino = [2.3, 1.6, 1.2, 0.9, 0.7, 0.55, 0.45, 0.38, 0.33, 0.30]
perda_valid = [2.4, 1.7, 1.3, 1.05, 0.9, 0.85, 0.84, 0.86, 0.9, 0.95]

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(epocas, perda_treino, marker="o", label="treino")
ax.plot(epocas, perda_valid, marker="o", label="validação")
ax.set_title("Curva de aprendizado")
ax.set_xlabel("época")
ax.set_ylabel("perda")
ax.legend()
plt.show()
''', corpo="<p>Rode no Colab ou no Jupyter. É o gráfico mais olhado por quem treina modelos:</p>",
            exps=["A partir de que época a perda de validação para de cair e começa a subir? O que isso indica? (Dica: overfitting, Fase 3.)", "Acrescente <code>ax.axvline(7, linestyle=\"--\")</code> para marcar a melhor época."]),
        cod("Escolhendo a melhor época", "Sem gráfico, encontre o número da época (contando a partir de 1) com a <b>menor perda de validação</b>. É o ponto que você marcaria no gráfico.",
            '''
import numpy as np

perda_valid = np.array([2.4, 1.7, 1.3, 1.05, 0.9, 0.85, 0.84, 0.86, 0.9, 0.95])

melhor_epoca = None
print(melhor_epoca)
''',
            [("Época 7", "assert melhor_epoca == 7, f'deu {melhor_epoca}'")],
            '''
import numpy as np

perda_valid = np.array([2.4, 1.7, 1.3, 1.05, 0.9, 0.85, 0.84, 0.86, 0.9, 0.95])

melhor_epoca = int(perda_valid.argmin()) + 1
print(melhor_epoca)
''', ["<code>argmin()</code> dá a posição do menor (começando em 0)."]),
        erros([
            ("Eixo y começando longe do zero em gráfico de barras.", "Diferenças pequenas parecem enormes. Barras começam no zero."),
            ("Gráfico sem título e sem rótulos.", "Quem olha precisa saber o que é cada eixo e a unidade."),
            ("Pizza com muitas fatias.", "Olhos comparam mal ângulos. Barras ordenadas quase sempre são melhores."),
        ]),
        ponte("Gráficos que você vai fazer em IA",
              "<p>Curvas de perda e acurácia, matriz de confusão, curva ROC, importância de atributos, exemplos de imagens mal classificadas. Ferramentas como TensorBoard e Weights &amp; Biases desenham automaticamente, mas por baixo é o mesmo raciocínio: escolher o gráfico que responde à pergunta.</p>"),
        quiz([
            ("Para mostrar a relação entre altura e peso, use:", ["Histograma.", "Dispersão.", "Pizza."], 1, "Um ponto por pessoa."),
            ("O que <code>fig, ax = plt.subplots()</code> devolve?", ["Uma tabela.", "A figura e a área de desenho.", "Dois gráficos."], 1, "Folha e eixos."),
            ("Por que barras devem começar no zero?", ["Por estética.", "Porque o comprimento da barra representa o valor.", "Porque o Matplotlib exige."], 1, "Cortar o eixo distorce a comparação."),
        ]),
    ],
    ["A pergunta escolhe o gráfico: linha, barras, dispersão ou histograma.", "<code>fig, ax = plt.subplots()</code> e métodos no <code>ax</code>.", "Título e rótulos fazem o gráfico se explicar sozinho."],
    "Seaborn: gráficos estatísticos com menos código.",
    livro=("PDSH:04.00-introduction-to-matplotlib", "Capítulo 4, “Visualization with Matplotlib”", "Qual a diferença entre a interface MATLAB e a orientada a objetos, segundo o livro?"))

AULAS["Seaborn"] = aula(
    30,
    "O Matplotlib dá controle total, mas pede muitas linhas. O Seaborn conversa direto com DataFrames e faz, em uma linha, gráficos estatísticos que separam grupos por cor, desenham médias com intervalos e mostram correlações.",
    ["criar gráficos a partir de colunas de um DataFrame;", "separar grupos com <code>hue</code>;", "ler um mapa de calor de correlação."],
    ["Matplotlib e Pandas."],
    [
        chute("Num gráfico do Seaborn, para que serve o parâmetro <code>hue=\"sexo\"</code>?", ["Mudar o título.", "Colorir os pontos de acordo com a coluna sexo.", "Ordenar os dados."], 1,
              ["O título é definido à parte.", "Isso! <code>hue</code> separa os grupos por cor e cria a legenda sozinho.", "Ordenar não muda cores."],
              "Uma terceira variável, de graça, só com uma cor."),
        concreto("O fotógrafo com filtro pronto", "<p>Com o Matplotlib você ajusta cada detalhe da câmera. O Seaborn é a câmera com <b>modos prontos</b> para o que estatísticos fazem todo dia: comparar grupos, mostrar distribuição, ver correlação.</p>"),
        nota("Os gráficos mais usados", [
            ("<code>sns.histplot(df, x=\"idade\", hue=\"grupo\")</code>", "distribuição", "Histograma por grupo."),
            ("<code>sns.boxplot(df, x=\"cidade\", y=\"preco\")</code>", "caixa", "Mediana, quartis e valores extremos por categoria."),
            ("<code>sns.scatterplot(df, x=\"a\", y=\"b\", hue=\"c\")</code>", "dispersão", "Relação entre duas variáveis, colorida por uma terceira."),
            ("<code>sns.heatmap(df.corr(numeric_only=True), annot=True)</code>", "mapa de calor", "Correlação entre todas as colunas numéricas."),
            ("<code>sns.pairplot(df, hue=\"classe\")</code>", "pares", "Todas as dispersões de uma vez: ótimo para explorar."),
        ]),
        lab("Explorando um dataset clássico", '''
import seaborn as sns
import matplotlib.pyplot as plt

pinguins = sns.load_dataset("penguins").dropna()
sns.scatterplot(pinguins, x="flipper_length_mm", y="body_mass_g", hue="species")
plt.show()

sns.heatmap(pinguins.corr(numeric_only=True), annot=True, cmap="vlag", vmin=-1, vmax=1)
plt.show()
''', corpo="<p>Rode no Colab:</p>",
            exps=["As espécies se separam bem no gráfico de dispersão? Um classificador teria facilidade?", "Quais duas medidas têm a correlação mais forte no mapa de calor?"]),
        cod("Calculando a correlação", "O mapa de calor mostra correlações. Calcule, com Pandas, a correlação entre <code>horas</code> e <code>nota</code> e arredonde para 2 casas.",
            '''
import pandas as pd

df = pd.DataFrame({"horas": [1, 2, 3, 4, 5, 6], "nota": [4.0, 5.5, 6.0, 7.5, 8.0, 9.5]})

r = None
print(r)
''',
            [("Correlação ≈ 0.99", "assert r == 0.99, f'r = {r}'")],
            '''
import pandas as pd

df = pd.DataFrame({"horas": [1, 2, 3, 4, 5, 6], "nota": [4.0, 5.5, 6.0, 7.5, 8.0, 9.5]})

r = round(df["horas"].corr(df["nota"]), 2)
print(r)
''', ["<code>df[\"horas\"].corr(df[\"nota\"])</code> e depois <code>round(..., 2)</code>."]),
        erros([
            ("Ler correlação como causa.", "Sorvete e afogamentos sobem juntos no verão. Correlação não diz quem causa quem."),
            ("Mapa de calor com dezenas de colunas e números minúsculos.", "Escolha as colunas que importam para a pergunta."),
            ("Usar <code>pairplot</code> num dataset enorme.", "Fica lento e ilegível. Faça uma amostra com <code>df.sample(1000)</code>."),
        ]),
        ponte("Visualizar antes de modelar",
              "<p>Um <code>pairplot</code> colorido pela classe mostra, antes de qualquer treino, se as classes são separáveis e quais atributos ajudam. Um <code>boxplot</code> revela valores absurdos que derrubariam um modelo. Dez minutos de gráficos economizam horas de ajuste.</p>"),
        quiz([
            ("Qual gráfico mostra mediana, quartis e valores extremos?", ["Boxplot.", "Pizza.", "Linha."], 0, "A caixa resume a distribuição."),
            ("Uma correlação de -0.9 indica:", ["Nenhuma relação.", "Forte relação inversa.", "Que uma causa a outra."], 1, "Quando uma sobe, a outra desce."),
            ("Qual a vantagem do Seaborn sobre o Matplotlib puro?", ["É mais rápido para calcular.", "Faz gráficos estatísticos a partir de DataFrames com menos código.", "Não precisa de dados."], 1, "Construído sobre o Matplotlib."),
        ]),
    ],
    ["O Seaborn trabalha direto com colunas de DataFrames.", "<code>hue</code> separa grupos por cor.", "Correlação mostra relação, não causa."],
    "Análise exploratória: método para conhecer um dataset.",
    livro=("PDSH:04.14-visualization-with-seaborn", "Seção 4.14, “Visualization with Seaborn”", "Que tipos de gráfico o livro mostra com o dataset de maratonas?"))

AULAS["Análise exploratória de dados (EDA)"] = aula(
    45,
    "Antes de treinar qualquer modelo, é preciso conhecer os dados: o que cada coluna significa, como se distribuem, o que está faltando, o que parece errado. A análise exploratória é a conversa inicial com o dataset, e ela muda as perguntas que você vai fazer.",
    ["seguir um roteiro de EDA;", "analisar variáveis sozinhas e em pares;", "registrar descobertas e hipóteses."],
    ["Pandas, limpeza, Matplotlib e Seaborn."],
    [
        chute("Num dataset de fraudes, 99,5% das transações são legítimas. Um modelo que diz sempre “legítima” tem 99,5% de acerto. Isso é bom?", ["Sim, quase perfeito.", "Não: ele nunca pega uma fraude.", "Depende da GPU."], 1,
              ["A acurácia alta esconde que o modelo é inútil para o objetivo.", "Isso! A EDA mostra o <b>desequilíbrio</b> das classes logo no início, e muda a métrica que você vai usar.", "O hardware não muda a conclusão."],
              "A EDA evita que você comemore um modelo inútil."),
        concreto("O médico na primeira consulta", "<p>Antes de qualquer remédio, o médico pergunta, mede a pressão, olha os exames. Ele quer entender o paciente. A EDA é a primeira consulta: medir, olhar e anotar antes de tratar.</p>"),
        passos("Roteiro de EDA", [
            ("<b>Contexto</b>: o que é cada linha? Qual é o alvo? De onde vieram os dados?", "Sem isso, nenhum número faz sentido."),
            ("<b>Estrutura</b>: <code>shape</code>, <code>info()</code>, ausentes, duplicados.", "O tamanho do problema."),
            ("<b>Uma variável por vez</b>: <code>describe()</code>, histogramas, <code>value_counts()</code>.", "Distribuições, valores estranhos, categorias raras."),
            ("<b>Em relação ao alvo</b>: médias do alvo por categoria, dispersões, correlações.", "Quais atributos parecem ajudar a prever?"),
            ("<b>Anotar</b>: descobertas, problemas e hipóteses.", "Vira o plano de limpeza e de engenharia de atributos."),
        ]),
        cod("Um mini relatório", "Complete a função <code>resumo(df)</code> que devolve um dicionário com: <code>linhas</code>, <code>colunas</code>, <code>ausentes</code> (total de valores ausentes) e <code>duplicadas</code> (linhas repetidas).",
            '''
import pandas as pd

def resumo(df):
    return {}

df = pd.DataFrame({"a": [1, 2, 2, None], "b": ["x", "y", "y", "z"]})
print(resumo(df))
''',
            [("Resumo correto", "import pandas as pd\nd = pd.DataFrame({'a': [1, 2, 2, None], 'b': ['x', 'y', 'y', 'z']})\nassert resumo(d) == {'linhas': 4, 'colunas': 2, 'ausentes': 1, 'duplicadas': 1}, f'deu {resumo(d)}'")],
            '''
import pandas as pd

def resumo(df):
    return {
        "linhas": df.shape[0],
        "colunas": df.shape[1],
        "ausentes": int(df.isna().sum().sum()),
        "duplicadas": int(df.duplicated().sum()),
    }

df = pd.DataFrame({"a": [1, 2, 2, None], "b": ["x", "y", "y", "z"]})
print(resumo(df))
''', ["<code>df.shape</code> dá linhas e colunas.", "<code>df.isna().sum().sum()</code> e <code>df.duplicated().sum()</code>."]),
        cod("O alvo por grupo", "Calcule a <b>taxa de cancelamento</b> (média da coluna <code>cancelou</code>) por plano, ordenada da maior para a menor. Essa tabela é uma das descobertas mais valiosas de uma EDA.",
            '''
import pandas as pd

clientes = pd.DataFrame({
    "plano": ["básico", "premium", "básico", "básico", "premium", "família"],
    "cancelou": [1, 0, 1, 0, 0, 0],
})

taxa = None
print(taxa)
''',
            [("Taxas corretas e ordenadas", "assert [round(v, 2) for v in taxa.tolist()] == [0.67, 0.0, 0.0] and taxa.index[0] == 'básico', f'taxa = {taxa.to_dict()}'")],
            '''
import pandas as pd

clientes = pd.DataFrame({
    "plano": ["básico", "premium", "básico", "básico", "premium", "família"],
    "cancelou": [1, 0, 1, 0, 0, 0],
})

taxa = clientes.groupby("plano")["cancelou"].mean().sort_values(ascending=False)
print(taxa)
''', ["A média de uma coluna 0/1 é a proporção de 1.", "<code>.sort_values(ascending=False)</code>"], rot="Mão no código · nível 2"),
        erros([
            ("Pular a EDA e ir direto para o modelo.", "Você descobre os problemas depois de treinar, quando eles custam mais caro."),
            ("Olhar o conjunto de teste durante a EDA.", "Decisões tomadas olhando o teste contaminam a avaliação. Explore só o treino."),
            ("Gráficos bonitos sem conclusão.", "Cada gráfico deve responder a uma pergunta e gerar uma anotação."),
        ]),
        ponte("EDA para dados de texto e LLMs",
              "<p>Com texto, a EDA vira: quantos tokens tem cada documento? Há duplicados? Em que idiomas? Quais as perguntas mais comuns dos usuários? Esse olhar decide o tamanho dos trechos de um RAG e o que entra num conjunto de avaliação.</p>"),
        quiz([
            ("Qual é o primeiro passo de uma EDA?", ["Treinar um modelo simples.", "Entender o contexto: o que é cada linha e qual é o alvo.", "Remover os outliers."], 1, "Contexto primeiro."),
            ("Por que não explorar o conjunto de teste?", ["Porque é pequeno.", "Para não contaminar a avaliação final.", "Porque não tem alvo."], 1, "O teste deve simular dados nunca vistos."),
            ("Como ver se uma categoria ajuda a prever o alvo?", ["Contar as linhas.", "Comparar a média do alvo entre as categorias.", "Ordenar a coluna."], 1, "Um groupby com o alvo."),
        ]),
    ],
    ["EDA: contexto, estrutura, uma variável por vez, relação com o alvo e anotações.", "Desequilíbrio de classes muda a métrica.", "Explore só o treino."],
    "Jupyter e Colab: o laboratório do cientista de dados.",
    livro=("PDSH:03.00-introduction-to-pandas", "Capítulo 3, seções sobre agregação e agrupamento", "Que exemplo de análise exploratória o livro faz com dados de planetas?"))

AULAS["Jupyter Notebook e Google Colab"] = aula(
    25,
    "Escrever um pouco, rodar, ver o resultado, ajustar. O notebook é o caderno de laboratório da ciência de dados: código, gráficos e explicações no mesmo documento. E o Colab ainda empresta uma GPU de graça.",
    ["usar células de código e de texto;", "entender a ordem de execução e o estado do kernel;", "ativar a GPU no Colab."],
    ["Python básico."],
    [
        chute("Você rodou a célula 5 (que define <code>x = 10</code>), depois apagou essa célula. A célula 6 usa <code>x</code>. O que acontece ao rodá-la?", ["Dá erro: x não existe.", "Funciona: x ainda vale 10 na memória.", "x vale 0."], 1,
              ["O código sumiu da tela, mas a variável ainda vive no kernel.", "Isso! O kernel guarda o estado das células já executadas, mesmo apagadas. Por isso notebooks enganam.", "Variáveis não têm valor padrão."],
              "O teste de fogo: <b>Reiniciar e executar tudo</b>. Se quebrar, o notebook dependia de algo invisível."),
        concreto("O caderno de laboratório", "<p>Um cientista anota o procedimento, o resultado e a interpretação, na ordem em que fez. O notebook faz o mesmo: célula de texto explicando, célula de código executando, saída logo abaixo.</p>"),
        nota("O que saber", [
            ("Célula de código / de texto (Markdown)", "tipos de célula", "Texto explica; código roda. Use as duas."),
            ("<code>Shift + Enter</code>", "executar", "Roda a célula e passa para a próxima."),
            ("Kernel", "o motor", "O processo Python que guarda as variáveis. Reiniciar apaga tudo da memória."),
            ("<code>!pip install pacote</code>", "comando de terminal", "O <code>!</code> roda comandos do sistema dentro da célula."),
            ("Ambiente de execução → Alterar tipo → GPU", "GPU no Colab", "Grátis, com limite de tempo de uso."),
        ], rot="Agora sim, os conceitos"),
        passos("Um notebook que outra pessoa consegue rodar", [
            ("Primeira célula: todos os imports e instalações.", "Quem abre sabe o que precisa."),
            ("Células curtas, em ordem, com títulos em Markdown.", "Conta uma história."),
            ("Nada de caminhos do seu computador.", "Baixe os dados por URL ou do Drive."),
            ("Antes de compartilhar: <b>Reiniciar e executar tudo</b>.", "Se roda de cima a baixo, está pronto."),
        ]),
        cod("Simulando o estado do kernel", "Para fixar a ideia de estado: as “células” abaixo rodaram nesta ordem: 1, 3, 2. Qual o valor final de <code>total</code>? Escreva o código na ordem em que de fato rodou e imprima o resultado.",
            '''
# célula 1: total = 10
# célula 2: total = total * 2
# célula 3: total = total + 5

# reescreva as linhas na ordem 1, 3, 2 e imprima total
''',
            [("Resultado 30", "assert saida.strip() == '30', f'saiu {saida.strip()!r}'")],
            '''
total = 10
total = total + 5
total = total * 2
print(total)
''', ["Ordem de execução: 10, depois +5, depois ×2."], exp="<p>Na ordem da tela (1, 2, 3) o resultado seria 25. Notebooks executados fora de ordem produzem resultados que ninguém consegue reproduzir.</p>"),
        erros([
            ("Executar células fora de ordem e confiar no resultado.", "Reinicie e execute tudo antes de tirar conclusões."),
            ("Notebook gigante com tudo misturado.", "Quando o código se estabiliza, mova funções para arquivos <code>.py</code> e importe."),
            ("Deixar chaves de API escritas no notebook compartilhado.", "Use os “Secrets” do Colab ou variáveis de ambiente."),
        ]),
        ponte("Onde a IA é prototipada",
              "<p>Quase todo experimento de ML começa num notebook: explorar dados, testar um modelo, ajustar um prompt. Tutoriais do Hugging Face e do PyTorch vêm com botão “Abrir no Colab”. Na Fase 4, a GPU gratuita do Colab é onde você vai treinar suas primeiras redes.</p>"),
        quiz([
            ("O que o kernel guarda?", ["O texto das células.", "As variáveis e o estado da execução.", "Os gráficos salvos."], 1, "É o processo Python em execução."),
            ("Como garantir que o notebook é reproduzível?", ["Salvar várias vezes.", "Reiniciar o kernel e executar tudo do início.", "Usar só células de texto."], 1, "Sem estados escondidos."),
            ("Para que serve o <code>!</code> numa célula?", ["Comentar a linha.", "Rodar um comando do terminal.", "Destacar um erro."], 1, "Ex.: <code>!pip install</code>."),
        ]),
    ],
    ["Notebooks misturam código, saída e explicação.", "O kernel guarda estado: execute em ordem e teste com “reiniciar e executar tudo”.", "O Colab oferece GPU gratuita."],
    "SQL: perguntar coisas a um banco de dados.",
    livro=("PDSH:01.00-ipython-beyond-normal-python", "Capítulo 1, “IPython: Beyond Normal Python”", "Quais comandos mágicos (%timeit e outros) o livro apresenta?"))
