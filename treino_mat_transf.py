# -*- coding: utf-8 -*-
"""
Treino · Matemática, Módulo 5 do site (Matemática dos Transformers & Geometria de Embeddings).

Contas com números novos a cada vez (geradores em treino_contas_transf.py), saídas de código com NumPy (o gabarito
é o que o NumPy imprime de verdade) e questões de conceito.
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
    "Espaços vetoriais de alta dimensão e armazenamento de fatos em LLMs": [
        conta("quaseort"), conta("normsq"), conta("paramsffn"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            rng = np.random.default_rng(0)
            a, b = rng.normal(size=(2, 4096))
            cos = a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
            print(abs(cos) < 0.05)
         '''),
         "opcoes": ["True", "False", "1.0", "0.0"],
         "correta": 0,
         "x": "Em 4096 dimensões, o cosseno entre dois vetores aleatórios tem desvio de só 1/64 ≈ 0,016: eles saem quase perpendiculares."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            x = np.random.default_rng(0).normal(size=10_000)
            print(round(np.linalg.norm(x) / np.sqrt(10_000), 1))
         '''),
         "opcoes": ["1.0", "0.0", "100.0", "0.5"],
         "correta": 0,
         "x": "A norma de um vetor aleatório com variância 1 por coordenada fica perto de √d. Dividindo por √d, sobra cerca de 1."},
        {"k": "conceito", "pergunta": "Por que um modelo com vetores de 4096 dimensões consegue representar muito mais do que 4096 conceitos?",
         "opcoes": ["Em alta dimensão cabem muitíssimas direções quase perpendiculares, que quase não interferem umas nas outras", "Porque cada coordenada guarda vários números", "Porque o modelo comprime as palavras em zip", "Não consegue: são no máximo 4096"],
         "correta": 0,
         "x": "Se as direções podem ser só quase perpendiculares (cosseno perto de 0), o número delas cresce exponencialmente com a dimensão."},
        {"k": "conceito", "pergunta": "O que o lema de Johnson-Lindenstrauss diz?",
         "opcoes": ["Dá para projetar muitos pontos em menos dimensões preservando, aproximadamente, as distâncias entre eles", "Todo vetor pode ser escrito com duas coordenadas", "A distância entre pontos sempre aumenta com a dimensão", "Projeções aleatórias sempre destroem as distâncias"],
         "correta": 0,
         "x": "É a base de várias buscas aproximadas de vetores: dá para reduzir a dimensão sem bagunçar quem está perto de quem."},
        {"k": "conceito", "pergunta": "As camadas feed-forward (MLP) de um Transformer funcionam como…",
         "opcoes": ["uma memória chave-valor: a 1ª matriz reconhece padrões e a 2ª escreve a informação associada", "uma camada de atenção extra", "um verificador de gramática", "uma tabela de embeddings de posição"],
         "correta": 0,
         "x": "Pesquisas de interpretabilidade mostram fatos (\"Paris é a capital da França\") sendo recuperados nessas camadas."},
        {"k": "conceito", "pergunta": "Em dimensão alta, dois vetores sorteados ao acaso tendem a ser…",
         "opcoes": ["quase perpendiculares", "quase paralelos", "idênticos", "opostos"],
         "correta": 0,
         "x": "O cosseno entre eles se concentra perto de zero, com desvio de cerca de 1/√d."},
        {"k": "conceito", "pergunta": "Com d_ff = 4·d_model, que fração dos pesos de um bloco de Transformer fica na camada feed-forward?",
         "opcoes": ["Cerca de dois terços", "Cerca de 10%", "Metade", "Quase nada"],
         "correta": 0,
         "x": "Feed-forward: 2 · d · 4d = 8d². Atenção (Q, K, V e O): 4d². Então 8d² de 12d², ou seja, dois terços."},
    ],

    "Normalização de embeddings e geometria do espaço semântico": [
        conta("normaliza"), conta("dist2cos"), conta("rmsnorm"), conta("dist2cos"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            v = np.array([3.0, 4.0])
            u = v / np.linalg.norm(v)
            print(u, np.linalg.norm(u))
         '''),
         "opcoes": ["[0.6 0.8] 1.0", "[3. 4.] 5.0", "[0.6 0.8] 5.0", "[0.43 0.57] 1.0"],
         "correta": 0,
         "x": "Dividindo pela norma (5), sobra a direção com comprimento 1: [0.6 0.8]."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            x = np.array([1.0, 1.0, 3.0, 5.0])
            print(np.round(x / np.sqrt(np.mean(x ** 2)), 2))
         '''),
         "opcoes": ["[0.33 0.33 1.   1.67]", "[0.1 0.1 0.3 0.5]", "[1. 1. 3. 5.]", "[0.17 0.17 0.5  0.83]"],
         "correta": 0,
         "x": "A média dos quadrados é (1 + 1 + 9 + 25)/4 = 9, e a raiz é 3. A RMSNorm divide tudo por 3."},
        {"k": "conceito", "pergunta": "Com embeddings normalizados (comprimento 1), o produto escalar é igual a…",
         "opcoes": ["a similaridade de cosseno", "a distância euclidiana", "zero", "a soma das coordenadas"],
         "correta": 0,
         "x": "O cosseno é o produto escalar dividido pelas normas. Se as normas são 1, sobra só o produto escalar, que é bem rápido de calcular."},
        {"k": "conceito", "pergunta": "Por que a RMSNorm é mais barata que a LayerNorm?",
         "opcoes": ["Não calcula nem subtrai a média: só divide pela raiz da média dos quadrados", "Porque usa números inteiros", "Porque roda só na primeira camada", "Porque não tem parâmetros"],
         "correta": 0,
         "x": "Na prática ela funciona tão bem quanto a LayerNorm e economiza contas em todas as camadas. Por isso modelos como o Llama a usam."},
        {"k": "conceito", "pergunta": "Na esfera unitária vale ‖u − v‖² = 2 − 2 cos θ. O que isso quer dizer na prática?",
         "opcoes": ["Ordenar os vizinhos pela distância ou pelo cosseno dá o mesmo resultado", "A distância é sempre 2", "O cosseno não serve para embeddings", "Os vetores precisam ser perpendiculares"],
         "correta": 0,
         "x": "Quanto maior o cosseno, menor a distância. Com vetores normalizados, as duas métricas concordam."},
        {"k": "conceito", "tema": "O que é a esfera unitária", "pergunta": r"O que é a esfera unitária $\mathbb{S}^{d-1}$?",
         "opcoes": ["O conjunto dos vetores de comprimento 1 em d dimensões", "Uma bola cheia de raio d", "Os vetores com todas as coordenadas iguais a 1", "Uma esfera com d − 1 pontos"],
         "correta": 0,
         "x": "Em 2 dimensões é o círculo de raio 1; em 3, a casca da bola. Normalizar um embedding é projetá-lo nessa esfera."},
    ],

    "Projeções lineares e matrizes de pesos Query, Key e Value (W_q, W_k, W_v)": [
        conta("qkvshape"), conta("qproj"), conta("paramsqkv"), conta("qkvshape"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            X = np.ones((10, 512))
            W_q = np.ones((512, 64))
            print((X @ W_q).shape)
         '''),
         "opcoes": ["(10, 64)", "(512, 64)", "(10, 512)", "(64, 10)"],
         "correta": 0,
         "x": "10 tokens, cada um com 512 números, viram 10 queries de 64 números."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            x = np.array([1.0, 2.0])
            W_q = np.array([[1.0, 0.0], [0.0, 1.0]])
            W_k = np.array([[0.0, 1.0], [1.0, 0.0]])
            print(x @ W_q, x @ W_k)
         '''),
         "opcoes": ["[1. 2.] [2. 1.]", "[1. 2.] [1. 2.]", "[2. 1.] [1. 2.]", "[1. 2.] [0. 0.]"],
         "correta": 0,
         "x": "O mesmo embedding vira uma query e uma key diferentes: W_q aqui é a identidade, e W_k troca as coordenadas."},
        {"k": "conceito", "pergunta": "Na metáfora da biblioteca, o que é a query de um token?",
         "opcoes": ["O que ele está procurando", "Como ele se apresenta para os outros (a etiqueta)", "O conteúdo que ele entrega", "A posição dele na frase"],
         "correta": 0,
         "x": "Query: o que eu procuro. Key: como eu me apresento. Value: o que eu entrego se alguém prestar atenção em mim."},
        {"k": "conceito", "pergunta": "Por que usar matrizes W_Q e W_K diferentes, em vez de comparar os embeddings direto?",
         "opcoes": ["Assim \"o que procuro\" e \"o que ofereço\" podem ser coisas diferentes, e a atenção deixa de ser simétrica", "Para gastar mais memória", "Porque os embeddings não podem ser multiplicados", "Não há motivo: dá no mesmo"],
         "correta": 0,
         "x": "Um verbo pode procurar o sujeito sem que o sujeito procure o verbo. Comparando os embeddings brutos, a atenção de i para j seria igual à de j para i."},
        {"k": "conceito", "tema": "O que mede cada elemento de QKᵀ", "pergunta": r"$QK^\top$ tem shape (n, n). O que mede o elemento (i, j)?",
         "opcoes": ["O quanto o token i se interessa pelo token j", "A distância entre as posições i e j", "A probabilidade da palavra j", "O valor do token i"],
         "correta": 0,
         "x": "É o produto escalar da query de i com a key de j. Depois da escala e da softmax, vira o peso de atenção."},
        {"k": "conceito", "pergunta": "As matrizes W_Q, W_K e W_V são…",
         "opcoes": ["aprendidas no treino e as mesmas para todas as posições da frase", "fixas, definidas à mão", "diferentes para cada palavra do vocabulário", "sorteadas de novo a cada frase"],
         "correta": 0,
         "x": "São parâmetros comuns, ajustados pelo gradiente. Por isso o número de pesos não depende do tamanho da frase."},
    ],

    "Fórmula de Scaled Dot-Product Attention: softmax((Q @ K^T) / sqrt(d_k)) * V": [
        conta("attscore"), conta("attpesos"), conta("attout"), conta("varscale"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            q = np.array([1.0, 2.0, 0.0, 1.0])
            K = np.array([[1.0, 1.0, 0.0, 0.0],
                          [0.0, 0.0, 1.0, 0.0]])
            s = K @ q / np.sqrt(4)
            w = np.exp(s) / np.exp(s).sum()
            print(s, np.round(w, 2))
         '''),
         "opcoes": ["[1.5 0. ] [0.82 0.18]", "[3. 0.] [0.95 0.05]", "[1.5 0. ] [1. 0.]", "[0.75 0.  ] [0.68 0.32]"],
         "correta": 0,
         "x": "Os produtos escalares são 3 e 0; divididos por √4 = 2, viram 1,5 e 0. A softmax dá 82% de atenção para a primeira key."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            w = np.array([0.75, 0.25])
            V = np.array([[4.0, 0.0],
                          [0.0, 8.0]])
            print(w @ V)
         '''),
         "opcoes": ["[3. 2.]", "[2. 4.]", "[1. 6.]", "[4. 8.]"],
         "correta": 0,
         "x": "A saída é a média dos values ponderada pela atenção: 0,75·(4, 0) + 0,25·(0, 8) = (3, 2)."},
        {"k": "conceito", "tema": "Por que dividir por √d_k", "pergunta": r"Por que dividir as pontuações por $\sqrt{d_k}$?",
         "opcoes": ["Sem isso, as pontuações crescem com d_k, a softmax satura e os gradientes somem", "Para economizar memória", "Para as pontuações ficarem inteiras", "Por tradição, sem efeito real"],
         "correta": 0,
         "x": "Com d_k = 64, o produto escalar tem desvio padrão 8. Uma softmax de números grandes vira quase 0 ou 1, e o gradiente quase zera."},
        {"k": "conceito", "pergunta": "Depois da softmax, quanto soma cada linha da matriz de atenção?",
         "opcoes": ["1", "0", "n (o número de tokens)", "d_k"],
         "correta": 0,
         "x": "Cada linha é a distribuição de atenção de um token sobre todos os outros: probabilidades que somam 1."},
        {"k": "conceito", "pergunta": "O que é a saída da atenção para cada token?",
         "opcoes": ["Uma média ponderada dos values de todos os tokens", "O value do próprio token", "A key mais parecida", "A soma das queries"],
         "correta": 0,
         "x": "Cada token sai como uma mistura de informações da frase, na proporção da atenção que deu a cada posição."},
        {"k": "conceito", "pergunta": "Num modelo como o GPT, o que faz a máscara causal?",
         "opcoes": ["Impede cada token de olhar para os tokens futuros", "Esconde palavras aleatórias", "Remove a pontuação", "Junta tokens repetidos"],
         "correta": 0,
         "x": "Antes da softmax, as posições futuras recebem −∞. Assim o modelo aprende a prever a próxima palavra sem espiar a resposta."},
    ],

    "Mecanismo Multi-Head Attention: divisão de dimensões e concatenação": [
        conta("dk"), conta("mhashape"), conta("mhaparams"), conta("mhashape"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            n, d, h = 10, 512, 8
            Q = np.zeros((n, d))
            print(Q.reshape(n, h, d // h).shape)
         '''),
         "opcoes": ["(10, 8, 64)", "(10, 64, 8)", "(8, 10, 512)", "(10, 4096)"],
         "correta": 0,
         "x": "Os 512 números de cada token são fatiados em 8 cabeças de 64. É assim que a multi-head é implementada: um reshape, sem copiar nada."},
        {"k": "saida", "codigo": c('''
            d_model, h = 768, 12
            print(d_model // h, h * (d_model // h))
         '''),
         "opcoes": ["64 768", "12 768", "64 9216", "9216 768"],
         "correta": 0,
         "x": "Cada cabeça tem 768/12 = 64 dimensões. Juntando as 12, volta a 768: a concatenação reconstrói o d_model."},
        {"k": "conceito", "pergunta": "Por que usar várias cabeças de atenção em vez de uma?",
         "opcoes": ["Cada cabeça pode olhar um tipo diferente de relação (sintaxe, referência, posição) ao mesmo tempo", "Para o modelo ficar mais lento", "Porque uma cabeça só não consegue calcular a softmax", "Para usar mais memória de vídeo"],
         "correta": 0,
         "x": "Uma única softmax faz uma média só. Várias cabeças fazem várias médias independentes, cada uma focando numa coisa."},
        {"k": "conceito", "pergunta": "Aumentar o número de cabeças, com o d_model fixo…",
         "opcoes": ["não aumenta o custo total: cada cabeça fica menor", "dobra o número de parâmetros", "obriga a aumentar o vocabulário", "deixa cada cabeça maior"],
         "correta": 0,
         "x": "Com h cabeças de dimensão d/h, as contas somam o mesmo que uma cabeça de dimensão d."},
        {"k": "conceito", "pergunta": "Para que serve a matriz W_O no fim da multi-head attention?",
         "opcoes": ["Mistura as saídas das cabeças concatenadas de volta no espaço d_model", "Calcula a softmax", "Guarda as posições", "Escolhe qual cabeça usar"],
         "correta": 0,
         "x": "Sem a W_O, cada cabeça ficaria isolada na sua fatia. A projeção final combina o que todas encontraram."},
        {"k": "conceito", "pergunta": "Na grouped-query attention (GQA), usada em LLMs recentes, o que acontece?",
         "opcoes": ["Grupos de cabeças compartilham as mesmas keys e values, economizando memória na geração", "Cada cabeça usa um vocabulário diferente", "As queries são eliminadas", "A atenção passa a olhar só a última palavra"],
         "correta": 0,
         "x": "Na geração, keys e values de todos os tokens anteriores ficam guardados (o KV cache). Compartilhá-los entre cabeças reduz muito essa memória."},
    ],

    "Positional Encodings: funções sinusoidais e rotação vetorial (RoPE)": [
        conta("rope"), conta("roperel"), conta("pefreq"), conta("rope"),
        {"k": "saida", "codigo": c('''
            import numpy as np
            pos, d = 0, 4
            pe = [np.sin(pos / 10000 ** (i / d)) if i % 2 == 0 else np.cos(pos / 10000 ** ((i - 1) / d)) for i in range(d)]
            print(np.round(pe, 1))
         '''),
         "opcoes": ["[0. 1. 0. 1.]", "[0. 0. 0. 0.]", "[1. 0. 1. 0.]", "[1. 1. 1. 1.]"],
         "correta": 0,
         "x": "Na posição 0, todos os senos valem 0 e todos os cossenos valem 1. As outras posições giram esses pares em velocidades diferentes."},
        {"k": "saida", "codigo": c('''
            import numpy as np
            def rot(v, ang):
                c, s = np.cos(ang), np.sin(ang)
                return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1]])
            q, k, t = np.array([1.0, 2.0]), np.array([3.0, 1.0]), 0.3
            a = rot(q, 5 * t) @ rot(k, 2 * t)
            b = rot(q, 13 * t) @ rot(k, 10 * t)
            print(round(a, 6) == round(b, 6))
         '''),
         "opcoes": ["True", "False", "0.0", "3"],
         "correta": 0,
         "x": "Posições 5 e 2, ou 13 e 10: a diferença é 3 nos dois casos, então o produto escalar é o mesmo. É a propriedade que faz o RoPE funcionar."},
        {"k": "conceito", "pergunta": "Por que o Transformer precisa de codificação de posição?",
         "opcoes": ["Sem ela, a atenção trata a frase como um saco de palavras: não sabe a ordem", "Para economizar memória", "Para traduzir entre línguas", "Não precisa: a atenção já sabe a ordem"],
         "correta": 0,
         "x": "A atenção compara todos com todos e dá o mesmo resultado se você embaralhar os tokens. A posição precisa entrar de algum jeito."},
        {"k": "conceito", "pergunta": "No positional encoding senoidal original, o que se faz com a posição?",
         "opcoes": ["Soma-se o vetor de posição ao embedding do token", "Multiplica-se o embedding pela posição", "Escreve-se a posição como uma palavra extra", "Gira-se a query e a key"],
         "correta": 0,
         "x": "X + PE: cada posição tem um vetor fixo de senos e cossenos somado ao embedding. Girar a query e a key é a ideia do RoPE."},
        {"k": "conceito", "pergunta": "Qual é a grande vantagem do RoPE?",
         "opcoes": ["O produto escalar entre query e key passa a depender só da distância relativa entre as posições", "Dispensa a softmax", "Deixa o modelo sem parâmetros", "Faz cada token olhar só para o vizinho"],
         "correta": 0,
         "x": "Girar q por mθ e k por nθ deixa o produto escalar dependendo de (m − n)θ. Isso ajuda o modelo a lidar com textos mais longos que os do treino."},
        {"k": "conceito", "pergunta": "No encoding senoidal, para que servem as frequências mais lentas?",
         "opcoes": ["Para distinguir posições distantes, como o ponteiro das horas de um relógio", "Para marcar o fim da frase", "Para guardar a pontuação", "Não servem para nada"],
         "correta": 0,
         "x": "As frequências rápidas separam vizinhos (os segundos); as lentas mudam devagar e distinguem posições longe umas das outras (as horas)."},
    ],
}
