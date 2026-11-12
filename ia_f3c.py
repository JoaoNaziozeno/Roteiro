# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 3 (parte C): pré-processamento, interpretação e ética."""
from lesson_factory import *

AULAS = {}

AULAS["Normalização e padronização"] = aula(
    25,
    "Idade vai de 0 a 100; renda, de 0 a 100 mil. Para um modelo que mede distâncias ou usa gradiente, a renda grita e a idade sussurra. Colocar as colunas na mesma escala é um passo pequeno que muda muito o resultado.",
    ["padronizar (z-score) e normalizar (min-max);", "saber quais modelos precisam disso;", "ajustar o escalonador só no treino."],
    ["Pipelines e KNN."],
    [
        chute("Qual destes modelos <b>não</b> precisa de escalonamento?", ["KNN.", "Árvore de decisão.", "Regressão logística com gradiente."], 1,
              ["O KNN usa distâncias: precisa.", "Isso! Árvores só comparam valores com cortes; a escala não muda a ordem.", "O gradiente converge mal com escalas diferentes."],
              "Distância, gradiente ou regularização? Escalone. Árvores? Não precisa."),
        concreto("Moedas de países diferentes", "<p>Comparar 100 ienes com 100 reais sem converter dá conclusões absurdas. Escalonar é converter todas as colunas para a mesma “moeda” antes de comparar.</p>"),
        nota("As duas formas", [
            (r"$z = \frac{x - \mu}{\sigma}$", "padronização", "Média 0 e desvio 1. Padrão para a maioria dos modelos."),
            (r"$x' = \frac{x - \min}{\max - \min}$", "min-max", "Entre 0 e 1. Comum em imagens e redes neurais."),
            ("<code>RobustScaler</code>", "robusto", "Usa mediana e quartis: resiste a outliers."),
            ("<code>np.log1p(x)</code>", "logaritmo", "Para colunas muito assimétricas, como renda e preços."),
        ]),
        cod("Min-max com parâmetros do treino", "Implemente <code>minmax_fit</code> (devolve mínimo e máximo do treino) e <code>minmax_transform</code>. Valores do teste podem sair de [0, 1], e isso é esperado.",
            '''
import numpy as np

def minmax_fit(x):
    return 0.0, 1.0

def minmax_transform(x, minimo, maximo):
    return x

treino = np.array([10.0, 20.0, 30.0])
teste = np.array([40.0])
mn, mx = minmax_fit(treino)
print(minmax_transform(treino, mn, mx), minmax_transform(teste, mn, mx))
''',
            [("Treino entre 0 e 1", "import numpy as np\nmn, mx = minmax_fit(np.array([10.0, 20, 30]))\nassert np.allclose(minmax_transform(np.array([10.0, 20, 30]), mn, mx), [0, 0.5, 1])"),
             ("Teste usa parâmetros do treino", "import numpy as np\nmn, mx = minmax_fit(np.array([10.0, 20, 30]))\nassert np.allclose(minmax_transform(np.array([40.0]), mn, mx), [1.5])")],
            '''
import numpy as np

def minmax_fit(x):
    return x.min(), x.max()

def minmax_transform(x, minimo, maximo):
    return (x - minimo) / (maximo - minimo)

treino = np.array([10.0, 20.0, 30.0])
teste = np.array([40.0])
mn, mx = minmax_fit(treino)
print(minmax_transform(treino, mn, mx), minmax_transform(teste, mn, mx))
''', ["<code>x.min(), x.max()</code> no fit; a fórmula no transform."]),
        erros([("Ajustar o escalonador nos dados inteiros.", "Vazamento: ajuste só no treino (pipeline resolve)."), ("Min-max com outliers.", "Um valor extremo espreme todos os outros perto de zero. Use padronização ou RobustScaler."), ("Escalonar a variável-alvo e esquecer de desfazer.", "As previsões ficam na escala errada.")]),
        ponte("Normalização dentro das redes", "<p>Redes neurais normalizam não só a entrada: BatchNorm e LayerNorm (Fase 4) padronizam as ativações dentro da rede. Todo Transformer tem LayerNorm em cada bloco. A ideia desta aula vive no coração dos LLMs.</p>"),
        quiz([
            ("Padronização produz:", ["Valores entre 0 e 1.", "Média 0 e desvio 1.", "Só valores positivos."], 1, "z-score."),
            ("Qual escalonador resiste a outliers?", ["MinMaxScaler.", "RobustScaler.", "Nenhum."], 1, "Mediana e quartis."),
            ("Onde ajustar o escalonador?", ["No conjunto inteiro.", "Só no treino.", "Só no teste."], 1, "E aplicar no resto."),
        ]),
    ],
    ["Escalone para modelos com distância, gradiente ou regularização.", "Padronização (z) é o padrão; min-max para [0, 1].", "Ajuste só no treino."],
    "Dados desbalanceados.",
    livro=("PDSH:05.04-feature-engineering", "Seção 5.4, “Feature Engineering”, parte sobre transformações", "Que transformações de atributos o livro sugere?"))

