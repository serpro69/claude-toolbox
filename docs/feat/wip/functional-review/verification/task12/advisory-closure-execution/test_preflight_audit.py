"""Offline receipt-decoder controls; never runs actors or probes."""
import unittest

from preflight_audit import source_returned


class ReceiptTests(unittest.TestCase):
    def test_complete_plain_return(self):
        self.assertTrue(source_returned("first\nsecond\n", "header\nfirst\nsecond\nfooter"))

    def test_complete_numbered_return_including_terminal_empty_line(self):
        self.assertTrue(source_returned("first\nsecond\n", "1\tfirst\n2\tsecond\n3\t"))

    def test_truncation_does_not_establish_receipt(self):
        self.assertFalse(source_returned("first\nsecond\nthird\n", "1\tfirst\n2\tsecond"))

    def test_noncontiguous_numbering_does_not_establish_receipt(self):
        self.assertFalse(source_returned("first\nsecond\n", "1\tfirst\n3\tsecond"))

    def test_wrong_source_bytes_do_not_match(self):
        self.assertFalse(source_returned("first\nsecond\n", "1\tfirst\n2\tdifferent\n3\t"))


if __name__ == "__main__":
    unittest.main()
