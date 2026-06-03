# get_mode

## 1. Description

The `get_mode` command retrieves the reader's current operating mode and the RF settings associated with that mode.

This command returns:

- The operating mode type (SIMPLE, INVENTORY, PORTAL, etc.)
- Active antennas/beams and transmit power
- Environment profile and mode-specific settings

No additional payload fields are required to retrieve the active mode.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Operating Mode Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | set_mode, start, stop, get_config |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve active operating mode and RF settings |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_mode` to:

- Confirm the active mode before starting an inventory
- Verify antenna/beam and transmit power selection
- Check the environment profile in use
- Review mode-specific settings before changing them

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `type` | Operating mode (SIMPLE / INVENTORY / PORTAL / …) | Determines RF behavior and reported data |
| `antennas` | Active antenna ports or ATR beams | Controls coverage area |
| `transmitPower` | Desired TX power in dBm | Affects read range and regulatory compliance |
| `environment` | Interference environment profile | Tunes the radio for the deployment site |

> **Note:** Run `get_mode` before `set_mode` to review current RF settings and avoid disrupting an active read cycle.
