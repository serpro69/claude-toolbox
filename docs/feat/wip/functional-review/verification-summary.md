# Functional-review verification summary

> Updated: 2026-10-20 · feature verification complete (Tasks 13.1–13.6)
> Current source base: `70180071` plus Task 13 documentation/test-fixture changes
> Acceptance: Task 12 complete with disclosed limits; source review APPROVE and spec review CONFORMANT
> Archive: local and draft-release copies verified; human reference repair and cleanup remain under Task 13.7

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

Task 13.7 preparation has now extracted the reusable tools to
[`scripts/functional-review-evals/`](../../../../scripts/functional-review-evals/README.md).
All 15 offline checks pass on Python 3.11.13 and 3.12.11 from copies outside the
repository; all 13 shell suites pass. Independent source review approves after
fixing a receipt-retention regression. These are tooling checks, not new actor
evaluations or completed release housekeeping.

[The source-input audit](archive-source-audit.md) identifies a recoverable core
source export and unavailable early inputs: 18 distinct source hashes remain
unmatched in the examined evidence files/archive members. On 2026-10-20 the user
accepted this limitation on exact replay and retired the recovery gate.
Archive the retained evidence, compact records and available core export using
the [command guidance](release-archive-commands.md). Missing temporary inputs are
not represented as recovered. The user then approved preparing and verifying a
local archive under the project's ignored `.local-archives/functional-review/`
directory before cleanup. A release/tag is not needed for that work; release
upload and download verification follow cleanup and release creation.

The local archive is now verified at
`.local-archives/functional-review/20261020T171149Z-9fa9906a/functional-review-evidence-20261020T171149Z-9fa9906a.tar.gz`
(project-relative, ignored by Git; 188,522,487 bytes).
SHA-256: `ce99e6e69bcb6a266573e69ad9a561d3c891a343d90568abe8fe39efd191149d`.
The same directory contains the `.manifest.json` and `.sha256` companions.
Archive members begin with `payload/`; original evidence is under
`payload/docs/feat/wip/functional-review/verification/`.

Checksum and complete extracted-member verification pass: 73,126 regular files,
66 symlinks and 9,544 directories. The extracted evidence subtree matches every
original evidence inventory entry, with only recorded cache exclusions.
The [handoff](release-archive-handoff.md#verified-local-archive--2026-10-20)
retains detailed hashes, provenance and the assembly-time document-snapshot limit.
Local archive and retained-tooling prerequisites are complete. The user then
selected an existing draft release for immediate upload before cleanup.

All three functional-review assets are now attached to
[v0.24.0](https://github.com/serpro69/claude-toolbox/releases/tag/v0.24.0), currently a draft
(release ID `418689774`), along with the eight other feature archive sets.
All 27 downloaded files match their original checksums, and all nine downloaded
archives pass extracted-member verification. The
[asset receipt](../../../archives/feature-evidence/release-assets.json) supplies
exact filenames, asset IDs and download/API URLs; member paths above are unchanged.
The user specified v0.24.0 as the publication target, so canonical release/asset
links use that tag. Verification was performed against the existing draft;
its observed identity and authenticated asset API URLs remain in the receipt.
No release promotion or remote tag change was performed. Human reference repair,
evidence removal and history cleanup remain.
No cleanup, history rewrite or draft publication has been performed.
