"""Sequential model of the candidate contract, not an HTTP/database implementation.

Rows and the warehouse default are trusted current inputs. Callers supply active
from server configuration, never from the request body. Concurrency, authorization,
proxy propagation and production activation need separate integration evidence.
"""


def response(status, code, data=None):
    body = {"code": code, "message": code.replace("_", " ").lower()}
    if data is not None:
        body["data"] = data
    return status, body


def decode_rule(rule):
    if not isinstance(rule, dict):
        raise ValueError("Invalid rule")
    if rule == {"kind": "none"}:
        return {"kind": "none"}
    if (
        set(rule) == {"kind", "units"}
        and rule["kind"] == "minimum"
        and type(rule["units"]) is int
        and 1 <= rule["units"] <= 1000
    ):
        return dict(rule)
    raise ValueError("Invalid rule")


def read_sku(row, warehouse_rule):
    default = decode_rule(warehouse_rule)
    override = decode_rule(row["reserveRule"]) if "reserveRule" in row else None
    return {
        "id": row["id"],
        "label": row["label"],
        "reserveRule": override,
        "effectiveReserveRule": default if override is None else override,
        "ruleSource": "warehouse" if override is None else "sku",
    }


def valid_ids(ids, minimum):
    return (
        isinstance(ids, list)
        and minimum <= len(ids) <= 50
        and all(isinstance(item, str) and item for item in ids)
        and len(set(ids)) == len(ids)
    )


def updated_row(row, rule):
    result = dict(row)
    if rule is None:
        result.pop("reserveRule", None)
    else:
        result["reserveRule"] = decode_rule(rule)
    return result


def patch_sku(rows, sku_id, body, active):
    if "enabled" in body or "mode" in body:
        return response(400, "READ_ONLY_FIELD")
    if sku_id not in rows:
        return response(404, "SKU_NOT_FOUND", {"affectedSkus": [sku_id]})
    if "reserveRule" in body and not active:
        return response(409, "CONFIGURATION_INACTIVE")
    next_row = dict(rows[sku_id])
    if "reserveRule" in body:
        try:
            next_row = updated_row(next_row, body["reserveRule"])
        except ValueError:
            return response(400, "VALIDATION_ERROR")
    if "label" in body:
        next_row["label"] = body["label"]
    rows[sku_id] = next_row
    return response(200, "SKU_UPDATED", {"updatedSkus": [sku_id]})


def bulk_patch(rows, body, active):
    if "enabled" in body or "mode" in body:
        return response(400, "READ_ONLY_FIELD")
    ids = body.get("skuIds")
    if not valid_ids(ids, 1) or "reserveRule" not in body:
        return response(400, "VALIDATION_ERROR")
    try:
        rule = None if body["reserveRule"] is None else decode_rule(body["reserveRule"])
    except ValueError:
        return response(400, "VALIDATION_ERROR")
    if not active:
        return response(409, "CONFIGURATION_INACTIVE")
    missing = [sku_id for sku_id in ids if sku_id not in rows]
    if missing:
        return response(404, "SKU_NOT_FOUND", {"affectedSkus": missing})
    pending = {sku_id: updated_row(rows[sku_id], rule) for sku_id in ids}
    rows.update(pending)
    return response(200, "RULES_UPDATED", {"updatedSkus": list(ids)})


def preview(rows, warehouse_rule, ids):
    if not valid_ids(ids, 0):
        return response(400, "VALIDATION_ERROR")
    decode_rule(warehouse_rule)
    allowed, rejected = [], []
    for sku_id in ids:
        row = rows.get(sku_id)
        reasons = []
        if row is None:
            reasons.append("SKU_NOT_FOUND")
        else:
            rule = read_sku(row, warehouse_rule)["effectiveReserveRule"]
            if not row["enabled"]:
                reasons.append("SKU_DISABLED")
            minimum = rule["units"] if rule["kind"] == "minimum" else 0
            if row["stock"] - 1 < minimum:
                reasons.append("LOW_STOCK")
        if reasons:
            rejected.append({"id": sku_id, "reasons": reasons})
        else:
            allowed.append(sku_id)
    return response(200, "PREVIEW_EVALUATED", {"allowed": allowed, "rejected": rejected})


def confirm(rows, warehouse_rule, ids):
    if not valid_ids(ids, 1):
        return response(400, "VALIDATION_ERROR")
    _, evaluated = preview(rows, warehouse_rule, ids)
    if evaluated["data"]["rejected"]:
        return response(409, "RESERVATION_REJECTED", evaluated["data"])
    for sku_id in ids:
        rows[sku_id] = {**rows[sku_id], "stock": rows[sku_id]["stock"] - 1}
    return response(200, "RESERVED", {"reservedSkus": list(ids)})
