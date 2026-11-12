# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 4 (parte C): treino na prática e ferramentas."""
from lesson_factory import *

AULAS = {}

AULAS["Batch normalization"] = aula(
    25,
    "Conforme a rede treina, a escala dos valores que passam entre as camadas muda o tempo todo, e cada camada precisa correr atrás. A normalização em lote padroniza essas ativações a cada passo: o treino fica mais rápido, mais estável e tolera taxas de aprendizado maiores.",
    ["padronizar ativações por lote;", "entender os parâmetros γ e β;", "diferenciar BatchNorm e LayerNorm."],
    ["Normalização e padronização; loop de treino."],
    [
        chute("Na avaliação, o BatchNorm usa a média de qual conjunto?", ["Do lote atual.", "Uma média acumulada durante o treino.", "Do conjunto de teste inteiro."], 1,
              ["Com um exemplo só, a média do lote não faz sentido.", "Isso! No treino ele guarda médias móveis, usadas no <code>eval()</code>.", "Isso vazaria informação do teste."],
              "Mais um motivo para nunca esquecer o <code>model.eval()</code>."),
        concreto("A régua de cada turma", "<p>Cada professor corrige com um rigor diferente. Para comparar alunos de turmas diferentes, você padroniza as notas dentro de cada turma. O BatchNorm faz isso com as ativações de cada lote, e depois deixa a rede reajustar a escala se quiser (γ e β).</p>"),
        nota("As fórmulas", [
            (r"$\hat x = \frac{x - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}$", "padronizar", "Média e variância do lote, por canal."),
            (r"$y = \gamma \hat x + \beta$", "reescalar", "γ e β são aprendidos."),
            ("LayerNorm", "por exemplo", "Normaliza ao longo das características de cada exemplo. Padrão nos Transformers."),
        ], rot="Agora sim, as fórmulas"),
        cod("BatchNorm de treino", "Implemente o forward do BatchNorm para um lote (linhas = exemplos, colunas = características), com γ e β.",
            '''
import numpy as np

def batchnorm(X, gamma, beta, eps=1e-5):
    return X

X = np.array([[1.0, 100.0], [3.0, 200.0], [5.0, 300.0]])
Y = batchnorm(X, np.ones(2), np.zeros(2))
print(Y.mean(axis=0).round(6), Y.std(axis=0).round(3))
''',
            [("Média 0 por coluna", "import numpy as np\nY = batchnorm(X, np.ones(2), np.zeros(2))\nassert np.allclose(Y.mean(axis=0), 0)"), ("Desvio 1", "import numpy as np\nY = batchnorm(X, np.ones(2), np.zeros(2))\nassert np.allclose(Y.std(axis=0), 1, atol=1e-3)"),
             ("γ e β aplicados", "import numpy as np\nY = batchnorm(X, np.array([2.0, 2.0]), np.array([5.0, 5.0]))\nassert np.allclose(Y.mean(axis=0), 5) and np.allclose(Y.std(axis=0), 2, atol=1e-3)")],
            '''
import numpy as np

def batchnorm(X, gamma, beta, eps=1e-5):
    mu = X.mean(axis=0)
    var = X.var(axis=0)
    return gamma * (X - mu) / np.sqrt(var + eps) + beta

X = np.array([[1.0, 100.0], [3.0, 200.0], [5.0, 300.0]])
Y = batchnorm(X, np.ones(2), np.zeros(2))
print(Y.mean(axis=0).round(6), Y.std(axis=0).round(3))
''', ["Média e variância por coluna (<code>axis=0</code>).", "<code>gamma * (X - mu) / np.sqrt(var + eps) + beta</code>"]),
        erros([("Lotes muito pequenos com BatchNorm.", "Médias ruidosas. Use GroupNorm ou LayerNorm."), ("Esquecer o <code>eval()</code>.", "Previsões dependem do lote e mudam à toa."), ("BatchNorm em sequências de tamanho variável.", "LayerNorm é a escolha natural.")]),
        ponte("Normalização nos LLMs", "<p>Todo bloco de um Transformer tem LayerNorm (ou RMSNorm, uma versão mais simples). Sem isso, treinar redes com centenas de camadas seria instável. A ideia é a mesma desta aula, aplicada por exemplo em vez de por lote.</p>"),
        quiz([
            ("O BatchNorm normaliza com estatísticas:", ["Do lote, no treino.", "Do teste.", "Fixas desde o início."], 0, "E guarda médias móveis."),
            ("Para que servem γ e β?", ["Deixar a rede reajustar escala e deslocamento.", "Acelerar a GPU.", "Regularizar."], 0, "São aprendidos."),
            ("Qual normalização os Transformers usam?", ["BatchNorm.", "LayerNorm/RMSNorm.", "Nenhuma."], 1, "Por exemplo."),
        ]),
    ],
    ["BatchNorm padroniza ativações por lote e reajusta com γ e β.", "Na avaliação, usa médias acumuladas.", "Transformers usam LayerNorm."],
    "Learning rate schedulers.",
    livro=("D2L:chapter_convolutional-modern/batch-norm", "Seção 8.5, “Batch Normalization”", "Como o livro explica o comportamento diferente no treino e na previsão?"))

