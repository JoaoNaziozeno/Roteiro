# -*- coding: utf-8 -*-
"""Aulas Visuais de IA · Fase 6 (parte A): engenharia para colocar modelos em produção."""
from lesson_factory import *

AULAS = {}

AULAS["Docker"] = aula(
    30,
    "“Na minha máquina funciona” é a frase mais famosa da programação. O Docker acaba com ela: empacota seu código, as bibliotecas, a versão do Python e o sistema num <b>contêiner</b> que roda igual no seu notebook, no servidor e na nuvem.",
    ["diferenciar imagem e contêiner;", "escrever um Dockerfile para uma aplicação Python;", "usar camadas e cache para builds rápidos."],
    ["Ambientes virtuais e pip, linha de comando."],
    [
        chute("Qual a diferença entre imagem e contêiner?", ["São a mesma coisa.", "A imagem é a receita congelada; o contêiner é ela rodando.", "O contêiner é o arquivo; a imagem é o processo."], 1,
              ["São conceitos diferentes.", "Isso! Como classe e objeto: da mesma imagem você cria vários contêineres.", "É o contrário."],
              "Imagem = molde; contêiner = instância em execução."),
        concreto("O contêiner do porto", "<p>Antes dos contêineres de navio, cada carga era embarcada de um jeito. Com a caixa padrão, qualquer navio, trem ou caminhão leva qualquer carga. O Docker faz isso com software: uma caixa padrão que qualquer servidor sabe rodar.</p>"),
        texto("Um Dockerfile para uma API em Python", sh('''
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''') + "<p>E para construir e rodar:</p>" + sh('''
docker build -t minha-api .
docker run -p 8000:8000 minha-api
'''), rot="Mão na massa"),
        nota("As instruções", [
            ("<code>FROM</code>", "imagem base", "Prefira versões fixas e enxutas (<code>-slim</code>)."),
            ("<code>COPY requirements.txt</code> antes do código", "cache de camadas", "Se só o código mudou, as dependências não são reinstaladas."),
            ("<code>RUN</code>", "executa no build", "Cada instrução vira uma camada."),
            ("<code>CMD</code>", "comando ao iniciar", "O processo principal do contêiner."),
            ("<code>docker compose</code>", "vários serviços", "API + banco + Redis num arquivo só."),
        ]),
        cod("Cache de camadas", "O Docker reaproveita camadas até a primeira instrução cujo conteúdo mudou; dali em diante, refaz tudo. Escreva <code>camadas_refeitas(instrucoes, mudou)</code>: dada a lista de instruções e o conjunto de arquivos alterados, devolva quantas camadas serão refeitas. Uma instrução <code>COPY x</code> muda se x foi alterado (ou se é <code>COPY .</code> e algo mudou).",
            '''
def camadas_refeitas(instrucoes, mudou):
    return 0

bom = ["FROM python", "COPY requirements.txt", "RUN pip install", "COPY .", "CMD uvicorn"]
ruim = ["FROM python", "COPY .", "RUN pip install", "CMD uvicorn"]
print(camadas_refeitas(bom, {"main.py"}), camadas_refeitas(ruim, {"main.py"}))
''',
            [("Ordem boa", "assert camadas_refeitas(bom, {'main.py'}) == 2"),
             ("Ordem ruim", "assert camadas_refeitas(ruim, {'main.py'}) == 3"),
             ("Dependências mudaram", "assert camadas_refeitas(bom, {'requirements.txt'}) == 4"),
             ("Nada mudou", "assert camadas_refeitas(bom, set()) == 0")],
            '''
def camadas_refeitas(instrucoes, mudou):
    for i, ins in enumerate(instrucoes):
        if ins.startswith("COPY "):
            alvo = ins.split(" ", 1)[1]
            if (alvo == "." and mudou) or alvo in mudou:
                return len(instrucoes) - i
    return 0

bom = ["FROM python", "COPY requirements.txt", "RUN pip install", "COPY .", "CMD uvicorn"]
ruim = ["FROM python", "COPY .", "RUN pip install", "CMD uvicorn"]
print(camadas_refeitas(bom, {"main.py"}), camadas_refeitas(ruim, {"main.py"}))
''', ["Procure a primeira instrução <code>COPY</code> afetada.", "Dali até o fim, tudo é refeito: <code>len(instrucoes) - i</code>."],
            exp="<p>Por isso o <code>pip install</code> vem antes do <code>COPY .</code>: mudar uma linha de código não reinstala as bibliotecas.</p>"),
        erros([("Colocar senhas e chaves na imagem.", "Use variáveis de ambiente ou gerenciadores de segredos; imagens são fáceis de inspecionar."), ("Imagens enormes.", "Use bases <code>-slim</code>, <code>.dockerignore</code> e não copie dados ou modelos desnecessários."), ("Usar a tag <code>latest</code> em produção.", "Fixe versões para builds reproduzíveis.")]),
        ponte("Para onde vai o contêiner", "<p>Quase todo deploy moderno começa com uma imagem Docker: serviços de nuvem (Cloud Run, ECS, App Runner), Kubernetes e CI/CD. Nas próximas aulas, você coloca sua API num contêiner e na nuvem.</p>"),
        quiz([
            ("O que é um contêiner?", ["Uma imagem em execução.", "Um tipo de banco.", "Uma máquina virtual completa."], 0, "Instância da imagem."),
            ("Por que copiar o requirements.txt antes do código?", ["Para aproveitar o cache de camadas.", "Por estética.", "É obrigatório."], 0, "Dependências mudam menos."),
            ("Onde colocar segredos?", ["No Dockerfile.", "Em variáveis de ambiente/gerenciador de segredos.", "No código."], 1, "Fora da imagem."),
        ]),
    ],
    ["Imagem = receita; contêiner = execução.", "Dockerfile: base, dependências, código, comando.", "Ordene para aproveitar o cache; segredos fora da imagem."],
    "FastAPI e criação de APIs.",
    livro=("FASTAPI:deployment/docker", "Documentação do FastAPI, “FastAPI em contêineres - Docker”", "Que Dockerfile a documentação recomenda?"))

