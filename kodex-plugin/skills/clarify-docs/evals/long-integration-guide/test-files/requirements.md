# Warehouse reservation contract

This synthetic repository is shared with the editor and reservation-client engineers.
Every supplied file is accessible to that audience. The contract is a candidate;
`backend.py` is its sequential behavioral model, not a deployed HTTP service.

## Accepted behavior

One warehouse default controls the minimum stock remaining after a reservation. A
SKU without a stored `reserveRule` inherits the current default. An override replaces
it completely. Exactly one mode is allowed: `{kind: "none"}` or
`{kind: "minimum", units: N}`, where N is an integer from 1 through 1000. Booleans,
extra fields and combined modes are invalid. None removes the minimum restriction;
the SKU must still be enabled and have stock for one unit.

For `PATCH /skus/{id}`, omission of `reserveRule` preserves it, an object replaces it,
and null removes the field. Unrelated edits omit it. Latest committed explicit edits
win; there are no editor-version tokens. Stored null is invalid. An inherited read
returns null as `reserveRule`, the resolved `effectiveReserveRule`, and
`ruleSource: "warehouse"`; an override has `ruleSource: "sku"`. Public reads expose
`id` and `label`, without stored audit state.

`PUT /skus/reserve-rule` receives `skuIds` and a required `reserveRule`, including
null for removal. Accept 1–50 distinct nonempty IDs. Missing selected IDs return 404
`SKU_NOT_FOUND` with only those submitted IDs in `data.affectedSkus`; none of the
selected rows changes. Invalid requests return 400. Valid requests while inactive
return 409 `CONFIGURATION_INACTIVE`. Client `enabled` and `mode` writes are rejected.

Mina decided on **2026-02-10** that one bulk action must have one all-or-nothing result.
Do not automatically split a larger selection into multiple commits. Have the admin
choose at most 50 IDs. Refetch after individual, bulk or warehouse-default saves;
keep unsaved input and selection on failures.

`POST /reservations/preview` accepts `skuIds`, from zero through 50 distinct nonempty
IDs. Each selection requests one unit. A 200 `PREVIEW_EVALUATED` response contains
`data.allowed` and `data.rejected`; it may allow no SKUs. Rejected entries retain IDs
and reasons, including disabled or missing SKUs. It changes no stock.

`POST /reservations` accepts one through 50 selected IDs, rechecks current rules and
rows, and returns 409 `RESERVATION_REJECTED` if any selection fails, changing no stock.
Success reserves one unit of every selected SKU. Preview never reserves stock.
Keep rejected selections visible with their reasons; a missing SKU needs no invented
label. Distinguish a failed preview (unknown availability) from an evaluated empty
result. Proxies preserve HTTP status and the complete `{code, message, data}` body;
older errors may omit data, and data presence never establishes success.

## Release and evidence

Global enablement is server controlled. Staged typed defaults alone are inactive.
Before activation Mina needs validated defaults for every warehouse, compatible
serving writers, actual proxy/status/error and database persistence/isolation
verification, and a final readiness check protected against intervening writes.
The final check and switch write must be protected by a transaction or a controlled
write pause. Recovery retains enforcement; disabling requires reviewing all active
rules. No deployment approval or end-to-end passing result is recorded here.

The model supplies outcome examples and shows validation before updates. Its in-memory
calls do not prove database isolation, HTTP serialization, authentication or proxy
propagation. The release work owns those checks. Public DTOs must not expose audit
state, regardless of type assertions.

Lea has not decided whether bulk edits need a confirmation dialog. It is a proposal,
not a required or implemented step. Lea must decide its presentation before the UI
work closes; this does not change the accepted atomic-write requirement.

## Historical context supplied with the guide

Early review notes discussed naming the DTO `ReserveView` versus `SkuRuleView` and
included an artificial `editorEmail` response fixture. That field never became part
of the contract. Neither discussion changes what the client sends or consumes.
They are obsolete review history. In contrast, Mina's dated no-chunking decision,
Lea's open decision, and the model's evidence limits remain consequential.
