# get_ntpServer

## 1. Description

The `get_ntpServer` command retrieves the NTP server currently configured for time synchronization on the reader.

This command returns:

- The NTP server hostname or IP address

No additional payload fields are required to retrieve the NTP server setting.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | NTP Server Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | set_ntpServer, get_timeZone, get_status |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve the configured NTP server |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_ntpServer` to:

- Confirm the reader points to the correct time source
- Verify the result of a prior `set_ntpServer` call
- Troubleshoot clock drift affecting event timestamps

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `server` | NTP server hostname or IP address | Determines the reader's time synchronization source |

> **Note:** Use `get_ntpServer` before `set_ntpServer` to confirm the active server and avoid disrupting time sync.
