The `GET /cloud/version` REST endpoint and the `get_version` MQTT command retrieve detailed hardware and software component information from the reader's software stack.

This operation returns:
- Reader application, radio firmware, and cloud agent versions
- Reader model and serial number
- Available OS upgrade paths and rollback firmware details

This is a stateless operation. The REST endpoint does not require a request body payload, and the MQTT command only requires the standard command envelope without additional payload fields. For MQTT, the reader will echo the supplied `command_id` in the response.

## 1. Operation Details

| Property | Value |
|---|---|
| Pattern Name | Version Query |
| Supported Protocols | REST (HTTP/HTTPS), MQTT |
| Communication Type | Synchronous (REST), Bidirectional (MQTT) |
| Applies To | FXR90, FX7500, FX9600, ATR7000 |
| Related Operations | status, readerCapabilities, os (update), revertback |
| Required Request Fields | None (REST) / `command`, `command_id` (MQTT) |
| Supported Response Sections | JSON Body (REST) / `payload` (MQTT) |

## 2. When to Use This Command / Endpoint

Use `GET /cloud/version` or `get_version` to:
- Confirm the installed firmware versions (Reader App, Radio Firmware) before or after performing a system update.
- Verify the exact reader model (e.g., FXR90) when applying model-specific configuration.
- Capture the serial number for asset tracking, remote fleet management, or support cases.
- Audit available OS upgrade paths or rollback capabilities across a fleet.
- Validate API compatibility, as newer firmware versions may introduce new features or schema changes.

## 3. Key Fields to Check in the Response

| Field | What to Check | Why It Matters |
|---|---|---|
| `readerApplication` | Current reader software version | Determines feature and REST/MQTT API availability. |
| `radioFirmware` | Firmware running on the radio module | Affects RF behavior, read performance, and compatibility. |
| `model` | Reader model (FXR90 / FX7500 / FX9600 / ATR7000) | Drives physical capabilities, antenna limits, and model-specific configurations. |
| `serialNumber` | Unique reader serial number | Identifies the device securely for support and asset records. |
| `availableOsUpgrades` | Whether the object is empty `{}` or populated | Indicates if an OS upgrade path has been downloaded and is ready to be installed. |

> **Note:** Run this version query before triggering an OS update (`set_os`) to confirm the current version and available upgrade paths, ensuring you do not reapply an existing build or attempt an incompatible update. The `model` field will strictly return one of the predefined supported hardware identifiers.
