# Full functional-review rerun on Opus 5.5

Declared 2026-10-11 before measured sessions. User authorization: rerun the full
functional-review matrix on Claude and Codex, all applicable modes, twice per
baseline/candidate. The user retained the PAL deferral and upgraded Claude Code
after the old version rejected Opus 5.5. This supersedes the historical narrow
diagnostic/ordering-probe scope. It authorizes measurement, not actor repairs.

## Frozen comparison

- Baseline `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`.
- Candidate `581dd0e11455398cb73e3d6ae5542854c016fe7f`.
- Both providers receive complete coverage: R1–R7 and R9-mismatch/R9-recovery
  in standard and isolated modes; R8-zero/R8-failure in report replay mode;
  I1/I4 plan mode and I2/I3 standalone mode. This is 24 combinations × two
  providers × two sides × two repetitions = **192 measured sessions**.
- Ordinary eval prompts and fixtures remain unchanged. R8 replays are explicitly
  synthetic report checkpoints, not live PAL integration or full investigations.
- Freeze complete fixture/oracle/prompt hashes, filtered source/generated bundle
  identities, controller dependencies, runtime versions, this contract and the
  declaration before measurement. No historical run substitutes for a fresh run.
- Every required assertion remains required. All must PASS twice for candidate
  acceptance; FAIL/PARTIAL/unrun and PAL-deferred components never become PASS.
  Report behavioral results even if failures prevent feature acceptance. Do not
  iterate actor instructions or change thresholds during this requested rerun.

## Runtime and execution

Claude Code **2.1.296**, main and forced reviewer `claude-opus-5-5`, high effort;
the reviewed successor transport pins `CLAUDE_CODE_SUBAGENT_MODEL` and its force
flag. Codex **0.162.1**, main `gpt-6-astra`/xhigh with provider-model fallback
disabled; generated role bytes remain immutable (code reviewer and grader
`gpt-6.1-sol`/xhigh). Capy **0.16.8**, controller Python **3.12.11**, actor Python
**3.10.12**, Linux. Preserve resolved models and actual runtime errors in traces.

Fresh filtered bundles and repositories for every run; fresh empty Capy store
and private unavailable session vault. Probe workspaces are never measurement
seeds. No controller/oracle paths in actor prompts or catalogs. Capture public
tool events and artifacts, omit private reasoning, redact configured secrets,
then seal outside actor inputs. Audit receipt/use and material access afterward;
no OS-wide read confinement or exact Codex prompt-parity claim is made.

Actors execute serially to avoid shared temporary-path collisions. Prepare the
entire core matrix before measurement. Claude retains the reviewed explicit
tool policy/dontAsk/hooks/strict MCP/plugin-dir/registry capture. Its configured
PAL launcher remains unavailable; no restoration or live verification is
authorized. Codex explicitly disables PAL and unrelated MCP services, retains
workspace-write/never, and uses temporary trusted projects and revision-specific
local plugin installations. Record prior absence and remove only owned trust
and plugin entries, preserving the normal installation and unrelated settings.

Separate binding probes for both sides/providers precede their measurements.
Claude captures have the existing 30-minute deadline. Codex uses the retained
45-minute overall/120-second event deadline with interrupt-aware polling and
owned process-group cleanup. Runtime errors stop that batch, are retained, and
require an explicit successor attempt; successful runtime completion says
nothing about behavioral correctness. Never silently skip or overwrite attempts.

## Grading and reporting

Unchanged [revision-2 rubric](../../task2-rubric-v2.md), final assertions, and
[pinned grader](../../task2b/grader.md), SHA-256
`c2621b9a4f2f3e0d86cae6ec682b7ca1a2c729afb5da5cd9031873978b2dc342`.
Use independent fresh eval-grader roles, declared `gpt-6.1-sol`/xhigh, with only
manifest-listed sealed evidence and pinned grading instructions. Calibrate
positive/negative/missing-event and receipt/use controls before grading pairs.
Preserve grader dispatches and every assertion result. R3 7.5/7.6 and I2 9.5
alone use the versioned receipt/use fallback; exact submitted prompts remain
unverified. PAL-deferred portions are separately identified, never waived.

The 192 core sessions are reported separately from legacy routing/pre-write
controls, loading probes, offline tests and grading calibration. Legacy controls
remain a separate Task 12 gate; the requested full functional matrix does not
stand in for them. Task 13 and feature acceptance are not implied by capture
completion. Owner of any unrun/failed gate: implementing agent; durable results
must state the reason, next action and verification condition.
