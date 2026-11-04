# Authentication, sessions and access control

Hand-written summary of common practice, using OWASP Top 10, ASVS and Cheat Sheets. Not generated from the vault. Prefer the framework's or identity provider's mechanisms over custom ones.

## Access control

Broken access control is at the top of OWASP's list because it can't be found by looking at one input alone.

- **Deny by default.** A new endpoint is closed until allowed. Prefer central enforcement that a developer can't forget.
- **Check the object, not just the role.** `GET /invoices/123` must check that this user may see invoice 123 (IDOR, CWE-639). Prefer scoping queries: `WHERE id = ? AND tenant_id = ?`. Random IDs reduce guessing, but aren't an authorization check.
- **Check each operation.** Reading and editing are separate rights. Include batch operations, exports, GraphQL resolvers, background jobs, and admin paths.
- **Take identity from the session,** never from a client-supplied `userId` or `role`.
- **Consider the state.** Can this action be done now? Skipped steps in multi-step flows, changed prices and replayed requests are logic flaws.
- **Test the refusal,** with a second user and a lower role.

## Passwords

Store them with a slow salted hash, Argon2id preferably, or scrypt or bcrypt, with parameters from current guidance. Don't use a fast hash such as MD5 or SHA-256 alone. Reset tokens should be random, single-use, short-lived, and stored hashed. Avoid revealing whether an account exists. Allow long passwords, screen against breached lists, and support multi-factor authentication for sensitive access.

## Sessions

Use the framework's sessions. Cookies should be `HttpOnly`, `Secure`, with a suitable `SameSite`. Rotate the session ID on login and privilege changes, and invalidate it server-side on logout. Set idle and absolute timeouts.

## Tokens and JWT

- Verify the signature with a fixed expected algorithm, and refuse `none`. Check `exp`, `iss` and `aud`.
- A JWT payload is readable; don't put secrets in it. It can't be revoked easily, so keep lifetimes short and use refresh tokens with rotation.
- Storing tokens in `localStorage` exposes them to any XSS. Weigh that against cookie storage, which needs CSRF defenses.
- Use OAuth and OIDC via a library, with PKCE, and validate `state` and redirect URIs by exact match.
- API keys: generate randomly, store hashes, scope them narrowly, and allow rotation.

## CSRF

Browsers send cookies automatically, so state-changing requests authenticated by cookies need protection: framework tokens and `SameSite`. Don't change state on GET. APIs that only use an `Authorization` header aren't affected in the same way. Check the CORS configuration too.

## Abuse controls

Rate-limit logins, resets, sends and costly operations. Lock out carefully, since that can itself enable denial of service. Log authentication failures and privilege changes, without their secrets. Set limits on request size, pagination, and query complexity.

## Timing and comparison

Compare secrets, tokens and signatures with a constant-time function. Verify webhooks by their signature over the raw body, check timestamps to prevent replay, and treat the payload as untrusted.
