package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestGenerateAgentToolAccess(t *testing.T) {
	m, err := ParseManifest("../../scripts/kodex-generate-manifest.yml")
	if err != nil {
		t.Fatal(err)
	}
	m.SourcePlugin = filepath.Join("../..", m.SourcePlugin)
	m.TargetPlugin = t.TempDir()
	m.Agents.TargetDir = t.TempDir()
	if err := GenerateAgents(m, false); err != nil {
		t.Fatal(err)
	}
	if err := GenerateSkills(m, false); err != nil {
		t.Fatal(err)
	}

	cases := []struct {
		name      string
		canSearch bool
		canCapy   bool
	}{
		{name: "code-reviewer", canSearch: true, canCapy: true},
		{name: "design-reviewer", canSearch: true, canCapy: true},
		{name: "spec-reviewer", canSearch: true, canCapy: true},
		{name: "architecture-reviewer", canSearch: true, canCapy: true},
		{name: "profile-resolver", canSearch: true},
		{name: "eval-grader"},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			data, err := os.ReadFile(filepath.Join(m.Agents.TargetDir, tc.name+".toml"))
			if err != nil {
				t.Fatal(err)
			}
			content := string(data)
			for _, want := range []string{
				`sandbox_mode = "read-only"`, "## Codex Tool Access",
				"`exec_command`", "`functions.exec`", "- `Read`:",
				"Do not edit files", "role-specific path and input restrictions",
			} {
				if !strings.Contains(content, want) {
					t.Errorf("missing %q", want)
				}
			}
			for _, operation := range []string{"Grep", "Glob"} {
				if strings.Contains(content, "- `"+operation+"`:") != tc.canSearch {
					t.Errorf("unexpected permission for %s", operation)
				}
			}
			if strings.Contains(content, "- `capy_search`:") != tc.canCapy {
				t.Error("unexpected permission for capy_search")
			}
			if tc.name == "eval-grader" && !strings.Contains(content, "You MUST NOT open fixture paths") {
				t.Error("grader fixture isolation was lost")
			}
			if tc.name == "profile-resolver" && !strings.Contains(content, "Do not open files outside the worktree") {
				t.Error("resolver path restriction was lost")
			}
		})
	}

	// Runtime-read skill procedures must not restore the obsolete restrictions.
	for _, root := range []string{m.Agents.TargetDir, filepath.Join(m.TargetPlugin, "skills")} {
		err := filepath.WalkDir(root, func(path string, entry os.DirEntry, err error) error {
			if err != nil {
				return err
			}
			if entry.IsDir() {
				return nil
			}
			data, err := os.ReadFile(path)
			if err != nil {
				return err
			}
			for _, obsolete := range []string{"no shell", "frontmatter allowlist", "You have `Read` only"} {
				if strings.Contains(string(data), obsolete) {
					t.Errorf("%s retains %q", path, obsolete)
				}
			}
			return nil
		})
		if err != nil {
			t.Fatal(err)
		}
	}
}

func TestGenerateAgentRejectsUnsupportedTools(t *testing.T) {
	for _, tool := range []string{"Bash", "Write", "Edit", "mcp__capy__capy_execute", "UnknownTool"} {
		t.Run(tool, func(t *testing.T) {
			dir := t.TempDir()
			src := filepath.Join(dir, "agent.md")
			dst := filepath.Join(dir, "agent.toml")
			content := "---\nname: test\ntools:\n  - " + tool + "\n---\n\n# Test\n"
			if err := os.WriteFile(src, []byte(content), 0o644); err != nil {
				t.Fatal(err)
			}
			err := generateAgent(src, dst, AgentsConfig{SandboxMode: "read-only"})
			if err == nil || !strings.Contains(err.Error(), "unsupported agent tool") {
				t.Fatalf("expected unsupported-tool error, got %v", err)
			}
			_, statErr := os.Stat(dst)
			if statErr == nil {
				t.Fatal("unsupported agent wrote a destination file")
			}
			if !os.IsNotExist(statErr) {
				t.Fatalf("checking destination file: %v", statErr)
			}
		})
	}
}

func TestGenerateAgentEmptyToolList(t *testing.T) {
	for _, tc := range []struct {
		name      string
		field     string
		wantsDeny bool
	}{
		{name: "omitted tools inherit", field: ""},
		{name: "empty tools deny", field: "tools: []\n", wantsDeny: true},
	} {
		t.Run(tc.name, func(t *testing.T) {
			dir := t.TempDir()
			src := filepath.Join(dir, "agent.md")
			dst := filepath.Join(dir, "agent.toml")
			content := "---\nname: test\n" + tc.field + "---\n\n# Test\n"
			if err := os.WriteFile(src, []byte(content), 0o644); err != nil {
				t.Fatal(err)
			}
			if err := generateAgent(src, dst, AgentsConfig{SandboxMode: "read-only"}); err != nil {
				t.Fatal(err)
			}
			data, err := os.ReadFile(dst)
			if err != nil {
				t.Fatal(err)
			}
			if strings.Contains(string(data), "No tool operations are permitted") != tc.wantsDeny {
				t.Error("omitted and explicitly empty tool lists must retain distinct permissions")
			}
			if strings.Contains(string(data), "`exec_command`") {
				t.Error("an empty tool list should not grant shell inspection")
			}
		})
	}
}
