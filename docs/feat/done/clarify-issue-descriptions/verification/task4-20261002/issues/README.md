# Task 4 issue verification — 2026-10-02

Completed: **9 scenarios, 47 PASS, 0 FAIL, 0 PARTIAL**. The independent
[verdicts](grading/verdicts.json) cover every fixed assertion exactly once.
No operative instruction or fixture fix is needed.

| ID | Scenario | Assertions | Final artifact or response | Readers |
| --- | --- | ---: | --- | --- |
| 16 | GitHub bug | 7 PASS | [New draft](github-issue-bug/after/docs/feat/wip/replay/issue-42-draft.md) | Original + revised |
| 17 | Selected local draft | 5 PASS | [Edited draft](issue-local-draft/after/issue-draft.md) | Original + revised |
| 18 | Linear proposal | 6 PASS | [New draft](linear-issue-feature/after/issue-draft.md) | Original + revised |
| 19 | Different destination audience | 6 PASS | [Edited draft](issue-destination-visibility/after/issue-draft.md) | Original + revised |
| 20 | Missing destination | 4 PASS | [Destination question](issue-pasted-missing-destination/editor-final.txt); no writes | N/A |
| 21 | Unavailable supporting source | 7 PASS | [Qualified draft](issue-unavailable-source/after/drafts/issue-21.md) | Original + revised |
| 22 | Unavailable issue body | 4 PASS | [Body request](issue-unavailable-body/editor-final.txt); no writes | N/A |
| 23 | Implement non-trigger | 4 PASS | [Source change](issue-implement-non-trigger/after/greeting.py); issue unchanged | N/A |
| 24 | Fix non-trigger | 4 PASS | [Source change](issue-fix-non-trigger/after/timeout.py); issue unchanged | N/A |

Nine fresh final editors and ten separate fresh readers produced 54 complete
call/response pairs. A separate fresh default grader audited all records and
replayed all eight patches to the exact final bytes. Every participant used
`fork_turns=none`, with no model/effort override; recorded settings are
`gpt-6-astra`, `max` effort and default mode. Original/revised readers used
identical neutral questions and settings, receiving only their own artifact.

The tested canonical instruction snapshots are unchanged:

- Entry SHA-256: `1d63b6ed88d7a96257c6ab6471d6763d9df7f33da29b49f50fa26f642584a189`.
- Shared procedure SHA-256: `519f3fa45ae1954154aa292eff8e14abdcfadfb6b2e924214c2092b03a66d681`.
- Source revision: `9a501e1108b9083b83adbc6b550a18d0ff7b2b40`; source/fixture
  bytes and fixed-oracle hashes are in [source-hashes.json](source-hashes.json)
  and [cohort-manifest.json](cohort-manifest.json).

Each scenario retains before/after snapshots, exact editor/reader manifests,
pre-dispatch plaintext prompts, submission JSON where used, hashes, dispatch
receipts, original-byte visible-session JSONL, complete derived tool/message
traces, and final answers. [reader-artifacts.json](reader-artifacts.json) maps
staged reader paths back to durable snapshots. [trace-coverage.json](trace-coverage.json)
records the nineteen final editor/reader audits; the separate
[grader audit](grading/coordinator-audit.md) covers its own complete run.
[Protocol notes](protocol-notes.md) and [portability checks](portability.json)
describe the staging and retained evidence. No native-log or temporary-workspace
access is required to inspect the recorded behavior.

Case 17's [first attempt](issue-local-draft/attempt-01-prompt-mismatch/INVALID.md)
is invalid and excluded because saved/dispatched terminal newlines differed.
Its final fresh rerun is fully retained. Case 18's earlier agent-slot rejection
launched no child and remains scheduling evidence. The grader's first aggregate
metadata presentation was truncated; subsequent complete reads and independent
checks recovered coverage, as documented in its audit. No final editor/reader
tool output is truncated or missing.

These are synthetic offline runs with model readers. They do not certify live
GitHub/Linear connectors, human comprehension improvements, or source correctness
in the non-trigger cases. Shared-filesystem allowlists and complete trace audits
provide the isolation evidence; they are not OS isolation. Encrypted dispatch
cannot be independently decrypted, so exact pre-dispatch plaintext, hashes,
receipts and matching transport records are retained. Durable exports exclude
system/developer harness boilerplate and hidden reasoning; untouched native-log
hashes provide provenance.

