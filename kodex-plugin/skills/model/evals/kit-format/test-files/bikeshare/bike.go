package bikeshare

// BikeStatus is the availability state of a bike in the fleet.
type BikeStatus string

const (
	StatusAvailable   BikeStatus = "available"
	StatusInUse       BikeStatus = "in_use"
	StatusMaintenance BikeStatus = "maintenance"
)

// Bike is a single rentable bicycle, either docked or in use.
type Bike struct {
	ID     string
	Status BikeStatus
	DockID string // empty while the bike is in use
}

// A bike under maintenance is not eligible to start a ride.
func Eligible(b Bike) bool {
	return b.Status == StatusAvailable
}
