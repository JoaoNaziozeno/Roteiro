# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 1 (parte B): arquivos, erros, ferramentas e boas práticas."""
from lesson_factory import *

AULAS = {}

AULAS["Arquivos (ler e escrever)"] = aula(
    35,
    "Quando o programa termina, as variáveis somem. Para que algo sobreviva (um resultado, um log de treino, um dataset), ele precisa ir para um <b>arquivo</b>.",
    ["abrir arquivos com <code>with open(...)</code>;", "ler tudo, ler linha por linha e gravar;", "escolher o modo certo: <code>r</code>, <code>w</code> ou <code>a</code>."],
    ["Laços, listas e funções."],
    [
        chute("O arquivo <code>notas.txt</code> já tem 3 linhas. Depois de rodar o código, quantas linhas ele tem?", ["4", "1", "3"], 1,
              ["Seria 4 com o modo <code>\"a\"</code> (acrescentar).", "Isso! O modo <code>\"w\"</code> <b>apaga tudo</b> e começa do zero.", "O arquivo é reescrito, não fica como estava."],
              "<code>\"w\"</code> é o modo mais perigoso: sobrescreve sem perguntar.",
              cod='with open("notas.txt", "w") as f:\n    f.write("nova linha\\n")'),
        concreto("O caderno", "<p>Para usar um caderno você <b>abre</b>, <b>lê ou escreve</b> e <b>fecha</b>. Com arquivos é igual. O <code>with</code> é o amigo que fecha o caderno por você, mesmo que algo dê errado no meio.</p>"),
        crianca("<p>Três jeitos de abrir: <b>r</b> é “só quero ler”. <b>w</b> é “arranca todas as folhas e começa de novo”. <b>a</b> é “continua escrevendo depois da última linha”.</p>"),
        ver("como o professor abre, grava e fecha um arquivo"),
        nota("Abrir, ler e gravar", [
            ("<code>with open(\"a.txt\", \"r\", encoding=\"utf-8\") as f:</code>", "abrir para leitura", "O <code>with</code> fecha o arquivo sozinho no fim do bloco. <code>encoding=\"utf-8\"</code> evita problemas com acentos."),
            ("<code>f.read()</code>", "ler tudo", "Devolve o arquivo inteiro como um texto."),
            ("<code>for linha in f:</code>", "linha por linha", "Bom para arquivos grandes. Cada linha vem com <code>\\n</code> no final: use <code>.strip()</code>."),
            ("<code>f.write(\"texto\\n\")</code>", "gravar", "Não pula linha sozinho: inclua o <code>\\n</code>."),
        ]),
        passos("Gravando e lendo um log", [
            ("<code>with open(\"log.txt\", \"w\", encoding=\"utf-8\") as f:</code>", "Cria (ou zera) o arquivo."),
            ("<code>f.write(\"epoca 1: 0.9\\n\")</code>", "Uma linha por registro."),
            ("Fim do <code>with</code>.", "O arquivo é fechado e os dados vão de fato para o disco."),
            ("Reabra com <code>\"r\"</code> e percorra com <code>for linha in f</code>.", "Cada volta entrega uma linha."),
        ]),
        cod("Salvando e somando notas", "Grave as notas em <code>notas.txt</code>, uma por linha. Depois <b>leia o arquivo</b> e imprima a soma.",
            '''
notas = [7.5, 8.0, 6.5]

# 1) grave cada nota em uma linha de notas.txt

# 2) leia o arquivo e some os valores
soma = 0

print(soma)
''',
            [("Imprime 22.0", "assert saida.strip() == '22.0', f'saiu {saida.strip()!r}'"),
             ("O arquivo tem 3 linhas", "linhas = open('notas.txt', encoding='utf-8').read().split()\nassert linhas == ['7.5', '8.0', '6.5'], f'arquivo: {linhas}'")],
            '''
notas = [7.5, 8.0, 6.5]

with open("notas.txt", "w", encoding="utf-8") as f:
    for n in notas:
        f.write(f"{n}\\n")

soma = 0
with open("notas.txt", encoding="utf-8") as f:
    for linha in f:
        soma += float(linha.strip())

print(soma)
''', ["Grave com <code>f.write(f\"{n}\\n\")</code>.", "Ao ler, converta: <code>float(linha.strip())</code>."]),
        erros([
            ("Abrir com <code>\"w\"</code> um arquivo que você queria manter.", "Tudo é apagado na hora. Para acrescentar, use <code>\"a\"</code>."),
            ("Esquecer o <code>\\n</code> ao gravar.", "Tudo fica grudado numa linha só."),
            ("Não usar <code>with</code> e esquecer de fechar.", "Os dados podem não ser gravados. O <code>with</code> resolve."),
            ("Acentos virando símbolos estranhos.", "Passe sempre <code>encoding=\"utf-8\"</code>."),
        ]),
        ponte("Arquivos no ciclo de um modelo",
              "<p>Datasets chegam em arquivos (<code>.csv</code>, <code>.json</code>, <code>.parquet</code>), logs de treino são gravados linha a linha, e o próprio modelo treinado é salvo num arquivo de pesos (<code>.pt</code>, <code>.safetensors</code>). Ler e gravar com segurança é o que impede perder horas de GPU.</p>"),
        quiz([
            ("Qual modo acrescenta ao final sem apagar?", ["<code>\"w\"</code>", "<code>\"a\"</code>", "<code>\"r\"</code>"], 1, "<code>a</code> de <i>append</i>."),
            ("Por que usar <code>with open(...)</code>?", ["É mais rápido.", "O arquivo é fechado automaticamente.", "Permite ler arquivos maiores."], 1, "Mesmo se ocorrer um erro no bloco."),
            ("O que <code>linha.strip()</code> remove ao ler um arquivo?", ["As vogais.", "Espaços e a quebra de linha das pontas.", "A primeira palavra."], 1, "Cada linha lida termina com <code>\\n</code>."),
        ]),
    ],
    ["<code>with open(arquivo, modo, encoding=\"utf-8\")</code> abre e fecha com segurança.", "<code>r</code> lê, <code>w</code> sobrescreve, <code>a</code> acrescenta.", "Ao ler, limpe o <code>\\n</code>; ao gravar, inclua-o."],
    "Tratamento de erros: o programa que não quebra.",
    livro=("ATBS:9", "Capítulo 9, “Reading and Writing Files”", "Qual a diferença entre caminho absoluto e relativo segundo o livro?"))