AULAS["Dados desbalanceados (SMOTE)"] = aula(
    30,
    "Fraudes são 0,2% das transações; doenças raras, 1 em mil. Com classes tão desiguais, o modelo aprende que “nunca” é uma ótima resposta. Há três frentes para resolver: a métrica, os pesos e os dados.",
    ["reconhecer o problema do desbalanceamento;", "usar pesos de classe, reamostragem e SMOTE;", "ajustar o limiar de decisão."],
    ["Métricas e matriz de confusão."],
    [
        chute("Qual a <b>primeira</b> coisa a mudar num problema com 1% de positivos?", ["Gerar dados sintéticos com SMOTE.", "Trocar a métrica: parar de olhar acurácia.", "Comprar uma GPU."], 1,
              ["SMOTE pode ajudar, mas não antes de medir direito.", "Isso! Com a métrica certa (recall, F1, AUC-PR), você vê o problema e mede a melhora.", "Hardware não resolve."],
              "Métrica → pesos → limiar → reamostragem, nessa ordem."),
        concreto("Ensinar a reconhecer um pássaro raro", "<p>Mostrando 999 fotos de pombos e 1 de arara, o aprendiz conclui que “é sempre pombo”. Para ensinar, você dá mais atenção às araras (pesos), mostra mais vezes as fotos de arara (reamostragem) ou cria variações delas (SMOTE).</p>"),
        nota("As ferramentas", [
            ("<code>class_weight=\"balanced\"</code>", "pesos", "Erros na classe rara custam mais. Simples e eficaz."),
            ("Undersampling", "menos da maioria", "Descarta exemplos comuns; perde informação."),
            ("Oversampling / SMOTE", "mais da minoria", "Repete ou cria exemplos sintéticos entre vizinhos da classe rara."),
            ("Ajuste de limiar", "decisão", "Baixar o limiar aumenta o recall da classe rara."),
            ("Reamostrar só o treino", "regra de ouro", "Validação e teste mantêm a proporção real."),
        ]),
        cod("SMOTE na mão", "O SMOTE cria um ponto sintético entre um exemplo raro e um vizinho raro: novo = a + t·(b − a), com t entre 0 e 1. Complete a função e gere 4 pontos novos.",
            '''
import numpy as np

def smote_par(a, b, t):
    return a

rng = np.random.default_rng(0)
raros = np.array([[1.0, 1.0], [2.0, 2.0], [1.5, 2.5]])
novos = []
for _ in range(4):
    i, j = rng.choice(len(raros), 2, replace=False)
    novos.append(smote_par(raros[i], raros[j], rng.random()))
print(np.round(novos, 2))
''',
            [("Ponto no meio do caminho", "import numpy as np\nassert np.allclose(smote_par(np.array([0.0, 0]), np.array([2.0, 4]), 0.5), [1, 2])"),
             ("t=0 devolve a, t=1 devolve b", "import numpy as np\na, b = np.array([1.0, 1]), np.array([3.0, 5])\nassert np.allclose(smote_par(a, b, 0), a) and np.allclose(smote_par(a, b, 1), b)")],
            '''
import numpy as np

def smote_par(a, b, t):
    return a + t * (b - a)

rng = np.random.default_rng(0)
raros = np.array([[1.0, 1.0], [2.0, 2.0], [1.5, 2.5]])
novos = []
for _ in range(4):
    i, j = rng.choice(len(raros), 2, replace=False)
    novos.append(smote_par(raros[i], raros[j], rng.random()))
print(np.round(novos, 2))
''', ["<code>a + t * (b - a)</code>"]),
        erros([("Reamostrar antes de separar treino e teste.", "Exemplos sintéticos vazam para o teste e as métricas ficam falsas."), ("SMOTE em dados categóricos.", "Interpolar “Recife” e “Natal” não faz sentido. Use SMOTENC ou pesos."), ("Esquecer que o limiar padrão é 0,5.", "Com classes raras, o melhor limiar costuma ser bem menor.")]),
        ponte("Desbalanceamento em IA moderna", "<p>Moderação de conteúdo, detecção de alucinações e classificação de intenção raras sofrem do mesmo problema. Com LLMs, uma saída comum é gerar exemplos sintéticos da classe rara com o próprio modelo, o “SMOTE” da era generativa, com os mesmos cuidados.</p>"),
        quiz([
            ("Por que a acurácia engana com classes raras?", ["Fica sempre baixa.", "Um modelo que só prevê a classe comum já tem acurácia alta.", "Não engana."], 1, "99% sem pegar nada."),
            ("Onde aplicar a reamostragem?", ["No conjunto inteiro.", "Só no treino.", "Só no teste."], 1, "Teste com a proporção real."),
            ("O que o SMOTE faz?", ["Apaga exemplos da maioria.", "Cria exemplos sintéticos da minoria entre vizinhos.", "Muda os rótulos."], 1, "Interpolação."),
        ]),
    ],
    ["Com classes raras, troque a métrica antes de tudo.", "Pesos de classe e ajuste de limiar resolvem muito.", "Reamostragem e SMOTE só no treino."],
    "Seleção de atributos.",
    livro=("MLCC:", "Google ML Crash Course, “Classification”, parte sobre desbalanceamento", "Que técnica de downsampling com peso o curso descreve?"))

