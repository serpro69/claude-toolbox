package gym

import "errors"

// RouteState tracks a route's lifecycle on the wall.
type RouteState int

const (
	RouteStateUnknown RouteState = iota
	RouteStateSet
	RouteStateOpen
	RouteStateStripped
)

// Route is a climbable line set on a wall section.
type Route struct {
	ID     string
	WallID string
	Grade  string
	SetBy  string
	State  RouteState
}

// OpenRoute releases a set route to climbers.
func OpenRoute(r *Route) error {
	if r.State != RouteStateSet {
		return errors.New("only a set route can open")
	}
	if r.WallID == "" {
		return errors.New("route has no wall assignment")
	}
	if r.Grade == "" {
		return errors.New("route has no grade")
	}
	r.State = RouteStateOpen
	return nil
}

// StripRoute takes a route off the wall. A stripped route never reopens;
// re-setting the same line creates a new route.
func StripRoute(r *Route) error {
	if r.State == RouteStateStripped {
		return errors.New("route is already stripped")
	}
	r.State = RouteStateStripped
	return nil
}
