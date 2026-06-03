# stop_user_app

## Description

The `stop_user_app` command stops a running user application on the reader.

Use this command to:

- Halt a user app before uninstalling or updating
- Free CPU/memory resources on the reader
- Pause application logic during maintenance

## Command Details

| Property | Value |
|---|---|
| Pattern Name | User Application Control — Stop |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [start_user_app](start_user_app.md), [get_user_apps](get_user_apps.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported API Versions | V1.0 |

MQTT command key: `set_stopUserapp`.

## Sending the Command

```json
{
  "command": "set_stopUserapp",
  "command_id": "abcd1324",
  "payload": {
    "appname": "sample"
  }
}
```

## Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.appname` | string | Yes | User application name to stop. |
