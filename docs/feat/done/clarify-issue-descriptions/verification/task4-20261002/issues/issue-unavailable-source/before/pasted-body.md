# Zero wait still waits

Maybe timeout fallback. On ExportKit 2.1 / Ubuntu 24.04, I ran `exportctl send invoice-21 --timeout-ms 0 --mode sync` and got a 30-second wait, 2 of 3 tries. Expected immediate return when zero is requested. This delays checking the invoice. I suspect the zero gets replaced with a default but haven't confirmed the cause. Mina is getting the v2.1 source; nobody is assigned to reproduce or confirm cause. After it is available, reproduce on the reported version and compare timeout handling before choosing a fix. Async export is out of scope; no fix is agreed.

- [x] Record command and environment
- [ ] Mina: obtain accessible v2.1 source
- [ ] Assign reproduction/cause owner

Source reference: https://source.example.invalid/export/revision/v2.1/export.py
