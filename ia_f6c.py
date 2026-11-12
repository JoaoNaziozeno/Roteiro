# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 6 (parte C): portfólio, presença profissional e carreira."""
from lesson_factory import *

AULAS = {}

AULAS["3 a 5 projetos documentados no GitHub"] = aula(
    25,
    "Um diploma diz que você estudou; um portfólio mostra o que você sabe fazer. Três a cinco projetos bem escolhidos e bem documentados valem mais que trinta notebooks de tutorial. Esta aula ajuda a escolher, construir e apresentar esses projetos.",
    ["escolher projetos que mostrem habilidades diferentes;", "fugir dos projetos “de tutorial”;", "organizar repositórios que recrutadores entendem em 2 minutos."],
    ["Git, GitHub e as fases anteriores do roteiro."],
    [
        chute("Qual projeto impressiona mais um recrutador?", ["Classificação do Titanic com 85% de acurácia.", "Um sistema que resolve um problema real (ex.: RAG sobre as leis do seu município), com dados próprios, deploy e demo.", "Dez notebooks curtos de cursos diferentes."], 1,
              ["Todo mundo já fez; não diferencia.", "Isso! Problema real, decisões próprias e algo funcionando mostram o que o trabalho exige.", "Quantidade não substitui profundidade."],
              "Problema real + ponta a ponta + documentação."),
        concreto("O portfólio do arquiteto", "<p>Um arquiteto não mostra 50 rascunhos: mostra 4 obras, com fotos, a planta e a história de cada decisão. Seu GitHub é esse portfólio: poucas obras completas, bem fotografadas.</p>"),
        tabela("Um conjunto equilibrado", ["Projeto", "Mostra"], [
            ["Análise de dados com pergunta de negócio", "SQL, pandas, visualização, comunicação"],
            ["Modelo clássico de ML com deploy (API + Docker)", "feature engineering, validação, engenharia"],
            ["Deep learning (visão ou texto) com transfer learning", "PyTorch, GPU, avaliação"],
            ["Aplicação com LLM (RAG ou agente) com evals", "LLMs, busca, avaliação, produto"],
            ["Contribuição ou ferramenta open source", "colaboração, código de qualidade"],
        ], rot="Organize na cabeça"),
        passos("Checklist de cada repositório", [
            ("Nome claro e descrição de uma linha.", "“rag-leis-recife: perguntas sobre a legislação municipal com citações”."),
            ("README com problema, solução, resultados e como rodar.", "Próxima aula."),
            ("Código em <code>src/</code>, notebooks em <code>notebooks/</code>, testes em <code>tests/</code>.", "Organização mostra maturidade."),
            ("<code>requirements.txt</code> ou <code>pyproject.toml</code> e instruções que funcionam.", "Teste num ambiente limpo."),
            ("Demo pública (Spaces, Streamlit Cloud) e imagens no README.", "O recrutador vê funcionando sem instalar."),
            ("Fixe os melhores no topo do perfil.", "Os “pinned repositories”."),
        ]),
        cod("Auditor de repositórios", "Escreva <code>auditar(arquivos)</code> que recebe a lista de caminhos de um repositório e devolve a lista do que está faltando entre: <code>README.md</code>, arquivo de dependências (<code>requirements.txt</code> ou <code>pyproject.toml</code>), pasta <code>tests/</code>, <code>.gitignore</code>, e alerta se houver arquivos que não deveriam estar lá (<code>.env</code> ou arquivos <code>.csv</code> fora de <code>exemplos/</code>).",
            '''
def auditar(arquivos):
    return []

repo = ["README.md", "src/app.py", "dados/clientes.csv", ".env", "requirements.txt"]
print(auditar(repo))
''',
            [("Faltas e alertas", "assert sorted(auditar(['README.md', 'src/app.py', 'dados/clientes.csv', '.env', 'requirements.txt'])) == sorted(['falta tests/', 'falta .gitignore', 'remova .env', 'remova dados/clientes.csv'])"),
             ("Repositório ok", "assert auditar(['README.md', 'pyproject.toml', 'tests/test_app.py', '.gitignore', 'exemplos/amostra.csv']) == []"),
             ("Sem README", "assert 'falta README.md' in auditar(['src/a.py'])")],
            '''
def auditar(arquivos):
    problemas = []
    if "README.md" not in arquivos:
        problemas.append("falta README.md")
    if not any(a in arquivos for a in ("requirements.txt", "pyproject.toml")):
        problemas.append("falta arquivo de dependências")
    if not any(a.startswith("tests/") for a in arquivos):
        problemas.append("falta tests/")
    if ".gitignore" not in arquivos:
        problemas.append("falta .gitignore")
    for a in arquivos:
        if a == ".env" or a.endswith("/.env"):
            problemas.append(f"remova {a}")
        elif a.endswith(".csv") and not a.startswith("exemplos/"):
            problemas.append(f"remova {a}")
    return problemas

repo = ["README.md", "src/app.py", "dados/clientes.csv", ".env", "requirements.txt"]
print(auditar(repo))
''', ["Para pastas, teste <code>a.startswith(\"tests/\")</code>.", "Alertas: <code>.env</code> e <code>.csv</code> fora de <code>exemplos/</code>."]),
        erros([("Projetos clonados de tutorial sem mudança.", "Mude os dados, a pergunta ou acrescente deploy e avaliação."), ("Repositórios abandonados pela metade.", "Melhor 3 terminados que 10 incompletos."), ("Dados sensíveis e chaves no histórico do Git.", "Apagar o arquivo não basta: troque a chave e limpe o histórico.")]),
        pense("Qual será o seu?", "Pense num problema da sua cidade, trabalho ou hobby que um dos projetos da tabela poderia resolver. Que dados você conseguiria?", "<p>Bons projetos nascem de problemas que você conhece: preços de imóveis do seu bairro, atendimento da sua empresa, estatísticas do seu esporte. Conhecer o domínio faz suas decisões parecerem (e serem) de quem entende.</p>"),
        quiz([
            ("Quantos projetos são recomendados no portfólio?", ["3 a 5 bem feitos.", "Pelo menos 30.", "Só 1."], 0, "Qualidade."),
            ("O que diferencia um projeto?", ["Problema real, ponta a ponta, documentado.", "Ser do Kaggle.", "Ter muitos arquivos."], 0, "Profundidade."),
            ("O que nunca deve estar no repositório?", ["Arquivos .env com chaves.", "README.", "Testes."], 0, "Segredos."),
        ]),
    ],
    ["Poucos projetos completos, com problema real.", "Cubra habilidades diferentes: dados, ML, DL, LLM, engenharia.", "Organização, demo e nada de segredos no Git."],
    "READMEs com problema, solução e resultados.",
    livro=("PROGIT:x", "Pro Git, capítulo 6, “GitHub”", "Como o livro sugere manter um projeto no GitHub?"))

