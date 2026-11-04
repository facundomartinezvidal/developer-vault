# Complexity and strategic design

What complexity is, how to invest against it, and how to change a system without eroding it.

## Contents

- [Software Complexity](#software-complexity)
- [Strategic vs. Tactical Programming](#strategic-vs-tactical-programming)
- [ETC — Easier to Change](#etc-easier-to-change)
- [Modifying Existing Code](#modifying-existing-code)
- [Consistency](#consistency)
- [Don't Outrun Your Headlights](#dont-outrun-your-headlights)
- [Designing for Performance](#designing-for-performance)
- [Refactor Early, Refactor Often](#refactor-early-refactor-often)

## Software Complexity

> Complexity is anything related to the structure of a software system that makes it hard to understand and modify the system.

**Source:** *A Philosophy of Software Design*, Chapter 2.

### What it means in practice

Ousterhout's whole book is about one problem: managing complexity. He defines it by its *effect on developers*, not by size. A big system can be simple to work with, and a small one can be miserable. What counts is complexity in the parts people actually work on, weighted by how much time they spend there.

**Three symptoms:**
1. **Change amplification.** A simple change needs edits in many places (a color hard-coded on every page).
2. **Cognitive load.** How much you need to know to make a change safely. Note that *more lines* can mean *less* load, if each line is simpler.
3. **Unknown unknowns.** You can't tell what code you need to change, or what you need to know to change it. This is the worst symptom.

**Two causes:**
- **Dependencies.** Code that can't be understood or changed on its own. They can't be eliminated, but they can be reduced and made obvious.
- **Obscurity.** Important information isn't obvious: vague names, undocumented units, hidden dependencies, inconsistency.

**Complexity is incremental.** No single dependency or shortcut makes a system complex. Hundreds of small ones do. That's why it has to be fought with a "zero tolerance" attitude (Strategic vs. Tactical Programming).

### Example

```java
// Change amplification + obscurity: "30" means days in one place, minutes in another
if (invoice.ageDays() > 30) remind(invoice);
cache.put(key, value, 30);
sessionStore.expireAfter(30);

// One named, typed source of truth per meaning
static final Duration PAYMENT_REMINDER_AFTER = Duration.ofDays(30);
static final Duration RATE_CACHE_TTL = Duration.ofMinutes(30);
```

### Where it applies

- Deep Modules (`modularity.md`) and Information Hiding (and Leakage) (`modularity.md`) — the main tools against dependencies.
- code should be obvious, comments describe the non obvious, meaningful names, Consistency — the tools against obscurity.
- ETC — Easier to Change — Hunt & Thomas define good design as the opposite of complexity.

### Related

- Orthogonality (`modularity.md`) and Decoupling (`coupling.md`) — reducing dependencies.
- DRY — Don't Repeat Yourself (`modularity.md`)
- Define Errors Out of Existence (`robustness-and-testability.md`)
- Designing for Performance

## Strategic vs. Tactical Programming

> Working code isn't enough. … The most important thing is the long-term structure of the system.

**Source:** *A Philosophy of Software Design*, Chapter 3 (see also Chapter 16, Modifying Existing Code).

### What it means in practice

- **Tactical programming** aims to get a feature or fix working as fast as possible. Each shortcut seems harmless, but complexity is incremental, and a system built this way gets slower to work on every month. The extreme case is the **tactical tornado**: someone who ships features very fast, gets praised for it, and leaves a mess for everyone else.
- **Strategic programming** treats working code as necessary but not sufficient. The main goal is a **great design** that also happens to work. That means continually making **small investments**: thinking about alternatives, writing documentation, fixing design problems as you find them.

**How much to invest?** About **10–20%** of development time. Ousterhout argues it pays for itself within months, and after that the system is faster to work on than one built tactically. Startups aren't exempt. A messy codebase is very hard to clean up later, and good engineers notice it when deciding whether to join.

Chapter 16 applies this to changes in existing code. Don't ask "what's the smallest change that works?". Ask "if I were designing this system now, knowing this requirement, what would it look like?", and move the code a step in that direction.

### Example

The task is to add a second shipping carrier. Tactical: copy `UpsShippingService` into `FedexShippingService` and add `if (carrier == FEDEX)` in four places. Strategic: spend half a day extracting a `Carrier` interface with rate, label and tracking operations, so that the second carrier, and every one after it, plugs in without touching the callers.

### Contrast with the other books

- Martin's boy scout rule and Hunt & Thomas's Refactor Early, Refactor Often say much the same thing in different words.
- Ousterhout criticizes **TDD** and some **agile** practice for encouraging tactical thinking: the next test, the next feature. Martin's three laws of tdd and Hunt & Thomas's essence of agility see it differently.

### Related

- Software Complexity
- Modifying Existing Code
- ETC — Easier to Change

## ETC — Easier to Change

> Good Design Is Easier to Change Than Bad Design. — Tip 14

**Source:** *The Pragmatic Programmer*, Topic 8.

### What it means in practice

Hunt & Thomas reduce every design principle to one value: a thing is well designed if it adapts to the people who use it, and for code that means it **changes easily**. Every other principle is a special case. Decoupling makes things ETC because a change stays local. SRP does it because a requirement change touches one module. Good naming does it because readable code is easier to change.

ETC is a *value*, not a rule, so you use it as a question while you work: "Did what I just did make the system easier or harder to change?" When you can't tell what kind of change is coming:
1. Fall back on keeping the code *replaceable*: decoupled and cohesive.
2. Write down the situation in your engineering daybook and look back later to calibrate your instincts.

### Example

Before you merge, ask ETC of the change:

```java
// Harder to change: the tax rule is spread across controller, service and email template
// Easier to change: one place knows how VAT is computed
public final class VatPolicy {
    public Money vatFor(Money net, Country country) { return net.times(rateFor(country)); }
}
```

### Where it applies

- DRY — Don't Repeat Yourself (`modularity.md`), Orthogonality (`modularity.md`), Decoupling (`coupling.md`), reversibility — Hunt & Thomas's own special cases of ETC.
- two values of software — Martin's "architecture" value (keeping software soft) is the same idea at the system level.
- Software Complexity — Ousterhout defines complexity as whatever makes a system hard to understand *and modify*, which is the opposite of ETC.

### Related

- Strategic vs. Tactical Programming
- Encapsulate What Varies (`coupling.md`)

## Modifying Existing Code

> If you want to maintain a clean design for a system, you must take a strategic approach when modifying existing code.

**Source:** *A Philosophy of Software Design*, Chapter 16.

### What it means in practice

Most development is changing existing code, and that's where design gets worse. The tactical habit is to look for the *smallest change* that makes the new feature work. Each one adds a special case or a dependency, and over time the design decays. Instead:

- **Stay strategic.** After each change, the system should look as if it had been *designed from the start* with that change in mind. If that needs some refactoring, do it. If it truly can't be done now, avoid making things worse, and note the compromise.
- **Keep comments up to date:**
  - **Keep comments near the code** they describe, so edits naturally update them. Avoid big header comments far from the code.
  - **Comments belong in the code, not the commit log.** Future developers read the code, not `git log`. Put the explanation where they'll see it.
  - **Avoid duplicating comments.** Document each decision in one place and refer to it from the others.
  - **Check the diffs** before committing, to catch comments that no longer match.
  - **Higher-level comments are easier to maintain**, because they don't change with every implementation detail.

### Example

Adding a "pause subscription" feature. The tactical version: `if (sub.isPaused()) return;` sprinkled through billing, emails and renewals. The strategic version: introduce a `SubscriptionState` with `ACTIVE`, `PAUSED` and `CANCELLED`, let billing ask `sub.isBillableOn(date)`, and update the class comment to describe the state machine. The diff is larger, but the next feature ("pause until a date") becomes a one-line change.

### Related

- Strategic vs. Tactical Programming
- Refactor Early, Refactor Often
- DRY — Don't Repeat Yourself (`modularity.md`) — duplicated comments go stale like duplicated code.

## Consistency

> Consistency is a powerful tool for reducing the complexity of a system and making its behavior more obvious.

**Source:** *A Philosophy of Software Design*, Chapter 17.

### What it means in practice

When similar things are done in similar ways, a reader who has learned one example understands the rest. That reduces cognitive load, and they can make safe assumptions about code they haven't read. Consistency applies to:

- **Names**: one name per concept, never reused for something else (meaningful names).
- **Coding style**: formatting and conventions.
- **Interfaces**: different implementations of an interface behave alike.
- **Design patterns**: solve the same kind of problem the same way everywhere.
- **Invariants**: properties that always hold, such as "every line in this buffer ends with a newline".

How to keep it:
- **Document** the conventions somewhere people will actually find them.
- **Enforce** them automatically: linters, formatters, pre-commit hooks.
- **When in Rome, do as the Romans do.** Follow the existing conventions of the code you're editing.
- **Don't change existing conventions** just because you have a slightly better idea. Inconsistency costs more than a slightly worse convention, unless the new approach is *much* better and you'll update all the old code.

**Taking it too far:** don't force dissimilar things into the same shape just to make them consistent.

### Example

Every HTTP handler in a service returns errors as `{ "error": { "code": "...", "message": "..." } }` with the matching status code. A new endpoint that returns `{ "msg": "bad input" }` with a 200 breaks every client's error handling, even if it's "simpler".

### Related

- DRY — Don't Repeat Yourself (`modularity.md`) — one representation per piece of knowledge.
- Software Complexity — inconsistency causes obscurity.

## Don't Outrun Your Headlights

> Take Small Steps—Always. — Tip 42

**Source:** *The Pragmatic Programmer*, Topic 27 (also Tip 43, "Avoid Fortune-Telling").

### What it means in practice

A driver at night shouldn't go faster than they can stop within the distance the headlights reach. In software, the headlights are how far ahead you can see with confidence, and that's usually not very far. So:

- **Take small, deliberate steps.** After each one, check feedback (a test, a REPL, a demo to a user) before taking the next.
- **Feedback comes in many forms:** unit tests, user demos, real-world results. The goal is to *learn* before you commit more.
- **Avoid fortune-telling.** Don't design for a future you can't see ("we'll need multi-currency someday"). Make the code replaceable instead, so the future is cheap to handle whenever it actually arrives.
- **Black swans happen.** The tech you bet on may vanish, and the one you dismissed may take over. That's one more reason to keep things reversible.

### Example

Instead of building a "plugin system for future payment providers":

```java
// Today: one provider, behind an interface you own (cheap, replaceable)
interface PaymentGateway { ChargeId charge(Money amount, CardToken card); }
class StripeGateway implements PaymentGateway { ... }
// When a second provider is a real requirement, add it — the interface already makes that cheap.
```

### Related

- Refactor Early, Refactor Often
- General-Purpose Modules Are Deeper (`modularity.md`) — Ousterhout's "somewhat general-purpose" is the middle path between overbuilding and fortune-telling.

## Designing for Performance

> Clean design and high performance are compatible.

**Source:** *A Philosophy of Software Design*, Chapter 20.

### What it means in practice

Ousterhout's position is between "optimize everything" (which adds complexity everywhere) and "never think about performance" (which leaves you with many small slowdowns that no single fix solves):

1. **Know what's naturally expensive.** Network round-trips, disk and flash I/O, dynamic memory allocation, and cache misses. Use micro-benchmarks to learn the costs. Then, when two designs are *equally clean*, choose the one that's naturally faster.
2. **Measure before modifying.** Intuitions about where time goes are often wrong. Measure the system to get a baseline and find the real bottleneck.
3. **Design around the critical path.** For code that really matters, ask what the *minimum* work for the common case is. Design the cleanest code that does only that, and handle special cases off the fast path, ideally with a single test that routes all of them away.

Simpler code tends to be faster, because it does less unnecessary work.

### Example

An API for listing a customer's orders makes N+1 queries (one for the orders, then one per order for its items), and it's slow. After measuring, the critical path is "fetch orders with their items for one customer". The redesign is one query with a join, mapped in one pass. The rare case "include archived orders" takes a separate, slower path behind a single flag check.

### Related

- Deep Modules (`modularity.md`) — a deep module can optimize internally without changing its interface.
- Define Errors Out of Existence (`robustness-and-testability.md`) — fewer special cases on the critical path.
- Software Complexity

## Refactor Early, Refactor Often

> Refactor Early, Refactor Often. — Tip 65

**Source:** *The Pragmatic Programmer*, Topic 40.

### What it means in practice

Software is more like **gardening** than construction. Things grow, some die, and plants need to be moved or pruned. Refactoring (Fowler's definition: restructuring code without changing its external behavior) is the routine gardening work, not a special phase.

**When to refactor:** when you find duplication, a non-orthogonal (`modularity.md`) design, outdated knowledge (the requirements moved on), usage patterns that show what actually matters, or performance problems, and *whenever the tests pass* after a change. Refactor early: the longer you wait, the more code depends on the bad structure, and the more expensive the fix.

**How:** don't refactor and add functionality at the same time. Make sure you have good tests first. Take short, deliberate steps (one method, one field), and test after each one.

Management pushes back because they see no new features. The book compares it to surgery: putting off removing a tumor makes the operation more dangerous. Explain the cost of the broken windows in terms of time and risk.

### Example

PR 1: "Extract `TaxCalculator` from `CheckoutService` (no behavior change)". All tests are green and the diff is mechanical. PR 2: "Add Brazilian ICMS tax rule", a small change thanks to PR 1. Reviewers can check each one easily, which they couldn't do with a single combined PR.

### Where it applies

- Refactoring — Fowler's book: the smells that tell you when, and the catalog that tells you how.
- boy scout rule — Martin's version: always leave the code a bit better.
- successive refinement — refactoring under a full test suite, step by step.

### Related

- Don't Outrun Your Headlights
- Strategic vs. Tactical Programming
- Modifying Existing Code
