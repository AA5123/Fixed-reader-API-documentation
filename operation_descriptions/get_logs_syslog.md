# get_logs_syslog

## 1. Description

The `get_logs_syslog` command retrieves the reader's system log as a downloadable archive.

This command returns:

- The archive filename
- The Base64-encoded `.tar.gz` log content

No additional payload fields are required to retrieve the syslog archive.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Syslog Retrieval |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | del_syslogs, get_logs, get_radio_pkt_logs |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve the system log archive |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_logs_syslog` to:

- Collect system logs for support or diagnostics
- Capture a log snapshot before rebooting or updating
- Archive logs before purging with `del_syslogs`

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `filename` | Archive filename (e.g. `syslog.tar.gz`) | Identifies the downloaded file |
| `binary` | Base64-encoded `.tar.gz` content | Decode and extract to read the logs |

> **Note:** The `binary` field can be large; ensure your MQTT client and broker allow a sufficient payload size.
