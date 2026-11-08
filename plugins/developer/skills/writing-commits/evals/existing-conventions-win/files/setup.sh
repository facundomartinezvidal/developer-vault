#!/bin/sh
# Creates the repository for this exercise in ./repo.
set -e
git init -q repo
cd repo
git config user.name "Test User"
git config user.email "test@example.com"
mkdir conventions
cat > conventions/commits.md <<'MD'
# Convenciones de commits

- Título: `[TICKET] Verbo en infinitivo y descripción`, en español. Ejemplo: `[PAY-12] Validar el importe del cobro`.
- Sin tipos como `feat:` o `fix:`.
- El cuerpo es opcional y va en español.
MD
cat > payments.py <<'PY'
def charge(amount):
    return {"amount": amount}
PY
printf 'DEBUG=false\n' > settings.env
git add .
git commit -q -m "feat: add payments"
git commit -q --allow-empty -m "fix: adjust charge"
cat > payments.py <<'PY'
def charge(amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    return {"amount": amount}
PY
printf 'DEBUG=true\n' > settings.env
