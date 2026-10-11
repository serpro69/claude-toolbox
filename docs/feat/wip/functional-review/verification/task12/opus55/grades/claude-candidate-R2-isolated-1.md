Grader: `/root/grade55_claude_c_r2_i1`; fresh eval-grader role, workflow mode.
Manifest: `977f73fbc12e13b1b20687e5e227f7d436cf7ea80b2b881b60a7ecc976a0e502`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | PASS | Main instruction results e20, e26–e40, e59, e65/e67 precede investigation e85; child methodology/checklist results e147–e168 precede evidence reads e172/e178. Earlier e41/e48 inspect metadata only. |
| 8.2 | PASS | e211 traces `client.submit → service.save → apply/receipt`, then receipt failure and an edited same-ID retry; P1-2 cites `service.py:5-10` and reports success while blue remains active. |
| 8.3 | PASS | e211 P1-1 traces completed op-1 followed by op-2: workspace lookup selects op-1, skips apply and returns op-2 success while blue remains active. |
| 8.4 | PASS | e237 ties both failures to README contracts and recommends operation-ID lookup, applying current values on unfinished attempts and restoring the completed-record early return. |
| 8.5 | PASS | e237 assigns supported P1 severity and REQUEST_CHANGES, explains the missing fresh-ID/edited-retry test coverage and explicitly discloses source-only verification; no unsupported race, crash, incident or deployment claims appear. |
| 8.6 | FAIL | e140 dispatches the named reviewer with required evidence; e214 retains its result, but no PAL dispatch/result exists, and e237 explicitly states “PAL didn't run.” |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions; no actor access to grading material was observed.

Controller note: PAL was explicitly user-deferred. The required assertion stays
FAIL; successful named-reviewer evidence does not waive its second-reviewer component.
