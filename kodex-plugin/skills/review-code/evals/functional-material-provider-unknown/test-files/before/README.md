# Settings client

Python 3.9+, standard library only. The public `save(transport, display_name)`
accepts strings (including empty strings) and preserves the transport response
and exceptions. Other input types to `save` are outside its contract.
See [the versioned provider protocol](protocol.md).

This increment adds `clear_name(transport)`: request removal of the explicit
label so the account default is used. Sending an empty label is not equivalent.
The new operation can be called immediately after the client is deployed; it has
no local activation flag. Existing `save` behavior must remain unchanged.

Run local tests with `python3 -B -m unittest discover -s tests -v`.
The test transport records requests; it does not implement a provider.
