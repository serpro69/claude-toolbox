def address_of(row):
    if "destination" in row:
        return row["destination"]["address"]
    return row["address"]
