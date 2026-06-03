# get_radio_pkt_logs

## 1. Description

The `get_radio_pkt_logs` command retrieves the radio packet log as a downloadable archive.

This command returns:

- The archive filename
- The Base64-encoded `.tar.gz` log content

No additional payload fields are required to retrieve the radio packet log archive.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Radio Packet Log Retrieval |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | del_radio_pkt_logs, get_logs, get_logs_syslog |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve the radio packet log archive |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_radio_pkt_logs` to:

- Collect low-level radio packet traces for RF diagnostics
- Capture evidence when investigating read-performance issues
- Archive packet logs before purging with `del_radio_pkt_logs`

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `filename` | Archive filename (e.g. `radioPktLog.tar.gz`) | Identifies the downloaded file |
| `binary` | Base64-encoded `.tar.gz` content | Decode and extract to analyze packets |

> **Note:** Radio packet logging must be enabled (see `get_logs`/`set_logs`) for this archive to contain data.
