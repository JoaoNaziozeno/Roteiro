# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 4 (parte A): fundamentos de redes neurais e arquiteturas."""
from lesson_factory import *

AULAS = {}

AULAS["Neurônio, camadas e pesos"] = aula(
    35,
    "Um neurônio artificial faz uma conta de ensino fundamental: multiplica cada entrada por um peso, soma tudo e passa por uma função. Empilhe milhares deles em camadas e você tem uma rede capaz de reconhecer rostos e escrever textos.",
    ["calcular a saída de um neurônio;", "montar uma camada como multiplicação de matrizes;", "contar os parâmetros de uma rede."],
    ["Regressão logística, produto escalar e matrizes (Matemática)."],
    [
        chute("Uma camada recebe 784 entradas e tem 128 neurônios. Quantos parâmetros ela tem?", ["912", "100.352", "100.480"], 2,
              ["Isso seria só somar.", "Faltaram os vieses: um por neurônio.", "Isso! 784 × 128 pesos + 128 vieses."],
              "Parâmetros de uma camada densa = entradas × saídas + saídas."),
        concreto("Uma votação ponderada", "<p>Para decidir se vai à praia, você pesa: sol (peso alto), calor (médio), trânsito (negativo). Soma tudo e, se passar de um limite, vai. Um neurônio é essa decisão ponderada; uma camada são muitas decisões ao mesmo tempo; uma rede são decisões sobre decisões.</p>"),
        crianca("<p>Cada neurônio é uma pessoa que escuta várias outras, dá mais atenção a umas que a outras, e depois grita “sim!” ou fica quieta. Na próxima fileira, outras pessoas escutam esses gritos. No fim da fila, sai a resposta.</p>"),
        ver("como o vídeo descreve o que cada camada de neurônios “procura” na imagem"),
        nota("A conta de uma camada", [
            (r"$z = w \cdot x + b$", "soma ponderada", "Um neurônio: produto escalar mais viés."),
            (r"$a = f(z)$", "ativação", "Uma função não linear, como ReLU ou sigmoide."),
            (r"$A = f(XW + b)$", "camada inteira", "Todos os neurônios de uma vez, para um lote de exemplos."),
            ("<code>nn.Linear(784, 128)</code>", "no PyTorch", "Guarda W (128 × 784) e b (128)."),
        ], rot="Agora sim, a fórmula"),
        cod("Uma camada com NumPy", "Implemente <code>camada(X, W, b)</code> com ativação ReLU e passe um lote de 4 exemplos por uma rede de duas camadas (3 → 5 → 2).",
            '''
import numpy as np

def relu(z):
    return np.maximum(0, z)

def camada(X, W, b):
    return X

rng = np.random.default_rng(0)
X = rng.normal(size=(4, 3))
W1, b1 = rng.normal(size=(3, 5)), np.zeros(5)
W2, b2 = rng.normal(size=(5, 2)), np.zeros(2)

resultado = camada(camada(X, W1, b1), W2, b2)
print(resultado.shape)
''',
            [("Formato (4, 2)", "assert resultado.shape == (4, 2), f'shape = {resultado.shape}'"), ("Valores corretos", "import numpy as np\nassert np.allclose(resultado, relu(relu(X @ W1 + b1) @ W2 + b2))"), ("Sem negativos (ReLU)", "assert (resultado >= 0).all()")],
            '''
import numpy as np

def relu(z):
    return np.maximum(0, z)

def camada(X, W, b):
    return relu(X @ W + b)

rng = np.random.default_rng(0)
X = rng.normal(size=(4, 3))
W1, b1 = rng.normal(size=(3, 5)), np.zeros(5)
W2, b2 = rng.normal(size=(5, 2)), np.zeros(2)

resultado = camada(camada(X, W1, b1), W2, b2)
print(resultado.shape)
''', ["<code>relu(X @ W + b)</code>: multiplicação de matrizes e broadcasting do viés."]),
        lab("A mesma rede no PyTorch", '''
import torch
from torch import nn

rede = nn.Sequential(nn.Linear(784, 128), nn.ReLU(), nn.Linear(128, 10))
x = torch.randn(32, 784)            # lote de 32 imagens 28x28 achatadas
print(rede(x).shape)                 # (32, 10): uma nota por dígito
print(sum(p.numel() for p in rede.parameters()), "parâmetros")
''', corpo="<p>Rode no Colab:</p>", exps=["Confira a contagem de parâmetros na mão.", "Acrescente uma camada de 64 neurônios no meio."]),
        erros([("Esquecer a ativação entre camadas.", "Sem ela, várias camadas lineares equivalem a uma só."), ("Formatos que não batem.", "A saída de uma camada é a entrada da próxima: confira os <code>shape</code>."), ("Achar que mais camadas é sempre melhor.", "Mais capacidade = mais dados e cuidado com overfitting.")]),
        ponte("De 100 mil a 100 bilhões", "<p>A rede do exercício tem uns 100 mil parâmetros. Um LLM tem dezenas ou centenas de bilhões, mas cada camada linear dele faz exatamente <code>XW + b</code>. O que muda é a escala e a arquitetura em volta (atenção, normalização).</p>"),
        quiz([
            ("O que o viés faz num neurônio?", ["Multiplica as entradas.", "Desloca a soma, permitindo ativar mesmo com entradas zero.", "Normaliza a saída."], 1, "Como o b da reta."),
            ("Por que precisamos de funções de ativação não lineares?", ["Para acelerar.", "Sem elas, a rede inteira vira uma única transformação linear.", "Para ter menos pesos."], 1, "A não linearidade dá poder."),
            ("Parâmetros de <code>nn.Linear(10, 3)</code>:", ["13", "30", "33"], 2, "10 × 3 + 3."),
        ]),
    ],
    ["Neurônio: soma ponderada + viés, depois ativação.", "Camada: <code>f(XW + b)</code> para um lote inteiro.", "Parâmetros = entradas × saídas + saídas."],
    "Funções de ativação.",
    livro=("NNDL:chap1", "Capítulo 1, “Using neural nets to recognize handwritten digits”", "Como o livro passa do perceptron ao neurônio sigmoide?"))

