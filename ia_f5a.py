# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 5 (parte A): teoria dos LLMs, ferramentas e primeiras aplicações."""
from lesson_factory import *

AULAS = {}

AULAS["Tokenização e embeddings"] = aula(
    35,
    "Um LLM não lê letras nem palavras: lê <b>tokens</b>, pedaços de texto que viram números. E cada número vira um vetor, o embedding, onde palavras de sentido parecido ficam perto. Entender esses dois passos explica por que modelos erram contas de letras e por que “rei − homem + mulher ≈ rainha”.",
    ["entender tokenização por subpalavras (BPE);", "contar tokens e estimar custo;", "entender embeddings como vetores de significado."],
    ["Dicionários (Fase 1), vetores e produto escalar (Matemática)."],
    [
        chute("Por que muitos LLMs erram ao contar quantas letras “r” há em “carrossel”?", ["Porque não sabem português.", "Porque não veem letras: veem tokens como “car” e “rossel”.", "Porque a pergunta é difícil demais."], 1,
              ["Sabem bastante português.", "Isso! A palavra chega em pedaços, e as letras de dentro de cada pedaço não ficam visíveis.", "Para uma pessoa é fácil; o obstáculo é a representação."],
              "O que o modelo enxerga é a sequência de tokens, não a de caracteres."),
        concreto("As peças de Lego da linguagem", "<p>Com um vocabulário de peças comuns (“pre”, “visão”, “ção”, “mente”), dá para montar qualquer palavra, inclusive as que nunca apareceram. A tokenização BPE escolhe essas peças juntando os pares de caracteres mais frequentes num grande volume de texto.</p>"),
        crianca("<p>Imagine que cada palavra tem um <b>endereço num mapa</b>. “Gato” e “cachorro” moram no mesmo bairro (animais de estimação); “banana” mora em outro. Esse endereço, com centenas de números, é o embedding.</p>"),
        ver("como o vídeo mostra o texto sendo quebrado em tokens"),
        nota("Do texto ao vetor", [
            ("Token", "pedaço de texto", "Pode ser palavra, parte de palavra ou pontuação. Em média, ~4 caracteres em inglês, um pouco menos em português."),
            ("BPE", "byte-pair encoding", "Começa com caracteres e junta, repetidamente, o par mais frequente."),
            ("ID do token", "número", "Posição no vocabulário (dezenas a centenas de milhares)."),
            ("Embedding", "vetor aprendido", "Uma linha de uma matriz grande; parecidos ficam próximos."),
            ("Similaridade de cosseno", "proximidade", "Mede o quanto dois embeddings apontam para o mesmo lado."),
        ], rot="Agora sim, os conceitos"),
        cod("Um passo de BPE", "Implemente o coração do BPE: conte os pares de símbolos vizinhos em todas as palavras e devolva o mais frequente; depois junte esse par em todas as palavras.",
            '''
from collections import Counter

def par_mais_frequente(palavras):
    return None

def juntar(palavras, par):
    return palavras

palavras = [list("baixa"), list("baixo"), list("caixa")]
par = par_mais_frequente(palavras)
print(par, juntar(palavras, par))
''',
            [("Par mais frequente", "assert par_mais_frequente([list('baixa'), list('baixo'), list('caixa')]) == ('a', 'i')"),
             ("Junta o par", "r = juntar([list('baixa'), list('caixa')], ('a', 'i'))\nassert r == [['b', 'ai', 'x', 'a'], ['c', 'ai', 'x', 'a']], f'r = {r}'"),
             ("Segunda rodada", "p = [list('baixa'), list('baixo'), list('caixa')]\np = juntar(p, par_mais_frequente(p))\nassert par_mais_frequente(p) == ('ai', 'x')")],
            '''
from collections import Counter

def par_mais_frequente(palavras):
    cont = Counter()
    for p in palavras:
        for a, b in zip(p, p[1:]):
            cont[(a, b)] += 1
    return cont.most_common(1)[0][0] if cont else None

def juntar(palavras, par):
    novas = []
    for p in palavras:
        out, i = [], 0
        while i < len(p):
            if i < len(p) - 1 and (p[i], p[i + 1]) == par:
                out.append(p[i] + p[i + 1])
                i += 2
            else:
                out.append(p[i])
                i += 1
        novas.append(out)
    return novas

palavras = [list("baixa"), list("baixo"), list("caixa")]
par = par_mais_frequente(palavras)
print(par, juntar(palavras, par))
''', ["Conte com <code>zip(p, p[1:])</code>.", "Ao juntar, percorra com índice e pule dois quando achar o par."]),
        cod("Analogia com embeddings", "Com os embeddings de brinquedo abaixo, calcule <code>rei − homem + mulher</code> e descubra, pela similaridade de cosseno, a palavra mais próxima (sem contar as três usadas).",
            '''
import math

emb = {
    "rei":    [0.9, 0.8, 0.1],
    "rainha": [0.9, 0.1, 0.8],
    "homem":  [0.1, 0.9, 0.1],
    "mulher": [0.1, 0.2, 0.9],
    "maçã":   [0.0, 0.1, 0.1],
}

def cosseno(a, b):
    return 0.0

alvo = None
resposta = None
print(resposta)
''',
            [("Cosseno", "assert abs(cosseno([1, 0], [1, 1]) - 0.7071) < 1e-3"), ("Responde rainha", "assert resposta == 'rainha', f'resposta = {resposta}'")],
            '''
import math

emb = {
    "rei":    [0.9, 0.8, 0.1],
    "rainha": [0.9, 0.1, 0.8],
    "homem":  [0.1, 0.9, 0.1],
    "mulher": [0.1, 0.2, 0.9],
    "maçã":   [0.0, 0.1, 0.1],
}

def cosseno(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

alvo = [r - h + m for r, h, m in zip(emb["rei"], emb["homem"], emb["mulher"])]
candidatas = {p: v for p, v in emb.items() if p not in ("rei", "homem", "mulher")}
resposta = max(candidatas, key=lambda p: cosseno(alvo, candidatas[p]))
print(resposta)
''', ["Some posição a posição: <code>[r - h + m for r, h, m in zip(...)]</code>.", "Use <code>max</code> com <code>key</code> sobre as candidatas."], rot="Mão no código · nível 2"),
        erros([("Achar que 1 token = 1 palavra.", "Conte com o tokenizador do modelo; textos em português costumam gastar mais tokens que em inglês."), ("Comparar embeddings de modelos diferentes.", "Cada modelo tem seu espaço; não misture."), ("Esquecer que custo e limite de contexto são em tokens.", "Estime tokens antes de enviar textos longos.")]),
        ponte("Onde isso aparece", "<p>Preço de API é por milhão de tokens; a janela de contexto é em tokens; a busca semântica de um RAG compara embeddings. Tokenização e embeddings são a porta de entrada de tudo que vem depois nesta fase.</p>"),
        quiz([
            ("O que o BPE faz repetidamente?", ["Remove palavras raras.", "Junta o par de símbolos mais frequente.", "Traduz o texto."], 1, "Constrói o vocabulário."),
            ("Embeddings de palavras parecidas:", ["Ficam próximos.", "São iguais.", "São perpendiculares sempre."], 0, "Vizinhos no espaço."),
            ("Por que textos em português custam mais tokens?", ["O português é mais longo sempre.", "Os tokenizadores foram treinados com mais inglês e quebram o português em mais pedaços.", "Não custam."], 1, "Vocabulário enviesado para o inglês."),
        ]),
    ],
    ["LLMs leem tokens (pedaços de palavras), não letras.", "BPE junta os pares mais frequentes para montar o vocabulário.", "Embeddings são vetores em que significados próximos ficam perto."],
    "Mecanismo de atenção (aula-piloto).",
    livro=("HF:chapter2/4", "LLM Course, capítulo 2, seção “Tokenizers”", "Que tipos de tokenização o curso compara?"))

