# -*- coding: utf-8 -*-
"""
Piloto das Aulas Visuais da trilha de IA (3 aulas de níveis diferentes):
  - Fase 1 · "Laços (for, while)"
  - Fase 3 · "Regressão logística"
  - Fase 5 · "Mecanismo de atenção"

O formato é o mesmo do piloto de Matemática (lesson_v2_assets.py), com os blocos novos de
lesson_blocks_v3.py: código Python que roda no navegador com testes ("codigo"), montar o código
("parsons"), "preveja a saída" (palpite com "codigo") e os laboratórios "logistica" e "atencao".

Os trechos de vídeo foram escolhidos lendo as legendas de cada vídeo; as missões perguntam
exatamente o que aparece no trecho.
"""

# ---------------------------------------------------------------------------
# Fase 1 · Laços (for, while)
# ---------------------------------------------------------------------------
PILOT_LACOS = {
    "v": 2,
    "duracao": 45,
    "gancho": r"""Imprimir os números de 1 a 1.000 escrevendo 1.000 linhas de <code>print</code>? Programador tem preguiça, no bom sentido: escreve a instrução <b>uma vez</b> e manda o computador <b>repetir</b>. É assim que um modelo de IA treina por milhares de rodadas com meia dúzia de linhas.""",
    "objetivos": [
        "escrever um laço <code>for</code> com <code>range(início, fim, passo)</code> e prever quantas vezes ele roda;",
        "usar <code>while</code> quando você não sabe de antemão quantas repetições serão;",
        "reconhecer e consertar um laço infinito;",
        "ler o laço de treino de um modelo de IA sem se assustar.",
    ],
    "prerequisitos": ["Variáveis, <code>print</code> e condicionais <code>if</code> (aulas anteriores da Fase 1)."],
    "blocos": [
        {
            "tipo": "palpite",
            "rotulo": "Preveja a saída",
            "codigo": "for i in range(1, 4):\n    print(i * 2)",
            "pergunta": "O que esse código imprime?",
            "opcoes": ["2, 4 e 6 (um por linha)", "2, 4, 6 e 8", "0, 2 e 4"],
            "correta": 0,
            "porques": [
                "Isso! <code>range(1, 4)</code> gera 1, 2 e 3: o fim (4) <b>não entra</b>. Cada um vezes 2 dá 2, 4 e 6.",
                "Quase: o 4 não entra. <code>range(1, 4)</code> para <b>antes</b> do 4, então só há 3 voltas.",
                "O <code>range</code> começa no primeiro número que você passou (1), não no zero. O zero só aparece quando você escreve <code>range(4)</code> ou <code>range(0, 4)</code>.",
            ],
            "explicacao": "Guarde esta regra, ela vale para quase tudo em Python: <b>o começo entra, o fim não</b>.",
        },
        {
            "tipo": "concreto",
            "titulo": "A lista de chamada",
            "corpo": r"""<p>A professora não escreve uma instrução para cada aluno. Ela segue uma regra só: <b>“para cada nome da lista, chame o nome e marque presença”</b>.</p>
<p>Isso é um <code>for</code>: ele percorre uma coleção do começo ao fim e repete o mesmo bloco para cada item.</p>
<pre class="lv2-code"><code>chamada = ["Ana", "Bia", "Caio"]
for aluno in chamada:
    print("Presente,", aluno)</code></pre>""",
        },
        {
            "tipo": "crianca",
            "corpo": r"""<p>“Faça <b>10 polichinelos</b>” é um <code>for</code>: você sabe quantas vezes vai repetir antes de começar.</p>
<p>“<b>Pule corda até errar</b>” é um <code>while</code>: você repete <b>enquanto</b> uma condição for verdadeira, sem saber quando ela vai deixar de ser.</p>
<p>E se a condição nunca ficar falsa? Você pula para sempre. Em programação isso se chama <b>laço infinito</b>, e é o erro mais comum de quem está começando.</p>""",
        },
        {
            "tipo": "video",
            "rotulo": "A ideia, com o Guanabara",
            "id": "cL4YDtFnCt4",
            "inicio": 270,
            "fim": 540,
            "canal": "Curso em Vídeo",
            "titulo_video": "Curso Python #013 · Estrutura de repetição for",
            "corpo": r"""<p>Só a parte da teoria (4:30 a 9:00): o personagem que precisa andar até a maçã.</p>""",
            "missao": [
                "Por que dar o comando <i>passo</i> 500 vezes seguidas é uma péssima solução?",
                "O que ele coloca “do lado da bolinha” para o personagem não cair da plataforma?",
                "Como o <i>pega</i> mostra se está dentro ou fora do laço?",
            ],
            "respostas": r"""<p><b>1.</b> O código fica gigante e repetido. Com um laço, mudar de 3 para 2.000 repetições é trocar um número só.</p>
<p><b>2.</b> Um <b>limite</b>: um contador (a variável de controle <code>c</code>) que conta as casinhas e faz o laço parar quando chega ao fim do intervalo.</p>
<p><b>3.</b> Pela <b>indentação</b> (o recuo): o <i>passo</i>, mais para dentro, repete; o <i>pega</i>, encostado à esquerda, roda uma vez só, depois do laço.</p>""",
        },
        {
            "tipo": "notacao",
            "rotulo": "Agora sim, a sintaxe",
            "titulo": "As duas formas de repetir",
            "itens": [
                {"simbolo": "<code>for c in range(a, b, p):</code>", "leitura": "para c no intervalo de a até b, de p em p",
                 "significado": "Começa em <code>a</code>, para <b>antes</b> de <code>b</code> e anda de <code>p</code> em <code>p</code>. Sem <code>p</code>, o passo é 1; sem <code>a</code>, começa no 0."},
                {"simbolo": "<code>for item in lista:</code>", "leitura": "para cada item da lista",
                 "significado": "Percorre qualquer coleção: lista, texto (letra por letra), linhas de um arquivo, lotes de dados."},
                {"simbolo": "<code>while condição:</code>", "leitura": "enquanto a condição for verdadeira",
                 "significado": "Testa a condição antes de cada volta. Algo <b>dentro</b> do laço precisa mudar para ela um dia ficar falsa."},
                {"simbolo": "<code>break</code> / <code>continue</code>", "leitura": "quebre / continue",
                 "significado": "<code>break</code> sai do laço na hora. <code>continue</code> pula o resto desta volta e vai para a próxima."},
            ],
        },
        {
            "tipo": "passos",
            "rotulo": "Resolvido passo a passo",
            "titulo": "Somando uma lista, volta por volta",
            "corpo": r"""<pre class="lv2-code"><code>soma = 0
for n in [4, 2, 3, 1]:
    soma = soma + n
print(soma)</code></pre>""",
            "passos": [
                {"faca": "Antes do laço: <code>soma = 0</code>.", "porque": "Quem acumula precisa começar do zero, senão soma lixo."},
                {"faca": "Volta 1: <code>n = 4</code>, <code>soma = 0 + 4 = 4</code>.", "porque": "O <code>for</code> entrega o primeiro item da lista."},
                {"faca": "Volta 2: <code>n = 2</code>, <code>soma = 4 + 2 = 6</code>.", "porque": "A variável <code>soma</code> lembra o valor da volta anterior."},
                {"faca": "Voltas 3 e 4: <code>soma = 6 + 3 = 9</code> e depois <code>9 + 1 = 10</code>.", "porque": "Acabaram os itens, o laço termina sozinho."},
                {"faca": "<code>print(soma)</code> mostra <b>10</b>, uma vez só.", "porque": "O <code>print</code> está fora do laço (sem recuo)."},
            ],
            "conclusao": "Esse padrão “acumulador começa em zero e cresce a cada volta” é o mesmo que calcula a perda média de um modelo sobre milhares de exemplos.",
        },
        {
            "tipo": "video",
            "rotulo": "Na prática, com o Guanabara",
            "id": "cL4YDtFnCt4",
            "inicio": 1049,
            "fim": 1277,
            "canal": "Curso em Vídeo",
            "titulo_video": "Curso Python #013 · Estrutura de repetição for",
            "corpo": r"""<p>Agora no PyCharm (17:29 a 21:17): ele testa o <code>range</code> de vários jeitos.</p>""",
            "missao": [
                "Com <code>range(1, 6)</code>, quantas vezes apareceu “oi”? Por quê?",
                "O que aconteceu quando ele recuou o <code>print('fim')</code> para dentro do laço?",
                "Como ele fez a contagem andar para trás? E de 2 em 2?",
            ],
            "respostas": r"""<p><b>1.</b> Cinco vezes: o último número do <code>range</code> é ignorado. Para contar de 1 a 6 ele usou <code>range(1, 7)</code>.</p>
<p><b>2.</b> “fim” passou a ser impresso a cada volta, porque virou parte do laço. Indentação muda o comportamento do programa.</p>
<p><b>3.</b> Com um terceiro valor negativo no <code>range</code>, o passo <code>-1</code>. Para andar de 2 em 2, passo <code>2</code>: <code>range(0, 7, 2)</code> dá 0, 2, 4 e 6.</p>""",
        },
        {
            "tipo": "parsons",
            "titulo": "Contagem regressiva com while",
            "corpo": r"""<p>Coloque as linhas na ordem certa para imprimir 10, 9, ..., 0 e depois “Fogo!”. O recuo de cada linha já está certo; só a ordem está embaralhada.</p>""",
            "linhas": ["n = 10", "while n >= 0:", "    print(n)", "    n = n - 1", 'print("Fogo!")'],
            "explicacao": r"""<p>Primeiro a variável nasce (<code>n = 10</code>), depois vem o teste do <code>while</code>. Dentro do laço, imprimimos e <b>diminuímos</b> <code>n</code>: sem essa linha, <code>n</code> seria 10 para sempre e o laço nunca acabaria. O “Fogo!” fica fora, sem recuo, para sair uma vez só.</p>""",
        },
        {
            "tipo": "codigo",
            "rotulo": "Mão no código · nível 1",
            "titulo": "Os pares de 2 a 20",
            "enunciado": "Ajuste o <code>range</code> para imprimir 2, 4, 6, ..., 20, um número por linha. Depois clique em <b>Verificar</b>.",
            "inicial": "# Ajuste os três números do range\nfor n in range(1, 2):\n    print(n)\n",
            "testes": [
                {"nome": "Imprime 10 números", "codigo": "assert len(saida.split()) == 10, f'saíram {len(saida.split())} números'"},
                {"nome": "São os pares de 2 a 20, em ordem", "codigo": "assert saida.split() == [str(x) for x in range(2, 21, 2)], 'confira o início, o fim (que não entra) e o passo'"},
            ],
            "dicas": ["Começo 2, passo 2. E o fim? Lembre que ele não entra."],
            "solucao": "for n in range(2, 21, 2):\n    print(n)",
            "explicacao": "<p>Também valeria <code>range(2, 22, 2)</code>: qualquer fim maior que 20 e até 22 funciona.</p>",
        },
        {
            "tipo": "codigo",
            "rotulo": "Mão no código · nível 2",
            "titulo": "Conserte o laço infinito",
            "enunciado": "Este código deveria somar 1 + 2 + ... + 10 e imprimir <b>55</b>. Clique em <b>Rodar</b> para ver o que acontece e depois conserte.",
            "inicial": "total = 0\ni = 1\nwhile i <= 10:\n    total = total + i\nprint(total)\n",
            "testes": [
                {"nome": "Termina e imprime 55", "codigo": "assert saida.strip() == '55', f'saiu {saida.strip()!r}'"},
            ],
            "dicas": ["Qual variável aparece na condição do <code>while</code>? Ela muda dentro do laço?"],
            "solucao": "total = 0\ni = 1\nwhile i <= 10:\n    total = total + i\n    i = i + 1\nprint(total)",
            "explicacao": "<p>Faltava <code>i = i + 1</code> dentro do laço. Sem isso, <code>i</code> fica 1 para sempre, a condição nunca fica falsa e o programa trava. O site interrompe depois de 8 segundos; no seu computador, seria <code>Ctrl + C</code>.</p>",
        },
        {
            "tipo": "codigo",
            "rotulo": "Mão no código · nível 3 · ponte para IA",
            "titulo": "Quando parar de treinar?",
            "enunciado": "A lista tem a perda de um modelo a cada época de treino. Imprima o número da <b>primeira</b> época (contando a partir de 1) em que a perda ficou <b>abaixo de 0,1</b> e pare o laço ali com <code>break</code>.",
            "inicial": "perdas = [2.31, 1.40, 0.92, 0.61, 0.43, 0.29, 0.18, 0.11, 0.07, 0.05]\n\n# seu código aqui\n",
            "testes": [
                {"nome": "Imprime só um número", "codigo": "assert len(saida.split()) == 1, f'saíram {len(saida.split())} valores; use break para parar no primeiro'"},
                {"nome": "É a época 9", "codigo": "assert saida.strip() == '9', f'saiu {saida.strip()!r}; conte as épocas a partir de 1'"},
            ],
            "dicas": [
                "<code>for epoca, perda in enumerate(perdas, start=1):</code> entrega o número da época e a perda juntos.",
                "Dentro do laço: <code>if perda &lt; 0.1:</code>, imprima a época e use <code>break</code>.",
            ],
            "solucao": "perdas = [2.31, 1.40, 0.92, 0.61, 0.43, 0.29, 0.18, 0.11, 0.07, 0.05]\n\nfor epoca, perda in enumerate(perdas, start=1):\n    if perda < 0.1:\n        print(epoca)\n        break",
            "explicacao": "<p>Essa é a ideia do <b>early stopping</b> que você verá na Fase 4: parar o treino quando ele já está bom o suficiente.</p>",
        },
        {
            "tipo": "armadilhas",
            "itens": [
                {"erro": "“<code>range(1, 10)</code> vai de 1 até 10.”", "correcao": "Vai de 1 até <b>9</b>. O fim nunca entra. Para incluir o 10, use <code>range(1, 11)</code>."},
                {"erro": "Esquecer de mudar a variável do <code>while</code>.", "correcao": "Se nada dentro do laço altera a condição, ela nunca fica falsa: laço infinito."},
                {"erro": "Esquecer os dois-pontos ou o recuo.", "correcao": "<code>for ... :</code> e <code>while ... :</code> terminam com <code>:</code>, e o bloco repetido fica recuado 4 espaços."},
                {"erro": "Apagar itens da lista enquanto anda por ela com <code>for</code>.", "correcao": "O laço pula itens. Crie uma lista nova (ou percorra uma cópia, <code>lista[:]</code>)."},
            ],
        },
        {
            "tipo": "ponte",
            "titulo": "O laço que treina uma rede neural",
            "corpo": r"""<p>Na Fase 4 você vai escrever isto, e agora já consegue ler cada linha:</p>
<pre class="lv2-code"><code>for epoca in range(10):          # repete o treino 10 vezes
    for lote in dados:           # percorre os dados em pedaços
        perda = modelo.treinar(lote)
    print(epoca, perda)</code></pre>
<p>Um <code>for</code> dentro de outro (laços <b>aninhados</b>): para cada época, o modelo passa por todos os lotes de dados. É só isso, repetido milhões de vezes numa GPU.</p>""",
        },
        {
            "tipo": "quiz",
            "corpo": r"""<p>3 perguntas. Acertando 2, a camada “Vá mais fundo” é liberada e as revisões são agendadas.</p>""",
            "perguntas": [
                {"pergunta": "Quantas vezes roda <code>for i in range(0, 10, 3)</code>?", "opcoes": ["3 vezes", "4 vezes (0, 3, 6 e 9)", "10 vezes"], "correta": 1,
                 "explicacao": "Começa em 0 e anda de 3 em 3 enquanto for menor que 10: 0, 3, 6, 9."},
                {"pergunta": "Quando o <code>while</code> é a melhor escolha?", "opcoes": ["Quando você sabe exatamente quantas repetições serão.", "Quando a repetição depende de uma condição, como “até o usuário digitar sair”.", "Nunca: <code>for</code> sempre é melhor."], "correta": 1,
                 "explicacao": "Número conhecido de voltas: <code>for</code>. Repetir até algo acontecer: <code>while</code>."},
                {"pergunta": "<code>x = 5</code> e depois <code>while x &gt; 0: print(x)</code>. O que acontece?", "opcoes": ["Imprime 5, 4, 3, 2, 1.", "Imprime 5 para sempre: x nunca muda.", "Dá erro de sintaxe."], "correta": 1,
                 "explicacao": "Nada dentro do laço diminui <code>x</code>, então a condição continua verdadeira para sempre."},
            ],
        },
        {
            "tipo": "camadas",
            "ponte": [
                {"nome": "Curso em Vídeo, Curso Python #014 (while)", "url": "https://www.youtube.com/watch?v=LH6OIn2lBaI",
                 "trecho": "vídeo completo, em português", "tempo": 38, "foco": "A continuação natural desta aula: o mesmo personagem, agora sem saber quantos passos dar."},
            ],
            "profundidade": [
                {"obra": "Al Sweigart, <i>Automate the Boring Stuff with Python</i> (grátis online)", "url": "https://automatetheboringstuff.com/2e/chapter2/",
                 "secao": "Capítulo 2, “Flow Control”: as partes sobre while, break, continue e for com range()",
                 "perguntas": ["Que exemplo o livro usa para mostrar um while que só termina quando o usuário digita a resposta certa?",
                               "Qual é a diferença entre break e continue segundo o livro?"]},
            ],
            "revisao": [
                {"nome": "Documentação oficial do Python, “Mais ferramentas de controle de fluxo”", "url": "https://docs.python.org/pt-br/3/tutorial/controlflow.html",
                 "trecho": "seções 4.2 a 4.4 (for, range, break e continue)", "tempo": 15, "foco": "A mesma matéria em texto, em português, com exemplos curtos."},
            ],
        },
    ],
    "resumo": [
        "<code>for</code> repete um número conhecido de vezes ou percorre uma coleção; <code>while</code> repete enquanto uma condição for verdadeira.",
        "Em <code>range(a, b, p)</code>, o começo entra e o fim não.",
        "Todo <code>while</code> precisa de algo, dentro dele, que um dia torne a condição falsa.",
        "O treino de um modelo de IA é um laço (épocas) dentro de outro (lotes de dados).",
    ],
    "proxima": "Funções: empacotar um laço útil num comando com nome, para reaproveitar.",
    "referencias": [
        {"obra": "Curso em Vídeo, Curso Python #013 e #014", "uso": "Explicação e prática dos laços em português."},
        {"obra": "Al Sweigart, Automate the Boring Stuff with Python, cap. 2", "uso": "Exemplos de while, break e continue."},
    ],
}

