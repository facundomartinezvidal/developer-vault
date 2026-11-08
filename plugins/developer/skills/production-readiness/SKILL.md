---
name: production-readiness
description: "Makes code behave well in production with logging, metrics, tracing, timeouts, retries, graceful failure and safe releases. Use when code calls other services, runs as a job or consumer, or is about to ship (\"agregá logs\", \"está listo para producción\"). A known failure: debugging."
---

# Production Readiness

Use this skill to **add** operational behavior to code, **review** whether a change is ready to ship, or **advise**. Its point of view: in production everything eventually fails, usually at the seams, so code has to fail in known ways and leave enough evidence for someone to work out what happened.

Scale it. A script or an internal tool doesn't need tracing, circuit breakers or canaries. Read what the project already uses for logging, metrics, flags and deployment, and extend that. Don't introduce a new platform for one change.

## Questions to ask of a change

1. **What can fail?** Every call across a network, disk, or process boundary can fail, hang or succeed without you finding out.
2. **What happens then?** Does the user see a clear error, does work retry, is data partly written? Is that outcome acceptable?
3. **How would we know?** Would a log, metric or alert show it, and with enough context?
4. **How do we undo it?** Can this be rolled back, or turned off, including its data changes?

## Core practices

- **Timeouts on every remote call.** Defaults are often infinite, and hung calls take the system down with them. The deadline must fit inside the caller's own.
- **Retry only what's safe and transient.** Use limits, exponential backoff and jitter, and retry at one level. A retry on a non-idempotent call can duplicate effects, so see the idempotency guidance in `references/resilience.md`.
- **Decide how to degrade.** Fail fast, return partial results, serve stale data, or queue it. That's a product decision when it changes what users see, so raise it.
- **Structured logs** at the boundaries and on failure, with correlation IDs and identifiers, without secrets or unneeded personal data.
- **Measure what matters to users:** rate, errors, duration. Alert on symptoms, not on every cause.
- **Separate deploy from release.** Use flags or gradual rollouts where a change is risky, and keep the old path available until the new one has proven itself.
- **Make data changes compatible** with both the old and new code, since both run during a deployment. See `relational-databases`.

## Output

**Adding:** code in the project's style, with a test that simulates the failure: a timeout, an error response or a duplicate message. Report what you ran.

**Readiness review:** the risks found, most serious first, with `file:line`, the scenario, and the fix. List what's fine. Separate what must happen before shipping from what can wait. Don't produce a generic checklist.

## Reference files

| File | Read when the topic is… |
|---|---|
| `references/observability.md` | logging, metrics, traces, correlation IDs, alerts, error reporting, health checks |
| `references/resilience.md` | timeouts, retries, backoff, idempotency, circuit breakers, queues, jobs, graceful shutdown |
| `references/safe-delivery.md` | CI checks, feature flags, gradual rollouts, rollback, configuration, compatibility during deploys |
