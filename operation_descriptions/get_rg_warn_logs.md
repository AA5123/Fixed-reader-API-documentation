# get_rg_warn_logs

## 1. Description

The `get_rg_warn_logs` command retrieves the reader-gateway warning log as a downloadable archive.

This command returns:

- The archive filename
- The Base64-encoded `.tar.gz` log content

No additional payload fields are required to retrieve the warning log archive.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Reader-Gateway Warning Log Retrieval |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | get_rg_error_logs, get_rc_log, get_logs |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve the reader-gateway warning log archive |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_rg_warn_logs` to:

- Review non-fatal reader-gateway warnings
- Spot early signs of degradation before errors occur
- Collect warning logs for support escalation

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `filename` | Archive filename (e.g. `rgWarningLog.tar.gz`) | Identifies the downloaded file |
| `binary` | Base64-encoded `.tar.gz` content | Decode and extract to read warning entries |

> **Note:** Pair with `get_rg_error_logs` to correlate warnings with subsequent errors.
