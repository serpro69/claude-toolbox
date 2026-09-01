package handlers

import (
	"io"
	"net/http"

	"github.com/acme/ingest/envelope"
)

func (s *Server) HandleTelemetry(w http.ResponseWriter, r *http.Request) {
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "read error", http.StatusBadRequest)
		return
	}
	msg, err := envelope.Open(body)
	if err != nil {
		http.Error(w, "bad payload", http.StatusBadRequest)
		return
	}
	s.store.Append(r.Context(), msg)
	w.WriteHeader(http.StatusAccepted)
}
