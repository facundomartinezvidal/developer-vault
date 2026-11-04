---
name: software-design
description: Evaluates and improves the design of modules and their interfaces using A Philosophy of Software Design and The Pragmatic Programmer — complexity, deep vs. shallow modules, information hiding, coupling, contracts, error handling, and concurrency. Use it whenever someone designs an API or internal module, asks whether code is well designed or over-engineered, has layers that only pass calls through, finds that small changes touch many files, needs to decide whether to merge or split something, or wants to reduce coupling, or handle errors or shared state better, even if they never mention these books. Also covers Spanish requests like "está bien diseñado", "cómo diseño esta interfaz", "está sobreingeniería", "muy acoplado", "cada cambio toca muchos archivos", "lo separo o lo junto". Not for line-level style, naming and formatting, nor for system-wide layering, which Clean Architecture covers.
---

# Software Design

This skill carries a personal study of how to keep software easy to change, at the scale of modules and interfaces, as reference files. Use it to **review** a design, **design** a new module, or **explain** a principle. Its point of view: complexity is the enemy, and every design choice is judged by whether it makes future work easier.

## The core model

- **Complexity is what makes a system hard to understand and change.** It shows up as change amplification (one change touches many places), cognitive load (how much you must know to act), and unknown unknowns (not knowing what you must know). Name which one a problem causes, because that keeps the conversation away from taste.
- **Prefer deep modules.** A good module gives a lot of functionality behind a small interface. The interface is the cost, the functionality is the benefit. Many tiny classes aren't automatically good: each adds an interface someone must learn.
- **Hide decisions.** Each module should own a piece of knowledge. The same format, order or rule known by two modules is information leakage, even if no code looks duplicated.
- **Pull complexity downward.** When something must be complicated, let the module's author handle it, not every caller. A configuration parameter is often a decision passed to someone who knows less.
- **Each layer needs its own abstraction.** Pass-through methods and wrappers that add nothing are a red flag. So are layers with near-identical signatures. Clean Architecture sometimes justifies a thin boundary to protect policy from a detail; that's a deliberate cost and should pay for itself.
- **Design it twice.** First ideas are rarely best. Compare genuinely different interfaces before choosing.
- **Define errors out of existence.** Prefer semantics where the failure case can't occur (deleting something that's already gone succeeds) to adding exceptions every caller must handle. Where failure is real and can't be handled meaningfully, fail early and loudly.
- **Invest strategically, in proportion.** Small, continuous design investment beats both tactical hacking and big speculative frameworks.

These principles pull against each other and against other books: small functions vs. deep modules, DRY vs. accidental duplication, comments vs. self-documenting code. When they conflict, say so and decide by the concrete change cost here rather than citing an authority.

## Modes

### Review

Read how the code is used, not just how it's written: callers reveal whether an interface is too wide or leaks. For each finding, most costly first:

- **What and where,** with `file:line`.
- **The symptom:** which form of complexity it causes, shown by a specific likely change ("adding a storage backend means editing these 4 files").
- **The fix,** concretely, with the new interface as code when it matters.

Close with what's fine, and what you'd leave alone. Don't raise hypothetical problems as defects or recommend abstractions for a variation that isn't on the horizon. If code is simple and small, say so: extra indirection is itself a design cost.

### Design

Clarify what callers need to do, and what's likely to change. Then:

1. Sketch **two or three really different interfaces** (for example, narrow and general-purpose vs. one method per use case), briefly, showing how a caller would use each.
2. Compare them by caller simplicity, what each hides, and how each copes with the likely change.
3. Recommend one, with its signature and its contract: what it promises, what it requires, how failure behaves.

Aim for "somewhat general-purpose": the interface covers today's needs without being tied to them, and without features nobody needs yet.

### Explain

Give the principle, what it means in practice, a realistic example and how it relates to neighbours. Mention where the sources disagree.

## Reference files

Read the one that matches the topic before answering in depth; each has a table of contents, so jump to the section you need.

| File | Read when the topic is… |
|---|---|
| `references/complexity.md` | what complexity is, tactical vs. strategic work, how to change existing code, consistency, small steps, performance |
| `references/modularity.md` | deep modules, information hiding, generality, pass-through layers, together vs. apart, orthogonality, DRY |
| `references/coupling.md` | decoupling techniques, interfaces, composition vs. inheritance, Law of Demeter, tell-don't-ask, events, pipelines, configuration |
| `references/robustness-and-testability.md` | contracts, crashing early, assertions, reducing exceptions, resource ownership, what tests reveal about design |
| `references/concurrency.md` | shared state, temporal coupling, actors, blackboards, defensive concurrency |
