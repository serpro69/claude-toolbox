# Zero wait is ignored in synchronous export

Synchronous export is reported to wait 30 seconds when zero wait is requested,
holding up maintainers checking an invoice that is ready. Asynchronous export is
outside this issue.

## Reported reproduction

Environment: ExportKit 2.3.1, macOS 15 arm64.

With `invoice-17` ready, run:

`exportctl send invoice-17 --timeout-ms 0 --mode sync`

- Expected: no wait.
- Observed in the report: a 30-second wait in 3/3 attempts.

## Contract and source evidence

The [requirements](requirements.md) specify that synchronous export must not wait
when `timeout_ms=0`; a missing or null timeout uses the 30000-millisecond
default.

The supplied [2.3.1 source snapshot](export.py) uses `timeout_ms or 30000` in
`effective_timeout`, which replaces zero with 30000. This conflicts with the
zero-wait contract and supports the suspected fallback cause. Source inspection
does not establish that this helper caused the reported wait; no execution
evidence was supplied.

## Next steps

Mina must confirm the behavior on the reported build before a fix is chosen.

- [x] Record command and environment
- [ ] Mina: confirm on the reported build
- [ ] Choose fix after confirmation
