# Brainstorm scenario guide

These are manual, multi-turn scenarios. Authored fixtures and green structure tests do not establish observed behavior. Run each scenario against canonical instructions and generated Codex instructions, recording each variant separately. No new runner or eval schema is required.

## Isolation and selection

Stage only the files listed in each `eval.json` under a fresh workspace outside the plugin and any `SKILL.md` ancestor, preserving paths relative to `test-files/` unless the runbook specifies a mapping. `files: []` means an empty workspace. Never expose `eval.json`, this README, any `oracle/` directory, future replies, or grading expectations to the tested agent. A shared filesystem is not isolation: audit the complete tool trace for reads outside the allowed manifest; oracle access or an incomplete trace invalidates the run.

For implicit routing scenarios 1 and 8–12, expose the descriptions and normal loading paths for `brainstorm`, `design`, `model`, and `implement`, without preloading any skill body or identifying the expected selection. Scenario 11 explicitly invokes `$kk:design`; it is an invocation regression, not implicit-selection evidence. For interview scenarios 2–7, explicitly select `$kk:brainstorm`. Normal skill loading must be observable; a skill-name classification question cannot substitute for execution. If the harness cannot expose competing descriptions and record actual loading, mark implicit-routing execution unavailable.

Canonical runs use `klaude-plugin/` instructions; generated runs use `kodex-plugin/` instructions after generation, including their resolved shared-reference files. Record the provider and model independently of the instruction variant: a canonical-instruction run on Codex does not certify the Claude Code host. Translate explicit invocation prefixes mechanically for the generated variant (slash to dollar); do not rewrite natural-language routing prompts. Keep all other inputs equal where applicable. Allow read-only access to the chosen variant's operative instruction closure, excluding its evals. Resolve canonical per-skill symlinks to the shared sources in the allowed-file manifest.

Keep instruction reads complete. When using nested tool orchestration, the outer output budget must accommodate the combined results; increasing only an inner shell command's budget is insufficient. If a response is truncated, require the omitted instruction content to be read before subject-matter work. Retain and rerun any execution whose required instruction loading cannot be established from its complete trace.

Positive brainstorm scenarios permit read-only project-file and web research as declared in their runbooks; no deliberate file writes, temporary interview artifacts, knowledge-store/session-vault searches, indexing, implementation, or external mutations. Negative routing scenarios follow their selected producer's contract: scenarios 9, 11, and 12 permit fixture-scoped written artifacts and supply required confirmations. Record unavailable tools and synthetic responses; never fabricate a successful source lookup.

## Fixed runbook contract

Every scenario has an evaluator-only `oracle/runbook.md` with these exact sections:

| Section | Required contents |
| --- | --- |
| `## Setup` | Catalog or explicitly selected skill; canonical/generated handling; allowed fixture paths; available tools; permitted writes; synthetic source responses. Must agree with `eval.json`. |
| `## Start` | Send `eval.json.prompt` exactly once. State any mechanical invocation conversion. Never add the expected skill or answer to a natural-language routing prompt. |
| `## Replies` | Ordered table with columns `ID`, `Send when`, `Exact user reply`. Unique IDs, observable topic/event conditions in the latest assistant response, and exact user facts or choices without grading guidance. An empty table is valid. |
| `## Stop` | Positive integer `Max assistant turns`, counting the initial response; observable completion; expected early stop if any. Check completion first. More input needed with no matching row means `off-script`; reaching the bound means `turn-limit`. |
| `## Grade` | Each assertion ID mapped to response, file-state, or tool-trace evidence; verdict PASS/FAIL/PARTIAL. Unreached or unobservable assertions are PARTIAL. |

After each assistant response, check completion first. Otherwise send at most one unused reply row whose condition matches, taking the first matching row when several match. Mark it consumed and never resend it. Keep all future rows hidden. Do not improvise replies or silently increase the bound. Evaluator bounds do not impose a question budget on the skill.

An off-script result can expose an incomplete runbook rather than a skill defect. Preserve the original trace, explicitly repair the runbook if warranted, and start a new run. Never relabel an interrupted run as successful. Record tool/harness failures separately as unavailable execution; missing or invalid runs remain pending.

## Evidence and grading

Keep execution evidence with the consuming project's verification notes, outside the staged workspace. For every run capture:

- Exact submitted setup/catalog, initial prompt and each delivered reply, including reply IDs and conditions matched. Capture submission text at delivery, not reconstructed later from the scenario.
- Instruction and fixture SHA-256 hashes, allowed-file manifest, provider/model/settings, harness version, instruction variant, workspace path, and initial file state.
- Complete assistant responses and raw tool calls/results, including actual skill loading. Selection comes from loading traces; conversation and artifact boundaries come from the full exchange and file state.
- Final file state, termination reason (`complete`, `early-stop`, `off-script`, `turn-limit`, `unavailable`, or `invalid`), and one verdict with concrete evidence per assertion. Record attempted prohibited mutations even when a sandbox prevents them.

Inspect the entire conversation for adaptive questions, challenged assumptions, rationale, and faithful recaps. Do not infer behavior from instruction wording. Preserve original runs and identify reruns by new IDs and hashes. If instruction changes affect an earlier case, rerun it; if discovery wording changes, rerun scenario 1 and affected routing cases in both variants.

## Coverage and design regressions

The complete acceptance matrix is twelve brainstorm scenarios plus four existing `$kk:design` regressions, each in two variants: 32 baseline runs before reruns. This directory supplies all twelve scenarios. Scenarios 1–7 cover conversation, research, revision and closure; scenarios 8–12 cover direct implementation, written planning, nontechnical requests, explicit design invocation and durable domain-kit creation. Unexecuted pairs are not passes.

The existing design regressions are `hard-gate-enforcement`, `proportional-diverge-routing`, `wip-feature-no-subphases`, and `clarity-after-drafting` under `design/evals/`. Each now has an evaluator-only `oracle/runbook.md` with the same five sections, explicit design selection, variant handling, fixture mappings, permitted writes, bounded confirmations, and termination. Their original prompts, assertions and fixture contents remain unchanged. The first two use empty workspaces and scripted foundation/classification replies. The WIP case maps its two documents into `docs/feat/wip/auth-refactor/`; the referenced implementation file is initially absent. Bounded replies clarify the fixture's policy ambiguities and authorize substantive documentation refinement before stopping at implementation handoff. Merely identifying readiness gaps does not demonstrate resumption. The drafting case stages `accepted.md` at workspace root and needs no replies because its prompt already supplies approvals. Keep all existing oracles hidden. These behavior regressions do not count as implicit routing coverage.
