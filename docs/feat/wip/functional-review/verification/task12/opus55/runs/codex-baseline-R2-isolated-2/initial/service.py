def save(store, workspace, operation_id, values):
    record = next((item for item in store.recovery.values()
                   if item["workspace"] == workspace), None)
    if record is None:
        record = {"operation_id": operation_id, "workspace": workspace,
                  "status": "pending", "values": dict(values)}
        store.recovery[operation_id] = record
    if record["status"] == "pending":
        store.apply(workspace, record["values"])
        record["status"] = "applied"
    store.receipt(record)
    return {"ok": True, "operation_id": operation_id}
