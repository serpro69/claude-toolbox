#!/usr/bin/env bash

set -e

# Parse flags
SKIP_CAPY="${SKIP_CAPY:-0}"
for arg in "$@"; do
  case "$arg" in
  --no-capy) SKIP_CAPY=1 ;;
  esac
done

cleanup() {
  rm -f "$0"
  git add "$0" || true
  git add .capy || true
  git add .codex || true
  git add .mcp.json || true
  git add CLAUDE.md
  git commit -m "Initialize claude-code"
}

trap cleanup EXIT

# Append @import reference for extra instructions (synced from upstream template)
if ! grep -q '@.claude/CLAUDE.extra.md' CLAUDE.md 2>/dev/null; then
  printf '\n# Extra Instructions\n' >>CLAUDE.md
  printf '@.claude/CLAUDE.extra.md\n' >>CLAUDE.md
fi

# Portable in-place sed: GNU sed uses `-i`, BSD/macOS sed needs `-i ''`
sed_inplace() {
  if sed --version >/dev/null 2>&1; then
    sed -i "$@"
  else
    sed -i '' "$@"
  fi
}

# Append @import reference for toolbox-specific claude instructions (synced from upstream template),
# next to the CLAUDE.extra.md import when it exists
if ! grep -q '@.claude/toolbox/CLAUDE.md' CLAUDE.md 2>/dev/null; then
  if grep -q '^@\.claude/CLAUDE\.extra\.md$' CLAUDE.md 2>/dev/null; then
    sed_inplace '/^@\.claude\/CLAUDE\.extra\.md$/a\
@.claude/toolbox/CLAUDE.md' CLAUDE.md
  else
    printf '\n@.claude/toolbox/CLAUDE.md\n' >>CLAUDE.md
  fi
fi

# Install the kk plugin from the claude-toolbox marketplace
claude plugin install kk@claude-toolbox

# Set up capy knowledge base (optional)
if [ "$SKIP_CAPY" = "1" ]; then
  : # skip silently
elif command -v capy >/dev/null 2>&1; then
  capy setup --local
else
  printf "⚠ capy not found on PATH — skipping knowledge base setup. Install: https://github.com/serpro69/capy\n" >&2
fi

printf "\n"
printf "Done initializing claude-code; committing CLAUDE.md file to git and cleaning up bootstrap script...\n"
printf "Your repo is now ready for AI-driven development workflows... Have fun!\n"
