# Task 1 verification

Task 1 delivers the core `/kk:brainstorm` conversation, shared reasoning references, scoped `/kk:design` discovery changes, registration, generated Codex output, and scenarios 1, 5, and 7. Six accepted scenario/variant runs pass all 28 assertions. Two earlier routing runs are preserved as invalid and excluded from acceptance. Tasks 2–4 remain pending.

Baseline: `9825150301b0fccea80e2d750bf0a1693df571c3`. Execution date: 2026-10-03. The worktree was clean before Task 1.

## Behavior and scope

The new skill loads both shared references before interviewing, asks one question at a time, selects relevant reasoning lenses, and closes in chat with decisions, rationale, and uncertainty. It permits focused file/web research and excludes knowledge-store/session-vault searches, writes, and automatic handoff. The recorded scenarios cover conversational selection, operation without a repository, and truthful early stopping. Research/revision behavior, other producer routes, and existing design regressions are owned by later tasks.

Both reasoning sources were relocated byte-for-byte, including upstream attribution and pinned source comments. Comparison with `git show HEAD:<old-path>` passed. SHA-256 values:

- `ideation-frameworks.md`: `9b49fcb0dd3b92af39318907d2d5342b478d4495a1f50ae31a0f13aa1ccbc08c`
- `idea-refinement-criteria.md`: `b5d3e31b454a668490dc00c08f74c1d4e82f2abf83375ac162b557974e344fbd`

The four canonical symlinks resolve to those sources; generated copies resolve locally. `design/idea-process.md` equals its baseline after replacing only the two reference names, including the HMW anchor. Its gates and procedure are unchanged. `/kk:design`'s description and Ideas and Prototypes entry now advertise written planning; scenarios c1r2/g1r2 exercise that wording alongside `/kk:model` and `/kk:implement`. No model-description change was needed. Other routing boundaries remain Task 3's responsibility.

The descriptions contain 514 characters (`brainstorm`) and 360 (`design`), below the 1,024-character portability target. The current [Claude Code description guidance](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short) was checked before editing: it still documents a 1,536-character default per-entry cap. New skill bodies have 33 canonical lines and 34 generated lines. Content-level research appears once, after instruction loading; the pinned external inspiration is attribution rather than a runtime read.

## Execution method and limits

All runs used OpenAI `gpt-6-astra`, reasoning effort `max`, Codex 0.160.0, and fresh `collaboration.spawn_agent` sessions with `fork_turns: none`. Canonical and generated identify the instruction variants, not two different host applications. These runs do not certify native Claude Code loading or behavior.

Source snapshots under `/tmp/brainstorm-task1-evals/instructions/{canonical,generated}/` were copied without any `evals/` directory. Each conversation used its own initially empty workspace under `/tmp/brainstorm-task1-evals/workspaces/`, outside a skill ancestor. Fixture manifests are empty. Only the selected workflow's operative instruction closure was authorized, with no file writes or external changes. Web tools were unavailable; no synthetic source responses were supplied. Harness setup directed replies to the caller rather than interactive input tools, allowing exact runbook replies to be delivered.

For routing, the initial submission supplied all four descriptions and their loading paths, without a body or expected selection. For scenarios 5/7 it explicitly selected the tested skill. The task setup restricted inherited skill listings to this catalog. Shared filesystem access and inherited host instructions are not OS isolation; the complete public tool traces were audited for out-of-manifest reads. Every run performed only three instruction reads through two tool calls; none read an oracle, project content, another workflow, or a knowledge store, and none attempted a mutation.

Each run directory retains the exact initial submitted message, each exact reply with its matched runbook condition, complete assistant responses and raw tool calls/results in `trace.jsonl`, session/provider/model metadata, and a `result.json` with file states, hashes, termination, and assertion evidence. `submission-01.txt` adds one final LF when serializing the submitted text: `submission_file_sha256` hashes the stored UTF-8 file bytes, while `exact_submission_sha256` hashes the delivered UTF-8 message without that added LF. Trace records omit private reasoning and repeated host setup; public tool calls/results and assistant messages are unabridged. Reply text was captured before delivery. Conversation turns count substantive responses, excluding the initial skill-use announcement.

`catalog_text_sha256` hashes the contiguous UTF-8 selection block in the submitted message: after the first blank line ending Conversation setup, up to the blank line before `User request:`, excluding those blank-line delimiters. Routing blocks include the full catalog heading and all four entries; explicit-selection blocks contain the single skill-selection line. This hash was recomputed during the audit to replace an undocumented partial-heading derivation; the recorded submitted messages did not change.

[Canonical input inventory](canonical-inputs.sha256) and [generated input inventory](generated-inputs.sha256) record the staged file bytes, including resolved symlink contents. Snapshot-relative paths map back to `klaude-plugin/` and `kodex-plugin/`. The inventories were captured at 14:49:11 UTC; their checks passed after all runs. For each run, all three full instruction texts returned by the tools were also compared byte-for-byte against the hashed snapshots. Final workspace listings remained empty.

