# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 3 (parte A): conceitos e algoritmos centrais de ML clássico."""
from lesson_factory import *

AULAS = {}

AULAS["Aprendizado supervisionado vs. não supervisionado"] = aula(
    30,
    "Na programação tradicional, você escreve as regras. Em machine learning, você mostra <b>exemplos</b> e o computador descobre as regras sozinho. A primeira pergunta de qualquer projeto é: os exemplos vêm com a resposta certa ou não?",
    ["diferenciar aprendizado supervisionado e não supervisionado;", "separar classificação de regressão;", "reconhecer o tipo de problema a partir da pergunta de negócio."],
    ["Fase 2 (Python para dados)."],
    [
        chute("Um banco tem milhares de transações marcadas como “fraude” ou “legítima” e quer marcar as novas automaticamente. Que tipo de problema é?", ["Não supervisionado (agrupamento).", "Supervisionado (classificação).", "Supervisionado (regressão)."], 1,
              ["Agrupamento é quando não há rótulo nenhum.", "Isso! Há exemplos com a resposta (o rótulo) e a resposta é uma categoria: classificação.", "Regressão prevê um número contínuo, como um valor em reais."],
              "Tem rótulo? Supervisionado. O rótulo é categoria? Classificação. É número? Regressão."),
        concreto("Professor com gabarito e explorador sem mapa", "<p>No <b>supervisionado</b>, o modelo estuda com um gabarito: vê mil fotos com a legenda “gato” ou “cachorro” e aprende a acertar. No <b>não supervisionado</b>, não há gabarito: o modelo recebe mil fotos e descobre sozinho que elas formam grupos parecidos.</p>"),
        crianca("<p>Supervisionado é aprender a separar frutas com a mãe dizendo “isso é maçã, isso é banana”. Não supervisionado é receber uma cesta e separar as frutas por cor e tamanho, sem ninguém dizer os nomes.</p>"),
        ver("os exemplos de cada tipo de aprendizado que aparecem no vídeo"),
        tabela("Os tipos de problema", ["Tipo", "Tem rótulo?", "Saída", "Exemplo"], [
            ["Classificação", "sim", "uma categoria", "spam ou não; qual doença"],
            ["Regressão", "sim", "um número", "preço de um imóvel; demanda de amanhã"],
            ["Agrupamento (clustering)", "não", "grupos", "segmentos de clientes"],
            ["Redução de dimensão", "não", "menos colunas", "visualizar dados de 100 colunas em 2D"],
            ["Detecção de anomalias", "geralmente não", "o que destoa", "transações estranhas"],
        ]),
        nota("O vocabulário", [
            ("<code>X</code>", "atributos (features)", "As colunas que o modelo usa para decidir. Uma linha por exemplo."),
            ("<code>y</code>", "rótulo (target)", "A resposta certa, só no supervisionado."),
            ("<code>modelo.fit(X, y)</code>", "treinar", "O modelo ajusta seus parâmetros aos exemplos."),
            ("<code>modelo.predict(X_novo)</code>", "prever", "Aplica o que aprendeu a exemplos novos."),
        ], rot="Agora sim, o vocabulário"),
        cod("Classifique os problemas", "Complete o dicionário com <b>\"classificacao\"</b>, <b>\"regressao\"</b> ou <b>\"agrupamento\"</b> para cada problema.",
            '''
problemas = {
    "prever o preço de um carro usado": "",
    "dizer se um e-mail é spam": "",
    "dividir clientes em grupos parecidos, sem rótulo": "",
    "prever quantos minutos uma entrega vai levar": "",
    "identificar o dígito escrito numa imagem": "",
}
print(problemas)
''',
            [("Todas corretas", "certo = ['regressao', 'classificacao', 'agrupamento', 'regressao', 'classificacao']\nerrados = [k for k, c in zip(problemas, certo) if problemas[k] != c]\nassert not errados, f'reveja: {errados}'")],
            '''
problemas = {
    "prever o preço de um carro usado": "regressao",
    "dizer se um e-mail é spam": "classificacao",
    "dividir clientes em grupos parecidos, sem rótulo": "agrupamento",
    "prever quantos minutos uma entrega vai levar": "regressao",
    "identificar o dígito escrito numa imagem": "classificacao",
}
print(problemas)
''', ["Pergunte: a resposta é um número ou uma categoria? Há gabarito?"]),
        erros([
            ("“Prever 0 ou 1 é regressão porque são números.”", "São rótulos de categorias. É classificação."),
            ("Achar que não supervisionado é “mais avançado”.", "É outro tipo de pergunta. Na prática, a maior parte dos projetos é supervisionada."),
            ("Começar pelo algoritmo.", "Comece pela pergunta e pelos dados: eles definem o tipo de problema."),
        ]),
        ponte("Onde os LLMs se encaixam",
              "<p>Um LLM é pré-treinado de forma <b>auto-supervisionada</b>: o rótulo é a própria próxima palavra do texto, então não é preciso ninguém anotar. Depois, ajustes finos usam exemplos rotulados (supervisionado) e preferências humanas (RLHF). As categorias desta aula continuam valendo, só que em escala gigante.</p>"),
        quiz([
            ("Prever a nota (0 a 10) que um cliente dará é:", ["Classificação.", "Regressão.", "Agrupamento."], 1, "Saída numérica."),
            ("O que diferencia o supervisionado?", ["Usar GPU.", "Ter exemplos com a resposta certa (rótulo).", "Ter muitos dados."], 1, "O gabarito."),
            ("Agrupar notícias por assunto sem categorias prévias é:", ["Supervisionado.", "Não supervisionado.", "Regressão."], 1, "Não há rótulos."),
        ]),
    ],
    ["Supervisionado aprende com exemplos rotulados; não supervisionado acha estrutura sem rótulos.", "Classificação prevê categorias; regressão prevê números.", "<code>fit</code> treina; <code>predict</code> aplica."],
    "Treino, validação e teste: medir sem se enganar.",
    livro=("MLCC:", "Google Machine Learning Crash Course, “Introduction to Machine Learning”", "Que exemplos de problemas supervisionados o curso apresenta?"))

AULAS["Treino, validação e teste"] = aula(
    30,
    "Um aluno que decorou as respostas da lista de exercícios tira 10 na lista e 3 na prova. Modelos fazem a mesma coisa. Por isso, todo projeto de ML guarda dados que o modelo <b>nunca viu</b> para descobrir o quanto ele realmente aprendeu.",
    ["separar dados em treino, validação e teste;", "entender o papel de cada parte;", "evitar usar o teste para tomar decisões."],
    ["Aprendizado supervisionado."],
    [
        chute("Você testou 50 configurações e escolheu a melhor pelo resultado no conjunto de <b>teste</b>. O desempenho no teste é uma boa estimativa para o mundo real?", ["Sim, é para isso que serve o teste.", "Não: o teste virou parte da escolha e ficou otimista.", "Sim, se o teste for grande."], 1,
              ["O teste só vale se for usado <b>uma vez</b>, no fim.", "Isso! Ao escolher pelo teste, você ajustou o modelo a ele. Para escolher, use a validação.", "Tamanho não resolve o vício da escolha."],
              "Treino ensina; validação escolhe; teste avalia uma vez só."),
        concreto("Lista, simulado e vestibular", "<p>O estudante resolve a <b>lista de exercícios</b> (treino), faz <b>simulados</b> para decidir o que revisar (validação) e, no fim, faz o <b>vestibular</b> (teste), uma única vez. Se ele visse a prova antes, a nota não diria nada.</p>"),
        nota("As três partes", [
            ("Treino (~70%)", "aprender", "O modelo ajusta os parâmetros aqui."),
            ("Validação (~15%)", "escolher", "Compara modelos e hiperparâmetros."),
            ("Teste (~15%)", "avaliar", "Usado uma vez, no fim, para a estimativa final."),
            ("<code>train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)</code>", "no scikit-learn", "<code>stratify</code> mantém a proporção das classes em cada parte."),
        ], rot="Os conceitos"),
        cod("Separando na mão", "Embaralhe os índices com a semente dada e separe 60% treino, 20% validação e 20% teste, <b>sem sobreposição</b>.",
            '''
import numpy as np

def separar(n, semente=42):
    rng = np.random.default_rng(semente)
    idx = np.arange(n)
    # embaralhe idx e fatie
    return idx, idx, idx

tr, va, te = separar(100)
print(len(tr), len(va), len(te))
''',
            [("Tamanhos 60/20/20", "tr, va, te = separar(100)\nassert (len(tr), len(va), len(te)) == (60, 20, 20), f'{len(tr)}, {len(va)}, {len(te)}'"),
             ("Sem sobreposição e cobrindo tudo", "tr, va, te = separar(100)\nassert len(set(tr) | set(va) | set(te)) == 100"),
             ("Embaralhado", "tr, va, te = separar(100)\nassert list(tr[:5]) != [0, 1, 2, 3, 4]"),
             ("Reproduzível", "assert list(separar(50)[0]) == list(separar(50)[0])")],
            '''
import numpy as np

def separar(n, semente=42):
    rng = np.random.default_rng(semente)
    idx = rng.permutation(n)
    a, b = int(n * 0.6), int(n * 0.8)
    return idx[:a], idx[a:b], idx[b:]

tr, va, te = separar(100)
print(len(tr), len(va), len(te))
''', ["<code>rng.permutation(n)</code> embaralha os índices.", "Fatie em 60% e 80% do tamanho."]),
        erros([
            ("Separar sem embaralhar dados ordenados.", "Se o arquivo está ordenado por data ou classe, o teste fica com um tipo só."),
            ("Embaralhar séries temporais.", "Aí o certo é o contrário: separe pelo tempo."),
            ("O mesmo cliente no treino e no teste.", "Separe por cliente (agrupado), senão o modelo reconhece a pessoa em vez de aprender o padrão."),
        ]),
        ponte("Avaliar LLMs também é assim",
              "<p>Benchmarks de LLMs sofrem do mesmo problema: se as questões vazaram para os dados de treino, o modelo “decorou a prova”. Por isso equipes sérias mantêm conjuntos de avaliação privados, que nunca foram publicados.</p>"),
        quiz([
            ("Para que serve o conjunto de validação?", ["Treinar o modelo.", "Escolher entre modelos e configurações.", "Dar a nota final."], 1, "O teste fica guardado."),
            ("Por que usar <code>stratify=y</code>?", ["Deixar mais rápido.", "Manter a proporção das classes em cada parte.", "Remover duplicados."], 1, "Importante com classes desbalanceadas."),
            ("Quantas vezes usar o conjunto de teste?", ["A cada experimento.", "Uma vez, no fim.", "Nunca."], 1, "Senão ele vira validação."),
        ]),
    ],
    ["Treino ensina, validação escolhe, teste avalia uma única vez.", "Embaralhe (exceto séries temporais) e estratifique.", "Separe por grupo quando houver registros da mesma entidade."],
    "Overfitting e underfitting: decorar ou não aprender.",
    livro=("MLCC:", "Google Machine Learning Crash Course, “Datasets, generalization, and overfitting”", "Como o curso define generalização?"))

