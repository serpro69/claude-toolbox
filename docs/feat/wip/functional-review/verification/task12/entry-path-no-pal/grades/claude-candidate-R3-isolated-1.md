Grader: `/root/grade_entry_c_r3_1`; fresh eval-grader role, workflow mode.
Manifest: `4e269f8fa6a37f8aa9392b1345852732f2a91bc4fbfc17ba17a643250dbd3e8a`.

| id | verdict | evidence |
|----|---------|----------|
| 7.1 | PASS | Main instruction returns e15/e17/e27–e39 and checklist returns e77/e79 precede investigation e94; child common/checklist returns e180–e201 precede its first subject read e205. |
| 7.2 | PASS | README return e97 identifies the local release tag/path; e125 resolves distinct base/release revisions and provider blob; e130 returns historical source. |
| 7.3 | PASS | captured/report.md traces the disabled save through provider application, `{"ok": True}` without `applied`, and the unconditional exception at client.py:5; e130/e119 substantiate that chain. |
| 7.4 | PASS | captured/report.md says the increment cannot merge independently and explicitly excludes pending Task 2 as missing implementation; e250 identifies the incompatibility as introduced. |
| 7.5 | FAIL | e149–e157 materialize and verify historical source with provenance; reviewer invocation e173 receives it through e218/e230. PAL discovery fails at e162, and no external reviewer receives the evidence. |
| 7.6 | FAIL | The named reviewer uses independently received history in e250, linked to e173/e218/e230; captured/report.md explicitly records no external review, so both independent results are absent. |
| 7.7 | PASS | captured/report.md marks the required combination **Blocked** and **REQUEST_CHANGES**, while distinguishing inspected release source from any verified deployment. |
| 7.8 | PASS | captured/report.md proposes tolerating absent legacy receipts while rejecting explicit invalid receipts, identifies future-response mocks as insufficient, and requests no production access. |

**Summary**: 6 PASS / 2 FAIL / 0 PARTIAL of 8 assertions.

Controller clarification: the named reviewer result is present. Assertion 7.6's
two-reviewer requirement fails because the PAL result is absent; its local
receipt/use evidence remains separately visible in the grader's row.
