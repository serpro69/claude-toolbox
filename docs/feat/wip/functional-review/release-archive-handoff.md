# Release archive handoff

> Prepared: 2026-10-20 after feature verification and final reviews
> Owner: human maintainer, AI-guided Task 13.7
> Status: local and uploaded draft-release archives verified; human reference repair and cleanup remain

[Feature verification](verification-summary.md) is complete. Task 13 stays open
because its release-housekeeping step explicitly assigns execution to the human
maintainer. The user authorized local archive preparation in the project before
cleanup; no release or tag is required at this stage. The feature remains under
`docs/feat/wip/` until its remaining housekeeping closes.

## Accepted local-first sequence — 2026-10-20

Create and verify the archive in `.local-archives/functional-review/`, already
ignored by `.gitignore`. Record its checksum, manifest and member paths. Local
extraction and integrity verification satisfy the archive prerequisite for
cleanup. The human then performs reference repair and history cleanup, creates
the release, and attaches the verified assets. Release creation, a tag and upload
are not prerequisites for local preparation or cleanup. Preserve the ignored
archive if cleanup uses a fresh clone or removes ignored files.

## User-selected draft upload — completed 2026-10-20

The user subsequently requested uploading all nine archive sets to the existing
[v0.24.0-draft release](https://github.com/serpro69/claude-toolbox/releases/tag/untagged-c0a403db0376380a3b00),
before cleanup. That explicit instruction supersedes the earlier upload ordering.
Release ID: `418689774`; it remains a draft with an empty `tag_name`. No tag or
publication was created by this upload.

All 27 existing assets uploaded without overwriting anything: nine `.tar.gz`,
nine `.manifest.json` and nine `.sha256` files, totaling 227,326,167 bytes.
Remote names, sizes, uploaded states and reported digests matched the originals.
Fresh downloads of all 27 files match the original SHA-256 values; all nine
downloaded archives were extracted and passed complete member-manifest verification.

[The release receipt](../../../archives/feature-evidence/release-assets.json)
records actual asset IDs and download/API URLs, including this feature's three
assets. Retrieve the named archive, then locate members under `payload/`; the
original evidence subtree remains
`payload/docs/feat/wip/functional-review/verification/`.
The `.local-archives/` preparation layout is not needed for retrieval.

Draft access remains authenticated. Refresh the observed release/download URLs
if its name/tag changes during publication. Upload and retrieval checks are now
complete; source removal, reference repair and Git-history cleanup remain pending.

## Verified local archive — 2026-10-20

Directory, relative to the project root:
`.local-archives/functional-review/20261020T171149Z-9fa9906a/`.

| Artifact | Observed value |
| --- | --- |
| Archive | `functional-review-evidence-20261020T171149Z-9fa9906a.tar.gz` — 188,522,487 bytes |
| Archive SHA-256 | `ce99e6e69bcb6a266573e69ad9a561d3c891a343d90568abe8fe39efd191149d` |
| Manifest | `functional-review-evidence-20261020T171149Z-9fa9906a.manifest.json` |
| Manifest SHA-256 | `022c4c1561c3b776035213250260a9cf34010b8d457d1c4d111c3dd299542019` |
| Checksum file | `functional-review-evidence-20261020T171149Z-9fa9906a.sha256` |
| Member prefix | `payload/` |
| Member inventory | 73,126 regular files, 66 symlinks, 9,544 directories |

Both checksum entries pass. A fresh local extraction passes the complete member
manifest. Its historical `verification/` subtree also matches the original tree's
full file/hash/mode/symlink/directory inventory: 73,099 files, 66 symlinks, 9,537
directories and 730,127,674 regular-file bytes, with recorded cache exclusions.
The core source export matches its original checksum.

The archive also contains feature documents/reviews and the assembly-time
working-tree patch under `payload/original-inputs/preparation.patch`. Feature
document copies are snapshots from assembly, preceding the final receipt and one
subsequent audit wording correction; the retained live documents carry the current
local-first sequence. Original evidence bytes are unchanged.

All three assets are ignored by Git. The staging copy is in `payload/` and the
verified extraction in `extracted/` beside them. No release asset was uploaded;
no repository evidence was removed and no history was rewritten. The local
archive prerequisite is complete. Independent documentation review approves the
sequence; archive verification above is parent-executed evidence.

## Inventory and retention map

The current `verification/` tree contains **73,099 regular files, 66 symlinks and
730,127,674 regular-file bytes**, excluding 17 regenerable `__pycache__` files.
This is a filesystem inventory, not an archive integrity manifest. Recompute it
when packaging; do not assume a later tree is identical.

| Location | Regular files | Bytes | Disposition |
| --- | ---: | ---: | --- |
| `verification/task12/` | 67,586 | 666,991,303 | Archive all experiments, failures, freezes, captures, grades, reviews and source/config archives; assess reusable tools below first. All 66 symlinks are here. |
| `verification/task2b/` | 2,249 | 24,602,355 | Archive capture-resolution evidence and historical receipt contracts; assess reusable adapter code first. |
| `verification/task2/` | 828 | 7,034,843 | Archive baseline captures and their supporting inputs. |
| `verification/task4/`, `task5/`, `task6/` | 1,628 | 23,777,911 | Archive implementation-slice evidence and earlier attempts. |
| `verification/task8/` | 655 | 5,315,946 | Archive grading evidence; assess reusable packaging logic first. |
| Remaining root/evidence/task7/task9/task10/task11 files | 153 | 2,405,316 | Archive together, preserving relative paths and provenance. |

**Keep in Git:**

- `verification-summary.md`, `verification-results.md`, current design,
  implementation, task and acceptance decisions, and final review records.
- Canonical evals, subject fixtures, oracles and harness documentation under
  `klaude-plugin/`, plus generated counterparts.
- Maintained staging/packet helpers and tests: review-code's
  `evals/_harness/setup.sh`, `scripts/prepare_instructions.py`,
  `test/test-review-eval-staging.sh`, `test/test-review-instructions.sh`,
  `test/review_instructions_test.py`, and related packaging checks.
- [Retained capture/grading tooling](../../../../scripts/functional-review-evals/README.md),
  its provenance record, synthetic tests and `test/test-functional-review-tools.sh`.
- [Source retention audit](archive-source-audit.md), including the accepted
  limitation on exact replay of older experiments.

**Archive outside Git:** the complete retained `verification/` tree, including
unfavorable attempts and original source/configuration inputs. Preserve original
commit IDs and hashes even if history is later rewritten. Existing evidence is
redacted; do not add authentication files, live stores or private vault history.
Only regenerable cache exclusions are permitted, with their scope recorded.

## Tooling extraction — completed preparation

The historical runners are not portable standalone scripts. Copying only the
entry file and deleting the evidence tree would break imports and frozen inputs.
The selected reusable scope now lives under `scripts/functional-review-evals/`.
Its dependency closure is standard library plus sibling modules. The test wrapper
copies it outside the repository and runs isolated imports; no historical tree,
account configuration, live model or network service is needed.

| Starting point | Retained disposition |
| --- | --- |
| `task12/opus55/matrix.py` | Archive the dated matrix/registrations/snapshots. Do not retain its import chain as a new general runner. |
| `task12/rework/{capture,driver,runtime,probe_pal}.py` | Retain `runtime.py` byte-identically with synthetic lifecycle tests; archive launch policies and historical PAL transport. |
| `task12/controller.py` and root capture/bundle helpers | Retain `prepare-bundles.py` as byte-identical `bundles.py`; canonical `setup.sh` continues to own fixture staging. Archive dated controllers. |
| `task2b/controller.py` and `capture-codex.py` | Extract public sanitization and paginated child-history collection into `receipts.py`, with explicit client/credentials and no account lookup. Exact prompt capture remains unverified. |
| `task8/prepare_grading.py` | Extract sealed event/fixture/rubric/grader packaging into `grading.py` with explicit inputs; preserve original seals and source identity. |

[Extraction provenance](../../../../scripts/functional-review-evals/provenance.json)
records original paths and SHA-256 values. All **15 offline tests pass on Python
3.11.13 and 3.12.11**, including execution from outside the checkout. All **13
repository shell suites pass**; the focused suite was rerun after the review fix.
[Independent source review](reviews/retained-tooling-review.md) approves after
restoring history persistence before supplementary metadata retrieval. Live
provider behavior remains untested; no new experiment was run.

`inventory.py` supplies manifest creation/verification for the local archive
step. It records regular-file hashes/modes, symlink targets, directory membership
and explicit cache exclusions. It does not prove external-input completeness.

## Source preservation — accepted scope

[The source audit](archive-source-audit.md) finds one core candidate archive that
must be exported from Git and fifteen early temporary source identities missing
from this checkout. Most early content exists elsewhere in the retained evidence;
18 of 845 distinct source hashes remain unmatched by the bounded file/archive
search. On 2026-10-20 the user accepted that these temporary inputs are unavailable
and approved archiving the retained material with this exact-replay limitation.
Recovery is no longer a prerequisite. Keep the audit findings and original
identities; do not represent the missing inputs as recovered. The still-available
core export remains part of archive assembly. The evidence tree and original Git
history remain intact.

## Human execution sequence

[Concrete command guidance](release-archive-commands.md) covers staging,
the known core source export, local inventory/extraction checks and later upload.
It includes the accepted source limitation in the staged records; no command has
been executed as part of preparing that guidance.

1. **Assemble retained content.** Tooling extraction is complete; retain the
   accepted source limitation and compact records, and export the available core
   source. A release tag is not needed.
2. **Package locally, outside Git tracking.** Archive the whole relative
   `docs/feat/wip/functional-review/verification/` tree (or its actual location
   after an explicitly chosen move), preserving symlinks and member paths.
   `tar -czf` with `-C <repository-root>` can produce the archive; exclude only
   `*/__pycache__` and record that exclusion. Use the ignored project directory
   `.local-archives/functional-review/` and a date/revision-based filename.
3. **Create integrity records.** Compute the archive's SHA-256 (`sha256sum`),
   plus a manifest of relative member paths, regular-file hashes, symlink targets,
   counts, exclusions and original source/fixture/grader identities. An archive
   checksum alone does not document omitted inputs.
4. **Verify the local archive.** Check its checksum, extract it into a fresh
   directory and verify the member manifest. Locate representative successes,
   failures, corrected grades and original inputs by their member paths.
5. **Update durable locators before deletion.** Record local asset paths,
   checksum and member-path lookup in `verification-summary.md`. Redirect
   references from retained docs/reviews to the compact record/local archive
   locator, with explicit members. Keep future release upload tracked separately.
6. **Perform maintainer-owned cleanup.** Remove archived evidence only after the
   checks above. Choose the affected refs and history-rewrite scope explicitly;
   the prior plan names `git filter-repo`, reflog expiry and garbage collection.
   No generic destructive command is supplied without that scope. Keep an
   old-to-new revision mapping and ensure the archive remains interpretable
   without the original Git objects.
7. **Attach to the release later.** After cleanup and release creation, upload
   the existing archive/checksum/manifest, download and verify the assets, and
   record the actual tag/URL. Then close 13.7/Task 13 and move the feature docs
   to `docs/feat/done/`, updating local links.

## Completion record to fill with observed values

| Field | Current value |
| --- | --- |
| Release tag and URL | User-selected draft URL above; actual `tag_name` is empty |
| Retained tooling destination and offline verification | `scripts/functional-review-evals/`; 15 tests pass on Python 3.11.13/3.12.11 outside checkout; source review APPROVE |
| Original source-input disposition | Early temporary inputs accepted as unavailable; core export remains part of assembly |
| Local archive, checksum and manifest paths | Recorded above; all ignored by Git |
| Archive SHA-256 and exclusion list | Recorded above and in the manifest; only cache directories excluded |
| Local extraction/member verification | Passed, including direct original-evidence comparison |
| Release upload/download verification | Completed against draft release `418689774`; all 27 files and nine extracted archives verified |
| Evidence removal and history cleanup confirmation | Pending |

These pending fields are release housekeeping. They do not reinstate retired
LLM grading gates or invalidate the completed feature verification.
