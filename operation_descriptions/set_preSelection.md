# set_preSelection

## 1. Description

The `set_preSelection` command enables or disables the rxSawFilter on the reader.

Use it to:

- Turn the rxSaw filter on or off for RF pre-selection
- Tune receiver sensitivity for the deployment environment
- Adjust filter settings before starting inventory

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | rxSawFilter Configuration |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_preSelection](get_preSelection.md), [set_mode](set_mode.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Enable or disable rxSawFilter |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Confirm the desired rxSawFilter state before sending.

> **Note:** Request and response schemas for this command are not yet available in `Command Schemas.json` / `Response Schemas.json`. Field details will be added when Zebra publishes them.
