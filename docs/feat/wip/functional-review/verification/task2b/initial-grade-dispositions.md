# Preserved initial grades and evidence updates

**Superseded evidence interpretation:** the table below records the first
history-only update. Final audit found that the history marker also accepts
formatted read errors. Original packages and summaries remain preserved;
[successful-read confirmations](receipt-grade-confirmations.md) use new sealed
packages containing successful read, formatting and inclusion records. All
four graders reassessed that stronger evidence. Use [grades-v2.json](grades-v2.json)
for final grades and `grades-v2-history-only.json` for the prior summary.

The initial packages remain under `grading/`; receipt-augmented packages are new
immutable directories under `grading-with-receipts/`. Original captures/seals,
rubric and assertions were not rewritten to change a result.

| Run | Initial result | Updated result | Basis |
| --- | --- | --- | --- |
| Codex R3 isolated 1 | 4 PASS / 3 FAIL / 1 PARTIAL | 5 PASS / 3 FAIL / 0 PARTIAL | 7.6's missing PAL receipt is resolved by existing successful history-embedding records matched to the actual call and payload hash. |
| Codex I2 standalone 1 | 4 PASS / 2 FAIL / 1 PARTIAL | 5 PASS / 2 FAIL / 0 PARTIAL | 9.5 becomes FAIL because actual PAL arguments leak the other reviewer's judgment; 9.6 becomes PASS after receipts remove the initial zero-source inference. |
| Codex I2 standalone 2 | 5 PASS / 1 FAIL / 1 PARTIAL | 5 PASS / 2 FAIL / 0 PARTIAL | Clarification of 9.5: complete results omit the required observable use of attributed execution results. Unknown child-prompt receipt does not soften that independently observable failure. No evidence or rubric changed for this clarification. |

The initial R3 7.6 and I2 9.5 rows correctly withheld PASS when receipts were
missing. The grader then inspected additional existing-runtime evidence rather
than inferring receipt from a correct report. For I2 repetition 2, the follow-up
explicitly requested the FAIL/PARTIAL distinction without a desired outcome;
the grader identified complete-result omission under the unchanged conjunction.

Codex R3 repetition 2 was graded with receipts on the first pass: 6 PASS / 2 FAIL.
Exact submitted prompt content/parity and unknown child verification receipt stay
unverified. Task 12 cannot reuse an unknown positive component as a candidate PASS.
