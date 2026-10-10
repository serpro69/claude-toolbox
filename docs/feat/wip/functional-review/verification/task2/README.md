# Task 2 seed fixtures and baseline capture

Task 2 is **in progress**. The four final fixtures are authored and frozen.
Sixteen baseline workflows were captured; four required Codex workflows remain
unrun because the available runtime surfaces do not expose exact reviewer
handoffs. Do not start operative changes or mark Task 2 complete on this evidence.

## Fixed inputs

- Actor: unchanged `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`, filtered using Task 1.
- [Fixture, metadata, oracle, prompt and rubric hashes](../task2-frozen.json).
- [Grading procedure and assertion/evidence mapping](../task2-rubric.md).
- [Run contract](../run-contract.md): provider, models and two-run threshold unchanged.
- R1: `review-code/evals/functional-cleanup-ownership`, ID 6.
- R3: `review-code/evals/functional-disabled-provider-history`, ID 7.
- I1: `implement/evals/functional-plan-delivery-conflict`, ID 8.
- I2: `implement/evals/functional-standalone-patch-contract`, ID 9.

Fixture paths above are relative to `klaude-plugin/skills/`. Metadata declares
every fixture file; expected results stay in sibling `oracle/` directories.
Codex copies were regenerated twice without second-generation drift. No operative
skill/agent instruction changed. The concrete workflow grader is Task 8 work;
no behavioral PASS/FAIL/PARTIAL grades are assigned here.

## Captures

Each run contains initial/final subject files, prompt, launch/command metadata,
public tool events, report and hashed manifest. `captured` means evidence was
retained, not that assertions passed. The [capture index](capture-index.json)
includes all 23 measured-attempt/unrun records, including three failed attempts.

| Provider | Case/mode | Repetition 1 | Repetition 2 |
| --- | --- | --- | --- |
| Claude | R1 standard | [captured](claude-r1-standard-1-capture2/manifest.json) | [captured](claude-r1-standard-2/manifest.json) |
| Claude | R1 isolated | [captured](claude-r1-isolated-1/manifest.json) | [captured](claude-r1-isolated-2/manifest.json) |
| Claude | R3 standard | [captured](claude-r3-standard-1/manifest.json) | [captured](claude-r3-standard-2/manifest.json) |
| Claude | R3 isolated | [captured](claude-r3-isolated-1/manifest.json) | [captured](claude-r3-isolated-2/manifest.json) |
| Claude | I1 plan | [captured](claude-i1-plan-1-capture2/manifest.json) | [captured](claude-i1-plan-2/manifest.json) |
| Claude | I2 standalone | [captured](claude-i2-standalone-1/manifest.json) | [captured](claude-i2-standalone-2/manifest.json) |
| Codex | R1 standard | [captured](codex-r1-standard-1/manifest.json) | [captured](codex-r1-standard-2/manifest.json) |
| Codex | I1 plan | [captured](codex-i1-plan-1/manifest.json) | [captured](codex-i1-plan-2/manifest.json) |
| Codex | R3 isolated | [unrun](codex-r3-isolated-1/attempt-status.json) | [unrun](codex-r3-isolated-2/attempt-status.json) |
| Codex | I2 standalone | [unrun](codex-i2-standalone-1/attempt-status.json) | [unrun](codex-i2-standalone-2/attempt-status.json) |

All 12 Claude executions returned success; all four measured Codex turns
completed. Claude outputs identify `claude-opus-4-8`; launch arguments request the
declared 1M model/high effort. Codex identifies `gpt-6-astra/xhigh`. Isolated Claude
paths contain named-agent dispatches and both PAL calls. Their presence does not
prove substantive source coverage; retain actual PAL coverage fields for grading.

Claude's explicit policy denied some compound shell commands for discovery,
temporary diffs and tests. Full denials remain in the index/result events. Actors
continued using permitted Read/Write or shell alternatives. Grade recovery from
subsequent events; any unfulfilled required capability is incomplete coverage.
These are not claims of denial-free verification. Candidate runs must use the
same policy unless both sides are recaptured.