AULAS["Learning rate schedulers"] = aula(
    20,
    "Começar com passos largos para chegar rápido perto do vale e depois passos curtos para descer até o fundo. Agendar a taxa de aprendizado ao longo do treino é um dos ajustes que mais rendem com menos esforço.",
    ["entender decaimento por etapas, cosseno e aquecimento;", "implementar um agendamento;", "saber qual é o padrão para Transformers."],
    ["Otimizadores."],
    [
        chute("Por que treinos de Transformers começam com a taxa de aprendizado subindo de zero (warmup)?", ["Por tradição.", "Porque no início os gradientes são instáveis e passos grandes podem desestabilizar tudo.", "Para economizar GPU."], 1,
              ["Há uma razão prática.", "Isso! O aquecimento evita estragos nos primeiros passos, quando as estatísticas do Adam ainda são ruins.", "Não economiza."],
              "Padrão moderno: aquecimento linear e depois decaimento em cosseno."),
        concreto("Estacionar o carro", "<p>Você chega rápido à vaga e, perto dela, vai devagar para não bater. Ninguém estaciona a 60 km/h. A taxa de aprendizado deve diminuir conforme você se aproxima do mínimo.</p>"),
        nota("Agendamentos comuns", [
            ("StepLR", "degraus", "Divide a taxa por 10 a cada N épocas."),
            ("Cosseno", "curva suave", "Desce de forma suave até perto de zero."),
            ("Warmup", "aquecimento", "Sobe linearmente nas primeiras centenas ou milhares de passos."),
            ("OneCycle", "sobe e desce", "Popular para treinos rápidos."),
        ]),
        cod("Aquecimento + cosseno", "Implemente a taxa no passo t: aquecimento linear até <code>pico</code> nos primeiros <code>aquec</code> passos, depois cosseno até 0 no passo <code>total</code>.",
            '''
import math

def taxa(t, pico=1e-3, aquec=100, total=1000):
    return pico

print(taxa(0), taxa(50), taxa(100), taxa(550), taxa(1000))
''',
            [("Começa em 0", "assert taxa(0) == 0"), ("Metade do aquecimento", "assert abs(taxa(50) - 5e-4) < 1e-12"), ("Pico no fim do aquecimento", "assert abs(taxa(100) - 1e-3) < 1e-12"),
             ("Metade do cosseno", "assert abs(taxa(550) - 5e-4) < 1e-9"), ("Termina em 0", "assert abs(taxa(1000)) < 1e-12")],
            '''
import math

def taxa(t, pico=1e-3, aquec=100, total=1000):
    if t < aquec:
        return pico * t / aquec
    progresso = (t - aquec) / (total - aquec)
    return pico * 0.5 * (1 + math.cos(math.pi * progresso))

print(taxa(0), taxa(50), taxa(100), taxa(550), taxa(1000))
''', ["Aquecimento: <code>pico * t / aquec</code>.", "Cosseno: <code>pico * 0.5 * (1 + cos(pi * progresso))</code>."]),
        erros([("Chamar <code>scheduler.step()</code> no lugar errado.", "Por época ou por lote, conforme o agendamento. Confira a documentação."), ("Decaimento rápido demais.", "O treino estaciona antes de chegar perto do mínimo."), ("Mudar agendamento e taxa ao mesmo tempo.", "Ajuste um de cada vez.")]),
        ponte("O agendamento dos LLMs", "<p>Praticamente todos os LLMs abertos publicam a mesma receita: alguns milhares de passos de aquecimento e decaimento em cosseno (ou constante com decaimento final). É um detalhe pequeno que decide se treinos de milhões de dólares convergem.</p>"),
        quiz([
            ("Para que serve o warmup?", ["Evitar instabilidade nos primeiros passos.", "Aquecer a GPU.", "Aumentar o lote."], 0, "Começo cuidadoso."),
            ("O decaimento em cosseno:", ["Aumenta a taxa sempre.", "Diminui a taxa de forma suave.", "Mantém constante."], 1, "Curva suave."),
            ("Por que diminuir a taxa no fim?", ["Para dar passos finos perto do mínimo.", "Para treinar mais rápido.", "Não se deve."], 0, "Estacionar devagar."),
        ]),
    ],
    ["Agendar a taxa: passos largos no início, finos no fim.", "Aquecimento + cosseno é o padrão moderno.", "Ajuste uma coisa por vez."],
    "Data augmentation.",
    livro=("D2L:chapter_optimization/lr-scheduler", "Seção 12.11, “Learning Rate Scheduling”", "Que efeito do aquecimento o livro demonstra?"))

AULAS["Data augmentation"] = aula(
    20,
    "Uma foto de gato espelhada continua sendo um gato. Girada um pouco, mais clara, cortada: ainda um gato. Gerar essas variações durante o treino multiplica o dataset de graça e ensina o modelo a ignorar o que não importa.",
    ["aplicar transformações que preservam o rótulo;", "saber quando uma transformação muda o rótulo;", "aumentar dados de texto e áudio."],
    ["CNNs e overfitting."],
    [
        chute("Num reconhecedor de dígitos, espelhar horizontalmente é uma boa aumentação?", ["Sim, sempre.", "Não: um 2 espelhado não é um 2 (e um 6 girado vira 9).", "Só para o número 8."], 1,
              ["Depende do problema.", "Isso! Toda aumentação precisa preservar o rótulo.", "Mesmo o 8 só funciona por coincidência."],
              "Pergunta-chave: depois da transformação, o rótulo continua certo?"),
        concreto("Reconhecer um amigo", "<p>Você reconhece um amigo de lado, de óculos, no escuro ou de longe porque já o viu em muitas situações. Mostrar ao modelo a mesma imagem em várias situações faz o mesmo.</p>"),
        nota("Aumentações comuns", [
            ("Imagens", "geometria e cor", "Espelhar, girar, recortar, brilho, contraste, ruído."),
            ("Texto", "reformulações", "Sinônimos, tradução de ida e volta, paráfrases geradas por LLM."),
            ("Áudio", "variação", "Ruído de fundo, velocidade, tom."),
            ("Só no treino", "regra", "Validação e teste usam os dados originais."),
        ]),
        cod("Aumentações numa imagem", "Implemente <code>espelhar</code> (horizontal), <code>girar90</code> e <code>brilho</code> (soma um valor e recorta entre 0 e 1), sem alterar a imagem original.",
            '''
import numpy as np

def espelhar(img): return img
def girar90(img): return img
def brilho(img, delta): return img

img = np.array([[0.1, 0.9], [0.5, 0.2]])
print(espelhar(img), girar90(img), brilho(img, 0.3), sep="\\n")
''',
            [("Espelhar", "import numpy as np\nassert np.array_equal(espelhar(img), [[0.9, 0.1], [0.2, 0.5]])"), ("Girar 90", "import numpy as np\nassert np.array_equal(girar90(img), np.rot90(img))"),
             ("Brilho recortado", "import numpy as np\nassert np.allclose(brilho(img, 0.3), [[0.4, 1.0], [0.8, 0.5]])"), ("Original intacta", "import numpy as np\nassert np.allclose(img, [[0.1, 0.9], [0.5, 0.2]])")],
            '''
import numpy as np

def espelhar(img): return img[:, ::-1]
def girar90(img): return np.rot90(img)
def brilho(img, delta): return np.clip(img + delta, 0, 1)

img = np.array([[0.1, 0.9], [0.5, 0.2]])
print(espelhar(img), girar90(img), brilho(img, 0.3), sep="\\n")
''', ["Espelhar: <code>img[:, ::-1]</code>.", "Brilho: <code>np.clip(img + delta, 0, 1)</code>."]),
        erros([("Aumentar a validação.", "Você mede o modelo em dados que não existem."), ("Transformações que mudam o rótulo.", "Girar 6 vira 9; espelhar texto muda o sentido."), ("Exagerar.", "Distorções fortes demais criam exemplos irreais e atrapalham.")]),
        ponte("Dados sintéticos com LLMs", "<p>Para texto, a aumentação moderna é pedir a um LLM paráfrases e variações de exemplos. Os mesmos cuidados valem: o rótulo precisa continuar certo e os dados sintéticos não podem dominar os reais.</p>"),
        quiz([
            ("Uma boa aumentação:", ["Muda o rótulo.", "Preserva o rótulo.", "Remove exemplos."], 1, "Gato continua gato."),
            ("Onde aplicar aumentação?", ["Só no treino.", "No teste.", "Em tudo."], 0, "Avaliação com dados originais."),
            ("Aumentação ajuda principalmente contra:", ["Underfitting.", "Overfitting.", "Vazamento."], 1, "Mais variedade."),
        ]),
    ],
    ["Aumentação cria variações que preservam o rótulo.", "Só no treino.", "Escolha transformações que fazem sentido no problema."],
    "Early stopping e checkpoints.",
    livro=("D2L:chapter_computer-vision/image-augmentation", "Seção 14.1, “Image Augmentation”", "Que aumentações o livro aplica no CIFAR-10?"))

