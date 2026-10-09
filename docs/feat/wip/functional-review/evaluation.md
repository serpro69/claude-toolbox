# Evaluation contract

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Tasks: [tasks.md](tasks.md)
> Status: loading verified, seeds frozen and 16 baselines captured; four Codex captures and behavioral acceptance remain open
> Revised: 2026-10-09; [run-contract amendment](verification/run-contract-2026-10-09.md)
> Reviewed claims: [consolidated disposition](reviews/design-review-consolidation.md)

## Comparison identity and acceptance

Use one immutable pre-feature actor baseline: c2d28c9e (v0.23.0), resolved to its full commit ID when preparing runs. The current design-only commit does not change operative skills. Every later baseline run uses this same actor revision, never the working tree after an earlier feature task.

Task 2 gate 2A preserves the final R1, R3, I1 and I2 fixture directories, frozen inputs and 16 captured baselines before operative edits. It is complete. Gate 2B owns the remaining four Codex baselines and may finish after development starts, using the preserved actor revision. Tasks 3–11 may proceed in sequence; Task 12 and feature completion still require 2B. Later cases likewise run against the preserved revision after their fixtures exist. Capture baseline and candidate on identical fixture bytes; a substantive fixture correction invalidates the comparison and requires both sides to rerun. The grading procedure/rubric is pinned before capture. Pin the concrete grader implementation before grading either side and hold it constant across the comparison; baseline traces can be captured before that implementation exists.

Write a run-contract.md under verification/ before the first measured baseline run. Record the full baseline revision and hashes, fixture hashes, exact runtime version, all main/reviewer/PAL model identifiers and reasoning settings, tools, permission policy, prompt, declared modes, grading procedure, repetition count and acceptance threshold. The candidate revision is pending until code exists; freeze and record its source/generated hashes before each candidate batch. A later fix creates a new identified candidate, never a mutable alias for earlier results. Launch probes may use a second baseline copy to validate the candidate loading location, but that is not a behavioral candidate result. The primary provider runs the complete matrix; the other distributed provider runs binding and representative R1 standard, R3 isolated, I1 plan and I2 standalone checks. Select and record the primary provider before observing results. Report full-matrix and representative coverage separately; do not claim full behavioral parity from generated-file checks or selected cases.

All assertions[] entries in new full-workflow evals are required; no schema extension or required flag is needed. Put optional cost/latency observations in the run summary, outside assertions[]. Run two independent fresh sessions on each side for every required case/mode in its declared coverage. Candidate acceptance requires PASS on every assertion in both sessions. FAIL, PARTIAL and unavailable evidence never count as PASS. This is a conservative observed-twice gate, not an estimate of model reliability. Retain all attempts; after a fix, rerun the affected pair using the new candidate revision. If the baseline already passes, report that fact without inventing an improvement.

Do not lower the threshold, switch the primary provider or replace a fixture after seeing failures without recording a revised run contract and repeating the affected baseline/candidate comparison.

### Codex handoff capture resolution

**Authority and owner.** On 2026-10-09 the user approved the sequencing change and conditional fallback below. The implementing agent owns gate 2B: Codex R3 isolated and I2 standalone, two baseline repetitions each. Original captures, assertions and the frozen revision-1 rubric remain unchanged until a successor contract is explicitly recorded; ciphertext never satisfies an exact-prompt assertion.

