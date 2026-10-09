# Task 6 verification

Status: **done**, with independent **APPROVE scoped to Task 6's implementation/integration slice** and no remaining hard slice blocker. The [final audit](review.md#final-disposition) supports the required I1/I2 behaviors within the limits below. This is not Task 12's repeated comparison or feature acceptance.

Current candidate: `10463ff31d654520b5712f1dc053407fccf48e9b`, frozen only in disposable controller storage, against repository base `61093fc7d610f44d3eba7f861bc4058a8f3c384b`. [Candidate6 identity](candidate6/identity.json), source/retained manifests, exclusions, patch and origin record bind the canonical/generated/agent bytes. No repository branch commit was created. The baseline, original seed fixtures and rubric remain unchanged.

## Implementation

Both implement modes always load shared change context and applicable instructions. Entry collects scope metadata; one common phase investigates full requirements and source before editing. Explicit conflicting behavior remains unresolved until an actual accepted decision; an observation or compatible alternative cannot silently weaken a requirement. Review handoffs refresh actual scope, baselines and evidence through the existing isolated/standard consumers. Hard unmet acceptance stays open; permitted external follow-up is durable and distinct from code completion.

The implement shared symlink uses the required relative target and its generated copy is regenerated. The structure suite checks both consumers through the same loop. No dependency, model, tool permission, fixture or acceptance requirement changed.

## Local checks

- [Nine shell suites](check-summary.json): **643 passing assertions, zero failures/skips** in their final runs. Original sandbox/cache/network-limited attempts remain in checks/. Fixture commits used per-command signing disabled; no persistent Git settings changed.
- Generator tests, plugin/Codex structure checks, Go tests and plugin graph validation pass. The existing graph cycle warning is retained.
- [Candidate6 freshness](freshness-candidate6.json): second generation leaves **685 generated files** unchanged, and **1,381 source entries** match the frozen candidate.
- [Mutation checks](mutation-checks.json): a clean disposable control passes; regular-file replacement, wrong resolving target, broken target and stale generated copy all fail as intended. Initial incomplete disposable copies are retained as setup failures.
- Shared instruction budgets remain **573/800** and **877/1,200** words. Bash syntax and whitespace checks pass.
- [Two-store probes](state-isolation/summary.json) verify real Capy search/index, absent foreign markers and unavailable private vaults. Every actor starts with fresh state, independent of those probes.

## Captures and corrections

The [run contract](run-contract.md) declares each candidate before launch and records explicit user authorization for the external Claude/PAL runs. The [review record](review.md) preserves source dispositions and native PAL output. Failed attempts and unlaunched snapshots are not relabeled.

| Candidate / capture | Disposition |
| --- | --- |
| Initial candidate `31269c67…` | Frozen, never launched. Independent source review found the requirement-document ordering exemption; corrected before binding. |
| Candidate2 `4ddc5c2a…`; binding/binding2 | Initial probe inferred the root after command denial; fresh binding2 observed the actual root. |
| Candidate2; i1-plan / i2-standalone | I1 read full task prose early. I2 read source before guidance and bypassed full test/review orchestration, omitting PAL. Retained failures. |
| Candidate3 `82e73ff6…`; binding3 / i1-plan3 / i2-standalone3 | I1 self-authorized a conditional interpretation and falsely completed the task. I2 invoked both workflows but reconstructed diff evidence. Detection enumeration was incomplete. |
| Candidate4 `68ea9c6e…`; binding4 / i1-plan4 / i2-standalone4 | Complete detection loading observed, but I1 again weakened a requirement without a decision. I2 exercised both reviewers; independent audit found cross-reviewer verdict leakage into PAL and invalid corroboration. |
| Candidate5 `0250f822…` | Frozen, never launched; extended with the plan-commitment clarification before execution. |
| Candidate6; binding6 | [Registered instructions and hook root verified](binding6-check.json); subject unchanged. |
| Candidate6; i1-plan6 | Independent audit supports the required conflict/decision boundary and unchanged code/specification. |
| Candidate6; i2-standalone6 | Independent audit supports the core implementation, tests, stale-evidence replacement and both independent handoffs; non-pristine scratch-file exposure and procedure limits remain explicit. |