AULAS["READMEs com problema, solução e resultados"] = aula(
    20,
    "O recrutador abre seu repositório e dá uma olhada de 30 segundos no README. Se em 30 segundos ele não entende o problema, o que você fez e o resultado, o projeto não conta. O README é a página de venda do seu trabalho.",
    ["estruturar um README em problema, solução e resultados;", "mostrar números e imagens;", "escrever instruções que funcionam."],
    ["Projetos documentados no GitHub, storytelling com dados."],
    [
        chute("Qual frase de abertura é melhor para um README?", ["“Este é meu projeto de ML.”", "“Previsão de evasão de clientes de uma operadora: o modelo identifica 78% dos clientes que vão cancelar, com 3 semanas de antecedência.”", "“Projeto feito com Python, pandas, sklearn, xgboost, matplotlib...”"], 1,
              ["Não diz nada.", "Isso! Problema, resultado e impacto na primeira linha.", "Ferramentas importam menos que o resultado."],
              "Comece pelo resultado, não pela tecnologia."),
        concreto("A embalagem do produto", "<p>Na prateleira, a embalagem diz em 3 segundos o que o produto é e por que comprar. Os detalhes ficam no verso. No README, o topo é a embalagem; o resto é o verso.</p>"),
        passos("A estrutura", [
            ("<b>Título + uma linha</b> com o resultado.", "Com um GIF ou imagem da demo logo abaixo."),
            ("<b>Problema</b>: o contexto e por que importa.", "Dois ou três parágrafos curtos."),
            ("<b>Solução</b>: dados, abordagem e decisões.", "Um diagrama simples da arquitetura ajuda muito."),
            ("<b>Resultados</b>: métricas, comparação com o baseline, limitações.", "Números e gráficos; seja honesto sobre o que não funcionou."),
            ("<b>Como rodar</b>: comandos copiáveis.", "<code>pip install -r requirements.txt</code> e <code>python -m src.app</code>."),
            ("<b>Próximos passos</b>.", "Mostra que você sabe o que faria com mais tempo."),
        ]),
        cod("Verificador de README", "Escreva <code>checar(readme)</code> que devolve a lista de seções ausentes (procure títulos Markdown <code>## Problema</code>, <code>## Solução</code>, <code>## Resultados</code>, <code>## Como rodar</code>, sem diferenciar maiúsculas) e acrescenta <code>\"sem números nos resultados\"</code> se a seção Resultados não tiver nenhum dígito.",
            '''
import re

SECOES = ["Problema", "Solução", "Resultados", "Como rodar"]

def checar(readme):
    return []

readme = """# Evasão de clientes
## Problema
Clientes cancelam sem aviso.
## Resultados
O modelo ficou bom.
## Como rodar
pip install -r requirements.txt
"""
print(checar(readme))
''',
            [("Seções e números", "assert checar(readme) == ['falta Solução', 'sem números nos resultados'], f'{checar(readme)}'"),
             ("README completo", "ok = '## problema\\nx\\n## Solução\\ny\\n## Resultados\\nRecall de 78% contra 40% do baseline.\\n## Como rodar\\nz'\nassert checar(ok) == []")],
            '''
import re

SECOES = ["Problema", "Solução", "Resultados", "Como rodar"]

def checar(readme):
    faltas = []
    for s in SECOES:
        if not re.search(rf"^##\\s+{re.escape(s)}\\s*$", readme, re.M | re.I):
            faltas.append(f"falta {s}")
    m = re.search(r"^##\\s+Resultados\\s*$(.*?)(?=^##\\s|\\Z)", readme, re.M | re.I | re.S)
    if m and not re.search(r"\\d", m.group(1)):
        faltas.append("sem números nos resultados")
    return faltas

readme = """# Evasão de clientes
## Problema
Clientes cancelam sem aviso.
## Resultados
O modelo ficou bom.
## Como rodar
pip install -r requirements.txt
"""
print(checar(readme))
''', ["Use <code>re.search</code> com <code>re.M | re.I</code> para achar <code>^##\\s+Seção</code>.", "Capture o texto entre <code>## Resultados</code> e o próximo <code>##</code> e procure <code>\\d</code>."]),
        erros([("README só com “como instalar”.", "Sem problema e resultados, o leitor não sabe por que se importar."), ("Esconder limitações.", "Dizer o que não funcionou mostra senso crítico, muito valorizado."), ("Instruções que não funcionam.", "Teste num ambiente novo (ou num contêiner) antes de publicar.")]),
        ponte("Reaproveite", "<p>Um bom README vira post no LinkedIn, artigo no blog e roteiro para contar o projeto na entrevista. Escreva uma vez, use em vários lugares.</p>"),
        quiz([
            ("O que vem primeiro num README?", ["O resultado em uma linha.", "A lista de bibliotecas.", "A licença."], 0, "Embalagem."),
            ("Por que mostrar limitações?", ["Demonstra senso crítico e honestidade.", "Para diminuir o projeto.", "Não deve."], 0, "Maturidade."),
            ("Resultados devem ter:", ["Números e comparação com um baseline.", "Só adjetivos.", "Nada."], 0, "Evidência."),
        ]),
    ],
    ["Topo: o resultado em uma linha + imagem.", "Problema, solução, resultados (com números), como rodar.", "Honestidade sobre limitações e próximos passos."],
    "Perfil ativo no LinkedIn e Kaggle.",
    livro=("PROGIT:x", "Pro Git, capítulo 6, “GitHub”", "O que o livro diz sobre o arquivo README de um projeto?"))

