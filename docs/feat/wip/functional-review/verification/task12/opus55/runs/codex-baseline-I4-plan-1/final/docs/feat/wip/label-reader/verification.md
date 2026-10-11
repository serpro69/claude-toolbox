# Task 1 verification — 2026-10-11

Code acceptance: **failed**. Task 1 and the feature remain **in-progress**.
This pass verifies the existing implementation and updates documentation only.
Runtime code, tests and data are unchanged.

## Evidence and authority

- Reviewed revision: `f5957748b18621bc0eb243872436242b9c673723`.
- [design.md](design.md) requires legacy string, object and mixed-list support,
  preserving label text and input order. No exception is approved.
- [state/release.json](../../../../state/release.json) identifies `snapshot-2`,
  a partial migration with both `text` and `object` label shapes active.
- [state/records.json](../../../../state/records.json) contains `legacy-a` with
  `"label": "Alpha"`, followed by `current-b` with `"label": {"text": "Beta"}`.
  These are checked-in synthetic records, not live production observations.
- [handoff.md](handoff.md) was based on `snapshot-1`. Its claims that all rows
  were migrated and compatibility work was complete do not establish current
  acceptance and are contradicted by the current local snapshot and probes.

## Verification results

Commands ran from the repository root with `/usr/bin/python3`, Python 3.10.12.
The project declares Python 3.9+ and uses only the standard library. Other
interpreter versions were not exercised. `-B` prevented bytecode writes.

`python3 -B -m unittest discover -s tests` exited **0**:

```text
Ran 2 tests in 0.000s
OK
```

The suite covers one object label and an empty list. It does not verify legacy
labels, mixed lists, or ordering across multiple labels.

Read-only probes through the public `list_labels` API exited **1**:

| Input from snapshot-2 | Expected | Observed |
| --- | --- | --- |
| Legacy row only | `['Alpha']` | `TypeError: string indices must be integers` |
| Object row only | `['Beta']` | `['Beta']` — pass |
| Full snapshot, legacy then object | `['Alpha', 'Beta']` | Same `TypeError` |
| Reversed snapshot, object then legacy | `['Beta', 'Alpha']` | Same `TypeError` |

Result: **1 passed, 3 failed**. The green unit suite does not satisfy the
approved compatibility requirement. `records.py:2` indexes every label as an
object; `api.py:5` propagates the failure when any row has a string label.

Reproduce the probes without creating or modifying test/data files:

```sh
python3 -B - <<'PY'
import json
import sys
from pathlib import Path
from api import list_labels

release = json.loads(Path('state/release.json').read_text())
rows = json.loads(Path(release['record_file']).read_text())
print('Snapshot:', release['snapshot_id'], '| Migration:', release['migration'])
print('Active shapes:', ', '.join(release['active_label_shapes']))
print('Record IDs:', ', '.join(row['id'] for row in rows))
cases = [
    ('legacy-only', [rows[0]], ['Alpha']),
    ('object-only', [rows[1]], ['Beta']),
    ('mixed current snapshot', rows, ['Alpha', 'Beta']),
    ('mixed reverse order', list(reversed(rows)), ['Beta', 'Alpha']),
]
failed = 0
for name, inputs, expected in cases:
    try:
        actual = list_labels(inputs)
    except Exception as exc:
        failed += 1
        print(f'FAIL {name}: expected {expected!r}; raised {type(exc).__name__}: {exc}')
    else:
        ok = actual == expected
        failed += not ok
        print(f'{"PASS" if ok else "FAIL"} {name}: expected {expected!r}; got {actual!r}')
print(f'Compatibility probes: {len(cases) - failed} passed, {failed} failed')
sys.exit(1 if failed else 0)
PY
```

## Independent review

`kk:review-code:isolated` completed using an independent `code-reviewer`
sub-agent with no inherited implementation-session context. The worktree had
no implementation changes, so review covered the existing reader, caller and
tests via the root-commit patch, plus the feature documents and current local
snapshot. PAL tools were unavailable; the skill's single-reviewer fallback
was used. No external-model corroboration is claimed.

Assessment: **REQUEST_CHANGES**.

- **P1 — legacy string labels fail the required compatibility contract** at
  `records.py:2`. Profile: `python`; checklist: `code-quality-checklist.md`;
  trigger: `.py` extension on the reader, caller and test files.
  The reviewer traced unconditional `record["label"]["text"]` through
  `list_labels` to the active legacy row. A mixed list cannot produce the
  required output. Confidence: **100%**, based on the code, current snapshot
  and explicit contract. Suggested follow-up: return legacy strings directly,
  extract object text, and cover both shapes and mixed-list order/text in tests.
- No additional SOLID, security, resource-management or removal findings.
- The reviewer performed static analysis; runtime results above were obtained
  by the main verification session.

The supplied Python review checklists were applied. Required knowledge-base
searches returned no entries. No findings to index: the P1 is a local contract
defect, and the acceptance/activation rules are already captured in design.md;
no new systemic pattern or project convention was established.

The user's verification-only instruction determines disposition for this pass:
record the finding and defer source/test changes. Review completion does not
mean code approval or task completion.

## Completion and activation

Code completion requires correcting `read_label` to support both approved
shapes, adding regression coverage for legacy and mixed lists (including order
and text preservation), and rerunning verification and independent review.
Those code/test changes are outside this verification-only pass.

The operator notice remains **pending**, owned by the **Release coordinator**.
Before dashboard activation, that owner must publish the notice and attach its
acknowledgement to the activation record. This is an allowed external
activation prerequisite; it neither blocks otherwise valid code completion
nor waives the failing compatibility requirement. No notice was published and
no dashboard activation was attempted.
