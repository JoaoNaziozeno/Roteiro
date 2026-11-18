# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · tópicos acrescentados na revisão do currículo (engenharia para trabalhar com IA)."""
from lesson_factory import *

AULAS = {}

# ---------------------------------------------------------------------------------------------
AULAS["Python assíncrono (async/await)"] = aula(
    35,
    "Uma chamada a um LLM leva 2 segundos esperando a rede. Se o seu sistema precisa fazer 10 chamadas, uma de cada vez, são 20 segundos de usuário olhando para a tela. Com <b>async/await</b>, o Python dispara as 10 juntas e espera todas ao mesmo tempo: fica perto de 2 segundos. É assim que funcionam agentes, RAG com várias buscas e qualquer API que fala com outras APIs.",
    ["entender por que esperar a rede desperdiça tempo;", "escrever funções com <code>async def</code> e <code>await</code>;", "rodar várias chamadas juntas com <code>asyncio.gather</code>;", "respeitar limites de uso com <code>asyncio.Semaphore</code>."],
    ["Funções, listas e consumir APIs com requests."],
    [
        chute("Você precisa fazer 3 chamadas a uma API; cada uma demora 1 segundo só esperando a resposta. Com async, quanto tempo leva no total?", ["3 segundos, não tem jeito.", "Perto de 1 segundo.", "0 segundos."], 1,
              ["Isso acontece quando você espera uma de cada vez.", "Isso! Enquanto uma espera a rede, as outras também estão esperando: as esperas se sobrepõem.", "A espera da rede continua existindo; ela só deixa de se somar."],
              "Async não deixa a rede mais rápida: ele para de desperdiçar o tempo de espera."),
        concreto("O garçom que não fica parado", "<p>Um garçom anota o pedido da mesa 1 e leva até a cozinha. Ele <b>não fica parado</b> na porta da cozinha esperando o prato ficar pronto: vai atender a mesa 2, a mesa 3, e volta quando a cozinha chama. Um garçom só, várias mesas ao mesmo tempo.</p><p>No código, o <code>await</code> é o momento em que o garçom diz “vou esperar a cozinha, enquanto isso posso atender outra mesa”.</p>"),
        crianca("<p>Imagine que você colocou 3 pipocas no micro-ondas, uma de cada vez: são 9 minutos. Se você tivesse 3 micro-ondas e ligasse todos juntos, em 3 minutos estaria tudo pronto. O async é ligar todos os micro-ondas juntos em vez de ficar parado olhando um só.</p>"),
        ver("o que é uma corrotina e o que o <code>await</code> faz"),
        texto("Do jeito lento para o jeito rápido", py('''
import asyncio

async def chamar_modelo(pergunta):
    await asyncio.sleep(1)          # finge 1 segundo esperando a rede
    return pergunta.upper()

async def principal():
    # Uma por vez: 3 segundos
    a = await chamar_modelo("oi")
    b = await chamar_modelo("tudo bem")

    # Todas juntas: ~1 segundo
    respostas = await asyncio.gather(
        chamar_modelo("oi"), chamar_modelo("tudo bem"), chamar_modelo("tchau"))
    return respostas                 # na mesma ordem dos pedidos

asyncio.run(principal())             # num arquivo .py, é assim que se começa
''') + "<p>Nos exercícios desta página, o código roda dentro de um laço que já está ativo, então você pode escrever <code>await principal()</code> direto. Num arquivo <code>.py</code> normal, use <code>asyncio.run(principal())</code>.</p>"),
        nota("As peças do asyncio", [
            ("<code>async def f():</code>", "define uma corrotina", "Chamar <code>f()</code> não executa: devolve uma corrotina que precisa ser esperada."),
            ("<code>await x</code>", "espera x terminar", "Só funciona dentro de <code>async def</code> e libera o Python para outras tarefas."),
            ("<code>asyncio.gather(a, b, c)</code>", "roda juntas", "Devolve os resultados na mesma ordem em que você passou."),
            ("<code>asyncio.Semaphore(n)</code>", "no máximo n por vez", "Respeita limites de uso (rate limit) da API."),
            ("<code>asyncio.run(main())</code>", "ponto de partida", "Usado uma vez, no começo do programa."),
        ]),
        cod("Três perguntas ao mesmo tempo", "Complete <code>sequencial</code> (uma pergunta por vez, com <code>await</code>) e <code>concorrente</code> (todas juntas, com <code>asyncio.gather</code>). As duas devem devolver as respostas <b>na ordem das perguntas</b>, e a concorrente precisa ser bem mais rápida.",
            '''
import asyncio, time

async def chamar_modelo(pergunta, segundos=0.05):
    await asyncio.sleep(segundos)          # finge a espera da rede
    return pergunta.upper()

async def sequencial(perguntas):
    # chame uma pergunta por vez, esperando cada resposta
    return []

async def concorrente(perguntas):
    # dispare todas juntas com asyncio.gather
    return []

perguntas = ["oi", "tudo bem", "tchau"]
t0 = time.perf_counter(); r1 = await sequencial(perguntas); t1 = time.perf_counter() - t0
t0 = time.perf_counter(); r2 = await concorrente(perguntas); t2 = time.perf_counter() - t0
print(r1, round(t1, 2))
print(r2, round(t2, 2))
''',
            [("Sequencial devolve na ordem", 'assert r1 == ["OI", "TUDO BEM", "TCHAU"], r1'),
             ("Concorrente devolve na ordem", 'assert r2 == ["OI", "TUDO BEM", "TCHAU"], r2'),
             ("Concorrente é bem mais rápida", "assert t2 < t1 * 0.7, (t1, t2)"),
             ("Cinco juntas levam o tempo de uma", "import time as _t\n_a = _t.perf_counter()\n_r = await concorrente(['x'] * 5)\nassert _r == ['X'] * 5 and _t.perf_counter() - _a < 0.15")],
            '''
import asyncio, time

async def chamar_modelo(pergunta, segundos=0.05):
    await asyncio.sleep(segundos)          # finge a espera da rede
    return pergunta.upper()

async def sequencial(perguntas):
    respostas = []
    for p in perguntas:
        respostas.append(await chamar_modelo(p))
    return respostas

async def concorrente(perguntas):
    return list(await asyncio.gather(*(chamar_modelo(p) for p in perguntas)))

perguntas = ["oi", "tudo bem", "tchau"]
t0 = time.perf_counter(); r1 = await sequencial(perguntas); t1 = time.perf_counter() - t0
t0 = time.perf_counter(); r2 = await concorrente(perguntas); t2 = time.perf_counter() - t0
print(r1, round(t1, 2))
print(r2, round(t2, 2))
''', ["No sequencial, use um <code>for</code> com <code>await chamar_modelo(p)</code> dentro.", "No concorrente, crie as corrotinas sem esperar e passe todas para <code>asyncio.gather(*...)</code>.", "O asterisco em <code>gather(*lista)</code> espalha a lista como vários argumentos."]),
        cod("Respeitando o limite da API", "A API só aceita <b>2 chamadas ao mesmo tempo</b>. A versão abaixo dispara tudo junto e estoura o limite. Use <code>asyncio.Semaphore</code> em <code>com_limite</code> para nunca passar de <code>limite</code> chamadas simultâneas, mantendo a ordem das respostas.",
            '''
import asyncio

ativas = 0
pico = 0

async def chamar_api(x):
    global ativas, pico
    ativas += 1
    pico = max(pico, ativas)
    await asyncio.sleep(0.02)
    ativas -= 1
    return x * 10

async def com_limite(itens, limite):
    return list(await asyncio.gather(*(chamar_api(x) for x in itens)))

resultado = await com_limite([1, 2, 3, 4, 5, 6], 2)
print(resultado, "pico de chamadas simultâneas:", pico)
''',
            [("Mantém a ordem", "assert resultado == [10, 20, 30, 40, 50, 60], resultado"),
             ("Nunca passa do limite", "assert pico <= 2, pico"),
             ("Ainda roda em paralelo (não é uma por vez)", "assert pico == 2, pico")],
            '''
import asyncio

ativas = 0
pico = 0

async def chamar_api(x):
    global ativas, pico
    ativas += 1
    pico = max(pico, ativas)
    await asyncio.sleep(0.02)
    ativas -= 1
    return x * 10

async def com_limite(itens, limite):
    sem = asyncio.Semaphore(limite)

    async def uma(x):
        async with sem:              # espera uma vaga antes de chamar
            return await chamar_api(x)

    return list(await asyncio.gather(*(uma(x) for x in itens)))

resultado = await com_limite([1, 2, 3, 4, 5, 6], 2)
print(resultado, "pico de chamadas simultâneas:", pico)
''', ["Crie <code>sem = asyncio.Semaphore(limite)</code> dentro de <code>com_limite</code>.", "Escreva uma função interna <code>async def uma(x)</code> que faz <code>async with sem:</code> antes de chamar a API.", "Passe <code>uma(x)</code> para o gather, no lugar de <code>chamar_api(x)</code>."]),
        erros([
            ("Chamar <code>f()</code> de uma função async e esquecer o <code>await</code>.", "Sem await você recebe um objeto corrotina, não o resultado, e o Python avisa “coroutine was never awaited”."),
            ("Usar <code>time.sleep</code> ou <code>requests</code> dentro de código async.", "Eles travam tudo. Use <code>asyncio.sleep</code> e bibliotecas async, como <code>httpx.AsyncClient</code>."),
            ("Disparar mil chamadas juntas.", "A API devolve erro 429 (limite de uso). Use um Semaphore para controlar quantas vão ao mesmo tempo."),
            ("Achar que async acelera cálculo pesado.", "Async ajuda quando o programa espera (rede, disco). Para cálculo pesado de CPU, ele não ajuda."),
        ]),
        ponte("Onde você vai usar isso", "<p>O FastAPI aceita rotas com <code>async def</code>; os SDKs de LLM têm clientes assíncronos; um agente que consulta três ferramentas pode consultar as três ao mesmo tempo. Na aula de RAG, buscar em vários documentos juntos é exatamente o <code>gather</code> desta aula.</p>"),
        quiz([
            ("O que o <code>await</code> faz?", ["Espera o resultado e libera o Python para outras tarefas enquanto isso.", "Deixa o código mais rápido para calcular.", "Cria uma nova thread."], 0, "Ele marca o ponto de espera: enquanto uma tarefa espera, outras andam."),
            ("Em que ordem o <code>asyncio.gather(a, b, c)</code> devolve os resultados?", ["Na ordem em que terminarem.", "Na mesma ordem em que foram passados.", "Em ordem aleatória."], 1, "A ordem dos resultados é sempre a dos argumentos."),
            ("Para não passar do limite de uso de uma API, você usa:", ["<code>asyncio.Semaphore</code>", "<code>time.sleep</code>", "<code>print</code>"], 0, "O Semaphore deixa no máximo n tarefas dentro do bloco ao mesmo tempo."),
        ]),
    ],
    ["Async serve para não desperdiçar o tempo de espera da rede.", "<code>async def</code> cria corrotinas; <code>await</code> espera; <code>gather</code> roda juntas, mantendo a ordem.", "Semaphore controla quantas chamadas vão ao mesmo tempo."],
    "Ferramentas: Git, GitHub e APIs.",
    livro=("FASTAPI:async", "Documentação do FastAPI, “Concorrência e async / await”", "Quando a documentação recomenda usar async def e quando não?"))

