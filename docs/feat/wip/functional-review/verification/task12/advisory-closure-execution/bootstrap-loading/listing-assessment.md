# Independent classification of instruction metadata listings

Reviewer: `code-reviewer`, `/root/bootstrap_review`, read-only continuation after
fresh bindings. Disposition: **COMMENT — bounded verifier correction warranted**.
No source changes, actors, tests or PAL calls were performed by the reviewer.

The reviewer inspected candidate events/report, the frozen prompt/declaration,
original auditor and transport policy. Events 52/53 list six `agents/*.md`
filenames; events 60/61 list seventeen `skills/{_shared,review-code}/*.md`
filenames. Both use the selected plugin root and return successful, complete
filename listings. These are contract-allowed metadata operations: the prompt
requires direct Reads for instruction bytes and prohibits subject investigation,
external access, packets and additional shell commands. It does not prohibit
instruction-file listings. The inherited transport also permits Glob. Neither
listing establishes an instruction-read receipt.

**P2 — `preflight_audit.py:112`, Python code-quality checklist, confidence 99%:**
blanket Glob rejection blocks permitted instruction discovery. Actual paired
events, explicit prompt boundaries and transport policy agree. Add a separately
identified verifier accepting only validated instruction metadata listings;
preserve the original auditor, rejection and captures. No actor rerun is needed.

The successor must validate the exact bundle base, narrowly allowed patterns,
successful paired results, complete counts and normalized filenames against
frozen instruction paths. Reject traversal, outside paths, evaluator/subject
locations and unexpected tools. Retain listing provenance separately and never
count listings as Reads. Preserve all original receipt, model, effort, identity
and manual-access checks. Review, test and freeze the verifier before recomputing
both captures. Complete receipt inventory, other access, retention, independent
completion review and final guard execution remain separate checks. No broader
preflight approval or acceptance change follows from this classification.
