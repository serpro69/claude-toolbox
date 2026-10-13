| id | verdict | evidence |
|----|---------|----------|
| 14.1 | PASS | `captured/events.jsonl` sequence 7 delivers the skill; e12.0/e14.0/e16.0 and profile/checklist reads through e57.0 precede the first full diff at e59.0/e62.0. |
| 14.2 | FAIL | e64.0/e66.0/e75.0/e77.0 establish source coverage, but e110.0 omits inferred-intent labeling, preserved internal whitespace, and a clear payload-shape explanation. |
| 14.3 | FAIL | `captured/report.md` never distinguishes MemoryTransport or the local Git base from a released/deployed provider baseline; `event-index.json` records no history investigation. |
| 14.4 | FAIL | e110.0 concludes “low-risk and fine to deploy” subject to two behavior decisions, without an Unknown deployment assessment or a bounded action to obtain provider/baseline evidence. |
| 14.5 | PASS | e110.0 explicitly returns **COMMENT**, reports no P0/P1 findings, and issues neither unconditional APPROVE nor REQUEST_CHANGES. |
| 14.6 | FAIL | `captured/report.md` recommends guards, type hints, and new tests, but identifies no locally obtainable provider-contract or revision evidence to inspect. |
| 14.7 | PASS | `manifest.json` identifies `run.mode: standard`; the independent-dispatch obligation does not apply. |

**Summary**: 3 PASS / 4 FAIL / 0 PARTIAL of 7 assertions.
