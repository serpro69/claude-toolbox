# Zero wait is ignored in synchronous export

A synchronous export of a ready invoice reportedly waits 30 seconds when given
`--timeout-ms 0`, delaying maintainers checking the invoice.

The [timeout contract](requirements.md) requires synchronous export to treat
`timeout_ms=0` as “do not wait.” A missing or null timeout uses the default of
30000 milliseconds. Asynchronous export is outside this issue.

## Reported reproduction

- Environment: ExportKit 2.3.1, macOS 15 arm64.
- Precondition: `invoice-17` is ready.
- Command: `exportctl send invoice-17 --timeout-ms 0 --mode sync`.
- Expected: zero wait.
- Observed: waited 30 seconds in 3/3 attempts.

## Source evidence and confirmation

The supplied [ExportKit 2.3.1 source snapshot](export.py) computes the effective
timeout with `timeout_ms or 30000`. This replaces numeric zero with 30000,
conflicting with the zero-wait requirement.

The fallback is a suspected cause of the reported wait, but that runtime cause
remains unverified. No execution evidence accompanies the source snapshot. Mina
must confirm on the reported build before a fix is chosen.

## Follow-up

- [x] Record command and environment
- [ ] Mina: confirm on the reported build
- [ ] Choose fix after confirmation
