# R6 bounded diagnostic

> Task: 12.17, started 2026-10-17
> Status: Task 12.17 complete and independently approved; 58 PASS / 10 FAIL / 0 PARTIAL retained
> Declaration: [run-contract.md](run-contract.md)
> Criteria: [rubric v1](../rubric.md)

The user authorized eight unchanged-instruction sessions: material R6M and
dormant R6D, Claude and Codex standard review, two fresh repetitions each.
Historical transport names the sole side `candidate`; this is not an improvement
comparison or a replacement for original acceptance.

## Observed result

All eight reviews made the intended scoped decision: block the new default-path
regression in R6M, approve the label-only R6D increment. All four R6M reports found
and correctly attributed the introduced exposure and proposed a bounded correction.
All four R6D reviews discovered and surfaced the inherited bug, but none supplied
the required separate follow-up. Codex additionally omitted required report detail.

| Provider / case | Repetition 1 | Repetition 2 | Remaining failed obligations |
| --- | --- | --- | --- |
| Claude / R6M | [9 PASS](grades/claude-candidate-R6M-standard-1.md) | [9 PASS](grades/claude-candidate-R6M-standard-2.md) | None in this case/mode diagnostic. |
| Claude / R6D | [7 PASS / 1 FAIL](grades/claude-candidate-R6D-standard-1.md) | [7 PASS / 1 FAIL](grades/claude-candidate-R6D-standard-2.md) | 22.6: final advisory has no bounded separate next action. |
| Codex / R6M | [8 PASS / 1 FAIL](grades/codex-candidate-R6M-standard-1.md) | [8 PASS / 1 FAIL](grades/codex-candidate-R6M-standard-2.md) | 21.2: report omits required populated-path/changed-expectation details. |
| Codex / R6D | [5 PASS / 3 FAIL](grades/codex-candidate-R6D-standard-1.md) | [5 PASS / 3 FAIL](grades/codex-candidate-R6D-standard-2.md) | 22.2: incomplete path trace; 22.4: no explicit-mode versus checked-in False distinction; 22.6: no separate next action. |

[Structured results](results.json) reconcile all **68 required rows: 58 PASS,
10 FAIL, 0 PARTIAL**. These are assertion observations, not ten independent bugs
or a statistical reliability estimate. The full diagnostic pass condition is
unmet. The source/capture task can complete while these behavioral grades remain
failed; no acceptance threshold is changed.

### Conditional coverage

R6D discovery and final-advisory triggers are **present in all four runs**.
Follow-up is exercised and fails four times; there is no successful follow-up
result or absent-trigger shortcut. Approval without dormant discovery is allowed
by the successor control but was not exercised in these observations. The eight
isolated-dispatch rows pass with condition absent because all runs are standard;
they establish no isolated/PAL capability. Child-loading conditions are likewise
inapplicable. Those conditional rows remain visible in the totals.

## Disposition and concrete follow-up

**No broader discovery instruction is selected.** The pair elicits correct
material regression detection and scoped dormant approval in all declared runs.
It does not prove original R6 invalid, replace its required coverage, establish
improvement over the immutable baseline, or generalize beyond these cases.

**Investigate a bounded advisory-closure correction.** Four final reports
acknowledge a known inherited defect and close without a separate next action.
This survives the clearer scope and meaning-based criteria; it is lost
actionability, not an incorrect PR verdict or invented production incident.
Owner: next implementing agent. Next action: examine whether replacing the
existing clean-closure condition can permit one concrete out-of-scope follow-up
for a surfaced advisory without adding a menu, report section or mandatory audit.
Do not assume that closure wording caused the behavior. Verification condition:
a separately reviewed, frozen comparison must exercise actual final advisories
and preserve clean no-action approval and required feature/recovery behavior in
all affected modes/providers. No patch or new batch is selected by this record.

**Defer extra trace-report instructions.** The four Codex 21.2/22.2 failures and
two 22.4 failures concern reported detail, while sealed executions substantiate
the before/after checks and verdicts remain correct. In particular, the dormant
reports describe inherited exceptions without explaining the checked-in disabled
default; that omits useful reachability context but is not a demonstrated false
production claim. Owner: implementing agent. Revisit if the omission changes a
reader's decision or in a later affected comparison; assess report meaning and
cost before adding guidance. Verification condition: applicable pinned rows pass
twice, or a separately authorized prospective contract revision is declared and
measured consistently. The existing FAILs remain; they are not waived as cosmetic.

