# Moves: functions, variables and statements

Hand-written from *Refactoring* (2nd ed.), Chapters 6–9, in our own words. Each move lists when to use it, how to do it safely, and what to watch out for. The steps are language-neutral; prefer a tool's automated version when it has one. Run the tests after each move.

## Contents

- Extract Function · Inline Function
- Extract Variable · Inline Variable
- Change Function Declaration · Rename Variable or Field
- Split Variable · Encapsulate Variable
- Replace Temp with Query · Replace Derived Variable with Query
- Split Phase · Substitute Algorithm
- Slide Statements · Split Loop · Replace Loop with Pipeline
- Move Statements into Function · Move Statements to Callers · Replace Inline Code with Function Call
- Remove Dead Code

## Extract Function

**When:** you need a moment to work out what a fragment does, or it repeats. The gap between what it does and how it does it is reason enough, whatever its length.
**How:** create a function named for its intent. Copy the fragment. Pass the variables it reads as parameters. A variable it modifies and that's used afterward becomes its return value. Replace the original fragment with a call. Look for other copies.
**Watch:** many outputs usually mean the wrong fragment; try slicing it differently, or apply Split Variable or Replace Temp with Query first. If you can't find a good name, the extraction may not be a real concept.

## Inline Function

**When:** the body says as much as the name, the indirection adds nothing, or a badly split group is easier to re-split after merging.
**How:** check it isn't overridden or polymorphic. Replace each call with the body, adjusting names, one at a time. Delete the definition when no calls remain.
**Watch:** recursion, multiple returns and dynamic calls.

## Extract Variable

**When:** an expression is hard to read. A name explains its part.
**How:** check it has no side effects. Declare an immutable variable with its value, and replace uses one by one.
**Watch:** if the meaning applies beyond this function, extract a function instead.

## Inline Variable

**When:** the name says no more than the expression, or the variable blocks a nearby refactoring.
**How:** check the expression has no side effects and evaluates the same at each use. Make the variable immutable to prove it has one assignment, then replace uses.

## Change Function Declaration

Also covers rename, add or remove a parameter.

**When:** a name doesn't explain the purpose, or the parameters couple the function to more context than it needs.
**How, simple:** when all callers are reachable, change the declaration and all the callers together.
**How, migration:** extract the body to a new function with the new declaration, make the old one delegate to it, migrate callers one by one, and inline and remove the old one. Keep it deprecated if the interface is published.
**Watch:** overrides and implementations of an interface, dynamic dispatch, serialized names and reflection.

## Rename Variable or Field

**When:** you now understand better what the thing is.
**How:** for wide scope or shared data, encapsulate it first, then rename. For a published record field, accept both names during migration.
**Watch:** names exposed in JSON, database columns, configuration, logs and templates are part of a contract.

## Split Variable

**When:** a variable is assigned for two different purposes, excluding loop counters and accumulators.
**How:** rename at the first assignment and make it immutable, update uses until the second assignment, and repeat.

## Encapsulate Variable

**When:** data with wide scope will be moved or its use changed, such as globals, module-level state or public fields.
**How:** create read and write functions, route all access through them, and restrict the data's visibility. Consider returning a copy or a read-only view.
**Watch:** a getter that returns a mutable reference hasn't encapsulated anything.

## Replace Temp with Query

**When:** a temporary holds a computation that other functions need, or blocks an extraction.
**How:** check it's computed once and gives the same result each time. Extract the assignment to a function, and replace uses with calls.
**Watch:** only for computations without side effects, and where repeating them is affordable or cached.

## Replace Derived Variable with Query

**When:** mutable data could instead be calculated, removing the risk of the two going out of sync.
**How:** add an assertion to find where it would differ, write the calculation, confirm, replace reads, and remove the updates.
**Watch:** if the source is immutable and the transformation is a pipeline, a new derived value can be just as good.

## Split Phase

**When:** code deals with two different things in sequence, such as parsing then calculating, or a compiler's stages.
**How:** extract the second phase into a function. Introduce an intermediate data structure as its argument, and move parameters into it. Extract the first phase so it returns that structure.
**Watch:** a good sign is a clear data shape between phases that changes for only one of them.

## Substitute Algorithm

**When:** a clearer way exists, often a library function.
**How:** isolate the algorithm behind one function, get tests around it, and swap the body. If a difference appears, run the old and new together to compare.

## Slide Statements

**When:** related code should sit together, typically before an extraction.
**How:** find where it can go without crossing any interfering side effects, reads or writes, and move it.
**Watch:** ordering with I/O, exceptions and shared state. This is where hidden temporal coupling shows up.

## Split Loop

**When:** one loop does several things, so you must understand all of them to change one.
**How:** copy the loop, delete the different parts from each copy, then consider extracting each.
**Watch:** the performance cost is rarely significant. Measure before you object, and re-merge if it matters.

## Replace Loop with Pipeline

**When:** a loop processes a collection and the language has map, filter, iterators, streams, or comprehensions.
**How:** create a variable for the pipeline, then move each piece of the loop into a stage, top to bottom. Remove the loop.
**Watch:** follow the language's idiom. Very long or side-effecting chains read worse than a loop, and early exit or laziness can change behavior.

## Move Statements into Function

**When:** the same code surrounds every call to a function.
**How:** extract the combination into a new function if there are many callers, migrate them, then inline it to rename if needed.

## Move Statements to Callers

**When:** a function does something that only some callers now need. The boundary has shifted.
**How:** the reverse of the above: extract what stays, then inline the old function into callers.

## Replace Inline Code with Function Call

**When:** inline code does what an existing function already does, and for the same reason. Prefer a library function if there is one.

## Remove Dead Code

**When:** code is confirmed to be unused. Version control keeps the history, so don't comment it out.
**How:** check for reflection, dynamic dispatch, exported APIs and entry points in configuration. Delete it and run the tests.
