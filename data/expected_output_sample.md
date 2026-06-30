# Saída Esperada de Exemplo — vulnerability_parser.py

Este arquivo mostra uma **saída de referência** de uma implementação completa de
`scripts/vulnerability_parser.py` contra `data/mixed_scan_results.json`.

Use este arquivo para validar a saída do seu parser. Pequenas diferenças de
redação são aceitáveis; a classificação e os campos normalizados devem corresponder.

---

## Relatório em Markdown

```markdown
## Relatório de Vulnerabilidades

Gerado em: 2024-11-15
Entrada: data/mixed_scan_results.json
Total de achados: 14 | Verdadeiros Positivos: 10 | Falsos Positivos: 4

### Resumo

| Severidade | Contagem (VP) |
| ---------- | ------------- |
| critical   | 2 |
| high       | 4 |
| medium     | 3 |
| low        | 1 |
| info       | 2 (FP) |

---

### Achados

| ID | Tool | Severity | CWE | File | Line | Description | FP |
| -- | ---- | -------- | --- | ---- | ---- | ----------- | -- |
| FINDING-001 | semgrep | high | CWE-89 | app/app.py | 74 | SQL injection via string formatting | No |
| FINDING-002 | semgrep | high | CWE-78 | app/app.py | 112 | OS command injection via shell=True | No |
| FINDING-003 | snyk | critical | CWE-20 | PyYAML (5.3.1) | N/A | Arbitrary Code Execution via yaml.load() | No |
| FINDING-004 | semgrep | medium | CWE-502 | app/app.py | 126 | Insecure deserialisation using pickle | No |
| FINDING-005 | snyk | high | CWE-79 | lxml (4.6.2) | N/A | XSS via lxml clean module | No |
| FINDING-006 | trivy | medium | N/A | requests (2.25.0) | N/A | Proxy-Authorization header forwarded to destination | No |
| FINDING-007 | semgrep | medium | CWE-798 | app/app.py | 32 | Hardcoded API token detected | No |
| FINDING-008 | semgrep | info | N/A | app/app.py | 44 | FIXME comment found — resolve before merging | Yes |
| FINDING-009 | snyk | critical | CWE-400 | Werkzeug (2.0.1) | N/A | Resource exhaustion via crafted multipart form data | No |
| FINDING-010 | owasp-dep-check | low | CWE-20 | Flask (2.0.1) | N/A | Open redirect in specific configurations | Yes |
| FINDING-011 | semgrep | info | CWE-94 | app/app.py | 36 | Flask DEBUG mode enabled in source code | No |
| FINDING-012 | gitleaks | high | N/A | app/app.py | 32 | GitHub Personal Access Token detected in source code | No |
| FINDING-013 | snyk | critical | CWE-400 | Werkzeug (2.0.1) | N/A | Duplicate of FINDING-009 via different scanner | Yes |
| FINDING-014 | semgrep | high | CWE-22 | app/app.py | 121 | Path traversal — open() called with unsanitised user input | No |
```

---

## Relatório CSV

```csv
id,tool,severity,cwe,file,line,description,false_positive
FINDING-001,semgrep,high,CWE-89,app/app.py,74,SQL injection via string formatting,False
FINDING-002,semgrep,high,CWE-78,app/app.py,112,OS command injection via shell=True,False
FINDING-003,snyk,critical,CWE-20,PyYAML (5.3.1),,Arbitrary Code Execution via yaml.load(),False
FINDING-004,semgrep,medium,CWE-502,app/app.py,126,Insecure deserialisation using pickle,False
FINDING-005,snyk,high,CWE-79,lxml (4.6.2),,XSS via lxml clean module,False
FINDING-006,trivy,medium,N/A,requests (2.25.0),,Proxy-Authorization header forwarded to destination,False
FINDING-007,semgrep,medium,CWE-798,app/app.py,32,Hardcoded API token detected,False
FINDING-008,semgrep,info,N/A,app/app.py,44,FIXME comment found — resolve before merging,True
FINDING-009,snyk,critical,CWE-400,Werkzeug (2.0.1),,Resource exhaustion via crafted multipart form data,False
FINDING-010,owasp-dep-check,low,CWE-20,Flask (2.0.1),,Open redirect in specific configurations,True
FINDING-011,semgrep,info,CWE-94,app/app.py,36,Flask DEBUG mode enabled in source code,False
FINDING-012,gitleaks,high,N/A,app/app.py,32,GitHub Personal Access Token detected in source code,False
FINDING-013,snyk,critical,CWE-400,Werkzeug (2.0.1),,Duplicate of FINDING-009 via different scanner,True
FINDING-014,semgrep,high,CWE-22,app/app.py,121,Path traversal — open() called with unsanitised user input,False
```

---

## Notas

- **FINDING-008** → FP: Comentário FIXME informacional; sem impacto de segurança.
- **FINDING-010** → FP: O scanner detectou as próprias fixtures de teste do Flask
  (uma string "debug" no código da biblioteca), não uma configuração incorreta no código do usuário.
- **FINDING-013** → FP / Duplicata: Mesmo CVE e pacote que FINDING-009;
  apenas um deve aparecer em um relatório sem duplicatas.
- **FINDING-011** → Verdadeiro Positivo: O modo Debug está definido em `app.py` linha 36 via
  `app.config["DEBUG"] = True`. Embora a severidade seja INFO, é um achado real
  no código do usuário.
