package tracking

import (
	"context"
	"database/sql"

	"github.com/acme/shipments/events"
)

// Projector consumes shipment events and maintains the denormalized
// tracking_status row per shipment.
type Projector struct {
	db *sql.DB
}

func (p *Projector) Handle(ctx context.Context, e events.ShipmentStatusChanged) error {
	_, err := p.db.ExecContext(ctx,
		`INSERT INTO tracking_status (shipment_id, status, updated_at)
		 VALUES ($1, $2, to_timestamp($3))
		 ON CONFLICT (shipment_id) DO UPDATE
		 SET status = EXCLUDED.status, updated_at = EXCLUDED.updated_at`,
		e.ShipmentID, e.Status, e.OccurredAt)
	return err
}
