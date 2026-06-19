"""
Vulnerable Flask Application — DevSecOps Security Playground
------------------------------------------------------------
This application intentionally contains multiple security vulnerabilities
for assessment purposes.

CANDIDATE NOTE:
  Your goal is to identify, classify, and fix the security issues present
  in this file. Do NOT use this application in production.

Vulnerabilities deliberately introduced (do not read ahead if you want a
clean assessment experience):
  - See /challenges/03_secure_code_review.md for instructions.
"""

import sqlite3
import subprocess
import pickle
import base64
import hashlib

from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ------------------------------------------------------------------ #
# Configuration                                                         #
# ------------------------------------------------------------------ #

# TODO (CANDIDATE): Is there anything wrong with how secrets are handled here?
SECRET_KEY = "supersecretkey123"
DB_PASSWORD = "admin1234"
API_TOKEN = "ghp_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"  # noqa: S105

app.config["SECRET_KEY"] = SECRET_KEY
app.config["DEBUG"] = True  # TODO (CANDIDATE): Is DEBUG mode safe for production?


# ------------------------------------------------------------------ #
# Database helpers                                                      #
# ------------------------------------------------------------------ #

def get_db_connection():
    """Return a connection to the local SQLite database."""
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialise the database with seed data."""
    conn = get_db_connection()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )"""
    )
    # Seed a default admin user — password stored as plain MD5
    # TODO (CANDIDATE): What is wrong with this password storage approach?
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
# Routes                                                                #
# ------------------------------------------------------------------ #

@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "Welcome to the Vulnerable App"})


@app.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user by username and password.

    TODO (CANDIDATE): Identify the vulnerability in this query and fix it.
    Hint: Think about CWE-89.
    """
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = get_db_connection()
    # VULNERABILITY: SQL injection — user input is interpolated directly into the query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    user = conn.execute(query).fetchone()
    conn.close()

    if user:
        return jsonify({"status": "success", "role": user["role"]})
    return jsonify({"status": "failure", "message": "Invalid credentials"}), 401


@app.route("/search")
def search():
    """
    Search for a user by username.

    TODO (CANDIDATE): Is this endpoint vulnerable? If so, how?
    Hint: Think about CWE-79.
    """
    username = request.args.get("username", "")

    # VULNERABILITY: Reflected XSS — unsanitised input rendered directly in HTML
    template = f"""
    <html>
      <body>
        <h1>Search Results</h1>
        <p>Results for: {username}</p>
      </body>
    </html>
    """
    return render_template_string(template)


@app.route("/ping")
def ping():
    """
    Ping a host to check connectivity.

    TODO (CANDIDATE): What vulnerability exists here? How would you fix it?
    Hint: Think about CWE-78.
    """
    host = request.args.get("host", "127.0.0.1")

    # VULNERABILITY: OS command injection — user-controlled input passed to shell
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True, text=True)  # noqa: S602
    return jsonify({"output": result})


@app.route("/deserialize", methods=["POST"])
def deserialize():
    """
    Deserialise a base64-encoded payload provided by the client.

    TODO (CANDIDATE): Why is deserialising arbitrary user input dangerous?
    Hint: Think about CWE-502.
    """
    data = request.form.get("data", "")

    # VULNERABILITY: Insecure deserialisation of untrusted data
    obj = pickle.loads(base64.b64decode(data))  # noqa: S301
    return jsonify({"result": str(obj)})


@app.route("/file")
def read_file():
    """
    Return the contents of a file by path.

    TODO (CANDIDATE): What vulnerability exists here? What is the impact?
    Hint: Think about CWE-22.
    """
    filename = request.args.get("name", "")

    # VULNERABILITY: Path traversal — no sanitisation of the filename parameter
    with open(filename, "r") as f:  # noqa: PTH123
        content = f.read()
    return jsonify({"content": content})


@app.route("/register", methods=["POST"])
def register():
    """
    Register a new user.

    TODO (CANDIDATE): Identify all security issues in this endpoint.
    """
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # VULNERABILITY: No input validation — any length/character set accepted
    # VULNERABILITY: Password stored in plain text (no hashing at all)
    conn = get_db_connection()
    conn.execute(
        f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"  # noqa: S608
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "registered"})


# ------------------------------------------------------------------ #
# Entry point                                                           #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    init_db()
    # VULNERABILITY: Running with debug=True and binding to all interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)  # noqa: S104
