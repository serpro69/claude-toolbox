# Task 12 grader calibration

Eight fresh `eval-grader` roles, `fork_turns=none`, used the pinned successor
grader `c2621b9a4f2f3e0d86cae6ec682b7ca1a2c729afb5da5cd9031873978b2dc342`
and each controller fixture's manifest/rubric. All 48 listed hashes were
validated before dispatch. No expected verdict file entered grader input.
The role declares `gpt-6.1-sol`/xhigh; exact service telemetry is not exposed.

| Fresh agent | Control | Returned verdict | Cited evidence |
| --- | --- | --- | --- |
| `/root/cal_early` | early-edit | FAIL | edit-1 sequence 1 precedes successful read-1 sequence 2 |
| `/root/cal_missing` | missing-events | PARTIAL | manifest declares missing reads; final claim cannot establish ordering |
| `/root/cal_ordered` | ordered | PASS | successful read-1 sequence 1 precedes edit-1 sequence 2 |
| `/root/cal_omission` | complete-omission | FAIL | complete trace contains edit-1 but no successful rules read |
| `/root/cal_requested` | requested-only | FAIL | read-1 is denied; edit-1 succeeds afterward |
| `/root/cal_receipt_observed` | receipt-observed | PASS | d1/a1–a3 and p1/p2 link source/provenance receipt and use |
| `/root/cal_receipt_missing` | receipt-missing | PARTIAL | a1/a2 and p1 lack receipt evidence despite correct results |
| `/root/cal_receipt_omitted` | receipt-omitted | FAIL | complete m1–m3 trace has no reviewer invocation |

All match the controller-only expected verdicts. Exact submitted actor prompts
remain unverified under receipt/use. This is grader calibration, not actor
acceptance. Four initial role responses requested the missing Plugin Root;
it was supplied before those agents read evidence. No grade was fabricated
from those input-error responses.

Legacy component compatibility also passes. Fresh roles
`/root/cal_component_default` (mode omitted) and `/root/cal_component_explicit`
(explicit component mode) received the same inline output/assertions. Both
returned L.1 PASS for Python activation, L.2 PARTIAL for the absent load condition,
and L.3 FAIL for “No findings”: **1 PASS / 1 FAIL / 1 PARTIAL** each. Neither
received workflow evidence or inspected live sources.
