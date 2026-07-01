# S-SDLC Lab — Playground de Segurança DevSecOps

> **Avaliação Técnica para candidatos a Analista de Segurança da Informação**

Este repositório é um ambiente de avaliação DevSecOps que simula
cenários do mundo real envolvendo S-SDLC, segurança de pipelines CI/CD
e gerenciamento de vulnerabilidades.

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
source venv/bin/activate  # no Windows: venv\Scripts\Activate.ps1

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
> **Nunca a implante em ambientes produtivos.**

---

## Orientações para Candidatos

- Leia cada arquivo de desafio com atenção antes de começar.

- Você pode utilizar quaisquer ferramentas (Semgrep, pip-audit, Bandit, etc.)
  para auxiliar sua análise, mas deve ser capaz de explicar cada achado e
  cada correção.
- A qualidade do raciocínio importa mais do que a quantidade de achados.

---

Boa sorte! 🔐
