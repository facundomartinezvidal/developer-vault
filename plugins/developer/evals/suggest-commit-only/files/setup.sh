#!/bin/sh
# Creates the repository for this exercise in ./repo.
set -e
git init -q repo
cd repo
git config user.name "Test User"
git config user.email "test@example.com"
cat > cart.py <<'PY'
def total(prices, discount):
    return sum(prices) - discount
PY
printf '# Cart\n' > README.md
git add .
git commit -q -m "Add cart total"
git commit -q --allow-empty -m "Set up project"
