from records import read_label


def list_labels(records):
    return [read_label(record) for record in records]
