# -*- coding: utf-8 -*-
"""Inglês · Módulo 7: Inglês para Trabalhar com IA (acrescentado na revisão do currículo).

Diferente dos módulos 1 a 6 (playlist do EnglishBay), aqui cada aula usa um vídeo em inglês sobre uma
situação real de trabalho. As aulas ficam chaveadas pelo videoId, como as outras de Inglês.
"""
from lesson_factory import *

AULAS = {}


def _t(vid, titulo):
    return {"videoId": vid, "title": titulo, "url": "https://www.youtube.com/watch?v=" + vid, "video_label": "▶ YouTube (EN)"}


MODULO_7 = {
    "t": "Módulo 7 · Inglês para Trabalhar com IA",
    "d": "3 a 4 semanas (1 aula a cada 2 dias)",
    "tip": "💡 <b>Dica de Estudo:</b> Aqui os vídeos são de falantes de inglês, sem tradução. Ative a legenda em inglês, pause e repita as frases. "
           "Depois de cada aula, aplique num artefato real seu: o README de um projeto, um pull request, a sua resposta de entrevista.",
    "p": "Gravar um vídeo de 2 minutos, em inglês, explicando um projeto seu do GitHub (problema, solução, resultado e o que aprendeu) e escrever o README dele em inglês.",
    "r": "Vídeos de inglês para profissionais de tecnologia · Seu próprio GitHub · Prática diária de 20 a 30 min",
    "g": [
        ["Ler e escrever no trabalho", [
            _t("lwqeNnboh_4", "Inglês no trabalho 01 · Ler documentação técnica"),
            _t("RjG689EwG5g", "Inglês no trabalho 02 · Ler artigos de Machine Learning"),
            _t("fDJNt67xdvQ", "Inglês no trabalho 03 · Escrever o README do seu projeto"),
            _t("DWCO02rBrAg", "Inglês no trabalho 04 · Pull requests e code review"),
        ]],
        ["Comunicação com a equipe", [
            _t("qXCWEOIOYhc", "Inglês no trabalho 05 · E-mails e mensagens de trabalho"),
            _t("MsxcpZr1LpM", "Inglês no trabalho 06 · Daily stand-up e reuniões"),
        ]],
        ["Entrevistas em inglês", [
            _t("VmsJVjKIWSg", "Inglês no trabalho 07 · Explicar o seu projeto em 2 minutos"),
            _t("RtXqF1_rKMk", "Inglês no trabalho 08 · “Tell me about yourself” e perguntas comportamentais"),
        ]],
    ],
}

# --------------------------------------------------------------------------------------------- 01
AULAS["lwqeNnboh_4"] = aula_en(
    "Quase toda biblioteca de IA (PyTorch, Hugging Face, LangChain, FastAPI) tem a documentação principal em inglês, e as versões traduzidas atrasam. Quem lê documentação em inglês com calma resolve sozinho o que outros ficam horas perguntando. A boa notícia: documentação usa um vocabulário pequeno e repetitivo, e dá para aprender os padrões.",
    ["reconhecer as partes de uma documentação (<i>quickstart, reference, guide</i>);", "entender os verbos e termos mais comuns (<i>returns, raises, deprecated</i>);", "procurar a resposta sem ler tudo."],
    ("Na documentação está escrito: <i>“This parameter is deprecated and will be removed in v3.”</i> O que isso quer dizer?", ["O parâmetro é obrigatório na versão 3.", "O parâmetro está ultrapassado e vai deixar de existir na versão 3.", "O parâmetro foi melhorado na versão 3."], 1,
     ["<i>Required</i> é que significaria obrigatório.", "Isso! <i>Deprecated</i> = ainda funciona, mas não use em código novo: vai sumir.", "Seria <i>improved</i>."],
     "Deprecated é um dos avisos mais importantes da documentação: troque antes que quebre."),
    ("Lendo a documentação juntos", [
        ("Dev", "Where did you find how to set the timeout?", "Onde você achou como configurar o tempo limite?"),
        ("Ana", "In the API reference. The quickstart doesn't cover it.", "Na referência da API. O guia rápido não fala disso."),
        ("Dev", "It says the function returns a dict and raises a ValueError if the key is missing.", "Diz que a função devolve um dicionário e levanta ValueError se a chave estiver faltando."),
        ("Ana", "Right. And check the note: the old parameter is deprecated.", "Isso. E veja a nota: o parâmetro antigo está ultrapassado."),
        ("Dev", "Got it. I'll use the new one and add a link to the docs in the PR.", "Entendi. Vou usar o novo e colocar o link da documentação no PR."),
    ]),
    "como a pessoa procura a informação: o que ela lê primeiro e o que ela pula",
    tabela("As partes de uma documentação", ["Seção", "O que você encontra", "Quando ler"], [
        ["Quickstart / Getting started", "o mínimo para rodar o primeiro exemplo", "no primeiro contato"],
        ["Tutorials / Guides", "passo a passo de tarefas comuns", "para aprender a usar"],
        ["API reference", "cada função: parâmetros, retorno, erros", "quando você já sabe o que procura"],
        ["Changelog / Release notes", "o que mudou em cada versão", "antes de atualizar a biblioteca"],
        ["FAQ / Troubleshooting", "problemas comuns e soluções", "quando algo dá errado"],
    ], corpo="<p>Use <b>Ctrl + F</b> com o nome da função ou o texto do erro. Documentação se consulta como um dicionário, não se lê como um romance.</p>"),
    [("returns", "devolve", "The function returns a list."), ("raises", "levanta (um erro)", "It raises a ValueError."), ("deprecated", "ultrapassado, vai ser removido", "This method is deprecated."),
     ("default", "valor padrão", "The default value is 10."), ("optional / required", "opcional / obrigatório", "The name is required."), ("under the hood", "por baixo dos panos", "Under the hood, it uses NumPy.")],
    [("The function returns a list of strings.", ["A função devolve uma lista de textos", "A função recebe uma lista", "A função apaga a lista"], 0, "A função devolve uma lista de textos."),
     ("This argument is optional.", ["Este argumento é opcional", "Este argumento é obrigatório", "Este argumento não existe"], 0, "Este argumento é opcional."),
     ("It raises an error if the file is missing.", ["Levanta um erro se o arquivo estiver faltando", "Cria o arquivo", "Ignora o arquivo"], 0, "Levanta um erro se o arquivo estiver faltando."),
     ("The default value is ten.", "5 palavras"), ("This method is deprecated.", "4 palavras")],
    [("The function returns a dictionary.", "A função devolve um dicionário."), ("This parameter is required.", "Este parâmetro é obrigatório."), ("I found it in the API reference.", "Achei na referência da API."), ("Under the hood, it uses PyTorch.", "Por baixo dos panos, usa PyTorch.")],
    [("Ler a documentação inteira do começo ao fim.", "Comece pelo quickstart e depois busque (Ctrl + F) só o que precisa."), ("Ignorar a palavra <i>deprecated</i>.", "Troque pelo que a documentação recomenda: vai parar de funcionar."), ("Confundir <i>returns</i> com <i>receives</i>.", "<i>returns</i> = devolve; os parâmetros são o que a função recebe.")],
    "<p>No dia a dia: <b>Did you check the docs?</b> (Você olhou a documentação?), <b>According to the docs, ...</b> (Segundo a documentação...), <b>The docs are outdated</b> (A documentação está desatualizada). Colocar o link da documentação no seu PR mostra cuidado.</p>",
    [("<i>“The method raises a KeyError.”</i>:", ["O método levanta um KeyError.", "O método corrige um KeyError.", "O método ignora o KeyError."], 0, "raises = levanta (um erro)."),
     ("Onde estão os parâmetros e o retorno de cada função?", ["Changelog", "API reference", "Quickstart"], 1, "A referência da API detalha cada função."),
     ("<i>deprecated</i> significa:", ["novo", "obrigatório", "ultrapassado, vai ser removido"], 2, "Ainda funciona, mas vai sumir.")],
    ["Quickstart para começar; API reference para detalhes; changelog antes de atualizar.", "returns, raises, default, required e deprecated aparecem em toda documentação.", "Busque com Ctrl + F em vez de ler tudo."],
    "Inglês no trabalho 02: ler artigos de Machine Learning.", "according to the docs")

