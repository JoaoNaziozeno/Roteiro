# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 4 (parte B): PyTorch na prática e mais arquiteturas."""
from lesson_factory import *

AULAS = {}

AULAS["Tensores e autograd"] = aula(
    30,
    "No PyTorch, tudo é tensor: imagens, textos, pesos. E todo tensor pode lembrar como foi calculado. Quando você chama <code>backward()</code>, o PyTorch percorre esse histórico de trás para frente e calcula todos os gradientes sozinho. É a retropropagação automática.",
    ["criar e operar tensores como arrays do NumPy;", "usar <code>requires_grad</code> e <code>backward</code>;", "entender o grafo computacional."],
    ["NumPy e backpropagation."],
    [
        chute("Depois de <code>y = x ** 2</code> com x = 3 (com <code>requires_grad=True</code>) e <code>y.backward()</code>, quanto vale <code>x.grad</code>?", ["3", "6", "9"], 1,
              ["Isso é o próprio x.", "Isso! A derivada de x² é 2x = 6.", "Isso é o valor de y."],
              "O autograd calcula exatamente as derivadas que você calcularia à mão."),
        concreto("A receita com rastreio", "<p>Imagine uma calculadora que anota cada operação feita. No fim, você pergunta: “quanto o resultado muda se eu mexer neste número do começo?”. Ela relê as anotações de trás para frente e responde. Esse caderno de anotações é o grafo computacional.</p>"),
        nota("O essencial", [
            ("<code>torch.tensor([1.0, 2.0])</code>", "tensor", "Como um array do NumPy, mas pode ir para a GPU e calcular gradientes."),
            ("<code>requires_grad=True</code>", "rastrear", "Pede ao PyTorch para registrar as operações."),
            ("<code>perda.backward()</code>", "retropropagar", "Preenche <code>.grad</code> de todos os tensores rastreados."),
            ("<code>with torch.no_grad():</code>", "desligar rastreio", "Para avaliar e atualizar pesos sem criar grafo."),
            ("<code>otimizador.zero_grad()</code>", "zerar", "Gradientes se acumulam: zere a cada passo."),
        ]),
        cod("Um mini-autograd", "Para entender o que o PyTorch faz, complete o <code>backward</code> desta classe que rastreia soma e multiplicação. Ela calcula o gradiente de f = a·b + a.",
            '''
class Valor:
    def __init__(self, v, pais=(), op=""):
        self.v, self.grad, self.pais, self.op = v, 0.0, pais, op

    def __add__(self, o): return Valor(self.v + o.v, (self, o), "+")
    def __mul__(self, o): return Valor(self.v * o.v, (self, o), "*")

    def backward(self, g=1.0):
        self.grad += g
        if self.op == "+":
            pass  # repasse g para os dois pais
        elif self.op == "*":
            pass  # cada pai recebe g vezes o valor do outro

a, b = Valor(2.0), Valor(3.0)
f = a * b + a
f.backward()
print(f.v, a.grad, b.grad)
''',
            [("Valor de f", "assert f.v == 8.0"), ("df/da = b + 1 = 4", "assert a.grad == 4.0, f'a.grad = {a.grad}'"), ("df/db = a = 2", "assert b.grad == 2.0, f'b.grad = {b.grad}'")],
            '''
class Valor:
    def __init__(self, v, pais=(), op=""):
        self.v, self.grad, self.pais, self.op = v, 0.0, pais, op

    def __add__(self, o): return Valor(self.v + o.v, (self, o), "+")
    def __mul__(self, o): return Valor(self.v * o.v, (self, o), "*")

    def backward(self, g=1.0):
        self.grad += g
        if self.op == "+":
            self.pais[0].backward(g)
            self.pais[1].backward(g)
        elif self.op == "*":
            x, y = self.pais
            x.backward(g * y.v)
            y.backward(g * x.v)

a, b = Valor(2.0), Valor(3.0)
f = a * b + a
f.backward()
print(f.v, a.grad, b.grad)
''', ["Na soma, a derivada local é 1 para os dois lados.", "No produto, cada lado recebe g vezes o valor do outro."],
            exp="<p>Note o <code>+=</code>: como <code>a</code> aparece duas vezes, os gradientes se somam. É por isso que o PyTorch acumula e pede <code>zero_grad()</code>. Essa ideia é a do micrograd, do Andrej Karpathy.</p>"),
        lab("Autograd de verdade", '''
import torch

w = torch.tensor(2.0, requires_grad=True)
x, y = torch.tensor(3.0), torch.tensor(10.0)
perda = (w * x - y) ** 2
perda.backward()
print(perda.item(), w.grad.item())   # 16 e 2*(6-10)*3 = -24
''', corpo="<p>Rode no Colab:</p>", exps=["Rode <code>perda.backward()</code> de novo (recalculando a perda) sem zerar. O que acontece com <code>w.grad</code>?"]),
        erros([("Esquecer <code>zero_grad()</code>.", "Os gradientes se somam entre passos e o treino enlouquece."), ("Atualizar pesos fora de <code>torch.no_grad()</code>.", "A atualização entra no grafo. Use o otimizador ou o bloco <code>no_grad</code>."), ("Tensores em dispositivos diferentes.", "Erro “expected all tensors to be on the same device”: mova tudo para a GPU.")]),
        ponte("O motor de todo deep learning", "<p>Treinar um LLM com centenas de bilhões de parâmetros usa exatamente este mecanismo: forward constrói o grafo, <code>backward</code> calcula os gradientes, o otimizador atualiza. Bibliotecas como JAX fazem o mesmo com outra filosofia.</p>"),
        quiz([
            ("O que <code>backward()</code> faz?", ["Desfaz a última operação.", "Calcula os gradientes de todos os tensores rastreados.", "Volta uma época."], 1, "Retropropagação automática."),
            ("Por que zerar os gradientes a cada passo?", ["Porque eles se acumulam.", "Para economizar memória.", "Não é necessário."], 0, "<code>+=</code> no backward."),
            ("Para que serve <code>torch.no_grad()</code>?", ["Desligar o rastreio em avaliação e atualizações.", "Apagar o modelo.", "Treinar mais rápido sempre."], 0, "Sem grafo."),
        ]),
    ],
    ["Tensores são arrays que podem ir para a GPU e rastrear operações.", "<code>backward</code> percorre o grafo e preenche os gradientes.", "Zere gradientes; avalie dentro de <code>no_grad</code>."],
    "Datasets e DataLoaders.",
    livro=("D2L:chapter_preliminaries/autograd", "Seção 2.5, “Automatic Differentiation”", "Como o livro explica o acúmulo de gradientes?"))

