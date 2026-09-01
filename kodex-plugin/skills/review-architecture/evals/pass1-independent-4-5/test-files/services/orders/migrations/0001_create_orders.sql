-- Orders table schema. Columns: generated id (primary key), customer_id, cents,
-- created_at. There are no additional columns or table constraints beyond those
-- listed below.
CREATE TABLE orders (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id TEXT   NOT NULL,
    cents       BIGINT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
