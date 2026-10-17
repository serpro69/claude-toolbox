# Advisory-closure preparation

> Task: [12.19](../../../tasks.md#task-1219-freeze-the-closure-candidate-and-review-its-comparison-contract)
> Date: 2026-10-17
> Status: candidate and criteria frozen; independent reviews approved; execution unrun

The [run contract](run-contract.md) declares 64 fresh sessions and 464 original
assertion rows for R6D, R6M, R5 and R9 recovery across both providers and review
modes. Its KEEP / REJECT / INCONCLUSIVE rules govern a bounded candidate-selection
decision; all original grades and full-feature acceptance obligations remain intact.
The user selected preparation only. No actor, evaluation-grader, binding or state
probe was launched, and no normal plugin/trust registration was changed.

## Frozen inputs and provenance

- Baseline: `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`.
- Candidate: `4b69421465131e2e9e497f200ec9ddbdb439ac83`, created only in a temporary
  source repository from parent `11b2c6efb0638605bb6acd3eb184edb9abd10f56` plus
  the four reviewed closure files. [Provenance](source-provenance.json) and
  [patch](candidate.patch) preserve that construction; working HEAD/staged content
  remain unchanged. The three source trees, not an entire repository checkout,
  are represented by the candidate's synthetic commit.
- Six compressed archives preserve full source, filtered actor trees, evaluation
  inputs and existing controller sources. Full source includes evaluator material
  and must never be supplied to an actor. Only `*-retained.tar.gz` contains actor
  runtime trees; stage subject fixtures separately from their `test-files` inputs.
- Source and retained manifests preserve hashes, modes and links. The filtered
  baseline has 435 files; the candidate has 447. Evaluation inputs contain 159
  files; the existing controller-source archive contains 17. Neither old runner
  is a ready adapter for this new comparison.
- [matrix.json](matrix.json) pins prompts, identities and every job;
  [runtime.json](runtime.json) records observed client/interpreter identities and
  declared model settings. Actual model binding remains unverified.

[freeze.json](freeze.json) seals the preparation inputs, review records and checks.
From this directory, `sha256sum -c SHA256SUMS` verifies all sealed files, including
the freeze record. Keep the checksum list with the committed/archive record; it is
an integrity manifest, not an access-control or signed-attestation mechanism.

For recovery, verify checksums first and use fresh controller-owned destinations.
Restore retained archives with permission preservation, for example
`tar --no-same-owner -xpf candidate-retained.tar.gz -C <fresh-directory>`.
Use the existing `verification/prepare-bundles.py verify` command against each
restored `retained/<tree>` and the corresponding retained manifest. Decompress
`*-source.tar.gz` to `source.tar` when an inherited controller needs that layout;
its uncompressed digest is in the side's identity JSON. Keep all manifests,
unfiltered source and grading archives outside actor-visible catalogs/workspaces.

## Verification and independent review

[checks.json](checks.json) records successful source/member hashes, file modes,
symlink targets, retained recovery/filter checks, exact four-file candidate delta,
evaluation/controller member comparisons, all prompts and the 64/464 inventory.
A deliberately modified recovered instruction was rejected by the existing
bundle verifier. Generated closure copies match canonical bytes. HEAD remains
the source parent and the staged diff remains empty.

The first recovery attempt exposed Python's safe extraction normalizing group-write
bits. The successful check compared archive members first, then restored only
verified regular-file modes before matching the retained manifests. No archive
bytes changed. An earlier preparation command was blocked before execution by a
repository hook; the successful construction used an explicit Git-only environment.

[Design review](review/design-review.md) found one P2 ambiguity in 22.4's tolerated
omission. The corrected component mapping and calibration examples resolve it;
the final assessment is SOUND. [Source review](review/source-review.md) approves
preparation with no findings. Both distinguish parent-executed integrity checks
from independent source/document inspection. PAL remains user-deferred; neither
review establishes external corroboration or behavioral acceptance.

The Task 12.18 source checks remain applicable because operative bytes did not
change during preparation. Its unrelated Codex hook-fixture failure remains
[assigned](../r6-validity/README.md#environment-attempts-and-unrelated-test-follow-up);
these archive checks are not a fresh full-repository test run.

## Next action and completion boundary

Task 12.19 is complete as source/criteria preparation. The implementing agent owns
the next execution-preparation work when measurement is selected: implement and
review the successor adapter, freeze its execution dependencies, freshly calibrate
the grader/disposition checks, run four binding and two state probes, and seal a
passing preflight before preparing/capturing the 64 sessions. See the contract's
ordered gates. Do not launch either historical runner unchanged.

The final preparation freeze is immutable input to that later execution freeze;
changes require a separately identified reviewed successor, preserving this record.
No KEEP decision, causal improvement, completed case acceptance, PAL capability,
legacy-control pass or Task 13 completion follows from this preparation.
