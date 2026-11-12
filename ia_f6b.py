# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 6 (parte B): infraestrutura e produto para aplicações de IA."""
from lesson_factory import *

AULAS = {}

AULAS["Kubernetes (noção)"] = aula(
    20,
    "Quando você tem dezenas de contêineres que precisam ficar sempre no ar, escalar com o tráfego e se recuperar sozinhos de falhas, entra o Kubernetes. Você não precisa dominá-lo no começo da carreira, mas precisa entender o vocabulário e saber quando ele vale a pena.",
    ["entender o que o Kubernetes resolve;", "conhecer pod, deployment, service e réplicas;", "pensar no modelo declarativo: estado desejado versus estado atual."],
    ["Docker e deploy em nuvem."],
    [
        chute("Você declarou 3 réplicas da API e um servidor caiu, levando uma delas. O que o Kubernetes faz?", ["Nada, espera alguém ver.", "Percebe que há 2 em vez de 3 e cria outra em um servidor saudável.", "Desliga as outras duas."], 1,
              ["Isso seria sem orquestração.", "Isso! Ele compara o estado atual com o desejado e corrige a diferença, o tempo todo.", "Pelo contrário."],
              "Você declara o que quer; ele mantém."),
        concreto("O termostato", "<p>Você não liga e desliga o ar-condicionado a cada minuto: define 23 graus e o termostato faz o resto. No Kubernetes você define “quero 3 cópias da API” e ele liga, desliga e move contêineres para manter isso.</p>"),
        nota("O vocabulário", [
            ("Cluster / nó", "o conjunto de máquinas", "Cada nó é um servidor."),
            ("Pod", "a menor unidade", "Um ou mais contêineres que rodam juntos."),
            ("Deployment", "estado desejado", "Qual imagem, quantas réplicas, como atualizar."),
            ("Service", "endereço estável", "Distribui tráfego entre os pods."),
            ("HPA", "escala automática", "Mais réplicas quando a CPU sobe."),
        ]),
        texto("Um deployment em YAML", sh('''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: minha-api
spec:
  replicas: 3
  selector:
    matchLabels: {app: minha-api}
  template:
    metadata:
      labels: {app: minha-api}
    spec:
      containers:
        - name: api
          image: registro/minha-api:1.4.0
          ports: [{containerPort: 8000}]
'''), rot="Como é na prática"),
        cod("O laço de reconciliação", "O coração do Kubernetes é um laço que compara o desejado com o atual. Escreva <code>reconciliar(desejado, atual)</code> que devolve as ações para cada aplicação: <code>(\"criar\", app, n)</code> ou <code>(\"remover\", app, n)</code>, e remove aplicações que não estão mais no desejado.",
            '''
def reconciliar(desejado, atual):
    return []

print(reconciliar({"api": 3, "worker": 2}, {"api": 2, "worker": 4, "antigo": 1}))
''',
            [("Ações corretas", "assert sorted(reconciliar({'api': 3, 'worker': 2}, {'api': 2, 'worker': 4, 'antigo': 1})) == [('criar', 'api', 1), ('remover', 'antigo', 1), ('remover', 'worker', 2)]"),
             ("Nada a fazer", "assert reconciliar({'api': 2}, {'api': 2}) == []"),
             ("App nova", "assert reconciliar({'api': 2}, {}) == [('criar', 'api', 2)]")],
            '''
def reconciliar(desejado, atual):
    acoes = []
    for app in sorted(set(desejado) | set(atual)):
        d, a = desejado.get(app, 0), atual.get(app, 0)
        if d > a:
            acoes.append(("criar", app, d - a))
        elif a > d:
            acoes.append(("remover", app, a - d))
    return acoes

print(reconciliar({"api": 3, "worker": 2}, {"api": 2, "worker": 4, "antigo": 1}))
''', ["Percorra a união das chaves dos dois dicionários.", "Use <code>.get(app, 0)</code> para quem falta em um dos lados."]),
        erros([("Usar Kubernetes num projeto pequeno.", "Para poucos serviços, contêiner gerenciado (Cloud Run etc.) é mais simples e barato."), ("Sem limites de CPU e memória nos pods.", "Um pod descontrolado derruba os vizinhos."), ("Configurar tudo à mão no cluster.", "Guarde os YAMLs no Git (GitOps).")]),
        ponte("Onde aparece em IA", "<p>Equipes de plataforma usam Kubernetes para servir modelos com GPUs, rodar treinos distribuídos e escalar APIs de inferência (KServe, Ray). Saber o vocabulário ajuda nas entrevistas de MLOps.</p>"),
        quiz([
            ("O que é um pod?", ["A menor unidade, com um ou mais contêineres.", "Um servidor físico.", "Um banco de dados."], 0, "Unidade básica."),
            ("O modelo do Kubernetes é:", ["Declarativo: você descreve o estado desejado.", "Manual: você liga cada contêiner.", "Aleatório."], 0, "Reconciliação."),
            ("Quando NÃO vale a pena usar Kubernetes?", ["Em projetos pequenos com poucos serviços.", "Em grandes plataformas.", "Nunca vale."], 0, "Complexidade."),
        ]),
    ],
    ["Kubernetes mantém o estado desejado: réplicas, recuperação, escala.", "Pod, deployment, service.", "Use quando a escala justificar."],
    "Filas e processamento assíncrono.",
    livro=("MISSING:metaprogramming", "Missing Semester, aula “Metaprogramming”", "Como a aula trata sistemas de build e dependências?"))

