# Calibration validity review

> Task: 12.20; independent fresh `design-reviewer`
> Final disposition: SOUND for calibration criteria and packets

The reviewer loaded review-design methodology and inspected the declaration,
calibration builder, all 25 packets and expected answers against the frozen
contract, R6 rubric and pinned grader. This authoring review may see expected
answers; actual calibration graders will not receive them.

The initial P1 finding identified conflicting controls 04/05: their complete
absent-advisory reports also omitted historical-setting limits, which should
trigger REJECT before the intended INCONCLUSIVE condition. Before any freeze or
dispatch, the parent added inspected scope, disabled-default context and explicit
unassessed historical/production settings without surfacing an advisory.
No-action controls 02/10 also retain the other required context, isolating the
follow-up failure. All intended expected outcomes remain unchanged.

Initial packets remain in `calibration-initial/`; corrected packets were rebuilt
and resealed. The reviewer confirmed the prior P1 resolved and returned SOUND
with no remaining findings. It checked 25 controls/69 assertions, unchanged old
verdicts/triggers, byte-identical copied manifests, matching original evidence
hashes and authoritative grader/contract copies. No packet manifest names the
controller-only expected-verdicts file. Dispatch instructions prohibit unrelated
source, other packets and expected-answer access.

This review did not run graders or verify service telemetry/access isolation.
Actual calibration outcomes and completion evidence remain separate.
