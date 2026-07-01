# Gabarito de Vulnerabilidades — `app/app.py`

> **Finalidade:** Este documento lista e classifica todas as vulnerabilidades intencionalmente presentes na aplicação Flask de laboratório, servindo como gabarito para avaliação de candidatos.

---

## Sumário

| # | Vulnerabilidade | Localização | CWE | OWASP Top 10 (2021) | Severidade |
| --- | --- | --- | --- | --- | --- |
| 1 | SQL Injection — Login | `login()` linha 86 | CWE-89 | A03 — Injection | Crítica |
| 2 | SQL Injection — Register | `register()` linha 165 | CWE-89 | A03 — Injection | Crítica |
| 3 | Injeção de Comando (OS Command Injection) | `ping()` linha 122 | CWE-78 | A03 — Injection | Crítica |
| 4 | Desserialização Insegura | `deserialize()` linha 137 | CWE-502 | A08 — Software and Data Integrity Failures | Crítica |
| 5 | Path Traversal (Directory Traversal) | `read_file()` linha 150 | CWE-22 | A01 — Broken Access Control | Alta |
| 6 | Server-Side Template Injection (SSTI) | `search()` linha 101 | CWE-94 | A03 — Injection | Alta |
| 7 | Segredos Hardcoded no Código-Fonte | Linhas 27–29 | CWE-798 | A02 — Cryptographic Failures | Alta |
| 8 | Algoritmo de Hash Fraco (MD5) para Senhas | `init_db()` linha 57 | CWE-916 | A02 — Cryptographic Failures | Alta |
| 9 | Senha Armazenada em Texto Claro | `init_db()` linha 62 | CWE-256 | A02 — Cryptographic Failures | Alta |
| 10 | Modo Debug Habilitado em Produção | Linha 32 e linha 179 | CWE-94 | A05 — Security Misconfiguration | Média |
| 11 | Aplicação Exposta em Todas as Interfaces (`0.0.0.0`) | Linha 179 | CWE-605 | A05 — Security Misconfiguration | Média |
| 12 | Ausência de Autenticação nos Endpoints Sensíveis | Múltiplos endpoints | CWE-306 | A01 — Broken Access Control | Alta |
| 13 | Ausência de Validação e Sanitização de Entrada | Múltiplos endpoints | CWE-20 | A03 — Injection | Alta |
| 14 | Ausência de Logging e Monitoramento | Aplicação inteira | CWE-778 | A09 — Security Logging and Monitoring Failures | Média |

---

## Detalhamento das Vulnerabilidades

---

### 1. SQL Injection — Login (Crítica)

**Localização:** `login()` — linha 86
**CWE:** CWE-89 — Improper Neutralization of Special Elements used in an SQL Command
**OWASP:** A03:2021 — Injection

**Código vulnerável:**

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
user = conn.execute(query).fetchone()
```

**Descrição:**
O valor recebido do formulário é concatenado diretamente na query SQL sem qualquer sanitização. Um atacante pode injetar código SQL para bypassar a autenticação.

**Exemplo de exploit:**

```text
username: admin' --
password: qualquer_coisa
# Query resultante: SELECT * FROM users WHERE username = 'admin' --' AND password = '...'
# O comentário "--" ignora a verificação da senha.
```

**Correção:**
Utilizar parametrização de queries (prepared statements):

```python
user = conn.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (username, hashed_password)
).fetchone()
```

---

### 2. SQL Injection — Register (Crítica)

**Localização:** `register()` — linha 165
**CWE:** CWE-89
**OWASP:** A03:2021 — Injection

**Código vulnerável:**

```python
conn.execute(
    f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
)
```

**Descrição:**
Idêntico ao caso anterior. A concatenação de string para montar a query permite injeção SQL no endpoint de registro.

**Exemplo de exploit:**

```text
username: hacker', 'x', 'admin') --
# Isso permite registrar um usuário com role 'admin'.
```

**Correção:**

```python
conn.execute(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    (username, hashed_password)
)
```

---

### 3. OS Command Injection (Crítica)

**Localização:** `ping()` — linha 122
**CWE:** CWE-78 — Improper Neutralization of Special Elements used in an OS Command
**OWASP:** A03:2021 — Injection

**Código vulnerável:**

```python
host = request.args.get("host", "127.0.0.1")
result = subprocess.check_output(f"ping {flag} 1 {host}", shell=True, text=True)
```

**Descrição:**
O parâmetro `host` é inserido diretamente em um comando shell executado com `shell=True`. Um atacante pode encadear comandos arbitrários.

**Exemplo de exploit:**

```text
GET /ping?host=127.0.0.1; cat /etc/passwd
GET /ping?host=127.0.0.1 && whoami
```

**Correção:**
Passar os argumentos como lista, sem `shell=True`, e validar o input com regex de IP/hostname:

```python
import re

