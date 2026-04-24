package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestIntegration_FullPipeline(t *testing.T) {
	targetDir := t.TempDir()
	fixtureDir := "testdata"
	manifestPath := filepath.Join(fixtureDir, "manifest.yml")

	fetcher := &LocalFetcher{BaseDir: fixtureDir}

	if err := run(manifestPath, targetDir, false, fetcher); err != nil {
		t.Fatalf("run: %v", err)
	}

	t.Run("output files exist", func(t *testing.T) {
		expected := []string{
			"review-code/security.md",
			"review-code/security-injection-ref.md",
			"review-code/database.md",
			"implement/security.md",
			"test/testing.md",
		}
		for _, rel := range expected {
			path := filepath.Join(targetDir, rel)
			if _, err := os.Stat(path); err != nil {
				t.Errorf("expected file %s not found", rel)
			}
		}
	})

	t.Run("from_first_h1 strips frontmatter and persona", func(t *testing.T) {
		data, err := os.ReadFile(filepath.Join(targetDir, "review-code/security.md"))
		if err != nil {
			t.Fatalf("reading security.md: %v", err)
		}
		content := string(data)
		if !strings.HasPrefix(content, "# Go Security Checklist") {
			t.Errorf("expected content to start with H1, got: %q", content[:min(60, len(content))])
		}
		if strings.Contains(content, "---") {
			t.Error("frontmatter delimiters not stripped")
		}
		if strings.Contains(content, "You are a Go security expert") {
			t.Error("persona declaration not stripped")
		}
	})

	t.Run("keep all preserves full content", func(t *testing.T) {
		data, err := os.ReadFile(filepath.Join(targetDir, "review-code/security-injection-ref.md"))
		if err != nil {
			t.Fatalf("reading security-injection-ref.md: %v", err)
		}
		content := string(data)
		if !strings.HasPrefix(content, "# SQL Injection Prevention") {
			t.Errorf("expected full content preserved, got: %q", content[:min(60, len(content))])
		}
		if !strings.Contains(content, "## Command Injection") {
			t.Error("full content not preserved")
		}
	})

	t.Run("co-vendored links rewritten", func(t *testing.T) {
		data, err := os.ReadFile(filepath.Join(targetDir, "review-code/security.md"))
		if err != nil {
			t.Fatalf("reading security.md: %v", err)
		}
		content := string(data)
		if !strings.Contains(content, "[injection details](security-injection-ref.md)") {
			t.Errorf("co-vendored link not rewritten, got: %s", content)
		}
	})

	t.Run("external links preserved", func(t *testing.T) {
		data, err := os.ReadFile(filepath.Join(targetDir, "review-code/security.md"))
		if err != nil {
			t.Fatalf("reading security.md: %v", err)
		}
		content := string(data)
		if !strings.Contains(content, "](https://pkg.go.dev/crypto/rand)") {
			t.Errorf("external link not preserved, got: %s", content)
		}
	})

	t.Run("cross-skill references stripped", func(t *testing.T) {
		data, err := os.ReadFile(filepath.Join(targetDir, "review-code/security.md"))
		if err != nil {
			t.Fatalf("reading security.md: %v", err)
		}
		content := string(data)
		if strings.Contains(content, "samber/cc-skills-golang@") {
			t.Error("cross-skill reference not stripped")
		}
		if !strings.Contains(content, "golang-testing") {
			t.Error("display text lost from stripped link")
		}
	})

	t.Run("non-vendored links stripped", func(t *testing.T) {
		data, err := os.ReadFile(filepath.Join(targetDir, "review-code/security.md"))
		if err != nil {
			t.Fatalf("reading security.md: %v", err)
		}
		content := string(data)
		if strings.Contains(content, "references/auth.md") {
			t.Error("non-vendored link not stripped")
		}
		if !strings.Contains(content, "auth notes") {
			t.Error("display text lost from non-vendored link")
		}
	})

	t.Run("index.md files have correct structure", func(t *testing.T) {
		phases := []string{"review-code", "implement", "test"}
		for _, phase := range phases {
			data, err := os.ReadFile(filepath.Join(targetDir, phase, "index.md"))
			if err != nil {
				t.Errorf("reading %s/index.md: %v", phase, err)
				continue
			}
			content := string(data)
			if !strings.Contains(content, beginMarker) {
				t.Errorf("%s/index.md missing BEGIN marker", phase)
			}
			if !strings.Contains(content, endMarker) {
				t.Errorf("%s/index.md missing END marker", phase)
			}
		}

		rcIndex, _ := os.ReadFile(filepath.Join(targetDir, "review-code", "index.md"))
		rcContent := string(rcIndex)
		if !strings.Contains(rcContent, "## Always load") {
			t.Error("review-code/index.md missing Always load heading")
		}
		if !strings.Contains(rcContent, "## Conditional") {
			t.Error("review-code/index.md missing Conditional heading")
		}
		if !strings.Contains(rcContent, "**Load if:**") {
			t.Error("review-code/index.md missing Load if clause")
		}
	})

	t.Run("implement has only always-load", func(t *testing.T) {
		data, _ := os.ReadFile(filepath.Join(targetDir, "implement", "index.md"))
		content := string(data)
		if !strings.Contains(content, "## Always load") {
			t.Error("implement/index.md missing Always load heading")
		}
		if strings.Contains(content, "## Conditional") {
			t.Error("implement/index.md should not have Conditional heading")
		}
	})
}

