# PR missing context — final instructions

Executed regression 14 on 2026-10-01. The independent fixture-capable grader
returned **3 PASS, 0 FAIL, 0 PARTIAL**; see [report](grading/report.md) and
[assertion verdicts](grading/verdicts.json).

The editor loaded both frozen instructions before reading the two fixtures, asked
for a destination and actual PR evidence, and left every file unchanged. Reader
comparison is not applicable. The run used the instruction hashes in
[revision metadata](../instruction-revision.json), including the 1,297-word final
shared procedure; no baseline run was required for this regression.

[Editor evidence](editor/) includes exact pre-dispatch prompt/settings/manifest,
before/after bytes and hashes, complete native tool/result/visible-message trace,
and coverage/read audit. [Dispatch records](dispatches-final.jsonl) and
[receipts](dispatch-receipts-final.json) link the saved plaintext to the editor.
[Grader evidence](grading/) retains its independent prompt, trace, report and
capacity-failure receipts. Fresh default agents used no overrides or inherited
conversation; native metadata records gpt-6-astra/xhigh.

The manifest explicitly authorized no writes, so this verifies behavior within
that permission boundary rather than autonomous permission inference. Native
prompt transport is encrypted; exact pre-dispatch plaintext, hashes, timestamps
and native receipts are retained. Traces audit declared reads on a shared
filesystem, not process-level isolation. This offline run does not certify a live
GitHub or Linear connector.
