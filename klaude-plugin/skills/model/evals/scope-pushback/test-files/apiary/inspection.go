package apiary

import "time"

// Inspection is a recorded visit to a single hive.
type Inspection struct {
	ID          string
	HiveID      string
	Date        time.Time
	QueenSeen   bool
	BroodFrames int
	MiteCount   int
	Findings    string
}

// Overdue reports whether the hive is past its inspection interval.
// Hives are inspected at least every 45 days during the season.
func (i Inspection) Overdue(now time.Time) bool {
	return now.Sub(i.Date) > 45*24*time.Hour
}
