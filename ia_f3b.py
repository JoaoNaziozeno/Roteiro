# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 3 (parte B): avaliação, pipelines e mais algoritmos."""
from lesson_factory import *

AULAS = {}

AULAS["Métricas: acurácia, precisão, recall, F1"] = aula(
    35,
    "Um teste de doença rara que diz “saudável” para todo mundo acerta 99% das vezes e não serve para nada. A acurácia engana quando as classes são desiguais. Precisão e recall contam a história que importa: quantos alarmes eram reais e quantos casos reais foram pegos.",
    ["calcular acurácia, precisão, recall e F1;", "escolher a métrica certa para o custo de cada erro;", "entender o compromisso entre precisão e recall."],
    ["Regressão logística e máscaras booleanas."],
    [
        chute("Um detector de fraudes marcou 10 transações; 8 eram fraudes de verdade. Havia 40 fraudes no total. Qual o recall?", ["80%", "20%", "8%"], 1,
              ["80% é a <b>precisão</b>: dos alarmes, quantos eram reais.", "Isso! Das 40 fraudes reais, ele pegou 8: recall de 20%.", "8 é a contagem de acertos, não uma taxa."],
              "Precisão olha para os alarmes; recall olha para os casos reais."),
        concreto("A rede de pesca", "<p>Uma rede fina pega quase todos os peixes (recall alto), mas também muito lixo (precisão baixa). Uma rede seletiva traz só peixe bom (precisão alta), mas deixa muitos escaparem (recall baixo). Você escolhe a rede conforme o que custa mais caro.</p>"),
        nota("As quatro contagens e as métricas", [
            ("VP, FP, VN, FN", "verdadeiros/falsos positivos e negativos", "VP: alarme certo. FP: alarme falso. FN: caso real que escapou."),
            (r"$\text{precisão} = \frac{VP}{VP + FP}$", "precisão", "Dos que eu marquei, quantos eram mesmo."),
            (r"$\text{recall} = \frac{VP}{VP + FN}$", "revocação", "Dos que eram, quantos eu marquei."),
            (r"$F1 = 2\frac{P \cdot R}{P + R}$", "F1", "Média harmônica: só é alta se as duas forem."),
        ], rot="Agora sim, as fórmulas"),
        cod("Métricas do zero", "Complete a função que devolve <code>(precisao, recall, f1)</code> a partir dos rótulos reais e previstos (0/1). Trate divisões por zero devolvendo 0.",
            '''
def metricas(real, previsto):
    return 0.0, 0.0, 0.0

print(metricas([1, 0, 1, 1, 0, 1], [1, 1, 1, 0, 0, 0]))
''',
            [("Exemplo", "p, r, f = metricas([1, 0, 1, 1, 0, 1], [1, 1, 1, 0, 0, 0])\nassert (round(p, 3), round(r, 3), round(f, 3)) == (0.667, 0.5, 0.571), f'{p}, {r}, {f}'"),
             ("Sem previsões positivas", "assert metricas([1, 1], [0, 0]) == (0.0, 0.0, 0.0)")],
            '''
def metricas(real, previsto):
    vp = sum(1 for r, p in zip(real, previsto) if r == 1 and p == 1)
    fp = sum(1 for r, p in zip(real, previsto) if r == 0 and p == 1)
    fn = sum(1 for r, p in zip(real, previsto) if r == 1 and p == 0)
    precisao = vp / (vp + fp) if vp + fp else 0.0
    recall = vp / (vp + fn) if vp + fn else 0.0
    f1 = 2 * precisao * recall / (precisao + recall) if precisao + recall else 0.0
    return precisao, recall, f1

print(metricas([1, 0, 1, 1, 0, 1], [1, 1, 1, 0, 0, 0]))
''', ["Conte VP, FP e FN com <code>zip</code>.", "Use <code>x / y if y else 0.0</code>."]),
        tabela("Qual métrica priorizar", ["Situação", "Erro mais caro", "Priorize"], [
            ["Triagem de câncer", "deixar um doente passar (FN)", "recall"],
            ["Filtro de spam", "esconder um e-mail importante (FP)", "precisão"],
            ["Detecção de fraude com revisão humana", "os dois, equilibrados", "F1"],
            ["Classes equilibradas e erros de custo parecido", "—", "acurácia"],
        ]),
        erros([("Reportar só acurácia com classes desbalanceadas.", "Mostre precisão, recall e a matriz de confusão."), ("Otimizar precisão e recall ao mesmo tempo sem perceber o trade-off.", "Subir um quase sempre baixa o outro: o limiar decide."), ("F1 para problemas multiclasse sem dizer a média.", "Diga se é macro (média das classes) ou ponderada.")]),
        ponte("Métricas de LLMs", "<p>Em RAG, “recall” é: dos trechos relevantes, quantos a busca trouxe? “Precisão”: dos trazidos, quantos eram relevantes? As mesmas fórmulas avaliam buscadores, detectores de conteúdo tóxico e classificadores feitos com LLMs.</p>"),
        quiz([
            ("Recall mede:", ["Dos alarmes, quantos eram reais.", "Dos casos reais, quantos foram detectados.", "O total de acertos."], 1, "VP / (VP + FN)."),
            ("Num filtro de spam, qual erro é pior?", ["Spam na caixa de entrada.", "E-mail importante indo para o spam.", "Nenhum."], 1, "Priorize precisão."),
            ("Quando o F1 é alto?", ["Quando a precisão é alta.", "Quando precisão e recall são altos.", "Quando a acurácia é alta."], 1, "Média harmônica."),
        ]),
    ],
    ["Precisão: acerto dos alarmes. Recall: casos reais encontrados.", "F1 equilibra as duas.", "A métrica certa depende do custo de cada tipo de erro."],
    "Matriz de confusão e curva ROC.",
    livro=("MLCC:", "Google ML Crash Course, “Classification: accuracy, recall, precision”", "Que exemplo o curso usa para o trade-off precisão × recall?"))

