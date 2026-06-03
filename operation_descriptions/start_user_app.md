# start_user_app

## Description

The `start_user_app` command starts a user application installed on the reader.

Use this command to:

- Launch an installed user app on demand
- Restart an app after configuration changes
- Bring application logic online after `install_user_app`

## Command Details

| Property | Value |
|---|---|
| Pattern Name | User Application Control — Start |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [stop_user_app](stop_user_app.md), [get_user_apps](get_user_apps.md), [install_user_app](install_user_app.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported API Versions | V1.0 |

MQTT command key: `set_startUserapp`.

## Sending the Command

```json
{
  "command": "set_startUserapp",
  "command_id": "abcd1324",
  "payload": {
    "appname": "sample"
  }
}
```

## Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.appname` | string | Yes | User application name to start. |
