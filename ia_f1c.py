# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 1 (parte C): recursos intermediários, bibliotecas úteis e prática."""
from lesson_factory import *

AULAS = {}

AULAS["Geradores e iteradores"] = aula(
    30,
    "Um dataset de 200 GB não cabe na memória. A saída é não carregar tudo: produzir <b>um item por vez</b>, só quando alguém pedir. É isso que um gerador faz, e é assim que modelos são treinados em dados gigantes.",
    ["criar geradores com <code>yield</code>;", "entender a avaliação preguiçosa;", "usar expressões geradoras."],
    ["Funções, laços e list comprehension."],
    [
        chute("O que esse código imprime?", ["1 2 3", "1", "Nada"], 1,
              ["Cada <code>next</code> entrega só <b>um</b> valor; aqui há um <code>next</code> só.", "Isso! O gerador roda até o primeiro <code>yield</code>, entrega o 1 e <b>pausa</b>.", "O <code>next</code> faz a função rodar até o primeiro <code>yield</code>."],
              "<code>yield</code> entrega um valor e congela a função até o próximo pedido.",
              cod='def contar():\n    yield 1\n    yield 2\n    yield 3\n\ng = contar()\nprint(next(g))'),
        concreto("O bebedouro e o galão", "<p>Uma <b>lista</b> é o galão cheio: toda a água já está ali, ocupando espaço. Um <b>gerador</b> é o bebedouro: a água só sai quando você aperta, um copo por vez.</p>"),
        crianca("<p><code>return</code> é entregar a pizza inteira e ir embora. <code>yield</code> é o garçom do rodízio: entrega <b>uma fatia</b>, espera você pedir a próxima e lembra exatamente onde parou.</p>"),
        nota("Produzir sob demanda", [
            ("<code>yield valor</code>", "entregar e pausar", "Transforma a função num gerador."),
            ("<code>next(g)</code>", "próximo", "Pede o próximo valor. Quando acaba, dispara <code>StopIteration</code>."),
            ("<code>for x in g:</code>", "percorrer", "O <code>for</code> chama <code>next</code> sozinho e para no fim."),
            ("<code>(x * 2 for x in v)</code>", "expressão geradora", "Como a comprehension, mas com parênteses: não cria a lista na memória."),
        ]),
        passos("Lendo um arquivo enorme", [
            ("<code>def linhas(caminho):</code> abre o arquivo e faz <code>yield linha.strip()</code> dentro do <code>for</code>.", "Só uma linha fica na memória por vez."),
            ("<code>for l in linhas(\"dados.txt\"):</code>", "O arquivo é lido conforme o laço avança."),
            ("Interrompeu no meio com <code>break</code>?", "O resto do arquivo nem chega a ser lido."),
        ], fim="Um gerador só pode ser percorrido <b>uma vez</b>. Para repetir, crie outro."),
        cod("Lotes de dados", "Complete o gerador <code>lotes</code>: ele recebe uma lista e um tamanho e entrega pedaços daquele tamanho (o último pode ser menor). É assim que um DataLoader alimenta o treino.",
            '''
def lotes(dados, tamanho):
    yield dados

for lote in lotes([1, 2, 3, 4, 5, 6, 7], 3):
    print(lote)
''',
            [("Divide em lotes de 3", "assert list(lotes([1, 2, 3, 4, 5, 6, 7], 3)) == [[1, 2, 3], [4, 5, 6], [7]], f'deu {list(lotes([1, 2, 3, 4, 5, 6, 7], 3))}'"),
             ("É um gerador", "import types\nassert isinstance(lotes([1], 1), types.GeneratorType), 'use yield'"), ("Lista vazia não entrega nada", "assert list(lotes([], 4)) == []")],
            '''
def lotes(dados, tamanho):
    for i in range(0, len(dados), tamanho):
        yield dados[i:i + tamanho]

for lote in lotes([1, 2, 3, 4, 5, 6, 7], 3):
    print(lote)
''', ["<code>range(0, len(dados), tamanho)</code> dá o início de cada lote.", "<code>dados[i:i + tamanho]</code> é o pedaço."]),
        erros([
            ("Percorrer o mesmo gerador duas vezes.", "Na segunda vez ele está esgotado e não entrega nada."),
            ("<code>len(gerador)</code> ou <code>gerador[0]</code>.", "Geradores não têm tamanho nem índice. Converta com <code>list()</code> se precisar (e couber na memória)."),
            ("Usar gerador para poucos dados que serão lidos várias vezes.", "Aí a lista é mais simples."),
        ]),
        ponte("Streaming de tokens",
              "<p>Quando um chatbot escreve a resposta aos poucos, é um gerador: a API entrega <b>um token por vez</b> com <code>yield</code>. E no treino, o <code>DataLoader</code> do PyTorch entrega um lote por vez, sem nunca carregar o dataset inteiro.</p>"),
        quiz([
            ("O que <code>yield</code> faz?", ["Encerra a função.", "Entrega um valor e pausa a função.", "Imprime um valor."], 1, "A função continua de onde parou no próximo pedido."),
            ("Qual a vantagem de um gerador sobre uma lista?", ["É sempre mais rápido.", "Não guarda todos os valores na memória.", "Permite usar índices."], 1, "Produz sob demanda."),
            ("O que acontece ao percorrer um gerador pela segunda vez?", ["Recomeça do início.", "Não entrega nada.", "Dá erro de sintaxe."], 1, "Ele já foi consumido."),
        ]),
    ],
    ["<code>yield</code> transforma a função num gerador que produz valores sob demanda.", "Geradores economizam memória e só podem ser percorridos uma vez.", "<code>(expr for x in v)</code> é a versão preguiçosa da comprehension."],
    "Decoradores: acrescentar comportamento a funções.",
    livro=("PYDOC:classes", "Seções 9.8 a 9.10 (iteradores, geradores e expressões geradoras)", "Como o tutorial reescreve um iterador como gerador?"))

AULAS["Decoradores (noção)"] = aula(
    30,
    "Aquele <code>@</code> em cima de uma função, que aparece em FastAPI, pytest e PyTorch, parece mágica. Não é: é só uma função que <b>embrulha</b> outra para acrescentar algo antes e depois.",
    ["entender que funções podem receber e devolver funções;", "ler e escrever um decorador simples;", "reconhecer decoradores comuns."],
    ["Funções e lambda."],
    [
        chute("O que esse código imprime?", ["oi", "antes, oi, depois (uma por linha)", "antes e depois"], 1,
              ["O decorador acrescenta coisas em volta.", "Isso! <code>@avisar</code> troca <code>ola</code> por uma versão embrulhada que imprime antes e depois.", "A função original também roda, no meio."],
              "<code>@avisar</code> em cima de <code>def ola</code> é o mesmo que <code>ola = avisar(ola)</code>.",
              cod='def avisar(f):\n    def nova():\n        print("antes")\n        f()\n        print("depois")\n    return nova\n\n@avisar\ndef ola():\n    print("oi")\n\nola()'),
        concreto("Papel de presente", "<p>O presente continua o mesmo, mas agora vem <b>embrulhado</b>: tem laço, tem cartão. Um decorador embrulha a função: o que ela faz não muda, mas algo acontece antes e depois.</p>"),
        nota("Lendo um decorador", [
            ("<code>@nome</code>", "arroba nome", "Aplica o decorador à função definida logo abaixo."),
            ("<code>def decorador(f):</code>", "recebe uma função", "<code>f</code> é a função original."),
            ("<code>def nova(*args, **kwargs):</code>", "a embrulhada", "Aceita qualquer argumento e repassa para <code>f</code>."),
            ("<code>return nova</code>", "devolve a embrulhada", "É ela que passa a ser chamada."),
        ]),
        passos("Um cronômetro", [
            ("<code>inicio = time.time()</code>", "Antes de chamar a função original."),
            ("<code>resultado = f(*args, **kwargs)</code>", "Chama a original e guarda o que ela devolveu."),
            ("<code>print(time.time() - inicio)</code>", "Depois: mostra quanto tempo levou."),
            ("<code>return resultado</code>", "Quem chamou nem percebe o embrulho."),
        ], fim="Com isso, qualquer função ganha medição de tempo só com uma linha: <code>@cronometrar</code>."),
        cod("Contador de chamadas", "Complete o decorador <code>contar</code>: a cada chamada da função decorada, some 1 em <code>nova.chamadas</code> e devolva o resultado da função original.",
            '''
def contar(f):
    def nova(*args, **kwargs):
        return f(*args, **kwargs)
    nova.chamadas = 0
    return nova

@contar
def dobro(x):
    return x * 2

dobro(1); dobro(2); dobro(3)
print(dobro.chamadas)
''',
            [("Conta 3 chamadas", "assert saida.strip() == '3', f'saiu {saida.strip()!r}'"), ("O resultado continua certo", "assert dobro(5) == 10")],
            '''
def contar(f):
    def nova(*args, **kwargs):
        nova.chamadas += 1
        return f(*args, **kwargs)
    nova.chamadas = 0
    return nova

@contar
def dobro(x):
    return x * 2

dobro(1); dobro(2); dobro(3)
print(dobro.chamadas)
''', ["Dentro de <code>nova</code>, antes do <code>return</code>: <code>nova.chamadas += 1</code>."]),
        erros([
            ("Esquecer o <code>return</code> dentro da função embrulhada.", "A função decorada passa a devolver <code>None</code>."),
            ("Escrever <code>@decorador()</code> com parênteses sem necessidade.", "Só use parênteses se o decorador recebe argumentos, como <code>@app.get(\"/\")</code>."),
            ("Criar decoradores para tudo.", "Use os prontos; escreva o seu quando o mesmo embrulho se repetir em várias funções."),
        ]),
        ponte("Decoradores que você vai usar",
              "<p><code>@app.get(\"/prever\")</code> no FastAPI transforma uma função num endereço da API. <code>@torch.no_grad()</code> desliga o cálculo de gradientes na avaliação. <code>@pytest.fixture</code> prepara dados para os testes. <code>@tool</code> registra uma função como ferramenta de um agente. Em todos, a ideia é a mesma: embrulhar.</p>"),
        quiz([
            ("<code>@d</code> em cima de <code>def f</code> equivale a:", ["<code>f = d(f)</code>", "<code>d = f(d)</code>", "<code>f()</code>"], 0, "O decorador recebe <code>f</code> e devolve a nova versão."),
            ("O que um decorador recebe como argumento?", ["Um número.", "Uma função.", "Uma classe sempre."], 1, "A função que será embrulhada."),
            ("Para que serve <code>*args, **kwargs</code> na função embrulhada?", ["Para aceitar e repassar qualquer argumento.", "Para deixar a função mais rápida.", "Para criar listas."], 0, "Assim o decorador serve para qualquer função."),
        ]),
    ],
    ["Decorador é uma função que recebe outra e devolve uma versão embrulhada.", "<code>@d</code> é açúcar para <code>f = d(f)</code>.", "Aparecem em FastAPI, pytest, PyTorch e agentes."],
    "datetime: datas e horas sem dor de cabeça.",
    livro=("PYDOC:controlflow", "Seção 4.9 (mais sobre definição de funções), partes sobre *args e **kwargs", "Como o tutorial explica argumentos arbitrários?"))