AULAS["Datasets e DataLoaders"] = aula(
    25,
    "Uma rede não lê a pasta inteira de uma vez: recebe lotes, embaralhados a cada época, carregados enquanto a GPU trabalha no lote anterior. No PyTorch, isso é dividido em duas peças: o Dataset (como pegar um exemplo) e o DataLoader (como montar os lotes).",
    ["escrever um <code>Dataset</code> com <code>__len__</code> e <code>__getitem__</code>;", "configurar <code>batch_size</code>, <code>shuffle</code> e <code>num_workers</code>;", "aplicar transformações por exemplo."],
    ["Classes (Fase 1), geradores e tensores."],
    [
        chute("Por que embaralhar os dados a cada época?", ["Para o treino ficar mais lento.", "Para os lotes não seguirem sempre a mesma ordem, o que pode enviesar o aprendizado.", "Para economizar memória."], 1,
              ["Não tem relação com velocidade.", "Isso! Se os dados estão ordenados por classe, lotes inteiros teriam uma classe só.", "Não economiza."],
              "<code>shuffle=True</code> no treino; <code>False</code> na validação."),
        concreto("O garçom e a cozinha", "<p>O Dataset é a cozinha: sabe preparar o prato número 37 quando pedido. O DataLoader é o garçom: junta pratos em bandejas (lotes), em ordem sorteada, e vai trazendo enquanto você come.</p>"),
        nota("As duas peças", [
            ("<code>__len__</code>", "quantos exemplos", "O tamanho do dataset."),
            ("<code>__getitem__(i)</code>", "o exemplo i", "Lê, transforma e devolve <code>(x, y)</code>."),
            ("<code>DataLoader(ds, batch_size=32, shuffle=True)</code>", "lotes", "Agrupa e embaralha."),
            ("<code>num_workers=4</code>", "paralelo", "Prepara os próximos lotes enquanto a GPU treina."),
        ]),
        cod("Seu próprio Dataset e DataLoader", "Complete o <code>Dataset</code> e o gerador <code>carregar</code>, que embaralha os índices (com a semente) e entrega lotes de exemplos.",
            '''
import random

class MeuDataset:
    def __init__(self, xs, ys):
        self.xs, self.ys = xs, ys
    def __len__(self):
        return 0
    def __getitem__(self, i):
        return None

def carregar(ds, tamanho, embaralhar=True, semente=0):
    idx = list(range(len(ds)))
    # embaralhe se pedido e entregue lotes [ds[i] for i in pedaço]
    yield []

ds = MeuDataset(list(range(10)), [i % 2 for i in range(10)])
lotes = list(carregar(ds, 4))
print([len(l) for l in lotes])
''',
            [("Tamanho e item", "assert len(ds) == 10 and ds[3] == (3, 1)"), ("Lotes 4, 4, 2", "assert [len(l) for l in carregar(ds, 4)] == [4, 4, 2]"),
             ("Todos os exemplos aparecem uma vez", "assert sorted(x for l in carregar(ds, 3) for x, _ in l) == list(range(10))"),
             ("Embaralha", "assert [x for x, _ in next(iter(carregar(ds, 10)))] != list(range(10))"), ("Sem embaralhar mantém a ordem", "assert [x for x, _ in next(iter(carregar(ds, 10, embaralhar=False)))] == list(range(10))")],
            '''
import random

class MeuDataset:
    def __init__(self, xs, ys):
        self.xs, self.ys = xs, ys
    def __len__(self):
        return len(self.xs)
    def __getitem__(self, i):
        return self.xs[i], self.ys[i]

def carregar(ds, tamanho, embaralhar=True, semente=0):
    idx = list(range(len(ds)))
    if embaralhar:
        random.Random(semente).shuffle(idx)
    for i in range(0, len(idx), tamanho):
        yield [ds[j] for j in idx[i:i + tamanho]]

ds = MeuDataset(list(range(10)), [i % 2 for i in range(10)])
lotes = list(carregar(ds, 4))
print([len(l) for l in lotes])
''', ["<code>__getitem__</code> devolve <code>(self.xs[i], self.ys[i])</code>.", "Embaralhe os índices com <code>random.Random(semente).shuffle(idx)</code> e fatie."]),
        erros([("Carregar todas as imagens na memória no <code>__init__</code>.", "Guarde os caminhos e leia no <code>__getitem__</code>."), ("<code>shuffle=True</code> na validação.", "Não erra, mas atrapalha comparar resultados."), ("GPU ociosa esperando dados.", "Aumente <code>num_workers</code> e use <code>pin_memory=True</code>.")]),
        ponte("Dados de LLMs", "<p>No treino de LLMs, os textos são tokenizados e cortados em blocos de tamanho fixo, e o DataLoader entrega lotes de blocos. Datasets do Hugging Face fazem isso com <code>streaming=True</code>, lendo da internet aos poucos, sem baixar terabytes.</p>"),
        quiz([
            ("O que <code>__getitem__</code> devolve?", ["O dataset inteiro.", "Um exemplo (entrada e rótulo).", "Um lote."], 1, "O DataLoader monta os lotes."),
            ("Para que serve <code>num_workers</code>?", ["Preparar lotes em paralelo.", "Usar mais GPUs.", "Embaralhar."], 0, "Evita GPU ociosa."),
            ("Onde embaralhar?", ["No treino.", "Na validação e no teste.", "Em lugar nenhum."], 0, "Treino com shuffle."),
        ]),
    ],
    ["Dataset sabe pegar um exemplo; DataLoader monta lotes.", "Embaralhe o treino a cada época.", "Leia sob demanda e em paralelo."],
    "Loop de treino e avaliação.",
    livro=("D2L:chapter_linear-regression/synthetic-regression-data", "Seção 3.3, sobre leitura de dados em minibatches", "Como o livro implementa um iterador de lotes do zero?"))

