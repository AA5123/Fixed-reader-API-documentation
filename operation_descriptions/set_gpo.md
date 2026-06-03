# set_gpo

## 1. Description

The `set_gpo` command sets the output state of a general-purpose output (GPO) pin on the reader.

Use it to:

- Drive an external device (light stack, horn, gate) via a GPO pin
- Toggle a single GPO pin HIGH or LOW
- Reflect application logic on physical outputs

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | GPO Control |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_gpostatus](get_gpostatus.md), [get_gpi_status](get_gpi_status.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Set a single GPO pin state |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Gather these details before sending the command. Targeting a port beyond the model's capacity will be rejected.

| What You Need | Details |
|---|---|
| Port number | GPO port ID (1–4; max depends on model — see `get_readerCapabilites`). |
| State | Desired output state (`true` = HIGH, `false` = LOW). |

## 4. Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.port` | integer | Yes | GPO port ID (1–4; device-dependent maximum). |
| `payload.state` | boolean | Yes | `true` — drive port HIGH. `false` — drive port LOW (default `false`). |
