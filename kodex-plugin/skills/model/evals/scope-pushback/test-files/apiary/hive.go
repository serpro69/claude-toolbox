package apiary

// Hive is a physical hive box standing at a yard.
type Hive struct {
	ID         string
	YardID     string
	BoxCount   int
	FrameCount int
	QueenYear  int
	Marked     bool
	Notes      string
}

// RequeenDue reports whether the hive's queen is due for replacement.
// Queens older than two seasons are requeened at the spring inspection.
func (h Hive) RequeenDue(currentYear int) bool {
	return currentYear-h.QueenYear >= 2
}