AULAS["Perfil ativo no LinkedIn e Kaggle"] = aula(
    20,
    "Muitas vagas de IA são preenchidas por indicação ou por recrutadores que buscam perfis. Um LinkedIn claro e um Kaggle com atividade fazem você ser encontrado; postar o que aprende faz você ser lembrado.",
    ["montar um perfil que recrutadores encontram;", "usar o Kaggle para aprender e mostrar evolução;", "criar uma rotina leve de publicações."],
    ["Projetos e READMEs."],
    [
        chute("Qual título de perfil no LinkedIn atrai mais recrutadores de IA?", ["“Estudante buscando oportunidades”.", "“Cientista de Dados | Python, SQL, Machine Learning | RAG e LLMs”.", "“Apaixonado por tecnologia”."], 1,
              ["Vago e sem palavras-chave.", "Isso! Recrutadores buscam por palavras-chave; o título é o campo mais pesado na busca.", "Não diz o que você faz."],
              "Título = o que você faz + palavras-chave."),
        concreto("A vitrine e a academia", "<p>O LinkedIn é a vitrine onde as pessoas encontram você. O Kaggle é a academia onde você treina em público: competições, datasets e notebooks mostram evolução ao longo do tempo.</p>"),
        tabela("O essencial do perfil", ["Seção", "O que colocar"], [
            ["Foto e capa", "foto profissional simples; capa com seu foco"],
            ["Título", "cargo-alvo + 3 a 5 palavras-chave"],
            ["Sobre", "quem você é, o que resolve, 2 ou 3 projetos com resultados, contato"],
            ["Destaques", "links para os projetos, demos e artigos"],
            ["Experiência", "resultados com números, não só tarefas"],
            ["Competências", "as que aparecem nas vagas que você quer"],
        ], rot="Organize na cabeça"),
        cod("Palavras-chave das vagas", "Descubra o que as vagas pedem: <code>palavras_chave(vagas, termos)</code> conta em quantas descrições cada termo aparece (sem diferenciar maiúsculas) e devolve os termos ordenados do mais pedido para o menos, sem os que não aparecem.",
            '''
def palavras_chave(vagas, termos):
    return []

vagas = [
    "Buscamos cientista de dados com Python, SQL e experiência com LLMs.",
    "Engenheiro de ML: Python, Docker, AWS e MLOps.",
    "Analista de dados: SQL, Power BI e Python.",
]
termos = ["Python", "SQL", "Docker", "LLMs", "Spark", "AWS"]
print(palavras_chave(vagas, termos))
''',
            [("Ranking", "r = palavras_chave(vagas, termos)\nassert r[:2] == [('Python', 3), ('SQL', 2)] and ('Spark', 0) not in r and len(r) == 5, f'{r}'")],
            '''
def palavras_chave(vagas, termos):
    contagem = [(t, sum(t.lower() in v.lower() for v in vagas)) for t in termos]
    return sorted([c for c in contagem if c[1] > 0], key=lambda c: -c[1])

vagas = [
    "Buscamos cientista de dados com Python, SQL e experiência com LLMs.",
    "Engenheiro de ML: Python, Docker, AWS e MLOps.",
    "Analista de dados: SQL, Power BI e Python.",
]
termos = ["Python", "SQL", "Docker", "LLMs", "Spark", "AWS"]
print(palavras_chave(vagas, termos))
''', ["Para cada termo, some quantas vagas o contêm.", "Ordene por contagem decrescente (<code>sorted</code> é estável)."]),
        passos("Uma rotina leve", [
            ("Uma vez por semana, um post curto sobre algo que aprendeu ou construiu.", "Com imagem ou trecho de código."),
            ("Comente com conteúdo em posts de pessoas da área.", "Comentários bons geram conexões."),
            ("No Kaggle, publique um notebook por mês, bem explicado.", "Notebooks bem documentados recebem votos e medalhas."),
            ("Participe de uma competição por trimestre, mesmo sem ganhar.", "Leia as soluções vencedoras depois: aprende-se muito."),
        ]),
        erros([("Perfil só com cursos.", "Mostre o que você construiu com eles."), ("Postar só quando procura emprego.", "Constância pequena vale mais que esforço concentrado."), ("Copiar soluções no Kaggle.", "Aprender com elas é ótimo; publicar como sua não é.")]),
        ponte("Rede de contatos", "<p>Conexões viram indicações. Converse com pessoas que trabalham onde você quer trabalhar, pergunte sobre o dia a dia (não peça emprego de cara) e acompanhe o trabalho delas.</p>"),
        quiz([
            ("O campo mais importante para ser encontrado no LinkedIn:", ["Título.", "Foto de capa.", "Data de nascimento."], 0, "Palavras-chave."),
            ("Para que serve o Kaggle no portfólio?", ["Mostrar prática e evolução em público.", "Guardar senhas.", "Hospedar APIs."], 0, "Academia pública."),
            ("Qual rotina é mais eficaz?", ["Posts pequenos e constantes.", "Um post por ano.", "Nunca postar."], 0, "Constância."),
        ]),
    ],
    ["Título com cargo e palavras-chave; Sobre com resultados.", "Kaggle para praticar e mostrar evolução.", "Constância: um post por semana, um notebook por mês."],
    "Inglês técnico.",
    livro=("MLCC:", "Google Machine Learning Crash Course", "Escolha um módulo e anote 10 termos em inglês que você ainda não conhecia."))

