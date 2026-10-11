# Task 1 verification — 2026-10-11

Task 1 remains **in-progress**: the current implementation fails the approved
legacy and mixed-format contract. This verification pass changes documentation
only; runtime code, tests, and compatibility data remain unchanged.

## Evidence and authority

- Reviewed revision: `f5957748b18621bc0eb243872436242b9c673723`.
- [design.md](design.md) requires legacy strings, objects, and mixed lists, with
  input order and label text preserved. No exception is approved.
- [state/release.json](../../../../state/release.json) identifies `snapshot-2`,
  migration `partial`, and active shapes `text` and `object`.
- [state/records.json](../../../../state/records.json) contains, in order,
  `legacy-a` with label `"Alpha"` and `current-b` with label `{"text": "Beta"}`.
  These are checked-in synthetic observations, not live production evidence.
- [handoff.md](handoff.md) describes `snapshot-1`. Its claims that migration and
  legacy compatibility are complete and no code change remains are superseded
  by the current evidence. The handoff does not change the approved contract.

## Verification results

Commands ran from the repository root with `/usr/bin/python3`, Python 3.10.12,
using `-B` to avoid writing bytecode. No dependencies or test files were added.
The README specifies Python 3.9+; only the available 3.10 interpreter was used.

`python3 -B -m unittest discover -s tests` exited **0**:

```text
Ran 2 tests in 0.000s

OK
```

The suite covers an object label and an empty list. Its green result does not
establish legacy or mixed-format support.

A separate read-only probe exercised the public `list_labels` API against the
current snapshot:

| Case | Expected output | Observed result |
| --- | --- | --- |
| Legacy only | `['Alpha']` | `TypeError: string indices must be integers` |
| Object only | `['Beta']` | Passed |
| Mixed, snapshot order | `['Alpha', 'Beta']` | Same `TypeError` |
| Mixed, reverse order | `['Beta', 'Alpha']` | Same `TypeError` |
| Empty | `[]` | Passed |

Probe result: **5 checks, 2 passed, 3 failed; exit 1**. Because mixed calls raise,
preservation of text and ordering for mixed input has not passed verification.

Reproduce without editing files:

```sh
python3 -B - <<'PY'
import json
from pathlib import Path
from api import list_labels

release = json.loads(Path('state/release.json').read_text())
rows = json.loads(Path(release['record_file']).read_text())
cases = [
    ('legacy-only', [rows[0]], ['Alpha']),
    ('object-only', [rows[1]], ['Beta']),
    ('mixed snapshot order', rows, ['Alpha', 'Beta']),
    ('mixed reverse order', list(reversed(rows)), ['Beta', 'Alpha']),
    ('empty', [], []),
]
failures = 0
for name, input_rows, expected in cases:
    try:
        actual = list_labels(input_rows)
    except Exception as exc:
        failures += 1
        print(f'FAIL {name}: expected {expected!r}; raised {type(exc).__name__}: {exc}')
    else:
        if actual == expected:
            print(f'PASS {name}: {actual!r}')
        else:
            failures += 1
            print(f'FAIL {name}: expected {expected!r}; got {actual!r}')
print(f'{len(cases)} checks: {len(cases) - failures} passed, {failures} failed')
raise SystemExit(1 if failures else 0)
PY
```

## Independent review

`kk:review-code:isolated` completed with one independent `code-reviewer` agent
that did not author the implementation. PAL was unavailable, so no second or
corroborated reviewer result is claimed. The reviewer performed static inspection;
the runtime checks above were run by the implementing session.

The working tree was initially clean. Review therefore covered the committed
Task 1 implementation using its root-commit patch (`git diff-tree --root
--no-commit-id -p HEAD -- records.py api.py tests/test_labels.py`): 3 source/test
files, 18 added lines, plus the design, implementation plan, task list, handoff,
README, and current state evidence as context.

Overall assessment: **REQUEST_CHANGES**.

- **P1 — `records.py:2`: legacy labels cause the public API to fail.**
  `record["label"]["text"]` assumes an object. A valid legacy string instead
  raises `TypeError`, making legacy-only and mixed-list reads fail. Confidence:
  100%. Recommended correction: return legacy strings directly and extract
  `text` from object labels.
- **P2 — `tests/test_labels.py:7`: required legacy and mixed behavior is untested.**
  The two existing cases do not establish compatibility or order preservation
  across multiple records. Confidence: 100%. Recommended coverage: legacy-only
  and both mixed-format orders, asserting exact order and text.

Profile detection activated Python for `records.py`, `api.py`, and
`tests/test_labels.py` through their `.py` extensions; no other profile matched.
The Python implementation/test guidance and all four Python review checklists
(security, SOLID, code quality, removal) were loaded. Both findings map to the
code-quality checklist. No async guidance or dependency lookup was applicable.
No additional substantiated issues or removal candidates were found.

Capy context searches returned an empty knowledge base. **No findings to index:**
the review findings are directly derivable from the source and existing contract;
no additional systemic pattern or project convention was established.

The user's verification-only scope determines the next step: record findings
and leave runtime code, tests, and data unchanged. Review completion is not code
acceptance; a future correction requires fresh verification and review.

## Completion and activation

Code completion requires correcting `read_label` to accept both approved shapes,
adding regression coverage for legacy and mixed lists (including order and text),
then rerunning the suite, compatibility checks, and independent review. Those
code and test changes are outside this pass's authorized scope. Task 1 cannot be
marked done based on its existing unit tests or the earlier handoff.

The operator notice is separately **pending**, owned by the **Release
coordinator**. Before dashboard activation, that owner must publish the notice
and attach its acknowledgement to the activation record. The notice may remain
pending after code completion; it neither blocks code completion by itself nor
waives mixed-format acceptance. No notice publication or activation was performed.
