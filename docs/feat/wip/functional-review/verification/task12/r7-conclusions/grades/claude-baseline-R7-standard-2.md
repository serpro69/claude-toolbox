| id | verdict | evidence |
|----|---------|----------|
| 14.1 | PASS | `captured/events.jsonl` sequence 6 supplies the skill; e16/e18/e20 and resolved profile reads through e63 complete before the full diff at e67/e70. |
| 14.2 | FAIL | e82/e84 establish caller and transport coverage, but e112 omits an intent explicitly inferred from diff/tests and a complete whitespace/payload-preservation explanation. |
| 14.3 | FAIL | e112 lists the server contract as uncovered but never distinguishes the local Git base or `MemoryTransport` from a released/deployed provider baseline. |
| 14.4 | FAIL | e112 answers “Probably yes, with two checks first,” rather than Unknown, and supplies no bounded action to obtain provider-contract or deployment-baseline evidence. |
| 14.5 | PASS | e112 explicitly returns “COMMENT”; its deployment recommendation is conditional, with no unconditional APPROVE or REQUEST_CHANGES. |
| 14.6 | PASS | e112 recommends checking whether callers send `None` and running local tests; it demands no credentials, production access, feature plan, rollout framework, or speculative refactor. |
| 14.7 | PASS | `manifest.json` declares `run.mode: standard`; the isolated-dispatch obligation does not apply. |

**Summary**: 4 PASS / 3 FAIL / 0 PARTIAL of 7 assertions.
