#!/bin/sh
# Creates the repository for this exercise in ./repo.
set -e
git init -q repo
cd repo
git config user.name "Test User"
git config user.email "test@example.com"
mkdir conventions
cat > conventions/commits.md <<'MD'
# Commit conventions

Titles follow Conventional Commits: `type(scope): imperative title`, at most 72 characters. Bodies explain why.
MD
cat > app.py <<'PY'
def discount(price, percent):
    return price * percent


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b
PY
printf '# App\n' > README.md
git add .
git commit -q -m "feat: add price helpers"
cat > app.py <<'PY'
def discount(price, percent):
    return price * percent / 100


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def format_price(price):
    return f"${price:.2f}"
PY
cat > test_app.py <<'PY'
from app import discount


def test_discount_is_a_percentage():
    assert discount(200, 10) == 20
PY
printf '# App\n\nUse `format_price` to show a price with two decimals.\n' > README.md
