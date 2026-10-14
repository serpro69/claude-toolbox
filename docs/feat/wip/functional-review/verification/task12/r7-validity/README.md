# Task 12.14: R7 evaluation validity

Completed diagnostic, 2026-10-14. **Disposition: no further operative skill change
for the R7 compatibility concern.** Both material-case reports withhold target
readiness; both benign controls approve the supported increment. Independent
grading records **23 PASS / 1 FAIL / 0 PARTIAL**. This is not a complete diagnostic
pass or full-feature acceptance.

## What changed and why

The [audit](audit.md) separates actual old report claims from hypothetical provider
semantics. New canonical evals 19/R7M (`functional-material-provider-unknown`) and
20/R7B (`functional-benign-provider-contract`) use explicit contracts and identical
ordinary review prompts. R7M requires null-clearing support available in v2 but
absent in v1, with target version unknown. R7B preserves string semantics on both
supported versions. Oracles stay outside test-files; both distributions include
the new fixtures. Original eval 14 and all historical results remain unchanged.

The [prospective rubric](rubric.md) supplies meaningful positive/negative examples,
old-to-new assertion mapping, evidence rules and the decision boundary. It neither
amends the feature verdict table nor replaces original R7 for acceptance.
[Independent validity review](reviews.md) corrected one whitespace-definition
ambiguity before freeze, then returned SOUND.

## Measurement and results

The [run contract](run-contract.md) and [freeze](freeze.json) pin unchanged actor
revision `6bc277ea6d1ee023cb30a1246c983456eff86fdb`, separate successor fixtures,
rubric, grader, controllers and runtimes. Exactly four fresh Claude standard
sessions completed, two per case. The historical adapter's “candidate” label
means current unchanged source here; there is no baseline/improvement comparison.

| Case | Repetition 1 | Repetition 2 | Observed conclusion |
| --- | --- | --- | --- |
| R7M | 5 PASS / 1 FAIL | 6 PASS | COMMENT; target compatibility Unknown until provider v2 evidence is established |
| R7B | 6 PASS | 6 PASS | APPROVE scoped increment; source-level equivalence on v1/v2, no claimed live verification |

[Per-assertion results](results.json), [material 1](grades/claude-candidate-R7M-standard-1.md),
[material 2](grades/claude-candidate-R7M-standard-2.md),
[benign 1](grades/claude-candidate-R7B-standard-1.md) and
[benign 2](grades/claude-candidate-R7B-standard-2.md) retain independent judgments.
Four fresh eval-grader roles used pinned instructions, declared gpt-6.1-sol/xhigh,
fork_turns=none and only their sealed evidence packages. Controller dispatch files
identify each exact package and manifest hash. [Calibration](calibration/README.md)
matched all 20 expected verdicts across eight independent calibration agents.

**Retained failure:** R7M repetition 1 assertion 19.2 fails because the final
report omits the explicit `PUT /settings` endpoint from its behavior trace. It
correctly explains preserved saves, null/default semantics, v1 rejection, v2
support and the missing target version. The failure remains FAIL; 3/4 runs meet
every required assertion. This is a report-completeness issue, not the targeted
unsupported-readiness claim. Adding operative instructions for this omission is
not justified by its observed impact or instruction cost.

No concrete compatibility overclaim or invented benign blocker survives these
four clearer cases. That supports **no change for this slice**, without claiming
reliability, proving the old fixture invalid, identifying the cause of historical
reports or waiving any required acceptance condition. Owner of 19.2 disposition:
implementing agent. Revisit only if an omitted path obscures a material consequence
or a broader accepted evaluation requires a correction; retain this counterexample
and use a separately declared matched comparison for any later skill change.

## Verification and evidence limits

- Five fixture/adapter checks, four EPERM rejection controls and 18 inherited
  capture regressions pass: 27 checks, including all four snapshot suites (10
  fixture tests). The initial inherited host run failed five cases; the corrected
  controller-only Darwin handling passed before any actor launch.
- All 11 shell suites pass (645 helper assertions, zero failed). Go tests pass;
  plugin-graph reports no broken edges/orphans and retains its existing cycle
  warning. See [shell log](shell-checks.log), [Go log](go-checks.log) and
  [graph log](graph-checks.log).
- Repeated Codex generation preserves 926 files, aggregate SHA-256
  `c092113b43774a597255392def9dae13e33fd941aafcbcc9290615d3a9215d3a`.
  Only new eval files are added under canonical/generated plugins; tracked
  operative files and generated agents remain byte-identical to HEAD.
- The filtered source snapshot retains 447 files and excludes 1,368 evaluator
  files. Actual Claude bundle validation covers 229 files per workspace.
- The binding capture verifies selected-root delivery, complete normalized
  instruction text for parent/child, actual Opus 5.5 identities, Capy connected
  and PAL absent. The helper created packets in the host temporary directory;
  the binding actor used the direct-read fallback and did not read subject code.
- Real [state probes](state-probe/summary.json) establish empty separate Capy
  stores, index/search success, absent foreign markers and unavailable private
  vaults. No normal user knowledge or plugin/trust settings changed.
- Audits validate 144 sealed capture files across binding plus four runs, and
  342 manifest-listed grading files. All initial subject files are unchanged.
  Manual inspection of 35 shell requests and captured file requests finds no
  grading-material access. This is observed-access evidence, not OS confinement.
- Actor tool denials remain in original traces and grades use successful returned
  evidence, not requested calls. One report accurately discloses its denied
  randomized probe. The audit helper was corrected for string-valued runtime
  notices and expected plugin-root substitution; captures were never rewritten.

## Retention and outstanding feature work

The [runtime archive inventory](runtime-inputs.json) verifies 80 exact configuration/
packet files across 13 helper allocations; archive SHA-256
`e853c8543ce3c71c5c3897536f2d26587affe105520eceb87e32f32161d18df3`.
The first archive attempt rejected the host /var alias before creating an archive;
the successor normalizes only the standard /var/folders to /private/var/folders
alias and passed all hashes. Source archive, retained/excluded manifests, frozen
contracts, attempts, original captures, grading packages and results remain here.

Scratch workspaces and packets are deliberately retained until Task 13 evidence
housekeeping: /private/tmp/fr-r7-validity-20261014, the separate
/private/tmp/fr-r7-validity-state-20261014 probes, and the 13 paths enumerated in
runtime-inputs.json. These are redundant copies; durable evidence does not depend
on their survival. Owner: implementing agent during Task 13 preparation; verify
archive contents before deleting only the recorded owned scratch paths. No history
rewrite, release upload or repository-evidence removal was performed.

Original R7 acceptance, other Task 12 dispositions, live PAL (user-deferred),
legacy controls and Task 13 remain open. This diagnostic does not cover Codex,
isolated review, no-spec behavior, live deployments or exact reviewer handoffs.
[Final independent completion review](completion-review.md) approves closing
Task 12.14 with the retained failure. Its P3 calibration-path metadata finding
was corrected and independently rechecked; no open in-scope source finding remains.
No next implementation task starts automatically.
