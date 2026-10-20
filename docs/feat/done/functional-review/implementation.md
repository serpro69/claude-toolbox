# Implement functional and operational review

> Design: [design.md](design.md)
> Evaluation: [evaluation.md](evaluation.md)
> Tasks: [tasks.md](tasks.md)
> Review disposition: [consolidated assessment](reviews/design-review-consolidation.md)
> Status: done; archive/cleanup verified, draft promotion separate
> Revised: 2026-10-20; Tasks 1–13 complete
> Next-session handoff: [follow-up.md](follow-up.md)

## Starting points

The [current acceptance reassessment](acceptance-reassessment.md) supersedes the
blanket thresholds and old open-gate statements in the historical slices below.
Task 12.25's [completed assessment](implementation-verification-assessment.md)
closes Task 12 with a documented execution/recovery limitation. No additional
skill patch or actor batch is selected. Task 13 finalization is complete;
[the summary](verification-summary.md) records checks/reviews and
[the archive handoff](release-archive-handoff.md) records completed retention,
draft upload and maintainer cleanup. Release promotion remains separate.
Historical I2 verification remains incomplete and no autonomous-recovery guarantee is made.

Canonical changes belong under klaude-plugin/. Current entry points are review-code/SKILL.md, review-process.md and review-isolated.md; agents/code-reviewer.md; implement/SKILL.md, plan-mode.md and standalone-mode.md. Shared review-scope-protocol.md also serves /kk:review-spec; pal-codereview-invocation.md also serves /kk:review-design. Preserve those consumers.

