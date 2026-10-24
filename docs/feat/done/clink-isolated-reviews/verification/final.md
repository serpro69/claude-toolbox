# Final verification — clink fallback for isolated reviews (Task 3), 2026-10-24

Status: **complete** (all Task 3 subtasks performed and recorded; open user
decisions and unassigned follow-ups are listed in tasks.md and design.md). Nothing
below is claimed passed without a recorded run.

Baseline: branch `feat/clink_reviews` at `46b3118` (Task 2b commit) plus the
uncommitted Task 3 changes described here. Host: Linux; Python 3.10 default with
3.12 shimmed onto PATH for the suites; codex 0.163.0, claude 2.1.296, agy 1.4.6.
Connected PAL: 1.4.2 launched by `uvx --from git+…pal-mcp-server.git`; the cached
package's `direct_url.json` names commit `c73dab7d8cf9d791961b84614a0e082b74ee5569`
and its `tools/listmodels.py` hashes `60d416c2…f92683e`, identical to the
[Task 0 validation record](../../../../archives/feature-evidence/clink-isolated-reviews.md "archive member payload/docs/feat/done/clink-isolated-reviews/verification/linux-20261023/pal-fix-validation.json"). The connected
server therefore runs the minimum verified revision.

Raw captures for this task (actor outputs, grader verdicts, Codex event logs,
live clink responses) are kept out of Git in the ignored local archive
`.local-archives/feature-evidence/clink-isolated-reviews-task3-20261024/`
(`actor-output/`, `grader-output/`, `codex/`, `live/`) with a SHA-256 inventory
(`inventory.sha256`, written at the end of the task).

## 3.1 Deterministic checks

Command sequence (Capy run `b080b06f-937f-4156-9dba-515334661d77`, with
`GIT_CONFIG_PARAMETERS="'commit.gpgsign=false' 'tag.gpgsign=false'"` and
`/tmp/py312shim` first on PATH):

| Check | Result |
| --- | --- |
| `make generate-kodex` | Go tests ok; `test-plugin-structure.sh` 238/0; `test-codex-structure.sh` 29/0 |
| second `make generate-kodex` | generated tree hash manifest identical (`1ae1c34866afb00b`) |
| `make plugin-graph` | Go tests ok; `validate`: no broken edges or orphans |
| `test/test-*.sh` (13 suites) | all exit 0: claude-extra 21, codex-hooks 64, codex-structure 29, cpr 27, functional-review-tools 1, hooks 27, manifest-jq 17, plugin-structure 238, review-eval-staging 1, review-instructions 1, semver-compare 48, template-cleanup 23, template-sync 269 assertions, 0 failed |

Environment note: the first capture run hung in `test-template-cleanup.sh`
because its `git commit` inherited the user's global `commit.gpgsign` and gpg
stopped waiting for a terminal. The override above disables signing for the run
only; the suites were not changed. The suites' dependence on the caller's signing
configuration is a pre-existing robustness gap (owner unassigned; next action:
pass `-c commit.gpgsign=false` in the test helpers; verification: the suite
completes under a non-tty capture without the override). Confirmation: after the user
refreshed the gpg-agent cache, all 13 suites also passed under capture with signing
enabled and no override (Capy run `0b84b575-0e17-4871-9fa6-0d580fe2aa22`, template-cleanup
23/0 in 12 s, template-sync 269/0); the hang depends only on whether gpg can sign
non-interactively.

Intentionally partial eval links were not touched (`plugin-graph validate`
exempts them by design).

**Final re-run on the final bytes** (Capy run `7d49c859-1c5e-414b-9872-76b79a8b6e54`,
after every review-driven edit): `make generate-kodex` Go tests ok, 238/0 and
29/0; second generation identical (manifest `b719c2f1b40e33f9`); `make
plugin-graph` OK; all 13 suites exit 0 with the same assertion counts (template-sync
269). Final instruction hashes: protocol `3852f4d5d1505d2e`, code workflow
`0b403c6a3b1c0e99`, design workflow `72f032c7df267b03`, design criteria
`b6448a1beed72f0b`, design-reviewer agent `f79fea01b552ac62`. The plugin-prose
audit found no link to a toolbox-only document (only pre-existing consumer-path
references to `/docs/feat/wip/` in the review-spec commands).

