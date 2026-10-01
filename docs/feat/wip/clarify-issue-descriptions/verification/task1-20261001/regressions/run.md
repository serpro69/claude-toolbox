# Task 1 smoke regressions — 2026-10-01

Cases: `dense-source` (1) and `runtime-pr` (12), using the frozen revised Task 1
instructions. Independent original readers, editors, revised readers and a
general-purpose fixture-capable grader run with `fork_turns=none` and no overrides.
The initial executions used at most one active child; the parent later authorized
two during retries. Status: **complete — both clean retries valid; all 11
assertions PASS**.

Evidence is scoped to this directory; editable fixtures are staged under
`/tmp/clarify-issue-task1/regressions/`, outside every `SKILL.md` ancestor.
Plaintext prompts were written before dispatch. Reader questions are identical;
each reader can read only its declared artifact. Editor manifests permit only
the frozen instructions and scenario inputs. The runtime editor cannot read the
snapshot staging inputs, or write Git metadata, existing drafts or captured bodies.

The actual original-reader sessions use `gpt-6-astra`, effort `xhigh`; full settings
and launch arguments are recorded per session. The harness supplies normal system
and repository instructions even with no inherited conversation. No scenario
oracle, eval specification, other run, or grading content is included in editor or
reader prompts. Runtime isolation is checked against tool traces, not assumed from
the shared filesystem.

`*-trace.jsonl` files preserve complete tool calls/results and visible assistant
messages from the actual rollout JSONL files. Hidden reasoning, encrypted transport
envelopes, and system/repository boilerplate are excluded. Exact plaintext dispatch
prompts are separate pre-existing files; encrypted transport is never reconstructed.
Each settings file records its rollout path and hash.

## Staging record

Runtime Git revisions and the actual diff are recorded in
`runtime-pr/git-revisions.txt` and `runtime-pr/git-diff.patch`. `review-base` and
`review-head` are real local commits, with head checked out. Snapshots are retained
in `runtime-pr/before/snapshots/` for the grader only.

The first staging commit attempt inherited global GPG signing and failed before
creating a commit because sandbox access to the GPG agent was unavailable. That
temporary fixture checkout was recreated, and the successful fixture commits used
command-local `commit.gpgsign=false`, `tag.gpgsign=false` and disabled hooks. No
repository or global configuration was changed. This was coordinator staging,
before the editor and reader runs.

After the initial grader completed, copied Git metadata under the evidence
`before/` and `after/` trees was packaged into `checkout-git-metadata.zip` files.
Each archive retains the original `checkout/.git/...` member paths and every byte;
the packaging step verified every member hash before removing the copied `.git`
directory. This keeps evidence trackable without creating embedded Git repositories.
`metadata-packaging.json` maps archived files and hashes. Live staged checkout
metadata was never changed by this packaging. Historical grader manifests refer
to the pre-packaging evidence paths; archive members now provide those bytes.

Some sessions' default login-shell initialization reports that the navi log cannot
be created outside the sandbox. The complete error output is retained in traces;
no successful log write or scenario-external content access is indicated by it.

## Initial attempts retained

`dense-source/` and `runtime-pr/` preserve the original executions.
`initial-grader-verdicts.md` records PASS for all 11 content assertions. Runtime
was nevertheless invalid as a compliant execution because the editor's
`git status --short` refreshed the read-only `checkout/.git/index`. Every other
existing runtime file stayed byte-identical and exactly one draft was created.

The initial grader also withheld a strict boundary pass for both cases because
default login-shell startup attempted denied navi log writes. These diagnostics
do not establish a successful external write or any evaluation-material leakage.
Dense's only actual changed file was `guide.md`. This disputed environmental
boundary was removed from both final attempts by using non-login shell commands.
One initial-grader follow-up was not captured as plaintext before dispatch; its
retrospective record is in `initial-grader-followup-record.md`. The initial grade
is advisory history; final grading uses a new independent session with its exact
prompt saved before dispatch.

## Clean retries

`dense-source-retry/` and `runtime-pr-retry/` preserve fresh editors and fresh
original/revised readers. Each prompt records `login:false` before dispatch;
runtime additionally requires `git --no-optional-locks` or `GIT_OPTIONAL_LOCKS=0`.
The scenario prompts, original fixture content, frozen instructions, oracles and
assertions are unchanged. Harness-change records explain the environment fixes.

Coordinator hash audit: dense changed only `guide.md`, creating nothing; runtime
created only `docs/feat/wip/prep/pr-12-draft.md`, with every pre-existing file,
including all Git metadata, byte-identical. Both revised readers answer all five
questions from their sole allowed artifact. The dense original reader already
answered all five; its edit repairs the declared orientation defects without
establishing an answer-accuracy gain. Runtime's original reader retains the
misleading inherited-schema framing; its revised reader distinguishes the runtime
increment and answers the concrete cases.

The final grader receives only the clean retries' artifacts, sources, oracles,
prompts, manifests, hashes, settings and actual traces, plus the frozen instructions
and packaging records. `final-grader-prompt.txt` and `final-grader-manifest.json`
were saved before dispatch. No initial grading verdict is supplied.

## Final verdicts

The fresh independent grader reports **PASS** for `1.1`–`1.5` and `12.1`–`12.6`,
and **valid** for both executions. See [final-grader-verdicts.md](final-grader-verdicts.md)
for every assertion's evidence and the original/revised reader comparison.

| Scenario | Assertions | Trace/manifest validity | Observed changes |
|---|---|---|---|
| Dense source, clean retry | 5/5 PASS | PASS | Only `guide.md` changed; nothing created. |
| Runtime PR, clean retry | 6/6 PASS | PASS | One new local draft; all 27 existing files, including 20 Git metadata members, unchanged. |

The grader verified all 78 final-manifest hashes, prompt/participant-manifest
hashes, complete input/output inventories, and metadata archive/member hashes.
Actual Git trees match the grader-only snapshots. Both editors loaded the exact
complete frozen instructions before source reads. Every visible tool call has
a result; all sessions completed; no result was truncated. Final artifacts and
completions preserve the required behavior and open decisions.

All editor/reader reads remain within their manifests, with no oracle or
grader-snapshot access, network calls, or successful outside-scope mutation.
Every retry shell command uses `login:false`; every runtime Git query disables
optional locks. A runtime `rg` listing was blocked by a hook before execution,
producing no read or mutation; authorized Git queries supplied the evidence.
Both clean executions therefore pass the strict audit without the initial
attempts' environment ambiguity.

`final-grader-trace.jsonl` preserves the grader's actual visible calls, results and
completion; `final-grader-settings.json` records its actual settings and source
rollout. `final-grader-dispatch-check.json` and `dispatch-trace-checks.json` record
pre-dispatch plaintext capture times and participant tool-call pairing. Dispatch
transport remains encrypted and was not reconstructed. No supplemental prompt was
sent to the final grader.

These are offline manual behavioral evaluations. They do not certify a live
tracker connector or measure improved human comprehension. The initial attempts,
environment failures and advisory grading limitations remain preserved above.
