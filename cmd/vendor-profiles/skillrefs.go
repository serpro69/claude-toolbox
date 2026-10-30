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
	skillFileHintRegex = regexp.MustCompile(`^[ \t]+\(([a-zA-Z0-9_.-]+\.md)\)`)
)

// RewriteSkillReferences handles upstream skill navigation written as inline
// code rather than Markdown links. It prefers same-phase targets, then other
// packaged phases. Unavailable navigation retains its topic descriptions as
// plain text instead of directing the reader to an uninstalled skill.
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
			refs := skillIDRegex.FindAllStringSubmatch(line[start:end], -1)
			var referenceFile string
			if hint := skillFileHintRegex.FindStringSubmatch(line[end:]); len(refs) == 1 && hint != nil {
				referenceFile = hint[1]
				end += len(hint[0])
			}
			var links []string
			for _, ref := range refs {
				if ref[1] != repo {
					continue
				}
				source := path.Join("skills", ref[2], "SKILL.md")
				if referenceFile != "" {
					source = path.Join("skills", ref[2], "references", referenceFile)
				}
				if target := localReferenceTarget(source, phase, files); target != "" {
					links = append(links, "["+strings.TrimPrefix(target, "../")+"]("+target+")")
				}
			}
			if len(links) > 0 {
				line = line[:start] + line[start:start+3] + " " + strings.Join(links, ", ") + line[end:]
				continue
			}
			line = rewriteUnavailableSkillClause(line, start, end)
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

// Prefer a same-phase copy, otherwise use the lexical first path so manifest
// ordering cannot change which packaged copy a reference resolves to.
func localReferenceTarget(source, phase string, files []*File) string {
	var target string
	for _, file := range files {
		if file.Source != source {
			continue
		}
		if file.Phase == phase {
			return file.As
		}
		candidate := path.Join("..", file.Phase, file.As)
		if target == "" || candidate < target {
			target = candidate
		}
	}
	return target
}

func rewriteUnavailableSkillClause(line string, start, end int) string {
	// Include an optional arrow and the opening parenthesis of a parenthetical
	// reference. Preserve topics both before and after the unavailable identifier.
	var topics []string
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
			topic := strings.TrimSpace(prefix[clauseStart:])[4:]
			topics = append(topics, strings.TrimRight(topic, ", \t"))
			prefix = strings.TrimRight(prefix[:clauseStart], " \t")
		}
	}

	// Stop at the enclosing parenthesis, table cell, or sentence/clause end.
	// Dots inside code spans (b.Loop(), sync.Pool) are not sentence boundaries.
	depth := 0
	inCode := false
	descriptionStart := end
	descriptionEnd := end
	terminator := ""
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
					descriptionEnd = end
					if parenthetical {
						end++
					}
					break
				}
				depth--
			}
			if depth == 0 && !parenthetical && (c == ';' || c == '.' && (end+1 == len(line) || line[end+1] == ' ')) {
				descriptionEnd = end
				terminator = string(c)
				end++
				break
			}
			if c == '|' {
				descriptionEnd = end
				break
			}
		}
		end++
		descriptionEnd = end
	}
	description := strings.TrimSpace(line[descriptionStart:descriptionEnd])
	if strings.HasPrefix(strings.ToLower(description), "for ") {
		description = strings.TrimSpace(description[4:])
	}
	if description != "" {
		topics = append(topics, description)
	}
	if len(topics) > 0 {
		topicText := "Related topics: " + strings.Join(topics, "; ")
		if parenthetical {
			topicText = "(" + topicText + ")"
		}
		if prefix != "" {
			topicText = prefix + " " + topicText
		}
		suffix := line[end:]
		if strings.HasPrefix(suffix, "|") {
			suffix = " " + suffix
		}
		return topicText + terminator + suffix
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
