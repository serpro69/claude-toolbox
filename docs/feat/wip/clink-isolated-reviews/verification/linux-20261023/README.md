# Linux Task 0 verification — 2026-10-23

Status: **Task 0 complete for the corrected local PAL candidate identified below.**
C1–C8 pass within the recorded bounds. [Independent review](independent-review.md)
approved the discovery correction and final evidence. This record supplements the historical
[macOS verification](../pal-contract.md), without invalidating its scoped results.

## Baselines and boundaries

- Toolbox: clean `09f9be3b334b0f9265d0a5b9107af6cafe429b5e` before this evidence update.
- Original PAL candidate: clean `d25c2d029a5d157935aa9bb836c18e9725969b8f`.
  Tests and the temporary Claude MCP server use a `git archive` of that revision.
  The subsequently authorized correction changes three PAL files, recorded in
  [pal-fix-validation.json](pal-fix-validation.json). No plugin instructions changed.
- Connected PAL reports 1.4.2, Python 3.12.11, Linux, provider-free mode and zero
  configured API providers/models. See [version](version.json) and
  [discovery](discovery.json). Its startup snapshot finds Claude/agy and misses
  Codex/Gemini. Presence is not authentication.
- Three cached 1.4.2 package copies have the same `tools/clink.py` SHA-256 as the
  candidate: `b9b8c9a146680f82e6eed5dadd6f7c7dced692247053c41410cad68f4036cad7`.
  This is a bounded package comparison, not proof of the running process's exact
  installation. The separately launched Claude server has explicit source provenance.
- Existing PAL virtualenv: Python 3.10.12 with pytest, pytest-asyncio and MCP
  already installed. No dependency installation, CLI upgrade, login, model
  configuration or saved permission changes were performed.
- Claude Code 2.1.296; agy 1.4.6. Existing agy settings report
  `agentMode: auto`, with no explicit `permissions` block or model field.
  Agy's returned actual model identity is unknown. Native auto permissions were
  retained; no enforced read-only claim is made.
- Selected external roster: Claude/Anthropic and agy/Google, using the earlier
  explicit operator mapping/selection. OpenAI authored the fixture and is excluded.
  Gemini remains excluded by the earlier operator choice. Executable name and
  PAL `provider_used` (which echoes the client) do not establish model-provider identity.
- Scheduling for this integration remains sequential. Deterministic concurrency
  checks passed, but live simultaneous model invocations were not tested.

## Deterministic execution

[Command and result](upstream-tests.json): **829 passed, 11 deselected in 42.82s**,
exit 0, complete Capy capture `84822d6f-d3db-4f27-b68f-4438fae30b31`.

This is a focused existing upstream suite, not a new plugin implementation or
a general eval runner. Unit tests use controlled providers/processes; the
`test_cli_only_mcp.py` and `test_clink_working_directory_mcp.py` cases exercise
actual MCP stdio/SDK/server boundaries with fake child CLIs. No paid API-backed
review was performed. The 11 deselected cases are live agy edit-safety and
role/cwd combinations; selected-provider live review/continuation runs are below.

| Contract | Executed upstream evidence |
| --- | --- |
| C1 discovery | `test_cli_only_startup.py`: provider-free startup, API-mode registration with empty restricted catalog, fatal malformed catalog, unavailable-tool rejection before dispatch, API dispatch; `test_listmodels.py` and `test_listmodels_restrictions.py`: configured/empty/restricted catalogs |
| C2 availability | Startup discovery does not spawn/login, configured child PATH resolution, missing executables and invocation recheck after executable removal; role/schema validation in continuation/safe-default suites |
| C3 configuration | Safe-default, environment and agy tests preserve configured model/role arguments; live command/model evidence is recorded separately |
| C5 controls and isolation | `test_saved_selection_continues_without_cli_or_role_and_never_inherits_edits`, `test_parent_history_and_attachments_do_not_restore_permissions`, real-stdio `test_stdio_cli_conversation_discovery_history_and_permissions`, and agy continuation/safety tests |
| C5 concurrency | `test_clink_concurrency.py`, `test_clink_working_directory_mcp.py::test_mcp_distinct_bound_threads_overlap_without_crossing_projects`, environment scratch isolation |
| C6 failures | `test_clink_execution_errors.py`: semantic failures despite exit 0, authentication/errors, spawn errors and diagnostic retention; agy `test_missing_executable_is_a_tool_error`, `test_timeout_reaps_one_process_without_replay_or_command_prompt`, `test_denied_actions_surface_in_successful_payload_metadata` |
| C6 output limits | `test_clink_tool.py::test_clink_tool_truncates_large_output` and `test_clink_tool_truncates_without_summary`; bounded agy error/stderr and reduced-history cases |

