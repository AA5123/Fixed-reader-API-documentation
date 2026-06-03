# get_SupportedRegionList

## 1. Description

The `get_SupportedRegionList` command retrieves the list of RF regions this reader is permitted to operate in.

This command returns:

- The set of supported country/region names

No additional payload fields are required to retrieve the supported region list.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Supported Region Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | get_region, set_region, get_SupportedStandardlist |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve permitted RF regions for this reader |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_SupportedRegionList` to:

- Determine valid values before calling `set_region`
- Confirm a target deployment region is supported by the hardware
- Build a region picker in a provisioning UI

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `SupportedRegions` | Array of supported region names | Only these values are accepted by `set_region` |

> **Note:** Setting a region not in this list will be rejected; validate against `SupportedRegions` first.
