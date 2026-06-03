# del_syslogs

## Description

The `del_syslogs` command purges system logs stored on the reader, allowing a fresh log collection cycle.

Use this command to:

- Clear syslog archives after collecting them with `get_logs_syslog`
- Free storage consumed by accumulated system logs
- Reset logging before a diagnostic test run

## Command Details

| Property | Value |
|---|---|
| Pattern Name | Syslog Purge |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_logs_syslog](get_logs_syslog.md), [get_logs](get_logs.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported API Versions | V1.0 |

## Before You Begin

Archive logs with `get_logs_syslog` before purging if you need to retain them for support.

MQTT command key: `del_logs_syslog`.

## Sending the Command

### Example: Purge syslogs

```json
{
  "command": "del_logs_syslog",
  "command_id": "abcd1234",
  "payload": {}
}
```

## Reading the Response

The reader responds with `response: "success"` or `"failure"`. Purged logs cannot be recovered.
