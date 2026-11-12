# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 1 (parte A): base da linguagem e estruturas de dados."""
from lesson_factory import *

AULAS = {}

AULAS["Instalar Python e usar o terminal"] = aula(
    30,
    "Todo programa de IA do mundo começa do mesmo jeito: alguém abre um terminal e digita <code>python</code>. Hoje você monta a sua bancada de trabalho e roda sua primeira linha de código.",
    ["instalar o Python e conferir a versão;", "navegar entre pastas pelo terminal;", "rodar um arquivo <code>.py</code> e usar o modo interativo."],
    ["Nenhum: é aqui que tudo começa."],
    [
        chute("Você digita <code>python --version</code> no terminal e aparece “comando não encontrado”. O que é mais provável?",
              ["O Python está com vírus.", "O Python não está instalado ou não foi adicionado ao PATH.", "O computador não suporta Python."], 1,
              ["Não tem nada a ver com vírus: o terminal só não achou o programa.", "Isso! O terminal procura programas numa lista de pastas chamada PATH. Se o Python não estiver nela, é como se não existisse.", "Qualquer computador dos últimos 15 anos roda Python."],
              "No Windows, marque a caixa <b>“Add python.exe to PATH”</b> na primeira tela do instalador."),
        concreto("O terminal é um balcão de atendimento",
                 "<p>Em vez de clicar em ícones, você <b>escreve o pedido</b>: “liste os arquivos”, “entre nesta pasta”, “rode este programa”. Parece antigo, mas é mais rápido e é como servidores e ferramentas de IA são operados.</p>"),
        crianca("<p>O computador é uma casa com muitos cômodos (pastas). O terminal é você andando pela casa de olhos vendados e perguntando: “onde estou?” (<code>pwd</code>), “o que tem aqui?” (<code>ls</code> ou <code>dir</code>), “quero ir para a cozinha” (<code>cd cozinha</code>).</p>"),
        ver("os passos que o professor segue para instalar o Python e abrir o primeiro programa"),
        nota("Os comandos que você vai usar todo dia", [
            ("<code>python --version</code>", "python versão", "Mostra a versão instalada. No Mac e no Linux pode ser <code>python3</code>."),
            ("<code>cd pasta</code>", "change directory", "Entra numa pasta. <code>cd ..</code> volta uma pasta."),
            ("<code>ls</code> / <code>dir</code>", "listar", "Mostra o que há na pasta atual (<code>dir</code> no Prompt do Windows)."),
            ("<code>python arquivo.py</code>", "rodar", "Executa o programa salvo no arquivo."),
            ("<code>python</code>", "modo interativo", "Abre o <code>&gt;&gt;&gt;</code>: cada linha roda na hora. Sai com <code>exit()</code>."),
        ], rot="Agora sim, os comandos"),
        passos("Do zero ao “Olá, mundo”", [
            ("Baixe o instalador em python.org e instale (no Windows, marque “Add to PATH”).", "Sem o PATH, o terminal não acha o Python."),
            ("Abra o terminal e digite <code>python --version</code>.", "Confirma que a instalação deu certo."),
            ("Crie uma pasta <code>estudos</code> e entre nela com <code>cd estudos</code>.", "Projetos organizados em pastas evitam bagunça desde o primeiro dia."),
            ("Crie o arquivo <code>ola.py</code> com a linha <code>print(\"Olá, mundo!\")</code>.", "Use o VS Code ou qualquer editor de texto simples."),
            ("Rode <code>python ola.py</code>.", "O Python lê o arquivo de cima para baixo e executa."),
        ], fim="Nesta página você nem precisa instalar nada para treinar: os exercícios rodam Python dentro do navegador."),
        cod("Seu primeiro programa", "Faça o programa imprimir exatamente <b>Olá, mundo!</b> e, na linha de baixo, o resultado de <b>2 + 3</b>.",
            '''
# Troque o texto e complete a segunda linha
print("...")
print()
''',
            [("Primeira linha é Olá, mundo!", "assert saida.splitlines()[0].strip() == 'Olá, mundo!', f'saiu {saida.splitlines()[0]!r}'"),
             ("Segunda linha é 5", "assert saida.splitlines()[1].strip() == '5', 'a segunda linha deve mostrar o resultado de 2 + 3'")],
            '''
print("Olá, mundo!")
print(2 + 3)
''', ["Texto vai entre aspas; conta vai sem aspas: <code>print(2 + 3)</code>."]),
        erros([
            ("Digitar código Python direto no terminal do sistema.", "<code>print(1)</code> só funciona depois de abrir o Python (o <code>&gt;&gt;&gt;</code>) ou dentro de um arquivo <code>.py</code>."),
            ("Salvar o arquivo como <code>ola.py.txt</code>.", "Ative a exibição de extensões no sistema e confira que termina em <code>.py</code>."),
            ("Rodar o arquivo estando em outra pasta.", "O terminal só enxerga a pasta atual. Use <code>cd</code> até a pasta do arquivo, ou passe o caminho completo."),
        ]),
        ponte("O terminal na vida de quem faz IA",
              "<p>Treinar um modelo num servidor com GPU, instalar bibliotecas com <code>pip</code>, subir uma API, versionar com <code>git</code>: tudo isso acontece no terminal. Quanto antes ele virar um lugar confortável, mais rápido você anda nas próximas fases.</p>"),
        quiz([
            ("O que faz <code>cd ..</code>?", ["Apaga a pasta atual.", "Volta para a pasta de cima.", "Lista os arquivos."], 1, "<code>..</code> significa “a pasta que contém esta”."),
            ("Como rodar o programa salvo em <code>app.py</code>?", ["<code>run app.py</code>", "<code>python app.py</code>", "<code>app.py --python</code>"], 1, "É o Python que executa o arquivo."),
            ("Para que serve o modo interativo (<code>&gt;&gt;&gt;</code>)?", ["Para testar linhas rápidas e ver o resultado na hora.", "Para instalar o Python.", "Para salvar arquivos."], 0, "Ótimo para experimentar; para programas de verdade, use arquivos."),
        ]),
    ],
    ["O terminal executa comandos escritos; <code>cd</code> anda entre pastas e <code>ls</code>/<code>dir</code> lista.", "<code>python arquivo.py</code> roda um programa; <code>python</code> sozinho abre o modo interativo.", "No Windows, o Python precisa estar no PATH."],
    "Variáveis e tipos: como o programa guarda informação.",
    livro=("MISSING:course-shell", "Aula 1, “The Shell”", "Quais comandos a aula usa para navegar entre pastas?"))

