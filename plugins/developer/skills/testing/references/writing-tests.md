# Writing tests

What makes tests useful and readable, three positions on TDD, and generated inputs.

## Contents

- [Clean Tests (F.I.R.S.T.)](#clean-tests-first)
- [Test to Code](#test-to-code)
- [The Three Laws of TDD](#the-three-laws-of-tdd)
- [Property-Based Testing](#property-based-testing)

## Clean Tests (F.I.R.S.T.)


**Source:** *Clean Code*, Chapter 9 (heuristics T1–T9).

### What it means in practice

Dirty tests are worse than no tests. They get harder to change as the production code changes, until the team gives up on them, and then the production code rots too. What keeps tests clean is **readability**:

- **Build-Operate-Check.** Each test sets up data, runs the operation, and checks the result, with no noise in between.
- **A domain-specific testing language.** Helper functions (`givenCustomerWithOverdueInvoice()`, `assertResponseIsXml()`) let a test read like a specification.
- **A dual standard.** Tests must be clear, but they don't have to be efficient. Shortcuts that would be wrong in production, like string concatenation in a loop or huge fixtures, can be fine in a test.
- **One concept per test.** "One assert per test" is a good guideline, but the real rule is to test a single concept.

**F.I.R.S.T.:**
- **Fast**, or people stop running them.
- **Independent**: no test sets up the next one.
- **Repeatable** in any environment, including offline and on a laptop.
- **Self-validating**: they pass or fail, with no reading logs.
- **Timely**: written just before the production code they test.

Chapter 17's T-heuristics add: use a coverage tool, test boundary conditions, test exhaustively near bugs, and treat an ignored test as an open question.

### Example

```java
@Test void overdue_invoice_blocks_new_orders() {
    Customer customer = givenCustomerWithOverdueInvoice(daysOverdue(45));   // build
    OrderResult result = ordering.place(orderFor(customer));                 // operate
    assertThat(result).isRejectedBecause(OVERDUE_BALANCE);                   // check
}
```

### Where it applies

- The Three Laws of TDD — how these tests get written.
- Property-Based Testing — Hunt & Thomas: generate the inputs instead of writing every example by hand.
- Pragmatic Starter Kit (`testable-code.md`) — the build runs every test automatically ("test state coverage, not code coverage", "find bugs once").

### Related

- Test to Code
- The Test Boundary (`testable-code.md`) — Martin: fragile tests are a design problem. Couple tests to a stable API, not to the GUI.
- Humble Object (`testable-code.md`) — splitting off a hard-to-test part is what keeps the rest fast and repeatable.

## Test to Code


**Source:** *The Pragmatic Programmer*, Topic 41 (Tips 66–70).

### What it means in practice

Hunt & Thomas say most of the value of testing comes from *thinking about* the test, not from running it. A test is **your code's first caller** (Tip 67). When writing one is painful, because you need a database, a clock, three mocks and a global, the code is telling you it's too coupled. So:

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

- design by contract — a test checks the contract: preconditions in, postconditions out.
- The Three Laws of TDD — Martin's stricter discipline. Hunt & Thomas prefer the thinking over the ritual.
- The Test Boundary (`testable-code.md`) — Martin's argument that testability is an architectural force.

### Related

- Clean Tests (F.I.R.S.T.)
- Property-Based Testing
- Separate Constructing a System from Using It (`testable-code.md`)
- Pragmatic Starter Kit (`testable-code.md`)
- Humble Object (`testable-code.md`)

## The Three Laws of TDD


**Source:** *Clean Code*, Chapter 9.

### What it means in practice

The three laws are: write no production code without a failing test, write only enough of a test to fail, and write only enough code to pass it. They lock you into a cycle about 30 seconds long: write a little test, write a little code, repeat. Tests come a few seconds before the code they cover. After a day there are dozens of tests, and after a year thousands. Together they cover nearly all the production code. That suite is what makes refactoring safe: without it, every change is a possible bug, so people stop changing things and the code rots.

Martin also says **tests enable the "-ilities"**. Flexibility, maintainability and reusability all depend on being able to change code without fear, and tests give you that.

### Three books, three positions on TDD

- **Martin**: TDD is a professional discipline. Follow the three laws.
- **Hunt & Thomas** (Test to Code): the benefit of TDD is the *thinking* a test forces about the code's interface and coupling. They warn against becoming a "TDD slave" who builds bottom-up without looking at the whole, and they recommend building end-to-end in thin slices (tracer bullets).
- **Ousterhout** (strategic vs tactical programming): TDD is *tactical*. It optimizes for the next passing test instead of good design. Write tests, but write them for larger units after designing the abstraction. Writing a test first when fixing a bug is the exception he endorses.

### Example

```java
@Test void free_shipping_above_threshold() {                           // 1. failing test (doesn't compile yet)
    assertThat(shipping.costFor(cartTotalling(usd(120)))).isEqualTo(usd(0));
}
public Money costFor(Cart cart) { return Money.ZERO; }                   // 2. just enough to pass
@Test void flat_rate_below_threshold() { ... }                          // 3. next test forces the real rule
```

### Related

- Clean Tests (F.I.R.S.T.) — the tests produced this way have to be kept as clean as production code.
- The Test Boundary (`testable-code.md`) — Martin's architecture-level view of tests as a system component.
- Pragmatic Starter Kit (`testable-code.md`)

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

- Clean Tests (F.I.R.S.T.)
- Test to Code
- Pragmatic Starter Kit (`testable-code.md`)