AULAS["Matriz de confusão e curva ROC"] = aula(
    30,
    "Uma única nota esconde onde o modelo erra. A matriz de confusão mostra cada tipo de acerto e de erro numa tabela; a curva ROC mostra o modelo em todos os limiares de uma vez, e a área sob ela (AUC) resume tudo num número que não depende do limiar.",
    ["montar e ler uma matriz de confusão;", "entender taxa de verdadeiros e falsos positivos;", "interpretar a curva ROC e a AUC."],
    ["Métricas de classificação."],
    [
        chute("Um modelo tem AUC de 0,5. O que isso significa?", ["É ótimo.", "É tão bom quanto jogar uma moeda.", "Acerta metade das fraudes."], 1,
              ["0,5 é o piso.", "Isso! AUC 0,5 é a diagonal: o modelo não separa as classes.", "AUC não é taxa de acerto."],
              "AUC 1 = separação perfeita; 0,5 = acaso."),
        concreto("O detector de metais", "<p>Aumentando a sensibilidade, o detector apita para toda moeda (pega todos os metais, mas com muito alarme falso). Diminuindo, só apita para objetos grandes. A curva ROC desenha o detector em <b>todas</b> as sensibilidades.</p>"),
        nota("Ler a matriz e a curva", [
            ("Linhas = real, colunas = previsto", "matriz", "A diagonal são os acertos; fora dela, os erros."),
            (r"$TPR = \frac{VP}{VP+FN}$", "taxa de verdadeiros positivos", "É o recall: eixo y da ROC."),
            (r"$FPR = \frac{FP}{FP+VN}$", "taxa de falsos positivos", "Eixo x da ROC."),
            ("AUC", "área sob a curva", "Probabilidade de um positivo receber nota maior que um negativo."),
        ], rot="Agora sim, as definições"),
        cod("AUC pela definição", "A AUC é a fração de pares (positivo, negativo) em que o positivo recebeu nota maior (empates contam meio). Implemente com dois laços ou com broadcasting.",
            '''
import numpy as np

def auc(real, notas):
    return 0.0

real = np.array([1, 1, 0, 0, 1, 0])
notas = np.array([0.9, 0.7, 0.6, 0.2, 0.4, 0.4])
print(auc(real, notas))
''',
            [("Exemplo", "import numpy as np\nassert abs(auc(np.array([1, 1, 0, 0, 1, 0]), np.array([0.9, 0.7, 0.6, 0.2, 0.4, 0.4])) - 7.5 / 9) < 1e-9"),
             ("Separação perfeita = 1", "import numpy as np\nassert auc(np.array([0, 0, 1, 1]), np.array([0.1, 0.2, 0.8, 0.9])) == 1.0"),
             ("Ao contrário = 0", "import numpy as np\nassert auc(np.array([1, 0]), np.array([0.1, 0.9])) == 0.0")],
            '''
import numpy as np

def auc(real, notas):
    pos, neg = notas[real == 1], notas[real == 0]
    maior = (pos[:, None] > neg[None, :]).sum()
    empate = (pos[:, None] == neg[None, :]).sum()
    return (maior + 0.5 * empate) / (len(pos) * len(neg))

real = np.array([1, 1, 0, 0, 1, 0])
notas = np.array([0.9, 0.7, 0.6, 0.2, 0.4, 0.4])
print(auc(real, notas))
''', ["Separe as notas dos positivos e dos negativos.", "<code>pos[:, None] &gt; neg[None, :]</code> compara todos os pares."]),
        lab("Matriz e ROC no scikit-learn", '''
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_auc_score, RocCurveDisplay
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0, stratify=y)
m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(Xtr, ytr)
print(confusion_matrix(yte, m.predict(Xte)))
print("AUC:", roc_auc_score(yte, m.predict_proba(Xte)[:, 1]))
RocCurveDisplay.from_estimator(m, Xte, yte)
''', corpo="<p>Rode no Colab:</p>", exps=["Onde estão os falsos negativos na matriz?"]),
        erros([("Calcular AUC com as classes previstas (0/1).", "A AUC precisa das <b>notas</b> (probabilidades)."), ("ROC com classes muito desbalanceadas.", "Prefira também a curva precisão-recall, mais sensível ao caso raro."), ("Confundir linhas e colunas da matriz.", "No scikit-learn, linhas são o real e colunas, o previsto.")]),
        ponte("Escolher o limiar", "<p>O modelo dá notas; a decisão é sua. Com a curva ROC em mãos, você escolhe o limiar que respeita um limite de alarmes falsos aceitável pelo negócio. É o mesmo raciocínio para decidir quando um LLM deve recusar ou pedir confirmação.</p>"),
        quiz([
            ("Na matriz de confusão, a diagonal mostra:", ["Os erros.", "Os acertos.", "As probabilidades."], 1, "Real igual ao previsto."),
            ("O eixo x da curva ROC é:", ["Recall.", "Taxa de falsos positivos.", "Precisão."], 1, "FP / (FP + VN)."),
            ("Por que a AUC é útil?", ["Não depende de um limiar específico.", "É sempre maior que a acurácia.", "Mede a velocidade."], 0, "Resume todos os limiares."),
        ]),
    ],
    ["A matriz de confusão separa cada tipo de acerto e erro.", "A ROC mostra TPR × FPR em todos os limiares.", "AUC: 1 é perfeito; 0,5 é acaso."],
    "Scikit-learn e pipelines.",
    livro=("MLCC:", "Google ML Crash Course, “ROC and AUC”", "Como o curso interpreta a AUC em termos de ordenação?"))

