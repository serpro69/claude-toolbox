Grader: `/root/grade55_claude_c_r7_i1`; fresh eval-grader role, workflow mode.
Manifest: `a49d4ca27cedf129b122d2a6e825c599c51330cb505b36cc4f00799375e8cf4f`.

| id | verdict | evidence |
|----|---------|----------|
| 14.1 | PASS | Main instruction/checklist results e12.0, e20.0–e30.0, e39.0, e49.0, e55.0/e57.0 precede full-diff investigation e74.0; child methodology results e129.0–e150.0 precede evidence reads e154.0 onward. |
| 14.2 | PASS | e196.0 traces `save → build_payload → transport.put("/settings", body)` and preserves the `display_name` shape; e215.0 labels intent inferred and compares surrounding/internal whitespace and empty strings. |
| 14.3 | FAIL | Despite acknowledging absent deployed baselines, e196.0 declares “old servers receiving new-client requests” Supported and “no server change is needed”; neither report explains MemoryTransport's mock coverage limitation. |
| 14.4 | PASS | e215.0 states “Deploy readiness: Unknown,” identifies missing handler/consumer evidence, and requests confirmation of empty-name handling; e207.0 records the bounded local-history lookup. |
| 14.5 | PASS | e215.0 returns “COMMENT on the code” with deployment Unknown and conditional, unconfirmed blocker reachability. |
| 14.6 | PASS | e204.0/e207.0 inspect local history; e196.0 requests specific handler and caller source, while e215.0 proposes scoped tests/contract clarification without credentials or a rollout framework. |
| 14.7 | FAIL | e122.0 dispatches the named reviewer with source/context and e199.0 retains its result, but no PAL dispatch/result exists; raw sequence 3 records PAL failed, and e215.0 discloses absent corroboration. |

**Summary**: 5 PASS / 2 FAIL / 0 PARTIAL of 7 assertions; no evaluator-material reads were observed.

Controller note: PAL is user-deferred. Unsupported server compatibility remains
a separate failed obligation even though the final deployment verdict is Unknown.
