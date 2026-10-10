# Task 12: comparison execution — acceptance failed, work remains

Task 12 remains **in-progress**. Fifty-eight measured Claude captures have sealed
evidence and independent grades. The latest [candidate-6 R5 follow-up](candidate6/results.md)
passes **11 of 12 assertions**: both candidate reviews avoid unnecessary work,
but one still investigates source before loading all instructions. The two-run
gate remains unmet. Candidate 5's R1/R3 passes remain tied to that earlier source.
The full matrix, Task 13 and feature acceptance remain open.
The user directed that PAL-based verification be ignored for now; this exception
does not waive other behavioral requirements.

## Retained experiments

The [original contract](run-contract.md) fixes the runtime, model, fixture,
grader, baseline and evidence policy. [Preflight](preflight.md) preserves failed
and successful binding attempts, the resolved approval rejection and fresh-state
probes. [Grader calibration](calibration.md) preserves all workflow controls and
both legacy component-mode checks.

| Candidate | Source revision | Measured captures | Results |
| --- | --- | --- | --- |
| 1 | `4fb1941779f6b24dbed4440c288f1d901f0c4609` | 8, both sides of R1-standard/R3-isolated | [R1](r1-candidate1-grades.md), [R3](r3-candidate1-grades.md) |
| 2 | `174cbb3ff5fb5b0647082705b9bba7ef07986bee` | 0; binding only | [Declaration](candidate2/run-contract.md) |
| 3 | `f7bbcc81c4760167d38622d9b698c2b2da54e5d9` | 20, both sides of R1/R2/R4/R5/R6-standard | [Results and evidence references](candidate3/results.md) |
| 4 | `cde36b8239de1fc1e10e589e969e6613668aa26c` | 14: twelve candidates plus two R3-standard baselines | [Results and evidence references](candidate4/results.md) |
| 5 | `be1a283cf872ec97fe569c9fd481bbe623cc8214` | 12 fresh baseline/candidate R1/R3/R5-standard captures | [Focused diagnostic results](candidate5/results.md) |
| 6 | `ab7daa7f2833abefc64dedc08e8e44790ce5a0ee` | 4 fresh baseline/candidate R5-standard captures | [R5 follow-up results](candidate6/results.md) |

Candidate 4 reuses both matching baseline repetitions from candidate 3 for five
cases, as declared before measurement. Those ten reused runs are not counted
again in the 42 original captures. Candidate 5 adds twelve fresh captures under
the reviewed successor runner, without reusing earlier baselines. Candidate 6
adds four fresh R5 comparisons with the same runner and unchanged rubric. These are
iterative development observations, not accepted cells of the full matrix or a
reliability estimate. All failures
and partials remain; earlier candidate successes cannot satisfy latest-source
acceptance. Candidate 1's two isolated candidate runs are invalid for acceptance
because they shared temporary evidence paths.

Baseline remains `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`. Exact source archives
and identity/filtering manifests are retained in `baseline-bundle/`,
`candidate1-bundle/`, and each later candidate's `bundle/`. Candidate 2–6 commit
identities belong to temporary source repositories; they do not identify commits
in the main repository. Frozen controllers and previous evidence have not been
rewritten.

## Source corrections and review

The working-tree draft strengthens complete profile detection, reads component
contracts before diff analysis, traces initial/intermediate/final states, checks
fixes against existing invariants, calibrates severity to demonstrated impact,
avoids redundant or hypothetical recommendations, and grounds coverage claims
in successful tool results. Canonical instructions and generated Codex output
match. The common method is now 1,147 words against the 1,200-word budget.
Candidate 5 additionally consolidates instruction preparation into complete
source packets and uses a compact contract/scenario record. These changes have
scoped source approval; the R5 failures remain visible.
Candidate 6 conditionally closes clean reviews without a remediation menu and
separates early diff selection from later task-scope investigation. Its
[source review](candidate6/review.md) approves the change; the instruction-order
failure remains open despite both clean-closure checks passing.

[Independent source review](review.md) approved the instruction changes and
earlier preparation-integrity fixes. The original controller review is
**REQUEST_CHANGES**, with three open findings: abandoned background captures on
preparation failure, lost actor-runtime exit status, and PAL-probe cleanup that
can skip sealing. No new capture should use these runners before the first two
are repaired. PAL-probe correction can be tested offline and is required before
that deferred probe is used again. Source approval and static checks do not
override the behavioral failures or these open findings. The subsequently
approved [successor runner](rework/README.md) fixes those execution paths while
preserving old controller bytes. It was used for candidates 5 and 6; the original
runners remain historical artifacts and should not launch new captures.

