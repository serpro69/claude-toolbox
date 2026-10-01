# Staging and capture notes

The two scenarios use separate workspaces under
`/tmp/clarify-issue-task2/regressions/`, outside every `SKILL.md` ancestor.
Their sibling `instructions/` directory contains the frozen full entry point and
procedure. Neither editor workspace contains a snapshot staging directory, eval
specification, or oracle. Original and revised readers each receive a separate
copy of their sole allowed artifact.

The staging commands created real local Git repositories, committed the supplied
base and head snapshots, and tagged them `review-base` and `review-head`. Both
leave head checked out. `staging-command-log.json` records every successful Git
command and result; `git-revisions.txt` and `git-diff.patch` preserve the actual
revision IDs and diff. Author/committer identities and timestamps were synthetic.
Signing and hooks were disabled for these fixture-creation commands only.

Every editor and reader prompt requires non-login shell commands. Editor Git
queries must disable optional locks. Before/after inventories include every file,
including Git metadata. Git metadata is copied directly into ZIP archives with
its original member paths and per-member hashes, avoiding embedded repositories
in the tracked evidence. No live checkout metadata was deleted for packaging.

Two coordinator-only command attempts were blocked before execution by broad
PreToolUse path patterns. The first staging command attempted to inherit the shell
environment and matched the `.env` pattern; successful staging instead supplied
an explicit minimal subprocess environment. The first contract capture command's
metadata-prefix comparison matched the `.git/` pattern; the successful capture
compared complete metadata member inventories. Neither rejected command executed,
and neither rejection occurred in an editor, reader or grader run. Their original
tool calls and rejection results remain in coordinator rollout
`01a0f8b7-5c3f-7890-b1c9-0376b972d87e`.

Participant prompts were saved with native `apply_patch` before dispatch; exact
file manifests, settings and native submission receipts are preserved per role.
Session capture exports complete visible tool call/result records, visible
assistant messages and task lifecycle events from the native rollout JSONL.
Hidden reasoning and automatically supplied system/repository boilerplate are
excluded. The transport encrypts task messages; receipts retain the native call
and response while the corresponding pre-existing prompt files provide plaintext.
No prompt was reconstructed after its run.

All participants use fresh `default` agents with `fork_turns=none` and no model or
effort overrides. Captured actual settings are `gpt-6-astra`, effort `max` for both
editors and all four readers. The normal harness still automatically supplies its
system/repository boilerplate; isolation depends on the recorded explicit file
manifests and trace audit, not on shared filesystem access controls.
