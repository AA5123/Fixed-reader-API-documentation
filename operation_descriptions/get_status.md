# get_status

## 1. Description

The `get_status` command retrieves operational statistics and health information from the reader at the moment of the request.

This command returns:

- Uptime and current system time
- Radio connection and activity state
- Reader temperature

No additional payload fields are required to retrieve the full status snapshot.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Reader Status Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | get_version, get_readerCapabilites, get_config |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve live operational statistics and health |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_status` to:

- Confirm the reader is powered, healthy, and reachable
- Verify the radio is connected before starting inventory
- Monitor reader temperature for thermal issues
- Synchronize against the reader's current system time

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `uptime` | How long the reader has been running | Detects unexpected reboots |
| `systemTime` | ISO 8601 reader clock value | Confirms time sync for event timestamps |
| `radioConnection` | Radio connection status | Radio must be connected for RF operations |
| `temperature` | Current reader temperature (°C) | High temperature can throttle or stop the radio |

> **Note:** The status payload uses the field name `radioActivitiy` (spelling as returned by the reader) for radio activity state.
