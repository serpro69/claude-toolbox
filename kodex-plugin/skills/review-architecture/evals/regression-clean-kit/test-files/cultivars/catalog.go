package cultivars

// Cultivar is a named plant variety the nursery propagates.
type Cultivar struct {
	Name    string
	Species string
	Stock   int
}

// Catalog holds the nursery's cultivars.
type Catalog struct {
	cultivars []Cultivar
}

// Add registers a cultivar in the catalog.
func (c *Catalog) Add(cv Cultivar) {
	c.cultivars = append(c.cultivars, cv)
}

// BySpecies returns every cultivar of the given species.
func (c *Catalog) BySpecies(species string) []Cultivar {
	var out []Cultivar
	for _, cv := range c.cultivars {
		if cv.Species == species {
			out = append(out, cv)
		}
	}
	return out
}