AULAS["Loop de treino e avaliação"] = aula(
    35,
    "Cinco linhas se repetem em todo treino de rede neural do mundo: prever, calcular a perda, zerar os gradientes, retropropagar, dar o passo. Em volta delas, a avaliação a cada época diz se o modelo está realmente aprendendo.",
    ["escrever o loop de treino padrão;", "avaliar corretamente com <code>eval()</code> e <code>no_grad()</code>;", "registrar perdas para ver a curva de aprendizado."],
    ["Tensores e autograd; DataLoaders; otimizadores."],
    [
        chute("Qual a ordem certa dentro do loop?", ["backward, zero_grad, step, perda", "previsão, perda, zero_grad, backward, step", "step, backward, perda, previsão"], 1,
              ["Fora de ordem.", "Isso! Prever, medir o erro, limpar gradientes antigos, calcular os novos e atualizar.", "Fora de ordem."],
              "Decore as cinco linhas: elas não mudam."),
        concreto("O treino do atleta", "<p>Cada repetição: tentar (forward), cronometrar (perda), ouvir a correção do técnico (backward) e ajustar o movimento (step). No fim do dia, uma prova sem correção (validação) mostra se o atleta melhorou de verdade.</p>"),
        nota("O loop padrão", [
            ("<code>modelo.train()</code>", "modo treino", "Liga dropout e o modo de treino do BatchNorm."),
            ("<code>perda = criterio(modelo(x), y)</code>", "forward + perda", "Previsão e erro do lote."),
            ("<code>opt.zero_grad(); perda.backward(); opt.step()</code>", "aprender", "Limpa, calcula, atualiza."),
            ("<code>modelo.eval()</code> + <code>torch.no_grad()</code>", "avaliar", "Sem dropout e sem grafo."),
        ]),
        cod("Um loop completo com NumPy", "Treine uma regressão logística com lotes de 16 por 30 épocas e registre a perda média de cada época em <code>historico</code>. A perda deve cair e a acurácia final passar de 90%.",
            '''
import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(size=(400, 2))
y = (X[:, 0] - X[:, 1] > 0).astype(float)
w, b = np.zeros(2), 0.0
historico = []

for epoca in range(30):
    idx = rng.permutation(len(X))
    perdas = []
    for i in range(0, len(X), 16):
        lote = idx[i:i + 16]
        xb, yb = X[lote], y[lote]
        p = 1 / (1 + np.exp(-(xb @ w + b)))
        perdas.append(-np.mean(yb * np.log(p + 1e-9) + (1 - yb) * np.log(1 - p + 1e-9)))
        # gradientes: dw = xb.T @ (p - yb) / len(lote); db = média de (p - yb)
        # atualize w e b com taxa 0.5
    historico.append(np.mean(perdas))

acc = (((X @ w + b) > 0) == y).mean()
print(round(historico[0], 3), round(historico[-1], 3), acc)
''',
            [("A perda cai", "assert historico[-1] < historico[0] / 3, f'{historico[0]:.3f} -> {historico[-1]:.3f}'"), ("Acurácia acima de 90%", "assert acc > 0.9, f'acc = {acc}'"), ("30 épocas registradas", "assert len(historico) == 30")],
            '''
import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(size=(400, 2))
y = (X[:, 0] - X[:, 1] > 0).astype(float)
w, b = np.zeros(2), 0.0
historico = []

for epoca in range(30):
    idx = rng.permutation(len(X))
    perdas = []
    for i in range(0, len(X), 16):
        lote = idx[i:i + 16]
        xb, yb = X[lote], y[lote]
        p = 1 / (1 + np.exp(-(xb @ w + b)))
        perdas.append(-np.mean(yb * np.log(p + 1e-9) + (1 - yb) * np.log(1 - p + 1e-9)))
        dw = xb.T @ (p - yb) / len(lote)
        db = np.mean(p - yb)
        w -= 0.5 * dw
        b -= 0.5 * db
    historico.append(np.mean(perdas))

acc = (((X @ w + b) > 0) == y).mean()
print(round(historico[0], 3), round(historico[-1], 3), acc)
''', ["<code>dw = xb.T @ (p - yb) / len(lote)</code>, <code>db = np.mean(p - yb)</code>.", "<code>w -= 0.5 * dw</code>."]),
        lab("O mesmo loop no PyTorch", '''
import torch
from torch import nn

def treinar(modelo, treino, valid, epocas=10, lr=1e-3):
    opt = torch.optim.AdamW(modelo.parameters(), lr=lr)
    criterio = nn.CrossEntropyLoss()
    for epoca in range(epocas):
        modelo.train()
        for x, y in treino:
            perda = criterio(modelo(x), y)
            opt.zero_grad()
            perda.backward()
            opt.step()
        modelo.eval()
        acertos = total = 0
        with torch.no_grad():
            for x, y in valid:
                acertos += (modelo(x).argmax(1) == y).sum().item()
                total += len(y)
        print(f"época {epoca}: perda {perda.item():.3f}, acc valid {acertos / total:.3f}")
''', corpo="<p>O esqueleto que você vai reutilizar em todos os projetos de deep learning:</p>", exps=["Teste com o MNIST (<code>torchvision.datasets.MNIST</code>) e a rede da primeira aula da fase."]),
        erros([("Avaliar em modo de treino.", "Dropout ligado deixa as métricas erradas."), ("Imprimir a perda de um lote só.", "Oscila muito. Registre a média da época."), ("Treinar sem conjunto de validação.", "Você não vê o overfitting chegando.")]),
        ponte("O loop dos LLMs", "<p>O treino de um LLM é este mesmo loop, com detalhes de escala: acúmulo de gradientes entre lotes, precisão mista, recorte de gradientes, agendamento da taxa e checkpoints frequentes. As próximas aulas da fase tratam de cada um.</p>"),
        quiz([
            ("Onde fica o <code>zero_grad()</code>?", ["Depois do step.", "Antes do backward.", "Fora do loop."], 1, "Limpa antes de calcular os novos."),
            ("O que <code>modelo.eval()</code> muda?", ["Desliga dropout e fixa o BatchNorm.", "Congela os pesos para sempre.", "Nada."], 0, "Modo de inferência."),
            ("Por que registrar a perda de validação?", ["Para ver se o modelo generaliza.", "Para treinar mais rápido.", "Não é útil."], 0, "Detecta overfitting."),
        ]),
    ],
    ["Prever, perda, zero_grad, backward, step.", "Avalie com <code>eval()</code> e <code>no_grad()</code>.", "Registre perdas médias para ver a curva."],
    "Treinar em GPU (Colab).",
    livro=("D2L:chapter_linear-classification/softmax-regression-concise", "Seção 4.5, “Concise Implementation of Softmax Regression”", "Como o livro organiza o loop de treino?"))

