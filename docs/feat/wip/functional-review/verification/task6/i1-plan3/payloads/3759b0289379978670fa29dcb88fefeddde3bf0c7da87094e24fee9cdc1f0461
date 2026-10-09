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

    def test_sends_require_receipt_without_dropping_values(self):
        sent = {}

        def send(workspace_id, request):
            sent.update(request)
            return {"ok": True, "applied": True}

        save_settings(send, "w", {"label": "blue"})
        self.assertTrue(sent["require_receipt"])
        self.assertEqual(sent["settings"], {"label": "blue"})

    def test_applied_receipt_is_accepted(self):
        result = save_settings(lambda w, r: {"ok": True, "applied": True},
                               "w", {"label": "blue"})
        self.assertTrue(result["saved"])

    def test_receipt_reporting_not_applied_is_rejected(self):
        with self.assertRaises(RuntimeError):
            save_settings(lambda w, r: {"ok": True, "applied": False},
                          "w", {"label": "blue"})

    def test_current_provider_without_receipt_still_succeeds(self):
        # Independent delivery: a provider that predates receipts omits
        # "applied"; the ordinary save must keep returning success.
        result = save_settings(lambda w, r: {"ok": True},
                               "w", {"label": "blue"})
        self.assertTrue(result["saved"])

    def test_transport_failure_is_rejected(self):
        with self.assertRaises(RuntimeError):
            save_settings(lambda w, r: {"ok": False},
                          "w", {"label": "blue"})