AULAS["Scikit-learn e pipelines"] = aula(
    35,
    "Normalizar, codificar, imputar e treinar: quatro passos que precisam acontecer na mesma ordem, com os mesmos parâmetros, no treino e em produção. O pipeline amarra tudo num objeto só, e é a defesa mais simples contra vazamento de dados.",
    ["entender a interface <code>fit</code> / <code>transform</code> / <code>predict</code>;", "montar um <code>Pipeline</code> com <code>ColumnTransformer</code>;", "salvar e carregar o modelo inteiro."],
    ["Encoding, normalização e validação cruzada."],
    [
        chute("Você padronizou o conjunto inteiro antes de separar treino e teste. Qual o problema?", ["Nenhum.", "A média e o desvio usaram o teste: houve vazamento.", "O modelo fica lento."], 1,
              ["É um problema sutil e comum.", "Isso! Parâmetros do pré-processamento devem vir só do treino. Num pipeline isso acontece sozinho.", "Velocidade não muda."],
              "<code>fit</code> só no treino; <code>transform</code> no treino e no teste."),
        concreto("A linha de montagem", "<p>Numa fábrica, cada peça passa pelas mesmas estações na mesma ordem. Ninguém pula uma estação, nem muda a ordem amanhã. O pipeline é a linha de montagem dos dados até a previsão.</p>"),
        nota("A interface do scikit-learn", [
            ("<code>fit(X, y)</code>", "aprender", "Transformadores aprendem parâmetros (média, categorias); modelos aprendem pesos."),
            ("<code>transform(X)</code>", "aplicar", "Usa o que foi aprendido no <code>fit</code>."),
            ("<code>Pipeline([(\"esc\", StandardScaler()), (\"mod\", LogisticRegression())])</code>", "pipeline", "Encadeia; o último passo é o modelo."),
            ("<code>ColumnTransformer([...])</code>", "por coluna", "Numéricas por um caminho, categóricas por outro."),
            ("<code>joblib.dump(pipe, \"modelo.joblib\")</code>", "salvar", "Leva o pré-processamento junto."),
        ]),
        cod("Seu próprio transformador", "Implemente <code>Padronizador</code> no estilo do scikit-learn: <code>fit</code> guarda média e desvio do treino; <code>transform</code> aplica. O teste confere que o teste usa a média <b>do treino</b>.",
            '''
import numpy as np

class Padronizador:
    def fit(self, X):
        return self

    def transform(self, X):
        return X

treino = np.array([[1.0], [2.0], [3.0]])
teste = np.array([[5.0]])
p = Padronizador().fit(treino)
print(p.transform(treino).ravel(), p.transform(teste).ravel())
''',
            [("Treino padronizado", "import numpy as np\nr = Padronizador().fit(np.array([[1.0], [2], [3]])).transform(np.array([[1.0], [2], [3]]))\nassert np.allclose(r.ravel(), [-1.2247, 0, 1.2247], atol=1e-3)"),
             ("Teste usa parâmetros do treino", "import numpy as np\np = Padronizador().fit(np.array([[1.0], [2], [3]]))\nassert np.allclose(p.transform(np.array([[5.0]])).ravel(), [3.6742], atol=1e-3)"),
             ("fit devolve self", "import numpy as np\nassert isinstance(Padronizador().fit(np.array([[1.0], [2]])), Padronizador)")],
            '''
import numpy as np

class Padronizador:
    def fit(self, X):
        self.media_ = X.mean(axis=0)
        self.desvio_ = X.std(axis=0)
        return self

    def transform(self, X):
        return (X - self.media_) / self.desvio_

treino = np.array([[1.0], [2.0], [3.0]])
teste = np.array([[5.0]])
p = Padronizador().fit(treino)
print(p.transform(treino).ravel(), p.transform(teste).ravel())
''', ["No <code>fit</code>: <code>self.media_ = X.mean(axis=0)</code> e o desvio.", "No <code>transform</code>, use os atributos guardados."]),
        lab("Pipeline completo com colunas mistas", '''
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.DataFrame({"idade": [25, None, 40, 33], "plano": ["a", "b", "a", "c"], "cancelou": [0, 1, 0, 1]})
num = Pipeline([("imp", SimpleImputer(strategy="median")), ("esc", StandardScaler())])
pre = ColumnTransformer([("num", num, ["idade"]), ("cat", OneHotEncoder(handle_unknown="ignore"), ["plano"])])
pipe = Pipeline([("pre", pre), ("mod", LogisticRegression())]).fit(df[["idade", "plano"]], df["cancelou"])
print(pipe.predict(pd.DataFrame({"idade": [30], "plano": ["z"]})))
''', corpo="<p>Rode no Colab: note o plano “z”, que nunca apareceu no treino.</p>", exps=["Troque o modelo por <code>RandomForestClassifier</code> mudando só a última etapa."]),
        erros([("Pré-processar fora do pipeline.", "Vazamento e inconsistência entre treino e produção."), ("Salvar só o modelo.", "Em produção, faltará o pré-processamento. Salve o pipeline inteiro."), ("Chamar <code>fit_transform</code> no teste.", "No teste, só <code>transform</code>.")]),
        ponte("Pipelines em IA moderna", "<p>Um sistema de RAG também é um pipeline: limpar, dividir em trechos, gerar embeddings, buscar, montar o prompt, chamar o modelo. Mudar uma etapa sem mudar as outras quebra tudo. A disciplina de “uma linha de montagem versionada” vem daqui.</p>"),
        quiz([
            ("Onde o transformador aprende a média?", ["No <code>transform</code>.", "No <code>fit</code>, só com o treino.", "No <code>predict</code>."], 1, "Depois só aplica."),
            ("Para que serve o <code>ColumnTransformer</code>?", ["Aplicar tratamentos diferentes a colunas diferentes.", "Ordenar colunas.", "Remover colunas vazias."], 0, "Numéricas e categóricas."),
            ("O que salvar para produção?", ["Só o modelo.", "O pipeline inteiro.", "Os dados de treino."], 1, "Pré-processamento incluso."),
        ]),
    ],
    ["<code>fit</code> aprende no treino; <code>transform</code> aplica em qualquer dado.", "Pipeline encadeia pré-processamento e modelo.", "Salve e implante o pipeline inteiro."],
    "Ajuste de hiperparâmetros.",
    livro=("PDSH:05.02-introducing-scikit-learn", "Seção 5.2, “Introducing Scikit-Learn”", "Quais são os passos da API de estimadores segundo o livro?"))

