# -*- coding: utf-8 -*-
"""
PILOTO de aulas de Matemática (formato "Concreto -> Desenho -> Fórmula").

Três aulas reescritas para validar o novo formato antes de expandir para as 43:
  1. Vetores e espaços vetoriais: intuição geométrica
  2. Produto escalar (Dot Product) e projeções
  3. Algoritmo de Descida do Gradiente (Vanilla Gradient Descent)

Princípios aplicados em todas:
  - Chute antes de ver (bloco "palpite"): ativa curiosidade e expõe a intuição errada antes de corrigi-la.
  - Concreto -> Desenho -> Fórmula (método de Singapura): o símbolo só aparece depois do significado.
  - "Explica como se eu tivesse 10 anos": a mesma ideia sem jargão.
  - Vídeos como etapas, não como lista: trecho exato + missão enquanto assiste.
      3Blue1Brown = intuição visual; Khan Academy Brasil = mecânica em português; StatQuest = revisão.
  - Widget manipulável: descobrir mexendo, com missões.
  - Prática em 3 níveis com correção automática e dicas em camadas.
  - Quiz de saída: aprovado -> revisões em 1, 3, 7 e 21 dias e libera "Vá mais fundo" (livros gratuitos).

Os blocos que já estavam bons nas aulas v2 são reaproveitados (não duplicamos conteúdo).
Vídeos e links verificados em 06/11/2026.
"""
import copy

from math_lessons_v2_mod1 import GUIDES_MOD1_V2, SVG_PARALELOGRAMO
from math_lessons_v2_mod2 import GUIDES_MOD2_V2
from math_lessons_v2_samples import LESSONS_V2_SAMPLES

T_VET = "Vetores e espaços vetoriais: intuição geométrica"
T_DOT = "Produto escalar (Dot Product) e projeções"
T_GD = "Algoritmo de Descida do Gradiente (Vanilla Gradient Descent)"

_vet = copy.deepcopy(GUIDES_MOD1_V2[T_VET])
_dot = copy.deepcopy(LESSONS_V2_SAMPLES[T_DOT])
_gd = copy.deepcopy(GUIDES_MOD2_V2[T_GD])

MML = "https://mml-book.github.io/book/mml-book.pdf"

# =========================================================================
# 1. VETORES
# =========================================================================
_vet_b = _vet["blocos"]  # 0 texto, 1 notacao, 2 visual, 3 ponte, 4 laboratorio, 5 desafio, 6 armadilhas