AULAS["Arquitetura Transformer"] = aula(
    40,
    "Em 2017, um artigo chamado “Attention Is All You Need” propôs uma arquitetura que mudou a IA. Todo LLM atual é uma pilha de blocos iguais: atenção para trocar informação entre tokens, uma rede neural para processar cada token, normalização e conexões residuais.",
    ["montar o bloco de um Transformer;", "entender as conexões residuais;", "seguir um token do texto até a previsão da próxima palavra."],
    ["Mecanismo de atenção, redes neurais e LayerNorm."],
    [
        chute("O que sai da última camada de um LLM, para cada posição?", ["A próxima palavra escrita.", "Uma nota (logit) para cada token do vocabulário.", "O embedding da palavra atual."], 1,
              ["A palavra só aparece depois de escolher o token.", "Isso! Um softmax sobre essas notas dá a probabilidade de cada próximo token.", "Isso é a entrada."],
              "Gerar texto = repetir: prever distribuição, escolher um token, acrescentar e prever de novo."),
        concreto("A reunião em rodadas", "<p>Cada palavra é uma pessoa numa reunião. Em cada rodada (camada), todas conversam (atenção) e depois cada uma pensa sozinha no que ouviu (rede neural). Depois de dezenas de rodadas, a última pessoa sabe o suficiente para adivinhar a próxima palavra.</p>"),
        ver("as etapas que o vídeo mostra entre o texto de entrada e a previsão"),
        nota("O bloco do Transformer (decodificador)", [
            ("Embedding + posição", "entrada", "Cada token vira um vetor que também carrega a posição."),
            (r"$x = x + \text{Atenção}(\text{LN}(x))$", "atenção com residual", "Os tokens trocam informação; o resultado é somado ao original."),
            (r"$x = x + \text{MLP}(\text{LN}(x))$", "rede por token", "Duas camadas lineares com ativação no meio, aplicadas a cada posição."),
            ("× N camadas", "pilha", "De 12 a mais de 100 blocos."),
            ("Cabeça de linguagem", "saída", "Projeção para o vocabulário + softmax."),
        ], rot="Agora sim, a arquitetura"),
        cod("Contando parâmetros de um Transformer", "Um bloco com dimensão d tem: atenção com 4 matrizes d×d (Q, K, V e saída) e MLP com duas matrizes d×4d e 4d×d (ignore vieses e normalizações). Calcule os parâmetros de um modelo com d = 768, 12 blocos e vocabulário de 50.257 tokens (embedding compartilhado com a saída).",
            '''
def parametros(d, blocos, vocab):
    return 0

print(parametros(768, 12, 50257))
''',
            [("Bloco = 12·d²", "assert parametros(10, 1, 0) == 1200"), ("Modelo do tamanho do GPT-2 pequeno", "assert parametros(768, 12, 50257) == 12 * 12 * 768 ** 2 + 50257 * 768, f'{parametros(768, 12, 50257)}'")],
            '''
def parametros(d, blocos, vocab):
    atencao = 4 * d * d
    mlp = 2 * d * 4 * d
    return blocos * (atencao + mlp) + vocab * d

print(parametros(768, 12, 50257))
''', ["Atenção: 4d². MLP: 8d². Total por bloco: 12d².", "Some o embedding: vocab × d."], exp="<p>Dá cerca de 124 milhões: o GPT-2 pequeno. Um modelo de 70 bilhões é a mesma conta com d e camadas muito maiores.</p>"),
        cod("Conexão residual", "Mostre por que a conexão residual ajuda: aplique 50 vezes uma “camada” que encolhe o sinal (multiplica por 0,5), com e sem residual (x = x + camada(x) normalizado por 1,5), e compare a norma final.",
            '''
import numpy as np

def camada(x):
    return 0.5 * x

x0 = np.ones(4)
sem = x0.copy()
com = None  # comece de x0.copy() e atualize dentro do laço
for _ in range(50):
    sem = camada(sem)
    # com residual: com = (com + camada(com)) / 1.5

print(np.linalg.norm(sem), np.linalg.norm(com))
''',
            [("Sem residual o sinal some", "import numpy as np\nassert np.linalg.norm(sem) < 1e-10"), ("Com residual o sinal sobrevive", "import numpy as np\nassert abs(np.linalg.norm(com) - 2.0) < 1e-9, f'{np.linalg.norm(com)}'")],
            '''
import numpy as np

def camada(x):
    return 0.5 * x

x0 = np.ones(4)
sem = x0.copy()
com = x0.copy()
for _ in range(50):
    sem = camada(sem)
    com = (com + camada(com)) / 1.5

print(np.linalg.norm(sem), np.linalg.norm(com))
''', ["Dentro do laço: <code>com = (com + camada(com)) / 1.5</code>."], rot="Mão no código · nível 2",
            exp="<p>O atalho residual deixa o sinal (e o gradiente) passar direto, mesmo quando a camada encolhe tudo. É isso que permite empilhar dezenas de blocos.</p>"),
        erros([("Achar que o Transformer “lê” da esquerda para a direita como uma RNN.", "Ele processa todos os tokens em paralelo; a máscara causal é que impede olhar o futuro."), ("Ignorar a MLP.", "Ela guarda boa parte dos parâmetros e do “conhecimento” do modelo."), ("Achar que mais camadas sempre ajudam.", "Escala exige equilíbrio entre largura, profundidade e dados.")]),
        ponte("Construa o seu", "<p>O vídeo “Let’s build GPT” do Andrej Karpathy constrói um Transformer do zero em algumas centenas de linhas de PyTorch. Depois desta aula e da aula de atenção, você tem todas as peças para acompanhar.</p>"),
        quiz([
            ("Quais são as duas subcamadas de um bloco?", ["Convolução e pooling.", "Atenção e MLP.", "LSTM e softmax."], 1, "Com LayerNorm e residuais."),
            ("Para que serve a conexão residual?", ["Deixar sinal e gradiente atravessarem muitas camadas.", "Reduzir parâmetros.", "Tokenizar."], 0, "Atalho."),
            ("Como um LLM gera texto?", ["Escreve a frase toda de uma vez.", "Prevê um token, acrescenta e repete.", "Copia do treino."], 1, "Autorregressivo."),
        ]),
    ],
    ["Transformer = pilha de blocos (atenção + MLP) com LayerNorm e residuais.", "A saída é uma distribuição sobre o vocabulário.", "Gera texto token a token."],
    "Pré-treino, fine-tuning e RLHF.",
    livro=("D2L:chapter_attention-mechanisms-and-transformers/transformer", "Seção 11.7, “The Transformer Architecture”", "Como o livro organiza o bloco codificador e o decodificador?"))

