Grader: `/root/grade55_codex_c_r2_s2`; fresh eval-grader role, workflow mode.
Manifest: `a5db9812891d7c73d614201bd513613a7f58c987970f6a222001e6bad6bbd498`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | PASS | Raw `captured/items-01a12b1c-9064-7a72-9df3-0edf974fa30c.json` contains complete successful instruction reads at `exec-a9f3f32a…`, `exec-f73e908f…`, `exec-b7071264…`, and `exec-4a9bda05…`, before the README investigation at `exec-91bfb205…`; earlier subject access is filenames/metadata only. |
| 8.2 | PASS | `events/0019.json` establishes `submit → save` and provider/receipt behavior; `events/0020.json` reproduces receipt failure after blue is applied, then successful green retry leaving blue active; report finding 2 cites `service.py:8`. |
| 8.3 | PASS | `events/0020.json` traces completed `op-1` followed by fresh `op-2`, returning `op-2` success while retaining blue and only the `op-1` record; report finding 1 attributes this to workspace lookup at `service.py:2`. |
| 8.4 | PASS | `captured/report.md` grounds findings in the README contract and recommends operation-ID lookup, applying latest values for unfinished operations, updating recovery values, and preserving the completed-operation shortcut. |
| 8.5 | FAIL | `captured/report.md` gives supported P1 severity, `REQUEST_CHANGES`, and bounded coverage, but only states “All three existing tests pass”; it does not explain that the supplied tests omit edited retries and fresh IDs on an already-used workspace. |
| 8.6 | PASS | `manifest.json` identifies `run.mode: standard`; the conditional independent-dispatch requirement does not apply. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions.
