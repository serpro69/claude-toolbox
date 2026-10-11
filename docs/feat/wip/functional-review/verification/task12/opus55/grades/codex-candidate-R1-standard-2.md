Grader: `/root/grade55_codex_c_r1_s2`; fresh eval-grader role, workflow mode.
Manifest: `f2df530126644a1b3413197ff485bf315b705c02a37184ea16969cc678a4d6f9`.

| id | verdict | evidence |
|----|---------|----------|
| 6.1 | PASS | `captured/protocol.jsonl` sequences 72, 80, 98 and 112 retain complete common/profile instruction results before investigation at 193; earlier scope reads contain metadata only. |
| 6.2 | PASS | `events/0017.json` reads unchanged setup/store; `events/0019.json` executes failed A pending → successful B → cleanup A and observes `active_connection` returning `None`. |
| 6.3 | PASS | `events/0024.json` cites `cleanup.py:3` and explains that A’s queued cleanup deletes B’s association, losing B’s connection. |
| 6.4 | PASS | `events/0024.json`: “Restore the `setup_id` guard while retaining unconditional removal of A’s pending record”; proposes only a focused regression test. |
| 6.5 | PASS | `events/0024.json` gives P1/REQUEST_CHANGES; reproduction in `0019` and two passing tests in `0020` substantiate its distinction between existing coverage and the regression. |
| 6.6 | PASS | `manifest.json` declares standard mode, so independent dispatch obligations do not apply. |

**Summary**: 6 PASS / 0 FAIL / 0 PARTIAL of 6 assertions; no actor access to grading material was observed.
