# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 5 (parte B): agentes, segurança e o funcionamento interno dos LLMs."""
from lesson_factory import *

AULAS = {}

AULAS["Agentes e uso de ferramentas"] = aula(
    35,
    "Um chatbot responde. Um agente <b>age</b>: decide o próximo passo, chama ferramentas (buscar, calcular, ler arquivos, enviar e-mail), observa o resultado e continua até cumprir o objetivo. É o mesmo LLM, agora dentro de um laço com ferramentas e regras.",
    ["entender o laço pensar → agir → observar (ReAct);", "descrever ferramentas com esquemas claros;", "pôr limites: número de passos, permissões e confirmação humana."],
    ["Usar APIs de LLMs (tool use)."],
    [
        chute("Um agente entrou num laço: chama a mesma busca 40 vezes. Qual a proteção mais simples?", ["Usar um modelo maior.", "Limite máximo de passos e detecção de chamadas repetidas.", "Desligar as ferramentas."], 1,
              ["Ajuda às vezes, mas não garante.", "Isso! Todo agente precisa de um teto de passos (e de custo) e de um jeito de parar quando repete.", "Sem ferramentas não há agente."],
              "Agentes falham de formas novas: laços, ações erradas, custo descontrolado."),
        concreto("O estagiário com acesso ao sistema", "<p>Dar ferramentas a um LLM é como dar ao estagiário acesso ao sistema da empresa. Ele faz muito mais, mas você define o que pode (ler, não apagar), pede confirmação para o que é irreversível e confere o trabalho.</p>"),
        passos("O laço ReAct", [
            ("<b>Pensar</b>: o modelo raciocina sobre o objetivo e o que falta.", "“Preciso do preço atual antes de calcular.”"),
            ("<b>Agir</b>: escolhe uma ferramenta e os argumentos.", "<code>buscar_preco(\"PETR4\")</code>"),
            ("<b>Observar</b>: o resultado volta para o histórico.", "“38,20”"),
            ("<b>Repetir ou terminar</b>: até a resposta final ou o limite de passos.", "Com registro de cada passo para depuração."),
        ]),
        cod("Um agente com limites", "Complete o agente: execute as ações do plano (o “modelo” falso), pare ao chegar em <code>fim</code>, recuse ferramentas fora da lista permitida e pare com <code>\"limite\"</code> se passar de <code>max_passos</code>. Guarde cada observação em <code>log</code>.",
            '''
def somar(a, b):
    return a + b

def apagar_tudo():
    return "apagado!"

PERMITIDAS = {"somar": somar}

def agente(plano, max_passos=3):
    log = []
    for passo, (ferramenta, args) in enumerate(plano):
        log.append("?")
    return "fim", log

print(agente([("somar", (2, 3)), ("fim", ())]))
print(agente([("apagar_tudo", ()), ("fim", ())]))
print(agente([("somar", (1, 1))] * 5))
''',
            [("Executa e termina", "assert agente([('somar', (2, 3)), ('fim', ())]) == ('fim', [5])"),
             ("Recusa ferramenta perigosa", "r, log = agente([('apagar_tudo', ()), ('fim', ())])\nassert log == ['recusado: apagar_tudo'], f'log = {log}'"),
             ("Respeita o limite", "r, log = agente([('somar', (1, 1))] * 5)\nassert r == 'limite' and log == [2, 2, 2], f'{r}, {log}'")],
            '''
def somar(a, b):
    return a + b

def apagar_tudo():
    return "apagado!"

PERMITIDAS = {"somar": somar}

def agente(plano, max_passos=3):
    log = []
    for passo, (ferramenta, args) in enumerate(plano):
        if ferramenta == "fim":
            return "fim", log
        if passo >= max_passos:
            return "limite", log
        if ferramenta not in PERMITIDAS:
            log.append(f"recusado: {ferramenta}")
            continue
        log.append(PERMITIDAS[ferramenta](*args))
    return "limite", log

print(agente([("somar", (2, 3)), ("fim", ())]))
print(agente([("apagar_tudo", ()), ("fim", ())]))
print(agente([("somar", (1, 1))] * 5))
''', ["Trate <code>fim</code> primeiro, depois o limite, depois a permissão.", "Ferramenta fora da lista: registre <code>f\"recusado: {ferramenta}\"</code> e continue."]),
        erros([("Descrições de ferramentas vagas.", "O modelo escolhe pela descrição: diga o que faz, quando usar e o formato dos argumentos."), ("Ações irreversíveis sem confirmação.", "Pagamentos, envios e exclusões pedem aprovação humana."), ("Agente para tudo.", "Se o fluxo é fixo, um programa comum com uma chamada de LLM é mais barato e confiável.")]),
        ponte("Do laço ao produto", "<p>Assistentes de código, agentes de pesquisa e de atendimento são este laço com boas ferramentas, memória e avaliação. Frameworks (LangGraph, SDKs de agentes) e o protocolo MCP ajudam a organizar, mas a lógica é a que você acabou de escrever.</p>"),
        quiz([
            ("O que diferencia um agente de um chatbot?", ["O tamanho do modelo.", "Ele decide e executa ações com ferramentas, em laço.", "A interface."], 1, "Agir, observar, repetir."),
            ("Qual proteção todo agente deve ter?", ["Limite de passos e permissões.", "Temperatura zero.", "Nenhuma."], 0, "Evita laços e danos."),
            ("Quando NÃO usar agente?", ["Quando o fluxo é fixo e previsível.", "Quando há ferramentas.", "Nunca."], 0, "Simples é melhor."),
        ]),
    ],
    ["Agente = LLM + ferramentas + laço pensar/agir/observar.", "Limites de passos, permissões e confirmação humana.", "Descrições claras de ferramentas guiam a escolha."],
    "Avaliação e segurança de sistemas com LLM.",
    livro=("PROMPT:techniques/react", "Prompt Engineering Guide, “ReAct”", "Como o ReAct intercala raciocínio e ação?"))

