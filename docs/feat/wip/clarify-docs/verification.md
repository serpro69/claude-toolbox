# Clarify-docs verification

Task 1 evidence below describes its original local-document revision. Task 2's
PR and visibility evidence is recorded in [Task 2 verification](#task-2-verification).

## Task 1 verification

Date: 2026-09-29. Scope: local-document editing only; Tasks 2–5 remain pending.

**Task 1 complete.** The current ten scenarios pass all **40 applicable assertions**;
the six document cases pass all **30 revised-reader answers**, with fidelity graded
separately. Structure, generation stability and isolated code review pass. The full
repository shell suite retains two pre-existing hook-test failures described below.

## Instruction and structure checks

- Shared instructions: `wc -w klaude-plugin/skills/_shared/document-clarity.md`
  reports **820 words**. There are no additional mandatory linked instructions;
  this is below the 1,000-word target and 1,200-word ceiling.
- Checked the current [Claude Code description-budget guidance](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short)
  before authoring. It documents the 1,536-character default per-entry cap and 1%
  context-window listing budget, both configurable. The new description is 426
  characters including its final newline, below the repository's 1,024-character
  portable ceiling.
- `/kk:implement` and `/kk:test` detection: `skill-md` (entry point and skill-root
  adjacency), plus `python` for synthetic `.py` sources. Loaded all three applicable
  skill-authoring checklists; neither profile contributes a test index in the
  installed plugin. No dependency was introduced.
- `make generate-kodex`: PASS, including generator Go tests and both structure suites.
- `make plugin-graph`: PASS, no broken edges or orphans; existing graph-cycle warning
  remains advisory. No deliberately partial fixture links were repaired.
- All nine shell suites were executed. Eight passed. `test/test-hooks.sh` failed
  two assertions: it expects `node_modules` and `.log` to be denied, while the
  unchanged `klaude-plugin/scripts/validate-bash.sh` omits those patterns.
- Second generation: PASS, repeated after the eval-question refinement. The final
  SHA-256 digest over the sorted generated-file checksums was identical before/after:
  `98f4ff1b26b41620ba6f52cdf1a2855fa58015f02aa000e583036812f1c3cbbd`.
- All ten eval definitions parse and their declared fixture paths exist. The
  instruction-order dedup check found a single post-load source-reading phase.
- [Isolated code review](verification/task1-20260929/review.md): no code-reviewer
  findings; the external review's one LOW coverage finding was fixed by adding
  `clarify-docs` to the reference-check regex. The structure rerun passed all 184
  assertions. No P0/P1 systemic findings to index.

## Behavioral runs

Run `task1-20260929` executed all ten authored scenarios, including separate
original/revised readers for the six document cases. Independent grading recorded
39 assertion passes and one PARTIAL (2.1). That result is preserved. The narrowly
scoped `task1-20260929-retry1` used the same instructions and original fixtures,
with a concrete reader question declared before a fresh editor and reader pair.
It also received 4 PASS and 1 PARTIAL: existing-order behavior remained uncertain.
`task1-20260929-retry2` adds an executable default-change example to the supplied
synthetic source. Running it prints `{'new_lookup': 20, 'old_order': 15}` and exits
0. It retains the same questions, expected answers and assertions as retry1 and
uses another fresh editor/reader pair. Its independent grade is **5/5 assertions
PASS and 5/5 revised-reader answers PASS**, including an independent execution of
the stronger example. [Final source-disagreement verdict](verification/task1-20260929-retry2/source-disagreement/verdicts.md).
This pass applies to the stronger current fixture; neither earlier PARTIAL is
reclassified as a pass.

| Scenario | Latest applicable assertions | Comprehension: original → revised | Evidence |
| --- | --- | --- | --- |
| Dense source | 5/5 PASS | 5/5 → 5/5; orientation defects repaired | [Verdicts and artifacts](verification/task1-20260929/dense-source/verdicts.md) |
| Source disagreement | 5/5 PASS, retry2 | Baseline omits implementation mismatch → 5/5 | [Final verdict and artifacts](verification/task1-20260929-retry2/source-disagreement/verdicts.md); [first PARTIAL](verification/task1-20260929/source-disagreement/verdicts.md); [second PARTIAL](verification/task1-20260929-retry1/source-disagreement/verdicts.md) |
| Missing context | 5/5 PASS | 2 PASS, 2 PARTIAL, 1 FAIL → 5/5 | [Verdicts and artifacts](verification/task1-20260929/missing-context/verdicts.md) |
| Cross-file preservation | 5/5 PASS | 5/5 → 5/5; jargon/planned status repaired | [Verdicts and artifacts](verification/task1-20260929/cross-file-preservation/verdicts.md) |
| Already clear | 4/4 PASS | 5/5 → 5/5; all files byte-identical | [Verdicts and artifacts](verification/task1-20260929/already-clear/verdicts.md) |
| Clear factual error | 4/4 PASS | 5/5 → 5/5; only 60→90 reference repair | [Verdicts and artifacts](verification/task1-20260929/clear-factual-error/verdicts.md) |
| Skill instruction target | 3/3 PASS | N/A — routing | [Verdicts and artifacts](verification/task1-20260929/skill-instruction-target/verdicts.md) |
| Agent instruction target | 3/3 PASS | N/A — routing | [Verdicts and artifacts](verification/task1-20260929/agent-instruction-target/verdicts.md) |
| Code non-trigger | 3/3 PASS | N/A — routing | [Verdicts and artifacts](verification/task1-20260929/code-non-trigger/verdicts.md) |
| Brevity non-trigger | 3/3 PASS | N/A — routing | [Verdicts and artifacts](verification/task1-20260929/brevity-non-trigger/verdicts.md) |

All editor and reader sessions used `gpt-6-astra`, reasoning `xhigh`, with
`fork_turns="none"`. The runtime supplies no immutable model build identifier or
sampling temperature; neither is inferred. Inputs were staged outside the plugin
under a temporary directory, excluding `eval.json` and `oracle/`. Each session
received an explicit allowed-file manifest. Readers received only their version of
the artifact and audience-accessible reading path; source-only requirements and
implementation were available to editors and graders.

Two independent general-purpose graders (`gpt-6-astra`/`xhigh`) assessed local
document and routing cases separately, without inherited author conversation. The
local-document grader also assessed both later attempts using their own snapshots.
Verdicts link the manifests, hashes, exact prompts, outputs and raw traces for each
run. All authored Task 1 cases were executed; no authored-but-unrun Task 1 scenario
is counted as passing. Later-task PR and workflow-integration scenarios remain
outside this slice.

Supporting artifacts are stored under [verification/task1-20260929](verification/task1-20260929/).
Raw tool events are extracted from session transcripts, with original timestamps,
call arguments and outputs retained. System instructions and unrelated session
content are not copied. Manifests record staged hashes and session identifiers.
The log stores spawn-message transport text encrypted. Prompt records retain that
field and add `message_plaintext`, copied from the exact tool inputs in the live
conversation. This export is attested by the orchestrating session, not
cryptographically checked against the encrypted field. Standard harness and
repository instructions remain present in fresh sessions; author conversation and
oracles do not. Some login shells attempted a denied `navi.log` append during
startup; the trace audit distinguishes that environmental side effect from source
access. No out-of-manifest contents were exposed by those failed appends.
The same filesystem was shared: these runs enforce access by prompt manifests and
audit actual tool traces, not by filesystem isolation. Any out-of-manifest access
or incomplete trace invalidates the corresponding run. Reader answers are evidence
about these AI sessions, not proof of improved comprehension for human readers.

## Follow-up outside Task 1

**Owner:** repository maintainer. **Issue:** reconcile the two stale hook-test
expectations with the intended deny policy. Both hook and test are unchanged from
the starting revision, so this documentation task does not choose that policy.
**Next step:** decide whether the patterns should be denied, update the hook or
test accordingly, and rerun `bash test/test-hooks.sh`. The full repository suite
must not be described as green until this is resolved.

PR/destination-visibility scenarios and automatic-consumer scenarios belong to Tasks
2 and 3; the full feature evaluation and release verification remain Tasks 4 and 5.

## Reflection

Task 1 followed the local-only scope without changing the writing pipeline. The
source-disagreement eval needed a concrete reader question and stronger executable
source evidence; its expected answers and fidelity assertions were retained. The
operative skill did not change during those reruns. Dense and cross-file baseline
readers already answered correctly, so those edits demonstrate correction of the
predeclared orientation defects while preserving answers, not improved answer
accuracy. The encrypted prompt-export issue and manual trace-audit limitations are
recorded above; the export lesson was indexed under `kk:test-patterns`.

## Task 2 verification

Date: 2026-09-29. Scope: PR drafts and audience boundaries only. Tasks 3–5 remain
pending. Five new scenarios are authored and executed, with two separately
preserved reruns. **Task 2 complete:** all **24 applicable assertions** and
**20 revised-reader answers** pass at their latest applicable fixture revisions.

### Behavior and review

The new entry point accepts local drafts, remote PR bodies and pasted text. Edits
stay local, use actual base/head evidence when accessible, and apply the ordered
audience rules. The user guide documents destination selection, collision handling,
source-access limits and publication boundaries. No dependency or profile was added.

| Scenario | Latest verdict | Evidence |
| --- | --- | --- |
| Contract-only PR | 5/5 PASS; readers 1/5 → 5/5 | [Final verdicts](verification/task2-20260929-retry1/contract-only-pr/verdicts.md); [first PARTIAL](verification/task2-20260929/contract-only-pr/verdicts.md) |
| Runtime PR and draft collision | 6/6 PASS; readers 0/5 → 5/5 | [Verdicts](verification/task2-20260929/runtime-pr/verdicts.md) |
| Destination visibility and clear-prose repair | 6/6 PASS; readers 5/5 → 5/5 | [Verdicts](verification/task2-20260929/destination-visibility/verdicts.md) |
| Missing destination/source | 3/3 PASS; readers N/A | [Verdicts](verification/task2-20260929/pr-missing-context/verdicts.md) |
| Unavailable source with authorized destination | 4/4 PASS; readers 4/5 → 5/5 | [Final verdicts](verification/task2-20260929-retry1/pr-unavailable-source/verdicts.md); [first PARTIAL](verification/task2-20260929/pr-unavailable-source/verdicts.md) |

The [first run](verification/task2-20260929/summary.md) had 21/24 assertion passes
and three PARTIALs. The contract editor chose a valid 20-minute example, while the
oracle required 15 without supplying that example to the editor. The current base
and head requirements now explicitly provide the 15-minute example; the assertion
is unchanged. The unavailable-source reader omitted the verification owner/action
from broad questions. Its third question now explicitly asks for missing evidence
and ownership; that expectation moved from answer five to answer three, preserving
all protected claims. Both cases received fresh editors and original/revised
readers after those refinements. Operative skill instructions stayed unchanged.
Earlier PARTIALs are not reclassified as passes.
The [retry grade](verification/task2-20260929-retry1/summary.md) confirms 9/9
assertions and 10/10 revised answers for those two cases. These are refined-input
runs, not repeated trials on identical conditions or changed skill instructions.

[Independent code review](verification/task2-20260929/code-reviewer.md) found no
P0–P3 defects, including a follow-up review of the final fixture refinements.
[External review](verification/task2-20260929/external-review.md) reported two LOW
items: finish task tracking after grading, and correct a temporary diff capture
that omitted added files. The capture was corrected before the code reviewer
finished; its 97-file review included all added fixtures and generated counterparts.
Task tracking is now complete. These two LOW observations require no further action.
No P0/P1 systemic findings qualified for indexing. New learnings are recorded here;
no additional project convention was established.

### Checks and reproducibility

- The shared procedure is **1,000 whitespace-delimited words**, with no mandatory
  linked instructions. The frontmatter description is **418 characters**. Current
  [Claude Code description guidance](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short)
  was checked before editing; the description remains below the repository's
  portable ceiling. The skill-creator validator passes.
- Active profiles: `skill-md`, plus `python` for synthetic sources. All applicable
  implement/review checklists were read. Neither installed profile contributes a
  test or documentation phase index. No new dependency lookup was necessary.
- `make generate-kodex`: PASS, including Go tests, **184 plugin-structure** and
  **29 Codex-structure** assertions. Initial sandbox cache/agent-write restrictions
  were resolved using a temporary Go cache and authorized generation escalation.
  The default Python 3.10 lacked a TOML parser; selecting the existing Python 3.12
  for these checks resolved all seven misleading parse failures without file changes.
- Second generation: PASS, no further output changes. SHA-256 over sorted generated
  file checksums before and after:
  `8307312bea859c921985422be9d04604a9f6175860166c0aea0beeebf6d758a8`.
- `make plugin-graph`: PASS, including Go tests; no broken edges or orphans. Its
  existing cycle warning remains advisory. Deliberately partial fixture links remain.
- All nine shell suites ran; **eight pass**. Manifest/schema suites initially hit
  cache restrictions and temporary-commit signing errors; reruns with cache access
  and process-local `commit.gpgsign=false` passed. The only remaining failures are
  the same two unchanged hook expectations documented in Task 1 (node_modules and
  .log). The maintainer's existing follow-up above still applies.
- All 15 eval definitions parse and resolve declared fixture paths; assertion IDs
  are sequential. The runtime fixture's three assertions pass. `git diff --check`
  passes. The ten Task 1 scenarios were not rerun for this slice; their historical
  results do not certify the final combined feature revision. Task 4 owns that run.

Raw [check logs](verification/task2-20260929/checks/) retain initial failures and
successful retries. Behavioral evidence records source/instruction hashes, actual
Git refs/diffs, original/revised artifacts, prompts, tool calls/results, reader
answers and independent per-assertion grades. Remote reads are simulated by declared
offline platform responses and synthetic URLs; no live connector was exercised.

All editor and reader sessions used `gpt-6-astra` with `xhigh` reasoning and no
inherited author history. Model build and sampling temperature are not exposed.
The independent general-purpose grader used the same model/settings, with no
inherited author history; its session record accompanies the first run.
Separate readers receive only their artifact. Editors and readers receive no oracle.
Shared-filesystem isolation uses allowed-file manifests and trace audits, not OS
sandbox separation. The observed traces stay within those manifests. Encrypted
spawn transport is preserved alongside orchestrator-attested plaintext prompts;
that transcription is not cryptographically verified. Results describe these AI
reader sessions, not general human comprehension or repeatability.

### Report-path limitation

The contract editor's caller-facing completion message uses an absolute clickable
link to its selected output. The PR body contains no absolute workspace pointer.
The harness prefers absolute links for real local artifacts, while the shared
procedure applies its path restriction to change reports too. **Owner:** feature
maintainer. **Next step (Task 4):** clarify the distinction between a caller-only
output link and private source pointers disclosed in a destination artifact, then
exercise it explicitly. This is retained as a runtime instruction-precedence
limitation; passing the current assertions does not establish a path-free report.

## Task 3 verification

Task 3 integrates the shared clarity procedure into `/kk:design` and `/kk:document`.
Instructions load before subject matter; one final pass follows drafting. Resumes
edit only refined documents, and unchanged resumes skip editing. Domain topics,
task state and links remain protected. The existing `/kk:implement` call chain is
unchanged: plan completion invokes documentation; standalone completion does not.
The user guide explains each entry point and its review limit.

Five new consumer evals ran in fresh sessions. The [first grade](verification/task3-20260929/verdicts.md)
records **19 PASS / 2 PARTIAL**, with all ordering, file-boundary, pass-count and
artifact-preservation assertions passing. The partials concern omitted reporting:
the document response did not state its in-session review limit, and the route
inspection omitted a later explicit documentation request. Both initial results
remain preserved.

The document consumer now explicitly requires the review-limit statement in its
change report. The routing prompt now asks about a separate documentation request;
its assertions are unchanged. [Focused reruns](verification/task3-20260929-retry1/run.md)
use fresh sessions and separate evidence. Their [independent grade](verification/task3-20260929-retry1/verdicts.md)
records **9/9 PASS**, bringing the latest applicable results to **21/21 PASS**.
The three design cases remain applicable because their instructions and inputs did
not change in this correction.

The [independent code review and follow-up](verification/task3-20260929/code-reviewer.md)
found no P0–P3 issues. A [fresh external review](verification/task3-20260929/external-review-fresh.md)
returned no actionable findings. The first external submission disclosed the code
reviewer's approval; its [independence limitation](verification/task3-20260929/external-review.md)
is preserved, and the fresh review omitted that information. Its sole LOW tracker
observation is addressed by finalizing Task 3 after grading. No systemic P0/P1
finding or new project convention needed indexing.

### Task 3 checks and limits

- `make generate-kodex`: PASS, including Go generator tests, **184 plugin-structure**
  and **29 Codex-structure** assertions. The first sandbox attempt could not write
  `.codex/agents`; authorized generation with a temporary Go cache succeeded.
  The checks used the existing Python 3.12 through a temporary PATH shim.
- Final repeated generation: PASS, no further generated changes. The aggregate
  checksum is recorded in [additional checks](verification/task3-20260929/checks/fixture-validation.md).
- `make plugin-graph`: PASS; no broken edges or orphans. The existing cycle warning
  remains advisory. Deliberately partial fixture links remain unchanged.
- All nine shell suites ran; **eight pass**. Two schema suites initially failed
  on sandboxed uv-cache access and passed with authorized cache access. The same
  two pre-existing `node_modules` / `.log` hook assertions fail. The repository
  maintainer's [existing follow-up](#follow-up-outside-task-1) remains applicable.
- Both skill validators pass. All nine design/document eval definitions parse,
  resolve declared fixtures and use sequential assertion IDs. The new empty
  Kustomize fixture builds to no resources. `kubeconform` is unavailable; its
  install hint and skipped schema coverage are recorded in additional checks.
- The mandatory shared procedure remains **1,000 words**. Skill descriptions,
  dependencies and implementation completion instructions did not change.

The [run manifest](verification/task3-20260929/run.md) and retry manifest record
requests, instruction/input hashes, drafts, final outputs and tool traces. Editors
used `gpt-6-astra` / `xhigh`, `fork_turns="none"`; model build and temperature are
not exposed. The independent grader used the same model/settings. Allowed-file
manifests and trace audits constrain shared-filesystem access; there is no claim
of separate OS sandboxes. Committed request copies omit only terminal blank lines;
verbatim runtime text remains in the traces.

These are procedural integration checks. The implementation-mode case is a
read-only instruction-route inspection, not a completed implementation lifecycle.
Separate original/revised comprehension readers and final feature-wide acceptance
remain owned by Tasks 4–5. No Task 3 result proves improved human comprehension or
re-certifies the earlier standalone/PR scenarios at the combined feature revision.
