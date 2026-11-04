# Principles across language families

Hand-written; not generated from the vault. Many reference examples are in Java. This maps the underlying ideas onto other languages, so that advice is translated rather than copied. It lists examples, not the whole of any language, and versions change: follow the project's existing style, and check the current documentation.

## The same idea, in different forms

| Idea | Class-based OO (Java, C#, Kotlin) | Dynamic (Python, Ruby, JS/TS, PHP) | Systems (Go, Rust, C, C++, Zig) | Functional (Haskell, Elixir, Clojure, F#, Erlang) |
|---|---|---|---|---|
| Expected failure | Exceptions, or `Result` in some styles | Exceptions; `Promise` rejections; TS unions | Go `error`, Rust `Result`, C return codes, C++ exceptions or `expected` | `Either`, `{:ok, _}` tuples; supervisors for crashes |
| Absence | `Optional`, nullable types | `None`, `nil`, `undefined`, TS strict null | `Option`, pointers, Go zero values | `Maybe`, `nil` |
| Interface | `interface` | Duck typing, protocols, TS structural types | Go implicit interfaces, Rust traits, C++ concepts, C function pointers | Type classes, protocols, behaviours |
| Variants | Sealed types, polymorphism | Classes, tagged objects, TS unions | Rust `enum`, Go interfaces with type switches, C++ `variant` | Algebraic data types, pattern matching |
| Sharing behavior | Composition, inheritance | Composition, mixins | Embedding, traits, templates | Functions, higher-order functions, macros |
| Resource cleanup | try-with-resources, `using` | `with`, `ensure`, `finally` | `defer`, RAII and `Drop` | Bracket functions, process lifecycle |
| Immutability | `final`, records | Convention, frozen objects, `const` | `const`, Rust default | Default |
| Concurrency | Threads, virtual threads, tasks | Event loop, async, processes; a GIL may apply | Goroutines, async, threads | Actors, processes, STM |
| Grouping | Packages, classes | Modules, files | Packages, crates, headers | Modules, namespaces |
| Dependency injection | Constructor, container | Parameters, a module-level default | Parameters, interfaces | Passing functions, config |

## Translating common advice

- **"Keep functions small"** applies everywhere, but idiomatic Go's explicit error checks make functions longer, and that's normal there. Judge by whether a function does one thing, rather than by lines.
- **"Prefer exceptions to error codes"** (Clean Code) was written against returned integers that callers forget. Result types and checked error values keep failures visible and are the right form where they're idiomatic. Don't add exceptions to Go, or `Result` wrappers to everyday Python.
- **"Don't return null"** is partly solved by the type system in languages with `Option` or strict null checks. Lean on it.
- **"Replace conditional with polymorphism"** versus exhaustive pattern matching: with a fixed set of variants and many operations, a match the compiler checks is often clearer. With new variants added often, polymorphism fits.
- **Design patterns** often reduce to language features: Strategy to a function argument, Iterator to generators, Singleton to a module, Decorator to a wrapper or `@decorator`, Command to a closure, Observer to events or channels. Use the simple form unless the structure earns its cost.
- **Classes and SOLID:** in languages without classes, read "class" as a cohesive module with its type. The reasons, like one reason to change and depending on abstractions, still hold.
- **Getters and setters:** avoid mechanical accessors in languages with properties, or where public fields on plain data are normal.
- **Inheritance:** absent in Go and Rust by design. Composition is the default.

## By type system

- **Static:** make illegal states unrepresentable, so the compiler enforces rules. Run the type checker as part of verification. Avoid escapes such as `any`, unchecked casts and `unsafe`, or explain them.
- **Gradual (TypeScript, Python with type hints):** match the project's strictness. Types can be wrong at runtime, so validate external data at the boundary.
- **Dynamic:** refactoring tools and types give fewer guarantees, so rely on tests. Look for dynamic dispatch, reflection and metaprogramming before you rename anything.

## By memory model

- **Garbage-collected:** you still own non-memory resources such as files, sockets and locks, and leaks through long-lived references.
- **Ownership (Rust):** work with the borrow checker rather than cloning everything or reaching for `unsafe`. Fighting it may point to a design issue.
- **Manual (C, C++):** prefer RAII and smart pointers where available, establish clear ownership, and run sanitizers. Treat every bound as something to check.

## Finding the tools

| Ecosystem | Look for | Usual commands (check the project first) |
|---|---|---|
| JS/TS | `package.json` scripts, lockfile | `npm test`, `pnpm test`, `tsc --noEmit`, `eslint` |
| Python | `pyproject.toml`, `uv.lock`, `tox.ini` | `pytest`, `ruff`, `mypy`, `pyright` |
| Go | `go.mod` | `go test ./...`, `go vet`, `gofmt`, `golangci-lint` |
| Rust | `Cargo.toml` | `cargo test`, `cargo clippy`, `cargo fmt` |
| JVM | `pom.xml`, `build.gradle` | `./mvnw test`, `./gradlew test` |
| .NET | `*.csproj`, `*.sln` | `dotnet test`, `dotnet format` |
| Ruby | `Gemfile` | `bundle exec rspec`, `rubocop` |
| PHP | `composer.json` | `vendor/bin/phpunit`, `phpstan` |
| C/C++ | `CMakeLists.txt`, `Makefile` | `ctest`, `make test`, sanitizers |
| Swift | `Package.swift`, `*.xcodeproj` | `swift test`, `xcodebuild test` |
| Any | `Makefile`, `justfile`, `.github/workflows`, Docker files | Use the exact commands CI runs |

Prefer the project's wrapper scripts and pinned versions: they match CI.
