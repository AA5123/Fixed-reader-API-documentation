# warning

## 1. Description

The `warning` event reports a warning-level diagnostic message from the reader's Reader Gateway (RG) or Radio subsystems.

This event includes:

- A human-readable `message` describing the warning

Use this event to:

- Spot early signs of degradation before they become errors
- Monitor elevated resource use and rising temperatures
- Track database capacity approaching its limit

## 2. Event Details

| Property | Value |
|---|---|
| Event Type | Warning |
| Communication Type | Device to Cloud |
| Applies To | FX7500, FX9600, ATR7000 |
| Trigger Condition | Published when a monitored warning condition occurs (per `managementEventConfig.warnings`) |
| Related Events | async-events, error, heartbeat |
| Supported API Versions | V1.0 |

## 3. When This Event Is Published

The reader publishes `warning` automatically when a warning condition occurs. No command is required. Representative conditions include:

| Source | Example Conditions |
|---|---|
| Reader Gateway | CPU/RAM/FLASH utilization elevated; NTP sync degraded |
| Radio — Temperature | Ambient or PA temperature high (not yet critical) |
| Radio — Database | Database nearing full; will reset soon |
| NGE API | API error code reported |

### Field

| Field | Type | Description |
|---|---|---|
| `message` | string | Warning message text describing the condition. |

> **Note:** Warnings often precede `error` events for the same subsystem (e.g. "Temperature High" before "Temperature Critical") — use them as early indicators.
