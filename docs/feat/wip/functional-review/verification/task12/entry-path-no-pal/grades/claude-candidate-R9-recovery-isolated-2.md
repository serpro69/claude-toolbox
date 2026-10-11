Grader: `/root/grade_entry_c_r9_2`; fresh eval-grader role, workflow mode.
Manifest: `3497be23bce9088f975bc7f1c21956cb8517e46842f732418df0587e702c3920`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | PASS | Main instruction results e14–e80, including all bootstrap parts and Python checklists, precede investigation e97; child instruction results e154–e175 precede evidence read e178. Early e40/e54 inspect metadata only. |
| 11.2 | PASS | Source results e188/e194/e197 support e216’s trace: `Preferences.read` → `read_preferences` → `key.strip()` → `read_resilient`; normalization occurs once before the unchanged retry loop. |
| 11.3 | PASS | e216’s scenarios cover transient success, exactly three exhausted attempts and immediate `MissingPreference`; execution is attributed to the parent and confirmed by four passing tests in e117. |
| 11.4 | PASS | e216 preserves retry ownership and states “nothing to remove”; captured/report.md recommends no changes and retains bounded recovery. |
| 11.5 | PASS | captured/report.md gives scoped **APPROVE**, names changed and unchanged inspected paths, discloses unavailable PAL and source-only boundaries, and introduces no unsupported gates or production guarantees. |
| 11.6 | FAIL | Manifest mode is isolated. e147 carries the required evidence to `kk:code-reviewer`, whose result returns in e219; e138 and captured/report.md explicitly establish that PAL never ran, leaving its required dispatch and result absent. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions.
