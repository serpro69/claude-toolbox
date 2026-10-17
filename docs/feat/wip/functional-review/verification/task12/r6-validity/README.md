# R6 successor fixture authoring

> Task: [12.16](../../../tasks.md#task-1216-author-and-review-r6-material-exposure-and-dormant-control-evaluations)
> Date: 2026-10-17
> Status: authoring complete; subsequent eight-session diagnostic recorded separately

The user selected fixture/rubric authoring and independent review after the
[R6 assessment](../../../r6-assessment.md). This record owns the offline checks
and prospective criteria. It is not a run contract, frozen actor bundle or
acceptance result.

The user subsequently authorized [Task 12.17's diagnostic](diagnostic/README.md).
All eight sessions are captured and independently graded: **58 PASS / 10 FAIL /
0 PARTIAL**. This authoring record remains distinct from those measured results.

| Case | Canonical eval | Expected distinction |
| --- | --- | --- |
| R6M, eval 21 | [functional-inherited-defect-exposed](../../../../../../../klaude-plugin/skills/review-code/evals/functional-inherited-defect-exposed/eval.json) | Changed default reaches inherited division for empty batches; request changes for the new default-entry regression. |
| R6D, eval 22 | [functional-inherited-defect-dormant](../../../../../../../klaude-plugin/skills/review-code/evals/functional-inherited-defect-dormant/eval.json) | Label-only increment preserves reachability; approve its scope. Discovery is optional; surfaced advisories require accurate attribution and a bounded separate follow-up. |

Each case has complete before/after trees, a natural review prompt, required
assertions and a separate grader-only oracle. Both use identical reporting logic
with visible mean output and explicit per-call overrides. The [rubric](rubric.md)
defines evidence boundaries, conditional-trigger accounting, pre-run examples and
the mapping from original R6. Optional discovery is an explicit prospective
decision for R6D under the user-approved authoring scope, subject to validity
review; it changes no original assertion or grade.

## Offline verification

Run from the repository root with its existing Python/Git/Bash tooling:

```bash
python3 -B docs/feat/wip/functional-review/verification/task12/r6-validity/test_fixtures.py
```

The controller-only [test suite](test_fixtures.py) checks case IDs and complete
file manifests, intended diffs, shared implementation, all four supplied snapshot
suites, actual boundary outcomes, and the production staging helper against both
snapshots. Staging uses fresh temporary directories outside any `SKILL.md`
ancestor, preserves original Git-base contents, and admits only subject files.
Neither the rubric, this suite nor oracles belong in actor inputs. Future actors
also require filtered instruction bundles under the existing isolation contract.

## Results

| Check | Observed result |
| --- | --- |
| `python3 -B .../r6-validity/test_fixtures.py`, Python 3.10.12 | 6 controller tests PASS, including 4 supplied snapshot suites × 4 tests, 32 outcome comparisons and both cases through the real staging helper. |
| `make generate-kodex`, with installed Python 3.12.11 on PATH | PASS; generator tests and plugin/Codex structure checks pass (223 + 29 assertions). |
| Generation freshness | Two completed generations produce identical hashes across 958 generated files; no existing generated file or agent definition differs from HEAD. The only additions are the 32 successor eval files. |
| Remaining shell suites | 9 suites PASS, 434 assertions, no skips. Combined with the two structure suites: 11 suites PASS, 686 assertions. The twelfth suite has the separate pre-existing failure below. |
| `make plugin-graph` and `go test ./...` | PASS. Graph reports no broken edges/orphans and retains its existing cycle warning. |
| Documentation and whitespace | Local file/heading links and `git diff --check` pass. |
| [Independent source/validity review](review.md) | APPROVE, no findings; source inspection, not independent execution or actor measurement. |

The inherited defect is deliberately retained. Passing controller tests establish
the fixture's intended contrast, not skill performance, grader calibration or
feature acceptance. Original R6/R7, capture evidence and operative instructions
remain unchanged. Live PAL remains user-deferred; no actor runtime/provider/batch
has been selected.

## Environment attempts and unrelated test follow-up

The first sandboxed `make generate-kodex` stopped when it could not rewrite the
protected `.codex/agents` directory, after clearing generated skills/profiles.
The authorized rerun restored all output. Its structure checks then reported
seven TOML parse failures because default Python 3.10 had neither `tomllib` nor
`tomli`. Using the already installed Python 3.12.11 resolved those checks; no
dependency, persistent setting or test assertion was changed. Generation
freshness compares the completed outputs, not the interrupted state.

**Open unrelated test issue — owner: repository test maintainer / next implementing
agent.** `test/test-codex-hooks.sh` stops at Section 3, “Legacy: curl is denied,”
with expected `permissionDecision: deny`, actual empty output. The test initializes
`TOOLBOX_HOOKS` from the repository's `.codex/hooks.json` and assumes that file
contains toolbox entries only. The file at HEAD `6093213a` already contains Capy
`codex-launch` entries for PreToolUse, so the unchanged hook correctly takes its
registered-Capy pass-through branch. The same failure reproduced in a disposable
directory containing the unchanged test/helper/scripts/hooks files; those inputs
have no diff against HEAD. This is not a full-repository-green result.

Deferred here because this task authors R6 evaluations and does not change hook
routing or its tests. Next action: construct an explicit toolbox-only test fixture
instead of assuming the configured repository file is toolbox-only; preserve
registered/missing/malformed/per-event cases. Verification condition: the complete
hook suite passes with the live repository configuration untouched, then rerun
the full shell suite. This deferral does not waive any feature acceptance gate.

## Completion boundary

Task 12.16 is complete as fixture/rubric authoring with independent review. The
subsequently authorized diagnostic used unchanged instructions, filtered actor
inputs and calibrated grading; its [record](diagnostic/README.md) preserves all
remaining failures and follow-up dispositions. Conditional absent-trigger passes
must not count as exercised capability. No further run or patch is selected;
original R6 acceptance, PAL, legacy actor controls and Task 13 remain open.

Optional wording pass: `/kk:clarify-docs` on this record and `rubric.md`.
