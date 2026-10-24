# clink-isolated-reviews retention

Prepared 2026-10-24 during Task 3.7 of the feature, from branch `feat/clink_reviews`
at `46b311870e8d` plus the uncommitted Task 3 changes present at assembly time.
The user-approved criterion (tasks.md, 2026-10-23) keeps compact records in Git and
moves raw captures to the ignored local archive with a hashed inventory.

Archive the **entire** feature directory (then `docs/feat/wip/clink-isolated-reviews/`, now `docs/feat/done/clink-isolated-reviews/`) (48 members,
106842 bytes compressed). Members use `payload/` followed by the
original repository-relative path. Extraction was verified member-by-member
against the originals before any file was removed.

Local archive (ignored by Git):
`.local-archives/feature-evidence/20261024T202514Z-46b31187/clink-isolated-reviews/clink-isolated-reviews-evidence-20261024T202514Z-46b31187.tar.gz`
(SHA-256 `5495a5fff62c7cedd4aac017139d0b708e44da10bb9baa1c79b291470c466900`), with the manifest
`clink-isolated-reviews-evidence-20261024T202514Z-46b31187.manifest.json` and checksum file `clink-isolated-reviews-evidence-20261024T202514Z-46b31187.sha256` alongside.

**Kept in Git:** `design.md`, `implementation.md`, `tasks.md`, and under
`verification/`: `pal-contract.md`, `linux-20261023/README.md`,
`linux-20261023/independent-review.md`, `linux-20261023/internal-review.md`,
the Task 1, Task 2 and Task 2b eval READMEs, and `final.md`. Historical grades,
findings and the Task 0 C1–C8 results are unchanged; links from those records to
removed captures now point at this note with the archive member named in the
link title.

**Removed from Git after archiving** (37 raw captures: live MCP responses,
discovery/tool-surface captures, the PAL discovery patch and validation hashes,
upstream test output, and the disposable fixture copies):

- `payload/docs/feat/wip/clink-isolated-reviews/verification/agy-default-mcp-followup.json` (9375 bytes, sha256 `305147449be40593…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/agy-default-mcp.json` (10810 bytes, sha256 `bcee03dcfb139288…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/agy-initial.json` (3683 bytes, sha256 `2b4ffae95e28f59d…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/claude-after-auth.json` (6851 bytes, sha256 `79a09c75f07e5a8d…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/claude-default-mcp-followup.json` (7213 bytes, sha256 `06ca31d5894a6cd5…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/claude-default-mcp.json` (14246 bytes, sha256 `98dd2cdd6e1840fa…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/claude-followup.json` (5073 bytes, sha256 `ebded61b679d6d94…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/claude-initial.json` (4795 bytes, sha256 `26e9abb3d2d6265e…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/claude-read-grant.json` (8090 bytes, sha256 `975ee4e6d0f4eef0…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/clink-surface-after-manifest.txt` (2807 bytes, sha256 `358580806e1a41ba…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/codex-default-mcp-followup.json` (5283 bytes, sha256 `5545d2a7c8125723…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/codex-default-mcp.json` (7854 bytes, sha256 `4748615494b05877…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/listmodels-after-manifest.json` (3462 bytes, sha256 `91fb1db3ac2af139…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/listmodels.json` (3462 bytes, sha256 `227116c211a54530…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/tool-surface.txt` (4458 bytes, sha256 `d6e60a7ee502666f…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/version.json` (1856 bytes, sha256 `2a915d2504721702…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/linux-20261023/agy-followup.json` (5265 bytes, sha256 `6ee30e72c9976860…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/linux-20261023/agy-initial.json` (8316 bytes, sha256 `dd2c3c06859b6626…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/linux-20261023/capture-smoke.json` (1734 bytes, sha256 `e5167b74ac91c35c…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/linux-20261023/claude-granted-followup.json` (9091 bytes, sha256 `b0495fe103b86008…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/linux-20261023/claude-granted-initial.json` (16061 bytes, sha256 `3e04776cce93a10f…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/linux-20261023/claude-initial.json` (8434 bytes, sha256 `d33fb2b961ce367f…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/linux-20261023/clink-tool-declaration.txt` (2814 bytes, sha256 `dab86b9e2be01830…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/linux-20261023/discovery.json` (3468 bytes, sha256 `9278b9fe54250b1b…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/linux-20261023/empty-api-discovery-fixed.json` (2781 bytes, sha256 `5ad954d88cf87798…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/linux-20261023/empty-api-discovery.json` (2706 bytes, sha256 `5c69efcf7a90d8fe…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/linux-20261023/pal-discovery.patch` (6287 bytes, sha256 `b8de8e14faea5b87…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/linux-20261023/pal-fix-validation.json` (3226 bytes, sha256 `da320029c7b50666…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/linux-20261023/upstream-tests.json` (1322 bytes, sha256 `5c4241cdeed5992f…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/linux-20261023/version.json` (1871 bytes, sha256 `4c8ddfa51aaacb0c…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/fixtures/codex-criteria.md` (1010 bytes, sha256 `3f96330fd885fd46…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/fixtures/snapshots/candidate.txt` (87 bytes, sha256 `01d4113a3d367373…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/fixtures/criteria/review.md` (962 bytes, sha256 `9c3f4ef361243366…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/fixtures/project/caller.txt` (43 bytes, sha256 `9f175f0e8a632e01…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/fixtures/project/contract.md` (302 bytes, sha256 `30cfef2c117e07e2…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/fixtures/project/design.md` (332 bytes, sha256 `74bfca12737fc470…`)
- `payload/docs/feat/wip/clink-isolated-reviews/verification/fixtures/project/retry.txt` (116 bytes, sha256 `60243b157b16c5c6…`)

**Task 3 raw outputs** (eval actor outputs, grader verdicts, Codex event logs and
driver, live clink responses) were never in Git; they live in
`.local-archives/feature-evidence/clink-isolated-reviews-task3-20261024/` with
`inventory.sha256`.

**Limits and maintainer actions.** The captures remain in the branch's history;
only a squash merge or a history filter keeps them out of `master` (the
2026-10-20 batch used the prepared filter-repo procedure). Registering this
archive in `archives.json`, uploading it as a release asset and running the
filter are maintainer actions, as for the earlier batch. The PAL fix evidence
(`pal-discovery.patch`, `pal-fix-validation.json`) is also reproducible from PAL
commit `c73dab7d8cf9d791961b84614a0e082b74ee5569`, whose diff from
`d25c2d029a5d157935aa9bb836c18e9725969b8f` is the retained patch.
