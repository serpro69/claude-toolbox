# Functional-review verification summary

> Updated: 2026-10-20 · feature verification complete (Tasks 13.1–13.6)
> Current source base: `70180071` plus Task 13 documentation/test-fixture changes
> Acceptance: Task 12 complete with disclosed limits; source review APPROVE and spec review CONFORMANT
> Release archive: not yet created or published; human-owned Task 13.7 remains open

## What is implemented

Ordinary `/kk:review-code` and `/kk:implement` invocations establish intended
behavior, affected contracts, relevant current/historical baselines and evidence
limits. Standard and isolated review share the functional method. Implementation
refreshes the actual review evidence and preserves unmet hard requirements.
Missing specifications do not reduce review to code quality alone; missing
operational evidence limits deployment conclusions.

The canonical implementation is in `klaude-plugin/`; Codex skills and agent
definitions are generated. The behavior is instruction-driven. Structure tests
verify packaging and helper behavior, not model reliability.

## Core comparison and provenance

The [compact result table](verification-results.md) retains every final assertion
grade from the 192-session core comparison: two providers, 24 case/mode
combinations, two source sides and two fresh repetitions. Values below are
**PASS / FAIL / PARTIAL** observations, including unavailable PAL components.

| Provider | Baseline | Candidate |
| --- | --- | --- |
| Claude | 189 / 114 / 1 | 251 / 49 / 4 |
| Codex | 203 / 96 / 5 | 264 / 30 / 10 |

Original baseline: `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`.
Core candidate: `581dd0e11455398cb73e3d6ae5542854c016fe7f`.
These are historical source identities, not the current source revision.

The frozen [core contract](verification/task12/opus55/run-contract.md) records:

- Claude Code 2.1.296, `claude-opus-5-5`/high main and forced reviewer;
  explicit allowed tools, `dontAsk`, normal hooks and isolated plugin/config inputs.
- Codex 0.162.1, `gpt-6-astra`/xhigh main and `gpt-6.1-sol`/xhigh named reviewer;
  workspace-write/never, fallback disabled and isolated plugin/config inputs.
- Capy 0.16.8; controller Python 3.12.11; actor Python 3.10.12; Linux.
  Fresh fixture/knowledge state; no real vault history.
- Revision-2 rubric; grader SHA-256
  `c2621b9a4f2f3e0d86cae6ec682b7ca1a2c729afb5da5cd9031873978b2dc342`.
  Independent configured `gpt-6.1-sol`/xhigh graders used sealed inputs.

The [freeze](verification/task12/opus55/freeze.json) identifies fixture, prompt,
oracle, instruction-bundle and controller hashes. Each package under
`verification/task12/opus55/grading/<run>/` contains its manifest and assertion/
source mapping; final grades are in `grades/`, earlier returns and corrections in
`grading-revisions/`. These paths also identify future archive members.

## Later evidence and current disposition

The following experiments have separate revisions and configurations. Do not
pool their grades with the core matrix or infer the isolated effect of a small
wording change from a pre-feature comparison.

| Evidence | Observed result | Retained decision |
| --- | --- | --- |
| [Entry-path correction](verification/task12/entry-path-no-pal/README.md), 12 Claude isolated sessions | Candidate 32 PASS / 8 FAIL; baseline 20 / 20. Required PAL portions remain failed. | Keep explicit instruction paths; targeted acquisition improved without certifying every mode. |
| [R7 wording comparison](verification/task12/r7-conclusions/README.md), 48 sessions | Effective candidate 147 / 21 / 0; baseline 95 / 72 / 1. | Wording rejected and reverted under its frozen rule. |
| [R7 validity diagnostic](verification/task12/r7-validity/README.md), four unchanged-skill Claude standard sessions | Material uncertainty and benign approval conclusions correct twice each; 23 PASS / 1 report-detail FAIL. | No additional R7 instruction change. |
| [R6 validity diagnostic](verification/task12/r6-validity/diagnostic/README.md), eight unchanged-skill standard sessions | Correct scoped decisions throughout; 58 PASS / 10 report-detail/follow-up FAIL. | Material exposure distinguished from a dormant inherited defect. |
| [Closure comparison](verification/task12/advisory-closure-execution/bootstrap-loading/comparison-result.md), 64 sessions | Effective candidate 202 / 30 / 0; baseline 163 / 57 / 12. Seven of eight final dormant advisories include an action. | Candidate rejected under its frozen rule and reverted; no reinstatement. |
| [Acceptance reassessment](acceptance-reassessment.md) and [I2/I3/I4 assessment](implementation-verification-assessment.md) | Material outcomes distinguished from quality observations and evidence limits; retrospective I2 suites pass 6/6 and 5/5. | Task 12 accepted with the limitations below; old grades remain unchanged. |

