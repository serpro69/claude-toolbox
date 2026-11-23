# Claude first-install verification

Linux, 2026-11-20. The first-install tests exercise the repository installer, a standalone copy, the release dispatcher and the candidate guard. They run in temporary homes. The tag tests substitute the GitHub HTTP responses so the installer consumes a real archive without publishing a release.

| Check | Result |
| --- | --- |
| `bash test/test-kk.sh` | All 18 tests passed on CPython 3.10.12 (`2b8cb15d-d736-4eec-9e32-61a0db74c7f0`) and 3.8.20 (`8af96c8c-dce2-4943-bea1-0097605b993e`). Cases cover a clean checkout, tagged archives, path containment, validation failures, symlink ownership, competing writers, state preservation and standalone recovery. |
| `shellcheck install.sh kk/bin/kk test/test-kk.sh` | Passed. |
| Existing plugin structure, guard engine and plugin-root suites | `bash test/test-plugin-structure.sh`, `bash test/test-guard.sh` and `bash test/test-cpr.sh` passed. |
| Claude Code 2.1.296 | Installed the full checkout at user scope in a disposable Claude configuration. The vendor validator passed with warnings about existing command files without YAML frontmatter. |

For the recovery probe, a standalone copy of `install.sh` ran with `--local <checkout>` and a private `HOME`, `KK_HOME` and `CLAUDE_CONFIG_DIR`. A wrapper forwarded every command to the real Claude CLI and returned 17 immediately after a successful `claude plugin install`. At that point the journal recorded candidate `local-2ac9c0c5a8794400b0cd5dcd06d9c79d` in phase `activating`. The second invocation used the real CLI directly and took no installer arguments.

```text
Active: local-2ac9c0c5a8794400b0cd5dcd06d9c79d
claude: ready
Rollback target: none
```

The matching `kk@toolbox` inventory entry was enabled at user scope. Its `readFromFolder` resolved to the promoted release’s `klaude-plugin/` directory. Capture IDs are `3ea8a6fb-381c-4924-8d38-bf6e999ae0cb` for clean install and `2bc4499e-4d56-434c-a6f1-41ba683452d6` for interruption and recovery. The probes used temporary directories and did not register anything in the maintainer’s Claude configuration.

The marketplace name is a pre-tag decision. A public tagged download, macOS and upgrades from an already active release are outside these results.

The repository-wide run passed 16 of 17 suites with Python 3.11.13 and jq 1.6 (`0ce30727-ae33-417f-b722-92a9e053a207`). The template-sync suite expected the malformed merge base to log “unexpected shape”. The same assertion failed on an archive of the pre-implementation commit `60661249` (`2f1f8b1c-be51-49f0-ab0b-043e7bf11cb8`).
