# Objects, classes and SOLID

Objects versus data structures, cohesion, construction versus use, and the SOLID principles applied to classes.

## Contents

- [Data/Object Anti-Symmetry](#dataobject-anti-symmetry)
- [Class Cohesion (Classes Should Be Small)](#class-cohesion-classes-should-be-small)
- [Separate Constructing a System from Using It](#separate-constructing-a-system-from-using-it)
- [Tell, Don't Ask](#tell-dont-ask)
- [SRP: Single Responsibility Principle](#srp-single-responsibility-principle)
- [OCP: Open-Closed Principle](#ocp-open-closed-principle)
- [LSP: Liskov Substitution Principle](#lsp-liskov-substitution-principle)
- [ISP: Interface Segregation Principle](#isp-interface-segregation-principle)
- [DIP: Dependency Inversion Principle](#dip-dependency-inversion-principle)

## Data/Object Anti-Symmetry

> Objects hide their data behind abstractions and expose functions that operate on that data. Data structures expose their data and have no meaningful functions.

**Source:** *Clean Code*, Chapter 6.

### What it means in practice

Objects and data structures are opposites, and each makes the other's easy case hard:

| | Add a new **type** | Add a new **operation** |
|---|---|---|
| **Objects** (polymorphism) | easy — one new class | hard — touch every class |
| **Data structures** (procedural) | hard — touch every function | easy — one new function |

So neither is always right. Expecting new kinds of things? Use objects. Expecting new operations over a stable set of types? Use plain data and functions. "Everything is an object" is a myth.

**Data abstraction.** Hiding fields behind getters and setters isn't encapsulation. An object should expose *operations in terms of the abstraction* (`fuelPercentRemaining()`), not its variables (`getGallonsOfGasoline()`).

**Hybrids are the worst of both**: half-objects with public data *and* business methods. They're hard to extend in either direction. **DTOs** and **Active Records** are legitimate data structures. Keep business rules out of them and put the rules in separate objects that wrap or use them.

The **Law of Demeter** is in this chapter too. It applies to *objects*. Chaining through a plain data structure's fields isn't a violation, but chaining through an object's getters is a "train wreck".

### Example

```java
// Data structures + functions: easy to add a new report, hard to add a new payment kind
record CardPayment(Money amount, String last4) {}
record BankTransfer(Money amount, String iban) {}
Money fee(Object p) { return switch (p) { case CardPayment c -> ...; case BankTransfer b -> ...; default -> ...; }; }

// Objects: easy to add a new payment kind, hard to add a new operation across all of them
interface Payment { Money fee(); }
class CardPayment implements Payment { public Money fee() { ... } }
class BankTransfer implements Payment { public Money fee() { ... } }
```

### Where it applies

- visitor pattern — the standard way to add *operations* to an object hierarchy, accepting that adding types gets harder.
- Repeated Switches — what the procedural side looks like when the set of types keeps changing.
- Data Class — Fowler treats it as a smell. Martin says it's fine *as a data structure* and a smell only as a hybrid.
- functional programming and object oriented programming — the two paradigms this table is about.

### Related

- OCP: Open-Closed Principle
- Tell, Don't Ask

## Class Cohesion (Classes Should Be Small)

> We want our systems to be composed of many small classes, not a few large ones. Each small class encapsulates a single responsibility, has a single reason to change, and collaborates with a few others.

**Source:** *Clean Code*, Chapter 10 (Martin & Jeff Langr).

### What it means in practice

For a class, "small" means few *responsibilities*, not few lines. A quick test is whether you can describe the class in about 25 words without using "if", "and", "or" or "but". Names like `Processor`, `Manager` or `Super` hint that the class does too much.

**Cohesion** is how many of a class's instance variables each method uses. When every method uses every field, the class is maximally cohesive. When splitting a big function forces you to promote locals to fields that only some methods use, cohesion drops, and that's the moment to split the class. Keeping classes cohesive naturally produces many small classes. Martin's analogy: would you rather have a toolbox with labeled drawers, or a few drawers you dump everything into?

**Organizing for change.** Opening a class to add a feature is a risk. Structure classes so new behavior comes from *adding* a class (one SQL statement type per subclass), and isolate concrete details behind interfaces so tests can substitute them.

### Example

```java
// Low cohesion: two groups of methods using two disjoint groups of fields
class CustomerAccount {
    String email, passwordHash, mfaSecret;          // used by login methods
    List<Invoice> invoices; Money credit;           // used by billing methods
    boolean verifyPassword(String pw) { ... } boolean verifyMfa(String code) { ... }
    Money balanceDue() { ... } void applyCredit(Money m) { ... }
}

// Split along the cohesion seam
class Credentials { String email, passwordHash, mfaSecret; boolean verifyPassword(...); boolean verifyMfa(...); }
class BillingAccount { List<Invoice> invoices; Money credit; Money balanceDue(); void applyCredit(Money m); }
```

### Contrast with Ousterhout

deep modules criticizes "classitis": too many small, *shallow* classes, each adding an interface to learn. The two views fit together once you look at depth. Martin's small classes are fine when each one hides a real decision. They're harmful when they're pass-throughs.

### Where it applies

- SRP: Single Responsibility Principle — the principle behind this chapter. Clean Code states it as "one reason to change".
- Large Class and Divergent Change — the smells of low cohesion. The fix is Extract Class.
- OCP: Open-Closed Principle — "organizing for change" is OCP at the class level.

### Related

- DIP: Dependency Inversion Principle — "isolating from change" with interfaces.
- Small Functions That Do One Thing (`names-and-functions.md`)
- What Is Clean Code (`foundations.md`)

## Separate Constructing a System from Using It

> Software systems should separate the startup process, when the application objects are constructed and the dependencies are "wired" together, from the runtime logic that takes over after startup.

**Source:** *Clean Code*, Chapter 11 (Kevin Dean Wampler).

### What it means in practice

Lazy initialization inside business code (`if (service == null) service = new MyServiceImpl(...)`) hard-wires a concrete dependency, mixes two responsibilities, and makes testing harder. Martin's alternatives:

- **Separation of main.** Construct everything in `main` (or modules it calls) and pass finished objects into the application. The application assumes everything has already been built.
- **Factories** when the application has to decide *when* to create something (an order creates its line items). The application owns the factory *interface*, and `main` provides the implementation.
- **Dependency Injection.** An object gets its dependencies through constructors or setters instead of building them. A container or `main` does the wiring.

The chapter then scales the idea up. Concerns that **cut across** many objects (persistence, transactions, security) shouldn't be written by hand in each class. Use proxies, AOP, or a framework, so the domain objects stay plain (POJOs). An architecture built this way can grow incrementally, and decisions can be put off until the last responsible moment. Apply standards only when they add value, and use domain-specific languages where they help.

### Example

```java
// Before: the use case builds its own collaborators
public class CheckoutService {
    private PaymentGateway gateway;
    public Receipt checkout(Cart cart) {
        if (gateway == null) gateway = new StripeGateway(System.getenv("STRIPE_KEY"));  // construction mixed with use
        return gateway.charge(cart.total(), cart.card());
    }
}

// After: wired at startup, used at runtime
public class CheckoutService {
    private final PaymentGateway gateway;
    public CheckoutService(PaymentGateway gateway) { this.gateway = gateway; }
    public Receipt checkout(Cart cart) { return gateway.charge(cart.total(), cart.card()); }
}
// Main / composition root
var checkout = new CheckoutService(new StripeGateway(config.stripeKey()));
```

### Where it applies

- main component — Clean Architecture's "Main is the dirtiest component", the same idea at the architecture level.
- DIP: Dependency Inversion Principle — the factory interface belongs to the application, and its implementation belongs to `main`.
- abstract factory pattern and factory method pattern — the factories this chapter talks about.
- proxy pattern and decorator pattern — how cross-cutting concerns get wrapped around plain objects.


## Tell, Don't Ask

> Tell, Don't Ask. — Tip 45

**Source:** *The Pragmatic Programmer*, Topic 28.

### What it means in practice

Don't ask an object for its state, make a decision based on that state, and then update the object. That moves the object's responsibility into the caller and couples the caller to the object's internals. Instead, *tell* the object what you want and let it decide. Each object hides its own state and enforces its own rules.

This is the usual fix for a train wreck: a chain of getters becomes one intention-revealing call on the nearest object, which delegates to the next one.

### Example

```java
// Ask: the controller makes the subscription's decision for it
if (sub.getStatus() == ACTIVE && sub.getPaidUntil().isBefore(today)) {
    sub.setStatus(PAST_DUE);
    sub.setGraceEndsOn(today.plusDays(7));
}

// Tell: the subscription owns its own state transitions
sub.markOverdueIfUnpaidAsOf(today);
```

### Where it applies

- principle of least knowledge — TDA is how you follow the Law of Demeter without writing pass-through wrappers everywhere.
- Feature Envy — the smell for "asking": a method more interested in another object's data than its own.
- Data/Object Anti-Symmetry — TDA applies to *objects*. Plain data structures are meant to be asked.

### Related

- Shared State Is Incorrect State (`concurrency.md`) — telling a resource to act atomically instead of check-then-act.

## SRP: Single Responsibility Principle

> A module should be responsible to one, and only one, actor.

**Source:** *Clean Architecture*, Chapter 7.

### What it means in practice

SRP is widely misquoted as "a module should do one thing" — that's a different, function-level principle. The real SRP is about *organizational* coupling: a module should answer to exactly one **actor** (a stakeholder or group of stakeholders who'd request the same kind of change). "Gather together those things that change at the same times and for the same reasons; separate those things that change at different times or for different reasons."

When code serving two different actors is crammed into one class, a change requested by actor A can accidentally break behavior actor B depends on — because both changes touch the same file, get merged by the same team, and share state neither actor intended to share. The fix is splitting by actor, even if it means more, smaller classes.

### Example: a class three stakeholders depend on

```java
// Violates SRP: HR, payroll, and DBAs all have a reason to change this class
public class Employee {
    public Money calculatePay() { /* payroll's concern */ }
    public Report reportHours() { /* HR's concern */ }
    public void save() { /* DBA's concern */ }
}
```

```java
// Split by actor — each class now has exactly one reason to change
public class PayCalculator {
    public Money calculatePay(EmployeeData data) { /* ... */ }
}

public class HoursReporter {
    public Report reportHours(EmployeeData data) { /* ... */ }
}

public class EmployeeRepository {
    public void save(EmployeeData data) { /* ... */ }
}
```

A change to how hours get reported no longer risks breaking how pay gets calculated — they're not even in the same file anymore, and different teams can own each one independently.

### Related

- OCP: Open-Closed Principle
- Class Cohesion (Classes Should Be Small)
- Small Functions That Do One Thing (`names-and-functions.md`)
- Concurrency Defense Principles (`concurrency.md`)

## OCP: Open-Closed Principle

> A software artifact should be open for extension but closed for modification.

**Source:** *Clean Architecture*, Chapter 8.

### What it means in practice

At the architecture level this isn't a small class-design tweak — Martin calls it "the most fundamental reason we study software architecture." A good design lets new requirements be met by **adding** code, not editing existing, already-tested code. That requires two things working together: separating things that change for different reasons (SRP), and then directing the dependencies between those pieces (via interfaces) so that important, stable components never depend on volatile, low-level ones. "If component A should be protected from changes in component B, then component B should depend on component A" — not the other way around.

This produces a hierarchy of "levels": the most protected component (business rules) sits at the top, shielded by interfaces from everything underneath it (UI, database, frameworks), which are free to change without ever forcing a change in the business rules.

### Example: adding a payment method without touching checkout

```java
public interface PaymentStrategy {
    void pay(BigDecimal amount);
}

public class Checkout {
    private final PaymentStrategy paymentStrategy;
    public Checkout(PaymentStrategy paymentStrategy) { this.paymentStrategy = paymentStrategy; }
    public void completeOrder(BigDecimal amount) { paymentStrategy.pay(amount); }
}
```

Adding cryptocurrency payments later means writing `CryptoPayment implements PaymentStrategy` — `Checkout` is never opened, recompiled, or redeployed. It's open for extension (new `PaymentStrategy` implementations) and closed for modification (nothing about `Checkout` changes). See Strategy Pattern for the full walkthrough — Strategy is OCP applied directly.

### Related

- SRP: Single Responsibility Principle
- DIP: Dependency Inversion Principle — the dependency-direction mechanism that makes OCP possible.
- Class Cohesion (Classes Should Be Small)
- Data/Object Anti-Symmetry
- Exceptions over Error Codes (`errors-and-boundaries.md`)
- Successive Refinement (`foundations.md`)

## LSP: Liskov Substitution Principle

> If for each object o1 of type S there is an object o2 of type T such that for all programs P defined in terms of T, the behavior of P is unchanged when o1 is substituted for o2, then S is a subtype of T.

**Source:** *Clean Architecture*, Chapter 9. (Barbara Liskov, 1988.)

### What it means in practice

Plainly: if code is written against an interface/supertype, any implementation of it must be swappable in without the calling code noticing a behavior difference. This started as guidance about inheritance (the textbook illustration is a `Square` that "is-a" `Rectangle` but breaks any code that sets width and height independently), but Martin extends it to any interface/implementation relationship — Java interfaces, REST APIs sharing a contract, plugins.

Violations don't stay contained: when one implementation doesn't honor the contract clients assume, calling code fills up with special-case `if`s to route around it, and that special-casing tends to leak into the architecture as extra mechanisms (config tables, feature flags) just to keep incompatible implementations from breaking each other.

### Example: an "add" that lies about its own interface

```java
List<String> names = getNames(); // could be an ArrayList — or an unmodifiable view
names.add("New Name");
```

If `getNames()` sometimes returns `Collections.unmodifiableList(...)`, this throws `UnsupportedOperationException` at runtime — even though the code only depends on `List`, per Program To An Interface. `List` promises `add()` works; an unmodifiable implementation silently breaks that promise. Any code written generically against `List` is an LSP violation waiting to happen the moment it meets that implementation.

### Related

- ISP: Interface Segregation Principle
- Design by Contract (`errors-and-boundaries.md`)

## ISP: Interface Segregation Principle

> Clients should not be forced to depend on methods they do not use.

**Source:** *Clean Architecture*, Chapter 10.

### What it means in practice

A fat interface with unrelated methods forces every caller to depend on the whole thing, even the parts it never calls — "depending on something that carries baggage you don't need can cause you troubles you didn't expect." In statically typed languages this is sharpest: a change to any method's signature forces every dependent to recompile and redeploy, even callers that never touch that method. Martin generalizes this past interfaces to architecture: depending on a framework that itself drags in something unrelated (say, a specific database library) means unrelated failures in that dependency can still ripple up into your system.

### Example: a fat gateway interface

```java
// Violates ISP: Checkout only calls charge(), but depends on all four methods
public interface PaymentGateway {
    void charge(BigDecimal amount);
    void refund(String transactionId);
    Report generateComplianceReport();
    void syncWithAccounting();
}
```

```java
// Segregated: each client depends only on what it actually uses
public interface Payments {
    void charge(BigDecimal amount);
    void refund(String transactionId);
}

public interface PaymentReporting {
    Report generateComplianceReport();
    void syncWithAccounting();
}

public class StripeAdapter implements Payments, PaymentReporting { /* ... */ }
```

`Checkout` now depends only on `Payments`. A signature change in `generateComplianceReport()` no longer forces `Checkout` to recompile or redeploy — it was never using that method anyway.

### Related

- LSP: Liskov Substitution Principle

## DIP: Dependency Inversion Principle

> The most flexible systems are those in which source code dependencies refer only to abstractions, not to concretions.

**Source:** *Clean Architecture*, Chapter 11.

### What it means in practice

This is the SOLID, formally-named version of Program To An Interface, Not An Implementation — same idea, one book calling it a naming convention, the other calling it an architectural law. DIP isn't absolute: depending on a genuinely stable concretion (`java.lang.String`) is harmless. The danger is depending on a **volatile** concrete class — one you're actively changing. Four rules keep that in check: don't refer to, derive from, or override volatile concrete classes, and don't name anything concrete-and-volatile if you can avoid it.

The one problem this creates: *something* has to call `new` on the real implementation eventually. DIP's answer is an **Abstract Factory** — a factory interface that creates the abstraction, implemented by a concrete factory that's the only place in the system allowed to mention the volatile concrete class. Most systems push every DIP violation like this into one place (often called `main`), so the rest of the codebase never mentions a concrete type at all.

### Example: the same idea as Program To An Interface, plus construction

```java
public interface PaymentGateway { void charge(BigDecimal amount); }

public interface PaymentGatewayFactory {
    PaymentGateway create();
}

public class StripeGatewayFactory implements PaymentGatewayFactory {
    public PaymentGateway create() {
        return new StripeAdapter(new StripeClient()); // the only place that names StripeAdapter
    }
}
```

`OrderService` depends on `PaymentGateway` and `PaymentGatewayFactory` — both abstractions. Nothing outside `StripeGatewayFactory` ever names `StripeAdapter` or `StripeClient`.

### Related

- OCP: Open-Closed Principle
- Class Cohesion (Classes Should Be Small)
- Clean Boundaries (`errors-and-boundaries.md`)
- Separate Constructing a System from Using It
- Simple Design Rules (Emergence) (`foundations.md`)
