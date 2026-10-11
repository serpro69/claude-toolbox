def migrate_batch(records, limit):
    migrated = 0
    for row in records:
        if migrated >= limit:
            break
        if "destination" not in row:
            row["destination"] = {"address": row.pop("address")}
            migrated += 1
    return migrated