AULAS["Seleção de atributos"] = aula(
    25,
    "Mais colunas não é sempre melhor: colunas inúteis trazem ruído, overfitting e custo. Selecionar atributos é ficar com o que ajuda a prever, e de quebra ter um modelo mais rápido e mais fácil de explicar.",
    ["remover atributos constantes e redundantes;", "usar filtros, métodos embutidos e eliminação recursiva;", "evitar vazamento na seleção."],
    ["Correlação, Lasso e validação cruzada."],
    [
        chute("Duas colunas têm correlação 0,99 entre si (preço em reais e em dólares). O que fazer?", ["Manter as duas, mais informação.", "Manter uma: a outra é redundante.", "Remover as duas."], 1,
              ["É a mesma informação duas vezes.", "Isso! Redundância só aumenta custo e instabilidade dos pesos.", "Uma delas é útil."],
              "Comece pelo óbvio: constantes, duplicadas e quase idênticas."),
        concreto("Arrumar a mala", "<p>Para uma viagem de três dias, você não leva o guarda-roupa: tira o que é repetido, o que não vai usar e o que pesa demais. Seleção de atributos é fazer a mala do modelo.</p>"),
        nota("Três famílias", [
            ("Filtros", "antes do modelo", "Variância baixa, correlação com o alvo, informação mútua. Rápidos."),
            ("Embutidos", "durante o treino", "Lasso zera pesos; árvores dão importância."),
            ("Wrappers (RFE)", "testando o modelo", "Remove o pior atributo e treina de novo, repetidamente. Caro."),
            ("Seleção dentro da validação", "regra", "Escolher atributos olhando o conjunto todo vaza informação."),
        ]),
        cod("Filtro simples", "Remova as colunas com variância zero e, de cada par com correlação absoluta acima de 0.95, remova a segunda. Devolva a lista de colunas mantidas.",
            '''
import pandas as pd

def selecionar(df, limite=0.95):
    return list(df.columns)

df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 4, 6, 8.1], "c": [5, 5, 5, 5], "d": [4, 1, 3, 2]})
print(selecionar(df))
''',
            [("Mantém a e d", "assert selecionar(df) == ['a', 'd'], f'deu {selecionar(df)}'")],
            '''
import pandas as pd

def selecionar(df, limite=0.95):
    cols = [c for c in df.columns if df[c].var() > 0]
    mantidas = []
    for c in cols:
        if all(abs(df[c].corr(df[m])) <= limite for m in mantidas):
            mantidas.append(c)
    return mantidas

df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 4, 6, 8.1], "c": [5, 5, 5, 5], "d": [4, 1, 3, 2]})
print(selecionar(df))
''', ["Primeiro filtre <code>df[c].var() &gt; 0</code>.", "Depois mantenha uma coluna só se não for muito correlacionada com as já mantidas."]),
        erros([("Selecionar atributos com o dataset inteiro e depois validar.", "Vazamento: a seleção “viu” a validação. Faça dentro do pipeline."), ("Remover atributos só por correlação baixa com o alvo.", "Um atributo pode ser útil em combinação com outros."), ("Confiar em uma única execução da RFE.", "Confira a estabilidade com validação cruzada.")]),
        ponte("Seleção em LLMs: o contexto", "<p>Num RAG, escolher quais trechos entram no prompt é seleção de atributos: trechos inúteis distraem o modelo e custam tokens. Menos e melhor vale também para contexto.</p>"),
        quiz([
            ("Qual método é “embutido”?", ["Variância mínima.", "Lasso.", "Correlação com o alvo."], 1, "A seleção acontece no treino."),
            ("Por que remover colunas redundantes?", ["Para aumentar a acurácia sempre.", "Reduzem custo e instabilidade sem trazer informação nova.", "Não se deve remover."], 1, "Mesma informação duas vezes."),
            ("Onde fazer a seleção?", ["Antes de separar os dados.", "Dentro da validação, no pipeline.", "No teste."], 1, "Evita vazamento."),
        ]),
    ],
    ["Tire constantes, duplicadas e redundantes.", "Filtros, métodos embutidos e RFE.", "Selecione dentro da validação."],
    "Vazamento de dados: o erro que faz modelos parecerem geniais.",
    livro=("ISLP", "Capítulo 6, seção 6.1, “Subset Selection”", "Quais as diferenças entre forward e backward selection?"))

