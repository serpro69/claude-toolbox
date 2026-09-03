package benches

// Bench is a growing surface with a fixed lot capacity.
type Bench struct {
	Label    string
	Capacity int
}

// CanAccept reports whether the bench can take n more lots given its current load.
func CanAccept(b Bench, current, n int) bool {
	return current+n <= b.Capacity
}
