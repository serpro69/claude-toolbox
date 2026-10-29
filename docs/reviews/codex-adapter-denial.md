# Codex adapter denial diagnostic fix

Status: implemented, verified and reviewed (2026-10-29).

The patch and MCP adapters previously ran `guard.sh` as an unguarded command
under an `ERR` trap. A normal guard denial exits 2 and therefore also emitted
the misleading "adapter could not run; repair the hook" diagnostic.

The fix preserves exit 0 and the guard's explained exit 2, while
retaining `fail_closed` for unexpected statuses and adapter setup failures.
The existing Bash adapter provides the same status-handling pattern.

The user applied the adapter patch directly after the guard's `selfmod` rule
blocked agent edits. No policy exception was required. The reviewed baseline
is local HEAD `1d4a48f72456fba94a19542c8954a632ec9085e3`; the candidate is the
unstaged adapter, hook-test and configuration-documentation changes.

Verification:

- Tightened hook tests failed against the original adapters on the duplicate
  stderr diagnostic: run `d8f03019-9df2-4e55-a707-91e32f796f3a`.
- `bash test/test-codex-hooks.sh` passes after the fix: 30 cases, 211 assertions,
  run `ac307c6f-ae65-4e3f-905a-e6bba4d6d696`. Coverage includes policy denials,
  patch deletion outside temporary roots, silent allows, guard-generated
  failure denials, missing wrappers and closed input.
- `bash test/test-codex-structure.sh` passes with installed Python 3.12 on PATH:
  run `66e29d75-dcf4-44a5-9ad4-ce15458478f1`. The first attempt under default
  Python 3.10 failed TOML validation because no parser was available (run
  `68ab4fae-1020-4fa7-9ed7-3eff2b00a6a7`); no TOML sources changed.
- `git diff --check` passes. No generated artifacts were changed.

Independent code-reviewer (GPT-6.1 Sol): APPROVE, no findings. It inspected all
four changed files and four unchanged dependencies; execution results above
were supplied as author-attributed evidence, not independently rerun.

External review through PAL's Claude CLI: APPROVE (source review only), no
P0/P1/P2 findings; one optional P3 documentation-placement suggestion.
No API provider was configured. Claude was the only available eligible CLI;
its provider was initially assumed to be Anthropic from PAL's shipped mapping,
and the response reported `claude-opus-5-5`. The configured model was not
available in discovery. The absent Codex and agy executables were not candidates;
Gemini is retired. An operator declaration in repository agent instructions
overrides assumed mappings.

External execution completed successfully. Its reported coverage includes the
four criteria, the selected diff, all four changed files and four unchanged
dependencies, plus targeted guard-engine and Codex-documentation excerpts.
The large PAL trace was truncated in this session, so complete source receipt
was not independently verified and no corroboration claim is made. Two optional
shell-semantics probes were denied by reviewer permissions; neither reviewer
ran the test suites. External review of the execution logs was optional and
not performed; the captured red/green runs above remain author evidence.

Optional external P3 follow-up (unassigned): consider moving the accurate
Codex-specific paragraph at `docs/user-guide/configuration.md:173` to
`docs/providers/codex.md`, or linking it there. Author context: retained here
because this shared hooks section already discusses Codex adapters, and moving
the paragraph is not needed for the diagnostic fix. At the next documentation
reorganization, choose one home and verify the cross-link resolves.

The external reviewer also observed that a syntactically corrupted guard
wrapper can itself exit 2 without denial JSON. This still blocks the tool,
matches the existing Bash adapter behavior, and was explicitly reported as
requiring no change. No new guarantee for corrupt wrapper diagnostics is
claimed by this fix.

Scope limits: live Codex presentation and downstream installations were not
exercised. This is a local code fix, not a downstream rollout claim. No systemic
P0/P1 findings to index or required code follow-ups were identified.