AULAS["Avaliação e segurança de sistemas com LLM"] = aula(
    30,
    "Um sistema com LLM pode funcionar na demonstração e falhar com clientes reais: inventar fatos, vazar dados, ser manipulado ou ofender alguém. Avaliar e proteger não é etapa final: é o que separa um protótipo de um produto.",
    ["montar um conjunto de avaliação com casos reais;", "conhecer os principais riscos (alucinação, injeção, vazamento);", "aplicar defesas em camadas."],
    ["RAG, agentes e engenharia de prompts."],
    [
        chute("Você mudou o prompt e as respostas “parecem melhores”. Como confirmar?", ["Perguntar a um colega.", "Rodar o mesmo conjunto de casos de teste antes e depois e comparar as notas.", "Publicar e ver se reclamam."], 1,
              ["Uma opinião não substitui medida.", "Isso! Sem um conjunto fixo de avaliação, cada mudança é um palpite.", "Arriscado e lento."],
              "Prompts são código: mudanças pedem testes."),
        concreto("O controle de qualidade da fábrica", "<p>Uma fábrica não confia que a peça saiu boa: testa amostras sempre, com critérios fixos. E tem barreiras: luvas, travas, alarmes. Avaliação é o controle de qualidade; segurança são as barreiras.</p>"),
        tabela("Riscos e defesas", ["Risco", "Exemplo", "Defesa"], [
            ["Alucinação", "inventa uma política da empresa", "RAG com citações, permitir “não sei”"],
            ["Prompt injection", "documento diz “ignore as instruções”", "separar dados de instruções, limitar ferramentas"],
            ["Vazamento", "revela dados de outro cliente", "controle de acesso antes da busca"],
            ["Conteúdo nocivo", "resposta ofensiva", "moderação na entrada e na saída"],
            ["Custo", "agente em laço", "limites de tokens e passos"],
        ], rot="O mapa de riscos"),
        cod("Mini avaliação", "Escreva <code>avaliar(sistema, casos)</code>: para cada caso, chame o sistema com a pergunta e confira se todas as palavras de <code>deve_conter</code> aparecem na resposta (sem diferenciar maiúsculas). Devolva a taxa de acerto e a lista das perguntas que falharam.",
            '''
def sistema(pergunta):
    respostas = {
        "prazo de devolução": "Você tem 30 dias para devolver.",
        "frete": "O frete é calculado no carrinho.",
    }
    return next((r for k, r in respostas.items() if k in pergunta.lower()), "Não sei.")

casos = [
    {"pergunta": "Qual o prazo de devolução?", "deve_conter": ["30 dias"]},
    {"pergunta": "O frete é grátis?", "deve_conter": ["grátis", "200"]},
    {"pergunta": "Qual a cor do céu?", "deve_conter": ["não sei"]},
]

def avaliar(sistema, casos):
    return 0.0, []

print(avaliar(sistema, casos))
''',
            [("Taxa e falhas", "taxa, falhas = avaliar(sistema, casos)\nassert abs(taxa - 2 / 3) < 1e-9 and falhas == ['O frete é grátis?'], f'{taxa}, {falhas}'")],
            '''
def sistema(pergunta):
    respostas = {
        "prazo de devolução": "Você tem 30 dias para devolver.",
        "frete": "O frete é calculado no carrinho.",
    }
    return next((r for k, r in respostas.items() if k in pergunta.lower()), "Não sei.")

casos = [
    {"pergunta": "Qual o prazo de devolução?", "deve_conter": ["30 dias"]},
    {"pergunta": "O frete é grátis?", "deve_conter": ["grátis", "200"]},
    {"pergunta": "Qual a cor do céu?", "deve_conter": ["não sei"]},
]

def avaliar(sistema, casos):
    falhas = []
    for c in casos:
        r = sistema(c["pergunta"]).lower()
        if not all(p.lower() in r for p in c["deve_conter"]):
            falhas.append(c["pergunta"])
    return (len(casos) - len(falhas)) / len(casos), falhas

print(avaliar(sistema, casos))
''', ["Use <code>all(p.lower() in resposta for p in ...)</code>.", "Taxa = acertos / total."]),
        erros([("Avaliar só com exemplos inventados por você.", "Use perguntas reais de usuários, incluindo as difíceis e as maliciosas."), ("Confiar numa única barreira.", "Defesa em camadas: prompt, filtros, permissões, monitoramento."), ("Não registrar as conversas.", "Sem logs (com cuidado com dados pessoais), você não descobre as falhas.")]),
        ponte("O próximo nível", "<p>As aulas seguintes aprofundam cada parte: avaliação de LLMs com evals e benchmarks, alucinações e prompt injection. A ideia central é sempre esta: medir com casos fixos e proteger em camadas.</p>"),
        quiz([
            ("Por que manter um conjunto fixo de casos de teste?", ["Para comparar versões de forma justa.", "Para treinar o modelo.", "Para reduzir custo."], 0, "Antes e depois."),
            ("Qual defesa reduz alucinações?", ["Temperatura alta.", "RAG com citações e permitir “não sei”.", "Prompts mais curtos."], 1, "Base nos documentos."),
            ("O que é defesa em camadas?", ["Várias barreiras independentes.", "Um prompt muito longo.", "Usar dois modelos iguais."], 0, "Se uma falha, outra segura."),
        ]),
    ],
    ["Avalie com casos reais e fixos, antes e depois de cada mudança.", "Riscos: alucinação, injeção, vazamento, conteúdo nocivo, custo.", "Proteja em camadas."],
    "Self-attention e multi-head.",
    livro=("PROMPT:risks/adversarial", "Prompt Engineering Guide, “Prompting adversarial”", "Que tipos de ataque o guia descreve?"))

AULAS["Self-attention e multi-head"] = aula(
    35,
    "Na aula de atenção você viu um token olhando para os outros. A <b>self-attention</b> faz isso para todos os tokens ao mesmo tempo, com matrizes. E a <b>multi-head</b> roda várias atenções em paralelo, cada uma especializada num tipo de relação: uma olha a gramática, outra os pronomes, outra o assunto.",
    ["calcular a self-attention com matrizes Q, K e V;", "aplicar a máscara causal;", "dividir em várias cabeças e juntar."],
    ["Mecanismo de atenção (aula-piloto), multiplicação de matrizes e softmax."],
    [
        chute("Por que dividir por √d dentro do softmax da atenção?", ["Para deixar mais rápido.", "Porque produtos escalares crescem com a dimensão e saturam o softmax.", "Por tradição."], 1,
              ["Não muda a velocidade.", "Isso! Com d grande, os produtos ficam enormes, o softmax vira quase “tudo ou nada” e o gradiente some.", "Tem um motivo matemático."],
              "A escala mantém a variância dos produtos perto de 1."),
        concreto("O grupo de estudo com especialistas", "<p>Num grupo de estudo, cada pessoa escuta as outras (self-attention). Com várias cabeças, é como se cada pessoa tivesse vários “ouvidos”: um presta atenção em quem fala de datas, outro em quem fala de nomes. No fim, junta tudo que ouviu.</p>"),
        nota("A fórmula", [
            (r"$Q = XW_Q,\ K = XW_K,\ V = XW_V$", "projeções", "Cada token vira pergunta, chave e valor."),
            (r"$\text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}} + M\right)V$", "atenção", "M é a máscara: −∞ onde não pode olhar."),
            ("Máscara causal", "não espiar o futuro", "Na geração, o token i só vê os tokens 0 a i."),
            ("h cabeças", "multi-head", "Cada cabeça usa d/h dimensões; as saídas são concatenadas e projetadas."),
        ], rot="Agora sim, a fórmula"),
        cod("Self-attention com máscara causal", "Implemente <code>atencao(Q, K, V, causal)</code> com NumPy: pontuações escaladas, máscara causal opcional (−∞ acima da diagonal), softmax por linha e média ponderada dos valores. Devolva a saída e os pesos.",
            '''
import numpy as np

def softmax(x):
    x = x - x.max(axis=-1, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=-1, keepdims=True)

def atencao(Q, K, V, causal=False):
    pesos = np.zeros((Q.shape[0], K.shape[0]))
    return pesos @ V, pesos

rng = np.random.default_rng(0)
X = rng.normal(size=(4, 8))
out, pesos = atencao(X, X, X, causal=True)
print(pesos.round(2))
''',
            [("Pesos somam 1", "import numpy as np\nassert np.allclose(pesos.sum(axis=1), 1)"),
             ("Máscara causal", "import numpy as np\nassert np.allclose(np.triu(pesos, 1), 0) and pesos[0, 0] == 1"),
             ("Sem máscara olha tudo", "import numpy as np\n_, p2 = atencao(X, X, X)\nassert (p2 > 0).all()"),
             ("Fórmula", "import numpy as np\n_, p3 = atencao(X, X, X)\nesp = softmax(X @ X.T / np.sqrt(8))\nassert np.allclose(p3, esp)")],
            '''
import numpy as np

def softmax(x):
    x = x - x.max(axis=-1, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=-1, keepdims=True)

def atencao(Q, K, V, causal=False):
    s = Q @ K.T / np.sqrt(K.shape[1])
    if causal:
        s = np.where(np.triu(np.ones_like(s), 1) == 1, -np.inf, s)
    pesos = softmax(s)
    return pesos @ V, pesos

rng = np.random.default_rng(0)
X = rng.normal(size=(4, 8))
out, pesos = atencao(X, X, X, causal=True)
print(pesos.round(2))
''', ["Pontuações: <code>Q @ K.T / np.sqrt(d)</code>.", "Máscara: <code>np.where(np.triu(np.ones_like(s), 1) == 1, -np.inf, s)</code>."]),
        cod("Dividindo em cabeças", "Para multi-head, a matriz (tokens × d) é dividida em h cabeças de d/h colunas. Escreva <code>dividir(X, h)</code> que devolve um array (h × tokens × d/h) e <code>juntar</code>, que desfaz.",
            '''
import numpy as np

def dividir(X, h):
    return X

def juntar(H):
    return H

X = np.arange(24).reshape(3, 8)
H = dividir(X, 2)
print(H.shape)
''',
            [("Formato", "assert dividir(np.zeros((3, 8)), 2).shape == (2, 3, 4)"),
             ("Primeira cabeça = primeiras colunas", "import numpy as np\nassert np.array_equal(dividir(X, 2)[0], X[:, :4])"),
             ("Ida e volta", "import numpy as np\nassert np.array_equal(juntar(dividir(X, 4)), X)")],
            '''
import numpy as np

def dividir(X, h):
    n, d = X.shape
    return X.reshape(n, h, d // h).transpose(1, 0, 2)

def juntar(H):
    h, n, dh = H.shape
    return H.transpose(1, 0, 2).reshape(n, h * dh)

X = np.arange(24).reshape(3, 8)
H = dividir(X, 2)
print(H.shape)
''', ["<code>reshape(n, h, d // h)</code> e depois <code>transpose(1, 0, 2)</code>.", "Para juntar, faça o caminho inverso."], rot="Mão no código · nível 2"),
        erros([("Esquecer a escala √d.", "O treino fica instável."), ("Esquecer a máscara causal num decodificador.", "O modelo “cola” vendo a resposta e não aprende a gerar."), ("Achar que cabeças são definidas à mão.", "A especialização emerge do treino.")]),
        ponte("O custo quadrático", "<p>A matriz de pesos tem tokens × tokens entradas: dobrar o contexto quadruplica o custo da atenção. É por isso que existem FlashAttention, atenção esparsa e o KV cache, assunto de uma das próximas aulas.</p>"),
        quiz([
            ("O que a máscara causal impede?", ["Que um token veja tokens futuros.", "Que o modelo treine.", "Tokens repetidos."], 0, "Geração da esquerda para a direita."),
            ("Para que servem várias cabeças?", ["Capturar tipos diferentes de relação em paralelo.", "Reduzir o vocabulário.", "Guardar o histórico."], 0, "Especialização."),
            ("O custo da atenção cresce com o contexto de forma:", ["Linear.", "Quadrática.", "Constante."], 1, "n × n."),
        ]),
    ],
    ["softmax(QKᵀ/√d + M)V para todos os tokens de uma vez.", "Máscara causal: sem espiar o futuro.", "Multi-head: várias atenções em paralelo, concatenadas."],
    "Positional encoding.",
    livro=("D2L:chapter_attention-mechanisms-and-transformers/multihead-attention", "Seção 11.5, “Multi-Head Attention”", "Como o livro implementa a divisão em cabeças?"))

