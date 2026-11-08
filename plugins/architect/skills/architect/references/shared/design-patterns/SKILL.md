---
name: design-patterns
description: "Chooses, applies and removes design patterns and GRASP responsibilities, in any language. Use when growing conditionals, object creation or notifications might need a pattern, to judge if one is overkill, or to explain one (\"qué patrón uso\", \"quién debería hacer esto\")."
---

# Design Patterns

This skill carries a personal study of the classic patterns as reference files. Use it to **choose**, **apply**, **explain** or **remove** a pattern. Its point of view: a pattern is a known solution to a recurring problem in a context, with a cost. Start from the change that hurts, not from the catalog.

## Choosing

1. **Name the concrete problem.** What varies? What change is expensive today, and is it actually happening? Read the current code and its callers.
2. **Compare with the simplest option.** A function, a lookup table, a first-class function or a language feature is often enough. Many patterns collapse in languages with closures, modules, algebraic data types or decorators. Say so when that's the case.
3. **Compare the candidates.** Patterns with the same structure can differ in intent: Strategy and State, Decorator and Proxy, Adapter and Facade. Decide by what the code is trying to do, using the table below.
4. **State the cost.** Extra types, indirection and harder navigation. Say what would make it worth it, and what would mean you should leave it out for now.

Prioritize applicable project requirements, including academic goals. When deciding to apply or discard a concrete relevant pattern, present the recommendation, alternative and costs to the user before implementation unless that choice is already approved. A request for analysis alone needs no approval to compare options. Do not force a pattern without a real variation.

Refactor toward a pattern when the need has appeared, rather than building for it up front. If an existing pattern is unused flexibility, such as a factory with one product or a strategy with one implementation, recommending its removal is a valid answer.

## Problem to pattern

| The problem | Look at | Reference |
|---|---|---|
| An algorithm or rule varies and is picked at runtime | Strategy | `references/behavioral.md` |
| Behavior depends on state, with growing conditionals | State | `references/behavioral.md` |
| Others must react to a change without being known | Observer | `references/behavioral.md` |
| Actions must be queued, logged or undone | Command, Memento | `references/behavioral.md` |
| Same steps, some differ | Template Method (or Strategy) | `references/behavioral.md` |
| A request passes through handlers that may act on it | Chain of Responsibility | `references/behavioral.md` |
| Peers talk to each other in a tangle | Mediator | `references/behavioral.md` |
| Add operations over a stable set of types | Visitor | `references/behavioral.md` |
| Traverse without exposing internals; evaluate a small grammar | Iterator; Interpreter | `references/behavioral.md` |
| Add behavior around an object, in combinations | Decorator | `references/structural.md` |
| Control access to an object: lazy, remote, permissions | Proxy | `references/structural.md` |
| Fit an interface you don't control | Adapter | `references/structural.md` |
| Simplify a complicated subsystem | Facade | `references/structural.md` |
| Treat parts and wholes the same way | Composite | `references/structural.md` |
| Two dimensions vary independently | Bridge | `references/structural.md` |
| Very many similar objects cost too much memory | Flyweight | `references/structural.md` |
| Callers shouldn't choose concrete classes | Factory Method, Abstract Factory | `references/creational.md` |
| Construction has many optional steps | Builder | `references/creational.md` |
| Copying is easier than building | Prototype | `references/creational.md` |
| Exactly one instance | Singleton, usually better as one instance passed in | `references/creational.md` |
| Separating UI, input and state | MVC | `references/compound.md` |
| Which object should own this? | GRASP | `references/beyond-gof.md` |
| Wrap an external system; repeated null checks | Gateway; Null Object | `references/beyond-gof.md` |

Read `references/principles.md` for what patterns are, how they go bad (Golden Hammer and others), and the principles behind them: encapsulate what varies, composition over inheritance, program to an interface, loose coupling. Read `references/beyond-gof.md` for GRASP (who should own a responsibility), other everyday patterns, the simpler equivalents in modern languages, and common anti-patterns.

## Output

**Choosing:** the recommendation, tied to what varies here, and a short sketch of the code using the project's names. Include the rejected alternatives, what it costs, and when not to use it.

**Applying:** make the change in small steps, keeping behavior, and verify. Use names from the domain; `PriceCalculationStrategy` tells less than `SeasonalDiscount`. Use the project's language idioms instead of translating Java.

**Explaining:** intent, a realistic example, when it fits, and its nearest confusions.

**Review:** say whether the pattern earns its cost in this code, with `file:line`.