AULAS["Tratamento de erros (try/except)"] = aula(
    35,
    "O usuário digita “dez” onde você esperava 10. A internet cai no meio do download. O arquivo não existe. Programas reais não podem simplesmente morrer: eles precisam <b>tentar</b> e, se der errado, <b>reagir</b>.",
    ["capturar erros com <code>try</code> / <code>except</code>;", "capturar o erro certo, e não todos;", "usar <code>else</code>, <code>finally</code> e <code>raise</code>."],
    ["Funções e arquivos."],
    [
        chute("O que esse código imprime?", ["Nada, o programa quebra", "erro e depois fim", "fim"], 1,
              ["Sem o <code>try</code> quebraria. Com ele, o erro é capturado.", "Isso! A divisão por zero pula para o <code>except</code>, e o programa <b>continua</b> depois.", "O <code>except</code> também roda, antes."],
              "Depois de tratado, o erro deixa de ser fatal.",
              cod='try:\n    x = 10 / 0\nexcept ZeroDivisionError:\n    print("erro")\nprint("fim")'),
        concreto("A rede do trapezista", "<p>O trapezista <b>tenta</b> o salto. Se cair, a <b>rede</b> segura e o show continua. O <code>try</code> é o salto; o <code>except</code> é a rede.</p>"),
        crianca("<p>“<b>Tenta</b> abrir o pote. <b>Se</b> estiver emperrado, pede ajuda. <b>De qualquer jeito</b>, guarda o pote no armário depois.” Tentar, reagir e arrumar a bagunça: <code>try</code>, <code>except</code>, <code>finally</code>.</p>"),
        ver("os tipos de erro que o professor provoca de propósito"),
        nota("As quatro partes", [
            ("<code>try:</code>", "tente", "O código que pode falhar."),
            ("<code>except ValueError:</code>", "exceto se", "Roda só se ocorrer aquele tipo de erro. <code>except ValueError as e</code> guarda a mensagem em <code>e</code>."),
            ("<code>else:</code>", "senão", "Roda se <b>não</b> houve erro."),
            ("<code>finally:</code>", "por fim", "Roda sempre, com erro ou sem. Bom para fechar e limpar."),
            ("<code>raise ValueError(\"msg\")</code>", "levante", "Você mesmo dispara um erro quando algo está errado."),
        ]),
        passos("Lendo um número com segurança", [
            ("<code>try: n = int(texto)</code>", "Se <code>texto</code> for “dez”, <code>int</code> dispara <code>ValueError</code>."),
            ("<code>except ValueError: n = 0</code>", "Só esse tipo de erro é tratado; os outros continuam aparecendo."),
            ("O programa segue com um valor válido.", "Em vez de morrer, ele se recupera."),
        ], fim="Leia sempre a <b>última linha</b> do traceback: ela diz o tipo do erro e a mensagem."),
        cod("Conversão segura", "Devolva o número inteiro do texto; se o texto não for um número, devolva o valor <code>padrao</code>.",
            '''
def para_inteiro(texto, padrao=0):
    return int(texto)

print(para_inteiro("42"), para_inteiro("abc"), para_inteiro("x", -1))
''',
            [("Texto numérico", "assert para_inteiro('42') == 42"), ("Texto inválido devolve 0", "assert para_inteiro('abc') == 0"), ("Padrão escolhido", "assert para_inteiro('x', -1) == -1")],
            '''
def para_inteiro(texto, padrao=0):
    try:
        return int(texto)
    except ValueError:
        return padrao

print(para_inteiro("42"), para_inteiro("abc"), para_inteiro("x", -1))
''', ["Envolva o <code>int(texto)</code> num <code>try</code>.", "Capture <code>ValueError</code> e devolva <code>padrao</code>."]),
        cod("Validando uma entrada", "Um modelo só aceita taxa de aprendizado entre 0 e 1 (sem incluir o 0). Faça a função <b>disparar</b> <code>ValueError</code> quando o valor for inválido e devolver o valor quando for válido.",
            '''
def validar_taxa(taxa):
    return taxa

print(validar_taxa(0.01))
''',
            [("Valor válido passa", "assert validar_taxa(0.01) == 0.01 and validar_taxa(1) == 1"),
             ("Zero é inválido", "try:\n    validar_taxa(0)\n    ok = False\nexcept ValueError:\n    ok = True\nassert ok, 'taxa 0 deveria disparar ValueError'"),
             ("Maior que 1 é inválido", "try:\n    validar_taxa(1.5)\n    ok = False\nexcept ValueError:\n    ok = True\nassert ok, 'taxa 1.5 deveria disparar ValueError'")],
            '''
def validar_taxa(taxa):
    if not 0 < taxa <= 1:
        raise ValueError(f"taxa inválida: {taxa}")
    return taxa

print(validar_taxa(0.01))
''', ["<code>raise ValueError(\"mensagem\")</code> dispara o erro."], rot="Mão no código · nível 2"),
        erros([
            ("<code>except:</code> sem dizer o tipo.", "Engole <b>qualquer</b> erro, inclusive os de digitação no seu código. Capture o erro específico."),
            ("<code>except Exception: pass</code>", "O erro some em silêncio e o bug vira um mistério. No mínimo, registre a mensagem."),
            ("Colocar o programa inteiro dentro de um <code>try</code>.", "Envolva só a linha que pode falhar."),
        ]),
        ponte("Erros que você vai ver em IA",
              "<p>Chamadas a APIs de LLM falham por limite de uso ou instabilidade de rede: o padrão é <code>try</code> + nova tentativa com espera crescente. No treino, <code>finally</code> salva um checkpoint mesmo se algo quebrar. E validar entradas com <code>raise</code> evita treinar por horas com um parâmetro errado.</p>"),
        quiz([
            ("Quando o bloco <code>finally</code> roda?", ["Só se houver erro.", "Sempre.", "Só se não houver erro."], 1, "Com ou sem erro."),
            ("Por que evitar <code>except:</code> genérico?", ["É mais lento.", "Esconde erros que você não previu.", "Não funciona em Python 3."], 1, "Bugs reais passam despercebidos."),
            ("O que <code>raise</code> faz?", ["Ignora o erro.", "Dispara um erro de propósito.", "Repete o <code>try</code>."], 1, "Serve para recusar valores inválidos."),
        ]),
    ],
    ["<code>try</code> tenta; <code>except TipoDoErro</code> reage; <code>finally</code> roda sempre.", "Capture erros específicos e nunca os engula em silêncio.", "<code>raise</code> dispara um erro quando a entrada é inválida."],
    "Ambientes virtuais e pip: instalar bibliotecas sem bagunça.",
    livro=("PYDOC:errors", "Seções 8.3 e 8.4 (tratando e levantando exceções)", "Que exemplo o tutorial usa com vários except?"))

AULAS["Ambientes virtuais e pip"] = aula(
    30,
    "Projeto A precisa do pandas 1.5. Projeto B, do 2.2. Instalar tudo junto é receita para “na minha máquina funcionava”. Cada projeto merece a sua própria caixa de bibliotecas.",
    ["criar e ativar um ambiente virtual com <code>venv</code>;", "instalar pacotes com <code>pip</code>;", "registrar as dependências em <code>requirements.txt</code>."],
    ["Terminal e módulos."],
    [
        chute("Você instalou <code>requests</code> com o ambiente virtual <b>desativado</b> e depois ativou o ambiente. O <code>import requests</code> funciona dentro dele?", ["Sim, o pip instala para todos.", "Não: foi instalado fora do ambiente.", "Só no Windows."], 1,
              ["Cada ambiente tem sua própria pasta de pacotes.", "Isso! O pacote foi para o Python global. O ambiente virtual é isolado e não o enxerga.", "O comportamento é igual em todos os sistemas."],
              "Regra de ouro: <b>ative o ambiente antes</b> de qualquer <code>pip install</code>."),
        concreto("Uma cozinha por receita", "<p>Imagine que cada receita tivesse sua <b>própria despensa</b>, com exatamente os ingredientes e as marcas que ela pede. Nada vence, nada se mistura. Um ambiente virtual é essa despensa: uma pasta com um Python e as bibliotecas daquele projeto.</p>"),
        crianca("<p>É como ter uma <b>caixa de brinquedos para cada brincadeira</b>. As peças do Lego não se misturam com as do quebra-cabeça, e nenhuma some.</p>"),
        nota("Os comandos", [
            ("<code>python -m venv .venv</code>", "criar", "Cria a pasta <code>.venv</code> com o ambiente."),
            ("<code>.venv\\Scripts\\activate</code>", "ativar (Windows)", "No Mac e no Linux: <code>source .venv/bin/activate</code>. O nome do ambiente aparece no início da linha do terminal."),
            ("<code>pip install pandas</code>", "instalar", "Baixa a biblioteca para o ambiente ativo."),
            ("<code>pip freeze &gt; requirements.txt</code>", "registrar", "Grava a lista de pacotes e versões."),
            ("<code>pip install -r requirements.txt</code>", "reinstalar", "Recria o ambiente em outra máquina."),
        ], rot="Agora sim, os comandos"),
        passos("Começando um projeto do jeito certo", [
            ("<code>mkdir meu_projeto</code> e <code>cd meu_projeto</code>", "Uma pasta por projeto."),
            ("<code>python -m venv .venv</code>", "Cria o ambiente dentro do projeto."),
            ("Ative o ambiente.", "A partir daqui, <code>python</code> e <code>pip</code> são os do ambiente."),
            ("<code>pip install requests</code> e <code>pip freeze &gt; requirements.txt</code>", "Instala e registra."),
            ("Adicione <code>.venv</code> ao <code>.gitignore</code>.", "O ambiente não vai para o Git; o <code>requirements.txt</code> vai."),
        ]),
        ordem("A ordem certa dos comandos",
              ["python -m venv .venv", ".venv\\Scripts\\activate", "pip install pandas", "pip freeze > requirements.txt"],
              corpo="<p>Ordene os comandos para começar um projeto no Windows.</p>",
              exp="<p>Criar, ativar, instalar, registrar. Instalar antes de ativar manda o pacote para o lugar errado.</p>"),
        cod("Lendo um requirements.txt", "Complete a função que recebe o texto de um <code>requirements.txt</code> e devolve um dicionário <code>{pacote: versão}</code>. Ignore linhas vazias e comentários (<code>#</code>).",
            '''
def ler_requisitos(texto):
    pacotes = {}
    for linha in texto.splitlines():
        pass
    return pacotes

print(ler_requisitos("pandas==2.2.0\\n# dados\\nnumpy==1.26.4\\n"))
''',
            [("Lê dois pacotes", "assert ler_requisitos('pandas==2.2.0\\n# dados\\nnumpy==1.26.4\\n') == {'pandas': '2.2.0', 'numpy': '1.26.4'}"),
             ("Ignora vazias e comentários", "assert ler_requisitos('\\n# x\\n  \\n') == {}")],
            '''
def ler_requisitos(texto):
    pacotes = {}
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        nome, versao = linha.split("==")
        pacotes[nome] = versao
    return pacotes

print(ler_requisitos("pandas==2.2.0\\n# dados\\nnumpy==1.26.4\\n"))
''', ["<code>linha.strip()</code>, depois pule se estiver vazia ou começar com <code>#</code>.", "<code>nome, versao = linha.split(\"==\")</code>"]),
        erros([
            ("Instalar tudo no Python global.", "Com o tempo, versões entram em conflito. Um ambiente por projeto."),
            ("Subir a pasta <code>.venv</code> para o GitHub.", "São centenas de MB que não funcionam em outra máquina. Suba só o <code>requirements.txt</code>."),
            ("Esquecer de ativar ao abrir um terminal novo.", "Confira se o <code>(.venv)</code> aparece no início da linha."),
        ]),
        ponte("Por que isso é crítico em IA",
              "<p>PyTorch, CUDA, transformers: as bibliotecas de IA mudam rápido e uma versão errada quebra o treino. Um <code>requirements.txt</code> com versões fixas é o que permite a outra pessoa (ou a você, daqui a seis meses) reproduzir o resultado. Ferramentas como <code>conda</code>, <code>uv</code> e Docker são evoluções desta mesma ideia.</p>"),
        quiz([
            ("Para que serve um ambiente virtual?", ["Deixar o Python mais rápido.", "Isolar as bibliotecas de cada projeto.", "Rodar código sem instalar o Python."], 1, "Cada projeto com suas versões."),
            ("O que deve ir para o Git?", ["A pasta <code>.venv</code>.", "O <code>requirements.txt</code>.", "Os dois."], 1, "O ambiente se recria a partir do arquivo."),
            ("Como recriar o ambiente em outra máquina?", ["<code>pip install -r requirements.txt</code>", "<code>pip freeze</code>", "<code>python requirements.txt</code>"], 0, "<code>-r</code> lê a lista do arquivo."),
        ]),
    ],
    ["Um ambiente virtual por projeto: <code>python -m venv .venv</code>.", "Ative antes de instalar com <code>pip</code>.", "<code>requirements.txt</code> torna o projeto reproduzível."],
    "Git: uma máquina do tempo para o seu código.",
    livro=("PYDOC:venv", "Capítulo 12, “Ambientes virtuais e pacotes”", "Como o tutorial explica o problema que os ambientes resolvem?"))

