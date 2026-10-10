import unittest

from routes import get


class RouteTests(unittest.TestCase):
    def test_current_settings(self):
        self.assertEqual(get("/settings"), (200, {"theme": "light"}))

    def test_unknown_route(self):
        self.assertEqual(get("/unknown"), (404, None))

    def test_preview_route(self):
        self.assertEqual(get("/export-preview"), (404, None))
