from reader import address_of


def list_destinations(records):
    return [{"id": row["id"], "address": address_of(row)} for row in records]
