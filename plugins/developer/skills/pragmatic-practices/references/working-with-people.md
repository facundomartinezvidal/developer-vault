# Working with people

Communicating, taking responsibility, reviewing and building together, and moving a team.

## Contents

- [Take Responsibility](#take-responsibility)
- [Communicate!](#communicate)
- [Working Together](#working-together)
- [Pragmatic Teams](#pragmatic-teams)
- [Stone Soup and Boiled Frogs](#stone-soup-and-boiled-frogs)

## Take Responsibility

> Provide Options, Don't Make Lame Excuses. — Tip 4

**Source:** *The Pragmatic Programmer*, Topics 1, 2 and 53 (Tips 1–4, 97–99).

### What it means in practice

The book opens and closes on ownership:

- **You have agency** (Topic 1). If your job, your stack or your team is bad, you can change it, or change *where* you work. Don't just complain.
- **Own your mistakes** (Topic 2). When something goes wrong (a missed deadline, a lost backup, a bug in production), don't blame the vendor, the language or a teammate. Before you report a problem, run through the excuse in your head: does it sound reasonable or lame? Then come with **options**: what can be done, what it costs, what you need. Commitments are made knowing the risks, and if a risk is outside your control, you say so up front.
- **Sign your work** (Topic 53). Be proud enough of what you build to put your name on it. Others then know it's yours, they can rely on it, and they can ask you about it. That doesn't mean being defensive about others' changes to "your" code. And: first, do no harm. Don't build software that hurts users.

### Example

> "The nightly export failed because the vendor changed their CSV format."
> vs.
> "The nightly export broke on a vendor format change. I've patched the parser and backfilled last night's data. To stop this recurring, I'd add a schema check that alerts us before the import runs — about half a day."

### Related

- Communicate! — options only help if they're delivered clearly.
- Good-Enough Software (`approaching-work.md`) — being responsible includes knowing when to stop.
- Estimating (`approaching-work.md`)
- Stay Safe Out There (`tooling-and-automation.md`)
- Stone Soup and Boiled Frogs

## Communicate!

> It's Both What You Say and the Way You Say It. — Tip 12

**Source:** *The Pragmatic Programmer*, Topic 7 (Tips 11–13).

### What it means in practice

Treat **English** (or whatever language your team speaks) **as just another programming language** (Tip 11). Good ideas that aren't communicated don't count for much. A checklist:

- **Know your audience** and **what you want to say**. Write an outline first.
- **Choose your moment** and **choose a style** (formal, brief, detailed). Ask what the reader wants.
- **Make it look good**, **involve your audience** in drafts, **be a listener**, and **get back to people** promptly, even just to say "I'll get back to you".
- **Build documentation in, don't bolt it on** (Tip 13). Comments and docs generated from the code stay current, while a separate document goes stale. Comment *why*, not *how*. The code already shows how.

### Example

A pull request description with this structure: **what changed** (one line), **why** (link to the incident or ticket), **how to verify** (a curl command or test name), and **risk/rollback**. It works for the reviewer reading it today and for whoever runs `git blame` next year.

### Related

- Take Responsibility — offering options is a communication skill.
- The Requirements Pit (`approaching-work.md`)
- Working Together
- Estimating (`approaching-work.md`)

## Working Together

> Don't Go into the Code Alone. — Tip 82

**Source:** *The Pragmatic Programmer*, Topic 47.

### What it means in practice

Hunt & Thomas suggest replacing "throw it over the wall" handoffs (requirements → dev → QA → ops) with *conversations* while the code is being written:

- **Pair programming.** One person types and the other thinks about the bigger picture. You get continuous review, and knowledge spreads across the team.
- **Mob programming.** The whole team, sometimes including a user, works on one problem at one screen, with a rotating typist. It's good for hard problems and onboarding.
- Whatever form you use: build the code, not your ego. Start small, criticize the code and not the person, listen and try to understand other points of view, and do retrospectives.

It's slower in typing-per-person, and faster in finished, shared, reviewed work.

### Example

A tricky migration of billing data across three services is done as a mob session with a backend dev, the DBA, and an ops engineer. The rollout plan, rollback script and monitoring dashboard get built together in one afternoon, instead of over a week of review comments.

### Related

- Pragmatic Teams
- Communicate!
- The Essence of Agility (`approaching-work.md`)
- The Requirements Pit (`approaching-work.md`) — "work with a user to think like a user".

## Pragmatic Teams

> Maintain Small, Stable Teams. — Tip 84 &nbsp;·&nbsp; Organize Fully Functional Teams. — Tip 86

**Source:** *The Pragmatic Programmer*, Topic 49 (Tips 84–86).

### What it means in practice

Every individual pragmatic practice also works at the team level:

- **Small and stable.** About 10–12 people at most, with members who trust each other and stay together.
- **No broken windows, no boiled frogs.** Quality is the whole team's responsibility, and someone keeps watching the environment for gradual decline.
- **Schedule it to make it happen** (Tip 85). Knowledge-portfolio time, system improvement, experiments and refactoring only happen if they're on the schedule.
- **Communicate team presence.** A team with a clear identity and reliable output is easier to work with.
- **Don't repeat yourselves.** Good communication prevents duplicate work between team members.
- **Fully functional teams.** Organize around **functionality**, end to end (UI to database to deployment), not by job role (a "DB team", a "UI team"). That way one team can deliver a feature with no handoffs.
- **Automate** and know when to stop adding paint.

### Example

Instead of a frontend team, a backend team and a QA team, a "Payments" team owns checkout end to end, including its UI, API, data, alerts and on-call. It ships a new payment method without filing tickets with three other teams.

### Related

- Working Together
- The Essence of Agility (`approaching-work.md`)
- Pragmatic Starter Kit (`tooling-and-automation.md`)

## Stone Soup and Boiled Frogs

> Be a Catalyst for Change. — Tip 6 &nbsp;·&nbsp; Remember the Big Picture. — Tip 7

**Source:** *The Pragmatic Programmer*, Topic 4.

### What it means in practice

Two short parables:

- **Stone soup: how to start change.** In the folk tale, hungry soldiers start "soup" with only stones in a pot, and the curious villagers each add one ingredient. When you know what should be built but can't get approval or resources for the whole thing, build a small, reasonable piece and make it visible. People join something that's already succeeding. They resist a big proposal on paper. (Use this for good, not to trick people.)
- **Boiled frogs: how decline happens.** Raise the water temperature slowly enough and the frog never jumps out. Projects decay the same way: one scope creep, one skipped test, one extra hour at a time. Keep looking at the big picture so you notice the trend, not just today's small change.

### Example

You want structured logging and tracing, but the team has no appetite for "an observability initiative". You add OpenTelemetry to the one service that keeps having incidents, and the next postmortem takes 20 minutes instead of a day. Other teams ask how to add it to theirs.

### Related

- Tracer Bullets (`approaching-work.md`) — a working end-to-end slice is a good stone for the soup.
- Take Responsibility — you have agency.
- Pragmatic Teams — teams can boil too. Someone should be watching for it.
- Good-Enough Software (`approaching-work.md`)
