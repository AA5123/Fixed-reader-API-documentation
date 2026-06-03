# get_readerCapabilites

## 1. Description

The `get_readerCapabilites` command retrieves the static hardware and software capabilities of the reader.

This command returns:

- GPIO capacity (number of GPIs and GPOs)
- Protocol support (e.g. LLRP)
- Supported endpoint types and API versions

No additional payload fields are required to retrieve the capability set.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Reader Capability Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | get_version, get_status, get_config |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve static reader capabilities |
| Supported Response Sections | capabilities |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_readerCapabilites` to:

- Discover how many GPI/GPO pins are available before wiring logic
- Confirm whether LLRP is supported on this model
- Determine which endpoint types can be configured for data/management
- Verify the API versions the reader accepts

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `numGPIs` | Number of GPI pins supported | Bounds valid GPI configuration |
| `numGPOs` | Number of GPO pins supported | Bounds valid GPO configuration |
| `llrpSupported` | Whether LLRP is supported | Determines protocol options |
| `endpointTypesSupported` | Supported endpoint types | Drives valid endpoint configuration |

> **Note:** Capabilities are static per model; cache the result rather than polling it repeatedly.
