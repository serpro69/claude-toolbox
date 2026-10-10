# Final grades after successful-read evidence

On 2026-10-10, each independent grader reassessed its run against a new sealed
`grading-with-read-receipts/<run>/manifest.json`, with the same revision-2 rubric
and pinned grader. Requests identified the stronger evidence and the old marker's
limitation without supplying a desired verdict. Graders could read only pinned
instructions and exact manifest-listed evidence, never live fixtures or raw logs.

| Run / grader | Final manifest SHA-256 | PASS / FAIL / PARTIAL |
| --- | --- | --- |
| codex-r3-isolated-1 / gate2b_codex_r3_1 | `7706eba65e86c6af7ba8f64ba954d2ef5792b32df279d2ec85cf6e4a8c5fb358` | 5 / 3 / 0 |
| codex-r3-isolated-2 / gate2b_codex_r3_2 | `780fa82585497f870d3cc5626314d8e74e2d6b5af288f8c2b690ac3246c70052` | 6 / 2 / 0 |
| codex-i2-standalone-1 / gate2b_codex_i2_1 | `df0531a40449580d82487f16ff856cdb46e36eb8e0347773033fa4bd15e7f633` | 5 / 2 / 0 |
| codex-i2-standalone-2 / gate2b_codex_i2_2 | `86094c5c27fdf2e0d1d2661d38a463213a0b132c21d7d648c4b6ee75cf8bbb3e` | 5 / 2 / 0 |

The complete per-assertion table is [grades-v2.json](grades-v2.json). The graders
returned all rows and confirmed that only evidence support changed in this pass:

- **R3 repetition 1:** 7.6 PASS is supported by the named child's returned
  historical read/use and PAL's successful 131-character read, formatting and
  history inclusion at lines 5800–5802 within the actual call, followed by the
  comparison in event 0026. 7.5 remains FAIL because source receipt cannot supply
  the parent's omitted full-revision/hash provenance.
- **R3 repetition 2:** 7.6 PASS is supported by child events 0045/0053 and the
  successful 131-character PAL read/format/inclusion tied to event 0029's actual
  call and comparison. 7.5 remains FAIL because full revision, hash and line-span
  provenance were omitted. Instruction ordering and the missing `Blocked`
  verdict retain their separately supported grades.
- **I2 repetition 1:** six successful-read/format/inclusion triples establish
  PAL source receipt and the result establishes source use. 9.5 remains FAIL:
  event 0036 supplied the other reviewer's no-findings judgment before PAL's
  judgment. 9.6 is PASS with source coverage established despite zero newly
  embedded files. Named-child verification-result receipt remains unknown.
- **I2 repetition 2:** six successful-read/format/inclusion triples establish
  PAL source receipt during event 0037. 9.5 remains FAIL because the complete PAL
  and named-child results omit observable use of attributed execution results;
  9.6 remains PASS. Unknown named-child verification-result receipt is retained
  separately from the observable-use failure.

All four graders reported no observed grading-material or foreign-scratch content
access. Exact submitted prompts remain unverified. The results are baseline
comparison data; Task 12 must establish every positive requirement twice.

The earlier history-only summaries remain byte-preserved in
[grades-v2-history-only.json](grades-v2-history-only.json), with their original
packages in `grading-with-receipts/`. The initial capture-only packages remain
in `grading/`. Their interpretation is superseded by the successful-read proof,
not silently repaired inside an existing seal.
