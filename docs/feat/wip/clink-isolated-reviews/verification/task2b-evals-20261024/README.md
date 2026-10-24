# Task 2b evaluation runs — 2026-10-24

Component-mode grading of the two code-review scenarios affected by the
default provider mapping for PAL's shipped clients (design.md, Review
corrections 2026-10-24): eval 40, rewritten from `external-undeclared-mapping`
to `external-default-mapping`, and eval 29 `external-unknown-identity`, which
keeps the roster question for a custom client name (its duplicate-provider
clause was retired with the gemini client later the same day, see below). Historical grades for the old eval 40 in the Task 1 README are retained
unchanged; they graded the superseded "declare or ask" behavior.

## Setup

- Toolbox working tree at `7418a41` (Task 2 commit) plus the uncommitted Task
  2b changes. Instruction bundle `/tmp/kk-bundle-2b.JQj62U/klaude-plugin`
  (`klaude-plugin/` with every `evals/` subtree excluded). The bundle was
  resynced once after the first eval 40 run (see below); worktree hashes at
  the final rerun: `_shared/external-review-invocation.md` `e7ea0cbb21b7eaea`,
  `review-code/review-isolated.md` `ea85f46eb686c5b1`.
- Fixtures staged with `review-code/evals/_harness/setup.sh` into
  `/tmp/review-code-evals._q092qx7` (independent Git repositories, flat
  fixtures added against an empty base).
- Actor: one `general-purpose` Claude Code sub-agent per scenario with the
  eval's ordinary prompt, the staged repository as project root and the bundle
  as plugin root. PAL MCP tools and the Agent tool were declared unavailable;
  the fixtures' synthetic `discovery.json`, `external-results/*.json` and
  `independent-review.md` stood in for their results. Actors could not create
  files, so they used the packet helper's direct-read fallback. No fixture
  edits were observed. Actor model: the session default (not pinned).
- Grader: one `kk:eval-grader` per run in component mode, reading only the
  saved actor output. Raw actor outputs are kept out of Git in the ignored
  local archive
  `.local-archives/feature-evidence/clink-isolated-reviews-task2b-20261024/actor-output/`
  with a SHA-256 inventory (`actor-output.sha256`).
- This measures instruction routing and reporting on synthetic replays; no
  live MCP transport, real sub-agent, Codex host or concurrency.

## Results

| Eval | Assertions | Pass | Fail | Partial | Notes |
|---|---|---|---|---|---|
| 29 external-unknown-identity | 29.1–29.4 (4) | 4 | 0 | 0 | custom `mycli` and the Google duplicate still asked; nothing dispatched |
| 40 external-default-mapping (first run) | 40.1–40.4 (4) | 3 | 0 | 1 | 40.3 partial: override path not stated (see below) |
| 40 external-default-mapping (rerun, post-fix bundle) | 40.1–40.4 (4) | 3 | 0 | 1 | 40.4 partial: corroboration withheld (see below) |
| **Total** | **12** | **10** | **0** | **2** | single sample per run |

Material outcomes (PASS in every run): with no declared mapping, `claude`,
`agy` and `codex` resolved to Anthropic, Google and OpenAI as assumed defaults
and no roster question was asked; `codex` was excluded as the authoring
provider by that default; `gemini` stayed a non-candidate; both roster clients
received one fresh `role: default`, `allow_edits: false`, model-free request
with the full manifest; the roster labeled every provider as assumed; the
verdict was REQUEST_CHANGES; and eval 29 still asked one question covering the
custom name and the duplicate choice before dispatching anything.

**40.3 first-run PARTIAL (fixed).** The actor labeled the providers as assumed
but never told the user that a declaration overrides the defaults; the shared
protocol's report rule had not asked for that. The rule now says that when any
provider is assumed, the report states that a declaration in the project's
agent instruction file overrides the default. The rerun stated it (40.3 PASS).
The grader also noted the first run claimed 14 manifest paths while listing 12;
the rerun listed all 12 individually.

**40.4 rerun PARTIAL (variability, not a defect).** The rerun reported claude's
read trace as observed receipt but declined to mark the P1 corroborated because
the fixture's `independent-review.md` carries no tool trace for the internal
reviewer and the actor would not treat an internal Claude sub-agent and an
assumed-Anthropic client as independent without a declaration. The first run
corroborated and labeled the supporter as assumed, as 40.4 expects. Both
readings keep attribution, the assumed label and the verdict intact; the
difference is how strictly "relevant observable evidence" is applied to a
fixture that gives the internal reviewer no trace. Recorded as a quality
observation; no further rerun was made because another sample would not change
adoption of the default-mapping rule.