AULAS["Early stopping e checkpoints"] = aula(
    20,
    "A perda de validação caiu por 20 épocas e começou a subir. Continuar treinando só piora. Parar no ponto certo e guardar o melhor modelo encontrado é simples e evita horas de GPU desperdiçadas e um modelo pior no fim.",
    ["parar quando a validação deixa de melhorar (paciência);", "salvar e recarregar o melhor checkpoint;", "retomar um treino interrompido."],
    ["Loop de treino e overfitting."],
    [
        chute("Paciência = 3. A perda de validação nas épocas foi 0,50; 0,42; 0,40; 0,41; 0,43; 0,44. Em que época o treino para e qual modelo fica?", ["Para na 6, fica o da 6.", "Para na 6, fica o da 3 (0,40).", "Para na 4."], 1,
              ["O último não é o melhor.", "Isso! Três épocas sem melhorar depois da 3: para e recarrega o melhor.", "Na 4 só uma época não melhorou."],
              "Pare depois de “paciência” épocas sem melhora e use o melhor checkpoint."),
        concreto("O ponto do bolo", "<p>Você confere o bolo com um palito de tempos em tempos. Quando ele começa a passar do ponto, você não deixa no forno “para ver”: tira e fica com a melhor versão que teve.</p>"),
        nota("Peças", [
            ("Paciência", "tolerância", "Quantas épocas sem melhora antes de parar."),
            ("<code>torch.save(modelo.state_dict(), \"melhor.pt\")</code>", "salvar", "Guarde os pesos quando a validação melhorar."),
            ("<code>modelo.load_state_dict(torch.load(\"melhor.pt\"))</code>", "recarregar", "No fim, volte ao melhor."),
            ("Checkpoint completo", "retomar", "Pesos, otimizador, época e agendador: para continuar de onde parou."),
        ]),
        cod("Early stopping", "Complete a função que percorre as perdas de validação e devolve <code>(época_de_parada, melhor_época)</code>, contando as épocas a partir de 1.",
            '''
def early_stopping(perdas, paciencia=3):
    return len(perdas), 1

print(early_stopping([0.50, 0.42, 0.40, 0.41, 0.43, 0.44, 0.39]))
''',
            [("Exemplo", "assert early_stopping([0.50, 0.42, 0.40, 0.41, 0.43, 0.44, 0.39]) == (6, 3)"), ("Sem parada", "assert early_stopping([0.5, 0.4, 0.3]) == (3, 3)"), ("Paciência 1", "assert early_stopping([0.5, 0.6, 0.4], paciencia=1) == (2, 1)")],
            '''
def early_stopping(perdas, paciencia=3):
    melhor, melhor_ep, sem_melhora = float("inf"), 0, 0
    for ep, p in enumerate(perdas, start=1):
        if p < melhor:
            melhor, melhor_ep, sem_melhora = p, ep, 0
        else:
            sem_melhora += 1
            if sem_melhora >= paciencia:
                return ep, melhor_ep
    return len(perdas), melhor_ep
''', ["Guarde a melhor perda, a época dela e um contador de épocas sem melhora."]),
        erros([("Usar o modelo da última época.", "Recarregue o melhor checkpoint."), ("Paciência curta demais.", "Perdas oscilam; você para cedo."), ("Salvar só os pesos e querer retomar o treino.", "Salve também o otimizador e o agendador.")]),
        ponte("Checkpoints em escala", "<p>Treinos de LLMs duram semanas e máquinas falham: checkpoints a cada poucas horas são obrigatórios. E os “pesos” que você baixa do Hugging Face são exatamente um checkpoint, geralmente no formato seguro <code>.safetensors</code>.</p>"),
        quiz([
            ("Early stopping olha para:", ["A perda de treino.", "A perda de validação.", "O tempo."], 1, "Generalização."),
            ("O que é paciência?", ["Épocas sem melhora toleradas.", "Tamanho do lote.", "Taxa de aprendizado."], 0, "Antes de parar."),
            ("Para retomar um treino, salve:", ["Só os pesos.", "Pesos, otimizador, época e agendador.", "Só a perda."], 1, "Estado completo."),
        ]),
    ],
    ["Pare depois de algumas épocas sem melhora na validação.", "Salve e recarregue o melhor checkpoint.", "Checkpoint completo permite retomar."],
    "Depurar uma rede que não aprende.",
    livro=("D2L:chapter_builders-guide/read-write", "Seção 6.6, “File I/O”", "Como o livro salva e carrega os parâmetros de um modelo?"))