AULAS["Funções de ativação"] = aula(
    25,
    "Sem ativação, empilhar camadas não adianta: tudo vira uma reta. A função de ativação é a pitada de não linearidade que deixa a rede desenhar curvas, e a escolha dela já decidiu se redes profundas treinavam ou não.",
    ["conhecer sigmoide, tanh, ReLU, GELU e softmax;", "entender o problema do gradiente que desaparece;", "escolher a ativação de cada camada."],
    ["Neurônio, camadas e pesos."],
    [
        chute("Qual a derivada da sigmoide quando a entrada é muito grande (por exemplo, 10)?", ["Grande.", "Quase zero.", "Exatamente 1."], 1,
              ["A curva fica plana nas pontas.", "Isso! A sigmoide satura e o gradiente some: as camadas de baixo param de aprender.", "Só a identidade tem derivada 1 sempre."],
              "Por isso a ReLU, com derivada 1 para positivos, destravou as redes profundas."),
        concreto("O interruptor e o dimmer", "<p>A ReLU é um interruptor com dimmer: abaixo de zero, desligado; acima, deixa passar proporcionalmente. A sigmoide é um dimmer que trava nas pontas: girar mais não muda nada, e é aí que o aprendizado empaca.</p>"),
        tabela("As principais", ["Ativação", "Fórmula", "Onde usar"], [
            ["ReLU", "max(0, z)", "camadas ocultas: padrão"],
            ["GELU", "z·Φ(z) (suave)", "Transformers e LLMs"],
            ["Sigmoide", "1 / (1 + e^(−z))", "saída binária"],
            ["Tanh", "entre −1 e 1", "RNNs clássicas"],
            ["Softmax", "e^z / Σe^z", "saída multiclasse"],
        ]),
        cod("Ativações e suas derivadas", "Implemente <code>sigmoide</code>, <code>d_sigmoide</code> (σ(z)·(1 − σ(z))), <code>relu</code> e <code>d_relu</code> (1 se z &gt; 0, senão 0). Depois compare os gradientes em z = 10.",
            '''
import numpy as np

def sigmoide(z): return z
def d_sigmoide(z): return z
def relu(z): return z
def d_relu(z): return z

z = np.array([-10.0, 0.0, 10.0])
print(d_sigmoide(z), d_relu(z))
''',
            [("Sigmoide", "import numpy as np\nassert np.allclose(sigmoide(np.array([0.0])), [0.5])"), ("Derivada da sigmoide", "import numpy as np\nassert np.allclose(d_sigmoide(np.array([0.0])), [0.25]) and d_sigmoide(np.array([10.0]))[0] < 1e-4"),
             ("ReLU e derivada", "import numpy as np\nz = np.array([-2.0, 3.0])\nassert np.allclose(relu(z), [0, 3]) and np.allclose(d_relu(z), [0, 1])")],
            '''
import numpy as np

def sigmoide(z): return 1 / (1 + np.exp(-z))
def d_sigmoide(z): return sigmoide(z) * (1 - sigmoide(z))
def relu(z): return np.maximum(0, z)
def d_relu(z): return (z > 0).astype(float)

z = np.array([-10.0, 0.0, 10.0])
print(d_sigmoide(z), d_relu(z))
''', ["<code>(z &gt; 0).astype(float)</code> é a derivada da ReLU."]),
        erros([("Sigmoide nas camadas ocultas de redes profundas.", "Gradientes somem. Use ReLU ou GELU."), ("Softmax e depois <code>CrossEntropyLoss</code> no PyTorch.", "A perda já aplica o softmax internamente: aplique duas vezes e o treino piora."), ("Neurônios ReLU “mortos”.", "Se a soma for sempre negativa, o gradiente é zero para sempre. Taxas menores ou LeakyReLU ajudam.")]),
        ponte("Ativações nos LLMs", "<p>Os blocos de rede neural dentro de cada camada de um Transformer usam GELU ou SwiGLU, versões suaves da ReLU. E na última camada, um softmax sobre o vocabulário inteiro transforma notas em probabilidades para o próximo token.</p>"),
        quiz([
            ("Qual ativação é o padrão em camadas ocultas?", ["Sigmoide.", "ReLU (ou GELU).", "Softmax."], 1, "Gradientes saudáveis."),
            ("O que é o gradiente que desaparece?", ["Pesos que viram zero.", "Derivadas muito pequenas que impedem as camadas iniciais de aprender.", "Um erro de memória."], 1, "Comum com sigmoide."),
            ("Qual ativação usar na saída com 10 classes?", ["ReLU.", "Softmax.", "Tanh."], 1, "Probabilidades que somam 1."),
        ]),
    ],
    ["Ativações dão não linearidade às redes.", "ReLU/GELU nas ocultas; sigmoide ou softmax na saída.", "Saturação faz o gradiente sumir."],
    "Função de perda.",
    livro=("D2L:chapter_multilayer-perceptrons/mlp", "Seção 5.1, “Multilayer Perceptrons”, parte sobre funções de ativação", "Que gráficos de derivadas o livro mostra?"))

