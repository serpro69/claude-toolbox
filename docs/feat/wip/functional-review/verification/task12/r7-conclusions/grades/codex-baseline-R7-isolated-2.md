| id | verdict | evidence |
|----|---------|----------|
| 14.1 | PASS | Parent instruction/profile reads in `events/0002.json`, `0005.json`, `0006.json`, `0008.json`, and `0009.json` completed before source investigation in `0011.json`; child checklist reads `0024.json`–`0027.json` completed before `0028.json`–`0033.json`. |
| 14.2 | FAIL | `events/0011.json` and `0016.json` cover the builder, caller, and transport boundary, but reports `0022.json` and `0039.json` omit an explicitly inferred normalization intent and before/after explanation. |
| 14.3 | FAIL | Reports acknowledge in-memory validation, but never distinguish the local Git review base from a released/deployed provider baseline; `captured/launch.json` records only the local review revision. |
| 14.4 | FAIL | `events/0022.json` says production integration is “unverified” and identifies contract uncertainty, but offers only “request further validation?” without a bounded evidence-gathering action. |
| 14.5 | FAIL | Child report `events/0039.json` returns **APPROVE**; parent report `0022.json` states “No actionable findings or code-review blockers to deployment” without an unambiguous non-approval verdict. |
| 14.6 | PASS | `events/0022.json` identifies the input/server contract, specifically non-string inputs and blank names, without demanding credentials, production access, a feature plan, rollout framework, or refactor. |
| 14.7 | FAIL | `events/0014.json` records the named reviewer; `captured/command.json` records PAL disabled, and `0022.json` confirms no second-reviewer corroboration. Required PAL dispatch and result are absent. |

**Summary**: 2 PASS / 5 FAIL / 0 PARTIAL of 7 assertions for codex-baseline-R7-isolated-2; exact submitted prompt content remains unverified.
