# Review preparation ordering: proposed follow-up

> Status: scoped proposal; no guard, runtime probe or new candidate implemented
> Authority: the user agreed to scope instruction ordering after candidate 6
> Parent: [design](design.md), [implementation](implementation.md), [Task 12](tasks.md#task-12-execute-and-assess-the-full-comparison-matrix)
> Evidence: [candidate-6 results](verification/task12/candidate6/results.md)
> Owner: implementing agent, Task 12

## Recommendation

Keep candidate 6's clean-review closure change. Investigate a review-scoped tool
guard in one bounded feasibility slice before committing to production hook
integration. Its job would be to reject premature source operations until the
same reviewer has received the required instruction content. The existing
packet helper remains a packager; it must not certify its own output as read.

This is a proposal to test a mechanism, not another candidate instruction patch
or approval to expand the behavioral matrix. The previous exclusion of
cross-provider hook enforcement remains in force for operative code until this
proposal is reviewed and implementation is authorized. No model, dependency,
fixture, assertion or threshold change is proposed.

## Observed problem

Candidate 6 standard R5 repetition 1 received the full diff at event 45 and
config/settings at event 61. Python checklist bodies arrived at events 97/99;
task requirements also arrived too early at events 86/88. Repetition 2 completed
its instruction reads before investigation. Both reviews passed the clean-closure
assertion. The remaining failure concerns the transition into investigation,
not instruction availability or the correctness of the final recommendation.

`prepare_instructions.py` currently creates bootstrap, profile-index and
checklist packets. It validates instruction paths and checklist membership, but
does not observe tool results or restrict other tools. Its manifest correctly
states that the gate is not established. More checkpoint wording would still
leave the same bypass available.

## Why feasibility comes first

Current official documentation describes pre-tool blocking and post-tool result
events in both runtimes. Claude documents subagent identity and skill-hook
lifetime extending beyond the invoking turn. [Claude hook reference](https://code.claude.com/docs/en/hooks#hooks-in-skills-and-agents)

Codex documents local-tool coverage, omissions, hook trust, nonblocking failure
modes and shell-session continuation that does not repeat the pre-tool event.
Its post-tool event normally carries model-facing output, but other hooks can
affect delivery. [Codex hook reference](https://learn.chatgpt.com/docs/hooks#tool-coverage),
[post-tool results](https://learn.chatgpt.com/docs/hooks#posttooluse)

These are current documentation claims, not verified capabilities of the
declared Claude 2.1.272 / Codex 0.162.1 evaluation runtimes. The Context7 version
catalog did not provide an exact Claude 2.1.272 entry. Installed-version probes
must settle support; no automatic upgrade or dependency change is implied.

The repository already has Bash pre-tool hooks, but no instruction-receipt
observer. Existing hook configuration does not establish native Read coverage,
ordinary skill activation, safe per-review lifetime, or cross-provider parity.
The generator also needs investigation before assuming plugin-hook distribution.

## Proposed contract

The supported claim would be **prevention of accidental early source operations
on verified tool paths while the review guard is active and healthy**. It is
not an OS sandbox, proof that the model understood the text, or a substitute for
the execution-evidence grader. Hook failures and uncovered tool paths preclude
a universal enforcement claim.

| Boundary | Required behavior |
| --- | --- |
| Activation | Observe ordinary registered review invocation before its first subject operation. Starting only when the model voluntarily calls the helper leaves a gap and is insufficient. Unrelated skills remain unaffected. |
| Identity | Key state by runtime, session, reviewer/agent, review invocation and instruction-bundle identity. A parent, sibling, earlier review or previous bundle cannot supply another reviewer's receipts. |
| Instruction inventory | Reuse the existing Known-profile rules, active indexes and load/skip decisions. Preserve all always-load entries and conservative loading of undecidable conditionals. Do not port semantic detection into a second Python implementation. |
| Receipts | Count successful, complete returned instruction content, linked to tool-call identity and original source hashes. A manifest, existing file, requested path, model acknowledgement or helper exit zero is insufficient. |
| Ready transition | Require the complete declared instruction set and prior completed receipts before permitting the first investigation request. A concurrently submitted source request cannot become valid merely because the last read happens to finish first. |
| Expiry | End the guard with that review. Restart for another review, changed bundle/scope, or resume/compaction unless the runtime can establish the required preserved context. Never leave an unrelated later turn locked. |
| Failure | Missing/malformed evidence cannot set ready. Handler errors, disabled/untrusted hooks and unobserved tools must remain explicit coverage failures, not silently reported enforcement. |

The guard can validate structural completeness and ordering of the declared set.
It cannot independently prove that a semantic profile non-match was correct.
The existing detection/routing assertions and independent grader retain that
responsibility. Hooks that replace or truncate a result must not leave a receipt
for content that the reviewer did not receive.

### Operations during preparation

Before ready, allow only instruction reads/packet generation, bounded metadata
selection and declared predicate routing. Full diffs, task requirements, source
investigation, tests, edits, arbitrary shell and source-reading MCP calls remain
closed. Existing permission policy still applies after ready; the guard adds
restrictions and never grants additional permission.

Use narrow structured helper operations for Git filename/status metadata and
bounded routing if native tool arguments cannot be classified reliably. A
metadata operation must return no hunks, execute no repository hooks/external
diff or pager, and accept no arbitrary shell. Routing remains limited to a named
declared predicate and approximately 16 KiB per candidate file. If that cannot
be safely represented, conservatively load the relevant instructions instead
of opening an unrestricted content-read exception.

Do not implement a general shell parser or allow commands because they begin
with `git diff --stat` or `cat`. Compound commands, redirections, interpreters,
pre-existing interactive processes and alternate read tools can bypass such a
rule. The probe must identify these paths and reject or explicitly exclude
unsupported configurations from the guarded-support claim.

Read-only reviewers must retain a direct-instruction-read path with equivalent
receipt tracking; they must not acquire shell access. Helper unavailability may
use the existing direct-read procedure, but it cannot be labelled guarded unless
the adapter actually observes and enforces that path.

## Alternatives and trade-offs

| Approach | Decision |
| --- | --- |
| Another prose/checkpoint revision | Do not choose as the next experiment: candidate 6 already distinguishes selection, task scope and checklist completion, yet early reads recur. |
| Load every profile into the entry point | Do not choose: discards selective loading, substantially expands context and still needs complete-delivery evidence. |
| Review-scoped guard plus independent event audit | Preferred feasibility target: acts at the observed failure boundary while retaining current review semantics. Activation, receipt fidelity and lifecycle support are unproven. |
| New isolated launcher or filesystem sandbox | Reserve for a separate proposal if hooks cannot cover the necessary paths. It changes invocation/tooling scope and is not a hidden fallback here. |
| Relax the ordering assertion | Rejected: this would amend the acceptance requirement rather than demonstrate the proposed fix. |

## Bounded feasibility slice

Plan controller-only work under `verification/task12/ordering-probe/`; keep it
out of distributed skills and actor evaluator inputs. Use a disposable copy of
the candidate-6 plugin, innocuous synthetic instruction/source markers, and
run-owned hook configuration. Preserve all historical controllers and captures.
No new evaluator answers enter a normal review prompt.

1. Record exact runtime/schema/tool support and a probe contract. Identify
   ordinary activation, actor identity, post-result bytes, concurrent-call order,
   hook failure behavior and review termination. → Verify: each required
   capability has an installed-version evidence target; unknowns are named.
2. Build the smallest controller-only state/adapter experiment. Use offline
   event sequences to reject missing, partial, failed, duplicate-as-completion,
   altered, wrong-actor and stale receipts; exercise concurrent source requests
   and review teardown. → Verify: negative cases stay closed, and a complete
   correctly ordered sequence opens only its own review.
3. Run at most **two fresh top-level sessions per provider**: one directed
   synthetic tool-boundary exercise and one ordinary registered-skill lifecycle
   probe. Child calls may be included to test actor separation. Pin session/model
   configuration before launch; do not repeat unsuccessful probes indefinitely.
   → Verify: retain actual requests, blocking responses, completed reads and
   matching model-visible results, plus the absence of the source marker before
   readiness. Also demonstrate a valid read after readiness and an unaffected
   unrelated operation after teardown. Unexercised controls stay unknown.
4. Audit and report GO / NO-GO per provider and tool path. → Verify: an
   independent evidence review can reproduce the disposition from sealed events,
   with source hashes, trust/configuration changes and owned cleanup recorded.

No live PAL calls are needed. Use existing credentials without recording them;
do not modify normal marketplace/trust registrations. Any temporary trust needed
for a concrete probe follows the existing authorization policy and is removed
afterward. Probe success is not a behavioral matrix pass.

**GO requires** reliable activation before subject access, complete same-actor
receipt evidence, denial before execution on every proposed supported path,
correct concurrent-call ordering and bounded lifetime on both declared runtimes.
**NO-GO** means any of those is false or unobservable. Record the smallest missing
capability and stop this experiment; do not silently ship a Claude-only contract,
weaken the grader, widen privileges or build a generic policy engine. A runtime
whose documented hook failures are nonblocking cannot support a claim of
unconditional failure containment, even if its healthy-path probe passes.

## Conditional integration and validation

Only after GO and review should a separate implementation slice define the exact
production files. Likely owners are `review-code/scripts/prepare_instructions.py`
for packaging metadata, a small canonical hook/state module for receipts,
`review-code/packet-preparation.md` and mode/agent entry points for lifetime, and
the generator/provider hook configuration for distribution. Preserve existing
Bash validation and shared review-spec/design consumers. Regenerate Codex output;
do not hand-author generated hooks or agent copies.

That integration needs meaningful state/adapter tests, hook composition and
direct-read regression coverage, generation/graph checks and independent source
review before model measurements. The preparation assertion and all R5 behavior
assertions stay unchanged. Runtime hook policy is an explicit comparison change:
freeze a successor contract and source, disclose the shipped candidate hook as
part of the treatment, keep unrelated infrastructure identical, and run fresh
matching baseline/candidate R5 repetitions under the pinned rubric. Do not
retrofit the guard into the immutable baseline or reuse older baseline captures.

Require all six R5 assertions in both candidate runs. Preserve denied premature
requests in the trace and apply the existing grader literally; do not assume a
blocked request is automatically a passing procedure. Isolated-mode, Codex and
remaining matrix coverage still have their own requirements. No prior candidate
success is reassigned to the successor.

## Assumptions and exclusions

The feasibility bets are that ordinary review activation is observable on both
runtimes, actual complete instruction results can be distinguished from raw or
truncated output, and each review can have an independent bounded lifetime. The
probe must disprove these assumptions when evidence is missing.

This scope excludes production guard implementation, a universal shell/MCP
policy engine, OS confinement, runtime upgrades, new services/models, profile
redesign and behavioral-matrix expansion. PAL remains user-deferred. A successful
scope document or probe does not complete Task 12 or authorize Task 13.