AULAS["Função de perda"] = aula(
    25,
    "Para aprender, a rede precisa de um número que diga o quão errada ela está. A função de perda é esse número, e escolher a perda certa é dizer ao modelo o que você realmente quer que ele faça.",
    ["usar MSE para regressão e entropia cruzada para classificação;", "calcular a entropia cruzada à mão;", "entender por que a perda precisa ser derivável."],
    ["Funções de ativação e métricas."],
    [
        chute("O modelo deu 0,9 de probabilidade para a classe certa num exemplo e 0,1 em outro. Qual exemplo gera mais perda na entropia cruzada?", ["O de 0,9.", "O de 0,1.", "Os dois iguais."], 1,
              ["−log(0,9) ≈ 0,1: pequena.", "Isso! −log(0,1) ≈ 2,3: errar com confiança custa caro.", "O logaritmo pune muito mais o 0,1."],
              "Entropia cruzada = −log(probabilidade dada à resposta certa)."),
        concreto("A nota do professor exigente", "<p>Um professor exigente não só marca certo ou errado: dá meia nota para quem quase acertou e pune muito quem errou com convicção. A entropia cruzada é esse professor.</p>"),
        nota("As perdas mais usadas", [
            (r"$\frac{1}{n}\sum (y - \hat y)^2$", "MSE", "Regressão. Pune muito erros grandes."),
            (r"$\frac{1}{n}\sum |y - \hat y|$", "MAE", "Regressão robusta a outliers."),
            (r"$-\log \hat p_{\text{correta}}$", "entropia cruzada", "Classificação. <code>nn.CrossEntropyLoss</code> recebe as notas brutas (logits)."),
            ("Perda × métrica", "diferença", "A perda precisa ser derivável para o gradiente; a métrica (acurácia, F1) é o que você reporta."),
        ], rot="Agora sim, as fórmulas"),
        cod("Entropia cruzada do zero", "Implemente a entropia cruzada média a partir de <b>logits</b> (notas brutas): aplique o softmax estável e tire −log da probabilidade da classe certa.",
            '''
import numpy as np

def entropia_cruzada(logits, rotulos):
    return 0.0

logits = np.array([[2.0, 1.0, 0.1], [0.5, 2.5, 0.3]])
rotulos = np.array([0, 1])
print(round(entropia_cruzada(logits, rotulos), 4))
''',
            [("Valor correto", "import numpy as np\nassert abs(entropia_cruzada(np.array([[2.0, 1.0, 0.1], [0.5, 2.5, 0.3]]), np.array([0, 1])) - 0.3185) < 1e-3"),
             ("Logits enormes não quebram", "import numpy as np\nr = entropia_cruzada(np.array([[1000.0, 0.0]]), np.array([0]))\nassert np.isfinite(r) and r < 1e-6"),
             ("Uniforme = log(classes)", "import numpy as np\nassert abs(entropia_cruzada(np.zeros((1, 4)), np.array([2])) - np.log(4)) < 1e-9")],
            '''
import numpy as np

def entropia_cruzada(logits, rotulos):
    z = logits - logits.max(axis=1, keepdims=True)
    log_probs = z - np.log(np.exp(z).sum(axis=1, keepdims=True))
    return float(-log_probs[np.arange(len(rotulos)), rotulos].mean())

logits = np.array([[2.0, 1.0, 0.1], [0.5, 2.5, 0.3]])
rotulos = np.array([0, 1])
print(round(entropia_cruzada(logits, rotulos), 4))
''', ["Subtraia o máximo de cada linha antes de exponenciar.", "log softmax = z − log(Σ e^z); pegue a coluna do rótulo de cada linha."]),
        erros([("MSE para classificação.", "Aprende devagar e mal. Use entropia cruzada."), ("Calcular log da probabilidade sem estabilidade.", "log(0) = −∞. Trabalhe com log-softmax."), ("Otimizar a perda e reportar outra coisa sem checar.", "Perda caindo e métrica piorando indica problema.")]),
        ponte("A perda dos LLMs", "<p>O pré-treino de um LLM minimiza exatamente a entropia cruzada do próximo token, somada sobre trilhões de tokens. A “perplexidade” que aparece em artigos é só e elevado à perda média.</p>"),
        quiz([
            ("Para regressão, a perda padrão é:", ["Entropia cruzada.", "MSE.", "Acurácia."], 1, "Erro quadrático."),
            ("Por que a acurácia não serve como perda?", ["É lenta.", "Não é derivável de forma útil para o gradiente.", "É sempre alta."], 1, "Muda aos saltos."),
            ("Errar com convicção, na entropia cruzada:", ["Custa pouco.", "Custa muito.", "Não custa nada."], 1, "−log de um número pequeno é grande."),
        ]),
    ],
    ["A perda mede o erro de forma derivável.", "MSE para regressão; entropia cruzada para classificação.", "Use log-softmax estável."],
    "Backpropagation: como a rede aprende.",
    livro=("NNDL:chap3", "Capítulo 3, seção sobre a função de custo de entropia cruzada", "Por que o livro diz que a entropia cruzada acelera o aprendizado?"))

