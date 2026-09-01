package inventory

import (
	"github.com/acme/pricing/schema"
)

// value reaches into the pricing service's private schema package directly —
// the forbidden static dependency the first boundary claim prohibits.
func value(sku string, qty int) int64 {
	price := schema.Price{SKU: sku}
	return price.Cents * int64(qty)
}