PILOT_VETORES = {
    "v": 2,
    "duracao": 40,
    "gancho": r"""Se alguém te disser só <b>“ande 3 passos”</b>, você fica parado: falta saber <i>para onde</i>. Essa informação que falta é exatamente o que separa um número comum de um <b>vetor</b>, a peça com que toda Inteligência Artificial é montada.""",
    "prerequisitos": ["Nada avançado: saber somar, multiplicar e localizar um ponto em um mapa quadriculado."],
    "objetivos": [
        "explicar com suas palavras o que é um vetor, como seta e como lista de números;",
        "somar vetores e multiplicá-los por um número, no desenho e na conta;",
        "ler a notação $\\vec v$, $v_i$ e $\\mathbb{R}^n$ sem travar;",
        "entender por que palavras viram vetores dentro de um modelo de linguagem.",
    ],
    "blocos": [
        {
            "tipo": "palpite",
            "pergunta": r"""O GPS diz: <b>“o restaurante fica a 5 km de você”</b>. Só com essa frase, você consegue chegar lá?""",
            "opcoes": ["Sim, é só andar 5 km.", "Não, falta saber a direção.", "Só se o caminho for em linha reta."],
            "correta": 1,
            "porques": [
                "Andar 5 km para o norte ou para o sul leva a lugares completamente diferentes.",
                "Exatamente: “5 km” diz o tamanho do deslocamento, mas não o sentido.",
                "Mesmo em linha reta, existem infinitas retas saindo de você. Qual delas?",
            ],
            "explicacao": r"""<p>“5 km” é um <b>escalar</b>: só um tamanho. Para chegar ao restaurante você precisa de <b>tamanho + direção</b>, por exemplo “3 km para leste e 4 km para norte”. Esse pacote é um <b>vetor</b>.</p>""",
        },
        {
            "tipo": "concreto",
            "titulo": "O mapa do tesouro",
            "corpo": r"""<p>Num mapa do tesouro está escrito: <b>“3 passos para a direita, 1 passo para cima”</b>. Dá para guardar essa instrução inteira em dois números entre colchetes:</p>
$$[3,\;1]$$
<p>Isso já é um vetor. Repare em duas coisas que vão valer para sempre:</p>
<ul>
<li><b>A ordem importa.</b> $[3, 1]$ (3 para a direita, 1 para cima) é outro tesouro que $[1, 3]$.</li>
<li><b>Cada posição tem um significado fixo.</b> A primeira é sempre “direita/esquerda”, a segunda é sempre “cima/baixo”.</li>
</ul>
<p>Agora troque o mapa por uma avaliação da nossa cafeteria: <code>[estrelas, número de palavras, sentimento]</code>, por exemplo $[5,\;40,\;0{,}9]$. É a mesma ideia: uma lista ordenada em que cada posição mede uma coisa. Para a IA, <b>um cliente, uma frase ou uma foto são só setas num mapa com muitas direções</b>.</p>""",
        },
        {
            "tipo": "crianca",
            "corpo": r"""<p>Um vetor é um <b>bilhete de instruções de caminhada</b>: “tantos passos para o lado, tantos para cima”.</p>
<p><b>Somar dois vetores</b> é seguir um bilhete e depois o outro, e ver onde você terminou.</p>
<p><b>Multiplicar por 2</b> é fazer cada passo em dobro. <b>Multiplicar por −1</b> é andar de costas: mesmo caminho, sentido contrário.</p>""",
        },
        {
            "tipo": "video",
            "rotulo": "Intuição visual (3Blue1Brown)",
            "id": "fNk_zzaMoSs",
            "inicio": 0,
            "fim": 172,
            "canal": "3Blue1Brown",
            "titulo_video": "Vectors · Essence of linear algebra, cap. 1",
            "corpo": r"""<p>Em inglês, com legendas em português disponíveis (ative em ⚙️ → Legendas → Traduzir automaticamente, se preciso). Só os primeiros 3 minutos.</p>""",
            "missao": [
                "Quais são as <b>três visões</b> de vetor que ele apresenta (física, computação e matemática)?",
                "Por que o físico pode “arrastar” a seta para qualquer lugar e continuar dizendo que é o mesmo vetor?",
            ],
            "respostas": r"""<p><b>1.</b> Física: seta com tamanho e direção. Computação: lista ordenada de números. Matemática: qualquer coisa que se possa somar e multiplicar por número respeitando certas regras.</p>
<p><b>2.</b> Porque o vetor é o <b>deslocamento</b> (o bilhete de instruções), não o lugar onde ele começa. “3 para a direita, 1 para cima” é a mesma instrução saindo da sua casa ou da escola.</p>""",
        },
        dict(_vet_b[2], rotulo="O desenho", titulo="Somar é encadear bilhetes",
             corpo=r"""<p>Siga o bilhete $\vec u = [3, 0]$ e, de onde parar, siga $\vec v = [1, 2]$. Você termina em $[4, 2]$: some posição com posição. No desenho, isso forma um paralelogramo:</p>"""),
        {
            "tipo": "widget",
            "widget": "vetores",
            "titulo": "Laboratório de setas",
            "corpo": r"""<p>Mexa nos controles e observe a seta verde ($\vec u + \vec v$) e a laranja ($k \cdot \vec v$).</p>""",
            "missoes": [
                "Faça $\\vec u + \\vec v$ cair exatamente na origem $[0, 0]$. Que relação $\\vec v$ precisa ter com $\\vec u$?",
                "Coloque $k = -1$. O que acontece com a seta laranja em relação a $\\vec v$?",
                "Com $\\vec v = [1, 2]$, qual $k$ faz $k \\cdot \\vec v = [2, 4]$? E $[-1, -2]$?",
                "Troque a ordem: a soma $\\vec u + \\vec v$ muda se você trocar os valores de $\\vec u$ com os de $\\vec v$? Por quê?",
            ],
        },
        {
            "tipo": "video",
            "rotulo": "A mecânica em português (Khan Academy Brasil)",
            "id": "Y0ZyUhi0khY",
            "inicio": 180,
            "fim": 320,
            "canal": "Khan Academy Brasil",
            "titulo_video": "Introdução aos vetores para a álgebra linear",
            "corpo": r"""<p>Só a parte em que ele sai do desenho e passa para a escrita (de 3:00 a 5:20). O começo do vídeo repete a ideia de seta que você já viu.</p>""",
            "missao": [
                "Anote como o professor escreve um vetor “em pé” (vetor coluna).",
                "Ele usa duas notações para o mesmo vetor. Quais são?",
            ],
            "respostas": r"""<p><b>1.</b> Em coluna, um número embaixo do outro: o deslocamento horizontal em cima (5) e o vertical embaixo (0). Ele comenta que essa é a forma mais comum.</p>
<p><b>2.</b> Deitado, entre parênteses, $(5, 0)$, e em pé, como coluna. Os dois guardam a mesma informação: primeiro o quanto anda na horizontal, depois na vertical. Ele também mostra que, no caderno, o vetor ganha uma setinha em cima: $\vec v$.</p>""",
        },
        dict(_vet_b[1], rotulo="Agora sim, a fórmula", titulo="A mesma ideia, na língua dos livros"),
        _vet_b[3],
        _vet_b[4],
        {
            "tipo": "pratica",
            "titulo": "Treino em 3 níveis",
            "corpo": r"""<p>Para vetores, digite os componentes separados por ponto e vírgula, por exemplo <code>3; -1</code>.</p>""",
            "exercicios": [
                {"nivel": 1, "enunciado": r"Calcule $[2,\,5] + [1,\,-3]$.", "valor": [3, 2],
                 "dicas": ["Some primeiro com primeiro, segundo com segundo."],
                 "resposta": r"$[2+1,\;5+(-3)] = [3,\;2]$."},
                {"nivel": 1, "enunciado": r"Calcule $3 \cdot [2,\,-1]$.", "valor": [6, -3],
                 "dicas": ["Multiplique cada componente por 3."],
                 "resposta": r"$[3\times2,\;3\times(-1)] = [6,\;-3]$. A seta ficou 3 vezes maior, na mesma direção."},
                {"nivel": 2, "enunciado": r"Um robô segue três bilhetes em sequência: $[2,\,1]$, depois $[-1,\,3]$, depois $[4,\,0]$. Onde ele termina, saindo da origem?", "valor": [5, 4],
                 "dicas": ["Encadear bilhetes = somar os vetores.", "Some as primeiras posições: $2 - 1 + 4$."],
                 "resposta": r"$[2-1+4,\;1+3+0] = [5,\;4]$. A ordem dos bilhetes não muda o ponto final (a soma é comutativa)."},
                dict(_vet_b[5]["exercicios"][0], nivel=2, valor=[13, -17, 8]),
                {"nivel": 3, "enunciado": r"Na cafeteria, as avaliações viram vetores <code>[estrelas, palavras, sentimento]</code>. A avaliação A é $[5,\;40,\;0{,}9]$ e a B é $[1,\;12,\;-0{,}8]$. Calcule a <b>média</b> $\tfrac{1}{2}(A + B)$, o “cliente típico” desse grupo.", "valor": [3, 26, 0.05],
                 "dicas": ["Primeiro some A + B.", r"Depois multiplique o resultado pelo escalar $\tfrac12$."],
                 "resposta": r"$A+B = [6,\;52,\;0{,}1]$ e $\tfrac12(A+B) = [3,\;26,\;0{,}05]$. Esse “ponto do meio” se chama <b>centroide</b> e é exatamente o que o algoritmo K-Means calcula para cada grupo de clientes."},
                {"nivel": 3, "enunciado": r"Qual número $k$ faz $k \cdot [2,\,-6] = [-1,\,3]$?", "valor": -0.5,
                 "dicas": ["Olhe só a primeira posição: $k \\times 2 = -1$.", "Confira se o mesmo $k$ funciona na segunda posição."],
                 "resposta": r"$k = -\tfrac12$: metade do tamanho e sentido invertido. Conferindo: $-\tfrac12 \times (-6) = 3$ ✓. Quando existe um $k$ assim, dizemos que os vetores são <b>paralelos</b>."},
            ],
        },
        _vet_b[6],
        {
            "tipo": "quiz",
            "corpo": r"""<p>3 perguntas rápidas. Acertando 2, a camada “Vá mais fundo” é liberada e as revisões são agendadas.</p>""",
            "perguntas": [
                {"pergunta": r"$[1, 3]$ e $[3, 1]$ são o mesmo vetor?", "opcoes": ["Sim, têm os mesmos números.", "Não, a ordem dos componentes importa."], "correta": 1,
                 "explicacao": "Cada posição tem um significado fixo. 1 para a direita e 3 para cima não é o mesmo que 3 para a direita e 1 para cima."},
                {"pergunta": r"O que acontece com uma seta quando você a multiplica por $-2$?", "opcoes": ["Fica com metade do tamanho.", "Dobra de tamanho e inverte o sentido.", "Gira 90 graus."], "correta": 1,
                 "explicacao": "O 2 dobra o tamanho e o sinal negativo vira a seta para o lado oposto."},
                {"pergunta": r"Em NumPy, quanto dá <code>np.array([1, 2]) + np.array([3, 4])</code>?", "opcoes": ["[1, 2, 3, 4]", "[4, 6]", "10"], "correta": 1,
                 "explicacao": "Arrays do NumPy somam como vetores (posição a posição). Já listas comuns do Python, <code>[1, 2] + [3, 4]</code>, são concatenadas: <code>[1, 2, 3, 4]</code>."},
            ],
        },
        {
            "tipo": "camadas",
            "ponte": [
                {"nome": "Immersive Linear Algebra, cap. 2 “Vectors”", "url": "https://immersivemath.com/ila/ch02_vectors/ch02.html",
                 "trecho": "§2.1 a §2.3 (em inglês)", "tempo": 25, "foco": "Livro com figuras que você arrasta com o mouse. Refaça as missões do laboratório nas figuras de soma e multiplicação por escalar."},
                {"nome": "MIT 18.06, Gilbert Strang, aula 1", "url": "https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/",
                 "trecho": "“The Geometry of Linear Equations” (em inglês, com transcrição)", "tempo": 40, "foco": "Veja como o professor mais famoso de Álgebra Linear usa combinações de vetores. Prepara o terreno para a aula 2."},
            ],
            "profundidade": [
                {"obra": "Deisenroth, Faisal & Ong, <i>Mathematics for Machine Learning</i> (PDF gratuito)", "url": MML,
                 "secao": "§2.4 Vector Spaces (leia até o fim dos exemplos de espaços vetoriais)",
                 "perguntas": ["Quais propriedades um conjunto precisa ter para ser um espaço vetorial? Liste 3 com suas palavras.",
                               r"Por que $\mathbb{R}^n$, com a soma e a multiplicação por escalar desta aula, é um espaço vetorial?",
                               "O livro dá exemplos de espaços vetoriais que não são “setas”. Qual achou mais surpreendente?"]},
            ],
        },
    ],
    "resumo": _vet["resumo"],
    "proxima": _vet["proxima"],
    "referencias": _vet["referencias"] + [
        {"obra": "Immersive Linear Algebra (Ström, Åström & Akenine-Möller)", "trecho": "cap. 2", "uso": "Figuras interativas de soma e escalar"},
    ],
}

