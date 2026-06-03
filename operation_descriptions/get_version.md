# get_version

## 1. Description

The `get_version` command retrieves firmware and component version information from the reader's software stack.

This command returns:

- Reader application and radio firmware versions
- Reader model and serial number
- Available OS upgrade paths

No additional payload fields are required to retrieve the full version set. The reader echoes the supplied `command_id` in the response.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Version Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | get_status, get_readerCapabilites, set_os, revertback |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve firmware, model, and serial number details |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_version` to:

- Confirm the installed firmware version before an OS update
- Verify the reader model when applying model-specific configuration
- Capture the serial number for asset tracking or support cases
- Audit available OS upgrade paths across a fleet

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `readerApplication` | Current reader software version | Determines feature/API availability |
| `radioFirmware` | Firmware running on the radio | Affects RF behavior and compatibility |
| `model` | Reader model (FX7500 / FX9600 / ATR7000) | Drives model-specific configuration |
| `serialNumber` | Unique reader serial number | Identifies the device for support/asset records |

> **Note:** Run `get_version` before `set_os` to confirm the current version and the available upgrade paths so you don't reapply an existing build.