AULAS["Treinar em GPU (Colab)"] = aula(
    20,
    "Uma GPU tem milhares de núcleos pequenos que multiplicam matrizes em paralelo. Para redes neurais, isso significa treinar em minutos o que levaria horas na CPU. No Colab, ela é gratuita: basta saber ligá-la e mover os dados para lá.",
    ["ativar a GPU no Colab e conferir com <code>torch.cuda.is_available()</code>;", "mover modelo e dados com <code>.to(device)</code>;", "diagnosticar falta de memória."],
    ["Loop de treino e avaliação."],
    [
        chute("Você moveu o modelo para a GPU, mas os dados continuam na CPU. O que acontece?", ["Funciona, só mais devagar.", "Dá erro: os tensores precisam estar no mesmo dispositivo.", "O PyTorch move sozinho."], 1,
              ["Não chega a rodar.", "Isso! “Expected all tensors to be on the same device”. Mova cada lote no loop.", "Ele não move automaticamente."],
              "Modelo uma vez; dados a cada lote."),
        concreto("Um pintor e mil pintores", "<p>Pintar um muro de mil tijolos: um pintor muito rápido (CPU) pinta um por vez; mil pintores lentos (GPU) pintam todos ao mesmo tempo. Multiplicar matrizes é pintar muros: a GPU vence com folga.</p>"),
        nota("Os comandos", [
            ("<code>device = \"cuda\" if torch.cuda.is_available() else \"cpu\"</code>", "escolher", "Código que roda nos dois."),
            ("<code>modelo.to(device)</code>", "mover o modelo", "Uma vez, antes do treino."),
            ("<code>x, y = x.to(device), y.to(device)</code>", "mover o lote", "Dentro do loop."),
            ("<code>!nvidia-smi</code>", "ver a GPU", "Memória usada e modelo da placa."),
            ("CUDA out of memory", "falta de memória", "Diminua o lote, use precisão mista ou acumule gradientes."),
        ]),
        cod("Quanto cabe na memória?", "Estime a memória de treino de um modelo: cada parâmetro em float32 ocupa 4 bytes, e o treino com Adam guarda 4 cópias (pesos, gradientes e dois momentos). Calcule em GB para 1 bilhão de parâmetros.",
            '''
def memoria_treino_gb(parametros, bytes_por_valor=4, copias=4):
    return 0.0

print(memoria_treino_gb(1_000_000_000))
''',
            [("1 bilhão ≈ 16 GB", "assert abs(memoria_treino_gb(1_000_000_000) - 16.0) < 1e-9, f'deu {memoria_treino_gb(1_000_000_000)}'"), ("Meia precisão", "assert abs(memoria_treino_gb(1_000_000_000, bytes_por_valor=2) - 8.0) < 1e-9")],
            '''
def memoria_treino_gb(parametros, bytes_por_valor=4, copias=4):
    return parametros * bytes_por_valor * copias / 1e9

print(memoria_treino_gb(1_000_000_000))
''', ["parâmetros × bytes × cópias, dividido por 10⁹."], exp="<p>E isso sem contar as ativações do lote. Por isso treinar LLMs exige várias GPUs, e inferência de modelos grandes usa quantização.</p>"),
        erros([("Esquecer de ativar a GPU no Colab.", "Ambiente de execução → Alterar tipo → GPU."), ("Converter para NumPy dentro do loop a cada passo.", "<code>.cpu().numpy()</code> sincroniza e atrasa. Faça só quando precisar."), ("Lote grande demais.", "Out of memory. Reduza e compense com acúmulo de gradientes.")]),
        ponte("GPUs e o custo da IA", "<p>O custo de treinar e servir LLMs é, em grande parte, custo de GPU. Saber estimar memória e tempo é o que permite decidir entre treinar, ajustar com LoRA ou só usar uma API.</p>"),
        quiz([
            ("O que <code>.to(device)</code> faz?", ["Salva o modelo.", "Move o tensor ou modelo para o dispositivo (CPU/GPU).", "Treina."], 1, "Mesmo dispositivo para tudo."),
            ("Por que a GPU acelera redes neurais?", ["Tem um núcleo muito rápido.", "Faz milhares de operações em paralelo.", "Usa menos energia."], 1, "Multiplicação de matrizes."),
            ("Erro “CUDA out of memory”. Primeira tentativa:", ["Aumentar o lote.", "Diminuir o lote.", "Trocar de otimizador."], 1, "Menos memória por passo."),
        ]),
    ],
    ["Ative a GPU e confira com <code>torch.cuda.is_available()</code>.", "Modelo e dados no mesmo dispositivo.", "Estime memória: parâmetros × bytes × cópias."],
    "Autoencoders.",
    livro=("D2L:chapter_builders-guide/use-gpu", "Seção 6.7, “GPUs”", "Como o livro copia tensores entre dispositivos?"))

AULAS["Autoencoders"] = aula(
    25,
    "Um autoencoder aprende a comprimir uma imagem num punhado de números e depois reconstruí-la. Para conseguir, ele precisa descobrir o essencial. Esse “essencial” comprimido é útil para remover ruído, achar anomalias e, como você verá, gerar imagens.",
    ["entender codificador, gargalo e decodificador;", "usar o erro de reconstrução;", "aplicar autoencoders em anomalias e remoção de ruído."],
    ["Loop de treino e PCA."],
    [
        chute("Um autoencoder treinado só com fotos de peças boas recebe uma peça defeituosa. O que acontece com o erro de reconstrução?", ["Fica baixo.", "Fica alto: ele não sabe reconstruir o que nunca viu.", "Fica zero."], 1,
              ["Ele só aprendeu o “normal”.", "Isso! Erro alto = algo diferente do normal: detecção de anomalias.", "Zero só para cópia perfeita."],
              "Erro de reconstrução é uma pontuação de anomalia natural."),
        concreto("O resumo do livro", "<p>Resumir um livro em uma página obriga a guardar só o enredo principal. Alguém que lê o resumo consegue recontar a história, sem os detalhes. O codificador faz o resumo; o decodificador reconta.</p>"),
        nota("As partes", [
            ("Codificador", "compressão", "Transforma a entrada (ex.: 784 pixels) num vetor pequeno (ex.: 16 números)."),
            ("Gargalo / espaço latente", "o resumo", "Onde fica a representação comprimida."),
            ("Decodificador", "reconstrução", "Tenta recriar a entrada a partir do resumo."),
            ("Perda de reconstrução", "MSE", "Diferença entre entrada e reconstrução."),
            ("VAE", "autoencoder variacional", "O espaço latente vira uma distribuição: permite gerar exemplos novos."),
        ]),
        cod("Um autoencoder linear", "Um autoencoder linear de 3 → 1 → 3 aprende o mesmo que o PCA. Use o SVD para obter o codificador e reconstrua os dados; depois compare o erro de um ponto normal com o de um anômalo.",
            '''
import numpy as np

rng = np.random.default_rng(0)
t = rng.normal(size=200)
X = np.column_stack([t, 2 * t, -t]) + rng.normal(0, 0.05, (200, 3))
media = X.mean(axis=0)
_, _, Vt = np.linalg.svd(X - media, full_matrices=False)
cod = Vt[:1]          # codificador: 3 -> 1

def reconstruir(x):
    return x          # codifique com cod e decodifique com cod.T (lembre da média)

def erro(x):
    return float(((x - reconstruir(x)) ** 2).sum())

print(round(erro(np.array([1.0, 2.0, -1.0])), 4), round(erro(np.array([1.0, -2.0, 1.0])), 4))
''',
            [("Ponto normal reconstruído bem", "import numpy as np\nassert erro(np.array([1.0, 2.0, -1.0])) < 0.05"), ("Anomalia tem erro bem maior", "import numpy as np\nassert erro(np.array([1.0, -2.0, 1.0])) > 50 * erro(np.array([1.0, 2.0, -1.0])) + 1")],
            '''
import numpy as np

rng = np.random.default_rng(0)
t = rng.normal(size=200)
X = np.column_stack([t, 2 * t, -t]) + rng.normal(0, 0.05, (200, 3))
media = X.mean(axis=0)
_, _, Vt = np.linalg.svd(X - media, full_matrices=False)
cod = Vt[:1]

def reconstruir(x):
    z = (x - media) @ cod.T
    return z @ cod + media

def erro(x):
    return float(((x - reconstruir(x)) ** 2).sum())

print(round(erro(np.array([1.0, 2.0, -1.0])), 4), round(erro(np.array([1.0, -2.0, 1.0])), 4))
''', ["Codificar: <code>z = (x - media) @ cod.T</code>.", "Decodificar: <code>z @ cod + media</code>."]),
        erros([("Gargalo grande demais.", "O autoencoder só copia, sem aprender o essencial."), ("Usar a reconstrução de treino para escolher o limiar de anomalia.", "Escolha com dados de validação."), ("Esperar boas imagens novas de um autoencoder comum.", "Para gerar, use VAE ou modelos de difusão.")]),
        ponte("Espaços latentes na IA generativa", "<p>O Stable Diffusion não trabalha com pixels: um autoencoder comprime a imagem num espaço latente pequeno, a difusão acontece ali, e o decodificador devolve a imagem. Sem autoencoders, gerar imagens seria lento demais.</p>"),
        quiz([
            ("O que fica no gargalo?", ["A imagem original.", "Uma representação comprimida.", "Os rótulos."], 1, "O espaço latente."),
            ("Como detectar anomalias com autoencoder?", ["Pelo erro de reconstrução alto.", "Pela acurácia.", "Pelo tamanho do arquivo."], 0, "Ele só sabe reconstruir o normal."),
            ("Um autoencoder linear equivale a:", ["K-Means.", "PCA.", "Árvore de decisão."], 1, "Mesmas direções principais."),
        ]),
    ],
    ["Autoencoder comprime e reconstrói.", "Erro de reconstrução aponta anomalias.", "Espaços latentes são a base da IA generativa de imagens."],
    "GANs.",
    livro=("UDL", "Capítulo 17, “Variational Autoencoders”", "Como o livro relaciona o VAE à geração de exemplos novos?"))

