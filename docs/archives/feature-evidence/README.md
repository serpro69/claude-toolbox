# Feature evidence archive register

**Upload verified, 2026-10-20:** all eight feature asset sets, plus functional-review,
are attached to the draft for [v0.24.0](https://github.com/serpro69/claude-toolbox/releases/tag/v0.24.0).
The [release asset receipt](release-assets.json) records the 27 exact filenames,
asset IDs, API/download URLs and SHA-256 values. All downloaded files match the
originals and all nine downloaded archives pass full extracted-member verification.
The canonical links target v0.24.0 after promotion. The receipt retains the actual
draft upload identity separately. Publication, evidence removal and history
cleanup were not performed.

Prepared 2026-10-20 from `3339e897dfad6bd32a6e7e47533bd53cc1510a72`.
The user requested the same local preservation/archive treatment for other
features, assessing each individually. Completed feature directories remain
frozen; these retention records live outside `docs/feat/done/`.

## Scope and decisions

The survey covered `docs/feat/done/`, `wip/` and `archive/`, looking for verification
captures, saved sessions, stored review attempts and executable helpers. Eight
completed-feature directories contain such material. The separate clarify-docs
consolidation experiment belongs with that feature. Functional-review already has
its own verified archive and is not repackaged here. Other feature directories
contain ordinary plans/reference material rather than comparable captures.

| Feature | Material identified | Individual disposition |
| --- | --- | --- |
| [brainstorm-skill](brainstorm-skill.md) | 866 verification files, 8,631,143 bytes | Preserve a compact machine-readable applicability audit outside captures; keep plans and maintained evals. |
| [clarify-docs](clarify-docs.md) | 1,716 verification files, 14,139,698 bytes; separate consolidation experiment | Existing root verification summary is retained; preserve final outcomes, historical failures, limits and the consolidation decision. |
| [clarify-issue-descriptions](clarify-issue-descriptions.md) | 2,814 verification files, 24,345,255 bytes | Preserve the final aggregate assertion ledger outside captures; keep the existing summary and canonical evals. |
| [codex-support](codex-support.md) | One 168,481-byte design session | Keep design/implementation/tasks and record their status inconsistency; session is historical context. |
| [design-skill-refinement](design-skill-refinement.md) | Eight review reports, 86,722 bytes | Keep the small review reports in Git alongside plans; archive is an additional snapshot, not a recommendation to remove them. |
| [go-vendor-integration](go-vendor-integration.md) | One 55,778-byte design session | Keep plans, manifest/tool/tests; session is historical context. |
| [isolated-review-agents](isolated-review-agents.md) | One 28,536-byte design session | Keep both design generations, v2 completion record and review documents. |
| [kubernetes-support](kubernetes-support.md) | Six nested session/probe records, 340,093 bytes | Keep root plans, ADRs and maintained profiles/tests; preserve probe transcripts in the archive. |

Counts above describe candidate evidence areas, not whole-archive totals. Each
archive contains the **entire feature directory**, preserving hidden files,
symlinks and unsuccessful attempts. The clarify-docs archive also contains
`docs/feat/reviews/clarify-docs-consolidation/`. Only regenerable directories named
`__pycache__` are excluded and recorded by the existing inventory tool.

## Preservation policy

- Keep each feature's design/implementation/task decisions and useful summary
  records in Git. The individual notes identify existing records and any new
  compact copies; no old grade or completion state is rewritten.
- Maintained evals, fixtures, oracles, profiles, source code and tests outside
  capture trees remain in place. No live runner depends on the archived captures
  among the inspected scripts/tests/workflows.
- The only standalone script found in these captures is the issue experiment's
  dated native-session exporter. It hardcodes a Mac session directory/date and
  has no current consumer. Preserve its original bytes in the archive; do not
  promote it to a new maintained framework. Other `.py`/`.yaml` files are subject
  snapshots, not execution-tool dependencies.
- Preserve available evidence and disclose its limits. Missing old scratch
  directories do not trigger recovery work or new behavioral acceptance gates.
  No new model runs, regrading, live-service claims or release tags are required.

## Local archives and verification

The ignored directory is
`.local-archives/feature-evidence/20261020T172123Z-3339e897/` relative to the project.
Each feature gets a `.tar.gz`, `.manifest.json` and `.sha256` file. Members use
`payload/` followed by the original repository-relative path. Retention notes and
applicable compact records are included as supplementary members.

[The completed receipt](archives.json) records all archive/checksum paths, sizes,
SHA-256 values, member counts and original source roots. All eight archives pass
checksum validation and complete extracted-member verification. Every extracted
feature tree matches the original file/hash/mode/symlink/directory inventory;
the supplementary consolidation tree also matches. This verifies preservation,
not the historical experiments' behavioral conclusions.

| Feature | Compressed bytes | Local verification |
| --- | ---: | --- |
| brainstorm-skill | 2,446,345 | PASS |
| clarify-docs, including consolidation | 3,662,151 | PASS |
| clarify-issue-descriptions | 6,159,421 | PASS |
| codex-support | 64,409 | PASS |
| design-skill-refinement | 51,979 | PASS |
| go-vendor-integration | 35,609 | PASS |
| isolated-review-agents | 42,374 | PASS |
| kubernetes-support | 165,039 | PASS |
| **Total** | **12,627,327** | **8 verified archives** |

The two compact record copies match their originals byte-for-byte. The brainstorm
ledger also reconciles with all 32 accepted result files/146 original assertions;
the issue ledger reconciles 29 rows/133 assertions. These checks preserve recorded
results without regrading them. Existing behavioral suites and model runs were
not rerun, since no executable code or operative instruction changed.

Archives contain the retention notes as they stood at assembly time. This final
register and completion receipt are retained separately in Git. All original
feature trees, the related consolidation tree and maintained plugin/tool/test
files remain unchanged. All archive assets are excluded by the existing ignore
rule; staging and extraction copies remain alongside them for inspection.

Independent review approves the per-feature preservation decisions and copied
ledgers without findings. That review compared the summaries with their original
records; archive-byte verification and extraction comparisons above were performed
by the parent session. Local-link, JSON and authored-document whitespace checks
also pass. No runtime behavior or historical acceptance was reassessed.

Original evidence removal, link repair, Git-history cleanup and later publication
are separate work. This operation creates local archives and durable retention
records; it does not remove source directories or rewrite history.

For retrieval, use the release asset filename/URL from `release-assets.json`,
then the original repository-relative member path under `payload/`. The local
paths in `archives.json` preserve preparation provenance; they are not required
to retrieve uploaded evidence. The release/download URLs already target v0.24.0,
as specified by the user. Until promotion, use authenticated asset API URLs/IDs
or the receipt's upload-observation draft prefix. Verification applies to those
observed draft assets, not a claim that the final URLs are already live.

The two copied JSON records are byte-identical historical records. Their internal
relative paths retain their original interpretation, documented in the feature
notes; they must not be resolved relative to the new `records/` directory.
