# Dependencies, configuration and platform risks

Hand-written summary of common practice. Not generated from the vault.

## Dependencies and supply chain

- **Add deliberately.** Each dependency is code that you run with your privileges. Check maintenance, popularity and transitive weight. A few lines of your own may be better. Check spelling too, because typosquatted names are a real attack. Verify in the registry that a suggested package actually exists and is the intended one: language models often invent package names, and attackers register them (slopsquatting).
- **Pin and lock.** Commit lockfiles. In CI, use the frozen install: `npm ci`, `pip install --require-hashes`, `cargo --locked`, `go mod verify`.
- **Audit:** `npm audit`, `pip-audit`, `cargo audit`, `govulncheck`, `bundler-audit`, OWASP Dependency-Check, or the platform's alerts. Check whether the vulnerable path is actually reachable, and update promptly when it's exploitable.
- **Install scripts** run arbitrary code at install time. Disable or review them where the risk is high.
- **Update regularly in small steps,** so a security patch isn't blocked by a large upgrade.
- **CI itself:** pin third-party actions, scope tokens narrowly, and be careful running workflows on untrusted pull requests.

## Secure configuration

- Turn debug modes, default credentials, sample apps and directory listings off in production.
- **HTTP headers** where they apply: `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, and `frame-ancestors` to prevent clickjacking.
- **CORS:** allow specific origins. Reflecting any `Origin` along with credentials is dangerous.
- **Least privilege:** database users without admin rights, narrow cloud roles, non-root containers.
- **Containers:** small, pinned base images, no secrets in layers, and rebuild regularly. Scan images.
- **Infrastructure:** storage buckets and databases aren't public by default, and internal doesn't mean trusted.

## Memory-unsafe code

In C, C++, and `unsafe` blocks or FFI elsewhere, the common defects are buffer overflows, use-after-free, integer overflow and format strings. Use bounds-checked operations, smart pointers and modern containers. Compile with warnings as errors, and run AddressSanitizer, UBSan and fuzzing. Check the sizes of everything read from outside. Keep unsafe regions small, and document what they require.

## Concurrency and timing

Check-then-act on security state is a race (TOCTOU, CWE-367): double-spending a balance, using a coupon twice, or swapping a file between checking and opening. Use database constraints, atomic updates, transactions at the right isolation, or idempotency keys.

## Features built on LLMs

When an application calls a language model, its output is untrusted input and its instructions can be overridden by the content it reads (prompt injection). Don't feed output directly into SQL, a shell or HTML. Give tools the least privileges, and require confirmation for consequential actions. Keep secrets out of prompts. Separate data from instructions, while recognizing that this reduces the risk but doesn't remove it. See OWASP's Top 10 for LLM applications.
