# Smells: readability and size

Refactoring, Chapter 3: code that is hard to read, too big, or repeats itself.

## Contents

- [Mysterious Name](#mysterious-name)
- [Duplicated Code](#duplicated-code)
- [Long Function](#long-function)
- [Long Parameter List](#long-parameter-list)
- [Large Class](#large-class)
- [Data Clumps](#data-clumps)
- [Primitive Obsession](#primitive-obsession)
- [Repeated Switches](#repeated-switches)
- [Loops](#loops)
- [Temporary Field](#temporary-field)
- [Comments (as a smell)](#comments-as-a-smell)

## Mysterious Name

**Source:** *Refactoring*, Chapter 3.

### What it looks like

A function, variable, class, or module whose name doesn't tell you what it does or how to use it — you have to read the body (or worse, ask someone) to find out. Fowler calls naming "one of the two hard things in programming," and treats a name you can't get right as a signal, not a cosmetic issue: "when you can't think of a good name for something, it's often a sign of a deeper design malaise."

### Example

```java
// Mysterious: what is t, what is u, what does this return?
double f(double t, double u) {
    return t * u / 100;
}
```

```java
// Clear: the name is the documentation
double calculateDiscountAmount(double price, double discountPercentage) {
    return price * discountPercentage / 100;
}
```

### Fixes it

- Change Function Declaration (rename a function)
- Rename Variable
- Rename Field

### Related

- Comments — a comment explaining a name is a hint the name itself should change instead.
- The Boy Scout Rule (`changing-code-safely.md`)

## Duplicated Code

**Source:** *Refactoring*, Chapter 3.

### What it looks like

The same code structure appearing in more than one place. Every copy is a tax: reading it means checking whether the copies have secretly diverged, and changing it means finding and fixing every occurrence — miss one and you've got a bug that only reproduces in the path you forgot.

### Example

```java
// Duplicated: same shipping-fee formula in two places
double webCheckoutFee = baseRate + (weightKg * 2.5);
double phoneOrderFee  = baseRate + (weightKg * 2.5);
```

```java
// Unified: one function, called from both places
double shippingFee(double baseRate, double weightKg) {
    return baseRate + (weightKg * 2.5);
}
```

### Fixes it

- Extract Function — the simplest case: same expression in two methods of one class.
- Slide Statements — when the duplicates are similar but not identical, line them up first.
- Pull Up Method — when the duplication is across subclasses of a common base.

### Related

- Long Function
- Data Clumps
- True vs. Accidental Duplication (`changing-code-safely.md`) — only *true* duplication is this smell; code that looks alike but changes for different reasons should stay duplicated.
- The Boy Scout Rule (`changing-code-safely.md`)
- Broken Windows (Software Entropy) (`changing-code-safely.md`)
- Refactor Early, Refactor Often (`changing-code-safely.md`)
- DRY — Don't Repeat Yourself (`changing-code-safely.md`)

## Long Function

**Source:** *Refactoring*, Chapter 3.

### What it looks like

A function that does too much in one place. Counter to intuition, the programs that age best have *lots of short, well-named functions* — "the real key to making it easy to understand small functions is good naming... if you have a good name for a function, you mostly don't need to look at its body." The heuristic Fowler and Beck use: whenever you feel the urge to write a comment explaining a chunk of code, write a function instead, named after what that code is *for*.

### Example

```java
// Long: validation, pricing, and notification all inline, one giant function
void processOrder(Order order) {
    if (order.getItems().isEmpty()) throw new IllegalStateException("empty order");
    if (order.getCustomer() == null) throw new IllegalStateException("no customer");
    double total = 0;
    for (Item item : order.getItems()) total += item.getPrice() * item.getQuantity();
    if (order.getCustomer().isVip()) total *= 0.9;
    order.setTotal(total);
    emailService.send(order.getCustomer().getEmail(), "Order confirmed: $" + total);
}
```

```java
// Short: each step is named and independently readable
void processOrder(Order order) {
    validate(order);
    order.setTotal(calculateTotal(order));
    notifyCustomer(order);
}
```

### Fixes it

- Extract Function — the fix 99% of the time.
- Replace Temp with Query, Introduce Parameter Object, Preserve Whole Object — when too many temps/parameters block extraction.
- Decompose Conditional — for conditional-heavy functions.
- Split Loop — when an extracted loop is doing two things at once.

### Related

- Duplicated Code
- Repeated Switches
- Comments (as a smell)
- The Boy Scout Rule (`changing-code-safely.md`)

## Long Parameter List

**Source:** *Refactoring*, Chapter 3.

### What it looks like

A function that needs so many parameters that calling it correctly is hard to get right and hard to read at the call site. It's often the result of over-correcting against Global Data (`smells-change-and-coupling.md`) — "pass everything the function needs as a parameter" is fine advice until the list itself becomes confusing.

### Example

```java
// Long: what does true, true, 3 mean at the call site?
User createUser(String name, String email, String phone, String address,
                 boolean isAdmin, boolean sendWelcomeEmail, int retryCount) { /* ... */ }
```

```java
// Slimmed: one cohesive object, self-documenting at the call site
User createUser(UserRequest request) { /* ... */ }
```

### Fixes it

- Replace Parameter with Query — when one parameter can be derived from another.
- Preserve Whole Object — pass the original structure instead of pulling fields out of it.
- Introduce Parameter Object — when several parameters always travel together.
- Remove Flag Argument — for a boolean that just selects between two behaviors.
- Combine Functions into Class — when multiple functions share the same parameter set.

### Related

- Data Clumps
- Global Data (`smells-change-and-coupling.md`)

## Large Class

**Source:** *Refactoring*, Chapter 3.

### What it looks like

A class trying to do too much, usually showing up first as too many fields — and "when a class has too many fields, duplicated code cannot be far behind." A good signal for how to split it: common prefixes/suffixes among the fields, or looking at which *clients* only ever touch a subset of the class's features — each subset is a candidate for its own class.

### Example

```java
// Large: payment, shipping, invoicing, and refunds all live on one Order
class Order {
    // payment fields
    String cardNumber; String billingAddress;
    // shipping fields
    String carrier; String trackingNumber; String shippingAddress;
    // invoicing fields
    String invoiceNumber; Date invoiceDate;
    // refund fields
    String refundReason; double refundAmount;
    // 30+ more...
}
```

```java
// Split by clients' actual usage
class Order       { Payment payment; Shipment shipment; Invoice invoice; }
class Payment     { String cardNumber; String billingAddress; }
class Shipment    { String carrier; String trackingNumber; String shippingAddress; }
```

### Fixes it

- Extract Class — bundle related fields into a component.
- Extract Superclass / Replace Type Code with Subclasses — when the split fits an inheritance shape.

### Related

- Data Clumps
- Shotgun Surgery (`smells-change-and-coupling.md`)

## Data Clumps

**Source:** *Refactoring*, Chapter 3.

### What it looks like

The same small group of data items — three or four fields, or parameters — showing up together over and over, as fields in multiple classes or as parameters in many method signatures. A good test: "consider deleting one of the data values — if the others don't make sense without it, that's a sure sign you have an object that's dying to be born."

### Example

```java
// Clumped: startDate, endDate, and timezone always travel together
void scheduleReport(Date startDate, Date endDate, String timezone) { /* ... */ }
void archiveLogs(Date startDate, Date endDate, String timezone) { /* ... */ }
```

```java
// Born: the clump becomes its own type
record DateRange(Date startDate, Date endDate, String timezone) { }

void scheduleReport(DateRange range) { /* ... */ }
void archiveLogs(DateRange range) { /* ... */ }
```

### Fixes it

- Extract Class — when the clump shows up as fields.
- Introduce Parameter Object / Preserve Whole Object — when the clump shows up as parameters.

### Related

- Long Parameter List
- Primitive Obsession
- Duplicated Code
- Large Class

## Primitive Obsession

**Source:** *Refactoring*, Chapter 3.

### What it looks like

Reluctance to create small, meaningful types for domain concepts, leaving code that treats everything as an `int`, `double`, or `String` — money handled as a plain number, physical quantities computed while ignoring units, or a phone number represented as a raw string ("stringly typed"). The primitive compiles fine but throws away every rule the domain actually has (you can add two `int`s that represent unrelated things without the compiler blinking).

### Example

```java
// Primitive: nothing stops you from adding USD cents to EUR cents
double amount = 4999; // cents
String currency = "USD";
```

```java
// A real type: the rules live with the data
record Money(long cents, String currencyCode) {
    Money add(Money other) {
        if (!currencyCode.equals(other.currencyCode)) throw new IllegalArgumentException();
        return new Money(cents + other.cents, currencyCode);
    }
}
```

### Fixes it

- Replace Primitive with Object
- Replace Type Code with Subclasses + Replace Conditional with Polymorphism — when the primitive is a type code driving conditional logic.
- Extract Class / Introduce Parameter Object — when primitives commonly travel together (Data Clumps).

### Related

- Data Clumps

## Repeated Switches

**Source:** *Refactoring*, Chapter 3.

### What it looks like

Not "any switch statement is bad" — Fowler is explicit that he's not "unconditionally opposed to the conditional." The smell is the *same* switch/case (or if/else cascade), switching on the same condition, duplicated in multiple places. Every time a new case is added, you have to hunt down and update every copy — miss one and behavior silently diverges between them.

### Example

```java
// Repeated: the same switch on orderType shows up in three methods
double calculatePrice(Order o)  { switch (o.getType()) { case STANDARD: ...; case EXPRESS: ...; } }
double calculateTax(Order o)    { switch (o.getType()) { case STANDARD: ...; case EXPRESS: ...; } }
Label generateLabel(Order o)     { switch (o.getType()) { case STANDARD: ...; case EXPRESS: ...; } }
```

```java
// Polymorphic: adding a new order type touches one class, not three switches
interface OrderType {
    double price(Order o);
    double tax(Order o);
    Label label(Order o);
}
class StandardOrder implements OrderType { /* ... */ }
class ExpressOrder implements OrderType { /* ... */ }
```

This is exactly what Strategy and OCP give you: adding `OvernightOrder` means one new class, zero edits to existing switches.

### Fixes it

- Replace Conditional with Polymorphism

### Related

- Long Function
- DRY — Don't Repeat Yourself (`changing-code-safely.md`)

## Loops

**Source:** *Refactoring*, Chapter 3.

### What it looks like

Not a claim that loops don't work — a claim that, now that first-class functions are widely supported, an explicit `for`/`while` loop is usually less clear than a pipeline of `filter`/`map`/`reduce`-style operations. A pipeline names *what* is being selected and *what* is being done to it; a loop makes you read the whole body to reconstruct that intent.

### Example

```java
// Loop: intent is buried in the accumulation logic
List<String> names = new ArrayList<>();
for (User user : users) {
    if (user.isActive()) {
        names.add(user.getName());
    }
}
```

```java
// Pipeline: filter and map name the intent directly
List<String> names = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .collect(Collectors.toList());
```

### Fixes it

- Replace Loop with Pipeline


## Temporary Field

**Source:** *Refactoring*, Chapter 3.

### What it looks like

A field that's only set (and only meaningful) under certain circumstances, and sits null/unused the rest of the time. This is confusing because "you expect an object to need all of its fields" — trying to figure out why a field exists when it doesn't seem to be used can drive you nuts.

### Example

```java
// Temporary: discountCode only matters during checkout, null every other time
class Order {
    private String discountCode; // null unless a checkout is in progress
}
```

```java
// A dedicated home for the checkout-only state
class CheckoutSession {
    private final Order order;
    private final String discountCode;
}
```

### Fixes it

- Extract Class — give the orphan field(s) their own home.
- Move Function — move the code that concerns the field into that new class.
- Introduce Special Case — for the conditional logic around "is this field valid right now."

### Related

- Data Class (`smells-structure-and-speculation.md`)

## Comments (as a smell)

**Source:** *Refactoring*, Chapter 3.

### What it looks like

Not an argument against comments — Fowler calls them "a sweet smell," not a bad one. The smell is comments used as a **deodorant**: thickly commented code where the comment is only there because the code itself is confusing or badly named. Chase the comment back to whatever Long Function, Mysterious Name, or other smell it's covering for, fix that, and the comment usually becomes unnecessary on its own.

### Example

```java
// Deodorant: the comment is doing the job the code should do
// Check if user is eligible for premium discount (must be active member for 1+ years)
if (user.isActive() && user.getMembershipMonths() >= 12) { ... }
```

```java
// The comment becomes superfluous once the code says it directly
if (user.isEligibleForPremiumDiscount()) { ... }
```

A comment is genuinely useful when it explains *why* — a non-obvious constraint, a workaround, an area of uncertainty for future readers — not *what* the next few lines do.

### Fixes it

- Extract Function — turn the commented block into a well-named function.
- Change Function Declaration — if the function's already extracted but still needs explaining, rename it instead.
- Introduce Assertion — for comments stating a required system state.

### Related

- Mysterious Name
- Long Function
