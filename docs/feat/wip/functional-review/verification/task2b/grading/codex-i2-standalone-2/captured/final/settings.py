def patch_settings(current, patch):
    """Return a shallow copy with every explicitly supplied patch value applied."""
    result = dict(current)
    for key, value in patch.items():
        result[key] = value
    return result
