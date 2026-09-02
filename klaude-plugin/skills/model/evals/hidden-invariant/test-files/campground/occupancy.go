package campground

import "time"

// OccupantOf reports the booking occupying a site at the given time.
func (l *Ledger) OccupantOf(siteID string, at time.Time) (Booking, bool) {
	for _, b := range l.Bookings {
		if b.SiteID != siteID || !b.CancelledAt.IsZero() {
			continue
		}
		if !at.Before(b.From) && at.Before(b.To) {
			return b, true
		}
	}
	return Booking{}, false
}
