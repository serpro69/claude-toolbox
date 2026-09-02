package bikeshare

// Dock is a fixed station where bikes are picked up and returned.
type Dock struct {
	ID       string
	Capacity int
	BikeIDs  []string
}

// CanAccept reports whether the dock has room for another returned bike.
// TODO(BIKE-204): replace the static Capacity with live occupancy once the
// dock-sensor rollout ships.
func (d Dock) CanAccept() bool {
	return len(d.BikeIDs) < d.Capacity
}
