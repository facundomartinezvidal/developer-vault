# What a pattern is and the principles behind them

What a pattern is, how good ones go bad, and the object-oriented principles patterns are built on.

## Contents

- [What Is a Design Pattern](#what-is-a-design-pattern)
- [Anti-Patterns](#anti-patterns)
- [Encapsulate What Varies](#encapsulate-what-varies)
- [Favor Composition Over Inheritance](#favor-composition-over-inheritance)
- [Program To An Interface, Not An Implementation](#program-to-an-interface-not-an-implementation)
- [Strive for Loosely Coupled Designs](#strive-for-loosely-coupled-designs)
- [The Hollywood Principle](#the-hollywood-principle)
- [Principle of Least Knowledge (Law of Demeter)](#principle-of-least-knowledge-law-of-demeter)
- [Inheritance Tax](#inheritance-tax)

## What Is a Design Pattern


**Source:** *Head First Design Patterns*, Chapter 13 — "Better Living with Patterns".

### What it means in practice

The three parts: the **context** is a *recurring* situation; the **problem** is a goal plus the constraints (forces) acting on it in that context; the **solution** is a general design anyone can apply that resolves the goal and constraints. "Recurring" is what separates a pattern from a one-off hack (breaking your car window when you've locked the keys inside solves a problem in a context, but it's not a pattern). A real pattern description also has a **name** — the name is what builds a team's shared vocabulary, which the book calls one of the biggest payoffs of patterns.

**Categories** (GoF's scheme, by purpose — every pattern in one bucket, even if some feel like they fit two):

| Category | Concerned with | Patterns |
|---|---|---|
| **Creational** | object instantiation; decoupling clients from what they instantiate | Singleton (`creational.md`), Abstract Factory (`creational.md`), Factory Method (`creational.md`), Builder (`creational.md`), Prototype (`creational.md`) |
| **Structural** | composing classes/objects into larger structures | Adapter (`structural.md`), Decorator (`structural.md`), Facade (`structural.md`), Composite (`structural.md`), Proxy (`structural.md`), Bridge (`structural.md`), Flyweight (`structural.md`) |
| **Behavioral** | how objects interact and distribute responsibility | Strategy (`behavioral.md`), Observer (`behavioral.md`), Command (`behavioral.md`), Template Method (`behavioral.md`), Iterator (`behavioral.md`), State (`behavioral.md`), Chain of Responsibility (`behavioral.md`), Interpreter (`behavioral.md`), Mediator (`behavioral.md`), Memento (`behavioral.md`), Visitor (`behavioral.md`) |

A second scheme splits by whether a pattern deals with **class** relationships (fixed at compile time via inheritance: Template Method, Factory Method, class Adapter, Interpreter) or **object** relationships (composition at runtime: everything else). Categories are just a thinking aid — use them when they help.

**Thinking in patterns** (the chapter's practical advice):

- **Keep it simple.** The goal is the simplest design that works, not "which pattern applies here". Patterns aren't a magic bullet; each one adds complexity and has consequences.
- **Introduce a pattern when you're sure it solves a real problem** — or when you're confident an aspect of the system *will* vary (practical change, not hypothetical change).
- **Refactoring time is patterns time.** Conditionals everywhere may want State (`behavioral.md`); scattered `new` may want a factory.
- **Take out what you don't need.** Remove a pattern when its flexibility is no longer used.
- **Let patterns emerge** from the design principles instead of designing *from* patterns.

The "three minds": the Beginner uses patterns everywhere ("I need a pattern for Hello World"), the Intermediate starts to see where they don't fit, the Zen mind applies them only where they fit naturally — and adapts them.

### Example: same problem, with and without a pattern

A notification service sends email only. Wrapping it in Strategy + Abstract Factory "in case we add SMS" is the Beginner move. The Zen move: keep a single `EmailNotifier` behind a `Notifier` interface (cheap, and just programming to an interface). When SMS actually arrives and the second implementation appears, the Strategy (`behavioral.md`) shape is already there — it emerged instead of being imposed.

### Related

- Anti-Patterns
- Model-View-Controller (Compound Pattern) (`compound.md`) — compound patterns: recurring combinations of patterns.
- Encapsulate What Varies — most patterns are this principle applied to one specific axis of change.

## Anti-Patterns


**Source:** *Head First Design Patterns*, Chapter 13 — "Better Living with Patterns".

### What it means in practice

An anti-pattern documents a *recurring* bad solution so others can recognize it before they commit to it. It always looks good at first — that's why it recurs. A useful anti-pattern description has the same parts as a pattern (name, problem, context, forces) plus:

1. **Why the bad solution is attractive** — the seductive part.
2. **Why it's bad in the long run** — where you'll get into trouble.
3. **A refactored solution** — which good patterns or practices to use instead.

There are development, OO, organizational, and domain-specific anti-patterns.

The book's example, **Golden Hammer**: a team that knows one technology well applies it to every problem, even where it clearly doesn't fit. Attractive because it's familiar, easy to estimate, and unfamiliar tech feels risky. Refactored solution: broaden the team's knowledge (training, study groups, exposure to alternatives).

### Example: Golden Hammer in a modern stack

A team fluent in their relational database implements a job queue as a `jobs` table polled every second, a pub/sub system as triggers, full-text search with `LIKE '%term%'`, and a cache as another table. Each choice was quick and familiar; together they produce lock contention, slow searches, and a database that is now the bottleneck for everything. Refactored solution: keep the database for what it's good at, and use a real queue, a search index, and an in-memory cache behind interfaces — after the team has actually evaluated them.

### Related

- What Is a Design Pattern
- Singleton Pattern (`creational.md`) — overused Singletons are commonly cited as an anti-pattern (global state in disguise).

## Encapsulate What Varies



**Source:** *Head First Design Patterns*, Chapter 1.

### What it means in practice

Whatever part of a class changes for reasons unrelated to the rest of it — a new format, a new provider, a new rule — pull it out into its own class (or family of classes) behind an interface. The class that used to contain that logic now just delegates to it. Change one variant later and nothing else has to move.

### Example: report export formats

```java
// Before: the varying part (how to build each format) is mixed into one class
public class ReportExporter {
    public void export(Report report, String format) {
        if (format.equals("pdf")) {
            // build a PDF...
        } else if (format.equals("csv")) {
            // build a CSV...
        } else if (format.equals("xlsx")) {
            // build an Excel file...
        }
    }
}
```

```java
// After: the varying part is pulled into its own family of classes
public interface ExportFormat {
    void export(Report report);
}

public class PdfExportFormat implements ExportFormat {
    public void export(Report report) { /* build a PDF */ }
}

public class CsvExportFormat implements ExportFormat {
    public void export(Report report) { /* build a CSV */ }
}

public class ReportExporter {
    private final ExportFormat format;

    public ReportExporter(ExportFormat format) {
        this.format = format;
    }

    public void export(Report report) {
        format.export(report);
    }
}
```

Adding XLSX support later means adding one new `ExportFormat` implementation — `ReportExporter` never changes again, and nothing else in the codebase has to know a new format exists.

### Where it applies

- Strategy Pattern (`behavioral.md`) — the payment logic that varies per method gets pulled out of `Checkout` into `PaymentStrategy` implementations; `Checkout` itself never changes when a new payment method is added.

### Related

- Favor Composition Over Inheritance
- Program To An Interface
- Observer Pattern (`behavioral.md`) — what varies is the number and kind of observers.
- Factory Method Pattern (`creational.md`) — the principle applied to object creation.
- Iterator Pattern (`behavioral.md`) — what varies is how a collection is stored.
- State Pattern (`behavioral.md`) — what varies is behavior per state.
- What Is a Design Pattern — most patterns are this principle applied to one axis of change.
- Bridge Pattern (`structural.md`)
- Builder Pattern (`creational.md`)
- Command Pattern (`behavioral.md`)
- Memento Pattern (`behavioral.md`)
- Principle of Least Knowledge (Law of Demeter)
- Strategy Pattern (`behavioral.md`)

## Favor Composition Over Inheritance



**Source:** *Head First Design Patterns*, Chapter 1.

### What it means in practice

Give a class a *reference to* the behavior/object it needs (HAS-A) instead of *inheriting* that behavior from a superclass (IS-A). Composition lets you mix independent variations freely and swap them at runtime; inheritance locks a combination in at compile time and multiplies subclasses every time a new axis of variation shows up.

### Example: avoiding subclass explosion

```java
// Inheritance: one subclass per combination — and it multiplies with every new engine or transmission
class GasManualCar extends Car { }
class GasAutomaticCar extends Car { }
class ElectricManualCar extends Car { }
class ElectricAutomaticCar extends Car { }
// add a hybrid engine or a CVT transmission and this doubles again
```

```java
// Composition: mix and match at runtime, no subclass explosion
public class Car {
    private final Engine engine;
    private final Transmission transmission;

    public Car(Engine engine, Transmission transmission) {
        this.engine = engine;
        this.transmission = transmission;
    }
}

public interface Engine {
    void start();
}

public class GasEngine implements Engine {
    public void start() { /* ... */ }
}

public class ElectricEngine implements Engine {
    public void start() { /* ... */ }
}

public interface Transmission {
    void shift();
}
```

```java
Car car = new Car(new ElectricEngine(), new ManualTransmission());
```

Any engine/transmission combination — zero new subclasses, even as more variants get added on either axis.

### Where it applies

- Strategy Pattern (`behavioral.md`) — `Checkout` HAS-A `PaymentStrategy` instead of inheriting payment logic; the strategy can be swapped per order, at runtime.
- Adapter Pattern (`structural.md`) — `StripeAdapter` composes a `StripeClient` rather than subclassing it, which is also the only option Java allows (no multiple inheritance for a class adapter).

### Related

- Encapsulate What Varies
- Program To An Interface
- Decorator Pattern (`structural.md`) — extends behavior by wrapping instead of subclassing.
- Observer Pattern (`behavioral.md`) — observers are composed with subjects at runtime.
- Bridge Pattern (`structural.md`) — composition across two independent hierarchies.
- Template Method Pattern (`behavioral.md`) — the inheritance-based alternative, and its trade-offs.
- Abstract Factory Pattern (`creational.md`)
- Adapter Pattern (`structural.md`)
- Strategy Pattern (`behavioral.md`)
- Strive for Loosely Coupled Designs
- Inheritance Tax

## Program To An Interface, Not An Implementation



**Source:** *Head First Design Patterns*, Chapter 1.

### What it means in practice

Declare variables, parameters, and return types using the interface/abstract type, never the concrete class — even when only one implementation exists today. The concrete type gets decided at the point of construction (or injected from outside), not baked into every place that uses it.

### Example: the everyday Java version

```java
// Programming to an implementation
ArrayList<String> names = new ArrayList<>();

// Programming to an interface — same behavior, but callers only ever see List
List<String> names = new ArrayList<>();
```

### Example: where it actually matters — swappable dependencies

```java
public interface UserRepository {
    User findById(String id);
}

public class PostgresUserRepository implements UserRepository {
    public User findById(String id) { /* real DB query */ }
}

public class InMemoryUserRepository implements UserRepository {
    public User findById(String id) { /* fake data, used in tests */ }
}

public class UserService {
    private final UserRepository repository; // depends on the interface, not a specific DB

    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}
```

`UserService` runs against Postgres in production and an in-memory fake in tests, without a single line of `UserService` changing. This is the same reason DI containers/constructor injection exist — the practice is this principle applied systematically.

### Where it applies

- Strategy Pattern (`behavioral.md`) — `Checkout` holds a `PaymentStrategy` field, never a concrete `CreditCardPayment`/`PayPalPayment`.
- Adapter Pattern (`structural.md`) — the rest of the app depends only on `PaymentGateway`; `StripeClient` (the concrete vendor SDK) is only ever referenced inside `StripeAdapter`.

### Related

- Encapsulate What Varies
- Favor Composition Over Inheritance
- Strive for Loosely Coupled Designs — interfaces are how loosely coupled objects know each other.
- Observer Pattern (`behavioral.md`)
- Proxy Pattern (`structural.md`) — a proxy is substitutable only because clients depend on the interface.
- Abstract Factory Pattern (`creational.md`)
- Adapter Pattern (`structural.md`)
- Composite Pattern (`structural.md`)
- Decorator Pattern (`structural.md`)
- Iterator Pattern (`behavioral.md`)
- Prototype Pattern (`creational.md`)
- Strategy Pattern (`behavioral.md`)
- What Is a Design Pattern
- Inheritance Tax

## Strive for Loosely Coupled Designs


**Source:** *Head First Design Patterns*, Chapter 2.

### What it means in practice

Two objects are loosely coupled when they can work together while knowing almost nothing about each other — ideally only that the other implements some interface. The less one object assumes about another (its concrete class, its internals, when it exists), the more freely either side can change, be replaced at runtime, or be reused elsewhere. In practice: depend on an interface, let the dependency be supplied from outside, and keep the contract between the two as small as possible.

### Example: order events and their side effects

```java
// Tightly coupled: OrderService knows every concrete consumer
public class OrderService {
    private final EmailService email = new EmailService();
    private final AnalyticsClient analytics = new AnalyticsClient();
    private final InventoryService inventory = new InventoryService();

    public void place(Order order) {
        save(order);
        email.sendConfirmation(order);
        analytics.track("order_placed", order.total());
        inventory.reserve(order.items());
    }
}
```

```java
// Loosely coupled: OrderService only knows "something that cares about placed orders"
public interface OrderPlacedListener { void onOrderPlaced(Order order); }

public class OrderService {
    private final List<OrderPlacedListener> listeners = new ArrayList<>();
    public void subscribe(OrderPlacedListener l) { listeners.add(l); }

    public void place(Order order) {
        save(order);
        listeners.forEach(l -> l.onOrderPlaced(order));
    }
}
```

Adding a loyalty-points consumer is a new `OrderPlacedListener`; `OrderService` never changes, and each listener can be tested and reused on its own.

### Where it applies

- Observer Pattern (`behavioral.md`) — the chapter's motivating case: `WeatherData` only knows its displays implement `Observer`; in the example above, `OrderService` is the subject.
- Mediator Pattern (`behavioral.md`) — checkout form widgets stop knowing about each other entirely.
- Facade Pattern (`structural.md`) — clients couple to one `CheckoutFacade` instead of the whole subsystem.
- Command Pattern (`behavioral.md`) — the invoker never knows the receiver.

### Related

- Program To An Interface, Not An Implementation — the mechanism: the only thing one side knows about the other is an interface.
- Favor Composition Over Inheritance
- Principle of Least Knowledge (Law of Demeter) — the same goal, applied to how many objects any one object talks to.
- Observer Pattern (`behavioral.md`)
- Chain of Responsibility Pattern (`behavioral.md`)
- Command Pattern (`behavioral.md`)
- Facade Pattern (`structural.md`)
- Mediator Pattern (`behavioral.md`)

## The Hollywood Principle


**Source:** *Head First Design Patterns*, Chapter 8.

### What it means in practice

Low-level components may *hook into* a system, but the high-level component decides **when** and **how** they're used. Low-level code never calls up into the high-level code that drives it. This prevents "dependency rot" — the tangle where high-level depends on low-level depends on high-level depends on sideways components, until nobody can tell how the system is structured. Frameworks are the everyday example: you write handlers, the framework calls them.

It's related to DIP but not the same: DIP is about *what you depend on* (abstractions, not concretions); Hollywood is about *who calls whom* — a technique for letting low-level code participate in a computation without the two layers depending on each other in both directions.

### Example: a scheduled job runner

```java
// High-level: owns the flow and calls the hooks
public abstract class ScheduledJob {
    public final void run() {
        if (!shouldRun()) return;            // hook with default
        var input = fetch();
        var result = process(input);
        publish(result);
    }
    protected boolean shouldRun() { return true; }
    protected abstract List<Row> fetch();
    protected abstract Report process(List<Row> rows);
    protected abstract void publish(Report report);
}

// Low-level: plugs in, never calls run() or another job's internals
public class NightlySalesJob extends ScheduledJob { ... }
```

`NightlySalesJob` never decides when it runs or in what order its steps happen; the runner (and the scheduler above it) calls it.

### Where it applies

- Template Method Pattern (`behavioral.md`) — the chapter's case: the abstract class (`DataImporter` in its example) calls the subclass steps.
- Factory Method Pattern (`creational.md`) — the creator calls the subclass's factory method.
- Observer Pattern (`behavioral.md`) — observers register, the subject calls them.
- Strategy Pattern (`behavioral.md`) — the context calls whichever strategy it holds.

### Related

- Template Method Pattern (`behavioral.md`)
- Factory Method Pattern (`creational.md`)
- Observer Pattern (`behavioral.md`)
- Strategy Pattern (`behavioral.md`)

## Principle of Least Knowledge (Law of Demeter)


**Source:** *Head First Design Patterns*, Chapter 7; *Clean Code*, Chapter 6 (and heuristic G36, "Avoid Transitive Navigation"); *The Pragmatic Programmer*, Topic 28.

### How the other books refine it

- **Clean Code** calls chained getters **train wrecks**, and limits the law to *objects*. Chaining through a plain data structure (`config.db.host`) doesn't violate it, because a data structure is supposed to expose its fields (data object anti symmetry). Hybrids, which are half object and half data structure, make it unclear which rule applies.
- **The Pragmatic Programmer** simplifies it to "**Don't Chain Method Calls**" (Tip 46), with an exception for language-level pipelines that won't change. The fix it suggests is tell dont ask.

### What it means in practice

Limit how many classes any one object interacts with, and especially *how it reaches them*. Inside a method, only call methods on:

1. the object itself (`this`),
2. objects passed in as parameters,
3. objects the method creates,
4. the object's own components (instance variables).

Don't call methods on objects *returned* by other calls — `a.getB().getC().doSomething()` makes your class depend on B's and C's structure too, so a change three classes away breaks you. The fix is usually to ask the immediate friend to do the work for you. The cost: more small "wrapper" methods on the intermediate classes, which can add complexity, so it's a guideline to weigh, not an absolute rule.

### Example: shipping cost from a customer's address

```java
// Before: ShippingCalculator knows Customer → Address → Region → zone
public Money cost(Customer customer, Cart cart) {
    String zone = customer.getAddress().getRegion().getShippingZone();
    return rates.lookup(zone, cart.weight());
}
```

```java
// After: talk only to the friend you were given
public Money cost(Customer customer, Cart cart) {
    return rates.lookup(customer.shippingZone(), cart.weight());
}

// Customer hides how it knows its own zone
public String shippingZone() { return address.shippingZone(); }
```

If addresses later get geocoded zones instead of region-based ones, only `Address` changes.

### Where it applies

- Facade Pattern (`structural.md`) — the chapter's motivating case: the client of `CheckoutFacade` has one friend instead of inventory, payments, shipping, and email.
- Mediator Pattern (`behavioral.md`) — each colleague only talks to the mediator.

### Related

- Strive for Loosely Coupled Designs
- Encapsulate What Varies
- Facade Pattern (`structural.md`)
- Mediator Pattern (`behavioral.md`)

## Inheritance Tax


**Source:** *The Pragmatic Programmer*, Topic 31 (Tips 51–54).

### What it means in practice

People use inheritance for two different reasons. **Code reuse** ("I'll subclass it to get its methods") couples you to the parent's implementation, its fields, and every method it will ever add. **Type modeling** ("a Car is-a Vehicle") rarely matches reality, and inheritance hierarchies get too rigid to change. Either way you pay a "tax": a change to the base class can break a subclass far away (the fragile base class problem).

Three alternatives, each covering one use:
- **Interfaces and protocols** (Tip 52) express polymorphism without inheriting implementation.
- **Delegation** (Tip 53, *has-a trumps is-a*) reuses behavior by holding a service and calling it.
- **Mixins and traits** (Tip 54) share a piece of functionality without a class hierarchy.

### Example

```java
// Tax: reusing persistence by inheritance couples every model to the ORM's base class
class Invoice extends ActiveRecordBase { ... }        // now Invoice exposes save(), delete(), where(...) to everyone

// Interface + delegation
interface InvoiceRepository { void save(Invoice i); Optional<Invoice> byId(InvoiceId id); }
class InvoiceService {
    private final InvoiceRepository invoices;           // has-a, not is-a
    void issue(Invoice i) { i.markIssued(); invoices.save(i); }
}
```

### Where it applies

- Favor Composition Over Inheritance — *Head First*'s statement of the same rule.
- Program To An Interface, Not An Implementation — Tip 52 in other words.
- Refused Bequest — the smell when a subclass doesn't want what it inherited. The fix is Replace Subclass with Delegate.
- liskov substitution principle — the condition inheritance has to meet to be safe.

### Related

- Strategy Pattern (`behavioral.md`) and Decorator Pattern (`structural.md`) — delegation-based alternatives to subclassing.
