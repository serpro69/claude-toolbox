# Warehouse reservation integration

This guide is for the engineers building the warehouse editor and reservation client.
Warehouse owners need a default minimum remaining stock and exceptions for individual
SKUs. A SKU is the identifier for a stock item. This increment adds typed rules,
rule editing, a preview and a current-data check when reserving. Each reservation
requests one unit of every selected SKU; quantities and restocking are outside scope.

For example, a warehouse requires 10 units to remain. Two enabled SKUs each have 8
units: A inherits the default and B explicitly has no minimum. Reserving A would
leave 7, so A fails; B can be reserved. Preview describes these decisions without
changing stock. Trying to reserve both together rejects the complete selection.
Staged defaults do not activate the feature. Release verification remains pending,
and Lea has not decided whether bulk edits should show a confirmation dialog.

The candidate contract and its in-memory behavior are described by
[requirements.md](requirements.md) and [backend.py](backend.py). Normal integration
review still applies. The sections below collect the endpoint behavior and the
implementation notes accumulated while reviewing that contract.

## Public data and implementation notes

`read_sku` constructs a public view with `id`, `label`, `reserveRule`,
`effectiveReserveRule` and `ruleSource`. The storage row can contain additional audit
state; that state does not belong in a public response. A client should consume the
public fields rather than spread an arbitrary stored row into its own view model.
The effective value is calculated when reading, which means an inherited SKU can
show a different effective rule after a warehouse edit without a SKU write.

The original type discussion called this object `ReserveView`. A later review used
`SkuRuleView` to distinguish it from reservation outcomes. Neither name is a wire
field, and the final name of a frontend type alias is not prescribed by this guide.
The discussion was retained because both names appeared in review comments and
someone comparing those comments with current examples might otherwise wonder
whether there were two subtly different response variants.

Another review fixture included `editorEmail` at the top level. That was an artificial
example, not an established response field. Its removal did not change audit storage
or authorize changing an audit identity. It was useful for discussing projection
boundaries, although consumers do not need to implement a compatibility branch for
its presence. The public model deliberately has no such field.

Model functions return a status alongside a body. Status is HTTP metadata; the JSON
envelope contains `code`, `message` and sometimes `data`. The existence of data does
not turn an error into a success. This distinction matters when adapting these
examples to a proxy, because validation and compatibility failures can themselves
have useful structured data. Older errors may contain only code and message.

## Rules and editor operations

There is one rule at each configured scope. The values are `{"kind":"none"}` and
`{"kind":"minimum","units":10}`. Minimum units are integers from 1 through 1000;
zero uses explicit none. Boolean units, extra members and combinations are rejected.
No minimum still requires an enabled SKU and stock for the requested one unit. A
warehouse rule is completely replaced by an item override, never combined with it.

