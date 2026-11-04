---
name: architecture-documentation
description: Documents and diagrams software architecture with the C4 model — system context, container, component and supplementary (deployment, dynamic, landscape) views in Mermaid or Structurizr, chosen for a specific audience and derived from the real system. Use it whenever someone wants an architecture diagram or overview, needs to explain how a system or its services fit together, is onboarding people, preparing a design doc or a presentation for management, or wants the architecture section of a README, even if they don't mention C4. Also covers Spanish requests like "diagrama de arquitectura", "documentá la arquitectura", "explicar cómo está armado el sistema", "armar un diagrama para gerencia", "mapa de servicios". Not for class diagrams of one module, ER diagrams alone, or API reference documentation.
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

Only draw levels that add value. Skip code-level diagrams: they go stale immediately and IDEs generate them on demand. Skip component diagrams unless the container is complex enough that a reader would otherwise be lost.

## 2. Get the abstractions right

The vocabulary is what makes C4 useful, and misuse is its most common error.

- **Person:** a user role.
- **Software system:** the highest level of what delivers value, usually owned by one team. Things you don't own (Stripe, the corporate ERP) are external systems.
- **Container:** something that must be running, or that stores data, for the system to work: a web app, API, worker, database, queue, bucket. It's a deployable or runtime boundary and has nothing to do with Docker: a serverless function counts, and a sidecar may just be infrastructure detail.
- **Component:** a grouping of related code behind an interface, inside one container. It isn't separately deployable.

Frequent mistakes to avoid: drawing a library or framework as a container; showing a shared Postgres server as one box when two systems own separate schemas (or as two when it really is shared, which is itself worth showing); treating each microservice's internals as part of one big diagram.

## 3. Derive it from reality

When there is a repository, build the picture from evidence, in roughly this order: deployment manifests (`docker-compose`, Kubernetes, Terraform, serverless config), then environment variables and client SDKs for external dependencies, then entrypoints and routes, then message topics and queue consumers. Read how things are actually connected. A README describing the intended design may be out of date.

Report what doesn't add up instead of smoothing it over: a service nothing calls, a dependency used in code but absent from the manifests, two services writing to the same tables, or a docs-versus-code mismatch. These findings are often worth more than the diagram.

Keep inference honest. If the code doesn't tell you what a relationship carries or who a user is, mark it as an assumption in the text or leave the detail out. A precise-looking diagram with invented facts is worse than none. Cite the file that supports each non-obvious element.

## 4. Draw it clearly

- **Title** stating type and scope: "Container diagram: Billing Platform".
- **Each element** shows its name, its type, a short responsibility, and for containers and components its technology.
- **Each line** is one-way, labeled with its intent ("publishes invoice events to"), never just "uses". Between containers, add the protocol or technology.
- **A key or legend** whenever shapes or colors carry meaning, and acronyms spelled out for the audience.
- **The system boundary** is drawn so it is clear what is inside and what is external.
- **Aim for about 20 elements or fewer.** If it doesn't fit, split by flow or by subsystem rather than shrinking the text.

For a non-technical reader, drop protocols and technologies and describe relationships in business terms.

Use Mermaid by default, since it renders in GitHub and is reviewable as text; match whatever the repo already uses (Structurizr DSL, PlantUML). `references/c4-mermaid.md` has ready patterns. Check that every diagram is valid before handing it over: quoted labels, unique ids.

## 5. Package and keep it alive

Put each diagram with a few sentences saying what it answers and what it omits on purpose, plus the key decisions and risks that a picture can't carry; link ADRs where they exist. Keep it in the repo next to the code (`docs/architecture/` or the README), as text, so changes show up in review.

Note the date and what the documentation was derived from, and name what will make it go stale first. Offer the smallest check that would catch that, if there is one (for example, a CI step that fails when a service in the compose file is missing from the diagram), and only build it if asked.
