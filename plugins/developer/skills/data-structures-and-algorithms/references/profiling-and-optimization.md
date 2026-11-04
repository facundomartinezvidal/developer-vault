# Profiling and optimization

Hand-written from common practice; not generated from the vault. It complements `designing-for-performance` in `complexity.md`.

## Method

1. **Define the goal.** What's slow, for whom, and what's the target? Without one, you don't know when to stop.
2. **Reproduce with realistic data and load.** Small data hides quadratic behavior. Use a production-like build, since debug builds mislead.
3. **Measure.** Find where the time actually goes before changing anything. Intuition about this is unreliable.
4. **Fix the largest cost first,** one change at a time, and measure it again. Keep the change only if it's worth its complexity.
5. **Guard it.** Add a benchmark or budget if this path matters.

## Tools, by kind

Sampling profilers show where CPU time goes: `pprof`, `perf`, `py-spy`, `async-profiler`, Chrome DevTools, `dotnet-trace`, Instruments. Flame graphs are a good way to read them. Use memory profilers for allocations and leaks. For services, distributed traces show which call is the slow one. For queries, read `EXPLAIN`. Use the ecosystem's benchmark harness (`pytest-benchmark`, `go test -bench`, JMH, `criterion`), because hand-rolled timing is misled by warm-up, caching and compiler optimizations. Run several times, and compare distributions: p95 and p99, not only averages.

## Usual suspects, roughly by payoff

- **Round trips:** N+1 queries, an API call in a loop. Batch them.
- **Work you don't need:** loading whole tables, unused columns, recomputing. Filter earlier, paginate, or stream.
- **Wrong structure:** list membership in a loop, repeated sorting, string building by concatenation.
- **Missing index,** or a query that can't use one.
- **Serialization and logging** in hot paths.
- **Allocation pressure:** reuse buffers where it's been measured to matter.
- **Contention:** locks, connection pools, or one slow dependency.
- **On the front end:** large bundles, unnecessary re-renders, unoptimized images.

## Caching

Caching trades speed for staleness and complexity. Define the key, including everything the result depends on such as the user or locale, as well as invalidation, a size limit and what happens on a miss storm. Don't cache permission-sensitive data under a shared key. Fix the underlying slowness first if you can.

## Reporting

State the input, environment, the before and after, and how it was measured. Don't claim a speedup you haven't measured.