AULAS["FastAPI e criação de APIs"] = aula(
    35,
    "Seu modelo funciona no notebook. Para um site, um app ou outro sistema usá-lo, ele precisa de uma <b>API</b>: um endereço que recebe dados em JSON e devolve a previsão. O FastAPI faz isso em poucas linhas, com validação automática e documentação interativa.",
    ["criar rotas GET e POST;", "validar entradas com Pydantic;", "servir um modelo de ML com carregamento único."],
    ["Funções, JSON, APIs (consumir) e saída estruturada."],
    [
        chute("Onde carregar o modelo de ML numa API?", ["Dentro da função da rota, a cada requisição.", "Uma vez, quando a aplicação inicia.", "No navegador do usuário."], 1,
              ["Carregar a cada chamada deixa tudo lentíssimo.", "Isso! Carregue na inicialização e reutilize em todas as requisições.", "O modelo fica no servidor."],
              "Carregar é caro; prever é barato."),
        concreto("O balcão de atendimento", "<p>Uma API é um balcão: tem endereços (rotas) para cada serviço, um formulário que precisa estar preenchido certo (validação) e um atendente que já está pronto (o modelo carregado), sem precisar ir buscá-lo a cada cliente.</p>"),
        lab("Uma API de previsão", '''
from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib

app = FastAPI(title="Previsão de preço de imóveis")
modelo = joblib.load("modelo.joblib")          # carregado uma única vez

class Imovel(BaseModel):
    area: float = Field(gt=0, description="Área em m²")
    quartos: int = Field(ge=0, le=20)

@app.get("/saude")
def saude():
    return {"status": "ok"}

@app.post("/prever")
def prever(imovel: Imovel):
    preco = modelo.predict([[imovel.area, imovel.quartos]])[0]
    return {"preco": round(float(preco), 2)}
''', corpo="<p>Salve como <code>main.py</code> e rode <code>uvicorn main:app --reload</code>. Abra <code>/docs</code>:</p>", exps=["Envie uma área negativa pelo <code>/docs</code> e veja o erro 422.", "Adicione uma rota que recebe uma lista de imóveis e devolve todas as previsões."]),
        nota("O essencial", [
            ("<code>@app.get</code> / <code>@app.post</code>", "rotas", "GET para consultar, POST para enviar dados."),
            ("Modelo Pydantic", "corpo da requisição", "Validação automática; erro 422 se inválido."),
            ("<code>/docs</code>", "documentação automática", "Teste a API pelo navegador."),
            ("Códigos HTTP", "200, 400, 404, 422, 500", "Diga ao cliente o que aconteceu."),
        ]),
        cod("Um roteador de API em miniatura", "Para entender o que o FastAPI faz por baixo, implemente um decorador <code>rota(metodo, caminho)</code> que registra funções em <code>ROTAS</code>, e <code>atender(metodo, caminho, corpo)</code> que chama a função certa e devolve (código, resposta): 404 se a rota não existe, 422 se a função levantar <code>ValueError</code>.",
            '''
ROTAS = {}

def rota(metodo, caminho):
    def registrar(f):
        return f
    return registrar

def atender(metodo, caminho, corpo=None):
    return 200, None

@rota("GET", "/saude")
def saude(corpo):
    return {"status": "ok"}

@rota("POST", "/prever")
def prever(corpo):
    if corpo.get("area", 0) <= 0:
        raise ValueError("área inválida")
    return {"preco": corpo["area"] * 5000}

print(atender("POST", "/prever", {"area": 50}))
''',
            [("Rota existente", "assert atender('GET', '/saude') == (200, {'status': 'ok'})"),
             ("POST com corpo", "assert atender('POST', '/prever', {'area': 50}) == (200, {'preco': 250000})"),
             ("Validação", "assert atender('POST', '/prever', {'area': -1})[0] == 422"),
             ("Não encontrada", "assert atender('GET', '/xyz')[0] == 404 and atender('GET', '/prever')[0] == 404")],
            '''
ROTAS = {}

def rota(metodo, caminho):
    def registrar(f):
        ROTAS[(metodo, caminho)] = f
        return f
    return registrar

def atender(metodo, caminho, corpo=None):
    f = ROTAS.get((metodo, caminho))
    if f is None:
        return 404, {"erro": "não encontrado"}
    try:
        return 200, f(corpo or {})
    except ValueError as e:
        return 422, {"erro": str(e)}

@rota("GET", "/saude")
def saude(corpo):
    return {"status": "ok"}

@rota("POST", "/prever")
def prever(corpo):
    if corpo.get("area", 0) <= 0:
        raise ValueError("área inválida")
    return {"preco": corpo["area"] * 5000}

print(atender("POST", "/prever", {"area": 50}))
''', ["No decorador: <code>ROTAS[(metodo, caminho)] = f</code>.", "Em <code>atender</code>: busque a função; trate <code>ValueError</code> com 422."]),
        erros([("Modelo carregado a cada requisição.", "Carregue na inicialização."), ("Aceitar qualquer entrada.", "Valide tipos e limites com Pydantic."), ("Sem rota de saúde.", "Plataformas de deploy usam <code>/saude</code> (ou <code>/health</code>) para saber se o serviço está vivo.")]),
        ponte("Do notebook ao produto", "<p>Com FastAPI + Docker, seu modelo vira um serviço que qualquer aplicação chama. É a peça central do portfólio de quem quer trabalhar com IA aplicada.</p>"),
        quiz([
            ("Qual código HTTP o FastAPI devolve quando a validação falha?", ["200.", "422.", "301."], 1, "Unprocessable Entity."),
            ("Onde ver a documentação automática?", ["Em <code>/docs</code>.", "No terminal.", "Não existe."], 0, "Swagger UI."),
            ("Para enviar dados para previsão, usa-se em geral:", ["GET.", "POST.", "DELETE."], 1, "Corpo em JSON."),
        ]),
    ],
    ["Rotas com decoradores; corpo validado por Pydantic.", "Carregue o modelo uma vez.", "/docs para testar; /saude para monitorar."],
    "Deploy em nuvem.",
    livro=("FASTAPI:tutorial/first-steps", "Documentação do FastAPI, “Primeiros Passos”", "O que o uvicorn faz e como abrir a documentação interativa?"))

