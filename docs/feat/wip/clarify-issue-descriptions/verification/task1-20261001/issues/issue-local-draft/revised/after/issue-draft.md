# Zero wait is ignored in synchronous export

Synchronous export reportedly waits 30 seconds when `--timeout-ms 0` requests
no wait, delaying maintainers checking a ready invoice. Asynchronous export is
outside this issue.

## Reported reproduction

Environment: ExportKit 2.3.1, macOS 15 arm64.

With invoice-17 ready, run
`exportctl send invoice-17 --timeout-ms 0 --mode sync`.

- Expected: no wait. The [timeout contract](requirements.md) specifies that
  synchronous export with `timeout_ms=0` does not wait; a missing or null value
  uses 30000 milliseconds.
- Observed: a 30-second wait in 3/3 reported attempts.

## Source evidence and confirmation needed

The supplied [2.3.1 source snapshot](export.py) uses
`return timeout_ms or 30000` in `effective_timeout`. That expression replaces zero
with 30000, conflicting with the timeout contract and supporting the suspected
cause. Source inspection does not confirm that this caused the reported wait;
no execution evidence is supplied, and the reproduction command has not been run
during this edit.

Mina must confirm the behavior on the reported build before a fix is chosen.

- [x] Record command and environment
- [ ] Mina: confirm on the reported build
- [ ] Choose fix after confirmation
