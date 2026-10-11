Grader: `/root/grade55_codex_c_r9r_s1`; fresh eval-grader role, workflow mode.
Manifest: `e977bf40211a6d26bb8ee553c2b53ecccc6d0f6e8cf1a5600456da354a1bdc66`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | PASS | events/0002, 0006–0011, 0014, and 0016–0017 return complete instructions before investigation in 0019 and 0022–0024; earlier scope checks use filenames and adjacency only. |
| 11.2 | PASS | events/0022–0024 establish `Preferences.read → read_preferences → read_resilient(key.strip())`; 0028 explains preserved trimming and retry ownership. |
| 11.3 | PASS | events/0023 and 0027 bind successful executions to transient recovery, three-failure exhaustion, and immediate permanent failure; 0026 records additional executions, summarized separately from source coverage in 0028. |
| 11.4 | PASS | events/0028 says “No changes recommended” and preserves `read_resilient`; 0026 verifies permanent errors terminate without further retries. |
| 11.5 | PASS | events/0028 approves against HEAD `7c0410c`, names reviewed paths, and limits compatibility to local source and the scripted backend without adding gates. |
| 11.6 | PASS | manifest.json records `run.mode: standard`; independent named-reviewer and PAL dispatch obligations do not apply. |

**Summary**: 6 PASS / 0 FAIL / 0 PARTIAL of 6 assertions.