AULAS["Deploy em nuvem (AWS, GCP ou Azure)"] = aula(
    30,
    "Deploy é colocar sua aplicação num servidor acessível pela internet, 24 horas por dia. As três grandes nuvens oferecem dezenas de serviços, mas para começar você precisa de poucos: um lugar para rodar o contêiner, um para guardar arquivos e um para os segredos.",
    ["conhecer os modelos de serviço (VM, contêiner gerenciado, serverless);", "fazer o deploy de um contêiner;", "controlar custos e segredos."],
    ["Docker e FastAPI."],
    [
        chute("Para uma API com tráfego baixo e irregular, qual opção costuma ser mais barata?", ["Uma máquina virtual grande ligada o tempo todo.", "Um serviço de contêiner que escala até zero (Cloud Run, App Runner, Container Apps).", "Um cluster Kubernetes."], 1,
              ["Você paga mesmo sem uso.", "Isso! Você paga pelo uso; sem requisições, quase nada.", "Complexo e caro para começar."],
              "Comece simples; complexidade só quando precisar."),
        concreto("Alugar, não construir", "<p>Você pode construir uma casa (servidor próprio), alugar um apartamento (máquina virtual) ou ficar num hotel e pagar por noite (serverless). Para quem está começando, o hotel é o mais prático: alguém cuida da manutenção.</p>"),
        tabela("Os serviços equivalentes", ["Necessidade", "AWS", "GCP", "Azure"], [
            ["Rodar contêiner gerenciado", "App Runner / ECS Fargate", "Cloud Run", "Container Apps"],
            ["Máquina virtual", "EC2", "Compute Engine", "Virtual Machines"],
            ["Guardar arquivos (modelos, dados)", "S3", "Cloud Storage", "Blob Storage"],
            ["Segredos", "Secrets Manager", "Secret Manager", "Key Vault"],
            ["Funções serverless", "Lambda", "Cloud Functions", "Functions"],
        ], rot="Organize na cabeça"),
        passos("Deploy de um contêiner (exemplo no Cloud Run)", [
            ("Crie a conta e <b>configure um alerta de orçamento</b>.", "O primeiro passo, antes de qualquer serviço."),
            ("Construa a imagem e envie para o registro.", "<code>gcloud builds submit --tag ...</code>"),
            ("Crie o serviço apontando para a imagem.", "<code>gcloud run deploy minha-api --image ... --region southamerica-east1</code>"),
            ("Configure variáveis de ambiente e segredos.", "Nunca dentro da imagem."),
            ("Teste a URL pública e a rota <code>/saude</code>.", "Veja os logs no console."),
        ]),
        cod("Quanto vai custar?", "Compare o custo mensal de uma VM ligada 24h (preço por hora) com um serviço por uso (preço por milhão de requisições + preço por segundo de CPU). Devolva a opção mais barata para o volume dado.",
            '''
def custo_vm(preco_hora):
    return 0.0

def custo_serverless(req_mes, seg_por_req, preco_milhao_req=0.40, preco_seg_cpu=0.000024):
    return 0.0

def mais_barato(req_mes, seg_por_req, preco_hora_vm):
    return "vm"

print(mais_barato(100_000, 0.2, 0.05), mais_barato(50_000_000, 0.2, 0.05))
''',
            [("VM", "assert abs(custo_vm(0.05) - 0.05 * 24 * 30) < 1e-9"),
             ("Serverless", "assert abs(custo_serverless(1_000_000, 0.5) - (0.40 + 1_000_000 * 0.5 * 0.000024)) < 1e-9"),
             ("Escolha pelo volume", "assert mais_barato(100_000, 0.2, 0.05) == 'serverless' and mais_barato(50_000_000, 0.2, 0.05) == 'vm'")],
            '''
def custo_vm(preco_hora):
    return preco_hora * 24 * 30

def custo_serverless(req_mes, seg_por_req, preco_milhao_req=0.40, preco_seg_cpu=0.000024):
    return req_mes / 1e6 * preco_milhao_req + req_mes * seg_por_req * preco_seg_cpu

def mais_barato(req_mes, seg_por_req, preco_hora_vm):
    return "serverless" if custo_serverless(req_mes, seg_por_req) < custo_vm(preco_hora_vm) else "vm"

print(mais_barato(100_000, 0.2, 0.05), mais_barato(50_000_000, 0.2, 0.05))
''', ["VM: preço por hora × 24 × 30.", "Serverless: parte por requisição + parte por segundo de CPU."],
            exp="<p>Os preços são ilustrativos; confira a calculadora oficial do provedor. A lição vale sempre: pouco tráfego favorece pagar por uso; muito tráfego constante favorece máquinas reservadas.</p>"),
        erros([("Não configurar alerta de orçamento.", "Faça isso no primeiro dia: erros de configuração geram contas altas."), ("Chaves de acesso no GitHub.", "Robôs varrem repositórios públicos em minutos; use segredos e permissões mínimas."), ("Escolher a região mais distante.", "Para usuários no Brasil, regiões de São Paulo reduzem a latência.")]),
        ponte("Uma nuvem basta", "<p>Escolha uma nuvem e aprenda bem o básico (contêiner, armazenamento, segredos, logs, permissões). Os conceitos se transferem para as outras. Todas têm camadas gratuitas para estudar.</p>"),
        quiz([
            ("Qual a primeira coisa a configurar numa conta de nuvem?", ["Kubernetes.", "Alerta de orçamento.", "Um banco de dados."], 1, "Evita sustos."),
            ("Serviços que escalam até zero são bons para:", ["Tráfego baixo ou irregular.", "Tráfego altíssimo e constante sempre.", "Nada."], 0, "Pague pelo uso."),
            ("Onde guardar o arquivo do modelo treinado?", ["No armazenamento de objetos (S3, Cloud Storage, Blob).", "No e-mail.", "No código-fonte."], 0, "Arquivos grandes."),
        ]),
    ],
    ["Comece com contêiner gerenciado; VM e Kubernetes quando precisar.", "Alerta de orçamento e segredos fora do código.", "Os conceitos se transferem entre AWS, GCP e Azure."],
    "Testes e boas práticas de código.",
    livro=("FASTAPI:deployment", "Documentação do FastAPI, “Implantação”", "Que conceitos de deploy a documentação explica (HTTPS, réplicas, reinício)?"))

