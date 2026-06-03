# error

## 1. Description

The `error` event reports an error-level diagnostic message from the reader's Reader Gateway (RG) or Radio Control (RC) subsystems.

This event includes:

- A human-readable `message` describing the error

Use this event to:

- Detect critical conditions (antenna disconnects, critical temperature, radio/Tx failures)
- Monitor resource exhaustion (CPU, RAM, flash, database full)
- Feed alerting pipelines for operational issues

## 2. Event Details

| Property | Value |
|---|---|
| Event Type | Error |
| Communication Type | Device to Cloud |
| Applies To | FX7500, FX9600, ATR7000 |
| Trigger Condition | Published when a monitored error condition occurs (per `managementEventConfig.errors`) |
| Related Events | async-events, warning, heartbeat |
| Supported API Versions | V1.0 |

## 3. When This Event Is Published

The reader publishes `error` automatically when an error condition occurs. No command is required. Representative conditions include:

| Source | Example Conditions |
|---|---|
| Reader Gateway | CPU/RAM/FLASH utilization thresholds; NTP sync failure; data endpoint disconnected; retention queue full |
| Radio Control — Antennas | Antenna disconnected/reconnected on a port |
| Radio Control — Temperature | Ambient or PA temperature critical |
| Radio Control — Radio | Tx (PA) failure on a port; NGE stopped/errored; tag-info parse error |
| Radio Control — Database | Database full and reset; NGE reset failures |

### Field

| Field | Type | Description |
|---|---|---|
| `message` | string | Error message text describing the condition. |

> **Note:** Error events carry a free-text `message`; parse known substrings (e.g. "Antenna Disconnected on Port") to classify and route alerts.
