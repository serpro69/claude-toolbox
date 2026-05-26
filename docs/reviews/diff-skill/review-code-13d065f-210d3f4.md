# diff-skill: review-code (13d065f → 210d3f4)

## Summary

**Verdict: Complexity regressed.** No load-bearing instructions were dropped or weakened — the diff, profile checklists, spec context, and task scope all still reach pal, just via `relevant_files` instead of inlined in `step`. However, the edit introduced two complexity concerns: parallel definitions of the same 5-category file list in two files that must stay synchronized, and a judgment-heavy "surrounding code files" collection step without clear bounds or verification criteria.

## Complexity Regressions

### 1. Parallel file-list definitions across two files

**Where:** `review-isolated.md` Step 1g and `pal-codereview-invocation.md` §Assembling `relevant_files`.

**What:** The same 5-category file list (diff file, changed sources, surrounding code, profile checklists, design docs) is defined in both files with slightly different framing — the shared file documents the protocol interface (what pal expects), the skill file documents the caller implementation (how to collect). Both enumerate the same categories in the same order with overlapping descriptions.

**Why it matters:** Changes to the categorization must be synchronized across both files. If a future edit updates one without the other, the caller and protocol will drift. This is the classic "same list in two places" maintenance hazard. Consider whether the shared file's `relevant_files` section could be authoritative, with the skill file referencing it rather than restating it.

**Status: Acknowledged, won't fix.** The duplication is structural — interface vs implementation. The shared doc defines the protocol contract (what categories pal expects); Step 1g defines the caller implementation (how to collect each category, with specific tool instructions and cross-references to earlier substeps). Deduplicating by making the shared doc authoritative would force the LLM to jump to a second file mid-step to learn the categories, then return for collection instructions, then cross-reference substeps 1a/1b/1c — three locations to assemble a single list. The current inline definition keeps Step 1g self-contained for sequential execution. The drift risk is low: the categories are stable (they map to fundamental code review artifact types), and updating both places on change is trivial.

### 2. Judgment-heavy "surrounding code files" collection

**Where:** `review-isolated.md` Step 1g, category #3.

**What:** The instruction asks the LLM to "identify direct imports, callers, interfaces, and type definitions referenced in the diff" and "Use `grep`/`rg` to locate these. Include files that a reviewer would need to verify cross-file correctness." The bounding guidance is "aim for the immediate dependency ring, not transitive closure."

**Why it matters:** "Immediate dependency ring" is subjective — different executions on the same diff could produce very different file sets depending on how aggressively the LLM follows import chains. There is no cap on file count, no verification step to confirm the set is reasonable, and no fallback if the search produces too many or too few files. For a step that feeds directly into `relevant_files` (which has token budget implications in pal), unbounded output is a practical risk.

**Status: Addressed.** Step 1g category #3 now has a 10-file cap, a prioritized collection order (imports > callers > adjacency), and a fallback (drop adjacency if over cap). The shared protocol mirrors the cap.

## Pre-existing Complexity

### 1. Step 1 substep density

**Where:** `review-isolated.md` Step 1, substeps 1a–1g.

**What:** Step 1 "Prepare Artifacts" now has 7 substeps that produce artifacts with cross-references between them (e.g., 1g references the temp file from 1a, the profile list from 1c, and the spec context from 1b). While the edit added only one substep (1g), the structural complexity of managing 7 artifact-gathering substeps with forward and backward dependencies existed at 6 substeps already.

**Why it matters:** High substep count in a single phase increases the chance of an LLM skipping or conflating steps. Each artifact-passing dependency (1g depends on 1a, 1b, 1c) is implicit rather than enforced. This is a candidate for restructuring — e.g., grouping the "collect for pal" concerns (1a temp file write, 1g file list) into a single focused substep.

## Neutral Changes

- **Step 1a: Diff temp file.** Added `git diff > /tmp/kk-review-diff-$(git rev-parse --short HEAD).patch`. This is a new instruction (not a relocation) that serves the new `relevant_files` delivery mechanism. It's well-specified and bounded.
- **Step 2 Reviewer B: `step` parameter reworked.** The before-state said to include the git diff in `step`; the after-state says not to and instead passes content via `relevant_files`. The substance (pal gets the diff) is preserved via a different mechanism. The new `step` structure (framing + scope + spec summary + file manifest) is more prescriptive, not less.
- **`pal-codereview-invocation.md`: `step` content section.** New section with a clear example of the file manifest format. Adds specification but is well-structured.
- **Checklist and Contents update.** "(1a–1g)" and the 1g entry in Contents correctly reflect the new substep.
- **Second link to `shared-pal-codereview-invocation.md`.** Added in the Step 2 `step` parameter description. Resolves correctly; provides navigability to the format spec.