AULAS["Overfitting e underfitting"] = aula(
    35,
    "Um modelo simples demais não aprende nem os exemplos de treino. Um complexo demais decora até o ruído e falha com dados novos. Todo o ofício do machine learning é achar o meio-termo, e saber diagnosticar de que lado você está.",
    ["reconhecer underfitting e overfitting pelas métricas;", "entender viés e variância;", "conhecer os remédios para cada caso."],
    ["Treino, validação e teste."],
    [
        chute("Acurácia no treino: 99%. Na validação: 71%. Qual o diagnóstico?", ["Underfitting.", "Overfitting.", "Modelo perfeito."], 1,
              ["Underfitting teria resultado ruim também no treino.", "Isso! A distância grande entre treino e validação mostra que o modelo decorou em vez de generalizar.", "71% na validação, longe do treino, não é perfeito."],
              "Treino ruim → underfitting. Treino ótimo e validação ruim → overfitting."),
        concreto("Três alunos", "<p>O primeiro não estudou: erra a lista e a prova (<b>underfitting</b>). O segundo <b>decorou</b> as respostas da lista: 10 na lista, 4 na prova (<b>overfitting</b>). O terceiro entendeu a matéria: vai bem nas duas (<b>generalização</b>).</p>"),
        crianca("<p>Desenhe uma linha passando pelos pontos. Uma reta reta demais nem chega perto deles. Um rabisco que passa exatamente por cada ponto fica maluco entre eles. A boa curva passa <b>perto</b> de todos, sem zigue-zague.</p>"),
        ver("o que o vídeo chama de viés (bias) e de variância"),
        tabela("Diagnóstico e remédio", ["Sintoma", "Diagnóstico", "Remédios"], [
            ["Erro alto no treino e na validação", "underfitting (viés alto)", "modelo mais complexo, mais atributos, treinar mais"],
            ["Erro baixo no treino, alto na validação", "overfitting (variância alta)", "mais dados, regularização, modelo mais simples, early stopping"],
            ["Erro baixo nos dois", "bom ajuste", "confirme no teste e pare"],
        ]),
        cod("Diagnóstico automático", "Complete a função: devolva <b>\"underfitting\"</b> se o erro de treino for maior que 0.2, <b>\"overfitting\"</b> se a validação for mais de 0.1 pior que o treino, e <b>\"ok\"</b> no resto.",
            '''
def diagnostico(erro_treino, erro_valid):
    return "ok"

print(diagnostico(0.02, 0.30), diagnostico(0.35, 0.38), diagnostico(0.08, 0.11))
''',
            [("Overfitting", "assert diagnostico(0.02, 0.30) == 'overfitting'"), ("Underfitting", "assert diagnostico(0.35, 0.38) == 'underfitting'"), ("Ok", "assert diagnostico(0.08, 0.11) == 'ok'")],
            '''
def diagnostico(erro_treino, erro_valid):
    if erro_treino > 0.2:
        return "underfitting"
    if erro_valid - erro_treino > 0.1:
        return "overfitting"
    return "ok"

print(diagnostico(0.02, 0.30), diagnostico(0.35, 0.38), diagnostico(0.08, 0.11))
''', ["Teste primeiro o underfitting (treino ruim)."]),
        cod("Complexidade na prática", "Ajuste polinômios de grau 1, 3 e 9 aos dados de treino (use <code>np.polyfit</code>) e guarde em <code>erros_valid</code> o erro quadrático médio de cada um na validação. Depois descubra qual grau generaliza melhor.",
            '''
import numpy as np

rng = np.random.default_rng(0)
x = np.linspace(0, 1, 30)
y = np.sin(2 * np.pi * x) + rng.normal(0, 0.15, 30)
xt, yt = x[::2], y[::2]      # treino
xv, yv = x[1::2], y[1::2]    # validação

erros_valid = {}
for grau in [1, 3, 9]:
    pass

melhor = None
print(erros_valid, melhor)
''',
            [("Calcula os três erros", "assert set(erros_valid) == {1, 3, 9}"), ("Grau 3 generaliza melhor", "assert melhor == 3, f'melhor = {melhor}, erros = {erros_valid}'"),
             ("Grau 1 sofre underfitting", "assert erros_valid[1] > erros_valid[3] * 3")],
            '''
import numpy as np

rng = np.random.default_rng(0)
x = np.linspace(0, 1, 30)
y = np.sin(2 * np.pi * x) + rng.normal(0, 0.15, 30)
xt, yt = x[::2], y[::2]
xv, yv = x[1::2], y[1::2]

erros_valid = {}
for grau in [1, 3, 9]:
    coef = np.polyfit(xt, yt, grau)
    erros_valid[grau] = float(np.mean((np.polyval(coef, xv) - yv) ** 2))

melhor = min(erros_valid, key=erros_valid.get)
print(erros_valid, melhor)
''', ["<code>coef = np.polyfit(xt, yt, grau)</code> e <code>np.polyval(coef, xv)</code> prevê.", "<code>min(erros_valid, key=erros_valid.get)</code> acha o grau de menor erro."], rot="Mão no código · nível 2"),
        erros([
            ("Olhar só a métrica de treino.", "Ela sempre melhora com mais complexidade. A validação é que conta."),
            ("Tentar resolver overfitting com um modelo maior.", "Piora. Mais dados ou regularização."),
            ("Achar que mais épocas é sempre melhor.", "A partir de certo ponto a validação piora: é o overfitting chegando."),
        ]),
        ponte("Overfitting em deep learning e LLMs",
              "<p>Redes enormes conseguem decorar datasets inteiros. As defesas são as mesmas desta aula, com outros nomes: dropout, weight decay, data augmentation, early stopping (Fase 4). Em ajuste fino de LLMs, treinar épocas demais num dataset pequeno faz o modelo repetir frases do treino.</p>"),
        quiz([
            ("Erro alto no treino e na validação indica:", ["Overfitting.", "Underfitting.", "Vazamento de dados."], 1, "O modelo não aprendeu nem o treino."),
            ("Qual remédio combate overfitting?", ["Modelo mais complexo.", "Mais dados ou regularização.", "Remover o conjunto de validação."], 1, "Reduz a variância."),
            ("Overfitting está ligado a:", ["Viés alto.", "Variância alta.", "Poucos atributos."], 1, "O modelo muda muito com os dados de treino."),
        ]),
    ],
    ["Underfitting: ruim no treino. Overfitting: ótimo no treino e ruim na validação.", "Complexidade demais decora o ruído.", "Remédios: mais dados, regularização, modelos mais simples, early stopping."],
    "Validação cruzada: uma estimativa mais estável.",
    livro=("ISLP", "Capítulo 2, seção 2.2, “Assessing Model Accuracy” (trade-off viés-variância)", "Como o livro ilustra o trade-off com curvas de erro?"))