1. **Bound the investigation.** Identify a supported capture surface or runtime alternative that differs materially from the two failed probes. Record why it could expose submitted messages, then run at most one additional fresh synthetic-marker probe. Success requires the actual readable submitted message, its parent/call/receiving-child linkage and observable child reads of the referenced immutable evidence. A schema field, child echo or final actor confirmation alone is insufficient. Record failure or the absence of a viable alternative and stop; do not repeat unchanged probes, decrypt protected content or build an open-ended tracing system.
2. **Choose the evidence path.** If that probe succeeds, retain the exact-handoff assertions and capture the missing baselines. Otherwise activate the authorized receipt/use fallback through a successor rubric and assertion mapping before measured runs. It requires actual named-reviewer and PAL invocation identities, independently observable reads or embedded-source evidence tied to immutable content hashes/provenance, and each reviewer's result demonstrating use of the material context. R3 still requires both reviewers to use the historical provider source in the compatibility comparison. I2 still requires both to receive and use the finished diff, requested semantics, unchanged callers and attributed verification evidence. Parent summaries, mere file availability, hashes without receipt evidence and a correct final answer alone cannot pass. Missing external source coverage remains explicit and cannot satisfy a required evidence assertion.
3. **Version before measuring.** Record the probe outcome and selected path in a new run-contract amendment. If falling back, preserve the original assertion/oracle bytes at a recorded immutable revision or archive, create `verification/task2-rubric-v2.md` and `verification/task2-frozen-v2.json`, and update the final R3/I2 eval definitions and generated copies with a precise old-to-new assertion mapping. Keep subject fixtures and ordinary prompts unchanged. Both providers and both comparison sides use the same revised behavioral assertions; retain raw dispatch evidence wherever available. Do not overwrite the original freeze, rubric, capture manifests or grades. Apply the selected rubric to both sides; regrade retained evidence where sufficient and recapture both affected sides where it is not. Runtime, model, permission-policy or material capture-configuration changes require a revised declaration and fresh affected baseline/candidate comparisons under matching conditions.
4. **Close capture, then grade.** Complete the four missing baseline runs and any required baseline recaptures with sufficient evidence to grade the selected assertions; candidate counterparts remain Task 12 work. Observed baseline failures are data and do not prevent capture completion. Gate 2B closes when its investigation, contract selection and baseline captures are recorded; Task 12 still requires every candidate assertion to pass twice. The fallback supports reviewer receipt/use, with exact submitted prompt content explicitly unverified. It does not certify byte-for-byte prompt parity or private inherited context. If receipt/use evidence is also unavailable, 2B remains open with the concrete missing capability; do not waive the runs or mark the feature complete.

The [dated run-contract amendment](verification/run-contract-2026-10-09.md) supersedes the original stop-development instruction. It changes no captured result and starts no probe. The capture failure is deferred from implementation readiness because the immutable baseline can still be launched later, not because incomplete evidence counts as acceptance.

## Bind the actual instructions

A root in the prompt or TOOLBOX_PLUGIN_ROOT alone does not bind a full skill invocation. Bind entry points, auxiliary instructions, profiles, agents and generated output from one revision. Run each repetition in a new process/session, with no resumed implementation or prior-eval history.

Preserve the baseline checkout and a fixed candidate snapshot in controller storage outside the actor's inputs. Build a separate actor instruction bundle for each revision/provider before launching it. Never edit an installed cache to switch versions. Record the resolved entry-point and agent locations, byte hashes and the active plugin identity from the host's loading/catalog evidence. Fail the launch probe if those cannot be reconciled with the intended bundle manifest. A model saying it used the requested revision is insufficient.

### Actor instruction bundles

The complete plugin trees are not suitable actor inputs: canonical and generated skills include eval.json, oracle/ and other evaluator material. Build a filtered copy of klaude-plugin/ for Claude and kodex-plugin/ for Codex, retaining manifests and all operative skills, shared instructions, profiles, agents, hooks and scripts. Exclude every evals/ subtree and controller-only verification/report artifacts. Copy required runtime files rather than linking back into the unfiltered checkout; resolve shared symlinks within the filtered bundle. The generated project agent files come from the same revision and contain no fixture/oracle material.

Apply the same path-based exclusion policy to baseline and candidate. Preserve retained file bytes and operational symlink semantics; do not edit instructions to make the tests pass. Record a full-source manifest, the exclusion list and a retained-bundle manifest so source identity and actor input identity remain distinct. Compare loaded/cache bytes against the retained-bundle manifest. This is eval packaging only; do not change normal plugin distribution or the generator's production output for this purpose.

Before any actor starts, scan its bundle, mounted paths and installed cache copy for eval metadata, oracles, grading fixtures and saved results. Fail setup if any are present, a retained symlink escapes to the unfiltered checkout, or a required runtime resource was removed. Keep controller checkout/oracle paths out of actor prompts and catalogs; where filesystem isolation is supported, exclude those roots. A detected actor read of grading material still invalidates the run. Merely excluding the files from Git diff is not input isolation.

### Claude Code

