# Moves: conditionals and APIs

Hand-written from *Refactoring* (2nd ed.), Chapters 10–11, in our own words. Run the tests after each move.

## Contents

- Decompose Conditional · Consolidate Conditional Expression · Replace Nested Conditional with Guard Clauses
- Replace Conditional with Polymorphism · Introduce Special Case · Introduce Assertion
- Separate Query from Modifier · Parameterize Function · Remove Flag Argument
- Preserve Whole Object · Replace Parameter with Query · Replace Query with Parameter
- Remove Setting Method · Replace Constructor with Factory Function · Replace Function with Command · Replace Command with Function

## Decompose Conditional

**When:** a condition and its branches hide why they exist.
**How:** extract the condition and each branch to functions named for intent, such as `isSummer` and `summerCharge`.

## Consolidate Conditional Expression

**When:** several checks with different conditions have the same outcome and are really one check.
**How:** check that they have no side effects, combine with logical operators, and extract the result into a named function.
**Watch:** keep them apart if they're independent reasons that happen to coincide today.

## Replace Nested Conditional with Guard Clauses

**When:** one path is the normal flow and others are unusual, but the nesting treats them equally.
**How:** turn each unusual case into an early return or a raised error, starting from the outermost.
**Watch:** run any required cleanup with the language's mechanism: `defer`, `finally`, `using`, or RAII.

## Replace Conditional with Polymorphism

**When:** the same switch on a type appears repeatedly, or a variant modifies a base logic.
**How:** create the types and a factory, move the conditional into a method on the base or interface, then move each branch to its variant. Leave the default where it makes sense.
**Watch:** a single simple switch is fine. Many languages have better options: tagged unions with exhaustive matching, a lookup table, or passing functions. Exhaustive `match` suits a fixed set of variants with new operations; polymorphism suits new variants with fixed operations.

## Introduce Special Case

**When:** many callers check for one value and do the same thing, usually null or "unknown".
**How:** create a special-case object or value with the expected behavior. Add an `isUnknown` check to both, change the checks to use it, then move the behavior into the special case, removing checks when possible.
**Watch:** the classic form is Null Object. Don't use it when absence must be handled differently by callers; an option type may express that better.

## Introduce Assertion

**When:** a condition is assumed, and is only clear from reading the logic.
**How:** add an assertion that documents it.
**Watch:** assert what must be true for a programmer's code to be correct. Don't use it to validate external input, and check whether assertions are disabled in production in this language.

## Separate Query from Modifier

**When:** a function returns a value and also has side effects.
**How:** copy it as a query with its side effects removed. Replace uses of its return value, then remove the return value from the original.
**Watch:** check concurrency; a separate read and write can create a race. An atomic operation that does both, like `pop` or compare-and-swap, is a legitimate exception.

## Parameterize Function

**When:** similar functions differ only in literal values.
**How:** pick one, add a parameter for the literal, and change callers to use it. Adapt the body to handle all cases, then remove the others.

## Remove Flag Argument

**When:** a boolean or literal argument selects behavior and callers pass a constant.
**How:** create an explicit function for each value, and migrate callers. If the logic is tangled, decompose it first.
**Watch:** a flag from computed data, or several combined flags, can be a reasonable parameter; consider an options type.

## Preserve Whole Object

**When:** a caller extracts several values from an object just to pass them on.
**How:** create the new function with the whole object, delegating to the old. Migrate callers, then inline.
**Watch:** this couples the function to the type. If it should stay independent of it, or if a smaller value is its real concept, keep the separate values.

## Replace Parameter with Query

**When:** a parameter can be determined by the function itself, shifting that burden from callers.
**How:** extract the calculation if needed, replace references, and remove the parameter.
**Watch:** the function must stay referentially transparent if it was. Don't introduce a dependency on a global or mutable value.

## Replace Query with Parameter

**When:** a function reaches for a global, a clock or some element it shouldn't depend on, which makes it hard to test or reuse.
**How:** extract the query into a variable, extract the rest into a new function taking a parameter, inline, and migrate.
**Watch:** moves the burden to callers. This is the usual way to inject time and randomness.

## Remove Setting Method

**When:** a field shouldn't change after construction.
**How:** ensure it's set by the constructor, change callers to pass it, remove the setter and make the field immutable.

## Replace Constructor with Factory Function

**When:** you need a better name, a choice of subtype, or a constructor is restricted by the language.
**How:** create a function that calls the constructor, migrate callers, and restrict the constructor's visibility.

## Replace Function with Command

**When:** a function needs undo, a life cycle, parameters built in stages, or a complicated body broken up with shared state.
**How:** create a class with an `execute` method, move the function in and turn its parameters into fields.
**Watch:** most of the time a function or a closure is the better choice. Use a command only when it's actually necessary.

## Replace Command with Function

**When:** a command object does nothing a plain function couldn't.
**How:** extract the creation and the call into one function, move everything into it, and remove the class.
