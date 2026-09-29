# Implementation: comprehension-focused editing

> Status: in-progress — Tasks 1–3 complete; Tasks 4–5 pending
> Design: [design.md](design.md)
> Execution: [tasks.md](tasks.md)

## 1. Standalone editing of local documentation

Create `klaude-plugin/skills/clarify-docs/SKILL.md` and the shared procedure at
`klaude-plugin/skills/_shared/document-clarity.md`. Link the latter through
`clarify-docs/shared-document-clarity.md` → `../_shared/document-clarity.md`.

The skill entry point owns triggering, target selection and output expectations.
Use a short, trigger-first description for improving the clarity of existing human
documentation. The shared procedure owns understanding sources, selecting essential
meaning, editing and verification. It must not depend on toolbox-repo documents or
private examples. State its rules and rationale in the shipped instructions.

The top-level workflow loads the shared procedure before subject-matter reads. Once
loaded, the procedure reads the selected artifact and the relevant underlying work.
Do not introduce a preliminary content scan that bypasses instruction loading.
No new profile resolver, agent or dependency is required.
Measure the newly mandatory shared instructions with `wc -w`: target at most 1,000
words and do not exceed the design's 1,200-word ceiling, including any mandatory
linked instructions added by the procedure. Record the count in `verification.md`.

Inputs are the selected target and any supplied audience, purpose, requirements or
source references. Infer these from current context where justified; ask about
consequential ambiguity. Keep edits inside the selected scope. Reading related code
or requirements does not authorize editing them.

The editor must be able to explain the behavior behind a claim before changing its
presentation. A document's assertion is not sufficient verification. Trace code at
the relevant revision and distinguish requirements, current behavior, proposals and
test evidence. Reuse applicable source understanding from the invoking session;
inspect missing context rather than repeating unrelated investigation.

If the document is already clear, make no cosmetic rewrite. If its claims conflict
with source or requirements, correct only evidence-backed factual errors and keep
unresolved intent/implementation disagreements visible with a next action. No
arbitrary new report, claim ledger or summary file is produced.

Register `clarify-docs` in `test/test-plugin-structure.sh`'s `EXPECTED_SKILLS` after
the files exist. Add user guidance to `docs/user-guide/skills.md` describing inputs,
source understanding, preservation and unchanged-output behavior. Update the maintained
inventories in `README.md`, `klaude-plugin/README.md`, `docs/user-guide/skills.md`,
`docs/getting-started/index.md`, `docs/getting-started/overview.md`,
`docs/getting-started/plugin-only.md` and `docs/contributing/architecture.md` (whose
counts are already stale). These are mechanical count/catalog updates; do not add
the utility as a required pipeline stage or rewrite frozen feature history.

For an explicit agent-instruction or `SKILL.md` target, report that it is outside
editorial scope and suggest `/kk:implement`, without invoking it. Its own detection
selects `skill-md` where appropriate. Use this same behavior in the trigger text and evals.

**Verify:** staged local-document cases demonstrate the claimed behavior; plugin
structure and graph validation resolve the new skill and shared link. Check the
current upstream description limits before authoring the new description, as required
by repository conventions.

## 2. PR drafts and audience boundaries

Extend the entry point and the same shared procedure to existing PR-description
drafts. This is one editorial workflow with artifact-specific context, not a second
copy of the rules.

- An existing local draft is edited in place. A PR URL or supplied PR text can be
  used as input; obtain its body and review context with available read-only tools.
- For a remote or pasted input, use the caller's destination or a named local draft
  under the current feature directory. If neither scope nor destination is clear,
  ask before writing. Never overwrite an unrelated existing file.
- Inspect the actual base/head and relevant diff for a PR; do not infer the increment
  solely from a stack annotation, branch name or task number. Report missing source
  access and limit unsupported statements.
- Explain the problem, resulting behavior, current increment, concrete example when
  useful, focused review path and meaningful validation. Avoid a commit diary or
  listing every changed file as the default explanation.
