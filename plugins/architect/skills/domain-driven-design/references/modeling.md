# Modeling and the ubiquitous language

Chapters 1–3 and 8–11: learning the domain with experts, the shared language, and refactoring toward deeper insight.

## Contents

- [Knowledge Crunching](#knowledge-crunching)
- [Ubiquitous Language](#ubiquitous-language)
- [Model-Driven Design](#model-driven-design)
- [Hands-On Modelers](#hands-on-modelers)
- [Making Implicit Concepts Explicit](#making-implicit-concepts-explicit)
- [Refactoring Toward Deeper Insight](#refactoring-toward-deeper-insight)
- [Breakthrough](#breakthrough)
- [Analysis Patterns](#analysis-patterns)
- [Design Patterns as Domain Patterns](#design-patterns-as-domain-patterns)

## Knowledge Crunching

> Effective domain modelers are knowledge crunchers. They take a torrent of information and probe for the relevant trickle.

**Source:** *Domain-Driven Design*, Chapter 1.

### What it means in practice

Developers and domain experts build a model **together**: the developers usually lead, sketching objects and walking through scenarios, and the experts correct them until the model can carry the real cases. Evans lists five ingredients:

1. **Bind the model to the implementation early.** A crude prototype with no UI and no persistence, driven by tests, makes the model concrete.
2. **Cultivate a language based on the model.** This becomes the Ubiquitous Language.
3. **Make the model knowledge-rich.** Objects carry behavior and rules, not just data. The model is not a database schema.
4. **Distill it.** Drop concepts that don't pull their weight, as well as add new ones.
5. **Brainstorm and experiment.** Try many variants out loud and in code.

Two common failure modes miss this:
- **Waterfall:** analysts model, programmers code, and knowledge only flows one way.
- **Iterative but shallow:** the team builds whatever feature is asked for without ever abstracting the principles behind it. Software built this way works, but new features never fall out "for free" as corollaries of old ones.

Knowledge also leaks: people leave and code gets outsourced. So a team practices **continuous learning** and keeps a stable core of people who know the domain. A **deep model** is what this process produces over time: a model that goes beyond "find the nouns" and captures business rules and policies, including the ones experts apply without being aware of them.

### Example: overbooking hidden in a booking service

```java
// Before: a domain rule buried in an if, invisible to anyone reading the model
public BookingResult book(Seat request, Flight flight) {
    if (flight.bookedSeats() + 1 > flight.capacity() * 1.05) return BookingResult.rejected();
    ...
}

// After crunching: the experts call it an overbooking policy, so the model says so
public BookingResult book(Seat request, Flight flight) {
    if (!overbookingPolicy.allows(flight, request)) return BookingResult.rejected();
    ...
}
```

The policy is now something experts can name, review and change (per route, per fare class) without a developer having to translate an `if` back into business terms. Evans's version of this example is cargo bookings on a ship voyage.

### Related

- Ubiquitous Language
- Model-Driven Design
- Making Implicit Concepts Explicit — the techniques for digging hidden rules out.
- Refactoring Toward Deeper Insight
- Breakthrough
- Analysis Patterns — someone else's crunched knowledge.
- Hands-On Modelers

## Ubiquitous Language

> Use the model as the backbone of a language. Commit the team to exercising that language relentlessly in all communication within the team and in the code.

**Source:** *Domain-Driven Design*, Chapter 2.

### What it means in practice

Without a shared language, experts speak business jargon and developers speak class names, and every conversation needs a translator. Each translation loses meaning, and the model in the code drifts away from the model in people's heads. A Ubiquitous Language closes that gap:
- The same terms appear in speech, diagrams, documents, class names, method names and tests.
- **A change in the language is a change in the model.** If people start saying "fulfillment" instead of "shipping", the code gets renamed to match.
- Experts object to terms that are awkward or wrong. Developers object to terms that are ambiguous or inconsistent.

**Modeling out loud** is the main tool: describe scenarios aloud using only model terms. If a sentence sounds clumsy, the model is probably wrong. Try alternative phrasings, then push the better one back into the diagrams and code.

On documents, Evans's view is that **the code and the spoken language are the primary carriers of the model.** Diagrams should be small sketches that convey the essentials. Written documents should complement code and speech rather than duplicate them, and a document that is no longer actively used should be dropped. The language is only *ubiquitous* within one Bounded Context (`context-mapping.md`): different contexts have their own dialects.

### Example: one sentence, two models

> "When a customer's **subscription renews**, we **charge** the **default payment method**; if it fails, the subscription goes **past due** and we **retry** three times before **cancelling**."

```java
// The code reads like the sentence
subscription.renew(clock.today());                    // emits RenewalDue
Charge charge = billing.charge(subscription.defaultPaymentMethod(), subscription.renewalAmount());
if (charge.failed()) subscription.markPastDue(retryPolicy.schedule(charge));
```

The version this replaces had `UserPlanRecord.status = 3` and a nightly `ProcessPendingJob`. No expert could read it, and none of its words appeared in any conversation.

### Related

- Knowledge Crunching
- Model-Driven Design
- Bounded Context (`context-mapping.md`) — the scope within which one language holds.
- Intention-Revealing Interfaces (`supple-design.md`) — the language at method and class level.
- Context Map (`context-mapping.md`) — names of contexts become part of the language too.
- Modules (`building-blocks.md`) — module names are part of the language.
- Analysis Patterns
- Conformist (`context-mapping.md`)
- Continuous Integration (of a Model) (`context-mapping.md`)
- Domain Service (`building-blocks.md`)
- Domain Vision Statement (`distillation.md`)
- Highlighted Core (`distillation.md`)
- Making Implicit Concepts Explicit
- Published Language (`context-mapping.md`)
- Refactoring Toward Deeper Insight
- System Metaphor (`large-scale-structure.md`)

## Model-Driven Design

> Design a portion of the software system to reflect the domain model in a very literal way, so that mapping is obvious.

**Source:** *Domain-Driven Design*, Chapters 3 and 5 (Modeling Paradigms).

### What it means in practice

Many projects keep an "analysis model" (diagrams for understanding the business) separate from the design that actually gets coded. The two drift apart, the analysis model becomes useless, and the code loses the insight. Model-Driven Design demands **one model that serves both purposes**: it explains the domain, it can be implemented naturally, and it backs the Ubiquitous Language.
- Class names, responsibilities and associations are taken straight from the model.
- If the model can't be implemented cleanly, **change the model** until it can, rather than letting the code drift away from it.
- A code change may be a model change, and that change has to flow back into the conversations and diagrams.

The paradigm matters. **Objects** dominate because they map naturally onto domain concepts and are widely understood. Rule engines, workflow engines and similar non-object paradigms can be used, but the language must stay unified across them so the overall design remains model-driven. Purely procedural code makes this binding very hard. Evans's contrast is a PCB tool written as mechanical text-file processing versus the same tool built from `Net`, `Bus` and `RuleType` objects.

### Example: procedural vs. model-driven refund rules

```java
// Mechanistic: correct, but the business concepts are nowhere
if (order.getStatus() == 4 && daysBetween(order.getShippedAt(), now) <= 30 && !order.getFlags().contains("FINAL_SALE")) { ... }

// Model-driven: the expert's own concepts carry the logic
if (order.isDelivered() && order.returnWindow().includes(today) && !order.isFinalSale()) { ... }
```

Here `ReturnWindow` is a Value Object (`building-blocks.md`) the experts already talked about ("30-day return window"). It now exists in the code, so changing the policy to 60 days for premium members is one obvious edit.

### Related

- Knowledge Crunching
- Ubiquitous Language
- Hands-On Modelers — the people side of keeping model and code bound.
- Layered Architecture (`building-blocks.md`) — the isolation that makes a literal model possible.
- Entity (`building-blocks.md`), Value Object (`building-blocks.md`), Domain Service (`building-blocks.md`), Modules (`building-blocks.md`) — the building blocks that express the model.
- Supple Design (`supple-design.md`) — the next step: a model-driven design that is also pleasant to change.
- Declarative Design (`supple-design.md`) — the "holy grail" version of the binding.

## Hands-On Modelers

> Any technical person contributing to the model must spend some time touching the code, whatever primary role he or she plays on the project.

**Source:** *Domain-Driven Design*, Chapter 3.

### What it means in practice

If the people who model never code and the people who code never model, the model loses touch with what is implementable and the code loses the insight behind it. The fix works in both directions:
- **Modelers code.** An architect who designs the domain model also pairs on it, reviews it and writes some of it.
- **Coders model.** Every developer takes part in model discussions and talks to domain experts. Anyone changing code has to learn to express the model through it, because a "small refactoring" can silently destroy the model.

Large projects still need technical leads who coordinate high-level design. They just can't be detached from the code. Evans comes back to this in Chapter 17: strategic designers must stay in contact with the application teams, the "objects are specialists, developers are generalists" (`large-scale-structure.md`) rule.

### Example: a "design handoff" that goes wrong

An architect delivers a UML model of `Policy`, `Coverage` and `Claim` for an insurance platform and moves to another project. The developers find that the `Coverage` hierarchy doesn't fit the ORM. They flatten it into a `coverage_type` column with a switch statement, and the concept of coverage riders quietly disappears. A hands-on modeler would have been in that conversation. Either the model would have been reshaped to fit the code, or the code would have kept the riders.

### Related

- Model-Driven Design
- Knowledge Crunching
- Strategic Design Decisions (`large-scale-structure.md`) — the same rule for architecture teams.
- Refactoring Toward Deeper Insight

## Making Implicit Concepts Explicit

> The key to distinguishing a process that ought to be made explicit from one that should be hidden is simple: Is this something the domain experts talk about, or is it just part of the mechanism of the computer program?

**Source:** *Domain-Driven Design*, Chapter 9.

### What it means in practice

Deep models come from noticing concepts that are already present but hidden: in conversations, in awkward code, in rules buried inside conditionals. Evans's techniques for finding them:
- **Listen to language.** Experts use a term the code doesn't have, or correct your phrasing. A word that keeps coming up is probably a concept.
- **Scrutinize awkwardness.** Where the design is clumsy and code is hard to explain, something is usually missing.
- **Contemplate contradictions.** Two experts saying incompatible things usually means two concepts, or two contexts (`context-mapping.md`).
- **Read the book.** Accounting, logistics and insurance have established theory. Also read analysis patterns.
- **Try, try again.** Expect several wrong models before a good one. Each attempt still embeds knowledge.

Three categories of concepts that object-oriented "nouns and verbs" thinking tends to miss:
1. **Constraints.** Start by giving a constraint a named method. When it needs data foreign to its host, gets duplicated across classes, or dominates conversations while hiding in procedural code, make it an object.
2. **Processes the experts talk about.** Model them as a Service (`building-blocks.md`), or as a Strategy when there are alternatives. Purely mechanical steps stay hidden.
3. **Specifications (`building-blocks.md`):** rules that test whether an object meets some criteria.

### Example: a refund constraint that wants out

```java
// Hidden: the rule lives inside Order and needs data Order shouldn't know
public boolean canRefund() {
    return status == DELIVERED
        && daysSince(deliveredAt) <= (customer.isPremium() ? 60 : 30)
        && !lines.stream().anyMatch(l -> l.category().equals("digital"))
        && fraudScore < 0.7;
}

// Explicit: the business calls it the refund policy, so model it
public interface RefundPolicy { RefundDecision evaluate(Order order, CustomerTier tier, RiskScore risk); }
```

The support and risk teams now argue about `RefundPolicy` by name. Different marketplaces get different implementations, and `Order` loses its dependency on fraud scoring.

### Related

- Knowledge Crunching
- Ubiquitous Language — listening to language is the main detector.
- Specification (`building-blocks.md`)
- Domain Service (`building-blocks.md`)
- Assertions (`supple-design.md`) — explicit constraints stated as invariants.
- Refactoring Toward Deeper Insight
- Breakthrough
- Analysis Patterns
- Bounded Context (`context-mapping.md`)
- Design Patterns as Domain Patterns

## Refactoring Toward Deeper Insight

> If you wait until you can make a complete justification for a change, you've waited too long.

**Source:** *Domain-Driven Design*, Part III introduction and Chapter 13.

### What it means in practice

Classic refactoring, as in Fowler's catalog, is driven by code smells. It's essential, but it's only half the story. Evans adds **refactoring driven by domain insight**: the code may look tidy, but the model is shallow, the experts' language doesn't match it, or new requirements don't fit naturally. Three things to focus on:

1. **Live in the domain.**
2. **Keep looking at things a different way.**
3. **Maintain an unbroken dialog with domain experts.**

How it unfolds:
- **Initiation:** a trouble spot, which can be awkward code or a language mismatch. Spotting it is the hardest part.
- **Exploration teams:** a few developers plus a domain expert brainstorm for an hour, sketch, sleep on it and reconvene. Keep it self-organized, small in scope and short, and use it to exercise the Ubiquitous Language.
- **Prior art:** domain literature, analysis patterns, design patterns that fit the model, and established formalisms.
- **Timing:** don't demand full justification up front, because the cost of an awkward design is invisible but real.

Refactor when:
- the design doesn't express the team's current understanding of the domain;
- important concepts are implicit and you see how to make them explicit;
- you see a chance to make an important part suppler (`supple-design.md`).

Don't refactor the day before a release, and don't introduce a "deeper model" you couldn't get a domain expert to use.

### Example

The code for shipment tracking is clean and well tested. But ops keeps saying "a shipment can be **split** at the warehouse", and the code models it as cancelling one shipment and creating two. Nothing smells, yet the model is wrong. A two-session exploration with the warehouse lead produces `Shipment.split(parcels)` with consignment lineage. Late-split reporting, partial delivery notifications and carrier reconciliation all become straightforward.

### Related

- Breakthrough — the occasional jump this steady process produces.
- Knowledge Crunching
- Making Implicit Concepts Explicit
- Supple Design (`supple-design.md`)
- Analysis Patterns
- Design Patterns as Domain Patterns
- Hands-On Modelers
- Abstract Core (`distillation.md`)
- Core Domain (`distillation.md`)
- Ubiquitous Language

## Breakthrough

> This sort of breakthrough is not a technique; it is an event.

**Source:** *Domain-Driven Design*, Chapters 8 and 13 ("Crisis as Opportunity").

### What it means in practice

The return on refactoring isn't linear. Small refactorings add up steadily and hold off entropy. But continuous refinement also gives the team a clearer and clearer view, and sometimes that clarity tips into a sudden insight. The model reshapes itself at a deeper level, and **versatility and explanatory power jump while complexity drops**. Evans compares it to punctuated equilibrium: long plateaus broken by short bursts of rapid change.

How to handle one:
- **Recognize it.** It often begins as a crisis: the model can't handle a new requirement, or the experts' language suddenly doesn't match the code.
- **Weigh the risk honestly.** A breakthrough usually means a big refactoring. Evans's team took a week to rebuild a loan-syndication model mid-release because the deeper model was worth it.
- **Don't chase it.** You can't schedule breakthroughs. Keep making the small refactorings that make them possible, and focus on basics: a model that expresses the experts' concepts.
- **Expect a cascade.** One deeper model makes the next insights easier to see.

### Example: from "user permissions" to "memberships"

A B2B SaaS product grows a tangle of `user.isAdmin`, `user.teamIds`, `user.billingContact` and special cases for agencies that manage several client accounts. Each feature adds another flag. One day, while discussing agencies, someone notices that the experts never talk about "users with permissions". They talk about **people who hold memberships in organizations, each with a role**. Rebuilding around `Person`, `Organization` and `Membership(role)` takes a painful sprint. Afterwards, agencies, guest access and seat-based billing all fall out of the model naturally instead of each needing its own hack.

### Related

- Refactoring Toward Deeper Insight — the steady process breakthroughs come out of.
- Knowledge Crunching — a deep model is the payoff.
- Supple Design (`supple-design.md`) — breakthroughs both need and produce it.
- Making Implicit Concepts Explicit — the missing concept is usually what the breakthrough reveals.
- Evolving Order (Large-Scale Structure) (`large-scale-structure.md`) — the same rhythm at the large-scale structure level.
- Choosing a Model Context Strategy (`context-mapping.md`)
- Core Domain (`distillation.md`)

## Analysis Patterns

> Analysis patterns are groups of concepts that represent a common construction in business modeling. It may be relevant to only one domain or it may span many domains.

**Source:** *Domain-Driven Design*, Chapter 11 (quoting Fowler, *Analysis Patterns*, 1997).

### What it means in practice

Design patterns solve technical design problems. Analysis patterns are **reusable model fragments for business domains**: a few objects that represent a concept experienced modelers have already worked out. Fowler's catalog includes accounts and entries, posting rules, party, and observation and measurement. Good analysis patterns also discuss implementation and long-term maintenance consequences, not just diagrams.

How to use them:
- They are **starting points**, not out-of-the-box solutions. Feed them into knowledge crunching and refactor toward your own domain.
- The result often resembles the pattern but is adapted, and sometimes it only bears the pattern's influence.
- **Keep the concept intact when you borrow the name.** If you call something a "posting rule", it should mean what Fowler meant. That protects the embedded experience and gives the Ubiquitous Language widely understood terms. If the meaning drifts, rename it.
- Analysis patterns differ from framework reuse: a framework is a complete working whole, while an analysis pattern is a kit of model fragments focused on the hardest decisions.

Evans's example takes an interest-accrual system and restructures it with Fowler's **Accounts, Entries and Posting Rules**. Interest is posted as entries into accounts, and posting rules fire to create derived entries, so the ledger behaves like real accounting.

### Example: marketplace payouts as accounts and entries

```java
// Instead of mutating seller.balance in five services:
public class Account { AccountId id; List<Entry> entries; Money balance() { /* sum */ } }
public record Entry(Money amount, Instant at, EntryType type, TransactionId tx) {}

// Posting rule: when a sale entry is posted to "seller receivable", derive the fee entry
public class MarketplaceFeeRule implements PostingRule {
    public List<Entry> process(Entry sale) {
        return List.of(new Entry(sale.amount().times(feeRate).negate(), sale.at(), FEE, sale.tx()));
    }
}
```

Every balance becomes auditable, and refunds and chargebacks are just more entries. Finance recognizes the model immediately, because it's the one their own discipline uses.

### Related

- Knowledge Crunching
- Design Patterns as Domain Patterns
- Refactoring Toward Deeper Insight — analysis patterns are "prior art" for it.
- Making Implicit Concepts Explicit — "read the book".
- Supple Design (`supple-design.md`) — drawing on established formalisms.
- Ubiquitous Language
- Generic Subdomains (`distillation.md`) — published models are an option for generic parts.
- Knowledge Level (`large-scale-structure.md`)
- Published Language (`context-mapping.md`)

## Design Patterns as Domain Patterns

> The only requirement is that the pattern should say something about the conceptual domain, not just be a technical solution to a technical problem.

**Source:** *Domain-Driven Design*, Chapter 12.

### What it means in practice

Some GoF patterns can serve as **domain patterns**: they apply to both model and implementation, because the structure they describe also exists in the business concepts. Using them this way means shifting the emphasis from technical flexibility to **expressing a concept**.
- **Strategy (a.k.a. Policy).** The design-pattern view is "swap algorithms". The domain view is "factor a rule or process out of what it governs and make it a named concept". Evans's example is route-finding policies, fastest vs. cheapest.
- **Composite.** Domain objects really made of objects of the same kind, like routes built from legs and sub-routes. The point is to flesh out *operational* behavior so that every level can answer the same questions, such as total time or total cost, rather than just nesting data.
- **Flyweight is the counter-example.** It is a pure implementation option for widely shared Value Objects (`building-blocks.md`) and corresponds to nothing in the model. That makes it a fine design pattern but not a domain pattern.

Evans doesn't compile a list of eligible patterns. The test is whether the pattern says something about the domain, and he declines to rule any pattern out (even Interpreter). As with any pattern, apply it only when it's needed.

### Example: commission policies and product bundles

```java
// Strategy as a domain concept the sales team names
public interface CommissionPolicy { Money commissionFor(Sale sale); }
public class TieredCommission implements CommissionPolicy { ... }       // "tiered plan"
public class FlatRateCommission implements CommissionPolicy { ... }     // "flat plan"

// Composite with real domain operations at every level
public interface CatalogItem { Money price(); Weight shippingWeight(); boolean inStock(); }
```

Sales ops can say "move EMEA to the tiered plan", and that sentence maps to one line of configuration.

### Related

- Analysis Patterns
- Making Implicit Concepts Explicit — processes and policies as objects.
- Specification (`building-blocks.md`) — Composite and Interpreter applied to rules.
- Refactoring Toward Deeper Insight
- Value Object (`building-blocks.md`)