AULAS["datetime"] = aula(
    30,
    "“Quantos dias faltam para a entrega?” “Que dia da semana vendeu mais?” Datas parecem simples até você tentar somar 30 dias a 31 de janeiro. O módulo <code>datetime</code> faz essa conta por você.",
    ["criar datas e horários;", "converter texto em data e data em texto;", "somar e subtrair períodos com <code>timedelta</code>."],
    ["Módulos e f-strings."],
    [
        chute("O que esse código imprime?", ["31", "30", "Dá erro"], 0,
              ["Isso! Subtrair duas datas dá um <code>timedelta</code>; <code>.days</code> é o número de dias. Janeiro tem 31.", "Janeiro tem 31 dias.", "Subtrair datas é permitido e muito útil."],
              "Datas se subtraem; o resultado é uma <b>duração</b>.",
              cod='from datetime import date\nprint((date(2025, 2, 1) - date(2025, 1, 1)).days)'),
        concreto("Calendário e régua", "<p>Uma <b>data</b> é um ponto no calendário. Um <b>timedelta</b> é uma régua de tempo: “7 dias”, “3 horas”. Ponto mais régua dá outro ponto; ponto menos ponto dá uma régua.</p>"),
        nota("As quatro peças", [
            ("<code>date(2025, 3, 15)</code>", "data", "Ano, mês, dia. <code>date.today()</code> é hoje."),
            ("<code>datetime(2025, 3, 15, 14, 30)</code>", "data e hora", "<code>datetime.now()</code> é agora."),
            ("<code>timedelta(days=7)</code>", "duração", "Soma e subtrai de datas."),
            ("<code>d.strftime(\"%d/%m/%Y\")</code>", "data para texto", "<code>%d</code> dia, <code>%m</code> mês, <code>%Y</code> ano, <code>%H:%M</code> hora e minuto."),
            ("<code>datetime.strptime(txt, formato)</code>", "texto para data", "O caminho inverso: lê o texto seguindo o formato."),
        ]),
        passos("Vencimento de um boleto", [
            ("<code>emissao = date(2025, 1, 20)</code>", "Ponto de partida."),
            ("<code>venc = emissao + timedelta(days=30)</code>", "Soma a duração: 19 de fevereiro."),
            ("<code>venc.strftime(\"%d/%m/%Y\")</code>", "Texto no formato brasileiro: 19/02/2025."),
            ("<code>venc.weekday()</code>", "0 é segunda, 6 é domingo."),
        ]),
        cod("Dias até o prazo", "Complete a função: recebe duas datas em texto no formato <code>dd/mm/aaaa</code> e devolve quantos dias há da primeira até a segunda.",
            '''
from datetime import datetime

def dias_entre(inicio, fim):
    return 0

print(dias_entre("01/03/2025", "15/03/2025"))
''',
            [("14 dias", "assert dias_entre('01/03/2025', '15/03/2025') == 14"), ("Atravessa o mês", "assert dias_entre('28/02/2025', '02/03/2025') == 2"), ("Mesmo dia", "assert dias_entre('10/10/2025', '10/10/2025') == 0")],
            '''
from datetime import datetime

def dias_entre(inicio, fim):
    f = "%d/%m/%Y"
    return (datetime.strptime(fim, f) - datetime.strptime(inicio, f)).days

print(dias_entre("01/03/2025", "15/03/2025"))
''', ["<code>datetime.strptime(texto, \"%d/%m/%Y\")</code> converte.", "Subtraia e pegue <code>.days</code>."]),
        erros([
            ("Confundir <code>strftime</code> (formatar) com <code>strptime</code> (interpretar).", "<b>f</b> de <i>format</i>: data → texto. <b>p</b> de <i>parse</i>: texto → data."),
            ("<code>%m</code> e <code>%M</code>.", "Minúsculo é mês; maiúsculo é minuto."),
            ("Ignorar fuso horário em sistemas com usuários de vários lugares.", "Guarde tudo em UTC e converta só na hora de mostrar."),
        ]),
        ponte("Datas em dados",
              "<p>Séries temporais (vendas, sensores, preços) dependem de datas bem tratadas. Extrair dia da semana, mês e feriado de uma data é uma das formas mais rentáveis de <b>engenharia de atributos</b>. E todo log de treino e todo registro de uso de API carrega um carimbo de tempo.</p>"),
        quiz([
            ("O que resulta de subtrair duas datas?", ["Um número inteiro.", "Um <code>timedelta</code>.", "Um texto."], 1, "Uma duração, com <code>.days</code>."),
            ("Qual formato produz <b>25/12/2025</b>?", ["<code>%Y-%m-%d</code>", "<code>%d/%m/%Y</code>", "<code>%m/%d/%y</code>"], 1, "Dia, mês e ano com 4 dígitos."),
            ("Como obter a data de daqui a 10 dias?", ["<code>date.today() + 10</code>", "<code>date.today() + timedelta(days=10)</code>", "<code>date.today().add(10)</code>"], 1, "Soma-se uma duração."),
        ]),
    ],
    ["<code>date</code> e <code>datetime</code> são pontos no tempo; <code>timedelta</code> é duração.", "<code>strptime</code> lê texto; <code>strftime</code> gera texto.", "Datas se somam e se subtraem."],
    "os e pathlib: caminhos de arquivos que funcionam em qualquer sistema.",
    livro=("ATBS:17", "Capítulo 17, “Keeping Time, Scheduling Tasks”", "Que exemplo de cronômetro o livro constrói?"))