AULAS["Testes e boas práticas de código"] = aula(
    30,
    "Código de ciência de dados tem fama de bagunçado: notebooks gigantes, funções de 300 linhas, nada testado. Em produção, isso vira bugs silenciosos que entregam previsões erradas. Testes, funções pequenas e ferramentas de qualidade são o que faz seu código ser confiável e fácil de mudar.",
    ["testar funções de dados e de modelos;", "organizar o projeto em módulos;", "usar formatador, linter e tipagem."],
    ["pytest, PEP 8, docstrings e funções."],
    [
        chute("O que testar num pipeline de ML?", ["Só a acurácia final.", "Funções de transformação, formatos de entrada e saída, e comportamentos esperados do modelo.", "Nada, modelos são aleatórios."], 1,
              ["Acurácia não pega bugs de pré-processamento.", "Isso! Teste unidades (limpeza, features) e propriedades do modelo (formato da saída, invariâncias).", "Fixe sementes e teste propriedades."],
              "Teste o código e o comportamento, não só a métrica."),
        concreto("O checklist do piloto", "<p>Pilotos experientes ainda usam checklist antes de decolar. Não porque esquecem, mas porque um erro custa caro. Testes automatizados são o checklist do seu código: rodam toda vez, sem preguiça.</p>"),
        tabela("Testes em projetos de ML", ["Tipo", "Exemplo"], [
            ["Unidade", "a função de limpeza remove nulos e mantém as colunas"],
            ["Dados", "nenhuma idade negativa; colunas esperadas presentes"],
            ["Modelo: formato", "a saída tem uma probabilidade por linha, entre 0 e 1"],
            ["Modelo: invariância", "trocar o nome da pessoa não muda a previsão de crédito"],
            ["Modelo: direção", "mais área não deve diminuir o preço previsto"],
            ["Integração", "a API recebe JSON e devolve a previsão"],
        ], rot="Organize na cabeça"),
        cod("Testes de comportamento", "Complete os testes do modelo de preço de imóveis: (1) mais área nunca diminui o preço; (2) a saída é sempre positiva; (3) o bairro escrito em maiúsculas ou minúsculas dá o mesmo preço. Cada teste deve devolver True ou False.",
            '''
def modelo(area, bairro):
    base = {"centro": 8000, "praia": 10000}.get(bairro.lower(), 5000)
    return 20000 + area * base

def teste_direcao():
    return None

def teste_positivo():
    return None

def teste_invariancia():
    return None

print(teste_direcao(), teste_positivo(), teste_invariancia())
''',
            [("Direção", "assert teste_direcao() is True"), ("Positivo", "assert teste_positivo() is True"), ("Invariância", "assert teste_invariancia() is True"),
             ("Os testes pegam um modelo errado", "def modelo(area, bairro):\n    return 100000 - area * ({'centro': 8000}.get(bairro, 5000))\nassert teste_direcao() is False and teste_invariancia() is False")],
            '''
def modelo(area, bairro):
    base = {"centro": 8000, "praia": 10000}.get(bairro.lower(), 5000)
    return 20000 + area * base

def teste_direcao():
    return all(modelo(a + 10, b) >= modelo(a, b) for a in range(10, 200, 10) for b in ["centro", "praia", "outro"])

def teste_positivo():
    return all(modelo(a, b) > 0 for a in range(1, 300, 7) for b in ["centro", "praia", "outro"])

def teste_invariancia():
    return all(modelo(80, b) == modelo(80, b.upper()) for b in ["centro", "praia", "outro"])

print(teste_direcao(), teste_positivo(), teste_invariancia())
''', ["Use <code>all(...)</code> sobre várias áreas e bairros.", "Invariância: compare <code>modelo(80, b)</code> com <code>modelo(80, b.upper())</code>."]),
        nota("Ferramentas de qualidade", [
            ("<code>ruff</code>", "linter e formatador", "Rápido; substitui flake8, isort e black."),
            ("Dicas de tipo + <code>mypy</code>", "tipagem", "Pega erros antes de rodar."),
            ("<code>pre-commit</code>", "ganchos de commit", "Roda as ferramentas automaticamente."),
            ("<code>src/</code> + <code>tests/</code>", "estrutura", "Código reutilizável fora dos notebooks."),
        ]),
        erros([("Lógica importante só no notebook.", "Mova para funções em módulos e importe no notebook."), ("Testes que dependem de dados enormes.", "Use pequenas amostras fixas (fixtures)."), ("Corrigir um bug sem escrever um teste.", "Escreva o teste que falha, corrija, e o bug não volta.")]),
        ponte("A base do CI/CD", "<p>Com testes e ferramentas de qualidade, dá para automatizar: a cada push, o GitHub Actions roda tudo e só deixa publicar se passar. É a aula de CI/CD, logo adiante.</p>"),
        quiz([
            ("Um teste de invariância verifica que:", ["Mudanças irrelevantes não alteram a previsão.", "O modelo é rápido.", "A acurácia é alta."], 0, "Robustez."),
            ("Onde deve ficar a lógica reutilizável?", ["Em módulos Python testáveis.", "Só no notebook.", "Em comentários."], 0, "src/."),
            ("O que o ruff faz?", ["Lint e formatação.", "Treina modelos.", "Faz deploy."], 0, "Qualidade."),
        ]),
    ],
    ["Teste unidades, dados e comportamento do modelo.", "Código em módulos, notebooks só para explorar.", "ruff, tipos e pre-commit automatizam a qualidade."],
    "Versionamento de dados e modelos.",
    livro=("MADEML:testing", "Made With ML, seção “Testing”", "Que tipos de testes de modelo o curso propõe?"))

