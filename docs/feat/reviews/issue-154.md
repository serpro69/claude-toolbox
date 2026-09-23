# Issue #154 verification

Codex generation now replaces Claude shell lookup instructions with resolution
from the installed skill's absolute `SKILL.md` path. Delegating agents pass the
absolute plugin root under `## Plugin Root`; generated sub-agents report missing
input instead of discovering a root themselves.

## Review

External review through `/kk:review-code` (Gemini 3.1 Pro) identified one medium
coverage gap: targeted file assertions would miss variable leakage in future
skills. Addressed by scanning every generated skill and agent for
`TOOLBOX_PLUGIN_ROOT`, excluding profile authoring documentation intentionally.
No systemic P0/P1 findings to index.

The initial isolated `code-reviewer` could not run: its instructions required
Read/Grep/Glob and claimed it had no shell, but this Codex runtime exposed file
inspection through native execution tools. The external reviewer completed that
review. The subsequent tool-access fix maps each agent's declared operations to
native Codex tools while retaining read-only restrictions, narrower grader and
resolver scopes, and explicit errors for unsupported tool declarations.

Tool-access verification covers all six generated roles, unsupported declarations,
and the difference between an omitted tool list and an explicit empty list.
The regenerated `code-reviewer` completed a live independent review: native
`cat`, `sed`, `rg`, and `rg --files` reads through `functions.exec` and
`exec_command`, plus Capy search, all worked. No tool-name incompatibility
blocked inspection. The other five roles were checked statically, not run live.
The code reviewer approved the tool-access change. External review suggested two
low-severity diagnostics improvements: clarified the test's unexpected-file
message; the proposed additional agent-name context is already supplied by the
outer `GenerateAgents` error wrapper. The explicit-empty-list case was also
reproduced and corrected before completion. No systemic P0/P1 findings to index.

## Verification and existing failures

- All Go packages pass `go test ./...`.
- Plugin structure: 182 assertions pass. Codex structure: 29 assertions pass
  using the installed Python 3.12 (system Python 3.10 lacks a TOML parser).
- Initially, seven of nine shell suites passed. The five failures below also
  reproduced in a clean `git archive HEAD` checkout at `60f5564`, before this fix.

Baseline test maintenance resolved in the follow-up:

- `test/test-claude-extra.sh`: updated three heading checks for the current
  levels in `.claude/CLAUDE.extra.md`. Replaced the stale project-content check
  with checks for the `@AGENTS.md` import and the expected sections in
  `AGENTS.md`. The duplicate behavioral-heading check now covers all heading
  levels.
- `test/test-manifest-jq.sh`: aligned the example manifest with the existing
  `gpt-6-astra` value used by the generated fixture and template-sync defaults.

Follow-up verification: all nine shell suites pass, with 600 assertions and
zero failures, using Python 3.12 for TOML parsing. Shell syntax checks pass.
Independent external review identified an end-of-line anchor that could let a
duplicate behavioral heading with trailing whitespace or a suffix escape the
negative check. Removed that anchor and reran the affected suite successfully.
No systemic P0/P1 findings to index.

Remaining generation follow-up, outside the failing-test fixes:

- Generation also copies the existing canonical `twelve-factor` profile into an
  untracked Codex directory. That unrelated output is excluded from this fix;
  regenerate and commit it with the twelve-factor work.