AULAS["Validação cruzada"] = aula(
    30,
    "Com poucos dados, a nota de um único conjunto de validação depende muito da sorte de quais exemplos caíram lá. A validação cruzada faz várias provas diferentes e tira a média: uma medida mais justa do modelo.",
    ["entender o k-fold;", "usar a média e o desvio das notas;", "escolher a variante certa (estratificada, agrupada, temporal)."],
    ["Treino, validação e teste; overfitting."],
    [
        chute("No 5-fold, quantas vezes o modelo é treinado?", ["1", "5", "25"], 1,
              ["Uma vez seria uma separação simples.", "Isso! Cada uma das 5 partes serve de validação uma vez, enquanto as outras 4 treinam.", "Seriam 25 com 5 repetições de 5-fold."],
              "Cada exemplo é usado para validar exatamente uma vez."),
        concreto("O rodízio de juízes", "<p>Para julgar um campeonato com justiça, cada jurado avalia uma rodada e nenhum avalia sempre o mesmo competidor. No k-fold, cada parte dos dados é “jurada” uma vez, e a nota final é a média de todas.</p>"),
        passos("Como funciona o 5-fold", [
            ("Divida os dados em 5 partes iguais.", "Depois de embaralhar."),
            ("Rodada 1: treine nas partes 2 a 5 e valide na parte 1.", "Guarde a nota."),
            ("Repita trocando a parte de validação.", "5 rodadas, 5 notas."),
            ("Reporte média e desvio padrão.", "“0,84 ± 0,02” diz mais que “0,85”."),
        ]),
        nota("No scikit-learn", [
            ("<code>cross_val_score(modelo, X, y, cv=5)</code>", "k-fold pronto", "Devolve as 5 notas."),
            ("<code>StratifiedKFold</code>", "estratificado", "Mantém a proporção de classes em cada parte (padrão para classificação)."),
            ("<code>GroupKFold</code>", "por grupo", "O mesmo paciente/cliente nunca fica dos dois lados."),
            ("<code>TimeSeriesSplit</code>", "temporal", "Treina no passado, valida no futuro, sempre avançando."),
        ]),
        cod("Gerando as dobras", "Complete a função que devolve uma lista de pares <code>(treino, validacao)</code> com os índices do k-fold (sem embaralhar, para simplificar).",
            '''
import numpy as np

def kfold(n, k):
    partes = np.array_split(np.arange(n), k)
    dobras = []
    # para cada i, validação = partes[i]; treino = as outras juntas
    return dobras

for tr, va in kfold(10, 5):
    print(tr, va)
''',
            [("5 dobras", "assert len(kfold(10, 5)) == 5"),
             ("Cada índice valida uma vez", "import numpy as np\nv = np.concatenate([va for _, va in kfold(10, 5)])\nassert sorted(v.tolist()) == list(range(10))"),
             ("Treino e validação sem sobreposição", "assert all(set(tr.tolist()).isdisjoint(va.tolist()) and len(tr) + len(va) == 12 for tr, va in kfold(12, 3))")],
            '''
import numpy as np

def kfold(n, k):
    partes = np.array_split(np.arange(n), k)
    dobras = []
    for i in range(k):
        va = partes[i]
        tr = np.concatenate([p for j, p in enumerate(partes) if j != i])
        dobras.append((tr, va))
    return dobras

for tr, va in kfold(10, 5):
    print(tr, va)
''', ["Treino: <code>np.concatenate([p for j, p in enumerate(partes) if j != i])</code>."]),
        lab("Validação cruzada com scikit-learn", '''
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
modelo = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
notas = cross_val_score(modelo, X, y, cv=5)
print(notas.round(3), "média:", notas.mean().round(3), "±", notas.std().round(3))
''', corpo="<p>Rode no Colab:</p>", exps=["Troque <code>cv=5</code> por <code>cv=10</code>. A média muda muito? E o desvio?"]),
        erros([
            ("Normalizar os dados antes da validação cruzada.", "A média de todos os dados vaza para as dobras. Ponha o pré-processamento num pipeline."),
            ("Usar k-fold comum em séries temporais.", "O modelo treina com o futuro. Use <code>TimeSeriesSplit</code>."),
            ("Usar a validação cruzada e esquecer o teste final.", "A validação cruzada escolhe; o teste guardado confirma."),
        ]),
        ponte("Quando não dá para fazer k-fold",
              "<p>Em deep learning e LLMs, treinar 5 vezes um modelo grande custa caro demais; por isso se usa uma única divisão treino/validação com bastante dado. A validação cruzada brilha onde o ML clássico vive: datasets pequenos e médios, modelos rápidos.</p>"),
        quiz([
            ("O que a validação cruzada estima melhor que uma única divisão?", ["O tempo de treino.", "O desempenho esperado, com menos dependência da sorte da divisão.", "O número de atributos."], 1, "Média de várias provas."),
            ("Para classificação com classes desbalanceadas, use:", ["KFold comum.", "StratifiedKFold.", "TimeSeriesSplit."], 1, "Mantém as proporções."),
            ("Por que o pré-processamento deve ficar dentro do pipeline?", ["Por estética.", "Para não vazar informação das dobras de validação.", "Para treinar mais rápido."], 1, "Cada dobra calcula seus próprios parâmetros."),
        ]),
    ],
    ["k-fold: cada parte valida uma vez; reporte média e desvio.", "Estratificado para classes, agrupado para entidades, temporal para séries.", "Pré-processamento dentro do pipeline."],
    "Engenharia de atributos: dar ao modelo as pistas certas.",
    livro=("ISLP", "Capítulo 5, seção 5.1, “Cross-Validation”", "Que vantagem o livro aponta do k-fold sobre o leave-one-out?"))

