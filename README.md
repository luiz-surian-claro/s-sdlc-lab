# S-SDLC Lab — Playground de Segurança DevSecOps

> **Avaliação Técnica para candidatos a Analista Sênior de Segurança da Informação**

Este repositório é um ambiente de avaliação DevSecOps autocontido que simula
cenários do mundo real envolvendo Secure SDLC, segurança de pipelines CI/CD
e gerenciamento de vulnerabilidades.

---

## Estrutura do Repositório

```text
s-sdlc-lab/
├── app/                        # Aplicação Flask vulnerável
│   ├── app.py                  # Código-fonte da aplicação (contém vulnerabilidades intencionais)
│   ├── requirements.txt        # Dependências Python (algumas desatualizadas/vulneráveis)
│   └── README.md               # Documentação da aplicação
│
├── data/                       # Resultados de varreduras de vulnerabilidades
│   ├── sast_results.json       # Saída do SAST Semgrep
│   ├── sca_results.json        # Saída do SCA Snyk (inclui candidatos a falso positivo)
│   ├── mixed_scan_results.json # Resultados multi-ferramenta (schema inconsistente — desafio de parsing)
│   └── expected_output_sample.md  # Saída de referência para o desafio de parsing
│
├── scripts/
│   └── vulnerability_parser.py # Script esqueleto — o candidato deve completar
│
├── ci-cd/
│   └── pipeline.yml            # Workflow do GitHub Actions (contém configurações incorretas)
│
├── challenges/
│   ├── 01_fix_vulnerabilities.md
│   ├── 02_false_positive_validation.md
│   ├── 03_secure_code_review.md
│   ├── 04_cicd_security.md
│   └── 05_json_parsing.md
│
├── SCORING.md                  # Rubrica de pontuação (somente para avaliadores)
└── README.md                   # Este arquivo
```

---

## Visão Geral da Avaliação

A avaliação consiste em **cinco desafios** que avaliam diferentes competências
DevSecOps. Os candidatos devem completar todos os cinco desafios dentro da
janela de tempo acordada.

| # | Desafio | Competências Avaliadas |
| - | ------- | ---------------------- |
| 1 | Corrigir Código Vulnerável | Triagem de SAST, codificação segura |
| 2 | Validação de Falsos Positivos | Julgamento analítico, avaliação de risco |
| 3 | Revisão de Código Seguro | Revisão manual, análise de dependências |
| 4 | Segurança em CI/CD | Hardening de pipeline, gerenciamento de segredos |
| 5 | Parsing de JSON | Scripting, normalização de dados |

---

## Primeiros Passos

### Pré-requisitos

- Python 3.10+
- Git

### Configuração

```bash
# Clonar o repositório
git clone https://github.com/luiz-surian-claro/s-sdlc-lab.git
cd s-sdlc-lab

# Criar um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate

# Instalar as dependências da aplicação
pip install -r app/requirements.txt
```

### Executando a Aplicação

```bash
cd app
python app.py
```

A aplicação inicia em `http://localhost:5000`.

> ⚠️ **Atenção**: Esta aplicação contém vulnerabilidades de segurança intencionais.
> **Nunca a implante em ambiente de produção.**

---

## Desafios

Resolva cada desafio na ordem indicada. As instruções estão no diretório
`/challenges`.

### Desafio 1 — Corrigir Código Vulnerável

📄 [`challenges/01_fix_vulnerabilities.md`](challenges/01_fix_vulnerabilities.md)

Analise os resultados de SAST em `data/sast_results.json` e corrija as
vulnerabilidades correspondentes em `app/app.py`. Abrange: injeção de SQL,
injeção de comando, path traversal, desserialização insegura, criptografia
fraca, segredos hardcoded.

### Desafio 2 — Validação de Falsos Positivos

📄 [`challenges/02_false_positive_validation.md`](challenges/02_false_positive_validation.md)

Revise os resultados de SCA em `data/sca_results.json` e identifique verdadeiros
positivos, falsos positivos e achados ambíguos. Justifique cada decisão.
Elabore uma política de triagem de falsos positivos.

### Desafio 3 — Revisão de Código Seguro

