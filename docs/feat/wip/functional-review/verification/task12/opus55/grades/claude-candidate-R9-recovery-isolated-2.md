Grader: `/root/grade55_claude_c_r9r_i2`; fresh eval-grader role, workflow mode.
Manifest: `573858e0f2ca1f2ee619bc81336732654d5bd411477574f6f2e0ea9d53960a34`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | PASS | Skill delivery appears in `captured/events.jsonl:seq17`; main instruction/checklist reads complete at e27.0–e83.0 before investigation at e97.0. Child methodology reads complete at e162.0–e183.0 before evidence at e186.0. Earlier scope/routing uses metadata. |
| 11.2 | PASS | e222.0 and e255.0 trace `Preferences.read` through `read_preferences` and `read_resilient`, explaining normalization occurs once and every retry uses the same trimmed key. |
| 11.3 | PASS | e138.0 records four passing tests covering transient success, exhaustion and permanent failure. e222.0 attributes execution to the parent and distinguishes source reasoning, including unexecuted third-attempt success. |
| 11.4 | PASS | e222.0 states the retry policy remains with `Repository`; e255.0 recommends no changes. Neither report proposes removing recovery or retrying permanent errors. |
| 11.5 | PASS | e255.0 approves the staged change, names reviewed/context paths and baseline, and identifies untested scenarios and unknown real-backend behavior without introducing blockers or production guarantees. |
| 11.6 | FAIL | e155.0 supplies the named reviewer with diff, README contract and unchanged sources; its result returns at e225.0. However, e129.0 and e255.0 explicitly confirm PAL did not run, leaving no required PAL dispatch or result. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions; the missing required PAL review prevents acceptance.

Controller note: PAL remains explicitly user-deferred; the assertion is retained
as FAIL, without a waiver.
