package berths

// Berth is a rentable mooring space on a pier.
type Berth struct {
	Name        string
	Pier        string
	LengthM     float64
	Maintenance bool
}

// Registry holds the marina's berths in registration order.
type Registry struct {
	berths []Berth
}

// Register adds a berth to the registry.
func (r *Registry) Register(b Berth) {
	r.berths = append(r.berths, b)
}

// FindByName returns the first berth whose name matches.
func (r *Registry) FindByName(name string) (Berth, bool) {
	for _, b := range r.berths {
		if b.Name == name {
			return b, true
		}
	}
	return Berth{}, false
}