## Accepted runs

| Scenario | Canonical evidence | Generated evidence | Turns | Termination | Verdict |
| --- | --- | --- | --- | --- | --- |
| 1: loose technical idea | [c1r2](c1r2/result.json) | [g1r2](g1r2/result.json) | 4 each | complete | 1.1–1.5 PASS in each variant |
| 5: no repository | [c5](c5/result.json) | [g5](g5/result.json) | 3 each | complete | 5.1–5.5 PASS in each variant |
| 7: early stop | [c7](c7/result.json) | [g7](g7/result.json) | 2 each | early-stop | 7.1–7.4 PASS in each variant |

Scenario 1 selected brainstorming and narrowed the next action to checking artifact retention policy before building. Scenario 5 chose a one-week reminder trial and retained uncertainty about sustained operator response. Scenario 7 stopped after E1 and preserved unknown repeat safety and absent rollout approval. All replies matched unused runbook rows; no bounds were extended and no off-script reply was invented.

The first routing runs, [c1](c1/result.json) and [g1](g1/result.json), completed their conversations, but the runbook required input hashes before launch and that capture was missed. They remain invalid for acceptance, with PARTIAL assertion grades; c1r2/g1r2 are fresh replacements with pre-start inventories/submission hashes. No skill, scenario, or runbook instruction changed to obtain a pass. Scenarios 5/7 do not require pre-start hashing; their recorded tool outputs establish the exact bytes read.

## Structural verification

| Check | Result and durable evidence |
| --- | --- |
| Full shell suite | 9 suites, 304 test cases, 630 assertions, zero failures; [raw log](checks/shell-suite.txt). |
| Plugin structure | 40 test cases, 210 assertions, zero failures; [final log](checks/plugin-structure.txt). Includes new skill registration and both consumers' shared symlinks. |
| Codex structure | 16 test cases, 29 assertions, zero failures; included in generation and full-suite logs. |
| Generator tests and regeneration | `make generate-kodex` succeeded; [log](checks/generation.txt). |
| Generation stability | [Before](checks/generated-before.sha256) and [after](checks/generated-after.sha256) inventories compare equal, including generated skills and agents. |
| Plugin graph | Go tests passed; validation reported no broken edges or orphans, with a nonfatal cycle warning; [log](checks/plugin-graph.txt). |
| Skill validators | Bundled skill-creator validator passed for canonical and generated brainstorm. |
| Eval structure | All three JSON files parse; fixture paths, five runbook sections, unique reply IDs, positive turn bounds, and assertion mappings verified. |
| Diff and relocation | `git diff --check`, exact source comparisons, design procedure comparison, symlink resolution, and stale operative-link searches passed. |

The default `/usr/bin/python3` is 3.10 without `tomllib` or `tomli`, so the first Codex test attempt failed. Tests succeeded with the already installed Python 3.12 at `/home/sergio/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/bin` prepended to PATH. The initial sandbox also blocked `.codex/agents` regeneration and uv's existing cache during schema checks; the authorized generator/full-suite reruns succeeded with the required filesystem access. No test assertions were weakened and no dependency was added.

## Reviews and remaining work

The isolated code reviewer loaded all three applicable skill-md review checklists and approved the source changes without P0–P3 findings. It verified reference blob identity, symlinks, discovery scope, generated transformations, and runbook contracts. The initial review explicitly excluded still-in-progress evidence finalization. During the evidence audit it identified three preservation issues: the distinction between saved-file and submitted-message hashes, the catalog hash's undocumented derivation, and raw check logs hidden by ignore rules. Hash conventions are now explicit and verified; logs retain their raw bytes under `.txt` names that normal Git staging includes. No behavior or input content changed.

The final independent evidence audit approved all six accepted runs and all 28 PASS verdicts, including exact prompts/replies, applicable reply conditions, instruction bytes/hashes, metadata, permitted reads, empty file states, turn counts, and stopping reasons. It confirmed the two invalid originals remain excluded, all three audit corrections are resolved, and the logs/inventories support the check totals. The reviewer audited recorded checks rather than independently rerunning them. No remaining finding prevents Task 1 completion.

The two-step PAL review used `gemini-3.1-pro-preview` and returned no issues; [native result](pal-review.json). Per the isolated-review protocol, a zero-issue external result supplies no actionable review signal and does not certify behavioral evidence. No P0/P1 systemic findings required indexing; no new project convention beyond the documented plan was established.

The environment rejected deletion of the temporary review diff at `/tmp/brainstorm-task1-review.patch`, requiring explicit approval for file removal. The patch is retained; remove that exact temporary file only after deletion is authorized. This cleanup has no effect on repository changes or verification results.

Tasks 2–4 own the remaining 26 baseline scenario/variant runs, later affected-case reruns, user documentation/count reconciliation, and full-feature specification review. This note does not mark those checks complete. Optional `/kk:clarify-docs` may review this verification note after the feature's documentation task; it has not been invoked.
