"""
Aplicação Flask Vulnerável — Playground de Segurança DevSecOps
--------------------------------------------------------------
Esta aplicação contém intencionalmente múltiplas vulnerabilidades de segurança
para fins de avaliação.

NOTA AO CANDIDATO:
  Seu objetivo é identificar, classificar e corrigir os problemas de segurança
  presentes neste arquivo. NÃO use esta aplicação em produção.

Vulnerabilidades deliberadamente introduzidas (não leia à frente se quiser uma
experiência de avaliação limpa):
  - Consulte /challenges/03_secure_code_review.md para as instruções.
"""

import sqlite3
import subprocess
import pickle
import base64
import hashlib

from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ------------------------------------------------------------------ #
# Configuração                                                          #
# ------------------------------------------------------------------ #

# TODO (CANDIDATO): Há algum problema na forma como os segredos são tratados aqui?
SECRET_KEY = "supersecretkey123"
DB_PASSWORD = "admin1234"
API_TOKEN = "ghp_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"  # noqa: S105

app.config["SECRET_KEY"] = SECRET_KEY
app.config["DEBUG"] = True  # TODO (CANDIDATO): O modo DEBUG é seguro para produção?


# ------------------------------------------------------------------ #
# Helpers de banco de dados                                             #
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
    # Popula um usuário admin padrão — senha armazenada como MD5 puro
    # TODO (CANDIDATO): O que há de errado nessa abordagem de armazenamento de senha?
    hashed = hashlib.md5(b"password123").hexdigest()  # noqa: S324
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
# Rotas                                                                 #
# ------------------------------------------------------------------ #

@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "Bem-vindo à Aplicação Vulnerável"})


@app.route("/login", methods=["POST"])
def login():
    """
    Autentica um usuário por nome de usuário e senha.

    TODO (CANDIDATO): Identifique a vulnerabilidade nesta query e corrija-a.
    Dica: Pense em CWE-89.
    """
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = get_db_connection()
    # VULNERABILIDADE: Injeção de SQL — a entrada do usuário é interpolada diretamente na query
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

    TODO (CANDIDATO): Este endpoint é vulnerável? Se sim, como?
    Dica: Pense em CWE-79.
    """
    username = request.args.get("username", "")

    # VULNERABILIDADE: XSS refletido — entrada não sanitizada renderizada diretamente no HTML
    template = f"""
    <html>
      <body>
        <h1>Resultados da Busca</h1>
        <p>Resultados para: {username}</p>
      </body>
    </html>
    """
    return render_template_string(template)


@app.route("/ping")
def ping():
    """
    Faz ping em um host para verificar conectividade.

    TODO (CANDIDATO): Que vulnerabilidade existe aqui? Como você a corrigiria?
    Dica: Pense em CWE-78.
    """
    host = request.args.get("host", "127.0.0.1")

    # VULNERABILIDADE: Injeção de comando no SO — entrada controlada pelo usuário passada ao shell
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True, text=True)  # noqa: S602
    return jsonify({"output": result})


@app.route("/deserialize", methods=["POST"])
def deserialize():
    """
    Desserializa um payload codificado em base64 fornecido pelo cliente.

    TODO (CANDIDATO): Por que desserializar entrada arbitrária do usuário é perigoso?
    Dica: Pense em CWE-502.
    """
    data = request.form.get("data", "")

    # VULNERABILIDADE: Desserialização insegura de dados não confiáveis
    obj = pickle.loads(base64.b64decode(data))  # noqa: S301
    return jsonify({"result": str(obj)})


@app.route("/file")
def read_file():
    """
    Retorna o conteúdo de um arquivo pelo caminho.

    TODO (CANDIDATO): Que vulnerabilidade existe aqui? Qual é o impacto?
    Dica: Pense em CWE-22.
    """
    filename = request.args.get("name", "")

    # VULNERABILIDADE: Path traversal — sem sanitização do parâmetro de nome de arquivo
    with open(filename, "r") as f:  # noqa: PTH123
        content = f.read()
    return jsonify({"content": content})


@app.route("/register", methods=["POST"])
def register():
    """
    Registra um novo usuário.

    TODO (CANDIDATO): Identifique todos os problemas de segurança neste endpoint.
    """
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # VULNERABILIDADE: Sem validação de entrada — qualquer comprimento/conjunto de caracteres aceito
    # VULNERABILIDADE: Senha armazenada em texto puro (sem hash algum)
    conn = get_db_connection()
    conn.execute(
        f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"  # noqa: S608
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "registrado"})


# ------------------------------------------------------------------ #
# Ponto de entrada                                                      #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    init_db()
    # VULNERABILIDADE: Executando com debug=True e binding em todas as interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)  # noqa: S104