AULAS["Ajuste de hiperparâmetros"] = aula(
    30,
    "Profundidade da árvore, número de vizinhos, taxa de aprendizado: são escolhas que o modelo não aprende sozinho. Testá-las com método, sem olhar o teste, é o que separa um bom resultado de um resultado de sorte.",
    ["diferenciar parâmetros de hiperparâmetros;", "usar busca em grade e busca aleatória;", "combinar busca com validação cruzada."],
    ["Validação cruzada e pipelines."],
    [
        chute("Você quer testar 5 valores de 4 hiperparâmetros. Quantas combinações tem a busca em grade?", ["20", "625", "9"], 1,
              ["20 seria se você testasse cada um isoladamente.", "Isso! 5⁴ = 625, e com validação de 5 dobras são 3.125 treinos.", "Não."],
              "A grade explode rápido: daí a busca aleatória."),
        concreto("Afinar o violão", "<p>As cordas (pesos) se ajustam tocando; mas a escolha do tipo de corda e da afinação base (hiperparâmetros) você faz antes, testando e ouvindo. Testar de forma organizada é melhor do que mexer em tudo ao mesmo tempo.</p>"),
        nota("Formas de buscar", [
            ("<code>GridSearchCV(modelo, grade, cv=5)</code>", "grade", "Testa todas as combinações."),
            ("<code>RandomizedSearchCV(modelo, distribuicoes, n_iter=50)</code>", "aleatória", "Sorteia combinações; acha bons valores com muito menos treinos."),
            ("Escala logarítmica", "para taxas", "Teste 0,001, 0,01, 0,1, não 0,01, 0,02, 0,03."),
            ("Optuna", "busca bayesiana", "Aprende com as tentativas anteriores onde procurar."),
        ]),
        cod("Busca em grade na mão", "Teste os graus de polinômio de 1 a 8 com validação simples e guarde em <code>melhor_grau</code> o de menor erro de validação. O teste nunca é usado.",
            '''
import numpy as np

rng = np.random.default_rng(3)
x = rng.uniform(-3, 3, 60)
y = 0.5 * x ** 3 - x + rng.normal(0, 1.5, 60)
xt, yt, xv, yv = x[:40], y[:40], x[40:], y[40:]

resultados = {}
for grau in range(1, 9):
    pass

melhor_grau = None
print(melhor_grau, resultados)
''',
            [("Testa os 8 graus", "assert sorted(resultados) == list(range(1, 9))"), ("Escolhe o menor erro", "assert melhor_grau == min(resultados, key=resultados.get)"), ("Grau razoável (3 a 5)", "assert 3 <= melhor_grau <= 5, f'melhor_grau = {melhor_grau}'")],
            '''
import numpy as np

rng = np.random.default_rng(3)
x = rng.uniform(-3, 3, 60)
y = 0.5 * x ** 3 - x + rng.normal(0, 1.5, 60)
xt, yt, xv, yv = x[:40], y[:40], x[40:], y[40:]

resultados = {}
for grau in range(1, 9):
    coef = np.polyfit(xt, yt, grau)
    resultados[grau] = float(np.mean((np.polyval(coef, xv) - yv) ** 2))

melhor_grau = min(resultados, key=resultados.get)
print(melhor_grau, resultados)
''', ["Para cada grau: <code>np.polyfit</code> no treino e erro na validação."]),
        erros([("Escolher hiperparâmetros pelo teste.", "O teste vira validação e fica otimista."), ("Grade fina em todos os hiperparâmetros.", "Explode o custo. Comece aleatória e larga, depois refine."), ("Ajustar 20 hiperparâmetros com poucos dados.", "Você acaba fazendo overfitting na validação.")]),
        ponte("Hiperparâmetros de redes e LLMs", "<p>Taxa de aprendizado, tamanho do lote, dropout e, nos LLMs, temperatura e top-p de geração: tudo isso é hiperparâmetro. Em deep learning, a taxa de aprendizado é quase sempre o mais importante a buscar primeiro.</p>"),
        quiz([
            ("Qual destes é hiperparâmetro?", ["Os pesos de uma regressão.", "A profundidade máxima de uma árvore.", "Os cortes aprendidos na árvore."], 1, "Escolhido antes do treino."),
            ("Por que a busca aleatória costuma vencer a grade?", ["É determinística.", "Testa mais valores diferentes de cada hiperparâmetro com o mesmo custo.", "Não usa validação."], 1, "Explora melhor o espaço."),
            ("Como testar taxas de aprendizado?", ["Em passos iguais: 0,01, 0,02...", "Em escala logarítmica.", "Um valor só."], 1, "Ordens de grandeza."),
        ]),
    ],
    ["Hiperparâmetros são escolhas antes do treino.", "Grade é exaustiva; aleatória é mais eficiente.", "Sempre com validação cruzada, nunca com o teste."],
    "KNN: classificar pelos vizinhos.",
    livro=("PDSH:05.03-hyperparameters-and-model-validation", "Seção 5.3, “Hyperparameters and Model Validation”", "Como o livro desenha a curva de validação?"))

AULAS["KNN"] = aula(
    25,
    "“Diga-me com quem andas e te direi quem és.” O KNN classifica um ponto novo olhando os k exemplos mais parecidos e fazendo uma votação. Não há treino: o modelo é a própria memória dos dados.",
    ["classificar por votação dos k vizinhos mais próximos;", "entender o papel de k e da escala;", "conhecer o custo de prever com KNN."],
    ["Distâncias (Matemática), broadcasting e normalização."],
    [
        chute("Com k = 1, o KNN acerta 100% no treino. Por quê?", ["Porque é o melhor modelo.", "Porque o vizinho mais próximo de cada ponto de treino é ele mesmo.", "Por sorte."], 1,
              ["100% no treino é um alerta, não uma vitória.", "Isso! k = 1 decora os dados: é overfitting puro.", "Não há sorte nisso."],
              "k pequeno = fronteira nervosa (overfitting); k grande = fronteira lisa demais (underfitting)."),
        concreto("O bairro novo", "<p>Para saber se um bairro é tranquilo, você pergunta aos 5 vizinhos mais próximos da casa. A maioria diz “tranquilo”? Provavelmente é. Isso é KNN com k = 5.</p>"),
        nota("O algoritmo", [
            ("Distância euclidiana", "quem é vizinho", "Raiz da soma dos quadrados das diferenças."),
            ("k", "quantos vizinhos", "Ímpar evita empates na classificação binária."),
            ("Votação / média", "decisão", "Classe mais comum ou média dos valores (regressão)."),
            ("Padronizar", "obrigatório", "Senão a coluna de maior escala decide sozinha quem é vizinho."),
        ]),
        cod("KNN do zero", "Complete <code>knn(X_treino, y_treino, x, k)</code>: calcule as distâncias, pegue os k índices mais próximos e devolva a classe mais votada.",
            '''
import numpy as np

def knn(X_treino, y_treino, x, k=3):
    return 0

X = np.array([[1, 1], [1, 2], [2, 1], [6, 6], [7, 6], [6, 7]], dtype=float)
y = np.array([0, 0, 0, 1, 1, 1])
print(knn(X, y, np.array([1.5, 1.5])), knn(X, y, np.array([6.5, 6.2])))
''',
            [("Classe 0 perto do grupo 0", "import numpy as np\nassert knn(X, y, np.array([1.5, 1.5])) == 0"), ("Classe 1 perto do grupo 1", "import numpy as np\nassert knn(X, y, np.array([6.5, 6.2])) == 1"),
             ("k grande vota com todos", "import numpy as np\nX2 = np.array([[0.0], [1], [10], [11], [12]]); y2 = np.array([0, 0, 1, 1, 1])\nassert knn(X2, y2, np.array([0.5]), k=1) == 0 and knn(X2, y2, np.array([0.5]), k=5) == 1")],
            '''
import numpy as np

def knn(X_treino, y_treino, x, k=3):
    dist = np.sqrt(((X_treino - x) ** 2).sum(axis=1))
    vizinhos = y_treino[np.argsort(dist)[:k]]
    return int(np.bincount(vizinhos).argmax())

X = np.array([[1, 1], [1, 2], [2, 1], [6, 6], [7, 6], [6, 7]], dtype=float)
y = np.array([0, 0, 0, 1, 1, 1])
print(knn(X, y, np.array([1.5, 1.5])), knn(X, y, np.array([6.5, 6.2])))
''', ["Distâncias com broadcasting: <code>((X_treino - x) ** 2).sum(axis=1)</code>.", "<code>np.argsort(dist)[:k]</code> e <code>np.bincount(...).argmax()</code>."]),
        erros([("KNN sem padronizar.", "Renda em reais domina idade em anos."), ("Muitas colunas (dezenas ou centenas).", "Em alta dimensão, todos ficam “longe” de todos: a maldição da dimensionalidade."), ("Usar KNN puro com milhões de exemplos.", "Cada previsão compara com todos. Use índices de busca aproximada.")]),
        ponte("O KNN dos LLMs", "<p>A busca semântica de um RAG é um KNN: dado o embedding da pergunta, encontre os k trechos mais próximos. Bancos vetoriais existem para fazer esse KNN em milhões de vetores em milissegundos, com busca aproximada.</p>"),
        quiz([
            ("O que o KNN aprende no treino?", ["Pesos.", "Nada: ele guarda os dados.", "Cortes de árvore."], 1, "É um modelo “preguiçoso”."),
            ("Aumentar k tende a:", ["Aumentar o overfitting.", "Suavizar a fronteira de decisão.", "Não mudar nada."], 1, "Mais vizinhos, mais média."),
            ("Por que padronizar?", ["Para a distância não ser dominada por uma coluna.", "Para treinar mais rápido.", "Não precisa."], 0, "A distância depende da escala."),
        ]),
    ],
    ["KNN prevê pela votação dos k exemplos mais próximos.", "k controla o equilíbrio entre overfitting e underfitting.", "Padronize; é a mesma ideia da busca vetorial."],
    "Naive Bayes: probabilidade que classifica texto.",
    livro=("PDSH:05.03-hyperparameters-and-model-validation", "Seção 5.3 (exemplo com KNN e validação)", "Como o livro mostra que k=1 decora o treino?"))

