# Desafio 4 — Melhoria de Segurança no Pipeline CI/CD

## Objetivo

Revise o pipeline do GitHub Actions em `ci-cd/pipeline.yml`, identifique todas
as configurações incorretas de segurança e proponha (e implemente) uma versão
com hardening.

---

## Contexto

Pipelines CI/CD são uma superfície de ataque crítica em ambientes DevSecOps modernos.
Pipelines mal configurados podem:

- Vazar segredos para logs de build ou serviços de terceiros
- Permitir ataques à cadeia de suprimentos via actions não fixadas
- Executar código malicioso injetado via pull requests
- Implantar código vulnerável ou não testado em produção

---

## Achados a Procurar

O pipeline em `ci-cd/pipeline.yml` contém pelo menos **oito** configurações
incorretas intencionais. Sua tarefa é encontrá-las todas.

Categorias de dicas (sem ordem):

- Gerenciamento de segredos
- Permissões
- Lógica de gate de segurança
- Configuração de trigger
- Fixação de actions
- Supressão de erros
- Isolamento de ambiente
- Controles de implantação

---

## Suas Tarefas

### Tarefa 4.1 — Enumerar as Configurações Incorretas

Revise `ci-cd/pipeline.yml` e liste cada configuração incorreta encontrada.
Para cada uma, forneça:

| Campo | Descrição |
| ----- | --------- |
| **ID** | Identificador único (ex.: PL-001) |
| **Localização** | Nome do job e número da linha |
| **Problema** | Descrição curta |
| **Risco** | O que um atacante poderia fazer? |
| **Severidade** | Crítica / Alta / Média / Baixa |
| **Correção** | Remediação proposta |

**Mínimo: identifique pelo menos 6 configurações incorretas distintas.**

### Tarefa 4.2 — Implementar um Pipeline com Hardening

Crie `ci-cd/pipeline_hardened.yml` — uma versão corrigida do pipeline.

Seu pipeline com hardening **deve**:

1. **Fixar todas as actions** a um SHA de commit específico (não apenas uma tag)
   para prevenir ataques à cadeia de suprimentos.

2. **Usar GitHub Secrets** para todos os tokens (`SEMGREP_APP_TOKEN`, `SNYK_TOKEN`,
   `DEPLOY_KEY`, etc.).

3. **Definir permissões com menor privilégio** usando o bloco `permissions`
   no nível superior e/ou por job.

4. **Falhar o pipeline** quando ferramentas SAST ou SCA detectarem achados
   acima de um limiar de severidade configurável (não use `continue-on-error: true`).

5. **Exigir aprovação manual** antes de implantar em produção usando GitHub
   Environments com regras de proteção.

6. **Remover supressão de erros** (`|| true`) dos comandos de teste.

7. **Limitar o trigger** apenas a branches relevantes (ex.: `main`, `develop`,
   `release/**`).

8. **Adicionar verificação de integridade de dependências** (ex.: `pip install --require-hashes`
   ou um arquivo de lock).

### Tarefa 4.3 — Design de Gates de Segurança (Discussão)

Responda às seguintes perguntas no seu relatório:

1. Em que ponto do pipeline os resultados de SAST devem bloquear um merge?
   Qual limiar de severidade você escolheria, e por quê?

2. Como você lidaria com uma situação em que uma CVE crítica é encontrada em
   uma dependência transitiva sem correção disponível?

3. Quais gates de segurança adicionais você adicionaria a este pipeline além
   de SAST, SCA e DAST?

---

## Entregáveis

- `ci-cd/pipeline_hardened.yml` — pipeline corrigido
- `challenge_04_cicd.md` — tabela de achados e respostas à Tarefa 4.3

---

## Critérios de Avaliação

| Critério | Peso |
| -------- | ---- |
| Número e precisão das configurações incorretas identificadas | 30% |
| Qualidade e completude do pipeline com hardening | 40% |
| Profundidade das respostas à Tarefa 4.3 | 30% |

---

## Referências

- [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [OWASP CI/CD Security Top 10](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
- [Securing GitHub Actions — Pinning Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#using-third-party-actions)
- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