AULAS["Positional encoding"] = aula(
    25,
    "A atenção, sozinha, não sabe a ordem das palavras: “o cão mordeu o homem” e “o homem mordeu o cão” dariam o mesmo resultado. O positional encoding acrescenta a cada token um sinal da sua posição, e o modelo passa a distinguir ordem.",
    ["entender por que a atenção ignora a ordem;", "calcular o encoding senoidal;", "conhecer as alternativas modernas (aprendido, RoPE)."],
    ["Self-attention, seno e cosseno."],
    [
        chute("Se embaralharmos os tokens de entrada da self-attention (sem posição), o que acontece com as saídas?", ["Mudam completamente.", "São as mesmas, só que embaralhadas na mesma ordem.", "Dá erro."], 1,
              ["Parece intuitivo, mas não.", "Isso! A atenção é uma operação sobre um conjunto: não tem noção de primeiro ou último.", "Funciona normalmente."],
              "Sem posição, a frase vira um saco de palavras."),
        concreto("O relógio de vários ponteiros", "<p>O encoding senoidal funciona como um relógio com muitos ponteiros girando em velocidades diferentes: o dos segundos muda rápido, o das horas devagar. Olhando todos juntos, você sabe exatamente que horas são. Cada posição tem uma combinação única.</p>"),
        nota("As fórmulas", [
            (r"$PE_{(p,\,2i)} = \sin\left(p / 10000^{2i/d}\right)$", "dimensões pares", "Posição p, dimensão 2i."),
            (r"$PE_{(p,\,2i+1)} = \cos\left(p / 10000^{2i/d}\right)$", "dimensões ímpares", "Frequências diferentes por dimensão."),
            ("Aprendido", "uma tabela", "Um vetor treinável por posição (BERT, GPT-2)."),
            ("RoPE", "rotação", "Gira Q e K pelo ângulo da posição; usado em Llama, Qwen e Mistral."),
        ], rot="Agora sim, a fórmula"),
        cod("Encoding senoidal", "Implemente <code>pe(n, d)</code> que devolve a matriz (n × d) do positional encoding senoidal.",
            '''
import numpy as np

def pe(n, d):
    return np.zeros((n, d))

P = pe(50, 16)
print(P[:3, :4].round(3))
''',
            [("Posição 0", "import numpy as np\nP = pe(10, 8)\nassert np.allclose(P[0, 0::2], 0) and np.allclose(P[0, 1::2], 1)"),
             ("Valor conhecido", "import numpy as np\nassert abs(pe(10, 8)[1, 0] - np.sin(1)) < 1e-9"),
             ("Posições distintas", "import numpy as np\nP = pe(50, 16)\nassert len({tuple(np.round(l, 6)) for l in P}) == 50")],
            '''
import numpy as np

def pe(n, d):
    pos = np.arange(n)[:, None]
    i = np.arange(0, d, 2)[None, :]
    ang = pos / 10000 ** (i / d)
    P = np.zeros((n, d))
    P[:, 0::2] = np.sin(ang)
    P[:, 1::2] = np.cos(ang)
    return P

P = pe(50, 16)
print(P[:3, :4].round(3))
''', ["Ângulos: <code>pos / 10000 ** (i / d)</code>, com i = 0, 2, 4...", "Pares recebem seno, ímpares cosseno."]),
        cod("A atenção ignora a ordem", "Comprove: calcule a self-attention (sem posição) de X e de X com as linhas invertidas. Mostre que a saída da versão invertida é a saída original invertida. Depois some o encoding e mostre que isso deixa de valer.",
            '''
import numpy as np

def atencao(X):
    s = X @ X.T / np.sqrt(X.shape[1])
    e = np.exp(s - s.max(axis=1, keepdims=True))
    return (e / e.sum(axis=1, keepdims=True)) @ X

def pe(n, d):
    pos = np.arange(n)[:, None]
    ang = pos / 10000 ** (np.arange(0, d, 2)[None, :] / d)
    P = np.zeros((n, d))
    P[:, 0::2], P[:, 1::2] = np.sin(ang), np.cos(ang)
    return P

rng = np.random.default_rng(1)
X = rng.normal(size=(5, 8))
sem_posicao_igual = None
com_posicao_igual = None
print(sem_posicao_igual, com_posicao_igual)
''',
            [("Sem posição: só permuta", "assert sem_posicao_igual is True or sem_posicao_igual == True"),
             ("Com posição: muda", "assert com_posicao_igual is False or com_posicao_igual == False")],
            '''
import numpy as np

def atencao(X):
    s = X @ X.T / np.sqrt(X.shape[1])
    e = np.exp(s - s.max(axis=1, keepdims=True))
    return (e / e.sum(axis=1, keepdims=True)) @ X

def pe(n, d):
    pos = np.arange(n)[:, None]
    ang = pos / 10000 ** (np.arange(0, d, 2)[None, :] / d)
    P = np.zeros((n, d))
    P[:, 0::2], P[:, 1::2] = np.sin(ang), np.cos(ang)
    return P

rng = np.random.default_rng(1)
X = rng.normal(size=(5, 8))
sem_posicao_igual = bool(np.allclose(atencao(X[::-1]), atencao(X)[::-1]))
P = pe(5, 8)
com_posicao_igual = bool(np.allclose(atencao(X[::-1] + P), atencao(X + P)[::-1]))
print(sem_posicao_igual, com_posicao_igual)
''', ["Compare <code>atencao(X[::-1])</code> com <code>atencao(X)[::-1]</code> usando <code>np.allclose</code>.", "Repita somando <code>pe(5, 8)</code> à entrada nos dois casos."], rot="Mão no código · nível 2"),
        erros([("Achar que o modelo “sabe” a ordem por ler da esquerda para a direita.", "Sem encoding (ou máscara), não sabe."), ("Usar contexto maior que o treinado com encoding aprendido.", "Não há vetor para essas posições; RoPE com escalonamento lida melhor."), ("Confundir posição absoluta e relativa.", "RoPE codifica a distância entre tokens no produto Q·K.")]),
        ponte("Contextos longos", "<p>Boa parte do avanço para janelas de centenas de milhares de tokens veio de truques de posição: RoPE, interpolação de posições, YaRN. A janela de contexto é limitada pela memória e pelo que o encoding aguenta.</p>"),
        quiz([
            ("Por que a atenção precisa de positional encoding?", ["Ela não distingue a ordem dos tokens.", "Para ficar mais rápida.", "Para reduzir memória."], 0, "Operação sobre conjunto."),
            ("O encoding senoidal usa:", ["Ruído aleatório.", "Senos e cossenos de frequências diferentes.", "Números inteiros."], 1, "Relógio de ponteiros."),
            ("Qual técnica os LLMs abertos atuais mais usam?", ["RoPE.", "One-hot.", "Nenhuma."], 0, "Rotação de Q e K."),
        ]),
    ],
    ["A atenção sozinha ignora a ordem.", "Encoding senoidal: senos e cossenos em várias frequências.", "Modelos modernos usam RoPE."],
    "Encoder vs. decoder (BERT vs. GPT).",
    livro=("D2L:chapter_attention-mechanisms-and-transformers/self-attention-and-positional-encoding", "Seção 11.6, “Self-Attention and Positional Encoding”", "Que propriedade das posições relativas o livro demonstra?"))