AULAS["Pré-treino, fine-tuning e RLHF (visão geral)"] = aula(
    30,
    "Um LLM nasce em três etapas. No pré-treino, lê trilhões de tokens e aprende a continuar textos. No ajuste fino com instruções, aprende a responder pedidos. No alinhamento com preferências (RLHF, DPO), aprende quais respostas as pessoas preferem. Cada etapa muda o comportamento de um jeito diferente.",
    ["diferenciar pré-treino, ajuste supervisionado e alinhamento;", "entender o que são dados de preferência;", "saber por que um modelo base não segue instruções."],
    ["Arquitetura Transformer e função de perda."],
    [
        chute("Você pergunta a um modelo <b>base</b> (só pré-treinado): “Qual a capital da França?”. O que é provável?", ["Responde “Paris”.", "Continua o texto, por exemplo com outras perguntas de uma prova.", "Recusa responder."], 1,
              ["Pode acontecer, mas não é garantido.", "Isso! Ele aprendeu a continuar textos; listas de perguntas são continuações plausíveis.", "Recusas vêm do alinhamento."],
              "Seguir instruções é aprendido depois, no ajuste fino."),
        concreto("A formação de um médico", "<p>Primeiro, anos lendo tudo (pré-treino): sabe muito, mas não atende ninguém. Depois, a residência com casos e respostas modelo (ajuste supervisionado). Por fim, o feedback de pacientes e supervisores sobre qual atendimento foi melhor (alinhamento).</p>"),
        tabela("As três etapas", ["Etapa", "Dados", "Objetivo"], [
            ["Pré-treino", "trilhões de tokens da web, livros, código", "prever o próximo token"],
            ["Ajuste supervisionado (SFT)", "milhares a milhões de pares instrução → resposta", "seguir instruções"],
            ["Alinhamento (RLHF, DPO)", "pares de respostas com a preferida marcada", "preferir respostas úteis, honestas e seguras"],
        ]),
        nota("Os termos", [
            ("Modelo base", "só pré-treino", "Continua textos."),
            ("Modelo instruct/chat", "ajustado", "Responde pedidos."),
            ("Modelo de recompensa", "RLHF", "Aprende a dar nota às respostas a partir das preferências humanas."),
            ("DPO", "otimização direta de preferências", "Usa os pares de preferência sem treinar um modelo de recompensa separado."),
        ]),
        cod("Dados de preferência", "Transforme as avaliações humanas em pares (prompt, preferida, rejeitada): para cada prompt, a resposta de maior nota é a preferida e a de menor, a rejeitada. Ignore prompts com notas empatadas.",
            '''
avaliacoes = [
    ("Explique RAG", "RAG busca documentos e usa no prompt.", 5),
    ("Explique RAG", "É uma sigla.", 1),
    ("Resuma o texto", "Resumo A", 3),
    ("Resuma o texto", "Resumo B", 3),
]

def pares(avaliacoes):
    return []

print(pares(avaliacoes))
''',
            [("Um par válido", "assert pares(avaliacoes) == [('Explique RAG', 'RAG busca documentos e usa no prompt.', 'É uma sigla.')], f'{pares(avaliacoes)}'")],
            '''
avaliacoes = [
    ("Explique RAG", "RAG busca documentos e usa no prompt.", 5),
    ("Explique RAG", "É uma sigla.", 1),
    ("Resuma o texto", "Resumo A", 3),
    ("Resuma o texto", "Resumo B", 3),
]

def pares(avaliacoes):
    por_prompt = {}
    for p, r, n in avaliacoes:
        por_prompt.setdefault(p, []).append((n, r))
    saida_pares = []
    for p, lista in por_prompt.items():
        lista.sort()
        if lista[0][0] != lista[-1][0]:
            saida_pares.append((p, lista[-1][1], lista[0][1]))
    return saida_pares

print(pares(avaliacoes))
''', ["Agrupe por prompt num dicionário de listas (nota, resposta).", "Ordene e pegue a maior e a menor, se forem diferentes."]),
        erros([("Usar um modelo base esperando um assistente.", "Escolha a versão instruct/chat."), ("Achar que ajuste fino ensina muitos fatos novos.", "Ele ajusta comportamento e formato; conhecimento novo é mais barato via RAG."), ("Dados de preferência de baixa qualidade.", "O modelo aprende exatamente o que os rotuladores preferiram, inclusive vieses.")]),
        ponte("Na prática", "<p>Você raramente vai pré-treinar um modelo: custa milhões. Mas ajustar um modelo aberto com instruções do seu domínio (SFT com LoRA) ou com preferências (DPO, com a biblioteca TRL) cabe numa GPU do Colab. As próximas aulas mostram as ferramentas.</p>"),
        quiz([
            ("O pré-treino ensina o modelo a:", ["Seguir instruções.", "Prever o próximo token.", "Recusar pedidos perigosos."], 1, "Objetivo de linguagem."),
            ("O que são dados de preferência?", ["Respostas com a melhor marcada em relação a outra.", "Textos da web.", "Pesos do modelo."], 0, "Comparações."),
            ("Para ensinar fatos da sua empresa, o mais barato costuma ser:", ["Pré-treinar.", "RAG.", "RLHF."], 1, "Busca + prompt."),
        ]),
    ],
    ["Pré-treino: prever tokens. SFT: seguir instruções. Alinhamento: preferências.", "Modelos base continuam textos; modelos instruct respondem.", "Ajuste fino muda comportamento; RAG traz conhecimento."],
    "Hugging Face: modelos, datasets e transformers.",
    livro=("HF:chapter1/1", "LLM Course, capítulo 1, “Transformer models”", "Como o curso explica pré-treino e ajuste fino?"))