# --------------------------------------------------------------------------------------------- 02
AULAS["RjG689EwG5g"] = aula_en(
    "As novidades de IA aparecem primeiro em artigos científicos (<i>papers</i>), quase sempre em inglês, no site arXiv. Você não precisa entender cada fórmula para tirar proveito: o segredo é ler em camadas. Primeiro o resumo e as figuras, depois a conclusão e, só se valer a pena, o artigo inteiro.",
    ["conhecer as seções de um artigo (<i>abstract, method, results</i>);", "ler em camadas, do mais rápido ao mais profundo;", "usar as expressões típicas dos artigos (<i>we propose, outperforms, state of the art</i>)."],
    ("Um artigo diz: <i>“Our method outperforms the baseline by 5%.”</i> O que isso significa?", ["O método deles é 5% pior que o de referência.", "O método deles supera o de referência em 5%.", "O método deles é igual ao de referência."], 1,
     ["<i>Outperform</i> é ter desempenho melhor.", "Isso! <i>Baseline</i> é o ponto de comparação; <i>outperform</i> é superar.", "Seria <i>matches</i>."],
     "Baseline = referência para comparar; outperforms = supera."),
    ("Comentando um paper", [
        ("Leo", "Did you read the new paper on retrieval?", "Você leu o artigo novo sobre recuperação?"),
        ("Bia", "Only the abstract and the figures. They propose a new reranking method.", "Só o resumo e as figuras. Eles propõem um novo método de reranking."),
        ("Leo", "Does it outperform the baseline?", "Ele supera a referência?"),
        ("Bia", "Yes, by about 4 points, but the experiments are only in English.", "Sim, em uns 4 pontos, mas os experimentos são só em inglês."),
        ("Leo", "Good point. That's a limitation for our use case.", "Bem lembrado. Isso é uma limitação para o nosso caso."),
    ]),
    "as três formas de leitura que o pesquisador descreve",
    tabela("Leia em camadas", ["Passo", "Seções", "Pergunta que responde"], [
        ["1 · Sobrevoo (5 min)", "título, <i>abstract</i>, figuras", "Sobre o que é? Me interessa?"],
        ["2 · Ideia principal (20 min)", "<i>introduction, conclusion</i>, tabelas de <i>results</i>", "O que eles fizeram e quanto melhorou?"],
        ["3 · Profundo (horas)", "<i>method, experiments</i>, apêndice, código", "Como reproduzir? Onde estão os limites?"],
    ], corpo="<p>A maioria dos artigos só merece o passo 1 ou 2. Sites como <b>paperswithcode</b> ligam o artigo ao código.</p>"),
    [("abstract", "resumo do artigo", "Read the abstract first."), ("we propose", "propomos", "We propose a new method."), ("baseline", "referência de comparação", "It beats the baseline."),
     ("outperforms", "supera", "Our model outperforms GPT-2."), ("state of the art (SOTA)", "o melhor resultado atual", "It achieves state-of-the-art results."), ("limitations", "limitações", "The authors discuss the limitations.")],
    [("We propose a new attention mechanism.", ["Propomos um novo mecanismo de atenção", "Rejeitamos a atenção", "Copiamos o mecanismo"], 0, "Propomos um novo mecanismo de atenção."),
     ("The model outperforms the baseline.", ["O modelo supera a referência", "O modelo perde para a referência", "O modelo é a referência"], 0, "O modelo supera a referência."),
     ("The authors discuss the limitations.", ["Os autores discutem as limitações", "Os autores escondem os erros", "Os autores terminam o artigo"], 0, "Os autores discutem as limitações."),
     ("Read the abstract first.", "4 palavras"), ("It achieves state of the art results.", "7 palavras")],
    [("I read the abstract and the figures.", "Li o resumo e as figuras."), ("They propose a new training method.", "Eles propõem um novo método de treino."), ("It outperforms the baseline by five percent.", "Supera a referência em cinco por cento."), ("What are the limitations?", "Quais são as limitações?")],
    [("Tentar entender cada fórmula na primeira leitura.", "Primeiro o resumo e as figuras; as fórmulas, só no passo 3."), ("Confundir <i>abstract</i> com “abstrato”.", "Em artigos, <i>abstract</i> é o resumo."), ("Acreditar no resultado sem ler as limitações.", "Procure a seção <i>limitations</i> e os dados usados nos testes.")],
    "<p>Em entrevistas e reuniões: <b>I read a paper that proposes ...</b>, <b>It beats the baseline on ...</b>, <b>The main limitation is ...</b>. Ler um artigo por semana, no modo sobrevoo, já te deixa à frente da maioria.</p>",
    [("Qual seção ler primeiro?", ["Method", "Abstract", "Appendix"], 1, "O resumo diz se vale continuar."),
     ("<i>baseline</i> é:", ["o resultado final", "a referência de comparação", "o código do artigo"], 1, "O ponto de partida para comparar."),
     ("<i>“It achieves state-of-the-art results”</i>:", ["Consegue os melhores resultados atuais.", "Tem resultados ruins.", "É um artigo de arte."], 0, "SOTA = o melhor atual.")],
    ["Leia em camadas: resumo e figuras, depois conclusão e resultados, por fim o método.", "abstract, we propose, baseline, outperforms, state of the art, limitations.", "Sempre procure as limitações."],
    "Inglês no trabalho 03: escrever o README do seu projeto.", "we propose")

