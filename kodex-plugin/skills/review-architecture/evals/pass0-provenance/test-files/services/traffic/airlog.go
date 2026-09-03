package traffic

import "time"

// AirLog is the append-only record of spots that have aired.
type AirLog struct {
	entries []AirEntry
}

// AirEntry records one aired spot.
type AirEntry struct {
	SpotID   string
	Category string
	AiredAt  time.Time
	Daypart  string
}

// Append records an aired spot. All writes to the air log go through here.
func (l *AirLog) Append(e AirEntry) {
	l.entries = append(l.entries, e)
}