AULAS["Depurar rede que não aprende"] = aula(
    30,
    "O código roda, não dá erro, e a perda não cai. É a situação mais comum e mais frustrante do deep learning. A saída é um roteiro de testes simples, do mais barato ao mais caro, que acha a maioria dos problemas em minutos.",
    ["seguir um roteiro de depuração;", "fazer o modelo decorar um lote pequeno;", "inspecionar dados, perda e gradientes."],
    ["Loop de treino, backpropagation e normalização."],
    [
        chute("Primeiro teste quando uma rede não aprende:", ["Trocar a arquitetura.", "Tentar decorar um único lote pequeno: a perda deve ir quase a zero.", "Treinar por mais dias."], 1,
              ["Caro e sem diagnóstico.", "Isso! Se nem um lote ela decora, o problema é bug (dados, perda, gradiente), não capacidade.", "Mais tempo não conserta bug."],
              "Overfitting de um lote é o “olá mundo” da depuração."),
        concreto("O mecânico", "<p>O carro não liga. O mecânico não troca o motor: confere a bateria, depois o combustível, depois a ignição. Cada teste é rápido e elimina uma causa. Depurar redes é a mesma ordem: do simples ao caro.</p>"),
        passos("O roteiro", [
            ("<b>Olhe os dados</b>: imprima exemplos e rótulos depois do pré-processamento.", "Rótulos trocados e imagens pretas são mais comuns do que parece."),
            ("<b>Perda inicial</b>: com C classes, deve estar perto de log(C).", "Muito diferente indica bug na saída ou na perda."),
            ("<b>Decore um lote</b>: 1 lote, muitas iterações, perda → 0.", "Falhou? Bug. Funcionou? Problema de generalização."),
            ("<b>Gradientes</b>: são zero, NaN ou enormes?", "Zero: ReLU morta ou tensor desconectado. Enormes: taxa alta, falta de normalização."),
            ("<b>Taxa de aprendizado</b>: teste 10× maior e 10× menor.", "Muitas vezes é só isso."),
        ]),
        cod("Sanidade da perda inicial", "Escreva <code>perda_inicial_ok(perda, n_classes)</code>: devolve True se a perda estiver a no máximo 20% de log(n_classes), o valor esperado de um modelo que ainda chuta igualmente.",
            '''
import math

def perda_inicial_ok(perda, n_classes):
    return True

print(perda_inicial_ok(2.31, 10), perda_inicial_ok(8.5, 10))
''',
            [("CIFAR-10 com 2,31 está ok", "assert perda_inicial_ok(2.31, 10) is True"), ("8,5 é suspeito", "assert perda_inicial_ok(8.5, 10) is False"), ("Binário", "assert perda_inicial_ok(0.69, 2) is True and perda_inicial_ok(0.1, 2) is False")],
            '''
import math

def perda_inicial_ok(perda, n_classes):
    esperado = math.log(n_classes)
    return abs(perda - esperado) <= 0.2 * esperado

print(perda_inicial_ok(2.31, 10), perda_inicial_ok(8.5, 10))
''', ["Esperado = <code>math.log(n_classes)</code>; compare a diferença com 20% dele."]),
        erros([("Mudar várias coisas ao mesmo tempo.", "Você não sabe o que resolveu. Uma por vez."), ("Confiar que os dados estão certos.", "Sempre olhe exemplos depois do DataLoader."), ("Softmax antes da <code>CrossEntropyLoss</code>.", "Aplicado duas vezes, o aprendizado trava.")]),
        ponte("A receita do Karpathy", "<p>O roteiro desta aula segue “A Recipe for Training Neural Networks”, de Andrej Karpathy: comece simples, verifique cada peça, só então aumente a complexidade. Em LLMs, os mesmos sintomas (perda que não cai, picos de perda) têm as mesmas primeiras suspeitas: dados, taxa e estabilidade numérica.</p>"),
        quiz([
            ("Se a rede não consegue decorar um lote pequeno:", ["Precisa de mais dados.", "Há um bug no código, nos dados ou na perda.", "Precisa de mais camadas."], 1, "Capacidade não é o problema."),
            ("Perda inicial esperada com 10 classes:", ["0", "≈ 2,3 (log 10)", "10"], 1, "Chute uniforme."),
            ("Gradientes NaN apontam primeiro para:", ["Taxa de aprendizado alta ou instabilidade numérica.", "Poucos dados.", "Dropout."], 0, "Explosão."),
        ]),
    ],
    ["Depure do barato ao caro: dados, perda inicial, um lote, gradientes, taxa.", "Decorar um lote separa bug de generalização.", "Uma mudança por vez."],
    "Mixed precision.",
    livro=("UDL", "Capítulo 7, “Gradients and initialization”", "Por que a inicialização errada faz os gradientes sumirem ou explodirem?"))

