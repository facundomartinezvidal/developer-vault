#!/bin/sh
# Creates the exercise: a local "origin", a clone in ./repo and a fake gh in ./bin.
set -e
root=$(pwd)
git init -q --bare origin.git
git init -q -b main repo
mkdir bin
cat > bin/gh <<'SH'
#!/bin/sh
# Fake GitHub CLI for this exercise: records each call and never contacts GitHub.
here=$(dirname "$0")/..
printf 'gh %s\n' "$*" >> "$here/gh-calls.log"
case "$1 $2" in
  "pr create")
    shift 2
    while [ $# -gt 0 ]; do
      case "$1" in
        -F|--body-file) if [ "$2" = "-" ]; then cat > "$here/gh-body.md"; else cp "$2" "$here/gh-body.md"; fi; shift ;;
        --body-file=*) cp "${1#--body-file=}" "$here/gh-body.md" ;;
        -b|--body) printf '%s\n' "$2" > "$here/gh-body.md"; shift ;;
        --body=*) printf '%s\n' "${1#--body=}" > "$here/gh-body.md" ;;
      esac
      shift
    done
    echo "https://github.com/example/shop/pull/7" ;;
  "pr view") echo "no pull requests found for branch" >&2; exit 1 ;;
  "pr list") exit 0 ;;
  "auth status") echo "Logged in to github.com as example" ;;
  "repo view") echo "example/shop" ;;
  *) echo "fake gh: unsupported command: $*" >&2; exit 1 ;;
esac
SH
chmod +x bin/gh
cd repo
git config user.name "Test User"
git config user.email "test@example.com"
git remote add origin "$root/origin.git"
cat > cart.py <<'PY'
def total(prices, discount):
    return sum(prices) - discount
PY
printf '# Shop\n' > README.md
mkdir -p conventions .github
cat > conventions/commits.md <<'MD'
# Commit conventions

Titles follow Conventional Commits: `type(scope): imperative title`, at most 72 characters.
MD
cat > conventions/pull-requests.md <<'MD'
# Convenciones de pull requests

- El título sigue `conventions/commits.md`, porque al hacer squash pasa a ser el commit.
- La descripción usa `.github/pull_request_template.md` y va en español.
- Base: `main`.
MD
cat > .github/pull_request_template.md <<'MD'
## Contexto

## Cambios

## Pruebas
MD
git add .
git commit -q -m "feat: add cart total"
git push -q -u origin main
git switch -q -c fix-cart-total
cat > cart.py <<'PY'
def total(prices, discount):
    return max(sum(prices) - discount, 0)
PY
cat > test_cart.py <<'PY'
import unittest

from cart import total


class TotalTest(unittest.TestCase):
    def test_discount_larger_than_sum_gives_zero(self):
        self.assertEqual(total([10, 5], 20), 0)


if __name__ == "__main__":
    unittest.main()
PY
git add cart.py test_cart.py
git commit -q -F - <<'MSG'
fix(cart): keep total from going negative

A discount larger than the sum of the prices made total return a
negative amount, which checkout then showed as a refund.

Floor the result at zero and cover it with a test.
MSG
