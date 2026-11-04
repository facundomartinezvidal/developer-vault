# Modules and interfaces

How deep a module should be, what it should hide, and whether two things belong together.

## Contents

- [Deep Modules](#deep-modules)
- [Information Hiding (and Leakage)](#information-hiding-and-leakage)
- [General-Purpose Modules Are Deeper](#general-purpose-modules-are-deeper)
- [Pull Complexity Downwards](#pull-complexity-downwards)
- [Different Layer, Different Abstraction](#different-layer-different-abstraction)
- [Better Together or Better Apart?](#better-together-or-better-apart)
- [Orthogonality](#orthogonality)
- [DRY — Don't Repeat Yourself](#dry-dont-repeat-yourself)

## Deep Modules

> The best modules are those that provide powerful functionality yet have simple interfaces.

**Source:** *A Philosophy of Software Design*, Chapter 4.

### What it means in practice

A module (class, function, service, subsystem) has an **interface**, which is what users must know, and an **implementation**, which does the work. The interface is the *cost* the module imposes on everyone who uses it. The functionality is the *benefit*. Picture each module as a rectangle: the top edge is the interface, the area is the functionality.

- **Deep module.** A small interface hiding a lot of functionality. Unix file I/O is the classic example: five calls (`open`, `read`, `write`, `lseek`, `close`) hide disks, caching, permissions and file systems. Garbage collectors are deep too, with *no* interface at all.
- **Shallow module.** The interface is almost as complex as what it does (a linked-list class, a one-line wrapper method). Using it costs about as much as writing the code yourself.
- **Classitis.** The belief that "classes should be small", followed to excess: many shallow classes, each adding an interface to learn. Java I/O is his example. Opening a buffered file reader takes three objects (`FileInputStream` → `BufferedInputStream` → `ObjectInputStream`), even though buffering should simply be the default.

An interface has **formal** parts (signatures, types) and **informal** parts (side effects, ordering constraints, when to call it). Both count toward its cost. **Make the common case simple**: defaults should do the right thing.

### Example

```java
// Shallow: the caller does all the work through a thin interface
EmailMessage m = new EmailMessage(); m.setHeader("To", to); m.setHeader("From", from);
m.setBody(renderer.render(template, model)); m.setMime("text/html"); smtp.connect(); smtp.send(m.encode()); smtp.close();

// Deep: one call, the module owns templating, MIME, retries, provider failover
notifications.sendEmail(customer, Template.ORDER_SHIPPED, Map.of("order", order));
```

### Contrast with Clean Code

Martin's small functions and class cohesion push toward many small units. Ousterhout says smallness is not a goal in itself: *depth* is. A small class is fine if it hides something meaningful. It's harmful if it's just a pass-through. The two agree on avoiding large classes that do many unrelated things.

### Where it applies

- Information Hiding (and Leakage) — the main way to make a module deep.
- facade pattern — a facade is a deliberate deep module in front of a messy subsystem.
- clean boundaries — a good wrapper around a vendor SDK is deep.
- Middle Man and Lazy Element — Fowler's smells for shallow modules.

### Related

- General-Purpose Modules Are Deeper — general-purpose interfaces tend to be deeper.
- Different Layer, Different Abstraction — pass-through methods are the shallowest kind of code.
- Pull Complexity Downwards
- Software Complexity (`complexity.md`)
- Better Together or Better Apart?
- Define Errors Out of Existence (`robustness-and-testability.md`)
- Designing for Performance (`complexity.md`)

## Information Hiding (and Leakage)

> Each module should encapsulate a few pieces of knowledge, which represent design decisions. The knowledge is embedded in the module's implementation but does not appear in its interface.

**Source:** *A Philosophy of Software Design*, Chapter 5 (idea from David Parnas, 1971).

### What it means in practice

Information hiding is how you build Deep Modules. Each module owns a few *design decisions*: a data format, an algorithm, a protocol, a storage layout. Nothing outside the module depends on them. Hidden information reduces both causes of complexity (`complexity.md`): the interface is simpler, and there are fewer dependencies. Making a field `private` isn't enough. If a getter exposes it, the information hasn't been hidden.

**Information leakage** is the opposite: one design decision shows up in several modules, so changing it means changing all of them. Leakage can happen without either module mentioning the other in its interface, for example when two classes both know a file format. The fix is usually to merge the modules, or to pull the shared knowledge into one new module.

**Temporal decomposition** is a common cause. The code is structured by *the order in which things happen* (read file → modify → write file), so the same knowledge (the file format) appears in each step. Structure by *knowledge* instead.

**Overexposure** happens when an API forces users to know about rarely used features in order to use the common ones. Also: hide information *within* a class, by making each method encapsulate its own piece. Don't take hiding too far, either: information callers actually need should be exposed.

### Example

```java
// Leakage via temporal decomposition: the CSV layout lives in both reader and writer
class ReportReader { List<Sale> read(Path p) { /* split(";"), column 3 = amount in cents */ } }
class ReportWriter { void write(Path p, List<Sale> s) { /* join(";"), amount in cents at column 3 */ } }

// Hidden: one module owns the format decision
class SalesCsvFormat {
    List<Sale> parse(Path p) { ... }
    void write(Path p, List<Sale> sales) { ... }
}
```

### Where it applies

- Encapsulate What Varies (`coupling.md`) — *Head First*'s version: hide the decision most likely to change.
- single responsibility principle and common closure principle — group code by the decision it depends on.
- Divergent Change and Shotgun Surgery — Fowler's smells for information leakage.
- data object anti symmetry — Martin's "getters and setters aren't abstraction" makes the same point.

### Related

- Deep Modules
- Better Together or Better Apart? — leakage is a strong reason to merge.
- Orthogonality
- Decoupling (`coupling.md`)
- Principle of Least Knowledge (Law of Demeter) (`coupling.md`)
- Inheritance Tax (`coupling.md`) — implementation inheritance leaks the parent's decisions into subclasses.
- General-Purpose Modules Are Deeper
- Pull Complexity Downwards

## General-Purpose Modules Are Deeper

> The sweet spot is to implement new modules in a somewhat general-purpose fashion.

**Source:** *A Philosophy of Software Design*, Chapter 6.

### What it means in practice

When you design a module, you can make it fit today's exact need, or try to anticipate all future needs. Ousterhout picks the middle: **somewhat general-purpose**. The *functionality* covers only today's needs, but the *interface* is general enough to support other uses. That kind of interface tends to be simpler and deeper than a special-purpose one, because it isn't tied to one caller's details.

His example is a text editor's text class. Special-purpose methods like `backspace(cursor)` and `delete(selection)` pull UI concepts into the text class. General methods like `insert(position, text)` and `delete(start, end)` are fewer, simpler, and let the UI code build its own operations on top.

Questions to ask:
- What's the **simplest interface that covers all my current needs**?
- In **how many situations** will this method be used? If the answer is one, it's probably too special-purpose.
- Is the API **easy to use for my current needs**? If using it takes a lot of extra code, it's too general.

Also: **push specialization up** (into the UI or app layer) **or down** (into drivers), and keep the core general.

### Example

```java
// Special-purpose: the notification service knows every business event
void sendOrderShippedEmail(Order o); void sendPasswordResetEmail(User u); void sendInvoiceOverdueSms(Invoice i);

// Somewhat general-purpose: one deep operation, specialization pushed up to callers
void send(Recipient to, Channel channel, Template template, Map<String, Object> model);
```

### Where it applies

- Deep Modules — general-purpose interfaces are usually deeper.
- Don't Outrun Your Headlights (`complexity.md`) — Hunt & Thomas: don't build for a future you can't see. "Somewhat general" means a general *interface* without extra speculative *features*.
- Speculative Generality — Fowler's smell for going too general.

### Related

- Information Hiding (and Leakage)
- Pull Complexity Downwards
- Better Together or Better Apart? — separate general-purpose code from special-purpose code.

## Pull Complexity Downwards

> It is more important for a module to have a simple interface than a simple implementation.

**Source:** *A Philosophy of Software Design*, Chapter 8.

### What it means in practice

When some complexity can't be avoided, decide *who* deals with it. A module usually has many more users than developers, so it's better for the module's developers to absorb the complexity once than for every caller to handle it. If you can handle it inside the module, do.

**Configuration parameters** are a common way to push complexity *up*. Rather than deciding a retry policy or buffer size, a module exports a knob and makes every user choose. But users usually know less than the module does. Before adding a parameter, ask: "Will users be able to pick a better value than we could compute?" Prefer sensible defaults, or compute the value dynamically (for example, adapt a timeout to the measured latency).

**Taking it too far:** only pull complexity down when it's closely related to the module's existing functionality, *and* it simplifies the rest of the system, *and* it simplifies the module's interface. Moving all of an app's UI-specific logic into a text class would violate this.

### Example

```java
// Complexity pushed up: every caller must decide retry behavior
client.charge(amount, card, /*retries*/ 3, /*backoffMs*/ 200, /*retryOn*/ Set.of(503, 429));

// Pulled down: the gateway knows which failures are retryable and handles idempotency itself
client.charge(amount, card);   // retries 429/503 with jittered backoff using an internal idempotency key
```

### Where it applies

- Deep Modules — a simple interface over a richer implementation.
- Externalize Configuration (`coupling.md`) — Hunt & Thomas's case for configuration. Ousterhout's counterweight: externalize only what really varies between deployments.
- Define Errors Out of Existence (`robustness-and-testability.md`) — handling an exception inside the module is pulling complexity down.

### Related

- General-Purpose Modules Are Deeper
- Information Hiding (and Leakage)

## Different Layer, Different Abstraction

> If a system contains adjacent layers with similar abstractions, this is a red flag that suggests a problem with the class decomposition.

**Source:** *A Philosophy of Software Design*, Chapter 7.

### What it means in practice

In a well-designed layered system, each layer gives a *different* abstraction from the layers above and below it. A file system's layers go from files to blocks to disk sectors, and each one transforms the concept. When adjacent layers have the same abstraction, that's a sign of a bad split:

- **Pass-through methods.** A method that just calls a method with the same signature on another class. It adds interface without adding functionality. Fix it by exposing the lower class directly, redistributing the work, or merging the classes.
- **When duplicate interfaces are OK.** A **dispatcher** (same signature, different implementations chosen at runtime) or multiple implementations of the same interface each add real functionality.
- **Decorators** are often shallow pass-throughs. Before writing one, ask: could this go in the base class, or in the caller? Could it be merged with an existing decorator?
- **Interface vs. implementation.** A class's interface should differ from its implementation. If they mirror each other, the class isn't abstracting anything.
- **Pass-through variables.** A value threaded through many layers that don't use it. Alternatives: a shared object that every layer already has, a global (not recommended), or a **context object** created at startup and referenced where needed.

### Example

```java
// Pass-through: the service layer adds a layer but no abstraction
class CustomerService { Customer find(UUID id) { return customerRepository.find(id); } void save(Customer c) { customerRepository.save(c); } }

// Each layer earns its place: the service speaks in use cases, the repository in persistence
class CustomerOnboarding {
    Customer register(SignupForm form) { /* validate, dedupe by email, create, assign plan, emit event */ }
}
```

### Where it applies

- layered architecture — Evans's layers each carry a distinct responsibility.
- clean architecture layers — entities, use cases, adapters and frameworks are four different abstractions.
- Middle Man — Fowler's smell for pass-throughs. The fix is Remove Middle Man.
- decorator pattern — legitimate when it adds real behavior, shallow when it only forwards calls.
- one level of abstraction per function — Martin's version of the same idea at the function level.

### Related

- Deep Modules
- Decoupling (`coupling.md`) — a context object is "if it's important enough to be global, wrap it in an API".

## Better Together or Better Apart?

> The goal is to reduce the complexity of the system as a whole and improve its modularity.

**Source:** *A Philosophy of Software Design*, Chapter 9.

### What it means in practice

Splitting code into more pieces isn't automatically better. More pieces mean more interfaces to learn, more code to manage them, and pieces that are harder to see together. Ousterhout's guidance:

**Bring together when:**
- the pieces **share information** (the same format or protocol knowledge, which is leakage otherwise);
- they're **used together** in both directions;
- they **overlap conceptually**, sharing a higher-level category;
- it's **hard to understand one without the other**;
- combining them **simplifies the interface** or **eliminates duplication**.

**Separate when:**
- one piece is **general-purpose** and the other **special-purpose** (keep them in different modules);
- the code is unrelated.

**Splitting methods.** Long methods aren't automatically bad. Split one only if it produces a cleaner abstraction: a subtask that can be understood independently, or several methods each with a simple interface. Watch for **conjoined methods**, where you can't understand one piece without reading the other. That's a split that made things worse. Combining methods can also be the right fix.

### Example

```java
// Split badly: conjoined — validate() only makes sense if you read normalize()'s internals
Address normalize(AddressForm f) { /* uppercases, strips, but leaves zip unvalidated on purpose */ }
void validate(Address a) { /* assumes normalize() already uppercased country codes */ }

// Together: one cohesive operation with a simple contract
Address parseAddress(AddressForm form) throws InvalidAddressException { ... }
```

### Contrast with Clean Code

Martin's small functions says "extract till you drop". Ousterhout says length isn't the problem: depth and independence are. They agree on the goal (readable, single-purpose code) but disagree on the default. Use the conjoined-methods test to decide.

### Related

- Deep Modules
- Information Hiding (and Leakage)
- General-Purpose Modules Are Deeper

## Orthogonality

> Eliminate Effects Between Unrelated Things. — Tip 17

**Source:** *The Pragmatic Programmer*, Topic 10.

### What it means in practice

Two components are **orthogonal** if changing one doesn't affect the other. The book's counterexample is a helicopter, where every control affects every other one. In orthogonal systems components are self-contained, independent, and have a single, well-defined purpose. The payoff:

- **Productivity:** changes stay local, and combining orthogonal parts gives multiplicative functionality (M × N).
- **Lower risk:** a bug is contained in one module, and replacing a part doesn't ripple.

How to keep code orthogonal:
- Write **"shy" code** that doesn't reveal or depend on what it doesn't need (Law of Demeter (`coupling.md`), Decoupling (`coupling.md`)).
- **Avoid global data**. Pass context explicitly.
- **Avoid similar functions**. Shared structure suggests a Strategy.
- **Wrap third-party toolkits** so their quirks don't spread through your code.

A quick test for a design: "If I dramatically change the requirements behind one function, how many modules are affected?" The answer should be one.

### Example

```java
// Not orthogonal: changing the audit store breaks billing logic
class InvoiceService { void issue(Invoice i) { ...; jdbc.update("INSERT INTO audit ..."); } }

// Orthogonal: auditing is its own axis, plugged in from outside
class InvoiceService { InvoiceService(AuditLog audit) {...} void issue(Invoice i) { ...; audit.record(new InvoiceIssued(i.id())); } }
```

### Where it applies

- single responsibility principle — orthogonality is SRP stated as independence between modules.
- Strive for Loosely Coupled Designs (`coupling.md`) — the *Head First* name for the same goal.
- separate construction from use — Clean Code's cross-cutting concerns (logging, auditing, transactions) are its main source of orthogonality.
- aggregate and bounded context — DDD's units of independent change.

### Related

- ETC — Easier to Change (`complexity.md`)
- DRY — Don't Repeat Yourself
- Decoupling (`coupling.md`)
- Information Hiding (and Leakage) — Ousterhout's information leakage is a loss of orthogonality.
- Software Complexity (`complexity.md`) — change amplification is the symptom of non-orthogonal code.
- Breaking Temporal Coupling (`concurrency.md`)
- Shared State Is Incorrect State (`concurrency.md`)
- Refactor Early, Refactor Often (`complexity.md`)

## DRY — Don't Repeat Yourself

> Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

**Source:** *The Pragmatic Programmer*, Topic 9 (Tips 15–16); also *Clean Code* Chapters 3 and 12 and heuristic G5.

### What it means in practice

DRY is about **knowledge and intent, not text**. Two identical-looking lines that express different rules aren't a DRY violation. One rule expressed in two different-looking places *is* one. Hunt & Thomas list where duplication shows up:

- **In code:** copy-paste, but also *representational* duplication (a field that can be derived from others, such as storing `length` next to `start` and `end`).
- **In documentation:** comments that restate the code, which go stale when the code changes.
- **In data:** cached or derived values that can drift. Use an accessor instead (the uniform access principle).
- **Between systems:** an API spec, server code and client code each describing the same contract. Generate one from another.
- **Between developers:** two people building the same utility. Fix this with communication, a project librarian, and reuse that's easy (Tip 16).

Martin's version in Clean Code is more about code: duplication is "the root of all evil in software", and every `switch` repeated across the code is duplicated knowledge.

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

Martin's accidental duplication warns against the opposite mistake: merging two pieces of code that look alike but change for different reasons (different actors). DRY applies to the *same knowledge*. Code that only happens to look the same should stay separate.

### Where it applies

- Duplicated Code — Fowler's smell for the code-level case.
- simple design rules — "no duplication" is Beck's rule 2.
- Repeated Switches — the same type switch in several places is duplicated knowledge.
- Externalize Configuration (`coupling.md`) — one source for values that change per environment.

### Related

- ETC — Easier to Change (`complexity.md`)
- Orthogonality
- Consistency (`complexity.md`)
- Modifying Existing Code (`complexity.md`)
- Software Complexity (`complexity.md`)
