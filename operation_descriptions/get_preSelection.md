# get_preSelection

## 1. Description

The `get_preSelection` command returns the rxSawFilter status on the reader.

Use this command to:

- Verify whether the rxSaw filter is enabled
- Audit RF pre-selection before starting inventory

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | rxSawFilter Status Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [set_preSelection](set_preSelection.md), [get_mode](get_mode.md) |
| Required Request Fields | `command`, `command_id` |
| Supported Operations | Retrieve rxSawFilter status |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_preSelection` before `set_preSelection` to confirm the current filter state.

> **Note:** Schemas not yet available in Zebra source files. Field details pending.
