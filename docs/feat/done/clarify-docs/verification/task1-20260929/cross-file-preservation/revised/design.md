# Design: import preview

## Context

Import preview is planned to help operators catch CSV errors before applying an
import. It will report how many rows are valid and invalid while writing zero rows.
For example, a three-row CSV with one invalid row will report two valid rows and
one invalid row.

This increment covers preview only; apply remains future work. Product owns the
open duplicate-row policy decision, which must be resolved before implementing
apply. No implementation source was supplied; this document describes the planned
contract. See the [task state](tasks.md#task-1-preview) for recorded progress.

## Decision

Mira accepted preview-only delivery on 2026-09-01. CSV columns MUST remain `id,name`;
operators MAY download diagnostics. Diagnostics do not authorize applying rows.

## Deployment gate

Enable preview only after the support owner approves the sample-file walkthrough.

## Consequences

Apply remains disabled under this plan. Preview lets operators inspect row validity
without committing an import.
