# set_passthru

## 1. Description

The `set_passthru` command sends a pass-through command to the reader for low-level or vendor-specific operations.

Use it to:

- Forward custom commands not covered by the standard API
- Invoke reader-specific extensions during diagnostics
- Integrate legacy or proprietary control sequences

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Pass-Through Command |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_status](get_status.md), [set_config](set_config.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Send pass-through command |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Understand the pass-through payload format required by your use case before sending.

> **Note:** Request and response schemas for this command are not yet available in `Command Schemas.json` / `Response Schemas.json`. Field details will be added when Zebra publishes them.