AULAS["Filas e processamento assíncrono"] = aula(
    25,
    "Gerar um relatório com LLM leva 40 segundos; transcrever um áudio, minutos. Se a API espera tudo isso, as conexões acumulam e o servidor trava. A solução é responder na hora “recebido, número 123”, colocar a tarefa numa fila e deixar trabalhadores processarem em segundo plano.",
    ["entender produtor, fila e trabalhador;", "devolver um identificador e consultar o status;", "tratar falhas com novas tentativas e fila de mortos."],
    ["FastAPI, APIs de LLMs e tratamento de erros."],
    [
        chute("Por que não processar um vídeo de 10 minutos dentro da requisição HTTP?", ["Porque é ilegal.", "A conexão pode cair, o servidor fica preso e o usuário não sabe o que está acontecendo.", "Porque vídeos não cabem em JSON."], 1,
              ["Não há problema legal.", "Isso! Tarefas longas vão para a fila; a API só registra e informa o status.", "Dá para enviar arquivos."],
              "Requisição rápida, trabalho pesado em segundo plano."),
        concreto("A senha da padaria", "<p>Na padaria cheia, você pega uma senha e vai fazer outra coisa; quando chamam seu número, você busca o pedido. Ninguém fica parado no balcão esperando o pão assar. A senha é o ID da tarefa; os padeiros são os trabalhadores.</p>"),
        nota("As peças", [
            ("Produtor", "quem cria a tarefa", "A API recebe o pedido e o coloca na fila."),
            ("Fila", "a lista de espera", "Redis, RabbitMQ, SQS, Pub/Sub."),
            ("Trabalhador (worker)", "quem processa", "Celery, RQ, Dramatiq; vários em paralelo."),
            ("Status", "pendente → processando → pronto/erro", "O cliente consulta pelo ID (ou recebe um webhook)."),
            ("Fila de mortos (DLQ)", "tarefas que falharam demais", "Separadas para investigação."),
        ]),
        cod("Uma fila com trabalhadores", "Implemente <code>enviar(dados)</code> (gera um ID, guarda o status <code>\"pendente\"</code> e põe na fila) e <code>trabalhar()</code> (processa toda a fila: em caso de exceção, tenta de novo até 3 vezes; depois disso, status <code>\"erro\"</code> e a tarefa vai para <code>mortas</code>).",
            '''
from collections import deque

fila = deque()
status = {}
resultados = {}
mortas = []
contador = {"n": 0}

def processar(dados):
    if dados == "ruim":
        raise RuntimeError("falhou")
    return dados.upper()

def enviar(dados):
    contador["n"] += 1
    return contador["n"]

def trabalhar(max_tentativas=3):
    pass

a, b = enviar("relatorio"), enviar("ruim")
trabalhar()
print(status, resultados, mortas)
''',
            [("Status inicial", "fila.clear(); status.clear(); resultados.clear(); mortas.clear()\nx = enviar('oi')\nassert status[x] == 'pendente' and len(fila) == 1"),
             ("Processa", "fila.clear(); status.clear(); resultados.clear(); mortas.clear()\nx = enviar('oi'); trabalhar()\nassert status[x] == 'pronto' and resultados[x] == 'OI'"),
             ("Falha vai para mortas", "fila.clear(); status.clear(); resultados.clear(); mortas.clear()\ny = enviar('ruim'); trabalhar()\nassert status[y] == 'erro' and mortas == [y] and not fila")],
            '''
from collections import deque

fila = deque()
status = {}
resultados = {}
mortas = []
contador = {"n": 0}

def processar(dados):
    if dados == "ruim":
        raise RuntimeError("falhou")
    return dados.upper()

def enviar(dados):
    contador["n"] += 1
    tid = contador["n"]
    status[tid] = "pendente"
    fila.append((tid, dados, 0))
    return tid

def trabalhar(max_tentativas=3):
    while fila:
        tid, dados, tentativas = fila.popleft()
        status[tid] = "processando"
        try:
            resultados[tid] = processar(dados)
            status[tid] = "pronto"
        except Exception:
            if tentativas + 1 < max_tentativas:
                fila.append((tid, dados, tentativas + 1))
            else:
                status[tid] = "erro"
                mortas.append(tid)

a, b = enviar("relatorio"), enviar("ruim")
trabalhar()
print(status, resultados, mortas)
''', ["Guarde na fila a tupla (id, dados, tentativas).", "Na exceção, recoloque com tentativas + 1 ou mande para <code>mortas</code>."]),
        erros([("Tarefas que não podem ser repetidas com segurança.", "Faça tarefas idempotentes: rodar duas vezes deve dar o mesmo efeito (não cobrar duas vezes!)."), ("Fila sem limite.", "Se os trabalhadores não dão conta, a fila cresce sem fim; monitore o tamanho."), ("Cliente sem feedback.", "Mostre status e tempo estimado.")]),
        ponte("Em aplicações de IA", "<p>Transcrição de áudio, processamento de PDFs para RAG, geração de relatórios e retreinos: tudo isso vai para filas. A arquitetura API + fila + trabalhadores é das mais comuns em produtos de IA.</p>"),
        quiz([
            ("O que a API devolve ao receber uma tarefa longa?", ["O resultado final.", "Um ID para consultar o status.", "Nada."], 1, "A senha."),
            ("Para que serve a fila de mortos?", ["Separar tarefas que falharam repetidamente.", "Apagar tarefas antigas.", "Acelerar a fila."], 0, "Investigação."),
            ("O que é uma tarefa idempotente?", ["Repetir não causa efeito duplicado.", "Roda só uma vez.", "Nunca falha."], 0, "Segura para repetir."),
        ]),
    ],
    ["API rápida + fila + trabalhadores em segundo plano.", "ID e status para o cliente acompanhar.", "Novas tentativas, fila de mortos e idempotência."],
    "Redis, Postgres e pgvector.",
    livro=("FASTAPI:tutorial/background-tasks", "Documentação do FastAPI, “Tarefas em segundo plano”", "Quando a documentação recomenda usar uma fila como Celery em vez das tarefas internas?"))

