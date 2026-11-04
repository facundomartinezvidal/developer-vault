# Supple design

Chapter 10: making a model safe and pleasant to change.

## Contents

- [Supple Design](#supple-design)
- [Intention-Revealing Interfaces](#intention-revealing-interfaces)
- [Side-Effect-Free Functions](#side-effect-free-functions)
- [Assertions](#assertions)
- [Conceptual Contours](#conceptual-contours)
- [Standalone Classes](#standalone-classes)
- [Closure of Operations](#closure-of-operations)
- [Declarative Design](#declarative-design)

## Supple Design

> A supple design communicates its intent. The design makes it easy to anticipate the effect of running code—and therefore it easy to anticipate the consequences of changing it.

**Source:** *Domain-Driven Design*, Chapters 10 and 13.

### What it means in practice

Software is also for the developers who keep changing it. When a design is opaque, developers are afraid to touch it, so they duplicate code instead of reusing it, and every change makes it more rigid. A supple design does three things:
- It invites change by limiting **mental overload**, chiefly by cutting dependencies and side effects.
- It lets client developers combine elements without reading their internals.
- It is fine-grained only where the domain needs flexibility, and simple everywhere else.

It does not mean "add flexibility everywhere". Evans warns that layers of abstraction and indirection usually *reduce* suppleness. Suppleness comes from a deep model plus a set of techniques that reinforce each other:

| Purpose | Patterns |
|---|---|
| Make behavior obvious to client developers | Intention-Revealing Interfaces, Side-Effect-Free Functions, Assertions |
| Cut the design into the right pieces | Conceptual Contours, Standalone Classes, Closure of Operations |
| Go further | Declarative Design, composite Specifications (`building-blocks.md`) |

**Angles of attack.** You can't make a whole system supple at once:
- **Carve off subdomains.** Pick a specialized area, such as a mathematical or rule-heavy one, and make that part supple first.
- **Draw on established formalisms.** Where arithmetic, logic, graph theory or accounting fits part of the domain, adopt its rules wholesale. Evans's example is share math for loan payments: a `SharePie` value with add, subtract and prorate operations replaces tangled proportional-payment code.

### Example: proportional refunds

Before, refunding a partially used bundle meant copying proration loops into three services. After, an `Allocation` value object follows plain arithmetic: `allocation.prorate(Money total)`, `allocation.plus(other)` and `allocation.minus(refunded)` are all side-effect free and closed under `Allocation`. New features like split shipments and partial cancellations simply combine those operations, and nobody has to re-read the loop.

### Related

- Intention-Revealing Interfaces
- Side-Effect-Free Functions
- Assertions
- Conceptual Contours
- Standalone Classes
- Closure of Operations
- Declarative Design
- Specification (`building-blocks.md`)
- Refactoring Toward Deeper Insight (`modeling.md`) — supple design both enables and results from it.
- Breakthrough (`modeling.md`)
- Cohesive Mechanisms (`distillation.md`) — formalisms carved out as frameworks.
- Analysis Patterns (`modeling.md`)
- Core Domain (`distillation.md`)
- Evolving Order (Large-Scale Structure) (`large-scale-structure.md`)
- Model-Driven Design (`modeling.md`)

## Intention-Revealing Interfaces

> Name classes and operations to describe their effect and purpose, without reference to the means by which they do what they promise.

**Source:** *Domain-Driven Design*, Chapter 10 (term from Kent Beck).

### What it means in practice

If a developer has to read an implementation to use a component, encapsulation has failed. Worse, they may infer a purpose the original author never intended. Instead:
- Name for **effect and purpose** in the Ubiquitous Language (`modeling.md`), not for mechanism: `scheduleRetry`, not `insertIntoQueueTableWithDelay`.
- In domain interfaces, state **rules and relationships**, not how they're enforced; state **events and actions**, not how they're carried out.
- **Write the test first**, as the client would use it. That puts you in the client's head before you think about the implementation.
- Hide the tricky mechanism behind interfaces that speak in intentions.

Evans's example is a paint-mixing class whose `paint(Paint)` method becomes `mixIn(Paint)`. Making the intent visible exposed that the method was mixing pigments, which pointed to a missing concept.

### Example

```java
// Mechanism-revealing: the caller has to know how it works
subscription.setStatusAndRecalc(3, true);
cache.putWithTtl(key, value, 300);

// Intention-revealing
subscription.pauseUntil(resumeDate);
sessionStore.rememberFor(sessionId, user, Duration.ofMinutes(5));
```

```java
@Test void pausing_stops_billing_until_resume_date() {   // written first, from the client's view
    subscription.pauseUntil(may1);
    assertThat(subscription.nextChargeDate()).isEqualTo(may1);
}
```

### Related

- Supple Design
- Ubiquitous Language (`modeling.md`)
- Side-Effect-Free Functions — intention-revealing names make function composition safe to read.
- Cohesive Mechanisms (`distillation.md`) — mechanisms are exposed through intention-revealing interfaces.
- Domain Service (`building-blocks.md`), Factory (DDD) (`building-blocks.md`) — named for what they do for the client.
- Assertions
- Declarative Design

## Side-Effect-Free Functions

> Place as much of the logic of the program as possible into functions, operations that return results with no observable side effects. Strictly segregate commands (methods that result in modifications to observable state) into very simple operations that do not return domain information.

**Source:** *Domain-Driven Design*, Chapter 10.

### What it means in practice

When operations call other operations that change state, a developer must understand the whole call tree to predict what one call does, and combining calls becomes risky. So split operations in two:
- **Queries / functions** return a result and change nothing observable. They can be called any number of times, combined freely and tested trivially.
- **Commands** change state, are kept very simple, and don't return domain information.

Push complex logic into Value Objects (`building-blocks.md`) wherever a fitting concept exists. Immutable values make every operation on them a function. Then the Entity (`building-blocks.md`) only has to apply the *result* of a calculation, with one tiny command.

### Example: applying a coupon

```java
// Before: one method computes AND mutates; calling it twice double-discounts
public Money applyCoupon(Coupon c) {
    this.discount = this.discount.plus(c.amountFor(this.subtotal));
    this.total = this.subtotal.minus(this.discount);
    return this.total;
}

// After: the calculation is a function on a value; the entity just records the result
public record PriceBreakdown(Money subtotal, Money discount) {
    public PriceBreakdown with(Coupon c) { return new PriceBreakdown(subtotal, discount.plus(c.amountFor(subtotal))); }
    public Money total() { return subtotal.minus(discount); }
}

public class Cart {
    public PriceBreakdown previewWith(Coupon c) { return pricing.with(c); }   // query: safe to call from UI
    public void redeem(Coupon c) { this.pricing = previewWith(c); }           // command: one line
}
```

### Related

- Supple Design
- Value Object (`building-blocks.md`) — the natural home of functions.
- Intention-Revealing Interfaces
- Assertions — post-conditions describe what commands change.
- Closure of Operations
- Declarative Design
- Entity (`building-blocks.md`)

## Assertions

> State post-conditions of operations and invariants of classes and AGGREGATES. If ASSERTIONS cannot be coded directly in your programming language, write automated unit tests for them.

**Source:** *Domain-Driven Design*, Chapter 10.

### What it means in practice

Side-effect-free functions make queries safe, but commands still change state, and callers need to know *what* changes without reading the code. Assertions state it:
- **Post-conditions:** what is guaranteed after an operation.
- **Invariants:** what is always true of a class or an Aggregate (`building-blocks.md`).
- **Pre-conditions:** what the caller must ensure first.

Mainstream languages lack design-by-contract (Eiffel has it), so express assertions as **unit tests**, plus a note in docs or diagrams where that fits the team's process. Even more important, look for **models with coherent concepts**, where a developer can *infer* the right assertions without being told. Coherent concepts shorten the learning curve and make contradictory code less likely.

### Example: a wallet transfer

```java
// Post-condition: money is conserved; the source never goes below its overdraft limit
@Test void transfer_conserves_money() {
    Money before = source.balance().plus(target.balance());
    transfers.execute(source, target, usd(40));
    assertThat(source.balance().plus(target.balance())).isEqualTo(before);
}

// Aggregate invariant, checked at the root on every change
private void checkInvariants() {
    assert balance.isGreaterThanOrEqual(overdraftLimit.negate()) : "overdraft exceeded";
}
```

### Related

- Supple Design
- Side-Effect-Free Functions
- Aggregate (`building-blocks.md`) — invariants are defined per aggregate.
- Intention-Revealing Interfaces
- Making Implicit Concepts Explicit (`modeling.md`) — explicit constraints.

## Conceptual Contours

> Decompose design elements (operations, interfaces, classes, and AGGREGATES) into cohesive units, taking into consideration your intuition of the important divisions in the domain.

**Source:** *Domain-Driven Design*, Chapter 10.

### What it means in practice

Granularity can go wrong in either direction:
- **Too coarse:** monolithic classes and methods force duplication, because nothing can be reused in part.
- **Too fine:** a swarm of tiny pieces leaves the client to hold the meaning together, and concepts are lost.

The right cut follows the domain's own **conceptual contours**, the places where the domain naturally has seams. You rarely see them up front. Watch the **axes of change and stability** across successive refactorings: if every change keeps touching the same region, or keeps splitting the same class, that shows where the contour runs. Align the model with the consistent aspects of the domain, the ones that make it a coherent area of knowledge in the first place.

The payoff is that later changes fit. Evans's example: after an accrual-schedule refactoring along conceptual lines, an unanticipated new requirement for early payoff slotted in without a rewrite. The design wasn't built for that change, but it matched the domain, and the domain absorbed the change.

### Example: subscriptions split along real seams

```java
// Coarse: one class churns for every pricing, billing, or entitlement change
class Subscription { /* plan, price, discounts, invoices, retries, feature flags, seat counts */ }

// Along the contours the business actually reasons about
class Subscription   { Plan plan; BillingPeriod period; SubscriptionStatus status; }
class PriceSchedule  { Money priceFor(Plan plan, Seats seats, BillingPeriod p); }   // pricing changes here
class Entitlements   { boolean allows(Feature f); }                                  // packaging changes here
```

Pricing experiments, plan packaging and dunning rules come from three different teams and change at three different rates. After the split, each change lands in one place.

### Related

- Supple Design
- Aggregate (`building-blocks.md`), Modules (`building-blocks.md`) — boundaries that should follow contours.
- Standalone Classes
- Responsibility Layers (`large-scale-structure.md`)

## Standalone Classes

> Low coupling is fundamental to object design. When you can, go all the way. Eliminate all other concepts from the picture. Then the class will be completely self-contained and can be studied and understood alone.

**Source:** *Domain-Driven Design*, Chapter 10.

### What it means in practice

Every association, argument type and return type is a dependency, and each dependency adds a concept you must keep in your head. With one dependency you think about two classes; with three, the load snowballs. Modules (`building-blocks.md`) and Aggregates (`building-blocks.md`) limit the web. Standalone classes cut it.
- Refine until every remaining dependency is **fundamental to the concept's meaning**.
- In an important subset of the model, push the count to **zero**: a class understandable on its own, apart from language primitives and basic library types.
- **Implicit concepts count too.** Three integers that really mean "a color" are a hidden dependency, even though the compiler sees only `int`.
- Don't flatten everything into primitives to reach zero, which just hides the concepts. Factor the most intricate computations into standalone Value Objects (`building-blocks.md`) and let more connected classes use them.

### Example: tax calculation pulled out of the order

```java
// Coupled: to understand tax you must understand Order, Customer, Address, Product, Catalog
class Order { Money tax() { ... customer.address().region() ... line.product().taxCategory() ... } }

// Standalone: needs only values, testable and readable by itself
public record TaxRule(TaxCategory category, Region region, Percentage rate) {
    public Money taxOn(Money amount) { return amount.times(rate); }
}
```

`Order` still depends on `TaxRule`, but `TaxRule` depends on nothing in the domain. When the tax team asks "what's our rate logic?", one file answers.

### Related

- Supple Design
- Associations in the Domain Model (`building-blocks.md`) — eliminate associations that aren't essential.
- Value Object (`building-blocks.md`)
- Closure of Operations — a closed operation adds no new dependency.
- Conceptual Contours
- Aggregate (`building-blocks.md`)
- Modules (`building-blocks.md`)

## Closure of Operations

> Where it fits, define an operation whose return type is the same as the type of its argument(s).

**Source:** *Domain-Driven Design*, Chapter 10.

### What it means in practice

The term comes from math: adding two integers gives an integer, so integers are *closed* under addition. A closed operation offers a high-level interface **without introducing any new concept**. Results feed straight into the next operation, and chains of them read like arithmetic.
- If the implementer's own state takes part in the computation, it counts as an argument, so the return type should match the implementer.
- This pattern fits **Value Objects (`building-blocks.md`)** most of all. An Entity (`building-blocks.md`)'s life cycle matters, so you can't conjure up a new one to answer a question.
- Operations can be *partially* closed: an argument of a basic library type, like a predicate, adds no real mental load.

### Example

```java
Money total = itemsTotal.plus(shipping).minus(discount);           // Money × Money → Money
DateRange active = contract.term().intersect(subscription.period()); // DateRange × DateRange → DateRange
Specification<Order> risky = highValue.and(newCustomer.or(foreignCard)); // spec × spec → spec
List<Order> recentPaid = orders.filter(Order::isPaid).filter(placedAfter(cutoff)); // collection → collection
```

None of these lines make the reader learn an extra type to know what comes back.

### Related

- Supple Design
- Value Object (`building-blocks.md`)
- Side-Effect-Free Functions — closed operations on values are side-effect free by nature.
- Specification (`building-blocks.md`) — `and`/`or`/`not` are closed.
- Standalone Classes — closure keeps the dependency count down.
- Declarative Design
- Entity (`building-blocks.md`)

## Declarative Design

> Generating a running program from a declaration of model properties is a kind of Holy Grail of MODEL-DRIVEN DESIGN, but it does have its pitfalls in practice.

**Source:** *Domain-Driven Design*, Chapter 10.

### What it means in practice

Hand-written procedures can never fully guarantee what a design promises: some code can always add an unexpected side effect. Declarative design writes part of the program as an **executable specification**, a precise description of properties that actually drives the software. It can be implemented through reflection, code generation, rule engines or a **domain-specific language**. Evans is skeptical of the heavyweight forms because of two recurring traps:
- A declaration language that can't express everything needed, inside a framework that makes going beyond it very hard.
- Code generation that merges generated and hand-written code, so regenerating destroys work and the iterative cycle breaks.

The result is often a *dumbed-down* model, as teams cut features to fit the tool. Rule engines also blur declarative and imperative rules in subtle ways.

The practical payoff is a **declarative style** inside ordinary OO code. Once a design has intention-revealing interfaces, side-effect-free functions and closed operations, its elements combine into readable sentences. Composite Specifications (`building-blocks.md`) are the book's main example.

### Example: shipping eligibility as declarations

```java
// Imperative: the rule is buried in control flow
if (order.weight().kg() < 30 && !order.hasHazmat() && (order.country().isEu() || order.total().gt(usd(200)))) ...

// Declarative: the rule is data built from small, named specifications
Specification<Order> expressEligible =
        under(kg(30))
        .and(containsHazmat().not())
        .and(shipsWithinEu().or(totalOver(usd(200))));

shippingOptions.offerIf(expressEligible, Express.INSTANCE);
```

The logistics team can read `expressEligible` aloud, and each piece is tested once.

### Related

- Supple Design
- Specification (`building-blocks.md`)
- Model-Driven Design (`modeling.md`)
- Closure of Operations
- Cohesive Mechanisms (`distillation.md`) — the core stays declarative by delegating the "how" to a mechanism.
- Intention-Revealing Interfaces
- Side-Effect-Free Functions