AULAS["Encoder vs. decoder (BERT vs. GPT)"] = aula(
    25,
    "BERT e GPT usam os mesmos blocos de Transformer, mas com uma diferença decisiva: o BERT vê a frase inteira (encoder) e é ótimo para entender; o GPT só vê o passado (decoder) e é feito para gerar. Saber qual usar economiza muito dinheiro.",
    ["diferenciar encoder, decoder e encoder-decoder;", "relacionar cada tipo à sua tarefa de pré-treino;", "escolher o modelo certo para classificação, busca ou geração."],
    ["Self-attention e máscara causal."],
    [
        chute("Você precisa classificar 10 milhões de avaliações em positiva ou negativa. Qual a escolha mais econômica?", ["Um LLM gigante de geração.", "Um encoder pequeno (tipo BERT) ajustado para a tarefa.", "Um modelo de imagens."], 1,
              ["Funciona, mas custa muito mais por avaliação.", "Isso! Encoders pequenos ajustados são rápidos, baratos e muito precisos para classificar.", "Não é tarefa de imagem."],
              "Gerar é caro; para entender e classificar, encoders bastam."),
        concreto("O leitor e o escritor", "<p>O encoder é um leitor atento: lê o texto inteiro, para frente e para trás, antes de opinar. O decoder é um escritor: escreve uma palavra de cada vez, sem saber o que vem depois. O encoder-decoder é o tradutor: lê tudo e depois escreve.</p>"),
        tabela("Os três tipos", ["Tipo", "Atenção", "Pré-treino", "Exemplos", "Bom para"], [
            ["Encoder", "bidirecional", "preencher palavras mascaradas", "BERT, RoBERTa", "classificar, extrair, embeddings"],
            ["Decoder", "causal", "prever o próximo token", "GPT, Llama, Claude", "gerar, conversar, raciocinar"],
            ["Encoder-decoder", "bidirecional + causal", "reconstruir trechos", "T5, BART", "traduzir, resumir"],
        ]),
        cod("Máscara de cada tipo", "Escreva <code>mascara(n, tipo)</code> que devolve uma matriz n × n de 0/1 dizendo quem pode olhar para quem: <code>\"encoder\"</code> (todos veem todos) ou <code>\"decoder\"</code> (só o passado e a própria posição).",
            '''
def mascara(n, tipo):
    return [[0] * n for _ in range(n)]

for linha in mascara(3, "decoder"):
    print(linha)
''',
            [("Encoder", "assert mascara(3, 'encoder') == [[1, 1, 1], [1, 1, 1], [1, 1, 1]]"),
             ("Decoder", "assert mascara(3, 'decoder') == [[1, 0, 0], [1, 1, 0], [1, 1, 1]], f'{mascara(3, \"decoder\")}'")],
            '''
def mascara(n, tipo):
    if tipo == "encoder":
        return [[1] * n for _ in range(n)]
    return [[1 if j <= i else 0 for j in range(n)] for i in range(n)]

for linha in mascara(3, "decoder"):
    print(linha)
''', ["Decoder: a posição i vê j quando <code>j &lt;= i</code>."]),
        cod("Mascarar para pré-treinar um encoder", "No pré-treino do BERT, ~15% dos tokens viram <code>[MASK]</code> e o modelo tenta adivinhá-los. Escreva <code>mascarar(tokens, posicoes)</code> que devolve a entrada mascarada e o dicionário {posição: token original}.",
            '''
def mascarar(tokens, posicoes):
    return tokens, {}

print(mascarar(["o", "gato", "subiu", "no", "telhado"], [1, 4]))
''',
            [("Mascara e guarda as respostas", "assert mascarar(['o', 'gato', 'subiu', 'no', 'telhado'], [1, 4]) == (['o', '[MASK]', 'subiu', 'no', '[MASK]'], {1: 'gato', 4: 'telhado'})"),
             ("Não altera a lista original", "t = ['a', 'b']\nmascarar(t, [0])\nassert t == ['a', 'b']")],
            '''
def mascarar(tokens, posicoes):
    entrada = list(tokens)
    alvos = {}
    for p in posicoes:
        alvos[p] = entrada[p]
        entrada[p] = "[MASK]"
    return entrada, alvos

print(mascarar(["o", "gato", "subiu", "no", "telhado"], [1, 4]))
''', ["Copie a lista com <code>list(tokens)</code> antes de alterar."], rot="Mão no código · nível 2"),
        erros([("Usar um LLM gigante para tudo.", "Para classificar e gerar embeddings, encoders pequenos são muito mais baratos."), ("Tentar gerar texto com BERT.", "Ele não foi treinado para isso."), ("Achar que encoders morreram.", "Modelos de embeddings de RAG são, em geral, encoders.")]),
        ponte("No seu RAG", "<p>Num RAG típico, um <b>encoder</b> gera os embeddings para a busca, outro encoder (cross-encoder) reordena os resultados, e um <b>decoder</b> escreve a resposta. Os dois tipos trabalham juntos.</p>"),
        quiz([
            ("Qual tipo vê a frase inteira nos dois sentidos?", ["Encoder.", "Decoder.", "Nenhum."], 0, "Bidirecional."),
            ("GPT é um modelo:", ["Encoder.", "Decoder.", "Encoder-decoder."], 1, "Causal."),
            ("Como o BERT é pré-treinado?", ["Prevendo o próximo token.", "Adivinhando tokens mascarados.", "Com imagens."], 1, "Masked language modeling."),
        ]),
    ],
    ["Encoder: bidirecional, entende (BERT).", "Decoder: causal, gera (GPT).", "Escolha pelo trabalho: classificar e buscar com encoder, gerar com decoder."],
    "Janela de contexto e KV cache.",
    livro=("HF:chapter1/6", "LLM Course, capítulo 1, “Transformer Architectures”", "Que exemplos de cada arquitetura o curso cita?"))

