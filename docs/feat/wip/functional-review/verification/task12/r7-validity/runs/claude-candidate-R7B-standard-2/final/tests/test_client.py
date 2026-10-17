import unittest

from client import save

class MemoryTransport:
    def __init__(self):
        self.request = None

    def put(self, path, body):
        self.request = (path, body)
        return {"ok": True}


class ClientTests(unittest.TestCase):
    def test_save(self):
        transport = MemoryTransport()
        self.assertEqual(save(transport, "Ada"), {"ok": True})
        self.assertEqual(transport.request, ("/settings", {"display_name": "Ada"}))

    def test_empty_label(self):
        transport = MemoryTransport()
        save(transport, "")
        self.assertEqual(transport.request, ("/settings", {"display_name": ""}))

    def test_normalized_requests(self):
        for value, expected in [("  Ada  ", "Ada"), ("Ada Lovelace", "Ada Lovelace"),
                                (" \t\n", ""), ("\u00a0Ada\u3000", "Ada")]:
            with self.subTest(value=value):
                transport = MemoryTransport()
                save(transport, value)
                self.assertEqual(transport.request, ("/settings", {"display_name": expected}))