AULAS["Redis, Postgres e pgvector"] = aula(
    30,
    "Quase toda aplicação de IA usa dois bancos: um <b>Postgres</b> para os dados permanentes (usuários, documentos, histórico) e um <b>Redis</b> na memória para o que precisa ser instantâneo (cache, filas, limites de uso). Com a extensão <b>pgvector</b>, o Postgres também vira banco vetorial para o seu RAG.",
    ["escolher entre Postgres e Redis para cada dado;", "usar cache com tempo de expiração;", "fazer busca vetorial com pgvector em SQL."],
    ["SQL, bancos vetoriais e filas."],
    [
        chute("Onde guardar o resultado de uma chamada cara de LLM que pode ser reaproveitado por 1 hora?", ["No Postgres, para sempre.", "No Redis, com expiração de 1 hora.", "Na memória do navegador."], 1,
              ["Permanente demais e mais lento para isso.", "Isso! Cache com TTL: rápido e se apaga sozinho.", "Outros usuários não aproveitariam."],
              "Redis para o temporário e rápido; Postgres para o permanente."),
        concreto("O arquivo e a mesa", "<p>O Postgres é o arquivo de aço do escritório: guarda tudo, organizado e seguro. O Redis é a sua mesa: só o que você está usando agora, ao alcance da mão. O que fica muito tempo na mesa é guardado no arquivo ou jogado fora.</p>"),
        tabela("Quem guarda o quê", ["Dado", "Onde"], [
            ["usuários, documentos, pedidos", "Postgres"],
            ["embeddings dos documentos (RAG)", "Postgres + pgvector"],
            ["cache de respostas", "Redis (com TTL)"],
            ["filas de tarefas", "Redis (ou serviço de filas)"],
            ["contadores de limite de uso", "Redis"],
            ["sessões de login", "Redis"],
        ], rot="Organize na cabeça"),
        texto("Busca vetorial em SQL", sh('''
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE trechos (id serial PRIMARY KEY, texto text, embedding vector(768));
CREATE INDEX ON trechos USING hnsw (embedding vector_cosine_ops);

-- os 5 trechos mais parecidos com a pergunta (<=> é a distância de cosseno)
SELECT texto FROM trechos ORDER BY embedding <=> :embedding_da_pergunta LIMIT 5;
''') + "<p>A grande vantagem: filtros comuns e busca vetorial na mesma consulta (<code>WHERE setor = 'jurídico'</code>), no mesmo banco, com as mesmas permissões.</p>", rot="Mão na massa"),
        cod("Um cache com expiração", "Implemente o essencial do Redis para cache: <code>set(chave, valor, ttl)</code> e <code>get(chave)</code>, que devolve <code>None</code> se a chave não existe ou já expirou. Use o relógio <code>agora()</code> fornecido (que o teste controla).",
            '''
relogio = {"t": 0}

def agora():
    return relogio["t"]

class Cache:
    def __init__(self):
        self.dados = {}

    def set(self, chave, valor, ttl):
        self.dados[chave] = valor

    def get(self, chave):
        return self.dados.get(chave)

c = Cache()
c.set("resposta:clima", "sol", ttl=60)
relogio["t"] = 30
print(c.get("resposta:clima"))
relogio["t"] = 61
print(c.get("resposta:clima"))
''',
            [("Antes de expirar", "relogio['t'] = 0\nc = Cache(); c.set('k', 'v', ttl=10)\nrelogio['t'] = 9\nassert c.get('k') == 'v'"),
             ("Depois de expirar", "relogio['t'] = 0\nc = Cache(); c.set('k', 'v', ttl=10)\nrelogio['t'] = 10\nassert c.get('k') is None"),
             ("Chave inexistente", "assert Cache().get('nada') is None")],
            '''
relogio = {"t": 0}

def agora():
    return relogio["t"]

class Cache:
    def __init__(self):
        self.dados = {}

    def set(self, chave, valor, ttl):
        self.dados[chave] = (valor, agora() + ttl)

    def get(self, chave):
        item = self.dados.get(chave)
        if item is None:
            return None
        valor, expira = item
        if agora() >= expira:
            del self.dados[chave]
            return None
        return valor

c = Cache()
c.set("resposta:clima", "sol", ttl=60)
relogio["t"] = 30
print(c.get("resposta:clima"))
relogio["t"] = 61
print(c.get("resposta:clima"))
''', ["Guarde (valor, momento de expiração).", "No <code>get</code>, compare <code>agora()</code> com a expiração."]),
        erros([("Usar o Redis como banco principal.", "Ele vive na memória; configure persistência ou guarde o permanente no Postgres."), ("Cache sem expiração.", "Dados velhos e memória cheia; sempre defina TTL."), ("Um banco vetorial separado sem necessidade.", "Para milhões de vetores, o pgvector costuma bastar e simplifica a arquitetura.")]),
        ponte("A arquitetura típica", "<p>API (FastAPI) + Postgres com pgvector + Redis para cache e filas + trabalhadores. Com <code>docker compose</code>, tudo isso sobe na sua máquina com um comando, e é uma ótima base para projetos de portfólio.</p>"),
        quiz([
            ("Para que serve o TTL no cache?", ["Apagar automaticamente dados após um tempo.", "Criptografar.", "Comprimir."], 0, "Expiração."),
            ("O pgvector adiciona ao Postgres:", ["Busca por similaridade de vetores.", "Uma interface gráfica.", "Suporte a imagens."], 0, "RAG no SQL."),
            ("Onde guardar contadores de limite de uso por minuto?", ["No Redis.", "Num arquivo de texto.", "No README."], 0, "Rápido e temporário."),
        ]),
    ],
    ["Postgres para o permanente; Redis para o rápido e temporário.", "Cache sempre com TTL.", "pgvector: RAG com SQL e filtros no mesmo banco."],
    "Interfaces com Gradio e Streamlit.",
    livro=("MADEML:x", "Made With ML (MLOps)", "Como o curso organiza dados, modelos e serviços de um projeto?"))

