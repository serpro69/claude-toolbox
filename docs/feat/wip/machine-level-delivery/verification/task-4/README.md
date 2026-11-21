# Claude upgrade and rollback verification

Linux, 2026-11-20. The first-install and lifecycle suites ran with isolated Python and a stateful stub Claude CLI. A separate open-session probe used the real Claude Code 2.1.296 CLI, plugin registration, hook runner and filesystem. Its model responses came from a loopback fixture.

## Automated recovery cases

Run `bash test/test-kk.sh` from the repository root. The suite exercises the installed symlink, the dispatcher inside a retained release, and the actual journal. Fixture releases log which release stages, validates, activates and restores. The fixture exits with status 79 immediately after a chosen checkpoint writes the journal. The next command runs in a fresh process.

| Case | Evidence |
| --- | --- |
| Interruption at placement, marketplace write, registration, plugin install, verification, stable dispatcher write, link publication and promotion | Each interruption was followed separately by `kk upgrade` and `kk rollback`. Status named the mixed releases and the available recovery commands. Both paths restored the expected catalog, dispatcher and state. |
| Promoted release’s Python unavailable | The stable dispatcher restored its predecessor. With the stable dispatcher broken too, the recovery command printed by the upgrade restored the predecessor. An interrupted rollback could be retried with the promoted CLI still unavailable. |
| Interrupted dispatcher publication | The previous dispatcher stayed in place through mixed activation. On both sides of the post-promotion rename, a fresh process could finish from the validated bytes offline or roll back. Recovery also replaced a damaged dispatcher symlink without changing the foreign file it referenced. |
| Tagged candidate retained after interruption | After rollback, the candidate kept its source and digest. Requesting its tag again ran from the same verified directory with network access denied by the test. |
| Retention | A release active for a month and a previously unrecorded placed release both received a fresh supersession timestamp. The active release, rollback target and a release exactly 14 days old were retained. An eligible older release was pruned. |
| Bytecode and source integrity | A cache file published during the fingerprint walk left the digest unchanged. Changing the guard source blocked resume, and offline rollback remained available. |

The 25-test suite passed on CPython 3.10.12 (capture `0eed5fca-4e0c-469a-b77c-9cce26d15587`) and 3.8.20 (`541de22e-d28c-4d50-aa60-b6ec0bde806a`). ShellCheck passed for `install.sh`, `kk/bin/kk` and the suite wrapper.

The repository-wide run passed 16 of 17 shell suites with Python 3.11 and jq 1.6 (`2b3ab6d9-78b5-4187-ad6b-c6e441673478`). The template-sync suite reproduced the malformed-base diagnostic failure recorded before Task 4. [Task 3 baseline](../task-3/README.md)

Both fixture releases contain the lifecycle implemented in Task 4. The earlier, untagged Task 3 snapshot dispatched only first installs and status. Its active CLI cannot upgrade itself, and its saved dispatcher cannot restore it by invoking a rollback command.

## One open Claude session across recovery

The probe installed a local release into a disposable `HOME`, `KK_HOME` and `CLAUDE_CONFIG_DIR` and ran `kk upgrade --local <checkout>`. A wrapper returned 17 on `claude plugin list --json` after the marketplace pointed to the candidate. The journal still named the original active release. The probe started Claude in a scratch workspace with `KK_GUARD_INTERPRETERS` set to Python 3.11. The candidate’s validation run had used Python 3.10.

```sh
claude -p --input-format stream-json --output-format stream-json --verbose \
  --include-hook-events --strict-mcp-config --tools Read --model haiku --no-session-persistence
```

The process stayed open on stdin. For each user turn the local Messages-compatible fixture requested one `Read` of a distinct public marker file and then ended the turn. The probe checked the file contents in the tool result. The CLI emitted a successful result and a `PreToolUse` hook response on each turn.

| Point in the run | Observation |
| --- | --- |
| After marketplace switch | The session loaded candidate `local-9e7e9d30ffde4d41855185c5e186e0d0` and read `first.txt`. Its hook created `guard.cpython-311.pyc`. |
| After `kk upgrade` with no arguments | The same candidate was promoted in directory inode 2622696. Validation cleared the derived 3.11 cache. The open session read `second.txt` and regenerated it. |
| After `kk rollback` | The catalog and journal restored `local-ec61a3ff3ead41c58ffedb4ffcc07ce0`. The open session still reported the candidate’s plugin root, read `after-rollback.txt`, and retained the same inode. |

All three turns used session `3fd26679-4f18-412a-b2fc-41d315bf1795`. After the session exited, a second rollback verified the retained release digest and restored the same directory. Capture `3c0cce1f-94ff-4b2e-aaf0-52d18ef94853` contains the terminal outcomes. An earlier run timed out because the response fixture repeated its tool request. The completed run fixed the fixture to issue one tool call per turn. The probe used no real account credentials. macOS and a published release tag were outside this run.
