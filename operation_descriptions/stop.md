# stop

## Description

The `stop` command halts active RFID tag reads (or BLE scan) on the reader.

Use this command to:

- Stop an in-progress inventory cycle
- Halt tag reporting before changing mode with `set_mode`
- Return the reader to an idle radio state

## Command Details

| Property | Value |
|---|---|
| Pattern Name | RFID Read Control — Stop |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [start](start.md), [get_mode](get_mode.md), [get_status](get_status.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Stop tag reads |
| Supported API Versions | V1.0 |

## Before You Begin

Stopping when no read is active may still succeed or return failure depending on reader state — safe to send when you need to ensure idle state.

| What You Need | Details |
|---|---|
| Current activity | Optional — check heartbeat `radioActivity` or `get_status` if uncertain. |

## Sending the Command

### Example: Stop tag reads

```json
{
  "command": "stop",
  "command_id": "abcd1324",
  "payload": {}
}
```

## Reading the Response

The reader responds with `response: "success"` or `"failure"`. Match `command_id` in the response to your request.

> **Note:** If no inventory is running, the reader may already be idle — this is not necessarily an error condition.