AULAS["Engenharia de atributos (feature engineering)"] = aula(
    35,
    "Um modelo só enxerga as colunas que você entrega. “Data da compra” sozinha diz pouco; “dias desde a última compra” e “é fim de semana?” dizem muito. Criar boas colunas costuma render mais do que trocar de algoritmo.",
    ["criar atributos a partir de datas, textos e combinações;", "usar conhecimento do problema para ter ideias;", "evitar atributos que vazam a resposta."],
    ["Pandas, encoding e séries temporais."],
    [
        chute("Para prever o preço de um imóvel, qual atributo novo provavelmente ajuda mais?", ["O número da linha na planilha.", "Preço por metro quadrado do bairro.", "A cor da fachada."], 1,
              ["O número da linha não tem relação com o preço.", "Isso! Ele resume a informação de localização, a mais importante em imóveis.", "Pode até influenciar, mas muito menos."],
              "Bons atributos vêm de entender o problema, não de testar aleatoriamente."),
        concreto("O médico e o exame", "<p>O peso e a altura sozinhos dizem algo. Mas o médico calcula o <b>IMC</b>: uma combinação dos dois que separa muito melhor quem tem risco. Feature engineering é criar os “IMCs” do seu problema.</p>"),
        nota("Receitas que funcionam", [
            ("Datas → dia da semana, mês, feriado, “dias desde”", "tempo", "Ciclos e recência."),
            ("Razões e diferenças", "combinações", "Preço/m², gasto/renda, idade − idade média do grupo."),
            ("Agregações por grupo", "contexto", "Média de compras do cliente, nº de pedidos nos últimos 30 dias."),
            ("Texto → tamanho, contagem de palavras, presença de termos", "texto", "Simples e muitas vezes forte."),
            ("Faixas (<code>pd.cut</code>) e logaritmo (<code>np.log1p</code>)", "transformações", "Para valores muito assimétricos, como renda."),
        ], rot="As receitas"),
        cod("Atributos de comportamento", "Para cada cliente, crie <code>n_compras</code>, <code>ticket_medio</code> e <code>dias_desde_ultima</code> (em relação a 2025-03-31), a partir da tabela de compras.",
            '''
import pandas as pd

compras = pd.DataFrame({
    "cliente": ["a", "a", "b", "a", "b"],
    "data": pd.to_datetime(["2025-01-10", "2025-03-01", "2025-02-15", "2025-03-21", "2025-03-30"]),
    "valor": [100, 50, 80, 150, 40],
})
hoje = pd.Timestamp("2025-03-31")

atributos = None
print(atributos)
''',
            [("Uma linha por cliente", "assert sorted(atributos.index.tolist()) == ['a', 'b']"),
             ("Valores corretos", "a = atributos.loc['a']; b = atributos.loc['b']\nassert (a['n_compras'], a['ticket_medio'], a['dias_desde_ultima']) == (3, 100.0, 10) and (b['n_compras'], b['ticket_medio'], b['dias_desde_ultima']) == (2, 60.0, 1), f'\\n{atributos}'")],
            '''
import pandas as pd

compras = pd.DataFrame({
    "cliente": ["a", "a", "b", "a", "b"],
    "data": pd.to_datetime(["2025-01-10", "2025-03-01", "2025-02-15", "2025-03-21", "2025-03-30"]),
    "valor": [100, 50, 80, 150, 40],
})
hoje = pd.Timestamp("2025-03-31")

g = compras.groupby("cliente")
atributos = pd.DataFrame({
    "n_compras": g["valor"].count(),
    "ticket_medio": g["valor"].mean(),
    "dias_desde_ultima": (hoje - g["data"].max()).dt.days,
})
print(atributos)
''', ["Agrupe por cliente: <code>g = compras.groupby(\"cliente\")</code>.", "<code>(hoje - g[\"data\"].max()).dt.days</code> dá a recência."]),
        erros([
            ("Atributos que só existem depois do fato (“foi reembolsado” para prever fraude).", "É vazamento: no momento da previsão, essa informação não existe."),
            ("Criar centenas de colunas sem critério.", "Aumenta o overfitting e o custo. Comece pelas que fazem sentido no problema."),
            ("Calcular agregados usando o conjunto inteiro.", "Médias por grupo devem ser calculadas só com o treino."),
        ]),
        ponte("E no deep learning?",
              "<p>Redes neurais aprendem atributos sozinhas a partir de dados brutos (pixels, texto): essa é a grande virada da Fase 4. Mas com dados tabulares, que dominam as empresas, a engenharia de atributos com árvores de decisão continua vencendo na maioria dos casos.</p>"),
        quiz([
            ("De onde vêm as melhores ideias de atributos?", ["De testar combinações ao acaso.", "Do conhecimento sobre o problema.", "Do algoritmo escolhido."], 1, "Entender o negócio rende mais."),
            ("“Dias desde a última compra” é um atributo de:", ["Recência.", "Encoding.", "Normalização."], 0, "Mede quanto tempo passou."),
            ("Qual atributo vaza a resposta ao prever cancelamento?", ["Tempo de contrato.", "Data em que o cancelamento foi processado.", "Plano contratado."], 1, "Só existe depois do evento."),
        ]),
    ],
    ["Atributos bons traduzem o conhecimento do problema em colunas.", "Datas, razões, agregações e transformações são as receitas clássicas.", "Nunca use informação que não existiria no momento da previsão."],
    "Regressão linear: o primeiro modelo.",
    livro=("PDSH:05.04-feature-engineering", "Seção 5.4, “Feature Engineering”", "Que técnicas o livro mostra para texto e imagens?"))

AULAS["Regressão linear"] = aula(
    40,
    "Traçar a melhor reta por uma nuvem de pontos parece simples, mas é o algoritmo mais usado da estatística, a base da regressão logística e, multiplicado milhões de vezes, de uma rede neural. Tudo começa aqui.",
    ["entender a reta y = w·x + b e o que significam w e b;", "medir o erro com o MSE;", "treinar com a fórmula fechada e com gradiente descendente."],
    ["Overfitting; gradiente descendente (Matemática)."],
    [
        chute("Um modelo de preços diz: preço = 3.000 × área + 50.000. O que significa o 3.000?", ["O preço mínimo de um imóvel.", "Cada metro quadrado a mais aumenta o preço em 3.000.", "O número de imóveis analisados."], 1,
              ["O preço “de partida” é o 50.000 (o intercepto).", "Isso! O coeficiente diz quanto a saída muda quando o atributo aumenta uma unidade.", "Não tem relação com a quantidade de dados."],
              "O coeficiente é interpretável: essa é uma das grandes forças da regressão linear."),
        concreto("O taxista", "<p>A corrida custa uma bandeirada fixa mais um valor por quilômetro. Preço = 4,50 × km + 6. Isso é uma regressão linear: <b>b</b> é a bandeirada, <b>w</b> é o preço por km. Com os recibos de várias corridas, dá para descobrir os dois números.</p>"),
        crianca("<p>Estique um elástico por cima de pontos num papel, tentando passar perto de todos. A posição em que o elástico “descansa”, puxado igualmente por todos os pontos, é a melhor reta.</p>"),
        ver("como o vídeo mede a distância entre os pontos e a reta (os resíduos)"),
        nota("A reta e o erro", [
            (r"$\hat y = w\,x + b$", "y chapéu", "A previsão. Com vários atributos: $\\hat y = w_1x_1 + \\dots + w_nx_n + b$."),
            (r"$y - \hat y$", "resíduo", "O erro de cada exemplo."),
            (r"$\text{MSE} = \frac{1}{n}\sum (y - \hat y)^2$", "erro quadrático médio", "Quadrado: erros grandes pesam muito mais."),
            (r"$R^2$", "R quadrado", "Fração da variação de y explicada pelo modelo (1 é perfeito)."),
        ], rot="Agora sim, a fórmula"),
        passos("Os mínimos quadrados com uma variável", [
            (r"$w = \frac{\sum (x - \bar x)(y - \bar y)}{\sum (x - \bar x)^2}$", "Quanto x e y variam juntos, dividido por quanto x varia."),
            (r"$b = \bar y - w\,\bar x$", "A reta passa pelo ponto médio."),
            ("Com x = [1, 2, 3] e y = [2, 4, 6]: w = 2 e b = 0.", "A reta perfeita y = 2x."),
        ]),
        cod("Mínimos quadrados do zero", "Implemente <code>ajustar(x, y)</code> devolvendo <code>(w, b)</code> pela fórmula dos mínimos quadrados, e <code>mse</code>.",
            '''
import numpy as np

def ajustar(x, y):
    return 0.0, 0.0

def mse(y, y_prev):
    return 0.0

x = np.array([1, 2, 3, 4, 5], dtype=float)
y = np.array([3.1, 4.9, 7.2, 8.8, 11.0])
w, b = ajustar(x, y)
print(round(w, 3), round(b, 3), round(mse(y, w * x + b), 4))
''',
            [("Reta perfeita", "import numpy as np\nw, b = ajustar(np.array([1.0, 2, 3]), np.array([2.0, 4, 6]))\nassert abs(w - 2) < 1e-9 and abs(b) < 1e-9, f'w={w}, b={b}'"),
             ("Igual ao np.polyfit", "import numpy as np\nx = np.array([1, 2, 3, 4, 5.0]); y = np.array([3.1, 4.9, 7.2, 8.8, 11.0])\nw, b = ajustar(x, y)\nassert np.allclose([w, b], np.polyfit(x, y, 1)), f'w={w}, b={b}'"),
             ("MSE correto", "import numpy as np\nassert abs(mse(np.array([1.0, 2]), np.array([1.0, 4])) - 2) < 1e-9")],
            '''
import numpy as np

def ajustar(x, y):
    xm, ym = x.mean(), y.mean()
    w = ((x - xm) * (y - ym)).sum() / ((x - xm) ** 2).sum()
    b = ym - w * xm
    return w, b

def mse(y, y_prev):
    return float(np.mean((y - y_prev) ** 2))

x = np.array([1, 2, 3, 4, 5], dtype=float)
y = np.array([3.1, 4.9, 7.2, 8.8, 11.0])
w, b = ajustar(x, y)
print(round(w, 3), round(b, 3), round(mse(y, w * x + b), 4))
''', ["Calcule as médias, depois a fórmula de w, depois b.", "MSE: <code>np.mean((y - y_prev) ** 2)</code>."]),
        cod("O mesmo resultado com gradiente descendente", "Treine w e b com gradiente descendente (500 passos, taxa 0.02). As derivadas do MSE são: ∂/∂w = −2·média((y − ŷ)·x) e ∂/∂b = −2·média(y − ŷ).",
            '''
import numpy as np

x = np.array([1, 2, 3, 4, 5], dtype=float)
y = np.array([3.1, 4.9, 7.2, 8.8, 11.0])
w, b = 0.0, 0.0

for passo in range(500):
    pass  # calcule a previsão, os gradientes e atualize w e b

print(round(w, 2), round(b, 2))
''',
            [("Chega perto dos mínimos quadrados", "import numpy as np\nwr, br = np.polyfit(x, y, 1)\nassert abs(w - wr) < 0.05 and abs(b - br) < 0.15, f'w={w:.3f}, b={b:.3f}; esperado ≈ {wr:.3f}, {br:.3f}'")],
            '''
import numpy as np

x = np.array([1, 2, 3, 4, 5], dtype=float)
y = np.array([3.1, 4.9, 7.2, 8.8, 11.0])
w, b = 0.0, 0.0

for passo in range(500):
    y_prev = w * x + b
    gw = -2 * np.mean((y - y_prev) * x)
    gb = -2 * np.mean(y - y_prev)
    w -= 0.02 * gw
    b -= 0.02 * gb

print(round(w, 2), round(b, 2))
''', ["A cada passo: previsão, gradientes, e <code>w -= 0.02 * gw</code>."], rot="Mão no código · nível 2 · ponte para IA"),
        erros([
            ("Usar regressão linear para relações curvas sem transformar nada.", "Crie atributos como x² ou log(x), ou use outro modelo."),
            ("Ler o coeficiente como causa.", "Ele mede associação, mantendo os outros atributos fixos. Causa exige outro tipo de estudo."),
            ("Atributos em escalas muito diferentes com gradiente descendente.", "O treino fica lento e instável. Padronize antes."),
        ]),
        ponte("Uma camada linear é isto",
              "<p><code>nn.Linear</code> no PyTorch calcula exatamente $Wx + b$, com muitas entradas e saídas. Uma rede neural é uma pilha dessas camadas com funções não lineares entre elas. Treinar a rede é o mesmo gradiente descendente do exercício, só que com bilhões de pesos.</p>"),
        quiz([
            ("O que o intercepto b representa?", ["A inclinação.", "A previsão quando todos os atributos valem zero.", "O erro médio."], 1, "O ponto onde a reta corta o eixo y."),
            ("Por que o MSE eleva os erros ao quadrado?", ["Para ficarem positivos e erros grandes pesarem mais.", "Para ficar mais rápido.", "Por convenção sem motivo."], 0, "Sem sinal e punindo grandes desvios."),
            ("R² = 0,9 significa:", ["90% de acurácia.", "O modelo explica 90% da variação de y.", "90% dos pontos estão na reta."], 1, "Variação explicada."),
        ]),
    ],
    ["Regressão linear: $\\hat y = wx + b$, ajustada minimizando o MSE.", "Coeficientes são interpretáveis como efeito por unidade.", "Gradiente descendente chega ao mesmo resultado e escala para redes neurais."],
    "Regressão logística: de números para probabilidades (aula-piloto).",
    livro=("ISLP", "Capítulo 3, “Linear Regression”, seções 3.1 e 3.2", "Como o livro interpreta os coeficientes na regressão múltipla?"))

