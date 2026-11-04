---
name: architecture-documentation
description: Documents software architecture for a specific audience using C4 context/container/component views, flow or deployment diagrams, and focused class diagrams when type relationships explain the design. Use for architecture overviews, onboarding, stakeholder presentations, "diagrama de arquitectura", "documentá cómo está armado" or a requested view of an established domain model. Derive diagrams from evidence and distinguish current design from proposals. Not for inventing business rules, API reference docs or ER diagrams alone.
---

# Architecture Documentation

Documentation is worth what it changes in the reader's understanding, and it stays worth something only while it is true. Produce the least that answers the reader's question, with every statement traceable to the system.

## 1. Start from the audience

Ask who will read it if you can't tell, because that picks the level. If you have to guess, say which reader you assumed.

| Reader and question | Produce |
|---|---|
| Executives, non-technical stakeholders: what is this and who depends on it? | **System context** only, in business language |
| New developers, operators: what runs, and how do the pieces talk? | **Context + container** (enough for most teams) |
| Developers working in one complex service: how is it organized inside? | **Component**, for that one container |
| How a specific flow works across pieces | **Dynamic** or sequence diagram, for that one flow |
| Where it runs, for operators and security | **Deployment** |
| How several systems relate across the organization | **System landscape** |
| How a few types collaborate or express an established domain model | **Focused class diagram**, with only the relevant relationships |

Choose the smallest set of views that answers the question; the table is a default, not a requirement to produce every view. Reuse a supplied view if it is sufficient and correct it only where evidence requires. Code-level diagrams usually add maintenance cost; use them when explicitly useful to the request. Skip component diagrams unless a reader needs that internal detail.

## 2. Get the abstractions right

The vocabulary is what makes C4 useful, and misuse is its most common error.

- **Person:** a user role.
- **Software system:** a unit that delivers value to users. Choose and state the system of interest; external means outside that boundary, not necessarily outside the company. Team ownership is a useful clue, not a rule that every team or bounded context is a system.
- **Container:** an application or data store: a web app, API, worker, database schema, queue or bucket. It is a logical runtime boundary, not a Docker container or a physical server. A team-controlled schema on managed RDS or a bucket on S3 can be inside the system even though a provider operates the infrastructure. Keep runtime instances and physical hosting in the deployment view.
- **Component:** a grouping of related code behind an interface, inside one container. It isn't separately deployable.

Avoid drawing a library as a running application, or deriving logical data ownership solely from a shared physical server. Separate schemas can represent distinct logical stores; shared access to the same data is a dependency worth showing. Declare which logical stores and responsibilities the view represents. Do not mix every microservice's internals into one container view.

## 3. Derive it from reality

First establish whether the requested view describes the current system, a proposal, or a particular environment. Build it from deployment/runtime evidence, configuration, entrypoints, clients and message consumers; compare these with documentation and its date. A development compose file establishes local topology, not production. Source code shows supported paths, not which feature flag or transport is enabled there. Resolve conflicting evidence by scope, provenance and recency; do not silently choose one source as universally authoritative.

Report contradictions and missing evidence rather than smoothing them over: a configured dependency absent from manifests, shared writes, or a docs-versus-code mismatch. No inbound call found in the inspected files means an unknown invocation path, not proof that a service is unused; batch schedules, external callers and deployments may live elsewhere. Distinguish observed coupling from a design defect and describe the practical consequence before recommending change.

Keep known facts, inferences and unknowns distinct in both diagram and accompanying text. Do not draw an assumed relationship with the same certainty as a verified one. If protocol, identity, deployment or ownership is unknown, label it unknown or omit the detail and ask the question that would resolve it. Cite `file:line` or the supplied source for non-obvious elements and contradictions. Produce the useful verified portion rather than refusing the whole task because one edge is uncertain.

## 4. Draw it clearly

- **Title** stating type and scope: "Container diagram: Billing Platform".
- **Each element** shows its name, type and a short responsibility. Add technology for containers/components when verified; mark unknown details rather than guessing.
- **Each line** is one-way and labeled with its intent ("publishes invoice events to"), not just "uses". Between containers, add the verified protocol or technology; label missing evidence explicitly when the relationship itself is known.
- **A key or legend** whenever shapes or colors carry meaning, and acronyms spelled out for the audience.
- **The system boundary** is drawn so it is clear what is inside and what is external.
- **Aim for about 20 elements or fewer.** If it doesn't fit, split by flow or by subsystem rather than shrinking the text.

For a non-technical reader, drop protocols and technologies and describe relationships in business terms.

Use Mermaid by default as reviewable text; match the repository's established format and the target renderer. `references/c4-mermaid.md` has patterns and validation guidance. Check labels, IDs, boundaries and correspondence with the evidence. When a renderer is available, render the exact artifact and inspect it for parsing errors, clipped labels and ambiguous edges. Record the tool/result; a syntax review or a successful parse alone is not a successful visual inspection. If rendering is unavailable, state that limitation without claiming the diagram was rendered or is validated everywhere.

A class diagram is a supplementary code/model view, not another name for a C4 component view. Use one when the request or an important relationship warrants it. Show the relevant types, responsibilities, cardinalities and ownership using `classDiagram` (or the repository's notation). Distinguish composition, references and inheritance; do not infer lifecycle ownership from a foreign key or draw inheritance merely because types share fields. Avoid dumping every member from an ORM. If the business meaning is disputed, document the hypothesis and use domain modeling to settle it rather than making the diagram look authoritative.

## 5. Package and keep it alive

Put each diagram with a few sentences saying what it answers and what it omits on purpose, plus the key decisions and risks that a picture can't carry; link ADRs where they exist. Keep it in the repo next to the code (`docs/architecture/` or the README), as text, so changes show up in review.

Note the date and what the documentation was derived from, and name what will make it go stale first. Offer the smallest check that would catch that, if there is one (for example, a CI step that fails when a service in the compose file is missing from the diagram), and only build it if asked.
