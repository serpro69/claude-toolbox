# Task 9: state, retry and intent fixtures

Four final review scenarios are authored with complete before/after trees, natural
prompts, required workflow assertions and sibling grader-only oracles. IDs 8–11
extend the existing review-code sequence; no seed directory was replaced.

| Case / directory | Demonstrated behavior |
| --- | --- |
| R2 / `functional-retry-lifecycle` | Receipt failure after apply, retry with edited values, and reuse of a completed recovery record by a fresh operation. Both introduced failures reproduce while ordinary tests pass. |
| R4 / `functional-stored-data-compatibility` | The new reader fails on valid legacy rows before migration and after one batch; full migration remains a passing control. |
| R9 / `functional-intent-mismatch` | Normalization drops required transient retries; a new passing test explicitly expects the wrong behavior. |
| R9 companion / `functional-justified-recovery` | Normalization preserves bounded retries, exhaustion and immediate permanent errors; the rubric rejects removing necessary recovery. |

## Verification

[verify.py](verify.py) validates metadata, runs each snapshot's ordinary suite and
grader-side reproductions, stages real Git diffs through the existing helper, and
checks frozen seed hashes. Run from the repository root:

```bash
python3 -B docs/feat/wip/functional-review/verification/task9/verify.py
```

[checks.json](checks.json) records eight passing snapshot suites (18 tests), eight
passing reproduction groups, exact fixture hashes, expected staged paths and 51
unchanged seed files. The verifier and its hidden expectations stay outside actor
trees. Staging excludes wrappers, eval metadata and oracles; future workflow runs
must also filter evaluator content from installed instruction bundles as specified
in the [evaluation contract](../../evaluation.md#bind-the-actual-instructions).

[Repository checks](repository-checks.json) and [logs](logs/) retain all ten passing
shell suites (644 helper assertions, including the 20-test staging suite), Go and
graph checks, generation and a repeat-generation comparison of 785 files. The
existing graph-cycle warning remains visible. Python 3.10.12 ran fixture checks;
installed Python 3.12.11 ran repository suites. This is not a Python version matrix.

## Corrected attempts

The first verifier invocation used a nonexistent I2 seed directory and stopped with
`FileNotFoundError`; the corrected path passes all 51 frozen hashes. Initial
generation encountered the read-only Go cache, then the protected `.codex/agents`
directory. A task-local Go cache and approved generator execution resolved those
environment limits. Its structure check then failed because default Python 3.10
lacked a TOML parser; selecting installed Python 3.12 resolved all seven failures.
The failed and successful generator logs are retained. An initial patch-capture
command used zsh's special `path` variable and failed to find Git; the replacement
uses Bash and an ordinary variable. Neither capture attempt changes repository files.

## Acceptance boundary

These checks establish fixture validity and packaging, not reviewer behavior.
Owner: implementing agent, Task 12. After Task 2 gate 2B and Tasks 10–11, freeze
these fixture/rubric hashes, run both standard and actual isolated workflows twice
per baseline/candidate pair, and grade sealed evidence under the selected contract.
Every required candidate assertion must pass twice. Missing captures, failed
assertions or partial evidence remain open; no threshold or requirement was waived.

[Independent source review](review.md) approved Task 9 after tightening R2's verdict
and remedy assertions and making verifier path/encoding handling explicit. Initial
check hashes are retained in [checks-initial.json](checks-initial.json); the final
checks and repeat generation include the corrections. PAL's limited source coverage
is disclosed in the review record. Task 9 is complete; Task 10 is next.
