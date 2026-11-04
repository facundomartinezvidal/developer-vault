# Secrets, cryptography and sensitive data

Hand-written summary of common practice, using OWASP Cheat Sheets. Not generated from the vault. Algorithm and parameter recommendations change, so check current guidance.

## Secrets

- Keep them out of source, images, front-end bundles, logs, error messages and URLs. Use a secret manager, or environment variables injected at deployment. Commit an example file with placeholders, and ignore real ones.
- Give each environment and service its own credentials with the fewest privileges.
- Anything shipped to a browser or mobile client isn't secret.
- Use a pre-commit or CI secret scanner when possible.
- When one leaks: rotate first. Deleting the commit doesn't help since clones and caches keep it. Then check how it may have been used.

## Choosing primitives

Don't design your own cryptography. Use a high-level library: libsodium, or the platform's vetted API.

| Need | Use | Avoid |
|---|---|---|
| Encrypt data | AES-256-GCM, ChaCha20-Poly1305 | ECB, unauthenticated CBC, DES, RC4 |
| Integrity with a shared key | HMAC-SHA-256 | Plain hash with a secret appended |
| File or content hash | SHA-256 or better | MD5 and SHA-1 for security use |
| Passwords | Argon2id, scrypt, bcrypt | Fast hash, encryption |
| Signatures | Ed25519, ECDSA, RSA-PSS with enough size | Small keys, PKCS#1 v1.5 for new work |
| Random tokens | The OS's CSPRNG: `secrets`, `crypto.randomBytes`, `crypto/rand`, `SecureRandom` | `Math.random`, `rand()`, time-based seeds |
| Transport | TLS 1.2 or later, certificate checks on | `verify=false`, custom validation |

Never reuse a nonce with the same key in an AEAD cipher. Store keys separately from the data, and plan for rotation. Encoding, such as Base64, isn't encryption.

## Personal and sensitive data

Collect only what's needed, and know where it goes, including logs, analytics, backups, caches and third parties. Set retention periods and be able to delete it. Encrypt in transit, and at rest where it's warranted. Protect exports and restrict access. Legal requirements vary, so have someone qualified confirm them.

## Logs and error messages

Log security events, such as logins, denied access and changes to permissions, with who, what and when. Don't log passwords, tokens, full card numbers or unneeded personal data; filter these centrally. Show users a generic error with a correlation ID, and keep details on the server. Stack traces, query text and versions help attackers.

## Numbers and resources

Integer overflow and rounding on money, quantities and limits are security issues as well. Validate ranges on the server, and use exact types. Set limits on memory, time and size for work triggered by a request.
