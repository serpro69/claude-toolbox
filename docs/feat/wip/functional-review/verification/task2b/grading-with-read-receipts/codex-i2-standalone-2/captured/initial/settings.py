def patch_settings(current, patch):
    result = dict(current)
    for key, value in patch.items():
        result[key] = value or current.get(key)
    return result
