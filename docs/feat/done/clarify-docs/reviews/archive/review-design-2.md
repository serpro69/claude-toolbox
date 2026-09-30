# Design Review: clarify-docs

> Historical review of the initial design. All findings are assessed in
> [the combined assessment](review-design-assessment.md); findings are unchanged; the relocated assessment link was repaired during Task 5.

Scope: design.md + implementation.md + tasks.md
Overall assessment: CONCERNS_FOUND
Documents:

- Design: docs/feat/wip/clarify-docs/design.md
- Implementation: docs/feat/wip/clarify-docs/implementation.md
- Tasks: docs/feat/wip/clarify-docs/tasks.md

Summary: 8 findings: 0 critical, 2 high, 4 medium, 2 low

---

## Findings

### P0 - Critical

(none)

### P1 - High

- [INCONSISTENT] The /kk:implement coverage claim only holds for plan mode
  - Section: design.md §Decisions and provenance, §Integration boundaries (implement row)
  - Confidence: 8/10. Verified against klaude-plugin/skills/implement/SKILL.md and both mode files.
  - Description: The design states as inspected fact that implement "already invokes /kk:document at completion" and therefore needs no pass. Only plan mode does. Standalone mode (bug fixes, GitHub issues) has an entry procedure and no completion step, and SKILL.md marks Step 5 "Complete" as plan-mode only.
  - Evidence: standalone-mode.md ends at "return to SKILL.md Step 2"; plan-mode.md §Completion is the only /kk:document call. Issue #156 asked for the pass in implement's final verification stage.
  - Recommendation: Correct the claim. Then decide explicitly: either standalone-mode doc edits are out of scope (add to Not Doing with rationale) or standalone needs a completion hook. Do not leave the gap implied.
- [AMBIGUOUS] "Authorized for that destination" and "team-visible" have no decision rule
  - Section: design.md §Truth, preservation and visibility; implementation.md §2 bullet 5
  - Confidence: 8/10
  - Description: The privacy rule is the centerpiece of Task 2 and its eval oracle, but the docs never define how the editor decides a reference is shareable. In this repo docs/feat/wip/*/tasks.md is committed and public, so "private task numbers" are team-visible here but not in a customer repo. Two implementers will diverge, and the privacy eval cannot be graded objectively.
  - Recommendation: Define the rule concretely, for example: a reference is team-visible iff it is tracked in the target repository at PR head or is a URL the repo's audience can open; everything else is private unless the caller authorizes it. Put the rule in the shared procedure and cite it in the eval oracle.

### P2 - Medium

- [TECH_RISK] Fidelity is self-verified by the drafting session
  - Section: design.md §Editorial workflow step 5; §Integration boundaries
  - Confidence: 7/10
  - Description: The plugin's own rationale (implement SKILL.md line 40) treats same-session self-review as unreliable and mandates isolated reviewers. Here the author edits and then grades its own fidelity. /kk:review-design is a downstream net for design docs, but /kk:document output and standalone /kk:clarify-docs output have no independent check.
  - Recommendation: Name the downstream gate per entry point in the Integration table. Record an isolated-verification variant as deferred work with rationale rather than leaving it unmentioned.
- [TECH_RISK] Always-loaded shared procedure has no size budget
  - Section: design.md §Integration boundaries ("All consumers load the shared procedure during instruction loading")
  - Confidence: 6/10
  - Description: /kk:design already loads SKILL.md, a process file, frameworks, refinement criteria, profile detection and profile content on every run. A prior review in kk:arch-decisions recorded that unconditional loads carry real per-run cost. The new file's size is unconstrained.
  - Recommendation: State a size target for document-clarity.md, or decide to load it just before the pass and explicitly reconcile that with the instructions-before-action rule.
- [INCOMPLETE] Eval evidence location unnamed; Task 4 undersized
  - Section: implementation.md §4 ("the feature's verification evidence"); tasks.md Task 4
  - Confidence: 7/10
  - Description: No path is named for recording model, staged inputs, outputs and verdicts. Task 4 is tagged S yet includes manually running roughly nine scenario classes with baseline plus revised fresh-reader grading, plus four skill invocations.
  - Recommendation: Name the file (for example docs/feat/wip/clarify-docs/verification.md). Either resize Task 4 or split eval execution into its own task.
- [AMBIGUOUS] Fresh-reader comprehension protocol is underspecified
  - Section: design.md §Verification and acceptance; implementation.md §4
  - Confidence: 6/10
  - Description: Who plays the fresh reader is unstated. The existing kk:eval-grader agent (Read-only, no fixture access) fits but is not mentioned. The pass criterion is unclear when the unedited baseline already answers all five questions.
  - Recommendation: Name the reader mechanism and define the outcome when baseline already passes (expected: no-op edit).

### P3 - Low

- [INCOMPLETE] "Maintained skill inventories" not named
  - Section: implementation.md §1; tasks.md Task 1 subtask 4
  - Confidence: 9/10
  - Evidence: README.md line 57 and docs/user-guide/skills.md line 3 both hardcode "13 workflow skills"; skills.md also has a pipeline list and reference table.
  - Recommendation: Name both files.
- [INCONSISTENT] Instruction-editing requests: "redirected" vs "surfaced"
  - Section: design.md §Integration boundaries vs implementation.md §4 scenario table
  - Confidence: 6/10
  - Description: Design says redirect to "its appropriate workflow" without naming one. No skill-editing workflow exists besides /kk:implement with the skill-md profile. Implementation says only "surfaced".
  - Recommendation: Pick one behavior and name the target workflow.

---

## Clean Areas

- tasks.md format: Not Doing header, size tags (no L), parallel markers, dependency graph, vertical slices all present.
- Assumptions, Not Doing and Rejected Alternatives present and specific; no Not Doing item is a disguised blocker.
- All referenced files exist: design and document SKILL.md, idea-process.md, existing-task-process.md, user-guide/skills.md, EXPECTED_SKILLS, eval layout with oracle convention.
- Pass placement matches existing structure: idea-process Step 6 ends by recommending review; existing-task-process Step 5 is the refinement point.
- Codex generation needs no manifest change: include_all: true and shared: copy: true.
- Recursion guard and symlink convention follow AGENTS.md.

No capy index entries written. The P1 findings are feature-specific rather than systemic patterns.
