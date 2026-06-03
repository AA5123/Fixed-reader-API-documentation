# set_appled

## 1. Description

The `set_appled` command sets the color, duration, and flash behavior of the application LED on the reader.

Use it to:

- Drive the app LED to a specific color for operator signaling
- Update how long the LED stays in the requested state
- Enable or disable flashing for attention/alerting

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Application LED Configuration |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_appled](get_appled.md), [set_stackled](set_stackled.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Set application LED state |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Gather these details before sending the command. An out-of-range color or duration will be rejected with a `failure` response.

| What You Need | Details |
|---|---|
| LED color | One of `red`, `amber`, `green`, `off` (lowercase). |
| Duration | Seconds the LED stays in this state (default `60`). |
| Flash | Whether the LED should flash while active. |

## 4. Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.color` | string | Yes | LED color. Allowed: `red`, `amber`, `green`, `off`. |
| `payload.seconds` | integer | Yes | Duration the LED state remains active (default `60`). |
| `payload.flash` | boolean | Yes | `true` — LED flashes. `false` — LED stays solid. |
