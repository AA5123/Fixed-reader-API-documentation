# async-events

## 1. Description

The `async-events` envelope is the common wrapper for all asynchronous management events the reader publishes to configured management endpoints (`managementEventConfig` in reader configuration).

This event includes:

- An event `type` discriminator and `timestamp`
- The source `component` (`RG`, `RC`, or a user-app name) and an `eventNum`
- A `data` payload whose shape depends on `type`

Use this event to:

- Receive device health, GPIO, firmware, and diagnostic events in one channel
- Route events to the correct handler based on `type`
- Correlate events using `component` and `eventNum`

## 2. Event Details

| Property | Value |
|---|---|
| Event Type | Management Event Envelope |
| Communication Type | Device to Cloud |
| Applies To | FX7500, FX9600, ATR7000 |
| Trigger Condition | Wraps every asynchronous management event published by the reader |
| Related Events | heartbeat, firmwareUpdateProgress, gpi, gpo, error, warning, userapp_event |
| Supported API Versions | V1.0 |

## 3. When This Event Is Published

The reader publishes management events automatically to the endpoints set in `managementEventConfig`. No command is required. The `type` field selects which payload appears in `data`.

| `type` | `data` payload | Description |
|---|---|---|
| `heartbeat` | heartbeat | Periodic health snapshot |
| `firmwareUpdateProgress` | firmwareUpdateProgress | Firmware update status |
| `gpi` | gpi | GPI pin state change |
| `gpo` | gpo | GPO pin state change |
| `error` | error | Error diagnostic message |
| `warning` | warning | Warning diagnostic message |
| `userapp` | userapp_event | Custom user-application event |

### Envelope Fields

| Field | Type | Description |
|---|---|---|
| `type` | string | Event type (selects `data` payload). |
| `timestamp` | string (date-time) | Event timestamp. |
| `component` | string | Event source: `RG`, `RC`, or `<appname>`. |
| `eventNum` | number | Event sequence number. |
| `data` | object (oneOf) | Event payload matching `type`. |

> **Note:** Subscribe once to the management endpoint and branch on `type` rather than configuring a separate channel per event.