AULAS["os e pathlib"] = aula(
    30,
    "<code>dados\\treino.csv</code> funciona no Windows e quebra no Linux do servidor. Caminhos montados na mão são uma fonte clássica de “na minha máquina funcionava”. O <code>pathlib</code> resolve isso.",
    ["montar caminhos com <code>Path</code>;", "listar, criar e conferir arquivos e pastas;", "ler variáveis de ambiente com <code>os.environ</code>."],
    ["Arquivos e módulos."],
    [
        chute("O que esse código imprime?", ["relatorio", ".csv", "relatorio.csv"], 1,
              ["Isso é o <code>.stem</code>: o nome sem a extensão.", "Isso! <code>.suffix</code> é a extensão, com o ponto.", "Isso é o <code>.name</code>."],
              "<code>.name</code>, <code>.stem</code>, <code>.suffix</code> e <code>.parent</code> desmontam um caminho.",
              cod='from pathlib import Path\np = Path("dados") / "relatorio.csv"\nprint(p.suffix)'),
        concreto("O endereço", "<p>Um caminho é um endereço: país, cidade, rua, número. O <code>Path</code> entende as partes do endereço e monta o texto com a barra certa para cada sistema.</p>"),
        nota("Path no dia a dia", [
            ("<code>Path(\"dados\") / \"a.csv\"</code>", "juntar", "A barra <code>/</code> une partes do caminho em qualquer sistema."),
            ("<code>p.exists()</code>", "existe?", "Também <code>p.is_file()</code> e <code>p.is_dir()</code>."),
            ("<code>p.mkdir(parents=True, exist_ok=True)</code>", "criar pasta", "Cria as pastas que faltarem e não reclama se já existir."),
            ("<code>pasta.glob(\"*.csv\")</code>", "procurar", "Todos os arquivos que casam com o padrão."),
            ("<code>p.read_text(encoding=\"utf-8\")</code>", "ler", "Lê o arquivo inteiro. Há também <code>write_text</code>."),
            ("<code>os.environ.get(\"CHAVE\")</code>", "variável de ambiente", "Onde ficam segredos como chaves de API."),
        ]),
        passos("Organizando resultados de experimentos", [
            ("<code>saida = Path(\"resultados\") / \"exp1\"</code>", "Monta o caminho sem se preocupar com a barra."),
            ("<code>saida.mkdir(parents=True, exist_ok=True)</code>", "Garante que a pasta existe."),
            ("<code>(saida / \"metricas.txt\").write_text(\"acc=0.9\")</code>", "Grava o arquivo dentro dela."),
            ("<code>list(Path(\"resultados\").glob(\"*/metricas.txt\"))</code>", "Acha as métricas de todos os experimentos."),
        ]),
        cod("Inventário de arquivos", "A função recebe uma lista de nomes de arquivo e devolve um dicionário com a contagem por extensão (sem o ponto, em minúsculas). Use <code>Path</code>.",
            '''
from pathlib import Path

def por_extensao(nomes):
    return {}

print(por_extensao(["a.csv", "b.CSV", "notas.txt", "fotos/gato.png"]))
''',
            [("Conta por extensão", "assert por_extensao(['a.csv', 'b.CSV', 'notas.txt', 'fotos/gato.png']) == {'csv': 2, 'txt': 1, 'png': 1}, f'deu {por_extensao([\"a.csv\", \"b.CSV\", \"notas.txt\", \"fotos/gato.png\"])}'"), ("Lista vazia", "assert por_extensao([]) == {}")],
            '''
from pathlib import Path

def por_extensao(nomes):
    cont = {}
    for n in nomes:
        ext = Path(n).suffix.lower().lstrip(".")
        cont[ext] = cont.get(ext, 0) + 1
    return cont

print(por_extensao(["a.csv", "b.CSV", "notas.txt", "fotos/gato.png"]))
''', ["<code>Path(n).suffix</code> dá <code>\".csv\"</code>; tire o ponto com <code>.lstrip(\".\")</code> e use <code>.lower()</code>."]),
        erros([
            ("Montar caminhos com <code>+</code> e barras escritas à mão.", "Use <code>Path(...) / \"parte\"</code>."),
            ("Caminhos absolutos como <code>C:\\Users\\Fulano\\...</code> no código.", "Só funcionam na sua máquina. Use caminhos relativos ao projeto."),
            ("Chave de API escrita no código.", "Leia de <code>os.environ</code> e mantenha o arquivo <code>.env</code> fora do Git."),
        ]),
        ponte("Pastas de um projeto de IA",
              "<p><code>dados/brutos</code>, <code>dados/processados</code>, <code>modelos</code>, <code>notebooks</code>: todo projeto de ML tem essa organização, e o código navega por ela com <code>Path</code>. E a chave da API do seu LLM vem sempre de <code>os.environ[\"..._API_KEY\"]</code>.</p>"),
        quiz([
            ("Como juntar <code>dados</code> e <code>a.csv</code> com pathlib?", ["<code>Path(\"dados\") + \"a.csv\"</code>", "<code>Path(\"dados\") / \"a.csv\"</code>", "<code>Path(\"dados\", + \"a.csv\")</code>"], 1, "A barra é o operador de junção."),
            ("O que <code>p.stem</code> devolve para <code>modelo.pt</code>?", ["modelo", ".pt", "modelo.pt"], 0, "O nome sem a extensão."),
            ("Onde guardar segredos como chaves de API?", ["Em variáveis de ambiente.", "Em um comentário no código.", "No nome do arquivo."], 0, "E fora do controle de versão."),
        ]),
    ],
    ["<code>Path</code> monta e desmonta caminhos de forma portátil.", "<code>exists</code>, <code>mkdir</code> e <code>glob</code> resolvem o dia a dia.", "Segredos vêm de <code>os.environ</code>."],
    "json e csv: os dois formatos de dados mais comuns.",
    livro=("ATBS:10", "Capítulo 10, “Organizing Files”", "Como o livro percorre uma árvore de pastas?"))

AULAS["json e csv"] = aula(
    35,
    "Quase todo dado do mundo chega em um de dois formatos: <b>CSV</b>, a planilha em texto, e <b>JSON</b>, a árvore de chaves e valores. Dominar os dois é pré-requisito para qualquer trabalho com dados.",
    ["ler e gravar CSV com o módulo <code>csv</code>;", "converter JSON em objetos Python e vice-versa;", "escolher o formato certo para cada caso."],
    ["Arquivos e dicionários."],
    [
        chute("O que esse código imprime?", ["&lt;class 'dict'&gt;", "&lt;class 'str'&gt;", "&lt;class 'list'&gt;"], 0,
              ["Isso! <code>json.loads</code> lê o texto e devolve o objeto Python correspondente: aqui, um dicionário.", "O texto de entrada é <code>str</code>, mas a saída já é o objeto.", "Seria lista se o JSON começasse com colchete."],
              "<code>loads</code> = <i>load string</i>: texto → objeto. <code>dumps</code> faz o caminho de volta.",
              cod='import json\nd = json.loads(\'{"nome": "Ana", "idade": 30}\')\nprint(type(d))'),
        concreto("Planilha e ficha", "<p><b>CSV</b> é uma planilha: linhas e colunas, todas as linhas com os mesmos campos. <b>JSON</b> é uma ficha com gavetas dentro de gavetas: um cliente tem endereço, que tem cidade; e tem uma lista de pedidos.</p>"),
        nota("Os comandos", [
            ("<code>json.loads(texto)</code> / <code>json.dumps(obj)</code>", "texto ↔ objeto", "<code>dumps(obj, ensure_ascii=False, indent=2)</code> mantém acentos e deixa legível."),
            ("<code>json.load(f)</code> / <code>json.dump(obj, f)</code>", "arquivo ↔ objeto", "Sem o <b>s</b>: trabalham direto com o arquivo aberto."),
            ("<code>csv.DictReader(f)</code>", "ler CSV", "Cada linha vira um dicionário com os nomes das colunas."),
            ("<code>csv.DictWriter(f, fieldnames=[...])</code>", "gravar CSV", "<code>writeheader()</code> e depois <code>writerows(lista)</code>."),
        ]),
        passos("De CSV para JSON", [
            ("Abra o CSV e crie <code>leitor = csv.DictReader(f)</code>.", "A primeira linha vira os nomes das colunas."),
            ("<code>linhas = list(leitor)</code>", "Uma lista de dicionários."),
            ("Converta os números: <code>int(l[\"idade\"])</code>.", "No CSV <b>tudo é texto</b>."),
            ("<code>json.dumps(linhas, ensure_ascii=False)</code>", "Pronto para enviar a uma API."),
        ]),
        cod("Total de vendas", "O texto <code>dados</code> é um CSV. Leia com <code>csv.DictReader</code> e imprima o total vendido (quantidade × preço de cada linha), com duas casas.",
            '''
import csv, io

dados = """produto,quantidade,preco
caneta,10,2.50
caderno,3,18.00
mochila,1,120.00
"""

leitor = csv.DictReader(io.StringIO(dados))
total = 0

print(f"{total:.2f}")
''',
            [("Total 199.00", "assert saida.strip() == '199.00', f'saiu {saida.strip()!r}'")],
            '''
import csv, io

dados = """produto,quantidade,preco
caneta,10,2.50
caderno,3,18.00
mochila,1,120.00
"""

leitor = csv.DictReader(io.StringIO(dados))
total = 0
for linha in leitor:
    total += int(linha["quantidade"]) * float(linha["preco"])

print(f"{total:.2f}")
''', ["Cada <code>linha</code> é um dicionário: <code>linha[\"quantidade\"]</code>.", "Converta: <code>int(...)</code> e <code>float(...)</code>."]),
        cod("Configuração de treino", "Monte o dicionário de configuração e imprima-o como JSON com <code>json.dumps(config, sort_keys=True)</code>. Ele deve ter <code>modelo</code> = \"mini\", <code>epocas</code> = 3 e <code>taxas</code> = [0.1, 0.01].",
            '''
import json

config = {}

print(json.dumps(config, sort_keys=True))
''',
            [("JSON correto", "import json as _j\nassert _j.loads(saida) == {'modelo': 'mini', 'epocas': 3, 'taxas': [0.1, 0.01]}, f'saiu {saida.strip()}'")],
            '''
import json

config = {"modelo": "mini", "epocas": 3, "taxas": [0.1, 0.01]}

print(json.dumps(config, sort_keys=True))
''', ["Texto entre aspas, inteiro sem aspas e a lista entre colchetes."], rot="Mão no código · nível 2"),
        erros([
            ("Fazer contas com valores lidos de CSV sem converter.", "Tudo chega como texto: <code>\"10\" * 2</code> dá <code>\"1010\"</code>."),
            ("JSON com aspas simples ou vírgula sobrando.", "JSON exige aspas duplas e não aceita vírgula depois do último item."),
            ("Abrir CSV no Windows e ver linhas em branco entre os registros.", "Abra o arquivo com <code>newline=\"\"</code> ao gravar."),
        ]),
        ponte("Os formatos dos datasets",
              "<p>Datasets tabulares chegam em CSV; anotações, configurações e respostas de API, em JSON. Para treinar LLMs o padrão é o <b>JSONL</b>: um objeto JSON por linha, que pode ser lido aos poucos com um gerador. Na Fase 2, o Pandas lerá tudo isso com uma linha.</p>"),
        quiz([
            ("Qual função converte um texto JSON em dicionário?", ["<code>json.dumps</code>", "<code>json.loads</code>", "<code>json.read</code>"], 1, "<i>load string</i>."),
            ("Qual o tipo dos valores lidos por <code>csv.DictReader</code>?", ["Sempre <code>str</code>.", "O tipo original.", "Sempre <code>float</code>."], 0, "CSV não guarda tipos."),
            ("Quando o JSON é melhor que o CSV?", ["Para dados aninhados, com listas dentro de registros.", "Para tabelas simples e enormes.", "Nunca."], 0, "CSV é plano; JSON é uma árvore."),
        ]),
    ],
    ["CSV é tabela em texto; JSON é estrutura aninhada.", "<code>loads</code>/<code>dumps</code> para texto; <code>load</code>/<code>dump</code> para arquivo.", "No CSV tudo é texto: converta os números."],
    "Expressões regulares: encontrar padrões em texto.",
    livro=("ATBS:16", "Capítulo 16, “Working with CSV Files and JSON Data”", "Que projeto com JSON de previsão do tempo o livro monta?"))