HOST_RE = re.compile(r'^[a-zA-Z0-9.\-]{1,253}$')

if not HOST_RE.match(host):
    return jsonify({"error": "Host inválido"}), 400

result = subprocess.check_output(["ping", flag, "1", host], text=True)
```

---

### 4. Desserialização Insegura (Crítica)

**Localização:** `deserialize()` — linha 137
**CWE:** CWE-502 — Deserialization of Untrusted Data
**OWASP:** A08:2021 — Software and Data Integrity Failures

**Código vulnerável:**

```python
obj = pickle.loads(base64.b64decode(data))
```

**Descrição:**
`pickle.loads()` executado sobre dados fornecidos pelo usuário permite **Remote Code Execution (RCE)**. O módulo `pickle` pode instanciar classes e executar código arbitrário durante a desserialização.

**Exemplo de exploit:**
O script `scripts/pickle_dumps_base64.py` já demonstra como gerar um payload malicioso. Um atacante pode criar um objeto com `__reduce__` que executa um comando de sistema.

**Correção:**
Nunca desserializar `pickle` com dados não confiáveis. Usar formatos seguros como JSON:

```python
import json

obj = json.loads(base64.b64decode(data))
```

---

### 5. Path Traversal — Directory Traversal (Alta)

**Localização:** `read_file()` — linha 150
**CWE:** CWE-22 — Improper Limitation of a Pathname to a Restricted Directory
**OWASP:** A01:2021 — Broken Access Control

**Código vulnerável:**

```python
filename = request.args.get("name", "")
with open(filename, "r") as f:
    content = f.read()
```

**Descrição:**
O caminho do arquivo é fornecido diretamente pelo usuário sem qualquer restrição. Um atacante pode ler arquivos arbitrários do sistema de arquivos.

**Exemplo de exploit:**

```text
GET /file?name=../../etc/passwd
GET /file?name=C:\Windows\System32\drivers\etc\hosts
GET /file?name=users.db   # Expõe o banco de dados inteiro
```

**Correção:**
Restringir a leitura a um diretório específico e validar o caminho:

```python
import os

SAFE_DIR = os.path.abspath("./static/files")
requested = os.path.abspath(os.path.join(SAFE_DIR, filename))

if not requested.startswith(SAFE_DIR):
    return jsonify({"error": "Acesso negado"}), 403

with open(requested, "r") as f:
    content = f.read()
