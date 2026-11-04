# Testable code and automation

How to separate what is hard to test, how to keep tests from being fragile, and what to automate.

## Contents

- [The Test Boundary](#the-test-boundary)
- [Humble Object](#humble-object)
- [Separate Constructing a System from Using It](#separate-constructing-a-system-from-using-it)
- [Pragmatic Starter Kit](#pragmatic-starter-kit)

## The Test Boundary

> Tests are not outside the system; rather, they are parts of the system that must be well designed if they are to provide the desired benefits of stability and regression.

**Source:** *Clean Architecture*, Chapter 28.

### What it means in practice

Architecturally, every kind of test (TDD unit tests, Cucumber, FitNesse, ...) is the same thing: the **outermost circle**. Tests are concrete, depend inward on the code under test, nothing depends on them, and they're always deployed independently. Treating them as "outside the design" is catastrophic: tests coupled tightly to the system break by the hundreds on trivial changes (the **Fragile Tests Problem**), and then the team starts refusing changes — tests make the system *rigid*.

The first rule of design applies: **don't depend on volatile things**. GUIs are volatile, so tests that drive the GUI to check business rules are fragile by construction. Instead:

- **Testing API.** A dedicated API — a superset of the interactors and interface adapters the UI uses — with "superpowers": bypass security, skip expensive resources like the database, force the system into specific states. Keep it (and its dangerous parts) in a separately deployable component so it never ships to production.
- **Avoid structural coupling.** A test class per production class and a test method per production method locks tests to the code's structure. The testing API hides that structure, so production code can be refactored (and grow more abstract and general) while tests grow more concrete and specific — independently.

### Example: testing promotions without the storefront

```java
// Fragile: drives the browser to test a pricing rule
loginAs("vip@example.com"); clickCategory("Shoes"); addToCart("Runner X"); applyCoupon("VIP20");
assertThat(text("#total")).isEqualTo("$96.00");

// Through a testing API: same rule, no UI, no DB, no knowledge of internal classes
var shop = TestShop.inMemory();
var vip  = shop.givenCustomer().withTier(VIP).create();
shop.givenProduct("runner-x").pricedAt("120.00");
var cart = shop.cartFor(vip).add("runner-x").applyCoupon("VIP20");
assertThat(cart.total()).isEqualTo(Money.of("96.00"));
```

A checkout redesign breaks zero tests in the second style, and the pricing classes can be restructured freely as long as `TestShop` still works.

### Related

- Humble Object — the pattern that makes the core testable without the UI or DB.
- Pragmatic Starter Kit
- Clean Tests (F.I.R.S.T.) (`writing-tests.md`)
- Test to Code (`writing-tests.md`)
- The Three Laws of TDD (`writing-tests.md`)

## Humble Object

> At each architectural boundary, we are likely to find the Humble Object pattern lurking somewhere nearby.

**Source:** *Clean Architecture*, Chapter 23 (pattern originally from Meszaros, *xUnit Test Patterns*).

### What it means in practice

Split a behavior that's hard to test into two parts: a **humble** object that keeps only the hard-to-test bit, stripped down to almost nothing, and a testable object that holds everything else. Because that split usually falls exactly where an architectural boundary runs, the pattern doubles as a way to *find* and *protect* boundaries — and it's everywhere in the Clean Architecture:

| Boundary | Testable side | Humble side |
|---|---|---|
| UI | **Presenter** — formats dates, money, labels, enabled/disabled and color flags into a **View Model** of strings, booleans, enums | **View** — copies the View Model onto the screen, no logic |
| Database | **Interactor** — app rules; testable because gateways can be stubbed | **Gateway implementation** — just runs the SQL for methods like `lastNamesOfUsersLoggedInAfter(date)` |
| ORM | — | **Data mapper** (ORM) — lives in the database layer, between gateway interfaces and the DB |
| Services | Application code passes plain data structures | **Service listeners / senders** — translate to/from the wire format |

Martin's aside on ORMs: there's no such thing as an "object-relational mapper", because objects aren't data structures (from the outside they're just operations). ORMs are *data mappers* — they load tables into data structures — and they belong in the outer database layer.

### Example: an invoice screen

```java
// Testable: every decision about what appears on screen
public class InvoicePresenter implements ShowInvoiceOutputBoundary {
    private InvoiceViewModel vm;
    public void present(ShowInvoiceResponse r) {
        vm = new InvoiceViewModel(
            "Invoice #" + r.number(),
            DateTimeFormatter.ofPattern("MMM d, yyyy").format(r.dueDate()),
            r.balance().format(Locale.US),               // "$1,240.00"
            r.balance().isNegative(),                     // showBalanceInRed
            !r.isPaid()                                   // payButtonEnabled
        );
    }
}

// Humble: no branching, no formatting — just binding
public class InvoiceView {
    void render(InvoiceViewModel vm) {
        title.setText(vm.title()); due.setText(vm.dueDate());
        balance.setText(vm.balance()); balance.setRed(vm.showBalanceInRed());
        payButton.setEnabled(vm.payButtonEnabled());
    }
}
```

The presenter gets fast unit tests (`present(overdueInvoice)` → assert the strings and flags); the view is too dumb to need them.

### Related

- The Test Boundary — testability as an architectural force.
- Clean Tests (F.I.R.S.T.) (`writing-tests.md`)
- Test to Code (`writing-tests.md`)

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
- dependency inversion principle — the factory interface belongs to the application, and its implementation belongs to `main`.
- abstract factory pattern and factory method pattern — the factories this chapter talks about.
- proxy pattern and decorator pattern — how cross-cutting concerns get wrapped around plain objects.

### Related

- Test to Code (`writing-tests.md`)

## Pragmatic Starter Kit

> Test Early, Test Often, Test Automatically. — Tip 90 &nbsp;·&nbsp; Don't Use Manual Procedures. — Tip 95

**Source:** *The Pragmatic Programmer*, Topic 51 (Tips 89–95).

### What it means in practice

Every project needs three basics before anything else:

1. **Version control** drives builds, tests and releases (Tip 89). A push triggers everything, and a tag deploys.
2. **Ruthless, continuous testing:**
   - Test early, often, and automatically.
   - "Coding ain't done 'til all the tests run" (Tip 91).
   - Test at every level: unit, integration, validation and verification, performance and stress, usability.
   - **Use saboteurs to test your testing** (Tip 92). Deliberately introduce bugs (mutation testing) to make sure the tests notice.
   - **Test state coverage, not code coverage** (Tip 93).
   - **Find bugs once** (Tip 94). Every bug a human finds becomes an automated test, so it can't come back.
3. **Full automation.** Builds, deploys, database migrations and releases are scripts, never a wiki page of manual steps (Tip 95). Manual procedures don't get repeated the same way twice.

### Example

```yaml
# .github/workflows/ci.yml — the starter kit in one file
on: [push, pull_request]
jobs:
  build:
    steps:
      - run: ./gradlew spotlessCheck test integrationTest   # formatting + all tests, every push
      - run: ./gradlew pitest                                # saboteurs: mutation testing
      - if: startsWith(github.ref, 'refs/tags/v')
        run: ./deploy.sh production                          # no manual release steps
```

### Related

- Clean Tests (F.I.R.S.T.) (`writing-tests.md`) and The Three Laws of TDD (`writing-tests.md`)
- Test to Code (`writing-tests.md`)
- Property-Based Testing (`writing-tests.md`)
- The Test Boundary
