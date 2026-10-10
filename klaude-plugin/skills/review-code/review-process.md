### Workflow

**Mandatory ordering — methodology before evidence.** Follow [SKILL.md](SKILL.md)'s standard workflow strictly in sequence. Load all applicable instructions before investigation or action. The bounded routing exception below selects instructions only; it permits no behavioral analysis, findings, full-diff investigation, edits or tests.

Copy and complete this checklist:

```
Code Review Progress:
- [ ] Step 1: Load basic instructions
- [ ] Step 2: Select the diff from filenames/metadata
- [ ] Step 3: Detect profiles and route all checklists
- [ ] Step 4: Read every resolved checklist
- [ ] Step 5: Investigate behavior and compatibility
- [ ] Step 6: Apply profile and general checklists
- [ ] Step 7: Self-check and confidence assessment
- [ ] Step 8: Index findings
- [ ] Step 9: Present findings, coverage and verdict
- [ ] Step 10: Close the review or handle required next steps
- [ ] Step 11: Verify outputs
```

### 1) Load basic instructions

Read this entire process and [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md), [shared-profile-detection.md](shared-profile-detection.md), [shared-review-scope-protocol.md](shared-review-scope-protocol.md), [shared-change-context.md](shared-change-context.md), and [functional-review.md](functional-review.md) before routing. [Packet preparation](packet-preparation.md) supplies these original contents and every Known-profile detection rule together; Read all parts completely, or use its direct-read fallback. Already loaded, unchanged instructions need not be read twice. The common context and functional method apply even without active profiles or specification documents.

### 2) Select the diff from filenames/metadata

Use `git status -sb` and diff statistics/filenames only. Honor an explicit user-selected scope/range; otherwise select unstaged changes, falling back to staged changes when none are unstaged. If neither exists, report no changes and request a range. Record the chosen selector and keep it for investigation. Do not silently combine staged and unstaged scopes.

A large diff (>500 lines) needs focused batching, not an early content dump.
This phase selects the Git diff only. Locating feature documents and determining
task scope belong to investigation after checklist loading. Finding a task file
in a status/listing result does not make its requirements part of preparation.

### 3) Detect profiles and route all checklists

Invoke [shared-profile-detection.md](shared-profile-detection.md) with the scoped filenames. Read each known profile's `DETECTION.md` (directly or as complete original contents in the bootstrap packet) and evaluate its authoritative signals; do not stop enumerating after an obvious extension match. Path matches alone do not activate a profile. Multiple profiles may apply. Resolve the plugin root from this skill's loaded location (parent of `skills/`) and construct absolute profile paths; do not forward unresolved root tokens into tools.

Batch the Known-profile reads together when supported, then reconcile expected paths with completed lookups. Record each rule's match/non-match or the shared procedure's explicit unavailable-file outcome; apply that procedure's ENOENT and root-resolution fallbacks. A skipped lookup leaves routing incomplete even when a file extension suggests an obvious profile. This prevents an assumed negative from hiding an additional applicable profile.

For every active profile, read its `profiles/<profile>/review-code/index.md`. Collect **Always load** entries. Evaluate filename/metadata **Load if:** predicates first. For declared content predicates in detection or conditional loading, inspect at most approximately 16 KiB per candidate file, solely to resolve the predicate; log predicate/path. Apply the detection protocol's YAML document rules where relevant. If a conditional cannot be decided within the bound, conservatively select its instruction. Do not defer any conditional until after full source investigation.

Collect `(profile, checklist, triggered_by)` records for all matching/conservatively selected entries, carrying detection provenance and noting conservative selections. Indexes are authoritative; never hardcode checklist names. No profile means an empty list, not omission of the common method.

### 4) Read every resolved checklist

Read each selected `profiles/<profile>/review-code/<checklist>` using the resolved absolute plugin root, or Read the complete selected-checklist packet from [packet preparation](packet-preparation.md). An index read is routing, not checklist loading: every selected link requires its returned original content, even for a tiny diff. Keep the source paths as a loading ledger and mark them loaded only when complete read results arrive. Do not batch investigation commands with these reads.

