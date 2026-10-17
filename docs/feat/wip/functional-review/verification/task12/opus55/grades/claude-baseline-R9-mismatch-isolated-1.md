Grader: `/root/grade55_claude_b_r9m_i1`; fresh eval-grader role, workflow mode.
Manifest: `842514980c162b58a93a61cf740cb72886ae10d6eec60071328b4f2f1f89a135`.

| id | verdict | evidence |
|----|---------|----------|
| 10.1 | FAIL | Main receives the full diff at e40.0 before Python detection/index reads at e65.0/e67.0 and never loads its resolved checklists; child checklist results e87.0–e96.0 precede its diff read e99.0. |
| 10.2 | PASS | e106.0/e109.0/e112.0 establish repository/backend, caller, and reader behavior; e122.0 supplies README authority, applied in e125.0. |
| 10.3 | PASS | captured/report.md findings 1–2 contrast `read_resilient` with `read_once`, cite reader.py:2 and README, and explain one failure replacing second-attempt success. |
| 10.4 | PASS | captured/report.md identifies the test's incorrect exception expectation and recommends `read_resilient(key.strip())`, successful retry, and `keys == ["w", "w"]`. |
| 10.5 | PASS | e125.0 returns REQUEST_CHANGES with P1 severity; captured/report.md distinguishes three-attempt exhaustion from first-attempt `MissingPreference` propagation without unrelated gates. |
| 10.6 | FAIL | e81.0 omits the explicit README contract; the complete trace contains no PAL dispatch/result, and captured/report.md confirms only the named reviewer ran. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions.

Controller note: PAL is user-deferred; omitted explicit contract context remains
a separate handoff limitation.
