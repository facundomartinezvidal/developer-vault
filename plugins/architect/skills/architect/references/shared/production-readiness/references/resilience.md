# Resilience

Hand-written summary of common practice, drawing on Nygard's *Release It!* stability patterns. Not generated from the vault. Use the language's standard libraries or the project's existing tools for these.

## Timeouts and deadlines

Set connection and read timeouts on every remote call, database query and lock. Choose them from observed latency, not guesses. Pass a deadline through the call chain, such as a context or cancellation token, so that downstream work stops when nobody's waiting.

## Retries

Retry when the failure is transient (a timeout, 429, 503, or a dropped connection) and the operation is safe to repeat. Don't retry validation errors, or anything else that can't succeed.

- **Backoff with jitter,** so that clients don't retry in unison. Honor `Retry-After`.
- **Limit** attempts and overall time. Consider a retry budget.
- **One layer only.** Three layers with three attempts each make 27 calls and can turn a slow service into a dead one.

## Idempotency

A timeout means that you don't know if it worked. Repeating it safely requires an operation identity. The caller generates a key, and the server stores it with the result under a unique constraint within the same transaction as the effect. A repeat returns the stored result. Upserts and absolute updates ("set to X") are naturally safer than relative updates ("add X"). When completion can't be determined, provide a way to look up the outcome or reconcile it.

## Isolating failures

- **Circuit breaker:** after repeated failures, stop calling for a while, and fail fast. Add one where a dependency's failure is common and costly, not everywhere.
- **Bulkhead:** give each dependency its own pool or limit, so a slow one can't take all the threads or connections.
- **Backpressure and load shedding:** use bounded queues. Reject excess work early with a 429 or 503 instead of accepting everything until memory runs out.
- **Fallbacks:** serve cached or default data only if that's acceptable, and make it visible in metrics. A silent fallback can hide an outage or lost work.

## Queues and background jobs

Most queues deliver at least once, so consumers must tolerate duplicates and, usually, reordering. Exactly-once delivery is rarely what it seems; aim for idempotent processing. Limit attempts, and send poison messages to a dead-letter queue that someone monitors. Don't ack until the work is done. Jobs should be resumable and keep track of progress.

To write to a database and publish an event reliably, use an **outbox**: save the event in the same transaction as the data, then publish it separately. Doing the two independently means that one can fail without the other.

## Transactions and external calls

Avoid holding a transaction open during a network call: locks stay held for as long as it takes, and an external effect can't be rolled back. Commit the intent first, then call out, then record the outcome.

## Shutdown and startup

On a termination signal, stop taking new work, finish or requeue what's running within a limit, then close connections. On start, check configuration and fail clearly if it's invalid; a crash at startup beats a failure at the first request. Consider what happens when many instances start at once and all reconnect or warm caches.

## Resources

Bound everything: pool sizes, queues, caches with eviction, request bodies, result sets and file handles. Unbounded structures fail only under real load, so test with realistic volumes and failure injection where it's worthwhile.
