# Moves: inheritance

Hand-written from *Refactoring* (2nd ed.), Chapter 12, in our own words. In languages without inheritance, such as Go or Rust, or if the code base prefers composition, read this as interface and composition guidance. Run the tests after each move.

## Pull Up Method, Field or Constructor Body

**When:** subclasses have the same behavior or data. Duplication in a hierarchy invites divergence.
**How:** check they really are identical. Harmonize signatures, copy to the parent, remove one child's copy at a time, testing each. Constructors share by calling the parent's.
**Watch:** a pulled-up method mustn't use features only the children have. Share through a superclass only if it's truly an "is a" relationship.

## Push Down Method or Field

**When:** something on the parent is relevant to just one or a few children.
**How:** copy it to each child that needs it, then remove it from the parent.

## Replace Type Code with Subclasses

**When:** behavior varies with a type code, or some fields only apply to certain codes.
**How:** encapsulate the type code, then create a variant for each value, with a factory. Move behavior using Replace Conditional with Polymorphism, and remove the code.
**Watch:** a tagged union or enum with data is often a better fit. Use a delegate if the type can change at runtime or several dimensions vary.

## Remove Subclass

**When:** a subclass no longer does enough to be understood as its own thing.
**How:** replace constructors with a factory, move type checks to the parent, represent the difference as a field, then delete it.

## Extract Superclass

**When:** two classes do similar things, and a parent would express that.
**How:** create the empty parent, make both inherit, pull up members and common logic, and use the parent where possible.
**Watch:** extracting a shared collaborator instead is usually more flexible.

## Collapse Hierarchy

**When:** a parent and child are no longer different enough.
**How:** pick one to keep, move everything into it, adjust references and delete the other.

## Replace Subclass with Delegate

**When:** an object must vary along several dimensions, or at runtime, or inheritance couples too tightly to the parent.
**How:** create a delegate type, add a field for it on the host, move the factory to set it, then move subclass methods to the delegate, one by one, and remove each subclass. Use polymorphic delegates if more than one remains.
**Watch:** inheritance is fine for one stable dimension. Start with it, and move to a delegate when it starts to hurt.

## Replace Superclass with Delegate

**When:** the subclass doesn't really have an "is a" relationship with its parent, or exposes inherited operations it doesn't support. This is the usual fix for Refused Bequest.
**How:** add a field for the parent instance, write delegating methods for what callers really use, and then remove the inheritance link. Test after each step.
**Watch:** if most of the parent's interface is really needed, the delegation may be boilerplate; a small interface may help.
