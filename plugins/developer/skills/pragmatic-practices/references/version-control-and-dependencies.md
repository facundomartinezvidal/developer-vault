# Git, dependencies and documentation

Hand-written from common practice, drawing on the DORA research on small batches and trunk-based development, and on the Diátaxis documentation framework; not generated from the vault.

## Commits and branches

- One purpose per commit, with a message saying what changed and why. Follow the project's format.
- Read `git status` and `git diff` before committing, and stage specific files. Don't sweep in unrelated changes, secrets or build output.
- Work in small batches, and integrate often. Long-lived branches make merges and reviews costly.
- Before rewriting anything, look. `reset --hard`, `clean`, `checkout .` and force-push can destroy work that isn't yours. Uncommitted changes you didn't make belong to someone. Never force-push a shared branch without permission.
- Only commit, push or open a pull request when asked to or when the workflow calls for it.

## Merge conflicts

Understand what each side intended before choosing one. Read both changes and the code around them, keep both intentions where you can, then build and run tests. Choosing "ours" or "theirs" wholesale silently loses work.

## Adding a dependency

Check first whether the standard library or something already in the project does the job. Then check that the package exists under that exact name, is maintained, has a suitable license, and what it pulls in. Pin it through the lockfile, and mention it in your report. See `secure-coding` for supply-chain risks.

## Upgrading

Read the changelog and migration guide for each version crossed. Go one major version at a time, in its own change. Run the whole suite, and exercise what tests don't cover. Use the project's codemods if offered. Upgrade regularly: small steps are safer than a jump after years. Don't update everything at once when you were only asked for one.

## Long-running changes

For migrations across a large code base, change the shape in stages that all work: add the new way, move callers in batches, remove the old way, and keep a list of what remains. See `refactoring`.

## Understanding an unfamiliar code base

Start from an entry point: a route, command or test. Follow one real flow all the way through. Read the tests to see intended behavior, and use `git log` and `git blame` to see why something exists. Run it. Ask before removing odd-looking code, since it may be there for a reason (Chesterton's fence). Note what you've confirmed separately from what you've inferred.

## Documentation

Write what a reader can't quickly get from the code: why, how to run it, how to use it, and how it fails. Diátaxis separates four needs, and mixing them makes docs hard to use:

| Type | Purpose |
|---|---|
| Tutorial | Learning, with a guided first success |
| How-to | Doing a specific task |
| Reference | Looking up exact facts, ideally generated |
| Explanation | Understanding why |

A useful README says what it is, how to run and test it, and where to go next. Run the commands you document. Update docs in the same change as the behavior, and prefer checked forms: tests, type signatures and executable examples go stale less. Agent instructions such as `AGENTS.md` should hold short standing facts: commands and non-obvious rules. Don't add docs nobody asked for.

## Writing for reviewers and teammates

State the outcome first, then the reason and what's left. A change description says what, why, how it was tested, and what the risks are. When blocked, say so early, with what you've tried and the options.
