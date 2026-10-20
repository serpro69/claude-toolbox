# ADR 0010: Proportionate Verification and Agent Evaluation

## Status

Accepted (2026-10-20), following the user's explicit approval to reassess
functional-review acceptance and establish durable guidance for future agents.

## Context

Functional-review evaluations mixed consequential mistakes with missing optional
advice, report-detail omissions, tool unavailability and incomplete captures.
The all-assertions-pass-twice gate made every observation an acceptance veto.
Repeated small instruction changes led to large comparisons without isolating
those changes from the broader feature.

R6's label-only increment could be correctly approved while an unrelated dormant
bug lacked follow-up. R7's revised, clearer fixtures elicited the intended
compatibility decisions without a skill change. Neither example establishes
general reliability or proves every original test invalid. Both show why a
rubric failure and a product failure need separate assessment. The
[acceptance reassessment](../feat/wip/functional-review/acceptance-reassessment.md)
links the concrete reports and retained grades.

The testing skill also instructed agents to cover all branches and always run
all tests. A warning added elsewhere would leave that conflicting incentive.
This extends [ADR 0007](0007-failure-citing-defaults.md)'s falsifiable-default
principle to verification and acceptance.

## Decision

Verification must answer a decision-relevant question about agreed behavior.
Keep explicit software invariants, required repository checks and consequential
acceptance requirements. Separate material failures, quality observations and
evidence limitations; a score does not by itself decide adoption.

For agent evaluations, assess semantic outcomes and variability. Exact sequences
or wording need a contract-based reason. A clearly explained bug can be useful
without a suggested follow-up. Humans and implementing agents can select next
actions; this does not remove durable tracking for material work actually deferred.
Missing evidence cannot certify success, but neither proves a behavioral failure.

Validate fixtures and graders before changing actor instructions. A targeted
change needs an immediate-predecessor comparison to investigate its incremental
effect; a pre-feature comparison answers a broader question. Declare bounded
measurement and decision criteria before new runs. Expand only to resolve an
uncertainty that could change the decision. Consider simplification before adding
instructions, including the full loaded context and workflow cost.

Authorized policy corrections supersede live gates explicitly. Preserve old
captures, rubrics and grades; do not relabel them PASS or demand new actor runs
merely to retire an unjustified criterion. New behavioral claims still need
adequate evidence. A serious demonstrated failure may justify stopping even
without a reliability estimate.

Operative guidance lives in
[`verification-policy.md`](../../klaude-plugin/skills/_shared/verification-policy.md),
loaded by `/kk:design`, `/kk:review-design` (including its isolated reviewers)
and `/kk:test`. Existing testing guidance is replaced rather than supplemented
with a competing checklist. Grading instructions retain strict observation
scores while leaving adoption to the declared policy. `AGENTS.md` makes the
lesson available to repository contributors outside those workflows.

## Consequences

- Testing remains strong where a failure matters; optional advice and harmless
  report variation no longer silently become shipping requirements.
- Correcting a test is a supported outcome, with an explicit rationale and
  preserved evidence. Actual requirements cannot be weakened just to pass.
- Historical FAILs can coexist with a justified acceptance decision. Retired
  gates no longer keep work open under historical bookkeeping.
- Source review and structural checks establish this policy's integration, not
  improved model reliability. Reviewer simplification and new measurements are
  separate choices, justified only by a remaining consequential question.
