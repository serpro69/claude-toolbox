# Implementation: clarify issue descriptions

> Design: [design.md](design.md)
> Tasks: [tasks.md](tasks.md)
> Issue: [#157](https://github.com/serpro69/claude-toolbox/issues/157)
> Status: Task 1 done; Task 2 in-progress; Tasks 3–4 pending (2026-10-01)
> Created: 2026-09-30

Task 1 progress and executed evidence are recorded in [verification.md](verification.md).
The complete candidate and its measured 1,297-word ceiling are recorded in the
[budget decision](verification/budget/decision.md). Task 2 has applied the prepared
proposal guidance and authored scenarios 18/19; behavioral grading is in progress.
Tasks 3–4 remain pending.

## Repository map

| Location | Responsibility |
| --- | --- |
| `klaude-plugin/skills/clarify-docs/SKILL.md` | Trigger, input forms, selected scope, output boundary, instruction loading. |
| `klaude-plugin/skills/_shared/document-clarity.md` | Evidence, protected meaning, reader guidance, audience rules, self-check. |
| `klaude-plugin/skills/clarify-docs/shared-document-clarity.md` | Existing symlink to the shared source; retain it. |
| `klaude-plugin/skills/clarify-docs/evals/` | Manual scenarios, staged source fixtures, and grader-only oracles. |
| `README.md`, `docs/getting-started/overview.md`, `docs/user-guide/skills.md` | Maintained discovery and usage documentation. |
| `kodex-plugin/skills/clarify-docs/`, `kodex-plugin/skills/_shared/document-clarity.md` | Generated equivalents, including dereferenced shared content and evals. |
| `scripts/kodex-generate-manifest.yml`, `Makefile` | Existing generation and validation machinery; no changes expected. |

Read [AGENTS.md](../../../../AGENTS.md) for canonical-source, instruction-ordering,
description, and eval conventions. Read the
[current eval protocol](../../../../klaude-plugin/skills/clarify-docs/evals/README.md)
before authoring or staging scenarios. Do not apply the completed feature's
superseded automatic-consumer integration; use
[ADR 0009](../../../adr/0009-optional-document-clarification.md).

## Build order

Implement the slices below in sequence because they share the entry point,
procedure, eval setup, and generated files. Each slice includes a complete behavior
and its evals. Fixture files and generated copies are mechanical consequences of
the listed source changes; task sizes describe the operative work.

Author each scenario and oracle before changing the relevant instructions. Run it
against the existing behavior to establish the observed baseline, then against the
candidate. An existing safeguard may already pass: record that result rather than
manufacturing a failure. Record failures and uncertainties without weakening an
assertion merely to obtain green results.

## Budget preflight

Task 1 begins by drafting the complete planned instruction change, before any
operative edits or grading of the candidate's behavior. Save non-operative copies
as `verification/budget/document-clarity-candidate.md` and
`verification/budget/clarify-docs-entry-candidate.md` in this feature directory.
They must include Tasks 1–3's complete rules, not placeholders or word estimates.
These are implementation evidence, not new plugin dependencies.

Map each design rule and existing safeguard to the candidate, remove duplication,
and count the entire shared procedure plus any mandatory dependencies. Record the
entry-point count separately. Use 1,200 as the initial procedure ceiling. If the
complete candidate exceeds it, retain A and set the ceiling to that measured count;
record the increase, deduplication performed, and the rules requiring the remaining
text in `verification/budget/decision.md`. This is the selected overflow outcome,
not a request to choose an architecture again during implementation.

The decision records the candidate revision or hashes, coverage mapping, exact
numeric ceiling, and rationale before operative work starts. No behavioral pass is
claimed by this size/preservation check. Later slices apply the prepared portions
and keep the complete candidate current, including both applied and pending rules.
Both the operative procedure
and full candidate must fit the recorded ceiling. Any subsequent increase repeats
this complete-candidate check and justification before applying changed text, with
affected behavioral cases rerun. Do not borrow unspecified future headroom or
count each slice's additions separately.

## Task 1: clarify bug reports locally

Primary files: the entry point, shared procedure, and eval README; new scenarios
16 and 17 in the matrix below.

1. Complete the [budget preflight](#budget-preflight) for all three behavioral slices
   → verify: full candidate files cover every planned rule and existing safeguard,
   and `verification/budget/decision.md` records the measured ceiling and any
   increase rationale before operative edits or candidate behavioral grading.
2. Add GitHub bug and selected-local-draft scenarios with fixed reader questions,
   protected reproduction/environment details, and explicit output permissions
   → verify: independent baseline traces show the observed input routing, evidence
   reads, and file effects; expectations stay outside editor staging.
3. Update the entry point's trigger, title, accepted inputs, and examples for issue
   description editing. State the implement/fix and read-only-title boundaries and
   preserve all current non-trigger boundaries → verify: a text review finds explicit issue editing
   inputs and no implication that every issue URL invokes clarification. Recheck
   the linked provider description guidance in AGENTS.md and measure the edited
   description against current limits.
4. Apply the prepared shared-procedure guidance for issue evidence, bug-report
   preservation, and the bounded GitHub same-repository audience default. Keep
   PR revision requirements scoped to PR edits and retain loading before all
   target/source reads → verify: scenario 16 preserves
   reported versus source-supported facts without demanding a PR diff or an
   unnecessary audience declaration for a private same-repository issue; scenario
   17 changes only the selected draft and preserves reproduction details.
5. Add issue fixture staging instructions to `evals/README.md`: synthetic platform
   responses, immutable body captures, no network, and no PR base/head repository
   setup for issue scenarios → verify: an editor can run these two scenarios using
   their declared files without discovering additional setup or a live account.
6. Regenerate and inspect outputs using the checks below → verify: both scenarios
   pass, both the operative and full-candidate counts fit the recorded ceiling,
   generated files match the canonical instructions, and structure/graph checks
   pass. Smoke-run existing
   `dense-source` and `runtime-pr` against the candidate to catch shared-rule drift.

## Task 2: clarify proposals for their actual audience

Primary files: shared procedure, entry point only if clarification is needed, and
eval README; new scenarios 18 and 19.

1. Add a synthetic Linear feature request with accepted intent, a proposed solution,
   absent implementation, supplied acceptance criteria, and an unresolved decision
   → verify: the baseline distinguishes which rules already work and which issue
   guidance is missing; the oracle accepts explicit unknowns.
2. Apply the preflight candidate's guidance for features and other issue types.
   Preserve supplied criteria, decisions, and uncertainty without imposing bug-report sections or
   requiring future implementation → verify: scenario 18 produces the authorized
   local draft without invented criteria, test results, or implementation claims.
3. Explicitly restrict the PR-head visibility presumption to PR review context and
   retain Task 1's bounded same-repository default. Apply the existing
   public/confirmed-sharing rules when that default does not cover the audience. Add
   scenario 19 with both accessible references and restricted or unknown-access
   evidence → verify: shared references survive, private facts are absent from
   both draft and report, and removal of a citation does not mask disclosure.
4. Regenerate and repeat the instruction-size/structure checks against the recorded
   ceiling, including the complete candidate with all pending rules → verify:
   scenarios 18 and 19 pass; existing `contract-only-pr` and `destination-visibility` still
   pass with unchanged assertions. Repeat scenarios 16/17 if touched rules affect
   their routing, evidence, or output contract.

## Task 3: handle gaps and keep execution requests out

Primary files: entry point/shared procedure only where gaps require a change, plus
eval README; new scenarios 20–24.

1. Add pasted-input, unavailable-source, and unavailable-body cases → verify:
   scenario 20 asks for a destination without writing; 21 writes a qualified local
   draft; 22 requests accessible body text without inventing a revision. Distinguish
   a captured pasted body from a selected editable local draft in every manifest.
2. Reuse existing destination, collision, and missing-evidence rules, adding only
   the issue clarification prepared in the preflight candidate → verify: accessible
   context is read before questions, unrelated files and remote captures remain unchanged, and
   known/unknown owners and concrete next steps remain in supported output.
3. Add separate natural-language implement and fix non-trigger scenarios. Make
   the skill description available for selection without preloading its body;
   supply a small synthetic issue and source fixture for normal execution
   → verify: neither request selects `/kk:clarify-docs`, loads its shared procedure,
   rewrites the description, or creates an editorial draft. Allow ordinary handling
   of the fixture's implementation request and grade only the editorial boundary;
   do not prime the agent by asking it merely to classify the request.
4. Regenerate and validate any changed instructions/fixtures → verify: all new
   assertions pass with complete traces and the complete instruction text fits the
   recorded ceiling. Update the preflight evidence before any necessary increase.
   Existing `pr-missing-context`, `pr-unavailable-source`, and code/brevity
   non-trigger assertions remain valid and pass against the candidate.

## Task 4: document usage and verify the complete extension

Primary maintained docs: `README.md`, `docs/getting-started/overview.md`, and
`docs/user-guide/skills.md`. This is the final verification task and depends on all
behavioral slices.

1. Use `/kk:document` to update discovery wording and add issue examples for local,
   pasted, and URL inputs. Explain evidence limits, output selection, audience
   restrictions, and the distinction from implementing an issue. Preserve the
   optional clarification workflow → verify: every documented example maps to a
   supported path; no text promises remote updates or a mandatory integration.
2. Run the complete behavioral matrix and existing regressions using the protocol
   below → verify: all applicable assertions have PASS verdicts with evidence;
   authored-but-unrun scenarios and incomplete traces are explicitly incomplete.
3. Run `/kk:test` over the full repository checks listed below → verify: record
   command outcomes and generated-file freshness, including any failure or
   environment limitation rather than claiming blanket success.
4. Run `/kk:review-code` with Markdown skill instructions, JSON eval specifications,
   and generated Codex content as the review scope; run `/kk:review-spec` against
   this design, implementation plan, and tasks → verify: address findings and
   record any remaining issue durably at its affected site or in this feature's
   tasks/evidence, with owner and next step. Do not close acceptance items that
   remain unverified.

## Evaluation matrix

Create one directory per row under `klaude-plugin/skills/clarify-docs/evals/`, with
`eval.json`, self-contained `test-files/`, and a sibling `oracle/` when applicable.
IDs 16–24 follow the existing 1–15 at this baseline; check uniqueness before adding
them and adjust only if intervening work has used an ID. Assertion IDs follow
`<eval-id>.<n>`. Oracles and eval specifications are grader-only.

| ID / directory | Input and setup | Decisive assertions |
| --- | --- | --- |
| 16 `github-issue-bug` | Synthetic private GitHub repository R issue, immutable title/body, no caller-declared audience, identified default-branch revision and tracked requirements/current source, one explicitly restricted tracked source, reported older environment, established feature directory containing an unrelated colliding draft. | Infer R's issue audience without asking or adding a limitation solely for privacy; retain accessible R references while excluding the explicitly restricted source's facts; preserve reproduction and expected/observed uncertainty across versions; no PR-diff prerequisite or replacement-title suggestion; produce one unused local draft; captures and unrelated draft unchanged. |
| 17 `issue-local-draft` | Selected local bug draft, source evidence, exact reproduction commands, identifiers and task checkboxes. | Edit only the selected file; retain conditions, commands, state and links; do not execute reproduction commands or change implementation. |
| 18 `linear-issue-feature` | Synthetic Linear URL response with immutable title/body, confirmed audience access to requirements, proposed mechanism, supplied criterion, explicit missing future implementation, open owner decision, explicit destination. | Separate accepted/proposed/current/future states; preserve criterion and unknown decision; no invented criteria, root cause, runtime delivery, PR revisions, or replacement-title suggestion; immutable input and one local output. |
| 19 `issue-destination-visibility` | Local draft of a GitHub issue in R, explicitly declared destination audience different from R's issue audience, public/shared references, explicitly restricted tracked source, credential-only and unknown-access external sources. | The declared audience overrides the same-repository default; retain legitimate shared references but exclude restricted facts and pointers from draft/report; no PR-head or same-repository shortcut for a different audience; no disclosure through uncited paraphrases; preserve caller-only output-link exception. |
| 20 `issue-pasted-missing-destination` | Immutable pasted-description capture and accessible context; no feature scope or destination. | Inspect context, ask for destination, leave all files unchanged; do not replace the pasted-input capture or invent a feature directory. |
| 21 `issue-unavailable-source` | Immutable pasted issue body with supporting source unavailable and a supplied destination. | Produce supported local edits with reported/proposed status, evidence limitations, and next action/known or unknown owner; preserve the pasted capture; no fabricated verification or blanket refusal. |
| 22 `issue-unavailable-body` | Synthetic read-only access failure, no body or alternate copy, supplied destination. | Explain retrieval limit and request text/access; no fabricated description, output file, live network attempt, or external write. |
| 23 `issue-implement-non-trigger` | Natural request to implement a synthetic feature issue, with a small source fixture; skill description available without preloading its body. | Recognize execution intent; allow normal fixture implementation but do not load editorial instructions, edit issue text, or create an editorial draft. No original/revised readers needed. |
| 24 `issue-fix-non-trigger` | Natural request to fix a synthetic bug issue, with a small source fixture; same skill-selection setup. | Same non-trigger requirements for a fix request. |

All editing cases assert instructions before target/source reads, bounded evidence
inspection, no implementation changes or remote writes, and no extra summary.
For cases 16 and 18, make the original title tempting to rewrite and protect it in
the oracle: copying the unchanged title is allowed, changing or suggesting a new
one is not. Distinguish tracker-title metadata from editable description headings.
Cases 16–19 and 21 use fresh original/revised reader comparison. Cases 20 and 22
grade questions, traces, and unchanged files instead of expecting a draft. Cases
23/24 grade non-activation and unchanged issue text; ordinary source edits within
the staged fixture are permitted and are not the editorial evaluation target.

Rerun all existing fifteen standalone scenarios. Also rerun the current design
consumer scenarios `clarity-after-drafting`, `clarity-refined-documents-only`, and
`clarity-unchanged-resume`, and document consumer scenarios
`clarity-preserves-profile` and `clarity-unchanged-document`. Use their current
specifications; archived automatic-pass results are not substitutes. Do not edit
consumer instructions to introduce issue clarification automatically.

## Execution and evidence protocol

The repository has no built-in behavioral eval runner. Follow the existing manual
protocol, extending its README for issue setup rather than adding automation.

- Stage each `test-files/` as a separate workspace root outside a `SKILL.md`
  ancestor. Exclude `eval.json` and `oracle/` from editor and reader access.
- Provide synthetic provider identity, body/access responses, and audience
  declarations in readable fixtures. Use clearly synthetic URLs and explicitly
  prohibit network calls. Do not set up PR revision pairs for issue scenarios.
- Before editing, fix applicable neutral comprehension questions, expected answers,
  protected claims, and specific defects in the oracle. Unknowns can be correct
  answers; irrelevant topics are N/A with a reason.
- Run an editor with the target instructions and exact allowed-file manifest.
  Run separate original/revised readers with no inherited conversation and only
  their respective artifact and declared accessible sources. Use identical reader
  settings. A separate fixture-capable general-purpose grader sees the oracle,
  sources, artifacts, answers, and editor trace; the repository's `eval-grader`
  role cannot substitute because it is prohibited from opening fixtures.
- Capture exact prompts at submission, model/settings, source revision/hashes,
  allowed-file manifests, before/after files, raw tool traces, reader answers,
  and per-assertion PASS/FAIL/PARTIAL with evidence. Shared filesystem access is
  not isolation: audit reads against manifests and invalidate leaks or incomplete
  traces. Do not reconstruct unavailable prompt evidence after the run.
- When native dispatch payloads are encrypted, retain the exact pre-dispatch
  plaintext, its hash, the dispatch receipt and linkage to the resulting run.
  Audit complete tool/message records against the manifests. Opaque transport
  alone is a recorded limitation, not proof of missing evidence; absent,
  reconstructed or mismatched required records still invalidate the run.
- Create `verification.md` in this feature directory when runs begin, indexing
  evidence under `verification/<run-id>/<scenario>/`. Mark unrun cases explicitly.
  Record authored/executed status separately and retain failed attempts.

Synthetic response success does not certify a live GitHub or Linear connector.
No comparison of approaches A and B is promised; the evals establish whether the
selected implementation meets its stated contract.

## Repository checks

For each slice, separately count (a) the entire operative shared procedure and its
mandatory dependencies and (b) the complete final-form candidate and its mandatory
dependencies, including both applied and pending rules. Each count must fit the
numeric ceiling recorded by the budget preflight; do not add the two counts together.
Then run
`make generate-kodex`. This target includes generator tests and both plugin/Codex
structure suites. Inspect generated copies of the shared procedure, entry point,
and evals; do not edit them directly. Run `make plugin-graph` to check instruction
links and orphans, leaving intentionally partial eval/template links intact.

For final verification, run all `test/test-*.sh` suites, `make generate-kodex`,
`make plugin-graph`, and the repository's Go tests. Track each command's exit status
so one successful command cannot conceal another failure. Check generation
idempotence by comparing generated files immediately before and after a second
generation; do not mistake intended uncommitted generated changes for drift.
Once the intended changes are committed, the CI freshness check is
`make generate-kodex` followed by `git diff --exit-code kodex-plugin/ .codex/agents/`.

Structural checks establish packaging and link integrity, not editorial fidelity.
Run behavioral checks on the final operative instruction revision. Repeat affected
cases when subsequent changes alter their rules; record which revision was tested.

## Acceptance traceability

| Issue requirement | Delivery / evidence |
| --- | --- |
| Consistent entry point, shared guidance, maintained docs, generated output | Tasks 1–4, generation inspection, final documentation review. |
| GitHub bug and unimplemented Linear feature | Scenarios 16 and 18, independent readers and fidelity grading. |
| Essential details, uncertainty, local output, gaps, and audience restrictions | Scenarios 16–22 and their tool traces/file comparisons. |
| Ordinary implement/fix requests do not edit descriptions | Scenarios 23 and 24; current non-trigger regressions. |
| Existing document/PR behavior remains intact | All fifteen existing scenarios plus current optional-consumer scenarios. |

## Assumptions, exclusions, and design changes

Apply the [assumptions](design.md#assumptions), [Not Doing](design.md#not-doing), and
[rejected alternative](design.md#rejected-alternatives) from the design. No new
dependency, generator behavior, profile registration, skill count, or historical
document change is planned.

No required issue behavior is deferred. The instruction budget and behavior remain
unverified until implementation. Budget overflow retains A and follows the
[preflight procedure](#budget-preflight): record the full candidate, exact revised
ceiling, and justification before operative edits, then execute affected evals.
Do not switch to a separate guide or weaken preservation rules to fit the budget.
Live connector certification and approach-B benchmarking are scope exclusions, not
promised follow-up deliverables.
