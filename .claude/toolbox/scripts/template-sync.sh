#!/usr/bin/env bash
#
# template-sync.sh - Synchronize configuration from upstream claude-toolbox template
#
# This script fetches template updates from the upstream repository and applies
# project-specific substitutions using values stored in the state manifest.
#
# USAGE:
#   ./template-sync.sh                      # Sync to latest release
#   ./template-sync.sh --version v1.2.0     # Sync to specific version
#   ./template-sync.sh --dry-run            # Preview what would change
#   ./template-sync.sh --ci                 # CI mode for GitHub Actions
#   ./template-sync.sh --local                         # Fetch, compare, and apply locally
#   ./template-sync.sh --apply --output-dir ./staging  # Apply staged changes (CI)
#
# OPTIONS:
#   --version VERSION     Target version to sync (default: latest)
#                         - "latest": Most recent tagged release
#                         - "main": Latest from main branch
#                         - "v1.2.3": Specific tag
#   --dry-run             Preview changes without applying them
#   --local               Fetch, compare, and apply in a single invocation
#   --apply               Apply pre-staged changes to the working tree (used by CI)
#   --ci                  CI mode for GitHub Actions (structured output)
#   --output-dir DIR      Directory for staged changes (default: temp)
#   -h, --help            Show this help message
#
# ENVIRONMENT:
#   TEMPLATE_SYNC_NO_HANDOFF=1
#                         Disable the self-update handoff. By default, when the
#                         target version ships a different template-sync.sh,
#                         this script exec()s that copy so the version matching
#                         the templates drives the whole run (migrations
#                         included) in one invocation. Set this to run the
#                         local script as-is, e.g. while developing it.
#
# REQUIRES:
#   - jq (for JSON parsing)
#   - git
#   - curl
#   - yq (mikefarah/yq)
#   - python3 (standard library only)
#
# EXIT CODES:
#   0 - Success (with or without changes)
#   1 - Operational error (missing manifest, network failure, invalid JSON)
#   2 - Invalid CLI arguments
#
# TROUBLESHOOTING:
#   "Manifest not found":
#     - Ensure .github/template-state.json exists
#     - For repos created before sync feature, create manifest manually (see README)
#
#   "Version not found":
#     - Check available tags: git ls-remote --tags https://github.com/serpro69/claude-toolbox
#     - Use 'latest' for most recent release or 'main' for bleeding edge
#
#   "Network error":
#     - Verify internet connectivity
#     - Check if upstream repo is accessible
#     - Script will retry 3 times with 5s delay
#
#   "Invalid JSON in manifest":
#     - Check manifest file for syntax errors
#     - Restore from version control if corrupted

set -euo pipefail

# Source semver comparison (provides compare() function).
# Bootstrap: downstream repos may not have this file yet if they haven't synced
# since it was introduced — fetch from upstream so the script stays self-contained.
load_semver() {
  local helper
  helper="$(dirname "${BASH_SOURCE[0]}")/semver-compare.sh"
  if [[ ! -f "$helper" ]]; then
    curl -fsSL "https://raw.githubusercontent.com/serpro69/claude-toolbox/master/.claude/toolbox/scripts/semver-compare.sh" \
      -o "$helper" 2>/dev/null || { echo "Failed to fetch semver-compare.sh" >&2; exit 1; }
  fi
  # shellcheck source=semver-compare.sh
  source "$helper"
}
if [[ ${BASH_SOURCE[0]} != "$0" ]]; then
  load_semver
fi

# =============================================================================
# Global Configuration
# =============================================================================

MANIFEST_PATH=".github/template-state.json"
STAGING_DIR=""
DRY_RUN=false
CI_MODE=false
TARGET_VERSION="latest"
FETCHED_TEMPLATES_PATH=""
SUBSTITUTED_TEMPLATES_PATH=""

# Temp directory for cleanup tracking (set when using auto-generated staging dir)
TEMP_DIR=""

# File change tracking arrays
ADDED_FILES=()
MODIFIED_FILES=()
DELETED_FILES=()
UNCHANGED_FILES=()
DROPPED_DENY_ENTRIES=()
# Three-way settings merge: upstream settings.json at the last synced version
# (empty when unavailable) and what the merge removed or kept against upstream
SETTINGS_BASE_FILE=""
SETTINGS_BASE_WARNING=""
CODEX_BASE_DIR=""
SETTINGS_REMOVED_ENTRIES=()
SETTINGS_CONFLICT_ENTRIES=()

# Exclusion tracking arrays
EXCLUDED_FILES=()
SYNC_EXCLUSIONS=()

# Built-in exclusions: files that fetch_upstream_templates strips from staging
# because they're per-repo and must never be synced downstream. These patterns
# must also be honored during deletion detection — otherwise compare_files sees
# the file in the project but not in staging and incorrectly flags it as deleted.
# Keep this list in sync with the strip logic in fetch_upstream_templates().
BUILTIN_EXCLUSIONS=(
  ".claude/settings.local.json"
  ".claude/kk-guard.json"
  ".claude/capy/*"
  ".claude/scripts/capy.sh"
  ".codex/scripts/capy.sh"
  ".codex/capy-owner"
)

# Resolved version (for reporting)
RESOLVED_VERSION=""

# Plugin migration tracking
PLUGIN_MIGRATED=false

# Apply mode: when true, migration functions perform filesystem mutations.
# When false (default), they only populate tracking arrays for reporting.
APPLY_MODE=false

# Local mode: fetch + compare + apply in a single invocation
LOCAL_MODE=false
RETIRE_MODE=false

# Entry-point flag: true only when this file is the process' main script (set
# by the guard at the bottom of the file), false when sourced — e.g. by the
# test suite. handoff_to_upstream_script() exec()s over the current process,
# which is only safe in the former case.
IS_ENTRYPOINT=false

# =============================================================================
# Color Output
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# =============================================================================
# Logging Functions
# =============================================================================

log_info() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_success() {
  echo -e "${GREEN}✓${NC} $1"
}

log_step() {
  echo -e "${CYAN}>>>${NC} $1"
}

# =============================================================================
# Cleanup Functions
# =============================================================================

# Cleanup handler that preserves exit code
# Called on EXIT, INT, TERM signals
cleanup_on_exit() {
  local exit_code=$?

  # Only clean up if TEMP_DIR is set and exists
  if [[ -n "${TEMP_DIR:-}" && -d "$TEMP_DIR" ]]; then
    rm -rf "$TEMP_DIR"
    if ! $CI_MODE; then
      log_info "Cleaned up temporary directory"
    fi
  fi

  # Temp dir inherited from a parent process that exec()'d this script (see
  # handoff_to_upstream_script). exec() skips the parent's EXIT trap, so the
  # parent delegates its cleanup to us. Guarded by the mktemp naming pattern so
  # a stray value in the environment can never point us at an arbitrary path.
  local handoff_dir="${TEMPLATE_SYNC_HANDOFF_CLEANUP:-}"
  if [[ -n "$handoff_dir" && -d "$handoff_dir" ]]; then
    case "$handoff_dir" in
    */template-sync.*)
      rm -rf "$handoff_dir"
      ;;
    esac
  fi

  exit $exit_code
}

# =============================================================================
# Helper Functions
# =============================================================================