AULAS["Variáveis e tipos (int, float, str, bool)"] = aula(
    35,
    "Um modelo de IA é, no fundo, uma montanha de números guardados em variáveis. Antes de guardar bilhões, vamos aprender a guardar um.",
    ["criar variáveis e escolher bons nomes;", "reconhecer <code>int</code>, <code>float</code>, <code>str</code> e <code>bool</code>;", "converter um tipo em outro sem cair em pegadinhas."],
    ["Ter rodado seu primeiro <code>print</code>."],
    [
        chute("O que esse código imprime?", ["55", "10", "Dá erro"], 0,
              ["Isso! As aspas fazem de <code>\"5\"</code> um texto, e somar textos é <b>grudar</b> um no outro.", "Seria 10 se fossem números. Com aspas, são textos.", "Não dá erro: o <code>+</code> entre dois textos é permitido e significa juntar."],
              "O mesmo símbolo <code>+</code> faz coisas diferentes conforme o <b>tipo</b> do dado. Por isso tipos importam.",
              cod='a = "5"\nb = "5"\nprint(a + b)'),
        concreto("Caixas com etiqueta",
                 "<p>Uma variável é uma <b>caixa com etiqueta</b>. <code>idade = 30</code> põe o 30 numa caixa etiquetada “idade”. Depois, toda vez que você escrever <code>idade</code>, o Python abre a caixa e pega o que está dentro.</p>"),
        crianca("<p>Tipos são como potes da cozinha: um para <b>números inteiros</b> (quantos ovos), um para <b>números quebrados</b> (1,5 litro de leite), um para <b>palavras</b> (o nome da receita) e um para <b>sim ou não</b> (o forno está ligado?).</p>"),
        ver("como o professor mostra a diferença entre número e texto"),
        nota("Os quatro tipos básicos", [
            ("<code>int</code>", "inteiro", "Números sem vírgula: <code>7</code>, <code>-3</code>, <code>2024</code>."),
            ("<code>float</code>", "ponto flutuante", "Números com casas decimais, sempre com <b>ponto</b>: <code>1.75</code>, <code>0.001</code>."),
            ("<code>str</code>", "string (texto)", "Qualquer coisa entre aspas: <code>\"Ana\"</code>, <code>'42'</code>."),
            ("<code>bool</code>", "booleano", "Só dois valores: <code>True</code> ou <code>False</code>."),
            ("<code>type(x)</code>", "tipo de x", "Pergunta ao Python qual é o tipo. <code>int(\"5\")</code>, <code>float(\"1.5\")</code> e <code>str(5)</code> convertem."),
        ]),
        passos("Calculando uma média sem tropeçar no tipo", [
            ("<code>n1 = \"7\"</code> e <code>n2 = \"8\"</code> (vieram como texto, de um formulário).", "Tudo que o usuário digita chega como <code>str</code>."),
            ("<code>n1 + n2</code> daria <code>\"78\"</code>.", "Texto mais texto gruda."),
            ("Converta: <code>int(n1) + int(n2)</code> dá <code>15</code>.", "<code>int()</code> transforma o texto em número."),
            ("<code>15 / 2</code> dá <code>7.5</code>, um <code>float</code>.", "A divisão com <code>/</code> sempre devolve <code>float</code>."),
        ], fim="Regra prática: converta os dados para o tipo certo <b>assim que eles entram</b> no programa."),
        cod("Ficha de um modelo", "Complete as variáveis e imprima a frase exatamente assim: <b>Modelo gpt com 12 camadas e taxa 0.001</b>",
            '''
nome = "gpt"
camadas = 0      # deve ser o inteiro 12
taxa = 0         # deve ser o float 0.001

print("Modelo", nome)
''',
            [("camadas é int e vale 12", "assert type(camadas) is int and camadas == 12, f'camadas = {camadas!r}'"),
             ("taxa é float e vale 0.001", "assert type(taxa) is float and taxa == 0.001, f'taxa = {taxa!r}'"),
             ("Frase correta", "assert saida.strip() == 'Modelo gpt com 12 camadas e taxa 0.001', f'saiu {saida.strip()!r}'")],
            '''
nome = "gpt"
camadas = 12
taxa = 0.001

print("Modelo", nome, "com", camadas, "camadas e taxa", taxa)
''', ["O <code>print</code> aceita vários valores separados por vírgula e põe um espaço entre eles."]),
        erros([
            ("<code>idade = \"30\"</code> e depois <code>idade + 1</code>.", "Erro de tipo: texto não soma com número. Use <code>int(idade) + 1</code>."),
            ("Escrever <code>1,5</code> para um número decimal.", "Em Python o separador é o ponto: <code>1.5</code>. Com vírgula vira uma tupla de dois números."),
            ("Achar que <code>=</code> significa “é igual a”.", "<code>=</code> <b>guarda</b> um valor. Para comparar, usa-se <code>==</code>."),
            ("Nomes como <code>x1</code>, <code>aaa</code>, <code>coisa</code>.", "Prefira nomes que explicam o conteúdo: <code>preco_total</code>, <code>taxa_aprendizado</code>."),
        ]),
        ponte("Tipos em IA",
              "<p>Os pesos de uma rede neural são <code>float</code>. O número de camadas e de épocas é <code>int</code>. Os textos que um LLM lê são <code>str</code>, depois convertidos em inteiros (tokens). E <code>bool</code> decide coisas como “usar GPU?”. Você acabou de aprender os quatro tijolos.</p>"),
        quiz([
            ("Qual é o tipo de <code>3 / 2</code>?", ["int", "float", "str"], 1, "A divisão com <code>/</code> sempre devolve <code>float</code> (1.5)."),
            ("O que faz <code>int(\"12\") + 1</code>?", ["Dá erro.", "Resulta em 13.", "Resulta em \"121\"."], 1, "<code>int()</code> converte o texto em número antes da soma."),
            ("Qual nome de variável é o melhor?", ["<code>t</code>", "<code>total_de_vendas</code>", "<code>Total De Vendas</code>"], 1, "Descritivo, minúsculo e com sublinhados (e nomes não podem ter espaço)."),
        ]),
    ],
    ["Variável é um nome que guarda um valor; <code>=</code> guarda, <code>==</code> compara.", "Tipos básicos: <code>int</code>, <code>float</code>, <code>str</code> e <code>bool</code>.", "O mesmo operador se comporta diferente conforme o tipo; converta com <code>int()</code>, <code>float()</code> e <code>str()</code>."],
    "Entrada e saída de dados: conversar com quem usa o programa.",
    livro=("ATBS:1", "Capítulo 1, “Python Basics”", "Que tipos de dados o capítulo apresenta primeiro?"))

AULAS["Entrada e saída de dados"] = aula(
    30,
    "Um programa que não conversa com ninguém é uma calculadora trancada na gaveta. Com <code>input</code> ele pergunta, com <code>print</code> ele responde.",
    ["ler dados com <code>input()</code> e converter para número;", "montar mensagens com f-strings;", "formatar casas decimais na saída."],
    ["Variáveis e tipos."],
    [
        chute("O usuário digita <b>10</b>. O que o código imprime?", ["20", "1010", "Dá erro"], 1,
              ["Seria 20 se o valor fosse número.", "Isso! O <code>input</code> sempre devolve <b>texto</b>, e texto vezes 2 é o texto repetido.", "Multiplicar texto por inteiro é permitido: repete o texto."],
              "Guarde para sempre: <code>input()</code> devolve <code>str</code>. Para fazer contas, converta.",
              cod='n = input("Número: ")\nprint(n * 2)'),
        concreto("O caixa da padaria",
                 "<p>O caixa <b>pergunta</b> (“quantos pães?”), <b>espera</b> você responder, <b>calcula</b> e <b>fala o total</b>. É o ciclo de quase todo programa: entrada, processamento, saída.</p>"),
        crianca("<p><code>input</code> é o programa fazendo uma pergunta e ficando quietinho até você responder. <code>print</code> é o programa falando. E a f-string é uma frase com <b>lacunas</b> que o Python preenche: “Olá, {nome}!”.</p>"),
        ver("como o professor converte o que o usuário digita em número"),
        nota("Perguntar e responder", [
            ("<code>input(\"texto\")</code>", "input", "Mostra o texto, espera o usuário digitar e devolve o que foi digitado, sempre como <code>str</code>."),
            ("<code>int(input(...))</code>", "inteiro do input", "Lê e já converte para inteiro. Para decimais, <code>float(input(...))</code>."),
            ("<code>f\"Olá, {nome}\"</code>", "f-string", "Texto com lacunas: o que está entre chaves é calculado e encaixado."),
            ("<code>{valor:.2f}</code>", "duas casas", "Dentro da f-string, formata o número com 2 casas decimais."),
        ]),
        passos("Calculadora de gorjeta", [
            ("<code>conta = float(input(\"Valor da conta: \"))</code>", "Lê o texto e converte para número com casas decimais."),
            ("<code>gorjeta = conta * 0.10</code>", "10% do valor."),
            ("<code>print(f\"Gorjeta: {gorjeta:.2f}\")</code>", "A f-string encaixa o valor já com duas casas."),
        ], fim="Neste site, o <code>input()</code> é simulado: cada exercício já traz as respostas que “o usuário digitaria”."),
        cod("Cartão de boas-vindas", "Leia o nome e a idade com <code>input()</code> e imprima: <b>Olá, Ana! Em 5 anos você terá 30 anos.</b> (as entradas simuladas são Ana e 25).",
            '''
nome = input("Seu nome: ")
idade = input("Sua idade: ")

print("Olá")
''',
            [("Mensagem correta", "assert saida.strip().splitlines()[-1] == 'Olá, Ana! Em 5 anos você terá 30 anos.', f'última linha: {saida.strip().splitlines()[-1]!r}'")],
            '''
nome = input("Seu nome: ")
idade = int(input("Sua idade: "))

print(f"Olá, {nome}! Em 5 anos você terá {idade + 5} anos.")
''', ["Converta a idade: <code>int(input(...))</code>.", "Dentro das chaves pode haver uma conta: <code>{idade + 5}</code>."], entradas=["Ana", "25"]),
        cod("Preço com desconto", "A entrada simulada é o preço <b>80</b>. Imprima o preço com 15% de desconto, com duas casas: <b>Total: 68.00</b>",
            '''
preco = input("Preço: ")
''',
            [("Total com duas casas", "assert saida.strip().splitlines()[-1] == 'Total: 68.00', f'última linha: {saida.strip().splitlines()[-1]!r}'")],
            '''
preco = float(input("Preço: "))
total = preco * 0.85
print(f"Total: {total:.2f}")
''', ["15% de desconto é multiplicar por 0.85.", "<code>{total:.2f}</code> mostra duas casas."], entradas=["80"], rot="Mão no código · nível 2"),
        erros([
            ("Fazer contas direto com o resultado do <code>input</code>.", "Converta antes: <code>int(input(...))</code> ou <code>float(input(...))</code>."),
            ("Esquecer o <code>f</code> antes das aspas.", "Sem o <code>f</code>, as chaves aparecem como texto: <code>Olá, {nome}</code>."),
            ("<code>int(\"3.5\")</code>", "Dá erro: texto com ponto não vira inteiro direto. Use <code>float(\"3.5\")</code>."),
        ]),
        ponte("Entrada e saída num chatbot",
              "<p>Um chatbot é este mesmo ciclo em laço: <code>input</code> lê a sua mensagem, o modelo processa e <code>print</code> mostra a resposta. O <i>prompt</i> que você envia a um LLM quase sempre é montado com f-strings: <code>f\"Resuma o texto: {texto}\"</code>.</p>"),
        quiz([
            ("Qual é o tipo do valor devolvido por <code>input()</code>?", ["int", "str", "Depende do que for digitado"], 1, "Sempre <code>str</code>, mesmo que o usuário digite números."),
            ("O que imprime <code>print(f\"{2 + 3} itens\")</code>?", ["{2 + 3} itens", "5 itens", "2 + 3 itens"], 1, "A f-string calcula o que está entre chaves."),
            ("Como mostrar <code>x = 3.14159</code> com duas casas?", ["<code>f\"{x:.2f}\"</code>", "<code>f\"{x:2}\"</code>", "<code>f\"{x}.2\"</code>"], 0, "<code>:.2f</code> = duas casas decimais."),
        ]),
    ],
    ["<code>input()</code> sempre devolve texto: converta com <code>int()</code> ou <code>float()</code>.", "f-strings montam mensagens com lacunas entre chaves.", "<code>{x:.2f}</code> formata com duas casas decimais."],
    "Condicionais: fazer o programa tomar decisões.",
    livro=("PYDOC:inputoutput", "Seção 7.1, “Refinando a formatação de saída”", "Que outras formas de formatar texto o tutorial mostra além da f-string?"))

