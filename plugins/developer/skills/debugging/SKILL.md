---
name: debugging
description: "Finds the root cause of failures in any language with a reproduce, hypothesize and prove method, using The Pragmatic Programmer. Use whenever behavior is wrong and the cause is unknown: a stack trace, a bug report, a crash or hang, an intermittent or flaky failure, something broken only in production, a fix that didn't hold, or someone stuck on an error, even if they only paste the message. Covers \"por qué falla\", \"no entiendo este error\", \"falla a veces\", \"arreglá este bug\" and \"en mi máquina anda\". Not needed when the cause is already evident from the error; for writing regular tests use testing; to add logging or retries use production-readiness."
---

# Debugging

This skill carries a personal study of debugging as reference files. Use it to **diagnose** a failure or **fix** one. Its point of view: debugging is problem solving, and a fix that isn't tied to a proven cause is a guess. Code that starts working without an explanation is still broken.

Scale it to the problem. If the error plainly says what is wrong and the fix is obvious, fix it and verify.

## Method

1. **Read what the failure says.** The complete error, the stack trace and the logs. Note exact symptoms, inputs and environment. Find out what changed recently.
2. **Reproduce it.** Aim for one command, ideally a failing test. If you can't reproduce it, you don't understand it yet: gather data about when it happens instead of guessing, and add logging if needed. Say explicitly when you could not reproduce it.
3. **Narrow it down.** Binary search through the input, the call path or the history (`git bisect`). Compare a working case to a failing one and look at actual state, not what the code seems to say.
4. **State a hypothesis and test it.** Say what would be true if it's right, then check. Change one thing at a time. If a result contradicts the hypothesis, discard it. Suspect your own code before the compiler, the OS or a well-used library, but check versions and documentation rather than assuming.
5. **Fix the cause, not the symptom.** Explain why the failure happens and why the fix addresses it. A retry, a sleep, a null check or a catch that makes the error disappear needs a reason. Keep the fix minimal.
6. **Confirm and look around.** Run the failing test and the related suite. Keep the regression test. Search for the same pattern elsewhere, and ask why nothing caught this earlier.

If three reasonable attempts fail, stop, restate what is proven and what is assumed, and question the premise. Look at whether the bug is where you think it is, and whether you're running the code you edited. Agents and people both tend to settle on the first plausible cause, so ask what else would explain the symptom.

## Intermittent failures

"Sometimes" means a variable you aren't controlling yet. Check, in this order of likelihood for the context: shared mutable state and check-then-act races, ordering assumptions, test pollution, time zones and clocks, unseeded randomness, resource exhaustion, retries, caches, and differences between environments. Treat patterns like "fails on Tuesdays" as a phantom until you find the mechanism. Force the condition: add concurrency, fix the seed, repeat the run many times.

Remove temporary debugging code when finished, unless it's useful logging worth keeping.

## Output

- **Cause:** what happens and why, with `file:line` and the evidence. Mark what is proven and what is a hypothesis.
- **Fix:** the change, or the proposal if only a diagnosis was requested. A question like "por qué falla" gets the diagnosis and an offer; "arreglá" gets the fix.
- **Verification:** the commands actually run and their results, including the test that failed before.
- **Follow-ups:** other instances found, or the check that would have caught it.

## Reference files

| File | Read when the topic is… |
|---|---|
| `references/method.md` | debugging tactics, programming by coincidence, getting unstuck, daybook, tools |
| `references/production-and-tools.md` | failures only in production, tools by symptom (hangs, leaks, crashes, regressions, environments), common traps |
| `references/failure-sources.md` | crashing early, assertions, contracts, resource ownership, mutable data, races and defensive concurrency |
