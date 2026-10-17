Grader: `/root/grade55_codex_c_r6_i1`; fresh eval-grader role, workflow mode.
Manifest: `4b8bff82aed6d302331705a55bf79af2c9f683a1779d7fc68ea41d07a4064f8a`.

| id | verdict | evidence |
|----|---------|----------|
| 13.1 | PARTIAL | Events/0003–0016 load process/profile instructions before investigation at 0018; child reads 0035–0046 precede evidence at 0048. No completed `SKILL.md` load is captured. |
| 13.2 | PASS | Events/0021–0023 compare the staged diff with HEAD; 0052–0063 and 0066 trace `report`, the False setting, unchanged calculations, and the label/test changes. |
| 13.3 | PASS | Event/0066 identifies empty detailed-input division by zero as inherited from HEAD, “neither introduced nor activated here”; 0033 calls it unchanged. |
| 13.4 | PASS | Event/0066 separates empty detailed input from the shipped disabled configuration and marks historical deployment settings Unknown, supported by reads 0055–0063. |
| 13.5 | FAIL | Events/0033 and 0066 approve the scoped change without a blocker or refactor, but surface the inherited failure without the required bounded follow-up or next action. |
| 13.6 | FAIL | Event/0026 links the named reviewer and 0066 retains its result; 0010 and 0033 explicitly disclose that PAL was unavailable. No required PAL dispatch/result exists, and no waiver applies. |

**Summary**: 3 PASS / 2 FAIL / 1 PARTIAL of 6 assertions.

Controller note: PAL is user-deferred; the entry-point evidence gap remains
PARTIAL. The omitted inherited-defect follow-up is a separate behavioral
failure. Owner: implementing agent after this fixed-candidate matrix; any repair
requires a separately identified candidate and fresh affected comparisons.
