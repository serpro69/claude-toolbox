package envelope

import (
	sdk "github.com/devicecloud/sdk-go"
)

type Message struct {
	DeviceID    string
	RecordedAt  int64
	BatteryMV   int32
	Temperature float64
	DiagCode    int32
}

func Open(payload []byte) (Message, error) {
	env, err := sdk.ParseEnvelope(payload)
	if err != nil {
		return Message{}, err
	}
	return Message{
		DeviceID:    env.DeviceID(),
		RecordedAt:  env.RecordedAt(),
		BatteryMV:   env.Int32Field("battery_mv"),
		Temperature: env.Float64Field("temperature"),
		DiagCode:    env.Int32Field("diag_code"),
	}, nil
}
