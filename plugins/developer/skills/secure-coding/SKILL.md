---
name: secure-coding
description: "Writes and reviews application code so it resists common vulnerabilities, in any language, following the OWASP Top 10:2025 and CWE guidance. Use whenever code handles user input, SQL or shell commands, files, uploads, URLs, HTML, logins, sessions, permissions, tokens, secrets, encryption, payments or personal data, and whenever someone asks if code is safe, even if they never say \"security\". Covers injection, XSS, CSRF, SSRF, broken access control, password storage, dependency risks and \"esto es seguro\", \"revisá la seguridad de este código\", \"cómo guardo contraseñas\", \"cómo manejo este token\". For design-level threat modeling use the architect's threat-modeling. For defensive work on code the user owns or is authorized to test."
---

# Secure Coding

Use this skill to **write** safe code, **review** code for vulnerabilities or **fix** one. Its point of view: most vulnerabilities come from trusting data, from missing a check on one path, or from hand-building what a vetted library already does. Secure defaults are cheaper than later audits.

## How to think about it

1. **Trace untrusted data.** Anything that crosses a trust boundary is untrusted: request fields, headers, cookies, files, webhooks, messages, third-party responses and database values that came from users. Follow it from where it enters to where it's used.
2. **Look at the sink, not only the source.** Danger depends on the destination: SQL, shell, HTML, filesystem path, URL fetch, deserializer or template. Use the safe form for that sink. Input validation helps, but it doesn't replace parameterizing or encoding.
3. **Check who may do this, every time.** Authenticating says who the caller is. For every operation and object, the server must also check that this caller may act on this object. Hiding a button is not a check.
4. **Use what is vetted.** Prefer the framework's mechanisms for auth, sessions, CSRF, escaping and crypto over custom code. Check what the framework does by default in the installed version, including when auto-escaping is off.
5. **Fail closed.** On an error or an unexpected state, deny access. Mishandled exceptions are their own OWASP category now. Don't expose internals in responses.
6. **Trust no dependency by default.** Supply chain failures rank third in OWASP's list. Check that a package exists and is the intended one before adding it, especially one suggested from memory, because attackers register names that models invent.

## Check by sink

| If the code… | The risk | Do this |
|---|---|---|
| Builds SQL or a query | Injection | Parameterized queries, allowlists for identifiers |
| Runs a command | Command injection | Avoid the shell; pass an argument array |
| Writes HTML | XSS | Auto-escaping by context; sanitize allowed HTML with a library |
| Uses a path from input | Traversal | Generated names, resolve and check against a base directory |
| Fetches a URL from input | SSRF | Allowlist hosts; block internal addresses, including after redirects |
| Deserializes or parses | Code execution, XXE | Data-only formats, schema validation, disabled external entities |
| Takes an object ID | Broken access control | Query scoped by owner or tenant, or a check on each object |
| Binds a request to a model | Mass assignment | Explicit list of accepted fields |
| Changes state from a browser | CSRF | Framework tokens, SameSite cookies |
| Stores passwords | Credential theft | Argon2id, scrypt or bcrypt through a library |
| Holds a secret | Exposure | Secret manager or environment, not code or logs; plan rotation |
| Generates a token | Prediction | The cryptographic random generator |
| Reads and later acts on state | Race (TOCTOU) | Atomic operation, constraint or lock |

Read the matching reference for details and pitfalls.

## Modes

### Write

Apply the matching checks as part of the code, without an essay. Keep access checks close to the data. Add tests that show the refusal works: another user's ID returns not found or forbidden, and malicious input stays inert. Mention decisions the user should confirm, such as token lifetime.

### Review

Trace real paths and report demonstrated findings, most severe first:

- **Vulnerability and where,** with `file:line` and a CWE or OWASP category if clear.
- **The scenario:** who could do what, and what they need. Show how the data reaches the sink.
- **Impact and likelihood,** in terms of this system. Mark what you could not confirm, such as protection provided by a proxy.
- **The fix,** as concrete code.

Don't pad the list with theoretical issues or generic hardening. An unexploitable finding, labeled as defense in depth, goes last. Say what you checked and found fine, and what you did not check: a review isn't proof of safety.

Run the project's scanners if they exist (SAST, dependency audit, secret scan), but treat results as leads to verify. Their silence doesn't prove safety.

### Fix

Fix the cause, at the sink, and look for the same pattern elsewhere. Add a regression test. If a secret was exposed, removing it from the code isn't enough: it must be rotated, and it remains in version history. Tell the user. Rewriting history or rotating credentials needs their go-ahead.

## Limits

Proof-of-concept tests stay on local code or systems the user is authorized to test, using harmless payloads. Security questions with legal or compliance consequences, such as PCI or GDPR, need a specialist's confirmation; you can list the technical controls, but not declare compliance.

## Reference files

| File | Read when the topic is… |
|---|---|
| `references/input-and-injection.md` | injection in all its forms, XSS, traversal, SSRF, deserialization, uploads, ReDoS, unsafe functions by language family |
| `references/auth-and-access.md` | authentication, sessions, tokens and JWT, password storage, authorization, IDOR, CSRF, rate limiting |
| `references/secrets-crypto-and-data.md` | secrets, encryption, hashing, randomness, personal data, logging, error messages |
| `references/dependencies-and-config.md` | supply chain, audits, secure configuration, headers, CORS, containers, memory safety, LLM features |
