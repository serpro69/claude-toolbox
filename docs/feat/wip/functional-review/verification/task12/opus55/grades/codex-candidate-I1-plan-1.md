Grader: `/root/grade55_codex_c_i1_p1`; fresh eval-grader role, workflow mode.
Manifest: `273bb5c64a8b6e586b7e5190dc63fd6d503936766314314354e921154b408abf`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | PARTIAL | `events/0002.json` and `0013–0015.json` establish protocol/profile loading before `0018.json`; the raw protocol retains no successful `implement/SKILL.md` read or captured entry-point load. |
| 8.2 | PASS | `events/0018.json` returns both contracts; `0022.json` identifies their conflict before the sole bookkeeping/context edit in `0031.json`. |
| 8.3 | PASS | `events/0022.json` explains failure after values are saved with `enhanced_settings=False`; `0030.json` confirms the provider returns only `ok` even when a receipt is requested. |
| 8.4 | PASS | `events/0023.json` requests an explicit choice between relaxing receipt rejection and relaxing independent delivery; subsequent events perform baseline verification and record context without dependent implementation. |
| 8.5 | PASS | Manifest initial/final hashes match for source, tests, design and implementation; `captured/final.patch` changes only Task 1 status to `in-progress` and adds Execution context, preserving unchecked acceptance items. |
| 8.6 | PASS | `events/0031.json` durably distinguishes “Observed,” “Unresolved” and “Proposed, not accepted,” with owner and next action; `0033.json` accurately reports unchanged code and incomplete Task 1. |

**Summary**: 5 PASS / 0 FAIL / 1 PARTIAL of 6 assertions.

Controller note: absent entry-point delivery evidence remains PARTIAL; it is
not treated as proof that the runtime failed to inject the skill.