AULAS["Interfaces com Gradio e Streamlit"] = aula(
    20,
    "Um modelo sem interface só impressiona quem lê código. Com Gradio ou Streamlit, você cria em poucas linhas uma página onde qualquer pessoa digita, envia uma imagem ou conversa com seu modelo. É o jeito mais rápido de mostrar um projeto no portfólio.",
    ["criar uma interface com Gradio;", "comparar Gradio e Streamlit;", "publicar no Hugging Face Spaces."],
    ["Funções, Streamlit (Fase 2) e Hugging Face."],
    [
        chute("Você quer uma demo de chatbot para o portfólio, publicada hoje, de graça. O caminho mais curto:", ["Construir um front-end em React do zero.", "Gradio + Hugging Face Spaces.", "Um aplicativo de celular."], 1,
              ["Leva dias.", "Isso! Algumas linhas de Python e um repositório no Spaces dão uma URL pública.", "Muito mais trabalho."],
              "Demo rápida primeiro; front-end próprio quando o produto pedir."),
        concreto("A vitrine", "<p>Uma loja pode ter o melhor produto, mas se a vitrine está vazia ninguém entra. A interface é a vitrine do seu modelo: recrutadores e usuários testam em 30 segundos, sem instalar nada.</p>"),
        lab("Um chat com Gradio", '''
import gradio as gr

def responder(mensagem, historico):
    # troque por uma chamada ao seu modelo ou RAG
    return f"Você disse: {mensagem}"

gr.ChatInterface(responder, title="Meu assistente").launch()
''', corpo="<p>Instale com <code>pip install gradio</code> e rode:</p>", exps=["Troque a função por uma chamada ao modelo local do Ollama.", "Crie um Space no Hugging Face e envie <code>app.py</code> e <code>requirements.txt</code>."]),
        tabela("Gradio × Streamlit", ["", "Gradio", "Streamlit"], [
            ["Melhor para", "demos de modelos (entrada → saída, chat)", "dashboards e apps de dados"],
            ["Modelo mental", "função com entradas e saídas", "script que roda de cima a baixo"],
            ["Publicação grátis", "Hugging Face Spaces", "Streamlit Community Cloud / Spaces"],
        ], rot="Organize na cabeça"),
        cod("Pensando como o Gradio", "O Gradio liga componentes de entrada a uma função e a componentes de saída. Escreva <code>interface(fn, entradas, saidas)</code> que devolve uma função <code>enviar(valores)</code>: ela converte cada valor conforme o tipo do componente (<code>\"numero\"</code> → float, <code>\"texto\"</code> → str), chama <code>fn</code> e devolve um dicionário {nome da saída: valor}.",
            '''
def interface(fn, entradas, saidas):
    def enviar(valores):
        return {}
    return enviar

def prever_preco(area, bairro):
    return area * (8000 if bairro == "centro" else 5000), "ok"

app = interface(prever_preco, [("area", "numero"), ("bairro", "texto")], ["preco", "status"])
print(app(["50", "centro"]))
''',
            [("Converte e chama", "assert app(['50', 'centro']) == {'preco': 400000.0, 'status': 'ok'}"),
             ("Uma saída só", "app2 = interface(lambda t: t.upper(), [('t', 'texto')], ['maiusculo'])\nassert app2(['oi']) == {'maiusculo': 'OI'}")],
            '''
def interface(fn, entradas, saidas):
    conversores = {"numero": float, "texto": str}
    def enviar(valores):
        args = [conversores[tipo](v) for (nome, tipo), v in zip(entradas, valores)]
        r = fn(*args)
        if len(saidas) == 1:
            r = (r,)
        return dict(zip(saidas, r))
    return enviar

def prever_preco(area, bairro):
    return area * (8000 if bairro == "centro" else 5000), "ok"

app = interface(prever_preco, [("area", "numero"), ("bairro", "texto")], ["preco", "status"])
print(app(["50", "centro"]))
''', ["Converta com um dicionário de tipos.", "Se houver uma saída só, embrulhe o resultado numa tupla antes do <code>zip</code>."]),
        erros([("Chave de API no código do Space.", "Use os segredos do Space (variáveis de ambiente)."), ("Demo sem exemplos.", "Use <code>examples=[...]</code>: quem visita clica e vê funcionando."), ("Demo que trava com uso.", "Use filas (<code>.queue()</code>) e modelos que caibam no hardware gratuito.")]),
        ponte("Portfólio que se usa", "<p>Um link “teste aqui” no README e no LinkedIn vale mais que mil palavras. Coloque cada projeto de IA com uma demo pública.</p>"),
        quiz([
            ("Gradio é especialmente bom para:", ["Demos de modelos com entrada e saída.", "Bancos de dados.", "Treinar modelos."], 0, "Função → interface."),
            ("Onde publicar de graça uma demo Gradio?", ["Hugging Face Spaces.", "No e-mail.", "Não é possível."], 0, "Spaces."),
            ("Onde guardar a chave de API numa demo publicada?", ["Nos segredos do serviço.", "No código.", "No README."], 0, "Variáveis de ambiente."),
        ]),
    ],
    ["Gradio: função → interface em poucas linhas.", "Streamlit para dashboards; Gradio para demos.", "Publique no Spaces com segredos e exemplos."],
    "Front-end básico (HTML e JS).",
    livro=("HF:chapter9/1", "LLM Course, capítulo 9, “Building and sharing demos”", "Que componentes do Gradio o capítulo apresenta?"))