Before proceeding, emit a compact loading checkpoint naming the completed common-instruction reads, every known profile's detection-lookup outcome, and the loaded checklist paths (or explicitly no active profiles). Any selected path without returned content keeps the gate closed; surface unreadable instructions and stop, except for detection fallbacks explicitly defined by the shared procedure. This checkpoint records evidence already obtained, not a promise to load guidance later. It catches accidental index-to-diff shortcuts without creating a separate artifact or replacing the actual read events.

### 5) Investigate behavior and compatibility

This is the single entry point for subject-matter investigation. With methodology loaded:

- Locate and read available component README/contract documentation and relevant requirements/task documents first; build task scope with the shared protocol and establish explicit intent and preserved invariants. Label inference where no contract exists. Distinguish review base/candidate from any release baseline.
- Then read the full diff using the selector from scope and re-read every changed file at the reviewed revision, accounting for deletions. Do not rely on an earlier conversation's contents. Use index blobs for staged review and the selected candidate revision for a commit range; do not silently substitute unrelated worktree contents.
- Apply the common functional method: trace changed behavior through relevant dependencies and unchanged consumers, exercise concrete scenarios, and assess relevant delivery combinations. Obtain actual historical source when needed; label provenance and unavailable evidence using the shared context rules.
- Search `kk:review-findings` for relevant patterns and, for active programming-language profiles, `kk:lang-idioms`. With no language results, optionally index a canonical idioms source under that label. Skip language lookup for non-language profiles.

If investigation adds targets covered by new profiles or newly applicable conditionals, pause analysis of those targets and return to routing/loading before continuing. Subsequent focused re-reads, reproductions and verification substantiate findings within this investigation; they do not create another full-diff preflight. Keep claims within actual access and evidence.

### 6) Apply profile and general checklists

Apply every loaded `(profile, checklist, triggered_by)` record to the affected behavior and diff. Domain checklists supplement the common method. Tag findings with their profile/checklist origin and detection signal; use `Profile: generic · Checklist: —` and `Triggered by: —` for common reasoning. Keep severity-major output and merge duplicate issues across lenses.

General guidance that applies regardless of profile — apply these categories on every diff, whether or not a profile-specific checklist covered them:

- **SOLID / architecture:** SRP violations (overloaded modules with unrelated responsibilities), OCP (frequent edits to add behavior instead of extension points), LSP (subclasses that break expectations or require type checks), ISP (wide interfaces with unused methods), DIP (high-level logic tied to low-level implementations). When you propose a refactor, explain _why_ it improves cohesion/coupling and outline a minimal, safe split. If refactor is non-trivial, propose an incremental plan instead of a large rewrite.
- **Security / reliability:** XSS, injection (SQL/NoSQL/command), SSRF, path traversal; AuthZ/AuthN gaps, missing tenancy checks; secret leakage or API keys in logs/env/files; rate limits, unbounded loops, CPU/memory hotspots; unsafe deserialization, weak crypto, insecure defaults; race conditions, check-then-act, TOCTOU, missing locks. Call out both **exploitability** and **impact**.
- **Code quality:** error handling (swallowed exceptions, overly broad catch, missing handling, async errors); performance (N+1 queries, CPU-intensive ops in hot paths, missing cache, unbounded memory); boundary conditions (null/undefined, empty collections, numeric boundaries, off-by-one). Flag issues that may cause silent failures or production incidents.
- **Removal candidates:** propose deletion only when a demonstrated current cost or defect justifies it and required behavior is preserved. A pending task's unreachable scaffold or disabled feature is not, by itself, a removal candidate. Distinguish **safe delete now** vs **defer with plan** when removal is warranted.

### 7) Self-check and confidence assessment

For **each finding** from Steps 5–6:

1. Re-read the relevant code and surrounding context independently.
2. Ask: **"Could I be misreading the code?"** — trace execution paths, check for runtime behavior, configuration, or framework conventions that might make this correct.
3. Ask: **"Is this a real issue or a style preference?"** — distinguish between bugs/risks and subjective choices that don't affect correctness or security.
4. Ask: **"What's the actual impact?"** — verify that the severity matches the real-world consequence, not just the theoretical violation.
5. Assign final confidence score (1–100%) with **explicit reasoning** documenting:
   - What was verified
   - What evidence supports the finding
   - What uncertainty remains
