# get_gpostatus

## 1. Description

The `get_gpostatus` command retrieves the current state of each general-purpose output (GPO) pin on the reader.

This command returns:

- The HIGH/LOW state of each GPO pin (1–4)

No additional payload fields are required to retrieve all pin states.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | GPO Status Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | set_gpo, get_gpi_status, get_readerCapabilites |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve current GPO pin states |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_gpostatus` to:

- Confirm GPO pin states before or after a `set_gpo` call
- Verify external signaling (lights, horns, gates) is in the expected state
- Audit output state during troubleshooting

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `1`–`4` | HIGH/LOW state of each GPO pin | Reflects the actual electrical state driving external devices |

> **Note:** The number of usable GPO pins depends on the model; check `numGPOs` from `get_readerCapabilites`.
