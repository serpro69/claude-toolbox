package client

import (
	"github.com/acme/payments/api"
	"github.com/sony/gobreaker"
)

// PaymentsClient calls the payments service through a circuit breaker: every
// call to the payments API runs inside the breaker rather than hitting the API
// client directly.
type PaymentsClient struct {
	cb  *gobreaker.CircuitBreaker
	api *api.Client
}

func NewPaymentsClient(a *api.Client) *PaymentsClient {
	return &PaymentsClient{
		cb:  gobreaker.NewCircuitBreaker(gobreaker.Settings{Name: "payments"}),
		api: a,
	}
}

// Charge runs the payments call through the breaker.
func (c *PaymentsClient) Charge(orderID string, cents int64) error {
	_, err := c.cb.Execute(func() (interface{}, error) {
		return nil, c.api.Charge(orderID, cents)
	})
	return err
}
