def save_settings(send, workspace_id, values, enhanced_settings=False):
    response = send(workspace_id, {"settings": values, "require_receipt": True})
    if not response.get("ok"):
        raise RuntimeError("Settings save failed")
    # Enforce the applied receipt only when the provider returns one. A current
    # provider that predates receipts omits "applied"; independent delivery
    # requires ordinary saves against it to keep succeeding (design.md). A
    # receipt-bearing provider that reports applied=false means the values were
    # not applied, so reject it.
    if "applied" in response and not response["applied"]:
        raise RuntimeError("Settings were not applied")
    return {"saved": True, "enhanced": enhanced_settings}
