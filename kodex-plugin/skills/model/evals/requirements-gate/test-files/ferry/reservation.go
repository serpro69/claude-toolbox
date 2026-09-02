package ferry

// VehicleClass groups vehicles by the deck space they occupy.
type VehicleClass string

const (
	ClassCar     VehicleClass = "car"
	ClassVan     VehicleClass = "van"
	ClassLorry   VehicleClass = "lorry"
	ClassTrailer VehicleClass = "trailer"
)

// laneMetresByClass is the deck space each vehicle class occupies.
var laneMetresByClass = map[VehicleClass]int{
	ClassCar:     5,
	ClassVan:     7,
	ClassLorry:   17,
	ClassTrailer: 12,
}

// Source records how a reservation was sold.
type Source string

const (
	SourceAdvance Source = "advance" // booked ahead through the sales channel
	SourceWalkUp  Source = "walkup"  // sold at the ramp before departure
)

// Reservation claims deck space for one vehicle on one sailing.
type Reservation struct {
	ID      string
	Vehicle VehicleClass
	Source  Source
	Plate   string
}

// LaneMetres reports the deck space this reservation occupies.
func (r Reservation) LaneMetres() int {
	return laneMetresByClass[r.Vehicle]
}
