# set_cableLossCompensation

## 1. Description

The `set_cableLossCompensation` command sets cable loss compensation values on the reader, either globally for all read points or individually per read point.

Use it to:

- Compensate for signal loss due to antenna cable length
- Apply the same compensation to all read points at once
- Tune compensation per read point for multi-antenna deployments

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Cable Loss Compensation Configuration |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_cableLossCompensation](get_cableLossCompensation.md), [get_config](get_config.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Set cable loss compensation (all or per read point) |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Gather these details before sending the command. Use either the **All** variant (flat fields) or the **Each** variant (per read-point keys) — not both in the same payload.

| What You Need | Details |
|---|---|
| Variant | **All** — single `cableLength` + `cableLossPerHundredFt` for every read point. **Each** — per read-point keys `"1"` through `"8"`. |
| Cable length | Length of antenna cable (integer; float values accepted). |
| Cable loss | Loss per hundred feet of cable (integer; float values accepted). |

> **Note:** Cable loss compensation is not applicable to ATR7000 readers.

## 4. Payload Variants

The payload shape is determined by whether you set all read points at once or individually.

- **All** — Provide `cableLength` and `cableLossPerHundredFt` at the root of the payload. Applies the same values to every read point.
- **Each** — Provide numeric string keys (`"1"`, `"2"`, … up to `"8"`), each containing its own `cableLength` and `cableLossPerHundredFt`.

## 5. Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.cableLength` | integer | Yes (All variant) | Cable length for all read points. |
| `payload.cableLossPerHundredFt` | integer | Yes (All variant) | Loss per 100 ft for all read points. |
| `payload.<readPoint>` | object | Yes (Each variant) | Read point key (`"1"`–`"8"`). |
| `payload.<readPoint>.cableLength` | integer | Yes (Each variant) | Cable length for that read point. |
| `payload.<readPoint>.cableLossPerHundredFt` | integer | Yes (Each variant) | Loss per 100 ft for that read point. |

> **Note:** Use `get_cableLossCompensation` before this command to confirm existing values.
