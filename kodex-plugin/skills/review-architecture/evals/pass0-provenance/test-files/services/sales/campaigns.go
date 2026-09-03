package sales

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
)

// trafficAPI is the base URL of the traffic service's HTTP API.
const trafficAPI = "http://traffic.internal"

// AiredCount fetches how many times a spot has aired, via the traffic API.
func AiredCount(spotID string) (int, error) {
	resp, err := http.Get(trafficAPI + "/airlog/count?spot=" + url.QueryEscape(spotID))
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return 0, fmt.Errorf("traffic api: unexpected status %d", resp.StatusCode)
	}
	var out struct{ Count int }
	if err := json.NewDecoder(resp.Body).Decode(&out); err != nil {
		return 0, err
	}
	return out.Count, nil
}