AULAS["Hugging Face: modelos, datasets e transformers"] = aula(
    25,
    "Mais de um milhão de modelos, centenas de milhares de datasets, todos acessíveis com duas linhas de código. O Hugging Face é o GitHub da IA, e a biblioteca <code>transformers</code> é a forma padrão de baixar, rodar e ajustar modelos abertos.",
    ["usar <code>pipeline</code> para tarefas prontas;", "carregar tokenizador e modelo separadamente;", "carregar datasets e ler um model card."],
    ["Tokenização e Transformer."],
    [
        chute("O que você deve ler antes de usar um modelo do Hugging Face num produto?", ["Só o número de downloads.", "O model card: licença, dados de treino, limitações e uso pretendido.", "Nada."], 1,
              ["Popularidade não garante licença nem adequação.", "Isso! A licença pode proibir uso comercial, e as limitações dizem onde ele falha.", "Usar sem ler pode virar problema legal."],
              "Licença primeiro, desempenho depois."),
        concreto("A biblioteca pública", "<p>Em vez de escrever cada livro do zero, você pega emprestado. O Hugging Face é uma biblioteca de modelos e dados; o model card é a ficha catalográfica que diz do que o livro trata, quem escreveu e o que você pode fazer com ele.</p>"),
        nota("As peças", [
            ("<code>pipeline(\"sentiment-analysis\")</code>", "tarefa pronta", "Baixa um modelo padrão e roda."),
            ("<code>AutoTokenizer.from_pretrained(nome)</code>", "tokenizador", "Sempre o do mesmo modelo."),
            ("<code>AutoModelForCausalLM.from_pretrained(nome)</code>", "modelo", "Pesos baixados e guardados em cache."),
            ("<code>load_dataset(\"nome\")</code>", "datasets", "Com <code>streaming=True</code> para os grandes."),
            ("Model card", "documentação", "Licença, dados, avaliações e limites."),
        ]),
        lab("Seu primeiro modelo do Hub", '''
from transformers import pipeline

classificador = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
print(classificador(["Adorei o atendimento!", "Produto chegou quebrado."]))

gerador = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct")
mensagens = [{"role": "user", "content": "Explique o que é um token em uma frase."}]
print(gerador(mensagens, max_new_tokens=60)[0]["generated_text"][-1]["content"])
''', corpo="<p>Rode no Colab (<code>pip install transformers</code>):</p>", exps=["Leia o model card do Qwen2.5-0.5B: qual a licença?", "Troque por outro modelo pequeno e compare as respostas."]),
        cod("Escolhendo um modelo", "Filtre a lista de modelos: licença que permite uso comercial (apache-2.0 ou mit), tamanho até 3 bilhões de parâmetros, e ordene pelo resultado no benchmark, do maior para o menor. Devolva os nomes.",
            '''
modelos = [
    {"nome": "a", "licenca": "apache-2.0", "bilhoes": 1.5, "nota": 61},
    {"nome": "b", "licenca": "cc-by-nc-4.0", "bilhoes": 1.0, "nota": 70},
    {"nome": "c", "licenca": "mit", "bilhoes": 3.0, "nota": 66},
    {"nome": "d", "licenca": "apache-2.0", "bilhoes": 7.0, "nota": 75},
]

def escolher(modelos):
    return []

print(escolher(modelos))
''',
            [("Filtra e ordena", "assert escolher(modelos) == ['c', 'a'], f'{escolher(modelos)}'")],
            '''
modelos = [
    {"nome": "a", "licenca": "apache-2.0", "bilhoes": 1.5, "nota": 61},
    {"nome": "b", "licenca": "cc-by-nc-4.0", "bilhoes": 1.0, "nota": 70},
    {"nome": "c", "licenca": "mit", "bilhoes": 3.0, "nota": 66},
    {"nome": "d", "licenca": "apache-2.0", "bilhoes": 7.0, "nota": 75},
]

def escolher(modelos):
    ok = [m for m in modelos if m["licenca"] in ("apache-2.0", "mit") and m["bilhoes"] <= 3]
    return [m["nome"] for m in sorted(ok, key=lambda m: m["nota"], reverse=True)]

print(escolher(modelos))
''', ["Filtre com uma comprehension e ordene com <code>sorted(..., key=..., reverse=True)</code>."]),
        erros([("Tokenizador de um modelo com pesos de outro.", "Os IDs não batem e a saída vira lixo."), ("Ignorar a licença.", "“nc” significa não comercial."), ("Baixar modelos grandes sem checar a memória.", "Um modelo de 7B em float16 ocupa ~14 GB.")]),
        ponte("O ecossistema aberto", "<p>Modelos abertos (Llama, Qwen, Mistral, Gemma) rodam no seu servidor, sem enviar dados para fora, e podem ser ajustados. O Hugging Face é onde eles são publicados, comparados e baixados.</p>"),
        quiz([
            ("O que é um model card?", ["Um cartão de crédito.", "A documentação do modelo: licença, dados e limites.", "O arquivo de pesos."], 1, "Leia antes de usar."),
            ("Por que usar o tokenizador do mesmo modelo?", ["Os IDs de tokens são específicos de cada modelo.", "É mais rápido.", "Não precisa."], 0, "Vocabulários diferentes."),
            ("O que <code>pipeline</code> faz?", ["Treina do zero.", "Junta tokenizador, modelo e pós-processamento para uma tarefa.", "Publica modelos."], 1, "Atalho."),
        ]),
    ],
    ["O Hub reúne modelos, datasets e documentação.", "<code>pipeline</code> para começar; Auto* para controle.", "Leia licença e limitações no model card."],
    "Fine-tuning com LoRA.",
    livro=("HF:chapter3/1", "LLM Course, capítulo 3, “Fine-tuning a pretrained model”", "Que passos o curso segue para ajustar um modelo com o Trainer?"))

