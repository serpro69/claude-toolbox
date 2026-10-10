from settings import patch_settings


def update_preferences(current, payload):
    patch = {key: payload[key] for key in ("note", "enabled") if key in payload}
    return patch_settings(current, patch)
