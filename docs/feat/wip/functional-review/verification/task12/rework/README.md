# Focused rework after candidate 4

The user accepted focused rework after commit `87a26bb7`: repair capture
ownership, reduce instruction-navigation failure, preserve substantive review
requirements, and try R1/R3/R5 before expanding. PAL verification stays deferred.
This continuation supersedes the preceding stop for this bounded experiment.

## Successor runner

As of 2026-10-11, new captures through `driver.py` explicitly select
`claude-opus-5-5` with high effort. The command and prepared launch metadata use
the same model constant in `capture.py`; other launch flags are unchanged.
Subagents are pinned to the same model through `CLAUDE_CODE_SUBAGENT_MODEL` and
`CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`, recorded in `command.json`. This overrides
older model declarations in frozen baseline agents without changing their bytes.
The [documented override](https://code.claude.com/docs/en/sub-agents#run-every-subagent-on-one-model)
requires Claude Code 2.1.257 or later; the declared 2.1.272 runner meets that floor.
The runner pins its model rather than inheriting the repository setting.
Historical seed controllers and candidate-5/6 captures still record their actual
`claude-opus-4-8[1m]` model. Use a new declaration/run contract and freeze for the
updated runner, with fresh baseline/candidate runs and model binding checks;
existing freezes intentionally reject changed controller bytes.

Historical controllers and freezes remain unchanged. `driver.py` reuses their
input preparation and launch guards while binding new transport/runtime bytes
and the declaration into a successor freeze. Batch preparation finishes before
any capture; actors run serially. A nonzero model exit, missing completion,
timeout or interruption cannot become batch success merely because evidence was
sealed. Behavioral FAIL with runtime exit zero remains valid captured data.

Signal handlers record interruption without raising during resource acquisition
or sealing. The Linux stream reader observes process exit with `waitid(WNOWAIT)`
and cleans the owned process group before reaping the leader; this prevents a
surviving descendant and avoids signalling a recycled leader PID. Stdout EOF
does not shorten the declared runtime deadline. The platform boundary is
intentional: the new adapter targets the already-declared Linux batch, not the
historical macOS runs. Python 3.12 signal/subprocess/waitid semantics were checked
against versioned standard-library documentation before writing these calls.

The successor PAL probe attempts event recording and sealing even if buffered
stdin closure fails, preserving the primary exception. Interruption stops its
owned server and prevents later requests. Only dummy-process tests were run;
live PAL startup and integration remain deferred.

## Instruction preparation and reporting

The plugin helper packages original common instructions, every Known-profile
detection rule, active indexes and selected checklists into bounded parts.
It reads no subject source and evaluates no detection predicates. It rejects
incomplete index decisions, skipped always-load files and instruction paths
escaping the plugin or resolving into evaluator directories. The actor must
Read complete returned parts before investigation; creation and hashes alone
never open the checkpoint. Read-only agents retain direct source loading.

The unchanged grader accepts successfully returned instruction bytes, and the
unchanged adapter preserves packet tool results and linkage. A new adapter test
establishes this representation compatibility. Captures additionally retain
requested packet parts with explicit unverified receipt labels; actual Read
results remain authoritative. No hook-enforced compliance is claimed.

The functional method now uses a compact contract/state/transition/result/evidence
record. Conflicting prompts to recommend speculative extra work were removed.
All existing assertions and the revision-2 rubric remain required and unchanged;
failure classifications are diagnostic summaries only.

The 2026-10-11 review follow-up restores concrete steps and proportionate
validation checkpoints for warranted removal recommendations. The evidence
threshold and protection for pending scaffolding remain in place.

## Offline verification and independent review

The 2026-10-11 model/removal follow-up passes all eleven shell suites, nineteen
successor runner/evidence tests, twelve historical-controller tests, generation
and graph checks. All 902 generated entries match regeneration. No live model
evaluation was run for this follow-up; the behavioral gates below remain open.

- All eleven `test/test-*.sh` suites, Go tests, plugin graph and twelve historical
  controller tests pass. New packet tests cover nine cases; successor and packet
  evidence tests cover eighteen cases. Logs are retained under [checks/](checks/).
- Two generation passes preserve all 902 generated file hashes. The common
  functional method is 1,147 words, within its unchanged 1,200-word budget.
- Independent reviewer `/root/review_runner_rework` approved runtime helpers and
  driver integration after correcting descendant cleanup, post-EOF deadline and
  pending-probe interruption issues. A separate final review approved the
  packet-capture addition after its bounded-read correction; no findings remain.
- Independent reviewer `/root/review_packet_rework` approved sixteen scoped
  canonical/test files and checked generated parity after the resolved-symlink
  exclusion fix. Reviewers inspected source; passing test counts are parent
  execution evidence. No PAL corroboration is claimed.

The initial unmeasured candidate-5 controller freeze and original capture helper
bytes are retained as `candidate5/preflight-freeze.json` and
`candidate5/preflight-capture.py.txt` one directory above, before correcting the
packet read-allocation bound. No actor ran under that freeze.

## Behavioral checkpoint

Both binding probes pass. All twelve paired diagnostic captures are graded and
audited under [candidate 5's declaration](../candidate5/run-contract.md).
[Results](../candidate5/results.md): candidate 37 PASS / 3 FAIL, baseline
20 PASS / 18 FAIL / 2 PARTIAL. R1 and R3 pass twice; R5 still fails preparation
ordering once and recommendation scope twice. The failed checkpoint prevents
expansion. Task 12 and feature acceptance remain open.
