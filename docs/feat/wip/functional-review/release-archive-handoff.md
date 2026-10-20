# Release archive handoff

> Prepared: 2026-10-20 after feature verification and final reviews
> Owner: human maintainer, AI-guided Task 13.7
> Status: inventory/guidance prepared; tooling extraction, archive/upload, retrieval and cleanup unperformed

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
- The minimal selected capture/grading tooling and its tests after extraction
  from the historical tree. That extraction is still pending.

**Archive outside Git:** the complete retained `verification/` tree, including
unfavorable attempts and original source/configuration inputs. Preserve original
commit IDs and hashes even if history is later rewritten. Existing evidence is
redacted; do not add authentication files, live stores or private vault history.
Only regenerable cache exclusions are permitted, with their scope recorded.

## Tooling extraction prerequisite

The historical runners are not portable standalone scripts. Copying only the
entry file and deleting the evidence tree would break imports and frozen inputs.
Before removal, select the reusable execution scope, relocate its full dependency
closure (for example under `scripts/functional-review-evals/`), and prove its
offline tests work without the historical tree.

| Starting point | Dependency/portability work to resolve |
| --- | --- |
| `task12/opus55/matrix.py` | Imports `task12/rework/driver.py` and `runtime.py`; loads `task2b/controller.py` through the controller's verification root; uses dated run directories and declared snapshots. |
| `task12/rework/{capture,driver,runtime,probe_pal}.py` | Capture/driver load `task12/controller.py`; the PAL helper also loads its historical predecessor. Retain relevant runtime tests and replace history-dependent fixtures with small owned fixtures. |
| `task12/controller.py` and root capture/bundle helpers | Resolve repository-root assumptions, `capture-seeds.py`, `prepare-bundles.py`, rubric/grader paths and the declared dependency lists. Separate reusable execution from historical source pins. |
| `task2b/controller.py` | Retain the selected Codex receipt adapter and its actual dependencies/tests; do not imply exact prompt capture where only receipt/use is available. |
| `task8/prepare_grading.py` | Currently binds to Task 2 capture indexes, frozen inputs and a fixed verification-root layout. Extract only reusable packaging logic with explicit inputs and its tests. |

This is the assessed starting map, not a completed extraction manifest. Keep the
tree until the maintainer has selected and validated the retained tool set.
Historical variants and unused experiment-specific adapters remain in the archive.
No general evaluation framework or new live batch is required for this cleanup.

## Human execution sequence

1. **Choose the release and finish retention.** Use the release that contains the
   merged feature. Its tag and URL are not yet assigned here. Complete the tooling
   extraction above and retain the compact records before removing any evidence.
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
| Retained tooling destination and offline verification | Pending |
| Archive, checksum and manifest asset names | Pending |
| Archive SHA-256 and exclusion list | Pending |
| Download/member verification | Pending |
| Evidence removal and history cleanup confirmation | Pending |

These pending fields are release housekeeping. They do not reinstate retired
LLM grading gates or invalidate the completed feature verification.
