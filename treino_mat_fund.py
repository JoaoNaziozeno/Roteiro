# -*- coding: utf-8 -*-
"""
Treino · Matemática, Módulo 1 do site (Fundamentos: funções, logaritmos, notação matemática e distâncias).

Cada aula mistura contas com números novos a cada vez (geradores em treino_contas_calc.py), saídas de código
(o gabarito é o que o Python/NumPy imprime de verdade) e questões de conceito.
"""
import textwrap


def c(s):
    return textwrap.dedent(s).strip("\n")


def conta(g, **p):
    q = {"k": "conta", "g": g}
    if p:
        q["p"] = p
    return q


TREINO = {
    "Equações, inequações e gráficos de funções aplicadas": [
        conta("linz"), conta("linlado"), conta("distplano"), conta("inequa"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            w = np.array([2.0, 1.5])
            b = -5.0
            X = np.array([[4, 2], [1, 1]])
            print(X @ w + b)
         '''),
         "opcoes": ["[ 6.  -1.5]", "[11.   3.5]", "[6.  1.5]", "[ 6.5 -1. ]"],
         "correta": 0,
         "x": "Cada linha de X é um ponto: 2·4 + 1,5·2 − 5 = 6 e 2·1 + 1,5·1 − 5 = −1,5. Um único <code>@</code> pontua todos os pontos de uma vez."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            z = np.array([2.5, -0.3, 0.0, 4.0])
            print((z > 0).astype(int))
         '''),
         "opcoes": ["[1 0 0 1]", "[1 0 1 1]", "[ True False False  True]", "[ 1 -1  0  1]"],
         "correta": 0,
         "x": "A regra de decisão é \"classe 1 se z &gt; 0\". O zero não é maior que zero, então fica 0. O <code>astype(int)</code> troca True/False por 1/0."},
        {"k": "conceito", "tema": "O que o vetor de pesos diz sobre a fronteira", "pergunta": r"Num classificador linear, o que o vetor de pesos $w$ diz sobre a fronteira $w \cdot x + b = 0$?",
         "opcoes": ["É perpendicular à fronteira e aponta para o lado positivo", "É paralelo à fronteira", "É um ponto em cima da fronteira", "Só muda a altura do gráfico"],
         "correta": 0,
         "x": "Andar na direção de w aumenta z o mais rápido possível. Por isso w é a normal da fronteira e aponta para onde z fica positivo."},
        {"k": "conceito", "pergunta": "O que acontece com a fronteira se só o viés b mudar?",
         "opcoes": ["Ela se desloca em paralelo, sem girar", "Ela gira em torno da origem", "Ela vira uma curva", "Nada: o viés não afeta a fronteira"],
         "correta": 0,
         "x": "A inclinação vem de w. O viés só empurra a reta para um lado ou para o outro."},
        {"k": "conceito", "pergunta": "Ao multiplicar ou dividir os dois lados de uma inequação por um número negativo…",
         "opcoes": ["o sentido da desigualdade inverte", "nada muda", "a inequação vira uma equação", "só o lado esquerdo muda de sinal"],
         "correta": 0,
         "x": "Exemplo: 2 &lt; 3, mas −2 &gt; −3. Esquecer de inverter é o erro mais comum com inequações."},
        {"k": "conceito", "pergunta": "Por que um classificador como a regressão logística é chamado de linear?",
         "opcoes": ["Porque a fronteira de decisão é uma reta (um hiperplano, em mais dimensões)", "Porque a saída é sempre uma reta", "Porque só aceita uma variável de entrada", "Porque só acerta dados em linha reta"],
         "correta": 0,
         "x": r"A probabilidade pode ser uma curva (sigmoide), mas a decisão depende só do sinal de $w \cdot x + b$, e isso divide o espaço por um hiperplano."},
    ],

    "Exponenciais e logaritmos na modelagem de IA": [
        conta("logprop"), conta("logeq"), conta("lse"), conta("expdecay"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            print(np.exp(0), np.log(1), np.log(np.e))
         '''),
         "opcoes": ["1.0 0.0 1.0", "0.0 1.0 0.0", "1.0 1.0 1.0", "2.718281828459045 0.0 1.0"],
         "correta": 0,
         "x": r"$e^0 = 1$, $\ln 1 = 0$ e $\ln e = 1$. No NumPy, <code>np.log</code> é o logaritmo natural (base e)."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            z = np.array([1000.0, 1000.0])
            print(np.exp(z).sum())
         '''),
         "opcoes": ["inf", "2000.0", "OverflowError", "1000.6931471805599"],
         "correta": 0,
         "x": r"$e^{1000}$ passa do maior número que um float guarda, e o NumPy devolve <code>inf</code> (com um aviso). É exatamente o problema que o truque do LogSumExp resolve."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            print(round(np.logaddexp(1000, 1000), 2))
         '''),
         "opcoes": ["1000.69", "2000.0", "inf", "1000.0"],
         "correta": 0,
         "x": r"<code>logaddexp</code> calcula $\ln(e^a + e^b)$ sem estourar: $1000 + \ln 2 \approx 1000{,}69$."},
        {"k": "conceito", "pergunta": "Por que se soma log-probabilidades em vez de multiplicar as probabilidades?",
         "opcoes": ["Multiplicar muitas probabilidades pequenas dá um número tão pequeno que o computador arredonda para zero; o log vira soma", "Porque somar é mais preciso que multiplicar em qualquer caso", "Porque o log deixa as probabilidades maiores que 1", "Porque probabilidades não podem ser multiplicadas"],
         "correta": 0,
         "x": r"Mil probabilidades de 0,01 multiplicadas dão $10^{-2000}$, que vira 0 no float. A soma dos logs é −4605: um número normal."},
        {"k": "conceito", "pergunta": r"Por que a função $e^z$ aparece na saída das redes (softmax)?",
         "opcoes": [r"Porque $e^z$ é sempre positivo, qualquer que seja z", r"Porque $e^z$ é sempre menor que 1", r"Porque $e^z$ é uma reta", "Porque deixa o cálculo mais lento e estável"],
         "correta": 0,
         "x": "Probabilidade não pode ser negativa. Passando os logits pela exponencial e dividindo pela soma, tudo fica positivo e soma 1."},
        {"k": "conceito", "tema": "Logaritmo de um produto", "pergunta": r"$\ln(a \cdot b)$ é igual a…",
         "opcoes": [r"$\ln a + \ln b$", r"$\ln a \cdot \ln b$", r"$\ln(a + b)$", r"$a \ln b$"],
         "correta": 0,
         "x": r"Log transforma produto em soma. Também: $\ln(a/b) = \ln a - \ln b$ e $\ln(a^k) = k \ln a$."},
    ],

    "Somatório, produtório e notação matemática em papers": [
        conta("soma"), conta("prod"), conta("argmax"), conta("indic"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            x = np.array([3, 1, 4, 1, 5])
            print(x.sum(), x.prod(), np.argmax(x))
         '''),
         "opcoes": ["14 60 4", "14 60 5", "14 12 4", "13 60 4"],
         "correta": 0,
         "x": "Soma 14, produto 3·1·4·1·5 = 60. O maior (5) está na posição 4, porque o NumPy conta do zero."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            y = np.array([0, 1, 1, 0])
            p = np.array([0, 1, 0, 0])
            print((y == p).mean())
         '''),
         "opcoes": ["0.75", "3", "0.25", "[ True  True False  True]"],
         "correta": 0,
         "x": r"<code>y == p</code> é a função indicadora, e <code>.mean()</code> faz o $\frac{1}{N}\sum$: 3 acertos em 4, acurácia 0.75."},
        {"k": "conceito", "tema": "Somatório no NumPy", "pergunta": r"$\sum_{i=1}^{n} x_i$ no NumPy é…",
         "opcoes": ["<code>x.sum()</code>", "<code>x.prod()</code>", "<code>len(x)</code>", "<code>x.max()</code>"],
         "correta": 0,
         "x": r"O somatório vira <code>sum</code>; o produtório ($\prod$), <code>prod</code>. Laços em papers quase sempre viram uma operação vetorizada."},
        {"k": "conceito", "tema": "Quantos termos tem um somatório", "pergunta": r"Quantos termos tem $\sum_{i=3}^{7} x_i$?",
         "opcoes": ["5", "4", "7", "10"],
         "correta": 0,
         "x": "i vale 3, 4, 5, 6 e 7: o início e o fim entram. São 7 − 3 + 1 = 5 termos."},
        {"k": "conceito", "tema": "Função indicadora quando o modelo erra", "pergunta": r"Quanto vale $\mathbb{I}[\hat y_i = y_i]$ quando o modelo erra o exemplo i?",
         "opcoes": ["0", "1", "−1", "O tamanho do erro"],
         "correta": 0,
         "x": "A função indicadora só vale 1 ou 0: 1 quando a condição é verdadeira (acertou) e 0 quando é falsa (errou)."},
        {"k": "conceito", "tema": "O que o argmin devolve", "pergunta": r"O que $\arg\min_w L(w)$ devolve?",
         "opcoes": ["O valor de w que deixa L o menor possível", "O menor valor de L", "A derivada de L", "O número de pesos"],
         "correta": 0,
         "x": r"$\min$ devolve o menor valor da função; $\arg\min$ devolve <b>onde</b> ele acontece. Treinar um modelo é procurar o $\arg\min$ da perda."},
    ],

    "Geometria analítica e distância Euclidiana vs Manhattan": [
        conta("dist2"), conta("manh"), conta("knn"), conta("l1"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            a = np.array([1, 2])
            b = np.array([4, 6])
            print(np.abs(a - b).sum(), np.linalg.norm(a - b), np.abs(a - b).max())
         '''),
         "opcoes": ["7 5.0 4", "5.0 7 4", "7 5.0 3", "-7 5.0 4"],
         "correta": 0,
         "x": "Diferenças de 3 e 4: Manhattan soma (7), a euclidiana é a hipotenusa (5.0) e a do máximo (L∞) pega a maior (4)."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            q = np.array([0, 0])
            pts = np.array([[3, 4], [1, 2], [5, 1]])
            d = np.linalg.norm(pts - q, axis=1)
            print(np.argmin(d))
         '''),
         "opcoes": ["1", "0", "2", "2.23606797749979"],
         "correta": 0,
         "x": "As distâncias são 5, 2,24 e 5,10. O mais perto é o ponto de índice 1. <code>argmin</code> devolve a posição, não a distância."},
        {"k": "conceito", "pergunta": "Qual distância sofre menos com um valor muito discrepante (outlier) numa coordenada?",
         "opcoes": ["Manhattan (L1), que soma as diferenças sem elevar ao quadrado", "Euclidiana (L2)", "As duas sofrem igual", "Nenhuma: distâncias ignoram outliers"],
         "correta": 0,
         "x": "Na euclidiana, uma diferença de 10 vira 100 dentro da raiz e domina a conta. Na Manhattan ela pesa só 10."},
        {"k": "conceito", "pergunta": "Em dimensões muito altas, as distâncias euclidianas entre pontos aleatórios tendem a…",
         "opcoes": ["ficar todas parecidas, o que atrapalha o k-NN", "ficar todas iguais a zero", "crescer sem limite e virar infinito", "ficar negativas"],
         "correta": 0,
         "x": "É a maldição da dimensionalidade: o vizinho mais perto e o mais longe ficam quase à mesma distância. Por isso o cosseno é tão usado em embeddings."},
        {"k": "conceito", "pergunta": "No k-NN com k = 3, como se classifica um ponto novo?",
         "opcoes": ["Pela classe mais comum entre os 3 vizinhos mais próximos", "Pela classe do ponto mais distante", "Pela média das 3 primeiras linhas da tabela", "Sorteando uma das 3 classes"],
         "correta": 0,
         "x": "O k-NN não treina nada: guarda os dados e, na hora de prever, vota entre os k vizinhos mais próximos."},
        {"k": "conceito", "pergunta": "Do ponto (0, 0) ao ponto (1, 1), quanto dão as distâncias euclidiana e Manhattan?",
         "opcoes": [r"$\sqrt{2} \approx 1{,}41$ e $2$", r"$2$ e $\sqrt{2}$", r"$1$ e $1$", r"$2$ e $2$"],
         "correta": 0,
         "x": "Pela diagonal, a reta direta mede √2. Andando pelos eixos (como num táxi), é 1 + 1 = 2."},
    ],
}
