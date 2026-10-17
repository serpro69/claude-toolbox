| id | verdict | evidence |
|----|---------|----------|
| 22.3 | PASS | trigger=present; report.md: “Detailed empty input divides by zero in both versions; the label change neither causes nor activates it.” |
| 22.4 | PASS | report.md distinguishes configured False and successful empty plain reports from detailed-empty failure; “Historical settings were not assessed.” |
| 22.5 | PASS | report.md: “Approve the rename” and “No changes recommended,” without requiring dormant-path repair. |
| 22.6 | FAIL | trigger=present; the complete report.md surfaces the inherited defect but supplies no separate next action, closing with “No changes recommended.” |

**Summary**: 3 PASS / 1 FAIL / 0 PARTIAL of 4 assertions.