AULAS["Vazamento de dados (data leakage)"] = aula(
    30,
    "Um modelo com 99% de acurácia na validação e 60% em produção quase sempre tem a mesma causa: em algum lugar, a resposta vazou para os dados de treino. É o erro mais caro do machine learning, porque parece um sucesso.",
    ["reconhecer os tipos de vazamento;", "desconfiar de resultados bons demais;", "montar processos que impedem vazamento."],
    ["Treino/validação/teste, pipelines e séries temporais."],
    [
        chute("Para prever se um paciente terá pneumonia, o modelo usa a coluna “tomou antibiótico”. A acurácia é 98%. O que houve?", ["O modelo é excelente.", "Vazamento: o antibiótico é dado <b>depois</b> do diagnóstico.", "Faltou normalizar."], 1,
              ["Bom demais para ser verdade.", "Isso! No momento da previsão, essa informação ainda não existe.", "Normalizar não cria esse tipo de acerto."],
              "Pergunta-chave: no instante da previsão, eu teria esse dado?"),
        concreto("A cola na prova", "<p>Um aluno tira 10 em todos os simulados porque o gabarito estava no verso da folha. No vestibular, sem gabarito, a nota despenca. Vazamento é o gabarito escondido nos dados.</p>"),
        tabela("Tipos de vazamento", ["Tipo", "Exemplo", "Defesa"], [
            ["Do alvo", "Atributo que só existe depois do evento", "Pergunte se o dado existe no momento da previsão"],
            ["Do pré-processamento", "Média ou escalonador ajustado em todos os dados", "Pipeline; fit só no treino"],
            ["Temporal", "Treinar com dados do futuro", "Divisão por tempo"],
            ["De grupo", "Mesmo cliente no treino e no teste", "Divisão agrupada"],
            ["Duplicados", "Mesmo exemplo nos dois lados", "Deduplicar antes de separar"],
        ]),
        cod("Caça ao vazamento", "Para cada coluna candidata a prever <b>cancelamento de assinatura</b>, marque True se ela vaza (só existe depois do cancelamento) e False se é segura.",
            '''
colunas = {
    "meses_de_contrato": None,
    "data_do_pedido_de_cancelamento": None,
    "chamados_no_suporte_ultimo_mes": None,
    "motivo_do_cancelamento": None,
    "valor_da_mensalidade": None,
    "reembolso_emitido": None,
}
print(colunas)
''',
            [("Classificação correta", "certo = {'meses_de_contrato': False, 'data_do_pedido_de_cancelamento': True, 'chamados_no_suporte_ultimo_mes': False, 'motivo_do_cancelamento': True, 'valor_da_mensalidade': False, 'reembolso_emitido': True}\nerr = [k for k in certo if colunas[k] is not certo[k]]\nassert not err, f'reveja: {err}'")],
            '''
colunas = {
    "meses_de_contrato": False,
    "data_do_pedido_de_cancelamento": True,
    "chamados_no_suporte_ultimo_mes": False,
    "motivo_do_cancelamento": True,
    "valor_da_mensalidade": False,
    "reembolso_emitido": True,
}
print(colunas)
''', ["Pergunte, para cada coluna: ela existiria antes de o cliente cancelar?"]),
        erros([("Comemorar um resultado bom demais.", "Investigue: qual atributo mais importa? Ele faz sentido?"), ("Engenharia de atributos com o dataset inteiro.", "Médias por grupo, contagens e alvos agregados devem vir só do treino."), ("Avaliar com dados mais antigos que o treino.", "O teste deve ser o futuro.")]),
        ponte("Vazamento em LLMs", "<p>Se as perguntas de um benchmark estão na internet, provavelmente estão nos dados de treino do LLM: a nota fica inflada. Em RAG, avaliar com perguntas criadas a partir dos mesmos documentos usados para ajustar o sistema também vaza.</p>"),
        quiz([
            ("Qual sinal típico de vazamento?", ["Resultado bom demais e queda em produção.", "Treino lento.", "Muitas colunas."], 0, "Bom demais para ser verdade."),
            ("Escalonar os dados antes de separar é:", ["Correto.", "Vazamento do pré-processamento.", "Obrigatório."], 1, "A média usou o teste."),
            ("Como evitar vazamento temporal?", ["Embaralhando.", "Separando treino e teste pelo tempo.", "Usando mais colunas."], 1, "Passado treina, futuro testa."),
        ]),
    ],
    ["Vazamento é usar informação que não existiria no momento da previsão.", "Pipeline, divisão temporal e agrupada são as defesas.", "Desconfie de resultados bons demais."],
    "Séries temporais com machine learning.",
    livro=("MLCC:", "Google ML Crash Course, “Datasets, generalization, and overfitting”", "Que cuidados com a divisão dos dados o curso recomenda?"))

AULAS["Séries temporais com ML"] = aula(
    35,
    "Prever as vendas da semana que vem com um modelo de machine learning é possível, desde que você transforme o tempo em atributos e respeite uma regra sagrada: o modelo só pode ver o passado.",
    ["transformar uma série em tabela com defasagens e janelas;", "validar avançando no tempo;", "comparar com baselines ingênuos."],
    ["Séries temporais (Fase 2), Gradient Boosting e vazamento."],
    [
        chute("Qual é o primeiro modelo a testar para prever as vendas de amanhã?", ["Uma rede neural profunda.", "“Amanhã = hoje” (ou = mesmo dia da semana passada).", "Uma regressão com 300 atributos."], 1,
              ["Sem um baseline, você não sabe se a rede ajudou.", "Isso! Baselines ingênuos são surpreendentemente difíceis de vencer, e dão a régua.", "Comece simples."],
              "Se o seu modelo não bate o “repita a semana passada”, ele não serve."),
        concreto("O meteorologista amador", "<p>“Amanhã vai fazer o tempo de hoje” acerta muito mais do que parece. Um bom meteorologista começa daí e acrescenta pistas: estação do ano, frente fria chegando. É assim que se constrói um modelo de série temporal.</p>"),
        nota("Do tempo à tabela", [
            ("Defasagens (<i>lags</i>)", "<code>shift(1)</code>, <code>shift(7)</code>", "O valor de ontem e de uma semana atrás."),
            ("Janelas", "<code>shift(1).rolling(7).mean()</code>", "Média dos últimos 7 dias, sem incluir hoje."),
            ("Calendário", "dia da semana, mês, feriado", "Os ciclos."),
            ("<code>TimeSeriesSplit</code>", "validação", "Treina no passado, valida no período seguinte, avança."),
        ]),
        cod("Baseline sazonal × média", "Compare dois baselines nas últimas 14 observações: “igual a 7 dias atrás” e “média dos 7 dias anteriores”. Guarde os erros absolutos médios (MAE) e descubra o melhor.",
            '''
import numpy as np

dias = np.arange(70)
vendas = 100 + 30 * (dias % 7 >= 5) + np.random.default_rng(0).normal(0, 3, 70)

mae_sazonal = None
mae_media = None
print(mae_sazonal, mae_media)
''',
            [("Calcula os dois", "assert mae_sazonal is not None and mae_media is not None"), ("Sazonal vence", "assert mae_sazonal < mae_media, f'sazonal={mae_sazonal:.2f}, media={mae_media:.2f}'"),
             ("Valores coerentes", "import numpy as np\nesp = np.mean(np.abs(vendas[56:] - vendas[49:63]))\nassert abs(mae_sazonal - esp) < 1e-9")],
            '''
import numpy as np

dias = np.arange(70)
vendas = 100 + 30 * (dias % 7 >= 5) + np.random.default_rng(0).normal(0, 3, 70)

alvo = vendas[56:]
prev_sazonal = vendas[49:63]
prev_media = np.array([vendas[t - 7:t].mean() for t in range(56, 70)])

mae_sazonal = np.mean(np.abs(alvo - prev_sazonal))
mae_media = np.mean(np.abs(alvo - prev_media))
print(mae_sazonal, mae_media)
''', ["Alvo: <code>vendas[56:]</code>; sazonal: <code>vendas[49:63]</code>.", "Média: para cada t, <code>vendas[t-7:t].mean()</code>."]),
        erros([("Embaralhar na validação.", "O modelo vê o futuro. Use <code>TimeSeriesSplit</code>."), ("Janela que inclui o próprio dia.", "Vazamento: aplique <code>shift(1)</code> antes do <code>rolling</code>."), ("Avaliar só um período.", "Valide em várias janelas: o desempenho muda com a estação.")]),
        ponte("Previsão e modelos de fundação", "<p>Já existem “LLMs de séries temporais” (modelos pré-treinados em milhões de séries, como Chronos e TimesFM) que preveem sem treino específico. Mesmo assim, a avaliação continua a mesma desta aula: baseline ingênuo e validação avançando no tempo.</p>"),
        quiz([
            ("O que é um lag de 7 dias?", ["A média da semana.", "O valor de 7 dias atrás como atributo.", "Um atraso no treino."], 1, "<code>shift(7)</code>."),
            ("Por que comparar com um baseline ingênuo?", ["É obrigatório por lei.", "Para saber se o modelo complexo realmente ajuda.", "Para treinar mais rápido."], 1, "É a régua."),
            ("Qual validação usar?", ["KFold embaralhado.", "TimeSeriesSplit.", "Nenhuma."], 1, "Respeita o tempo."),
        ]),
    ],
    ["Transforme o tempo em atributos: lags, janelas e calendário.", "Valide avançando no tempo.", "Sempre compare com um baseline ingênuo."],
    "Importância de atributos.",
    livro=("MLCC:", "Google ML Crash Course, módulo sobre dados numéricos", "Como o curso recomenda transformar atributos de tempo?"))

