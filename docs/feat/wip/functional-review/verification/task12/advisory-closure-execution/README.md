# Advisory-closure adapter and calibration

> Task: [12.20](../../../tasks.md#task-1220-prepare-the-execution-adapter-and-run-fresh-calibration)
> Status: Task 12.20 complete; adapter frozen, fresh calibration PASS, completion review approved
> Actor comparison, binding/state probes and adoption: unrun

The adapter implements the frozen 64-session comparison without changing its
candidate, fixtures, assertions, model choices or decision rules. Fresh calibration
matched **all 25 controls, all 69 assertion judgments and all 11 conditional-trigger
observations**. Returned totals are **32 PASS / 35 FAIL / 2 PARTIAL**: the FAIL and
PARTIAL judgments are the expected results for negative and missing-evidence
controls, not failed calibration or measured actor performance.

## Source and execution evidence

- [Execution contract](execution-contract.md): authorization, isolation, calibration
  inventory and completion boundary. Only preparation and calibration were selected.
- [Execution freeze](execution-freeze.json): SHA-256
  `edc9cc7798bc3b2f7759a0c707db26abe2ead848bf51b6ec9de8535497a5dd85`.
  It pins the adapter/dependencies, current runtimes, case-specific rubrics,
  source/fixture identities, prompts and calibration inputs. The unchanged
  [preparation seal](../advisory-closure/freeze.json) binds archived historical
  dependencies and both actor sources.
- [Source review](review/source-review.md): APPROVE after resolving dispatch
  provenance, frozen-expectation verification and required Plugin Root gaps.
- [Calibration validity review](review/calibration-review.md): SOUND after fixing
  two absent-advisory reports whose missing evidence limits conflicted with their
  intended outcome. Expected verdicts stayed unchanged. Initial packets and
  earlier dispatch plans remain under `review/`.
- [Checks](checks/): 21 new offline tests, 19 inherited runtime tests and six
  inherited matrix tests pass. The final six calibration tests were rerun after
  the prompt-context correction. Eight offline staging combinations exercise
  both providers, source sides and rubrics without opening model transports or
  writing plugin/trust registrations.

## Calibration provenance and results

[Dispatches](calibration-dispatches.json) retain every exact planned request
submitted verbatim, returned canonical agent identity, workflow mode, prompt and
methodology hashes, public role configuration, packet hash and execution-freeze
hash. Each of the 25 controls used a distinct fresh `eval-grader` with
`fork_turns: none` and configured `gpt-6.1-sol`/xhigh. The method body is pinned
independently of its historical frontmatter. No grader was reused and no control
was retried.

The [dispatch plan](calibration/dispatch-plan.json), controller-only
[expected outcomes](calibration/expected-verdicts.json) and all sealed packets
were frozen before the first call. Each grader received only its controller
instruction path and explicit packet/methodology paths; expectations and other
packets were excluded from its permitted inputs. The results do not claim OS-wide
filesystem confinement, independent read receipts or service-internal model
telemetry. Per-grader raw tool transcripts were not exposed to the parent; exact
tool requests and returned tables are the observed provenance boundary.

[Returned tables](calibration-returns/) preserve the grader responses without
editorial changes (serialized with terminal newlines). [Reconciliation](calibration-results.json)
requires exact assertion coverage, expected verdicts, explicit trigger values,
matching dispatch/request settings and unique return linkage. Standalone verify
also rechecks frozen dependencies and inputs before reading expectations. All
25 results match; no post-result criterion, packet or source change occurred.

| Group | Fresh sessions | Assertions | Matched |
| --- | ---: | ---: | ---: |
| Ordering | 5 | 5 | 5 |
| R6 semantics and conditional triggers | 8 | 28 | 28 |
| Bounded disposition | 12 | 36 | 36 |

Disposition controls establish that the grader distinguishes the permitted
disabled-default omission from missing trigger detail and unsupported claims;
requires final-advisory coverage; and gives demonstrated failure precedence over
another missing capture. These are synthetic calibration observations, not
evidence that the closure candidate improves real review behavior.

## Verification and next action

Use the declared Python 3.12.11 interpreter with its directory first on PATH.
`runner.py verify` checks the execution freeze and runtime identities;
`calibration.py verify` rechecks frozen calibration inputs, dispatches and returns.
`inputs.py` restores from the immutable preparation archives into a fresh owned
input directory; reuse is rejected. The checks require those restored input paths,
whose identity is recorded in the execution freeze.

[Independent completion review](review/completion-review.md) approves with no
findings after reconciling every return and dispatch. The final `SHA256SUMS`
records the completed evidence set; verify it from this directory with
`sha256sum -c SHA256SUMS`. New binding/capture evidence must remain separately
identified and must not overwrite these calibration artifacts.

No binding/state probe, measured actor,
PAL call or runtime registration was performed. The next unrun work is four
provider/source binding probes, two independent Capy state probes, an independent
preflight audit and its sealed attestation. Only then can all 64 measured inputs
be prepared and captured when that work is selected. The adapter refuses capture
without that preflight or with any prior attempt artifact.

Original R6/R7 grades, required report/PAL obligations, legacy controls, unfinished
implementation verification and Task 13 remain open. The existing unrelated
Codex hook-fixture issue retains its prior assignment; this task did not rerun or
claim a green result for the whole repository suite.