Later declaration/freeze records linked from each experiment retain their own
runtime, model, source and grading identities. The R6/closure work uses Codex
0.163.0 and Capy 0.17.3; these are not the core matrix's configuration.
`c4e4c027` records the authorized proportionality policy and `70180071` closes
the material-verification assessment. Neither commit claims a new actor comparison.

## Limits that remain

- Some agents abandon an explicitly configured verification route after a
  compound-command denial. Both historical I2 candidates left tests unrun and
  disclosed that limitation. Retrospective local tests do not complete those
  historical workflows or prove an unattempted command would have succeeded.
- Live PAL remains user-deferred. R8 is a synthetic report replay; current
  two-reviewer integration coverage is not certified.
- Exact submitted Codex handoff content and some instruction receipts remain
  unverified. No OS-wide confinement or statistical reliability is claimed.
- Legacy actor controls were not broadly rerun. The accepted policy retires that
  blanket gate; relevant future changes still need proportionate verification.
- The published instructions can guide functional reasoning but cannot guarantee
  detection of every bug or autonomous recovery in every session.

The maintainer of `/kk:implement` owns the documented recovery limitation.
Revisit it for a consequential normal-session failure, a false verification claim,
or changed recovery instructions; start from exact commands and permissions.
Optional follow-up, redundant report detail and historical red rows do not create
new acceptance gates. [ADR 0010](../../../adr/0010-proportionate-verification.md)
records the general learning.

## Final repository checks

All 12 `test/test-*.sh` suites pass: **757 helper assertions, zero failures and
zero skips**. `go test ./...` passes all three Go tool packages.
`make plugin-graph` passes its tests and reports no broken edges or orphans
(the existing cycle warning is nonfatal). Repeated `make generate-kodex` leaves
`kodex-plugin/` and `.codex/agents/` byte-identical to the committed output.
The compact core table matches all 1,216 source grades across 192 runs.
[Independent source review](reviews/final-source-review.md) approves and
[spec review](reviews/final-spec-review.md) is conformant, both without findings.
Tasks 13.1–13.6 are complete. These reviews assess source/evidence consistency;
their test and full-table reconciliation evidence is parent-attributed.

The pre-existing Codex hook-test issue is corrected using an explicit toolbox-only
fixture rather than the developer's live hook registration. Production hook
behavior and live configuration are unchanged. Initial environment failures
(PATH hiding `yq`, sandboxed cache/signing access) are distinct from that fixture
bug and remain described in Task 13's execution record.

## Release retention

Keep this summary, [compact core grades](verification-results.md), the current
design/task decisions, maintained evals and reusable tooling in Git. The complete
evidence tree currently remains in `verification/`; no files or Git history have
been removed. [The release handoff](release-archive-handoff.md) records the
inventory, proposed retention map and human execution sequence.

Release tag/URL, archive name, archive SHA-256, manifest and retrieval verification
are **pending**, not placeholders for a completed upload. Record those actual
values here when the feature's release exists. Task 13.7 prevents removing the
evidence tree before archive retrieval and retained-tooling checks succeed.
