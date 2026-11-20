#!/usr/bin/env bash
# The tool's requested directory can belong to a different repository. Only
# the hook's own working directory selects a workspace policy.
guard_workspace() (
    unset GIT_DIR GIT_COMMON_DIR GIT_WORK_TREE GIT_CEILING_DIRECTORIES
    local launch diagnostic
    launch=$(pwd -P) || return 1
    # Send Git's absolute top level to our caller; capture stderr separately
    # so a Git warning cannot become part of the workspace path.
    exec 4>&1
    if diagnostic=$(LC_ALL=C git -C "$launch" rev-parse --show-toplevel 2>&1 >&4); then
        return 0
    elif [[ "$diagnostic" == "fatal: "[Nn]"ot a git repository (or any"* ]]; then
        printf '%s\n' "$launch"
    else
        # A failed Git executable, invalid worktree or unsafe ownership
        # cannot establish which repository's policy should apply.
        printf 'kk guard: unable to determine workspace: %s\n' "$diagnostic" >&2
        return 1
    fi
)
