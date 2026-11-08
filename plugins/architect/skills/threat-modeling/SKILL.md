---
name: threat-modeling
description: "Threat-models a design with STRIDE: assets, data flows, trust boundaries, ranked risks and mitigations. Use when designing or reviewing something with users, money, files, tenants, webhooks or AI agents (\"es seguro este diseño\", \"cómo lo podrían atacar\"). Vulnerable code: secure-coding."
---

# Threat Modeling

Threat modeling is a structured answer to four questions: what are we working on, what can go wrong, what are we going to do about it, and did we do a good enough job. The value is in design issues found and fixed, not in a thorough-looking document. A short list of real risks the team will act on beats a catalogue of a hundred generic ones.

## Scale it first

Match depth to exposure: what's at stake, who can reach it, and how much it would hurt.

- **Small scope and low exposure** (including an internal tool when its assets and permissions justify it): a short pass. Internal does not imply low impact; an internal admin tool with broad access can deserve a deeper review. Do the thinking below, but report a short list of the risks or checks that matter, each with the scenario and action. Zero new findings is a valid result; do not invent three to five risks to fill a quota. Aim for under 300 words, without a diagram or formal STRIDE report unless needed to explain the risk. A brief limit or conclusion is useful when it changes the decision. Don't prescribe a WAF, a SIEM or a pentest to a Slack bot. This person asked a small question; a long answer gets skimmed and the important fix gets lost.
- **Production feature or system with user data or money:** examine the relevant flows below, scoped to what changed if the rest was already modeled. Present only the detail needed to make the security decisions.
- **High stakes** (payments, health data, multi-tenant platform, critical infrastructure): full process, and say plainly when it needs human security specialists or a compliance review. This pass doesn't replace them.

Length costs the reader attention, whatever the tier. For a single feature or design, stay around 1,500 words. Reaching for more usually means you are repeating yourself across threats or covering hypotheticals.

Scope to a manageable piece, and say what you left out.

## 1. What are we working on?

Identify whether you are reviewing a proposed design or a running system. Ground the model in the supplied design, code and deployment evidence; code alone does not establish runtime reachability or configuration. Report disagreements and what remains unknown instead of silently choosing a convenient version.

- **Assets:** what an attacker wants or what would hurt to lose (data, money, credentials, availability, reputation). Being specific here is what makes later ranking possible.
- **Actors:** legitimate roles and realistic adversaries, including other tenants, malicious insiders, and compromised dependencies.
- **Data flow diagram** in Mermaid: external entities, processes, data stores, data flows.
- **Trust boundaries:** every place where the level of trust changes, such as internet to service, tenant to tenant, service to third party, user content to a parser, or untrusted text to an LLM with tools. Most serious threats live on these lines.

Separate **demonstrated gaps**, **conditional threats**, and **checks requiring evidence**. For each finding, point to the supplied fact or code that enables the scenario. A control not mentioned in a short document is unknown, not proven absent. A described control is relevant evidence of intent, not proof that it is implemented correctly. State the assumption that would enable a conditional threat and the smallest check that would resolve it.

Credit existing controls: explain which scenario they address, and investigate concrete residual paths rather than repeating the same vulnerability as if the control were absent. Do not label a public endpoint unauthenticated merely because it lacks a login screen when it validates a signed machine request. A signature authenticates its source; permissions and permitted data scope still need separate examination.

## 2. What can go wrong?

Walk the flows that cross trust boundaries, and for each element consider the STRIDE categories that apply:

| Threat | Violates | Typical question |
|---|---|---|
| **S**poofing | Authentication | Can someone pretend to be another user or service? |
| **T**ampering | Integrity | Can data be changed in transit, at rest, or by the client? |
| **R**epudiation | Non-repudiation | Could someone deny an action, with no evidence either way? |
| **I**nformation disclosure | Confidentiality | Can data reach someone who shouldn't see it? |
| **D**enial of service | Availability | Can someone exhaust or block it, cheaply? |
| **E**levation of privilege | Authorization | Can someone do what their role doesn't allow? |

| Element | Categories usually worth checking |
|---|---|
| External entity | S, R |
| Process | S, T, R, I, D, E |
| Data store | T, I, D (R if it holds audit logs) |
| Data flow | T, I, D |

Use the table as a prompt for thinking, not a form to fill in: skip what doesn't apply without comment. A threat has to name who does what to which element and with what effect, in this system. "Attackers could use SQL injection" is generic; "a tenant admin can read another tenant's invoices by changing `tenantId` in `GET /invoices`, because it's taken from the request instead of the token" is a finding.

STRIDE is weak on business logic, so also ask how someone could abuse a legitimate feature: refund loops, coupon stacking, invite spam, a webhook URL used to reach internal services. `references/common-threats.md` lists recurring architecture-level threats to check; use it to jog your memory after your own analysis, and keep only those that are real here.

## 3. What are we going to do about it?

Rank supported scenarios by **likelihood and impact on the assets you named**, considering controls already present, using High/Medium/Low with a one-line reason. Mark confidence or missing evidence separately from severity; an unknown is not automatically a high risk. Don't use a numeric score: it implies a precision the analysis doesn't have.

For each threat, pick a response: **mitigate**, **eliminate** (remove the feature or the data, often the best fix), **transfer** (delegate a control or financial exposure to a provider while naming what responsibility remains locally), or **accept** (only a person who owns the risk can accept it, so flag it for them). Mitigations should be concrete and placed in the design: which component changes, and how you would test it. Name the responsible role when known, or propose one explicitly rather than implying someone has accepted ownership. Prefer the framework's or platform's standard control over custom crypto or custom auth.

Report in this format, most severe first:

```markdown
### T1. <short title> — High (STRIDE category)
<Scenario in a sentence or two: who does what, via which path, and why that rating.>
**Fix:** concrete change and where it goes. **Verify:** the test or check showing it works.
```

Use that form for supported high risks when a full report is warranted; do not promote an uncertain scenario just to use the template. Merge threats that share one fix into a single entry, and put medium and low risks in a table of one line each (risk, rating, fix).

Start the report with a few lines on the top risks and what to fix first. Then give the diagram with its trust boundaries, the assumptions, and the threats. Close with a few lines on what looks well handled, because knowing what not to change is useful too.

## 4. Did we do a good enough job?

Before finishing, check that the scoped trust boundaries were examined, every high risk has a response, and assumptions and residual risks are explicit. Distinguish proposed verification from checks actually executed. If the supplied design addresses the relevant threats, say that no new blocking gap was identified within this scope and give the few checks that could invalidate that conclusion; do not certify the whole system. Tell the reader in two or three lines what you didn't cover and what would invalidate this report (a new external integration, a new data category, a change in auth or tenancy), since threat modeling follows design changes.

Don't claim the design is "secure". You found what this pass found.

## Authorized scope

This skill analyzes designs and code the user is responsible for, in order to defend them. Describe threats at the level needed to understand and fix them; working exploits aren't needed for that and aren't part of the output.
