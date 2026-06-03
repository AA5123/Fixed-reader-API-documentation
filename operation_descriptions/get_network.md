# get_network

## 1. Description

The `get_network` command retrieves the reader's network configuration across its interfaces.

This command returns:

- The device hostname
- Ethernet (`eth0`) interface configuration and status
- Wi-Fi (`mlan0`) interface configuration

No additional payload fields are required to retrieve the full network configuration.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Network Configuration Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | set_network, get_hostname, get_networkInterfaces |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve active network configuration |
| Supported Response Sections | hostName, networkInterface |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_network` to:

- Confirm the reader's IP addressing before changing it
- Verify which interface (Ethernet/Wi-Fi) is connected
- Audit network identity (hostname) across devices
- Review interface status during connectivity troubleshooting

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `hostName` | Device hostname | Identifies the reader on the network |
| `networkInterface.eth0.IPV4.ipAddress` | Static IPv4 address | Confirms addressing for Ethernet |
| `networkInterface.eth0.Status` | Interface connectivity status | Shows whether the link is up |
| `networkInterface.mlan0` | Wi-Fi interface configuration | Confirms wireless settings when used |

> **Note:** Use `get_network` before `set_network` to review existing addressing and avoid losing connectivity to the reader.
