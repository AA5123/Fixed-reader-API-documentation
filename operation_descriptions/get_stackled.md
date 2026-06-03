# get_stackled

## 1. Description

The `get_stackled` command retrieves the current state of the stack LED on the reader.

This command returns stack LED status information.

Use this command to:

- Confirm stack LED state before calling `set_stackled`
- Audit LED indicators during health checks

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Stack LED Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [set_stackled](set_stackled.md), [get_appled](get_appled.md) |
| Required Request Fields | `command`, `command_id` |
| Supported Operations | Retrieve stack LED state |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_stackled` to read the current stack LED configuration and state.

> **Note:** Request and response schemas are not yet available in `Command Schemas.json` / `Response Schemas.json`. Response field details will be added when Zebra publishes them.