AULAS["Janela de contexto e KV cache"] = aula(
    30,
    "A janela de contexto é quanto texto o modelo vê de uma vez: prompt, documentos e a resposta que está gerando. E para gerar cada novo token sem recalcular tudo, o modelo guarda as chaves e valores dos tokens anteriores, o KV cache, que vira o principal consumidor de memória na inferência.",
    ["entender o que ocupa a janela de contexto;", "calcular a memória do KV cache;", "saber por que a primeira resposta demora e as seguintes não."],
    ["Self-attention e multi-head."],
    [
        chute("Por que o primeiro token de uma resposta demora mais que os seguintes?", ["O servidor acorda devagar.", "O modelo processa o prompt inteiro primeiro (prefill); depois reaproveita o cache e só calcula o token novo.", "É proposital."], 1,
              ["Pode haver fila, mas há um motivo técnico.", "Isso! Prefill processa todo o prompt e enche o KV cache; a decodificação faz um token por vez.", "Não é proposital."],
              "Tempo até o primeiro token cresce com o tamanho do prompt."),
        concreto("As anotações da reunião", "<p>Sem anotações, para cada frase nova você precisaria reouvir a reunião inteira. Com anotações (o KV cache), basta ler o que anotou e acrescentar a frase nova. O caderno, porém, cresce a cada frase e ocupa espaço.</p>"),
        nota("As contas", [
            ("Janela de contexto", "limite total", "Entrada + saída, em tokens (de 8 mil a mais de 1 milhão)."),
            ("Prefill", "processar o prompt", "Paralelo, pesado em computação."),
            ("Decodificação", "um token por vez", "Limitada pela leitura de memória."),
            (r"$2 \times L \times h_{kv} \times d_h \times n \times b$", "memória do KV cache", "2 (K e V) × camadas × cabeças KV × dimensão por cabeça × tokens × bytes."),
            ("GQA", "grouped-query attention", "Várias cabeças de Q compartilham K e V: cache menor."),
        ], rot="Agora sim, as contas"),
        cod("Memória do KV cache", "Calcule o KV cache em GB para um modelo de 32 camadas, 8 cabeças KV de dimensão 128, em float16 (2 bytes), com 128 mil tokens de contexto. Depois, quantos usuários simultâneos com 8 mil tokens cabem em 40 GB livres?",
            '''
def kv_cache_gb(camadas, cabecas_kv, dim, tokens, bytes_=2):
    return 0.0

def usuarios(memoria_gb, tokens_por_usuario, **modelo):
    return 0

M = dict(camadas=32, cabecas_kv=8, dim=128)
print(round(kv_cache_gb(**M, tokens=128_000), 2), usuarios(40, 8000, **M))
''',
            [("Cache de 128 mil tokens", "assert abs(kv_cache_gb(32, 8, 128, 128_000) - 2 * 32 * 8 * 128 * 128_000 * 2 / 1e9) < 1e-9, f'{kv_cache_gb(32, 8, 128, 128_000)}'"),
             ("Usuários simultâneos", "assert usuarios(40, 8000, camadas=32, cabecas_kv=8, dim=128) == 38, f'{usuarios(40, 8000, camadas=32, cabecas_kv=8, dim=128)}'")],
            '''
def kv_cache_gb(camadas, cabecas_kv, dim, tokens, bytes_=2):
    return 2 * camadas * cabecas_kv * dim * tokens * bytes_ / 1e9

def usuarios(memoria_gb, tokens_por_usuario, **modelo):
    return int(memoria_gb // kv_cache_gb(tokens=tokens_por_usuario, **modelo))

M = dict(camadas=32, cabecas_kv=8, dim=128)
print(round(kv_cache_gb(**M, tokens=128_000), 2), usuarios(40, 8000, **M))
''', ["Multiplique tudo e divida por 1e9.", "Usuários = memória // cache de um usuário."], exp="<p>Um único contexto de 128 mil tokens ocupa ~16,8 GB. Por isso contextos longos são caros e provedores cobram mais por eles.</p>"),
        cod("Cabendo na janela", "Escreva <code>cortar_historico(mensagens, limite)</code>: mantenha sempre a primeira mensagem (o sistema) e o máximo de mensagens mais recentes cujo total de tokens (use <code>len(texto.split())</code>) caiba no limite.",
            '''
def tokens(m):
    return len(m.split())

def cortar_historico(mensagens, limite):
    return mensagens

hist = ["regras do sistema aqui", "oi", "tudo bem com você", "me explique RAG por favor", "claro aqui vai"]
print(cortar_historico(hist, 10))
''',
            [("Mantém sistema e as mais recentes", "assert cortar_historico(hist, 10) == ['regras do sistema aqui', 'claro aqui vai'], f'{cortar_historico(hist, 10)}'"),
             ("Tudo cabe", "assert cortar_historico(hist, 100) == hist"),
             ("Ordem preservada", "assert cortar_historico(hist, 14) == ['regras do sistema aqui', 'tudo bem com você', 'claro aqui vai'] or cortar_historico(hist, 14) == ['regras do sistema aqui', 'me explique RAG por favor', 'claro aqui vai']")],
            '''
def tokens(m):
    return len(m.split())

def cortar_historico(mensagens, limite):
    sistema, resto = mensagens[0], mensagens[1:]
    total = tokens(sistema)
    mantidas = []
    for m in reversed(resto):
        if total + tokens(m) > limite:
            break
        mantidas.insert(0, m)
        total += tokens(m)
    return [sistema] + mantidas

hist = ["regras do sistema aqui", "oi", "tudo bem com você", "me explique RAG por favor", "claro aqui vai"]
print(cortar_historico(hist, 10))
''', ["Percorra do fim para o começo com <code>reversed</code>.", "Pare quando a próxima não couber."], rot="Mão no código · nível 2"),
        erros([("Achar que tudo na janela é usado igualmente bem.", "Modelos lembram melhor o começo e o fim; informações no meio de contextos longos se perdem mais."), ("Encher a janela “por garantia”.", "Mais tokens = mais custo, mais latência e às vezes respostas piores."), ("Esquecer que a resposta também ocupa a janela.", "Reserve espaço para a saída.")]),
        ponte("Cache de prompt", "<p>Provedores oferecem cache de prompt: se o começo do prompt (instruções, documentos) se repete entre chamadas, o KV cache é reaproveitado e a chamada sai mais barata e rápida. Coloque a parte fixa no início.</p>"),
        quiz([
            ("O que o KV cache guarda?", ["As chaves e valores dos tokens já processados.", "As respostas antigas.", "Os pesos do modelo."], 0, "Evita recalcular."),
            ("A memória do KV cache cresce com:", ["O número de tokens no contexto.", "A temperatura.", "O idioma."], 0, "Linear em n."),
            ("O que é o prefill?", ["Processar o prompt inteiro antes de gerar.", "Treinar o modelo.", "Apagar o cache."], 0, "Primeira etapa."),
        ]),
    ],
    ["A janela inclui prompt e resposta.", "KV cache evita recalcular, mas ocupa muita memória.", "Contexto longo custa caro: corte e organize o histórico."],
    "Quantização (4-bit, 8-bit).",
    livro=("HF:chapter1/8", "LLM Course, capítulo 1, “Deep dive into text generation inference”", "Como o curso explica prefill, decodificação e KV cache?"))

