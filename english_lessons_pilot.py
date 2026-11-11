# -*- coding: utf-8 -*-
"""
Piloto das Aulas Visuais da trilha de Inglês (3 aulas de níveis diferentes do curso EnglishBay):
  - Módulo 1 · Aula 01 "Cumprimentos, apresentações e despedidas"  (0HHnezXSKnI)
  - Módulo 2 · Aula 09 "O que você está fazendo?" (present continuous) (Y-M_0XQxNqs)
  - Módulo 4 · Aula 04 "Superlativos"                               (HeGr10ZcxoQ)

Cada aula complementa o vídeo do curso: trechos com missão (escolhidos lendo as legendas),
diálogo com áudio, vocabulário, escuta/ditado, fala com reconhecimento de voz, armadilhas
de brasileiro e uma ponte com o inglês usado em tecnologia e IA.

As aulas são ligadas pelo videoId da playlist (english_playlist.json).
"""

# ---------------------------------------------------------------------------
# Módulo 1 · Aula 01 · Cumprimentos, apresentações e despedidas
# ---------------------------------------------------------------------------
PILOT_GREETINGS = {
    "v": 2,
    "duracao": 40,
    "gancho": r"""Primeira reunião com um time de fora. A câmera liga e alguém diz: “<i>Hi! I'm Sarah. Nice to meet you!</i>”. Os primeiros 10 segundos de qualquer conversa em inglês são sempre os mesmos: cumprimentar, dizer o nome, perguntar como a pessoa está e se despedir. Quem domina esse roteiro começa a conversa tranquilo.""",
    "objetivos": [
        "cumprimentar no horário certo (e não errar o <i>good night</i>);",
        "dizer seu nome e perguntar o da outra pessoa;",
        "responder e devolver o <i>How are you?</i>;",
        "se despedir de forma natural, inclusive num e-mail ou chat de trabalho.",
    ],
    "prerequisitos": ["Nenhum: esta é a primeira aula do curso."],
    "blocos": [
        {
            "tipo": "palpite",
            "rotulo": "Chute antes de ver",
            "pergunta": "São 20h e você entra numa reunião on-line com o time americano. Como cumprimenta?",
            "opcoes": ["Good night, everyone!", "Good evening, everyone!", "Good afternoon, everyone!"],
            "correta": 1,
            "porques": [
                "Esse é o erro mais comum de brasileiro! <i>Good night</i> é só para <b>despedida</b> (ou na hora de dormir). Chegar dizendo isso soa como “tchau, boa noite”.",
                "Isso! <i>Good evening</i> é o “boa noite” de quem está <b>chegando</b>.",
                "<i>Good afternoon</i> vai do meio-dia até o fim da tarde. Às 20h, já é <i>evening</i>.",
            ],
            "explicacao": "Em português, “boa noite” serve para chegar e para sair. Em inglês são duas expressões diferentes.",
        },
        {
            "tipo": "dialogo",
            "titulo": "Primeiro dia no time",
            "corpo": r"""<p>Ouça a conversa inteira, depois frase por frase (🔊). Tente entender antes de mostrar a tradução.</p>""",
            "falas": [
                {"quem": "Sarah", "en": "Hi! I'm Sarah. What's your name?", "pt": "Oi! Eu sou a Sarah. Qual é o seu nome?"},
                {"quem": "João", "en": "Hello, Sarah. My name's João. Nice to meet you.", "pt": "Olá, Sarah. Meu nome é João. Prazer em conhecer você."},
                {"quem": "Sarah", "en": "Nice to meet you too. How are you?", "pt": "Prazer em conhecer você também. Como você está?"},
                {"quem": "João", "en": "I'm very well, thanks. And you?", "pt": "Estou muito bem, obrigado. E você?"},
                {"quem": "Sarah", "en": "I'm fine. Welcome to the team!", "pt": "Estou bem. Bem-vindo ao time!"},
                {"quem": "João", "en": "Thank you! See you soon.", "pt": "Obrigado! Até breve."},
                {"quem": "Sarah", "en": "Take care!", "pt": "Se cuida!"},
            ],
        },
        {
            "tipo": "video",
            "rotulo": "Com o Teacher Júlio · parte 1",
            "id": "0HHnezXSKnI",
            "inicio": 122,
            "fim": 545,
            "canal": "EnglishBay",
            "titulo_video": "Módulo 01 Aula 01 · Cumprimentos, apresentações e despedidas",
            "corpo": r"""<p>Cumprimentos e formas de tratamento (2:02 a 9:05). Repita em voz alta sempre que ele pedir: <i>repeat</i>.</p>""",
            "missao": [
                "Qual é a diferença entre <i>good evening</i> e <i>good night</i>?",
                "Quando você usa <i>Mr., Mrs.</i> e <i>Miss</i>, e quando usa <i>sir</i> e <i>ma'am</i>?",
                "Que dica de pronúncia ele dá para não confundir <i>ma'am</i> com <i>man</i>?",
            ],
            "respostas": r"""<p><b>1.</b> <i>Good evening</i> é o boa-noite de chegada; <i>good night</i> é o de despedida.</p>
<p><b>2.</b> <i>Mr.</i> (senhor), <i>Mrs.</i> (senhora casada) e <i>Miss</i> (senhorita) vêm <b>com o sobrenome</b>: <i>Hello, Mr. Ford</i>. Quando você não sabe o nome, usa <i>sir</i> e <i>ma'am</i> sozinhos: <i>Good morning, sir</i>.</p>
<p><b>3.</b> Palavra que termina em som de M: <b>feche a boca</b> (<i>ma'am</i>). Terminou em N: língua no céu da boca (<i>man</i>). Trocar uma pela outra é chamar uma senhora de “homem”.</p>""",
        },
        {
            "tipo": "tabela",
            "rotulo": "Organize na cabeça",
            "titulo": "Cumprimentos por horário e formalidade",
            "cabecalho": ["Quando", "Informal", "Formal"],
            "linhas": [
                ["Qualquer hora", "Hi! / Hey!", "Hello."],
                ["Manhã (até 12h)", "Morning!", "Good morning."],
                ["Tarde (12h–18h)", "Afternoon!", "Good afternoon."],
                ["Noite, chegando", "Hi there!", "Good evening."],
                ["Noite, saindo", "Night!", "Good night."],
            ],
        },
        {
            "tipo": "video",
            "rotulo": "Com o Teacher Júlio · parte 2",
            "id": "0HHnezXSKnI",
            "inicio": 913,
            "fim": 1471,
            "canal": "EnglishBay",
            "titulo_video": "Módulo 01 Aula 01 · Cumprimentos, apresentações e despedidas",
            "corpo": r"""<p>“Prazer em conhecer” e “como você está” (15:13 a 24:31). Faça o pingue-pongue com ele em voz alta.</p>""",
            "missao": [
                "Como se responde a <i>Nice to meet you</i>?",
                "Que duas alternativas a <i>nice</i> ele mostra?",
                "Além de <i>And you?</i>, que outras duas formas ele ensina para devolver uma pergunta?",
            ],
            "respostas": r"""<p><b>1.</b> <i>Nice to meet you <b>too</b></i>: a mesma frase com “também” no final.</p>
<p><b>2.</b> <i>Pleased to meet you</i> e <i>Glad to meet you</i>. Ele recomenda que o iniciante foque só no <i>nice</i> primeiro.</p>
<p><b>3.</b> <i>How about you?</i> e <i>What about you?</i>, as duas significando “e quanto a você?”.</p>""",
        },
        {
            "tipo": "vocab",
            "titulo": "Frases para ter na ponta da língua",
            "corpo": r"""<p>Clique no cartão para ver a tradução. Marque <b>Já sei</b> ou <b>Rever</b>: fica salvo.</p>""",
            "cartoes": [
                {"en": "Nice to meet you.", "pt": "Prazer em conhecer você.", "ex": "Hi, I'm Ana. Nice to meet you."},
                {"en": "Nice to meet you too.", "pt": "Prazer em conhecer você também.", "ex": "Nice to meet you too, Ana."},
                {"en": "What's your name?", "pt": "Qual é o seu nome?", "ex": "Hello! What's your name?"},
                {"en": "How are you?", "pt": "Como você está?", "ex": "Hi, Tom! How are you?"},
                {"en": "I'm fine, thanks. And you?", "pt": "Estou bem, obrigado. E você?", "ex": "I'm fine, thanks. And you?"},
                {"en": "See you soon.", "pt": "Até breve.", "ex": "Bye, Sarah! See you soon."},
                {"en": "Take care.", "pt": "Se cuida.", "ex": "Have a good weekend. Take care!"},
                {"en": "I look forward to seeing you again.", "pt": "Estou ansioso para te ver de novo.", "ex": "It was great talking to you. I look forward to seeing you again."},
            ],
        },
        {
            "tipo": "ouvir",
            "titulo": "Escute e responda",
            "corpo": r"""<p>Clique em 🔊 (ou 🐢 para ouvir devagar). Nas três primeiras, escolha; nas duas últimas, escreva exatamente o que ouviu.</p>""",
            "itens": [
                {"frase": "Good evening, Mrs. Lane.", "opcoes": ["Está chegando à noite", "Está indo dormir", "Está cumprimentando de manhã"], "correta": 0, "pt": "Boa noite, senhora Lane."},
                {"frase": "Nice to meet you too.", "opcoes": ["É a primeira frase da conversa", "É uma resposta a “Nice to meet you”", "É uma despedida"], "correta": 1, "pt": "Prazer em conhecer você também."},
                {"frase": "I'm not feeling well.", "opcoes": ["A pessoa está muito bem", "A pessoa não está se sentindo bem", "A pessoa está com pressa"], "correta": 1, "pt": "Não estou me sentindo bem."},
                {"frase": "What's your name?", "dica": "4 palavras (contando a contração)"},
                {"frase": "See you next time.", "dica": "4 palavras"},
            ],
        },
        {
            "tipo": "falar",
            "titulo": "Agora é a sua vez de falar",
            "corpo": r"""<p>Ouça o modelo, clique em 🎙 <b>Falar</b> e diga a frase. O navegador transcreve e mostra em verde as palavras que reconheceu. Na primeira vez ele pede permissão para usar o microfone.</p>""",
            "frases": [
                {"en": "Hi, my name's João. Nice to meet you.", "pt": "Troque João pelo seu nome se quiser (o sistema vai marcar só essa palavra)."},
                {"en": "I'm very well, thanks. How about you?", "pt": "Estou muito bem, obrigado. E você?"},
                {"en": "Good evening, everyone.", "pt": "Boa noite (chegando), pessoal."},
                {"en": "I look forward to seeing you again.", "pt": "Estou ansioso para te ver de novo."},
            ],
        },
        {
            "tipo": "armadilhas",
            "itens": [
                {"erro": "Chegar dizendo <i>Good night</i>.", "correcao": "Chegando é <i>Good evening</i>. <i>Good night</i> é despedida."},
                {"erro": "Pronunciar “<i>nêimi</i>” (name) e “<i>náici</i>” (nice).", "correcao": "Sem o “i” no final: <i>name</i> termina em M (boca fechada) e <i>nice</i> em S."},
                {"erro": "<i>I'm fine, and you?</i> sempre, para tudo.", "correcao": "Está certo, mas varie: <i>I'm good, thanks. How about you?</i> soa mais natural no dia a dia."},
                {"erro": "Usar <i>Mr.</i> com o primeiro nome: <i>Mr. João</i>.", "correcao": "O mais comum é com o sobrenome: <i>Mr. Silva</i>. Com o primeiro nome, basta o nome."},
            ],
        },
        {
            "tipo": "ponte",
            "titulo": "No trabalho com tecnologia",
            "corpo": r"""<p>Os mesmos cumprimentos aparecem por escrito, em e-mails, Slack e GitHub:</p>
<ul><li><b>Hi team,</b> / <b>Hi everyone,</b>: abertura de mensagem para um grupo.</li>
<li><b>Nice to e-meet you!</b>: quando você conhece alguém por e-mail.</li>
<li><b>Looking forward to working with you.</b>: o “ansioso para trabalhar com você” do primeiro contato.</li>
<li><b>Thanks, and have a great day!</b> / <b>Best,</b>: fechamentos comuns de e-mail.</li></ul>""",
        },
        {
            "tipo": "quiz",
            "corpo": r"""<p>3 perguntas. Acertando 2, a camada “Vá mais fundo” é liberada e as revisões são agendadas.</p>""",
            "perguntas": [
                {"pergunta": "Alguém diz “<i>Nice to meet you!</i>”. A resposta mais natural é:", "opcoes": ["Nice to meet you too!", "I'm fine, thanks.", "Good night!"], "correta": 0,
                 "explicacao": "Repete-se a frase com <i>too</i> no final."},
                {"pergunta": "Você não sabe o nome de uma cliente. Como cumprimenta formalmente de manhã?", "opcoes": ["Good morning, Mrs.!", "Good morning, ma'am.", "Good night, ma'am."], "correta": 1,
                 "explicacao": "<i>Mrs.</i> precisa do sobrenome. Sem saber o nome, use <i>ma'am</i> (ou <i>sir</i>)."},
                {"pergunta": "Qual frase NÃO serve para devolver a pergunta “How are you?”", "opcoes": ["And you?", "How about you?", "What's your name?"], "correta": 2,
                 "explicacao": "<i>What's your name?</i> pergunta o nome. As outras duas devolvem o “e você?”."},
            ],
        },
        {
            "tipo": "camadas",
            "ponte": [
                {"nome": "YouGlish: “nice to meet you” na boca de nativos", "url": "https://youglish.com/pronounce/nice%20to%20meet%20you/english",
                 "trecho": "ouça 5 exemplos diferentes", "tempo": 5, "foco": "Ouvir a frase em vídeos reais, com sotaques diferentes, treina o ouvido melhor do que repetir um só modelo."},
            ],
            "revisao": [
                {"nome": "YouGlish: “good evening” na boca de nativos", "url": "https://youglish.com/pronounce/good%20evening/english",
                 "trecho": "ouça 5 exemplos", "tempo": 5, "foco": "No dia da revisão, confira se você ainda diz <i>good evening</i> (e não <i>good night</i>) ao chegar."},
            ],
        },
    ],
    "resumo": [
        "<i>Good evening</i> ao chegar; <i>good night</i> ao sair.",
        "<i>My name's ...</i> / <i>What's your name?</i> / <i>Nice to meet you (too)</i>.",
        "<i>How are you?</i> → <i>I'm fine/very well, thanks. And you?</i>",
        "Despedidas: <i>See you soon</i>, <i>Take care</i>, <i>I look forward to seeing you again</i>.",
    ],
    "proxima": "Aula 02: idade, nacionalidade e ocupação, para completar a apresentação.",
    "referencias": [
        {"obra": "EnglishBay, Curso de Inglês, Módulo 01 Aula 01 (Teacher Júlio)", "uso": "Estrutura da aula, exemplos e dicas de pronúncia."},
    ],
}

