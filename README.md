# S-SDLC Lab — DevSecOps Security Playground

> **Technical Assessment for Senior IT Security Analyst candidates**

This repository is a self-contained DevSecOps assessment environment that
simulates real-world scenarios involving Secure SDLC, CI/CD pipeline security,
and vulnerability management.

---

## Repository Structure

```
s-sdlc-lab/
├── app/                        # Vulnerable Flask application
│   ├── app.py                  # Application source code (contains intentional vulnerabilities)
│   ├── requirements.txt        # Python dependencies (some outdated/vulnerable)
│   └── README.md               # App-level documentation
│
├── data/                       # Vulnerability scan results
│   ├── sast_results.json       # Semgrep SAST output
│   ├── sca_results.json        # Snyk SCA output (includes FP candidates)
│   ├── mixed_scan_results.json # Multi-tool results (inconsistent schema — parsing challenge)
│   └── expected_output_sample.md  # Reference output for the parsing challenge
│
├── scripts/
│   └── vulnerability_parser.py # Skeleton script — candidate must complete
│
├── ci-cd/
│   └── pipeline.yml            # GitHub Actions workflow (contains misconfigurations)
│
├── challenges/
│   ├── 01_fix_vulnerabilities.md
│   ├── 02_false_positive_validation.md
│   ├── 03_secure_code_review.md
│   ├── 04_cicd_security.md
│   └── 05_json_parsing.md
│
├── SCORING.md                  # Evaluator-only scoring rubric
└── README.md                   # This file
```

---

## Assessment Overview

The assessment consists of **five challenges** that evaluate different
DevSecOps competencies. Candidates are expected to complete all five
challenges within the agreed time window.

| # | Challenge | Key Skills |
|---|-----------|-----------|
| 1 | Fix Vulnerable Code | SAST triage, secure coding |
| 2 | False Positive Validation | Analyst judgement, risk assessment |
| 3 | Secure Code Review | Manual review, dependency analysis |
| 4 | CI/CD Security | Pipeline hardening, secrets management |
| 5 | JSON Parsing | Scripting, data normalisation |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Git

### Set-up

```bash
# Clone the repository
git clone https://github.com/luiz-surian-claro/s-sdlc-lab.git
cd s-sdlc-lab

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install application dependencies
pip install -r app/requirements.txt
```

### Running the Application

```bash
cd app
python app.py
```

The application starts on `http://localhost:5000`.

> ⚠️ **Warning**: This application contains intentional security
> vulnerabilities. **Never deploy it in a production environment.**

---

## Challenges

Work through each challenge in order. Instructions are in the `/challenges`
directory.

### Challenge 1 — Fix Vulnerable Code
📄 [`challenges/01_fix_vulnerabilities.md`](challenges/01_fix_vulnerabilities.md)

Analyse SAST findings in `data/sast_results.json` and fix the corresponding
vulnerabilities in `app/app.py`. Covers: SQL injection, command injection,
path traversal, insecure deserialisation, weak cryptography, hardcoded secrets.

### Challenge 2 — False Positive Validation
📄 [`challenges/02_false_positive_validation.md`](challenges/02_false_positive_validation.md)

Review the SCA results in `data/sca_results.json` and identify true positives,
false positives, and ambiguous findings. Justify each decision. Write a
false-positive triage policy.

### Challenge 3 — Secure Code Review
📄 [`challenges/03_secure_code_review.md`](challenges/03_secure_code_review.md)

Perform a manual secure code review of `app/app.py` and `app/requirements.txt`.
Document all findings and implement fixes.

### Challenge 4 — CI/CD Security
📄 [`challenges/04_cicd_security.md`](challenges/04_cicd_security.md)

Review `ci-cd/pipeline.yml` for security misconfigurations. Produce a hardened
version and document your findings.

### Challenge 5 — JSON Parsing
📄 [`challenges/05_json_parsing.md`](challenges/05_json_parsing.md)

Complete `scripts/vulnerability_parser.py` to parse `data/mixed_scan_results.json`
and produce a normalised vulnerability report in CSV and/or Markdown.

---

## Deliverables

Submit the following as a pull request or zip archive:

| File | Challenge |
|------|-----------|
| `app/app.py` (fixed) | 1, 3 |
| `challenge_01_findings.md` | 1 |
| `challenge_02_false_positives.md` | 2 |
| `challenge_03_code_review.md` | 3 |
| `challenge_03_threat_model.md` *(optional)* | 3 |
| `ci-cd/pipeline_hardened.yml` | 4 |
| `challenge_04_cicd.md` | 4 |
| `scripts/vulnerability_parser.py` (completed) | 5 |
| `report.md` and/or `report.csv` | 5 |
| `scripts/test_parser.py` *(optional)* | 5 |

---

## Evaluation Criteria

Candidates are assessed on:

| Dimension | Description |
|-----------|-------------|
| **Technical depth** | Depth of vulnerability analysis beyond tool output |
| **Accuracy** | Correctness of classifications and fixes |
| **Reasoning** | Quality of justifications for decisions |
| **Code quality** | Readability, security, and correctness of written/fixed code |
| **Communication** | Clarity of written deliverables |

The maximum score is **100 points** (plus up to 10 bonus points).
See [`SCORING.md`](SCORING.md) for the full rubric *(evaluator only)*.

---

## OWASP References

The vulnerabilities in this lab are based on the
[OWASP Top 10 (2021)](https://owasp.org/Top10/):

| OWASP Category | Covered In |
|----------------|-----------|
| A01 — Broken Access Control | Path Traversal (app.py) |
| A02 — Cryptographic Failures | MD5 password hashing (app.py) |
| A03 — Injection | SQLi, XSS, Command Injection (app.py) |
| A05 — Security Misconfiguration | Debug mode, 0.0.0.0 binding, CI/CD |
| A06 — Vulnerable Components | Outdated dependencies (requirements.txt) |
| A07 — Auth Failures | Hardcoded credentials (app.py, pipeline.yml) |
| A08 — Software Integrity Failures | Insecure deserialisation (app.py) |

---

## Time Estimate

| Challenge | Estimated Time |
|-----------|---------------|
| Challenge 1 | 45–60 min |
| Challenge 2 | 30–45 min |
| Challenge 3 | 60–90 min |
| Challenge 4 | 45–60 min |
| Challenge 5 | 60–90 min |
| **Total** | **4–6 hours** |

---

## Notes for Candidates

- Read each challenge file carefully before starting.
- The `TODO (CANDIDATE):` comments in source files are hints — they do not
  tell you the full picture.
- Do not search for the `SCORING.md` file until after you submit your work.
- You may use any tools (Semgrep, pip-audit, Bandit, etc.) to assist your
  analysis, but you must be able to explain every finding and fix.
- Quality of reasoning matters more than the number of findings.

---

*Good luck! 🔐*
