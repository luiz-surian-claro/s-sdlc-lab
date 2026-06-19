# Sample Expected Output — vulnerability_parser.py

This file shows a **reference output** from a complete implementation of
`scripts/vulnerability_parser.py` against `data/mixed_scan_results.json`.

Use this to validate your parser's output. Minor differences in wording are
acceptable; the classification and normalised fields should match.

---

## Markdown Report

```markdown
## Vulnerability Report

Generated: 2024-11-15
Input: data/mixed_scan_results.json
Total findings: 14 | True Positives: 10 | False Positives: 4

### Summary

| Severity | Count (TP) |
| -------- | ---------- |
| critical | 2 |
| high     | 4 |
| medium   | 3 |
| low      | 1 |
| info     | 2 (FP) |

---

### Findings

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

## CSV Report

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

## Notes

- **FINDING-008** → FP: Informational FIXME comment; no security impact.
- **FINDING-010** → FP: The scanner matched Flask's own test fixtures
  (a "debug" string in library code), not user-code misconfiguration.
- **FINDING-013** → FP / Duplicate: Same CVE and package as FINDING-009;
  only one should appear in a de-duplicated report.
- **FINDING-011** → True Positive: Debug mode is set in `app.py` line 36 via
  `app.config["DEBUG"] = True`. Although the severity is INFO, it is a real
  finding in user code.
