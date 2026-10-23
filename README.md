# 🧠 Roteiro IA - Conexão com Banco de Dados Relacional (PostgreSQL / SQLite)

Este projeto conecta a página interativa do **Roteiro de Estudo (do zero à IA)** a uma estrutura local de banco de dados relacional com backend em **Python**.

---

## 📁 Estrutura de Arquivos

- **`schema.sql`**: Esquema DDL relacional em PostgreSQL (`users`, `phases`, `topic_groups`, `topics`, `progress` e a view `phase_progress`).
- **`seed.sql`**: Script DML com a inserção de todas as 7 fases e 209 tópicos do roteiro.
- **`server.py`**: Servidor web e API REST construído em Python. Conecta nativamente ao PostgreSQL (com suporte de fallback automático para SQLite local `roteiro.db`).
- **`docker-compose.yml`**: Configuração rápida para subir o PostgreSQL 16 com um único comando.
- **`requirements.txt`**: Dependências do Python (`psycopg2-binary`).
- **`.env`**: Configuração de conexão do banco de dados (host, porta, credenciais).
- **`index.html`** / **`Roteiro de Estudo_ do zero à IA.html`**: Interface web conectada à API REST.

---

## 🚀 Como Executar

### 1. Iniciar o Banco PostgreSQL

Você tem duas opções para o PostgreSQL:

#### Opção A: Usando Docker (Mais rápido e recomendado)
Basta rodar na pasta do projeto:
```bash
docker compose up -d
```
> O Docker irá baixar a imagem do PostgreSQL 16, criar o banco `roteiro_ia` e executar automaticamente os arquivos `schema.sql` e `seed.sql`.

#### Opção B: PostgreSQL já instalado na máquina
Se você já possui o PostgreSQL instalado localmente:
```bash
# Crie o banco de dados
createdb -U postgres roteiro_ia

# Execute os scripts de estrutura e dados
psql -U postgres -d roteiro_ia -f schema.sql
psql -U postgres -d roteiro_ia -f seed.sql
```

---

### 2. Instalar o Driver no Python

No seu terminal ou ambiente virtual:
```bash
pip install -r requirements.txt
```

---

### 3. Iniciar o Servidor Python

Inicie a aplicação com o comando:
```bash
python3 server.py
```

O terminal exibirá:
```
============================================================
🚀 Servidor Roteiro IA iniciado!
👉 Acesse no seu navegador: http://localhost:8000
📦 Banco de Dados em uso: POSTGRESQL
============================================================
```

> **Nota de contingência**: Se o PostgreSQL ainda não estiver rodando no momento em que você iniciar o servidor, ele ativará automaticamente o modo local **SQLite** (`roteiro.db`) para que você possa usar a página imediatamente sem travamentos.

---

## 🌐 Acessando a Página

Abra seu navegador no endereço:
👉 **[http://localhost:8000](http://localhost:8000)**

- O status no topo da página indicará `🐘 PostgreSQL Conectado`.
- Ao marcar tópicos como **Estudado**, **Revisar** ou **Do Zero**, ou adicionar anotações e datas, os dados são salvos em tempo real no banco.
- Se você já tinha anotações salvas anteriormente no navegador, clique no botão **☁️ Enviar dados locais ao Banco** para migrar tudo para o PostgreSQL com um único clique!

---

## 📊 Endpoints da API REST

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/status` | Retorna o status de conexão do banco e progresso geral |
| `GET` | `/api/phases` | Retorna todas as fases, grupos e tópicos estruturados |
| `GET` | `/api/progress?user_id=1` | Retorna o progresso e anotações do usuário |
| `POST` | `/api/progress` | Salva o status/anotação de um tópico específico |
| `POST` | `/api/progress/bulk` | Salva/sincroniza uma lista em lote de tópicos |
| `POST` | `/api/progress/clear` | Limpa o progresso do usuário no banco |
