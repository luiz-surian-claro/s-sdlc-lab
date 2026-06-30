# Desafio 3 — Revisão de Código Seguro

## Objetivo

Realize uma revisão de código seguro completa de `app/app.py` e `app/requirements.txt`.
Documente todos os achados, classifique-os por severidade e CWE, e implemente as correções.

---

## Contexto

A revisão de código seguro é uma das atividades mais valiosas em um Secure SDLC.
Diferentemente dos scanners automatizados, um revisor humano pode:

- Identificar **falhas de lógica** que as ferramentas perdem
- Compreender o **contexto** (o caminho vulnerável é alcançável? a entrada é confiável?)
- Detectar fraquezas de **nível de design**, não apenas bugs de implementação
- Avaliar **defesa em profundidade** e aderência ao princípio do menor privilégio

---

## Escopo

| Arquivo | No Escopo |
| ------- | --------- |
| `app/app.py` | Sim — revisão completa |
| `app/requirements.txt` | Sim — revisão de dependências |
| `ci-cd/pipeline.yml` | Não — coberto no Desafio 4 |

---

## Suas Tarefas

### Tarefa 3.1 — Produzir um Relatório de Revisão de Código

Examine `app/app.py` linha por linha. Para cada problema de segurança encontrado,
crie uma entrada no seu relatório com os seguintes campos:

| Campo | Descrição |
| ----- | --------- |
| **ID** | Identificador único (ex.: CR-001) |
| **Arquivo** | Nome do arquivo e número da linha |
| **Vulnerabilidade** | Nome curto (ex.: "Injeção de SQL") |
| **CWE** | Identificador CWE |
| **OWASP** | Categoria OWASP Top 10 |
| **Severidade** | Crítica / Alta / Média / Baixa / Info |
| **Descrição** | Descrição técnica do problema |
| **Impacto** | O que um atacante poderia conseguir? |
| **Correção** | Remediação proposta |

**Mínimo: reporte pelo menos 8 achados distintos.**

### Tarefa 3.2 — Revisão de Dependências

Usando `app/requirements.txt`, identifique todas as dependências com
vulnerabilidades conhecidas. Para cada uma:

- Informe o pacote, a versão e o(s) CVE(s)
- Descreva a vulnerabilidade
- Informe a versão corrigida e se é uma alteração que quebra compatibilidade
- Avalie se a vulnerabilidade é **alcançável** dado o uso atual da biblioteca na aplicação

Ferramentas que você pode usar: `pip-audit`, `safety`, `snyk test` ou pesquisa manual de CVE.

### Tarefa 3.3 — Implementar Correções

Aplique correções para os seguintes problemas (no mínimo):

1. Substitua todos os pontos de injeção de SQL por queries parametrizadas
2. Remova todos os segredos hardcoded; use `os.environ` ou um gerenciador de segredos
3. Corrija a injeção de comando em `/ping`
4. Adicione validação de entrada e sanitização de caminho em `/file`
5. Substitua a desserialização insegura com pickle por uma alternativa segura
6. Substitua o hash de senha MD5 por bcrypt ou argon2
7. Desabilite o modo debug; faça o bind apenas para localhost em ambientes não produtivos

### Tarefa 3.4 — Modelo de Ameaças (Bônus Opcional)

Crie um breve modelo de ameaças STRIDE para o endpoint `/login`. Identifique
pelo menos uma ameaça por categoria STRIDE e proponha uma mitigação.

---

## Entregáveis

- `app/app.py` atualizado com todas as correções aplicadas
- `challenge_03_code_review.md` — seu relatório de revisão (Tarefas 3.1 e 3.2)
- (Opcional) `challenge_03_threat_model.md` — análise STRIDE

---

## Critérios de Avaliação

| Critério | Peso |
| -------- | ---- |
| Número e precisão dos achados | 30% |
| Qualidade da análise de impacto | 20% |
| Qualidade e completude das correções | 30% |
| Precisão da revisão de dependências | 20% |

---

## O Que Torna uma Boa Revisão de Código Seguro?

Uma revisão sólida:

- Prioriza achados pelo **risco real**, não apenas pela pontuação CVSS
- Considera o **modelo de ameaças** (quem é o atacante? qual é o seu acesso?)
- Vai além da saída dos scanners para encontrar **falhas de lógica e design**
- Propõe **correções práticas** que não comprometem a funcionalidade
- Nota o que a aplicação faz **bem** (nem todo feedback é negativo)

---

## Referências

- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/)
- [OWASP Top 10 Proactive Controls](https://owasp.org/www-project-proactive-controls/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Python Security Best Practices](https://snyk.io/blog/python-security-best-practices-cheat-sheet/)