AULAS["Árvores de decisão"] = aula(
    35,
    "“Renda acima de 5 mil? Tem dívidas? Mais de 30 anos?” Uma árvore de decisão aprende sozinha qual pergunta fazer primeiro e onde cortar cada número. É o modelo mais fácil de explicar a um gerente, e o tijolo dos campeões de dados tabulares.",
    ["entender como a árvore escolhe a melhor pergunta;", "calcular a impureza de Gini;", "controlar a profundidade para evitar overfitting."],
    ["Condicionais (Fase 1) e overfitting."],
    [
        chute("Uma árvore sem limite de profundidade, treinada até cada folha ter um exemplo só, tem 100% de acerto no treino. O que esperar na validação?", ["100% também.", "Bem pior: ela decorou o treino.", "Exatamente 50%."], 1,
              ["Seria ótimo, mas quase nunca acontece.", "Isso! Árvores profundas são campeãs de overfitting.", "Não há por que ser exatamente 50%."],
              "Limite a profundidade (<code>max_depth</code>) ou o mínimo de exemplos por folha."),
        concreto("O jogo das 20 perguntas", "<p>“É um animal? Voa? É maior que um gato?” Cada pergunta divide as possibilidades. A árvore de decisão joga esse jogo com os dados, e escolhe a cada passo a pergunta que mais separa as classes.</p>"),
        crianca("<p>Separando brinquedos em caixas: primeiro “é de montar?”, depois “é pequeno?”. Uma boa pergunta deixa cada caixa com brinquedos <b>parecidos</b>. Uma pergunta ruim deixa tudo misturado.</p>"),
        ver("como o vídeo decide qual pergunta vai no topo da árvore"),
        nota("Como a árvore escolhe", [
            (r"$\text{Gini} = 1 - \sum_k p_k^2$", "impureza de Gini", "0 = grupo puro (uma classe só); 0,5 = meio a meio (duas classes)."),
            ("Ganho da divisão", "quanto a impureza caiu", "Impureza antes menos a média ponderada das impurezas depois."),
            ("<code>max_depth</code>, <code>min_samples_leaf</code>", "freios", "Controlam o tamanho da árvore e o overfitting."),
            ("<code>DecisionTreeClassifier</code>", "no scikit-learn", "<code>export_text</code> mostra as regras aprendidas."),
        ], rot="Agora sim, a matemática"),
        passos("Gini de um grupo com 6 sim e 4 não", [
            ("Proporções: p(sim) = 0,6 e p(não) = 0,4.", "Contagem dividida pelo total."),
            ("Quadrados: 0,36 + 0,16 = 0,52.", "Soma dos quadrados."),
            ("Gini = 1 − 0,52 = 0,48.", "Bem misturado."),
            ("Um grupo com 10 sim e 0 não: Gini = 1 − 1 = 0.", "Puro: perfeito para uma folha."),
        ]),
        cod("Gini e a melhor divisão", "Implemente <code>gini(rotulos)</code> e <code>ganho(rotulos, esquerda, direita)</code> (impureza antes menos a média ponderada depois). Depois descubra qual dos dois cortes de idade separa melhor.",
            '''
def gini(rotulos):
    return 0.0

def ganho(rotulos, esquerda, direita):
    return 0.0

idades = [22, 25, 31, 35, 42, 48, 55, 60]
compra = [0, 0, 0, 1, 1, 1, 1, 0]

def dividir(corte):
    esq = [c for i, c in zip(idades, compra) if i <= corte]
    dir_ = [c for i, c in zip(idades, compra) if i > corte]
    return esq, dir_

print(ganho(compra, *dividir(31)), ganho(compra, *dividir(48)))
''',
            [("Gini de grupo puro é 0", "assert gini([1, 1, 1]) == 0"), ("Gini 6x4 é 0.48", "assert abs(gini([1] * 6 + [0] * 4) - 0.48) < 1e-9"),
             ("Ganho do corte em 31", "assert abs(ganho(compra, *dividir(31)) - 0.2875) < 1e-4, f'deu {ganho(compra, *dividir(31))}'"),
             ("Corte em 31 é melhor que em 48", "assert ganho(compra, *dividir(31)) > ganho(compra, *dividir(48))")],
            '''
def gini(rotulos):
    n = len(rotulos)
    if n == 0:
        return 0.0
    return 1 - sum((rotulos.count(c) / n) ** 2 for c in set(rotulos))

def ganho(rotulos, esquerda, direita):
    n = len(rotulos)
    depois = len(esquerda) / n * gini(esquerda) + len(direita) / n * gini(direita)
    return gini(rotulos) - depois

idades = [22, 25, 31, 35, 42, 48, 55, 60]
compra = [0, 0, 0, 1, 1, 1, 1, 0]

def dividir(corte):
    esq = [c for i, c in zip(idades, compra) if i <= corte]
    dir_ = [c for i, c in zip(idades, compra) if i > corte]
    return esq, dir_

print(ganho(compra, *dividir(31)), ganho(compra, *dividir(48)))
''', ["Gini: <code>1 - sum((rotulos.count(c) / n) ** 2 for c in set(rotulos))</code>.", "Ganho: <code>gini(rotulos) - (len(esq)/n * gini(esq) + len(dir)/n * gini(dir))</code>."]),
        lab("Vendo as regras aprendidas", '''
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, export_text

X, y = load_iris(return_X_y=True, as_frame=True)
arvore = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X, y)
print(export_text(arvore, feature_names=list(X.columns)))
''', corpo="<p>Rode no Colab: a árvore vira regras de <code>if</code> legíveis.</p>", exps=["Aumente <code>max_depth</code> para 5. As regras ficam mais confiáveis ou só mais complicadas?"]),
        erros([
            ("Árvore sem limite de profundidade.", "Overfitting garantido."),
            ("Achar que árvores precisam de dados normalizados.", "Não precisam: elas só comparam com cortes."),
            ("Confiar numa árvore só.", "Pequenas mudanças nos dados mudam muito a árvore. Florestas (próxima aula) resolvem isso."),
        ]),
        ponte("Das árvores aos campeões",
              "<p>Sozinhas, árvores são instáveis. Em conjunto, viram Random Forest e Gradient Boosting (XGBoost, LightGBM), que até hoje vencem redes neurais na maioria dos problemas com tabelas. Toda a próxima sequência de aulas é sobre combinar árvores.</p>"),
        quiz([
            ("Qual o Gini de um grupo com metade de cada classe?", ["0", "0,5", "1"], 1, "1 − (0,25 + 0,25)."),
            ("Como a árvore escolhe a pergunta do topo?", ["Ao acaso.", "Pela que mais reduz a impureza.", "Pela primeira coluna."], 1, "Maior ganho."),
            ("Qual parâmetro combate o overfitting numa árvore?", ["<code>max_depth</code>", "<code>random_state</code>", "<code>n_jobs</code>"], 0, "Limita a profundidade."),
        ]),
    ],
    ["A árvore escolhe, a cada nó, a pergunta que mais reduz a impureza.", "Gini mede a mistura de classes num grupo.", "Sem limites, a árvore decora: use <code>max_depth</code>."],
    "Random Forest: a sabedoria da multidão de árvores.",
    livro=("ISLP", "Capítulo 8, “Tree-Based Methods”, seção 8.1", "Como o livro poda uma árvore grande?"))

