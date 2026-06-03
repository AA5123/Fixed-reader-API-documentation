# zoneHistory

## 1. Description

The `zoneHistory` payload records the sequence of zones a tag traversed before timing out in directionality mode.

This event includes:

- A timestamp and zone number for each zone visit

Use this event to:

- Reconstruct the path a tag took through multiple zones
- Audit zone transitions for compliance or workflow validation
- Debug directionality detection issues

## 2. Event Details

| Property | Value |
|---|---|
| Event Type | Zone History (embedded) |
| Communication Type | Device to Cloud |
| Applies To | FX7500, FX9600, ATR7000 |
| Trigger Condition | Included in `directionality_tag_data_events` on `TIMED_OUT` when `report_zone_history` is enabled |
| Related Events | directionality_tag_data_events, locationHistory |
| Supported API Versions | V1.0 |

## 3. When This Event Is Published

`zoneHistory` is not published as a standalone event. It appears as an array inside `directionality_tag_data_events` when `state` is `TIMED_OUT` and `report_zone_history` is enabled in directionality mode settings.

| Field | Type | Description |
|---|---|---|
| `timestamp` | number | UNIX millisecond timestamp of the zone visit. |
| `Zone` | integer | Zone number (1–6). |

> **Note:** Each array entry represents one zone the tag passed through, in chronological order.
