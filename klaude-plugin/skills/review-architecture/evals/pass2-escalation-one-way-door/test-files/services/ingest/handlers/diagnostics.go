package handlers

import (
	"io"
	"net/http"

	sdk "github.com/devicecloud/sdk-go"
)

func (s *Server) HandleDiagnostics(w http.ResponseWriter, r *http.Request) {
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "read error", http.StatusBadRequest)
		return
	}
	env, err := sdk.ParseEnvelope(body)
	if err != nil {
		http.Error(w, "bad payload", http.StatusBadRequest)
		return
	}
	report := map[string]any{
		"device_id": env.DeviceID(),
		"code":      env.Int32Field("diag_code"),
		"detail":    env.StringField("diag_detail"),
	}
	s.store.AppendDiagnostic(r.Context(), report)
	w.WriteHeader(http.StatusAccepted)
}
