# Implement functional and operational review

> Design: [design.md](design.md)
> Tasks: [tasks.md](tasks.md)
> Status: planned; no operative skill changes implemented

## Starting points

The canonical source is klaude-plugin/. Relevant current files:

- skills/review-code/SKILL.md and review-process.md: standard review and report contract.
- skills/review-code/review-isolated.md and commands/review-code/isolated.md: isolated preparation, delegation and report.
- agents/code-reviewer.md: independent review method and output.
- skills/_shared/review-scope-protocol.md: task-scope semantics, also consumed by /kk:review-spec.
- skills/_shared/pal-codereview-invocation.md: external invocation shared with /kk:review-design.
- skills/implement/SKILL.md, plan-mode.md and standalone-mode.md: entry, shared execution and completion.
- skills/review-code/evals/_harness/{setup.sh,HARNESS.md}: existing fixture staging and independent grading playbook.

The source baseline for the design is c2d28c9e. Re-read current files at kickoff; preserve concurrent changes. Existing installed skill caches are not implementation targets. Preserve a reproducible baseline instruction revision before Task 1 so later-authored scenarios can still compare the old and new workflows.

## Delivery and verification rules

Each slice must leave its changed invocation path usable, retain existing profile behavior and preserve consumer compatibility of shared instructions. Use source-relative links and per-skill shared symlinks. Agents resolve instruction paths from their injected absolute plugin root. Do not introduce toolbox-doc links into distributed plugin instructions.

After every canonical skill/agent slice, run make generate-kodex and include its actual generated changes with that slice. Do not hand-edit generated files. Run the plugin/codex structure suites and make plugin-graph to verify the new references and generated topology. For freshness after regeneration, compare a second generation against a saved generated snapshot, or stage intended generated changes and check for unstaged drift; do not mistake the expected implementation diff against HEAD for stale output.

Use behavioral dry-runs for the acceptance cases. A grep assertion that a paragraph exists is not evidence the agent performed the reasoning. Record tool failures and skipped checks accurately. No application deployment or private production access is needed for this feature.

## Standard review slice

Targets: review-code/SKILL.md, review-process.md, new functional-review.md; new _shared/change-context.md; _shared/review-scope-protocol.md. Add review-code/shared-change-context.md pointing to ../_shared/change-context.md.

1. Define the shared fields, provenance, evidence-qualified compatibility conclusions and producer/consumer duties from the design → verify: an ad-hoc diff and a planned task can both supply the record without requiring production access or new infrastructure.
2. Implement the common behavior investigation and findings/coverage requirements in functional-review.md → verify: the R1 fixture requires following an unchanged caller and reports a supported sequence and consequence.
3. Link and load both instructions from the standard entry point, then integrate investigation and reporting into review-process.md → verify: a normal /kk:review-code prompt performs the work, including with no spec and no active profile.
4. Align mandatory ordering: resolve conditional profile content through bounded predicate inspection, load it before full evidence analysis, and remove the conflicting deferred-load sequence → verify: captured tool ordering shows instructions before full diff/source investigation; targeted later evidence checks remain possible.
5. Clarify shared task-scope semantics for current breakage versus incomplete future functionality → verify: R3 flags current incompatibility; R5 does not flag intentionally pending features. Review /kk:review-spec's existing caller contract for compatibility.

Replace the SOLID-only title and overview with a description of the complete review responsibility while retaining SOLID/security/profile coverage. If editing the frontmatter description, verify the current documented description limits before writing it; keep trigger-first wording and the repository's portability budget.

## Isolated review slice

Targets: review-isolated.md, agents/code-reviewer.md, _shared/pal-codereview-invocation.md and commands/review-code/isolated.md.

1. Reorder isolated preparation so methodology/profile loading precedes diff analysis; gather change context after that gate → verify: the real isolated invocation loads instructions before evidence, rather than relying on prompt delivery order.
2. Include shared context, method paths, task scope and evidence references in the agent payload and PAL framing/file manifest → verify: both receive required facts; absent spec retains functional review; neither receives implementation-session history.
3. Teach the agent to load common methodology before evidence, independently verify relevant claims, and emit coverage/compatibility beside existing findings → verify: R1/R3 survive isolated review and source-only review does not claim executed tests.
4. Select external files by affected behavior, with the current surrounding-file count used as an initial budget and explicit missing-context handling → verify: an unchanged consumer essential to R3 reaches the external request; truncation/failure is reported.
5. Preserve native PAL findings, annotation and failure behavior; add report coverage and constrained conclusions → verify: R8 cannot become an unconditional clean or release-safe review.
6. Qualify shared PAL instructions by review type and update the command summary → verify: /kk:review-design still accepts document-only inputs and does not acquire code compatibility fields.

The shared record and method are authoritative; do not copy whole procedures into each prompt. The spawning workflow resolves absolute paths; the independent reviewer reads them through its existing tools.

## Implementation slice

Targets: implement/SKILL.md, plan-mode.md and standalone-mode.md. Add implement/shared-change-context.md pointing to ../_shared/change-context.md.

1. Load the shared context instructions alongside current mandatory instructions → verify: plan and standalone invocations load the contract even without active profile content.
2. Reconcile entry/core ordering: use request/doc context and candidate filenames first; move detailed standalone source investigation after profile/instruction loading. Set task in-progress only after the instruction gate → verify: existing pre-write evals still pass and there is one authoritative source-investigation entry.
3. Before implementation edits, inspect affected behavior, establish intent and applicable delivery constraints, and add specific verification cases → verify: I1 identifies its incompatible approach before editing and I2 proceeds with grounded context without a new feature-plan requirement.
4. Preserve user decisions and surface only material conflicts/unknowns; choose the simplest mechanism consistent with the constraints → verify: I3 does not create an irrelevant release gate or ask ceremonial confirmations.
5. Refresh context after implementation/fixes and pass it into the existing independent review → verify: both review paths receive the actual scope and baseline, and I4 rejects stale handoff evidence.
6. Separate task completion from deployment/activation readiness and durably own deferred work → verify: I4 cannot mark a violated hard requirement done or turn an unknown environment into a supported release.

