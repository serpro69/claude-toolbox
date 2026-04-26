package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

func GeneratePluginManifest(m *Manifest, dryRun bool) error {
	outDir := filepath.Join(m.TargetPlugin, ".codex-plugin")
	outPath := filepath.Join(outDir, "plugin.json")

	if dryRun {
		fmt.Printf("[dry-run] generate manifest → %s\n", outPath)
		return nil
	}

	sourceFields, err := readSourceManifest(m.Manifest.VersionFrom)
	if err != nil {
		return fmt.Errorf("reading source manifest: %w", err)
	}

	manifest := map[string]any{
		"name": m.Manifest.Name,
	}
	// Copy metadata fields from source (description, author, homepage, etc.)
	for _, key := range []string{"description", "author", "homepage", "repository", "license", "keywords"} {
		if v, ok := sourceFields[key]; ok {
			manifest[key] = v
		}
	}
	manifest["version"] = sourceFields["version"]
	for k, v := range m.Manifest.ExtraFields {
		manifest[k] = v
	}

	data, err := json.MarshalIndent(manifest, "", "  ")
	if err != nil {
		return fmt.Errorf("marshaling manifest: %w", err)
	}
	data = append(data, '\n')

	if err := os.MkdirAll(outDir, 0o755); err != nil {
		return fmt.Errorf("creating directory: %w", err)
	}
	if err := os.WriteFile(outPath, data, 0o644); err != nil {
		return fmt.Errorf("writing manifest: %w", err)
	}

	fmt.Printf("generated %s\n", outPath)
	return nil
}

func readSourceManifest(path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("reading %s: %w", path, err)
	}

	var source map[string]any
	if err := json.Unmarshal(data, &source); err != nil {
		return nil, fmt.Errorf("parsing %s: %w", path, err)
	}
	if _, ok := source["version"]; !ok {
		return nil, fmt.Errorf("no version field in %s", path)
	}

	return source, nil
}