AULAS["Backpropagation"] = aula(
    40,
    "A rede errou. Qual dos milhões de pesos é culpado, e quanto? A retropropagação responde com a regra da cadeia: o erro é distribuído de trás para frente, camada por camada, e cada peso recebe sua parte da culpa.",
    ["aplicar a regra da cadeia num grafo de contas;", "fazer forward e backward numa rede pequena;", "conferir gradientes numericamente."],
    ["Derivadas (Matemática), função de perda e gradiente descendente."],
    [
        chute("Em <code>y = (a · b) + c</code>, com a = 2, b = 3, c = 1, qual a derivada de y em relação a a?", ["1", "3", "6"], 1,
              ["1 é a derivada em relação a c.", "Isso! Mudar a em uma unidade muda a·b em b = 3 unidades.", "6 é o valor de a·b."],
              "Cada operação sabe a própria derivada local; a cadeia multiplica tudo."),
        concreto("O telefone sem fio ao contrário", "<p>Na linha de montagem, o produto final saiu errado. O inspetor volta posto por posto perguntando “quanto do erro veio daqui?”. Cada posto só precisa saber o que fez localmente; a responsabilidade vai sendo passada para trás. É a retropropagação.</p>"),
        ver("como o vídeo mostra a sensibilidade da perda a cada peso"),
        nota("A regra da cadeia", [
            (r"$\frac{\partial L}{\partial w} = \frac{\partial L}{\partial a} \cdot \frac{\partial a}{\partial z} \cdot \frac{\partial z}{\partial w}$", "cadeia", "Multiplique as derivadas locais pelo caminho."),
            ("Forward", "ida", "Calcula e guarda os valores intermediários."),
            ("Backward", "volta", "Usa esses valores para calcular os gradientes de trás para frente."),
            ("Checagem numérica", "conferência", "(L(w + ε) − L(w − ε)) / 2ε deve bater com o gradiente."),
        ], rot="Agora sim, a regra"),
        cod("Backprop num neurônio", "Um neurônio com sigmoide e perda MSE: z = w·x + b, a = σ(z), L = (a − y)². Complete o backward e confira com a derivada numérica.",
            '''
import numpy as np

def sig(z): return 1 / (1 + np.exp(-z))

def perda(w, b, x, y):
    return (sig(w * x + b) - y) ** 2

def gradientes(w, b, x, y):
    z = w * x + b
    a = sig(z)
    dL_da = 0.0
    da_dz = 0.0
    dL_dw = 0.0
    dL_db = 0.0
    return dL_dw, dL_db

w, b, x, y = 0.5, -0.2, 1.5, 1.0
print(gradientes(w, b, x, y))
''',
            [("dL/dw bate com o numérico", "e = 1e-6\nnum = (perda(w + e, b, x, y) - perda(w - e, b, x, y)) / (2 * e)\nassert abs(gradientes(w, b, x, y)[0] - num) < 1e-6, f'analítico {gradientes(w, b, x, y)[0]}, numérico {num}'"),
             ("dL/db bate com o numérico", "e = 1e-6\nnum = (perda(w, b + e, x, y) - perda(w, b - e, x, y)) / (2 * e)\nassert abs(gradientes(w, b, x, y)[1] - num) < 1e-6")],
            '''
import numpy as np

def sig(z): return 1 / (1 + np.exp(-z))

def perda(w, b, x, y):
    return (sig(w * x + b) - y) ** 2

def gradientes(w, b, x, y):
    z = w * x + b
    a = sig(z)
    dL_da = 2 * (a - y)
    da_dz = a * (1 - a)
    dL_dw = dL_da * da_dz * x
    dL_db = dL_da * da_dz
    return dL_dw, dL_db

w, b, x, y = 0.5, -0.2, 1.5, 1.0
print(gradientes(w, b, x, y))
''', ["dL/da = 2(a − y); da/dz = a(1 − a); dz/dw = x; dz/db = 1.", "Multiplique pela cadeia."]),
        cod("Uma rede aprende XOR", "Treine uma rede 2 → 4 → 1 (tanh na oculta, sigmoide na saída) com backprop para aprender o XOR. Os gradientes da saída já estão prontos; complete os da camada oculta.",
            '''
import numpy as np

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([[0], [1], [1], [0]], dtype=float)
rng = np.random.default_rng(1)
W1, b1 = rng.normal(0, 1, (2, 4)), np.zeros(4)
W2, b2 = rng.normal(0, 1, (4, 1)), np.zeros(1)

for passo in range(5000):
    h = np.tanh(X @ W1 + b1)
    p = 1 / (1 + np.exp(-(h @ W2 + b2)))
    dz2 = (p - y) / len(X)              # entropia cruzada + sigmoide
    dW2, db2 = h.T @ dz2, dz2.sum(axis=0)
    dh = dz2 @ W2.T
    dz1 = dh                             # complete: derivada da tanh é 1 - h**2
    dW1, db1 = X.T @ dz1, dz1.sum(axis=0)
    for P, G in [(W1, dW1), (b1, db1), (W2, dW2), (b2, db2)]:
        P -= 1.0 * G

print(np.round(p.ravel(), 2))
''',
            [("Aprende o XOR", "assert ((p.ravel() > 0.5).astype(int) == [0, 1, 1, 0]).all(), f'p = {p.ravel().round(2)}'")],
            '''
import numpy as np

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([[0], [1], [1], [0]], dtype=float)
rng = np.random.default_rng(1)
W1, b1 = rng.normal(0, 1, (2, 4)), np.zeros(4)
W2, b2 = rng.normal(0, 1, (4, 1)), np.zeros(1)

for passo in range(5000):
    h = np.tanh(X @ W1 + b1)
    p = 1 / (1 + np.exp(-(h @ W2 + b2)))
    dz2 = (p - y) / len(X)
    dW2, db2 = h.T @ dz2, dz2.sum(axis=0)
    dh = dz2 @ W2.T
    dz1 = dh * (1 - h ** 2)
    dW1, db1 = X.T @ dz1, dz1.sum(axis=0)
    for P, G in [(W1, dW1), (b1, db1), (W2, dW2), (b2, db2)]:
        P -= 1.0 * G

print(np.round(p.ravel(), 2))
''', ["<code>dz1 = dh * (1 - h ** 2)</code>: a cadeia passa pela derivada da tanh."], rot="Mão no código · nível 2"),
        erros([("Esquecer de multiplicar pela derivada da ativação.", "O gradiente fica errado e a rede não aprende. Confira numericamente."), ("Achar que backprop é um algoritmo de aprendizado.", "Ele só calcula gradientes; quem aprende é o otimizador."), ("Não guardar os valores do forward.", "O backward precisa deles.")]),
        ponte("Autograd faz isso por você", "<p>No PyTorch, <code>loss.backward()</code> faz exatamente o que você escreveu, automaticamente, para qualquer rede. Mas entender a cadeia ajuda a diagnosticar gradientes que somem ou explodem, um problema real em redes profundas e LLMs.</p>"),
        quiz([
            ("O que a retropropagação calcula?", ["A saída da rede.", "Os gradientes da perda em relação a cada peso.", "A acurácia."], 1, "Pela regra da cadeia."),
            ("Para que guardar os valores do forward?", ["Para o backward usar nas derivadas locais.", "Para imprimir.", "Não é preciso."], 0, "Cada derivada depende deles."),
            ("Como conferir se o gradiente está certo?", ["Pela acurácia.", "Comparando com a diferença numérica.", "Não dá."], 1, "Gradient checking."),
        ]),
    ],
    ["Backprop aplica a regra da cadeia de trás para frente.", "Forward guarda valores; backward usa-os para os gradientes.", "Confira gradientes numericamente."],
    "Gradiente descendente e otimizadores.",
    livro=("NNDL:chap2", "Capítulo 2, “How the backpropagation algorithm works”", "Quais são as quatro equações fundamentais do livro?"))

