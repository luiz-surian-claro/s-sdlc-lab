# Challenge 2 — False Positive Identification and Justification

## Objective

Analyse the SCA scan results in `data/sca_results.json` and the mixed scan
results in `data/mixed_scan_results.json`. Identify false positives, justify
your decisions, and explain the risks of misclassifying findings.

---

## Background

Security scanners generate a large volume of findings. Not all findings
represent real, exploitable vulnerabilities. A skilled security analyst must:

- Distinguish **true positives** from **false positives**
- Understand the difference between a vulnerability in a library and a
  vulnerability that is **reachable** in the application
- Communicate findings clearly to developers and stakeholders

---

## Findings Under Review

The `data/sca_results.json` file contains a `false_positives_candidates`
array with three entries:

| ID | Package | Finding | Severity Reported |
|----|---------|---------|-------------------|
| FP-001 | Flask 2.0.1 | Debug mode symbols in binary scan | HIGH |
| FP-002 | requests 2.25.0 | verify=False detected | CRITICAL |
| AMBIGUOUS-001 | PyYAML 5.3.1 | yaml.load() without Loader | CRITICAL |

---

## Your Tasks

### Task 2.1 — Classify each candidate

For each of the three candidates above, provide:

1. **Classification**: True Positive | False Positive | Ambiguous
2. **Justification** (≥3 sentences): Explain your reasoning using technical
   evidence from the scan data and the application code.
3. **Risk of misclassification**: What happens if this finding is
   incorrectly dismissed? Or incorrectly escalated?
4. **Recommended action**: Fix, Accept Risk, Monitor, or No Action — and why.

### Task 2.2 — Identify additional false positives

Review `data/mixed_scan_results.json` and identify any findings you consider
to be false positives beyond the labelled candidates.

For each additional false positive you identify, provide the same four-point
analysis as in Task 2.1.

### Task 2.3 — Define a false-positive policy

Write a brief (200–400 words) false-positive triage policy for your
organisation. Include:

- Criteria for classifying a finding as a false positive
- Required evidence/documentation
- Approval process (who signs off?)
- Review cadence (how often are FP decisions re-evaluated?)

---

## Deliverables

- A Markdown file `challenge_02_false_positives.md` with your analysis

---

## Evaluation Criteria

| Criterion | Weight |
|-----------|--------|
| Correct classification of FP-001 and FP-002 (obvious FPs) | 20 % |
| Nuanced analysis of AMBIGUOUS-001 | 25 % |
| Additional FPs identified in mixed results | 25 % |
| Quality of the false-positive policy | 30 % |

---

## Hints

- Read the `analyst_note` fields — they contain context but not the answer.
- Think about **reachability**: a vulnerable code path that is never called
  is different from one that is directly exposed.
- Think about **scanner limitations**: pattern-matching tools have
  well-known sources of noise.
- Consider the **business impact** of both under-reporting and over-reporting.

---

## References

- [OWASP False Positives](https://owasp.org/www-community/vulnerabilities/False_Positives)
- [CVE-2020-14343 (PyYAML)](https://nvd.nist.gov/vuln/detail/CVE-2020-14343)
- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
