# Commit conventions

These are this project's rules for commit messages. Change them whenever the team agrees on something else.

## Format

```text
<type>(<optional scope>): <title>

<optional body>

<optional footers>
```

Titles follow [Conventional Commits 1.0](https://www.conventionalcommits.org/en/v1.0.0/). Bodies follow the practice of the Git project: they explain the problem and the reason for the change.

## Title

- Use the imperative, as if giving the codebase an order: `add`, `fix`, `remove`, not `added` or `fixes`.
- Say specifically what changes. Avoid titles that could describe any commit, such as `fix: bug`.
- Start in lowercase and don't end with a period.
- Keep the whole line, including the type, to 72 characters or fewer.

## Type

| Type | Use it when the commit |
|---|---|
| `feat` | adds behavior for users of the software |
| `fix` | corrects a bug |
| `refactor` | restructures code without changing its behavior |
| `perf` | makes it faster or lighter |
| `test` | adds or corrects tests only |
| `docs` | changes documentation only |
| `style` | changes formatting only |
| `build` | changes the build system or dependencies |
| `ci` | changes continuous integration |
| `chore` | does maintenance that fits nowhere else |
| `revert` | reverts an earlier commit |

## Scope

Optional. A short noun for the affected area, such as `fix(auth):`. Reuse the names already in the history instead of inventing new ones.

## Body

Leave one blank line after the title and wrap lines at 72 characters. Skip the body when the title says it all.

Otherwise, explain what the diff can't show:

1. The problem, in the present tense: what the code does without this change.
2. Why this change is the right answer, and how it solves the problem at a high level.
3. Alternatives you discarded and downsides you accepted, if they matter.

If you claim an improvement, give the number. The message should make sense without opening a link, so summarize anything important from an issue or a discussion.

## Footers

Leave one blank line after the body. Each footer is a token and a value, such as `Refs: #142`. Use only issue numbers that exist.

Credit only people. Don't add `Co-Authored-By` trailers or other attribution for AI models or tools.

## Breaking changes

Add `!` before the colon, a `BREAKING CHANGE:` footer that explains what callers must do, or both.

```text
feat(api)!: require an API key on all requests

BREAKING CHANGE: requests without an `X-Api-Key` header now return 401.
```

## Atomic commits

Each commit does one thing and contains everything that thing needs, such as a fix with its test. If the title needs "and", or the body describes unrelated things, split it into several commits. Every commit should build and pass its tests, so it can be reverted or bisected alone.

## Language

Use the language of the recent history. In a new project, use English.

## Example

```text
fix(auth): reject expired refresh tokens

The middleware checks only the signature, so an expired token keeps a
session alive for as long as the client holds it.

Check the expiry claim as well and return 401 when it has passed.
Rotating the signing key would also end those sessions, but it would
log out every user.

Refs: #142
```