AULAS["Versionamento de dados e modelos"] = aula(
    25,
    "O Git guarda seu código, mas não lida bem com um CSV de 5 GB ou um modelo de 2 GB. E sem saber <b>qual versão dos dados</b> treinou <b>qual modelo</b>, é impossível reproduzir um resultado ou descobrir por que a versão nova piorou.",
    ["entender por que versionar dados e modelos;", "usar hashes para identificar versões;", "conhecer DVC e registros de modelos."],
    ["Git, GitHub e notebooks reprodutíveis."],
    [
        chute("O modelo em produção piorou. O que você precisa para investigar?", ["Só o código atual.", "Saber exatamente quais dados, código e parâmetros geraram cada versão do modelo.", "Treinar de novo e torcer."], 1,
              ["O código pode não ter mudado; os dados sim.", "Isso! Com essa linhagem, você compara as versões e acha o que mudou.", "Sem saber o que mudou, o problema volta."],
              "Modelo = código + dados + parâmetros."),
        concreto("A receita com ingredientes de lote", "<p>Uma fábrica de alimentos registra o lote de cada ingrediente usado em cada fornada. Se uma fornada sai ruim, ela sabe qual lote de farinha investigar. Versionar dados é registrar os lotes dos seus modelos.</p>"),
        nota("As ferramentas", [
            ("Hash (SHA-256)", "impressão digital", "Muda se um único byte do arquivo mudar."),
            ("DVC", "Git para dados", "Guarda os arquivos num armazenamento e só um ponteiro no Git."),
            ("Registro de modelos", "catálogo", "Versões, métricas e estágio (teste, produção) — MLflow, W&amp;B, Hugging Face."),
            ("Linhagem", "de onde veio", "Commit do código + versão dos dados + parâmetros → modelo."),
        ]),
        texto("DVC em quatro comandos", sh('''
dvc init
dvc add dados/vendas.csv        # cria dados/vendas.csv.dvc (o ponteiro)
git add dados/vendas.csv.dvc .gitignore
dvc push                        # envia o arquivo para o armazenamento remoto
'''), rot="Mão na massa"),
        cod("Impressão digital dos dados", "Escreva <code>versao(conteudo)</code> que devolve os 12 primeiros caracteres do SHA-256 de uma string, e <code>registrar(registro, nome_modelo, dados, params)</code> que guarda no dicionário a versão dos dados e os parâmetros. <code>mudou(registro, a, b)</code> diz o que mudou entre dois modelos: <code>\"dados\"</code>, <code>\"params\"</code>, ambos ou nada.",
            '''
import hashlib

def versao(conteudo):
    return ""

def registrar(registro, nome_modelo, dados, params):
    pass

def mudou(registro, a, b):
    return []

reg = {}
registrar(reg, "v1", "idade,renda\\n30,5000", {"profundidade": 3})
registrar(reg, "v2", "idade,renda\\n30,5000\\n41,7000", {"profundidade": 3})
print(mudou(reg, "v1", "v2"))
''',
            [("Hash estável", "assert versao('abc') == 'ba7816bf8f01' and len(versao('x')) == 12"),
             ("Detecta dados", "assert mudou(reg, 'v1', 'v2') == ['dados'], f'{mudou(reg, \"v1\", \"v2\")}'"),
             ("Detecta parâmetros", "registrar(reg, 'v3', 'idade,renda\\n30,5000\\n41,7000', {'profundidade': 5})\nassert mudou(reg, 'v2', 'v3') == ['params'] and mudou(reg, 'v1', 'v3') == ['dados', 'params']")],
            '''
import hashlib

def versao(conteudo):
    return hashlib.sha256(conteudo.encode("utf-8")).hexdigest()[:12]

def registrar(registro, nome_modelo, dados, params):
    registro[nome_modelo] = {"dados": versao(dados), "params": dict(params)}

def mudou(registro, a, b):
    return [campo for campo in ("dados", "params") if registro[a][campo] != registro[b][campo]]

reg = {}
registrar(reg, "v1", "idade,renda\\n30,5000", {"profundidade": 3})
registrar(reg, "v2", "idade,renda\\n30,5000\\n41,7000", {"profundidade": 3})
print(mudou(reg, "v1", "v2"))
''', ["<code>hashlib.sha256(texto.encode()).hexdigest()[:12]</code>.", "Compare os campos <code>dados</code> e <code>params</code> dos dois registros."]),
        erros([("Commitar arquivos grandes no Git.", "O repositório fica pesado para sempre; use DVC ou Git LFS."), ("Nomes como <code>modelo_final_v2_agora_vai.pkl</code>.", "Use um registro com versões e metadados."), ("Dados com informações pessoais versionados sem cuidado.", "Respeite a LGPD: acesso restrito e anonimização.")]),
        ponte("Reprodutibilidade", "<p>Com código no Git, dados no DVC e experimentos registrados (próxima aula: MLflow e W&amp;B), qualquer pessoa da equipe recria um modelo antigo exatamente. Isso é MLOps na prática.</p>"),
        quiz([
            ("Por que não colocar dados grandes no Git?", ["O Git não foi feito para arquivos grandes e o histórico fica pesado.", "É proibido.", "O Git apaga os dados."], 0, "Use DVC/LFS."),
            ("O que um hash identifica?", ["O conteúdo exato de um arquivo.", "O autor.", "A data."], 0, "Impressão digital."),
            ("O que é linhagem de um modelo?", ["Código, dados e parâmetros que o geraram.", "A família do autor.", "O tamanho."], 0, "De onde veio."),
        ]),
    ],
    ["Modelo = código + dados + parâmetros: versione os três.", "Hashes identificam versões de dados.", "DVC para dados; registro de modelos para modelos."],
    "MLflow ou Weights & Biases.",
    livro=("MADEML:versioning", "Made With ML, seção “Versioning”", "Como o curso versiona dados e modelos?"))

AULAS["MLflow ou Weights & Biases"] = aula(
    25,
    "Depois de 40 experimentos, ninguém lembra qual combinação de parâmetros deu aquele resultado bom de terça-feira. Ferramentas de rastreamento de experimentos registram automaticamente parâmetros, métricas, gráficos e modelos de cada execução, para comparar e reproduzir.",
    ["registrar parâmetros, métricas e artefatos;", "comparar execuções e escolher a melhor;", "promover um modelo no registro."],
    ["Hiperparâmetros, validação cruzada e versionamento."],
    [
        chute("Qual a vantagem de registrar todos os experimentos, até os ruins?", ["Nenhuma, só ocupa espaço.", "Saber o que já foi tentado, evitar repetir e entender o que funciona.", "Deixar o treino mais rápido."], 1,
              ["Os ruins também ensinam.", "Isso! Um histórico completo mostra tendências e evita refazer o que falhou.", "Não muda a velocidade."],
              "Experimento não registrado é experimento perdido."),
        concreto("O caderno de laboratório", "<p>Cientistas anotam cada experimento: condições, resultado, data. Sem o caderno, não dá para publicar nem repetir. MLflow e W&amp;B são o caderno de laboratório automático do cientista de dados.</p>"),
        tabela("MLflow × Weights & Biases", ["", "MLflow", "Weights & Biases"], [
            ["Licença", "código aberto, roda no seu servidor", "serviço (grátis para uso pessoal)"],
            ["Forte em", "registro de modelos, deploy", "visualização, colaboração, relatórios"],
            ["Comece com", "<code>mlflow ui</code> local", "<code>wandb login</code>"],
        ], rot="Organize na cabeça"),
        lab("Rastreando com MLflow", '''
import mlflow
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

X, y = load_diabetes(return_X_y=True)
mlflow.set_experiment("diabetes")
for prof in [2, 4, 8]:
    with mlflow.start_run(run_name=f"rf-prof-{prof}"):
        modelo = RandomForestRegressor(max_depth=prof, random_state=0)
        r2 = cross_val_score(modelo, X, y, cv=5, scoring="r2").mean()
        mlflow.log_param("max_depth", prof)
        mlflow.log_metric("r2_cv", r2)
        mlflow.sklearn.log_model(modelo.fit(X, y), "modelo")
''', corpo="<p>Rode e depois abra <code>mlflow ui</code> no navegador:</p>", exps=["Compare as três execuções lado a lado na interface.", "Registre o melhor modelo e mude seu estágio para produção."]),
        cod("Um rastreador de experimentos", "Implemente um mini MLflow: <code>log(execucao, params, metricas)</code> guarda em <code>EXECUCOES</code>; <code>melhor(metrica, maior=True)</code> devolve o nome da melhor execução; <code>comparar(param)</code> devolve a métrica média para cada valor do parâmetro.",
            '''
EXECUCOES = []

def log(execucao, params, metricas):
    pass

def melhor(metrica, maior=True):
    return None

def comparar(param, metrica):
    return {}

log("a", {"lr": 0.1, "prof": 3}, {"r2": 0.41})
log("b", {"lr": 0.01, "prof": 3}, {"r2": 0.47})
log("c", {"lr": 0.01, "prof": 6}, {"r2": 0.44})
print(melhor("r2"), comparar("lr", "r2"))
''',
            [("Melhor execução", "assert melhor('r2') == 'b' and melhor('r2', maior=False) == 'a'"),
             ("Comparação por parâmetro", "c = comparar('lr', 'r2')\nassert abs(c[0.1] - 0.41) < 1e-9 and abs(c[0.01] - 0.455) < 1e-9, f'{c}'")],
            '''
EXECUCOES = []

def log(execucao, params, metricas):
    EXECUCOES.append({"nome": execucao, "params": params, "metricas": metricas})

def melhor(metrica, maior=True):
    escolha = max if maior else min
    return escolha(EXECUCOES, key=lambda e: e["metricas"][metrica])["nome"]

def comparar(param, metrica):
    grupos = {}
    for e in EXECUCOES:
        grupos.setdefault(e["params"][param], []).append(e["metricas"][metrica])
    return {v: sum(m) / len(m) for v, m in grupos.items()}

log("a", {"lr": 0.1, "prof": 3}, {"r2": 0.41})
log("b", {"lr": 0.01, "prof": 3}, {"r2": 0.47})
log("c", {"lr": 0.01, "prof": 6}, {"r2": 0.44})
print(melhor("r2"), comparar("lr", "r2"))
''', ["<code>max</code> ou <code>min</code> com <code>key</code> na métrica.", "Agrupe por valor do parâmetro com <code>setdefault</code>."]),
        erros([("Registrar só a métrica final.", "Registre parâmetros, versão dos dados, commit do código e artefatos."), ("Comparar execuções com dados diferentes.", "Registre a versão dos dados para comparar de forma justa."), ("Escolher pelo melhor resultado na validação muitas vezes.", "Depois de muitos experimentos, confirme no conjunto de teste guardado.")]),
        ponte("No seu portfólio", "<p>Um projeto com experimentos rastreados e um relatório comparando abordagens mostra maturidade. Recrutadores de MLOps procuram exatamente isso.</p>"),
        quiz([
            ("O que o MLflow registra?", ["Parâmetros, métricas e artefatos de cada execução.", "Só o código.", "Senhas."], 0, "O caderno."),
            ("Para que serve um registro de modelos?", ["Guardar versões e estágios (teste, produção).", "Treinar mais rápido.", "Desenhar gráficos."], 0, "Catálogo."),
            ("Por que registrar experimentos ruins?", ["Para saber o que já foi tentado.", "Não deve.", "Para ocupar espaço."], 0, "Aprendizado."),
        ]),
    ],
    ["Registre parâmetros, métricas, artefatos e versões.", "Compare execuções e promova o melhor modelo.", "MLflow (aberto) ou W&amp;B (visual e colaborativo)."],
    "Monitoramento de modelos.",
    livro=("MADEML:experiment-tracking", "Made With ML, seção “Experiment tracking”", "Que informações o curso registra em cada execução?"))