# ---------------------------------------------------------------------------
# Módulo 2 · Aula 09 · O que você está fazendo? (Present Continuous)
# ---------------------------------------------------------------------------
PILOT_CONTINUOUS = {
    "v": 2,
    "duracao": 45,
    "gancho": r"""Numa chamada de vídeo, alguém pergunta: “<i>What are you doing?</i>”. Você está programando, o modelo está treinando e o café está esfriando. Para falar do que está acontecendo <b>agora</b>, o inglês usa uma estrutura quase igual à nossa: “estou fazendo” vira <i>I am doing</i>.""",
    "objetivos": [
        "montar frases afirmativas, negativas e perguntas no present continuous;",
        "dar respostas curtas (<i>Yes, I am. / No, she isn't.</i>);",
        "acertar a grafia do <i>-ing</i> (dancing, putting, lying);",
        "perguntar e responder “o que você está fazendo?”.",
    ],
    "prerequisitos": ["Verbo <i>to be</i> (am, is, are) do Módulo 1."],
    "blocos": [
        {
            "tipo": "palpite",
            "rotulo": "Chute antes de ver",
            "pergunta": "Como dizer “Estou estudando inglês agora”?",
            "opcoes": ["I study English now.", "I am studying English now.", "I studying English now."],
            "correta": 1,
            "porques": [
                "<i>I study</i> é o presente simples: fala de hábito (“eu estudo”, toda semana), não do que está acontecendo neste momento.",
                "Isso! <i>am</i> (estou) + <i>studying</i> (estudando). Igualzinho ao português.",
                "Faltou o verbo <i>to be</i>. Sem o <i>am</i>, a frase fica como “eu estudando”.",
            ],
            "explicacao": "A receita é sempre: sujeito + <b>am/is/are</b> + verbo com <b>-ing</b>.",
        },
        {
            "tipo": "dialogo",
            "titulo": "Uma chamada no meio do trabalho",
            "falas": [
                {"quem": "Lucas", "en": "Hey, what are you doing?", "pt": "E aí, o que você está fazendo?"},
                {"quem": "Bia", "en": "I'm debugging a script. It isn't working!", "pt": "Estou depurando um script. Ele não está funcionando!"},
                {"quem": "Lucas", "en": "Are you using Python?", "pt": "Você está usando Python?"},
                {"quem": "Bia", "en": "Yes, I am. I'm training a small model.", "pt": "Sim, estou. Estou treinando um modelo pequeno."},
                {"quem": "Lucas", "en": "Is it learning?", "pt": "Ele está aprendendo?"},
                {"quem": "Bia", "en": "No, it isn't. The loss is going up!", "pt": "Não, não está. A perda está subindo!"},
                {"quem": "Lucas", "en": "Maybe the learning rate is too high.", "pt": "Talvez a taxa de aprendizado esteja alta demais."},
            ],
        },
        {
            "tipo": "video",
            "rotulo": "Com o Teacher Júlio · a estrutura",
            "id": "Y-M_0XQxNqs",
            "inicio": 90,
            "fim": 640,
            "canal": "EnglishBay",
            "titulo_video": "Módulo 02 Aula 09 · O que você está fazendo?",
            "corpo": r"""<p>Estrutura, negativa e perguntas (1:30 a 10:40).</p>""",
            "missao": [
                "Quais são as duas peças que nunca podem faltar no present continuous?",
                "Como ele faz a frase negativa sobre o Scott, que está no banho?",
                "Como se faz a pergunta? E como é a resposta curta?",
            ],
            "respostas": r"""<p><b>1.</b> O verbo <i>to be</i> (am/is/are), entendido como “estar”, e o verbo principal com <b>-ing</b>.</p>
<p><b>2.</b> Colocando <i>not</i> depois do <i>to be</i>: <i>Scott is not taking a bath</i> (ele está no chuveiro, <i>taking a shower</i>).</p>
<p><b>3.</b> Invertendo o <i>to be</i> com o sujeito: <i>Is Scott taking a shower?</i> A resposta curta repete só o sujeito e o <i>to be</i>: <i>Yes, he is.</i> / <i>No, he isn't.</i></p>""",
        },
        {
            "tipo": "tabela",
            "rotulo": "Organize na cabeça",
            "titulo": "As três formas",
            "cabecalho": ["Afirmativa", "Negativa", "Pergunta", "Resposta curta"],
            "linhas": [
                ["I'm working.", "I'm not working.", "Am I working?", "Yes, you are."],
                ["You're working.", "You aren't working.", "Are you working?", "No, I'm not."],
                ["She's working.", "She isn't working.", "Is she working?", "Yes, she is."],
                ["They're working.", "They aren't working.", "Are they working?", "No, they aren't."],
            ],
        },
        {
            "tipo": "pense",
            "rotulo": "Descubra a regra",
            "titulo": "O que acontece com a grafia?",
            "corpo": r"""<p>Observe: <i>dance → dancing</i>, <i>close → closing</i>, <i>put → putting</i>, <i>stop → stopping</i>, <i>lie → lying</i>, <i>work → working</i>.</p>""",
            "pergunta": "Tente formular as três regras antes de abrir.",
            "resposta": r"""<p><b>1.</b> Verbo terminado em <b>-e</b> mudo: tira o <i>e</i> (<i>dance → dancing</i>).</p>
<p><b>2.</b> Uma sílaba (ou tônica na última) terminando em <b>consoante + vogal + consoante</b>: dobra a última consoante (<i>put → putting</i>, <i>stop → stopping</i>).</p>
<p><b>3.</b> Terminado em <b>-ie</b>: troca por <i>y</i> (<i>lie → lying</i>, <i>die → dying</i>).</p>
<p>Fora isso, só acrescente <i>-ing</i> (<i>work → working</i>).</p>""",
        },
        {
            "tipo": "video",
            "rotulo": "Com o Teacher Júlio · a grafia do -ing",
            "id": "Y-M_0XQxNqs",
            "inicio": 1745,
            "fim": 1925,
            "canal": "EnglishBay",
            "titulo_video": "Módulo 02 Aula 09 · O que você está fazendo?",
            "corpo": r"""<p>Confira as regras que você acabou de descobrir (29:05 a 32:05).</p>""",
            "missao": [
                "Que curiosidade ele conta sobre o verbo <i>lie</i>?",
                "Na regra do CVC (consoante, vogal, consoante), a pronúncia muda quando se dobra a letra?",
            ],
            "respostas": r"""<p><b>1.</b> <i>Lie</i> tem dois sentidos, “mentir” e “deitar”, com a mesma grafia e pronúncia. <i>He is lying</i> pode ser “ele está mentindo” ou “ele está deitando”: o contexto decide.</p>
<p><b>2.</b> Não. Dobrar a consoante muda só a escrita (<i>putting</i>); o som é o mesmo de <i>put</i> + <i>ing</i>.</p>""",
        },
        {
            "tipo": "parsons",
            "modo": "frase",
            "titulo": "Monte a pergunta",
            "corpo": r"""<p>Coloque as palavras na ordem de uma pergunta em inglês.</p>""",
            "linhas": ["What", "are", "you", "doing", "now?"],
            "explicacao": r"""<p>Palavra de pergunta (<i>What</i>) + <i>to be</i> (<i>are</i>) + sujeito (<i>you</i>) + verbo com -ing (<i>doing</i>). É a pergunta que você mais vai ouvir e fazer.</p>""",
        },
        {
            "tipo": "ouvir",
            "titulo": "Escute e responda",
            "itens": [
                {"frase": "She is brushing her hair.", "opcoes": ["Ela está escovando o cabelo", "Ela está escovando os dentes", "Ela está lavando o cabelo"], "correta": 0, "pt": "Ela está escovando o cabelo."},
                {"frase": "They aren't sleeping. They're watching TV.", "opcoes": ["Eles estão dormindo", "Eles não estão dormindo, estão vendo TV", "Eles estão desligando a TV"], "correta": 1, "pt": "Eles não estão dormindo. Estão vendo TV."},
                {"frase": "Who is she calling?", "opcoes": ["Para quem ela está ligando?", "Por que ela está chorando?", "Onde ela está indo?"], "correta": 0, "pt": "Para quem ela está ligando?"},
                {"frase": "I'm watching a video lesson.", "dica": "5 palavras (contando I'm)"},
                {"frase": "Where are you going?", "dica": "4 palavras"},
            ],
        },
        {
            "tipo": "falar",
            "titulo": "Agora é a sua vez de falar",
            "frases": [
                {"en": "What are you doing now?", "pt": "O que você está fazendo agora?"},
                {"en": "I'm studying English.", "pt": "Estou estudando inglês."},
                {"en": "We're training a new model.", "pt": "Estamos treinando um novo modelo."},
                {"en": "No, it isn't working.", "pt": "Não, não está funcionando."},
            ],
        },
        {
            "tipo": "vocab",
            "titulo": "Verbos do dia a dia (com -ing)",
            "cartoes": [
                {"en": "working", "pt": "trabalhando", "ex": "I'm working from home today."},
                {"en": "studying", "pt": "estudando", "ex": "She's studying for a test."},
                {"en": "waiting", "pt": "esperando", "ex": "We're waiting for the build."},
                {"en": "running", "pt": "correndo / rodando", "ex": "The script is running."},
                {"en": "taking a shower", "pt": "tomando banho (de chuveiro)", "ex": "He's taking a shower."},
                {"en": "going", "pt": "indo", "ex": "Where are you going?"},
            ],
        },
        {
            "tipo": "armadilhas",
            "itens": [
                {"erro": "<i>I studying now.</i>", "correcao": "Falta o <i>to be</i>: <i>I <b>am</b> studying now.</i>"},
                {"erro": "<i>Are you work now?</i>", "correcao": "Falta o <i>-ing</i>: <i>Are you work<b>ing</b> now?</i>"},
                {"erro": "<i>I'm knowing the answer.</i> / <i>I'm wanting coffee.</i>", "correcao": "Verbos de estado (<i>know, want, like, need, believe</i>) quase nunca vão para o -ing: <i>I know the answer. I want coffee.</i>"},
                {"erro": "<i>She is calling to the police.</i>", "correcao": "<i>Call</i> não leva <i>to</i>: <i>She is calling the police.</i> (como o professor alerta no vídeo)."},
            ],
        },
        {
            "tipo": "ponte",
            "titulo": "No trabalho com tecnologia",
            "corpo": r"""<p>O present continuous está em toda tela de programa e em toda reunião de status:</p>
<ul><li><b>Loading model...</b> / <b>Downloading...</b> / <b>Training is running.</b>: mensagens de progresso.</li>
<li><b>I'm working on the login bug.</b>: “estou trabalhando no bug do login”, a frase número 1 da daily.</li>
<li><b>The tests are failing.</b> / <b>The server isn't responding.</b>: relatar um problema que está acontecendo.</li>
<li>No GitHub: <b>Currently working on...</b> no seu perfil.</li></ul>""",
        },
        {
            "tipo": "quiz",
            "corpo": r"""<p>3 perguntas. Acertando 2, a camada “Vá mais fundo” é liberada e as revisões são agendadas.</p>""",
            "perguntas": [
                {"pergunta": "“<i>Is the model learning?</i>” Resposta curta negativa:", "opcoes": ["No, it isn't.", "No, it doesn't.", "No, it not learning."], "correta": 0,
                 "explicacao": "A resposta curta usa o mesmo <i>to be</i> da pergunta: <i>is → isn't</i>."},
                {"pergunta": "Qual grafia está correta?", "opcoes": ["stoping", "stopping", "stopeing"], "correta": 1,
                 "explicacao": "<i>Stop</i> termina em consoante-vogal-consoante e tem uma sílaba: dobra o <i>p</i>."},
                {"pergunta": "Qual frase está certa?", "opcoes": ["I'm needing help.", "I need help.", "I needing help."], "correta": 1,
                 "explicacao": "<i>Need</i> é verbo de estado: fica no presente simples."},
            ],
        },
        {
            "tipo": "camadas",
            "ponte": [
                {"nome": "Teacher Elza, “Present Continuous no inglês: como usar o ING”", "url": "https://www.youtube.com/watch?v=su5NeDlSJjI",
                 "trecho": "vídeo completo, em português", "tempo": 12, "foco": "Outra professora, outros exemplos: ótimo para fixar a estrutura por outro ângulo."},
            ],
            "revisao": [
                {"nome": "YouGlish: “what are you doing” na boca de nativos", "url": "https://youglish.com/pronounce/what%20are%20you%20doing/english",
                 "trecho": "ouça 5 exemplos", "tempo": 5, "foco": "Repare como os nativos juntam as palavras: “whaddaya doing?”."},
            ],
        },
    ],
    "resumo": [
        "Present continuous = <i>am/is/are</i> + verbo com <i>-ing</i>, para o que está acontecendo agora.",
        "Negativa: <i>not</i> depois do <i>to be</i>. Pergunta: inverta o <i>to be</i> e o sujeito.",
        "Grafia: tira o <i>e</i> mudo, dobra a consoante no CVC, <i>-ie</i> vira <i>y</i>.",
        "Verbos de estado (<i>know, want, need, like</i>) ficam no presente simples.",
    ],
    "proxima": "Aula 10: as horas em inglês, para dizer quando as coisas acontecem.",
    "referencias": [
        {"obra": "EnglishBay, Curso de Inglês, Módulo 02 Aula 09 (Teacher Júlio)", "uso": "Estrutura, exemplos (Scott, Marcy and Frank, Jean) e regras de grafia."},
    ],
}

