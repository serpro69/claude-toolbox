# Implement functional and operational review

> Design: [design.md](design.md)
> Evaluation: [evaluation.md](evaluation.md)
> Tasks: [tasks.md](tasks.md)
> Review disposition: [consolidated assessment](reviews/design-review-consolidation.md)
> Status: Tasks 1–11 complete; candidate comparisons and final verification pending
> Revised: 2026-10-10; Task 2 gate 2B closed under the selected receipt/use contract

## Starting points

Canonical changes belong under klaude-plugin/. Current entry points are review-code/SKILL.md, review-process.md and review-isolated.md; agents/code-reviewer.md; implement/SKILL.md, plan-mode.md and standalone-mode.md. Shared review-scope-protocol.md also serves /kk:review-spec; pal-codereview-invocation.md also serves /kk:review-design. Preserve those consumers.

The immutable actor baseline is c2d28c9e (v0.23.0), resolved to a full commit when runs are prepared. Task 2 gate 2A preserves the final seed fixtures, frozen inputs and 16 baseline captures from before operative changes. Gate 2B adds four fresh Codex baselines against that same preserved actor revision under the selected revision-2 contract. The installed normal cache and an intermediate Task 4 working tree are not valid substitutes. [Evaluation binding](evaluation.md#bind-the-actual-instructions) specifies entry-point, runtime-root and agent loading.

## Delivery and verification rules

Each operative slice leaves its invocation usable and includes regenerated kodex-plugin/ and .codex/agents/ output from make generate-kodex. Do not hand-edit generated files. For freshness, compare a second generation with the first generated snapshot or check unstaged drift after staging intended generated changes; expected differences against HEAD are not staleness.

Run the plugin/codex structure suites and make plugin-graph after relevant canonical changes. Behavioral evidence comes from actual invocations and sealed traces, not string-presence checks. The new word budgets and symlink assertions guard instruction packaging only.

Use source-relative links and local shared symlinks. Distributed instructions explain their own rules and never link back to toolbox design documents. Preserve unrelated work and intentionally broken eval/template links.

## Baseline preparation

Task 1 establishes the revision-bound launch probes and run contract. It builds filtered actor bundles, scans bundles/cache copies for evaluator material, and proves per-run Capy/fixture isolation before any measured run. Operative files retain their original bytes; normal plugin distribution is unchanged. Task 2 owns the final seed fixtures R1/R3/I1/I2. It creates their complete eval.json, paired snapshot layout where applicable, and separate oracle directories before capturing standard, isolated, plan and standalone runs. The source/fixture identity and provider-specific launch probes are defined in [evaluation.md](evaluation.md#comparison-identity-and-acceptance).

The user-approved [2026-10-09 amendment](verification/run-contract-2026-10-09.md) separates implementation readiness from capture completion. Both gates are now done. The [gate 2B completion record](verification/task2b/README.md) retains four new Codex captures, independent grades and the revised evidence contract. Task 12 is next; observed baseline failures are data, not candidate passes.

The implementing agent completed [the resolution procedure](evaluation.md#codex-handoff-capture-resolution): no viable supported plaintext alternative was found, so revision 2 selected observable reviewer receipt/use before measurement. The fallback narrows the claim about prompt content; it retains both reviewers, all required behavior and the two-run candidate threshold. [The run contract](verification/task2b/run-contract.md) records the selected path, assertion mapping and configuration. Future comparisons must match that declaration or recapture affected pairs under a new one.

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

Task 13 updates README.md and docs/user-guide/skills.md through /kk:document, and docs/contributing/testing.md for staging and grading. Then:

- Run /kk:test with every test/test-*.sh suite, including staging.
- Run make generate-kodex and a second-generation freshness check.
- Run make plugin-graph and go test ./....
- Reconcile all behavioral assertions and existing routing/pre-write controls with the run contract.
- Verify /kk:review-spec task-scope and /kk:review-design PAL input compatibility.
- Run /kk:review-code with the actual detected profiles and /kk:review-spec against this complete design package.
- Resolve findings or record permitted follow-up; do not mark required unrun/failed acceptance items complete.

This design-revision task changes documentation only. Launch probes, grader changes, ADR/AGENTS amendments and operative skill changes above remain explicitly planned work.