AULAS["Naive Bayes"] = aula(
    30,
    "Antes dos LLMs, os filtros de spam funcionavam com uma conta simples: a frequência de cada palavra no spam e nos e-mails normais. O Naive Bayes multiplica essas pistas e decide. Rápido, transparente e ainda imbatível com poucos dados de texto.",
    ["aplicar o teorema de Bayes à classificação;", "entender a suposição “ingênua” de independência;", "usar suavização de Laplace."],
    ["Probabilidade (Matemática) e dicionários."],
    [
        chute("A palavra “grátis” aparece em 30% dos spams e em 2% dos e-mails normais. Um e-mail tem “grátis”. Isso prova que é spam?", ["Sim.", "Não, mas aumenta muito a chance; depende também de quão comum é spam.", "Não muda nada."], 1,
              ["Uma pista não é prova.", "Isso! Bayes combina a pista com a frequência base (a priori) de spam.", "Muda bastante: a pista é 15 vezes mais comum no spam."],
              "Posterior ∝ verossimilhança × priori."),
        concreto("O detetive com pistas", "<p>Pegada de bota: suspeita aumenta. Fio de cabelo ruivo: aumenta mais. O detetive multiplica as pistas como se fossem independentes, mesmo sabendo que não são inteiramente. Por isso o “ingênuo” no nome: a simplificação funciona surpreendentemente bem.</p>"),
        nota("A fórmula", [
            (r"$P(c \mid x) \propto P(c) \prod_i P(x_i \mid c)$", "Bayes ingênuo", "A classe mais provável dado o texto."),
            (r"$P(c)$", "priori", "Quão comum é a classe."),
            (r"$P(x_i \mid c)$", "verossimilhança", "Frequência da palavra na classe."),
            (r"$\frac{n_{w,c}+1}{n_c + |V|}$", "suavização de Laplace", "Evita probabilidade zero para palavras nunca vistas na classe."),
            ("Somar logaritmos", "estabilidade", "Multiplicar muitas probabilidades pequenas dá zero no computador."),
        ], rot="Agora sim, a fórmula"),
        cod("Filtro de spam do zero", "Complete <code>prever</code>: para cada classe, some o log da priori e o log da probabilidade suavizada de cada palavra; devolva a classe de maior soma.",
            '''
import math
from collections import Counter

treino = [("ganhe dinheiro grátis agora", "spam"), ("oferta grátis clique", "spam"),
          ("reunião amanhã cedo", "ok"), ("relatório da reunião", "ok"), ("almoço amanhã", "ok")]

contagens = {"spam": Counter(), "ok": Counter()}
docs = Counter()
for texto, c in treino:
    docs[c] += 1
    contagens[c].update(texto.split())
vocab = set(w for c in contagens for w in contagens[c])

def prever(texto):
    return "ok"

print(prever("dinheiro grátis"), prever("reunião amanhã"))
''',
            [("Detecta spam", "assert prever('dinheiro grátis') == 'spam'"), ("Detecta ok", "assert prever('reunião amanhã') == 'ok'"), ("Palavra desconhecida não quebra", "assert prever('xyz grátis') == 'spam'")],
            '''
import math
from collections import Counter

treino = [("ganhe dinheiro grátis agora", "spam"), ("oferta grátis clique", "spam"),
          ("reunião amanhã cedo", "ok"), ("relatório da reunião", "ok"), ("almoço amanhã", "ok")]

contagens = {"spam": Counter(), "ok": Counter()}
docs = Counter()
for texto, c in treino:
    docs[c] += 1
    contagens[c].update(texto.split())
vocab = set(w for c in contagens for w in contagens[c])

def prever(texto):
    melhor, melhor_c = None, None
    for c in contagens:
        total = sum(contagens[c].values())
        s = math.log(docs[c] / sum(docs.values()))
        for w in texto.split():
            s += math.log((contagens[c][w] + 1) / (total + len(vocab)))
        if melhor is None or s > melhor:
            melhor, melhor_c = s, c
    return melhor_c

print(prever("dinheiro grátis"), prever("reunião amanhã"))
''', ["Priori: <code>math.log(docs[c] / sum(docs.values()))</code>.", "Para cada palavra: <code>math.log((contagens[c][w] + 1) / (total + len(vocab)))</code>."]),
        erros([("Esquecer a suavização.", "Uma palavra nova zera toda a probabilidade da classe."), ("Multiplicar probabilidades em vez de somar logs.", "Com textos longos, o resultado vira 0.0 por limite numérico."), ("Confiar nas probabilidades como calibradas.", "A ordem das classes é boa; os valores costumam ser extremos demais.")]),
        ponte("Bayes e LLMs", "<p>Um LLM também calcula probabilidades de palavras, mas condicionadas a todo o contexto anterior, sem a suposição ingênua. Naive Bayes continua ótimo como baseline rápido: se ele já resolve, você economiza um LLM.</p>"),
        quiz([
            ("Por que “ingênuo”?", ["Porque usa poucos dados.", "Porque supõe que as palavras são independentes dada a classe.", "Porque não usa probabilidades."], 1, "Uma simplificação que funciona."),
            ("Para que serve a suavização de Laplace?", ["Acelerar.", "Evitar probabilidade zero para palavras não vistas.", "Remover palavras comuns."], 1, "Soma 1 nas contagens."),
            ("Por que somar logaritmos?", ["Para evitar que o produto de muitas probabilidades pequenas vire zero.", "Por estética.", "Para ficar exato."], 0, "Estabilidade numérica."),
        ]),
    ],
    ["Naive Bayes combina priori e frequências de palavras.", "Suponha independência, suavize e some logaritmos.", "Rápido, transparente e ótimo baseline para texto."],
    "SVM: a fronteira com a maior margem.",
    livro=("PDSH:05.05-naive-bayes", "Seção 5.5, “In Depth: Naive Bayes Classification”", "Que dataset de texto o livro usa?"))

