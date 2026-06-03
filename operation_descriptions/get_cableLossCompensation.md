# get_cableLossCompensation

## 1. Description

The `get_cableLossCompensation` command retrieves the per-read-point cable loss compensation values configured on the reader.

This command returns:

- Cable length per read point
- Cable loss per hundred feet per read point

No additional payload fields are required; values are returned keyed by read point (1–8).

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Cable Loss Compensation Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | set_cableLossCompensation, get_config |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve per-read-point cable loss values |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_cableLossCompensation` to:

- Review compensation values before adjusting transmit power
- Verify cabling assumptions per antenna/read point
- Audit RF link budgets across read points
- Confirm settings after replacing antenna cabling

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `cableLength` | Configured cable length per read point | Used to estimate signal loss |
| `cableLossPerHundredFt` | Loss per hundred feet of cable | Directly affects effective radiated power |

> **Note:** Run `get_cableLossCompensation` before `set_cableLossCompensation` to confirm existing per-read-point values.