# is_excluded()
# Checks if a file path matches any exclusion pattern.
#
# Args:
#   $1 - Project-relative file path (e.g., ".claude/commands/chain-of-verification/default.md")
#
# Returns:
#   0 if path matches an exclusion pattern (excluded)
#   1 if path does not match any pattern (not excluded)
#
# Note: Uses bash case statement glob matching where * matches any characters including /
is_excluded() {
  local path="$1"
  local pattern
  # A symlink in the destination is adopter-owned. In particular a linked
  # config directory must never redirect migration writes outside the repo.
  if $RETIRE_MODE || [[ ${TEMPLATE_SYNC_MERGE_DENY:-0} == 1 ]]; then
    local entry=$path
    while [[ -n $entry && $entry != / ]]; do
      [[ ! -L $entry ]] || return 0
      [[ $entry == */* ]] || break
      entry=${entry%/*}
    done
  fi

  # Check built-in exclusions first (per-repo files stripped from staging)
  for pattern in "${BUILTIN_EXCLUSIONS[@]}"; do
    # IMPORTANT: pattern must be unquoted for glob expansion in case
    case "$path" in
    $pattern)
      return 0 # Excluded
      ;;
    esac
  done

  # Check user-configured exclusions from manifest
  for pattern in "${SYNC_EXCLUSIONS[@]}"; do
    if $RETIRE_MODE || [[ ${TEMPLATE_SYNC_MERGE_DENY:-0} == 1 ]]; then
      pattern=${pattern%/}
      # A directory excluded from retirement also protects its children.
      case "$path" in $pattern/*) return 0 ;; esac
    fi
    case "$path" in
    $pattern)
      return 0 # Excluded
      ;;
    esac
  done

  return 1 # Not excluded
}

# Older migrations operate on whole directories. During migration sync, keep
# a tree intact if moving or deleting it would also move an excluded child.
migration_excluded() {
  [[ ${TEMPLATE_SYNC_MERGE_DENY:-0} == 1 ]] || return 1
  local entry destination
  if is_excluded "$1"; then log_info "Excluded: $1"; return 0; fi
  if [[ -n ${2:-} ]] && is_excluded "$2"; then log_info "Excluded: $2"; return 0; fi
  if [[ -d $1 && ! -L $1 ]]; then
    while IFS= read -r -d '' entry; do
      if is_excluded "$entry"; then log_info "Keep $1 (excluded: $entry)"; return 0; fi
      if [[ -n ${2:-} ]]; then
        destination="$2/${entry#"$1/"}"
        if is_excluded "$destination"; then log_info "Keep $1 (excluded: $destination)"; return 0; fi
      fi
    done < <(find "$1" -mindepth 1 -print0)
  fi
  return 1
}

# sed_inplace()
# Portable in-place sed: GNU sed uses `-i`, BSD/macOS sed needs `-i ''`.
#
# Args:
#   $@ - sed script(s) and target file(s), as accepted by sed
#
# Note: scripts passed here must stick to POSIX sed syntax — e.g. `a\` followed
# by a literal newline, not GNU's one-line `a text` form — so both dialects work.
sed_inplace() {
  if sed --version >/dev/null 2>&1; then
    sed -i "$@"
  else
    sed -i '' "$@"
  fi
}

# =============================================================================
# Dependency Check
# =============================================================================

check_dependencies() {
  local missing=()

  if ! command -v jq &>/dev/null; then
    missing+=("jq")
  fi

  if ! command -v git &>/dev/null; then
    missing+=("git")
  fi

  # curl and yq are only needed for fetch/substitute, not apply mode
  if ! $APPLY_MODE; then
    if ! command -v curl &>/dev/null; then
      missing+=("curl")
    fi

    if ! command -v yq &>/dev/null; then
      missing+=("yq")
    fi

    if ! command -v python3 &>/dev/null; then
      missing+=("python3")
    fi
  fi

  if [[ ${#missing[@]} -gt 0 ]]; then
    log_error "Missing required dependencies: ${missing[*]}"
    echo "Please install the missing dependencies:"
    echo "  macOS:  brew install ${missing[*]}"
    echo "  Linux:  apt-get install ${missing[*]}"
    exit 1
  fi
}

# json_update()
# Atomically updates a JSON file using a jq expression.
# Writes to a temp file first, then moves into place on success.
#
# Args:
#   $1 - Target file path
#   $2 - jq filter expression
#   $@ - Additional arguments forwarded to jq (e.g., --arg key val)
#
# Returns:
#   0 on success, 1 on jq failure (target file unchanged)
json_update() {
  local file="$1" expr="$2"
  shift 2
  local tmp
  tmp=$(mktemp "/tmp/json-update.XXXXXX")
  if jq "$@" "$expr" "$file" >"$tmp"; then
    mv "$tmp" "$file"
    return 0
  else
    rm -f "$tmp"
    return 1
  fi
}

# =============================================================================
# Manifest Functions
# =============================================================================

# get_manifest_value()
# Extracts a value from the manifest file using a jq expression.
#
# Args:
#   $1 - jq expression to evaluate (e.g., '.variables.PROJECT_NAME')
#
# Returns:
#   Extracted value via stdout, or empty string if not found
#
# Example:
#   project_name=$(get_manifest_value '.variables.PROJECT_NAME')
get_manifest_value() {
  local jq_expr="$1"
  jq -r "$jq_expr" "$MANIFEST_PATH"
}

# read_manifest()
# Reads and validates the manifest file exists and contains valid JSON.
# Verifies required top-level fields (schema_version, upstream_repo, template_version, variables).
#
# Returns:
#   0 on success (manifest loaded)
#   Exits with 1 if manifest missing, invalid JSON, or missing required fields
#
# Side effects:
#   Logs info/error messages
read_manifest() {
  # Check if manifest file exists
  if [[ ! -f "$MANIFEST_PATH" ]]; then
    log_error "Manifest file not found: $MANIFEST_PATH"
    log_error ""
    log_error "This repository doesn't have a template state manifest."
    log_error "Possible reasons:"
    log_error "  - The repository was created before the sync feature was available"
    log_error "  - The cleanup script was run with an older version"
    log_error "  - The manifest file was accidentally deleted"
    log_error ""
    log_error "To create a manifest manually, see the template documentation."
    exit 1
  fi

  # Validate JSON syntax
  if ! jq -e '.' "$MANIFEST_PATH" &>/dev/null; then
    log_error "Invalid JSON in manifest file: $MANIFEST_PATH"
    log_error "The manifest file is not valid JSON. It may be corrupted."
    log_error "Please check the file for syntax errors or restore it from version control."
    exit 1
  fi

  # Verify required top-level fields exist
  local required_fields=("schema_version" "upstream_repo" "template_version" "variables")
  for field in "${required_fields[@]}"; do
    if [[ "$(get_manifest_value ".$field // empty")" == "" ]]; then
      log_error "Missing required field in manifest: $field"
      log_error "The manifest file may be incomplete or corrupted."
      exit 1
    fi
  done

  log_info "Manifest loaded: $MANIFEST_PATH"

  # Load sync exclusions if present (optional field)
  if jq -e '.sync_exclusions' "$MANIFEST_PATH" &>/dev/null; then
    mapfile -t SYNC_EXCLUSIONS < <(jq -r '.sync_exclusions[]' "$MANIFEST_PATH")
    if [[ ${#SYNC_EXCLUSIONS[@]} -gt 0 ]]; then
      log_info "Loaded ${#SYNC_EXCLUSIONS[@]} sync exclusion pattern(s)"
    fi
  fi
}

# validate_manifest()
# Validates manifest schema version and all required variables.
# Checks schema_version is supported (currently: "1") and validates
# upstream_repo format and required variable presence.
#
# Returns:
#   0 on success (manifest valid)
#   Exits with 1 if validation fails
#
# Side effects:
#   Logs success/error messages
validate_manifest() {
  # Check schema version
  local schema_version
  schema_version=$(get_manifest_value '.schema_version // empty')

  if [[ -z "$schema_version" ]]; then
    log_error "Invalid manifest: missing schema_version"
    log_error "The manifest file may be corrupted or from an incompatible version."
    exit 1
  fi

  if [[ "$schema_version" != "1" ]]; then
    log_error "Manifest schema version $schema_version is not supported"
    log_error "This sync script supports schema version 1."
    log_error "Please update the template-sync script or migrate your manifest."
    exit 1
  fi

  # Validate upstream_repo format (owner/repo)
  local upstream_repo
  upstream_repo=$(get_manifest_value '.upstream_repo')
  if [[ ! "$upstream_repo" =~ ^[^/]+/[^/]+$ ]]; then
    log_error "Invalid upstream_repo format: $upstream_repo (expected: owner/repo)"
    exit 1
  fi

  # Verify all required variables exist (can be empty but must be present)
  local required_vars=("PROJECT_NAME" "LANGUAGES" "CC_MODEL")
  for var in "${required_vars[@]}"; do
    if [[ "$(get_manifest_value ".variables.$var // \"__MISSING__\"")" == "__MISSING__" ]]; then
      log_error "Missing required variable in manifest: $var"
      exit 1
    fi
  done

  # Validate LANGUAGES is not empty
  local languages
  languages=$(get_manifest_value '.variables.LANGUAGES')
  if [[ -z "$languages" ]]; then
    log_error "LANGUAGES variable cannot be empty in manifest"
    exit 1
  fi

  # Validate sync_exclusions if present (optional field)
  if jq -e '.sync_exclusions' "$MANIFEST_PATH" &>/dev/null; then
    # Must be an array
    if ! jq -e '.sync_exclusions | type == "array"' "$MANIFEST_PATH" &>/dev/null; then
      log_error "sync_exclusions must be an array"
      exit 1
    fi
    # All elements must be strings
    if ! jq -e '.sync_exclusions | all(type == "string")' "$MANIFEST_PATH" &>/dev/null; then
      log_error "All sync_exclusions elements must be strings"
      exit 1
    fi
  fi

  log_success "Manifest validation passed"
}

# migrate_manifest()
# Migrates the manifest's upstream_repo from the old repository name
# (serpro69/claude-starter-kit) to the new name (serpro69/claude-toolbox).
# This ensures existing users' manifests are updated on their next sync.
#
# Returns:
#   0 on success (migration applied or not needed)
#   Exits with 1 if manifest rewrite fails
#
# Side effects:
#   Rewrites MANIFEST_PATH in-place if migration needed
#   Reloads manifest via read_manifest() after rewrite
#   Logs info message when migration is triggered
migrate_manifest() {
  local upstream_repo
  upstream_repo=$(get_manifest_value '.upstream_repo')

  if [[ "$upstream_repo" == "serpro69/claude-starter-kit" ]]; then
    log_info "Migrating upstream_repo from serpro69/claude-starter-kit to serpro69/claude-toolbox"
    if ! json_update "$MANIFEST_PATH" '.upstream_repo = "serpro69/claude-toolbox"'; then
      log_error "Failed to migrate manifest"
      exit 1
    fi
    read_manifest
  fi
}

# backfill_manifest_variables()
# Adds missing optional variables to the manifest with their default values.
# This ensures the manifest is always explicit about what values are being used,
# even for variables that were introduced after the downstream repo was created.
#
# Returns:
#   0 on success
#
# Side effects:
#   Rewrites MANIFEST_PATH in-place if any variables are added
#   Reloads manifest via read_manifest() after rewrite
#   Logs info message listing backfilled variables
backfill_manifest_variables() {
  local defaults=(
    "CC_STATUSLINE:enhanced"
    "CC_EFFORT_LEVEL:high"
    "CC_PERMISSION_MODE:default"
    "CODEX_MODEL:gpt-6.2-astra"
    "CODEX_APPROVAL_POLICY:on-request"
    "SKIP_CAPY:false"
  )

  local needs_update=false
  local backfilled=()

  for entry in "${defaults[@]}"; do
    local var="${entry%%:*}"
    local default_val="${entry#*:}"
    if [[ "$(get_manifest_value ".variables.$var // \"__MISSING__\"")" == "__MISSING__" ]]; then
      needs_update=true
      backfilled+=("$var=$default_val")
    fi
  done

  if $needs_update; then
    local jq_expr='.'
    for entry in "${defaults[@]}"; do
      local var="${entry%%:*}"
      local default_val="${entry#*:}"
      if [[ "$(get_manifest_value ".variables.$var // \"__MISSING__\"")" == "__MISSING__" ]]; then
        jq_expr="$jq_expr | .variables.$var = \"$default_val\""
      fi
    done
    if ! json_update "$MANIFEST_PATH" "$jq_expr"; then
      log_warn "Failed to backfill manifest variables"
      return 0
    fi
    log_info "Backfilled missing manifest variables: ${backfilled[*]}"
    read_manifest
  fi
}

# =============================================================================
# Plugin Migration Functions
# =============================================================================

# needs_plugin_migration()
# Checks whether the downstream repo needs to migrate from template-managed
# skills/commands/hooks to the kk plugin system.
#
# Args:
#   $1 - Path to fetched upstream directory (parent of klaude-plugin/)
#
# Returns:
#   0 if migration is needed
#   1 if migration is not needed (already migrated or upstream has no plugin)
needs_plugin_migration() {
  local upstream_dir="$1"

  # Check if upstream has the plugin
  if [[ ! -f "$upstream_dir/klaude-plugin/.claude-plugin/plugin.json" ]]; then
    return 1
  fi

  # Check if already migrated
  if [[ -f "$MANIFEST_PATH" ]] && jq -e '.plugin_migrated == true' "$MANIFEST_PATH" &>/dev/null; then
    return 1
  fi

  return 0
}

# run_plugin_migration()
# Removes template-managed skills, commands, hooks, and validate-bash.sh
# from the downstream repo and updates settings.json for the plugin system.
#
# Side effects:
#   - Deletes known template-managed files from .claude/
#   - Updates .claude/settings.json: removes hooks, adds marketplace/plugin config
#   - Sets plugin_migrated=true in template-state.json
#   - Appends removed files to DELETED_FILES array
#   - Logs all actions
run_plugin_migration() {
  log_step "Migrating to kk plugin system"

  local upstream_repo
  upstream_repo=$(get_manifest_value '.upstream_repo')

  # Static list of known template-managed files to remove.
  # These are the pre-plugin skill/command names that were installed by
  # template-sync before v0.5.0. Downstream projects upgrading from pre-plugin
  # versions need these paths cleaned up so the plugin can take over.
  # Do NOT rename these to post-plugin skill names — historical names only.
  local dirs_to_remove=(
    ".claude/skills/analysis-process"
    ".claude/skills/cove"
    ".claude/skills/development-guidelines"
    ".claude/skills/documentation-process"
    ".claude/skills/implementation-process"
    ".claude/skills/implementation-review"
    ".claude/skills/merge-docs"
    ".claude/skills/solid-code-review"
    ".claude/skills/testing-process"
    ".claude/commands/cove"
    ".claude/commands/implementation-review"
    ".claude/commands/migrate-from-taskmaster"
    ".claude/commands/sync-workflow"
  )
  local files_to_remove=(
    ".claude/scripts/validate-bash.sh"
  )

  # Track and optionally remove directories
  for dir in "${dirs_to_remove[@]}"; do
    if migration_excluded "$dir"; then continue; fi
    if [[ -d "$dir" ]]; then
      DELETED_FILES+=("$dir/")
      if $APPLY_MODE; then
        rm -rf "$dir"
        log_info "Removed $dir/"
      else
        log_info "Would remove $dir/"
      fi
    fi
  done

  # Track and optionally remove individual files
  for file in "${files_to_remove[@]}"; do
    if migration_excluded "$file"; then continue; fi
    if [[ -f "$file" ]]; then
      DELETED_FILES+=("$file")
      if $APPLY_MODE; then
        rm -f "$file"
        log_info "Removed $file"
      else
        log_info "Would remove $file"
      fi
    fi
  done

  if $APPLY_MODE; then
    # Clean up empty parent directories
    rmdir .claude/skills 2>/dev/null || true
    rmdir .claude/commands 2>/dev/null || true

    # Update settings.json: remove hooks, add marketplace and plugin config
    local settings_file=".claude/settings.json"
    # Migration sync staged the individual legacy-handler update. Resetting
    # hooks and marketplaces here would discard adopter registrations.
    if [[ -f "$settings_file" && ${TEMPLATE_SYNC_MERGE_DENY:-0} != 1 ]]; then
      if json_update "$settings_file" \
        'del(.hooks) |
         .extraKnownMarketplaces = {
           "claude-toolbox": {
             "source": {
               "source": "github",
               "repo": $repo
             }
           }
         }' --arg repo "$upstream_repo"; then
        log_info "Updated $settings_file for plugin system"
      else
        log_warn "Failed to update $settings_file — manual update required"
      fi
    fi

    # Set plugin_migrated flag in manifest
    if json_update "$MANIFEST_PATH" '.plugin_migrated = true'; then
      log_info "Set plugin_migrated flag in manifest"
    else
      log_warn "Failed to update manifest — manual update required"
    fi
  fi

  log_success "Plugin migration complete"
}

# =============================================================================
# Serena Removal Migration
# =============================================================================

# needs_serena_removal()
# Checks whether the downstream repo still has Serena artifacts from the
# template defaults that should be cleaned up.
# Detection is based on the SERENA_INITIAL_PROMPT manifest variable — its
# presence means the repo was set up when Serena was a template default.
# If a user manually added .serena/ without the variable, we leave it alone.
#
# Returns:
#   0 if removal is needed
#   1 if not needed
needs_serena_removal() {
  if [[ -f "$MANIFEST_PATH" ]] && jq -e '.variables.SERENA_INITIAL_PROMPT' "$MANIFEST_PATH" &>/dev/null 2>&1; then
    return 0
  fi

  return 1
}

# run_serena_removal()
# Removes .serena/ directory and SERENA_INITIAL_PROMPT from the manifest.
# Serena MCP was dropped from upstream defaults — downstream repos no longer
# need the config directory or the manifest variable.
#
# Side effects:
#   - Deletes .serena/ directory if present
#   - Removes SERENA_INITIAL_PROMPT from manifest variables
#   - Appends removed files to DELETED_FILES array
run_serena_removal() {
  log_step "Removing Serena artifacts (no longer in upstream defaults)"

  # Respect sync_exclusions — if .serena/ is excluded, skip directory removal
  if is_excluded ".serena/project.yml" || migration_excluded ".serena"; then
    log_info "Skipping .serena/ removal (matched sync_exclusions)"
  else
    if [[ -d ".serena" ]]; then
      DELETED_FILES+=(".serena/")
      if $APPLY_MODE; then
        rm -rf ".serena"
        log_info "Removed .serena/"
      else
        log_info "Would remove .serena/"
      fi
    fi

    # Remove !.serena from .gitignore if present
    if [[ -f ".gitignore" ]] && ! migration_excluded .gitignore && grep -q '^!\.serena' .gitignore; then
      MODIFIED_FILES+=(".gitignore")
      if $APPLY_MODE; then
        sed_inplace '/^!\.serena$/d' .gitignore
        log_info "Removed !.serena from .gitignore"
      else
        log_info "Would remove !.serena from .gitignore"
      fi
    fi

    # Remove mcp__serena__* from settings.local.json permissions if present
    local local_settings=".claude/settings.local.json"
    if [[ -f "$local_settings" ]] && ! migration_excluded "$local_settings" && jq -e '.permissions.allow | any(startswith("mcp__serena__"))' "$local_settings" &>/dev/null 2>&1; then
      if $APPLY_MODE; then
        if json_update "$local_settings" '.permissions.allow |= map(select(startswith("mcp__serena__") | not))'; then
          MODIFIED_FILES+=("$local_settings")
          log_info "Removed mcp__serena__* from $local_settings permissions"
        fi
      else
        MODIFIED_FILES+=("$local_settings")
        log_info "Would remove mcp__serena__* from $local_settings permissions"
      fi
    fi
  fi

  # Clean manifest: remove SERENA_INITIAL_PROMPT variable and set flag
  if [[ -f "$MANIFEST_PATH" ]]; then
    if $APPLY_MODE; then
      if json_update "$MANIFEST_PATH" 'del(.variables.SERENA_INITIAL_PROMPT)'; then
        read_manifest
        log_info "Removed SERENA_INITIAL_PROMPT from manifest"
      else
        log_warn "Failed to update manifest — manual cleanup may be needed"
      fi
    else
      log_info "Would remove SERENA_INITIAL_PROMPT from manifest"
    fi
  fi

  log_success "Serena removal complete"
}

# =============================================================================
# Script Consolidation Migration
# =============================================================================

# needs_script_consolidation()
# Checks whether scripts still exist at pre-consolidation locations.
# Returns 0 if any old-location scripts are found.
needs_script_consolidation() {
  local old_paths=(
    ".github/scripts/template-sync.sh"
    ".github/scripts/semver-compare.sh"
    ".claude/scripts/statusline.sh"
    ".claude/scripts/statusline_enhanced.sh"
    ".claude/scripts/sync-workflow.sh"
    "docs/update.sh"
  )

  for path in "${old_paths[@]}"; do
    if [[ -f "$path" ]]; then
      return 0
    fi
  done

  return 1
}

# run_script_consolidation()
# Removes scripts from pre-consolidation locations. The new copies at
# .claude/toolbox/scripts/ arrive via the normal .claude/ directory sync.
#
# Side effects:
#   - Deletes old-location script files
#   - Removes empty parent directories
#   - Appends removed files to DELETED_FILES array
run_script_consolidation() {
  log_step "Consolidating scripts to .claude/toolbox/scripts/"

  local files_to_remove=(
    ".github/scripts/template-sync.sh"
    ".github/scripts/semver-compare.sh"
    ".claude/scripts/statusline.sh"
    ".claude/scripts/statusline_enhanced.sh"
    ".claude/scripts/sync-workflow.sh"
    "docs/update.sh"
  )

  for file in "${files_to_remove[@]}"; do
    if migration_excluded "$file"; then continue; fi
    if [[ -f "$file" ]]; then
      DELETED_FILES+=("$file")
      if $APPLY_MODE; then
        rm -f "$file"
        log_info "Removed $file"
      else
        log_info "Would remove $file"
      fi
    fi
  done

  log_success "Script consolidation complete"
}

# =============================================================================
# Feature-Docs Relocation Migration
# =============================================================================

# needs_docs_feat_migration()
# Checks whether the downstream repo still keeps feature docs at the legacy
# top-level locations (docs/wip, docs/done, docs/archive) that upstream moved
# under docs/feat/.
#
# Gating is pure state detection (same pattern as needs_script_consolidation):
# the migration's own effect — the legacy dirs no longer existing — is the
# idempotency guard, so no manifest flag is required.
#
# Returns 0 if any legacy dir is present, 1 otherwise.
needs_docs_feat_migration() {
  local dir
  for dir in docs/wip docs/done docs/archive; do
    if [[ -d "$dir" ]]; then
      return 0
    fi
  done

  return 1
}

# run_docs_feat_migration()
# Relocates feature-doc directories from their legacy top-level paths to the
# docs/feat/ namespace, matching the upstream layout:
#   docs/wip     -> docs/feat/wip
#   docs/done    -> docs/feat/done
#   docs/archive -> docs/feat/archive
#
# Deliberate limitations (fail loud, don't over-reach):
#   - Only moves directories. It does NOT sed-rewrite references inside
#     consumer files: relative links within the moved trees survive the move,
#     and a repo-wide rewrite risks corrupting unrelated content. Any hardcoded
#     "docs/wip/..." references in consumer prose are the consumer's to fix.
#   - Never clobbers an existing target — if docs/feat/<name> already exists it
#     warns and skips that pair. Because gating is state-based, an unresolved
#     collision keeps warning on every sync until a human merges it, rather
#     than being silently suppressed by a flag.
#   - Respects sync_exclusions: an excluded legacy dir is left in place.
#
# Side effects:
#   - Moves legacy dirs into docs/feat/ (APPLY_MODE only)
#   - Appends old paths to DELETED_FILES and new paths to ADDED_FILES
#   - Logs all actions
run_docs_feat_migration() {
  log_step "Relocating feature docs to docs/feat/"

  local pairs=(
    "docs/wip:docs/feat/wip"
    "docs/done:docs/feat/done"
    "docs/archive:docs/feat/archive"
  )

  local pair src dst
  for pair in "${pairs[@]}"; do
    src="${pair%%:*}"
    dst="${pair##*:}"

    [[ -d "$src" ]] || continue

    # Respect sync_exclusions — if the source tree is excluded, leave it alone
    if is_excluded "$src" || migration_excluded "$src" "$dst"; then
      log_info "Skipping $src/ relocation (matched sync_exclusions)"
      continue
    fi

    # Never clobber an existing target — fail loud, skip this pair
    if [[ -e "$dst" ]]; then
      log_warn "Cannot relocate $src/ — $dst/ already exists; merge manually"
      continue
    fi

    DELETED_FILES+=("$src/")
    ADDED_FILES+=("$dst/")
    if $APPLY_MODE; then
      mkdir -p "$(dirname "$dst")"
      mv "$src" "$dst"
      log_info "Moved $src/ -> $dst/"
    else
      log_info "Would move $src/ -> $dst/"
    fi
  done

  log_success "Feature docs relocation complete"
}

# =============================================================================
# Version Resolution and Template Fetching
# =============================================================================

# resolve_version()
# Resolves target version string to a concrete git ref or SHA.
#
# Args:
#   $1 - Target version ("latest", "main", "master", "HEAD", or specific tag/SHA)
#   $2 - Upstream repository (owner/repo format)
#
# Returns:
#   Resolved version string via stdout:
#   - For "latest": returns tag name (e.g., "v1.0.0") or SHA if no tags
#   - For "main"/"master"/"HEAD": returns actual commit SHA
#   - For specific tag/SHA: returns as-is
#   Exits with 1 if resolution fails
#
# Note: All logging goes to stderr to keep stdout clean for return value
resolve_version() {
  local target="$1"
  local upstream="$2"
  local resolved=""
  local repo_url="https://github.com/$upstream.git"

  case "$target" in
  latest)
    # Ordinary sync follows stable releases. An explicit tag selects a pilot.
    local tags
    tags=$(git ls-remote --tags "$repo_url" 2>/dev/null |
      { grep -v '\^{}' || true; } |
      sed 's/.*refs\/tags\///')

    local tag
    while IFS= read -r tag; do
      [[ -z "$tag" ]] && continue
      local stripped="${tag#v}"
      [[ "$stripped" =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(\+[0-9A-Za-z.-]+)?$ ]] || continue
      if [[ -z "$resolved" ]]; then
        resolved="$tag"
      else
        local resolved_stripped="${resolved#v}"
        if [[ "$(compare "$stripped" "$resolved_stripped")" == "gt" ]]; then
          resolved="$tag"
        fi
      fi
    done <<<"$tags"

    # If no tags exist, resolve default branch to SHA
    if [[ -z "$resolved" ]]; then
      if [[ -n "$tags" ]]; then
        log_error "No stable release tag found. Choose an explicit tag or branch with --version." >&2
        return 1
      fi
      log_warn "No tags found in upstream repository, using default branch" >&2
      resolved=$(git ls-remote "$repo_url" HEAD 2>/dev/null | cut -f1)
      if [[ -z "$resolved" ]]; then
        log_error "Failed to resolve default branch SHA for upstream" >&2
        exit 1
      fi
    fi
    ;;
  main | master)
    # Resolve branch name to actual commit SHA
    resolved=$(git ls-remote "$repo_url" "refs/heads/$target" 2>/dev/null | cut -f1)
    if [[ -z "$resolved" ]]; then
      log_error "Branch '$target' not found in upstream repository" >&2
      exit 1
    fi
    ;;
  HEAD)
    # Resolve HEAD (default branch) to actual commit SHA
    resolved=$(git ls-remote "$repo_url" HEAD 2>/dev/null | cut -f1)
    if [[ -z "$resolved" ]]; then
      log_error "Failed to resolve HEAD for upstream repository" >&2
      exit 1
    fi
    ;;
  *)
    # Assume specific tag or SHA - return as-is
    resolved="$target"
    ;;
  esac

  # Validate we got something
  if [[ -z "$resolved" ]]; then
    log_error "Failed to resolve version: $target"
    exit 1
  fi

  echo "$resolved"
}

# fetch_upstream_templates()
# Fetches templates from upstream repository using git sparse-checkout.
# Implements retry logic for network failures (3 attempts, 5s delay).
#
# Args:
#   $1 - Version to fetch (tag, branch, or SHA)
#   $2 - Upstream repository (owner/repo format)
#   $3 - Working directory for clone operation
#
# Returns:
#   0 on success
#   Exits with 1 if fetch fails after retries or templates not found
#
# Side effects:
#   Sets global FETCHED_TEMPLATES_PATH to the path of fetched templates
#   Creates directories in work_dir
#   Logs progress/error messages
fetch_upstream_templates() {
  local version="$1"
  local upstream="$2"
  local work_dir="$3"
  local repo_url="https://github.com/$upstream.git"

  # Retry configuration
  local max_retries=3
  local retry_delay=5
  local attempt

  log_step "Fetching templates from $upstream @ $version"

  # Create work directory
  mkdir -p "$work_dir"

  # Clone with blob filter for efficiency (with retry logic)
  for ((attempt = 1; attempt <= max_retries; attempt++)); do
    if git clone --depth 1 --filter=blob:none \
      "$repo_url" "$work_dir/upstream" --quiet 2>/dev/null; then
      break
    fi

    if ((attempt < max_retries)); then
      log_warn "Clone failed, retrying in ${retry_delay}s (attempt $attempt/$max_retries)"
      sleep "$retry_delay"
      rm -rf "$work_dir/upstream" 2>/dev/null || true
    else
      log_error "Failed to fetch upstream after $max_retries attempts"
      log_error "Unable to reach GitHub. Please check your network connection and try again."
      log_error "Repository URL: $repo_url"
      exit 1
    fi
  done

  cd "$work_dir/upstream"

  # For non-default branches/tags, we need to fetch explicitly since we used --depth 1
  # HEAD means use whatever was cloned (default branch)
  local current_branch
  current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

  if [[ "$version" != "HEAD" && "$version" != "$current_branch" ]]; then
    # Fetch the specific version (try branch first, then tag)
    if ! git fetch --depth 1 origin "$version" --quiet 2>/dev/null; then
      # Try as a tag
      if ! git fetch --depth 1 origin "refs/tags/$version:refs/tags/$version" --quiet 2>/dev/null; then
        log_error "Invalid version: $version"
        log_error "The specified version does not exist in the upstream repository."
        log_error "Use 'latest' for the most recent release, 'main' for bleeding edge,"
        log_error "or specify a valid tag like 'v1.0.0'."
        cd - >/dev/null
        exit 1
      fi
    fi

    # Checkout the fetched version (try branch, then tag, then FETCH_HEAD)
    if ! git checkout "$version" --quiet 2>/dev/null; then
      if ! git checkout "tags/$version" --quiet 2>/dev/null; then
        if ! git checkout FETCH_HEAD --quiet 2>/dev/null; then
          log_error "Failed to checkout version: $version"
          log_error "The version was fetched but checkout failed unexpectedly."
          cd - >/dev/null
          exit 1
        fi
      fi
    fi
  fi

  # Configure sparse-checkout to fetch config dirs and sync infrastructure
  if ! git sparse-checkout init --cone --quiet 2>/dev/null; then
    log_warn "Sparse-checkout init failed, continuing with full checkout"
  fi
  if ! git sparse-checkout set .claude .codex .github/workflows/template-sync.yml klaude-plugin/.claude-plugin/plugin.json --quiet 2>/dev/null; then
    log_warn "Sparse-checkout set failed, config dirs may not exist at this version"
  fi

  cd - >/dev/null

  # Build a staging structure with claude/ subdirs (without dot prefix)
  # so the downstream substitution and comparison pipeline works unchanged.
  FETCHED_TEMPLATES_PATH="$work_dir/fetched"
  mkdir -p "$FETCHED_TEMPLATES_PATH"

  local upstream_root="$work_dir/upstream"
  if [[ -d "$upstream_root/.claude" ]]; then
    cp -rp "$upstream_root/.claude" "$FETCHED_TEMPLATES_PATH/claude"
    # settings.local.json is per-repo and must never be synced downstream
    rm -f "$FETCHED_TEMPLATES_PATH/claude/settings.local.json"
    # Guard additions belong to the downstream project, never the template.
    rm -f "$FETCHED_TEMPLATES_PATH/claude/kk-guard.json"
    # capy-related configs and files are generated by capy tooling per-repo and must never be synced downstream
    rm -rf "$FETCHED_TEMPLATES_PATH/claude/capy"
    rm -f "$FETCHED_TEMPLATES_PATH/claude/scripts/capy.sh"
  fi
  if [[ -d "$upstream_root/.codex" ]]; then
    cp -rp "$upstream_root/.codex" "$FETCHED_TEMPLATES_PATH/codex"
    rm -f "$FETCHED_TEMPLATES_PATH/codex/scripts/capy.sh"
    # .codex/capy-owner is the per-repo installation ID written by
    # `capy setup --platform codex`; capy refuses to regenerate it, so it
    # must never be synced or deleted downstream.
    rm -f "$FETCHED_TEMPLATES_PATH/codex/capy-owner"
  fi
  if [[ ! -d "$FETCHED_TEMPLATES_PATH/claude" ]]; then
    log_error "Config directories not found in upstream at version: $version"
    log_error "Expected .claude/ in the upstream repository."
    log_error "The upstream repository may not have this directory at this version,"
    log_error "or the repository structure has changed."
    exit 1
  fi

  log_success "Fetched config from $upstream @ $version"
}

# fetch_settings_base()
# Fetches upstream .claude/settings.json at the previously synced version, the
# base for the three-way settings merge. Without a base, the merge cannot tell
# an entry upstream removed from one the project added, so removals never
# propagate. Failure is non-fatal: the merge falls back to the union merge.
#
# Only tags and full commit SHAs identify a fixed base. A branch name or short
# SHA recorded by an older sync, versions before .claude/settings.json existed,
# and unreachable refs leave the base unset with a warning.
#
# Args:
#   $1 - Previously synced version (manifest template_version)
#   $2 - Directory with fetched templates (claude/settings.json is upstream)
#   $3 - Upstream partial clone created by fetch_upstream_templates
#   $4 - Work directory for the base file
#
# Side effects:
#   Sets SETTINGS_BASE_FILE to the base file path, or to "" without a base;
#   then SETTINGS_BASE_WARNING explains why, for the sync report
fetch_settings_base() {
  local version="$1"
  local templates_dir="$2"
  local upstream_clone="$3"
  local work_dir="$4"
  local base_file="$work_dir/settings-base.json"
  SETTINGS_BASE_FILE=""
  SETTINGS_BASE_WARNING=""

  if [[ -z "$version" || "$version" == "null" ]]; then
    settings_base_unavailable "no previous template_version"
    return 0
  fi

  if [[ "$version" == "$RESOLVED_VERSION" ]]; then
    if ! cp "$templates_dir/claude/settings.json" "$base_file" 2>/dev/null; then
      settings_base_unavailable "no .claude/settings.json at $version"
      return 0
    fi
  else
    local ref
    if [[ "$version" =~ ^[0-9a-f]{40}$ ]]; then
      ref="$version"
    else
      ref="refs/tags/$version"
    fi
    # The partial clone fetches only the commit and tree; git show pulls the
    # one blob on demand. FETCH_HEAD is the only ref this touches.
    if ! git -C "$upstream_clone" fetch --depth 1 --quiet origin "$ref" 2>/dev/null ||
      ! git -C "$upstream_clone" show "FETCH_HEAD:.claude/settings.json" >"$base_file" 2>/dev/null; then
      settings_base_unavailable "no .claude/settings.json fetched at $version (it must be a tag or full commit SHA)"
      rm -f "$base_file"
      return 0
    fi
  fi

  if ! jq -e 'type == "object"' "$base_file" &>/dev/null; then
    settings_base_unavailable ".claude/settings.json at $version is not a JSON object"
    rm -f "$base_file"
    return 0
  fi
  SETTINGS_BASE_FILE="$base_file"
}

# settings_base_unavailable()
# Records and logs why the three-way settings merge falls back to the union.
settings_base_unavailable() {
  SETTINGS_BASE_WARNING="No settings base ($1): settings entries removed upstream were not removed downstream"
  log_warn "$SETTINGS_BASE_WARNING"
}

# =============================================================================
# Self-Update Handoff
# =============================================================================

# handoff_to_upstream_script()
# Hands the current run over to the upstream copy of this script when the two
# differ, so the script version that matches the target templates drives the
# whole sync — fetch, migrations, report, apply — in a single invocation.
#
# Why this exists:
#   1. bash reads scripts lazily by byte offset. When apply_changes() copies a
#      newer template-sync.sh over the running one, the old shell keeps reading
#      the new file at stale offsets: at best a spurious "syntax error near
#      unexpected token" after main() returns, at worst execution of whatever
#      unrelated line the offset lands on.
#   2. Migrations that only the newer script knows about are not applied until
#      the user runs the sync a second time, and --dry-run previews miss them.
#
# Handing off BEFORE any mutation avoids both: the running (old) process never
# touches the working tree, and the new script sees the same pre-sync state.
#
# The upstream copy is exec()'d from $STAGING_DIR/bin — a stable location the
# later working-tree copy cannot disturb — with the original CLI arguments.
# It is read from the fetched/substituted templates tree (non-hidden
# `claude/...` layout) rather than the raw upstream checkout: in CI the
# staging dir travels through an artifact that drops hidden paths, so the
# `upstream/.claude/...` copy is not available in --apply mode.
#
# Environment contract with the exec()'d script (forward-only — newer scripts
# must keep honoring these names, since an older parent sets them):
#   TEMPLATE_SYNC_NO_HANDOFF=1         Skip the handoff. Set for the child to
#                                      prevent loops; users may set it to run a
#                                      locally modified script as-is.
#   TEMPLATE_SYNC_HANDOFF_CLEANUP=DIR  Auto-created temp dir owned by the
#                                      parent. exec() skips the parent's EXIT
#                                      trap, so the child removes it in
#                                      cleanup_on_exit().
#
# Args:
#   $1 - Templates dir laid out as claude/toolbox/scripts/... — either
#        FETCHED_TEMPLATES_PATH (fetch modes) or "$STAGING_DIR/substituted"
#        (--apply mode)
#   $@ - Remaining args: the original CLI arguments to re-pass verbatim
#
# Returns:
#   0 when no handoff is needed: identical script, handoff disabled, running
#     sourced rather than as the entry point, or no script at the target
#     version. Does not return when a handoff happens.
#
# Side effects:
#   On handoff, in fetch modes: removes the upstream/fetched/substituted
#   staging subdirs so the child's own fetch starts from a clean directory
#   (git clone refuses a non-empty target; cp -r would nest into existing
#   dirs). Left intact in --apply mode, where the child consumes them.
handoff_to_upstream_script() {
  local templates_dir="$1"
  shift

  if [[ -n "${TEMPLATE_SYNC_NO_HANDOFF:-}" ]]; then
    return 0
  fi

  # exec() replaces the whole process — only safe when this file IS the
  # process' main script, not when sourced by the test suite or another script.
  if ! $IS_ENTRYPOINT; then
    return 0
  fi

  local self="${BASH_SOURCE[0]}"
  local upstream_scripts_dir="$templates_dir/claude/toolbox/scripts"
  local upstream_script="$upstream_scripts_dir/template-sync.sh"

  if [[ ! -f "$upstream_script" ]]; then
    return 0
  fi

  if cmp -s "$self" "$upstream_script"; then
    return 0
  fi

  log_step "Sync script differs from upstream — handing off to the upstream version"

  local bin_dir="$STAGING_DIR/bin"
  mkdir -p "$bin_dir"
  cp "$upstream_script" "$bin_dir/template-sync.sh"
  chmod +x "$bin_dir/template-sync.sh"
  # The script sources semver-compare.sh from its own directory and would
  # otherwise bootstrap it from master over the network — keep them together.
  if [[ -f "$upstream_scripts_dir/semver-compare.sh" ]]; then
    cp "$upstream_scripts_dir/semver-compare.sh" "$bin_dir/semver-compare.sh"
  fi

  if ! $APPLY_MODE; then
    rm -rf "$STAGING_DIR/upstream" "$STAGING_DIR/fetched" "$STAGING_DIR/substituted"
  fi

  export TEMPLATE_SYNC_NO_HANDOFF=1
  if [[ -n "${TEMP_DIR:-}" ]]; then
    export TEMPLATE_SYNC_HANDOFF_CLEANUP="$TEMP_DIR"
  fi

  # $BASH is the interpreter running this script — reuse it rather than
  # whatever `bash` resolves to on PATH (matters on macOS with a Homebrew bash).
  exec "${BASH:-bash}" "$bin_dir/template-sync.sh" "$@"
}

# =============================================================================
# Substitution Functions
# =============================================================================

# Retain unchanged explicit tables verbatim; render only changed or repaired
# registrations. The scanner finds source spans, while yq remains the TOML
# parser and checks whether each server's source matches its merged value.
# Embedded to keep self-update handoff compatible with older sync scripts.
codex_toml() {
  python3 -I - "$@" <<'PY'
import copy
import json
from pathlib import Path
import re
import subprocess
import sys


def parse_toml(data):
    result = subprocess.run(
        ["yq", "-p", "toml", "-o", "json", "."],
        input=data, stdout=subprocess.PIPE, check=True, timeout=30,
    )
    # yq represents an empty or comment-only TOML document as JSON null.
    return json.loads(result.stdout) or {}


ABSENT = object()
POLICIES = {"sandbox_mode", "approval_policy", "approvals_reviewer"}


def same(left, right):
    if left is ABSENT or right is ABSENT:
        return left is right
    return json.dumps(left, sort_keys=True) == json.dumps(right, sort_keys=True)


def compare_config(local, template, base, retire, keep, path=()):
    if path in keep and local is not ABSENT:
        return local
    if same(local, template):
        return ABSENT if retire else local
    if isinstance(local, dict) and (isinstance(template, dict) or template is ABSENT):
        result = {}
        upstream = {} if template is ABSENT else template
        before = base if isinstance(base, dict) else {}
        for key in dict.fromkeys([*local, *upstream]):
            value = compare_config(local.get(key, ABSENT), upstream.get(key, ABSENT),
                                   before.get(key, ABSENT), retire, keep, path + (key,))
            if value is not ABSENT:
                result[key] = value
        return result if result or not local else ABSENT
    if retire:
        return local
    if local is ABSENT or same(local, base):
        return template
    return local


def lookup(obj, path):
    for key in path:
        if not isinstance(obj, dict) or key not in obj:
            return ABSENT
        obj = obj[key]
    return obj


def toml_value(value):
    if isinstance(value, dict):
        return "{ " + ", ".join(json.dumps(k, ensure_ascii=False) + " = " + toml_value(v)
                                 for k, v in value.items()) + " }"
    if isinstance(value, list):
        return "[" + ", ".join(map(toml_value, value)) + "]"
    return json.dumps(value, ensure_ascii=False)


KEY = re.compile(rb"""\s*((?:"(?:\\.|[^"\\])*"|'[^']*'|[^="'\n])+?)\s*=""")


def assignment_path(key):
    probe = parse_toml(key + b" = true")
    path = []
    while isinstance(probe, dict):
        name, probe = next(iter(probe.items()))
        path.append(name)
    return tuple(path)


def string_end(data, start):
    char = data[start:start + 1]
    delim = char * 3 if data.startswith(char * 3, start) else char
    pos = start + len(delim)
    while pos < len(data):
        if data.startswith(delim, pos):
            pos += len(delim)
            if len(delim) == 3:
                while data[pos:pos + 1] == char:
                    pos += 1
            return pos
        pos += 2 if char == b'"' and data[pos:pos + 1] == b"\\" else 1
    raise ValueError("unterminated TOML string")


def rewrite_value(raw, old, new):
    """Edit members of an inline table without respelling its surviving siblings."""
    start = len(raw) - len(raw.lstrip())
    if not (isinstance(old, dict) and isinstance(new, dict) and raw[start:start+1] == b"{"):
        return b" " + toml_value(new).encode() + (b"\n" if raw.endswith(b"\n") else b"")
    fields = []
    remaining = copy.deepcopy(new)
    pos = begin = start + 1
    depth = 0
    while pos < len(raw):
        char = raw[pos:pos+1]
        if char in (b"'", b'"'):
            pos = string_end(raw, pos)
            continue
        if char == b"#":
            pos = raw.find(b"\n", pos)
            if pos < 0:
                break
        elif depth == 0 and char in (b",", b"}"):
            member = raw[begin:pos]
            if member.strip():
                key = KEY.match(member)
                if key is None:
                    raise ValueError("cannot identify inline TOML member")
                path = assignment_path(key[1])
                value = lookup(new, path)
                if value is not ABSENT:
                    previous = lookup(old, path)
                    fields.append(member if same(previous, value) else
                                  member[:key.end()] + rewrite_value(member[key.end():], previous, value))
                    lookup(remaining, path[:-1]).pop(path[-1], None)
            begin = pos + 1
            if char == b"}":
                def additions(items, prefix=()):
                    for key, value in items.items():
                        path = prefix + (key,)
                        if isinstance(value, dict) and isinstance(lookup(old, path), dict):
                            yield from additions(value, path)
                        else:
                            name = ".".join(json.dumps(k, ensure_ascii=False) for k in path)
                            yield (" " + name + " = " + toml_value(value)).encode()
                fields.extend(additions(remaining))
                return raw[:start + 1] + b",".join(fields) + raw[pos:]
        elif char in (b"{", b"["):
            depth += 1
        elif char in (b"}", b"]"):
            depth -= 1
        pos += 1
    raise ValueError("unterminated inline TOML table")

def statements(data):
    """Yield complete TOML statements, including original terminators and trivia."""
    start = pos = depth = 0
    while pos < len(data):
        char = data[pos:pos + 1]
        if char in (b'"', b"'"):
            pos = string_end(data, pos)
            continue
        if char == b"#":
            newline = data.find(b"\n", pos)
            pos = len(data) if newline < 0 else newline
            continue
        if char in (b"[", b"{"):
            depth += 1
        elif char in (b"]", b"}"):
            depth -= 1
        elif char == b"\n" and depth == 0:
            yield data[start:pos + 1]
            start = pos + 1
        pos += 1
    if start < len(data):
        yield data[start:]


def table_spans(data):
    header, body, trivia = None, [], []
    for statement in statements(data):
        if not statement.strip() or statement.lstrip().startswith(b"#"):
            trivia.append(statement)
            continue
        if statement.lstrip().startswith(b"["):
            if header is not None:
                yield header, b"".join(body)
            header = statement.rstrip(b"\r\n")
            body = []
        body.extend(trivia)
        body.append(statement)
        trivia = []
    if header is not None:
        yield header, b"".join(body + trivia)


def table_path(header):
    # Let the TOML parser interpret quoted/dotted keys and array-table headers.
    marker = "__toolbox_table_probe__"
    node = parse_toml(header + b"\n" + marker.encode() + b" = true\n")
    path = []
    while node != {marker: True}:
        if isinstance(node, list) and len(node) == 1:
            node = node[0]
        elif isinstance(node, dict) and len(node) == 1:
            key, node = next(iter(node.items()))
            path.append(key)
        else:
            raise ValueError("unexpected TOML table path")
    return path


def render(merged, source):
    sections = []
    groups = {}
    explicit = set()
    for header, block in table_spans(source):
        path = table_path(header)
        if len(path) < 2 or path[0] != "mcp_servers":
            continue
        name = path[1]
        sections.append((name, block))
        groups.setdefault(name, []).append(block)
        if len(path) == 2 and not header.lstrip().startswith(b"[["):
            explicit.add(name)

    preserved = set()
    for name in explicit & merged.keys():
        actual = parse_toml(b"".join(groups[name])).get("mcp_servers", {})
        # Compare JSON representations so booleans cannot compare equal to 0/1.
        if json.dumps(actual, sort_keys=True) == json.dumps({name: merged[name]}, sort_keys=True):
            preserved.add(name)

    fragments = [block for name, block in sections if name in preserved]
    for name, value in merged.items():
        if name in preserved:
            continue
        # TOML child table headers are absolute. Give the encoder their full
        # path so nested env and http_headers stay inside the named server.
        result = subprocess.run(
            ["yq", "-p", "json", "-o", "toml", "."],
            input=json.dumps({"mcp_servers": {name: value}}).encode(), stdout=subprocess.PIPE,
            check=True, timeout=30,
        )
        fragments.append(b"\n" + result.stdout)

    output = bytearray()
    for fragment in fragments:
        if (not output and not fragment.startswith((b"\n", b"\r\n"))) or (
            output and not output.endswith(b"\n")
        ):
            output.extend(b"\n")
        output.extend(fragment)
    return output


def edit_config(source, desired, retire):
    """Retain original TOML statements, quoting and comments for surviving values."""
    original = parse_toml(source)
    if same(original, desired):
        return source
    remaining = copy.deepcopy(desired)
    sections = list(table_spans(source))
    preamble = source[:len(source) - sum(len(block) for _, block in sections)]
    rendered = []
    insertions = {}

    def consume(path):
        parent = lookup(remaining, path[:-1])
        if isinstance(parent, dict):
            parent.pop(path[-1], None)

    for header, block in [(None, preamble), *sections]:
        table = tuple(table_path(header)) if header is not None else ()
        # Array tables and their subtables form one value. Leave the entire
        # original sequence in place if it survives unchanged.
        array = next((table[:i] for i in range(1, len(table) + 1)
                      if isinstance(lookup(original, table[:i]), list)), None)
        if array is not None:
            if same(lookup(original, array), lookup(desired, array)):
                rendered.append(block)
                consume(array)
            continue
        if not isinstance(lookup(desired, table), dict):
            continue
        out = bytearray()
        lines = statements(block)
        if header is not None:
            for line in lines:
                out.extend(line)
                if line.rstrip(b"\r\n") == header.rstrip(b"\r"):
                    break
        preceding_trivia = b""
        for line in lines:
            if not line.strip() or line.lstrip().startswith(b"#"):
                out.extend(line)
                preceding_trivia = line
                continue
            # Ask the TOML parser to decode dotted and quoted keys. The value
            # can span several physical lines (arrays and multiline strings).
            key = KEY.match(line)
            if key is None:
                raise ValueError("cannot identify TOML assignment: " + repr(line))
            raw_key = key[1]
            path = table + assignment_path(raw_key)
            value = lookup(desired, path)
            if (retire and value is ABSENT and path == ("project_doc_max_bytes",)
                    and preceding_trivia.rstrip(b"\r\n") == b"# Allow larger project instruction chains before truncation."):
                del out[-len(preceding_trivia):]
            preceding_trivia = b""
            if value is not ABSENT:
                if same(lookup(original, path), value):
                    out.extend(line)
                else:
                    out.extend(line[:key.end()] +
                               rewrite_value(line[key.end():], lookup(original, path), value))
                consume(path)
        rendered.append(out)
        insertions[table] = out

    # Add incoming keys to their original enclosing table. Never repeat an
    # explicit header or redefine a dotted key's implicit parent.
    def add(node, prefix=()):
        for key, value in node.items():
            path = prefix + (key,)
            if isinstance(value, dict) and (isinstance(lookup(original, path), dict)
                                            or path in insertions):
                add(value, path)
                continue
            parent = prefix
            while parent not in insertions:
                parent = parent[:-1]
            out = insertions[parent]
            if out and not out.endswith(b"\n"):
                out.extend(b"\n")
            name = ".".join(json.dumps(k, ensure_ascii=False) for k in path[len(parent):])
            out.extend((name + " = " + toml_value(value) + "\n").encode())
    add(remaining)
    output = b"".join(rendered)
    if not same(parse_toml(output), desired):
        raise ValueError("could not preserve the repository's TOML settings")
    return output


if sys.argv[1] == "servers":
    output = render(json.loads(Path(sys.argv[2]).read_bytes()), Path(sys.argv[3]).read_bytes())
else:
    mode, source_file, template_file, base_file, model = sys.argv[1:]
    source = Path(source_file).read_bytes()
    local = parse_toml(source)
    template = parse_toml(Path(template_file).read_bytes())
    base = parse_toml(Path(base_file).read_bytes()) if base_file else {}
    keep = {(key,) for key in POLICIES}
    if mode == "retire" and model not in ("", "gpt-6.2-astra"):
        keep.add(("model",))
    # Evaluate top-level keys individually so whole-document equality cannot
    # remove policy fields or an explicitly selected model.
    desired = {}
    for key in dict.fromkeys([*local, *template]):
        item = compare_config(local.get(key, ABSENT), template.get(key, ABSENT),
                              base.get(key, ABSENT), mode == "retire", keep, (key,))
        if item is not ABSENT:
            desired[key] = item
    if mode == "retire":
        for key, value in desired.items():
            label = " = " + toml_value(value) if key in POLICIES or key == "model" else ""
            print("Keep Codex {}{}".format(key, label), file=sys.stderr)
    output = edit_config(source, desired, mode == "retire") if desired or not local else b""
sys.stdout.buffer.write(output)
PY
}

render_codex_mcp_servers() { codex_toml servers "$@"; }

# Keep this editor inside the sync script: older handoffs and kk migrate
# download just template-sync.sh and semver-compare.sh.
migration_json() {
  python3 -I - "$@" <<'PY'
import json
from pathlib import Path
import shlex
import sys

mode, source, template, manifest, base = sys.argv[1:]
text = Path(source).read_bytes().decode("utf-8")


def unique_object(pairs):
    obj = dict(pairs)
    if len(obj) != len(pairs):
        raise ValueError("ambiguous duplicate JSON member in " + source)
    return obj


local = json.loads(text, object_pairs_hook=unique_object)
up = json.loads(Path(template).read_bytes())
variables = json.loads(Path(manifest).read_bytes())["variables"]
missing = object()
origins = {}


def identity(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def legacy_statusline(command):
    try:
        words = shlex.split(command)
    except ValueError:
        return False
    if words and Path(words[0]).name in ("bash", "sh"):
        words = words[1:]
    if not words:
        return False
    scripts = {".claude/toolbox/scripts/statusline.sh", ".claude/toolbox/scripts/statusline_enhanced.sh"}
    return any(words[0] == prefix + script for script in scripts for prefix in (
        "", "./", "$CLAUDE_PROJECT_DIR/", "${CLAUDE_PROJECT_DIR}/", str(Path.cwd()) + "/"))


def subtract(value, reference, path=()):
    if path in keep or reference is missing:
        return value
    if path == ("statusLine",):
        if (isinstance(value, dict) and isinstance(value.get("command"), str)
                and (value == reference or legacy_statusline(value["command"]))):
            return missing
        return value
    if isinstance(value, dict) and isinstance(reference, dict):
        result = {}
        for key, item in value.items():
            rest = subtract(item, reference.get(key, missing), path + (key,))
            if rest is not missing:
                result[key] = rest
        if result or (not value and reference):
            return result
        return missing
    if isinstance(value, list) and isinstance(reference, list):
        owned = {identity(item) for item in reference}
        result = [item for item in value if identity(item) not in owned]
        return result if result else missing
    return missing if identity(value) == identity(reference) else value


def filter_hooks(document, upstream, previous=None, extra_commands=()):
    owned = {h["command"] for groups in upstream.values() for g in groups for h in g["hooks"]
             if isinstance(h.get("command"), str)}
    owned.update(extra_commands)
    if previous:
        for groups in json.loads(Path(previous).read_bytes()).get("hooks", {}).values():
            for group in groups:
                for handler in group["hooks"]:
                    cmd = handler.get("command", "")
                    if ".codex/scripts/" in cmd and ".codex/scripts/capy.sh" not in cmd:
                        owned.add(cmd)
    events = {}
    for name, groups in document.get("hooks", {}).items():
        remaining = []
        for group in groups:
            handlers = [h for h in group["hooks"] if h.get("command") not in owned]
            if handlers or not group["hooks"]:
                retained = dict(group, hooks=handlers)
                origins[id(retained)] = group
                remaining.append(retained)
        if remaining or not groups:
            events[name] = remaining
    if mode == "hooks-sync":
        for name, groups in upstream.items():
            events[name] = groups + events.get(name, [])
    result = dict(document)
    if events:
        result["hooks"] = events
    else:
        result.pop("hooks", None)
    return result


def preserve_spelling(desired):
    # Bind source slices to their locations. Equal commands in different
    # events may have different escaping, spacing, or key order.
    decoder = json.JSONDecoder()
    spans, prefixes, locations = {}, {}, {}

    def whitespace(pos):
        while pos < len(text) and text[pos] in " \r\n\t":
            pos += 1
        return pos

    def read(value, path, start):
        pos = start
        if isinstance(value, (dict, list)):
            locations[id(value)] = path
            pos = whitespace(pos + 1)
            entries = value.items() if isinstance(value, dict) else enumerate(value)
            for key, child in entries:
                if isinstance(value, dict):
                    member = pos
                    _, end = decoder.raw_decode(text, pos)
                    pos = whitespace(whitespace(end) + 1)
                    prefixes[path + (key,)] = text[member:pos]
                pos = whitespace(read(child, path + (key,), pos))
                if text[pos] == ",":
                    pos = whitespace(pos + 1)
            pos += 1
        else:
            _, pos = decoder.raw_decode(text, pos)
        spans[path] = (value, text[start:pos])
        return pos

    def write(value, path, level):
        if isinstance(value, (dict, list)):
            path = locations.get(id(origins.get(id(value), value)), path)
        old, raw = spans.get(path, (missing, None))
        if old is not missing and identity(old) == identity(value):
            return raw
        if isinstance(value, dict):
            items = []
            for key, child in value.items():
                child_path = None if path is None else path + (key,)
                prefix = prefixes.get(child_path, json.dumps(key) + ": ")
                items.append(prefix + write(child, child_path, level + 1))
            left, right = "{", "}"
        elif isinstance(value, list):
            available = list(range(len(old))) if isinstance(old, list) else []
            items = []
            for i, child in enumerate(value):
                match = next((j for j in available if identity(old[j]) == identity(child)), None)
                if match is not None:
                    available.remove(match)
                child_path = None if path is None else path + (match if match is not None else i,)
                items.append(write(child, child_path, level + 1))
            left, right = "[", "]"
        else:
            return json.dumps(value, ensure_ascii=False)
        pad = "\n" + "  " * (level + 1)
        return left + (pad + ("," + pad).join(items) + "\n" + "  " * level if items else "") + right

    if identity(local) == identity(desired):
        return text
    read(local, (), whitespace(0))
    output = write(desired, (), 0) + "\n"
    if identity(json.loads(output, object_pairs_hook=unique_object)) != identity(desired):
        raise ValueError("could not preserve repository JSON in " + source)
    return output


if mode.startswith("hooks-"):
    result = filter_hooks(local, up.get("hooks", {}), base)
    if mode == "hooks-retire":
        for event, groups in result.get("hooks", {}).items():
            for i, group in enumerate(groups):
                for j, handler in enumerate(group["hooks"]):
                    print("Keep Codex hooks.{}[{}].hooks[{}] ({})".format(
                        event, i, j, handler.get("type", "handler")), file=sys.stderr)
elif mode == "settings-retire":
    keep = {path for path, name, default in (
        (("model",), "CC_MODEL", "default"), (("effortLevel",), "CC_EFFORT_LEVEL", "high"),
        (("permissions", "defaultMode"), "CC_PERMISSION_MODE", "default"),
    ) if variables.get(name) not in (None, "", default)}
    result = subtract(local, up)
    if result is not missing:
        for key, value in result.items():
            if key == "permissions" and isinstance(value, dict):
                for field, entries in value.items():
                    if field == "deny":
                        for entry in entries:
                            print("Keep Claude deny " + json.dumps(entry), file=sys.stderr)
                    else:
                        print("Keep Claude permissions." + field, file=sys.stderr)
            else:
                print("Keep Claude " + key, file=sys.stderr)
else:
    result = up  # Apply the existing settings merge with adopter spelling.
    if base == "true" and "hooks" in up:
        # The pre-plugin template supplied this exact Bash handler. Strip it
        # during staging so both the preview and apply retain its neighbours.
        text = preserve_spelling(up)
        local = json.loads(text, object_pairs_hook=unique_object)
        result = filter_hooks(local, {}, extra_commands=["bash $CLAUDE_PROJECT_DIR/.claude/scripts/validate-bash.sh"])
if result is not missing and (result or not local or not mode.endswith("-retire")):
    sys.stdout.write(preserve_spelling(result))
PY
}

# apply_substitutions()
# Applies project-specific variable substitutions to fetched template files.
# Mirrors the substitution logic from template-cleanup.sh for consistency.
#
# Args:
#   $1 - Source template directory (raw fetched templates)
#   $2 - Output directory for substituted templates
#
# Returns:
#   0 on success
#
# Substitutions applied:
#   - Claude Code settings: CC_MODEL, CC_EFFORT_LEVEL, CC_PERMISSION_MODE
#   - Codex config.toml: CODEX_MODEL, CODEX_APPROVAL_POLICY; downstream
#     mcp_servers entries preserved
#   - Codex hooks.json: downstream non-toolbox hook entries preserved
#
# Side effects:
#   Creates output directory and copies/modifies template files
#   Logs progress messages
apply_substitutions() {
  local template_dir="$1"
  local output_dir="$2"
  DROPPED_DENY_ENTRIES=()
  SETTINGS_REMOVED_ENTRIES=()
  SETTINGS_CONFLICT_ENTRIES=()

  log_step "Applying substitutions from manifest"

  # Copy templates to output directory (preserving permissions)
  mkdir -p "$output_dir"
  cp -rp "$template_dir"/* "$output_dir/"

  # Read all variables from manifest
  local project_name languages cc_model cc_effort_level cc_permission_mode cc_statusline

  project_name=$(get_manifest_value '.variables.PROJECT_NAME')
  languages=$(get_manifest_value '.variables.LANGUAGES')
  cc_model=$(get_manifest_value '.variables.CC_MODEL')
  cc_effort_level=$(get_manifest_value '.variables.CC_EFFORT_LEVEL // "high"')
  cc_permission_mode=$(get_manifest_value '.variables.CC_PERMISSION_MODE // "default"')
  cc_statusline=$(get_manifest_value '.variables.CC_STATUSLINE // "enhanced"')

  # --- Claude Code Settings (claude/settings.json) ---
  local cc_settings_file="$output_dir/claude/settings.json"
  if [[ -f "$cc_settings_file" ]]; then
    # Three-way merge of downstream settings (D) with upstream (U), against
    # upstream at the last synced version (B, from fetch_settings_base):
    #   - upstream removed an entry: removed if D still equals B, else kept
    #     and reported (objects recurse, so untouched sub-keys still go)
    #   - upstream changed a value: taken if D still equals B, else D wins
    #     and the conflict is reported
    #   - upstream entries missing downstream are (re-)added; whether the
    #     project deleted them or never received them is unknowable, because
    #     template_version advances even when settings were excluded or
    #     reverted in the sync PR
    #   - arrays are element sets with the same rules; downstream order kept,
    #     new upstream elements appended
    # Without B this is the union merge: D wins, arrays unioned, no reports.
    # Upstream owns permissions.deny, so retired denies do not linger.
    # Falls back to the upstream template copy for first-time sync.
    local downstream_settings=".claude/settings.json"
    if [[ -f "$downstream_settings" ]] && { [[ ${TEMPLATE_SYNC_MERGE_DENY:-0} != 1 ]] || ! is_excluded "$downstream_settings"; }; then
      # $cc_settings_file contains the upstream template copy at this point.
      # Read downstream as jq input, upstream and base via --slurpfile.
      local dropped_deny_json merge_json
      if dropped_deny_json=$(jq -c --slurpfile upstream "$cc_settings_file" '
        (.permissions.deny // []) - ($upstream[0].permissions.deny // [])
      ' "$downstream_settings") && merge_json=$(jq -c \
        --arg merge_deny "${TEMPLATE_SYNC_MERGE_DENY:-0}" \
        --slurpfile upstream "$cc_settings_file" \
        --slurpfile base "${SETTINGS_BASE_FILE:-/dev/null}" '
        # Overwritten after the merge by manifest substitutions or the deny
        # baseline. B takes U'"'"'s value there, which keeps D-wins behavior
        # and reports nothing for them.
        def owned_paths: [["model"], ["effortLevel"], ["permissions", "defaultMode"],
          ["statusLine"], ["extraKnownMarketplaces", "claude-toolbox", "source"]]
          + (if $merge_deny == "1" then [] else [["permissions", "deny"]] end);
        def has_path($p): try (getpath($p[:-1]) | type == "object" and has($p[-1])) catch false;
        def neutralize($u): reduce owned_paths[] as $p (.;
          if ($u | has_path($p)) then setpath($p; $u | getpath($p))
          elif has_path($p) then delpaths([$p]) else . end);
        def has_el($e): any(.[]; . == $e);
        def child($p; $k):
          if ($k | test("^[A-Za-z_][A-Za-z0-9_]*$")) then (if $p == "" then $k else "\($p).\($k)" end)
          else "\($p)[\($k | tojson)]" end;
        def show: if type == "string" and (test("\n") | not) then . else tojson end;
        def none: {removed: [], conflicts: []};
        def plus($r): {removed: (.removed + $r.removed), conflicts: (.conflicts + $r.conflicts)};
        # . is the D value; $hb: a base exists; $bk: the key is in B with value $b.
        def m3($u; $hb; $bk; $b; $p):
          . as $d
          | if ($d | type) == "object" and ($u | type) == "object" then
              (if $bk and ($b | type) == "object" then $b else {} end) as $bo
              | reduce (($d | keys_unsorted) + [($u | keys)[] | select(. as $k | $d | has($k) | not)])[] as $k
                  ({v: {}, r: none};
                   child($p; $k) as $kp
                   | if ($d | has($k)) and ($u | has($k)) then
                       ($d[$k] | m3($u[$k]; $hb; ($bo | has($k)); $bo[$k]; $kp)) as $m
                       | .v[$k] = $m.v | .r |= plus($m.r)
                     elif ($u | has($k)) then .v[$k] = $u[$k]
                     elif $hb and ($bo | has($k)) then
                       if $d[$k] == $bo[$k] then .r.removed += [$kp]
                       elif ($d[$k] | type) == ($bo[$k] | type) and (($d[$k] | type) == "object" or ($d[$k] | type) == "array") then
                         ($d[$k] | m3(if type == "object" then {} else [] end; true; true; $bo[$k]; $kp)) as $m
                         | .r |= plus($m.r)
                         | if ($m.v | length) > 0 then .v[$k] = $m.v else . end
                       else .v[$k] = $d[$k] | .r.conflicts += ["\($kp): kept \($d[$k] | tojson), upstream removed it"]
                       end
                     else .v[$k] = $d[$k] end)
            elif ($d | type) == "array" and ($u | type) == "array" then
              (if $hb and $bk and ($b | type) == "array" then $b else [] end) as $ba
              | [$d[] | select(. as $e | ($ba | has_el($e)) and ($u | has_el($e) | not))] as $gone
              | {v: ([$d[] | select(. as $e | $gone | has_el($e) | not)]
                     + [$u[] | select(. as $e | $d | has_el($e) | not)]),
                 r: {removed: [$gone[] | "\($p): \(show)"], conflicts: []}}
            elif $d == $u then {v: $d, r: none}
            elif $hb and $bk and $d == $b then {v: $u, r: none}
            elif $hb and $bk and $u == $b then {v: $d, r: none}
            elif $hb then {v: $d, r: {removed: [], conflicts: ["\($p): kept \($d | tojson), upstream has \($u | tojson)"]}}
            else {v: $d, r: none} end;
        (if ($base | length) > 0 and (($base[0].permissions // {}) | type) == "object"
         then (try ($base[0] | neutralize($upstream[0])) catch null) else null end) as $b
        | m3($upstream[0]; $b != null; $b != null; $b; "")
        | if $merge_deny == "1" then . else .v.permissions.deny = ($upstream[0].permissions.deny // []) end
        | .base_rejected = (($base | length) > 0 and $b == null)
      ' "$downstream_settings") && jq '.v' <<<"$merge_json" >"${cc_settings_file}.tmp"; then
        # Excluded settings are never applied, so report no removals for them.
        if ! is_excluded "$downstream_settings"; then
          if [[ ${TEMPLATE_SYNC_MERGE_DENY:-0} != 1 ]]; then
            mapfile -t DROPPED_DENY_ENTRIES < <(jq -r '.[]' <<<"$dropped_deny_json")
          fi
          mapfile -t SETTINGS_REMOVED_ENTRIES < <(jq -r '.r.removed[]' <<<"$merge_json")
          mapfile -t SETTINGS_CONFLICT_ENTRIES < <(jq -r '.r.conflicts[]' <<<"$merge_json")
          if jq -e '.base_rejected' <<<"$merge_json" >/dev/null; then
            settings_base_unavailable "the base settings have an unexpected shape"
          fi
        fi
        mv "${cc_settings_file}.tmp" "$cc_settings_file"
      else
        if [[ ${TEMPLATE_SYNC_MERGE_DENY:-0} == 1 ]] && ! is_excluded "$downstream_settings"; then
          log_error "Cannot merge repository settings for migration: $downstream_settings"
          return 1
        fi
        log_warn "Smart merge failed — downstream .claude/settings.json may contain invalid JSON"
        log_warn "Falling back to upstream template for settings.json"
        rm -f "${cc_settings_file}.tmp"
      fi
    fi

    local statusline_script="statusline_enhanced.sh"
    if [[ "$cc_statusline" == "basic" ]]; then
      statusline_script="statusline.sh"
    fi
    local upstream_repo
    upstream_repo=$(get_manifest_value '.upstream_repo')
    jq \
      --arg cc_model "$cc_model" \
      --arg cc_effort_level "$cc_effort_level" \
      --arg cc_permission_mode "$cc_permission_mode" \
      --arg statusline_script "$statusline_script" \
      --arg repo "$upstream_repo" \
      '
      # Model: "default" removes the key, otherwise set it
      if $cc_model == "default" then del(.model) else .model = $cc_model end |
      # Effort level: "default" removes the key, otherwise set it
      if $cc_effort_level == "default" then del(.effortLevel) else .effortLevel = $cc_effort_level end |
      # Permission mode
      .permissions.defaultMode = $cc_permission_mode |
      # Statusline script (guard against null/missing statusLine)
      # Migrate old path (.claude/scripts/) to new (.claude/toolbox/scripts/)
      # and swap script filename if needed
      (if (.statusLine.command | type) == "string" then
        .statusLine.command |= gsub("\\.claude/scripts/"; ".claude/toolbox/scripts/") |
        .statusLine.command |= gsub("statusline_enhanced\\.sh"; $statusline_script)
      else . end) |
      # Plugin marketplace: directory -> github source for downstream
      .extraKnownMarketplaces."claude-toolbox".source = { "source": "github", "repo": $repo }
      ' "$cc_settings_file" >"${cc_settings_file}.tmp" && mv "${cc_settings_file}.tmp" "$cc_settings_file"

    log_info "Applied Claude Code settings"
    if [[ ${TEMPLATE_SYNC_MERGE_DENY:-0} == 1 && -f $downstream_settings ]] && ! is_excluded "$downstream_settings"; then
      migration_json settings-sync "$downstream_settings" "$cc_settings_file" "$MANIFEST_PATH" "$PLUGIN_MIGRATED" >"$cc_settings_file.tmp"
      mv "$cc_settings_file.tmp" "$cc_settings_file"
    fi
  fi

  # --- Codex Settings (codex/config.toml) ---
  local codex_config_file="$output_dir/codex/config.toml"
  if [[ -f "$codex_config_file" ]]; then
    local codex_model codex_approval_policy
    codex_model=$(get_manifest_value '.variables.CODEX_MODEL // "gpt-6.2-astra"')
    codex_approval_policy=$(get_manifest_value '.variables.CODEX_APPROVAL_POLICY // "on-request"')

    # Remove an empty parent before TOML serialization: yq can otherwise emit
    # it inside the preceding table (usually tui), where later root deletion
    # cannot find it.
    yq -i -p toml -o toml \
      ".model = \"$codex_model\" | .approval_policy = \"$codex_approval_policy\" |
       del(.mcp_servers.capy) | with(select(.mcp_servers | length == 0); del(.mcp_servers))" \
      "$codex_config_file"

    # Capy's registration belongs to the installation that created it, even
    # when capy setup has been run in the template repository itself. Exclude
    # upstream Capy on every path (including first sync and merge fallback).
    # Other downstream MCP entries fill gaps; template servers win by name.
    local mcp_source=".codex/config.toml"
    local has_downstream_mcp=true
    if [[ ! -f "$mcp_source" ]] || { [[ ${TEMPLATE_SYNC_MERGE_DENY:-0} == 1 ]] && is_excluded "$mcp_source"; }; then
      mcp_source="$template_dir/codex/config.toml"
      has_downstream_mcp=false
    fi
    local mcp_work_dir
    mcp_work_dir=$(mktemp -d "${TMPDIR:-/tmp}/codex-mcp.XXXXXX")
    # Recover registrations misplaced by older syncs. A valid root entry
    # replaces the entire misplaced entry, so stale launch settings cannot
    # leak into a registration subsequently repaired by capy setup.
    # Read upstream servers from the original template: yq's TOML rewrite
    # during substitutions can lose quoting on dotted server names.
    if yq -p toml -o json '.' "$mcp_source" 2>/dev/null \
      | jq --argjson downstream "$has_downstream_mcp" \
        '(.tui.mcp_servers // {}) + (.mcp_servers // {}) | if $downstream then . else del(.capy) end' \
        >"$mcp_work_dir/downstream.json" \
      && yq -p toml -o json \
        "load(\"$mcp_work_dir/downstream.json\") * ((.mcp_servers // {}) | del(.capy))" \
        "$template_dir/codex/config.toml" >"$mcp_work_dir/merged.json" 2>/dev/null \
      && yq -p toml -o toml 'del(.mcp_servers)' "$codex_config_file" >"$mcp_work_dir/config.toml" \
      && render_codex_mcp_servers "$mcp_work_dir/merged.json" "$mcp_source" >>"$mcp_work_dir/config.toml" \
      && yq -p toml -o json '.mcp_servers // {}' "$mcp_work_dir/config.toml" \
        | jq -e --slurpfile expected "$mcp_work_dir/merged.json" '. == $expected[0]' >/dev/null; then
      cat "$mcp_work_dir/config.toml" >"$codex_config_file"
      log_info "Preserved mcp_servers in config.toml"
    else
      log_warn "MCP server merge failed — $mcp_source may contain invalid TOML"
      log_warn "Falling back to upstream template for config.toml"
    fi
    rm -rf "$mcp_work_dir"

    if [[ ${TEMPLATE_SYNC_MERGE_DENY:-0} == 1 && -f .codex/config.toml ]] && ! is_excluded .codex/config.toml; then
      local base_config=""
      if [[ -n $CODEX_BASE_DIR && -f $CODEX_BASE_DIR/config.toml ]]; then base_config="$CODEX_BASE_DIR/config.toml"; fi
      codex_toml merge .codex/config.toml "$codex_config_file" "$base_config" "$codex_model" >"$codex_config_file.tmp"
      mv "$codex_config_file.tmp" "$codex_config_file"
    fi

    log_info "Applied Codex config.toml settings"
  fi

  # --- Codex Hooks (codex/hooks.json) ---
  local codex_hooks_file="$output_dir/codex/hooks.json"
  local downstream_hooks=".codex/hooks.json"
  # Only toolbox-owned hooks are distributable. In particular, never ship the
  # template checkout's owner-bound Capy hooks or its legacy Capy wrapper.
  # Sanitize before the merge so first-sync and fallback paths obey this too.
  local toolbox_hook_filter='def toolbox_owned:
    [.hooks[]?.command // empty]
    | any(contains(".codex/scripts/") and (contains(".codex/scripts/capy.sh") | not));'
  if [[ -f "$codex_hooks_file" && ( $RETIRE_MODE == true || ${TEMPLATE_SYNC_MERGE_DENY:-0} == 1 ) ]]; then
    jq '.hooks |= (map_values([.[] | .hooks |= map(select(
        (.command // "") | contains(".codex/scripts/") and (contains(".codex/scripts/capy.sh") | not)))
        | select(.hooks | length > 0)]) | with_entries(select(.value | length > 0)))' \
      "$codex_hooks_file" >"$codex_hooks_file.tmp"
    mv "$codex_hooks_file.tmp" "$codex_hooks_file"
  elif [[ -f "$codex_hooks_file" ]]; then
    jq "$toolbox_hook_filter"'
      .hooks |= (map_values(map(select(toolbox_owned))) | with_entries(select(.value | length > 0)))
    ' "$codex_hooks_file" >"${codex_hooks_file}.tmp"
    mv "${codex_hooks_file}.tmp" "$codex_hooks_file"
  fi
  if [[ -f "$codex_hooks_file" && -f "$downstream_hooks" && ${TEMPLATE_SYNC_MERGE_DENY:-0} == 1 ]]; then
    if ! is_excluded "$downstream_hooks"; then
      local base_hooks=""
      if [[ -n $CODEX_BASE_DIR && -f $CODEX_BASE_DIR/hooks.json ]]; then base_hooks="$CODEX_BASE_DIR/hooks.json"; fi
      migration_json hooks-sync "$downstream_hooks" "$codex_hooks_file" "$MANIFEST_PATH" "$base_hooks" >"$codex_hooks_file.tmp"
      mv "$codex_hooks_file.tmp" "$codex_hooks_file"
    fi
  elif [[ -f "$codex_hooks_file" && -f "$downstream_hooks" ]]; then
    # Toolbox owns script entries under .codex/scripts/ except capy.sh; those
    # come from upstream verbatim, so a toolbox entry that changed or was
    # removed upstream does not linger. Every other downstream entry (capy's
    # `capy codex-launch` hooks, hand-added hooks) is appended after upstream's
    # entries for its event. Events only downstream knows about are kept whole.
    if jq --slurpfile upstream "$codex_hooks_file" "$toolbox_hook_filter"'
      (.hooks // {}) as $d
      | $upstream[0]
      | (.hooks // {}) as $u
      | ($u | keys_unsorted) as $events
      | .hooks = (reduce ($events + [($d | keys_unsorted)[] | select(. as $k | $events | index($k) | not)])[] as $event ({};
          ($u[$event] // []) as $entries
          | .[$event] = $entries + [($d[$event] // [])[]
              | select((toolbox_owned | not) and (. as $e | $entries | index($e) | not))]))
    ' "$downstream_hooks" >"${codex_hooks_file}.tmp"; then
      mv "${codex_hooks_file}.tmp" "$codex_hooks_file"
      log_info "Preserved downstream hook entries in hooks.json"
    else
      log_warn "Hooks merge failed — downstream .codex/hooks.json may contain invalid JSON"
      log_warn "Falling back to upstream template for hooks.json"
      rm -f "${codex_hooks_file}.tmp"
    fi
  fi

  log_success "Substitutions applied to $output_dir"
}

# copy_sync_files()
# Copies sync infrastructure files (workflow) from upstream to staging.
# These files are synced as-is without variable substitution.
# Note: template-sync.sh and other scripts are now under .claude/toolbox/scripts/
# and are synced as part of the .claude/ directory — no separate copy needed.
#
# Args:
#   $1 - Upstream directory (parent of .github/)
#   $2 - Output directory for staged files
#
# Returns:
#   0 on success
#
# Side effects:
#   Creates workflows/ subdirectory in output_dir
#   Copies template-sync.yml if it exists
copy_sync_files() {
  local upstream_dir="$1"
  local output_dir="$2"

  log_step "Copying sync infrastructure files"

  mkdir -p "$output_dir/workflows"

  local copied=0

  # Copy workflow if it exists
  if [[ -f "$upstream_dir/.github/workflows/template-sync.yml" ]]; then
    cp "$upstream_dir/.github/workflows/template-sync.yml" "$output_dir/workflows/"
    log_info "Copied template-sync.yml"
    copied=$((copied + 1))
  fi

  if ((copied > 0)); then
    log_success "Copied $copied sync infrastructure file(s)"
  else
    log_info "No sync infrastructure files found in upstream"
  fi
}

# =============================================================================
# File Comparison Functions
# =============================================================================

# compare_files()
# Compares staging directory against current project directories.
# Detects added, modified, deleted, and unchanged files.
#
# Args:
#   $1 - Staging directory containing substituted templates
#
# Returns:
#   0 on success
#
# Side effects:
#   Populates global arrays: ADDED_FILES, MODIFIED_FILES, DELETED_FILES, UNCHANGED_FILES
#   Logs comparison summary
#
# Directories compared:
#   staging/claude    -> .claude/
compare_files() {
  local staging_dir="$1"

  log_step "Comparing files with current project"

  # Reset arrays
  ADDED_FILES=()
  MODIFIED_FILES=()
  DELETED_FILES=()
  UNCHANGED_FILES=()
  EXCLUDED_FILES=()

  # Directories to compare (staging subdir -> project dir)
  local -A dir_map=(
    ["claude"]=".claude"
    ["codex"]=".codex"
    ["workflows"]=".github/workflows"
  )

  for staging_subdir in "${!dir_map[@]}"; do
    local project_dir="${dir_map[$staging_subdir]}"
    local staging_path="$staging_dir/$staging_subdir"

    # Skip if staging subdir doesn't exist
    [[ ! -d "$staging_path" ]] && continue

    local staging_find_args=("$staging_path" -type f -print0)

    # Find all files in staging (excluding user-scoped directories)
    while IFS= read -r -d '' staging_file; do
      local relative_path="${staging_file#$staging_path/}"
      local project_file="$project_dir/$relative_path"
      local display_path="$project_dir/$relative_path"

      # Check exclusion before categorization
      if is_excluded "$display_path"; then
        EXCLUDED_FILES+=("$display_path")
        continue
      fi

      if [[ ! -f "$project_file" ]]; then
        # File exists in staging but not in project -> Added
        ADDED_FILES+=("$display_path")
      elif ! diff -q "$staging_file" "$project_file" &>/dev/null; then
        # Files differ -> Modified
        MODIFIED_FILES+=("$display_path")
      else
        # Files are identical -> Unchanged
        UNCHANGED_FILES+=("$display_path")
      fi
    done < <(find "${staging_find_args[@]}" 2>/dev/null)

    # Find deleted files (exist in project but not in staging)
    # Skip for workflows/ — we only sync template-sync.yml, not the entire directory
    # Migration sync copies the staged files and runs the named migrations.
    # Only those migrations actually delete files; their plans are merged below.
    if [[ -d "$project_dir" && "$staging_subdir" != "workflows" && ${TEMPLATE_SYNC_MERGE_DENY:-0} != 1 ]]; then
      local find_args=("$project_dir" -type f -print0)

      while IFS= read -r -d '' project_file; do
        local relative_path="${project_file#$project_dir/}"
        local staging_file="$staging_path/$relative_path"
        local display_path="$project_dir/$relative_path"

        # Skip excluded files in deletion detection (don't add to EXCLUDED_FILES to avoid double-counting)
        if is_excluded "$display_path"; then
          continue
        fi

        if [[ ! -f "$staging_file" ]]; then
          # File exists in project but not in staging -> Deleted
          DELETED_FILES+=("$display_path")
        fi
      done < <(find "${find_args[@]}" 2>/dev/null)
    fi
  done

  log_success "Comparison complete: ${#ADDED_FILES[@]} added, ${#MODIFIED_FILES[@]} modified, ${#DELETED_FILES[@]} deleted, ${#UNCHANGED_FILES[@]} unchanged, ${#EXCLUDED_FILES[@]} excluded"
}

# generate_diff_report()
# Generates a human-readable diff report showing all changes.
# In CI mode, also outputs GitHub Actions compatible format.
#
# Args:
#   $1 - Staging directory containing substituted templates
#
# Returns:
#   0 on success
#
# Output:
#   - Human-readable report to stdout with colored output
#   - In CI mode: writes to GITHUB_OUTPUT file for workflow consumption
#   - Shows version transition, change summary, and file diffs
#
# Side effects:
#   Reads from global arrays (ADDED_FILES, MODIFIED_FILES, etc.)
#   Reads RESOLVED_VERSION global variable
generate_diff_report() {
  local staging_dir="$1"
  local total_changes=$((${#ADDED_FILES[@]} + ${#MODIFIED_FILES[@]} + ${#DELETED_FILES[@]}))
  local has_changes=false
  [[ $total_changes -gt 0 ]] && has_changes=true

  # CI mode: output GitHub Actions format
  if $CI_MODE; then
    if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
      # Write to GITHUB_OUTPUT file
      {
        echo "has_changes=$has_changes"
        echo "added_count=${#ADDED_FILES[@]}"
        echo "modified_count=${#MODIFIED_FILES[@]}"
        echo "deleted_count=${#DELETED_FILES[@]}"
        echo "unchanged_count=${#UNCHANGED_FILES[@]}"
        echo "excluded_count=${#EXCLUDED_FILES[@]}"
        echo "dropped_deny_count=${#DROPPED_DENY_ENTRIES[@]}"
        echo "total_changes=$total_changes"
        echo "resolved_version=$RESOLVED_VERSION"
        echo "plugin_migrated=$PLUGIN_MIGRATED"
        echo "diff_summary<<EOF"
        generate_markdown_summary "$staging_dir"
        echo "EOF"
      } >>"$GITHUB_OUTPUT"
    else
      # Output to stdout for local testing
      echo "::group::GitHub Actions Outputs"
      echo "has_changes=$has_changes"
      echo "added_count=${#ADDED_FILES[@]}"
      echo "modified_count=${#MODIFIED_FILES[@]}"
      echo "deleted_count=${#DELETED_FILES[@]}"
      echo "unchanged_count=${#UNCHANGED_FILES[@]}"
      echo "excluded_count=${#EXCLUDED_FILES[@]}"
      echo "dropped_deny_count=${#DROPPED_DENY_ENTRIES[@]}"
      echo "total_changes=$total_changes"
      echo "resolved_version=$RESOLVED_VERSION"
      echo "::endgroup::"
    fi
  fi

  # Human-readable output
  echo ""
  echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
  echo -e "${BOLD}                    Template Sync Report                        ${NC}"
  echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
  echo ""

  local current_version
  current_version=$(get_manifest_value '.template_version')
  echo -e "  ${CYAN}From:${NC} $current_version"
  echo -e "  ${CYAN}To:${NC}   $RESOLVED_VERSION"
  echo ""

  if ! $has_changes; then
    echo -e "  ${GREEN}No changes detected - templates are up to date${NC}"
    echo ""
    # A kept project value can be the only outcome of an upstream change
    print_settings_conflicts
    return
  fi

  echo -e "  ${CYAN}Summary:${NC}"
  echo -e "    Added:     ${GREEN}${#ADDED_FILES[@]}${NC}"
  echo -e "    Modified:  ${YELLOW}${#MODIFIED_FILES[@]}${NC}"
  echo -e "    Deleted:   ${RED}${#DELETED_FILES[@]}${NC}"
  echo -e "    Unchanged: ${#UNCHANGED_FILES[@]}"
  echo -e "    Excluded:  ${#EXCLUDED_FILES[@]}"
  echo ""

  # List added files
  if [[ ${#ADDED_FILES[@]} -gt 0 ]]; then
    echo -e "  ${GREEN}Added files:${NC}"
    for file in "${ADDED_FILES[@]}"; do
      echo -e "    ${GREEN}+${NC} $file"
    done
    echo ""
  fi

  # List modified files with inline diffs
  if [[ ${#MODIFIED_FILES[@]} -gt 0 ]]; then
    echo -e "  ${YELLOW}Modified files:${NC}"
    for file in "${MODIFIED_FILES[@]}"; do
      echo -e "    ${YELLOW}~${NC} $file"
    done
    echo ""

    # Show diffs for modified files (limited to first 20 lines each)
    if ! $CI_MODE || [[ ${TEMPLATE_SYNC_MERGE_DENY:-0} == 1 && $DRY_RUN == true ]]; then
      echo -e "  ${CYAN}Diffs:${NC}"
      for file in "${MODIFIED_FILES[@]}"; do
        local staging_file
        # Map project path back to staging path
        if [[ "$file" == ".claude/"* || "$file" == ".codex/"* ]]; then
          staging_file="$staging_dir/${file#.}"
        else
          staging_file="$staging_dir/$file"
        fi

        if [[ -f "$staging_file" && -f "$file" ]]; then
          echo ""
          echo -e "    ${BOLD}--- $file${NC}"
          diff -u "$file" "$staging_file" 2>/dev/null | head -30 | sed 's/^/    /' || true
        fi
      done
      echo ""
    fi
  fi

  # List deleted files
  if [[ ${#DELETED_FILES[@]} -gt 0 ]]; then
    echo -e "  ${RED}Deleted files:${NC}"
    for file in "${DELETED_FILES[@]}"; do
      echo -e "    ${RED}-${NC} $file"
    done
    echo ""
  fi

  # List excluded files
  if [[ ${#EXCLUDED_FILES[@]} -gt 0 ]]; then
    echo -e "  ${CYAN}Excluded files (via sync_exclusions):${NC}"
    for file in "${EXCLUDED_FILES[@]}"; do
      echo -e "    ${CYAN}○${NC} $file"
    done
    echo ""
  fi

  if [[ ${#DROPPED_DENY_ENTRIES[@]} -gt 0 ]]; then
    echo "  Permission deny entries removed:"
    local entry
    for entry in "${DROPPED_DENY_ENTRIES[@]}"; do
      printf '    - %s\n' "$entry"
    done
    echo ""
    permission_deny_guidance
    echo ""
  fi

  if [[ ${#SETTINGS_REMOVED_ENTRIES[@]} -gt 0 ]]; then
    echo "  Settings entries removed upstream:"
    local entry
    for entry in "${SETTINGS_REMOVED_ENTRIES[@]}"; do
      printf '    - %s\n' "$entry"
    done
    echo ""
  fi

  print_settings_conflicts

  if [[ -n "$SETTINGS_BASE_WARNING" ]]; then
    echo "  $SETTINGS_BASE_WARNING"
    echo ""
  fi

  echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
  echo ""

  if $DRY_RUN; then
    echo -e "  ${YELLOW}Dry run mode - no changes applied${NC}"
    echo -e "  Run without --dry-run to apply these changes"
    echo ""
  fi
}

# Terminal list of settings values kept over upstream changes or removals.
print_settings_conflicts() {
  [[ ${#SETTINGS_CONFLICT_ENTRIES[@]} -gt 0 ]] || return 0
  echo "  Settings kept with project values (upstream changed or removed them):"
  local entry
  for entry in "${SETTINGS_CONFLICT_ENTRIES[@]}"; do
    printf '    - %s\n' "$entry"
  done
  echo ""
}

# Shared guidance for terminal reports and PR summaries.
permission_deny_guidance() {
  echo 'Put project secrets globs in `.claude/kk-guard.json` under `secrets` and destructive rules under `destructive`.'
  echo 'For full control of settings, add `.claude/settings.json` to `sync_exclusions` in `.github/template-state.json`.'
}

# Generate markdown summary for PR body
generate_markdown_summary() {
  local staging_dir="$1"
  local current_version
  current_version=$(get_manifest_value '.template_version')

  echo "## Template Sync Summary"
  echo ""
  echo "**From:** \`$current_version\`"
  echo "**To:** \`$RESOLVED_VERSION\`"
  echo ""
  echo "### Changes"
  echo ""
  echo "| Type | Count |"
  echo "|------|-------|"
  echo "| Added | ${#ADDED_FILES[@]} |"
  echo "| Modified | ${#MODIFIED_FILES[@]} |"
  echo "| Deleted | ${#DELETED_FILES[@]} |"
  echo "| Excluded | ${#EXCLUDED_FILES[@]} |"
  echo ""

  if [[ ${#ADDED_FILES[@]} -gt 0 ]]; then
    echo "### Added Files"
    echo ""
    for file in "${ADDED_FILES[@]}"; do
      echo "- \`$file\`"
    done
    echo ""
  fi

  if [[ ${#MODIFIED_FILES[@]} -gt 0 ]]; then
    echo "### Modified Files"
    echo ""
    for file in "${MODIFIED_FILES[@]}"; do
      echo "- \`$file\`"
    done
    echo ""
  fi

  if [[ ${#DELETED_FILES[@]} -gt 0 ]]; then
    echo "### Deleted Files"
    echo ""
    for file in "${DELETED_FILES[@]}"; do
      echo "- \`$file\`"
    done
    echo ""
  fi

  if [[ ${#EXCLUDED_FILES[@]} -gt 0 ]]; then
    echo "### Excluded Files"
    echo ""
    echo "_These files were skipped due to \`sync_exclusions\` patterns in the manifest:_"
    echo ""
    for file in "${EXCLUDED_FILES[@]}"; do
      echo "- \`$file\`"
    done
    echo ""
  fi

  if [[ ${#DROPPED_DENY_ENTRIES[@]} -gt 0 ]]; then
    echo "### Permission deny entries removed"
    echo ""
    local entry
    for entry in "${DROPPED_DENY_ENTRIES[@]}"; do
      printf -- '- `%s`\n' "$entry"
    done
    echo ""
    permission_deny_guidance
    echo ""
  fi

  if [[ ${#SETTINGS_REMOVED_ENTRIES[@]} -gt 0 ]]; then
    local entry
    echo "### Settings entries removed upstream"
    echo ""
    echo "_Upstream removed these \`.claude/settings.json\` entries and this project had not changed them. Restore any you still need in this branch._"
    echo ""
    for entry in "${SETTINGS_REMOVED_ENTRIES[@]}"; do
      printf -- '- `%s`\n' "$entry"
    done
    echo ""
  fi

  if [[ ${#SETTINGS_CONFLICT_ENTRIES[@]} -gt 0 ]]; then
    local entry
    echo "### Settings kept with project values"
    echo ""
    echo "_Upstream changed or removed these \`.claude/settings.json\` values, but this project had customized them, so the project values were kept._"
    echo ""
    for entry in "${SETTINGS_CONFLICT_ENTRIES[@]}"; do
      printf -- '- `%s`\n' "$entry"
    done
    echo ""
  fi

  if [[ -n "$SETTINGS_BASE_WARNING" ]]; then
    echo "### Settings merged without a base"
    echo ""
    echo "$SETTINGS_BASE_WARNING."
    echo ""
  fi

  if $PLUGIN_MIGRATED; then
    echo "### Plugin Migration"
    echo ""
    echo "Skills, commands, and hooks have been migrated to the **kk** plugin."
    echo "Template-managed files listed under \"Deleted Files\" above were removed."
    echo ""
    echo "**After merging this PR:**"
    echo "1. Run \`/plugin install kk@claude-toolbox\` to install the plugin"
    echo "2. Commands are now namespaced: \`/project:command\` → \`/kk:dir:command\` (skills remain unprefixed)"
    echo ""
  fi

  local serena_deleted=false
  for file in "${DELETED_FILES[@]}"; do
    if [[ "$file" == ".serena/"* || "$file" == ".serena/" ]]; then
      serena_deleted=true
      break
    fi
  done
  if $serena_deleted; then
    echo "### Serena Removed"
    echo ""
    echo "Serena MCP has been removed from the template defaults."
    echo "The \`.serena/\` directory and \`SERENA_INITIAL_PROMPT\` manifest variable have been cleaned up."
    echo ""
    echo "If you still want to use Serena, configure it at the user level in \`~/.claude.json\`."
    echo ""
  fi
}

# =============================================================================
# Apply Changes (consolidates all mutations the YAML used to do inline)
# =============================================================================

# apply_wiring()
# Wires the root CLAUDE.md @import references (CLAUDE.extra.md and
# toolbox/CLAUDE.md) and cleans up the obsolete "# Extra Instructions" header.
#
# The root CLAUDE.md is NOT a tracked template file, so its @import state is
# independent of the template diff. This function must therefore run even when
# `compare_files` reports zero changes (e.g. a re-run after the manifest version
# was already bumped) — otherwise a newly-introduced @import can never land.
# apply_changes() calls it on every apply; main() also calls it on the
# 0-change local path.
#
# Args:
#   $1 - Staging directory containing substituted templates
#
# Side effects:
#   Mutates the working tree's root CLAUDE.md (idempotent — guarded by grep)
apply_wiring() {
  local staging_dir="$1"
  if migration_excluded CLAUDE.md; then return 0; fi

  # Cleanup obsolete header
  if grep -q '^# Extra Instructions$' CLAUDE.md 2>/dev/null; then
    sed_inplace 's/^# Extra Instructions$//' CLAUDE.md
  fi

  # --- Auto-import CLAUDE.extra.md ---
  if [[ -f "$staging_dir/claude/CLAUDE.extra.md" && -f "CLAUDE.md" ]]; then
    if ! grep -q '@.claude/CLAUDE.extra.md' CLAUDE.md; then
      printf '@.claude/CLAUDE.extra.md\n' >>CLAUDE.md
      log_info "Added @import reference for .claude/CLAUDE.extra.md to CLAUDE.md"
    fi
  fi

  # --- Auto-import .claude/toolbox/CLAUDE.md ---
  if [[ -f "$staging_dir/claude/toolbox/CLAUDE.md" && -f "CLAUDE.md" ]]; then
    if ! grep -q '@.claude/toolbox/CLAUDE.md' CLAUDE.md; then
      # Keep the import next to the CLAUDE.extra.md one when it exists
      if grep -q '^@\.claude/CLAUDE\.extra\.md$' CLAUDE.md; then
        sed_inplace '/^@\.claude\/CLAUDE\.extra\.md$/a\
@.claude/toolbox/CLAUDE.md' CLAUDE.md
      else
        printf '\n@.claude/toolbox/CLAUDE.md\n' >>CLAUDE.md
      fi
      log_info "Added @import reference for .claude/toolbox/CLAUDE.md to CLAUDE.md"
    fi
  fi
}

# apply_changes()
# Applies all staged changes to the working tree: copies files, runs
# migrations, patches gitignore, auto-imports CLAUDE.extra.md, and
# updates the manifest version.
#
# Args:
#   $1 - Staging directory containing substituted templates
#   $2 - Resolved version string to write into the manifest
#
# Side effects:
#   Mutates working tree files, updates manifest
apply_changes() {
  local staging_dir="$1"
  local new_version="$2"

  log_step "Applying staged changes"

  # --- Copy staged files into working tree ---
  # NOTE: this cp overwrites .claude/toolbox/scripts/template-sync.sh in place.
  # That is safe only because (a) main() hands off to the upstream copy of the
  # script before reaching this point whenever the two differ, so the process
  # executing here runs from $STAGING_DIR/bin, not from the file being
  # overwritten (see handoff_to_upstream_script), and (b) the entry-point guard
  # at the bottom of this file exits immediately after main() returns, so even
  # with the handoff disabled bash never reads past the overwritten file's
  # stale byte offset.
  local -A dir_map=(
    ["claude"]=".claude"
    ["codex"]=".codex"
    ["workflows"]=".github/workflows"
    ["scripts"]=".github/scripts"
    ["docs"]="docs"
  )

  for staging_subdir in "${!dir_map[@]}"; do
    local source="$staging_dir/$staging_subdir"
    local target="${dir_map[$staging_subdir]}"
    [[ ! -d "$source" ]] && continue
    # Comparison exclusions must also govern apply (including CI's separate
    # --apply invocation). Copy entries individually so excluded descendants
    # cannot slip through a recursive directory copy.
    local staged_entry relative_path destination
    while IFS= read -r -d '' staged_entry; do
      relative_path="${staged_entry#$source/}"
      destination="$target/$relative_path"
      if is_excluded "$destination"; then
        continue
      fi
      if [[ -d "$staged_entry" && ! -L "$staged_entry" ]]; then
        mkdir -p "$destination"
      else
        mkdir -p "$(dirname "$destination")"
        cp -P "$staged_entry" "$destination"
      fi
    done < <(find "$source" -mindepth 1 -print0)
    log_info "Applied changes to $target/"
  done

  # Restore executable permissions on scripts
  if [[ ${TEMPLATE_SYNC_MERGE_DENY:-0} == 1 ]]; then
    local script
    for script in "$staging_dir"/codex/scripts/*.sh "$staging_dir"/scripts/*.sh; do
      [[ -f $script ]] || continue
      case $script in
      "$staging_dir"/codex/*) destination=.${script#"$staging_dir/"} ;;
      *) destination=.github/${script#"$staging_dir/"} ;;
      esac
      if ! is_excluded "$destination"; then chmod +x "$destination"; fi
    done
  else
    chmod +x .codex/scripts/*.sh 2>/dev/null || true
    chmod +x .github/scripts/*.sh 2>/dev/null || true
  fi

  # --- Run migrations ---
  local upstream_dir
  upstream_dir="$(dirname "$staging_dir")/upstream"
  if needs_plugin_migration "$upstream_dir"; then
    run_plugin_migration
  fi

  if needs_serena_removal; then
    run_serena_removal
  fi

  if needs_script_consolidation; then
    run_script_consolidation
  fi

  if needs_docs_feat_migration; then
    run_docs_feat_migration
  fi

  # --- Patch .gitignore for .codex ---
  if [[ -d "$staging_dir/codex" && -f ".gitignore" ]] && ! migration_excluded .gitignore; then
    if git check-ignore -q .codex 2>/dev/null; then
      if ! grep -q '^!\.codex' .gitignore; then
        if grep -q '^!\.claude' .gitignore; then
          sed_inplace '/^!\.claude$/a\
!.codex' .gitignore
        else
          printf '!.codex\n' >>.gitignore
        fi
        log_info "Added !.codex to .gitignore (was excluded by .* pattern)"
      fi
    fi
  fi

  # --- Wire root CLAUDE.md @imports ---
  # Independent of template file diffs (CLAUDE.md is not a tracked template),
  # so this also runs from main() on 0-change re-runs. See apply_wiring().
  apply_wiring "$staging_dir"

  # --- Update manifest version ---
  local synced_at
  synced_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  migrate_manifest
  backfill_manifest_variables

  if json_update "$MANIFEST_PATH" \
    '.template_version = $version | .synced_at = $synced_at' \
    --arg version "$new_version" --arg synced_at "$synced_at"; then
    log_info "Updated manifest to version $new_version"
  else
    log_warn "Failed to update manifest version"
  fi

  log_success "All changes applied"
}

# =============================================================================
# Retirement
# =============================================================================

retirement_regular_file() {
  local candidate=$1
  while [[ $candidate != . ]]; do
    [[ ! -L $candidate ]] || return 1
    if [[ $candidate != */* ]]; then break; fi
    candidate=${candidate%/*}
  done
  [[ -f $1 ]]
}

retire_template() {
  local upstream manifest stage clean rendered before after model choice
  local part file target template relative parent key
  local -a files=() infrastructure=()
  upstream=$(get_manifest_value '.upstream_repo')
  manifest="$(pwd -P)/$MANIFEST_PATH"
  mkdir -p -- "$STAGING_DIR"
  stage=$(mktemp -d "$(cd "$STAGING_DIR" && pwd -P)/retirement.XXXXXXXX")
  # When the caller supplied --output-dir, only our private snapshot is ours
  # to clean up. The ordinary temporary staging root already has an exit trap.
  if [[ -z $TEMP_DIR ]]; then TEMP_DIR=$stage; fi
  clean="$stage/empty" rendered="$stage/rendered" before="$stage/before" after="$stage/after"
  mkdir -p "$clean" "$before" "$after"
  fetch_upstream_templates "refs/tags/$TARGET_VERSION" "$upstream" "$stage"
  # Use first-install substitutions. Running from an empty project prevents
  # local hooks, MCP registrations and settings from becoming deletion evidence.
  (
    cd "$clean"
    MANIFEST_PATH=$manifest apply_substitutions "$FETCHED_TEMPLATES_PATH" "$rendered"
  )
  copy_sync_files "$stage/upstream" "$rendered"
  model=$(get_manifest_value '.variables.CODEX_MODEL // ""')
  choice=$(get_manifest_value '.variables.CC_STATUSLINE // "enhanced"')
  log_step "Retirement of the repository template at $TARGET_VERSION"
  echo "Committing this change affects everyone using this repository. Collaborators without kk lose the Codex guard and the repository deny list."
  echo "Cloud sessions and CI runners relying on committed plugin enablement lose the plugin. Installing kk alone does not restore native denies to unwrapped Claude sessions."
  echo "Repository Codex native forbids return only on machines that enabled the account-wide rules file."
  echo "Kept repository settings outrank machine defaults. To hand Codex sandbox and approvals to the machine, delete the sandbox_mode, approval_policy and approvals_reviewer lines from .codex/config.toml."
  echo "Manifest statusline choice: $choice."
  for key in CC_MODEL CC_EFFORT_LEVEL CC_PERMISSION_MODE CODEX_MODEL; do
    local value
    value=$(get_manifest_value ".variables.$key // \"\"")
    case "$key=$value" in *=|CC_MODEL=default|CC_EFFORT_LEVEL=high|CC_PERMISSION_MODE=default|CODEX_MODEL=gpt-6.2-astra) continue ;; esac
    printf 'Manifest choice: %s = %s (kept when present).\n' "$key" "$value"
  done

  for file in .claude/CLAUDE.*.md; do
    if [[ -f $file && $file != .claude/CLAUDE.extra.md ]]; then
      printf 'Keep %s. Codex stops receiving it unless AGENTS.md contains @%s.\n' "$file" "$file"
    fi
  done
  # Report excluded project-only files too, even if the template contains no
  # corresponding path. Never follow a link into another checkout.
  for part in .claude .codex .github CLAUDE.md; do
    [[ -e $part || -L $part ]] || continue
    while IFS= read -r -d '' file; do
      if is_excluded "$file"; then printf 'Excluded: %s\n' "$file"; fi
    done < <(find "$part" \( -type f -o -type l \) -print0)
  done

  for part in claude codex workflows; do
    [[ -d $rendered/$part ]] || continue
    case "$part" in workflows) target=.github/workflows ;; *) target=.$part ;; esac
    while IFS= read -r -d '' template; do
      relative=${template#"$rendered/$part/"}
      file="$target/$relative"
      if is_excluded "$file" || [[ ! -e $file && ! -L $file ]]; then continue; fi
      if ! retirement_regular_file "$file" || [[ -L $template ]]; then
        printf 'Keep non-regular or linked path: %s\n' "$file"
        continue
      fi
      case "$file" in .claude/CLAUDE.extra.md) ;; .claude/CLAUDE.*.md) continue ;; esac
      parent=${file%/*}
      mkdir -p "$before/$parent" "$after/$parent"
      cp -p -- "$file" "$before/$file"
      case "$file" in
      .claude/settings.json)
        migration_json settings-retire "$file" "$template" "$manifest" "" >"$after/$file" ;;
      .codex/hooks.json)
        migration_json hooks-retire "$file" "$template" "$manifest" "" >"$after/$file" ;;
      .codex/config.toml)
        codex_toml retire "$file" "$template" "" "$model" >"$after/$file" ;;
      *)
        if ! cmp -s "$file" "$template"; then
          printf 'Keep changed file: %s\n' "$file"
          continue
        fi ;;
      esac
      if [[ -f $after/$file ]] && cmp -s "$file" "$after/$file"; then continue; fi
      case "$file" in
      .github/workflows/template-sync.yml|.claude/toolbox/scripts/template-sync.sh|.claude/toolbox/scripts/semver-compare.sh|.claude/toolbox/scripts/sync-workflow.sh)
        infrastructure+=("$file") ;;
      *) files+=("$file") ;;
      esac
    done < <(find "$rendered/$part" \( -type f -o -type l \) -print0)
  done

  # Plan from the registrations that will survive, independent of find order.
  # Keep the runtime together because its handlers source sibling scripts.
  local hooks=.codex/hooks.json keep_runtime=false
  if [[ -e $hooks || -L $hooks ]]; then
    if is_excluded "$hooks" || ! retirement_regular_file "$hooks"; then
      keep_runtime=true
    else
      local remaining=$after/$hooks
      [[ -f $remaining ]] || remaining=$hooks
      if [[ -s $remaining ]]; then
        keep_runtime=$(jq -r 'any(.hooks[]?[]?.hooks[]?; (.command? // "") | test("[.]codex/scripts([^[:alnum:]_.-]|$)"))' "$remaining")
      fi
    fi
  fi
  if [[ $keep_runtime == true ]]; then
    local -a filtered=()
    for file in "${files[@]}"; do
      if [[ $file == .codex/scripts/* ]]; then
        printf 'Keep %s for retained %s\n' "$file" "$hooks"
      else
        filtered+=("$file")
      fi
    done
    files=("${filtered[@]}")
  fi
  if ! is_excluded "$MANIFEST_PATH" && retirement_regular_file "$MANIFEST_PATH"; then
    mkdir -p "$before/.github"
    cp -p "$MANIFEST_PATH" "$before/$MANIFEST_PATH"
    infrastructure+=("$MANIFEST_PATH")
  fi
  if retirement_regular_file CLAUDE.md && ! is_excluded CLAUDE.md; then
    cp -p CLAUDE.md "$before/CLAUDE.md"
  fi
  for file in "${files[@]}" "${infrastructure[@]}"; do
    if [[ ! -s $after/$file ]]; then printf '%s\0' "$file"; fi
  done >"$stage/removals"
  python3 -I - "$before/CLAUDE.md" "$after/CLAUDE.md" "$stage/removals" "$stage/upstream/CLAUDE.md" <<'PY'
import os
from pathlib import Path
import sys

source, output, plan, template = map(Path, sys.argv[1:])
removed = {Path(os.fsdecode(name)).resolve() for name in plan.read_bytes().split(b"\0") if name}
lines = source.read_bytes().splitlines(keepends=True) if source.exists() else []
present = {line.rstrip(b"\r\n") for line in lines}
drop = set()
for name in (".claude/CLAUDE.extra.md", ".claude/toolbox/CLAUDE.md"):
    target = Path(name)
    line = ("@" + name).encode()
    if not target.is_file() or target.resolve() in removed:
        drop.add(line)
        continue
    if name == ".claude/CLAUDE.extra.md":
        print("Keep {}. Codex stops receiving it unless AGENTS.md contains @{}.".format(name, name))
    if line in present:
        print("Keep @{} in CLAUDE.md. Claude will continue loading the retained file.".format(name))
if source.exists():
    # The stock file separates each import with a blank line. In customized
    # files only the import itself can be attributed to the template.
    stock_layout = (not template.is_symlink() and template.is_file()
                    and template.read_bytes().splitlines() == [line.rstrip(b"\r\n") for line in lines])
    kept = []
    for line in lines:
        if line.rstrip(b"\r\n") in drop:
            if stock_layout and kept and kept[-1] in (b"\n", b"\r\n"):
                kept.pop()
        else:
            kept.append(line)
    output.write_bytes(b"".join(kept))
PY
  if [[ -f $before/CLAUDE.md ]] && ! cmp -s "$before/CLAUDE.md" "$after/CLAUDE.md"; then
    files+=(CLAUDE.md)
  fi

  # Finish parsing and planning before making any repository change. Apply
  # configuration edits first; the manifest is the final removal on success.
  for file in "${files[@]}" "${infrastructure[@]}"; do
    if [[ -s $after/$file || $file == CLAUDE.md ]]; then
      printf 'Edit %s\n' "$file"
      diff -u -- "$before/$file" "$after/$file" || [[ $? == 1 ]]
    else
      printf 'Remove %s\n' "$file"
    fi
    if $DRY_RUN; then continue; fi
    if ! retirement_regular_file "$file" || ! cmp -s "$before/$file" "$file"; then
      log_error "File changed during retirement: $file"
      return 1
    fi
    if [[ -s $after/$file || $file == CLAUDE.md ]]; then
      local replacement
      replacement=$(mktemp "$file.XXXXXXXX")
      cp -p -- "$before/$file" "$replacement"
      cat "$after/$file" >"$replacement"
      mv -- "$replacement" "$file"
    else
      rm -- "$file"
    fi
  done
}

# =============================================================================
# Help / Usage
# =============================================================================

show_help() {
  cat <<'EOF'
Template Sync Script
Synchronizes template updates from the upstream claude-toolbox repository.

Usage:
  ./template-sync.sh                    # Sync to latest version
  ./template-sync.sh [options]          # Sync with custom options

Options:
  --version VERSION     Target version to sync to
                        - "latest": Most recent tagged release (default)
                        - "main": Latest from main branch
                        - "v1.2.3": Specific tag
                        - SHA: Specific commit
  --dry-run             Preview changes without applying them
  --local               Fetch, compare, and apply in a single invocation
  --retire              Compare with the explicit retirement tag and remove template-owned
                        entries. Use --dry-run to preview. For migration use kk migrate.
  --apply               Apply pre-staged changes to the working tree (CI only)
  --ci                  CI mode: outputs GitHub Actions compatible format
  --output-dir DIR      Directory to stage changes (default: temporary directory)
  -h, --help            Show this help message

Environment:
  TEMPLATE_SYNC_NO_HANDOFF=1
                        Run this script as-is instead of handing off to the
                        target version's copy when the two differ
  TEMPLATE_SYNC_MERGE_DENY=1
                        Prepare a migration: merge project deny entries and
                        preserve adopter-owned Codex settings and hook handlers.

Requires: jq, git, curl, yq (mikefarah/yq), python3 (standard library only)

Exit Codes:
  0 - Success (changes found or no changes)
  1 - Operational error (missing manifest, network failure, invalid JSON)
  2 - Invalid CLI arguments

Examples:
  # Preview changes without applying
  ./template-sync.sh --dry-run

  # Sync to latest release and apply locally
  ./template-sync.sh --local

  # Sync to specific version and apply locally
  ./template-sync.sh --local --version v1.0.0

  # CI mode with custom output directory
  ./template-sync.sh --ci --output-dir ./staging
EOF
}

# =============================================================================
# CLI Argument Parsing
# =============================================================================

parse_arguments() {
  while [[ $# -gt 0 ]]; do
    case $1 in
    --version)
      if [[ -z "${2:-}" ]]; then
        log_error "--version requires a value"
        exit 2
      fi
      TARGET_VERSION="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --apply)
      APPLY_MODE=true
      shift
      ;;
    --local)
      LOCAL_MODE=true
      shift
      ;;
    --retire)
      RETIRE_MODE=true
      shift
      ;;
    --ci)
      CI_MODE=true
      shift
      ;;
    --output-dir)
      if [[ -z "${2:-}" ]]; then
        log_error "--output-dir requires a value"
        exit 2
      fi
      STAGING_DIR="$2"
      shift 2
      ;;
    -h | --help)
      show_help
      exit 0
      ;;
    -*)
      log_error "Unknown option: $1"
      echo ""
      show_help
      exit 2
      ;;
    *)
      log_error "Unexpected argument: $1"
      echo ""
      show_help
      exit 2
      ;;
    esac
  done
}

# =============================================================================
# Main Entry Point
# =============================================================================

main() {
  # Register cleanup trap early for signal handling
  trap cleanup_on_exit EXIT INT TERM

  # Parse CLI arguments (before dependency check so APPLY_MODE is set)
  parse_arguments "$@"
  # Retirement uses an explicit tag. Even a standalone preview must not
  # bootstrap a missing helper into the repository.
  if ! $RETIRE_MODE; then load_semver; fi

  if $RETIRE_MODE && { $APPLY_MODE || $LOCAL_MODE || [[ ! $TARGET_VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+([+-][0-9A-Za-z.+-]+)?$ ]]; }; then
    log_error "--retire requires --version <retirement-tag> and runs separately from --apply and --local"
    exit 2
  fi

  # Check dependencies (applies mode-aware checks)
  check_dependencies

  # Apply mode requires an explicit staging directory
  if $APPLY_MODE && [[ -z "$STAGING_DIR" ]]; then
    log_error "--apply requires --output-dir to locate staged changes"
    exit 2
  fi

  # Set default staging directory if not provided (non-apply mode only)
  if [[ -z "$STAGING_DIR" ]]; then
    STAGING_DIR=$(mktemp -d "/tmp/template-sync.XXXXXX")
    # Track temp directory for cleanup
    TEMP_DIR="$STAGING_DIR"
    if [[ ! -d "$STAGING_DIR" ]]; then
      log_error "Failed to create temporary directory"
      exit 1
    fi
  fi

  # Display configuration in non-CI mode
  if ! $CI_MODE; then
    echo ""
    echo -e "${BOLD}Template Sync${NC}"
    echo "  Target version: $TARGET_VERSION"
    echo "  Dry run:        $DRY_RUN"
    echo "  Staging dir:    $STAGING_DIR"
    echo ""
  fi

  # Read and validate manifest
  read_manifest
  validate_manifest

  if $RETIRE_MODE; then
    retire_template
    return
  fi
  if [[ ${TEMPLATE_SYNC_MERGE_DENY:-0} == 1 ]] && { $DRY_RUN || is_excluded "$MANIFEST_PATH"; }; then
    if is_excluded "$MANIFEST_PATH"; then log_info "Excluded: $MANIFEST_PATH"; fi
    mkdir -p "$STAGING_DIR"
    local scratch_manifest
    scratch_manifest=$(mktemp "$STAGING_DIR/migration-manifest.XXXXXXXX")
    cp "$MANIFEST_PATH" "$scratch_manifest"
    MANIFEST_PATH=$scratch_manifest
  fi

  # Apply mode: skip fetch/compare/report, just apply staged changes.
  # The staged tree may carry a newer sync script — let it do the applying.
  if $APPLY_MODE; then
    handoff_to_upstream_script "$STAGING_DIR/substituted" "$@"
    log_info "To retire this repository's template after installing kk, run kk migrate."
    apply_changes "$STAGING_DIR/substituted" "$TARGET_VERSION"
    return 0
  fi

  migrate_manifest
  backfill_manifest_variables

  # Display manifest info
  if ! $CI_MODE; then
    local upstream_repo template_version project_name
    upstream_repo=$(get_manifest_value '.upstream_repo')
    template_version=$(get_manifest_value '.template_version')
    project_name=$(get_manifest_value '.variables.PROJECT_NAME')
    echo "  Upstream repo:  $upstream_repo"
    echo "  Current ver:    $template_version"
    echo "  Project name:   $project_name"
    echo ""
  fi

  # Get upstream repo from manifest
  local upstream_repo
  upstream_repo=$(get_manifest_value '.upstream_repo')

  # Resolve target version
  log_step "Resolving version: $TARGET_VERSION"
  RESOLVED_VERSION=$(resolve_version "$TARGET_VERSION" "$upstream_repo")
  log_info "Resolved version: $RESOLVED_VERSION"

  # Fetch upstream templates (sets FETCHED_TEMPLATES_PATH)
  local fetch_ref=$RESOLVED_VERSION
  if [[ ${TEMPLATE_SYNC_MERGE_DENY:-0} == 1 ]]; then fetch_ref="refs/tags/$RESOLVED_VERSION"; fi
  fetch_upstream_templates "$fetch_ref" "$upstream_repo" "$STAGING_DIR"

  # If the fetched version ships a different sync script, let that version
  # drive the rest of the run. Must happen before any migration/compare/apply
  # step so the working tree is still in its pre-sync state for the new script.
  handoff_to_upstream_script "$FETCHED_TEMPLATES_PATH" "$@"
  log_info "To retire this repository's template after installing kk, run kk migrate."

  # Display fetched templates info
  if ! $CI_MODE; then
    echo ""
    echo "  Templates path: $FETCHED_TEMPLATES_PATH"
    echo ""
  fi

  # Run plugin migration if needed (before comparing files)
  if needs_plugin_migration "$STAGING_DIR/upstream"; then
    PLUGIN_MIGRATED=true
    run_plugin_migration
  fi

  # Remove Serena artifacts if still present (upstream dropped Serena)
  if needs_serena_removal; then
    run_serena_removal
  fi

  if needs_script_consolidation; then
    run_script_consolidation
  fi

  if needs_docs_feat_migration; then
    run_docs_feat_migration
  fi

  # Excluded or first-time settings are not merged, so they need no base
  if [[ -f ".claude/settings.json" ]] && ! is_excluded ".claude/settings.json"; then
    fetch_settings_base "$(get_manifest_value '.template_version')" \
      "$FETCHED_TEMPLATES_PATH" "$STAGING_DIR/upstream" "$STAGING_DIR"
  fi

  if [[ ${TEMPLATE_SYNC_MERGE_DENY:-0} == 1 ]]; then
    local previous ref item
    previous=$(get_manifest_value '.template_version')
    CODEX_BASE_DIR="$STAGING_DIR/codex-base"
    mkdir -p "$CODEX_BASE_DIR"
    ref="refs/tags/$previous"
    if [[ $previous =~ ^[0-9a-f]{40}$ ]]; then ref="$previous"; fi
    if git -C "$STAGING_DIR/upstream" fetch --quiet --depth 1 origin "$ref" 2>/dev/null; then
      for item in hooks.json config.toml; do
        if git -C "$STAGING_DIR/upstream" cat-file -e "FETCH_HEAD:.codex/$item" 2>/dev/null; then
          git -C "$STAGING_DIR/upstream" show "FETCH_HEAD:.codex/$item" >"$CODEX_BASE_DIR/$item"
        elif [[ -f .codex/$item ]] && ! is_excluded ".codex/$item"; then
          log_warn "No previous .codex/$item at $previous; unmatched repository entries will be kept."
        fi
      done
    else
      log_warn "No Codex base fetched at $previous; unmatched repository settings and hooks will be kept."
    fi
  fi

  # Apply substitutions to fetched templates
  SUBSTITUTED_TEMPLATES_PATH="$STAGING_DIR/substituted"
  apply_substitutions "$FETCHED_TEMPLATES_PATH" "$SUBSTITUTED_TEMPLATES_PATH"

  # Copy sync infrastructure files (no substitution needed)
  copy_sync_files "$STAGING_DIR/upstream" "$SUBSTITUTED_TEMPLATES_PATH"

  # Display substituted templates info
  if ! $CI_MODE; then
    echo ""
    echo "  Substituted to: $SUBSTITUTED_TEMPLATES_PATH"
    echo ""
  fi

  # Compare files and generate report
  # Save pre-compare deletions (from migrations, consolidation, etc.)
  # before compare_files resets arrays
  local pre_compare_deletions=("${DELETED_FILES[@]}")
  compare_files "$SUBSTITUTED_TEMPLATES_PATH"
  # Merge pre-compare deletions back, skipping any already found by compare
  if [[ ${#pre_compare_deletions[@]} -gt 0 ]]; then
    local -A compare_seen=()
    for f in "${DELETED_FILES[@]}"; do compare_seen["$f"]=1; done
    for f in "${pre_compare_deletions[@]}"; do
      [[ -z "${compare_seen[$f]+x}" ]] && DELETED_FILES+=("$f")
    done
  fi
  generate_diff_report "$SUBSTITUTED_TEMPLATES_PATH"

  # Summary
  local total_changes=$((${#ADDED_FILES[@]} + ${#MODIFIED_FILES[@]} + ${#DELETED_FILES[@]}))
  if [[ $total_changes -eq 0 ]]; then
    log_success "Templates are up to date - no changes needed"
    # Root CLAUDE.md @import wiring is not a tracked template file, so it must
    # run even when no template files changed — e.g. a re-run after the version
    # was already bumped by a prior sync. Only mutate in local apply mode.
    if $LOCAL_MODE && ! $DRY_RUN; then
      apply_wiring "$SUBSTITUTED_TEMPLATES_PATH"
    fi
  elif $DRY_RUN; then
    log_info "Dry run complete - $total_changes file(s) would be changed"
  elif $LOCAL_MODE; then
    log_info "Applying $total_changes change(s) locally..."
    APPLY_MODE=true
    apply_changes "$SUBSTITUTED_TEMPLATES_PATH" "$RESOLVED_VERSION"
  else
    log_info "Sync complete - $total_changes file(s) identified for update"
    log_info "Review the changes above and apply manually or via PR"
  fi
}

# Run main with all arguments only if script is executed directly (not sourced)
# This allows tests to source the file and access functions without running main()
#
# The explicit `exit` is load-bearing: bash parses this whole if-block before
# executing it and reads the file lazily afterwards. apply_changes() may have
# overwritten this very file with a newer version, so any read past this block
# would hit stale byte offsets in the new content. Exiting here guarantees
# nothing past `fi` is ever read. Keep this the last statement in the file.
if [[ "${BASH_SOURCE[0]:-}" == "${0:-}" ]]; then
  IS_ENTRYPOINT=true
  main "$@"
  exit $?
fi
