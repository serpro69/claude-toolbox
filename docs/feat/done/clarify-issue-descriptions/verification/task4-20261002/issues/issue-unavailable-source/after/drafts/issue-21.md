# Zero wait still waits

Requesting a zero timeout for a synchronous export reportedly causes a 30-second wait, delaying the invoice check.

## Reported behavior

Environment: ExportKit 2.1 / Ubuntu 24.04.

Command:

```sh
exportctl send invoice-21 --timeout-ms 0 --mode sync
```

- Expected: immediate return when zero is requested.
- Observed: a 30-second wait in 2 of 3 attempts.

The reporter suspects that zero is replaced with a default timeout. The cause has not been confirmed.

## Investigation and scope

The [referenced v2.1 source](https://source.example.invalid/export/revision/v2.1/export.py) is unavailable: access was denied. No source, tests or logs are accessible to independently verify the report or its suspected cause.

Mina owns obtaining an accessible v2.1 source snapshot. The owner of reproduction and cause confirmation is unassigned. Once the source is available, reproduce on the reported version and compare timeout handling before choosing a fix.

Async export is out of scope. No fix is agreed.

- [x] Record command and environment
- [ ] Mina: obtain accessible v2.1 source
- [ ] Assign reproduction/cause owner
