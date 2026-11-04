# What clean code is

What readable code means, the rules of simple design, consistency, formatting, and how clean code actually gets written.

## Contents

- [What Is Clean Code](#what-is-clean-code)
- [Simple Design Rules (Emergence)](#simple-design-rules-emergence)
- [Code Should Be Obvious](#code-should-be-obvious)
- [Consistency](#consistency)
- [Code Formatting](#code-formatting)
- [Successive Refinement](#successive-refinement)

## What Is Clean Code

> Clean code is simple and direct. Clean code reads like well-written prose. — Grady Booch, quoted in *Clean Code*

**Source:** *Clean Code*, Chapter 1.

### What it means in practice

Martin makes an economic argument before an aesthetic one. A mess slows a team down a little more with every change, until productivity approaches zero. Adding people doesn't help, because the new people don't know the design either. The "grand redesign in the sky" doesn't save you: the rewrite has to chase a moving target, and it ends up a mess of its own. The only way out is to never let the mess build up. Writing code fast and dirty is never the fastest way, even under deadline pressure. Protecting the code is the programmer's professional duty, the same way a doctor washes their hands even when the patient says hurry.

The chapter collects definitions from well-known programmers. They share the same core:
- **Does one thing well** and is focused (Stroustrup). The same idea recurs in Small Functions That Do One Thing (`names-and-functions.md`) and Class Cohesion (Classes Should Be Small) (`objects-and-classes.md`).
- **Reads like prose.** Intent is obvious and there are no surprises (Booch, Cunningham: each routine is pretty much what you expected).
- **Has tests** and **no duplication**, expresses every design idea, and has few entities (Jeffries). These are Beck's Simple Design Rules (Emergence).
- **Looks like it was written by someone who cares** (Feathers).

**We are authors.** Time spent *reading* code is over 10× the time spent *writing* it, so making code easy to read also makes it easier to write. That's the justification for Meaningful Names (`names-and-functions.md`), Code Formatting and everything else in the book.

### Example

```java
// Works, ships today, and costs every future reader ten minutes
if (o.st == 3 && (System.currentTimeMillis() - o.ts) > 2592000000L && !o.f) arch(o);

// The same decision, written for the next reader
if (order.isDelivered() && order.isOlderThan(Duration.ofDays(30)) && !order.isFlagged())
    archive(order);
```

### Where it applies

- boy scout rule — how a team keeps code clean continuously instead of scheduling a rewrite.
- broken windows — Hunt & Thomas's version of the same argument that messes grow on their own.
- software complexity — Ousterhout gives a more precise account of what makes code hard to read and change.

### Related

- Code Should Be Obvious

## Simple Design Rules (Emergence)

> According to Kent, a design is "simple" if it follows these rules: Runs all the tests; Contains no duplication; Expresses the intent of the programmer; Minimizes the number of classes and methods.

**Source:** *Clean Code*, Chapter 12 (Jeff Langr, after Kent Beck).

### What it means in practice

The rules are in priority order, and good design can *emerge* from following them:

1. **Runs all the tests.** A system you can't verify shouldn't ship. Making code testable pushes it toward small, single-purpose classes and toward DIP (`objects-and-classes.md`), so testability is itself a design force.
2. **No duplication.** Duplication of code *and* of implementation. Template Method is a common way to remove duplication at a higher level.
3. **Expressive.** Good names, small functions and classes, standard pattern names, and well-written tests that serve as documentation.
4. **Minimal classes and methods.** The counterweight to rules 2–3. Don't create a class for every concept or an interface for every class just because a rule says so. Rule 4 has the lowest priority.

Rules 2–4 are applied by **refactoring**, which is only safe because of rule 1.

### Example

```java
// Duplication between two exporters (rule 2) …
class CsvSalesExport { byte[] export() { var rows = repo.sales(); /* filter */ /* format CSV */ } }
class XlsxSalesExport { byte[] export() { var rows = repo.sales(); /* same filter */ /* format XLSX */ } }

// … removed with a template method (rules 2 and 3) — without inventing more classes than needed (rule 4)
abstract class SalesExport {
    final byte[] export() { return format(activeSales(repo.sales())); }
    protected abstract byte[] format(List<Sale> rows);
}
```

### Where it applies

- dont repeat yourself — rule 2. Hunt & Thomas generalize it from code to *knowledge*.
- Speculative Generality — what ignoring rule 4 produces.
- three laws of tdd — the practice that makes rule 1 continuous.

### Related

- What Is Clean Code — Ron Jeffries's definition there is these four rules.
- Meaningful Names (`names-and-functions.md`)
- Small Functions That Do One Thing (`names-and-functions.md`)
- Successive Refinement

## Code Should Be Obvious

> If code is obvious, it means that someone can read the code quickly, without much thought, and their first guesses about the behavior or meaning of the code will be correct.

**Source:** *A Philosophy of Software Design*, Chapter 18.

### What it means in practice

Obscurity is one of the two causes of software complexity. Whether code is obvious is judged by the *reader*, not the writer, so code review is the best test. If a reviewer finds something non-obvious, it is, however clear it seemed to you.

**What makes code more obvious:** precise names (`names-and-functions.md`), Consistency, whitespace that separates the parts of a method, and comments (`comments.md`) that fill in what code can't say.

**What makes code less obvious:**
- **Event-driven programming.** You can't follow control flow by reading. Document when each handler is invoked.
- **Generic containers** like `Pair<Integer, Boolean>` or `Tuple`. `getKey()` and `getValue()` hide what the values mean. Define a small named type.
- **Declaring one type and allocating another** (`List<Order> orders = new ArrayList<>()`) when the specific type matters for behavior.
- **Code that violates reader expectations**, like a `main` that returns while background threads keep the program running.

### Example

```java
// Not obvious: what are the key and the value?
Pair<Integer, Boolean> r = inventory.check(sku);
if (r.getValue()) ship(r.getKey());

// Obvious
record StockCheck(int availableUnits, boolean canShipToday) {}
StockCheck stock = inventory.check(sku);
if (stock.canShipToday()) ship(stock.availableUnits());
```

### Related

- Meaningful Names (`names-and-functions.md`)
- Consistency
- Comments Should Describe What Isn't Obvious (`comments.md`)
- Command Query Separation (`names-and-functions.md`) — hidden side effects violate reader expectations.
- What Is Clean Code — Cunningham's line that each routine should be pretty much what you expected.
- Hidden Temporal Coupling (`names-and-functions.md`)
- Code Formatting
- Don't Return Null (and Don't Pass It) (`errors-and-boundaries.md`)

## Consistency

> Consistency is a powerful tool for reducing the complexity of a system and making its behavior more obvious.

**Source:** *A Philosophy of Software Design*, Chapter 17.

### What it means in practice

When similar things are done in similar ways, a reader who has learned one example understands the rest. That reduces cognitive load, and they can make safe assumptions about code they haven't read. Consistency applies to:

- **Names**: one name per concept, never reused for something else (Meaningful Names (`names-and-functions.md`)).
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

- Meaningful Names (`names-and-functions.md`)
- Code Formatting — Martin's "team rules" are consistency for style.
- Code Should Be Obvious

## Code Formatting

> Code formatting is about communication, and communication is the professional developer's first order of business.

**Source:** *Clean Code*, Chapter 5 (also heuristic G10, Vertical Separation).

### What it means in practice

Formatting outlives the code's functionality. The code will change, but the readability habits it establishes stay. Martin's rules:

- **Newspaper metaphor.** A file reads top to bottom like an article: the name is the headline, high-level concepts come first, and details increase as you go down.
- **Vertical openness and density.** Blank lines separate concepts, and lines that belong together stay close.
- **Vertical distance.** Declare variables close to where they're used. Put a caller above its callee (the stepdown rule (`names-and-functions.md`)). Code with **conceptual affinity** (functions that do similar things) sits close together.
- **Horizontal.** Keep lines short. Use whitespace to show precedence and associate things, and don't align columns of declarations: alignment emphasizes the wrong thing. Never collapse indentation, even for one-line `if`s.
- **Team rules win.** A team agrees on one style and everyone uses it, ideally enforced by a formatter, so the codebase reads as if one person wrote it.

### Example

```java
public class InvoiceExporter {                  // headline
    public byte[] export(Invoice invoice) {     // the story, high level
        Document doc = layout(invoice);
        return render(doc);
    }

    private Document layout(Invoice invoice) { ... }   // next level down, right below its caller
    private byte[] render(Document doc) { ... }
}
```

Today this mostly means agreeing on Prettier, Spotless or `gofmt` and never arguing about it again.

### Where it applies

- Consistency — Ousterhout: a consistent style lets readers reuse what they've learned, and conventions should be enforced automatically.
- power tools — Hunt & Thomas: automate formatting checks instead of reviewing them by hand.

### Related

- What Is Clean Code
- One Level of Abstraction per Function (the Stepdown Rule) (`names-and-functions.md`)
- Code Should Be Obvious

## Successive Refinement

> To write clean code, you must first write dirty code and then clean it.

**Source:** *Clean Code*, Chapters 14–16 (case studies: `Args`, JUnit's `ComparisonCompactor`, `SerialDate`).

### What it means in practice

Clean code isn't written in one pass. Martin shows a command-line parser (`Args`) that worked for two argument types and then became a mess when he added a third. Then he did three things:

- **He stopped adding features.** A mess that works is still a mess, and every new feature makes it harder to clean.
- **He went incrementally, with tests always green.** He made a tiny change, ran the tests, and repeated, hundreds of times. He never broke the system for more than a few minutes. A big redesign that leaves the code broken for a while is how good intentions turn into a worse mess.
- **He refactored toward the structure the code needed.** The `Args` design ended up with one `ArgumentMarshaler` per type. Adding a new type now means adding a class (an OCP (`objects-and-classes.md`) move), not editing a growing `switch`.

The JUnit and SerialDate chapters show the same discipline on code that's already good: **first make it work, then make it right**, and leave it better than you found it.

### Example

The shape of `Args` after refinement, recast as a config-file loader:

```java
interface ValueParser { Object parse(String raw); }
Map<Class<?>, ValueParser> parsers = Map.of(
    Integer.class, Integer::valueOf,
    Duration.class, Duration::parse,
    URI.class, URI::create);       // a new setting type = a new entry, not a new branch
```

### Where it applies

- boy scout rule — the everyday version of the same discipline.
- refactor early refactor often and dont outrun your headlights — Hunt & Thomas: small steps, with tests as the safety net.
- Replace Conditional with Polymorphism — the main refactoring in the `Args` case study.

### Related

- Simple Design Rules (Emergence)
- Small Functions That Do One Thing (`names-and-functions.md`)
