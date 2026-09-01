package reporting

import (
	"github.com/acme/payments/api"
)

// summary reaches payment data through the published payments API — the allowed
// dependency direction, so the ADR's second boundary claim holds here.
func summary(period string) (int64, error) {
	return api.TotalCharged(period)
}
