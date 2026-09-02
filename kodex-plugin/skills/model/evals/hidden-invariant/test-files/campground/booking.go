package campground

import (
	"errors"
	"time"
)

var (
	ErrUnknownSite = errors.New("unknown site")
	ErrBadDates    = errors.New("stay must end after it starts")
)

// Booking reserves a site for a guest between two dates.
type Booking struct {
	ID          string
	SiteID      string
	GuestID     string
	From, To    time.Time
	CancelledAt time.Time // zero unless the booking was cancelled
}

// Ledger holds the ground's sites and bookings.
type Ledger struct {
	Sites    map[string]Site
	Bookings []Booking
}

// Book records a stay for a guest on a site.
func (l *Ledger) Book(id, siteID, guestID string, from, to time.Time) (Booking, error) {
	if _, ok := l.Sites[siteID]; !ok {
		return Booking{}, ErrUnknownSite
	}
	if !to.After(from) {
		return Booking{}, ErrBadDates
	}
	b := Booking{ID: id, SiteID: siteID, GuestID: guestID, From: from, To: to}
	l.Bookings = append(l.Bookings, b)
	return b, nil
}

// Cancel marks a booking cancelled as of now.
func (l *Ledger) Cancel(bookingID string, now time.Time) bool {
	for i := range l.Bookings {
		if l.Bookings[i].ID == bookingID && l.Bookings[i].CancelledAt.IsZero() {
			l.Bookings[i].CancelledAt = now
			return true
		}
	}
	return false
}
