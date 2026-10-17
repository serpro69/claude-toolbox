# Settings protocol

`PUT /settings` accepts a JSON object with one `display_name` member.

| Value | Protocol v1 | Protocol v2 |
| --- | --- | --- |
| String | Store the string after removing leading/trailing Unicode whitespace | Same as v1 |
| Empty string (including a whitespace-only string after normalization) | Store an explicit empty label | Same as v1 |
| `null` | Return HTTP 422; leave the stored value unchanged | Remove the explicit label; subsequent reads use the account default |

Here, surrounding Unicode whitespace means exactly the characters removed by
Python's `str.strip()` with no argument. Both provider versions use this same
definition and preserve internal whitespace. A successful write returns
`{"ok": true}`. A transport returns that response on success and raises on
non-success HTTP status. The client receives a borrowed transport; it neither
owns the connection nor retries calls. These are versioned protocol semantics,
not a record of which version a deployment runs.