AULAS["Condicionais (if, elif, else)"] = aula(
    35,
    "“Se a nota for 7 ou mais, aprovado; senão, recuperação.” Decidir é a primeira coisa inteligente que um programa faz, e uma árvore de decisão de machine learning nada mais é do que um monte desses <i>se</i> empilhados.",
    ["escrever decisões com <code>if</code>, <code>elif</code> e <code>else</code>;", "combinar condições com <code>and</code>, <code>or</code> e <code>not</code>;", "evitar o erro clássico da ordem dos testes."],
    ["Variáveis, tipos e <code>input</code>."],
    [
        chute("O que esse código imprime?", ["A", "B", "A e depois B"], 0,
              ["Isso! Assim que um teste dá certo, o Python executa aquele bloco e <b>pula todos os outros</b>.", "85 também é maior que 70, mas o <code>elif</code> só é testado se o <code>if</code> de cima falhar.", "Numa cadeia <code>if/elif/else</code>, só <b>um</b> bloco roda."],
              "Por isso a <b>ordem</b> dos testes importa: do mais exigente para o menos exigente.",
              cod='nota = 85\nif nota >= 80:\n    print("A")\nelif nota >= 70:\n    print("B")\nelse:\n    print("C")'),
        concreto("O semáforo", "<p><b>Se</b> estiver verde, siga. <b>Senão, se</b> estiver amarelo, reduza. <b>Senão</b>, pare. Três caminhos, e você segue exatamente um. É a estrutura <code>if / elif / else</code>.</p>"),
        crianca("<p>É o jogo do “<b>se chover, levo guarda-chuva; senão, vou de boné</b>”. O programa olha a condição, responde sim ou não, e escolhe o caminho. O recuo (os espaços no começo da linha) mostra o que pertence a cada caminho.</p>"),
        ver("como o professor desenha os caminhos (os “desvios”) de uma condição"),
        nota("A gramática da decisão", [
            ("<code>if condição:</code>", "se", "Roda o bloco recuado só quando a condição é verdadeira."),
            ("<code>elif outra:</code>", "senão, se", "Só é testada se as anteriores falharam. Pode haver várias."),
            ("<code>else:</code>", "senão", "Roda quando nenhuma condição acima deu certo. Não tem condição."),
            ("<code>== != &gt; &lt; &gt;= &lt;=</code>", "comparações", "Devolvem <code>True</code> ou <code>False</code>. Igualdade é com <b>dois</b> sinais: <code>==</code>."),
            ("<code>and</code> / <code>or</code> / <code>not</code>", "e / ou / não", "<code>and</code>: as duas precisam ser verdade. <code>or</code>: basta uma. <code>not</code>: inverte."),
        ]),
        passos("Classificando uma temperatura", [
            ("<code>t = 31</code>", "O valor a classificar."),
            ("Teste 1: <code>t &gt;= 30</code>? Sim.", "Entra no primeiro bloco e imprime “quente”."),
            ("Os <code>elif</code> e o <code>else</code> são pulados.", "A cadeia termina no primeiro teste verdadeiro."),
            ("Com <code>t = 18</code>: falha em <code>&gt;= 30</code>, falha em <code>&gt;= 20</code>, cai no <code>else</code>: “frio”.", "O <code>else</code> é a rede de segurança."),
        ], corpo=py('if t >= 30:\n    print("quente")\nelif t >= 20:\n    print("agradável")\nelse:\n    print("frio")')),
        ordem("Monte o verificador de maioridade",
              ['idade = 17', 'if idade >= 18:', '    print("Pode entrar")', 'else:', '    print("Volte em alguns anos")'],
              corpo="<p>Coloque as linhas na ordem certa (o recuo já está pronto).</p>",
              exp="<p>Primeiro a variável, depois o teste. O bloco recuado logo abaixo de cada <code>if</code>/<code>else</code> é o que roda naquele caminho.</p>"),
        cod("Filtro de confiança", "Um classificador devolveu <code>prob</code> (0 a 1). Imprima <b>spam</b> se for maior ou igual a 0.8, <b>revisar</b> se estiver entre 0.5 e 0.8, e <b>ok</b> caso contrário. A função é testada com vários valores.",
            '''
def classificar(prob):
    # use if / elif / else e devolva "spam", "revisar" ou "ok"
    return "ok"

print(classificar(0.9), classificar(0.6), classificar(0.1))
''',
            [("0.9 é spam", "assert classificar(0.9) == 'spam'"), ("0.8 (na fronteira) é spam", "assert classificar(0.8) == 'spam', 'use >= 0.8'"),
             ("0.6 é revisar", "assert classificar(0.6) == 'revisar'"), ("0.5 é revisar", "assert classificar(0.5) == 'revisar', 'use >= 0.5'"), ("0.1 é ok", "assert classificar(0.1) == 'ok'")],
            '''
def classificar(prob):
    if prob >= 0.8:
        return "spam"
    elif prob >= 0.5:
        return "revisar"
    else:
        return "ok"

print(classificar(0.9), classificar(0.6), classificar(0.1))
''', ["Teste primeiro o caso mais exigente (<code>&gt;= 0.8</code>).", "No <code>elif</code>, basta <code>prob &gt;= 0.5</code>: se chegou ali, já sabemos que é menor que 0.8."]),
        erros([
            ("<code>if x = 5:</code>", "Um sinal só é atribuição. Comparar é <code>==</code>."),
            ("Testar primeiro o caso mais fraco: <code>if nota &gt;= 5 ... elif nota &gt;= 7</code>.", "O segundo teste nunca roda: todo 7 já é ≥ 5. Comece pelo mais exigente."),
            ("Esquecer os dois-pontos ou o recuo.", "Toda linha de <code>if</code>, <code>elif</code> e <code>else</code> termina em <code>:</code>, e o bloco fica recuado 4 espaços."),
            ("<code>if idade &gt; 18 or 65:</code>", "Cada lado do <code>or</code> precisa ser uma comparação completa: <code>idade &gt; 18 or idade &gt; 65</code>."),
        ]),
        ponte("Do <code>if</code> à árvore de decisão",
              "<p>Na Fase 3 você vai treinar <b>árvores de decisão</b>: modelos que aprendem sozinhos uma cadeia de perguntas do tipo “renda &gt; 5000? idade &lt; 30?”. A diferença é que, lá, quem escolhe as perguntas e os limites são os dados, não você.</p>"),
        quiz([
            ("Numa cadeia <code>if / elif / else</code>, quantos blocos rodam?", ["Todos os verdadeiros.", "No máximo um.", "Sempre dois."], 1, "O primeiro teste verdadeiro encerra a cadeia."),
            ("<code>x = 5</code>. Quanto vale <code>x &gt; 3 and x &lt; 4</code>?", ["True", "False", "Erro"], 1, "<code>and</code> exige as duas: 5 &gt; 3 é verdade, mas 5 &lt; 4 não."),
            ("Qual linha está correta?", ["<code>if x == 10:</code>", "<code>if x = 10:</code>", "<code>if (x == 10)</code>"], 0, "Dois sinais de igual e dois-pontos no final."),
        ]),
    ],
    ["<code>if</code> testa, <code>elif</code> dá alternativas e <code>else</code> pega o resto; só um bloco roda.", "Comparar é <code>==</code>; combine com <code>and</code>, <code>or</code> e <code>not</code>.", "Ordene os testes do mais exigente para o menos exigente."],
    "Laços: repetir sem copiar e colar.",
    livro=("ATBS:2", "Capítulo 2, “Flow Control”, até “else Statements”", "Como o livro desenha o fluxo de um if/else?"))

