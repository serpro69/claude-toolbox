from config import EXPORT_PREVIEW_ENABLED
from preview import render_preview
from settings import current_settings


def get(path):
    if path == "/settings":
        return 200, current_settings()
    if EXPORT_PREVIEW_ENABLED and path == "/export-preview":
        return 200, render_preview()
    return 404, None
