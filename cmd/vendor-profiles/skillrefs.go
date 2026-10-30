package main

import (
	"path"
	"regexp"
	"strings"
)

const skillIDPattern = "`([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)@([a-zA-Z0-9_.-]+)`"

var (
	skillIDRegex  = regexp.MustCompile(skillIDPattern)
	skillSeeRegex = regexp.MustCompile(`(?i)\bsee[ \t]+(?:the[ \t]+)?` + skillIDPattern +
		`(?:,[ \t]*` + skillIDPattern + `)*(?:[ \t]+skills?\b)?`)
)

// RewriteSkillReferences handles upstream skill navigation written as inline
// code rather than Markdown links. Like RewriteLinks, it links only to content
// vendored into the same phase. Unavailable navigation is removed as a clause,
// keeping the surrounding recommendation rather than leaving a dangling "see".
func RewriteSkillReferences(content []byte, repo, phase string, files []*File) []byte {
	if !skillSeeRegex.Match(content) {
		return content
	}
	lines := strings.Split(string(content), "\n")
	var output []string
	var fence string
	removedLine := false
	changed := false
	for _, line := range lines {
		trimmed := strings.TrimSpace(line)
		if strings.HasPrefix(trimmed, "```") || strings.HasPrefix(trimmed, "~~~") {
			marker := trimmed[:3]
			if fence == "" {
				fence = marker
			} else if fence == marker {
				fence = ""
			}
			output = append(output, line)
			continue
		}
		if fence != "" {
			output = append(output, line)
			continue
		}
		matches := skillSeeRegex.FindAllStringIndex(line, -1)
		changed = changed || len(matches) > 0
		for j := len(matches) - 1; j >= 0; j-- {
			start, end := matches[j][0], matches[j][1]
			var links []string
			for _, ref := range skillIDRegex.FindAllStringSubmatch(line[start:end], -1) {
				if ref[1] != repo {
					continue
				}
				for _, file := range files {
					if file.Phase == phase && file.Source == path.Join("skills", ref[2], "SKILL.md") {
						links = append(links, "["+file.As+"]("+file.As+")")
						break
					}
				}
			}
			if len(links) > 0 {
				line = line[:start] + line[start:start+3] + " " + strings.Join(links, ", ") + line[end:]
				continue
			}
			line = removeSkillClause(line, start, end)
		}
		if len(matches) > 0 && line == "" {
			removedLine = true
			continue
		}
		if removedLine && line == "" && (len(output) == 0 || output[len(output)-1] == "") {
			continue
		}
		removedLine = false
		output = append(output, line)
	}
	if !changed {
		return content
	}
	// A reference-only section can disappear entirely. Remove its now-empty
	// heading, without touching headings inside fenced examples.
	var cleaned []string
	fence = ""
	for i := 0; i < len(output); i++ {
		line := output[i]
		trimmed := strings.TrimSpace(line)
		if strings.HasPrefix(trimmed, "```") || strings.HasPrefix(trimmed, "~~~") {
			if fence == "" {
				fence = trimmed[:3]
			} else if fence == trimmed[:3] {
				fence = ""
			}
		} else if fence == "" && (line == "## Cross-References" || line == "## Related Skills") {
			end := i + 1
			for end < len(output) && strings.TrimSpace(output[end]) == "" {
				end++
			}
			if end == len(output) || strings.HasPrefix(output[end], "#") {
				i = end - 1
				continue
			}
		}
		cleaned = append(cleaned, line)
	}
	result := strings.Join(cleaned, "\n")
	if len(result) > 0 && strings.HasSuffix(string(content), "\n") {
		result = strings.TrimRight(result, "\n") + "\n"
	}
	return []byte(result)
}

func removeSkillClause(line string, start, end int) string {
	// Include an optional arrow and the opening parenthesis of a parenthetical
	// reference. "For ... see" introductions are navigation too.
	prefix := strings.TrimRight(line[:start], " \t")
	for _, marker := range []string{"→", "->"} {
		prefix = strings.TrimRight(strings.TrimSuffix(prefix, marker), " \t")
	}
	parenthetical := strings.HasSuffix(prefix, "(")
	if parenthetical {
		prefix = strings.TrimRight(strings.TrimSuffix(prefix, "("), " \t")
	} else {
		clauseStart := 0
		for _, separator := range []string{". ", "; "} {
			if pos := strings.LastIndex(prefix, separator); pos >= clauseStart {
				clauseStart = pos + len(separator)
			}
		}
		if strings.HasPrefix(strings.ToLower(strings.TrimSpace(prefix[clauseStart:])), "for ") {
			prefix = strings.TrimRight(prefix[:clauseStart], " \t")
		}
	}

	// Stop at the enclosing parenthesis, table cell, or sentence/clause end.
	// Dots inside code spans (b.Loop(), sync.Pool) are not sentence boundaries.
	depth := 0
	inCode := false
	for end < len(line) {
		c := line[end]
		if c == '`' {
			inCode = !inCode
		}
		if !inCode {
			if c == '(' {
				depth++
			} else if c == ')' {
				if depth == 0 {
					if parenthetical {
						end++
					}
					break
				}
				depth--
			}
			if depth == 0 && !parenthetical && (c == ';' || c == '.' && (end+1 == len(line) || line[end+1] == ' ')) {
				end++
				break
			}
			if c == '|' {
				break
			}
		}
		end++
	}
	prefix = strings.TrimRight(strings.TrimSuffix(prefix, "—"), " \t")
	if prefix == "-" || prefix == "*" {
		prefix = ""
	}
	suffix := strings.TrimLeft(line[end:], " \t")
	if suffix == "" && strings.HasSuffix(prefix, ";") {
		prefix = strings.TrimSuffix(prefix, ";")
		if strings.HasSuffix(strings.TrimSpace(line), ".") {
			prefix += "."
		}
	}
	if prefix == "" {
		return suffix
	}
	if suffix == "" || strings.ContainsAny(suffix[:1], ".,;)") {
		return prefix + suffix
	}
	return prefix + " " + suffix
}