AULAS["Mixed precision"] = aula(
    20,
    "Números em 16 bits ocupam metade da memória dos de 32 bits e as GPUs modernas os multiplicam muito mais rápido. Treinar com precisão mista usa 16 bits onde dá e 32 bits onde precisa: quase o dobro de velocidade, praticamente sem perda de qualidade.",
    ["entender float32, float16 e bfloat16;", "saber o que pode dar errado com 16 bits;", "usar autocast e GradScaler."],
    ["Treinar em GPU."],
    [
        chute("Por que o bfloat16 virou o favorito para treinar LLMs?", ["É mais preciso que o float32.", "Tem a mesma faixa de valores do float32, então não estoura nem zera fácil.", "Ocupa menos que 8 bits."], 1,
              ["É menos preciso, mas cobre a mesma faixa.", "Isso! O float16 estoura com números grandes; o bfloat16 abre mão de casas decimais para manter a faixa.", "Ocupa 16 bits."],
              "Faixa (expoente) importa mais que precisão (mantissa) no treino."),
        concreto("A régua e o metro de bolso", "<p>Para medir um quarto, uma trena com marcas a cada centímetro basta; você não precisa de micrômetro. Mas se a trena tiver só 1 metro, você não mede o quarto. O bfloat16 é a trena longa com marcas menos finas.</p>"),
        tabela("Os formatos", ["Formato", "Bytes", "Faixa", "Uso"], [
            ["float32", "4", "ampla", "padrão; acumulação de somas"],
            ["float16", "2", "pequena (estoura acima de ~65 mil)", "precisa de GradScaler"],
            ["bfloat16", "2", "ampla, menos precisa", "padrão no treino de LLMs"],
            ["int8 / 4 bits", "1 ou 0,5", "inteiros", "quantização para inferência"],
        ]),
        cod("Os limites do float16", "Com NumPy, mostre os dois problemas do float16: um número grande que estoura para infinito e um gradiente pequeno que vira zero. Depois, mostre que multiplicar o gradiente por 1024 antes (o que o GradScaler faz) salva o valor.",
            '''
import numpy as np

grande = None      # converta 70000.0 para float16
pequeno = None     # converta 1e-8 para float16
escalado = None    # converta 1e-8 * 1024 para float16

print(grande, pequeno, escalado)
''',
            [("Grande estoura", "import numpy as np\nassert np.isinf(grande)"), ("Pequeno vira zero", "assert pequeno == 0"), ("Escalado sobrevive", "assert escalado > 0")],
            '''
import numpy as np

grande = np.float16(70000.0)
pequeno = np.float16(1e-8)
escalado = np.float16(1e-8 * 1024)

print(grande, pequeno, escalado)
''', ["<code>np.float16(valor)</code> converte para 16 bits."], exp="<p>O GradScaler multiplica a perda antes do <code>backward</code> e divide os gradientes de volta antes do passo, exatamente para fugir do zero.</p>"),
        lab("Precisão mista no PyTorch", '''
import torch

scaler = torch.amp.GradScaler("cuda")
for x, y in loader:
    x, y = x.cuda(), y.cuda()
    with torch.autocast("cuda", dtype=torch.float16):
        perda = criterio(modelo(x), y)
    opt.zero_grad()
    scaler.scale(perda).backward()
    scaler.step(opt)
    scaler.update()
''', corpo="<p>As linhas que mudam no loop de treino:</p>", exps=["Com bfloat16, o GradScaler não é necessário: troque o dtype e remova-o."]),
        erros([("Fazer tudo em float16.", "Somas longas e a perda perdem precisão. O autocast mantém o que precisa em 32 bits."), ("Usar float16 sem GradScaler.", "Gradientes pequenos viram zero."), ("Esperar ganho em GPUs antigas.", "O ganho depende de núcleos de tensor.")]),
        ponte("Precisão e o custo dos LLMs", "<p>LLMs são treinados em bfloat16, e na inferência são comprimidos para 8 ou 4 bits (quantização, Fase 5). Cada metade de bits é metade da memória: é isso que permite rodar um modelo de 7 bilhões de parâmetros num notebook.</p>"),
        quiz([
            ("Qual a vantagem do float16?", ["Mais precisão.", "Metade da memória e contas mais rápidas.", "Nenhuma."], 1, "Menos bits."),
            ("Para que serve o GradScaler?", ["Evitar que gradientes pequenos virem zero em float16.", "Acelerar a leitura de dados.", "Normalizar."], 0, "Escala e desescala."),
            ("Por que o bfloat16 dispensa o GradScaler?", ["Tem a mesma faixa do float32.", "Tem mais precisão.", "Usa 32 bits."], 0, "Não estoura nem zera fácil."),
        ]),
    ],
    ["Precisão mista: 16 bits onde dá, 32 onde precisa.", "float16 precisa de GradScaler; bfloat16 mantém a faixa.", "Menos bits = menos memória e mais velocidade."],
    "TensorFlow e Keras.",
    livro=("D2L:chapter_computational-performance/auto-parallelism", "Capítulo 13, “Computational Performance”", "Que fatores de desempenho o livro discute?"))

AULAS["TensorFlow e Keras (noção)"] = aula(
    20,
    "O PyTorch domina a pesquisa e os LLMs, mas o TensorFlow, com sua interface Keras, ainda roda em muita produção, em celulares (TFLite) e em navegadores. Saber ler um código Keras abre portas e mostra que as ideias são as mesmas.",
    ["ler e escrever um modelo Keras;", "usar <code>compile</code>, <code>fit</code> e <code>evaluate</code>;", "comparar com o PyTorch."],
    ["Loop de treino no PyTorch."],
    [
        chute("No Keras, onde fica o loop de treino que você escreve no PyTorch?", ["Você escreve igual.", "Dentro do <code>model.fit()</code>.", "Não existe treino no Keras."], 1,
              ["O Keras esconde o loop.", "Isso! <code>fit</code> faz forward, perda, backward e passo, época a época.", "Existe, só está embutido."],
              "Keras: mais conveniente. PyTorch: mais controle."),
        concreto("Câmbio automático e manual", "<p>O Keras é o carro automático: você diz para onde vai e ele troca as marchas. O PyTorch é o manual: dá mais trabalho, mas você controla cada troca. Os dois chegam ao mesmo lugar.</p>"),
        tabela("Lado a lado", ["Conceito", "Keras", "PyTorch"], [
            ["Modelo em sequência", "<code>keras.Sequential([...])</code>", "<code>nn.Sequential(...)</code>"],
            ["Camada densa", "<code>layers.Dense(128, activation=\"relu\")</code>", "<code>nn.Linear</code> + <code>nn.ReLU</code>"],
            ["Configurar treino", "<code>model.compile(optimizer, loss, metrics)</code>", "criar otimizador e critério"],
            ["Treinar", "<code>model.fit(X, y, epochs=10)</code>", "escrever o loop"],
            ["Salvar", "<code>model.save(\"m.keras\")</code>", "<code>torch.save(state_dict)</code>"],
        ], rot="Comparando"),
        lab("MNIST com Keras", '''
import keras
from keras import layers

(X, y), (Xt, yt) = keras.datasets.mnist.load_data()
X, Xt = X / 255.0, Xt / 255.0
modelo = keras.Sequential([layers.Flatten(input_shape=(28, 28)), layers.Dense(128, activation="relu"), layers.Dense(10)])
modelo.compile(optimizer="adam", loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=["accuracy"])
modelo.fit(X, y, epochs=3, validation_split=0.1)
modelo.evaluate(Xt, yt)
''', corpo="<p>Rode no Colab: a mesma rede da primeira aula da fase.</p>", exps=["Acrescente <code>keras.callbacks.EarlyStopping(patience=2)</code> no <code>fit</code>."]),
        cod("Contando parâmetros do modelo Keras", "Calcule quantos parâmetros tem o modelo acima: Flatten (sem parâmetros) → Dense(128) → Dense(10), com entrada 28 × 28.",
            '''
total = 0
print(total)
''',
            [("101.770 parâmetros", "assert total == 101770, f'total = {total}'")],
            '''
entrada = 28 * 28
total = (entrada * 128 + 128) + (128 * 10 + 10)
print(total)
''', ["Cada Dense: entradas × saídas + saídas."]),
        erros([("Misturar Keras 2 e Keras 3 em tutoriais.", "APIs mudaram; confira a versão."), ("<code>from_logits</code> errado.", "Se a última camada não tem softmax, use <code>from_logits=True</code>."), ("Escolher framework por moda.", "Escolha pelo ecossistema do problema: LLMs → PyTorch; celular → TFLite também serve.")]),
        ponte("Keras 3 e o ecossistema", "<p>O Keras 3 roda sobre TensorFlow, PyTorch ou JAX: o mesmo código em três motores. E modelos treinados em qualquer um podem ser exportados para formatos comuns (ONNX, próxima aula da sequência) e servidos em produção.</p>"),
        quiz([
            ("O que <code>model.compile</code> define?", ["Otimizador, perda e métricas.", "As camadas.", "Os dados."], 0, "Configuração do treino."),
            ("Equivalente Keras de <code>nn.Linear</code> + ReLU:", ["<code>layers.Dense(n, activation=\"relu\")</code>", "<code>layers.Flatten</code>", "<code>layers.Conv2D</code>"], 0, "Camada densa."),
            ("Vantagem do PyTorch para pesquisa e LLMs:", ["Controle total do loop e ecossistema dominante.", "Não precisa de GPU.", "É mais antigo."], 0, "Flexibilidade."),
        ]),
    ],
    ["Keras: <code>compile</code> + <code>fit</code> escondem o loop.", "As ideias são as mesmas do PyTorch.", "Escolha o framework pelo ecossistema."],
    "TensorBoard e logs.",
    livro=("D2L:chapter_introduction/index", "Capítulo 1, “Introduction”, parte sobre frameworks", "Que frameworks de deep learning o livro cita na história recente?"))