6. Downgrade or **remove** findings that don't survive the self-check.

### 8) Index findings

Index any P0/P1 findings that suggest a systemic or structural pattern (not isolated typos or one-off mistakes) as `kk:review-findings`. Index on first encounter — recurrence detection happens on the search side in future reviews.

- If no P0/P1 systemic findings exist, explicitly note "No findings to index" and move on.
- This step is mandatory — do not skip it even if the review found no issues.

### 9) Present results

#### Output format

Structure your review as follows:

```markdown
## Code Review Summary

**Files reviewed**: X files, Y lines changed
**Overall assessment**: [APPROVE / REQUEST_CHANGES / COMMENT]
**Intent and scope**: requirement source, current task/request, selected diff and candidate state
**Baselines**: review base/candidate; separate release baseline if applicable

## Behavior and Compatibility

Inspected paths/scenarios, observed results and evidence limits. Include applicable
Supported / Blocked / Unknown / Not applicable conclusions with named baselines.
Attribute author-supplied results and inherited issues. Record outstanding evidence
or release prerequisites, next actions and durable tracking locations when deferred.

---

## Findings

### P0 - Critical

(none or list)

### P1 - High

- **[file:line]** Brief title
  - Profile: {profile_name} · Checklist: {checklist_filename}
  - Triggered by: {signal_type} — {signal_description}
  - Trigger/path, expected vs actual result and consequence
  - Confidence: 90% - reasoning behind the confidence level
  - Suggested fix

- **[another_file:line]** Brief title
  - Profile: generic · Checklist: —
  - Triggered by: —
  - Trigger/path, expected vs actual result and consequence
  - Confidence: 60% - reasoning behind the confidence level
  - Suggested fix

### P2 - Medium

...

### P3 - Low

...

---

## Removal/Iteration Plan

(if applicable)

Only include recommendations tied to a demonstrated issue or an identified,
currently required verification gap. A clean scoped review needs no extra work.
```

**Inline comments**: Use this format for file-specific findings:

```
::code-comment{file="path/to/file" line="42" severity="P1"}
Description of the issue and suggested fix.
::
```

Apply [functional-review.md](functional-review.md)'s verdict mapping: a hard acceptance/delivery violation cannot be approved; material Unknown evidence receives COMMENT absent a demonstrated blocker. Out-of-scope operational unknowns do not automatically downgrade an explicitly scoped code verdict. Preserve P0–P3 impact severity and distinguish code correctness from release readiness.

**Every review** reports coverage and limits, even with findings. When no issues are found, explicitly state:

- What was checked
- Any areas not covered (e.g., "Did not verify database migrations")
- Specific residual risks or required verification gaps, when supported

### 10) Close the review or handle required next steps

When there are no actionable findings and no outstanding evidence/prerequisite
required by the reviewed task, end with the scoped verdict and coverage. State
that no changes are recommended. Omit a Next Steps menu, remediation choices and
invitations to start pending work. A clean review is a complete result.

When action is needed, list only substantiated findings and specific required
evidence or prerequisites. Ask which actions to take only when the current request
has not already authorized them; an invoking implementation request may already
cover fixes. Review-only work still does not authorize edits.

Apply the same evidence threshold to every suggestion, including optional notes
and proposed menu choices. A rejected hypothetical concern does not become valid
by moving it out of Findings or offering it as future preparation. Retain material
unknowns and the common method's conditional verdicts; this closing branch does
not waive unverified requirements.

### 11) Verify outputs

Before declaring the review complete, check each item in the **Required Outputs** section of SKILL.md:

- [ ] Review report presented to user
- [ ] Intent, scope/baselines, inspected behavior, applicable compatibility conclusions and evidence limits reported
- [ ] P0/P1 systemic findings indexed as `kk:review-findings` (or explicitly noted "No findings to index")
- [ ] Required next steps handled, or clean review closed without proposing new work

If any item is unchecked, go back and complete it before proceeding.
