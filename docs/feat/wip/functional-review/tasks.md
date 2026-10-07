# Tasks: Functional and operational review

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Issue: [#166](https://github.com/serpro69/claude-toolbox/issues/166)
> Status: pending
> Created: 2026-10-07
> Not Doing: new review skill, whole-system audits, mandatory production access, deployments, generic release engine, new models/dependencies, profile redesign
> Delivery: preserve existing invocations and shared consumers; regenerate Codex artifacts with every operative slice.

The problem, scope and shared-context direction are approved. Detailed design review and implementation remain pending. Size excludes mechanical symlinks, generated output and fixture copies. Parallel markers identify compatible work; they do not authorize concurrent edits or delegation. Coordinate generator execution if slices run concurrently.

## Task 1: Standard review reasons about changed behavior

- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Standard review slice](implementation.md#standard-review-slice)

### Subtasks

- [ ] 1.1 Define the R1 minimal synthetic baseline/candidate fixture and capture the current standard-review outcome before changing instructions → verify: unchanged callers are available, expected answers are withheld, and the baseline result is recorded.
- [ ] 1.2 Add _shared/change-context.md and review-code/functional-review.md; add the review-code/shared-change-context.md symlink → verify: an arbitrary diff without a spec can supply context and all new instruction links resolve.
- [ ] 1.3 Update review-code/SKILL.md and review-process.md to load common methodology, resolve all conditional instructions before full analysis, trace behavior and report coverage → verify: R1 is found through a normal review prompt, with a concrete path and consequence.
- [ ] 1.4 Update _shared/review-scope-protocol.md to preserve responsibility for current breakage while excluding future missing implementation → verify: contrasting incompatible and clean partial-feature examples get different conclusions; /kk:review-spec still accepts its existing payload.
- [ ] 1.5 Regenerate Codex output, run structure/graph checks and record the candidate dry-run → verify: canonical/generated parity and instruction-before-analysis order; no unconditional production claim.

## Task 2: Independent reviewers receive and verify the same context

- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** Task 3
- **Docs:** [Isolated review slice](implementation.md#isolated-review-slice)

### Subtasks

- [ ] 2.1 Capture the existing isolated outcome and request payload for the minimal R3 consumer/provider scenario before editing → verify: evidence distinguishes orchestration from a directly prompted agent test.
- [ ] 2.2 Update review-code/review-isolated.md to load instructions before evidence, construct context and select files by affected behavior → verify: the unchanged provider/consumer contract reaches both reviewers.
- [ ] 2.3 Update agents/code-reviewer.md to load common methodology and independently check behavior, compatibility and coverage → verify: R3 is reported despite pending work; evidence supplied by the author is attributed.
- [ ] 2.4 Update the code-review branch of _shared/pal-codereview-invocation.md and commands/review-code/isolated.md → verify: missing spec never means quality-only review; /kk:review-design retains its document-only invocation.
- [ ] 2.5 Add bounded coverage conclusions to isolated reporting and exercise a degraded external result → verify: useful findings survive without converting incomplete external coverage into approval.
- [ ] 2.6 Regenerate Codex output, run structure/graph checks and repeat the isolated scenario → verify: actual orchestration and both payloads satisfy the contract; source-only reviewers do not claim test execution.

## Task 3: Implementation establishes constraints before editing

- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** Task 2
- **Docs:** [Implementation slice](implementation.md#implementation-slice)

### Subtasks

- [ ] 3.1 Capture existing plan/standalone preparation and handoff on minimal I1/I2 fixtures before editing → verify: the run records the first edit and context available at review.
- [ ] 3.2 Add implement/shared-change-context.md and integrate it into implement/SKILL.md → verify: both modes load shared context and applicable profiles before implementation edits.
- [ ] 3.3 Reconcile plan-mode.md/standalone-mode.md with the shared core; move detailed standalone investigation after the instruction gate → verify: existing pre-write-order evals pass and source discovery is not duplicated.
- [ ] 3.4 Establish intent, invariants, delivery constraints and meaningful verification before editing; persist enduring plan constraints in existing task documents → verify: I1 detects its incompatible approach and I2 remains usable without creating a full feature plan.
- [ ] 3.5 Refresh context for independent review, qualify completion/release claims and record unresolved work durably → verify: I4 cannot mark a violated hard requirement done or trust a stale baseline.
- [ ] 3.6 Regenerate Codex output and verify both modes plus I3's proportionality control → verify: no irrelevant production gate or new routine approval ceremony.

## Task 4: Evaluate complete review workflows on real regressions

- **Status:** pending
- **Depends on:** Task 2
- **Size:** M
- **Can run in parallel with:** Task 5
- **Docs:** [Evaluation staging and execution](implementation.md#evaluation-staging-and-execution)

### Subtasks

- [ ] 4.1 Extend review-code/evals/_harness/setup.sh for paired before/after snapshots while preserving legacy fixture behavior → verify: a real staged diff retains unchanged context and supports additions/modifications/deletions without staging wrappers or answers.
- [ ] 4.2 Add test/test-review-eval-staging.sh using existing helpers → verify: offline tests cover hidden files, malformed snapshots, escaping links/.git, and refusal to overwrite existing destinations.
- [ ] 4.3 Author self-contained R1–R9 eval directories, with separate R9 variants, noncolliding IDs, natural prompts, explicit file lists and grader-only oracles → verify: positive and negative controls are grounded in synthetic evidence; no private project content or assertion leakage.
- [ ] 4.4 Update HARNESS.md to distinguish component tests from actual standard/isolated skill invocation and shared-consumer checks → verify: full runs exercise context gathering rather than receiving preassembled answers.
- [ ] 4.5 Run the review matrix and record baseline/candidate comparisons, payload parity and R8 degradation handling → verify: all required assertions pass; unrun cases remain explicit gates and real PAL coverage is not inferred from a stub.
- [ ] 4.6 Regenerate fixture/document output and run structure/graph checks → verify: intentionally partial fixtures remain exempt and no genuine new broken links/orphans appear.

## Task 5: Evaluate implementation preparation and completion

- **Status:** pending
- **Depends on:** Task 3
- **Size:** M
- **Can run in parallel with:** Task 4
- **Docs:** [Workflow coverage](implementation.md#workflow-coverage)

### Subtasks

- [ ] 5.1 Author I1–I4 eval directories under implement/evals/ with real plan/standalone fixtures and grader-only expectations → verify: they test pre-edit reasoning, stale handoffs, completion constraints and proportionality without hinting at conclusions.
- [ ] 5.2 Add implement/evals/README.md with isolated staging, full invocation, trace collection and independent grading instructions → verify: fixtures are outside any SKILL.md ancestor and no oracle/assertion reaches the acting session.
- [ ] 5.3 Run I1/I4 in plan mode and I2/I3 standalone, alongside existing profile/pre-write regressions → verify: required assertions pass and no new trivial-change deployment or permission gate appears.
- [ ] 5.4 Record results and unresolved actions under verification/, regenerate output and run structure/graph checks → verify: every result names revision/mode/model and every failure or unavailable run has a next action.

## Task 6: Document and verify the complete feature

- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Documentation and final verification](implementation.md#documentation-and-final-verification)

### Subtasks

- [ ] 6.1 Update README.md, docs/user-guide/skills.md and docs/contributing/testing.md via /kk:document → verify: users understand ordinary functional review and evidence-qualified readiness; contributors can stage before/after evals.
- [ ] 6.2 Run /kk:test with all test/test-*.sh suites, make plugin-graph and go test ./... → verify: structural/plumbing checks pass, with environment failures explicitly distinguished from product failures.
- [ ] 6.3 Run make generate-kodex and verify a second generation introduces no drift → verify: kodex-plugin/ and .codex/agents/ match canonical instructions.
- [ ] 6.4 Check all behavioral results and shared consumers → verify: R1–R9, I1–I4 and existing controls pass in their declared modes; /kk:review-spec and /kk:review-design retain their contracts.
- [ ] 6.5 Run /kk:review-code with detected profiles and /kk:review-spec against this design/implementation/tasks set → verify: findings are resolved or durably assigned, and no required acceptance item is silently deferred.
- [ ] 6.6 Reconcile task status and verification limits before declaring completion → verify: all required work is done; no unrun gate, violated delivery constraint or unreviewed scope change is represented as complete.

## Dependency Graph

~~~
Task 1 ─┬─> Task 2 ─> Task 4 ─┐
        └─> Task 3 ─> Task 5 ─┴─> Task 6
~~~

## Design-stage checks

- Detailed /kk:review-design review is pending; no independent review is claimed.
- No canonical skill, generated plugin, application code or external issue has been changed by this design task.
- Behavioral evaluations and implementation checks above belong to implementation; document creation does not count as passing them.
