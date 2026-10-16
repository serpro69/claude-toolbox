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

## Formatting-preservation follow-up

Unchanged explicit MCP server tables are now copied from the original TOML
byte-for-byte. A Python standard-library scanner locates table spans, skipping
strings, comments, and nested array values. `yq` interprets each table path and
checks each server's complete source against its merged value before preservation.
Only changed or repaired registrations are re-rendered. Original upstream MCP
values are read before substitutions, avoiding `yq`'s loss of quotes around dotted
server names. The helper stays embedded in the sync script so an older script's
self-update handoff does not need to copy a new helper file.

- `bash test/test-template-sync.sh`: 146 cases and 265 assertions passed; three
  existing network-dependent checks skipped. Tests ran with Python 3.10.12 and
  `yq` 4.52.5.
- Byte comparisons cover Capy's compact launch-argument formatting, comments,
  quoting, table order, nested tables, repeated syncs, CRLF, and missing final
  newlines. A changed upstream registration does not reformat other servers.
  First-sync and conflicting dotted server names retain their correct meaning.
- The installed Capy v0.17.1 was run in a disposable project through
  `setup --platform codex` → sync → setup → sync. The entire `config.toml` stayed
  byte-identical. Python 3.12's independent `tomllib` parser also agreed with `yq`
  on the resulting configuration.
- Independent review found that a multiline string's closing line beginning
  with `#` could be misclassified as a comment, causing a failed fragment parse
  and template fallback. A regression reproduced the failure. The scanner now
  records actual comment/blank lines during lexical scanning; regression fixtures
  cover both basic and literal multiline strings. Re-review approved the fix
  with no remaining findings.
- Shell syntax and whitespace checks passed. ShellCheck warnings matched the
  baseline. Python 3 is now a documented prerequisite; no Python packages or
  automatic Capy setup step were added.

The broader environment limitations below were observed during the initial
placement fix. The formatting follow-up reran the focused sync suite and actual
Capy integration; it does not claim a fresh pass of the unrelated blocked suites.

## Initial placement-fix verification (c17570cc)

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
