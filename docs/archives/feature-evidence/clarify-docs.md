# Clarify-docs retention

Archive `docs/feat/done/clarify-docs/` in full, together with
`docs/feat/reviews/clarify-docs-consolidation/`. The latter contains related
instruction snapshots, protocols, graded attempts and filtered traces outside
the feature directory; omitting it would split the historical record.

Keep the feature's root plans/tasks, `verification.md` and `reviews/` in Git.
Keep the consolidation's `results.md` and `protocol.md`, plus current canonical
evals/oracles and generated copies. These existing records already summarize
outcomes and criteria; no duplicate full report is needed.

The feature's final Task 5 record preserves **87/87 applicable assertions and
70/70 revised-reader answers across 20 scenarios**. It reused applicable Task 4
results without rerunning editors/readers. Task 4 began at
`9a7ad32eef89a3b8c9b366292ac1f4776c7d005f`; Task 5 at `a7e2eaa`, dated
2026-09-30. Earlier PARTIAL/FAIL and invalid attempts remain unchanged.
Final shell/Go/generation/graph checks and independent reviews passed according
to those original records.

The consolidation is a separate adaptive comparison, not another feature-wide
PASS: initial long-guide trials were 6 PASS / 1 PARTIAL for both released and
candidate instructions; the final fresh long-guide trial passed 7/7 after
recording-precision changes. Earlier regression applicability is qualified in
its `results.md`. It does not demonstrate a general artifact-quality advantage
or human-comprehension improvement.

Preserve the recorded limits: AI readers, audited manifests on shared storage,
encrypted dispatch/export qualifications and limited external-review source
coverage. No OS isolation, live-service certification or general reliability is
inferred from these captures.

Historical follow-up remains visible: the Task 4 build-directory substring
matcher blocked `agent-instruction-target/`. The original record assigns the
repository maintainer to inspect component matching and add a benign-suffix
regression. Current resolution is not reassessed by archiving; keep that owner,
reason and next action in `verification.md` and this note. Optional broader
production-document validation remains outside the synthetic trials' claims.

All Python files in the verification tree are fixture/source snapshots; there
is no reusable standalone runner to extract. Archive failed retries and all
snapshot/protocol material, including the separate consolidation evidence.
Locators are `payload/docs/feat/done/clarify-docs/verification/` and
`payload/docs/feat/reviews/clarify-docs-consolidation/`.

## Open archived evidence

[Download the clarify-docs archive](https://github.com/serpro69/claude-toolbox/releases/download/v0.24.0/clarify-docs-evidence-20261020T172123Z-3339e897.tar.gz).
The canonical link targets v0.24.0 after promotion; authenticated draft asset
API URLs/IDs are in [release-assets.json](release-assets.json).

Retained evidence links point here and carry an `Archive member: payload/...`
title. Hover the link or read its Markdown source for the exact member path,
then open that path in the extracted archive. A trailing `#...` identifies the
original Markdown section. The member paths remain those of the original
snapshot, even after feature documents or Git revisions move.
