from settings import patch_settings


def clear_note(current):
    return patch_settings(current, {"note": None})
