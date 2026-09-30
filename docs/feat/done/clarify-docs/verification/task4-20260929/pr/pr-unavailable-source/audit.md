# Coordinator trace audit

Editor instruction calls at ordinal 19 finish before the source/destination checks at 25. The editor reads only its request, frozen entry/shared instructions, context.md, immutable remote-body.md and its selected output. The destination existence check is metadata only. The single patch at 34 creates drafts/pr-15.md and the verification read is at 39. No checkout is fabricated and no network call or outside read appears.

Only drafts/pr-15.md changes by before/after hashes; both fixture inputs remain byte-identical. The draft marks missing commit IDs/diff/source/test results, assigns revisions/diff/test output to the PR author, and retains product-owner-confirmed intent plus the pending badge decision. No tests run or runtime delivery is claimed.

Both reader traces are audited against their exact request/artifact manifests; no other content read or write appears. Their artifact bytes reproduce the immutable remote body and selected local output. Model metadata records gpt-6-astra, xhigh, summary none; temperature/build are unrecorded. No oracle or editor-only evidence reaches the readers. Shared-filesystem manifest restrictions are not OS isolation. Default initial shell startup emits an ambient navi logging error without disclosing additional subject matter. Independent grading remains separate from this coordinator audit.