AULAS["Random Forest"] = aula(
    30,
    "Uma árvore sozinha erra de um jeito muito particular. Cem árvores diferentes, cada uma vendo um pedaço dos dados, erram de jeitos diferentes, e na votação os erros se cancelam. É a sabedoria da multidão, em forma de algoritmo.",
    ["entender bagging e a escolha aleatória de atributos;", "saber por que a votação reduz a variância;", "usar a floresta e seus hiperparâmetros principais."],
    ["Árvores de decisão."],
    [
        chute("Cada árvore de uma floresta acerta 70% das vezes, e os erros são independentes. Como fica a votação de 101 árvores?", ["70%.", "Bem acima de 70%.", "Abaixo de 70%."], 1,
              ["A votação faz diferença quando os erros não andam juntos.", "Isso! Com erros independentes, a maioria acerta quase sempre. O desafio é fazer as árvores serem diferentes entre si.", "Votar entre modelos melhores que o acaso não piora."],
              "O segredo da floresta é a <b>diversidade</b> das árvores."),
        concreto("Adivinhar o peso do boi", "<p>Numa feira, centenas de pessoas chutaram o peso de um boi. Nenhum chute era bom sozinho, mas a <b>média</b> de todos ficou quase exata. Erros diferentes se cancelam. A floresta aplica isso às árvores.</p>"),
        nota("Como a floresta cria diversidade", [
            ("Bootstrap", "amostra com reposição", "Cada árvore treina numa amostra sorteada dos dados (algumas linhas repetem, outras ficam de fora)."),
            ("<code>max_features</code>", "atributos sorteados", "Em cada divisão, só um subconjunto aleatório de colunas pode ser usado."),
            ("Votação / média", "agregação", "Classificação: voto da maioria. Regressão: média."),
            ("<code>n_estimators</code>", "número de árvores", "Mais árvores não causam overfitting; só custam tempo."),
            ("OOB score", "fora da sacola", "As linhas que ficaram fora de cada amostra servem de validação grátis."),
        ]),
        cod("A força da votação", "Simule 101 “árvores” independentes que acertam com probabilidade 0.7 em 2.000 exemplos. Calcule a acurácia de uma árvore média e a acurácia da votação da maioria.",
            '''
import numpy as np

rng = np.random.default_rng(0)
acertos = rng.random((101, 2000)) < 0.7   # linha = árvore, coluna = exemplo

acc_uma = None
acc_votacao = None
print(acc_uma, acc_votacao)
''',
            [("Uma árvore ≈ 0.7", "assert abs(acc_uma - 0.7) < 0.02, f'acc_uma = {acc_uma}'"), ("Votação passa de 0.99", "assert acc_votacao > 0.99, f'acc_votacao = {acc_votacao}'")],
            '''
import numpy as np

rng = np.random.default_rng(0)
acertos = rng.random((101, 2000)) < 0.7

acc_uma = acertos.mean()
acc_votacao = (acertos.sum(axis=0) > 50).mean()
print(acc_uma, acc_votacao)
''', ["Uma árvore média: <code>acertos.mean()</code>.", "Votação: em cada exemplo (coluna), mais de 50 das 101 acertaram? <code>(acertos.sum(axis=0) &gt; 50).mean()</code>."],
            exp="<p>Na prática as árvores <b>não</b> são independentes (veem dados parecidos), por isso o ganho real é menor. Sortear linhas e colunas existe justamente para descorrelacioná-las.</p>"),
        lab("Árvore × floresta", '''
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

X, y = load_breast_cancer(return_X_y=True)
for nome, m in [("árvore", DecisionTreeClassifier(random_state=0)),
                ("floresta", RandomForestClassifier(n_estimators=300, random_state=0, n_jobs=-1))]:
    print(nome, cross_val_score(m, X, y, cv=5).mean().round(3))
''', corpo="<p>Rode no Colab:</p>", exps=["Compare as médias. Quanto a floresta ganhou?", "Use <code>oob_score=True</code> e compare o <code>oob_score_</code> com a validação cruzada."]),
        erros([
            ("Achar que mais árvores causam overfitting.", "Não causam; a curva estabiliza. Overfitting vem de árvores individuais profundas demais com poucos dados."),
            ("Esperar que a floresta extrapole.", "Ela só prevê dentro da faixa de valores vista no treino."),
            ("Modelo enorme em produção.", "Centenas de árvores profundas ocupam memória e são lentas. Ajuste o tamanho."),
        ]),
        ponte("Ensembles em IA",
              "<p>A ideia de combinar modelos aparece em toda parte: média de várias execuções de uma rede, “votação” entre várias respostas de um LLM (self-consistency) e as misturas de especialistas (MoE) dentro dos próprios LLMs modernos.</p>"),
        quiz([
            ("O que é bagging?", ["Treinar árvores em amostras sorteadas com reposição e combinar.", "Podar árvores.", "Normalizar os dados."], 0, "Bootstrap + agregação."),
            ("Por que sortear atributos em cada divisão?", ["Para acelerar a leitura.", "Para as árvores ficarem mais diferentes entre si.", "Para remover colunas inúteis."], 1, "Diversidade reduz a correlação dos erros."),
            ("Como a floresta combina as árvores na classificação?", ["Pega a melhor árvore.", "Voto da maioria.", "Multiplica as previsões."], 1, "Na regressão, a média."),
        ]),
    ],
    ["Random Forest = muitas árvores diversas + votação.", "Diversidade vem do bootstrap e do sorteio de atributos.", "Reduz a variância de uma árvore sozinha."],
    "Gradient Boosting: árvores que corrigem os erros das anteriores.",
    livro=("ISLP", "Capítulo 8, seção 8.2.1 e 8.2.2 (bagging e random forests)", "Como o livro explica a estimativa out-of-bag?"))

