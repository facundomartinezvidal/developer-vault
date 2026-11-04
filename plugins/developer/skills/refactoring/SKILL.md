---
name: refactoring
description: "Improves existing code in any language without changing its behavior, using Fowler's Refactoring (code smells and the catalog of moves) plus Clean Code, The Pragmatic Programmer and A Philosophy of Software Design. Use whenever code resists a change, someone wants to clean up before adding a feature, asks what smells code has or whether a refactor is worth it, or must make a large change in small safe steps, even if they just say \"esto se puede mejorar\". Covers Extract Function, Move Function, Replace Conditional with Polymorphism and \"refactorizá esto\", \"qué code smells tiene\", \"está duplicado\" and \"vale la pena refactorizar\". For restructuring layers or modules use the architect agent. Not for style preferences with no change cost."
---

# Refactoring

This skill carries a personal study of code smells and safe change as reference files. Use it to **refactor** code, **diagnose** smells or **decide** whether a cleanup is worth it. Its point of view: refactoring is a change to structure that keeps behavior, and it earns its cost by making a real change cheaper.

## Decide first

Refactor when the code is in the way of a change you are about to make (preparatory), when you had to work out what it does (comprehension), when you see the same thing a third time, or when it was asked for. Leave code alone when it is stable, nobody needs to change it, and it would only look nicer. Replace it instead when the behavior itself is wrong or the structure can't reach the goal in small steps; say so rather than calling a rewrite a refactor.

A smell is a clue, not a verdict. Feature Envy can be a deliberate Strategy, and similar code can be accidental duplication that will diverge. Before merging look-alike code, ask whether it changes for the same reason. Name the concrete change the smell makes harder.

## How to change safely

1. **Pin the current behavior.** Run the existing tests. If coverage of this code is missing, add characterization tests that capture what it does now, including the odd parts and the failure paths (`testing` explains how). If that isn't practical, say so and take smaller, tool-driven steps.
2. **Find what is actually observable.** Public signatures, returned values, errors, side effects, ordering, logs other systems read, and performance that callers rely on all count as behavior.
3. **Take the smallest step.** One move at a time: rename, extract, inline, move, change a declaration. Prefer the IDE's or language server's automated refactoring when available.
4. **Run the tests after each step.** On red, undo the step instead of debugging forward.
5. **Wear one hat at a time.** Refactoring and adding behavior are separate activities, even if you alternate every few minutes. If you find a bug, report it and fix it in its own step. Make the change easy, then make the easy change. Separate commits are worthwhile when they make review easier.
6. **Stop.** End when the goal is met. Don't chase everything you noticed; list it instead.

Public or widely used APIs need a migration path: add the new form, move the callers, then remove the old form. Do not change them unless the scope includes it.

## Smell to first move

These are starting points; the reference files explain each smell and when it's fine.

| You see | Try first |
|---|---|
| Name needs a comment | Rename |
| Long function | Extract Function, Split Phase |
| Same logic twice, same reason to change | Extract Function, then Pull Up if in a hierarchy |
| Many params traveling together | Introduce Parameter Object, Preserve Whole Object |
| One class changes for many reasons | Extract Class, Split Phase |
| One change touches many classes | Move Function or Field to one owner |
| Function uses another object's data | Move Function |
| Same switch repeated | Replace Conditional with Polymorphism, or a lookup table |
| Primitive carrying rules | Replace Primitive with Object |
| Chain of calls through objects | Hide Delegate, or move the logic |
| Class only delegates | Remove Middle Man, Inline |
| Unused flexibility | Inline, Collapse Hierarchy, Remove Dead Code |
| Shared mutable state | Encapsulate, narrow the scope, prefer returning new values |

Before applying a move you're unsure of, read its steps in the matching `moves-` reference. In languages without classes or inheritance, apply the idea with the language's own constructs.

## Output

**Diagnosis:** findings most costly first, with `file:line`, the smell, the change it makes harder, and the first move. Include what you'd leave alone.

**Refactor:** make the change in steps, then report what moved and why, what confirms behavior is unchanged (commands actually run), and anything you noticed but didn't touch. If tests were missing, say what risk remains.

## Reference files

| File | Read when the topic is… |
|---|---|
| `references/principles.md` | what counts as refactoring, the two hats, when and when not, large changes in small steps, published interfaces, performance |
| `references/moves-functions-and-variables.md` | steps for extract and inline, rename, change declaration, split phase, split loop, pipelines, dead code |
| `references/moves-structure-and-data.md` | steps for parameter objects, encapsulation, primitives to objects, extract class, move function or field, delegates, values and references |
| `references/moves-conditionals-and-apis.md` | steps for guard clauses, polymorphism, special cases, assertions, query and modifier, flags and parameters, commands |
| `references/moves-inheritance.md` | steps for pulling up and pushing down, subclasses and superclasses, replacing inheritance with delegation |
| `references/changing-code-safely.md` | when to refactor, modifying existing code, boy scout rule, broken windows, tactical vs. strategic, DRY vs. accidental duplication |
| `references/smells-readability-and-size.md` | names, duplication, long functions and parameter lists, large classes, data clumps, primitive obsession, switches, loops, temporary fields, comments |
| `references/smells-change-and-coupling.md` | divergent change, shotgun surgery, feature envy, insider trading, message chains, middle man, global and mutable data |
| `references/smells-structure-and-speculation.md` | lazy elements, speculative generality, data classes, refused bequest, alternative classes |
