# Design: import preview
## Context
This increment will let operators preview a CSV to catch mistakes before applying
an import. Preview will report valid and invalid row counts and write zero rows.
For example, a three-row CSV with one invalid row will report two valid rows and
one invalid row.

The scope is preview only; applying an import remains future work. Product owns
the open duplicate-row policy decision, which must be resolved before implementing
apply.
## Decision
Mira accepted preview-only delivery on 2026-09-01. CSV columns MUST remain id,name;
operators MAY download diagnostics. Diagnostics do not authorize applying rows.
## Deployment gate
Enable preview only after the support owner approves the sample-file walkthrough.
## Consequences
Apply must remain disabled in this increment. Resume with
[Task 1: Preview](tasks.md#task-1-preview); column parsing is marked complete, while
valid and invalid row counting remains pending.