AULAS["Expressões regulares (re)"] = aula(
    35,
    "Achar todos os e-mails num texto de 500 páginas. Extrair os valores em reais de mil notas fiscais. Com <code>if</code> e <code>split</code> seriam dezenas de linhas; com uma expressão regular, uma.",
    ["escrever padrões com <code>\\d</code>, <code>\\w</code>, <code>+</code> e <code>*</code>;", "usar <code>re.findall</code>, <code>re.search</code> e <code>re.sub</code>;", "capturar partes com parênteses."],
    ["Strings e listas."],
    [
        chute("O que esse código imprime?", ["['2', '0', '2', '5']", "['2025', '10']", "['2025']"], 1,
              ["Seria assim com <code>\\d</code> sem o <code>+</code>.", "Isso! <code>\\d+</code> pega <b>sequências</b> de um ou mais dígitos.", "Há dois grupos de dígitos no texto."],
              "<code>\\d</code> é “um dígito”; <code>+</code> é “um ou mais do anterior”.",
              cod='import re\nprint(re.findall(r"\\d+", "Em 2025 foram 10 aulas"))'),
        concreto("O molde vazado", "<p>Uma regex é um <b>molde vazado</b> que você desliza sobre o texto: onde o texto encaixa no molde, é um resultado. O molde <code>\\d\\d/\\d\\d</code> encaixa em “25/12” e não em “ab/cd”.</p>"),
        crianca("<p>É o jogo de <b>“ache tudo que tem este formato”</b>: três números, um traço, quatro números. Você descreve o <b>formato</b>, não o conteúdo.</p>"),
        nota("O vocabulário mínimo", [
            ("<code>\\d</code> · <code>\\w</code> · <code>\\s</code>", "dígito · letra/dígito/_ · espaço", "As versões maiúsculas negam: <code>\\D</code> é “não dígito”."),
            ("<code>.</code>", "ponto", "Qualquer caractere."),
            ("<code>+</code> · <code>*</code> · <code>?</code> · <code>{3}</code>", "quantificadores", "Um ou mais · zero ou mais · opcional · exatamente 3."),
            ("<code>[abc]</code> · <code>[a-z]</code>", "conjunto", "Um caractere dentre os listados."),
            ("<code>( )</code>", "grupo", "Captura só aquele pedaço do encaixe."),
            ("<code>^</code> · <code>$</code>", "início · fim", "Ancoram o padrão nas pontas."),
        ]),
        passos("Extraindo datas", [
            ("Padrão: <code>r\"\\d{2}/\\d{2}/\\d{4}\"</code>", "Dois dígitos, barra, dois dígitos, barra, quatro dígitos."),
            ("<code>re.findall(padrao, texto)</code>", "Devolve a lista de todas as datas."),
            ("Com grupos: <code>r\"(\\d{2})/(\\d{2})/(\\d{4})\"</code>", "Cada resultado vira uma tupla (dia, mês, ano)."),
            ("<code>re.sub(padrao, \"[DATA]\", texto)</code>", "Troca todas as datas por um marcador."),
        ], fim="Use sempre o prefixo <code>r\"...\"</code>: ele impede o Python de interpretar as barras invertidas."),
        cod("Caçador de e-mails", "Devolva a lista de todos os e-mails do texto. Considere e-mail como: letras, dígitos, ponto ou sublinhado, depois <code>@</code>, depois letras, dígitos e pontos.",
            '''
import re

def emails(texto):
    return []

print(emails("Fale com ana.silva@empresa.com ou suporte_2@ajuda.com.br hoje."))
''',
            [("Acha os dois", "assert emails('Fale com ana.silva@empresa.com ou suporte_2@ajuda.com.br hoje.') == ['ana.silva@empresa.com', 'suporte_2@ajuda.com.br'], f'deu {emails(\"Fale com ana.silva@empresa.com ou suporte_2@ajuda.com.br hoje.\")}'"),
             ("Sem e-mail, lista vazia", "assert emails('nada aqui @ nem ali') == []")],
            '''
import re

def emails(texto):
    return re.findall(r"[\\w.]+@\\w+(?:\\.\\w+)+", texto)

print(emails("Fale com ana.silva@empresa.com ou suporte_2@ajuda.com.br hoje."))
''', ["Antes do @: <code>[\\w.]+</code>.", "Depois: <code>\\w+</code> seguido de um ou mais <code>\\.\\w+</code>."]),
        cod("Anonimizando dados", "Troque todos os CPFs do texto (formato <code>000.000.000-00</code>) por <b>[CPF]</b>.",
            '''
import re

def anonimizar(texto):
    return texto

print(anonimizar("Cliente 123.456.789-09 e sócio 987.654.321-00."))
''',
            [("Troca os dois CPFs", "assert anonimizar('Cliente 123.456.789-09 e sócio 987.654.321-00.') == 'Cliente [CPF] e sócio [CPF].'"), ("Não mexe em outros números", "assert anonimizar('Pedido 12345 de 2025') == 'Pedido 12345 de 2025'")],
            '''
import re

def anonimizar(texto):
    return re.sub(r"\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}", "[CPF]", texto)

print(anonimizar("Cliente 123.456.789-09 e sócio 987.654.321-00."))
''', ["<code>re.sub(padrao, \"[CPF]\", texto)</code>.", "O ponto precisa de barra: <code>\\.</code>"], rot="Mão no código · nível 2"),
        erros([
            ("Esquecer de escapar o ponto.", "<code>.</code> sozinho casa com qualquer caractere. Ponto literal é <code>\\.</code>"),
            ("Padrões gulosos: <code>&lt;.*&gt;</code> pegando o texto inteiro.", "<code>*</code> pega o máximo possível. Use <code>.*?</code> para o mínimo."),
            ("Usar regex para tudo.", "Para HTML e JSON existem analisadores próprios; regex é para padrões simples em texto."),
        ]),
        ponte("Regex no pré-processamento",
              "<p>Limpar textos antes de treinar ou indexar (tirar URLs, normalizar espaços, mascarar dados pessoais) é quase todo feito com regex. E extrair a resposta de um LLM do meio de um texto (“o número depois de <i>Resposta:</i>”) é um uso diário.</p>"),
        quiz([
            ("O que <code>\\d{4}</code> casa?", ["Quatro letras.", "Exatamente quatro dígitos.", "Até quatro dígitos."], 1, "Chaves fixam a quantidade."),
            ("Qual função troca um padrão por outro texto?", ["<code>re.findall</code>", "<code>re.sub</code>", "<code>re.search</code>"], 1, "<i>substitute</i>."),
            ("Por que usar <code>r\"...\"</code>?", ["Deixa a regex mais rápida.", "Evita que o Python interprete as barras invertidas.", "Ignora maiúsculas."], 1, "É uma string crua."),
        ]),
    ],
    ["Regex descreve o <b>formato</b> do que você procura.", "<code>findall</code> lista, <code>search</code> acha o primeiro, <code>sub</code> substitui.", "Parênteses capturam partes; escape o ponto."],
    "Web scraping: coletar dados de páginas.",
    livro=("ATBS:7", "Capítulo 7, “Pattern Matching with Regular Expressions”", "Que projeto de extração de telefones o livro constrói?"))