AULAS["Funções, parâmetros e retorno"] = aula(
    40,
    "Toda vez que você escreve <code>print(...)</code> está usando uma função que alguém criou. Hoje você passa para o outro lado do balcão: empacotar um pedaço de código, dar um nome a ele e reutilizar para sempre.",
    ["definir funções com <code>def</code> e chamá-las;", "passar parâmetros, inclusive com valor padrão;", "entender a diferença entre <code>return</code> e <code>print</code>."],
    ["Condicionais e laços."],
    [
        chute("O que esse código imprime?", ["8", "None", "Nada"], 1,
              ["A função até calcula 8, mas não <b>devolve</b> o resultado: falta o <code>return</code>.", "Isso! Sem <code>return</code>, a função devolve <code>None</code> (“nada”). O 8 foi calculado e jogado fora.", "O <code>print</code> de fora roda e mostra o que a função devolveu: <code>None</code>."],
              "<code>return</code> é a função <b>entregando</b> o resultado para quem chamou.",
              cod='def dobro(x):\n    x * 2\n\nprint(dobro(4))'),
        concreto("O liquidificador", "<p>Você coloca ingredientes (<b>parâmetros</b>), aperta o botão (<b>chama</b> a função) e recebe a vitamina (<b>retorno</b>). Não precisa saber como o motor funciona, e pode usar quantas vezes quiser com ingredientes diferentes.</p>"),
        crianca("<p>Uma função é uma <b>receita com nome</b>. Em vez de explicar toda vez como se faz brigadeiro, você só diz “faz um brigadeiro”. E a receita pode ter lacunas: “faz um brigadeiro de <b>{sabor}</b>”.</p>"),
        ver("a diferença que o professor mostra entre uma função que imprime e uma que retorna"),
        nota("Anatomia de uma função", [
            ("<code>def nome(a, b):</code>", "definir", "Cria a função. <code>a</code> e <code>b</code> são os parâmetros: nomes para os valores que vão chegar."),
            ("<code>return valor</code>", "retornar", "Entrega o resultado e <b>encerra</b> a função na hora."),
            ("<code>nome(2, 3)</code>", "chamar", "Executa a função com esses valores (os argumentos)."),
            ("<code>def f(x, n=2):</code>", "valor padrão", "Se quem chama não passar <code>n</code>, ele vale 2."),
            ("<code>\"\"\"texto\"\"\"</code>", "docstring", "Primeira linha dentro da função: explica o que ela faz."),
        ]),
        passos("Acompanhando uma chamada", [
            ("<code>def media(a, b): return (a + b) / 2</code>", "Só <b>define</b>. Nada roda ainda."),
            ("<code>r = media(6, 8)</code>", "Chamada: <code>a</code> recebe 6 e <code>b</code> recebe 8."),
            ("Dentro: <code>(6 + 8) / 2 = 7.0</code>, e o <code>return</code> entrega 7.0.", "O valor volta para o lugar onde a função foi chamada."),
            ("<code>r</code> passa a valer 7.0.", "Agora dá para usar o resultado em outras contas."),
        ], fim="Função que <b>retorna</b> pode ser combinada com outras; função que só <b>imprime</b> não."),
        cod("Acurácia de um modelo", "Complete a função: ela recebe quantos acertos e o total de exemplos e <b>devolve</b> a porcentagem de acerto (de 0 a 100).",
            '''
def acuracia(acertos, total):
    """Devolve a porcentagem de acertos."""
    pass

print(acuracia(45, 50))
''',
            [("45 de 50 dá 90.0", "assert acuracia(45, 50) == 90.0, f'deu {acuracia(45, 50)!r}'"), ("1 de 4 dá 25.0", "assert acuracia(1, 4) == 25.0"),
             ("Devolve (não só imprime)", "assert acuracia(3, 3) is not None, 'faltou o return'")],
            '''
def acuracia(acertos, total):
    """Devolve a porcentagem de acertos."""
    return acertos / total * 100

print(acuracia(45, 50))
''', ["Divida e multiplique por 100, e não esqueça o <code>return</code>."]),
        cod("Saudação com valor padrão", "Crie <code>saudar(nome, periodo=\"dia\")</code> que devolve, por exemplo, <b>Bom dia, Ana!</b>. Se o período for \"noite\" ou \"tarde\", use <b>Boa</b>.",
            '''
def saudar(nome, periodo="dia"):
    return ""

print(saudar("Ana"))
print(saudar("Leo", "noite"))
''',
            [("Padrão: Bom dia", "assert saudar('Ana') == 'Bom dia, Ana!', f'deu {saudar(\"Ana\")!r}'"), ("Boa noite", "assert saudar('Leo', 'noite') == 'Boa noite, Leo!'"), ("Boa tarde", "assert saudar('Bia', periodo='tarde') == 'Boa tarde, Bia!'")],
            '''
def saudar(nome, periodo="dia"):
    inicio = "Bom" if periodo == "dia" else "Boa"
    return f"{inicio} {periodo}, {nome}!"

print(saudar("Ana"))
print(saudar("Leo", "noite"))
''', ["Decida entre “Bom” e “Boa” com um <code>if</code>.", "Monte o texto com f-string."], rot="Mão no código · nível 2"),
        erros([
            ("Usar <code>print</code> onde deveria haver <code>return</code>.", "<code>print</code> só mostra na tela. Se outra parte do programa precisa do valor, use <code>return</code>."),
            ("Código depois do <code>return</code>.", "Nunca roda: o <code>return</code> encerra a função."),
            ("Definir a função e esquecer de chamar.", "<code>def</code> só ensina a receita. Para cozinhar, é preciso escrever <code>nome(...)</code>."),
            ("Tentar usar fora da função uma variável criada dentro dela.", "Variáveis internas somem quando a função termina (escopo local). Devolva o valor com <code>return</code>."),
        ]),
        ponte("Tudo em IA é função chamando função",
              "<p><code>modelo.fit(X, y)</code>, <code>tokenizer.encode(texto)</code>, <code>loss.backward()</code>: bibliotecas de IA são coleções de funções. Uma rede neural inteira é uma função enorme: recebe números, devolve números. E <code>def treinar(modelo, dados, epocas=10)</code> é exatamente o que você escreveu hoje.</p>"),
        quiz([
            ("O que uma função devolve quando não tem <code>return</code>?", ["0", "<code>None</code>", "Dá erro"], 1, "<code>None</code> é o “nada” do Python."),
            ("Em <code>def f(a, b=10)</code>, quanto vale <code>f(1)</code> para <code>b</code>?", ["1", "10", "Erro: falta argumento"], 1, "<code>b</code> usa o valor padrão."),
            ("Qual a vantagem de <code>return</code> sobre <code>print</code>?", ["É mais rápido.", "O valor pode ser guardado e reutilizado.", "Mostra o resultado colorido."], 1, "O valor retornado pode ir para uma variável, outra função, um teste..."),
        ]),
    ],
    ["<code>def</code> cria a função; ela só roda quando é chamada.", "Parâmetros recebem os valores; <code>return</code> devolve o resultado e encerra.", "Valores padrão tornam parâmetros opcionais."],
    "Listas: guardar muitos valores numa variável só.",
    livro=("ATBS:3", "Capítulo 3, “Functions”", "Como o livro explica escopo local e global?"))

