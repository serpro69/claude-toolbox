The editor has six complete tool call/response pairs, a final answer and completion
event, with no truncated outputs. The allowlist loads at ordinal 14, full SKILL.md
at 19 and shared procedure at 24; all five subject files load at 29. The ls check
there reports the new destination absent. Native apply_patch at 39 creates only
issue-draft.md, which is reread at 44 under the manifest's read_after_creation
permission. Before/after hashes show every input unchanged and one added draft.

All shell calls use login:false. Complete trace inspection finds no network,
subject execution, PR setup, out-of-manifest read, extra report or other write.
The editor uses the supplied sharing context. The exact request, pre-dispatch
plaintext/JSON, settings, transport linkage and original bytes are retained.

editor-dispatch-attempts.jsonl also preserves the earlier agent-thread-limit
rejection. It launched no child and is a scheduling failure, not a behavioral
attempt. The actual successful dispatch matches the saved message's one terminal
LF. Both fresh readers execute exactly one cat of their respective artifact with
login:false and no other access. Their outputs and final answers are complete;
model/settings match. Reader-artifact hashes map back to the retained before/after
snapshots. Independent per-assertion grading remains separate.
