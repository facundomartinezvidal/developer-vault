# Names and functions

Choosing names, sizing functions, their arguments, side effects and call ordering.

## Contents

- [Meaningful Names](#meaningful-names)
- [Small Functions That Do One Thing](#small-functions-that-do-one-thing)
- [One Level of Abstraction per Function (the Stepdown Rule)](#one-level-of-abstraction-per-function-the-stepdown-rule)
- [Function Arguments](#function-arguments)
- [Command Query Separation](#command-query-separation)
- [Hidden Temporal Coupling](#hidden-temporal-coupling)

## Meaningful Names

> The name of a variable, function, or class, should answer all the big questions. It should tell you why it exists, what it does, and how it is used. — *Clean Code*

**Source:** *Clean Code*, Chapter 2; *The Pragmatic Programmer*, Topic 44 ("Name Well; Rename When Needed"); *A Philosophy of Software Design*, Chapter 14.

### What it means in practice

All three books treat naming as design work, not decoration.

- **Reveal intent (Martin).** If a name needs a comment to explain it, the name is wrong. Avoid disinformation: don't call something `accountList` if it isn't a `List`, and don't give two things names that differ only slightly. Avoid noise words (`ProductData` vs `ProductInfo`). Use pronounceable, searchable names, with the length matching the scope. Don't use encodings or Hungarian prefixes. Classes are nouns, methods are verbs. **Pick one word per concept** (`fetch`/`retrieve`/`get`: choose one) and don't pun (using one word for two different ideas). Use solution-domain terms (`JobQueue`, `AccountVisitor`) when talking to programmers, and problem-domain terms when no programmer term exists.
- **Name by role and rename freely (Hunt & Thomas).** Name a thing for what it *does* in context, not for what it *is*. Respect the culture of the language and the team. Keep a **project glossary**. When a name no longer fits, rename it: a misleading name is worse than none. If renaming is too hard, that's an ETC problem.
- **Precise and consistent (Ousterhout).** A good name creates an image in the reader's mind. Vague names (`data`, `result`, `count`, `status`) let a reader guess wrong. If a precise name is hard to find, the design may be unclear: the variable might be doing two things. Use the same name for the same thing everywhere, and never for anything else. Ousterhout disagrees with Go's habit of very short names for things that live more than a few lines.

### Example

```java
// Before: you have to read the body to understand
List<int[]> get(List<int[]> l) { ... }          // what list? get what?
int d;                                            // elapsed days? days until due? a discount?

// After
List<Cell> flaggedCells(Board board) { ... }
int daysSinceLastPayment;
```

```java
// Consistency (Ousterhout): one name, one meaning, everywhere
customerId   // always the internal UUID
externalRef  // always the payment-provider id — never also called "customerId"
```

### Where it applies

- intention revealing interfaces — Evans's version at the interface level, in the Ubiquitous Language.
- Mysterious Name — Fowler's smell for when naming goes wrong. Clean Code's N1–N7 heuristics are the same checklist.
- Good and Bad Comments (Clean Code's view) (`comments.md`) — Martin: a good name usually makes the comment unnecessary.
- Comments Should Describe What Isn't Obvious (`comments.md`) — Ousterhout: names can't carry everything, so interface comments fill the gap.

### Related

- Small Functions That Do One Thing — a function that does one thing is easier to name, and a good name keeps it to one thing.
- Consistency (`foundations.md`) — Ousterhout's broader principle, with naming as its most visible case.
- Code Should Be Obvious (`foundations.md`)
- Command Query Separation
- Hidden Temporal Coupling
- Simple Design Rules (Emergence) (`foundations.md`)
- What Is Clean Code (`foundations.md`)

## Small Functions That Do One Thing

> Functions should do one thing. They should do it well. They should do it only.

**Source:** *Clean Code*, Chapter 3 (also heuristic G30).

### What it means in practice

Martin has two rules for functions: they should be small, and then *smaller than that*. That means a handful of lines. The body of an `if` or `while` is usually a single call to a well-named function, and indentation rarely goes past one or two levels.

"One thing" has a test. A function does one thing if you can't extract another function from it whose name isn't just a restatement of the implementation. A function split into sections ("declarations", "initialization", "sieve") is doing several things.

Functions written this way read like a table of contents. Each name says what happens, and you only open the body when you need the detail. This depends on One Level of Abstraction per Function (the Stepdown Rule): doing one thing means staying at one level.

### Example

```java
// Before: validation, pricing, persistence and email in one place
public void placeOrder(Cart cart, User user) {
    if (cart.isEmpty()) throw new IllegalStateException("empty cart");
    for (Item i : cart.items()) if (!stock.has(i)) throw new OutOfStockException(i);
    BigDecimal total = BigDecimal.ZERO;
    for (Item i : cart.items()) total = total.add(i.price().multiply(i.qty()));
    if (user.isPremium()) total = total.multiply(new BigDecimal("0.9"));
    Order o = new Order(user, cart.items(), total); orders.save(o);
    mailer.send(user.email(), "Order " + o.id() + " confirmed");
}

// After: one level, one thing each
public void placeOrder(Cart cart, User user) {
    ensurePlaceable(cart);
    Order order = orders.save(new Order(user, cart.items(), priceFor(cart, user)));
    notifyConfirmation(user, order);
}
```

### A counterpoint

Ousterhout pushes back in deep modules and better together or apart. Splitting a method only helps if each piece is a clean abstraction. If you can't understand one piece without reading the other ("conjoined methods"), the split added interfaces and gained nothing. Depth matters more than length.

### Where it applies

- Long Function — the smell. Extract Function is the fix.
- Command Query Separation and Function Arguments — the other rules for functions in the same chapter.
- structured programming — Martin says that when functions are tiny, Dijkstra's single-entry/single-exit rule isn't needed: an occasional early `return` or `break` is fine.

### Related

- SRP: Single Responsibility Principle (`objects-and-classes.md`) — "one thing" at the function level. SRP is "one actor" at the module level.
- Class Cohesion (Classes Should Be Small) (`objects-and-classes.md`)
- Meaningful Names
- Simple Design Rules (Emergence) (`foundations.md`)
- Successive Refinement (`foundations.md`) — small functions come from refining a draft, not from the first draft.
- Exceptions over Error Codes (`errors-and-boundaries.md`)
- Good and Bad Comments (Clean Code's view) (`comments.md`)
- What Is Clean Code (`foundations.md`)

## One Level of Abstraction per Function (the Stepdown Rule)

> We want the code to read like a top-down narrative. We want every function to be followed by those at the next level of abstraction.

**Source:** *Clean Code*, Chapter 3 (also heuristics G6 and G34).

### What it means in practice

Every statement in a function should be at the same level of abstraction. When high-level intent (`renderInvoice()`) sits next to low-level detail (`sb.append("\n")`), the reader can't tell which lines are essential and which are mechanics. Once a function mixes levels, more details tend to get added to it.

The **Stepdown Rule** orders a file the same way. Each function is followed by the functions it calls, one level down, so the file reads top to bottom like a series of "to do X, we do Y and Z" paragraphs. Code Formatting (`foundations.md`) (the newspaper metaphor, vertical ordering) lays the file out to match.

### Example

```java
// Mixed levels: the business step and string plumbing interleaved
String renderStatement(Account acc) {
    StringBuilder sb = new StringBuilder("Statement for " + acc.owner() + "\n");
    for (Tx t : acc.transactions())
        sb.append(String.format("%-12s %10s%n", t.date(), t.amount()));
    sb.append("Balance: ").append(acc.balance());
    return sb.toString();
}

// One level per function, stepping down
String renderStatement(Account acc) {
    return header(acc) + transactionLines(acc) + footer(acc);
}
private String transactionLines(Account acc) {
    return acc.transactions().stream().map(this::line).collect(joining());
}
private String line(Tx t) { return String.format("%-12s %10s%n", t.date(), t.amount()); }
```

### Where it applies

- different layer different abstraction — Ousterhout's version at the class and layer level: each layer should provide a different abstraction from the layers above and below it.
- policy and level — Martin's architecture version: "level" is distance from inputs and outputs, and high-level policy shouldn't mix with low-level detail.
- Small Functions That Do One Thing — a function has to stay at one level to do one thing.


## Function Arguments

> The ideal number of arguments for a function is zero (niladic). Next comes one (monadic), followed closely by two (dyadic). Three arguments (triadic) should be avoided where possible.

**Source:** *Clean Code*, Chapter 3 (also heuristics F1–F3, G15).

### What it means in practice

Every argument is something the reader has to understand and the tester has to vary. Martin's guidelines:

- **Fewer is better.** Three or more arguments suggest some of them belong together in an **argument object** (`Point(x, y)`, `DateRange(from, to)`).
- **No flag arguments.** A boolean parameter announces that the function does two things. Split it into two functions.
- **No output arguments.** `appendFooter(report)` reads as if the report is being appended *to* something. If a function changes state, it should change its own object's state (`report.appendFooter()`).
- **One-argument functions should be a question or a transformation.** `boolean fileExists(path)` asks a question, and `InputStream open(path)` transforms its input. An event (`passwordAttemptFailedNTimes(int)`) is the rare third form.
- **Names can encode arguments.** `assertExpectedEqualsActual(expected, actual)` is harder to call in the wrong order than `assertEquals`.

### Example

```java
// Before: a flag and a pile of positional arguments
Report generate(LocalDate from, LocalDate to, String customerId, boolean includeRefunds, boolean pdf);

// After: two intents, one cohesive range object
Report salesReport(CustomerId customer, DateRange period);
Report salesReportWithRefunds(CustomerId customer, DateRange period);
// rendering format is a separate concern: pdfRenderer.render(report)
```

### Where it applies

- Long Parameter List — the smell. The fixes are Introduce Parameter Object and Remove Flag Argument.
- Data Clumps — arguments that always travel together are an argument object waiting to happen.
- Command Query Separation — output arguments break it by hiding a command inside something that looks like a query.

### Related

- Small Functions That Do One Thing

## Command Query Separation

> Functions should either do something or answer something, but not both.

**Source:** *Clean Code*, Chapter 3 (principle from Bertrand Meyer).

### What it means in practice

A **query** returns information and changes nothing. A **command** changes state and returns nothing. When one function does both, the caller can't tell from the call site whether it's safe to call. `if (set("username", "bob"))` could be asking "is it already set?" or "did setting it work?".

The same chapter warns against **hidden side effects**. A function named `checkPassword` that also initializes the session is lying about what it does. The hidden side effect creates a temporal coupling: the function is now safe to call only at certain moments. Either perform the side effect openly, in a function named for it, or move it out.

### Example

```java
// Mixed: a query that secretly mutates
public boolean checkPassword(User user, String password) {
    if (hasher.matches(password, user.passwordHash())) {
        sessions.initialize(user);          // surprise side effect
        return true;
    }
    return false;
}

// Separated
public boolean passwordMatches(User user, String password) { return hasher.matches(password, user.passwordHash()); }
public Session logIn(User user) { return sessions.start(user); }   // command, named for its effect

if (auth.passwordMatches(user, pw)) auth.logIn(user);
```

### Where it applies

- side effect free functions — Evans makes the same split in domain models: put logic in side-effect-free functions and keep commands simple.
- functional programming — CQS is a small, local step toward immutability.
- Function Arguments — output arguments are hidden commands.

### Related

- Small Functions That Do One Thing
- Meaningful Names — Clean Code's N7: names should describe side effects.
- Code Should Be Obvious (`foundations.md`)

## Hidden Temporal Coupling

> Temporal couplings are often necessary, but you should not hide the coupling.

**Source:** *Clean Code*, Chapter 17, heuristic G31 (see also Chapter 3's "Have No Side Effects").

### What it means in practice

Sometimes calls have to happen in a particular order: load, then validate, then save. If that order exists only in the programmer's head, someone will eventually reorder the calls and break things without noticing. The fix is to make each step need the *result* of the previous one. That creates a "bucket brigade" where the order is enforced by the data flow, so the code won't compile if the steps are reordered.

This costs a little ceremony (extra return values), and it's worth it, because the coupling stays visible.

### Example

```java
// Hidden: nothing stops someone from calling these out of order
importer.readFile(path);
importer.validateRows();
importer.persist();

// Explicit: each step consumes the previous step's output
RawRows raw = importer.read(path);
ValidRows valid = importer.validate(raw);
importer.persist(valid);
```

### Where it applies

- Breaking Temporal Coupling (`concurrency.md`) — Hunt & Thomas use the term at the workflow and concurrency level: find which steps really must be ordered and let the rest run in parallel.
- Command Query Separation — hidden side effects are the most common source of hidden temporal coupling.
- transforming programming — pipelines make ordering explicit by design, because each stage takes the previous stage's output.

### Related

- Code Should Be Obvious (`foundations.md`)
- Meaningful Names
- Concurrency Defense Principles (`concurrency.md`)
- Finish What You Start (Balancing Resources) (`errors-and-boundaries.md`)
