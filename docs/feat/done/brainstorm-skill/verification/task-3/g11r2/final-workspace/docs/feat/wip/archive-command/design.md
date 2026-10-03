# Design: Archive Command

Status: design drafted; implementation not started.

Source of requirements: [README.md](../../../../README.md). Related documents: [implementation plan](implementation.md) and [tasks](tasks.md).

## Problem and User

The owner of a local note collection needs to retire one note while preserving access to it. Archival records the note's state without deleting or relocating the note, hiding it from the ordinary list, or disrupting its links.

The planning workspace contains only README.md. It describes items with stable IDs, titles, bodies, and an archived flag, along with listing and editing behavior. It contains no runtime source or selected language. The integration responsibilities below are proposed; they are not claims about existing functions or files.

## Success Criteria

- Selecting one existing active ID marks exactly that item archived.
- The selected item's ID, title, body, location, and links remain unchanged. Other items remain unchanged.
- The ordinary list still includes the item and distinguishes its archived state using the existing presentation.
- Repeating the command succeeds without another state change or persistence write.
- A missing ID produces an explicit failure and changes no item.
- Operation is local, requires no network access, and introduces no dependencies.

## Command Behavior

The command accepts one stable item ID. Its exact invocation syntax and output formatting follow the eventual runtime's established command conventions.

| Current state | Action | Result |
| --- | --- | --- |
| ID does not exist | Report the missing ID; do not persist anything | Failure; collection unchanged |
| Item is already archived | Complete without persisting again | Success; collection unchanged |
| Item is active | Set only its archived flag and persist through the existing write mechanism | Success after persistence completes |

Lookup failure must remain distinct from an ID that is absent. A persistence error is reported as failure; the command must not claim successful archival. Use the runtime's existing error and persistence conventions. Crash consistency and rollback behavior cannot be claimed until that mechanism is inspected.

The command changes no listing filters, editing rules, identifiers, or link targets. Archived notes remain addressable through their original IDs and visible in the ordinary list.

## Design Decision

Use a direct lookup, validation, and archived-flag update in the command's normal execution path. Reuse the runtime's item lookup and persistence boundary once those are identified. Do not add an archive collection, alternate storage location, or generic decision framework.

| Approach | User value | Feasibility | Differentiation and trade-off |
| --- | --- | --- | --- |
| Direct flag update — selected | Meets the complete requested behavior | Small change using existing item data | Minimal new structure; decision and mutation remain together |
| Separate decision and update | Same observable behavior | Requires a decision representation and executor | Easier isolated decision testing, without a current user need |

## Assumptions

- Stable IDs uniquely identify individual items. Validate against the runtime's lookup rules before implementation.
- The selected runtime has a local item lookup and persistence mechanism that can preserve existing fields. Inspect its behavior before wiring the command.
- Ordinary listing already shows active and archived items distinctly, as README.md states. Confirm with a regression test.
- Existing editing and link resolution preserve IDs and links. Confirm that an archived item remains addressable and editable through those paths.
- No new storage schema is required because the archived flag already exists. Verify this against the actual item representation.

## Not Doing

- Deletion or hiding: these violate preservation and ordinary-list visibility.
- Moving notes or rewriting links: neither is needed to change the archived flag.
- Bulk operations, restore, or synchronization: these are outside this increment.
- Network access or new dependencies: the operation is local and uses existing mechanisms.
- Selecting a language or building a new runtime: this workspace supplies requirements, not an application implementation.

## Rejected Alternatives

- Separate decision/execution: additional structure is not justified for this single command.
- Hiding archived notes: contradicts the requirement to keep notes in the ordinary list.
- Moving notes into a separate archive location: adds unnecessary location and link-preservation risk.

## Verification Strategy

Use a temporary local collection containing an active target note, an already-archived note, an unrelated active note, and links involving the target. Compare stored item data before and after each command, including fields the command does not own.

Verify the active, repeated, already-archived, and missing-ID paths independently. Check the ordinary list and follow the target's original links after archival. Exercise persistence-error reporting using the existing test seam if available; do not introduce a new dependency to do so.

## Implementation Prerequisite

Before coding, identify the runtime repository, selected language, command dispatch path, item lookup/write interfaces, and relevant test entry points. Record concrete paths in the implementation plan. Until then, no executable test command or runtime filename can be established from the supplied evidence.