AULAS["SVM"] = aula(
    30,
    "Entre todas as retas que separam duas classes, qual escolher? A SVM escolhe a que fica o mais longe possível dos pontos mais próximos de cada lado: a fronteira com a maior margem. E, com o truque do kernel, separa até o que não é separável por reta.",
    ["entender margem e vetores de suporte;", "saber o papel do parâmetro C;", "entender o truque do kernel."],
    ["Regressão logística, produto escalar e normalização."],
    [
        chute("Na SVM, quais pontos definem a fronteira?", ["Todos os pontos.", "Só os mais próximos da fronteira (os vetores de suporte).", "Os mais distantes."], 1,
              ["Pontos longe da fronteira não mudam nada.", "Isso! Só os “encostados” na margem sustentam a fronteira, daí o nome.", "Os distantes são irrelevantes."],
              "Mover um ponto longe da margem não altera o modelo."),
        concreto("A estrada mais larga", "<p>Entre duas cidades (as classes), você constrói a estrada mais larga possível sem derrubar nenhuma casa. As casas que encostam no acostamento são os vetores de suporte. Uma estrada larga tolera melhor imprevistos: generaliza melhor.</p>"),
        nota("As ideias", [
            ("Margem", "distância da fronteira aos pontos mais próximos", "A SVM maximiza essa distância."),
            ("C", "rigidez", "C alto: quase nenhum erro no treino, margem estreita. C baixo: margem larga, tolera erros."),
            ("Kernel", "truque", "Mede semelhança como se os dados estivessem num espaço de mais dimensões, onde ficam separáveis."),
            ("RBF", "kernel gaussiano", "O mais usado; <code>gamma</code> controla o alcance de cada ponto."),
        ], rot="Agora sim, as ideias"),
        cod("O truque do kernel na mão", "Pontos em 1D: classe 1 no meio e classe 0 nas pontas; nenhuma reta separa. Crie o atributo <code>x²</code> e encontre um limiar nele que separe perfeitamente.",
            '''
import numpy as np

x = np.array([-3, -2.5, -2, -0.5, 0, 0.5, 2, 2.5, 3])
y = np.array([0, 0, 0, 1, 1, 1, 0, 0, 0])

novo = None
limiar = None
previsto = None
print(previsto)
''',
            [("Atributo x²", "import numpy as np\nassert np.allclose(novo, x ** 2)"), ("Separação perfeita", "import numpy as np\nassert (np.asarray(previsto) == y).all(), f'previsto = {previsto}'")],
            '''
import numpy as np

x = np.array([-3, -2.5, -2, -0.5, 0, 0.5, 2, 2.5, 3])
y = np.array([0, 0, 0, 1, 1, 1, 0, 0, 0])

novo = x ** 2
limiar = 2.0
previsto = (novo < limiar).astype(int)
print(previsto)
''', ["Em <code>x²</code>, os do meio ficam abaixo de 1 e os das pontas acima de 4.", "Qualquer limiar entre 0,25 e 4 serve."], exp="<p>O kernel faz isso implicitamente, sem criar as colunas novas.</p>"),
        erros([("SVM sem padronizar.", "As distâncias ficam distorcidas e o modelo piora muito."), ("SVM com milhões de exemplos.", "O treino com kernel escala mal. Para muitos dados, use modelos lineares ou árvores."), ("Ajustar C e gamma ao acaso.", "Faça busca em grade logarítmica com validação cruzada.")]),
        ponte("Kernels e embeddings", "<p>A ideia de “levar os dados para um espaço onde fica fácil separar” é o que as camadas de uma rede neural fazem, só que aprendendo esse espaço. Embeddings de LLMs são exatamente isso: um espaço onde significados parecidos ficam próximos.</p>"),
        quiz([
            ("O que são vetores de suporte?", ["Todos os dados.", "Os pontos mais próximos da fronteira.", "Os pesos do modelo."], 1, "Eles sustentam a fronteira."),
            ("C alto tende a:", ["Margem larga e tolerante.", "Margem estreita, poucos erros no treino (risco de overfitting).", "Ignorar os dados."], 1, "Rigidez."),
            ("O truque do kernel permite:", ["Treinar mais rápido.", "Fronteiras não lineares sem criar colunas explicitamente.", "Usar texto bruto."], 1, "Semelhança em espaço maior."),
        ]),
    ],
    ["A SVM busca a fronteira de maior margem.", "C controla o equilíbrio entre margem e erros.", "Kernels permitem fronteiras curvas."],
    "DBSCAN e clusterização hierárquica.",
    livro=("PDSH:05.07-support-vector-machines", "Seção 5.7, “In-Depth: Support Vector Machines”", "Como o livro visualiza a margem e os vetores de suporte?"))