# ---------------------------------------------------------------------------
# Fase 3 · Regressão logística
# ---------------------------------------------------------------------------
PILOT_LOGISTICA = {
    "v": 2,
    "duracao": 50,
    "gancho": r"""Seu e-mail não pergunta “<i>quão</i> spam é esta mensagem?”. Ele pergunta “<b>qual a chance</b> de ser spam?” e decide a partir disso. Prever uma <b>probabilidade</b> entre 0 e 100% e transformar isso numa decisão de sim ou não é exatamente o que a regressão logística faz, e é também o que um único neurônio artificial faz.""",
    "objetivos": [
        "explicar por que uma reta não serve para prever sim ou não;",
        "calcular a probabilidade de um modelo logístico com a função sigmoide;",
        "escolher e entender o limiar de decisão;",
        "programar a sigmoide e uma previsão do zero.",
    ],
    "prerequisitos": [
        "Regressão linear (aula anterior desta fase).",
        "Gradiente descendente (aula “Gradiente descendente” da trilha de Matemática).",
    ],
    "blocos": [
        {
            "tipo": "palpite",
            "rotulo": "Chute antes de ver",
            "pergunta": "Você ajustou uma <b>reta</b> para prever se um aluno passa (1) ou não (0) pelas horas de estudo. Para quem estuda 15 horas, a reta prevê <b>1,6</b>. O que isso significa?",
            "opcoes": ["160% de chance de passar.", "Nada útil: probabilidade não passa de 100%, a reta não foi feita para isso.", "Que ele deveria estudar menos."],
            "correta": 1,
            "porques": [
                "Não existe 160% de chance. Esse número estranho é o sintoma do problema que a regressão logística resolve.",
                "Isso! A reta cresce sem limite. Para sim ou não precisamos de uma curva presa entre 0 e 1.",
                "O número não diz nada sobre estudar menos: ele só mostra que a reta extrapola para fora do intervalo que faz sentido.",
            ],
            "explicacao": "A saída precisa ser uma probabilidade, e probabilidade mora entre 0 e 1.",
        },
        {
            "tipo": "concreto",
            "titulo": "Horas de estudo e aprovação",
            "corpo": r"""<p>Anotamos 16 alunos: quantas horas cada um estudou e se passou na prova (1) ou não (0). Quem estudou pouco quase sempre reprovou; quem estudou muito quase sempre passou; no meio, há de tudo.</p>
<p>Não queremos uma resposta seca para quem estudou 4 horas. Queremos algo como “<b>50% de chance</b>”. E para 8 horas, “<b>quase certo</b>”.</p>""",
        },
        {
            "tipo": "crianca",
            "corpo": r"""<p>Pense num <b>termômetro de certeza</b> que vai de 0 (“com certeza não”) a 1 (“com certeza sim”).</p>
<p>Por mais que você estude, o termômetro nunca passa do 1. Por menos que estude, nunca fica abaixo de 0. No meio ele sobe rápido, e nas pontas vai ficando quase parado. O desenho desse termômetro é uma <b>curva em S</b>.</p>""",
        },
        {
            "tipo": "video",
            "rotulo": "Intuição visual (StatQuest)",
            "id": "yIYKR4sgzI8",
            "inicio": 189,
            "fim": 527,
            "canal": "StatQuest with Josh Starmer",
            "titulo_video": "StatQuest: Logistic Regression",
            "corpo": r"""<p>Em inglês, com legendas em português (⚙️ → Legendas → Português). Do resumo da regressão logística até o fim (3:09 a 8:47).</p>""",
            "missao": [
                "No exemplo dele, o que o eixo vertical da curva em S representa?",
                "Como a probabilidade vira uma classificação de sim ou não?",
                "Por que a regressão logística não é ajustada com mínimos quadrados, como a linear?",
            ],
            "respostas": r"""<p><b>1.</b> A <b>probabilidade</b> de o camundongo ser obeso, dado o peso dele. Vai de 0 a 1.</p>
<p><b>2.</b> Com um limiar: acima de 50% de probabilidade, classifica como obeso; abaixo, como não obeso.</p>
<p><b>3.</b> Porque não há resíduos como na reta. Ela é ajustada por <b>máxima verossimilhança</b>: escolhe a curva que torna os dados observados o mais prováveis possível.</p>""",
        },
        {
            "tipo": "notacao",
            "rotulo": "Agora sim, a fórmula",
            "titulo": "Da soma ponderada à probabilidade",
            "corpo": r"""$$\hat p = \sigma(w\,x + b) = \frac{1}{1 + e^{-(w x + b)}}$$""",
            "itens": [
                {"simbolo": r"$z = w\,x + b$", "leitura": "z igual a w vezes x mais b", "significado": "Uma reta comum (o “escore”). Pode dar qualquer número, de −∞ a +∞."},
                {"simbolo": r"$\sigma(z)$", "leitura": "sigma de z (a sigmoide)", "significado": "Espreme qualquer número para dentro de (0, 1). $\\sigma(0) = 0{,}5$; $z$ muito positivo dá quase 1; muito negativo, quase 0."},
                {"simbolo": r"$\hat p$", "leitura": "p chapéu", "significado": "A probabilidade estimada de ser da classe 1 (passar, ser spam, ser fraude)."},
                {"simbolo": r"$\hat y = [\hat p \ge t]$", "leitura": "y chapéu é 1 se p chapéu for pelo menos t", "significado": "A decisão final, com o limiar $t$ (normalmente 0,5)."},
            ],
        },
        {
            "tipo": "widget",
            "widget": "logistica",
            "titulo": "Ajuste a curva você mesmo",
            "corpo": r"""<p>Cada bolinha é um aluno: cheia passou, vazia não passou. Mexa em $w$ e $b$ e veja a curva verde mudar; a linha laranja é o limiar.</p>""",
            "missoes": [
                "Clique em <b>Deixar o gradiente ajustar</b>. Quantos acertos o melhor modelo consegue? Por que não dá para acertar os 16?",
                "Com o modelo ajustado, mude o limiar para 0,3. O que acontece com a fronteira e com quem é marcado como “passa”?",
                "Coloque $w$ negativo. O que a curva passa a dizer sobre estudar?",
                "Aumente muito $w$ (perto de 3). O que acontece com o formato do S?",
            ],
        },
        {
            "tipo": "passos",
            "rotulo": "Resolvido passo a passo",
            "titulo": "Quem estudou 5 horas passa?",
            "corpo": r"""<p>Modelo já treinado: $w = 1{,}5$ e $b = -6$. Limiar $t = 0{,}5$.</p>""",
            "passos": [
                {"faca": r"Escore: $z = 1{,}5 \times 5 - 6 = 1{,}5$.", "porque": "Primeiro a parte linear, igual à regressão linear."},
                {"faca": r"$e^{-1{,}5} \approx 0{,}223$.", "porque": "Calculadora ou <code>math.exp(-1.5)</code>."},
                {"faca": r"$\hat p = 1 / (1 + 0{,}223) \approx 0{,}818$.", "porque": "A sigmoide transforma o escore em probabilidade: 81,8%."},
                {"faca": r"$0{,}818 \ge 0{,}5$, então $\hat y = 1$: <b>passa</b>.", "porque": "O limiar transforma a probabilidade em decisão."},
            ],
            "conclusao": r"Note que com 4 horas o escore é $1{,}5 \times 4 - 6 = 0$ e a probabilidade é exatamente 0,5: as 4 horas são a <b>fronteira de decisão</b> deste modelo.",
        },
        {
            "tipo": "codigo",
            "rotulo": "Mão no código",
            "titulo": "Sua primeira regressão logística, do zero",
            "enunciado": "Complete <code>sigmoide</code> e <code>prever</code> e clique em <b>Verificar</b>.",
            "inicial": "import math\n\ndef sigmoide(z):\n    # devolva 1 / (1 + e elevado a -z)\n    return 0\n\ndef prever(horas, w=1.5, b=-6, limiar=0.5):\n    # devolva 1 se sigmoide(w*horas + b) for >= limiar, senão 0\n    return 0\n\nprint(sigmoide(0), prever(5), prever(3))\n",
            "testes": [
                {"nome": "sigmoide(0) dá 0,5", "codigo": "assert abs(sigmoide(0) - 0.5) < 1e-9, f'deu {sigmoide(0)}'"},
                {"nome": "sigmoide(2) ≈ 0,881", "codigo": "assert abs(sigmoide(2) - 0.8808) < 1e-3, f'deu {sigmoide(2)}'"},
                {"nome": "Fica entre 0 e 1 nas pontas", "codigo": "assert sigmoide(-30) < 1e-6 and sigmoide(30) > 1 - 1e-6, 'para z muito negativo deve dar quase 0; muito positivo, quase 1'"},
                {"nome": "5 horas passa, 3 horas não", "codigo": "assert prever(5) == 1 and prever(3) == 0, f'prever(5)={prever(5)}, prever(3)={prever(3)}'"},
                {"nome": "Respeita o limiar", "codigo": "assert prever(4, limiar=0.6) == 0 and prever(4, limiar=0.4) == 1, 'com 4 horas a probabilidade é 0,5: limiar 0,6 reprova, 0,4 aprova'"},
            ],
            "dicas": ["<code>math.exp(-z)</code> calcula $e^{-z}$.", "Em <code>prever</code>: calcule <code>p = sigmoide(w * horas + b)</code> e devolva <code>1 if p &gt;= limiar else 0</code>."],
            "solucao": "import math\n\ndef sigmoide(z):\n    return 1 / (1 + math.exp(-z))\n\ndef prever(horas, w=1.5, b=-6, limiar=0.5):\n    p = sigmoide(w * horas + b)\n    return 1 if p >= limiar else 0\n\nprint(sigmoide(0), prever(5), prever(3))",
        },
        {
            "tipo": "pratica",
            "titulo": "Treino em 3 níveis",
            "corpo": r"""<p>Responda com números; use vírgula ou ponto como preferir.</p>""",
            "exercicios": [
                {"nivel": 1, "enunciado": r"Com $w = 2$ e $b = -4$, qual a probabilidade para $x = 2$?", "valor": 0.5,
                 "dicas": [r"Calcule $z$ primeiro: $2 \times 2 - 4$."], "resposta": r"$z = 0$ e $\sigma(0) = 0{,}5$: exatamente na fronteira."},
                {"nivel": 2, "enunciado": r"Um modelo diz $\hat p = 0{,}8$. Qual a <b>chance</b> (odds) $\hat p / (1 - \hat p)$?", "valor": 4,
                 "dicas": [r"$0{,}8 / 0{,}2$."], "resposta": r"4: “4 para 1” a favor. A regressão logística é linear no <b>logaritmo</b> dessa chance: $\ln(\hat p/(1-\hat p)) = w x + b$."},
                {"nivel": 3, "enunciado": r"Com $w = 1{,}5$, $b = -6$ e limiar 0,5, a partir de quantas horas o modelo aprova?", "valor": 4,
                 "dicas": [r"Limiar 0,5 acontece quando $z = 0$.", r"Resolva $1{,}5x - 6 = 0$."], "resposta": r"$x = 4$ horas. Mudar o limiar move essa fronteira; mudar $w$ muda a rapidez com que a probabilidade sobe ao redor dela."},
            ],
        },
        {
            "tipo": "laboratorio",
            "titulo": "A mesma coisa com scikit-learn",
            "corpo": r"""<p>No dia a dia, ninguém escreve a sigmoide na mão. Rode no Google Colab (o scikit-learn é pesado demais para o navegador):</p>""",
            "codigo": "from sklearn.linear_model import LogisticRegression\n\nhoras = [[0.5],[1],[1.5],[2],[2.5],[3],[3.5],[4],[4.5],[5],[5.5],[6],[6.5],[7],[8],[9]]\npassou = [0,0,0,0,1,0,0,1,0,1,1,0,1,1,1,1]\n\nmodelo = LogisticRegression().fit(horas, passou)\nprint('w =', modelo.coef_[0][0], ' b =', modelo.intercept_[0])\nprint('chance com 5h:', modelo.predict_proba([[5]])[0][1])",
            "experimentos": [
                "Compare o $w$ e o $b$ com os do laboratório acima depois de “Deixar o gradiente ajustar”. São parecidos? (O scikit-learn usa regularização por padrão, então não serão idênticos.)",
                "Troque <code>predict_proba</code> por <code>predict</code>. O que muda na saída?",
            ],
        },
        {
            "tipo": "armadilhas",
            "itens": [
                {"erro": "“Regressão logística prevê números, porque é regressão.”", "correcao": "Apesar do nome, ela é um <b>classificador</b>: prevê a probabilidade de uma classe."},
                {"erro": "“O limiar é sempre 0,5.”", "correcao": "É só o padrão. Num exame de câncer, você baixa o limiar para não deixar passar doentes, aceitando mais alarmes falsos."},
                {"erro": "“90% de probabilidade significa que o modelo tem certeza.”", "correcao": "Significa que, entre casos parecidos, cerca de 1 em cada 10 será da outra classe, se o modelo estiver bem calibrado."},
                {"erro": "Comparar os pesos $w$ de variáveis em escalas diferentes.", "correcao": "Um peso grande para “idade em anos” e pequeno para “renda em reais” não diz qual importa mais. Padronize as variáveis antes."},
            ],
        },
        {
            "tipo": "ponte",
            "titulo": "Um neurônio é uma regressão logística",
            "corpo": r"""<p>Um neurônio artificial faz exatamente $\sigma(w \cdot x + b)$, só que com muitas entradas: $x$ e $w$ viram <b>vetores</b> e $w x$ vira o produto escalar da aula de Matemática.</p>
<p>Quando há mais de duas classes (gato, cachorro, pássaro, ou a próxima palavra de um texto), a sigmoide é trocada pelo <b>softmax</b>, que distribui 100% de probabilidade entre todas as opções. É assim que um LLM escolhe o próximo token.</p>""",
        },
        {
            "tipo": "quiz",
            "corpo": r"""<p>3 perguntas. Acertando 2, a camada “Vá mais fundo” é liberada e as revisões são agendadas.</p>""",
            "perguntas": [
                {"pergunta": "O que a sigmoide garante?", "opcoes": ["Que a saída fique entre 0 e 1.", "Que o modelo acerte todos os exemplos.", "Que a fronteira de decisão seja curva."], "correta": 0,
                 "explicacao": "Ela espreme qualquer escore para dentro de (0, 1), por isso a saída pode ser lida como probabilidade."},
                {"pergunta": "Com $w = 2$ e $b = -10$, onde fica a fronteira (limiar 0,5)?", "opcoes": ["Em x = 2", "Em x = 5", "Em x = 10"], "correta": 1,
                 "explicacao": "Limiar 0,5 é quando $z = 0$: $2x - 10 = 0$, então $x = 5$."},
                {"pergunta": "Num detector de fraude, deixar passar uma fraude custa caro. O que fazer com o limiar?", "opcoes": ["Subir para 0,9.", "Baixar, por exemplo para 0,2.", "Manter 0,5 sempre."], "correta": 1,
                 "explicacao": "Limiar mais baixo marca mais transações como suspeitas: pega mais fraudes, ao custo de mais alarmes falsos."},
            ],
        },
        {
            "tipo": "camadas",
            "ponte": [
                {"nome": "StatQuest, “Logistic Regression Details Pt1: Coefficients”", "url": "https://www.youtube.com/watch?v=vN5cNN2-HWE",
                 "trecho": "vídeo completo (legendas em português)", "tempo": 19, "foco": "Por que os coeficientes vivem na escala do log das chances, e como lê-los."},
            ],
            "profundidade": [
                {"obra": "James, Witten, Hastie &amp; Tibshirani, <i>An Introduction to Statistical Learning</i> (PDF gratuito)", "url": "https://www.statlearning.com/",
                 "secao": "Capítulo 4, seção 4.3 “Logistic Regression” (até 4.3.3)",
                 "perguntas": ["Que exemplo de dados o livro usa para mostrar o problema de ajustar uma reta?",
                               "Como o livro interpreta um aumento de uma unidade em x no log das chances?"]},
                {"obra": "Dive into Deep Learning, “Softmax Regression”", "url": "https://d2l.ai/chapter_linear-classification/softmax-regression.html",
                 "secao": "Seção 4.1, até a função de perda (em inglês, com código)",
                 "perguntas": ["Como o softmax generaliza a sigmoide para várias classes?"]},
            ],
            "revisao": [
                {"nome": "scikit-learn, “Logistic regression” (guia do usuário)", "url": "https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression",
                 "trecho": "seção 1.1.11, primeiros parágrafos", "tempo": 15, "foco": "A versão de engenharia: parâmetros, regularização e quando usar cada solver."},
            ],
        },
    ],
    "resumo": [
        "Para sim ou não, a saída precisa ser uma probabilidade entre 0 e 1: uma reta não serve.",
        r"A regressão logística calcula $\hat p = \sigma(w x + b)$; a sigmoide transforma o escore numa curva em S.",
        "O limiar transforma a probabilidade numa decisão; mudá-lo troca acertos de um tipo por erros de outro.",
        "Um neurônio artificial é uma regressão logística; com várias classes, a sigmoide vira softmax.",
    ],
    "proxima": "Métricas de classificação: acurácia, precisão, recall e F1, para medir esses acertos e erros.",
    "referencias": [
        {"obra": "StatQuest, “Logistic Regression”", "uso": "Intuição visual da curva em S e da máxima verossimilhança."},
        {"obra": "An Introduction to Statistical Learning, cap. 4", "uso": "Formalização e interpretação das chances."},
    ],
}

