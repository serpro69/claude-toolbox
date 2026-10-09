def save_settings(send, workspace_id, values, enhanced_settings=False):
    response = send(workspace_id, {"settings": values, "require_receipt": True})
    if not response.get("ok"):
        raise RuntimeError("Settings save failed")
    # The provider's `applied` receipt ships in a later, independently-released
    # task. A merged client must keep working against the current provider, which
    # does not yet return a receipt, so only enforce it when one is present
    # (distinguishing an absent field from an explicit False). When present, the
    # receipt must confirm the settings were applied.
    if "applied" in response and response["applied"] is not True:
        raise RuntimeError("Settings reported not applied by provider")
    return {"saved": True, "enhanced": enhanced_settings}