AULAS["Listas e fatiamento"] = aula(
    40,
    "Uma variável guarda um valor. Mas e as notas de 40 alunos? Os 1.000 preços de um dataset? Listas guardam muitos valores em ordem, e fatiar listas é o gesto mais repetido em ciência de dados.",
    ["criar listas, acessar por índice e alterar itens;", "fatiar com <code>lista[início:fim]</code>;", "usar <code>append</code>, <code>len</code>, <code>in</code> e <code>sort</code>."],
    ["Laços e funções."],
    [
        chute("O que esse código imprime?", ["a", "b", "Dá erro"], 1,
              ["O primeiro item é o de índice <b>0</b>, não 1.", "Isso! A contagem começa no zero: <code>letras[0]</code> é “a”, <code>letras[1]</code> é “b”.", "O índice 1 existe: a lista tem 3 itens, com índices 0, 1 e 2."],
              "Índices começam em 0. O último item é <code>lista[-1]</code>.",
              cod='letras = ["a", "b", "c"]\nprint(letras[1])'),
        concreto("Uma fila de armários numerados", "<p>Uma lista é uma fileira de armários: cada um guarda uma coisa e tem um número na porta. A pegadinha: a numeração começa no <b>0</b>.</p>"),
        crianca("<p>Fatiar é pedir “me dá do armário 1 <b>até antes</b> do 3”. Você recebe os armários 1 e 2. É a mesma regra do <code>range</code>: o começo entra, o fim não.</p>"),
        ver("como o professor mostra os índices positivos e negativos de uma lista"),
        nota("O essencial das listas", [
            ("<code>v = [10, 20, 30]</code>", "lista", "Valores entre colchetes, separados por vírgula."),
            ("<code>v[0]</code> / <code>v[-1]</code>", "índice", "Primeiro e último item."),
            ("<code>v[1:3]</code>", "fatia de 1 até 3", "Itens de índice 1 e 2 (o fim não entra). <code>v[:2]</code> são os dois primeiros; <code>v[-2:]</code>, os dois últimos."),
            ("<code>v.append(x)</code>", "acrescentar", "Põe <code>x</code> no final."),
            ("<code>len(v)</code> / <code>x in v</code>", "tamanho / pertence", "Quantos itens há; se <code>x</code> está na lista."),
        ]),
        passos("Fatiando <code>v = [5, 8, 2, 9, 4]</code>", [
            ("<code>v[1:4]</code>", "Índices 1, 2 e 3: <code>[8, 2, 9]</code>."),
            ("<code>v[:2]</code>", "Do começo até antes do 2: <code>[5, 8]</code>."),
            ("<code>v[-2:]</code>", "Os dois últimos: <code>[9, 4]</code>."),
            ("<code>v[::2]</code>", "Pulando de 2 em 2: <code>[5, 2, 4]</code>."),
        ], fim="Fatiar <b>cria uma lista nova</b>; a original não muda."),
        cod("Treino e teste", "Separe a lista: os <b>8 primeiros</b> itens vão para <code>treino</code> e os <b>2 últimos</b> para <code>teste</code>. É assim que se separam dados em machine learning.",
            '''
dados = [3, 7, 1, 9, 4, 6, 2, 8, 5, 0]

treino = []
teste = []

print(treino, teste)
''',
            [("treino tem os 8 primeiros", "assert treino == [3, 7, 1, 9, 4, 6, 2, 8], f'treino = {treino}'"), ("teste tem os 2 últimos", "assert teste == [5, 0], f'teste = {teste}'"),
             ("A lista original continua inteira", "assert len(dados) == 10")],
            '''
dados = [3, 7, 1, 9, 4, 6, 2, 8, 5, 0]

treino = dados[:8]
teste = dados[8:]

print(treino, teste)
''', ["<code>dados[:8]</code> pega do começo até antes do índice 8.", "<code>dados[8:]</code> pega do índice 8 até o fim."]),
        cod("Maior nota", "Sem usar <code>max()</code>, percorra a lista com um <code>for</code> e imprima a maior nota.",
            '''
notas = [6.5, 8.0, 4.5, 9.5, 7.0]
maior = notas[0]

# percorra a lista e atualize "maior"

print(maior)
''',
            [("Imprime 9.5", "assert saida.strip() == '9.5', f'saiu {saida.strip()!r}'")],
            '''
notas = [6.5, 8.0, 4.5, 9.5, 7.0]
maior = notas[0]

for n in notas:
    if n > maior:
        maior = n

print(maior)
''', ["Para cada nota: se ela for maior que <code>maior</code>, atualize."], rot="Mão no código · nível 2"),
        erros([
            ("<code>v[len(v)]</code>", "IndexError: o último índice é <code>len(v) - 1</code>. Use <code>v[-1]</code>."),
            ("<code>b = a</code> achando que copiou a lista.", "As duas variáveis apontam para a <b>mesma</b> lista: mudar <code>b</code> muda <code>a</code>. Para copiar: <code>b = a[:]</code> ou <code>a.copy()</code>."),
            ("<code>v = v.append(3)</code>", "<code>append</code> altera a lista e devolve <code>None</code>. Escreva só <code>v.append(3)</code>."),
            ("Esperar que <code>v[1:3]</code> inclua o índice 3.", "O fim nunca entra."),
        ]),
        ponte("Fatias em dados e em IA",
              "<p><code>X[:800]</code> para treino e <code>X[800:]</code> para teste; <code>texto[:512]</code> para cortar no limite de tokens; <code>batch = dados[i:i+32]</code> para montar lotes. NumPy, Pandas e PyTorch usam exatamente essa mesma notação de fatias, em mais dimensões.</p>"),
        quiz([
            ("<code>v = [4, 5, 6, 7]</code>. Quanto vale <code>v[1:3]</code>?", ["[5, 6]", "[5, 6, 7]", "[4, 5, 6]"], 0, "Índices 1 e 2; o 3 não entra."),
            ("Como pegar o último item de qualquer lista?", ["<code>v[len(v)]</code>", "<code>v[-1]</code>", "<code>v[last]</code>"], 1, "Índices negativos contam do fim."),
            ("Depois de <code>a = [1, 2]</code>, <code>b = a</code>, <code>b.append(3)</code>, quanto vale <code>a</code>?", ["[1, 2]", "[1, 2, 3]", "Erro"], 1, "<code>a</code> e <code>b</code> são a mesma lista."),
        ]),
    ],
    ["Listas guardam itens em ordem; os índices começam em 0.", "<code>v[início:fim]</code> fatia sem incluir o fim e cria uma lista nova.", "<code>append</code>, <code>len</code> e <code>in</code> resolvem a maior parte do dia a dia."],
    "Dicionários: procurar pelo nome em vez da posição.",
    livro=("ATBS:4", "Capítulo 4, “Lists”", "Que exemplo o livro usa para mostrar referências a listas?"))

AULAS["Dicionários"] = aula(
    35,
    "Numa lista você procura pela <b>posição</b>. Num dicionário, pelo <b>nome</b>: <code>preco[\"café\"]</code>. É a estrutura que mais se parece com o mundo real, e é o formato dos dados que toda API de IA devolve.",
    ["criar dicionários e acessar valores pela chave;", "adicionar, alterar e percorrer chaves e valores;", "usar <code>.get()</code> para não quebrar com chave ausente."],
    ["Listas e laços."],
    [
        chute("O que esse código imprime?", ["1", "2", "3"], 2,
              ["O dicionário nasce com 2 chaves, mas ganha mais uma.", "Antes da terceira linha, sim. Depois, há uma chave nova.", "Isso! Atribuir a uma chave que não existe <b>cria</b> a chave."],
              "Em dicionários, <code>d[chave] = valor</code> serve tanto para criar quanto para alterar.",
              cod='estoque = {"café": 10, "chá": 4}\nestoque["mate"] = 7\nprint(len(estoque))'),
        concreto("A agenda de contatos", "<p>Você não procura “o contato número 37”. Procura “<b>Ana</b>” e o telefone aparece. O nome é a <b>chave</b>; o telefone é o <b>valor</b>.</p>"),
        crianca("<p>Um dicionário é uma estante de gavetas com <b>etiquetas escritas</b> em vez de números. Você abre a gaveta “brinquedos” e pega o que tem dentro. Duas gavetas não podem ter a mesma etiqueta.</p>"),
        ver("como o professor acessa e altera um valor pela chave"),
        nota("Chave e valor", [
            ("<code>d = {\"nome\": \"Ana\", \"idade\": 30}</code>", "dicionário", "Pares <code>chave: valor</code> entre chaves."),
            ("<code>d[\"nome\"]</code>", "valor da chave", "Devolve “Ana”. Se a chave não existir, dá <code>KeyError</code>."),
            ("<code>d.get(\"email\", \"-\")</code>", "pegar com segurança", "Devolve o valor ou o padrão (“-”) se a chave não existir."),
            ("<code>for k, v in d.items():</code>", "percorrer", "Entrega chave e valor a cada volta."),
            ("<code>\"nome\" in d</code>", "a chave existe?", "<code>True</code> ou <code>False</code>."),
        ]),
        passos("Contando palavras", [
            ("<code>contagem = {}</code>", "Começa vazio."),
            ("Para cada palavra do texto: <code>contagem[p] = contagem.get(p, 0) + 1</code>", "Se a palavra é nova, <code>get</code> devolve 0; senão, o total até agora."),
            ("Depois de “a casa a”: <code>{\"a\": 2, \"casa\": 1}</code>", "Cada chave aparece uma vez só, com sua contagem."),
        ], fim="Esse padrão “dicionário como contador” aparece em todo lugar, de análise de texto a tokenizadores."),
        cod("Contador de palavras", "Complete a função para devolver um dicionário com quantas vezes cada palavra aparece.",
            '''
def contar(frase):
    contagem = {}
    for palavra in frase.split():
        pass  # atualize a contagem
    return contagem

print(contar("o gato viu o rato"))
''',
            [("Conta 'o' duas vezes", "assert contar('o gato viu o rato')['o'] == 2"), ("Conta cada palavra", "assert contar('a b a b a') == {'a': 3, 'b': 2}, f'deu {contar(\"a b a b a\")}'"),
             ("Frase vazia dá dicionário vazio", "assert contar('') == {}")],
            '''
def contar(frase):
    contagem = {}
    for palavra in frase.split():
        contagem[palavra] = contagem.get(palavra, 0) + 1
    return contagem

print(contar("o gato viu o rato"))
''', ["<code>contagem.get(palavra, 0)</code> devolve 0 quando a palavra ainda não está lá."]),
        cod("Lendo a resposta de uma API", "A variável <code>resposta</code> imita o que uma API de LLM devolve. Imprima só o texto gerado e, na linha de baixo, o total de tokens.",
            '''
resposta = {
    "modelo": "mini-1",
    "escolhas": [{"texto": "Olá! Como posso ajudar?", "motivo": "fim"}],
    "uso": {"entrada": 12, "saida": 8},
}

''',
            [("Primeira linha é o texto", "assert saida.splitlines()[0] == 'Olá! Como posso ajudar?', f'saiu {saida.splitlines()[0]!r}'"), ("Segunda linha é 20", "assert saida.splitlines()[1].strip() == '20'")],
            '''
resposta = {
    "modelo": "mini-1",
    "escolhas": [{"texto": "Olá! Como posso ajudar?", "motivo": "fim"}],
    "uso": {"entrada": 12, "saida": 8},
}

print(resposta["escolhas"][0]["texto"])
print(resposta["uso"]["entrada"] + resposta["uso"]["saida"])
''', ["<code>resposta[\"escolhas\"]</code> é uma <b>lista</b>: pegue o item <code>[0]</code> e depois a chave <code>\"texto\"</code>."], rot="Mão no código · nível 2 · ponte para IA"),
        erros([
            ("<code>d[\"email\"]</code> quando a chave não existe.", "<code>KeyError</code>. Use <code>d.get(\"email\")</code> ou teste com <code>in</code> antes."),
            ("Usar lista como chave.", "Chaves precisam ser imutáveis: texto, número ou tupla."),
            ("Esperar duas chaves iguais.", "A segunda atribuição <b>substitui</b> a primeira."),
        ]),
        ponte("JSON é dicionário",
              "<p>Configurações de treino, respostas de APIs, datasets do Hugging Face, parâmetros de um modelo: tudo chega como <b>JSON</b>, que em Python vira dicionários e listas aninhados. Saber navegar por <code>dados[\"a\"][0][\"b\"]</code> é metade do trabalho de integrar um LLM.</p>"),
        quiz([
            ("Como ler uma chave que talvez não exista, sem erro?", ["<code>d[chave]</code>", "<code>d.get(chave)</code>", "<code>d.find(chave)</code>"], 1, "<code>get</code> devolve <code>None</code> (ou o padrão) em vez de quebrar."),
            ("O que faz <code>d[\"x\"] = 5</code> se <code>\"x\"</code> já existe?", ["Dá erro.", "Substitui o valor antigo.", "Cria uma segunda chave x."], 1, "Chaves são únicas."),
            ("O que <code>for k, v in d.items()</code> entrega a cada volta?", ["Só as chaves.", "Chave e valor.", "Só os valores."], 1, "<code>items()</code> entrega os pares."),
        ]),
    ],
    ["Dicionário associa chaves a valores; a busca é pelo nome.", "<code>d[k] = v</code> cria ou altera; <code>d.get(k, padrão)</code> lê com segurança.", "JSON vira dicionários e listas aninhados."],
    "Tuplas e conjuntos: quando a lista não é a melhor escolha.",
    livro=("ATBS:5", "Capítulo 5, “Dictionaries and Structuring Data”", "Que jogo o livro modela com dicionários?"))

