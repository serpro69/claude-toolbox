class ReceiptUnavailable(Exception):
    pass


class Store:
    def __init__(self):
        self.preferences = {}
        self.recovery = {}
        self.fail_receipt_once = False

    def apply(self, workspace, values):
        self.preferences[workspace] = dict(values)

    def receipt(self, record):
        if self.fail_receipt_once:
            self.fail_receipt_once = False
            raise ReceiptUnavailable("receipt store unavailable")
        record["status"] = "completed"
        return {"ok": True, "operation_id": record["operation_id"]}