```

---

### 6. Server-Side Template Injection — SSTI (Alta)

**Localização:** `search()` — linha 101
**CWE:** CWE-94 — Improper Control of Generation of Code
**OWASP:** A03:2021 — Injection

**Código vulnerável:**

```python
username = request.args.get("username", "")
template = f"""
    ...
    <p>Resultados para: {username}</p>
    ...
"""
return render_template_string(template, user=user)
```

**Descrição:**
O valor de `username` é interpolado via f-string **antes** de ser passado para `render_template_string`. Isso permite que um atacante injete diretivas Jinja2 que serão avaliadas pelo motor de template.

**Exemplo de exploit:**

```text
GET /search?username={{7*7}}          → exibe "49"
GET /search?username={{config}}       → expõe configurações da aplicação (incluindo SECRET_KEY)
GET /search?username={{''.__class__.__mro__[1].__subclasses__()}}  → RCE potencial
```

**Correção:**
Nunca interpolar input do usuário no template. Passar os dados como variáveis de contexto:

```python
TEMPLATE = """
    <html><body>
      <h1>Resultados da Busca</h1>
      <p>Resultados para: {{ username }}</p>
      ...
    </body></html>
"""
return render_template_string(TEMPLATE, username=username, user=user)
```

---

### 7. Segredos Hardcoded no Código-Fonte (Alta)

**Localização:** Linhas 27–29
**CWE:** CWE-798 — Use of Hard-coded Credentials
**OWASP:** A02:2021 — Cryptographic Failures

**Código vulnerável:**

```python
SECRET_KEY = "supersecretkey123"
DB_PASSWORD = "admin1234"
API_TOKEN = "ghp_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
```

**Descrição:**
Credenciais e tokens hardcoded no código-fonte são expostos a qualquer pessoa com acesso ao repositório (histórico Git inclusive). O token `ghp_` simula um Personal Access Token do GitHub.

**Correção:**
Utilizar variáveis de ambiente e nunca commitar segredos:

```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
API_TOKEN  = os.environ["API_TOKEN"]
```

Adicionar `.env` ao `.gitignore` e usar um cofre de segredos (ex.: Azure Key Vault, AWS Secrets Manager) em produção.

---

### 8. Hash Fraco — MD5 para Senhas (Alta)

**Localização:** `init_db()` — linha 57
**CWE:** CWE-916 — Use of Password Hash With Insufficient Computational Effort
**OWASP:** A02:2021 — Cryptographic Failures

**Código vulnerável:**

```python
hashed = hashlib.md5(b"password123").hexdigest()
```

**Descrição:**
MD5 é um algoritmo criptograficamente quebrado e extremamente rápido, tornando ataques de força bruta e rainbow tables triviais. Não deve ser usado para hashing de senhas.

**Correção:**
Utilizar algoritmos projetados para senhas, com salt automático e fator de custo ajustável:

```python
import bcrypt

hashed = bcrypt.hashpw(b"password123", bcrypt.gensalt())
```

Alternativas aceitas: `argon2-cffi`, `passlib` com `argon2` ou `bcrypt`.

---

### 9. Senha em Texto Claro no Banco de Dados (Alta)

**Localização:** `init_db()` — linha 62
**CWE:** CWE-256 — Plaintext Storage of a Password
**OWASP:** A02:2021 — Cryptographic Failures

**Código vulnerável:**

```python
conn.execute(
    "INSERT OR IGNORE INTO users (id, username, password, role) VALUES (2, 'alice', 'alice123', 'user')",
)
```

**Descrição:**
A senha do usuário `alice` é armazenada em texto plano no banco de dados. Qualquer pessoa com acesso ao arquivo `users.db` (incluindo via vulnerabilidade #5) tem acesso imediato à credencial.

**Correção:**
Aplicar hash com bcrypt (ou equivalente) antes de inserir no banco, conforme item anterior.

---

### 10. Modo Debug Habilitado (Média)

**Localização:** Linha 32 (`app.config`) e linha 179 (`app.run`)
**CWE:** CWE-94 / Misconfiguration
**OWASP:** A05:2021 — Security Misconfiguration

**Código vulnerável:**

```python
app.config["DEBUG"] = True
# ...
app.run(host="0.0.0.0", port=5000, debug=True)
```

**Descrição:**
Com `DEBUG=True`, o Flask expõe um **debugger interativo** no browser que permite execução de código Python arbitrário no servidor. Também exibe stack traces detalhados com variáveis internas.

**Correção:**
Controlar o modo debug por variável de ambiente e nunca habilitar em produção:

```python
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
app.config["DEBUG"] = DEBUG
app.run(debug=DEBUG)
```

---

### 11. Aplicação Exposta em Todas as Interfaces de Rede (Média)

**Localização:** Linha 179
**CWE:** CWE-605 — Multiple Binds to the Same Port
**OWASP:** A05:2021 — Security Misconfiguration

**Código vulnerável:**

```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

**Descrição:**
`host="0.0.0.0"` faz a aplicação escutar em **todas** as interfaces de rede do servidor, tornando-a acessível externamente sem passar por nenhum proxy reverso ou firewall de aplicação (WAF).

