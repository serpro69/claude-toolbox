# Zero wait still waits

On ExportKit 2.1 / Ubuntu 24.04, synchronous export reportedly waited 30 seconds despite a requested timeout of zero. This delays checking the invoice.

## Reported reproduction

Command:

```sh
exportctl send invoice-21 --timeout-ms 0 --mode sync
```

- Expected: return immediately when zero is requested.
- Observed: a 30-second wait in 2 of 3 tries.

The reporter suspects that zero is replaced with a default timeout. The cause is unconfirmed, and the available material does not establish independent reproduction.

## Evidence and next steps

The [v2.1 source reference](https://source.example.invalid/export/revision/v2.1/export.py) is unavailable: the supplied read-only access response was access denied. No source, tests, logs, PR or alternate copy is accessible to verify the report.

Mina owns obtaining an accessible v2.1 source snapshot. Once it is available, reproduce on the reported version and compare timeout handling before choosing a fix. The owner of reproduction and cause confirmation has not been assigned.

- [x] Record command and environment
- [ ] Mina: obtain accessible v2.1 source
- [ ] Assign reproduction/cause owner

Async export is out of scope. No fix is agreed.
