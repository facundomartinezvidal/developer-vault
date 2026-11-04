# Smells: structure and speculation

Refactoring, Chapter 3: elements that do not earn their place, and hierarchies that do not fit.

## Contents

- [Lazy Element](#lazy-element)
- [Speculative Generality](#speculative-generality)
- [Data Class](#data-class)
- [Refused Bequest](#refused-bequest)
- [Alternative Classes with Different Interfaces](#alternative-classes-with-different-interfaces)

## Lazy Element

**Source:** *Refactoring*, Chapter 3.

### What it looks like

A program element (function, class) that isn't pulling its weight — a function named the same as its one-line body, or a class that's really just one simple function wrapped in ceremony. Often it's a leftover: something that was expected to grow and never did, or something that used to earn its keep and got downsized by earlier refactoring but never removed.

### Example

```java
// Lazy: this function adds nothing beyond what its name already says
int getUserId(User user) {
    return user.id;
}
```

Just use `user.id` directly (or `user.getUserId()` doesn't need a free-standing wrapper).

### Fixes it

- Inline Function / Inline Class
- Collapse Hierarchy — when the lazy element is a spot in an inheritance chain.

### Related

- Speculative Generality
- Middle Man (`smells-change-and-coupling.md`)

## Speculative Generality

**Source:** *Refactoring*, Chapter 3.

### What it looks like

Machinery built for a future that hasn't arrived: code added because it might be needed someday, followed by hooks, abstract classes, and unused parameters added just in case. If the machinery isn't being used, it's not paying for itself — it just makes the code harder to understand and change today. A telltale sign: the only caller of a function or class is a test.

### Example

```java
// Speculative: an abstract "strategy" hierarchy with exactly one real implementation
abstract class DiscountStrategy { abstract double apply(double price); }
class StandardDiscount extends DiscountStrategy {
    double apply(double price) { return price * 0.95; }
}
// no other implementation exists, and none is planned
```

If there's really only one discount rule, a plain method is enough; build the abstraction when a second case actually shows up.

### Fixes it

- Collapse Hierarchy — for abstract classes doing little.
- Inline Function / Inline Class — for unnecessary delegation.
- Change Function Declaration — to drop unused parameters.
- Remove Dead Code — when only a test calls it.

### Related

- Lazy Element
- Broken Windows (Software Entropy) (`changing-code-safely.md`)

## Data Class

**Source:** *Refactoring*, Chapter 3.

### What it looks like

A class that's nothing but fields plus getters and setters — a dumb data holder with no behavior of its own, which other classes end up manipulating in far too much detail. It's a sign the behavior that belongs with this data is living somewhere else instead. (Exception: an immutable result record — e.g. the intermediate structure between two phases after Split Phase — is a legitimate data class; immutable fields don't need encapsulating.)

### Example

```java
// Data class: no behavior, just a bag of getters/setters manipulated from outside
class UserDto {
    private String name;
    private String email;
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
// elsewhere:
if (userDto.getEmail() != null && userDto.getEmail().contains("@")) { /* validation lives outside */ }
```

```java
// Behavior moves in where the data already is
class User {
    private String name;
    private String email;
    boolean hasValidEmail() { return email != null && email.contains("@"); }
}
```

### Fixes it

- Encapsulate Record — first move, if fields are public.
- Remove Setting Method — on any field that shouldn't change after construction.
- Move Function / Extract Function — pull the behavior that uses this data into the class itself.

### Related

- Temporary Field (`smells-readability-and-size.md`)

## Refused Bequest

**Source:** *Refactoring*, Chapter 3.

### What it looks like

A subclass that inherits methods and data from its parent but only wants part of what it's given. Fowler treats this as a mild smell most of the time — reusing a bit of behavior via subclassing is fine, and usually this smell is too weak to justify cleaning up. It gets much stronger when the subclass reuses the implementation but actively **doesn't want to support the parent's interface** — that's a real LSP violation, not just a style nitpick.

### Example

This is the same failure as LSP's `List`/unmodifiable-list example: an `UnsupportedOperationException`-throwing subtype that refuses part of its supertype's contract.

```java
class ReadOnlyList<T> extends ArrayList<T> {
    @Override public boolean add(T item) { throw new UnsupportedOperationException(); }
    @Override public T remove(int i)    { throw new UnsupportedOperationException(); }
}
```

`ReadOnlyList` inherited `add()`/`remove()` and refuses to honor them — any code written generically against `List` breaks the moment it receives one.

### Fixes it

- Push Down Method / Push Down Field — when the hierarchy itself is wrong; move the unused parts to a sibling.
- Replace Subclass with Delegate / Replace Superclass with Delegate — when the subclass refuses the *interface*, not just the implementation; don't patch the hierarchy, replace it.


## Alternative Classes with Different Interfaces

**Source:** *Refactoring*, Chapter 3.

### What it looks like

Two classes that do essentially the same job but can't be substituted for each other because their methods are named or shaped differently. One of the main benefits of classes — swapping one implementation for another — only works if their interfaces actually match.

### Example

```java
class EmailSender { void send(String message) { /* ... */ } }
class SmsGateway   { void dispatch(String text) { /* ... */ } }
// same job, different method names — can't be used interchangeably
```

When you own both classes, rename to align them directly. When you *don't* own one of them (a third-party SDK), that's exactly the situation Adapter exists for — wrap the one you can't change behind an interface that matches the one you can.

### Fixes it

- Change Function Declaration — rename to align, when you own both classes.
- Move Function — keep moving behavior until the protocols genuinely match.
- Extract Superclass — if aligning them creates duplication.
