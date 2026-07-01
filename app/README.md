# Aplicação Vulnerável — README

## Visão Geral

Esta é uma aplicação Flask deliberadamente insegura, utilizada como parte da
avaliação **Playground de Segurança DevSecOps**.

## Executando Localmente

```bash
# Instalar dependências (use um ambiente virtual)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Iniciar a aplicação
python app.py
```

A aplicação estará disponível em `http://localhost:5000`.

## Endpoints

| Método | Caminho        | Descrição                                        |
| ------ | -------------- | ------------------------------------------------ |
| GET    | `/`            | Verificação de saúde (health check)              |
| POST   | `/login`       | Autenticar com usuário e senha                   |
| GET    | `/search`      | Buscar usuários por nome de usuário              |
| GET    | `/ping`        | Pingar um host remoto                            |
| POST   | `/deserialize` | Desserializar um payload codificado em base64    |
| GET    | `/file`        | Ler um arquivo pelo caminho                      |
| POST   | `/register`    | Registrar um novo usuário                        |

## Notas da Avaliação

- Examine `app.py` e `requirements.txt` em busca de problemas de segurança.
- **Não** implante esta aplicação em um ambiente real.
