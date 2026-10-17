# Settings client

Python 3.9+, standard library only. The public `save(transport, display_name)`
accepts strings (including empty strings) and preserves the transport response
and exceptions. Other input types are outside its contract. This client supports
both protocol v1 and v2; see [the versioned provider protocol](protocol.md).

This increment normalizes surrounding Unicode whitespace on the client before
sending a name. The stored label must remain identical to the previous client
on both supported provider versions, including empty and whitespace-only names.
Internal whitespace must be preserved. No other operation changes.

Run local tests with `python3 -B -m unittest discover -s tests -v`.
The test transport records requests; it does not implement a provider.
