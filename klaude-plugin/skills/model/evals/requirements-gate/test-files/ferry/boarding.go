package ferry

import "errors"

var ErrDeckFull = errors.New("no deck space left on sailing")

// Reserve claims deck space on a sailing, freeing space from the tail of the
// reservation list when the deck is over-committed.
func Reserve(s *Sailing, r Reservation) error {
	for s.RemainingLaneMetres() < r.LaneMetres() {
		if len(s.Reservations) == 0 {
			return ErrDeckFull
		}
		s.Reservations = s.Reservations[:len(s.Reservations)-1]
	}
	s.Reservations = append(s.Reservations, r)
	return nil
}
