# Code language and shared vocabulary — 2026-11-07

Authorized change: English technical code names for developer, with domain terms
in the requirements' agreed language, and the same ubiquitous language across
architect, developer, reviewer and code-investigator. One shared source is
embedded into each role's generated formats; no runtime checkout is required.
Existing public contracts and business terms are preserved. Conflicting project
language instructions are raised to the user rather than silently overridden.

## Evaluation

Applied skill-creator and eval-harness. Initial scenarios and expectations were
written before instruction changes (`definition.json`). Independent read-only
textual sessions received one role and request, without rubrics or previous
conclusions, and saved their own full responses as artifacts. No candidate code
or hosted service was executed; this is instruction-scoped isolation, not OS
containment or a workaround for the eval-harness executor's refusal.

The initial developer scenario exposed an interaction with the inherited
SkillSwap AGENTS.md requiring all identifiers in Spanish. It returned Spanish
technical names. Preserve that failure in `initial-result.json` and
`responses/spanish-domain-initial.md`. The developer rule was clarified to flag
such a conflict and ask instead of silently changing technical naming language.

Final textual cases (`definition-final.json`) separate explicit user language
selection from unresolved project policy conflicts, and add a conflict scenario.
The initial prompt is not presented as a fixed-prompt before/after comparison.
Fresh sessions produced the final developer responses. Architect/reviewer
responses were retained because their relevant guidance did not change.

An independent judge received only final requests, expectations and the matching
response artifacts. `grading.json`: **5/5 textual cases met their criteria**.
These cover English technical names with Spanish business terms, consistent
handoffs, preserving vocabulary in read-only review, ambiguous domain terms and
conflicting project language policy. `source-hashes.json` records the final role
sources and shared policy. No claim of stability, pass@k/pass^k, baseline advantage,
actual implementation or native client invocation follows from these samples.

## Verification

19 deterministic tests pass: five shared-guidance packaging/format tests and seven
evaluation-accounting tests per specialist plugin. All three generators pass
--check. Both specialist eval-suite validators pass (27 + 25 historical scenarios
structurally checked, not behaviorally rerun). JSON and TOML parse, and diff
whitespace checks pass. Claude's marketplace and three plugin manifests validate;
pre-existing directory-submission license/icon issues remain out of scope.

The new packaging test checks that the exact same maintained vocabulary policy
is embedded in all four roles and all client formats. This is distribution
consistency evidence, not proof that every future agent obeys the policy.