## Candidate6 I1 evidence

The [sealed run](i1-plan6/manifest.json) retains [events](i1-plan6/events.jsonl), initial/final files and [report](i1-plan6/report.md). Independent audit identifies protocol returns13–20, all eight detection rules52–67, Python core78–83 and checkpoint89 before full requirements/source investigation. Client84/85 is explicitly declared bounded async routing at77, not premature behavioral investigation.

Full documents90/92/94 and provider96/97 establish the concrete conflict. Event142 compares the same receipt-less response against the two contradictory required outcomes and identifies the conditional alternative as a requirement change. The only edit143 records in-progress, unchecked acceptance, dated observations, the unresolved conflict and proposals. Final145 asks for a real decision and stops. Hashes and direct file comparisons confirm unchanged client/provider/tests/design/implementation bytes.

Residual procedure observations remain open for the pinned Task 8/12 grading: metadata grep33/34 returns task-bullet prose with filename fields, and Capy124 uses one broad `kk:` query after source reading instead of the declared mode lookup order. These observations are not silently passed.

## Candidate6 I2 evidence and limits

The [sealed run](i2-standalone6/manifest.json) retains [events](i2-standalone6/events.jsonl), payload captures, initial/final files and [report](i2-standalone6/report.md). Independent audit supports protocols16–23, all eight detection rules36–51, Python core63–68 and declared routing69/70 before checkpoint77. Caller content78–83 and explicit contract110 precede edit111. `/kk:test`119 and its core126–129 precede test edit136 and command138; actual result141 reports six passing tests covering falsey values, omission, ownership and both public caller paths.

Actual Git diff148/151 was obtained. An old scratch patch read201/202 was explicitly rejected210 and replaced211 before agent230 and PAL262/289. Both handoffs carry the same current source hashes and all eight review criteria. The child reads instructions236–261 before evidence269–287. PAL289 contains no child conclusions and precedes child final312; PAL298 reports 13 newly embedded files. The earlier candidate4 cross-reviewer contamination is not repeated in this observed handoff.

This is **bounded integration evidence, not a pristine matrix run**: the fixed `/tmp` name exposed a prior-run patch. Rejection and replacement demonstrate stale-evidence handling within this run; they do not erase the earlier read or establish complete state isolation. The copied current patch drops two blank context-space prefixes versus the actual Git output, although current changed source and tests reach both reviewers. Broad Capy104 follows initial source inspection, and the test-patterns lookup is skipped. These procedure/evidence limits remain open; no perfect workflow adherence or per-assertion matrix PASS is claimed.

## Remaining acceptance

Owner: implementing agent in Tasks 8/12. Pin/apply the workflow grader, execute the complete primary-provider matrix and secondary coverage, including existing routing/pre-write controls and I3/I4, and require every declared assertion twice under the selected contract. Preserve all observed failures, fix remaining gaps and recapture affected cases. One final dry-run pair cannot establish model reliability or generated-provider behavioral parity.

Before those measured runs, ensure fresh scratch evidence (unique run-owned paths or cleanup limited to verified owned artifacts), exact diff materialization, filename-only metadata extraction and required knowledge lookup ordering/coverage. Reject foreign scratch-file reads as pristine-run evidence. Verification condition: sealed traces establish fresh inputs, exact actual-diff handoffs and all declared procedure assertions under the pinned grader, twice; unknown/failed evidence remains open.

Task 2 gate 2B remains open and still blocks Task 12 and feature completion. No source opinion, generated-file check or successful subset waives those gates.

After the final audit, three scratch patches were removed only after their live hashes matched this task's captured Write contents; [cleanup proof](scratch-cleanup.json) records them. Sealed payloads remain retained. Cleanup does not retroactively make an earlier run pristine.
