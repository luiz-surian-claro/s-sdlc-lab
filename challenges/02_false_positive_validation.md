# Desafio 2 — Identificação e Justificativa de Falsos Positivos

## Objetivo

Analise os resultados da varredura SCA em `data/sca_results.json` e os
resultados mistos em `data/mixed_scan_results.json`. Identifique falsos positivos,
justifique suas decisões e explique os riscos de classificar erroneamente os achados.

---

## Contexto

Scanners de segurança geram um grande volume de achados. Nem todos representam
vulnerabilidades reais e exploráveis. Um analista de segurança qualificado deve:

- Distinguir **verdadeiros positivos** de **falsos positivos**
- Entender a diferença entre uma vulnerabilidade em uma biblioteca e uma
  vulnerabilidade que é **alcançável** na aplicação
- Comunicar os achados de forma clara a desenvolvedores e partes interessadas

---

## Achados em Revisão

O arquivo `data/sca_results.json` contém um array `false_positives_candidates`
com três entradas:

| ID | Pacote | Achado | Severidade Reportada |
| -- | ------ | ------ | -------------------- |
| FP-001 | Flask 2.0.1 | Símbolos de modo debug em varredura binária | ALTA |
| FP-002 | requests 2.25.0 | verify=False detectado | CRÍTICA |
| AMBIGUOUS-001 | PyYAML 5.3.1 | yaml.load() sem Loader | CRÍTICA |

---

## Suas Tarefas

### Tarefa 2.1 — Classificar cada candidato

Para cada um dos três candidatos acima, forneça:

1. **Classificação**: Verdadeiro Positivo | Falso Positivo | Ambíguo
2. **Justificativa** (≥3 frases): Explique seu raciocínio com evidências técnicas
   dos dados da varredura e do código da aplicação.
3. **Risco de classificação incorreta**: O que acontece se esse achado for
   descartado incorretamente? Ou incorretamente escalado?
4. **Ação recomendada**: Corrigir, Aceitar Risco, Monitorar ou Sem Ação — e por quê.

### Tarefa 2.2 — Identificar falsos positivos adicionais

Revise `data/mixed_scan_results.json` e identifique quaisquer achados que você
considere falsos positivos além dos candidatos rotulados.

Para cada falso positivo adicional identificado, forneça a mesma análise de
quatro pontos da Tarefa 2.1.

### Tarefa 2.3 — Definir uma política de falsos positivos

Escreva uma política de triagem de falsos positivos breve (200–400 palavras)
para sua organização. Inclua:

- Critérios para classificar um achado como falso positivo
- Evidências/documentação necessárias
- Processo de aprovação (quem assina?)
- Cadência de revisão (com que frequência as decisões de FP são reavaliadas?)

---

## Entregáveis

- Um arquivo Markdown `challenge_02_false_positives.md` com sua análise

---

## Critérios de Avaliação

| Critério | Peso |
| -------- | ---- |
| Classificação correta de FP-001 e FP-002 (FPs óbvios) | 20% |
| Análise refinada de AMBIGUOUS-001 | 25% |
| FPs adicionais identificados nos resultados mistos | 25% |
| Qualidade da política de falsos positivos | 30% |

---

## Dicas

- Leia os campos `analyst_note` — eles contêm contexto, mas não a resposta.
- Pense em **alcançabilidade**: um caminho de código vulnerável que nunca é
  chamado é diferente de um que está diretamente exposto.
- Pense nas **limitações do scanner**: ferramentas de correspondência de padrões
  têm fontes de ruído bem conhecidas.
- Considere o **impacto nos negócios** tanto de sub-reportar quanto de
  super-reportar.

---

## Referências

- [OWASP False Positives](https://owasp.org/www-community/vulnerabilities/False_Positives)
- [CVE-2020-14343 (PyYAML)](https://nvd.nist.gov/vuln/detail/CVE-2020-14343)
- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
