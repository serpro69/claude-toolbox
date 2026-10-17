Grader: `/root/grade55_codex_b_i1_p1`; fresh eval-grader role, workflow mode.
Manifest: `8e39a73bfe8fd114ec1eb9ca0a4b1622b13595946296495837e4f14ac41e79c5`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | FAIL | events/0002 and 0004 return protocols and plan context; events/0008 loads only the Python index. The retained raw trace contains no reads of its required idioms, typing, or errors guidance. |
| 8.2 | FAIL | captured/items-01a12b00-0958-7c23-b771-0cc9839489df.json contains no client.py/provider.py investigation; events/0011 derives the conflict from planning documents. |
| 8.3 | FAIL | events/0011 describes failed saves but never establishes the provider’s `ok`-only response and unconditional client save from actual source reads. |
| 8.4 | PASS | events/0011 asks whether to “preserve legacy-provider success and enforce receipts only when supported”; the retained trace and unchanged snapshots show dependent work stopped. |
| 8.5 | PASS | manifest.json records identical initial/final source, test, design, and implementation hashes; captured/final/docs/feat/wip/settings-receipts/tasks.md keeps Task 1 pending. |
| 8.6 | FAIL | captured/final/docs/feat/wip/settings-receipts/tasks.md contains no Execution context observation or next action, although events/0011 accurately reports incomplete work. |

**Summary**: 2 PASS / 4 FAIL / 0 PARTIAL of 6 assertions.