AULAS["Web scraping com BeautifulSoup"] = aula(
    35,
    "Nem todo dado vem numa API ou num CSV. Às vezes ele está numa página, no meio de menus e anúncios. Web scraping é ensinar o programa a <b>ler a página</b> e trazer só o que interessa.",
    ["entender a estrutura de tags do HTML;", "localizar elementos com <code>find</code>, <code>find_all</code> e <code>select</code>;", "raspar com responsabilidade."],
    ["Requests, dicionários e listas."],
    [
        chute("Para coletar os preços de uma página de produtos, qual é o primeiro passo?", ["Escrever uma regex que procure o símbolo de reais.", "Inspecionar o HTML e descobrir em que tag e classe os preços estão.", "Baixar todas as imagens."], 1,
              ["Regex em HTML quebra na primeira mudança de layout.", "Isso! Botão direito → Inspecionar mostra a estrutura. Com a tag e a classe em mãos, o código fica simples.", "Imagens não trazem o preço."],
              "Scraping é 80% inspecionar a página e 20% escrever código."),
        concreto("A estante etiquetada", "<p>Uma página HTML é uma estante cheia de caixas dentro de caixas, cada uma com uma <b>etiqueta</b> (a tag) e, às vezes, um <b>apelido</b> (a classe). Você pede ao BeautifulSoup: “me traga todas as caixas <code>span</code> com o apelido <code>preco</code>”.</p>"),
        nota("HTML e BeautifulSoup", [
            ("<code>&lt;h2 class=\"titulo\"&gt;Oi&lt;/h2&gt;</code>", "uma tag", "Nome <code>h2</code>, atributo <code>class</code>, conteúdo “Oi”."),
            ("<code>BeautifulSoup(html, \"html.parser\")</code>", "analisar", "Transforma o texto HTML numa árvore navegável."),
            ("<code>sopa.find(\"h2\")</code>", "achar o primeiro", "<code>find_all</code> acha todos."),
            ("<code>sopa.select(\"div.card span.preco\")</code>", "seletor CSS", "Ponto indica classe; espaço indica “dentro de”."),
            ("<code>tag.get_text(strip=True)</code> / <code>tag[\"href\"]</code>", "texto / atributo", "O conteúdo visível e o valor de um atributo."),
        ]),
        lab("Raspando uma página de verdade", '''
import requests
from bs4 import BeautifulSoup

r = requests.get("https://quotes.toscrape.com/", timeout=10)
sopa = BeautifulSoup(r.text, "html.parser")
for bloco in sopa.select("div.quote")[:3]:
    frase = bloco.select_one("span.text").get_text(strip=True)
    autor = bloco.select_one("small.author").get_text(strip=True)
    print(autor, "-", frase)
''', corpo="<p>Rode no seu computador (<code>pip install requests beautifulsoup4</code>). O site <i>quotes.toscrape.com</i> existe justamente para praticar.</p>",
            exps=["Troque o <code>[:3]</code> para pegar todas as frases da página.", "Colete também as tags de cada frase (<code>a.tag</code>)."]),
        cod("Extraindo sem biblioteca", "Para entender a ideia, extraia os preços de um HTML simples usando o analisador da biblioteca padrão: complete <code>handle_data</code> para guardar o texto só quando estiver dentro de um <code>span</code> com classe <code>preco</code>.",
            '''
from html.parser import HTMLParser

class Precos(HTMLParser):
    def __init__(self):
        super().__init__()
        self.dentro = False
        self.achados = []

    def handle_starttag(self, tag, attrs):
        self.dentro = tag == "span" and ("class", "preco") in attrs

    def handle_endtag(self, tag):
        self.dentro = False

    def handle_data(self, data):
        pass

html = '<div><h2>Caneta</h2><span class="preco">2.50</span><span class="obs">promo</span><span class="preco">18.00</span></div>'
p = Precos()
p.feed(html)
print(p.achados)
''',
            [("Acha os dois preços", "assert p.achados == ['2.50', '18.00'], f'achados = {p.achados}'")],
            '''
from html.parser import HTMLParser

class Precos(HTMLParser):
    def __init__(self):
        super().__init__()
        self.dentro = False
        self.achados = []

    def handle_starttag(self, tag, attrs):
        self.dentro = tag == "span" and ("class", "preco") in attrs

    def handle_endtag(self, tag):
        self.dentro = False

    def handle_data(self, data):
        if self.dentro:
            self.achados.append(data)

html = '<div><h2>Caneta</h2><span class="preco">2.50</span><span class="obs">promo</span><span class="preco">18.00</span></div>'
p = Precos()
p.feed(html)
print(p.achados)
''', ["Se <code>self.dentro</code> for verdadeiro, acrescente <code>data</code> em <code>self.achados</code>."]),
        erros([
            ("Raspar sem ler os termos de uso e o <code>robots.txt</code>.", "Respeite as regras do site e prefira a API oficial quando existir."),
            ("Fazer centenas de pedidos por segundo.", "Você pode derrubar o site e ser bloqueado. Use <code>time.sleep</code> entre os pedidos."),
            ("A página vem “vazia” no <code>requests</code>.", "O conteúdo é montado por JavaScript. Procure a API que a página chama, ou use Playwright."),
        ]),
        ponte("Scraping e IA",
              "<p>Os grandes modelos de linguagem foram treinados com textos coletados da web. No seu dia a dia, scraping alimenta um <b>RAG</b> com a documentação da sua empresa ou monta um dataset que não existe pronto. Dados pessoais e direitos autorais exigem cuidado redobrado.</p>"),
        quiz([
            ("O que <code>find_all(\"a\")</code> devolve?", ["O primeiro link.", "Uma lista com todas as tags <code>a</code>.", "O texto da página."], 1, "Todos os elementos com aquela tag."),
            ("No seletor <code>div.card</code>, o ponto indica:", ["Uma classe.", "Um id.", "O fim do seletor."], 0, "<code>.</code> é classe; <code>#</code> é id."),
            ("O que fazer antes de raspar um site?", ["Nada.", "Verificar se há API e ler as regras do site.", "Desligar o antivírus."], 1, "Raspagem responsável."),
        ]),
    ],
    ["HTML é uma árvore de tags com atributos.", "BeautifulSoup localiza elementos por tag, classe ou seletor CSS.", "Raspe devagar, respeitando regras e privacidade."],
    "Hora de praticar: 30 exercícios para fixar a base.",
    livro=("ATBS:12", "Capítulo 12, “Web Scraping”, seção sobre o BeautifulSoup", "Que projeto de busca o livro automatiza?"))

