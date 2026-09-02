package bikeshare

import "time"

// MaxRideDuration bounds how long a single ride may stay open before the
// system closes it automatically and bills the rider a full-day rate.
const MaxRideDuration = 24 * time.Hour

// AutoClose closes any ride that has been open longer than MaxRideDuration.
// It stamps the end time; billing reconciliation runs separately.
func AutoClose(r *Ride, now time.Time) bool {
	if r.EndedAt.IsZero() && now.Sub(r.StartedAt) > MaxRideDuration {
		r.EndedAt = now
		return true
	}
	return false
}