# =========================================================================
# 2. PRODUTO ESCALAR
# =========================================================================
_dot_b = _dot["blocos"]
# 0 texto mercado, 1 notacao, 2 visual sombra, 3 tabela sinal, 4 pense, 5 passos projeção,
# 6 visual embeddings, 7 tabela votação, 8 ponte, 9 laboratorio, 10 desafio, 11 armadilhas
_dot_ex = _dot_b[10]["exercicios"]

PILOT_DOT = {
    "v": 2,
    "duracao": 45,
    "gancho": _dot["gancho"],
    "prerequisitos": _dot["prerequisitos"],
    "objetivos": _dot["objetivos"],
    "blocos": [
        {
            "tipo": "palpite",
            "pergunta": r"""No caixa do mercado: 2 pães (1,50 real cada), 3 leites (4 reais cada) e 1 café (12 reais). Guardando as <b>quantidades</b> em $[2, 3, 1]$ e os <b>preços</b> em $[1{,}5;\;4;\;12]$, qual conta dá o total da compra?""",
            "opcoes": ["Somar todos os números: 2 + 3 + 1 + 1,5 + 4 + 12.",
                       "Multiplicar cada quantidade pelo seu preço e somar.",
                       "Somar as quantidades e multiplicar pela soma dos preços."],
            "correta": 1,
            "porques": ["Somar quantidade com preço mistura “unidades” com “reais”, o que não tem sentido.",
                        "Isso: $2\\times1{,}5 + 3\\times4 + 1\\times12 = 27$.",
                        "Daria $6 \\times 17{,}5 = 105$: seria como se cada item custasse a soma de todos os preços."],
            "explicacao": r"""<p>Você acabou de inventar o <b>produto escalar</b>: multiplicar par a par e somar. Vamos ver por que essa conta simples é a operação mais usada de toda a IA.</p>""",
        },
        dict(_dot_b[0], tipo="concreto", rotulo="Começando pelo concreto"),
        {
            "tipo": "crianca",
            "corpo": r"""<p>Imagine dois amigos puxando uma caixa com cordas.</p>
<ul>
<li>Se puxam <b>para o mesmo lado</b>, a força se soma: o produto escalar é <b>positivo</b>.</li>
<li>Se um puxa para a frente e o outro <b>para o lado</b>, um não ajuda nem atrapalha o outro: o produto é <b>zero</b>.</li>
<li>Se puxam <b>em sentidos opostos</b>, um atrapalha o outro: o produto é <b>negativo</b>.</li>
</ul>
<p>O produto escalar é um <b>medidor de “o quanto vocês estão no mesmo time”</b>, levando em conta também a força de cada um.</p>""",
        },
        {
            "tipo": "video",
            "rotulo": "Intuição visual (3Blue1Brown)",
            "id": "LyGKycYT2v0",
            "inicio": 51,
            "fim": 236,
            "canal": "3Blue1Brown",
            "titulo_video": "Dot products and duality · Essence of linear algebra, cap. 9",
            "missao": [
                "O que ele “projeta” sobre o quê para explicar o produto escalar?",
                "Quando o resultado fica <b>negativo</b>? E quando dá <b>zero</b>?",
            ],
            "respostas": r"""<p><b>1.</b> Projeta um vetor sobre a reta do outro (a “sombra”) e multiplica o tamanho da sombra pelo tamanho do outro vetor.</p>
<p><b>2.</b> Negativo quando a sombra cai “para trás”, ou seja, quando os vetores apontam para lados opostos (ângulo maior que 90°). Zero quando são perpendiculares: a sombra vira um ponto.</p>""",
        },
        dict(_dot_b[2], rotulo="O desenho"),
        {
            "tipo": "widget",
            "widget": "produto_escalar",
            "titulo": "A sombra que vira número",
            "corpo": r"""<p>A faixa laranja é a sombra de $\vec w$ sobre $\vec v$. Compare as duas contas no quadro: a regra “multiplica e soma” e a geometria “sombra × comprimento” sempre empatam.</p>""",
            "missoes": [
                "Encontre o ângulo que faz o produto escalar dar <b>zero</b>. Algum comprimento muda isso?",
                "Com ângulo de 45°, dobre o comprimento de $\\vec w$. O que acontece com $\\vec v \\cdot \\vec w$? E com $\\cos\\theta$?",
                "Monte a configuração com o produto <b>mais negativo possível</b>. Qual ângulo e quais comprimentos?",
                "Deixe o ângulo em 60°. Por que a sombra mede exatamente metade do comprimento de $\\vec w$?",
            ],
        },
        _dot_b[3],
        _dot_b[4],
        dict(_dot_b[1], rotulo="Agora sim, a fórmula"),
        {
            "tipo": "video",
            "rotulo": "A mecânica em português (Khan Academy Brasil)",
            "id": "OtGMHiOmMGE",
            "inicio": 0,
            "fim": 268,
            "canal": "Khan Academy Brasil",
            "titulo_video": "Produto escalar",
            "corpo": r"""<p>Só os primeiros 4 minutos e meio: a definição e a ideia da “sombra”. Depois disso ele parte para um exemplo de física.</p>""",
            "missao": [
                "Ele escreve a definição com cosseno, não com “multiplica e soma”. Anote-a e diga o que é $\\theta$.",
                "Que imagem ele usa para explicar $|\\vec a|\\cos\\theta$? Ela bate com a faixa laranja do laboratório?",
            ],
            "respostas": r"""<p><b>1.</b> $\vec a \cdot \vec b = |\vec a|\,|\vec b|\cos\theta$, em que $\theta$ é o ângulo entre os dois vetores. É a mesma operação do somatório $\sum a_i b_i$, vista pela geometria: as duas contas sempre dão o mesmo número.</p>
<p><b>2.</b> Uma lanterna acesa bem em cima, perpendicular a $\vec b$: a sombra de $\vec a$ sobre $\vec b$ mede $|\vec a|\cos\theta$, a parte de $\vec a$ que vai na mesma direção de $\vec b$. É exatamente a faixa laranja do laboratório.</p>""",
        },
        _dot_b[5],
        _dot_b[6],
        _dot_b[7],
        _dot_b[8],
        _dot_b[9],
        {
            "tipo": "pratica",
            "titulo": "Treino em 3 níveis",
            "corpo": r"""<p>Para respostas com vetores, separe os componentes por ponto e vírgula, por exemplo <code>2,5; 2,5</code>.</p>""",
            "exercicios": [
                {"nivel": 1, "enunciado": r"Calcule $[2,\,3,\,1] \cdot [1{,}5;\;4;\;12]$ (a conta do mercado).", "valor": 27,
                 "dicas": ["Multiplique posição por posição e some."],
                 "resposta": r"$3 + 12 + 12 = 27$."},
                {"nivel": 1, "enunciado": r"Calcule $[1,\,2] \cdot [2,\,-1]$. O que o resultado diz sobre o ângulo?", "valor": 0,
                 "dicas": ["$1\\times2 + 2\\times(-1)$."],
                 "resposta": r"$2 - 2 = 0$: os vetores são <b>perpendiculares</b>, mesmo sem nenhum ser nulo."},
                dict(_dot_ex[0], nivel=2, valor=1),
                dict(_dot_ex[1], nivel=2, valor=-1),
                dict(_dot_ex[2], nivel=2, valor=[2.5, 2.5]),
                dict(_dot_ex[3], nivel=3),
                {"nivel": 3, "enunciado": r"Um neurônio tem pesos $\vec w = [0{,}5;\;-1;\;2]$ e viés $b = -0{,}5$. Para a entrada $\vec x = [4,\;1,\;0{,}5]$, calcule $z = \vec w \cdot \vec x + b$. O neurônio “dispara” ($z > 0$)?", "valor": 1.5,
                 "dicas": ["Primeiro o produto escalar $\\vec w \\cdot \\vec x$.", "$2 - 1 + 1 = 2$. Agora some o viés."],
                 "resposta": r"$\vec w\cdot\vec x = 0{,}5\times4 + (-1)\times1 + 2\times0{,}5 = 2 - 1 + 1 = 2$, então $z = 2 - 0{,}5 = 1{,}5 > 0$: dispara. Cada neurônio de uma rede faz exatamente esta conta."},
            ],
        },
        _dot_b[11],
        {
            "tipo": "quiz",
            "corpo": r"""<p>3 perguntas. Acertando 2, a camada “Vá mais fundo” é liberada e as revisões são agendadas.</p>""",
            "perguntas": [
                {"pergunta": "O resultado de um produto escalar é...", "opcoes": ["um vetor do mesmo tamanho dos originais.", "um único número.", "uma matriz."], "correta": 1,
                 "explicacao": "Multiplica par a par e <b>soma tudo</b>: sobra um número só, um escalar. Daí o nome."},
                {"pergunta": r"Dois embeddings têm produto escalar $-7$. O que isso sugere?", "opcoes": ["Apontam para lados opostos: significados que “discordam”.", "São perpendiculares.", "Um deles é o vetor nulo."], "correta": 0,
                 "explicacao": "Sinal negativo = ângulo maior que 90°. As dimensões votaram mais contra do que a favor da semelhança."},
                {"pergunta": r"Em NumPy, com <code>a</code> e <code>b</code> vetores, qual expressão calcula o produto escalar?", "opcoes": ["<code>a * b</code>", "<code>a @ b</code>", "<code>a + b</code>"], "correta": 1,
                 "explicacao": "<code>a * b</code> multiplica elemento a elemento e devolve um vetor. O produto escalar é <code>a @ b</code> (ou <code>np.dot(a, b)</code>)."},
            ],
        },
        {
            "tipo": "camadas",
            "ponte": [
                {"nome": "Immersive Linear Algebra, cap. 3 “The Dot Product”", "url": "https://immersivemath.com/ila/ch03_dotproduct/ch03.html",
                 "trecho": "§3.1 a §3.3 (em inglês)", "tempo": 30, "foco": "Arraste os vetores nas figuras e confira o que você descobriu no laboratório da sombra."},
            ],
            "profundidade": [
                {"obra": "Deisenroth, Faisal & Ong, <i>Mathematics for Machine Learning</i> (PDF gratuito)", "url": MML,
                 "secao": "§3.2 Inner Products, §3.4 Angles and Orthogonality e §3.8 Orthogonal Projections",
                 "perguntas": ["O livro chama o produto escalar de “dot product” e fala de outros “inner products”. Qual a diferença?",
                               r"Como o livro define <i>ortogonal</i>? Bate com o “produto zero” desta aula?",
                               "Encontre no §3.8 a fórmula da projeção e compare com a que você calculou nos passos desta aula."]},
            ],
            "revisao": [
                {"nome": "3Blue1Brown, “Dot products and duality” (trecho final)", "url": "https://www.youtube.com/watch?v=LyGKycYT2v0&t=436s",
                 "trecho": "7:14 → 12:09", "tempo": 5, "foco": "No dia da revisão: um exemplo numérico e o caso de vetores que não têm tamanho 1."},
            ],
        },
    ],
    "resumo": _dot["resumo"],
    "proxima": _dot["proxima"],
    "referencias": _dot["referencias"] + [
        {"obra": "Immersive Linear Algebra (Ström, Åström & Akenine-Möller)", "trecho": "cap. 3", "uso": "Figuras interativas de produto escalar e projeção"},
    ],
}

