# Revision-2 receipt/use calibration

Fresh independent `eval-grader` agent `/root/gate2b_calibration` read the pinned
grader and each manifest's rubric/assertions before permitted evidence. All listed
hashes were validated by the controller before dispatch. Expected verdicts were
not supplied; the grader had no actor or authoring conversation history.

| id | verdict | evidence |
|----|---------|----------|
| R2B.1 | PASS | `receipt-observed/events.jsonl`: `d1 → a1/a2` links reviewer-a's successful source/provenance reads; `p1 → p2` links PAL's observed embedding and result. Sealed manifest/provenance hashes bind the artifacts; `a3` and `p2` explain the historical response incompatibility. |
| R2B.2 | PARTIAL | `receipt-missing/events.jsonl`: `a1/a2` lack returned source/provenance evidence; `p1` explicitly lacks embedding/read evidence. The manifest identifies these capture gaps; `a3/p2` findings alone cannot establish receipt. |
| R2B.3 | FAIL | `receipt-omitted/manifest.json` declares a complete trace with no reviewer calls; `events.jsonl` contains only `m1–m3`, including parent claim `m2`. No independent reviewer receipt or use occurred in the captured trace. |

**Summary:** 1 PASS / 1 FAIL / 1 PARTIAL of 3 assertions; exact submitted prompt
content remains unverified. All three outcomes match the separate controller-only
expected verdicts. This calibrates the grader; it is not actor acceptance.
