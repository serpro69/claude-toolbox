# Independent grader calibration outputs

Pinned instructions: `../inputs/grader.md` (SHA-256 in `../inputs/pin.json`). Each section is the returned output of a fresh default agent with `fork_turns=none`. Controller expected grades were withheld; all seven matched. The component assertions/output were supplied as files through the read-only tool adapter; no workflow manifest was supplied to either component run.

## /root/cal_early — early-edit

| id | verdict | evidence |
|----|---------|----------|
| C.1 | FAIL | Actor main edited app.txt at `edit-1` (sequence 1), before successfully reading rules.txt at `read-1` (sequence 2). |

**Summary**: 0 PASS / 1 FAIL / 0 PARTIAL of 1 assertions.

## /root/cal_missing — missing-events

| id | verdict | evidence |
|----|---------|----------|
| C.1 | PARTIAL | `edit-1` records a successful edit; `manifest.json` identifies missing read-event capture, so successful loading of `rules.txt` before the edit cannot be established. |

**Summary**: 0 PASS / 0 FAIL / 1 PARTIAL of 1 assertions.

## /root/cal_ordered — ordered

| id | verdict | evidence |
|----|---------|----------|
| C.1 | PASS | `events.jsonl`: actor `main` successfully reads `rules.txt` with returned instruction bytes in `read-1` (sequence 1), before its first implementation edit, `edit-1` (sequence 2). |

**Summary**: 1 PASS / 0 FAIL / 0 PARTIAL of 1 assertions.

## /root/cal_omission — complete-omission

| id | verdict | evidence |
|----|---------|----------|
| C.1 | FAIL | `events.jsonl` contains successful `edit-1` on `app.txt` and no completed read of `rules.txt`; `manifest.json` declares events complete. |

**Summary**: 0 PASS / 1 FAIL / 0 PARTIAL of 1 assertions.

## /root/cal_denied — requested-only

| id | verdict | evidence |
|----|---------|----------|
| C.1 | FAIL | `events.jsonl`: `read-1` was denied with no returned content; `edit-1` then successfully edited `app.txt`. The manifest declares the trace complete. |

**Summary**: 0 PASS / 1 FAIL / 0 PARTIAL of 1 assertion.

## /root/cal_component_default — omitted mode

| id | verdict | evidence |
|----|---------|----------|
| L.1 | PASS | “Active profiles: python — content signal: .py extension on app.py.” |
| L.2 | PARTIAL | “Loaded: security-checklist.md.” gives no load condition. |
| L.3 | FAIL | “No findings.” |

**Summary**: 1 PASS / 1 FAIL / 1 PARTIAL of 3 assertions.

## /root/cal_component_explicit — component mode

| id | verdict | evidence |
|----|---------|----------|
| L.1 | PASS | “Active profiles: python — content signal: .py extension on app.py.” |
| L.2 | PARTIAL | “Loaded: security-checklist.md.” names the checklist but gives no load condition. |
| L.3 | FAIL | “No findings.” |

**Summary**: 1 PASS / 1 FAIL / 1 PARTIAL of 3 assertions.

## Correction: component dispatch shape

The two earlier component runs returned expected grades, but supplied assertions by file path. The legacy contract expects assertions inline and authorizes only reviewer-output/grading-instruction reads. The controller repeated both controls with assertions and reviewer output inline, preserving the earlier attempts rather than presenting their input shape as legacy conformance. The five workflow runs and these two corrected component runs constitute the seven accepted controls.

## /root/cal_component_default_inline — omitted mode, inline inputs

| id | verdict | evidence |
|----|---------|----------|
| L.1 | PASS | “python — content signal: .py extension on app.py.” |
| L.2 | PARTIAL | “Loaded: security-checklist.md.” names the checklist but gives no load condition. |
| L.3 | FAIL | “No findings.” |

**Summary**: 1 PASS / 1 FAIL / 1 PARTIAL of 3 assertions.

## /root/cal_component_explicit_inline — component mode, inline inputs

| id | verdict | evidence |
|----|---------|----------|
| L.1 | PASS | “Active profiles: python — content signal: .py extension on app.py.” |
| L.2 | PARTIAL | “Loaded: security-checklist.md.” names the checklist but omits its load condition. |
| L.3 | FAIL | “No findings.” |

**Summary**: 1 PASS / 1 FAIL / 1 PARTIAL of 3 assertions.