AULAS["GANs"] = aula(
    25,
    "Um falsificador e um detetive treinando juntos: o falsificador tenta criar notas falsas convincentes; o detetive tenta desmascará-las. Cada um melhora com os erros do outro, até as falsificações ficarem indistinguíveis. Essa disputa é uma GAN.",
    ["entender gerador e discriminador;", "ver a perda como um jogo de dois jogadores;", "conhecer os problemas típicos de treino."],
    ["Loop de treino e entropia cruzada."],
    [
        chute("Numa GAN, o que o gerador recebe como entrada?", ["Imagens reais.", "Ruído aleatório.", "Rótulos das classes."], 1,
              ["Quem vê as imagens reais é o discriminador.", "Isso! O gerador transforma ruído em algo que pareça real.", "GANs condicionais podem receber rótulos, mas a base é o ruído."],
              "Ruído diferente → imagem diferente."),
        concreto("Falsificador × detetive", "<p>No começo, as notas falsas são grosseiras e o detetive pega todas. O falsificador aprende o que entregou o golpe e melhora; o detetive precisa ficar mais atento. Treinam um contra o outro até o detetive acertar só metade das vezes: aí as notas falsas parecem reais.</p>"),
        nota("O jogo", [
            ("Gerador G(z)", "falsificador", "Transforma ruído z numa amostra."),
            ("Discriminador D(x)", "detetive", "Dá a probabilidade de x ser real."),
            ("Perda do D", "classificar bem", "Real → 1; falso → 0."),
            ("Perda do G", "enganar", "Quer que D(G(z)) chegue a 1."),
            ("Colapso de modo", "problema clássico", "O gerador produz sempre as mesmas poucas saídas."),
        ]),
        cod("As perdas da GAN", "Implemente as perdas com entropia cruzada binária: <code>perda_D</code> recebe as probabilidades do discriminador para reais e falsos; <code>perda_G</code>, só para os falsos.",
            '''
import numpy as np

def bce(p, alvo):
    p = np.clip(p, 1e-9, 1 - 1e-9)
    return float(-np.mean(alvo * np.log(p) + (1 - alvo) * np.log(1 - p)))

def perda_D(p_reais, p_falsos):
    return 0.0

def perda_G(p_falsos):
    return 0.0

print(perda_D(np.array([0.9, 0.8]), np.array([0.1, 0.3])), perda_G(np.array([0.1, 0.3])))
''',
            [("Perda do discriminador", "import numpy as np\nassert abs(perda_D(np.array([0.9, 0.8]), np.array([0.1, 0.3])) - (bce(np.array([0.9, 0.8]), 1) + bce(np.array([0.1, 0.3]), 0))) < 1e-9"),
             ("Perda do gerador", "import numpy as np\nassert abs(perda_G(np.array([0.1, 0.3])) - bce(np.array([0.1, 0.3]), 1)) < 1e-9"),
             ("Gerador feliz quando engana", "import numpy as np\nassert perda_G(np.array([0.99])) < perda_G(np.array([0.1]))")],
            '''
import numpy as np

def bce(p, alvo):
    p = np.clip(p, 1e-9, 1 - 1e-9)
    return float(-np.mean(alvo * np.log(p) + (1 - alvo) * np.log(1 - p)))

def perda_D(p_reais, p_falsos):
    return bce(p_reais, 1) + bce(p_falsos, 0)

def perda_G(p_falsos):
    return bce(p_falsos, 1)

print(perda_D(np.array([0.9, 0.8]), np.array([0.1, 0.3])), perda_G(np.array([0.1, 0.3])))
''', ["D quer reais → 1 e falsos → 0.", "G quer que os falsos sejam vistos como 1."]),
        erros([("Discriminador forte demais.", "O gerador não recebe gradiente útil. Equilibre os dois."), ("Treino instável e oscilante.", "É comum em GANs. Taxas pequenas, normalização e arquiteturas testadas (DCGAN) ajudam."), ("Avaliar só olhando imagens escolhidas.", "Use métricas como FID e veja muitas amostras.")]),
        ponte("GANs e difusão", "<p>As GANs dominaram a geração de imagens até cerca de 2021 (rostos fotorrealistas, transferência de estilo). Os modelos de difusão tomaram o lugar por serem mais estáveis e diversos, mas a ideia de usar um modelo para julgar outro voltou com força: LLMs avaliando LLMs.</p>"),
        quiz([
            ("Qual o papel do discriminador?", ["Gerar imagens.", "Distinguir real de falso.", "Comprimir dados."], 1, "O detetive."),
            ("O que é colapso de modo?", ["O gerador produz pouca variedade.", "O treino termina cedo.", "O discriminador para."], 0, "Sempre as mesmas saídas."),
            ("O gerador “vence” quando:", ["D(G(z)) se aproxima de 1.", "D(G(z)) se aproxima de 0.", "A perda de D é zero."], 0, "Engana o detetive."),
        ]),
    ],
    ["GAN = gerador contra discriminador.", "Perdas de entropia cruzada com alvos opostos.", "Treino instável; difusão ocupou boa parte do espaço."],
    "Modelos de difusão.",
    livro=("UDL", "Capítulo 15, “Generative Adversarial Networks”", "Que problemas de treino de GANs o livro discute?"))