AULAS["Gradiente descendente e otimizadores (SGD, Adam)"] = aula(
    30,
    "Você já sabe descer a montanha com o gradiente. Mas o terreno de uma rede neural tem vales estreitos, platôs e milhões de dimensões. Otimizadores como momentum e Adam são técnicas de alpinismo que descem mais rápido e com menos tropeços.",
    ["entender SGD com lotes;", "entender momentum e Adam;", "escolher otimizador e taxa de aprendizado."],
    ["Backpropagation e gradiente descendente (Matemática)."],
    [
        chute("Por que treinar com mini-lotes em vez de usar todos os dados a cada passo?", ["Porque fica mais exato.", "Porque cada passo fica muito mais barato, e o ruído até ajuda a escapar de lugares ruins.", "Porque é obrigatório."], 1,
              ["O gradiente de um lote é uma estimativa, não exato.", "Isso! Milhares de passos baratos vencem poucos passos caros.", "É uma escolha prática."],
              "SGD com mini-lotes é a base de todo treino moderno."),
        concreto("A bola na ladeira", "<p>O SGD é uma pessoa cega dando passos na direção mais íngreme. O momentum é uma bola rolando: ganha velocidade nas descidas consistentes e não para em qualquer buraquinho. O Adam ajusta o tamanho do passo de cada direção conforme o terreno.</p>"),
        nota("Os otimizadores", [
            (r"$w \leftarrow w - \eta g$", "SGD", "Passo na direção oposta ao gradiente do lote."),
            (r"$v \leftarrow \beta v + g;\ w \leftarrow w - \eta v$", "momentum", "Acumula a direção dos passos anteriores."),
            ("Adam", "momento + escala adaptativa", "Média dos gradientes e dos quadrados; passo ajustado por parâmetro. Padrão em deep learning."),
            ("AdamW", "Adam + weight decay correto", "Padrão para Transformers e LLMs."),
        ], rot="Agora sim, as fórmulas"),
        cod("Momentum num vale estreito", "Minimize f(x, y) = x² + 25y² (um vale estreito) começando em (5, 1). Compare 50 passos de SGD (taxa 0.01) com 50 de momentum (taxa 0.01, β = 0.9).",
            '''
import numpy as np

def grad(p):
    return np.array([2 * p[0], 50 * p[1]])

def sgd(passos=50, lr=0.01):
    p = np.array([5.0, 1.0])
    for _ in range(passos):
        p = p - lr * grad(p)
    return p

def momentum(passos=50, lr=0.01, beta=0.9):
    p = np.array([5.0, 1.0])
    v = np.zeros(2)
    for _ in range(passos):
        pass  # atualize v e p
    return p

print(np.round(sgd(), 3), np.round(momentum(), 3))
''',
            [("Momentum chega mais perto do mínimo", "import numpy as np\nassert np.linalg.norm(momentum()) < np.linalg.norm(sgd()), f'sgd {sgd()}, momentum {momentum()}'"), ("Momentum converge", "import numpy as np\nassert np.linalg.norm(momentum(300)) < 1e-3")],
            '''
import numpy as np

def grad(p):
    return np.array([2 * p[0], 50 * p[1]])

def sgd(passos=50, lr=0.01):
    p = np.array([5.0, 1.0])
    for _ in range(passos):
        p = p - lr * grad(p)
    return p

def momentum(passos=50, lr=0.01, beta=0.9):
    p = np.array([5.0, 1.0])
    v = np.zeros(2)
    for _ in range(passos):
        v = beta * v + grad(p)
        p = p - lr * v
    return p

print(np.round(sgd(), 3), np.round(momentum(), 3))
''', ["<code>v = beta * v + grad(p)</code> e <code>p = p - lr * v</code>."]),
        erros([("Taxa de aprendizado alta demais.", "A perda oscila ou vira NaN. Diminua 10 vezes."), ("Mudar de otimizador antes de ajustar a taxa.", "A taxa importa mais que o otimizador."), ("Usar Adam com weight decay comum.", "Para regularizar direito, use AdamW.")]),
        ponte("O otimizador dos LLMs", "<p>LLMs são treinados com AdamW, taxa de aprendizado com aquecimento (warmup) e decaimento em cosseno, e lotes de milhões de tokens. Tudo variações do que você viu: o passo continua sendo “ande contra o gradiente”.</p>"),
        quiz([
            ("O que o momentum acumula?", ["Os pesos.", "A direção dos gradientes anteriores.", "A perda."], 1, "Inércia."),
            ("Qual otimizador é padrão para Transformers?", ["SGD puro.", "AdamW.", "Newton."], 1, "Adam com weight decay desacoplado."),
            ("Perda virou NaN. Primeiro suspeito:", ["Poucos dados.", "Taxa de aprendizado alta demais.", "Muitas camadas."], 1, "Diminua a taxa."),
        ]),
    ],
    ["SGD com mini-lotes é a base do treino.", "Momentum acelera nas direções consistentes; Adam adapta o passo.", "A taxa de aprendizado é o hiperparâmetro mais importante."],
    "Regularização em redes: dropout e weight decay.",
    livro=("D2L:chapter_optimization/adam", "Seção 12.10, “Adam”", "Como o livro corrige o viés das médias no início do Adam?"))

AULAS["Regularização (dropout, weight decay)"] = aula(
    25,
    "Redes grandes decoram com facilidade. Duas técnicas simples seguram esse impulso: o weight decay, que cobra uma multa por pesos grandes, e o dropout, que desliga neurônios ao acaso no treino para nenhum deles virar indispensável.",
    ["entender e aplicar dropout;", "relacionar weight decay e Ridge;", "saber o comportamento diferente no treino e na avaliação."],
    ["Regularização Lasso e Ridge; overfitting."],
    [
        chute("Com dropout de 50% no treino, o que acontece na hora de prever?", ["Metade dos neurônios continua desligada.", "Todos os neurônios ficam ligados (e as saídas são reescaladas).", "A rede para de funcionar."], 1,
              ["Isso deixaria as previsões aleatórias.", "Isso! Na avaliação o dropout é desligado. Por isso existem <code>model.train()</code> e <code>model.eval()</code>.", "Ela funciona normalmente."],
              "Esquecer o <code>model.eval()</code> é um bug clássico."),
        concreto("O time sem estrela", "<p>Se o técnico tira jogadores ao acaso em cada treino, ninguém pode depender sempre do craque: todos aprendem a jogar. O dropout faz isso com os neurônios: a rede aprende caminhos redundantes e generaliza melhor.</p>"),
        nota("As duas técnicas", [
            ("<code>nn.Dropout(p=0.3)</code>", "dropout", "No treino, zera cada ativação com probabilidade p e multiplica o resto por 1/(1−p)."),
            ("<code>AdamW(..., weight_decay=0.01)</code>", "weight decay", "Encolhe os pesos a cada passo: a penalidade L2."),
            ("<code>model.train()</code> / <code>model.eval()</code>", "modos", "Ligam e desligam dropout (e mudam o BatchNorm)."),
        ]),
        cod("Dropout invertido", "Implemente o dropout como no PyTorch: no treino, zere com probabilidade p e divida o resto por (1 − p); na avaliação, devolva a entrada intacta. A média das ativações deve se manter.",
            '''
import numpy as np

def dropout(a, p, treino, rng):
    return a

rng = np.random.default_rng(0)
a = np.ones(100000)
d = dropout(a, 0.3, True, rng)
print((d == 0).mean(), d.mean())
''',
            [("Zera cerca de 30%", "import numpy as np\nd = dropout(np.ones(100000), 0.3, True, np.random.default_rng(0))\nassert abs((d == 0).mean() - 0.3) < 0.01"),
             ("Média preservada", "import numpy as np\nd = dropout(np.ones(100000), 0.3, True, np.random.default_rng(0))\nassert abs(d.mean() - 1) < 0.02"),
             ("Na avaliação não muda nada", "import numpy as np\na = np.arange(5.0)\nassert np.array_equal(dropout(a, 0.5, False, np.random.default_rng(0)), a)")],
            '''
import numpy as np

def dropout(a, p, treino, rng):
    if not treino:
        return a
    mascara = rng.random(a.shape) >= p
    return a * mascara / (1 - p)

rng = np.random.default_rng(0)
a = np.ones(100000)
d = dropout(a, 0.3, True, rng)
print((d == 0).mean(), d.mean())
''', ["<code>mascara = rng.random(a.shape) &gt;= p</code>", "<code>a * mascara / (1 - p)</code>"]),
        erros([("Avaliar sem <code>model.eval()</code>.", "As previsões ficam aleatórias e piores."), ("Dropout alto em redes pequenas.", "Vira underfitting. Comece com 0,1 a 0,3."), ("Achar que regularização substitui dados.", "Mais dados continua sendo o melhor regularizador.")]),
        ponte("Regularização em LLMs", "<p>LLMs grandes usam pouco ou nenhum dropout no pré-treino (os dados são tantos que não dá para decorar), mas usam weight decay. Já no ajuste fino com poucos dados, dropout e cuidado com épocas voltam a ser importantes.</p>"),
        quiz([
            ("O que o dropout faz no treino?", ["Remove camadas.", "Zera ativações ao acaso.", "Diminui a taxa de aprendizado."], 1, "Neurônios desligados aleatoriamente."),
            ("Weight decay é parente de:", ["Lasso.", "Ridge (L2).", "K-Means."], 1, "Encolhe pesos."),
            ("Por que chamar <code>model.eval()</code> antes de avaliar?", ["Para salvar o modelo.", "Para desligar o dropout e fixar o BatchNorm.", "Para usar a GPU."], 1, "Comportamento de inferência."),
        ]),
    ],
    ["Dropout desliga neurônios ao acaso no treino.", "Weight decay encolhe pesos (L2).", "Use <code>train()</code> e <code>eval()</code> nos momentos certos."],
    "CNNs para imagens.",
    livro=("D2L:chapter_multilayer-perceptrons/dropout", "Seção 5.6, “Dropout”", "Como o livro justifica o reescalonamento por 1/(1−p)?"))

