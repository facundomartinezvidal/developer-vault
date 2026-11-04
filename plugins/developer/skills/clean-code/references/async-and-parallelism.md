# Async and parallel code

Hand-written from common practice; not generated from the vault. It complements `concurrency.md`.

## Pick the model by the kind of work

- **Waiting on I/O:** async, event loops, lightweight threads or goroutines. Many tasks spend most of their time waiting.
- **CPU-heavy work:** real parallelism with threads or processes. CPU work on an event loop blocks everything else. In runtimes with a global lock, threads may not help.
- **Independent units with their own state:** actors or message passing.

## Common defects, in any language

- **Forgotten awaits and lost tasks.** A task started and not awaited hides its errors and may outlive its request. Use structured concurrency where available: task groups, `errgroup`, scopes.
- **Blocking the event loop** with synchronous I/O or long computation.
- **Unbounded concurrency.** `map` over 10,000 items starting 10,000 requests. Use a semaphore, worker pool or bounded queue.
- **Missing cancellation and timeouts.** Pass a context or token along, and stop work when the caller is gone.
- **Races.** Check-then-act, and unsynchronized read-modify-write. Async code has these too, across every `await`.
- **Deadlocks.** Locks taken in differing orders, and holding one while making a remote call or awaiting. Keep critical sections small, and use one global order.
- **Starvation and retry storms** under load.
- **Leaks.** Goroutines, tasks, timers and listeners that never end. Each one needs a defined way to stop.
- **Order assumptions.** Results may arrive in any order; unordered map iteration can vary as well.
- **Errors inside tasks.** Decide what happens if one of several fails: cancel the others, or collect partial results.

## Testing it

Passing once proves little. Control time and scheduling where possible, use latches instead of sleeps, repeat the test many times, and use a race detector if the language has one: `go test -race`, ThreadSanitizer. Rust's type system rules out data races in safe code, but not logic races.
