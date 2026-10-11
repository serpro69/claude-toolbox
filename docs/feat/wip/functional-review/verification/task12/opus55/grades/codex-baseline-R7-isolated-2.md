Grader: `/root/grade55_codex_b_r7_i2`; fresh eval-grader role, workflow mode.
Manifest: `8953ad8a6c4c0652ff574a875f8535b92d950cd4e5d505e2576ba1e257c11411`.

| id | verdict | evidence |
|----|---------|----------|
| 14.1 | FAIL | Child source read `events/0031.json` completes before SKILL loading finishes in `0034`; review-process loads later in `0040`. |
| 14.2 | FAIL | `0014`, `0017`, and `0044` cover payload, caller, and transport behavior, but the reports omit an explicit inferred-intent label and before/after whitespace explanation. |
| 14.3 | FAIL | `0020` distinguishes local transport checks from a live endpoint; `0024` and `0044` omit the distinction between the local Git base and a released/deployed baseline. |
| 14.4 | FAIL | `0024` says deployment remains “unverified,” but supplies neither specific missing provider-contract/revision evidence nor a bounded next action. |
| 14.5 | FAIL | `0024` returns “APPROVE at the code-review level”; `0044` also returns APPROVE, without a non-approval deployment verdict. |
| 14.6 | PASS | `0017` verifies the locally available `/settings` route and `display_name` payload contract; `0024` requests only further validation, without credentials or expanded implementation scope. |
| 14.7 | FAIL | `captured/command.json` records PAL disabled; `0024` confirms “only one independent reviewer participated,” so the required PAL dispatch and result are absent. |

**Summary**: 1 PASS / 6 FAIL / 0 PARTIAL of 7 assertions.

Controller note: PAL is user-deferred; the remaining failures are retained
without changing their evidence requirements.
