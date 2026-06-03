# start

## Description

The `start` command begins RFID tag reads (or BLE scan) on the reader using the currently configured operating mode.

This command allows you to:

- Start an inventory or read cycle on demand
- Optionally control whether the reader persists tag-read state across restarts

Use this command to:

- Begin RFID inventory after configuring mode with `set_mode`
- Trigger reads without changing RF parameters
- Resume operations after a prior `stop`

## Command Details

| Property | Value |
|---|---|
| Pattern Name | RFID Read Control — Start |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [stop](stop.md), [get_mode](get_mode.md), [set_mode](set_mode.md), [get_status](get_status.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Start tag reads |
| Supported API Versions | V1.0 |

## Before You Begin

Confirm the operating mode is configured before starting reads. `start` triggers the active mode — it does not set RF parameters.

| What You Need | Details |
|---|---|
| Operating mode | Configure with `set_mode` (or verify with `get_mode`) before sending `start`. |
| State persistence | Optional `doNotPersistState` — whether to persist current tag-read state. |
| Radio status | Use `get_status` to confirm the radio is connected. |

## Sending the Command

### Example: Start tag reads

```json
{
  "command": "start",
  "command_id": "abcd1432",
  "payload": {
    "doNotPersistState": true
  }
}
```

## Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.doNotPersistState` | boolean | No | `true` — do not persist tag-read state. `false` — persist state. |

## Reading the Response

The reader responds with `response: "success"` or `"failure"`. Match `command_id` in the response to your request.

> **Note:** Sending `start` while reads are already active may fail — check `get_status` / heartbeat `radioActivity` first.