AULAS["Fine-tuning com LoRA"] = aula(
    30,
    "Ajustar todos os 7 bilhões de parâmetros de um modelo exige várias GPUs grandes. O LoRA congela o modelo e treina só duas matrizes pequenas por camada, que somadas aos pesos originais mudam o comportamento. Resultado parecido, com menos de 1% dos parâmetros treináveis.",
    ["entender a decomposição de posto baixo;", "calcular a economia de parâmetros;", "saber quando ajustar e quando usar prompt ou RAG."],
    ["Transfer learning, matrizes e Hugging Face."],
    [
        chute("Uma matriz de pesos tem 4096 × 4096. Com LoRA de posto 8, quantos parâmetros são treinados nela?", ["16,7 milhões.", "65.536.", "8."], 1,
              ["Isso é a matriz inteira.", "Isso! Duas matrizes: 4096 × 8 e 8 × 4096 = 65.536, 0,4% do total.", "O posto é a dimensão do meio, não a contagem."],
              "LoRA: W' = W + B·A, com A e B finas."),
        concreto("O post-it no livro", "<p>Em vez de reescrever o livro (os pesos), você cola post-its com correções. O livro fica intacto; os post-its são pequenos, baratos e dá para trocar por outro conjunto conforme a tarefa. Os adaptadores LoRA são esses post-its.</p>"),
        nota("A ideia", [
            (r"$W' = W + \frac{\alpha}{r} B A$", "atualização", "W congelada; A (r × d) e B (d × r) treinadas."),
            ("Posto r", "tamanho do adaptador", "Tipicamente 8 a 64."),
            ("QLoRA", "LoRA sobre modelo quantizado", "Modelo em 4 bits + adaptador: cabe numa GPU do Colab."),
            ("Adaptador", "arquivo pequeno", "Alguns MB; troque por tarefa."),
        ], rot="Agora sim, a fórmula"),
        cod("A economia do LoRA", "Calcule os parâmetros treináveis com LoRA (posto r) aplicado a todas as matrizes d×d de um modelo e a fração em relação a treinar tudo.",
            '''
def lora_parametros(d, r, n_matrizes):
    return 0

def fracao(d, r, n_matrizes):
    return 0.0

# 32 camadas x 4 matrizes de atenção, d = 4096, r = 16
print(lora_parametros(4096, 16, 128), round(fracao(4096, 16, 128), 5))
''',
            [("Parâmetros LoRA", "assert lora_parametros(4096, 16, 128) == 2 * 4096 * 16 * 128"), ("Fração", "assert abs(fracao(4096, 16, 128) - 2 * 16 / 4096) < 1e-12")],
            '''
def lora_parametros(d, r, n_matrizes):
    return 2 * d * r * n_matrizes

def fracao(d, r, n_matrizes):
    return lora_parametros(d, r, n_matrizes) / (d * d * n_matrizes)

print(lora_parametros(4096, 16, 128), round(fracao(4096, 16, 128), 5))
''', ["Cada matriz ganha A e B: 2 × d × r.", "Fração = LoRA / (d² × número de matrizes)."]),
        cod("Aplicando um adaptador", "Com NumPy, aplique o LoRA: W' = W + (α/r)·B·A. Confira que o formato não muda e que, com B = 0 (inicialização padrão), o modelo começa igual ao original.",
            '''
import numpy as np

def aplicar_lora(W, A, B, alpha, r):
    return W

rng = np.random.default_rng(0)
W = rng.normal(size=(6, 6))
A = rng.normal(size=(2, 6))
B = np.zeros((6, 2))
print(np.allclose(aplicar_lora(W, A, B, 16, 2), W))
''',
            [("B = 0 mantém o modelo", "import numpy as np\nassert np.allclose(aplicar_lora(W, A, np.zeros((6, 2)), 16, 2), W)"),
             ("Fórmula correta", "import numpy as np\nB2 = np.ones((6, 2))\nassert np.allclose(aplicar_lora(W, A, B2, 16, 2), W + 8 * B2 @ A)")],
            '''
import numpy as np

def aplicar_lora(W, A, B, alpha, r):
    return W + (alpha / r) * B @ A

rng = np.random.default_rng(0)
W = rng.normal(size=(6, 6))
A = rng.normal(size=(2, 6))
B = np.zeros((6, 2))
print(np.allclose(aplicar_lora(W, A, B, 16, 2), W))
''', ["<code>W + (alpha / r) * B @ A</code>"], rot="Mão no código · nível 2"),
        tabela("Prompt, RAG ou ajuste fino?", ["Quero...", "Use"], [
            ["respostas sobre documentos que mudam", "RAG"],
            ["um formato ou tom específico, sempre", "ajuste fino (LoRA)"],
            ["testar uma ideia rápido", "engenharia de prompt"],
            ["uma tarefa estreita com muitos exemplos e custo baixo", "ajuste fino de um modelo pequeno"],
        ], rot="Decidindo"),
        erros([("Ajustar para ensinar fatos.", "O modelo aprende mal e esquece; use RAG."), ("Poucos exemplos ruins.", "Qualidade dos dados vale mais que quantidade: 500 exemplos bons superam 5.000 ruins."), ("Não guardar um conjunto de avaliação.", "Sem ele, você não sabe se o ajuste ajudou ou piorou.")]),
        ponte("O ecossistema PEFT", "<p>A biblioteca <code>peft</code> do Hugging Face aplica LoRA em qualquer modelo; o TRL faz o treino supervisionado e por preferências. Com QLoRA, um modelo de 7 bilhões é ajustado numa única GPU de 16 GB.</p>"),
        quiz([
            ("No LoRA, o que fica congelado?", ["Os adaptadores.", "Os pesos originais do modelo.", "Nada."], 1, "Treina só A e B."),
            ("Por que B começa em zero?", ["Para o modelo começar idêntico ao original.", "Para treinar mais rápido.", "Por acaso."], 0, "BA = 0 no início."),
            ("O que é o QLoRA?", ["LoRA sobre um modelo quantizado em 4 bits.", "Um otimizador.", "Um tokenizador."], 0, "Economia de memória."),
        ]),
    ],
    ["LoRA treina matrizes pequenas (B·A) somadas aos pesos congelados.", "Menos de 1% dos parâmetros; adaptadores de poucos MB.", "Ajuste fino muda comportamento; RAG traz conhecimento."],
    "Engenharia de prompts.",
    livro=("HF:chapter11/1", "LLM Course, capítulo sobre ajuste fino de LLMs", "Que formato de dados de conversa o curso usa no SFT?"))

AULAS["Engenharia de prompts"] = aula(
    30,
    "O mesmo modelo pode dar uma resposta vaga ou uma resposta excelente dependendo de como você pede. Engenharia de prompts é o conjunto de técnicas para pedir bem: contexto, instruções claras, exemplos, formato e espaço para o modelo raciocinar.",
    ["estruturar prompts com papel, contexto, tarefa e formato;", "usar exemplos (few-shot);", "pedir raciocínio passo a passo e verificar."],
    ["Pré-treino e ajuste fino."],
    [
        chute("Qual prompt tende a dar o melhor resultado?", ["“Resuma.”", "“Resuma o relatório abaixo em 3 tópicos para um gerente sem formação técnica, destacando riscos. Relatório: ...”", "“RESUMA AGORA!!!”"], 1,
              ["Vago: quem lê? quanto? o quê?", "Isso! Público, tamanho, foco e o material: o modelo não precisa adivinhar.", "Ênfase não substitui clareza."],
              "Escreva como se fosse para um colega competente que não conhece o contexto."),
        concreto("O estagiário brilhante", "<p>Um estagiário muito inteligente, mas que chegou hoje: se você diz “faz aquele relatório”, ele erra. Se explica o objetivo, mostra um exemplo e diz o formato, ele acerta. O LLM é esse estagiário.</p>"),
        nota("As técnicas", [
            ("Papel e contexto", "quem e por quê", "“Você é um revisor jurídico; o texto é para clientes leigos.”"),
            ("Instruções claras", "o quê", "Verbos, limites e critérios de sucesso."),
            ("Few-shot", "exemplos", "Dois a cinco pares de entrada e saída no formato desejado."),
            ("Raciocínio passo a passo", "pensar antes", "Pedir o raciocínio antes da resposta melhora problemas de várias etapas."),
            ("Formato de saída", "estrutura", "JSON, tabela, tópicos; com delimitadores claros para os dados."),
        ]),
        cod("Montador de prompts", "Escreva <code>montar_prompt(tarefa, exemplos, entrada)</code> que gera um prompt few-shot: a tarefa, depois cada exemplo como <b>Entrada:</b> / <b>Saída:</b>, e por fim a nova entrada com <b>Saída:</b> vazia.",
            '''
def montar_prompt(tarefa, exemplos, entrada):
    return ""

p = montar_prompt("Classifique o sentimento como positivo ou negativo.",
                  [("Amei o produto", "positivo"), ("Chegou quebrado", "negativo")],
                  "Entrega rápida e bem embalada")
print(p)
''',
            [("Começa pela tarefa", "assert p.splitlines()[0] == 'Classifique o sentimento como positivo ou negativo.'"),
             ("Exemplos no formato", "assert 'Entrada: Amei o produto\\nSaída: positivo' in p"),
             ("Termina pedindo a saída", "assert p.rstrip().endswith('Entrada: Entrega rápida e bem embalada\\nSaída:'), repr(p[-60:])")],
            '''
def montar_prompt(tarefa, exemplos, entrada):
    partes = [tarefa, ""]
    for e, s in exemplos:
        partes += [f"Entrada: {e}", f"Saída: {s}", ""]
    partes += [f"Entrada: {entrada}", "Saída:"]
    return "\\n".join(partes)

p = montar_prompt("Classifique o sentimento como positivo ou negativo.",
                  [("Amei o produto", "positivo"), ("Chegou quebrado", "negativo")],
                  "Entrega rápida e bem embalada")
print(p)
''', ["Monte uma lista de linhas e junte com <code>\"\\n\".join</code>."]),
        erros([("Instruções contraditórias ou escondidas no meio do texto.", "Coloque o pedido principal no começo ou no fim, separado dos dados."), ("Exemplos todos parecidos.", "O modelo copia o padrão; varie os exemplos."), ("Não testar com vários casos.", "Um prompt que funciona num exemplo pode falhar em outros: monte um pequeno conjunto de teste.")]),
        ponte("Prompts em produção", "<p>Em sistemas reais, prompts são código: versionados, testados com conjuntos de avaliação e revisados. Uma mudança de três palavras pode melhorar ou quebrar milhares de respostas. A aula de avaliação de LLMs mostra como medir isso.</p>"),
        quiz([
            ("O que é few-shot?", ["Usar poucos tokens.", "Dar exemplos de entrada e saída no prompt.", "Treinar com poucos dados."], 1, "Exemplos no contexto."),
            ("Pedir raciocínio passo a passo ajuda principalmente em:", ["Problemas de várias etapas.", "Traduções curtas.", "Contar tokens."], 0, "Lógica e matemática."),
            ("Como separar instruções de dados?", ["Misturando tudo.", "Com delimitadores claros (tags, aspas, seções).", "Em maiúsculas."], 1, "Evita confusão e injeção."),
        ]),
    ],
    ["Contexto, instrução clara, exemplos e formato.", "Peça raciocínio para problemas de várias etapas.", "Teste prompts como código."],
    "Usar APIs de LLMs.",
    livro=("PROMPT:introduction", "Prompt Engineering Guide, “Introdução” e “Técnicas de prompting”", "Que elementos de um prompt o guia lista?"))

