# set_eSimConfig

## 1. Description

The `set_eSimConfig` command sets the eSIM configuration on the reader.

Use it to:

- Provision cellular connectivity via eSIM profile
- Update eSIM settings for mobile deployments
- Switch eSIM profiles across carriers or regions

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | eSIM Configuration |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_eSimConfig](get_eSimConfig.md), [set_network](set_network.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Set eSIM configuration |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Gather eSIM profile and carrier details before sending.

> **Note:** Request and response schemas for this command are not yet available in `Command Schemas.json` / `Response Schemas.json`. Field details will be added when Zebra publishes them.