AULAS["CNNs para imagens"] = aula(
    35,
    "Uma imagem de 224 × 224 pixels coloridos tem 150 mil números. Conectar todos a todos seria inviável. A convolução usa uma ideia mais esperta: um pequeno filtro desliza pela imagem procurando o mesmo padrão (uma borda, uma textura) em qualquer lugar.",
    ["entender convolução, filtros e mapas de ativação;", "calcular o tamanho da saída;", "conhecer pooling e a arquitetura típica de uma CNN."],
    ["Neurônio, camadas e pesos; matrizes."],
    [
        chute("Por que um filtro de convolução tem tão poucos pesos (por exemplo, 3 × 3 = 9)?", ["Porque a imagem é pequena.", "Porque o mesmo filtro é reaproveitado em todas as posições da imagem.", "Porque perde informação."], 1,
              ["Funciona com imagens de qualquer tamanho.", "Isso! Compartilhar pesos permite achar um padrão em qualquer lugar com poucos parâmetros.", "É uma vantagem, não uma perda."],
              "Um gato no canto ou no centro continua sendo um gato."),
        concreto("A lupa que procura", "<p>Você passa uma lupa por uma página procurando a letra “a”. A lupa é o filtro; onde ela encontra o padrão, você marca. A primeira camada procura bordas; as seguintes juntam bordas em formas, formas em olhos, olhos em rostos.</p>"),
        nota("As peças", [
            ("Filtro (kernel) k × k", "padrão procurado", "Desliza pela imagem; em cada posição faz uma soma ponderada."),
            ("Mapa de ativação", "onde o padrão apareceu", "Um mapa por filtro."),
            (r"$\text{saída} = \frac{n + 2p - k}{s} + 1$", "tamanho", "n: entrada, p: preenchimento (padding), k: filtro, s: passo (stride)."),
            ("Max pooling 2 × 2", "resumir", "Fica com o maior valor de cada bloco; reduz o tamanho pela metade."),
            ("<code>nn.Conv2d(3, 16, kernel_size=3, padding=1)</code>", "no PyTorch", "3 canais de entrada, 16 filtros."),
        ]),
        cod("Convolução do zero", "Implemente a convolução 2D (sem padding, passo 1) e aplique o filtro de bordas verticais na imagem: a borda entre o escuro e o claro deve se destacar.",
            '''
import numpy as np

def conv2d(img, filtro):
    k = filtro.shape[0]
    h, w = img.shape[0] - k + 1, img.shape[1] - k + 1
    saida = np.zeros((h, w))
    # para cada posição (i, j), some img[i:i+k, j:j+k] * filtro
    return saida

img = np.array([[0, 0, 0, 9, 9, 9]] * 5, dtype=float)
borda_vertical = np.array([[-1, 0, 1]] * 3, dtype=float)
print(conv2d(img, borda_vertical))
''',
            [("Formato (3, 4)", "assert conv2d(img, borda_vertical).shape == (3, 4)"),
             ("Destaca a borda", "import numpy as np\nr = conv2d(img, borda_vertical)\nassert np.allclose(r[0], [0, 27, 27, 0]), f'linha = {r[0]}'")],
            '''
import numpy as np

def conv2d(img, filtro):
    k = filtro.shape[0]
    h, w = img.shape[0] - k + 1, img.shape[1] - k + 1
    saida = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            saida[i, j] = (img[i:i + k, j:j + k] * filtro).sum()
    return saida

img = np.array([[0, 0, 0, 9, 9, 9]] * 5, dtype=float)
borda_vertical = np.array([[-1, 0, 1]] * 3, dtype=float)
print(conv2d(img, borda_vertical))
''', ["Dois laços em i e j; multiplique o pedaço da imagem pelo filtro e some."]),
        lab("Uma CNN para o CIFAR-10", '''
import torch
from torch import nn

cnn = nn.Sequential(
    nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),   # 32x32 -> 16x16
    nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),  # 16x16 -> 8x8
    nn.Flatten(), nn.Linear(64 * 8 * 8, 10),
)
print(cnn(torch.randn(8, 3, 32, 32)).shape)
''', corpo="<p>Rode no Colab e acompanhe o tutorial oficial do PyTorch para treinar:</p>", exps=["Quantos parâmetros tem a primeira convolução? (3 × 3 × 3 × 32 + 32)"]),
        erros([("Errar o tamanho da camada linear depois do <code>Flatten</code>.", "Calcule o tamanho da saída das convoluções ou imprima o <code>shape</code>."), ("Imagens sem normalização.", "Pixels de 0 a 255 atrapalham o treino. Normalize para média 0 e desvio 1."), ("Treinar CNN do zero com poucas imagens.", "Use transfer learning (próxima aula).")]),
        ponte("Visão nos modelos multimodais", "<p>Modelos multimodais que “veem” imagens usam Vision Transformers, que cortam a imagem em pedaços (patches) e os tratam como tokens. Mas a ideia de padrões locais que se combinam em conceitos maiores vem das CNNs, e elas continuam dominando em celulares e câmeras.</p>"),
        quiz([
            ("Entrada 32 × 32, filtro 3 × 3, sem padding, passo 1. Saída:", ["32 × 32", "30 × 30", "29 × 29"], 1, "(32 − 3)/1 + 1 = 30."),
            ("Para que serve o max pooling?", ["Aumentar a imagem.", "Reduzir o tamanho mantendo as ativações mais fortes.", "Normalizar."], 1, "Resume regiões."),
            ("Por que CNNs usam poucos parâmetros?", ["Os filtros são compartilhados em todas as posições.", "Usam imagens pequenas.", "Não têm pesos."], 0, "Compartilhamento."),
        ]),
    ],
    ["Convolução: filtros pequenos deslizando pela imagem.", "Camadas iniciais acham bordas; as finais, objetos.", "Pooling reduz; a saída é calculada por (n + 2p − k)/s + 1."],
    "Transfer learning.",
    livro=("D2L:chapter_convolutional-neural-networks/conv-layer", "Seção 7.2, “Convolutions for Images”", "Como o livro aprende um filtro de borda a partir dos dados?"))

