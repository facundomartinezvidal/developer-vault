# Coupling and decoupling techniques

Ways to keep parts of a system from knowing too much about each other.

## Contents

- [Decoupling](#decoupling)
- [Strive for Loosely Coupled Designs](#strive-for-loosely-coupled-designs)
- [Encapsulate What Varies](#encapsulate-what-varies)
- [Program To An Interface, Not An Implementation](#program-to-an-interface-not-an-implementation)
- [Favor Composition Over Inheritance](#favor-composition-over-inheritance)
- [The Hollywood Principle](#the-hollywood-principle)
- [Principle of Least Knowledge (Law of Demeter)](#principle-of-least-knowledge-law-of-demeter)
- [Tell, Don't Ask](#tell-dont-ask)
- [Event-Driven Programming](#event-driven-programming)
- [Transforming Programming](#transforming-programming)
- [Inheritance Tax](#inheritance-tax)
- [Externalize Configuration](#externalize-configuration)

## Decoupling

> Decoupled Code Is Easier to Change. — Tip 44

**Source:** *The Pragmatic Programmer*, Topic 28 (Tips 44–48).

### What it means in practice

Coupling is the enemy of change: when two things are coupled, changing one means changing the other. Hunt & Thomas list the symptoms: wacky dependencies between unrelated modules, simple changes rippling through the system, developers afraid to touch code, meetings where everyone has to attend because nobody knows what a change will affect.

The three forms of coupling the topic goes after:

1. **Train wrecks** (`customer.orders().find(id).totals().grandTotal()`). Each dot couples you to another class's internals. Fix it with Tell, Don't Ask and **don't chain method calls** (Tip 46), which is a simplified Law of Demeter. Chaining *language-level* things like stream pipelines is fine.
2. **Globalization.** Global data couples every module that touches it, including singletons and external resources. **Avoid global data** (Tip 47). **If it's important enough to be global, wrap it in an API** (Tip 48).
3. **Inheritance.** It's a form of coupling too. See Inheritance Tax.

### Example

```java
// Train wreck + global
Money discount = Config.INSTANCE.getPromotions().forCustomer(order.getCustomer().getTier()).getRate().times(order.getTotal());

// Decoupled: tell the order, inject what it needs
Money discount = order.discountUnder(promotionPolicy);   // PromotionPolicy passed in, Order knows its own tier and total
```

### Where it applies

- Strive for Loosely Coupled Designs — *Head First*'s statement of the goal.
- Orthogonality (`modularity.md`) — decoupling is how you get orthogonal components.
- Message Chains and Global Data — Fowler's smells for train wrecks and globalization.

### Related

- ETC — Easier to Change (`complexity.md`)
- Tell, Don't Ask
- Inheritance Tax
- Event-Driven Programming — Topic 29 follows on: reacting to events is another way to decouple.
- Information Hiding (and Leakage) (`modularity.md`) — Ousterhout's account of what dependencies cost.
- Software Complexity (`complexity.md`) — dependencies are one of the two causes of complexity.
- Actors and Processes (`concurrency.md`)
- Blackboards (`concurrency.md`)
- Breaking Temporal Coupling (`concurrency.md`)
- Different Layer, Different Abstraction (`modularity.md`)
- Externalize Configuration
- Finish What You Start (Balancing Resources) (`robustness-and-testability.md`)
- Transforming Programming
- Test to Code (`robustness-and-testability.md`)

## Strive for Loosely Coupled Designs

> Strive for loosely coupled designs between objects that interact.

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

- Observer Pattern — the chapter's motivating case: `WeatherData` only knows its displays implement `Observer`; in the example above, `OrderService` is the subject.
- Mediator Pattern — checkout form widgets stop knowing about each other entirely.
- Facade Pattern — clients couple to one `CheckoutFacade` instead of the whole subsystem.
- Command Pattern — the invoker never knows the receiver.

### Related

- Program To An Interface, Not An Implementation — the mechanism: the only thing one side knows about the other is an interface.
- Favor Composition Over Inheritance
- Principle of Least Knowledge (Law of Demeter) — the same goal, applied to how many objects any one object talks to.
- Decoupling
- Orthogonality (`modularity.md`)

## Encapsulate What Varies

> Identify the aspects of your application that vary and separate them from what stays the same.

> Take what varies and "encapsulate" it so it won't affect the rest of your code. The result? Fewer unintended consequences from code changes and more flexibility in your systems!

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

- Strategy Pattern — the payment logic that varies per method gets pulled out of `Checkout` into `PaymentStrategy` implementations; `Checkout` itself never changes when a new payment method is added.

### Related

- Favor Composition Over Inheritance
- Program To An Interface
- Principle of Least Knowledge (Law of Demeter)
- ETC — Easier to Change (`complexity.md`)
- Information Hiding (and Leakage) (`modularity.md`)

## Program To An Interface, Not An Implementation

> Program to an interface, not an implementation.

> "Program to an interface" really means "Program to a supertype."

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

- Strategy Pattern — `Checkout` holds a `PaymentStrategy` field, never a concrete `CreditCardPayment`/`PayPalPayment`.
- Adapter Pattern — the rest of the app depends only on `PaymentGateway`; `StripeClient` (the concrete vendor SDK) is only ever referenced inside `StripeAdapter`.

### Related

- Encapsulate What Varies
- Favor Composition Over Inheritance
- Strive for Loosely Coupled Designs — interfaces are how loosely coupled objects know each other.
- Inheritance Tax

## Favor Composition Over Inheritance

> Favor composition over inheritance.

> The HAS-A relationship is an interesting one: each duck has a FlyBehavior and a QuackBehavior to which it delegates flying and quacking. When you put two classes together like this you're using composition. Instead of inheriting their behavior, the ducks get their behavior by being composed with the right behavior object.

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

- Strategy Pattern — `Checkout` HAS-A `PaymentStrategy` instead of inheriting payment logic; the strategy can be swapped per order, at runtime.
- Adapter Pattern — `StripeAdapter` composes a `StripeClient` rather than subclassing it, which is also the only option Java allows (no multiple inheritance for a class adapter).

### Related

- Encapsulate What Varies
- Program To An Interface
- Strive for Loosely Coupled Designs
- Inheritance Tax

## The Hollywood Principle

> Don't call us, we'll call you.

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

- Template Method Pattern — the chapter's case: the abstract class (`DataImporter` in its example) calls the subclass steps.
- Factory Method Pattern — the creator calls the subclass's factory method.
- Observer Pattern — observers register, the subject calls them.
- Strategy Pattern — the context calls whichever strategy it holds.

### Related

- Event-Driven Programming

## Principle of Least Knowledge (Law of Demeter)

> Principle of Least Knowledge — talk only to your immediate friends.

**Source:** *Head First Design Patterns*, Chapter 7; *Clean Code*, Chapter 6 (and heuristic G36, "Avoid Transitive Navigation"); *The Pragmatic Programmer*, Topic 28.

### How the other books refine it

- **Clean Code** calls chained getters **train wrecks**, and limits the law to *objects*. Chaining through a plain data structure (`config.db.host`) doesn't violate it, because a data structure is supposed to expose its fields (data object anti symmetry). Hybrids, which are half object and half data structure, make it unclear which rule applies.
- **The Pragmatic Programmer** simplifies it to "**Don't Chain Method Calls**" (Tip 46), with an exception for language-level pipelines that won't change. The fix it suggests is Tell, Don't Ask.

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

- Facade Pattern — the chapter's motivating case: the client of `CheckoutFacade` has one friend instead of inventory, payments, shipping, and email.
- Mediator Pattern — each colleague only talks to the mediator.

### Related

- Strive for Loosely Coupled Designs
- Encapsulate What Varies
- Decoupling
- Information Hiding (and Leakage) (`modularity.md`)
- Orthogonality (`modularity.md`)
- Tell, Don't Ask

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

- Principle of Least Knowledge (Law of Demeter) — TDA is how you follow the Law of Demeter without writing pass-through wrappers everywhere.
- Feature Envy — the smell for "asking": a method more interested in another object's data than its own.
- data object anti symmetry — TDA applies to *objects*. Plain data structures are meant to be asked.

### Related

- Decoupling
- Shared State Is Incorrect State (`concurrency.md`) — telling a resource to act atomically instead of check-then-act.

## Event-Driven Programming

> An event represents the availability of information. — *The Pragmatic Programmer*, Topic 29

**Source:** *The Pragmatic Programmer*, Topic 29; critique in *A Philosophy of Software Design*, Chapter 18.

### What it means in practice

Real applications react to things: clicks, webhooks, messages, timers. Hunt & Thomas give four ways to structure code around events, each one less coupled than a direct call:

1. **Finite state machines.** A small table of `state × event → new state + action`. They're underused, and they're good for parsing, protocols and order lifecycles.
2. **The Observer pattern.** The event source keeps a list of callbacks. This still couples observers to the source, and a slow observer blocks everyone.
3. **Publish/subscribe.** Channels sit between publishers and subscribers, so neither knows about the other. The cost is that it's harder to see who reacts to what.
4. **Reactive programming and streams.** Treat events as a collection over time (RxJS, Reactor) that you `map`, `filter` and `merge`, just like data.

**Ousterhout's caveat:** event-driven code isn't obvious, because you can't follow control flow by reading it. When a handler is invoked indirectly, document *when* and *by whom* it's called in its interface comment (code should be obvious).

### Example

```java
// State machine for an order lifecycle: illegal transitions are impossible by construction
enum OrderState {
    PENDING   { OrderState on(Event e) { return switch (e) { case PAID -> CONFIRMED; case CANCELLED -> VOID; default -> illegal(e); }; } },
    CONFIRMED { OrderState on(Event e) { return switch (e) { case SHIPPED -> SHIPPED; case REFUNDED -> VOID; default -> illegal(e); }; } },
    ...;
    abstract OrderState on(Event e);
}

// Pub/sub: billing doesn't know who listens for OrderPaid
eventBus.publish(new OrderPaid(orderId, amount));   // shipping, email and analytics each subscribe independently
```

### Where it applies

- observer pattern — option 2, and the base of the others.
- state pattern — the object-oriented way to implement the FSM option.
- Blackboards (`concurrency.md`) and Actors and Processes (`concurrency.md`) — event-driven coordination at the system level.

### Related

- Decoupling
- Transforming Programming — reactive streams are transformation pipelines over time.
- Breaking Temporal Coupling (`concurrency.md`)
- The Hollywood Principle — "don't call us, we'll call you" is the basic event-driven inversion.

## Transforming Programming

> Programming Is About Code, But Programs Are About Data. — Tip 49

**Source:** *The Pragmatic Programmer*, Topic 30 (also Tip 50, "Don't Hoard State; Pass It Around").

### What it means in practice

Every program turns inputs into outputs. Hunt & Thomas suggest designing it that way on purpose. Start with the input and the desired output, then break the gap into a **pipeline of transformations**, each a function that takes data and returns new data. Unix pipes (`cat | grep | sort | uniq -c`) are the model.

- **Don't hoard state; pass it around.** Data flows through the pipeline instead of sitting in objects that methods modify. That removes a whole class of coupling.
- **Handle errors inside the pipeline.** Wrap values in a result type (`{ok, value}` / `{error, reason}`) and have each step skip work when it gets an error, so the pipeline still reads as one straight line.
- **Transformations at every scale:** a whole system, a module, or a single function.

### Example

```java
// Hoarded state: the importer object accumulates and mutates as it goes
importer.load(csv); importer.dedupe(); importer.enrichWithGeo(); importer.save();

// Transformation pipeline: each stage is a pure function of its input
Path csv = Path.of("leads.csv");
Files.lines(csv)
     .map(LeadParser::parse)          // String -> Result<Lead>
     .flatMap(Result::stream)          // drop/log failures in one place
     .distinct()                       // dedupe by value equality
     .map(geo::enrich)                 // Lead -> EnrichedLead
     .forEach(leads::save);
```

### Where it applies

- functional programming — the paradigm this topic asks you to borrow from.
- Loops — Fowler's smell, fixed by Replace Loop with Pipeline.
- hidden temporal coupling — in a pipeline, order is enforced by the data flow ("bucket brigade").
- closure of operations — Evans: operations that return the same type compose into pipelines.

### Related

- Event-Driven Programming — reactive streams are pipelines over events.
- Decoupling
- Breaking Temporal Coupling (`concurrency.md`)

## Inheritance Tax

> Don't Pay Inheritance Tax. — Tip 51

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

- Decoupling
- Information Hiding (and Leakage) (`modularity.md`)

## Externalize Configuration

> Parameterize Your App Using External Configuration. — Tip 55

**Source:** *The Pragmatic Programmer*, Topic 32.

### What it means in practice

Values that may change after the code ships don't belong in the code: credentials, service URLs, feature flags, tax rates, timeouts, license details. Put them in configuration so they can change without a rebuild. Hunt & Thomas add two refinements:

- **Wrap configuration behind your own API** instead of letting the whole codebase read a global YAML or environment hash. The format and location then become a detail.
- **Configuration-as-a-service.** Serve configuration from an API instead of static files. Many instances can share it, changes can be audited and access-controlled, and running apps can pick up changes without restarting.

The caution: don't overdo it. Making everything configurable ("let's make the business logic a config file") pushes complexity into configuration that nobody tests.

### Example

```java
// Hard-coded: a deploy to change a timeout
HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(3));

// Externalized and wrapped: one typed API, any source behind it (env, file, config service)
public record PaymentConfig(URI providerUrl, Duration timeout, boolean threeDsRequired) {}
var http = HttpClient.newBuilder().connectTimeout(config.payment().timeout());
```

### Contrast with Ousterhout

Pull Complexity Downwards (`modularity.md`) warns that configuration parameters can be a way of *exporting* complexity. Instead of making a decision, the module makes every user decide. Externalize what really varies between deployments, and let the code compute sensible defaults for everything else.

### Related

- DRY — Don't Repeat Yourself (`modularity.md`) — one authoritative source for each value.
- Decoupling — a wrapped config API instead of a global settings map.
