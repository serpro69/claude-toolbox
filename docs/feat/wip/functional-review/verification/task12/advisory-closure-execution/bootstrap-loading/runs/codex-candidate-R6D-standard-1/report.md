I’ll use `kk:review-code` to review the staged label change, trace the count it displays, and check for regressions.

The staged scope is two Python files, with five additions and five deletions. All six common instruction parts, the Python index, and both checklist parts are loaded: security, SOLID, code quality, and removal guidance under `profiles/python/review-code/`. Python matched; Go, Java, JS/TS, Kotlin, Kubernetes, operator, and skill profiles did not. I’ll now check the report contract and staged code.

The staged change follows the README contract: both plain and detailed reports use the shared count formatter, and the calculation and mode-selection code is unchanged. I also found an existing division-by-zero path for an empty detailed report. I’m comparing HEAD with the staged snapshot to confirm that behavior is inherited.

**APPROVE — no regressions found in the staged change.**

Reviewed HEAD `2b50e59` → staged index: two files, five additions and five deletions. The change meets the README requirement to rename “Items” to “Records” while preserving counts, calculations, mode selection, and the mean suffix.

Verification:

- All four tests pass on both revisions.
- Forty comparative scenarios cover both defaults, explicit overrides, empty batches, zero, negatives, and fractional means. Successful outputs differ only by the label.
- Compatibility is supported against HEAD; historical deployment settings were not assessed.

An inherited issue remains: empty detailed reports raise `ZeroDivisionError` in [stats.py:4](/tmp/fr-advisory-bootstrap-20261018/codex-candidate-R6D-standard-1/stats.py:4) on both revisions. Handle empty input before calculating the mean as a separate follow-up; it does not block this change.

No findings to index. No changes recommended for the staged increment.
