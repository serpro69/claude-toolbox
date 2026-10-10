# Candidate 1: R3 isolated observations

Four captures and their sealed grading packages are retained under `runs/` and
`grading/`, named `claude-{baseline,candidate}-R3-isolated-{1,2}`. Fresh graders
`/root/grade_r3_baseline1`, `grade_r3_baseline2`, `grade_r3_candidate1`,
`grade_r3_candidate2` used the pinned grader/rubric. All hashes were checked
before dispatch. These are literal original-assertion grades.

| Assertion | Baseline rep 1 | Baseline rep 2 | Candidate rep 1 | Candidate rep 2 |
| --- | --- | --- | --- | --- |
| 7.1 instruction order | FAIL | FAIL | PASS | PASS |
| 7.2 historical baseline | FAIL | FAIL | PASS | PASS |
| 7.3 disabled-path failure | FAIL | FAIL | PASS | PASS |
| 7.4 current versus pending work | PASS | PASS | PASS | PASS |
| 7.5 materialization/receipt | FAIL | FAIL | FAIL | FAIL |
| 7.6 both reviewers use history | FAIL | FAIL | FAIL | FAIL |
| 7.7 verdict/evidence limits | FAIL | FAIL | PASS | PASS |
| 7.8 compatible correction | PASS | PASS | PASS | PASS |

Baseline: **4 PASS / 12 FAIL / 0 PARTIAL**. Candidate:
**12 PASS / 4 FAIL / 0 PARTIAL**. No acceptance: PAL was absent and both
candidate runs shared a temporary directory.

Baseline 1 investigates at e34/e37 before profile/scope reads; e165 admits no
provider inspection despite an available local tag. Baseline 2 reads client.py
at e88/e89 after only the profile index; e191 confirms no historical read, while
e213 claims deployed-provider effects and omits Blocked. Neither supplies the
historical source to its named reviewer or invokes PAL.

Candidate 1 loads instructions before e83. e113/e116 return historical source;
e154/e155 and e162/e163 write source/provenance. Dispatch e180 and reads e225/e228
establish named receipt; e258 uses it. e281 traces persistence followed by the
exception and reports Blocked/REQUEST_CHANGES with no PAL execution.

Candidate 2 loads instructions before e85. e123/e126 return historical source,
e130 provenance. e159–e162 materialize it; dispatch e170 and reads e216/e219
establish named receipt; e247 uses it. e267 gives the supported verdict while
disclosing that PAL did not run. Exact prompt parity remains unverified.

The configured PAL launcher failed startup in all four sessions. A separate
[MCP startup probe](pal-startup-probe/result.json) confirms missing API
configuration. The user subsequently deferred PAL verification. Candidate
7.5/7.6 failures concern that deferred component; named-reviewer receipt/use
is observed rather than inferred from file availability.

Both candidate sessions fell back from denied compound shell commands to Write
calls under `/tmp/kk-evidence-enhset`. Although filenames partly differ, this
shared writable state invalidates fresh-state acceptance. Nine exact actor-written
files (eight there plus one baseline patch) were matched against captured Write
arguments, archived under `retained-scratch/`, then removed. No unrelated files
were removed. Further isolated/implementation sessions are serialized and audited.
