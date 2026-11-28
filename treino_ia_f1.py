# -*- coding: utf-8 -*-
"""
Treino · IA, Fase 1 (Fundamentos de Python): "Base da linguagem" e "Estruturas de dados".

Questões de marcar para fixar cada aula (formato em treino_js.py). Toda questão de código é conferida rodando
o Python de verdade (python -X utf8 treino.py): o gabarito é o que o programa mostra na tela.
"""
import textwrap


def c(s):
    """Código: tira a quebra de linha do começo e a indentação comum."""
    return textwrap.dedent(s).strip("\n")


TREINO = {
    # ------------------------------------------------------------------ Base da linguagem
    "Instalar Python e usar o terminal": [
        {"k": "conceito", "pergunta": "No terminal, você está em <code>C:\\Users\\ana</code> e roda <code>cd projetos</code> e depois <code>cd site</code>. Em que pasta você está agora?",
         "opcoes": ["<code>C:\\Users\\ana\\projetos\\site</code>", "<code>C:\\Users\\ana\\site</code>", "<code>C:\\site</code>", "<code>C:\\Users\\ana</code>"],
         "correta": 0,
         "x": "Cada <code>cd</code> entra numa pasta a partir de onde você está: primeiro em <code>projetos</code>, depois em <code>site</code>, que fica dentro dela."},
        {"k": "conceito", "pergunta": "Qual comando mostra a versão do Python instalada?",
         "opcoes": ["<code>python --version</code>", "<code>python version.py</code>", "<code>pip python</code>", "<code>cd python</code>"],
         "correta": 0,
         "x": "<code>python --version</code> (ou <code>python -V</code>) imprime algo como <code>Python 3.12.4</code>. É o primeiro teste depois de instalar."},
        {"k": "conceito", "pergunta": "No modo interativo (<code>&gt;&gt;&gt;</code>), você digita <code>2 + 3</code> e aperta Enter. O que acontece?",
         "opcoes": ["Aparece <code>5</code> logo abaixo", "Nada: sem <code>print</code>, não aparece nada", "Dá erro, porque falta o <code>print</code>", "O Python salva a conta num arquivo"],
         "correta": 0,
         "porques": ["", "No modo interativo, o valor de cada expressão aparece sozinho. Dentro de um arquivo .py, sim, precisaria de print.", "Não é erro: no modo interativo a expressão é avaliada e mostrada.", "O modo interativo não salva nada em arquivo."],
         "x": "O modo interativo avalia cada linha e mostra o resultado na hora. Ótimo para testar uma ideia rápida."},
        {"k": "conceito", "pergunta": "Você roda <code>python app.py</code> e aparece <code>can't open file 'app.py': No such file or directory</code>. O que provavelmente aconteceu?",
         "opcoes": ["O terminal está numa pasta diferente da do arquivo", "O Python não está instalado", "O app.py tem um erro de sintaxe", "Falta instalar o app.py com pip"],
         "correta": 0,
         "porques": ["", "Se o Python não estivesse instalado, o erro seria que o comando python não foi reconhecido.", "Com erro de sintaxe o Python abriria o arquivo e mostraria SyntaxError.", "Arquivos .py seus não se instalam com pip."],
         "x": "O Python foi achado, o arquivo não. Use <code>cd</code> até a pasta do app.py (confira com <code>dir</code> ou <code>ls</code>) e rode de novo."},
        {"k": "conceito", "pergunta": "No Windows aparece <code>'python' não é reconhecido como um comando interno</code>. Qual é a causa mais comum?",
         "opcoes": ["O Python não foi adicionado ao PATH na instalação", "O arquivo tem nome com acento", "Você esqueceu o print", "O computador está sem internet"],
         "correta": 0,
         "x": "O PATH é a lista de pastas onde o terminal procura programas. Reinstale marcando <i>Add python.exe to PATH</i> (ou use o comando <code>py</code>)."},
        {"k": "saida", "codigo": c('''
            print("Olá")
            print("mundo")
         '''),
         "opcoes": ["Olá\nmundo", "Olá mundo", "Olámundo", "mundo\nOlá"],
         "correta": 0,
         "x": "Cada <code>print</code> termina pulando de linha, então cada palavra sai numa linha."},
        {"k": "saida", "codigo": c('''
            print(2 + 3)
            print("2 + 3")
         '''),
         "opcoes": ["5\n5", "2 + 3\n2 + 3", "5\n2 + 3", "SyntaxError"],
         "correta": 2,
         "x": "Sem aspas, <code>2 + 3</code> é uma conta e sai <code>5</code>. Entre aspas é texto e sai do jeito que foi escrito."},
        {"k": "lacuna", "pergunta": "Complete para o programa mostrar <code>Oi, Python!</code> na tela.",
         "codigo": c('''
            ____("Oi, Python!")
         '''),
         "opcoes": ["print", "echo", "show", "input"], "correta": 0, "saida": "Oi, Python!",
         "x": "<code>print</code> mostra na tela. <code>echo</code> é comando do terminal, não do Python; <code>show</code> não existe; <code>input</code> espera a pessoa digitar."},
        {"k": "erro", "codigo": c('''
            print("Rodando o programa")
            print("Versão 1.0)
            print("Fim")
         '''),
         "linha": 2, "correcao": 'print("Versão 1.0")', "saida": "Rodando o programa\nVersão 1.0\nFim",
         "x": "Faltou fechar as aspas. É erro de sintaxe (<code>SyntaxError</code>): o Python nem começa a rodar, por isso nem a 1ª linha aparece."},
        {"k": "erro", "codigo": c('''
            nome = "Ana"
            Print("Olá,", nome)
            print("Tchau")
         '''),
         "linha": 2, "correcao": 'print("Olá,", nome)', "saida": "Olá, Ana\nTchau",
         "x": "O Python diferencia maiúsculas: <code>Print</code> não existe e dá <code>NameError</code>. O certo é <code>print</code>."},
    ],

    "Entrada e saída de dados": [
        {"k": "saida", "codigo": c('''
            preco = 4.5
            qtd = 3
            print(f"Total: R$ {preco * qtd:.2f}")
         '''),
         "opcoes": ["Total: R$ 13.5", "Total: R$ 13.50", "Total: R$ {preco * qtd:.2f}", "Total: R$ 13,50"],
         "correta": 1,
         "porques": ["Sem formatação seria 13.5; o :.2f força duas casas.", "", "Com o f antes das aspas, o que está entre chaves é calculado.", "O Python usa ponto como separador decimal."],
         "x": "Dentro das chaves a conta é feita (13.5) e <code>:.2f</code> mostra com duas casas: <code>13.50</code>."},
        {"k": "saida", "pergunta": "A pessoa digita <code>20</code>. O que aparece na tela?",
         "codigo": c('''
            idade = input("Idade: ")
            print(idade + idade)
         '''), "entradas": ["20"],
         "opcoes": ["Idade: 20\n40", "Idade: 20\n2020", "Idade: 20\nTypeError", "Idade: 20\n20 20"],
         "correta": 1,
         "porques": ["Para dar 40, seria preciso converter com int().", "", "Texto + texto é permitido: junta os dois.", "O + junta sem espaço."],
         "x": "<code>input()</code> sempre devolve texto. <code>\"20\" + \"20\"</code> junta os textos: <code>2020</code>."},
        {"k": "saida", "codigo": c('''
            x = int("7") + 3
            y = "7" + "3"
            print(x, y)
         '''),
         "opcoes": ["10 10", "73 73", "10 73", "TypeError"],
         "correta": 2,
         "x": "<code>int(\"7\")</code> vira o número 7, e 7 + 3 = 10. Já <code>\"7\" + \"3\"</code> junta textos: <code>73</code>."},
        {"k": "saida", "codigo": c('''
            media = 7.456
            print(f"{media:.1f}")
            print(round(media, 2))
         '''),
         "opcoes": ["7.4\n7.45", "7.5\n7.46", "7.456\n7.456", "7.5\n7.45"],
         "correta": 1,
         "x": "As duas formas arredondam: com 1 casa, 7.456 vira 7.5; com 2 casas, 7.46."},
        {"k": "saida", "codigo": c('''
            print(int("4.90"))
         '''),
         "opcoes": ["4", "4.9", "5", "ValueError"],
         "correta": 3,
         "x": "<code>int()</code> não aceita texto com ponto decimal: dá <code>ValueError</code>. Para preços, use <code>float(\"4.90\")</code>."},
        {"k": "lacuna", "pergunta": "A pessoa digita 2 e depois 3. Complete para o programa mostrar a soma, <code>5</code>.",
         "codigo": c('''
            a = ____(input("a: "))
            b = int(input("b: "))
            print(a + b)
         '''), "entradas": ["2", "3"],
         "opcoes": ["int", "str", "float", "len"], "correta": 0, "saida": "a: 2\nb: 3\n5",
         "x": "Converta o texto em número inteiro com <code>int</code>. Com <code>str</code> dá erro (texto + número), <code>float</code> mostraria 5.0 e <code>len</code> mede o tamanho do texto."},
        {"k": "lacuna", "pergunta": "Complete para mostrar <code>Preço: 3.50</code>.",
         "codigo": c('''
            preco = 3.5
            print(f"Preço: {preco____}")
         '''),
         "opcoes": [":.2f", ".2f", ":2f", ":.2"], "correta": 0, "saida": "Preço: 3.50",
         "x": "O formato vem depois de dois-pontos: <code>{preco:.2f}</code> = número com 2 casas. Sem os dois-pontos é erro; <code>:2f</code> mostra 6 casas e <code>:.2</code> usa 2 algarismos no total (3.5)."},
        {"k": "erro", "pergunta": "A pessoa digita 2.5 e 4. Em qual linha está o erro?",
         "codigo": c('''
            preco = float(input("Preço: "))
            qtd = int(input("Quantidade: "))
            total = preco * qtd
            print(f"Total: {total:.2f")
         '''), "entradas": ["2.5", "4"],
         "linha": 4, "correcao": 'print(f"Total: {total:.2f}")', "saida": "Preço: 2.5\nQuantidade: 4\nTotal: 10.00",
         "x": "Faltou fechar a chave dentro da f-string: <code>{total:.2f}</code>. É erro de sintaxe, então o programa nem começa."},
        {"k": "erro", "pergunta": "A pessoa digita 1.6 e 64. Em qual linha está o erro?",
         "codigo": c('''
            altura = float(input("Altura: "))
            peso = float(input("Peso: "))
            imc = peso / altura ** 2
            print("IMC:" round(imc, 1))
         '''), "entradas": ["1.6", "64"],
         "linha": 4, "correcao": 'print("IMC:", round(imc, 1))', "saida": "Altura: 1.6\nPeso: 64\nIMC: 25.0",
         "x": "No <code>print</code>, cada valor é separado por vírgula. Sem ela, o Python não entende a linha (<code>SyntaxError</code>)."},
        {"k": "conceito", "pergunta": "Você leu duas notas, <code>n1</code> e <code>n2</code>, como números. Qual linha mostra a média com 1 casa?",
         "opcoes": ['<code>print(f"Média: {(n1 + n2) / 2:.1f}")</code>', '<code>print(f"Média: {n1 + n2 / 2:.1f}")</code>',
                    '<code>print("Média: {(n1 + n2) / 2:.1f}")</code>', '<code>print(f"Média: {(n1 + n2) / 2}:.1f")</code>'],
         "correta": 0,
         "porques": ["", "Sem parênteses, a divisão acontece antes da soma: n1 + (n2 / 2).", "Sem o f antes das aspas, as chaves saem como texto.", "O :.1f precisa ficar dentro das chaves."],
         "x": "Parênteses garantem a soma antes da divisão, o <code>f</code> ativa as chaves e o <code>:.1f</code>, dentro delas, formata."},
    ],

    "Variáveis e tipos (int, float, str, bool)": [
        {"k": "saida", "codigo": c('''
            print(type(3 / 2))
            print(type(3 // 2))
         '''),
         "opcoes": ["<class 'int'>\n<class 'int'>", "<class 'float'>\n<class 'float'>", "<class 'float'>\n<class 'int'>", "<class 'int'>\n<class 'float'>"],
         "correta": 2,
         "x": "<code>/</code> sempre devolve float (1.5). <code>//</code> com dois inteiros devolve int (1)."},
        {"k": "saida", "codigo": c('''
            a = "5"
            b = 2
            print(a * b)
         '''),
         "opcoes": ["10", "55", "TypeError", "5 5"],
         "correta": 1,
         "porques": ["Seria 10 se a fosse o número 5, sem aspas.", "", "Texto vezes inteiro é permitido: repete o texto.", "A repetição não coloca espaço."],
         "x": "Texto vezes número repete o texto: <code>\"5\" * 2</code> é <code>\"55\"</code>. O mesmo operador muda de comportamento conforme o tipo."},
        {"k": "saida", "codigo": c('''
            x = 10
            y = x
            x = x + 5
            print(x, y)
         '''),
         "opcoes": ["15 15", "15 10", "10 15", "10 10"],
         "correta": 1,
         "x": "<code>y = x</code> copia o valor 10 naquele momento. Depois, <code>x</code> passa a valer 15 e <code>y</code> continua 10."},
        {"k": "saida", "codigo": c('''
            print(bool(0), bool("0"), bool(""))
         '''),
         "opcoes": ["False False False", "False True False", "True True False", "False True True"],
         "correta": 1,
         "x": "Zero e texto vazio são falsos. Já <code>\"0\"</code> é um texto com um caractere, então é verdadeiro."},
        {"k": "saida", "codigo": c('''
            print(int(3.99), round(3.99))
         '''),
         "opcoes": ["4 4", "3 4", "3 3", "3.99 4"],
         "correta": 1,
         "x": "<code>int()</code> corta as casas decimais (não arredonda): 3. <code>round()</code> arredonda: 4."},
        {"k": "lacuna", "pergunta": "Complete para o programa mostrar <code>13.5</code>.",
         "codigo": c('''
            texto = "12.5"
            numero = ____(texto)
            print(numero + 1)
         '''),
         "opcoes": ["float", "int", "str", "bool"], "correta": 0, "saida": "13.5",
         "x": "Texto com casas decimais vira número com <code>float</code>. <code>int(\"12.5\")</code> dá ValueError, <code>str</code> continua texto (e dá erro ao somar 1) e <code>bool</code> vira True."},
        {"k": "lacuna", "pergunta": "Complete para o programa mostrar <code>True</code>.",
         "codigo": c('''
            idade = 18
            print(idade ____ 18)
         '''),
         "opcoes": ["==", "=", "!=", ">"], "correta": 0, "saida": "True",
         "x": "Para comparar, use <code>==</code>. Um <code>=</code> só serve para guardar valor (aqui dá erro); <code>!=</code> e <code>&gt;</code> dão False."},
        {"k": "erro", "codigo": c('''
            nome = "Bia"
            idade = 25
            print("Oi, " + nome + "! Você tem " + idade + " anos.")
            print("Ano que vem:", idade + 1)
         '''),
         "linha": 3, "correcao": 'print("Oi, " + nome + "! Você tem " + str(idade) + " anos.")', "saida": "Oi, Bia! Você tem 25 anos.\nAno que vem: 26",
         "x": "Não dá para juntar texto com número usando <code>+</code> (<code>TypeError</code>). Converta com <code>str(idade)</code>, ou use uma f-string."},
        {"k": "erro", "codigo": c('''
            preco = 10
            desconto = 0.1
            if desconto = 0.1:
                print("Promoção!")
            print(preco * (1 - desconto))
         '''),
         "linha": 3, "correcao": "if desconto == 0.1:", "saida": "Promoção!\n9.0",
         "x": "No <code>if</code> você compara, então é <code>==</code>. O <code>=</code> guarda valor e ali vira erro de sintaxe."},
        {"k": "conceito", "pergunta": "Qual destes nomes de variável dá erro no Python?",
         "opcoes": ["<code>2nota</code>", "<code>nota_2</code>", "<code>_nota</code>", "<code>notaFinal</code>"],
         "correta": 0,
         "x": "Nome de variável não pode começar com número. Letras, números e <code>_</code> valem, desde que o primeiro caractere não seja um número."},
    ],

    "Operadores aritméticos": [
        {"k": "saida", "codigo": c('''
            print(2 + 3 * 4 ** 2)
         '''),
         "opcoes": ["50", "80", "146", "400"],
         "correta": 0,
         "porques": ["", "Isso seria (2 + 3) * 4 ** 2: a soma não vem antes.", "Isso seria 2 + (3 * 4) ** 2: a potência vale só para o 4.", "Isso seria fazer tudo da esquerda para a direita."],
         "x": "Primeiro a potência (4 ** 2 = 16), depois a multiplicação (3 * 16 = 48) e por fim a soma: 2 + 48 = 50."},
        {"k": "saida", "codigo": c('''
            print(17 // 5, 17 % 5, 17 / 5)
         '''),
         "opcoes": ["3 2 3.4", "3.4 2 3.4", "3 3 3.4", "2 3 3.4"],
         "correta": 0,
         "x": "<code>//</code> diz quantas vezes o 5 cabe em 17 (3), <code>%</code> diz o que sobra (2) e <code>/</code> é a divisão comum (3.4)."},
        {"k": "saida", "codigo": c('''
            print(-7 // 2)
         '''),
         "opcoes": ["-3", "-4", "-3.5", "3"],
         "correta": 1,
         "x": "<code>//</code> arredonda sempre para baixo, na direção do menos infinito. -3.5 para baixo é -4, e não -3."},
        {"k": "saida", "codigo": c('''
            print(2 ** 3 ** 2)
         '''),
         "opcoes": ["64", "512", "36", "12"],
         "correta": 1,
         "x": "Potência é calculada da direita para a esquerda: 3 ** 2 = 9, depois 2 ** 9 = 512. Na dúvida, use parênteses."},
        {"k": "saida", "codigo": c('''
            total = 125
            print(total // 60, "min", total % 60, "s")
         '''),
         "opcoes": ["2 min 5 s", "2 min 2 s", "5 min 2 s", "2.08 min 5 s"],
         "correta": 0,
         "x": "125 segundos: cabem 2 minutos inteiros (125 // 60) e sobram 5 segundos (125 % 60)."},
        {"k": "lacuna", "pergunta": "Complete para testar se <code>n</code> é par (deve mostrar <code>True</code>).",
         "codigo": c('''
            n = 14
            print(n ____ 2 == 0)
         '''),
         "opcoes": ["%", "//", "/", "**"], "correta": 0, "saida": "True",
         "x": "Número par deixa resto 0 na divisão por 2: <code>n % 2 == 0</code>. Com <code>//</code> ou <code>/</code> o resultado é 7, que não é 0."},
        {"k": "lacuna", "pergunta": "Complete para calcular a média de 6 e 9 (deve mostrar <code>7.5</code>).",
         "codigo": c('''
            a = 6
            b = 9
            media = ____
            print(media)
         '''),
         "opcoes": ["(a + b) / 2", "a + b / 2", "(a + b) // 2", "a + b // 2"], "correta": 0, "saida": "7.5",
         "x": "Os parênteses fazem a soma primeiro e o <code>/</code> mantém o .5. Sem parênteses o Python divide só o b; com <code>//</code> o resultado seria 7."},
        {"k": "erro", "pergunta": "A média de 8 e 6 deveria dar 7.0, mas o programa mostra 11.0. Em qual linha está o erro?",
         "codigo": c('''
            nota1 = 8
            nota2 = 6
            media = nota1 + nota2 / 2
            print("Média:", media)
         '''),
         "linha": 3, "correcao": "media = (nota1 + nota2) / 2", "saida": "Média: 7.0",
         "x": "A divisão vem antes da soma, então o Python fez 8 + 3.0. Os parênteses resolvem: <code>(nota1 + nota2) / 2</code>."},
        {"k": "erro", "pergunta": "A área de um quadrado de lado 4 é 16, mas o programa mostra 6. Qual linha está errada?",
         "codigo": c('''
            lado = 4
            area = lado ^ 2
            print("Área:", area)
         '''),
         "linha": 2, "correcao": "area = lado ** 2", "saida": "Área: 16",
         "x": "No Python, potência é <code>**</code>. O <code>^</code> é outra operação (ou exclusivo bit a bit), e 4 ^ 2 dá 6."},
        {"k": "conceito", "pergunta": "50 alunos vão ser divididos em grupos de 6. Qual operador diz quantos grupos completos dá para formar?",
         "opcoes": ["<code>//</code>", "<code>%</code>", "<code>/</code>", "<code>**</code>"],
         "correta": 0,
         "porques": ["", "% diz quantos sobram (2 alunos).", "/ dá 8.33…, um número quebrado.", "** é potência."],
         "x": "<code>50 // 6</code> = 8 grupos completos. O <code>%</code> mostraria os 2 alunos que sobram."},
    ],

    "Usar módulos prontos (import)": [
        {"k": "saida", "codigo": c('''
            import math
            print(math.sqrt(16), math.floor(2.7), math.ceil(2.1))
         '''),
         "opcoes": ["4 2 3", "4.0 2 3", "4.0 3 2", "4.0 2.7 3"],
         "correta": 1,
         "x": "<code>sqrt</code> devolve float (4.0); <code>floor</code> arredonda para baixo (2) e <code>ceil</code> para cima (3)."},
        {"k": "saida", "codigo": c('''
            from math import pi
            print(round(pi, 2))
         '''),
         "opcoes": ["3.14", "3.1416", "3", "NameError"],
         "correta": 0,
         "x": "Com <code>from math import pi</code>, o nome <code>pi</code> fica disponível direto, sem <code>math.</code>. Arredondado a 2 casas: 3.14."},
        {"k": "saida", "codigo": c('''
            import math
            print(sqrt(25))
         '''),
         "opcoes": ["5.0", "5", "NameError", "25"],
         "correta": 2,
         "x": "Com <code>import math</code>, as funções ficam dentro de <code>math</code>: o certo é <code>math.sqrt(25)</code>. Sozinho, <code>sqrt</code> não existe."},
        {"k": "saida", "codigo": c('''
            import math as m
            print(m.floor(-2.5))
         '''),
         "opcoes": ["-2", "-3", "-2.5", "NameError"],
         "correta": 1,
         "x": "<code>as m</code> cria um apelido para o módulo. E <code>floor</code> arredonda para baixo: abaixo de -2.5 vem -3."},
        {"k": "lacuna", "pergunta": "Complete para usar <code>sqrt</code> sem escrever <code>math.</code> antes.",
         "codigo": c('''
            ____ math import sqrt
            print(sqrt(9))
         '''),
         "opcoes": ["from", "import", "use", "include"], "correta": 0, "saida": "3.0",
         "x": "A forma é <code>from módulo import nome</code>. <code>use</code> e <code>include</code> são de outras linguagens."},
        {"k": "lacuna", "pergunta": "Complete para o programa mostrar <code>2</code>.",
         "codigo": c('''
            import math
            print(math.____(2.9))
         '''),
         "opcoes": ["floor", "ceil", "round", "sqrt"], "correta": 0, "saida": "2",
         "x": "<code>floor</code> arredonda para baixo: 2. <code>ceil</code> daria 3; <code>math.round</code> não existe (o <code>round</code> é embutido) e <code>sqrt</code> é raiz."},
        {"k": "erro", "codigo": c('''
            import math
            raio = 3
            area = math.pi * raio ** 2
            print(round(area, 1))
            perimetro = 2 * math.Pi * raio
            print(round(perimetro, 1))
         '''),
         "linha": 5, "correcao": "perimetro = 2 * math.pi * raio", "saida": "28.3\n18.8",
         "x": "Nomes diferenciam maiúsculas: o módulo tem <code>math.pi</code>, não <code>math.Pi</code> (<code>AttributeError</code>)."},
        {"k": "erro", "codigo": c('''
            from random import randint
            a = randint(1, 6)
            b = random.randint(1, 6)
            print(1 <= a <= 6 and 1 <= b <= 6)
         '''),
         "linha": 3, "correcao": "b = randint(1, 6)", "saida": "True",
         "x": "Só o nome <code>randint</code> foi importado; o nome <code>random</code> não existe aqui (<code>NameError</code>). Use <code>randint(1, 6)</code>, como na linha 2."},
        {"k": "conceito", "pergunta": "Você salvou seu arquivo como <code>random.py</code> e, dentro dele, escreveu <code>import random</code>. O que acontece?",
         "opcoes": ["O Python importa o seu próprio arquivo em vez do módulo, e as funções dele não existem", "Funciona normalmente", "O Python pergunta qual dos dois usar", "O Python baixa o módulo de novo"],
         "correta": 0,
         "x": "O Python procura primeiro na pasta do programa. Por isso, nunca dê ao seu arquivo o nome de um módulo (random.py, math.py, json.py…)."},
        {"k": "conceito", "pergunta": "Qual a diferença entre <code>import math</code> e <code>from math import sqrt</code>?",
         "opcoes": ["No primeiro você escreve <code>math.sqrt(...)</code>; no segundo, só <code>sqrt(...)</code>", "O segundo baixa o módulo da internet", "O primeiro só funciona depois de pip install", "Nenhuma: nos dois se escreve só <code>sqrt(...)</code>"],
         "correta": 0,
         "x": "<code>import math</code> traz o módulo inteiro e exige o prefixo. <code>from math import sqrt</code> traz só aquele nome, que fica disponível direto."},
    ],

    "Manipular textos (strings)": [
        {"k": "saida", "codigo": c('''
            s = "Python"
            print(s[1:4], s[-2:])
         '''),
         "opcoes": ["yth on", "Pyt on", "ytho on", "yth n"],
         "correta": 0,
         "x": "Índices começam em 0: <code>s[1:4]</code> pega as posições 1, 2 e 3 (y, t, h). <code>s[-2:]</code> pega as duas últimas."},
        {"k": "saida", "codigo": c('''
            nome = "  ana silva  "
            print(nome.strip().title())
         '''),
         "opcoes": ["Ana silva", "Ana Silva", "  Ana Silva  ", "ANA SILVA"],
         "correta": 1,
         "x": "<code>strip()</code> tira os espaços das pontas e <code>title()</code> põe a primeira letra de cada palavra em maiúscula."},
        {"k": "saida", "codigo": c('''
            s = "banana"
            s.upper()
            print(s)
         '''),
         "opcoes": ["BANANA", "banana", "Banana", "None"],
         "correta": 1,
         "x": "Strings não mudam. <code>s.upper()</code> devolve uma cópia em maiúsculas, mas ninguém guardou essa cópia. O certo seria <code>s = s.upper()</code>."},
        {"k": "saida", "codigo": c('''
            frase = "eu gosto de IA"
            palavras = frase.split()
            print(len(palavras), "-".join(palavras))
         '''),
         "opcoes": ["4 eu-gosto-de-IA", "14 eu-gosto-de-IA", "4 eu gosto de IA", "1 eu-gosto-de-IA"],
         "correta": 0,
         "x": "<code>split()</code> separa nos espaços: 4 palavras. <code>\"-\".join(...)</code> junta de volta, com hífen entre elas."},
        {"k": "saida", "codigo": c('''
            email = "ana@gmail.com"
            print(email.replace("gmail", "empresa"))
            print(email.find("@"))
         '''),
         "opcoes": ["ana@empresa.com\n3", "ana@empresa.com\n4", "ana@gmail.com\n3", "empresa\n3"],
         "correta": 0,
         "x": "<code>replace</code> devolve uma cópia trocando o trecho. <code>find</code> diz a posição do @: a, n, a ocupam 0, 1, 2, então o @ está na 3."},
        {"k": "lacuna", "pergunta": "Complete para o programa mostrar <code>DADOS</code>.",
         "codigo": c('''
            palavra = "dados"
            print(palavra.____())
         '''),
         "opcoes": ["upper", "capitalize", "lower", "title"], "correta": 0, "saida": "DADOS",
         "x": "<code>upper()</code> põe tudo em maiúsculas. <code>capitalize</code> e <code>title</code> dariam Dados; <code>lower</code>, dados."},
        {"k": "lacuna", "pergunta": "Complete para juntar a lista e mostrar <code>a, b, c</code>.",
         "codigo": c('''
            letras = ["a", "b", "c"]
            print(____)
         '''),
         "opcoes": ['", ".join(letras)', 'letras.join(", ")', '", ".split(letras)', '" ".join(letras)'], "correta": 0, "saida": "a, b, c",
         "x": "O <code>join</code> é chamado no separador e recebe a lista: <code>\", \".join(letras)</code>. Lista não tem <code>join</code>, e com <code>\" \"</code> sairia a b c."},
        {"k": "erro", "pergunta": "Era para mostrar só os números do CPF (12345678900). Qual linha está errada?",
         "codigo": c('''
            cpf = "123.456.789-00"
            numeros = cpf.replace(".", "")
            numeros = cpf.replace("-", "")
            print(numeros)
         '''),
         "linha": 3, "correcao": 'numeros = numeros.replace("-", "")', "saida": "12345678900",
         "x": "A linha 3 parte de novo do <code>cpf</code> original e perde a troca anterior. Continue de <code>numeros</code>: cada <code>replace</code> devolve uma cópia nova."},
        {"k": "erro", "codigo": c('''
            nome = "maria"
            nome[0] = "M"
            print(nome)
         '''),
         "linha": 2, "correcao": 'nome = "M" + nome[1:]', "saida": "Maria",
         "x": "Não dá para trocar uma letra de uma string (<code>TypeError</code>): strings são imutáveis. Monte uma nova, como <code>\"M\" + nome[1:]</code>, ou use <code>nome.capitalize()</code>."},
        {"k": "conceito", "pergunta": "Qual expressão conta quantas vezes a letra a aparece em <code>\"banana\"</code>?",
         "opcoes": ['<code>"banana".count("a")</code>', '<code>len("banana")</code>', '<code>"banana".find("a")</code>', '<code>"banana".index("a")</code>'],
         "correta": 0,
         "porques": ["", "len conta todos os caracteres (6).", "find diz a posição da 1ª ocorrência (1).", "index também diz a posição da 1ª ocorrência."],
         "x": "<code>count</code> conta as ocorrências: 3. <code>find</code> e <code>index</code> dizem onde aparece a primeira."},
    ],

    "Condicionais (if, elif, else)": [
        {"k": "saida", "codigo": c('''
            nota = 7
            if nota >= 9:
                print("A")
            elif nota >= 7:
                print("B")
            elif nota >= 5:
                print("C")
            else:
                print("D")
         '''),
         "opcoes": ["B", "B\nC", "C", "A\nB"],
         "correta": 0,
         "x": "O Python testa de cima para baixo e roda só o primeiro bloco verdadeiro: 7 &gt;= 9 é falso, 7 &gt;= 7 é verdadeiro, então sai B e o resto é ignorado."},
        {"k": "saida", "codigo": c('''
            x = 4
            if x > 2:
                print("maior que 2")
            if x > 3:
                print("maior que 3")
            else:
                print("até 3")
         '''),
         "opcoes": ["maior que 2", "maior que 2\nmaior que 3", "maior que 3", "maior que 2\naté 3"],
         "correta": 1,
         "x": "São dois <code>if</code> separados, não uma cadeia com <code>elif</code>. Cada um é testado: os dois são verdadeiros."},
        {"k": "saida", "codigo": c('''
            idade = 16
            tem_autorizacao = True
            if idade >= 18 or tem_autorizacao:
                print("pode entrar")
            else:
                print("não pode")
         '''),
         "opcoes": ["pode entrar", "não pode", "pode entrar\nnão pode", "SyntaxError"],
         "correta": 0,
         "x": "Com <code>or</code>, basta uma condição verdadeira. A idade não chega a 18, mas há autorização."},
        {"k": "saida", "codigo": c('''
            a = 5
            print(a > 3 and not a == 5)
         '''),
         "opcoes": ["True", "False", "5", "None"],
         "correta": 1,
         "x": "<code>a &gt; 3</code> é True, mas <code>not a == 5</code> é False. Com <code>and</code>, as duas precisam ser verdadeiras."},
        {"k": "lacuna", "pergunta": "Complete para mostrar <code>reprovado</code> quando a nota não chega a 5.",
         "codigo": c('''
            nota = 3
            if nota >= 5:
                print("aprovado")
            ____:
                print("reprovado")
         '''),
         "opcoes": ["else", "elif", "if", "else nota < 5"], "correta": 0, "saida": "reprovado",
         "x": "<code>else</code> pega todo o resto e não leva condição. <code>elif</code> e <code>if</code> precisariam de uma condição; <code>else</code> com condição é erro."},
        {"k": "lacuna", "pergunta": "Vai à praia só se fizer mais de 25 graus <b>e</b> não estiver chovendo. Com 20 graus, deve sair <code>casa</code>. Qual peça completa?",
         "codigo": c('''
            temperatura = 20
            chovendo = False
            if temperatura > 25 ____ not chovendo:
                print("praia!")
            else:
                print("casa")
         '''),
         "opcoes": ["and", "or", "+", "&"], "correta": 0, "saida": "casa",
         "x": "As duas coisas precisam valer ao mesmo tempo, então é <code>and</code>. Com <code>or</code>, bastaria não chover e sairia praia!"},
        {"k": "erro", "codigo": c('''
            senha = "abc123"
            if senha == "abc123"
                print("acesso liberado")
         '''),
         "linha": 2, "correcao": 'if senha == "abc123":', "saida": "acesso liberado",
         "x": "Toda linha de <code>if</code>, <code>elif</code> e <code>else</code> termina com dois-pontos."},
        {"k": "erro", "pergunta": "Com saldo 50, um saque de 80 deveria ser negado, mas o programa autoriza. Qual linha está errada?",
         "codigo": c('''
            saldo = 50
            saque = 80
            if saque > saldo:
                print("saque autorizado")
            else:
                print("saldo insuficiente")
         '''),
         "linha": 3, "correcao": "if saque <= saldo:", "saida": "saldo insuficiente",
         "x": "A condição está invertida: só pode sacar se o saque for menor ou igual ao saldo, <code>saque &lt;= saldo</code>."},
        {"k": "conceito", "pergunta": "Qual condição testa \"x entre 1 e 10, incluindo os dois\"?",
         "opcoes": ["<code>1 &lt;= x &lt;= 10</code>", "<code>1 &lt; x &lt; 10</code>", "<code>x &gt;= 1 or x &lt;= 10</code>", "<code>x =&gt; 1 and x =&lt; 10</code>"],
         "correta": 0,
         "porques": ["", "Com &lt; puro, o 1 e o 10 ficam de fora.", "Com or, qualquer número passa (todo número é maior que 1 ou menor que 10).", "=&gt; e =&lt; não existem: é &gt;= e &lt;=."],
         "x": "O Python aceita comparação encadeada: <code>1 &lt;= x &lt;= 10</code> é o mesmo que <code>x &gt;= 1 and x &lt;= 10</code>."},
        {"k": "conceito", "pergunta": "Num <code>if</code>, quais destes valores contam como falso?",
         "opcoes": ["<code>0</code>, <code>\"\"</code> (texto vazio), <code>[]</code> (lista vazia) e <code>None</code>", "Só a palavra <code>False</code>", "Qualquer número negativo", "O texto <code>\"False\"</code>"],
         "correta": 0,
         "x": "Zero, vazios e None são falsos; quase todo o resto é verdadeiro. Até o texto \"False\" é verdadeiro, porque não está vazio."},
    ],

    "Condições aninhadas e elif": [
        {"k": "saida", "codigo": c('''
            logado = True
            admin = False
            if logado:
                if admin:
                    print("painel")
                else:
                    print("perfil")
            else:
                print("login")
         '''),
         "opcoes": ["painel", "perfil", "login", "perfil\nlogin"],
         "correta": 1,
         "x": "Está logado, então entra no primeiro bloco. Lá dentro, como não é admin, cai no <code>else</code> de dentro: perfil."},
        {"k": "saida", "codigo": c('''
            t = 25
            if t > 30:
                print("quente")
            elif t > 20:
                print("agradável")
            elif t > 10:
                print("frio")
            print("fim")
         '''),
         "opcoes": ["agradável\nfim", "agradável\nfrio\nfim", "agradável", "fim"],
         "correta": 0,
         "x": "Só um caminho da cadeia roda (agradável). O <code>print(\"fim\")</code> está fora da cadeia e sempre roda."},
        {"k": "saida", "codigo": c('''
            n = 0
            if n > 0:
                print("positivo")
            elif n < 0:
                print("negativo")
         '''),
         "opcoes": ["positivo", "negativo", "zero", "(nada aparece)"],
         "correta": 3,
         "x": "Nenhuma condição é verdadeira para 0 e não há <code>else</code>, então nada é impresso."},
        {"k": "saida", "codigo": c('''
            x = 7
            if x % 2 == 0:
                print("par")
            elif x % 3 == 0:
                print("múltiplo de 3")
            else:
                print("outro")
         '''),
         "opcoes": ["par", "múltiplo de 3", "outro", "(nada aparece)"],
         "correta": 2,
         "x": "7 não é par (resto 1) nem múltiplo de 3 (resto 1), então cai no <code>else</code>."},
        {"k": "lacuna", "pergunta": "Com nota 95 o programa deve mostrar <code>A</code>. Qual palavra completa a segunda condição?",
         "codigo": c('''
            nota = 95
            if nota >= 90:
                conceito = "A"
            ____ nota >= 80:
                conceito = "B"
            else:
                conceito = "C"
            print(conceito)
         '''),
         "opcoes": ["elif", "if", "else", "else if"], "correta": 0, "saida": "A",
         "x": "Com <code>elif</code>, depois que o primeiro teste passa, os outros são pulados. Com um segundo <code>if</code>, ele também rodaria e trocaria o A por B."},
        {"k": "lacuna", "pergunta": "Adulto sem ingresso deve ver <code>compre o ingresso</code>. Qual condição completa o if de dentro?",
         "codigo": c('''
            idade = 20
            tem_ingresso = False
            if idade >= 18:
                if ____:
                    print("entra")
                else:
                    print("compre o ingresso")
            else:
                print("menor de idade")
         '''),
         "opcoes": ["tem_ingresso", "not tem_ingresso", "idade >= 18", "tem_ingresso or idade > 18"], "correta": 0, "saida": "compre o ingresso",
         "x": "A pergunta de dentro é \"tem ingresso?\". Como é False, cai no <code>else</code> de dentro. As outras condições deixariam entrar sem ingresso."},
        {"k": "erro", "pergunta": "Com nota 95 deveria sair excelente, mas sai bom. Qual linha causa o problema?",
         "codigo": c('''
            nota = 95
            if nota >= 70:
                faixa = "bom"
            elif nota >= 90:
                faixa = "excelente"
            else:
                faixa = "melhorar"
            print(faixa)
         '''),
         "linha": 2, "correcao": "if 70 <= nota < 90:", "saida": "excelente",
         "x": "O primeiro teste (<code>&gt;= 70</code>) já pega o 95 e o <code>elif</code> nunca roda. Ou se limita a faixa (<code>70 &lt;= nota &lt; 90</code>), ou se testa o 90 primeiro."},
        {"k": "erro", "indentacao": True, "codigo": c('''
            chuva = True
            frio = False
            if chuva:
                if frio:
                    print("casaco e guarda-chuva")
                else:
                    print("só guarda-chuva")
                else:
                    print("dia livre")
         '''),
         "linha": 8, "correcao": "else:", "saida": "só guarda-chuva",
         "x": "O segundo <code>else</code> é do <code>if chuva</code> e precisa ficar no mesmo recuo dele. No recuo de dentro, sobram dois <code>else</code> para o mesmo <code>if</code>."},
        {"k": "conceito", "pergunta": "Quando vale a pena colocar um <code>if</code> dentro de outro?",
         "opcoes": ["Quando a segunda pergunta só faz sentido se a primeira for verdadeira", "Sempre que houver mais de duas condições", "Nunca: é sempre melhor usar and", "Quando o programa tem laço"],
         "correta": 0,
         "x": "Exemplo: \"está logado?\" e, só então, \"é admin?\". Se as perguntas são independentes, <code>and</code> ou <code>elif</code> costumam ficar mais simples."},
        {"k": "conceito", "pergunta": "IMC: abaixo de 18.5 é magreza, abaixo de 25 é normal, abaixo de 30 é sobrepeso e o resto, obesidade. Usando <code>&lt;</code> numa cadeia de elif, qual ordem funciona?",
         "opcoes": ["&lt; 18.5, depois &lt; 25, depois &lt; 30, e else", "&lt; 30, depois &lt; 25, depois &lt; 18.5, e else", "Qualquer ordem dá o mesmo resultado", "&lt; 25, depois &lt; 18.5, depois &lt; 30, e else"],
         "correta": 0,
         "x": "Com <code>&lt;</code>, teste do menor limite para o maior. Se começar por &lt; 30, um IMC de 17 já cairia em sobrepeso."},
    ],

    "Laços (for, while)": [
        {"k": "saida", "codigo": c('''
            for i in range(2, 11, 3):
                print(i)
         '''),
         "opcoes": ["2\n5\n8", "2\n5\n8\n11", "3\n6\n9", "2\n3\n4"],
         "correta": 0,
         "x": "Começa em 2 e soma 3 a cada volta: 2, 5, 8. O 11 é o fim e não entra."},
        {"k": "saida", "codigo": c('''
            total = 0
            for n in [3, 1, 4]:
                total = total + n
            print(total)
         '''),
         "opcoes": ["8", "3\n4\n8", "4", "[3, 1, 4]"],
         "correta": 0,
         "x": "O laço acumula: 0 + 3 + 1 + 4 = 8. O <code>print</code> está fora do laço (sem recuo), então roda uma vez só."},
        {"k": "saida", "codigo": c('''
            x = 1
            while x < 20:
                x = x * 3
            print(x)
         '''),
         "opcoes": ["9", "27", "20", "81"],
         "correta": 1,
         "x": "x passa por 1, 3, 9 e 27. Com 27, a condição <code>x &lt; 20</code> fica falsa e o laço para."},
        {"k": "saida", "codigo": c('''
            for epoca in range(2):
                for lote in range(3):
                    pass
                print("época", epoca, "lote", lote)
         '''),
         "opcoes": ["época 0 lote 2\népoca 1 lote 2", "época 1 lote 2", "época 0 lote 3\népoca 1 lote 3", "época 2 lote 3"],
         "correta": 0,
         "x": "Como no treino de um modelo: cada época percorre todos os lotes (0, 1, 2). O print fica no laço de fora e mostra o último lote de cada época."},
        {"k": "lacuna", "pergunta": "Complete para mostrar 10, 8, 6, 4 e 2, um por linha.",
         "codigo": c('''
            for i in range(10, 0, ____):
                print(i)
         '''),
         "opcoes": ["-2", "2", "-1", "0"], "correta": 0, "saida": "10\n8\n6\n4\n2",
         "x": "Para descer, o passo é negativo: -2. Com passo 2 nada roda (já começa acima do fim), com -1 sairiam todos e passo 0 dá erro."},
        {"k": "lacuna", "pergunta": "Complete para a contagem terminar: deve mostrar 3, 2, 1 e Fogo!",
         "codigo": c('''
            n = 3
            while n > 0:
                print(n)
                ____
            print("Fogo!")
         '''),
         "opcoes": ["n = n - 1", "n = n + 1", "n - 1", "n == n - 1"], "correta": 0, "saida": "3\n2\n1\nFogo!",
         "x": "Algo dentro do laço precisa levar a condição a ficar falsa. <code>n - 1</code> sozinho calcula, mas não guarda; as outras opções deixam o laço infinito."},
        {"k": "erro", "indentacao": True, "codigo": c('''
            i = 0
            while i < 3:
                print("treino", i)
            i = i + 1
         '''),
         "linha": 4, "correcao": "    i = i + 1", "saida": "treino 0\ntreino 1\ntreino 2",
         "x": "Sem recuo, o <code>i = i + 1</code> fica fora do laço: i nunca muda e o laço é infinito. Recue a linha para ela fazer parte do while."},
        {"k": "erro", "pergunta": "Deveria mostrar a soma de 1 a 4 (10), mas mostra 4. Qual linha está errada?",
         "codigo": c('''
            soma = 0
            for n in range(1, 5):
                soma = n
            print("Soma de 1 a 4:", soma)
         '''),
         "linha": 3, "correcao": "    soma = soma + n", "saida": "Soma de 1 a 4: 10",
         "x": "<code>soma = n</code> troca o valor a cada volta e sobra só o último. Para acumular, some ao que já tinha: <code>soma = soma + n</code>."},
        {"k": "conceito", "pergunta": "Quantas vezes roda <code>for i in range(5, 15, 5)</code>?",
         "opcoes": ["2", "3", "10", "15"],
         "correta": 0,
         "x": "i vale 5 e depois 10. O 15 é o fim e não entra: 2 voltas."},
        {"k": "conceito", "pergunta": "Qual é o jeito mais simples de passar por cada nome da lista <code>nomes</code>?",
         "opcoes": ["<code>for nome in nomes:</code>", "<code>for i in nomes[i]:</code>", "<code>while nomes:</code>", "<code>for nomes in nome:</code>"],
         "correta": 0,
         "x": "O <code>for</code> percorre a lista entregando um item por volta. Não precisa de índice nem de contador."},
    ],

    "Repetir enquanto (while)": [
        {"k": "saida", "codigo": c('''
            saldo = 100
            meses = 0
            while saldo < 150:
                saldo = saldo * 1.25
                meses = meses + 1
            print(meses)
         '''),
         "opcoes": ["1", "2", "3", "150"],
         "correta": 1,
         "x": "100 vira 125 (1 mês) e depois 156.25 (2 meses). Aí <code>saldo &lt; 150</code> fica falso."},
        {"k": "saida", "codigo": c('''
            n = 10
            while n > 10:
                print(n)
                n = n - 1
            print("fim")
         '''),
         "opcoes": ["fim", "10\nfim", "(nada aparece)", "10\n9\nfim"],
         "correta": 0,
         "x": "A condição já começa falsa (10 não é maior que 10), então o laço roda zero vezes. Só o <code>print(\"fim\")</code> aparece."},
        {"k": "saida", "codigo": c('''
            x = 64
            passos = 0
            while x > 1:
                x = x // 2
                passos = passos + 1
            print(passos, x)
         '''),
         "opcoes": ["6 1", "5 2", "7 0", "6 0"],
         "correta": 0,
         "x": "64, 32, 16, 8, 4, 2, 1: são 6 divisões até chegar a 1, quando o laço para."},
        {"k": "saida", "pergunta": "A pessoa digita 5, depois 3, depois 0. O que aparece na tela?",
         "codigo": c('''
            total = 0
            valor = int(input("Valor: "))
            while valor != 0:
                total = total + valor
                valor = int(input("Valor: "))
            print("Total:", total)
         '''), "entradas": ["5", "3", "0"],
         "opcoes": ["Valor: 5\nValor: 3\nValor: 0\nTotal: 8", "Valor: 5\nValor: 3\nTotal: 8", "Valor: 5\nValor: 3\nValor: 0\nTotal: 0", "Valor: 5\nValor: 3\nValor: 0\nTotal: 5"],
         "correta": 0,
         "x": "O 0 é o valor de parada: é lido, mas o laço termina antes de somá-lo. Total: 5 + 3 = 8."},
        {"k": "lacuna", "pergunta": "Complete para o laço repetir até acertar (deve mostrar <code>Acertou na tentativa 3</code>).",
         "codigo": c('''
            tentativas = 0
            acertou = False
            while ____:
                tentativas = tentativas + 1
                if tentativas == 3:
                    acertou = True
            print("Acertou na tentativa", tentativas)
         '''),
         "opcoes": ["not acertou", "acertou", "acertou == True", "tentativas < 5"], "correta": 0, "saida": "Acertou na tentativa 3",
         "x": "Repita enquanto ainda <b>não</b> acertou: <code>not acertou</code>. Com <code>acertou</code> o laço nem começa; com <code>tentativas &lt; 5</code> ele iria até 5."},
        {"k": "lacuna", "pergunta": "n deve dobrar até passar de 100. Complete para mostrar <code>128</code>.",
         "codigo": c('''
            n = 1
            while n <= 100:
                n = n ____ 2
            print(n)
         '''),
         "opcoes": ["*", "+", "**", "//"], "correta": 0, "saida": "128",
         "x": "Dobrar é multiplicar por 2: 1, 2, 4, …, 64, 128. Com <code>+</code> pararia em 101; com <code>**</code> e <code>//</code>, n nunca passa de 100 e o laço fica infinito."},
        {"k": "erro", "codigo": c('''
            contador = 10
            while contador > 0:
                print(contador)
                contador = contador + 1
            print("Decolar!")
         '''),
         "linha": 4, "correcao": "    contador = contador - 1", "saida": "10\n9\n8\n7\n6\n5\n4\n3\n2\n1\nDecolar!",
         "x": "Somando, o contador só cresce e nunca fica menor que 1: laço infinito. Para a contagem regressiva, subtraia."},
        {"k": "erro", "pergunta": "A pessoa digita 0000 e depois 1234. Em qual linha está o erro?",
         "codigo": c('''
            senha = ""
            while senha = "1234":
                senha = input("Senha: ")
            print("Entrou!")
         '''), "entradas": ["0000", "1234"],
         "linha": 2, "correcao": 'while senha != "1234":', "saida": "Senha: 0000\nSenha: 1234\nEntrou!",
         "x": "O laço deve repetir enquanto a senha for <b>diferente</b> da certa: <code>!=</code>. Um <code>=</code> só é erro de sintaxe."},
        {"k": "conceito", "pergunta": "Quais são as três partes de um while que termina?",
         "opcoes": ["Valor inicial, condição e um passo que muda a variável dentro do laço", "Um import, uma lista e um print", "Condição, break e else", "Só a condição; o Python cuida do resto"],
         "correta": 0,
         "x": "Exemplo: <code>n = 3</code> (início), <code>while n &gt; 0</code> (condição) e <code>n = n - 1</code> (passo). Sem o passo, o laço não termina."},
        {"k": "conceito", "pergunta": "O que é um valor de parada (sentinela)?",
         "opcoes": ["Um valor especial, como 0 ou \"sair\", que avisa o laço para terminar", "O último número de um range", "Um erro que o Python mostra quando o laço é infinito", "A variável que conta as voltas"],
         "correta": 0,
         "x": "Útil quando você não sabe quantos dados virão: o laço lê até chegar o valor combinado. E o sentinela não entra na conta."},
    ],

    "Interromper laços (break) e f-strings": [
        {"k": "saida", "codigo": c('''
            for n in [4, 7, 0, 9]:
                if n == 0:
                    break
                print(n)
         '''),
         "opcoes": ["4\n7", "4\n7\n0", "4\n7\n9", "4"],
         "correta": 0,
         "x": "Quando chega no 0, o <code>break</code> encerra o laço na hora: nem o 0 nem o 9 são impressos."},
        {"k": "saida", "codigo": c('''
            nome = "Ana"
            nota = 8.456
            print(f"{nome}: {nota:.1f} ({nota:.0f})")
         '''),
         "opcoes": ["Ana: 8.5 (8)", "Ana: 8.4 (8)", "Ana: 8.5 (8.456)", "{nome}: 8.5 (8)"],
         "correta": 0,
         "x": "<code>:.1f</code> arredonda para 1 casa (8.5) e <code>:.0f</code> para nenhuma (8)."},
        {"k": "saida", "codigo": c('''
            i = 0
            while True:
                i = i + 1
                if i * i > 30:
                    break
            print(i)
         '''),
         "opcoes": ["5", "6", "30", "36"],
         "correta": 1,
         "x": "5 × 5 = 25 ainda não passa de 30; 6 × 6 = 36 passa, e o <code>break</code> sai com i = 6."},
        {"k": "saida", "codigo": c('''
            for i in range(3):
                for j in range(3):
                    if j == 1:
                        break
                    print(i, j)
         '''),
         "opcoes": ["0 0", "0 0\n1 0\n2 0", "0 0\n0 1\n1 0", "0 0\n1 0\n2 0\n3 0"],
         "correta": 1,
         "porques": ["O break sai só do laço de dentro; o de fora continua.", "", "Com j == 1 o break acontece antes do print.", "range(3) vai só até 2."],
         "x": "O <code>break</code> encerra apenas o laço onde ele está (o do j). O laço do i continua e faz as 3 voltas."},
        {"k": "saida", "codigo": c('''
            print(f"{3.14159:.3f}")
         '''),
         "opcoes": ["3.141", "3.142", "3.14", "3.1416"],
         "correta": 1,
         "x": "<code>:.3f</code> mostra 3 casas e arredonda: 3.14159 vira 3.142."},
        {"k": "lacuna", "pergunta": "A pessoa digita 4, 6 e 0. Complete para o programa mostrar a soma até o 0.",
         "codigo": c('''
            total = 0
            while True:
                v = int(input("N: "))
                if v == 0:
                    ____
                total = total + v
            print("Soma:", total)
         '''), "entradas": ["4", "6", "0"],
         "opcoes": ["break", "continue", "pass", "exit"], "correta": 0, "saida": "N: 4\nN: 6\nN: 0\nSoma: 10",
         "x": "<code>while True</code> só termina com <code>break</code>. <code>continue</code> e <code>pass</code> deixam o laço seguir pedindo números; <code>exit</code> sem parênteses não faz nada."},
        {"k": "lacuna", "pergunta": "Complete para mostrar <code>café: R$ 4.50</code>.",
         "codigo": c('''
            item = "café"
            preco = 4.5
            print(____"{item}: R$ {preco:.2f}")
         '''),
         "opcoes": ["f", "r", "s", "b"], "correta": 0, "saida": "café: R$ 4.50",
         "x": "O <code>f</code> antes das aspas transforma o texto em f-string e faz as chaves funcionarem. Com <code>r</code>, as chaves sairiam como texto."},
        {"k": "erro", "pergunta": "A pessoa digita 8, 6 e -1 (para sair). Em qual linha está o erro?",
         "codigo": c('''
            total = 0
            qtd = 0
            while True:
                n = float(input("Nota: "))
                if n < 0:
                    continue
                total = total + n
                qtd = qtd + 1
            print(f"Média: {total / qtd:.1f}")
         '''), "entradas": ["8", "6", "-1"],
         "linha": 6, "correcao": "        break", "saida": "Nota: 8\nNota: 6\nNota: -1\nMédia: 7.0",
         "x": "<code>continue</code> volta para o começo do laço e pede outra nota sem parar nunca. Para sair ao ler o -1, use <code>break</code>."},
        {"k": "erro", "codigo": c('''
            for tentativa in range(1, 4):
                print(f"Tentativa {tentativa}")
                if tentativa == 2:
                    print("Acertou!")
                    brake
         '''),
         "linha": 5, "correcao": "        break", "saida": "Tentativa 1\nTentativa 2\nAcertou!",
         "x": "Erro de digitação: <code>brake</code> não existe (<code>NameError</code>). A palavra é <code>break</code>."},
        {"k": "conceito", "pergunta": "Por que todo <code>while True</code> precisa de um <code>break</code>?",
         "opcoes": ["Porque a condição True nunca fica falsa; sem break o laço não termina", "Porque o Python exige, senão dá erro de sintaxe", "Para o laço rodar mais rápido", "Não precisa: o while True para sozinho no fim da lista"],
         "correta": 0,
         "x": "<code>while True</code> é um laço sem condição de saída. O <code>break</code>, dentro de um <code>if</code>, é a porta de saída."},
    ],

    # ------------------------------------------------------------------ Estruturas de dados
    "Tuplas e conjuntos": [
        {"k": "saida", "codigo": c('''
            ponto = (3, 4)
            x, y = ponto
            print(x + y, len(ponto))
         '''),
         "opcoes": ["7 2", "(3, 4) 2", "34 2", "7 1"],
         "correta": 0,
         "x": "Desempacotar coloca cada valor da tupla numa variável: x = 3 e y = 4. A tupla tem 2 itens."},
        {"k": "saida", "codigo": c('''
            cores = {"azul", "verde", "azul", "rosa"}
            print(len(cores))
         '''),
         "opcoes": ["4", "3", "2", "TypeError"],
         "correta": 1,
         "x": "Conjunto não guarda repetidos: o segundo \"azul\" some. Sobram azul, verde e rosa."},
        {"k": "saida", "codigo": c('''
            a = {1, 2, 3, 4}
            b = {3, 4, 5}
            print(a & b, a - b)
         '''),
         "opcoes": ["{3, 4} {1, 2}", "{1, 2, 3, 4, 5} {1, 2}", "{3, 4} {5}", "{1, 2} {3, 4}"],
         "correta": 0,
         "x": "<code>&amp;</code> é a interseção (o que está nos dois) e <code>-</code> é a diferença (o que está em a e não em b)."},
        {"k": "saida", "codigo": c('''
            t = (1, 2, 3)
            t[0] = 10
            print(t)
         '''),
         "opcoes": ["(10, 2, 3)", "TypeError", "(1, 2, 3)", "[10, 2, 3]"],
         "correta": 1,
         "x": "Tupla é imutável: depois de criada, não dá para trocar itens. Por isso ela é ótima para dados que não devem mudar."},
        {"k": "lacuna", "pergunta": "Complete para listar quem está em pelo menos uma das turmas: <code>['ana', 'bia', 'caio', 'davi']</code>.",
         "codigo": c('''
            turma_a = {"ana", "bia", "caio"}
            turma_b = {"bia", "davi"}
            print(sorted(turma_a ____ turma_b))
         '''),
         "opcoes": ["|", "&", "-", "+"], "correta": 0, "saida": "['ana', 'bia', 'caio', 'davi']",
         "x": "<code>|</code> é a união: junta os dois conjuntos sem repetir a Bia. <code>&amp;</code> daria só quem está nos dois, e conjuntos não se somam com <code>+</code>."},
        {"k": "lacuna", "pergunta": "Complete para contar quantos valores diferentes há na lista (deve mostrar <code>3</code>).",
         "codigo": c('''
            nums = [3, 1, 3, 2, 1, 3]
            unicos = ____(nums)
            print(len(unicos))
         '''),
         "opcoes": ["set", "list", "tuple", "sorted"], "correta": 0, "saida": "3",
         "x": "<code>set(lista)</code> joga fora os repetidos: sobram 1, 2 e 3. As outras opções mantêm os 6 itens."},
        {"k": "erro", "codigo": c('''
            coordenadas = (10, 20)
            x, y, z = coordenadas
            print(len(coordenadas), x + y)
         '''),
         "linha": 2, "correcao": "x, y = coordenadas", "saida": "2 30",
         "x": "A tupla tem 2 valores, mas a linha pede 3 variáveis (<code>ValueError</code>). Para desempacotar, a quantidade precisa bater."},
        {"k": "erro", "codigo": c('''
            tags = {"python", "ia"}
            tags.append("dados")
            tags.add("ia")
            print(len(tags), sorted(tags))
         '''),
         "linha": 2, "correcao": 'tags.add("dados")', "saida": "3 ['dados', 'ia', 'python']",
         "x": "Conjunto não tem <code>append</code> (isso é de lista): use <code>add</code>. E repare na linha 3: adicionar \"ia\" de novo não muda nada."},
        {"k": "conceito", "pergunta": "Por que funções costumam devolver tuplas, como <code>return minimo, maximo</code>?",
         "opcoes": ["Porque dá para devolver vários valores de uma vez e desempacotar: <code>a, b = f()</code>", "Porque tuplas são mais rápidas de imprimir", "Porque funções não podem devolver listas", "Porque a tupla se ordena sozinha"],
         "correta": 0,
         "x": "<code>return a, b</code> cria uma tupla, e quem chama a função recebe cada valor numa variável."},
        {"k": "conceito", "pergunta": "Qual destes NÃO pode ser item de um conjunto?",
         "opcoes": ["<code>[1, 2]</code> (uma lista)", "<code>(1, 2)</code> (uma tupla)", "<code>\"texto\"</code>", "<code>3.5</code>"],
         "correta": 0,
         "x": "Itens de conjunto precisam ser imutáveis. Lista pode mudar, então não entra (<code>TypeError: unhashable type</code>); tupla, texto e número entram."},
    ],

    "Listas e fatiamento": [
        {"k": "saida", "codigo": c('''
            v = [4, 5, 6, 7]
            v.append(v[-1] * 2)
            print(v[1:4])
         '''),
         "opcoes": ["[5, 6, 7]", "[4, 5, 6]", "[5, 6, 7, 14]", "IndexError"],
         "correta": 0,
         "porques": ["", "Os índices começam em 0, então o 1 já é o 5.", "O 14 entrou mesmo na lista, só que no fim, e a fatia não chega até lá.", "Fatiar fora do tamanho não dá erro; e aqui nem sai do tamanho."],
         "x": "Depois do <code>append</code>, v é [4, 5, 6, 7, 14]. Mas o fim da fatia nunca entra: <code>v[1:4]</code> pega só as posições 1, 2 e 3."},
        {"k": "saida", "codigo": c('''
            nums = [10, 20, 30, 40, 50]
            print(nums[-2], nums[:2], nums[3:])
         '''),
         "opcoes": ["40 [10, 20] [40, 50]", "30 [10, 20] [40, 50]", "40 [10, 20, 30] [30, 40, 50]", "40 [10, 20] [50]"],
         "correta": 0,
         "x": "<code>-2</code> é o penúltimo (40). <code>[:2]</code> pega do começo até antes do 2; <code>[3:]</code>, do 3 até o fim."},
        {"k": "saida", "codigo": c('''
            a = [1, 2, 3]
            b = a[:]
            b.append(4)
            print(a, b)
         '''),
         "opcoes": ["[1, 2, 3, 4] [1, 2, 3, 4]", "[1, 2, 3] [1, 2, 3, 4]", "[1, 2, 3] [4]", "[1, 2, 3, 4] [1, 2, 3]"],
         "correta": 1,
         "x": "<code>a[:]</code> cria uma lista nova, uma cópia. Mexer em b não afeta a. Com <code>b = a</code>, as duas seriam a mesma lista."},
        {"k": "saida", "codigo": c('''
            v = [3, 1, 2]
            w = v.sort()
            print(v, w)
         '''),
         "opcoes": ["[1, 2, 3] [1, 2, 3]", "[3, 1, 2] [1, 2, 3]", "[1, 2, 3] None", "[3, 1, 2] None"],
         "correta": 2,
         "x": "<code>sort()</code> ordena a própria lista e devolve <code>None</code>. Para ganhar uma lista nova e ordenada, use <code>sorted(v)</code>."},
        {"k": "lacuna", "pergunta": "Complete para o programa mostrar <code>['maçã', 'uva', 'pera']</code>.",
         "codigo": c('''
            frutas = ["maçã", "uva"]
            frutas.____("pera")
            print(frutas)
         '''),
         "opcoes": ["append", "add", "insert", "push"], "correta": 0, "saida": "['maçã', 'uva', 'pera']",
         "x": "<code>append</code> coloca no fim. <code>add</code> é de conjunto, <code>push</code> é de outras linguagens e <code>insert</code> precisa da posição: <code>insert(2, \"pera\")</code>."},
        {"k": "lacuna", "pergunta": "Complete para mostrar os 3 primeiros: <code>[5, 8, 2]</code>.",
         "codigo": c('''
            nums = [5, 8, 2, 9, 1]
            print(nums[____])
         '''),
         "opcoes": [":3", "1:3", "0:2", "3:"], "correta": 0, "saida": "[5, 8, 2]",
         "x": "<code>[:3]</code> vai do começo até antes do índice 3: posições 0, 1 e 2."},
        {"k": "erro", "codigo": c('''
            nomes = ["Ana", "Bia", "Caio"]
            ultimo = nomes[3]
            print(ultimo)
         '''),
         "linha": 2, "correcao": "ultimo = nomes[-1]", "saida": "Caio",
         "x": "Com 3 itens, os índices vão de 0 a 2: <code>nomes[3]</code> dá <code>IndexError</code>. O último é sempre <code>nomes[-1]</code>."},
        {"k": "erro", "codigo": c('''
            notas = [7, 9, 6]
            notas = notas.append(10)
            print(len(notas))
         '''),
         "linha": 2, "correcao": "notas.append(10)", "saida": "4",
         "x": "<code>append</code> muda a lista e devolve <code>None</code>. Guardando o resultado, <code>notas</code> vira None e o <code>len</code> quebra."},
        {"k": "conceito", "pergunta": "Qual a diferença entre <code>v.sort()</code> e <code>sorted(v)</code>?",
         "opcoes": ["<code>v.sort()</code> muda a própria lista e devolve None; <code>sorted(v)</code> devolve uma lista nova e não mexe em v", "Nenhuma", "<code>sorted</code> só funciona com números", "<code>v.sort()</code> ordena do maior para o menor"],
         "correta": 0,
         "x": "Use <code>sorted(v)</code> quando quiser manter a original; use <code>v.sort()</code> quando puder alterar a própria lista."},
        {"k": "conceito", "pergunta": "Como saber se \"uva\" está na lista <code>frutas</code>?",
         "opcoes": ['<code>"uva" in frutas</code>', '<code>frutas.has("uva")</code>', '<code>frutas.find("uva")</code>', '<code>frutas["uva"]</code>'],
         "correta": 0,
         "x": "<code>in</code> devolve True ou False. Lista não tem <code>has</code> nem <code>find</code>, e o índice de lista é um número, não um nome."},
    ],

    "Listas compostas (listas dentro de listas)": [
        {"k": "saida", "codigo": c('''
            m = [[1, 2, 3],
                 [4, 5, 6]]
            print(m[1][0], m[0][2], len(m))
         '''),
         "opcoes": ["4 3 2", "2 4 2", "4 3 3", "2 3 6"],
         "correta": 0,
         "x": "<code>m[linha][coluna]</code>: m[1][0] é linha 1, coluna 0 (4); m[0][2] é linha 0, coluna 2 (3). E <code>len(m)</code> conta as linhas: 2."},
        {"k": "saida", "codigo": c('''
            m = [[1, 2], [3, 4], [5, 6]]
            total = 0
            for linha in m:
                total = total + linha[1]
            print(total)
         '''),
         "opcoes": ["12", "9", "21", "6"],
         "correta": 0,
         "x": "<code>linha[1]</code> é a 2ª coluna de cada linha: 2 + 4 + 6 = 12."},
        {"k": "saida", "codigo": c('''
            linha = [0, 0]
            m = [linha, linha]
            m[0][0] = 7
            print(m)
         '''),
         "opcoes": ["[[7, 0], [0, 0]]", "[[7, 0], [7, 0]]", "[[7, 7], [0, 0]]", "[[0, 0], [0, 0]]"],
         "correta": 1,
         "x": "As duas linhas são a <b>mesma</b> lista, guardada duas vezes. Mudar uma é mudar a outra. Para linhas independentes, crie cada uma: <code>[[0, 0], [0, 0]]</code>."},
        {"k": "saida", "codigo": c('''
            grade = [[1, 2], [3, 4]]
            for linha in grade:
                for x in linha:
                    print(x * 10)
         '''),
         "opcoes": ["10\n20\n30\n40", "10\n30\n20\n40", "[10, 20]\n[30, 40]", "100"],
         "correta": 0,
         "x": "O laço de fora pega cada linha; o de dentro percorre os números dela, na ordem: 1, 2, 3, 4."},
        {"k": "lacuna", "pergunta": "Complete para mostrar a nota da Bia, <code>9</code>.",
         "codigo": c('''
            tabela = [["Ana", 8], ["Bia", 9], ["Caio", 7]]
            print(tabela____)
         '''),
         "opcoes": ["[1][1]", "[1][2]", "[2][1]", "[1, 1]"], "correta": 0, "saida": "9",
         "x": "A Bia está na linha 1 (a segunda) e a nota é a coluna 1: <code>tabela[1][1]</code>. Lista não aceita <code>[1, 1]</code>."},
        {"k": "lacuna", "pergunta": "Complete para pegar a última coluna: <code>[3, 6]</code>.",
         "codigo": c('''
            m = [[1, 2, 3], [4, 5, 6]]
            coluna = []
            for linha in m:
                coluna.append(linha[____])
            print(coluna)
         '''),
         "opcoes": ["2", "1", "3", "0"], "correta": 0, "saida": "[3, 6]",
         "x": "Cada linha tem 3 itens, nas posições 0, 1 e 2. A última é a 2 (ou -1). O índice 3 não existe."},
        {"k": "erro", "pergunta": "Era para mexer só na cópia, mas m também muda (aparece 100). Qual linha causa isso?",
         "codigo": c('''
            m = [[1, 2], [3, 4]]
            copia = m
            copia[0][0] = 100
            print(m[0][0])
         '''),
         "linha": 2, "correcao": "copia = [m[0][:], m[1][:]]", "saida": "1",
         "x": "<code>copia = m</code> não copia nada: são dois nomes para a mesma lista. E cuidado: nem <code>m[:]</code> resolve aqui, porque copia só a lista de fora. É preciso copiar cada linha."},
        {"k": "erro", "codigo": c('''
            m = [[5, 1], [2, 8]]
            maior = 0
            for linha in m:
                for x in m:
                    if x > maior:
                        maior = x
            print(maior)
         '''),
         "linha": 4, "correcao": "    for x in linha:", "saida": "8",
         "x": "O laço de dentro deve percorrer a <code>linha</code> atual. Percorrendo <code>m</code>, cada x é uma lista, e comparar lista com número dá <code>TypeError</code>."},
        {"k": "conceito", "pergunta": "Numa lista de listas <code>m</code>, o que <code>m[2]</code> devolve?",
         "opcoes": ["A 3ª linha inteira (uma lista)", "O 3º número da primeira linha", "A 3ª coluna", "O número 2"],
         "correta": 0,
         "x": "Com um índice só, você pega uma linha inteira. Para um número, são dois índices: <code>m[2][0]</code>."},
        {"k": "conceito", "pergunta": "Uma imagem em tons de cinza de 28 × 28 pixels, guardada como lista de listas, tem quantos números?",
         "opcoes": ["784", "56", "28", "2"],
         "correta": 0,
         "x": "28 linhas com 28 números cada: 28 × 28 = 784. É assim que redes neurais recebem imagens (como no conjunto MNIST)."},
    ],

    "Dicionários": [
        {"k": "saida", "codigo": c('''
            aluno = {"nome": "Ana", "nota": 8}
            aluno["nota"] = 9
            aluno["curso"] = "IA"
            print(len(aluno), aluno["nota"])
         '''),
         "opcoes": ["3 9", "2 9", "3 8", "4 9"],
         "correta": 0,
         "x": "<code>d[k] = v</code> altera a chave se ela existe (nota vira 9) e cria se não existe (curso). Ficam 3 chaves."},
        {"k": "saida", "codigo": c('''
            estoque = {"maçã": 3}
            print(estoque.get("pera", 0), estoque.get("maçã", 0))
         '''),
         "opcoes": ["0 3", "None 3", "KeyError", "pera 3"],
         "correta": 0,
         "x": "<code>get(chave, padrão)</code> devolve o padrão (0) quando a chave não existe, sem quebrar o programa."},
        {"k": "saida", "codigo": c('''
            precos = {"café": 4, "pão": 1}
            total = 0
            for item, preco in precos.items():
                total = total + preco
            print(total)
         '''),
         "opcoes": ["5", "café pão", "2", "TypeError"],
         "correta": 0,
         "x": "<code>items()</code> entrega um par (chave, valor) por volta. Somando os valores: 4 + 1 = 5."},
        {"k": "saida", "codigo": c('''
            d = {"a": 1}
            print(d["b"])
         '''),
         "opcoes": ["None", "KeyError", "0", "b"],
         "correta": 1,
         "x": "Ler com colchetes uma chave que não existe quebra o programa (<code>KeyError</code>). Para ler com segurança: <code>d.get(\"b\")</code>."},
        {"k": "saida", "codigo": c('''
            cont = {}
            for p in "o gato e o rato".split():
                cont[p] = cont.get(p, 0) + 1
            print(cont["o"], len(cont))
         '''),
         "opcoes": ["2 4", "2 5", "1 4", "3 4"],
         "correta": 0,
         "x": "As palavras são o, gato, e, o, rato: \"o\" aparece 2 vezes e há 4 palavras diferentes. É o jeito clássico de contar com dicionário."},
        {"k": "lacuna", "pergunta": "Complete para mostrar <code>Ana 30</code> e <code>Bia 25</code>.",
         "codigo": c('''
            idades = {"Ana": 30, "Bia": 25}
            for nome in idades:
                print(nome, idades____)
         '''),
         "opcoes": ["[nome]", ".nome", "(nome)", "[0]"], "correta": 0, "saida": "Ana 30\nBia 25",
         "x": "Percorrer o dicionário entrega as chaves; o valor se lê com <code>idades[nome]</code>. Dicionário não tem posição 0."},
        {"k": "lacuna", "pergunta": "Complete para ler \"batch\" e usar 32 se a chave não existir.",
         "codigo": c('''
            config = {"lr": 0.01, "epocas": 10}
            print(config.____("batch", 32))
         '''),
         "opcoes": ["get", "items", "keys", "find"], "correta": 0, "saida": "32",
         "x": "<code>get</code> aceita um valor padrão para chave ausente. <code>items</code> e <code>keys</code> não recebem argumentos, e dicionário não tem <code>find</code>."},
        {"k": "erro", "codigo": c('''
            pessoa = {"nome": "Caio", "idade": 40}
            print(pessoa[nome])
         '''),
         "linha": 2, "correcao": 'print(pessoa["nome"])', "saida": "Caio",
         "x": "A chave é o texto \"nome\", com aspas. Sem aspas, o Python procura uma variável chamada nome (<code>NameError</code>)."},
        {"k": "erro", "pergunta": "Era para contar os votos ({'sim': 2, 'não': 1}), mas tudo fica 0. Qual linha está errada?",
         "codigo": c('''
            votos = {"sim": 0, "não": 0}
            for v in ["sim", "não", "sim"]:
                votos[v] + 1
            print(votos)
         '''),
         "linha": 3, "correcao": "    votos[v] = votos[v] + 1", "saida": "{'sim': 2, 'não': 1}",
         "x": "<code>votos[v] + 1</code> calcula, mas não guarda. É preciso atribuir: <code>votos[v] = votos[v] + 1</code> (ou <code>votos[v] += 1</code>)."},
        {"k": "conceito", "pergunta": "A resposta de uma API em JSON vira o quê no Python?",
         "opcoes": ["Dicionários e listas, que podem estar um dentro do outro", "Uma tupla", "Uma string que não dá para ler", "Um conjunto"],
         "correta": 0,
         "x": "Objetos JSON viram dicionários e arrays viram listas. Por isso <code>dados[\"itens\"][0][\"nome\"]</code> é tão comum."},
    ],

    "List comprehension": [
        {"k": "saida", "codigo": c('''
            print([x * x for x in range(1, 5)])
         '''),
         "opcoes": ["[1, 4, 9, 16]", "[0, 1, 4, 9, 16]", "[1, 4, 9, 16, 25]", "[2, 4, 6, 8]"],
         "correta": 0,
         "x": "range(1, 5) vai de 1 a 4; cada x vira x * x."},
        {"k": "saida", "codigo": c('''
            print([n for n in [3, 8, 5, 10] if n > 4])
         '''),
         "opcoes": ["[8, 5, 10]", "[8, 10]", "[5, 8, 10]", "[False, True, True, True]"],
         "correta": 0,
         "x": "O <code>if</code> no final filtra: ficam os maiores que 4, na ordem original."},
        {"k": "saida", "codigo": c('''
            nomes = ["ana", "bia"]
            print([n.upper() for n in nomes])
         '''),
         "opcoes": ["['ANA', 'BIA']", "['Ana', 'Bia']", "ANA BIA", "[ANA, BIA]"],
         "correta": 0,
         "x": "Cada nome é transformado com <code>upper()</code>, e o resultado é uma lista nova de textos."},
        {"k": "saida", "codigo": c('''
            print(["par" if n % 2 == 0 else "ímpar" for n in [1, 2, 3]])
         '''),
         "opcoes": ["['ímpar', 'par', 'ímpar']", "['par']", "['ímpar', 'ímpar']", "SyntaxError"],
         "correta": 0,
         "x": "Aqui o if/else fica na <b>frente</b> e escolhe o que colocar para cada item. Ninguém é filtrado. O <code>if</code> no final, sem else, é que filtra."},
        {"k": "saida", "codigo": c('''
            print(len([x for x in range(10) if x % 3 == 0]))
         '''),
         "opcoes": ["3", "4", "10", "[0, 3, 6, 9]"],
         "correta": 1,
         "x": "De 0 a 9, os múltiplos de 3 são 0, 3, 6 e 9: 4 números (o 0 também conta)."},
        {"k": "lacuna", "pergunta": "Complete para aplicar 10% de desconto: <code>[9.0, 18.0, 27.0]</code>.",
         "codigo": c('''
            precos = [10, 20, 30]
            com_desconto = [____ for p in precos]
            print(com_desconto)
         '''),
         "opcoes": ["p * 0.9", "p - 0.1", "p * 0.1", "precos * 0.9"], "correta": 0, "saida": "[9.0, 18.0, 27.0]",
         "x": "Pagar 90% é multiplicar por 0.9. <code>p * 0.1</code> daria só o desconto, e <code>precos * 0.9</code> tenta multiplicar a lista inteira (erro)."},
        {"k": "lacuna", "pergunta": "Complete para ficar só com as palavras de mais de 2 letras: <code>['python', 'dados']</code>.",
         "codigo": c('''
            palavras = ["ia", "python", "dados", "ml"]
            longas = [p for p in palavras ____]
            print(longas)
         '''),
         "opcoes": ["if len(p) > 2", "if p > 2", "len(p) > 2", "if len(p) >= 2"], "correta": 0, "saida": "['python', 'dados']",
         "x": "O filtro é <code>if</code> + condição no final. Comparar texto com número dá erro, e com <code>&gt;= 2</code> o \"ia\" e o \"ml\" também entrariam."},
        {"k": "erro", "codigo": c('''
            nums = [1, 2, 3, 4]
            dobros = [for n in nums: n * 2]
            print(dobros)
         '''),
         "linha": 2, "correcao": "dobros = [n * 2 for n in nums]", "saida": "[2, 4, 6, 8]",
         "x": "Na list comprehension, o que fazer vem primeiro: <code>[n * 2 for n in nums]</code>. E não há dois-pontos."},
        {"k": "erro", "pergunta": "Quem tira 5 ou mais é aprovado, então deveria aparecer 3 aprovadas de 4. Qual linha está errada?",
         "codigo": c('''
            notas = [7, 4, 9, 5]
            aprovadas = [n for n in notas if n > 5]
            print(len(aprovadas), "aprovadas de", len(notas))
         '''),
         "linha": 2, "correcao": "aprovadas = [n for n in notas if n >= 5]", "saida": "3 aprovadas de 4",
         "x": "\"5 ou mais\" é <code>&gt;= 5</code>. Com <code>&gt; 5</code>, quem tirou exatamente 5 fica de fora."},
        {"k": "conceito", "pergunta": "Qual list comprehension faz o mesmo que este laço?",
         "codigo": c('''
            r = []
            for x in v:
                if x != 0:
                    r.append(1 / x)
         '''),
         "opcoes": ["<code>r = [1 / x for x in v if x != 0]</code>", "<code>r = [x != 0 for x in v if 1 / x]</code>", "<code>r = [1 / x if x != 0 for x in v]</code>", "<code>r = [for x in v if x != 0: 1 / x]</code>"],
         "correta": 0,
         "x": "Leia como frase: \"1 / x, para cada x em v, se x for diferente de 0\". O que fazer vem primeiro; o filtro, no final."},
    ],
}
