Grader: `/root/grade55_codex_c_r4_i1`; fresh eval-grader role, workflow mode.
Manifest: `9b811284017fc386fe48713321c679399a558fa8278d5e59057ee5aedbfc2933`.

| id | verdict | evidence |
|----|---------|----------|
| 9.1 | PASS | Parent instruction reads in events/0003.json–0019.json precede contract/source investigation in 0024.json–0025.json; 0013.json reads metadata only. Child completes eight instruction reads in 0043.json–0050.json before evidence reads beginning at 0052.json. |
| 9.2 | PASS | events/0025.json returns the fixture, API, writer, migration and changed reader. events/0079.json traces the unconditional nested lookup through the unchanged list consumer and identifies the legacy-row regression. |
| 9.3 | PASS | events/0079.json specifies `KeyError('destination')` at legacy-a initially and legacy-c after `migrate_batch(records, 1)`, aborting the listing; completed migration preserves all three addresses. events/0029.json corroborates both failures and the completed-state control. |
| 9.4 | PASS | events/0079.json ties **Blocked** and **REQUEST_CHANGES** to README’s mixed-data/background-batch contract and identifies the supplied snapshot as the compatibility baseline; production verification is explicitly inapplicable. |
| 9.5 | PASS | events/0079.json recommends restoring the conditional lookup and legacy fallback, defers removal until migration and contract permit it, and states that passing new-write tests or completing migration first cannot satisfy the current requirement. |
| 9.6 | FAIL | Manifest mode is `isolated`. events/0014.json and 0041.json explicitly disclose a single reviewer and unavailable PAL; the retained workflow contains no PAL dispatch/result. Exact named-reviewer handoff plaintext remains unverified. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions.

Controller note: PAL remains explicitly user-deferred; the omitted component
is retained as FAIL.