## Post-review changes, eval 42 and the gemini retirement (2026-10-24, later)

The isolated code review of Task 2b (APPROVE, five P3) led to protocol
wording changes (independence rule for corroboration, contradicting-model
reconciliation, assumed labels in both workflows' templates and roster lines)
and to a new eval 42 `external-assumed-duplicate` for two shipped Google
clients present without a declaration. Its first graded run was 2 PASS / 2 FAIL
(42.2, 42.3): the actor's single question also asked the operator to confirm or
correct the assumed mappings, which reintroduced the ceremony the defaults were
meant to remove. The protocol's roster-question rule gained the sentence "Do not
ask the operator to confirm or correct an assumed default", and a rerun produced
a question covering only the Google choice; the rerun's output was not archived
(the write was declined) and it was not graded, because the user then retired
the `gemini` client entirely: it is obsolete tooling, `agy` is the Google
client, and a `gemini` entry advertised by PAL is never a candidate. The
agy-versus-gemini duplicate case therefore no longer exists, eval 42 was deleted,
and every fixture's `gemini` client entry, mapping and oracle reference was
removed. The archived first-run output of eval 42 remains in the local archive
as history only.

Eval 29 `external-unknown-identity` lost its declared agy/gemini duplicate and
now covers only the custom `mycli` question; its fixture and assertions
changed, so it was rerun once on the final bytes (bundle resynced; protocol
hash `b2f32a29f39a1d75`; stage `/tmp/review-code-evals.ycxywuiw`): **29 (rerun)
4/4 PASS**, the single question covered only `mycli` and the declared clients
were not asked about. Eval 40's fixture lost its `gemini` (executable missing)
entry; its graded decisions are unaffected and it was not rerun.

## Final runs after the re-review (2026-10-24, last)

The reviewer's re-check (COMMENT: one P2, three P3) pointed out that the
"never ask to confirm an assumed default" rule had lost its only regression
scenario with eval 42. Eval 29 now carries it: its `scope.json` declares no
mapping, so claude and agy are assumed, and its `discovery.json` advertises a
`gemini` client with its executable found, which must be reported as retired.
The protocol also gained the `observed (configured or returned model)` provider
source, explicit precedence for the gemini retirement (never a candidate, even
when declared, disclosed as "retired, not a candidate"), and both workflows'
discovery sentences now repeat that the question never asks to confirm an
assumed default. Both affected scenarios were rerun once on the final bytes
(protocol hash `d6ea6308e237bae1`, review-code workflow `fc992061954e13cc`,
stage `/tmp/review-code-evals.g_4ekx50`):

| Eval | Assertions | Pass | Fail | Partial | Notes |
|---|---|---|---|---|---|
| 29 external-unknown-identity (final) | 29.1–29.4 (4) | 4 | 0 | 0 | one question about `mycli` only; defaults not confirmed; gemini retired |
| 40 external-default-mapping (final) | 40.1–40.4 (4) | 4 | 0 | 0 | override hint stated; corroboration labeled assumed |

Actor outputs: `29-external-unknown-identity.final.actor.md` and
`40-external-default-mapping.final.actor.md` in the local archive.

Final shipped set after Task 2b: evals 23, 24, 25, 27, 29, 36, 37, 38, 39, 40
(`external-default-mapping`) and 41 under `review-code/evals/`, plus the four
design scenarios. Per-run totals for this task: 29 first run 4/4, 29 rerun
4/4, 29 final 4/4, 40 first run 3/0/1, 40 rerun 3/0/1, 40 final 4/4, 42
(retired) 2/2/0. Accepted coverage limit: the one-client-per-provider rule for
operator-declared duplicates is covered by source reasoning only.

## Not run in Task 2b (owner: Task 3.2, bounded verification)

The Codex host, any live clink call and the remaining code-review scenarios
(unchanged by this task). Eval 40 on the Codex host joins the Task 3.2 routing
scenarios only if the operator wants the assumed-label path exercised there;
it is not added to the bounded gate.
