# tagDataEvents

## 1. Description

The `tagDataEvents` envelope is the common wrapper for all RFID tag read payloads the reader publishes to configured data endpoints.

This event includes:

- The operating mode `type` and a `timestamp`
- A `data` payload whose shape depends on the mode

Use this event to:

- Receive tag reads from inventory, portal, conveyor, and directionality modes
- Route tag data to the correct handler based on `type`
- Correlate reads using `timestamp` and `eventNum` (in the inner payload)

## 2. Event Details

| Property | Value |
|---|---|
| Event Type | Tag Data Event Envelope |
| Communication Type | Device to Cloud |
| Applies To | FX7500, FX9600, ATR7000 |
| Trigger Condition | Published when the reader reports tag reads during an active operating mode |
| Related Events | mode_tag_data_events, directionality_tag_data_events |
| Supported API Versions | V1.0 |

## 3. When This Event Is Published

The reader publishes `tagDataEvents` automatically to configured data endpoints while inventory or directionality is active. No command is required.

| `type` | `data` payload | Description |
|---|---|---|
| `SIMPLE` | mode_tag_data_events | Basic tag read |
| `INVENTORY` | mode_tag_data_events | Timed/triggered inventory read |
| `PORTAL` | mode_tag_data_events | Portal/dock read |
| `CONVEYOR` | mode_tag_data_events | Conveyor read |
| `CUSTOM` | mode_tag_data_events | Custom mode read |
| `DIRECTIONALITY` | directionality_tag_data_events | Zone/direction tag state |

### Envelope Fields

| Field | Type | Description |
|---|---|---|
| `type` | string | Operating mode (selects `data` payload). |
| `timestamp` | string (date-time) | Tag read timestamp (ISO 8601). |
| `data` | object (oneOf) | Tag read payload matching `type`. |

> **Note:** Configure data endpoints in `set_config` / `set_importCloudConfig` before tag data will flow to your backend.
