# set_region

## 1. Description

The `set_region` command updates the reader's RF region and regulatory settings.

Use it to:

- Set the deployment region to match the country of operation
- Change regulatory standard and channel configuration
- Re-provision a reader moved to a new geographic location

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Region Configuration |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_region](get_region.md), [get_SupportedRegionList](get_SupportedRegionList.md), [get_SupportedStandardlist](get_SupportedStandardlist.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Update RF region configuration |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Gather these details before sending the command. The target region must appear in `get_SupportedRegionList`.

| What You Need | Details |
|---|---|
| Target region | Region name from the supported region list. |
| Regulatory standard | Standard and channel settings for the region (see `get_SupportedStandardlist`). |

> **Note:** Request and response schemas for this command are not yet available in `Command Schemas.json` / `Response Schemas.json`. Field details will be added when Zebra publishes them. Use `get_region` to review the current configuration in the meantime.
