package apiary

import "time"

// Colony is the bee population living in a hive.
type Colony struct {
	ID          string
	HiveID      string
	Strength    int
	Temperament string
	SwarmedAt   time.Time
	Source      string
}

// NeedsSplit reports whether the colony is strong enough that it should be
// split before swarm season to avoid losing it.
func (c Colony) NeedsSplit() bool {
	return c.Strength >= 8 && c.SwarmedAt.IsZero()
}
