# -*- coding: utf-8 -*-
"""Aulas Visuais de Matemática acrescentadas na revisão do currículo (formato v2 da lesson_factory)."""
from lesson_factory import *

TITULO_AB = "Estatística para comparar modelos (teste A/B, bootstrap e tamanho de amostra)"

TOPICO_AB = {
    "title": TITULO_AB,
    "video_url": "https://www.youtube.com/watch?v=j9pnNCiQz3I",
    "video_label": "▶ Comunidade DS · Teste A/B",
    "video2_url": "https://www.youtube.com/watch?v=Xz0x-8-cgaQ",
    "video2_label": "🎬 2ª Opção: StatQuest Bootstrapping",
    "doc_url": "https://pt.khanacademy.org/math/statistics-probability/significance-tests-one-sample",
    "doc_label": "📘 Khan Academy: Testes de significância",
}

AULAS = {}

AULAS[TITULO_AB] = finalizar(aula(
    35,
    "Você trocou o prompt do seu chatbot e a taxa de acerto nos testes subiu de 82% para 85%. Melhorou de verdade ou foi sorte das perguntas que caíram? Essa pergunta aparece toda semana em quem trabalha com IA: comparar dois modelos, dois prompts, duas versões de um sistema. A estatística responde com duas ferramentas simples: o <b>intervalo de confiança por bootstrap</b> e a conta de <b>quantas amostras</b> você precisa.",
    ["entender por que uma diferença pequena pode ser só acaso;", "calcular um intervalo de confiança por bootstrap, sem fórmulas complicadas;", "decidir se a diferença entre dois modelos é real;", "estimar quantas perguntas de teste são necessárias."],
    ["Média e variância; intervalos de confiança e teste de hipóteses (noção)."],
    [
        chute("Com 20 perguntas de teste, o modelo A acertou 17 (85%) e o B acertou 16 (80%). O A é melhor?", ["Sim, 85% é maior que 80%.", "Não dá para afirmar: com só 20 perguntas, 1 acerto a mais pode ser sorte.", "Não, os dois são iguais com certeza."], 1,
              ["Com 20 perguntas, cada pergunta vale 5 pontos percentuais: a diferença é de uma única pergunta.", "Isso! A diferença existe nos números, mas é pequena demais para descartar o acaso.", "Também não dá para afirmar que são iguais."],
              "Poucas amostras e diferença pequena: o resultado pode virar se você trocar as perguntas."),
        concreto("O teste do cimento", "<p>Duas marcas de cimento prometem a mesma resistência. Você faz 2 corpos de prova de cada uma e a marca A dá um número um pouco maior. Ninguém experiente troca de fornecedor por isso: com 2 amostras, a diferença pode ser do jeito que cada peça foi moldada. Com 30 corpos de prova de cada, aí sim dá para confiar. Com modelos de IA é igual: a pergunta é <b>quantas amostras</b> e <b>quão grande</b> é a diferença.</p>"),
        crianca("<p>Se você jogar uma moeda 4 vezes e der 3 caras, não quer dizer que a moeda é viciada. Se jogar 1000 vezes e der 750 caras, aí desconfie. Quanto mais vezes você testa, menos o acaso consegue te enganar.</p>"),
        ver("como o teste A/B separa a diferença real do acaso"),
        texto("A ideia do bootstrap", "<p>Você só tem um conjunto de perguntas de teste. O bootstrap finge que tem vários: <b>sorteia com reposição</b> perguntas desse mesmo conjunto (algumas aparecem duas vezes, outras nenhuma), recalcula a diferença entre os modelos e repete isso milhares de vezes. Os valores que aparecem mostram o quanto a diferença “balança” por acaso.</p>" + py('''
import random
dif = []
for _ in range(2000):
    idx = [random.randrange(n) for _ in range(n)]      # sorteia perguntas com reposição
    acc_a = sum(a[i] for i in idx) / n
    acc_b = sum(b[i] for i in idx) / n
    dif.append(acc_a - acc_b)
dif.sort()
intervalo = (dif[int(0.025 * 2000)], dif[int(0.975 * 2000)])   # 95% do meio
''') + "<p>Sorteie as <b>mesmas</b> perguntas para os dois modelos (amostra pareada): a comparação fica justa. Se o intervalo de 95% <b>não contém o zero</b>, a diferença dificilmente é acaso.</p>"),
        nota("Para ler os resultados", [
            ("Intervalo de 95%", "faixa provável da diferença real", "Ex.: de +2% a +9%: A é melhor, e a vantagem está nessa faixa."),
            ("Contém o zero", "pode ser acaso", "Ex.: de −3% a +5%: não dá para dizer que um é melhor."),
            ("n ≈ 16 · p(1 − p) / d²", "amostras por versão (regra de bolso)", "p = taxa de acerto esperada; d = a diferença que você quer conseguir enxergar."),
            ("Tamanho do efeito", "quanto melhorou", "Diferença real, mas de 0,1%, pode não valer o custo."),
        ], rot="Agora sim, a notação"),
        cod("O prompt novo é melhor mesmo?", "Os mesmos 200 testes foram rodados com o prompt antigo (B) e o novo (A); 1 = acertou, 0 = errou. Complete as três funções: <code>diferenca</code> (acurácia de A menos acurácia de B); <code>bootstrap_ic</code>, que sorteia com reposição os <b>índices</b> das perguntas (os mesmos para A e B), repete <code>n</code> vezes e devolve o intervalo de 95% (posições 2,5% e 97,5% da lista ordenada); e <code>significativo</code>, que diz se o intervalo não contém o zero.",
            '''
import random

random.seed(42)
a = [1 if random.random() < 0.88 else 0 for _ in range(200)]   # prompt novo
b = [1 if random.random() < 0.74 else 0 for _ in range(200)]   # prompt antigo

def diferenca(acertos_a, acertos_b):
    return 0.0

def bootstrap_ic(acertos_a, acertos_b, n=2000, semente=0):
    rng = random.Random(semente)
    return (0.0, 0.0)

def significativo(ic):
    return False

ic = bootstrap_ic(a, b)
print("diferença:", round(diferenca(a, b), 3), "| IC 95%:", [round(x, 3) for x in ic], "| real?", significativo(ic))
''',
            [("Diferença de acurácia", "assert abs(diferenca(a, b) - (sum(a) - sum(b)) / len(a)) < 1e-9 and diferenca(a, b) > 0"),
             ("O intervalo tem largura de verdade", "lo, hi = bootstrap_ic(a, b)\nassert lo < diferenca(a, b) < hi and 0.03 < hi - lo < 0.3, (lo, hi)"),
             ("Diferença grande: é real", "assert significativo(bootstrap_ic(a, b)) is True"),
             ("Diferença de 1 pergunta: pode ser acaso", "b2 = a[:]\nb2[a.index(1)] = 0\nassert significativo(bootstrap_ic(a, b2)) is False"),
             ("Intervalo de 95% decide certo", "assert significativo((0.01, 0.08)) is True and significativo((-0.02, 0.05)) is False and significativo((-0.09, -0.01)) is True")],
            '''
import random

random.seed(42)
a = [1 if random.random() < 0.88 else 0 for _ in range(200)]   # prompt novo
b = [1 if random.random() < 0.74 else 0 for _ in range(200)]   # prompt antigo

def diferenca(acertos_a, acertos_b):
    return sum(acertos_a) / len(acertos_a) - sum(acertos_b) / len(acertos_b)

def bootstrap_ic(acertos_a, acertos_b, n=2000, semente=0):
    rng = random.Random(semente)
    tam = len(acertos_a)
    difs = []
    for _ in range(n):
        idx = [rng.randrange(tam) for _ in range(tam)]
        difs.append(sum(acertos_a[i] for i in idx) / tam - sum(acertos_b[i] for i in idx) / tam)
    difs.sort()
    return (difs[int(0.025 * n)], difs[int(0.975 * n) - 1])

def significativo(ic):
    return ic[0] > 0 or ic[1] < 0

ic = bootstrap_ic(a, b)
print("diferença:", round(diferenca(a, b), 3), "| IC 95%:", [round(x, 3) for x in ic], "| real?", significativo(ic))
''', ["Diferença: <code>sum(a)/len(a) - sum(b)/len(b)</code>.", "No bootstrap, sorteie <code>idx = [rng.randrange(tam) for _ in range(tam)]</code> e use os mesmos índices para A e B.", "Ordene a lista de diferenças e pegue as posições <code>int(0.025 * n)</code> e <code>int(0.975 * n) - 1</code>.", "Não contém o zero = o limite de baixo é maior que zero, ou o de cima é menor que zero."]),
        pratica([
            ("Fácil", "Seu modelo acerta cerca de 80% (p = 0,8) e você quer conseguir enxergar uma melhora de 10 pontos (d = 0,10). Pela regra de bolso, quantas perguntas de teste por versão?", 256, ["n ≈ 16 · p(1 − p) / d²", "16 · 0,8 · 0,2 = 2,56; e 0,10² = 0,01."], "16 · 0,8 · 0,2 / 0,01 = 256 perguntas."),
            ("Médio", "Mesmo modelo (p = 0,8), mas agora você quer enxergar uma melhora de só 5 pontos (d = 0,05). Quantas perguntas?", 1024, ["Metade da diferença exige 4 vezes mais amostras.", "0,05² = 0,0025."], "2,56 / 0,0025 = 1024. Diferenças pequenas exigem muitos testes."),
            ("Difícil", "Você tem só 100 perguntas de teste e o modelo acerta cerca de 50% (p = 0,5). Qual é a menor diferença d que dá para enxergar com segurança? Responda em pontos percentuais.", 20, ["Isole d: d ≈ √(16 · p(1 − p) / n).", "16 · 0,25 / 100 = 0,04; √0,04 = 0,2."], "d ≈ 0,20, ou seja, 20 pontos percentuais. Com 100 perguntas, só diferenças grandes aparecem."),
        ]),
        erros([
            ("Declarar vitória com poucas perguntas de teste.", "Calcule o intervalo (ou o tamanho de amostra) antes de comemorar."),
            ("Sortear perguntas diferentes para A e para B.", "Use as mesmas perguntas (pareado): a comparação fica muito mais precisa."),
            ("Rodar 20 comparações e comemorar a única que deu “significativa”.", "Quanto mais testes, mais falsos positivos. Defina antes o que vai comparar."),
            ("Confundir “estatisticamente real” com “importante”.", "Uma melhora real de 0,2% pode não valer o custo de um modelo mais caro."),
        ]),
        ponte("Onde isso aparece no trabalho com IA", "<p>Na trilha de IA, a aula de <b>Avaliação de LLMs (evals)</b> compara versões de prompts e modelos: é exatamente este bootstrap que diz se a versão nova é melhor. Em produto, o mesmo raciocínio decide testes A/B com usuários de verdade.</p>"),
        quiz([
            ("O intervalo de 95% da diferença entre A e B foi de −2% a +6%. Conclusão:", ["A é melhor.", "Não dá para dizer que um é melhor: o intervalo contém o zero.", "B é melhor."], 1, "Contém o zero: pode ser acaso."),
            ("No bootstrap, as perguntas são sorteadas:", ["sem reposição", "com reposição", "só as que o modelo errou"], 1, "Com reposição: algumas se repetem, outras ficam de fora."),
            ("Para enxergar uma diferença 2 vezes menor, você precisa de:", ["2 vezes mais amostras", "4 vezes mais amostras", "o mesmo número"], 1, "O n cresce com 1/d²."),
        ]),
    ],
    ["Diferenças pequenas com poucas amostras podem ser acaso.", "Bootstrap pareado: sorteie as mesmas perguntas com reposição; se o IC de 95% não contém o zero, a diferença é real.", "Amostras necessárias ≈ 16 · p(1 − p) / d²: diferenças pequenas exigem muitos testes."],
    "Teoria da Informação: Entropia de Shannon.",
    livro=("ISLP", "James et al., Introduction to Statistical Learning, seção 5.2 (The Bootstrap)", "Como o livro usa o bootstrap para medir a incerteza de uma estimativa?")),
    {"url": TOPICO_AB["doc_url"], "nome": "Khan Academy: Testes de significância"})
