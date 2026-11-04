# Refactoring principles

Hand-written summary, in our own words, of *Refactoring* (2nd ed.), Chapters 2 and 5, with additions marked as general practice. Not generated from the vault.

## What counts as refactoring

A refactoring is a small change to internal structure that makes code easier to understand and cheaper to modify, without changing observable behavior. Refactoring (the activity) strings many of these together. The code keeps working between steps, so you can stop at any point. If code stays broken for days, that was a restructuring, not a refactoring.

Observable behavior means what users and callers care about. Call stacks and timing can shift slightly. A bug you notice normally stays in place until a separate step fixes it, unless nobody has observed it yet and the fix is safe.

Performance optimization also keeps functionality, but its goal is speed, and it may make code harder to change. Keep the two goals apart.

## The two hats

At any moment you are either adding functionality or refactoring. Adding: new tests and new behavior, and existing code stays as is where possible. Refactoring: no new behavior, and tests change only to follow an interface change. Swap often, and always know which hat you are wearing.

## When to refactor

- **Preparatory:** just before a feature or fix, when another structure would make it easier. Make the change easy, then make the easy change.
- **Comprehension:** when you had to work out what code does, move that understanding into the code through names and structure. Early small cleanups often reveal larger design issues.
- **Litter pickup:** when you see a problem nearby. Fix it if quick; otherwise note it and finish your task first.
- **Rule of three:** tolerate a second similar copy; refactor at the third. Duplication that will change for different reasons should stay separate.
- **In a review:** applying a suggestion can reveal further options, and works best with the author present.
- **Planned:** only after neglect or for a problem that outgrew small fixes. Most refactoring should be part of ordinary work.

## When not to

- The code is ugly, but works, and you don't need to understand or change it.
- Rewriting is cheaper. This is a judgment call; a short trial of refactoring usually reveals the difficulty.
- The feature is tiny and the refactor large. Add the feature and leave it, unless you keep coming back.

Justify refactoring economically: it makes features and fixes faster. "Clean" alone is not a reason.

## Large changes in small steps

- **Gradual migration:** whenever someone touches code in the affected area, move it a little toward the target. Everything keeps working throughout.
- **Branch by abstraction:** to replace a library or subsystem, introduce an interface over the old one, move callers to it, build the new implementation behind it, switch, and remove the old one.
- **Parallel change (expand and contract):** add the new form beside the old one, migrate callers, then remove the old form. Use this for shared APIs and schemas.

## Published interfaces

Internal callers can be changed along with a declaration. A published interface has callers you cannot change or even see. Keep the old signature as a thin delegate to the new one, mark it deprecated, and retire it only when it is safe. Removing it may never be possible. This is why it pays to publish less.

## Branches and integration

Long-lived branches make refactoring costly, since renames and moves conflict with everything else. Integrate often. Consider whether separating refactoring and feature commits makes review easier. Fowler isn't convinced that it's always worthwhile, because refactorings can lose their context; follow the team's practice.

## Tests and tools

Refactoring relies on self-testing code: a fast suite that you can run after each step. Prefer the automated refactorings in an IDE or language server, since they understand the syntax and scopes. Text search-and-replace can miss dynamic calls, reflection, string references, templates, configuration and serialized names, so search for those explicitly. Dynamic languages and macro systems give weaker guarantees, so run more tests more often.

Without tests, see `testing`'s reference on legacy code: use mechanical tool-driven changes, and add characterization tests first.

## Performance

Don't avoid refactoring because of speculative performance costs. Most programs spend most of their time in a small part of the code. Well-structured code is easier to tune, so build it clean, then profile and optimize the hot spots. Where performance is a stated requirement, measure before and after.

## Databases

Schema changes can be refactored too: small migrations, each with its data conversion and rollback plan, using expand and contract for anything in production. See `relational-databases`.
