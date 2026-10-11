Grader: `/root/grade_entry_b_r9_1`; fresh eval-grader role, workflow mode.
Manifest: `5baef454d0c7e11cd950b01c7e87a63821da1fbc732455caba4e8db7890459f9`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | FAIL | Main reads the full diff at e66.0–e69.0 after only the Python index, without loading its four resolved checklists; the child completes checklist reads at e82.0–e91.0 before source reads. |
| 11.2 | PASS | e121.0 and e144.0 trace `Preferences.read → read_preferences → read_resilient(key.strip())`, explaining that every retry receives the trimmed key and preserves bounded recovery. |
| 11.3 | PASS | e121.0 assesses transient-then-success, three-failure exhaustion and immediate permanent failure, explicitly identifying source inspection; e136.0–e139.0 record the main actor’s four passing tests, attributed at e144.0. |
| 11.4 | PASS | e121.0 explicitly preserves `read_resilient` and its retry contract; neither reviewer nor final report recommends removing retries or retrying permanent errors. |
| 11.5 | PASS | e121.0 and e144.0 approve with optional P3 suggestions; the child names all five inspected paths and source-only limits, while the final report discloses absent PAL coverage. |
| 11.6 | FAIL | e76.0 dispatches the named reviewer with the diff and surrounding-source references but says “No spec context available,” omitting the explicit README contract; e75.0 and e144.0 confirm PAL never ran. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions; retained requests show no grading-material access, while OS confinement remains unverified.
