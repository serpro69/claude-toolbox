package main

import (
	"fmt"
	"strings"
)

func ApplyTransforms(content []byte, transforms []TransformConfig) ([]byte, error) {
	result := content
	for _, t := range transforms {
		switch t.Type {
		case "plugin_root_resolve":
			result = applyPluginRootResolve(result, t.ReplacementBase)
		case "inject_header":
			result = applyInjectHeader(result, t.Content)
		case "plugin_root_placeholder":
			result = applyPluginRootPlaceholder(result, t.Placeholder, t.Preamble)
		case "skill_prefix_rewrite":
			result = applySkillPrefixRewrite(result, t.From, t.To)
		case "read_only_tool_guidance":
			result = applyReadOnlyToolGuidance(result)
		default:
			return nil, fmt.Errorf("unknown transform type %q", t.Type)
		}
	}
	return result, nil
}

// Keep runtime instructions consistent with the operation mappings generated
// from agent frontmatter. Canonical Claude files and authoring profiles retain
// their provider-specific tool descriptions.
var readOnlyToolGuidance = strings.NewReplacer(
	"Your tool access is restricted via frontmatter allowlist to:",
	"Your permitted operations, mapped under **Codex Tool Access**, are:",
	"Restricted via frontmatter allowlist to:",
	"Permitted operations, mapped under **Codex Tool Access**, are:",
	"You have no shell and cannot resolve environment variables",
	"The plugin root must come from the spawning context",
	"You have `Read` only",
	"You may perform only the mapped `Read` operation",
	"you have read-only tools",
	"you have read-only access",
	"A Write tool.",
	"Permission to write files.",
	"no Write tool",
	"no permission to write files",
	"The `code-reviewer` sub-agent cannot resolve the plugin root on its own (it has no shell).",
	"The `code-reviewer` sub-agent must use the plugin root supplied by its parent.",
	"The sub-agents cannot resolve the plugin root themselves (no shell).",
	"The sub-agents must use the plugin root supplied by their parent.",
	"The agent has no shell, so",
	"The agent needs the plugin root from its parent, so",
	"the reviewer has no shell — Grep/Glob/Read only",
	"use the native equivalents of the Grep/Glob/Read operations",
)

func applyReadOnlyToolGuidance(content []byte) []byte {
	return []byte(readOnlyToolGuidance.Replace(string(content)))
}

func applyPluginRootResolve(content []byte, replacementBase string) []byte {
	s := rewritePluginRootGuidance(string(content))
	// Codex has no runtime plugin-root variable, so both the harness var
	// (${CLAUDE_PLUGIN_ROOT}) and the session var (${TOOLBOX_PLUGIN_ROOT})
	// resolve to the same concrete base at generation time.
	s = strings.ReplaceAll(s, "${CLAUDE_PLUGIN_ROOT}", replacementBase)
	s = strings.ReplaceAll(s, "${TOOLBOX_PLUGIN_ROOT}", replacementBase)
	return []byte(s)
}

// Path substitution alone leaves Claude-specific shell lookup instructions in
// the generated skills. Keep these prose rewrites narrow: profile authoring
// documentation deliberately retains the Claude variable names. The production
// source regression test catches wording changes that bypass these rewrites.
func rewritePluginRootGuidance(s string) string {
	const installedRoot = "the installed skill's absolute `SKILL.md` path " +
		"(the plugin root is the parent of the `skills/` directory)"
	s = strings.ReplaceAll(s,
		"from its shell variable `$TOOLBOX_PLUGIN_ROOT`",
		"from "+installedRoot+" and passes that absolute path to sub-agents under `## Plugin Root`")
	s = strings.ReplaceAll(s,
		"the variable is unset for the main agent",
		"the installed skill path is unavailable to the main agent")
	s = strings.ReplaceAll(s,
		"(`echo \"${TOOLBOX_PLUGIN_ROOT:-NOT_SET}\"`)",
		"from "+installedRoot)
	s = strings.ReplaceAll(s,
		"the installed plugin root (`$TOOLBOX_PLUGIN_ROOT`)",
		"the installed plugin root (derived from "+installedRoot+")")
	return s
}

func applyPluginRootPlaceholder(content []byte, placeholder, preamble string) []byte {
	s := string(content)
	s = strings.ReplaceAll(s, "${CLAUDE_PLUGIN_ROOT}", placeholder)
	s = strings.ReplaceAll(s, "${TOOLBOX_PLUGIN_ROOT}", placeholder)
	if preamble != "" {
		s = preamble + "\n" + s
	}
	return []byte(s)
}

func applySkillPrefixRewrite(content []byte, from, to string) []byte {
	s := string(content)
	s = strings.ReplaceAll(s, from, to)
	return []byte(s)
}

func applyInjectHeader(content []byte, header string) []byte {
	s := string(content)

	// Inject after frontmatter if present, otherwise at the top.
	if strings.HasPrefix(s, "---\n") {
		end := strings.Index(s[4:], "\n---\n")
		if end >= 0 {
			insertPos := 4 + end + 5 // past closing "---\n"
			return []byte(s[:insertPos] + header + s[insertPos:])
		}
	}

	return []byte(header + s)
}