`PATCH /skus/{id}` accepts label edits and a `reserveRule` instruction. An omitted
rule stays unchanged, an object replaces the whole rule, and null removes the stored
override. `PUT /skus/reserve-rule` applies one instruction to the explicitly selected
IDs. Both routes reject ordinary typed writes while inactive. See
[the later edit note](#edit-safety) for the practical concurrency consequence.

In the model, `updated_row` first builds a new dictionary. It removes a key for
null and copies validated objects for replacement. The bulk function builds pending
rows before applying them. The structure makes the all-or-nothing outcome visible
in one sequential call; it should not be mistaken for evidence about the eventual
database SDK, its transaction retries, or the HTTP response after a network failure.

The type review also asked whether a single wider interface would be easier than a
tagged union. That discussion did not approve combined modes or unknown fields.
The consumer contract remains exactly one valid kind. A compiler's acceptance of a
sample object cannot replace a check of actual response JSON, particularly when a
proxy maps or flattens responses before the browser sees them.

Inherited reads represent absence using `reserveRule: null`, include the current
effective rule, and set `ruleSource: "warehouse"`. Explicit none reports source
`"sku"`. The distinction allows the editor to explain why two visually unrestricted
rows may respond differently to a later warehouse-default change. Null on the wire
is a representation, not permission to store a null rule in the row.

## Previewing selected SKUs

`POST /reservations/preview` takes `skuIds`, with zero through 50 distinct nonempty
identifiers. Each ID requests one unit. An empty selection is useful before choosing
items. The body is evaluated against the supplied current rows and default. A 200
`PREVIEW_EVALUATED` body has `data.allowed` and `data.rejected`; a rejected entry
contains its submitted ID and reasons, which can include `LOW_STOCK`, `SKU_DISABLED`
or `SKU_NOT_FOUND`.

The model uses the public projection to resolve each effective rule. It collects
allowed IDs and rejected entries separately. That organization also supports mixed
examples in which an inherited minimum rejects one SKU while an explicit none
allows another. The model does not need a special branch called an exception menu
or a second inventory representation for those outcomes.

During review, an earlier example had only a rejected row. Another example added an
allowed row so readers could see both lists populated. Neither example is a complete
browser integration test. Both are useful for reviewing the public result shape,
and the mixed example avoids assuming that a successful evaluation means the
complete original selection is eligible. This point also appears in the later
confirmation discussion because the two endpoints serve different purposes.

An empty `allowed` array is a successful evaluation when the response is 200. A failed
request instead leaves availability unknown. A missing SKU has no guaranteed label;
keep its ID and reason visible without inventing metadata. Rejected selections stay
selected until the user removes them. A proxy must not transform either an error
body into a successful empty preview or a populated error body into success.

## Confirming a reservation

`POST /reservations` takes one through 50 selected IDs. It reloads the applicable
data in the eventual service and evaluates the current rows and rules again. In the
model, `confirm` calls `preview` over the current input immediately before applying
stock changes. An earlier preview cannot reserve stock, lock a rule or guarantee a
later successful submission. A stock change between the calls can change the result.

For the example in the introduction, confirming A and B returns 409
`RESERVATION_REJECTED` because A fails. Neither SKU loses a unit. Selecting only B
can succeed while it remains enabled and stocked. All selected items must pass;
there is no partial order or automatic removal of rejected entries. On success the
result is 200 `RESERVED`, with the selected IDs in `data.reservedSkus`.

The code's loop appears after the rejection branch. This is useful source evidence
for zero changes on a sequential rejection. It does not demonstrate concurrent
database isolation, authorization checks, proxy serialization, or deployed behavior.
Those checks remain with release verification. Review of a model and review of
serving software are different evidence, even if they share identical field names.

The wire envelope again contains code, message and optional data. A proxy should
carry the original HTTP status and complete body to the client. The original editor
examples and the reservation examples share this rule. The client must not infer
success solely because it can access `data`, and must not assume older errors always
have it. Keep the user's selections when the operation fails.

## Bulk request and examples

`PUT /skus/reserve-rule` requires `skuIds` and an explicit `reserveRule` value. IDs
must be distinct and nonempty, and the request accepts 1–50 of them. Objects replace
the complete rule; null removes it. For example:

```json
{"skuIds":["A","B"],"reserveRule":{"kind":"minimum","units":10}}
```

Success returns 200 `RULES_UPDATED` and `data.updatedSkus`. If B does not exist, the
response is 404 `SKU_NOT_FOUND`, with `data.affectedSkus: ["B"]`; neither A nor B
changes. The affected list contains only offending submitted IDs, not every unchanged
row. Invalid input returns 400. A valid typed write while disabled returns 409
`CONFIGURATION_INACTIVE`. Requests cannot set the server's `enabled` or `mode` fields.

The batch model prepares a map of changed dictionaries. It validates IDs and the
replacement before updating the supplied rows. That structure makes replacement and
removal comparable without maintaining two persistence algorithms in the example.
It still does not establish the behavior of a database transaction or a proxy that
has already sent a response. Source inspection and wire verification remain separate.

Reviewers discussed whether a future transport helper should return a response object
or separate status/body values. The current model uses a pair for convenience. The
pair itself is not the JSON body. Frontend code must preserve the backend's actual
status and the full envelope regardless of its helper's internal return type.

The request limit is part of the user action's semantics. The decision about larger
selections is recorded under [review evidence](#bulk-safety), rather than inferred
from whatever limit a database SDK might support. Successful saves require a later
read to display inherited effective values and other admins' intervening edits.

## Deployment notes

The new typed data is inactive until the global server-controlled switch is enabled.
Ordinary typed saves are rejected before that point. Staging defaults is preparation,
not activation. All serving writers must support the new contract before enablement;
otherwise a request can reach software that does not enforce the configured rules.
Every warehouse needs a valid default, even if many SKUs have their own overrides.

The model intentionally accepts `active` as an injected argument for editing. It is
supplied from trusted server configuration, not accepted as a request field. This
makes before/after examples straightforward without implementing production flag
storage inside the fixture. Copying that argument into a browser-editable property
would change the authority boundary and would not implement this contract.

The sample can be read locally without a server or database. That convenience helped
reviewers discuss shapes before selecting the eventual persistence implementation.
It does not show the actual proxy forwarding statuses correctly. The final release
evidence must cover those serving components, along with actual persistence and
isolation. No passing end-to-end result or deployment approval is recorded here.

## Review evidence and remaining notes

<a id="edit-safety"></a>

When saving an unrelated label change, omit `reserveRule`. Resending an earlier read
is an explicit replacement, so it can overwrite another admin's newer choice. The
latest committed explicit rule edit wins, without editor-version tokens or conflict
dialogs. Inheritance means the stored key is absent; stored null is invalid. This
storage detail differs from the null returned by an inherited read and from the null
instruction that removes an override.

After individual, bulk and warehouse-default saves, refetch the public reads to show
current effective rules. An acknowledgement describes the completed change, not a
promise that another admin has made no subsequent edit. On failure preserve the
selection and unsaved input. These behaviors apply to the editor regardless of
whether it displays the source badge inline or in an expanded row.

<a id="bulk-safety"></a>

Mina decided on 2026-02-10 that one user action must have one all-or-nothing result.
Do not automatically split 51 selected SKUs into independently committed chunks.
Have the admin select at most 50 instead. The reason is observable partial success:
the first chunk could commit and the second fail, leaving the admin with neither
the promised single result nor an unchanged selection. This qualification survives
any future increase in a database provider's technical batch limit.

<a id="rollout"></a>

Mina owns release readiness. In addition to validated defaults and compatible serving
writers, require actual proxy/status/error tests and database persistence/isolation
verification. Protect the final readiness check and switch write against intervening
configuration changes using a transaction or a controlled write pause. An earlier
successful staging run does not establish that the configuration is still ready.

Recovery keeps enforcement in place. Disabling the feature requires an explicit review
of every active rule; keeping typed fields in storage does not make disabled enforcement
safe. Mina owns that review and rollout evidence. Lea separately owns the proposed
bulk-confirmation dialog: she must decide its presentation before the UI work closes.
The dialog is not yet required or implemented, and its absence does not waive atomic
writes. The small model establishes neither completion of those tasks nor approval
to enable the feature.
