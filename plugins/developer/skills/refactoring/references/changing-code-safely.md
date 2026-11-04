# Changing code safely

When and how to refactor, how to leave code better than you found it, and when duplication is not the problem.

## Contents

- [Refactor Early, Refactor Often](#refactor-early-refactor-often)
- [Modifying Existing Code](#modifying-existing-code)
- [The Boy Scout Rule](#the-boy-scout-rule)
- [Broken Windows (Software Entropy)](#broken-windows-software-entropy)
- [Strategic vs. Tactical Programming](#strategic-vs-tactical-programming)
- [ETC — Easier to Change](#etc-easier-to-change)
- [DRY — Don't Repeat Yourself](#dry-dont-repeat-yourself)
- [True vs. Accidental Duplication](#true-vs-accidental-duplication)

## Refactor Early, Refactor Often


**Source:** *The Pragmatic Programmer*, Topic 40.

### What it means in practice

Software is more like **gardening** than construction. Things grow, some die, and plants need to be moved or pruned. Refactoring (Fowler's definition: restructuring code without changing its external behavior) is the routine gardening work, not a special phase.

**When to refactor:** when you find duplication, a non-orthogonal design, outdated knowledge (the requirements moved on), usage patterns that show what actually matters, or performance problems, and *whenever the tests pass* after a change. Refactor early: the longer you wait, the more code depends on the bad structure, and the more expensive the fix.

**How:** don't refactor and add functionality at the same time. Make sure you have good tests first. Take short, deliberate steps (one method, one field), and test after each one.

Management pushes back because they see no new features. The book compares it to surgery: putting off removing a tumor makes the operation more dangerous. Explain the cost of the broken windows in terms of time and risk.

### Example

PR 1: "Extract `TaxCalculator` from `CheckoutService` (no behavior change)". All tests are green and the diff is mechanical. PR 2: "Add Brazilian ICMS tax rule", a small change thanks to PR 1. Reviewers can check each one easily, which they couldn't do with a single combined PR.

### Where it applies

- Refactoring — Fowler's book: the smells that tell you when, and the catalog that tells you how.
- The Boy Scout Rule — Martin's version: always leave the code a bit better.
- successive refinement — refactoring under a full test suite, step by step.

### Related

- Strategic vs. Tactical Programming
- Modifying Existing Code
- Broken Windows (Software Entropy)
- Duplicated Code (`smells-readability-and-size.md`)

## Modifying Existing Code


**Source:** *A Philosophy of Software Design*, Chapter 16.

### What it means in practice

Most development is changing existing code, and that's where design gets worse. The tactical habit is to look for the *smallest change* that makes the new feature work. Each one adds a special case or a dependency, and over time the design decays. Instead:

- **Stay strategic.** After each change, the system should look as if it had been *designed from the start* with that change in mind. If that needs some refactoring, do it. If it truly can't be done now, avoid making things worse, and note the compromise.
- **Keep comments up to date:**
  - **Keep comments near the code** they describe, so edits naturally update them. Avoid big header comments far from the code.
  - **Put comments in the code instead of the commit log.** Future developers read the code, not `git log`. Put the explanation where they'll see it.
  - **Avoid duplicating comments.** Document each decision in one place and refer to it from the others.
  - **Check the diffs** before committing, to catch comments that no longer match.
  - **Higher-level comments are easier to maintain**, because they don't change with every implementation detail.

### Example

Adding a "pause subscription" feature. The tactical version: `if (sub.isPaused()) return;` sprinkled through billing, emails and renewals. The strategic version: introduce a `SubscriptionState` with `ACTIVE`, `PAUSED` and `CANCELLED`, let billing ask `sub.isBillableOn(date)`, and update the class comment to describe the state machine. The diff is larger, but the next feature ("pause until a date") becomes a one-line change.

### Related

- Strategic vs. Tactical Programming
- The Boy Scout Rule — Martin's version: always leave the module a bit cleaner.
- Refactor Early, Refactor Often
- Broken Windows (Software Entropy)
- DRY — Don't Repeat Yourself — duplicated comments go stale like duplicated code.

## The Boy Scout Rule


**Source:** *Clean Code*, Chapter 1.

### What it means in practice

Code rots over time unless someone actively works against it. The rule asks for something small every time you touch a module: check it in a little cleaner than you checked it out. Rename one variable, split one function that's too long, delete one piece of duplication, untangle one `if`. No single change is a project. Added together, they keep the codebase improving instead of decaying.

It works because it's local and continuous. You don't need permission or a refactoring sprint, and the code you clean is the code you're already changing, so it's also the code that most needs to be readable.

### Example

You open `InvoiceService` to add a late-fee rule. Before you leave:

```java
// Found
double c(Invoice i) { double t = 0; for (Line l : i.lines) t += l.p * l.q; return t * 1.21; }

// Left behind: same behavior, new name, magic number named
private static final BigDecimal VAT_RATE = new BigDecimal("1.21");
Money totalWithVat(Invoice invoice) { return invoice.subtotal().times(VAT_RATE); }
```

The late-fee change goes in a separate commit from the cleanup, so each one is easy to review on its own.

### Where it applies

- Broken Windows (Software Entropy) — the same idea from the other side: one unrepaired window invites more, and one cleanup stops the slide.
- Refactor Early, Refactor Often — Hunt & Thomas's version: refactor continuously, in small steps.
- successive refinement — *Clean Code* Chapters 14–16 apply the Boy Scout Rule systematically.

### Related

- Strategic vs. Tactical Programming — Ousterhout's advice to spend a little all the time (10–20%) is the same habit, framed as investment.
- Modifying Existing Code — Ousterhout's advice to leave the design better after every change.
- Mysterious Name (`smells-readability-and-size.md`), Duplicated Code (`smells-readability-and-size.md`), Long Function (`smells-readability-and-size.md`) — the usual things you clean up on the way out.

## Broken Windows (Software Entropy)


**Source:** *The Pragmatic Programmer*, Topic 3.

### What it means in practice

The book borrows from urban research: a building with one broken window that stays broken soon has many, because neglect signals that nobody cares. Code is the same. One hack, one ignored warning or one disabled test makes the next one feel acceptable, and **software entropy** (rot) speeds up. Psychology and culture matter more than any single technical cause.

So fix each broken window (bad design, wrong decision, poor code) as soon as you find it. If there's no time to fix it properly, at least *board it up*: comment it out, show a "not implemented" message, add a TODO with a ticket, substitute dummy data. Leave visible evidence that someone is in control. The other side of the rule: don't break a working, clean system to rush a feature in, the same way firefighters roll a carpet out of the way instead of trampling it.

### Example

The CI pipeline has had three "known flaky" tests marked `@Disabled` for months, so a fourth one gets disabled without discussion. Boarding up looks like this: one ticket per flaky test, each with an owner, and a CI check that fails if `@Disabled` appears without a ticket reference.

### Where it applies

- The Boy Scout Rule — Martin's positive version: leave each module cleaner than you found it.
- Refactor Early, Refactor Often — the tool for fixing windows before they spread.
- software complexity — Ousterhout: complexity is *incremental*, many small dependencies and obscurities piling up.

### Related

- Strategic vs. Tactical Programming
- Duplicated Code (`smells-readability-and-size.md`), Speculative Generality (`smells-structure-and-speculation.md`) — typical windows left broken.
- Modifying Existing Code

## Strategic vs. Tactical Programming


**Source:** *A Philosophy of Software Design*, Chapter 3 (see also Chapter 16, Modifying Existing Code).

### What it means in practice

- **Tactical programming** aims to get a feature or fix working as fast as possible. Each shortcut seems harmless, but complexity is incremental, and a system built this way gets slower to work on every month. The extreme case is the **tactical tornado**: someone who ships features very fast, gets praised for it, and leaves a mess for everyone else.
- **Strategic programming** treats working code as necessary but not sufficient. The main goal is a **great design** that also happens to work. That means continually making **small investments**: thinking about alternatives, writing documentation, fixing design problems as you find them.

**How much to invest?** About **10–20%** of development time. Ousterhout argues it pays for itself within months, and after that the system is faster to work on than one built tactically. Startups aren't exempt. A messy codebase is very hard to clean up later, and good engineers notice it when deciding whether to join.

Chapter 16 applies this to changes in existing code. Don't ask "what's the smallest change that works?". Ask "if I were designing this system now, knowing this requirement, what would it look like?", and move the code a step in that direction.

### Example

The task is to add a second shipping carrier. Tactical: copy `UpsShippingService` into `FedexShippingService` and add `if (carrier == FEDEX)` in four places. Strategic: spend half a day extracting a `Carrier` interface with rate, label and tracking operations, so that the second carrier, and every one after it, plugs in without touching the callers.

### Contrast with the other books

- Martin's The Boy Scout Rule and Hunt & Thomas's Refactor Early, Refactor Often say much the same thing in different words.
- Ousterhout criticizes **TDD** and some **agile** practice for encouraging tactical thinking: the next test, the next feature. Martin's three laws of tdd and Hunt & Thomas's essence of agility see it differently.

### Related

- Broken Windows (Software Entropy)
- Modifying Existing Code
- ETC — Easier to Change

## ETC — Easier to Change


**Source:** *The Pragmatic Programmer*, Topic 8.

### What it means in practice

Hunt & Thomas reduce every design principle to one value: good design is design that fits the people using it, and for code that means it **changes easily**. Every other principle is a special case. Decoupling makes things ETC because a change stays local. SRP does it because a requirement change touches one module. Good naming does it because readable code is easier to change.

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

- DRY — Don't Repeat Yourself, orthogonality, decoupling, reversibility — Hunt & Thomas's own special cases of ETC.
- two values of software — Martin's "architecture" value (keeping software soft) is the same idea at the system level.
- software complexity — Ousterhout defines complexity as whatever makes a system hard to understand *and modify*, which is the opposite of ETC.

### Related

- Strategic vs. Tactical Programming

## DRY — Don't Repeat Yourself


**Source:** *The Pragmatic Programmer*, Topic 9 (Tips 15–16); also *Clean Code* Chapters 3 and 12 and heuristic G5.

### What it means in practice

DRY is about **knowledge and intent, not text**. Two identical-looking lines that express different rules aren't a DRY violation. One rule expressed in two different-looking places *is* one. Hunt & Thomas list where duplication shows up:

- **In code:** copy-paste, but also *representational* duplication (a field that can be derived from others, such as storing `length` next to `start` and `end`).
- **In documentation:** comments that restate the code, which go stale when the code changes.
- **In data:** cached or derived values that can drift. Use an accessor instead (the uniform access principle).
- **Between systems:** an API spec, server code and client code each describing the same contract. Generate one from another.
- **Between developers:** two people building the same utility. Fix this with communication, a project librarian, and reuse that's easy (Tip 16).

Martin's version in Clean Code is more about code: duplication is the worst of the problems, and every `switch` repeated across the code is duplicated knowledge.

### Example

```java
// Not DRY: the rule "orders over $100 ship free" lives in three places
if (order.total().gt(usd(100))) shipping = ZERO;                       // backend
const freeShipping = cart.total > 100;                                  // frontend
// email template: "Free shipping on orders over $100!"

// DRY: one authoritative representation, others derived from it
public static final Money FREE_SHIPPING_THRESHOLD = usd(100);          // exposed via /config to the frontend and templates
```

### The other side

Martin's True vs. Accidental Duplication warns against the opposite mistake: merging two pieces of code that look alike but change for different reasons (different actors). DRY applies to the *same knowledge*. Code that only happens to look the same should stay separate.

### Where it applies

- Duplicated Code (`smells-readability-and-size.md`) — Fowler's smell for the code-level case.
- simple design rules — "no duplication" is Beck's rule 2.
- Repeated Switches (`smells-readability-and-size.md`) — the same type switch in several places is duplicated knowledge.
- externalize configuration — one source for values that change per environment.

### Related

- ETC — Easier to Change
- Shotgun Surgery (`smells-change-and-coupling.md`) — what changing duplicated knowledge feels like.
- Modifying Existing Code

## True vs. Accidental Duplication


**Source:** *Clean Architecture*, Chapter 16.

### What it means in practice

**True duplication** is when every change to one copy must be made to every other copy — that's the Duplicated Code (`smells-readability-and-size.md`) smell, and it should be removed. **Accidental duplication** is when two pieces of code look the same *today* but serve different actors or layers; they'll drift apart, and unifying them couples things that should change independently. Before extracting the shared code, ask "will these always change together, for the same reason?" — if not, leave the duplicate.

Two places this bites architects specifically:

- **Across use cases (vertical):** two screens or two queries look alike, so they get merged — then one use case's change breaks the other.
- **Across layers (horizontal):** a database row has the same fields as what the screen shows, so the row object gets passed straight up to the UI. Writing a separate view model is cheap; skipping it couples the UI to the schema.

### Example: two "identical" order summaries

```java
// Customer-facing order summary and warehouse pick-list happen to show the same fields today
record OrderSummaryView(String orderId, List<String> items, String shipTo) {}   // customer UI
record PickListView(String orderId, List<String> items, String shipTo) {}       // warehouse UI
```

The tempting refactor is one shared `OrderView`. But the customer view will soon add prices, promo badges, and estimated delivery; the pick list will add bin locations and package weight. Different actors (customers vs. warehouse ops), different reasons to change — the duplication is accidental, so keep two types.

### Related

- Duplicated Code (`smells-readability-and-size.md`) — the smell this note qualifies: only *true* duplication is the smell.
- Divergent Change (`smells-change-and-coupling.md`) — what you get after wrongly unifying accidental duplicates.
- DRY — Don't Repeat Yourself
