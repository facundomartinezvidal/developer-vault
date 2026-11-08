---
name: clean-code
description: "Makes code readable at the level of names, functions, comments, error handling and async code, in any language. Use when code is hard to follow, a name misleads or errors are swallowed (\"esta función es muy larga\"). Step-by-step restructuring: refactoring; whole PRs: reviewing-code."
---

# Clean Code

This skill carries a personal study of readable code as reference files. Use it to **write**, **review** or **explain** code. Its point of view: the reader is the customer. Code is clean when someone new can understand it and change it safely, not when it satisfies a metric.

## Scope and evidence

Work on the code in front of you and its immediate callers. Read the project's conventions first; consistency with the surrounding code usually beats a locally better style. Many examples are in Java, so translate them into the idioms of the language at hand: a `Result` type, an `if err != nil` or a dataclass may be the clean form there. `references/across-languages.md` maps the ideas across language families. Use `refactoring` for a sequence of behavior-preserving steps, and `testing` for the tests themselves.

## The core checks

Apply only the checks that reveal a real cost in this code.

- **Names.** Does the name say what it is and why it exists, in the domain's terms? Is one word used for one concept throughout? Length should grow with scope.
- **Functions.** Does the function do one thing at one level of abstraction? Can you describe it without "and"? Size is a clue, not the rule: Martin wants very small functions, and Ousterhout warns that many shallow ones scatter the logic. Split when the piece has a name that hides detail worth hiding, not to reach a line count.
- **Arguments and side effects.** A flag argument usually means two functions. Several values that travel together may want a type. A function should either answer or act, and hidden ordering should be made visible through its data flow.
- **Comments.** Fix the code first if a comment only restates it or apologizes for it. Keep or add comments for what code cannot say: why, intent, units, invariants, non-obvious consequences and the contract of an interface. The sources disagree here; decide by what the next reader would otherwise have to rediscover.
- **Objects and data.** Objects hide data and expose behavior; data structures expose data and have no behavior. Hybrids get the cost of both. Check cohesion: do the methods use the same fields?
- **Errors.** Keep the happy path readable, and make failure handling explicit. Don't return null where an empty result works, don't swallow errors, and include enough context to act. Validate at trust boundaries, fail fast on violated assumptions, and don't turn recoverable input errors into crashes.
- **Resources and boundaries.** Whoever acquires a resource releases it, including on failure. Wrap a third-party API only when it isolates real volatility or simplifies its use.
- **Concurrency.** Name what is shared. Check-then-act on shared state is a bug until proven otherwise. Prefer immutable data and message passing, and keep the concurrent part small and separate.

## Modes

### Write

Get it working, then clean it before calling it finished: first drafts are rarely clean, including yours. Match the file's existing style. Don't add abstractions, parameters or error handling for situations that cannot occur here.

### Review

Report findings most costly first:

- **What and where,** with `file:line`.
- **The cost:** what a reader will misread or what change it makes harder.
- **The fix,** concretely, with a short before and after when it helps.

Separate defects from preferences, and label preferences as such. Leave out what the formatter or linter already enforces. Say what is fine, and don't flag small code for failing a rule of thumb.

### Explain

Give the idea, a realistic example in the user's language, and where the sources disagree.

## Reference files

Read the one that matches the topic before answering in depth.

| File | Read when the topic is… |
|---|---|
| `references/foundations.md` | what clean code is, simple design rules, obviousness, consistency, formatting, successive refinement |
| `references/names-and-functions.md` | names, function size and arguments, abstraction levels, command-query separation, hidden call order |
| `references/comments.md` | whether and how to comment, comments as design |
| `references/objects-and-classes.md` | objects vs. data structures, cohesion, construction vs. use, tell-don't-ask, SOLID on classes |
| `references/errors-and-boundaries.md` | exceptions, null, contracts, crash early, assertions, resource ownership, third-party code, basic safety |
| `references/concurrency.md` | shared state, race conditions, ordering, actors |
| `references/async-and-parallelism.md` | async/await, threads, cancellation, deadlocks, bounded concurrency, testing concurrent code |
| `references/across-languages.md` | how these principles look in other languages, type systems and memory models; finding a project's tools |
