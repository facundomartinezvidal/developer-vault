---
name: domain-driven-design
description: Models and reviews complex business domains using ubiquitous language, bounded contexts, context maps, subdomains and aggregates. Use when business terms conflict, teams share a tangled model, a monolith needs business boundaries, legacy integrations distort the model, or business invariants need explicit consistency and transaction decisions. Also applies to requests such as "cómo modelo este dominio", "contextos delimitados", "agregados" and "lenguaje ubicuo". For dependency direction, layers or folder structure alone, use clean-architecture.
---

# Domain-Driven Design

This skill carries a personal chapter-by-chapter study of Evans's *Domain-Driven Design* as reference files. Use it to **model**, **review** or **explain**. Its added value is precision about what Evans really says and the judgment to apply only what pays off here.

## First: is DDD worth it here?

DDD is an investment that pays off when the business rules are genuinely complex and will keep evolving. Say so directly when it doesn't fit: CRUD back-offices, thin data pipelines, and generic subdomains get a simple approach or a bought product, and pushing aggregates and factories onto them only adds ceremony. Effort should concentrate where the business differentiates itself, and a system usually has only a few such places. A valid answer to "how do I apply DDD here?" is "only in this one part".

## Strategic before tactical

Most of DDD's value is strategic, and most misuse comes from starting with `Entity` and `Repository` base classes. Work in this order unless the request is clearly narrower:

1. **Language.** Listen for the terms the business uses, and where they conflict. A term meaning two things ("product", "account", "customer") is a clue to investigate, not enough evidence to split a context. Check whether the meanings imply different rules, lifecycles, owners or reasons to change. If you can't reach domain experts, list what you'd ask them, and mark your model as a hypothesis.
2. **Bounded contexts.** Draw them around where one model and one language hold consistently. Don't derive them from database tables, technical layers, or a list of nouns. A context is a model boundary, not a deployment unit. It can be implemented by modules in a monolith; modules can also organize concepts inside one context. A subdomain describes a business problem; a bounded context defines where a particular model applies. Their boundaries need not match one to one.
3. **Context map.** Map how contexts and teams actually relate today, using the real relationship patterns: Shared Kernel, Customer/Supplier, Conformist, Anticorruption Layer, Open Host Service, Published Language, Separate Ways. The choice depends on team power and communication as much as on technology, so identify who controls each side and the upstream/downstream direction where applicable. A REST call or an event does not establish the relationship pattern. An ACL protects a local model through semantic translation; do not prescribe one for every integration regardless of cost. Describe the present reality before proposing a future one.
4. **Distillation.** Identify the core domain, then supporting and generic subdomains. Best people and deepest modeling go to the core. For generic parts, recommend buying or using an off-the-shelf solution first.
5. **Tactical model,** only where it pays off, inside a context.

## When the problem is language

Help discover and test the language, not just rename classes or deliver a glossary. For a disputed term, capture the speaker, an example action, the states that matter and a counterexample where another meaning changes the decision. Propose a working definition with a concrete scenario for experts to confirm or reject; mark unanswered definitions as hypotheses. Different meanings can coexist in different contexts, and an ambiguous word alone does not justify splitting deployment or creating another context.

When code or tests are in scope, show how an agreed term changes a model operation or an example of expected behavior. Do not claim agreement without experts' confirmation. A short modeling conversation and a few executable examples can be more useful than a complete context map.

## Tactical heuristics

- **Value objects by default.** Make something an entity only when identity and lifecycle matter to the business. Immutable values remove whole classes of bugs.
- **Design aggregates from invariants.** State the rule, the operation that could break it and the state that must change atomically. That sets the boundary, not the object graph or the UI. Prefer small aggregates and references to other aggregates by ID. One aggregate per transaction is a useful default, not permission to weaken a strict business rule. If a rule spans roots, consider a reservation, a different boundary or a justified multi-aggregate transaction. Ask which lag, rejection or compensation the business accepts; do not infer tolerance for credit or payment from tolerance for stock shortages.
- **Close the concurrency gap.** A method that checks a balance on an in-memory object protects only that instance. For a shared limit, show how competing writes are serialized or rejected: a version check with bounded retry and fresh validation, a lock with all contenders following the same protocol, or a conditional atomic update. Saying "use a transaction" without isolation or conflict handling leaves the race open. Two orders can each fit the available credit and exceed it together; explain why the chosen mechanism prevents both from succeeding. Specify whether the rule concerns each order's amount or total outstanding exposure, and mark an interpretation as an assumption if the request is ambiguous.
- **Give asynchronous flows a failure path.** When recommending events or reservations, describe the relevant commit/publication boundary, duplicate handling, and what happens when a later step fails. A transactional outbox is an option when state and message publication must survive failures together. Reservation release or expiry must preserve the rule during retries and delayed messages. Domain events do not require a broker, event sourcing or CQRS.
- **Behavior belongs in the model where a rich model pays off.** Show the business decision or state transition on the entity, value object or aggregate that owns it, rather than only setters and a service script. Application services coordinate loading, transactions and delivery; a domain service expresses a business operation that belongs to no single object. The model enforces business rules; persistence supplies the concurrency mechanism that makes them hold across instances.
- **Repositories exist per aggregate root,** speak the domain's language, and hide persistence. A generic CRUD repository for every table is not this pattern.
- **Name things in the ubiquitous language,** in code, tests and conversation. When the model and language diverge, one of them needs refactoring.

## Modes

Choose the smallest useful response for the question. A tactical question does not need a full context map; a strategic question does not need entity classes. Keep observed facts, working assumptions and questions for domain experts distinct. Ask only questions that would change the recommendation, and continue with explicit assumptions when possible.

**Modeling:** for strategic work, identify the conflicting terms and rules, candidate contexts and ownership, important relationships and translations, and where modeling investment pays off. Use a language table or a Mermaid context map when it clarifies the decision. Justify proposed boundaries with concrete evidence and state what would change them. For tactical work, name the aggregate roots, owned state, business operations and invariants; explain the consistency and concurrency decisions for the relevant flow. If implementation is requested or needed to make the design concrete, use the user's language and framework and show behavior on the model plus the persistence contract that protects it. Propose an incremental path when changing an existing system.

**Review:** inspect the actual operations, model types, transaction boundaries and integration mappings before judging names or folders. Look for duplicated rules, leaking meanings, oversized aggregates (contention, excessive loading), undersized boundaries (strict rules without atomic enforcement), and transaction scripts wearing DDD names. Report the location or evidence, the business failure or change cost, and a concrete correction. Preserve intentional differences between contexts and simple CRUD where it works; missing DDD patterns are not findings by themselves.

**Explain:** give the relevant definition, its practical meaning and one realistic example. Consult the reference for claims about Evans; distinguish its guidance from later practices. Correct the misconception relevant to the question rather than listing every possible misuse.

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
