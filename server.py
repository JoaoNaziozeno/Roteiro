#!/usr/bin/env python3
"""
Servidor Backend em Python para o Roteiro de Estudo: do zero à IA.
Suporta PostgreSQL (definido em schema.sql) e fallback local em SQLite.
"""

import os
import sys
import json
import sqlite3
import mimetypes
from urllib.parse import urlparse, parse_qs
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

# ---------------------------------------------------------------------------
# Carregar configurações do arquivo .env (sem dependências externas)
# ---------------------------------------------------------------------------
def load_env(filepath=".env"):
    config = {
        "DB_TYPE": "postgres",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_NAME": "roteiro_ia",
        "DB_USER": "postgres",
        "DB_PASSWORD": "postgres",
        "PORT": "8000",
        "FALLBACK_SQLITE": "true"
    }
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                config[k.strip()] = v.strip().strip("\"'")
    for k in config:
        if k in os.environ:
            config[k] = os.environ[k]
    return config

CONFIG = load_env()

# ---------------------------------------------------------------------------
# Camada de Banco de Dados: PostgreSQL com fallback SQLite
# ---------------------------------------------------------------------------
class Database:
    def __init__(self, config):
        self.config = config
        self.db_type = config.get("DB_TYPE", "postgres").lower()
        self.fallback_sqlite = config.get("FALLBACK_SQLITE", "true").lower() in ("true", "1", "yes")
        self.driver = None
        self.conn = None
        self.init_connection()

    def init_connection(self):
        if self.db_type == "postgres":
            # Tentar importar driver psycopg2 ou psycopg (v3)
            try:
                import psycopg2
                import psycopg2.extras
                self.driver = "psycopg2"
            except ImportError:
                try:
                    import psycopg
                    self.driver = "psycopg"
                except ImportError:
                    self.driver = None

            if not self.driver:
                print("\n[AVISO] Nenhum driver PostgreSQL instalado (psycopg2 ou psycopg).")
                print("Para instalar: pip install psycopg2-binary")
                if self.fallback_sqlite:
                    print("--> Ativando modo local SQLite temporariamente para funcionamento imediato.\n")
                    self.db_type = "sqlite"
                    self.init_sqlite()
                    return
                else:
                    raise RuntimeError("Driver PostgreSQL ausente.")

            # Tentar conectar ao PostgreSQL
            try:
                host = self.config.get("DB_HOST", "localhost")
                port = int(self.config.get("DB_PORT", 5432))
                dbname = self.config.get("DB_NAME", "roteiro_ia")
                user = self.config.get("DB_USER", "postgres")
                password = self.config.get("DB_PASSWORD", "postgres")

                print(f"[*] Tentando conexão com PostgreSQL em {host}:{port}/{dbname} (usuário: {user})...")
                if self.driver == "psycopg2":
                    import psycopg2
                    self.conn = psycopg2.connect(
                        host=host, port=port, dbname=dbname, user=user, password=password, connect_timeout=3
                    )
                    self.conn.autocommit = True
                else:
                    import psycopg
                    self.conn = psycopg.connect(
                        f"host={host} port={port} dbname={dbname} user={user} password={password}",
                        autocommit=True
                    )
                print("[OK] Conexão com PostgreSQL estabelecida com sucesso!")
                self.init_postgres_tables()
            except Exception as e:
                print(f"[!] Não foi possível conectar ao PostgreSQL: {e}")
                if self.fallback_sqlite:
                    print("--> Alternando para SQLite local (roteiro.db) para manter a aplicação online.\n")
                    self.db_type = "sqlite"
                    self.init_sqlite()
                else:
                    raise
        else:
            self.init_sqlite()

    def init_sqlite(self):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "roteiro.db")
        print(f"[*] Usando banco de dados SQLite local: {db_path}")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.init_sqlite_tables()
        print("[OK] Banco de dados SQLite pronto.")

    def get_cursor(self):
        if self.db_type == "postgres":
            if self.driver == "psycopg2":
                import psycopg2.extras
                return self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            else:
                import psycopg.rows
                return self.conn.cursor(row_factory=psycopg.rows.dict_row)
        else:
            return self.conn.cursor()

    def query(self, sql, params=None):
        cur = self.get_cursor()
        if self.db_type == "sqlite":
            sql = sql.replace("%s", "?")
        cur.execute(sql, params or ())
        return cur

    def execute_script(self, script_path):
        if not os.path.exists(script_path):
            return
        with open(script_path, "r", encoding="utf-8") as f:
            sql = f.read()
        cur = self.conn.cursor()
        if self.db_type == "postgres":
            cur.execute(sql)
        else:
            self.conn.executescript(sql)
        if self.db_type == "sqlite":
            self.conn.commit()

    def init_postgres_tables(self):
        # Verifica se as tabelas já existem
        cur = self.query("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'phases';
        """)
        row = cur.fetchone()
        if not row:
            print("[*] Criando tabelas no PostgreSQL a partir de schema.sql e populando com seed.sql...")
            schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
            seed_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed.sql")
            self.execute_script(schema_path)
            self.execute_script(seed_path)
            print("[OK] Tabelas e sementes do PostgreSQL criadas com sucesso!")

    def init_sqlite_tables(self):
        cur = self.conn.cursor()
        cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
          id         INTEGER PRIMARY KEY AUTOINCREMENT,
          email      TEXT UNIQUE NOT NULL,
          name       TEXT,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS phases (
          id        INTEGER PRIMARY KEY AUTOINCREMENT,
          position  INTEGER NOT NULL,
          title     TEXT NOT NULL,
          duration  TEXT,
          project   TEXT,
          resources TEXT,
          tip       TEXT
        );

        CREATE TABLE IF NOT EXISTS topic_groups (
          id       INTEGER PRIMARY KEY AUTOINCREMENT,
          phase_id INTEGER NOT NULL REFERENCES phases(id) ON DELETE CASCADE,
          position INTEGER NOT NULL,
          name     TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS topics (
          id       INTEGER PRIMARY KEY AUTOINCREMENT,
          group_id INTEGER NOT NULL REFERENCES topic_groups(id) ON DELETE CASCADE,
          position INTEGER NOT NULL,
          title    TEXT NOT NULL,
          code     TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS progress (
          user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
          topic_id    INTEGER NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
          status      TEXT CHECK (status IN ('z','r','e')),
          note        TEXT,
          review_date TEXT,
          updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (user_id, topic_id)
        );
        """)
        self.conn.commit()

        # Seed data if empty
        cur.execute("SELECT COUNT(*) as count FROM phases")
        count = cur.fetchone()[0]
        if count == 0:
            print("[*] Populando SQLite com dados iniciais do roteiro...")
            seed_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_data.json")
            if os.path.exists(seed_json):
                with open(seed_json, "r", encoding="utf-8") as f:
                    phases = json.load(f)
                cur.execute("INSERT OR IGNORE INTO users (id, email, name) VALUES (1, 'aluno@local.com', 'Aluno Local')")
                t_id = 1
                g_id = 1
                p_id = 1
                for p in phases:
                    cur.execute(
                        "INSERT INTO phases (id, position, title, duration, project, resources, tip) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (p_id, p["position"], p["title"], p["duration"], p["project"], p["resources"], p.get("tip", ""))
                    )
                    for g in p["groups"]:
                        cur.execute(
                            "INSERT INTO topic_groups (id, phase_id, position, name) VALUES (?, ?, ?, ?)",
                            (g_id, p_id, g["position"], g["name"])
                        )
                        for t in g["topics"]:
                            cur.execute(
                                "INSERT INTO topics (id, group_id, position, title, code) VALUES (?, ?, ?, ?, ?)",
                                (t_id, g_id, t["position"], t["title"], t["code"])
                            )
                            t_id += 1
                        g_id += 1
                    p_id += 1
                self.conn.commit()
                print(f"[OK] SQLite populado com {p_id-1} fases e {t_id-1} tópicos!")

    # -----------------------------------------------------------------------
    # Operações da aplicação
    # -----------------------------------------------------------------------
    def get_status(self, user_id=1):
        cur = self.query("SELECT COUNT(*) AS total FROM topics")
        row = cur.fetchone()
        total_topics = row["total"] if isinstance(row, dict) else row[0]

        cur = self.query("SELECT COUNT(*) AS done FROM progress WHERE user_id = %s AND status = 'e'", (user_id,))
        row = cur.fetchone()
        done_topics = row["done"] if isinstance(row, dict) else row[0]

        return {
            "status": "online",
            "db_type": self.db_type,
            "connected": True,
            "user_id": user_id,
            "total_topics": total_topics,
            "done_topics": done_topics
        }

    def get_phases(self):
        sql = """
        SELECT 
          p.id AS p_id, p.position AS p_pos, p.title AS p_title, p.duration AS p_dur, p.project AS p_proj, p.resources AS p_res, p.tip AS p_tip,
          g.id AS g_id, g.position AS g_pos, g.name AS g_name,
          t.id AS t_id, t.position AS t_pos, t.title AS t_title, t.code AS t_code
        FROM phases p
        LEFT JOIN topic_groups g ON g.phase_id = p.id
        LEFT JOIN topics t ON t.group_id = g.id
        ORDER BY p.position, g.position, t.position;
        """
        cur = self.query(sql)
        rows = cur.fetchall()

        phases_map = {}
        for r in rows:
            if isinstance(r, sqlite3.Row):
                r = dict(r)
            pid = r["p_id"]
            if pid not in phases_map:
                phases_map[pid] = {
                    "id": f"p{pid}",
                    "db_id": pid,
                    "order": r["p_pos"],
                    "title": r["p_title"],
                    "dur": r["p_dur"] or "",
                    "project": r["p_proj"] or "",
                    "res": r["p_res"] or "",
                    "tip": r.get("p_tip") or "",
                    "groups": []
                }
            gid = r["g_id"]
            if not gid:
                continue
            groups = phases_map[pid]["groups"]
            group = next((g for g in groups if g["db_id"] == gid), None)
            if not group:
                group = {
                    "id": f"{pid}-{gid}",
                    "db_id": gid,
                    "name": r["g_name"],
                    "topics": []
                }
                groups.append(group)
            tid = r["t_id"]
            if not tid:
                continue
            code = r["t_code"] or str(tid)
            group["topics"].append({
                "id": code,
                "db_id": tid,
                "title": r["t_title"]
            })

        return list(phases_map.values())

    def get_progress(self, user_id=1):
        sql = """
        SELECT t.id AS topic_id, t.code AS topic_code, p.status, p.note, p.review_date
        FROM progress p
        JOIN topics t ON t.id = p.topic_id
        WHERE p.user_id = %s;
        """
        cur = self.query(sql, (user_id,))
        rows = cur.fetchall()
        result = {}
        for r in rows:
            if isinstance(r, sqlite3.Row):
                r = dict(r)
            tid = str(r["topic_id"])
            code = r["topic_code"] or tid
            val = {
                "s": r["status"] or "",
                "n": r["note"] or "",
                "d": str(r["review_date"]) if r["review_date"] else ""
            }
            result[code] = val
            result[tid] = val
        return result

    def resolve_topic_id(self, topic_identifier, title=None):
        if isinstance(topic_identifier, int) or (isinstance(topic_identifier, str) and topic_identifier.isdigit()):
            return int(topic_identifier)
        code_str = str(topic_identifier)
        cur = self.query("SELECT id FROM topics WHERE code = %s LIMIT 1", (code_str,))
        row = cur.fetchone()
        if row:
            return row["id"] if isinstance(row, dict) else row[0]

        # Cria automaticamente o tópico no banco caso seja novo (ex: trilhas de Inglês ou Matemática)
        try:
            sql = "INSERT INTO topics (group_id, position, title, code) VALUES (%s, %s, %s, %s)"
            self.query(sql, (1, 999, title or code_str, code_str))
            if self.db_type == "sqlite":
                self.conn.commit()
            cur = self.query("SELECT id FROM topics WHERE code = %s LIMIT 1", (code_str,))
            row = cur.fetchone()
            if row:
                return row["id"] if isinstance(row, dict) else row[0]
        except Exception:
            pass
        return None

    def save_progress(self, user_id, topic_identifier, status, note, review_date):
        topic_id = self.resolve_topic_id(topic_identifier)
        if not topic_id:
            return False

        status = status if status in ("z", "r", "e") else None
        note = note or None
        review_date = review_date or None

        if self.db_type == "postgres":
            sql = """
            INSERT INTO progress (user_id, topic_id, status, note, review_date, updated_at)
            VALUES (%s, %s, %s, %s, %s, now())
            ON CONFLICT (user_id, topic_id) DO UPDATE SET
              status = EXCLUDED.status,
              note = EXCLUDED.note,
              review_date = EXCLUDED.review_date,
              updated_at = now();
            """
        else:
            sql = """
            INSERT INTO progress (user_id, topic_id, status, note, review_date, updated_at)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (user_id, topic_id) DO UPDATE SET
              status = excluded.status,
              note = excluded.note,
              review_date = excluded.review_date,
              updated_at = CURRENT_TIMESTAMP;
            """
        cur = self.query(sql, (user_id, topic_id, status, note, review_date))
        if self.db_type == "sqlite":
            self.conn.commit()
        return True

    def bulk_save_progress(self, user_id, progress_dict):
        saved_count = 0
        for key, val in progress_dict.items():
            s = val.get("s", "")
            n = val.get("n", "")
            d = val.get("d", "")
            if self.save_progress(user_id, key, s, n, d):
                saved_count += 1
        return saved_count

    def clear_progress(self, user_id=1):
        self.query("DELETE FROM progress WHERE user_id = %s", (user_id,))
        if self.db_type == "sqlite":
            self.conn.commit()
        return True

