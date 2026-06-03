# get_rc_log

## 1. Description

The `get_rc_log` command retrieves the radio-control information log as a downloadable archive.

This command returns:

- The archive filename
- The Base64-encoded `.tar.gz` log content

No additional payload fields are required to retrieve the radio-control log archive.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Radio-Control Log Retrieval |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | get_rg_error_logs, get_rg_warn_logs, get_logs |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve the radio-control information log archive |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_rc_log` to:

- Investigate radio-control behavior and RF issues
- Collect radio-control logs for support escalation
- Correlate radio events with inventory anomalies

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `filename` | Archive filename (e.g. `rcLog.tar.gz`) | Identifies the downloaded file |
| `binary` | Base64-encoded `.tar.gz` content | Decode and extract to read radio-control entries |

> **Note:** Use alongside `get_radio_pkt_logs` when diagnosing low-level RF problems.