- Apply the ordered visibility rules in [the design](design.md#truth-preservation-and-visibility)
  and encode them in the shared procedure: explicit restrictions first, target-repo
  audience and PR-head membership second, evidenced external access third, and unknown
  visibility requiring an accessible alternative or clarification. The editor's own
  credentials prove no audience access. A tracked but restricted file cannot be
  disclosed; an accessible task reference need not be removed. Missing public evidence
  cannot justify an invented link or a private proposal presented as settled.
- Output a local artifact and a brief account of changes or unresolved gaps.
  Publishing is a separate action requiring its own authorization; this workflow
  does not call PR-update, comment or messaging tools.

**Verify:** PR cases distinguish contract-only and runtime increments, respect the
actual diff, and remove inaccessible pointers without losing authorized meaning.
Privacy fixtures declare audience/access facts and assert both exclusion of restricted
material and retention of legitimate shared references; they do not classify every
`docs/feat/` path or task number as private.

## 3. Reuse in existing writing workflows

Add per-skill links to `../_shared/document-clarity.md` in `design/` and `document/`.
Keep all operative prose in the shared file. Consumers supply the reader, selected
outputs, requirements and applicable implementation evidence they already have.

| File | Change |
| --- | --- |
| `klaude-plugin/skills/design/SKILL.md` | Include the shared procedure in mandatory instruction loading and summarize the final editorial pass. |
| `klaude-plugin/skills/design/idea-process.md` | Apply the pass after all three design artifacts are drafted, before recommending review; preserve their required sections and task format. |
| `klaude-plugin/skills/design/existing-task-process.md` | Apply the pass only to documents changed during refinement, before handoff; do not rewrite docs on an unchanged resume. |
| `klaude-plugin/skills/document/SKILL.md` | Load shared instructions before subject matter; apply the pass after documentation updates while preserving domain-rubric coverage. |

The final pass can reuse content already read during drafting. It verifies missing
or changed evidence instead of requiring a second complete repository investigation.
The shared procedure has no call back to `/kk:design`, `/kk:document` or
`/kk:clarify-docs`; this prevents recursion. Do not add another pass to
`/kk:implement` plan mode, whose completion already calls `/kk:document`.
Standalone implementation receives no new completion step. State this qualification
in user guidance and test both modes rather than advertising automatic coverage for all fixes.

Keep the downstream review boundaries from the design explicit: design output retains
the `/kk:review-design` recommendation; standalone editing and `/kk:document` have an
in-session check, followed by whatever review the caller's project requires. Do not
label their output independently verified or add a mandatory isolated runtime gate.

**Verify:** integration evals show instruction loading before content, drafting before
editing, preservation of required sections and exactly one pass over the selected
outputs per writing invocation. An unchanged WIP resume does not trigger a rewrite.
The mode-coverage regression must demonstrate that standalone implementation does not
gain a documentation call just because plan-mode completion has one.

## 4. Evaluation fixtures and release checks

Use the repository's per-scenario `eval.json`, `test-files/` and sibling `oracle/`
layout. Put most cases under `clarify-docs/evals/`; consumer-ordering cases belong
under `design/evals/` and `document/evals/`. Fixtures are synthetic and self-contained.

| Scenario | Required evidence |
| --- | --- |
| Dense document with implementation-dependent meaning | Editor reads supplied requirements/source and explains the actual behavior; all reader answers and protected claims survive. |
| Prose conflicts with code or a product requirement | Mismatch remains explicit; no invented decision or silent requirement removal. |
| Missing consequential context | Accessible context is investigated first; remaining uncertainty is surfaced. |
| Multi-document feature plan | Required headings, task state, decisions and cross-file links survive reorganization. |
| Contract-only PR and a later runtime PR | Current versus future behavior and actual review increments remain distinct. |
| Destination visibility | Declared-private aggregator data and tracked-but-restricted content stay private; accessible target-repo tasks remain usable; credential-only and unknown external access do not establish audience access. |
| Already-clear artifact | No gratuitous rewrite or extra summary file. |
| Clear prose with another defect | All five baseline answers pass, but a prohibited reference or source-backed factual error is still repaired; a genuinely clean baseline stays unchanged. |
| Code request, generic brevity request or agent-instruction target | Non-triggers stay inactive; explicit instruction targets receive the `/kk:implement` suggestion with no edit or automatic handoff. |
| Design/document final-pass integration | Correct ordering, bounded outputs, no recursion; plan-mode implementation inherits the pass and standalone mode has no added completion. |

### Fresh-reader protocol

1. Before editing, fix the five comprehension questions, source-backed expected
   answers, protected claims and concrete orientation assertions. Keep expectations
   in `oracle/`. Assertions must name observable defects, for example an unexplained
   term before its first use or a missing distinction between current and future behavior.
2. Run the editor in a session with the target skill and staged `test-files/`, including
   requirements and code it needs to understand. Capture its output and tool trace so
   source-inspection assertions can be graded. It sees no oracle or reader responses.
3. Launch two separate general-purpose read-only reader sessions with no inherited
   history (`fork_turns="none"` when using the Codex collaboration tool): one gets
   the original and one the revised artifact. Use the same model/settings, neutral
   reader role and five questions. Each gets only its artifact and an explicit manifest
   of audience-accessible linked sources; neither gets the other version, the editing
   skill, source-only editor context, tool trace or oracle. Require answers with pointers
   into that reading path and an explicit uncertainty statement when an answer is missing.
4. Have a separate grader session compare answers with the oracle and inspect the
   editor's trace and before/after artifacts for fidelity and orientation assertions.
   Give it the required source evidence. Use a general-purpose reviewer for this
   fixture-reading job; `klaude-plugin/agents/eval-grader.md` forbids fixture access
   and only grades supplied reviewer text. No new persistent agent definition is needed.
5. Record a PASS/FAIL/PARTIAL for every assertion; PARTIAL or missing evidence is not
   a pass. The revised artifact must pass all applicable comprehension, correctness,
   fidelity, visibility, structure and orientation assertions. When baseline answers
   already pass, an edit needs a predeclared defect in any of these dimensions that
   is demonstrably fixed while answer accuracy is preserved. Expect no-op only when
   the baseline meets all applicable requirements. If baseline answers fail, require
   the revised answers and the other applicable assertions to pass. Preserve explicit
   unknowns when they are the correct source-backed answer. Report the observed
   comparison, not a claim that an AI reader proves improved comprehension for all humans.

Create `docs/feat/wip/clarify-docs/verification.md` when runs begin. Index each run by
scenario, date, model/version/settings, staged input revision or hashes and verdict.
Store its manifest, editor output/trace, original/revised reader answers and grader
verdicts under `verification/<run-id>/<scenario>/`, linked from that index. Mark
authored-but-unrun scenarios explicitly. Keep oracle files outside editor/reader
staging; an agent sharing the repository is not filesystem-isolated merely because
its prompt says so, so enforce an allowed-file manifest and inspect tool traces for
access leakage. If clean staging is unavailable, record the isolation limitation
and do not label that run valid. This remains a manual protocol, not a new eval runner.

### Release checks

Run `make generate-kodex` after each operative skill change. Validate the generated
skill, shared links and rewritten `/kk:` references. Use `bash test/test-plugin-structure.sh`,
`bash test/test-codex-structure.sh` and `make plugin-graph` during relevant slices;
run the full repository checks at final verification. A second generation must produce
no further generated-file changes. Do not edit generated artifacts by hand or repair
deliberately partial fixture links.

## Deferred work

Automatic PR-authoring integration is excluded from v1 because no owning workflow
exists. If one is added later, reuse this procedure at its draft-completion boundary
and add an integration eval; do not create a parallel editorial implementation.
The maintainer deciding that workflow owns this follow-up. No unresolved v1 decision
depends on it.

An optional isolated runtime fidelity check is deferred. **Owner:** feature maintainer.
**Reason:** it adds a second source-reading pass and runtime latency to every use if
made mandatory, while the agreed v1 provides an editorial self-check. **Next step:**
if fidelity eval failures or real edits show residual errors, design an opt-in verifier
with explicit evidence scope and an eval comparing its detection benefit and cost.
Until then, preserve the entry-point review limits above; do not claim self-checking
is independent verification.
