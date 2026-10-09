# Task 4 verification

Status: Task 4 implementation slice complete, independently reviewed and audited. The final candidate demonstrates the specified R1 behavior and instruction-before-investigation gate. Full procedural compliance and paired matrix acceptance are not claimed.

The [run contract](run-contract.md) was declared before launch and amended before each new candidate/probe. [Original candidate origin](candidate-origin.json), [patch](candidate.patch), [identity](identity.json), source/retained manifests and exclusions identify candidate1. [Candidate2](candidate2/) binds final instruction snapshot `d0ab5f0122724c050c2ecbd4563bb6e6fce2b68c`. The repository branch was not committed by this task. Baseline captures and frozen seed/rubric bytes remain unchanged.

## Local evidence

- [Checks](checks.json): nine shell suites, 640 passing assertions, no skips. Raw outputs are in `checks/`.
- [Packaging mutations](mutation-checks.json): regular-file replacement, wrong/broken symlink targets and both oversized instruction files are rejected in disposable copies.
- Generation and structure checks pass. The second generation preserved hashes of all 684 generated files.
- Plugin graph validation passes with a cycle warning, no broken edges or orphans; the warning is preserved in `checks/graph.txt`.
- Fresh Capy isolation probes passed in `state-probe/summary.json`: independent empty stores, working index/search, absent foreign marker and unavailable vault.
- After the loading-checkpoint correction, generation/structure checks, graph validation and the second-generation comparison passed again. Current canonical/generated/agent files match candidate2's frozen source manifest.

## Captures and observed results

| Capture | Observation |
| --- | --- |
| `binding/` | Incomplete: entry/common-method reads succeeded, but attempted root commands were outside the fixed allowlist; root was inferred only. |
| `binding-retry/` | Candidate1 binding supported: the permitted `printenv TOOLBOX_PLUGIN_ROOT` returned the selected filtered root; all requested shared-method reads succeeded. |
| `r1-standard-1/` | Defect found, but ordering failed: diff request 38/result 41 preceded Python checklist reads 49–56. Later loading does not repair this trace. |
| `binding2/` | Final candidate binding supported: observed root result 12, registered skill result 13, common instruction results 19–32. |
| `r1-standard-2/` | Final candidate's Task 4 dry-run supported: common reads and applicable Python checklists completed before diff investigation; documented ownership regression reproduced and reported. Procedure/severity limits below remain open. |

The initial automatic approval rejection preceded execution. The user then explicitly authorized Task 4 Claude/PAL verification. A later rejection of candidate2 was resolved by comparing the manifests and exact delta: only two instruction files and their generated equivalents changed, with no new payload paths, fixture changes, destination, model or permission changes. The same approved launcher then ran; no indirect workaround was used.

Each capture retains its actual command, ordered public events, report, initial/final subjects, hashes and redaction record. All sealed hashes were verified; initial/final subjects are identical. Copied actor bundles passed post-run manifest checks. Read/command audit found no evaluator-material access. Private reasoning is omitted. Run-local Capy returned the expected empty-store result before successful indexing; no real knowledge/vault state was inherited.

## Final R1 evidence and limits

See [the report](r1-standard-2/report.md), [event inventory](r1-standard-2-event-index.json) and authoritative [public events](r1-standard-2/events.jsonl):

- Common instruction read results: 13–23. Python checklist results: 46–52. Loading checkpoint: 57. First behavioral diff/index request: 58, returned at 61.
- Unchanged setup/store/tests and README reads: 88–95. The README explicitly permits failed setup A's queued cleanup after successful setup B, and excludes concurrency/external services.
- Actual test/reproduction command: 111, result 114. Both existing tests pass; the documented cleanup interleaving yields `active_connection == None` instead of `connection-two`.
- Final report: 140 (also retained by the result record). It locates `cleanup.py:3`, explains the ownership regression and green-test gap, recommends restoring the ownership guard, and returns REQUEST_CHANGES without unrelated deployment or concurrency machinery.

The actor did **not** enumerate every known profile or query `kk:lang-idioms`; record these as failed procedural observations, not successful compliance. Its P0 severity is not validated/calibrated by this audit and differs from the oracle's suggested P1 or justified P2. Owner: implementing agent in Task 12. Next action: run the existing routing regression controls, verify omitted procedure steps, and grade impact/severity under the pinned workflow grader; correct instructions and recapture affected cases as needed. These limits do not erase the observed Task 4 behavior, and they must not be silently treated as full-workflow acceptance.

The Task 8 concrete grader is still pending. The existing frozen rubric and later two-fresh-run paired matrix remain mandatory. These are descriptive observations of two different intermediate candidates, not two passing repetitions or a claim of reliable model-family behavior.

## Independent review

The isolated code-reviewer inspected the original 16-file patch, candidate2's four-file delta, unchanged scope/detection/spec-review consumers, and the final sealed execution evidence. It approved the Task 4 implementation slice with the explicit limits above, finding no hard Task 4 closure blocker or actionable source defect. No systemic P0/P1 implementation finding requires indexing. PAL's two LOW suggestions and unverified source coverage/isolation are preserved in [review.md](review.md); no corroboration is claimed.
