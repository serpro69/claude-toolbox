The valid rerun's complete editor trace contains seven calls and seven responses, a final answer
and completion event, with no missing or truncated tool response. Each shell
uses login:false. The operational manifest loads at ordinal 14, full SKILL.md at
19 and shared procedure at 24, before all three subject files at 29. Only the
selected issue-draft.md is patched (ordinals 40 and 52) and reread at 45. The second
patch removes an unsupported exclusivity word before completion.

The snapshot comparison confirms only issue-draft.md changed; requirements.md
and export.py are byte-identical. Tool/message inspection shows no network,
source execution, reproduction, PR setup, out-of-manifest read or other write.
No oracle or eval specification was exposed. Shared filesystem access was
controlled by prompt and audited; it was not OS isolation. Prompt, raw trace,
encrypted dispatch/incoming linkage, final output and hashes are retained.

Attempt 01 is retained under attempt-01-prompt-mismatch/ and invalidated for a
terminal-newline mismatch. The final rerun uses child editor17_retry1 and the
pre-dispatch JSON's exact message bytes (one terminal LF).

The valid rerun's two fresh readers each execute exactly one cat of their own
artifact and nothing else. Their tool responses are complete, login:false is
set, and both final answers are retained. Model/settings match. Reader artifacts
are byte-identical to the declared before/after snapshots; neither reader receives
source files, editor context, specifications or oracle material.
