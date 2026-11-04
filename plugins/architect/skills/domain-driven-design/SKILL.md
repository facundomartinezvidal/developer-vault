---
name: domain-driven-design
description: Applies Eric Evans's Domain-Driven Design to model complex business software — ubiquitous language, bounded contexts and context maps, anticorruption layers, core vs. generic subdomains, aggregates, entities, value objects, repositories, domain services, and when DDD isn't worth it. Use it whenever someone struggles with a tangled domain model, a giant class everyone edits, teams stepping on each other, one term meaning different things, how to split a monolith along business lines, integrating with a legacy system, where consistency boundaries or transactions should go, or how to model a business rule, even if they never say "DDD". Also covers Spanish requests like "cómo modelo este dominio", "contextos delimitados", "agregados", "lenguaje ubicuo", "dividir el monolito", "qué es core", "qué va en cada servicio". Not for layer or folder structure by itself, where Clean Architecture is the better fit.
---

# Domain-Driven Design

This skill carries a personal chapter-by-chapter study of Evans's *Domain-Driven Design* as reference files. Use it to **model**, **review** or **explain**. Its added value is precision about what Evans really says and the judgment to apply only what pays off here.

## First: is DDD worth it here?

DDD is an investment that pays off when the business rules are genuinely complex and will keep evolving. Say so directly when it doesn't fit: CRUD back-offices, thin data pipelines, and generic subdomains get a simple approach or a bought product, and pushing aggregates and factories onto them only adds ceremony. Effort should concentrate where the business differentiates itself, and a system usually has only a few such places. A valid answer to "how do I apply DDD here?" is "only in this one part".

## Strategic before tactical

Most of DDD's value is strategic, and most misuse comes from starting with `Entity` and `Repository` base classes. Work in this order unless the request is clearly narrower:

1. **Language.** Listen for the terms the business uses, and where they conflict. A term meaning two things ("product", "account", "customer") usually signals a context boundary. If you can't reach domain experts, list what you'd ask them, and mark your model as a hypothesis.
2. **Bounded contexts.** Draw them around where one model and one language hold consistently. Don't derive them from database tables, technical layers, or a list of nouns. A context is not automatically a microservice, and not a module: it's a model boundary, which can live inside a monolith at first.
3. **Context map.** Map how contexts and teams actually relate today, using the real relationship patterns: Shared Kernel, Customer/Supplier, Conformist, Anticorruption Layer, Open Host Service, Published Language, Separate Ways. The choice depends on team power and communication as much as on technology, so ask who controls each side. Describe the present reality before proposing a future one.
4. **Distillation.** Identify the core domain, then supporting and generic subdomains. Best people and deepest modeling go to the core. For generic parts, recommend buying or using an off-the-shelf solution first.
5. **Tactical model,** only where it pays off, inside a context.

## Tactical heuristics

- **Value objects by default.** Make something an entity only when identity and lifecycle matter to the business. Immutable values remove whole classes of bugs.
- **Design aggregates from invariants.** Ask which rules must hold true at the end of every transaction; that sets the boundary, not the object graph or the UI. Keep them small, reference other aggregates by ID, and change one per transaction by default. Rules across aggregates are usually allowed to lag and are resolved by events or processes. Ask the business how long a lag is acceptable; it's often longer than developers assume.
- **Behavior belongs in the model.** An anemic model with all rules in services is a procedural design in disguise. Use a domain service only when an operation truly belongs to no single object.
- **Repositories exist per aggregate root,** speak the domain's language, and hide persistence. A generic CRUD repository for every table is not this pattern.
- **Name things in the ubiquitous language,** in code, tests and conversation. When the model and language diverge, one of them needs refactoring.

## Modes

**Modeling:** deliver the language table with terms that differ across contexts, the contexts with their responsibilities, a context map (Mermaid) with named relationship patterns, the core/supporting/generic classification, and, for the core only, the aggregates with their invariants. Say which open questions domain experts need to answer. Propose an incremental path; a big-bang rewrite is rarely the answer.

**Review:** for existing code, look for model problems: duplicated concepts, false cognates, leaking language between contexts, aggregates that are too large (contention, huge loads) or too small (invariants enforced in services), transaction scripts wearing DDD names, integration without translation. Report what each one costs the team, the fix, and what should be left alone.

**Explain:** give Evans's definition when the reference has it, what it means in practice, one realistic example, and how it relates to neighbouring patterns. Correct common misreadings: a bounded context isn't a microservice or a module; an entity isn't an ORM row; DDD isn't a folder structure.

## Limits of the source

Evans predates much of today's practice: Event Storming, event sourcing, CQRS and domain events as first-class patterns come from later work. Use them when relevant, but say they're not from this reference, and don't attribute them to Evans. Likewise, "reference by ID, one aggregate per transaction" is later community guidance (Vernon) that sharpens Evans's rules.

## Reference files

Read the one that matches the topic before answering in depth; each has a table of contents, so jump to the section you need.

| File | Read when the topic is… |
|---|---|
| `references/context-mapping.md` | boundaries, splitting a monolith, team relationships, integrating with legacy or third parties, translation |
| `references/distillation.md` | what is core vs. generic, where to invest, build vs. buy, focusing a large model |
| `references/building-blocks.md` | entities, value objects, services, modules, aggregates, factories, repositories, specifications, isolating the domain |
| `references/modeling.md` | working with experts, ubiquitous language, keeping model and code together, finding hidden concepts, refactoring toward insight |
| `references/supple-design.md` | making a model expressive and safe to change: interfaces, side-effect-free functions, assertions, contours |
| `references/large-scale-structure.md` | very large models, shared structure across teams, responsibility layers, how strategic decisions get made |
