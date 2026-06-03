# set_password

## 1. Description

The `set_password` command changes the password on the reader.

Use it to:

- Rotate the reader login password as part of security policy
- Set an initial password on a newly deployed reader
- Recover from a compromised credential

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Password Change |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [localrest_login](localrest_login.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Change reader password |
| Supported API Versions | V1.0 |

> **Security Note:** Never hardcode passwords in your payload or source code. Supply credentials at runtime from a secrets manager.

## 3. Before You Begin

Gather the current and new password values before sending. A failed change may lock you out if the old password is incorrect.

> **Note:** Request and response schemas for this command are not yet available in `Command Schemas.json` / `Response Schemas.json`. Field details will be added when Zebra publishes them.
