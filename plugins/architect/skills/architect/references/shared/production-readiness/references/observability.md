# Observability

Hand-written summary of common practice, drawing on the Google SRE book's golden signals and OpenTelemetry concepts. Not generated from the vault.

## Logs

Logs answer what happened to this particular request.

- **Structured:** key-value or JSON rather than sentences, so they can be queried. Follow the project's logger.
- **Correlation:** include a request or trace ID, and pass it across calls, queues and jobs.
- **Useful fields:** the operation, entity IDs, outcome, duration and error type.
- **Levels:** `error` means someone should look at it, `warn` is unexpected but handled, `info` covers significant business events, and `debug` is off in production. If a level is too noisy, people stop reading it.
- **Log an error once,** at the point where it's handled, with its stack and context. Logging at every layer produces duplicates. Wrap errors to add context as they move upward.
- **Never log** secrets, tokens, passwords or unneeded personal data. Watch out for logging whole objects or request bodies.
- **Cost:** avoid heavy logs in hot loops; sample if necessary.

## Metrics

Metrics answer how the system is doing overall.

- **Services:** request rate, error rate, duration (RED). Google SRE's golden signals add saturation.
- **Resources:** utilization, saturation, errors (USE) for pools, queues, disks and memory.
- **Business:** orders placed or messages processed, which often reveal what technical metrics miss.
- **Percentiles,** not averages, for latency: p95 and p99 show what's hidden in a mean.
- **Cardinality:** don't use user IDs or free text as labels; each label combination is a time series. Put those in logs and traces.

## Traces

A trace follows one request across services as spans. Use it to find where the time goes in distributed flows. Propagate context through HTTP headers and message metadata. OpenTelemetry is the vendor-neutral standard, with SDKs for most languages. Don't add tracing to a single process with few calls just because it's possible.

## Alerts

Alert on symptoms users feel, tied to objectives: error rate or latency over budget. Every alert should need action by a person and link to what to do. A noisy alert will get ignored.

## Error reporting and health checks

Send unexpected exceptions to the error tracker with release version and context. Keep **liveness** ("the process is not stuck") separate from **readiness** ("it can take traffic now"). Don't make liveness depend on a database, or an outage there will restart every instance.
