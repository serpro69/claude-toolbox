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
- Seven of nine shell suites pass. The five failures below also reproduce in a
  clean `git archive HEAD` checkout at `60f5564`, before this fix.

Deferred baseline test maintenance, outside issue #154:

- `test/test-claude-extra.sh`: four assertions expect instruction headings to
  reside directly in `.claude/CLAUDE.extra.md` and `CLAUDE.md`. Update the checks
  for the current instruction-file organization.
- `test/test-manifest-jq.sh`: the generated fixture uses `gpt-6-astra`, while the
  example manifest uses `gpt-5.6-sol`. Align the fixture and example model values.
- Generation also copies the existing canonical `twelve-factor` profile into an
  untracked Codex directory. That unrelated output is excluded from this fix;
  regenerate and commit it with the twelve-factor work.
