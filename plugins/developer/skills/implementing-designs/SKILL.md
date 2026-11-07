---
name: implementing-designs
description: "Turns architecture plans into working code without losing what was decided, including ADRs, C4 views, Clean Architecture layers, DDD models, threat models and proposals from the architect agent. Use whenever someone asks to implement, apply, or follow a design, ADR, architecture decision, plan or threat model, or asks how a design should look in code such as ASP.NET Core or Spring Boot, even if they just say \"implementá lo que dijo el arquitecto\" or \"cómo llevo esto a código\". Covers mapping layers, ports, aggregates, domain events and security mitigations to framework code, and making the design enforceable. If the decision itself is still open or needs changing, use the architect agent."
---

# Implementing Designs

Use this skill to **implement** a design, **explain** how to turn it into code, or **check** whether code matches it. Its point of view: a design only counts once it holds in code, and implementation is where it gets quietly lost, whether to framework habits or to a convenient shortcut. Keep the decisions, and take the smallest path to working software.

## 1. Read the design as a commitment

Find the sources: ADRs, diagrams, threat models, the architect's answer, and project guidance. Then separate them:

| Kind | How to treat it |
|---|---|
| Accepted decision | Binding. Implement it. |
| Plan from the architect that the person asks you to implement | Follow its approved choices, scope and acceptance checks. Verify the approval source; the architect authoring a plan does not approve unseen new choices for the user. Pending design and business decisions remain pending. |
| Proposed or draft ADR | Not a commitment. Don't implement it unless the person says so. |
| Superseded or deprecated | Follow the newer record, including what a partial supersession leaves in force. |
| "Pending" or suggested in an ADR | Options, not requirements. |
| Diagram of the current state | Describes what exists; it doesn't authorize changes. |

List what the design actually requires: the behavior, the boundaries, the guarantees and the mitigations. Read the real code too: the design may be out of date relative to it, and any gap should be stated.

Then look for what it leaves open. For each rule or operation, ask what happens in the cases the design doesn't mention: the operation repeated, the other states the object can be in, a failure halfway, and two concurrent callers. Designs usually describe the main rule and stay silent on these, and the code has to do something anyway.

## 2. Handle gaps and conflicts honestly

- **A technical detail is left open:** choose the simplest option consistent with the design and the project, and say so. Small implementation choices are yours to make.
- **A behavior is left open:** keeping what the code does today is a reasonable default, but it's still a decision that the design didn't make, and without being told, the person will assume that the design covers it. Name it as a gap and ask the user before implementing a new business or design choice. Preserve existing behavior where that does not decide the open question; continue independent work while waiting. Explain what the design does not define and who must decide. For example: "the ADR doesn't say what happens when a coupon is redeemed after it expires during checkout; accepting an expired coupon is unspecified; should checkout reject it or honor the earlier price?"
- **The design can't work as written,** or conflicts with the code, the framework, another decision or the request: stop on that point and show the concrete conflict. Propose the smallest deviation as a proposal. Don't silently reinterpret it, and keep working on what isn't affected.
- **A new structural decision appears:** return it to the architect agent if available, or mark it as a proposal for the person. Don't write an ADR as accepted on your own.
- **Business rules:** don't invent them. Ask, or mark as an assumption that needs confirming.

## 3. Plan a vertical path

Implement one real use case end to end through the planned structure before spreading it. That tests the design early and shows others the pattern. Then proceed in small working steps. In an existing system, migrate gradually with expand and contract, or branch by abstraction, rather than a rewrite. Don't build every layer, or abstractions for later use cases, up front. Boundaries the design doesn't require aren't yours to add.

## 4. Map the design to the framework

Keep the design's meaning, and use the framework's idioms for the rest. Load `framework-practices` and read `references/designs-in-frameworks.md` for how layers, ports, aggregates, events and mitigations look in ASP.NET Core and Spring Boot. A boundary doesn't need a project or a module per circle; choose the lightest form that's enforceable, unless the design says otherwise.

Common ways to lose a design:

- Business rules in controllers, handlers or SQL, because that's quick.
- ORM annotations, HTTP types or framework exceptions leaking into the domain when the design says that it stays independent.
- Interfaces that mirror the ORM, with the port's owner on the wrong side.
- An aggregate whose invariant is enforced only by the caller, or a transaction wider or narrower than the design's consistency boundary.
- Terms renamed away from the agreed language.
- A mitigation that is implemented but never verified.

## 5. Make it enforceable and verify it

An agreement that nothing checks will decay, so add a check where it protects something important: architecture tests (ArchUnit, Spring Modulith, NetArchTest), compile-time module boundaries or visibility, and contract tests.

Verify in the design's terms, and not only that tests pass:

- **Behavior:** tests for the rules and failure paths it specifies.
- **Boundaries:** dependencies point the agreed way.
- **Guarantees:** transactions, idempotency and ordering, with a test of the failure case.
- **Threat mitigations:** a test that shows each attack being refused.

## Output

When implementing, report:

- **Decisions followed:** a short table of each requirement, where it lives (`file:line`), and how it was verified. Mark whatever wasn't verified.
- **Technical choices you made** where the design was silent.
- **Gaps in the design:** behaviors it doesn't define, what the code does now and who should confirm them. If you found none, say which cases you checked.
- **Deviations and conflicts:** none silently taken; each with its reason and status as a proposal.
- **Not done:** what remains for later steps.

When asked how to implement without changing code, give the mapping with a representative code sketch and the steps. When checking conformance, list where the code matches and where it drifts, and whether to fix the code or revisit the decision. That last choice belongs to the person.

## Reference files

| File | Read when the topic is… |
|---|---|
| `references/designs-in-frameworks.md` | Clean Architecture, DDD building blocks, events, consistency, threat mitigations and enforcement, in ASP.NET Core and Spring Boot |
