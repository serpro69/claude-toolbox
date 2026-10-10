def save_settings(send, workspace_id, values, enhanced_settings=False):
    response = send(workspace_id, {"settings": values, "require_receipt": True})
    if not response.get("ok"):
        raise RuntimeError("Settings save failed")
    # Enforce the applied receipt only when the provider returns one. The current
    # provider predates receipts and omits "applied"; per the independent-delivery
    # guarantee this client must still treat such ordinary saves as successful.
    # An explicit applied=false is an affirmative "not applied" receipt -> reject.
    if "applied" in response and not response["applied"]:
        raise RuntimeError("Settings save was not applied")
    return {"saved": True, "enhanced": enhanced_settings}
