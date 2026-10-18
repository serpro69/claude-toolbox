# Independent source review: historical evidence integrity

Reviewer: `code-reviewer`, `/root/bootstrap_review`, fresh read-only agent without
authorship history. PAL remains user-deferred. The reviewer loaded its common
methodology and all four Python checklists before subject inspection. Installed
0.23.0 lacks the newer common method; the parent supplied canonical absolute
paths for those instructions before review continued.

The following retains the reviewer's provisional finding, before correction:

> Provisional P2 at bootstrap-loading/successor.py:36–44,
> python/security-checklist.md (Data Integrity), filename —
> successor.py/test_successor.py: historical reuse records are freshly hashed
> but never compared with the hash-pinned host freeze, allowing changed original
> Codex/state/review evidence to be resealed as unchanged reuse. Confidence 98%,
> source trace confirmed and intended contract acknowledged. Correct by checking
> the inherited map equals host freeze's inherited_evidence before extending it.
> Otherwise source review supports prompt boundaries, exact binding-only prompt
> check through captured command construction, carried strict receipt gate,
> unchanged measured prompts/runtime and bounded reuse. Await fix/test evidence
> for final re-review.

The parent added the comparison and a regression for both verification and fresh
freeze refusal. All eight tests pass; no historical input was edited. Final
independent disposition is recorded separately after re-review.
