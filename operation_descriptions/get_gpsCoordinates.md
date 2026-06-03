# get_gpsCoordinates

## 1. Description

The `get_gpsCoordinates` command retrieves the reader's current GPS coordinates.

Use this command to:

- Record reader location for asset tracking
- Verify GPS module functionality on mobile deployments

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | GPS Coordinates Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_network](get_network.md) |
| Required Request Fields | `command`, `command_id` |
| Supported Operations | Retrieve GPS coordinates |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

> **Note:** Schemas not yet available in Zebra source files. Field details pending.