# =========================================================================
# 3. DESCIDA DO GRADIENTE
# =========================================================================
_gd_b = _gd["blocos"]  # 0 texto anatomia, 1 tabela variantes, 2 passos à mão, 3 laboratorio

PILOT_GD = {
    "v": 2,
    "duracao": 45,
    "gancho": r"""Você está no alto de um morro, com <b>neblina total</b>. Não enxerga o vale, só sente a inclinação do chão sob os pés. Como chegar lá embaixo? A resposta para essa pergunta é, literalmente, o jeito como o ChatGPT, o Gemini e qualquer rede neural <b>aprendem</b>.""",
    "prerequisitos": [
        "Derivada como inclinação: o sinal diz se a curva sobe ou desce (tópico 13).",
        "Vetor gradiente $\\nabla f$: a seta que aponta para onde a função mais sobe (tópico 16).",
    ],
    "objetivos": [
        "explicar a descida do gradiente com uma analogia do dia a dia e com a fórmula $w \\leftarrow w - \\eta\\,\\nabla L$;",
        "calcular passos à mão e prever o efeito da taxa de aprendizado $\\eta$;",
        "reconhecer na prática os sintomas de $\\eta$ pequeno demais, bom e grande demais;",
        "comparar Batch, SGD e Mini-batch, e entender por que o Mini-batch é o padrão.",
    ],
    "blocos": [
        {
            "tipo": "palpite",
            "pergunta": r"""Na neblina, você só sente a inclinação do chão onde está pisando. Qual a melhor estratégia para chegar ao vale?""",
            "opcoes": ["Andar em uma direção qualquer e torcer.",
                       "Dar um passo para onde o chão desce mais e repetir.",
                       "Dar um único passo gigante para baixo."],
            "correta": 1,
            "porques": ["Sem usar a inclinação, você pode subir em vez de descer.",
                        "Isso: sentir a inclinação, dar um passo, sentir de novo. Essa é a descida do gradiente.",
                        "Um passo gigante pode passar do vale e cair na encosta do outro lado, mais alto do que antes."],
            "explicacao": r"""<p>Repare que a terceira opção não é boba: o <b>tamanho do passo</b> é decisivo. Ele tem nome, <b>taxa de aprendizado</b> ($\eta$, “eta”), e você vai ver no laboratório o que acontece quando ele é grande demais.</p>""",
        },
        {
            "tipo": "concreto",
            "titulo": "Ajustando a temperatura do chuveiro",
            "corpo": r"""<p>Você entra no banho e a água está <b>muito quente</b>. O que faz? Gira o registro para o lado frio. <b>Quanto</b> você gira depende de <b>quão errado</b> está: muito quente, gira bastante; quase bom, gira só um pouquinho.</p>
<p>Esse ajuste tem três ingredientes, que são exatamente os da descida do gradiente:</p>
<ul>
<li><b>O erro</b> (“está 10 °C acima do que eu quero”) é a <b>perda</b> $L$.</li>
<li><b>Para que lado girar</b> e <b>quanto</b> vem da inclinação do erro: o <b>gradiente</b>. Muito errado = gradiente grande = giro grande.</li>
<li><b>A sua coragem ao girar</b> é a <b>taxa de aprendizado</b> $\eta$. Medroso demais e o banho esfria antes de acertar. Corajoso demais e você passa do ponto: congela, gira de volta, queima... é o “zigue-zague”.</li>
</ul>
<p>Uma rede neural faz isso com <b>bilhões de registros ao mesmo tempo</b>, um para cada peso.</p>""",
        },
        {
            "tipo": "crianca",
            "corpo": r"""<p>Sabe a brincadeira de <b>“quente ou frio”</b>? Alguém esconde um objeto e só diz “tá esquentando” ou “tá esfriando”.</p>
<p>Você nunca vê o objeto, mas a cada passo sabe se está indo bem. Se der passos pequenos, chega devagar. Se der pulos enormes, passa do lugar e precisa voltar.</p>
<p>O computador brinca disso para aprender: o <b>erro</b> diz “quente ou frio”, e ele ajusta os números passo a passo.</p>""",
        },
        {
            "tipo": "video",
            "rotulo": "Intuição visual (3Blue1Brown)",
            "id": "IHZwWFHWa-w",
            "inicio": 415,
            "fim": 739,
            "canal": "3Blue1Brown",
            "titulo_video": "Gradient descent, how neural networks learn · Deep Learning, cap. 2",
            "missao": [
                "Por que o algoritmo anda no sentido <b>oposto</b> ao gradiente?",
                "O que acontece com o tamanho dos passos quando a bolinha se aproxima do fundo do vale? Por quê?",
            ],
            "respostas": r"""<p><b>1.</b> O gradiente aponta para onde a perda <b>sobe</b> mais rápido. Como queremos que ela desça, vamos no sentido contrário (daí o sinal de menos na fórmula).</p>
<p><b>2.</b> Ficam menores sozinhos, porque perto do fundo a inclinação é pequena, e o passo é proporcional à inclinação.</p>""",
        },
        {
            "tipo": "widget",
            "widget": "descida",
            "titulo": "Desça a montanha você mesmo",
            "corpo": r"""<p>A curva é a perda $L(w) = (w - 3)^2$, com o mínimo em $w = 3$. Escolha o chute inicial e a taxa de aprendizado, e dê passos.</p>""",
            "missoes": [
                "Com $\\eta = 0{,}1$ e $w_0 = 0$: quantos passos até convergir? Os passos ficam menores perto do fundo?",
                "Coloque $\\eta = 0{,}5$. Por que chega ao mínimo em <b>um único passo</b>? (Dica: faça a conta $w - 0{,}5 \\cdot 2(w-3)$.)",
                "Coloque $\\eta = 0{,}8$. Descreva o caminho. Ainda converge?",
                "Coloque $\\eta = 1$ e depois $\\eta = 1{,}05$. O que muda entre “ping-pong” e “explosão”?",
            ],
        },
        {
            "tipo": "notacao",
            "rotulo": "Agora sim, a fórmula",
            "titulo": "A regra que move a IA, símbolo por símbolo",
            "corpo": r"""<p>Tudo o que você fez no laboratório cabe em uma linha:</p>
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \eta\,\nabla L(\mathbf{w}_t)$$""",
            "itens": [
                {"simbolo": r"$\mathbf{w}_t$", "leitura": "w no passo t", "significado": "Os pesos atuais (a posição no morro, ou o registro do chuveiro agora)."},
                {"simbolo": r"$\nabla L(\mathbf{w}_t)$", "leitura": "gradiente de L em w t", "significado": "A seta que aponta para onde o erro <b>sobe</b> mais rápido. No laboratório, com uma variável só, era $2(w-3)$."},
                {"simbolo": r"$-$", "leitura": "menos", "significado": "Andamos no sentido <b>contrário</b> ao gradiente, para descer."},
                {"simbolo": r"$\eta$", "leitura": "eta (taxa de aprendizado)", "significado": "O tamanho do passo, a “coragem”. Número positivo pequeno, tipicamente entre 0,0001 e 0,1 em redes reais."},
                {"simbolo": r"$\mathbf{w}_{t+1}$", "leitura": "w no passo t mais 1", "significado": "A nova posição, depois do passo. Repete-se milhares ou milhões de vezes."},
            ],
        },
        _gd_b[2],
        {
            "tipo": "armadilhas",
            "itens": [
                {"erro": "“Taxa de aprendizado maior = aprende mais rápido.”",
                 "correcao": "Só até certo ponto. Passou do limite, os passos pulam o vale e o erro cresce até virar NaN, como você viu com $\\eta > 1$."},
                {"erro": "“O gradiente aponta para o mínimo.”",
                 "correcao": "Aponta para onde a perda <b>sobe</b> mais rápido. Por isso a fórmula tem o sinal de menos."},
                {"erro": "“Se parou de descer, achou a melhor solução possível.”",
                 "correcao": "Pode ter parado num vale local ou num ponto de sela. Em redes enormes isso é comum e, felizmente, esses vales costumam ser bons o bastante (tópico 20)."},
            ],
        },
        _gd_b[1],
        _gd_b[3],
        {
            "tipo": "pratica",
            "titulo": "Treino em 3 níveis",
            "corpo": r"""<p>Use $L(w) = (w - 3)^2$, cujo gradiente é $2(w - 3)$, a menos que o enunciado diga outra coisa.</p>""",
            "exercicios": [
                {"nivel": 1, "enunciado": r"Em $w = 5$, quanto vale o gradiente $2(w-3)$?", "valor": 4,
                 "dicas": ["Substitua $w$ por 5."],
                 "resposta": r"$2(5-3) = 4$. Positivo: a perda sobe para a direita, então devemos andar para a <b>esquerda</b>."},
                {"nivel": 1, "enunciado": r"Partindo de $w = 5$ com $\eta = 0{,}1$, qual é o novo $w$ após um passo?", "valor": 4.6,
                 "dicas": ["$w_{novo} = w - \\eta \\times \\text{gradiente}$.", "$5 - 0{,}1 \\times 4$."],
                 "resposta": r"$5 - 0{,}4 = 4{,}6$. Andou para a esquerda, em direção ao mínimo em 3."},
                {"nivel": 2, "enunciado": r"Partindo de $w_0 = -1$ com $\eta = 0{,}5$, quanto vale $w_1$?", "valor": 3,
                 "dicas": ["Gradiente em $-1$: $2(-1-3) = -8$.", "$w_1 = -1 - 0{,}5\\times(-8)$."],
                 "resposta": r"$w_1 = -1 + 4 = 3$: chegou ao mínimo em um passo. Com $\eta = 0{,}5$, a regra vira $w - (w-3) = 3$ para <b>qualquer</b> ponto de partida. Coincidência desta parábola: em problemas reais não existe esse $\eta$ mágico."},
                {"nivel": 2, "enunciado": r"Agora $L(w) = w^2$, cujo gradiente é $2w$. Partindo de $w_0 = 4$ com $\eta = 0{,}25$, quanto vale $w_3$ (depois de 3 passos)?", "valor": 0.5,
                 "dicas": ["Cada passo faz $w \\leftarrow w - 0{,}25 \\times 2w = 0{,}5\\,w$.", "Então $w$ cai pela metade a cada passo."],
                 "resposta": r"$4 \to 2 \to 1 \to 0{,}5$. Cada passo corta a distância ao mínimo pela metade: isso se chama <b>convergência linear</b>."},
                {"nivel": 3, "enunciado": r"Com $\eta = 1$, partindo de $w_0 = 0$ em $L(w) = (w-3)^2$, quanto vale $w_2$? O que isso revela?", "valor": 0,
                 "dicas": ["$w_1 = 0 - 1\\times2(0-3) = 6$.", "Agora calcule $w_2$ a partir de $w_1 = 6$."],
                 "resposta": r"$w_1 = 6$ e $w_2 = 6 - 2(6-3) = 0$. Voltou ao início! Com $\eta = 1$ o algoritmo fica pulando entre 0 e 6 para sempre, sem nunca descer. Taxa de aprendizado grande demais não “aprende mais rápido”: trava ou explode."},
                {"nivel": 3, "enunciado": r"Um neurônio sem viés prevê $\hat y = w\,x$. Com $x = 2$, alvo $y = 5$ e perda $L = (wx - y)^2$, o gradiente é $\frac{dL}{dw} = 2(wx - y)\,x$. Partindo de $w = 1$ com $\eta = 0{,}05$, qual é o novo $w$?", "valor": 1.6,
                 "dicas": ["Erro: $wx - y = 2 - 5 = -3$.", "Gradiente: $2 \\times (-3) \\times 2 = -12$. Agora aplique a regra."],
                 "resposta": r"$w = 1 - 0{,}05\times(-12) = 1{,}6$. A previsão foi de $2$ para $3{,}2$, mais perto do alvo 5. Treinar uma rede é repetir isto para milhões de pesos e exemplos."},
            ],
        },
        {
            "tipo": "quiz",
            "corpo": r"""<p>3 perguntas. Acertando 2, a camada “Vá mais fundo” é liberada e as revisões são agendadas.</p>""",
            "perguntas": [
                {"pergunta": "Por que a regra tem um sinal de menos: $w - \\eta\\nabla L$?", "opcoes": ["Porque o gradiente aponta para onde a perda sobe, e queremos descer.", "Para os pesos ficarem sempre negativos.", "É só uma convenção de notação."], "correta": 0,
                 "explicacao": "O gradiente é a direção de maior subida. Andar no sentido oposto faz a perda diminuir."},
                {"pergunta": "O treino mostra a perda subindo a cada passo até virar NaN. Qual o suspeito número 1?", "opcoes": ["Taxa de aprendizado pequena demais.", "Taxa de aprendizado grande demais.", "Poucos dados de treino."], "correta": 1,
                 "explicacao": "Passos grandes demais pulam o vale e caem cada vez mais alto do outro lado, como no laboratório com $\\eta > 1$."},
                {"pergunta": "Qual variante é o padrão no treino de redes neurais modernas?", "opcoes": ["Batch GD, com todos os dados a cada passo.", "SGD puro, com 1 exemplo por passo.", "Mini-batch, com um lote pequeno por passo."], "correta": 2,
                 "explicacao": "O Mini-batch equilibra estabilidade e velocidade e aproveita o paralelismo das GPUs."},
            ],
        },
        {
            "tipo": "camadas",
            "ponte": [
                {"nome": "Dive into Deep Learning, §12.3 “Gradient Descent”", "url": "https://d2l.ai/chapter_optimization/gd.html",
                 "trecho": "§12.3.1 One-Dimensional Gradient Descent (em inglês, com código)", "tempo": 30,
                 "foco": "O livro mostra os mesmos três casos do laboratório (η pequeno, bom e grande) com gráficos e código que você pode rodar no Colab."},
                {"nome": "Khan Academy Brasil, “Gradiente”", "url": "https://www.youtube.com/watch?v=Vn4ZuylKYQk",
                 "trecho": "vídeo completo, em português", "tempo": 7, "foco": "Se o “vetor gradiente” ainda estiver nebuloso, reveja este pré-requisito."},
            ],
            "profundidade": [
                {"obra": "Deisenroth, Faisal & Ong, <i>Mathematics for Machine Learning</i> (PDF gratuito)", "url": MML,
                 "secao": "§7.1 Optimization Using Gradient Descent (incluindo §7.1.1 Step-size e §7.1.3 Stochastic Gradient Descent)",
                 "perguntas": ["Que estratégia o livro sugere para ajustar o tamanho do passo quando a perda sobe?",
                               "Como o livro justifica que o SGD funciona, mesmo usando um gradiente “barulhento”?",
                               "O livro fala do “condicionamento” do problema. O que isso tem a ver com o zigue-zague do laboratório?"]},
                {"obra": "Goodfellow, Bengio & Courville, <i>Deep Learning</i> (online e gratuito)", "url": "https://www.deeplearningbook.org/contents/numerical.html",
                 "secao": "Capítulo 4, §4.3 Gradient-Based Optimization",
                 "perguntas": ["Como o livro define pontos críticos? Quais são os três tipos?",
                               "O que a Hessiana acrescenta à história contada só com o gradiente?"]},
            ],
            "revisao": [
                {"nome": "StatQuest, “Gradient Descent, Step-by-Step”", "url": "https://www.youtube.com/watch?v=sDv4f4s2SB8&t=85s",
                 "trecho": "1:25 → 5:38 e depois 9:40 → 14:48", "tempo": 15,
                 "foco": "Outra explicação, bem calma, com um exemplo de regressão. Ideal para o dia da revisão."},
            ],
        },
    ],
    "resumo": _gd["resumo"] + [
        "η pequeno demais: anda devagar. η adequado: converge. η grande demais: zigue-zague, ping-pong ou explosão.",
    ],
    "proxima": _gd["proxima"],
    "referencias": _gd["referencias"] + [
        {"obra": "Zhang, Lipton, Li & Smola, <i>Dive into Deep Learning</i>", "trecho": "§12.3 Gradient Descent", "uso": "Experimentos com a taxa de aprendizado"},
    ],
}

PILOT_GUIDES = {
    T_VET: PILOT_VETORES,
    T_DOT: PILOT_DOT,
    T_GD: PILOT_GD,
}
