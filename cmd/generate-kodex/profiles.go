package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func GenerateProfiles(m *Manifest, dryRun bool) error {
	if !m.Profiles.Copy {
		return nil
	}

	srcProfiles := filepath.Join(m.SourcePlugin, "profiles")
	dstProfiles := filepath.Join(m.TargetPlugin, "profiles")

	if dryRun {
		fmt.Printf("[dry-run] copy profiles/ → %s\n", dstProfiles)
		return nil
	}

	if _, err := os.Stat(srcProfiles); os.IsNotExist(err) {
		return nil
	}

	// Profiles use their own transform list — deliberately WITHOUT
	// plugin_root_resolve — so files that *document* the ${...PLUGIN_ROOT}
	// convention (e.g. profiles/skill-md/*) keep their tokens literal instead
	// of being rewritten to a path.
	if err := copySkillDir(srcProfiles, dstProfiles, m.Profiles.Transforms); err != nil {
		return fmt.Errorf("copying profiles directory: %w", err)
	}

	fmt.Println("generated profiles/")
	return nil
}