AULAS["DBSCAN e clusterização hierárquica"] = aula(
    25,
    "O K-Means exige que você diga quantos grupos existem e só acha grupos redondos. O DBSCAN encontra grupos de qualquer formato, descobre quantos são e ainda aponta quem não pertence a nenhum. A clusterização hierárquica mostra os grupos dentro dos grupos.",
    ["entender densidade, <code>eps</code> e <code>min_samples</code>;", "identificar ruído com o DBSCAN;", "ler um dendrograma."],
    ["K-Means e distâncias."],
    [
        chute("No DBSCAN, o que acontece com um ponto isolado, longe de todos?", ["Vira um grupo próprio.", "É marcado como ruído.", "Vai para o grupo mais próximo."], 1,
              ["Grupos precisam de densidade mínima.", "Isso! O DBSCAN rotula como −1 quem não está numa região densa.", "Esse é o comportamento do K-Means."],
              "Ruído também é resposta: às vezes, é a anomalia que você procura."),
        concreto("Ilhas no mapa", "<p>Olhando um mapa noturno de luzes, você vê cidades (regiões densas de luz), estradas ligando bairros e casas isoladas no campo. O DBSCAN encontra as cidades pela densidade, seja qual for o formato, e deixa as casas isoladas de fora.</p>"),
        nota("Os parâmetros", [
            ("<code>eps</code>", "raio da vizinhança", "Distância para considerar dois pontos vizinhos."),
            ("<code>min_samples</code>", "densidade mínima", "Quantos vizinhos um ponto precisa para ser “núcleo”."),
            ("Rótulo −1", "ruído", "Não pertence a nenhum grupo."),
            ("Dendrograma", "árvore de fusões", "Mostra como os grupos se juntam; corte numa altura para escolher o número de grupos."),
        ]),
        cod("Quem é núcleo?", "Um ponto é <b>núcleo</b> se tem pelo menos <code>min_samples</code> pontos (contando ele mesmo) a até <code>eps</code> de distância. Devolva uma máscara com os núcleos.",
            '''
import numpy as np

def nucleos(X, eps, min_samples):
    return np.zeros(len(X), dtype=bool)

X = np.array([[0, 0], [0, 0.5], [0.5, 0], [5, 5], [10, 10], [10, 10.4], [10.3, 10]])
print(nucleos(X, 1.0, 3))
''',
            [("Núcleos corretos", "import numpy as np\nr = nucleos(X, 1.0, 3)\nassert r.tolist() == [True, True, True, False, True, True, True], f'{r.tolist()}'")],
            '''
import numpy as np

def nucleos(X, eps, min_samples):
    dist = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(axis=2))
    return (dist <= eps).sum(axis=1) >= min_samples

X = np.array([[0, 0], [0, 0.5], [0.5, 0], [5, 5], [10, 10], [10, 10.4], [10.3, 10]])
print(nucleos(X, 1.0, 3))
''', ["Matriz de distâncias de todos para todos com broadcasting.", "Conte por linha quantos estão a até <code>eps</code>."]),
        lab("DBSCAN × K-Means em meias-luas", '''
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN, KMeans
import matplotlib.pyplot as plt

X, _ = make_moons(400, noise=0.06, random_state=0)
fig, ax = plt.subplots(1, 2, figsize=(9, 4))
ax[0].scatter(*X.T, c=KMeans(2, n_init=10).fit_predict(X)); ax[0].set_title("K-Means")
ax[1].scatter(*X.T, c=DBSCAN(eps=0.2, min_samples=5).fit_predict(X)); ax[1].set_title("DBSCAN")
plt.show()
''', corpo="<p>Rode no Colab:</p>", exps=["Qual dos dois acerta as meias-luas?", "Mude <code>eps</code> para 0.05 e para 0.5. O que acontece?"]),
        erros([("Escolher eps ao acaso.", "Olhe o gráfico das distâncias ao k-ésimo vizinho e procure o “joelho”."), ("DBSCAN com densidades muito diferentes.", "Um eps só não serve para todos. HDBSCAN resolve."), ("Esquecer de padronizar.", "Densidade depende da escala.")]),
        ponte("Agrupando embeddings", "<p>Para descobrir os temas de milhares de perguntas feitas a um chatbot, agrupa-se os embeddings com HDBSCAN (o primo do DBSCAN). As perguntas “ruído” costumam ser as mais interessantes: casos que ninguém previu.</p>"),
        quiz([
            ("Qual vantagem do DBSCAN sobre o K-Means?", ["É sempre mais rápido.", "Acha grupos de formato livre e não exige o número de grupos.", "Não tem parâmetros."], 1, "E marca ruído."),
            ("O que significa o rótulo −1 no DBSCAN?", ["Grupo negativo.", "Ruído.", "Erro."], 1, "Ponto fora de regiões densas."),
            ("Como escolher o número de grupos num dendrograma?", ["Cortando a árvore numa altura.", "Contando as folhas.", "Não é possível."], 0, "Cada corte dá um número de grupos."),
        ]),
    ],
    ["DBSCAN agrupa por densidade e marca ruído.", "<code>eps</code> e <code>min_samples</code> definem o que é denso.", "Hierárquica mostra grupos dentro de grupos."],
    "Regularização: Ridge e Lasso.",
    livro=("ISLP", "Capítulo 12, seção 12.4.2, “Hierarchical Clustering”", "Como o livro interpreta a altura das fusões no dendrograma?"))

AULAS["Regularização Lasso e Ridge"] = aula(
    30,
    "Com muitas colunas e poucos dados, a regressão linear dá pesos enormes para explicar até o ruído. A regularização cobra uma “multa” por pesos grandes. O Ridge encolhe todos; o Lasso zera os inúteis, escolhendo atributos de brinde.",
    ["entender a penalidade L2 (Ridge) e L1 (Lasso);", "ver o efeito de λ (alpha) nos pesos;", "usar regularização contra overfitting."],
    ["Regressão linear e overfitting."],
    [
        chute("Aumentando muito o alpha do Lasso, o que acontece com os pesos?", ["Crescem.", "Vão a zero, um por um.", "Não mudam."], 1,
              ["A multa empurra os pesos para baixo.", "Isso! A penalidade L1 zera os pesos menos úteis primeiro, até zerar todos.", "Mudam bastante."],
              "Lasso faz seleção de atributos automaticamente."),
        concreto("O orçamento apertado", "<p>Sem limite de gastos, você compra tudo que parece útil. Com um orçamento, precisa escolher: o Ridge dá um pouco para todos, o Lasso corta itens inteiros e fica com os essenciais. A multa por peso é o orçamento do modelo.</p>"),
        nota("As penalidades", [
            (r"$\text{MSE} + \lambda \sum w_j^2$", "Ridge (L2)", "Encolhe todos os pesos, raramente a zero."),
            (r"$\text{MSE} + \lambda \sum |w_j|$", "Lasso (L1)", "Zera pesos: seleciona atributos."),
            ("Elastic Net", "mistura", "L1 + L2; bom com atributos correlacionados."),
            (r"$\lambda$ (<code>alpha</code>)", "força da multa", "0 = regressão comum; grande = pesos quase zero."),
        ], rot="Agora sim, as fórmulas"),
        cod("Ridge pela fórmula fechada", "O Ridge tem solução fechada: w = (XᵀX + λI)⁻¹ Xᵀy. Implemente e confira que pesos encolhem quando λ cresce.",
            '''
import numpy as np

def ridge(X, y, lam):
    return np.zeros(X.shape[1])

rng = np.random.default_rng(0)
X = rng.normal(size=(30, 5))
y = X @ np.array([3.0, -2, 0, 0, 1]) + rng.normal(0, 0.5, 30)
for lam in [0, 1, 100]:
    print(lam, np.round(ridge(X, y, lam), 2))
''',
            [("λ=0 é mínimos quadrados", "import numpy as np\nassert np.allclose(ridge(X, y, 0), np.linalg.lstsq(X, y, rcond=None)[0], atol=1e-6)"),
             ("Pesos encolhem com λ", "import numpy as np\nn = [np.linalg.norm(ridge(X, y, l)) for l in [0, 1, 100]]\nassert n[0] > n[1] > n[2], f'normas = {n}'")],
            '''
import numpy as np

def ridge(X, y, lam):
    n = X.shape[1]
    return np.linalg.solve(X.T @ X + lam * np.eye(n), X.T @ y)

rng = np.random.default_rng(0)
X = rng.normal(size=(30, 5))
y = X @ np.array([3.0, -2, 0, 0, 1]) + rng.normal(0, 0.5, 30)
for lam in [0, 1, 100]:
    print(lam, np.round(ridge(X, y, lam), 2))
''', ["<code>np.linalg.solve(X.T @ X + lam * np.eye(n), X.T @ y)</code>"]),
        erros([("Regularizar sem padronizar.", "A multa atinge mais as colunas de escala pequena (que precisam de pesos grandes)."), ("Escolher alpha no olho.", "Use validação cruzada (<code>RidgeCV</code>, <code>LassoCV</code>)."), ("Interpretar o atributo zerado pelo Lasso como “sem relação”.", "Com colunas correlacionadas, o Lasso fica com uma e zera as outras.")]),
        ponte("Weight decay", "<p>Em redes neurais, a penalidade L2 se chama <b>weight decay</b> e está ligada no otimizador AdamW, o padrão para treinar LLMs. É exatamente a ideia do Ridge, aplicada a bilhões de pesos.</p>"),
        quiz([
            ("Qual penalidade zera pesos?", ["Ridge (L2).", "Lasso (L1).", "Nenhuma."], 1, "Seleção de atributos."),
            ("Alpha muito grande causa:", ["Overfitting.", "Underfitting.", "Nada."], 1, "Pesos quase zero."),
            ("Weight decay em redes neurais é parente de:", ["Lasso.", "Ridge.", "K-Means."], 1, "Penalidade L2."),
        ]),
    ],
    ["Regularização penaliza pesos grandes para reduzir overfitting.", "Ridge encolhe; Lasso zera e seleciona.", "Padronize e escolha alpha por validação cruzada."],
    "Detecção de anomalias.",
    livro=("ISLP", "Capítulo 6, seção 6.2, “Shrinkage Methods”", "Por que o Lasso zera coeficientes e o Ridge não, segundo o livro?"))

