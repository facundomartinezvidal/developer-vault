## Ubiquitous language across agents

Use one project-specific business vocabulary consistently across architect,
developer, reviewer, code-investigator and any delegated agent. Read the
requirements, accepted glossary, domain model and project guidance before naming
business concepts. Business terms may be English, Spanish or the requirements'
language; preserve their agreed meaning and spelling across code, designs,
documentation, tests, reviews and handoffs. The user's conversation language does
not by itself rename the domain.

Include the relevant approved terms and their source in delegated tasks and
handoffs. Reuse an existing glossary; do not create a separate vocabulary per
agent or require a new document for a small change. If requirements use conflicting
terms, ask the user which meaning/name applies before introducing or renaming
that concept. In reviewer consultations, return that question to the coordinator.
Do not silently translate terms or introduce synonyms. A vocabulary change is a
shared design/contract decision, not a local cleanup; preserve accepted contracts
and existing code until the change is approved.

Distinguish domain words from technical roles: `PublicacionRepository` can preserve
`Publicacion` while using the English technical suffix `Repository`; `findById`
is technical, while `publicar` can be the agreed business operation. Do not
require every project to use Spanish or to adopt these example names. Follow an
explicitly agreed project language policy; surface a material conflict instead
of silently overriding it. These naming rules do not expand any role's write
permissions or authorize translating user-facing text.
