# PAL contract verification — partial

Date: 2026-10-22. Task 0 is incomplete; this record does not authorize Task 1.
Requirements remain the corrected [C1–C8 contract](../design.md#task-0-acceptance-contract).
No minimum fully verified PAL revision has been established.

## Candidate and evidence

- Toolbox baseline: `5d0c5dd1e30ceb37b56bd83a8c61add853012f8c`, initially clean.
- Connected PAL reports `1.4.2`, provider-free mode, zero configured API providers/models. See [version](version.json), [discovery](listmodels.json) and the [host-exposed tool declarations](tool-surface.txt).
- Local PAL checkout: `d25c2d029a5d157935aa9bb836c18e9725969b8f` (`v1.4.2-4-gd25c2d0`), clean. The cached 1.4.2 package's `direct_url.json` names that same commit. SHA-256 comparisons matched checkout/package copies of `tools/clink.py`, `clink/registry.py`, and both Claude/agy parsers. Runtime process inspection was unavailable; package provenance is not proof of the exact running process's source.
- Installed CLI versions: Claude Code `2.1.296`, Gemini `0.65.0`, Codex `0.163.0`; agy was `1.3.5` for the original denial and `1.4.5` for the later successful scoped-read check. The agent did not upgrade agy.
- The user selected agy for Google and excluded Gemini for this run. OpenAI authored the fixture, so Codex is excluded from independent external review. The external roster is Claude/Anthropic and agy/Google, dispatched sequentially. The user subsequently requested a separate Codex integration check; that is recorded without counting it as an independent supporter or changing the author-exclusion policy. PAL's client name alone is not a model-provider identity contract.

## Recorded attempts

| Attempt | Actual result | Evidence |
| --- | --- | --- |
| Claude, fresh MCP request | Authentication failure; exit 1, PAL error, no continuation. Native `subtype: success` did not hide `is_error: true`. | [Initial response](claude-initial.json) |
| agy, fresh MCP request | Native headless `read_file` permission denied; exit 0 still became a PAL error. No continuation or source receipt. | [agy response](agy-initial.json) |
| Claude, fresh MCP request after the user reauthenticated | Inference succeeded with `claude-sonnet-5-5`; two denied criteria reads were returned in metadata. The answer explicitly reported no completed review. | [Post-auth response](claude-after-auth.json) |
| Claude MCP follow-up | Reused its own PAL conversation, retained two messages, inherited Claude/role/directory, and recalled the prior denied path without new source reads. `allow_edits=false` was explicit. | [Follow-up](claude-followup.json) |
| Claude direct CLI with user-authorized `--allowedTools Read` | Exit 0, no permission denials; returned all four file-only markers and identified the attempt-zero code defect and contradictory proposal. All six fixture hashes were unchanged. | [Read-grant probe](claude-read-grant.json) |
| Claude default-role MCP request after manifest repair/restart | Exit 0, no native permission denials; returned command contains `--allowedTools Read,Glob,Grep`. Native model is `claude-fable-5-1`. Tool results show criteria first, five successful reads, and the expected absent optional file. Both intended defects and all four markers returned; six fixture hashes unchanged. | [Default-role MCP review](claude-default-mcp.json) |
| Claude default-role MCP continuation | Same PAL conversation, two retained messages, inherited default role and directory, explicit `allow_edits=false`; recalled defects and all markers without new tool calls. Fixture hashes unchanged. | [Default-role follow-up](claude-default-mcp-followup.json) |
| Codex default-role MCP request | Existing manifest worked without changes. Exit 0; both intended defects and all four markers returned. Six fixture hashes unchanged. PAL removed detailed event traces and returned no actual model identity. | [Codex MCP review](codex-default-mcp.json) |
| Codex default-role MCP continuation | Same PAL conversation, two retained messages, inherited default role/directory, explicit `allow_edits=false`; correctly recalled defects, markers and missing optional file. Six hashes unchanged. No-tools claim is self-reported because PAL removed the trace. | [Codex follow-up](codex-default-mcp-followup.json) |
| agy default-role MCP request with scoped native read permission | agy `1.4.5`, exit 0, `agy_status: SUCCESS`; both intended defects and all four markers returned, no denied-actions metadata. Six hashes unchanged. Model identity and detailed read trace unavailable. | [agy MCP review](agy-default-mcp.json) |
| agy default-role MCP continuation | Same PAL conversation, two retained messages, inherited default role/directory, explicit `allow_edits=false`; correctly recalled defects, markers and missing optional file. Six hashes unchanged. | [agy follow-up](agy-default-mcp-followup.json) |

The earlier direct probe changed the launch permission, not saved user/PAL configuration. It used the same model, role-prompt contents, working directory and user prompt, but invoked Claude directly with `--append-system-prompt-file`; it was **not an MCP/clink run**. The later default-role MCP run separately verifies the user-updated manifest's actual launch arguments and source access. The retained direct review's extra invalid-input advice is a quality observation: invalid-input rejection is unspecified by this fixture, not a new requirement. The later MCP review correctly identifies that absence of validation is not a contract violation. Its opening file count is inaccurate; the returned tool trace establishes five successful reads and one failed optional read. Neither observation adds an acceptance gate.

## Contract status

### Restart and manifest repair

After the user changed the manifest and relaunched the session, the current tool surface exposed no PAL tools. The override at `~/.pal/cli_clients/claude.json` contained only `additional_args`, `safe_args`, and `edit_args`. Inspection of PAL's `CLIClientConfig` and registry establishes that `name` and `command` are required; overrides replace the full client definition. The previous Codex log path was unavailable, so this is a concrete configuration defect and source-backed startup explanation, not a captured startup traceback.

The missing fields were added as `"name": "claude"` and `"command": "claude"`, preserving the user's arguments. The original is backed up at `/private/tmp/clink-contract-20261022/claude-manifest-before-repair.json`. JSON parsing succeeded. This repaired override has no model argument and no explicit roles: Claude's native model configuration applies, and PAL supplies its default role. After the user restarted again, [discovery](listmodels-after-manifest.json) succeeded; the [updated schema](clink-surface-after-manifest.txt) advertises only `default` for Claude. A fresh `role: "default"`, `allow_edits: false` MCP call and its continuation both succeeded with `claude-fable-5-1`. The returned command confirms the loaded read/search grants and generic default prompt. Earlier MCP captures remain evidence for the earlier configuration only.

| ID | Result | Evidence and remaining check |
| --- | --- | --- |
| C1 | Partial | Live provider-free discovery and omission of `codereview` observed. API-available, empty restricted catalog and failed/ambiguous discovery have source-level coverage upstream; no deterministic checks were executed here. |
| C2 | Partial | Four executables and advertised review roles observed; operator selection resolves the current Google duplicate. Complete unknown-identity/duplicate-provider scenario checks remain unrun. |
| C3 | Pass for configuration ownership and identity reporting | Earlier Claude manifest explicitly selected sonnet; the user replacement delegates model choice to native configuration, observed as `claude-fable-5-1`. Codex uses native configuration (`gpt-6-astra`, effort `max`), but returned no observed model identity. agy also returned no model identity on success; its manifest delegates to native selection. Captured launches preserve those configured choices and use no invented per-call model field. Unknown returned identities are disclosed limits allowed by the design, not a failed requirement to expose model telemetry. |
| C4 | Pass for the recorded live fixtures | Claude tool results and agy/Codex file-only markers demonstrate external criteria/snapshot access; six hashes unchanged in each fixture. Claude instruction order is observed; agy/Codex order is self-reported. Native permission limits and request-selected directories are recorded. No enforced read-only sandbox is inferred. |
| C5 | Partial | Fresh default-role requests and provider-free, context-dependent Claude, agy and Codex MCP continuations observed with explicit `allow_edits=false` each time. Prior edit-opt-in reset and independent cross-review history checks remain unrun. |
| C6 | Partial | Authentication error, semantic failure despite exit 0, and successful transport with explicit denied-read/no-review output observed. Missing executable, useful partial output, timeout and truncation/summary checks remain unrun. |
| C7 | Pass for recorded reporting exercise | Claude supplies actual tool-use/results; Codex and agy return useful findings without detailed read traces. Their findings remain attributed, while general receipt, read order and actual model remain unverified. File-only markers establish only tested fixture access. No broad approval or independent corroboration is claimed from those limited receipts or the same-provider Codex check. Missing telemetry is a disclosed limit, not a failure or upstream prerequisite. This does not certify the pending plugin reporting implementation. |
| C8 | Partial | Both selected external providers, Claude/Anthropic and agy/Google, completed a source review through MCP with the same fixture contents and initial user prompt. Codex is an additional integration check, not an eligible independent supporter. Internal payload parity and concurrent isolation remain unrun. Sequential scheduling is retained pending isolation evidence. |

## Verified interface facts

`clink` accepts `prompt`, `cli_name`, `role`, `absolute_file_paths`, `images`, `continuation_id`, `working_directory_absolute_path`, `allow_edits`, and `editable_paths`. There is no `allowedTools`, arbitrary CLI-arguments, model, or `file_descriptions` request field. See [tool declarations](tool-surface.txt).

The inspected PAL implementation appends client-level `additional_args` and the selected role's `role_args` to the CLI command (`clink/agents/base.py`, `_build_command`). The current live configuration verifies client-level `"additional_args": ["--allowedTools", "Read,Glob,Grep"]` with PAL's default role. The alternative `codereviewer.role_args` path was source-inspected, not live-tested. These are launch-configuration capabilities, not per-request tool overrides. Registry configuration is cached; a separately started/restarted PAL instance loads a changed manifest. Omitting a role on a fresh conversation selects `default`; on continuation it inherits the saved role. Even with no explicit manifest roles, PAL supplies its generic default prompt.

The earlier direct Claude permission probe was explicitly authorized by the user's proposal and subsequent “try that” instruction. The user then installed the persistent argument override and restarted PAL; the agent repaired only the missing name/command fields. These actions do not authorize general permission bypass. `allow_edits=false` remains required for MCP calls, and no enforced read-only sandbox is claimed.

## Reproduction and outstanding actions

Fixture originals are retained under [fixtures](fixtures/criteria/review.md), with separate `criteria/`, `project/`, and `snapshots/` directories. Restore that tree under a fresh temporary root and substitute that root in the recorded requests. Use `project/` as the launch directory; the other two directories stay outside it. Receipt markers appear only in fixture files, never in the review request. Do not create `optional-context.md`: its absence is intentional. Initial requests omit continuation IDs; follow-ups use only the ID returned by their own successful request.

For the Codex variant, use `/private/tmp/clink-codex-contract-20261022/` (or a fresh substituted root), replace `criteria/review.md` with [codex-criteria.md](fixtures/codex-criteria.md), and initialize the disposable `project/` directory with `git init -q` before dispatch. The other five files retain the original bytes. The original criteria prohibited every shell command; that would prohibit Codex's native file-reading mechanism, so this variant explicitly permits read-only shell commands while still prohibiting edits, tests, delegation and network tools. The changed criteria hash is recorded in both Codex captures. This is a transport/access check, not a controlled comparison of model review quality.

Codex's observed command was `codex exec --json --enable web_search_request`, with neither a model override nor edit-mode arguments. `role: "default"` supplied PAL's generic prompt. No Codex manifest or native settings were changed. PAL strips its event array during normal response handling (`tools/clink.py`, `_prune_metadata`); the returned `events_removed_for_normal` field exposes that loss. There is no requirement to add telemetry merely to pass C7.

### agy scoped-read setup

The installed agy `1.4.5` help exposes no Claude-style `--allowedTools` flag. Its [official CLI permissions documentation](https://antigravity.google/docs/permissions?tab=cli) specifies recursive `read_file(/path)` grants in `~/.gemini/antigravity-cli/settings.json`; deny and ask rules take precedence over allow. Before this repair the settings contained no `permissions` block.

Under the user's request to resolve agy, the agent staged and applied exactly this additional block, retaining all existing settings:

```json
"permissions": {
  "allow": ["read_file(/private/tmp/clink-contract-20261022)"]
}
```

The original settings were backed up at `/private/tmp/agy-read-grant.rf4FUy/settings.before.json` in a private temporary directory. The copy was guarded by a comparison with the original to avoid overwriting concurrent changes. No mode/bypass flag, write grant, shell-command grant, model setting or PAL manifest was changed. Fresh `role: "default"`, `allow_edits: false` MCP requests read the new native setting without a PAL restart. The grant currently remains configured and covers only this fixture tree. Other review inputs outside the workspace require their own deliberate read scopes. To retire the fixture grant later, remove only this owned allow entry, preserving any subsequent user settings; the backup documents the earlier baseline.

Both the review and context-dependent continuation succeeded. File-only markers prove access to the fixture; missing read traces still limit claims about ordering/general coverage. The native `Critical` label for a recoverable toy defect and the suggestion to clarify an already explicit contract are retained quality observations, not additional acceptance requirements. Because the agy binary changed between the original denial and this run, this is verification of the current working configuration, not a controlled attribution of every behavioral difference to the permission rule alone.

| Owner | Reason work remains open | Concrete next action and completion evidence |
| --- | --- | --- |
| Capy operator | `capy_execute` rejected admission with `storage_unavailable`: “captured execution currently requires Linux supervision” on macOS | Restore supported capture or supply a scoped `routing.routine` operator exception. The attempted `python3 -m pytest --version` setup batch never started and returned no run ID. Capy doctor reported v0.18.1; no automated suite was run. |
| Task 0 executor | Required deterministic checks remain unrun | After capture works, run focused upstream discovery/startup, execution-error, safe-default, MCP continuation, output-limit and concurrency checks against the recorded candidate. Retain actual results; source inspection and historical upstream passes are not new execution evidence. |
| Task 0 executor | Verification record and complete roster acceptance are unfinished | Finish C1–C8, internal payload parity and the required independent review before marking Task 0 done. No independent review of this record has yet run. |

No plugin instructions or generated artifacts changed. Authentication and the Claude argument override were supplied by the user; the scoped agy read grant was applied while resolving its access issue. The permission-denied attempts are preserved alongside the successful direct and MCP checks. Claude and agy fixture-access actions are resolved by the linked MCP evidence and are no longer outstanding prerequisites.