# ---------------------------------------------------------------------------------------------
AULAS["Desenvolver com assistentes de IA (Claude Code, Copilot, Cursor)"] = aula(
    30,
    "Assistentes de código (Claude Code, GitHub Copilot, Cursor) escrevem funções inteiras em segundos. Em 2026, saber usar bem essas ferramentas é cobrado em entrevista. Mas existe uma diferença enorme entre quem <b>dirige</b> o assistente e quem é dirigido por ele: o primeiro entrega mais e melhor; o segundo cola código que não entende e quebra o sistema. Esta aula é sobre ser o primeiro.",
    ["escrever pedidos claros, com contexto e exemplos;", "revisar e testar o código gerado antes de aceitar;", "proteger segredos e dados ao usar assistentes;", "encaixar o assistente no fluxo de Git."],
    ["Funções, testes simples com pytest e Git."],
    [
        chute("O assistente gerou uma função que parece certa e roda sem erro. O que você faz?", ["Aceita e faz o commit: rodou, está certo.", "Lê, escreve ou roda testes com casos de borda, e só então aceita.", "Pede para ele gerar de novo até parecer melhor."], 1,
              ["Rodar sem erro não quer dizer estar certo: o bug mais comum é o silencioso.", "Isso! Você é o responsável pelo código, não o assistente.", "Gerar de novo sem critério é loteria."],
              "Código gerado é um rascunho de um colega muito rápido, que às vezes se engana com toda a confiança do mundo."),
        concreto("O estagiário genial e distraído", "<p>Pense no assistente como um estagiário que digita absurdamente rápido, conhece todas as bibliotecas, mas não conhece o seu sistema e às vezes inventa coisas com convicção. Você não deixaria um estagiário publicar código sem revisão. Explicar bem a tarefa e revisar o resultado continua sendo o seu trabalho.</p>"),
        ver("como a pessoa do vídeo pede as tarefas e confere o que foi gerado"),
        tabela("Pedido fraco × pedido forte", ["Pedido fraco", "Pedido forte"], [
            ["“faz uma função de média móvel”", "“função <code>media_movel(valores, n)</code> que devolve a média de cada janela de n valores seguidos; n ≤ 0 levanta ValueError; exemplo: [1,2,3,4] e n=2 dá [1.5, 2.5, 3.5]”"],
            ["“arruma esse erro”", "“o teste <code>test_vazio</code> falha com IndexError na linha 12 quando a lista está vazia; corrija sem mudar o comportamento dos outros testes”"],
            ["“melhora esse código”", "“extraia a validação da função <code>salvar</code> para uma função separada e mantenha os testes passando”"],
        ], rot="Contexto + exemplo + critério de pronto"),
        ordem("O fluxo que funciona", [
            "Escreva o que a função deve fazer, com exemplos e casos de borda",
            "Peça ao assistente, dando o contexto (arquivo, assinatura, exemplo)",
            "Leia o código gerado linha por linha",
            "Rode os testes, incluindo os casos de borda",
            "Corrija o que falhar e só então faça o commit",
        ], corpo="<p>Coloque os passos na ordem em que um bom desenvolvedor trabalha com o assistente.</p>",
            exp="Especificar antes e testar depois é o que separa usar a IA de ser usado por ela."),
        cod("Revise o código do assistente", "Você pediu ao assistente: “<i>média móvel dos últimos n valores; n ≤ 0 deve levantar ValueError</i>”. Ele gerou o código abaixo, que roda sem erro. Ele tem <b>dois problemas</b>. Encontre e corrija.",
            '''
# Código sugerido pelo assistente
def media_movel(valores, n):
    resultado = []
    for i in range(len(valores) - n):
        resultado.append(sum(valores[i:i + n]) / n)
    return resultado

print(media_movel([1, 2, 3, 4], 2))   # esperado: [1.5, 2.5, 3.5]
''',
            [("Inclui a última janela", "assert media_movel([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]"),
             ("Janela do tamanho da lista dá um valor", "assert media_movel([2, 4, 6], 3) == [4.0]"),
             ("Janela maior que a lista dá lista vazia", "assert media_movel([1, 2], 5) == []"),
             ("n inválido levanta ValueError", "try:\n    media_movel([1, 2, 3], 0)\n    assert False, 'deveria levantar ValueError'\nexcept ValueError:\n    pass")],
            '''
def media_movel(valores, n):
    if n <= 0:
        raise ValueError("n precisa ser maior que zero")
    resultado = []
    for i in range(len(valores) - n + 1):
        resultado.append(sum(valores[i:i + n]) / n)
    return resultado

print(media_movel([1, 2, 3, 4], 2))   # esperado: [1.5, 2.5, 3.5]
''', ["Conte quantas janelas de tamanho 2 cabem em 4 valores. O <code>range</code> está gerando essa quantidade?", "O pedido falava de n ≤ 0. O código trata esse caso?", "Com n = 0 o código atual nem chega a dividir: o laço roda e devolve uma lista sem sentido."],
            exp="O assistente errou o limite do <code>range</code> (faltou o +1) e ignorou um requisito do pedido. Dois erros típicos: um de detalhe e um de esquecimento."),
        erros([
            ("Colar chaves de API, senhas ou dados de clientes no prompt.", "Use variáveis de ambiente e dados fictícios. O que você cola pode sair da sua máquina."),
            ("Aceitar código que você não entende.", "Peça para o assistente explicar linha por linha, ou reescreva de um jeito que você entenda. Você vai dar manutenção nele."),
            ("Pedir tudo de uma vez (“faz o sistema inteiro”).", "Peça em passos pequenos e testáveis, um commit por passo."),
            ("Confiar em bibliotecas ou funções que o assistente citou.", "Confira na documentação: assistentes às vezes inventam funções que não existem."),
        ]),
        pense("Como isso aparece numa entrevista?", "O entrevistador pergunta: “Você usa IA para programar? Como garante a qualidade?”. O que você responde?",
              "<p>Algo como: “Uso para acelerar, mas trato como rascunho. Escrevo a especificação com exemplos, peço em passos pequenos, leio o código, rodo os testes e reviso o diff antes do commit. Nunca colo segredos nem dados reais.” Mostrar um processo vale mais do que dizer que usa a ferramenta.</p>"),
        ponte("O que você já faz", "<p>Este roteiro foi construído assim: você descreve o que quer, o assistente propõe, e cada mudança é testada e revisada antes de virar um commit. Na Fase 6, o CI/CD automatiza a parte de rodar os testes a cada mudança.</p>"),
        quiz([
            ("O que torna um pedido ao assistente mais eficaz?", ["Contexto, exemplos de entrada e saída e o critério de pronto.", "Ser bem curto.", "Repetir o pedido várias vezes."], 0, "Quanto mais claro o “o que é certo”, melhor o resultado e mais fácil a revisão."),
            ("O código gerado rodou sem erro. Isso garante que está correto?", ["Sim.", "Não: é preciso testar, principalmente os casos de borda.", "Só se o assistente disser que está certo."], 1, "Bugs silenciosos rodam sem erro."),
            ("O que nunca deve ir para o prompt?", ["Chaves de API e dados pessoais reais.", "O nome da função.", "Um exemplo de entrada."], 0, "Segredos e dados pessoais ficam fora do prompt; use dados fictícios."),
        ]),
    ],
    ["Trate o código gerado como rascunho: leia, teste e só então aceite.", "Bons pedidos têm contexto, exemplos e critério de pronto.", "Segredos e dados reais nunca vão para o prompt."],
    "Boas práticas: estilo de código PEP 8.")

