# Task 12 comparison contract

Declared 2026-10-10 before this batch's probes or measurements. The user's
request to execute the next functional-review task authorizes Task 12.

## Fixed identities and acceptance

- Baseline: `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`.
- Candidate 1: `4fb1941779f6b24dbed4440c288f1d901f0c4609`.
- Primary provider remains Claude Code; secondary remains Codex.
- Claude 2.1.272, main `claude-opus-4-8[1m]`, effort high; named reviewer
  uses the selected revision's unchanged role declaration and inherited effort.
- Codex 0.162.1, main `gpt-6-astra`/xhigh, named reviewer
  `gpt-6.1-sol`/xhigh. PAL `gemini-3.1-pro-preview`/max. No model fallback.
- Linux; controller Python 3.12.11, actor-test Python 3.10.12, Capy 0.16.8.
- Two independent fresh baseline and candidate runs per case/mode. Every
  required candidate assertion must PASS twice. FAIL/PARTIAL/unrun stay open.
  No statistical reliability or untested-provider parity claim.

The core matrix comprises 112 runs: Claude's nine review scenarios (R1–R7
and both R9 variants) in standard and isolated modes, four implementation
scenarios, two R8 report replays, and Codex's R1-standard/R3-isolated/I1-plan/
I2-standalone representative set; each on both sides with two repetitions.
Run existing five review routing controls in standard mode and eight implement
pre-write controls in their fixture mode on Claude, with the same two-run rule
(52 additional runs). A successful real isolated run with verified PAL receipt
may also supply the integration smoke evidence; R8 never supplies that evidence.

## Evidence and isolation

Use the unchanged Task 1 bundle builder on the exact commits. Keep source
archives, exclusion/retained manifests, fixtures, oracles and results outside
actor inputs. Verify retained bytes, symlink boundaries and generated role
bytes before launch. Freeze all fixture/metadata/oracle bytes, ordinary prompts,
controller dependencies, the rubric and grader before measured runs. Probe
prompts may test loading but never seed measured state or hint at defects.

Reuse the existing capture/staging mechanisms through a bounded Task 12 adapter;
do not rewrite old captures or controllers. Each run owns a fresh repository,
absent Capy store and private unavailable vault; no real history or probe state
is inherited. Audit observable reads for evaluator-material leakage. No OS-wide
read confinement is claimed. Preserve private-reasoning exclusion and credential
redaction. Declared runtime changes require new matching pairs; original results
remain historical evidence, including gate 2B baselines.

Claude retains the seed controller's explicit tool allowlist, dontAsk mode,
normal plugin hooks, strict run-local Capy/PAL services and `--plugin-dir` plus
run-specific CPR registry. Codex retains workspace-write/never and temporary,
revision-specific marketplace/cache registrations and project trust. Record
prior absence and restore only owned entries using the gate 2B cleanup procedure.
No deployment, production access or requirement-changing controller replies.

## Grading

Use [revision-2 rules](../task2-rubric-v2.md), the current final eval assertions
and the gate 2B [pinned grader](../task2b/grader.md), SHA-256
`c2621b9a4f2f3e0d86cae6ec682b7ca1a2c729afb5da5cd9031873978b2dc342`.
Fresh independent eval-grader role: `gpt-6.1-sol`/xhigh, Read-equivalent tools
restricted to manifest-listed sealed evidence and supplied instructions.
Re-run positive/negative/missing-evidence calibration before grading pairs.
All new scenario assertions remain required; R3/I2 alone use the selected
receipt/use mapping. Exact submitted prompts/parity remain unverified.

Successful source reads/formatting/history inclusion and observable use must
support required PAL receipt. A counter, requested path or inclusion marker alone
does not prove receipt. Preserve all failed attempts and explicit unknowns.
Freeze fixes as new candidate identities and rerun affected pairs; never count
a repaired report or handoff as the original actor's behavior.

## Stop and resume

An unavailable model/authentication/runtime or rejected required launch is an
unrun gate. Complete independent preparation/checks, retain the exact failure,
and record owner, next action and verification condition in tasks.md. Do not
switch the primary provider, weaken evidence rules or mark Task 12 done.