AULAS["Importância de atributos"] = aula(
    25,
    "“Quais fatores mais pesam na previsão?” É a pergunta que todo gestor faz. A importância por permutação responde com um experimento simples: embaralhe uma coluna e veja o quanto o modelo piora.",
    ["calcular importância por permutação;", "conhecer as limitações da importância das árvores;", "interpretar importâncias com cuidado."],
    ["Random Forest e métricas."],
    [
        chute("Ao embaralhar a coluna “renda”, a acurácia caiu de 85% para 84%. Ao embaralhar “histórico de pagamento”, caiu para 62%. Qual importa mais?", ["Renda.", "Histórico de pagamento.", "As duas igualmente."], 1,
              ["A queda foi pequena.", "Isso! Destruir a informação dessa coluna derrubou o modelo.", "As quedas foram muito diferentes."],
              "Importância = quanto o modelo depende daquela coluna."),
        concreto("Tirar uma peça do motor", "<p>Para saber o quanto uma peça importa, você a desliga e vê se o carro ainda anda. Embaralhar uma coluna é “desligar” a informação dela sem mudar o resto.</p>"),
        nota("Formas de medir", [
            ("Por permutação", "embaralhar e medir a queda", "Funciona com qualquer modelo; use dados de validação."),
            ("Impureza das árvores", "<code>feature_importances_</code>", "Rápida, mas favorece colunas com muitos valores distintos."),
            ("Coeficientes", "modelos lineares", "Só comparáveis com atributos padronizados."),
        ]),
        cod("Permutação do zero", "Implemente a importância por permutação: para cada coluna, embaralhe-a e meça a queda de acurácia do modelo <code>prever</code>.",
            '''
import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(size=(500, 3))
y = (X[:, 0] + 0.3 * X[:, 1] > 0).astype(int)

def prever(X):
    return (X[:, 0] + 0.3 * X[:, 1] > 0).astype(int)

def importancias(X, y):
    base = (prever(X) == y).mean()
    return [0.0] * X.shape[1]

print(np.round(importancias(X, y), 3))
''',
            [("Coluna 0 é a mais importante", "imp = importancias(X, y)\nassert imp[0] > imp[1] > imp[2], f'imp = {imp}'"), ("Coluna 2 não importa", "assert abs(importancias(X, y)[2]) < 1e-9")],
            '''
import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(size=(500, 3))
y = (X[:, 0] + 0.3 * X[:, 1] > 0).astype(int)

def prever(X):
    return (X[:, 0] + 0.3 * X[:, 1] > 0).astype(int)

def importancias(X, y):
    base = (prever(X) == y).mean()
    r = np.random.default_rng(1)
    imp = []
    for j in range(X.shape[1]):
        Xp = X.copy()
        Xp[:, j] = r.permutation(Xp[:, j])
        imp.append(base - (prever(Xp) == y).mean())
    return imp

print(np.round(importancias(X, y), 3))
''', ["Copie X, embaralhe a coluna j com <code>permutation</code> e meça a acurácia.", "Importância = base − nova acurácia."]),
        erros([("Ler importância como causa.", "Mostra de que o modelo depende, não o que causa o resultado."), ("Colunas correlacionadas.", "Embaralhar uma não derruba o modelo porque a gêmea compensa: as duas parecem pouco importantes."), ("Medir no treino.", "Use a validação para ver o que generaliza.")]),
        ponte("Explicar modelos", "<p>Importância global diz o que pesa em média. Para explicar <b>uma</b> previsão (por que este cliente foi recusado?), vem a próxima aula: SHAP. Para LLMs, a pergunta “por que respondeu isso?” é ainda mais difícil, e é um campo de pesquisa inteiro (interpretabilidade).</p>"),
        quiz([
            ("Como funciona a importância por permutação?", ["Remove linhas.", "Embaralha uma coluna e mede a piora do modelo.", "Conta valores únicos."], 1, "Desliga a informação."),
            ("Por que cuidado com a importância das árvores?", ["É sempre zero.", "Favorece colunas com muitos valores distintos.", "Só funciona com texto."], 1, "Viés conhecido."),
            ("Alta importância significa:", ["Que a coluna causa o alvo.", "Que o modelo depende dela.", "Que ela deve ser removida."], 1, "Dependência, não causa."),
        ]),
    ],
    ["Importância por permutação funciona com qualquer modelo.", "Meça na validação.", "Dependência não é causalidade; cuidado com colunas correlacionadas."],
    "SHAP e LIME: explicar cada previsão.",
    livro=("ISLP", "Capítulo 8, seção 8.2, parte sobre importância de variáveis", "Como o livro mede a importância em bagging?"))

