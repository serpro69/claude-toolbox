package apiary

// Harvest is one honey pull from a single hive.
type Harvest struct {
	ID           string
	HiveID       string
	Season       string
	FramesPulled int
	WeightKg     float64
	Moisture     float64
}

// Sellable reports whether the harvest can go to sale. Honey above 18.5%
// moisture ferments in the jar and is diverted to feed instead.
func (h Harvest) Sellable() bool {
	return h.Moisture <= 18.5
}
