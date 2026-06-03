# gpi

## 1. Description

The `gpi` event reports a change in the state of a general-purpose input (GPI) pin.

This event includes:

- The GPI pin number
- The new pin state (HIGH/LOW)

Use this event to:

- React to external sensors wired to GPI pins (motion, beam-break, button)
- Trigger workflows when an input changes
- Audit input transitions over time

## 2. Event Details

| Property | Value |
|---|---|
| Event Type | GPI |
| Communication Type | Device to Cloud |
| Applies To | FX7500, FX9600, ATR7000 |
| Trigger Condition | Published when a GPI pin changes state (enable via `managementEventConfig.gpiEvents`) |
| Related Events | async-events, gpo |
| Supported API Versions | V1.0 |

## 3. When This Event Is Published

The reader publishes `gpi` automatically when a GPI pin transitions, provided GPI events are enabled in `managementEventConfig`. No command is required.

| Field | Type | Description |
|---|---|---|
| `pin` | number | GPI pin number (`1`, `2`, `3`, `4`). |
| `state` | string | New pin state: `HIGH` or `LOW`. |

> **Note:** GPI events must be enabled in reader configuration before they are published. The number of available pins depends on the model (see `get_readerCapabilites`).
