# directionality_tag_data_events

## 1. Description

The `directionality_tag_data_events` payload carries zone-based tag state and direction information during DIRECTIONALITY operating mode.

This event includes:

- Tag identity (`tagId`) and zone state (`NEW`, `UPDATE`, `TRANSITION`, `TIMED_OUT`)
- Current and previous zone numbers, direction, and optional zone/location history

Use this event to:

- Track tag movement between zones (entry/exit detection)
- Determine travel direction when a tag times out
- Build zone-transition analytics and alerting

## 2. Event Details

| Property | Value |
|---|---|
| Event Type | Directionality Tag Data |
| Communication Type | Device to Cloud |
| Applies To | FX7500, FX9600, ATR7000 |
| Trigger Condition | Published on tag zone state changes in DIRECTIONALITY mode |
| Related Events | tagDataEvents, zoneHistory, locationHistory |
| Supported API Versions | V1.0 |

## 3. When This Event Is Published

The reader publishes this payload inside the `tagDataEvents` envelope (`type: DIRECTIONALITY`) when a tag's zone state changes. No command is required beyond starting directionality mode.

| `state` | Meaning | Extra Fields |
|---|---|---|
| `NEW` | Tag first seen in a zone | `zone`, `zoneName` |
| `UPDATE` | Tag still in the same zone | `zone`, `zoneName` |
| `TRANSITION` | Tag moved to a new zone | `zone`, `prevZone`, `prevZoneName` |
| `TIMED_OUT` | Tag left the read field | `direction`, optional `zoneHistory`, `locationHistory` |

### Key Fields

| Field | Type | Description |
|---|---|---|
| `eventNum` | integer | Monotonically increasing message ID. |
| `tagId` | string | Tag EPC/UII in hex. |
| `state` | string | Tag state: `NEW`, `UPDATE`, `TRANSITION`, `TIMED_OUT`. |
| `zone` | integer | Current zone number (1–6). |
| `zoneName` | string | User-defined zone name. |
| `prevZone` | number | Previous zone (TRANSITION only, 1–6). |
| `direction` | string | Travel direction (TIMED_OUT only): `IN`, `OUT`, `NONE`, `UNKNOWN`, `ERROR`. |
| `zoneHistory` | array | Zones traversed (TIMED_OUT + `report_zone_history` enabled). |
| `locationHistory` | array | Location estimates (TIMED_OUT + `report_location_history` enabled). |

> **Note:** `direction` and history arrays are only present in the `TIMED_OUT` state. Enable `report_zone_history` / `report_location_history` in directionality mode settings.
