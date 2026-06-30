# Desafio 1 — Corrigir Código Vulnerável (Achados de SAST)

## Objetivo

Analise os resultados de SAST disponíveis em `data/sast_results.json` e corrija
as vulnerabilidades correspondentes em `app/app.py`.

---

## Contexto

Você recebeu a saída de uma varredura de análise estática do **Semgrep** contra
a aplicação Flask em `/app`. A varredura identificou vários problemas de
segurança em múltiplas categorias do OWASP Top 10.

---

## Suas Tarefas

### Tarefa 1.1 — Triagem dos achados de SAST

Revise `data/sast_results.json` e preencha a tabela a seguir na sua submissão:

| ID do Achado | Regra | Severidade | CWE | Arquivo | Linha | Avaliação (Real / FP) | Prioridade |
| ------------ | ----- | ---------- | --- | ------- | ----- | --------------------- | ---------- |
| … | … | … | … | … | … | … | … |

### Tarefa 1.2 — Corrigir as vulnerabilidades

Para cada vulnerabilidade **real** identificada, implemente uma correção em `app/app.py`.

Correções mínimas obrigatórias:

1. **Injeção de SQL (CWE-89)** — Substitua queries com interpolação de string
   por queries parametrizadas usando o placeholder `?`.

2. **Injeção de Comando no SO (CWE-78)** — Refatore o endpoint `/ping` para evitar
   a passagem de entrada do usuário para um comando shell. Considere usar `subprocess`
   com uma lista de argumentos e `shell=False`.

3. **Segredos Hardcoded (CWE-798)** — Mova todas as credenciais e tokens para
   variáveis de ambiente ou um gerenciador de segredos. Remova-os do código-fonte.

4. **Path Traversal (CWE-22)** — Valide e sanitize o parâmetro `name`
   no endpoint `/file`. Restrinja o acesso a um diretório seguro específico.

5. **Desserialização Insegura (CWE-502)** — Substitua `pickle` por uma
   alternativa segura, como JSON ou um esquema de dados validado.

6. **Criptografia Fraca (CWE-327)** — Substitua MD5 por um algoritmo de hash
   de senhas (por exemplo, `bcrypt` ou `argon2`).

---

## Entregáveis

- `app/app.py` atualizado com todas as correções aplicadas
- Um breve relatório (`challenge_01_findings.md`) explicando:
  - A vulnerabilidade
  - O impacto
  - A correção aplicada
  - O CWE e a categoria OWASP

---

## Critérios de Avaliação

| Critério | Peso |
| -------- | ---- |
| Identificação correta de todas as vulnerabilidades | 20% |
| Qualidade e completude das correções | 40% |
| Explicação do impacto | 20% |
| Qualidade do código corrigido | 20% |

---

## Referências

- [OWASP Top 10](https://owasp.org/Top10/)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [CWE-78: OS Command Injection](https://cwe.mitre.org/data/definitions/78.html)
- [CWE-22: Path Traversal](https://cwe.mitre.org/data/definitions/22.html)
- [CWE-502: Insecure Deserialisation](https://cwe.mitre.org/data/definitions/502.html)
- [CWE-327: Weak Cryptography](https://cwe.mitre.org/data/definitions/327.html)
- [CWE-798: Hardcoded Credentials](https://cwe.mitre.org/data/definitions/798.html)
