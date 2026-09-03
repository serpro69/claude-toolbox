package traffic

import "time"

// minCategorySeparation is the minimum air time between two spots from the
// same advertiser category.
const minCategorySeparation = 15 * time.Minute

// psaCategory marks public-service announcements, which the separation
// scheduler skips.
const psaCategory = "psa"

// SeparationOK reports whether airing a spot of the given category at t keeps
// the required distance from the previous same-category airing.
func (l *AirLog) SeparationOK(category string, t time.Time) bool {
	if category == psaCategory {
		return true
	}
	for _, e := range l.entries {
		if e.Category == category && t.Sub(e.AiredAt) < minCategorySeparation {
			return false
		}
	}
	return true
}