AULAS["Tuplas e conjuntos"] = aula(
    30,
    "Coordenadas de um ponto não deveriam mudar por acidente. E-mails de uma lista de envio não deveriam se repetir. Para esses dois casos, o Python tem ferramentas próprias: tuplas e conjuntos.",
    ["usar tuplas para dados que não mudam e desempacotá-las;", "usar conjuntos para eliminar repetidos;", "fazer união, interseção e diferença."],
    ["Listas e dicionários."],
    [
        chute("O que esse código imprime?", ["5", "3", "Dá erro"], 1,
              ["A lista tem 5 itens, mas o conjunto elimina os repetidos.", "Isso! Um conjunto guarda cada valor <b>uma vez só</b>: {1, 2, 3}.", "<code>set()</code> aceita qualquer lista."],
              "Converter para <code>set</code> é o jeito mais rápido de tirar duplicatas.",
              cod='nums = [1, 2, 2, 3, 3]\nprint(len(set(nums)))'),
        concreto("RG e lista de convidados", "<p>Seu <b>RG</b> tem campos fixos numa ordem fixa: nome, data, número. Isso é uma <b>tupla</b>. A <b>lista de convidados</b> de uma festa não tem ordem e ninguém entra duas vezes: isso é um <b>conjunto</b>.</p>"),
        crianca("<p>Tupla é uma lista <b>plastificada</b>: dá para ler, não dá para riscar. Conjunto é um saco de figurinhas <b>sem repetidas</b>: se você tentar pôr uma que já tem, nada acontece.</p>"),
        nota("Parênteses e chaves", [
            ("<code>p = (3, 4)</code>", "tupla", "Como lista, mas imutável: <code>p[0] = 9</code> dá erro."),
            ("<code>x, y = p</code>", "desempacotar", "Distribui os itens em variáveis: <code>x = 3</code>, <code>y = 4</code>."),
            ("<code>s = {1, 2, 3}</code>", "conjunto", "Sem ordem e sem repetidos. Conjunto vazio é <code>set()</code>, não <code>{}</code>."),
            ("<code>a | b</code>, <code>a &amp; b</code>, <code>a - b</code>", "união, interseção, diferença", "Tudo; só o que está nos dois; o que está em <code>a</code> e não em <code>b</code>."),
        ]),
        passos("Quem fez os dois cursos?", [
            ("<code>python = {\"Ana\", \"Bia\", \"Caio\"}</code> e <code>sql = {\"Bia\", \"Caio\", \"Davi\"}</code>", "Dois conjuntos de alunos."),
            ("<code>python &amp; sql</code>", "Interseção: <code>{\"Bia\", \"Caio\"}</code>."),
            ("<code>python - sql</code>", "Só Python: <code>{\"Ana\"}</code>."),
            ("<code>python | sql</code>", "Todos, sem repetir: 4 nomes."),
        ]),
        cod("Vocabulário de um texto", "Devolva quantas palavras <b>diferentes</b> há na frase, ignorando maiúsculas e minúsculas.",
            '''
def vocabulario(frase):
    return 0

print(vocabulario("O gato e o rato"))
''',
            [("“O gato e o rato” tem 4", "assert vocabulario('O gato e o rato') == 4, f'deu {vocabulario(\"O gato e o rato\")}'"), ("Repetidas contam uma vez", "assert vocabulario('a a a b') == 2"), ("Vazia dá 0", "assert vocabulario('') == 0")],
            '''
def vocabulario(frase):
    return len(set(frase.lower().split()))

print(vocabulario("O gato e o rato"))
''', ["<code>frase.lower().split()</code> dá a lista de palavras em minúsculas.", "<code>set(...)</code> tira as repetidas; <code>len</code> conta."]),
        cod("Desempacotando resultados", "A função deve devolver <b>duas coisas</b> de uma vez: o menor e o maior valor da lista, como uma tupla.",
            '''
def extremos(valores):
    return 0, 0

menor, maior = extremos([4, 9, 1, 7])
print(menor, maior)
''',
            [("Devolve (1, 9)", "assert extremos([4, 9, 1, 7]) == (1, 9), f'deu {extremos([4, 9, 1, 7])}'"), ("Funciona com um item", "assert extremos([5]) == (5, 5)")],
            '''
def extremos(valores):
    return min(valores), max(valores)

menor, maior = extremos([4, 9, 1, 7])
print(menor, maior)
''', ["<code>return a, b</code> devolve uma tupla."], rot="Mão no código · nível 2"),
        erros([
            ("<code>t = (5)</code> achando que é tupla.", "Isso é só o número 5. Tupla de um item precisa da vírgula: <code>(5,)</code>."),
            ("<code>vazio = {}</code> para criar um conjunto.", "<code>{}</code> é um dicionário vazio. Conjunto vazio: <code>set()</code>."),
            ("Esperar ordem num conjunto.", "Conjuntos não têm posição: <code>s[0]</code> dá erro."),
        ]),
        ponte("Onde aparecem em IA",
              "<p>O formato de um tensor é uma tupla: <code>(32, 3, 224, 224)</code>. Funções que devolvem várias coisas (<code>X_treino, X_teste = ...</code>) usam desempacotamento. E o <b>vocabulário</b> de um tokenizador nasce como um conjunto de pedaços de texto únicos.</p>"),
        quiz([
            ("Qual é a principal diferença entre lista e tupla?", ["Tupla não pode ser alterada.", "Tupla só guarda números.", "Tupla não tem índice."], 0, "Tuplas são imutáveis."),
            ("<code>{1, 2} &amp; {2, 3}</code> resulta em:", ["{1, 2, 3}", "{2}", "{1, 3}"], 1, "<code>&amp;</code> é interseção: o que está nos dois."),
            ("Como tirar os repetidos de uma lista <code>v</code>?", ["<code>v.unique()</code>", "<code>list(set(v))</code>", "<code>v - v</code>"], 1, "Vira conjunto (sem repetidos) e volta a ser lista."),
        ]),
    ],
    ["Tupla: sequência imutável, ótima para devolver vários valores.", "Conjunto: sem ordem e sem repetidos, com união, interseção e diferença.", "<code>set(lista)</code> remove duplicatas."],
    "List comprehension: criar listas em uma linha.",
    livro=("PYDOC:datastructures", "Seções 5.3 e 5.4 (tuplas e conjuntos)", "Que operações de conjunto o tutorial demonstra?"))

