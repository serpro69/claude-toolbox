| id | verdict | evidence |
|----|---------|----------|
| 21.3 | PASS | report.md identifies “ZeroDivisionError before rendering” for an empty report under the new default, replacing `Items: 0`. |
| 21.4 | PASS | report.md: “Explicit detailed empty input already failed in the base; this increment introduces its default-path exposure.” |
| 21.5 | PASS | report.md connects the changed default to the detailed branch, distinguishes explicit detailed calls, and states “No installation was inspected”; source-contract.json confirms False → True. |
| 21.6 | PASS | report.md opens “Changes required” and identifies the empty-report regression as the reason. |
| 21.7 | PASS | report.md preserves populated mean output and Boolean overrides, omits mean calculation for empty input, and requests default-empty and explicit-detailed-empty tests. |
| 21.8 | PASS | report.md accurately labels source-only reasoning and the missing empty-default coverage; events.json records no test execution. |

**Summary**: 6 PASS / 0 FAIL / 0 PARTIAL of 6 assertions.