**Third run after the 3.4/3.5/design-smoke fixes** (Capy run
`da834248-e2a2-4156-aa9b-cba0fb972635`): generation ok and idempotent (manifest
`67db020944ac41e7`), plugin-graph OK, all 13 suites exit 0 with unchanged counts.
Final hashes (SHA-256 prefixes): external-review-invocation `3852f4d5d1505d2e`, pal-codereview-invocation `e100e64c0a4c1df7`, review-code review-isolated `dbd08cebac104a59`, review-design review-isolated `72f032c7df267b03`. The clink prompt framing
and the API transport's criteria wording changed after the component evals ran;
neither alters a graded routing or reporting decision, so no scenario was rerun
(recorded as a proportionality decision).

## 3.2 Bounded behavioral verification

Instruction bytes graded (SHA-256 prefixes of the working-tree files; the
actor bundles were `klaude-plugin/` and `kodex-plugin/` with every `evals/`
subtree excluded, resynced after each fix):

| File | start of 3.2 | after fix A (criteria receipt) | after fix B (internal-reviewer receipt) |
| --- | --- | --- | --- |
| `skills/_shared/external-review-invocation.md` | `d6ea6308e237bae1` | `f7821a44f62f7bdb` | `51bb6370a61d98af` |
| `skills/review-code/review-isolated.md` | `fc992061954e13cc` | `7114e4847f8cca41` | unchanged |
| `skills/review-design/review-isolated.md` | `6abfe29b3a4d36b8` | `998d688787344411` | unchanged |

Fixtures were staged with `review-code/evals/_harness/setup.sh` (code) and by
copying `test-files/` (design) into fresh temp directories outside any `SKILL.md`
ancestor. Component mode throughout: one actor per scenario given the eval's
ordinary prompt, the staged project and the bundle as plugin root, with PAL,
sub-agents and Capy declared unavailable and the fixtures' synthetic
`discovery.json` / `external-results/` standing in; one independent
`kk:eval-grader` per run reading only the saved actor output. This measures
instruction routing and reporting, not live transport.

### Claude host (actor: `general-purpose` sub-agent, session default model)

| Eval | Assertions | Pass | Fail | Partial | Bytes | Note |
| --- | --- | --- | --- | --- | --- | --- |
| 23 external-api-available | 4 | 4 | 0 | 0 | start | |
| 24 external-api-runtime-failure | 5 | 5 | 0 | 0 | start | |
| 25 external-clink-roster | 5 | 4 | 0 | 1 | start | 25.3: intent/context inlined in the prompt (the workflow permits this; assertion text aligned afterwards) |
| 27 external-discovery-error | 4 | 4 | 0 | 0 | start | |
| 29 external-unknown-identity | 4 | 4 | 0 | 0 | start | |
| 36 external-staged-snapshot | 4 | 4 | 0 | 0 | start | |
| 37 external-corroboration | 4 | 4 | 0 | 0 | start | |
| 38 external-all-reviewers-fail | 4 | 4 | 0 | 0 | start | |
| 39 external-standard-mode-regression | 3 | 2 | 0 | 1 | start | 39.3: finding labeled under the python profile (correct for a `.py` fixture); assertion text aligned afterwards |
| 40 external-default-mapping | 4 | 4 | 0 | 0 | start | |
| 41 external-receipt-limits (first) | 4 | 2 | 2 | 0 | start | **material**: claude counted as corroborator despite a denied criteria read |
| 41 external-receipt-limits (rerun) | 4 | 4 | 0 | 0 | fix A | |
| design 1 external-api-runtime-failure | 4 | 4 | 0 | 0 | start | |
| design 2 external-clink-document-scope | 4 | 4 | 0 | 0 | start | |
| design 3 external-all-reviewers-fail | 4 | 4 | 0 | 0 | start | |
| design 4 standard-mode-regression | 3 | 3 | 0 | 0 | start | |