AULAS["Gradient Boosting (XGBoost, LightGBM)"] = aula(
    35,
    "A floresta treina árvores em paralelo e tira a média. O boosting treina em <b>sequência</b>: cada árvore nova olha os erros da anterior e tenta corrigi-los. Essa ideia simples domina as competições de dados tabulares há uma década.",
    ["entender o boosting como soma de correções;", "relacionar resíduos e gradiente;", "ajustar taxa de aprendizado, número de árvores e early stopping."],
    ["Árvores de decisão, Random Forest e gradiente descendente."],
    [
        chute("O primeiro modelo previu 100 para uma casa que vale 130. O que a segunda árvore do boosting tenta prever?", ["130.", "O resíduo: 30.", "100 de novo."], 1,
              ["Ela não recomeça do zero.", "Isso! Cada nova árvore aprende o que falta: o erro do conjunto até agora.", "Repetir não corrige nada."],
              "Previsão final = previsão inicial + correção 1 + correção 2 + ..."),
        concreto("O golfista", "<p>A primeira tacada leva a bola perto do buraco. As seguintes são tacadas curtas, cada uma corrigindo o que faltou. Ninguém tenta acertar de uma vez: o boosting soma pequenas correções até chegar.</p>"),
        ver("como o vídeo calcula os resíduos e os soma à previsão anterior"),
        nota("As peças do boosting", [
            ("$F_0$ = média de y", "ponto de partida", "A previsão mais simples possível."),
            ("$r = y - F_{m-1}$", "resíduos", "O que falta acertar. Para o MSE, é o gradiente negativo: daí o nome."),
            (r"$F_m = F_{m-1} + \eta \cdot h_m$", "soma com taxa", "Cada árvore $h_m$ entra com um peso pequeno $\\eta$ (learning rate)."),
            ("<code>n_estimators</code>, <code>learning_rate</code>, <code>max_depth</code>", "hiperparâmetros", "Taxa menor pede mais árvores; árvores rasas (3 a 8 níveis)."),
            ("<code>early_stopping_rounds</code>", "parar a tempo", "Para quando a validação para de melhorar."),
        ], rot="Agora sim, a fórmula"),
        cod("Boosting com “tocos”", "Implemente um boosting simples para regressão: comece pela média e, a cada passo, ajuste um <b>toco</b> (árvore de uma pergunta, já pronta em <code>toco</code>) aos resíduos e some com taxa 0.5. Após 30 passos, o MSE de treino deve cair muito.",
            '''
import numpy as np

def toco(x, r):
    """Melhor árvore de uma pergunta para prever r: devolve uma função."""
    melhor = None
    for c in np.unique(x)[:-1]:
        e, d = r[x <= c].mean(), r[x > c].mean()
        erro = ((r - np.where(x <= c, e, d)) ** 2).sum()
        if melhor is None or erro < melhor[0]:
            melhor = (erro, c, e, d)
    _, c, e, d = melhor
    return lambda z: np.where(z <= c, e, d)

x = np.arange(20, dtype=float)
y = np.sin(x / 3) * 10

previsao = np.full_like(y, y.mean())
mse_inicial = ((y - previsao) ** 2).mean()

for passo in range(30):
    pass  # resíduos -> toco -> atualize a previsão

mse_final = ((y - previsao) ** 2).mean()
print(round(mse_inicial, 2), round(mse_final, 2))
''',
            [("MSE caiu para menos de 10% do inicial", "assert mse_final < mse_inicial * 0.1, f'inicial={mse_inicial:.2f}, final={mse_final:.2f}'")],
            '''
import numpy as np

def toco(x, r):
    melhor = None
    for c in np.unique(x)[:-1]:
        e, d = r[x <= c].mean(), r[x > c].mean()
        erro = ((r - np.where(x <= c, e, d)) ** 2).sum()
        if melhor is None or erro < melhor[0]:
            melhor = (erro, c, e, d)
    _, c, e, d = melhor
    return lambda z: np.where(z <= c, e, d)

x = np.arange(20, dtype=float)
y = np.sin(x / 3) * 10

previsao = np.full_like(y, y.mean())
mse_inicial = ((y - previsao) ** 2).mean()

for passo in range(30):
    residuos = y - previsao
    h = toco(x, residuos)
    previsao = previsao + 0.5 * h(x)

mse_final = ((y - previsao) ** 2).mean()
print(round(mse_inicial, 2), round(mse_final, 2))
''', ["Resíduos: <code>y - previsao</code>.", "<code>h = toco(x, residuos)</code> e <code>previsao = previsao + 0.5 * h(x)</code>."]),
        lab("XGBoost com early stopping", '''
import xgboost as xgb
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

X, y = fetch_california_housing(return_X_y=True)
Xtr, Xva, ytr, yva = train_test_split(X, y, test_size=0.2, random_state=0)
modelo = xgb.XGBRegressor(n_estimators=2000, learning_rate=0.05, max_depth=6, early_stopping_rounds=50)
modelo.fit(Xtr, ytr, eval_set=[(Xva, yva)], verbose=200)
print("melhor número de árvores:", modelo.best_iteration)
''', corpo="<p>Rode no Colab:</p>", exps=["Troque a taxa para 0.2. O número ideal de árvores sobe ou desce?", "Compare com o LightGBM (<code>lightgbm.LGBMRegressor</code>): qual treina mais rápido?"]),
        erros([
            ("Taxa de aprendizado alta com muitas árvores.", "Overfitting rápido. Taxa baixa + early stopping."),
            ("Árvores profundas no boosting.", "Cada árvore deve ser fraca: 3 a 8 níveis."),
            ("Esquecer o conjunto de validação no early stopping.", "Sem ele, o boosting continua até decorar o treino."),
        ]),
        ponte("Boosting e redes neurais",
              "<p>Somar correções guiadas pelo gradiente é a mesma intuição do treino de redes neurais, só que aplicada a árvores em vez de pesos. Para dados tabulares, XGBoost e LightGBM são o primeiro modelo a testar, antes de qualquer rede neural.</p>"),
        quiz([
            ("O que cada nova árvore aprende no boosting?", ["Os dados originais.", "Os erros (resíduos) do conjunto até agora.", "Uma amostra aleatória."], 1, "Correções sucessivas."),
            ("Qual a diferença central para a Random Forest?", ["Boosting treina em sequência; a floresta, em paralelo.", "Boosting não usa árvores.", "Nenhuma."], 0, "Sequencial × independente."),
            ("Para que serve o early stopping?", ["Acelerar a leitura dos dados.", "Parar quando a validação deixa de melhorar.", "Reduzir o número de atributos."], 1, "Evita overfitting."),
        ]),
    ],
    ["Boosting soma árvores fracas, cada uma corrigindo o erro anterior.", "Os resíduos são o gradiente da perda: daí “gradient boosting”.", "Taxa baixa, árvores rasas e early stopping."],
    "K-Means: encontrar grupos sem rótulos.",
    livro=("ISLP", "Capítulo 8, seção 8.2.3, “Boosting”", "Quais são os três hiperparâmetros do boosting segundo o livro?"))

