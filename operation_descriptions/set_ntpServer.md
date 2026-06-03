# set_ntpServer

## 1. Description

The `set_ntpServer` command sets the NTP server used by the reader for time synchronization.

Use it to:

- Point the reader to your organization's NTP server
- Correct clock drift affecting event and log timestamps
- Standardize NTP configuration across a fleet

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | NTP Server Configuration |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_ntpServer](get_ntpServer.md), [set_timeZone](set_timeZone.md), [get_status](get_status.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Set the NTP server address |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Gather these details before sending the command. An unreachable NTP server will leave the reader clock unsynchronized.

| What You Need | Details |
|---|---|
| NTP server | Hostname or IP address of a reachable NTP server on the reader's network. |

## 4. Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.server` | string | Yes | NTP server hostname or IP address. |

> **Note:** Use `get_ntpServer` before `set_ntpServer` to confirm the current server.
