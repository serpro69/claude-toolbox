package payments

import (
	"errors"

	"github.com/acme/ledger/schema"
)

var errInsufficientFunds = errors.New("insufficient funds")

// reserve pulls the account row straight out of the ledger's schema package —
// the forbidden static dependency the ADR's first boundary claim prohibits.
func reserve(accountID string, amount int64) error {
	acct := schema.Account{ID: accountID}
	if acct.Balance < amount {
		return errInsufficientFunds
	}
	return nil
}