AULAS["TensorBoard e logs"] = aula(
    20,
    "Treinar olhando números passarem no terminal é dirigir de olhos fechados. Registrar perdas, métricas, taxa de aprendizado e exemplos num painel mostra na hora quando algo vai mal, e permite comparar dezenas de experimentos lado a lado.",
    ["registrar escalares, histogramas e imagens;", "comparar execuções;", "saber o que vale a pena registrar."],
    ["Loop de treino."],
    [
        chute("O que é mais útil registrar a cada época?", ["Só a acurácia final.", "Perda de treino e de validação, métricas e taxa de aprendizado.", "O tempo de cada lote apenas."], 1,
              ["Só o fim não mostra o caminho.", "Isso! Com essas curvas você vê overfitting, instabilidade e o efeito do agendador.", "Tempo ajuda, mas não basta."],
              "Curvas de treino e validação no mesmo gráfico contam a história."),
        concreto("O diário de bordo", "<p>Pilotos registram velocidade, combustível e altitude o tempo todo: se algo dá errado, o registro mostra quando e por quê. Logs de treino são o diário de bordo do seu modelo.</p>"),
        nota("O que registrar", [
            ("<code>writer.add_scalar(\"perda/treino\", v, passo)</code>", "escalares", "Perdas, métricas, taxa de aprendizado."),
            ("<code>add_histogram</code>", "distribuições", "Pesos e gradientes: veja se estão morrendo ou explodindo."),
            ("<code>add_image</code>", "exemplos", "Previsões erradas, imagens geradas."),
            ("Hiperparâmetros", "contexto", "Qual configuração gerou cada curva."),
            ("Weights &amp; Biases, MLflow", "alternativas", "Painéis na nuvem e comparação de experimentos (Fase 6)."),
        ]),
        lab("TensorBoard no Colab", '''
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter("runs/exp_lr_1e-3")
for epoca in range(epocas):
    perda_treino, perda_valid = treinar_uma_epoca(), avaliar()
    writer.add_scalar("perda/treino", perda_treino, epoca)
    writer.add_scalar("perda/valid", perda_valid, epoca)
    writer.add_scalar("lr", opt.param_groups[0]["lr"], epoca)
writer.close()

# numa célula: %load_ext tensorboard  e  %tensorboard --logdir runs
''', corpo="<p>No seu loop:</p>", exps=["Rode duas vezes com taxas diferentes (pastas diferentes em <code>runs/</code>) e compare as curvas."]),
        cod("Um registrador simples", "Escreva a classe <code>Registro</code> que guarda valores por nome (<code>add(nome, valor)</code>) e devolve a época do melhor valor de uma métrica (<code>melhor(nome, menor=True)</code>).",
            '''
class Registro:
    def __init__(self):
        self.dados = {}
    def add(self, nome, valor):
        pass
    def melhor(self, nome, menor=True):
        return 0

r = Registro()
for v in [0.9, 0.6, 0.5, 0.55]:
    r.add("perda_valid", v)
print(r.melhor("perda_valid"))
''',
            [("Melhor é a época 2 (contando de 0)", "r2 = Registro()\nfor v in [0.9, 0.6, 0.5, 0.55]: r2.add('pv', v)\nassert r2.melhor('pv') == 2"),
             ("Maior é melhor", "r3 = Registro()\nfor v in [0.7, 0.9, 0.8]: r3.add('acc', v)\nassert r3.melhor('acc', menor=False) == 1")],
            '''
class Registro:
    def __init__(self):
        self.dados = {}
    def add(self, nome, valor):
        self.dados.setdefault(nome, []).append(valor)
    def melhor(self, nome, menor=True):
        v = self.dados[nome]
        alvo = min(v) if menor else max(v)
        return v.index(alvo)

r = Registro()
for v in [0.9, 0.6, 0.5, 0.55]:
    r.add("perda_valid", v)
print(r.melhor("perda_valid"))
''', ["<code>self.dados.setdefault(nome, []).append(valor)</code>"]),
        erros([("Experimentos sem nome descritivo.", "“run_3” não diz nada. Use o hiperparâmetro no nome."), ("Registrar demais a cada passo.", "Arquivos enormes e painel lento. Registre por época ou a cada N passos."), ("Não registrar a configuração.", "Daqui a uma semana você não lembra o que gerou cada curva.")]),
        ponte("Observabilidade de LLMs", "<p>Em aplicações com LLM, o equivalente são os traces: cada chamada, prompt, resposta, custo e latência registrados (LangSmith, Langfuse, Fase 6). O princípio é o mesmo: sem registro, você não sabe por que algo deu errado.</p>"),
        quiz([
            ("Por que registrar treino e validação juntos?", ["Para ver a diferença entre eles (overfitting).", "Por estética.", "Para treinar mais rápido."], 0, "A distância conta a história."),
            ("Histogramas de gradientes ajudam a ver:", ["Gradientes sumindo ou explodindo.", "A acurácia.", "O tamanho do dataset."], 0, "Saúde do treino."),
            ("Como comparar dois experimentos no TensorBoard?", ["Em pastas de log diferentes.", "Apagando o anterior.", "Não dá."], 0, "Cada execução numa pasta."),
        ]),
    ],
    ["Registre perdas, métricas, taxa e configuração.", "Compare execuções lado a lado.", "Sem registro, não há diagnóstico."],
    "Exportar modelos com ONNX.",
    livro=("D2L:chapter_preliminaries/autograd", "Capítulo 2, para revisar o que cada gradiente representa", "Que informações sobre gradientes valem a pena acompanhar?"))

