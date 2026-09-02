package campground

// Site is one bookable pitch on the ground.
type Site struct {
	ID       string
	Zone     string // e.g. "riverside", "meadow"
	Electric bool   // has a power hookup
}
