# Task 12.13: R7 conclusion consistency

**Disposition: reject the candidate; operative wording reverted.** All 48
declared sessions completed with exit code 0; all 336 assertions are graded and
integrity/cleanup checks pass. [Independent completion review](completion-review.md)
approves the rejection record with no findings. R7 and full-feature
acceptance remain open. No successor actor iteration is selected.

Both Claude standard R7 candidate repetitions still fail 14.3 and 14.4. The
[first report](grading/claude-candidate-R7-standard-1/captured/report.md) calls
provider compatibility Supported despite not having the provider contract, then
offers full approval if callers accept only strings. The
[second report](grading/claude-candidate-R7-standard-2/captured/report.md) similarly
ends with conditional deployment approval. Both received the candidate
instructions; source checks passing did not establish the desired behavior.
The [frozen keep criterion](run-contract.md) requires both repetitions in every
provider/mode to retain the evidence qualifications.

The three wording replacements and generated copy are restored to starting
`cc07a614a999e8f35e2f408a505546077154031f`. The previously kept Task 12.12
correction remains. [The rejected patch](candidate-method.patch),
[source provenance](source-provenance.json) and [source archives](source-inputs/)
preserve the attempt.

## Comparison and grading

The prospective comparison uses unchanged R7/R3/R5, both modes/providers and two
fresh repetitions per side: 48 sessions. Baseline is
`c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`; candidate is
`bf873de63369662ebe3b0cde4226dbda1c16104b`, a temporary commit built from the
starting source plus the two method-file replacements. There is no commit in the
working repository.

Claude 2.1.296 uses Opus 5.5/high; Codex 0.162.1 uses gpt-6-astra/xhigh and named
gpt-6.1-sol/xhigh reviewers. Capy 0.17.0, controller Python 3.12.11 and actor
Python 3.10.12 are declared before measurement. [All four loading probes](binding.md)
and [independent binding review](binding-review.md) pass. [Ten fresh grader
controls](calibration/README.md) match all 14 expected verdicts.

[Effective results](results.md): candidate **147 PASS / 21 FAIL / 0 PARTIAL**;
baseline **95 PASS / 72 FAIL / 1 PARTIAL**. Sixteen candidate failures are required
PAL omissions, four are the Claude R7 target failures, and one is the Codex R3
parent-report gap (explicit Blocked omitted despite identifying incompatibility).
Every original assertion retains the revision-2 rubric. PAL remains user-deferred
and its required omissions FAIL. Exact Codex child prompts remain unverified;
only the already declared R3 receipt/use fallback applies here. Fresh independent
graders use sealed evidence. [Two explicit grading corrections](grade-corrections/README.md)
fix confusion between grader-display truncation and complete actor receipts;
original grades and follow-up messages remain preserved.

This comparison uses the pre-feature baseline, so it does not isolate the
incremental effect of these 28 added words. Two repetitions are descriptive
evidence, not a reliability estimate. No historical grades are rewritten.

## Local verification and retained evidence

The candidate common method was 1,175/1,200 authored words; shared context stayed
573/800. [Source review](source-review.md) and [controller review](controller-review.md)
approved their source scopes. Controller review corrected an impossible
baseline-loading requirement before launch; both original and corrected
contract/freezes remain retained.

Generation, Go tests, graph validation, 19 inherited capture regressions, four
adapter controls and the real Capy state-isolation probe passed. The existing
graph cycle warning remains; there are no broken edges or orphans. A second
candidate generation preserved 902 tracked generated files. After rejection,
[restoration checks](checks/restoration.md) confirm operative/generated files match
the starting HEAD. The default Python 3.10 structure run lacked `tomllib`;
rerunning with the declared Python 3.12.11 passed without installing a dependency.

[Integrity checks](integrity-audit.json) verify 2,001 capture files, 5,350 grading
files, every assertion identity, frozen inputs, all 48 bundles, subject bytes,
Git refs, runtime inputs and model receipts. [Cleanup](cleanup.json) archives 311
files and verifies absence of 94 proven-owned temporary paths, including paths
already removed by actors. An unproven parent directory remains untouched.
Temporary plugin registration, project trust and cache directories are absent.
[Final workspace cleanup](workspace-cleanup.json) reverified archived runtime
inputs and final subject snapshots before removing all 52 actor workspaces.
Frozen source snapshots remain locally available; their archives are retained here.

[Runtime inputs](runtime-inputs.json) for all 52 measured/probe workspaces are
archived and verified. [The access audit](access-audit.json) covers all measured
tool/lifecycle records. Some instruction-filename discovery extends into ancestor
directories; no evaluator-content read was observed. This is not OS-wide read
confinement. Codex starts its builtin Apps server, but no Apps calls were observed.

## Launch block and next action

The initial Claude binding command was rejected by automatic approval review
before process creation because authorization for exporting instruction/fixture
content to the authenticated runtime was not explicit enough. No actor launched
and no alternate launch path bypassed that rejection.

The user then answered **"proceed"** to the request naming synthetic fixtures,
filtered instruction bundles, authenticated Claude/Codex destinations, loading
probes and the 48-run comparison with PAL excluded. This resolved that block;
all four probes and all 48 captures ran under the unchanged corrected freeze.

The candidate is rejected and Task 12.13 is complete as an experiment. There is
no launch to resume; select any further R7 investigation separately. Task 12 acceptance,
other assigned dispositions, live PAL, legacy controls and Task 13 stay open.
