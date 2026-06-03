# get_rg_error_logs

## 1. Description

The `get_rg_error_logs` command retrieves the reader-gateway error log as a downloadable archive.

This command returns:

- The archive filename
- The Base64-encoded `.tar.gz` log content

No additional payload fields are required to retrieve the error log archive.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Reader-Gateway Error Log Retrieval |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | get_rg_warn_logs, get_rc_log, get_logs |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve the reader-gateway error log archive |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_rg_error_logs` to:

- Investigate reader-gateway errors affecting data delivery
- Collect error logs for support escalation
- Correlate errors with `error` management events

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `filename` | Archive filename (e.g. `rgErrorLog.tar.gz`) | Identifies the downloaded file |
| `binary` | Base64-encoded `.tar.gz` content | Decode and extract to read error entries |

> **Note:** Pair with `get_rg_warn_logs` for a fuller picture of reader-gateway health.
