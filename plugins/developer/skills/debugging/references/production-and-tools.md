# Production failures and tools by symptom

Hand-written from common practice; not generated from the vault.

## When it only happens in production

First limit the damage. If a recent release is the likely cause, rolling back or turning off a flag often comes before understanding it; that's the owner's call. Then:

- Find when it started, and compare it with deploys, configuration, traffic and dependency changes.
- Compare environments: versions, configuration, data shape and volume, permissions, and network.
- Follow one failing request with its correlation ID through logs and traces.
- Get a sample of the data that triggers it, and reproduce it locally, without copying sensitive data.
- Don't debug by changing production. Reading is fine, but changes need a go-ahead.

Afterward, write down the cause, why nothing caught it, and which check or alert would have. Blame systems, not people.

## Tools by symptom

| Symptom | Reach for |
|---|---|
| Crash with a trace | Read from the first frame in your own code; check the cause chain |
| Wrong result | Debugger or logging at each step; compare a working input with a failing one |
| Regression, unknown commit | `git bisect` with a scripted test |
| Hang | Thread or goroutine dump, `py-spy dump`, `jstack`, `gdb`; look for locks and waits on I/O |
| Memory growth | Heap profiler; compare two snapshots |
| Native crash, corruption | AddressSanitizer, UBSan, Valgrind, core dump |
| Data race | Race detector, ThreadSanitizer, repeating the run |
| Slow | Profiler, trace, `EXPLAIN` |
| "Can't find file or connect" | `strace`, `dtruss`, `lsof`, `curl -v`, DNS and environment checks |
| Works in one environment | Diff versions, lockfiles, environment variables, and clean caches |
| Build or dependency failure | Read the first error, not the last; check the lockfile and tool version |
| Network or API | Logging the request and response, without secrets; a recorded replay |

## Traps

- **Fixing the first plausible cause.** Agents and people jump to one. Ask what else would explain it, and what evidence would rule this out.
- **Clearing the symptom.** Removing a cache or rerunning may make it pass while the cause remains.
- **Changing several things at once,** so that you learn nothing.
- **Trusting stale state:** old builds, running servers with old code, or a wrong working directory. Verify that what you run is what you edited.