AULAS["30 exercícios (Beecrowd, HackerRank, Exercism)"] = aula(
    40,
    "Assistir a aulas dá a sensação de ter aprendido. Resolver um problema sem olhar a resposta é o que <b>prova</b>. Esta aula é um método para praticar: como escolher exercícios, como atacar um problema e o que fazer quando travar.",
    ["seguir um método de 4 passos para resolver problemas;", "escolher exercícios no nível certo;", "transformar erros em aprendizado."],
    ["Todo o conteúdo da Fase 1 até aqui."],
    [
        chute("Você travou num exercício há 15 minutos. Qual a melhor atitude?", ["Ver a solução pronta e seguir em frente.", "Reler o enunciado, resolver um exemplo à mão e escrever os passos em português.", "Desistir: esse exercício é difícil demais."], 1,
              ["Ver a resposta dá alívio, mas o que ensina é o esforço de procurar.", "Isso! Quase todo travamento é um problema de <b>entendimento</b>, não de código. Voltar ao papel destrava.", "Travar faz parte. Sem alguma dificuldade, não há aprendizado."],
              "Dificuldade na medida certa é sinal de que você está aprendendo."),
        concreto("A academia", "<p>Ninguém fica forte assistindo a vídeos de musculação. Programar é igual: o músculo cresce na <b>repetição com carga</b>. Trinta exercícios pequenos valem mais que um curso inteiro só assistido.</p>"),
        passos("O método dos 4 passos", [
            ("<b>Entenda</b>: diga com suas palavras o que entra e o que sai.", "Se não consegue explicar, ainda não entendeu."),
            ("<b>Resolva à mão</b> um exemplo pequeno.", "Você descobre o algoritmo fazendo, não pensando no código."),
            ("<b>Escreva os passos</b> em português, como comentários.", "Cada comentário vira uma ou duas linhas de código."),
            ("<b>Programe e teste</b> com o exemplo, um caso de borda e um caso grande.", "Só então envie."),
        ], fim="Depois de resolver, veja uma solução de outra pessoa: é aí que você aprende truques novos."),
        tabela("Onde praticar", ["Plataforma", "Melhor para", "Idioma"], [
            ["Beecrowd", "Começar: problemas de entrada e saída, em ordem de dificuldade", "Português"],
            ["Exercism", "Receber revisão de mentores e aprender estilo", "Inglês"],
            ["HackerRank", "Trilhas por assunto e preparação para testes de emprego", "Inglês"],
            ["Estes exercícios", "Fixar cada aula logo depois de assistir", "Português"],
        ], rot="Mapa"),
        cod("Aquecimento: FizzBuzz", "O clássico das entrevistas. Para os números de 1 a 15: imprima <b>Fizz</b> se for múltiplo de 3, <b>Buzz</b> se for de 5, <b>FizzBuzz</b> se for dos dois, e o próprio número nos outros casos.",
            '''
for n in range(1, 16):
    print(n)
''',
            [("15 linhas corretas", "esperado = ['1','2','Fizz','4','Buzz','Fizz','7','8','Fizz','Buzz','11','Fizz','13','14','FizzBuzz']\nassert saida.split() == esperado, f'saiu {saida.split()}'")],
            '''
for n in range(1, 16):
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)
''', ["Teste primeiro o caso mais exigente: múltiplo de 3 <b>e</b> de 5.", "<code>n % 3 == 0</code> testa se é múltiplo de 3."]),
        cod("Palíndromo", "Devolva <code>True</code> se a frase for igual lida de trás para frente, ignorando espaços e maiúsculas.",
            '''
def palindromo(frase):
    return False

print(palindromo("A sacada da casa"), palindromo("Python"))
''',
            [("Frase com espaços", "assert palindromo('A sacada da casa') is True"), ("Não palíndromo", "assert palindromo('Python') is False"), ("Uma letra", "assert palindromo('a') is True")],
            '''
def palindromo(frase):
    limpa = frase.lower().replace(" ", "")
    return limpa == limpa[::-1]

print(palindromo("A sacada da casa"), palindromo("Python"))
''', ["Limpe: <code>frase.lower().replace(\" \", \"\")</code>.", "<code>texto[::-1]</code> inverte."], rot="Mão no código · nível 2"),
        cod("Número mais frequente", "Devolva o valor que mais aparece na lista (em caso de empate, o que aparece primeiro).",
            '''
def mais_frequente(valores):
    return None

print(mais_frequente([3, 1, 3, 2, 1, 3]))
''',
            [("Acha o 3", "assert mais_frequente([3, 1, 3, 2, 1, 3]) == 3"), ("Empate: o primeiro", "assert mais_frequente([5, 7, 7, 5]) == 5"), ("Textos também", "assert mais_frequente(['a', 'b', 'b']) == 'b'")],
            '''
def mais_frequente(valores):
    cont = {}
    for v in valores:
        cont[v] = cont.get(v, 0) + 1
    melhor = valores[0]
    for v in valores:
        if cont[v] > cont[melhor]:
            melhor = v
    return melhor

print(mais_frequente([3, 1, 3, 2, 1, 3]))
''', ["Conte com um dicionário.", "Percorra a lista na ordem original e troque só se a contagem for <b>maior</b>."], rot="Mão no código · nível 3"),
        erros([
            ("Só fazer exercícios fáceis.", "Sem esforço não há progresso. Procure os que exigem 15 a 40 minutos."),
            ("Copiar a solução e “entender”.", "Entender uma solução é diferente de conseguir produzi-la. Feche a aba e refaça no dia seguinte."),
            ("Pular o passo de resolver à mão.", "Código escrito sem plano vira tentativa e erro."),
        ]),
        ponte("Prática e IA generativa",
              "<p>Um assistente de IA resolve esses exercícios em segundos, e é exatamente por isso que você deve resolvê-los sozinho agora. Mais adiante, seu trabalho será <b>avaliar e corrigir</b> código gerado por IA, e só avalia bem quem já escreveu muito.</p>"),
        quiz([
            ("Qual é o primeiro passo diante de um problema?", ["Começar a digitar.", "Entender entrada e saída e resolver um exemplo à mão.", "Procurar a solução."], 1, "Entendimento antes do código."),
            ("Qual exercício ensina mais?", ["O que você resolve em 1 minuto.", "O que exige esforço mas você consegue.", "O que é impossível para o seu nível."], 1, "A zona de dificuldade desejável."),
            ("O que fazer depois de resolver?", ["Ir para o próximo.", "Comparar com outras soluções e anotar o que aprendeu.", "Apagar o código."], 1, "É assim que o repertório cresce."),
        ]),
    ],
    ["Método: entender, resolver à mão, escrever os passos, programar e testar.", "Escolha exercícios que exijam esforço real.", "Compare soluções depois de resolver."],
    "Algoritmos de busca e ordenação: os clássicos.",
    livro=("ATBS:8", "Capítulo 8, “Input Validation”, e os projetos práticos do fim dos capítulos", "Que projetos práticos o livro sugere no final de cada capítulo?"))

AULAS["Algoritmos de busca e ordenação"] = aula(
    40,
    "Achar um nome numa lista de um bilhão de itens em 30 passos, em vez de um bilhão. Não é hardware melhor: é um <b>algoritmo</b> melhor. Busca e ordenação são os exemplos clássicos de como uma boa ideia vale mais que força bruta.",
    ["implementar busca linear e busca binária;", "entender a ideia de um algoritmo de ordenação;", "usar <code>sorted</code> e <code>in</code> sabendo o que há por trás."],
    ["Listas, laços e funções."],
    [
        chute("Uma lista <b>ordenada</b> tem 1.000 números. No pior caso, quantas comparações a busca binária precisa para achar um deles?", ["1.000", "500", "Cerca de 10"], 2,
              ["Isso é a busca linear: olhar um por um.", "Metade seria o caso médio da busca linear.", "Isso! Cada comparação <b>descarta metade</b>: 1000 → 500 → 250 → ... → 1. São uns 10 passos."],
              "Dobrar o tamanho da lista custa só <b>um</b> passo a mais."),
        concreto("A lista telefônica", "<p>Para achar “Silva”, ninguém começa na página 1. Você abre <b>no meio</b>, vê que caiu em “M”, descarta a metade da esquerda e repete. Isso é a busca binária, e só funciona porque a lista está <b>em ordem</b>.</p>"),
        crianca("<p>O jogo de adivinhar um número de 1 a 100: se você chuta sempre o <b>meio</b> e a resposta é “maior” ou “menor”, acerta em no máximo 7 tentativas.</p>"),
        ver("como o professor acompanha o meio, o início e o fim a cada passo"),
        nota("As duas buscas", [
            ("Busca linear", "um por um", "Funciona em qualquer lista. No pior caso, olha todos os itens."),
            ("Busca binária", "sempre no meio", "Exige lista ordenada. Descarta metade a cada passo."),
            ("<code>inicio</code>, <code>fim</code>, <code>meio</code>", "os três ponteiros", "<code>meio = (inicio + fim) // 2</code>; depois move <code>inicio</code> ou <code>fim</code>."),
            ("<code>sorted(v)</code> / <code>v.sort()</code>", "ordenar", "O Python usa o Timsort, muito eficiente. <code>sorted</code> cria uma lista nova; <code>sort</code> altera a original."),
        ], rot="Os conceitos"),
        passos("Procurando o 23 em <code>[2, 5, 8, 12, 16, 23, 38, 56]</code>", [
            ("<code>inicio = 0</code>, <code>fim = 7</code>, <code>meio = 3</code> → valor 12.", "23 é maior: descarte a esquerda, <code>inicio = 4</code>."),
            ("<code>meio = (4 + 7) // 2 = 5</code> → valor 23.", "Achou, em 2 comparações."),
            ("Se não existisse, <code>inicio</code> passaria de <code>fim</code>.", "É o sinal de parada: devolva -1."),
        ]),
        cod("Busca binária", "Implemente a busca binária: devolva o <b>índice</b> do alvo na lista ordenada, ou -1 se não existir.",
            '''
def busca_binaria(lista, alvo):
    inicio, fim = 0, len(lista) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        # compare lista[meio] com o alvo e ajuste inicio ou fim
        break
    return -1

print(busca_binaria([2, 5, 8, 12, 16, 23, 38, 56], 23))
''',
            [("Acha o 23 no índice 5", "assert busca_binaria([2, 5, 8, 12, 16, 23, 38, 56], 23) == 5"), ("Primeiro e último", "v = [1, 3, 5, 7, 9]\nassert busca_binaria(v, 1) == 0 and busca_binaria(v, 9) == 4"),
             ("Ausente devolve -1", "assert busca_binaria([1, 3, 5], 4) == -1 and busca_binaria([], 1) == -1"), ("Funciona em lista grande", "v = list(range(0, 100000, 3))\nassert busca_binaria(v, 29997) == 9999")],
            '''
def busca_binaria(lista, alvo):
    inicio, fim = 0, len(lista) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if lista[meio] == alvo:
            return meio
        if lista[meio] < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1

print(busca_binaria([2, 5, 8, 12, 16, 23, 38, 56], 23))
''', ["Igual: devolva <code>meio</code>.", "Menor que o alvo: <code>inicio = meio + 1</code>. Maior: <code>fim = meio - 1</code>."]),
        cod("Ordenação por seleção", "Para entender como uma ordenação funciona por dentro: a cada volta, ache o menor item do trecho que falta e troque-o de lugar. Complete a troca.",
            '''
def ordenar(v):
    v = v[:]  # copia, para não alterar a original
    for i in range(len(v)):
        menor = i
        for j in range(i + 1, len(v)):
            if v[j] < v[menor]:
                menor = j
        # troque v[i] com v[menor]
    return v

print(ordenar([5, 2, 9, 1, 7]))
''',
            [("Ordena", "assert ordenar([5, 2, 9, 1, 7]) == [1, 2, 5, 7, 9]"), ("Com repetidos", "assert ordenar([3, 1, 3, 2]) == [1, 2, 3, 3]"), ("Não altera a original", "o = [2, 1]\nordenar(o)\nassert o == [2, 1]")],
            '''
def ordenar(v):
    v = v[:]
    for i in range(len(v)):
        menor = i
        for j in range(i + 1, len(v)):
            if v[j] < v[menor]:
                menor = j
        v[i], v[menor] = v[menor], v[i]
    return v

print(ordenar([5, 2, 9, 1, 7]))
''', ["Em Python a troca é uma linha: <code>v[i], v[menor] = v[menor], v[i]</code>."], rot="Mão no código · nível 2"),
        erros([
            ("Usar busca binária em lista desordenada.", "O resultado sai errado sem nenhum aviso. Ordene antes."),
            ("<code>inicio = meio</code> em vez de <code>meio + 1</code>.", "O intervalo nunca encolhe e o laço fica infinito."),
            ("Escrever sua própria ordenação em código de produção.", "Use <code>sorted</code>. Implementar serve para aprender, não para usar."),
        ]),
        ponte("Busca em IA",
              "<p>Quando um RAG procura os trechos mais parecidos com a sua pergunta entre milhões de documentos, ele não compara com todos: usa estruturas de <b>busca aproximada</b> (como HNSW) que, no espírito da busca binária, descartam quase tudo a cada passo. E <code>sorted(resultados, key=score)</code> é o último passo de qualquer ranqueamento.</p>"),
        quiz([
            ("Qual é o requisito da busca binária?", ["Lista sem repetidos.", "Lista ordenada.", "Lista com tamanho par."], 1, "Só assim dá para descartar metade."),
            ("Quantos passos, no pior caso, para 1 milhão de itens ordenados?", ["Cerca de 20", "1.000", "500.000"], 0, "2 elevado a 20 passa de 1 milhão."),
            ("Qual a diferença entre <code>sorted(v)</code> e <code>v.sort()</code>?", ["Nenhuma.", "<code>sorted</code> devolve uma lista nova; <code>sort</code> altera a original.", "<code>sort</code> é mais lento."], 1, "E <code>sort()</code> devolve <code>None</code>."),
        ]),
    ],
    ["Busca linear olha tudo; busca binária descarta metade a cada passo, em lista ordenada.", "Ordenar é o que torna buscas rápidas possíveis.", "No dia a dia, use <code>sorted</code> e saiba o que ele faz."],
    "Big O: medir o quanto um algoritmo escala.",
    livro=("PYDOC:datastructures", "Seção 5.1 (mais sobre listas), métodos sort e index", "Que métodos de lista o tutorial apresenta para busca e ordenação?"))

