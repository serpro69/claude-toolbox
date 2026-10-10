import unittest

from client import submit
from store import ReceiptUnavailable, Store


class SaveTests(unittest.TestCase):
    def test_save(self):
        store = Store()
        result = submit(store, "w", "op-1", {"color": "blue"})
        self.assertTrue(result["ok"])
        self.assertEqual(store.preferences["w"], {"color": "blue"})

    def test_retry_same_values(self):
        store = Store()
        store.fail_receipt_once = True
        with self.assertRaises(ReceiptUnavailable):
            submit(store, "w", "op-1", {"color": "blue"})
        self.assertTrue(submit(store, "w", "op-1", {"color": "blue"})["ok"])
        self.assertEqual(store.preferences["w"], {"color": "blue"})

    def test_completed_id_returns_receipt(self):
        store = Store()
        submit(store, "w", "op-1", {"color": "blue"})
        result = submit(store, "w", "op-1", {"color": "blue"})
        self.assertEqual(result, {"ok": True, "operation_id": "op-1"})
