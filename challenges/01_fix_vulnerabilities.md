# Challenge 1 — Fix Vulnerable Code (SAST Findings)

## Objective

Analyse the SAST results provided in `data/sast_results.json` and fix the
corresponding vulnerabilities in `app/app.py`.

---

## Background

You have been provided with the output of a **Semgrep** static analysis scan
against the Flask application in `/app`. The scan identified several
security issues across multiple OWASP Top 10 categories.

---

## Your Tasks

### Task 1.1 — Triage the SAST findings

Review `data/sast_results.json` and complete the following table in your
submission:

| Finding ID | Rule | Severity | CWE | File | Line | Assessment (Real / FP) | Priority |
| ---------- | ---- | -------- | --- | ---- | ---- | ---------------------- | -------- |
| … | … | … | … | … | … | … | … |

### Task 1.2 — Fix the vulnerabilities

For each **real** vulnerability you identified, implement a fix in `app/app.py`.

Minimum required fixes:

1. **SQL Injection (CWE-89)** — Replace string-formatted queries with
   parameterised queries using the `?` placeholder.

2. **OS Command Injection (CWE-78)** — Refactor the `/ping` endpoint to avoid
   passing user input to a shell command. Consider using `subprocess` with a
   list of arguments and `shell=False`.

3. **Hardcoded Secrets (CWE-798)** — Move all credentials and tokens to
   environment variables or a secrets manager. Remove them from source code.

4. **Path Traversal (CWE-22)** — Validate and sanitise the `name` parameter
   in the `/file` endpoint. Restrict access to a specific safe directory.

5. **Insecure Deserialisation (CWE-502)** — Replace `pickle` with a safe
   alternative such as JSON or a validated data schema.

6. **Weak Cryptography (CWE-327)** — Replace MD5 with a password-hashing
   algorithm (e.g., `bcrypt` or `argon2`).

---

## Deliverables

- Updated `app/app.py` with all fixes applied
- A brief write-up (`challenge_01_findings.md`) explaining:
  - The vulnerability
  - The impact
  - The fix you applied
  - The CWE and OWASP category

---

## Evaluation Criteria

| Criterion | Weight |
| --------- | ------ |
| Correct identification of all vulnerabilities | 20 % |
| Quality and completeness of fixes | 40 % |
| Explanation of impact | 20 % |
| Code quality of the fixed code | 20 % |

---

## References

- [OWASP Top 10](https://owasp.org/Top10/)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [CWE-78: OS Command Injection](https://cwe.mitre.org/data/definitions/78.html)
- [CWE-22: Path Traversal](https://cwe.mitre.org/data/definitions/22.html)
- [CWE-502: Insecure Deserialisation](https://cwe.mitre.org/data/definitions/502.html)
- [CWE-327: Weak Cryptography](https://cwe.mitre.org/data/definitions/327.html)
- [CWE-798: Hardcoded Credentials](https://cwe.mitre.org/data/definitions/798.html)
