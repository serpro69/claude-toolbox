## pal codereview invocation

`pal codereview` is a **multi-turn** tool. The initial call prepares review; complete the external continuation before treating it as an expert result. Select the caller branch below before constructing the payload. Common transport, native-output and failure rules apply to both branches.

### Code-review branch

For /kk:review-code, pass the same material scope, change-context facts, criteria and source evidence as the independent code-reviewer. Functional reasoning still applies without specifications; label inferred purpose and unresolved evidence. Do not import implementation-session history or the other reviewer's conclusions.

#### Assembling `relevant_files`

All paths are absolute and readable. Categorize them by role:

1. **Diff:** temporary file containing the selected diff.
2. **Candidate source:** changed files at the selected worktree/index/revision, accounting for deletions. When current files differ, use materialized candidate snapshots with original-path/revision provenance.
3. **Affected behavior:** relevant entry points, dependencies, unchanged consumers, state/data contracts and delivery configuration. Ten surrounding files is an initial selection budget, not a correctness boundary. Follow identified contract questions through focused additions/continuations or report the uncovered boundary; do not scan whole repositories.
4. **Historical source:** actual local Git blobs or bounded excerpts required for compatibility, plus their provenance manifest (repository, full revision, original path, blob/content hash, line span, omitted/redacted extent). Prepare read-only bundles outside the reviewed worktree. A parent summary cannot replace source absent from candidate files/diff hunks.
5. **Review criteria:** the common functional method, shared change-context and scope/knowledge protocols, plus resolved profile checklists. Resolve paths from the caller's known installation root; identify these as instructions to apply, not source to review.
6. **Intent/context:** relevant design/implementation/task documents and the factual change-context record if file-based. Inline the same Task Scope block and factual context into `step` when not supplied as files; keep baselines and attributed test results explicit.

For code review, submit only the selected **diff file** in the initial planning call's `relevant_files`. Supply the complete categorized bundle, including historical source and criteria, in the external continuation. This keeps the planning request small and makes newly embedded source coverage observable at the expert step; files carried through conversation history can otherwise be deduplicated from its new-file count. Do not omit the continuation's source bundle or treat a zero count as proof of either receipt or absence without other evidence.

Retain the same relevant source additions for both reviewers. For a missing-evidence request, the parent obtains available local source, then uses continuation with the new files and provenance. Name the comparison still needed; unavailable evidence stays Unknown with a next action. Do not expand access permissions automatically.

### Document-review branch

For /kk:review-design, document inputs remain sufficient. No Git diff, code-review change context, historical bundle or code profile is required.

- **Documents:** every in-scope design, implementation or task document; these are the review targets.
- **Related source:** existing files the design references, where available, for technical context.

Frame the review around technical soundness, completeness, consistency, edge cases, failure modes, constraints and ambiguity. Preserve the caller's document scope; do not treat planned code as a missing current implementation. Use its own review criteria. The common call sequence below remains identical.

### Step 1 — initial call

| Parameter | Value |
|---|---|
| `model` | Most capable available model from `pal listmodels` |
| `step` | Framing, applicable scope/context summary and categorized file manifest below |
| `step_number` | `1` |
| `total_steps` | `2` |
| `next_step_required` | `true` |
| `review_validation_type` | `"external"` |
| `thinking_mode` | `"max"` |
| `review_type` | `"full"` |
| `findings` | `"Initial submission for review. No findings yet."` |
| `relevant_files` | Code review: selected diff file only. Document review: in-scope documents and related source as supplied by the caller |
| `confidence` | `"exploring"` |

#### `step` content

Keep framing lean; file contents belong in `relevant_files`, not pasted into `step`:

1. Review purpose and applicable criteria. For code, include intended behavior, preserved contracts and applicable compatibility as well as security/architecture/quality.
2. Scope and factual context: code's Task Scope/change context/spec summary, or document review's selected documents and purpose.
3. Categorized absolute-path manifest so the model distinguishes criteria, candidate targets, historical evidence and intent. For code review, identify the initial diff and the full bundle to be attached at continuation; do not label later files as already submitted. The expert continuation's manifest, for example:

   ```
   Files provided via relevant_files:
   - Diff: /tmp/kk-review-code-a1b2c3.patch
   - Candidate source: /project/src/client.py
   - Affected behavior: /project/src/settings.py
   - Historical source: /tmp/kk-evidence-a1b2c3/provider.py
   - Historical provenance: /tmp/kk-evidence-a1b2c3/manifest.json
   - Review criteria: /plugin/skills/review-code/functional-review.md, ...
   - Intent/context: /project/docs/feat/wip/settings/design.md, ...
   ```

Document callers use **Documents** and **Related source** instead. Paths sent are not proof of source receipt: retain actual embedding/read evidence returned by the tool and distinguish it from requested coverage.

### Step 2 — continuation call

Use the initial response's `continuation_id`. Reattach the relevant source/criteria paths so the expert stage has the required inputs; record only genuinely inspected files in `files_checked` if that field is used, distinguishing the caller's checks from external receipt.

| Parameter | Value |
|---|---|
| `model` | Same model as step 1 |
| `continuation_id` | From step 1 response |
| `step` | Produce expert findings using the selected branch, supplied criteria and evidence; identify inspected coverage and unresolved comparisons |
| `step_number` | `2` |
| `total_steps` | `2` |
| `next_step_required` | `false` |
| `review_validation_type` | `"external"` |
| `relevant_files` | Required branch-specific files, including any new evidence/provenance |
| `findings` | Copy/summarize step 1's returned findings, with attribution; do not insert the independent reviewer's conclusions |
| `confidence` | Match actual evidence; do not assert high confidence merely because this is the final step |

For focused later evidence/clarification, continue the same review using its returned continuation identifier, the new files and the outstanding comparison. Preserve request provenance and provisional findings. If continuation is unavailable, disclose it and re-invoke with the original scope/context and the requesting reviewer's own provisional results plus additions; do not silently claim an uninterrupted review.

### Parallel execution with sub-agents

Launch step 1 alongside the independent reviewer when supported, then complete PAL's continuation. Supply equivalent relevant evidence additions to both without sharing their conclusions.

### Failure modes and coverage

- No available model or tool/call failure: disclose it and retain the other reviewer's useful findings.
- Initial call succeeds but continuation fails: retain any useful returned findings as provisional and label the incomplete external review.
- Zero findings with demonstrated relevant source coverage may be a clean review; zero findings alone prove neither success nor failure.
- Zero embedded/read source, unverified receipt or materially incomplete coverage: disclose that limit. Do not claim independent corroboration or broad code/release approval from the underfed response. Retain useful source-backed findings from the available reviewer and qualify unresolved conclusions.

PAL output remains in **native format**, with attribution. Do not remap its severity or finding types. Agreement does not substitute for source evidence. Keep temporary artifacts through evidence requests and required retention, then clean up only files created for this review.
