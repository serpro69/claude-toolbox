def save_settings(send, workspace_id, values, enhanced_settings=False):
    response = send(workspace_id, {"settings": values, "require_receipt": True})
    if not response.get("ok"):
        raise RuntimeError("Settings save failed")
    # The provider receipt ships in a later increment. When the provider returns an
    # `applied` receipt, it confirms the save only when it is exactly boolean True; any
    # other present value (False, None, a non-bool) is not a trustworthy confirmation and
    # is rejected. A provider that does not yet send the receipt omits the key entirely;
    # that legacy response stays a success so the client keeps working against the current
    # provider (independent delivery).
    if "applied" in response and response["applied"] is not True:
        raise RuntimeError("Settings reported saved but not applied")
    return {"saved": True, "enhanced": enhanced_settings}