## Verification and evidence limits

[Static logs](checks/) retain ten passing shell suites (644 assertions), twenty
staging tests within the shell-suite wrapper, twelve controller tests, passing
Go tests, graph validation and generation checks. Graph validation reports its
existing cycle warning and no broken edges or orphans. Generated file hashes
match before/after regeneration. The instruction/task diff passes
`git diff --check`. Checking all staged evidence also flags space indentation
under the configured `indent-with-non-tab` rule and captured formatting;
sealed evidence is preserved byte-for-byte. These checks do not cover the
originally reported subprocess/finalization defects. [Successor checks](rework/checks/)
add eighteen capture/evidence tests, nine packet tests, eleven passing shell
suites, Go/graph checks and stable regeneration across 902 generated files.

The [final integrity audit](integrity-audit.json) verifies 1,924 capture-file
hashes, 5,252 grading-file hashes, all 42 capture-to-grading manifest links, and
all 42 post-run actor bundles against their declared retained manifests. Every
measured actor runtime exited zero; behavioral FAIL is distinct from runtime
failure. A limited tool-input scan found no listed evaluator-material path
tokens. This scan is not the full event-level material-access audit required
before acceptance, and no OS-wide read confinement is claimed. Runtime-emitted
instruction messages remain in raw streams even where derived views omit them.
Exact submitted reviewer prompts and parity remain unverified under revision 2.

Nine files proven to belong to the isolated actors were archived in
`retained-scratch/` and removed from their shared temporary paths; no unrelated
files were removed. Captures, actor workspaces and immutable source snapshots
remain for audit. This task made no Codex marketplace/trust registrations.
Candidate 5 has its own [integrity](candidate5/integrity-audit.json) and
[access](candidate5/access-audit.json) audits, covering all twelve new captures,
their packet receipts and all 67 shell requests. Nineteen uniquely owned packet
directories (79 files) were verified and removed; sealed copies remain.
Candidate 6's [integrity](candidate6/integrity-audit.json) and
[access](candidate6/access-audit.json) audits cover all four fresh captures,
complete packet receipts and all 22 shell requests. Seven owned packet
directories (31 files) were verified and removed; sealed copies remain.

## Stop and continuation

The loaded /kk:implement skill says “STOP executing immediately when”
“Verification fails repeatedly.” Repeated candidate failures triggered that
stop. No further model actors were launched; final grading, integrity checks and
durable reporting were completed. The user was asked whether to rework the
workflow design or leave the failed gate recorded. No redesign or threshold
change is assumed from silence. The user then explicitly accepted focused rework.
[Candidate 5](candidate5/results.md) completes that twelve-run diagnostic with
R1/R3 passing twice and R5 still failing. The user then agreed to an R5-only
follow-up and requested a commit first. Commit `17344213` preserves candidate 5;
[candidate 6](candidate6/results.md) completes the accepted four-run follow-up.
Both clean-closure checks pass, but one preparation-order failure remains. No
broader matrix or further candidate was launched after this failed gate. The
candidate-6 follow-up edits and evidence remain uncommitted.

Owner for all remaining work: implementing agent, Task 12.

| Remaining work | Reason | Next action and verification condition |
| --- | --- | --- |
| R5 preparation order | Candidate 6 passes both clean-closure checks but still investigates source early once. | Define a separate approach to establish instruction completion before source access, freeze any successor and obtain two full R5 PASSes before expansion. |
| Remaining R1/R2/R3/R4/R6 standard and other matrix coverage | Candidate 6 only measures R5 standard; earlier-source passes do not establish latest-source acceptance. | After the diagnostic gate passes, complete the required fresh comparisons without pooling obsolete candidate results. |
| Latest-source isolated and implementation cases, R7/R9 | Full required matrix has not run. | Use fresh disjoint state, retain all attempts and satisfy each case/mode twice. |
| Codex representative checks and legacy routing/pre-write actor controls | No Task 12 captures for these gates. | Run matching declared baseline/candidate pairs and independently grade under the pinned contract. |
| Material-access, scratch and handoff audits for remaining runs | Candidates 5 and 6 are audited; the full matrix is incomplete. | Audit actual tool events and source receipt/use for each remaining run; invalidate contaminated runs and recapture. |
| R8 PAL-report replays, PAL receipt/corroboration and live integration | Temporarily user-deferred after missing API configuration. | When resumed, use the reviewed successor probe, restore the declared runtime, verify startup and actual receipt/use; preserve currently missing evidence as missing. |
| Task 13 documentation/final acceptance | Depends on Task 12. | Start only after required gates pass or their scope is explicitly revised. |
