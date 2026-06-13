The `get_version` command retrieves detailed hardware and software component version information from the reader's software stack.

This command returns:
- Reader application, radio firmware, and cloud agent versions
- Reader model and serial number
- Available OS upgrade paths and rollback firmware details

No additional payload fields are required to retrieve the full version set. The reader echoes the supplied `command_id` in the response.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Version Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FXR90, FX7500, FX9600, ATR7000 |
| Related Commands | get_status, get_readerCapabilites, set_os, revertback |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve firmware, model, serial number, and upgrade details |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_version` to:
- Confirm the installed firmware versions (Reader App, Radio Firmware) before an OS update
- Verify the exact reader model (e.g., FXR90) when applying model-specific configuration
- Capture the serial number for asset tracking, remote fleet management, or support cases
- Audit available OS upgrade paths or rollback capabilities across a fleet

Key fields to check in the response payload:

| Field | What to Check | Why It Matters |
|---|---|---|
| `readerApplication` | Current reader software version | Determines feature and REST/MQTT API availability |
| `radioFirmware` | Firmware running on the radio module | Affects RF behavior, read performance, and compatibility |
| `model` | Reader model (FXR90 / FX7500 / FX9600 / ATR7000) | Drives physical capabilities and model-specific configurations |
| `serialNumber` | Unique reader serial number | Identifies the device for support and asset records |
| `availableOsUpgrades` | Whether the object is empty `{}` or populated | Indicates if an OS upgrade path is ready to be installed |

> **Note:** Run `get_version` before `set_os` to confirm the current version and the available upgrade paths so you don't reapply an existing build or attempt an incompatible update.
