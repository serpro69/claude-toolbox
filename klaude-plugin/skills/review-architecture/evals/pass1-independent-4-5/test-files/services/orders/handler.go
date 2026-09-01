package orders

import (
	"database/sql"

	"github.com/acme/orders/client"
)

// CreateOrder inserts a new order row and charges payments through the
// breaker-wrapped client. The insert is a plain INSERT keyed on the generated
// id; the create path takes no request-supplied key and performs no pre-insert
// lookup before writing.
func CreateOrder(db *sql.DB, pay *client.PaymentsClient, customerID string, cents int64) (string, error) {
	var orderID string
	err := db.QueryRow(
		"INSERT INTO orders (customer_id, cents) VALUES ($1, $2) RETURNING id",
		customerID, cents,
	).Scan(&orderID)
	if err != nil {
		return "", err
	}
	if err := pay.Charge(orderID, cents); err != nil {
		return "", err
	}
	return orderID, nil
}
