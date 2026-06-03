# get_user_apps

## 1. Description

The `get_user_apps` command retrieves the list of user applications installed on the reader.

This command returns:

- An array of installed user apps, each with name, autostart flag, running status, and metadata

No additional payload fields are required to retrieve all installed user apps.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | User Application Inventory Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | install_user_app, uninstall-user-app, start_user_app, stop_user_app, autostart_user_app |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve the list of installed user applications |
| Supported Response Sections | payload (array) |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_user_apps` to:

- Confirm which user apps are installed before start/stop/uninstall
- Check whether an app is currently running
- Verify autostart configuration per app
- Audit deployed applications across a fleet

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `appname` | User app name | Identifies the app for start/stop/uninstall |
| `autostart` | Autostart setting | Determines whether the app launches on boot |
| `runningStatus` | Whether the app is running | Confirms current execution state |
| `metadata` | User app metadata string | Provides version/context details |

> **Note:** Use `get_user_apps` to obtain the exact `appname` before calling `start_user_app`, `stop_user_app`, or `uninstall-user-app`.
