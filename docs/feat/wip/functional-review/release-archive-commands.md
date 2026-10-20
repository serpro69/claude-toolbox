# Maintainer archive commands

These commands are guidance for the human-owned portion of Task 13.7. They have
not been executed by the preparation session. The retained tools have offline
tests; upload/download syntax was checked against installed `gh` help.

**Resolve [the source-input audit](archive-source-audit.md) before packaging.**
The old host's missing inputs cannot be replaced by current files with different
hashes. Choose the actual release containing this feature, commit retained tooling
and records, and use a fresh absolute output directory outside the checkout.
Use Bash and Python 3.11+; retain the same shell variables across the blocks.

## Assemble outside Git

Fill in `TAG` and `OUT`. This block intentionally stops when they are empty.

```bash
set -euo pipefail
REPO=$(git rev-parse --show-toplevel)
TREE=docs/feat/wip/functional-review/verification
TAG=''
OUT=''
: "${TAG:?Set the actual release tag}"
: "${OUT:?Set a fresh absolute directory outside the repository}"
case "$OUT" in
  /*) ;;
  *) printf 'OUT must be absolute\n' >&2; exit 1 ;;
esac
mkdir "$OUT"
OUT=$(cd "$OUT" && pwd -P)
case "$OUT/" in
  "$REPO/"*) printf 'OUT must be outside the checkout\n' >&2; exit 1 ;;
esac
BASE="functional-review-evidence-${TAG//\//-}"
STAGE="$OUT/payload"
mkdir -p "$STAGE/$(dirname "$TREE")" "$STAGE/original-inputs"
cp -a "$REPO/$TREE" "$STAGE/$TREE"
git -C "$REPO" archive 581dd0e11455398cb73e3d6ae5542854c016fe7f \
  klaude-plugin kodex-plugin .codex/agents \
  > "$STAGE/original-inputs/core-candidate-source.tar"
printf '%s  %s\n' \
  c7e56b46c89b28f6ae0c9cca42e4997e2e8acd7a238709de1489de957b032765 \
  "$STAGE/original-inputs/core-candidate-source.tar" | sha256sum -c -
```

Add verified early source inputs beneath `payload/original-inputs/`, with their
original revision/path/hash mapping. Check every original source-manifest entry.
Include this feature's compact records and recovery disposition in the payload
if useful for interpretation. **Stop here until that recovery is complete or
the maintainer has explicitly recorded a preservation exception.**

If the feature has moved to `done/`, set `TREE` to its real location before
assembly and preserve that member path in the retained summary.

## Package, upload and retrieve

After source completeness is resolved, run:

```bash
python3 -B "$REPO/scripts/functional-review-evals/inventory.py" create \
  "$STAGE" "$OUT/$BASE.manifest.json" --prefix payload \
  --revision "$(git -C "$REPO" rev-parse HEAD)"
tar --exclude='*/__pycache__' -C "$OUT" -czf "$OUT/$BASE.tar.gz" payload
(
  cd "$OUT"
  sha256sum "$BASE.tar.gz" "$BASE.manifest.json" > "$BASE.sha256"
)
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

No overwrite flags are used: an existing asset/destination requires inspection.
The inventory is built before packaging, then checked against the actual
downloaded copy. Locate representative successful/failed captures, corrected
grades, original contracts, actor inputs and recovered source members there.
Record the release URL, all asset names, archive checksum and member prefix
`payload/` in `verification-summary.md`.

## Cleanup remains a separate human action

Only after retrieval/integrity and source completeness are confirmed: repair
retained references, remove the archived tree, and choose the refs and historical
paths for history cleanup. Check feature docs and `docs/reviews/` references;
preserve original evidence identities and any old-to-new commit map. Reflog
expiry and garbage collection require the maintainer's selected scope; no generic
destructive command is supplied here. Recheck release accessibility after ref/tag
changes. Record observed completion before closing 13.7 or moving the feature.