No new global rule requires all projects to use independent deployment or feature flags. The skill discovers applicable policy and states the assumptions behind the chosen approach.

## Evaluation staging and execution

### Fixture format

Retain existing eval.json fields and per-eval layout. For the new before/after cases only, use a paired test-files/before/ and test-files/after/ convention. Each directory is a complete synthetic repository snapshot; unchanged context appears in both. The before snapshot becomes a base commit; the after snapshot is the staged candidate. Top-level scenario documents within each snapshot contain only information legitimately available to the acting user/reviewer, such as requirements, release policy or a recorded baseline.

Extend setup.sh to recognize the pair, reject a missing half, initialize the base from before/, replace the working tree with after/ while preserving .git, and stage additions/modifications/deletions. Preserve the existing all-added path for legacy fixtures. Snapshot roots must not contain .git or links escaping the fixture tree; validate before copying. Stage into a fresh owned directory and fail if a destination already exists; do not recursively delete a caller-supplied directory. Neither eval.json, oracle/ nor the before/after wrapper directories enters the candidate workspace.

Add test/test-review-eval-staging.sh, using existing shell test helpers, to exercise additions, modifications, deletions, unchanged callers, hidden files, malformed pairs, unsafe fixture paths and destination refusal. Keep the tests offline. This is limited fixture plumbing, not a general evaluation platform.

The new review case IDs must not collide with the existing registry. Allocate subsequent numeric IDs when authoring, preserving existing values. Use R1–R9 only as design traceability labels in scenario descriptions/reporting; give the two R9 variants separate eval directories and IDs. Apply the same policy independently to implement I1–I4. Every fixture file is declared in files[]; grader answers remain in sibling oracle/ and are never staged.

Before Task 4 adds automated snapshot support, stage the small Task 1/2 fixtures manually using exactly the same before-commit/after-staged contract in fresh temporary repositories. Do not run the legacy all-added helper on a paired fixture. Once extended, the helper stages both old and new cases correctly.

### Workflow coverage

Update HARNESS.md to distinguish the existing profile-resolver/reviewer component tests from full skill tests. Existing component tests remain useful but cannot validate orchestration, standard mode, implement preparation or the PAL handoff.

For each new full skill run, stage a fresh fixture and give a fresh acting session only the natural eval prompt, staged workspace and target plugin instructions. The acting session may invoke the skill's normal isolated reviewers. The orchestrator/independent grader retain assertions and oracle evidence separately. Never seed the acting session with the expected conclusion, special "production safety" reminders, or preselected surrounding files that it is supposed to discover.

R1–R7 and both R9 variants run in standard and isolated modes. Use mode-appropriate normal prompts; capture source reads, payloads, findings and coverage. R8 uses a clearly labeled controlled PAL response to test failure/coverage handling; also perform an available real PAL smoke run, recording exactly what was read. A stubbed result does not establish real tool coverage.

For implement, stage the I1/I4 task documents and I2/I3 standalone requests in disposable workspaces. Capture pre-edit ordering, edits, review handoff, verification and task/report state. Document this procedure in implement/evals/README.md; that playbook is operator guidance, not automatically loaded by /kk:implement.

For each slice's initial fixtures, record the unchanged baseline run before its operative edit. Later-authored cases run against the preserved baseline instruction revision and the candidate; reuse the same fixtures and model configuration for comparison. Explicitly bind each acting session to the intended baseline or candidate plugin root, including that revision's generated Codex agents where applicable, rather than silently using an installed cache. If a run fails, retain its result and reason; a rerun after a correction does not erase it. Final evidence records model/provider, instruction revision, fixture revision, mode, available tools, pass/fail/partial/unrun per assertion, false positives and relevant scope/latency observations. No specific model winner or absolute latency SLO is asserted.

### Acceptance record

Store sanitized run summaries under this feature's verification/ directory during implementation. Keep all R/I cases and existing regression controls visible. Required assertions must pass before declaring implementation verified. Tool unavailability is an explicit unrun gate with a next action; do not report those paths as verified or silently waive them. Source/plugin structure checks and behavioral results are separate sections of the record.

## Documentation and final verification

Update README.md and docs/user-guide/skills.md to describe ordinary functional review, implement preparation, evidence limits and the distinction between code completion and release readiness. Update docs/contributing/testing.md for the new staging test and before/after fixture convention. Preserve the existing skill names and user invocation syntax.

Final verification runs:

- /kk:test with all repository test/test-*.sh suites; include the new staging suite.
- make generate-kodex and a second-generation freshness check, including .codex/agents/.
- make plugin-graph for Go tests and broken-link/orphan validation.
- go test ./... for the repository Go tools.
- The full applicable behavioral matrix and the existing review profile-routing/implement pre-write controls.
- /kk:document, /kk:review-code using resolved skill-md and any actual shell/fixture profiles, and /kk:review-spec against these design documents.

Verify shared consumers explicitly: /kk:review-spec retains pending-task filtering and /kk:review-design retains its PAL document contract. Do not "repair" intentionally broken eval/template links.

This design-writing task itself requires only document consistency and link checks. No implementation test pass, behavioral improvement or independent review is claimed by creating these documents.
