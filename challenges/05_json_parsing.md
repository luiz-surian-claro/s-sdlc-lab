# Challenge 5 — JSON Parsing & Vulnerability Report Generation

## Objective

Complete `scripts/vulnerability_parser.py` to parse `data/mixed_scan_results.json`
and produce a normalised vulnerability report in CSV and/or Markdown format.

---

## Background

Vulnerability data from different security tools often arrives in inconsistent
formats. A real-world security engineer must be able to:

- Parse and normalise heterogeneous JSON data
- Apply business rules to filter noise (false positives, duplicates)
- Generate actionable reports for different audiences

---

## Input File

`data/mixed_scan_results.json` contains 14 findings from four different
scanners: **Semgrep**, **Snyk**, **Trivy**, and **OWASP Dependency Check**
(mock), and **Gitleaks**.

The file is **intentionally inconsistent**. Field names, severity labels, and
data structures vary across scanners. Examples:

| Scanner A | Scanner B | Scanner C | Canonical Field |
| --------- | --------- | --------- | --------------- |
| `id` | `finding_id` | `ref` | `id` |
| `source` | `tool` | `scanner` | `tool` |
| `severity` | `Risk` | `level` | `severity` |
| `file` | `filepath` | `location.path` | `file` |
| `line` | `line_number` | `location.start_line` | `line` |
| `message` | `description` | `details` | `description` |
| `cwe` (string) | `cwe_id` | `cwe` (list) | `cwe` |

---

## Your Tasks

### Task 5.1 — Implement the Parser

Complete the `TODO` sections in `scripts/vulnerability_parser.py`:

1. **`extract_field()`** — try multiple candidate field names, handle nested
   paths (e.g., `location.path`), and return a default if none match.

2. **`normalise_severity()`** — map any raw severity string (e.g., `"ERROR"`,
   `"Risk: HIGH"`, `"critical"`) to one of:
   `critical | high | medium | low | info`.

3. **`normalise_finding()`** — map each raw finding to the canonical schema:

   ```python
   {
     "id":            str,
     "tool":          str,
     "severity":      str,   # canonical
     "cwe":           str,   # first value if list; "N/A" if None
     "file":          str,   # file path or package name
     "line":          int | None,
     "description":   str,
     "false_positive": bool,
   }
   ```

4. **`apply_fp_rules()`** — implement at least 3 false-positive rules:
   - Explicit `false_positive=true` flag from scanner
   - Informational/low-severity FIXME comments (low value noise)
   - Duplicate findings (same package/CVE or same file/line/CWE)
   - (Optional) Any additional rule you define

5. **`to_csv()`** — generate a valid CSV with a header row.

6. **`to_markdown()`** — generate a Markdown table.

7. **`main()`** — wire everything together; handle errors gracefully.

### Task 5.2 — Handle Edge Cases

Your parser must not crash on:

- Missing or `null` fields
- Unexpected field types (e.g., `cwe` as a list vs. a string)
- Duplicate findings
- Findings with no `id`

### Task 5.3 — Output a Report

Run your completed parser and produce two output files:

```bash
python scripts/vulnerability_parser.py \
    --input  data/mixed_scan_results.json \
    --output report.md \
    --format markdown

python scripts/vulnerability_parser.py \
    --input  data/mixed_scan_results.json \
    --output report.csv \
    --format csv
```

---

## Expected Output (Sample)

Your Markdown report should look similar to:

```markdown
| ID | Tool | Severity | CWE | File | Line | Description | FP |
| -- | ---- | -------- | --- | ---- | ---- | ----------- | -- |
| FINDING-001 | semgrep | high | CWE-89 | app/app.py | 74 | SQL injection via string formatting | No |
| FINDING-002 | semgrep | high | CWE-78 | app/app.py | 112 | OS command injection via shell=True | No |
| FINDING-008 | semgrep | info | N/A | app/app.py | 44 | FIXME comment found | Yes |
| … | … | … | … | … | … | … | … |
```

---

## Bonus Tasks

- Add a `--filter-severity` flag that excludes findings below a given
  severity level (e.g., `--filter-severity high` keeps only critical and high)
- Generate a summary section at the top of the report showing counts by
  severity and false-positive status
- Write unit tests for `normalise_severity()` and `extract_field()`

---

## Deliverables

- `scripts/vulnerability_parser.py` — completed implementation
- `report.md` and/or `report.csv` — output from your parser
- (Optional) `scripts/test_parser.py` — unit tests

---

## Evaluation Criteria

| Criterion | Weight |
| --------- | ------ |
| Correct normalisation of all 14 findings | 30 % |
| Robustness (no crashes on malformed data) | 20 % |
| Accuracy of false-positive classification | 25 % |
| Code quality (readability, typing, error handling) | 25 % |

---

## References

- [Python `csv` module](https://docs.python.org/3/library/csv.html)
- [Python `json` module](https://docs.python.org/3/library/json.html)
- [Python `argparse` module](https://docs.python.org/3/library/argparse.html)
- [Semgrep SARIF output](https://semgrep.dev/docs/semgrep-ci/findings/)
- [Snyk JSON output format](https://docs.snyk.io/snyk-cli/scan-and-maintain-projects-using-the-cli/snyk-cli-for-open-source/output-formats-for-snyk-test)
