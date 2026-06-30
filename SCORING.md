# Rubrica de Pontuação — Playground de Segurança DevSecOps

Esta rubrica é destinada ao **avaliador**. Não compartilhe com os candidatos
antes que a avaliação seja concluída.

---

## Pontuação Total: 100 pontos

| Desafio | Pontuação Máxima |
| ------- | ---------------- |
| Desafio 1 — Corrigir Código Vulnerável | 25 |
| Desafio 2 — Validação de Falsos Positivos | 20 |
| Desafio 3 — Revisão de Código Seguro | 20 |
| Desafio 4 — Segurança em CI/CD | 20 |
| Desafio 5 — Parsing de JSON | 15 |
| **Total** | **100** |

---

## Desafio 1 — Corrigir Código Vulnerável (25 pontos)

### 1.1 Identificação de Vulnerabilidades (10 pontos)

| Achado | Pontos |
| ------ | ------ |
| Injeção de SQL (login) | 1,5 |
| Injeção de SQL (register) | 1,5 |
| Injeção de Comando no SO (ping) | 2 |
| Token de API hardcoded | 1 |
| Senha de banco hardcoded | 1 |
| Path Traversal (file) | 1,5 |
| Desserialização insegura (pickle) | 1 |
| Criptografia fraca (MD5 para senhas) | 1 |
| Modo debug habilitado + binding 0.0.0.0 | 0,5 |
| **Subtotal** | **11** *(conceder no máximo 10)* |

### 1.2 Qualidade das Correções (10 pontos)

| Correção | Pontos |
| -------- | ------ |
| Queries parametrizadas (ambos os endpoints) | 2 |
| shell=False + lista de argumentos para ping | 2 |
| Segredos movidos para variáveis de ambiente | 2 |
| Sanitização de caminho (os.path.realpath + verificação de prefixo) | 2 |
| pickle substituído por alternativa segura | 1 |
| MD5 substituído por bcrypt/argon2 | 1 |

### 1.3 Qualidade do Relatório (5 pontos)

- **5**: Todos os achados documentados com CWE, impacto e remediação clara
- **3–4**: Maioria dos achados documentada; lacunas menores
- **1–2**: Documentação parcial; análise de impacto ausente
- **0**: Nenhum relatório submetido

---

## Desafio 2 — Validação de Falsos Positivos (20 pontos)

### 2.1 Classificação de FP-001 (4 pontos)

**Resposta esperada**: Falso Positivo

- **4**: Corretamente classificado como FP com justificativa técnica clara (o scanner detectou símbolos de debug no binário da biblioteca, não no código do usuário)
- **2–3**: Classificação correta, justificativa fraca
- **1**: Classificação incorreta com entendimento parcial
- **0**: Classificação incorreta, sem justificativa

### 2.2 Classificação de FP-002 (4 pontos)

**Resposta esperada**: Falso Positivo

- **4**: Corretamente classificado como FP; identificou que o match foi na suíte de testes da biblioteca, não no código da aplicação
- **2–3**: Classificação correta, justificativa fraca
- **1**: Classificação incorreta com entendimento parcial
- **0**: Incorreto sem justificativa

### 2.3 Classificação de AMBIGUOUS-001 (6 pontos)

**Resposta esperada**: Ambíguo — tecnicamente um FP (código morto), mas deve ser sinalizado para remediação

- **6**: Reconhece a nuance — a chamada yaml.load() está em código morto, portanto não é diretamente explorável, mas o código morto deve ser removido; recomenda limpeza em vez de aceitar/ignorar
- **4–5**: Identifica a ambiguidade; recomenda ação
- **2–3**: Classificado como um extremo (TP claro ou FP claro) com raciocínio razoável, porém incompleto
- **0–1**: Classificação incorreta com justificativa fraca

### 2.4 FPs Adicionais em mixed_scan_results.json (3 pontos)

**FPs esperados**: FINDING-008 (comentário FIXME — INFO, sem impacto de segurança), FINDING-010 (string de debug em fixtures de teste do Flask), FINDING-013 (duplicata de FINDING-009)

- **3**: Identifica pelo menos 2 FPs adicionais com justificativa
- **2**: Identifica 1 FP adicional com justificativa
- **1**: Tenta a identificação, mas com raciocínio fraco
- **0**: Nenhum identificado

### 2.5 Política de Falsos Positivos (3 pontos)

- **3**: A política inclui critérios, requisitos de evidência, processo de aprovação e cadência de revisão
- **2**: A política cobre a maioria dos elementos; falta um
- **1**: Política parcial; faltam dois ou mais elementos
- **0**: Nenhuma política submetida

---

## Desafio 3 — Revisão de Código Seguro (20 pontos)

### 3.1 Relatório de Achados (10 pontos)

**Achados mínimos esperados (8):**

| Achado | Pontos |
| ------ | ------ |
| Injeção de SQL (login) | 1 |
| Injeção de SQL (register) | 1 |
| XSS (search) | 1 |
| Injeção de comando (ping) | 1 |
| Path traversal (file) | 1 |
| Desserialização insegura | 1 |
| Credenciais hardcoded / token | 1 |
| Hash de senha com MD5 | 1 |
| Armazenamento de senha em texto puro (register) | 0,5 |
| Modo debug + binding 0.0.0.0 | 0,5 |
| Validação de entrada ausente (register) | 0,5 |