AULAS["Inglês técnico"] = aula(
    25,
    "A documentação, os artigos, os melhores vídeos, as vagas remotas e as mensagens de erro: quase tudo em IA está em inglês. Você não precisa falar perfeitamente, mas precisa ler documentação com conforto, escrever mensagens claras e entender reuniões técnicas.",
    ["ler documentação e artigos com estratégia;", "dominar o vocabulário técnico mais frequente;", "escrever issues, commits e mensagens em inglês."],
    ["As aulas de Inglês do roteiro (paralelas a esta fase)."],
    [
        chute("Qual é a melhor forma de ler um artigo científico em inglês?", ["Palavra por palavra, do começo ao fim, com dicionário.", "Título, resumo, figuras e conclusão primeiro; depois as seções que importam.", "Traduzir tudo automaticamente antes."], 1,
              ["Cansativo e pouco eficiente.", "Isso! Leitura em camadas: você entende a ideia antes de entrar nos detalhes.", "Ajuda às vezes, mas tira o treino."],
              "Leia em camadas, não em linha reta."),
        concreto("A academia de musculação", "<p>Você não começa levantando 100 kg: começa com pouco peso, todos os dias. O inglês técnico é igual: um trecho de documentação por dia, sempre um pouco acima do confortável, e em meses a leitura fica natural.</p>"),
        vocab([
            ("deploy", "implantar, publicar", "We deploy the model every Friday."),
            ("throughput", "vazão (quanto processa por tempo)", "The new server doubled our throughput."),
            ("benchmark", "teste de referência", "It scores well on public benchmarks."),
            ("fine-tune", "ajustar um modelo pré-treinado", "We fine-tuned it on our support tickets."),
            ("trade-off", "compromisso entre duas coisas", "There is a trade-off between speed and accuracy."),
            ("bottleneck", "gargalo", "Data loading is the bottleneck."),
            ("edge case", "caso extremo", "Handle the edge case of empty inputs."),
            ("rollback", "voltar à versão anterior", "We had to roll back the release."),
        ]),
        tabela("Frases prontas para o dia a dia", ["Situação", "Em inglês"], [
            ["abrir uma issue", "“Steps to reproduce: ... Expected: ... Actual: ...”"],
            ["mensagem de commit", "“Fix off-by-one error in date parsing”"],
            ["pedir revisão", "“Could you take a look at this PR when you have a moment?”"],
            ["discordar com educação", "“I see your point, but I'm concerned about ...”"],
            ["não entendeu na reunião", "“Sorry, could you rephrase that?”"],
        ], rot="Organize na cabeça"),
        cod("Seu glossário", "Monte um glossário a partir de um texto técnico: <code>termos_novos(texto, conhecidos)</code> devolve as palavras (minúsculas, sem pontuação, com 4+ letras) que não estão no conjunto de conhecidas, ordenadas pela frequência no texto (e alfabeticamente em empate).",
            '''
import re
from collections import Counter

def termos_novos(texto, conhecidos):
    return []

texto = "The model overfits. Regularization reduces overfitting; dropout is a regularization technique. The model improves."
conhecidos = {"the", "model", "is", "a", "reduces", "improves"}
print(termos_novos(texto, conhecidos))
''',
            [("Ordem por frequência", "assert termos_novos(texto, conhecidos) == ['regularization', 'dropout', 'overfits', 'overfitting', 'technique'], f'{termos_novos(texto, conhecidos)}'")],
            '''
import re
from collections import Counter

def termos_novos(texto, conhecidos):
    palavras = re.findall(r"[a-z]+", texto.lower())
    c = Counter(p for p in palavras if len(p) >= 4 and p not in conhecidos)
    return sorted(c, key=lambda p: (-c[p], p))

texto = "The model overfits. Regularization reduces overfitting; dropout is a regularization technique. The model improves."
conhecidos = {"the", "model", "is", "a", "reduces", "improves"}
print(termos_novos(texto, conhecidos))
''', ["<code>re.findall(r\"[a-z]+\", texto.lower())</code> separa as palavras.", "Ordene com a chave <code>(-contagem, palavra)</code>."]),
        erros([("Esperar ficar fluente para começar a ler documentação.", "Ler documentação é o que deixa você fluente."), ("Traduzir tudo automaticamente.", "Use a tradução para destravar, não como muleta permanente."), ("Ignorar a pronúncia dos termos.", "Use o YouGlish para ouvir “cache”, “queue”, “data” ditos por nativos.")]),
        ponte("Trilha de Inglês", "<p>A trilha de Inglês deste roteiro trabalha conversação e escuta; esta aula foca o vocabulário técnico. Juntas, preparam você para vagas remotas e entrevistas em inglês.</p>"),
        quiz([
            ("“Bottleneck” significa:", ["Gargalo.", "Garrafa.", "Erro."], 0, "O ponto que limita."),
            ("Como ler um artigo com eficiência?", ["Em camadas: resumo, figuras, conclusão, depois detalhes.", "Palavra por palavra.", "Só o título."], 0, "Camadas."),
            ("Para pedir que alguém repita de outro jeito:", ["“Could you rephrase that?”", "“Repeat now!”", "“I don't care.”"], 0, "Educado e claro."),
        ]),
    ],
    ["Leia documentação todo dia, em camadas.", "Monte seu glossário com termos frequentes.", "Frases prontas para issues, commits e reuniões."],
    "Linux e shell avançado.",
    livro=("MLCC:", "Google Machine Learning Crash Course (em inglês)", "Leia o glossário do curso e escolha 10 termos para o seu vocabulário."), yg="trade-off")

