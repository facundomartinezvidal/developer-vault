# Comments

Where the sources disagree most: when a comment is a failure and when it carries what code cannot say.

## Contents

- [Good and Bad Comments (Clean Code's view)](#good-and-bad-comments-clean-codes-view)
- [Comments Should Describe What Isn't Obvious](#comments-should-describe-what-isnt-obvious)
- [Write the Comments First](#write-the-comments-first)

## Good and Bad Comments (Clean Code's view)

> The proper use of comments is to compensate for our failure to express ourself in code.

**Source:** *Clean Code*, Chapter 4 (heuristics C1–C5).

### What it means in practice

Martin treats every comment as a small failure. Comments aren't kept in sync with the code, so over time they become misleading. When you feel the urge to comment, first try to say it in code: extract a well-named function or variable instead.

**Comments worth keeping:** legal headers; informative ones (a regex's expected format); **explanation of intent** (why this choice); clarifying an unreadable library call; **warnings of consequences** ("not thread-safe", "takes 10 minutes"); `TODO`s; amplifying something that looks trivial but matters; Javadoc on *public* APIs.

**Comments to delete:** mumbling; **redundant** comments that restate the code; misleading ones; mandated Javadoc on every getter; journal/changelog comments (version control has that); noise ("default constructor"); position markers and closing-brace comments; attributions; **commented-out code** (just delete it, Git remembers); nonlocal information; too much history.

### Example

```java
// Bad: restates the code, and goes stale the moment the rule changes
// check if the employee is eligible for full benefits
if ((employee.flags & HOURLY_FLAG) != 0 && employee.age > 65) { ... }

// Better: the code says it
if (employee.isEligibleForFullBenefits()) { ... }

// Good comment: explains a constraint the code can't express
// Stripe rejects idempotency keys longer than 255 chars; we hash to stay under the limit.
String key = sha256(orderId + ":" + attempt);
```

### Contrast with Ousterhout

A Philosophy of Software Design disagrees on purpose. Ousterhout calls "good code is self-documenting" a *myth*. Code can't express an interface's abstraction, the reasons behind a design decision, or the meaning of units and boundaries. His rule is comments should describe what isn't obvious from the code, plus Write the Comments First. The two books agree that comments shouldn't repeat the code. They disagree on whether the *ideal* is to have no comments at all.

### Where it applies

- Comments (as a smell) — Fowler's "deodorant" comment is Martin's redundant comment.
- Meaningful Names (`names-and-functions.md`) — a good name is usually the replacement for a bad comment.
- Small Functions That Do One Thing (`names-and-functions.md`) — the extracted function's name *is* the comment.

### Related

- Comments Should Describe What Isn't Obvious
- Write the Comments First

## Comments Should Describe What Isn't Obvious

> Comments should describe things that aren't obvious from the code.

**Source:** *A Philosophy of Software Design*, Chapters 12–13.

### What it means in practice

Ousterhout argues that comments are essential to abstraction. The code shows *how*. Only comments can capture the *what* and *why* the designer had in mind. He answers the **four excuses** for not writing them:

1. *"Good code is self-documenting."* It's a myth. Signatures can't express units, side effects, preconditions or design rationale. Without comments, users of an abstraction have to read its implementation, and then it isn't an abstraction anymore.
2. *"I don't have time."* Writing comments takes a small fraction of development time, and the benefit is large.
3. *"Comments get out of date."* Keep them close to the code, and check them when reviewing diffs.
4. *"All the comments I've seen are worthless."* Then write better ones.

**What makes a comment useful:**
- **Don't repeat the code.** If someone could write the comment just by reading the next line, it adds nothing.
- **Lower-level comments add precision**: units, boundaries (inclusive or exclusive?), what `null` means, invariants.
- **Higher-level comments add intuition**: what a block of code is trying to do, and why.
- **Interface comments** (on classes and methods) describe the abstraction: behavior, arguments, return value, side effects, exceptions, preconditions. *No implementation details.* If an interface comment is hard to write, the design is probably too complicated.
- **Implementation comments** describe *what* and *why*, never *how*.
- **Cross-module design decisions** go where people will find them, such as a central design-notes file.

### Example

```java
/**
 * Reserves stock for every line of the order, all-or-nothing.
 *
 * @return a reservation that holds the items for 15 minutes; call
 *         {@link Reservation#confirm()} after payment or it expires on its own.
 * @throws InsufficientStockException if any line can't be fully reserved —
 *         in that case nothing is reserved.
 */
Reservation reserve(Order order);
```

None of that is visible from the signature `Reservation reserve(Order order)`.

### Contrast with Clean Code

Martin's Good and Bad Comments (Clean Code's view) treats every comment as a failure to express yourself in code. Ousterhout treats comments as part of the design. Both agree that **comments that repeat the code are bad**, and that good names reduce the need for comments. Where they differ: Martin removes comments by improving the code. Ousterhout adds comments that capture what code can't express. The interface comment above is the kind Ousterhout insists on and Martin accepts only for public APIs.

### Related

- Write the Comments First
- Meaningful Names (`names-and-functions.md`)
- Design by Contract (`errors-and-boundaries.md`) — interface comments are where informal contracts live.
- Code Should Be Obvious (`foundations.md`)

## Write the Comments First

> Use comments as part of the design process.

**Source:** *A Philosophy of Software Design*, Chapter 15.

### What it means in practice

Most developers write comments last, if at all, and by then they're rushed and the design is fixed. Ousterhout's approach: for a new class, write the **class interface comment** first. Then write the **interface comments and signatures** of its important methods, with empty bodies. Then iterate on those comments until the structure feels right. Implementation comes after.

Why it works:
- **Better comments.** The abstraction is fresh in your mind, before implementation details crowd it out.
- **Better design.** Comments are a design tool, a "canary in the coal mine". If a method's comment is long and complicated, its interface is too. If a variable's comment is hard to write, the variable probably isn't well defined.
- **Writing comments is more enjoyable** when it's part of designing than when it's a chore at the end.
- **It doesn't cost more**, because the time is spent anyway, just earlier.

### Example

```java
/**
 * Applies a customer's store credit to an invoice. Credit is consumed
 * oldest-first; any credit that would make the balance negative is left untouched.
 */
public class CreditApplier {
    /** Applies as much available credit as possible. @return the amount actually applied (≥ 0). */
    public Money apply(Customer customer, Invoice invoice) { throw new UnsupportedOperationException(); }
}
// Writing "oldest-first" exposed a missing concept: credits need an issue date → add it before coding.
```

### Related

- Comments Should Describe What Isn't Obvious — what those comments should say.
- Good and Bad Comments (Clean Code's view) — Martin's opposite default.
