# get_timeZone

## 1. Description

The `get_timeZone` command retrieves the time zone currently configured on the reader.

This command returns:

- The configured time zone value

No additional payload fields are required to retrieve the time zone.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Time Zone Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | set_timeZone, get_ntpServer, get_status |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve the configured time zone |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_timeZone` to:

- Confirm the reader's time zone before relying on event timestamps
- Verify the result of a prior `set_timeZone` call
- Audit time zone consistency across a fleet

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `timeZone` | Configured time zone value | Affects local time interpretation of timestamps |

> **Note:** Use `get_timeZone` before `set_timeZone` to confirm the current setting; pair with `get_ntpServer` for full time configuration.