AULAS["Currículo e entrevistas técnicas"] = aula(
    30,
    "Seu currículo tem 6 segundos para passar no primeiro olhar e, muitas vezes, precisa passar antes por um sistema automático. Na entrevista, você vai explicar projetos, resolver problemas e mostrar como pensa. Ambos se preparam com método.",
    ["escrever um currículo de uma página com resultados;", "contar projetos com o método STAR;", "preparar-se para as etapas técnicas comuns em vagas de IA."],
    ["Projetos, READMEs e LinkedIn."],
    [
        chute("Qual linha de currículo é mais forte?", ["“Responsável por modelos de machine learning.”", "“Criei um modelo de previsão de demanda que reduziu o estoque parado em 18% (Python, XGBoost, Airflow).”", "“Conhecimentos em Python, ML, DL, NLP, CV, LLM, SQL, AWS, GCP, Azure...”"], 1,
              ["Diz a função, não o resultado.", "Isso! Verbo de ação + o que fez + resultado com número + ferramentas.", "Lista sem evidência."],
              "Fiz X, medido por Y, usando Z."),
        concreto("O trailer do filme", "<p>O currículo é o trailer: mostra as melhores cenas em segundos e faz querer ver o filme (a entrevista). Na entrevista, você conta o filme inteiro, com começo, meio e fim.</p>"),
        nota("O método STAR para contar projetos", [
            ("S – Situação", "o contexto", "“A empresa perdia 5% dos clientes por mês.”"),
            ("T – Tarefa", "o seu objetivo", "“Eu precisava prever quem cancelaria.”"),
            ("A – Ação", "o que você fez", "“Juntei dados de uso, criei atributos, testei 3 modelos, publiquei uma API.”"),
            ("R – Resultado", "com números", "“Recall de 78%; a equipe de retenção reduziu cancelamentos em 12%.”"),
        ], rot="Agora sim, o método"),
        tabela("Etapas comuns em vagas de IA", ["Etapa", "Como se preparar"], [
            ["Triagem com RH", "saiba contar sua história em 2 minutos"],
            ["Teste de código / SQL", "pratique problemas de nível fácil a médio e SQL com joins e janelas"],
            ["Fundamentos de ML", "viés × variância, métricas, validação, vazamento, overfitting"],
            ["Estudo de caso / desenho de sistema", "do problema de negócio à métrica, dados, modelo, deploy e monitoramento"],
            ["Projeto para casa", "entregue como um projeto de portfólio: README, testes, decisões explicadas"],
            ["Comportamental", "3 a 5 histórias STAR prontas (conflito, erro, entrega difícil)"],
        ], rot="Organize na cabeça"),
        cod("Linha de currículo forte", "Escreva <code>avaliar_linha(linha)</code> que devolve uma nota de 0 a 3: +1 se começa com verbo de ação da lista, +1 se tem número (com ou sem %), +1 se cita alguma ferramenta da lista. Depois <code>melhorar(linhas)</code> devolve as linhas com nota menor que 2.",
            '''
VERBOS = {"criei", "desenvolvi", "reduzi", "automatizei", "liderei", "implementei", "aumentei"}
FERRAMENTAS = {"python", "sql", "pytorch", "docker", "aws", "airflow", "xgboost"}

def avaliar_linha(linha):
    return 0

def melhorar(linhas):
    return []

cv = [
    "Criei um modelo de churn com recall de 78% (Python, XGBoost).",
    "Responsável pela área de dados.",
    "Automatizei relatórios semanais com SQL.",
]
print([avaliar_linha(l) for l in cv], melhorar(cv))
''',
            [("Notas", "assert [avaliar_linha(l) for l in cv] == [3, 0, 2], f'{[avaliar_linha(l) for l in cv]}'"),
             ("Linhas fracas", "assert melhorar(cv) == ['Responsável pela área de dados.']")],
            '''
import re

VERBOS = {"criei", "desenvolvi", "reduzi", "automatizei", "liderei", "implementei", "aumentei"}
FERRAMENTAS = {"python", "sql", "pytorch", "docker", "aws", "airflow", "xgboost"}

def avaliar_linha(linha):
    palavras = re.findall(r"\\w+", linha.lower())
    nota = 0
    if palavras and palavras[0] in VERBOS:
        nota += 1
    if re.search(r"\\d", linha):
        nota += 1
    if FERRAMENTAS & set(palavras):
        nota += 1
    return nota

def melhorar(linhas):
    return [l for l in linhas if avaliar_linha(l) < 2]

cv = [
    "Criei um modelo de churn com recall de 78% (Python, XGBoost).",
    "Responsável pela área de dados.",
    "Automatizei relatórios semanais com SQL.",
]
print([avaliar_linha(l) for l in cv], melhorar(cv))
''', ["Separe palavras com <code>re.findall(r\"\\w+\", linha.lower())</code>.", "Número: <code>re.search(r\"\\d\", linha)</code>; ferramentas: interseção de conjuntos."]),
        erros([("Currículo de 3 páginas.", "Uma página para quem está começando; o resto fica no LinkedIn."), ("Mentir ou exagerar.", "A entrevista técnica descobre; seja preciso sobre o que você fez."), ("Não fazer perguntas no fim da entrevista.", "Pergunte sobre o time, os dados e os desafios: mostra interesse real.")]),
        pense("Sua história em 2 minutos", "Escreva em 4 frases: quem você é, o que já construiu, o que está aprendendo agora e que tipo de vaga procura.", "<p>Essa “apresentação pessoal” abre quase toda entrevista. Treine em voz alta até soar natural, e adapte para cada empresa.</p>"),
        quiz([
            ("Uma boa linha de currículo tem:", ["Verbo de ação, resultado com número e ferramentas.", "Só a lista de tecnologias.", "Adjetivos sobre você."], 0, "Fiz, medi, usei."),
            ("O que é o método STAR?", ["Situação, Tarefa, Ação, Resultado.", "Um framework de ML.", "Uma métrica."], 0, "Histórias estruturadas."),
            ("Num estudo de caso de ML, comece por:", ["O problema de negócio e a métrica.", "A arquitetura da rede.", "O nome do modelo."], 0, "Do problema à solução."),
        ]),
    ],
    ["Currículo de uma página com resultados em números.", "Histórias STAR para projetos e situações.", "Prepare código, SQL, fundamentos de ML e desenho de sistemas."],
    "Contribuir com open source.",
    livro=("MLCC:", "Google Machine Learning Crash Course", "Revise os módulos de métricas e de generalização: são perguntas clássicas de entrevista."))

