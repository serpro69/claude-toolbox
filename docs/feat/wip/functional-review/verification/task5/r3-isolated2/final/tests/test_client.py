import unittest
from client import save_settings


class SettingsTests(unittest.TestCase):
    def test_successful_save(self):
        def send(workspace, request):
            return {"ok": True, "applied": True}
        self.assertEqual(save_settings(send, "w", {"label": "blue"}),
                         {"saved": True, "enhanced": False})
