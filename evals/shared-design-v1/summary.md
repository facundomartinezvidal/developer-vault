# Shared decisions and knowledge — 2026-11-07

## Scope and sources

Change authorized by the user: share relevant specialist guidance between
architect and developer; consult new design/business choices, retain prior
approvals, and make the coordinator verify the handoff before implementation.
The Vercel `build-agents` skill was consulted: it describes filesystem-managed
instructions, tools, skills, subagents and evals, but does not prescribe this
approval protocol. We keep the existing plugin stack; no eve runtime is added.

`definition.json` was written before changing the instructions. It contains eight
capability/regression scenarios, with expected behaviors withheld from solvers.
`source-hashes.json` records final instructions and shared resources; final
source edits after initial responses were formatting-only, except a clarified
approval row in implementing-designs, after which business-gap was repeated in
a fresh session. The first response is not used as the final business-gap result.

## Method and results

Applied skill-creator and eval-harness guidance. Independent subagent sessions
received role instructions, one request, and minimal synthetic context. They did
not receive rubrics or prior conclusions. These were read-only textual exercises;
no candidate programs, hosted runtimes or paid model scripts were executed.

Eight final responses are transcribed in `responses.json`, with formatting and
links normalized by the evaluator; these are **not raw transcripts**. An
independent judge read the definitions and responses without role instructions
or parent conversation. Original grading is preserved in
`grading-original.json`: **7/8 met its original rubric**.

The failed local-detail rubric required performed changes, while the solver
assignment prohibited writes/commands and requested a proposed snippet and next
action. Its answer renamed the accumulator, preserved the test and did not ask
for approval; it did not claim execution. This is an evaluation mismatch, not
evidence of completed implementation. A separate textual-only reassessment is
recorded without overwriting the original grade. Some solver prompts included
fixture details not present in the initial judge package; those limits are
retained instead of treating a grade as proof of actual tool use.

Observed: explicit pattern alternatives and approval request; no repeated
approval for accepted State; no invented refund policy; agent consensus not
substituted for human approval; packaged fallback guidance; read-only review
limits; retention of an approved design rather than an unauthorized deviation.

## Deterministic verification

- Four new shared-package tests: complete references in an isolated single-plugin
  layout; no eval material; source drift makes build --check fail; obsolete copies
  are rejected; equivalent protocol in Claude/Copilot/Codex formats and valid TOML.
- Seven existing evaluation-accounting tests per specialist plugin: 14 total.
- Both eval-suite validators: 27 architect and 25 developer scenarios structurally
  valid. These validators do not rerun the historical behavioral suites.
- Both specialist generators and reviewer generator pass --check.
- JSON and Codex TOML parse; git diff --check passes.
- claude plugin validate passes for repository, architect and developer. Directory
  submission checks still report the pre-existing missing license/icon; no license
  was chosen as part of this change.

## Limits and follow-up

No claim of stability, pass@k/pass^k, comparison with baseline instructions,
OS containment, native client discovery or runtime tool-use enforcement. The
current eval-harness candidate executor refuses execution without verified OS
containment; it was not invoked or bypassed. Textual sessions follow this repo's
instruction-scoped procedure and are not an alternative execution backend.
Approval rules are instructions, not host permission controls. Runtime integration
and repeated, fully traced multi-turn evaluations remain future work. The
independent judge and these samples do not replace human judgment of utility.
