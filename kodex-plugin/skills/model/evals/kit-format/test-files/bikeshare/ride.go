package bikeshare

import "time"

// Ride is a single trip: a rider takes a bike from one dock and returns it to another.
type Ride struct {
	ID        string
	RiderID   string
	BikeID    string
	StartDock string
	EndDock   string
	StartedAt time.Time
	EndedAt   time.Time // zero until the ride is closed
}

// StartRide opens a ride for a rider on a bike taken from a dock.
func StartRide(id, riderID string, b *Bike, dockID string, now time.Time) *Ride {
	b.Status = StatusInUse
	b.DockID = ""
	return &Ride{
		ID:        id,
		RiderID:   riderID,
		BikeID:    b.ID,
		StartDock: dockID,
		StartedAt: now,
	}
}