**Fix A.** Eval 41 exposed an instruction gap: the protocol classified outcomes
as "adequately evidenced" without saying that receipt of the *criteria* is part
of it, so an actor could count a reviewer whose criteria read was denied as a
corroborator because its source reads were observed. Added one clause to the
Reviewer record and Aggregation rules (a denied or unverified criteria read
leaves the result executed but not adequately evidenced; such a reviewer cannot
corroborate) and the matching corroboration bullet in both isolated workflows.
The rerun passed 4/4. Fixture, grader and consequence were inspected before the
change: the fixture's trace shows `functional-review.md` denied while the answer
cites it, which is the scenario's trap.

### Codex host (actor: non-interactive `codex exec`, gpt-6-astra, reasoning xhigh, read-only sandbox)

Driver: `codex/run.sh` in the archive. The user-level `mcp_servers` (pal,
context7, linear, openaiDeveloperDocs) and the installed `kk@claude-toolbox`
plugin were disabled with `-c` overrides so the actor used only the bundled
`kodex-plugin` instructions; `--json` event logs were retained. The first pass
graded the session's final message; reruns and the design-1 regrade graded the
complete multi-message output assembled from the event log
(`codex/build_actor_output.py`).

| Eval | Assertions | Pass | Fail | Partial | Bytes | Note |
| --- | --- | --- | --- | --- | --- | --- |
| 23 external-api-available (first) | 4 | 2 | 1 | 1 | fix A | 23.4: corroboration withheld — fixture said `files_embedded: 9` for a 13-path manifest |
| 23 external-api-available (rerun) | 4 | 3 | 0 | 1 | fix B, fixture 13 | 23.1 evidence limit only |
| 25 external-clink-roster (first) | 5 | 3 | 1 | 1 | fix A | 25.5: internal reviewer required a read trace to corroborate |
| 25 external-clink-roster (rerun) | 5 | 4 | 0 | 1 | fix B | 25.1 evidence limit only |
| design 1 external-api-runtime-failure | 4 | 2 | 0 | 2 | fix A | 1.4: no next-steps menu (non-interactive session); regrade on the complete output: 2/1/1, same omission |
| design 2 external-clink-document-scope (first) | 4 | 2 | 1 | 1 | fix A | 2.4: same internal-reviewer receipt point |
| design 2 external-clink-document-scope (rerun) | 4 | 3 | 0 | 1 | fix B | 2.1 evidence limit only |

**Fix B.** The Codex actors would not count the internal reviewer as a
corroborating supporter without a returned read trace. In live runs the parent
never receives a sub-agent's tool trace, so under that reading corroboration is
unreachable whenever only one external client returns a trace. The protocol now
states that the receipt classification governs external reviewers and that the
internal reviewer supports a finding through its source-tied report. This is an
interpretation consistent with the accepted eval 25 oracle and with the
Claude-host runs; the user may change it. Task 2b had already recorded the
fixture side of this limit.

**Fixture calibration.** Eval 23's synthetic step-2 result reported nine embedded
files while both hosts' actors assemble a 13-path expert manifest for that
fixture (four common criteria, four python checklists, diff, three sources,
intent/context). The Codex actor's refusal to corroborate was the correct reading
of the receipt rule; the fixture now says 13. The Claude-host first-pass grade is
retained as recorded.

