# Task 4 issue verification protocol

This tree owns scenarios 16–24 only. Canonical SKILL.md and shared procedure are
copied byte-for-byte under instructions/. All scenario input snapshots, fixed
eval specifications and existing oracles were captured before editor dispatch.
Only test-files contents were copied into each /private/tmp workspace, which is
outside a SKILL.md ancestor. No PR repository or live service was set up.

Each editor and each original/revised reader uses a new default agent with
fork_turns=none and no model or effort override. At most one child of this
coordinator runs at a time. The actual model/settings come from exported session
turn_context records, not an assumption. All request text and neutral reader
questions are preserved unchanged. Descriptions, manifests and the ability to
load the skill are available for non-trigger selection; its body is not preloaded.

Prompts are authored with native apply_patch before dispatch. Visible-session
JSONL exports retain original-byte evaluation messages, every tool call/result,
visible assistant commentary/final answers, and task boundary events. They exclude
system/developer harness boilerplate, hidden reasoning, and unrelated state. Native
session files remain untouched; their hashes establish provenance without copying
privileged context into the repository. Derived traces retain every tool call and
response plus visible assistant messages. Metadata records prompt, native-source
and visible-export hashes, dispatch receipts, model/settings, call/output
pairing and truncation signals. Encrypted outgoing/incoming payload equality
links dispatch to each child; independent plaintext decryption is unavailable.

Before/after snapshots and SHA-256 maps retain original bytes. Readers receive
only their artifact copied as artifact.md in a separate workspace. A fresh
fixture-capable default grader receives the fixed oracle, full records, sources,
both artifacts and reader answers. Its findings do not replace the complete-trace
allowlist audit. No shared-filesystem boundary is claimed to be OS isolation.

Loaded testing instructions: canonical /kk:test SKILL.md, shared capy protocol,
shared profile-detection procedure, and skill-md detection. Parent performed full
profile detection and pre-write loading. Applicable skill-md/python profiles have
no test/ index. This work executes established manual evals without implementation
authoring. Remote knowledge search was skipped under the explicit offline rule.
Pre-dispatch JSON artifacts for later participants contain the exact decoded
message bytes as an additional check against terminal-newline mistakes. Case 17's
first attempt is retained as invalid because its saved and dispatched terminal
newlines differed; its valid rerun uses a distinct fresh child. The early case 18
agent-slot rejection launched no participant and remains scheduling evidence.

The temporary export helper only snapshots and exports existing evidence; it is
not a new repository evaluation harness.
