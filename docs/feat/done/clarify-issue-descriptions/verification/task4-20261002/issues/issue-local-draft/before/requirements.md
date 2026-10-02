# Export timeout contract

For synchronous export, timeout_ms=0 means do not wait; missing or null timeout_ms
uses 30000 milliseconds. Asynchronous export is outside this issue. The supplied
source is from 2.3.1, but no execution evidence is supplied. Mina owns confirming
the reported build before a fix is chosen.