# --------------------------------------------------------------------------------------------- 03
AULAS["fDJNt67xdvQ"] = aula_en(
    "O README é a primeira coisa que um recrutador vê no seu GitHub, e muitas vezes a única. Escrito em inglês, ele abre portas para vagas de fora. Um bom README responde em segundos: o que o projeto faz, por que importa, como rodar e qual foi o resultado.",
    ["montar a estrutura de um bom README;", "escrever frases curtas e diretas no imperativo (<i>Install, Run, Clone</i>);", "descrever resultados com números."],
    ("Qual é a melhor primeira frase para o README de um classificador de spam?", ["“This is my project.”", "“A spam classifier for Portuguese SMS messages that reaches 97% accuracy.”", "“Hello! Welcome to my repository!”"], 1,
     ["Não diz nada sobre o projeto.", "Isso! O quê, para quem e o resultado, numa frase.", "Simpático, mas não informa nada."],
     "A primeira linha do README é como a vitrine: precisa dizer o que é e por que vale a pena."),
    ("Revisando um README", [
        ("Rafa", "Your README is great, but I didn't understand how to run the project.", "Seu README está ótimo, mas não entendi como rodar o projeto."),
        ("Joana", "Oh, I forgot the installation section.", "Ah, esqueci a seção de instalação."),
        ("Rafa", "Add the commands step by step. And maybe a screenshot.", "Coloque os comandos passo a passo. E talvez uma captura de tela."),
        ("Joana", "Good idea. Should I mention the accuracy?", "Boa ideia. Devo mencionar a acurácia?"),
        ("Rafa", "Definitely. Numbers make it convincing.", "Com certeza. Números deixam convincente."),
    ]),
    "o que a pessoa coloca no topo do README e por quê",
    nota("A estrutura de um bom README", [
        ("# Project name", "título + uma frase", "<i>A spam classifier for Portuguese SMS messages.</i>"),
        ("## Demo", "imagem ou GIF", "Mostre funcionando antes de explicar."),
        ("## Features", "o que faz", "Lista curta, verbos no presente: <i>Detects spam in real time.</i>"),
        ("## Installation", "como instalar", "<i>Clone the repo, create a virtual environment, install the requirements.</i>"),
        ("## Usage", "como usar", "Um comando ou exemplo de código."),
        ("## Results", "números", "<i>97% accuracy on 5,000 messages.</i>"),
        ("## What I learned", "aprendizados", "<i>I learned how to handle imbalanced data.</i>"),
    ], rot="O esqueleto"),
    [("install", "instalar", "Install the requirements."), ("run", "rodar, executar", "Run the app with this command."), ("clone the repo", "clonar o repositório", "First, clone the repo."),
     ("features", "funcionalidades", "Main features: search and export."), ("requirements", "dependências", "Python 3.12 is required."), ("contributing", "como contribuir", "Pull requests are welcome.")],
    [("Clone the repo and install the requirements.", ["Clone o repositório e instale as dependências", "Apague o repositório", "Compre os requisitos"], 0, "Clone o repositório e instale as dependências."),
     ("Run the app with this command.", ["Rode o aplicativo com este comando", "Corra com o aplicativo", "Apague este comando"], 0, "Rode o aplicativo com este comando."),
     ("Pull requests are welcome.", ["Pull requests são bem-vindos", "Pull requests são proibidos", "Puxe os pedidos"], 0, "Pull requests são bem-vindos."),
     ("Install the requirements.", "3 palavras"), ("It reaches ninety seven percent accuracy.", "6 palavras")],
    [("This project detects spam in text messages.", "Este projeto detecta spam em mensagens de texto."), ("Clone the repo and run the script.", "Clone o repositório e rode o script."), ("It reaches ninety-seven percent accuracy.", "Atinge noventa e sete por cento de acurácia."), ("I learned how to deploy a model.", "Aprendi a colocar um modelo no ar.")],
    [("Escrever <i>Run the next command</i> sem mostrar o comando.", "Mostre o comando num bloco de código."), ("Usar o README como diário (“primeiro eu tentei...”).", "Seja direto: o que é, como usar, resultado."), ("Traduzir “rodar” como <i>to turn</i>.", "Rodar um programa é <i>to run</i>.")],
    "<p>Use o imperativo nas instruções (<b>Install</b>, <b>Run</b>, <b>Open</b>) e o presente nas descrições (<b>It detects</b>, <b>It uses</b>). Peça a um assistente de IA para revisar o inglês, mas mantenha os números e as decisões que são suas.</p>",
    [("Qual seção explica como instalar?", ["Results", "Installation", "Contributing"], 1, "Installation."),
     ("Instrução no README:", ["You must to install.", "Install the requirements.", "Installing requirements you."], 1, "Imperativo: Install ..."),
     ("O que deixa o README convincente?", ["Números de resultado", "Muitos emojis", "Texto longo"], 0, "Resultados com números.")],
    ["Primeira linha: o que é, para quem e o resultado.", "Seções: Demo, Features, Installation, Usage, Results, What I learned.", "Imperativo nas instruções, presente nas descrições."],
    "Inglês no trabalho 04: pull requests e code review.", "clone the repo")

