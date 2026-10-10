Review behavior, compatibility, SOLID, security and code quality in isolated mode with independent reviewers.

Two parallel reviewers: a `code-reviewer` sub-agent and `pal codereview` (external model). Produces a report organized by agreement level with corroborated findings highlighted.

Arguments: $ARGUMENTS

## Invocation

**If $ARGUMENTS is provided:**
Treat `$ARGUMENTS` as a commit range or file scope for the review.

**If $ARGUMENTS is empty:**
Review current unstaged changes (falling back to staged changes if no unstaged changes exist).

## Process

**Mandatory order — methodology before evidence.** Invoke `/kk:review-code` using its `review-isolated.md` workflow, strictly in sequence. Load all instructions before investigation. The only early content inspection resolves declared routing predicates within approximately 16 KiB per candidate file, logs predicate/path and conservatively loads undecidable conditionals; it permits no analysis or findings.

1. **Load basic instructions** — Process, shared protocols and common functional method.
2. **Resolve scope** — Filenames/metadata only; no diff or specification contents.
3. **Detect and route** — Every known profile's detection rules, active indexes and declared conditionals.
4. **Load checklists** — Every selected file; reconcile returned contents in the loading checkpoint before investigation.
5. **Investigate and prepare** — Read selected diff/source, establish context/task scope, trace behavior and materialize historical source with provenance for both reviewers.
6. **Review and obtain evidence** — Launch both reviewers when supported; complete PAL continuation and parent-mediated evidence requests.
7. **Annotate** — Preserve independent/native findings and author context; corroborate only with relevant evidence.
8. **Index** — Record systemic findings under the shared knowledge protocol.
9. **Report** — Findings, intent/scope/baselines, behavior/compatibility, coverage limits and qualified verdict; confirm next steps within existing authorization.
10. **Verify** — Check required outputs and clean up temporary evidence after follow-ups/retention.

## Examples

Review current changes:
```
/kk:review-code:isolated
```

Review a specific commit range:
```
/kk:review-code:isolated HEAD~3..HEAD
```