AULAS["Noções de complexidade (Big O)"] = aula(
    35,
    "Seu código roda em 1 segundo com mil linhas de dados. Com um milhão, vai levar 17 minutos ou 11 dias? A resposta está no <b>Big O</b>: uma forma de dizer como o tempo cresce quando os dados crescem.",
    ["reconhecer O(1), O(log n), O(n), O(n log n) e O(n²);", "estimar a complexidade contando laços;", "trocar lista por conjunto ou dicionário quando a busca pesa."],
    ["Laços, listas, dicionários e busca binária."],
    [
        chute("Quantas vezes o <code>print</code> roda quando <code>n = 1000</code>?", ["1.000", "2.000", "1.000.000"], 2,
              ["Seria com um laço só.", "Seria com dois laços, um depois do outro.", "Isso! Laço dentro de laço multiplica: 1.000 × 1.000. É o O(n²)."],
              "Laços <b>aninhados</b> multiplicam; laços <b>em sequência</b> somam.",
              cod='for i in range(n):\n    for j in range(n):\n        print(i, j)'),
        concreto("Apertos de mão", "<p>Numa festa, cumprimentar o <b>anfitrião</b> é 1 aperto, não importa quantos convidados: O(1). Cada convidado cumprimentar o anfitrião são n apertos: O(n). <b>Todos se cumprimentarem entre si</b> são cerca de n²/2: O(n²). Com 10 pessoas, 45; com 1.000, quase meio milhão.</p>"),
        tabela("A escada da complexidade", ["Notação", "Nome", "Exemplo", "n = 1 milhão"], [
            ["O(1)", "constante", "Acessar <code>v[5]</code>; buscar chave num dicionário", "1 passo"],
            ["O(log n)", "logarítmica", "Busca binária", "~20 passos"],
            ["O(n)", "linear", "Somar uma lista; <code>x in lista</code>", "1 milhão"],
            ["O(n log n)", "linearítmica", "<code>sorted</code>", "~20 milhões"],
            ["O(n²)", "quadrática", "Comparar todos com todos", "1 trilhão"],
        ], rot="Agora sim, a notação"),
        passos("Achando duplicados: de O(n²) para O(n)", [
            ("Versão 1: para cada item, percorrer a lista inteira procurando outro igual.", "Laço dentro de laço: O(n²)."),
            ("Versão 2: guardar os itens já vistos num <b>conjunto</b>.", "Perguntar <code>x in conjunto</code> custa O(1)."),
            ("Um laço só, com uma consulta rápida dentro.", "O(n): para 1 milhão de itens, de dias para menos de um segundo."),
        ], fim="Trocar a <b>estrutura de dados</b> costuma render mais do que otimizar linhas de código."),
        cod("Tem duplicado?", "Reescreva a função para rodar em tempo linear, usando um conjunto. O último teste usa 200 mil itens e só passa dentro do limite de tempo se a solução for O(n).",
            '''
def tem_duplicado(valores):
    for i in range(len(valores)):
        for j in range(i + 1, len(valores)):
            if valores[i] == valores[j]:
                return True
    return False

print(tem_duplicado([1, 2, 3, 2]), tem_duplicado([1, 2, 3]))
''',
            [("Acha duplicado", "assert tem_duplicado([1, 2, 3, 2]) is True"), ("Sem duplicado", "assert tem_duplicado([1, 2, 3]) is False and tem_duplicado([]) is False"),
             ("Rápido com 200 mil itens", "import time\nt = time.time()\nassert tem_duplicado(list(range(200000))) is False\nassert time.time() - t < 2, 'ainda está quadrático: use um conjunto'")],
            '''
def tem_duplicado(valores):
    vistos = set()
    for v in valores:
        if v in vistos:
            return True
        vistos.add(v)
    return False

print(tem_duplicado([1, 2, 3, 2]), tem_duplicado([1, 2, 3]))
''', ["Crie <code>vistos = set()</code>.", "Para cada valor: se já está em <code>vistos</code>, devolva <code>True</code>; senão, adicione."]),
        erros([
            ("<code>x in lista</code> dentro de um laço grande.", "É um laço escondido: vira O(n²). Converta a lista em <code>set</code> antes."),
            ("Otimizar antes de medir.", "Primeiro faça funcionar; depois meça onde está o gargalo."),
            ("Achar que Big O dá o tempo em segundos.", "Ele diz como o tempo <b>cresce</b>, não quanto dura."),
        ]),
        ponte("Complexidade em IA",
              "<p>A atenção de um Transformer compara cada token com todos os outros: O(n²) no tamanho do texto. É por isso que dobrar a janela de contexto quadruplica o custo, e por isso existem KV cache e atenção esparsa. Em dados, a diferença entre um laço Python e uma operação vetorizada do NumPy é a diferença entre horas e segundos.</p>"),
        quiz([
            ("Qual a complexidade de buscar uma chave num dicionário?", ["O(1)", "O(n)", "O(n²)"], 0, "Tabelas de espalhamento acham direto."),
            ("Dois laços <b>aninhados</b> sobre n itens dão:", ["O(n)", "O(2n)", "O(n²)"], 2, "Multiplicam."),
            ("Qual cresce mais devagar?", ["O(n)", "O(log n)", "O(n log n)"], 1, "Logarítmica: dobrar n soma um passo."),
        ]),
    ],
    ["Big O descreve como o custo cresce com o tamanho da entrada.", "Laços aninhados multiplicam; em sequência, somam.", "Conjuntos e dicionários transformam buscas O(n) em O(1)."],
    "Projeto final da fase: um programa de linha de comando completo.",
    livro=("MISSING:debugging-profiling", "Aula “Debugging and Profiling”, parte de profiling", "Que ferramentas a aula usa para medir tempo de execução?"))

