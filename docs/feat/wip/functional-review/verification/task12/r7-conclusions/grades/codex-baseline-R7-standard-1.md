| id | verdict | evidence |
|----|---------|----------|
| 14.1 | PASS | Successful instruction/profile reads in `events/0003.json`, `0005.json`, `0006.json`, and `0007.json` precede behavioral source reads in `0009.json`. |
| 14.2 | FAIL | `events/0009.json` and `0013.json` cover payload, caller, and transport behavior, but `captured/report.md` omits inferred-intent labeling and an explanation of the preserved payload shape and previous whitespace behavior. |
| 14.3 | FAIL | `events/0012.json` returns “Review base”; `captured/report.md` explains the in-memory transport limitation but never distinguishes that Git base from a released/deployed provider baseline. |
| 14.4 | FAIL | `captured/report.md` assesses deployment as “only partially verified,” without an Unknown conclusion or a bounded request for applicable provider contract/deployment-revision evidence. |
| 14.5 | FAIL | `events/0015.json` explicitly returns “APPROVE the staged code change,” rather than COMMENT or an equivalent non-approval verdict. |
| 14.6 | PASS | `captured/report.md` limits follow-up to checking `/settings` acceptance/persistence and whitespace-only behavior; it demands no credentials, production access, feature plan, rollout framework, or refactor. |
| 14.7 | PASS | `manifest.json` declares `run.mode: standard`; independent dispatch obligations do not apply. |

**Summary**: 3 PASS / 4 FAIL / 0 PARTIAL of 7 assertions.
