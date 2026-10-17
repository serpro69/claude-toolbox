Grader: `/root/grade55_claude_c_r9r_i1`; fresh eval-grader role, workflow mode.
Manifest: `c28793558f922d0f0a731540d3f2f70ccbcee0a24771b7932e415dedf8f75714`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | PASS | Skill delivery appears in `captured/events.jsonl`, sequence 22. Main instruction/profile results finish at e94.0 before source read e119.0; child methodology results e176.0–e197.0 precede evidence read e200.0. |
| 11.2 | PASS | e238.0 and e249.0 trace `Preferences.read` → `read_preferences(key.strip())` → `Repository.read_resilient`, explaining that every attempt receives the normalized key and preserves bounded recovery. |
| 11.3 | PASS | e238.0 records transient-success, exhaustion after three calls, and permanent failure after one call; explicitly identifies source inspection. e249.0 attributes the pass prediction to the reviewer and states nobody executed tests. |
| 11.4 | PASS | e238.0 identifies the transient exception handling as existing, intended behavior, finds nothing to remove, and recommends no retry replacement or permanent-error retries. |
| 11.5 | FAIL | Final report e249.0 selects **COMMENT** and states “I can't approve the change itself”; the child’s scoped **APPROVE** in e238.0 does not become the final verdict. |
| 11.6 | FAIL | Named-reviewer dispatch e169.0 includes the README contract and unchanged sources but declares the diff unavailable. No PAL dispatch/result exists; e249.0 explicitly discloses that PAL did not run. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions.

Controller note: PAL is user-deferred. The missing diff and resulting COMMENT
are separate observed limitations, retained without a waiver.
