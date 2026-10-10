# Candidate 1: R1 standard comparison

All four raw captures and sealed grading packages remain under `runs/` and
`grading/`, named `claude-{baseline,candidate}-R1-standard-{1,2}`. Fresh
`eval-grader` roles `/root/grade_r1_baseline1`, `grade_r1_baseline2`,
`grade_r1_candidate1`, `grade_r1_candidate2` used the declared pinned grader and
revision-2 rubric. Controller validated every raw/derived file hash before
dispatch. Both sides used identical fixture bytes and runtime configuration.

| Assertion | Baseline rep 1 | Baseline rep 2 | Candidate rep 1 | Candidate rep 2 |
| --- | --- | --- | --- | --- |
| 6.1 instruction loading | FAIL | FAIL | FAIL | FAIL |
| 6.2 documented lifecycle trace | FAIL | FAIL | FAIL | FAIL |
| 6.3 introduced ownership regression | FAIL | FAIL | PASS | PASS |
| 6.4 preserving correction | PASS | PASS | PASS | PASS |
| 6.5 severity/verdict/test limits | FAIL | FAIL | PASS | PASS |
| 6.6 mode-specific dispatch | PASS | PASS | PASS | PASS |

Baseline total: **4 PASS / 8 FAIL / 0 PARTIAL**. Candidate total:
**8 PASS / 4 FAIL / 0 PARTIAL**. These are descriptive results, not acceptance
or a reliability estimate. No evaluator-material access was observed in the
retained read/tool events; no OS-wide confinement is claimed.

## Evidence

- Baseline 1: e16 requires all known detection rules but only Python appears
  before e54/e57 investigation. e100 admits unseen callers; setup.py is unread.
  Its P0 finding omits the supported failed-job trigger and test distinction.
- Baseline 2: e19/e23 require enumeration; only Python e35/e36 precedes e59/e62.
  e106 admits no caller/lifecycle trace, overstates severity and omits the
  existing-tests versus uncovered-interleaving distinction.
- Candidate repetition 1: e13/e23 require all known detection files, but only
  Python e38/e39 precedes investigation e55. e73 reads setup.py; e128 describes
  completed-setup supersession/cancellation rather than failed A, queued cleanup
  and successful B. The ownership finding, P1, correction and denied-test
  disclosure are supported.
- Candidate repetition 2: e12/e22 require every detection rule; e36/e46 skip
  seven. e82 returns setup.py, but e119 traces two completed setups. Its remaining
  finding/correction/verdict assertions pass.

## Preserved grading correction

The initial 6.1 grades from baseline 1, baseline 2 and candidate repetition 1
were PASS, based only on resolved Python checklist ordering. Candidate repetition
2's grader identified the missing mandatory detection reads. Each of the other
three original graders independently reassessed the unchanged package and
superseded its 6.1 with FAIL, citing the captured procedure's enumeration rule.
No rubric, fixture, actor output or acceptance threshold changed. Initial totals
before correction were baseline **6/6/0**, candidate **9/3/0**; all other rows
remain unchanged. Original runtime synthetic skill-body messages are retained
in `captured/events.jsonl`, even though the older derived event view omits them.

These two observed gaps motivated the recorded candidate 2/3 instruction fixes.