# --------------------------------------------------------------------------------------------- 04
AULAS["DWCO02rBrAg"] = aula_en(
    "Em times internacionais, quase toda conversa técnica acontece por escrito nos pull requests (PRs): você descreve a sua mudança e outras pessoas revisam (code review). O inglês aqui é educado e direto, com expressões fixas que todo desenvolvedor reconhece, como <i>LGTM</i>, <i>nit</i> e <i>Could you ...?</i>.",
    ["escrever a descrição de um pull request;", "pedir mudanças com educação (<i>Could you ...?, What do you think about ...?</i>);", "entender as siglas de code review (<i>LGTM, nit, WIP</i>)."],
    ("Um revisor escreveu no seu PR: <i>“nit: rename this variable.”</i> O que ele quer dizer?", ["É um erro grave que bloqueia o PR.", "É um detalhe pequeno, uma sugestão sem urgência.", "Ele não entendeu o código."], 1,
     ["Erros graves não vêm marcados como nit.", "Isso! <i>nit</i> (de <i>nitpick</i>) é um detalhe pequeno: corrija se concordar.", "Ele está sugerindo uma melhoria."],
     "nit = detalhe pequeno; LGTM = looks good to me (pode aprovar)."),
    ("Uma revisão de código", [
        ("Rev", "Thanks for the PR! Could you add a test for the empty list case?", "Obrigado pelo PR! Você pode adicionar um teste para o caso da lista vazia?"),
        ("Dev", "Sure, good catch. I'll add it now.", "Claro, bem observado. Vou adicionar agora."),
        ("Rev", "Also, nit: this function name is a bit confusing.", "Também, detalhe: o nome dessa função está um pouco confuso."),
        ("Dev", "What do you think about calling it load_documents?", "O que você acha de chamá-la de load_documents?"),
        ("Rev", "Sounds good. LGTM after that!", "Parece bom. Aprovado depois disso!"),
    ]),
    "as frases educadas que a pessoa usa para pedir mudanças",
    tabela("Frases prontas para PRs", ["Situação", "Em inglês"], [
        ["Descrever o PR", "<i>This PR adds ... / fixes ... / refactors ...</i>"],
        ["Pedir uma mudança", "<i>Could you ...? / Would it make sense to ...?</i>"],
        ["Sugerir sem impor", "<i>What do you think about ...? / Consider ...</i>"],
        ["Perguntar", "<i>Why did you choose ...? / I'm not sure I understand ...</i>"],
        ["Concordar", "<i>Good catch! / Fair point. / Done.</i>"],
        ["Aprovar", "<i>LGTM (looks good to me) / Approved.</i>"],
    ], corpo="<p>Siglas comuns: <b>WIP</b> (work in progress, ainda não terminei), <b>PTAL</b> (please take another look, dê outra olhada), <b>nit</b> (detalhe).</p>"),
    [("pull request (PR)", "pedido para juntar código", "I opened a PR."), ("code review", "revisão de código", "Thanks for the code review!"), ("Could you ...?", "Você poderia ...?", "Could you add a test?"),
     ("good catch", "bem observado", "Good catch, I'll fix it."), ("LGTM", "parece bom para mim (aprovado)", "LGTM, ship it!"), ("nit", "detalhe pequeno", "nit: missing space here.")],
    [("Could you add a test for this case?", ["Você poderia adicionar um teste para este caso?", "Você testou este caso?", "Apague este teste"], 0, "Você poderia adicionar um teste para este caso?"),
     ("Good catch, I'll fix it.", ["Bem observado, vou corrigir", "Boa pegada, vou quebrar", "Pegue isso"], 0, "Bem observado, vou corrigir."),
     ("This PR fixes the login bug.", ["Este PR corrige o erro do login", "Este PR cria o login", "Este PR apaga o login"], 0, "Este PR corrige o erro do login."),
     ("Looks good to me.", "4 palavras"), ("What do you think about this?", "6 palavras")],
    [("This PR adds caching to the search endpoint.", "Este PR adiciona cache ao endpoint de busca."), ("Could you take another look?", "Você poderia dar outra olhada?"), ("Good catch, I'll fix it.", "Bem observado, vou corrigir."), ("What do you think about renaming this function?", "O que você acha de renomear esta função?")],
    [("<i>Change this.</i> (soa rude)", "<i>Could you change this?</i> ou <i>What do you think about ...?</i>"), ("Descrição de PR vazia.", "Escreva o que muda, por que muda e como testar."), ("Responder a um comentário só com “ok”.", "<i>Done</i>, <i>Fixed in the last commit</i> ou explique se discordar.")],
    "<p>Uma boa descrição de PR tem três partes: <b>What</b> (o que muda), <b>Why</b> (por que) e <b>How to test</b> (como testar). Contribuir para projetos open source em inglês é um dos melhores itens que você pode colocar no currículo.</p>",
    [("<i>LGTM</i> significa:", ["Looks good to me", "Let's go to the meeting", "Large git tree merge"], 0, "Aprovado."),
     ("Forma educada de pedir uma mudança:", ["Change it now.", "Could you change this?", "You must change."], 1, "Could you ...?"),
     ("O que costuma ter numa boa descrição de PR?", ["What, Why e How to test", "Só o título", "Uma piada"], 0, "O que, por que e como testar.")],
    ["Descreva o PR: what, why, how to test.", "Peça com Could you ...? e What do you think about ...?", "LGTM, nit, WIP, PTAL, good catch."],
    "Inglês no trabalho 05: e-mails e mensagens de trabalho.", "could you take a look")

