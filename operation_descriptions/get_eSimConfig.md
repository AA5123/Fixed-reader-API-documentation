# get_eSimConfig

## 1. Description

The `get_eSimConfig` command retrieves the eSIM configuration on the reader.

Use this command to:

- Audit cellular/eSIM settings before changes
- Verify eSIM profile configuration on mobile readers

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | eSIM Configuration Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [set_eSimConfig](set_eSimConfig.md), [get_network](get_network.md) |
| Required Request Fields | `command`, `command_id` |
| Supported Operations | Retrieve eSIM configuration |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

> **Note:** Schemas not yet available in Zebra source files. Field details pending.
