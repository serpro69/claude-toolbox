package gym

// Wall is a physical climbing surface divided into named sections.
type Wall struct {
	ID       string
	Name     string
	Sections []string
}

// FindWall returns the wall with the given ID from the gym's inventory.
func FindWall(walls []Wall, id string) (Wall, bool) {
	for _, w := range walls {
		if w.ID == id {
			return w, true
		}
	}
	return Wall{}, false
}
