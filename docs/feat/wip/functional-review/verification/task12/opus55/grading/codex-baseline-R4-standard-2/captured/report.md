I’m using `kk:review-code` to review the staged cleanup. I’ll load the applicable checklists before reading the diff, then check the changes and affected call sites.



The cleanup removes support for legacy records that the README still requires. The saved snapshot contains both formats, and migration runs in batches without a startup gate. I’ll check whether the API fails before migration finishes and whether the existing tests catch it.



**REQUEST_CHANGES** — one P1 finding in the staged change.

- **P1: Preserve legacy reads until migration finishes** — [reader.py:2](/tmp/fr-opus55-matrix-20261011/codex-baseline-R4-standard-2/reader.py:2). Removing the fallback makes `list_destinations()` raise `KeyError: 'destination'` whenever a legacy record remains, failing the entire listing. The README requires reads during bounded migration. Using the supplied snapshot, I reproduced failures before migration and after migrating one record; the original reader handles both.
  
  Restore the fallback until migration completion is enforced. Add coverage for mixed records and partial migration.
  
  Profile: `python` · Checklist: `removal-plan.md` · Trigger: `.py` extension. Confidence: **100%**, confirmed by execution.

Both existing tests pass; they cover only new writes and empty lists. Indexed the systemic finding as `kk:review-findings`. No files changed.

Would you like me to fix this or leave it as review-only?

The [review skill](/home/sergio/.codex/plugins/cache/fr-opus55-c2d28c9e-20261011/kk/0.23.0/skills/review-code/SKILL.md) requires “Next steps confirmation from user,” which is why I’m asking before making changes.
