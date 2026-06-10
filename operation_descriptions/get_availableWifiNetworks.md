# get_availableWifiNetworks

## 1. Description

The `get_availableWifiNetworks` command triggers a Wi-Fi scan and retrieves a list of all visible Wi-Fi networks in the reader's vicinity. 

This command returns:
- The Extended Service Set Identifier (ESSID) of each network.
- The current signal strength (as a percentage).
- The security protocols and capabilities supported by the access point (e.g., WPA2, WPA3, 802.1X).
- Any existing saved configuration profiles on the reader for these networks (including auto-connect behavior and enterprise security details).

No additional payload fields are required in the request to initiate the scan.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Wi-Fi Site Survey |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | get_networkInterfaces, get_network, set_network |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve visible Wi-Fi networks and local configurations |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_availableWifiNetworks` to:
- Perform a remote site survey to evaluate Wi-Fi coverage and visibility in the reader's physical location.
- Troubleshoot wireless connectivity issues by verifying if the target network is broadcasting and has adequate signal strength.
- Identify the security protocols mandated by the local access points (e.g., WPA3-Enterprise, OWE) before pushing a new network configuration.
- Audit the reader's saved profiles to see which networks are configured to `autoConnect`.

Key fields to check in the response payload:

| Field | What to Check | Why It Matters |
|---|---|---|
| `essid` | The broadcast name of the network | Verifies that the desired infrastructure network is actively visible to the reader. |
| `signalStrength` | The percentage of signal quality | A weak signal (e.g., < 60%) can lead to dropped connections or failed inventory uploads. |
| `capabilities` | The array of security protocols | Dictates how the reader must be configured (e.g., PSK vs. PEAP/TLS) to successfully authenticate. |
| `configuration` | The reader's saved profile data | Shows if `autoConnect` is enabled for a network and validates enterprise certificate/auth settings. |

> **Note:** The response may contain multiple entries with the same `essid` if there are multiple access points broadcasting the same network name with different security capabilities or on different frequencies (e.g., 2.4GHz vs 5GHz).