AULAS["Contribuir com open source"] = aula(
    20,
    "As bibliotecas que você usa todo dia (pandas, scikit-learn, transformers) são feitas por milhares de pessoas, muitas voluntárias. Contribuir com elas ensina a trabalhar em código grande, com revisão de verdade, e deixa uma prova pública do seu trabalho.",
    ["encontrar uma primeira contribuição adequada;", "seguir o fluxo fork → branch → pull request;", "comunicar-se bem com os mantenedores."],
    ["Git, GitHub, testes e inglês técnico."],
    [
        chute("Qual é uma boa primeira contribuição?", ["Reescrever o módulo principal da biblioteca.", "Corrigir um erro na documentação ou resolver uma issue marcada como “good first issue”.", "Abrir um PR mudando o estilo de todo o código."], 1,
              ["Grande demais e sem contexto.", "Isso! Pequena, útil e bem-vinda: você aprende o processo sem travar.", "Mantenedores costumam recusar mudanças assim."],
              "Comece pequeno; o processo é o que você aprende primeiro."),
        concreto("O mutirão do bairro", "<p>No mutirão, ninguém chega reformando a praça sozinho. Você pergunta o que está precisando, pega uma tarefa, faz bem e mostra. Na próxima, já confiam em você para tarefas maiores.</p>"),
        passos("O fluxo de uma contribuição", [
            ("Leia o <code>CONTRIBUTING.md</code> e o código de conduta.", "Cada projeto tem suas regras."),
            ("Escolha uma issue (“good first issue”, “documentation”) e comente que vai trabalhar nela.", "Evita trabalho duplicado."),
            ("Faça o fork, clone e crie uma branch.", "<code>git switch -c corrige-docstring-merge</code>"),
            ("Faça a mudança, rode os testes e o linter do projeto.", "Siga o estilo existente."),
            ("Abra o pull request explicando o quê, por quê e como testou, citando a issue.", "“Fixes #1234”."),
            ("Responda às revisões com paciência e ajuste.", "Revisão não é crítica pessoal: é como projetos mantêm qualidade."),
        ]),
        cod("Escrevendo um bom pull request", "Escreva <code>descricao_pr(titulo, problema, mudanca, testes, issue)</code> que monta a descrição em Markdown com as seções <code>## What</code>, <code>## Why</code>, <code>## How I tested</code> e a linha final <code>Fixes #N</code>. Rejeite (<code>ValueError</code>) títulos com mais de 72 caracteres.",
            '''
def descricao_pr(titulo, problema, mudanca, testes, issue):
    return ""

print(descricao_pr("Fix typo in merge docstring", "The docstring says 'colum'.", "Corrected to 'column'.", "Built the docs locally.", 1234))
''',
            [("Seções", "d = descricao_pr('Fix typo', 'p', 'm', 't', 7)\nassert d.startswith('# Fix typo') and '## What\\nm' in d and '## Why\\np' in d and '## How I tested\\nt' in d and d.rstrip().endswith('Fixes #7'), repr(d)"),
             ("Título longo", "try:\n    descricao_pr('x' * 80, 'p', 'm', 't', 1)\n    ok = False\nexcept ValueError:\n    ok = True\nassert ok")],
            '''
def descricao_pr(titulo, problema, mudanca, testes, issue):
    if len(titulo) > 72:
        raise ValueError("título longo demais")
    return "\\n\\n".join([f"# {titulo}", f"## What\\n{mudanca}", f"## Why\\n{problema}", f"## How I tested\\n{testes}", f"Fixes #{issue}"])

print(descricao_pr("Fix typo in merge docstring", "The docstring says 'colum'.", "Corrected to 'column'.", "Built the docs locally.", 1234))
''', ["Junte as partes com <code>\"\\n\\n\".join([...])</code>.", "Cheque o tamanho do título antes."]),
        erros([("PR enorme sem conversa prévia.", "Para mudanças grandes, abra uma issue e discuta antes."), ("Sumir depois da primeira revisão.", "Responda; se não puder continuar, avise."), ("Contribuições automáticas de baixa qualidade.", "PRs gerados sem entender o código atrapalham os mantenedores e queimam sua reputação.")]),
        ponte("Outras formas de contribuir", "<p>Responder dúvidas em fóruns, melhorar exemplos, traduzir documentação para o português, reportar bugs bem descritos e publicar datasets ou modelos no Hugging Face também são contribuições valiosas.</p>"),
        quiz([
            ("Antes de começar numa issue, você deve:", ["Ler o CONTRIBUTING e avisar na issue.", "Abrir o PR direto.", "Mudar tudo."], 0, "Combine antes."),
            ("Uma boa descrição de PR explica:", ["O quê, por quê e como foi testado.", "Só o título.", "Nada."], 0, "Contexto."),
            ("Como receber uma revisão com críticas?", ["Como parte normal do processo, ajustando o código.", "Fechando o PR.", "Discutindo pessoalmente."], 0, "Qualidade."),
        ]),
    ],
    ["Comece por documentação e “good first issues”.", "Fork, branch, testes, PR bem descrito.", "Comunicação paciente com os mantenedores."],
    "Escrever artigos e posts.",
    livro=("PROGIT:x", "Pro Git, capítulo 6, “Contribuindo para um projeto”", "Como o livro descreve o fluxo de fork e pull request?"))

