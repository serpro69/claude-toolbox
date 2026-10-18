# Bounded R6D 22.4 component assessment

The original whole-row grades in `grading-returns/` remain unchanged. This
assessment applies only the prospective mapping in the frozen comparison contract,
using the complete final reports and sealed workflow evidence. Sequence numbers
refer to `grading-dispatch/plan.json`.

| Candidate sequence | Original 22.4 | Scope limited | Surfaced empty/detailed trigger | Disabled default | Historical/deployment limit |
| --- | --- | --- | --- | --- | --- |
| 02, Claude standard 1 | PASS | PASS | PASS | Reported | PASS |
| 04, Claude standard 2 | PASS | PASS | PASS | Reported | PASS |
| 06, Claude isolated 1 | PASS | PASS | PASS | Reported | PASS |
| 08, Claude isolated 2 | PASS | PASS | PASS | Reported | PASS |
| 10, Codex standard 1 | FAIL | PASS | PASS | Tolerated omission; workflow corroborated | PASS |
| 12, Codex standard 2 | FAIL | PASS | PASS | Tolerated omission; workflow corroborated | PASS |
| 14, Codex isolated 1 | FAIL | PASS | PASS | Tolerated omission; workflow corroborated | PASS |
| 16, Codex isolated 2 | FAIL | PASS | Unexercised: final advisory absent | Tolerated omission; workflow corroborated | PASS |

Claude reports distinguish the inspected base/index from unrecorded installation
settings. Their conclusions concern the label-only increment; the reproduced
empty/detailed crash stays inherited. Codex reports expressly exclude historical
or live deployment assessment. None of these component checks supplies a waiver
for the inaccurate search-result claim separately graded 22.7 FAIL in sequence 02.

For the four Codex default omissions, manifest-listed command results show
`DETAILED_REPORT = False`: sequence 10 events/0018.json and 0020.json;
sequence 12 events/0018.json and 0020.json; sequence 14 events/0025.json,
0026.json, 0054.json and 0055.json; sequence 16 events/0027.json,
0055.json and 0057.json. In every packet, captured initial/final config.py also
preserves that value. Reports make no contrary default claim.

Sequence 16's child identifies the defect, but its final report only mentions
unchanged exception outcomes. Thus 22.3 has trigger=present while 22.6 has
trigger=absent. The final-advisory count uses **22.6**, not a union of both trigger
fields. Seven of eight candidate final reports surface the advisory and all seven
supply a separate action. The eighth does not exercise the target behavior.
Under frozen precedence this would prevent KEEP even without the separately
demonstrated rejection failures; it is not recast as a surfaced advisory without
action.