# --------------------------------------------------------------------------------------------- 05
AULAS["qXCWEOIOYhc"] = aula_en(
    "Trabalhando remoto para uma empresa de fora, a maior parte da comunicação é escrita: e-mails, Slack, Teams. Mensagens curtas, claras e educadas fazem você parecer profissional, mesmo com um inglês ainda em construção. Existem fórmulas prontas para abrir, pedir, avisar e fechar.",
    ["abrir e fechar e-mails com o tom certo;", "fazer pedidos e dar avisos de forma clara;", "escrever mensagens curtas no chat do trabalho."],
    ("Você vai se atrasar para entregar uma tarefa. Qual mensagem é a mais profissional?", ["“Sorry, task late.”", "“Heads up: I need one more day to finish the report. I'll send it by Friday.”", "“I can't do it.”"], 1,
     ["Curta demais e sem plano.", "Isso! Avisa cedo, diz o motivo em uma linha e dá um novo prazo.", "Sem contexto e sem solução."],
     "Heads up = aviso antecipado. Sempre traga um novo prazo."),
    ("Mensagens no Slack", [
        ("Sam", "Hi João, quick question: is the API ready for testing?", "Oi João, pergunta rápida: a API está pronta para testar?"),
        ("João", "Hi Sam! Almost. Heads up: I need until tomorrow to fix one bug.", "Oi Sam! Quase. Aviso: preciso até amanhã para corrigir um bug."),
        ("Sam", "No worries. Could you let me know when it's done?", "Sem problemas. Você pode me avisar quando terminar?"),
        ("João", "Sure, I'll ping you tomorrow morning.", "Claro, te chamo amanhã de manhã."),
        ("Sam", "Thanks a lot!", "Muito obrigado!"),
    ]),
    "como abrir e fechar um e-mail profissional",
    tabela("Fórmulas prontas", ["Para", "E-mail (mais formal)", "Chat (mais leve)"], [
        ["Abrir", "<i>Hi Sarah, I hope you're doing well.</i>", "<i>Hi Sam!</i>"],
        ["Pedir", "<i>Could you please send me ...?</i>", "<i>Could you share ...?</i>"],
        ["Avisar", "<i>I wanted to let you know that ...</i>", "<i>Heads up: ...</i>"],
        ["Dar retorno", "<i>Following up on my last email, ...</i>", "<i>Any updates on ...?</i>"],
        ["Anexar", "<i>Please find attached the report.</i>", "<i>Here's the file.</i>"],
        ["Fechar", "<i>Best regards, / Thanks in advance,</i>", "<i>Thanks!</i>"],
    ], corpo="<p>No chat: uma ideia por mensagem, nada de “Hi” sozinho esperando resposta. Escreva a pergunta inteira de uma vez.</p>"),
    [("heads up", "aviso antecipado", "Heads up: the server will restart."), ("follow up", "dar retorno, retomar", "Just following up on this."), ("ASAP", "o quanto antes", "Please reply ASAP."),
     ("ping someone", "chamar alguém (no chat)", "I'll ping you later."), ("attached", "em anexo", "The file is attached."), ("Thanks in advance", "Obrigado desde já", "Thanks in advance for your help.")],
    [("Heads up: the deploy is delayed.", ["Aviso: o deploy está atrasado", "Cabeça erguida: o deploy acabou", "O deploy foi cancelado"], 0, "Aviso: o deploy está atrasado."),
     ("Could you share the slides?", ["Você pode compartilhar os slides?", "Você fez os slides?", "Apague os slides"], 0, "Você pode compartilhar os slides?"),
     ("I'll ping you tomorrow.", ["Vou te chamar amanhã", "Vou te pagar amanhã", "Te vi amanhã"], 0, "Vou te chamar amanhã."),
     ("Please find attached the report.", "5 palavras"), ("Thanks in advance.", "3 palavras")],
    [("Hi Sarah, I hope you're doing well.", "Oi Sarah, espero que esteja bem."), ("Could you please send me the data?", "Você poderia, por favor, me enviar os dados?"), ("Heads up: I need one more day.", "Aviso: preciso de mais um dia."), ("Best regards, João.", "Atenciosamente, João.")],
    [("<i>I'm waiting your answer.</i>", "<i>I'm waiting <b>for</b> your answer</i> ou <i>Looking forward to your reply.</i>"), ("Mandar só “Hi” no chat e esperar.", "Escreva a pergunta inteira na mesma mensagem."), ("Traduzir “Segue em anexo” palavra por palavra.", "<i>Please find attached ...</i> ou <i>I've attached ...</i>")],
    "<p>Dica de quem trabalha remoto: deixe o rascunho pronto, peça a um assistente de IA para <b>revisar o tom e a gramática</b> e compare com o que você escreveu. Você aprende os ajustes e, com o tempo, precisa cada vez menos da revisão.</p>",
    [("<i>Heads up</i> serve para:", ["dar um aviso antecipado", "pedir desculpas", "encerrar o e-mail"], 0, "Aviso antecipado."),
     ("Forma correta:", ["I'm waiting your answer.", "I'm waiting for your answer.", "I wait your answer."], 1, "wait for."),
     ("Boa prática no chat:", ["Mandar “Hi” e esperar.", "Escrever a pergunta inteira de uma vez.", "Usar só emojis."], 1, "Uma mensagem completa.")],
    ["Abra com Hi + nome; feche com Thanks ou Best regards.", "Could you please ...?, Heads up, Following up.", "No chat: mensagem completa, uma ideia por vez."],
    "Inglês no trabalho 06: daily stand-up e reuniões.", "heads up")

