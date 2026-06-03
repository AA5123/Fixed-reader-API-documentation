# set_network

## 1. Description

The `set_network` command configures the reader's network identity and IP settings (DHCP or static).

Use it to:

- Set the reader hostname and MAC-referenced network parameters
- Enable DHCP or configure static IPv4 addressing
- Update gateway, subnet mask, and DNS for static deployments

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Network Configuration |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_network](get_network.md), [set_hostname](set_hostname.md), [get_hostname](get_hostname.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Configure network addressing |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Gather these details before sending the command. A wrong static IP or gateway can disconnect the reader from your network.

| What You Need | Details |
|---|---|
| Hostname | Desired reader hostname. |
| MAC address | Reader MAC address (as reported by `get_network`). |
| DHCP vs static | `dhcp: true` for automatic addressing, or `false` with full static details. |
| Static IP details | If DHCP disabled: `ipAddress`, `gatewayAddress`, `subnetMask`, `dnsAddress`. |

## 4. Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.hostName` | string | Yes | Reader hostname. |
| `payload.dhcp` | boolean | Yes | `true` — use DHCP. `false` — use static IP fields below. |
| `payload.macAddress` | string | Yes | Reader MAC address. |
| `payload.ipAddress` | string | If `dhcp` is false | Static IPv4 address. |
| `payload.gatewayAddress` | string | If `dhcp` is false | Default gateway IP. |
| `payload.subnetMask` | string | If `dhcp` is false | Subnet mask. |
| `payload.dnsAddress` | string | If `dhcp` is false | DNS server IP. |

> **Note:** Use `get_network` before `set_network` to capture current addressing. Ensure you retain a path to reach the reader after changing IP settings.