AULAS["Monitoramento de modelos"] = aula(
    30,
    "Um modelo em produção envelhece. Os clientes mudam, a economia muda, um campo do formulário muda de formato, e a acurácia cai sem ninguém perceber. Monitorar é vigiar entradas, saídas e resultados para detectar esse desvio antes que ele cause prejuízo.",
    ["diferenciar desvio de dados e de conceito;", "calcular o PSI para comparar distribuições;", "montar alertas com métricas técnicas e de negócio."],
    ["Métricas, histogramas e deploy."],
    [
        chute("O modelo de crédito foi treinado em 2023. Em 2025 a renda média dos clientes subiu 30%. O que é isso?", ["Overfitting.", "Desvio de dados (data drift): a distribuição das entradas mudou.", "Um bug."], 1,
              ["Overfitting é no treino.", "Isso! As entradas de produção não se parecem mais com as do treino.", "Pode não ser bug: o mundo mudou."],
              "Data drift: X mudou. Concept drift: a relação entre X e y mudou."),
        concreto("O GPS desatualizado", "<p>Um GPS com mapa de 5 anos atrás funciona quase sempre, até mandar você por uma rua que virou calçadão. O modelo é o mapa; monitoramento é perceber que as ruas mudaram e atualizar o mapa.</p>"),
        nota("O que vigiar", [
            ("Desvio de dados", "entradas mudaram", "Compare distribuições de produção com as do treino."),
            ("Desvio de conceito", "a relação mudou", "Mesmo cliente, comportamento diferente (ex.: pandemia)."),
            (r"$PSI = \sum (p_i - q_i)\ln\frac{p_i}{q_i}$", "índice de estabilidade", "Abaixo de 0,1: estável; 0,1 a 0,25: atenção; acima de 0,25: mudança forte."),
            ("Métricas de serviço", "latência, erros, volume", "O modelo está respondendo?"),
            ("Métricas de negócio", "inadimplência, conversão", "O modelo ainda ajuda?"),
        ], rot="Agora sim, as métricas"),
        cod("Calculando o PSI", "Implemente <code>psi(treino, producao, faixas)</code>: conte a proporção de valores em cada faixa (limites dados) nos dois conjuntos, troque proporções zero por 0,0001 e some (p − q)·ln(p/q). Depois classifique com <code>alerta(valor)</code>.",
            '''
import math

def proporcoes(valores, faixas):
    contagem = [0] * (len(faixas) - 1)
    for v in valores:
        for i in range(len(faixas) - 1):
            if faixas[i] <= v < faixas[i + 1]:
                contagem[i] += 1
                break
    return [max(c / len(valores), 0.0001) for c in contagem]

def psi(treino, producao, faixas):
    return 0.0

def alerta(valor):
    return "estável"

faixas = [0, 2000, 4000, 6000, 8000, 100000]
treino = [1500, 2500, 3000, 3500, 4500, 5000, 5500, 6500, 7000, 9000]
igual = [1600, 2600, 3100, 3600, 4600, 5100, 5600, 6600, 7100, 9100]
mudou = [5000, 6100, 6500, 7000, 7200, 7500, 8500, 9000, 9500, 12000]
print(round(psi(treino, igual, faixas), 3), round(psi(treino, mudou, faixas), 3))
''',
            [("Sem mudança", "assert psi(treino, igual, faixas) < 0.01"),
             ("Mudança forte", "assert psi(treino, mudou, faixas) > 0.25, f'{psi(treino, mudou, faixas)}'"),
             ("Alertas", "assert [alerta(0.05), alerta(0.2), alerta(0.4)] == ['estável', 'atenção', 'mudança forte']")],
            '''
import math

def proporcoes(valores, faixas):
    contagem = [0] * (len(faixas) - 1)
    for v in valores:
        for i in range(len(faixas) - 1):
            if faixas[i] <= v < faixas[i + 1]:
                contagem[i] += 1
                break
    return [max(c / len(valores), 0.0001) for c in contagem]

def psi(treino, producao, faixas):
    q, p = proporcoes(treino, faixas), proporcoes(producao, faixas)
    return sum((pi - qi) * math.log(pi / qi) for pi, qi in zip(p, q))

def alerta(valor):
    if valor < 0.1:
        return "estável"
    return "atenção" if valor <= 0.25 else "mudança forte"

faixas = [0, 2000, 4000, 6000, 8000, 100000]
treino = [1500, 2500, 3000, 3500, 4500, 5000, 5500, 6500, 7000, 9000]
igual = [1600, 2600, 3100, 3600, 4600, 5100, 5600, 6600, 7100, 9100]
mudou = [5000, 6100, 6500, 7000, 7200, 7500, 8500, 9000, 9500, 12000]
print(round(psi(treino, igual, faixas), 3), round(psi(treino, mudou, faixas), 3))
''', ["Use a função <code>proporcoes</code> nos dois conjuntos.", "Some <code>(p - q) * math.log(p / q)</code> faixa a faixa."]),
        erros([("Monitorar só se o servidor está no ar.", "O serviço pode responder perfeitamente com previsões cada vez piores."), ("Esperar o rótulo verdadeiro para agir.", "Às vezes ele demora meses (inadimplência); vigie o desvio das entradas enquanto isso."), ("Alertas demais.", "Se tudo dispara, ninguém olha; ajuste os limites.")]),
        ponte("Fechando o ciclo", "<p>Monitoramento alimenta o retreino: quando o desvio passa do limite, um pipeline treina com dados novos, avalia e, se for melhor, publica. Ferramentas como Evidently e os serviços de nuvem automatizam parte disso.</p>"),
        quiz([
            ("O que é data drift?", ["A distribuição das entradas mudou.", "O servidor caiu.", "O modelo ficou maior."], 0, "X mudou."),
            ("PSI acima de 0,25 indica:", ["Estabilidade.", "Mudança forte na distribuição.", "Erro de cálculo."], 1, "Investigue."),
            ("Por que vigiar métricas de negócio?", ["Para saber se o modelo ainda gera valor.", "Por obrigação legal sempre.", "Não precisa."], 0, "Impacto real."),
        ]),
    ],
    ["Modelos envelhecem: vigie entradas, saídas e resultados.", "PSI compara distribuições do treino e da produção.", "Alertas com métricas técnicas e de negócio."],
    "Linux e shell avançado.",
    livro=("MADEML:monitoring", "Made With ML, seção “Monitoring”", "Que tipos de desvio o curso descreve e como medi-los?"))

