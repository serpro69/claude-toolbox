I’ll use `kk:review-code` to review the staged cleanup, loading the applicable checklists before reading the diff.

The cleanup removes support for rows with a top-level `address`. I’m checking the migration, stored records, and callers to see whether that fallback is safe to delete.

The regression is confirmed: listing the supported snapshot raises `KeyError('destination')` before migration and after a partial batch. Both existing tests pass because they cover only new-format rows and empty lists. I’ll report one high-priority finding to retain the fallback until migration finishes.

**REQUEST_CHANGES** — reviewed 1 staged file, +1/−3 lines.

- **P1: Retain legacy reads until migration completes** — [reader.py:2](/tmp/fr-opus55-matrix-20261011/codex-baseline-R4-standard-1/reader.py:2). Removing the fallback makes `list_destinations()` raise `KeyError('destination')` for the supported mixed snapshot, failing the entire listing. Migration runs in bounded batches without a startup gate, so legacy rows remain valid during rollout. Restore the fallback and cover mixed records before and after partial migration.
  
  Profile: `python` · Checklist: `removal-plan.md` · Trigger: `.py` extension. **Confidence: 100%** — reproduced both failures; the original reader handles both successfully.

Both existing tests pass but miss these cases. Finding indexed as `kk:review-findings`. No files changed.

Fix this finding, or leave it review-only?

The [review skill](/home/sergio/.codex/plugins/cache/fr-opus55-c2d28c9e-20261011/kk/0.23.0/skills/review-code/SKILL.md) requires “Next steps confirmation from user.”
