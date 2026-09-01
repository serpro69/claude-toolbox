package schema

// Price is the pricing service's private schema type. Consumers are meant to
// reach prices through the pricing API, not by importing this package.
type Price struct {
	SKU   string
	Cents int64
}
