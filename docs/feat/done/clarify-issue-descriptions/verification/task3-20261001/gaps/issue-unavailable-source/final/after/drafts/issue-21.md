# Zero wait still waits

On ExportKit 2.1 / Ubuntu 24.04, requesting a zero timeout reportedly caused a 30-second wait in 2 of 3 attempts. The expected result is an immediate return. The wait delays checking the invoice.

## Reported reproduction

Run:

```sh
exportctl send invoice-21 --timeout-ms 0 --mode sync
```

- **Environment:** ExportKit 2.1 / Ubuntu 24.04.
- **Expected:** Immediate return when `--timeout-ms 0` is requested.
- **Observed:** A 30-second wait in 2 of 3 attempts.

## Investigation and scope

The reporter suspects that zero is replaced with a default timeout, but the cause is unconfirmed. No fix has been agreed. Async export is out of scope.

The referenced [v2.1 source](https://source.example.invalid/export/revision/v2.1/export.py) is unavailable because access was denied. No source, tests, logs, PR or alternate copy was accessible for this revision; the reported behavior has not been independently verified.

Mina owns obtaining an accessible v2.1 source snapshot. An owner for reproduction and cause confirmation still needs to be assigned. Once the source is available, reproduce on the reported version and compare timeout handling before choosing a fix.

- [x] Record command and environment
- [ ] Mina: obtain accessible v2.1 source
- [ ] Assign reproduction/cause owner
