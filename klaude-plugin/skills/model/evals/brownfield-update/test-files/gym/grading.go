package gym

// Scale lists the grades the gym displays on route cards, easiest first.
var Scale = []string{"4a", "4b", "4c", "5a", "5b", "5c", "6a", "6b", "6c", "7a", "7b", "7c", "8a"}

// SetGrade records the setting team's agreed grade for a route.
func SetGrade(r *Route, grade string) {
	r.Grade = grade
}

// DisplayGrade returns the grade shown on the route card.
func DisplayGrade(r *Route) string {
	for _, g := range Scale {
		if r.Grade == g {
			return g
		}
	}
	return r.Grade
}
