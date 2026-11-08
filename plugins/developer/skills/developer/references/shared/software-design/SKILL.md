---
name: software-design
description: "Designs and reviews module interfaces: information hiding, what callers must know, call ordering, and failure or retry contracts. Use when one change spreads across modules, an API is easy to misuse or a layer adds nothing (\"cómo diseño esta interfaz\", \"lo separo o lo junto\")."
---

# Software Design

This skill carries a personal study of how to keep software easy to change, at the scale of modules and interfaces, as reference files. Use it to **review** a design, **design** a new module, or **explain** a principle. Its point of view: complexity is the enemy, and every design choice is judged by whether it makes future work easier.

## Scope and evidence

The unit of analysis is a module **and its callers**. Correct dependency direction does not prove that an interface hides useful knowledge. Follow one representative operation from caller to implementation, including failure paths; inspect the tests or contract when available. Distinguish observed costs from hypothetical changes. If callers or implementation are missing, state which conclusions remain provisional instead of inferring them from method names.

Use Clean Architecture when the question is who may depend on whom, and DDD when it is what business concepts or invariants mean. Here, focus on which knowledge an interface makes callers carry, and whether its behavioral promises are usable. Do not turn a local interface review into a project restructuring.

## The core model

- **Complexity is what makes a system hard to understand and change.** It shows up as change amplification (one change touches many places), cognitive load (how much you must know to act), and unknown unknowns (not knowing what you must know). Name which one a problem causes, because that keeps the conversation away from taste.
- **Prefer deep modules.** Judge interface cost by everything a caller must know: parameters, exposed formats, exceptions, ordering, lifetimes and failure semantics. A one-method API can still be expensive; fewer methods and lines alone do not establish depth. Many tiny classes are not automatically good.
- **Hide decisions.** Identify the specific knowledge (format, algorithm, protocol or storage layout), its owner and every place that must change when it changes. Private fields and interfaces do not hide a decision if callers still reconstruct it. Group code that shares this knowledge, even when a pipeline originally separated it by execution step; preserve genuinely independent responsibilities.
- **Pull complexity downward.** When something must be complicated, let the module's author handle it, not every caller. A configuration parameter is often a decision passed to someone who knows less.
- **Each boundary needs a purpose.** Similar signatures are a clue, not proof of redundancy. A thin adapter or decorator can enforce access, resource ownership, instrumentation or dependency isolation. Identify the guarantee it provides before merging it. Remove delegation that adds neither a meaningful abstraction nor a justified boundary; do not erase a guarantee to save a class.
- **Design it twice.** First ideas are rarely best. Compare genuinely different interfaces before choosing.
- **Simplify errors without hiding outcomes.** Treat an absent object as successful deletion if callers need only absence, but preserve failures that change what they should do. Distinguish expected rejection, dependency failure and an unknown outcome after a timeout. A successful-looking default must not conceal lost work or a partial side effect. Apply fail-fast to violated assumptions; do not turn recoverable input errors into process failure.
- **Invest strategically, in proportion.** Small, continuous design investment beats both tactical hacking and big speculative frameworks.

These principles pull against each other and against other books: small functions vs. deep modules, DRY vs. accidental duplication, comments vs. self-documenting code. When they conflict, say so and decide by the concrete change cost here rather than citing an authority.

## Contracts that callers can rely on

For the operation under discussion, specify the relevant inputs, result and observable side effects. Include only the dimensions that can change a caller's correct behavior:

- **Ordering and lifecycle:** who acquires/releases resources, and which steps must precede others. Prefer a cohesive operation or explicit state when callers otherwise coordinate a fragile protocol.
- **Failure and partial success:** what is guaranteed when the operation returns, rejects or times out; whether some work may already be committed. Expected per-item rejections may need explicit results rather than a single exception or success flag.
- **Retries and concurrency:** who retries, what identifies the same logical operation, and why repeats cannot duplicate effects when that matters. If completion is unknown, name a recovery/reconciliation path instead of promising safe retries. An in-process lock or a type signature does not establish atomicity across writers.
- **Policy versus mechanism:** hide provider details and safe mechanical defaults, but keep decisions the caller legitimately owns explicit. Do not bury business choices such as acceptable loss or fail-open behavior in a generic utility.

Make a proposed contract concrete with a signature and representative caller usage, including the failure path that motivates the change. A full implementation is unnecessary unless requested. Name a small observable check for a consequential guarantee; do not claim it was tested unless it was run.

## Modes

### Review

Trace a representative caller and the implementation before proposing changes. For each demonstrated finding, most costly first:

- **What and where,** with `file:line`.
- **The symptom:** which form of complexity it causes, shown by a specific likely change ("adding a storage backend means editing these 4 files").
- **The fix,** concretely, showing what knowledge or protocol moves to which owner and a caller before/after when useful. Preserve relevant guarantees during migration.

Close with what's fine, and what you'd leave alone. Don't raise hypothetical problems as defects or recommend abstractions for a variation that isn't on the horizon. If code is simple and small, say so: extra indirection is itself a design cost.

### Design

Clarify what callers need to do, and what's likely to change. Then:

1. For a consequential design choice, sketch two genuinely different interfaces with caller usage. For a small local change, give the direct recommendation; do not manufacture alternatives.
2. Compare the viable options by knowledge callers carry, guarantees preserved, and the specific change they make cheaper. Include keeping the current design when it already meets the need.
3. Recommend one, with its signature and behavioral contract. Explain what remains exposed and why; fewer parameters are not a benefit if callers lose necessary control.

Generalize only the knowledge or behavior the current use cases actually share. A shared primitive with narrow use-case facades can be better than either duplication or one universal interface. Do not add provider registries, configurable algorithms or frameworks without a concrete need. Scale the response to the decision and avoid repeating the same finding under multiple principle names.

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