## Discovery and identity exercises (C1/C2)

These are manual applications of the accepted design to live/captured and
synthetic boundary inputs, checked against the executed PAL contract tests.
They establish usable input distinctions and a deterministic policy mapping;
they do **not** certify the unimplemented Task 1 selector.

| Input | Applied decision |
| --- | --- |
| Callable codereview plus a successfully discovered eligible API model | API branch. A later runtime failure remains an API failure; no clink switch. |
| Successful provider-free discovery, codereview absent, clink present | Clink roster; the connected Linux run observes this case. |
| Callable codereview but successful restricted catalog contains no eligible model | Select clink using the corrected candidate's `metadata.cli_clients`. The original candidate lacked these observations; the regression and corrected probe below close that gap. Configured-provider count alone does not establish model availability. |
| Failed discovery, malformed response, or unresolved eligibility | Unknown/unavailable external coverage; no speculative clink call. A fatal catalog error is not an empty catalog. |
| Neither callable external backend, or no eligible clients | Internal review only, explicit coverage limit. |
| OpenAI author; present Claude/agy with operator-confirmed Anthropic/Google mappings | Select Claude and agy once each; exclude Codex/OpenAI even if executable-present. |
| Authoring provider unknown | Resolve authorship before external dispatch. Current host CLI is not evidence of historical authorship. |
| Executable-present client with unknown model-provider mapping | That candidate remains unresolved/ineligible; do not infer its provider from the executable name. |
| Both agy and Gemini map to Google; no declared choice | Resolve the duplicate choice before Google dispatch; never count two clients as two providers. |
| Same duplicate with the recorded operator choice of agy | Select agy once, exclude Gemini. |
| Selected executable missing or role unusable | Exclude and disclose; do not substitute the authoring provider or a guessed role/model. |
| One selected client fails | Preserve the other result, report the failed attempt and maintain the original roster. |

PAL supplies no provider identity field for CLI models. The integration contract
therefore requires explicit operator/native configuration provenance, plus a
focused question when that mapping or duplicate choice is unresolved. It does
not require a new registry/API or invented clink request fields.

### Original discovery gap and correction

The focused [empty-catalog probe](empty-api-discovery.json) registers one synthetic
Custom/Local provider, restricts out its only model, verifies that both
`codereview` and `clink` remain callable, and executes the real `listmodels` tool.
Its response reports one configured provider and zero available models, but
metadata contains only `tool_name` and `configured_providers`. CLI executable
observations exist in the server's runtime snapshot but are not returned.
The clink schema enumerates configured clients/roles, including missing
executables, so it is not a replacement availability source.

This reproduces `tools/listmodels.py:86-87,362-365,422-436` at the original candidate:
only the provider-free branch publishes `cli_clients`. It prevents the accepted
empty-API-catalog case from constructing the required executable-present roster.
API-mode operation with `codereview` disabled has the same unexposed source;
that additional branch is source-inspected, not a separately executed probe.

The probe reports **1 passed** because its setup/response assertions succeeded;
the observed integration outcome is a **required capability gap**. The earlier
829 passing tests establish their covered behavior but do not cover this
consumer requirement. Initial C1/C2 pass assessments in this session were
superseded by this observation, without changing the accepted contract.

