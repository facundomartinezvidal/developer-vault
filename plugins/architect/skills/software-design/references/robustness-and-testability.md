# Robustness and testability

Contracts, failure handling, resource ownership, and what tests say about a design.

## Contents

- [Design by Contract](#design-by-contract)
- [Crash Early (Dead Programs Tell No Lies)](#crash-early-dead-programs-tell-no-lies)
- [Assertive Programming](#assertive-programming)
- [Define Errors Out of Existence](#define-errors-out-of-existence)
- [Finish What You Start (Balancing Resources)](#finish-what-you-start-balancing-resources)
- [Test to Code](#test-to-code)
- [Property-Based Testing](#property-based-testing)

## Design by Contract


**Source:** *The Pragmatic Programmer*, Topic 23 (DBC from Bertrand Meyer, Eiffel). Also Tip 36: "You Can't Write Perfect Software".

### What it means in practice

Every routine has a contract with its callers:

- **Preconditions** say what must be true for the routine to be called. Meeting them is the *caller's* responsibility.
- **Postconditions** say what the routine guarantees when it finishes.
- **Class invariants** must always hold from the caller's point of view.

If the caller meets the preconditions, the routine promises the postconditions and invariants, and it makes no promises otherwise. This leads to Hunt & Thomas's **lazy code**: accept strictly and promise little. The contract also tells you where the bug is. A broken precondition is a bug in the caller, and a broken postcondition is a bug in the routine.

Most languages don't support contracts directly, so they're expressed through assertions, guard clauses, types, documentation, and tests (Property-Based Testing fits them well). When a contract is violated, Crash Early (Dead Programs Tell No Lies) instead of continuing in an unknown state. DBC also helps with concurrency (`concurrency.md`), because an invariant tells you exactly what a lock has to protect.

### Example

```java
/**
 * Pre:  amount > 0 and amount <= balance()
 * Post: balance() == old balance() - amount
 * Inv:  balance() >= 0
 */
public void withdraw(Money amount) {
    require(amount.isPositive(), "amount must be positive");
    require(amount.lte(balance), "insufficient funds");
    Money before = balance;
    balance = balance.minus(amount);
    ensure(balance.equals(before.minus(amount)));
}
```

### Where it applies

- assertions — Evans's supple-design version: state post-conditions and invariants explicitly, and test them.
- Assertive Programming and Crash Early (Dead Programs Tell No Lies) — how contracts are enforced at runtime.
- liskov substitution principle — LSP is a contract rule: a subtype can't strengthen preconditions or weaken postconditions.

### Related

- Test to Code
- Property-Based Testing
- Define Errors Out of Existence — Ousterhout prefers *widening* the contract so that fewer calls are errors.

## Crash Early (Dead Programs Tell No Lies)


**Source:** *The Pragmatic Programmer*, Topic 24.

### What it means in practice

When code finds that something "impossible" has happened, the program is no longer in a state you understand. Continuing can corrupt data, charge the wrong card, or send the wrong email. A program that stops does far less damage than one that keeps running with bad data.

- **Don't catch-and-release.** Wrapping every call in `try { } catch (e) { log(e); }` hides the failure and keeps the program running in an unknown state. Let exceptions propagate unless you can actually handle them.
- **Crash, then restart cleanly.** Erlang's "let it crash" with supervisor trees shows this can be part of a design: a failing process is killed and a supervisor restarts it.
- **Crash *safely*.** Close what has to be closed and leave a useful message, but don't try to keep going.

### Example

```java
// Catch-and-release: the import "succeeds" with half the rows silently skipped
for (Row r : rows) { try { importRow(r); } catch (Exception e) { log.warn("skip", e); } }

// Crash early: stop at the first row we don't understand, inside a transaction that rolls back
@Transactional
public void importAll(List<Row> rows) { rows.forEach(this::importRow); }   // any exception → rollback, job marked failed
```

### Where it applies

- Design by Contract — a violated contract is the textbook reason to crash.
- Assertive Programming — assertions are how you notice the impossible.
- exceptions over error codes — Clean Code's rules for the errors you *can* handle.

### Related

- Define Errors Out of Existence — Ousterhout's "just crash" for errors not worth handling, such as out-of-memory.
- Finish What You Start (Balancing Resources) — crashing safely means releasing resources properly.
- Actors and Processes (`concurrency.md`) — supervision trees in actor systems.

## Assertive Programming


**Source:** *The Pragmatic Programmer*, Topic 25.

### What it means in practice

Every programmer has thought "this can never happen": the month can't be 13, the list can't be empty here, this code path is unreachable. Write those thoughts down as assertions. Then if the impossible happens, you find out right away and close to the cause.

- Assertions check for things that **should never happen**, not for normal error handling. Bad user input isn't impossible: validate it and handle it.
- Assertions **must not have side effects** (`assert queue.poll() != null` changes the queue).
- **Leave assertions on in production.** Hunt & Thomas reject turning them off once the code ships. Production is exactly where the impossible happens: different data, different load, different timing. Turn off only the specific ones that are too expensive.

### Example

```java
public Money refund(Order order, Money amount) {
    // Validation (expected bad input → handled)
    if (amount.gt(order.capturedAmount())) throw new RefundExceedsCaptureException(order.id(), amount);

    Money remaining = order.capturedAmount().minus(order.refundedSoFar());
    // Assertion (internal invariant → "impossible")
    if (remaining.isNegative())
        throw new IllegalStateException("Order " + order.id() + " has refunded more than it captured");
    ...
}
```

### Related

- Design by Contract — assertions are how contracts are checked in most languages.
- Crash Early (Dead Programs Tell No Lies)
- Property-Based Testing

## Define Errors Out of Existence


**Source:** *A Philosophy of Software Design*, Chapter 10.

### What it means in practice

Exceptions are among the worst sources of complexity. Every exception a module throws becomes part of its interface. Handling code is hard to write, rarely runs, and is rarely tested. Programmers also tend to throw more exceptions than needed, to look "defensive", which pushes the problem onto callers. Ousterhout lists four techniques, in order of preference:

1. **Define errors out of existence.** Change the semantics so the case is normal. Tcl's `unset` of a missing variable could just do nothing: the postcondition "variable doesn't exist" already holds. Java's `substring` could clamp out-of-range indices instead of throwing.
2. **Mask exceptions.** Handle them at a low level so higher levels never see them (TCP retransmits lost packets, and the application never knows).
3. **Aggregate exceptions.** Handle many exceptions in one place instead of in many handlers. For example, a web server's top-level handler turns any missing-parameter error into a 400.
4. **Just crash.** For errors that are rare and not worth handling, such as out-of-memory, print a diagnostic and abort.

The same reasoning applies to **special cases**. Design the normal case so it covers them (a "no selection" state represented as an empty selection). **Don't go too far**: if callers *need* to know (a network write failed, a payment was declined), the exception is part of the abstraction and must be exposed.

### Example

```java
// Error-heavy: callers must handle "already cancelled" and "not found"
void cancelSubscription(SubId id) throws SubscriptionNotFoundException, AlreadyCancelledException;

// Defined out of existence: postcondition "subscription is not active" — idempotent
void ensureCancelled(SubId id);   // no-op if already cancelled or never existed
```

### Contrast with the other books

- Martin's exceptions over error codes is about *how* to throw well. Ousterhout asks *whether* to throw at all.
- Martin's dont return null (Special Case objects) is defining errors out of existence for missing values.
- Hunt & Thomas's Crash Early (Dead Programs Tell No Lies) matches technique 4, applied to *impossible* states.

### Related

- Pull Complexity Downwards (`modularity.md`) — masking is pulling exception handling down.
- Design by Contract — widening preconditions so that fewer calls are errors.
- Deep Modules (`modularity.md`) — fewer exceptions mean a simpler interface.
- Software Complexity (`complexity.md`)
- Designing for Performance (`complexity.md`)

## Finish What You Start (Balancing Resources)


**Source:** *The Pragmatic Programmer*, Topic 26 (also Tip 41).

### What it means in practice

Memory, files, sockets, locks, transactions and DB connections all have to be released. The rule: **whoever allocates a resource releases it.** If a resource is opened in one function and closed in another, sooner or later some code path skips the close.

Related habits:
- **Act locally.** Keep the resource's lifetime inside one scope.
- **Deallocate in the reverse order of allocation.** This avoids leaving dangling references.
- **Allocate the same set of resources in the same order everywhere.** This prevents deadlocks.
- Use language features that guarantee release: `try-with-resources`, `using`, `with`, `defer`, RAII.
- Check balance with wrappers or tooling (leak detectors, connection-pool metrics).

### Example

```java
// Unbalanced: the caller must remember to close the connection opened elsewhere
Connection c = pool.openFor(report);
generate(c, report);           // throws → connection leaked
c.close();

// Balanced: the scope that opens also closes, on every path
try (Connection c = pool.getConnection();
     PreparedStatement ps = c.prepareStatement(SQL)) {
    return mapRows(ps.executeQuery());
}
```

### Related

- Crash Early (Dead Programs Tell No Lies) — crashing safely still releases what it holds.
- Shared State Is Incorrect State (`concurrency.md`) — locks are resources too, and acquiring them in a consistent order prevents deadlocks.
- Decoupling (`coupling.md`)

## Test to Code


**Source:** *The Pragmatic Programmer*, Topic 41 (Tips 66–70).

### What it means in practice

Hunt & Thomas say most of the value of testing comes from *thinking about* the test, not from running it. A test is **your code's first caller** (Tip 67). When writing one is painful, because you need a database, a clock, three mocks and a global, the code is telling you it's too coupled (`coupling.md`). So:

- **Design to test** (Tip 69). Think about how you'll test a function before you write it. That pushes you toward clear contracts, injected dependencies, and few side effects.
- **Build thin end-to-end slices, rather than top-down or bottom-up** (Tip 68). Build small vertical slices, learning about the problem as you go (tracer bullets).
- **TDD is a tool, not a religion.** Its strength is the test-first thinking, and its danger is spending ages on tiny unit tests without looking at the big picture.
- **Test your software, or your users will** (Tip 70). Also make the software testable in production: logging, a hot-key debug view, a health endpoint.

### Example

```java
// Painful to test → too coupled
class ReminderJob { void run() { for (Invoice i : Db.instance().overdue(LocalDate.now())) new SmtpClient().send(...); } }

// The test, written first, pulls the dependencies out
class ReminderJob {
    ReminderJob(InvoiceRepository invoices, Clock clock, Notifier notifier) { ... }
    void run() { invoices.overdueAsOf(LocalDate.now(clock)).forEach(notifier::remind); }
}
```

### Where it applies

- Design by Contract — a test checks the contract: preconditions in, postconditions out.
- three laws of tdd — Martin's stricter discipline. Hunt & Thomas prefer the thinking over the ritual.
- test boundary — Martin's argument that testability is an architectural force.

### Related

- Property-Based Testing
- Decoupling (`coupling.md`)

## Property-Based Testing


**Source:** *The Pragmatic Programmer*, Topic 42.

### What it means in practice

When you write the code *and* its example tests, the same wrong assumptions end up in both. Property-based testing removes you from choosing the inputs. You state **properties**, which are invariants and contracts that must hold for *every* valid input. A framework (Hypothesis, jqwik, fast-check) then generates hundreds of random inputs to try to break them. When it finds a failure, it **shrinks** the input to the smallest case that still fails, and that case often becomes a regular regression test.

Good properties include: round-trips (`decode(encode(x)) == x`), invariants (a sorted list has the same elements as before, in order), postconditions from a contract, and agreement with a simpler reference implementation.

### Example

```java
@Property
void splitting_a_bill_never_loses_or_creates_cents(@ForAll @Positive long totalCents,
                                                   @ForAll @IntRange(min = 1, max = 50) int people) {
    List<Money> shares = Bill.of(Money.cents(totalCents)).splitAmong(people);
    assertThat(sum(shares)).isEqualTo(Money.cents(totalCents));                 // conservation
    assertThat(maxMinusMin(shares)).isLessThanOrEqualTo(Money.cents(1));        // fairness
}
```

An example-based test with `100 / 3` might pass. The generator will find the total and head count where rounding drops a cent.

### Related

- Design by Contract — contracts are the natural source of properties.
- Assertive Programming — properties are assertions run against generated inputs.
- Test to Code