**`.1` partials on Codex.** The Codex actors do not narrate which instruction
files they loaded, so component-mode graders could not confirm the protocol read
from text. The event logs show, for all four scenarios, `cat` of the shared
external-review protocol before any subject read other than file listings
(commands #4, #9, #7 and #5 respectively). Recorded as an evidence limit of
component grading, not as a routing failure.

**Non-interactive menu omission (design 1 on Codex).** The actor replaced the
next-steps menu with prose recommendations and declared the read-only review
complete. Two graders rated the same omission PARTIAL and FAIL. The Claude-host
run of the scenario presented the menu. Recorded as a host-mode observation; no
instruction change, because a non-interactive branch would cost every reader for
a harness-specific case.

**Residual quality observation (both hosts).** Several actors read
`checkpoint.md` and, in some runs, the diff in their first tool batch alongside
`SKILL.md`, before the packets and checklists loaded, and said they re-traced
after loading. The replay prompt invites reading the checkpoint (it tells the
actor what stands in for PAL); reading the diff that early is the ordering lapse
ADR 0004 describes. No assertion grades it in component mode; workflow-mode
evidence would. Not changed in this task.

### Live smoke reviews against the verified PAL build

- **Code smoke = the 3.4 isolated code review below.** Discovery once:
  `codereview` not advertised, zero API models, `cli_clients` agy/claude/codex
  found, gemini missing → clink. Authoring provider Anthropic (this and the Task
  1–2b sessions). No operator declaration in the repository, so shipped defaults
  apply: claude excluded (Anthropic, assumed), roster codex (OpenAI, assumed) then
  agy (Google, assumed), gemini retired. Requests: `role: default`,
  `allow_edits: false`, working directory the repository root, the complete
  62-path checked manifest (11 criteria, diff, candidate, affected, historical
  with provenance, intent/context) on each first request, no model parameter,
  no continuation. **Outcome: executed for both roster clients; see 3.4.**
- **Document smoke (`/kk:review-design:isolated clink-isolated-reviews`, default scope).**
  Discovery once → clink; roster codex then agy (assumed), claude excluded, gemini
  retired; 16-path manifest (2 criteria, 3 documents, 11 related source files),
  document-review framing, `role: default`, `allow_edits: false`, no model, no
  continuation. Internal `kk:design-reviewer` 488 s: CONCERNS_FOUND (5×P2, 5×P3).
  codex 186.5 s, receipt unverified: CONCERNS_FOUND (2×P2, 1×P3). agy 252.3 s,
  receipt unverified: 1×P2, 3×P3 (agy also read two verification records outside
  the manifest and disclosed it). No corroborated finding under the protocol; all
  four reviewers agree that design.md lacks the observed provider tier. Outputs:
  archive `live/{internal-design-review,codex-design-review,agy-design-review}.md`.
  Resolution: see 3.5.
- **Multi-author disclosure.** Both smokes took the authoring provider to be the
  provider of the plugin changes (Anthropic). The code-smoke diff also carried
  Task 0 verification records produced by a Codex session, and codex was on the
  roster; the documents were edited by both Claude and Codex sessions. The design
  defines one authoring provider; how to treat mixed authorship is recorded as an
  open user decision in design.md.
- **Latency.** Live clink calls took 273 s (codex, code), 455 s (agy, code),
  186.5 s (codex, documents) and 252.3 s (agy, documents) on this host; Claude
  Code moved each to the background after 120 s and delivered the result. PAL's
  per-client limit is 1800 s. The Codex host's MCP tool timeout for calls this
  long is unverified (no live clink call was made from a Codex host; the
  Codex-host scenarios ran with PAL disabled).

## 3.3 User documentation

Delivered: `klaude-plugin/README.md` and `kodex-plugin/README.md` ("Isolated
reviews with external models": backend selection table, minimum PAL commit,
roster and provider sources with the shipped defaults and the assumed label, a
`CLAUDE.md`/`AGENTS.md` declaration example, custom-name and gemini rules, model
ownership, per-CLI read-access setup from Task 0, no-edit contract, receipt and
corroboration limits, design-review framing); `docs/user-guide/skills.md`
(condensed section, review-design isolated command row);
`docs/user-guide/mcp-servers.md` (Pal: API key optional, clink path, CLI
read-access table, declarations); `docs/getting-started/overview.md`; root
`README.md`; both SKILL.md "Requires" bullets name the README section;
`docs/adr/0011-isolated-review-external-backend.md`. Relative links and anchors
in the edited pages were checked by script; plugin prose contains no link to a
toolbox-only document.

## 3.4 Isolated code review (skill-md + python) — also the live code smoke

Run from the working-tree workflow (`klaude-plugin/skills/review-code/review-isolated.md`
is the subject under test, so the installed 0.24.0 cache was not used). Selector
`git diff master` (base `150bc8b`) against the working tree at `46b3118` plus
uncommitted Task 3 changes, generated trees excluded: 225 files, +7700/−254.
Evidence bundle `/tmp/kk-evidence-t3.6Md7a8/`: diff, review-base blobs of the five
rewritten files with a provenance manifest, change-context record with the Task
Scope block, 62-path checked manifest (11 criteria: 4 common + 3 skill-md + 4
python). Discovery once: `codereview` not advertised, zero API models,
`cli_clients` agy/claude/codex found → clink. Authoring provider Anthropic; no
declaration in the repository; roster codex then agy under the shipped defaults
(assumed), claude excluded, gemini retired; no question asked.

| Reviewer | Provider (source) | Outcome | Receipt | Duration | Result |
| --- | --- | --- | --- | --- | --- |
| kk:code-reviewer (sub-agent) | Anthropic (session model) | executed; source-tied report | n/a (internal) | 548 s | COMMENT, 0×P0–P2, 9×P3 |
| codex (clink) | OpenAI (assumed) | executed, not adequately evidenced | unverified — `events_removed_for_normal`; self-reported list only | 273 s | COMMENT, 1×P2, 2×P3 |
| agy (clink) | Google (assumed) | executed, not adequately evidenced | unverified — no trace; `agy_status SUCCESS`, no denied actions | 455 s | APPROVE (scoped), 2×P3 |

Every request: `role: default`, `allow_edits: false`, repository root as working
directory, identical 62-path manifest, no model parameter, no continuation.
Configured models: codex gpt-6-astra/xhigh (user config), agy native; neither
returned an observed model. No project file changed during either CLI review
(`git status` after each). Corroboration: none — both external receipts are
unverified, so agreeing findings (the `review` role example: internal + codex;
the design-review command row: internal + agy) stay attributed. Full outputs:
archive `live/{internal-code-review,codex-code-review,agy-code-review}.md`.

Findings and resolution (all documentation or wording precision; no routing,
ordering, standard-mode, generation or criteria-extraction regression by any
reviewer):

| # | Finding | Source | Resolution |
| --- | --- | --- | --- |
| 1 | README declaration example names a `review` role the protocol never requests | codex P2, internal P3 | fixed (example without role; `default` role stated) |
| 2 | Docs state corroboration needs receipt from both supporters; protocol exempts the internal reviewer | codex P3 | fixed in both READMEs and the user guide |
| 3 | "Never names a model" ignores API-branch model selection | codex P3 | fixed (API vs clink scoped) |
| 4 | Backend table lacks the internal-only outcome and the `codereview`-not-advertised trigger | internal P3 | fixed |
| 5 | Temp-directory grants assume `/tmp`; workflow uses `mktemp` | internal P3 | fixed (`$TMPDIR`, macOS path named) |
| 6 | "Pal's shipped clients are claude, codex, agy" — PAL also ships gemini | internal P3 | fixed |
| 7 | User-guide Commands table lists `/kk:review-design:isolated` though no command file exists | internal P3, agy P3 | row removed; invocation described as a skill mode; harness behavior without a command file unverified (deferred, unassigned) |
| 8 | ADR understates how unreachable corroboration is on the clink path | internal P3 | fixed |
| 9 | Provider-source precedence listed in an order it does not follow; observed-vs-custom-name unstated | internal P3 | fixed in the protocol and both workflow sentences |
| 10 | No rule for an unanswered roster question (non-interactive sessions suppress all external review) | internal P3 | **deferred to the user** (design decision; recorded in tasks.md) |
| 11 | `.claude/settings.json` `Read(//tmp/**)` propagates downstream via template-sync | internal P3 | **deferred to the user** (their commit a54fd6e; recorded in tasks.md) |
| 12 | Replay fixture layout hints the expected roster; eval 37 agy note explains the rule | internal P3 | note neutralized; layout change deferred (unassigned) |
| 13 | Workflows' "record each reviewer's outcome class" not limited to external reviewers | internal watch item | fixed |
| 14 | review-design SKILL.md typo "tree" | agy P3 | fixed |

Deterministic checks were re-run after these edits (see 3.1 final re-run).

## 3.5 Spec review

`/kk:review-spec:isolated clink-isolated-reviews` (`kk:spec-reviewer`, 436 s, 83
tool uses; mid-implementation scope: Tasks 0, 1, 2, 2b and the completed parts
of Task 3): DEVIATIONS_FOUND, no P0/P1. Confirmed decisions 1–6, the 2026-10-21
corrections (C7 honest reporting; C4/C5 no-edit behavior without a sandbox
claim) and the 2026-10-24 corrections are implemented faithfully; symlinks,
test registration, plugin-root token rules, no toolbox-doc links, unchanged
design-reviewer contract, no new command or agent, oracle placement and both
standard-mode regressions confirmed. Findings and resolution:

| Finding | Type / sev | Resolution |
| --- | --- | --- |
| clink code-review prompt lacks the correctness/security/architecture/quality framing the design requires | SPEC_DEV P2 | fixed: framing added to the clink prompt template (review-code workflow) |
| observed provider source in the protocol but not in design/plan/ADR/user docs | OUTDATED_DOC P2 | fixed: recorded in design.md "Implementation refinements recorded for ratification (2026-10-24)", implementation.md Task 2b and deferred-gaps paragraph, ADR 0011, both READMEs, user guide |
| internal reviewer's corroboration standard and same-provider independence not in design | AMBIGUOUS P2 | recorded in the same design.md section as implementation interpretations the user may change |
| design.md:214 and headers stale | OUTDATED_DOC P3 | fixed |
| 3.3 record mentions a command row that no longer exists; checkbox open | OUTDATED_DOC P3 | fixed (superseding clause; 3.1–3.4 ticked) |
| eval 29 description names three shipped clients; fixture has no codex | DOC_INCON P3 | fixed |
| PAL transport's document branch names only the verification policy as criteria | OUTDATED_DOC P3 | fixed (criteria wording generalized; direct conflict with the caller) |
| code workflow says "both prompts" | SPEC_DEV P3 | fixed ("every reviewer's prompt") |
| user docs overclaim Codex read-only sandbox and "another vendor's model … blind spots" | SPEC_DEV P3 | fixed (scoped to what was verified) |

Accepted limits recorded in implementation.md Task 3 step 2: configured model use
is covered by Task 0 C3 plus source reasoning; clink follow-up continuation by
Task 0 C5 plus source reasoning (no shipped eval exercises a clink
`continuation_id`). The standard-mode design criteria divergence (Task 2,
unassigned) and the declared-duplicate rule without an eval (Task 2b) stay as
recorded. Pre-existing: `docs/getting-started/plugin-only.md` and the plugin
README listed "design review" among command variants; both corrected.

After these edits the deterministic checks were run a third time (see 3.1).

## 3.6 / 3.7

This record is 3.6. **3.7 archive reduction (performed 2026-10-24):** the entire
feature directory was archived per the repository's feature-evidence convention
(`.local-archives/feature-evidence/20261024T202514Z-46b31187/clink-isolated-reviews/`, 48 members,
extraction verified member-by-member), then 37 raw captures (JSON responses,
tool-surface captures, the PAL patch and validation hashes, upstream test output,
fixture copies) were removed from `verification/` with `git rm`. Retained in Git:
`pal-contract.md`, the Linux README with its independent and internal review
records, the Task 1/2/2b eval READMEs and this file — the Task 2/2b READMEs and the
two review records are compact records, so they stay although the 2026-10-23
subtask text named only four files (the implementation plan's "retain summaries"
wording governs). Every link from a retained record to a removed capture was
redirected to `docs/archives/feature-evidence/clink-isolated-reviews.md` with the
archive member named in the link title (50 links across tasks.md, pal-contract.md, the
Linux README, its independent-review record and this file); a link check over all retained records and the three feature
documents found no broken link afterwards. Historical grades and findings are
unchanged. Limits: the captures remain in branch history (a squash merge or the
prepared filter procedure keeps them out of `master`); registering the archive in
`archives.json`, uploading it as a release asset and filtering history are
maintainer actions, as for the 2026-10-20 batch.

## Remaining limits

- Component-mode runs are single samples per scenario per host; they measure
  routing and reporting on synthetic replays, not live transport. One graded run
  does not establish reliability; the live smoke reviews cover transport once.
- Codex-host `.1` assertions are confirmed from event logs, not from the graded
  text.
- Operator-side CLI read grants and PAL publication of `c73dab7d` remain
  activation conditions outside code completion.