The user then explicitly authorized the minimal sibling PAL correction and its
verification. The [retained patch](pal-discovery.patch) exposes the existing
`cli_clients` startup snapshot in both discovery modes and adds
`cli_clients_observed_at: "startup"`. The latter scopes timing to CLI observations
without claiming the API model catalog is a startup snapshot. Existing
provider-free fields are preserved. Discovery performs no new CLI launch,
executable resolution, authentication probe or configuration change.

Four regression cases cover provider-free mode, normal API discovery, an empty
restricted API catalog and disabled `codereview`, with present/missing fake CLIs.
They failed before the fix and passed afterward. The
[corrected original probe](empty-api-discovery-fixed.json) now exposes the CLI
observations and preserves the API catalog text byte-for-byte in the retained
sanitized captures. This resolves the recorded gap without weaker eligibility.

[Validation](pal-fix-validation.json) records the exact commands, run IDs and hashes:

- Before changes: complete PAL quality checks passed, **3,445 tests passed**.
- After changes: **74 targeted tests passed**.
- Complete post-fix quality checks: **3,449 passed, 17 skipped, 26 deselected,
  19 subtests passed**; lint, formatting and import sorting passed.
- Corrected discovery capture: **1 probe passed**; no live API inference.

The three reviewed files were applied to the sibling PAL worktree after checking
its baseline and absence of conflicting edits. Their hashes match the tested
copy; reverse-application of the retained patch validates against that worktree.

## Live review, continuation and parity (C3–C5/C8)

Fixtures were restored from `../fixtures/` under
`/tmp/clink-contract-20261023/live/`. `project/` is the working directory;
`criteria/` and `snapshots/` are outside it. The selected snapshot differs from
the worktree file. No prompt contains fixture contents or receipt markers.
The absent `optional-context.md` is intentional.

- [Claude initial attempt](claude-initial.json): authenticated as
  `claude-sonnet-5-5`, but the first criteria read was denied. The native answer
  correctly reports no performed review. Transport continuation availability
  is not evidence of completed review. All six fixture hashes remained unchanged.
- [agy initial review](agy-initial.json): both intended code/document defects and
  all four file-only markers returned. Native `agy_status: SUCCESS`, no denied
  actions metadata. All six hashes remained unchanged.
- [agy continuation](agy-followup.json): explicit `allow_edits=false`, same PAL
  conversation, inherited client/role/directory, two retained messages, correct
  recalled defects/markers/selected snapshot and missing optional file. No new
  tools were requested; absence of detailed returned telemetry prevents proving
  that no child tools ran.
- [Internal review](internal-review.md): fresh independent agent, same substantive
  criteria and evidence, both defects and all markers returned. Its wrapper
  allows shell-backed read-only file access because that is this host's native
  Read mechanism. No expected answer or other reviewer's findings were supplied.
- [Claude with approved grant](claude-granted-initial.json): fresh default-role
  review on the explicitly sourced temporary PAL server, observed model
  `claude-sonnet-5-5`, five successful reads with criteria first, expected optional
  missing-file result, all four markers and both defects. All six hashes unchanged.
- [Claude continuation](claude-granted-followup.json): same conversation with
  two retained messages, inherited directory/client/role and explicit
  `allow_edits=false`; recalled defects/markers/snapshot/absence with no returned
  tool calls. All six hashes unchanged.

Claude split the candidate defect and its caller impact into two native findings
and added an explicitly unspecified-input observation. These are report-quality
observations, not additional defects or new acceptance requirements. Its native
output is retained. Both eligible external providers completed the fixture;
the internal reviewer received equivalent relevant criteria/evidence. The
separately launched PAL discovers Codex on its own PATH, unlike the connected
server's startup snapshot; OpenAI authorship still excludes it from this roster.

