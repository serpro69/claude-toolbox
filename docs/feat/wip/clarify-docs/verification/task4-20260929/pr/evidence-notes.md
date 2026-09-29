# Evidence handling

Each editor and reader was a fresh general-purpose agent with `fork_turns="none"`.
Only one child ran at a time until the parent explicitly expanded the allowance to
two slots. Only the final visibility retry-3 original/revised reader pair ran
concurrently, using separate fresh sessions and artifact manifests. The request files were written
before dispatch; the one-line spawn instruction points exclusively to that request.
Requests contain exact allowed-file manifests. Fixture oracles remain outside editor
and reader workspaces. Reader artifacts are byte copies of the corresponding frozen
before/after output, with no extra linked sources in these four PR reader cases.

Raw role traces contain every tool call/result and visible assistant message from
the native rollout. Readable Markdown traces decode nested `functions.exec` tool
results. Hidden reasoning and injected system/developer/repository boilerplate are
omitted. Final responses are extracted from actual `phase=final_answer` messages.
Metadata preserves native thread IDs, session lineage, model ID and reasoning effort.
The native model ID is `gpt-6-astra`; effort is `xhigh`, summary is `none`. No model
build or temperature is recorded, so neither is invented.

Native inter-agent call arguments encrypt their message fields. Each `*-dispatch.jsonl`
preserves that actual call, result, and child-start receipt. `*-spawn.txt` records the
plaintext fixed-template dispatch instruction; the request read in each child's
first tool call independently establishes which plaintext request it consumed.
The initial grader's coordinator follow-up is separately preserved in
`grading/grader-followup.md` with its raw dispatch receipt. Native ciphertext is
retained without attempting to reconstruct hidden message bodies; the grading
findings themselves are recorded in the grader's plaintext verdict and final output.

The initial repository revision is recorded in each manifest. Cases 11–13 use real
local Git commits and `review-base`/`review-head` refs, with process-local commit and
tag signing disabled. `git-evidence.txt`, `git-refs.json`, and `git-diff.txt` preserve
their revisions, trees and actual increments. Original fixture snapshots remain in
`scenario/test-files/snapshots/`. Snapshot setup did not change the toolbox repository.

All reader artifact copies were checked against their evidence counterparts, and
every recorded tool-call ID has a matching result. Before/after SHA256 inventories
cover all staged fixture/source/output files excluding Git metadata. Requests,
instruction files and final evidence also have hash inventories. Shared instruction
bytes are copied once under `instructions/`; full snapshot hashes record the frozen
instruction tree without duplicating it in each case.

These are shared-filesystem controls, not OS isolation. Agents also receive standard
harness and repository AGENTS instructions in fresh sessions. Default first shell
calls trigger ambient startup and a failed navi log initialization; the returned
content contains no additional evaluation subject matter. No tool trace exposes an
oracle or unallowed subject-matter source to an editor/reader. The manual audit does
not establish behavior outside these observed runs or improved human comprehension.