AULAS["Front-end básico (HTML e JS)"] = aula(
    30,
    "Uma hora o Gradio não basta: o cliente quer a interface com a cara da empresa, dentro do site que já existe. Saber o básico de HTML, CSS e JavaScript permite criar uma página que chama a sua API e mostra o resultado, inclusive com a resposta do LLM aparecendo aos poucos.",
    ["estruturar uma página com HTML;", "chamar uma API com <code>fetch</code>;", "mostrar resultados e erros na página."],
    ["FastAPI e JSON."],
    [
        chute("Sua página em <code>meusite.com</code> chama a API em <code>api.meusite.com</code> e o navegador bloqueia. O motivo provável:", ["A API está fora do ar.", "CORS: a API precisa permitir explicitamente esse site de origem.", "JavaScript não faz requisições."], 1,
              ["Pode ser, mas o erro típico aqui é outro.", "Isso! Navegadores bloqueiam chamadas entre origens diferentes, a menos que o servidor autorize (no FastAPI, <code>CORSMiddleware</code>).", "Faz, com <code>fetch</code>."],
              "Erro de CORS se resolve no servidor."),
        concreto("O corpo, a roupa e o movimento", "<p>HTML é o esqueleto (o que existe na página), CSS é a roupa (como parece), JavaScript é o movimento (o que acontece quando você clica). Para conversar com a sua API, o movimento é o <code>fetch</code>.</p>"),
        texto("Uma página que chama sua API", '<pre class="lv2-code" data-lang="html"><code>' + '''&lt;input id="area" type="number" placeholder="Área em m²"&gt;
&lt;button id="botao"&gt;Prever&lt;/button&gt;
&lt;p id="resultado"&gt;&lt;/p&gt;
&lt;script&gt;
document.getElementById("botao").addEventListener("click", async () =&gt; {
  const area = Number(document.getElementById("area").value);
  const resp = await fetch("/prever", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({area: area, quartos: 2}),
  });
  const saidaEl = document.getElementById("resultado");
  if (!resp.ok) { saidaEl.textContent = "Erro: verifique os dados."; return; }
  const dados = await resp.json();
  saidaEl.textContent = "Preço estimado: " + dados.preco.toLocaleString("pt-BR");
});
&lt;/script&gt;''' + '</code></pre>', rot="Mão na massa"),
        nota("O essencial", [
            ("<code>document.getElementById</code>", "pegar um elemento", "Para ler ou escrever na página."),
            ("<code>addEventListener(\"click\", ...)</code>", "reagir a ações", "Clique, digitação, envio."),
            ("<code>await fetch(url, opções)</code>", "chamar a API", "Método, cabeçalhos e corpo em JSON."),
            ("<code>textContent</code>", "mostrar texto", "Seguro: não interpreta HTML (evita injeção)."),
        ]),
        cod("Montando a requisição", "Antes de escrever em JavaScript, pense na lógica em Python: escreva <code>montar_requisicao(formulario)</code> que valida os campos (área positiva, quartos inteiros de 0 a 20), e devolve o dicionário com <code>method</code>, <code>headers</code> e <code>body</code> (JSON em string), ou levanta <code>ValueError</code> com a mensagem para mostrar ao usuário.",
            '''
import json

def montar_requisicao(formulario):
    return {}

print(montar_requisicao({"area": "72", "quartos": "3"}))
''',
            [("Requisição correta", "r = montar_requisicao({'area': '72', 'quartos': '3'})\nassert r['method'] == 'POST' and r['headers'] == {'Content-Type': 'application/json'} and json.loads(r['body']) == {'area': 72.0, 'quartos': 3}"),
             ("Área inválida", "try:\n    montar_requisicao({'area': '-5', 'quartos': '1'})\n    ok = False\nexcept ValueError:\n    ok = True\nassert ok"),
             ("Quartos inválidos", "try:\n    montar_requisicao({'area': '50', 'quartos': '2.5'})\n    ok = False\nexcept ValueError:\n    ok = True\nassert ok")],
            '''
import json

def montar_requisicao(formulario):
    try:
        area = float(formulario["area"])
        quartos = int(formulario["quartos"])
    except (KeyError, ValueError):
        raise ValueError("Preencha área e quartos com números.")
    if area <= 0:
        raise ValueError("A área deve ser positiva.")
    if not 0 <= quartos <= 20:
        raise ValueError("Quartos deve estar entre 0 e 20.")
    return {"method": "POST", "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"area": area, "quartos": quartos})}

print(montar_requisicao({"area": "72", "quartos": "3"}))
''', ["<code>int(\"2.5\")</code> levanta <code>ValueError</code>: aproveite isso.", "O corpo é <code>json.dumps(...)</code>."]),
        erros([("Usar <code>innerHTML</code> com a resposta do modelo.", "Se a resposta tiver HTML, ele roda na página; use <code>textContent</code> ou sanitize."), ("Chave de API no JavaScript.", "Tudo no navegador é público: a chave fica no servidor."), ("Só validar no front-end.", "Valide de novo no servidor; o front-end pode ser contornado.")]),
        ponte("Streaming na tela", "<p>Para mostrar a resposta do LLM aparecendo aos poucos, a API envia pedaços (Server-Sent Events) e o JavaScript lê o corpo com <code>resp.body.getReader()</code>, acrescentando cada pedaço na página. O princípio é o mesmo da requisição desta aula.</p>"),
        quiz([
            ("Qual a função do JavaScript na página?", ["Comportamento e chamadas à API.", "Estrutura.", "Banco de dados."], 0, "Movimento."),
            ("Como resolver um erro de CORS?", ["No servidor, permitindo a origem do site.", "Trocando de navegador.", "Apagando o JavaScript."], 0, "CORSMiddleware."),
            ("Por que preferir <code>textContent</code> a <code>innerHTML</code> para respostas do modelo?", ["Evita que HTML malicioso seja executado.", "É mais bonito.", "Não há diferença."], 0, "Segurança."),
        ]),
    ],
    ["HTML estrutura, CSS veste, JavaScript age.", "<code>fetch</code> com JSON para chamar a API.", "Chaves no servidor; <code>textContent</code> para respostas."],
    "Autenticação e limites de uso.",
    livro=("FASTAPI:tutorial/cors", "Documentação do FastAPI, “CORS (Cross-Origin Resource Sharing)”", "Como configurar as origens permitidas?"))

