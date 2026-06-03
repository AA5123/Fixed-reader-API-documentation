# get_SupportedStandardlist

## 1. Description

The `get_SupportedStandardlist` command retrieves the list of RF regulatory standards supported by the reader and the channel details for each.

This command returns:

- Supported standard names
- LBT and hopping configurability per standard
- Enabled channel data per standard

No additional payload fields are required to retrieve the supported standard list.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Supported Standard Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | get_region, set_region, get_SupportedRegionList |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve supported regulatory standards and channels |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_SupportedStandardlist` to:

- Discover which regulatory standards apply for a region
- Determine whether LBT or channel hopping is configurable
- Inspect channel availability before tuning RF settings

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `StandardName` | RF regulatory standard name | Identifies the applicable standard |
| `isLBTConfigurable` | Whether LBT can be configured | Determines LBT options for the standard |
| `channelData` | Enabled channel list | Shows usable spectrum for the standard |
| `isHoppingConfigurable` | Whether channel selection is configurable | Controls frequency-hopping options |

> **Note:** Standard availability is tied to the configured region; review `get_region` alongside this list.
