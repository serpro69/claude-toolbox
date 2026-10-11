Grader: `/root/grade55_codex_b_r2_s2`; fresh eval-grader role, workflow mode.
Manifest: `473b0327bc8ef40c3c3545c402ec9b6f0d2908ca138d3bf3383440e5aedd72cb`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | PASS | events/0002.json and 0005.json load methodology; detection, index, and checklist reads finish by 0019 before the behavioral diff in 0021. Earlier scope reads expose filenames only. |
| 8.2 | PASS | events/0025–0028 connect `submit` to `save` and the apply/receipt boundary; `edited_retry` reports success while blue remains active. Finding 2 in 0034 cites `service.py:8`. |
| 8.3 | PASS | events/0028.json reproduces completed `op-1` followed by `op-2`: success names `op-2`, preferences remain blue, and recovery contains only `op-1`; 0034 identifies workspace lookup as the cause. |
| 8.4 | PASS | events/0034.json proposes operation-ID lookup, applying latest retry values and updating recovery payloads, and restoring the completed-operation shortcut. |
| 8.5 | FAIL | events/0034.json gives supported P1 severity and REQUEST_CHANGES, but only states that existing tests pass; it does not explain their unchanged-value retries and missing fresh-operation coverage, visible in 0024. |
| 8.6 | PASS | manifest.json declares `run.mode: standard`; the isolated dispatch obligation does not apply. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions.
