"""QueueKit 1.5.0 default-branch snapshot; no 1.4.2 source or runtime evidence."""


def emit_receipt(job_id, seen_receipts):
    if job_id in seen_receipts:
        return None
    seen_receipts.add(job_id)
    return {"job_id": job_id, "state": "completed"}
