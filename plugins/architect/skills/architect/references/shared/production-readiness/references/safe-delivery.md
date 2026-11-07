# Safe delivery

Hand-written summary of common practice, drawing on *The Pragmatic Programmer* (`pragmatic-practices`) and the *Accelerate* and *Continuous Delivery* literature. Not generated from the vault.

## Small and frequent

Small changes are easier to review, reason about and undo. Integrate often, keep the main branch releasable, and don't let branches live long. When a change is large, ship it dark behind a flag or through expand and contract.

## CI

A change should pass at least: build, type check, lint, tests, and a dependency and secret scan where available. Keep it fast. A red build is everyone's first priority. Don't bypass checks to get a release out. If one is wrong, fix it, and say so.

## Feature flags

They separate deployment from release, and allow a fast off switch. Costs: more code paths, more to test, and stale flags that nobody removes. Give each one an owner and a removal plan. Decide the default when the flag service is down. Don't use a flag as a security control unless the check happens on the server.

## Rollouts

Use what the platform provides: rolling, blue-green or canary. Watch error rate and latency, and define beforehand what triggers a rollback. Be prepared to do it quickly.

## Rollback and compatibility

During a deploy, old and new versions run together, and a rollback brings the old one back. So:

- **Data:** new code must tolerate old data, and old code must tolerate new data. Use expand and contract for schemas and message formats.
- **Contracts:** add first and remove later, across services.
- **Irreversible steps,** like dropping a column or sending emails, need a separate later release. Back up before destructive migrations, and test the restore.

## Configuration

Keep what varies per environment outside the code, validate it at startup, and give safe defaults. Treat configuration changes like code: reviewed and versioned, because they cause many outages. Secrets go in a secret manager.

## Before shipping

Ask only what applies to this change: Is there a way to turn it off? How will we know that it's working? What if the dependency it adds is down? Does it handle real data volumes? Does anyone need to know about it, like support, or API clients? Is it documented where people will look?

Deploying, running migrations on shared data and flipping production flags reach other people, so get a go-ahead first, and report what happened.
