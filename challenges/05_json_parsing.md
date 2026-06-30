# Desafio 5 — Parsing de JSON e Geração de Relatório de Vulnerabilidades

## Objetivo

Complete `scripts/vulnerability_parser.py` para fazer o parsing de
`data/mixed_scan_results.json` e gerar um relatório de vulnerabilidades
normalizado em formato CSV e/ou Markdown.

---

## Contexto

Dados de vulnerabilidades de diferentes ferramentas de segurança frequentemente
chegam em formatos inconsistentes. Um engenheiro de segurança do mundo real precisa:

- Fazer o parsing e normalizar dados JSON heterogêneos
- Aplicar regras de negócio para filtrar ruído (falsos positivos, duplicatas)
- Gerar relatórios acionáveis para diferentes públicos

---

## Arquivo de Entrada

`data/mixed_scan_results.json` contém 14 achados de quatro scanners diferentes:
**Semgrep**, **Snyk**, **Trivy**, **OWASP Dependency Check** (simulado) e **Gitleaks**.

O arquivo é **intencionalmente inconsistente**. Nomes de campos, rótulos de
severidade e estruturas de dados variam entre os scanners. Exemplos:

| Scanner A | Scanner B | Scanner C | Campo Canônico |
| --------- | --------- | --------- | -------------- |
| `id` | `finding_id` | `ref` | `id` |
| `source` | `tool` | `scanner` | `tool` |
| `severity` | `Risk` | `level` | `severity` |
| `file` | `filepath` | `location.path` | `file` |
| `line` | `line_number` | `location.start_line` | `line` |
| `message` | `description` | `details` | `description` |
| `cwe` (string) | `cwe_id` | `cwe` (list) | `cwe` |

---

## Suas Tarefas

### Tarefa 5.1 — Implementar o Parser

Complete as seções `TODO` em `scripts/vulnerability_parser.py`:

1. **`extract_field()`** — tente múltiplos nomes de campo candidatos, trate
   caminhos aninhados (ex.: `location.path`) e retorne um valor padrão se
   nenhum corresponder.

2. **`normalise_severity()`** — mapeie qualquer string de severidade bruta
   (ex.: `"ERROR"`, `"Risk: HIGH"`, `"critical"`) para uma das seguintes:
   `critical | high | medium | low | info`.

3. **`normalise_finding()`** — mapeie cada achado bruto para o schema canônico:

   ```python
   {
     "id":            str,
     "tool":          str,
     "severity":      str,   # canônico
     "cwe":           str,   # primeiro valor se lista; "N/A" se None
     "file":          str,   # caminho do arquivo ou nome do pacote
     "line":          int | None,
     "description":   str,
     "false_positive": bool,
   }
   ```

4. **`apply_fp_rules()`** — implemente pelo menos 3 regras de falso positivo:
   - Flag explícita `false_positive=true` do scanner
   - Comentários FIXME de severidade informacional/baixa (ruído de baixo valor)
   - Achados duplicados (mesmo pacote/CVE ou mesmo arquivo/linha/CWE)
   - (Opcional) Qualquer regra adicional que você definir

5. **`to_csv()`** — gere um CSV válido com linha de cabeçalho.

6. **`to_markdown()`** — gere uma tabela Markdown.

7. **`main()`** — conecte tudo; trate erros de forma graceful.

### Tarefa 5.2 — Tratar Casos de Borda

Seu parser não deve crashar em:

- Campos ausentes ou com valor `null`
- Tipos de campo inesperados (ex.: `cwe` como lista vs. string)
- Achados duplicados
- Achados sem `id`

### Tarefa 5.3 — Gerar um Relatório

Execute seu parser completo e produza dois arquivos de saída:

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

## Saída Esperada (Exemplo)

Seu relatório Markdown deve ser similar a:

```markdown
| ID | Tool | Severity | CWE | File | Line | Description | FP |
| -- | ---- | -------- | --- | ---- | ---- | ----------- | -- |
| FINDING-001 | semgrep | high | CWE-89 | app/app.py | 74 | SQL injection via string formatting | No |
| FINDING-002 | semgrep | high | CWE-78 | app/app.py | 112 | OS command injection via shell=True | No |
| FINDING-008 | semgrep | info | N/A | app/app.py | 44 | FIXME comment found | Yes |
| ... | ... | ... | ... | ... | ... | ... | ... |
```

---

## Tarefas Bônus

- Adicione uma flag `--filter-severity` que exclua achados abaixo de um
  nível de severidade especificado (ex.: `--filter-severity high` mantém
  apenas críticos e altos)
- Gere uma seção de resumo no topo do relatório mostrando contagens por
  severidade e status de falso positivo
- Escreva testes unitários para `normalise_severity()` e `extract_field()`

---

## Entregáveis

- `scripts/vulnerability_parser.py` — implementação completa
- `report.md` e/ou `report.csv` — saída do seu parser
- (Opcional) `scripts/test_parser.py` — testes unitários

---

## Critérios de Avaliação

| Critério | Peso |
| -------- | ---- |
| Normalização correta de todos os 14 achados | 30% |
| Robustez (sem crashes em dados malformados) | 20% |
| Precisão na classificação de falsos positivos | 25% |
| Qualidade do código (legibilidade, tipagem, tratamento de erros) | 25% |

---

## Referências

- [Módulo `csv` do Python](https://docs.python.org/3/library/csv.html)
- [Módulo `json` do Python](https://docs.python.org/3/library/json.html)
- [Módulo `argparse` do Python](https://docs.python.org/3/library/argparse.html)
- [Saída SARIF do Semgrep](https://semgrep.dev/docs/semgrep-ci/findings/)
- [Formato de saída JSON do Snyk](https://docs.snyk.io/snyk-cli/scan-and-maintain-projects-using-the-cli/snyk-cli-for-open-source/output-formats-for-snyk-test)
