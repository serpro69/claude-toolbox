Grader: `/root/grade55_codex_c_r9m_s2`; fresh eval-grader role, workflow mode.
Manifest: `e89a2311d6eb604f37471c8aee9e47a881e93ad8969290d3ab1a4312bf093c22`.

| id | verdict | evidence |
|----|---------|----------|
| 10.1 | PASS | Full instruction reads in events/0003.json, 0006.json, 0007.json, 0012.json and 0014.json precede source investigation in events/0017.json; earlier scope inspection uses filenames and metadata. |
| 10.2 | PASS | events/0017.json loads the explicit README contract; events/0020.json, 0021.json and 0023.json trace and exercise Preferences → reader → Repository → ScriptedBackend. |
| 10.3 | PASS | events/0026.json cites reader.py:2 and the `read_resilient` replacement; events/0023.json demonstrates HEAD succeeding after two attempts versus staged failure on attempt one. README supplies intent. |
| 10.4 | PASS | events/0026.json says the passing transient test “asserts the regression,” recommends `read_resilient(key.strip())`, and requests successful recovery with two normalized lookups. |
| 10.5 | PASS | events/0026.json returns REQUEST_CHANGES/P1 and distinguishes recovery, three transient failures and immediate permanent errors; events/0023.json supports these results without additional gates. |
| 10.6 | PASS | manifest.json declares `run.mode: standard`; the independent-dispatch obligation does not apply. |

**Summary**: 6 PASS / 0 FAIL / 0 PARTIAL of 6 assertions.
