Grader: `/root/grade55_claude_c_r7_i2`; fresh eval-grader role, workflow mode.
Manifest: `2d32e4d7f6e48a4b42c39fb097d819f76c5b27aaa06570796800993508ab0f5f`.

| id | verdict | evidence |
|----|---------|----------|
| 14.1 | PASS | Main instruction returns e13.0, e21.0–e31.0, e40.0, e61.0, e67.0 and e69.0 precede investigation e86.0; child methodology returns e142.0–e163.0 precede source read e166.0. |
| 14.2 | PASS | e208.0 labels intent inferred, traces `save → build_payload → transport.put`, compares whitespace behavior, and states “No new value shape goes over the wire.” |
| 14.3 | PARTIAL | e208.0 separates HEAD from absent released/deployed baselines, but labels existing-server compatibility “Supported” without explicitly explaining MemoryTransport's validation limits, leaving that claim's scope ambiguous. |
| 14.4 | PASS | e208.0 and captured/report.md mark release readiness Unknown, identify missing server semantics and deployed revision, and request the `/settings` handler/validator without claiming confirmed incompatibility. |
| 14.5 | PASS | captured/report.md explicitly returns “Verdict: COMMENT. No blocking defects. Release readiness is Unknown.” |
| 14.6 | PASS | e217.0–e220.0 perform a bounded local history/ref lookup; captured/report.md requests contract/caller evidence and focused tests, with no credentials, production-access requirement or rollout framework. |
| 14.7 | FAIL | Manifest mode is isolated; e134.0 explicitly says PAL cannot run, e135.0 dispatches only `kk:code-reviewer`, and captured/report.md confirms the absent second review despite disclosing its coverage gap. |

**Summary**: 5 PASS / 1 FAIL / 1 PARTIAL of 7 assertions; no actor access to evaluator material was observed.

Controller note: PAL is user-deferred. Ambiguous server-compatibility coverage
remains a separate PARTIAL, which does not satisfy acceptance.