AULAS["SHAP e LIME"] = aula(
    30,
    "“Seu crédito foi negado.” Por quê? Leis de proteção de dados dão às pessoas o direito de entender decisões automatizadas. SHAP e LIME explicam uma previsão específica, mostrando quanto cada atributo empurrou o resultado para cima ou para baixo.",
    ["entender explicações locais;", "ler valores SHAP como contribuições que somam a previsão;", "saber as diferenças entre SHAP e LIME."],
    ["Importância de atributos."],
    [
        chute("Os valores SHAP de uma previsão são: base 0,30; renda +0,25; dívidas −0,10; idade +0,05. Qual a previsão final?", ["0,30", "0,50", "0,70"], 1,
              ["A base é só o ponto de partida.", "Isso! SHAP é aditivo: 0,30 + 0,25 − 0,10 + 0,05 = 0,50.", "Some os sinais com cuidado."],
              "Previsão = valor médio + soma das contribuições."),
        concreto("Dividir a conta do jantar", "<p>Quanto cada pessoa deve pagar de uma conta compartilhada, considerando o que cada um consumiu? Os valores de Shapley vêm da teoria dos jogos e fazem essa divisão de forma justa. SHAP divide a “conta” da previsão entre os atributos.</p>"),
        nota("As duas ferramentas", [
            ("SHAP", "valores de Shapley", "Contribuições que somam exatamente a previsão menos a média. Consistente; rápido para árvores (TreeSHAP)."),
            ("LIME", "modelo local", "Ajusta um modelo simples perto do exemplo, perturbando os dados. Flexível, menos estável."),
            ("Gráfico waterfall", "uma previsão", "Do valor base até a previsão, atributo por atributo."),
            ("Gráfico beeswarm", "visão geral", "As contribuições de todos os exemplos."),
        ]),
        cod("Shapley exato para 2 atributos", "Para um modelo com 2 atributos, o valor de Shapley de A é a média da sua contribuição marginal nas duas ordens possíveis. Complete e confira que as contribuições somam f(A,B) − f(nada).",
            '''
# f(conjunto de atributos presentes) -> previsão
f = {(): 0.30, ("A",): 0.60, ("B",): 0.25, ("A", "B"): 0.50}

shap_A = None
shap_B = None
print(shap_A, shap_B)
''',
            [("shap_A", "assert abs(shap_A - 0.275) < 1e-9, f'shap_A = {shap_A}'"), ("shap_B", "assert abs(shap_B - (-0.075)) < 1e-9, f'shap_B = {shap_B}'"), ("Somam o total", "assert abs(shap_A + shap_B - (f[('A', 'B')] - f[()])) < 1e-9")],
            '''
f = {(): 0.30, ("A",): 0.60, ("B",): 0.25, ("A", "B"): 0.50}

# ordem A depois B e ordem B depois A
shap_A = ((f[("A",)] - f[()]) + (f[("A", "B")] - f[("B",)])) / 2
shap_B = ((f[("B",)] - f[()]) + (f[("A", "B")] - f[("A",)])) / 2
print(shap_A, shap_B)
''', ["Contribuição de A entrando primeiro: f(A) − f(). Entrando depois de B: f(A,B) − f(B).", "Média das duas."]),
        lab("SHAP de verdade", '''
import shap, xgboost
from sklearn.datasets import fetch_california_housing

X, y = fetch_california_housing(return_X_y=True, as_frame=True)
modelo = xgboost.XGBRegressor(n_estimators=200).fit(X, y)
exp = shap.TreeExplainer(modelo)(X.iloc[:500])
shap.plots.waterfall(exp[0])
shap.plots.beeswarm(exp)
''', corpo="<p>Rode no Colab (<code>pip install shap</code>):</p>", exps=["No waterfall, qual atributo mais aumentou o preço da primeira casa?"]),
        erros([("Explicação como causa.", "SHAP explica o modelo, não o mundo."), ("Atributos correlacionados.", "O crédito se divide entre eles de forma às vezes estranha."), ("Mostrar SHAP bruto a quem não é técnico.", "Traduza: “a renda aumentou sua chance em 25 pontos”.")]),
        ponte("Explicar LLMs", "<p>Para LLMs, técnicas parecidas mostram quais palavras do prompt mais influenciaram a resposta. Em sistemas com RAG, a explicação mais útil costuma ser mais simples: mostrar a fonte de onde a resposta veio.</p>"),
        quiz([
            ("SHAP é aditivo. Isso significa:", ["As contribuições somam a previsão menos a média.", "Só funciona com soma.", "É sempre positivo."], 0, "Explicação exata."),
            ("Qual a diferença entre explicação global e local?", ["Nenhuma.", "Global vale para o modelo todo; local, para uma previsão.", "Local é mais rápida."], 1, "SHAP faz as duas."),
            ("De onde vêm os valores de Shapley?", ["Da estatística bayesiana.", "Da teoria dos jogos.", "Das redes neurais."], 1, "Divisão justa de um ganho."),
        ]),
    ],
    ["Explicações locais dizem quanto cada atributo pesou numa previsão.", "SHAP é aditivo e baseado em teoria dos jogos.", "Explicação do modelo não é causalidade."],
    "Viés e ética em ML.",
    livro=("ISLP", "Capítulo 1, introdução e motivação", "Que exemplos o livro dá de uso de modelos para decisões?"))

