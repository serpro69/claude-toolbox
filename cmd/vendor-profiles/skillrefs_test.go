package main

import "testing"

func TestRewriteSkillReferences(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{
			name:  "reported strings builder reference",
			input: "12. **Use `strings.Builder`** for concatenation in loops → see `samber/cc-skills-golang@golang-code-style`",
			want:  "12. **Use `strings.Builder`** for concatenation in loops",
		},
		{
			name:  "same phase local link",
			input: "- → See the `samber/cc-skills-golang@golang-naming` skill for naming conventions",
			want:  "- → See [naming.md](naming.md) for naming conventions",
		},
		{
			name:  "mixed reference list",
			input: "See `samber/cc-skills-golang@golang-safety`, `samber/cc-skills-golang@golang-naming`, `other/repo@golang-security` skills.",
			want:  "See [naming.md](naming.md).",
		},
		{
			name:  "standalone unavailable reference",
			input: "- -> See `samber/cc-skills-golang@golang-safety` skill for nil pitfalls (maps, slices)",
			want:  "",
		},
		{
			name:  "unavailable parenthetical preserves instruction",
			input: "Use an options struct (see `samber/cc-skills-golang@golang-design-patterns` skill).",
			want:  "Use an options struct.",
		},
		{
			name:  "parenthetical with nested description",
			input: "Use pprof (→ See `samber/cc-skills-golang@golang-troubleshooting` skill for profiles (CPU, memory)).",
			want:  "Use pprof.",
		},
		{
			name:  "multiple sentences preserve recommendation",
			input: "Use early returns. → See `samber/cc-skills-golang@golang-code-style` for examples. Keep errors clear.",
			want:  "Use early returns. Keep errors clear.",
		},
		{
			name:  "for introductions and semicolon clauses",
			input: "Style guidance. For naming see `samber/cc-skills-golang@golang-naming` skill; for design patterns see `samber/cc-skills-golang@golang-design-patterns` skill.",
			want:  "Style guidance. For naming see [naming.md](naming.md).",
		},
		{
			name:  "middle clause removal retains separator",
			input: "For naming see `samber/cc-skills-golang@golang-naming` skill; for safety see `samber/cc-skills-golang@golang-safety` skill; for security see `samber/cc-skills-golang@golang-security` skill.",
			want:  "For naming see [naming.md](naming.md); for security see [security.md](security.md).",
		},
		{
			name:  "all unavailable introductions",
			input: "Measurement workflow. For optimizations, → See `samber/cc-skills-golang@golang-performance` skill. For pprof setup, → See `samber/cc-skills-golang@golang-troubleshooting` skill.",
			want:  "Measurement workflow.",
		},
		{
			name:  "code spans and following local reference",
			input: "See `samber/cc-skills-golang@golang-benchmark` for `b.Loop()` (Go 1.24+). See `samber/cc-skills-golang@golang-naming` skill.",
			want:  "See [naming.md](naming.md).",
		},
		{
			name:  "table cells retain structure",
			input: "| Hot path | → See `samber/cc-skills-golang@golang-benchmark` skill | Keep measuring |",
			want:  "| Hot path | | Keep measuring |",
		},
		{
			name:  "remove dangling dash",
			input: "- **Respect 12-factor app** principles — → see `samber/cc-skills-golang@golang-project-layout`",
			want:  "- **Respect 12-factor app** principles",
		},
		{
			name:  "empty navigation section removed",
			input: "# Guidance\n\nKeep errors clear.\n\n## Cross-References\n\n- See `samber/cc-skills-golang@golang-safety` skill\n\n## Examples\n\nCheck errors.\n",
			want:  "# Guidance\n\nKeep errors clear.\n\n## Examples\n\nCheck errors.\n",
		},
		{
			name:  "fenced heading retained when prose changes",
			input: "See `samber/cc-skills-golang@golang-naming` skill.\n\n```markdown\n## Cross-References\n\n## Examples\n```\n",
			want:  "See [naming.md](naming.md).\n\n```markdown\n## Cross-References\n\n## Examples\n```\n",
		},
		{
			name:  "ordinary code and URLs unchanged",
			input: "Use `strings.Builder` and `samber/oops`. [Upstream](https://github.com/samber/cc-skills-golang)\n```text\nSee `samber/cc-skills-golang@golang-naming` skill\n```",
			want:  "Use `strings.Builder` and `samber/oops`. [Upstream](https://github.com/samber/cc-skills-golang)\n```text\nSee `samber/cc-skills-golang@golang-naming` skill\n```",
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := string(RewriteSkillReferences([]byte(tt.input), "samber/cc-skills-golang", "review-code", testFiles()))
			if got != tt.want {
				t.Errorf("got %q, want %q", got, tt.want)
			}
		})
	}
}

func TestRewriteSkillReferences_DoesNotLinkAcrossPhases(t *testing.T) {
	input := "See `samber/cc-skills-golang@golang-naming` skill."
	got := RewriteSkillReferences([]byte(input), "samber/cc-skills-golang", "implement", testFiles())
	if string(got) != "" {
		t.Errorf("reference to another phase should be removed, got %q", got)
	}
}
