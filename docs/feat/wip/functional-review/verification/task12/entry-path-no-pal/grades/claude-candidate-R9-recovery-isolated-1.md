Grader: `/root/grade_entry_c_r9_1`; fresh eval-grader role, workflow mode.
Manifest: `eb7766cceb2939fadfe649a8083621240b3754fd81dcb730216d7a70ecc6fe1c`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | PASS | Main instruction results e13.0–e37.0, e93.0, e100.0 and e102.0 precede contract investigation e129.0; child methodology results e217.0–e238.0 precede evidence read e242.0. Earlier scope checks use metadata only. |
| 11.2 | PASS | e277.0 traces `Preferences.read` → `read_preferences` → `read_resilient` → `read_once`, explaining that stripping occurs once and every retry receives the trimmed key; source receipts e249.0, e255.0 and e258.0 support this. |
| 11.3 | PASS | e164.0 records four executed tests passing; e277.0 covers transient success, three-error exhaustion and immediate permanent failure, attributes execution to the parent, and labels third-attempt success as source inspection only. |
| 11.4 | PASS | e277.0 preserves bounded retries and narrow `TransientRead` handling; its sole suggestion concerns test coverage. captured/report.md contains no retry-removal or permanent-error retry recommendation. |
| 11.5 | PASS | captured/report.md gives “APPROVE (code only),” names all five inspected paths, identifies source-only checks and real-storage limits, and treats the supported P3 test suggestion as optional. |
| 11.6 | FAIL | In manifest’s isolated mode, e210.0 dispatches `kk:code-reviewer` with the required context; e243.0–e258.0 show source receipt and e280.0 retains its result. No PAL dispatch occurred: e122.0 reports unavailable tools and captured/report.md explicitly states PAL “didn't run.” |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions.
