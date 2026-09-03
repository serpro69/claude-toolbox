package moorings

import (
	"errors"
	"time"

	"marina/berths"
)

// Assignment records a vessel occupying a berth.
type Assignment struct {
	VesselID  string
	BerthName string
	Since     time.Time
	Ended     *time.Time
}

// Roster holds the marina's mooring assignments.
type Roster struct {
	assignments []Assignment
}

// ErrAlreadyMoored rejects a second active assignment for the same vessel.
var ErrAlreadyMoored = errors.New("moorings: vessel already has an active assignment")

// AssignBerth records a new assignment for the vessel on the given berth.
func (r *Roster) AssignBerth(vesselID string, b berths.Berth) (Assignment, error) {
	if r.hasActiveAssignment(vesselID) {
		return Assignment{}, ErrAlreadyMoored
	}
	a := Assignment{VesselID: vesselID, BerthName: b.Name, Since: time.Now()}
	r.assignments = append(r.assignments, a)
	return a, nil
}

// Release ends the vessel's active assignment, if one exists.
func (r *Roster) Release(vesselID string) {
	now := time.Now()
	for i := range r.assignments {
		if r.assignments[i].VesselID == vesselID && r.assignments[i].Ended == nil {
			r.assignments[i].Ended = &now
		}
	}
}

// hasActiveAssignment reports whether the vessel currently occupies a berth.
func (r *Roster) hasActiveAssignment(vesselID string) bool {
	for _, a := range r.assignments {
		if a.VesselID == vesselID && a.Ended == nil {
			return true
		}
	}
	return false
}
