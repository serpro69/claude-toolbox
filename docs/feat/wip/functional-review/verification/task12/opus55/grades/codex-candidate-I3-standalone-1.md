Grader: `/root/grade55_codex_c_i3_s1`; fresh eval-grader role, workflow mode.
Manifest: `85dce739235f4629d407568eb1795eacca509b625533852d36880c1000b3ae82`.

| id | verdict | evidence |
|----|---------|----------|
| 10.1 | PASS | Events 0002–0017 show completed implementation protocol, standalone-mode and all eight detection-rule reads, adjacency checks, and no active profiles before edit 0042. |
| 10.2 | PASS | Events 0023–0024 establish the original text, one replacement, preservation of every other byte, the clean baseline, and no runtime or dependency changes. |
| 10.3 | PASS | Initial/final help snapshots and `captured/final.patch` show only `suported` → `supported`; `captured/launch.json` and `captured/completion.json` retain identical hashes for README, runtime code and tests. |
| 10.4 | PASS | Events 0047–0049 show the actual diff, successful exact-byte/scope comparison, clean diff check and one existing test passing; final snapshots contain no added tests or dependencies. |
| 10.5 | PARTIAL | `captured/protocol.jsonl` sequences 483/486 and event 0051 identify the reviewer but omit submitted arguments proving the diff and wording-constraint handoff. Later reads/use in 0076, 0079 and 0082 cannot establish those arguments; rubric revision 2 permits no I3 receipt/use fallback. |
| 10.6 | PASS | Final event 0060 accurately reports the correction, successful verification, independent approval and unavailable PAL; the final patch and file inventory show no unrelated changes or feature/release artifacts. |

**Summary**: 5 PASS / 0 FAIL / 1 PARTIAL of 6 assertions; 10.5 changes from PASS to PARTIAL because required dispatch evidence is unavailable, without inferring omission or extending the receipt/use fallback.

The [initial grade and clarification request](../grading-revisions/codex-candidate-I3-standalone-1-initial.md)
are preserved. The same grader reassessed unchanged sealed evidence under the
same rubric; no evidence contract was broadened. PAL remains user-deferred.
