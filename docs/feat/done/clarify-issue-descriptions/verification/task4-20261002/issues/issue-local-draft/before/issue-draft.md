# Zero wait is ignored in synchronous export

The `timeout_ms` path and its fallback seem relevant, see [source](export.py).
Not async export. Mina still needs a confirmation on the reported build before
we choose a fix. [Requirements](requirements.md) say zero means don't wait.

ExportKit 2.3.1, macOS 15 arm64. With invoice-17 ready, run
`exportctl send invoice-17 --timeout-ms 0 --mode sync`. It waited 30 seconds in
3/3 attempts, expected zero wait. This holds up maintainers checking a ready invoice.
I suspect zero is being replaced by the default; I have not verified that cause.

- [x] Record command and environment
- [ ] Mina: confirm on the reported build
- [ ] Choose fix after confirmation
