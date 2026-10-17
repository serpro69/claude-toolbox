# Preflight evidence supplied for independent review

> Task: 12.21
> Status: captures and local checks complete; independent disposition pending
> No measured comparison session was launched

All four declared binding processes completed with exit code 0 and unchanged
subject snapshots. The existing execution and calibration freezes still verify.
[Local audit records](preflight-audits/) tie complete returned instruction bodies
to their selected source hashes, runtime models, named child and captured events.
The audit helper checks receipt/model/source obligations; its output explicitly
leaves command-access interpretation to independent review.

| Binding | Observed parent / named child model | Minimum required instruction receipts |
| --- | --- | --- |
| Claude baseline | `claude-opus-5-5` / `claude-opus-5-5` | Registered skill body, three parent common files; child SKILL.md. Baseline agent has no candidate-only common-file requirement. |
| Claude candidate | `claude-opus-5-5` / `claude-opus-5-5` | Registered skill body, seven parent method files and eight detection files; child four common files plus SKILL.md. |
| Codex baseline | `gpt-6-astra` / `gpt-6.1-sol` | Four full source bodies for both parent and linked `code-reviewer`. |
| Codex candidate | `gpt-6-astra` / `gpt-6.1-sol` | Sixteen parent bodies and all five minimum child bodies; the child also reads additional method/detection instructions. |

Claude initialization records the selected filtered plugin root, connected Capy
and no PAL. The successful `printenv TOOLBOX_PLUGIN_ROOT` results match each
workspace's selected bundle. Codex catalog checks verify the selected marketplace,
filtered installed-cache bytes and generated role bytes; thread metadata records
models and parent/child linkage. Codex startup events show Capy ready and the
built-in `codex_apps` service; no PAL startup or invocation is observed. No
application connector call was requested by these probes. Exact submitted Codex
child prompt text remains unverified and no measured-case fallback is extended.

## Deviations and limits requiring interpretation

- The Claude candidate's standard helper created an owned instruction packet at
  `/tmp/kk-review-instructions-c413ove4`, outside the binding prompt's literal
  workspace/plugin path boundary. The actor recognized that location, did not
  read the packet, and used the documented direct-read fallback. Complete direct
  receipts establish the method bytes. This side effect is retained explicitly;
  do not describe the trace as literal compliance with every path restriction.
  Assess whether this prevents the declared source/model-loading readiness gate;
  no source change, acceptance waiver or replacement probe is assumed here.
- Codex baseline has three unsuccessful instruction-metadata searches (two main,
  one child) inside the selected plugin. Subsequent successful reads return every
  required body. These are not missing receipts or a blanket source-unavailable
  result; retain their failed command status rather than claiming every command
  succeeded.
- Captured public events support observed accesses and source receipt, not OS-wide
  confinement or internal service context. Private reasoning is excluded. Parent
  byte/hash checks are attributed execution evidence, not independent re-execution.

## State, retention and cleanup

[Two state probes](state-probe/summary.json) start with distinct empty stores,
index/retrieve their own marker, lack the foreign marker and report the private
vault unavailable. Raw requests/responses and stderr are retained beside the
summary. Neither store/workspace will seed a measured run.

[Runtime retention](preflight-runtime-inputs.json) records 32 verified per-run
configuration/role files in a checked archive. It verifies both Codex admin
sequences and prior trust absence, and confirms the two temporary plugin/trust
entries are absent from the live user configuration afterward. No personal
authentication file or knowledge database is copied. Owned scratch workspaces
and instruction packets remain for existing evidence-housekeeping procedures.

The original controller/auditor attempts and failed read statuses remain visible.
Automatic approval review rejected one attempt to route detailed binding metadata
through Capy because it could export sensitive content. The parent switched to
local audit code and bounded summaries; no blocked metadata export is required
for this preflight. Capy state probes exchange only their declared synthetic data.

`test_preflight_audit.py` passes five decoder controls (complete plain/numbered
returns, truncated content, noncontiguous numbering and wrong source bytes).
`preflight_audit.py` verifies all four capture seals and checked receipts;
`retain_preflight.py` verifies archive recovery and cleanup. These new tools only
inspect/retain completed evidence; they do not alter any frozen controller or
launch a model. Independent source/evidence review precedes the final attestation.