AULAS["Quantização (4-bit, 8-bit)"] = aula(
    30,
    "Um modelo de 70 bilhões de parâmetros em float16 ocupa 140 GB. Em 4 bits, cerca de 35 GB, e a qualidade cai muito pouco. Quantizar é guardar os pesos com menos bits, trocando uma pequena perda de precisão por modelos que cabem em GPUs comuns e rodam mais rápido.",
    ["calcular a memória de um modelo por precisão;", "implementar a quantização simétrica em 8 bits;", "entender quantização por blocos e formatos como GGUF."],
    ["Mixed precision (Fase 4) e NumPy."],
    [
        chute("Um modelo de 8 bilhões de parâmetros em 4 bits ocupa aproximadamente:", ["32 GB.", "16 GB.", "4 GB."], 2,
              ["Isso seria em float32 (4 bytes).", "Isso seria em float16.", "Isso! 4 bits = meio byte: 8 bi × 0,5 = 4 GB (mais um pouco para escalas e cache)."],
              "Memória ≈ parâmetros × bits / 8."),
        concreto("Arredondar o preço", "<p>Em vez de anotar 12,3487 reais você anota 12,35. Perde-se um pouquinho, mas a lista fica menor e ninguém percebe a diferença. A quantização arredonda cada peso para um de poucos valores possíveis (256 em 8 bits, 16 em 4 bits).</p>"),
        nota("A quantização simétrica", [
            (r"$s = \frac{\max|w|}{127}$", "escala", "Mapeia o maior peso para 127."),
            (r"$q = \text{round}(w / s)$", "quantizar", "Inteiros de −127 a 127 (int8)."),
            (r"$\hat w = q \cdot s$", "desquantizar", "Aproximação do peso original."),
            ("Por blocos", "uma escala a cada 32–128 pesos", "Um valor extremo só estraga o próprio bloco."),
            ("GGUF, GPTQ, AWQ, bitsandbytes", "formatos e métodos", "GGUF para llama.cpp/Ollama; os outros em GPUs."),
        ], rot="Agora sim, a fórmula"),
        cod("Quantizar em int8", "Implemente <code>quantizar(w)</code> (devolve os inteiros int8 e a escala) e <code>desquantizar(q, s)</code>. O erro máximo deve ser no máximo meia escala.",
            '''
import numpy as np

def quantizar(w):
    return w.astype(np.int8), 1.0

def desquantizar(q, s):
    return q.astype(np.float32)

rng = np.random.default_rng(0)
w = rng.normal(0, 0.02, size=1000).astype(np.float32)
q, s = quantizar(w)
print(q.dtype, s, np.abs(desquantizar(q, s) - w).max())
''',
            [("Tipo e intervalo", "import numpy as np\nq, s = quantizar(w)\nassert q.dtype == np.int8 and np.abs(q).max() == 127"),
             ("Erro pequeno", "import numpy as np\nq, s = quantizar(w)\nassert np.abs(desquantizar(q, s) - w).max() <= s / 2 + 1e-9")],
            '''
import numpy as np

def quantizar(w):
    s = np.abs(w).max() / 127
    q = np.round(w / s).astype(np.int8)
    return q, s

def desquantizar(q, s):
    return q.astype(np.float32) * s

rng = np.random.default_rng(0)
w = rng.normal(0, 0.02, size=1000).astype(np.float32)
q, s = quantizar(w)
print(q.dtype, s, np.abs(desquantizar(q, s) - w).max())
''', ["Escala: <code>np.abs(w).max() / 127</code>.", "Arredonde com <code>np.round</code> antes de converter."]),
        cod("Por que quantizar por blocos", "Um único valor extremo estraga a escala de todos os pesos. Compare o erro médio da quantização em 4 bits (inteiros de −7 a 7) com uma escala só e com uma escala a cada bloco de 32 pesos.",
            '''
import numpy as np

def q4(w):
    s = np.abs(w).max() / 7
    return np.round(w / s) * s

def q4_blocos(w, bloco=32):
    return q4(w)  # troque: uma escala por bloco

rng = np.random.default_rng(0)
w = rng.normal(0, 0.02, size=1024)
w[5] = 1.0  # um peso extremo
erro_um = np.abs(q4(w) - w).mean()
erro_blocos = np.abs(q4_blocos(w) - w).mean()
print(erro_um, erro_blocos)
''',
            [("Blocos reduzem muito o erro", "assert erro_blocos < erro_um / 3, f'{erro_um}, {erro_blocos}'"),
             ("Mesmo formato", "assert q4_blocos(w).shape == w.shape")],
            '''
import numpy as np

def q4(w):
    s = np.abs(w).max() / 7
    return np.round(w / s) * s

def q4_blocos(w, bloco=32):
    return np.concatenate([q4(w[i:i + bloco]) for i in range(0, len(w), bloco)])

rng = np.random.default_rng(0)
w = rng.normal(0, 0.02, size=1024)
w[5] = 1.0
erro_um = np.abs(q4(w) - w).mean()
erro_blocos = np.abs(q4_blocos(w) - w).mean()
print(erro_um, erro_blocos)
''', ["Aplique <code>q4</code> em cada fatia <code>w[i:i + bloco]</code> e junte com <code>np.concatenate</code>."], rot="Mão no código · nível 2"),
        erros([("Quantizar abaixo de 4 bits sem testar.", "Em 2–3 bits a qualidade costuma cair bastante."), ("Comparar só pela memória.", "Meça a qualidade na sua tarefa antes de decidir."), ("Esquecer o KV cache.", "Ele também ocupa memória e pode ser quantizado.")]),
        ponte("Na sua máquina", "<p>Os modelos que você baixa no Ollama já vêm quantizados (por exemplo Q4_K_M, um 4 bits por blocos). É a quantização que permite rodar um modelo de 8 bilhões num notebook com 16 GB de RAM, assunto da última aula desta fase.</p>"),
        quiz([
            ("Quantização troca:", ["Um pouco de precisão por menos memória e mais velocidade.", "Velocidade por precisão.", "Nada."], 0, "Compressão."),
            ("Quantos valores diferentes cabem em 4 bits?", ["4.", "16.", "256."], 1, "2⁴."),
            ("Por que quantizar por blocos?", ["Valores extremos só afetam o próprio bloco.", "É mais simples.", "Usa mais memória de propósito."], 0, "Escalas locais."),
        ]),
    ],
    ["Memória ≈ parâmetros × bits / 8.", "Escala, arredondar, multiplicar de volta.", "Blocos com escalas próprias protegem contra valores extremos."],
    "Scaling laws.",
    livro=("HF:chapter1/8", "LLM Course, capítulo 1, seção sobre inferência", "Que técnicas de otimização de inferência o curso menciona?"))

AULAS["Scaling laws"] = aula(
    25,
    "Por que as empresas gastam bilhões treinando modelos cada vez maiores? Porque a perda dos modelos cai de forma previsível, como uma lei de potência, quando aumentamos parâmetros, dados e computação. Essas “leis de escala” permitem prever o desempenho antes de gastar.",
    ["entender a relação de lei de potência;", "estimar a computação de um treino (6·N·D);", "conhecer a regra de Chinchilla sobre dados e parâmetros."],
    ["Função de perda, logaritmos e regressão linear."],
    [
        chute("Um laboratório tem orçamento fixo de computação. Segundo Chinchilla, é melhor:", ["Um modelo enorme com poucos dados.", "Equilibrar: cerca de 20 tokens de treino por parâmetro.", "Um modelo minúsculo com dados infinitos."], 1,
              ["Foi o erro de modelos como o GPT-3: grandes e pouco treinados.", "Isso! Para um orçamento ótimo, parâmetros e dados crescem juntos.", "Também desperdiça."],
              "Hoje muitos modelos treinam com muito mais que 20 tokens por parâmetro, para ficarem baratos na inferência."),
        concreto("Estudar mais rende menos a cada hora", "<p>A primeira hora de estudo faz sua nota subir muito; a centésima, pouco. Mas a melhora continua de um jeito previsível. Em escala log-log, essa curva vira uma reta, e retas dá para extrapolar.</p>"),
        nota("As fórmulas", [
            (r"$L(N) \approx \left(\frac{N_c}{N}\right)^{\alpha}$", "lei de potência", "A perda cai com o número de parâmetros N."),
            (r"$\log L = \alpha \log N_c - \alpha \log N$", "reta no log-log", "Inclinação −α."),
            (r"$C \approx 6\,N\,D$", "computação do treino", "Operações ≈ 6 × parâmetros × tokens."),
            ("Chinchilla", "D ≈ 20·N", "Proporção ótima para um orçamento fixo."),
        ], rot="Agora sim, as fórmulas"),
        cod("Estimando o expoente", "Dados de perda por tamanho de modelo seguem uma lei de potência. Ajuste uma reta em log-log (use <code>np.polyfit</code>) para achar α e preveja a perda de um modelo de 10 bilhões.",
            '''
import numpy as np

N = np.array([1e7, 1e8, 1e9])
L = 5.0 * (N / 1e7) ** -0.08

alfa = 0.0
previsao = 0.0
print(round(alfa, 3), round(previsao, 3))
''',
            [("Expoente", "assert abs(alfa - 0.08) < 1e-6, f'alfa = {alfa}'"),
             ("Previsão", "assert abs(previsao - 5.0 * (1e10 / 1e7) ** -0.08) < 1e-6, f'{previsao}'")],
            '''
import numpy as np

N = np.array([1e7, 1e8, 1e9])
L = 5.0 * (N / 1e7) ** -0.08

inclinacao, intercepto = np.polyfit(np.log(N), np.log(L), 1)
alfa = -inclinacao
previsao = float(np.exp(intercepto + inclinacao * np.log(1e10)))
print(round(alfa, 3), round(previsao, 3))
''', ["<code>np.polyfit(np.log(N), np.log(L), 1)</code> devolve inclinação e intercepto.", "α = −inclinação; previsão = exp(intercepto + inclinação · log(1e10))."]),
        cod("O orçamento de um treino", "Escreva <code>chinchilla(C)</code>: dado o orçamento C (operações), use C = 6·N·D e D = 20·N para achar N (parâmetros) e D (tokens). E <code>dias(C, flops_gpu, gpus)</code> com 40% de aproveitamento.",
            '''
import math

def chinchilla(C):
    return 0, 0

def dias(C, flops_gpu, gpus, aproveitamento=0.4):
    return 0.0

N, D = chinchilla(1e24)
print(f"{N:.2e} parâmetros, {D:.2e} tokens, {dias(1e24, 1e15, 1000):.0f} dias")
''',
            [("Proporção", "N, D = chinchilla(1e24)\nassert abs(D / N - 20) < 1e-6 and abs(6 * N * D - 1e24) / 1e24 < 1e-9"),
             ("Dias", "assert abs(dias(1e24, 1e15, 1000) - 1e24 / (1e15 * 1000 * 0.4) / 86400) < 1e-6")],
            '''
import math

def chinchilla(C):
    N = math.sqrt(C / 120)
    return N, 20 * N

def dias(C, flops_gpu, gpus, aproveitamento=0.4):
    return C / (flops_gpu * gpus * aproveitamento) / 86400

N, D = chinchilla(1e24)
print(f"{N:.2e} parâmetros, {D:.2e} tokens, {dias(1e24, 1e15, 1000):.0f} dias")
''', ["C = 6 · N · 20N = 120N², então N = √(C/120).", "Dias = C / (flops por segundo totais) / 86.400."], rot="Mão no código · nível 2"),
        erros([("Extrapolar muito além dos dados.", "Leis de escala valem num intervalo; previsões distantes são incertas."), ("Achar que perda menor é sempre capacidade nova.", "Algumas habilidades aparecem de forma abrupta em benchmarks."), ("Ignorar o custo de inferência.", "Um modelo menor treinado com mais dados pode sair mais barato no total.")]),
        ponte("Escalar na inferência", "<p>Modelos de raciocínio mostraram uma segunda lei: gastar mais computação na hora de responder (pensar por mais tokens) também melhora o resultado de forma previsível. Escala de treino e escala de inferência agora andam juntas.</p>"),
        quiz([
            ("Em escala log-log, uma lei de potência vira:", ["Uma reta.", "Uma parábola.", "Um círculo."], 0, "Inclinação = −α."),
            ("Computação de treino aproximada:", ["6·N·D.", "N + D.", "N²."], 0, "Por token e parâmetro."),
            ("Chinchilla sugere cerca de:", ["1 token por parâmetro.", "20 tokens por parâmetro.", "1000 parâmetros por token."], 1, "Para orçamento ótimo."),
        ]),
    ],
    ["A perda cai como lei de potência com parâmetros, dados e computação.", "C ≈ 6·N·D.", "Chinchilla: ~20 tokens por parâmetro para orçamento ótimo."],
    "Chunking e estratégias de recuperação no RAG.",
    livro=("D2L:chapter_attention-mechanisms-and-transformers/large-pretraining-transformers", "Seção 11.9, “Large-Scale Pretraining with Transformers”", "Que conclusões sobre escala o livro destaca?"))

