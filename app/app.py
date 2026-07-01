"""
Aplicação Flask Vulnerável — Playground de Segurança DevSecOps
--------------------------------------------------------------
Esta aplicação contém intencionalmente múltiplas vulnerabilidades de segurança
para fins de avaliação.

NOTA AO CANDIDATO:
  Seu objetivo é identificar, classificar e corrigir os problemas de segurança
  presentes neste arquivo. NÃO use esta aplicação em ambientes produtivos.
"""

import sqlite3
import subprocess
import pickle
import base64
import hashlib
import platform

from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ------------------------------------------------------------------ #
# Configuração                                                       #
# ------------------------------------------------------------------ #

SECRET_KEY = "supersecretkey123"
DB_PASSWORD = "admin1234"
API_TOKEN = "ghp_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

app.config["SECRET_KEY"] = SECRET_KEY
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False


# ------------------------------------------------------------------ #
# Helpers de banco de dados                                          #
# ------------------------------------------------------------------ #

def get_db_connection():
    """Retorna uma conexão com o banco de dados SQLite local."""
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inicializa o banco de dados com dados de seed."""
    conn = get_db_connection()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )"""
    )

    hashed = hashlib.md5(b"password123").hexdigest()
    conn.execute(
        "INSERT OR IGNORE INTO users (id, username, password, role) VALUES (1, 'admin', ?, 'admin')",
        (hashed,),
    )
    conn.execute(
        "INSERT OR IGNORE INTO users (id, username, password, role) VALUES (2, 'alice', 'alice123', 'user')",
    )
    conn.commit()
    conn.close()


# ------------------------------------------------------------------ #
# Rotas                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "Bem-vindo à Aplicação Vulnerável"})


@app.route("/login", methods=["POST"])
def login():
    """
    Autentica um usuário por nome de usuário e senha.
    """
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = get_db_connection()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    user = conn.execute(query).fetchone()
    conn.close()

    if user:
        return jsonify({"status": "success", "role": user["role"]})
    return jsonify({"status": "failure", "message": "Credenciais inválidas"}), 401


@app.route("/search")
def search():
    """
    Busca um usuário por nome de usuário.
    """
    username = request.args.get("username", "")

    conn = get_db_connection()
    user = conn.execute(
        "SELECT username, role FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()

    template = f"""
    <html>
      <body>
        <h1>Resultados da Busca</h1>
        <p>Resultados para: {username}</p>
        {{% if user %}}
            <p>Nome de usuário: {{{{ user['username'] }}}}</p>
            <p>Função: {{{{ user['role'] }}}}</p>
        {{% else %}}
            <p>Nenhum usuário encontrado.</p>
        {{% endif %}}
      </body>
    </html>
    """
    return render_template_string(template, user=user)


@app.route("/ping")
def ping():
    """
    Faz ping em um host para verificar conectividade.
    """
    host = request.args.get("host", "127.0.0.1")

    flag = "-n" if platform.system() == "Windows" else "-c"
    result = subprocess.check_output(f"ping {flag} 1 {host}", shell=True, text=True)
    return jsonify({"output": result})


@app.route("/deserialize", methods=["POST"])
def deserialize():
    """
    Desserializa um payload codificado em base64 fornecido pelo cliente.

    Exemplo de payload legítimo (base64 + pickle):
    gASVSQAAAAAAAAB9lCiMBWhlbGxvlIwFd29ybGSUjAZudW1iZXKUSyqMBGxpc3SUXZQoSwFLAksDZYwEZGljdJR9lIwDa2V5lIwFdmFsdWWUc3Uu
    """
    data = request.form.get("data", "")

    obj = pickle.loads(base64.b64decode(data))
    return jsonify({"result": str(obj)})


@app.route("/file")
def read_file():
    """
    Retorna o conteúdo de um arquivo pelo caminho.
    """
    filename = request.args.get("name", "")

    with open(filename, "r") as f:
        content = f.read()
    return jsonify({"content": content})


@app.route("/register", methods=["POST"])
def register():
    """
    Registra um novo usuário.
    """
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = get_db_connection()
    conn.execute(
        f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "registrado"})


# ------------------------------------------------------------------ #
# Entrypoint                                                         #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
