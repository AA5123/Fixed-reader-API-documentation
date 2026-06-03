# set_hostname

## 1. Description

The `set_hostname` command sets the network hostname of the reader.

Use it to:

- Assign a recognizable hostname for network identification
- Standardize naming conventions across a fleet
- Update hostname after device relocation or re-provisioning

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Hostname Configuration |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_hostname](get_hostname.md), [set_network](set_network.md), [get_network](get_network.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Set the reader hostname |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Gather these details before sending the command. Duplicate hostnames on the same network can cause resolution conflicts.

| What You Need | Details |
|---|---|
| Hostname | Desired hostname string (payload key is `hostname`, lowercase). |

## 4. Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.hostname` | string | Yes | Hostname to assign to the reader. |

> **Note:** Use `get_hostname` before `set_hostname` to confirm the current value.
