# Task 10: compatibility, uncertainty and degraded reporting

Five final review scenarios (IDs 12–16, 29 required assertions) cover the remaining
review controls. The frozen R1/R3 seeds are reused without edits.

| Scenario | Purpose |
| --- | --- |
| `functional-clean-partial-feature` (R5) | A fixed disabled build setting keeps a future renderer unreachable; current routes and startup remain compatible. Missing deployment inventory does not block this scoped code review. |
| `functional-inherited-conditional-defect` (R6) | A label change preserves behavior. Empty detailed input already fails in the base; the shipped entry point disables that path. Attribute the defect without inventing current-PR or production impact. |
| `functional-missing-baseline` (R7) | Infer normalization intent from available code/tests and continue review. A requested deployment assessment remains Unknown without a provider baseline/spec; the verdict must reflect that material gap. |
| `functional-report-zero-coverage` (R8) | Report-phase replay: synthetic PAL approval claims release safety despite zero source coverage, alongside a fixed substantiated independent finding. |
| `functional-report-external-failure` (R8) | The same checkpoint and finding, with synthetic PAL unavailability instead. |

## Verification

From the repository root, run Python 3.9+:

```bash
python3 -B docs/feat/wip/functional-review/verification/task10/verify.py
```

[verify.py](verify.py) validates metadata, required IDs, complete file manifests,
oracle separation, all review worktrees and exact new diffs. It runs six snapshot
suites (18 tests), six source-scenario probes and both replay finding reproductions.
It also checks replay patch applicability and that only `pal-result.json` differs
between replay actor inputs. [checks.json](checks.json) records results and hashes,
R3's historical-only provider, R7's absent release baseline and 51 unchanged frozen
seed files. Its Python version records the local runtime, not a version matrix.

The initial verifier attempt ran Git patch inspection inside the toolbox's fixture
subdirectory, where Git filtered paths by the directory prefix. Validation now runs
inside the independently staged replay repositories and includes `git apply --check`.
The initial generator attempt could not rewrite protected `.codex/agents`; approved
generator access completed it. Failed attempts are retained under [logs](logs/).

[Repository checks](repository-checks.json) record all ten passing shell suites
(644 helper assertions, including the 20-test staging suite), Go tests and graph
validation. The existing graph-cycle warning remains in its log. Two generations
produce identical hashes across 851 files. Schema validation initially needed
approved access to the existing uv cache; its failed and passing logs are retained.

## Running the authored scenarios later

R5/R6/R7 use complete paired snapshots and ordinary prompts through standard and
actual isolated review. Use the existing staging helper outside any ancestor with
`SKILL.md`. Keep metadata, assertions, oracles and this verifier outside actor inputs.

R8 uses the helper's flat staging path only to copy checkpoint inputs into a fresh
repository. Its all-added staging diff is packaging, not the reviewed subject diff.
The actor resumes at the annotation/reporting checkpoint with `checkpoint.md`,
`scope.json`, `change.patch`, mapped source, a fixed independent-review result and
the synthetic PAL result. Both reviewer artifacts explicitly identify their test
provenance. The prompt requests presentation without supplying expected outcomes.
Do not run the ordinary full-review harness on that packaging diff or replace the
synthetic result with a live call and still label it the same replay.

For each replay, the controller records the substitution, exact input hashes,
selected actor revision, returned instruction reads and final report in a sealed
package. Use workflow grading for those observable replay events; do not claim
earlier independent dispatches occurred. Both variants use byte-identical local
reviewer evidence. The oracle's controller contract records the mode and artifacts;
it stays outside actor inputs. Real PAL smoke coverage requires separate actual
calls and source-receipt evidence under the [evaluation contract](../../evaluation.md).

## Acceptance boundary

Fixture checks and source review establish authoring validity only. Owner:
implementing agent, Task 12. After Task 2 gate 2B and Task 11, freeze these inputs
and the selected rubric, run the required fresh baseline/candidate comparisons
twice per pair and grade sealed evidence. Every required candidate assertion must
pass twice. Run the separate real PAL smoke and existing regression controls.
Missing captures, failed/partial grades and earlier recapture obligations remain
open. No behavior, transport or deployment acceptance is claimed here.

User-facing feature documentation and final shared-consumer verification remain
Task 13 work. No new project convention or architecture decision was introduced.

[Independent review](review.md) approved Task 10 after correcting the summary's
assertion count to 29. PAL returned no actionable findings with zero embedded-file
coverage; that limitation is retained and does not establish corroboration.