📄 [`challenges/03_secure_code_review.md`](challenges/03_secure_code_review.md)

Realize uma revisão de código seguro de `app/app.py` e `app/requirements.txt`.
Documente todos os achados e implemente as correções.

### Desafio 4 — Segurança em CI/CD

📄 [`challenges/04_cicd_security.md`](challenges/04_cicd_security.md)

Revise `ci-cd/pipeline.yml` em busca de configurações incorretas de segurança.
Produza uma versão com hardening e documente seus achados.

### Desafio 5 — Parsing de JSON

📄 [`challenges/05_json_parsing.md`](challenges/05_json_parsing.md)

Complete `scripts/vulnerability_parser.py` para fazer o parsing de
`data/mixed_scan_results.json` e gerar um relatório de vulnerabilidades
normalizado em CSV e/ou Markdown.

---

## Entregáveis

Submeta os itens abaixo como pull request ou arquivo zip:

| Arquivo | Desafio |
| ------- | ------- |
| `app/app.py` (corrigido) | 1, 3 |
| `challenge_01_findings.md` | 1 |
| `challenge_02_false_positives.md` | 2 |
| `challenge_03_code_review.md` | 3 |
| `challenge_03_threat_model.md` *(opcional)* | 3 |
| `ci-cd/pipeline_hardened.yml` | 4 |
| `challenge_04_cicd.md` | 4 |
| `scripts/vulnerability_parser.py` (completo) | 5 |
| `report.md` e/ou `report.csv` | 5 |
| `scripts/test_parser.py` *(opcional)* | 5 |

---

## Critérios de Avaliação

Os candidatos são avaliados nos seguintes aspectos:

| Dimensão | Descrição |
| -------- | --------- |
| **Profundidade técnica** | Profundidade da análise de vulnerabilidades além da saída das ferramentas |
| **Precisão** | Correção das classificações e das correções aplicadas |
| **Raciocínio** | Qualidade das justificativas para as decisões |
| **Qualidade de código** | Legibilidade, segurança e correção do código escrito/corrigido |
| **Comunicação** | Clareza dos entregáveis escritos |

A pontuação máxima é de **100 pontos** (mais até 10 pontos bônus).
Consulte [`SCORING.md`](SCORING.md) para a rubrica completa *(somente para avaliadores)*.

---

## Referências OWASP

As vulnerabilidades deste laboratório são baseadas no
[OWASP Top 10 (2021)](https://owasp.org/Top10/):

| Categoria OWASP | Abordada em |
| --------------- | ----------- |
| A01 — Controle de Acesso Quebrado | Path Traversal (app.py) |
| A02 — Falhas Criptográficas | Hash de senha com MD5 (app.py) |
| A03 — Injeção | SQLi, XSS, Injeção de Comando (app.py) |
| A05 — Configuração Incorreta de Segurança | Modo debug, binding 0.0.0.0, CI/CD |
| A06 — Componentes Vulneráveis | Dependências desatualizadas (requirements.txt) |
| A07 — Falhas de Autenticação | Credenciais hardcoded (app.py, pipeline.yml) |
| A08 — Falhas de Integridade de Software | Desserialização insegura (app.py) |

---

## Estimativa de Tempo

| Desafio | Tempo Estimado |
| ------- | -------------- |
| Desafio 1 | 45–60 min |
| Desafio 2 | 30–45 min |
| Desafio 3 | 60–90 min |
| Desafio 4 | 45–60 min |
| Desafio 5 | 60–90 min |
| **Total** | **4–6 horas** |

---

## Orientações para Candidatos

- Leia cada arquivo de desafio com atenção antes de começar.
- Os comentários `TODO (CANDIDATO):` nos arquivos-fonte são dicas — eles não
  revelam o cenário completo.
- Não consulte o arquivo `SCORING.md` antes de submeter seu trabalho.
- Você pode utilizar quaisquer ferramentas (Semgrep, pip-audit, Bandit, etc.)
  para auxiliar sua análise, mas deve ser capaz de explicar cada achado e
  cada correção.
- A qualidade do raciocínio importa mais do que a quantidade de achados.

---

Boa sorte! 🔐
