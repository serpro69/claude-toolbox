package main

import (
	"bytes"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
)

// requireGit skips the calling test when git is not on PATH, so the suite stays
// green in minimal environments without git installed.
func requireGit(t *testing.T) {
	t.Helper()
	if _, err := exec.LookPath("git"); err != nil {
		t.Skip("git not available; skipping worktree test")
	}
}

// runGit runs a git command in dir, failing the test on error. Identity and
// config are pinned via the environment so the test is hermetic regardless of
// the developer's global git configuration (signing, default branch, etc.).
func runGit(t *testing.T, dir string, args ...string) {
	t.Helper()
	cmd := exec.Command("git", args...)
	cmd.Dir = dir
	cmd.Env = append(os.Environ(),
		"GIT_AUTHOR_NAME=test", "GIT_AUTHOR_EMAIL=test@example.com",
		"GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=test@example.com",
		"GIT_CONFIG_GLOBAL=/dev/null", "GIT_CONFIG_SYSTEM=/dev/null",
	)
	if out, err := cmd.CombinedOutput(); err != nil {
		t.Fatalf("git %v: %v\n%s", args, err, out)
	}
}

func writeRepoFile(t *testing.T, root, rel, content string) {
	t.Helper()
	abs := filepath.Join(root, filepath.FromSlash(rel))
	if err := os.MkdirAll(filepath.Dir(abs), 0o755); err != nil {
		t.Fatalf("mkdir for %s: %v", rel, err)
	}
	if err := os.WriteFile(abs, []byte(content), 0o644); err != nil {
		t.Fatalf("write %s: %v", rel, err)
	}
}

// newTestRepo builds a two-commit git repo. marker.txt differs between commits
// (v1 → v2) so a worktree at HEAD~1 can be proven to see the older state. A
// minimal plugin tree under plugintree/ (present from the first commit) lets the
// full CLI pipeline run inside the worktree for the run()-level test.
func newTestRepo(t *testing.T) string {
	t.Helper()
	repo := t.TempDir()
	runGit(t, repo, "init", "-q")

	writeRepoFile(t, repo, "marker.txt", "v1")
	writeRepoFile(t, repo, "plugintree/skills/_shared/profile-detection.md",
		"# Profile detection\n\n## Known profiles\n\n- `go`\n")
	writeRepoFile(t, repo, "plugintree/skills/alpha/SKILL.md", "# Alpha\n\nA skill.\n")
	writeRepoFile(t, repo, "plugintree/agents/code-reviewer.md", "# Code Reviewer\n\nAn agent.\n")
	runGit(t, repo, "add", "-A")
	runGit(t, repo, "commit", "-q", "-m", "c1")

	writeRepoFile(t, repo, "marker.txt", "v2")
	runGit(t, repo, "add", "-A")
	runGit(t, repo, "commit", "-q", "-m", "c2")
	return repo
}

func TestWithWorktreeSeesOlderState(t *testing.T) {
	requireGit(t)
	repo := newTestRepo(t)
	t.Chdir(repo)

	var seenRoot string
	err := WithWorktree("HEAD~1", func(root string) error {
		seenRoot = root
		if _, serr := os.Stat(root); serr != nil {
			t.Errorf("worktree root %q not present during fn: %v", root, serr)
		}
		data, rerr := os.ReadFile(filepath.Join(root, "marker.txt"))
		if rerr != nil {
			return rerr
		}
		if got := strings.TrimSpace(string(data)); got != "v1" {
			t.Errorf("worktree marker = %q, want %q (older-commit state)", got, "v1")
		}
		return nil
	})
	if err != nil {
		t.Fatalf("WithWorktree: %v", err)
	}

	// Cleanup must remove the worktree directory entirely.
	if _, serr := os.Stat(seenRoot); !os.IsNotExist(serr) {
		t.Errorf("worktree root %q still present after cleanup (stat err: %v)", seenRoot, serr)
	}
	// ...and git must no longer track it (no prunable leftovers).
	out, lerr := exec.Command("git", "worktree", "list", "--porcelain").Output()
	if lerr != nil {
		t.Fatalf("git worktree list: %v", lerr)
	}
	if strings.Contains(string(out), seenRoot) {
		t.Errorf("git still lists worktree %q after cleanup:\n%s", seenRoot, out)
	}
}

func TestWithWorktreeRejectsBadRefs(t *testing.T) {
	// Empty and leading-dash refs are rejected at the trust boundary, before any
	// git call — so this needs no git. A leading dash would otherwise be parsed by
	// git as an option (argument injection) even though it is a separate argv entry.
	cases := []struct {
		name string
		ref  string
	}{
		{"empty", ""},
		{"short-option", "-x"},
		{"long-option", "--detach"},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			called := false
			err := WithWorktree(tc.ref, func(string) error { called = true; return nil })
			if err == nil {
				t.Errorf("WithWorktree(%q) err = nil, want a rejection", tc.ref)
			}
			if called {
				t.Errorf("WithWorktree(%q) invoked fn despite a rejected ref", tc.ref)
			}
		})
	}
}

func TestWithWorktreeInvalidRef(t *testing.T) {
	requireGit(t)
	repo := newTestRepo(t)
	t.Chdir(repo)

	called := false
	err := WithWorktree("no-such-ref", func(string) error { called = true; return nil })
	if err == nil {
		t.Fatal("WithWorktree with a non-existent ref err = nil, want a git error")
	}
	if called {
		t.Error("fn ran even though git worktree add failed")
	}
	if !strings.Contains(err.Error(), "worktree: git worktree add") {
		t.Errorf("error = %q, want it to identify the failed git step", err)
	}
}

func TestWithWorktreeNotARepo(t *testing.T) {
	requireGit(t)
	dir := t.TempDir()
	// Guard against the rare case where TMPDIR sits inside a git checkout, which
	// would make this dir part of a real repo and defeat the not-a-repo path.
	probe := exec.Command("git", "rev-parse", "--is-inside-work-tree")
	probe.Dir = dir
	if probe.Run() == nil {
		t.Skip("temp dir is inside a git repo; cannot exercise the not-a-repo path here")
	}
	t.Chdir(dir)

	if err := WithWorktree("HEAD", func(string) error { return nil }); err == nil {
		t.Fatal("WithWorktree outside a git repo err = nil, want an error")
	}
}

func TestRunWithRef(t *testing.T) {
	requireGit(t)
	repo := newTestRepo(t)
	t.Chdir(repo)

	// End-to-end through run(): --ref builds a worktree at HEAD~1, the repo-relative
	// --root is resolved inside it, and the metrics pipeline runs against that state.
	var stdout, stderr bytes.Buffer
	code := run([]string{"--root", "plugintree/", "--ref", "HEAD~1", "metrics"}, &stdout, &stderr)
	if code != exitOK {
		t.Fatalf("run --ref exit = %d, want %d (stderr: %s)", code, exitOK, stderr.String())
	}
	if strings.TrimSpace(stdout.String()) == "" {
		t.Errorf("run --ref produced empty stdout")
	}
}
