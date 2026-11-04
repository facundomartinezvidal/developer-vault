---
name: architecture-decisions
description: Guides significant technical decisions from requirements to a written record — identifying the quality attributes and constraints that matter, comparing real options on trade-offs, recommending one, and writing an Architecture Decision Record (ADR). Use it whenever someone is choosing between technologies or approaches with lasting consequences (monolith vs. services, which database, queue or broker, build vs. buy, sync vs. async, multi-tenancy, a migration), asks "should we use X?", needs to justify a choice to a team, or wants to write, update or supersede an ADR — even if they never say "ADR" or "architecture". Also covers Spanish requests like "qué conviene usar", "X o Y", "ayudame a decidir", "documentá esta decisión", "justificar la elección", "registrar la decisión". Not for small reversible choices such as naming or a library that is easy to swap.
---

# Architecture Decisions

A good decision here is one the team can still understand, defend and revisit in two years. The common failure is not picking the wrong technology; it is picking one without saying what it was optimized for, what was given up, or what would make the choice wrong. This skill exists to surface exactly those things.

## 1. Decide how much process this deserves

Weight the effort by how costly the decision is to reverse.

- **Easy to reverse** (one module, swappable behind an interface): answer in a few lines and stop. A written record would be noise.
- **Costly to reverse** (data model, core platform, service split, a public contract, a vendor lock-in): go through the steps below and write an ADR.

If a costly decision can be made reversible cheaply, or deferred until there is real information, that is often the best recommendation. Say so, and say what would trigger making it. See `references/decision-principles.md` for reversibility and keeping options open.

## 2. Establish the drivers

Recommendations made without drivers are opinions. Pull these from the request, the repo and existing docs before asking anything:

- **The change or problem** that forces a decision now. If nothing does, question whether it has to be made yet.
- **Quality attributes in priority order.** Trade-offs only resolve when attributes are ranked, because you rarely get all of them. Make them measurable: "p95 under 300 ms at 200 req/s" beats "fast"; "a new payment provider ships in a week" beats "extensible".
- **Hard constraints:** team size and skills, budget, deadlines, compliance, what is already running.
- **Scale that is real:** today's numbers and a plausible 12–24 month horizon. Don't design for a hypothetical.

Ask only for what would change the answer, at most a few questions. If the user wants progress or can't answer, proceed with explicit assumptions and name which one, if wrong, would flip the recommendation. Keep facts you verified visibly separate from assumptions you made, and never present an invented number as a requirement.

## 3. Compare real options

Compare two to four options that someone could genuinely choose. Include the simplest thing that could work, and "do nothing" or "extend what we have" whenever those are viable, because they are the options most often skipped and most often right. A strawman alternative added only to make the favourite look good wastes the reader's time.

Evaluate each option against the ranked drivers, and also its **operational cost**: who runs it, how it fails, what it takes to migrate in and out. A table works well for the comparison, but the reasoning behind the deciding rows belongs in sentences.

## 4. Recommend and commit

State one recommendation, and don't hide behind "it depends". Then give:

- **Why it wins**, tied to the top drivers.
- **What it costs**, honestly, including what gets worse.
- **What would change your mind:** the specific signal or threshold (traffic, team size, a new requirement) that should reopen the decision. This turns a "never" into a checkable condition.
- **The cheapest way to validate it**, if there is real uncertainty: a spike, a prototype or a load test with a pass/fail criterion.

If the decision belongs to someone else, or hinges on business facts you don't have, say what is missing rather than pretending the technical analysis settles it.

## 5. Write the ADR

Use `assets/adr-template.md` when the repo has no format of its own.

**Look first.** Search for existing records (`docs/adr/`, `doc/adr/`, `docs/decisions/`, `doc/arch/`, `architecture/`, files named `adr-*` or `NNNN-*`). When there are some, follow their format, location, language and numbering, since consistency is what makes the log usable. Otherwise suggest `docs/adr/NNNN-short-title.md`.

What makes the record useful:

- **One decision per record**, one or two pages, written for a future developer who wasn't in the room.
- **Context states the forces as facts,** including the uncomfortable ones (deadline, team skills, politics). Hindsight can't recover these, and they are the part future readers need most.
- **Decision uses active voice:** "We will…".
- **Consequences list the negative and neutral ones too.** A record listing only benefits is a sales pitch.
- **Status is `proposed` unless the user tells you it has been agreed.** Recording a decision as accepted when nobody has accepted it misrepresents the team's position.
- **Records are immutable and numbers are never reused.** To reverse a decision, write a new record and change only the old one's status, adding a link back from the new one. The old reasoning stays because knowing why something was once right is often what prevents repeating it.
- **Say how much of the old decision survives.** Use `Superseded by ADR-NNNN` only when the old decision no longer applies at all. If it stays in force for some cases, use `Partially superseded by ADR-NNNN`, and state in the new record exactly what still holds. Otherwise a reader who sees "superseded" concludes the old approach is gone when most of the system may still run on it.
- **An accepted record only states what was decided.** When the team has told you the decision, the Decision section contains that decision and nothing you added. Implementation details that you think follow from it (a routing mechanism, a specific limit, a tool) go under a "Pending" or "Proposed details" heading, because people will later read the Decision section as something the team agreed to.

Write the record to a file when you are working in a repository, and leave code changes out of it unless asked.
