# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · aulas do curso de Python do Guanabara que faltavam na Fase 1 (ver trilha_guanabara.py).

Até a aula de Funções os exercícios não usam def: o curso só apresenta funções na aula 20.
"""
from lesson_factory import *

AULAS = {}

# ---------------------------------------------------------------------------------------------
AULAS["Operadores aritméticos"] = aula(
    30,
    "Média, porcentagem, quantos lotes cabem num treino: quase todo programa faz conta. O Python tem sete operadores e uma <b>ordem</b> para eles, e é na ordem que quase todo iniciante escorrega.",
    ["usar os sete operadores aritméticos;", "prever a ordem em que o Python calcula;", "usar <code>//</code> e <code>%</code> para dividir em grupos."],
    ["Variáveis e tipos."],
    [
        chute("O que o código imprime?", ["25", "17", "256"], 1,
              ["Seria 25 se a soma viesse antes da multiplicação.", "Isso! A potência primeiro (4), depois a multiplicação (12), por fim a soma (17).", "O Python não calcula simplesmente da esquerda para a direita."],
              "Primeiro parênteses, depois potência, depois multiplicação e divisões, por último soma e subtração.",
              cod="print(5 + 3 * 2 ** 2)"),
        concreto("A fila de prioridade do banco",
                 "<p>Não importa quem chegou primeiro: a prioridade passa na frente. Os <b>parênteses</b> são a senha preferencial, depois vem <code>**</code>, depois <code>* / // %</code> e, no fim, <code>+ -</code>.</p>"),
        crianca("<p>Você tem 17 balas e 5 amigos. Cada um ganha 3 (<code>17 // 5</code>) e sobram 2 na sua mão (<code>17 % 5</code>).</p>"),
        ver("a ordem de precedência dos operadores"),
        nota("Os operadores", [
            ("<code>+ - *</code>", "mais, menos, vezes", "Soma, subtração e multiplicação."),
            ("<code>/</code>", "dividido por", "Divisão. O resultado é sempre <code>float</code>."),
            ("<code>//</code>", "divisão inteira", "Quantas vezes cabe inteiro: <code>17 // 5</code> é 3."),
            ("<code>%</code>", "resto", "O que sobra: <code>17 % 5</code> é 2."),
            ("<code>**</code>", "elevado a", "Potência: <code>2 ** 3</code> é 8. Para raiz quadrada, <code>x ** (1/2)</code>."),
        ]),
        passos("Transformando 135 minutos em horas", [
            ("<code>horas = 135 // 60</code>", "Cabem 2 horas inteiras."),
            ("<code>minutos = 135 % 60</code>", "Sobram 15 minutos."),
            ("<code>print(horas, minutos)</code>", "Mostra 2 15."),
        ]),
        cod("Lotes de treino", "Você tem 1050 exemplos e treina em lotes de 32. Calcule <code>completos</code> (lotes cheios) e <code>sobra</code> (exemplos que sobraram).",
            '''
exemplos = 1050
lote = 32

completos = 0
sobra = 0

print(completos, sobra)
''',
            [("Lotes completos", "assert completos == 32, f'completos = {completos!r}'"),
             ("Sobra", "assert sobra == 26, f'sobra = {sobra!r}'")],
            '''
exemplos = 1050
lote = 32

completos = exemplos // lote
sobra = exemplos % lote

print(completos, sobra)
''', ["Quantos cabem inteiros: <code>//</code>.", "O que sobra: <code>%</code>."]),
        erros([
            ("<code>2 ^ 3</code> para potência.", "Use <code>2 ** 3</code>. Em Python, <code>^</code> é outra operação (bits)."),
            ("<code>n1 + n2 / 2</code> para média.", "A divisão acontece antes. Use <code>(n1 + n2) / 2</code>."),
            ("Esperar que <code>4 / 2</code> dê um inteiro.", "Dá <code>2.0</code>. Se precisa de inteiro, use <code>//</code>."),
        ]),
        ponte("Contas em IA",
              "<p>Acurácia é <code>acertos / total * 100</code>. O número de lotes usa <code>//</code>. O <code>%</code> faz o “salve o modelo a cada 10 épocas”: <code>if epoca % 10 == 0</code>.</p>"),
        quiz([
            ("Quanto é <code>19 // 4</code>?", ["4.75", "4", "3"], 1, "O 4 cabe 4 vezes inteiras em 19."),
            ("Quanto é <code>19 % 4</code>?", ["3", "4", "0.75"], 0, "4 × 4 é 16; sobram 3."),
            ("Qual expressão calcula a média de 6 e 8?", ["<code>6 + 8 / 2</code>", "<code>(6 + 8) / 2</code>", "<code>6 + 8 // 2</code>"], 1, "Os parênteses obrigam a soma a acontecer antes."),
        ]),
    ],
    ["Precedência: parênteses, potência, multiplicação e divisões, soma e subtração.", "<code>//</code> diz quantos cabem; <code>%</code> diz quanto sobra.", "<code>/</code> sempre devolve <code>float</code>."],
    "Módulos: usar ferramentas que já vêm prontas no Python.",
    livro=("ATBS:1", "Capítulo 1, seção de operadores matemáticos", "Em que ordem o Python avalia uma expressão?"))

# ---------------------------------------------------------------------------------------------
AULAS["Usar módulos prontos (import)"] = aula(
    30,
    "Raiz quadrada, sorteio, arredondamento: alguém já escreveu e testou. Programar bem também é saber <b>importar</b> em vez de reinventar.",
    ["importar um módulo inteiro ou só uma parte;", "usar <code>math</code> e <code>random</code>;", "distinguir módulo da biblioteca padrão de pacote instalado."],
    ["Variáveis e operadores aritméticos."],
    [
        chute("O que acontece?", ["Imprime 4.0", "Dá erro", "Imprime 16"], 1,
              ["Só depois de importar.", "Isso! <code>sqrt</code> não existe no programa até você importar.", "Nada é impresso: o programa para no erro."],
              "O Python liga com pouca coisa na memória. O resto você pede com <code>import</code>.",
              cod="print(sqrt(16))"),
        concreto("A caixa de ferramentas",
                 "<p><code>import math</code> traz a caixa inteira: para pegar uma peça você diz <code>math.sqrt</code>. <code>from math import sqrt</code> tira só essa chave e deixa na sua mão: aí basta <code>sqrt</code>.</p>"),
        crianca("<p>Você não fabrica o lápis para desenhar: pega no estojo. O <code>import</code> é abrir o estojo.</p>"),
        ver("a diferença entre <code>import</code> e <code>from ... import</code>"),
        nota("Importar", [
            ("<code>import math</code>", "importe math", "Usa com prefixo: <code>math.sqrt(16)</code>."),
            ("<code>from math import sqrt</code>", "de math importe sqrt", "Usa direto: <code>sqrt(16)</code>."),
            ("<code>math.ceil(x)</code>", "teto", "Arredonda para cima."),
            ("<code>math.floor(x)</code>", "piso", "Arredonda para baixo."),
            ("<code>random.randint(1, 6)</code>", "inteiro sorteado", "Sorteia de 1 a 6, incluindo os dois extremos."),
        ]),
        passos("Distância em linha reta", [
            ("<code>import math</code>", "Traz o módulo, sempre no topo do arquivo."),
            ("<code>d = math.hypot(3, 4)</code>", "Calcula a hipotenusa: a distância depois de andar 3 e 4."),
            ("<code>print(d)</code>", "Mostra 5.0."),
        ]),
        cod("Quantos lotes, contando o incompleto?", "São 1050 exemplos em lotes de 32. Com o módulo <code>math</code>, calcule <code>lotes</code> contando também o último, incompleto.",
            '''
# importe o módulo aqui

exemplos = 1050
lotes = 0

print(lotes)
''',
            [("33 lotes", "assert lotes == 33, f'lotes = {lotes!r}'")],
            '''
import math

exemplos = 1050
lotes = math.ceil(exemplos / 32)

print(lotes)
''', ["Arredondar para cima é <code>ceil</code>."]),
        erros([
            ("Salvar o seu arquivo como <code>math.py</code> ou <code>random.py</code>.", "O Python importa o seu arquivo no lugar do módulo. Use outro nome."),
            ("<code>import math</code> e depois <code>sqrt(9)</code>.", "Com esse import é <code>math.sqrt(9)</code>."),
            ("<code>from math import *</code> em tudo.", "Esconde de onde cada nome veio. Importe pelo nome."),
        ]),
        ponte("A primeira linha de todo projeto de IA",
              "<p><code>import numpy as np</code>, <code>import torch</code>: é o mesmo mecanismo. A diferença é que esses pacotes precisam ser instalados com <code>pip</code>; <code>math</code> e <code>random</code> já vêm com o Python.</p>"),
        quiz([
            ("Depois de <code>from math import floor</code>, como usar?", ["<code>math.floor(2.7)</code>", "<code>floor(2.7)</code>", "<code>import.floor(2.7)</code>"], 1, "O nome veio direto, sem prefixo."),
            ("Quanto é <code>math.ceil(4.1)</code>?", ["4", "5", "4.1"], 1, "<code>ceil</code> sempre sobe para o próximo inteiro."),
            ("Qual destes precisa de <code>pip install</code>?", ["math", "random", "numpy"], 2, "NumPy é um pacote externo."),
        ]),
    ],
    ["<code>import modulo</code> usa prefixo; <code>from modulo import nome</code> não.", "A biblioteca padrão já vem instalada.", "Nunca dê ao seu arquivo o nome de um módulo."],
    "Strings: cortar, buscar e transformar textos.",
    livro=("ATBS:2", "Capítulo 2, seção “Importing Modules”", "Por que o prefixo do módulo ajuda quem lê o código?"))

# ---------------------------------------------------------------------------------------------
AULAS["Manipular textos (strings)"] = aula(
    35,
    "Um LLM vive de texto. Antes de virar token, todo texto é limpo, cortado e juntado com os comandos desta aula.",
    ["fatiar uma string por posição;", "transformar e limpar com métodos;", "separar e juntar com <code>split</code> e <code>join</code>."],
    ["Variáveis, <code>print</code> e operadores."],
    [
        chute("O que o código imprime?", ["Pyt", "Pyth", "yth"], 0,
              ["Isso! Posições 0, 1 e 2: o final da fatia fica de fora.", "O índice 3 não entra.", "A contagem começa em 0, não em 1."],
              "Numa fatia, o começo entra e o fim não.",
              cod='print("Python"[0:3])'),
        concreto("Letras em vagões",
                 "<p>A string é um trem com uma letra por vagão, numerado <b>a partir de 0</b>. Você pode copiar um trecho, mas não trocar um vagão: todo método devolve um <b>trem novo</b>.</p>"),
        crianca("<p>É uma palavra de bloquinhos. Contar começa no zero. Se quiser mudar uma letra, monta outra palavra.</p>"),
        ver("os métodos de transformação, divisão e junção"),
        nota("O kit de textos", [
            ("<code>s[1:4]</code>", "fatia", "Posições 1, 2 e 3."),
            ("<code>s[-1]</code>", "último", "O último caractere."),
            ("<code>s.strip()</code>", "apare", "Tira espaços das duas pontas."),
            ("<code>s.lower()</code>", "minúsculas", "Também existe <code>upper()</code>."),
            ("<code>s.replace(a, b)</code>", "substitua", "Devolve uma cópia com a troca."),
            ("<code>s.split()</code>", "separe", "Divide nos espaços e devolve as palavras numa lista."),
            ("<code>\"-\".join(partes)</code>", "junte", "Cola as partes usando o separador."),
        ]),
        passos("Primeiro nome de um cadastro bagunçado", [
            ("<code>nome = \"  ANA souza \"</code>", "Veio com espaços e caixa misturada."),
            ("<code>limpo = nome.strip().lower()</code>", "Fica “ana souza”."),
            ("<code>primeiro = limpo.split()[0]</code>", "Separa e pega a primeira palavra: “ana”."),
        ]),
        cod("Nome de arquivo do modelo", "Transforme <code>titulo</code> em <code>arquivo</code> com o valor <b>meu-modelo-de-spam</b>: sem espaços sobrando, em minúsculas, com hífen entre as palavras.",
            '''
titulo = "  Meu Modelo   de SPAM  "

arquivo = titulo

print(arquivo)
''',
            [("Nome limpo", "assert arquivo == 'meu-modelo-de-spam', f'arquivo = {arquivo!r}'")],
            '''
titulo = "  Meu Modelo   de SPAM  "

arquivo = "-".join(titulo.lower().split())

print(arquivo)
''', ["<code>split()</code> sem argumento ignora espaços repetidos.", "Depois junte com <code>\"-\".join(...)</code>."]),
        erros([
            ("<code>s.upper()</code> e achar que <code>s</code> mudou.", "Guarde o resultado: <code>s = s.upper()</code>."),
            ("Contar posições a partir de 1.", "O primeiro caractere é <code>s[0]</code>."),
            ("Comparar textos sem normalizar.", "<code>\"Ana \"</code> é diferente de <code>\"ana\"</code>. Use <code>strip()</code> e <code>lower()</code>."),
        ]),
        ponte("Texto em IA",
              "<p>Chunking de RAG é fatiamento. Montar um prompt é junção. Limpar um dataset é <code>strip</code>, <code>lower</code> e <code>replace</code> em milhões de linhas.</p>"),
        quiz([
            ("Quanto é <code>len(\"IA\")</code>?", ["1", "2", "3"], 1, "São dois caracteres."),
            ("<code>\"dados\"[-1]</code> devolve o quê?", ["d", "o", "s"], 2, "-1 é o último."),
            ("O que <code>\"a b c\".split()</code> devolve?", ["Uma lista com três textos", "O texto abc", "O número 3"], 0, "<code>split</code> sempre devolve uma lista."),
        ]),
    ],
    ["Índices começam em 0 e a fatia exclui o fim.", "Strings não mudam: os métodos devolvem cópias.", "<code>split</code> separa; <code>join</code> junta."],
    "Condições: fazer o programa tomar decisões.",
    livro=("ATBS:6", "Capítulo 6, “Manipulating Strings”", "Quais métodos você usaria para limpar um cadastro?"))

# ---------------------------------------------------------------------------------------------
AULAS["Condições aninhadas e elif"] = aula(
    30,
    "A vida raramente tem só sim ou não. Com <code>elif</code> o programa escolhe entre vários caminhos e, aninhando, faz uma pergunta dentro da outra.",
    ["encadear decisões com <code>elif</code>;", "aninhar um <code>if</code> dentro de outro;", "ordenar faixas sem deixar caso inalcançável."],
    ["Condicionais <code>if</code> e <code>else</code>."],
    [
        chute("O que o código imprime?", ["ótimo", "passou", "Os dois"], 1,
              ["É o que se queria, mas a ordem está errada.", "Isso! A primeira condição verdadeira vence, e as outras nem são testadas.", "Numa cadeia if/elif só um bloco roda."],
              "Comece pela condição mais exigente.",
              cod='nota = 9.5\nif nota >= 6:\n    print("passou")\nelif nota >= 9:\n    print("ótimo")'),
        concreto("A triagem do hospital",
                 "<p>A enfermagem pergunta do mais grave para o mais leve e <b>para no primeiro sim</b>. Dentro de “grave”, pode haver outra pergunta: precisa de cirurgia? Isso é uma condição aninhada.</p>"),
        crianca("<p>Peneiras empilhadas: a pedra para na primeira em que fica presa e não passa pelas de baixo.</p>"),
        ver("por que a ordem dos <code>elif</code> muda o resultado"),
        nota("Vários caminhos", [
            ("<code>if a:</code>", "se", "Primeiro teste."),
            ("<code>elif b:</code>", "senão, se", "Só é testado se os anteriores falharam."),
            ("<code>else:</code>", "senão", "Pega todo o resto."),
            ("<code>6 &lt;= n &lt; 9</code>", "entre", "O Python aceita comparação encadeada."),
        ]),
        passos("Classificando 7.0", [
            ("<code>if nota &gt;= 9</code>", "Falso: segue."),
            ("<code>elif nota &gt;= 6</code>", "Verdadeiro: imprime aprovado e sai da cadeia."),
            ("<code>else</code>", "Nem é avaliado."),
        ]),
        cod("Publicar ou não o modelo", "Defina <code>decisao</code>: com acurácia de pelo menos 0.9, é <b>publicar</b> se o teste de segurança passou e <b>revisar segurança</b> se não passou; de 0.7 até antes de 0.9, <b>melhorar</b>; abaixo disso, <b>refazer</b>.",
            '''
acuracia = 0.93
seguro = False

decisao = ""
# if / elif / else aqui

print(decisao)
''',
            [("Caso do exemplo", "assert decisao == 'revisar segurança', f'decisao = {decisao!r}'")],
            '''
acuracia = 0.93
seguro = False

decisao = ""
if acuracia >= 0.9:
    if seguro:
        decisao = "publicar"
    else:
        decisao = "revisar segurança"
elif acuracia >= 0.7:
    decisao = "melhorar"
else:
    decisao = "refazer"

print(decisao)
''', ["O <code>if seguro:</code> fica dentro do primeiro <code>if</code>.", "Depois troque os valores de cima e veja os outros caminhos."]),
        erros([
            ("Vários <code>if</code> soltos para faixas.", "Mais de um pode rodar. Use <code>elif</code>."),
            ("Começar pela faixa mais ampla.", "Ela engole as outras. Comece pela mais exigente."),
            ("Cinco níveis de aninhamento.", "Junte com <code>and</code> ou inverta a condição."),
        ]),
        ponte("Guardrails",
              "<p>Antes de um agente executar uma ferramenta há uma cadeia destas: é permitido? Se sim, é arriscado? Se for, peça confirmação.</p>"),
        quiz([
            ("Numa cadeia if/elif/else, quantos blocos rodam?", ["Um", "Todos os verdadeiros", "Sempre dois"], 0, "A primeira verdade encerra a cadeia."),
            ("Qual faixa testar primeiro, com <code>&gt;=</code>?", ["A menor", "A maior", "Tanto faz"], 1, "Da mais exigente para a mais ampla."),
            ("O que é condição aninhada?", ["Um if dentro de outro", "Dois programas", "Um if sem dois-pontos"], 0, "A segunda pergunta só existe dentro da primeira."),
        ]),
    ],
    ["Só um caminho da cadeia roda.", "A ordem das faixas importa.", "Aninhe quando a segunda pergunta depende da primeira."],
    "Laço for: repetir sem copiar e colar.",
    livro=("ATBS:2", "Capítulo 2, “elif Statements”", "Quando um elif nunca é executado?"))

# ---------------------------------------------------------------------------------------------
AULAS["Repetir enquanto (while)"] = aula(
    30,
    "O <code>for</code> serve quando você sabe quantas voltas dar. Quando não sabe (até acertar a senha, até o modelo parar de melhorar), é <code>while</code>.",
    ["escolher entre <code>for</code> e <code>while</code>;", "escrever um laço que termina;", "usar um valor de parada (flag)."],
    ["Condições e laço <code>for</code>."],
    [
        chute("Quantos números o código imprime?", ["2", "3", "Infinitos"], 1,
              ["O 1 também é impresso.", "Isso! 3, 2 e 1. Quando n vira 0, a condição falha.", "Seria infinito sem a linha que diminui n."],
              "A condição é conferida antes de cada volta.",
              cod="n = 3\nwhile n > 0:\n    print(n)\n    n = n - 1"),
        concreto("Encher o balde",
                 "<p>Você não conta quantos segundos leva: <b>enquanto</b> não encheu, deixa a torneira aberta. Mas alguma coisa precisa mudar a cada instante, senão você espera para sempre.</p>"),
        crianca("<p>“Enquanto tiver brinquedo no chão, guarde um.” Se você não guardar nenhum, a tarefa nunca acaba.</p>"),
        ver("quando usar <code>while</code> em vez de <code>for</code>"),
        nota("As três peças", [
            ("<code>n = 1</code>", "começo", "O valor antes do laço."),
            ("<code>while n &lt;= 5:</code>", "enquanto", "Repete enquanto for verdade."),
            ("<code>n += 1</code>", "passo", "Muda o valor para um dia a condição falhar."),
        ]),
        passos("Somando até o usuário digitar 0", [
            ("<code>n = int(input())</code>", "Lê o primeiro valor antes de testar."),
            ("<code>while n != 0:</code>", "O 0 é a bandeira de parada."),
            ("<code>total += n</code> e <code>n = int(input())</code>", "Soma e lê o próximo, dentro do laço."),
        ]),
        cod("Some até o zero", "Leia números até vir 0 e guarde a soma em <code>total</code>. As entradas simuladas são 5, 7, 3 e 0.",
            '''
total = 0
n = int(input("Número (0 para parar): "))

# repita enquanto n não for 0

print(total)
''',
            [("Soma 15", "assert total == 15, f'total = {total!r}'")],
            '''
total = 0
n = int(input("Número (0 para parar): "))

while n != 0:
    total += n
    n = int(input("Número (0 para parar): "))

print(total)
''', ["Some antes de ler o próximo.", "A leitura se repete dentro do laço."], entradas=["5", "7", "3", "0"]),
        erros([
            ("Esquecer de mudar a variável da condição.", "O laço nunca termina."),
            ("Somar o valor de parada.", "Teste antes de somar."),
            ("Usar <code>while</code> para percorrer uma lista inteira.", "Aí o <code>for</code> é mais simples e seguro."),
        ]),
        ponte("O laço de um agente",
              "<p>Um agente é um <code>while</code>: enquanto a tarefa não terminou <b>e</b> não passou do limite de passos, pense, use uma ferramenta, observe. Sem o limite, vira um laço infinito que custa dinheiro.</p>"),
        quiz([
            ("Não sei quantas voltas serão. Uso:", ["for", "while", "if"], 1, "Repete até a condição mudar."),
            ("O que causa laço infinito?", ["A condição nunca ficar falsa", "Usar print", "Começar em 0"], 0, "Algo no corpo precisa levar ao fim."),
            ("Se a condição já começa falsa, quantas voltas?", ["Uma", "Nenhuma", "Infinitas"], 1, "O teste vem antes da primeira volta."),
        ]),
    ],
    ["<code>while</code> é para número desconhecido de voltas.", "Início, condição e passo.", "Todo laço precisa de um jeito de terminar."],
    "break e f-strings: sair do meio do laço e escrever bonito.",
    livro=("ATBS:2", "Capítulo 2, “while Loop Statements”", "O que diferencia um while de um if?"))

# ---------------------------------------------------------------------------------------------
AULAS["Interromper laços (break) e f-strings"] = aula(
    30,
    "Às vezes o momento de parar só aparece <b>no meio</b> da volta. O <code>break</code> sai na hora. E a f-string deixa o resultado legível.",
    ["usar <code>while True</code> com <code>break</code>;", "evitar contar o valor de parada;", "formatar saídas com f-strings."],
    ["Laço <code>while</code>."],
    [
        chute("O que o código imprime?", ["1 2", "1 2 3", "1 2 4"], 0,
              ["Isso! No 3 o laço acaba antes do print.", "O break vem antes do print.", "Pular só o 3 seria <code>continue</code>."],
              "<code>break</code> encerra o laço inteiro.",
              cod='for n in [1, 2, 3, 4]:\n    if n == 3:\n        break\n    print(n, end=" ")'),
        concreto("A saída de emergência",
                 "<p>A condição do <code>while</code> é a porta no começo do corredor. O <code>break</code> é a <b>saída de emergência</b> no meio dele: passou por ela, o que está depois não acontece.</p>"),
        crianca("<p>Você está contando carrinhos e a mãe chama para jantar: para na hora, nem termina o que ia contar.</p>"),
        ver("como o <code>break</code> evita somar o valor de parada"),
        nota("As ferramentas", [
            ("<code>while True:</code>", "repita sempre", "Precisa de um <code>break</code> dentro."),
            ("<code>break</code>", "pare", "Sai do laço mais interno."),
            ("<code>continue</code>", "pule", "Vai direto para a próxima volta."),
            ("<code>f\"{x:.1f}\"</code>", "f-string", "Encaixa x com uma casa decimal."),
        ]),
        passos("Média até digitar 999", [
            ("<code>while True:</code>", "Não precisa ler antes do laço."),
            ("<code>n = int(input())</code>", "Uma leitura só."),
            ("<code>if n == 999: break</code>", "Sai antes de o 999 entrar na conta."),
            ("<code>soma += n</code>", "Só valores válidos chegam aqui."),
        ]),
        cod("Pare e informe", "Com <code>while True</code> e <code>break</code>, some as entradas até vir 999 e imprima exatamente <b>Soma: 30</b>. As entradas simuladas são 10, 20 e 999.",
            '''
soma = 0

# seu laço aqui

print("Soma")
''',
            [("Soma sem o 999", "assert soma == 30, f'soma = {soma!r}'"),
             ("Mensagem", "assert saida.strip().splitlines()[-1] == 'Soma: 30', f'saiu {saida.strip()!r}'")],
            '''
soma = 0

while True:
    n = int(input())
    if n == 999:
        break
    soma += n

print(f"Soma: {soma}")
''', ["O <code>if</code> vem antes da soma.", "<code>f\"Soma: {soma}\"</code>."], entradas=["10", "20", "999"]),
        erros([
            ("<code>while True</code> sem <code>break</code> alcançável.", "Laço infinito."),
            ("Colocar o <code>break</code> depois da soma.", "O valor de parada entra na conta."),
            ("Esquecer o <code>f</code> da f-string.", "As chaves saem como texto."),
        ]),
        ponte("Early stopping",
              "<p>No treino de uma rede, quando o erro de validação para de cair, um <code>break</code> encerra as épocas. No streaming de um LLM, ele para ao chegar o sinal de fim.</p>"),
        quiz([
            ("O que o <code>break</code> faz?", ["Pula uma volta", "Sai do laço", "Fecha o Python"], 1, "O programa continua depois do laço."),
            ("Em laços aninhados, o break sai de qual?", ["Do mais interno", "De todos", "Do mais externo"], 0, "Só do laço onde ele está."),
            ("<code>f\"{2.456:.1f}\"</code> vira:", ["2.4", "2.5", "2.456"], 1, "Arredonda para uma casa."),
        ]),
    ],
    ["<code>while True</code> pede um <code>break</code>.", "Teste a parada antes de usar o valor.", "f-strings encaixam e formatam valores."],
    "Tuplas: guardar vários valores que não mudam.",
    livro=("ATBS:2", "Capítulo 2, “break Statements”", "Quando break deixa o código mais claro?"))

# ---------------------------------------------------------------------------------------------
AULAS["Listas compostas (listas dentro de listas)"] = aula(
    30,
    "Uma planilha, uma imagem em cinza, um lote de embeddings: tudo é lista dentro de lista. Entendeu isto, entendeu o formato dos dados em IA.",
    ["acessar linha e coluna;", "percorrer com laços aninhados;", "evitar a armadilha da cópia."],
    ["Listas e fatiamento."],
    [
        chute("O que o código imprime?", ["2", "3", "4"], 1,
              ["Seria a linha 0, coluna 1.", "Isso! Linha 1 é [3, 4]; coluna 0 dela é 3.", "Esse é m[1][1]."],
              "Primeiro colchete escolhe a linha, o segundo a coluna.",
              cod="m = [[1, 2], [3, 4]]\nprint(m[1][0])"),
        concreto("O prédio",
                 "<p><code>m[2][5]</code> é andar 2, apartamento 5. Primeiro o elevador (linha), depois o corredor (coluna). Os dois começam em zero.</p>"),
        crianca("<p>Uma gaveta com caixinhas dentro: primeiro abre a gaveta, depois escolhe a caixinha.</p>"),
        ver("por que ele usa <code>[:]</code> ao guardar uma lista dentro de outra"),
        nota("Linha e coluna", [
            ("<code>m[i]</code>", "linha i", "Uma lista inteira."),
            ("<code>m[i][j]</code>", "linha i, coluna j", "Um valor."),
            ("<code>len(m)</code>", "linhas", "Quantas listas de dentro."),
            ("<code>linha[:]</code>", "cópia", "Uma lista nova com os mesmos valores."),
        ]),
        passos("Somando cada linha", [
            ("<code>for linha in m:</code>", "Pega uma linha por vez."),
            ("<code>total = 0</code>", "Zera a cada linha."),
            ("<code>for v in linha: total += v</code>", "Percorre os valores dela."),
        ]),
        cod("Média de cada modelo", "Cada linha tem as notas de um modelo. Monte <code>medias</code> com a média de cada linha, na ordem.",
            '''
notas = [[8, 6], [10, 9], [5, 7]]
medias = []

# percorra as linhas

print(medias)
''',
            [("Três médias", "assert medias == [7.0, 9.5, 6.0], f'medias = {medias!r}'")],
            '''
notas = [[8, 6], [10, 9], [5, 7]]
medias = []

for linha in notas:
    medias.append(sum(linha) / len(linha))

print(medias)
''', ["<code>sum(linha) / len(linha)</code> é a média de uma linha."]),
        erros([
            ("<code>grupo.append(pessoa)</code> e depois <code>pessoa.clear()</code>.", "Apaga dentro do grupo também. Guarde <code>pessoa[:]</code>."),
            ("<code>[[0] * 3] * 2</code>", "Repete a mesma linha duas vezes: mudar uma muda a outra."),
            ("Trocar linha por coluna.", "É sempre <code>[linha][coluna]</code>."),
        ]),
        ponte("Isto é uma matriz",
              "<p>Um lote de 32 embeddings de 768 números é uma lista de 32 listas de 768. O NumPy chama isso de <code>shape (32, 768)</code>.</p>"),
        quiz([
            ("Em <code>[[1, 2, 3], [4, 5, 6]]</code>, quantas linhas?", ["2", "3", "6"], 0, "Duas listas de dentro."),
            ("Nessa lista, onde está o 6?", ["<code>[2][3]</code>", "<code>[1][2]</code>", "<code>[2][1]</code>"], 1, "Linha 1, coluna 2, contando do zero."),
            ("Para guardar uma cópia de uma lista:", ["<code>b = a</code>", "<code>b = a[:]</code>", "<code>b == a</code>"], 1, "<code>b = a</code> só cria outro nome para a mesma lista."),
        ]),
    ],
    ["<code>m[linha][coluna]</code>.", "Dois laços percorrem tudo.", "Copie com <code>[:]</code> antes de reaproveitar."],
    "Dicionários: procurar pelo nome em vez da posição.",
    livro=("ATBS:4", "Capítulo 4, “Lists”, parte sobre referências", "Por que b = a não copia a lista?"))

# ---------------------------------------------------------------------------------------------
AULAS["Funções: escopo, opcionais e docstrings"] = aula(
    35,
    "Saber criar uma função é metade. A outra metade é criar uma que <b>outra pessoa</b> consiga usar: com padrões, documentação e sem mexer escondido no resto do programa.",
    ["entender escopo local e global;", "criar parâmetros opcionais;", "documentar com docstring e consultar com <code>help</code>."],
    ["Funções, parâmetros e retorno."],
    [
        chute("O que o código imprime?", ["1", "5", "Dá erro"], 0,
              ["Isso! O x de dentro é outro: nasce e morre na função.", "A atribuição dentro da função criou uma variável local.", "É válido ter o mesmo nome nos dois escopos."],
              "O que é criado dentro da função fica dentro dela.",
              cod="x = 1\ndef mudar():\n    x = 5\nmudar()\nprint(x)"),
        concreto("A cozinha do restaurante",
                 "<p>O cliente não vê as panelas (variáveis locais), só recebe o prato (<code>return</code>). O cardápio é a <b>docstring</b>. “Se não falar nada, vem ao ponto” é o <b>parâmetro opcional</b>.</p>"),
        crianca("<p>O que se inventa dentro da cabana fica na cabana. Para alguém de fora ter, você precisa entregar pela porta.</p>"),
        ver("escopo de variáveis e parâmetros opcionais"),
        nota("Função bem feita", [
            ("<code>def f(a, b=0):</code>", "b opcional", "Se não vier, vale 0."),
            ("<code>\"\"\"texto\"\"\"</code>", "docstring", "Primeira linha do corpo; explica o uso."),
            ("<code>help(f)</code>", "ajuda", "Mostra a docstring."),
            ("<code>global x</code>", "use a de fora", "Existe, mas evite: prefira <code>return</code>."),
        ]),
        passos("Chamando <code>somar(4)</code> em <code>def somar(a, b=10)</code>", [
            ("<code>a</code> recebe 4", "Foi passado."),
            ("<code>b</code> recebe 10", "Não foi passado: vale o padrão."),
            ("<code>return a + b</code>", "Entrega 14; a e b deixam de existir."),
        ]),
        cod("Limiar com padrão", "Complete <code>aprovar(prob, limiar=0.5)</code>: devolve <code>True</code> quando <code>prob</code> é maior ou igual ao limiar. Escreva também uma docstring.",
            '''
def aprovar(prob, limiar=0.5):
    return False

print(aprovar(0.7))
''',
            [("Usa o padrão", "assert aprovar(0.5) is True and aprovar(0.4) is False, 'confira o limiar padrão'"),
             ("Aceita outro limiar", "assert aprovar(0.7, 0.8) is False and aprovar(0.9, limiar=0.8) is True, 'use o parâmetro limiar'"),
             ("Tem docstring", "assert aprovar.__doc__, 'falta a docstring'")],
            '''
def aprovar(prob, limiar=0.5):
    """Diz se a probabilidade alcança o limiar."""
    return prob >= limiar

print(aprovar(0.7))
''', ["A comparação já devolve True ou False.", "A docstring é a primeira linha do corpo, entre três aspas."]),
        erros([
            ("<code>def f(itens=[])</code>", "A mesma lista é reaproveitada entre chamadas. Use <code>None</code> como padrão."),
            ("Usar <code>global</code> para devolver resultado.", "Use <code>return</code>."),
            ("Opcional antes de obrigatório.", "Os opcionais vêm no fim."),
        ]),
        ponte("Ferramentas de agentes",
              "<p>Quando você dá uma função como ferramenta a um LLM, ele decide usá-la lendo <b>o nome, os parâmetros e a docstring</b>. Docstring ruim vira agente burro.</p>"),
        quiz([
            ("Variável criada dentro da função é:", ["Global", "Local", "Constante"], 1, "Só existe durante a chamada."),
            ("Onde ficam os parâmetros opcionais?", ["No fim", "No começo", "Depois do return"], 0, "Depois dos obrigatórios."),
            ("O que <code>help(f)</code> mostra?", ["O tempo da função", "A documentação", "O último resultado"], 1, "Lê a assinatura e a docstring."),
        ]),
    ],
    ["Escopo local protege o resto do programa.", "Valor padrão torna o parâmetro opcional.", "Docstring é o manual da função."],
    "Módulos e pacotes: dividir o programa em arquivos.",
    livro=("ATBS:3", "Capítulo 3, “Local and Global Scope”", "Por que preferir return a global?"))
