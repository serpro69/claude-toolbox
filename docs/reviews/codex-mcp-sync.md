# Codex MCP sync fix verification

The sync merge converted downstream MCP registrations to JSON and inserted them
into the template with `yq`. With `yq` 4.52.5, the TOML encoder appended an inline
`mcp_servers` assignment inside the final `[tui]` table. Capy's setup then added a
separate root-level registration, leaving the misplaced copy behind.

The fix renders explicit server tables, recovers misplaced TUI registrations,
prefers complete valid root entries over stale copies, and parses the candidate
output to verify its MCP map before accepting it. Quoted server names are
compatible with Capy's table parser. Nested settings remain inline within each
server table.

## Verification

- The regression failed before the fix: the parsed root Capy command was `null`.
- `bash test/test-template-sync.sh`: 144 cases, 256 assertions passed. Three
  existing network-dependent version-resolution checks were skipped.
- Covered explicit, inline, misplaced, and subsequently repaired registrations;
  owner arguments; nested environment settings; dotted server names; repeated
  sync; empty/first-sync configurations; and upstream precedence.
- A temporary copy of the actual `firestore2csv` configuration was passed through
  the fixed merge. Python 3.12's independent `tomllib` parser confirmed that the
  root Capy registration was unchanged, `[tui]` contained no MCP registration,
  and no server names were lost. The original project was not modified.
- Shell syntax checks passed. ShellCheck warnings matched the unchanged baseline.
  Whitespace checks passed with space indentation allowed, matching these files;
  the user's global Git whitespace setting otherwise flags their existing style.
- An independent code reviewer approved the three changed implementation, test,
  and provider-documentation files with no findings. No findings required indexing.
  The review was static; Capy setup itself was not executed.

## Broader checks and environment limits

All ten shell suites were attempted in a temporary snapshot of committed files
with this fix applied, using the available Python 3.12 for TOML validation. Eight
passed: Claude extras, Codex hooks, Codex structure, CPR, hooks, plugin structure,
semantic version comparison, and template sync.

`test-manifest-jq.sh` and `test-template-cleanup.sh` could not complete their schema
checks because `uv` tried to write to its read-only cache outside the sandbox.
The cleanup suite also encountered the user's unavailable Git signing key in its
temporary repositories. These environment checks remain unverified; rerun both
suites with a writable `uv` cache and commit signing disabled for test repositories.
No unrelated test or application behavior was changed to bypass them.

The initial hook-suite attempt in the working checkout failed because its
toolbox-only fixture reads the locally modified `.codex/hooks.json`, which already
contains Capy hooks. It passed in the clean snapshot; those local changes were
preserved.

The additional PAL/Gemini review failed because the configured API key was
rejected. The independent code-reviewer review completed successfully.
