package main

import (
	"errors"
	"fmt"
	"os"
	"os/exec"
	"strings"
)

// WithWorktree checks ref out into a throwaway detached git worktree, invokes fn
// with the worktree's root directory, and tears the worktree down afterward. It
// lets the CLI analyze a past commit without disturbing the user's working tree:
// `--ref HEAD~1` runs the whole pipeline against the prior state.
//
// git is resolved from the process working directory (exec inherits it), so the
// command must be run from inside the repository whose history is being
// analyzed — the same assumption the design records for `--ref`.
//
// ref is untrusted CLI input. Two defenses apply: it is passed to git as a
// separate argv entry (never through a shell, so metacharacters cannot inject
// commands), and a leading-dash guard rejects refs git would otherwise parse as
// an option rather than a commit-ish — closing the argument-injection gap that
// separate args alone leave open.
func WithWorktree(ref string, fn func(root string) error) (err error) {
	if ref == "" {
		return fmt.Errorf("worktree: empty git ref")
	}
	if strings.HasPrefix(ref, "-") {
		return fmt.Errorf("worktree: invalid git ref %q (must not start with '-')", ref)
	}

	tempDir, err := os.MkdirTemp("", "plugin-graph-worktree-*")
	if err != nil {
		return fmt.Errorf("worktree: create temp dir: %w", err)
	}

	// registered gates the `git worktree remove` step: it is meaningful only once
	// `git worktree add` has succeeded. On the add-failed path nothing is
	// registered, so removing the bare temp dir is the only teardown needed —
	// running `git worktree remove` there would just emit a spurious "not a
	// working tree" error.
	registered := false

	// Cleanup runs no matter how we leave (early return, panic, normal exit). The
	// two teardown steps are evaluated INDEPENDENTLY and combined with
	// errors.Join: gating the worktree-remove error on RemoveAll's outcome would
	// silently swallow a `git worktree remove` failure whenever RemoveAll
	// succeeded, leaking a dangling registration in the parent repo's
	// .git/worktrees/. Errors surface only when fn itself succeeded (err == nil),
	// so a real fn error is never masked by a teardown hiccup.
	defer func() {
		var rmErr error
		if registered {
			if out, e := exec.Command("git", "worktree", "remove", "--force", tempDir).CombinedOutput(); e != nil {
				rmErr = fmt.Errorf("git worktree remove: %w (%s)", e, strings.TrimSpace(string(out)))
			}
		}
		var dirErr error
		if e := os.RemoveAll(tempDir); e != nil {
			dirErr = fmt.Errorf("remove temp dir: %w", e)
		}
		if cleanupErr := errors.Join(rmErr, dirErr); cleanupErr != nil && err == nil {
			err = fmt.Errorf("worktree: cleanup %s: %w", tempDir, cleanupErr)
		}
	}()

	out, err := exec.Command("git", "worktree", "add", "--detach", tempDir, ref).CombinedOutput()
	if err != nil {
		return fmt.Errorf("worktree: git worktree add %q: %w (%s)", ref, err, strings.TrimSpace(string(out)))
	}
	registered = true

	return fn(tempDir)
}
