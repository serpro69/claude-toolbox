Grader: `/root/grade55_codex_c_r2_s1`; fresh eval-grader role, workflow mode.
Manifest: `da112b19b74682aaa6be46be89ee307e822380ad478ec2720af2ae6a71ad9469`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | PASS | `events/0006–0007.json` return all bootstrap parts; `0010` and `0012` return the Python index and four checklists before the first behavioral read in `0015`. Earlier inspection uses filenames and metadata. |
| 8.2 | PASS | `events/0018–0020.json` trace `client.submit` through apply and receipt failure; the edited retry returns success with blue still active. `0025` finding 2 cites `service.py:8`. |
| 8.3 | PASS | `events/0020.json` separately reproduces “fresh operation after simple success”: op-2 succeeds while preferences remain blue and only op-1 exists. `0025` finding 1 identifies workspace lookup reusing completed op-1. |
| 8.4 | PASS | `events/0025.json` cites the README contract and recommends operation-ID lookup, applying and recording latest values for incomplete operations, retaining audit records, and preserving the completed-ID fast path. |
| 8.5 | PASS | `events/0025.json` returns `REQUEST_CHANGES` with supported P1 findings and distinguishes supported unchanged retries from failing edited-retry/fresh-ID checks despite three passing tests; its scope excludes concurrency, restart, and external services. |
| 8.6 | PASS | `manifest.json` declares `mode: standard`; independent reviewer and PAL dispatch obligations do not apply. |

**Summary**: 6 PASS / 0 FAIL / 0 PARTIAL of 6 assertions; no grading-material access was observed in the retained events.
