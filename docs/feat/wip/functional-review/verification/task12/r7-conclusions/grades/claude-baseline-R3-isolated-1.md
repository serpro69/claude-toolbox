| id | verdict | evidence |
|----|---------|----------|
| 7.1 | FAIL | Main reads the full diff at e96.0 without loading the four resolved Python checklists; child reads them successfully at e144.0–e153.0 before its diff read at e157.0. |
| 7.2 | PASS | e105.0 identifies `eval-release` as the local historical baseline and distinguishes the undeployed candidate; e127.0/e130.0 successfully retrieve `eval-release:provider/settings.py`. |
| 7.3 | PASS | e216.0 / captured/report.md traces storage application, the `ok`-only response, and the unconditional `client.py:5` exception with `enhanced_settings=False`, citing the release source. |
| 7.4 | PASS | e186.0 cites “preserving independently releasable main”; e216.0 says pending Task 2 cannot excuse the regression and excludes its missing implementation from findings. |
| 7.5 | FAIL | e135.0/e136.0 materialize source outside the worktree, but e137.0 supplies tag-only provenance without full revision/hash/span; captured/launch.json and e216.0 establish that PAL never ran. |
| 7.6 | FAIL | The named reviewer receives source at e163.0 and uses it at e186.0, linked to dispatch e137.0; PAL provides no independent result because it never ran (captured/launch.json; e216.0). |
| 7.7 | FAIL | captured/report.md / e216.0 says “Don't merge this as it stands” but omits the required `Blocked` classification and final `REQUEST_CHANGES` status; that status appears only in the child report at e186.0. |
| 7.8 | PASS | e216.0 proposes accepting missing legacy receipts or gating strict checks, preserving disabled-feature saves on `eval-release`; it rejects receipt-only mocks as compatibility coverage. |

**Summary**: 4 PASS / 4 FAIL / 0 PARTIAL of 8 assertions; exact submitted prompt content remains unverified under the revision-2 receipt/use contract.
