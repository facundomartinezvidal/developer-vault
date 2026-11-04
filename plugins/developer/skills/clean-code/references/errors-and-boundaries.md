# Errors, contracts and boundaries

Error handling, null, contracts, failing fast, resource ownership, third-party code and basic code-level safety.

## Contents

- [Exceptions over Error Codes](#exceptions-over-error-codes)
- [Don't Return Null (and Don't Pass It)](#dont-return-null-and-dont-pass-it)
- [Define Errors Out of Existence](#define-errors-out-of-existence)
- [Design by Contract](#design-by-contract)
- [Crash Early (Dead Programs Tell No Lies)](#crash-early-dead-programs-tell-no-lies)
- [Assertive Programming](#assertive-programming)
- [Finish What You Start (Balancing Resources)](#finish-what-you-start-balancing-resources)
- [Clean Boundaries](#clean-boundaries)
- [Stay Safe Out There](#stay-safe-out-there)

## Exceptions over Error Codes

> Error handling is important, but if it obscures logic, it's wrong.

**Source:** *Clean Code*, Chapter 7 (Michael Feathers) and Chapter 3.

### What it means in practice

- **Use exceptions, not return codes.** Error codes force every caller to check right away, and the happy path gets buried in `if (result != OK)` branches. Exceptions keep the main logic and the error handling apart.
- **Error handling is one thing.** A function that handles errors should do nothing else. Extract the body of a `try` into its own function, so you have one function with the logic and one with the `try/catch`.
- **Write the try-catch-finally first** when code can throw. It defines what the caller can expect no matter what goes wrong inside, a bit like a transaction.
- **Use unchecked exceptions.** Checked exceptions break the OCP: Open-Closed Principle (`objects-and-classes.md`): a new `throws` deep down forces signature changes in every layer above it.
- **Provide context.** Include the operation and why it failed.
- **Define exception classes by how the caller handles them**, not by where they come from. Wrap a third-party API that throws five exception types into one exception the caller can actually act on.
- **Define the normal flow.** When there's a default behavior, use a **Special Case** object instead of throwing. Then the caller never sees the exception at all (see Don't Return Null (and Don't Pass It)).

### Example

```java
// Wrapping a payment SDK: callers handle one exception, defined by what they do about it
public class PaymentGateway {
    public ChargeId charge(Money amount, CardToken card) {
        try {
            return new ChargeId(stripe.charges().create(params(amount, card)).getId());
        } catch (CardException e) {
            throw new PaymentDeclinedException(card, e.getDeclineCode(), e);
        } catch (RateLimitException | ApiConnectionException e) {
            throw new PaymentUnavailableException("Stripe unreachable charging " + amount, e);
        }
    }
}
```

### Contrast with the other books

- Ousterhout (Define Errors Out of Existence) goes further. Every exception is part of the interface and adds complexity, so the best error handling is designing the API so the error *can't* happen. Masking and aggregating exceptions are also better than throwing them up the stack.
- Hunt & Thomas (Crash Early (Dead Programs Tell No Lies)) add that when something truly impossible happens, stop: a dead program does less damage than one running in a bad state.

### Where it applies

- Clean Boundaries — wrapping third-party exceptions is part of wrapping the third-party API.
- Small Functions That Do One Thing (`names-and-functions.md`) — "error handling is one thing" is the do-one-thing rule applied to `try/catch`.
- anticorruption layer — translating a foreign system's failures into your model's terms.

### Related

- Don't Return Null (and Don't Pass It)
- Design by Contract
- Assertive Programming
- OCP: Open-Closed Principle (`objects-and-classes.md`)
- Finish What You Start (Balancing Resources)

## Don't Return Null (and Don't Pass It)

> When we return null, we are essentially creating work for ourselves and foisting problems upon our callers.

**Source:** *Clean Code*, Chapter 7.

### What it means in practice

Every `null` you return is a check that every caller has to remember. Missing one check means a `NullPointerException` far away from where the null came from. Instead:

- Return an **empty collection** instead of `null` for "no results".
- Return a **Special Case / Null Object**: an object with the same interface that does the sensible default.
- Throw an exception if absence is really an error (Exceptions over Error Codes).
- (In modern Java, `Optional<T>` makes absence explicit in the type, which is the same idea.)

**Don't pass null either.** Most APIs have no good way to handle a `null` argument. The default should be that `null` isn't allowed, so the code doesn't need to defend against it everywhere.

### Example

```java
// Before: every caller must remember the null
Discount d = discounts.forCustomer(customer);
Money total = (d == null) ? subtotal : d.applyTo(subtotal);

// After: a special case object defines the normal flow
interface Discount { Money applyTo(Money amount); }
final class NoDiscount implements Discount { public Money applyTo(Money amount) { return amount; } }

Money total = discounts.forCustomer(customer).applyTo(subtotal);   // never null
```

### Where it applies

- Define Errors Out of Existence — Ousterhout's broader version: change the semantics so the "error" case is just a normal case.
- Introduce Special Case — Fowler's refactoring that introduces exactly this object.
- strategy pattern — `NoDiscount` is a do-nothing strategy.

### Related

- Exceptions over Error Codes
- Design by Contract — "no null arguments" is a precondition, and stating it is better than defending against it everywhere.
- Code Should Be Obvious (`foundations.md`)

## Define Errors Out of Existence

> The best way to eliminate exception handling complexity is to define your APIs so that there are no exceptions to handle.

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

- Martin's Exceptions over Error Codes is about *how* to throw well. Ousterhout asks *whether* to throw at all.
- Martin's Don't Return Null (and Don't Pass It) (Special Case objects) is defining errors out of existence for missing values.
- Hunt & Thomas's Crash Early (Dead Programs Tell No Lies) matches technique 4, applied to *impossible* states.

### Related

- Design by Contract — widening preconditions so that fewer calls are errors.

## Design by Contract

> Design with Contracts. — Tip 37

**Source:** *The Pragmatic Programmer*, Topic 23 (DBC from Bertrand Meyer, Eiffel). Also Tip 36: "You Can't Write Perfect Software".

### What it means in practice

Every routine has a contract with its callers:

- **Preconditions** say what must be true for the routine to be called. Meeting them is the *caller's* responsibility.
- **Postconditions** say what the routine guarantees when it finishes.
- **Class invariants** must always hold from the caller's point of view.

If the caller meets the preconditions, the routine promises the postconditions and invariants, and it makes no promises otherwise. This leads to Hunt & Thomas's **lazy code**: be strict about what you accept, and promise as little as possible in return. The contract also tells you where the bug is. A broken precondition is a bug in the caller, and a broken postcondition is a bug in the routine.

Most languages don't support contracts directly, so they're expressed through assertions, guard clauses, types, documentation, and tests (property based testing fits them well). When a contract is violated, Crash Early (Dead Programs Tell No Lies) instead of continuing in an unknown state. DBC also helps with concurrency (`concurrency.md`), because an invariant tells you exactly what a lock has to protect.

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
- LSP: Liskov Substitution Principle (`objects-and-classes.md`) — LSP is a contract rule: a subtype can't strengthen preconditions or weaken postconditions.

### Related

- Don't Return Null (and Don't Pass It) — "no nulls" is a precondition.
- Exceptions over Error Codes
- Define Errors Out of Existence — Ousterhout prefers *widening* the contract so that fewer calls are errors.
- Comments Should Describe What Isn't Obvious (`comments.md`) — interface comments are where informal contracts live.
- Stay Safe Out There

## Crash Early (Dead Programs Tell No Lies)

> Crash Early. — Tip 38

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
- Exceptions over Error Codes — Clean Code's rules for the errors you *can* handle.

### Related

- Define Errors Out of Existence — Ousterhout's "just crash" for errors not worth handling, such as out-of-memory.
- Finish What You Start (Balancing Resources) — crashing safely means releasing resources properly.
- Actors and Processes (`concurrency.md`) — supervision trees in actor systems.
- Stay Safe Out There

## Assertive Programming

> Use Assertions to Prevent the Impossible. — Tip 39

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
- Exceptions over Error Codes

## Finish What You Start (Balancing Resources)

> Finish What You Start. — Tip 40

**Source:** *The Pragmatic Programmer*, Topic 26 (also Tip 41, "Act Locally").

### What it means in practice

Memory, files, sockets, locks, transactions and DB connections all have to be released. The rule: **the function or object that allocates a resource is responsible for deallocating it.** If a resource is opened in one function and closed in another, sooner or later some code path skips the close.

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
- Exceptions over Error Codes — Clean Code's "write your try-catch-finally first".
- Hidden Temporal Coupling (`names-and-functions.md`) — open/close pairs split across functions are a temporal coupling.

## Clean Boundaries

> Code at the boundaries needs clear separation and tests that define expectations.

**Source:** *Clean Code*, Chapter 8 (James Grenning).

### What it means in practice

Third-party code is written for many users, so it exposes too much. Your code wants just enough. Three habits keep that conflict contained:

1. **Wrap it.** Don't pass `Map`s, SDK clients or vendor types around your codebase. Put them behind a small class of your own that exposes only what your application needs, using your names. Then the vendor's API can change, and you can swap vendors, by editing one file.
2. **Learning tests.** To learn a library, write tests that call it the way you plan to. They cost nothing, because you had to learn the API anyway. They also tell you right away when an upgrade changes behavior.
3. **Code that doesn't exist yet.** When the other side of a boundary isn't built (or isn't defined yet), write the interface *you wish you had*, and code against it. Later, an Adapter connects it to the real thing, and a fake implementation makes testing easy until then.

### Example

```java
// Your interface — the one you wish you had
public interface SmsSender { void send(PhoneNumber to, String message); }

// The only file that knows Twilio exists
public class TwilioSmsSender implements SmsSender {
    public void send(PhoneNumber to, String message) {
        Message.creator(new com.twilio.type.PhoneNumber(to.e164()), fromNumber, message).create();
    }
}

// Learning test, kept in the suite: alerts us if an upgrade changes behavior
@Test void twilio_rejects_numbers_without_country_code() { ... }
```

### Where it applies

- adapter pattern — the mechanism for "code that doesn't exist yet".
- anticorruption layer — Evans's strategic version: a whole translation layer between your model and a foreign one.
- frameworks are details — Martin's architecture version: don't let the framework into your core.

### Related

- Exceptions over Error Codes — wrap the library's exceptions as well.
- DIP: Dependency Inversion Principle (`objects-and-classes.md`) — your code owns the interface, and the vendor code depends on it.

## Stay Safe Out There

> Keep It Simple and Minimize Attack Surfaces. — Tip 72 &nbsp;·&nbsp; Apply Security Patches Quickly. — Tip 73

**Source:** *The Pragmatic Programmer*, Topic 43.

### What it means in practice

Once code works on the happy path, it's tempting to call it done. Hunt & Thomas list the basic security principles that are easy to forget:

1. **Minimize attack surface.** Complexity creates attack vectors. Validate all input, don't trust anything from outside, keep unauthenticated services to a minimum, limit the number of authenticated users, and turn off features and debug output you don't need. Don't leak information in error messages.
2. **Principle of least privilege.** Grant the lowest permission level, for the shortest time, that does the job.
3. **Secure defaults.** The default configuration should be the safe one. Users opt *in* to less safety.
4. **Encrypt sensitive data.** Never commit secrets, API keys or passwords to version control. Use config or a secret store. Don't roll your own crypto.
5. **Keep up with security patches.** Most large breaches exploit known vulnerabilities that were never patched.

Also: use proven password-handling and authentication practices (NIST guidance, long passphrases, MFA) instead of inventing rules.

### Example

A file-upload endpoint: authenticated users only; size and MIME-type limits; filenames generated server-side; stored in a bucket with no public access; the API's IAM role can write only to that one prefix; Dependabot alerts set to auto-merge patch updates.

### Related

- Crash Early (Dead Programs Tell No Lies) — but crash *safely*, without leaking stack traces to users.
- Design by Contract — validate preconditions at the trust boundary.
