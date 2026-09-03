# Ad-traffic scheduling architecture

Date: 2026-09-02

This document records the ad-traffic scheduling architecture of the station platform
as currently built. The airing rules in §Airing rules were recovered during a code
archaeology session; each entry's Origin column states where it came from.

## Components

The `traffic` service is the sole mutating owner of the `AirLog`, the append-only
record of aired spots. The `sales` service reads air logs only through the traffic
service's HTTP API.

## Airing rules

| # | Rule | Status | Origin |
| --- | --- | --- | --- |
| A1 | A spot may air at most 3 times within one daypart. | canonical — settled station policy | Recovered by reading the rotation guard in `services/traffic/rotation.go`. |
| A2 | Two spots from the same advertiser category must be separated by at least 15 minutes of air time. | proposed — pending confirmation with the sales director | Reverse-engineered from the scheduler in `services/traffic/separation.go`. |
| A3 | Public-service announcements are exempt from the category-separation rule. | canonical | Per programming decision RAD-88 (programming director, 2026-06). |

## Capacity assumption

Planning assumes 12 concurrent station streams. This figure is an invented
placeholder — no real concurrency measurements exist yet; replace it when the
operations team supplies real numbers.
