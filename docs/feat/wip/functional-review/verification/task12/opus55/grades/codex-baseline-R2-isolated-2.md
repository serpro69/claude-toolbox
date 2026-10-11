Grader: `/root/grade55_codex_b_r2_i2`; fresh eval-grader role, workflow mode.
Manifest: `11e1e68704b33d9bb59c7a4976a8f82b290902ecb53c2ee7e2282f81b13a2396`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | FAIL | `events/0004.json` references `shared-pal-codereview-invocation.md`, but the complete retained read trace never loads it before behavioral reads in `events/0023.json`–`0025.json`; child checklist reads correctly precede its source reads. |
| 8.2 | PASS | `events/0036.json` reproduces receipt failure followed by an edited `client.submit` retry returning success with blue still active; `events/0054.json` explains the introduced `service.py:8` path. |
| 8.3 | PASS | `events/0036.json` shows fresh `op-2` success with blue unchanged and only `op-1` in recovery; `events/0054.json` identifies the completed workspace record suppressing application. |
| 8.4 | PASS | `events/0054.json` cites both README guarantees and proposes operation-ID lookup, refreshing and reapplying incomplete-operation values, and immediate receipt return for completed IDs. |
| 8.5 | PASS | `events/0041.json` returns REQUEST_CHANGES with supported P1 severity; `events/0054.json` explains the missing test scenarios and explicitly excludes concurrency, restart and external-effect guarantees. |
| 8.6 | FAIL | `captured/command.json` records PAL as disabled; `captured/protocol.jsonl` retains no PAL invocation or result through completion at sequence 1662. The report discloses unavailability, but no waiver applies; exact named-reviewer handoff plaintext remains unverified. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions; no grader-material access was observed.

Controller note: PAL remains user-deferred; the missing instruction read is
retained separately from omitted live verification.
