package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

// Use the canonical plugin and production manifest so prose changes cannot
// silently bypass the Codex-specific root-resolution rewrite.
func TestGenerateInstalledPluginRootGuidance(t *testing.T) {
	m, err := ParseManifest("../../scripts/kodex-generate-manifest.yml")
	if err != nil {
		t.Fatal(err)
	}
	m.SourcePlugin = filepath.Join("../..", m.SourcePlugin)
	m.TargetPlugin = t.TempDir()
	m.Agents.TargetDir = t.TempDir()
	if err := GenerateSkills(m, false); err != nil {
		t.Fatal(err)
	}
	if err := GenerateShared(m, false); err != nil {
		t.Fatal(err)
	}
	if err := GenerateAgents(m, false); err != nil {
		t.Fatal(err)
	}

	// Guard future skills and prose variants as well as the known regressions.
	// Profiles are excluded: they document the canonical Claude conventions.
	for _, root := range []string{filepath.Join(m.TargetPlugin, "skills"), m.Agents.TargetDir} {
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
			if strings.Contains(string(data), "TOOLBOX_PLUGIN_ROOT") {
				t.Errorf("generated file %s still references TOOLBOX_PLUGIN_ROOT", path)
			}
			return nil
		})
		if err != nil {
			t.Fatal(err)
		}
	}

	cases := []struct {
		name string
		path string
		want []string
	}{
		{
			name: "shared detection",
			path: "skills/_shared/profile-detection.md",
			want: []string{
				"installed skill", "parent of the `skills/` directory",
				"installed skill path is unavailable", "## Plugin Root",
			},
		},
		{
			name: "dereferenced detection",
			path: "skills/review-code/shared-profile-detection.md",
			want: []string{"installed skill", "parent of the `skills/` directory", "## Plugin Root"},
		},
		{
			name: "architecture delegation",
			path: "skills/review-architecture/SKILL.md",
			want: []string{
				"installed skill", "parent of the `skills/` directory",
				"inject the absolute path under a `## Plugin Root` heading",
			},
		},
		{
			name: "code review delegation",
			path: "skills/review-code/review-isolated.md",
			want: []string{"Expand plugin-relative checklist paths to absolute paths", "## Plugin Root"},
		},
		{
			name: "eval delegation",
			path: "skills/review-code/evals/_harness/HARNESS.md",
			want: []string{"installed skill", "parent of the `skills/` directory", "## Plugin Root"},
		},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			data, err := os.ReadFile(filepath.Join(m.TargetPlugin, tc.path))
			if err != nil {
				t.Fatal(err)
			}
			content := string(data)
			if strings.Contains(content, "TOOLBOX_PLUGIN_ROOT") || strings.Contains(content, "the variable is unset") {
				t.Error("generated instructions still depend on the Claude shell variable")
			}
			for _, want := range tc.want {
				if !strings.Contains(content, want) {
					t.Errorf("missing %q", want)
				}
			}
		})
	}

	for _, name := range []string{"code-reviewer", "architecture-reviewer", "profile-resolver"} {
		t.Run(name, func(t *testing.T) {
			data, err := os.ReadFile(filepath.Join(m.Agents.TargetDir, name+".toml"))
			if err != nil {
				t.Fatal(err)
			}
			content := string(data)
			for _, want := range []string{"installed skill", "## Plugin Root", "If no `## Plugin Root` value was provided, stop"} {
				if !strings.Contains(content, want) {
					t.Errorf("missing %q", want)
				}
			}
			if strings.Contains(content, "If not provided, resolve") || strings.Contains(content, "TOOLBOX_PLUGIN_ROOT") {
				t.Error("sub-agent should use the injected root, without discovery or environment lookup")
			}
		})
	}
}