AULAS["Viés e ética em ML"] = aula(
    30,
    "Um modelo de crédito treinado com decisões do passado aprende os preconceitos do passado. Um reconhecedor facial que viu poucos rostos negros erra mais com eles. Modelos não são neutros: refletem os dados e as escolhas de quem os constrói.",
    ["identificar fontes de viés nos dados e no processo;", "medir diferenças de desempenho entre grupos;", "conhecer práticas de mitigação e de transparência."],
    ["Métricas e importância de atributos."],
    [
        chute("Você removeu as colunas “raça” e “gênero” do modelo de crédito. O viés acabou?", ["Sim.", "Não necessariamente: outras colunas (CEP, nome, escola) podem carregar a mesma informação.", "Sim, se a acurácia for alta."], 1,
              ["Remover a coluna não remove a correlação.", "Isso! São as variáveis “procuradoras” (proxies). É preciso medir os resultados por grupo.", "Acurácia alta pode esconder erros concentrados em um grupo."],
              "Medir é obrigatório: compare métricas entre grupos."),
        concreto("O espelho que amplifica", "<p>Um modelo é um espelho dos dados: se o passado foi injusto, o reflexo é injusto. Pior: aplicado em escala, ele amplifica, porque decide por milhares de pessoas ao mesmo tempo, sem que ninguém perceba o padrão.</p>"),
        nota("Fontes de viés", [
            ("Amostragem", "quem está nos dados", "Grupos sub-representados recebem previsões piores."),
            ("Rótulos históricos", "decisões do passado", "O modelo copia decisões humanas enviesadas."),
            ("Proxies", "variáveis substitutas", "CEP pode codificar raça e renda."),
            ("Métrica agregada", "a média esconde", "90% de acerto geral, 70% num grupo."),
            ("Paridade de oportunidades", "uma métrica de justiça", "Recall igual entre grupos."),
        ]),
        cod("Auditoria por grupo", "Calcule o <b>recall</b> do modelo separadamente para cada grupo e a diferença entre o maior e o menor.",
            '''
import pandas as pd

df = pd.DataFrame({
    "grupo":    ["A", "A", "A", "A", "B", "B", "B", "B"],
    "real":     [1, 1, 1, 0, 1, 1, 1, 0],
    "previsto": [1, 1, 1, 0, 1, 0, 0, 0],
})

recall_por_grupo = None
diferenca = None
print(recall_por_grupo, diferenca)
''',
            [("Recall por grupo", "assert {k: round(v, 3) for k, v in dict(recall_por_grupo).items()} == {'A': 1.0, 'B': 0.333}, f'{dict(recall_por_grupo)}'"), ("Diferença", "assert abs(diferenca - 2 / 3) < 1e-9")],
            '''
import pandas as pd

df = pd.DataFrame({
    "grupo":    ["A", "A", "A", "A", "B", "B", "B", "B"],
    "real":     [1, 1, 1, 0, 1, 1, 1, 0],
    "previsto": [1, 1, 1, 0, 1, 0, 0, 0],
})

positivos = df[df["real"] == 1]
recall_por_grupo = positivos.groupby("grupo")["previsto"].mean()
diferenca = recall_por_grupo.max() - recall_por_grupo.min()
print(recall_por_grupo, diferenca)
''', ["Recall = fração de positivos reais que foram previstos como positivos.", "Filtre os positivos e faça <code>groupby(\"grupo\")[\"previsto\"].mean()</code>."]),
        erros([("“O algoritmo é matemático, então é neutro.”", "A matemática é neutra; os dados e as escolhas, não."), ("Medir só o desempenho geral.", "Sempre separe por grupos relevantes."), ("Tratar ética como etapa final.", "Começa na escolha do problema e dos dados.")]),
        ponte("Viés em LLMs", "<p>LLMs aprendem estereótipos presentes na internet: associar profissões a gêneros, por exemplo. Avaliações de viés, filtros de dados e ajustes com feedback humano tentam reduzir isso, e regulações como o AI Act europeu já exigem documentação e testes para sistemas de alto risco.</p>"),
        quiz([
            ("Remover a coluna sensível elimina o viés?", ["Sim.", "Não necessariamente, por causa de proxies.", "Só em árvores."], 1, "Outras colunas carregam a informação."),
            ("Como detectar viés num modelo?", ["Olhando só a acurácia geral.", "Comparando métricas entre grupos.", "Aumentando os dados."], 1, "Auditoria por grupo."),
            ("Rótulos históricos podem trazer viés porque:", ["São antigos.", "Refletem decisões humanas do passado, que podem ser injustas.", "Têm erros de digitação."], 1, "O modelo copia o passado."),
        ]),
    ],
    ["Viés vem dos dados, dos rótulos, das proxies e das métricas.", "Audite métricas por grupo.", "Ética começa na escolha do problema."],
    "Sistemas de recomendação.",
    livro=("MLCC:", "Google ML Crash Course, “Fairness”", "Que tipos de viés o curso descreve?"))

