# Task 12.12: isolated-review entry-path comparison

Declared before binding and measurement. The user requested Task 12.12, then
required the completed assessment to be committed first. Commit `c84fc0f7`
preserves that assessment; this comparison implements only its selected slice.
Live PAL remains explicitly deferred.

## Frozen sources and scope

- Baseline: `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`, unchanged pre-feature actor.
- Candidate: `51cffecec1d912896dfcb4e48dc741f93ea250e1`, committed in the temporary
  source repository, not on the user's branch. [Source provenance](source-provenance.json)
  records its parent export and the sole operative change: the isolated command
  supplies plugin-root paths to its existing skill and workflow. Added words: 2.
- Common methodology remains byte-identical: change context 573 words, functional
  review 1,147 words, within the unchanged 800/1,200 ceilings. No new workflow,
  permission, dependency, retry protocol or guard is introduced.
- All 902 generated Codex files remain unchanged. No fresh Codex run or behavioral
  claim is required for this command-only change.
- Twelve fresh **Claude isolated** workflows: R3 target, R5 clean-increment
  control, R9-recovery justified-complexity control; baseline/candidate, twice each.
  Preserve original ordinary prompts, fixture/oracle bytes, required assertions
  and revision-2 rubric. Historical runs do not replace any declared repetition.

## Runtime and preparation

Match the [full matrix declaration](../opus55/run-contract.md): Claude Code
2.1.296, `claude-opus-5-5`/high for parent and forced child, Capy 0.16.8,
controller Python 3.12.11, actor Python 3.10.12, Linux. Codex 0.162.1 is recorded
by the inherited freeze but not launched. Freeze actual runtime output and all
controller, source, fixture, prompt, rubric and grader hashes in `freeze.json`.
Stop on runtime drift; do not silently substitute a model, policy or interpreter.

Reuse `rework/driver.py`, `capture.py`, `runtime.py`, the original controller and
grading adapter unchanged. The new `runner.py` only selects these twelve isolated
jobs and provides a binding-only prompt; it preserves measured prompts and
transport arguments. Each run uses a fresh disjoint workspace and empty Capy store,
with the private vault unavailable. Actor bundles exclude evaluator material and
retain operative bytes with manifests. Preparing every job precedes the first
measured transport; captures run serially in one owning process with the existing
deadline, interrupt, cleanup, redaction and sealing behavior.

Use the unchanged explicit tool policy and `dontAsk` permissions. Do not enable
PAL or restore its unavailable launcher. No credential or normal plugin/trust
configuration changes are required for the Claude-only workflow. A command denial
is evidence about that attempted command, not every operation of the tool.

Run separate baseline and candidate loading probes before the twelve workflows.
The probe invokes the isolated command, loads its selected instructions, checks
the hook-exported root and requests a named reviewer methodology read. Its exact
prompt is pinned in `runner.py`; probe inputs/results do not seed measured runs.
For the candidate, inspect actual command delivery and returned reads to verify
both substituted paths and selected bundle identity, without global discovery.
An unread path, wrong bundle, unresolved substitution or source investigation in
place of the loading probe is a failed binding gate, not behavioral acceptance.

The [official plugin reference](https://code.claude.com/docs/en/plugins-reference#where-each-variable-resolves)
documents Markdown-body substitution; it supplies design guidance, not proof for
the pinned runtime. Context7 had no exact 2.1.296 documentation version. The
actual loading probe is authoritative for this run.

## Grading, diagnostic disposition and integrity

Use the unchanged grader at `verification/task2b/grader.md`, SHA-256
`c2621b9a4f2f3e0d86cae6ec682b7ca1a2c729afb5da5cd9031873978b2dc342`, and revision-2
rubric. Fresh independent `eval-grader` roles use declared `gpt-6.1-sol`/xhigh
with no actor/authorship history and only manifest-listed sealed inputs. Exact
service telemetry is unavailable. Preserve the applicable
[ten-control calibration](../opus55/calibration.md); unchanged grader/rubric and
adapter semantics retain its validity. Any grading-contract change requires
prospective versioning, calibration and affected-pair treatment before use.

Grade every original assertion. PAL-dependent assertions remain FAIL while PAL
is absent. R3 7.5/7.6 retain the existing receipt/use exception; no new exception
or exact-prompt-parity claim is introduced. Separately inspect each local component
of those composite failures. Do not relabel an aggregate FAIL as a diagnostic PASS.

Keep the correction only if both R3 candidates establish every non-PAL component,
including historical source and named-reviewer receipt/use, and both repetitions
of each control retain ordering/coverage, R5 scoped approval and R9's required
recovery mechanism. Reject/revert if discovery or early stopping persists, target
components remain unmet, controls regress or the cost bound is exceeded. A failure
ends this bounded iteration; retain attempts and return to assessment rather than
launch another candidate. This diagnostic disposition does not complete Task 12
acceptance or waive any legacy/final gate.

Verify original/derived seals, frozen inputs, subject and bundle identity, actual
reviewer linkage and targeted tool-access traces. Remove only proven-owned runtime
temporary artifacts after their evidence is retained. No OS-wide read confinement
or statistical reliability is claimed. Owner: implementing agent, Task 12.12.
