# set_nameAndDescription

## 1. Description

The `set_nameAndDescription` command sets the human-friendly name and description of the reader.

Use it to:

- Label a reader with a site-specific display name
- Add a description for location, purpose, or asset tracking
- Update naming after deployment or re-provisioning

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Name & Description Configuration |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_nameAndDescription](get_nameAndDescription.md), [set_hostname](set_hostname.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Set reader name and description |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Gather these details before sending the command. Omitting a field leaves it unchanged only if the reader supports partial updates — confirm with `get_nameAndDescription` first.

| What You Need | Details |
|---|---|
| Name | Human-friendly reader display name (optional in schema). |
| Description | Free-text description (optional in schema). |

## 4. Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.name` | string | No | Reader display name. |
| `payload.description` | string | No | Reader description text. |

> **Note:** Use `get_nameAndDescription` before updating to preserve values you don't intend to change.
