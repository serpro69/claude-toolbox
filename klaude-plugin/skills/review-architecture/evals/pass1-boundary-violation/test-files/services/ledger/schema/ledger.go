package schema

// Account is the ledger service's private schema type. Consumers are meant to
// reach balances through the ledger API, not by importing this package.
type Account struct {
	ID      string
	Balance int64
}
