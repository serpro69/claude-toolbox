# Advisory-closure comparison contract v1

> Declared: 2026-10-17, before any calibration, binding or measured session
> Owner: implementing agent, [Task 12.19](../../../tasks.md#task-1219-freeze-the-closure-candidate-and-review-its-comparison-contract)
> Scope: frozen candidate and reviewed comparison declaration; execution unrun

## Authority and identities

The user selected freezing the reviewed candidate and writing an independently
reviewed run contract with explicit keep/reject criteria. This authorizes offline
preparation and review. It does not select actor execution, model calibration,
plugin/trust registration, PAL resumption or adoption. The execution owner must
complete the prelaunch gates below when measurement is selected.

Baseline: `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`, the immutable pre-feature
actor revision. Candidate: `4b69421465131e2e9e497f200ec9ddbdb439ac83`, a temporary
source commit containing only the plugin and generated-agent trees from parent
`11b2c6efb0638605bb6acd3eb184edb9abd10f56` plus the four reviewed closure-file
replacements. [Provenance](source-provenance.json) and [patch](candidate.patch)
identify those bytes. The working branch and index were not committed or changed
by snapshot creation. Planning documents are outside both actor snapshots.

Full source archives include evaluator files and remain controller-only. Only
the separately archived **retained** trees may enter actor workspaces/catalogs.
The existing bundle builder validates Git blobs, file modes, internal symlinks,
exclusions and retained hashes. Baseline/candidate manifests identify 435/447
retained files, respectively; exclusions are separately listed. Restore the
archived bytes, not the installed normal plugin or future working-tree contents.

This comparison measures the broader candidate against the pre-feature baseline.
It cannot isolate this closure replacement's incremental causal effect. Historical
Task 12.17 results are context, never substitutes for fresh matching runs. No
unchanged-current third arm or automatic expansion is included.

## Matrix, prompts and source inputs

Exactly **64 measured sessions**: four cases × two providers × two modes × two
sides × two fresh repetitions. [matrix.json](matrix.json) enumerates every job,
its ordinary prompt and source identity. Planned order is case, provider, mode,
repetition, then baseline/candidate; run serially and retain that order.

| Case | Fixture | Rubric | Purpose |
| --- | --- | --- | --- |
| R6D | `functional-inherited-defect-dormant`, eval 22 | R6 validity v1 | Surfaced inherited advisory receives a separate action; compatible label change stays approved. |
| R6M | `functional-inherited-defect-exposed`, eval 21 | R6 validity v1 | Newly exposed inherited failure remains a blocker with a contract-preserving correction. |
| R5 | `functional-clean-partial-feature`, eval 12 | Revision 2 | Clean partial feature closes without invented future work. |
| R9-recovery | `functional-justified-recovery`, eval 11 | Revision 2 | Normalization remains approved without removing required bounded recovery. |

Both sides receive identical current fixture snapshots and ordinary prompts from
the pinned evals. Standard invokes the registered skill; isolated invokes actual
orchestration, not a directly prompted reviewer. Use the existing prompt conversion:
Claude `/kk:review-code:isolated`; Codex `$kk:review-code isolated`. Do not add
advisory hints, expected verdicts or rubric language. `evaluation-inputs.tar.gz`
retains complete fixtures, assertions/oracles, both rubrics, the grader and existing
calibration inputs; only each fixture's staged subject snapshots reach actors.

There are **464 original assertion rows**, 232 per side. Grade every row, retaining
PASS/FAIL/PARTIAL and conditional-trigger evidence. Standard dispatch conditions
are absent, not transport successes. The comparison and original feature acceptance
remain distinct, as specified below.

## Runtime, tools and evidence

Pin the observed local clients: Claude Code **2.1.296**, Codex **0.163.0**, Capy
**0.17.3**, Linux and controller/actor Python **3.12.11** at the interpreter path
recorded in [runtime.json](runtime.json). Recheck exact versions and executable
identity before launch. Drift requires a separately reviewed successor execution
declaration before either side runs; never pool configurations or substitute models.

- Claude parent and named reviewer: `claude-opus-5-5`, high effort, existing forced
  child-model configuration. Normal hooks, project/local settings, auto-memory off,
  `dontAsk`, explicit existing tool allowlist, `--plugin-dir`, run-local registry
  and strict MCP config. The launched MCP config excludes PAL even though the
  inherited allowlist contains its names.
- Codex parent: `gpt-6-astra`, xhigh; named `code-reviewer`: generated source's
  `gpt-6.1-sol`, xhigh. Public app-server, `workspace-write`/`never`, provider fallback
  disabled, isolated marketplace/cache and project configuration. Record existing
  registration/trust absence before any temporary write; never overwrite normal
  entries. Retain and remove only owned temporary entries after capture.
- Graders: independent fresh `eval-grader` roles, `gpt-6.1-sol`/xhigh, no inherited
  actor/implementation history. Pin `task2b/grader.md` by content hash and apply
  the case's frozen rubric identically to both sides. Record actual dispatch
  settings; do not claim service-internal model telemetry.

Use the existing R7-conclusions/Opus55 capture transport and owned-process cleanup
as the implementation basis. [controller-inputs.json](controller-inputs.json)
pins those existing sources; it is **not a finished execution adapter**. The R7
adapter selects different cases, while the R6 diagnostic adapter is standard-only
and uses one source on both sides. Neither may be launched unchanged for this
comparison. A successor adapter must select this matrix, route both rubrics and
enforce this declaration; review/test/hash it before any model call. Preserve
historical controllers and results. No new dependency or permissions are proposed.

Every probe and measured run uses a fresh owned workspace outside any SKILL.md
ancestor, empty run-local Capy store and unavailable private vault. No prior store,
real vault history, mutable actor output or grading material may be inherited.
Scan bundles and caches, audit observed accesses and preserve raw public evidence;
no OS-wide filesystem confinement is claimed. A detected evaluator leak invalidates
the attempt. Keep private reasoning and credentials out of evidence.

Seal ordered public tool events, actual dispatches/results, reports, initial/final
subject files and runtime configuration with hashes. Keep per-actor ordering and
parent/child links. A source read proves returned bytes, not exact submitted prompt
content. The existing receipt/use fallback applies only to R3 7.5/7.6 and I2 9.5;
**none of these four cases receives that fallback**. Missing exact dispatch evidence
retains its original FAIL/PARTIAL; final claims cannot supply it.

## Calibration and prelaunch gates

The files sealed now are a **source/criteria preparation freeze**, not a completed
runtime freeze or permission to launch. Before the first measured session:

1. Review the successor adapter; verify offline matrix count/identities, rubric
   routing, refusal of reuse/overwrite and stop/cleanup behavior. Recheck frozen
   source/fixtures and generated parity. Create a distinct execution-freeze record
   referencing this preparation seal and the adapter/dependency hashes.
2. Calibrate the pinned graders on the five retained ordering controls and eight
   retained R6 semantic/trigger controls. Re-dispatch them freshly; historical
   calibration success is not this runtime's result. Keep expected answers outside
   grader inputs. Additionally calibrate the disposition table below on complete
   PASS, target FAIL, missing evidence, absent/child-only advisory and tolerated
   report omission versus unsupported-safety-claim examples before applying it.
3. Run four separate binding probes: each provider × source side, including an
   actual named reviewer. Require each side's own complete instructions and agent
   bytes; do not inject candidate-only common files into the pre-feature baseline.
   Confirm models, root identity, complete reads, working Capy and absent PAL.
4. Prove fresh Capy state with two separate probes: empty stores, successful
   index/search, foreign marker absent, private vault unavailable. Neither probe
   state may seed measured runs.
5. Retain and independently inspect successful calibration/binding/state evidence
   and hash it in a preflight attestation tied to the execution freeze. Prepare
   all 64 fresh inputs before the first measured capture. Any unmet gate blocks
   launch; its owner remains the implementing agent.

No actor/grader calibration or binding call is part of Task 12.19. A changed
contract gets a new version and review before capture; preserve this declaration.

## Bounded decision rules

These are prospective **candidate-selection criteria**, not changed assertion
grades or a waiver of required feature acceptance. Evaluate the whole final report
and sealed workflow. Report original grades first, then the bounded disposition.

| Decision check | Requirement for every candidate repetition in each provider/mode |
| --- | --- |
| Advisory follow-up | R6D 22.3, 22.5, 22.6 and 22.7 PASS; final-advisory trigger **present in all eight candidate R6D runs**. Child-only discovery or conditional PASS with absent trigger does not demonstrate follow-up. |
| Advisory reachability and limits | Every required bounded component of R6D 22.4 in the mapping below passes; only its stated disabled-default omission may be tolerated. The original whole-row grade is unchanged. |
| Material failure and correction | R6M 21.3–21.8 PASS, preserving requested detailed output, empty-input success and explicit overrides. |
| Clean approval | R5 12.2–12.5 PASS; no speculative remediation, pending implementation, flag framework or production-access gate. |
| Recovery preservation | R9 11.2–11.5 PASS; no removal of required recovery or invention of unrelated mechanisms. |
| Instruction ordering | 21.1, 22.1, 12.1 and 11.1 PASS under each case's pinned rules. |
| Real isolated participation | For each isolated candidate, a linked actual named-reviewer dispatch and returned review are observed. This is a bounded participation check, not a substitute PASS for any original dispatch/payload assertion. |
| Evidence honesty and no new harm | No unsupported production/global-safety claim, misattribution, waived hard requirement, unapproved subject edit or substantiated new defect introduced by the candidate's advice. |

R6M 21.2, R6D 22.2 and the checked-in-default **omission component** of 22.4
remain required graded report obligations but are outside the bounded keep gate.
The prior [disposition](../r6-validity/diagnostic/README.md#disposition-and-concrete-follow-up)
already defers added trace prose pending value. That does not excuse an incorrect
trace, fabricated check or unsupported claim: those fail the no-new-harm check.
For a tolerated report omission, the sealed workflow must establish the corresponding
before/after behavior. If it does not, the result is inconclusive, or reject when
contrary behavior is demonstrated. Keep each original FAIL/PARTIAL visible.

For **22.4**, retain its whole-row grade and additionally record these components
for the bounded decision. The source is the complete final report except where
workflow corroboration is explicitly required below; no exact phrase is mandatory.

| Original 22.4 component | Bounded decision requirement |
| --- | --- |
| Scope of conclusions | The report limits conclusions to inspected behavior; omission from a complete report or a broader unsupported conclusion fails this check. |
| Inherited-defect trigger | A surfaced advisory identifies empty input in detailed mode. Missing either part in a complete final report fails this check, even if its attribution and follow-up are otherwise correct. |
| Checked-in disabled default versus explicit detailed mode | Only omission of the fact that the checked-in default stays disabled is tolerated, and only when sealed workflow evidence establishes that fact and the report makes no contrary claim. The original 22.4 still FAILs. A wrong default/reachability claim fails this check; unavailable workflow corroboration is PARTIAL. |
| Historical settings and unsupported claims | The report distinguishes inspected local behavior from unverified historical/deployed settings and makes no unsupported global-safety or production-incident claim. Missing this limit in a complete report or an unsupported claim fails this check. |

A complete advisory saying only "an inherited exception exists; fix separately"
omits the empty/detailed trigger and therefore yields **REJECT**, even if 22.6
passes. A report identifying the trigger and local-only evidence, with the workflow
establishing the disabled default but the report omitting that default, may meet
this bounded mapping while original 22.4 remains FAIL. Truncated/missing final
evidence is PARTIAL, not a tolerated omission. Include both examples in disposition
calibration before use.

In isolated mode, 21.9, 22.8, 12.6 and 11.6 retain the required PAL components.
PAL is user-deferred and excluded, so those composite assertions cannot PASS.
Grade other missing payload components honestly; do not infer exact prompt parity
from participation or source use. Their full acceptance stays open even if this
bounded candidate-selection decision is KEEP.

Apply this precedence after auditing evidence; never average away a failed mode:

1. **REJECT** if any valid candidate run demonstrates a failed decision check,
   including a surfaced advisory without action or a control violating its contract.
   A known failure stays reject even if another run is missing. Preserve the patch,
   evidence and reasons; recommend reverting only this closure candidate. No
   automatic next wording experiment or rerun follows.
2. **INCONCLUSIVE / DO NOT ADOPT** if there is no demonstrated decision-check
   failure but any planned baseline/candidate capture or required decision evidence
   is missing/invalid, a decision check is PARTIAL, or any of the eight R6D final
   advisory triggers is absent/unobservable. Retain the unaccepted candidate and
   name the missing evidence. Do not retry until an advisory appears or substitute
   a report replay for these end-to-end sessions.
3. **KEEP FOR THIS BOUNDED SLICE** only when all 64 valid captures are independently
   graded, every decision check above passes twice in every candidate provider/mode,
   and all eight candidate R6D advisory triggers are present. Baseline behavior
   need not pass; if it already passes, state that without claiming improvement.

Source setup/integrity failure or capture/runtime failure stops further launches
and retains the attempt. Preserve every attempt; no overwrite, silent skip,
automatic replacement, threshold change or post-result fixture revision. Valid
earlier failures remain evidence. A grading/calibration discrepancy blocks decisions
until independently resolved without changing the pinned criteria to fit results.

KEEP would justify retaining this correction under these controls; it would not
establish causal attribution, reliability, full case acceptance or feature readiness.
Original R6/R7 acceptance, deferred report/PAL obligations, legacy controls,
unfinished implementation verification and Task 13 retain their owners and next
actions. No result or keep decision is claimed by freezing this contract.
