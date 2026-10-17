| id | verdict | evidence |
|----|---------|----------|
| 22.3 | PASS | trigger=present; report.md: detailed empty input “already divides by zero in both versions”; the rename does not increase reachability. |
| 22.4 | PASS | report.md distinguishes explicit detailed empty input from the False default and states historical installation settings are unknown. |
| 22.5 | PASS | report.md: “The label increment is approved”; separate repair “is not required for the label PR.” |
| 22.6 | PASS | trigger=present; report.md: “Separately specify empty detailed output and add a regression for it,” without blocking this PR. |
| 22.7 | PASS | report.md labels its conclusion source-based and says tests were not executed; events.json records no test execution. |

**Summary**: 5 PASS / 0 FAIL / 0 PARTIAL of 5 assertions in this synthetic calibration; discovery and final-advisory follow-up were both exercised.
