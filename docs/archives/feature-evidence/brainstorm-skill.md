# Brainstorm skill retention

Source: `docs/feat/done/brainstorm-skill/`; archive the entire directory.
Keep its root `design.md`, `implementation.md`, `tasks.md` and `review-findings.md`
in Git. Maintained brainstorm/design scenarios, runbooks, shared ideation
references and generated counterparts remain under their current plugin paths.

The final Task 4 record reports **32 accepted scenario/variant pairs and 146
passing assertions**, with **all 60 attempts retained and 28 excluded**. Original
confirmation failures, invalid attempts and superseded runs are not passes.
Final source/spec reviews approved. The reported nine shell suites, generation
checks and plugin graph passed at that time; no tests or model scenarios are
rerun by this archive operation.

Preserve [the compact applicability audit](records/brainstorm-behavioral-evidence.json)
outside `verification/`. It is an unchanged copy of
`verification/task-4/checks/behavioral-evidence.json`, SHA-256
`629bbbf589240d09d935a0f9b7fd67e567d20ef11d8df74ff209cbb662606a83`.
Its run paths resolve from that original location inside the archive. The
individual `result.json` records retain assertions, model/session metadata,
instruction hashes, exact-input provenance and trace pointers.

The evidence distinguishes canonical/generated **instruction variants**, both
executed through Codex; it does not certify native Claude Code hosting or live
web/service research. Recorded applicability audits are not fresh executions.
Task 4 baseline is `7b2bbd0`, execution date 2026-10-03.

No reusable execution code exists in this evidence tree. Its final record
explicitly says one-time audit tooling stayed outside the repository. Keep the
maintained eval runbooks; do not require recovering temporary audit tooling.

Primary archive locator:
`payload/docs/feat/done/brainstorm-skill/verification/task-4/README.md`.
The complete `verification/` tree is an eventual cleanup candidate after archive
verification and reference repair. No removal occurs in this operation.

## Open archived evidence

[Download the brainstorm-skill archive](https://github.com/serpro69/claude-toolbox/releases/download/v0.24.0/brainstorm-skill-evidence-20261020T172123Z-3339e897.tar.gz).
The canonical link targets v0.24.0 after promotion; authenticated draft asset
API URLs/IDs are in [release-assets.json](release-assets.json).

Retained evidence links point here and carry an `Archive member: payload/...`
title. Hover the link or read its Markdown source for the exact member path,
then open that path in the extracted archive. A trailing `#...` identifies the
original Markdown section. The member paths remain those of the original
snapshot, even after feature documents or Git revisions move.
