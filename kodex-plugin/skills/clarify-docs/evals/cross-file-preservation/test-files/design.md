# Design: import preview
## Context
A staged row count is the admission observation over the candidate CSV without any
commit to durable rows, for operators to catch mistakes before applying an import.
For a three-row CSV with one invalid row the preview reports two valid and one
invalid, writing zero rows. This increment is preview only. Apply remains future
work. Product must decide duplicate-row policy.
## Decision
Mira accepted preview-only delivery on 2026-09-01. CSV columns MUST remain id,name;
operators MAY download diagnostics. Diagnostics do not authorize applying rows.
## Deployment gate
Enable preview only after the support owner approves the sample-file walkthrough.
## Consequences
Apply remains disabled. See [task state](tasks.md#task-1-preview).
