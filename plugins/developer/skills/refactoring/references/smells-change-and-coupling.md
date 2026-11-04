# Smells: change and coupling

Refactoring, Chapter 3: code where one change spreads, or where parts know too much about each other.

## Contents

- [Divergent Change](#divergent-change)
- [Shotgun Surgery](#shotgun-surgery)
- [Feature Envy](#feature-envy)
- [Insider Trading](#insider-trading)
- [Message Chains](#message-chains)
- [Middle Man](#middle-man)
- [Global Data](#global-data)
- [Mutable Data](#mutable-data)

## Divergent Change

**Source:** *Refactoring*, Chapter 3.

### What it looks like

One module that gets changed in different ways for different, unrelated reasons: "I have to change these three functions every time I get a new database; I have to change these four functions every time there's a new financial instrument." Two separate contexts (database interaction, financial processing) are tangled into one module, so touching one forces you to understand both. This is exactly what SRP names as a class answering to more than one actor.

### Example

```java
// OrderService changes both when payment providers change AND when tax rules change
public class OrderService {
    void chargeCard(Order order) { /* Stripe-specific logic */ }
    void chargePayPal(Order order) { /* PayPal-specific logic */ }
    double calculateTax(Order order, String region) { /* tax-rule logic */ }
}
```

Splitting `Payment` and `TaxCalculator` into separate classes means a new payment provider never touches tax code, and a new tax rule never touches payment code.

### Fixes it

- Split Phase — if the two aspects naturally form a sequence (fetch, then process).
- Move Function — divide processing into the right modules when there's more back-and-forth.
- Extract Function, Extract Class — separate the mixed concerns before moving them.

### Related

- Shotgun Surgery — the opposite failure mode (one change scattered across many modules instead of many reasons crammed into one).
- True vs. Accidental Duplication (`changing-code-safely.md`) — wrongly unifying accidental duplicates produces this smell.
- Feature Envy

## Shotgun Surgery

**Source:** *Refactoring*, Chapter 3.

### What it looks like

The mirror image of Divergent Change: instead of one module changing for many reasons, *one reason to change* forces small edits scattered across many different classes. The edits are "hard to find, and it's easy to miss an important change" — exactly the failure mode the Common Closure Principle exists to prevent by co-locating things that change together.

### Example

```java
// Adding a new notification channel means editing four unrelated classes
class OrderService   { /* + one more if/case for the new channel */ }
class UserService     { /* + one more if/case for the new channel */ }
class AdminPanel       { /* + one more if/case for the new channel */ }
class ReportGenerator { /* + one more if/case for the new channel */ }
```

Gathering the notification logic into one `NotificationDispatcher` component means a new channel is added in exactly one place.

### Fixes it

- Move Function, Move Field — pull the scattered pieces into a single module.
- Combine Functions into Class / Combine Functions into Transform — for functions that operate on the same data.
- Split Phase — if the common functions can combine their output for a later phase.
- Inlining first (Inline Function, Inline Class) is a legitimate intermediate step — pull everything together into one Large Class (`smells-readability-and-size.md`), then re-extract sensibly.

### Related

- Divergent Change
- Large Class (`smells-readability-and-size.md`)
- DRY — Don't Repeat Yourself (`changing-code-safely.md`)

## Feature Envy

**Source:** *Refactoring*, Chapter 3.

### What it looks like

A function that spends more time reaching into another object's data (via getters) than working with its own module's data — "we've lost count of the times we've seen a function invoking half-a-dozen getter methods on another object to calculate some value." The fix is usually obvious once you see it: the function clearly wants to live where the data lives. The heuristic when a function touches several objects: put it with whichever one has most of the data it needs.

Fowler explicitly calls out that Strategy and Visitor (Strategy Pattern among them) intentionally break this rule — sometimes you *want* behavior to live away from its data, to keep it swappable. Feature Envy is a smell, not an absolute law.

### Example

```java
// Envious: ReportBuilder reaches into Invoice six different ways
class ReportBuilder {
    String summarize(Invoice invoice) {
        return invoice.getCustomerName() + " owes " + invoice.getTotal()
             + " due " + invoice.getDueDate() + " (" + invoice.getStatus() + ")";
    }
}
```

```java
// At home: the behavior moves to the data it actually uses
class Invoice {
    String summarize() {
        return customerName + " owes " + total + " due " + dueDate + " (" + status + ")";
    }
}
```

### Fixes it

- Move Function — send the whole function to where the data lives.
- Extract Function — when only part of a function is envious, split it off first.

### Related

- Divergent Change

## Insider Trading

**Source:** *Refactoring*, Chapter 3.

### What it looks like

Modules reaching into each other's internals more than their public boundary should allow — "modules that whisper to each other by the coffee machine," trading data in ways that increase coupling without going through a clean, visible interface. Inheritance makes this especially easy: a subclass always knows more about its parent's internals than the parent would like.

### Example

```java
// Insider trading: OrderService reaches directly into InventoryService's internal map
class InventoryService {
    Map<String, Integer> stockLevels = new HashMap<>(); // meant to be private
}
class OrderService {
    void reserve(String sku, InventoryService inventory) {
        inventory.stockLevels.put(sku, inventory.stockLevels.get(sku) - 1); // reaching in directly
    }
}
```

```java
// Regulated: the trade goes through a narrow, intentional interface
class InventoryService {
    private final Map<String, Integer> stockLevels = new HashMap<>();
    void reserve(String sku) { stockLevels.merge(sku, -1, Integer::sum); }
}
```

### Fixes it

- Move Function / Move Field — reduce the need to reach across.
- Hide Delegate — introduce a well-regulated intermediary for shared interests.
- Replace Subclass with Delegate / Replace Superclass with Delegate — when inheritance is the source of the collusion.

### Related

- Message Chains

## Message Chains

**Source:** *Refactoring*, Chapter 3.

### What it looks like

A client asking one object for another, then asking that object for yet another, and so on — a long line of `getThis().getThat().getOther()`. Navigating this way couples the client to the exact internal structure of the chain: change any intermediate relationship and every client following the chain has to change too.

### Example

```java
// Chained: the client knows the full path through the object graph
String zip = order.getCustomer().getAddress().getCity().getZipCode();
```

```java
// Hidden: the client asks Order directly; Order hides how it gets there
String zip = order.getShippingZipCode();
```

### Fixes it

- Hide Delegate — applied at one or more points in the chain.
- Extract Function + Move Function — take the code that uses the end result and push it down the chain instead.

### Related

- Middle Man — hiding every link in a chain risks turning every intermediate object into one of these.
- Insider Trading

## Middle Man

**Source:** *Refactoring*, Chapter 3.

### What it looks like

Encapsulation taken too far: a class whose interface is mostly just delegating calls straight through to another object, adding nothing of its own. Some delegation is healthy (you don't need to know whether a director's calendar is a diary or an app) — the smell is when *half the methods* on a class are pure pass-through.

### Example

```java
// Middle man: every method just forwards to warehouse
class WarehouseFacade {
    Item findItem(String id) { return warehouse.findItem(id); }
    void reserveItem(String id) { warehouse.reserveItem(id); }
    void releaseItem(String id) { warehouse.releaseItem(id); }
    // ... seven more pure pass-throughs
}
```

If `WarehouseFacade` never adds behavior of its own, callers should talk to `Warehouse` directly.

### Fixes it

- Remove Middle Man — talk to the real object instead.
- Inline Function — for the few methods not doing much.
- Replace Superclass with Delegate / Replace Subclass with Delegate — when there's real behavior to preserve while folding the middle man away.

### Related

- Message Chains
- Lazy Element (`smells-structure-and-speculation.md`)

## Global Data

**Source:** *Refactoring*, Chapter 3.

### What it looks like

Data — a global variable, a class variable, a singleton's mutable state — that any part of the codebase can read and modify, with no way to trace which code touched it. "The problem with global data is that it can be modified from anywhere in the code base, and there's no mechanism to discover which bit of code touched it" — leading to "spooky action at a distance" bugs that are hard to trace back to their source. Small amounts are tolerable (Fowler's Paracelsus reference: "the difference between a poison and something benign is the dose"), but the cost grows exponentially with how much of it there is.

### Example

```java
// Global: any class in the codebase can mutate this
public class Cache {
    public static Map<String, User> USERS = new HashMap<>();
}
```

```java
// Encapsulated: all access goes through one narrow, traceable surface
public class UserCache {
    private final Map<String, User> users = new HashMap<>();
    public User get(String id) { return users.get(id); }
    public void put(String id, User user) { users.put(id, user); }
}
```

### Fixes it

- Encapsulate Variable — the first move, always: wrap it behind a function so you can see (and later control) where it's touched.

### Related

- Mutable Data — global data is especially dangerous when it's also mutable.
- Long Parameter List (`smells-readability-and-size.md`)

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

- Global Data
