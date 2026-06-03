# get_availableWifiNetworks

## 1. Description

The `get_availableWifiNetworks` command retrieves Wi-Fi networks visible to the reader.

Use this command to:

- Discover available SSIDs during Wi-Fi provisioning
- Troubleshoot wireless connectivity issues

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Wi-Fi Scan Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_network](get_network.md), [set_network](set_network.md) |
| Required Request Fields | `command`, `command_id` |
| Supported Operations | Scan for available Wi-Fi networks |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use during initial Wi-Fi setup or when the reader cannot connect to the configured network.

> **Note:** Schemas not yet available in Zebra source files. Field details pending.
