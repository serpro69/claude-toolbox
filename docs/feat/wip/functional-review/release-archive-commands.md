# Maintainer archive commands

These commands describe Task 13.7's local archive preparation and later
maintainer release upload. Actual execution is recorded in the handoff; command
examples alone are not completion evidence. The retained tools have offline tests.

**The [temporary-input limitation](archive-source-audit.md) is accepted.**
Archive the retained material and available core source export; recovery of
missing scratch inputs is not required. No release or tag is needed to prepare
and verify the archive. Save it under the project's ignored `.local-archives/`
directory; it must never be staged or committed. Release upload follows cleanup.
Use Bash and Python 3.11+; retain the same shell variables across the blocks.

## Assemble outside Git

Use a fresh date/revision-based directory and filename:

```bash
set -euo pipefail
REPO=$(git rev-parse --show-toplevel)
TREE=docs/feat/wip/functional-review/verification
RUN="$(date -u +%Y%m%dT%H%M%SZ)-$(git rev-parse --short HEAD)"
BASE="functional-review-evidence-$RUN"
git -C "$REPO" check-ignore -q .local-archives/functional-review/probe
mkdir -p "$REPO/.local-archives/functional-review"
OUT="$REPO/.local-archives/functional-review/$RUN"
mkdir "$OUT"
STAGE="$OUT/payload"
mkdir -p "$STAGE/$(dirname "$TREE")" "$STAGE/original-inputs"
cp -a "$REPO/$TREE" "$STAGE/$TREE"
cp "$REPO/$(dirname "$TREE")/"*.md "$STAGE/$(dirname "$TREE")/"
cp -a "$REPO/$(dirname "$TREE")/reviews" "$STAGE/$(dirname "$TREE")/"
git -C "$REPO" diff HEAD --binary -- docs/feat/wip/functional-review \
  scripts/functional-review-evals/README.md \
  > "$STAGE/original-inputs/preparation.patch"
git -C "$REPO" archive 581dd0e11455398cb73e3d6ae5542854c016fe7f \
  klaude-plugin kodex-plugin .codex/agents \
  > "$STAGE/original-inputs/core-candidate-source.tar"
printf '%s  %s\n' \
  c7e56b46c89b28f6ae0c9cca42e4997e2e8acd7a238709de1489de957b032765 \
  "$STAGE/original-inputs/core-candidate-source.tar" | sha256sum -c -
```

The staged feature documents include the compact records, source audit and
accepted limitation. Keep the unavailable inputs' original identities and hashes;
do not substitute current files or claim exact replay of those older runs.
Proceed with the retained material after the core export checksum passes.

If the feature has moved to `done/`, set `TREE` to its real location before
assembly and preserve that member path in the retained summary.

## Package and verify locally

After assembly, run:

```bash
python3 -B "$REPO/scripts/functional-review-evals/inventory.py" create \
  "$STAGE" "$OUT/$BASE.manifest.json" --prefix payload \
  --revision "$(git -C "$REPO" rev-parse HEAD)"
tar --exclude='*/__pycache__' -C "$OUT" -czf "$OUT/$BASE.tar.gz" payload
(
  cd "$OUT"
  sha256sum "$BASE.tar.gz" "$BASE.manifest.json" > "$BASE.sha256"
)
(
  cd "$OUT"
  sha256sum -c "$BASE.sha256"
  mkdir extracted
  tar --no-same-owner -xzf "$BASE.tar.gz" -C extracted
)
python3 -B "$REPO/scripts/functional-review-evals/inventory.py" verify \
  "$OUT/extracted/payload" "$OUT/$BASE.manifest.json"
```

The inventory is built before packaging and checked against an extraction of the
actual compressed archive. Locate representative successful/failed captures,
corrected grades, original contracts and available source inputs there. Record
the local paths, archive checksum and member prefix `payload/` in the summary.
That verified local copy satisfies the archive prerequisite for cleanup.

## Cleanup remains a separate human action

Only after local checksum/member verification is confirmed: repair
retained references, remove the archived tree, and choose the refs and historical
paths for history cleanup. Check feature docs and `docs/reviews/` references;
preserve original evidence identities and any old-to-new commit map. Reflog
expiry and garbage collection require the maintainer's selected scope; no generic
destructive command is supplied here. Preserve `.local-archives/` through cleanup:
ignored files are not carried into a fresh clone and can be removed by an ignored-
file cleanup. Keep this local copy available until release upload is verified.

## Upload after cleanup and release creation

Once the release exists, use its actual tag. Reuse the verified filenames; no
renaming to include a tag is needed. This is later work, not a cleanup gate.

```bash
TAG=''
: "${TAG:?Set the tag of the now-created release}"
gh release upload "$TAG" --repo serpro69/claude-toolbox \
  "$OUT/$BASE.tar.gz" "$OUT/$BASE.manifest.json" "$OUT/$BASE.sha256"
RETRIEVED="$OUT/retrieved"
mkdir "$RETRIEVED"
gh release download "$TAG" --repo serpro69/claude-toolbox \
  --dir "$RETRIEVED" --pattern "$BASE.tar.gz" \
  --pattern "$BASE.manifest.json" --pattern "$BASE.sha256"
cmp "$OUT/$BASE.sha256" "$RETRIEVED/$BASE.sha256"
(
  cd "$RETRIEVED"
  sha256sum -c "$BASE.sha256"
  mkdir extracted
  tar --no-same-owner -xzf "$BASE.tar.gz" -C extracted
)
python3 -B "$REPO/scripts/functional-review-evals/inventory.py" verify \
  "$RETRIEVED/extracted/payload" "$RETRIEVED/$BASE.manifest.json"
```

Record the actual release URL/assets and download verification separately.
Close 13.7 only after its local verification, human cleanup and later release
attachment are observed; no proposed command sequence counts as completion.