AULAS["K-Means e clusterização"] = aula(
    30,
    "Milhares de clientes e nenhuma etiqueta. O K-Means descobre sozinho grupos de pessoas parecidas, repetindo dois passos simples até estabilizar. É o algoritmo de agrupamento mais usado do mundo.",
    ["executar o K-Means passo a passo;", "escolher o número de grupos (k);", "interpretar os centroides."],
    ["NumPy e broadcasting; aprendizado não supervisionado."],
    [
        chute("Quantos grupos o K-Means encontra?", ["Ele descobre sozinho.", "Exatamente o k que você escolher.", "Sempre 3."], 1,
              ["Essa é a grande limitação: o k é dado por você.", "Isso! E escolher k bem é metade do trabalho.", "3 é só um exemplo comum."],
              "Use o método do cotovelo, a silhueta ou o conhecimento do negócio."),
        concreto("Onde abrir as lojas", "<p>Uma rede quer abrir 3 lojas numa cidade. Começa chutando 3 lugares. Cada cliente vai para a loja mais perto. Depois, cada loja muda para o centro dos seus clientes. Repete até as lojas pararem de mudar. É o K-Means.</p>"),
        passos("Os dois passos que se repetem", [
            ("Escolha k centroides iniciais (ao acaso, ou com k-means++).", "Os “lugares” das lojas."),
            ("<b>Atribuir</b>: cada ponto vai para o centroide mais próximo.", "Distância euclidiana."),
            ("<b>Atualizar</b>: cada centroide vira a média dos seus pontos.", "A loja vai para o centro dos clientes."),
            ("Repita até as atribuições não mudarem.", "Converge em poucas iterações."),
        ]),
        cod("K-Means do zero", "Complete os dois passos dentro do laço: atribuir cada ponto ao centroide mais próximo (use broadcasting) e mover cada centroide para a média dos seus pontos.",
            '''
import numpy as np

rng = np.random.default_rng(1)
X = np.vstack([rng.normal([0, 0], 0.5, (30, 2)), rng.normal([5, 5], 0.5, (30, 2)), rng.normal([0, 5], 0.5, (30, 2))])
centros = X[[0, 30, 60]].copy()

for it in range(10):
    rotulos = np.zeros(len(X), dtype=int)   # passo 1: centroide mais próximo de cada ponto
    # passo 2: atualize centros[j] com a média dos pontos do grupo j

print(np.round(centros, 1))
''',
            [("Três grupos de 30", "assert sorted(np.bincount(rotulos).tolist()) == [30, 30, 30], f'tamanhos = {np.bincount(rotulos)}'"),
             ("Centros perto dos verdadeiros", "import numpy as np\nachados = sorted(map(tuple, np.round(centros)))\nassert achados == [(0.0, 0.0), (0.0, 5.0), (5.0, 5.0)], f'centros = {achados}'")],
            '''
import numpy as np

rng = np.random.default_rng(1)
X = np.vstack([rng.normal([0, 0], 0.5, (30, 2)), rng.normal([5, 5], 0.5, (30, 2)), rng.normal([0, 5], 0.5, (30, 2))])
centros = X[[0, 30, 60]].copy()

for it in range(10):
    dist = ((X[:, None, :] - centros[None, :, :]) ** 2).sum(axis=2)
    rotulos = dist.argmin(axis=1)
    for j in range(len(centros)):
        centros[j] = X[rotulos == j].mean(axis=0)

print(np.round(centros, 1))
''', ["Distâncias de todos para todos: <code>((X[:, None, :] - centros[None, :, :]) ** 2).sum(axis=2)</code> tem formato (90, 3).", "<code>argmin(axis=1)</code> dá o centroide mais próximo; a média por grupo usa uma máscara."]),
        nota("Escolhendo k", [
            ("Inércia", "soma das distâncias ao centroide", "Sempre cai quando k aumenta."),
            ("Método do cotovelo", "onde a queda desacelera", "O “cotovelo” do gráfico de inércia por k."),
            ("Silhueta", "coesão × separação", "De −1 a 1; quanto maior, mais bem definidos os grupos."),
            ("Negócio", "o que é útil", "5 segmentos de clientes que o marketing consegue usar valem mais que o k “ótimo”."),
        ], rot="Escolhendo k"),
        erros([
            ("Rodar sem padronizar.", "Uma coluna em reais domina uma em anos. Padronize antes."),
            ("Esperar grupos de formato estranho (anéis, meias-luas).", "K-Means acha grupos “redondos”. Para outros formatos, DBSCAN."),
            ("Confiar numa única inicialização.", "Resultados variam. Use várias (<code>n_init</code>) e k-means++."),
        ]),
        ponte("Agrupamento em IA moderna",
              "<p>Agrupar <b>embeddings</b> de textos revela os assuntos de milhares de mensagens de clientes sem ninguém ler tudo. Bancos vetoriais usam K-Means para organizar índices de busca (IVF). E a quantização de vetores começa com uma clusterização.</p>"),
        quiz([
            ("Qual é o passo de atualização do K-Means?", ["Cada ponto troca de grupo ao acaso.", "Cada centroide vira a média dos pontos do seu grupo.", "Remove os pontos distantes."], 1, "A loja vai para o centro dos clientes."),
            ("Por que padronizar antes?", ["Para convergir em 1 passo.", "Para colunas com escalas grandes não dominarem a distância.", "Não é necessário."], 1, "A distância depende da escala."),
            ("O K-Means tem dificuldade com:", ["Grupos redondos.", "Grupos de formatos alongados ou em anel.", "Dados numéricos."], 1, "Use DBSCAN."),
        ]),
    ],
    ["K-Means alterna atribuir pontos e mover centroides.", "Você escolhe k: cotovelo, silhueta e utilidade.", "Padronize e use várias inicializações."],
    "PCA: resumir muitas colunas em poucas.",
    livro=("ISLP", "Capítulo 12, seção 12.4.1, “K-Means Clustering”", "Por que o livro recomenda rodar o algoritmo várias vezes?"))

AULAS["PCA"] = aula(
    35,
    "Um dataset com 300 colunas não cabe num gráfico. O PCA encontra as poucas direções em que os dados mais variam e resume tudo nelas, muitas vezes guardando 90% da informação em 10 colunas. É a forma mais clássica de ver o invisível.",
    ["entender componentes principais como direções de maior variância;", "calcular PCA com NumPy;", "escolher quantos componentes manter."],
    ["Vetores e produto escalar (Matemática); NumPy."],
    [
        chute("Pontos alinhados quase numa reta diagonal, num gráfico 2D. Quantas dimensões bastam para descrevê-los bem?", ["2", "1", "0"], 1,
              ["A segunda direção quase não tem variação.", "Isso! A posição ao longo da reta diz quase tudo. O PCA acha essa reta.", "Os pontos não estão todos no mesmo lugar."],
              "PCA = encontrar as direções em que os dados se espalham mais."),
        concreto("A sombra do objeto", "<p>Você pode descrever um avião 3D pela sombra no chão. Uma sombra boa (vista de cima) mostra asas e cauda; uma ruim (vista de frente) vira uma mancha. O PCA escolhe o ângulo da lâmpada que gera a sombra mais informativa.</p>"),
        nota("Os conceitos", [
            ("Centralizar", "subtrair a média", "O PCA trabalha com variações em torno do centro."),
            ("Componente principal 1", "direção de maior variância", "O componente 2 é a de maior variância perpendicular ao 1, e assim por diante."),
            ("Variância explicada", "quanto cada componente guarda", "Some até chegar a 90% ou 95%."),
            ("SVD: <code>np.linalg.svd(Xc)</code>", "o cálculo", "As linhas de <code>Vt</code> são os componentes."),
        ], rot="Agora sim, os conceitos"),
        cod("PCA com NumPy", "Complete: centralize os dados, faça o SVD, guarde em <code>comp1</code> a primeira direção principal e em <code>var_exp</code> a fração de variância de cada componente.",
            '''
import numpy as np

rng = np.random.default_rng(0)
t = rng.normal(0, 3, 200)
X = np.column_stack([t, 0.5 * t + rng.normal(0, 0.3, 200)])

comp1 = None
var_exp = None
print(comp1, var_exp)
''',
            [("Primeiro componente explica mais de 95%", "assert var_exp[0] > 0.95, f'var_exp = {var_exp}'"), ("Frações somam 1", "assert abs(sum(var_exp) - 1) < 1e-9"),
             ("Direção ≈ (0.89, 0.45)", "import numpy as np\nd = np.abs(comp1) / np.linalg.norm(comp1)\nassert np.allclose(d, [0.894, 0.447], atol=0.02), f'comp1 = {comp1}'")],
            '''
import numpy as np

rng = np.random.default_rng(0)
t = rng.normal(0, 3, 200)
X = np.column_stack([t, 0.5 * t + rng.normal(0, 0.3, 200)])

Xc = X - X.mean(axis=0)
U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
comp1 = Vt[0]
var_exp = S ** 2 / (S ** 2).sum()
print(comp1, var_exp)
''', ["<code>Xc = X - X.mean(axis=0)</code>", "<code>U, S, Vt = np.linalg.svd(Xc, full_matrices=False)</code>; variância explicada = <code>S**2 / (S**2).sum()</code>."]),
        lab("Dígitos em 2D", '''
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
import plotly.express as px

X, y = load_digits(return_X_y=True)          # 64 colunas (8x8 pixels)
Z = PCA(n_components=2).fit_transform(X)
px.scatter(x=Z[:, 0], y=Z[:, 1], color=y.astype(str)).show()
''', corpo="<p>Rode no Colab: 64 dimensões viram um mapa 2D.</p>", exps=["Quais dígitos ficam misturados? Faz sentido visualmente (1 e 7, 3 e 8)?", "Quantos componentes são precisos para 90% da variância? Use <code>PCA(0.9)</code>."]),
        erros([
            ("PCA sem padronizar colunas de escalas diferentes.", "A coluna de maior escala vira o “componente principal” por acaso."),
            ("Achar que os componentes têm significado óbvio.", "São combinações de todas as colunas; interpretar exige cuidado."),
            ("Ajustar o PCA no conjunto inteiro antes de separar.", "Ajuste só no treino e aplique no teste."),
        ]),
        ponte("Visualizando embeddings",
              "<p>Embeddings de LLMs têm centenas ou milhares de dimensões. PCA (e seus primos t-SNE e UMAP) os projetam em 2D para você ver frases parecidas agrupadas. E a ideia de “poucas direções guardam quase tudo” reaparece no LoRA, que ajusta LLMs com matrizes de posto baixo.</p>"),
        quiz([
            ("O que é o primeiro componente principal?", ["A primeira coluna do dataset.", "A direção de maior variância dos dados.", "A média dos dados."], 1, "Onde eles mais se espalham."),
            ("Por que centralizar antes do PCA?", ["Para variância ser medida em torno da média.", "Para acelerar.", "Não é necessário."], 0, "O PCA olha variações."),
            ("Como escolher quantos componentes manter?", ["Sempre 2.", "Pela variância explicada acumulada (ex.: 90%).", "Pelo número de linhas."], 1, "Ou 2 para visualizar."),
        ]),
    ],
    ["PCA acha as direções de maior variância e projeta os dados nelas.", "Centralize (e padronize) antes; calcule via SVD.", "Escolha os componentes pela variância explicada."],
    "Métricas de classificação: além da acurácia.",
    livro=("ISLP", "Capítulo 12, seção 12.2, “Principal Components Analysis”", "Como o livro interpreta os loadings no exemplo de crimes?"))