AULAS["List comprehension"] = aula(
    30,
    "Quatro linhas para criar uma lista nova a partir de outra viram <b>uma</b>. A list comprehension é o jeito “pythônico” de transformar e filtrar dados, e você vai vê-la em quase todo código de ciência de dados.",
    ["transformar uma lista com <code>[expressão for item in lista]</code>;", "filtrar com <code>if</code> no final;", "saber quando um <code>for</code> comum é mais claro."],
    ["Listas e laços <code>for</code>."],
    [
        chute("O que esse código imprime?", ["[1, 2, 3]", "[1, 4, 9]", "[2, 4, 6]"], 1,
              ["Essa é a lista original; a comprehension cria outra.", "Isso! Para cada <code>n</code>, calcula <code>n * n</code>: 1, 4 e 9.", "Isso seria <code>n * 2</code>. Aqui é <code>n * n</code>."],
              "Leia de trás para frente: “para cada n em nums, me dê n vezes n”.",
              cod='nums = [1, 2, 3]\nprint([n * n for n in nums])'),
        concreto("A esteira da fábrica", "<p>Peças entram por um lado, passam por uma máquina que faz <b>a mesma coisa em cada uma</b> (pinta, corta, descarta as defeituosas) e saem do outro lado numa caixa nova. A list comprehension é essa esteira escrita em uma linha.</p>"),
        crianca("<p>“Para cada fruta da cesta, <b>descasque</b>; mas só se estiver <b>madura</b>.” O que fazer, com o quê, e a condição. Três partes, uma frase.</p>"),
        nota("As três partes", [
            ("<code>[x * 2 for x in v]</code>", "transformar", "Lista nova com cada item dobrado."),
            ("<code>[x for x in v if x &gt; 0]</code>", "filtrar", "Só os itens que passam no teste."),
            ("<code>[x * 2 for x in v if x &gt; 0]</code>", "as duas coisas", "Filtra e transforma de uma vez."),
            ("<code>{k: v for ...}</code>", "dict comprehension", "A mesma ideia, criando um dicionário."),
        ]),
        passos("Do <code>for</code> comum à comprehension", [
            ("<code>pares = []</code> · <code>for n in nums:</code> · <code>if n % 2 == 0:</code> · <code>pares.append(n)</code>", "A versão longa: 4 linhas."),
            ("Pegue o que vai no <code>append</code>: <code>n</code>.", "Vira o começo da comprehension."),
            ("Copie o <code>for</code> e o <code>if</code> na mesma ordem.", "<code>[n for n in nums if n % 2 == 0]</code>"),
        ], fim="Se a linha ficar comprida ou com dois <code>if</code>, volte ao <code>for</code> comum: clareza vale mais."),
        cod("Normalizando notas", "Com uma list comprehension, crie <code>normalizadas</code> dividindo cada nota por 10.",
            '''
notas = [8, 5, 10, 7]

normalizadas = []

print(normalizadas)
''',
            [("Valores corretos", "assert normalizadas == [0.8, 0.5, 1.0, 0.7], f'deu {normalizadas}'")],
            '''
notas = [8, 5, 10, 7]

normalizadas = [n / 10 for n in notas]

print(normalizadas)
''', ["<code>[n / 10 for n in notas]</code>"]),
        cod("Limpando textos", "Crie <code>limpas</code> só com as palavras de mais de 2 letras, todas em minúsculas.",
            '''
palavras = ["O", "Modelo", "de", "IA", "Aprende", "com", "Dados"]

limpas = []

print(limpas)
''',
            [("Filtra e converte", "assert limpas == ['modelo', 'aprende', 'com', 'dados'], f'deu {limpas}'")],
            '''
palavras = ["O", "Modelo", "de", "IA", "Aprende", "com", "Dados"]

limpas = [p.lower() for p in palavras if len(p) > 2]

print(limpas)
''', ["Transformação: <code>p.lower()</code>. Filtro: <code>if len(p) &gt; 2</code>."], rot="Mão no código · nível 2"),
        erros([
            ("Pôr o <code>if</code> de filtro antes do <code>for</code>.", "O filtro vai no <b>final</b>: <code>[x for x in v if cond]</code>."),
            ("Usar comprehension só para imprimir.", "Ela serve para <b>criar listas</b>. Para efeitos como <code>print</code>, use <code>for</code> comum."),
            ("Empilhar três níveis numa linha.", "Legível é melhor que esperto. Quebre em etapas."),
        ]),
        ponte("Pré-processamento em uma linha",
              "<p><code>tokens = [t.lower() for t in texto.split() if t not in stopwords]</code> é a limpeza clássica de texto. <code>[len(d) for d in documentos]</code> mede cada documento antes de mandar a um LLM. Depois, NumPy e Pandas farão o mesmo em colunas inteiras, mas a ideia é esta.</p>"),
        quiz([
            ("<code>[x + 1 for x in [1, 2, 3] if x != 2]</code> resulta em:", ["[2, 4]", "[2, 3, 4]", "[1, 3]"], 0, "Filtra o 2, depois soma 1 a 1 e a 3."),
            ("Onde fica o <code>if</code> que filtra?", ["No começo.", "No final, depois do <code>for</code>.", "Dentro de parênteses."], 1, "<code>[expr for x in v if cond]</code>."),
            ("Quando preferir o <code>for</code> comum?", ["Sempre.", "Quando a lógica é longa ou tem vários passos.", "Nunca."], 1, "Comprehension é para transformações curtas."),
        ]),
    ],
    ["<code>[expressão for item in lista if condição]</code> cria uma lista nova.", "Leia como frase: “o que fazer, para cada quem, se o quê”.", "Lógica longa pede <code>for</code> comum."],
    "Orientação a objetos: organizar dados e funções juntos.",
    livro=("PYDOC:datastructures", "Seção 5.1.3, “Compreensões de lista”", "Que exemplo de comprehension aninhada o tutorial mostra?"))

AULAS["Orientação a objetos (classes, métodos, herança)"] = aula(
    45,
    "<code>modelo.treinar()</code>, <code>df.head()</code>, <code>lista.append()</code>: esse ponto no meio é orientação a objetos. Você já usa todos os dias. Hoje vai entender o que há por trás e criar os seus.",
    ["criar uma classe com <code>__init__</code>, atributos e métodos;", "entender o papel do <code>self</code>;", "reaproveitar código com herança."],
    ["Funções e dicionários."],
    [
        chute("O que esse código imprime?", ["0", "2", "Dá erro"], 1,
              ["O contador começa em 0, mas o método é chamado duas vezes.", "Isso! Cada chamada de <code>clicar()</code> soma 1 ao atributo <b>daquele objeto</b>.", "O código é válido: <code>self.total</code> existe desde o <code>__init__</code>."],
              "Um objeto <b>lembra</b> do próprio estado entre uma chamada e outra.",
              cod='class Contador:\n    def __init__(self):\n        self.total = 0\n    def clicar(self):\n        self.total += 1\n\nc = Contador()\nc.clicar()\nc.clicar()\nprint(c.total)'),
        concreto("A forma e os biscoitos", "<p>A <b>classe</b> é a forma de biscoito: define o formato. Os <b>objetos</b> são os biscoitos: cada um feito com a mesma forma, mas com seu próprio recheio. Mudar um biscoito não muda os outros.</p>"),
        crianca("<p>Pense num personagem de jogo. Ele <b>tem</b> coisas (vida, nome, nível): são os <b>atributos</b>. E <b>faz</b> coisas (pular, atacar): são os <b>métodos</b>. A classe é a ficha em branco; cada jogador preenche a sua.</p>"),
        ver("o exemplo de classe e objeto que o professor constrói"),
        nota("As peças de uma classe", [
            ("<code>class Nome:</code>", "classe", "O molde. Por convenção, nome com inicial maiúscula."),
            ("<code>def __init__(self, x):</code>", "construtor", "Roda sozinho quando o objeto é criado. Prepara os atributos."),
            ("<code>self.x = x</code>", "atributo", "Um dado guardado <b>dentro</b> do objeto."),
            ("<code>def metodo(self):</code>", "método", "Função que pertence à classe. O primeiro parâmetro é sempre <code>self</code>: o próprio objeto."),
            ("<code>class Filha(Mae):</code>", "herança", "A filha ganha tudo da mãe e pode acrescentar ou trocar métodos."),
        ]),
        passos("O que acontece em <code>c = Conta(\"Ana\", 100)</code>", [
            ("O Python cria um objeto vazio.", "Ainda sem atributos."),
            ("Chama <code>__init__(self, \"Ana\", 100)</code>.", "<code>self</code> é o objeto recém-criado."),
            ("<code>self.dono = \"Ana\"</code> e <code>self.saldo = 100</code>.", "Os dados ficam presos àquele objeto."),
            ("<code>c.depositar(50)</code> vira <code>Conta.depositar(c, 50)</code>.", "É assim que o método sabe em <b>qual</b> conta mexer."),
        ], corpo=py('class Conta:\n    def __init__(self, dono, saldo):\n        self.dono = dono\n        self.saldo = saldo\n    def depositar(self, valor):\n        self.saldo += valor')),
        cod("Uma classe para métricas", "Complete a classe <code>Placar</code>: <code>registrar(acertou)</code> recebe True/False, e <code>acuracia()</code> devolve a fração de acertos (0 se não houver registros).",
            '''
class Placar:
    def __init__(self):
        self.acertos = 0
        self.total = 0

    def registrar(self, acertou):
        pass

    def acuracia(self):
        return 0

p = Placar()
for r in [True, True, False, True]:
    p.registrar(r)
print(p.acuracia())
''',
            [("3 de 4 dá 0.75", "p2 = Placar()\nfor r in [True, True, False, True]: p2.registrar(r)\nassert p2.acuracia() == 0.75, f'deu {p2.acuracia()}'"),
             ("Sem registros dá 0", "assert Placar().acuracia() == 0"), ("Objetos são independentes", "a, b = Placar(), Placar()\na.registrar(True)\nassert b.total == 0")],
            '''
class Placar:
    def __init__(self):
        self.acertos = 0
        self.total = 0

    def registrar(self, acertou):
        self.total += 1
        if acertou:
            self.acertos += 1

    def acuracia(self):
        if self.total == 0:
            return 0
        return self.acertos / self.total

p = Placar()
for r in [True, True, False, True]:
    p.registrar(r)
print(p.acuracia())
''', ["Em <code>registrar</code>: some 1 em <code>self.total</code> e, se acertou, em <code>self.acertos</code>.", "Cuidado com a divisão por zero em <code>acuracia</code>."]),
        cod("Herança", "Crie <code>Gato</code>, que herda de <code>Animal</code> e troca o som por <b>Miau</b>.",
            '''
class Animal:
    def __init__(self, nome):
        self.nome = nome
    def som(self):
        return "..."
    def falar(self):
        return f"{self.nome} diz {self.som()}"

# crie a classe Gato aqui

print(Gato("Mimi").falar())
''',
            [("Gato fala Miau", "assert Gato('Mimi').falar() == 'Mimi diz Miau', f'deu {Gato(\"Mimi\").falar()!r}'"), ("Gato é um Animal", "assert isinstance(Gato('x'), Animal)"), ("Animal continua igual", "assert Animal('Rex').falar() == 'Rex diz ...'")],
            '''
class Animal:
    def __init__(self, nome):
        self.nome = nome
    def som(self):
        return "..."
    def falar(self):
        return f"{self.nome} diz {self.som()}"

class Gato(Animal):
    def som(self):
        return "Miau"

print(Gato("Mimi").falar())
''', ["<code>class Gato(Animal):</code> e, dentro, só um novo <code>som</code>."], rot="Mão no código · nível 2"),
        erros([
            ("Esquecer o <code>self</code> na definição do método.", "<code>TypeError: takes 0 positional arguments but 1 was given</code>. Todo método recebe <code>self</code> primeiro."),
            ("Escrever <code>saldo = 100</code> dentro do <code>__init__</code>.", "Vira variável local e some. O atributo é <code>self.saldo = 100</code>."),
            ("Criar classe para tudo.", "Se não há estado para lembrar, uma função simples resolve melhor."),
        ]),
        ponte("Como se define uma rede neural",
              "<p>Em PyTorch, todo modelo é uma classe que <b>herda</b> de <code>nn.Module</code>: no <code>__init__</code> você cria as camadas (atributos) e no método <code>forward</code> diz como os dados passam por elas. É exatamente a estrutura que você treinou hoje.</p>" +
              py('class MinhaRede(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.camada = nn.Linear(10, 1)\n    def forward(self, x):\n        return self.camada(x)')),
        quiz([
            ("O que é o <code>self</code>?", ["O nome da classe.", "O próprio objeto que está chamando o método.", "Uma palavra opcional."], 1, "É por ele que o método acessa os atributos daquele objeto."),
            ("Quando o <code>__init__</code> roda?", ["Quando o objeto é criado.", "Quando o programa termina.", "Só se for chamado à mão."], 0, "É o construtor."),
            ("<code>class B(A):</code> significa que:", ["B contém um A.", "B herda atributos e métodos de A.", "A herda de B."], 1, "B é um tipo especial de A."),
        ]),
    ],
    ["Classe é o molde; objeto é cada exemplar, com seus próprios atributos.", "Métodos recebem <code>self</code> para acessar o estado do objeto.", "Herança reaproveita e especializa código."],
    "Módulos e pacotes: dividir o programa em arquivos.",
    livro=("PYDOC:classes", "Seções 9.3 e 9.5 (classes e herança)", "Como o tutorial diferencia variáveis de classe e de instância?"))

