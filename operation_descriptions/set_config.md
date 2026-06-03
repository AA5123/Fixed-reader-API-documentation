# set_config

## 1. Description

The `set_config` command updates the reader's full configuration, including RF/XML settings, GPIO and LED defaults, and reader-gateway endpoint configuration.

Use it to:

- Push a complete or partial reader XML configuration
- Configure GPIO/LED default states and event-triggered actions
- Set tag-data retention, batching, and data/management endpoint connections

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Reader Configuration Update |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_config](get_config.md), [set_importCloudConfig](set_importCloudConfig.md), [get_status](get_status.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Update reader configuration |
| Supported API Versions | V1.0 |

> **Security Note:** Endpoint connections may include TLS certificates and authentication credentials. Never hardcode sensitive values in your payload. Supply them at runtime from a secrets manager or environment variable.

## 3. Before You Begin

Gather these details before sending the command. An invalid XML string or misconfigured endpoint can disrupt tag reporting and management events.

| What You Need | Details |
|---|---|
| Configuration scope | Full `xml` string and/or partial `GPIO-LED` / `READER-GATEWAY` objects. |
| GPIO/LED defaults | Desired GPO pin defaults (`HIGH`/`LOW`) and LED colors per pin. |
| Endpoint connections | Data and management channel types (`mqtt`, `httpPost`, `tcpip-server`, etc.) with host, port, and security. |
| Certificates | Pre-installed or inline PEM content for TLS endpoints (see `get_certs`). |

## 4. Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.xml` | string | No | Full reader XML configuration string. |
| `payload.GPIO-LED.GPODefaults` | object | No | Default GPO states (`HIGH`/`LOW`) per pin `1`–`4`. |
| `payload.GPIO-LED.LEDDefaults` | object | No | Default LED color (`GREEN`/`RED`/`AMBER`) for pin 3. |
| `payload.GPIO-LED.GPIDebounce` | object | No | GPI debounce interval (ms) per pin. |
| `payload.READER-GATEWAY.retention` | object | No | Event retention (`throttle`, `maxNumEvents`, `maxEventRetentionTimeInMin`). |
| `payload.READER-GATEWAY.batching` | object | No | Tag-data batching (`reportingInterval`, `maxPayloadSizePerReport`). |
| `payload.READER-GATEWAY.managementEventConfig` | object | No | Async management events (errors, warnings, heartbeat, GPI, userapp). |
| `payload.READER-GATEWAY.endpointConfig.data.event` | object | No | Tag data event endpoint `connections[]` array. |
| `payload.READER-GATEWAY.endpointConfig.*.connections[].type` | string | No | Connection type: `mqtt`, `httpPost`, `tcpip-server`, `WEBSOCKET`, etc. |
| `payload.READER-GATEWAY.endpointConfig.*.connections[].options` | object | No | Type-specific connection options (host, port, security, topics). |

> **Note:** Use `get_config` before `set_config` to export the current configuration and avoid overwriting active settings. See the **Schema** tab for the complete nested structure.
