def save_settings(send, workspace_id, values, enhanced_settings=False):
    response = send(workspace_id, {"settings": values, "require_receipt": True})
    if not response.get("ok"):
        raise RuntimeError("Settings save failed")
    if response.get("applied") is not True:
        raise RuntimeError("Provider did not acknowledge applied settings")
    return {"saved": True, "enhanced": enhanced_settings}