AULAS["Módulos e pacotes"] = aula(
    30,
    "Ninguém escreve IA do zero: <code>import numpy</code>, <code>import torch</code>. Importar é pegar emprestado o trabalho de milhares de pessoas com uma linha. Hoje você aprende a importar e a organizar o seu próprio código em arquivos.",
    ["importar módulos de três jeitos;", "usar a biblioteca padrão (<code>math</code>, <code>random</code>);", "dividir seu programa em vários arquivos."],
    ["Funções."],
    [
        chute("O que esse código imprime?", ["4.0", "16", "Dá erro"], 0,
              ["Isso! <code>sqrt</code> é raiz quadrada e sempre devolve <code>float</code>.", "Isso seria 16 ao quadrado. <code>sqrt</code> é a raiz.", "Com <code>import math</code> na primeira linha, <code>math.sqrt</code> existe."],
              "O prefixo <code>math.</code> diz de qual “caixa de ferramentas” a função veio.",
              cod='import math\nprint(math.sqrt(16))'),
        concreto("Caixas de ferramentas", "<p>Você não carrega todas as ferramentas da casa no bolso. Pega a caixa de <b>elétrica</b> quando vai mexer na tomada. Um <b>módulo</b> é uma caixa: <code>import math</code> traz as ferramentas de matemática para a bancada.</p>"),
        crianca("<p>Um módulo é um <b>arquivo</b> <code>.py</code> com funções prontas. Um pacote é uma <b>pasta</b> cheia de módulos. Importar é dizer: “vou usar as coisas daquele arquivo ali”.</p>"),
        ver("as formas de importação que o professor compara"),
        nota("Três jeitos de importar", [
            ("<code>import math</code>", "importa o módulo", "Usa com prefixo: <code>math.pi</code>. É o mais claro."),
            ("<code>from math import sqrt</code>", "importa só um nome", "Usa direto: <code>sqrt(9)</code>."),
            ("<code>import numpy as np</code>", "com apelido", "Usa <code>np.array(...)</code>. Os apelidos <code>np</code>, <code>pd</code> e <code>plt</code> são convenção universal."),
            ("<code>if __name__ == \"__main__\":</code>", "só quando rodado direto", "O bloco não roda quando o arquivo é importado por outro."),
        ]),
        passos("Criando o seu módulo", [
            ("Crie <code>metricas.py</code> com <code>def media(v): return sum(v) / len(v)</code>.", "Qualquer arquivo <code>.py</code> já é um módulo."),
            ("Na mesma pasta, crie <code>app.py</code> com <code>import metricas</code>.", "O Python procura primeiro na pasta atual."),
            ("Use <code>metricas.media([1, 2, 3])</code>.", "O nome do arquivo vira o prefixo."),
        ], fim="Código de teste dentro do módulo deve ficar sob <code>if __name__ == \"__main__\":</code>."),
        cod("Sorteio reproduzível", "Use o módulo <code>random</code>: fixe a semente em <b>42</b> com <code>random.seed(42)</code> e depois imprima <code>random.randint(1, 100)</code>. Com a mesma semente, o “sorteio” é sempre o mesmo.",
            '''
import random

# fixe a semente e sorteie um inteiro de 1 a 100
''',
            [("Usa a semente 42", "import random as _r\n_r.seed(42)\nassert saida.strip() == str(_r.randint(1, 100)), 'fixe a semente com random.seed(42) antes de sortear'")],
            '''
import random

random.seed(42)
print(random.randint(1, 100))
''', ["<code>random.seed(42)</code> vem <b>antes</b> do sorteio."]),
        cod("Distância entre dois pontos", "Importe o que precisar de <code>math</code> e devolva a distância entre os pontos <code>(x1, y1)</code> e <code>(x2, y2)</code>.",
            '''
def distancia(x1, y1, x2, y2):
    return 0

print(distancia(0, 0, 3, 4))
''',
            [("(0,0) a (3,4) dá 5", "assert abs(distancia(0, 0, 3, 4) - 5) < 1e-9, f'deu {distancia(0, 0, 3, 4)}'"), ("Mesmo ponto dá 0", "assert distancia(2, 2, 2, 2) == 0")],
            '''
import math

def distancia(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

print(distancia(0, 0, 3, 4))
''', ["Teorema de Pitágoras: raiz de (Δx² + Δy²).", "<code>math.sqrt</code> ou <code>math.hypot</code>."], rot="Mão no código · nível 2"),
        erros([
            ("Chamar seu arquivo de <code>random.py</code> ou <code>math.py</code>.", "O Python importa o <b>seu</b> arquivo em vez do módulo oficial, e tudo quebra. Evite nomes de bibliotecas."),
            ("<code>from modulo import *</code>", "Traz tudo sem prefixo e esconde de onde cada nome veio. Evite."),
            ("<code>import numpy</code> sem ter instalado.", "<code>ModuleNotFoundError</code>: módulos de terceiros precisam de <code>pip install</code> (aula de ambientes virtuais)."),
        ]),
        ponte("As primeiras linhas de todo notebook de IA",
              "<p>Você vai digitar isto centenas de vezes:</p>" + py('import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nfrom sklearn.model_selection import train_test_split') +
              "<p>E a semente fixa (<code>random.seed(42)</code>) é o que torna um experimento <b>reproduzível</b>: outra pessoa roda e obtém o mesmo resultado.</p>"),
        quiz([
            ("Depois de <code>import math</code>, como usar o pi?", ["<code>pi</code>", "<code>math.pi</code>", "<code>math(pi)</code>"], 1, "Com o prefixo do módulo."),
            ("Para que serve <code>import pandas as pd</code>?", ["Instala o pandas.", "Dá um apelido curto ao módulo.", "Importa só uma função."], 1, "<code>pd</code> é a convenção."),
            ("Por que fixar a semente do <code>random</code>?", ["Para o sorteio ser mais rápido.", "Para o resultado ser reproduzível.", "Para sortear números maiores."], 1, "Mesma semente, mesma sequência."),
        ]),
    ],
    ["Módulo é um arquivo <code>.py</code>; pacote é uma pasta de módulos.", "<code>import x</code>, <code>from x import y</code> e <code>import x as z</code>.", "Não dê ao seu arquivo o nome de uma biblioteca."],
    "Arquivos: ler e gravar dados no disco.",
    livro=("PYDOC:modules", "Seções 6.1 e 6.4 (módulos e pacotes)", "O que o tutorial diz sobre o arquivo __init__.py?"))
