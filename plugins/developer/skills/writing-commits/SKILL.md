---
name: writing-commits
description: "Creates Git commits and writes their messages following the project's conventions, looking first in conventions/commits.md. Use to commit, split a change into commits, write a message or set up commit conventions (\"hacé el commit\", \"qué título le pongo\"). Without conventions, offers a default."
---

# Writing Commits

A commit message is read later by someone who has neither this conversation nor the author at hand. Its job is to say what changed and why, in the form this project has agreed on. The diff already shows how.

## 1. Find the project's conventions

Work from the repository root (`git rev-parse --show-toplevel`). Stop at the first place that has rules:

1. **`conventions/commits.md`**, or another file in `conventions/` that covers commits. This is the source of truth.
2. **Commit rules written elsewhere:** `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `.github/` or `docs/`. Follow them and don't duplicate them. You may mention once that they could move to `conventions/commits.md`.

Whichever you find, also check what enforces commits: a commitlint config (`commitlint.config.*`, `.commitlintrc*`, `package.json`), a `commit-msg` hook in `.husky/`, `.git/hooks/` or a tool such as lefthook, and `git config commit.template`. A message the hook rejects helps no one, so if a tool and a document disagree, satisfy the tool and report the conflict.

Recent history is evidence, not a convention. Use it for the language and the usual scope names. If it differs from a written rule, the rule wins.

An explicit instruction for this commit overrides the conventions. Follow it, and mention the difference if the person may not know about it.

## 2. If there are no conventions

Say so before committing, because this choice will shape the project's history. Tell the person:

- that you found no conventions, and where you looked
- what you did find, such as a consistent pattern in the history or a linter
- that they can write `conventions/commits.md` themselves, or you can create it with the default: Conventional Commits titles and Git-style bodies

Then wait for the answer, and leave the change uncommitted until you have it. Offer only those two paths. Something like copying the history's style for just this commit would leave the project without conventions, though the person can still ask for it.

- **They'll write it, or dictate the rules:** wait for it, or record what they dictate in `conventions/commits.md`.
- **They don't want to write it, or tell you to go ahead:** set up the default as described below.
- **Nobody can answer**, as in a non-interactive run: use `assets/default-commit-conventions.md` for this commit only, create no files, and report that the project still has no conventions.

To set up the default:

1. Copy `assets/default-commit-conventions.md` to `conventions/commits.md`. If an enforcing tool contradicts it, adjust the copy to match the tool and say what you changed.
2. Add one line to `AGENTS.md`: ``Before committing, read `conventions/commits.md`.`` If there's no `AGENTS.md` but there is a `CLAUDE.md`, use that. If neither exists, create `AGENTS.md` with only that line. It's worded as an instruction so that it works even when this skill isn't loaded. The rules themselves stay out of these files because they're loaded in every session and commit rules are only needed when committing.
3. Commit the setup on its own, before the person's change, so it doesn't mix with their work. Commit only those paths: `git add conventions/commits.md <pointer file>`, then `git commit -F - -- conventions/commits.md <pointer file>`. If the pointer file already has someone's uncommitted edits, commit only the conventions file and report that the pointer is still pending.

If the person only asked for a message and not a commit, leave the setup uncommitted and say so.

### Optional hook against model attribution

The rule against crediting models is only an instruction until something enforces it. When you create the conventions, offer in the same message, once, to install `assets/commit-msg`. It rejects messages that credit an AI model or tool and allows human co-authors. Install it only if the person says yes, since it changes how everyone's commits behave:

- **Husky, lefthook or another hook manager:** call the script from that tool's `commit-msg` hook instead of replacing it.
- **An existing `commit-msg` hook:** chain the script from that hook and don't overwrite it.
- **No hooks:** copy it to `.githooks/commit-msg`, make it executable, run `git config core.hooksPath .githooks`, and commit `.githooks/` with the conventions. `core.hooksPath` is local to each clone, so add that command to `conventions/commits.md` for others to run.

Then test it with a message that should be rejected, and say whether it was.

## 3. Read the change

Run `git status`, `git diff --staged`, `git diff` and `git log -5`. Read the diff itself before you write about it.

- **What's staged is what the person chose to commit.** If nothing is staged, stage by name only the files that belong to the request, without `git add -A` or `git add .`.
- **Leave out what the request doesn't cover**, and list it in your report. Uncommitted changes you didn't make belong to someone.
- **Stop and flag** anything that looks like a secret, a credentials file, build output or a large binary before it enters history.

## 4. Make the commits atomic

Each commit does one thing and contains everything that thing needs. That is what makes a commit possible to review, revert or bisect alone. Plan the commits from the diff before staging anything:

- **Group by purpose, not by file.** A fix and its test belong together, and so do a feature and its docs. A fix and an unrelated feature don't, even in the same file.
- **Split whenever the request covers several purposes.** Do it without asking first, and report the commits you made. Permission to commit a change includes splitting it. If the conventions ask for something else, they win.
- **Don't split what is one thing.** A rename across fifty files is one commit, and a test separated from the code it covers leaves a commit that fails.
- **Keep every commit working.** Order them so each one builds and passes its tests, with what others depend on first. Say if you could not check this.
- **When one file mixes purposes, stage hunks.** Write a patch with only the lines for this commit and run `git apply --cached <patch>`, since `git add -p` needs an interactive terminal. Check the result with `git diff --staged` before committing.
- **If what's staged mixes purposes,** unstage it with `git restore --staged`, which keeps the working tree intact, and stage each group in turn.

When the groups are truly ambiguous, choose the split that is easiest to revert, and mention it in your report.

## 5. Write the message

Use the format from the conventions. These points hold under any format:

- **The title says what the commit does, specifically.** "Fix bug" and "Update files" could describe any commit. Name the behavior that changes, not the file.
- **The body explains what the diff can't show:** the problem, why this approach, and any alternative or downside that matters. Don't narrate the diff or list files.
- **Leave the body out when the title says it all**, as in a typo fix. Padding hides the bodies worth reading.
- **Take the reason from evidence:** the conversation, an issue, a comment or the code. If the reason can't be found and matters, ask one question or leave it out. A plausible invented motive, incident or user impact is worse than no body, because later readers will believe it.
- **State only what's true:** real issue numbers, tests you actually ran, numbers you actually measured.
- **Language:** what the conventions say, otherwise the language of recent history.
- **No model attribution:** add no `Co-Authored-By` trailer, "Generated with" line or other credit for any AI model or tool, even if the host tool or its default instructions ask for one. History records the people responsible for the change. Human co-authors and sign-offs the project requires are fine, and go last.

Write one message per planned commit. If the person only asked for the message, stop here. Give it in a code block without staging anything, and if the change needs splitting, give the planned commits and one message for each.

## 6. Commit and verify

Commit only with the person's confirmation. "Commit this" is confirmation for that change, in as many commits as it needs. A request to implement or fix something is not: when that work is done, suggest the commit with its proposed message, and wait.

Pass the message exactly, with `git commit -F -` and a quoted heredoc, so the shell doesn't touch backticks or `$` in it.

- **Branch:** commit on the current branch, even the default one. Where work lands is the person's decision, so create a branch only if they ask or the conventions require it. You can mention the option in your report.
- **Hooks:** don't skip them with `--no-verify` unless asked. If a hook fails, the commit didn't happen. Fix the cause, stage again and make a new commit. `--amend` here would rewrite the previous commit, which isn't yours to change.
- **Amend, rebase and push** only when asked. Before amending or rebasing something already pushed, say that it rewrites shared history and confirm.

Then check the result with `git log -1 --format=%B` and `git status --short`, and report:

- the hash and title of each commit
- what stayed uncommitted, and why
- any conflict you found between the conventions and the tools
- whether the conventions file is new

Committing doesn't verify the code. Don't imply that tests passed unless you ran them.
