# Scoring Rubric — DevSecOps Security Playground

This rubric is intended for the **evaluator**. Do not share with candidates
before the assessment is complete.

---

## Total Score: 100 points

| Challenge | Max Points |
|-----------|-----------|
| Challenge 1 — Fix Vulnerable Code | 25 |
| Challenge 2 — False Positive Validation | 20 |
| Challenge 3 — Secure Code Review | 20 |
| Challenge 4 — CI/CD Security | 20 |
| Challenge 5 — JSON Parsing | 15 |
| **Total** | **100** |

---

## Challenge 1 — Fix Vulnerable Code (25 points)

### 1.1 Vulnerability Identification (10 points)

| Finding | Points |
|---------|--------|
| SQL Injection (login) | 1.5 |
| SQL Injection (register) | 1.5 |
| OS Command Injection (ping) | 2 |
| Hardcoded API token | 1 |
| Hardcoded DB password | 1 |
| Path Traversal (file) | 1.5 |
| Insecure deserialisation (pickle) | 1 |
| Weak crypto (MD5 passwords) | 1 |
| Debug mode enabled + 0.0.0.0 binding | 0.5 |
| **Subtotal** | **11** *(award up to 10 max)* |

### 1.2 Quality of Fixes (10 points)

| Fix | Points |
|-----|--------|
| Parameterised queries (both endpoints) | 2 |
| shell=False + arg list for ping | 2 |
| Secrets moved to env variables | 2 |
| Path sanitisation (os.path.realpath + prefix check) | 2 |
| pickle replaced with safe alternative | 1 |
| MD5 replaced with bcrypt/argon2 | 1 |

### 1.3 Write-up Quality (5 points)

- **5**: All findings documented with CWE, impact, and clear remediation
- **3–4**: Most findings documented; minor gaps
- **1–2**: Partial documentation; missing impact analysis
- **0**: No write-up submitted

---

## Challenge 2 — False Positive Validation (20 points)

### 2.1 FP-001 Classification (4 points)

**Expected answer**: False Positive

- **4**: Correctly classified as FP with clear technical justification (scanner matched debug symbols in library binary, not user code)
- **2–3**: Correct classification, weak justification
- **1**: Incorrect classification with partial understanding
- **0**: Incorrect classification, no justification

### 2.2 FP-002 Classification (4 points)

**Expected answer**: False Positive

- **4**: Correctly classified as FP; identified that the match was in the library's test suite, not application code
- **2–3**: Correct classification, weak justification
- **1**: Incorrect classification with partial understanding
- **0**: Incorrect with no justification

### 2.3 AMBIGUOUS-001 Classification (6 points)

**Expected answer**: Ambiguous — technically a FP (dead code), but should be flagged for remediation

- **6**: Recognises the nuance — the yaml.load() call is in dead code so it is not directly exploitable, but the dead code should be removed; recommends clean-up rather than accept/ignore
- **4–5**: Identifies ambiguity; recommends action
- **2–3**: Classified as one extreme (clear TP or clear FP) with reasonable but incomplete reasoning
- **0–1**: Misclassified with poor justification

### 2.4 Additional FPs from mixed_scan_results.json (3 points)

**Expected FPs**: FINDING-008 (FIXME comment — INFO, no security impact), FINDING-010 (debug string in Flask test fixtures), FINDING-013 (duplicate of FINDING-009)

- **3**: Identifies at least 2 additional FPs with justification
- **2**: Identifies 1 additional FP with justification
- **1**: Attempts identification but with weak reasoning
- **0**: None identified

### 2.5 False-Positive Policy (3 points)

- **3**: Policy includes criteria, evidence requirements, approval process, and review cadence
- **2**: Policy covers most elements; missing one
- **1**: Partial policy; missing two or more elements
- **0**: No policy submitted

---

## Challenge 3 — Secure Code Review (20 points)

### 3.1 Findings Report (10 points)

**Expected minimum findings (8):**

| Finding | Points |
|---------|--------|
| SQL injection (login) | 1 |
| SQL injection (register) | 1 |
| XSS (search) | 1 |
| Command injection (ping) | 1 |
| Path traversal (file) | 1 |
| Insecure deserialisation | 1 |
| Hardcoded credentials / token | 1 |
| MD5 password hashing | 1 |
| Plain-text password storage (register) | 0.5 |
| Debug mode + 0.0.0.0 binding | 0.5 |
| Missing input validation (register) | 0.5 |