AULAS["Usar APIs de LLMs (chamadas, streaming, tool use)"] = aula(
    35,
    "Chamar um LLM é enviar um JSON com as mensagens e receber outro com a resposta. Em volta disso estão as decisões que importam em produção: o papel de cada mensagem, o streaming para a resposta aparecer aos poucos, as ferramentas que o modelo pode chamar e o tratamento de falhas.",
    ["montar mensagens com papéis (system, user, assistant);", "entender streaming e uso de ferramentas;", "tratar erros com novas tentativas e espera crescente."],
    ["Consumir APIs (Fase 1), JSON e engenharia de prompts."],
    [
        chute("O modelo respondeu pedindo para chamar a ferramenta <code>consultar_clima(cidade=\"Recife\")</code>. Quem executa a ferramenta?", ["O próprio modelo, sozinho.", "O seu código: ele executa e devolve o resultado ao modelo numa nova mensagem.", "A empresa do modelo."], 1,
              ["O modelo só propõe a chamada.", "Isso! O modelo decide e preenche os argumentos; seu programa executa e devolve o resultado.", "A execução fica com você."],
              "Tool use = o modelo escolhe, seu código faz, o modelo usa o resultado."),
        concreto("O telefone com secretária", "<p>Você liga (requisição), explica quem você é e o que quer (mensagens), e a resposta vem aos poucos (streaming). Se a secretária precisa de um documento, pede para você buscar (ferramenta) e continua quando você entrega.</p>"),
        nota("A conversa em JSON", [
            ("<code>{\"role\": \"system\", ...}</code>", "instruções gerais", "Comportamento e regras."),
            ("<code>{\"role\": \"user\", ...}</code> / <code>assistant</code>", "a conversa", "O histórico inteiro é reenviado a cada chamada: a API não lembra sozinha."),
            ("Streaming", "resposta em pedaços", "Os tokens chegam conforme são gerados."),
            ("Ferramentas", "funções com esquema", "Nome, descrição e parâmetros em JSON Schema."),
            ("429 / 5xx", "limite e instabilidade", "Tente de novo com espera crescente."),
        ]),
        cod("O laço de ferramentas", "Simule um agente: a função <code>modelo</code> (falsa) pede uma ferramenta ou dá a resposta final. Complete o laço que executa as ferramentas pedidas, acrescenta o resultado ao histórico e repete até a resposta final.",
            '''
import json

def consultar_clima(cidade):
    return {"Recife": "30 graus, sol"}.get(cidade, "desconhecido")

FERRAMENTAS = {"consultar_clima": consultar_clima}

def modelo(historico):
    """Modelo falso: se ainda não viu o resultado da ferramenta, pede; senão responde."""
    if not any(m["role"] == "tool" for m in historico):
        return {"tipo": "ferramenta", "nome": "consultar_clima", "args": {"cidade": "Recife"}}
    clima = [m for m in historico if m["role"] == "tool"][-1]["content"]
    return {"tipo": "texto", "texto": f"Em Recife faz {clima}."}

def conversar(pergunta):
    historico = [{"role": "user", "content": pergunta}]
    for _ in range(5):
        r = modelo(historico)
        # se for texto, devolva; se for ferramenta, execute e acrescente
        # {"role": "tool", "content": resultado} ao histórico
        return r
    return "limite de passos"

print(conversar("Como está o tempo em Recife?"))
''',
            [("Resposta final", "assert conversar('Como está o tempo em Recife?') == 'Em Recife faz 30 graus, sol.'")],
            '''
import json

def consultar_clima(cidade):
    return {"Recife": "30 graus, sol"}.get(cidade, "desconhecido")

FERRAMENTAS = {"consultar_clima": consultar_clima}

def modelo(historico):
    if not any(m["role"] == "tool" for m in historico):
        return {"tipo": "ferramenta", "nome": "consultar_clima", "args": {"cidade": "Recife"}}
    clima = [m for m in historico if m["role"] == "tool"][-1]["content"]
    return {"tipo": "texto", "texto": f"Em Recife faz {clima}."}

def conversar(pergunta):
    historico = [{"role": "user", "content": pergunta}]
    for _ in range(5):
        r = modelo(historico)
        if r["tipo"] == "texto":
            return r["texto"]
        resultado = FERRAMENTAS[r["nome"]](**r["args"])
        historico.append({"role": "tool", "content": resultado})
    return "limite de passos"

print(conversar("Como está o tempo em Recife?"))
''', ["Se <code>r[\"tipo\"] == \"texto\"</code>, devolva o texto.", "Senão: <code>FERRAMENTAS[r[\"nome\"]](**r[\"args\"])</code> e acrescente ao histórico."]),
        cod("Espera crescente", "Escreva <code>com_retentativas(f, tentativas)</code>: chama <code>f()</code>; se der <code>ConnectionError</code>, tenta de novo, registrando em <code>esperas</code> o tempo 1, 2, 4, 8... (não precisa dormir de verdade). Se todas falharem, propague o erro.",
            '''
esperas = []

def com_retentativas(f, tentativas=4):
    return f()

falhas = {"n": 2}
def instavel():
    if falhas["n"] > 0:
        falhas["n"] -= 1
        raise ConnectionError("fora do ar")
    return "ok"

print(com_retentativas(instavel), esperas)
''',
            [("Recupera depois de 2 falhas", "esperas.clear(); falhas['n'] = 2\nassert com_retentativas(instavel) == 'ok' and esperas == [1, 2], f'esperas = {esperas}'"),
             ("Desiste depois do limite", "esperas.clear(); falhas['n'] = 10\ntry:\n    com_retentativas(instavel, 3)\n    ok = False\nexcept ConnectionError:\n    ok = True\nassert ok")],
            '''
esperas = []

def com_retentativas(f, tentativas=4):
    for i in range(tentativas):
        try:
            return f()
        except ConnectionError:
            if i == tentativas - 1:
                raise
            esperas.append(2 ** i)

falhas = {"n": 2}
def instavel():
    if falhas["n"] > 0:
        falhas["n"] -= 1
        raise ConnectionError("fora do ar")
    return "ok"

print(com_retentativas(instavel), esperas)
''', ["Laço com <code>try</code>; no <code>except</code>, registre <code>2 ** i</code>.", "Na última tentativa, <code>raise</code> de novo."], rot="Mão no código · nível 2"),
        erros([("Esperar que a API lembre a conversa.", "Envie o histórico a cada chamada."), ("Executar ferramentas pedidas pelo modelo sem validar.", "Confira argumentos e permissões: o pedido pode ter sido manipulado (prompt injection)."), ("Chave da API no código ou no front-end.", "Sempre no servidor, em variável de ambiente.")]),
        ponte("Agentes nascem aqui", "<p>O laço que você escreveu (modelo pede ferramenta → código executa → modelo continua) é o esqueleto de todo agente de IA. Frameworks como LangGraph e o protocolo MCP só organizam e padronizam esse laço.</p>"),
        quiz([
            ("Para que serve a mensagem de sistema?", ["Definir regras e comportamento gerais.", "Guardar a resposta.", "Medir custo."], 0, "Instruções de fundo."),
            ("Quem executa uma ferramenta pedida pelo modelo?", ["O modelo.", "O seu código.", "O usuário sempre."], 1, "O modelo só propõe."),
            ("O que fazer com um erro 429?", ["Desistir.", "Tentar de novo com espera crescente.", "Mudar de modelo na hora."], 1, "Limite de taxa."),
        ]),
    ],
    ["A API recebe o histórico de mensagens com papéis.", "Ferramentas: o modelo propõe, o código executa.", "Trate falhas com novas tentativas e espera crescente."],
    "RAG: busca em documentos + LLM.",
    livro=("PROMPT:applications", "Prompt Engineering Guide, seção sobre function calling", "Como o guia descreve o fluxo de chamada de funções?"))

