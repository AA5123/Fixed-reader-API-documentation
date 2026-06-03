# gpo

## 1. Description

The `gpo` event reports a change in the state of a general-purpose output (GPO) pin.

This event includes:

- The GPO pin number
- The new pin state (HIGH/LOW)

Use this event to:

- Confirm a GPO drove an external device (light, horn, gate)
- Audit output transitions, including those caused by `set_gpo`
- Synchronize external state with reader logic

## 2. Event Details

| Property | Value |
|---|---|
| Event Type | GPO |
| Communication Type | Device to Cloud |
| Applies To | FX7500, FX9600, ATR7000 |
| Trigger Condition | Published when a GPO pin changes state |
| Related Events | async-events, gpi |
| Supported API Versions | V1.0 |

## 3. When This Event Is Published

The reader publishes `gpo` automatically when a GPO pin transitions. No command is required.

| Field | Type | Description |
|---|---|---|
| `pin` | number | GPO pin number (`1`, `2`, `3`, `4`). |
| `state` | string | New pin state: `HIGH` or `LOW`. |

> **Note:** Use `get_gpostatus` to query current GPO states on demand; use this event to be notified of changes as they happen.
