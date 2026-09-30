# Optional document clarification — verification

Date: 2026-09-30. Starting revision: `3c06264e6937cfdde62a6c408a6863157410332d`.
Decision: [ADR 0009](../adr/0009-optional-document-clarification.md).

## Behavioral checks

Six fresh Codex sessions exercised the updated design/document workflows against
synthetic fixtures. A separate grader inspected actual tool traces, final artifacts,
source fixtures and fixed oracles. All 24 eval assertions pass at the final revision;
all protected claims and supplemental artifact/orientation requirements pass.

| Scenario | Assertions | Final evidence |
| --- | --- | --- |
| Fresh design | 5/5 | Initial execution; applicability checked after broadening the suggestion to all created artifact paths |
| Refine only implementation.md | 4/4 | Initial execution; relevant instructions unchanged |
| Unchanged design resume | 3/3 | Initial execution; relevant instructions unchanged |
| Documentation with Kubernetes rubric | 5/5 | Fresh retry after retaining purpose-first guidance in ordinary drafting |
| Implementation completion routes | 4/4 | Initial read-only route inspection; final applicability checked |
| Unchanged documentation | 3/3 | Fresh retry against the final document instructions |

The initial six-case run passed all numbered assertions and protected claims, but
the profile-document case was **PARTIAL** overall: its opening described the empty
overlay without explaining its stable-location purpose. That result is preserved.
Document Step 5 now explicitly retains purpose, current/planned behavior, evidence
limits and unresolved decisions as ordinary drafting requirements. The two document
cases were rerun from pristine fixtures; both pass. No assertion or oracle was relaxed.
The other four cases received applicability assessment rather than fresh execution.

Checks cover optional suggestions naming the affected paths, their order before
design review, absence of automatic clarification loads/execution, unchanged-output
behavior, and preservation of task state, links and profile topics. They do not
measure human comprehension. Implementation coverage inspects instructions rather
than executing an entire implementation lifecycle.

## Repository checks and review

- All nine shell suites pass, including 184 plugin-structure and 29 Codex-structure
  assertions. Temporary-repository commit signing was disabled for the test process.
- All three Go tool packages pass their tests. Graph validation finds no broken
  edges or orphans; its existing cycle warning remains advisory.
- Codex generation, both modified skill validators, eval JSON/fixture-path and
  assertion-ID checks, and `git diff --check` pass.
- The standalone clarification skill, shared procedure and archived feature history
  are unchanged.
- Isolated code review approved the final change. Its initial P3 about naming
  exactly three files was corrected to include every created artifact, including
  split documents. The external Gemini review initially reported that wording from
  a superseded patch; after checking the final source/generated files it returned
  no findings. No systemic P0/P1 finding or new convention required indexing.

## Evidence and limits

The temporary run directory is `/tmp/clarification-opt-in-20260930`. It contains
requests, original input hashes, instruction snapshots, JSONL tool traces, final
artifacts, initial and retry grader results, and check logs. Raw evidence is retained
locally, not committed; this note preserves the outcomes and initial partial without
claiming that the repository alone contains a replay bundle.

The editors used `codex-cli 0.159.2`, fresh ephemeral sessions, default model settings,
ignored user configuration, and workspace-write sandboxes. The specific model build,
reasoning setting and temperature were not exposed. Only fixtures and a tested
instruction package were staged; eval definitions and oracles were withheld from
editors. Allowed-file trace audits pass, but these runs do not establish OS-level
read isolation. Maintainer-session Capy lookups failed with a database decryption
error; the editor sessions had no external MCP configuration.

The retries have no separate pre-run input-hash manifest. Their inputs were checked
against unchanged canonical fixtures and first-read trace contents; protected files
retain their original hashes. Shell startup attempted a denied navi.log write;
the traces show no successful write outside the permitted workspace.

Each instruction snapshot has 187 files. SHA-256 over sorted
`relative-path + space + file-sha256` entries joined by newlines:

- Initial: `5027273c258d229f49668147c967004d967360d4e8667fd18a6b3bfc97c41782`
- Final: `36bf25f3f07c62da93b1326f659be2035a2ffd86a681902ca4a598b18a727d67`

| Session | Thread ID |
| --- | --- |
| Fresh design | `01a0f221-99ea-7993-aa21-7df843a461da` |
| Refined design | `01a0f221-99f4-76c1-81d6-c49391a557f8` |
| Unchanged design | `01a0f221-99eb-7310-9a39-dbb78800e6a3` |
| Profile documentation, initial | `01a0f221-99f5-79a0-a628-a88c5af405ce` |
| Completion routes | `01a0f221-9a02-74c3-8d34-60a790031524` |
| Unchanged documentation, initial | `01a0f221-9a1c-74a0-bbec-c7d00ab30be5` |
| Profile documentation, retry | `01a0f237-63e6-7cf0-b476-8e3c68d6a512` |
| Unchanged documentation, retry | `01a0f237-63e6-7291-8e2e-3a39d69c91ee` |