AULAS["Detecção de anomalias"] = aula(
    30,
    "Uma compra de madrugada em outro país, um servidor com uso de CPU estranho, uma peça fora do padrão na linha de produção. Anomalias são raras e diferentes, e quase nunca há exemplos rotulados delas. A detecção de anomalias aprende o “normal” para apontar o que foge dele.",
    ["entender por que anomalias pedem abordagens não supervisionadas;", "usar z-score robusto e Isolation Forest;", "escolher um limiar de alerta."],
    ["Outliers e duplicados; árvores de decisão."],
    [
        chute("Por que o Isolation Forest acha anomalias com cortes aleatórios?", ["Porque anomalias são isoladas com poucos cortes.", "Porque ele sabe quais são as anomalias.", "Por sorte."], 0,
              ["Isso! Pontos diferentes ficam sozinhos depressa; pontos normais, no meio da multidão, exigem muitos cortes.", "Ele não usa rótulos.", "Os cortes são aleatórios, mas a conclusão não é."],
              "Pontuação de anomalia = quão rápido o ponto foi isolado."),
        concreto("Achar a pessoa de casaco no verão", "<p>Numa praia lotada, você acha a única pessoa de casaco com uma ou duas perguntas (“de casaco?”). Para separar uma pessoa comum das outras, precisaria de muitas. O Isolation Forest mede isso: quanto menos perguntas para isolar, mais estranho.</p>"),
        nota("Abordagens", [
            ("z-score robusto", "mediana e MAD", "Desvio em relação à mediana; resiste aos próprios extremos."),
            ("Isolation Forest", "isolamento", "Árvores com cortes aleatórios; profundidade média baixa = anomalia."),
            ("Local Outlier Factor", "densidade local", "Compara a densidade do ponto com a dos vizinhos."),
            ("<code>contamination</code>", "taxa esperada", "Quantos por cento de anomalias você espera: define o limiar."),
        ]),
        cod("z-score robusto", "Implemente o z-score robusto: (x − mediana) / (1,4826 · MAD), em que MAD é a mediana dos desvios absolutos. Devolva os índices com |z| &gt; 3,5.",
            '''
import numpy as np

def anomalias(x):
    return []

valores = np.array([50, 52, 49, 51, 48, 53, 50, 400, 47, 51, -100])
print(anomalias(valores))
''',
            [("Acha as duas anomalias", "import numpy as np\nassert list(anomalias(np.array([50, 52, 49, 51, 48, 53, 50, 400, 47, 51, -100]))) == [7, 10]")],
            '''
import numpy as np

def anomalias(x):
    med = np.median(x)
    mad = np.median(np.abs(x - med))
    z = (x - med) / (1.4826 * mad)
    return np.where(np.abs(z) > 3.5)[0].tolist()

valores = np.array([50, 52, 49, 51, 48, 53, 50, 400, 47, 51, -100])
print(anomalias(valores))
''', ["<code>mad = np.median(np.abs(x - med))</code>", "<code>np.where(np.abs(z) &gt; 3.5)[0]</code>"]),
        erros([("Usar média e desvio padrão com anomalias grandes nos dados.", "Os extremos inflam o desvio e se escondem. Use mediana e MAD."), ("Alertas demais.", "Ninguém lê 500 alertas por dia. Ajuste o limiar ao que a equipe consegue investigar."), ("Tratar o modelo como verdade.", "Anomalia é suspeita, não culpa. Feche o ciclo com rótulos de quem investigou.")]),
        ponte("Anomalias em sistemas de IA", "<p>Monitorar um modelo em produção é detectar anomalias: entradas muito diferentes do treino, respostas de LLM com tamanho ou custo fora do padrão, picos de latência. As mesmas técnicas protegem o próprio sistema de IA.</p>"),
        quiz([
            ("Por que detecção de anomalias costuma ser não supervisionada?", ["Porque é mais fácil.", "Porque quase nunca há exemplos rotulados de anomalias.", "Porque anomalias não existem."], 1, "São raras e variadas."),
            ("No Isolation Forest, uma anomalia é isolada:", ["Com muitos cortes.", "Com poucos cortes.", "Nunca."], 1, "Está longe da multidão."),
            ("Por que usar mediana e MAD?", ["São mais rápidas.", "Não são distorcidas pelos próprios valores extremos.", "Funcionam só com texto."], 1, "Estatísticas robustas."),
        ]),
    ],
    ["Anomalias são raras: aprenda o normal e aponte o que foge dele.", "z-score robusto e Isolation Forest são bons pontos de partida.", "O limiar deve caber na capacidade de investigação."],
    "Normalização e padronização.",
    livro=("PDSH:05.13-kernel-density-estimation", "Seção 5.13, “Kernel Density Estimation”", "Como a densidade estimada pode apontar pontos raros?"))
