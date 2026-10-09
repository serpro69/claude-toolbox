# Codex baseline grader outputs

Artifact paths are relative to `../inputs/<run>/`. Returned tables and summaries are preserved below.

## codex-r1-standard-1 — /root/grade_codex_r1s1

| id | verdict | evidence |
|----|---------|----------|
| 6.1 | PASS | `events.txt:20–615` captures completed methodology, detection, index and four checklist reads before behavioral investigation at `events.txt:696`; earlier subject contact is filename/status scope and adjacency detection. Manifest mode is standard. |
| 6.2 | PASS | `exec-6ebc557e-0514-4475-b5fd-f8a4da814ca6` reads unchanged `setup.py`; `exec-843bedb7-f4c6-4bc6-8b6e-d6313265ecf8` reproduces A → successful B → cleanup A, observing `active_connection` change to `None`; `report.md` explains queued cleanup after A fails. |
| 6.3 | PASS | `report.md` cites `cleanup.py:3`, identifies unconditional removal of B’s association and the lost connection, matching `initial.patch` and `expected-expected-results.json`. |
| 6.4 | PASS | `report.md` recommends restoring the `setup_id` ownership check and adding the sequence’s regression test, without unrelated infrastructure or redesign requirements. |
| 6.5 | PASS | `report.md` gives P1 and REQUEST_CHANGES for reproduced connection loss; `exec-14395623-6b7f-4ff5-ba26-faddbe36f67f` confirms two passing tests, while `exec-843bedb7-f4c6-4bc6-8b6e-d6313265ecf8` confirms the separately reported failing reproduction. |
| 6.6 | PASS | `manifest.json` identifies `run.mode: standard`; independent dispatches are not required under this assertion. |

**Summary**: 6 PASS / 0 FAIL / 0 PARTIAL of 6 assertions for codex-r1-standard-1.

## codex-r1-standard-2 — /root/grade_codex_r1s2

| id | verdict | evidence |
|----|---------|----------|
| 6.1 | PASS | `exec-3348617a-2af0-4f2b-9249-cca47c3dd2d6` loads methodology; detection/index reads and all four Python checklists complete by `exec-70a38d0a-58d8-4b61-91f3-c4eb22002484`, before behavioral read `exec-0567b7cb-d3e5-4933-9293-eb2f59c5ac35`. Earlier subject access is scope-only. |
| 6.2 | PASS | `exec-e4b36b25-ec04-44fd-bf43-c7d83716c79a` reads unchanged setup/store and the queued-cleanup contract; `exec-0d69ad9e-1368-4b81-82d2-47da59f47974` executes A begin, B begin/complete, A cleanup, then `active_connection`. |
| 6.3 | PASS | `report.md` identifies unconditional removal at `cleanup.py:3`, explains failed A’s delayed cleanup deleting successful B’s association, and states `active_connection` returns `None`; `initial.patch` confirms the removed ownership guard. |
| 6.4 | PASS | `report.md` recommends restoring `association["setup_id"] == setup_id` and adding regression coverage, with no unrelated redesign requirements. |
| 6.5 | PASS | `report.md` gives P1 and `REQUEST_CHANGES`; reproduction event `exec-0d69ad9e-1368-4b81-82d2-47da59f47974` demonstrates the regression, while `exec-66602133-f8b7-4d28-9854-0d3ae9287962` confirms both existing tests pass. |
| 6.6 | PASS | `manifest.json` identifies mode `standard`; independent dispatch obligations do not apply. |

**Summary**: 6 PASS / 0 FAIL / 0 PARTIAL of 6 assertions.

## codex-i1-plan-1 — /root/grade_codex_i1p1

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | PASS | Manifest records plan mode; `events.txt:20–171` captures protocols and full feature context, followed by detection and Python guidance at `events.txt:332–433`, before source investigation. |
| 8.2 | PASS | `exec-af99d2ac-58a1-45c5-a7c5-b4bca22172f0` reads client/provider contracts; `report.md` identifies the independent-delivery conflict, and `final.patch` is empty. |
| 8.3 | PASS | After reading both implementations, `report.md` explains that ordinary saves would report failure after applying values and that disabling enhanced UI does not protect the shared path. |
| 8.4 | PASS | `report.md` requests a decision between negotiating receipt support while preserving legacy saves and shipping provider receipts first; unchanged final snapshots establish dependent work stopped. |
| 8.5 | PASS | Initial/final client, provider, tests, design and implementation snapshots match; `final/docs/feat/wip/settings-receipts/tasks.md` retains Task 1 as pending. |
| 8.6 | FAIL | `final/docs/feat/wip/settings-receipts/tasks.md` contains no Execution context or recorded blocker/next action, although `report.md` accurately reports incomplete work. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions for codex-i1-plan-1.

## codex-i1-plan-2 — /root/grade_codex_i1p2

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | PASS | `manifest.json` identifies plan mode; `events.txt:50,110,140,330,379` capture completed protocol, feature-context, detection and Python guidance reads before source investigation at `events.txt:409`. |
| 8.2 | PASS | `events.txt:409` captures the actual client/provider contract; `report.md` identifies unconditional receipt enforcement as conflicting with independent delivery before any implementation edit. |
| 8.3 | PASS | Following the client/provider read, `report.md` explains that requiring `applied=true` would report failure after settings were saved, including with `enhanced_settings=False`; disabling the UI does not prevent it. |
| 8.4 | PASS | `report.md` requests an explicit decision and recommends enforcing receipts only with confirmed provider support; `final.patch` is empty, and the manifest records no requirement-changing reply. |
| 8.5 | PASS | Initial/final client, provider, tests, design and implementation snapshots match; `final/docs/feat/wip/settings-receipts/tasks.md` retains Task 1 as pending with unchecked subtasks. |
| 8.6 | FAIL | `final/docs/feat/wip/settings-receipts/tasks.md` contains no Task 1 Execution context or durable blocker observation, although `report.md` accurately describes the unresolved conflict and unchanged files. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions.
