# Legacy code, flaky and slow tests

Hand-written, in our own words. It draws on *Refactoring*, Chapter 4, and common practice, with terms from Feathers's *Working Effectively with Legacy Code*, which isn't in the vault. It applies to any language.

## Changing code without tests

Legacy code here means code that you must change and that has no tests guarding it. The loop:

1. **Identify the change point.** Find the smallest area that needs to change.
2. **Find a test point:** where you can observe the effect, such as a return value, output or a record written.
3. **Break just enough dependencies** to run it under test, using the lowest-risk edits you can. Mechanical changes by a tool are preferred.
4. **Write characterization tests** that record what the code does now.
5. **Make the change,** using tests to guide it, and refactor.

## Characterization tests

They document actual behavior rather than intended behavior. Write an assertion you expect to fail, run it, and copy the real result in. Add cases until they cover the paths you're changing. If the behavior looks wrong, don't correct it silently: keep the test with a comment, and report it, since callers may depend on it.

**Golden master:** capture the output of a whole flow for many inputs and compare it to the stored version. It's cheap, covers plenty and doesn't explain why something failed. Normalize timestamps, IDs and ordering, and treat it as scaffolding.

## Seams

A seam is a place where behavior can be changed without editing the code at that point. Common options in most languages:

- A parameter: pass the dependency, clock or function in, defaulting to the current one so callers don't change.
- An interface or a subclass that overrides one method.
- A module-level replacement: an import, a linker symbol or a monkeypatch. It's useful as a first step when nothing else is possible.

## Adding code safely

- **Sprout:** write new behavior in a new tested function or class, and call it from the old code with minimal edits.
- **Wrap:** rename the old method, create a new one with the original name that adds behavior and calls the old one. This suits behavior that happens before or after.

Don't try to cover everything first. Add tests where you're changing things; coverage grows around the areas that actually change.

## Flaky tests

A flaky test passes and fails on the same code. It destroys trust, so people begin to ignore real failures. Treat it as a bug, and find the mechanism before changing anything:

| Symptom | Likely cause | Fix |
|---|---|---|
| Depends on order, or fails only in the full run | Shared state, leftover data, global mocks | Isolate state and reset it |
| Fails at certain times or dates | Real clock, time zones, end of month | Inject the clock |
| Fails under load or in CI | Timing, fixed sleeps | Await the condition, with a timeout |
| Different results between machines | Locale, paths, line endings, versions | Pin or normalize |
| Random failures | Unseeded randomness, unordered iteration | Seed and log the seed; sort it or compare as a set |
| Occasional failures with concurrency | A real race in the code | Reproduce it by repeating the test; fix the code |
| Network failure | External dependency | Fake it, or run it locally |

Run the test many times, alone and in the suite. A retry can hide a real race, so it's only a temporary measure, recorded along with the reason. If you quarantine a test, track who will fix it.

## Slow suites

Measure first: most of the time usually comes from a few tests. Then replace sleeps with waits, avoid repeated expensive setup, push rules down to lower levels, and run in parallel once the tests are isolated. A fast suite gets run, and a slow one doesn't.
