# Tooling and automation

Version control, automation, plain text, configuration and keeping systems safe.

## Contents

- [Version Control](#version-control)
- [Pragmatic Starter Kit](#pragmatic-starter-kit)
- [The Power of Plain Text](#the-power-of-plain-text)
- [Externalize Configuration](#externalize-configuration)
- [Stay Safe Out There](#stay-safe-out-there)

## Version Control


**Source:** *The Pragmatic Programmer*, Topic 19 (also Tip 89).

### What it means in practice

Version control is a project-wide undo button and time machine, and much more:

- **Everything goes in it**: code, docs, configuration, infrastructure, even personal dotfiles and notes, not just "source".
- **Shared directories aren't version control.** Something will overwrite something else.
- **Branches** isolate experiments and features, which keeps them orthogonal.
- **It's a project hub.** Pushes trigger builds, tests and deploys. Configuration is versioned and auditable.
- Ask who changed this line, when and why. Answer "what was in the release that broke?". Bisect to find the commit that caused a regression.

### Example

```bash
git bisect start v2.14.0 v2.13.0       # last known good / first known bad
git bisect run ./gradlew test --tests "*InvoiceRoundingTest"
# → the first commit that broke rounding, with its author and message
```

### Related

- Pragmatic Starter Kit — version control is the first item.
- The Power of Plain Text — diffs and merges need text.
- Reversibility (`approaching-work.md`) — every commit can be reverted.
- Stay Safe Out There

## Pragmatic Starter Kit


**Source:** *The Pragmatic Programmer*, Topic 51 (Tips 89–95).

### What it means in practice

Every project needs three basics before anything else:

1. **Version control** drives builds, tests and releases (Tip 89). A push triggers everything, and a tag deploys.
2. **Ruthless, continuous testing:**
   - Test early, often, and automatically.
   - Coding isn't finished until all the tests pass (Tip 91).
   - Test at every level: unit, integration, validation and verification, performance and stress, usability.
   - **Use saboteurs to test your testing** (Tip 92). Deliberately introduce bugs (mutation testing) to make sure the tests notice.
   - **Test state coverage, not code coverage** (Tip 93).
   - **Find bugs once** (Tip 94). Every bug a human finds becomes an automated test, so it can't come back.
3. **Full automation.** Builds, deploys, database migrations and releases are scripts, never a wiki page of manual steps (Tip 95). Manual procedures don't get repeated the same way twice.

### Example

```yaml
# .github/workflows/ci.yml — the starter kit in one file
on: [push, pull_request]
jobs:
  build:
    steps:
      - run: ./gradlew spotlessCheck test integrationTest   # formatting + all tests, every push
      - run: ./gradlew pitest                                # saboteurs: mutation testing
      - if: startsWith(github.ref, 'refs/tags/v')
        run: ./deploy.sh production                          # no manual release steps
```

### Related

- Version Control
- Tracer Bullets (`approaching-work.md`) — the first slice runs through this pipeline.
- Pragmatic Teams (`working-with-people.md`)
- Stay Safe Out There

## The Power of Plain Text


**Source:** *The Pragmatic Programmer*, Topic 16.

### What it means in practice

Plain text is made of printable characters that people can read and understand directly, ideally self-describing (`<deadline>2026-11-30</deadline>` rather than `11302026`). Binary formats separate the data from its meaning. Without the right program, the data is useless.

Why plain text wins:
- **Insurance against obsolescence.** Readable data outlives the application that wrote it.
- **Leverage.** Every tool works on it: `grep`, `diff`, editors, version control, scripts.
- **Easier testing.** Test fixtures and expected outputs are easy to write, read and change.

The costs are size and parsing time, which rarely matter today. Secrets can be encrypted, and the metadata around them can still be plain text.

### Example

Infrastructure as code (Terraform), configuration in YAML, database migrations as SQL files, architecture decisions as Markdown ADRs, and this vault itself as Markdown notes. All of them are diffable, reviewable in PRs, searchable, and readable in 20 years without the original tool.

### Related

- Version Control — diffs and merges need text.
- Externalize Configuration

## Externalize Configuration


**Source:** *The Pragmatic Programmer*, Topic 32.

### What it means in practice

Values that may change after the code ships don't belong in the code: credentials, service URLs, feature flags, tax rates, timeouts, license details. Put them in configuration so they can change without a rebuild. Hunt & Thomas add two refinements:

- **Wrap configuration behind your own API** instead of letting the whole codebase read a global YAML or environment hash. The format and location then become a detail.
- **Configuration-as-a-service.** Serve configuration from an API instead of static files. Many instances can share it, changes can be audited and access-controlled, and running apps can pick up changes without restarting.

The caution: don't overdo it. Making everything configurable ("let's make the business logic a config file") pushes complexity into configuration that nobody tests.

### Example

```java
// Hard-coded: a deploy to change a timeout
HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(3));

// Externalized and wrapped: one typed API, any source behind it (env, file, config service)
public record PaymentConfig(URI providerUrl, Duration timeout, boolean threeDsRequired) {}
var http = HttpClient.newBuilder().connectTimeout(config.payment().timeout());
```

### Contrast with Ousterhout

pull complexity downwards warns that configuration parameters can be a way of *exporting* complexity. Instead of making a decision, the module makes every user decide. Externalize what really varies between deployments, and let the code compute sensible defaults for everything else.

### Related

- The Power of Plain Text — config files are plain text by design.
- Reversibility (`approaching-work.md`)
- Stay Safe Out There — secrets are configuration and must never be in the repository.
- The Requirements Pit (`approaching-work.md`)

## Stay Safe Out There


**Source:** *The Pragmatic Programmer*, Topic 43.

### What it means in practice

Once code works on the happy path, it's tempting to call it done. Hunt & Thomas list the basic security principles that are easy to forget:

1. **Minimize attack surface.** Complexity creates attack vectors. Validate all input, don't trust anything from outside, keep unauthenticated services to a minimum, limit the number of authenticated users, and turn off features and debug output you don't need. Don't leak information in error messages.
2. **Principle of least privilege.** Grant the lowest permission level, for the shortest time, that does the job.
3. **Secure defaults.** The default configuration should be the safe one. Users opt *in* to less safety.
4. **Encrypt sensitive data.** Never commit secrets, API keys or passwords to Version Control. Use config or a secret store. Don't roll your own crypto.
5. **Keep up with security patches.** Most large breaches exploit known vulnerabilities that were never patched.

Also: use proven password-handling and authentication practices (NIST guidance, long passphrases, MFA) instead of inventing rules.

### Example

A file-upload endpoint: authenticated users only; size and MIME-type limits; filenames generated server-side; stored in a bucket with no public access; the API's IAM role can write only to that one prefix; Dependabot alerts set to auto-merge patch updates.

### Related

- Externalize Configuration — secrets live outside the code.
- Pragmatic Starter Kit
- Take Responsibility (`working-with-people.md`) — "first, do no harm".
