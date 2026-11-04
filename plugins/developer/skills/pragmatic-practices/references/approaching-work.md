# Approaching a piece of work

Learning requirements, cutting thin slices, prototyping, estimating, and deciding what is good enough.

## Contents

- [The Requirements Pit](#the-requirements-pit)
- [Tracer Bullets](#tracer-bullets)
- [Prototypes](#prototypes)
- [Estimating](#estimating)
- [Good-Enough Software](#good-enough-software)
- [Don't Outrun Your Headlights](#dont-outrun-your-headlights)
- [Reversibility](#reversibility)
- [Listen to Your Lizard Brain](#listen-to-your-lizard-brain)
- [The Essence of Agility](#the-essence-of-agility)

## The Requirements Pit


**Source:** *The Pragmatic Programmer*, Topic 45 (Tips 75–80).

### What it means in practice

Requirements aren't lying around waiting to be gathered. They're buried under assumptions, misunderstandings and politics, and they're **learned through feedback**. A programmer's job is to **help people discover what they need** (Tip 76):

- **Ask questions and explore edge cases.** Restate the requirement and show mockups and prototypes. Every round of feedback refines the shared understanding.
- **Work alongside users to see things as they do** (Tip 78). Spend a day doing their job.
- **Policy is metadata** (Tip 79). "Only supervisors can see salary data" is a *policy* that will change. Implement the general mechanism (access rules), and keep the specific policy as configurable data.
- **Requirements vs. documentation.** User stories and index cards are reminders for a conversation, not contracts. Avoid overspecifying.
- **Watch out for scope creep.** Make every change's impact visible.
- **Maintain a project glossary** (Tip 80), so users and developers mean the same thing by the same word.

### Example

Request: "Users must be able to export their data." Questions: which data, in what format, for whom (the user, an admin, regulators)? How often, and how large? Answer: a GDPR right-of-access export, JSON, delivered within 30 days, possibly 2 GB. That's an async job with an email link, not a "download CSV" button.

### Where it applies

- knowledge crunching — Evans's version: developers and domain experts learn the model together, in a feedback loop.
- ubiquitous language — the project glossary grown into a shared language used in code.
- Externalize Configuration (`tooling-and-automation.md`) — "policy is metadata" implemented as configuration.

### Related

- Prototypes and Tracer Bullets — the fastest feedback loops for requirements.
- Good-Enough Software — quality level is a requirement too.
- Communicate! (`working-with-people.md`)
- Estimating
- Working Together (`working-with-people.md`)

## Tracer Bullets


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
- Don't Outrun Your Headlights
- The Essence of Agility
- Pragmatic Starter Kit (`tooling-and-automation.md`) — the pipeline the first bullet runs through.
- Stone Soup and Boiled Frogs (`working-with-people.md`) — a working slice persuades people better than a proposal.
- Good-Enough Software
- Estimating
- The Requirements Pit

## Prototypes


**Source:** *The Pragmatic Programmer*, Topic 13.

### What it means in practice

A prototype answers **one specific question** as cheaply as possible, and then it's thrown away. The value is in what you *learn*, not in the code. You can prototype risky or unproven things: architecture, a new library, performance, UI and UX, algorithms, external interfaces. You can do it with code, but also with Post-it notes, whiteboards, or a drawing tool.

Because it's disposable, a prototype can ignore correctness, completeness, robustness and style. That's also the danger. Make it *very* clear to everyone, especially managers, that the prototype is not the product. If there's a risk it will be shipped anyway, use a tracer bullet instead.

### Example

"Can we generate 10k invoice PDFs in under a minute?" A 50-line script with hard-coded data compares two PDF libraries on one laptop. Answer: library A takes 40 s and library B takes 6 min. The script gets deleted, the decision gets recorded in the engineering daybook, and production code is written properly with library A.

### Related

- Tracer Bullets — kept, not thrown away.
- Don't Outrun Your Headlights
- Estimating — prototypes reduce the uncertainty in an estimate.
- Listen to Your Lizard Brain — prototyping is a way out when you're stuck.
- The Requirements Pit

## Estimating


**Source:** *The Pragmatic Programmer*, Topic 15.

### What it means in practice

- **Match units to accuracy.** "130 working days" sounds more precise than "about six months", even when it isn't. Choose units that signal how confident you are: days, then weeks, then months.
- **Where estimates come from:** first understand what's being asked, then build a model of the system, break it into components, give each a value, and calculate. Then compare with what actually happened, to improve the next estimate. **Keep a record** of how your estimates turn out.
- **Ranges, not points.** Use optimistic, most-likely and pessimistic values (PERT), so the uncertainty is visible.
- **Iterate the schedule with the code.** Experience is the best source of estimates, so re-estimate after each increment. The first estimate is the least informed one.
- When asked for an estimate on the spot, the right answer is **"I'll get back to you"**.

### Example

"How long to add SSO?" → "I'll get back to you this afternoon." Breakdown: SAML library spike (1–3 d), IdP config for the pilot customer (0.5–2 d), account linking (2–5 d), admin UI (1–3 d). Result: about 2–3 weeks, re-estimated after the spike.

### Where it applies

- algorithm speed — Topic 39: estimating the *resources* an algorithm needs, using Big-O.
- Tracer Bullets and The Essence of Agility — short cycles produce the actual data that improves estimates.

### Related

- Prototypes — a spike reduces the biggest uncertainty.
- Communicate! (`working-with-people.md`) — how an estimate is presented changes how it's heard.
- Take Responsibility (`working-with-people.md`) — commit with the risks stated.
- The Requirements Pit

## Good-Enough Software


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
- Take Responsibility (`working-with-people.md`)
- Stone Soup and Boiled Frogs (`working-with-people.md`)

## Don't Outrun Your Headlights


**Source:** *The Pragmatic Programmer*, Topic 27 (also Tip 43).

### What it means in practice

A driver at night shouldn't go faster than they can stop within the distance the headlights reach. In software, the headlights are how far ahead you can see with confidence, and that's usually not very far. So:

- **Take small, deliberate steps.** After each one, check feedback (a test, a REPL, a demo to a user) before taking the next.
- **Feedback comes in many forms:** unit tests, user demos, real-world results. The goal is to *learn* before you commit more.
- **Avoid fortune-telling.** Don't design for a future you can't see ("we'll need multi-currency someday"). Make the code replaceable instead, so the future is cheap to handle whenever it actually arrives.
- **Black swans happen.** The tech you bet on may vanish, and the one you dismissed may take over. That's one more reason to keep things reversible.

### Example

Instead of building a "plugin system for future payment providers":

```java
// Today: one provider, behind an interface you own (cheap, replaceable)
interface PaymentGateway { ChargeId charge(Money amount, CardToken card); }
class StripeGateway implements PaymentGateway { ... }
// When a second provider is a real requirement, add it — the interface already makes that cheap.
```

### Related

- Reversibility
- Tracer Bullets and Prototypes — small steps toward a target you can't see yet.
- The Essence of Agility

## Reversibility


**Source:** *The Pragmatic Programmer*, Topic 11 (also Tip 19).

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

- keep options open — Martin's architecture-level version: a good architect keeps as many decisions as possible open.
- database is a detail, web is a detail, frameworks are details — Clean Architecture's case studies in keeping specific decisions reversible.
- clean boundaries — wrapping vendor APIs is how reversibility is implemented in code.

### Related

- Don't Outrun Your Headlights — avoid fortune-telling: make the code replaceable instead of predicting the change.
- Version Control (`tooling-and-automation.md`)
- Externalize Configuration (`tooling-and-automation.md`)

## Listen to Your Lizard Brain


**Source:** *The Pragmatic Programmer*, Topic 37.

### What it means in practice

Experience builds instincts below conscious thought. When code feels wrong, or a task feels unexpectedly hard to start (fear of the blank page), that discomfort is information. Something in the design or the requirements is off, even if you can't say what yet.

What to do with it:
- **Stop and give it time.** Step away, take a walk, sleep on it. Let your nonconscious mind work.
- **Externalize it.** Draw it, explain it to a colleague or a rubber duck, or write it in your engineering daybook.
- **Prototype.** Tell yourself "this is a throwaway" and start typing. You'll quickly find the thing that was bothering you. Then delete the prototype and design properly.
- Notice the same instinct when reading *other people's* code. Not just whether it's wrong, but what feels odd about it.

### Example

Adding a "simple" feature to the billing module keeps feeling hard: every change needs three special cases. Instead of forcing it, you sketch the flow on paper and realize "invoice" is being used for two different concepts (draft quote vs. legal invoice). That's the real problem.

### Related

- Prototypes — the book's remedy for being stuck.

## The Essence of Agility


**Source:** *The Pragmatic Programmer*, Topic 48.

### What it means in practice

You can't *buy* agility or follow a process to *become* agile. Agility is the way you respond to change. The Agile Manifesto's values (individuals and interactions, working software, customer collaboration, responding to change) have no fixed recipe. Hunt & Thomas boil it down to a loop:

1. **Work out where you are.**
2. **Make the smallest meaningful step** toward where you want to be.
3. **Evaluate where you end up, and fix anything you broke.**

Repeat until done, and apply the loop *recursively*: to the project, to each feature, to each line of code, and to the process itself. Agility also depends on good design, because the loop only works if the code is easy to change.

### Example

A team's two-week sprints have turned into ritual: stand-ups as status reports, and a retro that changes nothing. Applying the loop to the process itself: measure where it hurts (lead time is 9 days, most of it waiting for review), take the smallest step (a review SLA plus pairing on risky PRs), evaluate after two weeks, and keep or drop the change.

### Related

- Don't Outrun Your Headlights — small steps with feedback.
- Tracer Bullets
- Pragmatic Teams (`working-with-people.md`)
- Estimating
- Working Together (`working-with-people.md`)
