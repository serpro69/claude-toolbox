# diff-skill: Go profile (deff036 → 7ca516b)

## Summary

**Verdict: Degraded — 1 degradation, 0 identified complexity regressions, 1 pre-existing advisory.** The commit preserves the principal recommendations and all fenced examples, and improves same-phase links. However, deleting entire unavailable-reference clauses also removes useful topic guidance. The implementation treats a target shipped in another profile phase as unavailable.

This is a commit-scoped application of the `/kk:diff-skill` degradation rubric to the Go profile assets consumed by skills. No files under either plugin's `skills/` directory changed. Reviewed all changed canonical profile hunks, the manifest, the reference transformer and its tests, and supporting target content. The changed files total approximately 403 KiB across both revisions; this is not an exhaustive traversal or behavioral evaluation of every consuming skill.

Canonical profile statistics:

| Measure | Result |
| --- | --- |
| Changed files | 27 |
| Added / deleted lines | 69 / 158 |
| Net line reduction | 89 |
| Size reduction across changed files | 11,063 bytes, or 5.2% |
| Changed fenced examples | 0 |
| Missing local Markdown file targets in changed HEAD files | 0 of 74 links checked |

The Codex profile changes duplicate the canonical changes, explaining the commit's 316 deleted lines. The 158 canonical deletions include lines replaced by local-link versions, headings, and whitespace; they are not 158 deleted rules.

Of 155 complete upstream skill identifiers in the previous versions of these files, 52 have a same-phase manifest target, 62 have targets only in other phases, and 41 have no vendored target. These counts are occurrences, not distinct skills; truncated identifiers in index descriptions are excluded.

## Degradations

### D1 — Removing navigation clauses also removes semantic guidance

**Location:** `cmd/vendor-profiles/skillrefs.go:56` restricts resolution to the same phase; line 66 removes the clause when no such target exists. `removeSkillClause` also removes the topic description following the identifier. `cmd/vendor-profiles/skillrefs_test.go:102` explicitly expects cross-phase references to disappear.

Examples of information lost in HEAD:

- Both error-handling variants lose the reference description “nil interface trap and nil error comparison pitfalls.” Neither topic appears elsewhere in the current Go profile under those terms. The missing upstream safety skill was already unavailable, but the reminder itself was present before this commit.
- `implement/structs-interfaces.md` loses its explicit pointer to interface naming conventions, including the method-plus-`-er` rule. That guidance still ships in `review-code/naming.md`.
- `review-code/performance.md` loses pointers to benchmarking methodology and the `benchdiff`/`cob` setup topic. `test/benchmark.md` still contains benchmarking guidance and describes those tools, although its detailed CI reference is not vendored.
- `implement/context.md` loses its observability cross-reference even though `design/observability.md` ships. Context's own trace-propagation summary remains, so this particular deletion loses navigation rather than the entire topic.

**Impact:** This is a loss of explicit prompts and discoverability, not deletion of complete implementations or a demonstrated runtime failure. The previous upstream skill identifiers were not valid local links, so the 62 cross-phase removals must not be described as 62 formerly working local links being broken. Nevertheless, their topic descriptions were usable instructions, and existing packaged targets could support local references or concise inline guidance.

**Recommended follow-up:** Preserve useful topic text when stripping an unavailable identifier. Prefer same-phase targets; where the subject warrants a reference to another phase, resolve that packaged target explicitly or retain a self-contained reminder if phase isolation is intentional. Do not restore calls to uninstalled skills. Change the generator and its preservation assertions, then regenerate both plugin variants; direct edits to vendored output would be overwritten.

**Status:** Resolved in the user-authorized follow-up described below. The original assessment above remains the record of commit `7ca516b`.

## Pre-existing Complexity

### A1 — Some detailed-reference labels already point to material outside the vendored set

The manifest mainly imports upstream `SKILL.md` files. The older `RewriteLinks` transformation strips non-vendored link destinations while retaining their labels. Consequently, summaries such as “pprof Reference,” “benchstat Reference,” and “Slice Internals Deep Dive” already lacked their detailed local files in the parent revision. HEAD did not remove those detailed documents.

**Status:** Outside this commit assessment and its follow-up; owner unassigned. If deeper coverage is wanted, audit the relevant manifest entries and selectively vendor needed reference files, or make their summaries self-contained, then verify the named guidance is available in the packaged profile. Avoid interpreting this older coverage limit as new content loss in HEAD.

## Neutral Changes