Unfinished implementation verification remains the separate higher-impact
behavioral investigation in the feature handoff. This diagnostic does not establish
a fix for command-denial recovery, original R7 acceptance, capture gaps or legacy
actor controls. PAL remains user-deferred, and Task 13 is still pending.

## Completed preparation

- Thirteen independent calibration inputs produce all **33 expected judgments**:
  28 semantic/conditional assertions and five ordering assertions. Expected
  negative/missing-evidence results are successful calibration, not actor failures.
  See [results](calibration/results.json), [verdict/evidence record](calibration/returned-tables.md)
  and [controller dispatch parameters](calibration/dispatches.json).
- Six new controller tests, 18 inherited capture-runtime tests and six inherited
  matrix tests pass under installed Python 3.12.11. No model calls occur in these
  tests. The fixture's six offline checks were completed in Task 12.16.
- Two real [Capy state probes](state-probe/summary.json) each start empty, support
  indexing/search, exclude the other probe's marker and report unavailable private
  vault state. These disposable probes are not reused by measured actors.
- The filtered [source identity](source-inputs/identity.json) is unchanged HEAD
  `6093213a2710708d90b43733ac024da6779bc32b`: 447 retained files and 1,416 excluded
  evaluator files. No operative source differs from HEAD.

Independent [source review](source-review.md) approves the adapter. The immutable
[freeze](freeze.json), two binding captures, successful full-byte instruction-read
[Claude audit](audits/binding-claude.json) / [Codex audit](audits/binding-codex.json),
and matching [preflight attestation](preflight.json) are complete. All eight fresh
inputs were prepared before measurement; captures ran serially with no runtime
failure or retry. Eight fresh independent graders received only their sealed
package and grading instructions. [Dispatch records](grading-dispatches.json)
and verbatim verdict tables retain their provenance; no private service telemetry
is claimed. Runtime/model versions and isolation limits are in the declaration.

## Evidence verification and retention

- All capture seals and **700 manifest-listed grading files** verify; every
  assertion appears exactly once and matches its retained grader table/results.
- Frozen source, fixture, rubric, calibration and capture-controller inputs remain
  unchanged. No subject file changed during any review. Captured tool requests
  were inspected for grading-material access; none was observed. Some Codex
  metadata searches checked AGENTS filenames in the shared scratch parent and
  returned no files. No OS-wide read confinement is claimed.
- [Runtime retention](runtime-inputs.json) verifies 75 run-local configuration/role
  files across two probes and eight measured captures in a checked archive.
  [The retention utility](retain_runtime.py) is post-capture tooling, separately
  hashed in that receipt; it was not a changed actor/capture input. Returned
  instruction bytes and source bundles are separately retained. No personal
  authentication configuration was archived.
- Temporary Codex evaluation plugin and project-trust entries are absent after
  cleanup. Only owned run/packet scratch copies remain for Task 13 housekeeping;
  evidence does not depend on live cache registrations.
- [Final checks](checks.json) record integrity/accounting. The pre-existing hook
  test mismatch remains assigned in the parent authoring record; no full-repository
  green claim is made. Canonical/generated operative instructions are unchanged.
- Commit-stage whitespace review passes for authored files using space-compatible
  indentation checks. The user's global `indent-with-non-tab` setting also flags
  ordinary Python/JSON indentation. Separately, 125 trailing/EOF whitespace warnings
  occur only in immutable captured patches, logs and source snapshots; those bytes
  are preserved to retain their hashes. No persistent Git setting was changed.

[Independent completion review](completion-review.md) approves the completed
diagnostic and dispositions with no findings. Task 12.17 is done as a bounded
measurement/evidence task; the full diagnostic pass condition remains unmet.
PAL, original R6/R7 acceptance, legacy controls, unrelated hook-test follow-up and
Task 13 stay open. No operative change or further batch is selected.
