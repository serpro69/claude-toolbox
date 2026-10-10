def save(store, workspace, operation_id, values):
    record = store.recovery.get(operation_id)
    if record is not None and record["status"] == "completed":
        return {"ok": True, "operation_id": operation_id}
    if record is None:
        record = {"operation_id": operation_id, "workspace": workspace,
                  "status": "pending"}
        store.recovery[operation_id] = record
    store.apply(workspace, values)
    record["values"] = dict(values)
    record["status"] = "applied"
    return store.receipt(record)