# ---------------------------------------------------------------------------------------------
AULAS["Tipagem, dataclasses e Pydantic"] = aula(
    35,
    "Quando você pede a um LLM “responda em JSON”, às vezes vem um campo faltando, um número como texto ou um valor inventado. Se o seu código confia cegamente, ele quebra lá na frente, longe do problema. <b>Tipagem</b> documenta o que cada coisa deve ser; <b>dataclasses</b> organizam os dados; o <b>Pydantic</b> confere na entrada e recusa o que veio errado. É a base de APIs (FastAPI), de saída estruturada e de ferramentas para agentes.",
    ["anotar tipos em funções e variáveis;", "criar classes de dados com <code>@dataclass</code>;", "validar dados de fora (APIs, LLMs) com modelos do Pydantic."],
    ["Funções, classes e dicionários; saber o que é JSON."],
    [
        chute("O LLM devolveu <code>{\"confianca\": \"alta\"}</code>, mas o seu código espera um número entre 0 e 1. Quando é melhor descobrir o problema?", ["Quando o relatório sair com um gráfico estranho.", "Logo na entrada, ao receber a resposta.", "Nunca: o modelo sempre acerta."], 1,
              ["Aí o erro já se espalhou e fica difícil achar a origem.", "Isso! Validar na fronteira (onde o dado entra) é a regra de ouro.", "Modelos erram formato com frequência."],
              "Dado de fora (usuário, API, LLM) é sempre suspeito até ser validado."),
        concreto("A conferência no recebimento", "<p>Num depósito de materiais de obra, o conferente confere a nota na entrada: 50 sacos de cimento, marca certa, sem saco rasgado. Se faltar algo, ele recusa ali, na porta. Ninguém descobre o problema três semanas depois, no meio da laje. O Pydantic é o conferente do seu código.</p>"),
        ver("como os tipos viram validação de verdade no Pydantic"),
        texto("Tipos, dataclass e Pydantic", py('''
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, ValidationError

def total(precos: list[float], desconto: float = 0.0) -> float:   # dicas de tipo
    return sum(precos) * (1 - desconto)

@dataclass
class Item:                      # classe de dados: menos código repetitivo
    nome: str
    preco: float
    tags: list[str] = field(default_factory=list)

class Resposta(BaseModel):       # Pydantic: valida de verdade
    sentimento: str
    confianca: float = Field(ge=0, le=1)

Resposta.model_validate_json('{"sentimento": "positivo", "confianca": 0.9}')   # ok
Resposta.model_validate_json('{"sentimento": "positivo", "confianca": 7}')     # ValidationError
''')),
        tabela("Qual usar?", ["Ferramenta", "Confere em tempo de execução?", "Quando usar"], [
            ["Dicas de tipo (<code>x: int</code>)", "Não (só o editor e o mypy avisam)", "Sempre: documentam e pegam erros no editor."],
            ["<code>@dataclass</code>", "Não", "Dados internos do seu programa."],
            ["Pydantic <code>BaseModel</code>", "Sim, e converte quando dá", "Dados que vêm de fora: APIs, arquivos, respostas de LLM."],
        ]),
        cod("Uma dataclass sem a armadilha da lista", "Crie a dataclass <code>Produto</code> com <code>nome: str</code>, <code>preco: float</code> e <code>tags: list[str]</code> começando vazia. Cuidado: cada produto precisa ter a <b>sua própria</b> lista de tags. Depois complete <code>total</code>, que soma os preços de uma lista de produtos.",
            '''
from dataclasses import dataclass, field

@dataclass
class Produto:
    nome: str
    preco: float
    tags: list = []          # isso está certo?

def total(itens: list[Produto]) -> float:
    return 0.0

a = Produto("cimento", 35.0)
b = Produto("areia", 120.0)
a.tags.append("obra")
print(a, b, total([a, b]))
''',
            [("Cria os produtos", "assert a.nome == 'cimento' and b.preco == 120.0"),
             ("Cada produto tem a sua lista", "assert a.tags == ['obra'] and b.tags == [], (a.tags, b.tags)"),
             ("Soma os preços", "assert total([a, b]) == 155.0 and total([]) == 0"),
             ("Tem dicas de tipo", "import typing\nassert typing.get_type_hints(Produto)['preco'] is float")],
            '''
from dataclasses import dataclass, field

@dataclass
class Produto:
    nome: str
    preco: float
    tags: list[str] = field(default_factory=list)

def total(itens: list[Produto]) -> float:
    return sum(p.preco for p in itens)

a = Produto("cimento", 35.0)
b = Produto("areia", 120.0)
a.tags.append("obra")
print(a, b, total([a, b]))
''', ["Rode o código como está: a própria dataclass reclama da lista. Por quê?", "Para valores mutáveis (listas, dicionários), use <code>field(default_factory=list)</code>.", "Em <code>total</code>, some <code>p.preco</code> para cada <code>p</code> da lista."],
            exp="Uma lista como valor padrão seria compartilhada por todos os objetos. A dataclass proíbe isso e indica <code>default_factory</code>, que cria uma lista nova para cada produto."),
        cod("Validando a resposta de um LLM", "Você pediu a um LLM a análise de sentimento de um comentário, em JSON. Crie o modelo <code>Resposta</code> do Pydantic com: <code>sentimento</code> que só aceita \"positivo\", \"negativo\" ou \"neutro\"; <code>confianca</code> entre 0 e 1; e <code>motivos</code>, uma lista de textos. Complete <code>ler</code>: devolve o modelo quando o JSON é válido e <code>None</code> quando não é.",
            '''
from typing import Literal
from pydantic import BaseModel, Field, ValidationError

class Resposta(BaseModel):
    sentimento: str
    confianca: float
    motivos: list

def ler(texto_json):
    return Resposta.model_validate_json(texto_json)

print(ler('{"sentimento": "positivo", "confianca": 0.92, "motivos": ["elogiou o prazo"]}'))
''',
            [("Aceita uma resposta válida", "r = ler('{\"sentimento\": \"positivo\", \"confianca\": 0.92, \"motivos\": [\"elogiou o prazo\"]}')\nassert r is not None and r.sentimento == 'positivo' and r.confianca == 0.92"),
             ("Recusa sentimento inventado", "assert ler('{\"sentimento\": \"feliz\", \"confianca\": 0.5, \"motivos\": []}') is None"),
             ("Recusa confiança fora de 0 a 1", "assert ler('{\"sentimento\": \"neutro\", \"confianca\": 7, \"motivos\": []}') is None"),
             ("Recusa campo faltando", "assert ler('{\"sentimento\": \"neutro\", \"motivos\": []}') is None"),
             ("Recusa JSON quebrado", "assert ler('isso não é json') is None")],
            '''
from typing import Literal
from pydantic import BaseModel, Field, ValidationError

class Resposta(BaseModel):
    sentimento: Literal["positivo", "negativo", "neutro"]
    confianca: float = Field(ge=0, le=1)
    motivos: list[str]

def ler(texto_json):
    try:
        return Resposta.model_validate_json(texto_json)
    except ValidationError:
        return None

print(ler('{"sentimento": "positivo", "confianca": 0.92, "motivos": ["elogiou o prazo"]}'))
''', ["Para limitar os valores possíveis, use <code>Literal[\"positivo\", \"negativo\", \"neutro\"]</code>.", "Para o intervalo, use <code>Field(ge=0, le=1)</code> (ge = maior ou igual; le = menor ou igual).", "Envolva a leitura em <code>try/except ValidationError</code> e devolva <code>None</code> no except (JSON quebrado também gera ValidationError)."]),
        erros([
            ("Achar que dica de tipo valida sozinha.", "<code>def f(x: int)</code> aceita uma string sem reclamar. Quem valida em execução é o Pydantic."),
            ("Usar <code>tags: list = []</code> como padrão.", "Use <code>field(default_factory=list)</code> na dataclass (no Pydantic, <code>Field(default_factory=list)</code>)."),
            ("Validar só no meio do código.", "Valide na fronteira: assim que o dado chega de fora."),
            ("Engolir o erro de validação em silêncio.", "Registre no log o que veio errado: é assim que você descobre que o prompt precisa melhorar."),
        ]),
        ponte("Saída estruturada e FastAPI", "<p>Na Fase 5, a aula de saída estruturada usa exatamente este modelo para obrigar o LLM a responder no formato certo. Na Fase 6, o FastAPI usa modelos do Pydantic para validar o que chega na sua API e gerar a documentação sozinho.</p>"),
        quiz([
            ("Qual destas confere os dados em tempo de execução?", ["Dica de tipo <code>x: int</code>", "Pydantic <code>BaseModel</code>", "Comentário no código"], 1, "Dicas de tipo ajudam o editor; o Pydantic valida de verdade."),
            ("Por que usar <code>field(default_factory=list)</code>?", ["Para cada objeto ter a sua própria lista.", "Para a lista ficar mais rápida.", "Para a lista ser imutável."], 0, "Sem isso, a mesma lista seria compartilhada por todos."),
            ("Onde validar a resposta de um LLM?", ["Assim que ela chega, antes de usar.", "Só no relatório final.", "Não precisa validar."], 0, "Valide na fronteira."),
        ]),
    ],
    ["Dicas de tipo documentam; o Pydantic valida em execução.", "Dataclasses organizam dados internos; use <code>default_factory</code> para listas.", "Todo dado de fora (API, usuário, LLM) passa por validação na entrada."],
    "Bibliotecas úteis: datetime.",
    livro=("FASTAPI:python-types", "Documentação do FastAPI, “Introdução aos tipos Python”", "Como o FastAPI e o Pydantic aproveitam as dicas de tipo?"))

