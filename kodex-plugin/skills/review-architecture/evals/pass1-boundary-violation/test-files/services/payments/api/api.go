package api

// TotalCharged is the payments service's published, read-only entry point. The
// reporting service is allowed to depend on THIS package — it exposes totals
// without leaking the private schema.
func TotalCharged(period string) (int64, error) {
	return 0, nil
}
