Coordinate the Task 1 manual behavioral evaluation for github-issue-bug (16) and
issue-local-draft (17). This is an explicitly required editor/reader/grader
evaluation from the active /kk:implement plan. You own only their run evidence in
docs/feat/wip/clarify-issue-descriptions/verification/task1-20261001/issues/ and
staging under /tmp/clarify-issue-task1/issues/. You are not alone in the workspace;
do not modify production instructions, eval specifications, or others' edits.

First read klaude-plugin/skills/clarify-docs/evals/README.md and the feature
implementation.md sections Execution and evidence protocol and Evaluation matrix.
Then read the two scenario eval.json and oracle/expected.json files and fixtures.
The editor and reader sessions must never see eval specifications or oracles.

Start by executing both scenarios against the frozen baseline instructions at
/tmp/clarify-issue-task1/instructions/baseline/clarify-docs/{SKILL.md,shared-document-clarity.md}.
Create separate workspaces containing only each test-files/ content, outside any
SKILL.md ancestor. Save before snapshots, hash manifests, exact allowed-file
manifests and complete plaintext prompts BEFORE submission. Spawn fresh
general-purpose editors with fork_turns=none, no model overrides. Give them the
exact eval prompt plus neutral harness constraints: stage root, instructions to
load instead of the installed copy, the allowed read/write scope, no network.
Do not add oracle expectations or prime issue-specific behavior. Wait for baseline
editors to finish, save raw tool-call/result/message traces and actual model/effort
metadata, then report BASELINES COMPLETE to the parent. Do not run the revised
instructions until the parent supplies their frozen path.

After receiving the revised instruction path, run fresh editors for both scenarios
from unchanged initial fixtures. Use separate fresh original and revised readers,
identical model/settings, fixed questions from the oracle, only their artifact and
declared reader_manifest files. Capture reader prompts at submission time. No
inherited conversation; no shared reader across versions/scenarios. If baseline
produces drafts, compare those too using fresh readers; shared original-reader
answers are acceptable only if its artifact, questions and settings are identical.

Use a separate general-purpose fixture-capable grader with fork_turns=none; the
eval-grader role is prohibited because it cannot inspect fixtures. The grader
reads source, artifacts, fixed oracle, both reader answers and actual editor trace,
audits access against manifests and returns every assertion as PASS/FAIL/PARTIAL
with evidence. Baseline failures are observations, not task failures. Do not weaken
assertions, reconstruct missing prompt evidence, or call incomplete traces a pass.
Retain failed attempts. A non-passing revised run must be reported to the parent
for correction and fresh rerun. Preserve relevant files, exact prompts, hashes,
raw traces, metadata, and grading under your owned evidence directory; summarize
all runs in run.md. Record live connector certification as excluded.

Trace capture: current Codex rollout JSONL files are readable under
/Users/sergio/.codex/sessions/. Match session IDs to files. Preserve actual
tool-call/results and visible messages, excluding hidden reasoning/system boilerplate.
If transport prompts are encrypted, retain the exact pre-dispatch plaintext
request rather than reconstructing it. Use native apply_patch for authored files;
cp can preserve snapshots and raw transcripts. Shared filesystem access requires
an explicit trace audit, not a claim of OS isolation.

Keep at most two child agents active at once to leave room for other checks. Send
concise progress and concrete blockers. Do not change the parent tasks.md.
