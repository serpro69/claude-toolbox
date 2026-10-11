I’m using `kk:review-code` for this loading probe. I’ll read its entry point and required methodology, then have a `code-reviewer` agent with no inherited conversation do the same and report the paths it read. I’ll stop before investigation.


Loaded `kk:review-code` and spawned the named `code-reviewer` role with `fork_turns: "none"` and the selected plugin root.

Both read these files under `/home/sergio/.codex/plugins/cache/fr-opus55-c2d28c9e-20261011/kk/0.23.0/skills/review-code/`:

- `SKILL.md`
- `shared-capy-knowledge-protocol.md`
- `shared-profile-detection.md`
- `review-process.md`

The agent also received its role methodology directly in its prompt. Stopped before investigation. No subject files were read or modified, and access stayed within the permitted locations.
