# get_bleConfig

## 1. Description

The `get_bleConfig` command retrieves BLE (Bluetooth Low Energy) configuration from the reader.

Use this command to:

- Audit BLE settings before changes
- Verify BLE is configured for beacon/tag scanning workflows

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | BLE Configuration Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [set_bleConfig](set_bleConfig.md), [start](start.md), [stop](stop.md) |
| Required Request Fields | `command`, `command_id` |
| Supported Operations | Retrieve BLE configuration |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

> **Note:** Schemas not yet available in Zebra source files. Field details pending.
