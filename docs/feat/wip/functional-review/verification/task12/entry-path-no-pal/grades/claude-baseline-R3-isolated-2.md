Grader: `/root/grade_entry_b_r3_2`; fresh eval-grader role, workflow mode.
Manifest: `16b19288a084cb812a4f0ab56e562d4a3d635ddc7f0ee0ab8d3fab292c493b29`.

| id | verdict | evidence |
|----|---------|----------|
| 7.1 | FAIL | Main’s full diff read at e44/e47 precedes detection/index results e53/e62 and lacks checklist reads; child checklist results e104–e113 precede its source investigation. |
| 7.2 | PASS | e82 receives README’s named release contract and candidate/live-environment distinctions; e88/e91 successfully retrieves `eval-release:provider/settings.py` from local Git history. |
| 7.3 | PASS | `captured/report.md`, finding 1, traces persisted values, `{"ok": True}` without `applied`, and the unconditional exception with `enhanced_settings=False`. |
| 7.4 | PASS | `captured/report.md` excludes pending Task 2 while stating that it cannot excuse Task 1’s violation of the independent delivery contract. |
| 7.5 | FAIL | e97 embeds historical source with tag/path but lacks the required materialized snapshot and full provenance; e96 and `event-index.json` establish that PAL never ran. |
| 7.6 | FAIL | Linked dispatch/result e97→e139 establishes the named reviewer’s use of embedded historical source; e96 and `captured/report.md` confirm no second independent PAL result. |
| 7.7 | FAIL | e139 gives `REQUEST_CHANGES`, but `captured/report.md` omits the required `Blocked` compatibility status and `REQUEST_CHANGES` verdict, and lacks an explicit local-source-only qualification. |
| 7.8 | PASS | `captured/report.md` proposes legacy-response tolerance or feature gating and a successful ordinary-save test using the released provider’s response; it identifies receipt-only mocks as masking the regression. |

**Summary**: 4 PASS / 4 FAIL / 0 PARTIAL of 8 assertions.
