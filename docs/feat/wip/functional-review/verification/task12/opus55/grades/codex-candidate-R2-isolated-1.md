Grader: `/root/grade55_codex_c_r2_i1`; fresh eval-grader role, workflow mode.
Manifest: `8409ba73cb4a2068f0eba0dd7cd6980170fd2893947890461dcd642b85f4c29a`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | PASS | Main instruction reads in `events/0007.json`–`0013.json`, `0018.json`, and `0020.json` precede investigation in `0023.json`; child methodology reads in `0047.json`–`0057.json` precede source reads in `0059.json`. |
| 8.2 | PASS | `events/0075.json` traces `client.submit → service.save → Store.apply/receipt`; `0030.json` reproduces an edited retry returning success while blue remains active, attributed to `service.py:8`. |
| 8.3 | PASS | `events/0075.json` separately traces completed `op-1` followed by fresh `op-2`; workspace lookup retains blue, creates no `op-2` record, and returns `op-2` success. |
| 8.4 | PASS | `events/0045.json` recommends applying current values for incomplete operations, restoring operation-ID lookup, retaining audit records, and restoring completed-receipt replay; `0075.json` cites the corresponding README clauses. |
| 8.5 | PASS | `events/0045.json` returns REQUEST_CHANGES with supported P1 findings; `0075.json` explains the missing edited-retry and fresh-operation tests and confines claims to the serialized in-memory contract. |
| 8.6 | FAIL | `captured/command.json` records PAL disabled; `events/0045.json` confirms a “single-reviewer isolated review without dual-reviewer corroboration.” No PAL dispatch or result exists, and no waiver applies. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions.

Controller note: PAL remains explicitly user-deferred; the omitted component
is retained as FAIL.