AULAS["Linux e shell avançado"] = aula(
    30,
    "Servidores, contêineres e GPUs na nuvem rodam Linux, e muitas vezes você só tem um terminal. Saber navegar, filtrar arquivos enormes, encadear comandos e automatizar com scripts faz você resolver em um minuto o que levaria uma hora com cliques.",
    ["encadear comandos com pipes;", "filtrar e contar com grep, cut, sort, uniq;", "acompanhar processos, uso de disco e logs."],
    ["Linha de comando básica (Fase 1)."],
    [
        chute("O que faz <code>cat acessos.log | grep \" 500 \" | wc -l</code>?", ["Apaga o log.", "Conta as linhas do log que contêm “ 500 ” (erros do servidor).", "Mostra as 500 primeiras linhas."], 1,
              ["Nada é apagado.", "Isso! O pipe passa a saída de um comando como entrada do próximo.", "Isso seria <code>head -n 500</code>."],
              "Pipes: pequenos comandos combinados em algo poderoso."),
        concreto("A linha de montagem", "<p>Cada comando do Linux faz uma coisa bem feita: um filtra, outro corta colunas, outro ordena, outro conta. O pipe (<code>|</code>) é a esteira que leva o produto de uma estação para a próxima.</p>"),
        texto("Comandos que você vai usar todo dia", sh('''
grep -i "erro" app.log | tail -20          # últimos 20 erros
cut -d, -f3 vendas.csv | sort | uniq -c | sort -rn | head   # valores mais comuns da coluna 3
find . -name "*.parquet" -size +100M       # arquivos grandes
du -sh * | sort -h                         # o que ocupa espaço
htop                                       # processos e memória
nvidia-smi                                 # uso da GPU
tail -f app.log                            # acompanhar o log ao vivo
nohup python treino.py > treino.log 2>&1 & # treino que continua após sair
'''), rot="Mão na massa"),
        cod("Um pipe em Python", "Reproduza em Python o pipe <code>cut -d, -f2 | sort | uniq -c | sort -rn | head -2</code>: a partir das linhas CSV, pegue a 2ª coluna, conte cada valor e devolva os 2 mais frequentes como (contagem, valor), do maior para o menor.",
            '''
linhas = [
    "2025-01-01,SP,120",
    "2025-01-01,RJ,80",
    "2025-01-02,SP,90",
    "2025-01-02,PE,60",
    "2025-01-03,SP,30",
    "2025-01-03,RJ,10",
]

def top(linhas, coluna, n):
    return []

print(top(linhas, 2, 2))
''',
            [("Mais frequentes", "assert top(linhas, 2, 2) == [(3, 'SP'), (2, 'RJ')], f'{top(linhas, 2, 2)}'"),
             ("Outra coluna", "assert top(linhas, 1, 1) == [(2, '2025-01-03')] or top(linhas, 1, 1)[0][0] == 2")],
            '''
from collections import Counter

linhas = [
    "2025-01-01,SP,120",
    "2025-01-01,RJ,80",
    "2025-01-02,SP,90",
    "2025-01-02,PE,60",
    "2025-01-03,SP,30",
    "2025-01-03,RJ,10",
]

def top(linhas, coluna, n):
    valores = [l.split(",")[coluna - 1] for l in linhas]
    return [(c, v) for v, c in Counter(valores).most_common(n)]

print(top(linhas, 2, 2))
''', ["Colunas do <code>cut</code> começam em 1: use <code>coluna - 1</code>.", "<code>Counter(...).most_common(n)</code> faz o <code>sort | uniq -c | sort -rn | head</code>."]),
        erros([("Rodar treinos longos direto no SSH.", "Se a conexão cair, o processo morre; use <code>tmux</code>, <code>screen</code> ou <code>nohup</code>."), ("<code>rm -rf</code> com caminho errado.", "Confira com <code>ls</code> antes; não há lixeira."), ("Abrir arquivos de 10 GB num editor.", "Use <code>head</code>, <code>tail</code>, <code>grep</code> e <code>less</code>.")]),
        ponte("Automatize", "<p>Quando repetir a mesma sequência de comandos pela terceira vez, coloque num script <code>.sh</code> ou num <code>Makefile</code>. O curso “Missing Semester” do MIT é a melhor referência gratuita para dominar o terminal.</p>"),
        quiz([
            ("O que o pipe <code>|</code> faz?", ["Passa a saída de um comando para o próximo.", "Apaga arquivos.", "Cria pastas."], 0, "Esteira."),
            ("Para acompanhar um log em tempo real:", ["<code>tail -f</code>.", "<code>rm</code>.", "<code>cd</code>."], 0, "Follow."),
            ("Como manter um treino rodando depois de sair do SSH?", ["tmux, screen ou nohup.", "Fechar o terminal rápido.", "Não é possível."], 0, "Sessão persistente."),
        ]),
    ],
    ["Pipes combinam comandos simples.", "grep, cut, sort, uniq, head, tail para dados e logs.", "tmux/nohup para processos longos; scripts para repetir."],
    "CI/CD com GitHub Actions.",
    livro=("MISSING:shell-tools", "Missing Semester, aula “Shell Tools and Scripting”", "Que ferramentas de busca a aula apresenta?"))