Launch from the staged fixture using the documented --plugin-dir flag pointing to the selected revision's filtered Claude bundle. This loads entry points and agents from that directory. Current loading rules prefer the session plugin over an installed plugin of the same name except where managed policy locks it; capture loading/debug evidence and fail on a policy conflict. Use the same explicit model and tool configuration on both sides. See [local plugin loading](https://code.claude.com/docs/en/plugins/create#load-a-plugin-for-one-session) and [name precedence](https://code.claude.com/docs/en/plugins/loading#name-conflicts).

The repository's SessionStart hook is an additional binding surface: scripts/set-plugin-root.sh prefers cpr.py's installed-registry result over its plugin-load argument. Supply a run-specific CPR_PLUGINS_FILE registry containing only a kk entry for the selected filtered bundle and staged project. This environment override already exists in cpr.py and test/test-cpr.sh. Confirm that the resulting TOOLBOX_PLUGIN_ROOT resolves to that same bundle, not its unfiltered source checkout. Merely overriding TOOLBOX_PLUGIN_ROOT before the hook runs is insufficient.

Use the ordinary /kk:review-code, /kk:review-code:isolated or /kk:implement prompt from eval.json. Keep hook behavior and MCP capabilities identical on both sides, with the per-run state locations and declared vault policy below; do not use a minimal mode that silently removes the behavior being evaluated. Validate binding in a separate disposable launch probe so it does not supply defect hints or persistent memory to the measured session.

### Codex

