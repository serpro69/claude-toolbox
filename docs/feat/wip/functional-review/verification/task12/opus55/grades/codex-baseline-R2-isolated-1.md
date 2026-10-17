Grader: `/root/grade55_codex_b_r2_i1`; fresh eval-grader role, workflow mode.
Manifest: `5a660502edcf8d3a22771afb9b90a74819cc7862923db3f9242bd057a8051642`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | PASS | Parent instruction/profile reads in events/0003.json, 0005.json, 0015.json, 0016.json and 0019.json finish before behavioral reads in 0021.json; child checklist reads in 0041–0044 finish before source reads in 0045–0050. |
| 8.2 | PASS | events/0031.json reproduces `submit` → save → receipt failure → edited retry returning success with blue still active; events/0059.json identifies the introduced `service.py:8` guard. |
| 8.3 | PASS | events/0031.json reproduces completed `op-1` followed by `op-2` success with blue active and only `op-1` retained; events/0059.json attributes this to workspace lookup at `service.py:2`. |
| 8.4 | PASS | events/0059.json cites both README contracts and recommends operation-ID lookup, applying current values for incomplete operations, and restoring the completed-ID early return. |
| 8.5 | FAIL | events/0039.json says passing tests “miss these cases,” but neither that report nor events/0059.json explains their same-value retry coverage and absence of a fresh-ID test; severity and REQUEST_CHANGES are supported. |
| 8.6 | FAIL | captured/launch.json records PAL disabled; events/0018.json and 0039.json disclose its absence, and no PAL dispatch/result exists. Exact named-reviewer handoff plaintext remains unverified. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions.

Controller note: PAL is user-deferred. The test-coverage explanation remains
a separate failed component.