# --------------------------------------------------------------------------------------------- 06
AULAS["MsxcpZr1LpM"] = aula_en(
    "Times de tecnologia fazem a <i>daily stand-up</i>: uma reunião curta, todo dia, em que cada pessoa diz o que fez ontem, o que vai fazer hoje e se tem algum bloqueio. Como é sempre a mesma estrutura, é o melhor treino de inglês falado que existe no trabalho: dá para preparar as frases.",
    ["dar a sua atualização no formato <i>yesterday / today / blockers</i>;", "falar de bloqueios e pedir ajuda;", "participar de reuniões com frases curtas (<i>Can you repeat that?, Let me share my screen</i>)."],
    ("Na daily, alguém diz: <i>“I'm blocked by the API keys.”</i> O que está acontecendo?", ["A pessoa terminou tudo.", "A pessoa não consegue avançar porque está esperando as chaves da API.", "A pessoa bloqueou a API."], 1,
     ["Seria <i>I'm done</i>.", "Isso! <i>Blocked by</i> = impedido de avançar por causa de algo.", "Ela é que está bloqueada, não a API."],
     "Blocker = o que te impede de avançar. Falar dele cedo é sinal de profissionalismo."),
    ("A daily do time", [
        ("Lead", "Good morning, everyone. João, do you want to start?", "Bom dia a todos. João, quer começar?"),
        ("João", "Sure. Yesterday I finished the data cleaning script.", "Claro. Ontem terminei o script de limpeza de dados."),
        ("João", "Today I'm going to work on the evaluation of the model.", "Hoje vou trabalhar na avaliação do modelo."),
        ("João", "I'm blocked by the access to the database. Could someone help me with that?", "Estou travado pelo acesso ao banco de dados. Alguém pode me ajudar com isso?"),
        ("Lead", "I'll check it after the meeting. Thanks, João!", "Vejo isso depois da reunião. Obrigado, João!"),
    ]),
    "as três partes da atualização de cada pessoa",
    nota("O roteiro da sua atualização", [
        ("Yesterday I ...", "o que fiz ontem", "<i>Yesterday I finished the API endpoint.</i>"),
        ("Today I'm going to ...", "o que farei hoje", "<i>Today I'm going to write the tests.</i>"),
        ("I'm blocked by ... / No blockers.", "bloqueios", "<i>I'm blocked by the API keys.</i>"),
        ("Could someone help me with ...?", "pedir ajuda", "<i>Could someone help me with the deploy?</i>"),
        ("Can you repeat that, please?", "não entendeu", "Sem vergonha: todo mundo pede."),
        ("Let me share my screen.", "mostrar algo", "Útil quando falar fica difícil."),
    ], rot="Prepare antes da reunião"),
    [("stand-up / daily", "reunião diária curta", "See you at the daily."), ("blocker", "bloqueio, impedimento", "Any blockers?"), ("I'm working on", "estou trabalhando em", "I'm working on the dashboard."),
     ("almost done", "quase pronto", "The report is almost done."), ("share my screen", "compartilhar minha tela", "Let me share my screen."), ("follow up after the meeting", "ver depois da reunião", "Let's follow up after the meeting.")],
    [("Yesterday I finished the tests.", ["Ontem terminei os testes", "Amanhã vou terminar os testes", "Ontem comecei os testes"], 0, "Ontem terminei os testes."),
     ("Today I'm going to work on the API.", ["Hoje vou trabalhar na API", "Hoje terminei a API", "Ontem trabalhei na API"], 0, "Hoje vou trabalhar na API."),
     ("No blockers for me.", ["Nenhum bloqueio para mim", "Estou bloqueado", "Sem tempo para mim"], 0, "Nenhum bloqueio para mim."),
     ("Can you repeat that please?", "5 palavras"), ("Let me share my screen.", "5 palavras")],
    [("Yesterday I finished the data pipeline.", "Ontem terminei o pipeline de dados."), ("Today I'm going to write the tests.", "Hoje vou escrever os testes."), ("I'm blocked by the database access.", "Estou travado pelo acesso ao banco."), ("Can you repeat that, please?", "Pode repetir, por favor?")],
    [("<i>Yesterday I finish</i> (sem passado).", "<i>Yesterday I finish<b>ed</b></i>."), ("Contar todos os detalhes técnicos na daily.", "Seja breve (30 a 60 segundos); detalhes depois: <i>Let's follow up after the meeting.</i>"), ("Esconder o bloqueio por vergonha.", "Diga cedo: <i>I'm blocked by ...</i>. Bloqueio escondido vira atraso.")],
    "<p>Antes de cada daily, escreva suas 3 frases (yesterday, today, blockers) e leia em voz alta uma vez. Em poucas semanas, você vai falar sem papel. Esse mesmo formato serve para relatórios semanais por escrito.</p>",
    [("As três partes da atualização:", ["yesterday, today, blockers", "hello, goodbye, thanks", "code, test, deploy"], 0, "Ontem, hoje, bloqueios."),
     ("Forma correta:", ["Yesterday I finish the API.", "Yesterday I finished the API.", "Yesterday I am finish the API."], 1, "Passado: finished."),
     ("Não entendeu o que foi dito. Você diz:", ["Can you repeat that, please?", "Be quiet.", "I'm blocked."], 0, "Peça para repetir.")],
    ["Yesterday I ... / Today I'm going to ... / I'm blocked by ...", "Seja breve; detalhes depois da reunião.", "Can you repeat that? e Let me share my screen salvam reuniões."],
    "Inglês no trabalho 07: explicar o seu projeto em 2 minutos.", "I'm blocked by")

