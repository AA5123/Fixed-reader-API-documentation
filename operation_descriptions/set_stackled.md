# set_stackled

## 1. Description

The `set_stackled` command updates the stack LED state on the reader.

Use it to:

- Drive stack LED colors for operator signaling
- Reflect application or system state on the LED stack
- Coordinate visual indicators with workflow events

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Stack LED Configuration |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_stackled](get_stackled.md), [set_appled](set_appled.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Set stack LED state |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Gather stack LED parameters before sending. Exact field names are pending schema publication.

> **Note:** Request and response schemas for this command are not yet available in `Command Schemas.json` / `Response Schemas.json`. Field details will be added when Zebra publishes them.