AULAS["Autenticação e limites de uso"] = aula(
    25,
    "Uma API de IA aberta na internet é um convite: alguém descobre a URL e gasta seu orçamento de tokens em uma noite. Autenticação diz <b>quem</b> está chamando; limites de uso dizem <b>quanto</b> cada um pode chamar. Os dois juntos protegem dinheiro, dados e disponibilidade.",
    ["diferenciar autenticação e autorização;", "usar chaves de API e tokens com segurança;", "implementar limite de uso com balde de fichas."],
    ["FastAPI, Redis e front-end."],
    [
        chute("Qual a forma certa de guardar as senhas dos usuários no banco?", ["Em texto puro.", "Com um hash lento e com sal (bcrypt, argon2).", "Criptografadas com uma chave no código."], 1,
              ["Um vazamento expõe tudo.", "Isso! Nem você consegue ler; só verifica se a senha digitada gera o mesmo hash.", "Se a chave vazar, todas as senhas vazam."],
              "Senhas nunca são guardadas; só seus hashes."),
        concreto("O crachá e a catraca", "<p>Na portaria, o crachá prova quem você é (autenticação) e define em que andares pode entrar (autorização). A catraca do refeitório limita uma refeição por pessoa (limite de uso). Sua API precisa dos três.</p>"),
        nota("As peças", [
            ("Autenticação", "quem é você?", "Login, chave de API, token."),
            ("Autorização", "o que você pode fazer?", "Papéis e permissões."),
            ("JWT", "token assinado", "O servidor confere a assinatura; expira em minutos ou horas."),
            ("OAuth / “Entrar com Google”", "login delegado", "Evita você guardar senhas."),
            ("Limite de uso (rate limit)", "quantas chamadas", "Por usuário, por minuto e por dia; erro 429 ao estourar."),
        ]),
        cod("Assinando tokens", "Implemente um token simples assinado com HMAC: <code>gerar(usuario, segredo, expira_em)</code> devolve <code>\"usuario|expira|assinatura\"</code>; <code>verificar(token, segredo, agora)</code> devolve o usuário se a assinatura confere e o token não expirou, ou <code>None</code>. Use <code>hmac.compare_digest</code>.",
            '''
import hmac, hashlib

def assinar(mensagem, segredo):
    return hmac.new(segredo.encode(), mensagem.encode(), hashlib.sha256).hexdigest()

def gerar(usuario, segredo, expira_em):
    return f"{usuario}|{expira_em}|"

def verificar(token, segredo, agora):
    return token.split("|")[0]

t = gerar("ana", "s3gredo", 1000)
print(verificar(t, "s3gredo", 500))
''',
            [("Token válido", "assert verificar(gerar('ana', 'k', 1000), 'k', 500) == 'ana'"),
             ("Expirado", "assert verificar(gerar('ana', 'k', 1000), 'k', 1001) is None"),
             ("Adulterado", "u, e, a = gerar('ana', 'k', 1000).split('|')\nassert verificar(f'admin|{e}|{a}', 'k', 500) is None"),
             ("Segredo errado", "assert verificar(gerar('ana', 'k', 1000), 'outro', 500) is None")],
            '''
import hmac, hashlib

def assinar(mensagem, segredo):
    return hmac.new(segredo.encode(), mensagem.encode(), hashlib.sha256).hexdigest()

def gerar(usuario, segredo, expira_em):
    corpo = f"{usuario}|{expira_em}"
    return f"{corpo}|{assinar(corpo, segredo)}"

def verificar(token, segredo, agora):
    try:
        usuario, expira, assinatura = token.split("|")
    except ValueError:
        return None
    if not hmac.compare_digest(assinatura, assinar(f"{usuario}|{expira}", segredo)):
        return None
    if agora > int(expira):
        return None
    return usuario

t = gerar("ana", "s3gredo", 1000)
print(verificar(t, "s3gredo", 500))
''', ["Assine <code>f\"{usuario}|{expira_em}\"</code> e acrescente a assinatura.", "Na verificação, recalcule a assinatura e compare com <code>hmac.compare_digest</code>."]),
        cod("Balde de fichas", "Implemente o limite de uso mais comum: cada usuário tem um balde com até <code>capacidade</code> fichas, que se recarrega a <code>taxa</code> fichas por segundo. Cada chamada gasta uma ficha; sem fichas, a chamada é recusada (429).",
            '''
class Balde:
    def __init__(self, capacidade, taxa):
        self.capacidade = capacidade
        self.taxa = taxa
        self.fichas = capacidade
        self.ultimo = 0.0

    def permitir(self, agora):
        return True

b = Balde(capacidade=3, taxa=1)
print([b.permitir(0) for _ in range(4)], b.permitir(1.0), b.permitir(1.0))
''',
            [("Rajada limitada", "b = Balde(3, 1)\nassert [b.permitir(0) for _ in range(4)] == [True, True, True, False]"),
             ("Recarga", "b = Balde(3, 1)\nfor _ in range(3): b.permitir(0)\nassert b.permitir(1.0) is True and b.permitir(1.0) is False"),
             ("Não passa da capacidade", "b = Balde(2, 1)\nassert [b.permitir(100) for _ in range(3)] == [True, True, False]")],
            '''
class Balde:
    def __init__(self, capacidade, taxa):
        self.capacidade = capacidade
        self.taxa = taxa
        self.fichas = capacidade
        self.ultimo = 0.0

    def permitir(self, agora):
        self.fichas = min(self.capacidade, self.fichas + (agora - self.ultimo) * self.taxa)
        self.ultimo = agora
        if self.fichas >= 1:
            self.fichas -= 1
            return True
        return False

b = Balde(capacidade=3, taxa=1)
print([b.permitir(0) for _ in range(4)], b.permitir(1.0), b.permitir(1.0))
''', ["Recarregue: <code>min(capacidade, fichas + tempo_passado × taxa)</code>.", "Se houver pelo menos 1 ficha, gaste e permita."], rot="Mão no código · nível 2"),
        erros([("Inventar sua própria criptografia.", "Use bibliotecas consolidadas (passlib, PyJWT, Authlib) e provedores de login."), ("Limite só por IP.", "Muitos usuários compartilham IP; limite por conta também."), ("Sem limite de gasto por usuário em apps com LLM.", "Defina cotas diárias de tokens por usuário.")]),
        ponte("Na prática", "<p>Serviços como Supabase, Auth0, Clerk e Firebase cuidam do login; um middleware com Redis faz o limite de uso. Você foca no produto, sem reinventar segurança.</p>"),
        quiz([
            ("Autorização responde:", ["Quem é você?", "O que você pode fazer?", "Quanto custa?"], 1, "Permissões."),
            ("Como guardar senhas?", ["Hash lento com sal (bcrypt/argon2).", "Texto puro.", "Base64."], 0, "Nunca a senha em si."),
            ("Qual código HTTP indica limite de uso excedido?", ["404.", "429.", "200."], 1, "Too Many Requests."),
        ]),
    ],
    ["Autenticação = quem; autorização = o quê; limite = quanto.", "Senhas com hash; tokens assinados e com validade.", "Balde de fichas por usuário, com cotas de tokens."],
    "Observabilidade de LLMs.",
    livro=("FASTAPI:tutorial/security", "Documentação do FastAPI, “Segurança”", "Que fluxos de autenticação a documentação apresenta?"))