AULAS["Modelos de difusão (noção)"] = aula(
    25,
    "Pegue uma foto e vá adicionando ruído até virar chiado de TV. Agora treine uma rede para desfazer um passo de ruído de cada vez. Partindo de chiado puro e repetindo esse passo, nasce uma imagem nova. É assim que funcionam Stable Diffusion, DALL·E e Midjourney.",
    ["entender o processo de adicionar ruído;", "entender o que a rede aprende a prever;", "relacionar texto e imagem na difusão guiada."],
    ["Autoencoders e loop de treino."],
    [
        chute("O que a rede de um modelo de difusão aprende a prever, na formulação mais comum?", ["A imagem final direto.", "O ruído que foi adicionado à imagem.", "O rótulo da imagem."], 1,
              ["Seria difícil demais de uma vez.", "Isso! Sabendo o ruído, dá para removê-lo um pouco e repetir.", "Não é um classificador."],
              "Gerar = remover ruído aos poucos, muitas vezes."),
        concreto("A escultura no mármore", "<p>O escultor diz que a estátua já estava no bloco: ele só tira o excesso. A difusão começa do “bloco” de ruído e, passo a passo, remove o que não faz parte da imagem, guiada pelo texto que você escreveu.</p>"),
        nota("As duas direções", [
            ("Processo direto", "adicionar ruído", "Fácil: em T passos, a imagem vira ruído puro."),
            (r"$x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon$", "atalho", "Pula direto para qualquer passo t."),
            ("Processo reverso", "remover ruído", "A rede prevê ε e o amostrador dá um passo de volta."),
            ("Guia por texto", "condicionamento", "O texto vira embedding e orienta cada passo."),
            ("Difusão latente", "eficiência", "Tudo acontece no espaço comprimido de um autoencoder."),
        ]),
        cod("O processo direto", "Implemente o atalho do processo direto e verifique que, com ᾱ perto de 1, a imagem quase não muda e, com ᾱ perto de 0, ela vira ruído.",
            '''
import numpy as np

def adicionar_ruido(x0, alfa_barra, rng):
    return x0

rng = np.random.default_rng(0)
x0 = np.ones(10000)
pouco = adicionar_ruido(x0, 0.99, rng)
muito = adicionar_ruido(x0, 0.001, rng)
print(round(pouco.mean(), 2), round(muito.mean(), 2), round(muito.std(), 2))
''',
            [("Pouco ruído preserva a imagem", "import numpy as np\np = adicionar_ruido(np.ones(10000), 0.99, np.random.default_rng(0))\nassert abs(p.mean() - np.sqrt(0.99)) < 0.01 and abs(p.std() - 0.1) < 0.01"),
             ("Muito ruído vira ruído padrão", "import numpy as np\nm = adicionar_ruido(np.ones(10000), 0.001, np.random.default_rng(0))\nassert abs(m.mean()) < 0.06 and abs(m.std() - 1) < 0.03")],
            '''
import numpy as np

def adicionar_ruido(x0, alfa_barra, rng):
    eps = rng.normal(size=x0.shape)
    return np.sqrt(alfa_barra) * x0 + np.sqrt(1 - alfa_barra) * eps

rng = np.random.default_rng(0)
x0 = np.ones(10000)
pouco = adicionar_ruido(x0, 0.99, rng)
muito = adicionar_ruido(x0, 0.001, rng)
print(round(pouco.mean(), 2), round(muito.mean(), 2), round(muito.std(), 2))
''', ["<code>np.sqrt(alfa_barra) * x0 + np.sqrt(1 - alfa_barra) * eps</code>"]),
        erros([("Achar que a difusão “cola” pedaços de imagens do treino.", "Ela aprende a distribuição; a geração parte de ruído novo."), ("Poucos passos de amostragem.", "Imagem borrada. Amostradores modernos usam 20 a 50."), ("Ignorar questões de direitos e consentimento.", "Os dados de treino e o uso das imagens geradas têm implicações legais e éticas.")]),
        ponte("Difusão além das imagens", "<p>A mesma ideia gera áudio, vídeo, estruturas de proteínas e até texto (modelos de difusão de linguagem). E quase todo modelo de imagem combina três peças que você já conhece: um autoencoder, uma rede que remove ruído e um codificador de texto.</p>"),
        quiz([
            ("O processo direto da difusão:", ["Remove ruído.", "Adiciona ruído até virar ruído puro.", "Classifica imagens."], 1, "É fixo, sem aprendizado."),
            ("Como uma imagem nova é gerada?", ["Partindo de ruído e removendo-o passo a passo.", "Copiando do treino.", "Em um único passo."], 0, "Processo reverso."),
            ("Para que serve a difusão latente?", ["Tornar o processo mais barato, num espaço comprimido.", "Aumentar a resolução.", "Remover o texto."], 0, "Usa um autoencoder."),
        ]),
    ],
    ["Difusão: adicionar ruído é fácil; a rede aprende a removê-lo.", "Gera partindo de ruído puro, passo a passo.", "Texto guia cada passo; o espaço latente deixa tudo mais barato."],
    "Redes de grafos.",
    livro=("UDL", "Capítulo 18, “Diffusion Models”", "Como o livro define o processo de codificação (encoder) da difusão?"))

