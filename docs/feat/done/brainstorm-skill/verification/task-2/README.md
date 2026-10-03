# Task 2 verification

Task 2 adds scenarios 2, 3, 4, and 6 for architecture discussions, discoverable project facts, changed premises, and unavailable evidence. All eight canonical/generated runs completed within their runbook bounds and passed 44 assertions. No operative skill instructions changed. Tasks 3–4 remain pending.

Baseline: `1f25a58a13fa097e5fdb058223af908741d020c1`. Execution date: 2026-10-03. The worktree was clean before this task.

## Accepted runs

| Scenario | Canonical | Generated | Assistant turns | Result |
| --- | --- | --- | --- | --- |
| 2: architecture audience | [c2](c2/result.json) | [g2](g2/result.json) | 3 each | 2.1–2.5 PASS in both |
| 3: discoverable project fact | [c3](c3/result.json) | [g3](g3/result.json) | 2 each | 3.1–3.5 PASS in both |
| 4: changed premise | [c4](c4/result.json) | [g4](g4/result.json) | 3 each | 4.1–4.6 PASS in both |
| 6: unavailable evidence | [c6](c6/result.json) | [g6](g6/result.json) | 2 each | 6.1–6.6 PASS in both |

All runs terminate `complete`; none were off-script, invalid, unavailable, or rerun. Architecture responses compare recovery and operational burden without a product questionnaire, then preserve standby as an investigation rather than a validated topology. The project-fact runs read the actual concurrency note, distinguish its lock constraint from the user's acceptable delay, and retain concurrency one while measuring lock occupancy.

The changed-premise runs explicitly reject persistent caching after the confidentiality correction, including encrypted retention, while preserving manual invocation and local-only processing. The missing-evidence runs attempt the absent capacity-report read, report the actual error, and keep eight-worker safety unresolved. The final decision to retain four temporarily is not presented as proof of downstream capacity.

## Execution method and evidence

Each run used a fresh `collaboration.spawn_agent` session with `fork_turns: none`, OpenAI `gpt-6-astra`, reasoning effort `xhigh`, and Codex 0.160.0. Canonical/generated identify the instruction variants, not different hosts; these runs do not certify the native Claude Code host. The inherited model setting differs from Task 1's `max` effort and is recorded per run.

The three operative instruction files were staged under `/tmp/brainstorm-task2-evals/instructions/{canonical,generated}/`, preserving canonical symlinks to copied shared sources. Snapshots contain no eval or oracle material. Each run had its own workspace outside any `SKILL.md` ancestor under `/tmp/brainstorm-task2-evals/workspaces/<run>/`. Only c3/g3 received a fixture, `ops/release-queue.md`; all other workspaces started empty. The missing report in c6/g6 remained absent. Web and external service tools were unavailable; no synthetic source responses were supplied.

The setup permits read-only access to the three instructions, their resolved targets, and declared workspace resources. It directs conversational responses to the caller so only the next applicable scripted user reply is delivered. Shared filesystem access and inherited host instructions are not OS isolation: every public tool call was inspected. Each run loaded the entry point, then both references, before substantive discussion or project reads. Calls only read those instructions and, in scenarios 3/6, the supplied or explicitly absent file. No run attempted a mutation, broad search, knowledge-store/session-vault search, indexing, implementation, or handoff. Initial/final file inventories match.

For each run:

- `setup.json` captures the workspace, allowed resources, initial fixture hashes, scenario/runbook hashes, instruction hashes, and exact setup hash before launch. The scenario/runbook hashes refer to the canonical evaluator inputs for both variants; the variant determines the operative instruction snapshot and invocation spelling. [Canonical](canonical-inputs.json) and [generated](generated-inputs.json) inventories identify all three allowed instruction reads and resolved paths. Paths within the variant snapshot map to the same relative paths under the corresponding repository plugin.
- `submission-01.txt` contains the exact delivered initial message with no added trailing newline. Its hash is `exact_submission_sha256`. `catalog_text_sha256` hashes the single skill-selection line between the conversation setup and `User request:`. There is no competing catalog in these explicitly selected behavior tests.
- `submission-02.json` and subsequent files capture each exact reply before delivery, its runbook ID, matched condition, message hash, and capture time. Reply selection was manual and followed the ordered table. No future reply or grading expectation was exposed to the tested agent.
- `trace.jsonl` preserves unabridged public assistant messages and raw tool calls/results in source order. Ordinals refer to source session records; line references in grades refer to this exported trace. Private reasoning and repeated host setup are excluded. `transport.jsonl` retains the original encrypted task-delivery records; the plaintext submissions were captured separately at delivery, not reconstructed from those records.
- `session.jsonl` preserves session identity, provider, harness version, and actual model settings. `audit.json` is a derived index of messages, calls, counts, and final file state; the raw trace is authoritative.
- `result.json` records termination, bounded turn count, consumed replies, hashes, unchanged final file state, and each assertion verdict with trace locations. Turns count substantive final responses; skill-use announcements are excluded. Returned instruction contents were compared byte-for-byte with the pre-start hashed snapshots.

Tool-call and result counts match in every run. All exact replies match their runbook rows, instruction/fixture hashes remain valid, and full file contents were available without truncation. The scripts used to stage and export this one-time verification remain temporary tooling outside the repository; no eval runner was added.

## Checks and earlier coverage

| Check | Result and evidence |
| --- | --- |
| Full shell suite | 9 suites, 304 test cases, 630 assertions, zero failures: [log](checks/shell-suite.txt). |
| Generator tests, Codex/plugin structure | `make generate-kodex` passed after adding scenarios and after the coverage-guide update: [initial successful generation](checks/generation.txt), [final generation](checks/generation-final.txt). |
| Generation stability | Second pass succeeded; generated output and agents have identical [before](checks/generated-before.sha256) and [after](checks/generated-after.sha256) inventories. |
| Plugin graph | Go tests and validation passed with no broken edges or orphans; existing nonfatal cycle warning remains: [log](checks/plugin-graph.txt). |
| Eval contracts | All four JSON files parse, every fixture exists, each runbook has all five fixed sections, unique reply IDs, a positive turn bound, and evidence mappings for every assertion. |
| Evidence audit | Exact submitted text/replies, hash stability, tool traces, observed stopping conditions, assertion evidence, and final file state checked across all eight runs. |
| Whitespace | `git diff --check` and new-file whitespace checks passed. |

The initial sandboxed generator could not update `.codex/agents`, and the first shell-suite attempt could not access uv's existing cache. Their [generator](checks/generation-initial.txt) and [suite](checks/shell-suite-initial.txt) failure logs are retained. Authorized reruns with the necessary filesystem access passed. As in Task 1, tests use the already installed Python 3.12 by prepending `/home/sergio/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/bin` to PATH. No dependencies or test assertions changed.

Subtask 2.3 needs no Task 1 reruns: the operative brainstorm/design/model instructions, shared references, and scenarios 1/5/7 are byte-identical to the Task 1 baseline. Only the new eval material and evaluator coverage guide changed. Task 1's original traces and six accepted runs remain intact. Combined coverage is 14 of the 32 baseline scenario/variant runs; Task 3 owns the remaining 18 runs. This task does not certify competing-producer routing or the design regressions.

## Review

The independent code reviewer loaded all three applicable skill-md checklists and [approved the source and evidence](code-review.md) with no P0–P3 findings. It independently checked all eight conversations, all 44 verdicts, exact prompts/replies and delivery timing, instruction and fixture hashes, allowed reads, unchanged workspaces, generated parity, Task 1 input identity, and test/generation logs. It audited recorded results without rerunning the scenarios or shell suite. Encrypted transport records cannot independently authenticate the captured plaintext; the preserved submissions and capture-before-delivery timestamps supply that evidence.

The two-step PAL review used `gemini-3.1-pro-preview` and returned no actionable issues; [native result](pal-review.json). Under the isolated-review protocol, this zero-issue external result is treated as no actionable signal rather than additional behavioral certification. No systemic P0/P1 findings or new project conventions required indexing. No findings remain to resolve; Task 2 is complete.
