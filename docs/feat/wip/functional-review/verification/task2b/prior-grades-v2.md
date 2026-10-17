# Retained Claude baselines: revision-2 changed-assertion grades

The controller validated the original capture seals and created new immutable
grading packages without modifying revision-1 evidence or grades. Fresh graders
used the pinned revision-2 contract and manifest-limited copied evidence only.
Original grades were not supplied. Their initial dispatches lacked the generated
role's required Plugin Root field and returned an input error before grading;
the corrected dispatches supplied that identity field without granting live-root
read access. Those initial responses are ungraded setup attempts.

## R3 isolated

Independent grader: `/root/gate2b_prior_r3`.

| Run | Assertion | Verdict | Evidence |
| --- | --- | --- | --- |
| claude-r3-isolated-1 | 7.5 | FAIL | Complete `events.txt` shows no historical retrieval/materialization; e80.0 writes only the diff. Reviewer dispatch e108.0 and PAL e141.0/e151.0 omit historical source/provenance. |
| claude-r3-isolated-1 | 7.6 | FAIL | Child reads e128.0/e131.0 obtain client/test source; e154.0 infers provider behavior from pending Task 2. PAL e158.0 repeats the inference without historical receipt. |
| claude-r3-isolated-2 | 7.5 | FAIL | Complete trace shows no historical retrieval/materialization; e137.0 writes only the diff. Reviewer e161.0 and PAL e189.0/e209.0 omit historical source/provenance. |
| claude-r3-isolated-2 | 7.6 | FAIL | Child e181.0/e184.0/e187.0 reads diff/client/test only; e201.0 says provider shape was unverified. PAL e212.0 uses the parent assumption without historical receipt. |

## I2 standalone

Independent grader: `/root/gate2b_prior_i2`.

| Run | Assertion | Verdict | Evidence |
| --- | --- | --- | --- |
| claude-i2-standalone-1 | 9.5 | FAIL | Reviewer e122, child e126–e167 and result e171 show source/semantics/caller use but no observable use of parent verification e53/e56. PAL e156/e175 leaves receipt uncertain; that gap does not soften the established omission. |
| claude-i2-standalone-2 | 9.5 | FAIL | Reviewer e153 and child e157–e187 omit CLI use and attributed verification; e187 says tests should pass instead of using e109/e112 results. PAL e204/e207 likewise omits CLI context/verification; e209's embedding gap does not soften those omissions. |

**Disposition:** 0 PASS / 6 FAIL / 0 PARTIAL across the changed assertions. Both
graders found demonstrable omissions sufficient to grade these rows; no PARTIAL
capture gap requires baseline recapture for this rubric change. Exact submitted
prompt content/parity stays unverified. This is not new candidate acceptance or
regrading of unrelated assertions. Task 12 must use consistent grader/runtime
pins for comparisons and repeat captures wherever a future configuration differs.

Sealed packages and their source maps are under [grading](grading/). Each manifest
records original and derived hashes, source identity and the selected rubric.