AULAS["RAG: busca em documentos + LLM"] = aula(
    40,
    "O LLM não conhece os documentos da sua empresa, e o que ele sabe pode estar desatualizado. O RAG resolve isso em três passos: buscar os trechos relevantes, colocá-los no prompt e pedir ao modelo para responder com base neles. É a aplicação de LLM mais comum no mercado.",
    ["montar o fluxo indexar → buscar → gerar;", "construir o prompt com os trechos e citações;", "avaliar a busca e a resposta separadamente."],
    ["Embeddings, prompts e APIs de LLM."],
    [
        chute("Um RAG deu uma resposta errada. Qual a primeira coisa a verificar?", ["O tamanho do modelo.", "Se os trechos certos foram encontrados na busca.", "A cor da interface."], 1,
              ["Modelo maior não ajuda se o trecho certo não chegou ao prompt.", "Isso! A maioria dos erros de RAG é de recuperação: o modelo nem viu a informação.", "Interface não afeta."],
              "Avalie a busca antes da geração."),
        concreto("A prova com consulta", "<p>Na prova com consulta, você não decorou tudo: procura as páginas certas do livro e responde com base nelas. Se procurar no capítulo errado, erra mesmo sabendo escrever bem. O RAG é a prova com consulta do LLM.</p>"),
        passos("O fluxo do RAG", [
            ("<b>Indexar</b>: dividir documentos em trechos e calcular os embeddings.", "Feito uma vez (e quando os documentos mudam)."),
            ("<b>Buscar</b>: embedding da pergunta → k trechos mais parecidos.", "É um KNN no espaço de embeddings."),
            ("<b>Montar o prompt</b>: instruções + trechos numerados + pergunta.", "“Responda só com base nos trechos; cite o número.”"),
            ("<b>Gerar</b>: o LLM responde.", "Se a resposta não estiver nos trechos, ele deve dizer que não sabe."),
        ]),
        cod("Um RAG de brinquedo", "Complete a busca: ranqueie os trechos pela quantidade de palavras em comum com a pergunta (uma “similaridade” simples no lugar de embeddings) e monte o prompt com os 2 melhores, numerados.",
            '''
trechos = [
    "O prazo de devolução é de 30 dias após a entrega.",
    "O frete é grátis para compras acima de 200 reais.",
    "A garantia dos eletrônicos é de 12 meses.",
    "Devoluções são feitas pelo site, na área Meus Pedidos.",
]

def palavras(t):
    return set(t.lower().replace(".", "").replace(",", "").split())

def buscar(pergunta, k=2):
    return []

def montar_prompt(pergunta):
    achados = buscar(pergunta)
    linhas = ["Responda só com base nos trechos e cite o número. Se não souber, diga que não sabe."]
    linhas += [f"[{i + 1}] {t}" for i, t in enumerate(achados)]
    linhas.append(f"Pergunta: {pergunta}")
    return "\\n".join(linhas)

print(montar_prompt("Qual o prazo de devolução?"))
''',
            [("Busca os trechos certos", "r = buscar('Qual o prazo de devolução?')\nassert trechos[0] in r and len(r) == 2, f'{r}'"),
             ("O primeiro é o mais relevante", "assert buscar('Qual o prazo de devolução?')[0] == trechos[0]"),
             ("Prompt numerado", "assert '[1] O prazo de devolução é de 30 dias após a entrega.' in montar_prompt('Qual o prazo de devolução?')")],
            '''
trechos = [
    "O prazo de devolução é de 30 dias após a entrega.",
    "O frete é grátis para compras acima de 200 reais.",
    "A garantia dos eletrônicos é de 12 meses.",
    "Devoluções são feitas pelo site, na área Meus Pedidos.",
]

def palavras(t):
    return set(t.lower().replace(".", "").replace(",", "").split())

def buscar(pergunta, k=2):
    q = palavras(pergunta)
    return sorted(trechos, key=lambda t: len(q & palavras(t)), reverse=True)[:k]

def montar_prompt(pergunta):
    achados = buscar(pergunta)
    linhas = ["Responda só com base nos trechos e cite o número. Se não souber, diga que não sabe."]
    linhas += [f"[{i + 1}] {t}" for i, t in enumerate(achados)]
    linhas.append(f"Pergunta: {pergunta}")
    return "\\n".join(linhas)

print(montar_prompt("Qual o prazo de devolução?"))
''', ["Interseção de conjuntos: <code>palavras(pergunta) &amp; palavras(t)</code>.", "Ordene pelo tamanho da interseção e pegue os k primeiros."]),
        erros([("Avaliar só a resposta final.", "Meça a recuperação (o trecho certo veio?) e a fidelidade (a resposta usa os trechos?) separadamente."), ("Trechos grandes demais ou pequenos demais.", "Ver a aula de chunking."), ("Não instruir o modelo a admitir que não sabe.", "Sem isso, ele inventa quando a busca falha.")]),
        ponte("RAG em produção", "<p>Na prática, entram bancos vetoriais (próxima aula), busca híbrida com palavras-chave, reranking, chunking cuidadoso e avaliação contínua. Mas o fluxo é sempre este: buscar, montar, gerar.</p>"),
        quiz([
            ("Quais são as etapas do RAG?", ["Treinar, testar, publicar.", "Indexar, buscar e gerar.", "Tokenizar e quantizar."], 1, "Com o prompt no meio."),
            ("Por que RAG em vez de ajuste fino para documentos da empresa?", ["É mais barato de atualizar e permite citar fontes.", "É sempre mais preciso.", "Não precisa de LLM."], 0, "Troca os documentos, não o modelo."),
            ("Resposta errada num RAG: primeiro verifique:", ["A busca.", "A temperatura.", "O idioma."], 0, "O trecho certo chegou?"),
        ]),
    ],
    ["RAG = indexar, buscar e gerar com os trechos no prompt.", "Peça citações e permita “não sei”.", "Avalie recuperação e geração separadamente."],
    "Bancos vetoriais e busca semântica.",
    livro=("HF:chapter5/6", "LLM Course, seção “Semantic search with FAISS”", "Como o curso indexa e busca os embeddings?"))

