package ferry

import "time"

// Sailing is one scheduled crossing with a fixed amount of vehicle-deck space.
type Sailing struct {
	ID             string
	Route          string
	Departs        time.Time
	DeckLaneMetres int
	Reservations   []Reservation
}

// RemainingLaneMetres reports the deck space not yet claimed by reservations.
func (s Sailing) RemainingLaneMetres() int {
	var used int
	for _, r := range s.Reservations {
		used += r.LaneMetres()
	}
	return s.DeckLaneMetres - used
}
