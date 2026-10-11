Grader: `/root/grade55_claude_b_r4_i2`; fresh eval-grader role, workflow mode.
Manifest: `344768797d3dcdda479c9a4d17309047c199df9838772ae7be6872dda416b7d8`.

| id | verdict | evidence |
|----|---------|----------|
| 9.1 | FAIL | e43.0/e44.0 read the full README contract before completing shared protocols or profile detection; `event-index.json` records no such instruction reads. |
| 9.2 | FAIL | `event-index.json` records no reads of the persisted records or unchanged callers; e50.0 states “I stopped before running any review” and identifies no compatibility regression. |
| 9.3 | FAIL | e50.0 contains no mixed-snapshot or one-record-batch failure, `KeyError`, or fully migrated control. |
| 9.4 | FAIL | e44.0 supplies the hard compatibility contract, but e50.0 reports tooling obstacles without a compatibility combination marked Blocked or REQUEST_CHANGES. |
| 9.5 | FAIL | e50.0 proposes allowing Bash or supplying a diff; it gives no dual-shape remedy or explicit delivery-contract change. |
| 9.6 | FAIL | Manifest mode is isolated; `event-index.json` records neither named-reviewer nor PAL dispatch, and e50.0 confirms the review stopped without reviewer results. |

**Summary**: 0 PASS / 6 FAIL / 0 PARTIAL of 6 assertions; no evaluator-material access was observed.

Controller note: retained early-stop response under the declared permission
policy. PAL was deferred; missing named-reviewer and behavioral work remain failed.
