# Vulnerable App — README

## Overview

This is a deliberately insecure Flask application used as part of the
**DevSecOps Security Playground** assessment.

## Running Locally

```bash
# Install dependencies (use a virtual environment)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start the app
python app.py
```

The application will be available at `http://localhost:5000`.

## Endpoints

| Method | Path           | Description                              |
| ------ | -------------- | ---------------------------------------- |
| GET    | `/`            | Health check                             |
| POST   | `/login`       | Authenticate with username/password      |
| GET    | `/search`      | Search users by username                 |
| GET    | `/ping`        | Ping a remote host                       |
| POST   | `/deserialize` | Deserialise a base64-encoded payload     |
| GET    | `/file`        | Read a file by path                      |
| POST   | `/register`    | Register a new user                      |

## Assessment Notes

- Examine `app.py` and `requirements.txt` for security issues.
- Refer to `/challenges/03_secure_code_review.md` for full instructions.
- Do **not** deploy this application in a real environment.