Award up to 10 points.

### 3.2 Dependency Review (5 points)

- **5**: All 8+ vulnerable packages identified with CVEs, impact, fix versions, and reachability analysis
- **3–4**: Most packages identified; minor gaps
- **1–2**: Fewer than 4 packages identified
- **0**: Not attempted

### 3.3 Fixes Applied (5 points)

Same as Challenge 1 — fixes evaluated holistically here if Challenge 1 was not submitted.

---

## Challenge 4 — CI/CD Security (20 points)

### 4.1 Misconfigurations Identified (10 points)

**Expected misconfigurations (8+):**

| Misconfiguration | Points |
|-----------------|--------|
| Hardcoded SEMGREP_APP_TOKEN in env | 1.5 |
| Hardcoded SNYK_TOKEN in env | 1.5 |
| DEPLOY_KEY hardcoded in step env | 2 |
| continue-on-error: true on SAST/SCA | 1.5 |
| `|| true` suppresses test failures | 1 |
| No permissions block (GITHUB_TOKEN over-permissioned) | 1 |
| Trigger on all branches (`"*"`) | 0.5 |
| No manual approval gate before production deploy | 1 |
| Actions not pinned to SHA | 0.5 |

Award up to 10 points.

### 4.2 Hardened Pipeline (7 points)

- **7**: All 8 required improvements implemented; pipeline is functional
- **5–6**: Most improvements implemented; 1–2 gaps
- **3–4**: Core improvements (secrets, permissions, gates) implemented; others missing
- **1–2**: Partial improvements with significant gaps
- **0**: Not attempted

### 4.3 Discussion Questions (3 points)

- **3**: All three questions answered thoughtfully with specific recommendations
- **2**: Two questions answered well
- **1**: Superficial answers
- **0**: Not attempted

---

## Challenge 5 — JSON Parsing (15 points)

### 5.1 Parser Implementation (10 points)

| Component | Points |
|-----------|--------|
| `extract_field()` — handles all variant field names and nested paths | 2 |
| `normalise_severity()` — handles all raw formats without error | 2 |
| `normalise_finding()` — all 14 findings normalised correctly | 3 |
| `apply_fp_rules()` — at least 3 rules implemented correctly | 2 |
| `to_csv()` and/or `to_markdown()` — valid output format | 1 |

### 5.2 Robustness (3 points)

- **3**: No crashes on missing/null fields, unexpected types, duplicates
- **2**: Handles most edge cases; 1–2 crashes on edge cases
- **1**: Basic error handling only
- **0**: Parser crashes on multiple inputs

### 5.3 False-Positive Classification Accuracy (2 points)

- **2**: FINDING-008, FINDING-010, and FINDING-013 correctly flagged as FP
- **1**: 1–2 correctly flagged
- **0**: None correctly flagged

---

## Scoring Bands

| Score | Band | Interpretation |
|-------|------|----------------|
| 90–100 | **Exceptional** | Ready for senior role; demonstrates deep expertise |
| 75–89  | **Strong** | Solid skills; minor gaps that can be closed quickly |
| 60–74  | **Adequate** | Meets baseline requirements; needs mentoring in some areas |
| 45–59  | **Developing** | Foundational knowledge present; significant skill gaps |
| < 45   | **Below Threshold** | Not suitable for a Senior IT Security Analyst role at this time |

---

## Bonus Points (up to 10 additional points)

| Bonus | Points |
|-------|--------|
| STRIDE threat model for `/login` (Challenge 3) | 3 |
| `--filter-severity` CLI flag in parser (Challenge 5) | 1 |
| Summary section in parser output (Challenge 5) | 1 |
| Unit tests for parser (Challenge 5) | 2 |
| Additional security improvements beyond required (any challenge) | up to 3 |

---

## Evaluator Notes

- Deduct points if fixes introduce new vulnerabilities
- Award partial credit generously where reasoning is sound even if the
  conclusion differs from the expected answer
- The AMBIGUOUS-001 case has no single correct answer; evaluate the **quality
  of reasoning**, not the classification alone
- A candidate who correctly identifies a finding not listed in this rubric
  should receive credit for it