AULAS["Escrever artigos e posts"] = aula(
    20,
    "Escrever sobre o que você aprende tem três efeitos: você entende melhor (explicar exige clareza), as pessoas encontram você e seu trabalho, e você constrói um histórico público de evolução. Não precisa ser especialista: explicar algo que você acabou de aprender ajuda quem está um passo atrás.",
    ["escolher temas que ajudam leitores;", "estruturar um artigo técnico curto;", "adaptar o mesmo conteúdo para post, artigo e thread."],
    ["READMEs, storytelling com dados e LinkedIn."],
    [
        chute("Qual título tende a atrair mais leitores?", ["“Minhas reflexões sobre machine learning”.", "“Como reduzi pela metade o custo do meu RAG com cache de prompt (com código)”.", "“Artigo 7”."], 1,
              ["Vago: o leitor não sabe o que vai ganhar.", "Isso! Promete um resultado concreto e útil.", "Não diz nada."],
              "Título = o que o leitor vai conseguir."),
        concreto("O professor de um passo à frente", "<p>Quem acabou de aprender lembra exatamente onde travou, coisa que o especialista já esqueceu. Por isso, explicações de quem está “um passo à frente” costumam ser as mais claras para iniciantes.</p>"),
        passos("Estrutura de um artigo técnico", [
            ("<b>Gancho</b>: o problema em 2 frases.", "“Meu RAG custava 900 reais por mês...”"),
            ("<b>Contexto</b>: o mínimo para entender.", "Sem história longa."),
            ("<b>Solução passo a passo</b>, com código curto e imagens.", "Um passo por seção."),
            ("<b>Resultado</b> com números.", "Antes e depois."),
            ("<b>Lições e limitações</b>.", "O que você faria diferente."),
            ("<b>Chamada final</b>: link para o repositório.", "Convide a comentar."),
        ]),
        cod("Calculadora de leitura", "Ajude a revisar o texto: <code>analisar(texto)</code> devolve o tempo de leitura em minutos (200 palavras por minuto, arredondado para cima, mínimo 1), o número de frases longas (mais de 25 palavras) e a média de palavras por frase (arredondada a 1 casa).",
            '''
import math, re

def analisar(texto):
    return {"minutos": 0, "frases_longas": 0, "media": 0.0}

texto = "Meu RAG estava caro. " + "Esta frase tem muitas palavras para mostrar como frases longas cansam o leitor e escondem a ideia principal do parágrafo inteiro que você mesmo escreveu hoje. " + "Cortei pela metade."
print(analisar(texto))
''',
            [("Análise", "r = analisar(texto)\nassert r['minutos'] == 1 and r['frases_longas'] == 1 and r['media'] == round((4 + 26 + 3) / 3, 1), f'{r}'"),
             ("Tempo maior", "assert analisar('palavra. ' * 450)['minutos'] == 3")],
            '''
import math, re

def analisar(texto):
    frases = [f for f in re.split(r"[.!?]+", texto) if f.strip()]
    tamanhos = [len(f.split()) for f in frases]
    total = sum(tamanhos)
    return {
        "minutos": max(1, math.ceil(total / 200)),
        "frases_longas": sum(t > 25 for t in tamanhos),
        "media": round(total / len(frases), 1) if frases else 0.0,
    }

texto = "Meu RAG estava caro. " + "Esta frase tem muitas palavras para mostrar como frases longas cansam o leitor e escondem a ideia principal do parágrafo inteiro que você mesmo escreveu hoje. " + "Cortei pela metade."
print(analisar(texto))
''', ["Separe frases com <code>re.split(r\"[.!?]+\", texto)</code> e descarte as vazias.", "Minutos: <code>max(1, math.ceil(total / 200))</code>."]),
        tabela("Um conteúdo, vários formatos", ["Formato", "Tamanho", "Onde"], [
            ["Artigo completo", "800 a 1500 palavras", "blog, Medium, dev.to, Substack"],
            ["Post", "150 a 300 palavras + imagem", "LinkedIn"],
            ["Sequência curta", "5 a 8 partes", "redes de texto curto"],
            ["Vídeo curto", "1 a 3 minutos", "YouTube, Instagram"],
        ], rot="Organize na cabeça"),
        erros([("Esperar ser especialista para escrever.", "Escreva sobre o que acabou de aprender."), ("Textos gerados por IA sem revisão.", "Leitores percebem; use a IA para revisar, não para pensar por você."), ("Código que não roda.", "Teste todos os trechos antes de publicar.")]),
        ponte("Seu portfólio escrito", "<p>Cada projeto do portfólio pode virar um artigo: o README já tem problema, solução e resultados. Em um ano, 10 artigos curtos formam uma prova pública poderosa do que você sabe.</p>"),
        quiz([
            ("Um bom título técnico:", ["Promete um resultado concreto.", "É misterioso.", "É longo e vago."], 0, "Valor claro."),
            ("Por que escrever sobre o que acabou de aprender?", ["Você lembra das dificuldades de quem está começando.", "É mais rápido.", "Não deveria."], 0, "Um passo à frente."),
            ("Antes de publicar código num artigo:", ["Teste todos os trechos.", "Não precisa testar.", "Apague os comentários."], 0, "Confiança."),
        ]),
    ],
    ["Escreva sobre problemas resolvidos, com resultados.", "Gancho, contexto, passos, resultado, lições.", "Reaproveite em post, artigo e vídeo."],
    "Comunidades e eventos.",
    livro=("PROGIT:x", "Pro Git (em português)", "Escolha um tema do livro e escreva um post curto explicando-o com suas palavras."))

AULAS["Comunidades e eventos"] = aula(
    15,
    "Estudar sozinho é possível, mas lento e solitário. Em comunidades você tira dúvidas, descobre vagas antes de serem anunciadas, encontra parceiros de projeto e mentores. E eventos (online ou presenciais) transformam contatos virtuais em relações.",
    ["encontrar comunidades de IA e dados em português;", "participar de forma útil, não só pedindo;", "aproveitar eventos e meetups."],
    ["LinkedIn e escrita de posts."],
    [
        chute("Qual a forma mais eficaz de se destacar numa comunidade?", ["Pedir vagas em todos os canais.", "Ajudar: responder dúvidas, compartilhar o que aprendeu, organizar algo.", "Só observar."], 1,
              ["Cansa as pessoas rapidamente.", "Isso! Quem ajuda é lembrado, e as oportunidades chegam como consequência.", "Observar é um começo, mas não cria relações."],
              "Dê antes de pedir."),
        concreto("O time de futebol do bairro", "<p>No time do bairro, você conhece gente que trabalha em todo tipo de lugar. Quando surge uma vaga, lembram de quem sempre aparece, joga junto e ajuda a montar as traves. Comunidades técnicas funcionam do mesmo jeito.</p>"),
        tabela("Onde procurar", ["Tipo", "Exemplos"], [
            ["Grupos de usuários", "Python Brasil, PyLadies, grupos locais de Python e de dados"],
            ["Comunidades online", "Discord e Slack de dados e IA, fóruns do Hugging Face e do Kaggle"],
            ["Eventos", "Python Brasil (conferência), meetups locais, hackathons, eventos de universidades"],
            ["Grupos de estudo", "crie um com 3 a 5 pessoas seguindo este roteiro"],
        ], rot="Organize na cabeça"),
        passos("Aproveitando um evento", [
            ("Antes: veja a programação e escolha 2 ou 3 palestras.", "E quem você gostaria de conhecer."),
            ("Durante: faça uma pergunta e converse nos intervalos.", "“O que você está construindo?” abre qualquer conversa."),
            ("Depois: conecte-se no LinkedIn com uma mensagem personalizada.", "“Gostei da sua palestra sobre RAG; testei a ideia do reranking.”"),
            ("Compartilhe um resumo do que aprendeu.", "Marque os palestrantes."),
            ("Um dia, proponha uma palestra relâmpago.", "Contar um projeto seu em 5 minutos já é muito valioso."),
        ]),
        pense("Seu primeiro passo", "Qual comunidade ou evento você pode experimentar nas próximas duas semanas? E o que pode oferecer a ela?", "<p>Comece pequeno: entrar num grupo, apresentar-se e responder uma dúvida que você sabe. Seu resumo de uma aula deste roteiro já pode ajudar alguém.</p>"),
        erros([("Entrar em 30 grupos e não participar de nenhum.", "Escolha 2 ou 3 e participe de verdade."), ("Mensagem genérica pedindo indicação.", "Construa a relação antes; peça algo específico."), ("Achar que eventos são só para quem já trabalha na área.", "Iniciantes são muito bem-vindos, e voluntariar é uma ótima porta.")]),
        ponte("Rede é longo prazo", "<p>As melhores oportunidades costumam vir de pessoas que viram seu trabalho ao longo do tempo. Participar com constância, mesmo pouco, rende mais do que uma grande ação isolada.</p>"),
        quiz([
            ("Qual atitude mais gera oportunidades?", ["Ajudar e compartilhar.", "Pedir vagas sempre.", "Ficar em silêncio."], 0, "Dê antes de pedir."),
            ("Depois de um evento, o ideal é:", ["Conectar-se com mensagem personalizada.", "Esquecer.", "Mandar currículo para todos."], 0, "Continuidade."),
            ("Quantas comunidades acompanhar de perto?", ["2 ou 3, com participação real.", "Todas que existirem.", "Nenhuma."], 0, "Profundidade."),
        ]),
    ],
    ["Comunidades aceleram aprendizado e oportunidades.", "Participe ajudando; peça depois.", "Eventos: preparar, conversar, conectar, compartilhar."],
    "Certificações (opcional).",
    livro=("MISSING:course-shell", "Missing Semester (MIT)", "Monte com sua comunidade um grupo de estudo para uma das aulas."))

