# Claude plugin session delivery

Linux, 2026-11-20, Claude Code 2.1.296. The probe ran in a disposable home. A loopback Messages API fixture checked the outgoing model input for each complete packaged Markdown file. It returned a short text response. The plugin installation, hook execution and environment file were handled by the real Claude CLI.

| Startup case | Behavioral text in model input | Plugin-root guidance in model input | Root exported by Claude’s session hook |
| --- | --- | --- | --- |
| Git marketplace, clean project | Yes | Yes | Versioned Git-plugin cache |
| Managed release, clean project | Yes | No | Loaded release’s `klaude-plugin/` |
| Managed release, project has `.claude/CLAUDE.extra.md` | No | No | Same release directory |
| Managed release, `claude.instructions` is `false` | No | No | Same release directory |

For the first case the probe registered a Git marketplace backed by a disposable local Git repository and installed `kk@claude-toolbox` at user scope. It then removed that installation and ran `./install.sh --local <checkout>` to install the managed release. Each case started a new `claude -p` session with `--strict-mcp-config --include-hook-events --output-format stream-json --verbose --no-session-persistence`. During the request, the probe matched the `TOOLBOX_PLUGIN_ROOT` export in that session’s environment file to the plugin path in Claude’s startup inventory. Capture `7e7a73c3-c24b-4a70-8b72-56970d6e6944` records all four results.

The shell fixtures also dispatched the registered hook for `resume`, `clear` and `compact`. They checked independent suppression of the two legacy sections, successful silence on opt-out, a diagnostic for an invalid switch, and root selection with a stale registry, a symlinked toolbox home and an interrupted custom-home install. These three event types were checked at the hook interface. The live probe covered startup.

| Repository check | Result |
| --- | --- |
| `bash test/test-hooks.sh`, `bash test/test-claude-extra.sh`, `bash test/test-cpr.sh` | Passed. The four legacy files matched their canonical sources byte for byte. |
| `make generate-claude-assets generate-kodex plugin-graph` | Passed, including the Go tests, both structure suites and graph validation. The Codex generator updated the matching profile guidance about root resolution. |
| ShellCheck on the three root/instruction hook scripts and Bash syntax checks on the two statusline scripts | Passed. |
| Full shell suite with Python 3.11 and jq 1.6 | 16 of 17 passed. Template sync again failed the previously recorded malformed-base diagnostic assertion. [Baseline](../task-3/README.md) |

The earlier probe that asked the model to print the root with Bash was inconclusive because the local fixture did not implement Claude’s auto-mode classifier. The completed probe read the session environment file directly. Launcher selection of a statusline is covered by Task 6.
