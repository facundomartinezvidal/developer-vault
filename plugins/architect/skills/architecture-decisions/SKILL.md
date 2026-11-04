---
name: architecture-decisions
description: Compares consequential technical options against explicit constraints and quality attributes, or records an agreed decision in an Architecture Decision Record (ADR). Use for "qué conviene usar", costly technology or deployment choices, build vs. buy, migrations, and creating or superseding ADRs. Distinguish advice from recording what a team already accepted. Not for ordinary naming, formatting or small local design choices.
---

# Architecture Decisions

A good decision here is one the team can still understand, defend and revisit in two years. The common failure is not picking the wrong technology; it is picking one without saying what it was optimized for, what was given up, or what would make the choice wrong. This skill exists to surface exactly those things.

## 1. Decide how much process this deserves

First distinguish the task:

- **Advice:** compare and recommend. Produce a written ADR only if requested or clearly part of the deliverable; otherwise answer directly, even for a consequential choice.
- **Record an agreed decision:** preserve what the team actually agreed, inspect existing records and document it. Do not reopen the choice or add implementation commitments unless asked. Flag a material contradiction as an unresolved question rather than rewriting their decision.

Weight the effort by how costly the decision is to reverse.

- **Easy to reverse** (one module, swappable behind an interface): answer in a few lines and stop. A written record would be noise.
- **Costly to reverse** (data model, core platform, service split, a public contract, vendor lock-in): investigate the drivers, alternatives and uncertainty below. Use the ADR workflow when a record is in scope.

If a costly decision can be made reversible cheaply, or deferred until there is real information, that is often the best recommendation. Say so, and say what would trigger making it. See `references/decision-principles.md` for reversibility and keeping options open.

## 2. Establish the drivers

Recommendations made without drivers are opinions. Pull these from the request, the repo and existing docs before asking anything:

- **The change or problem** that forces a decision now. If nothing does, question whether it has to be made yet.
- **Quality attributes in priority order.** Rank them to resolve trade-offs. Use measured values or user-supplied targets when available; otherwise propose a measurable target explicitly for validation. A suggested p95 or delivery time is not an existing requirement.
- **Hard constraints:** team size and skills, budget, deadlines, compliance, what is already running.
- **Scale that is real:** distinguish measured load from a forecast. Daily volume yields an average rate, not a burst distribution, processing-time budget or queue capacity. Do not turn a guessed peak multiplier into proof that a candidate meets an SLO.

Ask only for what would change the answer, at most a few questions. If the user wants progress or can't answer, proceed with explicit assumptions and name which one, if wrong, would flip the recommendation. Keep facts you verified visibly separate from assumptions you made, and never present an invented number as a requirement.

## 3. Compare real options

Compare two to four options that someone could genuinely choose. Include the simplest thing that could work, and "do nothing" or "extend what we have" whenever those are viable, because they are the options most often skipped and most often right. A strawman alternative added only to make the favourite look good wastes the reader's time.

Choose by the drivers, not a preferred technology or an unexplained numeric score. Where capability or capacity is unknown, state a check that can disqualify the option rather than inventing a guarantee. Evaluate each option against the ranked drivers, and also its **operational cost**: who runs it, how it fails, what it takes to migrate in and out. A table works well for the comparison, but the reasoning behind the deciding rows belongs in sentences.

## 4. Recommend and expose uncertainty

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
- **Context preserves the evidence,** including constraints such as deadlines or team skills. Distinguish supplied/verified facts, assumptions and proposed targets. Never fill missing team size, infrastructure, cost or approval history with plausible guesses.
- **Decision uses active voice:** "We will…".
- **Consequences include costs, risks and uncertainty.** State logical implications as implications, and predictions as expected effects. A dedicated database introduces additional database lifecycle work; it does not establish a particular routing catalog, migration schedule, staffing level, compliance result or measured availability. Put suggested mechanisms under Pending or Proposed details and label estimates with their basis. Apply fact/assumption discipline to every section, including Consequences and Revisit when; moving a guess outside Decision does not make it a fact.
- **Status is `proposed` unless the user tells you it has been agreed.** Recording a decision as accepted when nobody has accepted it misrepresents the team's position.
- **Records are immutable and numbers are never reused.** To reverse a decision, write a new record and change only the old one's status, adding a link back from the new one. The old reasoning stays because knowing why something was once right is often what prevents repeating it.
- **Say how much of the old decision survives.** Use `Superseded by ADR-NNNN` only when the old decision no longer applies at all. If it stays in force for some cases, use `Partially superseded by ADR-NNNN`, and state in the new record exactly what still holds. Otherwise a reader who sees "superseded" concludes the old approach is gone when most of the system may still run on it.
- **An accepted record only states what was decided.** When the team has told you the decision, the Decision section contains that decision and nothing you added. Implementation details that you think follow from it (a routing mechanism, a specific limit, a tool) go under a "Pending" or "Proposed details" heading, because people will later read the Decision section as something the team agreed to.

When a record is requested in a repository, write it to the appropriate file; do not create files for advice alone. Leave implementation and configuration changes out of scope unless asked. Before finishing a record, check that each accepted commitment is traceable to the user or prior records, uncertain statements remain labeled in every section, status reflects actual approval and links preserve history.