AULAS["Git: commit, branch, merge"] = aula(
    40,
    "<code>projeto_final.py</code>, <code>projeto_final_v2.py</code>, <code>projeto_final_AGORA_VAI.py</code>. Todo mundo já fez isso. O Git é a máquina do tempo que guarda cada versão do seu código, com data, autor e motivo.",
    ["registrar versões com <code>add</code> e <code>commit</code>;", "trabalhar em paralelo com <code>branch</code>;", "juntar o trabalho com <code>merge</code>."],
    ["Terminal."],
    [
        chute("Você editou 3 arquivos, mas rodou <code>git add</code> só em 1 e depois <code>git commit</code>. O que entra no commit?", ["Os 3 arquivos.", "Só o arquivo adicionado.", "Nenhum."], 1,
              ["O Git só registra o que você pôs na área de preparação.", "Isso! <code>add</code> escolhe o que entra na “foto”; <code>commit</code> tira a foto.", "O arquivo adicionado entra."],
              "Dois passos de propósito: você monta o commit com cuidado antes de registrar."),
        concreto("O ponto de salvamento do jogo", "<p>Antes de enfrentar o chefão, você <b>salva o jogo</b>. Se der errado, volta ao ponto salvo. Um <b>commit</b> é um ponto de salvamento do projeto inteiro, com uma mensagem dizendo o que mudou.</p>"),
        crianca("<p><b>Branch</b> é uma realidade paralela: você testa uma ideia maluca sem estragar a história principal. Se a ideia for boa, o <b>merge</b> junta as duas histórias. Se for ruim, você apaga a realidade paralela e ninguém fica sabendo.</p>"),
        ver("o caminho de um arquivo: modificado, preparado e commitado"),
        nota("O dia a dia do Git", [
            ("<code>git init</code>", "iniciar", "Transforma a pasta num repositório."),
            ("<code>git status</code>", "situação", "Mostra o que mudou. Rode sempre que estiver em dúvida."),
            ("<code>git add arquivo</code>", "preparar", "Escolhe o que entra no próximo commit."),
            ("<code>git commit -m \"mensagem\"</code>", "registrar", "Grava a versão com uma descrição."),
            ("<code>git switch -c nome</code>", "nova branch", "Cria uma linha paralela e muda para ela."),
            ("<code>git merge nome</code>", "juntar", "Traz as mudanças da outra branch para a atual."),
        ], rot="Agora sim, os comandos"),
        passos("Uma funcionalidade nova, sem medo", [
            ("<code>git switch -c grafico</code>", "Cria uma branch só para a novidade."),
            ("Edite, depois <code>git add .</code> e <code>git commit -m \"adiciona gráfico\"</code>", "O trabalho fica registrado na branch."),
            ("<code>git switch main</code>", "Volta à linha principal, intacta."),
            ("<code>git merge grafico</code>", "Junta o gráfico à principal."),
        ], fim="Se dois commits mexerem na mesma linha, o Git pede que você escolha: é o famoso <b>conflito</b>, e ele marca o trecho no arquivo para você resolver."),
        ordem("Seu primeiro commit",
              ["git init", "git status", "git add app.py", 'git commit -m "primeira versão"', "git log --oneline"],
              corpo="<p>Ordene os comandos para criar um repositório e registrar o primeiro arquivo.</p>",
              exp="<p>Iniciar, conferir, preparar, registrar e, por fim, ver o histórico.</p>"),
        cod("Boas mensagens de commit", "Uma boa mensagem é curta e começa com um verbo. Complete a função que devolve <code>True</code> quando a mensagem tem até 60 caracteres, não termina com ponto e não é vaga (“update”, “ajustes”, “mudanças”, “fix”).",
            '''
VAGAS = {"update", "ajustes", "mudanças", "fix"}

def mensagem_boa(msg):
    return True

print(mensagem_boa("corrige cálculo da média"), mensagem_boa("ajustes"))
''',
            [("Mensagem clara passa", "assert mensagem_boa('corrige cálculo da média') is True"), ("Vaga é recusada", "assert mensagem_boa('ajustes') is False and mensagem_boa('Update') is False"),
             ("Longa demais é recusada", "assert mensagem_boa('a' * 61) is False"), ("Com ponto final é recusada", "assert mensagem_boa('adiciona gráfico.') is False")],
            '''
VAGAS = {"update", "ajustes", "mudanças", "fix"}

def mensagem_boa(msg):
    if len(msg) > 60 or msg.endswith("."):
        return False
    return msg.lower().strip() not in VAGAS

print(mensagem_boa("corrige cálculo da média"), mensagem_boa("ajustes"))
''', ["Três testes: tamanho, ponto final e se <code>msg.lower()</code> está em <code>VAGAS</code>."]),
        erros([
            ("Commits gigantes com “várias mudanças”.", "Faça commits pequenos, um assunto por vez. Fica fácil entender e desfazer."),
            ("Trabalhar sempre direto na <code>main</code>.", "Crie uma branch por tarefa; a principal fica sempre funcionando."),
            ("Commitar senhas, chaves de API e a pasta <code>.venv</code>.", "Use um <code>.gitignore</code>. Chave que vai para o histórico deve ser trocada."),
        ]),
        ponte("Git em projetos de IA",
              "<p>Experimentos de ML mudam o tempo todo: hiperparâmetros, pré-processamento, arquitetura. Uma branch por experimento e commits bem descritos deixam claro <b>qual código gerou qual resultado</b>. Para dados e pesos grandes, ferramentas como DVC e Git LFS complementam o Git (Fase 6).</p>"),
        quiz([
            ("O que <code>git add</code> faz?", ["Grava a versão no histórico.", "Escolhe o que entra no próximo commit.", "Envia para o GitHub."], 1, "É a área de preparação."),
            ("Para que serve uma branch?", ["Para apagar commits.", "Para desenvolver em paralelo sem afetar a principal.", "Para fazer backup na nuvem."], 1, "Linhas de trabalho independentes."),
            ("Qual é a melhor mensagem de commit?", ["update", "corrige divisão por zero na média", "mudei umas coisas no arquivo e agora parece que funciona."], 1, "Curta, específica e com verbo."),
        ]),
    ],
    ["<code>add</code> prepara e <code>commit</code> registra uma versão.", "Branches isolam o trabalho; <code>merge</code> junta.", "Commits pequenos com mensagens claras contam a história do projeto."],
    "GitHub: seu código na nuvem e seu portfólio.",
    livro=("PROGIT", "Capítulos 2 e 3 (Fundamentos e Ramificação)", "Quais são os três estados de um arquivo no Git?"))

