module github.com/acme/orders

go 1.22

require (
	github.com/acme/payments v0.0.0
	github.com/sony/gobreaker v0.5.0
)

replace github.com/acme/payments => ../payments
