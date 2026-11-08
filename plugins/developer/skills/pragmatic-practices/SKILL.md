---
name: pragmatic-practices
description: "Advises on how to approach development work: unclear requirements, slicing, estimates, prototypes, unfamiliar code, dependency upgrades, merge conflicts, docs and automation (\"cómo encaro esto\", \"cuánto puede llevar\"). Not needed for a clearly specified small task."
---

# Pragmatic Practices

This skill carries a personal study of everyday development practice as reference files. Use it when the question is **how to do the work** rather than what the code should be. Its point of view: take small steps, get feedback fast, and be honest about what you know.

## Unclear requirements

Requirements are learned, not gathered. Find the need behind the request: what is it for, who uses it, and what happens today? Separate real constraints from habits. Show something concrete early and adjust. Ask the few questions that change the work, and record the assumptions. Don't build for an imagined future.

## Getting started

- **Tracer bullet:** a thin end-to-end slice of production-quality code, used when the path through the system is uncertain. It stays and grows.
- **Prototype:** throwaway code to learn one risk, such as an API, an algorithm or a UI. It answers a question and is discarded; state that up front.
- **Direct implementation:** when the path is known. Don't add ceremony.

Slice work so that each step can be verified. Take a step whose result you can see before planning further. If something feels wrong and you can't say why, stop and look; that hesitation often has a cause.

## Estimates

Before giving one, ask what it's for and what precision is needed. Break the work down, name the riskiest parts, and give a range with its assumptions, not a single number. Use a unit that matches the certainty. Say what would narrow the range: often a small spike. Don't present a guess as a commitment, and re-estimate as you learn. You can't measure how long tasks take for this person or team from code alone; say so.

## Good enough

Quality is part of the requirements. Agree on the bar for this context: a one-off script and a payment path differ. Good enough never means known data loss, security holes or tests silently disabled. Fix small degradations when you see them or record them, because neglect spreads.

## Tooling and automation

- **Version control:** everything needed to build goes in, with small commits that have one purpose and a message saying why. Don't commit secrets. Look before any command that can destroy work.
- **Dependencies and upgrades:** add them deliberately, and upgrade in small steps with the changelog at hand.
- **Automate what repeats:** build, tests, linting and deploys should run from one command and in CI. Automate after doing it by hand enough to know the steps are stable.
- **Configuration:** values that vary by environment live outside the code, and secrets outside the repository.
- **Security basics:** minimize the attack surface and privileges, apply patches, and don't hand-roll crypto.

Propose changes that fit what the project already uses, not a new toolchain.

## People

Bring options rather than excuses when something can't be done. Communicate early, tailored to the audience, and answer messages. Prefer early review or pairing on risky work. In a review, be concrete and criticize the code, not the person. For team changes, start with something small that visibly helps.

## Output

Give a concrete next step for this situation, with its reasoning and what would change your mind. Avoid general process advice and don't recite tips. If it needs a tool or team change, name its cost.

## Reference files

| File | Read when the topic is… |
|---|---|
| `references/approaching-work.md` | requirements, tracer bullets, prototypes, estimating, good enough, small steps, reversibility, intuition, agility |
| `references/tooling-and-automation.md` | version control, build and test automation, plain text, configuration, security basics |
| `references/version-control-and-dependencies.md` | commits, branches, conflicts, adding and upgrading dependencies, learning an unfamiliar code base, documentation |
| `references/working-with-people.md` | responsibility, communication, working together, teams, driving change |
