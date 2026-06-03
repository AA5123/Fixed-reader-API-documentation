# revertback

## Description

The `revertback` command reverts the reader firmware to the previous OS version on the secondary partition.

Use this command to:

- Roll back after a failed or unwanted `set_os` upgrade
- Restore the last known-good firmware
- Recover from compatibility issues with a new OS build

## Command Details

| Property | Value |
|---|---|
| Pattern Name | Firmware Rollback |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [set_os](set_os.md), [get_version](get_version.md), [reboot](reboot.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported API Versions | V1.0 |

MQTT command key: `set_revertbackOS`.

## Before You Begin

Plan for downtime — the reader reboots to the secondary partition. Monitor `firmwareUpdateProgress` events during rollback.

## Sending the Command

```json
{
  "command": "set_revertbackOS",
  "command_id": "abcd1434",
  "payload": {}
}
```

## Reading the Response

The reader responds with `response: "success"` or `"failure"`, then reboots. Confirm the rolled-back version with `get_version` after reconnect.
