# Initial verifier source review: normalize before uniqueness

Reviewer: `code-reviewer`, `/root/bootstrap_review`, read-only; no actor/test/PAL
execution. The source review supports preservation of the original audit checks,
separate listing provenance and the inherited recomputation/gate chain.

The reviewer identified one narrow contract gap in `listing_audit.py`: raw-name
distinctness could admit the same selected file once as `plugins/kk/agents/...`
and once as an absolute bundle path. Both normalize to the same instruction file,
violating the declaration's distinct normalized paths requirement. The reviewer
requested a uniqueness check after deriving bundle-relative paths and a focused
absolute/relative alias negative control before freeze.

The parent implemented both. The initial eleven-test run remains in
[listing-tests.txt](checks/listing-tests.txt); the final twelve-test run passes in
2.839 seconds, retained in [listing-tests-final.txt](checks/listing-tests-final.txt).
No capture or original frozen file changed. Final independent disposition follows
in a separate review record.