# ---------------------------------------------------------------------------------------------
AULAS["LGPD e dados pessoais em sistemas de IA"] = aula(
    30,
    "Todo sistema de IA que você construir no Brasil vai tocar em dados de pessoas: nome, CPF, e-mail, conversas de atendimento. A <b>LGPD</b> (Lei Geral de Proteção de Dados, Lei 13.709/2018) diz o que pode e o que não pode ser feito, e as empresas perguntam isso em entrevista. Esta aula não é consultoria jurídica: é o que um engenheiro de IA precisa saber para não colocar a empresa (e as pessoas) em risco.",
    ["reconhecer dados pessoais e dados sensíveis;", "aplicar os princípios de finalidade e necessidade em projetos de IA;", "mascarar dados pessoais antes de enviar a um LLM;", "saber quando chamar o jurídico ou o encarregado de dados (DPO)."],
    ["Expressões regulares (re) e APIs de LLMs."],
    [
        chute("Você vai usar um LLM de uma empresa de fora para resumir conversas de atendimento. As conversas têm CPF e telefone dos clientes. O que fazer primeiro?", ["Enviar tudo: o resumo fica melhor.", "Retirar ou mascarar o CPF e o telefone antes de enviar.", "Não usar IA nunca."], 1,
              ["Enviar dado que o resumo não precisa contraria o princípio da necessidade.", "Isso! O resumo não precisa do CPF: o que não é necessário não sai de casa.", "Dá para usar, com cuidado."],
              "Necessidade: use só os dados pessoais indispensáveis para a finalidade."),
        concreto("A planta da casa do cliente", "<p>Numa obra, você recebe a planta e as chaves da casa do cliente para fazer a reforma. Isso não te dá o direito de usar a casa para outra coisa, nem de mostrar a planta para quem quiser. Dados pessoais são parecidos: você recebe para uma finalidade, guarda com cuidado e devolve ou apaga quando acaba.</p>"),
        ver("quais riscos de IA com dados pessoais o palestrante destaca"),
        tabela("O essencial da LGPD para quem faz IA", ["Conceito", "O que significa na prática"], [
            ["Dado pessoal", "Qualquer informação que identifica alguém: nome, CPF, e-mail, telefone, endereço, IP."],
            ["Dado sensível", "Saúde, biometria, origem racial, religião, opinião política, vida sexual, dado genético. Exige cuidado redobrado."],
            ["Finalidade", "Use o dado só para o objetivo informado à pessoa."],
            ["Necessidade", "Colete e envie só o mínimo indispensável."],
            ["Base legal", "Todo tratamento precisa de uma (ex.: consentimento, execução de contrato, legítimo interesse). Quem define é o jurídico."],
            ["Direitos do titular", "A pessoa pode pedir acesso, correção, exclusão e explicação sobre decisões automatizadas."],
            ["ANPD", "Autoridade Nacional de Proteção de Dados: fiscaliza e pode multar."],
        ]),
        nota("Técnicas de proteção que o engenheiro aplica", [
            ("Mascarar", "trocar por um rótulo", "<code>João, CPF 123.456.789-00</code> vira <code>João, CPF [CPF]</code>."),
            ("Pseudonimizar", "trocar por um código", "O cliente vira <code>cliente_4821</code>; a tabela de correspondência fica guardada à parte."),
            ("Anonimizar", "impossível voltar", "Agregados e dados sem como reidentificar. Dado anonimizado sai do alcance da LGPD."),
            ("Minimizar", "não coletar", "O melhor dado pessoal para proteger é o que você nunca guardou."),
        ]),
        cod("Mascarando dados antes do LLM", "Complete <code>mascarar</code>: troque CPFs (formato <code>123.456.789-00</code>) por <code>[CPF]</code>, e-mails por <code>[EMAIL]</code> e telefones (formato <code>(11) 98765-4321</code> ou <code>(11) 3456-7890</code>) por <code>[TELEFONE]</code>. O resto do texto não pode mudar.",
            '''
import re

def mascarar(texto):
    return texto

msg = "Sou a Ana, CPF 123.456.789-00, e-mail ana.souza@gmail.com, telefone (11) 98765-4321. Meu pedido atrasou."
print(mascarar(msg))
''',
            [("Mascara CPF", "assert '[CPF]' in mascarar('CPF 123.456.789-00 ok') and '123.456' not in mascarar('CPF 123.456.789-00 ok')"),
             ("Mascara e-mail", "assert mascarar('fale com ana.souza@gmail.com hoje') == 'fale com [EMAIL] hoje'"),
             ("Mascara celular e fixo", "assert mascarar('(11) 98765-4321 ou (21) 3456-7890') == '[TELEFONE] ou [TELEFONE]'"),
             ("Mantém o resto do texto", "r = mascarar(msg)\nassert r == 'Sou a Ana, CPF [CPF], e-mail [EMAIL], telefone [TELEFONE]. Meu pedido atrasou.', r")],
            '''
import re

def mascarar(texto):
    texto = re.sub(r"\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}", "[CPF]", texto)
    texto = re.sub(r"[\\w.+-]+@[\\w-]+(\\.[\\w-]+)+", "[EMAIL]", texto)
    texto = re.sub(r"\\(\\d{2}\\)\\s?\\d{4,5}-\\d{4}", "[TELEFONE]", texto)
    return texto

msg = "Sou a Ana, CPF 123.456.789-00, e-mail ana.souza@gmail.com, telefone (11) 98765-4321. Meu pedido atrasou."
print(mascarar(msg))
''', ["Use <code>re.sub(padrão, substituto, texto)</code>, uma vez para cada tipo de dado.", "CPF: três dígitos, ponto, três, ponto, três, hífen, dois: <code>\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}</code>.", "Telefone: <code>\\(\\d{2}\\)\\s?\\d{4,5}-\\d{4}</code> pega celular (5 dígitos) e fixo (4)."],
            exp="Na prática, além de regex, existem bibliotecas que detectam nomes e endereços (como o Presidio, da Microsoft). A regex é a primeira camada, não a única."),
        erros([
            ("Mandar a base inteira de clientes para o LLM “para dar contexto”.", "Envie só o necessário, mascarado. Se der, use modelos que rodam dentro da empresa."),
            ("Guardar logs com o texto completo dos usuários.", "Mascare antes de gravar o log e defina por quanto tempo os logs ficam guardados."),
            ("Usar dados de clientes para treinar um modelo sem avisar.", "Treinar é uma nova finalidade: precisa de base legal. Converse com o jurídico."),
            ("Achar que “é só um teste” e usar dados reais.", "Em teste, use dados fictícios ou anonimizados."),
        ]),
        pense("Entrevista: o caso do chatbot do banco", "Você vai construir um chatbot que responde dúvidas de clientes de um banco usando RAG. Que cuidados de LGPD você citaria?",
              "<p>Mascarar dados pessoais antes de enviar ao modelo; não indexar documentos com dados de outros clientes no RAG; controlar quem acessa o quê; registrar logs sem dados pessoais; definir tempo de retenção; permitir que o cliente peça a exclusão; e envolver o encarregado de dados (DPO) desde o início. Citar o princípio da necessidade e a ANPD mostra maturidade.</p>"),
        ponte("Ligação com segurança de LLMs", "<p>A aula de prompt injection mostrou como um texto malicioso pode fazer o modelo vazar informações. Se os dados pessoais já foram mascarados antes, mesmo um ataque bem-sucedido vaza muito menos. Proteção de dados e segurança andam juntas.</p>"),
        quiz([
            ("Qual destes é dado <b>sensível</b> pela LGPD?", ["E-mail", "Informação de saúde", "Nome da empresa"], 1, "Saúde, biometria, religião, origem racial, entre outros, são sensíveis."),
            ("O princípio da necessidade diz que você deve:", ["Coletar o máximo possível para treinar melhor.", "Usar só os dados pessoais indispensáveis para a finalidade.", "Guardar tudo para sempre."], 1, "Mínimo indispensável."),
            ("Antes de enviar conversas de clientes a um LLM externo, o mais adequado é:", ["Mascarar os dados pessoais desnecessários.", "Enviar sem mudanças.", "Traduzir para o inglês."], 0, "O que não é necessário não deve sair."),
        ]),
    ],
    ["Dado pessoal identifica alguém; dado sensível exige cuidado redobrado.", "Finalidade e necessidade: use só o mínimo, só para o objetivo informado.", "Mascare antes de enviar a LLMs e de gravar logs; envolva o jurídico e o DPO."],
    "Engenharia: Docker.")