AULAS["GitHub: repositórios e README"] = aula(
    30,
    "O Git guarda a história no seu computador. O GitHub põe essa história na nuvem: backup, colaboração e, de quebra, o <b>portfólio</b> que recrutadores de IA abrem antes do seu currículo.",
    ["ligar um repositório local ao GitHub;", "usar <code>push</code>, <code>pull</code> e <code>clone</code>;", "escrever um README que explica o projeto."],
    ["Git: commit, branch, merge."],
    [
        chute("Você fez 3 commits no seu computador e ainda não rodou <code>git push</code>. O que aparece no GitHub?", ["Os 3 commits.", "Nada de novo.", "Só o último commit."], 1,
              ["Commit é local. Nada vai para a nuvem sozinho.", "Isso! Commits ficam na sua máquina até o <code>push</code>.", "O <code>push</code> envia todos os commits pendentes, mas só quando você roda."],
              "<code>commit</code> salva <b>aqui</b>; <code>push</code> envia <b>para lá</b>."),
        concreto("Pasta local e pasta na nuvem", "<p>É como um documento no computador e a cópia no Drive, só que a sincronização é <b>manual</b>: <code>push</code> sobe as suas mudanças, <code>pull</code> desce as dos outros.</p>"),
        crianca("<p>O README é a <b>capa do caderno</b>: quem pega o seu projeto lê primeiro ali o que é, para que serve e como usar. Sem capa, ninguém abre.</p>"),
        nota("Local e remoto", [
            ("<code>git clone URL</code>", "clonar", "Baixa um repositório inteiro, com todo o histórico."),
            ("<code>git remote add origin URL</code>", "ligar", "Diz ao seu repositório local onde fica a cópia na nuvem."),
            ("<code>git push</code>", "empurrar", "Envia os seus commits."),
            ("<code>git pull</code>", "puxar", "Traz os commits novos da nuvem."),
            ("Pull request", "pedido de inclusão", "Proposta de mudança que alguém revisa antes de entrar na principal."),
        ], rot="Agora sim, os comandos"),
        passos("Publicando um projeto", [
            ("Crie um repositório vazio no site do GitHub.", "Sem README, para não haver conflito com o seu."),
            ("<code>git remote add origin URL</code>", "Liga o local ao remoto."),
            ("<code>git push -u origin main</code>", "Envia e memoriza o destino; depois basta <code>git push</code>."),
            ("Edite o <code>README.md</code>, faça commit e <code>push</code>.", "A página inicial do repositório mostra o README."),
        ]),
        texto("O README que funciona", "<ul><li><b>O que é</b>: uma frase.</li><li><b>Problema</b>: o que ele resolve e para quem.</li><li><b>Como rodar</b>: os comandos, na ordem.</li><li><b>Resultado</b>: uma imagem, um gráfico ou um número (acurácia, tempo).</li><li><b>O que aprendi / próximos passos</b>.</li></ul>", rot="Modelo"),
        cod("Gerador de README", "Complete a função que monta o esqueleto de um README em Markdown: título com <code>#</code>, a descrição e a seção <code>## Como rodar</code> com cada comando numa linha de lista (<code>- </code>).",
            '''
def gerar_readme(titulo, descricao, comandos):
    linhas = []
    return "\\n".join(linhas)

print(gerar_readme("Previsor de preços", "Regressão linear com scikit-learn.", ["pip install -r requirements.txt", "python treinar.py"]))
''',
            [("Começa com o título", "r = gerar_readme('T', 'D', ['a'])\nassert r.splitlines()[0] == '# T', f'primeira linha: {r.splitlines()[0]!r}'"),
             ("Tem a descrição e a seção", "r = gerar_readme('T', 'D', ['a'])\nassert 'D' in r.splitlines() and '## Como rodar' in r.splitlines()"),
             ("Lista os comandos", "r = gerar_readme('T', 'D', ['x', 'y'])\nassert '- x' in r.splitlines() and '- y' in r.splitlines()")],
            '''
def gerar_readme(titulo, descricao, comandos):
    linhas = [f"# {titulo}", "", descricao, "", "## Como rodar"]
    for c in comandos:
        linhas.append(f"- {c}")
    return "\\n".join(linhas)

print(gerar_readme("Previsor de preços", "Regressão linear com scikit-learn.", ["pip install -r requirements.txt", "python treinar.py"]))
''', ["Monte uma lista de linhas e junte com <code>\"\\n\".join</code>."]),
        erros([
            ("Repositório sem README.", "Parece abandonado. Dez linhas claras já mudam a impressão."),
            ("Subir dados enormes ou chaves de API.", "Use <code>.gitignore</code>. Repositórios públicos são varridos por robôs em busca de chaves."),
            ("<code>push</code> rejeitado.", "Alguém enviou algo antes. Rode <code>git pull</code>, resolva e envie de novo."),
        ]),
        ponte("O GitHub de quem trabalha com IA",
              "<p>Modelos, datasets e artigos vivem no GitHub e no Hugging Face (que funciona do mesmo jeito, com Git). Três projetos pequenos, com README mostrando problema, abordagem e resultado, valem mais numa seleção do que dez certificados.</p>"),
        quiz([
            ("Qual comando envia seus commits ao GitHub?", ["<code>git commit</code>", "<code>git push</code>", "<code>git pull</code>"], 1, "<code>push</code> empurra para o remoto."),
            ("O que deve estar no começo de um README?", ["A licença completa.", "O que o projeto faz, em uma frase.", "O histórico de commits."], 1, "Quem chega quer saber isso primeiro."),
            ("O que é um pull request?", ["Um pedido para baixar o repositório.", "Uma proposta de mudança para revisão.", "Um erro de sincronização."], 1, "É como o trabalho em equipe entra na principal."),
        ]),
    ],
    ["<code>push</code> envia, <code>pull</code> traz, <code>clone</code> baixa tudo.", "O README é a porta de entrada do projeto.", "Nunca suba chaves, dados grandes ou a pasta do ambiente."],
    "Consumir APIs: buscar dados de outros sistemas.",
    livro=("PROGIT", "Capítulo 6, “GitHub”", "Como o livro descreve o fluxo de um pull request?"))