AULAS["Transfer learning"] = aula(
    25,
    "Treinar uma rede de visão do zero pede milhões de imagens e dias de GPU. Ou você pode pegar uma rede que já aprendeu a ver (bordas, texturas, formas) e ensinar só a parte final a reconhecer as suas classes, com algumas centenas de fotos.",
    ["reaproveitar modelos pré-treinados;", "congelar camadas e trocar a cabeça;", "saber quando fazer ajuste fino completo."],
    ["CNNs para imagens."],
    [
        chute("Você tem 300 fotos de 3 tipos de folhas doentes. Qual o melhor caminho?", ["Treinar uma CNN grande do zero.", "Pegar uma rede pré-treinada no ImageNet e treinar só a última camada.", "Desistir: são poucas fotos."], 1,
              ["300 fotos não ensinam a ver do zero.", "Isso! A rede já sabe extrair características; você só ensina a decisão final.", "Com transfer learning, 300 é bastante."],
              "Poucos dados → congele quase tudo. Mais dados → descongele mais."),
        concreto("O cozinheiro experiente", "<p>Um chef que já domina técnicas (cortar, refogar, temperar) aprende uma culinária nova em semanas. Ninguém o ensina a segurar a faca de novo. O modelo pré-treinado é o chef; você só ensina o cardápio novo.</p>"),
        nota("As estratégias", [
            ("Extrator de características", "congelar tudo", "Treina só a nova cabeça. Rápido; ótimo com poucos dados."),
            ("Ajuste fino (fine-tuning)", "descongelar algumas camadas", "Taxa de aprendizado pequena para não destruir o que já foi aprendido."),
            ("<code>p.requires_grad = False</code>", "congelar no PyTorch", "O otimizador não muda esses pesos."),
            ("Mesma normalização do pré-treino", "detalhe crucial", "Use as médias e desvios que o modelo original usou."),
        ]),
        lab("Trocando a cabeça de uma ResNet", '''
import torch
from torch import nn
from torchvision import models

modelo = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
for p in modelo.parameters():
    p.requires_grad = False                      # congela tudo
modelo.fc = nn.Linear(modelo.fc.in_features, 3)  # nova cabeça: 3 classes (treinável)

treinaveis = sum(p.numel() for p in modelo.parameters() if p.requires_grad)
print("parâmetros treináveis:", treinaveis)
otimizador = torch.optim.AdamW(modelo.fc.parameters(), lr=1e-3)
''', corpo="<p>Rode no Colab:</p>", exps=["Quantos parâmetros são treináveis de um total de ~11 milhões?", "Descongele o <code>layer4</code> e use lr=1e-4 nele."]),
        cod("Quantos parâmetros treinar?", "Uma rede pré-treinada tem as camadas abaixo (número de parâmetros). Calcule quantos parâmetros são treináveis ao congelar tudo e treinar só a nova cabeça de 512 → 3 (com viés).",
            '''
camadas = {"conv": 1_700_000, "layer1": 150_000, "layer2": 525_000, "layer3": 2_100_000, "layer4": 8_400_000}

cabeca = 0
total_treinavel = 0
fracao = 0.0
print(cabeca, total_treinavel, round(fracao, 5))
''',
            [("Cabeça", "assert cabeca == 1539"), ("Total treinável = cabeça", "assert total_treinavel == cabeca"), ("Fração", "assert abs(fracao - 1539 / (sum(camadas.values()) + 1539)) < 1e-12")],
            '''
camadas = {"conv": 1_700_000, "layer1": 150_000, "layer2": 525_000, "layer3": 2_100_000, "layer4": 8_400_000}

cabeca = 512 * 3 + 3
total_treinavel = cabeca
fracao = cabeca / (sum(camadas.values()) + cabeca)
print(cabeca, total_treinavel, round(fracao, 5))
''', ["Cabeça: 512 × 3 + 3."]),
        erros([("Taxa de aprendizado alta no ajuste fino.", "Destrói o que a rede sabia. Use 10 a 100 vezes menor."), ("Normalização diferente da usada no pré-treino.", "As entradas ficam “estranhas” para a rede."), ("Domínio muito diferente (raio-X × fotos comuns).", "Funciona, mas descongele mais camadas.")]),
        ponte("Transfer learning é a base dos LLMs", "<p>Todo o ecossistema de LLMs é transfer learning: um modelo pré-treinado gigantesco, ajustado (fine-tuning) ou adaptado com LoRA para tarefas específicas. A pergunta desta aula continua igual: quanto ajustar sem destruir o que já foi aprendido?</p>"),
        quiz([
            ("Por que transfer learning funciona com poucos dados?", ["Porque a rede já aprendeu características gerais.", "Porque usa menos camadas.", "Porque não treina nada."], 0, "Reaproveita conhecimento."),
            ("Congelar camadas significa:", ["Apagá-las.", "Não atualizar seus pesos no treino.", "Torná-las mais rápidas."], 1, "<code>requires_grad = False</code>."),
            ("No ajuste fino, a taxa de aprendizado deve ser:", ["Maior que no treino do zero.", "Menor.", "Igual."], 1, "Ajustes delicados."),
        ]),
    ],
    ["Reaproveite redes pré-treinadas e troque a cabeça.", "Poucos dados: congele; mais dados: descongele com taxa pequena.", "Use a normalização original."],
    "RNNs e LSTMs para sequências.",
    livro=("D2L:chapter_computer-vision/fine-tuning", "Seção 14.2, “Fine-Tuning”", "Que taxas de aprendizado o livro usa para a cabeça e para o resto?"))