# ---------------------------------------------------------------------------------------------
AULAS["Erros, tentativas e logs em produção"] = aula(
    35,
    "Em produção, APIs de LLM falham de verdade: tempo esgotado, erro 429 (limite de uso), servidor fora do ar por alguns segundos. Um sistema amador quebra na primeira falha e ninguém sabe por quê. Um sistema profissional <b>tenta de novo</b> do jeito certo, <b>desiste</b> quando não adianta e <b>registra</b> tudo num log que conta a história do que aconteceu.",
    ["diferenciar erros temporários de erros permanentes;", "implementar novas tentativas com espera crescente (backoff exponencial);", "registrar eventos com o módulo <code>logging</code>, sem vazar dados."],
    ["Tratamento de erros (try/except), funções e testes."],
    [
        chute("A API do LLM respondeu “erro 429: muitas requisições”. O que faz mais sentido?", ["Tentar de novo imediatamente, em loop, até dar certo.", "Esperar um pouco e tentar de novo, esperando mais a cada falha.", "Desistir e mostrar erro ao usuário na hora."], 1,
              ["Tentar sem parar piora o congestionamento e pode bloquear sua conta.", "Isso! É o backoff exponencial: 1 s, 2 s, 4 s...", "Muitas vezes, alguns segundos depois funciona."],
              "Erro temporário: espere e tente de novo, com limite. Erro permanente: não adianta tentar."),
        concreto("O pedreiro e a betoneira", "<p>A betoneira desligou. O pedreiro experiente espera um minuto (pode ter sido o disjuntor), tenta ligar de novo; se falhar, espera mais e tenta mais uma vez. Na terceira, chama o eletricista e <b>anota no diário de obra</b> o que aconteceu e a que horas. Ele não fica apertando o botão sem parar, nem desiste na primeira. O diário de obra é o log.</p>"),
        ver("como os níveis de log (DEBUG, INFO, WARNING, ERROR) são usados"),
        tabela("Tentar de novo ou não?", ["Erro", "Tipo", "O que fazer"], [
            ["Tempo esgotado (timeout)", "Temporário", "Tentar de novo com espera."],
            ["429 · limite de uso", "Temporário", "Esperar (às vezes a API diz quanto) e tentar de novo."],
            ["500 / 503 · servidor fora", "Temporário", "Tentar de novo com espera."],
            ["400 · pedido inválido", "Permanente", "Não adianta repetir: corrija o pedido."],
            ["401 · chave inválida", "Permanente", "Não repetir; avisar e corrigir a configuração."],
        ]),
        nota("Logging do jeito certo", [
            ("<code>logging.basicConfig(level=logging.INFO)</code>", "configura uma vez", "No início do programa, com formato e nível."),
            ("<code>log = logging.getLogger(__name__)</code>", "um logger por módulo", "Mostra de onde veio cada mensagem."),
            ("<code>log.warning(\"tentativa %s falhou\", n)</code>", "mensagem com parâmetros", "Use os parâmetros em vez de f-string."),
            ("<code>log.exception(\"falhou\")</code>", "dentro do except", "Registra a mensagem e o erro completo."),
            ("DEBUG < INFO < WARNING < ERROR", "níveis", "Em produção, normalmente INFO para cima."),
        ]),
        cod("Tentar de novo, do jeito certo", "Complete <code>com_tentativas</code>: chame <code>func()</code>; se der <code>TimeoutError</code> ou <code>ConnectionError</code>, registre um aviso no log, espere (<code>dormir(espera)</code>) e tente de novo, <b>dobrando a espera</b> a cada falha. Depois de <code>tentativas</code> falhas, levante o último erro. Qualquer outro erro (como <code>ValueError</code>) sobe <b>na hora</b>, sem nova tentativa.",
            '''
import logging, time
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("llm")

TEMPORARIOS = (TimeoutError, ConnectionError)

def com_tentativas(func, tentativas=3, espera=1.0, dormir=time.sleep):
    return func()

# Simulação: uma API que falha 2 vezes e depois responde
chamadas = []
def api_instavel():
    chamadas.append(1)
    if len(chamadas) < 3:
        raise TimeoutError("demorou demais")
    return "resposta do modelo"

esperas = []
print(com_tentativas(api_instavel, dormir=esperas.append), esperas)
''',
            [("Tenta de novo até funcionar", "assert len(chamadas) == 3, len(chamadas)"),
             ("Espera dobra a cada falha", "assert esperas == [1.0, 2.0], esperas"),
             ("Desiste depois do limite", "n = []\ndef sempre_cai():\n    n.append(1)\n    raise ConnectionError('fora do ar')\ntry:\n    com_tentativas(sempre_cai, tentativas=3, dormir=lambda s: None)\n    assert False, 'deveria levantar'\nexcept ConnectionError:\n    pass\nassert len(n) == 3, len(n)"),
             ("Erro permanente não repete", "m = []\ndef pedido_errado():\n    m.append(1)\n    raise ValueError('pedido inválido')\ntry:\n    com_tentativas(pedido_errado, dormir=lambda s: None)\n    assert False, 'deveria levantar'\nexcept ValueError:\n    pass\nassert len(m) == 1, len(m)")],
            '''
import logging, time
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("llm")

TEMPORARIOS = (TimeoutError, ConnectionError)

def com_tentativas(func, tentativas=3, espera=1.0, dormir=time.sleep):
    for n in range(1, tentativas + 1):
        try:
            return func()
        except TEMPORARIOS as erro:
            if n == tentativas:
                log.error("desistindo depois de %s tentativas: %s", n, erro)
                raise
            log.warning("tentativa %s falhou (%s); nova tentativa em %.1f s", n, erro, espera)
            dormir(espera)
            espera *= 2

# Simulação: uma API que falha 2 vezes e depois responde
chamadas = []
def api_instavel():
    chamadas.append(1)
    if len(chamadas) < 3:
        raise TimeoutError("demorou demais")
    return "resposta do modelo"

esperas = []
print(com_tentativas(api_instavel, dormir=esperas.append), esperas)
''', ["Use um <code>for n in range(1, tentativas + 1)</code> com <code>try: return func()</code> dentro.", "No <code>except TEMPORARIOS as erro:</code>, se for a última tentativa, use <code>raise</code> sozinho para subir o mesmo erro.", "Senão, registre com <code>log.warning</code>, chame <code>dormir(espera)</code> e faça <code>espera *= 2</code>. Erros fora de TEMPORARIOS sobem sozinhos, sem o except pegar."],
            exp="O parâmetro <code>dormir</code> deixa testar sem esperar de verdade: no teste, passamos uma função que só anota quanto teria esperado. Em produção, ela é o <code>time.sleep</code>. Bibliotecas como o <code>tenacity</code> fazem isso pronto."),
        erros([
            ("<code>except Exception: pass</code>", "Engolir o erro esconde o problema. Trate o que você espera e registre o resto."),
            ("Tentar de novo sem limite e sem espera.", "Sempre com limite de tentativas e espera crescente (de preferência com um pouco de aleatoriedade)."),
            ("Repetir pedidos que não podem ser repetidos (cobrar um cartão duas vezes).", "Só repita operações idempotentes, ou use uma chave de idempotência."),
            ("Gravar no log o prompt completo com dados do cliente ou a chave da API.", "Mascare dados pessoais e nunca registre segredos (veja a aula de LGPD)."),
            ("Usar <code>print</code> em produção.", "Use <code>logging</code>: tem nível, horário, origem e pode ir para arquivos e ferramentas de monitoramento."),
        ]),
        ponte("Observabilidade", "<p>Logs bem feitos são a primeira peça da observabilidade, que aparece logo adiante na Fase 6: com eles, você responde “o que aconteceu às 14h32 com o pedido do cliente X?” sem adivinhar.</p>"),
        quiz([
            ("Qual erro vale a pena tentar de novo?", ["401 · chave inválida", "Tempo esgotado (timeout)", "400 · pedido inválido"], 1, "Timeout, 429 e 5xx costumam ser temporários."),
            ("O que é backoff exponencial?", ["Esperar cada vez mais entre as tentativas (1 s, 2 s, 4 s...).", "Tentar sem parar.", "Desistir na primeira falha."], 0, "A espera cresce a cada falha."),
            ("Dentro de um <code>except</code>, qual comando registra a mensagem e o erro completo?", ["<code>print(erro)</code>", "<code>log.exception(\"mensagem\")</code>", "<code>pass</code>"], 1, "O log.exception inclui o rastreamento do erro."),
        ]),
    ],
    ["Erros temporários: espere e tente de novo, com limite. Permanentes: corrija.", "Backoff exponencial evita piorar o congestionamento.", "Use logging com níveis, nunca registre segredos nem dados pessoais."],
    "MLOps: versionamento de dados e modelos.")