AULAS["Consumir APIs com requests e JSON"] = aula(
    40,
    "Previsão do tempo, cotação do dólar, resposta do ChatGPT: nada disso está no seu computador. Você <b>pede</b> a um servidor e ele <b>responde</b> em JSON. Essa conversa é uma API, e é assim que todo aplicativo de IA fala com o modelo.",
    ["fazer uma requisição GET com <code>requests</code>;", "conferir o código de status;", "navegar pelo JSON da resposta."],
    ["Dicionários e tratamento de erros."],
    [
        chute("Uma API respondeu com o código de status <b>404</b>. O que significa?", ["Deu tudo certo.", "O endereço pedido não foi encontrado.", "O servidor está fora do ar."], 1,
              ["Sucesso é 200.", "Isso! 4xx são erros de quem pediu (endereço errado, falta de permissão).", "Servidor com problema responde 5xx."],
              "200 = ok · 4xx = erro no pedido · 5xx = erro no servidor."),
        concreto("O garçom", "<p>Você não entra na cozinha. Faz o <b>pedido</b> ao garçom (a API), que leva à cozinha (o servidor) e volta com o <b>prato</b> (a resposta). Você só precisa conhecer o cardápio: quais pedidos existem e como fazê-los.</p>"),
        crianca("<p>É como mandar uma <b>carta com uma pergunta</b> para um endereço e receber outra carta com a resposta, escrita num formato combinado. O endereço é a URL; o formato combinado é o JSON.</p>"),
        ver("como o professor confere o status e extrai um campo do JSON"),
        nota("O pedido e a resposta", [
            ("<code>requests.get(url, params={...})</code>", "pedir", "Faz o pedido. <code>params</code> vira o <code>?chave=valor</code> da URL."),
            ("<code>r.status_code</code>", "código de status", "200 é sucesso. <code>r.raise_for_status()</code> dispara erro se não for."),
            ("<code>r.json()</code>", "resposta em JSON", "Converte o texto da resposta em dicionários e listas."),
            ("<code>json.loads(texto)</code> / <code>json.dumps(obj)</code>", "ler / gerar JSON", "Do módulo <code>json</code>: texto para objeto e objeto para texto."),
            ("<code>headers={\"Authorization\": ...}</code>", "cabeçalhos", "Onde vai a chave de acesso de APIs pagas."),
        ]),
        lab("Uma requisição de verdade", '''
import requests

r = requests.get("https://api.github.com/repos/python/cpython", timeout=10)
r.raise_for_status()
dados = r.json()
print(dados["full_name"], "tem", dados["stargazers_count"], "estrelas")
''', corpo="<p>O navegador não deixa este editor acessar a internet livremente, então rode este exemplo no seu computador (depois de <code>pip install requests</code>):</p>",
            exps=["Troque <code>python/cpython</code> por outro repositório e veja as estrelas.", "Troque a URL por uma que não existe. Que erro o <code>raise_for_status()</code> dispara?"]),
        cod("Lendo a resposta de uma API de clima", "A variável <code>texto</code> é o JSON que uma API devolveu. Converta com o módulo <code>json</code> e imprima: <b>Recife: 29.5 graus, vento de 12 km/h</b>",
            '''
import json

texto = '{"cidade": "Recife", "atual": {"temp": 29.5, "vento": {"velocidade": 12, "direcao": "SE"}}}'

''',
            [("Frase correta", "assert saida.strip() == 'Recife: 29.5 graus, vento de 12 km/h', f'saiu {saida.strip()!r}'")],
            '''
import json

texto = '{"cidade": "Recife", "atual": {"temp": 29.5, "vento": {"velocidade": 12, "direcao": "SE"}}}'

d = json.loads(texto)
print(f"{d['cidade']}: {d['atual']['temp']} graus, vento de {d['atual']['vento']['velocidade']} km/h")
''', ["<code>d = json.loads(texto)</code> transforma o texto em dicionário.", "O vento está aninhado: <code>d[\"atual\"][\"vento\"][\"velocidade\"]</code>."]),
        cod("Tratando falhas", "Complete <code>resumo(resposta)</code>: recebe um dicionário com <code>status</code> e <code>corpo</code>. Se o status for 200, devolva <code>corpo[\"nome\"]</code>; se for 404, devolva <b>não encontrado</b>; para qualquer outro, devolva <b>erro 500</b> (com o número que veio).",
            '''
def resumo(resposta):
    return ""

print(resumo({"status": 200, "corpo": {"nome": "Ana"}}))
''',
            [("200 devolve o nome", "assert resumo({'status': 200, 'corpo': {'nome': 'Ana'}}) == 'Ana'"), ("404", "assert resumo({'status': 404, 'corpo': {}}) == 'não encontrado'"), ("Outros", "assert resumo({'status': 503, 'corpo': {}}) == 'erro 503'")],
            '''
def resumo(resposta):
    s = resposta["status"]
    if s == 200:
        return resposta["corpo"]["nome"]
    if s == 404:
        return "não encontrado"
    return f"erro {s}"

print(resumo({"status": 200, "corpo": {"nome": "Ana"}}))
''', ["Três caminhos: 200, 404 e o resto."], rot="Mão no código · nível 2"),
        erros([
            ("Usar <code>r.json()</code> sem conferir o status.", "Uma página de erro não é JSON. Chame <code>r.raise_for_status()</code> antes."),
            ("Escrever a chave da API no código.", "Guarde em variável de ambiente (<code>os.environ</code>) e nunca commite."),
            ("Esquecer o <code>timeout</code>.", "Sem ele, o programa pode ficar esperando para sempre."),
        ]),
        ponte("Falar com um LLM é isto",
              "<p>Chamar um modelo de linguagem é um <b>POST</b> com JSON: você envia as mensagens e recebe um JSON com o texto gerado e a contagem de tokens. As bibliotecas oficiais só embrulham este pedido. Na Fase 5 você fará exatamente isso.</p>"),
        quiz([
            ("O que <code>r.json()</code> devolve?", ["O texto cru da resposta.", "Dicionários e listas do Python.", "O código de status."], 1, "O JSON já convertido."),
            ("Um código 500 indica:", ["Sucesso.", "Erro no servidor.", "Endereço inexistente."], 1, "5xx é problema do lado de lá."),
            ("Onde guardar a chave de uma API?", ["No código, em uma variável.", "Em variável de ambiente, fora do Git.", "No README."], 1, "Chaves nunca vão para o repositório."),
        ]),
    ],
    ["Uma API recebe um pedido (URL + parâmetros) e responde, em geral, com JSON.", "Confira o status antes de usar a resposta.", "JSON vira dicionários e listas aninhados."],
    "PEP 8: código que outras pessoas conseguem ler.",
    livro=("ATBS:12", "Capítulo 12, “Web Scraping”, seção sobre o módulo requests", "Como o livro verifica se um download deu certo?"))

AULAS["Estilo de código PEP 8"] = aula(
    25,
    "Código é lido muito mais vezes do que é escrito, inclusive por você daqui a três meses. A PEP 8 é o acordo de estilo da comunidade Python: nada de regras para computador, só gentileza com quem lê.",
    ["aplicar as convenções de nomes;", "organizar espaços, linhas e imports;", "usar um formatador automático."],
    ["Funções e classes."],
    [
        chute("Qual destes nomes segue a PEP 8 para uma <b>função</b>?", ["<code>CalcularMedia</code>", "<code>calcular_media</code>", "<code>calcularMedia</code>"], 1,
              ["Inicial maiúscula em cada palavra é para <b>classes</b>.", "Isso! Funções e variáveis usam minúsculas com sublinhado (<i>snake_case</i>).", "Esse é o estilo do JavaScript e do Java (<i>camelCase</i>)."],
              "Só de olhar o nome você sabe o que é: <code>snake_case</code> função, <code>PascalCase</code> classe, <code>MAIUSCULAS</code> constante."),
        concreto("Regras de trânsito", "<p>Dirigir do lado direito não é “melhor”: é <b>combinado</b>. Como todos seguem, ninguém bate. Estilo de código é igual: quando todos escrevem parecido, qualquer pessoa lê qualquer projeto.</p>"),
        nota("As convenções que mais importam", [
            ("<code>total_vendas</code>", "variáveis e funções", "<i>snake_case</i>: minúsculas e sublinhado."),
            ("<code>ClienteVip</code>", "classes", "<i>PascalCase</i>: inicial maiúscula em cada palavra."),
            ("<code>TAXA_MAXIMA</code>", "constantes", "Tudo maiúsculo."),
            ("4 espaços", "recuo", "Nunca tabulação misturada com espaço."),
            ("<code>x = a + b</code>", "espaços", "Um espaço em volta de operadores e depois de vírgulas; nenhum colado em parênteses."),
            ("Linhas de até ~88 caracteres", "comprimento", "A PEP 8 diz 79; formatadores modernos usam 88."),
        ], rot="Agora sim, as regras"),
        passos("Arrumando um trecho", [
            ("<code>def Soma(a,b):return a+b</code>", "Nome com maiúscula, sem espaços e tudo numa linha."),
            ("Nome: <code>def soma(a, b):</code>", "Função em minúsculas; espaço depois da vírgula."),
            ("Corpo na linha de baixo, recuado: <code>return a + b</code>", "Uma instrução por linha, espaços em volta do <code>+</code>."),
        ], fim="Na prática, ninguém faz isso à mão: <code>ruff format</code> ou <code>black</code> formatam o arquivo inteiro em um segundo."),
        cod("Conserte o estilo", "O código funciona, mas está fora da PEP 8. Reescreva com bons nomes e espaçamento. Os testes conferem o comportamento e os nomes: a função deve se chamar <code>calcular_media</code> e a constante, <code>NOTA_MINIMA</code>.",
            '''
notaMinima=6
def CalcMed(L):return sum(L)/len(L)
print(CalcMed([7,8,9])>=notaMinima)
''',
            [("Função calcular_media existe e funciona", "assert calcular_media([7, 8, 9]) == 8"), ("Constante NOTA_MINIMA vale 6", "assert NOTA_MINIMA == 6"), ("Imprime True", "assert saida.strip() == 'True'")],
            '''
NOTA_MINIMA = 6


def calcular_media(notas):
    return sum(notas) / len(notas)


print(calcular_media([7, 8, 9]) >= NOTA_MINIMA)
''', ["Constante em maiúsculas, função em <i>snake_case</i>, parâmetro com nome que explica (<code>notas</code>)."]),
        erros([
            ("Nomes de uma letra: <code>l</code>, <code>O</code>, <code>I</code>.", "Confundem com 1 e 0. Use nomes descritivos."),
            ("Vários imports na mesma linha.", "Um por linha; primeiro a biblioteca padrão, depois terceiros, depois os seus."),
            ("Brigar por estilo em revisões de código.", "Deixe o formatador decidir e discuta o que importa: a lógica."),
        ]),
        ponte("Estilo em projetos de IA",
              "<p>Notebooks viram bagunça depressa. Nomes claros (<code>X_treino</code>, <code>taxa_aprendizado</code>) e funções pequenas fazem a diferença entre um experimento reproduzível e um “não sei mais o que essa célula faz”. Os repositórios de IA mais usados rodam formatador e linter a cada commit.</p>"),
        quiz([
            ("Como nomear uma classe?", ["<code>modelo_linear</code>", "<code>ModeloLinear</code>", "<code>MODELO_LINEAR</code>"], 1, "<i>PascalCase</i>."),
            ("Quantos espaços de recuo a PEP 8 recomenda?", ["2", "4", "8"], 1, "Quatro espaços."),
            ("Qual ferramenta formata o código automaticamente?", ["<code>pip</code>", "<code>black</code> ou <code>ruff format</code>", "<code>venv</code>"], 1, "Formatadores aplicam o estilo sozinhos."),
        ]),
    ],
    ["<i>snake_case</i> para funções e variáveis, <i>PascalCase</i> para classes, MAIÚSCULAS para constantes.", "Quatro espaços de recuo e espaços em volta de operadores.", "Use um formatador automático."],
    "Docstrings e comentários: explicar o porquê.",
    livro=("PYDOC:controlflow", "Seção 4.9.9, “Intermezzo: estilo de codificação”", "Quais pontos da PEP 8 o tutorial destaca?"))