AULAS["CI/CD com GitHub Actions"] = aula(
    25,
    "Toda vez que alguém envia código, uma série de passos deveria acontecer: instalar dependências, rodar testes, checar estilo, construir a imagem e publicar. Fazer isso à mão é lento e esquecível. CI/CD automatiza: o GitHub Actions roda tudo a cada push.",
    ["entender integração contínua (CI) e entrega contínua (CD);", "escrever um workflow do GitHub Actions;", "usar segredos e condições com segurança."],
    ["Git, GitHub, pytest e Docker."],
    [
        chute("Um colega abre um pull request que quebra os testes. Com CI configurado, o que acontece?", ["Nada, o código entra assim mesmo.", "O workflow falha, o PR fica marcado em vermelho e pode ser bloqueado até corrigir.", "O GitHub apaga o PR."], 1,
              ["É o que acontece sem CI.", "Isso! O problema é pego antes de chegar à branch principal.", "Ninguém apaga nada."],
              "CI = rede de segurança automática."),
        concreto("A inspeção na linha de produção", "<p>Numa fábrica moderna, cada peça passa por inspeção automática antes de seguir. Peça com defeito volta. O CI é essa inspeção para cada mudança de código; o CD é a esteira que leva as peças aprovadas até a loja.</p>"),
        texto("Um workflow para um projeto Python", sh('''
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  testes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: ruff check .
      - run: pytest -q
'''), rot="Mão na massa"),
        nota("As peças", [
            ("<code>on</code>", "gatilhos", "push, pull_request, agendamento (<code>schedule</code>), manual."),
            ("<code>jobs</code> e <code>steps</code>", "trabalhos e passos", "Jobs rodam em paralelo; passos em sequência."),
            ("<code>uses</code>", "ações prontas", "Reaproveite ações da comunidade (fixe a versão)."),
            ("<code>secrets</code>", "segredos", "Chaves de nuvem guardadas nas configurações do repositório."),
            ("<code>if</code>", "condições", "Ex.: só publicar quando for a branch main."),
        ]),
        cod("Simulando um pipeline", "Escreva <code>rodar_pipeline(passos, evento, branch)</code>: execute os passos em ordem (cada um é uma função que devolve True/False); pare no primeiro que falhar. Passos marcados com <code>so_main=True</code> só rodam em push para a <code>main</code>. Devolva a lista de nomes executados e o status final.",
            '''
def rodar_pipeline(passos, evento, branch):
    return [], "sucesso"

passos = [
    {"nome": "instalar", "f": lambda: True},
    {"nome": "lint", "f": lambda: True},
    {"nome": "testes", "f": lambda: True},
    {"nome": "deploy", "f": lambda: True, "so_main": True},
]
print(rodar_pipeline(passos, "pull_request", "feature"))
''',
            [("PR não faz deploy", "assert rodar_pipeline(passos, 'pull_request', 'feature') == (['instalar', 'lint', 'testes'], 'sucesso')"),
             ("Push na main faz deploy", "assert rodar_pipeline(passos, 'push', 'main') == (['instalar', 'lint', 'testes', 'deploy'], 'sucesso')"),
             ("Para na falha", "p2 = [dict(passos[0]), {'nome': 'lint', 'f': lambda: False}, dict(passos[2]), dict(passos[3])]\nassert rodar_pipeline(p2, 'push', 'main') == (['instalar', 'lint'], 'falhou em lint')")],
            '''
def rodar_pipeline(passos, evento, branch):
    executados = []
    for p in passos:
        if p.get("so_main") and not (evento == "push" and branch == "main"):
            continue
        executados.append(p["nome"])
        if not p["f"]():
            return executados, f"falhou em {p['nome']}"
    return executados, "sucesso"

passos = [
    {"nome": "instalar", "f": lambda: True},
    {"nome": "lint", "f": lambda: True},
    {"nome": "testes", "f": lambda: True},
    {"nome": "deploy", "f": lambda: True, "so_main": True},
]
print(rodar_pipeline(passos, "pull_request", "feature"))
''', ["Pule passos <code>so_main</code> quando não for push na main.", "Ao falhar, devolva imediatamente <code>f\"falhou em {nome}\"</code>."]),
        erros([("Segredos impressos nos logs.", "O GitHub mascara segredos registrados, mas não imprima variáveis sensíveis."), ("Ações de terceiros sem versão fixa.", "Fixe a versão (ou o commit) para evitar mudanças maliciosas."), ("CI lento demais.", "Use cache de dependências e rode testes pesados só quando necessário.")]),
        ponte("CI para ML", "<p>Em projetos de IA, o CI pode também rodar os evals do seu sistema com LLM, checar o desvio de dados ou retreinar num agendamento semanal. O mesmo arquivo YAML, com passos diferentes.</p>"),
        quiz([
            ("O que é CI?", ["Rodar testes e checagens automaticamente a cada mudança.", "Um tipo de banco.", "Escrever código sem testes."], 0, "Integração contínua."),
            ("Onde guardar a chave da nuvem para o deploy?", ["No YAML.", "Nos secrets do repositório.", "No README."], 1, "Segredos."),
            ("Como rodar o deploy só na main?", ["Com uma condição <code>if</code> ou gatilho por branch.", "Não é possível.", "Apagando outras branches."], 0, "Condições."),
        ]),
    ],
    ["CI roda testes e checagens a cada mudança; CD publica o que passou.", "Workflows em YAML: gatilhos, jobs, passos.", "Segredos nos secrets; ações com versão fixa."],
    "Kubernetes (noção).",
    livro=("PROGIT:x", "Pro Git (em português)", "Como o livro descreve o fluxo de branches e pull requests?"))
