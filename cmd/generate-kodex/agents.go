package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"gopkg.in/yaml.v3"
)

type AgentFrontmatter struct {
	Name        string   `yaml:"name"`
	Description string   `yaml:"description"`
	Tools       []string `yaml:"tools"`
}

func GenerateAgents(m *Manifest, dryRun bool) error {
	sourceAgents := filepath.Join(m.SourcePlugin, "agents")
	targetDir := m.Agents.TargetDir

	entries, err := os.ReadDir(sourceAgents)
	if err != nil {
		return fmt.Errorf("reading agents directory: %w", err)
	}

	if dryRun {
		for _, entry := range entries {
			if entry.IsDir() || !strings.HasSuffix(entry.Name(), ".md") {
				continue
			}
			name := strings.TrimSuffix(entry.Name(), ".md")
			fmt.Printf("[dry-run] generate agent %s → %s/%s.toml\n", entry.Name(), targetDir, name)
		}
		return nil
	}

	if err := os.MkdirAll(targetDir, 0o755); err != nil {
		return fmt.Errorf("creating agents directory: %w", err)
	}

	for _, entry := range entries {
		if entry.IsDir() || !strings.HasSuffix(entry.Name(), ".md") {
			continue
		}

		src := filepath.Join(sourceAgents, entry.Name())
		name := strings.TrimSuffix(entry.Name(), ".md")
		dst := filepath.Join(targetDir, name+".toml")

		if err := generateAgent(src, dst, m.Agents); err != nil {
			return fmt.Errorf("generating agent %s: %w", name, err)
		}
		fmt.Printf("generated agent %s\n", name)
	}

	return nil
}

func generateAgent(src, dst string, cfg AgentsConfig) error {
	content, err := os.ReadFile(src)
	if err != nil {
		return fmt.Errorf("reading %s: %w", src, err)
	}

	fm, body, err := parseFrontmatter(content)
	if err != nil {
		return fmt.Errorf("parsing frontmatter: %w", err)
	}

	body, err = ApplyTransforms(body, cfg.Transforms)
	if err != nil {
		return fmt.Errorf("transforming agent body: %w", err)
	}

	toolPolicy, err := agentToolPolicy(fm.Tools)
	if err != nil {
		return fmt.Errorf("mapping agent tools: %w", err)
	}
	toml := formatAgentTOML(fm, toolPolicy+string(body), cfg)

	return os.WriteFile(dst, []byte(toml), 0o644)
}

// Codex exposes different tool names, so preserve the source allowlist as
// permitted operations. The read-only sandbox remains configured separately.
func agentToolPolicy(toolNames []string) (string, error) {
	if toolNames == nil {
		return "", nil
	}
	if len(toolNames) == 0 {
		return "## Codex Tool Access\n\nNo tool operations are permitted. Work only from the provided input.\n\n", nil
	}

	var b strings.Builder
	b.WriteString("## Codex Tool Access\n\n")
	b.WriteString("Claude tool names in these instructions denote permitted operations, not literal Codex tool names. ")
	b.WriteString("Use native file tools when available; otherwise use `exec_command` for the read-only commands below, ")
	b.WriteString("directly or through a tool wrapper such as `functions.exec`. ")
	b.WriteString("Only the listed operations are permitted, subject to all role-specific path and input restrictions.\n\n")
	for _, name := range toolNames {
		switch name {
		case "Read":
			b.WriteString("- `Read`: read permitted files with a native file reader or `cat`/`sed` through `exec_command`.\n")
		case "Grep":
			b.WriteString("- `Grep`: search permitted file contents with a native search tool or `rg` through `exec_command`.\n")
		case "Glob":
			b.WriteString("- `Glob`: locate permitted paths with a native file-listing tool or `rg --files`/`ls` through `exec_command`.\n")
		case "mcp__capy__capy_search":
			b.WriteString("- `capy_search`: query project knowledge using the available Capy search tool.\n")
		default:
			return "", fmt.Errorf("unsupported agent tool %q", name)
		}
	}
	b.WriteString("\nDo not edit files, run tests or repository scripts, or request elevated permissions. ")
	b.WriteString("Shell access and tool wrappers do not grant additional operations or access to excluded inputs.\n\n")
	return b.String(), nil
}

func parseFrontmatter(content []byte) (AgentFrontmatter, []byte, error) {
	s := string(content)

	if !strings.HasPrefix(s, "---\n") {
		return AgentFrontmatter{}, content, fmt.Errorf("no frontmatter found")
	}

	end := strings.Index(s[4:], "\n---\n")
	if end < 0 {
		// Try trailing --- at end of file
		end = strings.Index(s[4:], "\n---")
		if end < 0 || (4+end+4 < len(s) && s[4+end+4] != '\n') {
			return AgentFrontmatter{}, content, fmt.Errorf("unterminated frontmatter")
		}
	}

	fmRaw := s[4 : 4+end]
	body := strings.TrimLeft(s[4+end+4:], "\n")

	var fm AgentFrontmatter
	if err := yaml.Unmarshal([]byte(fmRaw), &fm); err != nil {
		return AgentFrontmatter{}, nil, fmt.Errorf("parsing frontmatter YAML: %w", err)
	}

	if fm.Name == "" {
		return AgentFrontmatter{}, nil, fmt.Errorf("frontmatter missing name")
	}

	return fm, []byte(body), nil
}

func agentOverride(cfg AgentsConfig, name string) (model, effort string) {
	model = cfg.Model
	effort = cfg.ModelReasoningEffort
	for _, o := range cfg.Overrides {
		if o.Name == name {
			if o.Model != "" {
				model = o.Model
			}
			if o.ModelReasoningEffort != "" {
				effort = o.ModelReasoningEffort
			}
			break
		}
	}
	return
}

func formatAgentTOML(fm AgentFrontmatter, body string, cfg AgentsConfig) string {
	var b strings.Builder

	fmt.Fprintf(&b, "name = %q\n", fm.Name)

	desc := strings.TrimSpace(fm.Description)
	if strings.Contains(desc, "\n") {
		fmt.Fprintf(&b, "description = \"\"\"\n%s\n\"\"\"\n", escapeTomlMultiline(desc))
	} else {
		fmt.Fprintf(&b, "description = %q\n", desc)
	}

	model, effort := agentOverride(cfg, fm.Name)
	fmt.Fprintf(&b, "sandbox_mode = %q\n", cfg.SandboxMode)
	fmt.Fprintf(&b, "model = %q\n", model)
	fmt.Fprintf(&b, "model_reasoning_effort = %q\n", effort)

	body = strings.TrimRight(body, "\n")
	fmt.Fprintf(&b, "developer_instructions = \"\"\"\n%s\n\"\"\"\n", escapeTomlMultiline(body))

	return b.String()
}

func escapeTomlMultiline(s string) string {
	s = strings.ReplaceAll(s, "\\", "\\\\")
	s = strings.ReplaceAll(s, `"""`, `""\"`)
	return s
}