AULAS["Sistemas de recomendação"] = aula(
    35,
    "“Quem comprou isto também comprou...”, a próxima série, a próxima música. Sistemas de recomendação estão por trás de boa parte do que você consome na internet. A ideia central é simples: usuários parecidos gostam de coisas parecidas.",
    ["entender filtragem colaborativa e baseada em conteúdo;", "calcular similaridade de cosseno;", "conhecer a ideia de fatoração de matrizes."],
    ["Produto escalar (Matemática), NumPy e KNN."],
    [
        chute("Um usuário novo entra no serviço sem nenhum histórico. Como recomendar?", ["Filtragem colaborativa pura.", "Itens populares ou perguntas iniciais de preferência.", "Não dá."], 1,
              ["Sem histórico, não há vizinhos.", "Isso! É o problema do “início frio”: comece pelo popular ou pergunte gostos.", "Dá, com estratégias simples."],
              "Início frio é o calcanhar de Aquiles da filtragem colaborativa."),
        concreto("O amigo com gosto parecido", "<p>Se um amigo gosta dos mesmos filmes que você, a próxima indicação dele provavelmente vai te agradar. A filtragem colaborativa automatiza isso: acha seus “amigos de gosto” entre milhões de usuários.</p>"),
        nota("As abordagens", [
            ("Baseada em conteúdo", "itens parecidos", "Recomenda pelo que o item é: gênero, autor, descrição."),
            ("Colaborativa", "usuários parecidos", "Usa só as avaliações. Descobre afinidades inesperadas."),
            (r"$\cos(u, v) = \frac{u \cdot v}{\|u\| \|v\|}$", "similaridade de cosseno", "1 = mesma direção de gosto; 0 = nada em comum."),
            ("Fatoração de matrizes", "embeddings de usuários e itens", "Avaliação ≈ produto escalar do vetor do usuário com o do item."),
        ], rot="Agora sim, as ideias"),
        cod("Recomendação por vizinhos", "Ache o usuário mais parecido com <code>alvo</code> pela similaridade de cosseno e recomende o item que ele avaliou bem (nota ≥ 4) e o alvo ainda não viu (nota 0).",
            '''
import numpy as np

# linhas = usuários, colunas = filmes; 0 = não viu
notas = np.array([
    [5, 4, 0, 1, 0],   # alvo
    [5, 5, 4, 1, 1],
    [1, 0, 5, 5, 4],
    [4, 5, 5, 2, 0],
], dtype=float)
alvo = 0

def cosseno(a, b):
    return 0.0

vizinho = None
recomendacao = None
print(vizinho, recomendacao)
''',
            [("Cosseno correto", "import numpy as np\nassert abs(cosseno(np.array([1.0, 0]), np.array([1.0, 1])) - 0.7071) < 1e-3"),
             ("Vizinho mais parecido", "assert vizinho in (1, 3), f'vizinho = {vizinho}'"), ("Recomenda o filme 2", "assert recomendacao == 2, f'recomendacao = {recomendacao}'")],
            '''
import numpy as np

notas = np.array([
    [5, 4, 0, 1, 0],
    [5, 5, 4, 1, 1],
    [1, 0, 5, 5, 4],
    [4, 5, 5, 2, 0],
], dtype=float)
alvo = 0

def cosseno(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

sims = [cosseno(notas[alvo], notas[u]) if u != alvo else -1 for u in range(len(notas))]
vizinho = int(np.argmax(sims))
candidatos = [i for i in range(notas.shape[1]) if notas[alvo, i] == 0 and notas[vizinho, i] >= 4]
recomendacao = candidatos[0] if candidatos else None
print(vizinho, recomendacao)
''', ["Cosseno: <code>a @ b / (norm(a) * norm(b))</code>.", "Ignore o próprio alvo; depois procure itens com 0 no alvo e ≥ 4 no vizinho."]),
        erros([("Recomendar só o que já é popular.", "O sistema vira um eco: os mesmos itens para todos. Misture diversidade."), ("Avaliar só com acurácia de nota.", "O que importa é se a pessoa clicou, assistiu, comprou: métricas de ranking."), ("Ignorar o início frio.", "Tenha um plano para usuários e itens novos.")]),
        ponte("Recomendação e embeddings", "<p>A fatoração de matrizes representa usuários e itens como vetores: é a ideia de embeddings, anos antes dos LLMs. Hoje, sistemas modernos combinam embeddings de texto e imagem dos itens com o histórico, e LLMs começam a conversar com o usuário para entender o que ele quer.</p>"),
        quiz([
            ("Filtragem colaborativa usa principalmente:", ["A descrição dos itens.", "As avaliações de usuários parecidos.", "O preço."], 1, "Gostos em comum."),
            ("O que é o problema do início frio?", ["Servidores lentos.", "Falta de histórico de usuários ou itens novos.", "Dados duplicados."], 1, "Sem vizinhos."),
            ("Similaridade de cosseno 1 significa:", ["Gostos opostos.", "Mesma direção de preferência.", "Nenhuma relação."], 1, "Vetores alinhados."),
        ]),
    ],
    ["Conteúdo recomenda itens parecidos; colaborativa, o que usuários parecidos gostam.", "Similaridade de cosseno compara vetores de gosto.", "Fatoração de matrizes cria embeddings de usuários e itens."],
    "Fase 4: Deep Learning, começando pelo neurônio.",
    livro=("MLCC:", "Google ML Crash Course, introdução aos embeddings", "Como o curso relaciona embeddings e recomendações?"))
