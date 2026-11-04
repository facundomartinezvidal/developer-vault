# Principles for making architecture decisions

How to generate options, how much to commit, and how to learn cheaply before committing.

## Contents

- [Design It Twice](#design-it-twice)
- [Reversibility](#reversibility)
- [Keep Options Open: Policy vs. Details](#keep-options-open-policy-vs-details)
- [Software Trends (Seen Through Complexity)](#software-trends-seen-through-complexity)
- [Coconuts Don't Cut It](#coconuts-dont-cut-it)
- [Good-Enough Software](#good-enough-software)
- [The Requirements Pit](#the-requirements-pit)
- [Tracer Bullets](#tracer-bullets)
- [Prototypes](#prototypes)

## Design It Twice

> Designing software is hard, so it's unlikely that your first thoughts about how to structure a module or system will produce the best design.

**Source:** *A Philosophy of Software Design*, Chapter 11.

### What it means in practice

For any important design decision (a class's interface, a module's split, a system's architecture), sketch **at least two radically different approaches** before choosing. They should be different, not small variations on one idea. Then compare them on:

- Which has the simpler interface?
- Which is more general-purpose?
- Which interface allows a more efficient implementation?

Often the best result combines ideas from several options, or the comparison shows a better option you hadn't thought of. It costs an hour or two for a class, and maybe days for a system. That's small compared to living with the wrong design. Ousterhout notes that smart people often skip this step, because they're used to their first idea being good enough. In large systems it usually isn't.

### Example

Designing an API for "upload large files":
1. **Single request**: `POST /files` with the whole body. Simple, but no resume and it times out on large files.
2. **Chunked sessions**: `POST /uploads` → `PUT /uploads/{id}/parts/{n}` → `POST /uploads/{id}/complete`. Resumable and parallel.
3. **Pre-signed URL**: the server returns a signed object-storage URL, and the client uploads directly. The server never handles the bytes.

The comparison picks (3) for the common case, with (2) as the fallback, an answer the first sketch wouldn't have reached.

### Related

- Prototypes — a cheap way to compare alternatives when reasoning alone isn't enough.

## Reversibility

> There Are No Final Decisions. — Tip 18

**Source:** *The Pragmatic Programmer*, Topic 11 (also Tip 19, "Forgo Following Fads").

### What it means in practice

Requirements, vendors, users and fashions all change, often faster than the code. A decision that's expensive to reverse ("we're an Oracle shop", "everything is a microservice") turns into a cage. So:

- Treat decisions as written in sand. Hide third-party choices behind your own abstractions so changing your mind costs an adapter, not a rewrite.
- Make *architecture* flexible too. The book's history of fashion (monolith → client/server → n-tier → microservices → serverless → …) shows that whichever one is current will change.
- **Forgo following fads.** You can't predict the future, so don't bet the design on any one of them. Keep it ready for any of them.

### Example

```java
// Irreversible: S3 types leak through every service
public S3Object loadContract(String key) { return s3.getObject(bucket, key); }

// Reversible: one interface, swap S3 for GCS/Azure/local disk in one class
public interface DocumentStore { InputStream open(DocumentId id); }
class S3DocumentStore implements DocumentStore { ... }
```

### Where it applies

- Keep Options Open: Policy vs. Details — Martin's architecture-level version: a good architect maximizes the number of decisions *not* made.
- database is a detail, web is a detail, frameworks are details — Clean Architecture's case studies in keeping specific decisions reversible.
- clean boundaries — wrapping vendor APIs is how reversibility is implemented in code.

### Related

- Coconuts Don't Cut It — don't adopt a practice just because it's fashionable.

## Keep Options Open: Policy vs. Details

> The strategy behind that facilitation is to leave as many options open as possible, for as long as possible.

**Source:** *Clean Architecture*, Chapter 15.

### What it means in practice

Architecture is the *shape* of a system — its division into components, their arrangement, and how they communicate — and that shape exists to make the system easy to **develop, deploy, operate, and maintain**, not to make it work (plenty of terribly structured systems work fine). Martin weighs the four goals unequally: operational problems can usually be bought off with hardware, while development and maintenance (the "spelunking" through code plus the risk of breaking something) cost people, which is the expensive resource. A good architecture also makes operation *visible*: use cases are first-class, obvious elements of the code.

Every system splits into **policy** (business rules — where the value lives) and **details** (database, web server, framework, protocols, DI container, IO devices). The architect's job is to make the policy ignorant of the details, so those decisions can be postponed until there's real information to make them with — or made, swapped, and experimented with cheaply later. If the company already "decided" on a database or framework, a good architect pretends it hasn't and keeps the code shaped so it could still change. "A good architect maximizes the number of decisions not made."

Martin also insists that architects keep programming: they can't guide a design if they don't feel the problems it causes.

### Example: shipping the checkout rules before picking the stack

A team building a marketplace writes `PlaceOrder`, pricing, and stock-reservation logic against an `OrderRepository` interface and plain request/response objects. For the first two months orders live in an in-memory map and the "UI" is a test suite. When load numbers finally come in, they pick Postgres (not the MongoDB the original plan assumed) and REST over GraphQL — and neither choice touches the business rules. Martin's historical analogues: device-independent IO in the 1960s (programs written against an abstract "unit record" device ran unchanged on cards or tape), and replacing hard-wired cylinder/head/sector disk addresses with relative addresses.

### Related

- Reversibility

## Software Trends (Seen Through Complexity)

> Whenever you encounter a proposal for a new software development paradigm, challenge it from the standpoint of complexity.

**Source:** *A Philosophy of Software Design*, Chapter 19.

### What it means in practice

Ousterhout judges popular practices by one question: do they reduce complexity?

| Trend | Verdict |
|---|---|
| **Interface inheritance** | Good. One interface, many implementations, so knowledge is reused. |
| **Implementation inheritance** | Use with caution. It creates dependencies between parent and child, and knowledge spreads across the hierarchy. Prefer composition. |
| **Agile development** | Mixed. Incremental development is good, but agile can encourage **tactical** programming. Increments should be *abstractions*, not features. |
| **Unit tests** | Good. They make refactoring possible, which is how design improves. |
| **TDD** | Against. It focuses on making tests pass, not on finding the best design (it's tactical). Exception: write a failing test before fixing a bug. |
| **Design patterns** | Good when a pattern fits. Bad when applied by force, because not every problem needs a pattern. |
| **Getters and setters** | Avoid where possible. They're shallow methods that expose implementation, which is the opposite of information hiding. |

### Example

A team adds an `AbstractBaseService<T>` with generic CRUD that every service extends (implementation inheritance), and auto-generates getters and setters for every field. Under Ousterhout's lens, both increase complexity: the base class's choices leak into every subclass, and the getters expose every field as interface.

### Related

- Coconuts Don't Cut It — adopting practices without checking whether they help.

## Coconuts Don't Cut It

> Do What Works, Not What's Fashionable. — Tip 87

**Source:** *The Pragmatic Programmer*, Topic 50 (also Tip 88, "Deliver When Users Need It").

### What it means in practice

The title refers to the cargo cults of the Pacific. Islanders built runways and control towers out of coconuts and straw, copying what they had seen during the war, and expected planes full of cargo to land. Teams do the same when they copy Spotify's squads, Google's monorepo or Netflix's microservices without the context that made those work.

- **Context matters.** Try ideas, keep what works *for you*, and drop the rest. There's no one methodology that fits every team.
- **The goal is continuous delivery**: deliver when users need it, not on a ritual schedule. If you can't deploy on demand, work out what's in the way and fix that.

### Example

A five-person startup adopts Kubernetes, service mesh and twelve microservices "like Netflix". Deploys get slower, and debugging needs three dashboards. The coconut-free alternative is a modular monolith with one deploy pipeline. Split it only when a real scaling or team boundary shows up.

### Related

- Reversibility — "forgo following fads".
- Software Trends (Seen Through Complexity) — Ousterhout looks at fashionable practices just as skeptically.

## Good-Enough Software

> Make Quality a Requirements Issue. — Tip 8

**Source:** *The Pragmatic Programmer*, Topic 5.

### What it means in practice

Perfect software doesn't exist. "Good enough" doesn't mean sloppy. It means **good enough for its users, its future maintainers, and your own peace of mind**, and *the users* help decide what that means. So:

- **Involve users in the trade-off.** How good does this need to be, and how soon? Many would take an imperfect version today over a perfect one next year. Treat the quality level as a requirement and discuss it, don't assume it.
- **Know when to stop.** Like a painter who knows when the painting is finished, don't keep polishing. Over-embellishment and over-refinement can ruin a working program.
- Some systems have legal or safety requirements (medical devices, avionics, payments), and "good enough" there means something much stricter.

### Example

An internal admin dashboard: the ops team accepts no mobile layout and a 2-second load, as long as it ships this sprint. The public checkout page gets a performance budget, accessibility audits and cross-browser tests. Both are "good enough", for different users.

### Related

- The Requirements Pit — quality level is negotiated like any other requirement.
- Tracer Bullets — ship a thin working version early and improve it with feedback.

## The Requirements Pit

> No One Knows Exactly What They Want. — Tip 75 &nbsp;·&nbsp; Requirements Are Learned in a Feedback Loop. — Tip 77

**Source:** *The Pragmatic Programmer*, Topic 45 (Tips 75–80).

### What it means in practice

Requirements aren't lying around waiting to be gathered. They're buried under assumptions, misunderstandings and politics, and they're **learned through feedback**. A programmer's job is to **help people understand what they want** (Tip 76):

- **Ask questions and explore edge cases.** Restate the requirement and show mockups and prototypes. Every round of feedback refines the shared understanding.
- **Work with a user to think like a user** (Tip 78). Spend a day doing their job.
- **Policy is metadata** (Tip 79). "Only supervisors can see salary data" is a *policy* that will change. Implement the general mechanism (access rules), and keep the specific policy as configurable data.
- **Requirements vs. documentation.** User stories and index cards are reminders for a conversation, not contracts. Avoid overspecifying.
- **Watch out for scope creep.** Make every change's impact visible.
- **Maintain a project glossary** (Tip 80), so users and developers mean the same thing by the same word.

### Example

Request: "Users must be able to export their data." Questions: which data, in what format, for whom (the user, an admin, regulators)? How often, and how large? Answer: a GDPR right-of-access export, JSON, delivered within 30 days, possibly 2 GB. That's an async job with an email link, not a "download CSV" button.

### Where it applies

- knowledge crunching — Evans's version: developers and domain experts learn the model together, in a feedback loop.
- ubiquitous language — the project glossary grown into a shared language used in code.
- externalize configuration — "policy is metadata" implemented as configuration.

### Related

- Prototypes and Tracer Bullets — the fastest feedback loops for requirements.
- Good-Enough Software — quality level is a requirement too.

## Tracer Bullets

> Use Tracer Bullets to Find the Target. — Tip 20

**Source:** *The Pragmatic Programmer*, Topic 12.

### What it means in practice

When requirements are vague or the technology is new, don't specify everything and then build it in one go. Instead, build a thin, **real**, end-to-end slice through every layer (UI → API → domain → database → deploy) that does one tiny thing. It works like a tracer round in the dark: you see right away where it lands, and you adjust.

Unlike a prototype, tracer code is **kept**. It's production-quality skeleton code with tests and error checks, just very little functionality. The benefits:
- Users see something real early.
- Developers get a structure to hang new work on.
- Integration problems show up on day one, not at the end.
- You always have something to demo, and progress is visible.

If the bullet misses (the slice reveals a wrong assumption), adjust. Small slices are cheap to change.

### Example

Building a document-signing product: week 1 is "upload a PDF → it's stored → a signer gets an email link → clicking it shows the PDF". There's no signature yet, no templates and a plain UI, but the CI/CD pipeline, auth, storage, email provider and frontend are all wired up and deployed.

### Related

- Prototypes — the difference matters: prototypes are thrown away, tracer code is kept.
- Good-Enough Software
- The Requirements Pit

## Prototypes

> Prototype to Learn. — Tip 21

**Source:** *The Pragmatic Programmer*, Topic 13.

### What it means in practice

A prototype answers **one specific question** as cheaply as possible, and then it's thrown away. The value is in what you *learn*, not in the code. You can prototype risky or unproven things: architecture, a new library, performance, UI and UX, algorithms, external interfaces. You can do it with code, but also with Post-it notes, whiteboards, or a drawing tool.

Because it's disposable, a prototype can ignore correctness, completeness, robustness and style. That's also the danger. Make it *very* clear to everyone, especially managers, that the prototype is not the product. If there's a risk it will be shipped anyway, use a tracer bullet instead.

### Example

"Can we generate 10k invoice PDFs in under a minute?" A 50-line script with hard-coded data compares two PDF libraries on one laptop. Answer: library A takes 40 s and library B takes 6 min. The script gets deleted, the decision gets recorded in the engineering daybook, and production code is written properly with library A.

### Related

- Tracer Bullets — kept, not thrown away.
- Design It Twice — Ousterhout: compare alternative designs before committing. A prototype is one way to compare them.
- The Requirements Pit
