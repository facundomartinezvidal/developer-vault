# Pull request conventions

These are this project's rules for pull requests. Change them whenever the team agrees on something else.

## Scope

Each pull request has one purpose and includes everything it needs, such as tests and docs. Separate refactoring from behavior changes. If a change is too large to review in one sitting, split it into a series of smaller pull requests that each leave the project working.

## Title

Write the title like a commit title, following `conventions/commits.md` if it exists, because a squash merge turns it into the commit. Say specifically what the change does.

## Description

Use `.github/pull_request_template.md`. Omit sections with nothing to say, so a small change gets a short description.

- **Why:** the problem or the goal. A reviewer should understand it without opening a link, so summarize what matters from an issue or a discussion.
- **What changed:** the behavior and the approach, at a level the diff doesn't show.
- **How it was verified:** what you ran and its result, and what you couldn't check.
- **Risks:** migrations, configuration, contract changes, performance, rollout or rollback.
- **Where to look:** the parts that need the most attention.

Use `Closes #N` only for an issue the pull request fully resolves, and `Refs #N` otherwise.

Credit only people. Don't add "Generated with" lines, `Co-Authored-By` trailers or other attribution for AI models or tools.

## Before asking for review

- Review your own diff first: leftovers, secrets, unrelated files.
- Run the project's checks locally when you can.
- Open it as a draft only while it is unfinished.

## Language

Use the language of recent pull requests. In a new project, use English.
