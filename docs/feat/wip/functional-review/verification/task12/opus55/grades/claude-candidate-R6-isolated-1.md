Grader: `/root/grade55_claude_c_r6_i1`; fresh eval-grader role, workflow mode.
Manifest: `78bb7fc3c9d8fd79a9119c26d3f36beeb951ef2a4b4f289223340386e500456b`.

| id | verdict | evidence |
|----|---------|----------|
| 13.1 | PASS | Main instruction/profile results e26.0–e94.0 precede investigation e116.0; child methodology results e180.0–e201.0 precede evidence read e205.0. Routing used filename metadata. |
| 13.2 | FAIL | e246.0 and e264.0 explicitly state that the base-to-candidate diff was not inspected; count-format preservation and unchanged test coverage remain Unknown. |
| 13.3 | PASS | e246.0 identifies the detailed-input crash as inherited: “This change did not introduce or worsen it”; e264.0 preserves that attribution. |
| 13.4 | PASS | e246.0 names `summarize([], detailed=True)`, distinguishes checked-in `False` from unknown historical settings, and labels its assessment as source reasoning without test execution. |
| 13.5 | FAIL | Final report e264.0 returns “Overall assessment: COMMENT” and states “I can't approve it,” leaving approval conditional on an unresolved comparison. |
| 13.6 | FAIL | Named dispatch e173.0 explicitly carries “Selected diff: UNAVAILABLE”; no PAL dispatch/result appears in the retained trace, and e264.0 discloses that PAL did not run. |

**Summary**: 3 PASS / 3 FAIL / 0 PARTIAL of 6 assertions; no evaluator-material access was observed.

Controller note: PAL is user-deferred. Missing diff/base coverage and the
conditional code verdict remain separate observed limits.
