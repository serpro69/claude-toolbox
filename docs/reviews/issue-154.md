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

The additional isolated `code-reviewer` could not run: its tool allowlist requires
Read/Grep/Glob, which this Codex runtime did not expose. The external reviewer
completed the independent review. Follow-up: map the reviewer's permitted file
reads to available Codex tools; deferred because tool permissions are separate
from plugin-root resolution.

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
