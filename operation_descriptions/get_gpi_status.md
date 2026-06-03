# get_gpi_status

## 1. Description

The `get_gpi_status` command retrieves the current state of each general-purpose input (GPI) pin on the reader.

This command returns:

- The HIGH/LOW state of each GPI pin (1–4)

No additional payload fields are required to retrieve all pin states.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | GPI Status Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | get_gpostatus, set_gpo, get_readerCapabilites |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve current GPI pin states |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_gpi_status` to:

- Read the current state of external sensors wired to GPI pins
- Confirm a trigger source (e.g. motion sensor, beam break) before enabling start/stop triggers
- Audit input state during troubleshooting

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `1`–`4` | HIGH/LOW state of each GPI pin | Reflects the signal level from connected input devices |

> **Note:** The number of usable GPI pins depends on the model; check `numGPIs` from `get_readerCapabilites`.
