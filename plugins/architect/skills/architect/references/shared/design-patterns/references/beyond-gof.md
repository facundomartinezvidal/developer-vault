# Beyond the Gang of Four

Hand-written summary, in our own words. GRASP comes from Larman's *Applying UML and Patterns*, Chapters 17 and 25. Null Object and Gateway are covered in *Agile Principles, Patterns, and Practices*, Chapters 25 and 34. The rest is common practice. Not generated from the vault.

## GRASP: who should do this?

Before reaching for a pattern, it often helps to ask which object or module should own a responsibility.

| Principle | Answer |
|---|---|
| Information Expert | Give the responsibility to whoever has the information to fulfill it |
| Creator | Let an object create what it contains, aggregates, or has the data to initialize |
| Controller | A non-UI object receives and coordinates a system operation; it delegates rather than doing the work |
| Low Coupling | Among options, choose the one that adds the fewest dependencies, especially on unstable things |
| High Cohesion | Keep responsibilities focused and related |
| Polymorphism | When behavior varies by type, assign it to the types rather than to a conditional |
| Pure Fabrication | Invent a class outside the domain, such as a repository, when an expert would otherwise lose cohesion |
| Indirection | Put an intermediary between things to decouple them; every level has a cost |
| Protected Variations | Identify points of predicted instability, and put a stable interface around them |

Protected Variations underlies many GoF patterns. Apply it only to variation that's real or likely.

## Other useful patterns

- **Null Object or Special Case:** an object that does nothing or gives a safe default, removing repeated null checks. Avoid it if absence needs a different reaction.
- **Gateway:** an object that wraps access to an external system, with your own interface and types. It helps with testing and replacing vendors. A thin wrapper around one stable call may not be worth it.
- **Dependency Injection:** collaborators are passed in rather than created inside. Plain constructor or function parameters are enough for most code, and containers come at a cost.
- **Repository:** collection-like access to stored objects. It's useful when domain logic should be isolated from persistence. If it only forwards to an ORM, it adds nothing.
- **Value Object:** a small immutable type compared by value, such as money or a date range.
- **Result:** failure as a return value. Use it where the language supports it well.
- **Middleware or Pipeline:** a chain of handlers for cross-cutting concerns such as auth or logging. Most web frameworks provide this.
- **Pub/Sub, Event Bus:** Observer across components. Control flow becomes harder to follow, so use it when the decoupling is really worth it.

## Functional and modern equivalents

| GoF pattern | Often simplified to |
|---|---|
| Strategy, Command, Template Method | A function or closure as a parameter |
| Factory Method, Abstract Factory | A factory function or a map of constructors |
| Iterator | Generators, streams, built-in iteration |
| Decorator | Function wrappers, higher-order functions, language decorators |
| Observer | Events, signals, reactive streams, channels |
| Visitor | Pattern matching on a tagged union |
| Singleton | A module-level value or, better, a single instance passed in |
| State | A tagged union, or a transition table |
| Builder | Named or default arguments, an options struct |
| Adapter | A small function converting one form to another |

## Common anti-patterns

- **God object:** one type knows and does everything.
- **Golden hammer:** one tool or pattern for every problem.
- **Primitive obsession,** **shotgun surgery:** see `refactoring`.
- **Service locator:** dependencies hidden behind a global lookup.
- **Anemic domain:** data in one place, with the rules scattered in services. It's a real cost when the rules are complex, and a fine default in a simple CRUD.
- **Premature abstraction:** the wrong abstraction is often more costly than duplication.
