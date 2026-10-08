import unittest
from client import save_settings
from provider import update_settings


class SettingsTests(unittest.TestCase):
    def test_ordinary_save(self):
        # Backward compatibility: the current provider predates receipts and omits
        # "applied". The independent-delivery guarantee requires this to still succeed.
        storage = {}
        result = save_settings(lambda w, r: update_settings(storage, w, r),
                               "w", {"label": "blue"})
        self.assertTrue(result["saved"])
        self.assertEqual(storage["w"], {"label": "blue"})

    def test_sends_require_receipt(self):
        captured = {}

        def send(workspace_id, request):
            captured["request"] = request
            return {"ok": True}

        save_settings(send, "w", {"label": "blue"})
        self.assertTrue(captured["request"]["require_receipt"])
        self.assertEqual(captured["request"]["settings"], {"label": "blue"})

    def test_applied_receipt_succeeds(self):
        result = save_settings(lambda w, r: {"ok": True, "applied": True},
                               "w", {"label": "blue"})
        self.assertTrue(result["saved"])

    def test_not_applied_receipt_rejected(self):
        with self.assertRaises(RuntimeError):
            save_settings(lambda w, r: {"ok": True, "applied": False},
                          "w", {"label": "blue"})

    def test_transport_failure_rejected(self):
        with self.assertRaises(RuntimeError):
            save_settings(lambda w, r: {"ok": False},
                          "w", {"label": "blue"})
