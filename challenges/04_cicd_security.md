# Challenge 4 — CI/CD Security Pipeline Improvement

## Objective

Review the GitHub Actions pipeline in `ci-cd/pipeline.yml`, identify all
security misconfigurations, and propose (and implement) a hardened version.

---

## Background

CI/CD pipelines are a critical attack surface in modern DevSecOps environments.
Misconfigured pipelines can:

- Leak secrets to build logs or third-party services
- Allow supply-chain attacks via unpinned actions
- Execute malicious code injected via pull requests
- Deploy vulnerable or untested code to production

---

## Findings to Look For

The pipeline in `ci-cd/pipeline.yml` contains at least **eight** intentional
misconfigurations. Your task is to find them all.

Hint categories (not ordered):

- Secrets handling
- Permissions
- Security gate logic
- Trigger configuration
- Action pinning
- Error suppression
- Environment isolation
- Deployment controls

---

## Your Tasks

### Task 4.1 — Enumerate Misconfigurations

Review `ci-cd/pipeline.yml` and list every misconfiguration you find.
For each, provide:

| Field | Description |
|-------|-------------|
| **ID** | Unique identifier (e.g. PL-001) |
| **Location** | Job name and line number |
| **Issue** | Short description |
| **Risk** | What could an attacker do? |
| **Severity** | Critical / High / Medium / Low |
| **Fix** | Proposed remediation |

**Minimum: identify at least 6 distinct misconfigurations.**

### Task 4.2 — Implement a Hardened Pipeline

Create `ci-cd/pipeline_hardened.yml` — a corrected version of the pipeline.

Your hardened pipeline **must**:

1. **Pin all actions** to a specific commit SHA (not just a tag) to prevent
   supply-chain attacks.

2. **Use GitHub Secrets** for all tokens (`SEMGREP_APP_TOKEN`, `SNYK_TOKEN`,
   `DEPLOY_KEY`, etc.).

3. **Set least-privilege permissions** using the `permissions` block at the
   top level and/or per job.

4. **Fail the pipeline** when SAST or SCA tools detect findings above a
   configurable severity threshold (do not use `continue-on-error: true`).

5. **Require manual approval** before deploying to production using GitHub
   Environments with protection rules.

6. **Remove error suppression** (`|| true`) from test commands.

7. **Scope the trigger** to only relevant branches (e.g., `main`, `develop`,
   `release/**`).

8. **Add a dependency integrity check** (e.g., `pip install --require-hashes`
   or a lock file).

### Task 4.3 — Security Gate Design (Discussion)

Answer the following questions in your write-up:

1. At what point in the pipeline should SAST results block a merge?
   What severity threshold would you choose, and why?

2. How would you handle a situation where a critical CVE is found in a
   transitive dependency that has no available fix?

3. What additional security gates would you add to this pipeline beyond
   SAST, SCA, and DAST?

---

## Deliverables

- `ci-cd/pipeline_hardened.yml` — corrected pipeline
- `challenge_04_cicd.md` — findings table and answers to Task 4.3

---

## Evaluation Criteria

| Criterion | Weight |
|-----------|--------|
| Number and accuracy of misconfigurations identified | 30 % |
| Quality and completeness of the hardened pipeline | 40 % |
| Depth of answers to Task 4.3 | 30 % |

---

## References

- [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [OWASP CI/CD Security Top 10](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
- [Securing GitHub Actions — Pinning Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#using-third-party-actions)
- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