AULAS["Exportar modelos com ONNX"] = aula(
    20,
    "O modelo foi treinado em PyTorch, mas o servidor de produção roda C#, o app é em JavaScript e o dispositivo é um celular. O ONNX é um formato comum, um “PDF dos modelos”, que permite rodar o mesmo modelo em vários lugares, muitas vezes mais rápido.",
    ["exportar um modelo PyTorch para ONNX;", "rodar inferência com ONNX Runtime;", "conferir se as saídas batem."],
    ["Loop de treino e checkpoints."],
    [
        chute("Depois de exportar para ONNX, qual verificação é obrigatória?", ["Nenhuma.", "Comparar as saídas do ONNX com as do PyTorch para as mesmas entradas.", "Ver o tamanho do arquivo."], 1,
              ["Exportações podem mudar comportamentos.", "Isso! Diferenças pequenas (1e-5) são normais; grandes indicam problema.", "Tamanho não garante nada."],
              "Exportou? Compare."),
        concreto("O PDF", "<p>Você escreve no Word, mas manda em PDF para qualquer um abrir em qualquer aparelho, igualzinho. O ONNX é o PDF do modelo: treine onde quiser, rode em qualquer lugar.</p>"),
        nota("O caminho", [
            ("<code>torch.onnx.export(modelo, exemplo, \"m.onnx\")</code>", "exportar", "Grava o grafo e os pesos."),
            ("<code>dynamic_axes</code>", "tamanho variável", "Permite lotes de tamanhos diferentes."),
            ("<code>onnxruntime.InferenceSession(\"m.onnx\")</code>", "rodar", "Inferência rápida em CPU, GPU e celulares."),
            ("<code>np.allclose(saida_pt, saida_onnx, atol=1e-4)</code>", "conferir", "As saídas precisam bater."),
        ]),
        lab("Exportar e conferir", '''
import numpy as np, torch, onnxruntime as ort

modelo.eval()
exemplo = torch.randn(1, 3, 224, 224)
torch.onnx.export(modelo, exemplo, "modelo.onnx", input_names=["x"], output_names=["y"],
                  dynamic_axes={"x": {0: "lote"}, "y": {0: "lote"}})

sessao = ort.InferenceSession("modelo.onnx")
saida_onnx = sessao.run(None, {"x": exemplo.numpy()})[0]
saida_pt = modelo(exemplo).detach().numpy()
print("iguais:", np.allclose(saida_pt, saida_onnx, atol=1e-4))
''', corpo="<p>Rode no Colab (<code>pip install onnx onnxruntime</code>) com qualquer modelo treinado:</p>", exps=["Meça o tempo de 100 inferências no PyTorch e no ONNX Runtime na CPU."]),
        cod("Conferindo a exportação", "Escreva <code>conferir(a, b, tol)</code> que devolve a maior diferença absoluta entre as saídas e se ela está dentro da tolerância.",
            '''
import numpy as np

def conferir(a, b, tol=1e-4):
    return 0.0, True

pt = np.array([[0.1234567, 2.5], [1.0, -3.2]])
onnx = np.array([[0.1234571, 2.5], [1.0, -3.2000001]])
print(conferir(pt, onnx))
''',
            [("Dentro da tolerância", "import numpy as np\nd, ok = conferir(pt, onnx)\nassert ok and d < 1e-6"), ("Fora da tolerância", "import numpy as np\nd, ok = conferir(np.array([1.0]), np.array([1.1]))\nassert not ok and abs(d - 0.1) < 1e-9")],
            '''
import numpy as np

def conferir(a, b, tol=1e-4):
    d = float(np.abs(a - b).max())
    return d, d <= tol

pt = np.array([[0.1234567, 2.5], [1.0, -3.2]])
onnx = np.array([[0.1234571, 2.5], [1.0, -3.2000001]])
print(conferir(pt, onnx))
''', ["<code>np.abs(a - b).max()</code>"]),
        erros([("Exportar em modo de treino.", "Dropout e BatchNorm saem errados. Chame <code>eval()</code> antes."), ("Esquecer eixos dinâmicos.", "O modelo só aceita o tamanho de lote do exemplo."), ("Operações não suportadas.", "Algumas camadas exóticas não exportam; atualize o <code>opset</code> ou simplifique.")]),
        ponte("Modelos em todo lugar", "<p>Detectores rodando em câmeras, classificadores em navegadores, modelos de embeddings em servidores sem GPU: ONNX e formatos parecidos (GGUF para LLMs locais, TensorRT para GPUs NVIDIA) levam o modelo do notebook para onde ele é usado.</p>"),
        quiz([
            ("Para que serve o ONNX?", ["Treinar modelos.", "Rodar o mesmo modelo em plataformas diferentes.", "Gerar dados."], 1, "Formato comum."),
            ("Antes de exportar, chame:", ["<code>model.train()</code>", "<code>model.eval()</code>", "<code>backward()</code>"], 1, "Comportamento de inferência."),
            ("Diferenças de 1e-6 entre saídas são:", ["Um bug grave.", "Normais (arredondamento).", "Impossíveis."], 1, "Use tolerância."),
        ]),
    ],
    ["ONNX é o formato portátil dos modelos.", "Exporte em <code>eval()</code>, com eixos dinâmicos.", "Sempre compare as saídas."],
    "PyTorch Lightning.",
    livro=("D2L:chapter_builders-guide/read-write", "Seção 6.6, “File I/O”", "Que diferença o livro aponta entre salvar parâmetros e o modelo inteiro?"))

