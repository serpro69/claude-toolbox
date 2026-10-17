| id | verdict | evidence |
|----|---------|----------|
| 7.1 | PASS | Main instruction reads finish in `events/0013.json` before investigation in `events/0018.json`; child reads `events/0038.json`–`events/0045.json` finish before evidence inspection in `events/0047.json`. |
| 7.2 | PASS | `events/0018.json` returns the README’s release contract; `events/0020.json` returns historical provider source; `events/0021.json` distinguishes full release revision, HEAD base and index candidate. |
| 7.3 | PASS | `captured/report.md` identifies the unconditional check at `client.py:5`, missing `applied`, and disabled-feature failure; `events/0025.json` confirms values are stored before the candidate raises. |
| 7.4 | PASS | `captured/report.md` identifies the independent-release violation and keeps pending Task 2 outside scope, without reporting its absence as another defect. |
| 7.5 | FAIL | `events/0021.json` materializes historical evidence; reviewer-linked `events/0047.json` and `events/0059.json` return provenance and source. However, `captured/launch.json` disables PAL and `event-index.json` records no PAL invocation or receipt; exact prompts remain unverified. |
| 7.6 | FAIL | The linked reviewer uses historical source in `events/0068.json`, following receipt in `events/0059.json`; the required PAL result is absent, consistent with PAL being disabled in `captured/launch.json`. |
| 7.7 | FAIL | Parent final report `events/0036.json` gives REQUEST_CHANGES and local-source limits but omits the required Blocked compatibility assessment; that explicit classification appears only in the child’s `events/0068.json`. |
| 7.8 | PASS | `captured/report.md` recommends preserving supported legacy success and testing both stored values and caller success; it identifies the future-response mock as masking the regression and requires no production access. |

**Summary**: 5 PASS / 3 FAIL / 0 PARTIAL of 8 assertions.
