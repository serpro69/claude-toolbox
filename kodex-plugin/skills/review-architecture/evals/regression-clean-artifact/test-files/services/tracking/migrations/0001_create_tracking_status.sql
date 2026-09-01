CREATE TABLE tracking_status (
    shipment_id TEXT PRIMARY KEY,
    status      TEXT NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL
);
