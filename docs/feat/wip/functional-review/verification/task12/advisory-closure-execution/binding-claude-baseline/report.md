I loaded the review instructions and stopped before any investigation. I didn't read, diff or change any subject files: no `git diff`, not even `--stat`, and no capy search.

**Entry point and the files it requires** (all under `plugins/kk/skills/review-code/`):
- `SKILL.md`: the entry point, loaded via `/kk:review-code`. It sets a strict 10-phase order in which profile detection and checklist loading must finish before any diff content is read.
- `shared-capy-knowledge-protocol.md`: the rules for `kk:*` labels and for searching and indexing.
- `shared-profile-detection.md`: how active profiles are detected. It names 8 known profiles (`go`, `python`, `java`, `js_ts`, `kotlin`, `k8s`, `k8s-operator`, `skill-md`) and decides activation by filename or content signals, never by path alone.
- `review-process.md`: the detailed 12-step procedure, the output template and the next-steps prompt.

I didn't read `review-isolated.md`, because it only applies to `:isolated` mode.

**SessionStart root:** `printenv TOOLBOX_PLUGIN_ROOT` returned `/tmp/fr-advisory-actors-20261017/binding-claude-baseline/plugins/kk`. It's set and points to the selected plugin, inside the workspace.

**kk:code-reviewer agent:** I gave it that path as its plugin root and told it not to touch subject files. It read one file: `/tmp/fr-advisory-actors-20261017/binding-claude-baseline/plugins/kk/skills/review-code/SKILL.md`.
- **No separate methodology file to read:** the agent says its own definition only requires the checklists at `<plugin root>/profiles/<profile>/review-code/<checklist>` that the calling workflow passes in. Because no profiles were detected and passed, there were no checklist paths to load. In that case it uses general guidance written into its definition, which isn't a separate file.
- **Files it skipped:** it treated `shared-*.md`, `review-process.md` and `review-isolated.md` as instructions for the skill runner, not the sub-agent. It also skipped `_shared/review-scope-protocol.md`, which only applies when a Task Scope block is passed.
- **Files it couldn't read:** none, and it accessed nothing outside the plugin root.

The agent's answer only shows which methodology file paths would be used once a real review passes detected profiles in. No checklist content was actually loaded during this check.