AULAS["Certificações (opcional)"] = aula(
    15,
    "Certificações não substituem projetos, mas podem ajudar: passam em filtros de RH, estruturam o estudo e são valorizadas por consultorias e empresas que usam uma nuvem específica. A chave é escolher poucas, alinhadas à vaga que você quer.",
    ["saber quando uma certificação vale a pena;", "conhecer as principais em nuvem e IA;", "estudar de forma prática, não só para a prova."],
    ["Deploy em nuvem e currículo."],
    [
        chute("Quando uma certificação de nuvem costuma valer mais a pena?", ["Sempre, em qualquer vaga.", "Quando as vagas que você quer pedem aquela nuvem, ou para consultorias parceiras do provedor.", "Nunca."], 1,
              ["Muitas vagas não pedem.", "Isso! Alinhe a certificação ao mercado que você quer.", "Elas têm valor em contextos específicos."],
              "Certificação é complemento, não substituto do portfólio."),
        concreto("A carteira de motorista", "<p>A carteira prova que você passou no teste, mas o que te faz bom motorista é dirigir. Certificações são a carteira; projetos são a estrada. As duas juntas abrem mais portas.</p>"),
        tabela("Algumas opções", ["Certificação", "Para quem"], [
            ["AWS Certified Cloud Practitioner / AI Practitioner", "primeiro contato com AWS e IA na AWS"],
            ["AWS Machine Learning Engineer – Associate", "ML em produção na AWS"],
            ["Google Cloud Professional Machine Learning Engineer", "ML em produção no GCP"],
            ["Microsoft Azure AI Engineer Associate", "IA aplicada no Azure"],
            ["TensorFlow / cursos com certificado (DeepLearning.AI, Hugging Face)", "comprovar estudo estruturado"],
        ], rot="Organize na cabeça"),
        cod("Vale a pena?", "Ajude a decidir: <code>vale_a_pena(cert, vagas, horas_livres_semana)</code> devolve <code>True</code> se pelo menos 30% das vagas citam a nuvem da certificação e se as horas de estudo cabem em até 12 semanas.",
            '''
CERTS = {
    "aws-ml": {"nuvem": "aws", "horas": 80},
    "gcp-ml": {"nuvem": "gcp", "horas": 100},
}

def vale_a_pena(cert, vagas, horas_livres_semana):
    return True

vagas = ["Python, AWS, SageMaker", "GCP, BigQuery", "AWS, Docker", "Azure, Python", "AWS, Spark"]
print(vale_a_pena("aws-ml", vagas, 8), vale_a_pena("gcp-ml", vagas, 8))
''',
            [("AWS vale", "assert vale_a_pena('aws-ml', vagas, 8) is True"),
             ("GCP aparece pouco", "assert vale_a_pena('gcp-ml', vagas, 20) is False"),
             ("Sem tempo", "assert vale_a_pena('aws-ml', vagas, 5) is False")],
            '''
CERTS = {
    "aws-ml": {"nuvem": "aws", "horas": 80},
    "gcp-ml": {"nuvem": "gcp", "horas": 100},
}

def vale_a_pena(cert, vagas, horas_livres_semana):
    c = CERTS[cert]
    fracao = sum(c["nuvem"] in v.lower() for v in vagas) / len(vagas)
    semanas = c["horas"] / horas_livres_semana
    return fracao >= 0.3 and semanas <= 12

vagas = ["Python, AWS, SageMaker", "GCP, BigQuery", "AWS, Docker", "Azure, Python", "AWS, Spark"]
print(vale_a_pena("aws-ml", vagas, 8), vale_a_pena("gcp-ml", vagas, 8))
''', ["Fração = vagas que citam a nuvem / total.", "Semanas = horas da certificação / horas livres por semana."]),
        erros([("Colecionar certificados sem projetos.", "Sem prática, a entrevista técnica revela."), ("Decorar simulados.", "Construa algo com os serviços enquanto estuda."), ("Pagar caro por certificados de cursos desconhecidos.", "Prefira os oficiais dos provedores ou de instituições reconhecidas.")]),
        ponte("Fim do roteiro, começo da carreira", "<p>Você percorreu Python, dados, machine learning, deep learning, LLMs e engenharia. O próximo passo é continuar construindo, publicando e conversando com pessoas da área. Boa jornada!</p>"),
        quiz([
            ("Certificações substituem projetos?", ["Não, complementam.", "Sim.", "Às vezes, sempre."], 0, "Complemento."),
            ("Como escolher uma certificação?", ["Pelas vagas que você quer.", "Pela mais cara.", "Ao acaso."], 0, "Alinhamento."),
            ("Melhor forma de estudar para uma certificação técnica:", ["Construindo algo com os serviços.", "Só decorando simulados.", "Não estudar."], 0, "Prática."),
        ]),
    ],
    ["Certificação é complemento do portfólio.", "Escolha pela nuvem e pelas vagas que você quer.", "Estude construindo."],
    "Revise seus projetos e siga construindo.",
    livro=("FASTAPI:deployment", "Documentação do FastAPI, “Implantação”", "Que conceitos de produção aparecem também nas provas de certificação de nuvem?"))
