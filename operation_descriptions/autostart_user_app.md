# autostart_user_app

## Description

The `autostart_user_app` command configures whether a user application starts automatically when the reader boots.

Use this command to:

- Enable autostart for production user apps
- Disable autostart for test or manual-only apps
- Standardize boot behavior across a fleet

## Command Details

| Property | Value |
|---|---|
| Pattern Name | User Application Autostart Configuration |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_user_apps](get_user_apps.md), [start_user_app](start_user_app.md), [install_user_app](install_user_app.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported API Versions | V1.0 |

MQTT command key: `set_autostartUserapp`.

## Sending the Command

```json
{
  "command": "set_autostartUserapp",
  "command_id": "abcd1324",
  "payload": {
    "appname": "sample",
    "autostart": true
  }
}
```

## Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.appname` | string | Yes | User application name. |
| `payload.autostart` | boolean | Yes | `true` — start on boot. `false` — manual start only. |