AULAS["Docstrings e comentários"] = aula(
    25,
    "O código diz <b>como</b>. Só você pode dizer <b>por quê</b>. Um bom comentário economiza uma hora de quem lê; um comentário ruim é ruído que ainda por cima envelhece.",
    ["escrever docstrings em funções;", "comentar o porquê, não o óbvio;", "usar <code>help()</code> e dicas de tipo."],
    ["Funções e PEP 8."],
    [
        chute("Qual comentário é mais útil?", ["<code>x = x + 1  # soma 1 a x</code>", "<code>x = x + 1  # compensa o índice que começa em 0</code>", "<code># código abaixo</code>"], 1,
              ["Só repete o que o código já diz.", "Isso! Explica a <b>razão</b>, que não está escrita em lugar nenhum.", "Não informa nada."],
              "Comente o <b>porquê</b>. O <b>o quê</b> o próprio código mostra."),
        concreto("O manual e o post-it", "<p>A <b>docstring</b> é o manual da função: o que faz, o que recebe, o que devolve. O <b>comentário</b> é um post-it colado numa linha estranha: “não mexa, isso evita divisão por zero”.</p>"),
        nota("As ferramentas", [
            ("<code>\"\"\"Texto.\"\"\"</code>", "docstring", "Primeira coisa dentro da função, entre três aspas. Uma linha de resumo e, se preciso, detalhes."),
            ("<code># texto</code>", "comentário", "Explica uma decisão. Vai na linha de cima do trecho."),
            ("<code>help(funcao)</code>", "ajuda", "Mostra a docstring. É o que o editor exibe ao passar o mouse."),
            ("<code>def f(x: float) -&gt; float:</code>", "dicas de tipo", "Documentam os tipos esperados. O Python não obriga, mas o editor avisa."),
        ]),
        passos("Documentando uma função", [
            ("Linha de resumo: “Normaliza os valores para o intervalo 0 a 1.”", "No imperativo, terminando em ponto."),
            ("Args: o que cada parâmetro significa.", "Inclusive unidades e limites."),
            ("Returns: o que volta.", "Tipo e significado."),
            ("Comentário só onde há uma decisão não óbvia.", "Ex.: por que somar um valor mínimo ao divisor."),
        ], corpo=py('def normalizar(valores: list[float]) -> list[float]:\n    """Normaliza os valores para o intervalo 0 a 1.\n\n    Args:\n        valores: lista de números (pelo menos dois diferentes).\n    Returns:\n        Lista do mesmo tamanho, com mínimo 0 e máximo 1.\n    """\n    menor, maior = min(valores), max(valores)\n    return [(v - menor) / (maior - menor) for v in valores]')),
        cod("Documente a função", "Acrescente uma docstring a <code>erro_medio</code> (com pelo menos 20 caracteres, explicando o que ela faz) e dicas de tipo no retorno. O comportamento não pode mudar.",
            '''
def erro_medio(previstos, reais):
    return sum(abs(p - r) for p, r in zip(previstos, reais)) / len(reais)

print(erro_medio([2, 4], [3, 2]))
''',
            [("Tem docstring", "assert erro_medio.__doc__ and len(erro_medio.__doc__.strip()) >= 20, 'acrescente uma docstring explicando a função'"),
             ("Tem dica de tipo no retorno", "assert 'return' in erro_medio.__annotations__, 'use -> float'"), ("Continua funcionando", "assert erro_medio([2, 4], [3, 2]) == 1.5")],
            '''
def erro_medio(previstos, reais) -> float:
    """Devolve o erro absoluto médio entre os valores previstos e os reais."""
    return sum(abs(p - r) for p, r in zip(previstos, reais)) / len(reais)

print(erro_medio([2, 4], [3, 2]))
''', ["A docstring é a primeira linha dentro da função, entre três aspas.", "<code>def erro_medio(previstos, reais) -&gt; float:</code>"]),
        erros([
            ("Comentário que repete o código.", "Apague. Ele só dobra o trabalho de manutenção."),
            ("Comentário desatualizado.", "É pior que nenhum: mente para quem lê. Mudou o código, mude o comentário."),
            ("Código comentado “para o caso de precisar”.", "O Git guarda o histórico. Apague sem dó."),
        ]),
        ponte("Docstrings e LLMs",
              "<p>Quando você dá <b>ferramentas</b> a um agente de IA, a descrição da função é o que o modelo lê para decidir se e como usá-la. Uma docstring clara vira, literalmente, parte do prompt. Escrever boas descrições é uma habilidade de engenharia de IA.</p>"),
        quiz([
            ("Onde fica a docstring?", ["Antes do <code>def</code>.", "Na primeira linha dentro da função.", "No fim do arquivo."], 1, "Logo depois da linha do <code>def</code>."),
            ("O que um bom comentário explica?", ["O que cada símbolo faz.", "O motivo de uma decisão.", "O nome do autor."], 1, "O porquê."),
            ("O que <code>help(f)</code> mostra?", ["O código-fonte.", "A docstring de <code>f</code>.", "Os testes de <code>f</code>."], 1, "É a documentação embutida."),
        ]),
    ],
    ["Docstring: o que a função faz, recebe e devolve.", "Comentário: o porquê de uma decisão.", "Dicas de tipo documentam e ajudam o editor."],
    "Depuração: encontrar o erro com método.",
    livro=("PYDOC:controlflow", "Seções 4.9.7 e 4.9.8 (strings de documentação e anotações)", "Que convenções de docstring o tutorial recomenda?"))