AULAS["Bancos vetoriais e busca semântica"] = aula(
    30,
    "Buscar por palavras exatas falha quando a pergunta usa outras palavras: “como devolver um produto?” não casa com “política de trocas”. A busca semântica compara significados, via embeddings, e os bancos vetoriais fazem isso em milhões de documentos em milissegundos.",
    ["comparar busca por palavras e busca semântica;", "entender índices aproximados (HNSW, IVF);", "combinar as duas na busca híbrida."],
    ["Embeddings, KNN e RAG."],
    [
        chute("Para achar códigos de produto exatos (como “XZ-4410”), qual busca é melhor?", ["Semântica.", "Por palavras-chave (BM25).", "Nenhuma."], 1,
              ["Embeddings capturam sentido, não sequências exatas de caracteres.", "Isso! Termos exatos e raros são o forte da busca por palavras. Por isso a busca híbrida combina as duas.", "Uma delas resolve."],
              "Híbrida = semântica para o sentido + palavras-chave para o exato."),
        concreto("O bibliotecário e o fichário", "<p>O fichário por título só acha o livro se você souber o nome exato. Um bibliotecário entende “quero algo sobre como juntar dinheiro” e traz livros de finanças pessoais. A busca semântica é o bibliotecário; a por palavras, o fichário.</p>"),
        nota("As peças", [
            ("Busca exata (força bruta)", "comparar com todos", "Perfeita, mas lenta com milhões de vetores."),
            ("HNSW", "grafo de vizinhos", "Pula entre vizinhos até chegar perto; o padrão em bancos vetoriais."),
            ("IVF", "agrupar antes", "K-Means divide os vetores em grupos; busca só nos grupos próximos."),
            ("Metadados", "filtros", "“Só documentos de 2025, do setor jurídico.”"),
            ("Chroma, pgvector, Qdrant, FAISS", "ferramentas", "De biblioteca local a banco completo."),
        ]),
        cod("Busca vetorial com NumPy", "Implemente <code>buscar(consulta, base, k)</code>: normalize os vetores, calcule a similaridade de cosseno com toda a base de uma vez (multiplicação de matrizes) e devolva os índices dos k mais parecidos, do mais para o menos.",
            '''
import numpy as np

def buscar(consulta, base, k=2):
    return []

base = np.array([[1.0, 0.0, 0.0], [0.7, 0.7, 0.0], [0.0, 0.0, 1.0], [0.9, 0.1, 0.0]])
print(buscar(np.array([1.0, 0.05, 0.0]), base))
''',
            [("Os dois mais parecidos", "import numpy as np\nassert list(buscar(np.array([1.0, 0.05, 0.0]), base)) == [0, 3], f'{buscar(np.array([1.0, 0.05, 0.0]), base)}'"),
             ("k = 1", "import numpy as np\nassert list(buscar(np.array([0.0, 0.0, 2.0]), base, 1)) == [2]")],
            '''
import numpy as np

def buscar(consulta, base, k=2):
    b = base / np.linalg.norm(base, axis=1, keepdims=True)
    q = consulta / np.linalg.norm(consulta)
    sims = b @ q
    return np.argsort(-sims)[:k].tolist()

base = np.array([[1.0, 0.0, 0.0], [0.7, 0.7, 0.0], [0.0, 0.0, 1.0], [0.9, 0.1, 0.0]])
print(buscar(np.array([1.0, 0.05, 0.0]), base))
''', ["Normalize as linhas da base e a consulta.", "<code>sims = b @ q</code>; ordene com <code>np.argsort(-sims)</code>."]),
        cod("Busca híbrida", "Combine os rankings da busca semântica e da por palavras com a fusão por posição recíproca (RRF): cada documento ganha 1/(60 + posição) em cada lista. Devolva os documentos ordenados pela soma.",
            '''
def rrf(*rankings, k=60):
    return []

semantica = ["d3", "d1", "d2"]
palavras = ["d1", "d4", "d3"]
print(rrf(semantica, palavras))
''',
            [("Ordem combinada", "assert rrf(['d3', 'd1', 'd2'], ['d1', 'd4', 'd3']) == ['d1', 'd3', 'd4', 'd2'], f'{rrf([\"d3\", \"d1\", \"d2\"], [\"d1\", \"d4\", \"d3\"])}'")],
            '''
def rrf(*rankings, k=60):
    pontos = {}
    for ranking in rankings:
        for pos, doc in enumerate(ranking, start=1):
            pontos[doc] = pontos.get(doc, 0) + 1 / (k + pos)
    return sorted(pontos, key=pontos.get, reverse=True)

semantica = ["d3", "d1", "d2"]
palavras = ["d1", "d4", "d3"]
print(rrf(semantica, palavras))
''', ["Para cada lista e posição (começando em 1), some <code>1 / (k + pos)</code>.", "Ordene pela soma."], rot="Mão no código · nível 2"),
        erros([("Misturar embeddings de modelos diferentes no mesmo índice.", "Os espaços são incompatíveis: reindexe tudo ao trocar o modelo."), ("Esquecer de normalizar.", "Produto escalar sem normalizar favorece vetores longos."), ("Só busca semântica para códigos e nomes próprios.", "Use híbrida.")]),
        ponte("A memória dos sistemas de IA", "<p>Bancos vetoriais guardam a “memória de longo prazo” de RAGs e agentes: documentos, conversas passadas, exemplos. O pgvector, uma extensão do Postgres (Fase 6), permite fazer isso no mesmo banco que já guarda os outros dados da aplicação.</p>"),
        quiz([
            ("Busca semântica compara:", ["Palavras exatas.", "Significados, via embeddings.", "Tamanhos de documento."], 1, "Vetores."),
            ("Para que servem índices como HNSW?", ["Busca aproximada muito rápida.", "Treinar embeddings.", "Comprimir textos."], 0, "Sem comparar com todos."),
            ("O que a busca híbrida combina?", ["Duas GPUs.", "Busca semântica e por palavras-chave.", "Dois idiomas."], 1, "O melhor dos dois."),
        ]),
    ],
    ["Busca semântica compara embeddings; por palavras acha termos exatos.", "Índices aproximados (HNSW, IVF) escalam para milhões.", "Híbrida + RRF combina os dois rankings."],
    "Agentes e uso de ferramentas.",
    livro=("HF:chapter5/6", "LLM Course, seção “Semantic search with FAISS”", "Que modelo de embeddings o curso usa?"))
