# Challenge 3 — Secure Code Review

## Objective

Perform a thorough secure code review of `app/app.py` and `app/requirements.txt`.
Document all findings, classify them by severity and CWE, and implement fixes.

---

## Background

Secure code review is one of the most valuable activities in a Secure SDLC.
Unlike automated scanners, a human reviewer can:

- Identify **logic flaws** that tools miss
- Understand **context** (is the vulnerable path reachable? is input trusted?)
- Catch **design-level** weaknesses, not just implementation bugs
- Evaluate **defence-in-depth** and adherence to the principle of least privilege

---

## Scope

| File | In Scope |
| ---- | -------- |
| `app/app.py` | Yes — full review |
| `app/requirements.txt` | Yes — dependency review |
| `ci-cd/pipeline.yml` | No — covered in Challenge 4 |

---

## Your Tasks

### Task 3.1 — Produce a Code Review Report

Examine `app/app.py` line by line. For every security issue you find, create
an entry in your report with the following fields:

| Field | Description |
| ----- | ----------- |
| **ID** | Unique identifier (e.g. CR-001) |
| **File** | File name and line number |
| **Vulnerability** | Short name (e.g. "SQL Injection") |
| **CWE** | CWE identifier |
| **OWASP** | OWASP Top 10 category |
| **Severity** | Critical / High / Medium / Low / Info |
| **Description** | Technical description of the issue |
| **Impact** | What could an attacker achieve? |
| **Fix** | Proposed remediation |

**Minimum: report at least 8 distinct findings.**

### Task 3.2 — Dependency Review

Using `app/requirements.txt`, identify all dependencies with known
vulnerabilities. For each:

- State the package, version, and CVE(s)
- Describe the vulnerability
- State the patched version and whether it is a breaking change
- Assess whether the vulnerability is **reachable** given the application's
  current use of the library

Tools you may use: `pip-audit`, `safety`, `snyk test`, or manual CVE research.

### Task 3.3 — Implement Fixes

Apply fixes for the following issues (at minimum):

1. Replace all SQL injection points with parameterised queries
2. Remove all hardcoded secrets; use `os.environ` or a secrets manager
3. Fix the command injection in `/ping`
4. Add input validation and path sanitisation to `/file`
5. Replace insecure pickle deserialisation with a safe alternative
6. Replace MD5 password hashing with bcrypt or argon2
7. Disable debug mode; bind only to localhost in non-production environments

### Task 3.4 — Threat Model (Optional Bonus)

Create a brief STRIDE threat model for the `/login` endpoint. Identify at
least one threat per STRIDE category and propose a mitigation.

---

## Deliverables

- Updated `app/app.py` with all fixes applied
- `challenge_03_code_review.md` — your review report (Tasks 3.1 and 3.2)
- (Optional) `challenge_03_threat_model.md` — STRIDE analysis

---

## Evaluation Criteria

| Criterion | Weight |
| --------- | ------ |
| Number and accuracy of findings | 30 % |
| Quality of impact analysis | 20 % |
| Quality and completeness of fixes | 30 % |
| Dependency review accuracy | 20 % |

---

## What Makes a Good Secure Code Review?

A strong review:

- Prioritises findings by **actual risk**, not just CVSS score
- Considers the **threat model** (who is the attacker? what is their access?)
- Goes beyond scanner output to find **logic and design flaws**
- Proposes **practical fixes** that do not break functionality
- Notes what the application does **well** (not all feedback is negative)

---

## References

- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/)
- [OWASP Top 10 Proactive Controls](https://owasp.org/www-project-proactive-controls/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Python Security Best Practices](https://snyk.io/blog/python-security-best-practices-cheat-sheet/)
