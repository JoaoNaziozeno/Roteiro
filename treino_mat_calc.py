# -*- coding: utf-8 -*-
"""
Treino · Matemática, Módulo 3 do site (Cálculo Diferencial, Gradientes & Otimização).

Contas com números novos a cada vez (geradores em treino_contas_calc.py), saídas de código (o gabarito é o que o
Python imprime de verdade) e questões de conceito.
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
    "Limites e taxa de variação instantânea (ideia geral)": [
        conta("secante"), conta("derivlim"), conta("limfrac"), conta("diffnum"),
        {"k": "saida", "codigo": c('''
            f = lambda x: x ** 2
            for h in [1, 0.1, 0.01]:
                print(round((f(3 + h) - f(3)) / h, 2))
         '''),
         "opcoes": ["7.0\n6.1\n6.01", "6.0\n6.0\n6.0", "7.0\n6.1\n6.0", "7\n6\n6"],
         "correta": 0,
         "x": "A inclinação da secante é 6 + h: com h encolhendo, ela se aproxima de 6, que é a derivada de x² em x = 3 (2·3)."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            h = 1e-5
            print(round((np.sin(0 + h) - np.sin(0 - h)) / (2 * h), 4))
         '''),
         "opcoes": ["1.0", "0.0", "-1.0", "1e-05"],
         "correta": 0,
         "x": "A diferença central aproxima a derivada de sen x em 0, que é cos 0 = 1."},
        {"k": "conceito", "pergunta": "O que o limite da inclinação da secante, quando h → 0, representa?",
         "opcoes": ["A inclinação da reta tangente: a derivada naquele ponto", "O valor da função no ponto", "A área embaixo da curva", "A média da função"],
         "correta": 0,
         "x": "Com h cada vez menor, a secante encosta na curva num ponto só: vira a tangente, e sua inclinação é a derivada."},
        {"k": "conceito", "pergunta": "Ao conferir gradientes, por que se prefere a diferença central (f(x+h) − f(x−h)) / 2h?",
         "opcoes": ["Ela erra bem menos que a diferença para a frente, com o mesmo h", "Porque é a única que funciona com números negativos", "Porque dispensa calcular f", "Porque dá sempre um número inteiro"],
         "correta": 0,
         "x": "Os erros dos dois lados se cancelam: o erro cai com h² em vez de h. Com h = 0,001, isso é mil vezes mais preciso."},
        {"k": "conceito", "pergunta": "Se a derivada da perda em relação a um peso é positiva, o que fazer com o peso para a perda cair?",
         "opcoes": ["Diminuir o peso", "Aumentar o peso", "Deixar como está", "Trocar o sinal do peso"],
         "correta": 0,
         "x": "Derivada positiva quer dizer que aumentar o peso aumenta a perda. Então o caminho é o oposto: diminuir."},
        {"k": "conceito", "pergunta": "No computador, o que acontece com (f(x+h) − f(x)) / h se você usar h = 1e-20?",
         "opcoes": ["f(x+h) − f(x) vira 0 por arredondamento, e o resultado sai errado", "Dá a derivada exata", "O Python recusa números tão pequenos", "O resultado fica infinito"],
         "correta": 0,
         "x": "O float tem cerca de 16 dígitos: somar 1e-20 a um número normal não muda nada. Por isso se usa h em torno de 1e-5, nem grande nem pequeno demais."},
    ],

    "Derivadas fundamentais e regras básicas (potência, produto, soma)": [
        conta("dpoly"), conta("dpot"), conta("dprod"), conta("dmse"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            coef = [2, 0, 3, 1]        # 2x³ + 3x + 1
            d = np.polyder(coef)
            print(d, np.polyval(d, 2))
         '''),
         "opcoes": ["[6 0 3] 27", "[6 3] 27", "[2 0 3] 22", "[6 0 3] 54"],
         "correta": 0,
         "x": "A derivada de 2x³ + 3x + 1 é 6x² + 3 (coeficientes [6, 0, 3]). Em x = 2: 6·4 + 3 = 27."},
        {"k": "saida", "codigo": c('''
            def f(x):
                return x ** 3
            h = 0.001
            print(round((f(2 + h) - f(2)) / h))
         '''),
         "opcoes": ["12", "8", "6", "3"],
         "correta": 0,
         "x": "A inclinação numérica dá 12,006…, que arredonda para 12: a derivada de x³ é 3x², e em x = 2 vale 12."},
        {"k": "conceito", "pergunta": "Qual é a derivada de uma constante, como f(x) = 7?",
         "opcoes": ["0", "7", "1", "7x"],
         "correta": 0,
         "x": "Uma constante não muda quando x muda: a inclinação é zero."},
        {"k": "conceito", "tema": "Regra do produto", "pergunta": r"A regra do produto diz que $(u \cdot v)'$ é…",
         "opcoes": [r"$u' v + u v'$", r"$u' v'$", r"$u' v - u v'$", r"$u v'$"],
         "correta": 0,
         "x": "Pense num retângulo de lados u e v que cresce: a área ganha duas faixas, u'·v e u·v'."},
        {"k": "conceito", "tema": "Gradiente do erro quadrático", "pergunta": r"No erro quadrático $L = (\hat y - y)^2$, por que o gradiente é proporcional ao erro $(\hat y - y)$?",
         "opcoes": [r"Porque a derivada de $(\hat y - y)^2$ é $2(\hat y - y)$: errar mais dá um empurrão maior", "Porque o MSE ignora o sinal do erro", "Porque a derivada de um quadrado é sempre 2", "Porque o gradiente não depende do erro"],
         "correta": 0,
         "x": "Previsões muito erradas geram gradientes grandes e são corrigidas mais rápido. Previsões quase certas mexem pouco nos pesos."},
        {"k": "conceito", "pergunta": "A derivada da soma f + g é…",
         "opcoes": ["f' + g'", "f' · g'", "(f + g)²", "f' − g'"],
         "correta": 0,
         "x": "Derivar é linear: cada parcela se deriva separado. É por isso que a perda de um lote é a soma (ou média) das perdas de cada exemplo."},
    ],

    "Regra da Cadeia (Chain Rule) - o motor do Backpropagation": [
        conta("cadeia"), conta("cadeialn"), conta("cadeia3"), conta("passo1"),
        {"k": "saida", "codigo": c('''
            x, w, b, y = 2.0, 0.5, 1.0, 3.0
            z = w * x + b
            L = (z - y) ** 2
            dL_dz = 2 * (z - y)
            dL_dw = dL_dz * x
            print(z, L, dL_dw)
         '''),
         "opcoes": ["2.0 1.0 -4.0", "2.0 1.0 -2.0", "2.0 -1.0 -4.0", "2.0 1.0 4.0"],
         "correta": 0,
         "x": "Ida: z = 2,0 e L = (2 − 3)² = 1,0. Volta: dL/dz = 2·(−1) = −2 e, pela regra da cadeia, dL/dw = dL/dz · dz/dw = −2 · x = −4."},
        {"k": "saida", "codigo": c('''
            u = 3 * 1 + 1          # u = 3x + 1, em x = 1
            dy_du = 2 * u          # y = u²
            du_dx = 3
            print(dy_du * du_dx)
         '''),
         "opcoes": ["24", "8", "6", "16"],
         "correta": 0,
         "x": "u = 4, então dy/du = 8, e du/dx = 3. A regra da cadeia multiplica as taxas: 8 · 3 = 24."},
        {"k": "conceito", "pergunta": "No backpropagation, o que cada nó do grafo precisa saber calcular?",
         "opcoes": ["Só a própria derivada local; a regra da cadeia multiplica tudo no caminho de volta", "A derivada da rede inteira", "A perda final", "Nada: o otimizador calcula tudo de uma vez"],
         "correta": 0,
         "x": "Cada operação (soma, multiplicação, ativação) conhece só a sua derivada. Encadeando as derivadas locais, sai o gradiente de qualquer peso."},
        {"k": "conceito", "pergunta": "Qual é o erro mais comum ao aplicar a regra da cadeia?",
         "opcoes": ["Esquecer de multiplicar pela derivada de dentro", "Derivar a constante", "Usar parênteses demais", "Somar as derivadas"],
         "correta": 0,
         "x": "Em (3x + 1)², a derivada é 2(3x + 1) · 3. Sem o 3 (a derivada de dentro), a conta sai errada."},
        {"k": "conceito", "tema": "Regra da cadeia para f(g(x))", "pergunta": r"Para $y = f(g(x))$, quanto vale $\dfrac{dy}{dx}$?",
         "opcoes": [r"$f'(g(x)) \cdot g'(x)$", r"$f'(x) \cdot g'(x)$", r"$f'(g'(x))$", r"$f(g'(x))$"],
         "correta": 0,
         "x": "A derivada de fora é avaliada no valor de dentro, g(x), e multiplicada pela derivada de dentro."},
        {"k": "conceito", "pergunta": "Por que o backpropagation calcula de trás para a frente?",
         "opcoes": ["Porque as derivadas das camadas finais são reaproveitadas para calcular as das camadas anteriores", "Porque a perda fica na primeira camada", "Porque é mais fácil de programar ao contrário", "Não há motivo: a ordem não importa"],
         "correta": 0,
         "x": "Começando pela perda, cada camada recebe o gradiente pronto da camada seguinte e só multiplica pela sua derivada local. Assim nenhuma conta se repete."},
    ],

    "Derivadas de funções de ativação (Sigmoide, Tanh, ReLU, GeLU)": [
        conta("sigd"), conta("relud"), conta("tanhd"), conta("vanish"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            z = np.array([-2.0, 0.0, 3.0])
            print(np.maximum(0, z))
         '''),
         "opcoes": ["[0. 0. 3.]", "[-2.  0.  3.]", "[0 0 3]", "[2. 0. 3.]"],
         "correta": 0,
         "x": "A ReLU zera os negativos e mantém os positivos. Como z é float, a saída também é (3. em vez de 3)."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            s = 1 / (1 + np.exp(-0.0))
            print(s, s * (1 - s))
         '''),
         "opcoes": ["0.5 0.25", "0.0 0.0", "1.0 0.0", "0.5 0.5"],
         "correta": 0,
         "x": "Em z = 0 a sigmoide vale 0,5 e a derivada σ(1 − σ) chega no máximo: 0,25."},
        {"k": "conceito", "pergunta": "Por que as redes profundas trocaram a sigmoide pela ReLU nas camadas escondidas?",
         "opcoes": ["A derivada da ReLU é 1 nos positivos, então o gradiente não encolhe camada após camada", "Porque a ReLU é uma curva mais suave", "Porque a ReLU dá probabilidades", "Porque a sigmoide não tem derivada"],
         "correta": 0,
         "x": "Com a sigmoide, cada camada multiplica o gradiente por no máximo 0,25. Com a ReLU, os neurônios ativos passam o gradiente inteiro."},
        {"k": "conceito", "pergunta": "O que é a ReLU \"morta\" (dying ReLU)?",
         "opcoes": ["Um neurônio que só recebe z negativo: a derivada é 0 e ele para de aprender", "Uma ReLU que sempre devolve 1", "Uma ReLU com taxa de aprendizado zero", "Um erro de digitação no código"],
         "correta": 0,
         "x": "Se os pesos levam z para sempre abaixo de 0, a saída e o gradiente ficam em 0. Variantes como Leaky ReLU e GeLU deixam passar um pouco nos negativos."},
        {"k": "conceito", "pergunta": "Qual ativação é usada nos Transformers modernos, como os GPTs?",
         "opcoes": ["GeLU (ou variantes como SwiGLU)", "Degrau (0 ou 1)", "Só a sigmoide", "Nenhuma: Transformers não têm ativação"],
         "correta": 0,
         "x": "A GeLU parece uma ReLU suave: quase zero nos negativos, quase a identidade nos positivos, e com derivada sem quinas."},
        {"k": "conceito", "pergunta": "A saída da tanh fica entre…",
         "opcoes": ["−1 e 1", "0 e 1", "0 e infinito", "−infinito e infinito"],
         "correta": 0,
         "x": "A tanh é uma sigmoide esticada e centralizada no zero: tanh(z) = 2σ(2z) − 1."},
    ],

    "Derivadas parciais e o vetor Gradiente (nabla f)": [
        conta("parcial"), conta("parcial"), conta("grad"), conta("graddir"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            def L(w):
                return 2 * w[0] ** 2 + 3 * w[1] ** 2
            w = np.array([1.0, -1.0])
            h = 1e-5
            g = [(L(w + h * e) - L(w - h * e)) / (2 * h) for e in np.eye(2)]
            print(np.round(g, 3))
         '''),
         "opcoes": ["[ 4. -6.]", "[ 2. -3.]", "[4. 6.]", "[ 4. -6.  0.]"],
         "correta": 0,
         "x": "Mexendo um peso de cada vez (as linhas de <code>np.eye(2)</code>), sai cada derivada parcial: 4w₀ = 4 e 6w₁ = −6."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            g = np.array([3.0, 4.0])
            print(-g / np.linalg.norm(g))
         '''),
         "opcoes": ["[-0.6 -0.8]", "[0.6 0.8]", "[-3. -4.]", "[-0.8 -0.6]"],
         "correta": 0,
         "x": "−g aponta para a descida mais rápida; dividir pela norma (5) deixa só a direção, com tamanho 1."},
        {"k": "conceito", "tema": "O que é uma derivada parcial", "pergunta": r"O que é uma derivada parcial $\dfrac{\partial f}{\partial x}$?",
         "opcoes": ["A inclinação de f quando só x muda e as outras variáveis ficam congeladas", "A derivada de f em relação a todas as variáveis juntas", "Metade da derivada", "O valor de f no ponto x"],
         "correta": 0,
         "x": "Congela tudo e mexe numa variável só. Cada peso de uma rede tem a sua derivada parcial."},
        {"k": "conceito", "tema": "Para onde aponta o gradiente", "pergunta": r"Para onde aponta o gradiente $\nabla f$?",
         "opcoes": ["Para a direção de maior subida de f", "Para a direção de maior descida de f", "Sempre para a origem", "Para onde f é zero"],
         "correta": 0,
         "x": "Por isso a descida do gradiente anda no sentido contrário, −∇f."},
        {"k": "conceito", "pergunta": "Como o gradiente se relaciona com as curvas de nível de f?",
         "opcoes": ["É perpendicular a elas", "É paralelo a elas", "Fica sempre dentro da menor curva", "Não tem relação"],
         "correta": 0,
         "x": "Andando pela curva de nível, f não muda. A direção de maior mudança é a que cruza as curvas em ângulo reto."},
        {"k": "conceito", "pergunta": "Num modelo com 1 milhão de pesos, quantas componentes tem o gradiente da perda?",
         "opcoes": ["1 milhão: uma derivada parcial para cada peso", "Uma só", "Duas: x e y", "Depende do número de exemplos"],
         "correta": 0,
         "x": "O gradiente tem o mesmo formato dos parâmetros. O backpropagation calcula todas essas derivadas num único caminho de volta."},
    ],

    "Matriz Jacobiana e Matriz Hessiana (curvatura da loss)": [
        conta("hess"), conta("sela"), conta("jacob"), conta("sela"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            H = np.array([[2.0, 0.0], [0.0, -4.0]])
            print(np.linalg.eigvalsh(H))
         '''),
         "opcoes": ["[-4.  2.]", "[ 2. -4.]", "[2. 4.]", "[-2.  4.]"],
         "correta": 0,
         "x": "Para uma matriz simétrica, <code>eigvalsh</code> devolve os autovalores em ordem crescente: −4 e 2. Sinais opostos: ponto de sela."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            H = np.array([[2.0, 1.0], [1.0, 2.0]])
            vals = np.linalg.eigvalsh(H)
            print(vals, "mínimo" if (vals > 0).all() else "sela")
         '''),
         "opcoes": ["[1. 3.] mínimo", "[1. 3.] sela", "[2. 2.] mínimo", "[-1.  3.] sela"],
         "correta": 0,
         "x": "Os autovalores são 1 e 3, os dois positivos: a função curva para cima em todas as direções, então é um mínimo."},
        {"k": "conceito", "tema": "Formato da Jacobiana", "pergunta": r"A Jacobiana de uma função $F: \mathbb{R}^n \to \mathbb{R}^m$ tem formato…",
         "opcoes": ["m × n: uma linha por saída e uma coluna por entrada", "n × n", "m × m", "1 × n"],
         "correta": 0,
         "x": "Cada linha é o gradiente de uma das m saídas, com n derivadas parciais."},
        {"k": "conceito", "pergunta": "Por que métodos que usam a Hessiana não são usados em redes grandes?",
         "opcoes": ["A Hessiana tem n² entradas: com milhões de pesos, nem cabe na memória", "Porque a Hessiana não existe em redes neurais", "Porque são sempre mais lentos para convergir", "Porque só funcionam com uma variável"],
         "correta": 0,
         "x": "Com 1 bilhão de pesos, a Hessiana teria 10¹⁸ números. Otimizadores como o Adam usam só uma aproximação barata da curvatura, por coordenada."},
        {"k": "conceito", "pergunta": "Em alta dimensão, a maioria dos pontos críticos da perda (gradiente zero) são…",
         "opcoes": ["Pontos de sela", "Mínimos globais", "Máximos locais", "Mínimos locais ruins"],
         "correta": 0,
         "x": "Para ser mínimo, a curvatura precisa ser positiva em todas as direções. Com milhões delas, quase sempre alguma desce."},
        {"k": "conceito", "pergunta": "O que a Hessiana mede?",
         "opcoes": ["A curvatura da função: como a inclinação muda", "A inclinação da função", "O valor mínimo da função", "O número de variáveis"],
         "correta": 0,
         "x": "O gradiente diz para onde a função sobe; a Hessiana diz se essa subida acelera (curva para cima) ou freia (curva para baixo)."},
    ],

    "Algoritmo de Descida do Gradiente (Vanilla Gradient Descent)": [
        conta("gdpasso"), conta("gd2"), conta("gdlr"), conta("minibatch"),
        {"k": "saida", "codigo": c('''
            w, eta = 0.0, 0.2
            for passo in range(3):
                grad = 2 * (w - 3)
                w = w - eta * grad
            print(round(w, 3))
         '''),
         "opcoes": ["2.352", "3.0", "1.2", "-2.352"],
         "correta": 0,
         "x": "w vai de 0 para 1,2, depois 1,92 e 2,352: cada passo anda 40% do que falta até o mínimo (w = 3)."},
        {"k": "saida", "codigo": c('''
            w, eta = 1.0, 1.1
            for _ in range(4):
                w = w - eta * 2 * w      # L = w², gradiente 2w
            print(round(w, 4))
         '''),
         "opcoes": ["2.0736", "0.0", "-1.2", "1.0"],
         "correta": 0,
         "x": "Cada passo multiplica w por (1 − 2,2) = −1,2: o sinal troca e o tamanho cresce. Depois de 4 passos, (−1,2)⁴ = 2,0736. A taxa está grande demais e o treino diverge."},
        {"k": "conceito", "pergunta": "Por que o mini-batch é o padrão, em vez de usar todos os dados a cada passo?",
         "opcoes": ["Passos rápidos e paralelos na GPU, com um gradiente que já é uma boa estimativa", "Porque usar todos os dados dá um gradiente errado", "Porque o mini-batch sempre acha o mínimo global", "Porque dispensa a taxa de aprendizado"],
         "correta": 0,
         "x": "O gradiente de 64 ou 256 exemplos já aponta para perto da direção certa e custa muito menos que o do dataset inteiro."},
        {"k": "conceito", "pergunta": "Qual é o sintoma de uma taxa de aprendizado grande demais?",
         "opcoes": ["A perda oscila ou explode em vez de cair", "A perda cai devagar demais", "A perda fica exatamente zero", "O modelo para de usar memória"],
         "correta": 0,
         "x": "Os passos passam do mínimo e caem do outro lado, cada vez mais longe. É o primeiro ajuste a fazer quando a perda vira NaN."},
        {"k": "conceito", "pergunta": "Perto do mínimo, os passos ficam menores mesmo com a taxa η fixa. Por quê?",
         "opcoes": ["Porque o gradiente fica pequeno perto do mínimo", "Porque η diminui sozinho", "Porque o modelo fica cansado", "Porque a perda vira negativa"],
         "correta": 0,
         "x": "O passo é η vezes o gradiente. No fundo do vale a inclinação é quase zero, então o passo também é."},
        {"k": "conceito", "pergunta": "Qual é a regra de atualização da descida do gradiente?",
         "opcoes": [r"$w \leftarrow w - \eta \nabla L$", r"$w \leftarrow w + \eta \nabla L$", r"$w \leftarrow \eta \nabla L$", r"$w \leftarrow w - \nabla L / \eta$"],
         "correta": 0,
         "x": "Anda contra o gradiente (o sinal de menos), num passo do tamanho da taxa de aprendizado."},
    ],

    "Otimizadores modernos: Momentum, RMSprop e Adam": [
        conta("momentum"), conta("rmsprop"), conta("adambias"), conta("momentum"),
        {"k": "saida", "codigo": c('''
            v, beta = 0.0, 0.9
            for g in [1.0, 1.0, 1.0]:
                v = beta * v + (1 - beta) * g
            print(round(v, 3))
         '''),
         "opcoes": ["0.271", "1.0", "0.3", "2.71"],
         "correta": 0,
         "x": "v sobe devagar: 0,1, depois 0,19 e 0,271. Começando do zero, a média demora a chegar ao gradiente verdadeiro (1), e é isso que a correção de viés do Adam conserta."},
        {"k": "saida", "codigo": c('''
            m, b1, t = 0.0, 0.9, 1
            g = 5.0
            m = b1 * m + (1 - b1) * g
            print(round(m, 2), round(m / (1 - b1 ** t), 2))
         '''),
         "opcoes": ["0.5 5.0", "0.5 0.5", "4.5 45.0", "5.0 50.0"],
         "correta": 0,
         "x": "No 1º passo, m = 0,1 · 5 = 0,5, um décimo do gradiente. Dividindo por 1 − 0,9¹ = 0,1, a versão corrigida volta a 5,0."},
        {"k": "conceito", "pergunta": "O Momentum ajuda principalmente…",
         "opcoes": ["a atravessar ravinas sem zigue-zague e a acelerar em vales longos", "a calcular o gradiente exato", "a escolher o tamanho do lote", "a evitar a regra da cadeia"],
         "correta": 0,
         "x": "Como uma bola rolando: as oscilações de um lado para o outro se cancelam na média, e a direção que se repete ganha velocidade."},
        {"k": "conceito", "pergunta": "O que o RMSprop faz com cada coordenada do gradiente?",
         "opcoes": ["Divide o passo pela raiz da média dos gradientes ao quadrado daquela coordenada", "Soma 1 a cada coordenada", "Zera as coordenadas pequenas", "Ordena as coordenadas"],
         "correta": 0,
         "x": "Coordenadas com gradientes grandes andam com cuidado; as com gradientes pequenos ganham passos maiores. Cada peso tem a sua escala."},
        {"k": "conceito", "pergunta": "O Adam combina…",
         "opcoes": ["Momentum (1º momento) e RMSprop (2º momento), com correção de viés", "Descida do gradiente e k-NN", "Duas taxas de aprendizado fixas", "Momentum e dropout"],
         "correta": 0,
         "x": r"$m$ é a média dos gradientes (a direção) e $v$, a média dos quadrados (a escala). O passo é $\hat m / (\sqrt{\hat v} + \epsilon)$."},
        {"k": "conceito", "pergunta": "Por que o Adam precisa da correção de viés nos primeiros passos?",
         "opcoes": ["As médias começam em zero e ficam pequenas demais no início", "Porque o gradiente é sempre negativo no começo", "Porque a taxa de aprendizado começa em zero", "Não precisa: é só um detalhe estético"],
         "correta": 0,
         "x": r"Com $m_0 = 0$ e $\beta_1 = 0{,}9$, $m_1$ é só 10% do gradiente. Dividir por $1 - \beta_1^t$ compensa isso, e o efeito some com o tempo."},
    ],

    "Taxa de aprendizado (Learning Rate), convergência e pontos de sela": [
        conta("warmup"), conta("cosdecay"), conta("gdlr"), conta("sela"),
        {"k": "saida", "codigo": c('''
            import math
            eta_max, T = 0.01, 100
            for t in [0, 50, 100]:
                print(round(0.5 * eta_max * (1 + math.cos(math.pi * t / T)), 4))
         '''),
         "opcoes": ["0.01\n0.005\n0.0", "0.0\n0.005\n0.01", "0.01\n0.0\n0.01", "0.01\n0.0075\n0.0"],
         "correta": 0,
         "x": "O cosseno vai de 1 a −1: a taxa começa no máximo, passa pela metade no meio do treino e termina em zero."},
        {"k": "saida", "codigo": c('''
            eta_max, Tw = 0.003, 1000
            for t in [100, 500, 1000]:
                print(round(eta_max * t / Tw, 5))
         '''),
         "opcoes": ["0.0003\n0.0015\n0.003", "0.003\n0.003\n0.003", "0.03\n0.15\n0.3", "0.0003\n0.0015\n0.0015"],
         "correta": 0,
         "x": "No warmup, a taxa cresce em linha reta: 10%, 50% e 100% do máximo nos passos 100, 500 e 1000."},
        {"k": "conceito", "pergunta": "Para que serve o warmup no começo do treino de LLMs?",
         "opcoes": ["Evitar passos enormes enquanto os pesos e as médias do Adam ainda estão instáveis", "Aquecer a GPU antes do treino", "Aumentar a perda de propósito", "Escolher o tamanho do lote"],
         "correta": 0,
         "x": "No início, as estimativas do Adam são ruidosas e os pesos estão aleatórios. Começar com taxa baixa evita que o treino desande logo nos primeiros passos."},
        {"k": "conceito", "pergunta": "Em alta dimensão, por que mínimos locais ruins são raros?",
         "opcoes": ["Para ser mínimo, a curvatura precisa ser positiva em todas as direções; com tantas, quase sempre alguma desce (ponto de sela)", "Porque a perda é sempre uma parábola", "Porque o Adam pula todos eles", "Porque redes grandes não têm mínimos"],
         "correta": 0,
         "x": "É o argumento de Dauphin et al. (2014): o perigo real são os pontos de sela, onde o gradiente quase zera, e o ruído do mini-batch ajuda a escapar deles."},
        {"k": "conceito", "pergunta": "O que uma taxa de aprendizado pequena demais causa?",
         "opcoes": ["Treino muito lento, que pode parar antes de chegar perto do mínimo", "Divergência imediata", "Perda negativa", "Overfitting garantido"],
         "correta": 0,
         "x": "Cada passo anda quase nada. Com um número fixo de épocas, o modelo termina mal treinado."},
        {"k": "conceito", "pergunta": "O que o cosine decay faz com a taxa de aprendizado?",
         "opcoes": ["Faz a taxa cair suavemente do máximo até perto de zero, mais devagar no começo e no fim", "Faz a taxa subir sem parar", "Deixa a taxa constante", "Faz a taxa oscilar entre dois valores para sempre"],
         "correta": 0,
         "x": "Passos grandes enquanto há muito a aprender, e passos finos no fim para assentar no fundo do vale."},
    ],
}
