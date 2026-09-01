package handlers

import (
	"context"

	"github.com/acme/ingest/envelope"
)

type Store interface {
	Append(ctx context.Context, m envelope.Message) error
	AppendDiagnostic(ctx context.Context, report any) error
}

type Server struct {
	store Store
}
