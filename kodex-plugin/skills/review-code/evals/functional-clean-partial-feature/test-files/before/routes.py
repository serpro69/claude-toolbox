from settings import current_settings


def get(path):
    if path == "/settings":
        return 200, current_settings()
    return 404, None
