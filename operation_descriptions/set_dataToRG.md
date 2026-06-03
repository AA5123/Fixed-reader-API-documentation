# set_dataToRG

## 1. Description

The `set_dataToRG` command sends data to the reader gateway (RG) for processing or forwarding.

Use it to:

- Push application data into the reader gateway layer
- Integrate custom data flows with tag reporting pipelines
- Forward structured payloads for gateway-side handling

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Reader Gateway Data Injection |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [set_req_usr_app](set_req_usr_app.md), [get_config](get_config.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Send data to reader gateway |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Prepare the data payload structure required by your integration before sending.

> **Note:** Request and response schemas for this command are not yet available in `Command Schemas.json` / `Response Schemas.json`. Field details will be added when Zebra publishes them.
