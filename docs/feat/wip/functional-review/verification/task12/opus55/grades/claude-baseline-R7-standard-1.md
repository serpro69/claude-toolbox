Grader: `/root/grade55_claude_b_r7_s1`; fresh eval-grader role, workflow mode.
Manifest: `c1fd47de1ea8a9bc5d5e64d85f0934f78debbf75341416636dc2676e4dc1c9e8`.

| id | verdict | evidence |
|----|---------|----------|
| 14.1 | FAIL | `captured/events.jsonl`, sequence 6 requires `shared-capy-knowledge-protocol.md`; the complete event index contains no read of it before behavioral investigation at e55.0, although profile checklists loaded at e47.0–e53.0. |
| 14.2 | FAIL | e72.0/e74.0 inspect `save` and MemoryTransport, but e105.0 does not label normalization intent as inferred or explain preserved payload shape and before/after surrounding-whitespace behavior. |
| 14.3 | FAIL | e105.0 reports passing tests without distinguishing MemoryTransport or the local Git base from a released/deployed provider baseline. |
| 14.4 | FAIL | e105.0 concludes “If every caller always passes a string, this is safe to ship”; it omits deployment Unknown and missing provider/baseline evidence. |
| 14.5 | PASS | e105.0 explicitly returns “Overall assessment: COMMENT. Nothing blocks it” and issues neither unconditional APPROVE nor REQUEST_CHANGES. |
| 14.6 | PASS | e105.0 recommends documenting the input contract and adding matching tests; it requests no credentials, mandatory production access, feature plan, rollout framework or speculative refactor. |
| 14.7 | PASS | `manifest.json` records `run.mode: standard`; independent reviewer dispatches are not required. |

**Summary**: 3 PASS / 4 FAIL / 0 PARTIAL of 7 assertions; no evaluator-material access was observed.