AULAS["Redes de grafos (noção)"] = aula(
    20,
    "Redes sociais, moléculas, mapas de ruas: muitos dados são conexões entre coisas. Uma rede de grafos atualiza cada nó com a informação dos vizinhos, como fofoca se espalhando por uma rede de amigos.",
    ["representar dados como grafo;", "entender a troca de mensagens entre vizinhos;", "conhecer aplicações."],
    ["Neurônio, camadas e matrizes."],
    [
        chute("Depois de 2 rodadas de troca de mensagens, um nó conhece informação de quem?", ["Só dele mesmo.", "Dos vizinhos e dos vizinhos dos vizinhos.", "De todo o grafo sempre."], 1,
              ["Ele já ouviu os vizinhos.", "Isso! Cada camada amplia o alcance em um salto.", "Só com camadas suficientes."],
              "k camadas = alcance de k saltos."),
        concreto("A fofoca no bairro", "<p>Na primeira rodada, você sabe o que seus vizinhos contaram. Na segunda, eles já repassaram o que ouviram dos vizinhos deles. A rede de grafos faz isso com números, camada por camada.</p>"),
        nota("As peças", [
            ("Matriz de adjacência A", "quem liga a quem", "A[i, j] = 1 se i e j estão conectados."),
            ("Agregar", "juntar os vizinhos", "Média ou soma das representações dos vizinhos."),
            (r"$H' = \sigma(\hat A H W)$", "camada GCN", "Mistura os vizinhos (Â) e transforma (W)."),
        ]),
        cod("Uma rodada de mensagens", "Implemente a agregação: cada nó recebe a <b>média</b> dos valores dele mesmo e dos vizinhos.",
            '''
import numpy as np

A = np.array([[0, 1, 0, 0],
              [1, 0, 1, 0],
              [0, 1, 0, 1],
              [0, 0, 1, 0]], dtype=float)
H = np.array([[10.0], [0.0], [0.0], [0.0]])

def rodada(A, H):
    return H

print(rodada(A, H).ravel(), rodada(A, rodada(A, H)).ravel())
''',
            [("Uma rodada", "import numpy as np\nassert np.allclose(rodada(A, H).ravel(), [5, 10 / 3, 0, 0])"), ("Duas rodadas alcançam o nó 2", "import numpy as np\nassert rodada(A, rodada(A, H)).ravel()[2] > 0 and rodada(A, rodada(A, H)).ravel()[3] == 0")],
            '''
import numpy as np

A = np.array([[0, 1, 0, 0],
              [1, 0, 1, 0],
              [0, 1, 0, 1],
              [0, 0, 1, 0]], dtype=float)
H = np.array([[10.0], [0.0], [0.0], [0.0]])

def rodada(A, H):
    A_hat = A + np.eye(len(A))
    return (A_hat @ H) / A_hat.sum(axis=1, keepdims=True)

print(rodada(A, H).ravel(), rodada(A, rodada(A, H)).ravel())
''', ["Inclua o próprio nó: <code>A + np.eye(n)</code>.", "Some os vizinhos com <code>A_hat @ H</code> e divida pelo número de vizinhos."]),
        erros([("Camadas demais.", "Todos os nós ficam parecidos (over-smoothing)."), ("Grafos enormes inteiros na memória.", "Use amostragem de vizinhos.")]),
        ponte("Grafos em IA", "<p>Descoberta de remédios (moléculas como grafos), detecção de fraude em redes de transações e recomendação usam GNNs. E um Transformer pode ser visto como uma rede de grafos em que todo token conversa com todo token, com pesos dados pela atenção.</p>"),
        quiz([
            ("O que a matriz de adjacência representa?", ["As conexões entre os nós.", "Os pesos da rede.", "Os rótulos."], 0, "Quem liga a quem."),
            ("Duas camadas de GNN alcançam:", ["1 salto.", "2 saltos.", "Todo o grafo."], 1, "Uma por camada."),
            ("Exemplo de dado em grafo:", ["Uma molécula.", "Uma foto isolada.", "Um número."], 0, "Átomos e ligações."),
        ]),
    ],
    ["Grafos representam relações.", "GNNs trocam mensagens entre vizinhos.", "Cada camada amplia o alcance em um salto."],
    "Detecção de objetos.",
    livro=("UDL", "Capítulo 13, “Graph Neural Networks”", "Que tarefas em grafos o livro diferencia (nó, aresta, grafo)?"))

AULAS["Detecção de objetos (YOLO)"] = aula(
    25,
    "Classificar diz “tem um carro na foto”. Detectar diz “tem três carros, aqui, aqui e aqui”, com uma caixa em volta de cada um. É o que permite contar pessoas, ler placas e guiar carros autônomos.",
    ["entender caixas delimitadoras e confiança;", "calcular IoU;", "entender a supressão de não máximos (NMS)."],
    ["CNNs e métricas."],
    [
        chute("O modelo desenhou 5 caixas quase iguais em volta do mesmo cachorro. O que resolve?", ["Diminuir a imagem.", "Supressão de não máximos: manter a caixa de maior confiança e apagar as que se sobrepõem muito a ela.", "Treinar mais."], 1,
              ["Não resolve a duplicação.", "Isso! O NMS é o passo final de quase todo detector.", "Duplicatas são normais antes do NMS."],
              "IoU mede a sobreposição; o NMS usa a IoU para limpar."),
        concreto("Marcar com caneta", "<p>Para mostrar onde estão os objetos numa foto, você desenha retângulos e escreve o nome ao lado. O detector faz isso, dizendo também o quanto tem certeza de cada retângulo.</p>"),
        nota("As peças", [
            ("Caixa (x1, y1, x2, y2)", "localização", "Cantos superior esquerdo e inferior direito."),
            ("Confiança", "certeza", "Probabilidade de haver um objeto daquela classe na caixa."),
            ("IoU", "interseção sobre união", "Área em comum dividida pela área total. 1 = caixas idênticas."),
            ("NMS", "limpeza", "Remove caixas redundantes com IoU alta."),
            ("mAP", "métrica", "Precisão média em vários limiares de IoU."),
        ]),
        cod("IoU", "Implemente a IoU de duas caixas no formato (x1, y1, x2, y2).",
            '''
def iou(a, b):
    return 0.0

print(iou((0, 0, 2, 2), (1, 1, 3, 3)), iou((0, 0, 2, 2), (0, 0, 2, 2)), iou((0, 0, 1, 1), (2, 2, 3, 3)))
''',
            [("Sobreposição parcial", "assert abs(iou((0, 0, 2, 2), (1, 1, 3, 3)) - 1 / 7) < 1e-9"), ("Iguais = 1", "assert iou((0, 0, 2, 2), (0, 0, 2, 2)) == 1"), ("Separadas = 0", "assert iou((0, 0, 1, 1), (2, 2, 3, 3)) == 0")],
            '''
def iou(a, b):
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    return inter / (area_a + area_b - inter)

print(iou((0, 0, 2, 2), (1, 1, 3, 3)), iou((0, 0, 2, 2), (0, 0, 2, 2)), iou((0, 0, 1, 1), (2, 2, 3, 3)))
''', ["Interseção: maior dos inícios e menor dos fins; use <code>max(0, ...)</code>.", "União = área A + área B − interseção."]),
        lab("YOLO em três linhas", '''
from ultralytics import YOLO

modelo = YOLO("yolov8n.pt")
resultado = modelo("https://ultralytics.com/images/bus.jpg")
resultado[0].show()
''', corpo="<p>Rode no Colab (<code>pip install ultralytics</code>):</p>", exps=["Imprima <code>resultado[0].boxes</code>: veja coordenadas, classes e confianças."]),
        erros([("Limiar de confiança baixo demais.", "Muitos falsos positivos."), ("Avaliar só a acurácia.", "Detecção usa mAP com limiares de IoU."), ("Caixas em formatos diferentes.", "Confira se é (x1, y1, x2, y2) ou (centro, largura, altura).")]),
        ponte("Detecção e modelos multimodais", "<p>Modelos de visão e linguagem atuais conseguem responder “onde está o gato?” com coordenadas, e detectores de vocabulário aberto encontram objetos descritos por texto livre, sem treino específico. Por baixo, as ideias de caixa, IoU e NMS continuam.</p>"),
        quiz([
            ("IoU = 1 significa:", ["Caixas separadas.", "Caixas idênticas.", "Meia sobreposição."], 1, "Interseção igual à união."),
            ("Para que serve o NMS?", ["Remover caixas duplicadas.", "Aumentar a resolução.", "Classificar."], 0, "Fica com a mais confiante."),
            ("Diferença entre classificar e detectar:", ["Nenhuma.", "Detectar também localiza cada objeto.", "Detectar é só para carros."], 1, "Caixas."),
        ]),
    ],
    ["Detecção = classe + caixa + confiança.", "IoU mede sobreposição; NMS limpa duplicatas.", "Avalie com mAP."],
    "Segmentação de imagens.",
    livro=("D2L:chapter_computer-vision/bounding-box", "Seção 14.3, “Object Detection and Bounding Boxes”", "Que formatos de caixa o livro converte entre si?"))