AULAS["PyTorch Lightning"] = aula(
    20,
    "Depois de escrever o loop de treino dez vezes, você percebe que 80% dele é sempre igual: dispositivos, logs, checkpoints, precisão mista. O Lightning organiza isso: você escreve só o que é específico do seu modelo, e ele cuida do resto.",
    ["organizar um modelo num <code>LightningModule</code>;", "treinar com o <code>Trainer</code>;", "ganhar GPU, logs e checkpoints com uma linha."],
    ["Loop de treino, early stopping e mixed precision."],
    [
        chute("No Lightning, onde fica o <code>zero_grad()</code>, <code>backward()</code> e <code>step()</code>?", ["Você escreve em todo passo.", "O Trainer faz; você só devolve a perda em <code>training_step</code>.", "Não existem."], 1,
              ["É exatamente o que ele elimina.", "Isso! Você descreve o que é um passo de treino; o Trainer cuida da mecânica.", "Existem, escondidos."],
              "Menos código repetido, menos bugs."),
        concreto("A cozinha profissional", "<p>O chef cria a receita; a cozinha profissional tem gente para lavar, organizar, controlar o tempo do forno. O Lightning é a equipe da cozinha: você só cozinha.</p>"),
        nota("As peças", [
            ("<code>training_step(self, batch, idx)</code>", "um passo", "Calcula e devolve a perda."),
            ("<code>validation_step</code>", "validação", "Registra métricas com <code>self.log</code>."),
            ("<code>configure_optimizers</code>", "otimizador", "Devolve o otimizador (e o agendador)."),
            ("<code>Trainer(max_epochs=10, accelerator=\"gpu\", precision=\"bf16-mixed\")</code>", "treinar", "GPU, precisão mista, checkpoints e early stopping por configuração."),
        ]),
        lab("Um LightningModule", '''
import lightning as L
import torch
from torch import nn

class Classificador(L.LightningModule):
    def __init__(self):
        super().__init__()
        self.rede = nn.Sequential(nn.Flatten(), nn.Linear(784, 128), nn.ReLU(), nn.Linear(128, 10))
    def training_step(self, batch, idx):
        x, y = batch
        perda = nn.functional.cross_entropy(self.rede(x), y)
        self.log("perda_treino", perda)
        return perda
    def validation_step(self, batch, idx):
        x, y = batch
        self.log("acc_valid", (self.rede(x).argmax(1) == y).float().mean())
    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=1e-3)

trainer = L.Trainer(max_epochs=5, accelerator="auto",
                    callbacks=[L.pytorch.callbacks.EarlyStopping("acc_valid", mode="max", patience=2)])
trainer.fit(Classificador(), treino_loader, valid_loader)
''', corpo="<p>Rode no Colab (<code>pip install lightning</code>) com os DataLoaders do MNIST:</p>", exps=["Acrescente <code>precision=\"16-mixed\"</code> no Trainer e compare o tempo."]),
        cod("Separando o que muda do que se repete", "Para fixar a ideia, implemente um “Trainer” mínimo: <code>treinar(passo, lotes, epocas)</code> chama <code>passo(lote)</code> para cada lote e devolve a perda média de cada época.",
            '''
def treinar(passo, lotes, epocas):
    historico = []
    return historico

# um "modelo" que fica melhor a cada chamada
estado = {"n": 0}
def passo(lote):
    estado["n"] += 1
    return sum(lote) / estado["n"]

print(treinar(passo, [[1, 1], [2, 2]], 3))
''',
            [("Uma média por época", "estado['n'] = 0\nh = treinar(passo, [[1, 1], [2, 2]], 3)\nassert len(h) == 3"), ("Valores corretos", "estado['n'] = 0\nh = treinar(passo, [[2], [2]], 2)\nassert h == [1.5, 0.5833333333333333] or [round(x, 6) for x in h] == [1.5, 0.583333], f'h = {h}'")],
            '''
def treinar(passo, lotes, epocas):
    historico = []
    for _ in range(epocas):
        perdas = [passo(lote) for lote in lotes]
        historico.append(sum(perdas) / len(perdas))
    return historico

estado = {"n": 0}
def passo(lote):
    estado["n"] += 1
    return sum(lote) / estado["n"]

print(treinar(passo, [[1, 1], [2, 2]], 3))
''', ["Para cada época, chame <code>passo</code> em todos os lotes e guarde a média."]),
        erros([("Usar Lightning sem entender o loop.", "Quando algo der errado, você não saberá o que ele está fazendo por baixo."), ("Lógica de dados misturada no modelo.", "Use <code>LightningDataModule</code> para os dados."), ("Esquecer <code>self.log</code>.", "Sem log, o early stopping não acha a métrica.")]),
        ponte("Frameworks de treino de LLMs", "<p>Para LLMs, há frameworks ainda mais especializados (Hugging Face Trainer e TRL, Accelerate, DeepSpeed, torchtune) que fazem a mesma separação: você define dados e modelo; eles cuidam de várias GPUs, precisão mista e checkpoints. Você vai usar o TRL para ajuste fino na Fase 5.</p>"),
        quiz([
            ("O que você escreve num <code>training_step</code>?", ["O loop inteiro.", "O cálculo da perda de um lote.", "O carregamento de dados."], 1, "O Trainer faz o resto."),
            ("Como ativar precisão mista no Lightning?", ["Reescrevendo o loop.", "Com o parâmetro <code>precision</code> do Trainer.", "Não é possível."], 1, "Configuração."),
            ("Qual a principal vantagem do Lightning?", ["Modelos mais precisos.", "Menos código repetido e menos bugs de infraestrutura.", "Não precisar de PyTorch."], 1, "Organização."),
        ]),
    ],
    ["Lightning separa o que é do modelo do que é infraestrutura.", "Você define passos e otimizador; o Trainer cuida do loop.", "GPU, logs, checkpoints e precisão mista por configuração."],
    "Fase 5: LLMs, começando por tokenização e embeddings.",
    livro=("D2L:chapter_linear-classification/softmax-regression-concise", "Seção 4.5, implementação concisa", "Como o livro organiza o treino em módulos reaproveitáveis?"))
