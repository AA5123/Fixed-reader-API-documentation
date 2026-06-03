# get_config

## 1. Description

The `get_config` command retrieves the reader's full configuration, including RF/XML configuration, GPIO and LED defaults, and reader-gateway endpoint settings.

This command returns:

- The current reader XML configuration
- GPIO and LED default states
- Reader-gateway settings (tag data retention, batching, and endpoint configuration)

No additional payload fields are required to retrieve the full configuration.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Reader Configuration Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | set_config, set_importCloudConfig, get_status, get_readerCapabilites |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve active reader configuration details |
| Supported Response Sections | xml, GPIO-LED, READER-GATEWAY |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_config` to:

- Review the active configuration before calling `set_config`
- Audit GPIO/LED default states across readers
- Inspect tag-data retention and batching settings
- Confirm configured data/management endpoints

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `xml` | Current reader XML configuration | Source of truth for RF/reader settings |
| `GPIO-LED` | GPO and LED default states | Confirms startup pin/LED behavior |
| `READER-GATEWAY.retention` | Tag-data retention on disconnect | Controls data buffering behavior |
| `READER-GATEWAY.batching` | Tag-data batching configuration | Affects throughput and message size |

> **Note:** Use `get_config` before `set_config` to review existing settings and avoid overwriting active configuration unexpectedly.