# --------------------------------------------------------------------------------------------- 07
AULAS["VmsJVjKIWSg"] = aula_en(
    "Em quase toda entrevista técnica vem a pergunta: <i>“Walk me through a project you're proud of.”</i> (Me conte, passo a passo, sobre um projeto do qual você se orgulha.) Quem responde de forma organizada, em 2 minutos, mostra que entende o que fez. Existe uma estrutura simples que funciona sempre: problema, solução, resultado e aprendizado.",
    ["organizar a resposta em problema, solução, resultado e aprendizado;", "usar o passado para contar o que fez (<i>I built, I used, I improved</i>);", "falar de resultados com números."],
    ("O entrevistador diz: <i>“Walk me through your project.”</i> O que ele quer?", ["Que você mostre o código linha por linha.", "Que você explique o projeto do começo ao fim, de forma organizada.", "Que você ande pela sala."], 1,
     ["Ele quer a visão geral primeiro; o código, só se pedir.", "Isso! <i>Walk me through</i> = me guie pelo assunto, passo a passo.", "É uma expressão: “me conduza por”."],
     "Walk me through = explique passo a passo."),
    ("Na entrevista", [
        ("Interviewer", "Can you walk me through a project you're proud of?", "Pode me contar sobre um projeto do qual você se orgulha?"),
        ("João", "Sure. Small stores in my city lose time answering the same questions on WhatsApp.", "Claro. Lojas pequenas da minha cidade perdem tempo respondendo as mesmas perguntas no WhatsApp."),
        ("João", "So I built a chatbot with RAG that answers based on the store's catalog.", "Então construí um chatbot com RAG que responde com base no catálogo da loja."),
        ("João", "It now answers about seventy percent of the questions without a human.", "Hoje ele responde cerca de setenta por cento das perguntas sem um humano."),
        ("João", "I learned a lot about evaluation: at first, I had no way to measure quality.", "Aprendi muito sobre avaliação: no começo, eu não tinha como medir a qualidade."),
        ("Interviewer", "Interesting. How did you evaluate it?", "Interessante. Como você avaliou?"),
    ]),
    "a ordem em que a pessoa organiza a explicação do projeto",
    tabela("A estrutura de 2 minutos", ["Parte", "Tempo", "Frases úteis"], [
        ["Problem", "20 s", "<i>The problem was that ... / Small stores were losing time ...</i>"],
        ["Solution", "40 s", "<i>I built ... using ... / I chose ... because ...</i>"],
        ["Result", "30 s", "<i>It reduced ... by 30% / It now answers 70% of ...</i>"],
        ["Learning", "30 s", "<i>I learned ... / If I did it again, I would ...</i>"],
    ], corpo="<p>Termine com algo que convide perguntas, como um desafio: <i>The hardest part was ...</i>. O entrevistador costuma seguir por aí, e você já está preparado.</p>"),
    [("walk me through", "me explique passo a passo", "Walk me through your solution."), ("I built", "eu construí", "I built a recommendation system."), ("I chose ... because", "escolhi ... porque", "I chose FastAPI because it's simple."),
     ("it reduced", "reduziu", "It reduced the response time by half."), ("the hardest part was", "a parte mais difícil foi", "The hardest part was cleaning the data."), ("if I did it again", "se eu fizesse de novo", "If I did it again, I'd add tests earlier.")],
    [("I built a chatbot using RAG.", ["Construí um chatbot usando RAG", "Comprei um chatbot", "Vou construir um chatbot"], 0, "Construí um chatbot usando RAG."),
     ("The hardest part was the evaluation.", ["A parte mais difícil foi a avaliação", "A avaliação foi fácil", "A parte mais dura é o código"], 0, "A parte mais difícil foi a avaliação."),
     ("It reduced the costs by thirty percent.", ["Reduziu os custos em trinta por cento", "Aumentou os custos", "Custou trinta por cento"], 0, "Reduziu os custos em trinta por cento."),
     ("Walk me through your project.", "5 palavras"), ("I chose Python because it is simple.", "7 palavras")],
    [("The problem was that customers waited too long.", "O problema era que os clientes esperavam demais."), ("I built a chatbot using RAG and FastAPI.", "Construí um chatbot usando RAG e FastAPI."), ("It now answers seventy percent of the questions.", "Hoje ele responde setenta por cento das perguntas."), ("If I did it again, I would add tests earlier.", "Se eu fizesse de novo, colocaria testes mais cedo.")],
    [("Começar pela tecnologia (“I used LangChain and ...”).", "Comece pelo problema: o entrevistador precisa saber por que o projeto existe."), ("<i>I build</i> para algo que já terminou.", "Projeto concluído vai no passado: <i>I built, I used, I learned</i>."), ("Não ter nenhum número.", "Meça algo: tempo, acerto, custo, usuários. Até “5 amigos usaram por um mês” vale.")],
    "<p>Prepare esta resposta para os 2 ou 3 projetos do seu GitHub. Grave-se em vídeo (é o projeto prático deste módulo), ouça, ajuste e grave de novo. Na terceira vez, sai natural.</p>",
    [("A ordem recomendada é:", ["Solution, Problem, Learning, Result", "Problem, Solution, Result, Learning", "Learning, Result, Solution, Problem"], 1, "Problema primeiro."),
     ("Para um projeto já terminado, use:", ["I build a chatbot.", "I built a chatbot.", "I will build a chatbot."], 1, "Passado: built."),
     ("O que deixa a resposta mais forte?", ["Números de resultado", "Muitos nomes de bibliotecas", "Falar rápido"], 0, "Resultados medidos.")],
    ["Problem, Solution, Result, Learning, em cerca de 2 minutos.", "Passado para o que você fez: I built, I chose, I learned.", "Sempre um número no resultado."],
    "Inglês no trabalho 08: “Tell me about yourself” e perguntas comportamentais.", "walk me through")

