# Evidence format

Each accepted participant has three equivalent, deterministically filtered exports:

- `*-native.jsonl`, `*-trace.jsonl` and `*-tool-messages.jsonl` retain every visible
  assistant message, inbound agent message, tool call and tool result. Original
  source ordinals and retained source lines are preserved.
- System/developer harness boilerplate, initial environment setup, hidden
  reasoning, session boilerplate and duplicate event wrappers are excluded.

`tool_message_records` in `*-capture-metadata.json` counts the retained visible
records. `native_sha256` identifies the unchanged original session outside this
repository; `export_sha256` identifies the filtered portable export. Actual
settings are normalized to model, effort and collaboration mode without publishing
harness instructions. The 22 editor/reader sessions retain all 141 visible records.

`*-native-integrity.json` compares the filtered projection with the original session,
checks completion, records actual model/settings, verifies that the plaintext
prompt predates the dispatch, and links the dispatch ciphertext to its child's
inbound ciphertext. Files named `*-submission.json` additionally preserve the
exact dispatch message as a JSON string, including its terminal newline. These
envelopes began with case 3's original reader. The seven earlier participants have
the exact pre-dispatch plaintext file and matching native receipts; no prompt was
reconstructed after dispatch.

All submitted plaintext prompts include exactly one terminal newline, matching
the files written with native `apply_patch`. Ciphertext cannot independently
establish the plaintext bytes; this transport limitation is explicit.

The filtered sessions are the portable source record. Original session paths and
temporary workspace paths identify provenance; snapshots and visible traces
preserve the behavioral evidence after those original paths disappear.

The first grader was interrupted when this packaging correction was requested.
Its incomplete attempt remains in `grader/`, explicitly invalid for final
acceptance. Two first-attempt tool outputs that printed harness fragments are
redacted, with original ordinals and record hashes retained. No editor/reader
visible record, artifact, answer, assertion or prompt changed. Final verdicts use
a fresh grader against the stable filtered package; see `filter-correction.json`.