AULAS["Projeto de linha de comando completo"] = aula(
    45,
    "Hora de juntar tudo: funções, arquivos, JSON, erros e laços num programa que alguém consegue <b>usar</b>. Um projeto pequeno e terminado ensina mais do que dez tutoriais pela metade, e é o primeiro item do seu portfólio.",
    ["planejar um programa em funções pequenas;", "montar um menu em laço e salvar dados em JSON;", "ler argumentos da linha de comando."],
    ["Funções, arquivos, JSON e tratamento de erros."],
    [
        chute("Você vai fazer um gerenciador de tarefas. Por onde começar?", ["Pelo menu colorido.", "Pela lista de funções: adicionar, listar, concluir, salvar, carregar.", "Pela interface gráfica."], 1,
              ["A aparência vem por último.", "Isso! Primeiro o <b>núcleo</b> testável; o menu é só uma casca que chama essas funções.", "Interface gráfica multiplicaria o trabalho sem ensinar o essencial."],
              "Separe a <b>lógica</b> (funções que recebem e devolvem dados) da <b>conversa</b> com o usuário (<code>input</code> e <code>print</code>)."),
        concreto("A cozinha e o balcão", "<p>Num restaurante, o <b>balcão</b> anota pedidos e entrega pratos; a <b>cozinha</b> prepara. Se o balcão mudar (delivery, aplicativo), a cozinha continua igual. No seu programa, o menu é o balcão e as funções são a cozinha.</p>"),
        ver("como o professor divide o projeto em funções e arquivos"),
        passos("O plano do projeto", [
            ("Defina os dados: uma lista de dicionários <code>{\"titulo\": ..., \"feita\": False}</code>.", "A estrutura de dados é a primeira decisão."),
            ("Escreva as funções puras: <code>adicionar</code>, <code>concluir</code>, <code>pendentes</code>.", "Recebem a lista e devolvem o resultado. Fáceis de testar."),
            ("Escreva <code>salvar</code> e <code>carregar</code> com JSON.", "Os dados sobrevivem ao fim do programa."),
            ("Monte o menu num <code>while True</code> com <code>input</code>.", "Opção inválida não derruba o programa: trate o erro."),
            ("Escreva o README e publique no GitHub.", "Projeto sem README é projeto invisível."),
        ]),
        cod("O núcleo do gerenciador", "Implemente as três funções do núcleo. <code>adicionar</code> acrescenta uma tarefa não feita; <code>concluir</code> marca como feita a tarefa do índice dado (e dispara <code>IndexError</code> se o índice não existir); <code>pendentes</code> devolve os títulos das não feitas.",
            '''
def adicionar(tarefas, titulo):
    pass

def concluir(tarefas, indice):
    pass

def pendentes(tarefas):
    return []

tarefas = []
adicionar(tarefas, "estudar laços")
adicionar(tarefas, "fazer exercícios")
concluir(tarefas, 0)
print(pendentes(tarefas))
''',
            [("Adiciona como não feita", "t = []\nadicionar(t, 'a')\nassert t == [{'titulo': 'a', 'feita': False}], f't = {t}'"),
             ("Conclui pelo índice", "t = []\nadicionar(t, 'a'); adicionar(t, 'b')\nconcluir(t, 1)\nassert t[1]['feita'] is True and t[0]['feita'] is False"),
             ("Lista só as pendentes", "t = []\nadicionar(t, 'a'); adicionar(t, 'b')\nconcluir(t, 0)\nassert pendentes(t) == ['b']"),
             ("Índice inexistente dispara IndexError", "try:\n    concluir([], 3)\n    ok = False\nexcept IndexError:\n    ok = True\nassert ok")],
            '''
def adicionar(tarefas, titulo):
    tarefas.append({"titulo": titulo, "feita": False})

def concluir(tarefas, indice):
    tarefas[indice]["feita"] = True

def pendentes(tarefas):
    return [t["titulo"] for t in tarefas if not t["feita"]]

tarefas = []
adicionar(tarefas, "estudar laços")
adicionar(tarefas, "fazer exercícios")
concluir(tarefas, 0)
print(pendentes(tarefas))
''', ["<code>tarefas.append({\"titulo\": titulo, \"feita\": False})</code>", "<code>tarefas[indice]</code> já dispara <code>IndexError</code> sozinho quando o índice não existe."]),
        cod("Salvar e carregar", "Complete <code>salvar</code> e <code>carregar</code> com JSON. <code>carregar</code> deve devolver uma lista vazia se o arquivo ainda não existir.",
            '''
import json
from pathlib import Path

def salvar(tarefas, caminho):
    pass

def carregar(caminho):
    return []

salvar([{"titulo": "a", "feita": True}], "tarefas.json")
print(carregar("tarefas.json"))
''',
            [("Ida e volta", "salvar([{'titulo': 'a', 'feita': True}], 't.json')\nassert carregar('t.json') == [{'titulo': 'a', 'feita': True}]"), ("Arquivo inexistente devolve []", "assert carregar('nao_existe_123.json') == []"),
             ("Mantém acentos", "salvar([{'titulo': 'ação', 'feita': False}], 't2.json')\nassert carregar('t2.json')[0]['titulo'] == 'ação'")],
            '''
import json
from pathlib import Path

def salvar(tarefas, caminho):
    Path(caminho).write_text(json.dumps(tarefas, ensure_ascii=False, indent=2), encoding="utf-8")

def carregar(caminho):
    p = Path(caminho)
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))

salvar([{"titulo": "a", "feita": True}], "tarefas.json")
print(carregar("tarefas.json"))
''', ["<code>Path(caminho).write_text(json.dumps(tarefas), encoding=\"utf-8\")</code>", "Em <code>carregar</code>, teste <code>p.exists()</code> antes de ler."], rot="Mão no código · nível 2"),
        lab("A casca: menu e argumentos", '''
import sys

def menu():
    tarefas = carregar("tarefas.json")
    while True:
        opcao = input("[a]dicionar  [c]oncluir  [l]istar  [s]air: ").strip().lower()
        if opcao == "a":
            adicionar(tarefas, input("Título: "))
        elif opcao == "c":
            try:
                concluir(tarefas, int(input("Número: ")) - 1)
            except (ValueError, IndexError):
                print("Número inválido.")
        elif opcao == "l":
            for i, titulo in enumerate(pendentes(tarefas), start=1):
                print(i, titulo)
        elif opcao == "s":
            salvar(tarefas, "tarefas.json")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "listar":
        print(pendentes(carregar("tarefas.json")))
    else:
        menu()
''', corpo="<p>No seu computador, junte as funções que você escreveu com esta casca num arquivo <code>tarefas.py</code>:</p>",
            exps=["Rode <code>python tarefas.py</code> e depois <code>python tarefas.py listar</code>.", "Acrescente a opção de remover uma tarefa.", "Troque <code>sys.argv</code> pelo módulo <code>argparse</code> e ganhe o <code>--help</code> de graça."]),
        erros([
            ("Misturar <code>input</code> e <code>print</code> dentro das funções de lógica.", "Fica impossível testar. Funções de lógica recebem e devolvem dados."),
            ("Querer todas as funcionalidades antes de terminar a primeira.", "Faça o mínimo que funciona, publique e melhore."),
            ("Não tratar entrada inválida.", "Usuário digita qualquer coisa. O programa não pode cair por isso."),
        ]),
        ponte("Do CLI ao seu primeiro app de IA",
              "<p>Troque a função <code>adicionar</code> por uma chamada a um LLM e este mesmo esqueleto vira um chatbot de terminal: laço, <code>input</code>, função, <code>print</code>, histórico salvo em JSON. Scripts de treino também são CLIs: <code>python treinar.py --epocas 10 --taxa 0.001</code>.</p>"),
        quiz([
            ("Por que separar lógica e interface?", ["Para o programa ficar maior.", "Para testar a lógica e trocar a interface sem reescrever tudo.", "Porque o Python exige."], 1, "Cozinha e balcão."),
            ("Para que serve <code>if __name__ == \"__main__\":</code>?", ["Roda o bloco só quando o arquivo é executado diretamente.", "Importa o módulo principal.", "Define o nome do programa."], 0, "Importado por outro arquivo, o bloco não roda."),
            ("O que <code>sys.argv[1]</code> contém?", ["O nome do arquivo.", "O primeiro argumento digitado depois do nome do arquivo.", "A versão do Python."], 1, "<code>sys.argv[0]</code> é o nome do script."),
        ]),
    ],
    ["Comece pelos dados e pelas funções de lógica; o menu é a casca.", "JSON guarda o estado entre uma execução e outra.", "Projeto pequeno, terminado e com README vale ouro."],
    "Fase 2: Python para dados, começando pelo NumPy.",
    livro=("ATBS:9", "Projetos práticos do fim do capítulo 9", "Como o livro estrutura um projeto que lê e grava arquivos?"))
