def save_settings(send, workspace_id, values, enhanced_settings=False):
    response = send(workspace_id, {"settings": values})
    if not response.get("ok"):
        raise RuntimeError("Settings save failed")
    return {"saved": True, "enhanced": enhanced_settings}