- Same-phase upstream identifiers become usable local Markdown links.
- Core recommendations survive, including `strings.Builder` in loops, early error returns, context checks during retries, and `crypto/rand` for keys and tokens.
- Every fenced example in the changed canonical files is identical across the two revisions.
- Removing empty navigation headings and rendering index previews as plain text are reasonable cleanup.
- Static target checks found no missing local file destinations in the changed HEAD files. This checks file existence, not fragment correctness or whether a target provides every topic its label promises.

Verification used the immediate-parent diff, manifest classification, target-content inspection, and a read-only comparison of fenced blocks and link destinations. No runtime tests or skill evaluations were run; they would not by themselves establish semantic preservation of the removed prose.

## Follow-up resolution — 2026-10-30

The user authorized fixing D1. The candidate based on `7ca516b` now prefers
same-phase targets and falls back to a packaged copy in another phase. Multiple
fallback copies resolve by lexical phase/file order. Unavailable-reference
descriptions survive as plain `Related topics:` text; navigation without a
description can still disappear. No uninstalled skill invocation is restored.

Regression coverage includes the nil-interface reminder, data-structure safety
introduction, nested descriptions and clause boundaries, same-phase preference,
manifest-order-independent fallback, and an integrated cross-phase link whose
target is actually written. Both plugin variants were regenerated, and the
vendoring behavior is documented in `docs/contributing/architecture.md`.

Verification against the persisted candidate:

- `go test ./cmd/vendor-profiles/...` passed (capy run
  `0bb978a0-79fe-4206-a83f-0bdbc8a1d1ac`).
- `make vendor-profiles`, `make generate-kodex`, and `make plugin-graph` passed,
  including plugin/Codex structure checks (capy run
  `bb347e68-902e-4ac7-9580-dbfd47617540`; Python 3.12 selected on PATH for TOML
  validation). This final run supersedes `7736e61c-cc8e-4db6-9134-9e217d0af9fb`
  after the subpage correction below. Link validation reported no broken edges
  or orphans.
- All fenced examples in the 27 canonical files differing from pre-regression
  parent `deff036` are unchanged. `git diff --check` passed.
- Earlier runs before the implementation edits persisted are excluded from
  candidate verification evidence.

The isolated `code-reviewer` (GPT-6.1 Sol, OpenAI) approved the candidate without
findings after inspecting the transformer, tests, call chain, manifest,
documentation, and all canonical/generated change hunks. It did not independently
execute tests or fetch upstream content. Deployment/migration compatibility is
not applicable to this generator-only fix. No findings qualified for indexing.

External review uses PAL clink: `claude` was the only eligible executable found,
with Anthropic assumed from the shipped client mapping (an operator declaration
overrides that assumption). API review was unavailable; `agy` and `codex` were
unavailable, and `gemini` is retired. The request supplied the same 11 criteria
files and source/diff evidence. Its initial native verdict was **COMMENT** with
one P3: a `(testing.md)` subpage hint was left behind while the generated link
targeted the broader database overview. The fix now resolves a hinted
`references/<filename>.md` only when that specific file is packaged, otherwise
retaining its topic description. Two regression cases cover present and absent
hinted files. Both generated testing guides now retain the database integration
test topic without the misleading overview link.

The external reviewer also requested the pinned upstream sources and the
pre-regression output. Both were supplied as complete files with origin/hash
inventories, alongside a parent-to-final restoration diff. The final internal
review remains **APPROVE**, with no findings or outstanding evidence requests.
The external follow-up's native verdict is **APPROVE**, scoped to the code; its
P3 is **Resolved**, and restoration against the pre-regression parent is now
**Supported**. Its observed model was `claude-opus-5-5` (Anthropic); the configured
model was not independently inspected. No actionable findings remain.

The external follow-up has observable successful reads of all 11 criteria,
the transformer/tests, restoration diff, provenance and inventory files, plus
targeted final-diff/generated-content reads and searches. It inspected the
captured final verification run without executing tests. Receipt is adequately
evidenced for this scoped approval. Several optional shell commands to recompute
all historical Git blob hashes were denied by that reviewer's permissions;
that check remains unverified by the external reviewer. The supplied original
source, restoration diff, and successful source reads support the scoped review
without requiring permission expansion. General Markdown parsing and detailed
files never packaged before the regression remain outside the fix.

External observations outside the fix are recorded here without adding gates:
generic retained descriptions and helper length are quality observations;
table-description branch coverage is optional with no affected generated row.
The older three-character fence matcher, byte-based preview truncation, and
same-phase duplicate ordering remain unchanged. No affected current input was
identified. Owner unassigned: if upstream changes exercise these cases, add a
reproduction and respectively match fence lengths, truncate previews at UTF-8
boundaries, or define/reject duplicate same-phase mappings. These are inherited
limitations, not blockers for restoring the removed guidance.