AULAS["Depuração (debug) e leitura de erros"] = aula(
    35,
    "Programar é 20% escrever e 80% descobrir por que não funciona. Quem depura com método resolve em minutos o que os outros resolvem em horas de tentativa e erro.",
    ["ler um traceback de baixo para cima;", "isolar o problema com <code>print</code> e com o depurador;", "reconhecer os erros mais comuns."],
    ["Funções e tratamento de erros."],
    [
        chute("Num traceback do Python, onde está a informação mais importante?", ["Na primeira linha.", "Na última linha.", "No meio."], 1,
              ["A primeira linha só avisa que há um traceback.", "Isso! A última linha traz o <b>tipo do erro</b> e a <b>mensagem</b>. Logo acima, o arquivo e a linha.", "O meio mostra o caminho das chamadas, útil depois."],
              "Leia <b>de baixo para cima</b>: primeiro o quê, depois onde."),
        concreto("O detetive", "<p>Um detetive não prende o primeiro suspeito. Ele <b>observa</b> a cena (a mensagem de erro), <b>formula uma hipótese</b>, <b>testa</b> e, se errar, descarta e testa outra. Depurar é isso, e não “mudar coisas até funcionar”.</p>"),
        crianca("<p>Quando a luz não acende, você não troca a casa inteira: testa a lâmpada, depois o interruptor, depois o disjuntor. <b>Um passo de cada vez</b>, até achar onde o caminho quebra.</p>"),
        nota("Erros que você vai ver toda semana", [
            ("<code>SyntaxError</code>", "erro de sintaxe", "Faltou dois-pontos, parêntese ou aspas. O Python nem começa a rodar."),
            ("<code>NameError</code>", "nome não existe", "Variável não criada ou digitada errado."),
            ("<code>TypeError</code>", "tipo errado", "Somar texto com número; chamar algo que não é função."),
            ("<code>IndexError</code> / <code>KeyError</code>", "posição / chave inexistente", "Índice além do tamanho da lista; chave que não está no dicionário."),
            ("<code>AttributeError</code>", "atributo inexistente", "Muitas vezes o objeto é <code>None</code>: uma função não devolveu nada."),
        ], rot="O dicionário de erros"),
        passos("O método", [
            ("Leia a última linha do erro.", "Tipo e mensagem dizem <b>o que</b> aconteceu."),
            ("Vá à linha indicada.", "<b>Onde</b> aconteceu (nem sempre é onde está o bug)."),
            ("Imprima as variáveis logo antes: <code>print(f\"{x=}\")</code>.", "Compare o que você <b>acha</b> que elas valem com o que valem de fato."),
            ("Reduza: reproduza o erro com o menor exemplo possível.", "Metade dos bugs se revela neste passo."),
            ("Corrija uma coisa e rode de novo.", "Mudar três coisas de uma vez esconde qual resolveu."),
        ], fim="No VS Code, um clique à esquerda da linha cria um <b>breakpoint</b>: o programa para ali e você inspeciona tudo, passo a passo."),
        cod("Caça ao bug 1", "A função deveria devolver a média, mas dá erro com a lista do exemplo. Rode, leia a última linha da mensagem e conserte (lista vazia deve devolver 0).",
            '''
def media(valores):
    return sum(valores) / len(valores)

print(media([8, 6]), media([]))
''',
            [("Média normal", "assert media([8, 6]) == 7"), ("Lista vazia devolve 0", "assert media([]) == 0")],
            '''
def media(valores):
    if not valores:
        return 0
    return sum(valores) / len(valores)

print(media([8, 6]), media([]))
''', ["O erro é <code>ZeroDivisionError</code>: qual lista tem tamanho 0?"]),
        cod("Caça ao bug 2", "O código roda sem erro, mas o resultado está errado: deveria contar quantas notas são <b>maiores ou iguais</b> a 7. Ache o bug de lógica.",
            '''
def aprovados(notas):
    total = 0
    for n in notas:
        if n > 7:
            total = 1
    return total

print(aprovados([7, 9, 5, 8]))
''',
            [("Conta 3 aprovados", "assert aprovados([7, 9, 5, 8]) == 3, f'deu {aprovados([7, 9, 5, 8])}'"), ("Nenhum aprovado", "assert aprovados([1, 2]) == 0")],
            '''
def aprovados(notas):
    total = 0
    for n in notas:
        if n >= 7:
            total += 1
    return total

print(aprovados([7, 9, 5, 8]))
''', ["São <b>dois</b> bugs: a comparação e a forma de somar.", "Ponha um <code>print(n, total)</code> dentro do laço e acompanhe."], rot="Mão no código · nível 2"),
        erros([
            ("Mudar coisas ao acaso até funcionar.", "Você não aprende a causa e o bug volta. Formule uma hipótese e teste."),
            ("Ignorar a mensagem de erro.", "Ela quase sempre diz exatamente o problema. Leia inteira."),
            ("Achar que o bug está onde o erro apareceu.", "O erro surge onde o valor ruim foi <b>usado</b>; a causa pode estar linhas antes, onde ele foi <b>criado</b>."),
        ]),
        ponte("Depurar com (e sem) IA",
              "<p>Colar o traceback num assistente de IA resolve muita coisa, mas só se você souber <b>avaliar a resposta</b>. Em deep learning, os piores bugs não dão erro: a rede “treina” e não aprende. Aí vale o método do detetive: conferir formatos, valores e perdas, uma etapa por vez (Fase 4).</p>"),
        quiz([
            ("<code>NameError: name 'totl' is not defined</code> indica:", ["Divisão por zero.", "Nome digitado errado ou variável não criada.", "Lista vazia."], 1, "O Python não conhece esse nome."),
            ("Qual é o primeiro passo ao ver um erro?", ["Reescrever a função.", "Ler a última linha do traceback.", "Reiniciar o computador."], 1, "Tipo e mensagem primeiro."),
            ("Por que reduzir o problema a um exemplo mínimo?", ["Para o código ficar bonito.", "Para isolar a causa.", "Para rodar mais rápido."], 1, "Menos partes, menos suspeitos."),
        ]),
    ],
    ["Leia o traceback de baixo para cima: tipo, mensagem, linha.", "Depure com hipótese e teste, uma mudança por vez.", "Erros de lógica não dão mensagem: inspecione os valores."],
    "Testes com pytest: provar que funciona.",
    livro=("ATBS:11", "Capítulo 11, “Debugging”", "Para que o livro recomenda usar assert e logging?"))

AULAS["Testes simples com pytest"] = aula(
    35,
    "“Funcionou quando testei na mão” vale até a próxima mudança. Um teste automatizado é um robô que confere seu código em um segundo, toda vez, para sempre. Os exercícios deste site, aliás, são corrigidos assim.",
    ["escrever testes com <code>assert</code>;", "organizar testes para o <code>pytest</code>;", "pensar em casos normais, de borda e de erro."],
    ["Funções e tratamento de erros."],
    [
        chute("O que acontece quando o Python executa <code>assert 2 + 2 == 5</code>?", ["Nada.", "Dispara <code>AssertionError</code>.", "Imprime False."], 1,
              ["Nada acontece só quando a condição é verdadeira.", "Isso! <code>assert</code> exige que a condição seja verdadeira; se não for, dispara um erro.", "Ele não imprime: interrompe com erro."],
              "<code>assert</code> = “garanto que isto é verdade; se não for, pare tudo”."),
        concreto("A lista de conferência do piloto", "<p>Antes de cada voo, o piloto percorre a mesma lista: combustível, flaps, instrumentos. Não é desconfiança, é método. Testes são a lista de conferência do seu código, rodada a cada mudança.</p>"),
        crianca("<p>Você fez uma máquina de somar. Em vez de confiar, você pergunta: “2 + 2?” e confere se ela diz 4. “0 + 0?” “Um número negativo?” Cada pergunta com resposta conhecida é um <b>teste</b>.</p>"),
        ver("como o professor escreve e roda um teste simples"),
        nota("Como o pytest funciona", [
            ("<code>assert f(2) == 4</code>", "afirmação", "O coração do teste: compara o resultado com o esperado."),
            ("<code>def test_nome():</code>", "função de teste", "O pytest roda toda função que começa com <code>test_</code>."),
            ("<code>test_algo.py</code>", "arquivo de teste", "Arquivos que começam com <code>test_</code> são encontrados sozinhos."),
            ("<code>pytest</code>", "rodar", "No terminal, roda todos os testes e mostra o que passou e o que falhou."),
            ("<code>with pytest.raises(ValueError):</code>", "esperar um erro", "Testa que o código <b>recusa</b> entradas inválidas."),
        ]),
        passos("Três tipos de caso", [
            ("Caso normal: <code>assert media([6, 8]) == 7</code>", "O uso do dia a dia."),
            ("Caso de borda: <code>assert media([5]) == 5</code> e <code>media([])</code>", "Um item, lista vazia, zero, negativos: onde os bugs moram."),
            ("Caso de erro: entrada inválida deve falhar do jeito combinado.", "Falhar bem também é comportamento."),
        ], fim="Um teste que falha <b>antes</b> da correção e passa <b>depois</b> prova que você consertou o bug certo."),
        cod("Escreva os testes", "A função <code>e_par</code> está pronta. Escreva <b>3 testes</b> com <code>assert</code> dentro de <code>test_e_par</code>: um número par, um ímpar e o zero.",
            '''
def e_par(n):
    return n % 2 == 0

def test_e_par():
    pass  # troque por 3 asserts

test_e_par()
print("testes ok")
''',
            [("Os testes pegam o erro oposto", "certa = e_par\ne_par = lambda n: False\ntry:\n    test_e_par()\n    pegou = False\nexcept AssertionError:\n    pegou = True\ne_par = certa\nassert pegou, 'seus testes deveriam falhar se e_par sempre devolvesse False (teste um par)'"),
             ("Os testes passam com a função certa", "test_e_par()"),
             ("Os testes pegam uma função errada", "certa = e_par\ne_par = lambda n: True\ntry:\n    test_e_par()\n    pegou = False\nexcept AssertionError:\n    pegou = True\ne_par = certa\nassert pegou, 'seus testes deveriam falhar se e_par sempre devolvesse True (teste um ímpar)'")],
            '''
def e_par(n):
    return n % 2 == 0

def test_e_par():
    assert e_par(4) is True
    assert e_par(7) is False
    assert e_par(0) is True

test_e_par()
print("testes ok")
''', ["<code>assert e_par(4) is True</code>", "Teste um ímpar: <code>assert e_par(7) is False</code>."]),
        cod("Faça os testes passarem", "Os testes já estão escritos. Implemente <code>recortar</code>: limita o valor ao intervalo [minimo, maximo].",
            '''
def recortar(valor, minimo, maximo):
    return valor

def test_recortar():
    assert recortar(5, 0, 10) == 5
    assert recortar(-3, 0, 10) == 0
    assert recortar(42, 0, 10) == 10

test_recortar()
print("testes ok")
''',
            [("Dentro do intervalo", "assert recortar(5, 0, 10) == 5"), ("Abaixo do mínimo", "assert recortar(-3, 0, 10) == 0"), ("Acima do máximo", "assert recortar(42, 0, 10) == 10")],
            '''
def recortar(valor, minimo, maximo):
    return max(minimo, min(valor, maximo))

def test_recortar():
    assert recortar(5, 0, 10) == 5
    assert recortar(-3, 0, 10) == 0
    assert recortar(42, 0, 10) == 10

test_recortar()
print("testes ok")
''', ["Com <code>if</code>: se for menor que o mínimo, devolva o mínimo; se maior que o máximo, o máximo."], rot="Mão no código · nível 2"),
        erros([
            ("Testar só o caso feliz.", "Bugs moram nas bordas: vazio, zero, negativo, repetido."),
            ("Um teste gigante que confere dez coisas.", "Quando falha, você não sabe o quê. Testes pequenos e com nome claro."),
            ("Comparar <code>float</code> com <code>==</code>.", "<code>0.1 + 0.2 == 0.3</code> é <code>False</code>. Use <code>pytest.approx</code> ou uma tolerância."),
        ]),
        ponte("Testes em IA: os evals",
              "<p>Código de dados merece testes como qualquer outro: o pré-processamento mantém o número de linhas? A coluna não tem valores nulos? Para modelos de linguagem, a ideia vira <b>evals</b>: uma bateria de perguntas com respostas esperadas, rodada a cada mudança de prompt ou de modelo.</p>"),
        quiz([
            ("Como o pytest reconhece um teste?", ["Pelo comentário <code># teste</code>.", "Pelo nome começando com <code>test_</code>.", "Pela extensão <code>.test</code>."], 1, "Arquivos e funções <code>test_*</code>."),
            ("O que é um caso de borda?", ["O caso mais comum.", "Uma entrada no limite: vazia, zero, extrema.", "Um teste que sempre passa."], 1, "Onde o código costuma quebrar."),
            ("Por que <code>assert 0.1 + 0.2 == 0.3</code> falha?", ["Bug do Python.", "Números decimais têm erro de arredondamento.", "Falta um import."], 1, "Compare com tolerância."),
        ]),
    ],
    ["<code>assert</code> confere uma expectativa; o pytest roda todas as funções <code>test_*</code>.", "Teste casos normais, de borda e de erro.", "Testes dão segurança para mudar o código."],
    "Lambda, map e filter: funções como valores.",
    livro=("MISSING:debugging-profiling", "Aula “Debugging and Profiling”, primeira parte", "Que técnicas de depuração a aula lista antes do depurador?"))

