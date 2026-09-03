package traffic

// maxAiringsPerDaypart caps how many times one spot airs within a daypart.
const maxAiringsPerDaypart = 3

// CanAir reports whether the spot may air again in the given daypart.
func (l *AirLog) CanAir(spotID, daypart string) bool {
	var count int
	for _, e := range l.entries {
		if e.SpotID == spotID && e.Daypart == daypart {
			count++
		}
	}
	return count < maxAiringsPerDaypart
}
