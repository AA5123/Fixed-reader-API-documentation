# get_readPoints

## 1. Description

The `get_readPoints` command retrieves the read points configured on the reader.

Use this command to:

- Audit antenna/read-point configuration
- Map read points before cable-loss compensation changes

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Read Point Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_cableLossCompensation](get_cableLossCompensation.md), [set_cableLossCompensation](set_cableLossCompensation.md) |
| Required Request Fields | `command`, `command_id` |
| Supported Operations | Retrieve read point configuration |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

> **Note:** Schemas not yet available in Zebra source files. Field details pending.
