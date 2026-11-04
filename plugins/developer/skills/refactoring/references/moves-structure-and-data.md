# Moves: data, classes and modules

Hand-written from *Refactoring* (2nd ed.), Chapters 6–9, in our own words. "Class" means whatever groups data with behavior in your language: a class, a struct with methods, a module with a type, or a record with functions. Run the tests after each move.

## Contents

- Introduce Parameter Object · Combine Functions into Class · Combine Functions into Transform
- Encapsulate Record · Encapsulate Collection · Replace Primitive with Object
- Extract Class · Inline Class
- Move Function · Move Field
- Hide Delegate · Remove Middle Man
- Change Reference to Value · Change Value to Reference

## Introduce Parameter Object

**When:** the same values travel together through several functions, such as `start, end` or `amount, currency`.
**How:** define an immutable type. Add it as a parameter, change callers to pass it, then switch uses from the old parameters to it and remove them one at a time.
**Watch:** the real payoff comes after: behavior moves to the new type, and it may reveal a domain concept.

## Combine Functions into Class

**When:** a group of functions operates on the same data, particularly with that data passed in each time.
**How:** encapsulate the record, then move each function in, dropping the arguments that are now fields.
**Watch:** in languages without classes, a module with a type achieves the same goal.

## Combine Functions into Transform

**When:** several derivations are calculated from the same source data, and you'd rather produce one enriched record.
**How:** write a transform that returns a deep copy with the extra fields, then move derivations into it one by one.
**Watch:** the source must not be updated afterward, or the derived values go stale. If it can change, use a class.

## Encapsulate Record

**When:** a mutable record or map is shared widely. It can't express which fields are derived, or be changed easily.
**How:** encapsulate the variable, give it a class with accessors, and move callers to the new accessors. For nested data, return copies or read-only views.
**Watch:** plain immutable records are fine as they are, particularly in functional code.

## Encapsulate Collection

**When:** a getter returns the internal collection, so any caller can modify it behind the owner's back.
**How:** add `add` and `remove` operations, migrate modifications to them, and return a copy or a read-only view from the getter.
**Watch:** pick one convention for the whole code base. Consider the cost of copies for big collections.

## Replace Primitive with Object

**When:** a string or number has rules or behavior of its own, such as a phone number, money, or a priority.
**How:** encapsulate the variable, create a small value type, and change the setter and getter to go through it. Then move related logic into it.
**Watch:** a newtype, enum, tagged union, or branded type can give the same safety at low cost.

## Extract Class

**When:** a class has grown and a subset of data and methods go together, or change together.
**How:** create the new class and a link from the old one. Move fields, then methods, smallest and fewest callers first, testing each time. Decide whether to expose the new class.

## Inline Class

**When:** a class no longer does enough to justify itself, or as a first step in reassigning responsibilities between two classes.
**How:** create delegating methods on the target, move callers to them, move everything across and delete the empty class.

## Move Function

**When:** a function uses more of another context's data than its own, or would simplify callers there.
**How:** check what else it uses, and whether that should move too. Copy to the target and adjust it, delegate from the source, test, then either inline the delegate or keep it.
**Watch:** polymorphism. A new parameter is often needed if it uses features of its old context. A move is hard to decide if contexts aren't clear; postpone it if so.

## Move Field

**When:** a field is used more elsewhere, or is always passed along with another type's data.
**How:** encapsulate it, add the field on the target, adjust accessors, and move the data. Test, and then remove the source field.
**Watch:** with shared data, ensure the target is shared the same way. Persisted fields need a migration.

## Hide Delegate

**When:** callers navigate `a.getB().getC()`, so they depend on the structure.
**How:** add a delegating method on the server, change callers to use it, and remove the accessor if unused.

## Remove Middle Man

**When:** a class has become mostly delegating methods. Hide Delegate has gone too far.
**How:** expose the delegate, move each caller to it, and remove the delegating method. Find the balance as the system changes.

## Change Reference to Value

**When:** an inner object is small and needn't be shared, so it can be immutable.
**How:** check that it is or can be immutable, remove its setters, and define equality by value.

## Change Value to Reference

**When:** several copies of a record must all see the same update.
**How:** create a repository of instances, ensure each has an identity, and fetch from the repository instead of constructing it.
**Watch:** shared mutable objects are a source of concurrency and aliasing bugs. Prefer immutable values if updates are rare.