## Codex handoff blocker

Two fresh loading probes used only public baseline instructions and a synthetic
marker; neither counts as a behavioral run:

1. [Public app-server stream](codex-plaintext-probe/protocol.jsonl) and
   [child history](codex-child-surface/child-items.json): actual child IDs appear
   in `subAgentActivity`, but collaboration items expose a wait with empty
   receivers/null prompt. Child history omits the submitted task message.
2. [Observation hooks](codex-hook-probe/hook-tool-events/): PreToolUse/PostToolUse
   expose the role, call ID and fork mode, but `message` remains ciphertext.
   Hooks emit no context, decisions or rewritten inputs and never read transcripts.

The hook mechanism is documented in [Codex Hooks](https://learn.chatgpt.com/docs/hooks).
The installed 0.161.0 schema and observed records establish this session's limits.
A final actor confirmation is not plaintext dispatch evidence. R1/I1 assertions
do not depend on exact handoffs; their captures make no such claim. R3 isolated
and I2 standalone remain **UNRUN**, with the original requirement unchanged.

**Owner:** implementing agent. **Next action:** establish a supported plaintext
submission surface in a separate probe, then stage four fresh baseline runs with
these frozen inputs before operative changes. If another runtime is needed,
revise the run contract and recapture the affected comparison on both sides.
Do not reconstruct payloads from expected answers, decrypt protected runtime
content, lower assertions or substitute another provider.

## Isolation, retention and cleanup

[Post-run bindings](post-run-bindings.json) verify 18 completed run/probe bundles,
the installed Codex cache and generated role copies against Task 1 manifests.
Each measured workspace began with exact fixture bytes and an absent run-local
knowledge database. [Capy 0.16.8 probes](state-probe/summary.json) passed search/index,
foreign-marker absence and unavailable-vault checks.

R3's provider is in local `eval-release` history, absent from before/after and PR
hunks. Each launch records base/release/blob identity and historical source.
[Direct reproductions](fixture-reproductions.json) confirm R1's ownership loss and
R3's applied-save/raised-error difference; existing fixture tests pass as intended.

Independent review audited all 12 Claude input traces: no evaluator, oracle,
controller, personal-config or cross-workspace reads were observed. This does not
prove OS-wide read confinement. Private thinking is omitted at capture. All
packages record no configured credential value in `credential-redactions.json`.
Unrelated host/account notifications were removed during export; [redaction records](export-redactions.json)
preserve original sequence IDs. [The final manifest](manifest.json) hashes exported files.

Three attempts remain excluded: [launcher failure before model startup](claude-r1-standard-1/attempt-status.json),
[standard string-notice parser failure](claude-r1-standard-1-retry/attempt-status.json),
and [plan parser failure](claude-i1-plan-1/attempt-status.json). Fixes added event-shape
handling, safe teardown, child discovery, immutable retry handling and sealing on
success/failure. Reruns used fresh workspaces. Each command record identifies its
actual controller hash; the initial freeze does not imply the controller never changed.

[Cleanup](codex-cleanup/removed.json) removed ten temporary project trusts and two
hook trusts. The `fr-c2d28c9e-seeds` plugin/cache and marketplace were also removed.
Normal configuration remains. Controller/actor temporary roots may be discarded
after retention; repository evidence and immutable inputs support reconstruction.

## Verification and review

- 15 controller tests passed, including failed-capture sealing and immutable retries.
- All nine existing shell suites passed; `test-*.sh.log` files retain output.
- Generation passed twice without drift.
- Plugin graph passed with its existing cycle warning and no broken edges/orphans.
- [Independent review](review.md) approved corrected fixture/controller work.

Fixture/rubric bytes remain frozen. Candidate identity, workflow grades and the
four blocked baseline captures remain outstanding.