The historical pre-feature actor baseline is c2d28c9e (v0.23.0); preserve its
captures and identities. Future targeted comparisons use an immutable immediate
predecessor under the [current policy](evaluation.md#comparison-identity-and-acceptance).
An installed normal cache or mutable working tree is not a substitute for a
declared source revision. [Evaluation binding](evaluation.md#bind-the-actual-instructions)
specifies entry-point, runtime-root and agent loading.

## Delivery and verification rules

Each operative slice leaves its invocation usable and includes regenerated kodex-plugin/ and .codex/agents/ output from make generate-kodex. Do not hand-edit generated files. For freshness, compare a second generation with the first generated snapshot or check unstaged drift after staging intended generated changes; expected differences against HEAD are not staleness.

Run the plugin/codex structure suites and make plugin-graph after relevant canonical changes. Behavioral evidence comes from actual invocations and sealed traces, not string-presence checks. The new word budgets and symlink assertions guard instruction packaging only.

Use source-relative links and local shared symlinks. Distributed instructions explain their own rules and never link back to toolbox design documents. Preserve unrelated work and intentionally broken eval/template links.

## Baseline preparation

Task 1 establishes the revision-bound launch probes and run contract. It builds filtered actor bundles, scans bundles/cache copies for evaluator material, and proves per-run Capy/fixture isolation before any measured run. Operative files retain their original bytes; normal plugin distribution is unchanged. Task 2 owns the final seed fixtures R1/R3/I1/I2. It creates their complete eval.json, paired snapshot layout where applicable, and separate oracle directories before capturing standard, isolated, plan and standalone runs. The source/fixture identity and provider-specific launch probes are defined in [evaluation.md](evaluation.md#comparison-identity-and-acceptance).

The user-approved [2026-10-09 amendment](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/run-contract-2026-10-09.md") separates implementation readiness from capture completion. Both gates are now done. The [gate 2B completion record](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task2b/README.md") retains four new Codex captures, independent grades and the revised evidence contract. Task 12 is next; observed baseline failures are data, not candidate passes.

The implementing agent completed [the resolution procedure](evaluation.md#codex-handoff-capture-resolution): no viable supported plaintext alternative was found, so revision 2 selected observable reviewer receipt/use before measurement. The fallback narrows the claim about prompt content; it retains both reviewers, all required behavior and the two-run candidate threshold. [The run contract](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task2b/run-contract.md") records the selected path, assertion mapping and configuration. Future comparisons must match that declaration or recapture affected pairs under a new one.

Capture raw execution evidence; the workflow grader introduced later grades the preserved package. Preserve the original rubric, freeze and sealed records. Pin any successor rubric and the concrete grader implementation before grading either side. A rubric change requires regrading both sides, and recapturing both if saved evidence is insufficient. A runtime/model/tool-policy change requires a revised run contract and fresh affected baseline/candidate comparisons under the same configuration; developing the candidate does not change the identity of the preserved baseline.

Later fixture tasks extend the same directories and author only the remaining cases. Use the manual staging contract until the paired-snapshot helper exists, creating a fresh workspace and knowledge state for every run. Baseline and candidate must use identical fixture revisions and initial knowledge seeds; never relabel an intermediate candidate run as the unchanged baseline. Record the intentional unavailable-vault policy separately from knowledge search/index availability.

## Routing-convention slice

Task 3 updates docs/adr/0004-skill-workflow-ordering.md and AGENTS.md before changing workflow order. Explain that bounded predicate routing is the sole early-content exception after basic process instructions load: approximately 16 KiB per candidate file, only declared predicates, no behavioral findings or edits. If a conditional is undecidable within that bound, load it conservatively.

Preserve the rest of the instruction-before-action invariant. Verify the ADR and AGENTS.md agree and distinguish routing from full source investigation. This resolves existing contradictory wording without retroactively claiming that the deferred standard-review sequence already obeyed the proposed procedure.

## Standard review slice

Task 4 targets review-code/SKILL.md, review-process.md, new functional-review.md, new _shared/change-context.md and _shared/review-scope-protocol.md. Add review-code/shared-change-context.md pointing to ../_shared/change-context.md.

1. Define the shared record, provenance, historical-evidence responsibility and verdict mapping → verify: a standalone diff works without a formal spec or live production access.
2. Add the common functional method within the 1,200-word ceiling; keep shared context within 800 words → verify: complete-file whitespace word counts and normative coverage both pass.
3. Integrate method loading, bounded routing, affected-path reasoning and coverage into standard review → verify: R1 is found through an ordinary prompt and tool events show methodology before investigation.
4. Clarify current incompatibility versus pending features in the shared scope protocol → verify: R3 and R5 produce different outcomes without changing /kk:review-spec's payload requirements.
5. Add test/test-plugin-structure.sh checks for the shared source and current review-code symlink, including exact relative target and successful resolution → verify: a broken or regular-file replacement is caught; add the implement consumer only when Task 6 creates it.

Retain SOLID/security/profile coverage and existing finding labels. Broaden the title/overview and, if needed, the trigger-first description; verify current published description limits before changing frontmatter. Apply the design's explicit compatibility/verdict mapping; a missing deployment baseline is neither a fictitious defect nor grounds to certify a required unknown.

## Isolated review slice

Task 5 targets review-isolated.md, agents/code-reviewer.md, _shared/pal-codereview-invocation.md and commands/review-code/isolated.md. It completes isolated consumers before Task 6 integrates the producer.

1. Load shared methodology and resolved profiles before full diff analysis, then construct change context → verify: actual isolated invocation obeys the ordering gate.
2. Materialize decisive historical blobs/excerpts outside the reviewed worktree with repository/revision/path/hash/line provenance → verify: both agent and PAL payloads contain R3's released-provider source even though it is absent from candidate files and diff hunks.
3. Define evidence requests in the reviewer output and a parent-mediated resume/reinvoke path; send equivalent relevant additions through PAL continuation → verify: available local history is supplied; a truly missing baseline remains Unknown in R7 without expanded reviewer permissions.
4. Update the agent's instruction-loading and reporting contract and remove quality-only fallbacks → verify: it challenges author claims and does not claim test execution from its source-only access.
5. Introduce explicit code-review/document-review sections in the currently flat PAL protocol, then add behavior-selected and historical files to the code-review section → verify: /kk:review-design still accepts document-only inputs.
6. Preserve native external output, annotation and failure semantics while applying bounded coverage/verdict rules → verify: R8 replay preserves useful local findings without unsupported corroboration or release approval.

Treat the current surrounding-file cap as an initial selection budget. Follow identified contract questions beyond it through focused additional evidence or report the specific uncovered boundary. Do not ship a new unbounded whole-repository scan.

## Implementation slice

Task 6 depends on completed standard and isolated consumers. Targets: implement/SKILL.md, plan-mode.md, standalone-mode.md and its mechanical shared-change-context.md symlink.

1. Load shared context and profile guidance before detailed source investigation and implementation edits; reconcile standalone entry with the core → verify: existing pre-write-order controls and I2 pass.
2. Establish intent, required preserved behavior and applicable delivery constraints before editing → verify: I1 identifies the incompatible approach before making dependent edits; I3 stays proportionate.
3. Store observations in the task's labeled Execution context subsection, with status/source/date and proposed versus accepted decisions → verify: I4 cannot silently change design.md, implementation.md or acceptance criteria to match its code.
4. Refresh evidence after fixes/resume and pass actual scope/baselines to both existing review paths → verify: integrated handoff is tested against the completed Task 5 consumers.
5. Separate code completion from release/activation conditions and durably record allowed follow-up → verify: a violated hard requirement remains open; a legitimate external prerequisite remains explicitly conditional.
6. Extend the structure-test shared-file assertions to implement's new symlink → verify: both exact targets/resolution and both instruction budgets pass after regeneration.

Requirement changes still follow explicit user authorization. This feature does not impose independent deployment or feature flags on every repository.

## Evaluation staging slice

Task 7 extends review-code/evals/_harness/setup.sh and adds test/test-review-eval-staging.sh. Follow [fixture lifecycle and staging](evaluation.md#fixture-lifecycle-and-staging), including legacy flat inputs, before/after snapshots, R3's history manifest and tagged released snapshot.

Verify offline: additions, modifications, deletions, unchanged files, hidden files, historical blobs/tags, missing halves, escaping links, embedded .git, invalid history refs and refusal to overwrite destinations. Keep staging wrappers/oracles out of the actor workspace. Preserve the seed directories created in Task 2.

## Workflow-grading slice

Task 8 extends agents/eval-grader.md with explicit workflow mode while preserving the default component contract and Read-only access. Update review-code/evals/_harness/HARNESS.md and add implement/evals/README.md to carry the [execution-evidence contract](evaluation.md#execution-evidence-contract).

The controller assembles ordered tool events, real dispatches and resulting-file snapshots with hashes. The grader may read only manifest-listed evidence, its instructions and supplied rubric. Add calibration records under the harness's grading-fixtures directory: early edit plus false final claim fails, missing events are partial, and a complete ordered trace passes. Legacy component grading remains unchanged. Task 8 can implement and calibrate the grader while gate 2B is open; if the fallback is selected later, update its evidence mapping and regrade affected retained traces before acceptance.

R8 uses the concrete report-phase replay defined in [evaluation.md](evaluation.md#r8-controlled-report-phase-replay). No MCP proxy, tool interception API or new server dependency is introduced. A real PAL smoke run has separate evidence and cannot be replaced by the replay.

## Fixture-authoring slices

Tasks 9–11 author bounded groups in the final eval directories:

- Task 9: R2 retry/lifecycle, R4 persisted-data compatibility and both R9 intent/complexity variants.
- Task 10: R5 clean partial feature, R6 inherited defect, R7 absent evidence, and R8's two report-phase variants. Reuse R1/R3.
- Task 11: I3 proportionality and I4 resume/completion/spec-integrity; reuse I1/I2.

Each scenario has a natural prompt, complete declared file list, specific assertions and grader-only outcomes. All new assertions are required. New numeric IDs exceed existing maxima; use composite result keys to tolerate the documented pre-existing implement ID collision without unrelated renumbering.

Fixture authoring does not count as a matrix run. Do not include private source or records, hint at the hidden failure in the prompt, or stage expected answers.

## Matrix execution

Task 12 waits for Task 2 gate 2B, producer, isolated consumers, staging, grading and all scenarios. Run the declared primary-provider matrix and secondary representative coverage with the predeclared two-run threshold and selected versioned evidence contract. Preserve raw traces and per-assertion results, including failed attempts and unknown tool coverage. If the receipt/use fallback was selected, report that narrower observation and leave exact submitted prompt content explicitly unverified.

Review R3's historical-source handoff, R3/R7's verdict mapping, I4's resulting document state, and the grader calibration controls explicitly. Compare every candidate against the immutable actor baseline using the same fixture and grading revisions. An unavailable runtime or source capture yields an unrun gate with an owner/next action; it does not waive acceptance.

The user subsequently expanded coverage to both providers' complete applicable
matrix. [All 192 sessions and grades](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/README.md") are
complete. Required acceptance remains unmet; preserve PAL deferral and the
separate legacy/final gates. The bounded entry-path comparison below is complete;
no automatic full rerun follows.

## Documentation and final verification

### Task 12 focused rework checkpoint

The user approved focused rework after candidate 4. Execute these bounded slices
before expanding the matrix:

1. Add successor capture helpers under `verification/task12/rework/`, preserving
   historical controller bytes. Prepare the whole batch before launch and run
   captures serially in the owning process. Record SIGINT/SIGTERM without raising
   during acquisition; stop the owned Linux process group before reaping its
   leader, then seal evidence. Ignore repeated termination during cleanup.
   Check the sealed actor exit status and missing completion explicitly.
   Make probe evidence finalization independent of teardown success while
   preserving the primary failure. → Verify: offline subprocess tests for
   preparation failure, runtime failure, interruption and teardown failure; no
   model or live PAL calls in these tests. Independent review precedes capture.
2. Add a plugin-local instruction-packet helper and integrate it into standard
   review preparation. Preserve original instruction bytes, source paths,
   bounded reads and the direct-read fallback; include all known detection rules
   and validate selected profile paths against their indexes. Resolve profile
   predicates in the existing procedure, not in Python. Remove conflicting
   speculative-suggestion cues and use the contract-driven scenario record.
   → Verify: offline packet completeness/path-boundary/truncation controls,
   canonical/generated parity, source review and a separate binding probe.
3. Freeze candidate 5 and a diagnostic declaration for R1/R3/R5 standard, twice
   per side with fresh state. Report failure classes separately while preserving
   the pinned assertions/rubric and all old results. Runtime/capture changes get
   fresh matching baseline runs. → Verify: independently grade all twelve sealed
   captures; expand only if every candidate assertion passes in both runs.

Optional `/kk:clarify-docs` can refine the amended design, implementation and
task documents; `/kk:review-design functional-review` remains available for an
independent design assessment. These optional passes do not delay the already
authorized rework.

### Proposed ordering feasibility slice — conditional

After candidate 6, the user approved scoping a separate ordering fix. The
[ordering proposal](ordering.md) is the source of truth for this prospective
slice. Preserve the candidate-6 source and sealed results. The original scope
revision changed documents only; it did not implement or launch a probe, hook
or candidate.

If selected after Task 12.11, **12.10** is a risk-first experiment
under `verification/task12/ordering-probe/`, using disposable plugin copies.
Its four steps are capability declaration, offline receipt/state controls,
at most two top-level runtime sessions per provider, and independent evidence
review with a GO / NO-GO disposition. Each step's verification is specified in
[the bounded slice](ordering.md#bounded-feasibility-slice). Declare any actual
runtime/tool-policy changes before launch and preserve existing evidence.

GO supports designing a later production integration; it is not R5 acceptance.
NO-GO records the missing capability and ends this experiment. Neither outcome
changes the pinned assertions or authorizes a generic policy engine, runtime
upgrade, provider substitution or matrix expansion. A later integrated candidate
requires fresh matching comparisons as described in
[conditional validation](ordering.md#conditional-integration-and-validation).

### Severity and instruction-cost disposition

The [dated assessment](follow-up.md#assessment--2026-10-11) and
[observation ledger](assessment-observations.md) account for every candidate
FAIL/PARTIAL, separating behavioral impact, report omissions, missing evidence
and PAL deferral. Existing instruction burden is part of each disposition;
deferred requirements remain open.

Task 12.12's
[bounded plan](tasks.md#task-1212-resolve-isolated-review-instructions-at-entry)
replaces the isolated command's ambiguous instruction location with explicit
plugin-root paths, adding two words. [All twelve declared Claude comparisons](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/entry-path-no-pal/README.md")
are captured and graded; both repetitions meet the R3 non-PAL conditions and
R5/R9-recovery controls, supporting the keep decision. Common instructions and
generated Codex bytes are unchanged. An unexpected PAL connection in the initial
loading probe required a reviewed, separately frozen configuration that excludes
PAL from the actual launched MCP set. Both measured sides use that configuration;
fixtures, ordinary prompts, models, permission policy and assertions stay fixed.

Candidate totals remain 32 PASS / 8 FAIL / 0 PARTIAL; every required PAL omission
still fails its composite assertion. These observations neither close full feature
acceptance nor isolate the incremental causal effect from the preceding candidate.
Keep implementation acquisition, unsupported deployment claims and capture limits
separately assigned. Task 12.13 below records the rejected wording experiment;
Task 12.14 now prioritizes R7 evaluation validity under the same cost constraint. The earlier guard remains
deferred and may not address I4's later context-ordering violation.

### R7 conclusion consistency — Task 12.13

The user approved the bounded replacement approach on 2026-10-13. The experiment replaced existing
Supported, Unknown-verdict and final evidence-reconciliation wording in
`review-code/functional-review.md`; all standard/isolated consumers already load
this common method. It added no reporting section, checklist, workflow phase or
duplicated agent rule and preserved the intended treatment of known prerequisites,
scoped code approval and unrelated unknowns. The Codex distribution was regenerated.

The completed comparison used unchanged R7, R3 and R5 fixtures: both modes and
providers, two fresh repetitions per immutable baseline/candidate (48 sessions).
Runtime, filtered bundles, isolated state and capture contract were validated and
frozen prospectively. PAL remained excluded and its required omissions retain
FAIL. The fixed keep rule rejected the candidate if R7 still overclaimed or
R3/R5 regressed, with no automatic further iteration. Task 12.13 owns the evidence;
full-feature acceptance remains separate.

**Disposition: reject the candidate.** Both Claude standard R7 repetitions still
overclaim provider/deployment compatibility. The three operative replacements
and generated counterpart are reverted; the source archive and patch remain in
the [verification record](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/r7-conclusions/README.md"). R7 stays
unresolved and no successor wording or actor iteration is selected. Source checks
passing did not establish the required behavioral result.

### R7 evaluation validity — Task 12.14

The user requested a next-session handoff after questioning R7's simplified
whitespace fixture. Follow the [recorded redesign](follow-up.md#r7-evaluation-redesign--next-session):
establish a material compatibility dependency and a benign control, then write
meaning-based grading criteria and example reports before measuring agents.
Start with the existing `functional-missing-baseline` eval/oracle and Task 12.13
reports as evidence, not proof that another shared instruction is needed.

Keep operative skill instructions unchanged. Author successor fixtures and rubric
under separate identities; preserve historical results and explicitly document
any contract amendment. After review, a prospectively declared four-session
Claude standard diagnostic uses the unchanged current skill on both cases.
It is not the required baseline/candidate acceptance comparison. The
[completed four-session diagnostic](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/r7-validity/README.md")
records 23 PASS / 1 FAIL / 0 PARTIAL, with both target compatibility conclusions
passing twice and one retained report-trace omission. The disposition is no
further operative skill change for this R7 concern. Historical R7 and all broader
acceptance gates remain unchanged. Independent completion review approves closing
Task 12.14 as this bounded diagnostic.

Optional `/kk:clarify-docs` may refine the changed `follow-up.md`, `design.md`,
`implementation.md`, `evaluation.md` and `tasks.md`; then
`/kk:review-design functional-review` can assess the updated plan before operative
implementation. Task 13 remains dependent on Task 12's actual acceptance.

### R6 evaluation validity — Tasks 12.15 and 12.16

The completed [assessment](r6-assessment.md) separates inherited discovery,
reachability, correct scoped approval and missing advisory follow-up. The user
selected Task 12.16 to author the proposed material-exposure/dormant-control pair,
its criteria and pre-run examples, and obtain independent validity/source review.
Use separately identified evals 21/R6M and 22/R6D; preserve all original R6 files.

Both cases share a small reporting implementation whose detailed mean has a
visible consumer. R6M enables that mode by default while requiring empty-batch
success; R6D changes only the count label and leaves detailed mode disabled.
The [prospective rubric](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/r6-validity/rubric.md") makes dormant
discovery optional only in R6D, retains attribution and surfaced-advisory follow-up,
and separates final-report evidence from child discovery. This is the explicit
successor scope decision under the authoring request, not an old-grade amendment.

Verify complete snapshot manifests, intended diff boundaries, actual outcomes,
passing supplied tests with the intended coverage gap, and evaluator-free staging
through the existing helper. Generate Codex counterparts and run relevant
structure/staging/graph checks. Independent review must assess fixture validity
and criteria before measurement. The [authoring record](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/r6-validity/README.md")
retains checks and findings. This task ends at reviewed assets; a later bounded
diagnostic requires its own declaration. Operative instructions, historical
acceptance, PAL deferral, other investigations and Task 13 remain unchanged.

### R6 bounded diagnostic — Task 12.17

After authoring, the user authorized eight fresh standard reviews: R6M/R6D,
Claude/Codex, twice each, with unchanged operative instructions. The
[diagnostic declaration](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/r6-validity/diagnostic/run-contract.md")
pins its distinct runtime and evidence boundaries. Grader calibration, source
review, immutable freezing and both provider binding/state checks preceded
measurement. All eight captures are independently graded: **58 PASS / 10 FAIL /
0 PARTIAL**, with correct scoped verdicts in every run. Follow-up and reported
trace/reachability omissions remain failed. All four final dormant advisories
triggered the follow-up requirement; none received the required next action.

The [record](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/r6-validity/diagnostic/README.md") assigns bounded
advisory-closure investigation and defers added trace instructions pending value.
No operative patch or broader batch is selected. Original R6/R7 acceptance, PAL,
legacy actor controls, implementation-verification concerns and Task 13 remain
separate. Capture completion is not a full diagnostic or feature pass.

### Advisory-closure candidate — Task 12.18

The user selected the bounded advisory-closure investigation after Task 12.17.
The [assessment](advisory-closure.md) ties all four missing follow-ups to a possible
ambiguity between in-scope findings and separately reported inherited defects.
It does not claim that closure wording caused the omissions.

Replace only the standard and isolated closing branches: a surfaced substantiated
inherited defect receives a concrete separate follow-up when repair is outside
the task, without blocking an otherwise supported increment. Preserve clean
no-action approval, in-scope corrections, required evidence and authorization
limits. Regenerate Codex copies, verify packaging/parity and obtain independent
source review. [Source review](reviews/advisory-closure-review.md) and local checks
are complete; Task 12.18 completes candidate preparation only. The prospective
comparison, adoption and all existing acceptance gates remain separate.

### Advisory-closure freeze and declaration — Task 12.19

The user selected source/criteria preparation before measurement. The
[record](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/advisory-closure/README.md") retains candidate
`4b69421465131e2e9e497f200ec9ddbdb439ac83`, the immutable baseline, complete
source/filtered archives, evaluation/controller inputs and a 64-session matrix.
The [contract](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/advisory-closure/run-contract.md") defines bounded
KEEP / REJECT / INCONCLUSIVE outcomes separately from all original assertion grades
and full feature acceptance. Both independent reviews approve after clarifying
22.4's tolerated omission; archive recovery, source delta and final seal pass.

No operative change or model run occurs in this task. Execution needs a successor
adapter, its own reviewed dependency freeze, fresh grader/disposition calibration,
four binding probes, two state probes and passing preflight before measurement.
The source/criteria freeze remains immutable input; any revision gets a separately
identified successor. PAL, original acceptance and Task 13 retain their status.

### Advisory-closure adapter and calibration — Task 12.20

The user selected execution-adapter preparation and fresh calibration. The
[execution record](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/advisory-closure-execution/README.md")
preserves the reviewed adapter, checked archived dependencies, per-case rubric
routing, no-overwrite/serial-stop guards and exact frozen dispatch plans.
The preparation seal and operative candidate remain unchanged.

After source and calibration-validity review, the execution freeze preceded all
25 fresh independent grader calls. Every expected verdict/trigger matched:
69 assertions and 11 trigger observations. Returned FAIL/PARTIAL judgments are
the intended negative controls. Independent completion review approves with no
findings; tests and integrity checks remain parent-attributed execution evidence.

No actor, binding/state probe, PAL or registration action occurred. Four binding
probes, two state probes and a reviewed preflight remain the next unrun gates;
measured execution/adoption and broader acceptance are separate.

### Advisory-closure runtime preflight — Task 12.21

The user selected the four binding probes, two Capy state probes and independent
review. The [retained result](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/advisory-closure-execution/preflight-result.md")
supports instruction/model/role loading, state isolation, unchanged subjects and
owned cleanup, but does not establish the declared Claude child high effort.
Candidate frontmatter specifies xhigh; the parent high flag and model override
do not prove the child's effective effort under documented precedence.

Independent review returns COMMENT and readiness remains BLOCKED. Preserve every
capture and freeze; the implementing agent owns a reviewed successor launch-time
effort pin/receipt, its runtime/calibration identity and fresh affected Claude
bindings. No original requirement, historical grade, actor source or measured
comparison was changed. Task 12.21's PASS gate remains open.

The user selected the launcher correction. The [reviewed successor](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/advisory-closure-execution/high-effort-host/README.md")
now supplies/records high at the actual Claude launch boundary for both source
sides and binding/measured paths; actor bytes remain unchanged. Nine new and 26
predecessor tests pass. Calibration, Codex and state reuse preserves original
identities and has independent source approval. After a preserved sandbox-limited
startup failure, a separately frozen host request was rejected by automatic
approval review before launch over private-payload authorization to Claude/API.
Explicit approval of the two affected probes is now required; fresh receipts,
retention, independent evidence review and successful guard remain outstanding.
No measured execution, adoption or original-acceptance change follows.

The user subsequently explicitly approved both host/API bindings. The
[completed corrected probes](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/advisory-closure-execution/high-effort-host/preflight-result.md")
verify the high-effort launch mapping and both unchanged subjects. Baseline meets
the receipt inventory; candidate omits all eight bootstrap detection files and
expressly reports that omission. Keep 12.21.4 open. Reconcile the binding prompt's
stopping instruction with the required inventory and review any separately
identified successor before another affected capture. No further actor or
operative instruction change is selected; original acceptance remains unchanged.

Independent completion review confirms the loading failure and approves a
verification-only guard correction: the selected `guarded_successor.py` entry
recomputes pinned successful receipt evidence rather than trusting audit file
presence/hashes. Five regressions pass; its separate guard freeze preserves all
actual capture/runtime identities. The strict gate rejects the incomplete
candidate and the attestation stays BLOCKED. Use that guarded entry for later
preparation/measurement; the original frozen launcher remains historical.

The user selected that loading follow-up on 2026-10-18. The
[bootstrap successor](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/advisory-closure-execution/bootstrap-loading/preflight-result.md")
clarifies the probe-only stopping boundary while preserving source-specific
instruction requirements, measured prompts, runtime policy and strict receipt
recomputation. Independent source review approves after correcting historical
evidence drift checks; 48 local tests pass. The successor is separately frozen.
Automatic approval review rejected its baseline launch before process creation
over explicit payload/destination authorization. At that checkpoint no actor ran. The handoff
records the exact approval scope, then serial capture/audit, retention, independent
completion review and strict preflight verification. 12.21.4 remains open; old
failed captures, original acceptance and measured comparison stay unchanged.

The user then explicitly approved both transfers/probes. Both completed with
unchanged subjects and full required instruction receipts, including all eight
candidate detection files. Independent assessment found the auditor's blanket
rejection of two allowed instruction-filename Globs was a verifier defect. The
separately reviewed `bootstrap-loading/listing_guard.py` validates the narrow
listing scope and complete results while preserving every original receipt gate;
twelve tests pass and the original failure/captures remain untouched. Its verifier
freeze preserves the actual actor runtime identity. Independent final evidence
review approves; the sealed attestation passes the strict guard with exit 0.
Task 12.21.4 is complete. Later preparation/measurement must use that selected
entry point; the 64-session comparison, adoption and original acceptance are
still separate, uncompleted work.

### Advisory comparison execution — Task 12.22

After preflight passed, the user selected the 64-session comparison. All declared
inputs were prepared and each launch independently validated by the existing
adapter; no source/runtime/rubric change was needed. Automatic approval review
initially rejected launch before process creation. The user's explicit "yes" to
the concrete payload/destination request resolved that blocker. All 64 sessions
then completed successfully, without retries, and all 464 original assertion rows
were independently graded. Original returns and eight same-packet clarifications
are retained separately; the strict audit passes. Runtime retention preserves
480 configuration files and confirms removal of owned Codex entries for 32 jobs.

[The result report](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/advisory-closure-execution/bootstrap-loading/comparison-result.md")
records **REJECT** under the unchanged contract: an inaccurate evidence
claim and speculative refactor advice each fail a candidate decision check.
The initially graded truncation was traced to the grader's viewing tool and
corrected from existing sealed evidence. Seven of eight dormant final reports surface
the advisory and supply an action; the eighth leaves the target unexercised.
Independent completion review approves; Task 12.22 is complete. The next recommendation is to revert
only the closure candidate when selected, preserving its patch and evidence.
No rollback, new experiment or full feature acceptance follows automatically.

### Closure candidate rollback — Task 12.23

The user explicitly requested reverting the rejected closure candidate. Restore
only its frozen four-file patch: two canonical closing sections and their generated
Codex copies, matching source parent `11b2c6efb0638605bb6acd3eb184edb9abd10f56`.
The broader functional-review implementation remains in place. Preserve the
comparison's original evidence and completion seal, with its four historical
handoff targets archived before live tracking updates. The
[rollback record](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/advisory-closure-revert/README.md") retains
scope, passing verification, provenance and independent review APPROVE. Task 12.23
is complete. No actor rerun, new wording
experiment, PAL resumption or acceptance claim follows from this rollback.

### Verification-policy correction — Task 12.24

The user approved reassessing existing evidence and making the learning durable.
Record ADR 0010 and the repository guidance; share one self-contained policy
among design, test and design review, including isolated reviewers. Replace
blanket all-branches/all-tests guidance and separate grader observations from
adoption. Update current evaluation, design, task and handoff criteria so retired
gates actually stop blocking. Preserve all frozen evals/captures and the closure
rollback; reviewer simplification remains a separate decision.

Verify against the retained R6/R7 examples and a material-regression counterexample,
then check source consistency, symlinks, generated parity and plugin structure/graph.
Obtain independent review. This establishes integration, not improved actor
behavior; no live evaluation batch is needed for this policy correction.

### Task 13 finalization under the revised policy

Task 13 updates README.md and docs/user-guide/skills.md through /kk:document, and docs/contributing/testing.md for staging and grading. Then:

- Run /kk:test with every test/test-*.sh suite, including staging.
- Run make generate-kodex and a second-generation freshness check.
- Run make plugin-graph and go test ./....
- Reconcile material outcomes and evidence limits under the current policy. Select legacy controls only for affected behavior or a concrete unresolved risk; retired gates do not require new actor passes.
- Verify /kk:review-spec task-scope and /kk:review-design PAL input compatibility.
- Run /kk:review-code with the actual detected profiles and /kk:review-spec against this complete design package.
- Resolve findings or record permitted follow-up; do not mark required unrun/failed acceptance items complete.

[Task 13.7](tasks.md#137-evidence-retention-and-release-archive) combines authorized
AI-assisted local preparation with human cleanup and release housekeeping.
Keep the compact verification record, maintained
eval assets and reusable tooling in Git; archive the complete retained evidence
in the project's ignored `.local-archives/functional-review/` directory.
Verify local archive integrity and extracted members before the human removes
repository evidence and purges its history. Create the release and attach/verify
the assets afterward; a release/tag is not needed for the local archive.
The user's subsequent explicit request selected an existing draft release for
upload before cleanup. That upload and downloaded-asset/member verification are
now complete; the handoff records actual asset URLs. The subsequent maintainer
history cleanup and archive-reference repair are verified, completing the final
documentation closure. No draft publication was performed.
The user accepted unavailable historical temporary inputs on 2026-10-20: preserve
their original identities and disclose exact-replay limits without requiring
recovery. Include still-available inputs such as the known core source export.
Feature verification and this release follow-up have separate completion records;
Both are now complete, closing Task 13.

This handoff revision changes documentation only. Earlier completed slices and
sealed evidence retain their status; the selected and deferred follow-ups
and final verification are tracked in tasks.md.
