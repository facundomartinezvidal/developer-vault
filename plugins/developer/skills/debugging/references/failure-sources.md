# Where failures come from

Making failures visible close to their cause, and the recurring sources of intermittent bugs.

## Contents

- [Crash Early (Dead Programs Tell No Lies)](#crash-early-dead-programs-tell-no-lies)
- [Assertive Programming](#assertive-programming)
- [Design by Contract](#design-by-contract)
- [Finish What You Start (Balancing Resources)](#finish-what-you-start-balancing-resources)
- [Mutable Data](#mutable-data)
- [Shared State Is Incorrect State](#shared-state-is-incorrect-state)
- [Concurrency Defense Principles](#concurrency-defense-principles)

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
- exceptions over error codes — Clean Code's rules for the errors you *can* handle.

### Related

- Finish What You Start (Balancing Resources) — crashing safely means releasing resources properly.
- Debugging (`method.md`) — a crash with a clear message is the easiest bug to find.

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
- Programming by Coincidence (`method.md`) — an assertion turns an assumption into something you can check.
- Debugging (`method.md`)

## Design by Contract

> Design with Contracts. — Tip 37

**Source:** *The Pragmatic Programmer*, Topic 23 (DBC from Bertrand Meyer, Eiffel). Also Tip 36: "You Can't Write Perfect Software".

### What it means in practice

Every routine has a contract with its callers:

- **Preconditions** say what must be true for the routine to be called. Meeting them is the *caller's* responsibility.
- **Postconditions** say what the routine guarantees when it finishes.
- **Class invariants** must always hold from the caller's point of view.

If the caller meets the preconditions, the routine promises the postconditions and invariants, and it makes no promises otherwise. This leads to Hunt & Thomas's **lazy code**: be strict about what you accept, and promise as little as possible in return. The contract also tells you where the bug is. A broken precondition is a bug in the caller, and a broken postcondition is a bug in the routine.

Most languages don't support contracts directly, so they're expressed through assertions, guard clauses, types, documentation, and tests (property based testing fits them well). When a contract is violated, Crash Early (Dead Programs Tell No Lies) instead of continuing in an unknown state. DBC also helps with concurrency, because an invariant tells you exactly what a lock has to protect.

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

- Programming by Coincidence (`method.md`)

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
- Shared State Is Incorrect State — locks are resources too, and acquiring them in a consistent order prevents deadlocks.

## Mutable Data

**Source:** *Refactoring*, Chapter 3.

### What it looks like

Data that gets updated in place, where one part of the system changes it without realizing another part expected it to stay the same — a failure "that's particularly hard to spot if it only happens under rare conditions." This is the whole reason functional programming treats variables as never varying: an update always returns a new copy instead of mutating in place. Most of us still work in languages that allow mutation, but the same risk-reduction ideas apply at a smaller scale: narrow the surface that's allowed to update a value, and separate the code that reads/computes from the code that actually performs the update.

### Example

```java
// Mutable: total gets updated from five different call sites across the codebase
order.total = order.total + item.getPrice();
```

```java
// Computed on demand: nothing to update, nothing to get out of sync
double total() {
    return items.stream().mapToDouble(Item::getPrice).sum();
}
```

### Fixes it

- Encapsulate Variable — force updates through a narrow, monitorable function.
- Split Variable — if one variable is being reused to store different things.
- Separate Query from Modifier, Remove Setting Method
- Replace Derived Variable with Query — for mutable data that could just be calculated instead.
- Change Reference to Value — replace a structure in place rather than modifying it.

### Related

- Concurrency Defense Principles
- Shared State Is Incorrect State

## Shared State Is Incorrect State

> Shared State Is Incorrect State. — Tip 57

**Source:** *The Pragmatic Programmer*, Topic 34 (also Tip 58, "Random Failures Are Often Concurrency Issues").

### What it means in practice

Hunt & Thomas's example is two waiters in a diner. Each checks that there's one slice of pie left in the case, and each promises it to a customer. The problem is that "read, decide, write" isn't **atomic**. Any resource that two concurrent things can change has this problem: memory, a file, a database row, an external API.

The fixes, from crude to clean:
- **Semaphores and mutexes.** They work, but every user has to remember the protocol.
- **Make the resource transactional.** Move the locking *inside* the resource so callers can't get it wrong (`pieCase.takeSlice()` either succeeds or fails, all at once). This is tell dont ask applied to concurrency.
- **Multiple resources** mean deadlock risk. Acquire them in a consistent order, or redesign so you don't need to hold several at once.
- **Non-transactional updates** still need the same care: files, databases and external services all count as shared state.

Better still, avoid sharing state at all (actors and processes).

### Example

```java
// Check-then-act race: two requests both see 1 seat left and both book it
if (flight.availableSeats() > 0) { flight.setAvailableSeats(flight.availableSeats() - 1); bookings.save(...); }

// The resource guards itself: one atomic operation, success or failure
int updated = jdbc.update("UPDATE flights SET seats = seats - 1 WHERE id = ? AND seats > 0", flightId);
if (updated == 0) throw new SoldOutException(flightId);
```

### Related

- Concurrency Defense Principles — Clean Code's "limit the scope of data" and "use copies".
- Programming by Coincidence (`method.md`) — code that "works" only because of lucky timing.
- Debugging (`method.md`)
- Finish What You Start (Balancing Resources)

## Concurrency Defense Principles

> Concurrency is a decoupling strategy. It helps us decouple what gets done from when it gets done.

**Source:** *Clean Code*, Chapter 13 and Appendix A (Brett L. Schuchert).

### What it means in practice

Concurrency is hard, and the myths make it worse: it doesn't always improve performance, it *does* change the design, and you *do* need to understand the container's threading model. Schuchert's defenses:

- **SRP.** Keep concurrency code separate from other code, because concurrent code has its own lifecycle and its own ways of failing.
- **Limit the scope of shared data.** Encapsulate it and keep the number of `synchronized` places small.
- **Use copies of data** instead of sharing it, and merge the results at the end.
- **Threads should be as independent as possible.** Ideally each thread handles one request with no shared state.
- **Know your library** (thread-safe collections, executors, nonblocking structures) and the classic models (producer-consumer, readers-writers, dining philosophers).
- **Beware dependencies between synchronized methods.** Keep synchronized sections small, and plan shutdown early, because shutdown is where deadlocks hide.
- **Testing:** treat random failures as candidate threading problems. Get the non-threaded code working first, then make threading pluggable and tunable. Run with more threads than cores and on different platforms. Instrument the code to force different interleavings.

### Example

```java
// Shared mutable counter: every request thread contends, and bugs hide in the gaps
class RateLimiter { private final Map<String,Integer> hits = new HashMap<>(); synchronized boolean allow(String ip) { ... } }

// Limit scope + use the library: one thread-safe structure, no hand-written locking
class RateLimiter {
    private final ConcurrentHashMap<String, AtomicInteger> hits = new ConcurrentHashMap<>();
    boolean allow(String ip) { return hits.computeIfAbsent(ip, k -> new AtomicInteger()).incrementAndGet() <= LIMIT; }
}
```

### Where it applies

- Shared State Is Incorrect State — Hunt & Thomas's version of "limit the scope of data", with semaphores and transactional resources.
- actors and processes — "threads as independent as possible" taken to the limit: no shared state at all.
- functional programming — Martin argues immutability removes most concurrency problems.

### Related

- Mutable Data and Global Data
- Debugging (`method.md`) — random failures are often concurrency problems (Pragmatic Tip 58).
- Design by Contract