AULAS["Chunking e estratégias de recuperação no RAG"] = aula(
    30,
    "Antes de buscar, é preciso cortar os documentos em pedaços (chunks). Pedaços grandes demais diluem o assunto e gastam tokens; pequenos demais perdem o contexto. Como você corta e como busca define boa parte da qualidade de um RAG.",
    ["cortar textos com tamanho e sobreposição;", "respeitar a estrutura (parágrafos, seções);", "conhecer estratégias como busca híbrida, expansão de consulta e pai-filho."],
    ["RAG e bancos vetoriais."],
    [
        chute("Uma resposta depende de duas frases que ficaram em chunks vizinhos, cortadas no meio. Qual técnica ajuda?", ["Chunks sem sobreposição.", "Sobreposição entre chunks (por exemplo 15%).", "Apagar a pontuação."], 1,
              ["É o que causou o problema.", "Isso! A sobreposição repete o final de um chunk no início do próximo, e frases na fronteira aparecem inteiras em pelo menos um.", "Pioraria."],
              "Também ajuda cortar em parágrafos em vez de num número fixo de caracteres."),
        concreto("Fichas de estudo", "<p>Ao resumir um livro em fichas, você não corta no meio da frase: faz uma ficha por ideia. E anota na ficha de qual capítulo ela veio. Bons chunks são fichas: uma ideia, inteira, com a origem.</p>"),
        tabela("Estratégias", ["Estratégia", "Como", "Quando ajuda"], [
            ["Tamanho fixo + sobreposição", "N palavras, repetindo as últimas k", "ponto de partida"],
            ["Estrutural", "por parágrafos, seções, títulos", "documentos bem formatados"],
            ["Pai-filho", "busca em chunks pequenos, entrega o trecho maior", "precisão na busca + contexto na resposta"],
            ["Metadados", "título, data, autor em cada chunk", "filtros e citações"],
            ["Expansão de consulta", "o LLM reescreve a pergunta em várias versões", "perguntas vagas ou curtas"],
        ], rot="Organize na cabeça"),
        cod("Chunking com sobreposição", "Escreva <code>chunks(texto, tamanho, sobreposicao)</code> que divide o texto em listas de palavras de até <code>tamanho</code>, onde cada chunk começa <code>tamanho - sobreposicao</code> palavras depois do anterior. Devolva os chunks como strings, sem chunk final repetido.",
            '''
def chunks(texto, tamanho, sobreposicao):
    return [texto]

t = "um dois tres quatro cinco seis sete oito nove dez"
print(chunks(t, 4, 1))
''',
            [("Com sobreposição", "assert chunks(t, 4, 1) == ['um dois tres quatro', 'quatro cinco seis sete', 'sete oito nove dez'], f'{chunks(t, 4, 1)}'"),
             ("Sem sobreposição", "assert chunks(t, 5, 0) == ['um dois tres quatro cinco', 'seis sete oito nove dez']"),
             ("Texto curto", "assert chunks('a b', 4, 1) == ['a b']")],
            '''
def chunks(texto, tamanho, sobreposicao):
    p = texto.split()
    passo = tamanho - sobreposicao
    out = []
    for i in range(0, len(p), passo):
        out.append(" ".join(p[i:i + tamanho]))
        if i + tamanho >= len(p):
            break
    return out

t = "um dois tres quatro cinco seis sete oito nove dez"
print(chunks(t, 4, 1))
''', ["Ande de <code>tamanho - sobreposicao</code> em <code>tamanho - sobreposicao</code>.", "Pare quando o chunk atual chegar ao fim do texto."]),
        cod("Chunks por parágrafo", "Escreva <code>por_paragrafo(texto, max_palavras)</code>: separe por linhas em branco e junte parágrafos vizinhos enquanto o total couber em <code>max_palavras</code>. Cada chunk deve guardar o número do primeiro parágrafo como metadado.",
            '''
def por_paragrafo(texto, max_palavras):
    return []

doc = """Introdução curta.

Segundo parágrafo com mais algumas palavras.

Terceiro.

Quarto parágrafo que é bem mais longo que os outros todos juntos aqui."""
for c in por_paragrafo(doc, 8):
    print(c)
''',
            [("Agrupa e guarda a origem", "r = por_paragrafo(doc, 8)\nassert [c['inicio'] for c in r] == [0, 2, 3], f'{r}'"),
             ("Junta parágrafos pequenos", "r = por_paragrafo(doc, 8)\nassert r[0]['texto'] == 'Introdução curta.\\n\\nSegundo parágrafo com mais algumas palavras.', repr(r[0])")],
            '''
def por_paragrafo(texto, max_palavras):
    pars = [p.strip() for p in texto.split("\\n\\n") if p.strip()]
    out, atual, inicio = [], [], 0
    for i, p in enumerate(pars):
        n_atual = sum(len(x.split()) for x in atual)
        if atual and n_atual + len(p.split()) > max_palavras:
            out.append({"inicio": inicio, "texto": "\\n\\n".join(atual)})
            atual = []
        if not atual:
            inicio = i
        atual.append(p)
    if atual:
        out.append({"inicio": inicio, "texto": "\\n\\n".join(atual)})
    return out

doc = """Introdução curta.

Segundo parágrafo com mais algumas palavras.

Terceiro.

Quarto parágrafo que é bem mais longo que os outros todos juntos aqui."""
for c in por_paragrafo(doc, 8):
    print(c)
''', ["Separe com <code>texto.split(\"\\n\\n\")</code>.", "Feche o chunk atual quando o próximo parágrafo estourar o limite."], rot="Mão no código · nível 2"),
        erros([("Escolher o tamanho do chunk sem testar.", "Compare 2 ou 3 tamanhos no seu conjunto de avaliação."), ("Perder títulos e tabelas ao extrair de PDF.", "Confira o texto extraído; tabelas quebradas viram lixo."), ("Chunks sem metadados.", "Sem a origem, não dá para citar nem filtrar.")]),
        ponte("A peça seguinte", "<p>Mesmo com bons chunks, a busca vetorial traz alguns irrelevantes no topo. A próxima aula, sobre reranking, mostra como reordenar os candidatos com um modelo mais preciso.</p>"),
        quiz([
            ("Para que serve a sobreposição?", ["Evitar que informações na fronteira se percam.", "Economizar tokens.", "Deixar a busca mais rápida."], 0, "Repetir as bordas."),
            ("O que é a estratégia pai-filho?", ["Buscar em chunks pequenos e entregar o trecho maior.", "Um chunk por documento.", "Dois modelos."], 0, "Precisão + contexto."),
            ("Por que guardar metadados nos chunks?", ["Para citar e filtrar.", "Para aumentar o tamanho.", "Não serve."], 0, "Origem."),
        ]),
    ],
    ["Chunks: uma ideia inteira, com origem.", "Tamanho e sobreposição se escolhem testando.", "Estrutura, metadados e pai-filho melhoram a recuperação."],
    "Reranking.",
    livro=("PROMPT:techniques/rag", "Prompt Engineering Guide, “Retrieval Augmented Generation”", "Que componentes de um RAG o guia descreve?"))

