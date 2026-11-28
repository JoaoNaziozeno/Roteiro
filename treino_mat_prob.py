# -*- coding: utf-8 -*-
"""
Treino · Matemática, Módulo 4 do site (Probabilidade, Estatística & Teoria da Informação).

Contas com números novos a cada vez (geradores em treino_contas_prob.py), saídas de código (o gabarito é o que o
Python/NumPy imprime de verdade) e questões de conceito.
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
    "Variáveis aleatórias discretas e contínuas": [
        conta("pmffalta"), conta("pmfcum"), conta("unifarea"), conta("pmfcum"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            p = np.array([0.1, 0.2, 0.3, 0.4])
            print(round(p.sum(), 2), round(p[1:].sum(), 2))
         '''),
         "opcoes": ["1.0 0.9", "1.0 0.1", "0.9 1.0", "4 3"],
         "correta": 0,
         "x": "Uma PMF soma 1. <code>p[1:]</code> pega P(X = 2), P(X = 3) e P(X = 4), que somam 0.9: é o mesmo que 1 − P(X = 1)."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            x = np.random.default_rng(0).uniform(0, 10, size=100_000)
            print(round(((x >= 2) & (x <= 5)).mean(), 1))
         '''),
         "opcoes": ["0.3", "3.0", "0.1", "0.5"],
         "correta": 0,
         "x": "Sorteando 100 mil valores uniformes entre 0 e 10, cerca de 30% caem entre 2 e 5: a área (5 − 2) · (1/10)."},
        {"k": "conceito", "pergunta": "Numa variável contínua, quanto vale P(X = 2), exatamente?",
         "opcoes": ["0: a probabilidade é uma área, e um ponto não tem área", "A altura da densidade em 2", "1, se 2 estiver no intervalo", "Não dá para saber"],
         "correta": 0,
         "x": "No contínuo, só intervalos têm probabilidade. Por isso se fala em P(1,9 &lt; X &lt; 2,1), e não em P(X = 2)."},
        {"k": "conceito", "pergunta": "Qual é a diferença entre PMF e PDF?",
         "opcoes": ["A PMF dá a probabilidade de cada valor (discreta); a PDF dá uma densidade, e a probabilidade vem da área (contínua)", "Nenhuma: são nomes diferentes da mesma coisa", "A PMF é para dados de texto e a PDF para imagens", "A PDF sempre vale no máximo 1"],
         "correta": 0,
         "x": "Discreto: soma das probabilidades = 1. Contínuo: área total embaixo da densidade = 1."},
        {"k": "conceito", "pergunta": "Uma densidade (PDF) pode passar de 1?",
         "opcoes": ["Sim: o que precisa dar 1 é a área total, não a altura", "Não, nunca", "Só se a variável for discreta", "Só em distribuições normais"],
         "correta": 0,
         "x": "Uma uniforme entre 0 e 0,5 tem densidade 2 em todo o intervalo: altura 2 vezes largura 0,5 dá área 1."},
        {"k": "conceito", "pergunta": "Qual destas é uma variável aleatória discreta?",
         "opcoes": ["O número de cliques num anúncio por dia", "A altura de uma pessoa", "O tempo até um servidor responder", "A temperatura de uma GPU"],
         "correta": 0,
         "x": "Contagens (0, 1, 2, …) são discretas. Medidas como altura, tempo e temperatura podem assumir qualquer valor num intervalo: são contínuas."},
    ],

    "Média, mediana, variância e desvio padrão": [
        conta("media"), conta("mediana"), conta("variancia"), conta("zscore"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            x = np.array([2, 4, 4, 4, 5, 5, 7, 9])
            print(x.mean(), np.median(x), x.std())
         '''),
         "opcoes": ["5.0 4.5 2.0", "5.0 4.0 2.0", "5.0 4.5 4.0", "5.0 4.5 2.138089935299395"],
         "correta": 0,
         "x": "Média 40/8 = 5. Mediana: média dos dois do meio (4 e 5) = 4.5. O <code>std()</code> do NumPy divide por n (populacional): 2.0. Com <code>ddof=1</code> daria 2.138."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            x = np.array([1.0, 2.0, 3.0, 100.0])
            print(x.mean(), np.median(x))
         '''),
         "opcoes": ["26.5 2.5", "2.5 26.5", "26.5 26.5", "2.5 2.5"],
         "correta": 0,
         "x": "Um único valor extremo (100) puxa a média para 26.5, enquanto a mediana continua no meio dos dados: 2.5."},
        {"k": "conceito", "pergunta": "Qual medida resiste melhor a um valor extremo?",
         "opcoes": ["A mediana", "A média", "A variância", "O desvio padrão"],
         "correta": 0,
         "x": "A mediana só olha a posição do meio. Trocar o maior valor por um número gigante não a muda."},
        {"k": "conceito", "pergunta": "Por que a variância amostral divide por n − 1 (correção de Bessel)?",
         "opcoes": ["A média da amostra fica mais perto dos dados que a média real, e dividir por n subestimaria a variância", "Para o resultado ficar inteiro", "Porque um dos dados é sempre descartado", "Não há motivo: é só convenção"],
         "correta": 0,
         "x": "Os desvios são medidos em relação à média da própria amostra, que já foi \"ajustada\" aos dados. Dividir por n − 1 compensa isso."},
        {"k": "conceito", "pergunta": "O que a LayerNorm faz com cada vetor de um Transformer?",
         "opcoes": ["Subtrai a média e divide pelo desvio padrão do próprio vetor, e depois aplica escala e deslocamento aprendidos", "Arredonda os valores para inteiros", "Ordena as coordenadas", "Soma 1 a todas as coordenadas"],
         "correta": 0,
         "x": "É um escore z coordenada por coordenada, dentro de cada vetor. Mantém as ativações numa escala estável ao longo das camadas."},
        {"k": "conceito", "pergunta": "Qual é a relação entre desvio padrão e variância?",
         "opcoes": ["O desvio padrão é a raiz da variância e fica na mesma unidade dos dados", "A variância é a raiz do desvio padrão", "São a mesma coisa", "O desvio padrão é a variância dividida por n"],
         "correta": 0,
         "x": "Se os dados estão em reais, a variância está em reais² e o desvio padrão volta a reais. Por isso ele é mais fácil de interpretar."},
    ],

    "Esperança matemática, covariância e correlação": [
        conta("esper"), conta("esperjogo"), conta("cov"), conta("corrsinal"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            x = np.array([1, 2, 3, 4])
            y = np.array([2, 4, 6, 8])
            print(round(np.corrcoef(x, y)[0, 1], 3), np.cov(x, y, bias=True)[0, 1])
         '''),
         "opcoes": ["1.0 2.5", "2.0 2.5", "1.0 3.3333333333333335", "1.0 1.0"],
         "correta": 0,
         "x": "y = 2x: relação linear perfeita, correlação 1. A covariância populacional (<code>bias=True</code>) é 2.5; com n − 1, seria 3.33."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            valores = np.array([0, 10, 100])
            probs = np.array([0.5, 0.4, 0.1])
            print(valores @ probs)
         '''),
         "opcoes": ["14.0", "36.666666666666664", "1.0", "110"],
         "correta": 0,
         "x": "A esperança é o produto escalar de valores e probabilidades: 0·0,5 + 10·0,4 + 100·0,1 = 14. A média simples dos valores (36,7) ignora as probabilidades."},
        {"k": "conceito", "pergunta": "Correlação zero quer dizer que as variáveis são independentes?",
         "opcoes": ["Não: só que não há relação linear; pode haver uma relação curva", "Sim, sempre", "Sim, se houver muitos dados", "Não: quer dizer que uma é o dobro da outra"],
         "correta": 0,
         "x": "Em y = x², com x simétrico em torno de zero, a correlação é 0, mas y depende totalmente de x."},
        {"k": "conceito", "pergunta": "A correlação de Pearson entre dois vetores centralizados (média subtraída) é…",
         "opcoes": ["o cosseno do ângulo entre eles", "o produto escalar deles", "a distância euclidiana entre eles", "a soma deles"],
         "correta": 0,
         "x": r"$r = \dfrac{\sum (x - \bar x)(y - \bar y)}{\lVert x - \bar x \rVert\,\lVert y - \bar y \rVert}$: exatamente a fórmula do cosseno. Por isso fica entre −1 e 1."},
        {"k": "conceito", "pergunta": "Covariância positiva significa que…",
         "opcoes": ["quando x está acima da média, y tende a estar acima também", "x é sempre maior que y", "as variáveis são independentes", "y é o dobro de x"],
         "correta": 0,
         "x": "Os desvios andam juntos: produtos (x − x̄)(y − ȳ) positivos predominam."},
        {"k": "conceito", "pergunta": "Por que se usa a correlação, e não a covariância, para comparar a força de relações?",
         "opcoes": ["A correlação não depende das unidades: fica sempre entre −1 e 1", "A covariância é sempre zero", "A correlação é mais fácil de calcular", "A covariância só serve para dados discretos"],
         "correta": 0,
         "x": "Medir altura em centímetros em vez de metros multiplica a covariância por 100. A correlação não muda."},
    ],

    "Probabilidade condicional e Teorema de Bayes": [
        conta("bayes"), conta("condtab"), conta("odds"), conta("pelomenos"),
        {"k": "saida", "codigo": c('''
            prev, sens, fp = 0.01, 0.9, 0.05
            pos = sens * prev + fp * (1 - prev)
            print(round(sens * prev / pos, 3))
         '''),
         "opcoes": ["0.154", "0.9", "0.009", "0.95"],
         "correta": 0,
         "x": "P(+) junta os verdadeiros positivos (0,009) e os falsos (0,0495). Só 15,4% dos positivos estão doentes, mesmo com um teste que acerta 90% dos doentes."},
        {"k": "saida", "codigo": c('''
            emails = ["spam+", "spam+", "normal+", "normal+", "spam", "normal", "normal", "normal"]
            com = [e for e in emails if e.endswith("+")]
            print(sum(e.startswith("spam") for e in com) / len(com))
         '''),
         "opcoes": ["0.5", "0.6666666666666666", "0.25", "0.375"],
         "correta": 0,
         "x": "O \"+\" marca os e-mails com a palavra. Entre os 4 com a palavra, 2 são spam: P(spam | palavra) = 0.5. P(palavra | spam) seria 2/3, outra pergunta."},
        {"k": "conceito", "pergunta": "P(A | B) e P(B | A) são iguais?",
         "opcoes": ["Em geral não: a barra muda o grupo que se olha", "Sim, sempre", "Só quando A e B são independentes", "Sim, se forem probabilidades altas"],
         "correta": 0,
         "x": "P(tosse | gripe) é alta; P(gripe | tosse) é bem menor, porque muita coisa dá tosse. Trocar as duas é a confusão mais cara da estatística."},
        {"k": "conceito", "pergunta": "No classificador Naive Bayes, o \"ingênuo\" é supor que…",
         "opcoes": ["as palavras são independentes entre si, dada a classe", "todas as classes têm a mesma probabilidade", "o modelo não precisa de dados", "as palavras não importam"],
         "correta": 0,
         "x": "Com essa suposição, P(palavras | spam) vira um produto de probabilidades simples. Quase nunca é verdade, mas funciona bem na prática."},
        {"k": "conceito", "pergunta": "Um teste com 99% de acerto deu positivo para uma doença rara (1 em 10 mil). O mais provável é que…",
         "opcoes": ["seja um falso positivo: há muito mais saudáveis testados do que doentes", "a pessoa esteja doente, com 99% de chance", "o teste esteja quebrado", "a chance seja de 50%"],
         "correta": 0,
         "x": "Em 10 mil pessoas, 1 doente dá positivo, mas cerca de 100 saudáveis também (1%). Entre os positivos, menos de 1% está doente."},
        {"k": "conceito", "pergunta": "Qual é a fórmula de Bayes?",
         "opcoes": [r"$P(H \mid E) = \dfrac{P(E \mid H)\,P(H)}{P(E)}$", r"$P(H \mid E) = P(E \mid H)$", r"$P(H \mid E) = P(H) + P(E)$", r"$P(H \mid E) = \dfrac{P(H)}{P(E \mid H)}$"],
         "correta": 0,
         "x": "Posterior = verossimilhança × prior ÷ evidência. Na dúvida, troque porcentagens por contagens de pessoas."},
    ],

    "Distribuição Normal (Gaussiana) e probabilidade vs verossimilhança": [
        conta("regra689"), conta("normtail"), conta("bernoulliL"), conta("zscore"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            x = np.random.default_rng(1).normal(100, 15, size=200_000)
            print(round(np.mean(np.abs(x - 100) < 15), 2))
         '''),
         "opcoes": ["0.68", "0.95", "0.5", "0.34"],
         "correta": 0,
         "x": "Simulando 200 mil valores de uma normal (média 100, desvio 15), cerca de 68% ficam a menos de 1 desvio da média, como diz a regra."},
        {"k": "saida", "codigo": c('''
            def L(p, caras, n):
                return p ** caras * (1 - p) ** (n - caras)
            print(round(L(0.5, 7, 10), 4), round(L(0.7, 7, 10), 4))
         '''),
         "opcoes": ["0.001 0.0022", "0.0022 0.001", "0.5 0.7", "0.7 0.7"],
         "correta": 0,
         "x": "Com 7 caras em 10, a moeda com p = 0,7 explica os dados mais de duas vezes melhor que a honesta: maior verossimilhança."},
        {"k": "conceito", "pergunta": "Qual é a diferença entre probabilidade e verossimilhança?",
         "opcoes": ["A probabilidade fixa os parâmetros e pergunta pelos dados; a verossimilhança fixa os dados e compara parâmetros", "São a mesma coisa", "A verossimilhança é sempre maior", "A probabilidade só existe para dados contínuos"],
         "correta": 0,
         "x": "\"Com moeda honesta, qual a chance de 7 caras?\" é probabilidade. \"Vi 7 caras: qual p explica melhor?\" é verossimilhança."},
        {"k": "conceito", "pergunta": "Numa distribuição normal, a média, a mediana e a moda…",
         "opcoes": ["são iguais, porque a curva é simétrica", "são sempre diferentes", "dependem do desvio padrão", "não existem"],
         "correta": 0,
         "x": "O pico (moda), o ponto que divide a área ao meio (mediana) e o centro de massa (média) coincidem."},
        {"k": "conceito", "pergunta": "Numa normal, um valor com z = 4 é…",
         "opcoes": ["muito raro (bem menos de 0,1% dos casos): bom candidato a anomalia", "comum", "exatamente a média", "impossível"],
         "correta": 0,
         "x": "Além de 3 desvios já sobram só 0,3%. Com z = 4, são cerca de 6 em 100 mil: vale investigar."},
        {"k": "conceito", "pergunta": "A verossimilhança, somada (ou integrada) sobre todos os valores do parâmetro, dá 1?",
         "opcoes": ["Não necessariamente: ela não é uma distribuição sobre o parâmetro", "Sim, sempre", "Só para a normal", "Só se o parâmetro for inteiro"],
         "correta": 0,
         "x": "Ela é uma função do parâmetro para dados fixos. Só serve para comparar valores do parâmetro entre si."},
    ],

    "Teorema do Limite Central e amostragem": [
        conta("erropadrao"), conta("amostra4x"), conta("erropadrao"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            rng = np.random.default_rng(0)
            medias = rng.uniform(0, 1, size=(10_000, 100)).mean(axis=1)
            print(round(medias.mean(), 2), round(medias.std(), 3))
         '''),
         "opcoes": ["0.5 0.029", "0.5 0.289", "0.5 0.0", "1.0 0.029"],
         "correta": 0,
         "x": "Cada média de 100 uniformes fica perto de 0,5, com desvio 0,289/√100 ≈ 0,029. É o erro padrão da média, como o TLC prevê."},
        {"k": "saida", "codigo": c('''
            import math
            sigma = 10
            for n in [4, 16, 64]:
                print(sigma / math.sqrt(n))
         '''),
         "opcoes": ["5.0\n2.5\n1.25", "2.5\n0.625\n0.15625", "5.0\n4.0\n3.0", "20.0\n40.0\n80.0"],
         "correta": 0,
         "x": "Cada vez que n fica 4 vezes maior, o erro padrão cai pela metade."},
        {"k": "conceito", "pergunta": "O que o Teorema do Limite Central garante?",
         "opcoes": ["A média de muitas amostras independentes segue, aproximadamente, uma normal, mesmo que os dados não sejam normais", "Todos os dados do mundo são normais", "A média da amostra é sempre igual à média real", "Amostras grandes não têm erro"],
         "correta": 0,
         "x": "Por isso a normal aparece em todo lugar: qualquer soma ou média de muitos efeitos pequenos e independentes tende a ela."},
        {"k": "conceito", "pergunta": "Por que o gradiente de um mini-batch funciona?",
         "opcoes": ["É uma média de gradientes: pelo TLC, fica em torno do gradiente verdadeiro, com erro que cai com a raiz do tamanho do lote", "Porque é sempre igual ao gradiente verdadeiro", "Porque usa só o exemplo mais difícil", "Não funciona: é só um truque para economizar memória"],
         "correta": 0,
         "x": "Um lote 4 vezes maior deixa a estimativa só 2 vezes mais precisa. Por isso lotes médios costumam ser o melhor custo-benefício."},
        {"k": "conceito", "pergunta": "Dobrar o tamanho da amostra divide o erro padrão por…",
         "opcoes": [r"$\sqrt{2} \approx 1{,}41$", "2", "4", "nada: o erro não muda"],
         "correta": 0,
         "x": r"O erro padrão é $\sigma/\sqrt{n}$: dobrar n multiplica $\sqrt{n}$ por $\sqrt 2$."},
        {"k": "conceito", "pergunta": "Uma pesquisa ouviu só quem reclamou no suporte. Uma amostra enorme assim corrige o problema?",
         "opcoes": ["Não: o TLC trata da variação aleatória, não do viés de quem foi escolhido", "Sim, com amostra grande o viés some", "Sim, se a amostra passar de 1.000 pessoas", "Depende do desvio padrão"],
         "correta": 0,
         "x": "Mais dados enviesados dão uma estimativa precisa da coisa errada. A amostra precisa ser representativa."},
        {"k": "conceito", "pergunta": "O que o erro padrão da média mede?",
         "opcoes": ["Quanto a média da amostra varia de uma amostra para outra", "Quanto cada dado varia em torno da média", "O erro do instrumento de medida", "A diferença entre a média e a mediana"],
         "correta": 0,
         "x": "O desvio padrão descreve os dados; o erro padrão descreve a incerteza sobre a média calculada com eles."},
    ],

    "Intervalos de confiança e teste de hipóteses (noção)": [
        conta("ic95"), conta("pvalor"), conta("zteste"), conta("ic95"),
        {"k": "saida", "codigo": c('''
            import math
            xbar, s, n = 50, 10, 100
            m = 1.96 * s / math.sqrt(n)
            print(round(xbar - m, 2), round(xbar + m, 2))
         '''),
         "opcoes": ["48.04 51.96", "30.4 69.6", "49.0 51.0", "48.04 50.0"],
         "correta": 0,
         "x": "Erro padrão 10/√100 = 1, margem 1,96 · 1 = 1,96: o intervalo vai de 48,04 a 51,96."},
        {"k": "saida", "codigo": c('''
            alfa, testes = 0.05, 20
            print(round(1 - (1 - alfa) ** testes, 2))
         '''),
         "opcoes": ["0.64", "0.05", "1.0", "0.95"],
         "correta": 0,
         "x": "Com 20 testes, mesmo sem efeito nenhum, a chance de pelo menos um falso positivo é de 64%. Por isso se corrige o α quando há muitos testes."},
        {"k": "conceito", "pergunta": "O que é o p-valor?",
         "opcoes": ["A chance de ver dados tão extremos quanto os observados, se H₀ fosse verdadeira", "A chance de H₀ ser verdadeira", "A chance de o efeito ser grande", "A porcentagem de dados que ficou fora do intervalo"],
         "correta": 0,
         "x": "Ele mede o quanto os dados surpreendem quem acredita em H₀. Não diz a probabilidade de H₀ nem o tamanho do efeito."},
        {"k": "conceito", "pergunta": "O que significa um intervalo de confiança de 95%?",
         "opcoes": ["Se o estudo fosse repetido muitas vezes, 95% dos intervalos calculados conteriam o valor real", "Há 95% de chance de o valor real estar neste intervalo específico", "95% dos dados estão dentro do intervalo", "O modelo acerta 95% das vezes"],
         "correta": 0,
         "x": "O \"95%\" é uma propriedade do método. Cada intervalo, depois de calculado, contém ou não o valor real."},
        {"k": "conceito", "pergunta": "Com uma amostra gigante, quase qualquer diferença minúscula vira \"significativa\". O que mais olhar?",
         "opcoes": ["O tamanho do efeito: se a diferença importa na prática", "Só o p-valor", "O número de casas decimais", "Nada: significativo quer dizer importante"],
         "correta": 0,
         "x": "Melhorar a acurácia em 0,01 ponto pode ser \"significativo\" com 10 milhões de exemplos e mesmo assim não valer a troca de modelo."},
        {"k": "conceito", "pergunta": "Fazer 20 testes com α = 5% e mostrar só o que deu significativo é um problema porque…",
         "opcoes": ["aumenta muito a chance de falso positivo (p-hacking)", "20 testes é pouco", "o α deveria ser 50%", "não é problema nenhum"],
         "correta": 0,
         "x": "Sem efeito nenhum, cerca de 1 em cada 20 testes dá significativo por acaso. Escolher só esse é enganar a si mesmo."},
    ],

    "Máxima Verossimilhança (Maximum Likelihood Estimation - MLE)": [
        conta("mlebern"), conta("nll"), conta("mlemu"), conta("bernoulliL"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            ps = np.linspace(0.1, 0.9, 9)
            L = ps ** 7 * (1 - ps) ** 3
            print(round(ps[np.argmax(L)], 1))
         '''),
         "opcoes": ["0.7", "0.5", "0.3", "7"],
         "correta": 0,
         "x": "Testando p de 0,1 a 0,9, a verossimilhança de 7 caras em 10 é máxima em p = 0,7: a proporção observada."},
        {"k": "saida", "codigo": c('''
            import math
            probs = [0.9, 0.5, 0.25]
            print(round(-sum(math.log(p) for p in probs), 3))
         '''),
         "opcoes": ["2.185", "-2.185", "0.1125", "1.65"],
         "correta": 0,
         "x": "NLL = −(ln 0,9 + ln 0,5 + ln 0,25) = 0,105 + 0,693 + 1,386 ≈ 2,185. O exemplo com probabilidade 0,25 é o que mais pesa."},
        {"k": "conceito", "pergunta": "Por que maximizar o log da verossimilhança dá o mesmo resultado que maximizar a verossimilhança?",
         "opcoes": ["Porque o log é crescente: não muda onde fica o máximo", "Porque o log é sempre positivo", "Porque o log de 1 é 0", "Não dá o mesmo resultado"],
         "correta": 0,
         "x": "Se L(a) &gt; L(b), então log L(a) &gt; log L(b). O ponto de máximo é o mesmo, e as contas ficam bem mais fáceis."},
        {"k": "conceito", "pergunta": "Minimizar a NLL de um classificador é o mesmo que minimizar…",
         "opcoes": ["a entropia cruzada", "o erro absoluto", "a acurácia", "o número de parâmetros"],
         "correta": 0,
         "x": "Com rótulos one-hot, −log p(classe certa) é exatamente a entropia cruzada de cada exemplo."},
        {"k": "conceito", "pergunta": "Qual é a estimativa de máxima verossimilhança da média de uma normal?",
         "opcoes": ["A média amostral", "A mediana", "O maior valor", "A moda"],
         "correta": 0,
         "x": "Maximizar a verossimilhança da normal é minimizar a soma dos quadrados dos desvios, e quem faz isso é a média. Por isso o MSE combina com ruído gaussiano."},
        {"k": "conceito", "pergunta": "Por que se usa a log-verossimilhança no computador?",
         "opcoes": ["O produto de milhares de probabilidades vira zero (underflow); a soma dos logs, não", "Porque o computador não sabe multiplicar", "Para deixar os números positivos", "Para acelerar a GPU"],
         "correta": 0,
         "x": r"0,5 multiplicado mil vezes dá $10^{-301}$, perto do limite do float. A soma dos logs é só −693."},
    ],

    "Trade-off Viés vs. Variância (Bias-Variance Dilemma)": [
        conta("biasvar"), conta("diagfit"), conta("diagfit"),
        {"k": "saida", "codigo": c('''
            vies, var, ruido = 0.5, 0.2, 0.1
            print(round(vies ** 2 + var + ruido, 2))
         '''),
         "opcoes": ["0.55", "0.8", "0.45", "0.3"],
         "correta": 0,
         "x": "Erro esperado = viés² + variância + ruído = 0,25 + 0,2 + 0,1 = 0,55. O viés entra ao quadrado."},
        {"k": "saida", "codigo": c('''
            w, eta, lam = 10.0, 0.1, 0.5
            for _ in range(3):
                w = w - eta * lam * w     # só o termo de weight decay
            print(round(w, 3))
         '''),
         "opcoes": ["8.574", "8.5", "10.0", "9.5"],
         "correta": 0,
         "x": "Cada passo multiplica w por 1 − 0,1 · 0,5 = 0,95. Depois de 3 passos, 10 · 0,95³ ≈ 8,574: o weight decay encolhe os pesos aos poucos."},
        {"k": "conceito", "pergunta": "Underfitting é sinal de…",
         "opcoes": ["viés alto: o modelo é simples demais para o padrão dos dados", "variância alta", "dados demais", "taxa de aprendizado perfeita"],
         "correta": 0,
         "x": "Erra muito até nos dados de treino. Mais capacidade (modelo maior, mais atributos) costuma ajudar."},
        {"k": "conceito", "pergunta": "Qual destas técnicas ajuda contra overfitting?",
         "opcoes": ["Weight decay, dropout, mais dados ou early stopping", "Treinar por mais épocas", "Tirar a validação", "Aumentar o modelo"],
         "correta": 0,
         "x": "Todas reduzem a variância: limitam o tamanho dos pesos, sorteiam neurônios, dão mais exemplos ou param antes de decorar."},
        {"k": "conceito", "pergunta": "Aumentar a complexidade do modelo costuma…",
         "opcoes": ["diminuir o viés e aumentar a variância", "aumentar os dois", "diminuir os dois", "não mexer em nada"],
         "correta": 0,
         "x": "É o dilema: um modelo flexível se ajusta melhor ao padrão, mas também ao ruído."},
        {"k": "conceito", "pergunta": "O que é o ruído irredutível?",
         "opcoes": ["Um erro que não some com modelo nenhum: vem dos próprios dados", "O erro de arredondamento do computador", "O viés do modelo", "O erro que some com mais épocas"],
         "correta": 0,
         "x": "Rótulos errados, informação que falta nas entradas: nem o modelo perfeito acerta isso."},
        {"k": "conceito", "pergunta": "O que é early stopping?",
         "opcoes": ["Parar o treino quando o erro de validação para de cair", "Parar quando o erro de treino chega a zero", "Treinar uma época só", "Desligar o computador no meio"],
         "correta": 0,
         "x": "O erro de treino continua caindo, mas o de validação começa a subir quando o modelo passa a decorar. É a hora de parar."},
    ],

    "Estatística para comparar modelos (teste A/B, bootstrap e tamanho de amostra)": [
        conta("amostrasn"), conta("icdiff"), conta("acuraciase"), conta("icdiff"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            rng = np.random.default_rng(0)
            acertos = np.array([1, 0, 1, 1, 0, 1, 1, 1, 0, 1])
            amostras = [rng.choice(acertos, size=10).mean() for _ in range(5)]
            print(len(amostras), acertos.mean())
         '''),
         "opcoes": ["5 0.7", "10 0.7", "5 7", "5 0.5"],
         "correta": 0,
         "x": "O bootstrap sorteia, com reposição, conjuntos do mesmo tamanho (aqui 5 sorteios). A acurácia original é 7/10 = 0.7; a variação das acurácias sorteadas dá o intervalo de confiança."},
        {"k": "saida", "codigo": c('''
            p, d = 0.8, 0.05
            print(round(16 * p * (1 - p) / d ** 2))
         '''),
         "opcoes": ["1024", "51", "5120", "6400"],
         "correta": 0,
         "x": "16 · 0,8 · 0,2 / 0,05² = 2,56 / 0,0025 = 1024 perguntas para detectar 5 pontos de diferença perto de 80%."},
        {"k": "conceito", "pergunta": "O modelo B acertou 81% e o A, 80%, em 100 perguntas. Dá para dizer que B é melhor?",
         "opcoes": ["Não: com 100 perguntas a margem de erro é de uns ±8 pontos; 1 ponto pode ser acaso", "Sim, 81 é maior que 80", "Sim, se o B for mais novo", "Só se o B for mais rápido"],
         "correta": 0,
         "x": "Com amostras pequenas, a acurácia oscila bastante só pelo sorteio das perguntas. É preciso um intervalo de confiança para a diferença."},
        {"k": "conceito", "pergunta": "No bootstrap pareado para comparar dois modelos…",
         "opcoes": ["sorteiam-se as mesmas perguntas, com reposição, para os dois modelos, e olha-se a diferença", "cada modelo sorteia perguntas diferentes", "treina-se os modelos de novo", "usa-se só a primeira metade das perguntas"],
         "correta": 0,
         "x": "Repetindo o sorteio milhares de vezes, sai a distribuição da diferença. Se o intervalo de 95% não contém o zero, a diferença é real."},
        {"k": "conceito", "pergunta": "Por que comparar os modelos nas mesmas perguntas (de forma pareada)?",
         "opcoes": ["A dificuldade das perguntas afeta os dois igual, e a diferença fica mais precisa", "Porque é mais rápido de digitar", "Porque perguntas diferentes dão empate", "Não há motivo"],
         "correta": 0,
         "x": "Uma pergunta difícil derruba os dois modelos. Olhando a diferença pergunta a pergunta, essa variação some."},
        {"k": "conceito", "pergunta": "Para detectar uma diferença 2 vezes menor, a amostra precisa ficar…",
         "opcoes": ["4 vezes maior", "2 vezes maior", "igual", "8 vezes maior"],
         "correta": 0,
         "x": "O número de amostras cresce com 1/d²: metade da diferença pede o quádruplo de perguntas."},
    ],

    "Entropia de Shannon (medida de incerteza da informação)": [
        conta("entropia"), conta("surpresa"), conta("entmax"), conta("entropia"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            p = np.array([0.5, 0.25, 0.25])
            print(-(p * np.log2(p)).sum())
         '''),
         "opcoes": ["1.5", "-1.5", "1.0397207708399179", "3"],
         "correta": 0,
         "x": "0,5 · 1 + 0,25 · 2 + 0,25 · 2 = 1,5 bits. Com log natural sairia 1,04 (em nats)."},
        {"k": "saida", "codigo": c('''
            import math
            print(math.log2(1 / (1 / 1024)))
         '''),
         "opcoes": ["10.0", "1024", "-10.0", "0.0009765625"],
         "correta": 0,
         "x": "Um evento de probabilidade 1/1024 traz log₂ 1024 = 10 bits de surpresa."},
        {"k": "conceito", "pergunta": "Qual distribuição tem entropia máxima?",
         "opcoes": ["A uniforme: todos os resultados igualmente prováveis", "A que tem um resultado com probabilidade 1", "A normal", "Qualquer uma com 2 resultados"],
         "correta": 0,
         "x": "Sem nenhum resultado favorito, a incerteza é a maior possível: log₂ k bits para k resultados."},
        {"k": "conceito", "pergunta": "Entropia zero quer dizer…",
         "opcoes": ["que não há incerteza: um resultado tem probabilidade 1", "que todos os resultados são igualmente prováveis", "que a distribuição está errada", "que há infinitos resultados"],
         "correta": 0,
         "x": "Se você já sabe o que vai acontecer, observar o resultado não traz informação nenhuma."},
        {"k": "conceito", "pergunta": "Um modelo de linguagem confiante na próxima palavra tem uma distribuição de saída com…",
         "opcoes": ["entropia baixa", "entropia alta", "entropia negativa", "entropia igual ao tamanho do vocabulário"],
         "correta": 0,
         "x": "Quase toda a probabilidade fica numa palavra só. Entropia alta indicaria dúvida entre muitas palavras."},
        {"k": "conceito", "pergunta": "Qual é a diferença entre medir a entropia em bits e em nats?",
         "opcoes": ["Só a base do log: 2 para bits, e (natural) para nats", "Bits são para texto e nats para imagens", "Nats são sempre maiores que bits", "Nenhuma: são idênticos"],
         "correta": 0,
         "x": "1 nat ≈ 1,44 bit. O PyTorch usa log natural, então as perdas dele vêm em nats."},
    ],

    "Entropia Cruzada (Cross-Entropy Loss) e função Softmax": [
        conta("softmax"), conta("ce"), conta("cegrad"), conta("softmax"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            z = np.array([2.0, 1.0, 0.0])
            p = np.exp(z) / np.exp(z).sum()
            print(np.round(p, 2))
         '''),
         "opcoes": ["[0.67 0.24 0.09]", "[0.67 0.33 0.  ]", "[2. 1. 0.]", "[0.33 0.33 0.33]"],
         "correta": 0,
         "x": "e² ≈ 7,39, e¹ ≈ 2,72 e e⁰ = 1, que somam 11,1. Divididos pela soma: 0,67, 0,24 e 0,09."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            p = np.array([0.7, 0.2, 0.1])
            y = np.array([0, 1, 0])
            print(round(-np.sum(y * np.log(p)), 3), p - y)
         '''),
         "opcoes": ["1.609 [ 0.7 -0.8  0.1]", "0.357 [ 0.7 -0.8  0.1]", "1.609 [-0.7  0.8 -0.1]", "0.8 [ 0.7 -0.8  0.1]"],
         "correta": 0,
         "x": "A classe certa é a 2ª, com p = 0,2: perda −ln 0,2 ≈ 1,609. O gradiente p − y empurra a 2ª classe para cima (−0,8) e as outras para baixo."},
        {"k": "conceito", "pergunta": "Quanto dá a softmax de logits iguais, como [z, z, z]?",
         "opcoes": ["Probabilidades iguais: 1/3 cada", "Tudo zero", "1 para a primeira classe", "Depende do valor de z"],
         "correta": 0,
         "x": "Os exponenciais são todos iguais, então cada um vale um terço da soma, qualquer que seja z."},
        {"k": "conceito", "pergunta": "O que acontece com a softmax se você somar a mesma constante a todos os logits?",
         "opcoes": ["Nada: as probabilidades não mudam", "Todas as probabilidades aumentam", "A maior probabilidade vira 1", "A soma passa de 1"],
         "correta": 0,
         "x": r"$e^{z_i + c} = e^c e^{z_i}$, e o $e^c$ se cancela na divisão. É por isso que dá para subtrair o maior logit antes, para evitar overflow."},
        {"k": "conceito", "pergunta": "Por que a entropia cruzada pune tanto uma resposta confiante e errada?",
         "opcoes": ["Porque −ln p explode quando a probabilidade da classe certa vai a 0", "Porque ela eleva o erro ao quadrado", "Porque ela ignora as classes erradas", "Não pune: a perda é sempre 1"],
         "correta": 0,
         "x": "Dar 1% à classe certa custa −ln 0,01 ≈ 4,6; dar 50% custa só 0,69."},
        {"k": "conceito", "pergunta": "Qual é o gradiente de softmax + entropia cruzada em relação aos logits?",
         "opcoes": [r"$p - y$", r"$y - p$", r"$-\ln p$", r"$p(1 - p)$"],
         "correta": 0,
         "x": "Um dos resultados mais limpos do cálculo: probabilidades previstas menos o rótulo one-hot."},
    ],

    "Divergência de Kullback-Leibler (KL Divergence)": [
        conta("kl"), conta("ceent"), conta("kl"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            P = np.array([0.5, 0.5])
            Q = np.array([0.9, 0.1])
            kl = lambda a, b: (a * np.log2(a / b)).sum()
            print(round(kl(P, Q), 3), round(kl(Q, P), 3))
         '''),
         "opcoes": ["0.737 0.531", "0.737 0.737", "0.531 0.737", "0.0 0.0"],
         "correta": 0,
         "x": "Trocar a ordem muda o valor: a KL não é simétrica e, por isso, não é uma distância de verdade."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            P = np.array([0.2, 0.3, 0.5])
            print((P * np.log2(P / P)).sum())
         '''),
         "opcoes": ["0.0", "1.0", "1.4854752972273344", "nan"],
         "correta": 0,
         "x": "Comparando uma distribuição com ela mesma, cada log é log 1 = 0: a KL é zero, e só é zero quando P = Q."},
        {"k": "conceito", "tema": "A divergência KL é simétrica?", "pergunta": r"$D_{KL}(P \parallel Q)$ é igual a $D_{KL}(Q \parallel P)$?",
         "opcoes": ["Em geral não: a KL não é simétrica", "Sim, sempre", "Só para distribuições normais", "Só se P e Q tiverem 2 resultados"],
         "correta": 0,
         "x": "Por isso a ordem importa na hora de treinar: cada uma penaliza erros diferentes (cobrir todos os modos ou focar num só)."},
        {"k": "conceito", "pergunta": "No RLHF, a penalidade de KL em relação ao modelo original serve para…",
         "opcoes": ["manter o modelo ajustado perto do original, sem desaprender a língua nem trapacear o avaliador", "acelerar o treino", "aumentar o vocabulário", "deixar as respostas mais longas"],
         "correta": 0,
         "x": "Sem ela, o modelo pode achar respostas estranhas que enganam o modelo de recompensa. A KL funciona como uma coleira."},
        {"k": "conceito", "pergunta": "A divergência KL pode ser negativa?",
         "opcoes": ["Não: é sempre ≥ 0, e só vale 0 quando P = Q", "Sim, quando Q é melhor que P", "Sim, em metade dos casos", "Só com log natural"],
         "correta": 0,
         "x": "É a desigualdade de Gibbs: usar a distribuição errada sempre custa bits a mais, nunca a menos."},
        {"k": "conceito", "pergunta": "Minimizar a entropia cruzada H(P, Q) em relação a Q equivale a minimizar…",
         "opcoes": [r"$D_{KL}(P \parallel Q)$, porque $H(P)$ não depende de Q", "a entropia de Q", "a acurácia", r"$D_{KL}(Q \parallel P)$"],
         "correta": 0,
         "x": "H(P, Q) = H(P) + KL(P‖Q). Os dados (P) estão fixos, então só a KL muda com o modelo."},
        {"k": "conceito", "pergunta": "Se Q dá probabilidade zero a algo que P considera possível, a KL(P‖Q)…",
         "opcoes": ["vai a infinito", "vale zero", "vale 1", "fica negativa"],
         "correta": 0,
         "x": "Aparece p · log(p/0). Por isso modelos de linguagem nunca dão probabilidade exatamente zero a um token."},
    ],

    "Funções de perda de regressão (MSE, MAE, Huber) e classificação": [
        conta("mse"), conta("mae"), conta("huber"), conta("huber"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            y = np.array([3.0, 5.0, 2.0, 7.0])
            yh = np.array([2.5, 5.0, 4.0, 8.0])
            e = yh - y
            print((e ** 2).mean(), np.abs(e).mean())
         '''),
         "opcoes": ["1.3125 0.875", "0.875 1.3125", "5.25 3.5", "1.3125 0.625"],
         "correta": 0,
         "x": "Erros −0,5, 0, 2 e 1. MSE = (0,25 + 0 + 4 + 1)/4 = 1,3125; MAE = (0,5 + 0 + 2 + 1)/4 = 0,875. O erro de 2 pesa muito mais no MSE."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            y = np.array([2.0, 3.0, 4.0, 50.0])
            print(np.mean(y), np.median(y))
         '''),
         "opcoes": ["14.75 3.5", "3.5 14.75", "14.75 14.75", "3.5 3.5"],
         "correta": 0,
         "x": "Prever um valor único: o MSE é minimizado pela média (14.75, puxada pelo 50) e o MAE pela mediana (3.5)."},
        {"k": "conceito", "pergunta": "Qual perda é mais sensível a outliers?",
         "opcoes": ["MSE", "MAE", "Huber", "Todas igualmente"],
         "correta": 0,
         "x": "O MSE eleva o erro ao quadrado: um erro de 10 vale 100. Um outlier pode dominar a perda e o gradiente."},
        {"k": "conceito", "pergunta": "Minimizar o MSE leva o modelo a prever…",
         "opcoes": ["a média; minimizar o MAE leva à mediana", "a mediana; o MAE leva à média", "a moda", "sempre zero"],
         "correta": 0,
         "x": "É por isso que o MAE é mais robusto: a mediana ignora o tamanho dos valores extremos."},
        {"k": "conceito", "pergunta": "O que a perda de Huber combina?",
         "opcoes": ["Uma parte quadrática perto do alvo e uma linear longe dele", "MSE e entropia cruzada", "Duas taxas de aprendizado", "MAE e acurácia"],
         "correta": 0,
         "x": "Perto do alvo, gradiente suave como o MSE; longe, gradiente limitado como o MAE, sem deixar um outlier explodir o treino."},
        {"k": "conceito", "pergunta": "Para classificação, qual é a perda padrão?",
         "opcoes": ["A entropia cruzada", "O MSE", "O MAE", "A perda de Huber"],
         "correta": 0,
         "x": "Ela trabalha com probabilidades e dá o gradiente p − y junto com a softmax. O MSE em probabilidades gera gradientes fracos."},
    ],
}