# Instanciar conexão global com o banco
DB = Database(CONFIG)

# ---------------------------------------------------------------------------
# Manipulador HTTP REST API e Servidor de Arquivos Estáticos
# ---------------------------------------------------------------------------
class RoteiroHandler(BaseHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def send_json(self, data, status_code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/api/status":
            user_id = int(query.get("user_id", [1])[0])
            self.send_json(DB.get_status(user_id))
        elif path == "/api/phases":
            self.send_json(DB.get_phases())
        elif path == "/api/progress":
            user_id = int(query.get("user_id", [1])[0])
            self.send_json(DB.get_progress(user_id))
        else:
            self.serve_static(path)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length > 0 else b"{}"
        try:
            payload = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            payload = {}

        if path == "/api/progress":
            user_id = payload.get("user_id", 1)
            topic_id = payload.get("topic_id") or payload.get("id")
            s = payload.get("s", payload.get("status", ""))
            n = payload.get("n", payload.get("note", ""))
            d = payload.get("d", payload.get("review_date", ""))
            ok = DB.save_progress(user_id, topic_id, s, n, d)
            self.send_json({"success": ok})
        elif path == "/api/progress/bulk":
            user_id = payload.get("user_id", 1)
            progress = payload.get("progress", {})
            count = DB.bulk_save_progress(user_id, progress)
            self.send_json({"success": True, "saved_items": count})
        elif path == "/api/progress/clear":
            user_id = payload.get("user_id", 1)
            DB.clear_progress(user_id)
            self.send_json({"success": True})
        else:
            self.send_json({"error": "Endpoint não encontrado"}, 404)

    def serve_static(self, path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if path in ("/", "/index.html", "/roteiro"):
            filename = "index.html"
            filepath = os.path.join(base_dir, filename)
            if not os.path.exists(filepath):
                filename = "Roteiro de Estudo_ do zero à IA.html"
                filepath = os.path.join(base_dir, filename)
        else:
            clean_path = path.lstrip("/")
            filepath = os.path.join(base_dir, clean_path)

        if os.path.isfile(filepath):
            mime_type, _ = mimetypes.guess_type(filepath)
            mime_type = mime_type or "application/octet-stream"
            if mime_type.startswith("text/") or mime_type in ("application/javascript", "application/json"):
                mime_type += "; charset=utf-8"
            try:
                with open(filepath, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_cors_headers()
                self.send_header("Content-Type", mime_type)
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_json({"error": f"Erro ao ler arquivo: {e}"}, 500)
        else:
            self.send_json({"error": "Arquivo não encontrado"}, 404)

    def log_message(self, format, *args):
        # Log mais limpo para requisições no terminal
        if self.path.startswith("/api/"):
            print(f"[API] {self.command} {self.path} -> {args[1]}")
        else:
            super().log_message(format, *args)

# ---------------------------------------------------------------------------
# Execução do Servidor
# ---------------------------------------------------------------------------
class ReusableServer(ThreadingHTTPServer):
    allow_reuse_address = True

def run_server():
    base_port = int(CONFIG.get("PORT", 8000))
    server = None
    port = base_port
    for p in [base_port, 8080, 8001, 8088]:
        try:
            server = ReusableServer(("0.0.0.0", p), RoteiroHandler)
            port = p
            break
        except OSError:
            continue

    if not server:
        print(f"[!] Não foi possível iniciar o servidor na porta {base_port} nem nas portas alternativas.")
        return

    print("\n" + "="*60)
    print("🚀 Servidor Roteiro IA iniciado!")
    print(f"👉 Acesse no seu navegador: http://localhost:{port}")
    print(f"📦 Banco de Dados em uso: {DB.db_type.upper()}")
    print("="*60 + "\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Encerrando servidor...")
        server.server_close()

if __name__ == "__main__":
    run_server()
