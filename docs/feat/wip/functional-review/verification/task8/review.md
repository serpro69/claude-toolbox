# Task 8 isolated review

Independent `code-reviewer` agent `/root/review_task8`, with `fork_turns=none`,
reviewed the Task 8 diff and subsequent corrections. It loaded the seven resolved
skill-md/Python criteria before evidence. The installed 0.23.0 root lacked the
new common method; it stopped and requested the canonical absolute paths before
investigating. Those paths and the requested retained dispatch records were
supplied. Task 2 gate 2B and Tasks 9–13 were explicitly out of scope.

## Corrections and author context

The independent reviewer found that the adapter verified manifest-listed files
but discovered Codex event streams and oracle inputs by directory enumeration.
The corrected adapter selects events only from the original capture seal and
oracles only from the frozen fixture map. Regression checks reject an unsealed
stream and ignore an injected unpinned oracle. Rebuilding confirms all 611
already graded evidence files are unchanged; the original adapter remains pinned
and preserved.

PAL used `gemini-3.1-pro-preview/max` through the required two-step review.
[Initial arguments](palStep1Args.json), [step 1 result](palStep1.json) and
[native final result](palStep2.json) are retained. Its native findings were:

- **HIGH:** checking every ancestor for symlinks rejects trusted roots beneath
  platform aliases. Author context: corrected to inspect only appended path
  components; the platform-alias regression passes. The independent source
  reviewer inspected this correction.
- **LOW:** directory entries under `oracle/` can make `copyfile` fail. Author
  context: frozen manifest selection now replaces directory iteration; unsupported
  nested oracle paths explicitly fail instead of importing undeclared inputs.
- **LOW:** direct `item["id"]` access rejects malformed Codex events. Author
  context: retained fail-closed behavior is intentional for this sealed Task 2
  adapter. Inventing fallback event IDs would obscure absent provenance; new
  capture formats require an explicit adapter change and verification.

PAL reports **zero embedded/examined files**. Its coverage is unverified and its
output is not corroboration or proof of source correctness. Native severities
are preserved above; the independent source review has no remaining P0–P3
findings. No systemic P0/P1 implementation findings require knowledge indexing.

## Final independent report

The following is the reviewer's returned report.

### Code Review Findings

**Files reviewed**: 10 primary source/distribution files; 495 lines changed in the supplied patch, plus subsequent adapter fixes and focused calibration/evidence records  
**Active profiles**: skill-md, python  
**Overall assessment**: APPROVE — scoped to Task 8  
**Intent and scope**: Explicit Task 8 requirements: workflow grading, preserved component grading, sealed evidence access, calibration, and grading retained baselines. Tasks 2B and 9–13 remain excluded.  
**Baselines**: Review base `88a5b978c9d765bab429751b153c69a41132d29c`; candidate working tree after reviewed fixes. Compatibility baseline: prior component contract in the supplied diff. Behavioral captures use actor revision `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61` and frozen revision-1 rubric.

### Behavior and Compatibility

**Supported:** Omitted mode preserves output-only component grading. Explicit workflow mode requires completed reads, actual dispatch evidence and resulting snapshots; final claims cannot establish these behaviors. Canonical and inspected generated instructions retain this distinction.

**Supported:** The corrected adapter selects event streams from original capture seals and oracle inputs from frozen fixture manifests. It preserves tool-result content, identifiers, failure statuses and timing, while recording incomplete child/dispatch coverage. Regression source covers unsealed events, injected oracle files, tampering, traversal, symlinks and existing destinations.

**Supported within attributed execution limits:** Seven accepted calibration controls match their expected verdicts, including corrected inline component repetitions. All 16 retained baselines have all 106 assertion rows: **51 PASS / 44 FAIL / 11 PARTIAL**. Four missing captures remain UNRUN. Retained dispatch records bind fresh graders to the pinned instructions and manifests.

Controller evidence reports eight passing adapter tests, 644 shell assertions, passing Go/graph checks, freshness across 725 generated files, and 611 unchanged grading-evidence files after adapter corrections. I inspected these records; I did not execute checks.

**Not applicable:** This increment introduces no live deployment or migration. Candidate behavioral acceptance remains outside this review.

### Findings

P0, P1, P2 and P3: none.

### Removal/Iteration Plan

None required. The original pinned adapter source and superseded calibration attempts are retained with their provenance.

### Areas Not Covered

I did not independently recompute hashes or audit every grader tool action. Execution results and dispatch transcriptions are controller-attributed evidence.

Calibration uses fresh default agents loading pinned instructions. It does not establish registered-role/provider parity; the exact service model identifier is unavailable. Filesystem confinement is explicitly unclaimed.

Full candidate acceptance, live actor capture and the receipt/use fallback remain unassessed.

### Evidence Requests

None outstanding for this scoped verdict. Missing common instructions and requested grading/dispatch records were supplied and inspected.

### Outstanding Prerequisites

Tasks 2B and 12 retain the four missing captures, any future fallback calibration/regrading, and candidate comparisons. The implementing agent owns this work; its next actions and verification conditions are recorded in `tasks.md` and `verification/task8/README.md`. Current FAIL/PARTIAL/UNRUN results do not waive those gates.
