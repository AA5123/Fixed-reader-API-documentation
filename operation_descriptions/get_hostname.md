# get_hostname

## 1. Description

The `get_hostname` command retrieves the reader's configured hostname.

This command returns:

- The reader hostname

No additional payload fields are required to retrieve the hostname.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Hostname Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | set_hostname, get_network, get_nameAndDescription |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve the reader hostname |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_hostname` to:

- Confirm the reader's network hostname
- Verify the result of a prior `set_hostname` call
- Audit hostname consistency across a fleet

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `hostname` | Reader hostname | Identifies the reader on the network |

> **Note:** The payload key is `hostname` (lowercase). Use `get_hostname` before `set_hostname` to confirm the current value.
