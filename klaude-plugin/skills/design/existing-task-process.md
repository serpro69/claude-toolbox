### Workflow: Continue WIP Feature

**Entry prerequisite — instructions before subject matter.** Use filename-level discovery to locate the requested feature in `/docs/feat/wip/`; ask which feature only if the request leaves multiple candidates. Complete [SKILL.md's instruction-loading workflow](SKILL.md#workflow), including [shared-document-clarity.md](shared-document-clarity.md), before the content steps below. For its profile-detection phase, supply the feature-directory file list and any artifacts produced so far. If no file signal matches, use the shared design interaction pattern with a keyword-only scan of `design.md`; confirm inferred profiles. Load all resolved design guidance before reviewing progress or context. Do not repeat detection afterward.

1. **Review progress** — Read `tasks.md` to understand:
   - Which tasks are done, in-progress, or pending
   - What dependencies exist between remaining tasks
   - Any notes logged on previous subtasks

2. **Review context** — Read the linked `design.md` and `implementation.md` to understand the full picture. Also check any relevant contributing guidelines and documentation. **Capy search:** Search `kk:arch-decisions` and `kk:project-conventions` for context relevant to the feature being resumed. Audit the design against the already-loaded profile sections, including designs authored before the rubric existed.

3. **Assess readiness:**
   - **If tasks are well-documented and clear** → proceed to implement using the `/kk:implement` skill.
   - **If tasks need refinement** (missing details, unclear subtasks, gaps in the plan) → refine `tasks.md` and/or design/implementation docs using the drafting guidelines and task-format example loaded during entry. Use the existing decisions and loaded profile guidance; do not restart fresh-idea sub-phases.

4. **Clarify refined documents before handoff.** If refinement changed documents, apply the already-loaded shared clarity procedure once to those documents only, with their intended reader, accepted requirements and applicable evidence. This is the final pass summarized in SKILL.md. Reuse relevant context; preserve decisions, required sections, task state and cross-file links. Unchanged documents may supply context but are outside the edit scope; an unchanged resume performs no pass and no rewrite.

   Recommend `/kk:review-design <feature>` after refinement, then hand off to `/kk:implement` when ready. The recommendation is not automatic independent review. Do not invoke another writing skill for this pass.
