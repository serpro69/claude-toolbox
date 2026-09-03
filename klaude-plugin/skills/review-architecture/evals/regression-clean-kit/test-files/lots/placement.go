package lots

import "time"

// Lot is a batch of plants of one cultivar moving through the nursery together.
type Lot struct {
	ID         string
	CultivarID string
	BenchLabel string
	PlacedAt   time.Time
}

// Placements records which bench each lot occupies.
type Placements struct {
	byLot map[string]Lot
}

// PlaceLot records the lot on a bench, replacing any previous placement.
func (p *Placements) PlaceLot(l Lot, bench string) Lot {
	if p.byLot == nil {
		p.byLot = make(map[string]Lot)
	}
	l.BenchLabel = bench
	l.PlacedAt = time.Now()
	p.byLot[l.ID] = l
	return l
}

// On returns the lots currently placed on the given bench.
func (p *Placements) On(bench string) []Lot {
	var out []Lot
	for _, l := range p.byLot {
		if l.BenchLabel == bench {
			out = append(out, l)
		}
	}
	return out
}