The user explicitly approved a temporary Claude read grant after the denied
attempt. The staged manifest preserves `--model sonnet` and
`--permission-mode default`, adds only
`--allowedTools Read(//tmp/clink-contract-20261023/**)`, and uses the same default
role prompt. It is loaded by a separate MCP stdio server from the candidate
source using `CLI_CLIENTS_CONFIG_PATH=/tmp/clink-contract-20261023/clients`.
No `~/.pal` override, native settings rewrite, edit/bypass grant or restart of
the connected PAL instance is involved. This is a separately authorized setup
and rerun, not an automatic failed-review retry policy.

The scoped Claude rule follows the
[official absolute Read syntax](https://code.claude.com/docs/en/permissions#how-path-patterns-match).
Agy's existing configuration follows its
[native permission precedence](https://antigravity.google/docs/permissions?tab=cli);
no new agy permission rule was needed here.

## Coverage classification exercise (C7)

| Observed response | Reported outcome |
| --- | --- |
| Claude transport success plus denied first criteria read | No review; no source receipt, findings or approval. |
| Agy useful findings and file-only markers without a detailed read trace | Retain native attributed findings. Mark tested fixture access proven, general receipt/order and actual model unverified. |
| Successful context-dependent agy continuation | Conversation context works for the tested exchange; no-tool execution remains unverified. |
| Upstream denied-action success fixture | Useful partial answer remains attributed; denied action limits coverage despite transport success. |
| Upstream semantic/authentication/timeout/missing-executable failure fixture | Diagnostic/error result, not a completed review or approval. |
| Upstream summary/truncation fixture | Retain useful visible output with output-limit metadata; do not infer full original coverage/completeness. |

Internal/agy agreement on the two toy defects is recorded with their native
severity differences, not promoted to a broad approval or an independent
corroboration claim based on unverified general receipt. Missing telemetry does
not fail C7 or require a PAL tracing feature.

## Current acceptance and next actions

| Criterion | Current status |
| --- | --- |
| C1 | Passed: provider-free/API/unknown distinctions, original gap reproduced, corrected API-empty and disabled-review cases verified |
| C2 | Passed: executable observations exposed in both modes; present/missing clients, roles and explicit identity/author/duplicate roster examples verified |
| C3 | Passed within observed bounds: configured launches preserved, configured versus actual identity separated |
| C4 | Passed: Linux Claude/agy access and unchanged hashes; Claude's read order is observed, agy's order is not independently exposed |
| C5 | Passed: deterministic edit reset/isolation plus Linux Claude/agy live fresh requests and continuations |
| C6 | Passed for the executed failure/output cases |
| C7 | Passed for the recorded reporting exercise; future plugin reporting implementation remains Task 1 |
| C8 | Passed: internal/Claude/agy evidence parity, complete eligible external roster, independent conversations and sequential scheduling |

Minimum verified **revision**: PAL
`c73dab7d8cf9d791961b84614a0e082b74ee5569`. Its diff from base
`d25c2d029a5d157935aa9bb836c18e9725969b8f` exactly matches [pal-discovery.patch](pal-discovery.patch),
SHA-256 `b8de8e14faea5b87c242b20342a32481b5d056029ab07127b170f73f2c098475`.
[pal-fix-validation.json](pal-fix-validation.json) pins all three changed files.
The tested source was committed without code changes; this is not a published
release, and unmodified 1.4.2 does not satisfy C1/C2. To reproduce, check out the
verified revision (or apply the retained patch to its base) and use the recorded
environment/commands. No older-PAL compatibility is claimed.

The final independent review found no remaining material findings and confirmed
closure of C1/C2 for this exact candidate. Existing C3–C8 evidence is retained
for unchanged clink execution, parsers, conversation handling and native
configuration; the metadata-only correction does not require repeating those
paid live calls. Linux revalidation did not repeat the historical same-author
Codex integration check, which is outside the eligible external roster.

**Delivery follow-up (PAL maintainer):** publish/release the reviewed commit and
update/restart the intended PAL installation before relying on API-mode clink
discovery there. Completion evidence is a discovery response containing the
new CLI metadata from that corrected installation. Publication/activation is
outside this Task 0 verification request; the currently connected PAL process
was not updated. Task 1 may use the verified build contract; Tasks 1–3 remain pending.
