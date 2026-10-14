import unittest

from client import save, clear_name

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

    def test_clear_name(self):
        transport = MemoryTransport()
        self.assertEqual(clear_name(transport), {"ok": True})
        self.assertEqual(transport.request, ("/settings", {"display_name": None}))
