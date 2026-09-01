package events

// Shipment lifecycle events published for downstream consumers.

type ShipmentStatusChanged struct {
	EventID    string
	ShipmentID string
	Status     string
	OccurredAt int64
}
