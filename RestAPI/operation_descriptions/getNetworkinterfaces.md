The `GET /cloud/networkInterfaces` endpoint retrieves the list of physical and virtual network interfaces currently available on the reader.

This endpoint returns:
- An array of active network interface identifiers (e.g., Ethernet, Wi-Fi, Bluetooth, Cellular).

This is a stateless REST operation and does not require any request body payload.

### When to Use This Endpoint
Use `GET /cloud/networkInterfaces` to:
- Verify which network adapters are physically present and recognized by the reader's operating system via HTTP/HTTPS.
- Check for specific connectivity capabilities (like Wi-Fi or Cellular) before attempting to programmatically apply a network configuration.
- Validate network hardware availability during initial web-based provisioning or remote troubleshooting.

### Key Fields to Check in the Response Payload

| Field | What to Check | Why It Matters |
|---|---|---|
| `availableNetworkInterfaces` | The array of interface strings returned | Dictates the network paths the reader can currently utilize to connect to the cloud or local network. |

> **Note:** The interface strings returned by the reader map to standard Linux network interface naming conventions:
> * **`eth0`**: Primary wired Ethernet
> * **`mlan0`**: Wireless LAN (Wi-Fi)
> * **`bnep0`**: Bluetooth Network Encapsulation Protocol (Bluetooth PAN)
> * **`uap0`**: Micro Access Point (Reader acting as a Wi-Fi hotspot)
> * **`wan0`**: Wide Area Network (Cellular/LTE)
