package campground

import (
	"errors"
	"fmt"
	"time"
)

var ErrVacant = errors.New("site is vacant")

// GateCode issues the barrier code for whoever occupies a site at the given
// time; the code is derived from the occupying booking and texted to its guest.
func (l *Ledger) GateCode(siteID string, at time.Time) (string, error) {
	b, ok := l.OccupantOf(siteID, at)
	if !ok {
		return "", ErrVacant
	}
	return fmt.Sprintf("%s-%s", siteID, b.ID), nil
}
