package schema

// Payment is the payments service's PRIVATE schema type. The second boundary
// claim forbids the reporting service from importing this package; reporting
// reaches payment data through the payments API instead. It exists here so the
// "verified" control is a real contrast — a schema package that is present and
// deliberately NOT imported by reporting.
type Payment struct {
	ID    string
	Cents int64
}
