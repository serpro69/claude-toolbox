# Capture and grading integrity

Latest status: all 192 captures and grades pass the final integrity and cleanup
audit. The checkpoints below are chronological:
their pending statements describe those earlier checkpoints. See the
[final batch audit](#final-batch-audit) for current capture coverage.

Interim audit, 2026-10-11 11:47 UTC. This is evidence integrity, not behavioral
acceptance. The matrix is still running.

- All 88 completed Claude review captures passed SHA-256 verification of their
  3,996 sealed files.
- All 88 corresponding actor instruction bundles exactly matched their frozen
  side's retained manifest, including modes and symlink targets. Evaluator-only
  paths remain excluded by the bundle verifier.
- All 264 prepared runtime files and each run's Capy configuration still match
  their preparation hashes.
- All 86 saved grades contain every required assertion exactly once and cite
  the matching sealed grading-manifest digest. Their 536 assertion results are
  387 PASS, 147 FAIL and 2 PARTIAL; these are incomplete-matrix totals.

The controller verifies each captured/derived file again when preparing its
grading package. Complete model, material-access, provider-cleanup and final
192-run audits remain pending. No operating-system-wide read confinement or
exact Codex prompt-parity claim follows from these checks.

At 90 completed Claude sessions, every recorded initialization and all 3,633
assistant messages reporting a model identify `claude-opus-5-5`, including
728 messages carrying a parent-tool identifier. A read-only scan of captured
Read/Glob/Grep/Bash requests found no references to controller-repository paths,
source-snapshot paths, grading/oracle/verification directories, retained
manifests or named expected-output files. This is a trace-based targeted audit,
not proof against unobserved access or every possible indirect path.

## Complete Claude capture audit

2026-10-11 12:00 UTC: all 96 declared Claude captures completed with exit code 0.
All 4,382 sealed files, 288 prepared runtime files, 96 Capy configurations and
96 actor bundles passed their integrity checks. Every review-case subject
snapshot matches its initial subject inventory; implementation-case changes
are assessed individually by the graders.

All 97 initialization events and 3,899 assistant messages reporting a model
identify `claude-opus-5-5`, including 758 messages with a parent-tool identifier.
The repeated targeted material-access scan described above found no matches.
No capture, configuration, bundle or model mismatch was found. Codex capture
and final grade-table audits remain pending.

All 96 Claude grade tables subsequently passed the required-assertion and
manifest-digest checks: 608 assertion observations, each required ID exactly
once per run. Totals are 440 PASS / 163 FAIL / 5 PARTIAL across both sides;
the [provider table](claude-results.md) preserves every repetition separately.

The same evaluator-path scan also covers all 228 recorded Claude MCP argument
sets (184 Capy searches, 43 indexes and one execute request), with no matches.
No PAL tool invocation appears in those captures; startup connection failures
and synthetic R8 reports are not live PAL verification.

## Codex administration spot check

The first two measured Codex runs each retain sealed trust, install, uninstall
and untrust records. Every administrative file hash verifies, and neither
completed workspace remains trusted. While candidate R1 standard repetition 1
was active, only its owned project entry and candidate evaluation plugin were
present among this batch's registrations. Final all-run cleanup remains pending.

The first measured isolated Codex run (`codex-baseline-R1-isolated-1`) retains
both thread records: main `gpt-6-astra`/xhigh and child role `code-reviewer` on
`gpt-6.1-sol`/xhigh, linked through the child's `thread_spawn` source. This
confirms the measured role/model binding beyond the earlier loading probes;
the all-run model audit remains pending.

At six completed Codex sessions, 210 sealed capture files, 54 runtime files,
six bundles/configurations and 114 administrative files all verify. All six
main threads use `gpt-6-astra`/xhigh; both child threads use the named
`code-reviewer` role on `gpt-6.1-sol`/xhigh. Review subjects are unchanged and
completed-workspace trust entries are absent. The targeted evaluator-path scan
found no matches across 158 captured shell commands and 22 MCP argument sets.
Only the active candidate run's owned registration was present at this check.

## Cross-workspace trace check

At 109 completed captures, a scan of 3,507 recorded file/shell/MCP requests
found no explicit references to another measured workspace. Nineteen requests
used the batch's parent directory for instruction-file discovery or ancestor
AGENTS.md checks (18 Codex, one Claude). These were scoped filename/ancestor
checks, not reads of another run's subject or result files. The Codex results
contain no foreign workspace paths; instruction-only searches returned no
matches. This check supplements, rather than replaces, the evaluator-path
audit and its stated lack of OS-wide confinement.

## Observed Codex entry-point evidence gap

Some Codex candidate runs, including R3 standard repetition 2, R3 isolated
repetition 1 and I1 plan repetition 1, retain common/profile instruction reads
but no successful SKILL.md read or returned injection establishing that
entry-point load. Their graders retain PARTIAL ordering assertions. Valid
bundle/catalog binding does not fill this per-run evidence gap, nor does absent
delivery evidence prove an actual actor skip. No capture contract or grading
threshold was changed to resolve it. Individual grades identify every instance.

## First 24 Codex captures

2026-10-11 13:11 UTC: all 24 completed Codex captures pass verification of
874 sealed files, 216 prepared runtime files, 24 bundles/Capy configurations
and 456 administrative files. Every binding verifies its operative manifest
and generated role bytes. All 24 main threads are `gpt-6-astra`/xhigh and all
12 children are named `code-reviewer` threads on `gpt-6.1-sol`/xhigh.

Review subjects are unchanged; the targeted evaluator-path scan finds no
matches among 793 shell commands and 116 MCP argument sets. No completed
workspace remains trusted. Only the active baseline R2 standard repetition 1
has an owned project/plugin entry; the candidate evaluation cache is absent.
The baseline cache exists for that active run. No integrity, model or cleanup
issue was found. Implementation-file changes remain subject to their individual
behavioral grades, and final all-run verification is still pending.

All 24 corresponding grade tables subsequently pass the assertion-ID and
manifest-digest checks. These first six case/mode combinations total baseline
59 PASS / 23 FAIL / 0 PARTIAL and candidate 71 PASS / 8 FAIL / 3 PARTIAL across
82 assertion observations per side. They are an interim subset, not the full
Codex result.

## Git-reference integrity

At 124 completed captures, every workspace HEAD still matches its recorded
review base, and all 16 R3 release tags match their recorded release revisions.
The first audit command was blocked before execution because the repository
hook rejected inherited-environment inspection. The successful audit uses
fixed minimal Git subprocess settings and reads no environment data. No actor
input or capture was changed to perform this check.

## Grading-package integrity

At 126 prepared grading packages, all 15,112 manifest-listed files pass their
hash and package-containment checks. Every package uses the same pinned grader
digest `c2621b9a4f2f3e0d86cae6ec682b7ca1a2c729afb5da5cd9031873978b2dc342`
and revision-2 rubric digest
`d2a8b209c109b6f07beaf677d00709dec476288ecb6bbb46103661ab1590cae6`.
All 125 saved tables at that checkpoint contain every assertion exactly once
and cite their correct manifest digest; one independent grade was still pending.

## First 48 Codex captures

2026-10-11 14:26 UTC: all 48 completed Codex captures pass verification of
1,740 sealed files, 432 prepared runtime files, 48 bundles/Capy configurations
and 912 administrative files. Their 48 main threads use `gpt-6-astra`/xhigh;
all 24 child threads are named `code-reviewer` on `gpt-6.1-sol`/xhigh.
Review subjects are unchanged. No targeted evaluator-path reference appears
among 1,537 shell commands and 213 MCP argument sets. Completed workspaces
have no remaining trust entries; only active baseline R6 standard repetition 1
has the batch's owned project/plugin registration.

All 144 completed workspaces retain their recorded HEADs, and all 16 release
tags retain their recorded revisions. Across both providers, all 16,745 files
in 144 grading packages verify against their manifests; grader/rubric pins are
unchanged. The 143 saved grade tables pass every required-ID and digest check;
the final isolated R5 candidate grade was pending. No integrity or cleanup
issue was found. Remaining Codex captures and final audits are still pending.

The first 48 Codex grades are now saved: baseline 109 PASS / 45 FAIL / 0 PARTIAL,
candidate 135 PASS / 15 FAIL / 4 PARTIAL, with 154 assertion observations per
side. This is the completed first-half subset (R1–R5, I1 and I2 in applicable
modes), not the final provider result.

## Review report artifacts

`codex-candidate-R7-standard-1` adds `docs/reviews/settings-client.md` as its
review output. Its sealed inventories confirm no modified or removed initial
subject files. This report-only addition is retained for grading; it is not an
actor repair to the fixture. The final inventory audit must distinguish such
outputs from changes to the original review subjects.

At 135 completed review-mode captures, no initial subject file is modified or
removed. Three Codex candidate R7 runs add only their review reports: standard
repetition 1 (`docs/reviews/settings-client.md`), standard repetition 2
(`docs/reviews/settings-client-staged.md`), and isolated repetition 1
(`docs/reviews/code/settings-client-staged.md`). All are retained grading inputs.

## First 72 Codex captures

2026-10-11 15:28 UTC: all 72 completed Codex captures pass verification of
2,618 sealed files, 648 prepared runtime files, 72 bundles/Capy configurations
and 1,368 administrative files. All 72 main threads use `gpt-6-astra`/xhigh;
all 32 child threads are named `code-reviewer` on `gpt-6.1-sol`/xhigh.
The evaluator-path scan finds no matches among 2,152 shell commands and 266
MCP argument sets. No completed workspace remains trusted; only the active
baseline R9-mismatch standard repetition 1 has an owned registration.

All 168 completed workspaces retain their recorded HEADs, and all 16 release
tags match. The 144 completed review cases modify or remove no initial files.
Five add only reports: the four Codex candidate R7 runs and candidate R8-zero
repetition 1. The additional paths beyond the prior inventory are
`docs/reviews/settings-client-staged-review.md` (R7 isolated repetition 2)
and `review-report.md` (R8-zero repetition 1).

All 18,660 files in 168 grading packages verify, with unchanged grader/rubric
pins. All 166 saved tables at that checkpoint pass the required-ID and manifest
checks; the two R8 failure candidate grades were pending. No integrity, model
or cleanup issue was found. Final all-run verification remains pending.

All first-72 Codex grades are now saved: baseline 148 PASS / 78 FAIL / 0 PARTIAL
and candidate 197 PASS / 24 FAIL / 5 PARTIAL, with 226 assertion observations
per side. This subset ends at the R8 replays; R9-mismatch, R9-recovery, I3 and
I4 remain outside these interim totals.

## Complete review inventory

All 160 review-mode captures are complete. The final sealed-inventory check
finds no modification or removal of any original review fixture file. The only
additions are the same five report artifacts identified above. Implementation
cases remain separately assessed against their allowed edit boundaries.

## Final batch audit

The serial batch exited with status 0 after all **192 captures**, 96 per
provider. All 96 provider/case/mode/side groups contain repetitions 1 and 2;
there are no missing pairs or measured transport/finalization failures.

- All **7,884 sealed capture files**, **1,152 prepared runtime files**, 192 Capy
  configurations and **192 actor bundles/identities** verify.
- All 192 workspaces retain their recorded HEADs; all 16 R3 release tags match.
- The completed Claude model audit records only `claude-opus-5-5`. Codex's
  96 main threads use `gpt-6-astra`/xhigh and all 48 named `code-reviewer`
  children use `gpt-6.1-sol`/xhigh. All 96 Codex binding records verify the
  operative manifest and generated role bytes.
- All **1,824 Codex administrative files** verify. No evaluation project-trust
  or plugin entries remain, and both revision-specific evaluation cache roots
  are absent. Retained snapshots/workspaces are evidence, not active registrations.
- The targeted evaluator-path scan finds no matches in 3,050 Codex shell
  commands and 380 MCP argument sets. The earlier complete Claude scan is
  unchanged. Across **6,513** captured file/shell/MCP requests, no explicit
  foreign-workspace reference appears. The 95 parent-scope requests across 69
  runs are instruction-file discovery or ancestor checks. These trace checks
  do not establish OS-wide read confinement.
- All 160 review runs preserve every initial fixture file; only the five
  report additions listed above appear. Implementation boundaries are graded
  against each case's immutable source/specification expectations.
- All **21,023 files in 192 grading packages** verify, with the pinned grader
  and revision-2 rubric unchanged. All **192 saved tables** contain every
  required ID exactly once and cite their correct manifest digests: **1,216
  assertion observations**, with no missing or duplicate required rows.

The reviewed matrix.py, test_matrix.py and run-contract.md hashes still match
their premeasurement pins. `git diff --check` passes; repository changes remain
limited to the Task 12 execution record and this new evidence directory.
No actor instructions, fixtures, or assertion thresholds changed during the run.
The final controller verification of the frozen fixture/assertion/dependency
set passes. The final results retain 907 PASS / 289 FAIL / 20 PARTIAL across
both sides and providers; these are behavioral grades, not integrity failures.
