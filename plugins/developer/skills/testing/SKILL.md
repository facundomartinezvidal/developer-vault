---
name: testing
description: "Writes and reviews automated tests and makes code testable, in any language. Use when behavior needs tests, mocks are brittle, a suite is slow or flaky, code has no tests, or for TDD and coverage (\"qué debería testear\", \"cómo testeo esto\"). An unknown failure: debugging."
---

# Testing

This skill carries a personal study of testing as reference files. Use it to **write** tests, **review** a suite or **advise** on testing strategy. Its point of view: a test earns its keep by catching regressions and allowing change without fear. Writing it is also the first use of the code's interface, so a painful test is design feedback.

## Choosing what to test

Start from behavior and risk, not from classes or a coverage number. For this code, ask what would hurt if it broke and what is most likely to break.

- Cover the rules, boundary values, error paths and the states that matter. Coverage shows what never ran, not what was checked.
- Add a regression test for every bug, and test around it: bugs cluster.
- Test through the most stable interface that can still fail for the right reason. Coupling tests to internals or a GUI makes them block refactoring.
- Skip trivial getters, framework behavior and mirrors of the implementation.

Use the project's test framework, layout and helpers. Check how similar code is tested before introducing a new style. Choose the level by where the risk is: unit tests for rules, integration tests against real dependencies for queries and wiring, and a few end-to-end tests for critical journeys. `references/test-doubles-and-levels.md` has the details.

## Writing a good test

- **One concept per test,** named for the behavior: `overdue_invoice_blocks_new_orders`. A failure should say what broke.
- **Build, operate, check,** with no noise. Hide irrelevant setup in helpers that read like the domain.
- **F.I.R.S.T.:** fast, independent, repeatable, self-validating, timely. Control time, randomness, network and ordering.
- **Assert on outcomes,** not on how they were produced. Verify that the test can fail: check that it goes red when the behavior is broken.
- **Doubles only at real boundaries:** slow, nondeterministic or external collaborators. Mocking everything tests the mocks and freezes the design. Prefer real objects or simple fakes, and keep some tests against real dependencies where the integration is the risk.
- **Properties** suit parsers, serialization round trips, math and invariants. Generated inputs find assumptions you share with your examples.

Don't weaken an assertion, add sleeps or mark a test as skipped to get to green: a green result is only worth something if the test could have failed. A flaky test is either a bug in the test or a race in the code; find out which.

## TDD

The sources disagree. Martin treats it as discipline, Hunt and Thomas value the thinking but warn against losing the big picture, and Ousterhout calls it tactical apart from bug fixes. Don't impose one: use test-first when the behavior is clear, or fixing a bug; sketch first when the interface is still unknown. If the user asks for TDD, do it strictly: fail, pass, refactor.

## When code is hard to test

Name what makes it hard: a hidden clock, a global, `new` inside logic, I/O mixed with decisions. Then make the smallest change that fixes it: inject the dependency, split decisions from effects with a Humble Object, or pass values instead of fetching them. With untested legacy code, find a seam, capture current behavior in characterization tests, then change the structure; `references/legacy-and-flaky.md` gives the steps. Don't redesign just to reach a coverage figure.

## Output

**Writing:** the tests, run, with the actual result. State what isn't covered and why. If you find a bug, report it; don't encode it as expected behavior without saying so.

**Review:** findings most costly first, with `file:line`: tests that can't fail, gaps in risky behavior, coupling to internals, flakiness and slow setup. Say what is fine.

**Strategy:** a few focused recommendations for this system, what to test first and what not to test. Do not propose a generic test pyramid.

## Reference files

| File | Read when the topic is… |
|---|---|
| `references/writing-tests.md` | clean tests, F.I.R.S.T., test as first user, TDD positions, property-based testing |
| `references/test-doubles-and-levels.md` | unit, integration, contract and end-to-end tests; what to cover; stubs, fakes, spies and mocks; test data and isolation; mutation testing |
| `references/legacy-and-flaky.md` | code without tests, characterization tests, seams, sprout and wrap, flaky test causes, slow suites |
| `references/testable-code.md` | fragile tests, test boundary, Humble Object, separating construction, build automation and what to automate |
