# del_radio_pkt_logs

## Description

The `del_radio_pkt_logs` command purges radio packet logs stored on the reader.

Use this command to:

- Clear radio packet log archives after collecting with `get_radio_pkt_logs`
- Free storage used by high-volume RF packet traces
- Reset packet logging before a new diagnostic session

## Command Details

| Property | Value |
|---|---|
| Pattern Name | Radio Packet Log Purge |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_radio_pkt_logs](get_radio_pkt_logs.md), [set_logs](set_logs.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported API Versions | V1.0 |

## Before You Begin

Download logs with `get_radio_pkt_logs` before purging if you need them for RF analysis.

MQTT command key: `del_logs_radioPacketLog`.

## Sending the Command

### Example: Purge radio packet logs

```json
{
  "command": "del_logs_radioPacketLog",
  "command_id": "abcd1234",
  "payload": {}
}
```

## Reading the Response

The reader responds with `response: "success"` or `"failure"`. Purged logs cannot be recovered.
