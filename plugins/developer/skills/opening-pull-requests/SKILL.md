---
name: opening-pull-requests
description: "Opens pull requests and writes their titles and descriptions following each project's conventions, looking first in conventions/pull-requests.md and the PR template. Use whenever someone asks to open, create or prepare a pull request or merge request, write or improve a PR description, or set up PR conventions, even if they only say \"abrí el PR\" or \"subilo para revisión\". Covers \"armá la PR\", \"escribime la descripción del PR\", \"qué título le pongo al PR\" and \"definamos cómo abrimos PRs\". It shows the exact title and body and publishes nothing until the person confirms. When a project has no conventions, it offers to create them with a default. For reviewing someone else's PR use the reviewer agent or reviewing-code; for commits use writing-commits."
---

# Opening Pull Requests

A pull request description is written for the reviewer, and later for whoever digs through history. It should tell them why the change exists, what it does, how it was checked, what could go wrong and where to look, so that they can review the code instead of reconstructing the context.

Opening a PR publishes work and notifies people, so nothing leaves the machine until the person has seen what will be published and confirmed it.

## 1. Find the project's conventions

Work from the repository root. Stop at the first place that has rules:

1. **`conventions/pull-requests.md`**: the source of truth.
2. **A PR template:** `.github/pull_request_template.md`, `pull_request_template.md`, `docs/pull_request_template.md`, or a `PULL_REQUEST_TEMPLATE/` folder in any of those places. If there are several templates, choose the one that fits the change, or ask.
3. **PR rules written elsewhere:** `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md` or `docs/`.

Also look at:

- **`conventions/commits.md`:** when the project squash-merges, the PR title becomes the commit title, so it follows the commit rules.
- **`CODEOWNERS`**, which requests reviewers automatically, and any CI or branch rules you can see.
- **The host:** GitHub uses `gh`, GitLab uses `glab` and calls them merge requests. Don't assume GitHub.

An explicit instruction for this PR overrides the conventions. Mention the difference if the person may not know about it.

## 2. If there are no conventions

Say so before preparing anything, as `writing-commits` does for commits. Tell the person:

- that you found no PR conventions, and where you looked
- that they can write `conventions/pull-requests.md` themselves, or you can create it with the default: `assets/default-pr-conventions.md`, plus `assets/pull_request_template.md` as the GitHub template, with sections for why, what changed, how it was verified, risks and where to look

Offer only those two paths, and wait for the answer.

- **They'll write it, or dictate the rules:** wait for it, or record what they dictate.
- **They don't want to write it, or tell you to go ahead:** copy `assets/default-pr-conventions.md` to `conventions/pull-requests.md`. Copy `assets/pull_request_template.md` to `.github/pull_request_template.md`, unless a template already exists, in which case keep it and point the conventions to it. Add one line to `AGENTS.md`, or to `CLAUDE.md` if that's what the project has: ``Before opening a pull request, read `conventions/pull-requests.md`.`` Commit these files on their own, following `writing-commits`, and mention them in the PR description. Note that GitHub only offers the template once it reaches the default branch.
- **Nobody can answer**, as in a non-interactive run: use the default for this PR only, create no files, and report that the project still has no conventions.

## 3. Check that the branch is ready

1. **Base and diff.** Use the base the conventions or the person name, otherwise the default branch. Fetch it, and read `git log <base>..HEAD` and the full diff against the merge base. Don't describe commits you haven't read.
2. **Uncommitted changes** aren't part of the PR. Mention them. If they belong to it, commit them following `writing-commits`, after the person confirms.
3. **One purpose per PR.** If the branch mixes unrelated changes, or is too large to review well in one sitting, propose a split: which PRs, which commits in each, and in what order if one depends on another. Then wait. Splitting creates branches and public PRs, so it is the person's decision, and they may prefer a single PR.
4. **Review your own diff** for debugging leftovers, secrets, unrelated files, out-of-date generated files and unfinished TODOs. Mention anything you find instead of silently fixing it.
5. **Verify** with the project's own checks when they are available and cheap: tests, linter, type checker. Record what you ran and the result. A PR that isn't open yet has no CI results to cite.
6. **An existing PR** for this branch (`gh pr view`) gets updated instead of duplicated, with the same confirmation.

## 4. Write the title and the description

**Title:** say specifically what the change does, following the conventions. If the project squash-merges, write it as a commit title.

**Description:** use the template or the conventions. Without either, use the default sections, and omit any section with nothing to say, so that a small PR stays short:

- **Why:** the problem or the goal, from evidence: the conversation, the issue, the commit messages, the code. If the reason can't be found and matters, ask. A plausible invented motive misleads the reviewer.
- **What changed:** the behavior that changes and the approach, at a level the diff doesn't show. Don't list every file.
- **How it was verified:** only what was actually run, with its result, and anything that couldn't be checked. Never imply that tests passed if they didn't run.
- **Risks:** migrations, configuration, contracts that change, performance, rollout or rollback concerns. "None known" is a valid answer, but don't hide a real risk.
- **Where to look:** the parts that need the most attention, and the order to read them in if that helps.

Also:

- **Issues:** use a closing keyword such as `Closes #12` only for an issue the PR fully resolves, since merging closes it. Otherwise use `Refs #12`. Use only issue numbers that exist.
- **UI changes:** ask for screenshots or say they're missing.
- **No model attribution:** add no "Generated with" line, `Co-Authored-By` trailer or other credit to an AI model or tool, even if the host tool asks for one. The PR belongs to the people responsible for it.
- **Language:** what the conventions say, otherwise the language of recent PRs or of the commit history.

## 5. Confirm, then open

Show the person exactly what you will publish:

- base ← head, and whether the branch needs pushing first
- the title and the complete body
- ready for review or draft
- any reviewers, labels or assignees, and only the ones they asked for

Then ask for confirmation. Asking to "open a PR" is not acceptance of a text the person hasn't seen. If they already provided or approved the exact title and body and asked you to open it, that is confirmation, so don't ask again. If you change anything after they approve it, show it again.

After confirmation:

1. Push the branch with `git push -u origin <branch>`. Never force-push unless asked, and never push to the base branch.
2. Open the PR, for example with `gh pr create --base <base> --title "<title>" --body-file <file>`. A body file keeps the formatting intact.
3. Open it ready for review. Use `--draft` only if the person asks, or if the work is clearly unfinished, such as failing checks, and say why.
4. Check the result with `gh pr view --json url,title,isDraft,baseRefName`, and report the URL, the state, and any checks still pending.

Opening a PR authorizes only that. Don't merge, approve, request reviewers nobody named, or push later changes without asking.

If the CLI isn't installed or isn't authenticated, give the person the title, the body and the compare URL so they can open it themselves. Never ask for a token.