Use a revision-specific local marketplace, not a root-variable override. In the disposable subject repository, mount the selected revision's filtered Codex bundle at a fixed runner-owned path and register it in .agents/plugins/marketplace.json. Give baseline and candidate distinct marketplace names containing their revision identity; retain the plugin's kk identity and unchanged generated skill bytes. Enable only that kk marketplace through the trusted project's .codex/config.toml, and disable other visible kk installations for the run. Follow the supported local client's installation/refresh and fresh-session steps. The [local marketplace documentation](https://developers.openai.com/plugins/build/plugins#install-a-local-plugin-manually) specifies discovery, project enablement and installed-cache behavior.

A local marketplace can load an installed cache copy. After installation/refresh, compare its retained files with the filtered-bundle manifest and repeat the evaluator-material scan; reject stale, mixed or unfiltered copies. Copy that same revision's generated .codex/agents definitions into the disposable project's .codex/agents/ before startup. The [custom-agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents) describes project-scoped TOML discovery. Verify the effective role definitions, not only their filenames; fail the probe if a personal/managed role prevents the intended role from loading.

Keep runner-owned .agents/plugin metadata, .codex configuration and mounted plugin bytes outside the evaluated diff using the staging repository's local exclude metadata. They must not contain assertions, oracles or expected findings. They are identical infrastructure on each side except for selected actor revision. Invoke the registered kk skill normally; do not substitute a pasted SKILL.md or only inject a root into a default agent.

Record any client-specific installation steps in the run contract. Task 1's [completed probes](verification/README.md#completed-probes-after-login-refresh) established revision-bound Codex loading; exact reviewer handoff capture remains unresolved. Loading must still be verified for the runtime/bundle used by each batch; unavailable or incompatible clients produce an unrun result, not a mixed-version fallback.

## Per-run state isolation

Every case, mode, baseline/candidate side and repetition gets a newly staged subject repository and fresh writable state. A new conversation alone is insufficient. Restore fixture bytes before each run; never reuse implementation edits, task updates, review notes, launch-probe state or a prior run's knowledge store. Record the actual initial fixture and knowledge-state identities alongside the instruction-bundle manifest.

Keep Capy search/index capabilities available, but give each run its own MCP server bound through capy --project-dir to that run's unique subject repository. Confirm the resolved knowledge path with capy which before launch. The default initial knowledge store is empty; if a case needs prior knowledge, define a fixed sanitized seed and create an independent copy for each run. Writes during a run are allowed in that run's store only and are never seeds for later runs. Main and child sessions use the same run-local service; hooks and any CLI access must resolve to that same run-local project.

For these synthetic cases, session-vault retrieval is deliberately unavailable on both sides: launch the server and hooks without CAPY_VAULT_KEY, set CAPY_VAULT_PATH to a fresh run-private path, and do not connect to a pre-existing shared Capy server. Record the unavailable-vault state and exercise the normal empty/unavailable-history fallback while retaining knowledge search/index behavior. Do not alter the user's real stores or credentials. Any future vault-dependent eval must declare an isolated synthetic vault seed as part of its fixture rather than use real archived sessions.

The launch probe must verify that run-local knowledge writes succeed and that a marker indexed in probe A is absent from fresh probe B. Neither measured run may inherit either probe's state. Include store resolution, initial seed identity and the declared vault fallback in the sealed evidence. A shared real store, an unexpected history hit or an inherited fixture mutation is a setup failure, not a behavioral PASS. Runner-owned state directories remain outside the evaluated diff.

## Fixture lifecycle and staging

Seed fixtures are final fixtures, not throwaway variants. Task 2 creates complete eval.json, test-files/ and oracle/ directories for R1/R3 under review-code/evals/ and I1/I2 under implement/evals/. Subsequent authoring tasks extend those same directories or add remaining cases. They never create a competing minimal copy. Author all metadata and assertions up front, including grader-only expected results; withholding them from the actor is the controller's responsibility.

New review snapshots use test-files/before/ and test-files/after/ as complete repository trees. For R3, add test-files/history/released/ plus test-files/history.json. That manifest names an ordered historical snapshot and a local tag (eval-release); it contains staging instructions, not expected answers. The controller commits historical snapshots first, then commits before/ as the PR base, then stages after/. The released provider behavior must be absent from both before/ and after/ and from the PR diff. It is reachable through the local release tag. The candidate's ordinary scenario contract names the release tag as its supported-provider baseline.

The staging helper must:

1. Recognize a complete before/after pair and reject a missing half; preserve the legacy flat all-added fixture path.
2. Validate snapshot paths and optional historical entries: no .git entries, escaping symlinks, path traversal, duplicate refs or tags that overwrite the PR-base identity.
3. Build optional history and the base commit, replace subject files with the after snapshot while preserving the owned .git directory, and stage additions, modifications and deletions.
4. Keep unchanged context available, preserve hidden files, and exclude staging wrappers, eval.json and oracle/ from the workspace.
5. Use fresh owned destinations and refuse existing ones. Never delete a caller-supplied tree.

Until Task 7 provides helper support, manually stage the seed fixtures with this same contract in disposable repositories. Existing setup.sh must not run against paired fixtures before it supports them.

Use the existing eval.json fields and numeric IDs. Allocate new IDs above the current per-skill maximum. Aggregate results by (skill, eval directory name, assertion ID), not numeric ID alone: implement's existing js-ts-standalone-loads-implement-guidance and python-new-file-loads-core both use ID 4. Preserve those historical IDs for this feature. Any future renumbering must update assertion IDs and references together; it is separate maintenance, not a release gate here.

## Execution-evidence contract

Extend klaude-plugin/agents/eval-grader.md with an explicit Grading mode field. Omitted mode means the existing component mode: reviewer output plus assertions, current tools policy, and the same PASS/FAIL/PARTIAL report. Full workflow runs explicitly select workflow mode; do not send traces to an unchanged component grader.

The evaluation controller, never the acting model, seals a per-run evidence package outside the subject workspace after capture. The workflow grader receives only:

- Assertion records, their evidence-source mapping and relevant grader-only expected outcomes.
- A manifest naming run identity, actor/fixture/grader revisions, evidence-file hashes, completeness and redaction notes.
- Ordered observable tool events: actor/session ID, parent/dispatch ID, event sequence, tool name, arguments, result status, relevant returned content and artifact references.
- Actual independent-agent dispatches and PAL calls/results, with the filenames/content hashes of any file-based payload. If the versioned receipt/use fallback is selected, include the linked reviewer read/receipt evidence and mark unavailable prompt fields explicitly.
- Initial/final snapshots or diffs of the task/report files needed to grade completion and durable follow-up.
- The final user-facing report.

Do not include private model reasoning or the complete conversation. Record relevant explicit user decisions as attributed input events. Tools remain Read-only; in workflow mode the grader may open only manifest-listed sealed evidence and its own grading instructions, never the live fixture, live skill checkout or actor workspace. The controller keeps rubric/oracle files outside the actor workspace and never supplies their contents or paths. Where the runtime supports a filesystem allowlist, expose only subject and instruction inputs. Any actor read of grading material invalidates the run.

Preserve each actor's event order and parent-child dispatch/completion edges. Do not fabricate a single total order between concurrent reviewers. A successful file read is evidence of returned instruction bytes; a requested path or final "I loaded it" statement alone is not.

| Assertion class | Authoritative evidence |
| --- | --- |
| Instructions before source/edit | Completed instruction-read events, bounded-routing events and first subject/read/write event for the same actor; check the applicable routing exception. |
| Handoff parity and historical source | Revision 1 requires actual dispatch arguments plus referenced immutable files and provenance. Only after the [versioned fallback](#codex-handoff-capture-resolution) is selected may linked independent reviewer receipt/use evidence establish the narrower behavioral assertion; exact prompt parity remains unverified. |
| Stale-handoff refresh | Initial stale artifact, subsequent baseline/source evidence and updated dispatch/report. |
| Completion, scope and durable follow-up | Resulting tasks/doc snapshots and explicit requirement/decision input, not a final "done" claim. |
| Findings and report clarity | Final report against the expected supported trigger, consequence and uncertainty; do not re-infer from a live fixture. |

Observed contrary behavior is FAIL. Evidence missing or truncated such that the assertion cannot be established is PARTIAL with the missing event/artifact named. Neither passes acceptance. Treat a missing assertion or omitted required action visible in a complete trace as FAIL. The grader must cite event IDs or artifact locations rather than an unsupported claim from the actor.

Add grader calibration fixtures under review-code/evals/_harness/grading-fixtures/: one with an early edit followed by a falsely reassuring final report (FAIL), one lacking read events (PARTIAL), and one correctly ordered and complete run (PASS). Keep these controller/grader fixtures outside every actor test-files tree. Re-run representative legacy component grading to ensure the mode extension changes no legacy input requirement.

If the receipt/use fallback is activated, extend calibration before using it: a correct finding or parent handoff claim without linked reviewer receipt evidence cannot pass; a complete linked receipt/use trace can satisfy only the revised behavioral assertion. Keep exact prompt content marked unverified. Task 8 may proceed before gate 2B closes; any later rubric selection requires the corresponding calibration and regrading before Task 12 acceptance.

## R8: controlled report-phase replay

Use a bounded phase replay rather than inventing an MCP interception API. The controller supplies an explicit isolated-review checkpoint immediately before annotation/reporting: original scope, a fixed substantiated independent-agent result, and a synthetic PAL result file with provenance marked as test data. The actor loads the selected review instructions and resumes at that checkpoint with the normal instruction to present the review. This is a component evaluation of report handling, not an end-to-end skill or transport run.

Run two variants with the same local reviewer evidence:

- A PAL result shaped like a successful completed review, claiming no findings/broad approval while recording zero embedded/read source.
- A PAL failure result showing the external path unavailable.

The actor must retain the independent finding, disclose the external coverage/failure limit, avoid claiming corroboration and withhold any unsupported release-safe conclusion. Do not add those expected answers to the checkpoint prompt. Record the substitution in the controller manifest and grader evidence.

A real PAL smoke run remains separate: execute ordinary isolated review, record actual calls and source-coverage evidence, and report unavailable integration honestly. Emptying a live file manifest is not the selected test mechanism because the tool may reject it instead of producing the successful-but-underfed response under test.

## Matrix and evidence retention

R1–R7 and both R9 variants use actual standard and isolated invocation. R8 uses the two report-phase replays above. I1/I4 use plan mode; I2/I3 use standalone. Full implementation runs wait until isolated consumers and the producer are implemented. No snapshot substitution may supply a finished candidate consumer to an earlier task while claiming that earlier task's actual integration passed.

Keep legacy profile-routing and implementation pre-write controls. Add verdict checks to R3/R7, historical-source coverage to R3, and spec-integrity checks to I4. Record any automatic refactor recommendation in R5/R6/R9 so unwarranted complexity changes fail their negative assertions.

Store run contracts, results and sanitized traces under verification/ during implementation. A result states case/mode/repetition, source revisions, actual models, PASS/FAIL/PARTIAL/unrun, important false positives, coverage limits and artifact links. Comparisons are descriptive and mode-specific; two runs are not a benchmark of the model family. Unrun or failed required cases stay open with an owner, reason and next action.

These instructions are a concrete execution plan. Creating them does not constitute a launch probe, grader calibration, historical-source handoff test or behavioral acceptance run.