# --------------------------------------------------------------------------------------------- 08
AULAS["RtXqF1_rKMk"] = aula_en(
    "A entrevista quase sempre começa com <i>“Tell me about yourself.”</i> Não é para contar a sua vida inteira: é um resumo profissional de 1 minuto. E logo depois vêm as perguntas comportamentais (<i>“Tell me about a time when ...”</i>), que se respondem com o método <b>STAR</b>. Com as duas preparadas, você começa a entrevista confiante. E se você mudou de carreira, como o João do diálogo, que saiu da obra e virou desenvolvedor, isso é um diferencial: conte com orgulho.",
    ["responder <i>Tell me about yourself</i> no formato presente, passado e futuro;", "responder perguntas comportamentais com o método STAR;", "transformar a sua trajetória num ponto forte."],
    ("Qual é o melhor começo para <i>“Tell me about yourself”</i> numa vaga de desenvolvedor de IA?", ["“I was born in 1995 in a small town...”", "“I'm a Python developer focused on building applications with LLMs.”", "“I don't know, what do you want to know?”"], 1,
     ["Começar pela infância gasta o tempo com o que não importa para a vaga.", "Isso! Comece pelo presente profissional, ligado à vaga.", "Mostra falta de preparo."],
     "Presente (quem sou hoje), passado (como cheguei aqui), futuro (por que esta vaga)."),
    ("Começo da entrevista", [
        ("Interviewer", "So, tell me about yourself.", "Então, me fale sobre você."),
        ("João", "I'm a Python developer focused on AI applications, especially RAG and chatbots.", "Sou desenvolvedor Python focado em aplicações de IA, especialmente RAG e chatbots."),
        ("João", "Before tech, I worked for ten years in construction, where I learned to solve real problems under pressure.", "Antes da tecnologia, trabalhei dez anos na construção civil, onde aprendi a resolver problemas reais sob pressão."),
        ("João", "I taught myself programming and built projects that are on my GitHub.", "Aprendi programação sozinho e construí projetos que estão no meu GitHub."),
        ("João", "Now I'm looking for a role where I can build AI products with a strong team.", "Agora procuro uma vaga em que eu construa produtos de IA com um time forte."),
    ]),
    "a estrutura presente, passado e futuro que o professor ensina",
    [tabela("“Tell me about yourself”: presente, passado e futuro", ["Parte", "O que dizer", "Exemplo"], [
        ["Present", "quem você é hoje, profissionalmente", "<i>I'm a Python developer focused on AI applications.</i>"],
        ["Past", "como chegou aqui (experiências que importam)", "<i>Before tech, I worked in construction for ten years ...</i>"],
        ["Future", "o que você busca e por que esta vaga", "<i>Now I'm looking for a role where ...</i>"],
     ], corpo="<p>Cerca de 1 minuto. A sua mudança de carreira mostra disciplina, autonomia e resiliência: apresente como força, não como desculpa.</p>"),
     nota("Perguntas comportamentais: o método STAR", [
        ("S · Situation", "o contexto", "<i>In my last project, the API was too slow.</i>"),
        ("T · Task", "o seu papel", "<i>I was responsible for improving the response time.</i>"),
        ("A · Action", "o que VOCÊ fez", "<i>I added a cache and moved the heavy work to a queue.</i>"),
        ("R · Result", "o resultado, com número", "<i>The response time dropped from 4 seconds to 800 milliseconds.</i>"),
     ], rot="Para “Tell me about a time when ...”")],
    [("tell me about yourself", "me fale sobre você", "Let's start: tell me about yourself."), ("I'm focused on", "sou focado em", "I'm focused on LLM applications."), ("I taught myself", "aprendi sozinho", "I taught myself Python."),
     ("career change", "mudança de carreira", "I made a career change at thirty."), ("I was responsible for", "eu era responsável por", "I was responsible for the deploy."), ("I'm looking for", "estou procurando", "I'm looking for a remote role.")],
    [("I taught myself programming.", ["Aprendi programação sozinho", "Ensinei programação para mim e outros", "Odeio programação"], 0, "Aprendi programação sozinho."),
     ("I made a career change at thirty.", ["Mudei de carreira aos trinta", "Troquei de carro aos trinta", "Mudei de casa aos trinta"], 0, "Mudei de carreira aos trinta."),
     ("I was responsible for the deploy.", ["Eu era responsável pelo deploy", "Eu culpei o deploy", "O deploy foi responsável"], 0, "Eu era responsável pelo deploy."),
     ("Tell me about yourself.", "4 palavras"), ("I'm looking for a remote role.", "6 palavras")],
    [("I'm a Python developer focused on AI.", "Sou desenvolvedor Python focado em IA."), ("Before tech, I worked in construction for ten years.", "Antes da tecnologia, trabalhei dez anos na construção."), ("I taught myself programming.", "Aprendi programação sozinho."), ("Now I'm looking for a role where I can grow.", "Agora procuro uma vaga em que eu possa crescer.")],
    [("Contar a vida desde a infância.", "Comece pelo presente profissional; o passado só no que ajuda a vaga."), ("Pedir desculpas pela mudança de carreira.", "Apresente como força: <i>In construction, I learned to ...</i>"), ("Responder STAR com “we” o tempo todo.", "Mostre o que <b>você</b> fez: <i>I added, I decided, I measured.</i>")],
    "<p>Escreva a sua resposta de <i>Tell me about yourself</i> e 3 histórias STAR (um problema que você resolveu, um erro que cometeu e corrigiu, uma vez que aprendeu algo rápido). Treine em voz alta com um assistente de IA fazendo o papel de entrevistador: <i>Act as an interviewer for an AI developer role and ask me follow-up questions.</i></p>",
    [("A estrutura recomendada para <i>Tell me about yourself</i>:", ["Past, Present, Future", "Present, Past, Future", "Future only"], 1, "Comece pelo presente."),
     ("No STAR, a letra A é:", ["Action: o que você fez", "Answer", "Ambition"], 0, "Sua ação."),
     ("Como apresentar uma mudança de carreira?", ["Como desculpa.", "Como força: o que você trouxe da experiência anterior.", "Escondendo."], 1, "Experiência vira diferencial.")],
    ["Tell me about yourself: presente, passado e futuro, em cerca de 1 minuto.", "Comportamentais: STAR, com o que VOCÊ fez e um número no resultado.", "A sua trajetória é um diferencial: conte com orgulho."],
    "Revisão: grave o vídeo de 2 minutos sobre o seu projeto (projeto do Módulo 7).", "tell me about yourself")