AULAS["Reranking"] = aula(
    25,
    "A busca vetorial é rápida, mas aproximada: traz 50 candidatos, e o melhor pode estar em 12º. O reranking usa um modelo mais lento e preciso, que lê pergunta e trecho juntos, para reordenar esses candidatos e mandar só os 5 melhores ao LLM.",
    ["diferenciar bi-encoder e cross-encoder;", "montar a busca em duas etapas;", "medir a melhora com métricas de ranking (MRR, recall@k)."],
    ["Bancos vetoriais e encoder vs. decoder."],
    [
        chute("Por que não usar o cross-encoder (o mais preciso) direto em todos os documentos?", ["Ele é impreciso.", "Ele precisa processar a pergunta junto com cada documento: com 1 milhão de documentos, seria 1 milhão de chamadas por busca.", "Ele não aceita texto."], 1,
              ["É o mais preciso.", "Isso! O bi-encoder calcula os embeddings dos documentos uma vez só; o cross-encoder não dá para pré-calcular.", "Aceita."],
              "Duas etapas: rápido e amplo, depois lento e preciso."),
        concreto("O processo seletivo", "<p>Numa vaga com mil currículos, primeiro um filtro rápido por palavras-chave seleciona 50. Depois, alguém lê esses 50 com atenção e escolhe 5 para entrevista. Ninguém lê os mil com atenção: não daria tempo.</p>"),
        nota("As peças", [
            ("Bi-encoder", "dois vetores separados", "Pergunta e documento viram embeddings independentes; compara por cosseno."),
            ("Cross-encoder", "leitura conjunta", "Lê “pergunta + documento” e dá uma nota; muito mais preciso."),
            ("Recall@k", "o certo apareceu?", "Fração de perguntas com o documento certo entre os k primeiros."),
            ("MRR", "posição recíproca média", "Média de 1/posição do primeiro documento certo."),
        ]),
        cod("Medindo o ranking", "Escreva <code>mrr(rankings, corretos)</code> e <code>recall_k(rankings, corretos, k)</code>. Se o documento certo não aparece, a contribuição para o MRR é 0.",
            '''
def mrr(rankings, corretos):
    return 0.0

def recall_k(rankings, corretos, k):
    return 0.0

rankings = [["d2", "d1", "d3"], ["d5", "d4", "d6"], ["d7", "d8", "d9"]]
corretos = ["d1", "d5", "d0"]
print(mrr(rankings, corretos), recall_k(rankings, corretos, 1))
''',
            [("MRR", "assert abs(mrr(rankings, corretos) - (0.5 + 1 + 0) / 3) < 1e-9"),
             ("Recall@1 e @2", "assert abs(recall_k(rankings, corretos, 1) - 1 / 3) < 1e-9 and abs(recall_k(rankings, corretos, 2) - 2 / 3) < 1e-9")],
            '''
def mrr(rankings, corretos):
    total = 0.0
    for r, c in zip(rankings, corretos):
        if c in r:
            total += 1 / (r.index(c) + 1)
    return total / len(rankings)

def recall_k(rankings, corretos, k):
    return sum(c in r[:k] for r, c in zip(rankings, corretos)) / len(rankings)

rankings = [["d2", "d1", "d3"], ["d5", "d4", "d6"], ["d7", "d8", "d9"]]
corretos = ["d1", "d5", "d0"]
print(mrr(rankings, corretos), recall_k(rankings, corretos, 1))
''', ["Posição começa em 1: <code>r.index(c) + 1</code>.", "Recall@k: o certo está em <code>r[:k]</code>?"]),
        cod("Busca em duas etapas", "Monte o pipeline: a busca rápida devolve os candidatos; o “cross-encoder” (aqui, uma função de nota fornecida) reordena só esses candidatos; devolva os k melhores.",
            '''
def busca_rapida(pergunta, n):
    # simula a busca vetorial: devolve candidatos em ordem aproximada
    return ["frete", "garantia", "devolução em 30 dias", "trocas pelo site", "cupons"][:n]

def nota_cross(pergunta, doc):
    # simula um cross-encoder: nota alta para o que realmente responde
    relevancia = {"devolução em 30 dias": 0.95, "trocas pelo site": 0.7, "garantia": 0.3}
    return relevancia.get(doc, 0.05)

def buscar(pergunta, n_candidatos=5, k=2):
    return busca_rapida(pergunta, k)

print(buscar("Como devolver um produto?"))
''',
            [("Reordena os candidatos", "assert buscar('Como devolver um produto?') == ['devolução em 30 dias', 'trocas pelo site']"),
             ("Só olha os candidatos", "assert buscar('x', n_candidatos=2, k=2) == ['garantia', 'frete']")],
            '''
def busca_rapida(pergunta, n):
    return ["frete", "garantia", "devolução em 30 dias", "trocas pelo site", "cupons"][:n]

def nota_cross(pergunta, doc):
    relevancia = {"devolução em 30 dias": 0.95, "trocas pelo site": 0.7, "garantia": 0.3}
    return relevancia.get(doc, 0.05)

def buscar(pergunta, n_candidatos=5, k=2):
    candidatos = busca_rapida(pergunta, n_candidatos)
    return sorted(candidatos, key=lambda d: nota_cross(pergunta, d), reverse=True)[:k]

print(buscar("Como devolver um produto?"))
''', ["Pegue <code>n_candidatos</code> da busca rápida.", "Ordene pela nota do cross-encoder e corte em k."], rot="Mão no código · nível 2"),
        erros([("Candidatos de menos na primeira etapa.", "Se o documento certo não estiver entre eles, o reranker não salva."), ("Reranking sem medir.", "Compare MRR e recall@k com e sem."), ("Ignorar a latência.", "O reranker adiciona dezenas a centenas de milissegundos; ajuste o número de candidatos.")]),
        ponte("Ferramentas", "<p>Há rerankers abertos (como os da família BGE, via <code>sentence-transformers</code>) e por API. Num RAG sério, a sequência busca híbrida → reranking → LLM é o padrão.</p>"),
        quiz([
            ("O cross-encoder é mais preciso porque:", ["Lê pergunta e documento juntos.", "É maior sempre.", "Usa imagens."], 0, "Atenção entre os dois."),
            ("Por que duas etapas?", ["O cross-encoder é lento demais para todos os documentos.", "Por estética.", "Para gastar mais."], 0, "Rápido e amplo, depois preciso."),
            ("O que o MRR mede?", ["A posição do primeiro documento certo.", "O tamanho dos documentos.", "O custo."], 0, "1/posição."),
        ]),
    ],
    ["Bi-encoder busca rápido; cross-encoder reordena com precisão.", "Duas etapas: muitos candidatos, poucos finalistas.", "Meça com MRR e recall@k."],
    "Saída estruturada (JSON).",
    livro=("HF:chapter5/6", "LLM Course, seção “Semantic search with FAISS”", "Como o curso calcula a similaridade entre pergunta e trechos?"))
