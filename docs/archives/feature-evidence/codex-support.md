# Codex support retention

Archive the entire `docs/feat/done/codex-support/` directory. Its only capture
area is `.sessions/design-session.txt` (168,481 bytes).
Keep `design.md`, `implementation.md` and `tasks.md` in Git. Maintained Go
generation code/tests, Codex configuration/hooks/agents and generation manifest
remain in their current repository locations; none resides only in this capture.

Preserve the historical status discrepancy rather than rewriting frozen history:
the task-file header says pending and Task 11 says in-progress, while all five
Task 11 verification checkboxes are checked. Earlier entries report passing
structure/shell checks and a completed session smoke test. Directory placement
under `done/` is not new proof of completion, and this archive operation does
not revalidate or resolve those historical status labels.

No runtime helper, fixtures or unique result table requires extraction from the
session transcript. Plans and task records already contain the durable decisions.
The transcript remains a snapshot of the original discussion, not an active
instruction source.

Locator:
`payload/docs/feat/done/codex-support/.sessions/design-session.txt`.
Only the session directory is an eventual capture-cleanup candidate; keep the
three root records and current maintained implementation.