# ---------------------------------------------------------------------------
# Fase 5 · Mecanismo de atenção
# ---------------------------------------------------------------------------
PILOT_ATENCAO = {
    "v": 2,
    "duracao": 60,
    "gancho": r"""“Sentei no <b>banco</b> da praça” e “abri uma conta no <b>banco</b>”. Mesma palavra, sentidos diferentes, e você resolve isso olhando para as <b>outras palavras da frase</b>. Um Transformer faz igual: cada palavra “presta atenção” nas outras para descobrir o que significa naquele contexto. Essa operação é o coração de todo LLM.""",
    "objetivos": [
        "explicar o que consulta (query), chave (key) e valor (value) fazem;",
        "calcular pesos de atenção com produto escalar e softmax;",
        "entender para que serve a máscara causal e a divisão por √d;",
        "ler a fórmula da atenção sem travar.",
    ],
    "prerequisitos": [
        "Embeddings: palavras viram vetores (aula anterior desta fase).",
        "Produto escalar (trilha de Matemática) e softmax (aula de Regressão logística).",
    ],
    "blocos": [
        {
            "tipo": "palpite",
            "rotulo": "Chute antes de ver",
            "pergunta": "“O gato subiu no sofá porque <b>ele</b> estava cansado.” Para entender “ele”, para qual palavra é mais importante olhar?",
            "opcoes": ["gato", "sofá", "subiu"],
            "correta": 0,
            "porques": [
                "Isso! Quem fica cansado é o gato. Você ligou “ele” a “gato” prestando atenção na palavra certa.",
                "Sofá não se cansa. Mas repare que você precisou comparar “ele” com as outras palavras para decidir: é isso que a atenção faz.",
                "“Subiu” ajuda a montar a cena, mas não diz quem é “ele”.",
            ],
            "explicacao": "Resolver “ele = gato” é exatamente o tipo de ligação que uma camada de atenção aprende a fazer.",
        },
        {
            "tipo": "concreto",
            "titulo": "Numa festa barulhenta",
            "corpo": r"""<p>Dez conversas ao mesmo tempo e, mesmo assim, você ouve quando alguém fala o seu nome. Seu cérebro não ignora o resto: ele <b>dá pesos diferentes</b> para cada som.</p>
<p>A atenção de um Transformer funciona assim: para cada palavra, ela distribui <b>100% de atenção</b> pelas outras, muito para as relevantes e quase nada para as irrelevantes.</p>""",
        },
        {
            "tipo": "crianca",
            "corpo": r"""<p>Imagine que cada palavra levanta a mão com uma <b>pergunta</b> (“tem algum adjetivo perto de mim?”) e também carrega um <b>crachá</b> dizendo o que ela é (“sou um adjetivo de cor!”).</p>
<p>Quando a pergunta de uma palavra combina com o crachá de outra, as duas se conectam, e a primeira pega um pouco do <b>significado</b> da segunda. Pergunta = query, crachá = key, significado = value.</p>""",
        },
        {
            "tipo": "video",
            "rotulo": "Intuição visual (3Blue1Brown)",
            "id": "eMlx5fFNoYc",
            "inicio": 99,
            "fim": 760,
            "canal": "3Blue1Brown",
            "titulo_video": "Attention in transformers, step-by-step · Deep Learning, cap. 6",
            "corpo": r"""<p>Em inglês, com legendas em português (⚙️ → Legendas). Dos exemplos motivadores até a máscara (1:39 a 12:40).</p>""",
            "missao": [
                "Que palavra ele usa como exemplo de uma palavra com vários sentidos?",
                "Na frase da criatura, que palavras atualizam o significado de “creature”?",
                "O que é a <i>query</i>, o que é a <i>key</i>, e como ele mede se elas combinam?",
                "Para que serve a máscara (<i>masking</i>)?",
            ],
            "respostas": r"""<p><b>1.</b> “Mole”: pode ser o animal (toupeira), a unidade de química (mol) ou uma pinta na pele. O embedding inicial é o mesmo; o contexto é que decide.</p>
<p><b>2.</b> Os adjetivos “fluffy” e “blue”: a atenção move a informação deles para dentro do vetor de “creature”.</p>
<p><b>3.</b> A query é a “pergunta” que a palavra faz; a key é o “crachá” que a outra apresenta. Ele mede a combinação pelo <b>produto escalar</b> entre as duas: grande quando apontam na mesma direção. Depois aplica o softmax para virar pesos que somam 1.</p>
<p><b>4.</b> Para que palavras de trás não vejam as da frente. Assim o modelo pode treinar prevendo a próxima palavra sem “colar” a resposta.</p>""",
        },
        {
            "tipo": "notacao",
            "rotulo": "Agora sim, a fórmula",
            "titulo": "A fórmula que move os LLMs",
            "corpo": r"""$$\text{Atenção}(Q, K, V) = \text{softmax}\!\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V$$""",
            "itens": [
                {"simbolo": r"$Q,\ K,\ V$", "leitura": "consultas, chaves e valores", "significado": "Três versões de cada palavra, obtidas multiplicando o embedding por três matrizes aprendidas no treino."},
                {"simbolo": r"$Q K^\top$", "leitura": "Q vezes K transposta", "significado": "Todos os produtos escalares de uma vez: a pontuação de cada palavra com cada outra."},
                {"simbolo": r"$\sqrt{d_k}$", "leitura": "raiz de d k", "significado": "Divide as pontuações pelo tamanho dos vetores para elas não ficarem enormes e o softmax não ficar “decidido demais”."},
                {"simbolo": r"$\text{softmax}(\cdot)$", "leitura": "softmax", "significado": "Transforma cada linha de pontuações em pesos positivos que somam 1 (100% de atenção)."},
                {"simbolo": r"$\cdot\ V$", "leitura": "vezes V", "significado": "Mistura os valores das palavras de acordo com os pesos: o resultado é a palavra “atualizada pelo contexto”."},
            ],
        },
        {
            "tipo": "widget",
            "widget": "atencao",
            "titulo": "Para onde cada palavra olha",
            "corpo": r"""<p>Clique numa palavra (a consulta) e veja como ela distribui 100% de atenção entre as palavras anteriores. As pontuações são ilustrativas, no espírito do exemplo do vídeo.</p>""",
            "missoes": [
                "Clique em “creature”. Quem recebe mais atenção além dela mesma? Faz sentido?",
                "Clique em “forest” e depois em “roamed”. Em quem cada uma presta atenção?",
                "Leve a temperatura para 0,3 e depois para 3. O que acontece com as barras? Ligue isso à divisão por √d.",
                "Desmarque a máscara causal com “a” selecionada. Por que, num modelo que gera texto, isso seria “colar na prova”?",
            ],
        },
        {
            "tipo": "passos",
            "rotulo": "Resolvido passo a passo",
            "titulo": "Do produto escalar ao peso de atenção",
            "corpo": r"""<p>Uma consulta $q = [1, 0, 1]$ e três chaves: $k_1 = [1, 0, 1]$, $k_2 = [0, 1, 0]$, $k_3 = [1, 1, 1]$. Aqui $d_k = 3$.</p>""",
            "passos": [
                {"faca": r"Pontuações: $q \cdot k_1 = 2$, $q \cdot k_2 = 0$, $q \cdot k_3 = 2$.", "porque": "Produto escalar: multiplica posição a posição e soma."},
                {"faca": r"Escala: divida por $\sqrt{3} \approx 1{,}732$: fica $[1{,}155;\ 0;\ 1{,}155]$.", "porque": "Evita que vetores grandes gerem pontuações gigantes."},
                {"faca": r"Exponencial: $e^{1{,}155} \approx 3{,}173$ e $e^0 = 1$: $[3{,}173;\ 1;\ 3{,}173]$.", "porque": "O softmax primeiro deixa tudo positivo."},
                {"faca": r"Normalize: soma $= 7{,}346$; pesos $\approx [0{,}432;\ 0{,}136;\ 0{,}432]$.", "porque": "Divide pela soma para que os pesos somem 1."},
            ],
            "conclusao": r"$k_2$ é perpendicular a $q$ (produto escalar 0) e recebe o menor peso, mas não zero: o softmax nunca zera ninguém, só a máscara faz isso.",
        },
        {
            "tipo": "codigo",
            "rotulo": "Mão no código",
            "titulo": "Implemente a atenção de uma palavra",
            "enunciado": "Complete <code>softmax</code> e <code>pesos_de_atencao</code>. Um dos testes usa números grandes: se der <code>OverflowError</code>, veja a dica 2.",
            "inicial": "import math\n\ndef softmax(pontuacoes):\n    # devolva uma lista de probabilidades que somam 1: e^x / soma(e^x)\n    return []\n\ndef pesos_de_atencao(q, chaves):\n    # 1) pontuação de cada chave = produto escalar entre q e a chave\n    # 2) divida cada pontuação por sqrt(len(q))\n    # 3) aplique o softmax\n    return []\n\nq = [1, 0, 1]\nchaves = [[1, 0, 1], [0, 1, 0], [1, 1, 1]]\nprint([round(p, 3) for p in pesos_de_atencao(q, chaves)])\n",
            "testes": [
                {"nome": "softmax soma 1", "codigo": "assert abs(sum(softmax([2, 1, 0])) - 1) < 1e-9, f'somou {sum(softmax([2, 1, 0]))}'"},
                {"nome": "softmax([2, 1, 0]) ≈ [0,665; 0,245; 0,090]", "codigo": "assert [round(x, 3) for x in softmax([2, 1, 0])] == [0.665, 0.245, 0.09], f'deu {[round(x, 3) for x in softmax([2, 1, 0])]}'"},
                {"nome": "softmax aguenta números grandes", "codigo": "r = softmax([1001, 1000, 999])\nassert [round(x, 3) for x in r] == [0.665, 0.245, 0.09], f'deu {r}'"},
                {"nome": "Pesos do exemplo passo a passo", "codigo": "r = [round(x, 3) for x in pesos_de_atencao([1, 0, 1], [[1, 0, 1], [0, 1, 0], [1, 1, 1]])]\nassert r == [0.432, 0.136, 0.432], f'deu {r}'"},
            ],
            "dicas": [
                "Produto escalar: <code>sum(a * b for a, b in zip(q, k))</code>.",
                "Para números grandes, subtraia o maior valor antes da exponencial: <code>m = max(p)</code> e use <code>math.exp(x - m)</code>. O resultado do softmax não muda, e a conta não estoura.",
            ],
            "solucao": "import math\n\ndef softmax(pontuacoes):\n    m = max(pontuacoes)\n    ex = [math.exp(x - m) for x in pontuacoes]\n    total = sum(ex)\n    return [e / total for e in ex]\n\ndef pesos_de_atencao(q, chaves):\n    escala = math.sqrt(len(q))\n    pont = [sum(a * b for a, b in zip(q, k)) / escala for k in chaves]\n    return softmax(pont)\n\nq = [1, 0, 1]\nchaves = [[1, 0, 1], [0, 1, 0], [1, 1, 1]]\nprint([round(p, 3) for p in pesos_de_atencao(q, chaves)])",
            "explicacao": "<p>Subtrair o máximo é o truque de estabilidade numérica usado em todas as bibliotecas de deep learning.</p>",
        },
        {
            "tipo": "pratica",
            "titulo": "Treino em 3 níveis",
            "exercicios": [
                {"nivel": 1, "enunciado": r"Quanto vale cada peso de $\text{softmax}([0, 0])$?", "valor": 0.5,
                 "dicas": ["Duas pontuações iguais dividem a atenção igualmente."], "resposta": r"$e^0/(e^0+e^0) = 1/2 = 0{,}5$ para cada uma."},
                {"nivel": 2, "enunciado": r"As chaves têm dimensão $d_k = 64$. Por quanto dividimos as pontuações?", "valor": 8,
                 "dicas": [r"$\sqrt{64}$."], "resposta": r"$\sqrt{64} = 8$. Foi exatamente o valor usado no artigo original do Transformer."},
                {"nivel": 3, "enunciado": r"Um texto tem 1.000 tokens. Quantas pontuações de atenção uma camada (uma cabeça, sem máscara) calcula? Escreva o número sem pontos.", "valor": 1000000,
                 "dicas": ["Cada token compara sua consulta com a chave de cada token, inclusive a dele."], "resposta": r"$1000 \times 1000 = 10^6$. O custo cresce com o <b>quadrado</b> do contexto: dobrar o texto quadruplica a conta. É por isso que janelas de contexto longas são caras."},
            ],
        },
        {
            "tipo": "armadilhas",
            "itens": [
                {"erro": "“Os pesos de atenção explicam por que o modelo decidiu algo.”", "correcao": "Eles mostram para onde a informação fluiu numa camada, não a razão da resposta final. Há dezenas de camadas e cabeças combinadas."},
                {"erro": "“Sem a divisão por √d tanto faz.”", "correcao": "Com vetores grandes, as pontuações ficam enormes, o softmax vira quase “tudo em uma palavra” e os gradientes somem no treino."},
                {"erro": "“A máscara é um detalhe opcional.”", "correcao": "Num modelo que gera texto, sem máscara cada palavra veria as seguintes durante o treino, e o modelo aprenderia a copiar em vez de prever."},
                {"erro": "“Atenção é uma só.”", "correcao": "Cada camada tem várias cabeças (o GPT-3 tem 96 por camada), cada uma aprendendo um tipo de relação diferente."},
            ],
        },
        {
            "tipo": "ponte",
            "titulo": "Por que contexto longo custa caro",
            "corpo": r"""<p>Como cada token compara sua consulta com as chaves de todos os anteriores, o custo cresce com o quadrado do tamanho do texto. Duas ideias que você verá a seguir nesta fase atacam esse custo:</p>
<ul><li><b>KV cache</b>: ao gerar texto, as chaves e valores das palavras já lidas são guardados e reaproveitados, em vez de recalculados a cada novo token.</li>
<li><b>Janela de contexto</b>: o limite de tokens que o modelo consegue considerar de uma vez é, em boa parte, um limite de memória e tempo dessa conta.</li></ul>""",
        },
        {
            "tipo": "quiz",
            "corpo": r"""<p>3 perguntas. Acertando 2, a camada “Vá mais fundo” é liberada e as revisões são agendadas.</p>""",
            "perguntas": [
                {"pergunta": "Como a atenção mede o quanto uma palavra combina com outra?", "opcoes": ["Pela distância entre as posições na frase.", "Pelo produto escalar entre a query de uma e a key da outra.", "Contando letras em comum."], "correta": 1,
                 "explicacao": "Produto escalar grande = vetores apontando para o mesmo lado = combinam."},
                {"pergunta": "O que o softmax faz com as pontuações?", "opcoes": ["Transforma em pesos positivos que somam 1.", "Escolhe só a maior e zera as outras.", "Divide tudo por √d."], "correta": 0,
                 "explicacao": "Todas recebem algum peso; as maiores pontuações recebem mais."},
                {"pergunta": "Para que serve a máscara causal?", "opcoes": ["Para acelerar a conta.", "Para que uma palavra não veja as palavras que vêm depois dela.", "Para esconder palavras ofensivas."], "correta": 1,
                 "explicacao": "Assim o modelo treina prevendo o próximo token sem enxergar a resposta."},
            ],
        },
        {
            "tipo": "camadas",
            "ponte": [
                {"nome": "Jay Alammar, “The Illustrated Transformer”", "url": "https://jalammar.github.io/illustrated-transformer/",
                 "trecho": "seção “Self-Attention in Detail” (em inglês, muito visual)", "tempo": 25, "foco": "Os mesmos passos desta aula, com as matrizes Q, K e V desenhadas."},
                {"nome": "Jay Alammar, “The Narrated Transformer Language Model”", "url": "https://www.youtube.com/watch?v=-QH8fRhqFHM",
                 "trecho": "vídeo completo (em inglês)", "tempo": 30, "foco": "O Transformer inteiro em movimento, para ver onde a atenção se encaixa."},
            ],
            "profundidade": [
                {"obra": "Vaswani et al., <i>Attention Is All You Need</i> (2017, artigo original)", "url": "https://arxiv.org/abs/1706.03762",
                 "secao": "Seção 3.2 “Attention” (3.2.1 Scaled Dot-Product Attention e 3.2.2 Multi-Head Attention)",
                 "perguntas": ["Que justificativa os autores dão para dividir por √d_k?",
                               "Por que usar várias cabeças em vez de uma só, segundo o artigo?"]},
                {"obra": "Dive into Deep Learning, “Attention Scoring Functions”", "url": "https://d2l.ai/chapter_attention-mechanisms-and-transformers/attention-scoring-functions.html",
                 "secao": "Seção 11.3, até “Scaled Dot-Product Attention” (com código)",
                 "perguntas": ["Que outra função de pontuação o livro apresenta além do produto escalar?"]},
            ],
            "revisao": [
                {"nome": "3Blue1Brown, “Attention in transformers” (vídeo completo)", "url": "https://www.youtube.com/watch?v=eMlx5fFNoYc",
                 "trecho": "dos “Values” (13:10) até “Multiple heads” (22:16)", "tempo": 10, "foco": "A parte que não entrou no trecho desta aula: os valores e as várias cabeças."},
            ],
        },
    ],
    "resumo": [
        "Atenção deixa cada palavra atualizar seu significado olhando para as outras palavras da frase.",
        "Query e key se comparam por produto escalar; o softmax transforma as pontuações em pesos que somam 1.",
        "A saída é uma mistura dos values, ponderada por esses pesos; a divisão por √d e a máscara causal mantêm o treino estável e honesto.",
        "O custo cresce com o quadrado do contexto, o que explica KV cache e limites de janela.",
    ],
    "proxima": "Arquitetura Transformer: como camadas de atenção e de rede neural se empilham.",
    "referencias": [
        {"obra": "3Blue1Brown, “Attention in transformers, step-by-step”", "uso": "Exemplos visuais (mole, fluffy blue creature) e máscara."},
        {"obra": "Vaswani et al. (2017), Attention Is All You Need", "uso": "Fórmula da atenção escalada e multi-cabeça."},
    ],
}

# Ligação com os tópicos da trilha de IA (pelo título, como em build_ia_data.py)
IA_PILOT_GUIDES = {
    "Laços (for, while)": PILOT_LACOS,
    "Regressão logística": PILOT_LOGISTICA,
    "Mecanismo de atenção": PILOT_ATENCAO,
}