Conceder até 10 pontos.

### 3.2 Revisão de Dependências (5 pontos)

- **5**: Todos os 8+ pacotes vulneráveis identificados com CVEs, impacto, versões corrigidas e análise de alcançabilidade
- **3–4**: Maioria dos pacotes identificada; lacunas menores
- **1–2**: Menos de 4 pacotes identificados
- **0**: Não tentado

### 3.3 Correções Aplicadas (5 pontos)

Mesmo critério do Desafio 1 — as correções são avaliadas holisticamente aqui, caso o Desafio 1 não tenha sido submetido.

---

## Desafio 4 — Segurança em CI/CD (20 pontos)

### 4.1 Configurações Incorretas Identificadas (10 pontos)

**Configurações incorretas esperadas (8+):**

| Configuração Incorreta | Pontos |
| ---------------------- | ------ |
| SEMGREP_APP_TOKEN hardcoded em env | 1,5 |
| SNYK_TOKEN hardcoded em env | 1,5 |
| DEPLOY_KEY hardcoded em step env | 2 |
| continue-on-error: true em SAST/SCA | 1,5 |
| \|\| true suprime falhas nos testes | 1 |
| Sem bloco de permissões (GITHUB_TOKEN com permissões excessivas) | 1 |
| Trigger em todas as branches (`"*"`) | 0,5 |
| Sem gate de aprovação manual antes do deploy em produção | 1 |
| Actions não fixadas em SHA | 0,5 |

Conceder até 10 pontos.

### 4.2 Pipeline com Hardening (7 pontos)

- **7**: Todas as 8 melhorias obrigatórias implementadas; pipeline funcional
- **5–6**: Maioria das melhorias implementada; 1–2 lacunas
- **3–4**: Melhorias principais (segredos, permissões, gates) implementadas; outras ausentes
- **1–2**: Melhorias parciais com lacunas significativas
- **0**: Não tentado

### 4.3 Questões de Discussão (3 pontos)

- **3**: Todas as três questões respondidas de forma reflexiva com recomendações específicas
- **2**: Duas questões respondidas adequadamente
- **1**: Respostas superficiais
- **0**: Não tentado

---

## Desafio 5 — Parsing de JSON (15 pontos)

### 5.1 Implementação do Parser (10 pontos)

| Componente | Pontos |
| ---------- | ------ |
| `extract_field()` — trata todos os nomes de campo variantes e caminhos aninhados | 2 |
| `normalise_severity()` — trata todos os formatos brutos sem erros | 2 |
| `normalise_finding()` — todos os 14 achados normalizados corretamente | 3 |
| `apply_fp_rules()` — pelo menos 3 regras implementadas corretamente | 2 |
| `to_csv()` e/ou `to_markdown()` — formato de saída válido | 1 |

### 5.2 Robustez (3 pontos)

- **3**: Sem crashes em campos ausentes/nulos, tipos inesperados ou duplicatas
- **2**: Trata a maioria dos casos de borda; 1–2 crashes em casos extremos
- **1**: Tratamento de erros básico apenas
- **0**: O parser crasha em múltiplas entradas

### 5.3 Precisão na Classificação de Falsos Positivos (2 pontos)

- **2**: FINDING-008, FINDING-010 e FINDING-013 corretamente sinalizados como FP
- **1**: 1–2 corretamente sinalizados
- **0**: Nenhum corretamente sinalizado

---

## Faixas de Pontuação

| Pontuação | Faixa | Interpretação |
| --------- | ----- | ------------- |
| 90–100 | **Excepcional** | Pronto para função sênior; demonstra expertise profunda |
| 75–89 | **Forte** | Habilidades sólidas; lacunas menores que podem ser rapidamente superadas |
| 60–74 | **Adequado** | Atende aos requisitos básicos; necessita mentoria em algumas áreas |
| 45–59 | **Em Desenvolvimento** | Conhecimento fundamental presente; lacunas de habilidade significativas |
| < 45 | **Abaixo do Limiar** | Não adequado para uma função de Analista Sênior de Segurança da Informação no momento |

---

## Pontos Bônus (até 10 pontos adicionais)

| Bônus | Pontos |
| ----- | ------ |
| Modelo de ameaças STRIDE para `/login` (Desafio 3) | 3 |
| Flag `--filter-severity` no parser via CLI (Desafio 5) | 1 |
| Seção de resumo na saída do parser (Desafio 5) | 1 |
| Testes unitários para o parser (Desafio 5) | 2 |
| Melhorias de segurança adicionais além das obrigatórias (qualquer desafio) | até 3 |

---

## Notas para o Avaliador

- Deduzir pontos se as correções introduzirem novas vulnerabilidades
- Conceder crédito parcial generosamente quando o raciocínio for sólido, mesmo que a conclusão difira da resposta esperada
- O caso AMBIGUOUS-001 não possui resposta única correta; avalie a **qualidade do raciocínio**, não apenas a classificação
- Um candidato que identifique corretamente um achado não listado nesta rubrica deve receber crédito por isso
