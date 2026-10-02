# Zero wait is ignored in synchronous export

Synchronous export reportedly waits 30 seconds when `--timeout-ms 0` requests no
wait, holding up maintainers checking a ready invoice. The
[timeout contract](requirements.md) requires `timeout_ms=0` to mean do not wait;
a missing or null value uses the 30000-millisecond default. Asynchronous
export is outside this issue.

The report describes ExportKit 2.3.1 on macOS 15 arm64, with invoice-17 ready:
`exportctl send invoice-17 --timeout-ms 0 --mode sync`. The reported result was a
30-second wait in 3/3 attempts; the expected result was zero wait.

The supplied [2.3.1 source snapshot](export.py) shows that
`effective_timeout(timeout_ms)` returns `timeout_ms or 30000`, so a value of `0`
becomes `30000`. This supports the suspected cause, but the snapshot provides no
runtime verification of the reported behavior. Mina must confirm on the reported
build before a fix is chosen.

- [x] Record command and environment
- [ ] Mina: confirm on the reported build
- [ ] Choose fix after confirmation
