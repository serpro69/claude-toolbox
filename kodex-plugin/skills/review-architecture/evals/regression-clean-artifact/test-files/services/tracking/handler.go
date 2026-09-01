package tracking

import (
	"database/sql"
	"encoding/json"
	"net/http"
)

type Handler struct {
	db *sql.DB
}

func (h *Handler) GetStatus(w http.ResponseWriter, r *http.Request) {
	shipmentID := r.PathValue("shipment_id")
	var status, updatedAt string
	err := h.db.QueryRowContext(r.Context(),
		`SELECT status, updated_at FROM tracking_status WHERE shipment_id = $1`,
		shipmentID).Scan(&status, &updatedAt)
	if err != nil {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	json.NewEncoder(w).Encode(map[string]string{
		"shipment_id": shipmentID,
		"status":      status,
		"updated_at":  updatedAt,
	})
}
