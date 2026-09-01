package client

import (
	"context"
	"time"

	"github.com/acme/carrierapi"
)

const (
	callTimeout = 2 * time.Second
	maxAttempts = 3
)

type CarrierClient struct {
	api *carrierapi.Client
}

func (c *CarrierClient) FetchStatus(ctx context.Context, trackingNumber string) (carrierapi.Status, error) {
	var lastErr error
	for attempt := 0; attempt < maxAttempts; attempt++ {
		callCtx, cancel := context.WithTimeout(ctx, callTimeout)
		status, err := c.api.Status(callCtx, trackingNumber)
		cancel()
		if err == nil {
			return status, nil
		}
		lastErr = err
	}
	return carrierapi.Status{}, lastErr
}