# ---------------------------------------------------------------------------
# Módulo 4 · Aula 04 · Superlativos
# ---------------------------------------------------------------------------
PILOT_SUPERLATIVES = {
    "v": 2,
    "duracao": 45,
    "gancho": r"""“O modelo <b>mais rápido</b>”, “o notebook <b>mais barato</b>”, “a <b>melhor</b> opção”. Toda comparação de ferramentas, preços e benchmarks termina num superlativo, aquele que é o número 1 do grupo. Em inglês há duas receitas e alguns rebeldes, e você vai dominar os três.""",
    "objetivos": [
        "formar o superlativo de adjetivos curtos (<i>the tallest</i>) e longos (<i>the most expensive</i>);",
        "aplicar as regras de grafia (<i>biggest, easiest</i>);",
        "usar os irregulares <i>best, worst, farthest</i> e o oposto <i>the least</i>;",
        "saber quando o <i>the</i> sai (com possessivos).",
    ],
    "prerequisitos": ["Comparativos (Módulo 4, Aula 02): <i>cheaper than, more interesting than</i>."],
    "blocos": [
        {
            "tipo": "palpite",
            "rotulo": "Chute antes de ver",
            "pergunta": "Como dizer “o modelo mais barato”?",
            "opcoes": ["the most cheap model", "the cheapest model", "the more cheap model"],
            "correta": 1,
            "porques": [
                "<i>Cheap</i> tem uma sílaba só: adjetivo curto não usa <i>most</i>, ganha <i>-est</i>.",
                "Isso! Adjetivo curto: <i>the</i> + adjetivo + <i>-est</i>.",
                "<i>More</i> é do comparativo, e mesmo assim adjetivo curto usaria <i>cheaper</i>.",
            ],
            "explicacao": "O tamanho do adjetivo decide a receita, exatamente como no comparativo.",
        },
        {
            "tipo": "dialogo",
            "titulo": "Escolhendo um modelo",
            "falas": [
                {"quem": "Rafa", "en": "Which model is the best for our chatbot?", "pt": "Qual modelo é o melhor para o nosso chatbot?"},
                {"quem": "Nina", "en": "The large one is the most accurate, but it's the most expensive.", "pt": "O grande é o mais preciso, mas é o mais caro."},
                {"quem": "Rafa", "en": "And which one is the fastest?", "pt": "E qual é o mais rápido?"},
                {"quem": "Nina", "en": "The small one. It's the cheapest and the fastest.", "pt": "O pequeno. É o mais barato e o mais rápido."},
                {"quem": "Rafa", "en": "Is it the worst option, then?", "pt": "Então é a pior opção?"},
                {"quem": "Nina", "en": "No! For simple questions, it's the easiest choice.", "pt": "Não! Para perguntas simples, é a escolha mais fácil."},
            ],
        },
        {
            "tipo": "video",
            "rotulo": "Com o Teacher Júlio · as duas receitas",
            "id": "HeGr10ZcxoQ",
            "inicio": 90,
            "fim": 643,
            "canal": "EnglishBay",
            "titulo_video": "Módulo 04 Aula 04 · Superlativos",
            "corpo": r"""<p>A estrutura e as regras dos adjetivos curtos (1:30 a 10:43).</p>""",
            "missao": [
                "Como ele diz que o Everest é a montanha mais alta e a mais perigosa de escalar?",
                "Que palavrinha é essencial na estrutura do superlativo?",
                "Por que ele completa a frase com <i>in the world</i>?",
            ],
            "respostas": r"""<p><b>1.</b> <i>Mount Everest is <b>the highest</b> mountain in the world. It's <b>the most dangerous</b> to climb, too.</i> <i>High</i> é curto (ganha <i>-est</i>); <i>dangerous</i> tem três sílabas (usa <i>the most</i>).</p>
<p><b>2.</b> O <b>the</b>: superlativo é “o número 1”, e o <i>the</i> marca isso.</p>
<p><b>3.</b> Porque o superlativo costuma vir com o <b>lugar ou grupo</b> de comparação, com <i>in</i>: <i>in the world, in Brazil, in my family</i>. Em conversa, quando o contexto já está claro, dá para omitir.</p>""",
        },
        {
            "tipo": "tabela",
            "rotulo": "Organize na cabeça",
            "titulo": "As receitas",
            "cabecalho": ["Tipo de adjetivo", "Regra", "Exemplos"],
            "linhas": [
                ["1 sílaba", "the + adjetivo + -est", "tall → the tallest · cheap → the cheapest"],
                ["Termina em -e", "só + -st", "late → the latest · close → the closest"],
                ["Consoante-vogal-consoante", "dobra a última letra", "big → the biggest · sad → the saddest"],
                ["2 sílabas em -y", "y vira i + -est", "easy → the easiest · happy → the happiest"],
                ["2 sílabas ou mais (outros)", "the most + adjetivo", "expensive → the most expensive"],
                ["Irregulares", "decore", "good → the best · bad → the worst · far → the farthest"],
                ["O oposto (menos)", "the least + qualquer adjetivo", "the least expensive"],
            ],
        },
        {
            "tipo": "pense",
            "rotulo": "Descubra a regra",
            "titulo": "Cadê o “the”?",
            "corpo": r"""<p>Compare: <i>Larry is <b>the</b> closest friend I have.</i> e <i>Larry is <b>my</b> closest friend.</i> E também: <i>The president is <b>a country's</b> most important politician.</i></p>""",
            "pergunta": "Em que situação o <i>the</i> desaparece?",
            "resposta": r"""<p>Quando entra um <b>possessivo</b>: <i>my, your, his, her, our, their</i> ou o <b>'s</b> (<i>a country's, Monica's</i>). O possessivo ocupa o lugar do <i>the</i>. Nunca use os dois juntos: ✗ <i>the my best friend</i>.</p>""",
        },
        {
            "tipo": "video",
            "rotulo": "Com o Teacher Júlio · os rebeldes",
            "id": "HeGr10ZcxoQ",
            "inicio": 1570,
            "fim": 1830,
            "canal": "EnglishBay",
            "titulo_video": "Módulo 04 Aula 04 · Superlativos",
            "corpo": r"""<p>Irregulares e o oposto, “o menos” (26:10 a 30:30).</p>""",
            "missao": [
                "Quais são os superlativos de <i>good</i>, <i>bad</i> e <i>far</i>?",
                "Como dizer “o menos caro”? A regra muda com o tamanho do adjetivo?",
                "Qual dos anéis é o menos caro no exemplo dele?",
            ],
            "respostas": r"""<p><b>1.</b> <i>Good → the best</i>, <i>bad → the worst</i>, <i>far → the farthest</i> (ou <i>the furthest</i>).</p>
<p><b>2.</b> <i>The least expensive</i>. Não muda: <i>the least</i> serve para adjetivos de qualquer tamanho.</p>
<p><b>3.</b> O de prata: <i>The silver ring is the least expensive.</i></p>""",
        },
        {
            "tipo": "parsons",
            "modo": "frase",
            "titulo": "Monte a frase",
            "corpo": r"""<p>Ordene as palavras para dizer “Este é o maior modelo aberto”.</p>""",
            "linhas": ["This", "is", "the", "largest", "open", "model."],
            "explicacao": r"""<p><i>Large</i> termina em <i>-e</i>: só ganha <i>-st</i> (<i>largest</i>). O superlativo vem antes do substantivo, depois do <i>the</i>.</p>""",
        },
        {
            "tipo": "ouvir",
            "titulo": "Escute e responda",
            "itens": [
                {"frase": "It's the most expensive ring.", "opcoes": ["É o anel mais caro", "É o anel menos caro", "É um anel caro"], "correta": 0, "pt": "É o anel mais caro."},
                {"frase": "This is the worst restaurant in my city.", "opcoes": ["O melhor restaurante da cidade", "O pior restaurante da minha cidade", "Um restaurante novo na cidade"], "correta": 1, "pt": "Este é o pior restaurante da minha cidade."},
                {"frase": "Larry is my closest friend.", "opcoes": ["Larry é meu amigo mais próximo", "Larry mora mais perto de mim", "Larry é meu amigo mais antigo"], "correta": 0, "pt": "Larry é meu amigo mais próximo."},
                {"frase": "It's the saddest movie ever.", "dica": "5 palavras (contando It's)"},
                {"frase": "What is the easiest way to learn English?", "dica": "8 palavras"},
            ],
        },
        {
            "tipo": "falar",
            "titulo": "Agora é a sua vez de falar",
            "frases": [
                {"en": "Mount Everest is the highest mountain in the world.", "pt": "O Everest é a montanha mais alta do mundo."},
                {"en": "This is the best day ever.", "pt": "Este é o melhor dia de todos."},
                {"en": "It's the most important part of the project.", "pt": "É a parte mais importante do projeto."},
                {"en": "The small model is the cheapest.", "pt": "O modelo pequeno é o mais barato."},
            ],
        },
        {
            "tipo": "armadilhas",
            "itens": [
                {"erro": "<i>the most big</i> / <i>the most cheap</i>", "correcao": "Adjetivo curto ganha <i>-est</i>: <i>the biggest</i>, <i>the cheapest</i>."},
                {"erro": "<i>the best of the world</i>", "correcao": "Lugar vem com <i>in</i>: <i>the best <b>in</b> the world</i>."},
                {"erro": "Esquecer o <i>the</i>: <i>She is best student.</i>", "correcao": "<i>She is <b>the</b> best student.</i> (a menos que haja possessivo: <i>my best student</i>)."},
                {"erro": "<i>the most good</i> / <i>the baddest</i>", "correcao": "Irregulares: <i>the best</i> e <i>the worst</i>."},
            ],
        },
        {
            "tipo": "ponte",
            "titulo": "No mundo de IA",
            "corpo": r"""<p>Anúncios de modelos e tabelas de benchmark vivem de superlativos:</p>
<ul><li><b>state-of-the-art</b> (SOTA): o melhor resultado conhecido até agora.</li>
<li><b>our most capable model</b> / <b>our fastest model</b>: como as empresas apresentam modelos novos.</li>
<li><b>the largest open-weight model</b>: o maior modelo com pesos abertos.</li>
<li><b>the lowest latency</b> / <b>the highest accuracy</b>: a menor latência, a maior precisão.</li></ul>""",
        },
        {
            "tipo": "quiz",
            "corpo": r"""<p>3 perguntas. Acertando 2, a camada “Vá mais fundo” é liberada e as revisões são agendadas.</p>""",
            "perguntas": [
                {"pergunta": "Qual está correta?", "opcoes": ["the easyest", "the easiest", "the most easy"], "correta": 1,
                 "explicacao": "Duas sílabas terminando em <i>-y</i>: troca por <i>i</i> e acrescenta <i>-est</i>."},
                {"pergunta": "“O pior bug do projeto” é:", "opcoes": ["the baddest bug in the project", "the worst bug in the project", "the most bad bug of the project"], "correta": 1,
                 "explicacao": "<i>Bad</i> é irregular: <i>the worst</i>. E o grupo vem com <i>in</i>."},
                {"pergunta": "Qual frase está certa?", "opcoes": ["She is the my best friend.", "She is my best friend.", "She is my the best friend."], "correta": 1,
                 "explicacao": "O possessivo substitui o <i>the</i>."},
            ],
        },
        {
            "tipo": "camadas",
            "ponte": [
                {"nome": "YouGlish: “the most important” na boca de nativos", "url": "https://youglish.com/pronounce/the%20most%20important/english",
                 "trecho": "ouça 5 exemplos", "tempo": 5, "foco": "Repare que o <i>t</i> de <i>most</i> quase some antes de consoante: “the mos' important”."},
            ],
            "revisao": [
                {"nome": "Teacher Elza, “Os comparativos e superlativos em inglês”", "url": "https://www.youtube.com/watch?v=UcQeFtrAVis",
                 "trecho": "vídeo completo, em português", "tempo": 9, "foco": "Outra explicação curta, juntando comparativo e superlativo: ótima para o dia da revisão."},
            ],
        },
    ],
    "resumo": [
        "Curto: <i>the</i> + adjetivo + <i>-est</i>. Longo: <i>the most</i> + adjetivo.",
        "Grafia: <i>-e</i> só + <i>st</i>; CVC dobra a consoante; <i>-y</i> vira <i>-iest</i>.",
        "Irregulares: <i>the best, the worst, the farthest</i>. Oposto: <i>the least</i> + qualquer adjetivo.",
        "Possessivo (<i>my, Monica's</i>) substitui o <i>the</i>; o grupo de comparação vem com <i>in</i>.",
    ],
    "proxima": "Aula 05: o passado do verbo <i>to be</i> (<i>was, were</i>).",
    "referencias": [
        {"obra": "EnglishBay, Curso de Inglês, Módulo 04 Aula 04 (Teacher Júlio)", "uso": "Estrutura, exemplos (Everest, Amazon River, Larry, anéis) e irregulares."},
    ],
}

# Ligação com as aulas da playlist (pelo videoId de english_playlist.json)
ENGLISH_PILOT_GUIDES = {
    "0HHnezXSKnI": PILOT_GREETINGS,
    "Y-M_0XQxNqs": PILOT_CONTINUOUS,
    "HeGr10ZcxoQ": PILOT_SUPERLATIVES,
}