AULAS["Observabilidade de LLMs"] = aula(
    25,
    "Um usuário reclama: “o assistente respondeu errado ontem”. Sem registros, você não tem como saber o que aconteceu. Observabilidade é registrar cada etapa (prompt, documentos recuperados, ferramentas chamadas, resposta, tokens, tempo e custo) para depurar, avaliar e melhorar.",
    ["registrar rastros (traces) de cada chamada;", "acompanhar métricas de custo, latência e qualidade;", "transformar falhas reais em casos de avaliação."],
    ["Custo e latência, avaliação de LLMs e monitoramento."],
    [
        chute("O que é mais útil registrar num sistema RAG para depurar uma resposta errada?", ["Só a resposta final.", "A pergunta, os trechos recuperados, o prompt montado, a resposta e o tempo de cada etapa.", "Nada, por privacidade."], 1,
              ["Não mostra onde errou.", "Isso! Com o rastro completo, você vê se o erro foi na busca, no prompt ou no modelo.", "Registre com cuidado (anonimizando), mas registre."],
              "Rastro = a história completa de uma requisição."),
        concreto("A caixa-preta do avião", "<p>Depois de um incidente, os investigadores leem a caixa-preta: cada comando, cada leitura de instrumento, em ordem. Os rastros do seu sistema de IA são a caixa-preta: mostram exatamente o que aconteceu em cada etapa.</p>"),
        nota("As peças", [
            ("Trace (rastro)", "uma requisição", "Do pedido do usuário à resposta."),
            ("Span", "uma etapa", "Busca, chamada ao LLM, ferramenta: cada uma com início, fim e dados."),
            ("Métricas", "agregados", "Custo por dia, latência p95, taxa de erro, notas dos usuários."),
            ("Feedback", "👍 / 👎", "Liga a opinião do usuário ao rastro exato."),
            ("Ferramentas", "Langfuse, LangSmith, Phoenix, OpenTelemetry", "Muitas são de código aberto."),
        ]),
        cod("Rastreando etapas", "Implemente um decorador <code>span(nome)</code> que registra em <code>RASTRO</code> o nome da etapa, a duração (use <code>relogio()</code>) e, se a função devolver um dicionário com <code>tokens</code>, também os tokens. Depois, <code>resumo()</code> devolve a duração total e os tokens totais.",
            '''
import functools

tempo = {"t": 0.0}
def relogio():
    return tempo["t"]

RASTRO = []

def span(nome):
    def decorador(f):
        return f
    return decorador

@span("busca")
def buscar(p):
    tempo["t"] += 0.2
    return {"trechos": ["a", "b"]}

@span("llm")
def gerar(p, trechos):
    tempo["t"] += 1.5
    return {"texto": "resposta", "tokens": 850}

def resumo():
    return 0.0, 0

gerar("pergunta", buscar("pergunta")["trechos"])
print(RASTRO, resumo())
''',
            [("Etapas registradas", "assert [s['nome'] for s in RASTRO] == ['busca', 'llm'], f'{RASTRO}'"),
             ("Durações e tokens", "assert abs(RASTRO[0]['duracao'] - 0.2) < 1e-9 and RASTRO[1]['tokens'] == 850"),
             ("Resumo", "d, t = resumo()\nassert abs(d - 1.7) < 1e-9 and t == 850"),
             ("Mantém o retorno", "assert gerar('x', [])['texto'] == 'resposta'")],
            '''
import functools

tempo = {"t": 0.0}
def relogio():
    return tempo["t"]

RASTRO = []

def span(nome):
    def decorador(f):
        @functools.wraps(f)
        def envolvida(*args, **kwargs):
            inicio = relogio()
            r = f(*args, **kwargs)
            reg = {"nome": nome, "duracao": relogio() - inicio}
            if isinstance(r, dict) and "tokens" in r:
                reg["tokens"] = r["tokens"]
            RASTRO.append(reg)
            return r
        return envolvida
    return decorador

@span("busca")
def buscar(p):
    tempo["t"] += 0.2
    return {"trechos": ["a", "b"]}

@span("llm")
def gerar(p, trechos):
    tempo["t"] += 1.5
    return {"texto": "resposta", "tokens": 850}

def resumo():
    return sum(s["duracao"] for s in RASTRO), sum(s.get("tokens", 0) for s in RASTRO)

gerar("pergunta", buscar("pergunta")["trechos"])
print(RASTRO, resumo())
''', ["Dentro do decorador, meça <code>relogio()</code> antes e depois.", "Se o retorno for dict com <code>tokens</code>, registre também."]),
        erros([("Registrar dados pessoais sem cuidado.", "Anonimize, defina retenção e restrinja o acesso (LGPD)."), ("Olhar só médias.", "Acompanhe o p95 e p99 da latência: são os usuários mais irritados."), ("Ignorar o feedback dos usuários.", "Cada 👎 com rastro é um caso de teste pronto para o seu eval.")]),
        ponte("O ciclo de melhoria", "<p>Rastros revelam falhas → falhas viram casos no eval → você muda o prompt ou a busca → o eval confirma a melhora → publica → os rastros mostram o resultado. É assim que sistemas de IA melhoram em produção.</p>"),
        quiz([
            ("O que é um span?", ["Uma etapa dentro de um rastro.", "Um tipo de spam.", "Um modelo."], 0, "Busca, LLM, ferramenta."),
            ("Por que acompanhar o p95 da latência?", ["Mostra a experiência dos casos mais lentos.", "É a média.", "Não importa."], 0, "Cauda."),
            ("O que fazer com respostas marcadas como ruins?", ["Transformá-las em casos de avaliação.", "Apagar.", "Ignorar."], 0, "Melhoria contínua."),
        ]),
    ],
    ["Registre rastros com etapas, tokens, tempo e custo.", "Métricas: custo, latência p95, erros, feedback.", "Falhas reais alimentam os evals."],
    "Carreira: 3 a 5 projetos documentados no GitHub.",
    livro=("MADEML:x", "Made With ML (MLOps)", "Que práticas de monitoramento o curso recomenda?"))