# ---------------------------------------------------------------------------------------------
AULAS["Design de sistemas de ML e LLM (entrevistas)"] = aula(
    35,
    "Em entrevistas para engenheiro de IA, uma pergunta clássica é aberta: “Como você construiria um chatbot de atendimento para 10 mil usuários?”. Não existe resposta única. O que o entrevistador avalia é se você <b>organiza o problema</b>: entende os requisitos, escolhe métricas, desenha a arquitetura, faz contas de capacidade e custo e pensa em como manter o sistema funcionando.",
    ["seguir um roteiro de 6 passos para perguntas de design;", "estimar requisições por segundo e custo de um sistema com LLM;", "explicar trocas de decisão (custo × qualidade × latência)."],
    ["APIs de LLMs, RAG, avaliação de LLMs e custo e latência."],
    [
        chute("O entrevistador pergunta como construir um chatbot de atendimento. Qual é o melhor primeiro passo?", ["Dizer qual modelo usar.", "Fazer perguntas para entender os requisitos: quantos usuários, que tipo de pergunta, que erro é aceitável.", "Desenhar o banco de dados."], 1,
              ["Escolher o modelo antes de entender o problema é o erro mais comum.", "Isso! Esclarecer requisitos mostra maturidade e evita resolver o problema errado.", "Ainda é cedo para detalhes."],
              "Comece pelo problema, não pela tecnologia."),
        concreto("O projeto antes da obra", "<p>Ninguém começa uma casa comprando tijolo. Primeiro vem a conversa com o cliente (quantos quartos, orçamento, prazo), depois a planta, depois o cálculo da estrutura e da quantidade de material. Design de sistemas é a planta e o cálculo do software, antes de escrever a primeira linha.</p>"),
        ver("a ordem em que o candidato organiza a resposta"),
        passos("Os 6 passos de uma resposta de design", [
            ("1. Requisitos", "Quem usa, quantos, o que precisa responder, latência aceitável, o que não pode acontecer."),
            ("2. Métricas", "De negócio (casos resolvidos sem humano) e técnicas (taxa de acerto nos testes, latência, custo por conversa)."),
            ("3. Dados", "De onde vêm (FAQ, manuais, histórico), como limpar, LGPD."),
            ("4. Solução base e arquitetura", "Comece simples: LLM + RAG nos documentos da empresa; depois, ferramentas e agentes se precisar."),
            ("5. Avaliação", "Conjunto de perguntas com respostas esperadas (evals), testes antes de publicar, avaliação humana por amostragem."),
            ("6. Produção", "Monitoramento, logs, custo, plano para quando o modelo falhar (passar para um humano)."),
        ], fim="Fale em voz alta as trocas: “posso usar um modelo menor e mais barato e só chamar o maior quando a pergunta for difícil”."),
        tabela("Peças típicas de um sistema com LLM", ["Peça", "Para quê"], [
            ["API (FastAPI)", "Recebe a pergunta, autentica, aplica limites de uso."],
            ["RAG (busca + banco vetorial)", "Traz os trechos certos dos documentos para o modelo."],
            ["LLM", "Gera a resposta; pode ter um modelo pequeno e um grande."],
            ["Cache", "Perguntas repetidas não pagam o modelo de novo."],
            ["Fila", "Tarefas demoradas rodam em segundo plano."],
            ["Logs e métricas", "Saber o que acontece, quanto custa e onde falha."],
            ["Avaliação contínua", "Pegar quando a qualidade cai."],
        ]),
        cod("A conta de padaria do entrevistador", "Estimativas rápidas são parte da resposta. Complete <code>estimar</code>, que recebe usuários por dia, mensagens por usuário, tokens de entrada e de saída por mensagem e o preço (em dólares) por <b>1 milhão</b> de tokens de entrada e de saída. Devolva um dicionário com: <code>msgs_dia</code>; <code>rps_pico</code>, as requisições por segundo no pico, considerando o pico como <b>3 vezes a média</b> do dia; <code>custo_dia</code>; e <code>custo_mes</code>, com 30 dias. Arredonde os valores em dinheiro para 2 casas.",
            '''
def estimar(usuarios_dia, msgs_por_usuario, tokens_in, tokens_out, preco_in_milhao, preco_out_milhao):
    return {"msgs_dia": 0, "rps_pico": 0, "custo_dia": 0, "custo_mes": 0}

r = estimar(10_000, 5, 1_500, 300, 0.15, 0.60)
print(r)
''',
            [("Mensagens por dia", "assert r['msgs_dia'] == 50_000, r"),
             ("Pico de requisições por segundo", "assert round(r['rps_pico'], 2) == 1.74, r"),
             ("Custo por dia", "assert r['custo_dia'] == 20.25, r"),
             ("Custo por mês", "assert r['custo_mes'] == 607.5, r"),
             ("Funciona com outros números", "s = estimar(1_000, 2, 1_000, 1_000, 1.0, 1.0)\nassert s['msgs_dia'] == 2000 and s['custo_dia'] == 4.0 and s['custo_mes'] == 120.0, s")],
            '''
def estimar(usuarios_dia, msgs_por_usuario, tokens_in, tokens_out, preco_in_milhao, preco_out_milhao):
    msgs_dia = usuarios_dia * msgs_por_usuario
    rps_pico = msgs_dia / 86_400 * 3
    custo_msg = tokens_in / 1_000_000 * preco_in_milhao + tokens_out / 1_000_000 * preco_out_milhao
    custo_dia = round(msgs_dia * custo_msg, 2)
    return {"msgs_dia": msgs_dia, "rps_pico": rps_pico, "custo_dia": custo_dia, "custo_mes": round(custo_dia * 30, 2)}

r = estimar(10_000, 5, 1_500, 300, 0.15, 0.60)
print(r)
''', ["Mensagens por dia = usuários × mensagens por usuário.", "Um dia tem 86.400 segundos: a média é msgs_dia / 86_400; o pico é 3 vezes isso.", "Custo de uma mensagem = tokens_in / 1.000.000 × preço de entrada + tokens_out / 1.000.000 × preço de saída."],
            exp="50 mil mensagens por dia parecem muito, mas dão menos de 2 requisições por segundo no pico. Contas assim mostram ao entrevistador que você dimensiona antes de complicar a arquitetura."),
        pense("Treine a resposta em voz alta", "Use os 6 passos para responder, em 3 minutos: “Como você faria um assistente que responde dúvidas sobre os manuais de uma empresa de equipamentos?”",
              "<p>Requisitos (técnicos de campo, celular, respostas em segundos, citar a página do manual); métricas (taxa de respostas corretas num conjunto de 100 perguntas reais, latência, custo por pergunta); dados (PDFs dos manuais, divididos em trechos); arquitetura (FastAPI + RAG com banco vetorial + LLM, cache para perguntas repetidas); avaliação (evals antes de cada versão); produção (logs, custo diário, botão “não ajudou” que alimenta melhorias). Grave-se respondendo: ouvir a própria resposta é o melhor treino.</p>"),
        erros([
            ("Começar pela tecnologia da moda.", "Comece pelos requisitos e pela solução mais simples que resolve."),
            ("Esquecer de medir.", "Sem métricas e evals, você não sabe se a mudança melhorou ou piorou."),
            ("Ignorar custo e latência.", "Faça a conta: ela muda decisões (modelo menor, cache, respostas mais curtas)."),
            ("Não ter plano para falhas.", "Sempre diga o que acontece quando o modelo erra ou cai: passar para um humano, resposta padrão, nova tentativa."),
        ]),
        ponte("Também em inglês", "<p>Muitas dessas entrevistas são em inglês, como o vídeo desta aula. Treine os 6 passos em inglês também: <i>requirements, metrics, data, baseline and architecture, evaluation, deployment and monitoring</i>. O Módulo 7 de Inglês trabalha exatamente essas situações.</p>"),
        quiz([
            ("Qual é o primeiro passo numa pergunta de design de sistemas?", ["Escolher o modelo.", "Esclarecer os requisitos.", "Escrever o código."], 1, "Problema antes da tecnologia."),
            ("Para que serve um cache num sistema com LLM?", ["Evitar pagar e esperar o modelo de novo por perguntas repetidas.", "Treinar o modelo.", "Guardar senhas."], 0, "Economiza custo e latência."),
            ("50 mil mensagens por dia, com pico de 3 vezes a média, dão cerca de quantas requisições por segundo no pico?", ["Menos de 2.", "Cerca de 500.", "Cerca de 50 mil."], 0, "50.000 / 86.400 × 3 ≈ 1,7."),
        ]),
    ],
    ["Siga os 6 passos: requisitos, métricas, dados, arquitetura, avaliação, produção.", "Faça contas de capacidade e custo antes de complicar a arquitetura.", "Fale das trocas de decisão e do plano para falhas."],
    "Carreira: currículo e entrevistas técnicas.",
    livro=("MADEML", "Made With ML, do problema ao sistema em produção", "Que etapas o curso percorre antes de treinar qualquer modelo?"))