AULAS["RNNs e LSTMs para sequências"] = aula(
    30,
    "Para entender uma frase, a ordem das palavras importa: “cachorro morde homem” não é notícia; “homem morde cachorro” é. Redes recorrentes leem uma palavra por vez e carregam uma memória do que veio antes. Foram o estado da arte em texto até a chegada dos Transformers.",
    ["entender o estado oculto de uma RNN;", "saber por que RNNs simples esquecem;", "entender as portas de uma LSTM."],
    ["Neurônio, ativações e backpropagation."],
    [
        chute("Qual o principal problema de uma RNN simples com textos longos?", ["Fica rápida demais.", "Esquece o começo: os gradientes somem ao voltar muitos passos.", "Não aceita palavras novas."], 1,
              ["Ao contrário: é lenta, por ler um passo por vez.", "Isso! Multiplicar derivadas a cada passo faz o sinal do início sumir. A LSTM foi criada para isso.", "Isso depende do vocabulário, não da RNN."],
              "Memória curta e treino sequencial (lento) abriram caminho para a atenção."),
        concreto("Ler um livro com um caderninho", "<p>A cada página, você atualiza um resumo no caderninho e esquece a página. Depois de 300 páginas, detalhes do início sumiram. A LSTM tem um caderninho melhor: decide o que apagar, o que anotar e o que consultar.</p>"),
        nota("As fórmulas", [
            (r"$h_t = \tanh(W_x x_t + W_h h_{t-1} + b)$", "RNN", "O estado novo mistura a entrada atual e o estado anterior."),
            ("Porta de esquecimento", "LSTM", "Decide o que apagar da memória."),
            ("Porta de entrada", "LSTM", "Decide o que anotar."),
            ("Porta de saída", "LSTM", "Decide o que mostrar desta memória."),
            ("GRU", "versão simplificada", "Duas portas; parecida em desempenho."),
        ], rot="Agora sim, as fórmulas"),
        cod("Uma RNN lendo uma sequência", "Implemente o passo da RNN e processe a sequência inteira, guardando o estado final. Depois veja quanto o primeiro elemento ainda influencia esse estado.",
            '''
import numpy as np

def passo(x, h, Wx, Wh, b):
    return h

rng = np.random.default_rng(0)
Wx, Wh, b = rng.normal(0, 0.3, (1, 4)), rng.normal(0, 0.3, (4, 4)), np.zeros(4)

def ler(seq):
    h = np.zeros(4)
    for x in seq:
        h = passo(np.array([x]), h, Wx, Wh, b)
    return h

base = [0.0] * 20
mudado = [1.0] + [0.0] * 19
print(np.abs(ler(base) - ler(mudado)).max())
''',
            [("Passo correto", "import numpy as np\nh = passo(np.array([1.0]), np.zeros(4), Wx, Wh, b)\nassert np.allclose(h, np.tanh(np.array([1.0]) @ Wx + np.zeros(4) @ Wh + b))"),
             ("Influência do primeiro elemento quase some", "import numpy as np\nassert np.abs(ler([0.0] * 20) - ler([1.0] + [0.0] * 19)).max() < 1e-3")],
            '''
import numpy as np

def passo(x, h, Wx, Wh, b):
    return np.tanh(x @ Wx + h @ Wh + b)

rng = np.random.default_rng(0)
Wx, Wh, b = rng.normal(0, 0.3, (1, 4)), rng.normal(0, 0.3, (4, 4)), np.zeros(4)

def ler(seq):
    h = np.zeros(4)
    for x in seq:
        h = passo(np.array([x]), h, Wx, Wh, b)
    return h

base = [0.0] * 20
mudado = [1.0] + [0.0] * 19
print(np.abs(ler(base) - ler(mudado)).max())
''', ["<code>np.tanh(x @ Wx + h @ Wh + b)</code>"], exp="<p>Mudar o primeiro elemento quase não altera o estado final: é a memória curta da RNN simples.</p>"),
        erros([("Usar RNN simples para textos longos.", "Use LSTM/GRU ou, hoje, um Transformer."), ("Esquecer de recortar gradientes.", "RNNs também sofrem com gradientes que explodem: <code>clip_grad_norm_</code>."), ("Esperar paralelismo.", "RNNs leem um passo por vez; por isso treinam devagar em GPU.")]),
        ponte("Por que os Transformers venceram", "<p>Atenção lê todas as palavras ao mesmo tempo (paralelismo na GPU) e liga qualquer palavra a qualquer outra diretamente (sem memória que se apaga). Curiosamente, arquiteturas recentes como Mamba e RWKV trazem de volta ideias recorrentes para lidar com contextos enormes de forma mais barata.</p>"),
        quiz([
            ("O que o estado oculto guarda?", ["Os pesos.", "Um resumo do que foi lido até agora.", "A próxima palavra."], 1, "A memória da RNN."),
            ("O que a porta de esquecimento faz?", ["Apaga a rede.", "Decide o que descartar da memória.", "Acelera o treino."], 1, "Controle da memória."),
            ("Uma vantagem do Transformer sobre a RNN:", ["Ler um token por vez.", "Processar a sequência em paralelo.", "Ter menos parâmetros sempre."], 1, "Atenção é paralela."),
        ]),
    ],
    ["RNNs leem passo a passo, carregando um estado.", "RNNs simples esquecem; LSTM/GRU usam portas.", "Transformers venceram pelo paralelismo e pelas ligações diretas."],
    "Tensores e autograd no PyTorch.",
    livro=("D2L:chapter_recurrent-modern/lstm", "Seção 10.1, “Long Short-Term Memory (LSTM)”", "Como o livro desenha as portas da LSTM?"))
