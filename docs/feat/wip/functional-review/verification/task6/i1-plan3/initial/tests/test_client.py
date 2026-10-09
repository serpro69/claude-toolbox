import unittest
from client import save_settings
from provider import update_settings


class SettingsTests(unittest.TestCase):
    def test_ordinary_save(self):
        storage = {}
        result = save_settings(lambda w, r: update_settings(storage, w, r),
                               "w", {"label": "blue"})
        self.assertTrue(result["saved"])
        self.assertEqual(storage["w"], {"label": "blue"})