AULAS["Segmentação de imagens"] = aula(
    25,
    "Detecção desenha caixas; segmentação pinta cada pixel. Em imagens médicas, a diferença entre “tem um tumor por aqui” e o contorno exato do tumor é a diferença entre um alerta e um planejamento de cirurgia.",
    ["diferenciar segmentação semântica e de instâncias;", "entender a arquitetura U-Net;", "avaliar com IoU e coeficiente Dice."],
    ["CNNs e detecção de objetos."],
    [
        chute("Numa foto com três pessoas, a segmentação semântica pinta:", ["Cada pessoa de uma cor diferente.", "Todos os pixels de pessoa com a mesma cor.", "Só a pessoa maior."], 1,
              ["Isso é segmentação de instâncias.", "Isso! Semântica diz a classe de cada pixel, sem separar indivíduos.", "Pinta todas."],
              "Semântica: o que é cada pixel. Instâncias: de qual objeto ele é."),
        concreto("Livro de colorir", "<p>Segmentar é colorir um livro de desenho com regras: céu azul, árvore verde, estrada cinza, pixel por pixel. O modelo devolve uma imagem do mesmo tamanho, em que cada pixel tem a cor da sua classe.</p>"),
        nota("As peças", [
            ("Máscara", "saída", "Uma classe por pixel, do tamanho da imagem."),
            ("U-Net", "arquitetura", "Desce comprimindo (codificador) e sobe ampliando (decodificador), com atalhos entre os níveis para não perder detalhes."),
            (r"$\text{Dice} = \frac{2|A \cap B|}{|A| + |B|}$", "Dice", "Sobreposição entre máscara prevista e real; comum em medicina."),
            ("SAM", "Segment Anything", "Modelo que segmenta qualquer objeto a partir de um clique ou caixa."),
        ]),
        cod("Dice e IoU de máscaras", "Implemente o Dice e a IoU para máscaras binárias.",
            '''
import numpy as np

def dice(a, b):
    return 0.0

def iou_mascara(a, b):
    return 0.0

real = np.array([[0, 1, 1], [0, 1, 1], [0, 0, 0]])
prev = np.array([[0, 1, 0], [0, 1, 1], [0, 1, 0]])
print(dice(real, prev), iou_mascara(real, prev))
''',
            [("Dice", "import numpy as np\nassert abs(dice(real, prev) - 0.75) < 1e-9"), ("IoU", "import numpy as np\nassert abs(iou_mascara(real, prev) - 0.6) < 1e-9"), ("Máscaras iguais", "import numpy as np\nassert dice(real, real) == 1 and iou_mascara(real, real) == 1")],
            '''
import numpy as np

def dice(a, b):
    inter = np.logical_and(a, b).sum()
    return 2 * inter / (a.sum() + b.sum())

def iou_mascara(a, b):
    inter = np.logical_and(a, b).sum()
    return inter / np.logical_or(a, b).sum()

real = np.array([[0, 1, 1], [0, 1, 1], [0, 0, 0]])
prev = np.array([[0, 1, 0], [0, 1, 1], [0, 1, 0]])
print(dice(real, prev), iou_mascara(real, prev))
''', ["<code>np.logical_and</code> dá a interseção; <code>np.logical_or</code>, a união."]),
        erros([("Avaliar com acurácia de pixels.", "Se 95% é fundo, prever “tudo fundo” dá 95%. Use Dice ou IoU."), ("Esquecer os atalhos da U-Net.", "As bordas saem borradas."), ("Máscaras redimensionadas com interpolação suave.", "Use vizinho mais próximo para não criar classes intermediárias.")]),
        ponte("Segmentação com modelos de fundação", "<p>O Segment Anything (SAM) recortou objetos de qualquer imagem a partir de um clique, sem treino específico, e é usado para anotar datasets em minutos. A combinação “modelo de fundação + pouco ajuste” virou o padrão em visão, como em texto.</p>"),
        quiz([
            ("Segmentação de instâncias distingue:", ["Só classes.", "Cada objeto individual.", "Só o fundo."], 1, "Pessoa 1, pessoa 2..."),
            ("Para que servem os atalhos da U-Net?", ["Recuperar detalhes finos na reconstrução.", "Reduzir parâmetros.", "Acelerar o treino."], 0, "Ligam níveis do codificador e do decodificador."),
            ("Por que não usar acurácia de pixels?", ["É lenta.", "O fundo domina e esconde erros no objeto.", "Não existe."], 1, "Dice e IoU."),
        ]),
    ],
    ["Segmentação dá uma classe por pixel.", "U-Net: descer, subir e atalhos.", "Avalie com Dice e IoU."],
    "Batch normalization.",
    livro=("D2L:chapter_computer-vision/semantic-segmentation-and-dataset", "Seção 14.9, “Semantic Segmentation and the Dataset”", "Como o livro prepara as máscaras do dataset VOC?"))
