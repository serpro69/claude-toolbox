# Task 2 gate 2B: baseline capture completion

The selected receipt/use contract now has all four previously missing Codex
baselines, two R3 isolated runs and two I2 standalone runs. Independent grading
establishes **21 PASS / 9 FAIL / 0 PARTIAL** across their 30 required assertions.
These failures describe the immutable baseline; they are not candidate acceptance.
[Independent review](review.md) approved capture completion with no remaining
blocker. Gate 2B is closed and Task 2 is complete; Task 12 is next.

## Contract and preserved identities

The [bounded investigation](capture-investigation.md) found no supported,
materially different plaintext capture surface. No additional plaintext marker
experiment was run. The user-authorized fallback was selected and frozen before
measurement in the [run contract](run-contract.md), [revision-2 rubric](../task2-rubric-v2.md),
[assertion mapping](assertion-mapping.json) and [freeze](../task2-frozen-v2.json).
Only R3 assertions 7.5/7.6 and I2 assertion 9.5 changed evidence standards.

- Actor baseline remains `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`.
- Original freeze SHA-256 remains `455b8f9977222245382fb80db7c88a714a47cf54fe80ddcf515f58bfafa3ef1c`.
- Revision-2 freeze SHA-256 is `409ac765fcf3ba941211ea23bcc4501c1f2eef1dba83419d4c83c68ee34aacfa`.
- Pinned grader SHA-256 is `c2621b9a4f2f3e0d86cae6ec682b7ca1a2c729afb5da5cd9031873978b2dc342`.
- All 43 subject files and ordinary actor prompts are unchanged; four of 51
  frozen files changed assertion/oracle metadata. Original metadata is preserved
  at Git revision `1c67e55b` and its hashes match the original freeze.
- Original 16 baseline captures, original rubric and Task 8 grades are untouched.
  The new captures bring the seed baseline inventory to 20.

This batch declares Linux, Codex 0.162.1, controller Python 3.12.11, actor-test
Python 3.10.12, and Capy 0.16.8. Actor/reviewer/PAL identities are respectively
`gpt-6-astra/xhigh`, `gpt-6.1-sol/xhigh`, and `gemini-3.1-pro-preview/max`.
Original macOS/Codex 0.161.0 runs are historical evidence; matching comparisons
cannot silently substitute runtimes. [Binding](binding-audit.md) and two fresh
[state probes](state-probe/summary.json) passed before measurement.

## Captures and grades

Every run used a fresh process, subject repository and knowledge state. The
installed 206-file generated cache and baseline role definitions were verified.
Raw manifests retain ordered public parent/child events, actual invocation
identities/results, referenced payload snapshots, and initial/final subject files.

| Run | Raw capture manifest SHA-256 | PASS / FAIL / PARTIAL |
| --- | --- | --- |
| [R3 isolated 1](codex-r3-isolated-1/manifest.json) | `cbf1a352a24ceca6bdbcb3c4df5752c7a6b5327cad1aef23071618bb93791a67` | 5 / 3 / 0 |
| [R3 isolated 2](codex-r3-isolated-2/manifest.json) | `4da0344db700aa43eddcdeaf2443b56eb06fdf4e8211b7a09a87ab78c3923900` | 6 / 2 / 0 |
| [I2 standalone 1](codex-i2-standalone-1/manifest.json) | `705e8d1f8b3b101ebdc35690c1947f4d1cee6218387d03ce684b1efc1491d8c1` | 5 / 2 / 0 |
| [I2 standalone 2](codex-i2-standalone-2/manifest.json) | `3145213ec003ff5224cf2717d2d39be89e6dd70382e501b5019ff388447aa267` | 5 / 2 / 0 |

[Final grades](grades-v2.json) and [independent confirmations](receipt-grade-confirmations.md)
bind every row to the final grading-package manifest. R3 failures concern early
instruction ordering, omitted historical provenance and the missing explicit
`Blocked` verdict. I2 failures concern early investigation, independence between
reviewers, and omitted observable use of attributed verification results.

[Receipt/use calibration](calibration.md) produced the expected PASS, PARTIAL
and FAIL boundaries. [Changed-assertion regrading of retained Claude baselines](prior-grades-v2.md)
produced six demonstrable FAILs and no PARTIALs; those complete-trace omissions
do not require baseline recapture merely to select this rubric. Unrelated old
grades retain their original pin and must not be pooled as one experiment.

## Receipt proof and limits

Public child reads establish named-reviewer source receipt. PAL continuation
history requires a separate receipt check because its final newly-embedded-file
counter can be zero even when history contains source. The first supplement
used the history-inclusion marker alone. Audit found that marker can also
describe formatted read errors; that interpretation was rejected.

The [final supplement](pal-receipts-v2/source-semantics.md) retains 16 sets of
successful-read, successful-formatting and history-inclusion metadata already
emitted during the original calls. Their path, time window, token counts and
read character counts match the sealed payload snapshots. Focused source
excerpts explain the success/error distinction. All four graders reassessed
these stronger packages. The first supplements, summaries and original seals
remain preserved; no actor was rerun or repaired to manufacture receipt.

Exact submitted prompts, byte-for-byte prompt parity and private inherited
context remain unverified. Some named-child verification-result receipt also
remains unknown; independently observed false components establish the baseline
FAILs without pretending those positive components were seen. Task 12 needs
affirmative evidence of every component for a candidate PASS.

Only narrowly allowlisted nonsensitive log metadata was exported. An automatic
approval review rejected full-log processing through Capy; that operation was
not performed. The successful alternative validated selected metadata locally,
with no raw log supplied to an external service or grader. Private reasoning is
excluded and configured credentials are redacted. No OS-wide confinement or
runtime cryptographic digest of the bytes PAL read is claimed.

## Checks, cleanup and remaining work

[Repository checks](repository-checks.json) record 23 new controller/adapter
tests, 15 retained controller tests, all ten shell suites (644 assertions), Go
tests and plugin graph validation. Repeated generation retained identical bytes
across 892 generated files. A final attempt accidentally used Python 3.10 and
failed seven TOML checks because `tomllib` is unavailable; the declared Python
3.12 rerun passed. The failed log is retained, as are initial setup failures.

Initial CLI-scoped project trust did not enable local configuration. Supported
temporary project trust fixed loading before any actor run. Preflight review
also caught the legacy staging helper's revision-1 rubric check; a scoped adapter
was fixed/tested and the premeasurement freeze refreshed before the measured
batch. No measured controller or actor instruction changed afterward. The
refresh guard covers this declared batch's `task2b/codex-*/command.json` paths,
not arbitrary external evidence locations.

[Cleanup](cleanup.json) removed all five temporary trust entries and the
evaluation plugin/cache. Normal kk installation and unrelated configuration
remain intact. Owned temporary subject repositories and public runtime records
are retained for audit and will not be reused as fresh sessions.

Task 12 owns final fixture/grader/candidate freezing, matching baseline/candidate
configuration, affected prior regrading or paired recapture, and two fresh PASSes
for every required candidate assertion. Task 13 owns final feature documentation
and verification. Historical Task 9–11 verifiers retain their revision-1 fixture
pins; current successor validation uses the explicit revision-2 freeze.
