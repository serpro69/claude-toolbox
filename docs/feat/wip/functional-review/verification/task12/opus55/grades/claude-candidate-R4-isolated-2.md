Grader: `/root/grade55_claude_c_r4_i2`; fresh eval-grader role, workflow mode.
Manifest: `5158fbf481cd1b9f7f6f7b89c4b2f116d13f1eb4f89d14b34831184dd73f2a73`.

| id | verdict | evidence |
|----|---------|----------|
| 9.1 | PASS | Main instruction/profile results e19/e21, e28–e40, e55/e61/e63 precede investigation e83; child methodology results e150–e171 precede evidence read e174. Early scope operations e43/e50 inspect metadata only. |
| 9.2 | PASS | Successful reads e96/e98/e100/e102 inspect unchanged callers, migration, writer and snapshot; e217 identifies `reader.py:2`'s nested-field assumption as incompatible with legacy rows. |
| 9.3 | PASS | e243 reports `KeyError` on `legacy-a` initially and `legacy-c` after `migrate_batch(records, 1)`, failing the whole list; fully migrated records return three addresses. e228 reproduces the initial failure. |
| 9.4 | PASS | e243 cites the README's dual-shape/background-batch contract, marks mixed and partial states **Blocked**, returns **REQUEST_CHANGES**, and confines conclusions to the local JSON model. |
| 9.5 | PASS | e243 recommends restoring the fallback, retaining it until verified migration completion and contract revision, and explains why the passing new-write tests miss the regression. |
| 9.6 | FAIL | e143 dispatches the named reviewer with the required evidence and e220 retains its result, but event-index.json contains no PAL dispatch; e142/e243 explicitly state only one reviewer ran and disclose the missing coverage. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions; no actor access to grading material was observed in the retained events.

Controller note: PAL is user-deferred. The unchanged paired-reviewer assertion
remains FAIL despite successful named-reviewer receipt and use.
