# Test doubles and test levels

Hand-written, in our own words. It draws on *Refactoring*, Chapter 4, *Agile Principles, Patterns, and Practices*, Chapter 4 and common practice, with terms from Meszaros's *xUnit Test Patterns*. It applies to any language; use each ecosystem's own tools.

## Levels

Names vary between teams, so describe what a test does and follow the project's vocabulary.

| Level | What runs | Finds | Costs |
|---|---|---|---|
| Unit | Logic with no I/O; a function or a small group of objects | Wrong rules, edge cases | Very fast; can be coupled to structure if too small |
| Integration | Your code with a real database, queue or file system, ideally in a container or temp directory | Wrong queries, mapping, transactions, configuration | Slower; needs setup |
| Contract | Both sides of a service boundary against a shared agreement | Drift between consumer and provider | Coordination |
| End-to-end, acceptance | The whole system through its UI or API | Wiring, critical user journeys | Slow and more flaky |

Have most tests where they are fast, and just enough at the higher levels to cover what lower ones can't see. The right mix depends on where the risk is. A thin CRUD app gains more from integration tests against a real database; a pricing engine gains more from unit tests. Don't test the same rule at every level.

A test should be replaceable by its behavior: "unit" means an independent unit of behavior, not necessarily one class. Testing a small cluster through its public interface survives refactoring better.

## What to cover

- **Happy path, then the boundaries:** empty, one, many, zero, negative, maximum, just past the limit, unexpected types, and Unicode.
- **Failure paths:** dependency down, timeout, partial success, retry, and invalid input. Check that the failure can be observed.
- **State transitions and invariants** that must hold.
- **Permissions:** the user who must be refused is refused.
- **Concentrate on risk:** where code is complicated or changes often. An incomplete suite that runs is far better than a perfect one that doesn't exist.

Coverage reveals what never ran, not whether anything was checked. Mutation testing asks a harder question: if this code is changed, does a test fail? Use it on critical logic when a tool exists for the language.

## Test doubles

| Double | What it does | Use it for |
|---|---|---|
| Dummy | Fills a parameter, is never used | Required but irrelevant arguments |
| Stub | Returns canned answers | Driving the code down a path |
| Fake | Simple working implementation, like an in-memory repository | Fast tests with realistic behavior |
| Spy | Records calls for later checks | Verifying an outgoing effect |
| Mock | Pre-programmed with expected calls, and verifies them | Interactions that are themselves the behavior |

Guidelines:

- **Prefer real objects** for your own pure logic, then fakes, then stubs. Use a mock or spy only when the interaction is the requirement, such as "the email was sent once".
- **Double only at boundaries you control.** Wrap a third-party client in your own small interface, double that, and test the wrapper against the real thing or its sandbox. Mocking types you don't own encodes guesses about how they behave.
- **Check the double stays faithful.** A fake needs its own contract tests, run against both it and the real implementation.
- **Don't assert incidental calls.** Verifying every internal call pins the implementation, so correct refactors break tests. If a test needs many mocks, the code has too many collaborators.
- **In dynamic languages,** patching at runtime is easy, and it is not free. Dependency injection through parameters or small interfaces usually reads better, and stops the double drifting from the real signature.

## Test data and isolation

Build data through small helpers or builders that default the irrelevant fields, so a test shows only what matters. Avoid shared fixtures that many tests modify. Each test should create its own state, or run in a transaction that rolls back. Control the clock, seed randomness, and don't assume ordering of unordered results.
