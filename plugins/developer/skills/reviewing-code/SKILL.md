---
name: reviewing-code
description: "Reviews diffs and pull requests for correctness, safety and maintainability, and gives feedback people can act on, in any language. Use whenever someone asks to look over a PR, a diff, a commit or a branch before merging, or to check their own change, even if they just say \"le das una mirada\". Covers \"revisá este PR\", \"está bien este cambio\", \"qué le dirías a este PR\" and how to respond to review comments. For a deep review of one aspect, combine with secure-coding or testing. Reviews existing work; to review a whole package's structure use the architect agent."
---

# Reviewing Code

Use this skill to **review** a change, **prepare** a change for review or **respond** to comments. Its point of view: a review protects the code base and spreads knowledge. Its value lies in catching what tests and tools can't, so the reviewer's attention should go to what matters most.

## Before commenting

Understand the intent first, from the description, ticket and commit messages. Then read the whole diff, and the surrounding code it depends on. A diff doesn't show the caller that wasn't updated, the second copy that should have changed, or the test that's missing. Check out the code and run it where you can: run tests, the linter and the type checker, and say what you ran.

If the change is too large to review well, say so and suggest how to split it, rather than skimming.

## What to look for, in order

1. **Does it do what it claims?** Trace the main path and the failures. Look for off-by-one errors, null handling, wrong conditions, error paths, and partial failures.
2. **Is it safe?** Untrusted input, access checks, secrets, data loss, and migrations. Load `secure-coding` when the change touches these.
3. **Does it break anything else?** Callers, public contracts, compatibility, concurrency, and performance on realistic data.
4. **Is it tested?** Would the tests fail if the code were wrong? Are risky paths covered?
5. **Can the next person change it?** Names, unnecessary complexity, fit with existing conventions, misplaced responsibilities, and duplication of something that exists.
6. **Style.** Leave it to the tools. If no tool enforces it, raise it only when it's inconsistent with the project.

Don't enlarge the scope of the change: unrelated improvements go in a follow-up. Evaluate the change against what's already in the code base. It needn't be perfect if it makes things better overall.

## Giving feedback

Label each comment so the author knows what's required:

- **Blocking:** bug, security or data risk, or a broken contract. Say what fails and in what scenario.
- **Should fix:** a real cost, but with room for judgment.
- **Nit or optional:** a preference. Keep these few.
- **Question:** you don't know yet. Ask; don't assume it's wrong.

Each finding has its location as `file:line`, the concrete problem, and a suggested fix if you have one. Comment on the code, not the person. Explain why, because the reason teaches and lets the author push back with facts. Point out what's done well when it's truly notable.

Verify before you claim. A finding that turns out to be false costs trust, so check by reading or running the code. Mark what you merely suspect.

## Output

- **Verdict:** ready, ready after blocking fixes, or needs rework, in one line.
- **Findings:** most severe first, grouped by the labels above. No filler when there are none: "I found no blocking problems" along with what you looked at is a good result.
- **Not checked:** what you didn't run or read.

Don't post comments to a pull request or approve it unless asked. Your review goes to the user first.

## Preparing your own change

Read your diff as a reviewer before you ask for a review. Keep it small with one purpose. Remove debug code. Describe why it's needed, how it was tested and where to look closest.

## Responding to comments

Evaluate each comment on its merits, and check the claim against the code. Fix what's right. Where you disagree, give your technical reasons rather than complying blindly or ignoring it. Pass disagreement about preference to the project's conventions or a person's decision.