func TestIntegration_Idempotent(t *testing.T) {
	targetDir := t.TempDir()
	fixtureDir := "testdata"
	manifestPath := filepath.Join(fixtureDir, "manifest.yml")
	fetcher := &LocalFetcher{BaseDir: fixtureDir}

	if err := run(manifestPath, targetDir, false, fetcher); err != nil {
		t.Fatalf("first run: %v", err)
	}

	firstFiles := snapshotDir(t, targetDir)

	if err := run(manifestPath, targetDir, false, fetcher); err != nil {
		t.Fatalf("second run: %v", err)
	}

	secondFiles := snapshotDir(t, targetDir)

	if len(firstFiles) != len(secondFiles) {
		t.Fatalf("file count changed: %d → %d", len(firstFiles), len(secondFiles))
	}
	for path, firstContent := range firstFiles {
		secondContent, ok := secondFiles[path]
		if !ok {
			t.Errorf("file %s missing after second run", path)
			continue
		}
		if firstContent != secondContent {
			t.Errorf("file %s changed between runs.\nFirst:\n%s\nSecond:\n%s", path, firstContent, secondContent)
		}
	}
}

func TestIntegration_DryRun_NoFilesWritten(t *testing.T) {
	targetDir := t.TempDir()
	fixtureDir := "testdata"
	manifestPath := filepath.Join(fixtureDir, "manifest.yml")
	fetcher := &LocalFetcher{BaseDir: fixtureDir}

	if err := run(manifestPath, targetDir, true, fetcher); err != nil {
		t.Fatalf("dry-run: %v", err)
	}

	entries, err := os.ReadDir(targetDir)
	if err != nil {
		t.Fatalf("reading target dir: %v", err)
	}
	if len(entries) != 0 {
		var names []string
		for _, e := range entries {
			names = append(names, e.Name())
		}
		t.Errorf("dry-run should not create files, found: %v", names)
	}
}

func snapshotDir(t *testing.T, root string) map[string]string {
	t.Helper()
	files := make(map[string]string)
	err := filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			return nil
		}
		rel, _ := filepath.Rel(root, path)
		data, err := os.ReadFile(path)
		if err != nil {
			return err
		}
		files[rel] = string(data)
		return nil
	})
	if err != nil {
		t.Fatalf("walking %s: %v", root, err)
	}
	return files
}
