Grader: `/root/grade55_codex_b_r6_i2`; fresh eval-grader role, workflow mode.
Manifest: `2451cc83a25be13576b010ea850c863b8bb13a106ceb8cb4b30f449c9dc0aca7`.

| id | verdict | evidence |
|----|---------|----------|
| 13.1 | PASS | events/0003–0010.json record completed methodology/profile reads before behavioral investigation in events/0012–0013.json; child checklist reads in events/0027–0030.json precede source reads. |
| 13.2 | PASS | events/0013.json captures the label/test diff and full call chain with `DETAILED_REPORT=False`; events/0018.json traces references; events/0040.json confirms calculations remain unchanged. |
| 13.3 | FAIL | events/0025.json and events/0040.json report no findings and never identify the inherited empty-input division-by-zero defect. |
| 13.4 | FAIL | events/0040.json acknowledges the checked-in False setting and unverified historical settings, but omits the local `summarize([], detailed=True)` failure condition. |
| 13.5 | PASS | events/0025.json and events/0040.json approve the scoped change without unrelated repair requirements; manifest initial/final hashes confirm subject files remain unchanged. |
| 13.6 | FAIL | captured/command.json records PAL disabled; events/0025.json confirms only one independent reviewer ran. Exact submitted handoff plaintext remains unverified. |

**Summary**: 3 PASS / 3 FAIL / 0 PARTIAL of 6 assertions.

Controller note: PAL is user-deferred; missing the inherited defect and its
failure condition are separate behavioral failures.
