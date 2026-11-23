# Claude launch layer

Linux, Claude Code 2.1.296, 2026-11-20. The probe ran `install.sh --local` in a disposable home and invoked the installed `~/.local/bin/kk claude` from a separate workspace. The real CLI loaded the settings and executed the tools. A loopback Messages API fixture recorded the outgoing effort and returned deterministic tool requests. The probe used a local test key.

| Wrapped session | Observation |
| --- | --- |
| No effort preference | The outgoing Opus request used `high`. |
| Legacy top-level user effort set to `low` | Opus 4.6 used `low`. Opus 5.5 used its vendor default of `medium`. |
| Project effort set to `xhigh` | Opus 5.5 used `xhigh`. |
| Per-model user effort set to `low` | The request used `low`. The fixture wrote `modelSettings.claude-opus-5-5.effortLevel` in the user settings file, the format Claude saves for a per-model choice. |
| Adopter file passed with `--settings`, containing `disableAllHooks: true` and an empty deny list | Claude read the public control file. Its second Read returned a native permission-settings error for the decoy `.env`. |

Capture `9da040e0-686f-4c63-9139-00d7045a59a7` contains these observations. The effort cases exercised the saved setting across fresh sessions. The probe wrote the setting directly. The earlier top-level `medium` control matched the vendor default, so the repeat used distinct values on both models.

A separate no-tools control showed why the launcher validates the composed file. Claude accepted a file with low effort, then silently fell back to medium when the file also contained a numeric statusline. The structured `get_settings` response identified the field error and omitted the flag source. The corrected launcher exited before a model request for both an invalid statusline and a numeric effort. A valid low-effort control still succeeded. Captures `7cb5a653-4c29-4500-b803-c4b65e9d0e66`, `9c6cfa6a-a0b0-43e4-86e0-af9cf5373f5f` and `b170fd52-1896-4953-84e4-5131c41836b4`.

`bash test/test-kk.sh` passed all 36 launcher, installation and lifecycle tests (final capture `48138517-4544-4176-9902-1b012d07f39a`). The generator and plugin structure suites passed. `make check-guard` passed in a disposable checkout with the candidate files staged, exercising the same tracked and untracked freshness checks as CI (capture `517e4876-f7db-4e96-bee7-92c484cb4d98`).

The repository-wide run with Python 3.11.13 and jq 1.6 passed 16 of 17 suites (capture `a3f6b639-9c9f-4525-bf7a-225cd6656ece`). Template sync failed the same malformed-base diagnostic assertion reproduced before this feature. The initial run with the host’s Python 3.10 also lacked the TOML parser used in the Codex structure and functional review tooling checks. Both passed on 3.11. [Pre-feature result](../task-3/README.md)

The command guard rejected deletion of the two probe scripts and the temporary review files because `rm` is irreversible. They remain under `/tmp/kk-task6-probe.py`, `/tmp/kk-task6-validation.py`, `/tmp/kk-task6-review-lkks72dj/` and `/tmp/kk-review-instructions-0_fmwfb6/`.
