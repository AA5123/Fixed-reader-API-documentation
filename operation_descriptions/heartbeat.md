# heartbeat

## 1. Description

The `heartbeat` event provides a periodic health and activity snapshot of the reader for operational monitoring.

This event includes:

- Radio activity, connection state, and tag-read counts
- Reader-gateway event-delivery statistics
- System temperature, uptime, and user-app status

Use this event to:

- Confirm the reader is alive and reporting
- Track radio activity and tag throughput over time
- Monitor temperature and uptime for health dashboards

## 2. Event Details

| Property | Value |
|---|---|
| Event Type | Heartbeat |
| Communication Type | Device to Cloud |
| Applies To | FX7500, FX9600, ATR7000 |
| Trigger Condition | Published periodically per `managementEventConfig.heartbeat` configuration |
| Related Events | async-events, error, warning |
| Supported API Versions | V1.0 |

## 3. When This Event Is Published

The reader publishes `heartbeat` on a periodic interval configured in `managementEventConfig`. No command is required.

| Field | Type | What to Check |
|---|---|---|
| `radio_control.radioActivity` | string | Inventory state: `active`, `inactive`, `unknown`. |
| `radio_control.radioConnection` | string | Radio link: `connected`, `disconnected`. |
| `radio_control.numTagReads` | number | Total tags read (throughput indicator). |
| `reader_gateway.numManagementEventsTxed` | number | Management events sent to cloud. |
| `system.temperature.ambient` | number | Reader ambient temperature. |
| `system.uptime` | string | Reader uptime (hours:min:seconds). |
| `userapps[].status` | string | User app status: `running`, `stopped`. |

> **Note:** Use the heartbeat interval as a liveness timeout — if a heartbeat is missed for longer than the configured interval, treat the reader as unreachable.
