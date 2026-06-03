# set_req_usr_app

## 1. Description

The `set_req_usr_app` command sends a custom request or data payload to a user application running on the reader.

Use it to:

- Invoke custom logic in an installed user app
- Pass structured data or commands to the application layer
- Integrate third-party processing on the reader

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | User Application Request |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_user_apps](get_user_apps.md), [start_user_app](start_user_app.md), [stop_user_app](stop_user_app.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Send request to a user application |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Gather these details before sending the command. The target user app must be installed and running.

| What You Need | Details |
|---|---|
| User app name | Exact `appname` from `get_user_apps`. |
| Command/data | String or JSON object to pass to the user app (`payload.command`). |

## 4. Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.userapp` | string | Yes | Target user application name. |
| `payload.command` | string or object | Yes | Custom command or data sent to the user app. |

> **Note:** MQTT command key in the request envelope is `set_reqToUserapp`. Ensure the app is running (`get_user_apps` → `runningStatus`) before sending.