**Correção:**
Em desenvolvimento, usar `127.0.0.1`. Em produção, usar um WSGI server (Gunicorn, uWSGI) atrás de um reverse proxy (Nginx, Apache) e nunca expor o Flask diretamente:

```python
app.run(host="127.0.0.1", port=5000)
```

---

### 12. Ausência de Autenticação e Autorização (Alta)

**Localização:** Todos os endpoints (`/ping`, `/file`, `/deserialize`, `/search`, `/register`)
**CWE:** CWE-306 — Missing Authentication for Critical Function
**OWASP:** A01:2021 — Broken Access Control

**Descrição:**
Nenhum dos endpoints sensíveis exige autenticação. Qualquer usuário anônimo pode executar comandos no servidor (`/ping`), ler arquivos arbitrários (`/file`), obter RCE via desserialização (`/deserialize`) e registrar novos usuários (`/register`).

**Correção:**
Implementar autenticação (ex.: JWT, Flask-Login, sessão segura) e aplicar decorators de autorização nos endpoints:

```python
from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not validate_token(token):
            return jsonify({"error": "Não autorizado"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/file")
@require_auth
def read_file():
    ...
```

---

### 13. Ausência de Validação de Entrada (Alta)

**Localização:** Todos os endpoints
**CWE:** CWE-20 — Improper Input Validation
**OWASP:** A03:2021 — Injection

**Descrição:**
Nenhum dos parâmetros recebidos pelos endpoints é validado quanto a tipo, tamanho, formato ou caracteres permitidos. Isso amplifica o impacto de todas as outras vulnerabilidades de injeção listadas acima.

**Correção:**
Utilizar uma biblioteca de validação de schemas (ex.: `marshmallow`, `pydantic`, `cerberus`) e definir esquemas explícitos para todos os inputs:

```python
from pydantic import BaseModel, constr

class LoginInput(BaseModel):
    username: constr(max_length=64, pattern=r'^[a-zA-Z0-9_]+$')
    password: constr(min_length=8, max_length=128)
```

---

### 14. Ausência de Logging e Monitoramento de Segurança (Média)

**Localização:** Aplicação inteira
**CWE:** CWE-778 — Insufficient Logging
**OWASP:** A09:2021 — Security Logging and Monitoring Failures

**Descrição:**
A aplicação não registra tentativas de login falhas, erros de autenticação, acessos a arquivos ou execuções de comandos. Isso impede a detecção de ataques em andamento e a análise forense pós-incidente.

**Correção:**
Configurar logging estruturado para eventos de segurança:

```python
import logging

logging.basicConfig(level=logging.INFO)
security_logger = logging.getLogger("security")

# Exemplo de uso:
security_logger.warning("Falha de login para usuário: %s de IP: %s", username, request.remote_addr)
```

---

## Mapa OWASP Top 10

| OWASP Top 10 (2021) | Vulnerabilidades encontradas |
| --- | --- |
| A01 — Broken Access Control | Path Traversal (#5), Ausência de Autenticação (#12) |
| A02 — Cryptographic Failures | Segredos Hardcoded (#7), Hash Fraco MD5 (#8), Senha em Claro (#9) |
| A03 — Injection | SQL Injection Login (#1), SQL Injection Register (#2), Command Injection (#3), SSTI (#6), Validação de Entrada (#13) |
| A05 — Security Misconfiguration | Debug Mode (#10), Exposição 0.0.0.0 (#11) |
| A08 — Software and Data Integrity Failures | Desserialização Insegura com Pickle (#4) |
| A09 — Security Logging and Monitoring Failures | Ausência de Logging (#14) |

---

## Pontuação de Referência para Avaliação

| Categoria | Pontos por item | Total disponível |
| --- | --- | --- |
| Identificação correta da vulnerabilidade | 1 pt | 14 pts |
| Classificação CWE correta | 1 pt | 14 pts |
| Classificação OWASP correta | 1 pt | 14 pts |
| Correção proposta adequada | 2 pts | 28 pts |
| **Total** | | **70 pts** |

> **Nota:** Vulnerabilidades críticas não identificadas (#1, #3, #4) devem ser consideradas eliminatórias em avaliações de perfil de segurança sênior.
