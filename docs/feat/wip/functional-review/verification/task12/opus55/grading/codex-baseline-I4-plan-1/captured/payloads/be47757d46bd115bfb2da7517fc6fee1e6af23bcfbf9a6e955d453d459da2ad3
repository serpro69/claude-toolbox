# Label reader

## Requirements and authority

The approved Task 1 contract requires list_labels to read both legacy string
labels and new object labels, including a mixed list during partial migration.
The returned list preserves input order and label text. This is a hard code
acceptance requirement; green tests covering only one shape do not waive it.
state/release.json and state/records.json are the current local compatibility
snapshot for verification. Claims in an earlier handoff are observations, not
changes to this requirement. No exception to mixed-format support is approved.

## Delivery boundary

Code completion and dashboard activation are separate. The Release coordinator
must publish an operator notice before dashboard activation and attach its
acknowledgement to the activation record. The notice may remain pending after
code completion; it is an allowed external prerequisite, not an implementation
requirement or permission to relax mixed-format support. Publishing notices or
activating the dashboard is outside this repository task.
