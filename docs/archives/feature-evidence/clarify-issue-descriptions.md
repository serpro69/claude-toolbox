# Clarify issue descriptions retention

Archive `docs/feat/done/clarify-issue-descriptions/` in full. Keep its root design,
implementation, tasks and `verification.md` in Git. Maintained issue/local/PR
scenarios, fixtures, oracles, shared clarity guidance and generated counterparts
remain in their plugin locations.

Preserve [the aggregate verdict ledger](records/clarify-issue-aggregate-verdicts.json)
outside captures. It is an unchanged copy of
`verification/task4-20261002/aggregate-verdicts.json`, SHA-256
`4f6bd93b5c0c384ce857267d73c292c3cfd900ad7803fae2342e3a8c89ae29de`.
Its verdict-file references resolve from the original Task 4 directory in the
archive. This retains each skill/scenario's assertion IDs and final counts.

The original final result is **133 PASS / 0 FAIL / 0 PARTIAL across 29 scenarios**
(24 standalone and five consumer scenarios), with 30 applicable original/revised
readers. Cohorts are 40 document/routing assertions, 46 PR/consumer assertions,
and 47 issue assertions. The Task 4 start revision is
`9a501e1108b9083b83adbc6b550a18d0ff7b2b40`, dated 2026-10-02. Final source/spec
reviews and repository checks passed according to the original records.

Keep failed prompt-newline attempts, the interrupted grader, oracle v2 correction,
capture-recovery records, hashes and native Git exports. Final grades do not
reclassify those attempts. These are synthetic offline/model-reader observations,
not live tracker certification, OS confinement or general human-comprehension
evidence; encrypted transport remains opaque.

The sole standalone helper,
`verification/task1-20261001/issues/capture-evidence.py`, reads a hardcoded
`/Users/sergio/.codex/sessions/2026/10/01` directory and exports visible session
records. No consumer was found in inspected repository scripts/tests/workflows.
Preserve it as a historical controller in the archive. Promoting this dated
script to a maintained exporter is unnecessary for this task; other Python files
are fixture snapshots. The maintained generic tools are already under
`scripts/functional-review-evals/`.

Primary locator:
`payload/docs/feat/done/clarify-issue-descriptions/verification/task4-20261002/`.
The full `verification/` tree is a later cleanup candidate, after reference repair.

## Open archived evidence

[Download the clarify-issue-descriptions archive](https://github.com/serpro69/claude-toolbox/releases/download/v0.24.0/clarify-issue-descriptions-evidence-20261020T172123Z-3339e897.tar.gz).
The canonical link targets v0.24.0 after promotion; authenticated draft asset
API URLs/IDs are in [release-assets.json](release-assets.json).

Retained evidence links point here and carry an `Archive member: payload/...`
title. Hover the link or read its Markdown source for the exact member path,
then open that path in the extracted archive. A trailing `#...` identifies the
original Markdown section. The member paths remain those of the original
snapshot, even after feature documents or Git revisions move.
