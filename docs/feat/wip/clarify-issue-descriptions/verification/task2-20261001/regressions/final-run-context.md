# Final PR regression grading context

The subjects of this grade are `contract-only-pr-retry/` and
`destination-visibility-retry/`, using the full frozen files in
`instructions-retry/`. Both eval specifications and oracles are unchanged.
The editors and revised readers are independent fresh sessions. No earlier editor
result or grader verdict is part of this grader's input.

The two independent original-reader runs are reused with explicit parent
authorization: their source artifacts, fixed questions and model/settings are
unchanged. Their evidence has been copied byte-for-byte into the respective
retry directories. These copies retain their actual session IDs, original
prompt locations and allowed-reading paths; do not resolve those locations
outside this grader's manifest. Compare their artifact bytes with each retry's
before/workspace/pr-draft.md, and compare the complete reader settings and questions.
There is no newly claimed original-reader execution.

Original-reader session IDs:

- Contract: `01a0f8ba-6154-7d63-ad55-e058f55559a7`.
- Visibility: `01a0f8ba-d7e4-7e11-86ef-22bad467d540`.

Git metadata is retained in ZIP files whose entries preserve the original member
names. For audits, iterate these listed entries and hash their bytes in memory;
there is no need to extract them or access any live Git repository.
