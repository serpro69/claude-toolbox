# Design: import preview

## Context

This increment provides a CSV preview so operators can catch mistakes before
applying an import. The planned preview reports valid and invalid row counts
without writing any rows. For example, a three-row CSV with one invalid row will
report two valid rows and one invalid row, writing zero rows.

The scope is preview only; apply remains future work. These are planned behaviors:
no implementation source is supplied for verification.

## Decision

Mira accepted preview-only delivery on 2026-09-01. CSV columns MUST remain
`id,name`. Operators MAY download diagnostics. Diagnostics do not authorize
applying rows.

Product owns the open duplicate-row policy decision. Resolve it before
implementing apply, as tracked in [Task 2](tasks.md#task-2-apply).

## Deployment gate

Enable preview only after the support owner approves the sample-file walkthrough.

## Consequences

Apply remains disabled. Resume [Task 1: Preview](tasks.md#task-1-preview) by adding
the valid and invalid counts; column parsing is recorded as complete in the task
checklist. Support approval is still required before enabling preview.