AULAS["Lambda, map e filter"] = aula(
    30,
    "Em Python, uma função é um valor como outro qualquer: dá para guardar numa variável e <b>passar para outra função</b>. É assim que você diz ao <code>sorted</code> como ordenar e ao Pandas o que fazer com cada linha.",
    ["escrever funções anônimas com <code>lambda</code>;", "usar <code>map</code>, <code>filter</code> e <code>sorted(key=...)</code>;", "saber quando uma comprehension é mais clara."],
    ["Funções e list comprehension."],
    [
        chute("O que esse código imprime?", ["['ana', 'bia', 'caio']", "['bia', 'ana', 'caio']", "['caio', 'bia', 'ana']"], 0,
              ["Isso! A <code>key</code> manda ordenar pelo <b>tamanho</b>. “ana” e “bia” têm 3 letras e mantêm a ordem original; “caio” tem 4.", "Empates mantêm a ordem em que estavam: “ana” vem antes de “bia”.", "Isso seria ordem decrescente de tamanho."],
              "<code>key</code> recebe uma função que diz <b>o que comparar</b> em cada item.",
              cod='nomes = ["caio", "ana", "bia"]\nprint(sorted(nomes, key=lambda n: len(n)))'),
        concreto("O bilhete com a instrução", "<p>Você entrega uma pilha de provas ao assistente com um bilhete: “ordene <b>pela nota</b>”. A pilha são os dados; o bilhete é uma função pequena que diz o critério. <code>lambda</code> é esse bilhete.</p>"),
        crianca("<p><code>map</code> é “faça <b>isto</b> com <b>cada um</b>”. <code>filter</code> é “fique só com <b>os que passam</b> neste teste”. E a <code>lambda</code> é a regrinha curta que você escreve na hora, sem dar nome.</p>"),
        nota("Funções que recebem funções", [
            ("<code>lambda x: x * 2</code>", "função anônima", "Recebe <code>x</code>, devolve <code>x * 2</code>. Uma expressão só, sem <code>return</code>."),
            ("<code>map(f, lista)</code>", "aplicar em todos", "Aplica <code>f</code> a cada item. Envolva em <code>list(...)</code> para ver o resultado."),
            ("<code>filter(f, lista)</code>", "filtrar", "Mantém os itens em que <code>f</code> devolve <code>True</code>."),
            ("<code>sorted(lista, key=f)</code>", "ordenar por critério", "Ordena pelo valor que <code>f</code> calcula. <code>reverse=True</code> inverte."),
        ]),
        passos("Ordenando modelos pela acurácia", [
            ("<code>modelos = [(\"A\", 0.81), (\"B\", 0.93), (\"C\", 0.77)]</code>", "Lista de tuplas: nome e acurácia."),
            ("<code>key=lambda m: m[1]</code>", "O critério é o segundo item de cada tupla."),
            ("<code>sorted(modelos, key=lambda m: m[1], reverse=True)</code>", "Do melhor para o pior: B, A, C."),
        ], fim="Para transformações e filtros simples, a comprehension costuma ser mais legível que <code>map</code> e <code>filter</code>."),
        cod("O melhor experimento", "Cada experimento é um dicionário. Devolva o <b>nome</b> do experimento com a menor perda, usando <code>min</code> ou <code>sorted</code> com <code>key</code>.",
            '''
def melhor(experimentos):
    return ""

exps = [{"nome": "lr-0.1", "perda": 0.42}, {"nome": "lr-0.01", "perda": 0.18}, {"nome": "lr-0.001", "perda": 0.31}]
print(melhor(exps))
''',
            [("Escolhe a menor perda", "assert melhor([{'nome': 'a', 'perda': 0.4}, {'nome': 'b', 'perda': 0.1}, {'nome': 'c', 'perda': 0.3}]) == 'b'"), ("Funciona com um só", "assert melhor([{'nome': 'x', 'perda': 9}]) == 'x'")],
            '''
def melhor(experimentos):
    return min(experimentos, key=lambda e: e["perda"])["nome"]

exps = [{"nome": "lr-0.1", "perda": 0.42}, {"nome": "lr-0.01", "perda": 0.18}, {"nome": "lr-0.001", "perda": 0.31}]
print(melhor(exps))
''', ["<code>min(lista, key=lambda e: e[\"perda\"])</code> devolve o dicionário inteiro; pegue o <code>[\"nome\"]</code>."]),
        cod("map e filter", "Usando <code>filter</code> e <code>map</code> (com <code>lambda</code>), crie <code>resultado</code>: os preços acima de 50, com 10% de desconto.",
            '''
precos = [30, 80, 120, 45, 60]

resultado = []

print(resultado)
''',
            [("Valores corretos", "assert [round(x, 2) for x in resultado] == [72.0, 108.0, 54.0], f'deu {list(resultado)}'"), ("É uma lista", "assert isinstance(resultado, list), 'envolva em list(...)'")],
            '''
precos = [30, 80, 120, 45, 60]

caros = filter(lambda p: p > 50, precos)
resultado = list(map(lambda p: p * 0.9, caros))

print(resultado)
''', ["Primeiro <code>filter(lambda p: p &gt; 50, precos)</code>, depois <code>map(lambda p: p * 0.9, ...)</code>.", "Envolva tudo em <code>list(...)</code>."], rot="Mão no código · nível 2"),
        erros([
            ("Imprimir um <code>map</code> e ver <code>&lt;map object&gt;</code>.", "<code>map</code> e <code>filter</code> são preguiçosos. Use <code>list(...)</code> para materializar."),
            ("Lambdas longas, com lógica complicada.", "Se não cabe em uma linha clara, use <code>def</code> e dê um nome."),
            ("<code>f = lambda x: ...</code> para depois reutilizar.", "Se vai dar nome, use <code>def</code>: fica com docstring e aparece melhor nos erros."),
        ]),
        ponte("Lambda em dados e IA",
              "<p><code>df[\"preco\"].apply(lambda p: p * 1.1)</code> no Pandas, <code>dataset.map(lambda ex: tokenizar(ex))</code> no Hugging Face, <code>sorted(resultados, key=lambda r: r.score)</code> para ranquear documentos num RAG. A ideia de “passar uma regrinha” está em toda a pilha de dados.</p>"),
        quiz([
            ("<code>list(map(lambda x: x + 1, [1, 2]))</code> resulta em:", ["[1, 2]", "[2, 3]", "[3]"], 1, "Soma 1 a cada item."),
            ("Para que serve o parâmetro <code>key</code> do <code>sorted</code>?", ["Define o critério de ordenação.", "Define a senha da lista.", "Remove duplicados."], 0, "Uma função que calcula o valor comparado."),
            ("Quando trocar a <code>lambda</code> por <code>def</code>?", ["Nunca.", "Quando a lógica é longa ou será reutilizada.", "Sempre que houver números."], 1, "Nome e clareza valem mais."),
        ]),
    ],
    ["<code>lambda</code> cria uma função curta e sem nome.", "<code>map</code> transforma, <code>filter</code> seleciona, <code>sorted(key=...)</code> ordena por critério.", "Funções podem ser passadas como argumentos."],
    "Geradores e iteradores: produzir valores sob demanda.",
    livro=("PYDOC:controlflow", "Seção 4.9.6, “Expressões lambda”", "Que exemplo o tutorial dá de lambda devolvida por uma função?"))
