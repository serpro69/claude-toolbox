"""Prove that history markers cannot turn failed or mismatched reads into receipts."""
import unittest

import receipt_supplement_v2 as receipts


class SuccessfulReadReceiptTests(unittest.TestCase):
    def lines(self):
        prefix = "2026-10-10 14:36:24,728 - "
        return [prefix + "utils.file_utils - DEBUG - [FILES] Successfully read 5 characters from /tmp/owned.py",
                prefix + "utils.file_utils - DEBUG - [FILES] Formatted content for /tmp/owned.py: 80 chars, 20 tokens",
                prefix + "utils.conversation_memory - DEBUG - File embedded in conversation history: /tmp/owned.py (20 tokens)"]

    def test_success_is_bound_to_captured_content_and_call_window(self):
        triplet = receipts.parse_triplet(self.lines(), 30)
        stamp = triplet[0]["timestamp_ms"]
        call = {"relevant_files": ["/tmp/owned.py"], "start_ms": stamp - 1, "end_ms": stamp + 1}
        receipts.bind_payload(triplet, call, b"test\r\n")
        self.assertEqual(triplet[-1]["line"], 32)

    def test_nonempty_error_embedding_is_not_success(self):
        lines = self.lines()
        lines[0] = "2026-10-10 14:36:24,728 - utils.file_utils - DEBUG - [FILES] Returning error content for /tmp/owned.py: 20 tokens"
        with self.assertRaisesRegex(ValueError, "Missing allowlisted"):
            receipts.parse_triplet(lines, 30)

    def test_read_success_without_successful_formatting_is_not_receipt(self):
        lines = self.lines()
        lines[1] = "2026-10-10 14:36:24,728 - utils.file_utils - DEBUG - [FILES] Exception reading file /tmp/owned.py: private error"
        with self.assertRaisesRegex(ValueError, "Missing allowlisted") as raised:
            receipts.parse_triplet(lines, 30)
        self.assertNotIn("private", str(raised.exception))

    def test_mixed_paths_are_rejected(self):
        lines = self.lines()
        lines[1] = lines[1].replace("owned.py", "other.py")
        with self.assertRaisesRegex(ValueError, "paths differ"):
            receipts.parse_triplet(lines, 30)

    def test_read_counts_must_match_payload(self):
        triplet = receipts.parse_triplet(self.lines(), 30)
        stamp = triplet[0]["timestamp_ms"]
        with self.assertRaisesRegex(ValueError, "character count differs"):
            receipts.bind_payload(triplet, {"relevant_files": ["/tmp/owned.py"], "start_ms": stamp, "end_ms": stamp}, b"different")

    def test_token_counts_must_match_embedding(self):
        lines = self.lines()
        lines[2] = lines[2].replace("20 tokens", "19 tokens")
        with self.assertRaisesRegex(ValueError, "counts disagree"):
            receipts.parse_triplet(lines, 30)

    def test_out_of_order_timestamps_are_rejected(self):
        lines = self.lines()
        lines[0] = lines[0].replace("24,728", "24,729")
        with self.assertRaisesRegex(ValueError, "out of order"):
            receipts.parse_triplet(lines, 30)

    def test_outside_call_window_is_rejected(self):
        triplet = receipts.parse_triplet(self.lines(), 30)
        stamp = triplet[0]["timestamp_ms"]
        with self.assertRaisesRegex(ValueError, "outside actual invocation"):
            receipts.bind_payload(triplet, {"relevant_files": ["/tmp/owned.py"], "start_ms": stamp + 1, "end_ms": stamp + 2}, b"test\n")


if __name__ == "__main__":
    unittest.main()
