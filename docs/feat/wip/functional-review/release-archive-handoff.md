# Release archive handoff

> Prepared: 2026-10-20 after feature verification and final reviews
> Owner: human maintainer, AI-guided Task 13.7
> Status: tooling extracted/tested/reviewed; source-input recovery required; archive/upload, retrieval and cleanup unperformed

[Feature verification](verification-summary.md) is complete. Task 13 stays open
because its release-housekeeping step explicitly assigns execution to the human
maintainer. No archive, release asset, removal or history rewrite was performed
by this task. The feature remains under `docs/feat/wip/` until that step closes.

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
- [Source retention audit](archive-source-audit.md), including the exact recovery
  gap that must be resolved before evidence removal.

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

`inventory.py` supplies manifest creation/verification for the human archive
step. It records regular-file hashes/modes, symlink targets, directory membership
and explicit cache exclusions. It does not prove external-input completeness.

## Source preservation prerequisite — open

[The source audit](archive-source-audit.md) finds one core candidate archive that
must be exported from Git and fifteen early temporary source identities missing
from this checkout. Most early content exists elsewhere in the retained evidence;
18 of 845 distinct source hashes remain unmatched by the bounded file/archive
search. Recover and verify these inputs, or obtain an explicit preservation
decision if recovery is impossible. No exception is implied by the tooling tests.
The evidence tree and original Git history remain intact.

## Human execution sequence

[Concrete command guidance](release-archive-commands.md) covers staging,
the known core source export, inventory, upload and downloaded-member checks.
Its source-recovery stopping point is mandatory; no command has been executed
as part of preparing that guidance.

1. **Choose the release and finish retention.** Use the release that contains the
   merged feature. Its tag and URL are not yet assigned here. Tooling extraction
   is complete; resolve the source-input audit and retain the compact records
   before removing any evidence.
2. **Package outside the checkout.** Archive the whole relative
   `docs/feat/wip/functional-review/verification/` tree (or its actual location
   after an explicitly chosen move), preserving symlinks and member paths.
   `tar -czf` with `-C <repository-root>` can produce the archive; exclude only
   `*/__pycache__` and record that exclusion. Use an output directory outside
   the repository and an actual release-specific filename.
3. **Create integrity records.** Compute the archive's SHA-256 (`sha256sum`),
   plus a manifest of relative member paths, regular-file hashes, symlink targets,
   counts, exclusions and original source/fixture/grader identities. An archive
   checksum alone does not document omitted inputs.
4. **Upload and retrieve.** Attach archive, checksum and manifest to that release,
   then download and extract them outside the checkout. Verify the downloaded
   checksum and member manifest; locate representative successes, failures,
   corrected grades, frozen actor inputs and runtime configuration by their
   original member paths.
5. **Update durable locators before deletion.** Record the actual release URL,
   asset names, checksum and member-path lookup in `verification-summary.md`.
   Redirect references from retained docs/reviews to the release archive and
   explicit member paths. Verify the extracted tool tests independently of
   `verification/`.
6. **Perform maintainer-owned cleanup.** Remove archived evidence only after the
   checks above. Choose the affected refs and history-rewrite scope explicitly;
   the prior plan names `git filter-repo`, reflog expiry and garbage collection.
   No generic destructive command is supplied without that scope. Keep an
   old-to-new revision mapping and ensure the archive remains interpretable
   without the original Git objects.
7. **Close 13.7.** Record retrieval/integrity, retained-content checks and the
   human's confirmation of cleanup in the summary/tasks. Then mark Task 13 done
   and move the feature documentation to `docs/feat/done/`, updating local links.

## Completion record to fill with observed values

| Field | Current value |
| --- | --- |
| Release tag and URL | Pending |
| Retained tooling destination and offline verification | `scripts/functional-review-evals/`; 15 tests pass on Python 3.11.13/3.12.11 outside checkout; source review APPROVE |
| Original source-input completeness | Open: core export plus early-source recovery; see source audit |
| Archive, checksum and manifest asset names | Pending |
| Archive SHA-256 and exclusion list | Pending |
| Download/member verification | Pending |
| Evidence removal and history cleanup confirmation | Pending |

These pending fields are release housekeeping. They do not reinstate retired
LLM grading gates or invalidate the completed feature verification.
